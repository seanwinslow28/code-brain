"""Select target articles for vault_critic, defending against PR contamination.

Per memory feedback_synth_verify_filter_to_manifest.md (2026-05-21):
naive `ls -lt` selection mixes Mac-Mini-written articles with files merged
in from stale-checkout machines via PR. The PR #52 contamination on
2026-05-21 nearly produced wasted vault_critic compute on 88 pre-Tier-2
files. The filter here cross-references the Mac Mini auto-commit's file
list using `git log --since/--until --name-only`, NOT mtime.

Skip semantics: missing manifest → empty list (2026-05-15 MBP-offline case).
Manifest status=error → empty list. Already-critiqued (expansion file exists)
→ skip. These keep the agent quiet on degraded nights rather than producing
wasted output.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

CONCEPTS_REL = "vault/knowledge/concepts"
EXPANSIONS_REL = "vault/knowledge/expansions"
HEALTH_REL = "vault/health"
SYNTH_WINDOW_START_HOUR = "02:00"
SYNTH_WINDOW_END_HOUR = "04:00"


def list_macmini_synth_files(
    repo_root: Path,
    *,
    date_iso: str | None = None,
) -> list[Path]:
    """Return the concept files Mac Mini's auto-commit wrote in today's
    synth window. Shells to `git log --name-only` scoped to the synth
    window (02:00–04:00 today). Filters to vault/knowledge/concepts/*.md.

    Returns [] on any git failure — caller treats that as a quiet night.

    Silent-skip behavior: files that appear in the git log but no longer
    exist on disk (e.g., committed then deleted before the critic ran) are
    silently dropped from the output. This is the intended behavior — a
    deleted file can't be critiqued — but it means the returned list may be
    shorter than the manifest's concepts_written. To diagnose a missing
    expansion file, run the git log command above by hand and check whether
    each listed file exists at the printed path.
    """
    date_iso = date_iso or date.today().isoformat()
    since = f"{date_iso} {SYNTH_WINDOW_START_HOUR}"
    until = f"{date_iso} {SYNTH_WINDOW_END_HOUR}"

    cmd = [
        "git", "log",
        "--since", since,
        "--until", until,
        "--name-only",
        "--pretty=format:",
        "--",
        f"{CONCEPTS_REL}/*.md",
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (subprocess.SubprocessError, OSError):
        return []

    if result.returncode != 0:
        return []

    out: list[Path] = []
    seen: set[str] = set()
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith(f"{CONCEPTS_REL}/"):
            continue
        if line in seen:
            continue
        seen.add(line)
        full = repo_root / line
        if full.exists():
            out.append(full)
    return out


def _read_manifest(repo_root: Path, date_iso: str) -> dict | None:
    p = repo_root / HEALTH_REL / f"synth-manifest-{date_iso}.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def select_target_articles(
    repo_root: Path,
    *,
    date_iso: str | None = None,
    max_targets: int = 3,
) -> list[Path]:
    """Select up to `max_targets` concept articles to critique tonight.

    Filters applied in order:
      1. Today's synth-manifest must exist (else 2026-05-15-style MBP-offline).
      2. Manifest status must NOT be `error`.
      3. Article must be in Mac Mini's auto-commit file list (PR-contamination filter).
      4. Article must not already have an expansion file (snapshot semantics).
      5. Cap at `max_targets`, preserving auto-commit file order.

    Returns [] on any disqualifying condition.
    """
    date_iso = date_iso or date.today().isoformat()
    manifest = _read_manifest(repo_root, date_iso)
    if manifest is None:
        return []
    if manifest.get("status") == "error":
        return []

    mm_files = list_macmini_synth_files(repo_root, date_iso=date_iso)
    if not mm_files:
        return []

    expansions_dir = repo_root / EXPANSIONS_REL
    selected: list[Path] = []
    for fp in mm_files:
        if (expansions_dir / fp.name).exists():
            continue
        selected.append(fp)
        if len(selected) >= max_targets:
            break
    return selected
