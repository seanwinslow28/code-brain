"""Cluster-and-sample retrieval helpers — Tier 2 retrofit (2026-05-16).

The synthesizer's v1 retrieval was top-K cosine on `primary_text[:2000]`,
which produced cluster-bias where 6-7 of 9 retrieved chunks always came
from the densest concept region (agent-health / automation-reliability).
The Tier-1 prompt-level cross-domain hint helped the LLM compose better
synthesis *given* candidates, but didn't change *which* candidates the
retriever returns. Tier 2 attacks the bias structurally: retrieve a
larger pool (top-50), cluster it with HDBSCAN (`min_cluster_size=3`),
and sample 2-3 chunks per cluster.

Pattern: TopClustRAG (SIGIR 2025, arxiv.org/html/2506.15246v1).

Plan + intent spec at:
  vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
    job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md

Pure functions — no I/O, no globals — so tests can stand them up cheaply.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class DiversifiedPool:
    """Outcome of a cluster-and-sample call.

    Attributes:
        indices: Selected indices into the input embeddings list,
            sorted ascending so the caller's chunk list stays in
            cosine-rank order.
        clusters_found: Number of distinct real (non-noise) HDBSCAN
            clusters in the pool. ``0`` when the fall-back path
            (no clustering) was taken — also surfaces as the
            ``clusters_sampled`` synth-manifest field for telemetry.
        fell_back: ``True`` when ``cluster_and_sample`` returned the
            top-rank slice instead of clustering. Reasons: pool too
            small, hdbscan unavailable, <2 real clusters detected,
            or HDBSCAN raised on degenerate input.
    """
    indices: list[int] = field(default_factory=list)
    clusters_found: int = 0
    fell_back: bool = True


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_HEADING_RE = re.compile(r"^(#{1,2})\s+(.+?)\s*$", re.MULTILINE)
_FM_TYPE_RE = re.compile(r"^type:\s*(.+?)\s*$", re.MULTILINE)
_FM_TAGS_INLINE_RE = re.compile(r"^tags:\s*\[(.+?)\]", re.MULTILINE)
_FM_TAGS_BLOCK_RE = re.compile(r"^tags:\s*\n((?:\s+-\s+.+\n?)+)", re.MULTILINE)
_FM_TAGS_BLOCK_ITEM_RE = re.compile(r"-\s+(\S.*?)\s*$", re.MULTILINE)


def build_embedding_query(primary_text: str, *, max_chars: int = 1500) -> str:
    """Build a high-signal embedding query from a vault markdown file.

    Concatenates, in order:
      - frontmatter ``type``
      - frontmatter ``tags`` (inline ``[a, b]`` OR block ``-`` list)
      - up to 6 H1/H2 headings (in document order)
      - first non-empty paragraph after the frontmatter (truncated)

    Falls back to ``primary_text[:max_chars]`` when extraction yields
    nothing useful (no frontmatter, no headings, no paragraphs) — keeps
    the v1 behaviour for plain text and prevents an empty query from
    reaching the embedder.

    Args:
        primary_text: Raw markdown contents of the file driving this
            synthesis pass.
        max_chars: Hard cap on the returned query string. The embedder
            (nomic-embed-text) silently truncates beyond ~2048 tokens;
            1500 chars leaves headroom while keeping the query focused.

    Returns:
        The assembled query string, never longer than ``max_chars``.
    """
    if not primary_text:
        return ""

    parts: list[str] = []
    body = primary_text

    fm_match = _FRONTMATTER_RE.match(primary_text)
    if fm_match:
        fm = fm_match.group(1)
        type_m = _FM_TYPE_RE.search(fm)
        if type_m:
            parts.append(f"type: {type_m.group(1)}")
        tags_inline = _FM_TAGS_INLINE_RE.search(fm)
        if tags_inline:
            parts.append(f"tags: {tags_inline.group(1)}")
        else:
            tags_block = _FM_TAGS_BLOCK_RE.search(fm)
            if tags_block:
                items = _FM_TAGS_BLOCK_ITEM_RE.findall(tags_block.group(1))
                if items:
                    parts.append(f"tags: {', '.join(items)}")
        body = primary_text[fm_match.end():]

    headings = _HEADING_RE.findall(body)
    for _level, text in headings[:6]:
        parts.append(text.strip())

    for raw in body.split("\n\n"):
        p = raw.strip()
        if not p or p.startswith("#") or p.startswith("---") or p.startswith("- "):
            continue
        parts.append(p[:600])
        break

    if not parts:
        return primary_text[:max_chars]

    return "\n".join(parts)[:max_chars]


def cluster_and_sample(
    embeddings: Sequence[Sequence[float]],
    *,
    k_per_cluster: int = 2,
    min_cluster_size: int = 3,
    max_noise: int = 3,
    max_total: int = 15,
) -> DiversifiedPool:
    """Cluster embeddings and return a diversified subset of indices.

    The input is assumed pre-ranked by cosine similarity (highest first),
    so within-cluster sampling preserves that ranking — the top-rank
    point of each cluster is taken first.

    HDBSCAN finds variable-density clusters and labels low-density points
    as noise (label ``-1``). Real clusters (label ``>= 0``) each contribute
    ``k_per_cluster`` points. Noise points are included up to ``max_noise``
    because they often represent novel / non-clusterable content the
    synthesizer specifically wants to surface.

    Edge cases:
      - Empty input → empty ``DiversifiedPool`` with ``fell_back=True``.
      - ``n <= min_cluster_size`` → return all indices (clustering is
        meaningless on a tiny pool).
      - HDBSCAN finds fewer than 2 real clusters → fall back to the
        top-``max_total`` by input rank. The prompt-level cross-domain
        hint still steers the LLM; no value in pretending we diversified.
      - HDBSCAN raises on degenerate input (all-identical vectors, NaNs)
        → same fall-back behaviour, surfaced via a single exception
        guard so the synthesizer never aborts a run because of an
        unusual chunk set.

    Args:
        embeddings: 2-D sequence; ``embeddings[i]`` is the i-th vector.
        k_per_cluster: Max points to take per HDBSCAN cluster.
        min_cluster_size: HDBSCAN's ``min_cluster_size`` parameter.
            Clusters smaller than this collapse to noise.
        max_noise: Cap on noise (label ``-1``) points returned.
        max_total: Hard cap on the returned index count. Protects the
            prompt budget when the pool fragments into many small clusters.

    Returns:
        ``DiversifiedPool`` whose ``indices`` are deduplicated and sorted
        ascending. ``clusters_found`` is the count of real (non-noise)
        clusters HDBSCAN identified, or ``0`` on the fall-back path.
        ``fell_back`` is ``True`` whenever clustering was skipped or
        produced fewer than 2 real clusters.
    """
    n = len(embeddings)
    if n == 0:
        return DiversifiedPool(indices=[], clusters_found=0, fell_back=True)
    if n <= min_cluster_size:
        return DiversifiedPool(
            indices=list(range(min(n, max_total))),
            clusters_found=0,
            fell_back=True,
        )

    try:
        import hdbscan  # local import — avoid cost when caller doesn't cluster
    except ImportError:
        return DiversifiedPool(
            indices=list(range(min(n, max_total))),
            clusters_found=0,
            fell_back=True,
        )

    try:
        arr = np.asarray(embeddings, dtype=np.float64)
        if arr.ndim != 2 or arr.shape[0] != n:
            return DiversifiedPool(
                indices=list(range(min(n, max_total))),
                clusters_found=0,
                fell_back=True,
            )
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            metric="euclidean",
        )
        labels = clusterer.fit_predict(arr)
    except Exception:
        return DiversifiedPool(
            indices=list(range(min(n, max_total))),
            clusters_found=0,
            fell_back=True,
        )

    by_label: dict[int, list[int]] = defaultdict(list)
    for i, lab in enumerate(labels):
        by_label[int(lab)].append(i)

    real_clusters = sorted(lab for lab in by_label if lab >= 0)
    if len(real_clusters) < 2:
        return DiversifiedPool(
            indices=list(range(min(n, max_total))),
            clusters_found=len(real_clusters),
            fell_back=True,
        )

    selected: set[int] = set()
    for lab in real_clusters:
        selected.update(by_label[lab][:k_per_cluster])
    selected.update(by_label.get(-1, [])[:max_noise])

    return DiversifiedPool(
        indices=sorted(selected)[:max_total],
        clusters_found=len(real_clusters),
        fell_back=False,
    )


def count_real_clusters(labels: Iterable[int]) -> int:
    """Count distinct non-noise HDBSCAN labels.

    Exposed for the synthesizer's ``clusters_sampled`` manifest field.
    Noise is label ``-1`` and excluded.
    """
    return len({int(l) for l in labels if int(l) >= 0})
