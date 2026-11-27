"""以 IP 為單位的記憶體內限流 middleware。

client IP 的判定不再直接信任 ``X-Forwarded-For`` 的第一個值：該值由發出請求的人
自行填寫，換一個假 IP 就能繞過限流。反向代理會把它看到的來源 IP 附加在最右邊，
所以改為由右往左取第 ``TRUSTED_PROXY_HOPS`` 個項目（預設 1，代表只有一層代理）。
若代理層數不是 1，請設定環境變數 ``TRUSTED_PROXY_HOPS``；設為 0 則完全忽略
``X-Forwarded-For``，只使用 socket 對端位址。
"""
import logging
import os
import time
from collections import defaultdict
from typing import Optional

from fastapi import Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware  # type: ignore

logger = logging.getLogger(__name__)

DEFAULT_TRUSTED_PROXY_HOPS = 1
MAX_TRACKED_CLIENTS = 10_000
_HEALTH_PATH = "/api/health"


def trusted_proxy_hops_from_env() -> int:
    raw = os.getenv("TRUSTED_PROXY_HOPS", "").strip()
    if not raw:
        return DEFAULT_TRUSTED_PROXY_HOPS
    try:
        return max(0, int(raw))
    except ValueError:
        logger.warning("TRUSTED_PROXY_HOPS=%r 不是整數，改用預設值 %d", raw, DEFAULT_TRUSTED_PROXY_HOPS)
        return DEFAULT_TRUSTED_PROXY_HOPS


def resolve_client_ip(forwarded_for: Optional[str], peer_host: str, trusted_hops: int) -> str:
    """由右往左取第 ``trusted_hops`` 個 X-Forwarded-For 項目；資料不足時退回 socket 對端位址。"""
    if trusted_hops <= 0 or not forwarded_for:
        return peer_host
    entries = [part.strip() for part in forwarded_for.split(",") if part.strip()]
    if len(entries) < trusted_hops:
        return peer_host
    return entries[-trusted_hops]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """簡單的記憶體內限流；過期的 IP 會被清除，追蹤數量有上限。"""

    def __init__(
        self,
        app,
        max_requests: int = 30,
        window_seconds: int = 60,
        trusted_proxy_hops: Optional[int] = None,
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.trusted_proxy_hops = (
            trusted_proxy_hops if trusted_proxy_hops is not None else trusted_proxy_hops_from_env()
        )
        self.requests: dict[str, list[float]] = defaultdict(list)
        self._last_purge = time.time()

    def _purge_expired(self, now: float) -> None:
        cutoff = now - self.window_seconds
        expired = [ip for ip, stamps in self.requests.items() if not stamps or stamps[-1] <= cutoff]
        for ip in expired:
            del self.requests[ip]
        self._last_purge = now

    def _make_room_for(self, ip: str, now: float) -> None:
        if ip in self.requests:
            return
        if now - self._last_purge >= self.window_seconds:
            self._purge_expired(now)
        if len(self.requests) >= MAX_TRACKED_CLIENTS:
            self._purge_expired(now)
        while len(self.requests) >= MAX_TRACKED_CLIENTS:
            del self.requests[next(iter(self.requests))]

    async def dispatch(self, request: Request, call_next):
        if request.url.path == _HEALTH_PATH:
            return await call_next(request)

        peer = request.client.host if request.client else "unknown"
        client_ip = resolve_client_ip(request.headers.get("X-Forwarded-For"), peer, self.trusted_proxy_hops)

        now = time.time()
        self._make_room_for(client_ip, now)

        cutoff = now - self.window_seconds
        stamps = [t for t in self.requests[client_ip] if t > cutoff]
        self.requests[client_ip] = stamps

        if len(stamps) >= self.max_requests:
            retry_after = max(1, int(self.window_seconds - (now - stamps[0])))
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too many requests",
                    "message": f"Rate limit exceeded. Please wait {retry_after} seconds.",
                    "retry_after": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )

        stamps.append(now)
        response = await call_next(request)

        remaining = self.max_requests - len(stamps)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int(now + self.window_seconds))
        return response
