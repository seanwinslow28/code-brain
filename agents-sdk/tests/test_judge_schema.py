"""Tests for lib.judge.schema — Pydantic ActionProposal + JudgeDecision + Outcome.

These tests pin three contracts the rest of the judge layer + the dashboard
depend on:

  1. The eight required/optional split on ActionProposal — anyone who mutates
     this schema in the future has to update these tests, which forces a
     conversation about whether the new shape preserves the ledger consumer.

  2. The Outcome enum has exactly 5 values, including JUDGE_UNAVAILABLE. If a
     PR adds a 6th outcome without updating the dashboard's panel logic
     (Task 11), CI catches it here.

  3. JudgeDecision round-trips cleanly through model_dump() / model_validate()
     so the JSONL ledger writer (Day 5) can persist + replay rows without a
     custom (de)serializer.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from lib.judge.schema import (
    ActionProposal,
    JudgeDecision,
    Outcome,
)


# A canonical, fully-populated proposal used as a base for many tests.
# Modifying this dict in test bodies is fine; the original survives across
# tests because each test gets a fresh copy via dict() or **kwargs.
_VALID_PROPOSAL: dict = {
    "intended_action": "write_substack_draft",
    "target_surface": "vault/.../substack-drafts/2026-06-19-test.md",
    "evidence_used": ["chunk_id:abc123", "vault/40_knowledge/concepts/foo.md#L42"],
    "authorization_basis": (
        "substack_drafter.yaml#rule_b_block_attribution_requires_citation"
    ),
    "expected_consequence": (
        "A markdown draft file lands locally. No network IO."
    ),
    "rollback_path": "rm vault/.../substack-drafts/2026-06-19-test.md",
    "exposure_level": "local-only",
    "human_review_required": True,
}


class TestOutcomeEnum:
    def test_has_exactly_five_values(self) -> None:
        """The 5-value contract is what makes JUDGE_UNAVAILABLE observable
        instead of silent. If this test fails because someone added a 6th
        value, update the Task 11 dashboard panels and the policy YAML
        loader's fallback_outcome validator at the same PR."""
        assert len(list(Outcome)) == 5

    def test_named_outcomes_present(self) -> None:
        """Each value spelled exactly as the dashboard / ledger consumer reads
        it. Lowercase or punctuation changes would silently break the panels."""
        assert Outcome.ALLOW.value == "ALLOW"
        assert Outcome.BLOCK.value == "BLOCK"
        assert Outcome.REVISE.value == "REVISE"
        assert Outcome.ESCALATE.value == "ESCALATE"
        assert Outcome.JUDGE_UNAVAILABLE.value == "JUDGE_UNAVAILABLE"

    def test_outcome_is_str_subclass(self) -> None:
        """Inheriting from str lets the JSONL ledger write outcome=ALLOW
        without a custom encoder. Verify the contract; the ledger writer
        depends on this."""
        assert isinstance(Outcome.ALLOW, str)
        # And json-serializable directly via use_enum_values=True on the
        # wrapping JudgeDecision (covered in TestJudgeDecisionSerialization).


class TestActionProposalRequiredFields:
    def test_full_valid_proposal_constructs(self) -> None:
        """Baseline: a fully-populated proposal validates and round-trips."""
        proposal = ActionProposal(**_VALID_PROPOSAL)
        assert proposal.intended_action == "write_substack_draft"
        assert proposal.human_review_required is True

    @pytest.mark.parametrize(
        "missing_field",
        [
            "intended_action",
            "target_surface",
            "authorization_basis",
            "expected_consequence",
            "exposure_level",
            "human_review_required",
        ],
    )
    def test_missing_required_field_raises(self, missing_field: str) -> None:
        """Each of the six required fields must raise ValidationError if absent.
        evidence_used and rollback_path are Optional — they get their own test."""
        data = dict(_VALID_PROPOSAL)
        del data[missing_field]
        with pytest.raises(ValidationError) as exc_info:
            ActionProposal(**data)
        # Pydantic v2 emits errors keyed by field path; assert the missing
        # field appears in at least one error.
        errors = exc_info.value.errors()
        assert any(missing_field in str(err.get("loc", ())) for err in errors), (
            f"Expected {missing_field} in error locations: "
            f"{[err.get('loc') for err in errors]}"
        )

    def test_empty_string_required_field_rejected(self) -> None:
        """Empty strings on required fields are caught by min_length=1.
        A blank intended_action would silently look "set" to a sloppy consumer."""
        data = dict(_VALID_PROPOSAL)
        data["intended_action"] = ""
        with pytest.raises(ValidationError):
            ActionProposal(**data)


