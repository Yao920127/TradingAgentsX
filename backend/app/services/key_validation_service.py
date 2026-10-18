"""
Live connectivity/auth checks for user-supplied API keys.

Used by the Settings dialog's "Save" action to warn about dead keys without
blocking the save. Every checker is best-effort: a definite auth failure
(401/403, or a provider-specific "invalid key" body) is reported as
"invalid"; anything inconclusive (timeout, network error, unexpected
response shape) is reported as "unknown" rather than falsely flagging a
working key as broken.
"""
import asyncio
import logging
from typing import Any, Dict, Optional, Tuple

import httpx
from openai import AsyncOpenAI
from openai import AuthenticationError as OpenAIAuthError
from openai import PermissionDeniedError as OpenAIPermissionError
from openai import APIConnectionError as OpenAIConnectionError
from openai import APITimeoutError as OpenAITimeoutError
from openai import RateLimitError as OpenAIRateLimitError
from openai import APIStatusError as OpenAIStatusError

from anthropic import AsyncAnthropic
from anthropic import AuthenticationError as AnthropicAuthError
from anthropic import PermissionDeniedError as AnthropicPermissionError
from anthropic import APIConnectionError as AnthropicConnectionError
from anthropic import APITimeoutError as AnthropicTimeoutError
from anthropic import RateLimitError as AnthropicRateLimitError
from anthropic import APIStatusError as AnthropicStatusError

from google import genai as google_genai
from google.genai import errors as google_genai_errors

logger = logging.getLogger(__name__)

_CHECK_TIMEOUT = 10.0  # seconds, per provider call

_ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
_FINMIND_BASE_URL = "https://api.finmindtrade.com/api/v4/data"

# field_name -> (provider display name, OpenAI-compatible base_url) for the
# providers whose auth is "Bearer <key>" against an OpenAI-compatible API,
# mirroring frontend/lib/api-helpers.ts and
# tradingagents/graph/trading_graph.py's _create_llm dispatch.
_OPENAI_COMPATIBLE_FIELDS: Dict[str, Tuple[str, str]] = {
    "openai_api_key": ("OpenAI", "https://api.openai.com/v1"),
    "grok_api_key": ("Grok (xAI)", "https://api.x.ai/v1"),
    "deepseek_api_key": ("DeepSeek", "https://api.deepseek.com/v1"),
    "qwen_api_key": ("Qwen (Alibaba)", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
}


def _result(field: str, provider: str, status: str, reason: str, detail: Optional[str] = None) -> dict:
    return {"field": field, "provider": provider, "status": status, "reason": reason, "detail": detail}


async def _check_openai_compatible(field: str, provider: str, api_key: str, base_url: str) -> dict:
    """Cheap, no-token-spend check: list models. Works for OpenAI, Grok,
    DeepSeek, Qwen, and any OpenAI-compatible custom endpoint."""
    try:
        client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=_CHECK_TIMEOUT, max_retries=0)
        await client.models.list()
        return _result(field, provider, "valid", "ok")
    except (OpenAIAuthError, OpenAIPermissionError) as e:
        return _result(field, provider, "invalid", "auth_failed", str(e)[:300])
    except OpenAIRateLimitError as e:
        return _result(field, provider, "unknown", "rate_limited", str(e)[:300])
    except OpenAITimeoutError as e:
        return _result(field, provider, "unknown", "timeout", str(e)[:300])
    except OpenAIConnectionError as e:
        return _result(field, provider, "unknown", "network_error", str(e)[:300])
    except OpenAIStatusError as e:
        if e.status_code == 404:
            # Endpoint doesn't implement /models (common on some custom
            # OpenAI-compatible gateways) — can't conclude the key is bad.
            return _result(field, provider, "unknown", "unsupported", str(e)[:300])
        if e.status_code in (401, 403):
            return _result(field, provider, "invalid", "auth_failed", str(e)[:300])
        if e.status_code >= 500:
            return _result(field, provider, "unknown", "server_error", str(e)[:300])
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])
    except Exception as e:
        logger.warning(f"Unexpected error validating {field}: {e}")
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])


