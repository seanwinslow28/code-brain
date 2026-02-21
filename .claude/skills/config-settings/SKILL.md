---
name: config-settings
description: Claude Code configuration and settings management guide. Covers the settings hierarchy (Enterprise managed > project local > project > user), permission evaluation order (Deny > Ask > Allow), CLAUDE.md best practices, settings.json schema, settings.local.json personal overrides, memory management, and context optimization strategies. Use when configuring Claude Code, updating settings, writing CLAUDE.md, managing permissions, or optimizing context window usage.
---

# Configuration and Settings Management

## Purpose

Configure Claude Code's behavior, permissions, and memory across the settings hierarchy. Understand which settings file to edit, how permissions evaluate, and how to manage the context window effectively through CLAUDE.md, skills, and context strategies.

## When to Use

- Setting up a new project's .claude/settings.json and CLAUDE.md
- Configuring permission rules (allow, deny, ask) for tools
- Creating settings.local.json for personal overrides
- Writing or improving a CLAUDE.md file
- Managing context window size and preventing context rot
- Understanding why a permission rule is not behaving as expected

## Examples

**Example 1: Setting up project permissions**
```
User: "Configure Claude Code to auto-approve reads but ask before running npm install"
Claude: [Uses config-settings] Creates .claude/settings.json:
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(git status)", "Bash(git log *)"],
    "ask": ["Bash(npm install *)", "Bash(git push *)"],
    "deny": ["Read(./.env*)", "Bash(rm -rf *)"]
  }
}
Explains: Deny is checked first (blocks .env reads), then Ask (prompts for npm install), then Allow (auto-approves reads).
```

**Example 2: Writing a CLAUDE.md**
```
User: "Create a CLAUDE.md for this Next.js project"
Claude: [Uses config-settings] Generates a concise CLAUDE.md (~50 lines):
- Stack overview (Next.js 14, TypeScript, Tailwind, Supabase)
- Core commands (dev, test, lint, build)
- Coding standards (absolute imports, async/await, test files required)
- Architecture notes (hooks in src/hooks, UI in src/components)
- References to detailed docs via @path syntax
Avoids: generic advice, API docs (use skills instead), volatile info.
```

**Example 3: Debugging permission behavior**
```
User: "Why is Claude still asking me before editing package.json even though I allowed Edit?"
Claude: [Uses config-settings] Checks permission evaluation order:
1. Deny list: Is "Edit(package.json)" in deny? No.
2. Ask list: Is "Edit(package.json)" in ask? Yes -- found "Edit(package.json)" in ask rules.
3. Allow list: "Edit" is in allow but ask matched first.
Fix: Remove "Edit(package.json)" from ask, or the specific ask rule takes precedence over the general allow.
```

## Settings Hierarchy

Settings merge from bottom to top. Higher-priority scopes override lower ones.

| Priority | Scope | File Location | Purpose |
|----------|-------|--------------|---------|
| 1 (Highest) | Managed | System path (Enterprise IT) | Immutable security policies. Cannot be overridden. |
| 2 | CLI Flags | Command line (e.g., `--model opus`) | Session-only overrides |
| 3 | Local Project | `.claude/settings.local.json` | Personal overrides. Git-ignored. |
| 4 | Shared Project | `.claude/settings.json` | Team standards. Committed to git. |
| 5 (Lowest) | Global User | `~/.claude/settings.json` | Personal defaults across all projects |

## Permission Evaluation Order

When Claude attempts to use a tool, rules are evaluated in this order. **First match wins.**

1. **Deny** -- checked first. If matched, action is blocked immediately.
2. **Ask** -- checked second. If matched, user is prompted to approve/deny.
3. **Allow** -- checked last. If matched, action proceeds automatically.

**Implication**: A deny rule always wins. An ask rule for a specific tool overrides a general allow for that tool category.

