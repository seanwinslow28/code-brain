"""Declarative YAML policy loader for the judge layer.

A policy is a list of rules. Each rule names a condition the judge should look
for in the actor's proposal + the outcome to return when that condition fires
+ a feedback template (REVISE) or quarantine reason template (ESCALATE).

Why YAML and not Python: the policy is the part a recruiter / CISO reads to
understand what your control plane gates against. Code is implementation;
YAML is contract. The judge.evaluate() function (Day 3) loads the policy at
runtime and feeds the rules into the local-model prompt.

Schema (top-level keys):
  name: str               — human-friendly name, e.g. "Substack Drafter Policy v1"
  agent: str              — which agent this policy gates, e.g. "substack_drafter"
  version: str            — semver. Bumps on every rule change.
  rules: list[Rule]       — ordered. First match wins (deny > ask > allow pattern).
  fallback_outcome: str   — what to return if no rule fires. Default ALLOW.

Each Rule:
  id:                str  — stable identifier, kebab-case. Used in the ledger
                            row's `authorization_basis` field for traceability.
  condition:         str  — natural-language description of what to look for.
                            The judge model receives this verbatim in its prompt.
  outcome:           str  — one of Outcome's 5 string values.
  feedback_template: str  — Optional. Required when outcome=REVISE.
  quarantine_reason: str  — Optional. Required when outcome=ESCALATE.

The loader validates the schema and the cross-field constraints (REVISE rules
must carry feedback_template, ESCALATE rules must carry quarantine_reason)
BEFORE returning the Policy object. A malformed YAML never reaches evaluate().
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from lib.judge.schema import Outcome

# Where policy YAMLs live. agents-sdk/policies/<name>.yaml is the convention.
# Matches the [substack_drafter] / [llm_council] / [gemini_researcher] config-
# block colocation pattern — one file per actor.
POLICIES_DIR = Path(__file__).parent.parent.parent / "policies"


class PolicyError(Exception):
    """Base class for any policy load/validation error."""


class PolicyNotFoundError(PolicyError):
    """Raised when load_policy(name) can't find <name>.yaml at POLICIES_DIR."""


class PolicySchemaError(PolicyError):
    """Raised when YAML loads but the schema is wrong (missing key, wrong
    type, REVISE rule without feedback_template, etc.). Fails loud at boot
    so a typo in the YAML never reaches evaluate()."""


@dataclass(frozen=True)
class Rule:
    """One rule inside a Policy.

    Frozen so the dict[str, Rule] inside Policy can't be mutated mid-run.
    Order in the YAML is preserved by the load_policy parser (PyYAML
    safe_load preserves dict ordering on Python 3.7+); first match wins
    in the evaluator (Day 3).
    """

    id: str
    condition: str
    outcome: Outcome
    feedback_template: str | None = None
    quarantine_reason: str | None = None


@dataclass(frozen=True)
class Policy:
    """A loaded, validated policy.

    Frozen — mutation requires reloading from disk. The Day 3 evaluator
    treats Policy as a value, not a mutable state container.
    """

    name: str
    agent: str
    version: str
    rules: list[Rule] = field(default_factory=list)
    fallback_outcome: Outcome = Outcome.ALLOW


# Cross-field constraints: which Outcome values demand which optional field.
# Centralized here so the test file can read this dict directly when checking
# the loader's validation logic, instead of duplicating the rule.
_OUTCOME_REQUIRED_FIELDS: dict[Outcome, str] = {
    Outcome.REVISE: "feedback_template",
    Outcome.ESCALATE: "quarantine_reason",
}


def _validate_outcome_string(raw: str, *, where: str) -> Outcome:
    """Parse a string into an Outcome enum, raising a clear error on miss.

    `where` is a human-readable location string used in the error message
    (e.g., "rules[0].outcome" or "fallback_outcome") so a recruiter reading
    the traceback can see exactly which YAML cell failed.
    """
    try:
        return Outcome(raw)
    except ValueError as exc:
        valid = ", ".join(o.value for o in Outcome)
        raise PolicySchemaError(
            f"{where}: '{raw}' is not a valid Outcome. Must be one of: {valid}"
        ) from exc


