"""Load SKILL.md files as system prompt content for Agent SDK agents."""

from __future__ import annotations

import re
from pathlib import Path

# Strip YAML frontmatter: --- ... ---
_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def load_skill_prompt(skill_name: str, skills_dir: Path) -> str:
    """Read a skill's SKILL.md and return the body as a prompt string.

    The YAML frontmatter (between --- delimiters) is stripped, leaving
    only the markdown body that contains the skill's instructions.

    Args:
        skill_name: Name of the skill directory (e.g., "daily-driver").
        skills_dir: Path to the .claude/skills/ directory.

    Returns:
        The markdown body of the SKILL.md file.

    Raises:
        FileNotFoundError: If the skill directory or SKILL.md doesn't exist.
    """
    skill_file = skills_dir / skill_name / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"Skill not found: {skill_file}")

    content = skill_file.read_text(encoding="utf-8")
    body = _FRONTMATTER_RE.sub("", content, count=1).strip()
    return body


def load_skills(skill_names: list[str], skills_dir: Path) -> str:
    """Load multiple skills and concatenate them with separators.

    Args:
        skill_names: List of skill names to load.
        skills_dir: Path to the .claude/skills/ directory.

    Returns:
        Concatenated skill prompts separated by horizontal rules.
    """
    parts = []
    for name in skill_names:
        prompt = load_skill_prompt(name, skills_dir)
        parts.append(f"## Skill: {name}\n\n{prompt}")
    return "\n\n---\n\n".join(parts)
