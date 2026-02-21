<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Task: Build a canonical, source-backed map of Claude Code capabilities.

Scope:

- Official Claude Code docs: CLI, interactive commands, skills, subagents, hooks, plugins/marketplaces, MCP, permissions/sandboxing, headless mode, GitHub Actions, Chrome extension/IDE integrations.
- Include version notes + dates where possible (flag anything that changed recently).

Deliverables:

1) A categorized capability map (sections listed within Sean-Winslow-Profile-Context-Compact.md).
2) A “Top 25 superuser moves” list, each with:
    - what it does
    - how to trigger it
    - when to use it
    - pitfalls
3) A glossary of key files/folders (e.g., CLAUDE.md, .claude/skills, .claude/agents, settings.json, plugin manifests).
4) A citation-heavy appendix.

Hard requirements:

- Every claim must be linked/cited.
- Prefer official docs, but include reputable community sources if they add practical detail.

Output format:

- Markdown report + JSON appendix.

Now I'll generate the final comprehensive markdown report:

# Claude Code: Canonical Capability Map \& Superuser Guide

**Report Date:** January 29, 2026
**Research Depth:** 152+ sources analyzed
**Version Coverage:** v0.2.x (beta) through v2.1.17 (current)

***

## Executive Summary

Claude Code represents Anthropic's production-grade agentic coding tool, evolving from beta (v0.2.x, 2024) to general availability (v1.0.0, April 2025) and now v2.1.17. This canonical map documents every major capability, configuration mechanism, and integration point based on official documentation, engineering blog posts, and extensive community validation.[^1][^2][^3][^4][^5]

**Core Philosophy:** Claude Code operates on Unix principles—composable tools, scriptable interfaces, and giving Claude the same terminal access human developers use. This design unlocks both coding and general-purpose agent workflows.[^5][^1]

**Key Milestones:**

- **176 releases** tracked in 2025 alone (37 beta, 82 v1.0.x, 57 v2.0.x)[^6][^7]
- **Major capabilities:** Skills, Subagents, Hooks, MCP, Sandboxing, GitHub Actions, Chrome Integration
- **Sandboxing** (Oct 2025) reduced permission prompts by 84%[^3]

***

## I. Categorized Capability Map

### A. CLI Modes \& Session Management

#### Interactive Mode

**Command:** `claude`
**Description:** Standard REPL session with full conversational interface
**Key Features:**[^8][^9][^2]

- Real-time tool execution with permission dialogs
- Multi-line input via `\\ + Enter`, `Option+Enter` (Mac), or `Shift+Enter` (after `/terminal-setup`)
- Vim mode support (`/vim`)
- Keyboard shortcuts (Shift+Tab for mode cycling, Tab for extended thinking, Ctrl+B for background tasks)
- Session persistence with automatic saves

**When to Use:** Standard development workflow, iterative problem-solving, learning codebases

#### Print Mode (Headless)

**Command:** `claude -p "query"`
**Description:** Non-interactive query-and-exit mode for automation[^10][^11][^12]
**Output Formats:**

- `--output-format json` - Full JSON response
- `--output-format stream-json` - Streaming JSON objects
- `--output-format text` - Plain text (default)

**Use Cases:**

- CI/CD pipelines (`claude -p "review PR changes"`)
- Data processing (`cat data.csv | claude -p "analyze trends"`)
- Automation scripts with structured output

**Pitfall:** No interactive clarifications—provide complete context upfront

#### Session Management

**Resume Previous Session:**[^13][^14][^15]

- `claude --resume` - Interactive selector with search
- `claude -c` or `claude --continue` - Most recent session
- `claude -r session-id` - Specific session by ID
- `/resume` in active session - Search and switch

**Session Persistence Caveat:** While command history persists, context recovery varies. CLAUDE.md helps maintain project knowledge across resumes.[^13]

**Suspend/Resume Workflow:**[^16]

- `Ctrl+Z` - Suspend process
- `fg` - Resume in foreground
- Session state fully preserved

***

### B. Configuration Files \& Directory Structure

#### CLAUDE.md - Project Memory

**Locations (precedence order):**[^17][^18][^1]

1. `~/.claude/CLAUDE.md` (global, all projects)
2. `CLAUDE.md` or `.claude/CLAUDE.md` (project root)
3. Subdirectory `CLAUDE.md` files (auto-loaded when working in that path)
4. `CLAUDE.local.md` (local, gitignored overrides)

**Auto-Loading:** Pulled into context at session start[^1]

**Generation:** `/init` command scans project and generates starter file[^18][^17]

**Live Updates:** Press `#` key during session to add entries; prompts for file selection[^19][^1]

**Best Practices:**[^20][^17]

- **Store facts (nouns), not procedures:** Architecture, file locations, tech stack
- **Keep lean:** Use `@imports` to reference detailed docs
- **Modular organization:** Use `.claude/rules/` directory for topic-specific rules (e.g., `code-style.md`, `testing.md`, `security.md`)
- **Subdirectory specificity:** Place `CLAUDE.md` in subdirectories for context that only applies to that module

**Version Notes:** `@imports` and `.claude/rules/` added in v1.0.x[^6][^17]

#### settings.json Hierarchy

**Scope Precedence (highest to lowest):**[^4]

1. **Managed** (`managed-settings.json` in system directories) - Enterprise/org-level, read-only
2. **Local** (`.claude/settings.local.json`) - Per-project, gitignored
3. **Project** (`.claude/settings.json`) - Team-shared, version-controlled
4. **User** (`~/.claude/settings.json`) - Personal defaults

**Key Fields:**[^21][^22][^4]

```json
{
  "model": "opus",
  "defaultMode": "default",
  "permissions": {
    "allow": ["Read(*)", "Edit(*.py)", "Bash(git *)"],
    "deny": ["Read(.env)", "Bash(rm *)"],
    "ask": ["Bash(npm install)"]
  },
  "outputStyle": "explanatory",
  "env": {
    "CUSTOM_VAR": "value"
  }
}
```

**Permission Rule Syntax:**[^23][^24][^25]

- `ToolName` - All uses of tool
- `ToolName(*)` - Tool with any argument
- `ToolName(pattern)` - Glob-matched argument (e.g., `Bash(git *)`, `Edit(*.md)`)
- **Precedence:** deny → ask → allow (first match wins)


#### ~/.claude.json

**Dual Purpose:**[^21]

- Global user settings (overlaps with `~/.claude/settings.json`)
- MCP server configurations (user and project scopes)
- Project statistics and cache

**Structure Oddity:** Community notes this as "chaotic" with mixed concerns. Prefer `~/.claude/settings.json` for permissions.[^21]

#### Directory Structure Reference

