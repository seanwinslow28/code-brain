# Core Features - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Core Features"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals, working across three domains: PM work, creative projects (React Native + Phaser game dev), and life optimization/automation. My stack is React, Python, Supabase, and I use Claude Code as my primary development tool.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers the **foundational features** of Claude Code itself.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Core Features") contains deep research on Claude Code's core architecture and capabilities: the CLI, skills system, hooks lifecycle, subagents, MCP (Model Context Protocol), plugins, headless mode, permissions, and configuration management. Sources include official Anthropic documentation, community tutorials, power user discussions, and technical deep dives.

## Your Task

Analyze all sources in this notebook and generate **6-7 Claude Skills** that teach Claude Code how to help me understand and leverage its own feature set. These skills are "meta" — they make Claude Code better at using itself and helping me use it effectively.

## Target Skills to Extract

### 1. Skill System Mastery
**Priority**: High
**What to extract**: How to create effective SKILL.md files, YAML frontmatter best practices, auto-loading trigger optimization, progressive disclosure patterns, when to use references/ vs inline content. The skill should help Claude Code create and improve other skills.
**Trigger phrases**: "create a skill", "improve this skill", "write a SKILL.md", "skill template"

### 2. Hooks Configuration & Patterns
**Priority**: High
**What to extract**: Complete hook lifecycle (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd), exit codes (0=allow, 1=error, 2=deny), blocking vs non-blocking, Python and Bash patterns, common hooks (secret blocking, auto-formatting, test running, logging). The skill should help Claude Code create and debug hooks.
**Trigger phrases**: "create a hook", "add a hook", "block dangerous commands", "auto-format on save", "run tests on stop"

### 3. Subagent Orchestration
**Priority**: High
**What to extract**: When to use subagents vs skills vs hooks (decision framework), tool restrictions with disallowedTools (deny-list only — never allow-list), background vs foreground agents, multi-agent patterns (swarm, council, pipeline), ephemeral agents, context isolation benefits. The skill should help Claude Code design effective agent architectures.
**Trigger phrases**: "create an agent", "run this in parallel", "delegate this task", "agent architecture"

### 4. MCP Server Integration Guide
**Priority**: High
**What to extract**: What MCP is and how it works, stdio vs HTTP transport, user vs project vs managed scope, OAuth flows, common MCP servers (Jira, Slack, Figma, databases, Obsidian), troubleshooting connection failures, security implications. The skill should help Claude Code set up and debug MCP connections.
**Trigger phrases**: "connect to", "set up MCP", "add MCP server", "MCP not working", "integrate with"

### 5. Configuration & Settings Management
**Priority**: Medium
**What to extract**: Settings hierarchy (Enterprise managed > Project local > Project settings > User settings), permission evaluation order (Deny > Ask > Allow), CLAUDE.md best practices (what to include, what to avoid, ideal token size), settings.json schema, settings.local.json for personal overrides, context management strategies.
**Trigger phrases**: "configure Claude Code", "update settings", "CLAUDE.md", "permissions", "settings.json"

### 6. Commands, Shortcuts & CLI Mastery
**Priority**: Medium
**What to extract**: All keyboard shortcuts, / commands, @ mentions, CLI flags, hidden commands, efficiency patterns, Plan Mode (double Shift+Tab) vs Extended Thinking (single Tab) — CRITICAL: never document Tab as entering Plan Mode. Include command combinations and workflow shortcuts power users rely on daily.
**Trigger phrases**: "keyboard shortcuts", "CLI flags", "how do I", "shortcut for"

### 7. Headless Mode & Automation
**Priority**: Medium
**What to extract**: The -p flag for non-interactive mode, --output-format stream-json, GitHub Actions integration (anthropics/claude-code-action), batch processing patterns, scripting Claude Code in CI/CD pipelines, CLAUDE_CODE_TASK_LIST_ID for multi-instance coordination.
**Trigger phrases**: "headless mode", "CI/CD", "automate", "GitHub Actions", "batch process", "run non-interactive"

## Extraction Guidance

- These skills are **foundational** — they'll be used alongside every other domain playground. Prioritize accuracy and completeness over brevity.
- Include concrete code examples: real settings.json snippets, real hook scripts, real SKILL.md templates.
- For hooks, always include the exit code reference (0/1/2) — this trips up even experienced users.
- For subagents, emphasize **disallowedTools** (deny-list) — never document allow-lists, as Claude Code uses deny-lists only.
- For Plan Mode: double Shift+Tab or /plan. Extended Thinking: single Tab. This is a non-negotiable rule — getting it wrong creates confusion.
- Cross-reference with the permissions system where relevant (e.g., hooks that enforce permissions, MCP security scope).

## Cross-Domain Notes

These skills are referenced by every other domain:
- PM Workflows uses MCP (Jira, Slack, Figma) and hooks (auto-formatting)
- Creative Projects uses subagents (parallel rendering) and headless mode
- Life Optimization uses headless mode and MCP (calendar, task managers)
- Advanced Techniques builds directly on these foundations
- All domains use CLAUDE.md and configuration management

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include concrete examples, not just conceptual explanations
- Be immediately usable (copy skill folder into .claude/skills/ and it works)
- Focus on what Claude doesn't already know — skip basic CLI concepts it inherently understands
- Reference files in references/ for detailed schemas, examples, or lookup tables over 50 lines

---

## PROMPT END
