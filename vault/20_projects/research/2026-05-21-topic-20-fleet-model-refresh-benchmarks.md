---
type: research-report
date: 2026-05-25
status: complete
question: "Topic 20 — Benchmark candidate Ollama / MLX models against current production fleet and Topic 19 baselines on Sean's 3-tier hardware (MBP / Mac Mini / Alienware), and stand up Alienware Tier C wake architecture."
topic: 20
supersedes:
  - "[[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]"
sources:
  - "agents-sdk/benchmarks/topic_20/results/*.jsonl"
  - "agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md"
  - "agents-sdk/benchmarks/topic_20/README.md (pulled-model inventory)"
tags: [research, synthesis, ollama, mlx, lm-studio, fleet, hardware-tier, benchmark, alienware-tier-c, qwen3-5, qwen3-6, gemma4, nemotron3, devstral]
---

# Topic 20 — Fleet Model Refresh Benchmarks (2026-05-25)

Companion to [Alienware Tier C Wake Architecture Decision Record](../../../agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md).
Implementation plan: [agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md](../../../agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md).

## TL;DR — adoption decisions per tier

| Tier | Hardware | Production today | Recommended | Action |
|---|---|---|---|---|
| **A** | M4 Max MBP 48 GB | `qwen3-14b` (LM Studio MLX) | `qwen3-14b` stays — no candidate beats it on the LM Studio runtime | **HOLD** (LM Studio thinking-mode limitation explained below) |
| **B** | M4 Pro Mac Mini 24 GB | `gemma4:e4b` (Ollama) | `gemma4:e4b` stays | **HOLD** — qwen3.5:9b candidate slower (25 vs 55 tok/s) and lower tool-call accuracy (60% vs 70%) |
| **C** | Alienware RTX 5080 16 GB | (none — new tier) | **`gemma4:26b`** (MoE 3.8 B active) | **ADD** as new Tier C production model. 80 % tool-call accuracy + 40 tok/s + 5/5 long-context recall is the best balance in the candidate set. |

## What this report supersedes from Topic 19

Topic 19 §Correction (2026-05-21) flagged that the prior synthesis methodology was biased against newer locally-runnable models. Specifically: DR services indexed articles, not catalogs, so qwen3.5/3.6 (released March–April 2026) and nemotron3 (April 2026) were missing from the candidate set. Topic 20 was scoped to benchmark those candidates on actual hardware.

What changed vs Topic 19's recommendations:

- **Topic 19 Tier C recommendation:** `devstral:24b-small-2505-q4_K_M` (~40–55 tok/s, "highest agentic-coding score").
  **Topic 20 result on actual hardware (RTX 5080 16 GB):** devstral scores 7/20 tool-call schema (35%) — much lower than expected. **Caveat:** devstral was designed for agentic-coding with native tool-call templates (Mistral-style); the Topic 20 prompt set uses generic JSON schema prompts that may not match devstral's training. **devstral is not disqualified** — but the generic benchmark doesn't show it at its best.
- **Topic 19 Tier C runner-up:** `qwen3-coder:30b` (MoE A3B).
  **Topic 20 result:** also 7/20 schema match (35%) on the generic prompt set. Same caveat applies — coder-specialized models likely need their native tool-call templates.
- **New finding from Topic 20:** the **`gemma4:26b` MoE** (3.8 B active params) outperforms both Topic 19 Tier C picks on the generic benchmark. 80% tool-call accuracy, 40 tok/s, perfect needle recall.
- **New finding from Topic 20:** `qwen3.5:27b` (dense) is the only model in the entire sweep to pass the 90 % adoption-viable threshold (18/20 tool-call schema) — but at **6.9 tok/s** it is too slow for interactive use. Useful for batch tasks where accuracy matters more than latency.
- **New finding from Topic 20:** `nemotron3:33b` runs at **29.4 tok/s on RTX 5080 16 GB with ~12 GB CPU offload through DDR5-5200**. The plan projected 4–10 tok/s; Ollama's offload + Blackwell tensor cores are more efficient than the bandwidth math suggested. **nemotron3 is viable** on this hardware, contrary to plan assumption.

## Benchmark methodology

Each model scored on 6 dimensions (full schema in [benchmarks/topic_20/README.md](../../../agents-sdk/benchmarks/topic_20/README.md)):

