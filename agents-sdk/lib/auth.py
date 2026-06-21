"""Headless auth helpers for the agent fleet.

Scheduled (launchd) SDK agents have no interactive session in which to refresh
the `claude login` OAuth credential, so an expired access token surfaces as a
401 (observed 2026-06-20: the 08:30 daily-driver run failed with "Invalid
authentication credentials", cost=$0, 1 turn). A long-lived token minted with
`claude setup-token` and stored in Keychain removes that dependency — it is
read at runtime and injected as CLAUDE_CODE_OAUTH_TOKEN into the spawned
`claude` CLI's environment.

One-time setup (interactive — only Sean can mint the token):

    claude setup-token                                   # prints a long-lived token
    python3 lib/keychain.py set claude_code_oauth_token <token>

The token is NEVER written to a tracked file (this is a public repo); it lives
only in the macOS Keychain. If neither the env var nor the Keychain credential
is present, callers fall back to the pre-existing interactive OAuth credential
(unchanged behavior).
"""

from __future__ import annotations

import os
from typing import Callable

from lib.keychain import get_credential

OAUTH_TOKEN_ENV = "CLAUDE_CODE_OAUTH_TOKEN"
OAUTH_TOKEN_CREDENTIAL = "claude_code_oauth_token"


def resolve_oauth_token(
    *, keychain_get: Callable[[str], str | None] = get_credential
) -> str | None:
    """Return a long-lived Claude Code OAuth token for headless runs.

    Precedence: the CLAUDE_CODE_OAUTH_TOKEN env var, then the Keychain
    credential ``claude_code_oauth_token``. Returns None when neither is set,
    in which case callers should leave auth to the SDK's default (interactive
    `claude login` OAuth credential).

    Args:
        keychain_get: Injectable Keychain reader (for tests). Defaults to the
            real macOS Keychain helper.
    """
    env_token = os.environ.get(OAUTH_TOKEN_ENV)
    if env_token:
        return env_token
    return keychain_get(OAUTH_TOKEN_CREDENTIAL)
