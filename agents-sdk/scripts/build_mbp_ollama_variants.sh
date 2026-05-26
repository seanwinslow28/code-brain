#!/usr/bin/env bash
# Build 32K-context variants of the 5 MBP-Ollama Topic 21 candidates.
# Runs over SSH from Mac Mini against the MBP. Mirrors the Tier C variant naming
# convention so the aggregator can three-way compare same-model-different-runtime.
#
# Run after pulls complete; idempotent (ollama create overwrites existing variants).

set -euo pipefail

MBP_USER="seanwinslow"
MBP_HOST="seans-macbook-pro.local"

# base_tag → variant_name
declare -a PAIRS=(
  "qwen3.5:27b qwen3.5_27b-32k"
  "qwen3.5:35b-a3b qwen3.5_35b-a3b-32k"
  "qwen3.6:27b qwen3.6_27b-32k"
  "qwen3.6:35b-a3b qwen3.6_35b-a3b-32k"
  "qwen3-coder:30b qwen3-coder_30b-32k"
)

for pair in "${PAIRS[@]}"; do
  read -r base variant <<<"$pair"
  echo "--- $base → $variant ---"
  ssh "${MBP_USER}@${MBP_HOST}" bash <<EOF
export PATH=/opt/homebrew/bin:\$PATH
if ! ollama list | grep -q "^${base%:*}\s\+${base#*:}\|^${base} "; then
  # Try alternate match (base tag listing convention)
  if ! ollama list | awk '{print \$1}' | grep -Fxq "${base}"; then
    echo "SKIP: base tag '${base}' not present on MBP — pull first."
    exit 0
  fi
fi
TMPFILE=\$(mktemp /tmp/${variant}.modelfile.XXXX)
echo "FROM ${base}" > "\$TMPFILE"
echo "PARAMETER num_ctx 32768" >> "\$TMPFILE"
ollama create "${variant}" -f "\$TMPFILE"
rm -f "\$TMPFILE"
EOF
done

echo ""
echo "=== Final MBP variant inventory ==="
ssh "${MBP_USER}@${MBP_HOST}" 'export PATH=/opt/homebrew/bin:$PATH; ollama list'
