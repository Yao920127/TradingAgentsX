# -*- coding: utf-8 -*-
"""
辯論歷史的共用工具。

- latest_round：報告顯示時只取最後一輪發言、去掉輪次標題（相容舊報告）。
- compact_debate_history：把完整辯論歷史壓成「較早發言的開頭摘錄 + 最近一輪全文」，
  讓辯論者在多輪辯論後仍記得先前的論點，同時控制 input tokens。
"""

import re

# 最近發言保留全文時，單次發言的字元上限
RECENT_TURN_CHAR_LIMIT = 2000
# 較早發言只保留開頭摘錄的字元數（核心論點通常寫在開頭）
EARLIER_TURN_DIGEST_CHARS = 220
# 未超過此長度的歷史不做壓縮
DEBATE_HISTORY_LIMIT = 3000

_SPEAKER_LABELS = (
    "看漲分析師：",
    "看跌分析師：",
    "激進分析師：",
    "保守分析師：",
    "中立分析師：",
    "Bull Analyst: ",
    "Bear Analyst: ",
    "Aggressive Analyst: ",
    "Conservative Analyst: ",
    "Neutral Analyst: ",
)
_TURN_START = re.compile(
    r"^(?=(?:" + "|".join(re.escape(label) for label in _SPEAKER_LABELS) + r"))",
    re.MULTILINE,
)


# 舊版報告會把每一輪發言累加並加上「# 第 N 輪」／「# Round N」標題
_ROUND_HEADING = re.compile(r"^# (?:第 \d+ 輪|Round \d+)[ \t]*$", re.MULTILINE)


def latest_round(history: str) -> str:
    """只取某位辯論者最後一輪的發言，並去掉輪次標題（相容舊報告的累加格式）。"""
    if not history:
        return history
    return _ROUND_HEADING.split(history)[-1].strip()


def _split_turns(history: str) -> list[str]:
    return [turn.strip() for turn in _TURN_START.split(history) if turn.strip()]


def _digest(turn: str) -> str:
    flat = " ".join(turn.split())
    if len(flat) <= EARLIER_TURN_DIGEST_CHARS:
        return flat
    return flat[:EARLIER_TURN_DIGEST_CHARS] + "…"


def _cap(turn: str) -> str:
    if len(turn) <= RECENT_TURN_CHAR_LIMIT:
        return turn
    return turn[:RECENT_TURN_CHAR_LIMIT] + "…"


def compact_debate_history(
    history: str,
    recent_turns: int,
    language: str = "zh-TW",
    limit: int = DEBATE_HISTORY_LIMIT,
) -> str:
    """
    壓縮辯論歷史供辯論者閱讀。

    Args:
        history: 完整辯論歷史（每次發言以發言者標籤開頭）。
        recent_turns: 保留全文的最近發言數（通常為辯論人數，即最近一整輪）。
        language: 報告語言，決定區段標題。
        limit: 未超過此字元數時原樣返回。
    """
    if len(history) <= limit:
        return history

    turns = _split_turns(history)
    if len(turns) <= recent_turns:
        # 無法辨識發言邊界或只有最近一輪：退回保留尾段
        return "...[truncated]\n" + history[-limit:]

    earlier = turns[:-recent_turns]
    recent = turns[-recent_turns:]

    if language == "en":
        earlier_title = "[Earlier turns, opening excerpts only]"
        recent_title = "[Most recent turns, full text]"
    else:
        earlier_title = "【較早發言（僅開頭摘錄）】"
        recent_title = "【最近發言（全文）】"

    earlier_block = "\n".join(f"{i}. {_digest(turn)}" for i, turn in enumerate(earlier, 1))
    recent_block = "\n\n".join(_cap(turn) for turn in recent)
    return f"{earlier_title}\n{earlier_block}\n\n{recent_title}\n{recent_block}"
