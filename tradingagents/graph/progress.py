# -*- coding: utf-8 -*-
# TradingAgentsX/graph/progress.py

"""
追蹤代理圖的執行進度。

將 LangGraph 的節點事件（開始 / 結束）轉換為使用者可理解的「步驟」快照，
讓前端可以顯示目前是哪個代理在工作、做到哪一步、各步驟花了多少時間。

節點名稱必須與 `setup.py` 中 `workflow.add_node(...)` 使用的名稱一致。
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[Dict[str, Any]], None]

# 研究辯論與風險辯論的節點 → 代理 key
_RESEARCH_DEBATERS = {
    "Bull Researcher": "bull_researcher",
    "Bear Researcher": "bear_researcher",
}
_RISK_DEBATERS = {
    "Risky Analyst": "risky_analyst",
    "Safe Analyst": "safe_analyst",
    "Neutral Analyst": "neutral_analyst",
}
# 單一節點即為一個步驟
_SINGLE_NODE_STEPS = {
    "Report Summarizer": "report_summarizer",
    "Research Manager": "research_manager",
    "Trader": "trader",
    "Risk Judge": "risk_judge",
}


class ProgressTracker:
    """
    根據所選分析師與辯論回合數建立步驟計畫，並依節點事件更新狀態。

    進度百分比以「代理回合」計算：每位分析師、每次辯論發言、
    摘要員、研究經理、交易員、風險裁判各算一個單位。
    """

    def __init__(
        self,
        selected_analysts: List[str],
        max_debate_rounds: int,
        max_risk_discuss_rounds: int,
        callback: Optional[ProgressCallback] = None,
    ):
        self.callback = callback
        self.started_at = time.time()
        self.current_step: Optional[str] = None
        self.current_agent: Optional[str] = None
        self.current_tools: List[str] = []
        self.finished = False

        self.steps: List[Dict[str, Any]] = []
        self._node_to_step: Dict[str, str] = {}

        for analyst in selected_analysts:
            key = f"{analyst}_analyst"
            self._add_step(key)
            label = analyst.capitalize()
            for node in (f"{label} Analyst", f"tools_{analyst}", f"Msg Clear {label}"):
                self._node_to_step[node] = key

        self._add_step("report_summarizer")
        self._add_step("research_debate", total_turns=2 * max_debate_rounds)
        self._add_step("research_manager")
        self._add_step("trader")
        self._add_step("risk_debate", total_turns=3 * max_risk_discuss_rounds)
        self._add_step("risk_judge")

        for node in _RESEARCH_DEBATERS:
            self._node_to_step[node] = "research_debate"
        for node in _RISK_DEBATERS:
            self._node_to_step[node] = "risk_debate"
        self._node_to_step.update(_SINGLE_NODE_STEPS)

        self._steps_by_key = {s["key"]: s for s in self.steps}

    def _add_step(self, key: str, total_turns: Optional[int] = None):
        step: Dict[str, Any] = {
            "key": key,
            "status": "pending",
            "started_at": None,
            "completed_at": None,
        }
        if total_turns is not None:
            step["turns_done"] = 0
            step["total_turns"] = total_turns
        self.steps.append(step)

    # ------------------------------------------------------------------
    # 節點事件
    # ------------------------------------------------------------------

    def on_node_start(self, node: str):
        step_key = self._node_to_step.get(node)
        if step_key is None:
            return
        step = self._steps_by_key[step_key]
        now = time.time()

        # 進入新步驟時，把之前仍在執行中的步驟視為完成
        # （例如辯論步驟在經理開始時結束）
        if self.current_step and self.current_step != step_key:
            self._complete(self._steps_by_key[self.current_step], now)

        if step["status"] == "pending":
            step["status"] = "running"
            step["started_at"] = now
        self.current_step = step_key

        if node.startswith("tools_"):
            # 工具節點：保留上一個分析師節點留下的工具名稱
            pass
        elif node.startswith("Msg Clear"):
            self.current_tools = []
        else:
            self.current_agent = self._agent_key(node)
            self.current_tools = []

        self.emit()

    def on_node_end(self, node: str, result: Any):
        step_key = self._node_to_step.get(node)
        if step_key is None:
            return
        step = self._steps_by_key[step_key]
        now = time.time()

        if node in _RESEARCH_DEBATERS or node in _RISK_DEBATERS:
            step["turns_done"] = min(step["turns_done"] + 1, step["total_turns"])
            if step["turns_done"] >= step["total_turns"]:
                self._complete(step, now)
        elif node.startswith("Msg Clear") or node in _SINGLE_NODE_STEPS:
            self._complete(step, now)
        elif node.endswith(" Analyst"):
            # 分析師節點結束：若要求呼叫工具，記錄工具名稱供前端顯示
            self.current_tools = self._extract_tool_names(result)
        else:
            return  # tools_* 節點結束不需要額外更新

        self.emit()

    def finish(self):
        """圖執行完畢；將所有步驟標記為完成。"""
        now = time.time()
        for step in self.steps:
            if step["status"] != "completed":
                self._complete(step, now)
        self.current_step = None
        self.current_agent = None
        self.current_tools = []
        self.finished = True
        self.emit()

    # ------------------------------------------------------------------
    # 快照
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        total_units = 0
        done_units = 0
        for step in self.steps:
            if "total_turns" in step:
                total_units += step["total_turns"]
                done_units += step["turns_done"]
            else:
                total_units += 1
                done_units += 1 if step["status"] == "completed" else 0

        return {
            "started_at": self.started_at,
            "updated_at": time.time(),
            "percent": round(100 * done_units / total_units) if total_units else 0,
            "finished": self.finished,
            "current_step": self.current_step,
            "current_agent": self.current_agent,
            "current_tools": list(self.current_tools),
            "steps": [dict(s) for s in self.steps],
        }

    # ------------------------------------------------------------------
    # 內部工具
    # ------------------------------------------------------------------

    @staticmethod
    def _complete(step: Dict[str, Any], now: float):
        if step["status"] == "completed":
            return
        if step["started_at"] is None:
            step["started_at"] = now
        step["status"] = "completed"
        step["completed_at"] = now

    @staticmethod
    def _agent_key(node: str) -> str:
        if node in _RESEARCH_DEBATERS:
            return _RESEARCH_DEBATERS[node]
        if node in _RISK_DEBATERS:
            return _RISK_DEBATERS[node]
        if node in _SINGLE_NODE_STEPS:
            return _SINGLE_NODE_STEPS[node]
        # "Market Analyst" -> "market_analyst"
        return node.lower().replace(" ", "_")

    @staticmethod
    def _extract_tool_names(result: Any) -> List[str]:
        if not isinstance(result, dict):
            return []
        messages = result.get("messages") or []
        if not messages:
            return []
        tool_calls = getattr(messages[-1], "tool_calls", None) or []
        names = []
        for call in tool_calls:
            name = call.get("name") if isinstance(call, dict) else getattr(call, "name", None)
            if name and name not in names:
                names.append(name)
        return names

    def emit(self):
        if self.callback is None:
            return
        try:
            self.callback(self.snapshot())
        except Exception as e:  # 進度回報失敗不應中斷分析
            logger.warning(f"Progress callback failed: {e}")
