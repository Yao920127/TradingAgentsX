"""
簡體 → 繁體（台灣用語）轉換。

即使提示詞要求繁體中文，LLM（尤其讀到簡體來源資料時）仍可能混入簡體字，
例如「财务分析」「资料中心」。簡體字也會造成 PDF 缺字（NotoSerifTC 沒有簡體字形）。
這裡以 OpenCC s2twp 做確定性轉換；對已是繁體的文字不會改動。
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

TRADITIONAL_LANGUAGE = "zh-TW"


@lru_cache(maxsize=1)
def _converter():
    try:
        from opencc import OpenCC
    except ImportError:  # 未安裝時不轉換，避免整個分析失敗
        return None
    return OpenCC("s2twp")


def to_traditional(value: Any) -> Any:
    """遞迴轉換字串、dict、list 中的所有文字，回傳新物件（不修改原物件）。"""
    converter = _converter()
    if converter is None:
        return value
    if isinstance(value, str):
        return converter.convert(value)
    if isinstance(value, dict):
        return {key: to_traditional(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_traditional(item) for item in value]
    return value


def localize_for(language: str | None, value: Any) -> Any:
    """只有繁體中文報告才轉換；英文報告原樣回傳。"""
    return to_traditional(value) if language == TRADITIONAL_LANGUAGE else value
