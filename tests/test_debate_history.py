"""辯論歷史工具與辯論者節點的單元測試（不打外部 API）。"""
from types import SimpleNamespace

from tradingagents.agents.researchers.bear_researcher import create_bear_researcher
from tradingagents.agents.researchers.bull_researcher import create_bull_researcher
from tradingagents.agents.risk_mgmt.aggresive_debator import create_risky_debator
from tradingagents.agents.risk_mgmt.conservative_debator import create_safe_debator
from tradingagents.agents.risk_mgmt.neutral_debator import create_neutral_debator
from tradingagents.agents.utils.debate_history import append_round, compact_debate_history


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


def test_append_round_labels_first_round_without_leading_blank():
    assert append_round("", "內容", 1) == "# 第 1 輪\n\n內容"


def test_append_round_keeps_earlier_rounds():
    result = append_round(append_round("", "first", 1, "en"), "second", 2, "en")

    assert result == "# Round 1\n\nfirst\n\n# Round 2\n\nsecond"


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


def test_bull_and_bear_accumulate_their_own_rounds():
    bull = create_bull_researcher(FakeLLM("BULL"), FakeMemory())
    bear = create_bear_researcher(FakeLLM("BEAR"), FakeMemory())
    debate = {"history": "", "bull_history": "", "bear_history": "", "current_response": "", "count": 0}

    for _ in range(2):
        debate = bull({"investment_debate_state": debate, "analyst_summary": "S"})["investment_debate_state"]
        debate = bear({"investment_debate_state": debate, "analyst_summary": "S"})["investment_debate_state"]

    assert debate["bull_history"] == "# 第 1 輪\n\nBULL-1\n\n# 第 2 輪\n\nBULL-2"
    assert debate["bear_history"] == "# 第 1 輪\n\nBEAR-1\n\n# 第 2 輪\n\nBEAR-2"
    assert debate["count"] == 4
    # 路由仍依賴 current_response 的發言者前綴
    assert debate["current_response"] == "看跌分析師：BEAR-2"


def test_risk_debaters_accumulate_their_own_rounds():
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

    assert debate["risky_history"] == "# 第 1 輪\n\nRISKY-1\n\n# 第 2 輪\n\nRISKY-2"
    assert debate["safe_history"] == "# 第 1 輪\n\nSAFE-1\n\n# 第 2 輪\n\nSAFE-2"
    assert debate["neutral_history"] == "# 第 1 輪\n\nNEUTRAL-1\n\n# 第 2 輪\n\nNEUTRAL-2"
    assert debate["count"] == 6
