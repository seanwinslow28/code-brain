from datetime import datetime

from lib.job_renderer import render_roll_up, read_roll_up_frontmatter
from lib.job_types import Posting, ScoringResult


def _scored(rid: str, score: int, **overrides) -> tuple[int, Posting, ScoringResult]:
    p_kwargs = dict(
        source="ashby:hopper", source_role_id=rid, url=f"https://x.example/{rid}",
        company="Hopper", title="Senior PM, AI & Commerce",
        location="Remote (US)", salary_disclosed=None,
        posted_at=datetime(2026, 5, 9), description="x",
    )
    p_kwargs.update(overrides)
    s = ScoringResult(
        fit_score=score, role_band="Sr_PM_stretch",
        rationale="Boston-HQ, remote-OK, AI-PM lands cleanly.",
        concerns=["YOE floor 3yr"] if score < 5 else [],
        fit_dimensions={"role_band_fit": score, "geo_fit": 5, "industry_fit": 5, "yoe_fit": 3},
    )
    return (int(rid), Posting(**p_kwargs), s)


def test_render_roll_up_with_strong_medium_weak_buckets(tmp_path):
    today = "2026-05-09"
    scored = [
        _scored("47", 5),
        _scored("48", 5),
        _scored("49", 4),
        _scored("50", 4),
        _scored("51", 3),
        _scored("52", 3),
        _scored("53", 3),
        _scored("54", 3),
        _scored("55", 3),
        _scored("56", 3),
        _scored("57", 2),
        _scored("58", 1),
    ]
    md = render_roll_up(today, scored=scored, unscored=[], complete=True)
    assert md.startswith("---")
    assert "total_surfaced: 12" in md
    assert "top_fits: 4" in md
    assert "medium_fits: 6" in md
    assert "weak_fits: 2" in md
    assert "complete: true" in md
    assert "## Top Fits (≥ 4/5)" in md
    assert "## Medium Fits (3/5)" in md
    assert "## Weak Fits (≤ 2/5)" in md
    assert "Hopper" in md
    assert "db_id:** 47" in md


def test_render_roll_up_unscored_section_present_only_when_needed(tmp_path):
    today = "2026-05-09"
    unscored = [_scored("99", 0)[1]]  # just the posting
    md = render_roll_up(today, scored=[], unscored=unscored, complete=False)
    assert "complete: false" in md
    assert "unscored: 1" in md
    assert "## Unscored — MBP was asleep" in md
    assert "MBP" in md


def test_render_roll_up_omits_unscored_section_when_empty(tmp_path):
    md = render_roll_up("2026-05-09", scored=[_scored("1", 5)], unscored=[], complete=True)
    assert "## Unscored" not in md


def test_read_roll_up_frontmatter_returns_complete_true(tmp_path):
    f = tmp_path / "2026-05-09.md"
    f.write_text("---\ntype: job-feed-daily\ncomplete: true\ntotal_surfaced: 12\n---\n# x\n")
    fm = read_roll_up_frontmatter(f)
    assert fm.get("complete") is True
    assert fm.get("total_surfaced") == 12


def test_read_roll_up_frontmatter_missing_file_returns_none(tmp_path):
    assert read_roll_up_frontmatter(tmp_path / "nope.md") is None
