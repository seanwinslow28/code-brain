#!/usr/bin/env python3
"""Scheduled-only ADR-12 claim-6 notification drill."""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from lib.claim6_drill import append_drill_record


@dataclass(frozen=True)
class DrillConfig:
    """Registered monthly schedule and acknowledgment contract."""

    schedule_enabled: bool = False
    day_of_month: int = 0
    launchd_label: str = ""
    acknowledged_device: str = ""
    hour: int = 8
    minute: int = 15
    grace_minutes: int = 30
    retry_seconds: int = 300
    expire_seconds: int = 900
    receipt_poll_seconds: int = 5

    @classmethod
    def from_mapping(cls, raw: dict) -> "DrillConfig":
        return cls(
            schedule_enabled=bool(raw.get("schedule_enabled", False)),
            day_of_month=int(raw.get("day_of_month", 0)),
            launchd_label=str(raw.get("launchd_label", "")),
            acknowledged_device=str(raw.get("acknowledged_device", "")),
            hour=int(raw.get("hour", 8)),
            minute=int(raw.get("minute", 15)),
            grace_minutes=int(raw.get("grace_minutes", 30)),
            retry_seconds=int(raw.get("retry_seconds", 300)),
            expire_seconds=int(raw.get("expire_seconds", 900)),
            receipt_poll_seconds=int(raw.get("receipt_poll_seconds", 5)),
        )


def validate_registration(config: DrillConfig) -> None:
    """Fail closed until all three deploy-time values are registered."""
    if not config.schedule_enabled:
        raise ValueError("claim-6 schedule is not enabled")
    if not 1 <= config.day_of_month <= 31:
        raise ValueError("claim-6 day_of_month must be registered from 1 through 31")
    if not config.launchd_label:
        raise ValueError("claim-6 launchd label is not registered")
    if not config.acknowledged_device:
        raise ValueError("claim-6 acknowledged device is not registered")
    if config.receipt_poll_seconds < 5:
        raise ValueError("claim-6 receipt polling must respect the five-second floor")


def validate_production_provenance(
    config: DrillConfig,
    *,
    ppid: int,
    environment_label: str | None,
    now: datetime,
) -> datetime:
    """Return the registered slot or refuse a production network call."""
    validate_registration(config)
    if ppid != 1:
        raise ValueError("claim-6 production send requires launchd PPID 1")
    if environment_label != config.launchd_label:
        raise ValueError("claim-6 launchd label does not match registration")
    if (now.day, now.hour, now.minute) != (
        config.day_of_month,
        config.hour,
        config.minute,
    ):
        raise ValueError("claim-6 current slot is not the registered calendar slot")
    return now.replace(second=0, microsecond=0)


def _record_base(
    *,
    config: DrillConfig,
    drill_id: str,
    drill_event: str,
    occurred_at: datetime,
    scheduled_for: datetime,
    writer_build: str,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "record_type": "drill",
        "drill_id": drill_id,
        "drill_event": drill_event,
        "occurred_at": occurred_at.isoformat(),
        "scheduled_for": scheduled_for.isoformat(),
        "launchd_label": config.launchd_label,
        "writer_build": writer_build,
    }