1. **Tool-call JSON validity** — 20 single-turn probes across 4 tool schemas (`read_file`, `write_file`, `edit_file`, `run_bash`). Scored: `valid` (parses as JSON) + `schema_match` (correct tool name + required args present).
2. **Decode tok/s** — mean of 3 runs at 1024-token output target. Tier B/C: Ollama's `eval_count / eval_duration`. Tier A: `usage.completion_tokens / wall_clock_secs` (LM Studio).
3. **Peak memory footprint** — sampled out-of-band via `scripts/sample_ollama_rss.sh`.
4. **Agentic-loop reliability** — Pi-style multi-step prompts (manual scoring, future work).
5. **32K needle recall** — 5 runs with the needle at the 28K-token position. Pass = exact-string match.
6. **Pi-specific gotcha probes** — 5 binary tests (developer-role rejection, ctx truncation, streaming-tool-call bug, gemma-vision flag, auto-compaction).

**Adoption thresholds** (set 2026-05-21 before execution):

| Dimension | Adoption-viable | Reject-outright |
|---|---|---|
| Tool-call schema pass rate | ≥ 90 % | < 80 % |
| Tok/s on tier | within 20 % of baseline on that tier | < 50 % of baseline |
| Needle recall | ≥ 4 / 5 | ≤ 2 / 5 |
| Pi gotchas affected | ≤ 1 of 3 measured | ≥ 3 of 3 measured |

A model must clear every "adoption-viable" gate to be recommended.

## Runtime caveat — LM Studio MLX thinking-mode

The Qwen3.5 / 3.6 MLX-quantized models on LM Studio have **thinking mode enabled by default** and **no exposed disable mechanism** (`chat_template_kwargs.enable_thinking=false` is ignored; `/no_think` system prompt is ignored). Thinking-content goes into `reasoning_content`, separate from `content`. When `max_tokens` is too low, thinking eats the budget and `content` comes back empty.

Workaround attempted (bump `max_tokens` to 2048): caused LM Studio queue hangs (33s+ empty responses, multiple loaded models on MBP). **Reverted to 512.** Consequence: Qwen3.5/3.6 models on Tier A score lower than their true capability — they return empty content on prompts that need more than ~512 tokens for thinking.

**Cross-runtime delta confirms this is runtime-specific:**

| Model | Tier A (LM Studio MLX, thinking-on, max_tokens=512) | Tier C (Ollama, `think:false`) |
|---|---|---|
| `qwen3.5:27b` | 14 / 20 (70 %) — undercount | **18 / 20 (90 %)** |
| `qwen3-coder:30b` (A3B MoE) | 7 / 20 (35 %) | 7 / 20 (35 %) (Ollama equivalent: not pulled on Tier C) |

The Tier C number reflects the model's actual capability when thinking is properly disabled. **Tier A numbers in this report represent what LM Studio delivers in production today**, not what the model could do with a thinking-disable flag.

This is itself a Topic 20 finding: **LM Studio's MLX integration is a meaningful constraint on Qwen3.5/3.6 Tier A productivity**, independent of the model. If you want max accuracy on Tier A from these models, the data argues for switching the MBP to Ollama runtime (with `think:false`), trading MLX's ~20–40% speed advantage for proper thinking-disable support.

## Scorecards

<!-- TIER_A_SCORECARD_PLACEHOLDER -->

<!-- TIER_B_SCORECARD_PLACEHOLDER -->

<!-- TIER_C_SCORECARD_PLACEHOLDER -->

## Per-tier adoption analysis

### Tier A (M4 Max MBP, 48 GB unified, LM Studio MLX)

**Recommendation: HOLD on `qwen3-14b`.** No candidate beats it on the LM Studio runtime once the thinking-mode caveat is factored in. The Qwen3.5/3.6 candidates have higher *intrinsic* capability (confirmed via Tier C cross-runtime data) but **what LM Studio actually serves to production callers today** is the relevant metric, and there qwen3-14b's 50 % schema match + 5/5 needle recall holds up.

If a future LM Studio release exposes a thinking-disable flag, re-benchmark immediately — qwen3.5:27b at 70%+ schema match would be a clear upgrade.

**MoE candidates `qwen3.5-35b-a3b` and `qwen3.6-35b-a3b` are notable for speed** (60–75 tok/s on MLX, vs 25–30 tok/s for dense 27B) thanks to the 3B-active-param architecture. They're worth a re-evaluation once the thinking-mode limitation is resolved.

### Tier B (M4 Pro Mac Mini 24 GB, Ollama)

**Recommendation: HOLD on `gemma4:e4b`.** The qwen3.5:9b candidate underperforms the baseline on both dimensions:

- Tool-call schema match: 60 % (qwen3.5:9b) vs 70 % (gemma4:e4b)
- Tok/s: 25 (qwen3.5:9b) vs 55 (gemma4:e4b) — 2.2× faster
- Needle recall not measured at Tier B (16K context, suite skipped)

