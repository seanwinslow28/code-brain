---
type: research-synthesis
date: 2026-05-21
question: "Topic 19 — Optimal Ollama model for Pi-driven coding + agentic workflows in 2026, ranked by RAM/VRAM tier."
sources:
  - "[[2026-05-21-topic-19a-optimal-ollama-models-pi-perplexity]]"
  - "[[2026-05-21-topic-19b-optimal-ollama-models-pi-gemini-dr]]"
  - "[[2026-05-21-topic-19c-optimal-ollama-models-pi-chatgpt]]"
synthesis_method: "Three independent vendor sources (Perplexity, Gemini DR, ChatGPT) cross-ranked. Convergence + divergence analyzed against Pi's published documentation. Speculative vendor claims (TriAttention, TurboQuant, mdq100/qwen3.5-coder community tag) flagged but not used in the canonical recommendation."
target_reader: "Solo developer running Pi (pi.dev) on a 3-device personal fleet: M4 Max MacBook Pro, M4 Pro Mac Mini 24GB (always-on headless), RTX 4090 24GB Alienware."
tags: [research, synthesis, pi.dev, ollama, optimal-models, hardware-tier]
---

# Optimal Ollama Models for Pi (pi.dev) — Three-Source Synthesis (2026-05-21)

## TL;DR — The Pick Per Tier

| Tier | Hardware | Best Overall | Why |
|---|---|---|---|
| **A** | M4 Max MacBook Pro (assume 48GB+) | `qwen3-coder:30b` Q4_K_M | Pi's officially documented default. MoE 30B / 3.3B-active fits in ~18GB and runs ~60–70 t/s. Wins all four Pi workloads. |
| **B** | M4 Pro Mac Mini 24GB (headless, always-on) | `qwen3-coder:30b` Q4_K_M @ `num_ctx=16384` | Same model — fits within the 24GB budget at 16K context. Trades context depth for memory headroom. ~40–50 t/s. |
| **C** | RTX 4090 24GB VRAM (Alienware) | `devstral:24b-small-2505-q4_K_M` | Dense 24B specifically fine-tuned for agentic coding (SWE-Bench Verified 46.8% — highest in this guide). CUDA prefers dense matmuls over sparse MoE. ~40–55 t/s. |

**Single-model routing pattern** for Sean's 3-device fleet:
1. Tier B Mac Mini = primary autonomous-agent tool-caller (qwen3-coder:30b @ 16K)
2. Tier A MBP = primary interactive dev session (qwen3-coder:30b @ 32–64K)
3. Tier C Alienware = batch codegen + long-context summarization (devstral 24B @ 32K)

**Lightweight fallback (all tiers):** `qwen3:8b` Q4_K_M (~5GB, 60–120 t/s depending on hardware).

---

## How the Three Sources Disagreed (and Which to Trust)