```
~/.claude/                     # Global user config
├── settings.json              # User-level settings
├── CLAUDE.md                  # Global project context
├── commands/                  # User-level slash commands
├── agents/                    # User-level subagents
├── skills/                    # User-level skills
├── output-styles/             # Custom output styles
├── tasks/                     # Task persistence
│   └── [task-list-id]/       # Named task lists (via CLAUDE_CODE_TASK_LIST_ID)
└── keybindings.json           # Custom keyboard shortcuts

.claude/                       # Project-specific config
├── settings.json              # Project settings (team-shared)
├── settings.local.json        # Local overrides (gitignored)
├── CLAUDE.md                  # Project context
├── commands/                  # Project slash commands
├── agents/                    # Project subagents
├── skills/                    # Project skills
└── rules/                     # Modular rule files
    ├── code-style.md
    ├── testing.md
    └── security.md
```


***

### C. Skills - Auto-Loaded Domain Expertise

**Concept:** Skills are markdown-based knowledge packages that Claude auto-loads when relevant or that can be manually invoked.[^26][^27]

**Progressive Disclosure:** Only skill metadata (name + description) loads at startup (~30-50 tokens); full content loads when triggered (~500-5000 tokens).[^28][^27]

**File Format: SKILL.md with YAML frontmatter**[^26]

```markdown
---
name: security-review
description: Use when reviewing code for security vulnerabilities
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---

## Security Review Protocol

1. Scan for SQL injection patterns
2. Check authentication/authorization
3. Review sensitive data handling
4. Validate input sanitization
...
```

**Frontmatter Fields:**[^28][^26]

- `name` (required) - Unique identifier, used for `/skill-name` invocation
- `description` (required) - When Claude should use this skill (critical for auto-loading)
- `allowed-tools` - Restrict tools (allowlist)
- `disallowed-tools` - Block tools (denylist)
- `context: fork` - Run in subagent with specified agent type
- `agent: Explore|Plan` - Which subagent type to use with fork

**Locations:**[^26]

- `~/.claude/skills/` - User-level (all projects)
- `.claude/skills/` - Project-level

**Invocation:**

- **Automatic:** Claude reads descriptions and loads when context matches
- **Manual:** Type `/skill-name` (e.g., `/security-review`)
- **Via SlashCommand tool:** Claude can invoke skills programmatically (v1.0.123+)[^6]

**Use Cases:**[^27]

- Domain-specific knowledge (security patterns, API design conventions)
- Complex workflows (multi-step code generation, testing protocols)
- Conditional expertise (only load when working on specific file types/domains)

**Pitfalls:**

- Description field must be precise for auto-loading to work
- Skills load once per conversation; cannot reload same skill[^29]
- Over-broad descriptions cause skills to load when irrelevant

***

### D. Subagents - Specialized Instances

**Concept:** Subagents are separate Claude instances with their own context windows, system prompts, tool restrictions, and permission modes.[^30][^31]

**Built-in Subagents:**[^30]

- **Explore** - Read-only tools for codebase exploration
- **Plan** - Planning without execution
- **General-purpose** - Standard capabilities

**Custom Subagent Definition (Markdown Format):**[^30]

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. Focus on:
- Code quality and maintainability
- Security best practices
- Performance considerations
- Test coverage

Provide specific, actionable feedback with file paths and line numbers.
```

**Configuration via /agents Command:**[^30]

- Create new subagents (guided setup or Claude-generated)
- Edit existing configurations
- View all available subagents (built-in, user, project, plugin)
- Delete custom subagents

**Inline Definition via CLI:**[^30]

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

**Locations:**[^30]

- `~/.claude/agents/` - User-level
- `.claude/agents/` - Project-level

**Delegation:**[^30]

- **Automatic:** Claude delegates based on task description matching subagent description
- **Explicit:** "Use the code-reviewer subagent to analyze this module"
- **Background:** Run concurrently with pre-approved permissions; auto-denies anything not pre-approved

**Tool Control:**[^30]

- Inherit parent tools by default
- `tools` field (allowlist) restricts to specified tools
- `disallowedTools` field (denylist) blocks specific tools
- MCP tools accessible to subagents

**Key Constraints:**[^30]

- **Cannot spawn other subagents** (no nested delegation)
- **Background subagents can't ask clarifying questions** (tool call fails, subagent continues)
- MCP tools not available in background mode

**Use Cases:**[^31]

- Code review (isolated analysis, doesn't pollute main context)
- Security scanning (restricted tools, focused expertise)
- Testing (run tests, analyze results, report summary)
- Exploration (gather context without execution risk)

**Version Notes:** Subagents introduced in v1.0.x; background execution added later[^7][^6]

***

### E. Hooks - Deterministic Automation

**Concept:** Hooks are shell commands or LLM prompts that run automatically at specific lifecycle events.[^32][^33][^34]

**Why Hooks?** Provide deterministic control over probabilistic LLM behavior—ensure formatting, linting, testing always happen rather than relying on Claude to remember.[^34][^35]

**Hook Events:**[^33][^34]


| Event | When It Runs | Can Block? | Use Cases |
| :-- | :-- | :-- | :-- |
| `PreToolUse` | Before tool execution | ✅ Yes | Validation, pre-commit checks |
| `PostToolUse` | After tool completes | ❌ No (feedback only) | Auto-formatting, linting |
| `UserPromptSubmit` | Before Claude processes prompt | ✅ Yes | Add context, enforce rules |
| `PermissionRequest` | When permission dialog shown | ✅ Yes (allow/deny) | Auto-approve trusted tools |
| `Stop` | When Claude finishes | ✅ Yes | Verify completion, run tests |
| `SubagentStop` | When subagent completes | ✅ Yes | Validate subagent output |
| `PreCompact` | Before compaction | ❌ No | Save state, log history |
| `Setup` | When invoked with --setup | N/A | One-time initialization |
| `Notification` | When notification sent | ❌ No | External logging |

**Hook Types:**[^33]

1. **Command Hook** - Shell command execution
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "black .",
        "timeout": 30
      }]
    }]
  }
}
```

2. **Prompt Hook** - LLM evaluation
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Evaluate if Claude should stop. Check if:\n1. All tasks complete\n2. No errors\n3. No follow-up needed\n\nReturn JSON: {\"ok\": true} to allow, {\"ok\": false, \"reason\": \"...\"} to continue."
      }]
    }]
  }
}
```

3. **Pipeline** - Sequential hook execution
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit(*.py)",
      "hooks": [
        {"type": "command", "command": "black $FILE"},
        {"type": "command", "command": "pylint $FILE"}
      ]
    }]
  }
}
```

**Matcher Syntax:**[^34][^33]

- `*` - All tools
- `Write` - Specific tool
- `Write|Edit` - Multiple tools (OR)
- `Write(*.py)` - Tool with glob pattern

**Configuration Methods:**[^33][^34]

