"""所有 agent 共用的語言指令、格式規則、角色指令與報告結尾。"""


def get_language_instruction(language: str = "zh-TW") -> str:
    """Get the language instruction for agent prompts."""
    if language == "en":
        return """**Important: You MUST respond entirely in English.**
**Strictly forbidden: Do NOT use any emoji symbols (such as ✅ ❌ 📊 📈 🚀 etc.).**
**Use only plain text, numbers, punctuation, and necessary Unicode symbols (such as ↑ ↓ ★ ● etc.).**"""
    
    return """**重要：您必須使用繁體中文（Traditional Chinese）回覆所有內容。**
**嚴格禁止：請勿在回覆中使用任何 emoji 表情符號（如 ✅ ❌ 📊 📈 🚀 等）。**
**請只使用純文字、數字、標點符號和必要的 Unicode 符號（如 ↑ ↓ ★ ●等）。**"""


def get_language_closing_instruction(language: str = "zh-TW") -> str:
    """Get the language closing instruction placed at the END of agent prompts for maximum compliance."""
    if language == "en":
        return (
            "**Language Rule: Your ENTIRE response MUST be written in English only. Do NOT use Chinese or any other language.**\n\n"
            f"{REPORT_FORMAT_RULES_EN}"
        )
    return f"【語言規定】\n您的回覆必須完全使用繁體中文，嚴格禁止使用英文或其他語言。\n\n{REPORT_FORMAT_RULES_ZH}"


REPORT_FORMAT_RULES_ZH = """【格式規定】
- 大標題一律寫成「## 一、標題」，小標題一律寫成「### 1. 標題」；不要使用「#」一級標題
- 不要用整行粗體（**...**）當標題，也不要把整句或整段加粗
- 粗體只用在關鍵字、關鍵數字與結論，例如 **持有**、**131.69**、**營業利益率 76.3%**
- 條列一律用「- 」開頭；表格使用標準 Markdown 表格"""


REPORT_FORMAT_RULES_EN = """**Formatting Rules:**
- Write every section heading as "## 1. Heading" and every sub-heading as "### Heading"; do not use "#" level-1 headings
- Do not use a whole bold line (**...**) as a heading, and never bold whole sentences or paragraphs
- Use bold only for key terms, key numbers and conclusions, e.g. **HOLD**, **131.69**, **operating margin 76.3%**
- Start bullet points with "- "; use standard Markdown tables"""


def get_agent_role_instruction(language: str = "zh-TW") -> str:
    """Get the common agent role instruction."""
    if language == "en":
        return (
            "You are a helpful AI assistant collaborating with other assistants."
            " Use the provided tools to answer questions step by step."
            " If you cannot fully answer, that's okay; another assistant with different tools will help where you left off."
            " If you or any other assistant has a final trading proposal: **Buy/Hold/Sell** or a deliverable,"
            " prefix your response with 'Final Trading Proposal: **Buy/Hold/Sell**' so the team knows to stop."
        )
    
    return (
        "您是一個樂於助人的人工智慧助理，與其他助理協同工作。"
        " 使用提供的工具來逐步回答問題。"
        " 如果您無法完全回答，沒關係；另一個擁有不同工具的助理會在您中斷的地方提供幫助。"
        " 如果您或任何其他助理有最終交易提案：**買入/持有/賣出** 或可交付成果，"
        " 請在您的回覆前加上「最終交易提案：**買入/持有/賣出**」，以便團隊知道停止。"
    )


def get_context_message(language: str, current_date: str, company_name: str, ticker: str) -> str:
    """Get the context message template."""
    if language == "en":
        return f"For your reference, today's date is {current_date}. The company we are analyzing is {company_name} (ticker: {ticker})."
    
    return f"供您參考，目前日期是 {current_date}。我們想關注的公司是 {company_name} （股票代碼：{ticker}）"


def get_report_closing(language: str, report_type: str) -> str:
    """Get report closing disclaimer based on report type."""
    closings = {
        "en": {
            "market": "---\n※ This report is technical analysis only. Recommend combining with fundamental and sentiment analysis. Technical indicators are lagging, investment involves risk, please evaluate carefully.",
            "fundamentals": "---\n※ This report is fundamental analysis only. Recommend referring to the latest financial reports and combining with technical and sentiment analysis. Financial data may have time lag, investment involves risk, please evaluate carefully.",
            "social": "---\n※ This report is market sentiment analysis only. Recommend combining with fundamental and technical analysis. Investment involves risk, please evaluate carefully.",
            "news": "---\n※ This report is news analysis only. Recommend combining with fundamental and technical analysis. News information is time-sensitive, investment involves risk, please evaluate carefully.",
            "default": "---\n※ Investment involves risk, please evaluate carefully.",
        },
        "zh-TW": {
            "market": "---\n※ 本報告為技術面分析，建議搭配基本面及市場情緒綜合研判。技術指標具滯後性，投資有風險，請謹慎評估。",
            "fundamentals": "---\n※ 本報告為基本面分析，建議參考最新財報公告並搭配技術面及市場情緒綜合研判。財務數據可能存在時間差，投資有風險，請謹慎評估。",
            "social": "---\n※ 本報告為市場情緒分析，建議搭配基本面及技術面綜合研判。投資有風險，請謹慎評估。",
            "news": "---\n※ 本報告為新聞面分析，建議搭配基本面及技術面綜合研判。新聞資訊時效性強，投資有風險，請謹慎評估。",
            "default": "---\n※ 投資有風險，請謹慎評估。",
        }
    }
    lang_closings = closings.get(language, closings["zh-TW"])
    return lang_closings.get(report_type, lang_closings["default"])
