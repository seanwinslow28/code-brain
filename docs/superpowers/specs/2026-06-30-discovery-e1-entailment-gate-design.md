# E1 — Entailment gate v2 for the core VERIFY stage (design spec)

- **Date:** 2026-06-30
- **Project:** fusion-discovery-council
- **Roadmap item:** E1 (the defensibility/brand core — "verified, not hallucinated")
- **Research:** `vault/20_projects/research/2026-06-30-citation-entailment-nli-verification-research.md`
- **Branch:** `feat/discovery-e1-entailment-gate`

## Problem

Today the anti-fabrication gate is **substring containment**:
`verify.py::quote_supported_at_url(*, cited_quote, fetched_text) -> bool` lowercases both and
asks `cited_quote in fetched_text`. It is the single shared chokepoint for **Stage 3 VERIFY**
(`verify_pain_points` → `_quote_present_at_url`) and **Stage 5 BACKFILL**.

Substring is high-precision but **low-recall**: real supporting evidence is frequently *paraphrased*,
and the research shows lexical overlap trails NLI by ~18 ROC-AUC points on factual consistency. So a
genuinely-supported pain point whose cited quote is a paraphrase of the evidence sentence is **wrongly
dropped** today. E1 upgrades the primitive in place to **substring pre-filter → atomic-claim + NLI
entailment**, and reports **citation precision + recall**.

## Decisions locked (with Sean, 2026-06-30)

- **Cost model = local NLI, in-process.** $0 recurring; the in-process ONNX path has no model server,
  so the fleet's "asleep local host" failure mode never applies. (Rejected: per-claim OpenRouter judge
  = cost trap; subscription agent = interactive-only.)
- **Model = `cross-encoder/nli-deberta-v3-small`**, run via its pre-built **173 MB int8 ONNX**
  (`onnx/model_qint8_avx512_vnni.onnx`) on onnxruntime, CPU-only, Apache-2.0. 3-label NLI head
  (entailment / neutral / contradiction).
- **Optional dependency + graceful fallback.** onnxruntime + tokenizer are an **optional extra**;
  the model is downloaded by a setup script. If deps or model are absent, the gate **degrades to
  today's substring-only check with a one-time warning** — it never hard-fails a run.

## Architecture

### 1. The chokepoint cascade (`verify.py`)

Upgrade the primitive in place, adding an injected scorer:

```
quote_supported_at_url(*, cited_quote, fetched_text, scorer=None) -> bool
```

