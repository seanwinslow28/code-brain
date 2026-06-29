# Spec — fusion-discovery-council E3: near-duplicate pain-point dedup + MMR gap ranking

- **Date:** 2026-06-29
- **Branch:** `feat/discovery-e3-mmr-dedup`
- **Roadmap item:** E3 (Step B), closing the D4↔E3 coupling
- **Research:** `vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md`
- **Predecessors:** PM4+D1 (`scoring.py`/`bet.py`, #103) · D4 (`whitespace.py`, #104)

## Problem

Two defects in the discovery ledger today:

1. **Near-duplicate pain points are not collapsed.** The Fusion judge can emit three near-duplicate
   `CandidatePainPoint`s for one underlying pain. Each becomes its own ranked card, and each inflates
   the corroboration signal — so the ranked list shows "3 versions of the same pain" and
   `distinct_sources`/corroboration counts overstate distinct evidence.
2. **D4's whitespace gaps render in panel order with an explicit "no rank claim" caveat** because there
   was no similarity/score signal over gaps. The D4 field report flags this as coupled to E3: the
   similarity machinery built for pain-point dedup is what lets the whitespace hero rank gaps
   worst-first.

## Goal

Before FRAME, collapse semantically near-duplicate pain points into one — keeping the strongest
evidence and merging corroboration **honestly** — so the ranked ledger reflects *distinct* pains. Then
reuse the same similarity signal to **rank D4's whitespace gaps** (replacing panel order), dropping the
"no rank claim" caveat. Recency/reach decay already live in `scoring.py` (PM4) and are **not**
re-touched here — E3's net-new is the dedup + a defensible, shared similarity signal.

## Research grounding (load-bearing decisions)

Full synthesis + citations: `vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md`
(22/25 claims confirmed via adversarial verify; 3 refuted). The findings that shaped the design:

1. **MMR is the wrong tool for pure dedup; it's the right tool for diversity selection.** The canonical
   formula (verified verbatim against Carbonell & Goldstein 1998, ACL X98-1025) is
   `MMR(Dⱼ) = λ·Sim(Dⱼ,Q) − (1−λ)·maxᵢ∈S Sim(Dⱼ,Dᵢ)`; the **max** (not average) over the selected set
   is the near-duplicate penalty. The research's open question #3 establishes that for *pure dedup with
   no query*, a **direct pairwise-similarity threshold + transitivity-guarded clustering** is the
   appropriate tool, while MMR fits the **gap ranking/selection** problem. → The prompt's "same
   machinery" is honestly a **shared similarity function**, used by two different algorithms.
2. **Lexical token Jaccard is the $0/deterministic workhorse**, but the strongest caveat in the report:
   the standard 0.7–0.9 thresholds are calibrated for **long documents**; short 1–2 sentence texts have
   few tokens, so Jaccard is noisy and a single token swap moves the score a lot. **No source supplied
   a short-text-specific threshold.** → threshold is a tunable constant, biased conservative,
   calibrated against fixtures.
3. **Dominant over-merge trap = transitive closure** (A=B, B=C ⇒ A=C; Oracle Jones/James/Jamos
   example). Conservative posture (Neo4j, record-linkage literature): **start high, bias toward
   under-merging.** Connected-components-as-the-guard was *refuted* — don't lean on it. → greedy
   **merge-to-canonical** (each non-canonical attaches to at most one canonical; merged-away points
   never anchor comparisons) instead of unbounded transitive clustering.
4. **Honest merge (Fellegi-Sunter framing) is only additive under independence**; syndicated /
   same-domain sources double-count. → union source URLs, but corroboration stays keyed on **distinct
   domains** (which `scoring.py` already does), so a merge cannot inflate corroboration.
5. **MMR λ for a diversity goal is low (~0.3 band).** λ=1 pure relevance, λ=0 pure diversity. →
   `MMR_LAMBDA = 0.3`.

## Design

### New module: `council/discovery/dedup.py` ($0, deterministic, no model call)

**Layer 1 — shared similarity core**

- `normalize_tokens(text: str) -> frozenset[str]` — lowercase, strip punctuation, split on whitespace,
  drop a small inline English stopword set. No external deps (determinism + hermetic tests).
- `jaccard(a: frozenset, b: frozenset) -> float` — `|a∩b| / |a∪b|`; returns `0.0` when the union is
  empty (two empty texts are treated as **non-duplicates** — safe under the under-merge bias).
- `pain_similarity(a: str, b: str) -> float` — `jaccard(normalize_tokens(a), normalize_tokens(b))`.
  This is the default `similarity_fn`; both algorithms accept `similarity_fn` as an injectable
  parameter so a future `nomic-embed-text` local-embedding path can swap in **without touching either
  algorithm**.
- `_point_text(point: CandidatePainPoint) -> str` — `f"{point.title}. {point.summary}"` (the text the
  similarity function compares).

**Layer 2 — pain-point dedup (threshold-clustering, runs after verify)**

```python
SIM_THRESHOLD = 0.5   # tunable; conservative, biased toward under-merging; finalized in TDD

@dataclass(frozen=True)
class MergeRecord:
    canonical_title: str
    merged_titles: list[str]      # titles absorbed into the canonical (excludes canonical)

def dedup_verified(
    verified: list[VerifiedPainPoint],
    *,
    threshold: float = SIM_THRESHOLD,
    similarity_fn: Callable[[str, str], float] = pain_similarity,
) -> tuple[list[VerifiedPainPoint], list[MergeRecord]]:
    ...
```

- Only `verified == True` points participate. Unverified points pass through unchanged and in their
  original relative position is irrelevant (FRAME drops them), but they are **not** dropped here, so
  `dropped_count` computed upstream stays correct.
- **Evidence strength key** (for representative selection + cluster seeding), strongest first:
  `(distinct_domains(supporting_urls) DESC, intensity DESC, len(quotes) DESC, original_index ASC)`.
- **Greedy merge-to-canonical** (transitivity guard): iterate verified-true points in strength order.
  For each, compute similarity (via `similarity_fn` on `_point_text`) against every existing
  **canonical**. Join the single **best-matching** canonical whose `sim ≥ threshold` (argmax); if none,
  the point becomes a new canonical. Merged-away points never become comparison anchors → no unbounded
  transitive closure.
- **Honest merge** of a cluster into its canonical:
  - title / summary / lead-quote / intensity / consensus / recency = **canonical's** (strongest
    evidence wins; intensity & consensus are *kept, never maxed* — no inflation).
  - `supporting_urls`, `point.urls`, `point.quotes` = **order-preserving unions** across the cluster
    (so scoring, the quote bank, and receipts see all distinct evidence).
  - Result is a `VerifiedPainPoint(point=merged CandidatePainPoint, verified=True,
    supporting_urls=union)`. Corroboration is recomputed downstream by `score_opportunity` from
    distinct **domains** of the unioned `supporting_urls` → syndicated/same-domain merges cannot
    inflate it.
