"""Tests for skill_loader module."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.skill_loader import load_skill_prompt, load_skills


class TestLoadSkillPrompt:
    def test_loads_skill_and_strips_frontmatter(self, tmp_skills: Path):
        result = load_skill_prompt("test-skill", tmp_skills)
        assert "# Test Skill" in result
        assert "This is a test skill body." in result
        assert "Follow these test instructions." in result
        # Frontmatter should be stripped
        assert "---" not in result
        assert "name: test-skill" not in result

    def test_missing_skill_raises(self, tmp_skills: Path):
        with pytest.raises(FileNotFoundError, match="nonexistent"):
            load_skill_prompt("nonexistent", tmp_skills)

    def test_skill_without_frontmatter(self, tmp_skills: Path):
        # Create a skill with no frontmatter
        no_fm_dir = tmp_skills / "no-frontmatter"
        no_fm_dir.mkdir()
        (no_fm_dir / "SKILL.md").write_text(
            "# Plain Skill\n\nNo frontmatter here.\n",
            encoding="utf-8",
        )
        result = load_skill_prompt("no-frontmatter", tmp_skills)
        assert "# Plain Skill" in result
        assert "No frontmatter here." in result


class TestLoadSkills:
    def test_loads_multiple_skills(self, tmp_skills: Path):
        result = load_skills(["test-skill", "another-skill"], tmp_skills)
        assert "## Skill: test-skill" in result
        assert "## Skill: another-skill" in result
        assert "---" in result  # Separator between skills
        assert "This is a test skill body." in result
        assert "Do another thing." in result

    def test_single_skill_no_separator(self, tmp_skills: Path):
        result = load_skills(["test-skill"], tmp_skills)
        assert "## Skill: test-skill" in result
        # Only one skill, so the --- separator appears only in skill content
        assert result.count("\n---\n") == 0

    def test_empty_list(self, tmp_skills: Path):
        result = load_skills([], tmp_skills)
        assert result == ""
