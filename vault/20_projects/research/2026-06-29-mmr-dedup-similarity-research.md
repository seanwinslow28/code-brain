---
title: "Research — MMR, lexical near-duplicate dedup, and honest evidence merging (E3)"
date: 2026-06-29
tags: [research, fusion-discovery-council, dedup, mmr, similarity]
status: active
method: deep-research skill ($0, Anthropic subscription) — 5 angles, 21 sources fetched, 94 claims extracted, 25 adversarially verified (3-vote), 22 confirmed / 3 refuted
feeds: docs/superpowers/specs/2026-06-29-discovery-e3-mmr-dedup-design.md
---

# MMR + near-duplicate dedup + honest merge — research for E3

Scoped to the load-bearing unknowns for E3 (near-duplicate pain-point dedup + reusing the similarity
signal to rank D4's whitespace gaps): MMR's λ direction, lexical similarity metrics + thresholds for
**short** texts under a $0/deterministic constraint, dedup failure modes, and honest evidence merging.
Lexical/deterministic methods were preferred over neural embeddings per the build constraint.

## Findings

### 1. MMR is the wrong tool for pure dedup — right tool for diversity *selection* (confidence: high)
The canonical formula, verified verbatim against the **Carbonell & Goldstein 1998** primary PDF
(ACL Anthology X98-1025):

> `MMR(Dⱼ) = λ·Sim₁(Dⱼ,Q) − (1−λ)·maxᵢ∈S Sim₂(Dⱼ,Dᵢ)`

The diversity term subtracts the **maximum** (not average) pairwise similarity to already-selected
items — this is precisely what makes MMR a *near-duplicate penalty* (a candidate is penalized by its
single closest prior selection). **But** the research's open question #3 establishes that for **pure
dedup with no query**, the relevance term degenerates ("relevance-to-pool"), and a **direct pairwise
similarity threshold + transitivity-guarded clustering** is the appropriate tool. MMR fits the
**ranking/selection** problem (ordering gaps with diversity).
- Vote: 3-0 on the formula (against the primary source). Sources: Carbonell & Goldstein 1998 (via
  grokipedia/inferensys/truegeometry mirrors of the formula); open-question framing from the
  synthesis caveats.

### 2. For a diversity goal, MMR λ is LOW — ~0.3 band (confidence: high)
λ=1.0 = pure relevance (no diversity); λ=0.0 = pure diversity. Recommended bands: **0.3–0.5
diversity/exploration**, 0.5–0.7 balanced, ≥0.8 relevance-dominant (LangChain default 0.7).
- Vote: unanimous across 6 supporting claims. **Refuted (0-3):** the narrower "optimal λ 0.5–0.75" —
  do not adopt. Sources: Elastic, Qdrant, Inferensys, LangChain docs.
- **→ `MMR_LAMBDA = 0.3`** (diversity-dominant; we want the most-distinct gap first).

### 3. Lexical token Jaccard is the $0/deterministic workhorse; thresholds are NOT short-text-calibrated (confidence: high, with a critical scope caveat)
Mainstream near-duplicate Jaccard thresholds are **0.7–0.9** (0.7 aggressive, 0.8 de-facto standard,
0.9 near-perfect-only); SlimPajama-DC and CulturaX both use 0.8 over n-grams. **Critical caveat:** these
are calibrated for **long documents / full web pages**, *not* the 1–2 sentence title+summary items E3
targets. Short texts have few shingles, so Jaccard is noisy and a **single token swap moves the score
sharply** (a one-word difference in 3-word shingles → J=0.333). No source supplied a short-text-specific
threshold.
- Vote: 3-0 on the 0.7–0.9 band; the short-text non-transfer is the synthesis's headline caveat.
- **→** token Jaccard with normalization (lowercase + punctuation strip + stopword removal); threshold a
  **tunable constant, biased conservative (~0.5), finalized against realistic fixtures**, not a
  hard-coded literature number.

### 4. Normalization matters more than the raw metric for short text (confidence: high)
Word-level shingles are sensitive to synonym substitution; **character-level shingles after lowercasing
are more robust** to synonyms/formatting/case. (A specific char-shingle k of 5–9 was **refuted 0-3** —
do not cite a settled k.)
- **→** normalize aggressively (lowercase, strip punctuation, drop stopwords) before token Jaccard;
  keep the metric injectable so a char-n-gram or embedding variant can swap in if lexical under-merges
  in practice.

### 5. Dominant over-merge failure = transitive closure; conservative posture = start high, bias under-merge (confidence: high / medium)
Transitive closure (A=B, B=C ⇒ A=C even when A≁C directly) is the classic over-merge trap — Oracle's
own docs give the "Jones=James=Jamos" false-merge example, and ER literature (Draisbach et al.) calls
unguarded transitive closure "dangerous." Recommended posture (Neo4j, record-linkage refs): **begin
with high thresholds, lower only as observed quality justifies — deliberately bias toward
under-merging.** **Refuted (0-3):** "connected-components-with-one-representative is THE guard" — do
not present component analysis as settled best practice.
- **→** greedy **merge-to-canonical**: each non-canonical attaches to at most one (best-matching)
  canonical above threshold; merged-away points never anchor further comparisons → bounded, no
  unbounded chaining. Bias the threshold conservative.

### 6. Honest merge: union fields, but corroboration is only additive under independence (confidence: medium)
The **Fellegi-Sunter** record-linkage model is the principled frame (λ prior + m/u probabilities;
additive log match-weights). **Critical caveat:** additivity holds **only under conditional
independence** — correlated/syndicated sources **double-count** if summed naively (Oxford IJE: the
independence assumption "is likely to be violated in practice").
- Vote: FS parameters 3-0; additive merging 2-1 (the independence caveat is the reason for the split).
- **→** on merge, take the **union of source URLs** but keep corroboration keyed on **distinct
  domains** (already how `scoring.py` computes it), so syndicated/same-domain merges cannot inflate the
  corroboration signal. Keep canonical intensity/consensus (don't max — no inflation).

## Refuted claims (do NOT adopt)
- "Optimal MMR λ is 0.5–0.75." (0-3)
- "Most LLM dedup uses character shingles k=5–9 / The Pile used k=5" as a settled number. (0-3)
- "Connected-component analysis with one representative is THE conservative over-merge guard." (0-3)
- (Not adopted, flagged in caveats) IJNRD's single 0.4 cutoff applied to both cosine and Jaccard —
  contradicts mainstream 0.7–0.9 and is from a low-tier journal.

## Open questions (acknowledged, handled by conservative defaults + tests)
1. Exact Jaccard/char-n-gram threshold for short 1–2 sentence texts — none published; we calibrate
   against fixtures and bias conservative.
2. Quantified threshold delta from stopword/stemming normalization on short text — unquantified; we
   normalize and validate empirically.
3. Best practical transitive-over-merge guard given component-analysis was refuted — we use bounded
   merge-to-canonical (no unbounded closure).

## How this changed the build
1. **Split one "MMR for everything" idea into two algorithms sharing a similarity function.** The
   research's open-question #3 is the pivot: pain-point **dedup** uses threshold merge-to-canonical;
   gap **ranking** uses MMR (λ=0.3). The prompt's "same machinery" → a shared `pain_similarity`, not a
   shared algorithm. This is cleaner and more defensible than forcing MMR onto dedup.
2. **Made the threshold a conservative tunable, not a literature constant.** The short-text
   non-transfer caveat (finding #3) means 0.8 would be wrong; we default ~0.5 and calibrate in TDD,
   explicitly biased to under-merge (finding #5).
3. **Chose bounded merge-to-canonical over transitive clustering** (finding #5) — directly avoids the
   documented over-merge trap; component-analysis was refuted as the guard.
4. **Locked corroboration to distinct domains on merge** (finding #6) — the union-but-don't-double-count
   rule falls out of the independence caveat and reuses `scoring.py`'s existing domain keying.
5. **Set the gap-rank honesty framing:** "most-distinct-first" is an ordering by dissimilarity to what
   the run surfaced — explicitly *not* a severity/confidence score (preserves D4's absence-of-evidence
   guardrail).