- Output order: deduped canonicals (FRAME re-sorts by composite anyway).

**Layer 3 — gap ranking (MMR, for D4)**

```python
MMR_LAMBDA = 0.3   # diversity-dominant (research)

def rank_gaps(
    gaps: list[str],
    reference_texts: list[str],            # deduped verified pain texts (_point_text of each)
    *,
    lambda_: float = MMR_LAMBDA,
    threshold: float = SIM_THRESHOLD,
    similarity_fn: Callable[[str, str], float] = pain_similarity,
) -> list[str]:
    ...
```

- `blindspot(gap) = 1 − max_sim(gap, reference_texts)` (empty reference ⇒ 1.0). A gap most *unlike*
  what the run surfaced scores highest → "worst-first" = most-distinct-first.
- MMR greedy selection: repeatedly pick the unselected gap maximizing
  `λ·blindspot(gap) − (1−λ)·max_sim(gap, already-selected gaps)`.
- **Near-duplicate gap drop:** a gap whose `max_sim(gap, already-selected) ≥ threshold` is dropped
  (MMR + dedup in one pass). Blank/whitespace gaps are dropped (existing `whitespace.py` behavior,
  preserved).
- Deterministic tie-break: original index ascending.

### Pipeline wiring (`pipeline.py`, minimal)

