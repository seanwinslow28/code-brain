"""Cap-policy registry: the ONE content home for shared-ledger spend caps.

Editing cap_policy.json IS a cap change and requires Sean's explicit approval — the
plan -> approve -> execute gate recorded in the-oracle's CLAUDE.md (rule 2 /
"Spend governance") and in the approved F8b plan
(the-oracle/docs/phase-plans/2026-07-18-f8b-ledger-governance.md). Policy CONTENT lives
in git (code-reviewed, Sean-gated); policy ACTIVATION is the separate Sean-gated act
(``activate_policy``) that makes a version enforceable via the shared spend root.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from pathlib import Path


ACTIVE_POLICY_FILENAME = "council-policy-active.json"
_POLICY_FILENAME = "cap_policy.json"
_TOP_LEVEL_KEYS = {"policy_version", "tools", "aggregate", "sum_exceeds_aggregate"}
_TOOL_KEYS = {
    "per_query_caps",
    "daily_cap",
    "monthly_cap",
    "reservation_basis",
    "force_per_query_allowed",
}
_AGGREGATE_KEYS = {"daily_cap", "monthly_cap"}
_RESERVATION_BASES = {"worst_case", "estimate"}
_ACTIVATION_KEYS = {"policy_version", "policy_hash", "activated_at_utc", "policy"}


class PolicyError(Exception):
    """A cap policy is missing, malformed, or internally inconsistent."""


def _reject_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise PolicyError(f"duplicate JSON key {key!r}")
        seen[key] = value
    return seen


def _positive_decimal(value, *, field: str) -> Decimal:
    # Money must be authored as a JSON decimal (7.00, never 7): ints are refused so that
    # semantically identical policies cannot acquire different canonical hashes
    # ("245" vs "245.0" — review finding 3). Fail closed on ambiguity, one identity per policy.
    if isinstance(value, bool) or not isinstance(value, float):
        raise PolicyError(
            f"{field} must be a positive finite JSON decimal (write 7.00, not 7), got {value!r}"
        )
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise PolicyError(f"{field} must be a positive finite number, got {value!r}") from exc
    if not number.is_finite() or number <= 0:
        raise PolicyError(f"{field} must be a positive finite number, got {value!r}")
    return number


def _require_exact_keys(value: dict, expected: set[str], *, field: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise PolicyError(f"{field} keys invalid: missing={missing}, extra={extra}")


def _validate_policy(data, *, source: str) -> dict:
    if not isinstance(data, dict):
        raise PolicyError(f"{source}: top level must be an object")
    _require_exact_keys(data, _TOP_LEVEL_KEYS, field=f"{source}: top-level keys")

    version = data["policy_version"]
    if isinstance(version, bool) or not isinstance(version, int) or version <= 0:
        raise PolicyError(f"{source}: policy_version must be a positive integer")

    tools = data["tools"]
    if not isinstance(tools, dict) or not tools:
        raise PolicyError(f"{source}: tools must be a non-empty object")

    daily_sum = Decimal(0)
    monthly_sum = Decimal(0)
    for tool_name, entry in tools.items():
        if not isinstance(entry, dict):
            raise PolicyError(f"{source}: tool {tool_name!r} must be an object")
        _require_exact_keys(entry, _TOOL_KEYS, field=f"{source}: tool {tool_name!r} keys")

        per_query_caps = entry["per_query_caps"]
        if not isinstance(per_query_caps, list) or not per_query_caps:
            raise PolicyError(
                f"{source}: tool {tool_name!r} per_query_caps must be a non-empty list"
            )
        cap_numbers = [
            _positive_decimal(value, field=f"{source}: tool {tool_name!r} per_query_caps")
            for value in per_query_caps
        ]
        if len(set(cap_numbers)) != len(cap_numbers):
            raise PolicyError(f"{source}: tool {tool_name!r} per_query_caps must be unique")
        if cap_numbers != sorted(cap_numbers):
            raise PolicyError(
                f"{source}: tool {tool_name!r} per_query_caps must be sorted ascending"
            )

        daily = _positive_decimal(
            entry["daily_cap"], field=f"{source}: tool {tool_name!r} daily_cap"
        )
        monthly = _positive_decimal(
            entry["monthly_cap"], field=f"{source}: tool {tool_name!r} monthly_cap"
        )
        if daily > monthly:
            raise PolicyError(
                f"{source}: tool {tool_name!r} daily_cap must not exceed monthly_cap"
            )
        daily_sum += daily
        monthly_sum += monthly

        basis = entry["reservation_basis"]
        if not isinstance(basis, str) or basis not in _RESERVATION_BASES:
            # The isinstance guard keeps unhashable values (e.g. a list) from escaping as a
            # raw TypeError instead of the fail-closed PolicyError (review finding 2).
            raise PolicyError(
                f"{source}: tool {tool_name!r} reservation_basis must be one of "
                f"{sorted(_RESERVATION_BASES)}"
            )
        if not isinstance(entry["force_per_query_allowed"], bool):
            raise PolicyError(
                f"{source}: tool {tool_name!r} force_per_query_allowed must be a bool"
            )

    aggregate = data["aggregate"]
    if not isinstance(aggregate, dict):
        raise PolicyError(f"{source}: aggregate must be an object")
    _require_exact_keys(aggregate, _AGGREGATE_KEYS, field=f"{source}: aggregate")
    aggregate_daily = _positive_decimal(
        aggregate["daily_cap"], field=f"{source}: aggregate.daily_cap"
    )
    aggregate_monthly = _positive_decimal(
        aggregate["monthly_cap"], field=f"{source}: aggregate.monthly_cap"
    )
    if aggregate_daily > aggregate_monthly:
        raise PolicyError(f"{source}: aggregate.daily_cap must not exceed monthly_cap")

    relation_flag = data["sum_exceeds_aggregate"]
    if not isinstance(relation_flag, bool):
        raise PolicyError(f"{source}: sum_exceeds_aggregate must be a bool")
    computed = daily_sum > aggregate_daily or monthly_sum > aggregate_monthly
    if computed != relation_flag:
        raise PolicyError(
            f"{source}: sum_exceeds_aggregate mismatch: daily sum {daily_sum} vs "
            f"daily aggregate {aggregate_daily}; monthly sum {monthly_sum} vs "
            f"monthly aggregate {aggregate_monthly}"
        )
    return data


def load_policy(path=None) -> dict:
    """Load and strictly validate a policy; never fall back to another source."""
    policy_path = Path(path) if path is not None else Path(__file__).with_name(_POLICY_FILENAME)
    try:
        raw = policy_path.read_text()
    except FileNotFoundError as exc:
        raise PolicyError(f"policy file missing: {policy_path}") from exc
    except UnicodeDecodeError as exc:
        # read_text() decodes before json.loads runs; without this clause invalid UTF-8
        # escapes as a raw UnicodeDecodeError instead of PolicyError (review finding 2).
        raise PolicyError(f"{policy_path}: not valid UTF-8") from exc
    except OSError as exc:
        raise PolicyError(f"cannot read policy file {policy_path}: {exc}") from exc
    try:
        data = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except PolicyError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise PolicyError(f"{policy_path}: malformed JSON") from exc
    return _validate_policy(data, source=str(policy_path))


def policy_hash(policy: dict) -> str:
    """Return the SHA-256 of the policy's canonical JSON serialization."""
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def load_active_policy(root: Path) -> dict | None:
    """Read and validate the shared activation snapshot, or return None if absent."""
    from council import budget

    path = Path(root) / ACTIVE_POLICY_FILENAME
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return None
    except UnicodeDecodeError as exc:
        raise budget.LedgerCorrupt("policy activation is not valid UTF-8") from exc
    except OSError as exc:
        raise budget.LedgerCorrupt(f"policy activation unreadable: {exc}") from exc
    try:
        record = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except PolicyError as exc:
        raise budget.LedgerCorrupt(f"policy activation {exc}") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise budget.LedgerCorrupt("policy activation malformed JSON") from exc

    if not isinstance(record, dict) or set(record) != _ACTIVATION_KEYS:
        raise budget.LedgerCorrupt(
            "policy activation keys invalid: required policy_version, policy_hash, "
            "activated_at_utc, policy"
        )
    try:
        embedded = _validate_policy(record["policy"], source="activation embedded policy")
    except PolicyError as exc:
        raise budget.LedgerCorrupt(f"activation embedded policy invalid: {exc}") from exc

    outer_version = record["policy_version"]
    # Python's True == 1 would launder a boolean outer version through an equality check
    # (review finding 1) — require the exact type before comparing.
    if isinstance(outer_version, bool) or not isinstance(outer_version, int):
        raise budget.LedgerCorrupt("policy activation policy_version must be an integer")
    if outer_version != embedded["policy_version"]:
        raise budget.LedgerCorrupt("policy activation version mismatch")
    if not isinstance(record["policy_hash"], str):
        raise budget.LedgerCorrupt("policy activation policy_hash must be a string")
    expected_hash = policy_hash(embedded)
    if record["policy_hash"] != expected_hash:
        raise budget.LedgerCorrupt("policy activation hash mismatch")
    activated_at = record["activated_at_utc"]
    if not isinstance(activated_at, str):
        raise budget.LedgerCorrupt("policy activation activated_at_utc is invalid")
    try:
        parsed_at = datetime.fromisoformat(activated_at)
    except ValueError as exc:
        raise budget.LedgerCorrupt("policy activation activated_at_utc is invalid") from exc
    if parsed_at.tzinfo is None or parsed_at.utcoffset() != timezone.utc.utcoffset(parsed_at):
        raise budget.LedgerCorrupt("policy activation activated_at_utc is not UTC")
    return record


