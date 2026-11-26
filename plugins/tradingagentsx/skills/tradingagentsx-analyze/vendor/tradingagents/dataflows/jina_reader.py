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


def read_urls(urls: list[str]) -> list[str]:
    """並行讀取多個網址，失敗的位置回傳空字串（順序與輸入相同）。"""
    if not urls:
        return []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        return list(pool.map(lambda u: read_article(u) if u else "", urls))


def attach_content(items: list[dict], url_key: str, top_n: int, content_key: str = "content") -> list[dict]:
    """回傳新的 dict 清單：前 top_n 筆有網址的項目加上 Jina 全文（不修改原物件）。"""
    targets = [i for i, item in enumerate(items) if item.get(url_key)][:top_n]
    contents = dict(zip(targets, read_urls([items[i][url_key] for i in targets])))
    return [
        {**item, content_key: contents[i]} if contents.get(i) else dict(item)
        for i, item in enumerate(items)
    ]


# 文字中的網址：只接受網址合法的 ASCII 字元（中文緊接在網址後也能正確切開），
# 括號與引號視為網址邊界，結尾的英文標點另外去除
_URL_PATTERN = re.compile(r"https?://[A-Za-z0-9\-._~:/?#@!$&*+,;=%]+")
_URL_TRAILING = ".,;:!?"


def extract_urls(text: str, limit: int, exclude_domains: tuple[str, ...] = ()) -> list[str]:
    """從文字中依出現順序取出不重複的網址。"""
    seen: list[str] = []
    for raw in _URL_PATTERN.findall(text or ""):
        url = raw.rstrip(_URL_TRAILING)
        if url not in seen and not any(domain in url for domain in exclude_domains):
            seen.append(url)
        if len(seen) >= limit:
            break
    return seen


def append_linked_content(text: str, top_n: int, heading: str = "引用文章全文摘錄") -> str:
    """讀取文字中引用的前 top_n 個網址，把全文摘錄附在文末。"""
    urls = extract_urls(text, top_n)
    excerpts = [(u, c) for u, c in zip(urls, read_urls(urls)) if c]
    if not excerpts:
        return text
    section = "\n\n".join(f"- {u}\n  > {c}" for u, c in excerpts)
    return f"{text}\n\n## {heading}\n{section}"
