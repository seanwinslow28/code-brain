"""Cost estimation, spend recording, and pre-flight cap enforcement.

Spend files live at $COUNCIL_SPEND_DIR (default: vault/health/) and are append-only
JSON written atomically via tmp + rename.

F8a.3 adds the-oracle's locked reserve-before-dispatch surface on this same ledger:
a canonical month-scoped ``flock`` (``month_lock``), a locked ``record_spend`` for
*every* writer (so an unmigrated sibling's stale read-modify-write can never clobber a
durably-appended oracle reservation), a strict fail-closed enforcement parser
(``strict_ledger_state``), the ``check_and_reserve`` transaction, and a crash-safe
``reserved -> dispatched -> settled | unknown`` reservation lifecycle. Siblings keep
their tolerant preflight/settlement lifecycle until F8b; only their *mutation* is now
serialized. The reserved-cost is the sole enforcement debit (``amount``/``total``);
actual ``usage.cost`` is recorded in a non-debit ``actuals`` array keyed by
``run_id``+``attempt_id``. The schema is versioned so F8b is additive.
"""

import contextlib
import fcntl
import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import ROUND_CEILING, Decimal, InvalidOperation
from pathlib import Path

# Additive schema contract (F8b populates the nullable policy_* fields + adds writers
# without rewriting F8a rows or changing the lock kernel).
LEDGER_SCHEMA_VERSION = 2
_SUPPORTED_SCHEMA_VERSIONS = (1, 2)
_MICRO = Decimal("0.000001")
_RESERVATION_KIND = "reservation"
_RESERVED = "reserved"
_DISPATCHED = "dispatched"
_SETTLED = "settled"
_UNKNOWN = "unknown"
_LIFECYCLE_STATES = (_RESERVED, _DISPATCHED, _SETTLED, _UNKNOWN)
_NONTERMINAL = (_RESERVED, _DISPATCHED)
_PROVENANCE = ("authoritative", "estimated", "unknown")

# Task 5 flips it.
POLICY_ENFORCEMENT_ENABLED = False


@dataclass(frozen=True)
class Pricing:
    """Per-1k-token prices in USD."""
    prompt_per_1k: float
    completion_per_1k: float


class BudgetExceeded(Exception):
    """Raised when a pre-flight check rejects a query."""


class LedgerCorrupt(Exception):
    """Strict enforcement parse refused the ledger — fail closed, never under-count.

    Distinct from the tolerant ``_read_total_*``/``_sum_runs`` readers, which stay
    tolerant for dashboards/reporting only.
    """


class ReservationError(Exception):
    """An illegal reservation lifecycle transition or a missing reservation row."""


def utc_accounting_date() -> date:
    """Return the UTC calendar day used by every ledger writer.

    This is the ONLY sanctioned accounting-date source for ledger writers, matching the
    derivation used inline by the-oracle's ``oracle/spend.py::reserve_sync``. A local date
    is a correctness bug (residual 2): a sibling writing at 17:00 PDT on August 31 uses
    2026-08-31 locally even though the instant is 2026-09-01 UTC. Its spend then never
    appears in the UTC September aggregate, and it takes August's month lock while a UTC
    writer holds September's, so mutual exclusion is lost across the boundary.

    Month-boundary contract: THE ADMISSION MONTH OWNS THE RUN. A ``Reservation`` carries
    its ``on_date``; actuals and ``close`` write to that month's file under that month's
    lock (the existing kernel behavior). This is sound precisely because reservation is a
    pre-dispatch bound: cash from a run reserved August 31 and settled September 1 was
    already admitted against August's caps and cannot exceed its August debit. Never take
    two month locks in one transaction.
    """
    return datetime.now(timezone.utc).date()


def _spend_dir() -> Path:
    raw = os.environ.get("COUNCIL_SPEND_DIR")
    if raw:
        d = Path(raw)
    else:
        # Walk up to find vault/health/ relative to this file.
        here = Path(__file__).resolve()
        d = here.parents[3] / "vault" / "health"
    d.mkdir(parents=True, exist_ok=True)
    return d


def spend_dir() -> Path:
    """Public reporting/tooling accessor for the configured spend directory.

    Enforcement transactions continue to pin one resolved root via ``_resolve_root``.
    """
    return _spend_dir()


def _daily_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.isoformat()}.json"


def _monthly_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.strftime('%Y-%m')}.json"


def estimate_cost(*, pricing: dict[str, Pricing], per_model_tokens: list[tuple[str, int, int]]) -> float:
    """Sum per-model (in_tokens × prompt_per_1k + out_tokens × completion_per_1k) over /1000.

    `per_model_tokens` is a list of (model_id, in_tokens, out_tokens) tuples.
    Raises KeyError if any model_id is missing from pricing.
    """
    total = 0.0
    for model_id, in_tokens, out_tokens in per_model_tokens:
        if model_id not in pricing:
            raise KeyError(f"pricing missing for model {model_id!r}")
        p = pricing[model_id]
        total += (in_tokens / 1000.0) * p.prompt_per_1k
        total += (out_tokens / 1000.0) * p.completion_per_1k
    return total


def _atomic_write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def _read_total_for_day(on_date: date) -> float:
    f = _daily_file(on_date)
    if not f.exists():
        return 0.0
    return float(json.loads(f.read_text()).get("total", 0.0))


def _read_total_for_month(on_date: date) -> float:
    # Sum every council-spend-YYYY-MM-DD.json in the same YYYY-MM
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    total = 0.0
    for f in _spend_dir().glob(f"{prefix}*.json"):
        try:
            total += float(json.loads(f.read_text()).get("total", 0.0))
        except (json.JSONDecodeError, ValueError):
            continue
    return total


