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
CONNECTIONS_REL = "vault/knowledge/connections"
EXPANSIONS_REL = "vault/knowledge/expansions"
EXPANSIONS_CONNECTIONS_REL = "vault/knowledge/expansions/connections"
HEALTH_REL = "vault/health"
SYNTH_WINDOW_START_HOUR = "02:00"
SYNTH_WINDOW_END_HOUR = "04:00"


def resolve_expansion_path(repo_root: Path, article_path: Path) -> Path:
    """Map a source article path to its expansion file path.

    Connections route to `vault/knowledge/expansions/connections/{slug}.md` so
    they don't collide with same-slugged concepts (e.g.
    `automation-failure-and-daily-note-disruption.md` exists in both folders).
    Concepts stay at `vault/knowledge/expansions/{slug}.md`, preserving the
    existing flat layout and the 4 hand-vetted expansion files already shipped.
    """
    try:
        rel_str = str(article_path.relative_to(repo_root))
    except ValueError:
        rel_str = ""
    if rel_str.startswith(f"{CONNECTIONS_REL}/"):
        return repo_root / EXPANSIONS_CONNECTIONS_REL / article_path.name
    return repo_root / EXPANSIONS_REL / article_path.name


def select_manual_targets(
    repo_root: Path,
    *,
    targets: list[Path],
    force: bool = False,
) -> tuple[list[Path], list[str]]:
    """Filter a manually-curated target list. Bypasses the manifest gate and
    PR-contamination filter that protect the nightly path; the caller is
    hand-picking from the existing concepts/connections corpus.

    Skip rules (logged as warnings, not errors):
      - path doesn't exist
      - path is outside `vault/knowledge/{concepts,connections}/`
      - expansion already exists and `force` is False (snapshot semantics)

    Returns (selected_paths_in_input_order, skip_warnings).
    """
    selected: list[Path] = []
    warnings: list[str] = []
    for raw in targets:
        full = raw if raw.is_absolute() else (repo_root / raw)
        if not full.exists():
            warnings.append(f"skip missing target: {raw}")
            continue
        try:
            rel_str = str(full.relative_to(repo_root))
        except ValueError:
            warnings.append(f"skip outside repo: {raw}")
            continue
        if not (
            rel_str.startswith(f"{CONCEPTS_REL}/")
            or rel_str.startswith(f"{CONNECTIONS_REL}/")
        ):
            warnings.append(f"skip not in concepts/connections: {rel_str}")
            continue
        if not force:
            existing = resolve_expansion_path(repo_root, full)
            if existing.exists():
                warnings.append(
                    f"skip already-critiqued: {existing.relative_to(repo_root)}"
                )
                continue
        selected.append(full)
    return selected, warnings


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
    """Select up to `max_targets` concept articles to critique tonight (fresh lane).

    Filters applied in order:
      1. Today's synth-manifest must exist (else 2026-05-15-style MBP-offline).
      2. Manifest status must NOT be `error`.
      3. Article path must be listed in the manifest's `concept_paths` (2026-05-27:
         replaces the prior 02:00–04:00 git-log window proxy, which silently
         dropped manual catch-up runs whose auto-commit timestamps fell outside
         that range).
      4. Falls back to `list_macmini_synth_files` only when the manifest predates
         the `concept_paths` field (resilience for older manifests during rollout).
      5. Article must not already have an expansion file (snapshot semantics).
      6. Cap at `max_targets`, preserving manifest order.

    Returns [] on any disqualifying condition.
    """
    date_iso = date_iso or date.today().isoformat()
    manifest = _read_manifest(repo_root, date_iso)
    if manifest is None:
        return []
    if manifest.get("status") == "error":
        return []

    manifest_paths = manifest.get("concept_paths")
    if isinstance(manifest_paths, list) and manifest_paths:
        candidates: list[Path] = []
        for rel in manifest_paths:
            if not isinstance(rel, str):
                continue
            if not rel.startswith(f"{CONCEPTS_REL}/"):
                continue
            full = repo_root / rel
            if full.exists():
                candidates.append(full)
    else:
        # Resilience path: older manifests written before 2026-05-27 lack the
        # `concept_paths` field. Fall back to the git-log proxy so the rollout
        # day's nightly run still finds targets.
        candidates = list_macmini_synth_files(repo_root, date_iso=date_iso)

    if not candidates:
        return []

    expansions_dir = repo_root / EXPANSIONS_REL
    selected: list[Path] = []
    for fp in candidates:
        if (expansions_dir / fp.name).exists():
            continue
        selected.append(fp)
        if len(selected) >= max_targets:
            break
    return selected


def select_backfill_targets(
    repo_root: Path,
    *,
    max_targets: int = 5,
    include_connections: bool = True,
    exclude: list[Path] | None = None,
) -> list[Path]:
    """Scan concepts/+connections/ for orphans missing an expansion file.

    Returns up to `max_targets` paths, oldest-first by source mtime, so the
    earliest unexpanded synth output gets critiqued first. Designed to drain
    the historical backlog of pre-critic synth files (~85 concepts + ~260
    connections as of 2026-05-27): when the synth was producing thin output
    daily before vault_critic existed, those files never got Round-3
    enrichment from Codex + Anti-Gravity.

    The `exclude` list lets the caller skip paths already chosen by the
    fresh lane so backfill doesn't re-pick them in the same run.

    Connections are included by default — the nightly fresh lane is
    concepts-only (a pre-2026-05-27 design choice), but backfill treats
    both folders as eligible since the corpus debt covers both.
    """
    exclude_set = {str(p.resolve()) for p in (exclude or [])}
    expansions_dir = repo_root / EXPANSIONS_REL
    expansions_connections_dir = repo_root / EXPANSIONS_CONNECTIONS_REL

    candidates: list[Path] = []
    concepts_dir = repo_root / CONCEPTS_REL
    if concepts_dir.exists():
        for fp in concepts_dir.glob("*.md"):
            if str(fp.resolve()) in exclude_set:
                continue
            if (expansions_dir / fp.name).exists():
                continue
            candidates.append(fp)

    if include_connections:
        connections_dir = repo_root / CONNECTIONS_REL
        if connections_dir.exists():
            for fp in connections_dir.glob("*.md"):
                if str(fp.resolve()) in exclude_set:
                    continue
                if (expansions_connections_dir / fp.name).exists():
                    continue
                candidates.append(fp)

    candidates.sort(key=lambda p: p.stat().st_mtime)
    return candidates[:max_targets]