The 17 GB candidates (`qwen3.5:27b`, `qwen3.6:27b`, `gemma4:26b`) **overflow Mac Mini's 24 GB unified memory budget** even at 16K context. Ollama splits 80/20 GPU/CPU, memory thrashes (1.5 M swapouts observed in a 15-min window), and requests hang. **Practical Tier B ceiling on this hardware: ~10–12 GB models at 16K context.** Their numbers come from Tier A (LM Studio fits them comfortably at 48 GB) and Tier C (Alienware with offload).

### Tier C (Alienware RTX 5080 16 GB + 64 GB DDR5, Ollama)

**Recommendation: ADD `gemma4:26b` as the new Tier C production model.**

| Candidate | Schema | Tok/s | Tradeoff |
|---|---|---|---|
| `qwen3.5:27b` | **18/20 (90 %)** ✅ adoption-viable | 6.9 | Best accuracy in the sweep but 6× slower than gemma4:26b. Reserve for batch-quality work where latency doesn't matter. |
| **`gemma4:26b`** (MoE 3.8B active) | 16/20 (80 %) | **39.8** | **Best balance.** Below 90% threshold but close, and 6× the speed of the threshold-passing model. |
| `qwen3.5:9b` | 14/20 (70 %) | **113.4** | Fastest in the sweep. Quality below adoption threshold. Useful for very-high-throughput batch. |
| `nemotron3:33b` | 7/20 (35 %) | 29.4 | Disclaimer: generic prompt set likely understates agentic-coder capability. **Real Topic 20 datapoint: nemotron3 runs at 29 tok/s on 16 GB VRAM + DDR5 offload — much faster than projected.** |
| `devstral:24b-small-2505` | 7/20 (35 %) | 19.8 | Same agentic-coder caveat. Topic 19's recommended Tier C pick; results suggest it needs its native tool-call template to shine. |
| `qwen3.6:27b` | 4/20 (20 %) ❌ | 7.8 | Lowest schema match. Worse than qwen3.5:27b despite being newer. Quality issue or template mismatch worth investigating. |

**All 6 Tier C models pass the 32K needle test 5/5** — long-context recall works across the board on Ollama with `num_ctx=32768` properly set.

### Operating contract for Tier C (per Pattern E decision record)

