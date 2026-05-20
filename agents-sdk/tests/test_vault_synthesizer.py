"""Tests for agents.vault_synthesizer — D.2.b concept + connection articles.

Phase D (v3.20.0, 2026-05-01) extensions: edge-write side effects via
the new `db_conn` parameter, including invalid-relation rejection that
must NOT abort the synthesis run.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agents.vault_indexer import init_db
from agents.vault_synthesizer import (
    MIN_WIKILINKS_PER_ARTICLE,
    SynthesisResult,
    count_wikilinks,
    extract_wikilinks,
    format_concept_article,
    format_connection_article,
    regenerate_index,
    run_synthesis,
    validate_article_body,
)


@pytest.fixture(autouse=True)
def _stub_pushover_creds(monkeypatch: pytest.MonkeyPatch) -> None:
    """Inject dummy Pushover env vars so ensure_credentials_or_raise() passes.

    Added in B4 (vs-019): run_synthesis() now calls ensure_credentials_or_raise()
    at boot. Unit tests don't have keychain access, so we set non-empty stubs.
    This fixture is autouse so every test in this module gets it automatically.
    """
    monkeypatch.setenv("PUSHOVER_USER_KEY", "test-stub-user")
    monkeypatch.setenv("PUSHOVER_API_TOKEN", "test-stub-token")


def _make_vault(tmp_path: Path, files: dict[str, str]) -> Path:
    vault = tmp_path / "vault"
    for rel, content in files.items():
        p = vault / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return vault


def test_extract_wikilinks() -> None:
    body = "See [[Concept A]] and also [[Concept-B|label]] plus [[Concept C]]."
    assert set(extract_wikilinks(body)) == {"Concept A", "Concept-B", "Concept C"}


def test_count_wikilinks_zero_when_missing() -> None:
    assert count_wikilinks("plain text no links") == 0


def test_validate_article_body_requires_two_wikilinks() -> None:
    ok = "## Definition\n\nSee [[X]] and [[Y]] for context."
    assert validate_article_body(ok) is True

    too_few = "## Definition\n\nOnly [[X]] here."
    assert validate_article_body(too_few) is False


def test_format_concept_article_has_frontmatter_and_wikilinks() -> None:
    body = format_concept_article(
        title="RIFE Interpolation Hyperparameters",
        definition="RIFE is a frame interpolation model used to densify keyframes.",
        context="Phase 5 autoresearch tunes temporal_smoothing.",
        examples=["Wan 2.2 → RIFE 8x → Pixel Quantizer passes 87.6%"],
        related=["Wan 2.2 Keyframes", "Pixel Quantizer"],
        sources=["05_projects/phase5-autoresearch.md", "90_system/rife-notes.md"],
        today="2026-04-17",
    )
    assert body.startswith("---")
    assert "type: concept" in body
    assert "[[Wan 2.2 Keyframes]]" in body
    assert "[[Pixel Quantizer]]" in body
    assert count_wikilinks(body) >= MIN_WIKILINKS_PER_ARTICLE


def test_format_connection_article_has_three_concepts() -> None:
    body = format_connection_article(
        title="Keyframe Sparsity Tradeoff",
        synthesis="Fewer keyframes = faster generation but more drift.",
        concepts=["RIFE Interpolation Hyperparameters", "Wan 2.2 Keyframes", "Pixel Quantizer"],
        implications=["Tune per animation complexity.", "Document regression thresholds."],
        today="2026-04-17",
    )
    assert "type: connection" in body
    for c in ["RIFE Interpolation Hyperparameters", "Wan 2.2 Keyframes", "Pixel Quantizer"]:
        assert f"[[{c}]]" in body
    assert count_wikilinks(body) >= 3


def test_regenerate_index_lists_all_articles(tmp_path: Path) -> None:
    knowledge = tmp_path / "vault" / "knowledge"
    (knowledge / "concepts").mkdir(parents=True)
    (knowledge / "connections").mkdir(parents=True)
    (knowledge / "concepts" / "rife-hyperparams.md").write_text(
        "---\ntitle: RIFE Hyperparams\ntype: concept\n---\nBody [[A]] [[B]]",
        encoding="utf-8",
    )
    (knowledge / "connections" / "keyframe-tradeoff.md").write_text(
        "---\ntitle: Keyframe Tradeoff\ntype: connection\n---\nBody [[A]] [[B]] [[C]]",
        encoding="utf-8",
    )

    regenerate_index(knowledge)
    index = (knowledge / "index.md").read_text(encoding="utf-8")
    assert "RIFE Hyperparams" in index
    assert "Keyframe Tradeoff" in index
    assert "concepts/rife-hyperparams.md" in index
    assert "connections/keyframe-tradeoff.md" in index


def test_run_synthesis_happy_path(tmp_path: Path) -> None:
    """End-to-end with a mock LLM + mock retrieval."""
    vault = _make_vault(
        tmp_path,
        {
            "05_projects/phase5-autoresearch.md": "# Phase 5\nWe tested RIFE temporal_smoothing=0.8.",
            "05_projects/pixel-quantizer.md": "# Pixel Quantizer\nQuantizes to 4-color palette.",
            "05_projects/wan-notes.md": "# Wan 2.2\nKeyframe-based video gen.",
        },
    )

    def fake_llm(prompt: str, max_tokens: int = 2000) -> dict:
        return {
            "concepts": [
                {
                    "title": "RIFE Interpolation Hyperparameters",
                    "definition": (
                        "RIFE Interpolation Hyperparameters control how the "
                        "model bridges sparse keyframes by synthesizing "
                        "intermediate frames. The `temporal_smoothing` knob "
                        "trades drift against perceived motion smoothness. "
                        "Tuning is empirical because the optimum shifts with "
                        "the upstream keyframe density and the downstream "
                        "quantizer's tolerance for jitter."
                    ),
                    "context": "Phase 5 tuning surfaces this tradeoff in autoresearch sweeps.",
                    "evidence": [
                        "RIFE Interpolation Hyperparameters control how the model bridges sparse keyframes by synthesizing intermediate frames.",
                        "The temporal_smoothing knob trades drift against perceived motion smoothness during the densification pass.",
                    ],
                    "examples": ["temporal_smoothing=0.8 wins by 8% on Pixel Quantizer eval"],
                    "related": ["Wan 2.2 Keyframes", "Pixel Quantizer"],
                }
            ],
            "connections": [
                {
                    "title": "Keyframe Sparsity Tradeoff",
                    "synthesis": (
                        "Sparser Wan 2.2 keyframes accelerate generation but "
                        "force RIFE to invent more in-between content, which "
                        "compounds drift before the Pixel Quantizer can "
                        "stabilize it. The tension is not local — it propagates "
                        "across three pipeline stages, each of which would look "
                        "tunable in isolation. Optimizing any stage alone "
                        "regresses the others."
                    ),
                    "concepts": [
                        "RIFE Interpolation Hyperparameters",
                        "Wan 2.2 Keyframes",
                        "Pixel Quantizer",
                    ],
                    "evidence": {
                        "RIFE Interpolation Hyperparameters": [
                            "RIFE Interpolation Hyperparameters control how the model bridges sparse keyframes by synthesizing intermediate frames during the densification pass."
                        ],
                        "Wan 2.2 Keyframes": [
                            "Wan 2.2 emits keyframes whose spacing directly determines how much intermediate content RIFE must invent downstream."
                        ],
                        "Pixel Quantizer": [
                            "The Pixel Quantizer absorbs jitter from upstream drift but its 4-color palette compresses information past the point where smoothing can recover it."
                        ],
                    },
                    "implications": [
                        "Per-pipeline-stage tuning is insufficient; sweeps must explore the joint space across keyframe spacing, smoothing, and quantizer palette.",
                        "Document regression thresholds at every stage so a regression at stage N can be attributed to a setting change at stage N-1 or N-2.",
                    ],
                }
            ],
        }

    changed = [
        vault / "05_projects/phase5-autoresearch.md",
        vault / "05_projects/pixel-quantizer.md",
    ]

    def fake_search(query: str, top_k: int = 5) -> list[dict]:
        # Return ≥2 chunks so Tier-1.5's thin-source skip path doesn't fire.
        return [
            {"file_path": "05_projects/wan-notes.md", "chunk_text": "Wan 2.2 keyframe density notes", "similarity": 0.9},
            {"file_path": "05_projects/quantizer.md", "chunk_text": "Pixel Quantizer palette behaviour", "similarity": 0.8},
        ]

    result = run_synthesis(
        vault_root=vault,
        changed_files=changed,
        llm_caller=fake_llm,
        retriever=fake_search,
        now_iso="2026-04-17",
        budget_seconds=300,
    )

    assert isinstance(result, SynthesisResult)
    assert result.status == "ok"
    assert result.concepts_written >= 1
    assert result.connections_written >= 1
    concepts_dir = vault / "knowledge" / "concepts"
    connections_dir = vault / "knowledge" / "connections"
    assert any(p.suffix == ".md" for p in concepts_dir.iterdir())
    assert any(p.suffix == ".md" for p in connections_dir.iterdir())
    # index.md exists
    assert (vault / "knowledge" / "index.md").exists()


def test_run_synthesis_rejects_articles_without_two_wikilinks(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path, {"x.md": "seed"})

    def bad_llm(prompt: str, max_tokens: int = 2000) -> dict:
        return {
            "concepts": [
                {
                    "title": "Orphan Concept",
                    "definition": "No links here.",
                    "context": "none",
                    "examples": [],
                    "related": [],   # < 2 → must be rejected
                }
            ],
            "connections": [],
        }

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=bad_llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-04-17",
        budget_seconds=300,
    )
    # All files processed successfully but no articles survived validation →
    # status is now "success-empty" (previously would have been "ok", which
    # masked the silent-empty regression fixed in vs-015/vs-016/vs-017).
    assert result.status == "success-empty"
    assert result.concepts_written == 0
    assert result.rejected_count >= 1


def test_run_synthesis_respects_budget(tmp_path: Path) -> None:
    """If budget_seconds=0, returns immediately without writing."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})

    def slow_llm(prompt: str, max_tokens: int = 2000) -> dict:
        raise AssertionError("should never be called")

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=slow_llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-04-17",
        budget_seconds=0,
    )
    assert result.status == "budget-exhausted"
    assert result.concepts_written == 0


