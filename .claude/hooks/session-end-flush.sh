#!/bin/bash
# SessionEnd hook — spawn flush.py detached to extract session knowledge.
# Must return <100ms so session close isn't blocked. Any failure is silent
# (hook exit 0) except recursion/env issues which use exit 2 per CLAUDE.md.
#
# Input (from Claude Code): JSON on stdin containing `transcript_path` and
# other session metadata. We grep for the path rather than pulling in jq.

set -u

# Recursion guard: if this hook was itself invoked from inside flush.py's
# child process tree, bail out quietly.
if [ "${CLAUDE_INVOKED_BY:-}" = "flush" ]; then
    exit 0
fi

REPO_ROOT="/Users/seanwinslow/Code-Brain/claude-code-superuser-pack"
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
    "$VENV_PY" "$AGENT" $FLUSH_ARG \
    >"$LOG_DIR/session-end-flush.log" 2>&1 &
disown

exit 0
