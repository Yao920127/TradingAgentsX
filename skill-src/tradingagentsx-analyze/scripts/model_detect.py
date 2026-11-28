"""從執行環境偵測「正在跑這次分析的模型」。

模型常不知道自己的 ID（opencode 的 Nemotron 會填 unknown、Codex 的 GPT 會誤報 Claude），
所以 `--model` 為 unknown 時，改用 harness 傳給子行程的 session ID，精準對應到「這一次對話」：
  - Codex：環境變數 CODEX_THREAD_ID → ~/.codex/sessions/**/rollout-*-<id>.jsonl 最後一筆 turn_context 的 model
  - opencode：環境變數 OPENCODE_SESSION_ID → ~/.local/share/opencode/opencode.db
    該 session 最新 assistant 訊息的模型（2.x 在 session_message／session_v2，1.x 在 message／session）
兩個變數都沒有（例如 Claude Code）就回傳 None，不去猜別的工具的紀錄。
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Mapping, Optional

_SAFE_ID = re.compile(r"^[\w\-]+$")


def _codex_model(home: Path, thread_id: str) -> Optional[str]:
    if not _SAFE_ID.match(thread_id):
        return None
    files = list((home / ".codex" / "sessions").glob(f"**/rollout-*-{thread_id}.jsonl"))
    if not files:
        return None
    found = None
    with files[0].open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:  # model 只記在每回合開頭的 turn_context，不在檔尾，所以要整檔逐行掃
            if '"turn_context"' not in line or '"model"' not in line:
                continue
            try:
                found = json.loads(line).get("payload", {}).get("model") or found
            except ValueError:
                continue
    return found


def _opencode_model(home: Path, session_id: str) -> Optional[str]:
    db = home / ".local" / "share" / "opencode" / "opencode.db"
    if not db.exists():
        return None
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            # opencode 2.x：session_message（type=assistant）的 data.model.id，其次 session_v2.model.id
            queries = (
                ("select json_extract(data,'$.model.id') from session_message "
                 "where session_id=? and type='assistant' order by seq desc limit 1", False),
                ("select model from session_v2 where id=?", True),
                # opencode 1.x：message.data.modelID，其次 session.model.id
                ("select json_extract(data,'$.modelID') from message "
                 "where session_id=? and json_extract(data,'$.role')='assistant' "
                 "order by time_created desc limit 1", False),
                ("select model from session where id=?", True),
            )
            for sql, is_json in queries:
                try:
                    row = con.execute(sql, (session_id,)).fetchone()
                except sqlite3.Error:
                    continue  # 該版本沒有這張表
                if not row or not row[0]:
                    continue
                found = _json_id(row[0]) if is_json else row[0]
                if found:
                    return found
        finally:
            con.close()
    except sqlite3.Error:
        return None
    return None


def _json_id(raw: str) -> Optional[str]:
    try:
        return json.loads(raw).get("id")
    except (ValueError, AttributeError):
        return None


def detect_runtime_model(home: Optional[Path] = None, env: Optional[Mapping[str, str]] = None) -> Optional[str]:
    """回傳偵測到的模型 ID；不在 Codex／opencode 內或找不到就回傳 None。"""
    home = home or Path.home()
    env = os.environ if env is None else env
    try:
        if env.get("CODEX_THREAD_ID"):
            return _codex_model(home, env["CODEX_THREAD_ID"])
        if env.get("OPENCODE_SESSION_ID"):
            return _opencode_model(home, env["OPENCODE_SESSION_ID"])
    except OSError:
        return None
    return None