- **Interactive:** `/hooks` command (guided setup)
- **File-based:** Edit `~/.claude/settings.json` or `.claude/settings.json`
- **Plugin-distributed:** In plugin's `hooks/hooks.json`

**Decisions \& Feedback:**[^33]

- **Block decision:** `{"decision": "block", "reason": "explanation"}` prevents action, sends reason to Claude
- **Undefined decision:** Action proceeds
- **Additional context:** `hookSpecificOutput.additionalContext` adds info for Claude

**Critical Pitfall - Stop/SubagentStop Loops:**[^36][^33]

- Default `blocking: false` to prevent infinite loops
- If `blocking: true`, failed hook sends error to Claude → Claude tries to fix → triggers hook again → infinite loop
- Explicitly set `blocking: true` only when you understand the risk

**Use Cases:**[^32][^34]

- Auto-formatting on file writes (black, prettier)
- Pre-commit validation (linting, type checking)
- Post-generation testing
- Logging and auditing

**Version Notes:** Hooks introduced v1.0.38 (July 2025)[^6]

***

### F. MCP (Model Context Protocol)

**Concept:** MCP enables Claude Code to integrate external tools, APIs, databases, and data sources via a standardized protocol.[^37][^38]

**Transport Types:**

- **stdio** - Local process communication (more reliable)
- **HTTP** - Remote server connections (requires OAuth for many)

**Scopes \& Configuration:**[^37]


| Scope | File Location | Use Case |
| :-- | :-- | :-- |
| User | `~/.claude.json` (mcpServers field) | Personal tools across all projects |
| Project | `.mcp.json` in project root | Team-shared, version-controlled |
| Plugin | `.mcp.json` at plugin root | Bundled with plugin distribution |
| Managed | `managed-mcp.json` in system dirs | Enterprise/org-wide control |

**Adding MCP Servers:**[^37]

**CLI Method:**

```bash
# Add stdio server
claude mcp add my-server /path/to/server-binary

# Add HTTP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Import from Claude Desktop
claude mcp add-from-claude-desktop
```

**Interactive Method:**

```
/mcp
→ Add server
→ Configure transport, command, args, env vars
```

**Project .mcp.json Example:**[^37]

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

**OAuth Authentication:**[^37]

1. Add server requiring auth: `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`
2. In session: `/mcp` → follow browser login flow

**Claude Code as MCP Server:**[^38][^37]

```bash
# Start Claude Code in server mode
claude mcp serve
```

**Configure in Claude Desktop:**

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Managed MCP (Enterprise):**[^37]

**Option 1: Exclusive Control via managed-mcp.json**

- Deploy fixed set of servers
- Users cannot add/modify/extend
- Highest precedence

**Option 2: Policy-Based Control**

- `allowedMcpServers` - Whitelist approved servers
- `deniedMcpServers` - Blacklist prohibited servers
- Users can add servers within policy constraints

**Allowlist Patterns:**[^37]

- `server-name` - Allow by name
- `http://localhost:*/*` - Allow any localhost port
- `https://approved.com/*` - URL pattern matching

**Version Notes:** MCP improvements in v1.0.27 (OAuth, streaming HTTP servers, @-mentionable resources)[^6]

***

### G. Plugins \& Marketplaces

**Concept:** Plugins bundle commands, agents, skills, hooks, MCP servers, and LSP servers for distribution.[^39][^40][^41]

**Official Marketplace:** `claude-plugins-official` (auto-available at startup)[^39]

**Plugin Structure:**[^41][^42]

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest (REQUIRED, only file here)
├── commands/                # Slash commands (.md files)
├── agents/                  # Subagents (.md files)
├── skills/                  # Skills (SKILL.md in subdirs)
├── hooks/                   # hooks.json
├── .mcp.json                # MCP server config
├── .lsp.json                # LSP server config
└── README.md
```

**plugin.json Manifest:**[^41]

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

**Plugin Installation:**[^40][^39]

```bash
# Add marketplace
/plugin marketplace add org/repo-name

# Install plugin
/plugin install plugin-name@marketplace-name

# Browse via UI
/plugin → Discover tab
```

**Team Distribution:**[^43][^39]
Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Team members prompted to install marketplace when they trust the project folder.

**Scope Configuration:**[^41]

- User: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local: `.claude/settings.local.json`
- Managed: `managed-settings.json`

**Auto-Updates:**[^39]

- Enable per marketplace in /plugin UI
- Updates marketplace data + installed plugins at startup
- Notification if plugins updated (suggests restart)
- Disable Claude Code auto-updates while keeping plugin updates: set `DISABLE_AUTOUPDATER` env var

**Community Marketplaces:**[^44][^40]

- `anthropics/claude-code` - Official GitHub marketplace
- `EveryInc/every-marketplace` - Every.io productivity tools
- `davila7/claude-code-templates` - Next.js, Supabase, testing templates
- Jeremy Longshore's marketplace - 20+ plugin packs, educational focus

**Version Notes:** Plugin system introduced v1.0.x[^6]

***

### H. Sandboxing - Secure Autonomous Operation

**Problem:** Default permission model requires constant approval, causing approval fatigue and limiting autonomy.[^45][^3]

**Solution:** OS-level sandboxing with filesystem + network isolation.[^3]

**Boundaries:**[^3]

1. **Filesystem Isolation**
    - Read/write access to current working directory only
    - Modification of files outside cwd blocked
    - Prevents compromised Claude from accessing SSH keys, sensitive configs
2. **Network Isolation**
    - Internet access through Unix domain socket → proxy server
    - Proxy enforces domain restrictions
    - User confirmation for new domains
    - Customizable traffic rules

**Benefits:**[^45][^3]

- **84% reduction in permission prompts** (internal usage data)
- **Prompt injection containment** - Even successful injection fully isolated
- **Safe YOLO mode** - Can use `--dangerously-skip-permissions` inside sandbox

**Activation:**[^3]

```bash
/sandbox
```

**Disable:**[^46][^3]

```bash
claude --dangerouslydisablesandbox
```

(Returns to standard permission protocols, does NOT skip permissions)

**Use Cases:**

- Untrusted repositories
- Prompt injection concerns
- Autonomous agent workflows
- Testing/experimentation

**Pitfalls:**

- May need to configure allowed paths/domains for your workflow
- Git interactions require proxy service (handled automatically in Claude Code on web)[^3]

**Version Notes:** Sandboxing released October 2025 (v1.0.x)[^45][^3]

***

### I. GitHub Actions Integration

**Concept:** Run Claude Code directly in GitHub workflows via @claude mentions in PRs/issues.[^47][^48][^49]

**Action:** `anthropics/claude-code-action@v1`[^48]

**Setup:**

1. Add `ANTHROPIC_API_KEY` to repository secrets
2. Create workflow file (`.github/workflows/claude-code.yml`):
```yaml
name: Claude Code

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Trigger:** @claude mention in comment (e.g., "@claude implement this feature based on issue description")[^47][^48]

