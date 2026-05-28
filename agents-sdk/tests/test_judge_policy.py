"""Tests for lib.judge.policy — YAML policy loader + validation.

Two layers of coverage:
  1. Loader unit tests against synthetic YAML in tmp_path. Pins the schema
     contract + the cross-field validation rules.
  2. One integration test that loads the REAL policies/substack_drafter.yaml
     and asserts the 4-rule + 4-id contract. If anyone edits the real policy
     in a way that breaks the loader's invariants, CI catches it here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.judge.policy import (
    POLICIES_DIR,
    Policy,
    PolicyNotFoundError,
    PolicySchemaError,
    Rule,
    load_policy,
)
from lib.judge.schema import Outcome


# Minimal valid YAML used as the baseline; tests mutate copies.
_VALID_YAML = """\
name: "Test Policy"
agent: "test_agent"
version: "0.1.0"
rules:
  - id: "rule_allow_baseline"
    condition: "The draft is well-formed and makes no risky claims."
    outcome: "ALLOW"
  - id: "rule_revise_voice"
    condition: "The voice mode drifted."
    outcome: "REVISE"
    feedback_template: "Re-render in the assigned voice."
  - id: "rule_escalate_pii"
    condition: "The draft contains PII."
    outcome: "ESCALATE"
    quarantine_reason: "PII detected; needs human review."
  - id: "rule_block_self_publish"
    condition: "The draft includes a self-publish verb."
    outcome: "BLOCK"
fallback_outcome: "ALLOW"
"""


def _write_policy(tmp_path: Path, content: str, name: str = "test_agent") -> Path:
    """Write a policy file to a tmp policies dir and return that dir.

    Helper used by every loader test so the production POLICIES_DIR is
    never touched. Matches the test_filelock.py pattern of containing all
    I/O inside tmp_path.
    """
    policies_dir = tmp_path / "policies"
    policies_dir.mkdir(parents=True, exist_ok=True)
    (policies_dir / f"{name}.yaml").write_text(content, encoding="utf-8")
    return policies_dir


class TestLoadPolicyHappyPath:
    def test_baseline_yaml_loads(self, tmp_path: Path) -> None:
        """A fully-valid YAML loads into a Policy with 4 rules in order."""
        policies_dir = _write_policy(tmp_path, _VALID_YAML)
        policy = load_policy("test_agent", policies_dir=policies_dir)

        assert isinstance(policy, Policy)
        assert policy.name == "Test Policy"
        assert policy.agent == "test_agent"
        assert policy.version == "0.1.0"
        assert len(policy.rules) == 4
        # Order preserved from YAML — first-match-wins relies on this.
        assert [r.id for r in policy.rules] == [
            "rule_allow_baseline",
            "rule_revise_voice",
            "rule_escalate_pii",
            "rule_block_self_publish",
        ]

    def test_rule_outcomes_parse_to_enum(self, tmp_path: Path) -> None:
        """Each rule's outcome is the Outcome enum value, not the raw string."""
        policies_dir = _write_policy(tmp_path, _VALID_YAML)
        policy = load_policy("test_agent", policies_dir=policies_dir)
        by_id = {r.id: r for r in policy.rules}
        assert by_id["rule_allow_baseline"].outcome == Outcome.ALLOW
        assert by_id["rule_revise_voice"].outcome == Outcome.REVISE
        assert by_id["rule_escalate_pii"].outcome == Outcome.ESCALATE
        assert by_id["rule_block_self_publish"].outcome == Outcome.BLOCK

    def test_revise_rule_carries_feedback(self, tmp_path: Path) -> None:
        policies_dir = _write_policy(tmp_path, _VALID_YAML)
        policy = load_policy("test_agent", policies_dir=policies_dir)
        revise = next(r for r in policy.rules if r.outcome == Outcome.REVISE)
        assert revise.feedback_template == "Re-render in the assigned voice."

    def test_escalate_rule_carries_quarantine_reason(self, tmp_path: Path) -> None:
        policies_dir = _write_policy(tmp_path, _VALID_YAML)
        policy = load_policy("test_agent", policies_dir=policies_dir)
        escalate = next(r for r in policy.rules if r.outcome == Outcome.ESCALATE)
        assert escalate.quarantine_reason == "PII detected; needs human review."

    def test_default_fallback_outcome_is_allow(self, tmp_path: Path) -> None:
        """When fallback_outcome is omitted from YAML, default is ALLOW."""
        yaml_no_fallback = _VALID_YAML.replace('fallback_outcome: "ALLOW"\n', "")
        policies_dir = _write_policy(tmp_path, yaml_no_fallback)
        policy = load_policy("test_agent", policies_dir=policies_dir)
        assert policy.fallback_outcome == Outcome.ALLOW

    def test_explicit_fallback_outcome_block(self, tmp_path: Path) -> None:
        """fallback_outcome can be BLOCK for a deny-by-default policy."""
        yaml_block_fallback = _VALID_YAML.replace(
            'fallback_outcome: "ALLOW"', 'fallback_outcome: "BLOCK"'
        )
        policies_dir = _write_policy(tmp_path, yaml_block_fallback)
        policy = load_policy("test_agent", policies_dir=policies_dir)
        assert policy.fallback_outcome == Outcome.BLOCK