async def _check_anthropic(api_key: str) -> dict:
    field, provider = "anthropic_api_key", "Anthropic"
    try:
        client = AsyncAnthropic(api_key=api_key, timeout=_CHECK_TIMEOUT, max_retries=0)
        await client.models.list()
        return _result(field, provider, "valid", "ok")
    except (AnthropicAuthError, AnthropicPermissionError) as e:
        return _result(field, provider, "invalid", "auth_failed", str(e)[:300])
    except AnthropicRateLimitError as e:
        return _result(field, provider, "unknown", "rate_limited", str(e)[:300])
    except AnthropicTimeoutError as e:
        return _result(field, provider, "unknown", "timeout", str(e)[:300])
    except AnthropicConnectionError as e:
        return _result(field, provider, "unknown", "network_error", str(e)[:300])
    except AnthropicStatusError as e:
        if e.status_code >= 500:
            return _result(field, provider, "unknown", "server_error", str(e)[:300])
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])
    except Exception as e:
        logger.warning(f"Unexpected error validating anthropic_api_key: {e}")
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])


async def _check_google(api_key: str) -> dict:
    """Google's SDK (google-genai) raises ClientError for a bad key, but
    unlike OpenAI/Anthropic it reports it as HTTP 400 ("API key not valid"),
    not 401/403 — so auth failure is detected by message content, not just
    status code."""
    field, provider = "google_api_key", "Google"
    try:
        client = google_genai.Client(api_key=api_key)

        async def _list_first():
            pager = await client.aio.models.list()
            async for _ in pager:
                break

        await asyncio.wait_for(_list_first(), timeout=_CHECK_TIMEOUT)
        return _result(field, provider, "valid", "ok")
    except google_genai_errors.ClientError as e:
        message = str(e).lower()
        if e.code in (401, 403) or "api key not valid" in message or "api_key_invalid" in message:
            return _result(field, provider, "invalid", "auth_failed", str(e)[:300])
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])
    except google_genai_errors.ServerError as e:
        return _result(field, provider, "unknown", "server_error", str(e)[:300])
    except asyncio.TimeoutError:
        return _result(field, provider, "unknown", "timeout", None)
    except Exception as e:
        logger.warning(f"Unexpected error validating google_api_key: {e}")
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])


async def _check_alpha_vantage(api_key: str) -> dict:
    """Alpha Vantage returns HTTP 200 even for an invalid key — the error
    shows up in the JSON body instead, so the body must be parsed.

    Known limitation (confirmed by live probing, not just docs): Alpha
    Vantage's GLOBAL_QUOTE/TIME_SERIES endpoints accept *any* non-empty
    apikey value and serve real data regardless of whether that key is
    actually registered — they only reject a request with a missing/empty
    apikey param. So a "valid" result here only confirms the key was
    transmitted and the endpoint is reachable, not that this exact key is
    genuinely registered to an account. OVERVIEW was tried first but is
    now a premium-only endpoint on the free tier (confirmed live), which
    would misreport every free-tier key as rate-limited — GLOBAL_QUOTE
    stays on the free tier.
    """
    field, provider = "alpha_vantage_api_key", "Alpha Vantage"
    try:
        async with httpx.AsyncClient(timeout=_CHECK_TIMEOUT) as client:
            resp = await client.get(
                _ALPHA_VANTAGE_BASE_URL,
                params={"function": "GLOBAL_QUOTE", "symbol": "IBM", "apikey": api_key},
            )
        if resp.status_code >= 500:
            return _result(field, provider, "unknown", "server_error", f"HTTP {resp.status_code}")
        if resp.status_code != 200:
            return _result(field, provider, "unknown", "unknown_error", f"HTTP {resp.status_code}")

        try:
            body: Any = resp.json()
        except ValueError:
            return _result(field, provider, "unknown", "unknown_error", "Non-JSON response")

        if isinstance(body, dict) and body.get("Global Quote"):
            return _result(field, provider, "valid", "ok")

        error_msg = (body.get("Error Message") or "") if isinstance(body, dict) else ""
        info_msg = (body.get("Information") or body.get("Note") or "") if isinstance(body, dict) else ""

        if error_msg and ("apikey" in error_msg.lower() or "api key" in error_msg.lower()):
            return _result(field, provider, "invalid", "auth_failed", error_msg[:300])
        if info_msg:
            # Usually a rate-limit or premium-gate message — doesn't confirm
            # the key itself is bad.
            return _result(field, provider, "unknown", "rate_limited", info_msg[:300])
        if error_msg:
            return _result(field, provider, "unknown", "unknown_error", error_msg[:300])
        return _result(field, provider, "unknown", "unknown_error", "Unexpected empty response")
    except httpx.TimeoutException:
        return _result(field, provider, "unknown", "timeout", None)
    except httpx.RequestError as e:
        return _result(field, provider, "unknown", "network_error", str(e)[:300])
    except Exception as e:
        logger.warning(f"Unexpected error validating alpha_vantage_api_key: {e}")
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])