# ─── Phase D — typed reasoning edges via db_conn ──────────────────────────


def _phase_d_llm_factory(relations: list[dict]):
    """Build an LLM caller that returns a single connection with `relations`.

    Fixture content is intentionally rich enough to pass the Tier-1.5
    depth gate (≥3-sentence definitions, ≥60-char prose quotes, ≥3-sentence
    synthesis, ≥2 substantive implications). The point of the Phase-D
    tests is edge-write semantics; the article content must still survive
    the production gate so the tests exercise the real path.
    """

    rich_quote_a = (
        "Concept Alpha emerges when two independent subsystems both depend on the same "
        "invariant without either subsystem declaring the dependency in source."
    )
    rich_quote_b = (
        "Concept Beta surfaces the consequence of Alpha — a coupling that is only "
        "visible when one of the two subsystems silently changes state at runtime."
    )
    rich_quote_g = (
        "Concept Gamma is the structural fix: a third surface that declares the "
        "shared invariant explicitly so neither original subsystem can drift."
    )

    def _call(prompt: str, max_tokens: int = 2000) -> dict:
        return {
            "concepts": [
                {
                    "title": "Concept Alpha",
                    "definition": (
                        "Concept Alpha names a class of failure where two independent "
                        "subsystems share an invariant that is not declared in either "
                        "subsystem's source. The shared invariant becomes load-bearing "
                        "exactly when a third party changes runtime conditions, and "
                        "neither subsystem reports the change because neither owns the "
                        "invariant. The defect surfaces as silent drift rather than a "
                        "crash."
                    ),
                    "context": (
                        "Recurs across the agent fleet whenever two scheduled jobs both "
                        "depend on the MBP being awake at 02:30."
                    ),
                    "evidence": [rich_quote_a, rich_quote_b],
                    "examples": ["vault_synthesizer + knowledge_lint both gate on MBP awake-at-02:30"],
                    "related": ["Concept Beta", "Concept Gamma"],
                },
                {
                    "title": "Concept Beta",
                    "definition": (
                        "Concept Beta is the observable consequence of Concept Alpha — a "
                        "drift that appears in one subsystem's output without either "
                        "subsystem reporting an error. The drift is visible only when an "
                        "operator notices the downstream artifact looks stale, which is "
                        "always after the producer has finished and exited cleanly. "
                        "Detection therefore lags causation by at least one cycle."
                    ),
                    "context": "The lag is the whole reason Tier-1.5 surfaces rejected_reasons.",
                    "evidence": [rich_quote_b, rich_quote_g],
                    "examples": ["meta-agent reports daily-driver error 10 min before daily-driver fires"],
                    "related": ["Concept Alpha", "Concept Gamma"],
                },
            ],
            "connections": [
                {
                    "title": "Alpha-Beta-Gamma Triangle",
                    "synthesis": (
                        "Alpha names the latent coupling, Beta is its observable drift, "
                        "and Gamma is the structural fix that declares the shared "
                        "invariant explicitly. The triangle matters because most "
                        "shop-floor debuggers stop at Beta — they treat the symptom as "
                        "the bug and patch in the affected subsystem. The actual fix "
                        "lives one level up, at the surface that declares the invariant."
                    ),
                    "concepts": ["Concept Alpha", "Concept Beta", "Concept Gamma"],
                    "evidence": {
                        "Concept Alpha": [rich_quote_a],
                        "Concept Beta": [rich_quote_b],
                        "Concept Gamma": [rich_quote_g],
                    },
                    "implications": [
                        "Bug triage that stops at the symptom subsystem will miss latent invariants and ship coupling-tighter fixes that fail again.",
                        "Every shared invariant deserves an explicit declaration surface owned by neither of the original subsystems involved.",
                    ],
                    "relations": relations,
                }
            ],
        }

    return _call


