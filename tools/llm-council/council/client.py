"""Async OpenRouter client wrapping httpx with retry + typed responses."""

import asyncio
import os
import time
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

# Load .env walking up from CWD; superuser-pack root is expected to hold OPENROUTER_API_KEY.
load_dotenv()

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


@dataclass
class ModelResponse:
    model_id: str  # the REQUESTED model id — lineage/policy selection key
    content: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    # Provider-reported audit/measurement fields (nullable; older/mocked responses omit them):
    returned_model_id: str | None = None  # the model OpenRouter actually served
    generation_id: str | None = None      # OpenRouter generation id (reconciliation key)
    cost: float | None = None             # provider-reported usage.cost (authoritative $)
    finish_reason: str | None = None      # terminal reason for this choice


class ClientError(Exception):
    """Raised on any non-recoverable client failure."""


class OpenRouterClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = OPENROUTER_BASE,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
    ) -> None:
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise ClientError(
                "OPENROUTER_API_KEY not found in environment. "
                "Set it in the superuser-pack root .env file."
            )
        self._api_key = key
        self._base_url = base_url
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int | None = None,
        provider: dict | None = None,
    ) -> ModelResponse:
        """Single non-streaming completion call. Retries 5xx; does not retry 4xx.

        `max_tokens`, when set, caps generated (incl. reasoning) tokens. `provider`, when
        set, is OpenRouter's provider-routing object (e.g. a fail-closed `max_price` ceiling
        + `allow_fallbacks:false` + `require_parameters:true`); the caller owns its values,
        the client validates shape and injects it. Both are validated before any network
        call (fail closed).
        """
        if max_tokens is not None:
            if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
                raise ClientError(
                    f"max_tokens must be a positive int when set; got {max_tokens!r}"
                )
        if provider is not None and not isinstance(provider, dict):
            raise ClientError(f"provider must be a dict when set; got {provider!r}")
        url = f"{self._base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if provider is not None:
            payload["provider"] = provider

        attempt = 0
        start = time.perf_counter()
        while True:
            try:
                resp = await self._client.post(url, headers=headers, json=payload)
            except httpx.TimeoutException as e:
                if attempt >= self._max_retries:
                    raise ClientError(f"timeout after {self._timeout}s on model {model}") from e
                attempt += 1
                await asyncio.sleep(0.5 * (2 ** attempt))
                continue

            if 200 <= resp.status_code < 300:
                body = resp.json()
                if "choices" not in body or not body["choices"]:
                    err = body.get("error", {}) if isinstance(body, dict) else {}
                    msg = err.get("message") or "response had no choices"
                    code = err.get("code", "")
                    raise ClientError(
                        f"OpenRouter 200-with-no-choices on model {model}: {code} {msg}"
                    )
                choice = body["choices"][0]
                content = choice["message"]["content"]
                usage = body.get("usage", {})
                latency_ms = max(1, int((time.perf_counter() - start) * 1000))
                return ModelResponse(
                    model_id=model,
                    content=content,
                    tokens_in=usage.get("prompt_tokens", 0),
                    tokens_out=usage.get("completion_tokens", 0),
                    latency_ms=latency_ms,
                    returned_model_id=body.get("model"),
                    generation_id=body.get("id"),
                    cost=usage.get("cost"),
                    finish_reason=choice.get("finish_reason"),
                )

            # 4xx — do not retry. Surface the error.
            if 400 <= resp.status_code < 500:
                try:
                    msg = resp.json().get("error", {}).get("message", resp.text)
                    code = resp.json().get("error", {}).get("code", "")
                except Exception:
                    msg = resp.text
                    code = ""
                raise ClientError(
                    f"4xx from OpenRouter on model {model}: {resp.status_code} {code} {msg}"
                )

            # 5xx — retry if budget remains.
            if attempt >= self._max_retries:
                raise ClientError(
                    f"persistent 5xx from OpenRouter on model {model}: {resp.status_code}"
                )
            attempt += 1
            await asyncio.sleep(0.5 * (2 ** attempt))
