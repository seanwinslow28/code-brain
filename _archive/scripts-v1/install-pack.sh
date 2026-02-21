#!/bin/bash
# Install a Claude Code Superuser Pack into a target project

set -e

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory does not exist: $TARGET_DIR"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <target-directory> <pack-name>"
    echo "Available packs: starter, power, enterprise"
    exit 1
fi

PACK_NAME="$2"
PACK_PATH="$PACK_DIR/packs/$PACK_NAME"

if [ ! -d "$PACK_PATH" ]; then
    echo "Error: Pack '$PACK_NAME' not found at $PACK_PATH"
    echo "Available packs: starter, power, enterprise"
    exit 1
fi

echo "Installing '$PACK_NAME' pack to $TARGET_DIR..."

# Copy CLAUDE.md
if [ -f "$PACK_PATH/CLAUDE.md" ]; then
    cp "$PACK_PATH/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "✓ Copied CLAUDE.md"
fi

# Copy .gitignore (merge with existing if present)
if [ -f "$PACK_PATH/.gitignore" ]; then
    if [ -f "$TARGET_DIR/.gitignore" ]; then
        echo "" >> "$TARGET_DIR/.gitignore"
        echo "# Claude Code Superuser Pack" >> "$TARGET_DIR/.gitignore"
        cat "$PACK_PATH/.gitignore" >> "$TARGET_DIR/.gitignore"
        echo "✓ Merged .gitignore"
    else
        cp "$PACK_PATH/.gitignore" "$TARGET_DIR/.gitignore"
        echo "✓ Copied .gitignore"
    fi
fi

# Copy .claude directory
if [ -d "$PACK_PATH/.claude" ]; then
    mkdir -p "$TARGET_DIR/.claude"
    
    # Copy settings.json
    if [ -f "$PACK_PATH/.claude/settings.json" ]; then
        cp "$PACK_PATH/.claude/settings.json" "$TARGET_DIR/.claude/settings.json"
        echo "✓ Copied .claude/settings.json"
    fi
    
    # Copy settings.local.json.example
    if [ -f "$PACK_PATH/.claude/settings.local.json.example" ]; then
        cp "$PACK_PATH/.claude/settings.local.json.example" "$TARGET_DIR/.claude/settings.local.json.example"
        echo "✓ Copied .claude/settings.local.json.example"
    fi
    
    # Copy skills directory
    if [ -d "$PACK_PATH/.claude/skills" ]; then
        cp -r "$PACK_PATH/.claude/skills" "$TARGET_DIR/.claude/"
        echo "✓ Copied .claude/skills/"
    fi
    
    # Copy agents directory
    if [ -d "$PACK_PATH/.claude/agents" ]; then
        cp -r "$PACK_PATH/.claude/agents" "$TARGET_DIR/.claude/"
        echo "✓ Copied .claude/agents/"
    fi
    
    # Copy hooks directory
    if [ -d "$PACK_PATH/.claude/hooks" ]; then
        mkdir -p "$TARGET_DIR/.claude/hooks"
        cp -r "$PACK_PATH/.claude/hooks/"* "$TARGET_DIR/.claude/hooks/"
        chmod +x "$TARGET_DIR/.claude/hooks/"*.sh 2>/dev/null || true
        echo "✓ Copied .claude/hooks/ (made scripts executable)"
    fi
    
    # Copy templates directory
    if [ -d "$PACK_PATH/.claude/templates" ]; then
        cp -r "$PACK_PATH/.claude/templates" "$TARGET_DIR/.claude/"
        echo "✓ Copied .claude/templates/"
    fi
fi

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Review $TARGET_DIR/CLAUDE.md"
echo "2. Review $TARGET_DIR/.claude/settings.json"
echo "3. Copy $TARGET_DIR/.claude/settings.local.json.example to $TARGET_DIR/.claude/settings.local.json for local-only tweaks"
echo "4. Start using Claude Code with your new pack!"
