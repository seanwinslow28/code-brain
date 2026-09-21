"""The viewer renderer — one self-contained HTML per engagement, to DESIGN.md (#292)."""
import re
import shutil
from pathlib import Path

import pytest

from synth import build
from tracekit import KIT_NAME, KIT_VERSION
from tracekit.checker import row_block
from tracekit.engagement import load_engagement
from tracekit.viewer import render, render_html


@pytest.fixture(scope="module")
def eng_dir(tmp_path_factory) -> Path:
    return build(tmp_path_factory.mktemp("eng") / "pc-eng-000-callboard")


@pytest.fixture(scope="module")
def html(eng_dir) -> str:
    return render_html(load_engagement(eng_dir), rendered_on="2026-09-13")


def copy_of(eng_dir: Path, tmp_path: Path) -> Path:
    dst = tmp_path / "pc-eng-000-callboard"
    shutil.copytree(eng_dir, dst)
    return dst


def row(html: str, pid: str) -> str:
    block = row_block(html, pid)
    assert block, f"no row for {pid}"
    return block


def test_self_contained_no_network(html):
    assert "<link" not in html
    assert 'src="http' not in html and "src='http" not in html
    assert "url(http" not in html and "@import" not in html
    assert html.count("data:font/woff2;base64,") == 2


def test_anatomy_in_fixed_order(html):
    marks = ["<h1>pc-eng-000 · Callboard", 'class="reading"', 'class="counter"', "<h2>Where it broke</h2>",
             "<h2>The train</h2>", "<h2>Passes</h2>", "<h2>What comes later</h2>", "<footer>"]
    positions = [html.index(m) for m in marks]
    assert positions == sorted(positions)


def test_synthetic_badge_only_when_the_brief_says_so(eng_dir, tmp_path, html):
    assert 'class="synthetic"' in html
    d = copy_of(eng_dir, tmp_path)
    p = d / "brief.md"
    p.write_text(p.read_text().replace("synthetic: true", "synthetic: false"))
    real = render_html(load_engagement(d))
    assert 'class="synthetic"' not in real
    assert "REAL" not in real


def test_reading_line_composes_from_the_data(html):
    line = re.search(r'<p class="reading">(.*?)</p>', html, re.S).group(1)
    assert "<strong>25 passes</strong>" in line
    assert "<strong>22 are labeled</strong>" in line
    assert "18 pass, 4 fail" in line
    assert "<strong>3 wait for a verdict.</strong>" in line
    assert "broke first at stage 1" in line
    assert "stage-3 break is the one that cost downstream work" in line
    assert "Rung 0 is clean on 10 of 10 checks" in line