def record_spend(*, amount: float, profile: str, tag: str, on_date: date, tool: str = "council") -> None:
    """Append a run to today's daily spend file under the canonical month lock.

    F8a.3 (finding 1): the read-modify-write acquires the month lock on *every*
    mutation, including legacy sibling calls, so an unmigrated sibling's stale snapshot
    can never clobber a durably-appended oracle reservation. The signature and on-disk
    shape are unchanged, so siblings need no code change.
    """
    on_date = _normalize_account_date(on_date)
    root = _resolve_root()
    with month_lock(on_date, root=root):
        f = _daily_file_in(root, on_date)
        if f.exists():
            data = json.loads(f.read_text())
        else:
            data = {"date": on_date.isoformat(), "total": 0.0, "runs": []}
        data["runs"].append({"amount": amount, "profile": profile, "tag": tag, "tool": tool})
        # Recompute total as the Decimal sum of all runs (not an iterative float round),
        # so the stored total never drifts past the strict parser's tolerance (finding 9).
        _recompute_total(data)
        _atomic_write_json(f, data)


def _sum_runs(path: Path, tool: str) -> float:
    if not path.exists():
        return 0.0
    try:
        runs = json.loads(path.read_text()).get("runs", [])
    except (json.JSONDecodeError, ValueError):
        return 0.0
    # Records written before the tool field default to "council".
    return sum(float(r.get("amount", 0.0)) for r in runs if r.get("tool", "council") == tool)


def tool_total_for_day(on_date: date, tool: str) -> float:
    return _sum_runs(_daily_file(on_date), tool)


def tool_total_for_month(on_date: date, tool: str) -> float:
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    return sum(_sum_runs(f, tool) for f in _spend_dir().glob(f"{prefix}*.json"))


def preflight_tool(
    *, estimated: float, per_query_cap: float, daily_cap: float, monthly_cap: float,
    on_date: date, tool: str, force: bool = False,
) -> None:
    """Like preflight, but daily/monthly totals are scoped to one tool."""
    if not force and estimated > per_query_cap:
        raise BudgetExceeded(
            f"per-run cap exceeded: estimated ${estimated:.4f} > cap ${per_query_cap:.4f}. "
            f"Use --force to override (still subject to daily/monthly caps)."
        )
    today = tool_total_for_day(on_date, tool)
    if today + estimated > daily_cap:
        raise BudgetExceeded(
            f"{tool} daily cap would be exceeded: today=${today:.4f} + "
            f"estimated=${estimated:.4f} > daily_cap=${daily_cap:.4f}"
        )
    month = tool_total_for_month(on_date, tool)
    if month + estimated > monthly_cap:
        raise BudgetExceeded(
            f"{tool} monthly cap would be exceeded: month-to-date=${month:.4f} + "
            f"estimated=${estimated:.4f} > monthly_cap=${monthly_cap:.4f}"
        )


def preflight(
    *,
    estimated: float,
    per_query_cap: float,
    daily_cap: float,
    monthly_cap: float,
    on_date: date,
    force: bool = False,
) -> None:
    """Reject the query if any cap would be breached.

    `force=True` bypasses per-query cap (but still respects daily/monthly).
    Daily and monthly caps are NEVER bypassed.
    """
    if not force and estimated > per_query_cap:
        raise BudgetExceeded(
            f"per-query cap exceeded: estimated ${estimated:.4f} > cap ${per_query_cap:.4f}. "
            f"Use --force to override (still subject to daily/monthly caps)."
        )
    today_total = _read_total_for_day(on_date)
    if today_total + estimated > daily_cap:
        raise BudgetExceeded(
            f"daily cap would be exceeded: today=${today_total:.4f} + "
            f"estimated=${estimated:.4f} > daily_cap=${daily_cap:.4f}"
        )
    month_total = _read_total_for_month(on_date)
    if month_total + estimated > monthly_cap:
        raise BudgetExceeded(
            f"monthly cap would be exceeded: month-to-date=${month_total:.4f} + "
            f"estimated=${estimated:.4f} > monthly_cap=${monthly_cap:.4f}"
        )


# ---------------------------------------------------------------------------
# F8a.3 — canonical lock identity + locked reserve + crash-safe lifecycle
# ---------------------------------------------------------------------------


def _normalize_account_date(on_date) -> date:
    """Coerce to a plain calendar ``date`` or fail closed.

    ``datetime`` is a ``date`` subclass whose ``isoformat()`` is a timestamp — left as-is
    it would open a per-*instant* daily file that bypasses the calendar day's accumulated
    total (finding 1). Normalize a ``datetime`` to its UTC-agnostic calendar day; reject
    anything that is not a date at all (the-oracle derives the accounting date internally
    in UTC and passes a plain ``date``).
    """
    if isinstance(on_date, datetime):
        return on_date.date()
    if isinstance(on_date, date):
        return on_date
    raise TypeError("on_date must be a datetime.date")


def _resolve_root() -> Path:
    """Resolve the spend dir to an absolute realpath ONCE for a whole transaction.

    Pinning collapses symlink/relative/trailing-slash spellings AND freezes the root for
    the duration of the locked transaction, so a concurrent ``COUNCIL_SPEND_DIR``/cwd/
    symlink change cannot make the lock and the data files diverge (finding 3).
    """
    return Path(os.path.realpath(_spend_dir()))


def _daily_file_in(root: Path, on_date: date) -> Path:
    return root / f"council-spend-{on_date.isoformat()}.json"


def _month_files_in(root: Path, on_date: date) -> list:
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    return sorted(root.glob(f"{prefix}*.json"))