def activate_policy(policy_path=None, root=None) -> dict:
    """Sean-gated activation: atomically publish a validated checkout policy snapshot."""
    from council import budget

    validated = load_policy(policy_path)
    # Realpath-resolve an injected root too: the lock kernel's identity rule is that two
    # spellings of one directory must collapse to the same lock file.
    spend_root = budget._resolve_root() if root is None else Path(os.path.realpath(root))
    record = {
        "policy_version": validated["policy_version"],
        "policy_hash": policy_hash(validated),
        "activated_at_utc": datetime.now(timezone.utc).isoformat(),
        "policy": validated,
    }
    accounting_date = budget.utc_accounting_date()
    with budget.month_lock(accounting_date, root=spend_root):
        budget._atomic_write_json_fsync(spend_root / ACTIVE_POLICY_FILENAME, record)
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Manage the shared council cap policy")
    subparsers = parser.add_subparsers(dest="command", required=True)
    activate = subparsers.add_parser("activate", help="activate a validated policy")
    activate.add_argument("--policy", type=Path)
    args = parser.parse_args(argv)

    try:
        record = activate_policy(args.policy)
    except (PolicyError, OSError) as exc:
        print(f"policy activation refused: {exc}", file=sys.stderr)
        return 1
    print(f"activated policy version {record['policy_version']} hash {record['policy_hash']}")
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised through main()
    raise SystemExit(main())
