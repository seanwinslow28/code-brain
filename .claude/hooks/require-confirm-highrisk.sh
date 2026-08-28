#!/bin/bash
# PreToolUse hook (matcher: Bash): gate destructive shell commands.
#
# Payload contract (measured 2026-08-28 against Claude Code, not assumed):
#   {"hook_event_name":"PreToolUse","tool_name":"Bash",
#    "tool_input":{"command":"...","description":"..."}, ...}
# The tool name is `tool_name` (NOT `tool`); the command lives at
# `tool_input.command` (NOT top-level `command`). The previous version read a
# `"tool"` field that has never existed, so TOOL_NAME was always empty and this
# guard exited 0 on every call -- 16,888 recorded no-op runs in
# .claude/tool-use.log between 2026-02-15 and 2026-08-28.
#
# Portability: macOS ships bash 3.2, so no namerefs (`local -n`), no
# associative arrays, no `${var,,}`. Parallel indexed arrays only.
#
# Decisions: deny (exit 2) | ask (JSON on stdout, exit 0) | allow (exit 0).
# CLAUDE_ALLOW_HIGHRISK=true downgrades deny -> ask. It is an escape hatch,
# not a bypass.
#
# Regression suite: .claude/hooks/tests/test-hooks.sh

set -uo pipefail

HOOK_DATA=$(cat)

# Parse with python3 so escaped quotes/newlines in the command cannot truncate
# the value the way the old `grep -o '"[^"]*"'` did.
PARSED=$(printf '%s' "$HOOK_DATA" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
except Exception:
    print("PARSE_ERROR"); print(""); sys.exit(0)
print(d.get("tool_name", ""))
print((d.get("tool_input") or {}).get("command", "").replace("\n", " "))
' 2>/dev/null)

TOOL_NAME=$(printf '%s\n' "$PARSED" | sed -n '1p')
COMMAND=$(printf '%s\n' "$PARSED" | sed -n '2p')

# Fail CLOSED on a payload we cannot read. Silent fail-open is the bug we are
# fixing; an unreadable payload is not something this hook can vouch for.
if [ "$TOOL_NAME" = "PARSE_ERROR" ] || [ -z "$PARSED" ]; then
    echo "require-confirm-highrisk: unparseable hook payload; denying." >&2
    exit 2
fi

[ "$TOOL_NAME" = "Bash" ] || exit 0
[ -n "$COMMAND" ] || exit 0

# --- Catastrophic: deny --------------------------------------------------
DENY_PAT=(
  'rm[[:space:]]+-[a-zA-Z]*[rR][a-zA-Z]*[[:space:]]+(/|/\*|~|\$HOME)([[:space:]]|$)'
  '\bmkfs(\.[a-z0-9]+)?[[:space:]]'
  '\bdd\b[^|]*\bof=/dev/(disk|rdisk|sd|nvme|hd)'
  '\bdiskutil[[:space:]]+(eraseDisk|eraseVolume|zeroDisk|reformat|partitionDisk)'
  '\bfdisk[[:space:]]'
  ':[[:space:]]*\(\)[[:space:]]*\{.*\|.*&.*\}[[:space:]]*;[[:space:]]*:'
  '\bsudo[[:space:]]+rm[[:space:]]+-[a-zA-Z]*[rR]'
)
DENY_LBL=(
  'recursive delete of / or $HOME'
  'filesystem format (mkfs)'
  'raw disk write via dd'
  'destructive diskutil operation'
  'disk partitioning (fdisk)'
  'fork bomb'
  'sudo recursive delete'
)

# --- Destructive but sometimes intended: ask -----------------------------
ASK_PAT=(
  '\brm[[:space:]]+-[a-zA-Z]*[rR]'
  '\brm[[:space:]]+-[a-zA-Z]*f'
  '\bchmod[[:space:]]+(-[a-zA-Z]+[[:space:]]+)?777\b'
  '\bsudo[[:space:]]+(rm|mv|cp|chmod|chown|dd|tee)\b'
  '>[[:space:]]*/dev/(disk|rdisk|sd|nvme|hd)'
  '\bgit[[:space:]]+(checkout|restore)[[:space:]]+\.[[:space:]]*$'
)
ASK_LBL=(
  'recursive delete (rm -r)'
  'force delete (rm -f)'
  'world-writable chmod 777'
  'sudo filesystem mutation'
  'redirect into a raw device'
  'discard all working-tree changes'
)
# Deliberately NOT matched -- the old list would have blocked all of these the
# moment parsing was fixed:
#   "format"     -> git log --format=, npm run format
#   "> /dev/"    -> > /dev/null, 2>/dev/null
#   "chmod +x /" -> chmod +x /Users/<you>/bin/tool

emit_ask() {  # $1 = reason
    python3 -c '
import json, sys
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": sys.argv[1]}}))' "$1"
}

i=0
while [ $i -lt ${#DENY_PAT[@]} ]; do
    if printf '%s' "$COMMAND" | grep -qiE "${DENY_PAT[$i]}"; then
        LABEL="${DENY_LBL[$i]}"
        if [ "${CLAUDE_ALLOW_HIGHRISK:-false}" = "true" ]; then
            emit_ask "High-risk ($LABEL); CLAUDE_ALLOW_HIGHRISK downgraded deny to ask."
            exit 0
        fi
        echo "BLOCKED (deny): $LABEL" >&2
        echo "Command: $COMMAND" >&2
        echo "Set CLAUDE_ALLOW_HIGHRISK=true to downgrade this to a confirmation prompt." >&2
        exit 2
    fi
    i=$((i + 1))
done

i=0
while [ $i -lt ${#ASK_PAT[@]} ]; do
    if printf '%s' "$COMMAND" | grep -qiE "${ASK_PAT[$i]}"; then
        emit_ask "Destructive command (${ASK_LBL[$i]}). Confirm before running."
        exit 0
    fi
    i=$((i + 1))
done

exit 0
