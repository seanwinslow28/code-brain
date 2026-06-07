#!/usr/bin/env python3
"""Governance demo — replay a synthetic spend request through the three control legs.

This is a *stubbed* harness. It does NOT call an LLM, an agent runner, or any paid
API. Each fixture under `fixtures/` is a hand-authored, obviously-synthetic record of
what an agent runner *would have* requested. The script replays that request through
the same shape of control logic the real fleet enforces (Authority -> Recovery ->
Audit) and prints the outcome.

Three legs, exercised by three fixtures:

  - allowed       Authority passes, spend is within the daily cap -> ALLOW (exit 0)
  - over_budget   spend breaches the daily cap -> circuit trips BEFORE any "spend",
                  a breach row is appended to the ledger, Pushover is paged,
                  the rollback path is printed -> BUDGET BREACH (exit 7)
  - missing_auth  the keychain-gated key is stripped -> Authority denies at the
                  credential gate, before budget is even evaluated -> (exit 3)

Exit-code convention (DEMO-ONLY — see README):
    0  allowed
    3  auth denied (keychain gate)
    7  budget breach (circuit tripped)

The production fleet enforces hook exit codes 0/1/2 and typed exceptions
(RouteUnavailable, budget-cap aborts); exit 7 here is a demo convention chosen so the
worked example has one unambiguous, greppable breach signal. See
agents-sdk/docs/CONTROL_ARCHITECTURE.md, "Worked example".

Stdlib only — no third-party deps, runs anywhere Python 3.10+ does.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES_DIR = HERE / "fixtures"
DEFAULT_LEDGER = HERE / "outputs" / "sample_ledger.jsonl"

# DEMO-ONLY exit-code convention (see module docstring + README).
EXIT_ALLOWED = 0
EXIT_AUTH_DENIED = 3
EXIT_BUDGET_BREACH = 7

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
ROLLBACK_HINT = (
    "rollback: set the agent's `max_budget_usd` / `daily_cap_usd` deliberately in "
    "agents-sdk/config.toml, or `git revert` the change that raised the spend. "
    "No code change required — the cap is policy, not logic."
)


@dataclass
class ReplayResult:
    """Outcome of replaying one fixture. Returned by run(); tests assert on it."""

    fixture: str
    decision: str  # "allowed" | "auth_denied" | "budget_breach"
    exit_code: int
    pushover_fired: bool
    pushover_mode: str | None  # "dry" | "live" | None
    budget_evaluated: bool
    ledger_record: dict = field(default_factory=dict)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_fixture(name: str) -> dict:
    path = FIXTURES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"unknown fixture {name!r}; expected one of: "
            f"{', '.join(sorted(p.stem for p in FIXTURES_DIR.glob('*.json')))}"
        )
    return json.loads(path.read_text())


def _append_ledger(ledger_path: Path, record: dict) -> None:
    """Append one JSON object per line — the append-only shape the real ledgers use."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _page_pushover(title: str, message: str, *, dry: bool) -> tuple[bool, str]:
    """Escalation leg. dry=True logs and never hits the network (CI + rehearsal).

    Live mode reads PUSHOVER_USER_KEY / PUSHOVER_API_TOKEN from the environment (the
    real fleet sources these from the macOS Keychain via lib/keychain.py; this demo
    keeps the dependency surface to stdlib + env). If creds are absent in live mode,
    it reports that it *would* have paged rather than raising — the demo must never
    crash on a missing phone.
    """
    if dry:
        print(f"[pushover:dry] would page -> {title}: {message}")
        return True, "dry"

    user = os.environ.get("PUSHOVER_USER_KEY")
    token = os.environ.get("PUSHOVER_API_TOKEN")
    if not user or not token:
        print(
            "[pushover:live] PUSHOVER_USER_KEY / PUSHOVER_API_TOKEN not set; "
            "would have paged. (Set them, or use --dry-pushover.)"
        )
        return False, "live"

    data = urllib.parse.urlencode(
        {"token": token, "user": user, "title": title, "message": message}
    ).encode()
    try:
        with urllib.request.urlopen(  # noqa: S310 — fixed, trusted Pushover URL
            urllib.request.Request(PUSHOVER_URL, data=data), timeout=10
        ) as resp:
            ok = resp.status == 200
        print(f"[pushover:live] paged (HTTP {resp.status})")
        return ok, "live"
    except urllib.error.URLError as exc:  # network down — demo stays alive
        print(f"[pushover:live] send failed ({exc}); breach still recorded in ledger.")
        return False, "live"


