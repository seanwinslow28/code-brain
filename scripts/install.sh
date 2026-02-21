#!/bin/bash
# Claude Code Superuser Pack — Composable Installer v3.0.0
# Reads export-group manifests for skill/agent names, copies from canonical .claude/ sources
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR=""
PRESET=""
SECURITY="standard"
EXTRA_SELECTED=()

# ─── Usage ───────────────────────────────────────────────────────────
usage() {
    cat <<'USAGE'
Claude Code Superuser Pack Installer v3.0.0

Usage:
  install.sh <target-dir> --preset <name>
  install.sh <target-dir> <group> [<group>...] [--security <profile>]
  install.sh <target-dir> --preset <name> <extra-group> [...]

Examples:
  install.sh ./my-project --preset starter
  install.sh ./my-project --preset power
  install.sh ./my-project pm-workflows remotion-mastery
  install.sh ./my-project pm-workflows --security enterprise
  install.sh ./my-project --preset starter remotion-mastery
  install.sh --list

Options:
  --preset <name>       Use a preset: starter, power, enterprise, creative
  --security <profile>  Security profile: standard (default), enterprise
  --list                List available export groups and presets
  -h, --help            Show this help
USAGE
}

list_available() {
    echo "Available export groups:"
    for pg_dir in "$REPO_DIR"/export-groups/*/; do
        pg_name=$(basename "$pg_dir")
        desc=$(python3 -c "
import json
with open('$pg_dir/playground.json') as f:
    print(json.load(f).get('description',''))
" 2>/dev/null || echo "(no description)")
        printf "  %-28s %s\n" "$pg_name" "$desc"
    done
    echo ""
    echo "Available presets:"
    for preset_file in "$REPO_DIR"/presets/*.json; do
        p_name=$(basename "$preset_file" .json)
        p_desc=$(python3 -c "
import json
with open('$preset_file') as f:
    print(json.load(f).get('description',''))
" 2>/dev/null || echo "(no description)")
        printf "  %-16s %s\n" "$p_name" "$p_desc"
    done
}

# ─── Parse Arguments ─────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --preset)
            PRESET="$2"
            shift 2
            ;;
        --security)
            SECURITY="$2"
            shift 2
            ;;
        --list)
            list_available
            exit 0
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                EXTRA_SELECTED+=("$1")
            fi
            shift
            ;;
    esac
done

if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: Target directory is required."
    echo ""
    usage
    exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory does not exist: $TARGET_DIR"
    exit 1
fi

if [[ -z "$PRESET" && ${#EXTRA_SELECTED[@]} -eq 0 ]]; then
    echo "Error: Specify --preset <name> and/or one or more export group names."
    echo ""
    usage
    exit 1
fi

# ─── Resolve Preset ─────────────────────────────────────────────────
SELECTED=()

if [[ -n "$PRESET" ]]; then
    PRESET_FILE="$REPO_DIR/presets/$PRESET.json"
    if [[ ! -f "$PRESET_FILE" ]]; then
        echo "Error: Preset '$PRESET' not found. Available: starter, power, enterprise, creative"
        exit 1
    fi

    eval "$(python3 -c "
import json
with open('$PRESET_FILE') as f:
    data = json.load(f)
pgs = data.get('export_groups', [])
print('SELECTED=(' + ' '.join('\"' + p + '\"' for p in pgs) + ')')
print('SECURITY=\"' + data.get('security', 'standard') + '\"')
")"
fi

# Merge extra groups (deduplicate)
for pg in "${EXTRA_SELECTED[@]}"; do
    already=false
    for existing in "${SELECTED[@]}"; do
        if [[ "$existing" == "$pg" ]]; then
            already=true
            break
        fi
    done
    if [[ "$already" == "false" ]]; then
        SELECTED+=("$pg")
    fi
done

# ─── Validate Export Groups Exist ──────────────────────────────────
for pg in "${SELECTED[@]}"; do
    if [[ ! -d "$REPO_DIR/export-groups/$pg" ]]; then
        echo "Error: Export group '$pg' not found in $REPO_DIR/export-groups/"
        exit 1
    fi
done

# ─── Validate Security Profile ──────────────────────────────────────
SECURITY_FILE="$REPO_DIR/shared/security/$SECURITY.json"
if [[ ! -f "$SECURITY_FILE" ]]; then
    echo "Error: Security profile '$SECURITY' not found. Available: standard, enterprise"
    exit 1
fi

# ─── Resolve Dependencies ───────────────────────────────────────────
echo "Resolving export groups..."
for pg in "${SELECTED[@]}"; do
    PG_JSON="$REPO_DIR/export-groups/$pg/playground.json"
    if [[ -f "$PG_JSON" ]]; then
        deps=$(python3 -c "
import json
with open('$PG_JSON') as f:
    deps = json.load(f).get('dependencies', [])
print(' '.join(deps))
" 2>/dev/null)
        for dep in $deps; do
            found=false
            for existing in "${SELECTED[@]}"; do
                if [[ "$existing" == *"$dep"* ]]; then
                    found=true
                    break
                fi
            done
            if [[ "$found" == "false" ]]; then
                echo "  Warning: '$pg' depends on '$dep' which is not in the install list."
            fi
        done
    fi
done

# ─── Collect Skill and Agent Names from Manifests ────────────────────
SKILL_NAMES=()
AGENT_NAMES=()

for pg in "${SELECTED[@]}"; do
    PG_JSON="$REPO_DIR/export-groups/$pg/playground.json"
    if [[ -f "$PG_JSON" ]]; then
        # Get skill names from manifest
        eval "$(python3 -c "
import json
with open('$PG_JSON') as f:
    data = json.load(f)
skills = data.get('skills', [])
print('PG_SKILLS=(' + ' '.join('\"' + s + '\"' for s in skills) + ')')
agents = data.get('agents', [])
print('PG_AGENTS=(' + ' '.join('\"' + a + '\"' for a in agents) + ')')
")"
        for s in "${PG_SKILLS[@]}"; do
            SKILL_NAMES+=("$s")
        done
        for a in "${PG_AGENTS[@]}"; do
            AGENT_NAMES+=("$a")
        done
    fi
done

# Deduplicate skill names
SKILL_NAMES=($(printf '%s\n' "${SKILL_NAMES[@]}" | sort -u))
AGENT_NAMES=($(printf '%s\n' "${AGENT_NAMES[@]}" | sort -u))

# ─── Begin Installation ─────────────────────────────────────────────
echo ""
echo "Installing to $TARGET_DIR"
echo "  Export groups: ${SELECTED[*]}"
echo "  Security:      $SECURITY"
echo "  Skills:        ${#SKILL_NAMES[@]}"
echo "  Agents:        ${#AGENT_NAMES[@]}"
echo ""

mkdir -p "$TARGET_DIR/.claude/skills"
mkdir -p "$TARGET_DIR/.claude/agents"
mkdir -p "$TARGET_DIR/.claude/hooks"

# ─── Copy Skills from Canonical Source ───────────────────────────────
SKILLS_COPIED=0
for skill in "${SKILL_NAMES[@]}"; do
    src="$REPO_DIR/.claude/skills/$skill"
    if [[ -d "$src" ]]; then
        cp -r "$src" "$TARGET_DIR/.claude/skills/"
        SKILLS_COPIED=$((SKILLS_COPIED + 1))
    else
        echo "  Warning: Skill '$skill' not found in .claude/skills/"
    fi
done
echo "  Skills: $SKILLS_COPIED copied"

# ─── Copy Agents from Canonical Source ───────────────────────────────
AGENTS_COPIED=0
for agent in "${AGENT_NAMES[@]}"; do
    src="$REPO_DIR/.claude/agents/$agent.md"
    if [[ -f "$src" ]]; then
        cp "$src" "$TARGET_DIR/.claude/agents/"
        AGENTS_COPIED=$((AGENTS_COPIED + 1))
    else
        echo "  Warning: Agent '$agent' not found in .claude/agents/"
    fi
done
echo "  Agents: $AGENTS_COPIED copied"

# ─── Copy Hooks from Security Profile ───────────────────────────────
HOOKS_COPIED=0
HOOK_FILES=$(python3 -c "
import json
with open('$SECURITY_FILE') as f:
    data = json.load(f)
hooks = data.get('hooks', {})
files = set()
for event_hooks in hooks.values():
    for h in event_hooks:
        cmd = h.get('command', '')
        if '/' in cmd:
            files.add(cmd.split('/')[-1])
for f in sorted(files):
    print(f)
")

for hook_file in $HOOK_FILES; do
    src="$REPO_DIR/shared/hooks/$hook_file"
    if [[ -f "$src" ]]; then
        cp "$src" "$TARGET_DIR/.claude/hooks/"
        chmod +x "$TARGET_DIR/.claude/hooks/$hook_file" 2>/dev/null || true
        HOOKS_COPIED=$((HOOKS_COPIED + 1))
    fi
done
echo "  Hooks:  $HOOKS_COPIED copied"

# ─── Compose settings.json ──────────────────────────────────────────
python3 -c "
import json

with open('$SECURITY_FILE') as f:
    security = json.load(f)

settings = {
    'permissions': security.get('permissions', {'default': 'ask', 'rules': []}),
    'hooks': security.get('hooks', {})
}

with open('$TARGET_DIR/.claude/settings.json', 'w') as f:
    json.dump(settings, f, indent=2)
    f.write('\n')
"
echo "  Generated .claude/settings.json"

# ─── Compose CLAUDE.md ──────────────────────────────────────────────
{
    cat <<'HEADER'
# CLAUDE.md

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.
2. **Agent tool restrictions**: Use `disallowedTools` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow

---

HEADER

    for pg in "${SELECTED[@]}"; do
        section="$REPO_DIR/export-groups/$pg/CLAUDE.section.md"
        if [[ -f "$section" ]]; then
            cat "$section"
            echo ""
            echo "---"
            echo ""
        fi
    done

    cat <<FOOTER
## Configuration

- **Security profile**: $SECURITY
- **Installed export groups**: ${SELECTED[*]}
- **Settings**: \`.claude/settings.json\` — permissions, hooks
- **Local overrides**: Copy \`.claude/settings.local.json.example\` to \`.claude/settings.local.json\`

Installed by Claude Code Superuser Pack v3.0.0
FOOTER
} > "$TARGET_DIR/CLAUDE.md"
echo "  Generated CLAUDE.md"

# ─── Create settings.local.json.example ──────────────────────────────
cat > "$TARGET_DIR/.claude/settings.local.json.example" <<'EXAMPLE'
{
  "// NOTE": "Rename this file to settings.local.json for local-only overrides.",
  "// INFO": "This file is gitignored and never committed.",
  "permissions": {
    "rules": []
  }
}
EXAMPLE
echo "  Created .claude/settings.local.json.example"

# ─── Merge .gitignore ───────────────────────────────────────────────
GITIGNORE_LINES=".claude/settings.local.json
.claude/tool-use.log"

if [[ -f "$TARGET_DIR/.gitignore" ]]; then
    if ! grep -q "settings.local.json" "$TARGET_DIR/.gitignore" 2>/dev/null; then
        echo "" >> "$TARGET_DIR/.gitignore"
        echo "# Claude Code Superuser Pack" >> "$TARGET_DIR/.gitignore"
        echo "$GITIGNORE_LINES" >> "$TARGET_DIR/.gitignore"
        echo "  Merged .gitignore entries"
    fi
else
    echo "# Claude Code Superuser Pack" > "$TARGET_DIR/.gitignore"
    echo "$GITIGNORE_LINES" >> "$TARGET_DIR/.gitignore"
    echo "  Created .gitignore"
fi

# ─── Report ──────────────────────────────────────────────────────────
echo ""
echo "Installation complete!"
echo ""
echo "Installed $SKILLS_COPIED skills, $AGENTS_COPIED agents, $HOOKS_COPIED hooks"
echo ""
echo "Next steps:"
echo "  1. Review $TARGET_DIR/CLAUDE.md"
echo "  2. Review $TARGET_DIR/.claude/settings.json"
echo "  3. Optionally create $TARGET_DIR/.claude/settings.local.json for local overrides"
echo "  4. Start using Claude Code!"
