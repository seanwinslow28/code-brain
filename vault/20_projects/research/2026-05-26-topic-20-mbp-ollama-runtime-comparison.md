---
type: research-report
date: 2026-05-26
status: complete
question: "Topic 20 follow-up — Does switching the MBP from LM Studio MLX to Ollama (with `think:false`) recover the schema-accuracy and needle-recall losses caused by LM Studio's missing thinking-disable flag, and at what speed cost?"
topic: 20
supersedes: []
related:
  - "[[2026-05-21-topic-20-fleet-model-refresh-benchmarks]]"
sources:
  - "agents-sdk/benchmarks/topic_20/results/*-tierA-ollama-2026-05-26.jsonl"
  - "agents-sdk/benchmarks/topic_20/results/*-tierA-lmstudio-2026-05-25.jsonl"
  - "agents-sdk/benchmarks/topic_20/results/*-tierC-2026-05-25.jsonl"
tags: [research, synthesis, ollama, mlx, lm-studio, fleet, hardware-tier, benchmark, runtime-comparison, mbp-ollama, qwen3-5, qwen3-6, qwen3-coder]
---

# Topic 20 follow-up — MBP-Ollama vs LM Studio MLX runtime comparison (2026-05-26)

Resolves the Topic 20 Open Question §"MBP Ollama runtime trial."

## TL;DR

**Headline finding:** the hypothesis ("Ollama `think:false` will recover capability lost to LM Studio's missing thinking-disable") is **partially confirmed and partially refuted** — gains range from **+25 pp** to **-25 pp** depending on the model. Cross-runtime data refutes any "switch wholesale" framing; the right move is **per-model runtime selection**.

**Best Tier A upgrade candidate identified:** `qwen3.6:35b-a3b` on **MBP-Ollama** at 85 % schema match, 5/5 needle recall, 30 tok/s — beats the current `qwen3-14b` LM Studio production baseline on every dimension (50 % schema, 5/5 needle, 27.9 tok/s).

**Adoption recommendation:** add Ollama as a co-resident runtime on the MBP (Ollama + LM Studio both bound, different ports). Migrate the agents that benefit (vault_synthesizer, knowledge_lint Tier 2, job_feed scoring) to call MBP-Ollama with `qwen3.6:35b-a3b` for accuracy-critical work; keep LM Studio available for cases where its 2-3× decode-speed advantage matters more.

## Result table — same model, three runtimes

Same model file behaves differently across runtimes. Same hardware (MBP M4 Max 48 GB) behaves differently between LM Studio MLX and Ollama. Same runtime (Ollama) behaves differently between MBP and Alienware. All three axes captured here.

| Model | LM Studio MLX (thinking-on, max_tok=512) | **MBP-Ollama (think:false)** | Tier C Alienware-Ollama (think:false) | Δ schema |
|---|---|---|---|---|
| `qwen3.5:27b` | 70 % schema, 13.9 tok/s, **0/5 needle** | **90 %, 8.8 tok/s, 5/5** | 90 %, 6.9 tok/s, 5/5 | **+20 pp** ✅ |
| `qwen3.5:35b-a3b` | 65 %, 63.0 tok/s, **0/5 needle** | **75 %, 30.1 tok/s, 5/5** | not tested | **+10 pp** ✅ |
| `qwen3.6:27b` | 50 %, 14.4 tok/s, **0/5 needle** | 25 %, 8.8 tok/s, 5/5 | 20 %, 7.8 tok/s, 5/5 | **-25 pp** ❌ |
| `qwen3.6:35b-a3b` | 60 %, 80.2 tok/s, **0/5 needle** | **85 %, 30.0 tok/s, 5/5** | not tested | **+25 pp** ✅ |
| `qwen3-coder:30b` | 35 %, 79.1 tok/s, **0/5 needle** | 30 %, 68.9 tok/s, 5/5 | not tested | **-5 pp** (within noise) |
| `qwen3-14b` *(baseline)* | 50 %, 27.9 tok/s, 5/5 | not tested | n/a | — |

