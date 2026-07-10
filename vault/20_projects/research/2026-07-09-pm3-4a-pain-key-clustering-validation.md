---
type: research
status: complete
tags: [fusion-discovery-council, pm3]
---

# PM3 Item 4a — Pain-Key Clustering Validation ($0)

> **Extended same-session (2026-07-09):** after the lexical matcher (Matcher 1) failed, two more $0 matchers were measured on the same judged pairs — E1's in-proc NLI cross-encoder (Matcher 2) and a local Ollama LLM judge (Matcher 3) — plus the two-stage candidate-gen → judge combination. See the Matcher 2 / Matcher 3 / Combined-architecture sections and the updated Verdict below the original sections.

## Method

PM3's core assumption: pains surfaced by different fusion-discovery-council runs on the same topic can be matched by a *stable key* (canonical title or similarity clustering), so a persistent pain-taxonomy store can dedup/link pains across re-runs.

Tested against real, on-disk data — two runs on the identical topic, same day, different tiers/panels:

- **Run A** (deep, 3 verified pains): `vault/20_projects/research/2026-06-21-claude-skills-2d-animation-pipelines-pm-deep-idea-ledger.md`
- **Run B** (standard, 12 verified pains): `vault/20_projects/research/2026-06-21-claude-skills-2d-animation-pipelines-pm-standard-idea-ledger.md`