def _run_lifecycle(
    config: DrillConfig,
    *,
    log_path: Path,
    scheduled_for: datetime,
    clock: Callable[[], datetime],
    sender: Callable[..., dict],
    receipt_reader: Callable[[str], dict],
    sleep: Callable[[float], None],
    writer_build: str,
) -> str:
    """Run one already-authorized lifecycle against the supplied boundary."""
    drill_id = f"claim6-{scheduled_for.strftime('%Y%m%dT%H%M%z')}"

    append_drill_record(
        log_path,
        _record_base(
            config=config,
            drill_id=drill_id,
            drill_event="scheduled",
            occurred_at=clock(),
            scheduled_for=scheduled_for,
            writer_build=writer_build,
        ),
    )

    try:
        response = sender(
            title="Scheduled claim-6 acknowledgment drill",
            message="Scheduled claim-6 drill: acknowledge on the registered device.",
            priority=2,
            retry=config.retry_seconds,
            expire=config.expire_seconds,
            # The send and the acknowledgment rule must name the same device.
            # Broadcasting let any device acknowledge while only the registered
            # one qualified, so the likeliest human action — silencing the
            # repeat on whichever screen is nearest — wrote a NEGATIVE row and
            # failed the drill. eng-002.d160.
            device=config.acknowledged_device,
        )
        if response.get("status") != 1 or not response.get("request") or not response.get(
            "receipt"
        ):
            raise ValueError("provider acceptance omitted status, request, or receipt")
    except Exception as exc:
        failed = _record_base(
            config=config,
            drill_id=drill_id,
            drill_event="send_failed",
            occurred_at=clock(),
            scheduled_for=scheduled_for,
            writer_build=writer_build,
        )
        failed.update(
            {
                "alerts": 1,
                "attempted": True,
                "delivered": False,
                "probe": "not-run",
                "dry_run": False,
                "error": str(exc)[:500],
            }
        )
        append_drill_record(log_path, failed)
        return "send_failed"

    receipt = str(response["receipt"])
    delivery_row_id = f"{drill_id}:send_accepted"
    accepted = _record_base(
        config=config,
        drill_id=drill_id,
        drill_event="send_accepted",
        occurred_at=clock(),
        scheduled_for=scheduled_for,
        writer_build=writer_build,
    )
    accepted.update(
        {
            "request": str(response["request"]),
            "receipt": receipt,
            "delivery_row_id": delivery_row_id,
            "alerts": 1,
            "attempted": True,
            "delivered": True,
            "probe": "not-run",
            "dry_run": False,
        }
    )
    append_drill_record(log_path, accepted)

    max_reads = math.ceil(config.expire_seconds / config.receipt_poll_seconds) + 1
    last_status: dict = {}
    for read_index in range(max_reads):
        try:
            last_status = receipt_reader(receipt)
        except Exception as exc:
            failed_poll = _record_base(
                config=config,
                drill_id=drill_id,
                drill_event="receipt_poll_failed",
                occurred_at=clock(),
                scheduled_for=scheduled_for,
                writer_build=writer_build,
            )
            failed_poll.update(
                {
                    "receipt": receipt,
                    "delivery_row_id": delivery_row_id,
                    "error": str(exc)[:500],
                }
            )
            append_drill_record(log_path, failed_poll)
            return "receipt_poll_failed"

        acknowledged = last_status.get("acknowledged") == 1
        acknowledged_at = last_status.get("acknowledged_at")
        acknowledged_device = last_status.get("acknowledged_by_device")
        if (
            acknowledged
            and acknowledged_at not in (None, 0, "", "0")
            and acknowledged_device == config.acknowledged_device
        ):
            ack = _record_base(
                config=config,
                drill_id=drill_id,
                drill_event="acknowledged",
                occurred_at=clock(),
                scheduled_for=scheduled_for,
                writer_build=writer_build,
            )
            ack.update(
                {
                    "receipt": receipt,
                    "delivery_row_id": delivery_row_id,
                    "acknowledged": 1,
                    "acknowledged_at": acknowledged_at,
                    "acknowledged_by_device": acknowledged_device,
                    "registered_device": config.acknowledged_device,
                }
            )
            append_drill_record(log_path, ack)
            return "acknowledged"

        if acknowledged and acknowledged_device != config.acknowledged_device:
            negative_reason = "acknowledged_by_unregistered_device"
            break
        if last_status.get("expired") == 1:
            negative_reason = "provider_expired_unacknowledged"
            break
        if read_index < max_reads - 1:
            sleep(config.receipt_poll_seconds)
    else:
        negative_reason = "receipt_window_elapsed_unacknowledged"

    expired = _record_base(
        config=config,
        drill_id=drill_id,
        drill_event="expired_unacknowledged",
        occurred_at=clock(),
        scheduled_for=scheduled_for,
        writer_build=writer_build,
    )
    expired.update(
        {
            "receipt": receipt,
            "delivery_row_id": delivery_row_id,
            "negative_reason": negative_reason,
            "acknowledged": last_status.get("acknowledged", 0),
            "acknowledged_at": last_status.get("acknowledged_at", 0),
            "acknowledged_by_device": last_status.get("acknowledged_by_device", ""),
            "expired": last_status.get("expired", 0),
            "last_delivered_at": last_status.get("last_delivered_at", 0),
        }
    )
    append_drill_record(log_path, expired)
    return "expired_unacknowledged"


def run_test_drill(
    config: DrillConfig,
    *,
    log_path: Path,
    now: datetime,
    sender: Callable[..., dict],
    receipt_reader: Callable[[str], dict],
    sleep: Callable[[float], None],
    writer_build: str = "test-build",
) -> str:
    """Exercise the lifecycle with injected, network-disabled test boundaries.

    The real Pushover functions are explicitly refused here. Production has a
    separate no-argument entrypoint that performs launchd provenance checks.
    """
    validate_registration(config)
    if (now.day, now.hour, now.minute) != (
        config.day_of_month,
        config.hour,
        config.minute,
    ):
        raise ValueError("test clock is not the registered calendar slot")
    for boundary in (sender, receipt_reader):
        if getattr(boundary, "__module__", "") == "lib.pushover":
            raise ValueError("real Pushover network boundary is disabled in test mode")
    scheduled_for = now.replace(second=0, microsecond=0)
    return _run_lifecycle(
        config,
        log_path=log_path,
        scheduled_for=scheduled_for,
        clock=lambda: now,
        sender=sender,
        receipt_reader=receipt_reader,
        sleep=sleep,
        writer_build=writer_build,
    )


def run_production_drill() -> str:
    """Run the real network path only from the registered launchd occurrence."""
    if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
        raise RuntimeError("claim-6 production network is disabled under test")

    from lib.config import load_config
    from lib.pushover import read_receipt_status, send_push

    loaded = load_config()
    config = DrillConfig.from_mapping(loaded.agents.get("claim6_drill", {}))
    now = datetime.now().astimezone()
    scheduled_for = validate_production_provenance(
        config,
        ppid=os.getppid(),
        environment_label=os.environ.get("CLAIM6_LAUNCHD_LABEL"),
        now=now,
    )
    return _run_lifecycle(
        config,
        log_path=loaded.vault_root / "health" / "claim6-drills.jsonl",
        scheduled_for=scheduled_for,
        clock=lambda: datetime.now().astimezone(),
        sender=send_push,
        receipt_reader=read_receipt_status,
        sleep=time.sleep,
        writer_build=os.environ.get("CODE_BRAIN_BUILD", "claim6-drill-v1"),
    )


def main() -> None:
    """No CLI send mode: launchd provenance is the only production entry."""
    if len(sys.argv) != 1:
        raise SystemExit("claim6_drill has no hand-run send mode or CLI options")
    final_event = run_production_drill()
    print(f"claim-6 drill complete: {final_event}")


if __name__ == "__main__":
    main()