def test_run_synthesis_writes_edges_when_db_conn_provided(tmp_path: Path) -> None:
    """Phase D — mock LLM emits a `relations` payload; run_synthesis should
    INSERT typed edges into concept_edges. Pure unit-test path per the
    chosen empty-vault verification approach (CHANGELOG v3.20.0)."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})
    db_conn = init_db(tmp_path / "test.db")

    llm = _phase_d_llm_factory([
        {"from": "Concept Alpha", "to": "Concept Beta", "relation": "contradicts",
         "confidence": 0.9},
        {"from": "Concept Beta", "to": "Concept Gamma", "relation": "supports"},
    ])

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-05-01",
        budget_seconds=300,
        db_conn=db_conn,
    )

    assert result.edges_written == 2
    assert result.edges_rejected == 0
    rows = db_conn.execute(
        "SELECT from_slug, to_slug, relation FROM concept_edges "
        "ORDER BY from_slug, to_slug"
    ).fetchall()
    assert ("concept-alpha", "concept-beta", "contradicts") in rows
    assert ("concept-beta", "concept-gamma", "supports") in rows
    db_conn.close()


def test_run_synthesis_drops_invalid_relations_but_writes_article(tmp_path: Path) -> None:
    """Phase D watchpoint — invalid relation values must NOT abort the run.
    Article still writes; bad edge is logged + counted as rejected."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})
    db_conn = init_db(tmp_path / "test.db")

    llm = _phase_d_llm_factory([
        {"from": "Concept Alpha", "to": "Concept Beta", "relation": "not-a-real-relation"},
        {"from": "Concept Alpha", "to": "Concept Gamma", "relation": "contradicts"},
    ])

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-05-01",
        budget_seconds=300,
        db_conn=db_conn,
    )

    # Article still wrote.
    assert result.connections_written == 1
    # One bad relation rejected, one good relation written.
    assert result.edges_written == 1
    assert result.edges_rejected == 1
    rows = db_conn.execute("SELECT relation FROM concept_edges").fetchall()
    assert rows == [("contradicts",)]
    db_conn.close()


