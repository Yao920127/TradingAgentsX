"""
需要金鑰的社群來源（皆為選用，未設定金鑰就略過）：

- StockTwits  經 Apify 的 fetch_cat/stocktwits-scraper 擷取（APIFY_API_TOKEN）
              每則貼文帶有使用者自標的 bullish / bearish，可直接計算多空比
- X(Twitter)  經 Apify 的 apidojo/tweet-scraper 擷取（APIFY_API_TOKEN）
              Apify 免費方案不能透過 API 使用；每次查詢至少 50 則
- LunarCrush  API v4（LUNARCRUSH_API_KEY），社群端點需付費方案
              官方文件為前端渲染，欄位未能逐一確認，因此採寬鬆解析
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from .news_models import NewsProviderError, require_env_key, truncate

APIFY_SYNC_URL = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
STOCKTWITS_ACTOR = "fetch_cat~stocktwits-scraper"
X_ACTOR = "apidojo~tweet-scraper"
APIFY_RUN_TIMEOUT = 90  # Apify 端執行上限（秒）
STOCKTWITS_MESSAGES = 50
X_TWEETS = 50  # Tweet Scraper V2 每次查詢最少 50 則
SHOWN_POSTS = 8
SNIPPET_LIMIT = 240

LUNARCRUSH_BASE = "https://lunarcrush.com/api4/public"

SourceResult = tuple[str, str]


def _run_apify_actor(actor: str, payload: dict, provider: str) -> list[dict]:
    token = require_env_key("Apify", "APIFY_API_TOKEN", "APIFY_TOKEN")
    try:
        response = requests.post(
            APIFY_SYNC_URL.format(actor=actor),
            params={"timeout": APIFY_RUN_TIMEOUT},
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
            timeout=APIFY_RUN_TIMEOUT + 15,
        )
    except requests.RequestException as e:
        raise NewsProviderError(f"{provider} 連線失敗：{e}") from e
    if response.status_code in (401, 402, 403):
        raise NewsProviderError(f"{provider} 金鑰無效、額度不足或方案不支援 API（HTTP {response.status_code}）")
    if not response.ok:
        raise NewsProviderError(f"{provider} 執行失敗（HTTP {response.status_code}）：{truncate(response.text, 160)}")
    items = response.json()
    return items if isinstance(items, list) else []


# ---------------------------------------------------------------- StockTwits（Apify）

def stocktwits_messages(ticker: str) -> SourceResult:
    if ticker.isdigit():
        return "StockTwits：不適用（台股代碼不在 StockTwits）", ""
    items = _run_apify_actor(
        STOCKTWITS_ACTOR,
        {"symbols": [ticker], "maxMessagesPerSymbol": STOCKTWITS_MESSAGES, "continueOnError": True},
        "StockTwits（Apify）",
    )
    messages = [m for m in items if m.get("body")]
    if not messages:
        return "StockTwits：0 則", ""
    bullish = sum(1 for m in messages if m.get("sentiment") == "bullish")
    bearish = sum(1 for m in messages if m.get("sentiment") == "bearish")
    labeled = bullish + bearish
    ratio = f"看多 {bullish / labeled:.0%}／看空 {bearish / labeled:.0%}" if labeled else "無多空標記"
    top = sorted(messages, key=lambda m: m.get("likes") or 0, reverse=True)[:SHOWN_POSTS]
    lines = [
        "## StockTwits 散戶貼文（使用者自標多空）",
        f"最新 {len(messages)} 則：看多 {bullish} 則、看空 {bearish} 則、未標記 {len(messages) - labeled} 則（{ratio}）",
        *(
            f"- [{m.get('sentiment') or '未標記'}]｜{(m.get('createdAt') or '')[:10]}｜"
            f"{m.get('likes') or 0} 讚｜{truncate(m['body'], SNIPPET_LIMIT)}"
            for m in top
        ),
    ]
    return f"StockTwits：{len(messages)} 則", "\n".join(lines)


# ---------------------------------------------------------------- X / Twitter（Apify）

def _tweet_date(raw: str) -> str:
    # 範例格式：Fri Nov 24 17:49:36 +0000 2023
    try:
        return datetime.strptime(raw, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return ""


def x_posts(ticker: str, keyword: str, start: str, end: str) -> SourceResult:
    cashtag = "" if ticker.isdigit() else f" OR ${ticker}"
    query = f'("{keyword}"{cashtag}) lang:en since:{start} until:{end} -filter:retweets'
    items = _run_apify_actor(
        X_ACTOR, {"searchTerms": [query], "maxItems": X_TWEETS, "sort": "Latest"}, "X（Apify）"
    )
    tweets = [t for t in items if t.get("text") and not t.get("isRetweet")]
    if not tweets:
        return "X：0 則", ""
    engagement = lambda t: (t.get("likeCount") or 0) + 2 * (t.get("retweetCount") or 0) + (t.get("replyCount") or 0)
    top = sorted(tweets, key=engagement, reverse=True)[:SHOWN_POSTS]
    lines = [
        f"## X（Twitter）貼文（{len(tweets)} 則，依互動數排序）",
        *(
            f"- {_tweet_date(t.get('createdAt', ''))}｜@{(t.get('author') or {}).get('userName', '')}｜"
            f"{t.get('likeCount') or 0} 讚、{t.get('retweetCount') or 0} 轉推、{t.get('replyCount') or 0} 回覆｜"
            f"{truncate(t['text'], SNIPPET_LIMIT)}"
            for t in top
        ),
    ]
    return f"X：{len(tweets)} 則", "\n".join(lines)


# ---------------------------------------------------------------- LunarCrush

def _flatten_metrics(data: dict[str, Any]) -> list[str]:
    """取出數值與短字串欄位，以及一層的 dict（例如各平台情緒），交給 LLM 解讀。"""
    lines = []
    for key, value in data.items():
        if isinstance(value, bool) or value is None:
            continue
        if isinstance(value, (int, float)) or (isinstance(value, str) and len(value) <= 60):
            lines.append(f"- {key}: {value}")
        elif isinstance(value, dict) and all(isinstance(v, (int, float)) for v in value.values()):
            lines.append(f"- {key}: " + ", ".join(f"{k}={v}" for k, v in value.items()))
    return lines


def lunarcrush_topic(ticker: str, keyword: str) -> SourceResult:
    api_key = require_env_key("LunarCrush", "LUNARCRUSH_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    topics = ([f"${ticker.lower()}"] if not ticker.isdigit() else []) + [keyword.lower()]
    last_error = ""
    for topic in topics:
        try:
            response = requests.get(f"{LUNARCRUSH_BASE}/topic/{topic}/v1", headers=headers, timeout=15)
        except requests.RequestException as e:
            last_error = f"連線失敗：{e}"
            continue
        if response.status_code in (401, 402, 403):
            raise NewsProviderError(f"LunarCrush 金鑰無效或方案不含社群端點（HTTP {response.status_code}）")
        if not response.ok:
            last_error = f"HTTP {response.status_code}"
            continue
        data = (response.json() or {}).get("data") or {}
        metrics = _flatten_metrics(data) if isinstance(data, dict) else []
        if metrics:
            block = f"## LunarCrush 社群指標（主題 {topic}；涵蓋 X、Reddit、YouTube、TikTok 等）\n" + "\n".join(metrics)
            return f"LunarCrush：主題 {topic}", block
    raise NewsProviderError(f"找不到主題資料（{last_error or '無資料'}）")
