# -*- coding: utf-8 -*-
from langchain_core.messages import HumanMessage
from tradingagents.agents.utils.agent_utils import make_cached_system_message
from tradingagents.agents.utils.debate_history import compact_debate_history
from tradingagents.agents.utils.output_filter import fix_common_llm_errors, validate_and_warn
from tradingagents.agents.utils.prompts import get_conservative_debator_prompt


def create_safe_debator(llm, language: str = "zh-TW"):
    """
    建立一個保守的風險辯論員節點。

    Args:
        llm: 用於生成回應的語言模型。
        language: 報告語言 ('en' 或 'zh-TW')

    Returns:
        function: 一個代表保守辯論員節點的函式。
    """

    def safe_node(state) -> dict:
        """保守辯論員節點的執行函式。"""
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        # 使用 analyst_summary（由 Report Summarizer 預先壓縮），節省約 75% input tokens
        analyst_summary = state.get("analyst_summary", "")
        trader_decision = state["trader_investment_plan"]

        # 較早發言只留開頭摘錄、最近一輪保留全文，避免多輪後遺忘先前論點
        history = compact_debate_history(history, recent_turns=3, language=language)

        # base_prompt 為靜態指令，透過 make_cached_system_message 加上 cache_control（僅 Claude 生效）
        base_prompt = get_conservative_debator_prompt(language)

        # 動態資料放入 HumanMessage（不快取）
        if language == "en":
            human_text = f"""【Available Information】
- Trader Plan: {trader_decision}
- Analyst Summary: {analyst_summary}
- Debate History: {history}
- Opponent Views: {current_risky_response}, {current_neutral_response}

Please provide your conservative risk analysis."""
        else:
            human_text = f"""【可用資訊】
- 交易員計畫：{trader_decision}
- 分析摘要：{analyst_summary}
- 辯論歷史：{history}
- 對手觀點：{current_risky_response}, {current_neutral_response}

【語言規定】
您的回覆必須完全使用繁體中文，嚴格禁止使用英文或其他語言。

請用繁體中文提供您的保守風險分析。"""

        messages = [
            make_cached_system_message(base_prompt, llm),
            HumanMessage(content=human_text),
        ]

        response = llm.invoke(messages)

        response.content = fix_common_llm_errors(response.content)
        validate_and_warn(response.content, "Conservative_Debator")

        if language == "en":
            argument = f"Conservative Analyst: {response.content}"
        else:
            argument = f"保守分析師：{response.content}"

        # 個人歷史（報告顯示用）只保留最後一輪發言；完整過程留在共用 history
        new_risk_debate_state = {
            "history": risk_debate_state.get("history", "") + "\n" + argument,
            "safe_history": response.content.strip(),
            "risky_history": risk_debate_state.get("risky_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Safe",
            "current_safe_response": argument,
            "current_risky_response": risk_debate_state.get("current_risky_response", ""),
            "current_neutral_response": risk_debate_state.get("current_neutral_response", ""),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return safe_node
