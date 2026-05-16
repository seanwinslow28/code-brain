#!/bin/bash
# schedule_wakes.sh
#
# Queues the next 7 days of pmset wake events for the MBP agent fleet.
# Run nightly via /Library/LaunchDaemons/com.sean.agent-fleet-wake-scheduler.plist
# (as root — no sudo needed inside this script when invoked from a LaunchDaemon).
#
# Manual run for testing:
#   sudo /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/schedule_wakes.sh
#
# Inspect queue:
#   pmset -g sched

set -euo pipefail

LOG_PREFIX="[schedule_wakes $(date '+%Y-%m-%d %H:%M:%S')]"
echo "$LOG_PREFIX starting"

# --- Wake schedule (24h format) ----------------------------------------------
# Each entry: "DOW_PATTERN HH:MM   # comment"
#   DOW pattern: "*" = every day,  "1-5" = Mon–Fri,  "4" = Thursday only
#   DOW numbers: 1=Mon  2=Tue  3=Wed  4=Thu  5=Fri  6=Sat  7=Sun  (POSIX)
WAKES=(
  "*   02:25"   # Vault Synthesizer (2:30 AM daily)        — MBP-hosted Qwen3-14B
  "1-5 07:55"   # Job Feed window opens (8:00 AM weekdays) — MBP via HybridRouter
  "1-5 09:25"   # Mid-window Job Feed fire keep-alive
  "1-5 10:55"   # End-of-window Job Feed fire keep-alive
  "4   17:55"   # Substack-Drafter (Thu 18:00, opt-in)     — MBP via HybridRouter
  "7   21:55"   # Knowledge Lint Tier 2 (Sun 22:00)        — MBP Qwen3-14B if awake
)

# --- Wipe old one-shot events (does NOT touch `pmset repeat`) ----------------
pmset schedule cancelall 2>/dev/null || true

# --- Queue next 7 days -------------------------------------------------------
queued=0
for i in $(seq 0 6); do
  d=$(date -v +"${i}"d +%m/%d/%Y)
  dow=$(date -v +"${i}"d +%u)   # 1=Mon ... 7=Sun

  for entry in "${WAKES[@]}"; do
    pattern=$(echo "$entry" | awk '{print $1}')
    hhmm=$(echo "$entry"    | awk '{print $2}')

    match=0
    if   [[ "$pattern" == "*" ]]; then
      match=1
    elif [[ "$pattern" == *-* ]]; then
      lo="${pattern%-*}"; hi="${pattern#*-}"
      (( dow >= lo && dow <= hi )) && match=1
    elif [[ "$pattern" == "$dow" ]]; then
      match=1
    fi

    if (( match )); then
      pmset schedule wakeorpoweron "${d} ${hhmm}:00"
      queued=$((queued + 1))
    fi
  done
done

echo "$LOG_PREFIX queued $queued wake events through $(date -v +6d +%Y-%m-%d)"
pmset -g sched | head -50