def run(
    fixture_name: str,
    *,
    dry_pushover: bool = False,
    ledger_path: Path | None = None,
) -> ReplayResult:
    """Replay one fixture through Authority -> Recovery -> Audit. Pure enough to test."""
    ledger_path = ledger_path or DEFAULT_LEDGER
    fx = load_fixture(fixture_name)

    task = fx.get("task", "<unnamed task>")
    requested = float(fx.get("requested_usd", 0.0))
    daily_spent = float(fx.get("daily_spent_usd", 0.0))
    daily_cap = float(fx.get("daily_cap_usd", 0.0))
    key_name = fx.get("keychain_key", "<none>")
    auth_present = bool(fx.get("auth_present", True))

    base_record = {
        "ts": _now_iso(),
        "fixture": fixture_name,
        "task": task,
        "keychain_key": key_name,
        "requested_usd": requested,
        "daily_spent_usd": daily_spent,
        "daily_cap_usd": daily_cap,
    }

    # ---- Leg 1: AUTHORITY (credential gate) — runs before any spend evaluation ----
    if not auth_present:
        record = {**base_record, "decision": "auth_denied", "exit_code": EXIT_AUTH_DENIED}
        _append_ledger(ledger_path, record)
        print(
            f"[authority] DENY — keychain key {key_name!r} is absent. "
            f"No spend evaluated. (exit {EXIT_AUTH_DENIED})"
        )
        return ReplayResult(
            fixture=fixture_name,
            decision="auth_denied",
            exit_code=EXIT_AUTH_DENIED,
            pushover_fired=False,
            pushover_mode=None,
            budget_evaluated=False,
            ledger_record=record,
        )

    # ---- Leg 1b: AUTHORITY (budget cap) ----
    projected = daily_spent + requested
    if projected > daily_cap:
        # ---- Leg 2: RECOVERY — circuit trips BEFORE the spend; page the human ----
        msg = (
            f"{task}: ${requested:.2f} would push daily spend to ${projected:.2f}, "
            f"over the ${daily_cap:.2f} cap. Blocked before the call."
        )
        print(f"[authority] BLOCK — {msg}")
        fired, mode = _page_pushover("Budget breach blocked", msg, dry=dry_pushover)
        print(f"[recovery] {ROLLBACK_HINT}")
        # ---- Leg 3: AUDIT — append the breach, append-only ----
        record = {
            **base_record,
            "projected_usd": round(projected, 4),
            "decision": "budget_breach",
            "exit_code": EXIT_BUDGET_BREACH,
            "pushover_fired": fired,
            "pushover_mode": mode,
        }
        _append_ledger(ledger_path, record)
        print(f"[audit] breach appended to {ledger_path} (exit {EXIT_BUDGET_BREACH})")
        return ReplayResult(
            fixture=fixture_name,
            decision="budget_breach",
            exit_code=EXIT_BUDGET_BREACH,
            pushover_fired=fired,
            pushover_mode=mode,
            budget_evaluated=True,
            ledger_record=record,
        )

    # ---- ALLOW path: within budget, key present ----
    record = {
        **base_record,
        "projected_usd": round(projected, 4),
        "decision": "allowed",
        "exit_code": EXIT_ALLOWED,
    }
    _append_ledger(ledger_path, record)
    print(
        f"[authority] ALLOW — {task}: ${requested:.2f} keeps daily spend at "
        f"${projected:.2f}, under the ${daily_cap:.2f} cap."
    )
    print(f"[audit] run appended to {ledger_path} (exit {EXIT_ALLOWED})")
    return ReplayResult(
        fixture=fixture_name,
        decision="allowed",
        exit_code=EXIT_ALLOWED,
        pushover_fired=False,
        pushover_mode=None,
        budget_evaluated=True,
        ledger_record=record,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay a synthetic spend request through Authority/Recovery/Audit."
    )
    parser.add_argument(
        "--fixture",
        required=True,
        choices=["allowed", "over_budget", "missing_auth"],
        help="which synthetic scenario to replay",
    )
    parser.add_argument(
        "--dry-pushover",
        action="store_true",
        help="log the page instead of hitting the Pushover API (use for rehearsal/CI)",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=None,
        help=f"ledger file to append to (default: {DEFAULT_LEDGER})",
    )
    args = parser.parse_args(argv)
    result = run(args.fixture, dry_pushover=args.dry_pushover, ledger_path=args.ledger)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
