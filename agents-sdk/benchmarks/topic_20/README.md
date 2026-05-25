# Topic 20 — Fleet Model Refresh Benchmarks

Reusable benchmark harness for evaluating candidate models against the
current production fleet across Sean's 3-tier hardware. Driven by two scripts:

- `agents-sdk/scripts/benchmark_ollama_model.py` — talks to Ollama `/api/chat` (Tiers B, C)
- `agents-sdk/scripts/benchmark_lmstudio_model.py` — talks to LM Studio OpenAI-compat `/v1/chat/completions` (Tier A)

## Run a single model

```bash
cd agents-sdk

# Tier B / Tier C — Ollama
PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
    --model qwen3.5_27b-32k \
    --host http://192.168.68.201:11434 \
    --tier C --num-ctx 32768

# Tier A — LM Studio MLX
PYTHONPATH=. .venv/bin/python3 scripts/benchmark_lmstudio_model.py \
    --model qwen3.5-27b \
    --host http://seans-macbook-pro.local:1234 \
    --tier A --num-ctx 32768
```

## Aggregate results

```bash
.venv/bin/python3 benchmarks/topic_20/aggregate.py
```

Prints one markdown table per tier with per-model scorecards.

## Prompts

- `prompts/tool_calls.jsonl` — 20 single-turn tool-call prompts, 4 schemas.
- `prompts/agentic_loops.jsonl` — 10 multi-step "Pi-style" sessions.
- `prompts/needle_haystack.py` — generates a 32K-token prompt with a needle at the 28K mark.

## Dimensions captured per (model, tier) pair

1. Tool-call JSON validity (% pass) — 20 probes × 4 tool schemas
2. Decode tok/s on a fixed 1024-token output (mean ± stddev, 3 runs)
3. Peak memory footprint (sampled out-of-band via `scripts/sample_ollama_rss.sh`)
4. Agentic-loop reliability — Pi-style multi-step (manual scoring, future work)
5. Long-context recall at 28K position inside 32K window (5 runs)
6. Pi-specific gotcha checks (5 binary tests)

## Harness fixes captured during 2026-05-25 execution

- **Ollama harness** — pass `think: false` at top of body (Qwen3.5/3.6 family
  defaults to thinking mode; without this, `message.content` is empty and
  all tool_call probes fail. Verified against qwen3.5:9b.)
- **LM Studio harness** — bump `max_tokens` from default 512 / 32 to **2048 / 512**
  for tool_call / needle suites. LM Studio's MLX-quantized Qwen3.5/3.6 do
  not expose a thinking-disable flag (`chat_template_kwargs.enable_thinking=false`
  is ignored). Workaround: give the model enough budget to finish thinking AND
  produce real content. Adds ~100-400 tokens of thinking overhead per probe.

## Pulled models (state as of 2026-05-25)

| Tier | Host | Runtime | Base tag | Custom variant | num_ctx | Disk |
|---|---|---|---|---|---|---|
| **A** | MBP M4 Max 48GB | LM Studio MLX | `qwen3-14b` | (production baseline) | 40K | ~9 GB |
| A | MBP | LM Studio MLX | `qwen/qwen3-coder-30b` (A3B MoE) | — | 256K | ~17 GB |
| A | MBP | LM Studio MLX | `qwen3.5-27b` (dense) | — | 256K | ~15 GB |
| A | MBP | LM Studio MLX | `qwen3.5-35b-a3b` (MoE 3B active) | — | 256K | ~20 GB |
| A | MBP | LM Studio MLX | `qwen3.6-27b-mlx` (dense) | — | 256K | ~15 GB |
| A | MBP | LM Studio MLX | `qwen3.6-35b-a3b-mlx` (MoE 3B active) | — | 256K | ~20 GB |
| **B** | Mac Mini M4 Pro 24GB | Ollama | `gemma4:e4b` (production) | `gemma4_e4b-16k` | 16K | 9.6 GB |
| B | Mac Mini | Ollama | `qwen3.5:9b` | `qwen3.5_9b-16k` | 16K | 6.6 GB |
| B | Mac Mini | Ollama | `qwen3.5:27b` ✗ | (overflow — see notes) | — | 17 GB |
| B | Mac Mini | Ollama | `qwen3.6:27b` ✗ | (overflow) | — | 17 GB |
| B | Mac Mini | Ollama | `gemma4:26b` ✗ | (overflow) | — | 17 GB |
| **C** | Alienware RTX 5080 16GB | Ollama | `qwen3.5:9b` | `qwen3.5_9b-32k` | 32K | 6.6 GB |
| C | Alienware | Ollama | `devstral:24b-small-2505-q4_K_M` | `devstral_24b-32k` | 32K | 14 GB |
| C | Alienware | Ollama | `qwen3.5:27b` | `qwen3.5_27b-32k` | 32K | 17 GB |
| C | Alienware | Ollama | `qwen3.6:27b` | `qwen3.6_27b-32k` | 32K | 17 GB |
| C | Alienware | Ollama | `gemma4:26b` (MoE 3.8B) | `gemma4_26b-32k` | 32K | 17 GB |
| C | Alienware | Ollama | `nemotron3:33b` | `nemotron3_33b-32k` | 32K | 27 GB |

### Tier B 17 GB models — rerouted

The plan's Hardware Budget table called `qwen3.5:27b` / `gemma4:26b` / `qwen3.6:27b`
"tight" on the Mac Mini's 24 GB unified memory. In practice they overflow even at
16K context: Ollama splits 80/20 GPU/CPU, memory thrashes (1.5M swapouts observed),
and requests time out. These candidates are benchmarked on:

- **Tier A** (MBP 48 GB unified) — they fit comfortably in LM Studio
- **Tier C** (Alienware 16 GB VRAM + 64 GB DDR5 with controlled offload) — they run with modest performance penalty

The Mac Mini practical Tier B ceiling is ~10–12 GB models at 16K context.

### Rollback (per-host)

```bash
# Mac Mini (Tier B)
for tag in qwen3.5:9b qwen3.5_9b-16k gemma4_e4b-16k; do
  ollama rm "$tag" || true
done
# Note: gemma4:26b, qwen3.5:27b, qwen3.6:27b on Mac Mini can stay or be removed —
# they were pulled but couldn't be benchmarked. ~51 GB recoverable if removed.

# Alienware (Tier C) — run while machine is awake
ssh seanw@192.168.68.201 'for tag in qwen3.5:9b qwen3.5_9b-32k devstral:24b-small-2505-q4_K_M devstral_24b-32k qwen3.5:27b qwen3.5_27b-32k qwen3.6:27b qwen3.6_27b-32k gemma4:26b gemma4_26b-32k nemotron3:33b nemotron3_33b-32k; do ollama rm "$tag" || true; done'

# MBP (Tier A, LM Studio) — use LM Studio UI to remove from My Models
# Or delete model directories under ~/.cache/lm-studio/models/
```

## Output

Raw results land at `results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl` (Ollama) or
`results/<model-slug>-<tier>-lmstudio-<YYYY-MM-DD>.jsonl` (LM Studio). Each line is
one measurement record with a `kind` field disambiguating (`tool_call`,
`throughput`, `needle`, `pi_gotcha`).

Synthesis lives at `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`.