Steps:
1. Extracted each pain card's title + descriptive "Pain:" text from both ledgers verbatim.
2. Read `tools/llm-council/council/discovery/dedup.py` (E3's near-duplicate merge machinery). Reused its actual `pain_similarity()` function (token-Jaccard over normalized, stopword-stripped tokens of `title + ". " + summary`) via a throwaway script (`pm3_4a_sim.py`) run with `cd tools/llm-council && uv run python ...` — no reimplementation. E3's own threshold: `SIM_THRESHOLD = 0.5`, documented as "biased toward UNDER-merging."
3. Computed the full 3×12 cross-run matrix (A-pains × B-pains) and the full 12×12 within-run B matrix.
4. Manually judged (same-pain / related-but-distinct / different) every A-pain's best B-match, plus scanned evidence-URL overlap across all 36 A×B pairs as a second, independent corroboration signal (shared source URL is a strong hint even when Jaccard score is low).
5. Scored precision/recall against the 80% campaign bar and ran the within-run B×B sanity probe.

Extension (same session):

6. **Matcher 2:** scored all 36 A×B pairs (plus the 5 most-confusable within-run B pairs) with E1's in-proc NLI cross-encoder (`council/discovery/nli.py`, `cross-encoder/nli-deberta-v3-small` int8 ONNX, CPU) — bidirectional entailment on the same title+summary texts, reporting min and mean of the two directions (`pm3_4a_nli.py`).
7. **Matcher 3:** judged the same 41 pairs with a local LLM (Ollama `qwen3.6_35b-a3b-32k`, `/api/chat`, temperature 0, think off, strict SAME / RELATED / DIFFERENT one-word verdict + one-line reason; `pm3_4a_llm_judge.py`). Scored against my human judgments, where the positive class for precision/recall is SAME (only SAME would trigger a merge in a persistence layer).
8. Evaluated the two-stage architecture proposed after pass 1: cheap candidate generation (shared evidence URL and/or lexical top-1) → LLM-judge confirmation.

## Match table

**Cross-run matrix (token-Jaccard, `pain_similarity`) — full scores:**

```
        B1     B2     B3     B4     B5     B6     B7     B8     B9    B10    B11    B12
A1   0.115  0.020  0.039  0.073  0.065  0.038  0.060  0.100  0.070  0.018  0.037  0.078
A2   0.028  0.015  0.045  0.087  0.038  0.014  0.030  0.029  0.055  0.141  0.059  0.092
A3   0.067  0.037  0.035  0.083  0.029  0.053  0.054  0.034  0.031  0.033  0.033  0.034
```

**Cross-run pairs at or above E3's threshold (≥0.5): zero.** The matcher, run at its own real operating point, made no claimed same-pain matches at all across this A×B set.

**Best (top-1) B-match per A-pain, judged by hand:**

| A-pain | Best B-match | Score | My verdict |
|---|---|---|---|
| **A1** — "Perceived regression in Claude Code reliability and code quality": *"Heavy users report that Claude Code has gotten slower and lower-quality on complex agentic tasks, raising the cost of supervising animation pipelines and undermining trust in agentic setups."* | **B1** — "Heavy manual cleanup required on precision-sensitive 2D tasks": *"Connector output is prototype quality at best... substantial human correction is required... cleanup, simple in-betweens, batch layer operations..."* | 0.115 | **Different.** A1 is a temporal "got worse recently" reliability/trust claim about Claude Code itself; B1 is a persistent capability-gap claim about connector precision work. Overlapping theme (quality shortfall) but distinct pains. |
| **A2** — "MCP/skill stacking causes latency, token waste, and state-management bugs": *"Layering many MCP servers, hooks, and skills makes pipelines feel slow, wastes tokens on schema processing each turn, and causes Claude to modify stale file versions..."* | **B10** — "Plugin/skill stack complexity hurts performance and clarity": *"Builders stacking MCP servers on top of hooks on top of skills find the resulting system slow and confusing..."* | 0.141 | **Same pain.** Both cite the identical source (`buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review`) and the identical quote ("Builders stacked MCP servers on top of hooks on top of skills and wondered why things felt slow."). This is a genuine cross-run duplicate — and it scored **0.141, nowhere near the 0.5 threshold.** |
| **A3** — "Output falls short of studio-grade motion design": *"Even when Claude successfully wires up animation pipelines, the resulting motion is amateurish — closer to slide-deck animation than professional motion graphics..."* | **B4** — "Adobe & Blender connectors feel unpredictable and not production-ready": *"Claude's Adobe and Blender Connectors have been tested on design/animation tasks and consistently judged unreliable for serious work."* | 0.083 | **Different.** A3's evidence base (a single YouTube review, unique to run A) never surfaced in run B at all. B4 is a connector-category reliability judgment; A3 is a craft/aesthetic-quality judgment about the resulting motion. Related theme, distinct pain. |

**A supplementary finding from the URL-overlap scan** (not captured by top-1 scoring): A1's second evidence URL (`trustpilot.com/review/claude.ai?page=9`) is the *same page* B12 ("Broken append/edit modes erode trust for incremental file changes") draws from — and the quote "Its append mode is broken." literally appears in A1's Quote Bank too, unused as A1's framed pain. Run A bundled that quote into its broad "regression" pain; run B split it out into its own separate pain-point (B12). Verdict: **related-but-distinct**, not same-pain — this is a *granularity mismatch* (one run's coarse pain = another run's several fine-grained pains), a different failure mode than simple phrasing drift, and it means "same source URL" alone is not a sufficient matching signal either.

## Precision + recall vs the 80% bar

Two ways to score precision, because the matcher's real threshold produced no matches at all:

1. **At E3's actual threshold (≥0.5):** 0 claimed matches → precision undefined by the strict correct/claimed formula, but functionally this is a **total failure to link anything cross-run** in this sample — the persistence layer would never connect A2 and B10 even though they cite the same source and the same quote.
2. **Forced top-1 (no threshold, always take the best match)**, the fairest reading of "matcher's claimed same-pain matches": 1 of 3 correct = **33% precision.**

Either reading is decisively **below the 80% bar. Verdict: FAIL.**

**Recall:** In this sample there is exactly one clean, independently-corroborated genuine cross-run same-pain pair: A2↔B10 (shared source + shared verbatim quote). The forced top-1 approach did surface it as A2's top candidate — but at a score (0.141) so far under the real threshold (0.5) that a threshold-gated matcher misses it entirely (recall 0/1 = 0% at the real operating point). One additional near-miss (A1's implicit relationship to B3/B8/B12) is a granularity split, not a clean same-pain match, so it doesn't count toward recall either way — it's a structurally different problem (one-to-many, not missed one-to-one).

