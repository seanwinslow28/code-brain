# Field Report — fusion-discovery-council PM3 groundwork: de-risk + pre-plan (Item 4)

**Date:** 2026-07-09
**Campaign:** Phase 2 "everything buildable now" — **Item 4 of 4** (research + spec only; no branch, no PR, no build)
**Cost:** $0 (E3 lexical similarity + E1's in-proc NLI + local Ollama qwen3.6-35b; all local)

## 4a — pain-key clustering validation: the assumption FAILED, and the failure bought the design

PM3's §7 assumption #2 ("same pain" is matchable across runs by a stable key) was tested on the
only true same-topic pair on disk: the two 2026-06-21 2D-animation pm runs (3×12 verified pains,
36 cross-run pairs, human-judged, one independently-corroborated genuine duplicate).

**Every single-signal matcher fails the ≥80% bar:**
- E3's token-Jaccard at its 0.5 threshold: zero claims — cross-run phrasing drift lives at
  0.06–0.17, an order below the within-run dedup band. Canonical-title keys are dead on arrival.
- E1's NLI cross-encoder (bidirectional, any threshold): 0% — principled failure; paraphrase
  duplicates entail in neither direction, specific→generic entails spuriously. (Off-label use —
  no reflection on the E1 gate.)
- Local LLM judge alone: 100% recall, 25% precision — over-merges thematically-adjacent pains.

**The two-stage architecture passes:** candidate-gen (exact evidence-URL overlap ∪ lexical top-1)
→ temperature-0 local LLM confirm, merge only on SAME. 100%/100% on this sample, and the
structural finding is stronger than the n=1 headline: the stages fail in *complementary* ways,
8-for-8 — every judge false-positive lies outside every cheap candidate set; the judge rejects
every false candidate the cheap signals over-propose. Measured hazard: band-based lexical
candidate gen admits a pair the judge wrongly merges — candidate gen must stay top-1 + exact-URL.
Bonus discovery: granularity mismatch (one broad pain ↔ several fine-grained) is a distinct
failure mode needing a typed `broader_than` link, not a merge.

Findings note: `vault/20_projects/research/2026-07-09-pm3-4a-pain-key-clustering-validation.md`
(side-by-side quotes, full score tables, prominent small-n caveat).

## 4b — persistence spec (execute-ready, gated)

`docs/superpowers/specs/2026-07-09-pm3-persistence-design.md`: SQLite at
`vault/.discovery-pains.db` (own file next to `.vault-index.db` — different producer, different
locks); **no stable pain-key** (opaque ids; identity established per-ingest by the measured
two-stage matcher); `EvidenceRecord`-mirroring evidence table so `EvidenceBundle.to_dict/from_dict`
round-trips; observations preserve full per-run phrasing/intensity/velocity history;
`match_audit` makes every judge decision replayable; honest Ollama-down deferral (no cloud
fallback); trend labels (newly emerged / accelerating / cooling / steady) as one pure recalibrable
function, emitted into the ledger + the D3 dashboard's reserved PM3 slot.

## The gate holds

The **7/21 t1 verdict** remains the only thing between this spec and a build: it tests whether
cross-run deltas on a 2-week gap are signal or panel noise (red-team #5). GO → 4b executes as
written, with the 4a corpus as regression fixtures. KILL → Phase 2 spent $0 on this item.

## Carried forward
- Embedding-based candidate gen: untested upgrade path — evaluate against the same 4a corpus first.
- D3's session store (Item 3) is the provenance spine PM3 links to via `session_id`; the
  persist-by-default fix is what makes PM3's history accumulation trustworthy at all.
