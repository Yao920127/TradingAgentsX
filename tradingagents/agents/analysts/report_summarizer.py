"""
Report Summarizer — 將 4 份分析師報告「分別」壓縮後，合併成單一結構化摘要。

用途：在 Bull/Bear 研究員和風險辯論員收到報告之前，
先用 quick_thinking_llm 壓縮，減少下游 agent 的 input tokens。

每份報告各自一次 LLM 呼叫（平行執行）：
- 模型一次只看到一份報告，數字不會被寫進別的章節。
- 各份報告有自己的篇幅，不會被較長的報告擠壓。
- 某一份摘要失敗時只有那一份退回原文，其餘照常。
"""

import logging
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import HumanMessage

from tradingagents.agents.utils.agent_utils import make_cached_system_message
from tradingagents.agents.utils.output_filter import _normalize_content
from tradingagents.agents.utils.prompts import (
    get_section_summarizer_prompt,
    get_section_summary_title,
)

logger = logging.getLogger(__name__)

# (章節鍵, state 欄位)；順序即合併後摘要的章節順序
REPORT_SECTIONS = (
    ("market", "market_report"),
    ("sentiment", "sentiment_report"),
    ("news", "news_report"),
    ("fundamentals", "fundamentals_report"),
)

UNAVAILABLE_TEXT = {"en": "Data unavailable", "zh-TW": "無資料"}
HUMAN_INSTRUCTION = {
    "en": "Please summarize the following analyst report:",
    "zh-TW": "請摘要以下這份分析師報告：",
}


def _lang(language: str) -> str:
    return "en" if language == "en" else "zh-TW"


def _summarize_section(llm, section: str, report: str, language: str) -> str:
    """摘要單一份報告；沒有報告時不呼叫 LLM，失敗或空輸出時退回原文。"""
    if not report or not report.strip():
        return UNAVAILABLE_TEXT[_lang(language)]

    messages = [
        # Claude → cache_control；其他 → 普通
        make_cached_system_message(get_section_summarizer_prompt(section, language), llm),
        HumanMessage(content=f"{HUMAN_INSTRUCTION[_lang(language)]}\n\n{report}"),
    ]
    try:
        summary = _normalize_content(llm.invoke(messages).content).strip()
    except Exception as e:
        # 不中斷整個 graph；下游改讀這一份的原文，而不是空白
        logger.warning(f"[Report Summarizer] {section} 摘要失敗，改用原始報告: {e}")
        return report

    if not summary:
        logger.warning(f"[Report Summarizer] {section} 摘要為空，改用原始報告")
        return report
    return summary


def create_report_summarizer(llm, language: str = "zh-TW"):
    """建立 Report Summarizer 節點。

    Args:
        llm: quick_thinking_llm（使用者設定的輕量模型）
        language: 輸出語言，"en" 或 "zh-TW"

    Returns:
        LangGraph 節點函式 node(state) -> dict
    """

    def summarizer_node(state) -> dict:
        reports = [(section, state.get(field, "") or "") for section, field in REPORT_SECTIONS]

        with ThreadPoolExecutor(max_workers=len(reports)) as executor:
            summaries = list(
                executor.map(
                    lambda item: _summarize_section(llm, item[0], item[1], language),
                    reports,
                )
            )

        if language == "en":
            parts = [
                f"[{get_section_summary_title(section, language)}]\n{summary}"
                for (section, _), summary in zip(reports, summaries)
            ]
        else:
            parts = [
                f"【{get_section_summary_title(section, language)}】\n{summary}"
                for (section, _), summary in zip(reports, summaries)
            ]

        return {"analyst_summary": "\n\n".join(parts)}

    return summarizer_node
