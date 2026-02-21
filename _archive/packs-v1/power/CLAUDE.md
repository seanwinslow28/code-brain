# Claude Code Configuration - Power Pack

## Quick Start

This pack provides enhanced productivity with PM, creative, and life automation skills. Perfect for power users who want comprehensive tooling.

## Plan Mode vs Extended Thinking

**Important:** These are different features with different triggers:

- **Plan Mode**: Requires explicit trigger - **double `Shift+Tab`** or `/plan` command
- **Extended Thinking**: Toggled by **single `Tab`** key

Never document `Tab` as entering Plan Mode. Plan Mode requires the explicit trigger above.

## Skills Available

This pack includes all starter skills plus:
- `pm-prd` - Product Requirements Document creation
- `pm-jira` - Jira ticket management
- `pm-stakeholder-update` - Stakeholder communication
- `react-native-phaser` - React Native + Phaser game development
- `supabase-python` - Supabase integration in Python
- `life-budget` - Personal finance tracking and automation

## Agents Available

- `pm-tech-writer` - Technical documentation specialist (read-only)
- `security-reviewer` - Security audit specialist (read-only)
- `game-design-advisor` - Game design guidance
- `data-analyst` - Data analysis and insights

## Hooks

- `block-secrets.py` - PreToolUse hook that blocks edits to sensitive files
- `log-tool-use.sh` - PostToolUse hook that logs tool usage
- `format-on-edit.sh` - PostToolUse hook that auto-formats files (prettier/black)
- `run-tests-on-stop.sh` - PostStop hook that runs tests (non-blocking)

## Templates

Pre-built templates in `.claude/templates/`:
- `prd.md` - Product Requirements Document
- `jira_ticket.md` - Jira ticket template
- `stakeholder_update.md` - Stakeholder status update
- `game_feature_spec.md` - Game feature specification
- `finance_report.md` - Financial report template

## Configuration

- Settings: `.claude/settings.json`
- Local overrides: Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` (never commit)

## Safety Features

- Default permission: `ask` (prompts for risky operations)
- Automatic blocking of sensitive file edits
- Tool usage logging for audit trail
- Auto-formatting on edit (non-blocking)

## Next Steps

1. Review `.claude/settings.json` and customize as needed
2. Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` for local-only tweaks
3. Explore the templates in `.claude/templates/`
4. Start using the skills and agents in your prompts
