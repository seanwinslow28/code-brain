"""Tests for lib.judge.judge.evaluate() — the control-plane heartbeat.

Mock seam: lib.judge.judge._call_router is the only HTTP boundary; tests
monkeypatch it directly so we never need a live Mac Mini + Ollama running.
This matches the substack-drafter test pattern.

Coverage:
  - All 4 model-emittable outcomes round-trip cleanly.
  - JUDGE_UNAVAILABLE fires on: transport error, unexpected exception,
    parse failure past retries.
  - Parse retries actually retry, with the parse error included in the
    retry prompt's user_text (so the model can self-correct).
  - latency_ms is populated and monotonically non-zero.
  - attempted_model is recorded on the decision (for dashboard per-model
    availability panels).
  - The system prompt enumerates all policy rules + the output contract.
  - evaluate() never raises — fail-open is the contract.
"""

from __future__ import annotations

from typing import Any

import pytest

from lib.judge import judge as judge_module
from lib.judge.judge import (
    JudgeTransportError,
    _build_system_prompt,
    _build_user_prompt,
    _parse_judge_output,
    JudgeParseError,
    evaluate,
)
from lib.judge.policy import Policy, Rule
from lib.judge.schema import ActionProposal, JudgeDecision, Outcome


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_proposal() -> ActionProposal:
    """A canonical valid ActionProposal for tests that need any proposal."""
    return ActionProposal(
        intended_action="write_substack_draft",
        target_surface="vault/.../substack-drafts/2026-06-19-test.md",
        evidence_used=["chunk_id:abc123"],
        authorization_basis="substack_drafter.yaml#rule_b_block_attribution",
        expected_consequence="A local markdown draft file lands.",
        rollback_path="rm vault/.../substack-drafts/2026-06-19-test.md",
        exposure_level="local-only",
        human_review_required=True,
    )


@pytest.fixture
def sample_policy() -> Policy:
    """A minimal valid Policy with one rule of each model-emittable outcome."""
    return Policy(
        name="Test Policy",
        agent="test_agent",
        version="0.1.0",
        rules=[
            Rule(
                id="rule_revise",
                condition="The draft has a voice drift.",
                outcome=Outcome.REVISE,
                feedback_template="Re-render in the assigned voice.",
            ),
            Rule(
                id="rule_escalate",
                condition="The draft contains PII.",
                outcome=Outcome.ESCALATE,
                quarantine_reason="PII detected.",
            ),
            Rule(
                id="rule_block",
                condition="The draft contains a publish verb.",
                outcome=Outcome.BLOCK,
            ),
        ],
        fallback_outcome=Outcome.ALLOW,
    )


class _RouterStub:
    """Stub for monkeypatching _call_router.

    Tracks call count + the user prompts seen across attempts so retry tests
    can assert the parse error was actually included in the retry prompt.
    """

    def __init__(self, responses: list[Any], model_name: str = "gemma4:e4b") -> None:
        """Args:
            responses: list of items returned per call, in order. Each item
                is either:
                  - a str (the raw model output), or
                  - an Exception instance (raised when this call fires).
            model_name: the model_used value returned on successful calls.
        """
        self.responses = list(responses)
        self.model_name = model_name
        self.call_count = 0
        self.user_prompts_seen: list[str] = []
        self.system_prompts_seen: list[str] = []
        self.timeouts_seen: list[float] = []

    def __call__(self, *, task: str, system: str, user: str, timeout_s: float) -> tuple[str, str]:
        self.call_count += 1
        self.user_prompts_seen.append(user)
        self.system_prompts_seen.append(system)
        self.timeouts_seen.append(timeout_s)
        if not self.responses:
            raise AssertionError(
                f"_RouterStub ran out of responses on call {self.call_count}; "
                f"test passed fewer responses than evaluate() consumed."
            )
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item, self.model_name


def _install_router_stub(monkeypatch: pytest.MonkeyPatch, stub: _RouterStub) -> None:
    """Monkeypatch _call_router in the judge module to use the stub."""
    monkeypatch.setattr(judge_module, "_call_router", stub)


# ─── All 4 model-emittable outcomes ──────────────────────────────────────────