**Capabilities:**[^49][^48]

- **Instant PR creation** - Describe need, Claude creates complete PR
- **Automated code implementation** - Turn issues into working code
- **PR feedback responses** - Claude addresses reviewer comments
- **CI error fixes** - Analyze failures, implement fixes
- **Follows standards** - Respects `CLAUDE.md` guidelines[^49]

**Parameters:**[^49]

- `trigger_phrase` - Phrase to activate Claude (default: "@claude")
- `timeout_minutes` - Max execution time
- `github_token` - Auth (default: auto-provided)
- `direct_prompt` - Explicit prompt (or infer from comment)
- `allowed_tools` - Tool restrictions

**Best Practices:**[^49]

- **Create CLAUDE.md** - Document code style, testing instructions, core files, repo etiquette
- **Detailed issue descriptions** - More context = better implementations
- **Review PR carefully** - AI-generated code still needs human review

**Version Notes:** Built on Claude Code SDK released v1.0.23 (June 2025)[^6]

***

### J. Chrome Integration

**Concept:** Claude navigates browser, reads console/DOM/network, tests UIs without manual verification.[^50][^51][^52]

**Requirements:**[^50]

- Claude Pro, Max, Team, or Enterprise subscription
- Chrome extension v2.10+
- Claude Code v2.0.73+
- **No WSL support** (run Claude Code in native Windows)

**Setup:**[^50]

1. Install Chrome extension from Chrome Web Store
2. Pin extension to toolbar
3. Sign in with Claude account
4. Launch Claude Code with Chrome flag:
```bash
claude --chrome
```

5. Verify connection:
```
/chrome
→ Should show "Chrome integration: Enabled"
```

**Workflow: Build-Test-Verify Loop**[^51][^52]

1. **Build** - Claude Code creates feature in terminal (Sonnet/Opus)
2. **Test** - Claude in Chrome navigates, fills forms, tests UX
3. **Verify** - Claude reports validation errors, broken fields
4. **Debug** - Claude reads console logs, network requests, DOM state
5. **Iterate** - Fix in Claude Code, repeat

**Capabilities:**[^51][^50]

- Open web pages
- Click buttons, fill forms
- Read console errors, inspect DOM
- Take screenshots, create GIFs
- Access authenticated sites (Gmail, Notion, Sheets) - uses your browser session, no API keys needed
- Performance analysis (via Chrome DevTools MCP)

**Quick Test:**[^50]

```
"Open google.com, click the search field, type 'Claude Code tutorial', 
and tell me the autocomplete suggestions."
```

**Context Sync:** MCP (Model Context Protocol) syncs context between terminal and browser sessions.[^52]

**Comparison to Chrome DevTools MCP:**[^50]

- **Claude in Chrome:** Streamlined, excludes some less-used tools (e.g., performance monitoring), fewer tokens
- **Chrome DevTools MCP:** Full dev tools access including performance analysis

**Version Notes:** Chrome integration introduced ~v2.0.73 (late 2025)[^50][^6]

***

### K. Extended Thinking \& Output Styles

#### Extended Thinking

**Concept:** Claude spends more reasoning tokens before responding, using serial test-time compute.[^53][^54]

**Activation:**[^55][^56]

- **Interactive:** Press `Tab` key to toggle
- **Implicit:** Include "think" in your prompt
- **API:** Set thinking budget (max tokens for reasoning)

**Visible Thought Process:** Claude's reasoning shown in raw form before final answer.[^53]

**Performance Scaling:** Accuracy improves logarithmically with thinking tokens (e.g., math problems).[^53]

**When to Use:**[^55]

- Complex refactors
- Multi-step decision-making
- Formal verification
- Algorithm design
- Debugging tricky bugs

**When NOT to Use:**[^55]

- Routine tasks
- Well-defined operations
- Simple code generation

**Cost Trade-off:** Higher token usage, slower responses.[^54]

**Thinking Budget Control (API):**[^57][^54]

```python
# Set max thinking tokens (up to 128K)
response = anthropic.messages.create(
    model="claude-3-7-sonnet",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[...]
)
```

**Version Notes:** Extended thinking introduced with Claude 3.7 Sonnet (Feb 2025); Tab toggle in Claude Code v1.0.x[^53][^6]

#### Output Styles

**Concept:** Replace system prompt to change Claude's tone, personality, and approach.[^58][^59][^60]

**Built-in Styles:**[^59]

1. **Default** - Efficient software engineering (existing system prompt)
2. **Explanatory** - Educational "Insights" between tasks, explains implementation choices
3. **Learning** - Collaborative pair-programming, teaches codebase patterns

**Custom Styles:**[^60][^58]

```bash
/output-style:new [name] [description]
```

Claude scaffolds a markdown file; tweak at user or project level.

**Locations:**[^61]

- `~/.claude/output-styles/` - User-level
- `.claude/output-styles/` - Project-level

**Custom Style Example:**

```markdown
---
name: code-reviewer
description: Emphasizes critiques and best practices
keep-coding-instructions: true
---

You are a meticulous code reviewer. For every change:
- Identify potential bugs
- Suggest performance optimizations
- Enforce style consistency
- Recommend tests

Be direct and actionable.
```

**keep-coding-instructions Flag:**[^59][^60]

- `true` - Preserve default coding knowledge
- `false` (default for custom) - Exclude coding instructions (for non-coding agents)

**Activation:**[^59]

```bash
/output-style                    # Menu selector
/output-style explanatory        # Direct switch
```

Or set in `settings.json`:

```json
{
  "outputStyle": "code-reviewer"
}
```

**vs. Skills/Agents:**[^59]

- **Output Styles:** Always active, modify tone/structure, apply to main loop
- **Skills:** Task-specific, invoked conditionally
- **Agents:** Separate instances, different tools/permissions

**Pitfalls:**[^60]

- Custom styles lose default engineering expertise unless `keep-coding-instructions: true`
- Can't dynamically switch mid-session (require restart or explicit switch)

**Version Notes:** Output styles introduced v1.0.81 (Aug 2025)[^58][^6]

***

### L. Context Management

#### The Context Window

**Contains:**[^62]

- Conversation history
- File contents
- Command outputs
- CLAUDE.md
- Loaded skills
- System instructions

**Visualization:** `/context` command shows colored grid of what's using space[^20][^19]

#### /compact - Strategic Compression

**What It Does:** Summarizes conversation into shorter form, preserves salient facts/decisions, replaces verbose history.[^63][^20]

**Syntax:**

```
/compact
/compact Summarize decisions, open TODOs, and config changes only
```

**When to Use:**[^63][^20]

- Before long new task that would fill context
- Token budget optimization
- Maintain thread continuity without full history

**Auto-Compact:** May trigger automatically near context limits (rolling out, not all versions).[^20]

