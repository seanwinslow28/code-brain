# E3 — Pain-Point Dedup + MMR Gap Ranking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse near-duplicate verified pain points before FRAME (honest evidence merge) and reuse the same lexical similarity signal to rank D4's whitespace gaps worst-first.

**Architecture:** One new $0/deterministic module `council/discovery/dedup.py` exposes a shared token-Jaccard `pain_similarity` (injectable) feeding two algorithms — `dedup_verified` (greedy bounded merge-to-canonical, bias-to-under-merge) and `rank_gaps` (MMR diversity selection). Wired into `pipeline.py` between verify and frame; `whitespace.py` wording updated to reflect that gaps are now ranked.

**Tech Stack:** Python 3.11+, stdlib only (`re`, `dataclasses`, `urllib.parse`), pytest, `uv`.

## Global Constraints

- **$0, no model call, deterministic** — lexical token Jaccard, stdlib only, no new dependencies.
- **Gate sacred** — dedup runs only on gate-survived `VerifiedPainPoint`s; merge unions only already-verified evidence and never fabricates a quote/URL or inflates corroboration (corroboration stays keyed on distinct **domains** in `scoring.py`).
- **Conservative dedup** — `SIM_THRESHOLD = 0.5` biased toward UNDER-merging; bounded merge-to-canonical (NO transitive closure).
- **`MMR_LAMBDA = 0.3`** (diversity-dominant, per research).
- **Injectable similarity** — both algorithms accept `similarity_fn` so embeddings can swap in later without touching the algorithm.
- **Vault**: write nothing under `vault/` from this branch; the research note is already created and left unstaged for Sean.
- **Tests**: `cd tools/llm-council && uv run pytest tests/ -q` (baseline **212 passed, 1 skipped**) + `python3 scripts/validate.py` (repo root). Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- All paths below are relative to repo root; pytest is run from `tools/llm-council/`.

---

### Task 1: Similarity core (`dedup.py` foundation)

**Files:**
- Create: `tools/llm-council/council/discovery/dedup.py`
- Test: `tools/llm-council/tests/discovery/test_dedup.py`

**Interfaces:**
- Consumes: `council.discovery.fusion.CandidatePainPoint`
- Produces: `normalize_tokens(text:str)->frozenset[str]`, `jaccard(a:frozenset,b:frozenset)->float`, `pain_similarity(a:str,b:str)->float`, `_point_text(point:CandidatePainPoint)->str`, constants `SIM_THRESHOLD=0.5`, `MMR_LAMBDA=0.3`, type alias `SimilarityFn`.

- [ ] **Step 1: Write the failing test**

