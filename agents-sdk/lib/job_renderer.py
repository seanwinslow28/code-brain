"""Markdown roll-up renderer + frontmatter reader for idempotency check."""

from __future__ import annotations

from pathlib import Path

import yaml

from lib.job_types import Posting, ScoringResult


def _slug_anchor(idx: int, company: str) -> str:
    return f"{idx}-{company.lower().replace(' ', '-').replace(',', '')}"


def _render_scored_entry(idx: int, db_id: int, posting: Posting, score: ScoringResult) -> str:
    stars = "⭐ " + f"{score.fit_score}/5"
    posted = posting.posted_at.date().isoformat() if posting.posted_at else "unknown"
    comp = posting.salary_disclosed or "not disclosed"
    concerns = "; ".join(score.concerns) if score.concerns else "none"
    return (
        f"### {idx}. {posting.company} — {posting.title} · {stars}\n"
        f"- **Source:** {posting.source} · **Location:** {posting.location or 'unspecified'} "
        f"· **Posted:** {posted} · **Comp:** {comp}\n"
        f"- **Band:** {score.role_band} · **Concerns:** {concerns}\n"
        f"- **Rationale:** {score.rationale}\n"
        f"- **Status:** new\n"
        f"- 🔗 [Apply]({posting.url}) · **db_id:** {db_id}\n"
    )


def _render_unscored_entry(idx: int, posting: Posting) -> str:
    return (
        f"### {idx}. {posting.company} — {posting.title} · ⏳ unscored\n"
        f"- **Source:** {posting.source} · **Location:** {posting.location or 'unspecified'}\n"
        f"- 🔗 [Apply]({posting.url})\n"
    )


def render_roll_up(
    today_iso: str,
    *,
    scored: list[tuple[int, Posting, ScoringResult]],
    unscored: list[Posting],
    complete: bool,
) -> str:
    top = [t for t in scored if t[2].fit_score >= 4]
    med = [t for t in scored if t[2].fit_score == 3]
    weak = [t for t in scored if t[2].fit_score <= 2]

    fm_data = {
        "type": "job-feed-daily",
        "project": "prj-job-hunt-2026",
        "date": today_iso,
        "total_surfaced": len(scored),
        "top_fits": len(top),
        "medium_fits": len(med),
        "weak_fits": len(weak),
        "unscored": len(unscored),
        "complete": complete,
        "ai-context": (
            "Daily job-feed roll-up. Hits sorted by fit_score desc. "
            "Status mutations via update_status.py."
        ),
    }
    fm = "---\n" + yaml.safe_dump(fm_data, sort_keys=False) + "---\n\n"

    head = (
        f"# Job Feed — {today_iso}\n\n"
        f"**{len(scored)} new fits** from 4 feeds + watchlist polls.\n"
        f"{len(top)} strong (≥4) · {len(med)} medium (3) · {len(weak)} weak (≤2) "
        f"· {len(unscored)} unscored.\n\n"
    )

    sections: list[str] = []

    if top:
        sections.append("## Top Fits (≥ 4/5)\n")
        for i, (db_id, p, s) in enumerate(top, start=1):
            sections.append(_render_scored_entry(i, db_id, p, s))

    if med:
        sections.append("\n## Medium Fits (3/5)\n")
        base = len(top)
        for i, (db_id, p, s) in enumerate(med, start=base + 1):
            sections.append(_render_scored_entry(i, db_id, p, s))

    if weak:
        sections.append("\n## Weak Fits (≤ 2/5) — included for visibility\n")
        base = len(top) + len(med)
        for i, (db_id, p, s) in enumerate(weak, start=base + 1):
            sections.append(_render_scored_entry(i, db_id, p, s))

    if unscored:
        sections.append("\n## Unscored — MBP was asleep\n")
        sections.append(
            "MBP could not be reached during today's fires. "
            "These postings are persisted and will be scored on the next run.\n\n"
        )
        base = len(scored)
        for i, p in enumerate(unscored, start=base + 1):
            sections.append(_render_unscored_entry(i, p))

    triage = (
        "\n## Triage\n\n"
        "```bash\n"
        "cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk\n"
        "PYTHONPATH=. .venv/bin/python3 scripts/update_status.py <db_id> applied\n"
        "PYTHONPATH=. .venv/bin/python3 scripts/update_status.py <db_id> passed\n"
        "```\n"
        "(Or in an interactive Claude session: `update status <db_id> to applied`)\n"
    )

    return fm + head + "".join(sections) + triage


def read_roll_up_frontmatter(path: Path) -> dict | None:
    """Return YAML frontmatter as a dict, or None if file missing / no frontmatter."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block = text[4:end]
    try:
        return yaml.safe_load(block) or {}
    except yaml.YAMLError:
        return None
