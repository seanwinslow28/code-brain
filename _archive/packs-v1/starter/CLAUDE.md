# Claude Code Configuration - Starter Pack

## Quick Start

This pack provides safe defaults with basic productivity skills. It's perfect for getting started with Claude Code.

## Plan Mode vs Extended Thinking

**Important:** These are different features with different triggers:

- **Plan Mode**: Requires explicit trigger - **double `Shift+Tab`** or `/plan` command
- **Extended Thinking**: Toggled by **single `Tab`** key

Never document `Tab` as entering Plan Mode. Plan Mode requires the explicit trigger above.

## Skills Available

This pack includes:
- `team-styleguide` - Enforces team coding standards
- `commit-checklist` - Validates commits against best practices
- `safe-ops` - Ensures safe operations with confirmation prompts

## Hooks

- `block-secrets.py` - PreToolUse hook that blocks edits to sensitive files (`.env`, `**/secrets/**`, etc.)
- `log-tool-use.sh` - PostToolUse hook that logs tool usage for audit trail

## Configuration

- Settings: `.claude/settings.json`
- Local overrides: Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` (never commit)

## Safety Features

- Default permission: `ask` (prompts for risky operations)
- Automatic blocking of sensitive file edits
- Tool usage logging for audit trail

## Next Steps

1. Review `.claude/settings.json` and customize as needed
2. Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` for local-only tweaks
3. Start using the skills in your prompts
