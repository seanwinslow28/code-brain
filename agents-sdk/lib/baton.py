"""Baton File utility for inter-agent dependency chains.

Baton Files are simple flag files that signal completion between agents.
Process Inbox creates ~/.claude/batons/inbox_done.flag on success;
Daily Driver's launchd plist uses WatchPaths to trigger on that flag.

Usage:
    from lib.baton import create_baton, check_baton, cleanup_baton

    # Agent A completes successfully:
    create_baton("inbox_done")

    # Agent B checks dependency:
    if check_baton("inbox_done"):
        run_agent_b()
        cleanup_baton("inbox_done")
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

BATON_DIR = Path.home() / ".claude" / "batons"


def _baton_path(name: str) -> Path:
    """Return the path for a named baton file."""
    if not name.endswith(".flag"):
        name = f"{name}.flag"
    return BATON_DIR / name


def create_baton(name: str, metadata: str = "") -> Path:
    """Create a baton flag file signaling agent completion.

    Args:
        name: Baton name (e.g., "inbox_done"). .flag extension added if missing.
        metadata: Optional text to write into the flag file (e.g., timestamp, summary).

    Returns:
        Path to the created baton file.
    """
    BATON_DIR.mkdir(parents=True, exist_ok=True)
    path = _baton_path(name)

    content = f"agent_completed_at: {datetime.now().isoformat()}\n"
    if metadata:
        content += f"metadata: {metadata}\n"

    path.write_text(content, encoding="utf-8")
    logger.info("Baton created: %s", path)
    return path


def check_baton(name: str) -> bool:
    """Check if a baton file exists (dependency was satisfied).

    Args:
        name: Baton name to check.

    Returns:
        True if the baton file exists.
    """
    return _baton_path(name).exists()


def cleanup_baton(name: str) -> bool:
    """Remove a baton file after the dependent agent has consumed it.

    Args:
        name: Baton name to clean up.

    Returns:
        True if the file was deleted, False if it didn't exist.
    """
    path = _baton_path(name)
    if path.exists():
        path.unlink()
        logger.info("Baton cleaned up: %s", path)
        return True
    return False


def cleanup_all_batons() -> int:
    """Remove all baton files. Used for testing or manual reset.

    Returns:
        Number of baton files removed.
    """
    if not BATON_DIR.exists():
        return 0

    count = 0
    for flag in BATON_DIR.glob("*.flag"):
        flag.unlink()
        count += 1
    logger.info("Cleaned up %d baton files", count)
    return count


def list_batons() -> list[dict[str, str]]:
    """List all active baton files with their metadata.

    Returns:
        List of dicts with 'name', 'created_at', and 'metadata' keys.
    """
    if not BATON_DIR.exists():
        return []

    results = []
    for flag in sorted(BATON_DIR.glob("*.flag")):
        content = flag.read_text(encoding="utf-8")
        entry: dict[str, str] = {"name": flag.stem}
        for line in content.strip().splitlines():
            if ": " in line:
                key, _, value = line.partition(": ")
                entry[key.strip()] = value.strip()
        results.append(entry)
    return results
