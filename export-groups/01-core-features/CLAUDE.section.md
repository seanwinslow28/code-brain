## Core Features

Foundation skills for Claude Code configuration and best practices.

### Non-Negotiable Rules
- **Plan Mode**: Double `Shift+Tab` or `/plan`. **Extended Thinking**: Single `Tab`. Never swap these.
- **Agent tool restrictions**: Use `disallowedTools` (deny-list), never allow-list.
- **Hook blocking**: Exit code `2` to deny. Exit `0` to allow. Exit `1` to log error.
- **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
- **Permission evaluation** (first match wins): Deny > Ask > Allow

### Available Skills
- **team-styleguide**: Enforces coding standards ("review this code for style")
- **commit-checklist**: Validates commits before submission ("check this commit")
- **safe-ops**: Confirms destructive operations ("safely delete these files")
- **org-security**: Security policy enforcement ("review security of this code")
- **org-definition-of-done**: Definition of Done validation ("is this feature done?")
- **subagent-driven-development**: Fresh subagent per task with two-stage review ("execute this plan")