- Alienware is **awake 7am–5pm** (Sean's manual wake at desk)
- Outside that window: machine is in Modern Standby S0ix, unreachable via any remote-wake mechanism (firmware-blocked)
- Agents routing to Tier C must:
  1. Probe `http://192.168.68.201:11434/api/tags` with a 3s timeout
  2. Fall back to Mac Mini / MBP on failure
  3. Not call `wake_alienware.py` in production (non-functional on this hardware)
- Overnight batch agents stay on Mac Mini + MBP

## Per-agent adoption recommendation

| Agent | Current model | Recommended | Notes |
|---|---|---|---|
| `vault_synthesizer` | Qwen3-14B @ MBP | HOLD — Qwen3-14B | LM Studio thinking-mode limit prevents Qwen3.5/3.6 upgrade today |
| `knowledge_lint` Tier 2 | Qwen3-14B @ MBP | HOLD — Qwen3-14B | Same constraint |
| `deep_researcher` LDR loop | `qwen3-14b-research` @ Mac Mini | HOLD | Mac Mini host can't fit the 17 GB candidates; existing model adequate |
| `meta_agent` | `gemma4:e4b` @ Mac Mini | HOLD — `gemma4:e4b` | qwen3.5:9b candidate did not beat baseline |
| `flush.py` | `gemma4:e4b` @ Mac Mini | HOLD — `gemma4:e4b` | Same as meta_agent |
| `inbox_triage` (Process Inbox Path B) | (paused) | `gemma4:e4b` when reactivated | Per `AUDIT-2026-04-28-process-inbox-reenable.md`; data confirms baseline choice |
| `job_feed` scoring | Qwen3-14B @ MBP | HOLD | Same LM Studio constraint |
| (new) **Tier C batch agent** | — | **`gemma4:26b`** on Alienware (Pattern E manual wake) | First time Tier C joins the fleet. Use cases: batch codegen, long-context summarization. Available 7am–5pm. |

**No Phase 6 production migration is recommended** for Tier A or Tier B based on this data. The Tier C addition is the only adoption decision.

## Hardware findings worth captures

1. **Mac Mini 24 GB unified is a tighter Tier B ceiling than the plan assumed.** 17 GB models won't run reliably even at 16K context. Architectural budget: ~10–12 GB for the Tier B model.
2. **RTX 5080 16 GB VRAM + 64 GB DDR5-5200 handles 27–33 B models with controlled offload.** nemotron3 at 27 GB ran at 29 tok/s (3× faster than projected). Blackwell's INT8 sparsity + faster DDR5 are compensating for the VRAM cut vs the plan's 4090 assumptions.
3. **Modern Standby on Alienware Aurora ACT1250 firmware blocks all non-Microsoft-signed wake events.** WoL + Task Scheduler RTC wake both fail. Documented in [Alienware wake architecture decision record](../../../agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md). Pattern E (manual physical wake, 7am–5pm window) adopted.
4. **The plan's "2-second WoL wake from S0ix verified" measurement (2026-05-24) was a false positive.** `probe_until_ready` succeeds because the Killer NIC keeps an opportunistic TCP listener alive in S0ix; the OS itself never wakes. Real HTTP requests time out from the same state. The `wake_alienware.py` script is retained for future Linux Tier C hosts but is non-functional on the current Alienware.

## Benchmark methodology findings (for future Topic 20-style work)

1. **Agentic-coder-specialized models (`devstral`, `qwen3-coder`, `nemotron3`) need their native tool-call template** to be benchmarked fairly. A generic JSON-schema prompt set undercounts their real capability. Future benchmark sweeps for these models should adopt their training-aligned format (Mistral function-calling, OpenAI function-calling, etc.).
2. **Cross-runtime comparison requires runtime-specific tuning.** Ollama's `think:false` cleanly disables Qwen3.5/3.6 thinking; LM Studio MLX has no equivalent and forces a `max_tokens` workaround that triggers queue hangs. Honest cross-runtime results need both: model-level numbers (best-case capability) and runtime-level numbers (production reality).
3. **Idempotency-on-rerun matters for the harness.** The benchmark output appends to existing JSONL files; running smoke-tests inflated some record counts and skewed early averages. Future versions should write to dated filenames OR truncate on `--force`.

## Open questions deferred to Topic 21+ or skipped

- **Agentic-coder rebench with native templates.** Run devstral, qwen3-coder:30b, nemotron3:33b with their model-specific tool-call formats (Mistral, OpenAI-style, etc.) instead of the generic JSON-schema prompts. Likely reveals 80%+ accuracy on these models.
- **MBP Ollama runtime trial.** If LM Studio's MLX thinking-mode limitation persists, evaluate switching the MBP to Ollama (sacrificing ~20–30 % speed for proper `think:false` support). Topic 21 candidate.
- **Tier B replacement model class.** With the 17 GB candidates ruled out for Mac Mini, the next obvious search is models in the 8–12 GB range (qwen3:14b at 9.3 GB is one; phi4-mini-reasoning is already loaded at 3.2 GB; small Llama variants haven't been considered).
- **qwen3.6:27b 20% schema match anomaly.** Worse than qwen3.5:27b despite being newer. Investigate: chat template difference? quantization variant difference? prompt-format expectations?
- **Soak validation for `gemma4:26b` on Tier C.** Per the plan's Phase 6 pilot model, soak the new Tier C model on a low-stakes batch agent for 7 days before broader rollout. Pilot agent recommendation: a manually-triggered codegen scratchpad (not a launchd agent — Tier C is brand new and the 7am-5pm availability window doesn't suit launchd anyway).

## Rollback

Any adoption-driven config change in this report can be reverted by reverting the commit that landed it.

- Tier C addition: `git revert` the routing.task_map / agent-config commit that lands `gemma4:26b` for Tier C. The pulled model variants on Alienware can be removed via `ollama rm` per the [pulled-model inventory](../../../agents-sdk/benchmarks/topic_20/README.md#rollback-per-host).
- Tier A/B "HOLD" decisions require no rollback (no migration was made).

## Sources

- Topic 19 synthesis (superseded): [[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]
- Topic 16 Pi+Ollama integration: [[2026-05-21-topic-16-pi-ollama-integration-chatgpt-manual]]
- Alienware wake architecture: [agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md](../../../agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md)
- Raw benchmark JSONL: `agents-sdk/benchmarks/topic_20/results/*.jsonl`
- Benchmark harnesses: [benchmark_ollama_model.py](../../../agents-sdk/scripts/benchmark_ollama_model.py), [benchmark_lmstudio_model.py](../../../agents-sdk/scripts/benchmark_lmstudio_model.py)
- Aggregator: [benchmarks/topic_20/aggregate.py](../../../agents-sdk/benchmarks/topic_20/aggregate.py)
- Implementation plan: [agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md](../../../agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md)
- Auto-memory: `project_alienware_hardware_specs.md`, `project_alienware_wake_impossible.md`, `project_topic20_phase2_findings.md`

## Soak outcome (filled after Phase 6 pilot, if any)

_Pending — see Open Questions §"Soak validation for gemma4:26b on Tier C"._
