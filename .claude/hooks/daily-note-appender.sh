#!/bin/bash
# Stop hook: Appends a session summary to today's Obsidian daily note.
# Runs when Claude Code stops (session ends or user triggers stop).
# Exit code 0 = success (hooks in Stop phase don't block).
#
# Session entries use Dataview inline fields for queryability:
#   - [time:: HH:MM] | [domain:: <domain>] | [context:: <project>] | **Outcomes:** <summary>

# Vault path — relative to this hook's location (.claude/hooks/)
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$HOOK_DIR/../../vault"
DAILY_NOTES_DIR="$VAULT_DIR/10_timeline/daily"
TEMPLATE_DIR="$VAULT_DIR/90_system/templates"
TODAY=$(date +%Y-%m-%d)
DAILY_NOTE="$DAILY_NOTES_DIR/$TODAY.md"

# Read stop data from stdin (JSON with session context)
STOP_DATA=$(cat)

# Extract the stop reason if available
STOP_REASON=$(echo "$STOP_DATA" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('stop_reason', 'manual'))
except:
    print('manual')
" 2>/dev/null)

# Only append if the daily notes directory exists (vault is accessible)
if [ ! -d "$DAILY_NOTES_DIR" ]; then
    # Vault not mounted/accessible — skip silently
    exit 0
fi

# Detect domain from working directory name.
# v3.15.0 structure: 3 primary domains (the-block, creative-studio, life-systems)
# nested under the repo root. Order matters — most-specific patterns first so
# they win against the generic repo-wide claude-mastery fallback.
WORK_DIR=$(pwd)
DOMAIN="unknown"
case "$WORK_DIR" in
    # --- Most-specific: nested project paths ---
    *creative-studio/16bitfit-battle-mode*|*16bitfit*|*16BitFit*) DOMAIN="creative-studio" ;;
    *creative-studio/design-team*) DOMAIN="creative-studio" ;;
    *the-block/product-management*) DOMAIN="the-block" ;;
    # --- Domain roots ---
    *the-block*|*theblock*) DOMAIN="the-block" ;;
    *creative-studio*|*animation*|*remotion*) DOMAIN="creative-studio" ;;
    *life-systems*|*finance*|*health*) DOMAIN="life-systems" ;;
    # --- Job hunt 2026 (post-Block) ---
    *job-hunt-2026*|*job-hunt*|*onwards-and-upwards*) DOMAIN="job-hunt" ;;
    # --- Block-specific keywords (route to the-block, not generic PM) ---
    *campus*|*etf*) DOMAIN="the-block" ;;
    # --- Vault path (specific) ---
    *vault*) DOMAIN="vault" ;;
    # --- Cross-cutting / generic fallback (LAST so specific patterns win) ---
    *claude-mastery*) DOMAIN="claude-mastery" ;;
    *superuser-pack*|*claude-code*) DOMAIN="claude-mastery" ;;
esac

# Detect project context from directory name
PROJECT_DIR=$(basename "$WORK_DIR")
CONTEXT=$(echo "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

# Create daily note if it doesn't exist (matching tpl-daily.md structure)
if [ ! -f "$DAILY_NOTE" ]; then
    cat > "$DAILY_NOTE" << EOF
---
type: daily
date: $TODAY
energy-peak: null
mood: null
---
# $TODAY

## Morning Focus (Manual — <2 min)
> What's the ONE thing that makes today successful?

**Focus:**

## Tasks

## Work Log
<!-- jira-log -->

## Claude Code Sessions
<!-- claude-sessions -->

## Side Project Notes
<!-- side-projects -->

## Evening Reflection (Manual — <2 min)
> What worked? What didn't? Carry forward?

**Win:**
**Lesson:**
**Carry forward:**
EOF
fi

# Append session entry below the <!-- claude-sessions --> anchor
TIMESTAMP=$(date +%H:%M)
SESSION_ENTRY="- [time:: $TIMESTAMP] | [domain:: $DOMAIN] | [context:: $CONTEXT] | **Outcomes:** Session ended ($STOP_REASON). Working dir: $WORK_DIR"

# Use sed to insert after the anchor comment
if grep -q "<!-- claude-sessions -->" "$DAILY_NOTE"; then
    # Insert the session entry on the line after the anchor
    sed -i '' "/<!-- claude-sessions -->/a\\
$SESSION_ENTRY" "$DAILY_NOTE"
else
    # Fallback: append to end of file if anchor not found
    {
        echo ""
        echo "## Claude Code Sessions"
        echo "<!-- claude-sessions -->"
        echo "$SESSION_ENTRY"
    } >> "$DAILY_NOTE"
fi

exit 0
