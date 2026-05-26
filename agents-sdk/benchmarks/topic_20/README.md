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

## Pulled models (state as of 2026-05-26 post-cleanup)

After Topic 20 closed (2026-05-25), Tier B 17 GB models that couldn't run were
removed from Mac Mini, and Tier A LM Studio Topic 20 candidates that
underperformed the baseline were removed from MBP. A 5-model MBP-Ollama
sweep was pulled to test the LM Studio thinking-disable hypothesis (Topic 20
Open Question §"MBP Ollama runtime trial"). Disk reclaim: ~205 GB across
the fleet.

| Tier | Host | Runtime | Base tag | Custom variant | num_ctx | Disk |
|---|---|---|---|---|---|---|
| **A (LM Studio)** | MBP M4 Max 48GB | LM Studio MLX | `qwen3-14b` | (production baseline) | 40K | ~9 GB |
| **A-ollama** | MBP M4 Max 48GB | Ollama (MLX backend) | `qwen3.5:27b` (dense) | `qwen3.5_27b-32k` | 32K | ~17 GB |
| A-ollama | MBP | Ollama | `qwen3.5:35b-a3b` (MoE 3B active) | `qwen3.5_35b-a3b-32k` | 32K | ~20 GB |
| A-ollama | MBP | Ollama | `qwen3.6:27b` (dense) | `qwen3.6_27b-32k` | 32K | ~17 GB |
| A-ollama | MBP | Ollama | `qwen3.6:35b-a3b` (MoE 3B active) | `qwen3.6_35b-a3b-32k` | 32K | ~20 GB |
| A-ollama | MBP | Ollama | `qwen3-coder:30b` (A3B MoE) | `qwen3-coder_30b-32k` | 32K | ~16 GB |
| **B** | Mac Mini M4 Pro 24GB | Ollama | `gemma4:e4b` (production) | `gemma4_e4b-16k` | 16K | 9.6 GB |
| B | Mac Mini | Ollama | `qwen3:14b` / `qwen3-14b-research` | (deep_researcher LDR) | 32K | 9.3 GB |
| B | Mac Mini | Ollama | `phi4-mini-reasoning` | — | 4K | 3.2 GB |
| B | Mac Mini | Ollama | `nomic-embed-text` | (nightly indexer) | — | 274 MB |
| **C** | Alienware RTX 5080 16GB | Ollama | `qwen3.5:9b` | `qwen3.5_9b-32k` | 32K | 6.6 GB |
| C | Alienware | Ollama | `devstral:24b-small-2505-q4_K_M` (TBD — Topic 21) | `devstral_24b-32k` | 32K | 14 GB |
| C | Alienware | Ollama | `qwen3.5:27b` (batch-quality) | `qwen3.5_27b-32k` | 32K | 17 GB |
| C | Alienware | Ollama | **`gemma4:26b`** (Tier C production) | `gemma4_26b-32k` | 32K | 17 GB |
| C | Alienware | Ollama | `nemotron3:33b` (TBD — Topic 21) | `nemotron3_33b-32k` | 32K | 27 GB |
| C | Alienware | Ollama | `qwen3-vl:8b` (vision) | — | — | 6.1 GB |

### Removed 2026-05-26 (Topic 20 cleanup)

- **Mac Mini:** `gemma4:26b` + `qwen3.5:27b` + `qwen3.6:27b` (all 17 GB, overflowed
  Mac Mini's 24 GB unified memory — couldn't run reliably even at 16K) +
  `qwen3.5:9b` (lost the Tier B benchmark on both axes vs `gemma4:e4b`).
  ~58 GB reclaimed (APFS purgeable; full reclaim after Time Machine rotation).
- **MBP (LM Studio):** all 5 Topic 20 candidates (`Qwen3.5-27B-4bit`,
  `Qwen3.5-35B-A3B-4bit`, `Qwen3.6-27B-MLX-4bit`, `Qwen3.6-35B-A3B-MLX-4bit`,
  `Qwen3-Coder-30B-A3B-Instruct-MLX-4bit`) + 2 pre-Topic-20 exploration models
  (`gemma-4-31B-it-MLX-4bit` dense, `Qwen2.5-Coder-32B-Instruct-4bit`).
  +128 GB reclaimed immediately.
- **Alienware:** `qwen3.6:27b` + `qwen3.6_27b-32k` (20 % schema match — worst in
  Tier C sweep, no utility). +17.4 GB reclaimed.

### Tier B 17 GB models — confirmed unusable on Mac Mini

Per the Topic 20 finding documented in the synthesis report: the practical Tier B
ceiling on Mac Mini's 24 GB unified memory is **~10–12 GB models at 16K context**.
17 GB models overflow (Ollama splits 80/20 GPU/CPU, 1.5 M swapouts in a 15-min
window, requests time out). They have been removed from Mac Mini; the same
candidates run on Alienware Tier C with controlled DDR5 offload at acceptable
tok/s.

### Rollback (per-host, current state)

```bash
# Mac Mini (Tier B) — production set only
for tag in gemma4_e4b-16k gemma4:e4b qwen3-14b-research qwen3:14b nomic-embed-text phi4-mini-reasoning; do
  ollama rm "$tag" || true
done

# MBP (Tier A LM Studio) — remove production baseline
ssh seanwinslow@seans-macbook-pro.local 'rm -rf ~/.cache/huggingface/hub/models--mlx-community--Qwen3-14B-4bit ~/.lmstudio/models/mlx-community/Qwen3-14B-4bit'

# MBP (Tier A-ollama) — remove the new Topic 21 sweep
ssh seanwinslow@seans-macbook-pro.local 'export PATH=/opt/homebrew/bin:$PATH; for tag in qwen3.5:27b qwen3.5_27b-32k qwen3.5:35b-a3b qwen3.5_35b-a3b-32k qwen3.6:27b qwen3.6_27b-32k qwen3.6:35b-a3b qwen3.6_35b-a3b-32k qwen3-coder:30b qwen3-coder_30b-32k; do ollama rm "$tag" || true; done'

# Alienware (Tier C) — run while machine is awake
ssh seanw@192.168.68.201 'for tag in qwen3.5:9b qwen3.5_9b-32k devstral:24b-small-2505-q4_K_M devstral_24b-32k qwen3.5:27b qwen3.5_27b-32k gemma4:26b gemma4_26b-32k nemotron3:33b nemotron3_33b-32k; do ollama rm "$tag" || true; done'
```

## Output

Raw results land at `results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl` (Ollama) or
`results/<model-slug>-<tier>-lmstudio-<YYYY-MM-DD>.jsonl` (LM Studio). Each line is
one measurement record with a `kind` field disambiguating (`tool_call`,
`throughput`, `needle`, `pi_gotcha`).

Synthesis lives at `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`.
