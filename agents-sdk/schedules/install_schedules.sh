#!/bin/bash
# Install launchd schedules for autonomous agents.
# Symlinks .plist files to ~/Library/LaunchAgents/ and loads them.
#
# Usage:
#   ./schedules/install_schedules.sh              # Install all (except gemini + substack-drafter — default disabled)
#   INSTALL_GEMINI=1 ./schedules/install_schedules.sh  # Install all including gemini-researcher
#   INSTALL_SUBSTACK_DRAFTER=1 ./schedules/install_schedules.sh  # Install all including substack-drafter
#   ./schedules/install_schedules.sh --list       # Show what would be installed (opt-in agents marked as default disabled)
#   ./schedules/install_schedules.sh --remove     # Unload and remove ALL symlinks (including gemini if opted in)
#
# Gemini opt-in:
#   com.sean.agent.gemini-researcher.plist is EXCLUDED by default because:
#     1. [agents.gemini_researcher].enabled = false in config.toml (belt-and-suspenders)
#     2. Gemini DR / DR Max incur real API cost (~$2–7/run)
#   To enable: edit config.toml to set enabled = true, then:
#     INSTALL_GEMINI=1 ./schedules/install_schedules.sh
#
# Substack-Drafter opt-in:
#   com.sean.agent.substack-drafter.plist is EXCLUDED by default because:
#     1. [substack_drafter].enabled = false in config.toml (belt-and-suspenders)
#     2. Sean reviews drafts before committing to weekly cadence (C9 pilot loop)
#   To enable: edit config.toml to set enabled = true, then:
#     INSTALL_SUBSTACK_DRAFTER=1 ./schedules/install_schedules.sh
#
# Not an agent:
#   com.sean.oracle-reminder.plist is a plain weekly reminder for the Content
#   Oracle's probation (GitHub #169). It sends one fixed email on /usr/bin/python3
#   and reads nothing but Keychain — no model, no SDK, no repo reads. Its label
#   omits `.agent.` on purpose: an Oracle that reached the inbox on a schedule
#   would have smuggled itself past its own probation. Installed by default;
#   remove it after probation with `launchctl unload` if the Oracle graduates
#   to a real schedule.

set -euo pipefail

SCHEDULES_DIR="$(cd "$(dirname "$0")" && pwd)"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
GEMINI_PLIST="com.sean.agent.gemini-researcher.plist"
SUBSTACK_DRAFTER_PLIST="com.sean.agent.substack-drafter.plist"
# eng-002.d49 / ADR-04 — the critic's nightly schedule is disabled at Phase 0
# (eng-002.d15); manual mode is untouched. Opt-in, so a re-run of this
# installer cannot silently restore it.
VAULT_CRITIC_PLIST="com.sean.agent.vault-critic.plist"

# LaunchDaemon-class plists (system-level, require sudo install at /Library/LaunchDaemons/)
# These must NOT be loaded as user-level LaunchAgents — they reference paths like
# /var/log/ that only root can write to, causing exit-78 failures in launchctl list.
# Install manually with sudo per the install block at the top of each plist.
LAUNCH_DAEMON_PLISTS=(
    "com.sean.agent-fleet-wake-scheduler.plist"
)

is_launch_daemon() {
    local name="$1"
    local d
    for d in "${LAUNCH_DAEMON_PLISTS[@]}"; do
        [[ "$name" == "$d" ]] && return 0
    done
    return 1
}

# Ensure LaunchAgents directory exists
mkdir -p "$LAUNCH_AGENTS"

if [[ "${1:-}" == "--list" ]]; then
    echo "Available schedules:"
    for plist in "$SCHEDULES_DIR"/*.plist; do
        name=$(basename "$plist")
        if [[ "$name" == "$GEMINI_PLIST" ]]; then
            echo "  $name  (default disabled — INSTALL_GEMINI=1 to enable)"
        elif [[ "$name" == "$SUBSTACK_DRAFTER_PLIST" ]]; then
            echo "  $name  (default disabled — INSTALL_SUBSTACK_DRAFTER=1 to enable)"
        elif [[ "$name" == "$VAULT_CRITIC_PLIST" ]]; then
            echo "  $name  (default disabled — INSTALL_VAULT_CRITIC=1 to enable)"
        elif is_launch_daemon "$name"; then
            echo "  $name  (LaunchDaemon — install manually with sudo, see plist header)"
        else
            echo "  $name"
        fi
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

# eng-002.d49 / ADR-04 — convergent removal. The old behaviour merely *skipped* a
# default-disabled plist, so a symlink and launchd label installed before the
# opt-in existed survived every subsequent run. That left the disable living in
# a human's memory of which commands not to run. Skipping now enforces absence:
# the formerly dangerous command is the one that converges the state.
skip_disabled() {
    local name="$1" hint="$2"
    local target="$LAUNCH_AGENTS/$name"
    if [[ -L "$target" || -e "$target" ]]; then
        launchctl unload "$target" 2>/dev/null || true
        rm -f "$target"
        echo "  Removed $name (default disabled — set $hint=1 to enable)"
    else
        echo "  Skipping $name (default disabled — set $hint=1 to enable)"
    fi
}

echo "Installing agent schedules..."
for plist in "$SCHEDULES_DIR"/*.plist; do
    name=$(basename "$plist")

    # Skip LaunchDaemon-class plists — they must be installed manually with sudo
    # at /Library/LaunchDaemons/ (see install block at the top of each plist).
    if is_launch_daemon "$name"; then
        echo "  Skipping $name (LaunchDaemon — install manually with sudo, see plist header)"
        continue
    fi

    # Skip gemini-researcher unless INSTALL_GEMINI=1 is set
    if [[ "$name" == "$GEMINI_PLIST" ]]; then
        if [[ "${INSTALL_GEMINI:-0}" != "1" ]]; then
            skip_disabled "$name" "INSTALL_GEMINI"
            continue
        fi
    fi

    # Skip substack-drafter unless INSTALL_SUBSTACK_DRAFTER=1 is set
    # Sean reviews drafts before committing to weekly cadence (C9 pilot loop).
    if [[ "$name" == "$SUBSTACK_DRAFTER_PLIST" ]]; then
        if [[ "${INSTALL_SUBSTACK_DRAFTER:-0}" != "1" ]]; then
            skip_disabled "$name" "INSTALL_SUBSTACK_DRAFTER"
            continue
        fi
    fi

    # Skip vault-critic unless INSTALL_VAULT_CRITIC=1 is set (eng-002.d15/d49).
    # Manual mode (--target/--from-list/--force) is unaffected.
    if [[ "$name" == "$VAULT_CRITIC_PLIST" ]]; then
        if [[ "${INSTALL_VAULT_CRITIC:-0}" != "1" ]]; then
            skip_disabled "$name" "INSTALL_VAULT_CRITIC"
            continue
        fi
    fi

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

echo "Done. Verify with: launchctl list | grep com.sean."
