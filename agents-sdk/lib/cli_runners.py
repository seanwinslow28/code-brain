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