async def _check_finmind(token: str) -> dict:
    """FinMind reports an invalid/malformed token as HTTP 400 (confirmed by
    live probing — e.g. {"msg": "Token is illegal.", "status": 400}), not
    401/403, so the body must be inspected even on a 400 response rather
    than treating it as a generic client error."""
    field, provider = "finmind_api_key", "FinMind"
    try:
        async with httpx.AsyncClient(timeout=_CHECK_TIMEOUT) as client:
            resp = await client.get(
                _FINMIND_BASE_URL,
                headers={"Authorization": f"Bearer {token}"},
                params={"dataset": "TaiwanStockInfo", "data_id": "2330"},
            )

        if resp.status_code >= 500:
            return _result(field, provider, "unknown", "server_error", f"HTTP {resp.status_code}")

        try:
            body: Any = resp.json()
        except ValueError:
            return _result(field, provider, "unknown", "unknown_error", f"HTTP {resp.status_code}, non-JSON response")

        msg = str(body.get("msg", "")).lower() if isinstance(body, dict) else ""

        if resp.status_code in (401, 403) or any(
            k in msg for k in ("token", "authentication", "unauthorized", "illegal")
        ):
            return _result(field, provider, "invalid", "auth_failed", body.get("msg", f"HTTP {resp.status_code}")[:300])
        if "rate limit" in msg or "too many requests" in msg:
            return _result(field, provider, "unknown", "rate_limited", body.get("msg", "")[:300])
        if resp.status_code == 200 and isinstance(body, dict) and (
            body.get("status") == 200 or body.get("data") is not None
        ):
            return _result(field, provider, "valid", "ok")
        return _result(field, provider, "unknown", "unknown_error", f"HTTP {resp.status_code}: {str(body)[:250]}")
    except httpx.TimeoutException:
        return _result(field, provider, "unknown", "timeout", None)
    except httpx.RequestError as e:
        return _result(field, provider, "unknown", "network_error", str(e)[:300])
    except Exception as e:
        logger.warning(f"Unexpected error validating finmind_api_key: {e}")
        return _result(field, provider, "unknown", "unknown_error", str(e)[:300])


async def validate_api_keys(payload: Dict[str, str]) -> Dict[str, dict]:
    """
    Dispatch a validation coroutine per non-empty field in `payload`.
    Returns a dict keyed by field name -> KeyValidationResult-shaped dict.
    Fields that were empty/absent are simply not present in the result.
    """
    tasks: Dict[str, "asyncio.Task"] = {}

    for field, (provider, base_url) in _OPENAI_COMPATIBLE_FIELDS.items():
        key = (payload.get(field) or "").strip()
        if key:
            tasks[field] = asyncio.ensure_future(_check_openai_compatible(field, provider, key, base_url))

    anthropic_key = (payload.get("anthropic_api_key") or "").strip()
    if anthropic_key:
        tasks["anthropic_api_key"] = asyncio.ensure_future(_check_anthropic(anthropic_key))

    google_key = (payload.get("google_api_key") or "").strip()
    if google_key:
        tasks["google_api_key"] = asyncio.ensure_future(_check_google(google_key))

    alpha_vantage_key = (payload.get("alpha_vantage_api_key") or "").strip()
    if alpha_vantage_key:
        tasks["alpha_vantage_api_key"] = asyncio.ensure_future(_check_alpha_vantage(alpha_vantage_key))

    finmind_key = (payload.get("finmind_api_key") or "").strip()
    if finmind_key:
        tasks["finmind_api_key"] = asyncio.ensure_future(_check_finmind(finmind_key))

    # Custom endpoint: only test when BOTH fields are present.
    custom_base_url = (payload.get("custom_base_url") or "").strip()
    custom_api_key = (payload.get("custom_api_key") or "").strip()
    if custom_base_url and custom_api_key:
        tasks["custom_api_key"] = asyncio.ensure_future(
            _check_openai_compatible("custom_api_key", "Custom Endpoint", custom_api_key, custom_base_url)
        )

    if not tasks:
        return {}

    done = await asyncio.gather(*tasks.values(), return_exceptions=True)
    results: Dict[str, dict] = {}
    for field, outcome in zip(tasks.keys(), done):
        if isinstance(outcome, BaseException):
            logger.error(f"Validator for {field} raised unexpectedly: {outcome}")
            results[field] = _result(field, field, "unknown", "unknown_error", str(outcome)[:300])
        else:
            results[field] = outcome
    return results
