import json
from datetime import date
from pathlib import Path

import pytest

from lib.critic_selector import (
    list_macmini_synth_files,
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
