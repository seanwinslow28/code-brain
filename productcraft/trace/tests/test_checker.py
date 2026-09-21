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


# --------------------------------------------------------------------------- #
# #297 · the gaps the first engagement exposed
# --------------------------------------------------------------------------- #

CORPUS = "Cited corpus files appear in the transcript's file reads"
METER = "Meter present or UNMEASURED"
PARSE = "Records parse and carry every required field"


def record(eng_dir: Path, pass_id: str) -> Path:
    hits = sorted((eng_dir / "trace").glob(f"{pass_id}-*.md"))
    assert hits, f"no record for {pass_id}"
    return hits[0]


def test_a_repair_is_not_charged_with_the_citations_its_own_earlier_revision_made(eng_dir):
    """pass-03 redrafts strategy-pov.md in place; the file keeps pass-01's citation.

    Charging the repair with a read that happened in pass-01 is the false finding
    the first engagement hit. The read is accounted for along the artifact's own
    revision chain, and said out loud in a note.
    """
    cite = "corpus/strategy/good-strategy-bad-strategy.md"
    assert cite in (eng_dir / "artifacts/strategy-pov.md").read_text()
    edit(record(eng_dir, "pass-03"), f"- {cite}\n", "")
    c = results(eng_dir)[CORPUS]
    assert c.ok, c.findings
    assert any("earlier revision" in n for n in c.notes)


def test_an_unread_citation_is_still_a_finding_when_no_revision_accounts_for_it(eng_dir):
    cite = "corpus/strategy/good-strategy-bad-strategy.md"
    for pid in ("pass-01", "pass-03"):
        edit(record(eng_dir, pid), f"- {cite}\n", "")
    c = results(eng_dir)[CORPUS]
    assert not c.ok
    assert any("pass-03" in f and cite in f for f in c.findings)


def test_reads_travel_along_one_artifact_only_never_sideways(eng_dir):
    """pass-09 writes a different artifact, so pass-01's reads do not cover its citations."""
    cite = "corpus/insights/trustworthy-online-experiments.md"
    edit(record(eng_dir, "pass-09"), f"- {cite}\n", "")
    c = results(eng_dir)[CORPUS]
    assert not c.ok
    assert any("pass-09" in f and cite in f for f in c.findings)


def test_a_meter_may_report_one_total_as_the_runtime_reported_it(eng_dir):
    """The Agent tool's usage field and the Codex footer each report one number."""
    edit(record(eng_dir, "pass-05"), "meter:\n", "meter:\n  total: 203700\n")
    r = record(eng_dir, "pass-05").read_text()
    for line in ("  input:", "  output:", "  cached:"):
        r = "\n".join(x for x in r.split("\n") if not x.startswith(line))
    record(eng_dir, "pass-05").write_text(r)
    c = results(eng_dir)[METER]
    assert c.ok, c.findings
    assert any("total only" in n for n in c.notes)


def test_a_meter_with_neither_a_split_nor_a_total_is_a_finding(eng_dir):
    p = record(eng_dir, "pass-05")
    text = "\n".join(x for x in p.read_text().split("\n") if not x.startswith(("  input:", "  output:", "  cached:")))
    p.write_text(text)
    c = results(eng_dir)[METER]
    assert not c.ok
    assert any("pass-05" in f and "total" in f for f in c.findings)


def test_a_total_that_is_not_a_whole_token_count_is_a_finding(eng_dir):
    edit(record(eng_dir, "pass-05"), "meter:\n", "meter:\n  total: about 200k\n")
    c = results(eng_dir)[METER]
    assert not c.ok
    assert any("whole token count" in f for f in c.findings)


def test_the_coordinators_open_pass_needs_no_drafting_conversation_withheld(eng_dir):
    """`open` anchors the chain: the brief, entries and frozen evidence, with no seat fired."""
    src = record(eng_dir, "pass-25").read_text()
    src = src.replace("pass: pass-25", "pass: pass-26").replace("kind: close", "kind: open")
    src = "\n".join(x for x in src.split("\n") if x.strip() != "- the drafting conversation")
    (eng_dir / "trace" / "pass-26-coordinator-open.md").write_text(src)
    eng = load_engagement(eng_dir)
    rec = eng.by_id["pass-26"]
    assert rec.kind == "open"
    assert rec.errors == []


