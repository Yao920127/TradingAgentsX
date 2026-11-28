import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "skill-src" / "tradingagentsx-analyze" / "scripts" / "model_detect.py"


@pytest.fixture(scope="module")
def md():
    spec = importlib.util.spec_from_file_location("model_detect", MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["model_detect"] = mod
    spec.loader.exec_module(mod)
    return mod


def _codex(home, model, mtime):
    f = home / ".codex" / "sessions" / "2026" / "11" / "28" / "rollout-x.jsonl"
    f.parent.mkdir(parents=True)
    f.write_text(f'{{"model":"old"}}\n{{"turn_context":{{"model":"{model}"}}}}\n')
    os.utime(f, (mtime, mtime))


def _opencode(home, model, mtime):
    f = home / ".local" / "state" / "opencode" / "model.json"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps({"recent": [{"providerID": "opencode", "modelID": model}]}))
    os.utime(f, (mtime, mtime))


def test_codex_session_model_detected(md, tmp_path):
    _codex(tmp_path, "gpt-6-luna", 1000)
    assert md.detect_runtime_model(tmp_path, now=1001) == "gpt-6-luna"


def test_opencode_recent_model_detected(md, tmp_path):
    _opencode(tmp_path, "nemotron-3.5-lightning-free", 1000)
    assert md.detect_runtime_model(tmp_path, now=1001) == "nemotron-3.5-lightning-free"


def test_newest_source_wins(md, tmp_path):
    _codex(tmp_path, "gpt-6-luna", 1000)
    _opencode(tmp_path, "grok-code", 2000)
    assert md.detect_runtime_model(tmp_path, now=2001) == "grok-code"


def test_stale_record_ignored(md, tmp_path):
    _codex(tmp_path, "gpt-6-luna", 1000)
    assert md.detect_runtime_model(tmp_path, now=1000 + md.MAX_AGE_SECONDS + 1) is None


def test_nothing_found_returns_none(md, tmp_path):
    assert md.detect_runtime_model(tmp_path) is None
