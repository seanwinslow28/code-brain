<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# HANDOFF PACKET (Claude Code Mastery) — v1

## 0) TL;DR (8 bullets max)

- Claude Code is Anthropic's production agentic coding CLI (v2.1.17 current, Jan 2026) with 176+ releases in 2025 alone—evolving from beta to enterprise-grade tool https://claudefa.st/blog/guide/changelog
- **CLAUDE.md** is auto-loaded project memory (facts, architecture, standards); keep lean, use `#` key to add entries mid-session https://www.builder.io/blog/claude-md-guide
- **Skills** = auto-invoked expertise (30-50 tokens), **Slash Commands** = user-triggered templates (100-1000 tokens), **Subagents** = isolated Claude instances with restricted tools https://rewire.it/blog/claude-code-agents-skills-slash-commands/
- **Sandboxing** (Oct 2025) reduced permission prompts 84% via filesystem + network isolation; enables safe autonomous operation https://www.anthropic.com/engineering/claude-code-sandboxing
- **MCP (Model Context Protocol)** connects external APIs/databases/tools; OAuth support, can import from Claude Desktop https://code.claude.com/docs/en/mcp
- **Hooks** = deterministic shell commands at lifecycle events (PreToolUse, PostToolUse, Stop); prevents relying on LLM memory for formatting/linting https://code.claude.com/docs/en/hooks
- **Tasks system** (v2.1.x, Jan 2025) replaced Todos with dependency tracking, multi-session persistence via `CLAUDE_CODE_TASK_LIST_ID` https://claudefa.st/blog/guide/development/task-management
- **GitHub Actions** integration (`anthropics/claude-code-action@v1`) enables @claude mentions in PRs/issues to trigger autonomous implementations https://code.claude.com/docs/en/github-actions


## 1) What matters most (Top 12 findings)

- **Interactive vs. Print mode:** `claude` for REPL, `claude -p "query"` for headless CI/CD with `--output-format stream-json` https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm
- **Permission hierarchy:** deny → ask → allow (first match wins); use `allowedTools` in settings.json for granular control https://www.claudelog.com/faqs/how-to-set-claude-code-permission-mode/
- **Config precedence:** managed-settings.json > .claude/settings.local.json > .claude/settings.json > ~/.claude/settings.json https://code.claude.com/docs/en/settings
- **Shift+Tab cycles modes:** default → acceptEdits → plan; plan mode reviews before execution https://moonandeye.github.io/en/programming/think-mode-on-claude-code/
- **Ctrl+B backgrounds tasks:** run dev servers/builds while Claude continues; press twice in tmux https://code.claude.com/docs/en/interactive-mode
- **Extended Thinking (Tab key):** spends more reasoning tokens; use for complex refactors, overkill for routine tasks https://www.anthropic.com/news/visible-extended-thinking
- **Vim mode (`/vim`):** modal editing with h/j/k/l navigation, subset of full Vim https://dev.to/rajeshroyal/vim-mode-edit-prompts-at-the-speed-of-thought-3l6c
- **Rewind (Esc+Esc):** undo conversation + code state; may not catch all filesystem changes https://code.claude.com/docs/en/interactive-mode
- **@-mentions:** type `@` for file autocomplete; adds precision without context pollution https://shipyard.build/blog/claude-code-cheat-sheet/
- **Compact strategically:** `/compact [focus instruction]` summarizes conversation; early instructions may be lost—prefer CLAUDE.md for persistence https://www.cometapi.com/managing-claude-codes-context/
- **Chrome integration** (Pro/Max+ only, v2.0.73+): `claude --chrome` enables browser automation, console reading, UI testing; no WSL support https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/
- **Agent SDK** (v1.0.23+, June 2025): programmatic access for custom agents (email assistant, code reviewer) with structured output support https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk


## 2) Practical "Superuser Moves" (Top 15)

**1. CLAUDE.md Project Memory**

- When to use: Start of every project, updated continuously as architecture evolves
- Exact trigger / command: `/init` to generate; `#` key to add entries mid-session
- Gotcha: Token bloat if too verbose; use `@imports` and `.claude/rules/` for modular organization
- Source URL: https://www.builder.io/blog/claude-md-guide

