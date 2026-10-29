"""
多來源新聞 / 社群資料的共用模型與工具。

各新聞供應商（Finnhub、Marketaux、NewsAPI、GDELT）都轉成同一個 Article，
再由 news_aggregator 統一去重、排序、格式化，避免同一則新聞重複餵給 LLM。
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Iterable, Optional

# 單一供應商 HTTP 請求逾時（秒）
REQUEST_TIMEOUT = 15
USER_AGENT = "TradingAgentsX/1.0 (+https://github.com/Yao920127/TradingAgentsX)"


class NewsProviderError(Exception):
    """供應商回傳錯誤或無法使用（缺金鑰、權限不足、配額用盡）。"""


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    source: str
    published_at: str  # ISO 8601（UTC）
    summary: str = ""
    provider: str = ""
    sentiment: Optional[float] = None  # -1 ~ 1，僅部分供應商提供
    content: str = ""  # Jina Reader 擷取的全文摘錄

    def with_content(self, content: str) -> "Article":
        return replace(self, content=content)


def get_env_key(*names: str) -> Optional[str]:
    """依序讀取環境變數，回傳第一個非空值。"""
    for name in names:
        value = (os.getenv(name) or "").strip()
        if value:
            return value
    return None


def require_env_key(provider: str, *names: str) -> str:
    key = get_env_key(*names)
    if not key:
        raise NewsProviderError(f"未設定 {provider} API 金鑰（{' / '.join(names)}）")
    return key


def date_window(curr_date: str, look_back_days: int) -> tuple[str, str]:
    """回傳 (start, end) 兩個 yyyy-mm-dd 字串。"""
    end = datetime.strptime(curr_date, "%Y-%m-%d")
    start = end - timedelta(days=look_back_days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def _normalize_title(title: str) -> str:
    return re.sub(r"[^\w]+", "", title.lower())[:80]


def dedupe_articles(articles: Iterable[Article]) -> list[Article]:
    """以 URL 與標題去重，保留先出現者（呼叫端決定供應商優先順序）。"""
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[Article] = []
    for article in articles:
        url_key = article.url.split("?")[0].rstrip("/").lower()
        title_key = _normalize_title(article.title)
        if not article.title or url_key in seen_urls or (title_key and title_key in seen_titles):
            continue
        seen_urls.add(url_key)
        if title_key:
            seen_titles.add(title_key)
        unique.append(article)
    return unique


def sort_by_date(articles: Iterable[Article]) -> list[Article]:
    return sorted(articles, key=lambda a: a.published_at or "", reverse=True)


def format_articles(articles: list[Article], heading: str) -> str:
    """格式化為精簡 Markdown，控制送進 LLM 的 token 量。"""
    lines = [f"## {heading}（共 {len(articles)} 則）", ""]
    for i, article in enumerate(articles, 1):
        meta = [article.source or article.provider, article.published_at[:10]]
        if article.sentiment is not None:
            meta.append(f"情緒分數 {article.sentiment:+.2f}")
        lines.append(f"### {i}. {article.title}")
        lines.append(f"（{' | '.join(m for m in meta if m)}）{article.url}")
        if article.summary:
            lines.append(article.summary)
        if article.content:
            lines.append(f"> 全文摘錄：{article.content}")
        lines.append("")
    return "\n".join(lines).strip()


def truncate(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


@lru_cache(maxsize=256)
def resolve_company_name(ticker: str) -> str:
    """以 yfinance 取得公司名稱，供以關鍵字搜尋的供應商使用（如 SKHY → SK hynix Inc.）。"""
    try:
        import yfinance as yf

        info = yf.Ticker(ticker).info or {}
        return info.get("longName") or info.get("shortName") or ticker
    except Exception:
        return ticker


def search_name(company_name: str) -> str:
    """去掉 Inc./Corp./Co., Ltd. 等字尾，提升關鍵字搜尋命中率。"""
    cleaned = re.sub(
        r"[,.]?\s*\b(inc|incorporated|corp|corporation|co|company|ltd|limited|plc|holdings?|group|sa|ag|nv)\b\.?",
        "",
        company_name,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s+", " ", cleaned).strip(" ,.") or company_name
