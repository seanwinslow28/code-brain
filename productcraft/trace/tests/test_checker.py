"""Rung 0 — deterministic checks, no model, no network (#272 decision 7)."""
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, format_report, run_checks
from tracekit.engagement import load_engagement


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def results(d: Path) -> dict:
    return {c.name: c for c in run_checks(load_engagement(d))}


def edit(p: Path, old: str, new: str) -> None:
    text = p.read_text()
    assert old in text, f"{old!r} not in {p}"
    p.write_text(text.replace(old, new, 1))


def edit_artifact(eng_dir: Path, rel: str, old: str, new: str) -> None:
    """Edit an artifact *as if the seat had written it*: every record that hashed the old bytes
    (as an input or an output) is re-pointed at the new hash, so only the content changes."""
    import hashlib
    p = eng_dir / rel
    before = hashlib.sha256(p.read_bytes()).hexdigest()
    edit(p, old, new)
    after = hashlib.sha256(p.read_bytes()).hexdigest()
    for rec in (eng_dir / "trace").glob("pass-*.md"):
        t = rec.read_text()
        if before in t:
            rec.write_text(t.replace(before, after))


def test_clean_synthetic_engagement_passes_every_check(eng_dir):
    checks = run_checks(load_engagement(eng_dir))
    assert [c.name for c in checks] == list(CHECK_NAMES)
    failing = [(c.name, c.findings) for c in checks if not c.ok]
    assert failing == []
    counts = {c.name: (c.n_ok, c.n_total) for c in checks}
    assert counts["Every pass has a record"] == (25, 25)
    assert counts["Every pass has a label row"] == (25, 25)


def test_superseded_revision_hashes_are_accepted_as_a_recorded_prior_output(eng_dir):
    # pass-02's input is strategy-pov revision 1, overwritten by pass-03; the chain still holds
    c = results(eng_dir)["Input hashes match disk or a recorded prior revision"]
    assert c.ok and c.n_total > 0
    assert any("superseded" in n for n in c.notes)


def test_missing_record_is_caught_with_the_gap_named(eng_dir):
    (eng_dir / "trace" / "pass-10-discovery-lead-audit.md").unlink()
    c = results(eng_dir)["Every pass has a record"]
    assert not c.ok
    assert any("pass-10" in f for f in c.findings)


def test_filename_must_match_the_record(eng_dir):
    p = eng_dir / "trace" / "pass-10-discovery-lead-audit.md"
    p.rename(eng_dir / "trace" / "pass-10-discovery-lead-draft.md")
    c = results(eng_dir)["Every pass has a record"]
    assert not c.ok and any("pass-10-discovery-lead-draft.md" in f for f in c.findings)


def test_missing_label_row_is_caught(eng_dir):
    edit(eng_dir / "trace" / "labels.md", "| pass-05 | pass |", "| pass-99 | pass |")
    c = results(eng_dir)["Every pass has a label row"]
    assert not c.ok
    assert any("pass-05" in f for f in c.findings)
    assert any("pass-99" in f for f in c.findings)  # a row for a pass that does not exist


def test_unlabeled_rows_count_as_missing_labels(eng_dir):
    c = results(eng_dir)["Every pass has a label row"]
    assert c.ok  # the clean build labels 22 of 25 with rows for all 25
    assert c.n_ok == 25
    edit(eng_dir / "trace" / "labels.md", "| pass-18 |  |", "| pass-18 | |")  # still no verdict
    c = results(eng_dir)["Every pass has a label row"]
    assert c.ok


def test_hash_drift_is_caught_and_names_the_path(eng_dir):
    (eng_dir / "artifacts" / "growth-gtm.md").write_text((eng_dir / "artifacts" / "growth-gtm.md").read_text() + "\nedited after the fact\n")
    c = results(eng_dir)["Input hashes match disk or a recorded prior revision"]
    assert not c.ok
    assert any("artifacts/growth-gtm.md" in f and "pass-13" in f for f in c.findings)


def test_missing_input_file_is_caught(eng_dir):
    (eng_dir / "audits" / "gate-1-r1.md").unlink()
    c = results(eng_dir)["Input hashes match disk or a recorded prior revision"]
    assert not c.ok and any("audits/gate-1-r1.md" in f and "missing" in f for f in c.findings)


def test_cited_corpus_file_not_opened_is_caught(eng_dir):
    edit(eng_dir / "trace" / "pass-14-business-economics-draft.md",
         "- corpus/business/monetizing-innovation.md\n", "")
    c = results(eng_dir)["Cited corpus files appear in the transcript's file reads"]
    assert not c.ok
    assert any("pass-14" in f and "corpus/business/monetizing-innovation.md" in f for f in c.findings)


def test_grounding_full_with_nothing_read_is_caught(eng_dir):
    rec = eng_dir / "trace" / "pass-09-insights-analytics-draft.md"
    edit(rec, "## Corpus read\n\n- corpus/insights/trustworthy-online-experiments.md\n- artifacts/discovery-packet.md\n- artifacts/strategy-pov.md\n",
         "## Corpus read\n\nnone\n")
    c = results(eng_dir)["Cited corpus files appear in the transcript's file reads"]
    assert not c.ok and any("grounding: full" in f and "pass-09" in f for f in c.findings)


def test_move_naming_a_nonexistent_upstream_item_is_caught(eng_dir):
    edit_artifact(eng_dir, "artifacts/growth-gtm.md", "- kept — C1 from pc-eng-000.strategy", "- kept — C9 from pc-eng-000.strategy")
    c = results(eng_dir)["Every move names an existing upstream item; splits are subsets"]
    assert not c.ok
    assert any("pass-12" in f and "C9" in f for f in c.findings)