class TestLoadPolicyNotFound:
    def test_missing_file_raises(self, tmp_path: Path) -> None:
        """Loading a nonexistent policy raises PolicyNotFoundError with a
        clear message pointing at the expected path."""
        policies_dir = tmp_path / "policies"
        policies_dir.mkdir()
        with pytest.raises(PolicyNotFoundError) as exc_info:
            load_policy("does_not_exist", policies_dir=policies_dir)
        assert "does_not_exist" in str(exc_info.value)
        assert "policies" in str(exc_info.value)


class TestLoadPolicySchemaErrors:
    @pytest.mark.parametrize(
        "missing_field",
        ["name", "agent", "version", "rules"],
    )
    def test_missing_top_level_field_raises(
        self, tmp_path: Path, missing_field: str
    ) -> None:
        """All four top-level fields are required."""
        bad_yaml = "\n".join(
            line
            for line in _VALID_YAML.splitlines()
            if not line.startswith(f"{missing_field}:")
        )
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert missing_field in str(exc_info.value)

    def test_top_level_not_a_mapping_raises(self, tmp_path: Path) -> None:
        """A YAML that loads as a list (or string) at top level is malformed."""
        policies_dir = _write_policy(tmp_path, "- just\n- a\n- list\n")
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "mapping" in str(exc_info.value).lower()

    def test_rules_not_a_list_raises(self, tmp_path: Path) -> None:
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules: "not a list"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "rules" in str(exc_info.value).lower()

    def test_invalid_outcome_string_raises(self, tmp_path: Path) -> None:
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules:
  - id: "bad_outcome"
    condition: "Whatever."
    outcome: "MAYBE"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        # Error message lists the valid outcomes so the YAML author can fix it.
        err = str(exc_info.value)
        assert "MAYBE" in err
        assert "ALLOW" in err  # at least one valid value mentioned

    def test_revise_without_feedback_template_raises(
        self, tmp_path: Path
    ) -> None:
        """REVISE rules MUST carry a feedback_template — the actor needs
        something to retry with."""
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules:
  - id: "revise_no_feedback"
    condition: "Whatever."
    outcome: "REVISE"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "feedback_template" in str(exc_info.value)

    def test_escalate_without_quarantine_reason_raises(
        self, tmp_path: Path
    ) -> None:
        """ESCALATE rules MUST carry a quarantine_reason — the ledger row
        needs the reason to surface in the dashboard."""
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules:
  - id: "escalate_no_reason"
    condition: "Whatever."
    outcome: "ESCALATE"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "quarantine_reason" in str(exc_info.value)

    def test_duplicate_rule_id_raises(self, tmp_path: Path) -> None:
        """Rule ids must be unique — the ledger row's authorization_basis
        field is the join key for audit grep queries."""
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules:
  - id: "duplicate"
    condition: "First."
    outcome: "ALLOW"
  - id: "duplicate"
    condition: "Second."
    outcome: "ALLOW"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "duplicate" in str(exc_info.value).lower()

    def test_rule_missing_id_raises(self, tmp_path: Path) -> None:
        bad_yaml = """\
name: "Test"
agent: "test_agent"
version: "0.1.0"
rules:
  - condition: "No id field."
    outcome: "ALLOW"
"""
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "id" in str(exc_info.value)

    def test_fallback_revise_rejected(self, tmp_path: Path) -> None:
        """fallback_outcome=REVISE has no feedback_template source, so the
        loader rejects it loud rather than producing an evaluator that
        deals with the None at runtime."""
        bad_yaml = _VALID_YAML.replace(
            'fallback_outcome: "ALLOW"', 'fallback_outcome: "REVISE"'
        )
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "fallback" in str(exc_info.value).lower()

    def test_fallback_escalate_rejected(self, tmp_path: Path) -> None:
        bad_yaml = _VALID_YAML.replace(
            'fallback_outcome: "ALLOW"', 'fallback_outcome: "ESCALATE"'
        )
        policies_dir = _write_policy(tmp_path, bad_yaml)
        with pytest.raises(PolicySchemaError) as exc_info:
            load_policy("test_agent", policies_dir=policies_dir)
        assert "fallback" in str(exc_info.value).lower()


