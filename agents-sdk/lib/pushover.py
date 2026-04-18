"""Pushover push-notification helper.

Credentials live in macOS Keychain (never plaintext in config):
    pushover_user_key   — Sean's user key
    pushover_app_token  — the "sean-claude-notify" app token

Called by hybrid_router.route_to_macbook() on WOL/unreachable failures,
by flush.py on repeated errors, and by phase6_gatecheck.py on failing gates
(see config.toml [notifications] notify_on).
"""

from __future__ import annotations

import logging

import httpx

from lib.keychain import get_credential

logger = logging.getLogger(__name__)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
_TIMEOUT = 10.0


class PushoverError(Exception):
    """Raised when a Pushover send fails."""


def send_push(
    *,
    title: str,
    message: str,
    priority: int = 0,
    user_key: str | None = None,
    app_token: str | None = None,
) -> dict:
    """Send a Pushover notification.

    Credentials default to macOS Keychain lookups (`pushover_user_key`,
    `pushover_app_token`). Pass `user_key`/`app_token` to override (for tests).

    Returns the parsed JSON response on success.
    Raises PushoverError on missing creds or HTTP failure.
    """
    user = user_key or get_credential("pushover_user_key")
    token = app_token or get_credential("pushover_app_token")
    if not user or not token:
        raise PushoverError(
            "Missing Pushover credentials in Keychain "
            "(pushover_user_key / pushover_app_token)"
        )

    data = {
        "token": token,
        "user": user,
        "title": title,
        "message": message,
        "priority": priority,
    }
    try:
        resp = httpx.post(PUSHOVER_URL, data=data, timeout=_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise PushoverError(f"Pushover send failed: {exc}") from exc
    return resp.json()


def notify_wol_failure(*, task: str, machine: str, detail: str = "") -> None:
    """Canonical Phase 6 push for WOL / unreachable-machine failures.

    Best-effort: logs rather than raises on send failure so callers can
    continue their own error handling (e.g., deferring synthesis to next night).
    """
    body = f"{machine} unreachable for task {task}."
    if detail:
        body += f" {detail}"
    try:
        send_push(
            title=f"MacBook WOL failed ({machine})",
            message=body,
            priority=0,
        )
    except PushoverError as exc:
        logger.error("Pushover notify_wol_failure send failed: %s", exc)


def notify_agent_error(*, agent: str, error: str) -> None:
    try:
        send_push(
            title=f"Agent error: {agent}",
            message=error[:900],
            priority=0,
        )
    except PushoverError as exc:
        logger.error("Pushover notify_agent_error send failed: %s", exc)


def notify_gate_check_fail(*, criterion: str, detail: str = "") -> None:
    try:
        send_push(
            title=f"Gate check FAIL: {criterion}",
            message=detail[:900] or "See gate-check output.",
            priority=1,
        )
    except PushoverError as exc:
        logger.error("Pushover notify_gate_check_fail send failed: %s", exc)
