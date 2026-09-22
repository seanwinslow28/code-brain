"""The content machine's trace kit (#291): the profile, line 8, rep-id moves, labels on stages 0–6, the two CLIs."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from machine import BANNED_FROM_SHAPING, CONTENT_MACHINE, KIT_DIR, REP_ID, shapes_check
from deck_synth import build
from tracekit.checker import CHECK_NAMES, STRUCTURE_CHECKS, check_names, run_checks
from tracekit.engagement import load_engagement
from tracekit.labels import LabelsError, parse_labels
from tracekit.moves import extract_ids
from tracekit.viewer import render_html

TRACE = Path(__file__).resolve().parents[1]
REPO = TRACE.parents[3]


@pytest.fixture
def run_dir(tmp_path) -> Path:
    return build(tmp_path / "2026-10-06-x-deck")


def load(d: Path):
    return load_engagement(d, repo=REPO, studio=CONTENT_MACHINE)


def results(d: Path) -> dict:
    return {c.name: c for c in run_checks(load(d))}


def edit(p: Path, old: str, new: str) -> None:
    text = p.read_text()
    assert old in text, f"{old!r} not in {p}"
    p.write_text(text.replace(old, new, 1))


def rehash(run_dir: Path, rel: str, old_hash: str) -> None:
    """After editing an artifact as if its pass had written it, re-point every record at the new hash."""
    new = hashlib.sha256((run_dir / rel).read_bytes()).hexdigest()
    for rec in (run_dir / "trace").glob("pass-*.md"):
        t = rec.read_text()
        if old_hash in t:
            rec.write_text(t.replace(old_hash, new))


def shape_record(run_dir: Path, n: int) -> Path:
    return next((run_dir / "trace").glob(f"pass-{4 + n:02d}-shaper-shape.md"))


# ---- the profile ------------------------------------------------------------


def test_profile_is_the_machines_numbering_and_registers_line_8():
    assert CONTENT_MACHINE.all_stage_numbers == [0, 1, 2, 3, 4, 5, 6]
    assert CONTENT_MACHINE.coordinator_stage is None            # stage 0 is the Oracle, a real stage
    assert CONTENT_MACHINE.forward_kinds == ("shape",)          # only the shaper owns `## Moves`
    assert STRUCTURE_CHECKS["content-machine"] is shapes_check
    names = check_names(CONTENT_MACHINE)
    assert names[7] == "Each shape ran in the clean context, was gated, and reached the pick"
    assert names[:7] == CHECK_NAMES[:7] and names[8:] == CHECK_NAMES[8:]


def test_kit_is_imported_not_copied():
    import tracekit
    assert Path(tracekit.__file__).resolve().parent.parent == KIT_DIR
    assert not (TRACE / "tracekit").exists()


# ---- the clean synthetic run --------------------------------------------------


def test_clean_synthetic_run_passes_every_line(run_dir):
    checks = run_checks(load(run_dir))
    assert [c.name for c in checks] == list(check_names(CONTENT_MACHINE))
    assert [(c.name, c.findings) for c in checks if not c.ok] == []
    counts = {c.name: (c.n_ok, c.n_total) for c in checks}
    assert counts["Every pass has a record"] == (15, 15)
    assert counts["Each shape ran in the clean context, was gated, and reached the pick"] == (3, 3)
    assert counts["Every move names an existing upstream item; splits are subsets"] == (7, 7)


def test_corpus_line_is_a_note_for_this_studio(run_dir):
    c = results(run_dir)["Cited corpus files appear in the transcript's file reads"]
    assert c.ok and c.n_total == 0 and "checked under Moves" in c.notes[0]


# ---- line 8: the clean context ----------------------------------------------


def test_a_banned_file_in_the_shaping_context_is_a_finding(run_dir):
    rec = shape_record(run_dir, 1)
    edit(rec, "  - path: do-not-promote.md", f"  - path: {BANNED_FROM_SHAPING[0]}\n    sha256: {'0' * 64}\n  - path: do-not-promote.md")
    edit(rec, "- do-not-promote.md", f"- {BANNED_FROM_SHAPING[0]}\n- do-not-promote.md")
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert not c.ok
    assert any("banned from it" in f and "pass-05" in f for f in c.findings)


def test_a_shape_with_no_story_is_a_finding(run_dir):
    rec = shape_record(run_dir, 1)
    text = rec.read_text()
    story = re.search(r"  - path: (stimulus/[^\n]+)\n    sha256: [0-9a-f]{64}\n", text)
    rec.write_text(text.replace(story.group(0), "", 1).replace(f"- {story.group(1)}\n", "", 1))
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert any("writes from nothing" in f for f in c.findings)


def test_handed_but_never_opened_is_a_finding(run_dir):
    rec = shape_record(run_dir, 3)
    edit(rec, "- voice-samples.md\n", "")
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert any("never opened" in f and "voice-samples.md" in f for f in c.findings)


def test_an_ungated_shape_is_a_finding(run_dir):
    for g in (run_dir / "trace").glob("pass-*-gate.md"):
        if "pass-08" in g.name or "pass-09" in g.name:   # both gates on card 1
            g.unlink()
    rec = shape_record(run_dir, 1)
    text = rec.read_text()
    text = re.sub(r"  - pass: pass-0[89]\n    kind: gate\n    verdict: [^\n]+\n", "", text)
    rec.write_text(text)
    # renumbering is not the point here: line 8 must name the ungated shape regardless of line 2
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert any("no gate record fired" in f and "pass-05" in f for f in c.findings)


def test_a_gate_missing_from_checks_is_a_finding(run_dir):
    rec = shape_record(run_dir, 2)
    text = rec.read_text()
    rec.write_text(re.sub(r"  - pass: pass-10\n    kind: gate\n    verdict: [^\n]+\n", "", text))
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert any("not in its `checks`" in f and "pass-10" in f for f in c.findings)


def test_an_unpicked_shape_is_a_note_while_open_and_a_finding_once_closed(run_dir):
    pick = next((run_dir / "trace").glob("pass-14-sean-pick.md"))
    text = pick.read_text()
    pick.write_text(re.sub(r"  - path: 3-orrery-forty-lines\.md\n    sha256: [0-9a-f]{64}\n", "", text))
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert any("no stage-5 pick" in f and "pass-07" in f for f in c.findings)
    edit(run_dir / "run.md", "closed: 2026-10-06", "closed: null")
    c = results(run_dir)["Each shape ran in the clean context, was gated, and reached the pick"]
    assert c.ok and any("still open" in n and "pass-07" in n for n in c.notes)


# ---- moves name real reps in the clean context ----------------------------------


def test_rep_ids_are_whole_tokens():
    assert extract_ids("Rep 7e from corpus/06", REP_ID) == ["Rep 7e"]
    assert extract_ids("Rep 1 + Rep 3 → the closing line", REP_ID) == ["Rep 1", "Rep 3"]
    assert extract_ids("the Tuesdays turn from the block", REP_ID) == []


def test_a_move_naming_a_rep_not_in_the_context_is_a_finding(run_dir):
    card = run_dir / "1-quillfeather-terminal-changelog.md"
    before = hashlib.sha256(card.read_bytes()).hexdigest()
    edit(card, "- kept — Rep 2 from", "- kept — Rep 99 from")
    rehash(run_dir, card.name, before)
    c = results(run_dir)["Every move names an existing upstream item; splits are subsets"]
    assert any("Rep 99" in f and "pass-05" in f for f in c.findings)


def test_rep_7_does_not_satisfy_a_line_that_named_rep_7e(run_dir):
    corpus = run_dir / "corpus" / "06-short-form-and-exercises.md"
    before = hashlib.sha256(corpus.read_bytes()).hexdigest()
    edit(corpus, "### Rep 7e — the invoice", "### Rep 7 — the invoice (renamed)")
    rehash(run_dir, "corpus/06-short-form-and-exercises.md", before)
    c = results(run_dir)["Every move names an existing upstream item; splits are subsets"]
    assert any("Rep 7e" in f and "pass-07" in f for f in c.findings)


def test_a_shape_without_a_moves_section_is_a_finding(run_dir):
    card = run_dir / "3-orrery-forty-lines.md"
    before = hashlib.sha256(card.read_bytes()).hexdigest()
    edit(card, "## Moves", "## Moves I made")
    rehash(run_dir, card.name, before)
    c = results(run_dir)["Every move names an existing upstream item; splits are subsets"]
    assert any("no `## Moves` section" in f and "pass-07" in f for f in c.findings)


# ---- labels on the machine's stages ------------------------------------------------


def test_first_failing_stage_runs_0_to_6():
    header = "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n"
    ok = parse_labels(header + "| pass-01 | fail | 0 | the Oracle decked a spike with no ending | |\n",
                      stages=CONTENT_MACHINE.all_stage_numbers)
    assert ok["pass-01"].first_failing_stage == 0
    with pytest.raises(LabelsError, match="0–6"):
        parse_labels(header + "| pass-01 | fail | 7 | x | |\n", stages=CONTENT_MACHINE.all_stage_numbers)


def test_a_label_row_outside_the_machines_stages_fails_line_1(run_dir):
    edit(run_dir / "trace" / "labels.md", "| pass-06 | fail | 3 |", "| pass-06 | fail | 7 |")
    c = results(run_dir)["Records parse and carry every required field"]
    assert any("labels.md" in f and "0–6" in f for f in c.findings)


def test_a_record_on_a_stage_the_machine_lacks_fails_line_1(run_dir):
    edit(shape_record(run_dir, 1), "stage: 3", "stage: 7")
    c = results(run_dir)["Records parse and carry every required field"]
    assert any("stage must be an integer 0–6" in f for f in c.findings)


# ---- the viewer on the machine's names -----------------------------------------------


def test_render_uses_the_machines_stages_and_names(run_dir):
    html = render_html(load(run_dir), rendered_on="2026-10-06")
    assert "Content Machine" in html and "productcraft/trace" in html          # the studio, and the kit it imports
    for label in ("0 Oracle", "3 Shape", "4 Gates", "6 Lessons"):
        assert label in html
    assert "Strategist" not in html and "Leadership" not in html
    assert "<th scope='col'>0</th>" in html and "<th scope='col'>6</th>" in html and "<th scope='col'>7</th>" not in html
    assert "start " in html                                                       # the matrix's first row
    assert "broke at 3 Shape" in html                                              # the one labeled fail
    assert 'x="64"' in html and ">gate</text>" in html                             # gate seats drawn as gates in the train
    assert "<script src" not in html and "<link" not in html and "http://" not in html and "https://" not in html.replace("https://github.com", "")


def test_render_shows_the_advisory_gate_finding(run_dir):
    html = render_html(load(run_dir), rendered_on="2026-10-06")
    assert "<b>1</b> note" in html and "in <code>gates/</code>" in html


# ---- the two commands, on the system python ------------------------------------------


def run(*args):
    return subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True, cwd=TRACE)


def test_check_cli(run_dir):
    r = run("check.py", str(run_dir))
    assert r.returncode == 0, r.stderr
    assert "PASS  Each shape ran in the clean context, was gated, and reached the pick  3 of 3" in r.stdout
    assert r.stdout.count("PASS") == 10
    data = json.loads(run("check.py", str(run_dir), "--json").stdout)
    assert len(data) == 10 and all(c["ok"] for c in data)


def test_check_cli_exits_one_on_a_finding_and_two_off_a_run(run_dir, tmp_path):
    (run_dir / "trace" / "pass-14-sean-pick.md").unlink()
    r = run("check.py", str(run_dir))
    assert r.returncode == 1 and "pass-14 has no record" in r.stdout
    assert run("check.py", str(tmp_path / "nowhere")).returncode == 2


def test_render_cli(run_dir, tmp_path):
    r = run("render.py", str(run_dir))
    assert r.returncode == 0, r.stderr
    assert (run_dir / "trace" / "eval.html").is_file() and "rung 0 clean" in r.stdout
    out = tmp_path / "elsewhere.html"
    assert run("render.py", str(run_dir), "--out", str(out)).returncode == 0 and out.is_file()


# ---- privacy ------------------------------------------------------------------------


def test_synth_refuses_the_private_brain(tmp_path):
    with pytest.raises(SystemExit):
        build(tmp_path / "creative-studio" / "content-machine" / "pieces" / "x")
    with pytest.raises(SystemExit):
        build(tmp_path / "ledger" / "x")


def test_run_folders_are_ignored_by_git():
    r = subprocess.run(["git", "check-ignore", "-q", "creative-studio/content-machine/pieces/x/trace/pass-01-shaper-shape.md"],
                       cwd=REPO)
    assert r.returncode == 0
