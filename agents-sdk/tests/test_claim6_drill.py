"""ADR-12 claim-6 drill runner and record contract."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from agents.claim6_drill import (
    DrillConfig,
    run_production_drill,
    run_test_drill,
    validate_production_provenance,
)
from lib.claim6_drill import append_drill_record, render_drill_report_block


def _scheduled_record(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "schema_version": 1,
        "record_type": "drill",
        "drill_id": "claim6-2026-09-03T0815",
        "drill_event": "scheduled",
        "occurred_at": "2026-09-03T08:15:00-04:00",
        "scheduled_for": "2026-09-03T08:15:00-04:00",
        "launchd_label": "com.example.claim6-drill",
        "writer_build": "test-build",
    }
    record.update(overrides)
    return record


def _registered_config(**overrides: object) -> DrillConfig:
    values: dict[str, object] = {
        "schedule_enabled": True,
        "day_of_month": 3,
        "launchd_label": "com.example.claim6-drill",
        "acknowledged_device": "registered-device",
    }
    values.update(overrides)
    return DrillConfig(**values)


def test_drill_writer_appends_canonical_scheduled_row(tmp_path) -> None:
    log_path = tmp_path / "claim6-drills.jsonl"

    append_drill_record(log_path, _scheduled_record())

    rows = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert rows == [_scheduled_record()]


@pytest.mark.parametrize(
    "incident_data",
    [
        {"incident_id": "inc-1"},
        {"severity": "high"},
        {"verified_restored_at": "2026-09-03T09:00:00-04:00"},
        {"restore_verification": {"verified": True}},
        {"restoreVerification": {"verified": True}},
        {"context": {"restore_verification_result": "passed"}},
    ],
)
def test_drill_writer_rejects_incident_only_fields(
    tmp_path, incident_data: dict[str, object]
) -> None:
    with pytest.raises(ValueError, match="incident-only"):
        append_drill_record(
            tmp_path / "claim6-drills.jsonl",
            _scheduled_record(**incident_data),
        )


def test_send_accepted_row_carries_b3_transport_shape(tmp_path) -> None:
    log_path = tmp_path / "claim6-drills.jsonl"
    record = _scheduled_record(
        drill_event="send_accepted",
        request="request-123",
        receipt="receipt-123",
        delivery_row_id="claim6-2026-09-03T0815:send_accepted",
        alerts=1,
        attempted=True,
        delivered=True,
        probe="not-run",
        dry_run=False,
    )

    append_drill_record(log_path, record)

    persisted = json.loads(log_path.read_text())
    assert {
        key: persisted[key]
        for key in ("alerts", "attempted", "delivered", "probe", "dry_run")
    } == {
        "alerts": 1,
        "attempted": True,
        "delivered": True,
        "probe": "not-run",
        "dry_run": False,
    }


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("alerts", 0),
        ("attempted", False),
        ("delivered", False),
        ("probe", "ok"),
        ("dry_run", True),
    ],
)
def test_send_accepted_writer_rejects_non_b3_transport_shapes(
    tmp_path, field: str, bad_value: object
) -> None:
    record = _scheduled_record(
        drill_event="send_accepted",
        request="request-123",
        receipt="receipt-123",
        delivery_row_id="claim6-2026-09-03T0815:send_accepted",
        alerts=1,
        attempted=True,
        delivered=True,
        probe="not-run",
        dry_run=False,
    )
    record[field] = bad_value

    with pytest.raises(ValueError, match="send_accepted"):
        append_drill_record(tmp_path / "claim6-drills.jsonl", record)


@pytest.mark.parametrize(
    ("ppid", "label", "now", "message"),
    [
        (99, "com.example.claim6-drill", datetime(2026, 9, 3, 8, 15), "PPID 1"),
        (1, "wrong.label", datetime(2026, 9, 3, 8, 15), "label"),
        (1, "com.example.claim6-drill", datetime(2026, 9, 4, 8, 15), "slot"),
        (1, "com.example.claim6-drill", datetime(2026, 9, 3, 8, 16), "slot"),
    ],
)
def test_production_send_refuses_wrong_parent_label_or_calendar_slot(
    ppid: int, label: str, now: datetime, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_production_provenance(
            _registered_config(), ppid=ppid, environment_label=label, now=now
        )


def test_production_provenance_accepts_only_the_registered_launchd_slot() -> None:
    scheduled = validate_production_provenance(
        _registered_config(),
        ppid=1,
        environment_label="com.example.claim6-drill",
        now=datetime(2026, 9, 3, 8, 15, 42),
    )
    assert scheduled == datetime(2026, 9, 3, 8, 15)


def test_fake_transport_lifecycle_persists_qualified_registered_device_ack(
    tmp_path,
) -> None:
    sent: list[dict[str, object]] = []
    receipt_reads = iter(
        [
            {"acknowledged": 0, "expired": 0, "last_delivered_at": 1788441300},
            {
                "acknowledged": 1,
                "acknowledged_at": 1788441420,
                "acknowledged_by_device": "registered-device",
                "expired": 0,
            },
        ]
    )
    sleeps: list[float] = []
    log_path = tmp_path / "claim6-drills.jsonl"

    final_event = run_test_drill(
        _registered_config(),
        log_path=log_path,
        now=datetime(2026, 9, 3, 8, 15),
        sender=lambda **kwargs: sent.append(kwargs)
        or {"status": 1, "request": "request-123", "receipt": "receipt-123"},
        receipt_reader=lambda receipt: next(receipt_reads),
        sleep=sleeps.append,
        writer_build="test-build",
    )

    rows = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert final_event == "acknowledged"
    assert [row["drill_event"] for row in rows] == [
        "scheduled",
        "send_accepted",
        "acknowledged",
    ]
    assert sent == [
        {
            "title": "Scheduled claim-6 acknowledgment drill",
            "message": "Scheduled claim-6 drill: acknowledge on the registered device.",
            "priority": 2,
            "retry": 300,
            "expire": 900,
            # eng-002.d160 — the send names the same device the ack rule
            # requires. Broadcasting let any device acknowledge while only the
            # registered one qualified, so silencing the repeat on the nearest
            # screen wrote a negative row and failed the drill.
            "device": "registered-device",
        }
    ]
    assert sleeps == [5]
    assert rows[1]["delivery_row_id"] == rows[2]["delivery_row_id"]
    assert rows[2]["acknowledged_by_device"] == "registered-device"


@pytest.mark.parametrize(
    ("acknowledged", "acknowledged_at", "device"),
    [
        (0, 1788441420, "registered-device"),
        (1, 0, "registered-device"),
        (1, 1788441420, "different-device"),
    ],
)
def test_acknowledged_writer_requires_all_three_qualifying_facts(
    tmp_path, acknowledged: int, acknowledged_at: int, device: str
) -> None:
    record = _scheduled_record(
        drill_event="acknowledged",
        receipt="receipt-123",
        delivery_row_id="claim6-2026-09-03T0815:send_accepted",
        acknowledged=acknowledged,
        acknowledged_at=acknowledged_at,
        acknowledged_by_device=device,
        registered_device="registered-device",
    )

    with pytest.raises(ValueError, match="qualifying acknowledgment"):
        append_drill_record(tmp_path / "claim6-drills.jsonl", record)


def test_production_network_entrypoint_is_unreachable_under_pytest() -> None:
    with pytest.raises(RuntimeError, match="disabled under test"):
        run_production_drill()


def test_reconciliation_renders_typed_missing_fire_after_grace(tmp_path) -> None:
    block = render_drill_report_block(
        config={
            "schedule_enabled": True,
            "day_of_month": 3,
            "hour": 8,
            "minute": 15,
            "grace_minutes": 30,
            "launchd_label": "com.example.claim6-drill",
            "acknowledged_device": "registered-device",
        },
        log_path=tmp_path / "missing.jsonl",
        now=datetime(2026, 9, 3, 8, 45, 1),
    )

    assert "DRILL FIRE MISSING — SCHEDULED EXECUTION NOT OBSERVED" in block
    assert "**Means:**" in block
    assert "**Does not mean / Next:**" in block
    assert len([line for line in block.splitlines() if line.startswith("- ")]) == 3


def test_meta_agent_report_contains_drill_block_before_delivery(tmp_path) -> None:
    from agents import meta_agent
    from lib.config import load_config

    config = load_config()
    config.vault_root = tmp_path
    # State the precondition instead of inheriting it from whatever this
    # machine's config.toml happens to say. Amended 2026-08-31 (eng-002.d160):
    # this read the live file, so arming the drill on the Mini turned the
    # production suite red for the whole B3 window.
    config.agents = dict(config.agents)
    config.agents["claim6_drill"] = {}

    report = meta_agent.generate_fleet_report(dry_run=True, config=config)

    assert "## Claim-6 Drill" in report
    assert "**Status:** DRILL NOT REGISTERED — SCHEDULE NOT ARMED" in report


@pytest.mark.parametrize(
    "receipt_status",
    [
        {
            "acknowledged": 1,
            "acknowledged_at": 1788441420,
            "acknowledged_by_device": "different-device",
            "expired": 0,
        },
        {
            "acknowledged": 0,
            "acknowledged_at": 0,
            "acknowledged_by_device": "",
            "expired": 1,
            "last_delivered_at": 1788441300,
        },
    ],
)
def test_wrong_device_or_expiry_is_retained_negative_evidence(
    tmp_path, receipt_status: dict[str, object]
) -> None:
    log_path = tmp_path / "claim6-drills.jsonl"

    final_event = run_test_drill(
        _registered_config(),
        log_path=log_path,
        now=datetime(2026, 9, 3, 8, 15),
        sender=lambda **kwargs: {
            "status": 1,
            "request": "request-123",
            "receipt": "receipt-123",
        },
        receipt_reader=lambda receipt: receipt_status,
        sleep=lambda seconds: None,
    )

    rows = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert final_event == "expired_unacknowledged"
    assert rows[-1]["drill_event"] == "expired_unacknowledged"
    assert rows[-1]["acknowledged_by_device"] == receipt_status[
        "acknowledged_by_device"
    ]
    assert rows[-1]["negative_reason"] in {
        "acknowledged_by_unregistered_device",
        "provider_expired_unacknowledged",
    }


def test_send_and_receipt_read_failures_are_persisted_not_discarded(tmp_path) -> None:
    send_log = tmp_path / "send-failed.jsonl"
    receipt_log = tmp_path / "receipt-failed.jsonl"

    send_event = run_test_drill(
        _registered_config(),
        log_path=send_log,
        now=datetime(2026, 9, 3, 8, 15),
        sender=lambda **kwargs: (_ for _ in ()).throw(RuntimeError("send down")),
        receipt_reader=lambda receipt: {},
        sleep=lambda seconds: None,
    )
    receipt_event = run_test_drill(
        _registered_config(),
        log_path=receipt_log,
        now=datetime(2026, 9, 3, 8, 15),
        sender=lambda **kwargs: {
            "status": 1,
            "request": "request-123",
            "receipt": "receipt-123",
        },
        receipt_reader=lambda receipt: (_ for _ in ()).throw(
            RuntimeError("receipt down")
        ),
        sleep=lambda seconds: None,
    )

    send_rows = [json.loads(line) for line in send_log.read_text().splitlines()]
    receipt_rows = [json.loads(line) for line in receipt_log.read_text().splitlines()]
    assert send_event == "send_failed"
    assert send_rows[-1]["drill_event"] == "send_failed"
    assert send_rows[-1]["attempted"] is True
    assert send_rows[-1]["delivered"] is False
    assert receipt_event == "receipt_poll_failed"
    assert receipt_rows[-1]["drill_event"] == "receipt_poll_failed"


@pytest.mark.parametrize(
    "drill_event",
    ["send_failed", "expired_unacknowledged", "receipt_poll_failed"],
)
def test_negative_event_rows_require_their_retained_evidence_fields(
    tmp_path, drill_event: str
) -> None:
    with pytest.raises(ValueError, match=drill_event):
        append_drill_record(
            tmp_path / "claim6-drills.jsonl",
            _scheduled_record(drill_event=drill_event),
        )


def test_reconciliation_does_not_let_malformed_rows_hide_a_missing_fire(
    tmp_path,
) -> None:
    log_path = tmp_path / "claim6-drills.jsonl"
    log_path.write_text(
        json.dumps(
            {
                "drill_event": "scheduled",
                "scheduled_for": "2026-09-03T08:15:00-04:00",
                "launchd_label": "com.example.claim6-drill",
            }
        )
        + "\n"
    )

    block = render_drill_report_block(
        config={
            "schedule_enabled": True,
            "day_of_month": 3,
            "launchd_label": "com.example.claim6-drill",
            "acknowledged_device": "registered-device",
        },
        log_path=log_path,
        now=datetime(2026, 9, 3, 8, 46),
    )

    assert "DRILL RECORD READ FAILED" in block


def test_drill_send_targets_only_the_registered_device(tmp_path) -> None:
    """eng-002.d160, stated on its own so it cannot be lost in a shape diff.

    Two devices exist on the live account — `sean-phone` and `fleet-pager`,
    the Mac Mini that runs the fleet. An untargeted priority-2 drill repeats
    on both until someone silences it, and acknowledging on the Mini would be
    both a negative row and the exact circularity ADR-12 exists to avoid:
    the machine under test certifying its own pager.
    """
    sent: list[dict] = []
    log_path = tmp_path / "claim6-drills.jsonl"
    run_test_drill(
        _registered_config(acknowledged_device="sean-phone"),
        log_path=log_path,
        now=datetime(2026, 9, 3, 8, 15),
        sender=lambda **kwargs: sent.append(kwargs)
        or {"status": 1, "request": "r", "receipt": "rc"},
        receipt_reader=lambda receipt: {
            "acknowledged": 1, "acknowledged_at": 111,
            "acknowledged_by_device": "sean-phone",
        },
        sleep=lambda _s: None,
        writer_build="test-build",
    )
    assert sent[0]["device"] == "sean-phone"
