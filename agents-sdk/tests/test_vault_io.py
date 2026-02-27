"""Tests for vault_io module."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from lib.vault_io import (
    create_from_template,
    daily_note_path,
    inject_at_anchor,
    read_frontmatter,
    recent_daily_notes,
    weekly_note_path,
    yesterday_note_path,
)


class TestDailyNotePath:
    def test_today(self, tmp_vault: Path):
        path = daily_note_path(tmp_vault)
        today = date.today().isoformat()
        assert path == tmp_vault / "10_timeline" / "daily" / f"{today}.md"

    def test_specific_date(self, tmp_vault: Path):
        d = date(2026, 2, 21)
        path = daily_note_path(tmp_vault, d)
        assert path == tmp_vault / "10_timeline" / "daily" / "2026-02-21.md"


class TestWeeklyNotePath:
    def test_week_number(self, tmp_vault: Path):
        d = date(2026, 2, 21)  # Week 8 of 2026
        path = weekly_note_path(tmp_vault, d)
        assert "W08" in path.name or "W8" in path.name


class TestYesterdayNotePath:
    def test_yesterday(self, tmp_vault: Path):
        path = yesterday_note_path(tmp_vault)
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        assert path.name == f"{yesterday}.md"


class TestInjectAtAnchor:
    def test_injects_below_anchor(self, tmp_vault: Path):
        note = tmp_vault / "10_timeline" / "daily" / "test.md"
        note.write_text(
            "# Test\n\n## Work Log\n<!-- jira-log -->\n\n## Sessions\n<!-- claude-sessions -->\n",
            encoding="utf-8",
        )

        result = inject_at_anchor(note, "jira-log", "- Did some work today")
        assert result is True

        content = note.read_text(encoding="utf-8")
        lines = content.split("\n")
        jira_idx = next(i for i, l in enumerate(lines) if "<!-- jira-log -->" in l)
        assert lines[jira_idx + 1] == "- Did some work today"

    def test_missing_anchor_returns_false(self, tmp_vault: Path):
        note = tmp_vault / "10_timeline" / "daily" / "test.md"
        note.write_text("# No anchors here\n", encoding="utf-8")

        result = inject_at_anchor(note, "nonexistent", "content")
        assert result is False

    def test_missing_file_returns_false(self, tmp_vault: Path):
        result = inject_at_anchor(
            tmp_vault / "nonexistent.md", "anchor", "content"
        )
        assert result is False

    def test_preserves_other_content(self, tmp_vault: Path):
        note = tmp_vault / "10_timeline" / "daily" / "test.md"
        note.write_text(
            "# Title\n\n## Section\n<!-- anchor -->\nExisting content\n\n## Other\nKeep this\n",
            encoding="utf-8",
        )

        inject_at_anchor(note, "anchor", "New injected line")

        content = note.read_text(encoding="utf-8")
        assert "# Title" in content
        assert "New injected line" in content
        assert "Existing content" in content
        assert "Keep this" in content


class TestReadFrontmatter:
    def test_reads_frontmatter(self, tmp_vault: Path):
        note = tmp_vault / "test-fm.md"
        note.write_text(
            "---\ntype: daily\ndate: 2026-02-21\nmood: good\n---\n# Title\n",
            encoding="utf-8",
        )

        fm = read_frontmatter(note)
        assert fm["type"] == "daily"
        assert fm["date"] == "2026-02-21"
        assert fm["mood"] == "good"

    def test_no_frontmatter(self, tmp_vault: Path):
        note = tmp_vault / "no-fm.md"
        note.write_text("# Just a title\n\nSome content.\n", encoding="utf-8")

        fm = read_frontmatter(note)
        assert fm == {}

    def test_missing_file(self, tmp_vault: Path):
        fm = read_frontmatter(tmp_vault / "nonexistent.md")
        assert fm == {}


class TestCreateFromTemplate:
    def test_creates_note_from_template(self, tmp_vault: Path):
        template = tmp_vault / "90_system" / "templates" / "tpl-daily.md"
        dest = tmp_vault / "10_timeline" / "daily" / "2026-02-21.md"

        result = create_from_template(template, dest, {"title": "2026-02-21"})

        assert result == dest
        assert dest.exists()
        content = dest.read_text(encoding="utf-8")
        assert "# 2026-02-21" in content
        assert "date: 2026-02-21" in content
        assert "<!-- jira-log -->" in content

    def test_creates_parent_dirs(self, tmp_vault: Path):
        template = tmp_vault / "90_system" / "templates" / "tpl-daily.md"
        dest = tmp_vault / "new" / "nested" / "dir" / "note.md"

        create_from_template(template, dest, {"title": "test"})
        assert dest.exists()

    def test_missing_template_raises(self, tmp_vault: Path):
        import pytest

        with pytest.raises(FileNotFoundError, match="Template not found"):
            create_from_template(
                tmp_vault / "nonexistent-template.md",
                tmp_vault / "output.md",
            )


class TestRecentDailyNotes:
    def test_finds_existing_notes(self, tmp_vault: Path):
        today = date.today()
        daily_dir = tmp_vault / "10_timeline" / "daily"

        # Create notes for today and 2 days ago (skip yesterday)
        (daily_dir / f"{today.isoformat()}.md").write_text("today", encoding="utf-8")
        two_ago = today - timedelta(days=2)
        (daily_dir / f"{two_ago.isoformat()}.md").write_text("two days ago", encoding="utf-8")

        notes = recent_daily_notes(tmp_vault, days=7)
        assert len(notes) == 2
        assert notes[0].name == f"{today.isoformat()}.md"  # Most recent first

    def test_no_notes_returns_empty(self, tmp_vault: Path):
        notes = recent_daily_notes(tmp_vault, days=7)
        assert notes == []
