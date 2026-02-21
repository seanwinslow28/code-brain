# Claude Code Configuration - Enterprise Pack

## Quick Start

This pack provides maximum safety with logging, compliance, and strict guardrails. Designed for organizations requiring enhanced security and audit trails.

## Plan Mode vs Extended Thinking

**Important:** These are different features with different triggers:

- **Plan Mode**: Requires explicit trigger - **double `Shift+Tab`** or `/plan` command
- **Extended Thinking**: Toggled by **single `Tab`** key

Never document `Tab` as entering Plan Mode. Plan Mode requires the explicit trigger above.

## Skills Available

This pack includes:
- `org-security` - Organizational security policy enforcement
- `org-definition-of-done` - Definition of Done validation
- `pm-prd` - Product Requirements Document creation

## Agents Available

- `security-reviewer` - Security audit specialist (read-only)
- `compliance-summarizer` - Compliance review specialist (read-only)

## Hooks

- `block-secrets.py` - PreToolUse hook that blocks edits to sensitive files
- `require-confirm-highrisk.sh` - PreToolUse hook that blocks risky Bash commands
- `log-tool-use.sh` - PostToolUse hook that logs tool usage
- `run-tests-on-stop.sh` - PostStop hook that runs tests (configurable blocking/non-blocking)

## Configuration

- Settings: `.claude/settings.json`
- Local overrides: Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` (never commit)

## Safety Features

- Default permission: `ask` (prompts for risky operations)
- Automatic blocking of sensitive file edits
- Blocking of risky Bash commands (unless explicitly allowed)
- Comprehensive tool usage logging for audit trail
- Configurable test blocking (set `CLAUDE_TEST_BLOCKING=true` to enable blocking mode)

## Enterprise Considerations

- All operations are logged for audit compliance
- Risky operations require explicit approval
- Test runs can be configured to block deployment if tests fail
- Security and compliance agents provide read-only reviews

## Next Steps

1. Review `.claude/settings.json` and customize as needed
2. Copy `.claude/settings.local.json.example` to `.claude/settings.local.json` for local-only tweaks
3. Configure `CLAUDE_TEST_BLOCKING` environment variable based on your organization's preference
4. Ensure all team members understand the security and compliance requirements