Decision cascade, per atomic claim:
1. **Substring pre-filter** — if the claim is a substring of `fetched_text` (today's lowercased check)
   → **ACCEPT**. Fast, high-precision.
2. **NLI residual** — else, if `scorer` is available, compute
   `scorer.entails(premise=fetched_text, hypothesis=claim)` → **ACCEPT iff** entailment is the argmax
   label **and** its probability ≥ `τ` (default 0.5, module constant).
3. **Graceful fallback** — if `scorer is None`, the NLI branch is skipped (substring-only), and a
   one-time `logging.warning` records that the gate is degraded.

**Hard invariant (recall safety):** substring may only ever **ADD** an accept — it must **never reject**.
Every substring-miss falls through to the NLI branch (or, when degraded, to a reject *only because NLI
is unavailable*, exactly as today). This is the load-bearing rule from the research: substring-only
would systematically false-negative paraphrased support.

**Atomic-claim decomposition:** split `cited_quote` into sentences with the existing `_SENT`-style
regex; the quote is supported **iff every sentence** passes the cascade (AND semantics). Cited quotes
are usually a single sentence, so this is normally one check; it future-proofs multi-sentence claims.

`_quote_present_at_url` and `verify_pain_points` thread the optional `scorer` through unchanged in
behavior when `scorer is None`.

### 2. NLI scorer module (`council/discovery/nli.py`) — new

- `class NliScorer` with `entails(premise: str, hypothesis: str) -> float` returning the entailment
  probability, plus `label_probs(...) -> dict` if useful internally. Loads the int8 ONNX via
  onnxruntime + a tokenizer; runs the cross-encoder forward pass in-process on CPU; softmaxes the
  3-label logits; maps the entailment index.
- `get_scorer() -> NliScorer | None` — lazy module-level singleton. Returns `None` (cached) on **any**
  failure: `ImportError` (onnxruntime/tokenizer absent), missing model file, or load error. This is the
  graceful-degradation seam the whole design leans on.
- **Model location:** a gitignored `tools/llm-council/models/nli-deberta-v3-small/` (mirrors the
  TTS `models/` pattern), overridable via env var `DISCOVERY_NLI_MODEL_DIR`.
- **Label index** for `cross-encoder/nli-deberta-v3-small` must be confirmed against the model card at
  build time (id2label) — do not hard-code without verifying; a wrong index silently inverts the gate.

### 3. Citation precision / recall (ALCE-style) — additive reporting

Computed in `verify_pain_points` over the run, reference-free, via the same scorer:
- **Recall** (per verified pain point): does the concatenation of its supporting evidence entail the
  cited claim? (1/0, averaged.)
- **Precision** (per citation): the remove-one-citation test — a citation is irrelevant iff it alone
  doesn't support the claim **and** the remaining citations still entail it.
- Surfaced in the pipeline **session JSON**: `citation_precision`, `citation_recall`, and
  `verify_mode: "nli" | "substring-only"`. A one-line honesty note in the ledger when degraded
  ("verification: substring-only — NLI model not loaded"). Never claims NLI when it didn't run.
- v1 may compute these only when the scorer is active; in degraded mode they're omitted/null.

### 4. Dependencies + setup

- `pyproject.toml`: add `[project.optional-dependencies] nli = ["onnxruntime", "tokenizers"]` (exact
  tokenizer dep TBD at build — `tokenizers` if we tokenize directly, else `transformers`). Base install
  stays light; CI/headless don't pull it.
- `scripts/install_nli_model.sh` (mirrors `agents-sdk/scripts/install_tts_models.sh`): downloads the
  173 MB int8 ONNX + tokenizer files from Hugging Face into the model dir. Idempotent.
- Document in `.claude/skills/fusion-discovery-council/SKILL.md` §6 (the gate) + CHANGELOG.

## Testing (hermetic — no model download in CI)

Dependency injection is the testability seam. Unit tests pass a **deterministic fake scorer**:

- substring fast-accept (NLI never consulted)
- NLI accept on a paraphrase (substring miss → fake scorer returns high entailment)
- NLI reject on unsupported claim (fake scorer returns low entailment / neutral argmax)
- **substring-never-rejects** invariant (a substring hit accepts even if the fake scorer would reject)
- `scorer=None` → exact substring-only behavior of today (all existing verify tests stay green)
- sentence-split AND semantics (one entailed + one not → reject)
- ALCE precision/recall math on a small fixture
- `verify_mode` surfaced correctly in the session JSON for both active and degraded
- One real-model integration test behind a skip-marker (`@pytest.mark.skipif(model_absent)`) that loads
  the actual ONNX if present — never required for the suite to pass.

`nli.py`'s `get_scorer()` returning `None` on ImportError is itself unit-tested by simulating the
missing dependency.

## Out of scope (v1)

- Enriching the NLI premise beyond the stored `rec.quote` (single extracted sentence) with fuller page
  context — a later optimization; v1 uses what the bundle already keeps.
- Wiring precision/recall into the rendered card UI beyond the one-line mode note.
- Threshold tuning on a labeled benchmark — ship a sane default `τ`; tuning is a follow-up.

## Success criteria

- A paraphrased-but-genuinely-supported pain point that substring drops today is **accepted** when the
  NLI scorer is active.
- A fabricated/unsupported claim is still **rejected** (precision preserved).
- With no model/deps present, the suite passes and discovery runs exactly as today (substring-only),
  with a visible degraded-mode note.
- `cd tools/llm-council && uv run pytest tests/ -q` green; `python3 scripts/validate.py` PASS.
