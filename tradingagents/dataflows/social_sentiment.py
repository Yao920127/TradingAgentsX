"""
社群情緒資料聚合（get_social_sentiment）。

分兩階段查詢，先免費、後付費（單一來源失敗不影響其他來源）：

第一階段：免費來源（同時查詢）
- ApeWisdom    Reddit 各股討論熱度排名（免金鑰，美股）
- Hacker News  科技社群討論與留言（免金鑰，適合科技 / 半導體股；以 Jina Reader 擷取討論連結的原始文章）
- PTT 股票板   台股散戶討論（免金鑰，台股；以 Jina Reader 擷取內文）
- Reddit       官方 API（免費，需 REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET）

第二階段：付費來源（只有第一階段完全沒有實質資料時才啟用）
- StockTwits / X  經 Apify 擷取，按用量計費（APIFY_API_TOKEN）
- LunarCrush      社群端點需付費方案（LUNARCRUSH_API_KEY）
- Jina 搜尋       以 s.jina.ai 搜尋 Reddit / X 貼文，消耗 Jina 額度（JINA_API_KEY）

新聞情緒分數（Marketaux）屬於新聞面，由新聞分析師使用，這裡不重複計入。
Reddit 與 StockTwits 的公開端點會對伺服器回傳 403，因此不採用免金鑰爬取。
"""
from __future__ import annotations

import html
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Callable

import requests

from .jina_reader import read_article, read_urls
from .social_paid_sources import lunarcrush_topic, stocktwits_messages, x_posts
from .news_models import (
    REQUEST_TIMEOUT,
    USER_AGENT,
    NewsProviderError,
    date_window,
    get_env_key,
    resolve_company_name,
    search_name,
    truncate,
)

ITEM_LIMIT = 8
SNIPPET_LIMIT = 280
APEWISDOM_PAGES = 3
HN_COMMENT_STORIES = 2
HN_COMMENTS_PER_STORY = 3
PTT_JINA_POSTS = 2
REDDIT_JINA_LINKS = 2  # 連到外部文章的 Reddit 貼文，讀取前幾篇原始文章
REDDIT_OWN_DOMAINS = ("reddit.com", "redd.it")  # 圖片、相簿、站內連結不是外部文章
REDDIT_SUBREDDITS = "stocks+investing+wallstreetbets+StockMarket+ValueInvesting"

APEWISDOM_UNRANKED = "ApeWisdom：未上榜"

SourceResult = tuple[str, str]  # (來源狀態, 內容區塊；無資料時為空字串)


def _get(url: str, provider: str, **kwargs) -> requests.Response:
    headers = {"User-Agent": USER_AGENT, **kwargs.pop("headers", {})}
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, **kwargs)
    except requests.RequestException as e:
        raise NewsProviderError(f"{provider} 連線失敗：{e}") from e
    if not response.ok:
        raise NewsProviderError(f"{provider} 回應錯誤（HTTP {response.status_code}）")
    return response


def _strip_html(text: str) -> str:
    return truncate(html.unescape(re.sub(r"<[^>]+>", " ", text or "")), SNIPPET_LIMIT)


def _epoch(date_str: str, end_of_day: bool = False) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp()) + (86399 if end_of_day else 0)


# ---------------------------------------------------------------- ApeWisdom（Reddit 討論熱度）

def apewisdom_rank(ticker: str) -> SourceResult:
    if ticker.isdigit():
        return "ApeWisdom：不適用（僅涵蓋美股）", ""
    for page in range(1, APEWISDOM_PAGES + 1):
        data = _get(f"https://apewisdom.io/api/v1.0/filter/all-stocks/page/{page}", "ApeWisdom").json()
        for row in data.get("results") or []:
            if row.get("ticker", "").upper() == ticker:
                block = (
                    "## Reddit 討論熱度（ApeWisdom，近 24 小時）\n"
                    f"排名第 {row.get('rank')}（24 小時前第 {row.get('rank_24h_ago')}）｜"
                    f"提及 {row.get('mentions')} 次（24 小時前 {row.get('mentions_24h_ago')} 次）｜"
                    f"讚數 {row.get('upvotes')}"
                )
                return "ApeWisdom：有排名", block
    note = f"## Reddit 討論熱度（ApeWisdom）\n{ticker} 未進入 Reddit 討論熱度前 {APEWISDOM_PAGES * 100} 名，散戶關注度低。"
    return APEWISDOM_UNRANKED, note


# ---------------------------------------------------------------- Hacker News

def _hn_comments(story_id: str) -> list[str]:
    data = _get(f"https://hn.algolia.com/api/v1/items/{story_id}", "Hacker News").json()
    texts = [_strip_html(c.get("text", "")) for c in data.get("children") or [] if c.get("text")]
    return texts[:HN_COMMENTS_PER_STORY]


