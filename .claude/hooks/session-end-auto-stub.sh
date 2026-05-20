#!/bin/bash
# SessionEnd hook — auto-create minimal person stubs for new [[Name]]
# wikilinks discovered in author: YAML frontmatter. See
# agents-sdk/scripts/auto_stub_people.py for filter logic.
#
# Fire-and-forget: detached, must return <100ms so session close isn't
# blocked. Any failure inside the script logs to
# vault/90_system/agent-logs/auto-stub-people.log and exits 0 — the hook
# never fails the session.

set -u

# Recursion guard: if invoked from inside the script's child process tree.
if [ "${CLAUDE_INVOKED_BY:-}" = "auto-stub" ]; then
    exit 0
fi

REPO_ROOT="/Users/seanwinslow/Code-Brain/code-brain"
SCRIPT="$REPO_ROOT/agents-sdk/scripts/auto_stub_people.py"
VENV_PY="$REPO_ROOT/agents-sdk/.venv/bin/python3"
LOG_DIR="$REPO_ROOT/vault/90_system/agent-logs"
mkdir -p "$LOG_DIR"

if [ ! -x "$VENV_PY" ] || [ ! -f "$SCRIPT" ]; then
    exit 0
fi

# Fire and forget.
CLAUDE_INVOKED_BY=auto-stub \
    nohup env PYTHONPATH="$REPO_ROOT/agents-sdk" \
    "$VENV_PY" "$SCRIPT" \
    >"$LOG_DIR/session-end-auto-stub.log" 2>&1 &
disown

exit 0
