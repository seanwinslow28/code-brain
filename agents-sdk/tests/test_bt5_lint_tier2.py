"""BT5 Phase C — C3: wire knowledge_lint's Tier-2 LLM leg for real.

Fixes Origin C from the BT5 diagnosis (docs/plans/wwf5d/fable-runs/bt5-fable.md):
knowledge_lint.main() passed no llm_caller, so the semantic contradiction scan
and `soul-tier-a-conflict` never ran in production; the prompt embedded no
article corpus; and the LLM block swallowed failures with `except: pass`.

Failing-test-first (verification-loops). These assert the DESIRED post-fix
behavior, so they are RED until C3 lands.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from agents.knowledge_lint import (
    _batch_corpus,
    _build_tier2_prompt,
    _load_concept_corpus,
    format_report,
    run_tier1,
    run_tier2,
)
from lib.hybrid_router import HybridRouter, WOLUnavailable


def _concept(vault: Path, slug: str, definition: str) -> None:
    d = vault / "knowledge" / "concepts"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.md").write_text(
        f"# {slug.title()}\n\n## Definition\n{definition}\n", encoding="utf-8"
    )


# ─── corpus injection ────────────────────────────────────────────────────────

def test_build_tier2_prompt_includes_corpus_batch() -> None:
    """C3: the prompt must carry the actual articles to review — the old
    prompt embedded no corpus, so a wired caller reviewed nothing."""
    prompt = _build_tier2_prompt(
        "", [("knowledge/concepts/alpha.md", "# Alpha\nAlpha means the first thing.")]
    )
    assert "knowledge/concepts/alpha.md" in prompt
    assert "Alpha means the first thing" in prompt
    assert "soul_conflicts" in prompt  # instructions preserved


def test_build_tier2_prompt_backward_compatible_single_arg() -> None:
    """Existing callers pass only soul_context — must still work (no corpus)."""
    assert "soul_conflicts" in _build_tier2_prompt("")
    assert "soul_conflicts" in _build_tier2_prompt("## SOUL — creative-studio\n")


def test_load_concept_corpus_reads_digests(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    _concept(vault, "alpha", "Alpha is the first thing and it matters.")
    _concept(vault, "beta", "Beta is the second thing entirely.")
    corpus = _load_concept_corpus(vault)
    rels = {r for r, _ in corpus}
    assert "knowledge/concepts/alpha.md" in rels
    assert "knowledge/concepts/beta.md" in rels
    assert any("Alpha is the first" in dg for _, dg in corpus)


def test_load_concept_corpus_empty_when_no_concepts(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    assert _load_concept_corpus(vault) == []


def test_batch_corpus_splits_by_char_budget() -> None:
    corpus = [(f"c{i}.md", "x" * 100) for i in range(10)]
    batches = _batch_corpus(corpus, max_chars=250)
    assert len(batches) > 1
    assert sum(len(b) for b in batches) == 10  # nothing dropped


# ─── run_tier2 wiring ────────────────────────────────────────────────────────

def test_run_tier2_calls_llm_per_batch_and_reports_reviewed(tmp_path: Path) -> None:
    """C3: with concepts present, run_tier2 batches them and calls the LLM per
    batch, injecting the corpus, and records how many batches it reviewed."""
    vault = tmp_path / "vault"
    vault.mkdir()
    for i in range(4):
        _concept(vault, f"c{i}", "definition body " * 20)

    calls = {"n": 0}

    def fake_llm(prompt: str) -> dict:
        calls["n"] += 1
        assert "knowledge/concepts/" in prompt  # corpus injected
        return {"contradictions": [], "soul_conflicts": []}

    notes: list[str] = []
    run_tier2(
        vault, llm_caller=fake_llm, soul_context="", report_notes=notes,
        tier2_batch_max_chars=200,
    )
    assert calls["n"] >= 2, "multiple batches must each get an LLM call"
    assert any("reviewed" in n for n in notes)
    assert any("Tier-2 LLM" in n for n in notes)


def test_run_tier2_llm_failure_is_reported_not_silent(tmp_path: Path) -> None:
    """C3: the old `except Exception: pass` masked scan failures as clean
    scans. A failure must surface in the report notes."""
    vault = tmp_path / "vault"
    vault.mkdir()
    _concept(vault, "alpha", "alpha body")

    def boom(prompt: str) -> dict:
        raise RuntimeError("network down")

    notes: list[str] = []
    issues = run_tier2(vault, llm_caller=boom, soul_context="", report_notes=notes)
    assert any("Tier-2 LLM" in n and "fail" in n.lower() for n in notes)
    # still returns cleanly (no raise), structural/sql findings unaffected
    assert isinstance(issues, list)


def test_run_tier2_still_finds_soul_conflict_with_empty_vault(tmp_path: Path) -> None:
    """Backward-compat: the one-call floor preserves the existing contract —
    an empty vault still makes one LLM call and processes soul_conflicts."""
    vault = tmp_path / "vault"
    vault.mkdir()

    def fake_llm(prompt: str) -> dict:
        return {
            "contradictions": [],
            "soul_conflicts": [
                {"file": "knowledge/concepts/x.md", "tier_a_item": "T", "detail": "d"}
            ],
        }

    issues = run_tier2(vault, llm_caller=fake_llm, soul_context="")
    assert any(i.kind == "soul-tier-a-conflict" for i in issues)


# ─── report footer ───────────────────────────────────────────────────────────

def test_format_report_renders_tier2_notes() -> None:
    tier1 = run_tier1(Path("/nonexistent-vault-xyz"))  # empty → 0 issues
    report = format_report(
        tier1=tier1, tier2=[], today="2026-07-05",
        tier2_notes=["Tier-2 LLM scan: deferred (host unreachable)."],
    )
    assert "Tier-2 LLM scan: deferred (host unreachable)." in report


# ─── main() honest deferral (done-criterion 5) ───────────────────────────────

def test_main_reports_deferral_when_host_unreachable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """C3 done-criterion 5: with the Tier-2 host down, the lint report must
    contain an explicit deferral line — not silence."""
    import agents.knowledge_lint as kl

    monkeypatch.setenv("PUSHOVER_USER_KEY", "stub")
    monkeypatch.setenv("PUSHOVER_API_TOKEN", "stub")
    vault = tmp_path / "vault"
    (vault / "health").mkdir(parents=True, exist_ok=True)
    logs = tmp_path / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    cfg = SimpleNamespace(vault_root=vault, log_dir=logs, log_level="INFO")
    monkeypatch.setattr(kl, "load_config", lambda: cfg)
    # Force Tier 2 to run by faking a non-clean Tier 1.
    from agents.knowledge_lint import Tier1Report, LintIssue, LintSeverity
    fake_t1 = Tier1Report(issues=[LintIssue(kind="x", severity=LintSeverity.LOW,
                                            file=Path("a.md"), detail="d", tier=1)])
    monkeypatch.setattr(kl, "run_tier1", lambda root: fake_t1)
    monkeypatch.setattr(kl, "build_soul_context", lambda c: "")

    async def _raise_wol(self, *a, **k):
        raise WOLUnavailable("mbp down")
    monkeypatch.setattr(HybridRouter, "route_to_macbook", _raise_wol)
    monkeypatch.setattr(sys, "argv", ["knowledge_lint"])

    rc = kl.main()
    assert rc == 0
    report_path = vault / "health" / f"{date.today().isoformat()}-lint-report.md"
    assert report_path.exists()
    body = report_path.read_text(encoding="utf-8")
    assert "Tier-2 LLM scan: deferred (host unreachable)." in body