## Within-run sanity probe

Ran `pain_similarity` on all 66 pairs within Run B alone (12 pains). **Max score: 0.161** (B1↔B7), well under the 0.5 threshold — confirming E3's threshold does not over-merge distinct pains within a single run, consistent with its documented "bias to under-merge."

But this is the crux problem for cross-run reuse: **the score band that contains the one genuine cross-run duplicate (A2-B10 = 0.141) overlaps with the score band of clearly-different within-run B pairs**:

| Pair | Score | Same pain? |
|---|---|---|
| B1 ↔ B7 | 0.161 | No — manual-cleanup-need vs. batch non-determinism |
| B4 ↔ B6 | 0.155 | No — connector unreliability vs. artist-replacement gap |
| B4 ↔ B5 | 0.113 | No — connector unreliability vs. weak multi-step planning |
| **A2 ↔ B10 (cross-run, genuine dup)** | **0.141** | **Yes** |

There is no single threshold in the 0.10–0.20 band that separates the one true cross-run match from the false within-run near-misses. Lowering the threshold enough to catch A2↔B10 would also start merging B1↔B7 and B4↔B6, which are not the same pain. Raw title+summary token-Jaccard, as currently tuned and even as re-tuned, does not have a workable single cut point for this job.

## Matcher 2 — E1's NLI cross-encoder (bidirectional entailment)

Scored every pair with `NliScorer.entails()` in both directions (A-text as premise / B-text as hypothesis, and reversed), reporting min and mean of the two directions. Note this is off-label use of E1's model — its production job is quote→pain *support* verification, not pain↔pain *equivalence* — and the results show exactly why that distinction matters.

**Result: total failure — worse than Jaccard.** The one genuine duplicate ranks near the *bottom*; judged-different pairs top the ranking. Key rows (full table in `pm3_4a_nli_results.json`; `(wr)` = within-run B pair):

| Pair | fwd (P→H) | bwd (H→P) | min | mean | My verdict |
|---|---|---|---|---|---|
| B4 ↔ B6 (wr) | 0.883 | 0.219 | **0.219** | **0.551** | different |
| B1 ↔ B6 (wr) | 0.975 | 0.003 | 0.003 | 0.489 | different |
| A1 ↔ B9 | 0.000 | 0.738 | 0.000 | 0.369 | different |
| B1 ↔ B7 (wr) | 0.038 | 0.230 | 0.038 | 0.134 | different |
| **A2 ↔ B10 (true dup)** | 0.030 | 0.000 | **0.0003** | **0.015** | **same** |
| median of all 36 A×B pairs | — | — | ~0.001 | ~0.003 | (35 different/related) |

No threshold on min or mean separates same-pain from different: ranked by mean, four judged-different pairs sit above the true duplicate; ranked by min, the true duplicate is in the bottom quartile. **Precision at any threshold that claims ≥1 match: 0%. Recall at any usable threshold: 0/1.**

Why it fails (and why this doesn't impugn E1's gate): entailment is directional and literal. Paraphrases of the same pain each carry details the other omits (A2's "token waste, stale file versions" vs B10's "confusing, DCC apps, render farms"), so *neither* direction entails — the true dup scores ~0. Meanwhile a specific complaint entails a generic one (B1 "connector output needs heavy correction" → B6 "falls short of replacing a skilled artist" at 0.975), producing spurious high one-directional scores between distinct pains. Same-pain matching needs symmetric semantic similarity, which NLI entailment is not.

## Matcher 3 — local LLM judge (qwen3.6_35b-a3b-32k, $0)

