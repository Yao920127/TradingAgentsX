import importlib.util
import json
import sqlite3
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


def _codex(home, thread, model):
    f = home / ".codex" / "sessions" / "2026" / "11" / "28" / f"rollout-2026-11-28T20-00-00-{thread}.jsonl"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(
        '{"type":"session_meta","payload":{"model":"old"}}\n'
        + f'{{"type":"turn_context","payload":{{"model":"{model}"}}}}\n'
        + "x" * 600_000 + "\n"  # model 之後再塞大量內容，確認不是只讀檔尾
    )


def _opencode(home, sid, session_model, assistant_model=None):
    db = home / ".local" / "share" / "opencode" / "opencode.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.execute("create table session (id text, model text)")
    con.execute("create table message (session_id text, time_created int, data text)")
    con.execute("insert into session values (?, ?)", (sid, json.dumps({"id": session_model})))
    if assistant_model:
        con.execute("insert into message values (?, 1, ?)", (sid, json.dumps({"role": "assistant", "modelID": assistant_model})))
    con.commit()
    con.close()


def _opencode_v2(home, sid, session_model, assistant_model=None):
    db = home / ".local" / "share" / "opencode" / "opencode.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.execute("create table session_v2 (id text, model text)")
    con.execute("create table session_message (session_id text, type text, seq int, data text)")
    con.execute("insert into session_v2 values (?, ?)", (sid, json.dumps({"id": session_model})))
    if assistant_model:
        con.execute("insert into session_message values (?, 'assistant', 1, ?)",
                    (sid, json.dumps({"model": {"id": assistant_model}})))
    con.commit()
    con.close()


def test_opencode_v2_reads_assistant_message_model(md, tmp_path):
    _opencode_v2(tmp_path, "ses_2", "nemotron-3-ultra-free", "nemotron-3.5-lightning-free")
    assert md.detect_runtime_model(tmp_path, {"OPENCODE_SESSION_ID": "ses_2"}) == "nemotron-3.5-lightning-free"


def test_opencode_v2_falls_back_to_session_v2_model(md, tmp_path):
    _opencode_v2(tmp_path, "ses_2", "nemotron-3.5-lightning-free")
    assert md.detect_runtime_model(tmp_path, {"OPENCODE_SESSION_ID": "ses_2"}) == "nemotron-3.5-lightning-free"


def test_codex_uses_own_thread_not_newest_file(md, tmp_path):
    _codex(tmp_path, "aaa-111", "gpt-6-luna")
    _codex(tmp_path, "bbb-222", "gpt-6-astra")
    assert md.detect_runtime_model(tmp_path, {"CODEX_THREAD_ID": "aaa-111"}) == "gpt-6-luna"


def test_opencode_prefers_latest_assistant_model(md, tmp_path):
    _opencode(tmp_path, "ses_1", "nemotron-3-ultra-free", "nemotron-3.5-lightning-free")
    assert md.detect_runtime_model(tmp_path, {"OPENCODE_SESSION_ID": "ses_1"}) == "nemotron-3.5-lightning-free"


def test_opencode_falls_back_to_session_model(md, tmp_path):
    _opencode(tmp_path, "ses_1", "seaglass-alpha-free")
    assert md.detect_runtime_model(tmp_path, {"OPENCODE_SESSION_ID": "ses_1"}) == "seaglass-alpha-free"


def test_other_harness_returns_none_even_if_records_exist(md, tmp_path):
    _codex(tmp_path, "aaa-111", "gpt-6-luna")
    assert md.detect_runtime_model(tmp_path, {}) is None


def test_missing_records_return_none(md, tmp_path):
    assert md.detect_runtime_model(tmp_path, {"CODEX_THREAD_ID": "zzz"}) is None
    assert md.detect_runtime_model(tmp_path, {"OPENCODE_SESSION_ID": "ses_x"}) is None


def test_path_traversal_thread_id_rejected(md, tmp_path):
    assert md.detect_runtime_model(tmp_path, {"CODEX_THREAD_ID": "../x"}) is None
