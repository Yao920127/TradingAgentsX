"""
個別新聞供應商的 HTTP 客戶端，全部回傳 list[Article]。

金鑰一律由環境變數讀取（trading_service 會把使用者 BYOK 金鑰寫入環境變數，
未提供時沿用伺服器端設定）：
- Finnhub    FINNHUB_API_KEY      免費方案：公司新聞僅限北美上市公司
- Marketaux  MARKETAUX_API_KEY    免費方案：每日 100 次、每次最多 3 則，附實體情緒分數
- NewsAPI    NEWSAPI_API_KEY      免費（Developer）方案：僅供開發用途、文章延遲 24 小時
- GDELT      免金鑰               全球多語系新聞索引，限制每 5 秒 1 次請求
"""
from __future__ import annotations

from datetime import datetime, timezone

import requests

from .news_models import (
    REQUEST_TIMEOUT,
    USER_AGENT,
    Article,
    NewsProviderError,
    require_env_key,
    truncate,
)

SUMMARY_LIMIT = 300


def _get_json(url: str, params: dict, provider: str) -> dict | list:
    try:
        response = requests.get(
            url, params=params, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        raise NewsProviderError(f"{provider} 連線失敗：{e}") from e
    if response.status_code == 429:
        raise NewsProviderError(f"{provider} 超過速率限制（HTTP 429）")
    if response.status_code in (401, 402, 403):
        raise NewsProviderError(f"{provider} 金鑰無效或方案權限不足（HTTP {response.status_code}）")
    if not response.ok:
        raise NewsProviderError(f"{provider} 回應錯誤（HTTP {response.status_code}）")
    try:
        return response.json()
    except ValueError as e:
        raise NewsProviderError(f"{provider} 回應不是 JSON：{truncate(response.text, 120)}") from e


def _unix_to_iso(ts: int | float | None) -> str:
    if not ts:
        return ""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- Finnhub

FINNHUB_BASE = "https://finnhub.io/api/v1"


def _finnhub_articles(items: list) -> list[Article]:
    return [
        Article(
            title=item.get("headline", ""),
            url=item.get("url", ""),
            source=item.get("source", ""),
            published_at=_unix_to_iso(item.get("datetime")),
            summary=truncate(item.get("summary", ""), SUMMARY_LIMIT),
            provider="finnhub",
        )
        for item in items
        if isinstance(item, dict)
    ]


def finnhub_company_news(ticker: str, start_date: str, end_date: str, limit: int) -> list[Article]:
    token = require_env_key("Finnhub", "FINNHUB_API_KEY")
    data = _get_json(
        f"{FINNHUB_BASE}/company-news",
        {"symbol": ticker, "from": start_date, "to": end_date, "token": token},
        "Finnhub",
    )
    if isinstance(data, dict) and data.get("error"):
        raise NewsProviderError(f"Finnhub：{data['error']}")
    return _finnhub_articles(data if isinstance(data, list) else [])[:limit]


def finnhub_general_news(limit: int) -> list[Article]:
    token = require_env_key("Finnhub", "FINNHUB_API_KEY")
    data = _get_json(f"{FINNHUB_BASE}/news", {"category": "general", "token": token}, "Finnhub")
    return _finnhub_articles(data if isinstance(data, list) else [])[:limit]


# ---------------------------------------------------------------- Marketaux

MARKETAUX_URL = "https://api.marketaux.com/v1/news/all"


def _marketaux_sentiment(item: dict, symbols: set[str]) -> float | None:
    scores = [
        e.get("sentiment_score")
        for e in item.get("entities") or []
        if e.get("sentiment_score") is not None and (not symbols or e.get("symbol") in symbols)
    ]
    return round(sum(scores) / len(scores), 3) if scores else None


def marketaux_news(
    start_date: str,
    end_date: str,
    limit: int,
    symbols: list[str] | None = None,
    search: str | None = None,
) -> list[Article]:
    token = require_env_key("Marketaux", "MARKETAUX_API_KEY")
    params = {
        "api_token": token,
        "language": "en",
        "published_after": f"{start_date}T00:00:00",
        "published_before": f"{end_date}T23:59:59",
        "sort": "published_at",
        "limit": min(limit, 50),
    }
    if symbols:
        params.update({"symbols": ",".join(symbols), "filter_entities": "true"})
    if search:
        params["search"] = search
    data = _get_json(MARKETAUX_URL, params, "Marketaux")
    if isinstance(data, dict) and data.get("error"):
        raise NewsProviderError(f"Marketaux：{data['error'].get('message', data['error'])}")
    symbol_set = set(symbols or [])
    return [
        Article(
            title=item.get("title", ""),
            url=item.get("url", ""),
            source=item.get("source", ""),
            published_at=item.get("published_at", ""),
            summary=truncate(item.get("description") or item.get("snippet") or "", SUMMARY_LIMIT),
            provider="marketaux",
            sentiment=_marketaux_sentiment(item, symbol_set),
        )
        for item in (data.get("data") or [] if isinstance(data, dict) else [])
    ]


# ---------------------------------------------------------------- NewsAPI.org

NEWSAPI_BASE = "https://newsapi.org/v2"


def _newsapi_articles(data: dict) -> list[Article]:
    if data.get("status") == "error":
        raise NewsProviderError(f"NewsAPI：{data.get('code')} {data.get('message', '')}")
    return [
        Article(
            title=item.get("title", ""),
            url=item.get("url", ""),
            source=(item.get("source") or {}).get("name", ""),
            published_at=item.get("publishedAt", ""),
            summary=truncate(item.get("description") or "", SUMMARY_LIMIT),
            provider="newsapi",
        )
        for item in data.get("articles") or []
        if item.get("title") and item.get("title") != "[Removed]"
    ]


def newsapi_everything(query: str, start_date: str, end_date: str, limit: int) -> list[Article]:
    key = require_env_key("NewsAPI", "NEWSAPI_API_KEY", "NEWS_API_KEY")
    data = _get_json(
        f"{NEWSAPI_BASE}/everything",
        {
            "q": query,
            "from": start_date,
            "to": end_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": min(limit, 100),
            "apiKey": key,
        },
        "NewsAPI",
    )
    return _newsapi_articles(data if isinstance(data, dict) else {})


def newsapi_business_headlines(limit: int) -> list[Article]:
    key = require_env_key("NewsAPI", "NEWSAPI_API_KEY", "NEWS_API_KEY")
    data = _get_json(
        f"{NEWSAPI_BASE}/top-headlines",
        {"category": "business", "language": "en", "pageSize": min(limit, 100), "apiKey": key},
        "NewsAPI",
    )
    return _newsapi_articles(data if isinstance(data, dict) else {})


# ---------------------------------------------------------------- GDELT（免金鑰）

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def _gdelt_date(raw: str) -> str:
    # GDELT seendate 格式：20261028T043000Z
    try:
        return datetime.strptime(raw, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return ""


def gdelt_news(query: str, start_date: str, end_date: str, limit: int) -> list[Article]:
    """全球多語系新聞，對美股、台股以外的市場（韓、日、歐）特別有用。"""
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "sort": "datedesc",
        "maxrecords": min(limit, 75),
        "startdatetime": start_date.replace("-", "") + "000000",
        "enddatetime": end_date.replace("-", "") + "235959",
    }
    try:
        response = requests.get(
            GDELT_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        raise NewsProviderError(f"GDELT 連線失敗：{e}") from e
    if response.status_code == 429 or "limit requests" in response.text[:200]:
        raise NewsProviderError("GDELT 超過速率限制（每 5 秒 1 次）")
    try:
        data = response.json()
    except ValueError as e:
        raise NewsProviderError(f"GDELT 回應不是 JSON：{truncate(response.text, 120)}") from e
    return [
        Article(
            title=item.get("title", ""),
            url=item.get("url", ""),
            source=item.get("domain", ""),
            published_at=_gdelt_date(item.get("seendate", "")),
            provider="gdelt",
        )
        for item in data.get("articles") or []
    ]
