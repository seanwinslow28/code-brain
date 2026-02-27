"""Shared fixtures for agent tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture
def tmp_vault(tmp_path: Path) -> Path:
    """Create a minimal vault structure for testing."""
    # Daily notes directory
    daily_dir = tmp_path / "10_timeline" / "daily"
    daily_dir.mkdir(parents=True)

    # Weekly notes directory
    weekly_dir = tmp_path / "10_timeline" / "weekly"
    weekly_dir.mkdir(parents=True)

    # Templates directory
    templates_dir = tmp_path / "90_system" / "templates"
    templates_dir.mkdir(parents=True)

    # Agent logs directory
    logs_dir = tmp_path / "90_system" / "agent-logs"
    logs_dir.mkdir(parents=True)

    # Inbox directory
    inbox_dir = tmp_path / "00_inbox"
    inbox_dir.mkdir(parents=True)

    # Write a daily note template
    (templates_dir / "tpl-daily.md").write_text(
        "---\n"
        "type: daily\n"
        "date: <% tp.file.title %>\n"
        "---\n"
        "# <% tp.file.title %>\n"
        "\n"
        "## Work Log\n"
        "<!-- jira-log -->\n"
        "\n"
        "## Claude Code Sessions\n"
        "<!-- claude-sessions -->\n"
        "\n"
        "## Side Project Notes\n"
        "<!-- side-projects -->\n",
        encoding="utf-8",
    )

    return tmp_path


@pytest.fixture
def tmp_skills(tmp_path: Path) -> Path:
    """Create a minimal skills directory for testing."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir(parents=True)

    # Create a test skill
    test_skill_dir = skills_dir / "test-skill"
    test_skill_dir.mkdir()
    (test_skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: test-skill\n"
        "description: A test skill for unit tests.\n"
        "---\n"
        "\n"
        "# Test Skill\n"
        "\n"
        "## Purpose\n"
        "\n"
        "This is a test skill body.\n"
        "\n"
        "## Instructions\n"
        "\n"
        "Follow these test instructions.\n",
        encoding="utf-8",
    )

    # Create a second skill
    another_dir = skills_dir / "another-skill"
    another_dir.mkdir()
    (another_dir / "SKILL.md").write_text(
        "---\n"
        "name: another-skill\n"
        "description: Another test skill.\n"
        "---\n"
        "\n"
        "# Another Skill\n"
        "\n"
        "Do another thing.\n",
        encoding="utf-8",
    )

    return skills_dir


@pytest.fixture
def tmp_config(tmp_path: Path, tmp_vault: Path, tmp_skills: Path) -> Path:
    """Create a config.toml for testing."""
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        f'[paths]\n'
        f'repo_root = "{tmp_path}"\n'
        f'vault_root = "{tmp_vault}"\n'
        f'skills_dir = "{tmp_skills}"\n'
        f'life_systems_scripts = "{tmp_path / "scripts"}"\n'
        f'\n'
        f'[agents.daily_driver]\n'
        f'enabled = true\n'
        f'skills = ["test-skill", "another-skill"]\n'
        f'\n'
        f'[agents.spending_analysis]\n'
        f'enabled = false\n'
        f'\n'
        f'[safety]\n'
        f'max_turns_default = 10\n'
        f'max_budget_default = 0.25\n'
        f'permission_mode = "acceptEdits"\n'
        f'\n'
        f'[logging]\n'
        f'log_dir = "{tmp_vault / "90_system" / "agent-logs"}"\n'
        f'log_level = "DEBUG"\n',
        encoding="utf-8",
    )

    # Set API key for testing
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-key-for-unit-tests"

    return config_file
