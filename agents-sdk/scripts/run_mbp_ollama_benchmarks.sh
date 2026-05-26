#!/usr/bin/env bash
# Run benchmark_ollama_model.py against MBP-Ollama for the 5 Topic 21 candidates.
# Sequentially (per prior session memory: avoid memory pressure from parallel sweeps).
# Output lands in agents-sdk/benchmarks/topic_20/results/<slug>-tierA-ollama-<date>.jsonl
# and is picked up by aggregate.py under the new "A-ollama" tier bucket.

set -euo pipefail

cd "$(dirname "$0")/.."

MBP_HOST="http://seans-macbook-pro.local:11434"
TIER="A-ollama"

# 5 32K-context variants on MBP
declare -a VARIANTS=(
  "qwen3.5_27b-32k"
  "qwen3.5_35b-a3b-32k"
  "qwen3.6_27b-32k"
  "qwen3.6_35b-a3b-32k"
  "qwen3-coder_30b-32k"
)

for variant in "${VARIANTS[@]}"; do
  echo ""
  echo "=== [$(date +%H:%M:%S)] benchmarking ${variant} on MBP-Ollama ==="
  PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
    --model "${variant}" \
    --host "${MBP_HOST}" \
    --tier "${TIER}" \
    --num-ctx 32768
  echo "=== [$(date +%H:%M:%S)] done ${variant} ==="
done

echo ""
echo "=== All MBP-Ollama benchmarks complete; aggregating ==="
.venv/bin/python3 benchmarks/topic_20/aggregate.py
