"""辯論歷史工具與辯論者節點的單元測試（不打外部 API）。"""
from types import SimpleNamespace

from tradingagents.agents.researchers.bear_researcher import create_bear_researcher
from tradingagents.agents.researchers.bull_researcher import create_bull_researcher
from tradingagents.agents.risk_mgmt.aggresive_debator import create_risky_debator
from tradingagents.agents.risk_mgmt.conservative_debator import create_safe_debator
from tradingagents.agents.risk_mgmt.neutral_debator import create_neutral_debator
from tradingagents.agents.utils.debate_history import compact_debate_history, latest_round


class FakeLLM:
    """每次呼叫回傳帶序號的內容，並記錄收到的 human message。"""

    def __init__(self, tag: str):
        self.tag = tag
        self.calls: list[str] = []

    def invoke(self, messages):
        self.calls.append(messages[-1].content)
        return SimpleNamespace(content=f"{self.tag}-{len(self.calls)}")


class FakeMemory:
    def get_memories(self, situation, n_matches=2):
        return []


def test_latest_round_keeps_only_final_round_without_heading():
    history = "# 第 1 輪\n\n舊內容\n\n# 第 2 輪\n\n## 一、標題\n\n最終內容"

    assert latest_round(history) == "## 一、標題\n\n最終內容"


def test_latest_round_handles_english_headings():
    assert latest_round("# Round 1\n\nold\n\n# Round 2\n\nfinal") == "final"


def test_latest_round_returns_single_round_content_unchanged():
    assert latest_round("## 一、標題\n\n內容") == "## 一、標題\n\n內容"
    assert latest_round("") == ""


def test_compact_returns_short_history_unchanged():
    history = "\n看漲分析師：短\n看跌分析師：短"

    assert compact_debate_history(history, recent_turns=2) == history


def test_compact_keeps_recent_turns_in_full_and_digests_earlier_ones():
    turns = [
        f"{'看漲' if i % 2 == 0 else '看跌'}分析師：開頭{i}" + "字" * 1500 + f"結尾{i}"
        for i in range(6)
    ]
    history = "\n" + "\n".join(turns)

    compacted = compact_debate_history(history, recent_turns=2)

    # 最近一輪（第 4、5 次發言）保留全文
    assert "結尾4" in compacted and "結尾5" in compacted
    # 較早發言只留開頭，但每一次都還在
    for i in range(4):
        assert f"開頭{i}" in compacted
        assert f"結尾{i}" not in compacted
    assert len(compacted) < len(history) / 2


def test_compact_falls_back_to_tail_when_turns_cannot_be_split():
    history = "x" * 5000

    compacted = compact_debate_history(history, recent_turns=2)

    assert compacted.startswith("...[truncated]")
    assert len(compacted) < 3100


def test_bull_and_bear_keep_only_their_final_round():
    bull = create_bull_researcher(FakeLLM("BULL"), FakeMemory())
    bear = create_bear_researcher(FakeLLM("BEAR"), FakeMemory())
    debate = {"history": "", "bull_history": "", "bear_history": "", "current_response": "", "count": 0}

    for _ in range(2):
        debate = bull({"investment_debate_state": debate, "analyst_summary": "S"})["investment_debate_state"]
        debate = bear({"investment_debate_state": debate, "analyst_summary": "S"})["investment_debate_state"]

    # 報告只保留各自最後一輪的發言
    assert debate["bull_history"] == "BULL-2"
    assert debate["bear_history"] == "BEAR-2"
    # 完整辯論過程仍保留在共用 history，供辯論者與研究經理閱讀
    assert "BULL-1" in debate["history"] and "BEAR-1" in debate["history"]
    assert debate["count"] == 4
    # 路由仍依賴 current_response 的發言者前綴
    assert debate["current_response"] == "看跌分析師：BEAR-2"


def test_risk_debaters_keep_only_their_final_round():
    nodes = [
        create_risky_debator(FakeLLM("RISKY")),
        create_safe_debator(FakeLLM("SAFE")),
        create_neutral_debator(FakeLLM("NEUTRAL")),
    ]
    debate = {
        "history": "", "risky_history": "", "safe_history": "", "neutral_history": "",
        "latest_speaker": "", "current_risky_response": "", "current_safe_response": "",
        "current_neutral_response": "", "count": 0,
    }

    for _ in range(2):
        for node in nodes:
            debate = node({
                "risk_debate_state": debate,
                "analyst_summary": "S",
                "trader_investment_plan": "PLAN",
            })["risk_debate_state"]

    # 報告只保留各自最後一輪的發言
    assert debate["risky_history"] == "RISKY-2"
    assert debate["safe_history"] == "SAFE-2"
    assert debate["neutral_history"] == "NEUTRAL-2"
    # 完整辯論過程仍保留在共用 history，供辯論者與風險經理閱讀
    assert "RISKY-1" in debate["history"] and "NEUTRAL-1" in debate["history"]
    assert debate["count"] == 6