def test_run_synthesis_db_conn_none_skips_edges_silently(tmp_path: Path) -> None:
    """Phase D — passing db_conn=None (pure unit-test path / fresh-vault
    path before vault_indexer ran) MUST NOT crash and MUST still write
    articles. Edge counts stay at 0."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})

    llm = _phase_d_llm_factory([
        {"from": "Concept Alpha", "to": "Concept Beta", "relation": "contradicts"},
    ])

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-05-01",
        budget_seconds=300,
        db_conn=None,
    )

    assert result.connections_written == 1
    assert result.edges_written == 0
    assert result.edges_rejected == 0


def test_run_synthesis_sets_run_id(tmp_path: Path) -> None:
    """run_id is populated at synthesis start so synth-manifest + edge rows
    share the same source_synth_run anchor."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})
    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=lambda p, max_tokens=2000: {"concepts": [], "connections": []},
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-05-01",
        budget_seconds=300,
    )
    # ISO 8601 with seconds precision — contains 'T' and at least one ':'.
    assert "T" in result.run_id
    assert result.run_id.count(":") >= 2


def test_default_retriever_factory_accepts_include_embeddings_kwarg() -> None:
    """Regression for the 2026-05-17 Tier-2 routing bug.

    The v3.37.0 factory shim only accepted ``(query, top_k)``. The synthesizer's
    new ``retriever(query, k, include_embeddings=True)`` call therefore raised
    ``TypeError``; the silent fallback handler re-invoked positional-only and
    the cluster path never fired — manifest reported ``clusters_sampled=0``.
    Pinning the signature here so the seam can't regress.
    """
    import inspect

    from agents.vault_synthesizer import _default_retriever_factory

    retriever = _default_retriever_factory(Path("/nonexistent"))
    sig = inspect.signature(retriever)
    assert "include_embeddings" in sig.parameters
    param = sig.parameters["include_embeddings"]
    assert param.default is False
    assert param.kind == inspect.Parameter.KEYWORD_ONLY