def _validate_rule_dict(raw: dict, *, index: int) -> Rule:
    """Convert a raw YAML rule dict into a Rule, raising on schema violations.

    `index` is the rule's position in the YAML list, used in error messages
    so the failing rule is immediately findable in the file.
    """
    # Required fields on every rule.
    for required in ("id", "condition", "outcome"):
        if required not in raw:
            raise PolicySchemaError(
                f"rules[{index}]: missing required field '{required}'"
            )

    rule_id = raw["id"]
    if not isinstance(rule_id, str) or not rule_id:
        raise PolicySchemaError(
            f"rules[{index}].id: must be a non-empty string, got {type(rule_id).__name__}"
        )

    condition = raw["condition"]
    if not isinstance(condition, str) or not condition.strip():
        raise PolicySchemaError(
            f"rules[{index}].condition: must be a non-empty string"
        )

    outcome = _validate_outcome_string(
        raw["outcome"], where=f"rules[{index}].outcome"
    )

    # Cross-field check: REVISE rules need feedback_template, ESCALATE rules
    # need quarantine_reason. Both being empty when required → load fails.
    required_aux = _OUTCOME_REQUIRED_FIELDS.get(outcome)
    if required_aux and not raw.get(required_aux):
        raise PolicySchemaError(
            f"rules[{index}] (id={rule_id!r}, outcome={outcome.value}): "
            f"missing required field '{required_aux}' for this outcome"
        )

    return Rule(
        id=rule_id,
        condition=condition,
        outcome=outcome,
        feedback_template=raw.get("feedback_template"),
        quarantine_reason=raw.get("quarantine_reason"),
    )


def load_policy(
    name: str,
    *,
    policies_dir: Path | None = None,
) -> Policy:
    """Load and validate a policy from <policies_dir>/<name>.yaml.

    Args:
        name: Policy name without the .yaml suffix. Convention: matches the
            agent's [config.toml] table name (e.g., "substack_drafter" →
            substack_drafter.yaml).
        policies_dir: Override the default agents-sdk/policies/ path. Tests
            pass a tmp_path so they don't touch the real policy files.

    Returns:
        A frozen Policy dataclass with rules in YAML-declared order.

    Raises:
        PolicyNotFoundError: <name>.yaml doesn't exist.
        PolicySchemaError:   YAML loads but fails schema/cross-field checks.
    """
    base = policies_dir or POLICIES_DIR
    path = base / f"{name}.yaml"

    if not path.exists():
        raise PolicyNotFoundError(
            f"Policy '{name}' not found at {path}. "
            f"Expected file: {path.name} in {path.parent}/"
        )

    with open(path, encoding="utf-8") as fh:
        try:
            raw = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            raise PolicySchemaError(f"{path.name}: malformed YAML — {e}") from e

    if not isinstance(raw, dict):
        raise PolicySchemaError(
            f"{path.name}: top-level YAML must be a mapping, got {type(raw).__name__}"
        )

    # Required top-level fields.
    for required in ("name", "agent", "version", "rules"):
        if required not in raw:
            raise PolicySchemaError(
                f"{path.name}: missing required top-level field '{required}'"
            )

    if not isinstance(raw["rules"], list):
        raise PolicySchemaError(
            f"{path.name}: 'rules' must be a list, got {type(raw['rules']).__name__}"
        )

    rules: list[Rule] = []
    seen_ids: set[str] = set()
    for i, raw_rule in enumerate(raw["rules"]):
        if not isinstance(raw_rule, dict):
            raise PolicySchemaError(
                f"{path.name}: rules[{i}] must be a mapping, got {type(raw_rule).__name__}"
            )
        rule = _validate_rule_dict(raw_rule, index=i)
        if rule.id in seen_ids:
            raise PolicySchemaError(
                f"{path.name}: rules[{i}].id='{rule.id}' is a duplicate; rule IDs "
                f"must be unique (the ledger row references them for traceability)."
            )
        seen_ids.add(rule.id)
        rules.append(rule)

    fallback_raw = raw.get("fallback_outcome", "ALLOW")
    fallback = _validate_outcome_string(fallback_raw, where="fallback_outcome")

    # Defensive: an ESCALATE / REVISE fallback would have no feedback or
    # quarantine_reason source. Reject it loud at load instead of leaving the
    # evaluator to deal with the None.
    if fallback in _OUTCOME_REQUIRED_FIELDS:
        raise PolicySchemaError(
            f"{path.name}: fallback_outcome={fallback.value} requires a "
            f"{_OUTCOME_REQUIRED_FIELDS[fallback]} which fallback can't provide. "
            f"Use ALLOW, BLOCK, or JUDGE_UNAVAILABLE as fallback."
        )

    return Policy(
        name=raw["name"],
        agent=raw["agent"],
        version=str(raw["version"]),
        rules=rules,
        fallback_outcome=fallback,
    )
