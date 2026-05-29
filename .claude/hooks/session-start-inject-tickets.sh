#!/bin/bash
# SessionStart hook — inject the open Manual tickets (Todo + In Progress) from
# vault/00_inbox/tickets.md as `additionalContext` so each new Claude Code
# session starts aware of outstanding follow-ups (cost incidents, deferred
# fixes, "do this later" items) instead of losing them between sessions.
# These tickets also drive the Agent Fleet Observability kanban Manual lane.
# File-read-only; no LLM calls. Always exits 0 so a missing/broken tickets
# file never blocks session start.
#
# Output (stdout): SessionStart hook contract
#   {
#     "hookSpecificOutput": {
#       "hookEventName": "SessionStart",
#       "additionalContext": "## Open Manual Tickets ... <truncated>"
#     }
#   }
#
# Test override: TICKETS_PATH and TICKETS_MAX_CHARS env vars.

set -u

REPO_ROOT="/Users/seanwinslow/Code-Brain/code-brain"
DEFAULT_TICKETS="$REPO_ROOT/vault/00_inbox/tickets.md"
DEFAULT_MAX_CHARS=4000

TICKETS_PATH="${TICKETS_PATH:-$DEFAULT_TICKETS}"
MAX_CHARS="${TICKETS_MAX_CHARS:-$DEFAULT_MAX_CHARS}"

# Drain stdin (Claude Code may pipe session metadata; we don't use it).
head -c 65536 >/dev/null 2>&1 || true

# Build the JSON via Python (stdlib only — robust JSON escaping for
# arbitrary ticket contents). On any unexpected failure, emit the empty
# stub rather than blocking session start.
python3 - "$TICKETS_PATH" "$MAX_CHARS" <<'PYEOF' || cat <<'JSONFALLBACK'
import json
import sys
from pathlib import Path

tickets_path = Path(sys.argv[1])
try:
    max_chars = int(sys.argv[2])
except (ValueError, IndexError):
    max_chars = 4000

EMPTY_STUB = (
    "## Open Manual Tickets (vault/00_inbox/tickets.md)\n\n"
    "No open Todo or In Progress tickets. When work surfaces a follow-up "
    "that won't finish this session, append a one-line `-` bullet under "
    "`## Todo` in vault/00_inbox/tickets.md so it lands on the Agent Fleet "
    "Observability kanban Manual lane."
)


def _sections(text):
    """Return {section_title: [bullet, ...]} for top-level '## ' sections."""
    out = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            stripped = line.strip()
            # Top-level bullets only (mirror the kanban parser: sub-bullets
            # are indented and ignored).
            if line.startswith("- ") or line.startswith("* "):
                out[current].append(stripped)
    return out


body = EMPTY_STUB
if tickets_path.exists():
    try:
        content = tickets_path.read_text(encoding="utf-8")
    except OSError:
        content = ""
    secs = _sections(content)
    # Case-insensitive lookup for the two open lanes.
    lower = {k.lower(): v for k, v in secs.items()}
    todo = lower.get("todo", [])
    in_progress = lower.get("in progress", [])
    if todo or in_progress:
        parts = ["## Open Manual Tickets (vault/00_inbox/tickets.md)\n"]
        if in_progress:
            parts.append("### In Progress")
            parts.extend(in_progress)
            parts.append("")
        if todo:
            parts.append("### Todo")
            parts.extend(todo)
            parts.append("")
        parts.append(
            "_When a follow-up won't finish this session, add a `-` bullet "
            "under `## Todo` here before wrapping up._"
        )
        rendered = "\n".join(parts)
        if len(rendered) > max_chars:
            rendered = rendered[:max_chars] + "\n\n(truncated)\n"
        body = rendered

print(json.dumps(
    {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }
))
PYEOF
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"## Open Manual Tickets (vault/00_inbox/tickets.md)\n\nTickets file unavailable this session. When work surfaces a follow-up that won't finish this session, append a `-` bullet under `## Todo` in vault/00_inbox/tickets.md."}}
JSONFALLBACK

exit 0