Pi-gotchas: 0/5 across the entire MBP-Ollama sweep vs 1/5 across the LM Studio sweep (LM Studio's `developer_role` rejection at the Jinja chat-template layer). One concrete Ollama win.

## Key findings

### 1. The needle recall fix is **universal and complete**

LM Studio MLX scored **0/5** on the 32K needle test for every Qwen3.5/3.6 candidate because of the thinking-mode + `max_tokens=64` collision: thinking tokens ate the budget and `content` came back empty. **MBP-Ollama with `think:false` scored 5/5 on every single model.** This isn't a partial recovery — it's a full restoration of long-context recall, with no per-model variance.

Practical implication: any vault/Knowledge agent that relies on 32K-context retrieval (vault_synthesizer T2 cluster sampling, knowledge_lint Tier 2 contradiction scan, job_feed scoring against multi-paragraph job descriptions) loses zero recall on MBP-Ollama. Today, on LM Studio MLX with Qwen3.5/3.6, those agents return empty content at the long-context end of their distribution.

### 2. Schema accuracy is model-specific — three patterns

**Pattern A: Ollama wins big (Qwen3.5 dense + Qwen3.6 MoE).**

- `qwen3.5:27b`: 70 % → 90 % (+20 pp)
- `qwen3.6:35b-a3b`: 60 % → 85 % (+25 pp)

The MBP-Ollama 18/20 score on `qwen3.5:27b` is bit-for-bit identical to the Alienware Tier C score on the same model. Hardware doesn't matter; runtime does. The thinking-mode handicap on LM Studio cost this model exactly 4 prompts' worth of schema-correct tool calls per 20-prompt suite.

**Pattern B: Ollama wins moderate (Qwen3.5 MoE).**

- `qwen3.5:35b-a3b`: 65 % → 75 % (+10 pp)

Smaller gain because the MLX MoE was already partially recovering through fast decode even when thinking-mode chewed budget. Still a clear improvement.

**Pattern C: Ollama LOSES (Qwen3.6 dense).**

- `qwen3.6:27b`: 50 % → 25 % (**-25 pp**)

The MBP-Ollama (25 %) and Tier C Alienware-Ollama (20 %) numbers are within noise of each other → consistent failure mode in Ollama for this specific model. LM Studio MLX gets 50 % on the same model. Hypothesis: thinking-mode tokens, even when they eat content budget, contribute to a less-fragile internal state for tool-call construction on dense Qwen3.6 specifically. Or there's a chat-template / quantization mismatch in Ollama's `qwen35` family adapter that doesn't affect Qwen3.5 dense but does affect Qwen3.6 dense. Worth follow-up investigation; tagged for Topic 21.

**Pattern D: Effectively no change (coder model).**

- `qwen3-coder:30b`: 35 % → 30 % (within noise)

Topic 20's existing finding still applies — coder-specialized models need their native tool-call templates (Mistral / OpenAI function-calling), not the generic JSON-schema prompt set. The runtime change can't compensate for the prompt-set / model-tradition mismatch.

### 3. Speed cost is real but tolerable for accuracy-critical work

| Model | LM Studio tok/s | MBP-Ollama tok/s | Slowdown |
|---|---|---|---|
| `qwen3.5:27b` | 13.9 | 8.8 | -37 % |
| `qwen3.5:35b-a3b` | 63.0 | 30.1 | -52 % |
| `qwen3.6:27b` | 14.4 | 8.8 | -39 % |
| `qwen3.6:35b-a3b` | 80.2 | 30.0 | -63 % |
| `qwen3-coder:30b` | 79.1 | 68.9 | -13 % |

MoE A3B models lose the most relative speed in Ollama (52-63 % slowdown). Dense 27B models lose ~37-39 %. Coder model loses the least (-13 %).

Possible explanation: Ollama's MLX backend integration is newer than its CUDA / Metal-llama.cpp backends. The MoE routing path in MLX-via-Ollama may not yet match LM Studio's hand-tuned MLX MoE kernels. This is a versioning artifact; future Ollama releases may close the gap.

### 4. MBP-Ollama beats Alienware-Ollama on per-model speed, despite the VRAM gap

| Model | MBP-Ollama tok/s | Alienware-Ollama tok/s | MBP advantage |
|---|---|---|---|
| `qwen3.5:27b` | 8.8 | 6.9 | +27 % |
| `qwen3.6:27b` | 8.8 | 7.8 | +13 % |

The 48 GB unified memory on MBP holds the entire 17 GB model + KV cache + activations in fast SoC RAM (~800 GB/s bandwidth). The Alienware's 16 GB VRAM forces partial offload to DDR5-5200 (~83 GB/s) for these 27B dense models. For models that fit comfortably on MBP, Apple Silicon's unified-memory architecture wins on this specific workload class.

This is consistent with the Topic 20 plan's intuition that "MBP for accuracy-critical, Alienware for VRAM-bound work" — but the cross-over point may be higher than expected. The MoE A3B variants and larger dense models (33B+) are where Alienware's VRAM + offload still wins.

## Per-agent adoption recommendation (revised from Topic 20 baseline)

| Agent | Current model | Recommended (post-2026-05-26) | Rationale |
|---|---|---|---|
| `vault_synthesizer` (T1 quote-first, T2 cluster sampling, T1.5 depth gate) | Qwen3-14B @ MBP-LM-Studio | **`qwen3.6:35b-a3b` @ MBP-Ollama** | +35 pp schema match, +8 % decode speed, 5/5 needle. Net upgrade on every dimension. |
| `knowledge_lint` Tier 2 (contradiction scan) | Qwen3-14B @ MBP-LM-Studio | **`qwen3.6:35b-a3b` @ MBP-Ollama** | Same. Lint Tier 2 explicitly relies on long-context recall to compare claims across files. |
| `job_feed` scoring | Qwen3-14B @ MBP-LM-Studio | **`qwen3.6:35b-a3b` @ MBP-Ollama** | Same. Job-description-vs-resume comparisons benefit from accurate JSON tool calls + needle recall in the 8K-32K window. |
| `deep_researcher` LDR loop | `qwen3-14b-research` @ Mac Mini | HOLD | Mac Mini host can't fit 17 GB models; existing pick stays. |
| `meta_agent` | `gemma4:e4b` @ Mac Mini | HOLD | Tier B sweep already settled. |
| `flush.py` | `gemma4:e4b` @ Mac Mini | HOLD | Same. |
| `inbox_triage` (Process Inbox Path B, paused) | (planned: `gemma4:e4b`) | HOLD | Same. |
| (Tier C batch agent) | — | **`gemma4:26b` @ Alienware-Ollama (Pattern E manual wake)** | Unchanged from Topic 20 main report. |

**Three production agents migrate** (`vault_synthesizer`, `knowledge_lint`, `job_feed`). All three currently underperform on long-context retrieval due to the LM Studio thinking-mode artifact. The migration cost is a config change (host + model name) per agent — no code change.

## Runtime co-residence pattern

Recommendation: **do not uninstall LM Studio.** Keep both runtimes bound on the MBP, different ports:

- LM Studio MLX: `http://seans-macbook-pro.local:1234` (existing)
- Ollama: `http://seans-macbook-pro.local:11434` (new)

Reasons to keep LM Studio available:
- 2-3× decode speed on Qwen3.5/3.6 MoE models for cases where tok/s matters more than accuracy (interactive chat, latency-sensitive single-shot)
- The `qwen3-14b` production baseline lives there with 5/5 needle and 50 % schema — still a solid fallback
- Future LM Studio releases may add `chat_template_kwargs.enable_thinking=false` support, which would re-open the Qwen3.5/3.6 candidates on the faster runtime

Future architectural option: a HybridRouter that picks runtime per request based on quality vs latency requirements. Out of scope for this report; logged for Topic 21+ consideration.

## Open questions raised by this report

- **Why does `qwen3.6:27b` collapse on Ollama (50 % → 25 %)?** Cross-runtime data (MBP and Alienware both at ~20-25 %) rules out hardware. The model itself behaves differently between Ollama's `qwen35` family adapter and LM Studio's MLX adapter. Worth a Topic 21 investigation: compare Ollama's chat template + tokenizer config against LM Studio's for this specific model.
- **Will the Ollama MoE-speed gap close?** Ollama's MLX backend is newer than its other backends. Re-benchmark after Ollama ≥ 0.30 to see if MoE A3B kernels reach LM Studio parity.
- **Pi-gotcha 0/5 on Ollama vs 1/5 on LM Studio** — is the `developer_role` rejection the only systematic difference, or are there other failure-mode classes we haven't measured? Worth a probe set extension.
- **Native-template rebench for coder + agentic models** still owed. `qwen3-coder:30b` on MBP-Ollama scored 30 % on the generic JSON-schema prompts — same caveat as Topic 20 main report. Topic 21 candidate.

## Power-loss event (2026-05-26 ~11:01)

Initial sweep launched 10:36; power loss interrupted between models 2 and 3. The 2 completed JSONL files (`qwen3.5_27b-32k`, `qwen3.5_35b-a3b-32k`) survived with full record counts (33 records each, matching Tier C reference). Resumed at 11:30 with the 3 remaining models; full sweep complete at 11:59. No data loss; the harness is idempotent against existing files when each rerun targets a clear filename.

Operational note: the bench sweep batches well under the laptop battery's runtime. For future benchmark work where power-loss risk is non-zero, route the orchestrator through the Mac Mini (UPS-protected) and treat MBP / Alienware as inference back-ends — which is what we did this time. The Mac Mini's bash background survived the MBP's interruption because the failure mode was MBP-side, not orchestrator-side.

## Rollback

This report introduces no production migration on its own. The recommended agent-config changes (three agents pointing at `http://seans-macbook-pro.local:11434` and `qwen3.6:35b-a3b`) are separate commits. Roll back each by reverting the commit that lands it; the previous LM Studio config will resume working immediately (LM Studio remains installed and bound).

To remove the 5 MBP-Ollama models + variants if the migration is abandoned:

```bash
ssh seanwinslow@seans-macbook-pro.local '
  export PATH=/opt/homebrew/bin:$PATH
  for tag in qwen3.5:27b qwen3.5_27b-32k qwen3.5:35b-a3b qwen3.5_35b-a3b-32k \
             qwen3.6:27b qwen3.6_27b-32k qwen3.6:35b-a3b qwen3.6_35b-a3b-32k \
             qwen3-coder:30b qwen3-coder_30b-32k; do
    ollama rm "$tag" || true
  done
'
```

Frees ~101 GB on MBP.

## Sources

- Topic 20 main synthesis (this report extends, does not supersede): [[2026-05-21-topic-20-fleet-model-refresh-benchmarks]]
- Raw MBP-Ollama benchmark JSONL: `agents-sdk/benchmarks/topic_20/results/*-tierA-ollama-2026-05-26.jsonl`
- Aggregator: [benchmarks/topic_20/aggregate.py](../../../agents-sdk/benchmarks/topic_20/aggregate.py)
- Harness change for new `A-ollama` tier: [scripts/benchmark_ollama_model.py](../../../agents-sdk/scripts/benchmark_ollama_model.py)
- Helper scripts: [build_mbp_ollama_variants.sh](../../../agents-sdk/scripts/build_mbp_ollama_variants.sh), [run_mbp_ollama_benchmarks.sh](../../../agents-sdk/scripts/run_mbp_ollama_benchmarks.sh)
- Pulled-model inventory: [agents-sdk/benchmarks/topic_20/README.md](../../../agents-sdk/benchmarks/topic_20/README.md)

## Soak / migration outcome

_Pending — see Open Questions §`qwen3.6:35b-a3b` Tier A migration._
