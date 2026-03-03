# Agents SDK Integration Guide

> How the Claude Agent SDK extends the Superuser Pack from an interactive toolkit into an autonomous second brain.

**Version:** 3.9.0
**Last Updated:** 2026-02-22
**Prerequisites:** Python 3.10+, Claude Code CLI (`claude login` completed)

---

## Table of Contents

1. [What Is the Agents SDK Layer?](#what-is-the-agents-sdk-layer)
2. [Architecture: Interactive vs Autonomous](#architecture-interactive-vs-autonomous)
3. [How It Works With the Superuser Pack](#how-it-works-with-the-superuser-pack)
4. [Directory Structure](#directory-structure)
5. [Core Modules Reference](#core-modules-reference)
6. [The Daily Driver Agent](#the-daily-driver-agent)
7. [Scheduling with launchd](#scheduling-with-launchd)
8. [Safety and Observability](#safety-and-observability)
9. [How Skills, Hooks, and Agents Relate](#how-skills-hooks-and-agents-relate)
10. [Usage Guide](#usage-guide)
11. [Expanding the System](#expanding-the-system)
12. [Tools, APIs, and MCPs to Connect](#tools-apis-and-mcps-to-connect)
13. [Troubleshooting](#troubleshooting)

---

## What Is the Agents SDK Layer?

The Claude Agent SDK (`claude-agent-sdk` Python package) spawns Claude Code CLI as a subprocess, giving you programmatic control over Claude from Python scripts. This means you can build agents that run **without you being present** — on schedules, in response to events, or as part of automated pipelines.

Before this integration, the Superuser Pack was purely **interactive**: you opened Claude Code, typed commands, and skills/hooks/agents activated during your session. Now there are two layers:

| Layer | Trigger | Human Present? | Runtime |
|-------|---------|----------------|---------|
| **Interactive** (Claude Code) | You type | Yes | CLI session |
| **Autonomous** (Agent SDK) | Schedule or event | No | Python script |

Both layers share the same vault, the same skills, and the same hooks. The Agent SDK doesn't replace anything — it adds a new execution mode.

---

## Architecture: Interactive vs Autonomous

```
INTERACTIVE (human-in-the-loop)              AUTONOMOUS (scheduled)
───────────────────────────────              ─────────────────────
Claude Code CLI                              Agent SDK Python scripts
  .claude/skills/  (auto-loaded)               agents-sdk/agents/*.py
  .claude/agents/  (subagents)                 agents-sdk/lib/ (shared utils)
  .claude/hooks/   (lifecycle)                 agents-sdk/schedules/*.plist
                                               agents-sdk/config.toml
```

### What They Share

- **Vault** (`vault/`) — Both read and write to the same Obsidian vault. Interactive sessions create notes; autonomous agents update them at anchors.
- **Skills** (`.claude/skills/`) — SDK agents load SKILL.md files as system prompts. When you improve a skill, the improvement flows to autonomous agents automatically.
- **Hooks** (`.claude/settings.json`) — SDK agents inherit hooks via `setting_sources=["project"]`. The `block-secrets.py` hook prevents agents from modifying `.env` files.
- **Secrets** (`.env`) — Both use the same environment variables when needed.

### What's Different

- **Interactive agents** (`.claude/agents/`) are subagents spawned within a Claude Code session. They have a human watching.
- **Autonomous agents** (`agents-sdk/agents/`) are Python scripts that call the SDK's `query()` function. No human is present, so they must make decisions autonomously.

### The Key Insight: Skills Are Prompts, Agents Are Runners

A skill is a prompt document (SKILL.md). It tells Claude **what to do and how to do it**. An agent is a runner — it decides **when** to execute, loads the appropriate skills as system prompts, and manages the lifecycle (logging, error handling, cost tracking).

This separation means:
- You never duplicate skill content between interactive and autonomous modes
- Skill improvements are automatically inherited by all agents
- You can mix and match skills per agent freely via `config.toml`

---

## How It Works With the Superuser Pack

### Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                        macOS launchd                            │
│  Triggers daily_driver.py at 6am, 5pm, Friday 4pm              │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  agents-sdk/agents/daily_driver.py                              │
│                                                                  │
│  1. load_config()  ─── reads config.toml + .env                 │
│  2. load_skills()  ─── reads .claude/skills/daily-driver/       │
│                        reads .claude/skills/vault-read-write/   │
│  3. build prompt   ─── combines preamble + skill content        │
│                        + mode-specific task instructions         │
│  4. query()        ─── spawns Claude Code CLI as subprocess     │
│  5. record_run()   ─── appends to agent-run-history.csv         │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  Claude Code CLI (spawned by SDK)                               │
│                                                                  │
│  - System prompt: "claude_code" preset + skill prompts          │
│  - Allowed tools: Read, Write, Edit, Glob, Grep, vault_inject  │
│  - Hooks: block-secrets.py (inherited via setting_sources)      │
│  - CWD: repo root                                               │
│                                                                  │
│  Reads/writes vault files autonomously                          │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  Obsidian Vault                                                  │
│                                                                  │
│  vault/10_timeline/daily/2026-02-22.md   ← created/updated      │
│  vault/10_timeline/weekly/2026-W08.md    ← weekly review         │
│  vault/90_system/agent-logs/             ← run logs              │
│  vault/90_system/agent-logs/agent-run-history.csv                │
└──────────────────────────────────────────────────────────────────┘
```

### Anchor-Based Writes

The vault daily note template uses HTML comment anchors:
```markdown
<!-- jira-log -->
<!-- claude-sessions -->
<!-- side-projects -->
```

SDK agents use the `vault_inject` MCP tool to append content below these anchors without replacing existing content. This is a PATCH operation — multiple agents and interactive sessions can write to the same note without conflicts.

---

## Directory Structure

```
agents-sdk/
├── pyproject.toml              # Python project: deps, entry points, pytest config
├── config.toml                 # Central config: paths, agent settings, safety limits
├── .env.example                # Template (API key is optional)
│
├── lib/                        # Shared library modules
│   ├── __init__.py
│   ├── config.py               # Load config.toml + .env → Config dataclass
│   ├── skill_loader.py         # Read SKILL.md files → system prompt strings
│   ├── vault_io.py             # Vault path conventions, anchor injection, templates
│   ├── logging_setup.py        # Per-run log files + CSV run history
│   └── custom_tools.py         # MCP tool definitions (vault_inject)
│
├── agents/                     # Agent implementations
│   ├── __init__.py
│   └── daily_driver.py         # Morning planning, EOD review, weekly review
│
├── schedules/                  # macOS launchd job definitions
│   ├── com.sean.agent.daily-morning.plist    # 6:00 AM daily
│   ├── com.sean.agent.daily-evening.plist    # 5:00 PM daily
│   ├── com.sean.agent.weekly-review.plist    # Friday 4:00 PM
│   └── install_schedules.sh                  # Install/remove launchd jobs
│
└── tests/                      # pytest test suite (33 tests)
    ├── __init__.py
    ├── conftest.py             # Shared fixtures (tmp_vault, tmp_skills, tmp_config)
    ├── test_config.py          # Config loading tests
    ├── test_skill_loader.py    # Skill prompt loading tests
    ├── test_vault_io.py        # Vault I/O tests
    └── test_logging_setup.py   # Logging tests
```

---

## Core Modules Reference

### `lib/config.py` — Configuration

Loads `config.toml` and `.env`, returns a typed `Config` dataclass.

**Key classes:**

| Class | Fields | Purpose |
|-------|--------|---------|
| `Config` | `repo_root`, `vault_root`, `skills_dir`, `life_systems_scripts`, `log_dir`, `log_level`, `safety`, `agents`, `anthropic_api_key` | Top-level config |
| `SafetyConfig` | `max_turns_default` (30), `max_budget_default` ($0.50), `permission_mode` ("acceptEdits") | Global safety limits |
| `AgentConfig` | `enabled`, `skills`, `max_turns`, `max_budget_usd` | Per-agent settings |

**Key function:**

```python
config = load_config()                          # Uses default paths
config = load_config(config_path=Path("..."))   # Custom config file

daily_cfg = config.agent_config("daily_driver") # Returns AgentConfig
daily_cfg.enabled    # True
daily_cfg.skills     # ["daily-driver", "vault-read-write"]
```

**Authentication:** The `anthropic_api_key` field is `str | None`. When `None`, the SDK uses Claude Code CLI's existing OAuth auth from `claude login`. You don't need an API key if you're logged into Claude Code.

### `lib/skill_loader.py` — Skill-to-Prompt Bridge

Reads `.claude/skills/<name>/SKILL.md`, strips YAML frontmatter, returns the markdown body as a system prompt string.

```python
# Load a single skill
prompt = load_skill_prompt("daily-driver", config.skills_dir)

# Load multiple skills (concatenated with headers)
prompt = load_skills(["daily-driver", "vault-read-write"], config.skills_dir)
# Returns:
# ## Skill: daily-driver
# [daily-driver SKILL.md content]
#
# ---
#
# ## Skill: vault-read-write
# [vault-read-write SKILL.md content]
```

### `lib/vault_io.py` — Vault Operations

Provides typed helpers for Obsidian vault file I/O.

**Path conventions:**

| Function | Returns | Example |
|----------|---------|---------|
| `daily_note_path(vault_root)` | Today's daily note | `vault/10_timeline/daily/2026-02-22.md` |
| `daily_note_path(vault_root, date)` | Specific date's note | `vault/10_timeline/daily/2026-02-21.md` |
| `weekly_note_path(vault_root)` | This week's review | `vault/10_timeline/weekly/2026-W08.md` |
| `yesterday_note_path(vault_root)` | Yesterday's note | `vault/10_timeline/daily/2026-02-21.md` |
| `recent_daily_notes(vault_root, 7)` | Last 7 existing notes | `[Path(...), ...]` (most recent first) |

**Core operations:**

| Function | Purpose |
|----------|---------|
| `inject_at_anchor(path, anchor, content)` | Append content below `<!-- anchor -->` comment |
| `read_frontmatter(path)` | Extract YAML frontmatter as dict |
| `create_from_template(template, dest, subs)` | Create note from template with substitutions |

### `lib/logging_setup.py` — Observability

**Per-run log files:**
```
vault/90_system/agent-logs/daily-driver-2026-02-22-morning.log
vault/90_system/agent-logs/daily-driver-2026-02-22-evening.log
vault/90_system/agent-logs/daily-driver-2026-02-22-weekly.log
```

**Run history CSV:**
```
vault/90_system/agent-logs/agent-run-history.csv
```

Columns: `date`, `time`, `agent`, `mode`, `status`, `cost_usd`, `duration_ms`, `turns`, `notes`

### `lib/custom_tools.py` — MCP Tools

Defines custom MCP tools that agents can call during execution.

**Current tools:**

| Tool | MCP Name | Purpose |
|------|----------|---------|
| `vault_inject` | `mcp__vault-tools__vault_inject` | PATCH content below an HTML anchor in a vault file |

**Usage in agents:**
```python
from lib.custom_tools import create_vault_mcp_server

vault_server = create_vault_mcp_server()
options = ClaudeAgentOptions(
    mcp_servers={"vault-tools": vault_server},
    allowed_tools=[..., "mcp__vault-tools__vault_inject"],
)
```

---

## The Daily Driver Agent

The first implemented agent. Runs three protocols from the `daily-driver` skill:

### Morning Mode (6:00 AM)

1. Read yesterday's daily note — extract carry-forwards and open loops
2. Read referenced project notes from `vault/20_projects/`
3. Create today's daily note from `tpl-daily.md` template
4. Write 1-3-5 priority plan (1 big thing, 3 medium, 5 small)

### Evening Mode (5:00 PM)

1. Read today's daily note — review morning plan and session entries
2. Summarize progress against planned tasks
3. Write Evening Reflection: Win, Lesson, Carry Forward

### Weekly Mode (Friday 4:00 PM)

1. Read last 7 daily notes
2. Aggregate: tasks completed, decisions made, open loops, patterns
3. Create weekly review note at `vault/10_timeline/weekly/`

### Running Manually

```bash
cd agents-sdk

# Dry run (prints prompt without calling API — free)
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run

# Live run
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode evening
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode weekly
```

### System Prompt Construction

The agent builds its system prompt from three layers:

1. **Preset base:** `{"type": "preset", "preset": "claude_code"}` — gives Claude all standard CLI capabilities
2. **Skill prompts:** Loaded from `.claude/skills/daily-driver/SKILL.md` and `.claude/skills/vault-read-write/SKILL.md`
3. **Autonomous preamble:** "No human is present. Make best-judgment decisions. Write to vault files, not stdout."

---

## Scheduling with launchd

### How It Works

macOS `launchd` is the native job scheduler (like cron but better). Each `.plist` file in `schedules/` defines a job:

| File | Schedule | Agent Mode |
|------|----------|------------|
| `com.sean.agent.daily-morning.plist` | Every day 6:00 AM | `--mode morning` |
| `com.sean.agent.daily-evening.plist` | Every day 5:00 PM | `--mode evening` |
| `com.sean.agent.weekly-review.plist` | Friday 4:00 PM | `--mode weekly` |

### Installing Schedules

```bash
# Install all schedules
./agents-sdk/schedules/install_schedules.sh

# List available schedules
./agents-sdk/schedules/install_schedules.sh --list

# Remove all schedules
./agents-sdk/schedules/install_schedules.sh --remove

# Verify installation
launchctl list | grep com.sean.agent
```

### How Plists Work

Each plist specifies:
- **Program:** The venv Python path
- **Arguments:** The agent script + `--mode` flag
- **WorkingDirectory:** The repo root
- **StartCalendarInterval:** When to run (Hour, Minute, optionally Weekday)
- **StandardOutPath / StandardErrorPath:** Log file locations in `vault/90_system/agent-logs/`

### Customizing Schedules

Edit `config.toml` to change times (for your own reference), then edit the corresponding `.plist` to match:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>7</integer>    <!-- Change from 6 to 7 -->
    <key>Minute</key>
    <integer>30</integer>   <!-- Change from 0 to 30 -->
</dict>
```

After editing, reinstall: `./agents-sdk/schedules/install_schedules.sh`

---

## Safety and Observability

### Safety Mechanisms

| Mechanism | What It Does |
|-----------|--------------|
| `max_turns` | Caps conversation turns per run (default: 30) |
| `max_budget_usd` | Caps API spend per run (default: $0.50) |
| `permission_mode: "acceptEdits"` | Auto-approves file edits (required for autonomous operation) |
| `setting_sources: ["project"]` | Inherits `block-secrets.py` hook — prevents `.env` modification |
| `allowed_tools` | Whitelist of tools the agent can use (no Bash by default) |
| `--dry-run` flag | Test prompt construction without API calls |

### Observability

| What | Where |
|------|-------|
| Per-run logs | `vault/90_system/agent-logs/{agent}-{date}-{mode}.log` |
| Run history | `vault/90_system/agent-logs/agent-run-history.csv` |
| launchd stdout | `vault/90_system/agent-logs/{mode}-stdout.log` |
| launchd stderr | `vault/90_system/agent-logs/{mode}-stderr.log` |

### Cost Monitoring

Every run records its cost in `agent-run-history.csv`. You can track spending over time:

```bash
# View recent runs
cat vault/90_system/agent-logs/agent-run-history.csv | column -t -s,

# Sum costs this month
awk -F, 'NR>1 && $1~/2026-02/ {sum+=$6} END {printf "$%.4f\n", sum}' \
  vault/90_system/agent-logs/agent-run-history.csv
```

---

## How Skills, Hooks, and Agents Relate

### Skills → Agent Prompts

Skills are loaded as system prompts via `lib/skill_loader.py`. The mapping is defined in `config.toml`:

```toml
[agents.daily_driver]
skills = ["daily-driver", "vault-read-write"]

[agents.spending_analysis]
skills = ["subscription-audit", "vault-read-write"]
```

When a skill is updated (e.g., you refine the daily-driver protocol), every autonomous agent using that skill automatically gets the update on its next run.

### Hooks → Agent Guardrails

SDK agents inherit hooks from `.claude/settings.json` via `setting_sources=["project"]`. This means:

- `block-secrets.py` (PreToolUse) — prevents agents from reading or modifying `.env`, credentials, API keys
- `log-tool-use` (PostToolUse) — logs every tool call the agent makes
- `network-access-control` (PreToolUse Bash) — blocks unauthorized network access

If you add a new hook to `settings.json`, autonomous agents inherit it immediately.

### Interactive Agents vs SDK Agents

| Feature | Interactive (`.claude/agents/`) | Autonomous (`agents-sdk/agents/`) |
|---------|------|------|
| Trigger | User spawns via Task tool | Schedule or CLI |
| Human present | Yes | No |
| Decision making | Can ask user | Must decide autonomously |
| Tool access | Full Claude Code tools | Restricted whitelist |
| Cost control | User monitors | `max_budget_usd` cap |
| Logging | Session transcript | Dedicated log files + CSV |

### Can Interactive Agents Call SDK Agents?

Not directly. They serve different purposes:
- Interactive agents are subagents within a Claude Code session
- SDK agents are standalone Python scripts

However, you could trigger an SDK agent from a hook. For example, the `preserve-session` agent (planned for Phase 3) will run as a Stop hook — when your Claude Code session ends, it captures decisions and updates the vault.

---

## Usage Guide

### Initial Setup

```bash
# 1. Navigate to agents-sdk
cd agents-sdk

# 2. Create virtual environment (Python 3.10+ required)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Run tests to verify
PYTHONPATH=. pytest tests/ -v

# 5. Ensure Claude Code CLI auth is set up
claude login
```

### First Run (Dry Run)

Always test with `--dry-run` first:

```bash
cd agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run
```

This prints the full prompt and configuration without calling the API. Verify:
- Skills are loaded correctly
- Vault paths are correct
- Allowed tools look right
- Cost and turn limits are set

### First Live Run

```bash
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning
```

Check the output:
- `vault/10_timeline/daily/` for the created note
- `vault/90_system/agent-logs/` for the run log
- `vault/90_system/agent-logs/agent-run-history.csv` for cost tracking

### Setting Up Schedules

Once you're confident the agent works:

```bash
./agents-sdk/schedules/install_schedules.sh
launchctl list | grep com.sean.agent
```

### Running Tests

```bash
cd agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -v
```

All 33 tests should pass.

---

## Expanding the System

### Adding a New Agent

1. **Create the agent file** at `agents-sdk/agents/your_agent.py`
2. **Add config** in `config.toml`:
   ```toml
   [agents.your_agent]
   enabled = true
   skills = ["skill-a", "skill-b"]
   max_turns = 20
   max_budget_usd = 0.25
   ```
3. **Follow the daily_driver pattern:**
   - `build_preamble()` — autonomous context
   - `build_prompt()` — task-specific instructions
   - `build_options()` — SDK configuration
   - `async run()` — execution with logging
   - `main()` — CLI argument parsing
4. **Add a launchd plist** if scheduled
5. **Add tests** in `tests/`

### Planned Agents (from the roadmap)

| Agent | Skills | Trigger | Status |
|-------|--------|---------|--------|
| **Daily Driver** | daily-driver, vault-read-write | launchd (6am, 5pm, Fri 4pm) | Implemented |
| **Preserve Session** | preserve-session, vault-read-write | Stop hook | Phase 3 |
| **Spending Analysis** | subscription-audit, vault-read-write | launchd (Sunday 9am) | Phase 2 |
| **Process Inbox** | process-inbox, vault-read-write | launchd (8am) | Phase 3 |
| **Health Audit** | health-habits, vault-read-write | launchd (7pm) | Phase 4 |
| **MD to Anki** | vault-read-write | launchd (daily) | Phase 4 |

### Adding Custom MCP Tools

To give agents capabilities beyond file I/O:

1. **Define the tool** in `lib/custom_tools.py`:
   ```python
   @tool("tool_name", "Description of what it does",
         {"param1": str, "param2": int})
   async def your_tool(args):
       result = do_something(args["param1"], args["param2"])
       return {"content": [{"type": "text", "text": str(result)}]}
   ```

2. **Register it** in the MCP server creation function

3. **Allow it** in the agent's `allowed_tools` list:
   ```python
   allowed_tools=[..., "mcp__vault-tools__tool_name"]
   ```

### Adding New Skills for Agents

Create a new skill at `.claude/skills/your-skill/SKILL.md` with clear, autonomous-friendly instructions. Then reference it in `config.toml`:

```toml
[agents.your_agent]
skills = ["your-skill", "vault-read-write"]
```

Tips for autonomous-friendly skills:
- Include explicit decision criteria (don't say "ask the user")
- Provide fallback behavior for missing data
- Specify output formats precisely
- Include anchor names for vault injection points

---

## Tools, APIs, and MCPs — Current State

> **Updated 2026-02-28.** Most high-priority integrations are now connected via native MCPs, replacing earlier Zapier-dependent recommendations.

### Connected and Ready (Native MCPs)

| # | Service | MCP Server | Status | Key Tools |
|---|---------|-----------|--------|-----------|
| 1 | **Jira + Confluence** | `mcp-atlassian` (local) | Connected | `jira_search`, `jira_create_issue`, `jira_transition_issue`, `confluence_search`, `confluence_create_page` |
| 2 | **Jira + Confluence** | `claude.ai Atlassian` (cloud) | Connected | Read-heavy operations, quick lookups |
| 3 | **Google Calendar** | `claude.ai Google Calendar` | Connected | `gcal_list_events`, `gcal_find_my_free_time`, `gcal_create_event` |
| 4 | **Google Workspace** | `google-workspace` (local) | Connected | Calendar, Gmail, Drive, Docs, Sheets, Chat, Forms, Slides, Tasks, Contacts |
| 5 | **Gmail** | `claude.ai Gmail` | Connected | `gmail_search_messages`, `gmail_read_message`, `gmail_create_draft` |
| 6 | **GitHub** | `github` (Docker MCP) | Connected | `search_issues`, `list_pull_requests`, `create_pull_request`, `search_code` |
| 7 | **Obsidian Vault** | `obsidian-vault` | Connected | `search_notes`, `read_note`, `write_note`, `list_directory` |
| 8 | **NotebookLM** | `notebooklm-mcp` | Connected | `notebook_query`, `source_add`, `studio_create` (audio/video) |
| 9 | **Hugging Face** | `claude.ai Hugging Face` | Connected | `hub_repo_search`, `paper_search`, `hf_doc_search` |
| 10 | **Figma** | `claude.ai Figma` | Connected | `get_design_context`, `get_screenshot`, `get_metadata` |
| 11 | **Slack** | Slack plugin (user-level) | Installed | Pending admin approval for The Block workspace |
| 12 | **Cloudflare** | `claude.ai Cloudflare` | Connected | Workers, KV, R2, D1 |
| 13 | **Playwright** | `plugin:playwright` | Connected | Browser automation, screenshots, testing |
| 14 | **Context7** | `plugin:context7` | Connected | Library documentation lookup |
| 15 | **Remotion** | `remotion-docs` | Connected | Remotion documentation |

**IMPORTANT — Google Calendar:** Always query BOTH calendars in parallel:
- `sean.winslow28@gmail.com` (personal/primary)
- `swinslow@theblock.co` (The Block work)

Google Calendar API only supports one calendarId per request — must make parallel calls.

### Preferred MCP Selection (Native over Zapier)

When a service is available through both native MCP and Zapier, **always prefer the native MCP**:

| Service | Native MCP (preferred) | Zapier (fallback) |
|---------|----------------------|-------------------|
| Google Calendar | `claude.ai Google Calendar` or `google-workspace` | `google_calendar_find_events` |
| Gmail | `claude.ai Gmail` or `google-workspace` | `gmail_find_email`, `gmail_send_email` |
| Google Sheets | `google-workspace` (`modify_sheet_values`) | `google_sheets_*` |
| Google Docs | `google-workspace` (`get_doc_content`) | `google_docs_*` |
| Google Drive | `google-workspace` (`search_drive_files`) | `google_drive_*` |
| Jira | `mcp-atlassian` (`jira_search`) | `jira_software_cloud_*` |
| Confluence | `mcp-atlassian` (`confluence_search`) | `confluence_cloud_*` |
| Slack | Slack plugin (when authorized) | `slack_send_channel_message` |
| GitHub | `github` MCP | N/A (not via Zapier) |

### Still Zapier-Only (No Native Alternative)

Keep Zapier for these services:

| Service | Why Zapier | Zapier Tools |
|---------|-----------|-------------|
| **Salesforce** | No standalone MCP exists | `salesforce_find_record`, `salesforce_create_record` |
| **Google Analytics 4** | No standalone MCP exists | `google_analytics_4_run_report_for_a_property` |
| **Webhooks** | Custom HTTP requests | `webhooks_by_zapier_post`, `webhooks_by_zapier_get` |
| **Code execution** | Cloud-side Python/JS | `code_by_zapier_run_python` |

### Pending / Future Integrations

| Service | Status | Notes |
|---------|--------|-------|
| **Slack (The Block)** | Awaiting admin approval | Plugin installed; need workspace admin to authorize |
| **Apple Reminders/Notes** | Researching | Community `apple-mcp` exists; would feed personal tasks to daily-driver |
| **Supabase** | Plugin available | Keys in `.env`; install plugin for direct DB access |

### Integration Architecture for Agent SDK

When connecting MCPs to autonomous agents, follow this pattern:

```python
# In agent's build_options() — configure MCP servers
mcp_servers={
    "vault-tools": create_vault_mcp_server(),
    "mcp-atlassian": {"type": "stdio", "command": "uvx", "args": ["mcp-atlassian"]},
    "obsidian": {"type": "stdio", "command": "npx", "args": ["@mauricio.wolff/mcp-obsidian@latest", vault_path]},
}

# Whitelist specific tools per agent
allowed_tools=[
    "Read", "Write", "Edit", "Glob", "Grep",
    "mcp__vault-tools__vault_inject",
    "mcp__mcp-atlassian__jira_search",
    "mcp__mcp-atlassian__jira_get_issue",
]
```

**Safety rule:** Autonomous agents should use explicit `allowed_tools` whitelists. Never give an unattended agent access to all tools from a service — scope to the minimum needed.

---

## Troubleshooting

### Common Issues

**"No matching distribution found for claude-agent-sdk"**
- Requires Python 3.10+. Check: `python3 --version`
- If using system Python on macOS, install via Homebrew: `brew install python@3.13`

**Agent runs but produces no output**
- Check `vault/90_system/agent-logs/` for error logs
- Run with `--dry-run` to verify prompt construction
- Verify vault paths in `config.toml` are correct

**"Daily driver agent is disabled in config.toml"**
- Set `enabled = true` under `[agents.daily_driver]` in `config.toml`

**Cost higher than expected**
- Lower `max_budget_usd` in `config.toml`
- Reduce `max_turns_default` for shorter runs
- Check `agent-run-history.csv` for per-run cost breakdown

**launchd job not running**
- Verify: `launchctl list | grep com.sean.agent`
- Check plist paths point to correct venv Python
- Review stderr logs in `vault/90_system/agent-logs/`

**"python-dotenv parse warning" on .env**
- Harmless warning from a non-parseable line in `.env`. Does not affect functionality.

### Debugging Steps

1. **Always start with `--dry-run`** to verify the prompt looks right
2. **Check logs** in `vault/90_system/agent-logs/`
3. **Run tests** to verify lib modules work: `PYTHONPATH=. pytest tests/ -v`
4. **Lower limits** for testing: set `max_turns=5` and `max_budget_usd=0.10` in `config.toml`
5. **Check auth**: run `claude --version` and `claude login` to verify CLI auth

---

## Appendix: config.toml Reference

```toml
[paths]
repo_root = "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack"
vault_root = "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault"
skills_dir = ".claude/skills"
life_systems_scripts = "life-systems/scripts"

[agents.daily_driver]
enabled = true
skills = ["daily-driver", "vault-read-write"]
morning_time = "06:00"
evening_time = "17:00"
weekly_day = "Friday"
weekly_time = "16:00"

[agents.preserve_session]
enabled = true
skills = ["preserve-session", "vault-read-write"]

[agents.spending_analysis]
enabled = true
skills = ["subscription-audit", "vault-read-write"]
input_dir = "life-systems/finance"
output_dir = "vault/50_sources/finance"

[agents.process_inbox]
enabled = false
skills = ["process-inbox", "vault-read-write"]

[agents.health_audit]
enabled = false
skills = ["health-habits", "vault-read-write"]

[agents.md_to_anki]
enabled = false
skills = ["vault-read-write"]

[safety]
max_turns_default = 30
max_budget_default = 0.50
permission_mode = "acceptEdits"

[logging]
log_dir = "vault/90_system/agent-logs"
log_level = "INFO"
```

## Appendix: Full Function Reference

### lib/config.py
| Function/Class | Signature | Returns |
|--------|-----------|---------|
| `load_config` | `(config_path?, env_path?)` | `Config` |
| `Config.agent_config` | `(name: str)` | `AgentConfig` |

### lib/skill_loader.py
| Function | Signature | Returns |
|----------|-----------|---------|
| `load_skill_prompt` | `(skill_name, skills_dir)` | `str` |
| `load_skills` | `(skill_names, skills_dir)` | `str` |

### lib/vault_io.py
| Function | Signature | Returns |
|----------|-----------|---------|
| `daily_note_path` | `(vault_root, target_date?)` | `Path` |
| `weekly_note_path` | `(vault_root, target_date?)` | `Path` |
| `yesterday_note_path` | `(vault_root)` | `Path` |
| `inject_at_anchor` | `(file_path, anchor, content)` | `bool` |
| `read_frontmatter` | `(file_path)` | `dict[str, str]` |
| `create_from_template` | `(template_path, destination, substitutions?)` | `Path` |
| `recent_daily_notes` | `(vault_root, days?)` | `list[Path]` |

### lib/logging_setup.py
| Function | Signature | Returns |
|----------|-----------|---------|
| `setup_logger` | `(agent_name, log_dir, log_level?, mode?)` | `Logger` |
| `record_run` | `(log_dir, agent_name, mode, status, cost_usd, duration_ms, turns, notes?)` | `None` |

### lib/custom_tools.py
| Function | Signature | Returns |
|----------|-----------|---------|
| `vault_inject_tool` | `(args: dict)` | `dict` |
| `create_vault_mcp_server` | `()` | MCP server config |

### agents/daily_driver.py
| Function | Signature | Returns |
|----------|-----------|---------|
| `build_preamble` | `(mode, config)` | `str` |
| `build_prompt` | `(mode, config)` | `str` |
| `build_options` | `(config)` | `ClaudeAgentOptions` |
| `run` | `(mode, dry_run?)` | `None` (async) |
| `main` | `()` | `None` |
