"""JSONL ledger writer for the judge layer (Task 12, Day 5).

Turns a JudgeDecision from an in-memory return value into an observable,
append-only telemetry stream at vault/health/judge_log/<YYYY-MM-DD>.jsonl —
the surface the Fleet Observability Dashboard (Task 11) reads to plot the
judge-outcome distribution and judge-availability % panels.

Design decisions:

  - One JSON object per line. Each line round-trips both the JudgeDecision
    telemetry and the full ActionProposal (model_dump) so a downstream
    consumer can reconstruct exactly what the actor wanted to do AND what the
    judge said about it, with no schema lookup.

  - Date bucketing rolls at UTC midnight, keyed off JudgeDecision.evaluated_at
    (already UTC), NOT datetime.now(). A row written just after UTC midnight
    lands in the correct UTC-dated file even when the caller's local clock
    still reads mid-evening — so the dashboard's per-day panels never split a
    decision across the wrong file.

  - Concurrent-safe append via lib.filelock.FileLock (POSIX advisory lock).
    The vault is written by several agents at once (synthesizer, flush,
    knowledge_lint, job_feed); the exclusive lock on <dir>/.lock keeps two
    simultaneous writers from interleaving half-lines into the JSONL.

  - matched_rule_id is DERIVED from the proposal's authorization_basis, not
    carried on JudgeDecision. The judge returns an outcome + feedback /
    quarantine_reason; it does not echo which rule id fired. The actor's
    authorization_basis is the one place a rule id is referenced, so we parse
    it out of there. This is a *reference* to an existing rule, never a new
    one (the substack_drafter.yaml policy stays at exactly 4 rules).

Mirrors lib/pushover.py's exception-class shape (a base class + a specific
subclass) and reuses lib/filelock.py rather than reinventing either.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import timezone
from pathlib import Path
from typing import Optional

from lib import filelock
from lib import pushover
from lib.judge.schema import ActionProposal, JudgeDecision

logger = logging.getLogger(__name__)


# ─── Exceptions (mirror pushover.py's base-class + subclass shape) ────────────


class LedgerError(Exception):
    """Base class for any ledger error."""


class LedgerWriteError(LedgerError):
    """Raised on FileLock timeout or filesystem I/O failure.

    The caller (judge_action, or any future wrapper) decides what to do — for
    the fail-open control plane that means: log it, keep the JudgeDecision,
    and let Sean's manual review stay the canonical Tier-A control.
    """


# ─── Defaults ─────────────────────────────────────────────────────────────────

# How long to wait for the exclusive append lock before giving up. Judge
# decisions are low-frequency (one per drafted piece); 5s is generous headroom
# over the milliseconds a single-line append actually holds the lock.
_LOCK_TIMEOUT_S = 5.0

# Lock filename inside the ledger directory. Shared by every writer of this dir.
_LOCK_NAME = ".lock"

# Probe filename used by ensure_ledger_ready() to prove the dir is writable.
_WRITE_TEST_NAME = ".write-test"


def _default_ledger_dir() -> Path:
    """Resolve the canonical ledger dir: <vault_root>/health/judge_log/.

    Mirrors config.toml's [paths].vault_root. Falls back to the repo-relative
    layout if config can't load (e.g., a stripped CI environment) — tests never
    hit this path because they always pass an explicit tmp_path.
    """
    try:
        from lib.config import load_config

        return load_config().vault_root / "health" / "judge_log"
    except Exception:  # noqa: BLE001 — config load is best-effort for the default
        # agents-sdk/lib/judge/ledger.py -> parents[3] == repo root.
        return Path(__file__).resolve().parents[3] / "vault" / "health" / "judge_log"


# ─── matched_rule_id derivation ───────────────────────────────────────────────

# A rule id token as used in substack_drafter.yaml (rule_a_..., rule_d_...).
_RULE_ID_RE = re.compile(r"rule_[a-z0-9_]+")


def _derive_matched_rule_id(authorization_basis: str) -> Optional[str]:
    """Extract the referenced rule id from an ActionProposal.authorization_basis.

    authorization_basis is free text that references a policy rule. Three
    shapes are handled, most-specific first:
      1. 'substack_drafter.yaml#rule_d_publish_verb_at_top_level'
         -> the fragment after the final '#'.
      2. 'rule_a_unverifiable_claim_named_person' (bare id, or embedded in prose)
         -> the first 'rule_...' token.
      3. anything else (no rule reference) -> None.
    """
    if not authorization_basis:
        return None
    if "#" in authorization_basis:
        fragment = authorization_basis.rsplit("#", 1)[1].strip()
        if fragment:
            return fragment
    match = _RULE_ID_RE.search(authorization_basis)
    if match:
        return match.group(0)
    return None


# ─── Row construction ─────────────────────────────────────────────────────────


def _build_row(
    decision: JudgeDecision,
    proposal: ActionProposal,
    *,
    agent_name: str,
) -> dict:
    """Assemble the exact JSONL row schema the dashboard consumes.

    Keys are fixed and ordered for readability; the proposal sub-object is the
    full ActionProposal model_dump so the row is self-describing.
    """
    evaluated_at = decision.evaluated_at
    # Normalise to UTC for the stored ISO string. A naive datetime is treated
    # as already-UTC (JudgeDecision's default_factory produces aware UTC; this
    # only guards a caller that hand-built a naive one).
    if evaluated_at.tzinfo is None:
        evaluated_at = evaluated_at.replace(tzinfo=timezone.utc)
    else:
        evaluated_at = evaluated_at.astimezone(timezone.utc)

    return {
        "evaluated_at": evaluated_at.isoformat(),
        "agent_name": agent_name,
        "outcome": decision.outcome,  # str via use_enum_values=True
        "matched_rule_id": _derive_matched_rule_id(proposal.authorization_basis),
        "model_used": decision.model_used,
        "latency_ms": decision.latency_ms,
        "feedback": decision.feedback,
        "quarantine_reason": decision.quarantine_reason,
        "proposal": proposal.model_dump(mode="json"),
    }


def _bucket_filename(decision: JudgeDecision) -> str:
    """Pick the <YYYY-MM-DD>.jsonl filename from the decision's UTC date.

    Rolls at UTC midnight off evaluated_at, never local time, so a row written
    just past UTC midnight does not land in yesterday's file.
    """
    evaluated_at = decision.evaluated_at
    if evaluated_at.tzinfo is None:
        evaluated_at = evaluated_at.replace(tzinfo=timezone.utc)
    else:
        evaluated_at = evaluated_at.astimezone(timezone.utc)
    return f"{evaluated_at.strftime('%Y-%m-%d')}.jsonl"


# ─── Public API ───────────────────────────────────────────────────────────────


def write_decision(
    decision: JudgeDecision,
    proposal: ActionProposal,
    *,
    agent_name: str,
    ledger_dir: Path | None = None,
) -> Path:
    """Append one JSONL row recording a judge decision.

    Args:
        decision:    The JudgeDecision returned by judge.evaluate().
        proposal:    The ActionProposal that was evaluated (serialised in full).
        agent_name:  The actor whose action this was (e.g. 'substack_drafter').
        ledger_dir:  Override the ledger directory. Defaults to
                     <vault_root>/health/judge_log/. Tests pass a tmp_path.

    Returns:
        The absolute Path of the JSONL file the row landed in.

    Raises:
        LedgerWriteError: on FileLock timeout or any filesystem I/O failure.
    """
    target_dir = Path(ledger_dir) if ledger_dir is not None else _default_ledger_dir()
    target_file = target_dir / _bucket_filename(decision)
    lock_path = target_dir / _LOCK_NAME

    row = _build_row(decision, proposal, agent_name=agent_name)
    line = json.dumps(row, ensure_ascii=False) + "\n"

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        with filelock.FileLock(lock_path, exclusive=True, timeout=_LOCK_TIMEOUT_S):
            with open(target_file, "a", encoding="utf-8") as fh:
                fh.write(line)
    except filelock.LockTimeout as exc:
        raise LedgerWriteError(
            f"Timed out acquiring ledger lock at {lock_path}: {exc}"
        ) from exc
    except OSError as exc:
        raise LedgerWriteError(
            f"Filesystem error writing ledger row to {target_file}: {exc}"
        ) from exc

    return target_file.resolve()


def ensure_ledger_ready(ledger_dir: Path | None = None) -> None:
    """Boot-time check: the ledger dir is writable AND Pushover creds exist.

    Fail loud at agent startup rather than silent later — mirrors the v3.33.0
    Pushover boot check in vault_synthesizer.py. Called by the Day 6 wire-up
    (and any manual judge smoke-test CLI) before the first decision is made.

    Behaviour:
      1. mkdir -p the ledger dir (and parents).
      2. Prove it's writable by creating and deleting a .write-test file.
      3. Verify Pushover credentials via lib.pushover.ensure_credentials_or_raise().

    Raises:
        LedgerWriteError: if the dir can't be created or isn't writable.
        PushoverConfigurationError: re-raised directly from lib.pushover so the
            operator sees the same actionable message the synthesizer surfaces.
    """
    target_dir = Path(ledger_dir) if ledger_dir is not None else _default_ledger_dir()

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        probe = target_dir / _WRITE_TEST_NAME
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        raise LedgerWriteError(
            f"Ledger directory {target_dir} is not writable: {exc}"
        ) from exc

    # Re-raise PushoverConfigurationError directly (do not wrap) — the operator
    # gets the same message they'd see from any other agent's boot check.
    pushover.ensure_credentials_or_raise()
