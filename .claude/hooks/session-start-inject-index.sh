#!/bin/bash
# SessionStart hook — inject vault/knowledge/index.md as `additionalContext`
# so each new Claude Code session starts aware of the synthesized knowledge
# graph. File-read-only; no LLM calls. Always exits 0 so a missing/broken
# index never blocks session start.
#
# Output (stdout): SessionStart hook contract
#   {
#     "hookSpecificOutput": {
#       "hookEventName": "SessionStart",
#       "additionalContext": "## Knowledge Index ... <truncated>"
#     }
#   }
#
# Test override: KNOWLEDGE_INDEX_PATH and KNOWLEDGE_INDEX_MAX_CHARS env vars.

set -u

REPO_ROOT="/Users/seanwinslow/Code-Brain/code-brain"
DEFAULT_INDEX="$REPO_ROOT/vault/knowledge/index.md"
DEFAULT_MAX_CHARS=15000

INDEX_PATH="${KNOWLEDGE_INDEX_PATH:-$DEFAULT_INDEX}"
MAX_CHARS="${KNOWLEDGE_INDEX_MAX_CHARS:-$DEFAULT_MAX_CHARS}"

# Drain stdin (Claude Code may pipe session metadata; we don't use it).
head -c 65536 >/dev/null 2>&1 || true

# Build the JSON via Python (stdlib only — robust JSON escaping for
# arbitrary index contents). On any unexpected failure, emit the empty
# stub rather than blocking session start.
python3 - "$INDEX_PATH" "$MAX_CHARS" <<'PYEOF' || cat <<'JSONFALLBACK'
import json
import re
import sys
from pathlib import Path

index_path = Path(sys.argv[1])
try:
    max_chars = int(sys.argv[2])
except (ValueError, IndexError):
    max_chars = 15000

EMPTY_STUB = (
    "## Knowledge Index (vault/knowledge/index.md)\n\n"
    "The knowledge index is empty — vault_synthesizer has not yet "
    "generated concept or connection articles. The producer pipeline "
    "(SessionEnd flush → nightly synthesizer at 02:30) will populate "
    "it as you work."
)


def _has_real_articles(text: str) -> bool:
    """True if the index lists at least one wikilink or markdown link."""
    if re.search(r"\[\[[^\]]+\]\]", text):
        return True
    if re.search(r"\[[^\]\n]+\]\([^)]+\)", text):
        return True
    return False


if not index_path.exists():
    body = EMPTY_STUB
else:
    try:
        content = index_path.read_text(encoding="utf-8")
    except OSError:
        content = ""
    if not content.strip() or not _has_real_articles(content):
        body = EMPTY_STUB
    else:
        truncated = content[:max_chars]
        body = (
            "## Knowledge Index (vault/knowledge/index.md)\n\n"
            + truncated
            + "\n\n_To read any article, use the Read tool on the path shown._"
        )

print(json.dumps(
    {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }
))
PYEOF
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"## Knowledge Index (vault/knowledge/index.md)\n\nThe knowledge index is empty — vault_synthesizer has not yet generated concept or connection articles. The producer pipeline (SessionEnd flush → nightly synthesizer at 02:30) will populate it as you work."}}
JSONFALLBACK

exit 0