class TestModelEmittableOutcomes:
    def test_allow_outcome(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "ALLOW"
        assert decision.feedback is None
        assert decision.quarantine_reason is None
        assert decision.model_used == "gemma4:e4b"
        assert decision.latency_ms >= 0
        assert stub.call_count == 1

    def test_block_outcome(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "BLOCK", "matched_rule_id": "rule_block", "feedback": null, "quarantine_reason": null}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "BLOCK"
        assert decision.feedback is None

    def test_revise_outcome_with_feedback(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "REVISE", "matched_rule_id": "rule_revise", '
            '"feedback": "Re-render in Sedaris voice.", "quarantine_reason": null}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "REVISE"
        assert decision.feedback == "Re-render in Sedaris voice."

    def test_escalate_outcome_with_quarantine_reason(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "ESCALATE", "matched_rule_id": "rule_escalate", '
            '"feedback": null, "quarantine_reason": "Unverifiable quote."}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "ESCALATE"
        assert decision.quarantine_reason == "Unverifiable quote."


# ─── Fail-open paths → JUDGE_UNAVAILABLE ─────────────────────────────────────


class TestJudgeUnavailablePaths:
    def test_transport_error_returns_unavailable(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([JudgeTransportError("Mac Mini Ollama unreachable")])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        # Default attempted model when transport failed before resolution
        assert decision.model_used == "gemma4:e4b"
        assert decision.latency_ms >= 0

    def test_unexpected_exception_returns_unavailable(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """Even a non-JudgeTransportError exception → JUDGE_UNAVAILABLE,
        not a propagated raise. evaluate() never lets exceptions out."""
        stub = _RouterStub([RuntimeError("unexpected disk-full")])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "JUDGE_UNAVAILABLE"

    def test_parse_failure_past_retries_returns_unavailable(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """The model emits garbage on all retries → JUDGE_UNAVAILABLE."""
        # Pass max_parse_retries + 1 garbage responses (the function tries
        # initial + max_parse_retries retries, so 4 total at default=3).
        stub = _RouterStub(
            [
                "I have decided this is fine.",  # initial
                "Looks good to me.",  # retry 1
                "Yep, allow it.",  # retry 2
                "Sure, ALLOW.",  # retry 3
            ]
        )
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        # All 4 attempts (1 initial + 3 retries) consumed
        assert stub.call_count == 4

    def test_evaluate_never_raises_on_arbitrary_failure(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """Even if the stub itself raises ValueError, evaluate() returns
        JUDGE_UNAVAILABLE rather than propagating. Defense-in-depth pin."""
        stub = _RouterStub([ValueError("contrived")])
        _install_router_stub(monkeypatch, stub)
        # Should not raise
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "JUDGE_UNAVAILABLE"


# ─── Parse-retry path (model self-correction) ─────────────────────────────────


class TestParseRetry:
    def test_retry_succeeds_after_initial_garbage(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """First call returns garbage, second call returns valid JSON.
        evaluate() succeeds on the retry."""
        stub = _RouterStub(
            [
                "Sorry, I can't return JSON.",  # initial garbage
                '{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}',  # retry succeeds
            ]
        )
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "ALLOW"
        assert stub.call_count == 2

    def test_retry_prompt_includes_parse_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """The retry prompt must contain the parse error from the prior
        attempt — that's how the model self-corrects. Pin it."""
        stub = _RouterStub(
            [
                "Not JSON at all.",  # initial — parse fails
                '{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}',
            ]
        )
        _install_router_stub(monkeypatch, stub)
        evaluate(sample_proposal, sample_policy)
        # Second user prompt should contain the parse-error retry context
        retry_user = stub.user_prompts_seen[1]
        assert "previous response failed to parse" in retry_user.lower()
        assert "json" in retry_user.lower()

    def test_max_parse_retries_respected(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """When max_parse_retries=1, we get 2 total attempts (initial + 1)."""
        stub = _RouterStub(
            [
                "garbage 1",
                "garbage 2",
                # A third would crash AssertionError — but we shouldn't get there
            ]
        )
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy, max_parse_retries=1)
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        assert stub.call_count == 2

    def test_revise_without_feedback_treated_as_parse_failure(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """Cross-field check: outcome=REVISE without feedback is invalid.
        The parser raises JudgeParseError; the retry path kicks in."""
        stub = _RouterStub(
            [
                # Initial response: REVISE but no feedback (contract violation)
                '{"outcome": "REVISE", "matched_rule_id": "rule_revise", "feedback": null, "quarantine_reason": null}',
                # Retry: properly populated
                '{"outcome": "REVISE", "matched_rule_id": "rule_revise", "feedback": "Re-render properly.", "quarantine_reason": null}',
            ]
        )
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.outcome == "REVISE"
        assert decision.feedback == "Re-render properly."
        assert stub.call_count == 2


# ─── Prompt-shape regression tests ───────────────────────────────────────────


class TestPromptBuilders:
    def test_system_prompt_includes_all_policy_rules(
        self, sample_policy: Policy
    ) -> None:
        system = _build_system_prompt(sample_policy)
        for rule in sample_policy.rules:
            assert rule.id in system, f"Rule {rule.id} missing from system prompt"

    def test_system_prompt_states_json_contract(self, sample_policy: Policy) -> None:
        """The model must be told to emit JSON, not prose. Pin the contract."""
        system = _build_system_prompt(sample_policy)
        assert "JSON" in system
        # Must enumerate all 4 model-emittable outcomes for unambiguous parsing
        assert "ALLOW" in system
        assert "BLOCK" in system
        assert "REVISE" in system
        assert "ESCALATE" in system
        # JUDGE_UNAVAILABLE is set by evaluate(), not the model — must NOT
        # appear in the model's emittable set in the prompt
        assert "JUDGE_UNAVAILABLE" not in system.split("OUTPUT CONTRACT")[1]

    def test_user_prompt_carries_all_eight_proposal_fields(
        self, sample_proposal: ActionProposal
    ) -> None:
        user = _build_user_prompt(sample_proposal)
        # All 8 ActionProposal field names must appear in the rendered prompt
        for field_name in [
            "intended_action",
            "target_surface",
            "evidence_used",
            "authorization_basis",
            "expected_consequence",
            "rollback_path",
            "exposure_level",
            "human_review_required",
        ]:
            assert field_name in user, f"Field {field_name} missing from user prompt"


# ─── Output parser unit tests (the JSON extractor) ───────────────────────────


class TestParseJudgeOutput:
    def test_clean_json_parses(self) -> None:
        raw = '{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}'
        parsed = _parse_judge_output(raw)
        assert parsed["outcome"] == "ALLOW"

    def test_json_with_prose_preamble_parses(self) -> None:
        """gemma4:e4b sometimes wraps JSON in a prose preamble. Extract anyway."""
        raw = (
            'Here is my verdict:\n'
            '{"outcome": "BLOCK", "matched_rule_id": "rule_block", '
            '"feedback": null, "quarantine_reason": null}'
        )
        parsed = _parse_judge_output(raw)
        assert parsed["outcome"] == "BLOCK"

    def test_no_json_raises_parse_error(self) -> None:
        with pytest.raises(JudgeParseError) as exc_info:
            _parse_judge_output("Just prose, no JSON object here.")
        assert "no json" in str(exc_info.value).lower()

    def test_missing_outcome_key_raises(self) -> None:
        with pytest.raises(JudgeParseError) as exc_info:
            _parse_judge_output('{"matched_rule_id": "x"}')
        assert "outcome" in str(exc_info.value).lower()

    def test_invalid_outcome_string_raises(self) -> None:
        with pytest.raises(JudgeParseError) as exc_info:
            _parse_judge_output('{"outcome": "MAYBE", "feedback": null}')
        assert "maybe" in str(exc_info.value).lower()

    def test_judge_unavailable_not_emittable_by_model(self) -> None:
        """JUDGE_UNAVAILABLE is set by evaluate() only. If the model tries
        to emit it (e.g., hallucinated copy of the system prompt), reject."""
        with pytest.raises(JudgeParseError) as exc_info:
            _parse_judge_output('{"outcome": "JUDGE_UNAVAILABLE", "feedback": null}')
        # Should fail because JUDGE_UNAVAILABLE is not in the emittable set
        assert "JUDGE_UNAVAILABLE" not in {
            o.value for o in [Outcome.ALLOW, Outcome.BLOCK, Outcome.REVISE, Outcome.ESCALATE]
        }
        assert "judge_unavailable" in str(exc_info.value).lower()


# ─── Latency + model attribution checks ──────────────────────────────────────


class TestLatencyAndModelAttribution:
    def test_latency_ms_populated(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        # latency_ms is an int and >= 0 (could legitimately be 0 if the stub
        # returns within the millisecond bucket).
        assert isinstance(decision.latency_ms, int)
        assert decision.latency_ms >= 0

    def test_attempted_model_recorded_on_unavailable(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """JUDGE_UNAVAILABLE rows must carry the attempted model so the
        dashboard's per-model availability % panel works."""
        stub = _RouterStub([JudgeTransportError("down")])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.model_used == "gemma4:e4b"

    def test_actual_model_recorded_on_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        """On success, model_used is whatever the router returned (not the
        default). Pin that the router-returned value wins over the fallback."""
        stub = _RouterStub(
            ['{"outcome": "ALLOW", "matched_rule_id": null, "feedback": null, "quarantine_reason": null}'],
            model_name="phi4-mini",  # different from default, e.g. an API fallback
        )
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        assert decision.model_used == "phi4-mini"


# ─── Round-trip: JudgeDecision is JSONL-ready ───────────────────────────────


class TestJudgeDecisionIsLedgerReady:
    """The output of evaluate() must be JSONL-writable (Day 5 ledger writer).
    Round-trip checks here insulate Day 5 from any schema regression."""

    def test_decision_dumps_to_dict_cleanly(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([
            '{"outcome": "REVISE", "matched_rule_id": "rule_revise", '
            '"feedback": "Fix voice.", "quarantine_reason": null}'
        ])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        # model_dump() must work and outcome must serialize as a string
        # (use_enum_values=True), not a nested enum dict.
        dumped = decision.model_dump()
        assert dumped["outcome"] == "REVISE"
        assert not isinstance(dumped["outcome"], dict)
        # All four telemetry fields present for the dashboard's panels
        assert "model_used" in dumped
        assert "latency_ms" in dumped
        assert "evaluated_at" in dumped
        assert "feedback" in dumped

    def test_decision_dumps_to_json_cleanly(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([JudgeTransportError("down")])
        _install_router_stub(monkeypatch, stub)
        decision = evaluate(sample_proposal, sample_policy)
        # model_dump_json() must round-trip via model_validate_json()
        as_json = decision.model_dump_json()
        rehydrated = JudgeDecision.model_validate_json(as_json)
        assert rehydrated == decision
        assert rehydrated.outcome == "JUDGE_UNAVAILABLE"
