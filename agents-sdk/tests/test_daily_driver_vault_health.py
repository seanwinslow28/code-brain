"""Tests for daily_driver.vault_health_summary (Phase 6 D.3.d) plus
Phase D (v3.20.0) synth_health_summary surfacing in the morning preamble."""

from __future__ import annotations

import json
from pathlib import Path

from lib.lint_report import (
    latest_lint_report,
    latest_synth_manifest,
    synth_health_summary,
    vault_health_summary,
)


def test_no_reports_returns_pass(tmp_path: Path) -> None:
    msg = vault_health_summary(tmp_path)
    assert "PASS" in msg


def test_latest_lint_report_picks_newest(tmp_path: Path) -> None:
    health = tmp_path / "health"
    health.mkdir()
    (health / "2026-04-10-lint-report.md").write_text("# old", encoding="utf-8")
    (health / "2026-04-17-lint-report.md").write_text("# new", encoding="utf-8")
    latest = latest_lint_report(tmp_path)
    assert latest is not None
    assert latest.name == "2026-04-17-lint-report.md"


def test_clean_report_passes(tmp_path: Path) -> None:
    (tmp_path / "health").mkdir()
    (tmp_path / "health" / "2026-04-17-lint-report.md").write_text(
        "# Knowledge Lint Report — 2026-04-17\n\n_0 issues found._\n",
        encoding="utf-8",
    )
    msg = vault_health_summary(tmp_path)
    assert "PASS" in msg
    assert "2026-04-17-lint-report.md" in msg


def test_critical_high_counts_surface(tmp_path: Path) -> None:
    (tmp_path / "health").mkdir()
    (tmp_path / "health" / "2026-04-17-lint-report.md").write_text(
        "# Knowledge Lint Report — 2026-04-17\n\n"
        "## CRITICAL (2)\n- x\n- y\n\n"
        "## HIGH (5)\n- a\n- b\n\n"
        "## LOW (1)\n- c\n",
        encoding="utf-8",
    )
    msg = vault_health_summary(tmp_path)
    assert "2 CRITICAL" in msg
    assert "5 HIGH" in msg
    assert "PASS" not in msg


# ─── Phase D (v3.20.0) — synth-manifest surfacing in morning preamble ─────


def test_latest_synth_manifest_picks_newest(tmp_path: Path) -> None:
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-04-15.json").write_text("{}", encoding="utf-8")
    (health / "synth-manifest-2026-05-01.json").write_text("{}", encoding="utf-8")
    latest = latest_synth_manifest(tmp_path)
    assert latest is not None
    assert latest.name == "synth-manifest-2026-05-01.json"


def test_synth_health_summary_surfaces_counts_in_morning_brief(tmp_path: Path) -> None:
    """The line that lands in daily_driver.build_preamble's morning block."""
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-05-01.json").write_text(
        json.dumps({
            "concepts_written": 12,
            "connections_written": 4,
            "edges_written": 7,
            "rejected_count": 1,
        }),
        encoding="utf-8",
    )
    msg = synth_health_summary(tmp_path)
    assert "last synth:" in msg
    assert "12 concepts" in msg
    assert "4 connections" in msg
    assert "7 edges" in msg
    assert "1 rejected" in msg


def test_build_preamble_morning_includes_synth_line_when_manifest_exists(
    tmp_path: Path,
) -> None:
    """Phase D — the morning preamble should append the synth line under
    Vault Health when a manifest exists. Tests the wiring from
    daily_driver.build_preamble through to the formatted line."""
    # Create vault layout with both a lint report and a synth-manifest.
    vault = tmp_path / "vault"
    health = vault / "health"
    health.mkdir(parents=True)
    (health / "2026-05-01-lint-report.md").write_text(
        "# Knowledge Lint Report — 2026-05-01\n\n_0 issues found._\n",
        encoding="utf-8",
    )
    (health / "synth-manifest-2026-05-01.json").write_text(
        json.dumps({
            "status": "ok",
            "concepts_written": 5,
            "connections_written": 2,
            "edges_written": 3,
            "rejected_count": 0,
            "duration_s": 12.3,
        }),
        encoding="utf-8",
    )

    # Stub config — agents.daily_driver.build_preamble reads
    # config.vault_root, config.repo_root, and a few agent config knobs.
    class _StubConfig:
        vault_root = vault
        repo_root = tmp_path
        agents = {"daily_driver": {"morning_time": "06:00"}}
        artifacts: dict = {}
        fleet_memory: dict = {}

        def artifact_config(self, name):  # noqa: D401
            return {}

    from agents.daily_driver import build_preamble
    preamble = build_preamble("morning", _StubConfig())
    assert "VAULT HEALTH" in preamble
    # render_vault_health() produces "✅ ok — N concepts written in Xs." for status=ok
    assert "5 concepts written" in preamble
    assert "12.3s" in preamble


def test_build_preamble_morning_omits_synth_line_when_no_manifest(
    tmp_path: Path,
) -> None:
    """Fresh vault (no synth-manifest yet) — preamble must not insert
    a stub line. Vault Health line still renders normally."""
    vault = tmp_path / "vault"
    vault.mkdir()

    class _StubConfig:
        vault_root = vault
        repo_root = tmp_path
        agents = {"daily_driver": {"morning_time": "06:00"}}
        artifacts: dict = {}
        fleet_memory: dict = {}

        def artifact_config(self, name):
            return {}

    from agents.daily_driver import build_preamble
    preamble = build_preamble("morning", _StubConfig())
    assert "VAULT HEALTH" in preamble
    assert "last synth:" not in preamble