All 36 A×B pairs + the 5 confusable within-run pairs, temperature 0, strict one-word verdict. Distribution: 5 SAME, 14 RELATED, 22 DIFFERENT. Full verdicts + reasons in `pm3_4a_llm_results.json`.

**Judge's SAME claims vs my human judgments:**

| Pair | LLM verdict | My verdict | Call |
|---|---|---|---|
| **A2 ↔ B10** | SAME | **same** (shared source + verbatim quote) | **true positive** |
| A1 ↔ B5 | SAME | different (temporal regression vs planning-capability gap) | false positive |
| A1 ↔ B7 | SAME | different (regression-over-time vs batch non-determinism) | false positive |
| A3 ↔ B1 | SAME | related-but-distinct (aesthetic motion quality vs precision-cleanup burden) | false positive |
| B1 ↔ B7 (wr) | SAME | different | false positive |

- **Precision: 1/4 = 25%** on the 36 cross-run pairs (1/5 = 20% including within-run probes). **Below the 80% bar standalone.**
- **Recall: 1/1 = 100%** — it caught the true duplicate, and critically it also got the two hard negative-space cases right: **A1↔B12 → RELATED** (the granularity-mismatch pair sharing a Trustpilot URL — correctly *not* merged) and **A1↔B1 / A3↔B4 → RELATED** (the lexical top-1 false candidates — correctly rejected).
- Binary same/not-same agreement with my judgments: 37/41 pairs. The failure mode is uniform: over-merging thematically-adjacent pains ("declining quality" umbrella) when both texts orbit the same product complaint climate. Its RELATED band is broader than mine, but RELATED never triggers a merge, so only the SAME over-claims cost precision.

## Combined architecture — candidate generation → LLM confirm

The decisive observation: **all four of the LLM judge's false positives lie outside every cheap candidate set.** Measured on this sample:

| Architecture | Candidates generated | LLM confirms SAME | Precision | Recall |
|---|---|---|---|---|
| Shared exact evidence-URL | A2-B10, A1-B12 | A2-B10 | **1/1 = 100%** | 1/1 = 100% |
| Lexical top-1 per A-pain | A1-B1, A2-B10, A3-B4 | A2-B10 | **1/1 = 100%** | 1/1 = 100% |
| Union (URL ∪ lexical top-1) | A1-B1, A1-B12, A2-B10, A3-B4 | A2-B10 | **1/1 = 100%** | 1/1 = 100% |
| LLM judge alone, no candidate gate | all 36 | 4 pairs | 1/4 = 25% | 1/1 = 100% |

The candidate stage and the judge stage fail in *complementary* ways: cheap signals (URL overlap, lexical top-1) are precision-poor but never proposed the judge's false-positive pairs (A1-B5 = 0.065, A1-B7 = 0.060, A3-B1 = 0.067 — all deep in lexical noise, no shared URLs); the judge is recall-strong and correctly rejects the candidates the cheap signals over-propose (A1-B1, A3-B4, A1-B12). Two-stage clears the bar; each stage alone fails it.

One measured risk to carry into 4b: a lexical *band* candidate generator (e.g. ≥0.10 all-pairs rather than top-1) would have proposed B1↔B7 (0.161) had it been a cross-run pair, and the judge wrongly merges that one — so keep candidate generation tight (top-1 per new pain + exact-URL overlap), not band-based.

## Verdict & implications for 4b's key design (updated after Matchers 2–3)

**Single-signal matchers all fail the 80% bar on this sample:**

