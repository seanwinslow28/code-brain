#!/bin/bash
# PostToolUse hook (matcher: Write|Edit): auto-format the edited file.
# Non-blocking; always exits 0.
#
# Contract (measured 2026-08-28): the path lives at `tool_input.file_path`.
# The previous version read a top-level `"target"` with a `||` fallback to
# `"file_path"` -- but a `grep | cut` pipeline exits with cut's status (0) even
# when grep matches nothing, so the fallback never fired and FILE_PATH was
# always empty. This hook had never formatted a file.
#
# Inert unless `prettier` / `black` are on PATH.

HOOK_DATA=$(cat)

FILE_PATH=$(printf '%s' "$HOOK_DATA" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
except Exception:
    print(""); sys.exit(0)
ti = d.get("tool_input") or {}
print(ti.get("file_path") or ti.get("notebook_path") or "")
' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json|*.css|*.scss|*.md)
        if command -v prettier >/dev/null 2>&1; then
            prettier --write "$FILE_PATH" >/dev/null 2>&1 &
        fi
        ;;
    *.py)
        if command -v black >/dev/null 2>&1; then
            black "$FILE_PATH" >/dev/null 2>&1 &
        fi
        ;;
esac

exit 0