def test_default_retriever_factory_forwards_include_embeddings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The factory shim must thread ``include_embeddings`` through to
    ``vault_indexer.search`` so Tier-2 actually receives embeddings.
    """
    from agents import vault_indexer as vi
    from agents.vault_synthesizer import _default_retriever_factory

    db_path = tmp_path / ".vault-index.db"
    db_path.touch()
    monkeypatch.setattr(vi, "get_db_path", lambda root: db_path)

    captured: dict[str, object] = {}

    async def fake_search(
        query: str,
        _db: Path,
        top_k: int = 5,
        *,
        include_embeddings: bool = False,
    ) -> list[dict[str, object]]:
        captured["query"] = query
        captured["top_k"] = top_k
        captured["include_embeddings"] = include_embeddings
        return [{"file_path": "f.md", "chunk_text": "x", "similarity": 0.9}]

    monkeypatch.setattr(vi, "search", fake_search)

    retriever = _default_retriever_factory(tmp_path)

    # Kwarg path — Tier-2 reachable.
    retriever("q", 50, include_embeddings=True)
    assert captured == {"query": "q", "top_k": 50, "include_embeddings": True}

    # Legacy positional path — backward compat preserved.
    retriever("q2", 5)
    assert captured["include_embeddings"] is False


# ─── Tier 1.5 — insight-depth gate (2026-05-20) ─────────────────────────────
#
# Pre-Tier-1.5 the validator only checked wikilink count + the forbidden
# "Evidence pending" string. That let median-quality output through —
# CLI-snippet evidence, restated-prompt definitions, two-sentence stub
# articles. `evaluate_article_depth` is the new semantic gate. Legacy
# `validate_article_body` stays unchanged for backward compatibility; the
# production path in `run_synthesis` now calls both.


def _concept_body(
    *,
    definition: str = (
        "Cross-domain bridging emerges when the same operational pattern "
        "surfaces in two unrelated PARA folders for the same underlying "
        "reason. The bridge is not coincidence; it is evidence that a "
        "deeper invariant governs both surfaces. Naming the invariant is "
        "what makes the bridge useful."
    ),
    context: str = (
        "Sean's vault is structured to make these bridges discoverable. "
        "The synthesizer's job is to surface them before he notices manually."
    ),
    quotes: list[str] | None = None,
    examples: list[str] | None = None,
    related: list[str] | None = None,
) -> str:
    from agents.vault_synthesizer import format_concept_article

    if quotes is None:
        quotes = [
            "The synthesizer surfaces non-obvious patterns that connect creative "
            "studio workflows with job-hunt portfolio strategy through shared "
            "automation primitives.",
            "Every connection that spans different PARA folders represents a "
            "structural insight rather than a within-cluster restatement of the "
            "same idea.",
        ]
    if examples is None:
        examples = [
            "Daily-driver morning brief uses the same pattern as the Substack drafter weekly run.",
            "Both are scheduled producers that consume vault state and emit one artifact per fire.",
        ]
    if related is None:
        related = ["Autonomous Agent Fleets", "Vault as SSoT"]

    return format_concept_article(
        title="Cross-Domain Bridging",
        definition=definition,
        context=context,
        examples=examples,
        related=related,
        sources=["20_projects/example.md"],
        evidence=quotes,
        today="2026-05-20",
    )


def _connection_body(
    *,
    synthesis: str = (
        "Three independent automation surfaces all gate on whether the MBP "
        "is awake at 02:30 AM. The shared dependency is invisible in each "
        "agent's source. It emerges sharply when a travel day knocks the "
        "laptop off the LAN and all three skip in the same window."
    ),
    quotes_by_concept: dict[str, list[str]] | None = None,
    implications: list[str] | None = None,
    concepts: list[str] | None = None,
) -> str:
    from agents.vault_synthesizer import format_connection_article

    if concepts is None:
        concepts = ["Vault Synthesizer", "Knowledge Lint", "Substack Drafter"]
    if quotes_by_concept is None:
        quotes_by_concept = {
            c: [
                f"{c} routes vault-synthesis tasks to Qwen3-14B on the MBP via "
                f"HybridRouter, which raises WOLUnavailable when the laptop is "
                f"asleep and the fleet falls back to a no-op state."
            ]
            for c in concepts
        }
    if implications is None:
        implications = [
            "Any travel day longer than 36 hours will leave a visible synthesis gap unless cloud fallback is wired in.",
            "The MBP-asleep dependency should be promoted to a first-class config knob with explicit per-agent fallback rules.",
        ]

    return format_connection_article(
        title="MBP-Wake Dependency Across Producers",
        synthesis=synthesis,
        concepts=concepts,
        implications=implications,
        evidence=quotes_by_concept,
        today="2026-05-20",
    )


# --- depth gate: concept articles --------------------------------------------


def test_evaluate_concept_depth_accepts_real_concept() -> None:
    from agents.vault_synthesizer import evaluate_article_depth

    passes, reason = evaluate_article_depth(_concept_body())
    assert passes is True, f"unexpected reject: {reason}"
    assert reason == ""


def test_evaluate_concept_depth_rejects_thin_definition() -> None:
    """A single-sentence definition is a restatement, not a definition."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _concept_body(definition="It is a collection of automated processes.")
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "thin-definition"


