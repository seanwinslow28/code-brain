"""Tests for agents.knowledge_lint — D.3 two-tier vault health scan."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from agents.knowledge_lint import (
    LintIssue,
    LintSeverity,
    Tier1Report,
    _build_tier2_prompt,
    build_soul_context,
    build_synthetic_vault,
    find_broken_wikilinks,
    find_camelcase_filenames,
    find_missing_frontmatter,
    find_orphan_files,
    recall_against_oracle,
    run_tier1,
    run_tier2,
)
from lib.artifact_loader import clear_cache


@pytest.fixture(autouse=True)
def _reset_artifact_cache():
    clear_cache()
    yield
    clear_cache()


@dataclass
class _FakeConfig:
    """Stand-in for lib.config.Config — fields knowledge_lint touches."""

    vault_root: Path
    artifacts: dict = field(default_factory=dict)

    def artifact_config(self, name: str) -> dict:
        if not self.artifacts.get("enabled", False):
            return {}
        return self.artifacts.get("per_agent", {}).get(name, {})


def _kl_config(tmp_artifacts: Path, *, enabled: bool = True, on_demand=("SOUL",)) -> _FakeConfig:
    return _FakeConfig(
        vault_root=tmp_artifacts,
        artifacts={
            "enabled": enabled,
            "per_agent": {"knowledge_lint": {"on_demand": list(on_demand)}},
        },
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


# ─── Phase 2: SOUL context + soul-tier-a-conflict ────────────────────────


class TestBuildSoulContext:
    def test_returns_empty_when_config_is_none(self):
        assert build_soul_context(None) == ""

    def test_returns_empty_when_artifacts_disabled(self, tmp_artifacts: Path):
        cfg = _kl_config(tmp_artifacts, enabled=False)
        assert build_soul_context(cfg) == ""

    def test_returns_empty_when_no_per_agent_entry(self, tmp_artifacts: Path):
        cfg = _FakeConfig(
            vault_root=tmp_artifacts,
            artifacts={"enabled": True, "per_agent": {}},
        )
        assert build_soul_context(cfg) == ""

    def test_returns_empty_when_soul_not_in_on_demand(self, tmp_artifacts: Path):
        cfg = _kl_config(tmp_artifacts, on_demand=("USER",))
        assert build_soul_context(cfg) == ""

    def test_includes_all_three_domain_souls(self, tmp_artifacts: Path):
        ctx = build_soul_context(_kl_config(tmp_artifacts))
        assert "## SOUL — creative-studio" in ctx
        assert "## SOUL — life-systems" in ctx
        assert "## SOUL — job-hunt-2026" in ctx
        assert ctx.startswith("--- BEGIN OPERATING-MODEL SOUL CONTEXT")
        assert "--- END OPERATING-MODEL SOUL CONTEXT ---" in ctx


class TestBuildTier2Prompt:
    def test_includes_soul_context_when_supplied(self):
        soul = "--- BEGIN OPERATING-MODEL SOUL CONTEXT ---\n\n## SOUL — creative-studio\nbody\n--- END ---\n\n"
        prompt = _build_tier2_prompt(soul)
        assert prompt.startswith("--- BEGIN OPERATING-MODEL SOUL CONTEXT")
        assert "soul_conflicts" in prompt
        assert "tier_a_item" in prompt

    def test_omits_soul_section_when_empty(self):
        prompt = _build_tier2_prompt("")
        assert not prompt.startswith("---")
        assert "soul_conflicts" in prompt  # instructions still ask for it


class TestRunTier2SoulConflicts:
    def test_emits_soul_tier_a_conflict_issue_at_high_severity(self, tmp_path: Path):
        vault = tmp_path / "vault"
        vault.mkdir()

        def fake_llm(prompt: str) -> dict:
            assert "## SOUL — creative-studio" in prompt
            return {
                "contradictions": [],
                "soul_conflicts": [
                    {
                        "file": "knowledge/concepts/sample.md",
                        "tier_a_item": "GitHub write is hard never",
                        "detail": "Article asserts GitHub write workflow is OK.",
                    }
                ],
            }

        soul_ctx = (
            "--- BEGIN OPERATING-MODEL SOUL CONTEXT ---\n\n"
            "## SOUL — creative-studio\n\nGitHub write is hard never.\n"
            "## SOUL — life-systems\n\nbody\n"
            "## SOUL — job-hunt-2026\n\nbody\n"
            "--- END OPERATING-MODEL SOUL CONTEXT ---\n\n"
        )
        issues = run_tier2(vault, llm_caller=fake_llm, soul_context=soul_ctx)
        soul_issues = [i for i in issues if i.kind == "soul-tier-a-conflict"]
        assert len(soul_issues) == 1
        i = soul_issues[0]
        assert i.severity == LintSeverity.HIGH
        assert i.tier == 2
        assert "GitHub write is hard never" in i.detail
        assert i.file == Path("knowledge/concepts/sample.md")

    def test_no_false_positives_when_soul_conflicts_empty(self, tmp_path: Path):
        vault = tmp_path / "vault"
        vault.mkdir()

        def fake_llm(prompt: str) -> dict:
            return {"contradictions": [], "soul_conflicts": []}

        issues = run_tier2(vault, llm_caller=fake_llm, soul_context="")
        soul_issues = [i for i in issues if i.kind == "soul-tier-a-conflict"]
        assert soul_issues == []

    def test_skips_entries_with_missing_file_field(self, tmp_path: Path):
        vault = tmp_path / "vault"
        vault.mkdir()

        def fake_llm(prompt: str) -> dict:
            return {
                "contradictions": [],
                "soul_conflicts": [
                    {"file": "", "tier_a_item": "x", "detail": "skipped"},
                    {"file": "k/concepts/real.md", "tier_a_item": "y", "detail": "kept"},
                ],
            }

        issues = run_tier2(vault, llm_caller=fake_llm, soul_context="")
        soul_issues = [i for i in issues if i.kind == "soul-tier-a-conflict"]
        assert len(soul_issues) == 1
        assert soul_issues[0].file == Path("k/concepts/real.md")

    def test_caller_exception_does_not_break_run(self, tmp_path: Path):
        vault = tmp_path / "vault"
        vault.mkdir()

        def boom(prompt: str) -> dict:
            raise RuntimeError("simulated network failure")

        # Should not raise; staleness scan still runs (returns whatever it finds)
        issues = run_tier2(vault, llm_caller=boom, soul_context="")
        soul_issues = [i for i in issues if i.kind == "soul-tier-a-conflict"]
        assert soul_issues == []


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


# ─── Phase D — SQL fast path on concept_edges ─────────────────────────────


class TestSqlFastPath:
    """Phase D (v3.20.0) — knowledge_lint Tier 2 reads concept_edges
    directly for `relation='contradicts'` rows. Documented dedupe rule:
    SQL hits win when both paths surface the same pair."""

    @staticmethod
    def _seed_db(vault_root: Path, pairs: list[tuple[str, str]]) -> None:
        """Create vault/.vault-index.db with the Phase D schema and seed
        contradiction rows. Uses init_db so the schema matches production."""
        from agents.vault_indexer import init_db
        from lib import concept_edges as ce

        db_path = vault_root / ".vault-index.db"
        conn = init_db(db_path)
        for from_slug, to_slug in pairs:
            ce.insert_edge(
                conn,
                from_slug=from_slug,
                to_slug=to_slug,
                relation="contradicts",
                source_synth_run="2026-05-01T00:00:00",
            )
        conn.close()

    def test_sql_fast_path_emits_critical_for_each_row(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        vault.mkdir()
        self._seed_db(vault, [("alpha", "beta"), ("gamma", "delta")])

        issues = run_tier2(vault)  # llm_caller=None — exercises ONLY the SQL path
        contradictions = [i for i in issues if i.kind == "contradiction"]
        assert len(contradictions) == 2
        for issue in contradictions:
            assert issue.severity == LintSeverity.CRITICAL
            assert issue.tier == 2
            assert "(source=sql)" in issue.detail

    def test_sql_fast_path_skipped_silently_when_db_missing(
        self, tmp_path: Path
    ) -> None:
        """Fresh vault: no DB file. Must NOT raise; must NOT emit
        contradictions; LLM-less Tier 2 still completes."""
        vault = tmp_path / "vault"
        vault.mkdir()
        # No DB seeded.
        issues = run_tier2(vault)
        contradictions = [i for i in issues if i.kind == "contradiction"]
        assert contradictions == []

    def test_sql_fast_path_skipped_when_table_missing(self, tmp_path: Path) -> None:
        """DB exists (from a hypothetical legacy vault_indexer that didn't
        have the Phase D schema) but concept_edges table is absent. Must
        no-op cleanly, not crash, and not mutate the schema."""
        import sqlite3 as _sqlite3

        vault = tmp_path / "vault"
        vault.mkdir()
        db_path = vault / ".vault-index.db"
        # Hand-roll the chunks table only — no concept_edges.
        conn = _sqlite3.connect(str(db_path))
        conn.execute(
            "CREATE TABLE chunks (id INTEGER PRIMARY KEY, file_path TEXT)"
        )
        conn.commit()
        conn.close()

        issues = run_tier2(vault)
        assert [i for i in issues if i.kind == "contradiction"] == []

        # Verify we did NOT mutate the schema as a side effect of the read pass.
        check = _sqlite3.connect(str(db_path))
        try:
            row = check.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='concept_edges'"
            ).fetchone()
            assert row is None, "Tier 2 must not create concept_edges as a side effect"
        finally:
            check.close()

    def test_sql_and_llm_dedupe_by_slug_pair(self, tmp_path: Path) -> None:
        """Phase D dedupe rule — when both paths surface the same
        (from_slug, to_slug) pair, the SQL row wins and the LLM duplicate
        is dropped. LLM-only contradictions still surface."""
        vault = tmp_path / "vault"
        vault.mkdir()
        self._seed_db(vault, [("alpha", "beta")])

        # LLM emits the same alpha-beta pair (should be deduped) AND a new
        # gamma-delta pair (should surface as source=llm).
        def llm(prompt: str) -> dict:
            return {
                "contradictions": [
                    {"files": ["knowledge/concepts/alpha.md",
                               "knowledge/concepts/beta.md"],
                     "detail": "would be a dupe of SQL"},
                    {"files": ["knowledge/concepts/gamma.md",
                               "knowledge/concepts/delta.md"],
                     "detail": "synthesizer missed this one"},
                ],
                "soul_conflicts": [],
            }

        issues = run_tier2(vault, llm_caller=llm)
        contradictions = [i for i in issues if i.kind == "contradiction"]
        # 1 SQL hit (alpha-beta) + 1 LLM-unique (gamma-delta) = 2 total.
        assert len(contradictions) == 2
        sources = {i.detail for i in contradictions}
        # SQL row carries (source=sql); LLM row keeps the LLM's prose detail.
        assert any("(source=sql)" in d for d in sources)
        assert any("synthesizer missed this one" in d for d in sources)
        # The LLM dupe of alpha-beta did NOT survive.
        assert not any(
            "would be a dupe of SQL" in d for d in sources
        )

    def test_sql_fast_path_preserves_soul_conflicts_from_llm(
        self, tmp_path: Path
    ) -> None:
        """Phase D dedupe targets contradictions only — soul-tier-a-conflict
        is a Phase 2 capability with no SQL substitute and must always
        surface from the LLM, even when SQL fast path has hits."""
        vault = tmp_path / "vault"
        vault.mkdir()
        self._seed_db(vault, [("alpha", "beta")])

        def llm(prompt: str) -> dict:
            return {
                "contradictions": [],
                "soul_conflicts": [
                    {"file": "knowledge/concepts/x.md",
                     "tier_a_item": "Protect deep-work mornings",
                     "detail": "article suggests scheduling meetings before 10am"},
                ],
            }

        issues = run_tier2(vault, llm_caller=llm)
        soul_issues = [i for i in issues if i.kind == "soul-tier-a-conflict"]
        assert len(soul_issues) == 1
        assert "Protect deep-work mornings" in soul_issues[0].detail