def month_lock_path(accounting_date: date, *, root: Path | None = None) -> Path:
    """Return the ONE canonical lock file for ``accounting_date``'s month.

    The path is the resolved absolute realpath of the spend dir (not the raw
    ``COUNCIL_SPEND_DIR``/symlink spelling — two spellings of one directory must
    collapse to the same lock file) over the MONTH kernel: the monthly cap spans every
    daily file in the ``YYYY-MM``, so serializing the whole month makes a monthly-total
    read + reservation write atomic. The lock keys on the *accounting month of the data
    row*, so any two writers touching the same monthly data set take the same lock
    regardless of their wall clocks. Pass a pre-resolved ``root`` to pin it for the whole
    transaction; ``check_and_reserve`` and the locked ``record_spend`` both do this, and
    F8b reuses the identical kernel.
    """
    accounting_date = _normalize_account_date(accounting_date)
    root = root if root is not None else _resolve_root()
    return root / f".council-spend-{accounting_date.strftime('%Y-%m')}.lock"


@contextlib.contextmanager
def month_lock(accounting_date: date, *, root: Path | None = None):
    """Hold an exclusive inter-process ``flock`` over the accounting month.

    Advisory (``fcntl.flock``); every mutation path in this module takes it. NEVER nest
    two acquisitions on one thread — separate open file descriptions would deadlock.
    """
    path = month_lock_path(accounting_date, root=root)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _atomic_write_json_fsync(path: Path, data: dict) -> None:
    """Atomically replace ``path`` and fsync both the file and its parent directory.

    Durability contract for the reservation lifecycle: a ``reserved``/``dispatched`` row
    must survive a crash (so the budget stays consumed until reconciliation), which
    requires the data to reach disk (file fsync) and the rename to be durable (parent-dir
    fsync) before we return — i.e. before the first network byte for ``dispatched``.
    """
    directory = path.parent
    fd, tmp_name = tempfile.mkstemp(dir=directory, prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    dir_fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def _to_decimal(value, *, field: str) -> Decimal:
    """Coerce a JSON money value to a finite, nonnegative ``Decimal`` or fail closed."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LedgerCorrupt(f"{field} must be a number, got {value!r}")
    try:
        dec = Decimal(str(value))
    except InvalidOperation as exc:
        raise LedgerCorrupt(f"{field} is not a valid decimal: {value!r}") from exc
    if not dec.is_finite():
        raise LedgerCorrupt(f"{field} must be finite, got {value!r}")
    if dec < 0:
        raise LedgerCorrupt(f"{field} must be nonnegative, got {value!r}")
    return dec


def _resolve_provenance(provenance: str | None, usage_cost: float | None) -> str:
    """Resolve and validate additive actual-cost provenance."""
    resolved = (
        "authoritative" if usage_cost is not None else "unknown"
    ) if provenance is None else provenance
    if resolved not in _PROVENANCE:
        raise ReservationError(
            f"provenance must be one of {_PROVENANCE!r}, got {provenance!r}"
        )
    if resolved in ("authoritative", "estimated") and usage_cost is None:
        raise ReservationError(f"{resolved} provenance requires a known usage_cost")
    if resolved == "unknown" and usage_cost is not None:
        raise ReservationError("unknown provenance requires usage_cost None")
    return resolved


@dataclass(frozen=True)
class _ParsedFile:
    aggregate: Decimal
    by_tool: dict
    reservation_ids: tuple
    attempt_ids: tuple


def _reject_duplicate_keys(pairs):
    """``object_pairs_hook`` that refuses duplicate JSON object keys (finding 6).

    Plain ``json.loads`` keeps the last value, so a tampered ledger with a second
    ``"runs"``/``"total"`` would parse as zero and hide spend. Strict enforcement rejects.
    """
    seen: dict = {}
    for key, value in pairs:
        if key in seen:
            raise LedgerCorrupt(f"duplicate JSON key {key!r}")
        seen[key] = value
    return seen


def _strict_parse_file(path: Path) -> _ParsedFile:
    """Strictly parse ONE daily file for enforcement — refuse on any anomaly.

    Refuses (never skips/zeroes): malformed JSON, duplicate JSON keys, a bool/unsupported
    ``schema_version``, an unparseable ``date``, an existing file missing ``runs``/``total``
    (truncation), non-finite/negative money, a reservation row missing ``tool``/``run_id``/
    ``status``/``reservation_id``, a stored ``total`` inconsistent with the summed runs
    (beyond a per-run micro tolerance), an illegal reservation ``status``, or a duplicate
    reservation/attempt id within the file. The reserved-cost ``amount`` is the debit for
    every run regardless of lifecycle status (``total`` is reserved-only).
    """
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return _ParsedFile(Decimal(0), {}, (), ())
    try:
        data = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except (json.JSONDecodeError, ValueError) as exc:
        raise LedgerCorrupt(f"{path.name}: malformed JSON") from exc
    if not isinstance(data, dict):
        raise LedgerCorrupt(f"{path.name}: top level is not an object")

    version = data.get("schema_version")
    if version is not None and (
        isinstance(version, bool) or version not in _SUPPORTED_SCHEMA_VERSIONS
    ):
        raise LedgerCorrupt(f"{path.name}: unsupported schema_version {version!r}")

    date_field = data.get("date")
    if date_field is not None:
        try:
            date.fromisoformat(date_field)
        except (TypeError, ValueError) as exc:
            raise LedgerCorrupt(f"{path.name}: invalid date {date_field!r}") from exc

    # An existing ledger file must carry both runs and total; their absence means a
    # truncated/incomplete write and MUST fail closed rather than read as zero (finding 4).
    if "runs" not in data:
        raise LedgerCorrupt(f"{path.name}: ledger missing runs")
    if "total" not in data:
        raise LedgerCorrupt(f"{path.name}: ledger missing total")
    runs = data["runs"]
    if not isinstance(runs, list):
        raise LedgerCorrupt(f"{path.name}: runs is not a list")

    aggregate = Decimal(0)
    by_tool: dict = {}
    reservation_ids: list = []
    for row in runs:
        if not isinstance(row, dict):
            raise LedgerCorrupt(f"{path.name}: a run is not an object")
        amount = _to_decimal(row.get("amount"), field=f"{path.name}: run amount")
        is_reservation = row.get("kind") == _RESERVATION_KIND
        if is_reservation and "tool" not in row:
            # A reservation charged to the legacy "council" default would vanish from its
            # real per-tool total and defeat the HARD per-tool cap (finding 5).
            raise LedgerCorrupt(f"{path.name}: reservation row missing tool")
        tool = row.get("tool", "council")
        if not isinstance(tool, str) or not tool:
            raise LedgerCorrupt(f"{path.name}: run tool must be a nonempty string")
        aggregate += amount
        by_tool[tool] = by_tool.get(tool, Decimal(0)) + amount
        if is_reservation:
            status = row.get("status")
            if status not in _LIFECYCLE_STATES:
                raise LedgerCorrupt(f"{path.name}: illegal reservation status {status!r}")
            rid = row.get("reservation_id")
            if not isinstance(rid, str) or not rid:
                raise LedgerCorrupt(f"{path.name}: reservation missing reservation_id")
            run_id = row.get("run_id")
            if not isinstance(run_id, str) or not run_id:
                raise LedgerCorrupt(f"{path.name}: reservation missing run_id")
            reservation_ids.append(rid)

    if len(set(reservation_ids)) != len(reservation_ids):
        raise LedgerCorrupt(f"{path.name}: duplicate reservation_id")

    stored = _to_decimal(data["total"], field=f"{path.name}: total")
    # Legacy files written by the old iterative round(...,6) can drift up to a micro per
    # run; tolerate that band while still catching gross tampering (finding 9).
    tolerance = _MICRO * max(1, len(runs))
    if abs(stored - aggregate) > tolerance:
        raise LedgerCorrupt(
            f"{path.name}: total {stored} inconsistent with summed runs {aggregate}"
        )

    actuals = data.get("actuals", [])
    if not isinstance(actuals, list):
        raise LedgerCorrupt(f"{path.name}: actuals is not a list")
    attempt_ids: list = []
    for act in actuals:
        if not isinstance(act, dict):
            raise LedgerCorrupt(f"{path.name}: an actual is not an object")
        aid = act.get("attempt_id")
        if aid is not None:
            attempt_ids.append(aid)
        cost = act.get("usage_cost")
        if cost is not None:
            _to_decimal(cost, field=f"{path.name}: usage_cost")
        if "provenance" in act and act["provenance"] not in _PROVENANCE:
            raise LedgerCorrupt(
                f"{path.name}: invalid actual provenance {act['provenance']!r}"
            )
    if len(set(attempt_ids)) != len(attempt_ids):
        raise LedgerCorrupt(f"{path.name}: duplicate attempt_id")

    return _ParsedFile(aggregate, by_tool, tuple(reservation_ids), tuple(attempt_ids))


def strict_ledger_state(accounting_date: date, *, root: Path | None = None) -> dict:
    """Fail-closed per-tool and aggregate totals for the day and month of ``accounting_date``.

    Enforcement-only: refuses a corrupt ledger (``LedgerCorrupt``) rather than
    under-counting and admitting a cap-breaking run. Callers MUST hold ``month_lock``.
    Pass a pinned ``root`` (as ``check_and_reserve`` does) so the read cannot race a
    concurrent spend-root change.
    """
    accounting_date = _normalize_account_date(accounting_date)
    root = root if root is not None else _resolve_root()
    day_parsed = _strict_parse_file(_daily_file_in(root, accounting_date))
    month_agg = Decimal(0)
    month_by_tool: dict = {}
    all_reservation_ids: list = []
    all_attempt_ids: list = []
    for path in _month_files_in(root, accounting_date):
        parsed = _strict_parse_file(path)
        month_agg += parsed.aggregate
        for tool, amt in parsed.by_tool.items():
            month_by_tool[tool] = month_by_tool.get(tool, Decimal(0)) + amt
        all_reservation_ids.extend(parsed.reservation_ids)
        all_attempt_ids.extend(parsed.attempt_ids)
    if len(set(all_reservation_ids)) != len(all_reservation_ids):
        raise LedgerCorrupt("duplicate reservation_id across the accounting month")
    if len(set(all_attempt_ids)) != len(all_attempt_ids):
        raise LedgerCorrupt("duplicate attempt_id across the accounting month")
    return {
        "day": {"aggregate": day_parsed.aggregate, "by_tool": dict(day_parsed.by_tool)},
        "month": {"aggregate": month_agg, "by_tool": month_by_tool},
        "reservation_ids": set(all_reservation_ids),
        "attempt_ids": set(all_attempt_ids),
    }


@dataclass(frozen=True)
class Reservation:
    """Handle to a durable reservation row; carries what the lifecycle helpers need."""
    reservation_id: str
    run_id: str
    tool: str
    amount: float
    on_date: date


def _load_daily_in(root: Path, on_date: date) -> dict:
    f = _daily_file_in(root, on_date)
    if f.exists():
        data = json.loads(f.read_text())
    else:
        data = {"date": on_date.isoformat(), "total": 0.0, "runs": []}
    data.setdefault("runs", [])
    data.setdefault("actuals", [])
    return data


def _recompute_total(data: dict) -> None:
    total = sum((_to_decimal(r.get("amount"), field="run amount") for r in data["runs"]), Decimal(0))
    data["total"] = float(total)


def check_and_reserve(
    *,
    reserved_cost: float,
    tool: str,
    tag: str,
    profile: str,
    run_id: str,
    on_date: date,
    per_query_cap: float,
    tool_daily_cap: float,
    tool_monthly_cap: float,
    aggregate_daily_cap: float,
    aggregate_monthly_cap: float,
    reservation_id: str | None = None,
    policy_version=None,
    policy_hash=None,
    force: bool = False,
) -> Reservation:
    """One locked transaction: strict-check the caps, then durably reserve.

    Under the canonical month lock (over a spend root pinned once for the whole
    transaction): strict-parse the ledger (fail closed on corruption), enforce the
    per-tool per-query/daily/monthly caps and the cross-tool aggregate daily/monthly
    ceiling, then write a durable ``reserved`` row (atomic rename + fsync of file and
    parent dir). ``force=True`` skips ONLY the per-query comparison when policy permits;
    it still debits the full reserved cost. Daily and monthly caps are NEVER bypassed.
    The reserved cost is the sole enforcement debit.
    """
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("run_id must be a nonblank string")
    on_date = _normalize_account_date(on_date)
    # Quantize the reserved cost UP to the ledger micro before comparing to caps, so a
    # float-noise value fractionally over a cap can never slip through (finding 10) and
    # the stored debit never rounds below its bound.
    cost = _to_decimal(reserved_cost, field="reserved_cost").quantize(_MICRO, rounding=ROUND_CEILING)
    rid = reservation_id or uuid.uuid4().hex
    root = _resolve_root()
    with month_lock(on_date, root=root):
        if POLICY_ENFORCEMENT_ENABLED:
            # Lazy import keeps budget <-> policy import-safe. The activation snapshot is
            # enforcement state and must be read from this transaction's pinned shared
            # root while the canonical month lock is held.
            from council import policy

            active = policy.load_active_policy(root)
            if active is not None:
                active_version = active["policy_version"]
                active_hash = active["policy_hash"]
                if policy_version is None and policy_hash is None:
                    policy_version = active_version
                    policy_hash = active_hash
                elif policy_version is None or policy_hash is None:
                    raise ReservationError(
                        "both policy_version and policy_hash are required when either is supplied"
                    )
                else:
                    # True == 1 in Python: exact-type checks must precede the equality
                    # comparison or a boolean version launders through (review finding 1).
                    if isinstance(policy_version, bool) or not isinstance(policy_version, int):
                        raise ReservationError("policy_version must be an integer")
                    if not isinstance(policy_hash, str):
                        raise ReservationError("policy_hash must be a string")
                    if policy_version != active_version or policy_hash != active_hash:
                        raise ReservationError(
                            f"caller policy does not match active policy version {active_version} "
                            f"hash {active_hash}"
                        )

                active_tools = active["policy"]["tools"]
                if tool not in active_tools:
                    raise ReservationError(f"tool {tool!r} is not in active policy")
                active_tool = active_tools[tool]
                if force and not active_tool["force_per_query_allowed"]:
                    raise ReservationError(
                        f"force is not allowed for tool {tool!r} by the active policy"
                    )

                requested_per_query = _to_decimal(per_query_cap, field="per_query_cap")
                active_per_query = {
                    Decimal(str(value)) for value in active_tool["per_query_caps"]
                }
                if requested_per_query not in active_per_query:
                    raise ReservationError(
                        f"per_query_cap drift: {per_query_cap!r} is not in activated "
                        f"per_query_caps {active_tool['per_query_caps']!r}"
                    )

                cap_pairs = (
                    ("tool_daily_cap", tool_daily_cap, active_tool["daily_cap"]),
                    ("tool_monthly_cap", tool_monthly_cap, active_tool["monthly_cap"]),
                    (
                        "aggregate_daily_cap",
                        aggregate_daily_cap,
                        active["policy"]["aggregate"]["daily_cap"],
                    ),
                    (
                        "aggregate_monthly_cap",
                        aggregate_monthly_cap,
                        active["policy"]["aggregate"]["monthly_cap"],
                    ),
                )
                for field, supplied, activated in cap_pairs:
                    if _to_decimal(supplied, field=field) != Decimal(str(activated)):
                        raise ReservationError(
                            f"{field} drift: caller {supplied!r} != activated {activated!r}"
                        )

                # Admission always uses the activated snapshot. The caller chooses one
                # enumerated per-query tier; every other cap has exactly one active value.
                per_query_cap = float(requested_per_query)
                tool_daily_cap = active_tool["daily_cap"]
                tool_monthly_cap = active_tool["monthly_cap"]
                aggregate_daily_cap = active["policy"]["aggregate"]["daily_cap"]
                aggregate_monthly_cap = active["policy"]["aggregate"]["monthly_cap"]

        state = strict_ledger_state(on_date, root=root)
        if rid in state["reservation_ids"]:
            raise ReservationError(f"reservation_id {rid!r} already exists")
        if not force and cost > _to_decimal(per_query_cap, field="per_query_cap"):
            raise BudgetExceeded(
                f"per-query cap exceeded: reserved ${cost} > cap ${per_query_cap}"
            )
        tool_day = state["day"]["by_tool"].get(tool, Decimal(0))
        if tool_day + cost > _to_decimal(tool_daily_cap, field="tool_daily_cap"):
            raise BudgetExceeded(
                f"{tool} daily cap would be exceeded: day=${tool_day} + reserved=${cost} "
                f"> daily_cap=${tool_daily_cap}"
            )
        tool_month = state["month"]["by_tool"].get(tool, Decimal(0))
        if tool_month + cost > _to_decimal(tool_monthly_cap, field="tool_monthly_cap"):
            raise BudgetExceeded(
                f"{tool} monthly cap would be exceeded: month=${tool_month} + "
                f"reserved=${cost} > monthly_cap=${tool_monthly_cap}"
            )
        agg_day = state["day"]["aggregate"]
        if agg_day + cost > _to_decimal(aggregate_daily_cap, field="aggregate_daily_cap"):
            raise BudgetExceeded(
                f"aggregate daily ceiling would be exceeded: day=${agg_day} + "
                f"reserved=${cost} > aggregate_daily_cap=${aggregate_daily_cap}"
            )
        agg_month = state["month"]["aggregate"]
        if agg_month + cost > _to_decimal(aggregate_monthly_cap, field="aggregate_monthly_cap"):
            raise BudgetExceeded(
                f"aggregate monthly ceiling would be exceeded: month=${agg_month} + "
                f"reserved=${cost} > aggregate_monthly_cap=${aggregate_monthly_cap}"
            )

        data = _load_daily_in(root, on_date)
        data["schema_version"] = LEDGER_SCHEMA_VERSION
        data["runs"].append({
            "amount": float(cost),
            "profile": profile,
            "tag": tag,
            "tool": tool,
            "kind": _RESERVATION_KIND,
            "reservation_id": rid,
            "run_id": run_id,
            "status": _RESERVED,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "policy_version": policy_version,
            "policy_hash": policy_hash,
        })
        _recompute_total(data)
        _atomic_write_json_fsync(_daily_file_in(root, on_date), data)
    return Reservation(reservation_id=rid, run_id=run_id, tool=tool, amount=float(cost), on_date=on_date)


def _find_reservation_row(data: dict, reservation_id: str) -> dict:
    for row in data["runs"]:
        if row.get("kind") == _RESERVATION_KIND and row.get("reservation_id") == reservation_id:
            return row
    raise ReservationError(f"reservation {reservation_id} not found")


def _transition(reservation: Reservation, *, expected, new_status: str) -> None:
    on_date = _normalize_account_date(reservation.on_date)
    root = _resolve_root()
    with month_lock(on_date, root=root):
        _strict_parse_file(_daily_file_in(root, on_date))  # fail closed before mutating
        data = _load_daily_in(root, on_date)
        row = _find_reservation_row(data, reservation.reservation_id)
        if row["status"] != expected:
            raise ReservationError(
                f"illegal transition {row['status']} -> {new_status} "
                f"(expected current status {expected})"
            )
        row["status"] = new_status
        _atomic_write_json_fsync(_daily_file_in(root, on_date), data)


def mark_dispatched(reservation: Reservation) -> None:
    """Transition ``reserved -> dispatched`` and fsync BEFORE the first network byte.

    A crash after this point leaves a durable ``dispatched`` debit that startup
    reconciliation retains as ``unknown`` — the budget stays consumed, never under-counts.
    """
    _transition(reservation, expected=_RESERVED, new_status=_DISPATCHED)


def settle(
    reservation: Reservation,
    *,
    attempt_id: str,
    generation_id: str | None,
    usage_cost: float | None,
    status: str = _SETTLED,
    provenance: str | None = None,
) -> None:
    """Terminal ``dispatched -> settled | unknown``; record the NON-debit actual.

    ``usage.cost`` is stored in ``actuals`` keyed by ``run_id``+``attempt_id`` and never
    debits ``amount``/``total``. Terminal ``unknown`` retains the reservation debit
    (``usage_cost=None``); refund only on affirmative provider evidence of no charge.
    """
    if status not in (_SETTLED, _UNKNOWN):
        raise ReservationError(f"settle status must be settled|unknown, got {status!r}")
    if status == _UNKNOWN and usage_cost is not None:
        raise ReservationError("an unknown actual must carry usage_cost None")
    resolved_provenance = _resolve_provenance(provenance, usage_cost)
    if status == _SETTLED and resolved_provenance != "authoritative":
        raise ReservationError(
            "cannot settle settled with non-authoritative provenance — use unknown"
        )
    on_date = _normalize_account_date(reservation.on_date)
    root = _resolve_root()
    with month_lock(on_date, root=root):
        parsed = _strict_parse_file(_daily_file_in(root, on_date))
        if attempt_id in parsed.attempt_ids:
            raise ReservationError(f"attempt_id {attempt_id!r} already recorded")
        data = _load_daily_in(root, on_date)
        row = _find_reservation_row(data, reservation.reservation_id)
        if row["status"] != _DISPATCHED:
            raise ReservationError(
                f"illegal transition {row['status']} -> {status} (expected dispatched)"
            )
        row["status"] = status
        if usage_cost is not None:
            _to_decimal(usage_cost, field="usage_cost")
        data.setdefault("actuals", []).append({
            "reservation_id": reservation.reservation_id,
            "run_id": reservation.run_id,
            "attempt_id": attempt_id,
            "generation_id": generation_id,
            "usage_cost": usage_cost,
            "status": status,
            "provenance": resolved_provenance,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        })
        _atomic_write_json_fsync(_daily_file_in(root, on_date), data)


def reconcile_stale(accounting_date: date, *, older_than: datetime | None = None) -> list:
    """Startup reconciliation under the lock: retain crash-orphaned reservations.

    Any ``reserved``/``dispatched`` row left by a crash becomes terminal ``unknown`` and
    KEEPS its debit (consumed budget >= the retained reservation). A refund requires
    affirmative provider evidence of no charge — the generation-id reconciliation query is
    deferred to just before F8a.4, so F8a.3 conservatively retains.

    ``older_than`` guards against clobbering a *live* dispatch owned by another process
    (finding 8): only rows whose ``created_at`` predates the cutoff are reconciled. The
    single-user sequential model calls this at startup before any in-flight dispatch;
    cross-process liveness is F8b. A row with an unparseable/absent ``created_at`` is
    reconciled (conservative retain).
    """
    accounting_date = _normalize_account_date(accounting_date)
    root = _resolve_root()
    with month_lock(accounting_date, root=root):
        _strict_parse_file(_daily_file_in(root, accounting_date))
        data = _load_daily_in(root, accounting_date)
        reconciled = []
        for row in data["runs"]:
            if row.get("kind") != _RESERVATION_KIND or row.get("status") not in _NONTERMINAL:
                continue
            if older_than is not None:
                created = row.get("created_at")
                created_dt = None
                if isinstance(created, str):
                    try:
                        created_dt = datetime.fromisoformat(created)
                    except ValueError:
                        created_dt = None
                if created_dt is not None and created_dt >= older_than:
                    continue  # too new — a live dispatch, not a crash orphan
            row["status"] = _UNKNOWN
            reconciled.append(row["reservation_id"])
        if reconciled:
            _atomic_write_json_fsync(_daily_file_in(root, accounting_date), data)
        return reconciled


def record_actual(
    reservation: Reservation,
    *,
    attempt_id: str,
    generation_id: str | None,
    usage_cost: float | None,
    status: str = _SETTLED,
    provenance: str | None = None,
) -> None:
    """Append ONE non-debit per-attempt actual; DO NOT transition the reservation.

    The council/retrieval graphs run many attempts under one reservation (F8a.4). Each
    attempt's ``usage.cost``+``generation_id`` is recorded as its own ``actuals`` row so
    per-generation truth survives — a failed-but-billed attempt is never laundered into an
    aggregate zero — and ``reserved >= sum(actual)`` stays checkable per graph. The
    reservation stays ``dispatched``; the single terminal transition is ``close`` (or
    ``settle`` for the atomic single-attempt seams). ``usage.cost`` NEVER debits
    ``amount``/``total``. ``attempt_id`` must be unique within the day, matching ``settle``.
    """
    if status not in (_SETTLED, _UNKNOWN):
        raise ReservationError(f"actual status must be settled|unknown, got {status!r}")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ReservationError(f"attempt_id must be a nonblank string, got {attempt_id!r}")
    if generation_id is not None and (not isinstance(generation_id, str) or not generation_id):
        raise ReservationError(
            f"generation_id must be None or a nonblank string, got {generation_id!r}"
        )
    # settled <-> a KNOWN cost; unknown <-> no usable cost. Never mislabel one as the other,
    # or a null-cost "settled" row would falsely assert a fully-accounted attempt.
    if status == _SETTLED and usage_cost is None:
        raise ReservationError("a settled actual requires a known usage_cost (got None)")
    if status == _UNKNOWN and usage_cost is not None:
        raise ReservationError("an unknown actual must carry usage_cost None")
    resolved_provenance = _resolve_provenance(provenance, usage_cost)
    on_date = _normalize_account_date(reservation.on_date)
    root = _resolve_root()
    with month_lock(on_date, root=root):
        parsed = _strict_parse_file(_daily_file_in(root, on_date))
        if attempt_id in parsed.attempt_ids:
            raise ReservationError(f"attempt_id {attempt_id!r} already recorded")
        data = _load_daily_in(root, on_date)
        row = _find_reservation_row(data, reservation.reservation_id)
        if row["status"] != _DISPATCHED:
            raise ReservationError(
                f"cannot record an actual against a {row['status']!r} reservation "
                "(expected dispatched)"
            )
        if usage_cost is not None:
            _to_decimal(usage_cost, field="usage_cost")
        data.setdefault("actuals", []).append({
            "reservation_id": reservation.reservation_id,
            "run_id": reservation.run_id,
            "attempt_id": attempt_id,
            "generation_id": generation_id,
            "usage_cost": usage_cost,
            "status": status,
            "provenance": resolved_provenance,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        })
        _atomic_write_json_fsync(_daily_file_in(root, on_date), data)


def close(reservation: Reservation, *, status: str) -> None:
    """Terminal ``dispatched -> settled | unknown`` transition WITHOUT recording an actual.

    For the multi-attempt seams whose per-attempt actuals were already written via
    ``record_actual``: ``close`` performs only the single terminal transition, preserving
    ``settle``'s one-terminal-transition invariant. ``unknown`` retains the reservation
    debit (refund only on affirmative provider no-charge evidence). A fully failed graph
    (zero surviving attempts, zero actuals) closes ``unknown`` and keeps its debit.
    """
    if status not in (_SETTLED, _UNKNOWN):
        raise ReservationError(f"close status must be settled|unknown, got {status!r}")
    on_date = _normalize_account_date(reservation.on_date)
    root = _resolve_root()
    with month_lock(on_date, root=root):
        _strict_parse_file(_daily_file_in(root, on_date))  # fail closed before mutating
        data = _load_daily_in(root, on_date)
        row = _find_reservation_row(data, reservation.reservation_id)
        if row["status"] != _DISPATCHED:
            raise ReservationError(
                f"illegal transition {row['status']} -> {status} (expected dispatched)"
            )
        if status == _SETTLED:
            # ``settled`` asserts the graph is FULLY accounted: at least one actual, and none
            # of this reservation's actuals left unknown/null. A zero-actual or any-unknown
            # graph closes ``unknown`` — never launder a possibly-billed graph into a clean
            # settled/no-cost terminal that reconcile_stale will not revisit.
            own = [
                a for a in data.get("actuals", [])
                if a.get("reservation_id") == reservation.reservation_id
            ]
            if not own:
                raise ReservationError("cannot close settled with zero actuals — use unknown")
            if any(
                a.get("status") != _SETTLED
                or a.get("usage_cost") is None
                or a.get("provenance", "authoritative") != "authoritative"
                for a in own
            ):
                raise ReservationError(
                    "cannot close settled while an actual is unknown/uncosted/"
                    "non-authoritative — use unknown"
                )
        row["status"] = status
        _atomic_write_json_fsync(_daily_file_in(root, on_date), data)


@dataclass(frozen=True)
class ReconcileResult:
    """Outcome of reconciling ledger actuals against authoritative provider records.

    ``reconciled_total`` is the provider-authoritative billed sum (matched + unaccounted) —
    the honest figure the ``reserved >= actual`` cross-check uses. Unresolved attempts stay
    ``unknown`` (never zero) and contribute nothing to the total.
    """
    reconciled_total: Decimal
    resolved: list      # ledger null-cost filled from provider truth
    confirmed: list     # ledger cost == provider cost
    corrected: list     # ledger cost != provider cost (provider authoritative)
    unaccounted: list   # provider generation with NO ledger actual (failed-but-billed)
    unresolved: list    # ledger actual with no usable provider cost — stays unknown


def _reconcile_money(value, *, field: str) -> Decimal:
    """Coerce a reconciliation money value to a finite, nonnegative ``Decimal`` or fail
    closed. Accepts ``Decimal`` (as well as the ledger's JSON int/float) so the helper's own
    ``reconciled_cost`` output can be fed back unchanged in an idempotent replay."""
    if isinstance(value, Decimal):
        dec = value
    elif isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LedgerCorrupt(f"{field} must be a number, got {value!r}")
    else:
        try:
            dec = Decimal(str(value))
        except InvalidOperation as exc:
            raise LedgerCorrupt(f"{field} is not a valid decimal: {value!r}") from exc
    if not dec.is_finite():
        raise LedgerCorrupt(f"{field} must be finite, got {value!r}")
    if dec < 0:
        raise LedgerCorrupt(f"{field} must be nonnegative, got {value!r}")
    return dec


def reconcile_generations(actuals, provider_records) -> ReconcileResult:
    """Idempotent reconciliation of ledger actuals against provider generation truth.

    Keyed by ``generation_id``; the provider is authoritative for what was billed:
      * ledger cost null  + provider cost       -> resolved (filled from provider)
      * ledger cost == provider cost            -> confirmed (exact Decimal equality)
      * ledger cost != provider cost            -> corrected (provider wins)
      * provider generation with NO ledger row  -> unaccounted (failed-but-billed)
      * ledger row with no usable provider cost -> unresolved (stays unknown, never zero)

    ``reconciled_total`` sums provider truth over every matched + unaccounted generation.
    Pure: no ledger mutation and no network (provider records are injected), so re-running
    on the resolved ledger yields the identical total — idempotent by construction. Corrupt
    ledger money / ids fail closed (``LedgerCorrupt``) rather than pass as a silent zero.
    """
    provider: dict = {}
    for gen_id, cost in dict(provider_records).items():
        provider[gen_id] = None if cost is None else _reconcile_money(cost, field="provider usage_cost")

    # The billed total is provider truth, counted ONCE per generation — independent of how
    # many (or how few) ledger rows reference it. Summing per-ledger-row would double-count a
    # duplicated generation_id, and a doubled cost total is dangerously-wrong.
    total = sum((c for c in provider.values() if c is not None), Decimal(0))

    resolved: list = []
    confirmed: list = []
    corrected: list = []
    unresolved: list = []
    matched: set = set()
    seen: set = set()  # every generation_id present in a ledger row (usable cost or not)

    for act in actuals:
        gen_id = act.get("generation_id")
        attempt_id = act.get("attempt_id")
        ledger_cost = act.get("usage_cost")
        if gen_id is not None and (not isinstance(gen_id, str) or not gen_id):
            raise LedgerCorrupt(
                f"actual generation_id must be None or a nonblank string, got {gen_id!r}"
            )
        # Validate ledger money UP FRONT so a corrupt cost fails closed even when there is no
        # provider truth to compare against — never silently pass as an unresolved zero.
        ledger_dec = None if ledger_cost is None else _reconcile_money(ledger_cost, field="ledger usage_cost")
        if gen_id is not None:
            seen.add(gen_id)
        prov_cost = provider.get(gen_id) if gen_id is not None else None
        if gen_id is None or gen_id not in provider or prov_cost is None:
            # No usable provider truth for this row → stays unknown, never zeroed.
            unresolved.append({"attempt_id": attempt_id, "generation_id": gen_id})
            continue
        matched.add(gen_id)
        entry = {"attempt_id": attempt_id, "generation_id": gen_id, "reconciled_cost": prov_cost}
        if ledger_dec is None:
            resolved.append(entry)
        elif ledger_dec == prov_cost:
            confirmed.append(entry)
        else:
            corrected.append(entry)

    unaccounted: list = []
    for gen_id, prov_cost in provider.items():
        if gen_id in seen:
            # The ledger already holds a row for this generation — its disposition was decided
            # in the actuals loop (matched or unresolved). Don't emit a phantom duplicate.
            continue
        if prov_cost is None:
            # Provider knows the generation but reports no cost yet → stays unknown.
            unresolved.append({"attempt_id": None, "generation_id": gen_id})
            continue
        unaccounted.append({"generation_id": gen_id, "reconciled_cost": prov_cost})

    return ReconcileResult(
        reconciled_total=total,
        resolved=resolved,
        confirmed=confirmed,
        corrected=corrected,
        unaccounted=unaccounted,
        unresolved=unresolved,
    )
