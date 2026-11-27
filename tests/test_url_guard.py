"""SSRF 防護：驗證使用者可控的 LLM base_url 不能指向內網或非 http(s) 協定。"""
import socket

import pytest
from pydantic import ValidationError

from backend.app.core import url_guard
from backend.app.core.url_guard import validate_outbound_url
from backend.app.models.schemas import AnalysisRequest, ChatRequest, ValidateKeysRequest


def _fake_resolver(mapping):
    def fake_getaddrinfo(host, port, *args, **kwargs):
        ips = mapping.get(host)
        if ips is None:
            raise socket.gaierror("unknown host")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port or 443)) for ip in ips]

    return fake_getaddrinfo


@pytest.fixture(autouse=True)
def _public_dns(monkeypatch):
    monkeypatch.delenv("ALLOW_PRIVATE_LLM_URLS", raising=False)
    monkeypatch.setattr(
        url_guard.socket,
        "getaddrinfo",
        _fake_resolver(
            {
                "api.openai.com": ["104.18.7.192"],
                "evil.example.com": ["10.0.0.5"],
                "mixed.example.com": ["104.18.7.192", "169.254.169.254"],
            }
        ),
    )


def test_accepts_public_https_url():
    assert validate_outbound_url("https://api.openai.com/v1") == "https://api.openai.com/v1"


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1:9999/x",
        "https://localhost/v1",
        "https://169.254.169.254/latest/meta-data",
        "https://10.1.2.3/v1",
        "https://192.168.0.1/v1",
        "https://[::1]/v1",
        "https://0.0.0.0/v1",
        "https://[::ffff:127.0.0.1]/v1",
        "https://2130706433/v1",
    ],
)
def test_rejects_private_and_loopback_literals(url):
    with pytest.raises(ValueError):
        validate_outbound_url(url)


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://api.openai.com/", "gopher://api.openai.com/", "api.openai.com/v1"])
def test_rejects_non_http_schemes(url):
    with pytest.raises(ValueError):
        validate_outbound_url(url)


def test_rejects_plain_http_even_for_public_host():
    with pytest.raises(ValueError):
        validate_outbound_url("http://api.openai.com/v1")


def test_rejects_hostname_resolving_to_private_ip():
    with pytest.raises(ValueError):
        validate_outbound_url("https://evil.example.com/v1")


def test_rejects_when_any_resolved_address_is_private():
    with pytest.raises(ValueError):
        validate_outbound_url("https://mixed.example.com/v1")


def test_rejects_unresolvable_host():
    with pytest.raises(ValueError):
        validate_outbound_url("https://nope.invalid/v1")


def test_rejects_embedded_credentials():
    with pytest.raises(ValueError):
        validate_outbound_url("https://user:pw@api.openai.com/v1")


def test_opt_in_allows_private_and_http(monkeypatch):
    monkeypatch.setenv("ALLOW_PRIVATE_LLM_URLS", "true")
    assert validate_outbound_url("http://127.0.0.1:11434/v1") == "http://127.0.0.1:11434/v1"


def test_opt_in_still_rejects_non_http_schemes(monkeypatch):
    monkeypatch.setenv("ALLOW_PRIVATE_LLM_URLS", "true")
    with pytest.raises(ValueError):
        validate_outbound_url("file:///etc/passwd")


def test_chat_request_rejects_internal_base_url():
    with pytest.raises(ValidationError):
        ChatRequest(
            message="hi", reports={}, ticker="NVDA", analysis_date="2026-11-27",
            model="m", api_key="k", base_url="https://169.254.169.254/",
        )


def test_chat_request_default_base_url_is_valid():
    req = ChatRequest(
        message="hi", reports={}, ticker="NVDA", analysis_date="2026-11-27",
        model="m", api_key="k",
    )
    assert req.base_url == "https://api.openai.com/v1"


def test_validate_keys_rejects_internal_custom_base_url():
    with pytest.raises(ValidationError):
        ValidateKeysRequest(custom_base_url="https://10.0.0.5/v1", custom_api_key="k")


def test_validate_keys_allows_empty_and_missing_custom_base_url():
    assert ValidateKeysRequest(custom_base_url="").custom_base_url == ""
    assert ValidateKeysRequest().custom_base_url is None


@pytest.mark.parametrize("field", ["openai_base_url", "quick_think_base_url", "deep_think_base_url", "embedding_base_url"])
def test_analysis_request_rejects_internal_base_urls(field):
    with pytest.raises(ValidationError):
        AnalysisRequest(ticker="NVDA", analysis_date="2026-11-27", **{field: "https://127.0.0.1/v1"})


def test_analysis_request_defaults_still_valid():
    req = AnalysisRequest(ticker="NVDA", analysis_date="2026-11-27")
    assert req.deep_think_base_url == "https://api.openai.com/v1"
