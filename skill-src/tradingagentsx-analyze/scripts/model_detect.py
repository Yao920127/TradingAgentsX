"""從執行環境偵測「正在跑這次分析的模型」。

模型常不知道自己的 ID（opencode 的 Nemotron 會填 unknown、Codex 的 GPT 會誤報 Claude），
所以 `--model` 為 unknown 時，改用 harness 傳給子行程的 session ID，精準對應到「這一次對話」：
  - Codex：環境變數 CODEX_THREAD_ID → ~/.codex/sessions/**/rollout-*-<id>.jsonl 最後一筆 turn_context 的 model
  - opencode：環境變數 OPENCODE_SESSION_ID → ~/.local/share/opencode/opencode.db
    該 session 最新一則 assistant 訊息的 modelID（沒有就用 session.model）
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
            row = con.execute(
                "select json_extract(data,'$.modelID') from message "
                "where session_id=? and json_extract(data,'$.role')='assistant' "
                "order by time_created desc limit 1",
                (session_id,),
            ).fetchone()
            if row and row[0]:
                return row[0]
            row = con.execute("select model from session where id=?", (session_id,)).fetchone()
        finally:
            con.close()
        return json.loads(row[0]).get("id") if row and row[0] else None
    except (sqlite3.Error, ValueError, AttributeError):
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
