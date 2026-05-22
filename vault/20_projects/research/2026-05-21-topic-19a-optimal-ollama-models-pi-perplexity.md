---
type: research-report
date: 2026-05-21
question: "Topic 19 (source A — Perplexity) — Optimal Ollama model for Pi-driven coding + agentic workflows in 2026, ranked by RAM/VRAM tier: M4 Max MBP, M4 Pro Mac Mini 24GB, RTX 3090/4090 24GB VRAM."
topic: 19
source: perplexity-manual
source_letter: A
tier: dr
synthesis_target: "[[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]"
tags: [research, deep-research, pi.dev, ollama, optimal-models, perplexity-manual]
---

# Optimal Ollama Models for Pi (pi.dev) Workflows Across Three Hardware Tiers — May 2026

> **Scope:** Pi = the terminal coding agent at [pi.dev](https://pi.dev/) / [github.com/earendil-works/pi](https://github.com/earendil-works/pi-mono), not Raspberry Pi. Ollama = [ollama.com](https://ollama.com/). All tok/s figures are generation throughput (not prefill), measured at Q4_K_M quantization unless otherwise noted.

***

## 1. Workload Profile — What Pi Actually Demands

Pi is a "minimal terminal coding harness" with four core built-in tools (`read`, `write`, `edit`, `bash`) plus an extension system. Every Pi agentic loop sends tool calls through Ollama via an `openai-completions`-compatible API at `http://localhost:11434/v1`. This creates four distinct load patterns:[^1][^2]

| Workload | Pi behavior | Primary bottleneck |
|---|---|---|
| **(a) Tool-calling / agentic loops** | Rapid read→edit→bash cycles; model must emit valid JSON tool schemas on every turn | Format correctness, low latency per turn |
| **(b) Code completion + inline edits** | `edit` tool diffs; fill-in-the-middle for completions | Raw tok/s, FIM accuracy |
| **(c) Multi-turn planning / reasoning** | Long sessions accumulate context; Pi auto-compacts only at `agent_end` and before next user prompt[^3] | Context window depth, memory footprint |
| **(d) Long-context summarization** | Reading large files via `read`; repo-scale understanding | KV-cache size, bandwidth-limited throughput |

Pi uses the `compat.supportsDeveloperRole` and `compat.supportsReasoningEffort` flags to signal when a local server (like Ollama) lacks OpenAI reasoning-tier fields — this must be set to `false` for Ollama in `models.json`. Pi's official documentation explicitly recommends `qwen3-coder` as the default local model.[^2][^1]

***

## 2. Tier A — M4 Max MacBook Pro (48GB Unified Memory)

**Memory budget:** With 48GB unified and ~4–6GB consumed by macOS + background apps, roughly 42GB is available for the model. Ollama 0.8+ on Apple Silicon uses the llama.cpp Metal backend; the optional MLX backend added in Ollama 0.19 (March 2026) delivers 15–30% throughput gains.[^4]

### Best Overall: `qwen3-coder:30b` (Q4_K_M)

**qwen3-coder:30b** is an MoE model with 30B total parameters but only 3.3B activated per token. This is the architecture that makes it fast on bandwidth-constrained hardware. Pi's official documentation lists it as the named default local model, and the Ollama library page explicitly surfaces Pi integration alongside it.[^5][^6][^1]

- **Quantization:** Q4_K_M (default tag)
- **Memory footprint:** ~17–19GB unified memory at 16K context; ~24–32GB at 64K context[^7][^8]
- **Tokens/sec (Ollama):** ~60–70 tok/s on M4 Max 48GB[^8][^4]
- **Tokens/sec (LM Studio/MLX):** ~100+ tok/s at same hardware — if you want maximum throughput and are comfortable with LM Studio's server mode, configure Pi to point to LM Studio's OpenAI-compatible endpoint[^9][^10]
- **Context window:** 256K native; set `num_ctx` explicitly in Ollama (see §6 for the gotcha)[^5]
- **Shines at:** All four workloads — the MoE architecture's low activation count means it doesn't slow down under long context the way dense models do; native tool-calling via the Ollama API works correctly[^11]

```bash
ollama pull qwen3-coder:30b
```

**Pi `models.json` entry:**
```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [{ "id": "qwen3-coder:30b", "contextWindow": 32768 }]
    }
  }
}
```

***

### Runner-Up #1: `devstral:24b-small-2505-q4_K_M`

**Devstral Small 2505** is fine-tuned specifically for agentic coding from Mistral Small 3.1, achieving 46.8% on SWE-Bench Verified — beating Claude 3.5 Haiku and GPT-4.1-mini under the same OpenHands scaffold. It's a dense 24B with a 128K context window.[^12][^13][^14]

- **Quantization:** Q4_K_M
- **Memory footprint:** ~14–16GB at 16K context
- **Tokens/sec (Tier A):** ~35–45 tok/s estimated on M4 Max (dense 24B vs MoE; see §5 note on RTX 4090 baseline of 34–40 tok/s for dense 24B Q4)[^15]
- **Context window:** 128K — but Ollama defaults to 2048; must set `num_ctx` manually (see §6)[^16][^17]
- **Shines at:** Tool-calling reliability, multi-file code editing (workloads a and b); trained end-to-end for coding agent scaffolds

```bash
ollama pull devstral:24b-small-2505-q4_K_M
```

***

### Runner-Up #2: `qwen2.5-coder:32b` (Q4_K_M)

**Qwen2.5-Coder 32B** is a dense 32B code-specialized model, scoring 73.7 on the Aider benchmark (comparable to GPT-4o) and 65.9 on McEval across 40+ languages. It fits in 48GB with headroom but is noticeably slower than the MoE qwen3-coder due to all 32B parameters being active.[^18]

- **Quantization:** Q4_K_M
- **Memory footprint:** ~19–20GB at 8K context
- **Tokens/sec (Tier A):** ~12–18 tok/s on M4 Max 48GB (dense 32B; a 64GB M4 Max measures 22 tok/s for the similar-scale Qwen3-32B dense)[^19]
- **Context window:** 128K; same `num_ctx` requirement
- **Shines at:** Code reasoning and repair (workload b); established community support and the most-tested model in local coding agent setups

```bash
ollama pull qwen2.5-coder:32b
```

***

### Lightweight Session Model: `qwen3:8b` (Q4_K_M)

When other apps need RAM or for quick inline edits that don't warrant loading the full 30B MoE, `qwen3:8b` is the pick. It fits in ~5–6GB and runs at 80–120 tok/s on M4 Max, leaving ample memory for IDEs, browsers, and other processes.[^4]

```bash
ollama pull qwen3:8b
```

***

## 3. Tier B — M4 Pro Mac Mini, 24GB Unified Memory (Headless, Always-On)

**Memory budget:** 24GB unified with ~6–8GB for macOS headless processes leaves 16–18GB available for the model. This is the binding constraint. The M4 Pro has 273 GB/s memory bandwidth, which translates directly to MoE throughput advantages.[^20]

Priority ordering for this tier: **tool-calling reliability > codegen speed**, as a headless agent runner should produce correct, parseable tool calls consistently rather than maximizing raw throughput.

### Best Overall: `qwen3-coder:30b` (Q4_K_M)

The same MoE model that tops Tier A is even more advantageous at 24GB. Its ~17–19GB footprint at practical context sizes fits within the memory budget, while its MoE activation pattern means only 3.3B parameters need bandwidth per token — making it faster proportionally than a same-parameter dense model would be.[^6][^5]

- **Quantization:** Q4_K_M
- **Memory footprint:** ~17–19GB (within budget at 16K context; set `num_ctx` carefully)
- **Tokens/sec (Tier B):** ~40–50 tok/s on M4 Pro 24GB via Ollama, based on M4 Pro 64GB benchmark of ~70 tok/s (memory bandwidth scales proportionally for MoE)[^8]
- **Critical config:** Keep `num_ctx` at ≤16384 to avoid OOM; at 32K context the model can exceed available memory
- **Shines at:** Tool-calling and agentic loops (workloads a and b); reliable output formatting for Pi's `openai-completions` API

```bash
ollama pull qwen3-coder:30b
```

**Pi `models.json` — memory-safe config for Tier B:**
```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": { "supportsDeveloperRole": false, "supportsReasoningEffort": false },
      "models": [{ "id": "qwen3-coder:30b", "contextWindow": 16384 }]
    }
  }
}
```

***

### Runner-Up #1: `devstral:24b-small-2505-q4_K_M`

At ~14–16GB, Devstral Q4_K_M fits more comfortably in 24GB than qwen3-coder:30b and leaves more headroom for context growth during long agentic sessions. It's the safer choice if the agent will be running continuously with large codebases.

- **Memory footprint:** ~14–16GB at 16K context — approximately 2–3GB less than qwen3-coder:30b
- **Tokens/sec (Tier B):** ~30–40 tok/s estimated (dense 24B on M4 Pro; benchmarks for Mistral Small 3.1-class models on M4 Pro 24GB suggest this range)[^15][^20]
- **Context window:** 128K model max; set `num_ctx` to 32768 — safe at this footprint
- **Shines at:** Always-on headless agent loops where memory stability matters more than peak throughput

```bash
ollama pull devstral:24b-small-2505-q4_K_M
```

***

### Runner-Up #2: `qwen3:14b` (Q5_K_M)

For when even Devstral feels heavy, `qwen3:14b` at Q5_K_M uses ~10GB unified memory and delivers ~55–65 tok/s on M4 Pro. Community testing confirms it as one of the stable models on Mac Mini M4 Pro 24GB for coding agent use. It handles tool calling reliably as a Qwen-family model.[^21][^4]

```bash
ollama pull qwen3:14b
```

***

### Lightweight Session Model: `qwen3:8b` (Q4_K_M)

Same as Tier A — at ~5GB it leaves 19GB free and is the right pick for Pi sessions that only need quick file reads, grep operations, and simple edits.

```bash
ollama pull qwen3:8b
```

***

### Workload Routing Note for Tier B

Tier B cannot competently handle all four workloads simultaneously at acceptable speed when operating at the edge of memory. The recommended routing pattern:

- **Workloads a + b (tool-calling, code edits):** Run locally with qwen3-coder:30b at 16K context
- **Workload c (multi-turn planning with very long context >32K):** Route to cloud (Qwen3-Coder-Next via OpenRouter at $0.11/M input tokens) or to Tier A/C[^22]
- **Workload d (repo-scale summarization):** Same cloud routing recommendation; the 24GB KV cache limit makes sustained 100K+ context windows impractical for headless use

***

## 4. Tier C — RTX 3090/4090 24GB VRAM (Alienware, CUDA)

**Memory budget:** 24GB GDDR6X VRAM, dedicated (no OS sharing). CUDA inference via llama.cpp CUDA backend in Ollama. The RTX 4090 benchmarks at 20–30 tok/s for dense 32B Q4_K_M models and 34–40 tok/s for dense 24B Q4_K_M. Critically, VRAM and unified memory are comparable in capacity at 24GB, but NVIDIA's memory bandwidth (RTX 4090: ~1,000 GB/s) can outpace M4 Pro (273 GB/s) on dense models while the M4 Max (546 GB/s) is more competitive.[^20][^15][^4]

### Best Overall: `devstral:24b-small-2505-q4_K_M`

On a CUDA GPU, Devstral's dense 24B architecture fully utilizes the 4090's CUDA cores, while the MoE activation sparsity that helps Apple Silicon less directly benefits NVIDIA's highly parallel architecture. Devstral Q4_K_M fits in ~14–16GB VRAM with room for 32K–64K context.[^23][^24]

- **Quantization:** Q4_K_M
- **Memory footprint:** ~14–16GB VRAM; confirmed to run on single RTX 4090[^23][^12]
- **Tokens/sec (Tier C, RTX 4090):** ~40–55 tok/s estimated (dense 24B at Q4_K_M; databasemart benchmarks show 58.62 tok/s for Qwen 14B Q4 and 34.22 tok/s for DeepSeek 32B Q4 on RTX 4090, triangulating dense 24B to ~40–55 range)[^15]
- **SWE-Bench:** 46.8% — the highest of any model in this guide for agentic coding tasks[^12]
- **Shines at:** All four workloads; CUDA gives it a speed advantage over the M4 Pro at the same model size; dense architecture pairs well with NVIDIA's throughput model

```bash
ollama pull devstral:24b-small-2505-q4_K_M
```

**Critical context fix for Ollama + Devstral (see §6):**
```bash
ollama show devstral:24b-small-2505-q4_K_M --modelfile > devstral.modelfile
echo "PARAMETER num_ctx 32768" >> devstral.modelfile
ollama create devstral-32k -f devstral.modelfile
```

***

### Runner-Up #1: `qwen3-coder:30b` (Q4_K_M)

On an RTX 4090, the MoE qwen3-coder:30b still fits in ~17–19GB VRAM and runs faster than a dense 32B thanks to sparse activation — but it runs slower than Devstral on NVIDIA hardware because CUDA is highly optimized for dense matmuls, not sparse MoE.[^25]

- **Memory footprint:** ~17–19GB VRAM
- **Tokens/sec (Tier C, RTX 4090):** ~55–75 tok/s (MoE 3.3B active; RTX 3090 community benchmarks show Qwen3-30B-A3B at ~72.9 tok/s)[^10]
- **Shines at:** Long-context summarization and planning (workloads c and d); 256K native context window means it can handle very large repos without truncation

```bash
ollama pull qwen3-coder:30b
```

***

### Runner-Up #2: `qwen3:32b` (Q4_K_M)

The dense 32B non-coder variant fits in ~19–20GB VRAM on a 4090 and delivers strong multi-turn reasoning. Less specialized than Devstral for pure agent loops, but broader general and planning ability makes it useful when Pi sessions involve architecture decision-making, not just code editing.

- **Memory footprint:** ~19–20GB VRAM
- **Tokens/sec (Tier C, RTX 4090):** ~20–30 tok/s (dense 32B Q4_K_M; per April 2026 community consensus)[^4]
- **Shines at:** Multi-turn planning and reasoning (workload c)

```bash
ollama pull qwen3:32b
```

***

### Lightweight Session Model: `qwen3:8b` (Q4_K_M)

On a 4090, `qwen3:8b` Q4_K_M runs at ~80–100 tok/s in VRAM and uses ~5GB, leaving 19GB free. Fast enough for real-time inline completions.[^4]

```bash
ollama pull qwen3:8b
```

***

### Tier C vs Tier A Speed Comparison — Same Model

For the same model/quant, Tier C (RTX 4090) beats Tier B (M4 Pro 24GB) on dense models, roughly ties with Tier A (M4 Max 48GB) on dense 24B, and loses to Tier A on MoE models due to Apple Silicon's bandwidth-to-activation efficiency advantage:

| Model | RTX 4090 density | Apple Silicon advantage |
|---|---|---|
| Dense 24B Q4 (Devstral) | 4090 wins by ~10–20 tok/s | M4 Pro close; M4 Max slightly behind 4090 |
| Dense 32B Q4 | Similar at ~20–30 tok/s | M4 Max ties; M4 Pro loses |
| MoE 30B/3.3B-active Q4 | 4090 still fast but sparsity advantage is less | M4 Max wins due to bandwidth-per-active-param |

***

## 5. Cross-Tier Comparison Table

| Model | Tier A (M4 Max 48GB) | Tier B (M4 Pro 24GB) | Tier C (RTX 4090 24GB) | Best-fit Pi workload |
|---|---|---|---|---|
| `qwen3-coder:30b` Q4_K_M | ~60–70 tok/s[^8][^4] | ~40–50 tok/s (est.) | ~55–75 tok/s[^10] | All four; especially (a) + (d) |
| `devstral:24b-small-2505` Q4_K_M | ~35–45 tok/s (est.) | ~30–40 tok/s (est.) | ~40–55 tok/s[^15] | (a) + (b): tool-calling + code edits |
| `qwen2.5-coder:32b` Q4_K_M | ~12–18 tok/s[^19] | ⚠️ Too large (~20GB; marginal fit) | ~20–34 tok/s[^15] | (b): code completion |
| `qwen3:32b` Q4_K_M | ~20–25 tok/s[^19] | ⚠️ Marginal (may exceed 18GB budget) | ~20–30 tok/s[^4] | (c): planning/reasoning |
| `qwen3:14b` Q5_K_M | ~55–65 tok/s[^4] | ~45–55 tok/s[^4] | ~50–65 tok/s[^4] | (b): fast code edits |
| `qwen3:8b` Q4_K_M (lightweight) | ~80–120 tok/s[^4] | ~60–90 tok/s[^26] | ~80–100 tok/s[^4] | Quick tool loops, low RAM sessions |

**Workload routing recommendation across tiers:**
- Route Pi's multi-turn planning sessions (workload c, >32K context) to **Tier A** (most memory headroom)
- Keep always-on tool-calling agent loops (workload a) on **Tier B** (energy efficient, always running)
- Use **Tier C** for batch code generation and long-context summarization (workloads b + d) where CUDA throughput gives the fastest turnaround

***

## 6. Pi-Specific Compatibility Notes

### Critical: Ollama's 2048-Token Default Context Window

Pi's agentic loops accumulate tool call history rapidly. Ollama defaults its context window to **2048 tokens** unless explicitly overridden — and it silently truncates leading context without warning. A typical Pi session reading a few files and executing bash commands will blow past 2048 in minutes. Every Ollama model used in Pi must have `num_ctx` explicitly set.[^27]

**Fix via Modelfile (permanent):**
```bash
ollama show qwen3-coder:30b --modelfile > mymodel.modelfile
echo "PARAMETER num_ctx 32768" >> mymodel.modelfile
ollama create qwen3-coder-32k -f mymodel.modelfile
```

Or set the environment variable globally:
```bash
OLLAMA_CONTEXT_LENGTH=32768 ollama serve
```

Or configure it per-session in Pi's `models.json`:
```json
{ "id": "qwen3-coder:30b", "contextWindow": 32768 }
```

This was confirmed as a known issue in the Devstral + OpenHands setup: "By default, it will be initialized to have context length of a mere 2048 tokens".[^16]

***

### Pi `compat` Settings Required for Ollama

Pi's `models.md` documentation explicitly notes that Ollama does not support the `developer` role (used for reasoning models) or `reasoning_effort` (used for extended thinking). Without the compat flags, Pi may crash or produce malformed API calls when using any reasoning-capable model variant.[^2]

**Required provider-level compat block:**
```json
"compat": {
  "supportsDeveloperRole": false,
  "supportsReasoningEffort": false
}
```

For Qwen-family models with thinking mode (e.g., `qwen3` with thinking enabled), also set `thinkingFormat: "qwen"` at the model level.[^2]

***

### Gemma 4 Multimodal Vision Failure (GitHub Issue #3022)

When using `gemma4:31b-cloud` or other multimodal models via Ollama's `openai-completions` provider, Pi's `read` tool cannot deliver binary image data to the model correctly. The `convertMessages` function in `packages/ai/src/providers/openai-completions.ts` uses an "interleaved" delivery pattern that fails with unified-architecture multimodal models via Ollama. The model receives tool text but drops the visual payload, causing hallucinations about image content.[^28]

**Workaround:** For workloads requiring image understanding, use a cloud provider directly rather than routing multimodal models through Ollama. For pure text/code workloads (all four Pi workloads described in §1), this issue is not relevant.

***

### Tool Call Format Issues with Non-Qwen Models

A documented pattern in both Continue.dev and Pi community threads: some Ollama models output XML-style tool call syntax rather than the JSON format Pi's `openai-completions` API expects. The Qwen-family (qwen3-coder, qwen2.5-coder, qwen3) and Devstral use native tool calling via the Ollama API and are the most reliable. Llama variants and older Mistral models are more prone to outputting literal JSON strings instead of executing tool calls.[^29][^11]

**Symptom:** Pi session shows the tool call JSON in the terminal response instead of executing the tool.

**Fix:** Ensure the model supports `tools` in its Ollama metadata (check [ollama.com/library](https://ollama.com/library) — models with the `tools` tag support native tool calling). Lower temperature to 0.1 for tool-calling-heavy sessions.[^18][^5]

***

### Qwen3-Coder Missing FIM in Ollama Template (GitHub Issue #11621)

A reported issue (filed August 2025, subsequently closed) noted that `qwen3-coder:30b`'s Ollama template was initially missing FIM (Fill-In-the-Middle) and tool-calling support in its template definition. This was resolved in Ollama's library update, but if running an older cached version, pull the latest tag explicitly:[^30]

```bash
ollama pull qwen3-coder:30b --insecure
```

Or check the template supports tools:
```bash
ollama show qwen3-coder:30b --template
```

The template should include tool-use sections if properly updated.

***

### Auto-Compaction Overflow During Long Tool-Call Chains (Pi Issue #2871)

Pi's auto-compaction only triggers at `agent_end` and before the next user prompt — not mid-turn. In long agentic sessions (reading and editing many files in a single turn), context can balloon to 400K+ tokens before any compaction fires. This causes Pi to strip the last valid assistant response and retry, wasting completed work.[^3]

**Mitigation:** Set a conservative `contextWindow` value in `models.json` (e.g., 32768 for Tier B) to trigger compaction earlier. For Tier A and C where memory allows, 65536 gives a better balance between long context and compaction frequency.

***

## 7. Sources

| URL | Notes | Access Date |
|---|---|---|
| [docs.ollama.com/integrations/pi](https://docs.ollama.com/integrations/pi) | Official Pi integration docs; lists qwen3-coder as default local model | May 2026 |
| [github.com/earendil-works/pi/.../models.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md) | Pi custom model config reference; compat fields for Ollama | May 8, 2026 commit |
| [ollama.com/library/qwen3-coder](https://ollama.com/library/qwen3-coder) | Official Qwen3-Coder library page; MoE params, context window | May 2026 |
| [ollama.com/library/devstral](https://ollama.com/library/devstral) | Devstral official page; SWE-Bench 46.8%, RTX 4090 / 32GB Mac requirement | May 2026 |
| [carlosmarten.com/best-local-ai-by-hardware-april-26-2026](https://carlosmarten.com/best-local-ai-by-hardware-april-26-2026/) | Hardware-tier model guide; RTX 4090 and Apple Silicon tok/s figures | April 26, 2026 |
| [macgpu.com M4 Pro benchmark](https://macgpu.com/en/blog/2026-mac-inference-framework-vllm-mlx-ollama-llamacpp-benchmark.html) | M4 Pro Ollama vs MLX vs llama.cpp throughput comparison | Feb 2026 |
| [asiai.dev/benchmark-llm-mac](https://asiai.dev/benchmark-llm-mac/) | M4 Pro 64GB: LM Studio 102 tok/s vs Ollama 70 tok/s for qwen3-coder-30b | March 2026 |
| [llmcheck.net Qwen3 32B on M4 Max](https://llmcheck.net/models/qwen-3-32b-on-m4-max/) | M4 Max 64GB MLX benchmark: 22 tok/s dense 32B Q4_K_M | Feb 2026 |
| [r/LocalLLM M4 Max 128GB Qwen3-30B](https://www.reddit.com/r/LocalLLM/comments/1l6lxcr/qwen3_30b_a3b_on_macbook_pro_m4_frankly_its_crazy/) | M4 Max 128GB MLX: 103 tok/s; M3 Max 64GB: 88 tok/s; M1 Max 64GB also tested | June 2025 |
| [databasemart.com RTX 4090 Ollama benchmark](https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx4090) | RTX 4090 eval rates: Qwen2.5-14B: 63.92 tok/s; Qwen2.5-32B: 34.39 tok/s | Dec 2024 |
| [github.com/earendil-works/pi/issues/3022](https://github.com/earendil-works/pi/issues/3022) | Gemma 4 multimodal vision failure with openai-completions | April 10, 2026 |
| [github.com/earendil-works/pi/issues/2871](https://github.com/earendil-works/pi/issues/2871) | Pi auto-compaction not checked mid-turn | April 5, 2026 |
| [github.com/ollama/ollama/issues/11621](https://github.com/ollama/ollama/issues/11621) | Qwen3-Coder missing FIM/tools in Ollama template (closed) | August 2025 |
| [reddit.com/r/LocalLLaMA — Devstral context](https://www.reddit.com/r/LocalLLaMA/comments/1kui17w/) | Devstral Ollama defaults to 2048-token context; confirmed breakage | May 2025 |
| [r/ollama Ollama Pi + Qwen 3.6 thread](https://www.reddit.com/r/ollama/comments/1svf5b1/) | Community thread on Pi + Ollama + Qwen tool call behavior | April 2026 |
| [mistral.ai/news/devstral](https://mistral.ai/news/devstral) | Official Devstral launch; SWE-Bench verified score, hardware requirements | May 2025 |
| [whatllm.org/best-ollama-models](https://whatllm.org/best-ollama-models) | April 2026 Ollama model rankings by use case | April 2026 |
| [morphllm.com/best-ollama-models](https://www.morphllm.com/best-ollama-models) | Qwen2.5-Coder 32B: 92.7% HumanEval; April 2026 rankings | April 2026 |

---

## References

1. [Pi - Ollama's documentation](https://docs.ollama.com/integrations/pi)

2. [pi/packages/coding-agent/docs/models.md at main - GitHub](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md) - AI agent toolkit: coding agent CLI, unified LLM API, TUI & web UI libraries, Slack bot, vLLM pods - ...

3. [Auto-compaction not checked mid-turn: context grows unbounded ...](https://github.com/earendil-works/pi/issues/2871) - Use an extension or custom model config to set contextWindow to 200k on a model whose provider accep...

4. [Best Local AI by Hardware — April 26, 2026 - Carlos Marten](https://carlosmarten.com/best-local-ai-by-hardware-april-26-2026/) - Running AI models locally has never been more practical. In April 2026, a consumer RTX 4090 can serv...

5. [qwen3-coder - Ollama](https://ollama.com/library/qwen3-coder) - Alibaba's performant long context models for agentic and coding tasks.

6. [qwen3-coder:30b - Ollama](https://ollama.com/library/qwen3-coder:30b) - qwen3-coder:30b offers 30B total parameters with only 3.3B activated, delivering strong performance ...

7. [Running Qwen3 on your macbook, using MLX, to vibe code for free](https://news.ycombinator.com/item?id=43856489) - I'm using Qwen3-30B-A3B locally and it's very impressive. Feels like the GPT-4 killer we were waitin...

8. [How to Benchmark LLMs on Mac - asiai](https://asiai.dev/benchmark-llm-mac/) - How to benchmark LLM inference on Mac: step-by-step guide to measure tok/s, TTFT, power, and VRAM on...

9. [Qwen3 30B a3b on MacBook Pro M4, Frankly, it's crazy to be able to ...](https://www.reddit.com/r/LocalLLM/comments/1l6lxcr/qwen3_30b_a3b_on_macbook_pro_m4_frankly_its_crazy/) - Qwen3 30B a3b on MacBook Pro M4, Frankly, it's crazy to be able to use models of this quality with s...

10. [Qwen 3 Performance: Quick Benchmarks Across Different Setups ...](https://theaterfi.re/post/2198611)

11. [Ollama models consistently print XML instead of calling tools or ...](https://github.com/continuedev/continue/discussions/10534) - Some models: XML-style (what you are seeing); Continue expects a specific format. Model not trained ...

12. [devstral - Ollama](https://ollama.com/library/devstral) - Devstral: the best open source model for coding agents

13. [Devstral - Mistral AI](https://mistral.ai/news/devstral) - Here, we show Devstral's performance on the popular SWE-Bench Verified benchmark ... Devstral is lig...

14. [Devstral Small 2505 - API Pricing & Benchmarks - OpenRouter](https://openrouter.ai/mistralai/devstral-small-2505) - Devstral supports a 128k context window and uses a custom Tekken tokenizer. It is text-only, with th...

15. [Benchmarking LLMs on NVIDIA RTX 4090 GPU Server with Ollama](https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx4090) - Discover the ultimate RTX 4090 benchmark for running LLMs on Ollama, a GPU server optimized for effi...

16. [OpenHands + Devstral is utter crap as of May 2025 (24G VRAM)](https://www.reddit.com/r/LocalLLaMA/comments/1kui17w/openhands_devstral_is_utter_crap_as_of_may_2025/) - Did you run devstral with default parameters in ollama? By default, it will be initialized to have c...

17. [How does num_ctx and model's context length work (together)?](https://www.reddit.com/r/ollama/comments/1j4egbh/how_does_num_ctx_and_models_context_length_work/) - In ollama, you can set the context length of a model by setting its num_ctx parameter. But, the mode...

18. [qwen2.5-coder - Ollama](https://ollama.com/library/qwen2.5-coder) - Qwen 2.5 Coder 32B performs excellent across more than 40 programming languages, scoring 65.9 on McE...

19. [Run Qwen 3 32B on M4 Max — Performance, Setup & Benchmarks](https://llmcheck.net/models/qwen-3-32b-on-m4-max/) - Qwen 3 32B runs at 22 tok/s on M4 Max with 64 GB RAM. Q4_K_M quantization via MLX. Complete setup gu...

20. [04. Deployment: Activating...](https://macgpu.com/en/blog/2026-mac-inference-framework-vllm-mlx-ollama-llamacpp-benchmark.html) - In the age of M4 Pro, which framework rules them all? Benchmarking throughput and latency on bare me...

21. [Stable OpenCLAW models on Mac Mini 4 Pro - Facebook](https://www.facebook.com/groups/1577315533418837/posts/1668247274325662/) - Qwen 3.5 and 3.6 are far better than Qwen3. And Qwen3 is far better than 2.5. Qwen 2.5 is obsolete t...

22. [Qwen: Qwen3 Coder Next - Pi Coding Agent](https://pi.dev/models/openrouter/qwen-qwen3-coder-next) - A terminal-based coding agent

23. [devstral:24b-small-2505-q4_K_M - Ollama](https://ollama.com/library/devstral:24b-small-2505-q4_K_M) - Devstral: the best open source model for coding agents

24. [devstral:24b-small-2505-q8_0 - Ollama](https://ollama.com/library/devstral:24b-small-2505-q8_0) - The model achieves remarkable performance on SWE-bench which positionates it as the #1 open source m...

25. [Qwen3 MoE 30b-a3b, poor performance and Low GPU utilization ...](https://github.com/ollama/ollama/issues/10458) - What is the issue? When running Qwen3-30b-a3b, my 4090 is only running at ~120w, really low utilizat...

26. [Benchmark Analysis — Anubis OSS - devPad](https://devpadapp.com/anubis_bench_analysis.html)

27. [Ollama has a num_ctx parameter that controls the context window ...](https://news.ycombinator.com/item?id=42833427) - Ollama has a num_ctx parameter that controls the context window length - it defaults to 2048. At a g...

28. [gemma4:31b-cloud multimodal model can't 'see' images · Issue #3022](https://github.com/earendil-works/pi/issues/3022) - Steps to reproduce. Setup a Pi coding agent with a gemma4 model; Ask it to use the 'read' tool on an...

29. [issues with ollama models tool calls - Facebook](https://www.facebook.com/groups/openclawusers/posts/669627972866146/) - My experience with VS code is that models run locally via ollama do not support tool calls ... Anyon...

30. [Qwen3-Coder missing Tools and FIM support in template](https://github.com/ollama/ollama/issues/11621) - What is the issue? As per https://github.com/QwenLM/Qwen3-Coder/blob/main/README.md, both Tool calli...

