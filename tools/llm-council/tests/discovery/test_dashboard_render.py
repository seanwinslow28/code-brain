# tests/discovery/test_dashboard_render.py
from pathlib import Path

from council.discovery.dashboard import SpendDay
from council.discovery.dashboard_render import render_dashboard
from tests.discovery.test_dashboard import (
    EMPTY_SESSION, FAILURE_SESSION, PRE_E1_SESSION, SUCCESS_SESSION, _rows,
)

GEN = "2026-07-09 12:00"
SDIR = Path("/tmp/sessions")


def _render(sessions=(), skipped_sessions=(), days=(), skipped_spend=()):
    return render_dashboard(list(sessions), list(skipped_sessions), list(days),
                            list(skipped_spend), generated_at=GEN, sessions_dir=SDIR)


def test_thin_badge_and_header():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert "thin: 1 runs" in html
    assert GEN in html


def test_empty_state_names_dir_and_fix():
    html = _render()
    assert str(SDIR) in html
    assert "persist" in html.lower()          # points at the Slice A fix


def test_run_table_metrics_and_na_markers():
    html = _render(sessions=_rows(SUCCESS_SESSION, PRE_E1_SESSION))
    assert "ai coding agents" in html
    assert "0.97" in html and "0.88" in html            # citation P/R when present
    assert "n/a (pre-E1 run)" in html                    # missing citation keys on old run
    assert "n/a (pre-E4 run)" in html                    # missing velocity keys on old run
    assert "why-now" in html.lower()


def test_spend_section_uses_caps():
    html = _render(sessions=_rows(SUCCESS_SESSION),
                   days=[SpendDay("2026-07-07", 1.0485, [{"amount": 1.0485}])])
    assert "$10.00/day" in html and "$50.00/mo" in html
    assert "1.05" in html
    # per-run tier cap from tiers.py (standard = $1.50), never hardcoded prose
    assert "1.50" in html


def test_failure_and_health_section():
    html = _render(sessions=_rows(SUCCESS_SESSION, FAILURE_SESSION, EMPTY_SESSION))
    assert "panel collapsed" in html
    assert "fuse" in html
    assert "sonar" in html


def test_rerun_block_present():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert "uv run python -m council.discovery" in html
    assert "ai-coding-agents-rerun-idea-ledger.md" in html


def test_footer_lists_skipped_files():
    html = _render(sessions=_rows(SUCCESS_SESSION),
                   skipped_sessions=[("pm3-t0-ai-coding-assistants-2026-06-30.json",
                                      "foreign shape (not a session record)")],
                   skipped_spend=[("council-spend-2026-07-01.json", "malformed ledger (KeyError)")])
    assert "pm3-t0-ai-coding-assistants-2026-06-30.json" in html
    assert "council-spend-2026-07-01.json" in html


def test_pm3_slot_and_discrepancies():
    html = _render(sessions=_rows(SUCCESS_SESSION), days=[SpendDay("2026-07-05", 0.5, [{}])])
    assert "Pain-taxonomy movement" in html and "7/21" in html
    assert "no session" in html                          # 07-05 spend, no session


def test_topic_html_escaped():
    evil = {**SUCCESS_SESSION, "topic": "<script>alert(1)</script>"}
    html = _render(sessions=_rows(evil))
    assert "<script>alert(1)" not in html
    assert "&lt;script&gt;" in html


def test_no_javascript():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert "<script" not in html
