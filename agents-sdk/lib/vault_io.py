"""Vault I/O helpers for reading and writing Obsidian vault files."""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

# Match YAML frontmatter block
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def daily_note_path(vault_root: Path, target_date: date | None = None) -> Path:
    """Return the path for a daily note.

    Args:
        vault_root: Root of the Obsidian vault.
        target_date: Date for the note. Defaults to today.

    Returns:
        Path like vault/10_timeline/daily/2026-02-21.md
    """
    d = target_date or date.today()
    return vault_root / "10_timeline" / "daily" / f"{d.isoformat()}.md"


def weekly_note_path(vault_root: Path, target_date: date | None = None) -> Path:
    """Return the path for a weekly review note.

    Args:
        vault_root: Root of the Obsidian vault.
        target_date: Any date in the target week. Defaults to today.

    Returns:
        Path like vault/10_timeline/weekly/2026-W08.md
    """
    d = target_date or date.today()
    week_num = d.isocalendar()[1]
    year = d.isocalendar()[0]
    return vault_root / "10_timeline" / "weekly" / f"{year}-W{week_num:02d}.md"


def yesterday_note_path(vault_root: Path) -> Path:
    """Return the path for yesterday's daily note."""
    return daily_note_path(vault_root, date.today() - timedelta(days=1))


def inject_at_anchor(file_path: Path, anchor: str, content: str) -> bool:
    """Inject content below an HTML comment anchor in a file.

    Finds the line containing `<!-- anchor -->` and inserts content
    on the next line. This is a PATCH operation (append, not replace).

    Args:
        file_path: Path to the markdown file.
        anchor: The anchor name (without <!-- --> wrapping).
        content: The content to inject below the anchor.

    Returns:
        True if the anchor was found and content injected, False otherwise.
    """
    if not file_path.exists():
        return False

    text = file_path.read_text(encoding="utf-8")
    marker = f"<!-- {anchor} -->"

    if marker not in text:
        return False

    # Insert content on the line after the anchor
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if marker in line:
            new_lines.append(content)

    file_path.write_text("\n".join(new_lines), encoding="utf-8")
    return True


def read_frontmatter(file_path: Path) -> dict[str, str]:
    """Extract YAML frontmatter from a markdown file as a dict.

    Simple key: value parsing (no nested YAML support).

    Args:
        file_path: Path to the markdown file.

    Returns:
        Dict of frontmatter key-value pairs. Empty dict if no frontmatter.
    """
    if not file_path.exists():
        return {}

    text = file_path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}

    result = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def create_from_template(
    template_path: Path,
    destination: Path,
    substitutions: dict[str, str] | None = None,
) -> Path:
    """Create a new note from a vault template.

    Reads the template, applies substitutions (replacing Templater-style
    `<% tp.file.title %>` placeholders with the provided values), and
    writes to the destination.

    Args:
        template_path: Path to the template file.
        destination: Path where the new note should be created.
        substitutions: Dict of placeholder -> replacement. The key
            `title` replaces `<% tp.file.title %>`.

    Returns:
        The destination path.

    Raises:
        FileNotFoundError: If the template doesn't exist.
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    content = template_path.read_text(encoding="utf-8")

    subs = substitutions or {}
    if "title" in subs:
        content = content.replace("<% tp.file.title %>", subs["title"])

    for key, value in subs.items():
        content = content.replace(f"{{{{ {key} }}}}", value)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return destination


def recent_daily_notes(vault_root: Path, days: int = 7) -> list[Path]:
    """Return paths to the last N daily notes that exist.

    Args:
        vault_root: Root of the Obsidian vault.
        days: Number of days to look back.

    Returns:
        List of existing daily note paths, most recent first.
    """
    today = date.today()
    paths = []
    for i in range(days):
        d = today - timedelta(days=i)
        p = daily_note_path(vault_root, d)
        if p.exists():
            paths.append(p)
    return paths
