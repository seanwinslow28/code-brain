"""Loading an engagement folder: brief, records, labels, notes, artifacts."""
from pathlib import Path

import pytest

from synth import build
from tracekit.engagement import load_engagement, resolve_path, sha256_path


@pytest.fixture(scope="module")
def eng_dir(tmp_path_factory) -> Path:
    return build(tmp_path_factory.mktemp("eng") / "pc-eng-000-callboard")


def test_records_load_in_pass_order(eng_dir):
    eng = load_engagement(eng_dir)
    assert [r.pass_id for r in eng.records][:3] == ["pass-01", "pass-02", "pass-03"]
    assert len(eng.records) == 25
    assert eng.errors == []


def test_brief_fields(eng_dir):
    eng = load_engagement(eng_dir)
    assert eng.brief["id"] == "pc-eng-000"
    assert eng.brief["name"] == "Callboard"
    assert eng.brief["type"] == "full-train"
    assert eng.brief["synthetic"] is True
    assert eng.brief["pass_budget"] == 26


def test_trace_dir_is_accepted_as_the_path_too(eng_dir):
    a, b = load_engagement(eng_dir), load_engagement(eng_dir / "trace")
    assert a.root == b.root == eng_dir
    assert a.trace_dir == b.trace_dir == eng_dir / "trace"


def test_record_fields(eng_dir):
    eng = load_engagement(eng_dir)
    r = eng.by_id["pass-03"]
    assert (r.seat, r.kind, r.stage, r.runtime) == ("product-strategist", "repair", 1, "claude-opus-5")
    assert r.launch == "Agent tool, fresh context"
    assert r.triggered_by == "pass-02" and r.shadow_of is None
    assert r.inputs[0].path == "artifacts/strategy-pov.md" and len(r.inputs[0].sha256) == 64
    assert r.outputs[0].path == "artifacts/strategy-pov.md" and r.outputs[1].id == "pc-eng-000.d03"
    assert r.checks[0].pass_id == "pass-04" and r.checks[0].kind == "gate"
    assert r.checks[0].verdict.startswith("STRATEGY PASS")
    assert r.meter == {"input": 96700, "output": 9900, "cached": 88000}
    assert r.corpus_read == ["corpus/strategy/good-strategy-bad-strategy.md", "audits/gate-1-r1.md"]
    assert r.moves_pointer == "artifacts/strategy-pov.md § Moves"
    assert r.notes.startswith("Repair against gate r1.")


def test_close_record_has_no_meter(eng_dir):
    r = load_engagement(eng_dir).by_id["pass-25"]
    assert r.kind == "close" and r.stage == 0
    assert r.meter is None and r.meter_source == "UNMEASURED"
    assert r.inputs == []


def test_labels_and_notes(eng_dir):
    eng = load_engagement(eng_dir)
    assert len(eng.labels) == 25
    assert sum(1 for l in eng.labels.values() if l.verdict) == 22
    assert eng.labels["pass-13"].first_failing_stage == 3
    assert eng.notes and "Synthetic process notes." in eng.notes


def test_artifact_moves_are_read_through_the_record(eng_dir):
    eng = load_engagement(eng_dir)
    mv = eng.moves_for(eng.by_id["pass-03"])
    assert mv is not None and mv.counts()["split"] == 1
    assert eng.moves_state(eng.by_id["pass-03"]) == "current"
    # pass-01's origin draft was overwritten in place by the repair (#274): its Moves are no longer on disk
    assert eng.moves_for(eng.by_id["pass-01"]) is None
    assert eng.moves_state(eng.by_id["pass-01"]) == "superseded"
    assert eng.moves_state(eng.by_id["pass-02"]) == "none-kind"  # a gate hands nothing forward
    assert eng.moves_state(eng.by_id["pass-16"]) == "current"


def test_missing_required_field_is_a_record_error_not_a_crash(tmp_path):
    d = build(tmp_path / "e")
    p = d / "trace" / "pass-05-discovery-lead-draft.md"
    p.write_text(p.read_text().replace("meter_source: Agent-tool usage\n", ""))
    eng = load_engagement(d)
    r = eng.by_id["pass-05"]
    assert any("meter_source" in e for e in r.errors)


def test_unparseable_record_lands_in_errors(tmp_path):
    d = build(tmp_path / "e")
    p = d / "trace" / "pass-06-insights-analytics-co-sign.md"
    p.write_text("## no frontmatter\n")
    eng = load_engagement(d)
    assert any("pass-06-insights-analytics-co-sign.md" in e for e in eng.errors)
    assert "pass-06" not in eng.by_id


def test_missing_labels_file_is_empty_not_fatal(tmp_path):
    d = build(tmp_path / "e")
    (d / "trace" / "labels.md").unlink()
    eng = load_engagement(d)
    assert eng.labels == {} and eng.labels_error is None


def test_resolve_path_prefers_the_engagement_then_the_repo(tmp_path):
    root, repo = tmp_path / "eng", tmp_path / "repo"
    (root / "artifacts").mkdir(parents=True)
    (root / "artifacts" / "x.md").write_text("x")
    (repo / "productcraft" / "templates").mkdir(parents=True)
    (repo / "productcraft" / "templates" / "t.md").write_text("t")
    assert resolve_path(root, repo, "artifacts/x.md") == root / "artifacts" / "x.md"
    assert resolve_path(root, repo, "productcraft/templates/t.md") == repo / "productcraft" / "templates" / "t.md"
    assert resolve_path(root, repo, "nowhere.md") is None


def test_directory_hash_is_deterministic_and_content_sensitive(tmp_path):
    d = tmp_path / "a"
    (d / "sub").mkdir(parents=True)
    (d / "one.md").write_text("1")
    (d / "sub" / "two.md").write_text("2")
    h1 = sha256_path(d)
    assert h1 == sha256_path(d) and len(h1) == 64
    (d / "sub" / "two.md").write_text("changed")
    assert sha256_path(d) != h1
