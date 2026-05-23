#!/usr/bin/env bash
# Sample ollama-server RSS every 2 seconds for the duration of a benchmark.
# Writes timestamped samples to benchmarks/topic_20/results/<host>-rss-<date>.csv
# Usage: ./sample_ollama_rss.sh <hostname-tag> [duration-seconds]
set -euo pipefail

HOST_TAG="${1:?host tag required, e.g., macmini / mbp / alienware}"
DURATION="${2:-600}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO_ROOT/benchmarks/topic_20/results/${HOST_TAG}-rss-$(date +%Y-%m-%d).csv"

echo "ts,rss_kb,vsz_kb" > "$OUT"
END=$(( $(date +%s) + DURATION ))
while [ "$(date +%s)" -lt "$END" ]; do
  LINE=$(ps -o rss=,vsz= -p "$(pgrep -x ollama | head -1)" 2>/dev/null || echo "0 0")
  RSS=$(echo "$LINE" | awk '{print $1}')
  VSZ=$(echo "$LINE" | awk '{print $2}')
  echo "$(date +%s),$RSS,$VSZ" >> "$OUT"
  sleep 2
done
echo "[sample_ollama_rss] wrote $OUT"
