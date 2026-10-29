"""
報告 Markdown 版面校正：讓所有報告的標題層級一致。

即使提示詞規定了格式，LLM 仍會混用「## 一、標題」、「**一、標題**」、純文字「一、標題」
與「# 標題」。這裡把它們統一成：
- 章節標題（一、二、三… / 整行的「一、」開頭）→ ## 標題
- 整行粗體的短句（小標題）→ ### 標題
- # 一級標題 → ##（報告頁本身已有分析師名稱當大標）
並在標題前後補空行，避免標題與下一行被併成同一段。表格與條列不處理。

另外移除報告開頭的思考過程（開場白）、分隔線，並把 ▸ / • 等符號統一成 Markdown 條列。
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


# 分隔線（---、***、—-）：一律移除，章節由標題區隔
_HORIZONTAL_RULE = re.compile(r"^\s*[-—–*_=]{2,}\s*$")
# 非標準條列符號 → Markdown 條列
_BULLET_SYMBOL = re.compile(r"^\s*[▸►▶•●▪◆·∙]\s*")
# 「**分析日期：** 2026…」這類標籤行：前面補空行，避免與上一行併成一段
_LABEL_LINE = re.compile(r"^\*\*[^*]{1,30}?(?:[:：]\*\*|\*\*\s*[:：])")

# AI 在工具呼叫與正式報告之間的開場白（思考過程），只檢查報告開頭幾行
_PREAMBLE = re.compile(
    r"(?:^|[，,。])\s*(?:數據|資料|新聞|所有|相關|工具)?[^\n]{0,12}"
    r"(?:已(?:經)?(?:全數|全部|成功|順利)?(?:取得|獲取|收集|蒐集|齊全|備齊)"
    r"|(?:現在|接下來|下面|讓我|我將|我會|我來)(?:開始|來)?(?:進行|撰寫|整理|為您|提供|產出|彙整|分析))"
    r"|^(?:Now|Next),? (?:I(?:'ll| will)|let me)|^(?:I have|I've) (?:now )?(?:gathered|collected|obtained|got)"
    r"|^Let me (?:now )?(?:write|compile|analy[sz]e|put together)",
    re.IGNORECASE,
)
# 開場白一定會提到資料或報告本身；只有動作詞（例如「現在進行整理」）的是內文
_PREAMBLE_SUBJECT = re.compile(r"報告|分析|資料|數據|新聞|data|report|analysis", re.IGNORECASE)
MAX_PREAMBLE_CHARS = 80
MAX_PREAMBLE_LINES = 2


def _is_preamble(line: str) -> bool:
    stripped = line.strip()
    return (
        bool(stripped)
        and len(stripped) <= MAX_PREAMBLE_CHARS
        and not stripped.startswith(("#", "|", "-", "*"))
        and bool(_PREAMBLE.search(stripped))
        and bool(_PREAMBLE_SUBJECT.search(stripped))
    )


def strip_report_preamble(text: str) -> str:
    """移除報告開頭的思考過程，例如「數據已全數取得，現在進行深度整合分析並撰寫完整技術報告。」"""
    lines = text.splitlines()
    removed = 0
    while lines and removed < MAX_PREAMBLE_LINES:
        if not lines[0].strip() or _HORIZONTAL_RULE.match(lines[0]):
            lines.pop(0)
            continue
        if not _is_preamble(lines[0]):
            break
        lines.pop(0)
        removed += 1
    return "\n".join(lines)


def normalize_report_markdown(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return text
    output: list[str] = []
    for line in strip_report_preamble(text).splitlines():
        if _HORIZONTAL_RULE.match(line):
            continue
        line = _BULLET_SYMBOL.sub("- ", line, count=1)
        heading = _normalize_line(line)
        if heading is None:
            previous = output[-1].strip() if output else ""
            is_table = line.strip().startswith("|")
            # 表格與前後文字、標籤行與上一行之間都要有空行，Markdown 才會分開渲染
            needs_gap = previous and (
                is_table != previous.startswith("|") or _LABEL_LINE.match(line.strip())
            )
            if needs_gap:
                output.append("")
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