**2. Plan Mode Before Execution**

- When to use: Complex tasks, unfamiliar codebases, high-stakes changes
- Exact trigger / command: `Shift+Tab` twice, or `/plan` command
- Gotcha: Approving plan may auto-enable acceptEdits mode; explicitly disable if unwanted
- Source URL: https://moonandeye.github.io/en/programming/think-mode-on-claude-code/

**3. Background Tasks**

- When to use: Dev servers, build tools, test runners, Docker, Terraform
- Exact trigger / command: `Ctrl+B` when command is running (press twice for tmux users)
- Gotcha: Need to retrieve output manually via TaskOutput tool
- Source URL: https://code.claude.com/docs/en/interactive-mode

**4. Custom Slash Commands with Arguments**

- When to use: Frequent atomic tasks—testing, commits, scaffolding, project-specific workflows
- Exact trigger / command: Create `.md` file in `~/.claude/commands/` or `.claude/commands/`, use `$ARGUMENTS`
- Gotcha: Restart Claude after creating/editing commands
- Source URL: https://shipyard.build/blog/claude-code-cheat-sheet/

**5. Headless Mode for CI/CD**

- When to use: Code reviews in pipelines, automation scripts, data processing workflows
- Exact trigger / command: `claude -p "query" --output-format stream-json`
- Gotcha: No interactive clarifications; must provide complete context upfront
- Source URL: https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm

**6. Subagent Delegation**

- When to use: Code review, security scans, testing—isolated tasks that pollute main context
- Exact trigger / command: `/agents` to configure; Claude auto-delegates based on description
- Gotcha: Cannot spawn other subagents; background subagents can't ask clarifying questions
- Source URL: https://code.claude.com/docs/en/sub-agents

**7. Permission Presets via allowedTools**

- When to use: Trusted operations, workflow automation, team standards
- Exact trigger / command: Add to settings.json: `permissions.allow` array, or `--allowedTools` flag
- Gotcha: Deny rules override allow; order matters in permission hierarchy
- Source URL: https://www.claudelog.com/faqs/what-is-allowed-tools-in-claude-code/

**8. Sandboxed Development**

- When to use: Prompt injection concerns, untrusted repos, autonomous agent workflows
- Exact trigger / command: `/sandbox` command
- Gotcha: May need to allow specific paths/domains; reduces prompts 84% but adds config overhead
- Source URL: https://www.anthropic.com/engineering/claude-code-sandboxing

**9. Extended Thinking for Complex Problems**

- When to use: Complex refactors, multi-step reasoning, formal verification, algorithm design
- Exact trigger / command: `Tab` key to toggle, or include "think" in prompt
- Gotcha: Higher token cost, slower responses; overkill for routine tasks
- Source URL: https://www.anthropic.com/news/visible-extended-thinking

**10. Task Dependencies for Multi-Session Work**

- When to use: Complex projects, parallel workstreams, multi-agent orchestration
- Exact trigger / command: Set `CLAUDE_CODE_TASK_LIST_ID` env var, use TaskCreate/TaskUpdate tools
- Gotcha: Tasks persist in `~/.claude/tasks/`, not project-specific unless configured
- Source URL: https://claudefa.st/blog/guide/development/task-management

**11. Hooks for Deterministic Actions**

- When to use: Auto-formatting, linting, testing, commit message validation
- Exact trigger / command: `/hooks` command or edit `settings.json` hooks field
- Gotcha: Stop/SubagentStop hooks use `blocking:false` by default to prevent loops
- Source URL: https://code.claude.com/docs/en/hooks

**12. MCP Servers for External Tools**

- When to use: Access live data, proprietary APIs, specialized tools not built-in
- Exact trigger / command: `claude mcp add server-name`, or `/mcp` command in session
- Gotcha: OAuth required for many remote servers; stdio transport more reliable than HTTP
- Source URL: https://code.claude.com/docs/en/mcp

**13. Skills for Domain Expertise**

- When to use: Security patterns, API design, testing conventions—expertise that applies conditionally
- Exact trigger / command: Create `SKILL.md` in `~/.claude/skills/` with descriptive frontmatter
- Gotcha: Description field is critical for auto-loading; keep focused to avoid loading irrelevant skills
- Source URL: https://code.claude.com/docs/en/skills

