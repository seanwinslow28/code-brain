"""Pydantic schemas for the judge layer.

Three types form the entire interface between an agent (the actor) and the
judge that gates its actions:

  1. ActionProposal — what the agent *intends* to do, fully typed.
  2. Outcome       — the 5-value enum the judge returns.
  3. JudgeDecision — the judge's full response (outcome + telemetry).

Designed so the dashboard (Task 11) + the JSONL ledger (Day 5) can consume
JudgeDecision objects without a parser — model_dump() round-trips cleanly.

Why Pydantic and not @dataclass: per council brief 2026-05-16, "ActionProposal"
is the load-bearing demo phrase. Pydantic gives us runtime validation, JSON
schema export (for non-Python consumers), and the field-level Optional/required
distinction without a hand-rolled __post_init__. The schema IS the artifact.

Why pydantic v2 specifically: model_validate / model_dump / ConfigDict are the
modern API. The repo already has pydantic 2.12.5 in the venv (transitively via
google-genai). Adding it as an explicit dep in pyproject.toml is a Day-3 follow-up.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Outcome(str, Enum):
    """The 5 outcomes a judge can return.

    The fifth value — JUDGE_UNAVAILABLE — is the load-bearing one. It turns
    "the judge model didn't respond" into a named, observable state. Without
    it, judge unavailability is either a silent exception (worst case — the
    actor proceeds unchecked) or a hard error (the actor's entire run aborts
    because the *judge* failed).

    We chose neither. JUDGE_UNAVAILABLE means: "I tried to evaluate, I
    couldn't reach the judge, here's a row in the ledger so you can see how
    often this happens, and I'm telling the caller to fall open." The caller
    decides what fall-open means in its own policy context — for Substack-
    Drafter, it means "write the draft, fire a Pushover ping, and let Sean's
    manual review catch what the judge would have caught." That preserves
    the Tier-A 'agents draft / Sean sends' boundary as defense-in-depth.
    """

    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REVISE = "REVISE"
    ESCALATE = "ESCALATE"
    JUDGE_UNAVAILABLE = "JUDGE_UNAVAILABLE"


class ActionProposal(BaseModel):
    """The structured proposal an actor emits *before* taking an action.

    Eight fields. Two are Optional because not every actor can produce them
    on every action:

      - evidence_used:   None when the actor's action is pure-generation
                         (e.g., a Substack draft built only from voice rules,
                         no retrieved evidence chunks). Required-feeling for
                         retrieval-grounded actions; truly None for pure ones.
      - rollback_path:   None when the action is local-only and idempotent
                         (writing a draft to disk that Sean can just delete).
                         Required for any action that touches an external
                         system or git history.

    The other six are required. Together they answer a recruiter's "what
    would your control plane intercept" question with a single struct.
    """

    model_config = ConfigDict(
        # Validate on assignment so a mid-life mutation can't sneak past
        # the schema (e.g., setting outcome on the wrapping JudgeDecision).
        validate_assignment=True,
        # Reject unknown fields so the schema is the contract — drift hits
        # in test, not in production. Council brief: "the schema IS the
        # contract." A typo on intended_actoin shouldn't silently work.
        extra="forbid",
        # Preserve enum string values on dump (Outcome.ALLOW → "ALLOW",
        # not {"_name_": "ALLOW", "_value_": "ALLOW"}). The JSONL ledger
        # consumer (Task 11 dashboard) reads strings.
        use_enum_values=True,
    )

    intended_action: str = Field(
        ...,
        min_length=1,
        description=(
            "What the actor wants to do, in one verb phrase. "
            "Examples: 'write_substack_draft', 'send_pushover_ping', "
            "'commit_to_vault'."
        ),
    )

    target_surface: str = Field(
        ...,
        min_length=1,
        description=(
            "Where the action will land. A path, a service name, or a "
            "named resource. Examples: 'vault/.../substack-drafts/foo.md', "
            "'pushover://com.sean.agents.pushover_api_token', 'git://origin/main'."
        ),
    )

    evidence_used: Optional[list[str]] = Field(
        default=None,
        description=(
            "Provenance for any factual claims the actor is making. "
            "Each entry is a stable identifier: a chunk_id, a vault path "
            "with line range, a URL. None ONLY when the action makes no "
            "factual claims requiring evidence (e.g., pure-generation drafts)."
        ),
    )

    authorization_basis: str = Field(
        ...,
        min_length=1,
        description=(
            "The policy clause that permits this action. Free-text reference "
            "to a rule in the active YAML policy. Example: "
            "'substack_drafter.yaml#rule_d_publish_verb_only_via_sean'."
        ),
    )

    expected_consequence: str = Field(
        ...,
        min_length=1,
        description=(
            "What the actor expects to happen after the action lands. "
            "Used by the judge to detect overreach (the action's stated "
            "consequence should match what the policy permits)."
        ),
    )

    rollback_path: Optional[str] = Field(
        default=None,
        description=(
            "How to undo the action if the consequence turns out wrong. "
            "A shell command, a file path to delete, or a named procedure. "
            "None ONLY when the action is local-only and idempotent."
        ),
    )

    exposure_level: str = Field(
        ...,
        min_length=1,
        description=(
            "Blast radius classifier. One of: 'local-only' (just this "
            "machine's filesystem), 'org-internal' (vault, private agents), "
            "'external-readonly' (LinkedIn impression, no write), "
            "'external-write' (publishing, sending email, executing trades). "
            "Free-text for now; future v0.2 can promote to enum."
        ),
    )

    human_review_required: bool = Field(
        ...,
        description=(
            "Whether the action MUST hit a human before it lands, regardless "
            "of the judge's verdict. True for any action whose blast radius "
            "exceeds the actor's authorization, even when the policy would "
            "otherwise ALLOW. Substack-Drafter sets True on any publish-verb "
            "action — judge agrees AND Sean still has to send."
        ),
    )


class JudgeDecision(BaseModel):
    """The judge's full response to an ActionProposal.

    Wraps an Outcome plus telemetry the dashboard + ledger consume:
      - feedback         — populated on REVISE. The text the actor retries with.
      - quarantine_reason — populated on ESCALATE. What made this escalate-worthy.
      - model_used       — which judge model evaluated. Telemetry for the
                           judge-availability % panel.
      - latency_ms       — how long the judge took. Telemetry for the dashboard.
      - evaluated_at     — UTC timestamp. The ledger sorts on this field.

    Round-trips cleanly through model_dump() for JSONL ledger writes. The
    Outcome enum dumps as its string value (use_enum_values=True), so the
    ledger row reads like:
      {"outcome": "ALLOW", "model_used": "gemma4:e4b", "latency_ms": 412, ...}
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        use_enum_values=True,
    )

    outcome: Outcome = Field(
        ...,
        description="One of the 5 Outcome enum values.",
    )

    feedback: Optional[str] = Field(
        default=None,
        description=(
            "Required when outcome=REVISE. The string the actor appends to "
            "its prompt on retry. None for ALLOW/BLOCK/ESCALATE/JUDGE_UNAVAILABLE."
        ),
    )

    quarantine_reason: Optional[str] = Field(
        default=None,
        description=(
            "Required when outcome=ESCALATE. The reason the action was kicked "
            "to the quarantine subfolder for Sean to review. None otherwise."
        ),
    )

    model_used: str = Field(
        ...,
        min_length=1,
        description=(
            "Identifier of the judge model. Example: 'gemma4:e4b'. "
            "On JUDGE_UNAVAILABLE this carries the model that was *attempted* "
            "so the dashboard can plot per-model availability."
        ),
    )

    latency_ms: int = Field(
        ...,
        ge=0,
        description=(
            "Total wall-clock time the judge spent evaluating, in milliseconds. "
            "Includes router resolution, prompt build, model call, parse. "
            "0 is legal (e.g., a synthetic test).",
        ),
    )

    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description=(
            "UTC timestamp of the evaluation. Default is now; tests can set "
            "explicitly. The JSONL ledger writer at lib/judge/ledger.py (Day 5) "
            "uses this field to bucket rows into daily files."
        ),
    )
