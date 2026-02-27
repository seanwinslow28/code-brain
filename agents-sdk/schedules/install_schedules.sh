#!/bin/bash
# Install launchd schedules for autonomous agents.
# Symlinks .plist files to ~/Library/LaunchAgents/ and loads them.
#
# Usage:
#   ./schedules/install_schedules.sh         # Install all
#   ./schedules/install_schedules.sh --list  # Show what would be installed
#   ./schedules/install_schedules.sh --remove # Unload and remove symlinks

set -euo pipefail

SCHEDULES_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

# Ensure LaunchAgents directory exists
mkdir -p "$LAUNCH_AGENTS"

if [[ "${1:-}" == "--list" ]]; then
    echo "Available schedules:"
    for plist in "$SCHEDULES_DIR"/*.plist; do
        name=$(basename "$plist")
        echo "  $name"
    done
    exit 0
fi

if [[ "${1:-}" == "--remove" ]]; then
    echo "Removing agent schedules..."
    for plist in "$SCHEDULES_DIR"/*.plist; do
        name=$(basename "$plist")
        target="$LAUNCH_AGENTS/$name"
        if [[ -L "$target" ]]; then
            launchctl unload "$target" 2>/dev/null || true
            rm "$target"
            echo "  Removed: $name"
        fi
    done
    echo "Done."
    exit 0
fi

echo "Installing agent schedules..."
for plist in "$SCHEDULES_DIR"/*.plist; do
    name=$(basename "$plist")
    target="$LAUNCH_AGENTS/$name"

    # Unload if already loaded
    if [[ -L "$target" ]]; then
        launchctl unload "$target" 2>/dev/null || true
    fi

    # Create symlink
    ln -sf "$plist" "$target"

    # Load the schedule
    launchctl load "$target"
    echo "  Installed: $name"
done

echo "Done. Verify with: launchctl list | grep com.sean.agent"
