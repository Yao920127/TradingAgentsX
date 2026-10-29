"""
報告 Markdown 版面校正：讓所有報告的標題層級一致。

即使提示詞規定了格式，LLM 仍會混用「## 一、標題」、「**一、標題**」、純文字「一、標題」
與「# 標題」。這裡把它們統一成：
- 章節標題（一、二、三… / 整行的「一、」開頭）→ ## 標題
- 整行粗體的短句（小標題）→ ### 標題
- # 一級標題 → ##（報告頁本身已有分析師名稱當大標）
並在標題前後補空行，避免標題與下一行被併成同一段。表格與條列不處理。
"""
from __future__ import annotations

import re
from typing import Any

# 視為小標題的整行粗體最大長度（超過多半是一句強調的內文）
MAX_BOLD_HEADING_CHARS = 40
SENTENCE_ENDINGS = ("。", "！", "？", ".", "!", "?")

_CHINESE_SECTION = re.compile(r"^[一二三四五六七八九十]{1,3}[、．.]\s*\S")
_WHOLE_BOLD = re.compile(r"^\*\*(?P<text>[^*]+?)\*\*\s*[:：]?$")
_HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.+)$")


def _strip_bold(text: str) -> str:
    return text.replace("**", "").strip()


def _normalize_line(line: str) -> str | None:
    """回傳校正後的標題行；不是標題則回傳 None。"""
    stripped = line.strip()
    if not stripped or stripped.startswith(("|", "- ", "* ", "> ")):
        return None

    heading = _HEADING.match(stripped)
    if heading:
        level = max(2, len(heading.group("hashes")))
        text = _strip_bold(heading.group("text"))
        if _CHINESE_SECTION.match(text):
            level = 2
        return f"{'#' * min(level, 3)} {text}"

    bold = _WHOLE_BOLD.match(stripped)
    plain = _strip_bold(bold.group("text")) if bold else stripped
    if _CHINESE_SECTION.match(plain) and len(plain) <= MAX_BOLD_HEADING_CHARS:
        return f"## {plain}"
    # 以句號等結尾的是一句強調的內文，不是小標題
    if bold and len(plain) <= MAX_BOLD_HEADING_CHARS and not plain.endswith(SENTENCE_ENDINGS):
        return f"### {plain}"
    return None


def normalize_report_markdown(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return text
    output: list[str] = []
    for line in text.splitlines():
        heading = _normalize_line(line)
        if heading is None:
            output.append(line)
            continue
        if output and output[-1].strip():
            output.append("")
        output.extend([heading, ""])
    # 合併標題後補出的連續空行
    return re.sub(r"\n{3,}", "\n\n", "\n".join(output)).strip()


def normalize_reports(value: Any) -> Any:
    """遞迴校正 dict / list 中的所有報告文字，回傳新物件（不修改原物件）。"""
    if isinstance(value, str):
        return normalize_report_markdown(value)
    if isinstance(value, dict):
        return {key: normalize_reports(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_reports(item) for item in value]
    return value