**14. Chrome Integration for Build-Test-Verify**

- When to use: Frontend development, UI testing, design verification vs Figma
- Exact trigger / command: `claude --chrome`, then `/chrome` to confirm connection
- Gotcha: Requires paid plan, no WSL support, needs Chrome extension installed
- Source URL: https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/

**15. GitHub Actions Integration**

- When to use: PR feedback automation, issue-to-PR conversion, CI error fixes
- Exact trigger / command: Add `anthropics/claude-code-action@v1` to `.github/workflows/`
- Gotcha: Requires `ANTHROPIC_API_KEY` secret; respects `CLAUDE.md` for standards
- Source URL: https://code.claude.com/docs/en/github-actions


## 3) Configuration + Artifacts Map

- **CLAUDE.md** (root, subdirs, `~/.claude/`): Auto-loaded project context; use `.claude/rules/` for modular organization https://www.builder.io/blog/claude-md-guide
- **settings.json** (precedence: managed > local > project > user): Permissions, environment variables, tool behavior https://code.claude.com/docs/en/settings
- **~/.claude/commands/** or **.claude/commands/**: Custom slash commands with `$ARGUMENTS` support https://shipyard.build/blog/claude-code-cheat-sheet/
- **~/.claude/skills/** or **.claude/skills/**: SKILL.md files with YAML frontmatter for auto-loading https://code.claude.com/docs/en/skills
- **~/.claude/agents/** or **.claude/agents/**: Custom subagent definitions (Markdown format) https://code.claude.com/docs/en/sub-agents
- **~/.claude.json**: MCP server configurations (`mcpServers` field) + global settings https://code.claude.com/docs/en/mcp
- **.mcp.json**: Project-scoped MCP servers, team-shared https://code.claude.com/docs/en/mcp
- **hooks/hooks.json** (in plugin): Hook configurations for lifecycle events https://code.claude.com/docs/en/hooks
- **.claude-plugin/plugin.json**: Plugin manifest (REQUIRED, only file in this directory) https://code.claude.com/docs/en/plugins-reference
- **~/.claude/tasks/**: Task persistence storage; share via `CLAUDE_CODE_TASK_LIST_ID` https://claudefa.st/blog/guide/development/task-management
- **~/.claude/output-styles/**: Custom output style definitions with `keep-coding-instructions` flag https://code.claude.com/docs/en/output-styles
- **~/.claude/keybindings.json**: Custom keyboard shortcuts, generated via `/keybindings` https://code.claude.com/docs/en/keybindings


## 4) Plugins / MCP / Integrations shortlist

- **claude-plugins-official**: Anthropic's official marketplace, auto-available at startup; install via `/plugin install plugin-name@claude-plugins-official` https://code.claude.com/docs/en/discover-plugins
- **GitHub Actions (anthropics/claude-code-action@v1)**: @claude mentions trigger autonomous PR creation/issue implementation; requires `ANTHROPIC_API_KEY` secret https://code.claude.com/docs/en/github-actions
- **Chrome extension (v2.10+)**: Browser automation for build-test-verify loop; requires Claude Pro/Max+, install from Chrome Web Store https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/
- **VS Code extension**: Inline diffs, @-mentions, plan review; install .vsix from `@anthropic-ai/claude-code` npm package https://code.claude.com/docs/en/vs-code
- **MCP stdio servers**: Local tools (filesystem, databases); more reliable than HTTP transport https://code.claude.com/docs/en/mcp
- **MCP HTTP servers with OAuth**: Remote services (Sentry, Linear, GitHub); use `claude mcp add --transport http` https://code.claude.com/docs/en/mcp
- **Claude Code as MCP server**: `claude mcp serve` exposes Claude Code tools to Claude Desktop https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/
- **Agent SDK (@anthropic-ai/claude-agent-sdk)**: Programmatic access for custom agents; supports structured output via JSON schemas https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk


## 5) Security / safety notes (Top 8)

- **Sandboxing (Oct 2025)**: Filesystem isolation to cwd, network via proxy; 84% fewer permission prompts; activate with `/sandbox` https://www.anthropic.com/engineering/claude-code-sandboxing
- **Permission hierarchy**: deny → ask → allow (first match); deny rules override allow; configure in `settings.json` permissions field https://www.claudelog.com/faqs/how-to-set-claude-code-permission-mode/
- **YOLO mode (`--dangerously-skip-permissions`)**: Use ONLY in sandboxed/containerized environments; no safety guardrails https://www.reddit.com/r/ClaudeAI/comments/1kuj1dm/how_to_run_claude_code_in_yolo_mode_a_quick_guide/
- **Managed settings (enterprise)**: `managed-settings.json` highest precedence; deploy fixed MCP servers or use allowlist/denylist policies https://code.claude.com/docs/en/mcp
- **Background subagents**: Auto-deny anything not pre-approved; can't ask clarifying questions; use for trusted isolated tasks https://code.claude.com/docs/en/sub-agents
- **Hook loop risk**: Stop/SubagentStop hooks with `blocking:true` can create infinite loops; default `blocking:false` prevents this https://code.claude.com/docs/en/hooks
- **Sandbox override**: Claude Code may override sandbox without permission (community reports); verify behavior in your version https://www.reddit.com/r/Anthropic/comments/1oc8uq9/claude_code_overrides_the_sandbox_without/
- **Tool restrictions in subagents**: Use `tools` (allowlist) or `disallowedTools` (denylist) in agent frontmatter; inherits parent by default https://code.claude.com/docs/en/sub-agents


## 6) Conflicts / version-sensitive items

- **Auto-compact behavior**: May trigger unexpectedly, losing early instructions; community recommends disabling for serious work, but configuration method varies by version; **Verify**: Check `/config` for auto-compact settings in your version; **Best guess**: Manual `/compact [focus]` preferred; https://www.reddit.com/r/ClaudeAI/comments/1lmoeej/claude_code_maintain_context_best_practice_prior/
- **Plan mode → auto-accept**: Approving plan may auto-enable acceptEdits mode (GitHub issue open); **Verify**: Test in your workflow; **Best guess**: Explicitly disable acceptEdits after plan approval; https://github.com/anthropics/claude-code/issues/2988
- **Session context recovery**: `--resume` restores command history but context recovery varies; **Verify**: Test resume behavior with complex sessions; **Best guess**: CLAUDE.md helps maintain project knowledge across resumes; https://www.reddit.com/r/ClaudeCode/comments/1ns47r4/how_does_one_start_claude_with_an_existing/
- **Tasks vs. Todos**: Tasks introduced v2.1.x (Jan 2025) replacing Todos; **Verify**: Check your version; **Best guess**: `CLAUDE_CODE_ENABLE_TASKS=false` reverts to Todos; https://www.reddit.com/r/ClaudeAI/comments/1qkjznp/anthropic_replaced_claude_codes_old_todos_with/
- **WSL compatibility**: Chrome integration and some IDE features unreliable in WSL; **Verify**: Test in your environment; **Best guess**: Native Windows or Mac preferred; https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/
- **Agent SDK V2 development**: V1 stable but breaking changes possible; **Verify**: Check release notes for SDK updates; **Best guess**: Pin SDK version for production agents; https://nader.substack.com/p/the-complete-guide-to-building-agents
- **Output styles keep-coding-instructions**: Default `false` for custom styles loses coding expertise; **Verify**: Test custom output styles; **Best guess**: Set `keep-coding-instructions: true` for coding workflows; https://code.claude.com/docs/en/output-styles
- **MCP OAuth flows**: Some servers require browser login, others fail silently; **Verify**: Test OAuth servers individually; **Best guess**: stdio transport more reliable than HTTP; https://code.claude.com/docs/en/mcp


## 7) Prompt B launchpad

**Follow-up questions:**

1. What are the exact YAML frontmatter fields for SKILL.md and how does the auto-loading algorithm work (description matching, keyword extraction, context size)?
2. How do you configure `PreToolUse` hooks to block specific Bash commands with glob patterns while allowing others?
3. What is the complete permission syntax for `allowedTools` (glob patterns, regex, tool chaining) and precedence rules when rules conflict?
4. How does the Task dependency graph resolve blockers across multiple sessions when tasks complete out of order?
5. What are the exact differences between VS Code extension mode and terminal `/ide` mode in terms of context syncing and file awareness?
6. How do you create a custom MCP server (stdio vs HTTP) with OAuth 2.0 and what are the manifest schema requirements?
7. What are the token costs (startup, per-invocation) of Skills vs Slash Commands vs Subagents vs Output Styles at different context sizes?
8. How does Claude Code's compaction algorithm decide what to preserve vs summarize, and can you influence it with PreCompact hooks?
9. What is the complete keybindings.json schema and how do you override default shortcuts for specific contexts (Chat, Editor, Terminal)?
10. How do you orchestrate multiple subagents with shared task lists and MCP servers for parallel feature development workflows?

**Search terms / queries:**

1. "Claude Code SKILL.md frontmatter schema allowed-tools syntax"
2. "Claude Code hooks PreToolUse blocking glob patterns examples"
3. "Claude Code permission syntax allowedTools regex wildcard"
4. "Claude Code task dependencies multi-session real-time broadcast"
5. "Claude Code VS Code extension vs terminal ide mode comparison"
6. "MCP server implementation OAuth stdio HTTP manifest schema"
7. "Claude Code skills slash commands token cost comparison benchmark"
8. "Claude Code compaction algorithm PreCompact hook influence context"
9. "Claude Code keybindings.json schema context override examples"
10. "Claude Code multi-agent orchestration parallel workflows task coordination"

## 8) Source pack (Top 15 URLs)

1. **https://code.claude.com/docs/en/overview** - Official docs hub, authoritative reference (updated Jan 2026)
2. **https://www.anthropic.com/engineering/claude-code-best-practices** - Anthropic engineering best practices (Apr 2025)
3. **https://claudefa.st/blog/guide/changelog** - Complete version history with feature annotations (updated Jan 2026)
4. **https://www.builder.io/blog/claude-md-guide** - CLAUDE.md complete guide with examples (Jan 2026)
5. **https://code.claude.com/docs/en/settings** - Settings hierarchy and precedence (official, Jan 2026)
6. **https://code.claude.com/docs/en/skills** - Skills system with frontmatter schema (official, Jan 2026)
7. **https://code.claude.com/docs/en/sub-agents** - Subagents creation and delegation (official, Jan 2026)
8. **https://code.claude.com/docs/en/hooks** - Hooks reference with event types (official, Jan 2026)
9. **https://code.claude.com/docs/en/mcp** - MCP integration guide with OAuth (official, Jan 2026)
10. **https://www.anthropic.com/engineering/claude-code-sandboxing** - Sandboxing architecture and security (Oct 2025)
11. **https://code.claude.com/docs/en/github-actions** - GitHub Actions integration setup (official, Jan 2026)
12. **https://rewire.it/blog/claude-code-agents-skills-slash-commands/** - Skills vs Commands vs Agents comparison (Oct 2024)
13. **https://www.cometapi.com/managing-claude-codes-context/** - Context management practical handbook (Jan 2026)
14. **https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk** - Agent SDK programmatic guide (Sep 2025)
15. **https://shipyard.build/blog/claude-code-cheat-sheet/** - CLI cheatsheet with shortcuts (Jan 2026)

## 9) JSON Appendix (for Labs/NotebookLM)

```json
{
  "key_findings": [
    {
      "claim": "CLAUDE.md is auto-loaded project memory; use # key to add entries mid-session",
      "source_url": "https://www.builder.io/blog/claude-md-guide",
      "confidence": 1.0,
      "how_to_apply": "/init to generate, place in project root or ~/.claude/, organize with .claude/rules/ for modularity"
    },
    {
      "claim": "Sandboxing (Oct 2025) reduced permission prompts 84% via filesystem + network isolation",
      "source_url": "https://www.anthropic.com/engineering/claude-code-sandboxing",
      "confidence": 1.0,
      "how_to_apply": "Activate with /sandbox command; enables safe autonomous operation in untrusted repos"
    },
    {
      "claim": "Skills (30-50 tokens startup) auto-load based on description field; Slash Commands (100-1000 tokens) expand on invocation",
      "source_url": "https://rewire.it/blog/claude-code-agents-skills-slash-commands/",
      "confidence": 0.95,
      "how_to_apply": "Skills for conditional expertise, Slash Commands for frequent atomic tasks; create SKILL.md with precise description"
    },
    {
      "claim": "Permission hierarchy: deny → ask → allow (first match wins); configure in settings.json permissions field",
      "source_url": "https://www.claudelog.com/faqs/how-to-set-claude-code-permission-mode/",
      "confidence": 1.0,
      "how_to_apply": "Use allowedTools array with glob patterns (e.g., Bash(git *)) to pre-approve trusted operations"
    },
    {
      "claim": "Tasks system (v2.1.x, Jan 2025) supports dependencies and multi-session persistence via CLAUDE_CODE_TASK_LIST_ID",
      "source_url": "https://claudefa.st/blog/guide/development/task-management",
      "confidence": 1.0,
      "how_to_apply": "Export CLAUDE_CODE_TASK_LIST_ID=project-name for shared task lists; use addBlockedBy for dependencies"
    },
    {
      "claim": "Hooks provide deterministic control at lifecycle events; Stop/SubagentStop default blocking:false to prevent loops",
      "source_url": "https://code.claude.com/docs/en/hooks",
      "confidence": 1.0,
      "how_to_apply": "Configure PostToolUse hooks for auto-formatting/linting; use PreToolUse to block specific commands"
    }
  ],
  "superuser_moves": [
    {
      "name": "CLAUDE.md Project Memory",
      "trigger": "/init to generate, # key to add entries",
      "when": "Start of every project, updated as architecture evolves",
      "verification": "Check with /context command to see CLAUDE.md in context window",
      "source_url": "https://www.builder.io/blog/claude-md-guide"
    },
    {
      "name": "Plan Mode Before Execution",
      "trigger": "Shift+Tab twice or /plan command",
      "when": "Complex tasks, unfamiliar codebases, high-stakes changes",
      "verification": "Claude presents plan for approval before making changes",
      "source_url": "https://moonandeye.github.io/en/programming/think-mode-on-claude-code/"
    },
    {
      "name": "Background Tasks (Ctrl+B)",
      "trigger": "Ctrl+B when command is running (twice in tmux)",
      "when": "Dev servers, build tools, test runners, Docker, Terraform",
      "verification": "Command runs in background, Claude continues working",
      "source_url": "https://code.claude.com/docs/en/interactive-mode"
    },
    {
      "name": "Sandboxed Development",
      "trigger": "/sandbox command",
      "when": "Prompt injection concerns, untrusted repos, autonomous workflows",
      "verification": "84% reduction in permission prompts, filesystem isolated to cwd",
      "source_url": "https://www.anthropic.com/engineering/claude-code-sandboxing"
    },
    {
      "name": "MCP Servers for External Tools",
      "trigger": "claude mcp add server-name or /mcp in session",
      "when": "Access live data, proprietary APIs, specialized tools",
      "verification": "Server appears in /mcp list, tools available in session",
      "source_url": "https://code.claude.com/docs/en/mcp"
    }
  ],
  "tools_and_configs": [
    {
      "thing": "CLAUDE.md",
      "purpose": "Auto-loaded project context (facts, architecture, standards); use .claude/rules/ for modularity",
      "source_url": "https://www.builder.io/blog/claude-md-guide"
    },
    {
      "thing": "settings.json (precedence: managed > local > project > user)",
      "purpose": "Permissions, environment variables, tool behavior, output styles",
      "source_url": "https://code.claude.com/docs/en/settings"
    },
    {
      "thing": "~/.claude/skills/ or .claude/skills/",
      "purpose": "SKILL.md files with YAML frontmatter for auto-loading domain expertise",
      "source_url": "https://code.claude.com/docs/en/skills"
    },
    {
      "thing": "~/.claude/agents/ or .claude/agents/",
      "purpose": "Custom subagent definitions (Markdown format) with tool restrictions",
      "source_url": "https://code.claude.com/docs/en/sub-agents"
    },
    {
      "thing": "~/.claude.json or .mcp.json",
      "purpose": "MCP server configurations (user/project scopes) with OAuth support",
      "source_url": "https://code.claude.com/docs/en/mcp"
    },
    {
      "thing": "hooks/hooks.json",
      "purpose": "Lifecycle event automation (PreToolUse, PostToolUse, Stop) for deterministic behavior",
      "source_url": "https://code.claude.com/docs/en/hooks"
    },
    {
      "thing": "~/.claude/tasks/[task-list-id]/",
      "purpose": "Task persistence with dependencies; share via CLAUDE_CODE_TASK_LIST_ID env var",
      "source_url": "https://claudefa.st/blog/guide/development/task-management"
    }
  ],
  "risks": [
    {
      "risk": "YOLO mode (--dangerously-skip-permissions) bypasses all safety guardrails",
      "mitigation": "Use ONLY in sandboxed/containerized environments; prefer allowedTools for granular control",
      "source_url": "https://www.reddit.com/r/ClaudeAI/comments/1kuj1dm/how_to_run_claude_code_in_yolo_mode_a_quick_guide/"
    },
    {
      "risk": "Hook loops: Stop/SubagentStop hooks with blocking:true can create infinite retry loops",
      "mitigation": "Default blocking:false prevents loops; set blocking:true only when you understand the risk",
      "source_url": "https://code.claude.com/docs/en/hooks"
    },
    {
      "risk": "Auto-compact may trigger unexpectedly, losing early instructions and context",
      "mitigation": "Use manual /compact [focus instruction]; store persistent rules in CLAUDE.md, not conversation",
      "source_url": "https://www.cometapi.com/managing-claude-codes-context/"
    },
    {
      "risk": "Background subagents auto-deny anything not pre-approved; can't ask clarifying questions",
      "mitigation": "Pre-approve all required tools via allowedTools; use foreground subagents for interactive tasks",
      "source_url": "https://code.claude.com/docs/en/sub-agents"
    },
    {
      "risk": "Plan mode may auto-enable acceptEdits mode after approval (unexpected behavior)",
      "mitigation": "Explicitly disable acceptEdits after plan approval; GitHub issue open for configuration option",
      "source_url": "https://github.com/anthropics/claude-code/issues/2988"
    },
    {
      "risk": "MCP OAuth flows may fail silently; HTTP transport less reliable than stdio",
      "mitigation": "Test OAuth servers individually; prefer stdio transport for local tools; check MCP logs",
      "source_url": "https://code.claude.com/docs/en/mcp"
    },
    {
      "risk": "Custom output styles lose coding expertise unless keep-coding-instructions:true",
      "mitigation": "Set keep-coding-instructions:true in output style frontmatter for coding workflows",
      "source_url": "https://code.claude.com/docs/en/output-styles"
    },
    {
      "risk": "Session resume restores command history but context recovery varies",
      "mitigation": "Use CLAUDE.md to maintain project knowledge; don't rely on resume for critical context",
      "source_url": "https://www.reddit.com/r/ClaudeCode/comments/1ns47r4/how_does_one_start_claude_with_an_existing/"
    }
  ],
  "open_questions": [
    {
      "question": "What is the exact auto-loading algorithm for Skills (description matching, keyword extraction, context size)?",
      "why_it_matters": "Critical for writing skill descriptions that trigger reliably without polluting context with irrelevant skills"
    },
    {
      "question": "How does the Task dependency graph resolve blockers when tasks complete out of order across multiple sessions?",
      "why_it_matters": "Essential for parallel workstream orchestration and multi-agent collaboration patterns"
    },
    {
      "question": "What are the token costs (startup, per-invocation) of Skills vs Slash Commands vs Subagents vs Output Styles?",
      "why_it_matters": "Optimize configuration choices based on actual token budgets and cost constraints"
    },
    {
      "question": "How does Claude Code's compaction algorithm decide what to preserve vs summarize?",
      "why_it_matters": "Understanding compaction behavior enables better pre-compact state management and context optimization"
    },
    {
      "question": "Can you influence compaction behavior with PreCompact hooks or focus instructions?",
      "why_it_matters": "Enables custom compaction strategies for different project types and workflow patterns"
    }
  ]
}
```

<span style="display:none">[^1]</span>

<div align="center">⁂</div>

[^1]: Sean-Winslow-Profile-Context-Compact.md

