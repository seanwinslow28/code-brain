"""Tests for agents.vault_synthesizer — D.2.b concept + connection articles."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

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
    assert result.status in {"ok", "partial"}
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
