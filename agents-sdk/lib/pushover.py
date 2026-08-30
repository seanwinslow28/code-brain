"""Pushover push-notification helper.

Credentials live in macOS Keychain (never plaintext in config):
    pushover_user_key   — Sean's user key
    pushover_app_token  — the "sean-claude-notify" app token

Called by hybrid_router.route_to_macbook() on WOL/unreachable failures,
by flush.py on repeated errors, and by phase6_gatecheck.py on failing gates
(see config.toml [notifications] notify_on).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import quote

import httpx

from lib.keychain import get_credential

logger = logging.getLogger(__name__)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_RECEIPT_URL = "https://api.pushover.net/1/receipts/{receipt}.json"
_TIMEOUT = 10.0


class PushoverError(Exception):
    """Raised when a Pushover send fails."""


class PushoverConfigurationError(RuntimeError):
    """Raised when Pushover credentials are missing at agent boot.

    Designed to fail loud at startup instead of silent-logging at notify time —
    a silent failure in the system whose job is surfacing failures is exactly
    the regression vs-019 catches.
    """


def ensure_credentials_or_raise() -> None:
    """Load Pushover keychain creds; raise PushoverConfigurationError if missing.

    Call this at the top of any agent's main entrypoint, before any LLM call,
    so a credential misconfiguration crashes the run early rather than producing
    a quiet-fail cascade of ~40 missing-creds log lines per run.

    Lookup honors environment overrides (PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN)
    first, then falls back to macOS keychain (pushover_user_key / pushover_app_token).
    """
    import os

    # Env-var override first (test fixtures can clear these to force the failure)
    user = os.environ.get("PUSHOVER_USER_KEY")
    token = os.environ.get("PUSHOVER_API_TOKEN")

    if not user or not token:
        # Fall back to keychain using the same lookup as send_push()
        try:
            user = user or get_credential("pushover_user_key")
            token = token or get_credential("pushover_app_token")
        except Exception:
            # Keychain access can fail in test/CI environments — treat as missing
            pass

    if not user or not token:
        missing = [
            name
            for name, value in [("user_key", user), ("api_token", token)]
            if not value
        ]
        raise PushoverConfigurationError(
            f"Pushover credentials missing from environment + keychain: {missing}"
        )


def send_push(
    *,
    title: str,
    message: str,
    priority: int = 0,
    retry: int | None = None,
    expire: int | None = None,
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
    if retry is not None:
        data["retry"] = retry
    if expire is not None:
        data["expire"] = expire
    try:
        resp = httpx.post(PUSHOVER_URL, data=data, timeout=_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise PushoverError(f"Pushover send failed: {exc}") from exc
    return resp.json()


def read_receipt_status(
    receipt: str,
    *,
    app_token: str | None = None,
) -> dict:
    """Read one emergency-priority receipt from Pushover.

    The caller owns polling cadence. This function performs exactly one read
    and raises ``PushoverError`` on missing credentials or HTTP failure.
    """
    token = app_token or get_credential("pushover_app_token")
    if not receipt:
        raise PushoverError("Missing Pushover receipt")
    if not token:
        raise PushoverError("Missing Pushover app token in Keychain")

    url = PUSHOVER_RECEIPT_URL.format(receipt=quote(receipt, safe=""))
    try:
        resp = httpx.get(url, params={"token": token}, timeout=_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise PushoverError(f"Pushover receipt read failed: {exc}") from exc
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


# ── Job Feed strong-fit push (2026-06-18) ────────────────────────────────────
# Instant phone buzz when the job_feed agent surfaces a STRONG role fit (>=4),
# the companion to the email digest. Reuses the existing Pushover Keychain creds
# (no new secret). Best-effort: never raises into the agent run. A per-day
# .pushed-<date>.json ledger dedupes by db_id so the 7 morning fires never
# re-push the same role. `fits` are the agent's (db_id, Posting, ScoringResult)
# tuples (see JobDB.scored_today); attributes are read duck-typed.

def build_strong_fits_push(fits: list[tuple]) -> tuple[str, str]:
    """Return (title, message) summarizing the strong fits. Pure."""
    n = len(fits)
    title = f"{n} strong job fit{'' if n == 1 else 's'}"
    lines = [f"★{s.fit_score} {p.company} — {p.title}" for (_db_id, p, s) in fits[:5]]
    if n > 5:
        lines.append(f"+{n - 5} more")
    return title, "\n".join(lines)


def _load_push_ledger(path: Path) -> set[int]:
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValueError, OSError):
        return set()


def _append_push_ledger(path: Path, ids: list[int]) -> None:
    current = _load_push_ledger(path)
    current.update(ids)
    path.write_text(json.dumps(sorted(current)), encoding="utf-8")


def maybe_push_strong_fits(
    *,
    push_cfg: dict | None,
    fits: list[tuple],
    ledger_path: Path,
    today_iso: str,
    send_fn=None,
) -> dict:
    """Best-effort: push any new strong fits (>= min_fit_score). Never raises.

    Returns {"pushed": int, "error": str | None}. A disabled config or no new
    strong fits is a no-op. `send_fn` is injectable for tests (defaults to
    send_push). Reuses the existing pushover_user_key / pushover_app_token
    Keychain creds.
    """
    if not push_cfg or not push_cfg.get("enabled", False):
        return {"pushed": 0, "error": None}

    min_fit_score = int(push_cfg.get("min_fit_score", 4))
    already = _load_push_ledger(ledger_path)
    new_fits = [
        f
        for f in fits
        if f[2].fit_score is not None
        and f[2].fit_score >= min_fit_score
        and f[0] not in already
    ]
    if not new_fits:
        return {"pushed": 0, "error": None}

    title, message = build_strong_fits_push(new_fits)
    sender = send_fn or send_push
    try:
        sender(title=title, message=message, priority=1)
    except PushoverError as exc:
        logger.error("Pushover strong-fit push failed: %s", exc)
        return {"pushed": 0, "error": str(exc)}

    _append_push_ledger(ledger_path, [db_id for (db_id, _p, _s) in new_fits])
    return {"pushed": len(new_fits), "error": None}
