---
name: cli-mastery
description: Claude Code keyboard shortcuts, slash commands, CLI flags, and power user workflow reference. Covers all keyboard shortcuts, permission mode cycling, Plan Mode (double Shift+Tab) vs Extended Thinking (single Tab), slash commands for session management, @ mentions, ! bash prefix, CLI flags for headless mode, and efficiency techniques like context reset and parallel worktrees. Use when looking up keyboard shortcuts, CLI flags, slash commands, or workflow optimizations.
---

# Commands, Shortcuts, and CLI Mastery

## Purpose

Provide a complete reference for Claude Code keyboard shortcuts, slash commands, CLI flags, and power user workflows. Master the interaction model to work faster and manage context effectively.

## When to Use

- Looking up a keyboard shortcut or slash command
- Switching between permission modes (Normal, Auto-Accept, Plan)
- Using Plan Mode vs Extended Thinking (critical distinction)
- Finding CLI flags for headless or automated execution
- Optimizing workflow with context resets, parallel sessions, or worktrees
- Using special prefixes (!, #, @, &) for quick actions

## Examples

**Example 1: Mode confusion**
```
User: "How do I enter Plan Mode?"
Claude: [Uses cli-mastery]
Plan Mode: Press Shift+Tab TWICE (double Shift+Tab) or type /plan.
This is NOT the same as Extended Thinking (single Tab or Alt+T).
- Plan Mode: Claude creates a plan, gets approval, then executes. Uses Opus for planning, Sonnet for coding.
- Extended Thinking: Claude reasons silently before responding. Toggle with Tab or Alt+T.
```

**Example 2: CLI flags for automation**
```
User: "How do I pipe a file into Claude Code?"
Claude: [Uses cli-mastery]
cat build.log | claude -p "Analyze these logs for errors"

Key flags:
- -p "prompt": Headless mode (execute and exit)
- --output-format json: Structured output for parsing
- --max-turns 5: Prevent infinite loops
- --model opus: Force a specific model
```

**Example 3: Context management**
```
User: "My session is getting slow and Claude keeps forgetting things"
Claude: [Uses cli-mastery] Context rot detected. Options:
1. /compact focus on [current task] -- summarize and free tokens
2. HANDOFF.md pattern: Ask Claude to write a handoff summary, then /clear and resume from @HANDOFF.md
3. /clear -- full reset if you're switching tasks entirely
4. /context -- check token usage breakdown to see what's consuming space
```

## Permission Modes

Cycle through modes with **Shift+Tab**:

| Mode | Indicator | Description |
|------|-----------|-------------|
| Normal (Default) | (None) | Asks permission for edits and shell commands |
| Auto-Accept | `accept edits on` | Auto-approves file edits. Still asks for shell. |
| Plan Mode | `plan mode on` | Read-only. Opus plans, Sonnet executes. |

YOLO Mode (bypasses ALL permissions) is CLI-only: `--dangerously-skip-permissions`

## Keyboard Shortcuts

For the complete shortcut reference table, see `references/shortcuts.md`.

### Session Control
| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current generation (does not exit) |
| `Ctrl+D` | Exit session (EOF) |
| `Ctrl+L` | Clear screen (preserves history) |
| `Esc Esc` | Rewind -- undo last action (Code, Conversation, or Both) |
| `Ctrl+B` | Move running task to background |
| `Ctrl+O` | Toggle verbose mode (shows thinking blocks) |

### Input and Editing
| Shortcut | Action |
|----------|--------|
| `Tab` | Extended Thinking toggle (NOT Plan Mode) |
| `Alt+T` / `Option+T` | Extended Thinking toggle (alternative) |
| `Shift+Tab` | Cycle permission modes (Normal > Auto-Accept > Plan) |
| `Shift+Enter` | New line without submitting |
| `Alt+P` / `Option+P` | Switch model (Sonnet/Opus/Haiku) |
| `Ctrl+G` | Open prompt in external editor ($EDITOR) |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+V` | Paste image from clipboard |

### Critical Distinction

| Action | Shortcut | What Happens |
|--------|----------|-------------|
| **Plan Mode** | `Shift+Tab` x2 or `/plan` | Opus generates a plan for approval, then Sonnet executes |
| **Extended Thinking** | `Tab` or `Alt+T` | Model reasons silently before responding (thinking budget) |

These are NOT the same. Never document Tab as entering Plan Mode.

## Slash Commands

### Session and Context
| Command | Action |
|---------|--------|
| `/clear` | Clear conversation history (fresh context) |
| `/compact` | Summarize conversation to free tokens |
| `/compact focus on [topic]` | Guided summary keeping specific context |
| `/resume` | Resume a past session |
| `/fork` | Branch conversation into new session |
| `/init` | Scan codebase and generate CLAUDE.md |
| `/export` | Save transcript to Markdown file |

### Configuration and Status
| Command | Action |
|---------|--------|
| `/config` | Interactive settings menu |
| `/context` | Token usage breakdown |
| `/cost` | Session cost and duration |
| `/model` | Switch models |
| `/permissions` | Manage tool allow/deny lists |
| `/doctor` | Check installation health |

### Advanced
| Command | Action |
|---------|--------|
| `/plan` | Enter Plan Mode |
| `/agents` | Manage custom subagents |
| `/tasks` | List running background tasks |
| `/mcp` | Manage MCP servers |
| `/skills` | List loaded skills |
| `/teleport` | Resume remote session from claude.ai |
| `/sandbox` | Enable sandboxed execution |

## Special Prefixes

| Prefix | Function | Example |
|--------|----------|---------|
| `!` | Execute bash immediately, add output to context | `!npm test` |
| `#` | Add note to memory / CLAUDE.md | `# Always use TypeScript` |
| `@` | Reference file, directory, or URL | `@src/utils/` |
| `&` | Dispatch task to Claude Code Remote (background) | `& Fix the tests` |

## CLI Flags

### Execution
| Flag | Description |
|------|-------------|
| `-p "prompt"` | Headless mode: execute, print, exit |
| `-c` / `--continue` | Resume most recent session |
| `-r "id"` / `--resume` | Resume specific session |
| `--dangerously-skip-permissions` | YOLO mode (sandboxed environments only) |

### Configuration
| Flag | Description |
|------|-------------|
| `--model [name]` | Force specific model |
| `--output-format json\|text\|stream-json` | Output format for parsing |
| `--max-turns [n]` | Limit agent loops (prevents runaway) |
| `--max-budget-usd [amount]` | Cost cap for the session |
| `--allowedTools "Bash,Read"` | Whitelist tools for auto-approval |
| `--add-dir [path]` | Grant access outside project root |
| `--no-session-persistence` | Clean slate per run (CI use) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API authentication |
| `MAX_THINKING_TOKENS` | Extended thinking budget (0 to disable) |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Response size cap (default 32k) |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background processes |
| `CLAUDE_NO_TELEMETRY` | Disable usage tracking |
| `CLAUDE_CONFIG_DIR` | Override config directory location |
| `ENABLE_TOOL_SEARCH` | MCP tool lazy loading (auto/true/false) |

## Power User Workflows

### Context Reset Pattern
Prevent context rot in long sessions:
1. Ask Claude: "Create a HANDOFF.md summarizing progress and next steps"
2. Run `/clear`
3. Prompt: "Read @HANDOFF.md and continue"

### Parallel Worktrees
Run multiple Claude instances on different branches:
```bash
git worktree add ../feature-branch feature-branch
cd ../feature-branch && claude
```
Each worktree gets its own context with no collision.

### Pipe Workflows
```bash
cat error.log | claude -p "What caused this crash?"
git diff | claude -p "Review this diff for security issues"
claude -p "List all TODO comments" --output-format json | jq '.result'
```

## Success Criteria

- [ ] Correct shortcut is used (Tab for thinking, Shift+Tab x2 for plan mode)
- [ ] Appropriate slash command chosen for the situation
- [ ] CLI flags used correctly for headless/automation scenarios
- [ ] Context management prevents degraded performance
- [ ] Permission mode matches the current task's risk level

## Copy/Paste Ready

```
"What keyboard shortcuts are available?"
"How do I enter Plan Mode?"
"What CLI flags can I use for automation?"
"Show me all slash commands"
"How do I manage my context window?"
```
