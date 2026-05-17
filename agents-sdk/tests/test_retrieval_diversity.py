"""Tests for lib.retrieval_diversity — Tier 2 cluster-and-sample retrieval.

Companion to the Tier 2 retrofit in vault_synthesizer.py. The v1 retriever
biased toward the densest concept region of the vault (7/9 chunks pulled
from agent-health/fleet/automation). cluster_and_sample fixes this by
retrieving a larger pool, clustering with HDBSCAN, and sampling per
cluster so cross-domain content surfaces structurally.

Plan:
  vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
    job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
"""

from __future__ import annotations

import numpy as np

from lib.retrieval_diversity import (
    DiversifiedPool,
    build_embedding_query,
    cluster_and_sample,
    count_real_clusters,
)


# ─── cluster_and_sample ───────────────────────────────────────────────────


def test_cluster_and_sample_empty_input() -> None:
    result = cluster_and_sample([])
    assert isinstance(result, DiversifiedPool)
    assert result.indices == []
    assert result.clusters_found == 0
    assert result.fell_back is True


def test_cluster_and_sample_pool_below_min_cluster_size_returns_all() -> None:
    # n=2 ≤ default min_cluster_size=3 → clustering is meaningless,
    # so return everything in input order via the fall-back path.
    embeddings = [[1.0, 0.0], [0.0, 1.0]]
    result = cluster_and_sample(embeddings)
    assert result.indices == [0, 1]
    assert result.fell_back is True
    assert result.clusters_found == 0


def test_cluster_and_sample_three_obvious_clusters_returns_all_three() -> None:
    """Three well-separated clusters of 4 points each.

    With ``k_per_cluster=2``, expect a returned index set whose members
    span all three clusters (indices 0-3 = cluster A, 4-7 = B, 8-11 = C),
    ``clusters_found == 3``, and ``fell_back is False``.
    """
    rng = np.random.default_rng(0)
    centers = [
        [10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    embeddings: list[list[float]] = []
    for c in centers:
        for _ in range(4):
            embeddings.append((np.array(c) + rng.normal(0, 0.1, 8)).tolist())

    result = cluster_and_sample(embeddings, k_per_cluster=2, min_cluster_size=3)
    spans = {i // 4 for i in result.indices}
    assert spans == {0, 1, 2}, f"expected all 3 clusters represented, got {result.indices}"
    assert result.clusters_found == 3
    assert result.fell_back is False


def test_cluster_and_sample_caps_returned_count_at_max_total() -> None:
    rng = np.random.default_rng(1)
    embeddings: list[list[float]] = []
    # 10 well-separated clusters of 3 points each → without cap, 20 selected.
    for i in range(10):
        c = np.zeros(20)
        c[i] = 5.0
        for _ in range(3):
            embeddings.append((c + rng.normal(0, 0.05, 20)).tolist())

    result = cluster_and_sample(embeddings, k_per_cluster=2, max_total=8)
    assert len(result.indices) <= 8


def test_cluster_and_sample_returns_sorted_indices() -> None:
    """Returned indices preserve input (cosine-rank) order."""
    rng = np.random.default_rng(2)
    embeddings: list[list[float]] = []
    for _ in range(5):
        embeddings.append((np.array([10.0, 0.0]) + rng.normal(0, 0.1, 2)).tolist())
    for _ in range(5):
        embeddings.append((np.array([0.0, 10.0]) + rng.normal(0, 0.1, 2)).tolist())

    result = cluster_and_sample(embeddings, k_per_cluster=2, min_cluster_size=3)
    assert result.indices == sorted(result.indices)


def test_cluster_and_sample_within_cluster_takes_highest_rank_first() -> None:
    """When HDBSCAN forms one cluster from contiguous indices, the
    lowest-indexed (highest-rank) members are chosen.
    """
    rng = np.random.default_rng(3)
    embeddings: list[list[float]] = []
    # Cluster A — 5 tight points, indices 0-4
    for _ in range(5):
        embeddings.append((np.array([10.0, 0.0]) + rng.normal(0, 0.05, 2)).tolist())
    # Cluster B — 5 tight points, indices 5-9
    for _ in range(5):
        embeddings.append((np.array([0.0, 10.0]) + rng.normal(0, 0.05, 2)).tolist())

    result = cluster_and_sample(embeddings, k_per_cluster=2, min_cluster_size=3)
    cluster_a = [i for i in result.indices if i < 5]
    cluster_b = [i for i in result.indices if i >= 5]
    # Within each cluster, the chosen indices are the lowest available.
    assert cluster_a == sorted(cluster_a)
    assert cluster_b == sorted(cluster_b)
    # And they must be at the front of each contiguous block.
    assert cluster_a[0] == 0
    assert cluster_b[0] == 5


def test_cluster_and_sample_degenerate_identical_input_falls_back() -> None:
    """All-identical embeddings — HDBSCAN may complain; we must not raise."""
    embeddings = [[1.0, 0.0, 0.0]] * 20
    result = cluster_and_sample(embeddings, max_total=5)
    # Fall-back path returns top-max_total by input order.
    assert result.indices == [0, 1, 2, 3, 4]
    assert result.fell_back is True


# ─── build_embedding_query ───────────────────────────────────────────────


def test_build_embedding_query_extracts_frontmatter_and_headings() -> None:
    text = '''---
type: concept
tags: [agent-fleet, automation]
created: 2026-05-13
---

# Main Title

First paragraph that explains the concept in detail.

## Subheading

Subsection details.
'''
    query = build_embedding_query(text)
    assert "Main Title" in query
    assert "Subheading" in query
    assert "agent-fleet" in query
    assert "automation" in query
    assert "concept" in query  # type field


def test_build_embedding_query_extracts_block_style_tags() -> None:
    text = '''---
type: project
tags:
  - life-systems
  - finance
---

# Some Project

Body text.
'''
    query = build_embedding_query(text)
    assert "life-systems" in query
    assert "finance" in query
    assert "Some Project" in query


def test_build_embedding_query_no_structure_falls_back_to_raw_text() -> None:
    text = "just plain text without markdown structure"
    assert build_embedding_query(text) == text


def test_build_embedding_query_truncates_at_max_chars() -> None:
    text = "x" * 5000
    query = build_embedding_query(text, max_chars=200)
    assert len(query) == 200


def test_build_embedding_query_empty_input() -> None:
    assert build_embedding_query("") == ""


def test_build_embedding_query_skips_lists_for_first_paragraph() -> None:
    """The 'first paragraph' picker should not lock onto a bullet list."""
    text = '''---
type: concept
---

# Heading

- a bullet
- another bullet

This is the real paragraph we want to embed.
'''
    query = build_embedding_query(text)
    assert "real paragraph" in query


# ─── count_real_clusters ─────────────────────────────────────────────────


def test_count_real_clusters_excludes_noise() -> None:
    assert count_real_clusters([0, 0, 1, 1, -1, -1, 2]) == 3
    assert count_real_clusters([-1, -1, -1]) == 0
    assert count_real_clusters([]) == 0
