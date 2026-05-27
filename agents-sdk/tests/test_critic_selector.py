import json
from datetime import date
from pathlib import Path

import pytest

from lib.critic_selector import (
    list_macmini_synth_files,
    resolve_expansion_path,
    select_backfill_targets,
    select_manual_targets,
    select_target_articles,
)


@pytest.fixture
def tmp_vault(tmp_path):
    """Minimal vault layout mirroring the production paths."""
    (tmp_path / "vault" / "knowledge" / "concepts").mkdir(parents=True)
    (tmp_path / "vault" / "knowledge" / "expansions").mkdir(parents=True)
    (tmp_path / "vault" / "health").mkdir(parents=True)
    return tmp_path


def _write_concept(vault_root: Path, slug: str, title: str) -> Path:
    p = vault_root / "vault" / "knowledge" / "concepts" / f"{slug}.md"
    p.write_text(
        f'---\ntitle: "{title}"\ntype: concept\n---\n\n## Definition\n\nbody\n',
        encoding="utf-8",
    )
    return p


def _write_manifest(vault_root: Path, today_iso: str, **kwargs):
    payload = {
        "run_id": f"{today_iso}T02:31:00",
        "status": "ok",
        "concepts_written": 1,
        "connections_written": 0,
        **kwargs,
    }
    (vault_root / "vault" / "health" / f"synth-manifest-{today_iso}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_list_macmini_synth_files_returns_concept_paths_from_commit(monkeypatch, tmp_vault):
    """The function shells to git log to enumerate files written by Mac Mini's
    auto-commit in the synth window (02:00-04:00 today), then filters to
    vault/knowledge/concepts/*.md paths. Mock the git call to keep the test
    hermetic."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "real-mm-concept", "Real Mac Mini Concept")
    _write_concept(tmp_vault, "pr-contamination", "PR Contamination Concept")

    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        # Simulate a Mac Mini auto-commit listing exactly one concept file.
        class Result:
            returncode = 0
            stdout = "vault/knowledge/concepts/real-mm-concept.md\n"
            stderr = ""
        return Result()

    monkeypatch.setattr("lib.critic_selector.subprocess.run", fake_run)

    files = list_macmini_synth_files(tmp_vault, date_iso=today)
    assert len(files) == 1
    assert files[0].name == "real-mm-concept.md"
    # The git command must scope to the synth window today.
    assert "--since" in captured["cmd"]
    assert today in " ".join(captured["cmd"])


def test_select_target_articles_filters_to_manifest_count(monkeypatch, tmp_vault):
    """If the manifest reports concepts_written=1 but ls shows 5 fresh concept
    files, only the 1 file from the Mac Mini auto-commit is selected."""
    today = "2026-05-21"
    for slug in ("good", "bad1", "bad2", "bad3", "bad4"):
        _write_concept(tmp_vault, slug, slug.title())
    _write_manifest(tmp_vault, today, concepts_written=1)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            root / "vault" / "knowledge" / "concepts" / "good.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert len(targets) == 1
    assert targets[0].name == "good.md"


def test_select_target_articles_caps_at_max_targets(monkeypatch, tmp_vault):
    today = "2026-05-21"
    for slug in ("a", "b", "c", "d", "e"):
        _write_concept(tmp_vault, slug, slug.upper())
    _write_manifest(tmp_vault, today, concepts_written=5)

    all_paths = [
        tmp_vault / "vault" / "knowledge" / "concepts" / f"{s}.md"
        for s in ("a", "b", "c", "d", "e")
    ]
    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: all_paths,
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert len(targets) == 3


def test_select_target_articles_returns_empty_when_no_manifest(tmp_vault):
    """No synth ran or wasn't completed — exit cleanly with empty list.
    This is the 2026-05-15 MBP-offline canonical case."""
    targets = select_target_articles(tmp_vault, date_iso="2026-05-21", max_targets=3)
    assert targets == []


def test_select_target_articles_skips_already_critiqued(monkeypatch, tmp_vault):
    """If vault/knowledge/expansions/foo.md already exists, skip foo —
    snapshot semantics, no regeneration in v1."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "already", "Already")
    _write_concept(tmp_vault, "fresh", "Fresh")
    (tmp_vault / "vault" / "knowledge" / "expansions" / "already.md").write_text(
        "previous critique", encoding="utf-8",
    )
    _write_manifest(tmp_vault, today, concepts_written=2)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            tmp_vault / "vault" / "knowledge" / "concepts" / "already.md",
            tmp_vault / "vault" / "knowledge" / "concepts" / "fresh.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["fresh.md"]


def test_select_target_articles_skips_when_manifest_status_is_error(monkeypatch, tmp_vault):
    """If the synthesizer's manifest says status=error, don't critique its
    output — those articles are an error path, not real synth output."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "fresh", "Fresh")
    _write_manifest(tmp_vault, today, status="error", concepts_written=0)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            tmp_vault / "vault" / "knowledge" / "concepts" / "fresh.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert targets == []


# ---------------------------------------------------------------------------
# Manual-mode helpers (Sean's on-demand critique of existing corpus, 2026-05-24)
# ---------------------------------------------------------------------------


def _write_connection(vault_root: Path, slug: str) -> Path:
    p = vault_root / "vault" / "knowledge" / "connections" / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'---\ntitle: "{slug}"\ntype: connection\n---\n\nbody\n',
        encoding="utf-8",
    )
    return p


def test_resolve_expansion_path_routes_concepts_flat_and_connections_to_subfolder(
    tmp_vault,
):
    """One concrete slug collision exists in prod
    (automation-failure-and-daily-note-disruption.md exists in both concepts/
    and connections/). The expansion path must namespace them apart so the
    second-critiqued doesn't clobber the first."""
    concept_path = _write_concept(tmp_vault, "shared-slug", "Shared")
    connection_path = _write_connection(tmp_vault, "shared-slug")

    concept_exp = resolve_expansion_path(tmp_vault, concept_path)
    connection_exp = resolve_expansion_path(tmp_vault, connection_path)

    assert concept_exp == tmp_vault / "vault" / "knowledge" / "expansions" / "shared-slug.md"
    assert connection_exp == (
        tmp_vault / "vault" / "knowledge" / "expansions" / "connections" / "shared-slug.md"
    )
    assert concept_exp != connection_exp


def test_select_manual_targets_filters_missing_outside_and_existing(tmp_vault):
    """Manual mode must drop: paths that don't exist, paths outside the
    concepts/connections corpus, and paths whose expansion already exists
    (the 4 hand-vetted expansions stay untouched without --force).
    All skips surface as warnings, never errors."""
    keeper = _write_concept(tmp_vault, "fresh-concept", "Fresh")
    already_done = _write_concept(tmp_vault, "already-critiqued", "Done")
    # Mark the second concept as already-expanded.
    (tmp_vault / "vault" / "knowledge" / "expansions" / "already-critiqued.md").write_text(
        "existing expansion", encoding="utf-8"
    )
    # An unrelated vault file (not a concept/connection).
    (tmp_vault / "vault" / "knowledge").mkdir(parents=True, exist_ok=True)
    stray = tmp_vault / "vault" / "knowledge" / "index.md"
    stray.write_text("index", encoding="utf-8")

    inputs = [
        Path("vault/knowledge/concepts/fresh-concept.md"),
        Path("vault/knowledge/concepts/already-critiqued.md"),
        Path("vault/knowledge/concepts/missing-file.md"),
        Path("vault/knowledge/index.md"),
    ]
    selected, warnings = select_manual_targets(tmp_vault, targets=inputs, force=False)

    assert selected == [keeper]
    assert len(warnings) == 3
    assert any("already-critiqued" in w for w in warnings)
    assert any("missing" in w for w in warnings)
    assert any("index.md" in w for w in warnings)
    # Sanity: the already-done expansion was not mutated by selection.
    _ = already_done  # explicit reference to keep linter quiet


def test_select_manual_targets_force_includes_already_critiqued(tmp_vault):
    """--force re-critiques even when an expansion file exists, for when Sean
    wants a fresh pass against an updated source concept."""
    p = _write_concept(tmp_vault, "redo-me", "Redo")
    (tmp_vault / "vault" / "knowledge" / "expansions" / "redo-me.md").write_text(
        "stale expansion", encoding="utf-8"
    )
    selected, warnings = select_manual_targets(
        tmp_vault, targets=[Path("vault/knowledge/concepts/redo-me.md")], force=True,
    )
    assert selected == [p]
    assert warnings == []


def test_select_manual_targets_accepts_connections(tmp_vault):
    """Connections folder is a valid manual-mode source (the nightly selector
    is concepts-only; manual mode opens up the connections corpus too)."""
    p = _write_connection(tmp_vault, "neat-connection")
    selected, warnings = select_manual_targets(
        tmp_vault,
        targets=[Path("vault/knowledge/connections/neat-connection.md")],
        force=False,
    )
    assert selected == [p]
    assert warnings == []


# ---------------------------------------------------------------------------
# Manifest-driven fresh lane (2026-05-27) — replaces git-log/02:00–04:00 proxy
# ---------------------------------------------------------------------------


def test_select_target_articles_reads_manifest_concept_paths(tmp_vault):
    """The 2026-05-27 fix: the selector reads `concept_paths` from the
    synth-manifest verbatim. No git-log proxy, no 02:00–04:00 window — the
    synth itself recorded which files it wrote, and that list is authoritative.

    This is the case that today's catch-up exposed: synth ran at 09:36 after
    a power outage, the auto-commit landed at 09:36 (not 02-04), and the old
    git-log filter returned empty. The manifest path lists the files
    regardless of when auto-commit fired.
    """
    today = "2026-05-27"
    _write_concept(tmp_vault, "off-window-concept", "Off Window")
    _write_manifest(
        tmp_vault, today,
        concepts_written=1,
        concept_paths=["vault/knowledge/concepts/off-window-concept.md"],
    )
    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["off-window-concept.md"]


def test_select_target_articles_falls_back_to_git_log_for_legacy_manifest(monkeypatch, tmp_vault):
    """Manifests written before 2026-05-27 lack `concept_paths`. The selector
    falls back to `list_macmini_synth_files` so the rollout day's nightly run
    still finds targets — no flag day required."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "legacy-concept", "Legacy")
    # No concept_paths in the manifest (pre-rollout shape).
    _write_manifest(tmp_vault, today, concepts_written=1)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            root / "vault" / "knowledge" / "concepts" / "legacy-concept.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["legacy-concept.md"]


def test_select_target_articles_manifest_path_skips_missing_files(tmp_vault):
    """Defensive: a manifest path may reference a file that's been deleted
    between synth-write and critic-read (e.g., the auto-commit hook removed
    a duplicate). Skip silently rather than crashing."""
    today = "2026-05-27"
    _write_concept(tmp_vault, "exists", "Exists")
    _write_manifest(
        tmp_vault, today,
        concepts_written=2,
        concept_paths=[
            "vault/knowledge/concepts/exists.md",
            "vault/knowledge/concepts/deleted-before-critic.md",
        ],
    )
    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["exists.md"]


def test_select_target_articles_manifest_path_rejects_paths_outside_concepts(tmp_vault):
    """A malformed manifest pointing at a connections path or a vault root
    file must not get smuggled through the fresh-lane selector. The fresh
    lane is concepts-only by contract."""
    today = "2026-05-27"
    _write_concept(tmp_vault, "real-concept", "Real")
    _write_connection(tmp_vault, "wrong-folder")
    _write_manifest(
        tmp_vault, today,
        concepts_written=1,
        concept_paths=[
            "vault/knowledge/concepts/real-concept.md",
            "vault/knowledge/connections/wrong-folder.md",  # rejected
            "vault/knowledge/index.md",                      # rejected
        ],
    )
    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["real-concept.md"]


def test_select_target_articles_manifest_path_skips_already_expanded(tmp_vault):
    """The expansion-exists short-circuit applies to the manifest path too —
    snapshot semantics preserved across the proxy change."""
    today = "2026-05-27"
    _write_concept(tmp_vault, "already", "Already")
    _write_concept(tmp_vault, "fresh", "Fresh")
    (tmp_vault / "vault" / "knowledge" / "expansions" / "already.md").write_text(
        "prior", encoding="utf-8",
    )
    _write_manifest(
        tmp_vault, today,
        concepts_written=2,
        concept_paths=[
            "vault/knowledge/concepts/already.md",
            "vault/knowledge/concepts/fresh.md",
        ],
    )
    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["fresh.md"]


# ---------------------------------------------------------------------------
# Backfill lane (2026-05-27) — drains historical corpus debt
# ---------------------------------------------------------------------------


def test_select_backfill_targets_returns_orphan_concepts_oldest_first(tmp_vault):
    """Backfill scans concepts/ for files missing an expansion sibling and
    returns oldest-first by source mtime. The backlog drains in the order the
    files were originally synthesized."""
    import os

    older = _write_concept(tmp_vault, "older", "Older")
    newer = _write_concept(tmp_vault, "newer", "Newer")
    os.utime(older, (1_700_000_000, 1_700_000_000))
    os.utime(newer, (1_750_000_000, 1_750_000_000))

    backfill = select_backfill_targets(tmp_vault, max_targets=5, include_connections=False)
    assert [p.name for p in backfill] == ["older.md", "newer.md"]


def test_select_backfill_targets_skips_already_expanded(tmp_vault):
    """A concept with an expansion file is not a backfill candidate — that's
    the whole signal we use to define 'orphan'."""
    _write_concept(tmp_vault, "expanded", "Expanded")
    _write_concept(tmp_vault, "orphan", "Orphan")
    (tmp_vault / "vault" / "knowledge" / "expansions" / "expanded.md").write_text(
        "prior", encoding="utf-8",
    )
    backfill = select_backfill_targets(tmp_vault, max_targets=5, include_connections=False)
    assert [p.name for p in backfill] == ["orphan.md"]


def test_select_backfill_targets_includes_connections_when_enabled(tmp_vault):
    """Connections are second-class in the nightly fresh lane (concepts only),
    but the backfill lane treats them as eligible since the historical debt
    spans both folders. Connection expansions land under
    `expansions/connections/` per resolve_expansion_path."""
    (tmp_vault / "vault" / "knowledge" / "expansions" / "connections").mkdir(parents=True)
    _write_concept(tmp_vault, "concept-orphan", "Concept")
    _write_connection(tmp_vault, "connection-orphan")

    with_conn = select_backfill_targets(tmp_vault, max_targets=5, include_connections=True)
    without_conn = select_backfill_targets(tmp_vault, max_targets=5, include_connections=False)

    assert {p.name for p in with_conn} == {"concept-orphan.md", "connection-orphan.md"}
    assert {p.name for p in without_conn} == {"concept-orphan.md"}


def test_select_backfill_targets_excludes_paths_already_chosen_by_fresh_lane(tmp_vault):
    """When a fresh-lane target is already queued, backfill must NOT pick it
    again — that would double-critique the same article in one nightly run.
    The `exclude` arg is the de-dup hook."""
    fresh = _write_concept(tmp_vault, "fresh", "Fresh")
    _write_concept(tmp_vault, "other-orphan", "Other")
    backfill = select_backfill_targets(
        tmp_vault, max_targets=5, include_connections=False, exclude=[fresh],
    )
    assert [p.name for p in backfill] == ["other-orphan.md"]


def test_select_backfill_targets_caps_at_max_targets(tmp_vault):
    """Backfill must honor its cap regardless of backlog size — 5/night by
    default is the slow-drain rate that keeps the wall budget available for
    the fresh lane."""
    for slug in ("a", "b", "c", "d", "e", "f", "g"):
        _write_concept(tmp_vault, slug, slug.upper())
    backfill = select_backfill_targets(tmp_vault, max_targets=3, include_connections=False)
    assert len(backfill) == 3


def test_select_backfill_targets_returns_empty_on_fresh_vault(tmp_vault):
    """No concepts/connections directories yet → no candidates → empty list,
    not a crash. Defends against fresh-clone edge cases before the synth has
    ever run."""
    backfill = select_backfill_targets(tmp_vault, max_targets=5, include_connections=True)
    assert backfill == []
