"""
Jina AI Reader（r.jina.ai）：把新聞網址轉成乾淨文字，讓 LLM 讀到內文而不只是標題。

免金鑰可用（約 20 RPM）；設定 JINA_API_KEY 後速率上限較高。
擷取失敗一律回傳原文章，不影響新聞清單本身。
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

import requests

from .news_models import Article, get_env_key, truncate

JINA_READER_URL = "https://r.jina.ai/"
JINA_TIMEOUT = 20
# 每則全文摘錄長度上限（字元），控制送進 LLM 的 token 量
CONTENT_LIMIT = 1200
MAX_WORKERS = 3

_MARKDOWN_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
# 選單 / 頁首 / 頁尾等非內文區塊（Jina 會在擷取前移除）
REMOVE_SELECTORS = "header, nav, footer, aside, form, [role=navigation], [class*=menu], [class*=nav], [class*=footer]"
# 短於此長度的條列項目多半是選單連結，不是內文
MIN_BULLET_CHARS = 40
_HEADER_LINE = re.compile(r"^(Title|URL Source|Published Time|Markdown Content):.*$", re.MULTILINE)


def _is_body_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped[:2] in ("* ", "- ", "+ ") and len(stripped) < MIN_BULLET_CHARS:
        return False
    return not set(stripped) <= set("*-=_#|> ")


def _clean(markdown: str) -> str:
    text = _HEADER_LINE.sub("", markdown)
    text = _MARKDOWN_LINK.sub(r"\1", text)
    body = "\n".join(line for line in text.splitlines() if _is_body_line(line))
    return truncate(body, CONTENT_LIMIT)


def read_article(url: str) -> str:
    headers = {
        "X-Retain-Images": "none",
        "X-Return-Format": "markdown",
        "X-Remove-Selector": REMOVE_SELECTORS,
    }
    api_key = get_env_key("JINA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"{JINA_READER_URL}{url}", headers=headers, timeout=JINA_TIMEOUT)
    except requests.RequestException:
        return ""
    if not response.ok:
        return ""
    return _clean(response.text)


def enrich_with_content(articles: list[Article], top_n: int) -> list[Article]:
    """為前 top_n 則新聞補上全文摘錄（並行擷取），其餘原樣保留。"""
    if top_n <= 0 or not articles:
        return articles
    head, tail = articles[:top_n], articles[top_n:]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        contents = list(pool.map(lambda a: read_article(a.url) if a.url else "", head))
    enriched = [a.with_content(c) if c else a for a, c in zip(head, contents)]
    return enriched + tail