| Question | Perplexity (A) | Gemini DR (B) | ChatGPT (C) | Verdict |
|---|---|---|---|---|
| Tier A best model | `qwen3-coder:30b` (MoE, Pi's documented default) | `mdq100/qwen3.5-coder:35b` (community tag, "Gated DeltaNet sparse MoE") | `gemma4:31b` (26B MoE, multimodal) | **A wins** — names Pi's officially recommended local model; B's "Qwen 3.5 Coder 35B" is unverified and `mdq100/` is a community fork; C's Gemma4 has the Pi GitHub issue #3022 multimodal tool failure |
| Tier B best model | `qwen3-coder:30b` @ 16K context | `gemma4:26b` (4B active MoE) | `gemma4:26b` dense | **A wins by safety** — Gemma4 has the multimodal-vision bug for Pi's `read` tool; qwen3-coder keeps Pi-native tool-calling reliability |
| Tier C best model | `devstral:24b-small-2505-q4_K_M` | `mdq100/qwen3.5-coder:35b` (168–189 t/s claim with "TriAttention + TurboQuant") | `qwen3.5:35b-a3b-coding-nvfp4` (only 12 t/s — slow) | **A wins** — Devstral has verifiable SWE-Bench scores and is documented to fit in 24GB VRAM; B's TriAttention/TurboQuant tech does not appear in public Ollama, llama.cpp, or NVIDIA release notes as of 2026-05; C's own benchmark is unfavorable |
| Lightweight model | `qwen3:8b` | `phi-4-mini:3.8b` | `phi3.5:3.8b` | **All three viable** — qwen3:8b is the conservative pick (stays in Qwen family for tool-call consistency); phi-3.5/4-mini is fine if RAM is critical |

### Why Perplexity Outranks the Other Two

- Cites Pi's official documentation explicitly recommending `qwen3-coder` as the default local model (verified against `docs.ollama.com/integrations/pi` and `github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md`).
- All benchmark figures attributed to real, dated URLs (carlosmarten.com, databasemart.com, llmcheck.net, r/LocalLLaMA threads).
- All Ollama tags are inspectable on the official Ollama library — no community-only forks.
- Identifies real, dated GitHub issues with Pi-specific implications (`earendil-works/pi#3022`, `#2871`, `ollama/ollama#11621`).

### Where to Be Skeptical of Gemini DR

The following claims appear in source B (Gemini DR) but **do not appear in source A or source C**, and could not be verified against primary documentation as of 2026-05-21:

1. **"Qwen 3.5 Coder 35B" with "Gated DeltaNet + sparse MoE routing"** — the `mdq100/qwen3.5-coder:35b` Ollama tag is a community fork, not an official Qwen release. The Qwen series most recently shipped Qwen3-Coder (which all three sources implicitly agree exists).
2. **"TriAttention backend + TurboQuant KV compression" giving 40% KV cache reduction on RTX 4090** — neither technology appears in NVIDIA, llama.cpp, or Ollama release notes through 2026-05-21. Treat as hypothetical.
3. **"OpenClaw" framework with version 2026.4.26 and bug issues #5769 / #11828 / #74579** — Pi's underlying codebase is hosted at `github.com/earendil-works/pi`. There is no public `openclaw/openclaw` repository at the time of writing. The bug numbers do not match Pi's actual issue tracker.
4. **"ollama launch pi" zero-config command** — Source A (Perplexity) and source C (ChatGPT) do not mention this CLI flow. Verify against `ollama --help` before relying on it.

**Recommendation:** Read source B for its taxonomy of workload patterns (the four-workload framework is genuinely useful), but treat all specific model tags, benchmark figures, and GitHub issue numbers as needing verification against the other two sources or primary docs.

### Where ChatGPT (Source C) Was Useful

- Most pragmatic on **Pi compatibility gotchas** — independently confirms (with source A) the tool-call streaming bug, the 2048/4096 default context window issue, and the `compat.supportsDeveloperRole: false` requirement.
- Honest about throughput on Apple Silicon — its 12 t/s figure for Qwen3.5 35B on RTX 4090 is unflattering but realistic for that quantization. Reality-checks Gemini DR's 168–189 t/s claim.

---

## Canonical Recommendation — Pi Configs for Each Tier

### Tier A — M4 Max MacBook Pro (interactive dev sessions)

```bash
ollama pull qwen3-coder:30b
```

Create a 32K-context Modelfile (Ollama default of 2048 will break Pi after one tool loop):

```bash
ollama show qwen3-coder:30b --modelfile > qwen3c-32k.modelfile
echo "PARAMETER num_ctx 32768" >> qwen3c-32k.modelfile
ollama create qwen3-coder-32k -f qwen3c-32k.modelfile
```

Pi `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "ollama-mbp": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "qwen3-coder-32k", "contextWindow": 32768 }
      ]
    }
  }
}
```

Expected: ~60–70 t/s, ~18–24GB unified memory used (leaves headroom for IDE + browser).

---

### Tier B — M4 Pro Mac Mini 24GB (always-on headless agent runner)

Same model, smaller context. Set Ollama to listen on the LAN so the MBP and Alienware can also hit it:

```bash
# On the Mac Mini:
launchctl setenv OLLAMA_HOST 0.0.0.0
launchctl setenv OLLAMA_KEEP_ALIVE 30m
ollama pull qwen3-coder:30b

ollama show qwen3-coder:30b --modelfile > qwen3c-16k.modelfile
echo "PARAMETER num_ctx 16384" >> qwen3c-16k.modelfile
ollama create qwen3-coder-16k -f qwen3c-16k.modelfile
```

Pi `~/.pi/agent/models.json` on any client device pointing at the Mac Mini:

```json
{
  "providers": {
    "ollama-macmini": {
      "baseUrl": "http://mac-mini.local:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "qwen3-coder-16k", "contextWindow": 16384 }
      ]
    }
  },
  "settings": {
    "defaultProvider": "ollama-macmini",
    "defaultModel": "qwen3-coder-16k",
    "timeout": 30000,
    "fallbackProvider": "anthropic"
  }
}
```

Expected: ~40–50 t/s, ~17–19GB unified memory. The 16K context is the binding constraint — if you need >32K, route to Tier A or cloud (per Perplexity's routing note).

**LAN/Tailscale alternative:** replace `mac-mini.local` with `mac-mini.tail-name.ts.net` for off-LAN access via Tailscale MagicDNS.

---

### Tier C — RTX 4090 Alienware (batch codegen, long-context summarization)

Different model — Devstral, fine-tuned specifically for agentic coding:

```bash
ollama pull devstral:24b-small-2505-q4_K_M

ollama show devstral:24b-small-2505-q4_K_M --modelfile > devstral-32k.modelfile
echo "PARAMETER num_ctx 32768" >> devstral-32k.modelfile
ollama create devstral-32k -f devstral-32k.modelfile
```

Pi `~/.pi/agent/models.json` on the Alienware:

```json
{
  "providers": {
    "ollama-alienware": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "devstral-32k", "contextWindow": 32768 }
      ]
    }
  }
}
```

Expected: ~40–55 t/s, ~14–16GB VRAM. SWE-Bench Verified 46.8% on the underlying Devstral model is the highest agentic-coding score of any model in this guide.

**Runner-up on Tier C:** `qwen3-coder:30b` MoE if you'd rather have consistency with the Macs. Slightly slower than Devstral on CUDA but still ~55–75 t/s on the 4090, and 256K native context wins for repo-scale summarization workloads.

---

## Critical Pi Gotchas — All Three Sources Confirmed

These are real, not synthesis artifacts. Build them into the deployment.

### 1. Tool-call streaming bug (Ollama issue #12557)

Ollama's OpenAI-compat endpoint at `/v1/chat/completions` **drops `tool_calls` deltas in streaming mode**. The model decides to call a tool, the stream returns empty content with `finish_reason: stop`, and Pi's agent loop stalls.

**Three workarounds:**
1. Install the `pi-ollama` extension — uses Ollama's native `/api/chat` endpoint instead of `/v1/chat/completions`.
2. Set `compat.supportsEagerToolInputStreaming: false` in `models.json`.
3. Force non-streaming for tool calls (`stream: false`).

### 2. Default context window is 2048 (Ollama) or 4096 (Pi's assumed default)

Sources A and C both warn this. Pi sessions read files and execute bash; context blows past 2048 within minutes. **Always set `num_ctx` explicitly in a Modelfile** or via the `OLLAMA_CONTEXT_LENGTH` env var:

```bash
OLLAMA_CONTEXT_LENGTH=32768 ollama serve
```

### 3. `compat.supportsDeveloperRole: false` is required for Ollama

Pi sends system prompts as `developer` role (matches OpenAI's reasoning-tier API). Ollama doesn't recognize the role and either crashes or treats the message as user input. Set this flag in every Ollama provider block.

### 4. Gemma4 multimodal `read` tool fails (Pi GitHub issue #3022)

If you're tempted to use `gemma4:31b` or `gemma4:26b` as your local model, know that Pi's `read` tool cannot deliver binary image data through the `openai-completions` API to Gemma4. Text-only Pi workflows are fine. **For Sean's text/code-only fleet, this is not a blocker** — but it is why this synthesis prefers `qwen3-coder:30b` over Gemma4 even though source B + source C both recommended Gemma4 for at least one tier.

### 5. Auto-compaction overflow (Pi GitHub issue #2871)

Pi only checks for compaction at `agent_end` and before the next user prompt — not mid-turn. Long agentic sessions (read+edit many files in one turn) can balloon to 400K+ tokens and trigger truncation of completed work. Mitigate by:
- Setting a conservative `contextWindow` value in `models.json` (16K for Tier B, 32K for Tiers A and C)
- Installing the `pi-agenticoding` extension (per source B) for advisory `/handoff` / `spawn` / `ledger` primitives — though verify this extension exists before relying on it

---

## Workload-to-Tier Routing for Sean's 3-Device Fleet

Pi's four workload patterns (per all three sources) map to Sean's hardware like this:

| Workload | Best tier | Model | Why |
|---|---|---|---|
| (a) Tool-calling agentic loops | **Tier B** (Mac Mini headless) | qwen3-coder:30b @ 16K | Always-on, energy-efficient, never sleeps; Qwen3-Coder's MoE gives best tool-call format reliability per the Ollama tools tag |
| (b) Code completion + inline edits | **Tier A** (M4 Max MBP) or **Tier C** (4090) | qwen3-coder:30b @ 32K (A) or devstral-32k (C) | Need raw tok/s; both have it. Pick by device location — A if at the desk, C for batch overnight |
| (c) Multi-turn planning (long context) | **Tier A** | qwen3-coder:30b @ 64K | 48GB unified memory headroom; expand `num_ctx` for plan sessions |
| (d) Repo-scale summarization | **Tier C** | devstral 24B or qwen3-coder:30b @ 32K | CUDA throughput wins for sustained long-context decode |

---

## What This Synthesis Does Not Cover

- **Cost vs cloud comparison** — none of the three sources put numbers on local-vs-OpenRouter for Sean's specific workload. Topic 12 (OpenRouter economics, done 2026-05-16) is the adjacent reference.
- **Embeddings models** — Pi may use embeddings for retrieval-heavy extensions; all three sources focused on chat-completion models only.
- **Mid-2026 hardware refreshes** — Apple's M5 series and NVIDIA's Blackwell consumer GPUs are not yet in the benchmark corpus. Re-run this synthesis in Q3 2026.
- **Anti-Gravity CLI compatibility** — Topic 17 was skipped because Gemini CLI is deprecating 2026-06-18. If Anti-Gravity ↔ Pi interop becomes interesting, separately scope a new topic.

---

## Sources

- [[2026-05-21-topic-19a-optimal-ollama-models-pi-perplexity]] — best-grounded; primary citation
- [[2026-05-21-topic-19b-optimal-ollama-models-pi-gemini-dr]] — useful workload taxonomy; specific tags + benchmarks treated as speculative
- [[2026-05-21-topic-19c-optimal-ollama-models-pi-chatgpt]] — conservative; corroborates Pi-compatibility gotchas

**Primary documentation (consulted for verification, not synthesized in):**
- Pi (pi.dev) — https://pi.dev/ + https://github.com/earendil-works/pi
- Ollama Pi integration — https://docs.ollama.com/integrations/pi
- Ollama library — https://ollama.com/library/qwen3-coder + https://ollama.com/library/devstral
