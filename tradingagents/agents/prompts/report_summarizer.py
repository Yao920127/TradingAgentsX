"""分析師報告摘要提示詞：每份報告各自壓縮，避免數字跨報告污染。"""


REPORT_SUMMARY_SECTIONS = {
    "market": {
        "en": ("Market Technical Summary", 200, "key trend, moving averages, RSI / MACD and other indicators, support and resistance levels, trading signal"),
        "zh-TW": ("市場技術摘要", 200, "關鍵趨勢、均線、RSI／MACD 等技術指標、支撐與壓力位、交易信號"),
    },
    "sentiment": {
        "en": ("Sentiment Summary", 150, "overall market mood, key themes and discussion volume from social data"),
        "zh-TW": ("情緒摘要", 150, "整體市場情緒、社群數據的主要主題與討論量"),
    },
    "news": {
        "en": ("News Summary", 150, "the most important 1-3 events and their investment implications"),
        "zh-TW": ("新聞摘要", 150, "最重要的 1-3 個事件及其投資意涵"),
    },
    "fundamentals": {
        "en": ("Fundamentals Summary", 200, "key financial metrics, valuation, competitive position, growth outlook"),
        "zh-TW": ("基本面摘要", 200, "關鍵財務指標、估值、競爭地位、成長展望"),
    },
}


def get_section_summary_title(section: str, language: str = "zh-TW") -> str:
    """Get the heading used for one section of the combined analyst summary."""
    lang = "en" if language == "en" else "zh-TW"
    return REPORT_SUMMARY_SECTIONS[section][lang][0]


def get_section_summarizer_prompt(section: str, language: str = "zh-TW") -> str:
    """Get the system prompt that compresses ONE analyst report.

    Each report is summarized in its own call so numbers from one report cannot
    leak into another section and no report is squeezed out by a longer one.
    """
    if language == "en":
        title, words, focus = REPORT_SUMMARY_SECTIONS[section]["en"]
        return f"""You are a concise analyst synthesizer. Compress the single analyst report you are given into the "{title}" section, at most {words} words.

Output exactly two parts, with no heading:
Key data: one line listing the most critical numbers found in this report, separated by " | " (for example: Price: $XXX | RSI: XX). Write "Key data: none" if the report contains no numbers.
Summary: {focus}.

Rules:
- **MUST verbatim preserve** all specific numbers, ratios, price levels, and percentages — vague phrases like "elevated" or "strong" MUST be replaced with actual values
- Use ONLY numbers and facts that appear in this report; never estimate or fill in values that are missing
- Use plain text only, no markdown tables
- Do not add new analysis or opinions — only compress existing content"""

    title, words, focus = REPORT_SUMMARY_SECTIONS[section]["zh-TW"]
    return f"""您是簡潔的分析師整合員。將收到的單一份分析師報告壓縮成「{title}」段落，最多 {words} 字。

請輸出以下兩個部分，不要加標題：
關鍵數據：用一行列出這份報告中最重要的數字，以「 | 」分隔（例如：股價：$XXX | RSI：XX）。報告中沒有數字時寫「關鍵數據：無」。
摘要：{focus}。

規則：
- **必須逐字保留**所有具體數字、比率、價位和百分比——模糊描述（如「偏高」、「強勁」）**必須替換**為實際數值
- 只能使用這份報告中出現的數字與事實；缺少的數值不可估計或自行補上
- 僅使用純文字，不使用 Markdown 表格
- 不要添加新的分析或意見——只壓縮現有內容"""
