#!/bin/bash
# PostToolUse hook: audit trail of tool usage. Non-blocking; always exits 0.
#
# Contract (measured 2026-08-28): the tool name is `tool_name` (NOT `tool`) and
# file paths live under `tool_input` (NOT a top-level `target`/`file_path`).
# The previous version read the phantom `"tool"` field and wrote 16,888 rows of
# `tool= target=` between 2026-02-15 and 2026-08-28 -- an audit log with no
# audit in it. Parsed with python3 so escaped quotes cannot truncate values.

LOG_FILE="${CLAUDE_LOG_DIR:-.claude}/tool-use.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

HOOK_DATA=$(cat)

PARSED=$(printf '%s' "$HOOK_DATA" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
except Exception:
    print("unknown"); print("N/A"); sys.exit(0)
ti = d.get("tool_input") or {}
target = (ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
          or ti.get("pattern") or ti.get("command") or "N/A")
print(d.get("tool_name", "unknown"))
print(str(target).replace("\n", " ")[:200])
' 2>/dev/null)

TOOL_NAME=$(printf '%s\n' "$PARSED" | sed -n '1p')
TARGET=$(printf '%s\n' "$PARSED" | sed -n '2p')
[ -n "$TOOL_NAME" ] || TOOL_NAME="unknown"
[ -n "$TARGET" ] || TARGET="N/A"

mkdir -p "$(dirname "$LOG_FILE")"
echo "[$TIMESTAMP] tool=$TOOL_NAME target=$TARGET" >> "$LOG_FILE"
exit 0