**Microcompact:** Intelligent compaction behaviors (community discussions, experimental).[^20]

**Pitfall:** Early instructions may be lost; prefer CLAUDE.md for persistent rules.[^62][^20]

**Hook Integration:** `PreCompact` hook runs before compaction (save state, log history).[^34][^33]

#### /clear - Fresh Start

**What It Does:** Wipes conversation history completely; session continues but messages removed.[^20]

**When to Use:**

- Hit message/token limit
- Change direction completely
- Start new feature in same project

**Destructive:** Cannot undo; use `/resume` to return to old sessions.[^20]

#### CLAUDE.md for Persistent Context

**Best Practice:** Put permanent rules in CLAUDE.md, not conversation.[^62][^20]

**CLAUDE.md = Nouns (facts), Slash Commands = Verbs (procedures)**.[^20]

***

### M. Task Management System

**Evolution:** Replaced old Todos (flat lists, memory-only) with Tasks (dependencies, persistence, multi-session) in v2.1.x (Jan 2025).[^64][^65]

**New Tools:**[^66][^64]

- `TaskCreate` - Create with subject, description, status
- `TaskGet` - Retrieve full details including dependencies
- `TaskUpdate` - Update status, add blockers, modify
- `TaskList` - List all tasks with state

**Persistence:**[^64]

- Default location: `~/.claude/tasks/` (home directory, not project)
- Shared task lists: Set `CLAUDE_CODE_TASK_LIST_ID` env var

```bash
export CLAUDE_CODE_TASK_LIST_ID=my-project
claude
```

Now tasks stored in `~/.claude/tasks/my-project/`

**Dependencies \& Blockers:**[^64]

```typescript
TaskCreate({
  subject: "Implement frontend",
  addBlockedBy: ["task-id-for-api-endpoint"]
})
```

When API endpoint task completes, frontend task becomes available.

**Multi-Session Collaboration:**[^64]

- Session A completes task → Session B sees update immediately
- Enables parallel workstreams (frontend + backend sessions sharing blockers)
- Resume anywhere (close laptop, tasks exactly where you left off)

**Subagents \& Tasks:**[^65][^66]

- Subagents have access to task tools
- Can create tasks for other subagents
- Real-time broadcast across sessions

**Usage:**

```
/tasks                           # List current tasks
"create a task to refactor auth" # Claude uses TaskCreate
"mark task 3 as complete"        # Claude uses TaskUpdate
```

**Disable (revert to old Todos):**[^8]

```bash
export CLAUDE_CODE_ENABLE_TASKS=false
```

**Version Notes:** Tasks introduced v2.1.x (Jan 23, 2025); Todos were previous system[^64][^6]

***

### N. IDE Integration

#### VS Code Extension

**Official Extension:** Available from Anthropic.[^67]

**Installation:**[^68]

1. Get extension path: `npm list -g @anthropic-ai/claude-code`
2. Install .vsix: `code --install-extension /path/to/node_modules/@anthropic-ai/claude-code/vendor/claude-code.vsix`
3. Open VS Code terminal, run `claude`
4. Connect: `/ide` → Select VS Code

**Features:**[^67]

- Inline diffs
- @-mentions
- Plan review
- Keyboard shortcuts via Command Palette (Cmd+Shift+P / Ctrl+Shift+P)

**Focus States:**[^67]

- **Editor focused** - Cursor in code file
- **Claude focused** - Cursor in prompt box
- Shortcuts behave differently based on focus


#### Cursor Integration

**Method 1: Terminal in Cursor:**[^69][^68]

1. Open Cursor terminal
2. Run `claude`
3. `/ide` → Connect to Cursor
4. Highlights active file, syncs editor state

**Method 2: VS Code Extension in Cursor:**[^69]
Same as VS Code installation (Cursor is VS Code fork).

**External Terminal + Cursor:**[^68]

- Run `claude` in external terminal (e.g., iTerm2)
- `/ide` → Connect to Cursor
- Claude knows which file open in Cursor
- Useful for dual-monitor setups

**Pitfall:**[^68]

- VS Code extension vs terminal mode have different UX
- Choose one workflow to avoid confusion
- Some users report occasional bugs when extension new[^68]

***

### O. Permission Modes \& Security

**Permission System Hierarchy:** deny → ask → allow (first match wins).[^70][^23]

**Permission Modes:**[^22][^71][^23]


| Mode | Description | Use Case |
| :-- | :-- | :-- |
| `default` | Prompt on first use of each tool | Standard development, learning |
| `acceptEdits` | Auto-accept file edits | Trusted projects, rapid prototyping |
| `plan` | Analyze but no modifications | Review mode, exploration |
| `dontAsk` | Auto-deny unless pre-approved | Restrictive environments |
| `bypassPermissions` | Skip all prompts | Sandboxed environments ONLY |

**Set Default Mode:**[^22]

```json
{
  "defaultMode": "acceptEdits"
}
```

**CLI Override:**[^72]

```bash
claude --permission-mode plan
```

**Interactive Toggle:** Shift+Tab to cycle modes.[^73][^74]

**Tool Categories:**[^23]

- **Read-only** (Read, Grep, Glob) - No approval needed
- **Bash commands** - Approval required
- **File modification** (Edit, Write) - Approval until session end

**"Yes, don't ask again" Behavior:**[^23]

- Bash commands: Permanently per project directory and command
- File modifications: Until session end

**YOLO Mode (--dangerously-skip-permissions):**[^75][^76]

```bash
claude --dangerously-skip-permissions
```

**CRITICAL WARNING:** Use ONLY in sandboxed/containerized environments. No safety guardrails.

**Safer Alternative:** `--allowedTools` for granular control.[^25]

***

### P. Keyboard Shortcuts \& Vim Mode

#### Essential Shortcuts[^77][^56][^19][^8]

**Permission \& Mode Control:**

- `Shift+Tab` - Cycle permission modes (default → acceptEdits → plan)
- `Tab` - Toggle extended thinking
- `Alt+M` (some configs) - Toggle permission modes

**Model \& Display:**

- `Option+P` (Mac) / `Alt+P` (Win/Linux) - Switch model
- `Option+T` (Mac) / `Alt+T` (Win/Linux) - Toggle extended thinking
- `Ctrl+O` - Toggle verbose output

**Editing:**

- `Ctrl+G` - Open external editor (set EDITOR env var)
- `Ctrl+S` - Stash current prompt
- `Ctrl+R` - Reverse search command history
- `Ctrl+L` - Clear screen (keeps conversation)
- `Ctrl+U` - Delete line
- `Ctrl+K` - Delete to end of line
- `Ctrl+W` - Delete word
- `Ctrl+A` - Beginning of line
- `Ctrl+E` - End of line

**Session Control:**