## settings.json Schema

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "defaultMode": "ask",
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run lint)",
      "Bash(git status)",
      "Bash(git log *)"
    ],
    "deny": [
      "Read(./.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf *)",
      "Bash(curl *)"
    ],
    "ask": [
      "Bash(npm install *)",
      "Bash(git push *)",
      "Edit(package.json)"
    ],
    "additionalDirectories": [
      "../shared-library"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "hooks": {},
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `model` | Default model for sessions |
| `permissions.defaultMode` | `default`, `acceptEdits`, `plan`, or `bypassPermissions` |
| `permissions.allow` | Tools auto-approved. Supports wildcards: `Bash(git *)` |
| `permissions.deny` | Tools always blocked. Checked before allow. |
| `permissions.ask` | Tools requiring user confirmation |
| `permissions.additionalDirectories` | Access paths outside project root (monorepos) |
| `env` | Environment variables set for the session |
| `hooks` | Lifecycle hook configurations |
| `sandbox.enabled` | OS-level isolation for bash commands |

### Permission Pattern Syntax

```
ToolName                    # Match all uses of tool
ToolName(exact_argument)    # Match specific argument
ToolName(pattern*)          # Wildcard matching
Read(./.env*)               # Block all .env files
Bash(git *)                 # Allow all git commands
Bash(npm install *)         # Ask for any npm install
```

## settings.local.json

Personal overrides that must not be shared with the team. Add to .gitignore.

**Use cases:**
- Personal API keys for MCP tools
- Model override (e.g., using haiku to save costs while team uses sonnet)
- Temporary debugging flags
- Machine-specific paths

```json
{
  "model": "claude-haiku-4-5-20251001",
  "env": {
    "JIRA_API_TOKEN": "your-personal-token"
  }
}
```

## CLAUDE.md Best Practices

CLAUDE.md is the project's long-term memory, loaded at the start of every session.

### Size Target
Keep under **300 lines**. If larger, Claude may ignore instructions due to context saturation. Use skills and @imports to modularize.

**Token budget per section:** Architecture (~25 lines), Decisions (~25), Patterns (~25), Gotchas (~20), Commands (~15). If a section overflows, move details to an external file and reference via `@import`.

### What to Include
- Stack and architecture overview (brief)
- Core commands: dev, test, lint, build
- Coding standards: high-level conventions
- Common pitfalls specific to this repo
- References to detailed docs: `See @docs/testing.md for test protocols`

### What to Avoid
- Generic advice ("Write clean code")
- Detailed API documentation (use skills instead)
- Volatile information that changes frequently
- Duplicate information already in settings.json

### Template

```markdown
# Project Context
- Stack: [frameworks, languages, databases]
- State Management: [approach]

## Core Commands
- Dev: `npm run dev`
- Test: `npm run test:unit`
- Lint: `npm run lint`
- Build: `npm run build`

## Coding Standards
- [Convention 1]
- [Convention 2]
- [Convention 3]

## Architecture
- [Where logic lives]
- [Where UI lives]
- See @docs/architecture-decisions.md for ADRs
```

### The @import System

Keep CLAUDE.md lean by referencing external files. Claude reads them only when relevant:

```markdown
See @docs/database-schema.md for table definitions.
See @docs/deployment-procedures.md for release checklists.
```

### Monorepo Pattern

In `root/packages/frontend`, Claude loads BOTH `root/CLAUDE.md` AND `root/packages/frontend/CLAUDE.md`. Keep the root lean and push framework-specific rules into subfolders.

### Global Security CLAUDE.md

Place in `~/.claude/CLAUDE.md` to apply across all projects:

```markdown
# Global Identity and Security Rules

## Identity
- Git User: "Your Name"
- Email: "you@example.com"

## SECURITY GATES (ABSOLUTE)
1. Secrets: NEVER output real API keys, passwords, or tokens in chat.
2. Environment: NEVER commit `.env` files to git. Always check `.gitignore`.
3. Deprecations: Treat deprecation warnings as build failures.
```

### CLAUDE.md vs Skills

| Aspect | CLAUDE.md | Skills |
| :--- | :--- | :--- |
| Loading | Always on (every session) | On demand (triggered by description match) |
| Use for | Rules for every interaction | Complex tasks needed occasionally |
| Token cost | Constant (every prompt) | Zero when not triggered |

If context is only needed occasionally (e.g., "Deploy to AWS"), put it in a Skill. If it applies to every interaction (formatting, commands, file structure), put it in CLAUDE.md.

### Update Cadence

1. **Start fast:** Run `/init` to generate a baseline, then delete the fluff
2. **Update on friction:** Every time you correct Claude, add the rule to CLAUDE.md immediately
3. **Review periodically:** Ask Claude: "Review this CLAUDE.md and suggest removals for redundant or obsolete instructions"

## Context Management Strategies

The 200k token context window is finite. Use these strategies to manage it:

| Strategy | How | When |
|----------|-----|------|
| `/clear` | Wipes conversation history | Between distinct tasks |
| `/compact` | Summarizes conversation | Mid-session when context is bloated |
| `/compact focus on [topic]` | Guided summary | Keep specific context, discard noise |
| Subagents | Delegate exploration to isolated agent | Reading 5+ files to find an answer |
| Skills (progressive disclosure) | Description loads ~100 tokens; body loads only when triggered | Always -- better than monolithic CLAUDE.md |
| `@filename` | Load specific file into context | When you know exactly which file is needed |
| HANDOFF.md pattern | Summarize progress, /clear, resume from file | Long sessions approaching context limit |

## Success Criteria

- [ ] settings.json has correct permission rules with deny > ask > allow priority
- [ ] CLAUDE.md is under 500 lines and contains only non-obvious project info
- [ ] settings.local.json is git-ignored and contains only personal overrides
- [ ] Permission behavior matches expectations (tested with actual tool calls)
- [ ] Context management strategy prevents degraded performance in long sessions

## Copy/Paste Ready

```
"Configure Claude Code permissions for this project"
"Create a CLAUDE.md for this repo"
"Why is my permission rule not working?"
"Set up settings.local.json for personal overrides"
"Optimize my context window usage"
```
