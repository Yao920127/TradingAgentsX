"""出站 URL 驗證（SSRF 防護）。

使用者可以自帶 LLM 端點（BYOK），後端會代為發出請求，因此必須擋掉指向內網、
loopback、link-local（含雲端 metadata）的位址與非 http(s) 協定。

預設只允許 https 且所有解析結果都必須是公開位址。本機跑 Ollama 等合法情境，
可設定環境變數 ``ALLOW_PRIVATE_LLM_URLS=true`` 明確放行私有位址與 http。

限制：驗證時與實際連線時各解析一次 DNS，無法完全排除 DNS rebinding；
若部署環境需要更強保證，請另外在網路層（egress 規則）限制。
"""
import ipaddress
import os
import socket
from typing import Optional
from urllib.parse import urlparse

_ALLOW_PRIVATE_ENV = "ALLOW_PRIVATE_LLM_URLS"
_TRUTHY = {"1", "true", "yes", "on"}
_BLOCKED_HOSTNAMES = {"localhost", "localhost.localdomain"}


def _private_urls_allowed() -> bool:
    return os.getenv(_ALLOW_PRIVATE_ENV, "").strip().lower() in _TRUTHY


def _is_public_ip(ip: "ipaddress.IPv4Address | ipaddress.IPv6Address") -> bool:
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        ip = mapped
    return ip.is_global


def _resolve_addresses(host: str, port: Optional[int]) -> list:
    try:
        infos = socket.getaddrinfo(host, port)
    except socket.gaierror as exc:
        raise ValueError(f"無法解析主機：{host}") from exc
    return [ipaddress.ip_address(info[4][0]) for info in infos]


def validate_outbound_url(url: str) -> str:
    """驗證使用者提供的 base_url，通過則原樣回傳，否則丟出 ValueError。"""
    parsed = urlparse(url.strip())
    allow_private = _private_urls_allowed()

    allowed_schemes = {"http", "https"} if allow_private else {"https"}
    if parsed.scheme not in allowed_schemes:
        raise ValueError("base_url 必須使用 https")

    host = parsed.hostname
    if not host:
        raise ValueError("base_url 缺少主機名稱")
    if parsed.username or parsed.password:
        raise ValueError("base_url 不可包含帳號或密碼")

    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("base_url 的連接埠不合法") from exc

    if allow_private:
        return url

    if host.lower().rstrip(".") in _BLOCKED_HOSTNAMES:
        raise ValueError("base_url 不可指向本機或內部位址")

    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        addresses = _resolve_addresses(host, port)

    if not addresses or not all(_is_public_ip(ip) for ip in addresses):
        raise ValueError("base_url 不可指向本機或內部位址")

    return url


def validate_optional_outbound_url(url: Optional[str]) -> Optional[str]:
    """欄位為選填：None 與空字串視為未設定，直接放行。"""
    if url is None or not url.strip():
        return url
    return validate_outbound_url(url)
