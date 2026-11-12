# -*- coding: utf-8 -*-
from langchain_core.messages import HumanMessage
from tradingagents.agents.utils.agent_utils import make_cached_system_message
from tradingagents.agents.utils.debate_history import compact_debate_history
from tradingagents.agents.utils.output_filter import fix_common_llm_errors, validate_and_warn
from tradingagents.agents.utils.prompts import get_bull_researcher_prompt


def create_bull_researcher(llm, memory, language: str = "zh-TW"):
    """
    建立一個看漲研究員節點。

    Args:
        llm: 用於生成回應的語言模型。
        memory: 儲存過去情況和反思的記憶體物件。
        language: 報告語言 ('en' 或 'zh-TW')

    Returns:
        function: 一個代表看漲研究員節點的函式。
    """

    def bull_node(state) -> dict:
        """看漲研究員節點的執行函式。"""
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        current_response = investment_debate_state.get("current_response", "")

        # 使用 analyst_summary（由 Report Summarizer 預先壓縮），節省約 75% input tokens
        analyst_summary = state.get("analyst_summary", "")

        # 較早發言只留開頭摘錄、最近一輪保留全文，避免多輪後遺忘先前論點
        history = compact_debate_history(history, recent_turns=2, language=language)

        # 記憶體查詢用 analyst_summary 作為情境
        curr_situation = analyst_summary
        past_memories = memory.get_memories(curr_situation, n_matches=2)
        past_memory_str = ""
        for rec in past_memories:
            past_memory_str += rec["recommendation"] + "\n\n"

        # base_prompt 為靜態指令，透過 make_cached_system_message 加上 cache_control（僅 Claude 生效）
        base_prompt = get_bull_researcher_prompt(language)

        # 動態資料放入 HumanMessage（不快取）
        if language == "en":
            human_text = f"""【Available Data】
- Analyst Summary: {analyst_summary}
- Debate History: {history}
- Bearish Arguments: {current_response}
- Past Experience: {past_memory_str}

Please provide your bullish analysis now."""
        else:
            human_text = f"""【可用資料】
- 分析摘要：{analyst_summary}
- 辯論歷史：{history}
- 看跌論點：{current_response}
- 過往經驗：{past_memory_str}

請提供您的看漲分析。"""

        messages = [
            make_cached_system_message(base_prompt, llm),
            HumanMessage(content=human_text),
        ]

        response = llm.invoke(messages)

        response.content = fix_common_llm_errors(response.content)
        validate_and_warn(response.content, "Bull_Researcher")

        # Format argument based on language (with label for combined history only)
        if language == "en":
            argument = f"Bull Analyst: {response.content}"
        else:
            argument = f"看漲分析師：{response.content}"

        # 個人歷史（報告顯示用）只保留最後一輪發言；完整過程留在共用 history
        new_investment_debate_state = {
            "history": investment_debate_state.get("history", "") + "\n" + argument,
            "bull_history": response.content.strip(),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bull_node
