"""Tests for agents.knowledge_lint — D.3 two-tier vault health scan."""

from __future__ import annotations

from pathlib import Path

import pytest

from agents.knowledge_lint import (
    LintIssue,
    LintSeverity,
    Tier1Report,
    build_synthetic_vault,
    find_broken_wikilinks,
    find_camelcase_filenames,
    find_missing_frontmatter,
    find_orphan_files,
    recall_against_oracle,
    run_tier1,
)


def _touch(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_find_broken_wikilinks(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    _touch(v / "a.md", "links to [[b]] and [[missing]]")
    _touch(v / "b.md", "exists")
    issues = find_broken_wikilinks(v)
    targets = {i.detail for i in issues}
    assert any("missing" in t for t in targets)
    assert not any("b" == t.strip() for t in targets)


def test_find_orphan_files(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    # index.md is the MOC hub (skip-listed), linked files cross-reference
    _touch(v / "index.md", "see [[a]] and [[b]]")
    _touch(v / "a.md", "see [[b]]")
    _touch(v / "b.md", "see [[a]]")
    _touch(v / "orphan.md", "nobody links to me")
    issues = find_orphan_files(v)
    orphan_files = {i.file.name for i in issues}
    assert "orphan.md" in orphan_files
    assert "a.md" not in orphan_files
    assert "b.md" not in orphan_files
    assert "index.md" not in orphan_files


def test_find_missing_frontmatter_scoped_to_knowledge(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    _touch(v / "knowledge" / "concepts" / "good.md", "---\ntitle: Good\n---\nBody")
    _touch(v / "knowledge" / "concepts" / "bad.md", "no frontmatter at all")
    _touch(v / "notes" / "freeform.md", "no frontmatter but not required here")
    issues = find_missing_frontmatter(v)
    bad_files = {i.file.name for i in issues}
    assert "bad.md" in bad_files
    assert "good.md" not in bad_files
    assert "freeform.md" not in bad_files


def test_find_camelcase_filenames_scoped_to_knowledge(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    _touch(v / "knowledge" / "concepts" / "good-name.md", "ok")
    _touch(v / "knowledge" / "concepts" / "BadName.md", "camel")
    _touch(v / "notes" / "AnyCase.md", "not in knowledge")
    issues = find_camelcase_filenames(v)
    files = {i.file.name for i in issues}
    assert "BadName.md" in files
    assert "good-name.md" not in files
    assert "AnyCase.md" not in files


def test_run_tier1_aggregates_all_structural_issues(tmp_path: Path) -> None:
    v = tmp_path / "vault"
    _touch(v / "knowledge" / "concepts" / "rife.md", "---\ntitle: RIFE\n---\n[[NotHere]]")
    _touch(v / "knowledge" / "concepts" / "BadName.md", "no frontmatter")
    _touch(v / "orphan.md", "nobody points here")

    report: Tier1Report = run_tier1(v)
    assert report.total_issues >= 3
    kinds = {i.kind for i in report.issues}
    assert "broken-wikilink" in kinds
    assert "orphan" in kinds
    assert "missing-frontmatter" in kinds
    assert "camelcase-filename" in kinds


def test_build_synthetic_vault_has_20_planted_issues(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    oracle = build_synthetic_vault(vault)
    # Count distinct oracle entries by kind
    total_planted = sum(oracle["counts"].values())
    assert total_planted == 20, f"expected 20 planted, got {total_planted}"
    # 10 clean controls
    assert oracle["clean_count"] == 10
    # Full directory listing ~30 files
    md_files = list(vault.rglob("*.md"))
    assert len(md_files) >= 30


def test_tier1_recall_on_synthetic_vault(tmp_path: Path) -> None:
    """The gate-check test: lint must catch ≥19 of 20 TIER-1 issues.

    Only Tier 1 issues are tested here (Tier 2 requires an LLM). The oracle
    separates Tier 1 from Tier 2 planted issues.
    """
    vault = tmp_path / "vault"
    oracle = build_synthetic_vault(vault)
    report = run_tier1(vault)

    recall = recall_against_oracle(report.issues, oracle["tier1"])
    # Plan §4 gate: ≥95% recall on ≥19 of 20. With 14 Tier-1 issues planted,
    # ≥13/14 = 92.9%, ≥14/14 = 100%. We pass on 100% to keep the gate tight.
    assert recall >= 0.95, f"Tier 1 recall {recall:.2%} below 95%"
    # Zero false positives on clean controls
    flagged = {i.file.name for i in report.issues}
    for clean_name in oracle["clean_files"]:
        assert clean_name not in flagged, (
            f"False positive on clean file {clean_name}"
        )
