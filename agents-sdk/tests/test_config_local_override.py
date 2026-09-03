"""Contract for the gitignored `config.local.toml` override (2026-09-03).

This mechanism exists to end a specific failure: the claim-6 drill
registration used to live as a permanent local modification to the TRACKED
`config.toml`, held in place by a `skip-worktree` mask and two untracked
`.git/hooks` guards. None of that showed in `git status` or survived a fresh
clone, and Obsidian-Git's repo-wide `add -A` kept trying to commit it.

The property under test: the tracked config ships unarmed and committable,
while the machine reads an armed registration from the override.
"""

from __future__ import annotations

import pytest
import tomllib
from pathlib import Path

from lib.config import (
    deep_merge,
    load_config,
    load_raw_config,
    local_config_path_for,
)


SDK_ROOT = Path(__file__).parent.parent


# ─── deep_merge ──────────────────────────────────────────────────────────────

def test_deep_merge_overrides_one_key_without_restating_its_table() -> None:
    """The whole point: an override sets one key, the rest survives."""
    base = {"agents": {"claim6_drill": {"schedule_enabled": False, "hour": 8, "minute": 15}}}
    merged = deep_merge(base, {"agents": {"claim6_drill": {"schedule_enabled": True}}})
    drill = merged["agents"]["claim6_drill"]
    assert drill["schedule_enabled"] is True
    assert drill["hour"] == 8, "sibling keys must survive a partial override"
    assert drill["minute"] == 15


def test_deep_merge_does_not_mutate_its_inputs() -> None:
    base = {"agents": {"claim6_drill": {"schedule_enabled": False}}}
    deep_merge(base, {"agents": {"claim6_drill": {"schedule_enabled": True}}})
    assert base["agents"]["claim6_drill"]["schedule_enabled"] is False


def test_deep_merge_replaces_lists_wholesale_rather_than_concatenating() -> None:
    merged = deep_merge({"a": {"skills": ["x", "y"]}}, {"a": {"skills": ["z"]}})
    assert merged["a"]["skills"] == ["z"]


def test_deep_merge_adds_tables_absent_from_the_base() -> None:
    merged = deep_merge({"agents": {}}, {"agents": {"new_agent": {"enabled": True}}})
    assert merged["agents"]["new_agent"] == {"enabled": True}


# ─── path derivation ─────────────────────────────────────────────────────────

def test_local_path_is_derived_from_the_given_config_not_hardcoded(tmp_path) -> None:
    """A test pointing at a tmp config must never pick up the real machine's
    override — that would make the suite depend on deploy state again."""
    assert local_config_path_for(tmp_path / "config.toml") == tmp_path / "config.local.toml"


# ─── load_raw_config ─────────────────────────────────────────────────────────

def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_absent_override_returns_the_tracked_values_and_no_provenance(tmp_path) -> None:
    cfg = _write(tmp_path / "config.toml", "[agents.claim6_drill]\nschedule_enabled = false\n")
    merged, applied = load_raw_config(cfg)
    assert merged["agents"]["claim6_drill"]["schedule_enabled"] is False
    assert applied is None


def test_present_override_arms_the_drill_and_reports_its_provenance(tmp_path) -> None:
    cfg = _write(
        tmp_path / "config.toml",
        "[agents.claim6_drill]\nschedule_enabled = false\nday_of_month = 0\nhour = 8\n",
    )
    _write(
        tmp_path / "config.local.toml",
        '[agents.claim6_drill]\nschedule_enabled = true\nday_of_month = 2\n',
    )
    merged, applied = load_raw_config(cfg)
    drill = merged["agents"]["claim6_drill"]
    assert drill["schedule_enabled"] is True
    assert drill["day_of_month"] == 2
    assert drill["hour"] == 8, "unoverridden keys still come from the tracked config"
    assert applied == tmp_path / "config.local.toml", "the merge must never be silent"


def test_malformed_override_raises_rather_than_being_silently_skipped(tmp_path) -> None:
    """A skipped override would silently disarm a registered machine — the
    exact class of invisible failure this file replaced."""
    cfg = _write(tmp_path / "config.toml", "[agents.claim6_drill]\nschedule_enabled = false\n")
    _write(tmp_path / "config.local.toml", "this is not = = valid toml [[[")
    with pytest.raises(tomllib.TOMLDecodeError):
        load_raw_config(cfg)


def test_load_config_surfaces_the_override_path_on_the_config_object(tmp_path) -> None:
    cfg = _write(
        tmp_path / "config.toml",
        '[paths]\nrepo_root = "/tmp/x"\n[agents.claim6_drill]\nschedule_enabled = false\n',
    )
    _write(tmp_path / "config.local.toml", "[agents.claim6_drill]\nschedule_enabled = true\n")
    loaded = load_config(config_path=cfg, env_path=tmp_path / "nonexistent.env")
    assert loaded.agents["claim6_drill"]["schedule_enabled"] is True
    assert loaded.local_config_path == tmp_path / "config.local.toml"


# ─── the deployment property this all exists to protect ──────────────────────

def test_tracked_config_on_disk_ships_unarmed_so_it_stays_committable() -> None:
    """The working-tree config must now be clean and unarmed on EVERY machine,
    registered or not. Before the override existed, a registered machine had to
    keep this file permanently dirty, which is what Obsidian-Git kept trying to
    commit and what the pre-commit hook existed to block.
    """
    with (SDK_ROOT / "config.toml").open("rb") as stream:
        drill = tomllib.load(stream)["agents"]["claim6_drill"]
    assert drill["schedule_enabled"] is False
    assert drill["day_of_month"] == 0
    assert drill["launchd_label"] == ""
    assert drill["acknowledged_device"] == ""


def test_the_example_override_is_tracked_so_the_mechanism_is_discoverable() -> None:
    """A fresh clone must be able to SEE that local overrides exist. The
    mechanism this replaced was invisible by construction."""
    example = SDK_ROOT / "config.local.toml.example"
    assert example.exists(), "config.local.toml.example must stay tracked"
    text = example.read_text(encoding="utf-8")
    assert "config.local.toml" in text
    assert "claim6_drill" in text, "the example must name the case that motivated it"
