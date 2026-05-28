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
    model_id: str
    content: str
    tokens_in: int
    tokens_out: int
    latency_ms: int


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

    async def complete(self, *, model: str, system: str, user: str) -> ModelResponse:
        """Single non-streaming completion call. Retries 5xx; does not retry 4xx."""
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
                content = body["choices"][0]["message"]["content"]
                usage = body.get("usage", {})
                latency_ms = max(1, int((time.perf_counter() - start) * 1000))
                return ModelResponse(
                    model_id=model,
                    content=content,
                    tokens_in=usage.get("prompt_tokens", 0),
                    tokens_out=usage.get("completion_tokens", 0),
                    latency_ms=latency_ms,
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
