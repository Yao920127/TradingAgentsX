"""安全加固：JWT secret 啟動檢查，以及錯誤回應不得洩漏上游原文。"""
import asyncio
import logging

import pytest
from fastapi.testclient import TestClient

from backend.app.api import auth as auth_module
from backend.app.db import get_db
from backend.app.main import app
from backend.app.services import chat_service
from backend.app.services.auth_utils import DEFAULT_DEV_JWT_SECRET, resolve_jwt_secret

LEAK_MARKER = "UPSTREAM-SECRET-MARKER-7f3a"
STRONG_SECRET = "s" * 44


# ---------- JWT secret ----------

@pytest.mark.parametrize(
    "env",
    [
        {"RAILWAY_ENVIRONMENT": "production"},
        {"RAILWAY_ENVIRONMENT": "production", "JWT_SECRET": DEFAULT_DEV_JWT_SECRET},
        {"RAILWAY_ENVIRONMENT": "production", "JWT_SECRET": "short"},
        {"ENVIRONMENT": "production", "JWT_SECRET": ""},
        {"APP_ENV": "Prod"},
    ],
)
def test_production_refuses_missing_default_or_weak_secret(env):
    with pytest.raises(RuntimeError):
        resolve_jwt_secret(env)


def test_production_accepts_strong_secret():
    assert resolve_jwt_secret({"RAILWAY_ENVIRONMENT": "production", "JWT_SECRET": STRONG_SECRET}) == STRONG_SECRET


def test_development_falls_back_to_default_with_warning(caplog):
    with caplog.at_level(logging.WARNING):
        assert resolve_jwt_secret({}) == DEFAULT_DEV_JWT_SECRET
    assert any("JWT_SECRET" in record.getMessage() for record in caplog.records)


def test_development_uses_configured_secret():
    assert resolve_jwt_secret({"JWT_SECRET": "custom-dev-secret"}) == "custom-dev-secret"


# ---------- /api/chat ----------

CHAT_PAYLOAD = {
    "message": "hi",
    "reports": {},
    "ticker": "NVDA",
    "analysis_date": "2026-11-27",
    "model": "m",
    "api_key": "k",
}


@pytest.fixture
def client():
    return TestClient(app)


def _fake_chat(exc: Exception):
    async def fake(**kwargs):
        raise exc

    return fake


def test_chat_unexpected_error_does_not_leak_details(client, monkeypatch):
    monkeypatch.setattr(chat_service, "chat_with_reports", _fake_chat(RuntimeError(LEAK_MARKER)))
    response = client.post("/api/chat", json=CHAT_PAYLOAD)
    assert response.status_code == 500
    assert LEAK_MARKER not in response.text


def test_chat_service_error_message_is_passed_through(client, monkeypatch):
    monkeypatch.setattr(chat_service, "chat_with_reports", _fake_chat(chat_service.ChatServiceError("請稍後再試")))
    response = client.post("/api/chat", json=CHAT_PAYLOAD)
    assert response.status_code == 500
    assert "請稍後再試" in response.text


def test_chat_service_masks_unrecognised_llm_errors(monkeypatch):
    class BoomClient:
        def __init__(self, **kwargs):
            pass

        class chat:
            class completions:
                @staticmethod
                async def create(**kwargs):
                    raise RuntimeError(LEAK_MARKER)

    monkeypatch.setattr(chat_service, "AsyncOpenAI", BoomClient)

    with pytest.raises(chat_service.ChatServiceError) as exc_info:
        asyncio.run(
            chat_service.chat_with_reports(
                message="hi", reports={}, ticker="NVDA", analysis_date="2026-11-27", history=None,
                model="m", api_key="k", base_url="https://api.openai.com/v1",
            )
        )
    assert LEAK_MARKER not in str(exc_info.value)


# ---------- Google OAuth ----------

class _FakeResponse:
    status_code = 400
    headers = {"content-type": "application/json"}
    text = LEAK_MARKER

    def json(self):
        return {"error": LEAK_MARKER}


class _FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def post(self, *args, **kwargs):
        return _FakeResponse()


@pytest.fixture
def oauth_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "secret")
    monkeypatch.setattr(auth_module.httpx, "AsyncClient", _FakeAsyncClient)

    async def fake_db():
        yield None

    app.dependency_overrides[get_db] = fake_db
    yield
    app.dependency_overrides.pop(get_db, None)


def test_google_token_exchange_failure_does_not_leak_upstream_body(client, oauth_env):
    response = client.post("/api/auth/google/token", json={"code": "c", "redirect_uri": "https://x.example/cb"})
    assert response.status_code == 400
    assert LEAK_MARKER not in response.text


def test_google_callback_failure_does_not_leak_upstream_body(client, oauth_env):
    response = client.get("/api/auth/google/callback", params={"code": "c"})
    assert response.status_code == 400
    assert LEAK_MARKER not in response.text
