"""Tests for meta_agent.* operating-model artifact wiring (Phase 2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from agents.meta_agent import (
    _parse_summary_json,
    build_schedule_recs_context,
    generate_domain_aware_summary,
    render_domain_aware_section,
)
from lib.artifact_loader import clear_cache


@pytest.fixture(autouse=True)
def _reset_cache():
    clear_cache()
    yield
    clear_cache()


@dataclass
class _FakeConfig:
    """Stand-in for lib.config.Config — fields the meta_agent path touches."""

    vault_root: Path
    artifacts: dict = field(default_factory=dict)

    def artifact_config(self, name: str) -> dict:
        if not self.artifacts.get("enabled", False):
            return {}
        return self.artifacts.get("per_agent", {}).get(name, {})


def _config(tmp_artifacts: Path, *, enabled: bool = True, per_agent: dict | None = None) -> _FakeConfig:
    if per_agent is None:
        per_agent = {"meta_agent": {"on_demand": ["schedule-recommendations"]}}
    return _FakeConfig(
        vault_root=tmp_artifacts,
        artifacts={"enabled": enabled, "per_agent": per_agent},
    )


class TestBuildScheduleRecsContext:
    def test_concatenates_all_three_domains(self, tmp_artifacts: Path):
        ctx = build_schedule_recs_context(_config(tmp_artifacts))
        assert "## schedule-recommendations — the-block" in ctx
        assert "## schedule-recommendations — creative-studio" in ctx
        assert "## schedule-recommendations — life-systems" in ctx

    def test_returns_empty_when_artifacts_disabled(self, tmp_artifacts: Path):
        cfg = _config(tmp_artifacts, enabled=False)
        assert build_schedule_recs_context(cfg) == ""

    def test_returns_empty_when_no_per_agent_entry(self, tmp_artifacts: Path):
        cfg = _config(tmp_artifacts, per_agent={})
        assert build_schedule_recs_context(cfg) == ""

    def test_returns_empty_when_schedule_recs_not_in_on_demand(self, tmp_artifacts: Path):
        cfg = _config(tmp_artifacts, per_agent={"meta_agent": {"on_demand": ["SOUL"]}})
        assert build_schedule_recs_context(cfg) == ""

    def test_returns_empty_when_config_is_none(self):
        assert build_schedule_recs_context(None) == ""

    def test_missing_per_domain_artifact_maps_to_unavailable(self, tmp_artifacts: Path):
        # Remove one domain's schedule-recommendations file
        (tmp_artifacts / "05_atlas" / "operating-models" / "the-block" / "schedule-recommendations.md").unlink()
        ctx = build_schedule_recs_context(_config(tmp_artifacts))
        assert "## schedule-recommendations — the-block\n\n[unavailable]" in ctx
        # Other two still present
        assert "## schedule-recommendations — creative-studio" in ctx


class TestParseSummaryJSON:
    def test_parses_well_shaped_json(self):
        text = '{"aligned": ["a"], "misaligned": ["b"], "suggestions": ["c"]}'
        out = _parse_summary_json(text)
        assert out == {"aligned": ["a"], "misaligned": ["b"], "suggestions": ["c"]}

    def test_strips_surrounding_prose(self):
        text = "Some prose before. {\"aligned\": [], \"misaligned\": [], \"suggestions\": []} more prose."
        out = _parse_summary_json(text)
        assert out == {"aligned": [], "misaligned": [], "suggestions": []}

    def test_returns_none_on_garbage(self):
        assert _parse_summary_json("no braces here") is None
        assert _parse_summary_json("{not valid json}") is None

    def test_coerces_non_list_values_to_empty_list(self):
        text = '{"aligned": "scalar", "misaligned": null, "suggestions": ["ok"]}'
        out = _parse_summary_json(text)
        assert out == {"aligned": [], "misaligned": [], "suggestions": ["ok"]}


class TestRenderDomainAwareSection:
    def test_renders_three_subsections(self):
        parsed = {"aligned": ["A1"], "misaligned": ["M1"], "suggestions": ["S1"]}
        md = render_domain_aware_section(parsed)
        assert "## Domain-Aware Insights" in md
        assert "### Aligned with Protect / Automate" in md
        assert "- A1" in md
        assert "### Misaligned or Touching Decline" in md
        assert "- M1" in md
        assert "### Suggestions" in md
        assert "- S1" in md

    def test_renders_empty_subsection_as_none_marker(self):
        parsed = {"aligned": [], "misaligned": [], "suggestions": []}
        md = render_domain_aware_section(parsed)
        assert md.count("_(none)_") == 3

    def test_fallback_when_parsed_is_none(self):
        md = render_domain_aware_section(None)
        assert "## Domain-Aware Insights" in md
        assert "Local summary unavailable" in md


class TestGenerateDomainAwareSummary:
    def test_returns_empty_when_artifacts_off(self, tmp_artifacts: Path):
        cfg = _config(tmp_artifacts, enabled=False)
        out = generate_domain_aware_summary(config=cfg, fleet_snapshot="…")
        assert out == ""

    def test_dry_run_skips_caller(self, tmp_artifacts: Path):
        called = {"n": 0}

        def fake_caller(prompt: str) -> str:
            called["n"] += 1
            return ""

        out = generate_domain_aware_summary(
            config=_config(tmp_artifacts),
            fleet_snapshot="…",
            summary_caller=fake_caller,
            dry_run=True,
        )
        assert called["n"] == 0
        assert "Dry run" in out
        assert "## Domain-Aware Insights" in out

    def test_caller_receives_schedule_recs_and_snapshot(self, tmp_artifacts: Path):
        seen = {"prompt": ""}

        def fake_caller(prompt: str) -> str:
            seen["prompt"] = prompt
            return '{"aligned": ["x"], "misaligned": [], "suggestions": []}'

        out = generate_domain_aware_summary(
            config=_config(tmp_artifacts),
            fleet_snapshot="SNAPSHOT-MARKER",
            summary_caller=fake_caller,
        )
        assert "schedule-recommendations — the-block" in seen["prompt"]
        assert "SNAPSHOT-MARKER" in seen["prompt"]
        assert "- x" in out

    def test_caller_garbage_response_falls_back(self, tmp_artifacts: Path):
        out = generate_domain_aware_summary(
            config=_config(tmp_artifacts),
            fleet_snapshot="…",
            summary_caller=lambda p: "no json at all",
        )
        assert "Local summary unavailable" in out
