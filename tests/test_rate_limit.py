"""RateLimitMiddleware：不可被偽造的 X-Forwarded-For 繞過，且過期的 IP key 要被清除。"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.core import rate_limit
from backend.app.core.rate_limit import RateLimitMiddleware, resolve_client_ip

MAX_REQUESTS = 3


def _client(trusted_hops: int = 1) -> tuple[TestClient, RateLimitMiddleware]:
    app = FastAPI()

    @app.get("/api/ping")
    async def ping():
        return {"ok": True}

    @app.get("/api/health")
    async def health():
        return {"ok": True}

    app.add_middleware(RateLimitMiddleware, max_requests=MAX_REQUESTS, window_seconds=60, trusted_proxy_hops=trusted_hops)
    client = TestClient(app)
    middleware = _find_middleware(app)
    return client, middleware


def _find_middleware(app: FastAPI) -> RateLimitMiddleware:
    app.middleware_stack = app.build_middleware_stack()
    layer = app.middleware_stack
    while layer is not None:
        if isinstance(layer, RateLimitMiddleware):
            return layer
        layer = getattr(layer, "app", None)
    raise AssertionError("RateLimitMiddleware not installed")


def _hit(client: TestClient, forwarded_for: str | None = None) -> int:
    headers = {"X-Forwarded-For": forwarded_for} if forwarded_for is not None else {}
    return client.get("/api/ping", headers=headers).status_code


def test_spoofed_leading_forwarded_for_entries_do_not_bypass_limit():
    client, _ = _client(trusted_hops=1)
    # 反向代理會把真實 client IP 附加在最右邊；攻擊者只能控制左邊的項目
    statuses = [_hit(client, f"10.9.9.{i}, 203.0.113.7") for i in range(MAX_REQUESTS + 2)]
    assert statuses[:MAX_REQUESTS] == [200] * MAX_REQUESTS
    assert statuses[MAX_REQUESTS:] == [429, 429]


def test_different_real_clients_are_limited_independently():
    client, _ = _client(trusted_hops=1)
    for _ in range(MAX_REQUESTS):
        assert _hit(client, "1.1.1.1, 203.0.113.7") == 200
    assert _hit(client, "1.1.1.1, 203.0.113.7") == 429
    assert _hit(client, "1.1.1.1, 198.51.100.9") == 200


def test_without_forwarded_for_uses_socket_peer():
    client, _ = _client(trusted_hops=1)
    statuses = [_hit(client) for _ in range(MAX_REQUESTS + 1)]
    assert statuses[-1] == 429


def test_zero_trusted_hops_ignores_forwarded_for_entirely():
    client, _ = _client(trusted_hops=0)
    statuses = [_hit(client, f"10.9.9.{i}") for i in range(MAX_REQUESTS + 1)]
    assert statuses[-1] == 429


def test_health_endpoint_is_not_rate_limited():
    client, _ = _client()
    assert all(client.get("/api/health").status_code == 200 for _ in range(MAX_REQUESTS * 3))


@pytest.mark.parametrize(
    "header, hops, peer, expected",
    [
        ("a, b, c", 1, "9.9.9.9", "c"),
        ("a, b, c", 2, "9.9.9.9", "b"),
        ("a", 2, "9.9.9.9", "9.9.9.9"),
        (None, 1, "9.9.9.9", "9.9.9.9"),
        ("a, b", 0, "9.9.9.9", "9.9.9.9"),
        (" , ", 1, "9.9.9.9", "9.9.9.9"),
    ],
)
def test_resolve_client_ip(header, hops, peer, expected):
    assert resolve_client_ip(header, peer, hops) == expected


def test_expired_ip_entries_are_purged(monkeypatch):
    now = [1_000.0]
    monkeypatch.setattr(rate_limit.time, "time", lambda: now[0])
    client, middleware = _client(trusted_hops=1)

    for i in range(20):
        _hit(client, f"x, 203.0.113.{i}")
    assert len(middleware.requests) == 20

    now[0] += 61  # 超過 window
    _hit(client, "x, 198.51.100.1")
    assert set(middleware.requests) == {"198.51.100.1"}


def test_tracked_ip_count_is_bounded(monkeypatch):
    monkeypatch.setattr(rate_limit, "MAX_TRACKED_CLIENTS", 10)
    client, middleware = _client(trusted_hops=1)
    for i in range(50):
        _hit(client, f"x, 203.0.113.{i}")
    assert len(middleware.requests) <= 10


def test_trusted_hops_read_from_environment(monkeypatch):
    monkeypatch.setenv("TRUSTED_PROXY_HOPS", "2")
    assert rate_limit.trusted_proxy_hops_from_env() == 2
    monkeypatch.setenv("TRUSTED_PROXY_HOPS", "not-a-number")
    assert rate_limit.trusted_proxy_hops_from_env() == 1
    monkeypatch.delenv("TRUSTED_PROXY_HOPS")
    assert rate_limit.trusted_proxy_hops_from_env() == 1
