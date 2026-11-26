"""各 agent 提示詞套件。

每個 agent 一個檔案，共用內容在 common.py 與 principles.py。
外部一律從 tradingagents.agents.prompts 匯入。
"""

from .common import (
    get_language_instruction,
    get_language_closing_instruction,
    REPORT_FORMAT_RULES_ZH,
    REPORT_FORMAT_RULES_EN,
    get_agent_role_instruction,
    get_context_message,
    get_report_closing,
)

from .principles import (
    ANALYST_PRINCIPLES_ZH,
    ANALYST_PRINCIPLES_EN,
    get_analyst_principles,
    DEBATE_PRINCIPLES_ZH,
    DEBATE_PRINCIPLES_EN,
    get_debate_principles,
)

from .market_analyst import (
    get_market_analyst_prompt,
)

from .fundamentals_analyst import (
    get_fundamentals_analyst_prompt,
)

from .social_analyst import (
    get_social_analyst_prompt,
)

from .news_analyst import (
    get_news_analyst_prompt,
)

from .bull_researcher import (
    get_bull_researcher_prompt,
)

from .bear_researcher import (
    get_bear_researcher_prompt,
)

from .research_manager import (
    get_research_manager_prompt,
)

from .trader import (
    get_trader_prompt,
)

from .aggressive_debator import (
    get_aggressive_debator_prompt,
)

from .conservative_debator import (
    get_conservative_debator_prompt,
)

from .neutral_debator import (
    get_neutral_debator_prompt,
)

from .risk_manager import (
    get_risk_manager_prompt,
)

from .report_summarizer import (
    REPORT_SUMMARY_SECTIONS,
    get_section_summary_title,
    get_section_summarizer_prompt,
)


__all__ = [
    "get_language_instruction",
    "get_language_closing_instruction",
    "REPORT_FORMAT_RULES_ZH",
    "REPORT_FORMAT_RULES_EN",
    "get_agent_role_instruction",
    "get_context_message",
    "get_report_closing",
    "ANALYST_PRINCIPLES_ZH",
    "ANALYST_PRINCIPLES_EN",
    "get_analyst_principles",
    "DEBATE_PRINCIPLES_ZH",
    "DEBATE_PRINCIPLES_EN",
    "get_debate_principles",
    "get_market_analyst_prompt",
    "get_fundamentals_analyst_prompt",
    "get_social_analyst_prompt",
    "get_news_analyst_prompt",
    "get_bull_researcher_prompt",
    "get_bear_researcher_prompt",
    "get_research_manager_prompt",
    "get_trader_prompt",
    "get_aggressive_debator_prompt",
    "get_conservative_debator_prompt",
    "get_neutral_debator_prompt",
    "get_risk_manager_prompt",
    "REPORT_SUMMARY_SECTIONS",
    "get_section_summary_title",
    "get_section_summarizer_prompt",
]