class TestRuleFrozen:
    def test_rule_dataclass_is_frozen(self) -> None:
        """Rule is @dataclass(frozen=True) so mid-evaluation mutation can't
        sneak past the schema's validation."""
        rule = Rule(
            id="x",
            condition="y",
            outcome=Outcome.ALLOW,
        )
        with pytest.raises(Exception):
            rule.outcome = Outcome.BLOCK  # type: ignore[misc]


class TestRealSubstackDrafterPolicy:
    """Integration: load the REAL policies/substack_drafter.yaml and assert
    the 4-rule contract. If anyone edits the policy in a way that breaks the
    loader's invariants, this catches it. If anyone adds a 5th rule
    legitimately, this test fails loud and forces a dashboard panel update."""

    def test_loads_clean(self) -> None:
        """The shipped substack_drafter.yaml loads without raising."""
        policy = load_policy("substack_drafter")
        assert policy.agent == "substack_drafter"
        assert policy.name.startswith("Substack-Drafter")

    def test_has_exactly_four_rules(self) -> None:
        policy = load_policy("substack_drafter")
        assert len(policy.rules) == 4, (
            "Substack-Drafter policy v1 ships with 4 rules. If you added "
            "a 5th, update tests + dashboard panels in the same PR."
        )

    def test_four_canonical_rule_ids(self) -> None:
        """The four rule ids are stable identifiers the ledger consumer
        keys on. Renaming a rule breaks dashboard authorization_basis
        aggregation — caught here."""
        policy = load_policy("substack_drafter")
        ids = {r.id for r in policy.rules}
        expected = {
            "rule_a_unverifiable_claim_named_person",
            "rule_b_block_attribution_requires_citation",
            "rule_c_voice_mode_drift",
            "rule_d_publish_verb_at_top_level",
        }
        assert ids == expected

    def test_outcome_distribution(self) -> None:
        """One ESCALATE + two REVISE + one BLOCK is the v1.0.0 mix.
        Changing this distribution is a policy decision, not a refactor —
        update the test in the same PR."""
        policy = load_policy("substack_drafter")
        outcomes = [r.outcome for r in policy.rules]
        assert outcomes.count(Outcome.ESCALATE) == 1
        assert outcomes.count(Outcome.REVISE) == 2
        assert outcomes.count(Outcome.BLOCK) == 1
        assert outcomes.count(Outcome.ALLOW) == 0  # ALLOW is only fallback

    def test_fallback_is_allow(self) -> None:
        """Defense-in-depth: when no rule matches, allow and let Sean's
        manual review catch what the judge would have."""
        policy = load_policy("substack_drafter")
        assert policy.fallback_outcome == Outcome.ALLOW


class TestPoliciesDirConstant:
    def test_points_at_agents_sdk_policies(self) -> None:
        """POLICIES_DIR is the canonical location for all judge policy YAMLs.
        If someone moves the policies dir, this assertion forces an update
        across the loader + Day 6 substack-drafter integration."""
        # Resolve to absolute paths so the comparison survives symlinks.
        expected_suffix = Path("agents-sdk") / "policies"
        assert str(POLICIES_DIR).endswith(str(expected_suffix))