def test_evaluate_concept_depth_rejects_restatement_phrases() -> None:
    """LLM-tell phrases like "a collection of X designed to Y" mean the LLM
    restated the prompt rather than naming a mechanism."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _concept_body(
        definition=(
            "A collection of automated processes designed to support Sean's "
            "job-hunting efforts, including status updates and application "
            "tracking across multiple pipeline stages. These routines "
            "streamline his workflow by ensuring consistency and efficiency "
            "across the application pipeline at every step. The system "
            "ensures that nothing falls through the cracks."
        )
    )
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "restatement-definition"


def test_evaluate_concept_depth_rejects_code_only_evidence() -> None:
    """Evidence that is purely CLI commands is not evidence — it's a recipe."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _concept_body(
        quotes=[
            "cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/update_status.py",
            "PYTHONPATH=. .venv/bin/python3 scripts/update_status.py <db_id> applied --status applied --note 'auto'",
        ]
    )
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "code-only-evidence"


def test_evaluate_concept_depth_rejects_short_quotes() -> None:
    """A quote shorter than 60 chars is a fragment, not an argument."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _concept_body(quotes=["Short claim.", "Another fragment is short."])
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "thin-evidence"


def test_evaluate_concept_depth_rejects_when_examples_duplicate_evidence() -> None:
    """If Examples section is the same text as Evidence, the LLM is padding."""
    from agents.vault_synthesizer import evaluate_article_depth

    quotes = [
        "The synthesizer surfaces non-obvious patterns that connect creative "
        "studio workflows with job-hunt portfolio strategy through shared "
        "automation primitives.",
        "Every connection that spans different PARA folders represents a "
        "structural insight rather than a within-cluster restatement.",
    ]
    body = _concept_body(quotes=quotes, examples=quotes)
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "duplicate-examples"


# --- depth gate: connection articles -----------------------------------------


def test_evaluate_connection_depth_accepts_real_connection() -> None:
    from agents.vault_synthesizer import evaluate_article_depth

    passes, reason = evaluate_article_depth(_connection_body())
    assert passes is True, f"unexpected reject: {reason}"
    assert reason == ""


def test_evaluate_connection_depth_rejects_thin_synthesis() -> None:
    """A one-sentence synthesis describes; it doesn't name the tension."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _connection_body(
        synthesis="Three producers share an MBP dependency."
    )
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "thin-synthesis"