```python
# tools/llm-council/tests/discovery/test_dedup.py
from council.discovery.fusion import CandidatePainPoint
from council.discovery.dedup import (
    normalize_tokens, jaccard, pain_similarity, _point_text,
    SIM_THRESHOLD, MMR_LAMBDA,
)


def test_normalize_tokens_lowercases_strips_punct_and_stopwords():
    toks = normalize_tokens("The Export FAILS, silently!")
    assert toks == frozenset({"export", "fails", "silently"})   # "the" dropped, punct stripped


def test_jaccard_basic_and_empty():
    assert jaccard(frozenset(), frozenset()) == 0.0             # two empty => non-duplicate
    assert jaccard(frozenset({"a"}), frozenset({"a"})) == 1.0
    assert jaccard(frozenset({"a", "b"}), frozenset({"b", "c"})) == 1 / 3


def test_pain_similarity_word_reorder_is_high():
    a = "exports fail silently on conflict"
    b = "on conflict, exports silently fail"
    assert pain_similarity(a, b) == 1.0                          # same content tokens, reordered


def test_pain_similarity_distinct_pains_low():
    a = "exports fail silently"
    b = "onboarding tutorial is confusing"
    assert pain_similarity(a, b) < SIM_THRESHOLD


def test_point_text_joins_title_and_summary():
    pt = CandidatePainPoint("Export loss", "notes vanish on conflict", [], [])
    assert _point_text(pt) == "Export loss. notes vanish on conflict"


def test_constants_are_conservative():
    assert SIM_THRESHOLD == 0.5
    assert MMR_LAMBDA == 0.3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: FAIL — `ModuleNotFoundError: council.discovery.dedup`.

- [ ] **Step 3: Write minimal implementation**

```python
# tools/llm-council/council/discovery/dedup.py
"""E3 — near-duplicate pain-point dedup (threshold merge-to-canonical) + MMR gap ranking.

A shared lexical similarity (token Jaccard, $0/deterministic) drives two algorithms:
  * dedup_verified — collapse near-duplicate gate-survived pain points. Conservative
                     (bias-to-UNDER-merge) and bounded merge-to-canonical: each non-canonical
                     attaches to at most one canonical, so there is NO transitive closure
                     (A=B,B=C =/=> A=C) — the documented over-merge trap.
  * rank_gaps      — MMR (Carbonell & Goldstein 1998) diversity selection over D4's whitespace
                     gaps: "worst-first" = most-distinct-from-what-the-run-surfaced, near-dups dropped.

Both take an injectable similarity_fn so a future nomic-embed-text path swaps in without touching
either algorithm. Honest merge: union URLs/quotes; corroboration stays keyed on distinct DOMAINS in
scoring.py so syndicated/same-domain sources can't double-count.

Spec: docs/superpowers/specs/2026-06-29-discovery-e3-mmr-dedup-design.md
Research: vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from council.discovery.fusion import CandidatePainPoint
from council.discovery.verify import VerifiedPainPoint

# --- tunable constants (conservative; research gave no short-text number — calibrated vs fixtures) ---
SIM_THRESHOLD = 0.5     # token-Jaccard >= this => "same pain"; biased toward UNDER-merging
MMR_LAMBDA = 0.3        # diversity-dominant gap ranking (research: 0.3-0.5 band for a diversity goal)

_STOPWORDS = frozenset(
    "a an and are as at be but by for from has have in into is it its of on or that the their "
    "this to was were will with your you our we they them then than i me my so if not no can "
    "cant do does dont how what when where which who why".split()
)
_WORD = re.compile(r"[a-z0-9]+")

SimilarityFn = Callable[[str, str], float]


def normalize_tokens(text: str) -> frozenset[str]:
    """Lowercase, extract alphanumeric word tokens, drop stopwords. Deterministic, no deps."""
    return frozenset(t for t in _WORD.findall((text or "").lower()) if t not in _STOPWORDS)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    union = a | b
    if not union:
        return 0.0                       # two empty texts => non-duplicate (under-merge bias)
    return len(a & b) / len(union)


def pain_similarity(a: str, b: str) -> float:
    """Default similarity_fn: token-Jaccard over the normalized tokens of two short texts."""
    return jaccard(normalize_tokens(a), normalize_tokens(b))


def _point_text(point: CandidatePainPoint) -> str:
    return f"{point.title}. {point.summary}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dedup.py tools/llm-council/tests/discovery/test_dedup.py
git commit -m "feat(discovery): E3 shared lexical similarity core (token Jaccard)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `dedup_verified` — bounded merge-to-canonical

**Files:**
- Modify: `tools/llm-council/council/discovery/dedup.py`
- Test: `tools/llm-council/tests/discovery/test_dedup.py`

**Interfaces:**
- Consumes: `pain_similarity`, `_point_text`, `SIM_THRESHOLD`, `council.discovery.verify.VerifiedPainPoint`, `council.discovery.fusion.CandidatePainPoint`
- Produces: `@dataclass(frozen=True) MergeRecord(canonical_title:str, merged_titles:list[str])`; `dedup_verified(verified:list[VerifiedPainPoint], *, threshold:float=SIM_THRESHOLD, similarity_fn:SimilarityFn=pain_similarity) -> tuple[list[VerifiedPainPoint], list[MergeRecord]]`

- [ ] **Step 1: Write the failing test**

```python
# append to tools/llm-council/tests/discovery/test_dedup.py
from council.discovery.verify import VerifiedPainPoint
from council.discovery.dedup import dedup_verified, MergeRecord


def _vpp(title, summary, *, urls, quotes=("q",), intensity=3, verified=True, supporting=None):
    pt = CandidatePainPoint(title, summary, list(quotes), list(urls), intensity=intensity)
    return VerifiedPainPoint(point=pt, verified=verified,
                             supporting_urls=list(supporting if supporting is not None else urls))


def test_dedup_merges_reordered_restatement_and_unions_evidence():
    a = _vpp("Exports fail silently", "exports silently fail on conflict",
             urls=["https://d1.com/a"], quotes=["exports fail silently"])
    b = _vpp("Silently failing exports", "on conflict exports fail silently",
             urls=["https://d2.com/b"], quotes=["silent export failure"])
    deduped, merges = dedup_verified([a, b])
    assert len(deduped) == 1
    merged = deduped[0]
    # union of supporting urls across both members (order-preserving, canonical first)
    assert set(merged.supporting_urls) == {"https://d1.com/a", "https://d2.com/b"}
    assert "exports fail silently" in merged.point.quotes and "silent export failure" in merged.point.quotes
    assert len(merges) == 1 and isinstance(merges[0], MergeRecord)
    assert merges[0].merged_titles                          # the absorbed title is recorded


def test_dedup_representative_is_strongest_evidence():
    weak = _vpp("Weak phrasing", "exports fail silently here",
                urls=["https://only.com/x"], intensity=5)            # 1 domain, high intensity
    strong = _vpp("Strong phrasing", "exports fail silently here",
                  urls=["https://a.com/x", "https://b.com/y"], intensity=3)   # 2 domains
    deduped, _ = dedup_verified([weak, strong])
    assert len(deduped) == 1
    assert deduped[0].point.title == "Strong phrasing"      # more distinct domains wins, not intensity


def test_dedup_does_not_merge_distinct_pains():
    a = _vpp("Export loss", "exports fail silently", urls=["https://a.com/x"])
    b = _vpp("Onboarding pain", "the onboarding tutorial confuses new users",
             urls=["https://b.com/y"])
    deduped, merges = dedup_verified([a, b])
    assert len(deduped) == 2 and merges == []


def test_dedup_bounded_no_transitive_collapse():
    # A~B and B~C by shared tokens, but A and C share almost nothing -> must NOT collapse to one.
    a = _vpp("alpha export sync", "alpha export sync", urls=["https://a.com/x"])
    b = _vpp("export sync billing", "export sync billing", urls=["https://b.com/y"])
    c = _vpp("billing invoice tax", "billing invoice tax", urls=["https://c.com/z"])
    deduped, _ = dedup_verified([a, b, c])
    assert len(deduped) >= 2                                 # A and C never merged via B


def test_dedup_passes_unverified_through_untouched():
    good = _vpp("Real", "exports fail silently", urls=["https://a.com/x"])
    bad = _vpp("Fake", "never said", urls=["https://f.com/x"], verified=False, supporting=[])
    deduped, _ = dedup_verified([good, bad])
    assert any(not v.verified for v in deduped)              # unverified preserved


def test_dedup_injectable_similarity_fn():
    a = _vpp("totally", "different one", urls=["https://a.com/x"])
    b = _vpp("words", "entirely other", urls=["https://b.com/y"])
    deduped, _ = dedup_verified([a, b], similarity_fn=lambda x, y: 1.0)   # force everything equal
    assert len(deduped) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: FAIL — `ImportError: cannot import name 'dedup_verified'`.

- [ ] **Step 3: Write minimal implementation**

Append to `tools/llm-council/council/discovery/dedup.py`:

```python
@dataclass(frozen=True)
class MergeRecord:
    canonical_title: str
    merged_titles: list[str]            # titles absorbed into the canonical (excludes the canonical)


def _distinct_domains(urls: list[str]) -> int:
    return len({urlparse(u).netloc.lower() for u in urls if u})


def _dedup_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def _strength_key(v: VerifiedPainPoint, idx: int) -> tuple:
    # Strongest first: most distinct domains, then intensity, then quote count, then earliest index.
    return (-_distinct_domains(v.supporting_urls), -int(v.point.intensity or 0),
            -len(v.point.quotes), idx)


def _merge_cluster(members: list[VerifiedPainPoint]) -> VerifiedPainPoint:
    seed = members[0]                                   # strongest (members built seed-first)
    sp = seed.point
    merged = CandidatePainPoint(
        title=sp.title, summary=sp.summary,
        quotes=_dedup_keep_order([q for m in members for q in m.point.quotes]),
        urls=_dedup_keep_order([u for m in members for u in m.point.urls]),
        consensus=sp.consensus, intensity=sp.intensity, recency=sp.recency, segment=sp.segment,
    )
    supporting = _dedup_keep_order([u for m in members for u in m.supporting_urls])
    return VerifiedPainPoint(point=merged, verified=True, supporting_urls=supporting)


def dedup_verified(
    verified: list[VerifiedPainPoint],
    *,
    threshold: float = SIM_THRESHOLD,
    similarity_fn: SimilarityFn = pain_similarity,
) -> tuple[list[VerifiedPainPoint], list[MergeRecord]]:
    """Collapse near-duplicate gate-survived pain points. Bounded merge-to-canonical: each point
    joins at most one (best-matching) canonical above `threshold`, else seeds a new canonical — no
    transitive closure. Unverified points pass through untouched."""
    true_pts = [(i, v) for i, v in enumerate(verified) if v.verified]
    passthrough = [v for v in verified if not v.verified]
    ordered = sorted(true_pts, key=lambda iv: _strength_key(iv[1], iv[0]))

    clusters: list[list[VerifiedPainPoint]] = []        # each cluster is [seed, members...]
    for _idx, v in ordered:
        vtext = _point_text(v.point)
        best_c, best_sim = None, 0.0
        for c in clusters:
            sim = similarity_fn(vtext, _point_text(c[0].point))
            if sim > best_sim:
                best_sim, best_c = sim, c
        if best_c is not None and best_sim >= threshold:
            best_c.append(v)
        else:
            clusters.append([v])

    deduped: list[VerifiedPainPoint] = []
    merges: list[MergeRecord] = []
    for members in clusters:
        if len(members) == 1:
            deduped.append(members[0])
            continue
        deduped.append(_merge_cluster(members))
        merges.append(MergeRecord(
            canonical_title=members[0].point.title,
            merged_titles=[m.point.title for m in members[1:]],
        ))
    return deduped + passthrough, merges
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: PASS (12 tests total).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dedup.py tools/llm-council/tests/discovery/test_dedup.py
git commit -m "feat(discovery): E3 dedup_verified — bounded merge-to-canonical, honest evidence union

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `rank_gaps` — MMR diversity selection

**Files:**
- Modify: `tools/llm-council/council/discovery/dedup.py`
- Test: `tools/llm-council/tests/discovery/test_dedup.py`

**Interfaces:**
- Consumes: `pain_similarity`, `SIM_THRESHOLD`, `MMR_LAMBDA`
- Produces: `rank_gaps(gaps:list[str], reference_texts:list[str], *, lambda_:float=MMR_LAMBDA, threshold:float=SIM_THRESHOLD, similarity_fn:SimilarityFn=pain_similarity) -> list[str]`

- [ ] **Step 1: Write the failing test**

```python
# append to tools/llm-council/tests/discovery/test_dedup.py
from council.discovery.dedup import rank_gaps


def test_rank_gaps_worst_first_most_distinct_from_found():
    found = ["Export loss. notes vanish on conflict"]
    gaps = [
        "nobody covers export conflict recovery",   # close to what we found -> ranked later
        "pricing transparency is unaddressed",      # orthogonal -> ranked first (biggest blind spot)
    ]
    ranked = rank_gaps(gaps, found)
    assert ranked[0] == "pricing transparency is unaddressed"


def test_rank_gaps_drops_near_duplicate_gaps():
    gaps = [
        "pricing transparency is unaddressed",
        "transparency of pricing is not addressed",   # near-dup of the first
        "mobile offline mode is missing",
    ]
    ranked = rank_gaps(gaps, [])
    assert len(ranked) == 2
    assert "mobile offline mode is missing" in ranked


def test_rank_gaps_empty_inputs():
    assert rank_gaps([], []) == []
    assert rank_gaps(["  ", ""], []) == []          # blank gaps dropped


def test_rank_gaps_no_reference_keeps_all_distinct():
    gaps = ["alpha topic one", "beta subject two", "gamma matter three"]
    ranked = rank_gaps(gaps, [])
    assert set(ranked) == set(gaps)                 # all distinct -> all kept
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: FAIL — `ImportError: cannot import name 'rank_gaps'`.

- [ ] **Step 3: Write minimal implementation**

Append to `tools/llm-council/council/discovery/dedup.py`:

```python
def rank_gaps(
    gaps: list[str],
    reference_texts: list[str],
    *,
    lambda_: float = MMR_LAMBDA,
    threshold: float = SIM_THRESHOLD,
    similarity_fn: SimilarityFn = pain_similarity,
) -> list[str]:
    """MMR diversity selection over whitespace gaps. relevance(gap) = 'blind-spot-ness' =
    1 - max_sim(gap, reference_texts) (a gap most UNLIKE what the run surfaced ranks first).
    A gap whose max similarity to an already-selected gap >= threshold is dropped (MMR + dedup
    in one pass). Deterministic; ties break on original order."""
    cleaned = [g.strip() for g in (gaps or []) if g and g.strip()]
    if not cleaned:
        return []
    refs = [r for r in (reference_texts or []) if r and r.strip()]

    def blindspot(g: str) -> float:
        if not refs:
            return 1.0
        return 1.0 - max(similarity_fn(g, r) for r in refs)

    selected: list[str] = []
    remaining = list(enumerate(cleaned))            # (orig_idx, gap)
    while remaining:
        best = None                                 # (mmr_score, -orig_idx, orig_idx, gap, max_sel)
        for oi, g in remaining:
            max_sel = max((similarity_fn(g, s) for s in selected), default=0.0)
            mmr = lambda_ * blindspot(g) - (1.0 - lambda_) * max_sel
            cand = (mmr, -oi, oi, g, max_sel)
            if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] > best[1]):
                best = cand
        _mmr, _noi, oi, g, max_sel = best
        remaining = [(i, x) for (i, x) in remaining if i != oi]
        if selected and max_sel >= threshold:
            continue                                # near-duplicate of an already-selected gap -> drop
        selected.append(g)
    return selected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dedup.py -q`
Expected: PASS (16 tests total).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dedup.py tools/llm-council/tests/discovery/test_dedup.py
git commit -m "feat(discovery): E3 rank_gaps — MMR worst-first gap ranking with near-dup drop

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Pipeline wiring + `merged_count`

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Modify: `tools/llm-council/council/discovery/render.py` (add `merged_count` note)
- Modify: `tools/llm-council/council/discovery/render_substack.py` (add `merged_count` note)
- Test: `tools/llm-council/tests/discovery/test_pipeline.py`

**Interfaces:**
- Consumes: `council.discovery.dedup.dedup_verified`, `rank_gaps`, `_point_text`
- Produces: deduped `verified` + ranked `fr.blind_spots` flowing into frame/render; `session["merged_count"]`; `render_ledger(..., merged_count:int=0)` and `render_substack_ledger(..., merged_count:int=0)`.

- [ ] **Step 1: Write the failing test**

```python
# append to tools/llm-council/tests/discovery/test_pipeline.py
@pytest.mark.asyncio
async def test_pipeline_dedups_near_duplicate_pain_points():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/a", "https://d1.com/a", "2026-06-18", "exports fail silently", 9))
    bundle.add(EvidenceRecord("reddit", "r/b", "https://d2.com/b", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 2 records (2 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Exports fail silently", "exports silently fail on conflict",
                               ["exports fail silently"], ["https://d1.com/a"], intensity=5),
            CandidatePainPoint("Silently failing exports", "on conflict exports fail silently",
                               ["exports fail silently"], ["https://d2.com/b"], intensity=4),
        ], blind_spots=["x"], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert res.verified_count == 1                              # two near-dups collapsed to one
    assert res.session["merged_count"] == 1
    assert "Merged 1" in res.markdown                           # honest render note


@pytest.mark.asyncio
async def test_pipeline_ranks_blind_spots_worst_first():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/a", "https://d1.com/a", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Exports fail silently", "exports silently fail on conflict",
                               ["exports fail silently"], ["https://d1.com/a"], intensity=5),
        ], blind_spots=["nobody covers export conflict recovery",
                        "pricing transparency is unaddressed"],
           tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    md = res.markdown
    # the orthogonal gap (pricing) is ranked above the one close to the found pain (export recovery)
    assert md.index("pricing transparency is unaddressed") < md.index("nobody covers export conflict recovery")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py::test_pipeline_dedups_near_duplicate_pain_points tests/discovery/test_pipeline.py::test_pipeline_ranks_blind_spots_worst_first -q`
Expected: FAIL — `KeyError: 'merged_count'` / "Merged 1" not found / ordering assertion fails.

- [ ] **Step 3: Write minimal implementation**

In `tools/llm-council/council/discovery/pipeline.py`, add the import near the other discovery imports (after the `verify` import on line 19):

```python
from council.discovery.dedup import dedup_verified, rank_gaps, _point_text
```

Replace the verify/dropped block (currently lines 105-106):

```python
        verified = verify_pain_points(fr.pain_points, bundle)
        dropped = sum(1 for v in verified if not v.verified)
```

with:

```python
        verified = verify_pain_points(fr.pain_points, bundle)
        dropped = sum(1 for v in verified if not v.verified)
        # E3 — collapse near-duplicate gate-survived pains (honest merge), then rank D4's gaps
        # worst-first against what the run actually surfaced. Both reuse one lexical similarity.
        verified, merges = dedup_verified(verified)
        fr.blind_spots = rank_gaps(
            fr.blind_spots, [_point_text(v.point) for v in verified if v.verified])
```

In the substack branch, pass `merged_count` to the renderer (modify the `render_substack_ledger(...)` call, currently lines 124-126):

```python
            md = render_substack_ledger(topic=topic, tier=tier, segment=segment, angles=angles,
                                        quote_bank=quote_bank, fusion_result=fr, cost_usd=cost,
                                        dropped_count=dropped, supplement=supplement_result,
                                        merged_count=len(merges))
```

In the pm branch, pass `merged_count` to the renderer (modify the `render_ledger(...)` call, currently lines 131-133):

```python
            cards, quote_bank = frame_pm(verified, fr, bundle, today=today)
            md = render_ledger(topic=topic, lens=lens, tier=tier, segment=segment, cards=cards,
                               quote_bank=quote_bank, fusion_result=fr, cost_usd=cost,
                               dropped_count=dropped, supplement=supplement_result,
                               merged_count=len(merges))
```

Add `merged_count` to the session dict (in the `session = {...}` literal, after the `"dropped": dropped,` entry on line 139):

```python
            "dropped": dropped, "merged_count": len(merges), "cost_usd": cost,
```

In `tools/llm-council/council/discovery/render.py`, add the param to `render_ledger` (modify the signature on lines 9-12):

```python
def render_ledger(*, topic: str, lens: str, tier: str, segment: str = "", cards: list[IdeaCard],
                  quote_bank: list[str], fusion_result: FusionResult,
                  cost_usd: float, dropped_count: int,
                  supplement: "BackfillResult | None" = None, merged_count: int = 0) -> str:
```

and insert the note after the cost line (after line 16, `L.append(f"- **Cost:** ...\n")`):

```python
    if merged_count:
        L.append(f"- Merged {merged_count} near-duplicate pain point(s) before ranking.\n")
```

In `tools/llm-council/council/discovery/render_substack.py`, add the param to `render_substack_ledger` (modify the signature on lines 11-14):

```python
def render_substack_ledger(*, topic: str, tier: str, segment: str = "", angles: list[PostAngle],
                           quote_bank: list[str], fusion_result: FusionResult,
                           cost_usd: float, dropped_count: int,
                           supplement: "BackfillResult | None" = None, merged_count: int = 0) -> str:
```

and insert the note after its cost line (after line 18):

```python
    if merged_count:
        L.append(f"- Merged {merged_count} near-duplicate pain point(s) before ranking.\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -q`
Expected: PASS (all pipeline tests, including the 2 new ones).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/pipeline.py tools/llm-council/council/discovery/render.py tools/llm-council/council/discovery/render_substack.py tools/llm-council/tests/discovery/test_pipeline.py
git commit -m "feat(discovery): E3 wire dedup + gap-ranking into pipeline, merged_count note

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: `whitespace.py` wording — gaps are now ranked

**Files:**
- Modify: `tools/llm-council/council/discovery/whitespace.py`
- Test: `tools/llm-council/tests/discovery/test_whitespace.py`

**Interfaces:**
- Consumes: nothing new (pure formatter; gaps arrive pre-ranked from the pipeline).
- Produces: updated `_CAVEAT` / gap-section wording — gaps are ranked most-distinct-first, with an explicit "not a severity/confidence score" honesty note; absence-of-evidence + investigate-only guardrails unchanged.

- [ ] **Step 1: Write the failing test**

```python
# append to tools/llm-council/tests/discovery/test_whitespace.py
from council.discovery.whitespace import whitespace_hero


def test_hero_states_gaps_are_ranked_most_distinct_first():
    out = "\n".join(whitespace_hero(blind_spots=["gap one", "gap two"], tier="standard",
                                    segment="devs", verified_count=2, dropped_count=0))
    assert "most-distinct-first" in out
    assert "not a severity" in out.lower() or "not a confidence" in out.lower()
    # the absence-of-evidence guardrail must remain
    assert "absence-of-evidence" in out
    assert "investigate" in out.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py::test_hero_states_gaps_are_ranked_most_distinct_first -q`
Expected: FAIL — "most-distinct-first" not present.

- [ ] **Step 3: Write minimal implementation**

In `tools/llm-council/council/discovery/whitespace.py`, replace `_CAVEAT` (lines 10-14) with:

```python
_CAVEAT = (
    "> Gaps below = absence-of-evidence (what the panel and evidence did **not** surface), NOT "
    "verified claims or confirmed opportunities. They are **ranked most-distinct-first** — by "
    "dissimilarity to what this run actually surfaced, which is an ordering signal, **not a severity "
    "or confidence score** (a blind spot has no supporting evidence by definition). The next move for "
    "each gap is to **investigate** it — never to build on it. Absence of a surfaced gap is not proof "
    "of full coverage."
)
```

Update the gaps-section header (line 66) from:

```python
    L.append("**Gaps the panel/evidence missed:**")
```

to:

```python
    L.append("**Gaps the panel/evidence missed (ranked most-distinct-first):**")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py -q`
Expected: PASS — the new test passes and all pre-existing whitespace tests still pass (the guardrail substrings they assert on are preserved). If any pre-existing test asserted the old exact `_CAVEAT` string, update it to assert the preserved substrings (`absence-of-evidence`, `investigate`) rather than the full literal.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/whitespace.py tools/llm-council/tests/discovery/test_whitespace.py
git commit -m "feat(discovery): D4 hero — gaps ranked most-distinct-first (E3), guardrail intact

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: PM4 carry-forward nits

**Files:**
- Modify: `tools/llm-council/tests/discovery/test_scoring.py`

**Interfaces:**
- Consumes: existing `score_opportunity`, `EvidenceRecord`, `EvidenceBundle`.
- Produces: a new seam test for the source/domain counting asymmetry; `author{i}` → `src{i}` fixture rename.

- [ ] **Step 1: Write the failing test + apply the rename**

Add this test to `tools/llm-council/tests/discovery/test_scoring.py`:

```python
def test_domain_count_and_source_count_use_different_inputs():
    # Documented intentional asymmetry: distinct_domains is derived from supporting_urls (gate truth),
    # while engagement_sum/distinct_sources come from matched bundle records. Construct a case where a
    # supporting_url has NO matching record -> it still counts as a domain but contributes 0 sources.
    rec = EvidenceRecord("reddit", "solo", "https://matched.com/x", "2026-06-20", "q", engagement=50)
    supporting = ["https://matched.com/x", "https://unmatched.com/y"]   # 2 domains, 1 matched record
    s = score_opportunity(_pt(intensity=4), supporting, _bundle(rec), today=TODAY)
    assert s.distinct_domains == 2                 # from supporting_urls
    assert s.distinct_sources == 1                 # only the matched record's source_name
    assert s.engagement_sum == 50                  # only the matched record's engagement
```

In the same file, rename the fixture author labels to `src{i}` to match the `distinct_sources` honesty rename (these are cosmetic source labels, not assertions): on line 42 change `f"author{i}"` → `f"src{i}"`. (The `f"a{i}"` and `"solo"`/`"a"`/`"src"` labels elsewhere are already fine; only `author{i}` needs renaming.)

- [ ] **Step 2: Run test to verify the new test passes and rename is clean**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_scoring.py -q`
Expected: PASS (all scoring tests, including the new seam test). The rename does not change any assertion.

- [ ] **Step 3: Commit**

```bash
git add tools/llm-council/tests/discovery/test_scoring.py
git commit -m "test(discovery): PM4 nits — source/domain asymmetry seam test + src{i} fixture rename

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Docs — SKILL.md + CHANGELOG

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§2 stages, §4 FRAME)
- Modify: `CHANGELOG.md`

**Interfaces:** none (documentation).

- [ ] **Step 1: Update SKILL.md**

In `.claude/skills/fusion-discovery-council/SKILL.md`:
- In **§2 (stages)**: note that after VERIFY and before FRAME, a $0/deterministic **dedup** step collapses near-duplicate gate-survived pain points (bounded merge-to-canonical, honest evidence union, corroboration keyed on distinct domains), and that D4's whitespace gaps are now **ranked most-distinct-first** (MMR) rather than panel order.
- In **§4 (FRAME)**: note that the ranked ledger now reflects *distinct* pains (a `merged N near-duplicate pain point(s)` line appears when merges occur) and that corroboration counts are therefore honest.

- [ ] **Step 2: Update CHANGELOG.md**

Add an entry under the current/Unreleased section:

```markdown
- **fusion-discovery-council E3 — near-duplicate pain-point dedup + MMR gap ranking.** New
  `council/discovery/dedup.py` ($0/deterministic): a shared lexical token-Jaccard similarity drives
  (a) `dedup_verified` — collapses near-duplicate gate-survived pain points via bounded
  merge-to-canonical (bias-to-under-merge, no transitive closure), unioning evidence honestly with
  corroboration kept keyed on distinct domains; and (b) `rank_gaps` — MMR (Carbonell & Goldstein 1998,
  λ=0.3) ranking that orders D4's whitespace gaps most-distinct-first and drops near-duplicate gaps.
  Wired into `pipeline.py` after VERIFY; renderers show a `merged_count` note. Design grounded in a $0
  deep-research pass (`vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md`). Also
  closes two PM4 carry-forward test nits. No model cost, gate untouched.
```

- [ ] **Step 3: Run full suite + validator**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: all pass (baseline 212 + new tests; 1 skipped).
Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: validator passes.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md
git commit -m "docs(discovery): E3 dedup + MMR gap-ranking — SKILL.md §2/§4 + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Final adversarial review + field report

**Files:**
- Create: `docs/field-reports/2026-06-29-fusion-discovery-council-e3-mmr-dedup-field-report.md`

- [ ] **Step 1: Dispatch the Code Reviewer agent** on the most capable model against the full branch diff (`git diff main...HEAD`). Focus: gate integrity (no fabricated/merged quotes; corroboration not double-counted), the transitivity guard (no over-merge), MMR determinism, and the byte-stability of unchanged render paths.

- [ ] **Step 2: Triage findings.** Fix any Critical/Important inline (TDD: failing test → fix → green). Record Minor/deferred as tickets flagged for Sean (do not commit to `vault/`).

- [ ] **Step 3: Re-run gates** — `cd tools/llm-council && uv run pytest tests/ -q` + `python3 scripts/validate.py`.

- [ ] **Step 4: Write the field report** mirroring `docs/field-reports/2026-06-29-fusion-discovery-council-d4-whitespace-hero-field-report.md` (what shipped, the research-before-locking move + how it changed the design, process notes, what the review caught, vault hygiene, carry-forward).

- [ ] **Step 5: Commit + open PR** into `main` (one roadmap item). PR body ends with the Claude Code footer. Verify the staged set contains **zero `vault/` paths** before pushing.

## Self-Review (plan vs spec)

- **Spec coverage:** similarity core (T1), dedup_verified incl. honest merge + representative + transitivity guard (T2), rank_gaps MMR incl. near-dup drop (T3), pipeline wiring + merged_count + gap reorder (T4), whitespace wording w/ guardrail intact (T5), both PM4 nits (T6), SKILL/CHANGELOG (T7), final review + field report + vault hygiene (T8). All spec sections mapped.
- **Placeholder scan:** none — every code/edit step shows exact code and exact anchors.
- **Type consistency:** `dedup_verified`/`rank_gaps`/`MergeRecord`/`pain_similarity`/`_point_text`/`SIM_THRESHOLD`/`MMR_LAMBDA` names match across tasks and the pipeline import; renderer `merged_count` param matches the pipeline call sites.
