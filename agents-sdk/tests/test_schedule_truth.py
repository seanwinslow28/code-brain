"""Schedule display metadata must tell the same truth as launchd."""

from __future__ import annotations

import plistlib
import re
import tomllib
from pathlib import Path

from agents.meta_agent import AGENT_METADATA


SCHEDULES_DIR = Path(__file__).parent.parent / "schedules"
PLIST_BY_AGENT = {
    "vault_indexer": "com.sean.agent.vault-indexer.plist",
    "vault_synthesizer": "com.sean.agent.vault-synthesizer.plist",
    "vault_critic": "com.sean.agent.vault-critic.plist",
    "deep_researcher": "com.sean.agent.deep-researcher.plist",
    "job_feed": "com.sean.job-feed.plist",
    "daily_driver": "com.sean.agent.daily-morning.plist",
    "knowledge_lint": "com.sean.agent.knowledge-lint.plist",
    "meta_agent": "com.sean.agent.meta-agent.plist",
}


def _plist_slots(plist_name: str) -> set[tuple[int | None, int, int]]:
    with (SCHEDULES_DIR / plist_name).open("rb") as stream:
        intervals = plistlib.load(stream)["StartCalendarInterval"]
    if isinstance(intervals, dict):
        intervals = [intervals]
    return {
        (item.get("Weekday"), int(item["Hour"]), int(item["Minute"]))
        for item in intervals
    }


def _display_slots(display: str) -> set[tuple[int | None, int, int]]:
    if display == "Sunday 22:00":
        return {(0, 22, 0)}
    if display == "8:00-11:00 AM x7":
        return {
            (None, 8, 0),
            (None, 8, 30),
            (None, 9, 0),
            (None, 9, 30),
            (None, 10, 0),
            (None, 10, 30),
            (None, 11, 0),
        }
    match = re.fullmatch(r"(\d{1,2}):(\d{2}) (AM|PM) daily", display)
    assert match, f"unparseable scheduled display: {display!r}"
    hour = int(match.group(1)) % 12 + (12 if match.group(3) == "PM" else 0)
    return {(None, hour, int(match.group(2)))}


def test_agent_metadata_schedules_match_checked_in_launchd_plists() -> None:
    assert set(PLIST_BY_AGENT) == set(AGENT_METADATA) - {"flush"}
    assert AGENT_METADATA["flush"]["schedule"] == "hook-triggered"

    for agent, plist_name in PLIST_BY_AGENT.items():
        assert _display_slots(str(AGENT_METADATA[agent]["schedule"])) == _plist_slots(
            plist_name
        ), agent


def test_config_schedule_fields_match_checked_in_launchd_plists() -> None:
    with (Path(__file__).parent.parent / "config.toml").open("rb") as stream:
        agents = tomllib.load(stream)["agents"]

    assert agents["daily_driver"]["morning_time"] == "08:30"
    assert agents["meta_agent"]["schedule"] == "08:45"
    assert _plist_slots("com.sean.agent.daily-morning.plist") == {(None, 8, 30)}
    assert _plist_slots("com.sean.agent.meta-agent.plist") == {(None, 8, 45)}


def test_daily_note_auto_fill_copy_names_the_actual_daily_driver_time() -> None:
    source = (Path(__file__).parent.parent / "agents" / "daily_driver.py").read_text()
    assert "_Auto-filled by Daily Driver at 08:30. Do not edit manually._" in source
    assert "_Auto-filled by Daily Driver at 08:45. Do not edit manually._" not in source
