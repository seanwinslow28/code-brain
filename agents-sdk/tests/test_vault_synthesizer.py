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
                    "definition": "RIFE controls frame interpolation.",
                    "context": "Phase 5 tuning.",
                    "examples": ["temporal_smoothing=0.8 wins by 8%"],
                    "related": ["Wan 2.2 Keyframes", "Pixel Quantizer"],
                }
            ],
            "connections": [
                {
                    "title": "Keyframe Sparsity Tradeoff",
                    "synthesis": "Sparse keyframes = drift; dense = slow.",
                    "concepts": [
                        "RIFE Interpolation Hyperparameters",
                        "Wan 2.2 Keyframes",
                        "Pixel Quantizer",
                    ],
                    "implications": ["Tune per complexity."],
                }
            ],
        }

    changed = [
        vault / "05_projects/phase5-autoresearch.md",
        vault / "05_projects/pixel-quantizer.md",
    ]

    def fake_search(query: str, top_k: int = 5) -> list[dict]:
        return [
            {"file_path": "05_projects/wan-notes.md", "chunk_text": "Wan 2.2", "similarity": 0.9}
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
        retriever=lambda q, top_k=5: [],
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
        retriever=lambda q, top_k=5: [],
        now_iso="2026-04-17",
        budget_seconds=0,
    )
    assert result.status == "budget-exhausted"
    assert result.concepts_written == 0


# ─── Phase D — typed reasoning edges via db_conn ──────────────────────────


def _phase_d_llm_factory(relations: list[dict]):
    """Build an LLM caller that returns a single connection with `relations`."""

    def _call(prompt: str, max_tokens: int = 2000) -> dict:
        return {
            "concepts": [
                {
                    "title": "Concept Alpha",
                    "definition": "Alpha is a thing.",
                    "context": "test",
                    "examples": ["x"],
                    "related": ["Concept Beta", "Concept Gamma"],
                },
                {
                    "title": "Concept Beta",
                    "definition": "Beta is a thing.",
                    "context": "test",
                    "examples": ["y"],
                    "related": ["Concept Alpha", "Concept Gamma"],
                },
            ],
            "connections": [
                {
                    "title": "Alpha-Beta-Gamma Triangle",
                    "synthesis": "Three things that interact.",
                    "concepts": ["Concept Alpha", "Concept Beta", "Concept Gamma"],
                    "implications": ["something"],
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
        retriever=lambda q, top_k=5: [],
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
        retriever=lambda q, top_k=5: [],
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
        retriever=lambda q, top_k=5: [],
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
        retriever=lambda q, top_k=5: [],
        now_iso="2026-05-01",
        budget_seconds=300,
    )
    # ISO 8601 with seconds precision — contains 'T' and at least one ':'.
    assert "T" in result.run_id
    assert result.run_id.count(":") >= 2
