#!/bin/bash
# PreCompact hook — spawn flush.py detached BEFORE Claude Code auto-compacts
# the session, so pre-compact knowledge isn't silently lost. Mirrors
# `session-end-flush.sh`; the only diff is `--trigger pre-compact`.
#
# Must return <100ms so compaction isn't blocked. Any failure is silent
# (hook exit 0). Recursion-guarded via CLAUDE_INVOKED_BY.
#
# Input (from Claude Code): JSON on stdin containing `transcript_path` and
# other session metadata. We grep for the path rather than pulling in jq.

set -u

# Recursion guard: if this hook was itself invoked from inside flush.py's
# child process tree, bail out quietly.
if [ "${CLAUDE_INVOKED_BY:-}" = "flush" ]; then
    exit 0
fi

REPO_ROOT="/Users/seanwinslow/Code-Brain/code-brain"
AGENT="$REPO_ROOT/agents-sdk/agents/flush.py"
VENV_PY="$REPO_ROOT/agents-sdk/.venv/bin/python3"
LOG_DIR="$REPO_ROOT/vault/90_system/agent-logs"
mkdir -p "$LOG_DIR"

# Read stdin (non-blocking, up to 64KB) and pull transcript_path.
INPUT=$(head -c 65536 2>/dev/null || true)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" \
    | grep -o '"transcript_path"[[:space:]]*:[[:space:]]*"[^"]*"' \
    | head -1 \
    | sed 's/.*:[[:space:]]*"\(.*\)"/\1/')

if [ ! -x "$VENV_PY" ] || [ ! -f "$AGENT" ]; then
    exit 0
fi

FLUSH_ARG="--latest"
if [ -n "${TRANSCRIPT_PATH:-}" ] && [ -f "$TRANSCRIPT_PATH" ]; then
    FLUSH_ARG="--transcript $TRANSCRIPT_PATH"
fi

# Fire and forget. PYTHONPATH is required for `lib.*` imports.
CLAUDE_INVOKED_BY=flush \
    nohup env PYTHONPATH="$REPO_ROOT/agents-sdk" \
    "$VENV_PY" "$AGENT" $FLUSH_ARG --trigger pre-compact \
    >"$LOG_DIR/pre-compact-flush.log" 2>&1 &
disown

exit 0
