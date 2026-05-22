"""Async subprocess wrappers for Codex CLI and Anti-Gravity CLI.

Smoke-tested 2026-05-21 — see agents-sdk/docs/multi-cli-integration-patterns.md
§Smoke Test Evidence for the ground-truth behavior. These wrappers are the
single point in the codebase that knows the CLIs' trust flags, sandbox modes,
and output shapes. Both vault_critic and (future) tools/llm-council adapters
import from here.

Trust flags / sandbox modes are set explicitly per invocation; silent reliance
on inherited env is a latent bug we are deliberately avoiding.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_CODEX_TOKENS_RE = re.compile(r"tokens used\s*\n\s*([\d,]+)")


def parse_codex_tokens(stderr_text: str) -> int | None:
    """Return the token count from Codex's `tokens used` footer, or None.

    Codex prints `tokens used\\n<count>` at the end of stderr. The count may
    or may not contain comma thousands separators depending on terminal width.
    """
    m = _CODEX_TOKENS_RE.search(stderr_text or "")
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


@dataclass(frozen=True)
class CLIResponse:
    """Result of a single CLI invocation.

    `text` is the raw markdown response (Codex stdout or Anti-Gravity
    `response` field). `tokens` is None when the CLI did not report a
    token count. `rate_capped` is set by the wrapper when the CLI's
    stderr matches a known rate-cap signature; the caller MUST treat
    rate-capped responses as failures even if exit_code == 0.
    """

    cli: Literal["codex", "antigravity"]
    text: str
    tokens: int | None
    duration_s: float
    exit_code: int
    rate_capped: bool
    error: str | None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


_RATE_CAP_PATTERNS = (
    "rate limit",
    "429",
    "quota",
    "resource_exhausted",
    "too many requests",
)


def detect_rate_cap(cli: str, stderr_text: str) -> bool:
    """Heuristic rate-cap detector. True when stderr looks rate-capped.

    Both Codex and Anti-Gravity surface rate-cap errors as free-text or JSON
    in stderr (no consistent structured signal). We match a small set of
    case-insensitive substrings that cover the documented + anecdotal shapes.
    False positives on non-cap errors are tolerable — the run is marked
    partial either way and the wrapper logs full stderr.
    """
    lowered = (stderr_text or "").lower()
    return any(p in lowered for p in _RATE_CAP_PATTERNS)


CODEX_BINARY = "/opt/homebrew/bin/codex"
CODEX_DEFAULT_TIMEOUT_S = 120


async def run_codex(prompt: str, timeout_s: float = CODEX_DEFAULT_TIMEOUT_S) -> CLIResponse:
    """Invoke `codex exec` with read-only sandbox and skip-git-repo-check.

    Runs from `Path.home()` (trusted per ~/.codex/config.toml `[projects]`).
    Captures stdout (markdown response) and stderr (session metadata +
    `tokens used` footer). Returns a CLIResponse — never raises on CLI failure;
    timeouts and rate-caps surface via response fields.
    """
    cmd = [
        CODEX_BINARY,
        "exec",
        "--sandbox", "read-only",
        "--skip-git-repo-check",
        prompt,
    ]
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex binary missing: {exc}",
        )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex timeout after {timeout_s}s",
        )

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    return CLIResponse(
        cli="codex",
        text=stdout_text,
        tokens=parse_codex_tokens(stderr_text),
        duration_s=time.monotonic() - t0,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=detect_rate_cap("codex", stderr_text),
        error=None if proc.returncode == 0 else stderr_text[:500],
    )


ANTIGRAVITY_BINARY = "/opt/homebrew/bin/gemini"
ANTIGRAVITY_DEFAULT_TIMEOUT_S = 120


def _antigravity_tokens(payload: dict) -> int | None:
    """Pluck the total token count from Anti-Gravity stats, model-name-agnostic.

    `stats.models` is a {<model_name>: {tokens: {total: int, ...}}} map.
    The model name is whichever the auto-router resolved to and may change
    over time, so we read whichever single key is present.
    """
    models = (payload.get("stats") or {}).get("models") or {}
    if not models:
        return None
    # If multiple models surface (multi-model routing in a future CLI version),
    # sum them — total across the call is the right number for our manifest.
    total = 0
    found = False
    for entry in models.values():
        tk = (entry or {}).get("tokens") or {}
        if "total" in tk:
            total += int(tk["total"])
            found = True
    return total if found else None


async def run_antigravity(prompt: str, timeout_s: float = ANTIGRAVITY_DEFAULT_TIMEOUT_S) -> CLIResponse:
    """Invoke `gemini -p` with JSON output and plan approval mode.

    Trust set via GEMINI_CLI_TRUST_WORKSPACE=true added to the inherited
    process env (the var is set explicitly per invocation; the surrounding
    env is preserved). Sandbox via --approval-mode plan (read-only per
    smoke test). Returns a CLIResponse; never raises on CLI failure.
    """
    cmd = [
        ANTIGRAVITY_BINARY,
        "-p", prompt,
        "--output-format", "json",
        "--approval-mode", "plan",
    ]
    env = {**os.environ, "GEMINI_CLI_TRUST_WORKSPACE": "true"}
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
            env=env,
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"gemini binary missing: {exc}",
        )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"antigravity timeout after {timeout_s}s",
        )

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    duration = time.monotonic() - t0
    rate_capped = detect_rate_cap("antigravity", stderr_text)

    try:
        payload = json.loads(stdout_text)
    except json.JSONDecodeError as exc:
        return CLIResponse(
            cli="antigravity", text=stdout_text, tokens=None,
            duration_s=duration,
            exit_code=proc.returncode if proc.returncode is not None else -1,
            rate_capped=rate_capped,
            error=f"antigravity json parse failed: {exc}",
        )

    return CLIResponse(
        cli="antigravity",
        text=str(payload.get("response", "")),
        tokens=_antigravity_tokens(payload),
        duration_s=duration,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=rate_capped,
        error=None if proc.returncode == 0 else stderr_text[:500],
    )
