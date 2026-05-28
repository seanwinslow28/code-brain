"""judge_action() — the effectful wrapper around the pure evaluate().

Option B (locked 2026-05-28 by Sean): judge.evaluate() stays a pure function —
no filesystem, no network, fully unit-tested by the Day 1-3 suite. This module
is the thin effects layer the rest of agents-sdk expects: pure logic plus a
wrapper that does the I/O.

judge_action():
  1. calls evaluate() to get a JudgeDecision,
  2. writes that decision to the JSONL ledger (Day 5 telemetry stream),
  3. fires a best-effort Pushover alert on JUDGE_UNAVAILABLE,
  4. returns the JudgeDecision unchanged.

It NEVER raises. evaluate() already guarantees never-raises; this wrapper takes
over that contract for the I/O it adds — a ledger-write failure or a Pushover
send failure is logged, never propagated. The caller (Day 6's substack_drafter
wire-up) always gets a JudgeDecision back and falls open to Sean's manual
review when the outcome is JUDGE_UNAVAILABLE. That preserves the Tier-A
'agents draft / Sean sends' boundary as defense-in-depth.

A note on the Pushover message under Option B: evaluate() swallows the raw
model / transport error text to the logger and returns only the JudgeDecision
(JudgeDecision is frozen — it carries no error field). So this wrapper cannot
put the raw failure tail into the alert; it sends the actionable identifiers it
does have (agent_name, attempted model, latency) and points the operator at the
agent logs for the detail. That was the accepted trade-off of keeping
evaluate() pure.
"""

from __future__ import annotations

import logging

from lib import pushover
from lib.judge import ledger
from lib.judge.judge import evaluate
from lib.judge.policy import Policy
from lib.judge.schema import ActionProposal, JudgeDecision, Outcome

logger = logging.getLogger(__name__)

# Pushover priority for the JUDGE_UNAVAILABLE warning. 0 == low-priority
# "warning" per the Day 5 spec (not -1 silent, not 1 high — the judge being
# down is a warning, not a page; Sean's manual gate still catches everything).
_JUDGE_UNAVAILABLE_PRIORITY = 0
_PUSHOVER_TITLE = "Judge layer unavailable"


def judge_action(
    proposal: ActionProposal,
    policy: Policy,
    *,
    agent_name: str,
    ledger_dir=None,
) -> JudgeDecision:
    """Evaluate a proposal, record it to the ledger, alert on JUDGE_UNAVAILABLE.

    Args:
        proposal:    The actor's typed proposal.
        policy:      The loaded policy gating the actor.
        agent_name:  The actor's name, recorded in the ledger row.
        ledger_dir:  Override the ledger directory (tests pass tmp_path).
                     Defaults to <vault_root>/health/judge_log/.

    Returns:
        The JudgeDecision from evaluate(), unchanged. Never raises.
    """
    decision = evaluate(proposal, policy)

    # (1) Ledger: every outcome lands a row. A write failure is logged, never
    # raised — fail-open keeps the decision flowing to the caller.
    try:
        ledger.write_decision(
            decision,
            proposal,
            agent_name=agent_name,
            ledger_dir=ledger_dir,
        )
    except ledger.LedgerError as exc:
        logger.error(
            "judge_action: ledger write failed for agent=%s outcome=%s: %s",
            agent_name,
            decision.outcome,
            exc,
        )

    # (2) Pushover: only on JUDGE_UNAVAILABLE, best-effort, severity 0.
    if decision.outcome == Outcome.JUDGE_UNAVAILABLE.value:
        _alert_judge_unavailable(decision, agent_name=agent_name)

    return decision


def _alert_judge_unavailable(decision: JudgeDecision, *, agent_name: str) -> None:
    """Fire a best-effort low-priority Pushover ping. Logs on failure, never raises."""
    message = (
        f"agent={agent_name} model={decision.model_used} "
        f"latency={decision.latency_ms}ms — judge fell open to manual review. "
        f"See agent logs for the failure detail."
    )
    try:
        pushover.send_push(
            title=_PUSHOVER_TITLE,
            message=message,
            priority=_JUDGE_UNAVAILABLE_PRIORITY,
        )
    except pushover.PushoverError as exc:
        logger.error(
            "judge_action: Pushover JUDGE_UNAVAILABLE alert failed (agent=%s): %s",
            agent_name,
            exc,
        )
