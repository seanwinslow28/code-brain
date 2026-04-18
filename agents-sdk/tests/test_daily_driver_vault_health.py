"""Tests for daily_driver.vault_health_summary (Phase 6 D.3.d)."""

from __future__ import annotations

from pathlib import Path

from lib.lint_report import latest_lint_report, vault_health_summary


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