def test_readout_is_a_kind_and_an_unknown_kind_still_fails(eng_dir):
    src = record(eng_dir, "pass-25").read_text().replace("pass: pass-25", "pass: pass-26")
    (eng_dir / "trace" / "pass-26-coordinator-readout.md").write_text(src.replace("kind: close", "kind: readout"))
    assert load_engagement(eng_dir).by_id["pass-26"].errors == []
    (eng_dir / "trace" / "pass-26-coordinator-readout.md").unlink()
    (eng_dir / "trace" / "pass-26-coordinator-debrief.md").write_text(src.replace("kind: close", "kind: debrief"))
    c = results(eng_dir)[PARSE]
    assert not c.ok
    assert any("debrief" in f for f in c.findings)


# --------------------------------------------------------------------------- #
# #297 · shared repo machinery as a pass input
# --------------------------------------------------------------------------- #

HASHES = "Input hashes match disk or a recorded prior revision"


@pytest.fixture
def eng_in_repo(tmp_path) -> Path:
    """A synthetic engagement sitting inside a repo that also holds studio machinery."""
    (tmp_path / "CLAUDE.md").write_text("# fake repo root\n")
    tpl = tmp_path / "productcraft" / "templates"
    tpl.mkdir(parents=True)
    (tpl / "strategy-pov.md").write_text("# Strategy & POV template\n\nrevision 1\n")
    return build(tmp_path / "pc-eng-000-callboard")


def add_input(eng_dir: Path, pass_id: str, rel: str, sha: str) -> None:
    p = record(eng_dir, pass_id)
    edit(p, "inputs:\n", f"inputs:\n  - path: {rel}\n    sha256: {sha}\n")


def test_machinery_that_moved_after_the_pass_is_unverifiable_not_tampering(eng_in_repo):
    """A template improves after a train closes; the record keeps the hash the seat saw."""
    import hashlib
    tpl = eng_in_repo.parent / "productcraft" / "templates" / "strategy-pov.md"
    add_input(eng_in_repo, "pass-01", "productcraft/templates/strategy-pov.md",
              hashlib.sha256(tpl.read_bytes()).hexdigest())
    assert results(eng_in_repo)[HASHES].ok
    tpl.write_text(tpl.read_text() + "\n## Diagnosis\n")      # the ticket that fixes the template
    c = results(eng_in_repo)[HASHES]
    assert c.ok, c.findings
    assert c.n_unverifiable == 1
    assert any("shared repo machinery" in n and "strategy-pov.md" in n for n in c.notes)


def test_an_engagement_file_edited_outside_a_pass_is_still_a_finding(eng_in_repo):
    """The guarantee that matters is unchanged: the chain's own files stay strict."""
    (eng_in_repo / "artifacts" / "strategy-pov.md").write_text("tampered\n")
    c = results(eng_in_repo)[HASHES]
    assert not c.ok
    assert any("artifacts/strategy-pov.md" in f for f in c.findings)


def test_a_repo_path_the_engagement_itself_wrote_stays_in_the_chain(eng_in_repo):
    """Machinery means *not written here* — a repo path some pass output is a chain link."""
    import hashlib
    tpl = eng_in_repo.parent / "productcraft" / "templates" / "strategy-pov.md"
    sha = hashlib.sha256(tpl.read_bytes()).hexdigest()
    add_input(eng_in_repo, "pass-03", "productcraft/templates/strategy-pov.md", sha)
    p = record(eng_in_repo, "pass-01")
    edit(p, "outputs:\n", f"outputs:\n  - path: productcraft/templates/strategy-pov.md\n    sha256: {sha}\n")
    tpl.write_text("moved on\n")
    c = results(eng_in_repo)[HASHES]
    assert not c.ok
    assert c.n_unverifiable == 0
    assert any("productcraft/templates/strategy-pov.md" in f for f in c.findings)
