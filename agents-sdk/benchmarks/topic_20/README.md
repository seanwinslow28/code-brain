# Topic 20 — Fleet Model Refresh Benchmarks

Reusable benchmark harness for evaluating candidate Ollama models against
the current production fleet. Driven by `agents-sdk/scripts/benchmark_ollama_model.py`.

## Run a single model

    cd agents-sdk
    PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
        --model qwen3.5:27b \
        --host http://192.168.68.200:11434 \
        --tier B \
        --out benchmarks/topic_20/results/

## Prompts

- `prompts/tool_calls.jsonl` — 20 single-turn tool-call prompts, 4 schemas.
- `prompts/agentic_loops.jsonl` — 10 multi-step "Pi-style" sessions.
- `prompts/needle_haystack.py` — generates a 32K-token prompt with a needle
  at the 28K mark; produces a new haystack each call so models can't memorize.

## Dimensions captured per (model, tier) pair

1. Tool-call JSON validity (% pass)
2. Decode tok/s on a fixed 1024-token output (mean ± stddev, 3 runs)
3. Peak memory footprint during a 5-iter Pi-style session
4. Agentic-loop reliability (successful completions / 10)
5. Long-context recall at 28K (5 runs)
6. Pi-specific gotcha checks (5 binary tests)

## Output

Raw results land at `results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl`.
Each line is one prompt's full record. Aggregation lives in the synthesis
report at `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`.
