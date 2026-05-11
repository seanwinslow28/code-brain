from pathlib import Path
from unittest.mock import MagicMock

from agents.daily_driver import _append_job_feed_summary


def _make_roll_up(path: Path, complete: bool, top_n: int = 3) -> None:
    fm_complete = "true" if complete else "false"
    entries = ""
    for i in range(1, top_n + 1):
        entries += (
            f"### {i}. Company{i} — PM, Foo · ⭐ 5/5\n"
            f"- **Source:** ashby:co{i} · **Location:** Remote (US)\n"
            f"- 🔗 [Apply](https://x.example/{i}) · **db_id:** {i}\n\n"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\ntype: job-feed-daily\ndate: 2026-05-09\n"
        f"total_surfaced: {top_n}\ntop_fits: {top_n}\nmedium_fits: 0\nweak_fits: 0\n"
        f"unscored: 0\ncomplete: {fm_complete}\n---\n\n"
        f"# Job Feed — 2026-05-09\n\n## Top Fits (≥ 4/5)\n\n{entries}"
    )


def test_summary_renders_when_roll_up_exists_and_complete(tmp_path):
    cfg = MagicMock()
    cfg.vault_root = tmp_path
    feed_path = tmp_path / "20_projects/prj-job-hunt-2026/job-feed/2026-05-09.md"
    _make_roll_up(feed_path, complete=True, top_n=3)

    out = _append_job_feed_summary(cfg, today="2026-05-09")
    assert "Job Feed (2026-05-09)" in out
    assert "Company1" in out and "Company2" in out and "Company3" in out
    assert "scoring deferred" not in out.lower()


def test_summary_renders_deferred_when_complete_false(tmp_path):
    cfg = MagicMock()
    cfg.vault_root = tmp_path
    feed_path = tmp_path / "20_projects/prj-job-hunt-2026/job-feed/2026-05-09.md"
    _make_roll_up(feed_path, complete=False, top_n=0)

    out = _append_job_feed_summary(cfg, today="2026-05-09")
    assert "scoring deferred" in out.lower()


def test_summary_silent_when_roll_up_missing(tmp_path):
    cfg = MagicMock()
    cfg.vault_root = tmp_path
    out = _append_job_feed_summary(cfg, today="2026-05-09")
    assert out == ""