Insert between `verify_pain_points` and backfill/frame:

```python
verified = verify_pain_points(fr.pain_points, bundle)
dropped  = sum(1 for v in verified if not v.verified)          # unchanged
verified, merges = dedup_verified(verified)                    # NEW
fr.blind_spots   = rank_gaps(                                  # NEW — reorder in place
    fr.blind_spots,
    [_point_text(v.point) for v in verified if v.verified],
)
```

- Backfill, `frame_pm`, `frame_substack`, both renderers, and the session all read the deduped
  `verified` / ranked `fr.blind_spots` with no further plumbing (renderers already read
  `fusion_result.blind_spots`; backfill consumes `fr.blind_spots` → now ranked worst-first).
- `session["merged_count"] = len(merges)` — an honest delta explaining why `verified` (distinct pains)
  may be lower than gate survivors. Surface as a one-line render note ("Merged N near-duplicate
  pain point(s)") when `> 0`.

### `whitespace.py` (wording only — guardrail stays)

- The absence-of-evidence guardrail, investigate-only per-gap action, and "no fabricated score on a
  gap" all **stay**.
- Change the framing that gaps are panel-order / carry no rank claim → gaps are now **ranked
  most-distinct-first** with an explicit honesty note: *this ordering is by dissimilarity to what the
  run surfaced — it is not a severity or confidence score.*

### PM4 carry-forward nits (same PR, same files)

1. **Source/domain asymmetry seam test** in `test_scoring.py`: a case where `supporting_urls` carry
   domains with no matched bundle record (and vice versa), asserting `distinct_domains` derives from
   `supporting_urls` while `engagement_sum`/`distinct_sources` derive from matched records — locking
   the documented intentional asymmetry against regression.
2. **Fixture rename** `author{i}` → `src{i}` across `test_scoring.py` fixtures, matching the
   `distinct_sources` honesty rename.

## Out of scope (YAGNI)

- No embeddings/NLI (injectable seam only; lexical default). No recency/reach changes (PM4 owns them).
- No new model calls, no cost. No interactive triage. No SQLite/persistence (that's PM3/E-tier).
- Dedup does not run before the gate; the gate is untouched.

## Testing (TDD — watch each fail first)

`tests/discovery/test_dedup.py`:
- `normalize_tokens` / `jaccard` units (empty-set → 0.0; identical → 1.0; partial overlap).
- **Merge:** reordered/restated near-dup pair merges; union of `supporting_urls`/quotes; canonical =
  strongest evidence; corroboration not double-counted (same-domain dup doesn't raise distinct_domains).
- **Under-merge bias:** two distinct pains sharing a couple content tokens do **not** merge.
- **Transitivity guard:** a 3-point chain (A~B, B~C, A≁C) does not over-collapse A and C.
- **Injectable seam:** a stub `similarity_fn` drives merging deterministically.
- **MMR:** worst-first ordering against a reference set; near-duplicate gap dropped; empty reference
  and empty gaps edge cases.

`tests/discovery/test_pipeline.py`: dedup runs after verify, before frame; `fr.blind_spots` ranked;
`merged_count` in session; `dropped_count` unchanged by merges.

`tests/discovery/test_whitespace.py`: new most-distinct-first wording present; absence-of-evidence
guardrail + investigate-only action still present.

`tests/discovery/test_scoring.py`: the 2 PM4 nits.

Gates: `cd tools/llm-council && uv run pytest tests/ -q` (currently 212 passed / 1 skipped) +
`python3 scripts/validate.py` (repo root). Final whole-branch adversarial review via the Code Reviewer
agent on the most capable model.

## Cost & vault

$0 (deep-research on subscription; build is local/deterministic). Per the active vault cycle, the
research note is written to `vault/20_projects/research/` but left **unstaged** for Sean; this branch
carries **zero vault changes**.
