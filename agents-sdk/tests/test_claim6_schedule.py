"""Deployment contract for the default-unarmed monthly claim-6 plist."""

from __future__ import annotations

import plistlib
import tomllib
from pathlib import Path

from schedules.render_claim6_plist import render_claim6_plist


SDK_ROOT = Path(__file__).parent.parent


def test_claim6_schedule_is_unregistered_and_default_disabled() -> None:
    with (SDK_ROOT / "config.toml").open("rb") as stream:
        config = tomllib.load(stream)["agents"]["claim6_drill"]

    assert config["schedule_enabled"] is False
    assert config["day_of_month"] == 0
    assert config["launchd_label"] == ""
    assert config["acknowledged_device"] == ""


def test_registered_template_renders_monthly_0815_with_full_launchd_environment(
    tmp_path,
) -> None:
    output = tmp_path / "claim6.plist"
    render_claim6_plist(
        template_path=SDK_ROOT / "schedules" / "com.sean.agent.claim6-drill.plist.template",
        output_path=output,
        config={
            "schedule_enabled": True,
            "day_of_month": 3,
            "launchd_label": "com.example.claim6-drill",
            "acknowledged_device": "registered-device",
        },
    )

    with output.open("rb") as stream:
        plist = plistlib.load(stream)
    assert plist["Label"] == "com.example.claim6-drill"
    assert plist["StartCalendarInterval"] == {"Day": 3, "Hour": 8, "Minute": 15}
    assert plist["EnvironmentVariables"] == {
        "PATH": "/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONPATH": "/Users/seanwinslow/Code-Brain/code-brain/agents-sdk",
        "CLAIM6_LAUNCHD_LABEL": "com.example.claim6-drill",
    }


def test_registration_does_not_choose_or_narrow_the_b3_day(tmp_path) -> None:
    output = tmp_path / "day-31.plist"
    render_claim6_plist(
        template_path=SDK_ROOT / "schedules" / "com.sean.agent.claim6-drill.plist.template",
        output_path=output,
        config={
            "schedule_enabled": True,
            "day_of_month": 31,
            "launchd_label": "com.example.claim6-drill",
            "acknowledged_device": "registered-device",
        },
    )

    with output.open("rb") as stream:
        assert plistlib.load(stream)["StartCalendarInterval"]["Day"] == 31
