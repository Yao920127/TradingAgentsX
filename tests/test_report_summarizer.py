"""Report Summarizer 的單元測試：四份報告分別摘要後再合併（不打外部 API）。"""
from types import SimpleNamespace

from tradingagents.agents.analysts.report_summarizer import create_report_summarizer

STATE = {
    "market_report": "MARKET-RAW RSI 36.5",
    "sentiment_report": "SENTIMENT-RAW",
    "news_report": "NEWS-RAW",
    "fundamentals_report": "FUNDAMENTALS-RAW",
}


class FakeLLM:
    """記錄每次呼叫的 human message，並回傳可辨識的摘要。"""

    def __init__(self, fail_on: str = "", content_factory=None):
        self.calls: list[str] = []
        self.fail_on = fail_on
        self.content_factory = content_factory or (lambda text: f"SUMMARY<{text.splitlines()[-1]}>")

    def invoke(self, messages):
        human_text = messages[-1].content
        self.calls.append(human_text)
        if self.fail_on and self.fail_on in human_text:
            raise RuntimeError("boom")
        return SimpleNamespace(content=self.content_factory(human_text))


def test_each_report_is_summarized_in_its_own_call():
    llm = FakeLLM()

    create_report_summarizer(llm, "zh-TW")(STATE)

    assert len(llm.calls) == 4
    for raw in STATE.values():
        matching = [call for call in llm.calls if raw in call]
        assert len(matching) == 1
        others = [other for other in STATE.values() if other != raw]
        assert not any(other in matching[0] for other in others)


def test_summary_keeps_fixed_section_order_with_headings():
    llm = FakeLLM()

    summary = create_report_summarizer(llm, "zh-TW")(STATE)["analyst_summary"]

    headings = ["【市場技術摘要】", "【情緒摘要】", "【新聞摘要】", "【基本面摘要】"]
    positions = [summary.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "SUMMARY<MARKET-RAW RSI 36.5>" in summary
    assert "SUMMARY<FUNDAMENTALS-RAW>" in summary


def test_english_headings():
    summary = create_report_summarizer(FakeLLM(), "en")(STATE)["analyst_summary"]

    assert "[Market Technical Summary]" in summary
    assert "[Fundamentals Summary]" in summary


def test_missing_report_skips_llm_and_marks_unavailable():
    llm = FakeLLM()
    state = {**STATE, "news_report": ""}

    summary = create_report_summarizer(llm, "zh-TW")(state)["analyst_summary"]

    assert len(llm.calls) == 3
    assert "【新聞摘要】\n無資料" in summary


def test_failed_section_falls_back_to_original_report_only_for_that_section():
    llm = FakeLLM(fail_on="NEWS-RAW")

    summary = create_report_summarizer(llm, "zh-TW")(STATE)["analyst_summary"]

    assert "【新聞摘要】\nNEWS-RAW" in summary
    assert "SUMMARY<MARKET-RAW RSI 36.5>" in summary
    assert "SUMMARY<SENTIMENT-RAW>" in summary


def test_empty_llm_output_falls_back_to_original_report():
    llm = FakeLLM(content_factory=lambda text: "")

    summary = create_report_summarizer(llm, "zh-TW")(STATE)["analyst_summary"]

    assert "【市場技術摘要】\nMARKET-RAW RSI 36.5" in summary


def test_responses_api_content_blocks_are_normalized():
    blocks = [{"type": "reasoning", "summary": [], "content": []}, {"type": "text", "text": "OK"}]
    llm = FakeLLM(content_factory=lambda text: blocks)

    summary = create_report_summarizer(llm, "zh-TW")(STATE)["analyst_summary"]

    assert "【市場技術摘要】\nOK" in summary