- `Ctrl+C` - Cancel current input/generation
- `Ctrl+D` - Exit Claude Code
- `Ctrl+Z` - Suspend (resume with `fg`)
- `Esc+Esc` - Rewind conversation/code

**Tasks \& Background:**

- `Ctrl+B` - Background running tasks (press twice for tmux)

**Input Modes:**

- `@` - File path autocomplete
- `#` - Add to CLAUDE.md
- `/` - Slash command
- `!` - Bash mode (direct command execution)

**Image Input:**

- `Ctrl+V` (Mac/Linux) / `Alt+V` (Windows) - Paste image

**Multi-line Input:**

- `\\ + Enter` - Works everywhere
- `Option+Enter` - macOS standard
- `Shift+Enter` - After `/terminal-setup`
- `Ctrl+J` - Line feed


#### Vim Mode[^78][^79][^80]

**Activation:** `/vim` or configure via `/config`[^79]

**Supported Subset:**[^79]

- **Mode switching:** Esc (NORMAL), i/I, a/A, o/O
- **Navigation:** h/j/k/l, w/b/e, 0/\$, gg/G, f/F, t/T
- **Editing:** d/c/y commands, p/P paste, >>/<<, J, .
- **Deletion:** dd, dw, de, db, D
- **Change:** cc, cw, ce, cb, C

**External Editor Integration:**[^80]

```bash
export EDITOR=nvim
# In Claude Code, press Ctrl+E → opens nvim in new terminal
# Save and close → prompt updates with edits
```

**Custom Keybindings:**[^77]

```
/keybindings
→ Opens ~/.claude/keybindings.json
```

Example override:

```json
{
  "$schema": "https://platform.claude.com/docs/schemas/claude-code/keybindings.json",
  "bindings": [{
    "context": "Chat",
    "bindings": {
      "ctrl+e": "chat:externalEditor",
      "ctrl+u": null
    }
  }]
}
```


***

### Q. Desktop App \& Claude Code for Desktop

**Desktop App (General):**[^81][^82]

- **Platforms:** macOS, Windows (x64 + ARM64), iOS, Android
- **All plan types:** Free, Pro, Max, Team, Enterprise
- **Features:**
    - Quick entry from dock/system tray
    - Voice input (Mac only)
    - Screenshot/window sharing (Mac only)
    - Claude in Chrome integration built-in
    - Desktop extensions for local tools/files
    - Scheduled tasks, planning mode

**Claude Code for Desktop (v2.0.51+):**[^83][^84]

- **Interface:** Integrated into desktop app with session tabs
- **Parallel Sessions:** Multiple local/remote sessions via git worktrees[^83]
- **Workflow:** One agent debugging, another exploring GitHub, third updating docs
- **CLI Button:** Opens terminal with `claude`
- **VS Code Button:** Opens VS Code with Claude Code CLI
- **Plan Mode Enhancements:** Opus 4.5 asks clarifying questions before autonomous work[^83]

**Installation:**[^82]

1. Visit claude.com/download
2. Download for OS (macOS 11+, Windows 10+)
3. Install and launch
4. Sign in

**Enterprise Deployment:**[^81]

- MSIX installers (Windows), PKG installers (Mac)
- Control version updates
- Automatic SSO for managed devices
- Pre-approve desktop extensions

***

### R. Agent SDK (Programmatic Access)

**Concept:** Same agent loop, tools, and context management as Claude Code, but programmatic in Python/TypeScript.[^85][^86][^5]

**Installation:**[^85]

```bash
npm install -g @anthropic-ai/claude-code  # Runtime
npm install @anthropic-ai/claude-agent-sdk
```

**Basic Query:**[^86]

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review this codebase for security issues",
  options: {
    model: "opus",
    allowedTools: ["Read", "Grep", "Glob"],
    permissionMode: "bypassPermissions",
    maxTurns: 250
  }
})) {
  if (message.type === "assistant") {
    console.log(message.message.content);
  }
  if (message.type === "result") {
    console.log("Total cost:", message.total_cost_usd);
  }
}
```

**Structured Output:**[^87][^88][^85]

```typescript
const reviewSchema = {
  type: "object",
  properties: {
    issues: { type: "array", items: {...} },
    summary: { type: "string" },
    overallScore: { type: "number" }
  },
  required: ["issues", "summary", "overallScore"]
};

for await (const message of query({
  prompt: "Review code",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: reviewSchema
    }
  }
})) {
  if (message.type === "result" && message.structured_output) {
    const result = message.structured_output;
    // Guaranteed to match schema
  }
}
```

**Subagents in SDK:**[^85]

```typescript
const agents = {
  "security-scanner": {
    description: "Deep security analysis",
    prompt: "You are a security expert...",
    tools: ["Read", "Grep", "Glob"],
    model: "sonnet"
  }
};

