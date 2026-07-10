# tests/discovery/test_dashboard.py
import json

import pytest

from council.discovery.dashboard import SpendDay, load_sessions, load_spend

SUCCESS_SESSION = {
    "id": "20260707-101500-abc123", "topic": "ai coding agents", "lens": "pm",
    "tier": "standard", "segment": "developer", "evidence_count": 40, "verified": 9,
    "dropped": 2, "merged_count": 1, "cost_usd": 1.05,
    "gather_status": {"sonar": "ok: 15 records (15 found)", "web": "ok: 6 records (6 found)"},
    "blind_spots": [], "contradictions": [], "supplement": None,
    "verify_mode": "nli", "citation_precision": 0.97, "citation_recall": 0.88,
    "velocity_mode": "off", "why_now_coverage": 0.0,
}

PRE_E1_SESSION = {  # 2026-06-21 vintage: no citation/velocity/merged/segment keys
    "id": "20260621-133044-0c8894", "topic": "2D animation pipelines", "lens": "pm",
    "tier": "standard", "evidence_count": 26, "verified": 12, "dropped": 0,
    "cost_usd": 2.7369, "gather_status": {"sonar": "ok: 15 records (15 found)"},
    "blind_spots": [], "contradictions": [],
}

FAILURE_SESSION = {
    "id": "20260630-172729-4ee6bd", "topic": "broken run", "lens": "pm", "tier": "quick",
    "evidence_count": 12, "gather_status": {"sonar": "ok: 12 records (12 found)"},
    "failed_stage": "fuse", "error": "panel collapsed", "cost_usd": 0.11,
}

EMPTY_SESSION = {
    "id": "20260709-090000-eeeeee", "topic": "niche topic", "lens": "pm", "tier": "quick",
    "segment": "", "empty": True, "cost_usd": 0.018,
    "gather_status": {"sonar": "ok: 0 records (0 found)"},
    "verify_mode": "substring-only", "citation_precision": None, "citation_recall": None,
    "velocity_mode": "off", "why_now_coverage": 0.0,
}

FOREIGN_BUNDLE = {  # pm3-t0 shape: an evidence-bundle capture, not a session record
    "stamp": "t0", "date": "2026-06-30", "topic": "ai coding assistants",
    "tier": "standard", "lens": "pm", "verified_count": 8, "dropped_count": 2,
    "cost_usd": 1.8465, "evidence_count": 93, "gather_cost_usd": 0.02984,
    "bundle": {"records": [], "gather_cost_usd": 0.02984},
}


def _write_sessions(d, **files):
    d.mkdir(parents=True, exist_ok=True)
    for name, payload in files.items():
        p = d / f"{name}.json"
        p.write_text(payload if isinstance(payload, str) else json.dumps(payload))


def test_load_sessions_classifies_and_sorts(tmp_path):
    d = tmp_path / "s"
    _write_sessions(d, ok=SUCCESS_SESSION, old=PRE_E1_SESSION,
                    fail=FAILURE_SESSION, empty=EMPTY_SESSION)
    sessions, skipped = load_sessions(d)
    assert skipped == []
    assert [s["_kind"] for s in sessions] == ["success", "failure", "success", "empty"]
    assert [s["_date"] for s in sessions] == ["2026-06-21", "2026-06-30", "2026-07-07", "2026-07-09"]
    assert sessions[0]["_file"] == "old.json"


def test_load_sessions_skips_foreign_and_malformed(tmp_path):
    d = tmp_path / "s"
    _write_sessions(d, ok=SUCCESS_SESSION, bundle=FOREIGN_BUNDLE, broken="{not json")
    sessions, skipped = load_sessions(d)
    assert len(sessions) == 1
    reasons = dict(skipped)
    assert "foreign" in reasons["bundle.json"]
    assert "malformed" in reasons["broken.json"]


def test_load_sessions_missing_dir(tmp_path):
    sessions, skipped = load_sessions(tmp_path / "nope")
    assert sessions == [] and skipped == []


def test_load_spend_filters_to_discovery(tmp_path):
    d = tmp_path / "health"
    d.mkdir()
    (d / "council-spend-2026-07-07.json").write_text(json.dumps({
        "date": "2026-07-07", "total": 1.34,
        "runs": [
            {"amount": 1.0485, "profile": "standard", "tag": "discovery-pm", "tool": "discovery"},
            {"amount": 0.29, "profile": "premium", "tag": "critique", "tool": "council"},
        ],
    }))
    (d / "council-spend-2026-07-05.json").write_text(json.dumps({
        "date": "2026-07-05", "total": 0.29,
        "runs": [{"amount": 0.29, "profile": "premium", "tag": "critique", "tool": "council"}],
    }))
    days, skipped = load_spend(d)
    assert skipped == []
    assert [f"{x.date}:{x.discovery_total}" for x in days] == ["2026-07-05:0.0", "2026-07-07:1.0485"]
    assert len(days[1].runs) == 1


def test_load_spend_skips_malformed(tmp_path):
    d = tmp_path / "health"
    d.mkdir()
    (d / "council-spend-2026-07-01.json").write_text("{oops")
    days, skipped = load_spend(d)
    assert days == []
    assert skipped and "malformed" in skipped[0][1]
