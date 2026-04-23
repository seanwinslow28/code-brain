"""Load operating-model artifacts for agent context injection.

Artifacts live at `vault/05_atlas/operating-models/{domain}/{kind}.md` and
are produced by the work-operating-model skill. This module is the
downstream consumer: it reads artifact bodies on demand, caches by file
mtime, and degrades gracefully when files are missing or not yet confirmed.

Pattern mirrors lib/skill_loader.py — plain module functions, regex
frontmatter stripping, explicit None for missing content (never raises).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger("artifact_loader")

DOMAINS: tuple[str, ...] = ("the-block", "creative-studio", "life-systems")
KINDS: tuple[str, ...] = (
    "HEARTBEAT",
    "USER",
    "SOUL",
    "operating-model",
    "schedule-recommendations",
)

_DEFAULT_SUBPATH = "05_atlas/operating-models"
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)

# Cache keyed on (domain, kind, file_mtime_ns) → body text.
# mtime-keyed: any edit to an artifact invalidates the old entry on next access.
_cache: dict[tuple[str, str, int], str] = {}


def artifact_path(domain: str, kind: str, vault_root: Path, subpath: str = _DEFAULT_SUBPATH) -> Path:
    """Return the filesystem path for a given (domain, kind) artifact."""
    return vault_root / subpath / domain / f"{kind}.md"


def _parse_status(frontmatter_text: str) -> str | None:
    m = _STATUS_RE.search(frontmatter_text)
    return m.group(1).strip() if m else None


def load_artifact(
    domain: str,
    kind: str,
    vault_root: Path,
    *,
    subpath: str = _DEFAULT_SUBPATH,
    strip_frontmatter: bool = True,
    require_confirmed: bool = True,
) -> str | None:
    """Load one operating-model artifact body.

    Args:
        domain: "the-block" | "creative-studio" | "life-systems".
        kind: "HEARTBEAT" | "USER" | "SOUL" | "operating-model" | "schedule-recommendations".
        vault_root: Absolute path to the vault root.
        subpath: Relative path under vault_root where artifacts live.
        strip_frontmatter: If True (default), YAML frontmatter is removed.
        require_confirmed: If True (default), artifacts whose frontmatter
            is missing `status: confirmed` return None.

    Returns:
        The artifact body as a string, or None if the file is missing,
        unconfirmed (when required), or cannot be read. Never raises.
    """
    path = artifact_path(domain, kind, vault_root, subpath)

    if not path.exists():
        logger.warning("artifact_missing domain=%s kind=%s path=%s", domain, kind, path)
        return None

    try:
        mtime_ns = path.stat().st_mtime_ns
    except OSError as exc:
        logger.warning("artifact_stat_error domain=%s kind=%s err=%s", domain, kind, exc)
        return None

    cache_key = (domain, kind, mtime_ns)
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("artifact_read_error domain=%s kind=%s err=%s", domain, kind, exc)
        return None

    frontmatter_match = _FRONTMATTER_RE.match(text)
    frontmatter_text = frontmatter_match.group(1) if frontmatter_match else ""

    if require_confirmed:
        status = _parse_status(frontmatter_text)
        if status != "confirmed":
            logger.info(
                "artifact_not_confirmed domain=%s kind=%s status=%s",
                domain, kind, status or "missing",
            )
            return None

    if strip_frontmatter and frontmatter_match:
        body = text[frontmatter_match.end():].lstrip()
    else:
        body = text

    _cache[cache_key] = body
    return body


def load_heartbeats(
    vault_root: Path,
    *,
    subpath: str = _DEFAULT_SUBPATH,
    require_confirmed: bool = True,
) -> dict[str, str | None]:
    """Return HEARTBEAT bodies for all three domains.

    Missing or unconfirmed domains map to None. Never raises.
    """
    return {
        domain: load_artifact(
            domain,
            "HEARTBEAT",
            vault_root,
            subpath=subpath,
            require_confirmed=require_confirmed,
        )
        for domain in DOMAINS
    }


def clear_cache() -> None:
    """Reset the module-level cache. Primarily for tests."""
    _cache.clear()
