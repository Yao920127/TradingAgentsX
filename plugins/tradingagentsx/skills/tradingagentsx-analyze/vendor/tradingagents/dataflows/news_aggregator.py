"""
多來源新聞聚合（vendor 名稱："aggregator"）。

同時查詢 Finnhub / Marketaux / NewsAPI / GDELT，去重後依時間排序，
再以 Jina Reader 補上前幾則的全文摘錄。任一來源失敗不影響其他來源；
全部來源都沒有結果時才拋出例外，讓 route_to_vendor 繼續備援到其他供應商。
"""
from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from . import news_providers as providers
from .jina_reader import enrich_with_content
from .news_models import (
    Article,
    NewsProviderError,
    date_window,
    dedupe_articles,
    format_articles,
    resolve_company_name,
    search_name,
    sort_by_date,
)

MAX_ARTICLES = 15
PER_PROVIDER_LIMIT = 10
JINA_TOP_N = 3
GDELT_MIN_INTERVAL = 5.0
GDELT_ATTEMPTS = 2  # 被限流時等待間隔後重試一次

_gdelt_lock = threading.Lock()
_gdelt_last_call = 0.0

ProviderCall = tuple[str, Callable[[], list[Article]]]


def _throttled_gdelt(*args) -> list[Article]:
    """GDELT 限制每 5 秒 1 次，並行查詢時需排隊；被限流時等待後重試一次。"""
    global _gdelt_last_call
    with _gdelt_lock:
        for attempt in range(GDELT_ATTEMPTS):
            wait = GDELT_MIN_INTERVAL - (time.monotonic() - _gdelt_last_call)
            if wait > 0:
                time.sleep(wait)
            try:
                return providers.gdelt_news(*args)
            except NewsProviderError as e:
                if "速率限制" not in str(e) or attempt == GDELT_ATTEMPTS - 1:
                    raise
            finally:
                _gdelt_last_call = time.monotonic()
        return []


def _yf_symbol(ticker: str) -> str:
    """台股代碼（純數字）在 yfinance 需加 .TW 才查得到公司名稱。"""
    return f"{ticker}.TW" if ticker.isdigit() else ticker


def _company_query(ticker: str) -> tuple[str, str]:
    """回傳 (顯示名稱, 搜尋關鍵字)。"""
    name = resolve_company_name(_yf_symbol(ticker))
    keyword = search_name(name) if name and name != _yf_symbol(ticker) else ticker
    return name, keyword


def _run_providers(calls: list[ProviderCall]) -> tuple[list[Article], list[str]]:
    """並行呼叫各來源，回傳 (依呼叫順序合併的文章, 各來源狀態說明)。"""

    def run(call: ProviderCall) -> tuple[str, list[Article], str]:
        label, fn = call
        try:
            articles = fn()
            return label, articles, f"{label}：{len(articles)} 則"
        except NewsProviderError as e:
            return label, [], f"{label}：無法使用（{e}）"
        except Exception as e:  # 未預期錯誤也不能拖垮整個新聞查詢
            return label, [], f"{label}：失敗（{type(e).__name__}: {e}）"

    with ThreadPoolExecutor(max_workers=len(calls)) as pool:
        outcomes = list(pool.map(run, calls))
    articles = [a for _, found, _ in outcomes for a in found]
    statuses = [status for _, _, status in outcomes]
    return articles, statuses


def _build_report(articles: list[Article], statuses: list[str], heading: str, limit: int) -> str:
    ranked = sort_by_date(dedupe_articles(articles))[:limit]
    if not ranked:
        raise NewsProviderError("所有新聞來源皆無結果 — " + "；".join(statuses))
    ranked = enrich_with_content(ranked, JINA_TOP_N)
    status_block = "\n".join(f"- {s}" for s in statuses)
    return f"{format_articles(ranked, heading)}\n\n## 資料來源狀態\n{status_block}"


def get_news(ticker: str, start_date: str, end_date: str) -> str:
    """個股新聞：代碼查詢（Finnhub、Marketaux）＋公司名稱關鍵字查詢（NewsAPI、GDELT）。"""
    ticker = ticker.strip().upper()
    name, keyword = _company_query(ticker)
    phrase = f'"{keyword}"' if " " in keyword else keyword

    def marketaux() -> list[Article]:
        found = providers.marketaux_news(start_date, end_date, PER_PROVIDER_LIMIT, symbols=[ticker])
        # 代碼未收錄（常見於非美股）時改用公司名稱搜尋
        return found or providers.marketaux_news(start_date, end_date, PER_PROVIDER_LIMIT, search=phrase)

    calls: list[ProviderCall] = [
        ("Finnhub", lambda: providers.finnhub_company_news(ticker, start_date, end_date, PER_PROVIDER_LIMIT)),
        ("Marketaux", marketaux),
        ("NewsAPI", lambda: providers.newsapi_everything(phrase, start_date, end_date, PER_PROVIDER_LIMIT)),
        # 只取英文來源：多語系結果雜訊多（例如只順帶提到公司名的地方新聞）
        ("GDELT", lambda: _throttled_gdelt(f"{phrase} sourcelang:english", start_date, end_date, PER_PROVIDER_LIMIT)),
    ]
    articles, statuses = _run_providers(calls)
    heading = f"{name}（{ticker}）新聞 {start_date} ~ {end_date}"
    return _build_report(articles, statuses, heading, MAX_ARTICLES)


GLOBAL_GDELT_QUERY = '(economy OR "stock market" OR "federal reserve" OR inflation) sourcelang:english'


def get_global_news(curr_date: str, look_back_days: int = 7, limit: int = 10) -> str:
    """總體經濟與市場新聞。"""
    start_date, end_date = date_window(curr_date, int(look_back_days))
    limit = max(1, min(int(limit), MAX_ARTICLES))
    calls: list[ProviderCall] = [
        ("Finnhub", lambda: providers.finnhub_general_news(PER_PROVIDER_LIMIT)),
        ("NewsAPI", lambda: providers.newsapi_business_headlines(PER_PROVIDER_LIMIT)),
        ("Marketaux", lambda: providers.marketaux_news(start_date, end_date, PER_PROVIDER_LIMIT, search="stock market")),
        ("GDELT", lambda: _throttled_gdelt(GLOBAL_GDELT_QUERY, start_date, end_date, PER_PROVIDER_LIMIT)),
    ]
    articles, statuses = _run_providers(calls)
    # Finnhub / NewsAPI 頭條不支援日期區間，這裡過濾掉分析日期之後的新聞，避免前視偏差
    in_window = [a for a in articles if not a.published_at or a.published_at[:10] <= end_date]
    return _build_report(in_window, statuses, f"全球市場新聞 {start_date} ~ {end_date}", limit)