class TestActionProposalOptionalFields:
    def test_evidence_used_optional(self) -> None:
        """Pure-generation actions can omit evidence_used."""
        data = dict(_VALID_PROPOSAL)
        data["evidence_used"] = None
        proposal = ActionProposal(**data)
        assert proposal.evidence_used is None

    def test_rollback_path_optional(self) -> None:
        """Local-only idempotent actions can omit rollback_path."""
        data = dict(_VALID_PROPOSAL)
        data["rollback_path"] = None
        proposal = ActionProposal(**data)
        assert proposal.rollback_path is None

    def test_both_optionals_absent_still_valid(self) -> None:
        """A pure-gen, local-only action populates neither optional."""
        data = dict(_VALID_PROPOSAL)
        data["evidence_used"] = None
        data["rollback_path"] = None
        proposal = ActionProposal(**data)
        assert proposal.evidence_used is None
        assert proposal.rollback_path is None


class TestActionProposalExtraForbidden:
    def test_unknown_field_rejected(self) -> None:
        """extra='forbid' makes the schema the contract. A typo on
        intended_actoin shouldn't silently pass; it should hit ValidationError
        and surface in test or at runtime, NOT silently drop the value."""
        data = dict(_VALID_PROPOSAL)
        data["intended_actoin"] = "this_is_a_typo"  # typo
        with pytest.raises(ValidationError) as exc_info:
            ActionProposal(**data)
        errors = exc_info.value.errors()
        # Pydantic v2 reports extra-forbidden with type 'extra_forbidden'
        assert any("extra_forbidden" == err.get("type") for err in errors), (
            f"Expected extra_forbidden error type, got: "
            f"{[err.get('type') for err in errors]}"
        )


class TestActionProposalRoundTrip:
    def test_model_dump_then_validate_preserves_fields(self) -> None:
        """The ledger (Day 5) and the dashboard (Task 11) both read rows
        through model_validate(model_dump_json()). This pins that path."""
        original = ActionProposal(**_VALID_PROPOSAL)
        dumped = original.model_dump()
        rehydrated = ActionProposal.model_validate(dumped)
        assert rehydrated == original

    def test_model_dump_json_round_trip(self) -> None:
        """JSONL ledger writes a single line per row. Round-tripping via
        JSON preserves every field, including the optional ones being None."""
        data = dict(_VALID_PROPOSAL)
        data["evidence_used"] = None
        original = ActionProposal(**data)
        as_json = original.model_dump_json()
        rehydrated = ActionProposal.model_validate_json(as_json)
        assert rehydrated == original
        assert rehydrated.evidence_used is None


