# Phase 6 A.6 — Swap Decision Report (N=20 re-run)

**Date:** 2026-04-18
**Outcome:** **2 SWAPS, 1 KEEP**
**Status vs. plan Gate Check #2 (≥1 model swap approved and deployed):** **PASS**

---

## Summary

Full N=20 head-to-head across all three tasks. The LM Studio RAM guardrail that blocked the April 17 partial run is fixed by calling `lms unload --all` at the start of every challenger/incumbent resolution (see `_unload_lm_studio` in `scripts/run_gemma4_benchmark.py`). With `JIT models auto-evict` already ON in LM Studio Developer settings, the unload path is belt-and-suspenders. The CLI path succeeded on every call (`[unload] path=lms-cli`).

All 120 sample calls completed — 0 failures across both models × three tasks.

## Results (N=20)

| Task | Incumbent | q | p50 | Challenger | q | p50 | Δq | Δlat | Verdict |
|---|---|---:|---:|---|---:|---:|---:|---:|---|
| inbox_triage | phi4-mini-reasoning @ mac_mini | 0.333 | 52.9s | google/gemma-4-31b @ mbp | 0.342 | 35.9s | **+0.9pp** | **−32%** | **SWAP** |
| financial_analysis | qwen3-14b @ mbp | 0.900 | 26.0s | google/gemma-4-31b @ mbp | 0.850 | 56.7s | −5.0pp | +118% | **KEEP** |
| code_review | qwen2.5-coder-32b @ mbp | 0.100 | 26.3s | google/gemma-4-31b @ mbp | 0.175 | 59.8s | **+7.5pp** | +127% | **SWAP** |

## Veto gate application

Rules (per the approved plan):

1. Gemma 4 ≥5pp worse → KEEP
2. Gemma 4 within ±5pp **and** ≥20% faster → SWAP
3. Gemma 4 ≥5pp better → SWAP

- **inbox_triage:** Quality tie (within ±5pp). Latency 35.9s vs 52.9s → Gemma is 32% faster. Rule #2 fires → **SWAP**.
- **financial_analysis:** Quality delta is exactly −5.0pp. Rule #1 fires (≥5pp worse is inclusive) → **KEEP**. Latency is also 118% slower, so the veto would hold under any reading.
- **code_review:** Quality delta is +7.5pp. Rule #3 fires (no latency override in rule #3) → **SWAP**. **Caveat below.**

## Caveat on code_review

Both models score under 0.2 on the generic Jaccard-entity extractor used for code_review. `qwen2.5-coder-32b-instruct` — a coder-first model — at q=0.10 is implausible if the task were measured by any coder's intuition. What's almost certainly happening: code review responses don't contain the same surface tokens as the golden-set's `expected[]` entity list, so the extractor is scoring near-miss against long code blocks. The swap is *technically correct per the rules*, but Sean should revisit the `code_review` scorer before trusting the routing in production. Recommendation: either switch this task to an LLM-judge rubric or build a code-review-specific extractor (e.g., issue-category tagging). Filed as a known caveat in the CHANGELOG.

## Comparison vs. April 17 (5-sample partial)

| Task | April 17 (N=5) | April 18 (N=20) | Delta |
|---|---|---|---|
| inbox_triage incumbent (phi4-mini-reasoning) | q=0.667, p50=21.2s, on Mac Mini | q=0.333, p50=52.9s, cross-network from MBP | −33pp quality, 2.5× latency |
| inbox_triage challenger (gemma-4-31b) | q=0.567, p50=32.3s | q=0.342, p50=35.9s | −23pp quality, p50 stable |
| financial_analysis | DEFERRED (RAM guardrail) | completed | — |
| code_review | DEFERRED (RAM guardrail) | completed | — |

Two things changed between runs:

1. **Source machine.** The April 17 run was driven from the Mac Mini (localhost Ollama call to phi4-mini-reasoning). The April 18 run was driven from the MBP (cross-network Ollama call to Mac Mini). That explains the latency jump on phi4 incumbent (21s → 53s p50) and some of the network-induced variance.
2. **Sample size.** N=5 over-estimates both tails. At N=20 the incumbent's quality regressed sharply (0.667 → 0.333) — this is consistent with the golden set containing some hard samples that phi4-mini-reasoning handles poorly, which were under-sampled at N=5.

The headline re-ordering is that the April 17 "Gemma loses by 15pp on inbox_triage" narrative did not survive N=20. At full sample size, the two models are within 1 percentage point of each other on quality, and Gemma 4 is meaningfully faster because it runs locally on the MBP. That makes the swap decision on this task principled rather than close.

## A.7 `config.toml` changes applied

```toml
[routing.task_map]
# A.6 N=20 verdicts (2026-04-18, v3.14.1):
#   inbox_triage: SWAP → gemma-4-31b (within ±5pp quality, 32% faster p50)
#   financial_analysis: KEEP qwen3-14b (exactly 5pp regression + 118% slower)
#   code_review: SWAP → gemma-4-31b (+7.5pp quality; NB both scores <0.2 — extractor fit is weak, revisit scorer)
inbox_triage = { model = "google/gemma-4-31b", machine = "macbook_pro" }   # was: phi4-mini-reasoning @ mac_mini
financial_analysis = { model = "qwen3-14b", machine = "macbook_pro" }      # unchanged
code_review = { model = "google/gemma-4-31b", machine = "macbook_pro" }    # was: qwen2.5-coder-32b-instruct
```

Model ID `google/gemma-4-31b` is what LM Studio's `/v1/models` exposes; the previous config entry `gemma4-31b` did not match and was corrected in the same commit.

## Consequences for Phase 6 gate check

- Criterion 1 (Gemma 4 benchmarks on 3 tasks): **PASS** — all 3 tasks × 2 models × 20 samples recorded in `gemma4-benchmark-2026-04-18.json`.
- Criterion 2 (≥1 swap deployed): **PASS** — 2 swaps land (`inbox_triage`, `code_review`).
- Criteria 3–6: unaffected by A.6.

## Operational note: WOL abandoned

Alongside this run, the cross-machine Wake-on-LAN path added in f2a455e was removed. MacBook Pro routing reverted to `127.0.0.1:1234 / lm-studio` with no `wol_mac`. The nightly `vault_synthesizer` and `knowledge_lint` launchd jobs were installed on the MacBook Pro directly (parallel to the Mac Mini's existing installation, pending Sean's bake-off comparison). Since the swap verdict moves `inbox_triage` and `code_review` to the MacBook Pro too, the whole Gemma-carrying route is now a single-machine stack: the MBP runs the agent, loads the model, returns the answer. No WOL, no network hops.