def test_evaluate_connection_depth_rejects_thin_threads() -> None:
    """Per-concept threads with no substantive quote → article is shallow."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _connection_body(
        quotes_by_concept={
            "Vault Synthesizer": ["short"],
            "Knowledge Lint": ["x"],
            "Substack Drafter": ["y"],
        }
    )
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "thin-threads"


def test_evaluate_connection_depth_rejects_thin_implications() -> None:
    """Casual one-liner implications fail the gate."""
    from agents.vault_synthesizer import evaluate_article_depth

    body = _connection_body(implications=["it matters.", "consider this."])
    passes, reason = evaluate_article_depth(body)
    assert passes is False
    assert reason == "thin-implications"


# --- integration: run_synthesis records rejection reasons --------------------


def test_run_synthesis_records_rejected_reasons_for_thin_concepts(tmp_path: Path) -> None:
    """A thin-definition concept must be rejected and counted with a reason
    string — so the synth-manifest carries operator-grade signal about WHY
    output volume is low on any given night."""
    vault = _make_vault(tmp_path, {"x.md": "seed text long enough to be readable here"})

    def shallow_llm(prompt: str, max_tokens: int = 2000) -> dict:
        return {
            "concepts": [
                {
                    "title": "Automation Routines",
                    # one-sentence definition triggers thin-definition rejection
                    "definition": "It is a process for tracking applications.",
                    "context": "context",
                    "examples": ["cd foo", "python bar.py"],
                    "evidence": [
                        "cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk",
                        "PYTHONPATH=. .venv/bin/python3 scripts/update_status.py",
                    ],
                    "related": ["Daily Driver Agent", "Agent Health Monitoring"],
                }
            ],
            "connections": [],
        }

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=shallow_llm,
        retriever=lambda q, top_k=5: [{"file_path": "a.md", "chunk_text": "seed alpha", "similarity": 0.9}, {"file_path": "b.md", "chunk_text": "seed beta", "similarity": 0.8}],
        now_iso="2026-05-20",
        budget_seconds=300,
    )

    assert result.concepts_written == 0
    assert result.rejected_count >= 1
    # rejected_reasons is the new field — must contain at least one of the
    # depth-gate reason codes so the manifest can attribute failures.
    assert result.rejected_reasons, "expected rejected_reasons to be populated"
    assert any(
        k in {"thin-definition", "restatement-definition", "code-only-evidence", "thin-evidence"}
        for k in result.rejected_reasons
    )


def test_synth_manifest_persists_rejected_reasons_and_skipped(tmp_path: Path) -> None:
    """write_synth_manifest must serialize the new Tier-1.5 fields."""
    from agents.vault_synthesizer import write_synth_manifest

    result = SynthesisResult(status="ok")
    result.rejected_reasons = {"thin-definition": 2, "code-only-evidence": 1}
    result.skipped_thin_source = 4
    result.run_id = "2026-05-20T02:30:00"

    path = write_synth_manifest(vault_root=tmp_path, result=result, today="2026-05-20")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["rejected_reasons"] == {"thin-definition": 2, "code-only-evidence": 1}
    assert payload["skipped_thin_source"] == 4


def test_run_synthesis_skips_thin_source_files(tmp_path: Path) -> None:
    """When cluster_and_sample returns <2 chunks (thin source), the file is
    skipped entirely — no LLM call, no shallow output. Counted in
    skipped_thin_source so the manifest surfaces the signal."""
    vault = _make_vault(tmp_path, {"x.md": "seed"})

    llm_called = {"n": 0}

    def llm(prompt: str, max_tokens: int = 2000) -> dict:
        llm_called["n"] += 1
        return {"concepts": [], "connections": []}

    # Retriever returns just one chunk → below the min-cluster threshold for
    # Tier-1.5's skip path.
    def thin_retriever(query: str, top_k: int = 5, *, include_embeddings: bool = False) -> list[dict]:
        chunk = {"file_path": "y.md", "chunk_text": "tiny", "similarity": 0.9}
        if include_embeddings:
            chunk["embedding"] = [0.0] * 8
        return [chunk]

    result = run_synthesis(
        vault_root=vault,
        changed_files=[vault / "x.md"],
        llm_caller=llm,
        retriever=thin_retriever,
        now_iso="2026-05-20",
        budget_seconds=300,
    )

    assert result.skipped_thin_source >= 1
    assert llm_called["n"] == 0, "LLM must not be called when source is thin"