def test_split_child_that_already_exists_upstream_is_caught(eng_dir):
    edit_artifact(eng_dir, "artifacts/metrics-evidence-plan.md",
                  "- split — OC-1 → OC-1a, OC-1b from pc-eng-000.strategy", "- split — OC-1 → OC-1a, OC-2 from pc-eng-000.strategy")
    c = results(eng_dir)["Every move names an existing upstream item; splits are subsets"]
    assert not c.ok and any("OC-2" in f and "already exists upstream" in f for f in c.findings)


def test_malformed_move_line_is_caught(eng_dir):
    edit_artifact(eng_dir, "artifacts/business-case.md", "- kept — L1 from pc-eng-000.growth", "- tweaked — L1 from pc-eng-000.growth")
    c = results(eng_dir)["Every move names an existing upstream item; splits are subsets"]
    assert not c.ok and any("tweaked" in f for f in c.findings)


def test_unverifiable_moves_are_counted_not_failed(eng_dir):
    # pass-03 keeps B1–B3 "from revision 1", which is superseded; the gate file still names them,
    # so they verify. Make one item findable nowhere readable: it is reported as unverifiable.
    edit_artifact(eng_dir, "audits/gate-1-r1.md", "B1–B3 hold", "the bets hold")
    c = results(eng_dir)["Every move names an existing upstream item; splits are subsets"]
    assert c.ok
    assert c.n_unverifiable >= 1
    assert any("unverifiable" in n for n in c.notes)


def test_meter_source_outside_the_vocabulary_is_caught(eng_dir):
    edit(eng_dir / "trace" / "pass-05-discovery-lead-draft.md", "meter_source: Agent-tool usage", "meter_source: estimated")
    c = results(eng_dir)["Meter present or UNMEASURED"]
    assert not c.ok and any("pass-05" in f and "estimated" in f for f in c.findings)


def test_measured_meter_needs_integers(eng_dir):
    edit(eng_dir / "trace" / "pass-05-discovery-lead-draft.md", "  input: 240100\n", "  input: about 240k\n")
    c = results(eng_dir)["Meter present or UNMEASURED"]
    assert not c.ok and any("pass-05" in f for f in c.findings)


def test_stage_without_its_audit_is_caught(eng_dir):
    (eng_dir / "trace" / "pass-11-product-leadership-audit.md").unlink()
    c = results(eng_dir)["Each drafting stage has one draft, an audit, and its required co-signs"]
    assert not c.ok and any("stage 2" in f and "audit" in f for f in c.findings)


def test_audit_by_the_wrong_seat_is_caught(eng_dir):
    edit(eng_dir / "trace" / "pass-11-product-leadership-audit.md", "seat: product-leadership", "seat: growth-distribution")
    c = results(eng_dir)["Each drafting stage has one draft, an audit, and its required co-signs"]
    assert not c.ok and any("product-leadership" in f and "growth-distribution" in f for f in c.findings)


def test_two_drafts_on_one_stage_is_caught(eng_dir):
    edit(eng_dir / "trace" / "pass-07-discovery-lead-repair.md", "kind: repair", "kind: draft")
    c = results(eng_dir)["Each drafting stage has one draft, an audit, and its required co-signs"]
    assert not c.ok and any("stage 2" in f and "2 drafts" in f for f in c.findings)


def test_stage_structure_is_not_applied_outside_a_full_train(eng_dir):
    edit(eng_dir / "brief.md", "type: full-train", "type: audit")
    (eng_dir / "trace" / "pass-11-product-leadership-audit.md").unlink()
    c = results(eng_dir)["Each drafting stage has one draft, an audit, and its required co-signs"]
    assert c.ok and any("audit" in n and "not a full train" in n for n in c.notes)


def test_blind_broken_by_a_render_that_shows_the_runtime_in_the_row(eng_dir):
    (eng_dir / "trace" / "eval.html").write_text(
        '<html><details class="pass" id="pass-18">ran on codex gpt-5.6-sol high</details>'
        '<details class="pass" id="pass-16">hidden</details></html>')
    c = results(eng_dir)["Trials blind-labeled before their runtime is shown"]
    assert not c.ok and any("pass-18" in f and "eval.html" in f for f in c.findings)


def test_blind_holds_when_the_rows_hide_both_runtimes(eng_dir):
    # gates share the Codex runtime with the trial, so the string may appear elsewhere on the page
    (eng_dir / "trace" / "eval.html").write_text(
        '<html>the gates ran on codex gpt-5.6-sol high'
        '<details class="pass" id="pass-18">hidden</details><details class="pass" id="pass-16">hidden</details></html>')
    assert results(eng_dir)["Trials blind-labeled before their runtime is shown"].ok


def test_blind_cannot_be_verified_on_a_render_without_rows(eng_dir):
    (eng_dir / "trace" / "eval.html").write_text("<html>something else entirely</html>")
    c = results(eng_dir)["Trials blind-labeled before their runtime is shown"]
    assert c.ok and any("no row" in n for n in c.notes)


def test_trial_on_different_inputs_is_caught(eng_dir):
    rec = eng_dir / "trace" / "pass-18-delivery-execution-trial.md"
    edit(rec, "  - path: corpus/delivery/shape-up.md\n", "  - path: corpus/delivery/shelf.md\n")
    c = results(eng_dir)["Trials blind-labeled before their runtime is shown"]
    assert not c.ok and any("pass-18" in f and "identical" in f for f in c.findings)


def test_report_format(eng_dir):
    text = format_report(run_checks(load_engagement(eng_dir)))
    lines = text.strip().split("\n")
    assert lines[0].startswith("PASS  Records parse")
    assert all(l.startswith(("PASS", "FAIL", "  ")) for l in lines)
    assert "25 of 25" in text