| Matcher | Precision (SAME claims) | Recall (1 true dup) | 80% bar |
|---|---|---|---|
| 1. Canonical-title / token-Jaccard @ 0.5 (E3's real operating point) | 0 claims (functional total miss) | 0% | FAIL |
| 1'. Jaccard forced top-1 | 33% (1/3) | 100% | FAIL |
| 2. NLI bidirectional entailment (any threshold) | 0% | 0% | FAIL |
| 3. Local LLM judge alone | 25% (1/4) | 100% | FAIL |
| **4. Candidate gen (exact-URL ∪ lexical top-1) → LLM confirm** | **100% (1/1)** | **100% (1/1)** | **PASS** (n=1 positive — see caveats) |

**Recommended matching architecture for 4b:**

1. **Key:** persist each pain as a row with its full title+summary text and its evidence URLs — *not* a canonical-title string key and not a raw similarity cluster ID. Matching is a *process* run at ingest, not a hash.
2. **Candidate generation (cheap, deterministic, $0):** for each incoming pain, propose (a) any stored pain sharing an exact evidence URL, and (b) the lexical top-1 stored pain via E3's existing `pain_similarity` (reused as-is, no threshold gate — top-1 only). Keep it tight; do not use a lexical score band (measured over-merge risk at 0.16).
3. **Confirmation (local LLM, $0):** judge each candidate pair SAME / RELATED / DIFFERENT at temperature 0 with the strict one-word protocol used here (`qwen3.6_35b-a3b-32k` on the MBP, or any tier-2 local route). Merge only on SAME; persist RELATED verdicts as a typed link instead of a merge — this is exactly the shape of the existing `concept_edges` relation set (`related_to` vs a merge), and it is how the granularity-mismatch case (A1↔B12) wants to be stored.
4. **One-to-many handling:** measured need, not hypothetical — run A's coarse "regression" pain maps to ≥2 of run B's fine-grained pains via shared evidence. Judge each candidate pair independently and allow multiple RELATED links (and in principle multiple SAME merges) per incoming pain; never force a bijection.
5. **Embedding similarity (nomic-embed-text via the Mac Mini, `similarity_fn` injection point already designed into dedup.py) remains the untested upgrade path** for candidate generation if cross-run recall on future topics proves worse than top-1 lexical + URL overlap can catch — it was *not* measured here, so it ships behind evidence, not by default.

## Caveats

- **n is small.** This is 3×12 = 36 cross-run pairs and 66 within-run pairs from a *single topic, single day*. One clean genuine duplicate is not enough to compute a statistically meaningful recall rate — the 0%/100% recall framing above should be read as "the one case we have shows a clear miss," not as a stable rate.
- Judgments (same-pain / related-but-distinct / different) are my own reading, not a second independent rater — I've quoted both texts side-by-side above specifically so a human (or a second LLM judge) can re-derive or contest the calls.
- I did not exhaustively hand-read all 36 cross-run pairs at prose level; beyond the 3 top-1 matches I relied on an evidence-URL overlap scan across all pairs to catch other likely duplicates (which is how A1↔B12 surfaced). It's possible a full manual read of all 36 pairs would surface one more borderline case, but it would not change the headline verdict — the sample is dominated by non-matches either way.
- **The combined architecture's 100%/100% rests on a single true-positive pair (A2↔B10).** With one genuine duplicate in the sample, the pass is best read as "no measured failure" rather than a validated rate. What *is* well-supported by the data is the complementarity argument (the judge's 4 false positives all fall outside the cheap candidate sets, and the judge correctly rejects all 4 cheap-signal false candidates) — that structural result is 8-for-8 on this sample and is the real basis for the recommendation.
- Matcher 3's ground truth is my own 41-pair judgment set (verdicts + side-by-side texts preserved above and in `pm3_4a_llm_results.json`), not a second independent human rater. The four disputed SAME calls are quoted so a human can re-judge.
- Matcher 2 used E1's NLI model off-label (equivalence, not quote-support). Its failure here says nothing about the VERIFY gate's fitness for its actual job.
- Embedding-based candidate generation (nomic-embed-text) was **not** tested — the recommendation keeps it as a contingent upgrade path, not a validated component.
- Scratch scripts + raw outputs: `pm3_4a_sim.py`, `pm3_4a_nli.py`, `pm3_4a_llm_judge.py`, `pm3_4a_{results,nli_results,llm_results}.json` in the session scratchpad (not committed).
