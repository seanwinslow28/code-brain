"""The viewer renderer — one self-contained HTML per engagement, to DESIGN.md (#292)."""
import re
import shutil
from pathlib import Path

import pytest

from synth import build
from tracekit import KIT_NAME, KIT_VERSION
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
    m = re.search(rf'<details class="pass[^"]*" id="{pid}".*?</details>', html, re.S)
    assert m, f"no row for {pid}"
    return m.group(0)


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
    assert "Rung 0 is clean on 9 of 9 checks" in line


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
