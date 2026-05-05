"""Tests for daily_driver.build_artifact_preamble (Phase 1 wiring)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from agents.daily_driver import build_artifact_preamble, build_preamble
from lib.artifact_loader import clear_cache


@pytest.fixture(autouse=True)
def _reset_cache():
    clear_cache()
    yield
    clear_cache()


@dataclass
class _FakeSafety:
    max_turns_default: int = 30
    max_budget_default: float = 0.60
    permission_mode: str = "acceptEdits"


@dataclass
class _FakeConfig:
    """Stand-in for lib.config.Config — only fields the preamble touches."""

    vault_root: Path
    repo_root: Path
    agents: dict = field(default_factory=dict)
    artifacts: dict = field(default_factory=dict)
    safety: _FakeSafety = field(default_factory=_FakeSafety)

    def artifact_config(self, name: str) -> dict:
        if not self.artifacts.get("enabled", False):
            return {}
        return self.artifacts.get("per_agent", {}).get(name, {})


def _make_config(tmp_artifacts: Path, *, enabled: bool = True, per_agent: dict | None = None) -> _FakeConfig:
    if per_agent is None:
        per_agent = {
            "daily_driver": {
                "heartbeats": True,
                "on_demand": ["USER", "SOUL", "operating-model", "schedule-recommendations"],
            }
        }
    return _FakeConfig(
        vault_root=tmp_artifacts,
        repo_root=tmp_artifacts.parent,
        artifacts={
            "enabled": enabled,
            "vault_subpath": "05_atlas/operating-models",
            "require_confirmed": True,
            "per_agent": per_agent,
        },
    )


class TestArtifactPreambleContent:
    def test_includes_all_three_heartbeats(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts)
        block = build_artifact_preamble(cfg)
        assert "## creative-studio" in block
        assert "## life-systems" in block
        assert "## job-hunt-2026" in block
        # Body content from fixture
        assert "Block work through 3 PM" in block
        assert "Sacred first hour 5:30-6:30 AM" in block
        assert "Sacred first hour 8:45-9:45" in block

    def test_lists_on_demand_paths_for_all_domains(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts)
        block = build_artifact_preamble(cfg)
        assert "USER,SOUL,operating-model,schedule-recommendations" in block
        assert "creative-studio/" in block
        assert "life-systems/" in block
        assert "job-hunt-2026/" in block

    def test_includes_tone_and_capture_rules(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts)
        block = build_artifact_preamble(cfg)
        assert "calm, factual, zen" in block
        assert "CAPTURE-AND-DEFER" in block


class TestArtifactPreambleToggles:
    def test_disabled_globally_returns_empty(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts, enabled=False)
        assert build_artifact_preamble(cfg) == ""

    def test_no_per_agent_entry_returns_empty(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts, per_agent={})
        assert build_artifact_preamble(cfg) == ""

    def test_heartbeats_false_still_emits_on_demand_and_rules(self, tmp_artifacts: Path):
        cfg = _make_config(
            tmp_artifacts,
            per_agent={"daily_driver": {"heartbeats": False, "on_demand": ["USER"]}},
        )
        block = build_artifact_preamble(cfg)
        assert "## creative-studio" not in block
        assert "creative-studio/{USER}.md" in block
        assert "calm, factual, zen" in block

    def test_missing_heartbeat_does_not_crash(self, tmp_artifacts: Path):
        (tmp_artifacts / "05_atlas/operating-models/life-systems/HEARTBEAT.md").unlink()
        cfg = _make_config(tmp_artifacts)
        block = build_artifact_preamble(cfg)
        # Other two domains still render; the missing one surfaces a gap marker.
        assert "## creative-studio" in block
        assert "## life-systems" in block
        assert "artifact unavailable" in block
        assert "## job-hunt-2026" in block


class TestBuildPreambleIntegration:
    def test_morning_mode_injects_artifact_block(self, tmp_artifacts: Path, tmp_vault: Path):
        # build_preamble uses config.vault_root for both vault_health_summary
        # and for artifact lookups; point both at the artifact tree so the
        # artifact block resolves while vault_health gracefully says PASS.
        cfg = _FakeConfig(
            vault_root=tmp_artifacts,
            repo_root=tmp_artifacts.parent,
            agents={"daily_driver": {"morning_time": "08:45"}},
            artifacts={
                "enabled": True,
                "vault_subpath": "05_atlas/operating-models",
                "require_confirmed": True,
                "per_agent": {
                    "daily_driver": {
                        "heartbeats": True,
                        "on_demand": ["USER"],
                    }
                },
            },
        )
        out = build_preamble("morning", cfg)
        assert "ZERO-INTERACTION MANDATE" in out
        assert "OPERATING-MODEL CONTEXT (always loaded" in out
        assert "## creative-studio" in out

    def test_evening_mode_does_not_inject_artifact_block(self, tmp_artifacts: Path):
        cfg = _FakeConfig(
            vault_root=tmp_artifacts,
            repo_root=tmp_artifacts.parent,
            agents={"daily_driver": {"evening_time": "17:00"}},
            artifacts={
                "enabled": True,
                "vault_subpath": "05_atlas/operating-models",
                "require_confirmed": True,
                "per_agent": {"daily_driver": {"heartbeats": True, "on_demand": []}},
            },
        )
        out = build_preamble("evening", cfg)
        assert "ZERO-INTERACTION MANDATE" in out
        assert "OPERATING-MODEL CONTEXT" not in out


class TestToneGuard:
    """Forbidden-phrase audit per Section 8 Risk #9 (scolding tone drift)."""

    def test_preamble_has_no_scolding_phrases(self, tmp_artifacts: Path):
        cfg = _make_config(tmp_artifacts)
        block = build_artifact_preamble(cfg)
        lowered = block.lower()
        for phrase in ("you should", "you need to", "make sure to", "don't forget"):
            assert phrase not in lowered, f"scolding phrase leaked into preamble: {phrase!r}"