class TestJudgeDecision:
    def test_allow_outcome_minimal_construct(self) -> None:
        """An ALLOW decision needs only outcome + model_used + latency_ms."""
        decision = JudgeDecision(
            outcome=Outcome.ALLOW,
            model_used="gemma4:e4b",
            latency_ms=412,
        )
        # use_enum_values=True dumps the value as the string, so equality
        # in this test compares against the .value, which is what the ledger
        # consumer will see.
        assert decision.outcome == "ALLOW"
        assert decision.feedback is None
        assert decision.quarantine_reason is None
        assert isinstance(decision.evaluated_at, datetime)
        # evaluated_at defaults to UTC now via default_factory
        assert decision.evaluated_at.tzinfo == timezone.utc

    def test_revise_outcome_with_feedback(self) -> None:
        """REVISE decisions carry the feedback string the actor retries with."""
        decision = JudgeDecision(
            outcome=Outcome.REVISE,
            feedback="Add [citation needed] before the Block-attributable claim.",
            model_used="gemma4:e4b",
            latency_ms=618,
        )
        assert decision.outcome == "REVISE"
        assert "citation needed" in decision.feedback

    def test_escalate_outcome_with_quarantine_reason(self) -> None:
        """ESCALATE decisions name why this got kicked to quarantine."""
        decision = JudgeDecision(
            outcome=Outcome.ESCALATE,
            quarantine_reason=(
                "Draft attributes a quote to a named-but-unverifiable figure."
            ),
            model_used="gemma4:e4b",
            latency_ms=702,
        )
        assert decision.outcome == "ESCALATE"
        assert "unverifiable" in decision.quarantine_reason

    def test_judge_unavailable_carries_attempted_model(self) -> None:
        """On JUDGE_UNAVAILABLE, model_used still names which model was
        TRIED. The dashboard's per-model availability % panel needs this."""
        decision = JudgeDecision(
            outcome=Outcome.JUDGE_UNAVAILABLE,
            model_used="gemma4:e4b",
            latency_ms=10000,  # the full timeout window
        )
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        assert decision.model_used == "gemma4:e4b"

    def test_latency_ms_must_be_non_negative(self) -> None:
        """ge=0 catches anyone who passes a signed-int diff that went negative."""
        with pytest.raises(ValidationError):
            JudgeDecision(
                outcome=Outcome.ALLOW,
                model_used="gemma4:e4b",
                latency_ms=-1,
            )


class TestJudgeDecisionSerialization:
    """The dashboard (Task 11) + the JSONL ledger (Day 5) both read JudgeDecision
    rows. These tests pin the round-trip so a future schema change can't silently
    break either consumer."""

    def test_outcome_enum_dumps_as_string(self) -> None:
        """use_enum_values=True means a ledger row has outcome:'ALLOW', not
        outcome:{'_name_':'ALLOW',...}. The Task 11 panel keys on the string."""
        decision = JudgeDecision(
            outcome=Outcome.BLOCK,
            model_used="gemma4:e4b",
            latency_ms=300,
        )
        dumped = decision.model_dump()
        assert dumped["outcome"] == "BLOCK"
        # And specifically NOT the nested-dict shape:
        assert not isinstance(dumped["outcome"], dict)

    def test_evaluated_at_serializes_iso(self) -> None:
        """JSON round-trip preserves the UTC timestamp."""
        fixed_ts = datetime(2026, 5, 28, 14, 30, 0, tzinfo=timezone.utc)
        decision = JudgeDecision(
            outcome=Outcome.ALLOW,
            model_used="gemma4:e4b",
            latency_ms=412,
            evaluated_at=fixed_ts,
        )
        as_json = decision.model_dump_json()
        rehydrated = JudgeDecision.model_validate_json(as_json)
        assert rehydrated.evaluated_at == fixed_ts

    def test_full_round_trip_revise(self) -> None:
        """A REVISE decision with feedback round-trips identically."""
        original = JudgeDecision(
            outcome=Outcome.REVISE,
            feedback="Cite the JD URL inline.",
            model_used="gemma4:e4b",
            latency_ms=525,
        )
        as_json = original.model_dump_json()
        rehydrated = JudgeDecision.model_validate_json(as_json)
        assert rehydrated == original

    def test_full_round_trip_judge_unavailable(self) -> None:
        """The JUDGE_UNAVAILABLE row is the one the dashboard plots availability
        from. Pin that it survives the JSONL round-trip with model_used preserved."""
        original = JudgeDecision(
            outcome=Outcome.JUDGE_UNAVAILABLE,
            model_used="gemma4:e4b",
            latency_ms=10000,
        )
        as_json = original.model_dump_json()
        rehydrated = JudgeDecision.model_validate_json(as_json)
        assert rehydrated == original
        assert rehydrated.outcome == "JUDGE_UNAVAILABLE"