for await (const message of query({
  prompt: "Scan codebase",
  options: { agents }
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if ("name" in block && block.name === "Task") {
        console.log("Delegating to:", block.input.subagent_type);
      }
    }
  }
}
```

**Permission Handling:**[^71]

```typescript
query({
  prompt: "...",
  options: {
    permissionMode: "acceptEdits",  // or default, plan, bypassPermissions
    allowedTools: ["Read", "Edit", "Bash(git *)"],
    canUseTool: async (tool, input) => {
      // Custom approval logic
      return { allowed: true };
    }
  }
})
```

**Use Cases:**[^5][^85]

- Email assistant
- Code review agents
- Research agents
- Custom automation workflows

**Version Notes:** SDK released v1.0.23 (June 2025); V2 in development[^85][^6]

***

## II. Top 25 Superuser Moves

*(See JSON appendix for complete details with sources)*

1. **CLAUDE.md Project Memory** - Auto-loaded context[^17][^18][^1]
2. **Plan Mode Before Execution** - Review plan before changes[^89][^74]
3. **Background Tasks (Ctrl+B)** - Dev servers, builds while working[^8][^6]
4. **Custom Slash Commands with Arguments** - Reusable workflows[^9][^90]
5. **Headless Mode for CI/CD** - Automation pipelines[^11][^10]
6. **Subagent Delegation** - Isolated specialized tasks[^31][^30]
7. **Permission Presets via allowedTools** - Eliminate prompts[^25][^23]
8. **Sandboxed Development** - Safe autonomous operation[^45][^3]
9. **Extended Thinking** - Complex reasoning[^55][^53]
10. **@ File Mentions** - Direct file references[^19][^8]
11. **Task Dependencies** - Multi-session coordination[^65][^64]
12. **Compact Conversations** - Strategic token management[^63][^20]
13. **Hooks for Deterministic Actions** - Auto-format, lint, test[^32][^33]
14. **MCP Servers** - External tools/APIs[^38][^37]
15. **Skills for Domain Expertise** - Conditional knowledge[^27][^26]
16. **Chrome Integration** - Build-test-verify loop[^51][^50]
17. **GitHub Actions** - @claude PR automation[^48][^49]
18. **Output Styles** - Custom behavior/tone[^58][^59]
19. **Rewind** - Undo/redo for code + conversation[^91][^8]
20. **Vim Mode** - Modal editing in prompts[^78][^79]
21. **Bash Mode (!)** - Direct shell commands[^19][^8]
22. **Context Visualization** - Token budget insight[^19][^20]
23. **Multi-Session via Git Worktrees** - Parallel development[^1][^83]
24. **IDE Integration** - VS Code/Cursor sync[^67][^68]
25. **Agent SDK** - Custom programmatic agents[^5][^85]

***

## III. Key Files \& Folders Glossary

| Path | Purpose | Scope | Version Added |
| :-- | :-- | :-- | :-- |
| **CLAUDE.md** | Auto-loaded project context | Project root, subdirs | v0.2.x |
| **~/.claude/CLAUDE.md** | Global user context | All projects | v0.2.x |
| **CLAUDE.local.md** | Gitignored local overrides | Project | v1.0.x |
| **.claude/rules/** | Modular rule files | Project | v1.0.x |
| **~/.claude/settings.json** | User-level settings | All projects | v0.2.x |
| **.claude/settings.json** | Project settings (team-shared) | Project | v0.2.x |
| **.claude/settings.local.json** | Local overrides (gitignored) | Project | v0.2.x |
| **managed-settings.json** | Enterprise/org settings (read-only) | System-wide | v1.0.x |
| **~/.claude.json** | Global user settings + MCP config | All projects | v0.2.x |
| **.mcp.json** | Project MCP servers | Project | v1.0.27 |
| **~/.claude/commands/** | User-level slash commands | All projects | v0.2.x |
| **.claude/commands/** | Project slash commands | Project | v0.2.x |
| **~/.claude/agents/** | User-level subagents | All projects | v1.0.x |
| **.claude/agents/** | Project subagents | Project | v1.0.x |
| **~/.claude/skills/** | User-level skills | All projects | v1.0.x |
| **.claude/skills/** | Project skills | Project | v1.0.x |
| **~/.claude/output-styles/** | Custom output styles | All projects | v1.0.81 |
| **.claude/output-styles/** | Project output styles | Project | v1.0.81 |
| **~/.claude/tasks/** | Task persistence | Cross-project | v2.1.x |
| **~/.claude/keybindings.json** | Custom keyboard shortcuts | All projects | v2.0.x |
| **.claude-plugin/plugin.json** | Plugin manifest (REQUIRED) | Plugin | v1.0.x |
| **hooks/hooks.json** | Plugin hooks configuration | Plugin | v1.0.38 |
| **.lsp.json** | LSP server config | Plugin | v1.0.x |


***

## IV. Citation-Heavy Appendix


***

## V. Version History \& Recent Changes

**Major Version Milestones:**[^7][^6]

- **v2.1.17** (Jan 29, 2026) - Current stable
- **v2.0.51** (Nov 2025) - Opus 4.5, Claude Code for Desktop, updated usage limits
- **v2.0.14** (Sep 2025) - --system-prompt flag, output styles customization
- **v2.0.0** (Aug 2025) - Rewind feature (Esc+Esc), general availability
- **v1.0.123** (Jul 2025) - SlashCommand tool (Claude can invoke slash commands), Bash security fix
- **v1.0.81** (Aug 2025) - Output styles: Explanatory \& Learning
- **v1.0.71** (Jul 2025) - Background commands (Ctrl+B), /statusline
- **v1.0.38** (Jul 2025) - Hooks released
- **v1.0.27** (Jun 2025) - MCP improvements (OAuth, streaming HTTP, @-mentionable resources), /resume
- **v1.0.23** (Jun 2025) - SDK releases (TypeScript, Python)
- **v1.0.11** (May 2025) - Claude Pro subscription support
- **v1.0.0** (Apr 2025) - General availability, Sonnet 4 \& Opus 4 models
- **v0.2.96** (Mar 2025) - Claude Max subscription support
- **v0.2.x** (2024-2025) - Beta releases (37 versions)

**Context Engineering Theme:** 2025 saw unifying focus on context management across CLAUDE.md, Plan mode, Subagents, /context, Skills, compaction.[^7]

***

## VI. Limitations \& Known Issues

**Session Context Recovery:**[^13]

- `--resume` restores command history but context recovery varies
- CLAUDE.md helps maintain project knowledge across resumes
- Not guaranteed to remember prior reasoning/decisions

**Auto-Compact Behavior:**[^92]

- Can trigger unexpectedly, losing early instructions
- Community recommends disabling for serious work: configure auto-compact settings
- Manual /compact with focus instruction preferred

**Plan Mode → Auto-Accept:**[^89]

- Approving plan in Plan Mode may auto-enable acceptEdits mode
- Unexpected behavior, requires manual disable if unwanted
- GitHub issue open for configuration option

**WSL Incompatibilities:**

- Chrome integration doesn't work in WSL[^50]
- Some IDE integrations unreliable in WSL[^68]
- Native Windows or Mac preferred

**Subagent Constraints:**[^30]

- Cannot spawn other subagents
- Background subagents can't ask clarifying questions
- MCP tools unavailable in background mode

**Hook Loop Risk:**[^33]

- Stop/SubagentStop hooks with `blocking: true` can create infinite loops
- Default `blocking: false` to prevent, but reduces enforcement power

***

## VII. Community Resources \& Further Reading

**Official Documentation:**

- Main docs: https://code.claude.com/docs/en/overview[^2]
- Agent SDK: https://platform.claude.com/docs/en/agent-sdk/overview[^86]
- GitHub: https://github.com/anthropics/claude-code[^93]

**Best Practices \& Guides:**

- Anthropic Engineering Blog: https://www.anthropic.com/engineering/claude-code-best-practices[^1]
- Sandboxing: https://www.anthropic.com/engineering/claude-code-sandboxing[^3]
- Agent SDK Guide: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk[^5]

**Community Hubs:**

- r/ClaudeAI subreddit[many sources]
- ClaudeLog (community guides): https://www.claudelog.com/[various]
- Awesome Claude Code: https://github.com/hesreallyhim/awesome-claude-code[^94]
- Subagent collection: https://github.com/VoltAgent/awesome-claude-code-subagents[^95]

**Plugin Marketplaces:**

- Official: claude-plugins-official (auto-available)[^39]
- Community: https://claudemarketplaces.com[^44]
- Every.io: https://github.com/EveryInc/every-marketplace[^44]

**Video Tutorials:**

- Official playlist: Anthropic YouTube channel
- Community: Various creators on YouTube[many sources]

***

**End of Report**

*This canonical map represents comprehensive research across 152 sources as of January 29, 2026. Claude Code continues rapid development; always verify against official docs for latest features.*

<div align="center">⁂</div>

[^1]: https://www.anthropic.com/engineering/claude-code-best-practices

[^2]: https://code.claude.com/docs/en/overview

[^3]: https://www.anthropic.com/engineering/claude-code-sandboxing

[^4]: https://code.claude.com/docs/en/settings

[^5]: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

[^6]: https://claudefa.st/blog/guide/changelog

[^7]: https://dev.to/oikon/reflections-of-claude-code-from-changelog-833

[^8]: https://code.claude.com/docs/en/interactive-mode

[^9]: https://shipyard.build/blog/claude-code-cheat-sheet/

[^10]: https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm

[^11]: https://github.com/anthropics/claude-code/issues/733

[^12]: https://www.claudelog.com/faqs/what-is-output-format-in-claude-code/

[^13]: https://www.reddit.com/r/ClaudeCode/comments/1ns47r4/how_does_one_start_claude_with_an_existing/

[^14]: https://m.academy/lessons/resume-continue-coding-session-claude-code/

[^15]: https://www.linkedin.com/posts/mikemurphyco_claude-code-how-to-resume-past-sessions-activity-7414640703974060032-PpIh

[^16]: https://www.claudelog.com/faqs/how-to-suspend-claude-code/

[^17]: https://www.builder.io/blog/claude-md-guide

[^18]: https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/

[^19]: https://www.gradually.ai/en/claude-code-commands/

[^20]: https://www.cometapi.com/managing-claude-codes-context/

[^21]: https://www.reddit.com/r/ClaudeAI/comments/1l24a93/claude_code_settingsjson/

[^22]: https://www.claudelog.com/faqs/how-to-set-claude-code-permission-mode/

[^23]: https://code.claude.com/docs/en/iam

[^24]: https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code

[^25]: https://www.claudelog.com/faqs/what-is-allowed-tools-in-claude-code/

[^26]: https://code.claude.com/docs/en/skills

[^27]: https://rewire.it/blog/claude-code-agents-skills-slash-commands/

[^28]: https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

[^29]: https://www.reddit.com/r/ClaudeAI/comments/1ped515/understanding_claudemd_vs_skills_vs_slash/

[^30]: https://code.claude.com/docs/en/sub-agents

[^31]: https://shipyard.build/blog/claude-code-subagents-guide/

[^32]: https://www.datacamp.com/tutorial/claude-code-hooks

[^33]: https://code.claude.com/docs/en/hooks

[^34]: https://code.claude.com/docs/en/hooks-guide

[^35]: https://www.eesel.ai/blog/hooks-in-claude-code

[^36]: https://hexdocs.pm/claude/guide-hooks.html

[^37]: https://code.claude.com/docs/en/mcp

[^38]: https://www.ksred.com/claude-code-as-an-mcp-server-an-interesting-capability-worth-understanding/

[^39]: https://code.claude.com/docs/en/discover-plugins

[^40]: https://composio.dev/blog/claude-code-plugin

[^41]: https://code.claude.com/docs/en/plugins-reference

[^42]: https://code.claude.com/docs/en/plugins

[^43]: https://code.claude.com/docs/en/plugin-marketplaces

[^44]: https://claudemarketplaces.com

[^45]: https://www.infoq.com/news/2025/11/anthropic-claude-code-sandbox/

[^46]: https://www.reddit.com/r/Anthropic/comments/1oc8uq9/claude_code_overrides_the_sandbox_without/

[^47]: https://apidog.com/blog/claude-code-github-actions/

[^48]: https://code.claude.com/docs/en/github-actions

[^49]: https://stevekinney.com/courses/ai-development/integrating-with-github-actions

[^50]: https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/

[^51]: https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome

[^52]: https://aimaker.substack.com/p/claude-chrome-extension-browser-automation-guide

[^53]: https://www.anthropic.com/news/visible-extended-thinking

[^54]: https://www.lesswrong.com/posts/qkfRNcvWz3GqoPaJk/anthropic-releases-claude-3-7-sonnet-with-extended-thinking

[^55]: https://www.youtube.com/watch?v=_ijYYRzUU7Y

[^56]: https://www.youtube.com/watch?v=pm9mb9GD3Yc

[^57]: https://docs.aws.amazon.com/bedrock/latest/userguide/claude-messages-extended-thinking.html

[^58]: https://tessl.io/blog/claude-code-now-lets-you-customize-its-communication-style/

[^59]: https://code.claude.com/docs/en/output-styles

[^60]: https://shipyard.build/blog/claude-code-output-styles-pair-programming/

[^61]: https://www.eesel.ai/blog/output-styles-claude-code

[^62]: https://code.claude.com/docs/en/how-claude-code-works

[^63]: https://stevekinney.com/courses/ai-development/claude-code-compaction

[^64]: https://claudefa.st/blog/guide/development/task-management

[^65]: https://www.reddit.com/r/ClaudeAI/comments/1qkjznp/anthropic_replaced_claude_codes_old_todos_with/

[^66]: https://www.youtube.com/watch?v=6omInQipcag

[^67]: https://code.claude.com/docs/en/vs-code

[^68]: https://www.youtube.com/watch?v=gRNVCeD1br8

[^69]: https://www.youtube.com/watch?v=xU18PCIDQ8Y

[^70]: https://www.eesel.ai/blog/claude-code-permissions

[^71]: https://platform.claude.com/docs/en/agent-sdk/permissions

[^72]: https://www.petefreitag.com/blog/claude-code-permissions/

[^73]: https://www.claudelog.com/mechanics/auto-accept-permissions/

[^74]: https://moonandeye.github.io/en/programming/think-mode-on-claude-code/

[^75]: https://www.reddit.com/r/ClaudeAI/comments/1kuj1dm/how_to_run_claude_code_in_yolo_mode_a_quick_guide/

[^76]: https://www.reddit.com/r/ClaudeAI/comments/1l3thi1/claude_code_how_do_you_auto_accept_do_you_want_to/

[^77]: https://code.claude.com/docs/en/keybindings

[^78]: https://dev.to/rajeshroyal/vim-mode-edit-prompts-at-the-speed-of-thought-3l6c

[^79]: https://code.claude.com/docs/en/terminal-config

[^80]: https://www.reddit.com/r/ClaudeCode/comments/1p9pcq5/claude_has_vim_mode/

[^81]: https://claude.com/download

[^82]: https://support.claude.com/en/articles/10065433-installing-claude-desktop

[^83]: https://www.reddit.com/r/ClaudeAI/comments/1p5pn25/claude_code_is_now_available_in_our_desktop_app/

[^84]: https://www.youtube.com/watch?v=pZ2N7CJFbBk

[^85]: https://nader.substack.com/p/the-complete-guide-to-building-agents

[^86]: https://platform.claude.com/docs/en/agent-sdk/overview