def test_reading_line_still_parses_with_nothing_labeled(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    (d / "trace" / "labels.md").unlink()
    page = render_html(load_engagement(d))
    line = re.search(r'<p class="reading">(.*?)</p>', page, re.S).group(1)
    assert "<strong>0 are labeled</strong>" in line
    assert "No break has been labeled yet" in line
    assert "No fails labeled yet" in page
    assert "Next unlabeled: <a" in page


def test_every_string_from_a_record_or_label_is_escaped(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    p = d / "trace" / "labels.md"
    p.write_text(p.read_text().replace("| pass-04 | pass |  |  |", "| pass-04 | pass |  | <script>alert(1)</script> |"))
    page = render_html(load_engagement(d))
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "<script>alert(1)" not in page


def test_blind_pair_hides_runtime_and_launch_until_both_are_labeled(eng_dir, tmp_path, html):
    trial, base = row(html, "pass-18"), row(html, "pass-16")
    assert "codex" not in trial and "hidden" in trial
    assert "claude-sonnet-5" not in base and "hidden" in base
    assert "Blind pair with pass-16" in trial and "Blind pair with pass-18" in base
    d = copy_of(eng_dir, tmp_path)
    p = d / "trace" / "labels.md"
    p.write_text(p.read_text().replace("| pass-18 |  |  |  |", "| pass-18 | pass |  | Tighter than the baseline. |"))
    page = render_html(load_engagement(d))
    assert "codex gpt-5.6-sol high" in row(page, "pass-18")
    assert "claude-sonnet-5" in row(page, "pass-16")


def test_shadow_and_baseline_tags(html):
    assert "shadow of pass-16" in row(html, "pass-18")
    assert "baseline of pass-18" in row(html, "pass-16")


def test_bounce_loop_chip_names_the_trigger(html):
    assert "pass-02" in row(html, "pass-03") and "i-loop" in row(html, "pass-03")


def test_moves_show_counts_and_only_non_kept_lines(html):
    r = row(html, "pass-03")
    assert "<b>1</b> kept" in r and "<b>1</b> split" in r and "<b>1</b> dropped" in r
    assert "GP-1 → GP-a, GP-b" in r
    assert "B1–B3" not in r.split("Kept items")[0].split("Moves</h4>")[1]
    assert "Kept items are listed in the artifact" in r


def test_moves_absence_states_its_reason(html):
    assert "hands no artifact forward" in row(html, "pass-02")
    assert "overwritten in place" in row(html, "pass-01")


def test_unmeasured_meter_never_reads_zero(html):
    r = row(html, "pass-25")
    assert "UNMEASURED" in r
    assert ">0<" not in r


def test_verdicts_are_glyph_and_word_never_color(html):
    r = row(html, "pass-13")
    assert "#i-cross" in r and ">fail<" in r
    css = html.split("<style>")[1].split("</style>")[0]
    assert not re.search(r"\bred\b|#[cdef][0-9a-f]0000", css, re.I)  # no status color, DESIGN.md §3


def test_fails_list_names_upstream_breaks(html):
    section = html.split("Where it broke")[1].split("The train")[0]
    assert "The 4 fails, first failure named" in section
    assert "upstream of the pass read" in section and "at the pass read" in section
    assert "broke at 3 Insights" in section


def test_matrix_derives_last_good_from_first_failing(html):
    section = html.split("Where it broke")[1].split("The train")[0]
    assert "too few for a heat" in section  # 4 fails < 10
    assert section.count("<td class='c1'>") == 4  # four cells with count 1


def test_rung0_checks_are_listed_with_counts(html):
    assert "Rung 0 checks" in html
    assert "Every pass has a record" in html and "25 of 25" in html


def test_growth_slots_and_notes(html, eng_dir, tmp_path):
    for slot in ("Failure taxonomy", "Judge results", "Process notes"):
        assert slot in html
    assert "Synthetic process notes." in html
    d = copy_of(eng_dir, tmp_path)
    (d / "trace" / "notes.md").unlink()
    assert "No notes file yet." in render_html(load_engagement(d))


def test_footer_states_provenance_and_kit(html):
    assert "Rendered 2026-09-13 from 25 records and 22 label rows." in html
    assert "The records are the truth; this page is a view of them." in html
    assert f"{KIT_NAME} · kit {KIT_VERSION}" in html


def test_size_stays_under_the_design_ceiling(html):
    assert len(html.encode("utf-8")) < 400_000


def test_render_writes_into_the_trace_folder(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    out = render(d)
    assert out == d / "trace" / "eval.html" and out.is_file()
    assert render(d, out=tmp_path / "elsewhere.html") == tmp_path / "elsewhere.html"


def test_stage_column_and_seat_names(html):
    r = row(html, "pass-12")
    assert ">Growth<" in r and "4 Growth" in r
    assert "close" in row(html, "pass-25")


# --------------------------------------------------------------------------- #
# phase 3 of the eval learning plan: what you are judging, and guided reading
# --------------------------------------------------------------------------- #


def chapter(html: str, key: str) -> str:
    block = row_block(html, f"case-{key}")
    assert block, f"no chapter for {key}"
    return block


def test_the_four_statements_carry_live_values(html):
    section = html.split("<h2>What you are judging</h2>")[1].split("<h2>What happened in this review</h2>")[0]
    assert "Record checks" in section and "<b>10 of 10</b> pass" in section
    assert "Automated checks of the records, not a quality score." in section
    assert "Reviewer findings" in section and "note" in section and "check record" in section
    assert "A seat's assessment of one artifact and revision." in section
    assert "Your labels" in section and "Labeled <b>22 of 25</b>" in section
    assert "Owner decisions" in section and "never fills one in" in section
    for kind, prompt in [("draft", "answer the assigned question"), ("audit", "supported, consequential"),
                         ("repair", "without creating a material contradiction"), ("gate", "decision authority clear")]:
        assert f"<th scope='row'>{kind}</th>" in section and prompt in section
    assert "not an automated grader" in section


def test_what_happened_leads_with_the_written_intro_then_the_counts(html):
    section = html.split("<h2>What happened in this review</h2>")[1].split("<h2>Guided reading</h2>")[0]
    intro = section.index('<p class="intro">')
    assert intro < section.index('<p class="reading">') < section.index('class="counter"')
    assert "A made-up studio planned a casting tool" in section


def test_no_cases_file_renders_an_honest_empty_section(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    (d / "trace" / "cases.md").unlink()
    page = render_html(load_engagement(d))
    assert "No cases have been written for this engagement yet." in page
    assert "cases-template.md" in page and "<code>trace/cases.md</code>" in page
    assert "No plain-language summary has been written" in page
    assert '<p class="reading">' in page                       # the counts sentence still stands


def test_a_worked_case_shows_story_evidence_and_reasoning_open(html):
    c = chapter(html, "pass-02-1")
    assert 'data-assist="worked"' in c and c.startswith("<details class=\"chapter\"") and " open>" in c.split(">")[0] + ">"
    assert "Source excerpt" in c and "Fingerprint" in c
    assert '<div class="reveal open">' in c
    assert "The reviewer's reasoning" in c
    assert "data-locked" not in c
    assert "audits/gate-1-r1.md:16" in c                       # the excerpt resolved to its line


def test_an_independent_case_keeps_the_diagnosis_and_reveal_folded(html):
    c = chapter(html, "pass-13")
    assert 'data-assist="independent"' in c
    assert 'data-locked="1"' in c and "Show the diagnosis" in c
    assert c.index('data-practice="pass-13"') < c.index('data-locked="1"')   # the question comes first
    assert "the reviewer of this run recorded the failure one stage upstream" in c.split('data-locked="1"')[1]
    assert "<blockquote>" in c.split('data-practice="pass-13"')[0]           # evidence is up front


def test_a_hint_case_folds_its_hint_and_its_reveal(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    p = d / "trace" / "cases.md"
    p.write_text(p.read_text().replace("assist: worked", "assist: hint"))
    page = render_html(load_engagement(d))
    c = chapter(page, "pass-02-1")
    assert 'data-assist="hint"' in c
    assert 'data-exposure="hint"' in c and "Give me one hint" in c
    assert 'data-exposure="reveal"' in c and '<div class="reveal open">' not in c
    assert c.index("Explanation") < c.index("Give me one hint")             # the story stays open


def test_a_changed_source_qualifies_the_case_instead_of_quoting_it(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    src = d / "audits" / "gate-1-r1.md"
    src.write_text(src.read_text() + "\nA line added after the case was written.\n")
    page = render_html(load_engagement(d))
    c = chapter(page, "pass-02-1")
    assert "The source changed since this story was written" in c
    assert "GP-1 rests on an unstated assumption" not in c
    assert "read it as a qualified story" in c


def test_a_broken_case_is_reported_on_the_page_never_dropped_silently(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    p = d / "trace" / "cases.md"
    p.write_text(p.read_text().replace("assist: independent", "assist: whenever"))
    page = render_html(load_engagement(d))
    assert "did not check out" in page and "assist must be one of" in page
    assert "case-pass-13" not in page


def test_practice_notes_are_kept_apart_from_the_labels_draft(html):
    assert "'trace-practice:' + TRACE_ENG" in html and "'trace-labels:' + TRACE_ENG" in html
    assert "never touch the labels file" in html
    assert "Copy practice notes" in html and "Download backup" in html and "Restore backup" in html
    c = chapter(html, "pass-02-1")
    assert "data-practice-note" in c and "data-crit" not in c               # no label field inside a case


def test_row_summaries_lead_with_the_plain_run_line(html):
    r = row(html, "pass-12")
    summary = r.split("</summary>")[0]
    assert "<b>Run 12</b>" in summary and ">Growth<" in summary and ">draft<" in summary
    assert '<span class="pid-sub">pass-12</span>' in summary
    assert "Run 25" in row(html, "pass-25") and "close" in row(html, "pass-25")


def test_label_captions_use_the_plan_wording(html):
    r = row(html, "pass-12")
    assert "Your verdict: pass / fail" in r
    assert "Where did the problem first enter the workflow?" in r
    assert "What led to your judgment? Name the evidence and the consequence." in r
    assert "Critique, one to three sentences" not in html


def test_record_metadata_sits_behind_one_disclosure_after_the_artifact(html):
    r = row(html, "pass-12")
    assert '<details class="record-details">' in r and "<summary>Record details</summary>" in r
    body = r.split("</summary>", 1)[1]
    assert body.index("Checks on this pass") < body.index("Moves") < body.index("Record details")
    meta = r.split('<details class="record-details">')[1]
    for field in ("launch form", "raw log", "Inputs, hashed", "Withheld", "Outputs", "meter"):
        assert field in meta
    assert "launch form" not in r.split('<details class="record-details">')[0]


def test_rung_zero_shows_reasons_and_an_implication_not_a_bare_count(eng_dir, tmp_path, html):
    assert "Record checks" in html and "Rung 0 checks are the nine deterministic checks" in html
    assert ">verified<" in html
    d = copy_of(eng_dir, tmp_path)
    (d / "trace" / "pass-25-coordinator-close.md").unlink()
    page = render_html(load_engagement(d))
    section = page.split("<h3>Record checks</h3>")[1].split("</ul>")[1]
    assert "has no record" in page and ">failed<" in page
    assert "A pass with no record is work this page cannot show you." in page


def test_the_notes_column_leads_with_three_takeaways_and_names_its_author(eng_dir, tmp_path, html):
    slot = html.split("Process notes")[1]
    assert "The coordinator's running notes" in slot
    assert 'class="takeaways"' in slot
    d = copy_of(eng_dir, tmp_path)
    p = d / "trace" / "notes.md"
    p.write_text("- 2026-10-06 First note.\n- 2026-10-07 Second note.\n- 2026-10-08 Third note.\n- 2026-10-09 Fourth note.\n")
    page = render_html(load_engagement(d))
    slot = page.split("Process notes")[1]
    assert slot.count("<li>") >= 7                                          # three takeaways plus the full history
    assert "The full dated history, 4 entries" in slot
    assert slot.index("Third note.") < slot.index("Fourth note.")


# --------------------------------------------------------------------------- #
# #297 · a meter the runtime reported as one number
# --------------------------------------------------------------------------- #


def test_a_total_only_meter_renders_as_a_total_and_says_it_is_not_split(eng_dir, tmp_path):
    d = copy_of(eng_dir, tmp_path)
    rec = sorted((d / "trace").glob("pass-05-*.md"))[0]
    text = "\n".join(x for x in rec.read_text().split("\n") if not x.startswith(("  input:", "  output:", "  cached:")))
    rec.write_text(text.replace("meter:\n", "meter:\n  total: 203700\n"))
    out = render_html(load_engagement(d), rendered_on="2026-09-13")
    block = row_block(out, "pass-05")
    assert "203,700 total" in block
    assert "not split" in block
    assert "UNMEASURED" not in block