def hacker_news(keyword: str, start: str, end: str) -> SourceResult:
    data = _get(
        "https://hn.algolia.com/api/v1/search_by_date",
        "Hacker News",
        params={
            "query": keyword,
            "tags": "story",
            "hitsPerPage": ITEM_LIMIT,
            "numericFilters": f"created_at_i>={_epoch(start)},created_at_i<={_epoch(end, True)}",
        },
    ).json()
    hits = sorted(data.get("hits") or [], key=lambda h: h.get("num_comments") or 0, reverse=True)
    if not hits:
        return "Hacker News：0 則", ""
    top = hits[:HN_COMMENT_STORIES]
    # 討論最熱的幾則：同時抓留言（Algolia API）與討論所連結的原始文章（Jina Reader）
    with ThreadPoolExecutor(max_workers=HN_COMMENT_STORIES * 2) as pool:
        comment_jobs = [pool.submit(_hn_comments, h["objectID"]) for h in top]
        article_jobs = [pool.submit(read_article, h["url"]) if h.get("url") else None for h in top]
        comments = [job.result() for job in comment_jobs]
        articles = [job.result() if job else "" for job in article_jobs]
    lines = ["## Hacker News 科技社群討論"]
    for i, hit in enumerate(hits):
        lines.append(
            f"- {hit.get('created_at', '')[:10]}｜{hit.get('title')}｜"
            f"{hit.get('points') or 0} 分、{hit.get('num_comments') or 0} 則留言"
        )
        if i < len(top):
            if articles[i]:
                lines.append(f"  > 原始文章摘錄：{truncate(articles[i], SNIPPET_LIMIT * 2)}")
            lines.extend(f"  > 留言：{c}" for c in comments[i])
    return f"Hacker News：{len(hits)} 則", "\n".join(lines)


# ---------------------------------------------------------------- PTT 股票板（台股）

_PTT_ENTRY = re.compile(
    r'<div class="nrec">(?:<span[^>]*>([^<]*)</span>)?</div>.*?'
    r'<a href="(/bbs/Stock/M\.[^"]+\.html)">([^<]+)</a>.*?<div class="date">\s*([^<]+)</div>',
    re.S,
)


# PTT 文章頁開頭的看板／作者／時間資訊，到「時間 Mon Oct 26 15:58:56 2026」為止
_PTT_BOILERPLATE = re.compile(r"^.*?時間\s+\w{3}\s+\w{3}\s+\d+\s+[\d:]+\s+\d{4}\s*", re.S)


def _clean_ptt_body(text: str) -> str:
    """去掉看板資訊與文末簽名檔，只留本文。"""
    return _PTT_BOILERPLATE.sub("", text).split("※ 發信站")[0].rstrip(" -")


def _ptt_date(month_day: str, end: str) -> str:
    """PTT 列表日期只有「M/DD」，以分析日期推回年份（月份大於分析月份 → 去年）。"""
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    month, day = (int(x) for x in month_day.split("/"))
    year = end_dt.year if month <= end_dt.month else end_dt.year - 1
    return f"{year:04d}-{month:02d}-{day:02d}"


def ptt_stock(ticker: str, start: str, end: str) -> SourceResult:
    if not ticker.isdigit():
        return "PTT：不適用（僅涵蓋台股）", ""
    page = _get(
        "https://www.ptt.cc/bbs/Stock/search", "PTT", params={"q": ticker}, cookies={"over18": "1"}
    ).text
    posts = [
        {"push": push or "0", "url": f"https://www.ptt.cc{path}", "title": html.unescape(title), "date": _ptt_date(date.strip(), end)}
        for push, path, title, date in _PTT_ENTRY.findall(page)
    ]
    posts = [p for p in posts if start <= p["date"] <= end][:ITEM_LIMIT]
    if not posts:
        return "PTT：0 則", ""
    with ThreadPoolExecutor(max_workers=PTT_JINA_POSTS) as pool:
        bodies = list(pool.map(lambda p: _clean_ptt_body(read_article(p["url"])), posts[:PTT_JINA_POSTS]))
    lines = ["## PTT 股票板討論（推文數｜日期｜標題）"]
    for i, post in enumerate(posts):
        lines.append(f"- {post['push']}｜{post['date']}｜{post['title']}")
        if i < len(bodies) and bodies[i]:
            lines.append(f"  > 內文摘錄：{truncate(bodies[i], SNIPPET_LIMIT * 2)}")
    return f"PTT：{len(posts)} 則", "\n".join(lines)


# ---------------------------------------------------------------- Reddit 官方 API（選用）

