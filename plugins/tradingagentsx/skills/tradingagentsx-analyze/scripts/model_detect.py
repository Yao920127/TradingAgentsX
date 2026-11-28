"""從執行環境偵測「正在跑這次分析的模型」。

模型常不知道自己的 ID（opencode 的 Nemotron 會填 unknown、Codex 的 GPT 會誤報 Claude），
所以 `--model` 為 unknown 時，改讀 harness 自己留下的紀錄：
  - Codex：~/.codex/sessions/**/rollout-*.jsonl 內最後一個 "model"
  - opencode：~/.local/state/opencode/model.json 的 recent[0]
多個來源都有時取最近被寫入的那個；超過 MAX_AGE_SECONDS 沒動過的紀錄視為過期，不採用。
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Optional

MAX_AGE_SECONDS = 12 * 3600
_TAIL_BYTES = 256 * 1024
_MODEL_RE = re.compile(r'"model"\s*:\s*"([^"]+)"')


def _codex_model(home: Path) -> Optional[tuple[float, str]]:
    files = list((home / ".codex" / "sessions").glob("**/rollout-*.jsonl"))
    if not files:
        return None
    newest = max(files, key=lambda p: p.stat().st_mtime)
    with newest.open("rb") as fh:
        fh.seek(0, 2)
        fh.seek(max(0, fh.tell() - _TAIL_BYTES))
        tail = fh.read().decode("utf-8", errors="ignore")
    found = _MODEL_RE.findall(tail)
    return (newest.stat().st_mtime, found[-1]) if found else None


def _opencode_model(home: Path) -> Optional[tuple[float, str]]:
    path = home / ".local" / "state" / "opencode" / "model.json"
    try:
        recent = json.loads(path.read_text(encoding="utf-8")).get("recent") or []
        model_id = recent[0].get("modelID")
    except (OSError, ValueError, IndexError, AttributeError):
        return None
    return (path.stat().st_mtime, model_id) if model_id else None


def detect_runtime_model(home: Optional[Path] = None, now: Optional[float] = None) -> Optional[str]:
    """回傳偵測到的模型 ID；找不到或已過期回傳 None。"""
    home = home or Path.home()
    now = time.time() if now is None else now
    candidates = []
    for reader in (_codex_model, _opencode_model):
        try:
            hit = reader(home)
        except OSError:
            continue
        if hit and now - hit[0] <= MAX_AGE_SECONDS:
            candidates.append(hit)
    return max(candidates)[1] if candidates else None
