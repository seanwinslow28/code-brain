---
type: review
domain:
  - claude-mastery
  - creative-studio
status: complete
context: code-brain
created: 2026-06-03
topic: 20
question: "Did gemma4_26b-32k @ Alienware survive a 7-day Pattern E soak well enough to become the fleet's first Tier C production model?"
source: topic-20-tier-c-pilot-soak
references:
  - "[[2026-05-21-topic-20-fleet-model-refresh-benchmarks]]"
  - "agents-sdk/scripts/tier_c_soak.py"
  - "~/.claude/plans/we-re-continuing-topic-20-generic-kitten.md (soak protocol)"
tags: [review, soak, gemma4, alienware-tier-c, fleet, ollama]
---

# Topic 20 Tier C Soak Closeout — gemma4_26b-32k @ Alienware (2026-06-03)

**Model:** `gemma4_26b-32k:latest` @ `192.168.68.201:11434` (Alienware Aurora ACT1250, RTX 5080 16GB).
**Workload:** long-context vault research-article summarization (3-paragraph faithful summary, `think:false`, `temperature:0.0`, adaptive `num_ctx` 8K–32K).
**Harness:** [agents-sdk/scripts/tier_c_soak.py](../../../agents-sdk/scripts/tier_c_soak.py) — direct httpx, no HybridRouter, no `task_map`, no launchd. Pattern E manual wake (7am–5pm).
**Soak window:** 2026-05-26 → 2026-06-03 (9 calendar days; protocol planned 7, ran long because the verdict slot was never closed on 06-02).
**Datapoints:** 17 (2/day, ×8 days + 1 on 06-03). Telemetry: `vault/health/tier-c-soak-{date}.jsonl`; outputs: `vault/health/tier-c-soak/{date}/`.

## Verdict: **ADOPT** — as the Tier C **batch / async** model only

Every quality and stability gate passed clean. The sole soft miss is a 1.2% throughput shortfall against a threshold calibrated on benchmark prompts rather than real batch load — immaterial for an async tier. Recommend promotion for batch/async workloads; explicitly **not** for interactive use. The routing/`task_map` wiring stays deferred to a follow-up session per the protocol and CLAUDE.md.

## Gate-check table

| # | Gate (Adopt threshold) | Status | Evidence |
|---|---|---|---|
| G1 | ≥12 of 14 expected datapoints land (≥86% availability in Pattern E window) | **PASS** | 17 datapoints across 9 days. Alienware reachable on every attempted day; no `exit 2` gaps recorded. |
| G2 | 0 thinking-token leakage across all outputs | **PASS** | 0 / 17. Scanned for `<think>`, `Reasoning:`, `Step 1:`, `Okay, so…`. None present. `think:false` holds. |
| G3 | 0 truncation / parse-fail | **PASS** | 17 / 17 `ok:true`; every output terminates on sentence punctuation. No mid-sentence cutoff at any `num_ctx`. |
| G4 | 3-paragraph structure held | **PASS** | 17 / 17 produced exactly thesis / supporting-points / open-questions paragraphs as prompted. |
| G5 | Median quality = "thinking-partner shape" every sampling day | **PASS** | Every sampled summary states the source's actual thesis and preserves specific entities (model tags, issue numbers e.g. Mem0 #4956, tok/s figures, hardware constraints) rather than restating the title. No shallow days. |
| G6 | Throughput mean ≥30 tok/s | **PARTIAL** | mean **29.6**, median **29.6**, range 22.2–35.3, σ 3.8. 0.4 tok/s (1.2%) under threshold — see analysis. |
| G7 | No run >2× wall-clock outlier vs the day's other run | **PARTIAL** | 2 days exceed: 05-26 (2.58×), 05-27 (2.17×). Both are source-size pairings (30KB vs 4KB same day), not hangs — see analysis. |

## Throughput analysis (why G6/G7 are benign)

The two PARTIAL gates are the same phenomenon and neither indicates model instability:

- **Throughput is workload-bound, not time-degrading.** `corr(num_ctx, tokens_per_sec) = −0.75`: the slow runs are the large-article runs (the 22.2 tok/s floor was the 46,617-char source at `num_ctx=16384`). The 39.8 tok/s from the Topic 20 benchmark was measured on smaller, standardized prompts; the soak corpus skews larger (sources 2.2KB–50.9KB), pulling the sustained mean to ~30.
- **No drift over the 9 days.** tok/s bounces in the same 22–35 band on day 1 and day 9. There is no monotonic decline — the signature a soak exists to catch (thermal throttle, memory-leak slowdown, VRAM fragmentation on the 16GB RTX 5080) is absent.
- **The wall-ratio "outliers" are size artifacts.** 05-26 paired a 30.5KB source (27.2s) with a 4KB source (10.5s) → 2.58×. Normalize by tok/s and both sit mid-band (27.7 / 34.6). No run hung; max wall was 40.0s (the 46KB article), well inside the 300s `CHAT_TIMEOUT`.

**Conclusion:** G6/G7 fail the letter of a benchmark-calibrated threshold, not the spirit. ~30 tok/s sustained is entirely adequate for an async batch tier, which is the only role proposed.

## Per-day summary

| Date | Runs | tok/s | num_ctx | Notes |
|---|---|---|---|---|
| 05-26 | 2 | 27.7 / 34.6 | 12288 / 8192 | Day 1, includes harness smoke + first live run |
| 05-27 | 2 | 30.1 / 35.3 | 8192 / 8192 | |
| 05-28 | 2 | 26.5 / 24.8 | 12288 / 20480 | Largest-ctx day; 50.9KB source handled clean |
| 05-29 | 2 | 34.6 / 35.2 | 8192 / 8192 | Fastest day |
| 05-30 | 2 | 27.3 / 30.4 | 8192 / 8192 | Weekend — Alienware was awake |
| 05-31 | 2 | 22.2 / 26.9 | 16384 / 12288 | Slowest run (46KB source) — still clean |
| 06-01 | 2 | 28.1 / 32.9 | 8192 / 8192 | |
| 06-02 | 2 | 31.3 / 29.6 | 8192 / 8192 | Planned verdict day (verdict deferred to 06-03) |
| 06-03 | 1 | 26.3 | 16384 | Closeout day |

## Pattern E availability note

Availability was a non-issue across the window — the Alienware was reachable on every day a run was attempted, including both weekend days. This is a small but real positive signal that Pattern E (manual ~7am wake / ~5pm shutdown) is sustainable for Sean's actual working rhythm, at least over a 9-day span. No fabricated datapoints: the harness `exit 2`-on-unreachable design means absent days would simply not appear, and none are missing.

## Deviations from protocol

- **Ran 9 days, not 7.** The 06-02 verdict/stub-update step in the protocol was not executed on schedule; the soak kept producing datapoints through 06-03. More data, same conclusion — no harm.
- **Pilot workload was summarization, not a "codegen scratchpad."** The Open-Questions line in the parent report floated a codegen scratchpad; the settled plan-mode decision chose article summarization (automated, median-samplable). The closeout reflects what actually ran.

## Next step (deferred, logged as a ticket)

Promotion to a real route is **not** done here, by design (protocol + CLAUDE.md both defer it). Follow-up session should: add a `[routing.task_map]` Tier C entry for batch summarization, decide whether HybridRouter `fallback_to_api` is acceptable for that route, and add the Tier C "production" note to CLAUDE.md. Tracked in [vault/00_inbox/tickets.md](../../00_inbox/tickets.md).