def reddit_posts(ticker: str, keyword: str) -> SourceResult:
    client_id = get_env_key("REDDIT_CLIENT_ID")
    client_secret = get_env_key("REDDIT_CLIENT_SECRET")
    if not (client_id and client_secret):
        raise NewsProviderError("未設定 REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET")
    import praw

    reddit = praw.Reddit(
        client_id=client_id, client_secret=client_secret, user_agent=USER_AGENT, check_for_async=False
    )
    query = f'"{keyword}" OR {ticker}' if keyword != ticker else ticker
    submissions = list(
        reddit.subreddit(REDDIT_SUBREDDITS).search(query, sort="new", time_filter="month", limit=ITEM_LIMIT)
    )
    if not submissions:
        return "Reddit：0 則", ""
    # 連結型貼文（非純文字貼文）以 Jina Reader 讀取它分享的原始文章
    link_posts = [
        s for s in submissions
        if not s.is_self and s.url and not any(d in s.url for d in REDDIT_OWN_DOMAINS)
    ][:REDDIT_JINA_LINKS]
    linked = dict(zip((s.id for s in link_posts), read_urls([s.url for s in link_posts])))
    lines = ["## Reddit 貼文（分數｜留言數｜看板｜標題）"]
    for s in submissions:
        lines.append(f"- {s.score}｜{s.num_comments}｜r/{s.subreddit.display_name}｜{s.title}")
        if s.selftext:
            lines.append(f"  > {truncate(s.selftext, SNIPPET_LIMIT)}")
        if linked.get(s.id):
            lines.append(f"  > 分享文章摘錄：{truncate(linked[s.id], SNIPPET_LIMIT * 2)}")
    return f"Reddit：{len(submissions)} 則", "\n".join(lines)


# ---------------------------------------------------------------- Jina 搜尋（Reddit / X 備援）

def jina_social_search(keyword: str) -> SourceResult:
    api_key = get_env_key("JINA_API_KEY")
    if not api_key:
        raise NewsProviderError("未設定 JINA_API_KEY（Jina 搜尋需要金鑰）")
    response = _get(
        "https://s.jina.ai/",
        "Jina 搜尋",
        params={"q": f'"{keyword}" stock (site:reddit.com OR site:x.com)'},
        # 不加 X-Respond-With: no-content，讓 Jina 一併回傳搜尋結果頁面的內文
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    results = (response.json().get("data") or [])[:ITEM_LIMIT]
    if not results:
        return "Jina 搜尋：0 則", ""
    lines = ["## Jina 搜尋：Reddit / X 社群貼文"]
    for r in results:
        lines.append(f"- {r.get('title', '')}（{r.get('url', '')}）")
        text = r.get("content") or r.get("description")
        if text:
            lines.append(f"  > {truncate(text, SNIPPET_LIMIT * 2)}")
    return f"Jina 搜尋：{len(results)} 則", "\n".join(lines)


# ---------------------------------------------------------------- 對外入口

def _safe(label: str, fn: Callable[[], SourceResult]) -> SourceResult:
    try:
        return fn()
    except NewsProviderError as e:
        return f"{label}：無法使用（{e}）", ""
    except Exception as e:
        return f"{label}：失敗（{type(e).__name__}: {e}）", ""


def _run_sources(sources: list[tuple[str, Callable[[], SourceResult]]]) -> list[SourceResult]:
    with ThreadPoolExecutor(max_workers=len(sources)) as pool:
        return list(pool.map(lambda c: _safe(*c), sources))


def _has_substance(outcomes: list[SourceResult]) -> bool:
    """「未進入熱度排行」只是弱訊號，不算真正的社群資料。"""
    return any(block and not status.startswith(APEWISDOM_UNRANKED) for status, block in outcomes)


NO_DATA_NOTICE = (
    "【社群資料不足】所有社群來源都沒有找到這檔股票的討論或情緒資料。"
    "請在報告中直接說明資料不足、情緒面維持中性，不要推測或編造任何情緒結論，報告以 150 字以內為限。"
)


def get_social_sentiment(ticker: str, curr_date: str, look_back_days: int = 14) -> str:
    ticker = ticker.strip().upper()
    start, end = date_window(curr_date, int(look_back_days))
    yf_symbol = f"{ticker}.TW" if ticker.isdigit() else ticker
    name = resolve_company_name(yf_symbol)
    keyword = search_name(name) if name != yf_symbol else ticker

    free_sources = [
        ("ApeWisdom", lambda: apewisdom_rank(ticker)),
        ("Hacker News", lambda: hacker_news(keyword, start, end)),
        ("PTT", lambda: ptt_stock(ticker, start, end)),
        ("Reddit", lambda: reddit_posts(ticker, keyword)),
    ]
    paid_sources = [
        ("StockTwits", lambda: stocktwits_messages(ticker)),
        ("X", lambda: x_posts(ticker, keyword, start, end)),
        ("LunarCrush", lambda: lunarcrush_topic(ticker, keyword)),
        ("Jina 搜尋", lambda: jina_social_search(keyword)),
    ]

    outcomes = _run_sources(free_sources)
    if _has_substance(outcomes):
        outcomes += [(f"{label}：未啟用（免費來源已有資料，不使用付費來源）", "") for label, _ in paid_sources]
    else:
        outcomes += _run_sources(paid_sources)

    blocks = [block for _, block in outcomes if block]
    statuses = "\n".join(f"- {status}" for status, _ in outcomes)
    header = f"# {name}（{ticker}）社群情緒資料 {start} ~ {end}"
    body = "\n\n".join(blocks if _has_substance(outcomes) else [NO_DATA_NOTICE, *blocks])
    return f"{header}\n\n{body}\n\n## 資料來源狀態\n{statuses}"
