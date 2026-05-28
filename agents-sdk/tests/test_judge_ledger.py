"""Tests for lib.judge.ledger + lib.judge.action (Task 12, Day 5).

Two surfaces under test:
  - ledger.write_decision / ensure_ledger_ready — the JSONL telemetry writer
    and the boot-time readiness check.
  - action.judge_action — the Option-B effectful wrapper that calls the pure
    evaluate(), writes the ledger, and alerts on JUDGE_UNAVAILABLE.

Mock seams:
  - lib.judge.judge._call_router is the only HTTP boundary in evaluate();
    integration tests monkeypatch it directly (same pattern as
    test_judge_evaluate.py) so no live Mac Mini + Ollama is needed.
  - lib.pushover.send_push is spied so no real push fires.
  - lib.pushover.get_credential is neutralised for the boot-check creds test
    so the result is deterministic on a real Mac (with keychain) AND in CI.

ALL tests use tmp_path for ledger_dir. None touch the real vault/health/.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from lib import filelock, pushover
from lib.judge import action as action_module
from lib.judge import judge as judge_module
from lib.judge import ledger
from lib.judge.action import judge_action
from lib.judge.judge import JudgeTransportError
from lib.judge.ledger import (
    LedgerError,
    LedgerWriteError,
    ensure_ledger_ready,
    write_decision,
)
from lib.judge.policy import Policy, Rule
from lib.judge.schema import ActionProposal, JudgeDecision, Outcome


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_proposal() -> ActionProposal:
    return ActionProposal(
        intended_action="write_substack_draft",
        target_surface="vault/.../substack-drafts/2026-06-19-test.md",
        evidence_used=["chunk_id:abc123"],
        authorization_basis="substack_drafter.yaml#rule_d_publish_verb_at_top_level",
        expected_consequence="A local markdown draft file lands.",
        rollback_path="rm vault/.../substack-drafts/2026-06-19-test.md",
        exposure_level="local-only",
        human_review_required=True,
    )


@pytest.fixture
def allow_decision() -> JudgeDecision:
    return JudgeDecision(
        outcome=Outcome.ALLOW,
        feedback=None,
        quarantine_reason=None,
        model_used="gemma4:e4b",
        latency_ms=412,
        evaluated_at=datetime(2026, 5, 28, 12, 0, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def sample_policy() -> Policy:
    return Policy(
        name="Test Policy",
        agent="substack_drafter",
        version="0.1.0",
        rules=[
            Rule(
                id="rule_block",
                condition="The draft contains a publish verb.",
                outcome=Outcome.BLOCK,
            ),
        ],
        fallback_outcome=Outcome.ALLOW,
    )


class _RouterStub:
    """Minimal stub for lib.judge.judge._call_router.

    responses: ordered list; each item is a raw model-output str OR an
    Exception instance to raise on that call.
    """

    def __init__(self, responses: list, model_name: str = "gemma4:e4b") -> None:
        self.responses = list(responses)
        self.model_name = model_name
        self.call_count = 0

    def __call__(self, *, task: str, system: str, user: str, timeout_s: float):
        self.call_count += 1
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item, self.model_name


class _PushSpy:
    """Spy for lib.pushover.send_push."""

    def __init__(self, *, raises: bool = False) -> None:
        self.raises = raises
        self.calls: list[dict] = []

    def __call__(self, *, title: str, message: str, priority: int = 0, **kw) -> dict:
        self.calls.append({"title": title, "message": message, "priority": priority})
        if self.raises:
            raise pushover.PushoverError("simulated send failure")
        return {"status": 1}


def _read_lines(path: Path) -> list[str]:
    return [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


# ─── write_decision: a single row ────────────────────────────────────────────


class TestWriteDecision:
    def test_writes_one_valid_json_line_with_all_keys(
        self, tmp_path: Path, allow_decision: JudgeDecision, sample_proposal: ActionProposal
    ) -> None:
        out = write_decision(
            allow_decision, sample_proposal, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert out.exists()
        assert out.name == "2026-05-28.jsonl"
        lines = _read_lines(out)
        assert len(lines) == 1
        row = json.loads(lines[0])  # exactly one valid JSON object per line
        for key in (
            "evaluated_at",
            "agent_name",
            "outcome",
            "matched_rule_id",
            "model_used",
            "latency_ms",
            "feedback",
            "quarantine_reason",
            "proposal",
        ):
            assert key in row, f"missing key {key!r}"
        assert row["agent_name"] == "substack_drafter"
        assert row["outcome"] == "ALLOW"
        assert row["model_used"] == "gemma4:e4b"
        assert row["latency_ms"] == 412
        assert row["matched_rule_id"] == "rule_d_publish_verb_at_top_level"

    def test_proposal_subobject_round_trips(
        self, tmp_path: Path, allow_decision: JudgeDecision, sample_proposal: ActionProposal
    ) -> None:
        out = write_decision(
            allow_decision, sample_proposal, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        row = json.loads(_read_lines(out)[0])
        rebuilt = ActionProposal.model_validate(row["proposal"])
        assert rebuilt == sample_proposal

    def test_returns_absolute_path(
        self, tmp_path: Path, allow_decision: JudgeDecision, sample_proposal: ActionProposal
    ) -> None:
        out = write_decision(
            allow_decision, sample_proposal, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert out.is_absolute()


# ─── write_decision: append semantics ────────────────────────────────────────


class TestWriteDecisionAppend:
    def test_two_writes_two_lines_in_order(
        self, tmp_path: Path, sample_proposal: ActionProposal
    ) -> None:
        at = datetime(2026, 5, 28, 9, 0, 0, tzinfo=timezone.utc)
        first = JudgeDecision(outcome=Outcome.ALLOW, model_used="gemma4:e4b", latency_ms=1, evaluated_at=at)
        second = JudgeDecision(
            outcome=Outcome.BLOCK, model_used="gemma4:e4b", latency_ms=2, evaluated_at=at
        )
        p1 = write_decision(first, sample_proposal, agent_name="a", ledger_dir=tmp_path)
        p2 = write_decision(second, sample_proposal, agent_name="a", ledger_dir=tmp_path)
        assert p1 == p2  # same UTC date → same bucket file
        lines = _read_lines(p1)
        assert len(lines) == 2
        assert json.loads(lines[0])["outcome"] == "ALLOW"
        assert json.loads(lines[1])["outcome"] == "BLOCK"


# ─── write_decision: UTC-midnight bucketing ──────────────────────────────────


class TestWriteDecisionBucketsByUtcMidnight:
    def test_same_local_date_different_utc_date_splits_files(
        self, tmp_path: Path, sample_proposal: ActionProposal
    ) -> None:
        pst = timezone(timedelta(hours=-8))
        # Both are "the 28th" in PST, but one crosses UTC midnight into the 29th.
        morning_pst = JudgeDecision(
            outcome=Outcome.ALLOW,
            model_used="gemma4:e4b",
            latency_ms=1,
            evaluated_at=datetime(2026, 5, 28, 10, 0, 0, tzinfo=pst),  # 18:00Z → 05-28
        )
        evening_pst = JudgeDecision(
            outcome=Outcome.ALLOW,
            model_used="gemma4:e4b",
            latency_ms=1,
            evaluated_at=datetime(2026, 5, 28, 20, 0, 0, tzinfo=pst),  # 04:00Z next day → 05-29
        )
        p_morning = write_decision(morning_pst, sample_proposal, agent_name="a", ledger_dir=tmp_path)
        p_evening = write_decision(evening_pst, sample_proposal, agent_name="a", ledger_dir=tmp_path)
        assert p_morning.name == "2026-05-28.jsonl"
        assert p_evening.name == "2026-05-29.jsonl"
        assert p_morning != p_evening

    def test_naive_datetime_treated_as_utc(
        self, tmp_path: Path, sample_proposal: ActionProposal
    ) -> None:
        naive = JudgeDecision(
            outcome=Outcome.ALLOW,
            model_used="gemma4:e4b",
            latency_ms=1,
            evaluated_at=datetime(2026, 5, 28, 23, 59, 0),  # no tzinfo
        )
        out = write_decision(naive, sample_proposal, agent_name="a", ledger_dir=tmp_path)
        assert out.name == "2026-05-28.jsonl"


# ─── write_decision: atomicity / lock failure ────────────────────────────────


class TestWriteDecisionAtomicity:
    def test_lock_timeout_raises_ledger_write_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        allow_decision: JudgeDecision,
        sample_proposal: ActionProposal,
    ) -> None:
        class _BoomLock:
            def __init__(self, *a, **k) -> None:
                pass

            def __enter__(self):
                raise filelock.LockTimeout("simulated contention")

            def __exit__(self, *a) -> bool:
                return False

        monkeypatch.setattr(filelock, "FileLock", _BoomLock)
        with pytest.raises(LedgerWriteError):
            write_decision(
                allow_decision, sample_proposal, agent_name="a", ledger_dir=tmp_path
            )

    def test_ledger_write_error_is_a_ledger_error(self) -> None:
        assert issubclass(LedgerWriteError, LedgerError)


# ─── ensure_ledger_ready ─────────────────────────────────────────────────────


class TestEnsureLedgerReady:
    def test_creates_missing_dir_and_passes_when_creds_present(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("PUSHOVER_USER_KEY", "u")
        monkeypatch.setenv("PUSHOVER_API_TOKEN", "t")
        target = tmp_path / "judge_log"
        assert not target.exists()
        ensure_ledger_ready(ledger_dir=target)
        assert target.is_dir()
        # write-test probe is cleaned up
        assert not (target / ".write-test").exists()

    @pytest.mark.skipif(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        reason="root bypasses filesystem write permissions",
    )
    def test_raises_on_read_only_parent(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("PUSHOVER_USER_KEY", "u")
        monkeypatch.setenv("PUSHOVER_API_TOKEN", "t")
        ro_parent = tmp_path / "readonly"
        ro_parent.mkdir()
        ro_parent.chmod(0o500)  # r-x, no write
        try:
            with pytest.raises(LedgerWriteError):
                ensure_ledger_ready(ledger_dir=ro_parent / "judge_log")
        finally:
            ro_parent.chmod(0o700)  # restore so tmp_path cleanup can remove it

    def test_raises_pushover_configuration_error_when_creds_absent(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # Env-var override pattern (NOT a keychain probe): clear env + neutralise
        # the keychain fallback so the result is deterministic on a real Mac too.
        monkeypatch.delenv("PUSHOVER_USER_KEY", raising=False)
        monkeypatch.delenv("PUSHOVER_API_TOKEN", raising=False)
        monkeypatch.setattr(pushover, "get_credential", lambda name: None)
        with pytest.raises(pushover.PushoverConfigurationError):
            ensure_ledger_ready(ledger_dir=tmp_path / "judge_log")


# ─── matched_rule_id derivation ──────────────────────────────────────────────


class TestMatchedRuleIdDerivation:
    def test_fragment_after_hash(self) -> None:
        assert (
            ledger._derive_matched_rule_id("substack_drafter.yaml#rule_a_unverifiable_claim")
            == "rule_a_unverifiable_claim"
        )

    def test_bare_rule_token(self) -> None:
        assert ledger._derive_matched_rule_id("rule_c_voice_mode_drift") == "rule_c_voice_mode_drift"

    def test_no_rule_reference_is_none(self) -> None:
        assert ledger._derive_matched_rule_id("general allowance, no rule") is None

    def test_empty_is_none(self) -> None:
        assert ledger._derive_matched_rule_id("") is None


# ─── judge_action integration (Option B wrapper) ─────────────────────────────


class TestJudgeActionIntegration:
    def test_allow_writes_row_and_does_not_push(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub(['{"outcome": "ALLOW", "feedback": null, "quarantine_reason": null}'])
        monkeypatch.setattr(judge_module, "_call_router", stub)
        spy = _PushSpy()
        monkeypatch.setattr(pushover, "send_push", spy)

        decision = judge_action(
            sample_proposal, sample_policy, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert decision.outcome == "ALLOW"
        # ledger row landed
        files = list(tmp_path.glob("*.jsonl"))
        assert len(files) == 1
        rows = _read_lines(files[0])
        assert len(rows) == 1
        assert json.loads(rows[0])["outcome"] == "ALLOW"
        # Pushover NOT called on ALLOW
        assert spy.calls == []

    def test_judge_unavailable_writes_row_and_pushes_once(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([JudgeTransportError("mac mini unreachable")])
        monkeypatch.setattr(judge_module, "_call_router", stub)
        spy = _PushSpy()
        monkeypatch.setattr(pushover, "send_push", spy)

        decision = judge_action(
            sample_proposal, sample_policy, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        # ledger row landed
        files = list(tmp_path.glob("*.jsonl"))
        assert len(files) == 1
        assert json.loads(_read_lines(files[0])[0])["outcome"] == "JUDGE_UNAVAILABLE"
        # Pushover called exactly once, severity 0, with the canonical title
        assert len(spy.calls) == 1
        assert spy.calls[0]["priority"] == 0
        assert spy.calls[0]["title"] == "Judge layer unavailable"
        assert "substack_drafter" in spy.calls[0]["message"]
        assert "gemma4:e4b" in spy.calls[0]["message"]

    def test_pushover_send_failure_is_logged_not_raised(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub([JudgeTransportError("mac mini unreachable")])
        monkeypatch.setattr(judge_module, "_call_router", stub)
        spy = _PushSpy(raises=True)  # send_push raises PushoverError
        monkeypatch.setattr(pushover, "send_push", spy)

        # Must NOT raise; decision still returned, row still landed.
        decision = judge_action(
            sample_proposal, sample_policy, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert decision.outcome == "JUDGE_UNAVAILABLE"
        assert len(spy.calls) == 1
        assert json.loads(_read_lines(list(tmp_path.glob("*.jsonl"))[0])[0])["outcome"] == "JUDGE_UNAVAILABLE"

    def test_ledger_write_failure_is_logged_not_raised(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        sample_proposal: ActionProposal,
        sample_policy: Policy,
    ) -> None:
        stub = _RouterStub(['{"outcome": "ALLOW", "feedback": null, "quarantine_reason": null}'])
        monkeypatch.setattr(judge_module, "_call_router", stub)
        spy = _PushSpy()
        monkeypatch.setattr(pushover, "send_push", spy)

        def _boom(*a, **k):
            raise LedgerWriteError("simulated ledger failure")

        monkeypatch.setattr(action_module.ledger, "write_decision", _boom)

        # Wrapper takes over the never-raises contract: decision still returned.
        decision = judge_action(
            sample_proposal, sample_policy, agent_name="substack_drafter", ledger_dir=tmp_path
        )
        assert decision.outcome == "ALLOW"
