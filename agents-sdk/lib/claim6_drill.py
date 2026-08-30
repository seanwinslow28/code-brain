"""ADR-12 claim-6 drill records and schedule reconciliation."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Mapping


DRILL_SCHEMA_VERSION = 1
DRILL_EVENTS = frozenset(
    {
        "scheduled",
        "send_accepted",
        "acknowledged",
        "send_failed",
        "expired_unacknowledged",
        "receipt_poll_failed",
    }
)
_REQUIRED_BASE_FIELDS = frozenset(
    {
        "schema_version",
        "record_type",
        "drill_id",
        "drill_event",
        "occurred_at",
        "scheduled_for",
        "launchd_label",
        "writer_build",
    }
)
_INCIDENT_ONLY_FIELDS = frozenset(
    {"incident_id", "severity", "verified_restored_at"}
)


class DrillRecordError(ValueError):
    """Raised when a row violates the drill-only ADR-12 schema."""


def _incident_only_key(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            compact = normalized.replace("_", "")
            if normalized in _INCIDENT_ONLY_FIELDS or normalized.startswith(
                "restore_verification"
            ) or compact.startswith("restoreverification"):
                return str(key)
            found = _incident_only_key(child)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for child in value:
            found = _incident_only_key(child)
            if found:
                return found
    return None


def validate_drill_record(record: Mapping[str, Any]) -> None:
    """Validate the common, closed drill-record contract before append."""
    incident_key = _incident_only_key(record)
    if incident_key:
        raise DrillRecordError(
            f"incident-only field forbidden in drill record: {incident_key}"
        )
    missing = sorted(_REQUIRED_BASE_FIELDS - record.keys())
    if missing:
        raise DrillRecordError(f"missing required drill fields: {missing}")
    if record["schema_version"] != DRILL_SCHEMA_VERSION:
        raise DrillRecordError("unsupported drill schema_version")
    if record["record_type"] != "drill":
        raise DrillRecordError("record_type must be 'drill'")
    if record["drill_event"] not in DRILL_EVENTS:
        raise DrillRecordError(f"unknown drill_event: {record['drill_event']!r}")
    if record["drill_event"] == "send_accepted":
        required = {"request", "receipt", "delivery_row_id"}
        missing_send = sorted(required - record.keys())
        expected_transport = {
            "alerts": 1,
            "attempted": True,
            "delivered": True,
            "probe": "not-run",
            "dry_run": False,
        }
        mismatched = {
            key: record.get(key)
            for key, expected in expected_transport.items()
            if record.get(key) != expected
        }
        if missing_send or mismatched:
            raise DrillRecordError(
                "send_accepted requires request, receipt, delivery_row_id and "
                f"the B3 transport shape; missing={missing_send}, bad={mismatched}"
            )
    if record["drill_event"] == "acknowledged":
        required_ack = {
            "receipt",
            "delivery_row_id",
            "acknowledged",
            "acknowledged_at",
            "acknowledged_by_device",
            "registered_device",
        }
        missing_ack = sorted(required_ack - record.keys())
        qualifies = (
            record.get("acknowledged") == 1
            and record.get("acknowledged_at") not in (None, 0, "", "0")
            and bool(record.get("registered_device"))
            and record.get("acknowledged_by_device") == record.get("registered_device")
        )
        if missing_ack or not qualifies:
            raise DrillRecordError(
                "acknowledged event requires qualifying acknowledgment=1, nonzero "
                "acknowledged_at, and the registered device"
            )
    if record["drill_event"] == "send_failed":
        required_failure = {
            "alerts",
            "attempted",
            "delivered",
            "probe",
            "dry_run",
            "error",
        }
        expected_failure = {
            "alerts": 1,
            "attempted": True,
            "delivered": False,
            "probe": "not-run",
            "dry_run": False,
        }
        missing_failure = sorted(required_failure - record.keys())
        bad_failure = {
            key: record.get(key)
            for key, expected in expected_failure.items()
            if record.get(key) != expected
        }
        if missing_failure or bad_failure:
            raise DrillRecordError(
                f"send_failed requires retained failed-transport evidence; missing={missing_failure}, bad={bad_failure}"
            )
    if record["drill_event"] == "receipt_poll_failed":
        required_poll_failure = {"receipt", "delivery_row_id", "error"}
        missing_poll_failure = sorted(required_poll_failure - record.keys())
        if missing_poll_failure:
            raise DrillRecordError(
                "receipt_poll_failed requires retained receipt, delivery link, and "
                f"error; missing={missing_poll_failure}"
            )
    if record["drill_event"] == "expired_unacknowledged":
        required_expiry = {
            "receipt",
            "delivery_row_id",
            "negative_reason",
            "acknowledged",
            "acknowledged_at",
            "acknowledged_by_device",
            "expired",
            "last_delivered_at",
        }
        missing_expiry = sorted(required_expiry - record.keys())
        if missing_expiry:
            raise DrillRecordError(
                "expired_unacknowledged requires retained provider and negative "
                f"evidence; missing={missing_expiry}"
            )


def append_drill_record(path: Path, record: Mapping[str, Any]) -> None:
    """Append one validated row to the Phase-0 drill-only JSONL authority."""
    validate_drill_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(dict(record), sort_keys=True, separators=(",", ":")))
        stream.write("\n")


def _typed_block(status: str, means: str, next_step: str) -> str:
    return (
        "## Claim-6 Drill\n\n"
        f"- **Status:** {status}\n"
        f"- **Means:** {means}\n"
        f"- **Does not mean / Next:** {next_step}\n"
    )


def _rows_for_slot(
    path: Path, *, scheduled_for: datetime, launchd_label: str
) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                validate_drill_record(row)
                row_slot = datetime.fromisoformat(str(row["scheduled_for"]))
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise DrillRecordError(
                    f"unreadable drill row at source line {line_number}: {exc}"
                ) from exc
            if (
                row.get("launchd_label") == launchd_label
                and (row_slot.year, row_slot.month, row_slot.day, row_slot.hour, row_slot.minute)
                == (
                    scheduled_for.year,
                    scheduled_for.month,
                    scheduled_for.day,
                    scheduled_for.hour,
                    scheduled_for.minute,
                )
            ):
                rows.append(row)
    return rows


def render_drill_report_block(
    *, config: Mapping[str, Any], log_path: Path, now: datetime
) -> str:
    """Render ADR-12's retained three-line report surface."""
    enabled = bool(config.get("schedule_enabled", False))
    day = int(config.get("day_of_month", 0))
    label = str(config.get("launchd_label", ""))
    device = str(config.get("acknowledged_device", ""))
    if not enabled or not 1 <= day <= 31 or not label or not device:
        return _typed_block(
            "DRILL NOT REGISTERED — SCHEDULE NOT ARMED",
            "No monthly claim-6 fire is currently expected.",
            "This does not qualify B3; register day, launchd label, and device, then deploy the schedule.",
        )

    hour = int(config.get("hour", 8))
    minute = int(config.get("minute", 15))
    grace_minutes = int(config.get("grace_minutes", 30))
    if now.day != day:
        return _typed_block(
            f"DRILL NOT DUE TODAY — NEXT MONTHLY SLOT IS DAY {day} AT {hour:02d}:{minute:02d}",
            "The registered monthly occurrence is not today.",
            "This is not missed-fire evidence; inspect this block on the registered drill day.",
        )

    scheduled_for = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    grace_at = scheduled_for + timedelta(minutes=grace_minutes)
    try:
        rows = _rows_for_slot(
            log_path, scheduled_for=scheduled_for, launchd_label=label
        )
    except (OSError, DrillRecordError) as exc:
        return _typed_block(
            "DRILL RECORD READ FAILED — RECONCILIATION COULD NOT COMPLETE",
            f"The meta-agent could not read retained drill evidence: {str(exc)[:240]}",
            "This is not acknowledgment or a clean miss; repair the vault record path before B3 can qualify.",
        )

    scheduled_rows = [row for row in rows if row.get("drill_event") == "scheduled"]
    if not scheduled_rows:
        if now >= grace_at:
            return _typed_block(
                "DRILL FIRE MISSING — SCHEDULED EXECUTION NOT OBSERVED",
                "The registered 08:15 occurrence has no retained scheduled row after its grace instant.",
                "This does not isolate Pushover; check Mini, launchd, runner, and vault writes, then reset B3.",
            )
        return _typed_block(
            "DRILL FIRE PENDING — GRACE WINDOW OPEN",
            "The registered slot is due today and its scheduled row is not yet late.",
            "This is not success; reconcile again after the grace instant.",
        )

    latest = rows[-1]
    event = latest.get("drill_event")
    if event == "acknowledged":
        return _typed_block(
            "DRILL ACKNOWLEDGED — REGISTERED DEVICE CONFIRMED",
            "The scheduled send has a linked qualifying receipt acknowledgment.",
            "This proves one drill acknowledgment, not ordinary-alert or restore-path reliability.",
        )
    if event == "send_failed":
        return _typed_block(
            "DRILL SEND FAILED — NEGATIVE EVIDENCE RETAINED",
            "The scheduled runner attempted the send and retained delivered=false.",
            "This is not unmeasured; repair the send path and reset B3.",
        )
    if event == "receipt_poll_failed":
        return _typed_block(
            "DRILL RECEIPT READ FAILED — NEGATIVE EVIDENCE RETAINED",
            "Provider acceptance exists but receipt acknowledgment could not be read.",
            "Transport acceptance is not acknowledgment; repair receipt reads and reset B3.",
        )
    if event == "expired_unacknowledged":
        reason = str(latest.get("negative_reason", "unacknowledged"))
        return _typed_block(
            "DRILL EXPIRED UNACKNOWLEDGED — NEGATIVE EVIDENCE RETAINED",
            f"No qualifying registered-device acknowledgment exists ({reason}).",
            "Provider delivery facts are not acknowledgment; reset B3 after the cause is corrected.",
        )
    return _typed_block(
        "DRILL SEND INCOMPLETE — TERMINAL RECEIPT STATE NOT RETAINED",
        "The scheduled row exists, but the lifecycle has not reached a qualifying terminal record.",
        "Provider acceptance alone is not acknowledgment; inspect the runner before B3 can qualify.",
    )
