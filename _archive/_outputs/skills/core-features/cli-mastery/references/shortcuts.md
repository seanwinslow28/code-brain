# Complete Keyboard Shortcuts and Commands Reference

## Keyboard Shortcuts

### Session Control
| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+C` | Cancel current generation | Does not exit session |
| `Ctrl+D` | Exit session | Sends EOF |
| `Ctrl+L` | Clear screen | Preserves conversation history |
| `Esc` then `Esc` | Rewind | Opens menu: undo Code only, Conversation only, or Both |
| `Ctrl+B` | Background task | Move running task (bash/subagent) to background |
| `Ctrl+O` | Toggle verbose mode | Shows tool inputs/outputs and thinking blocks |

### Input and Editing
| Shortcut | Action | Notes |
|----------|--------|-------|
| `Tab` | Extended Thinking toggle | Sticky toggle. NOT Plan Mode. |
| `Alt+T` / `Option+T` | Extended Thinking toggle | Alternative to Tab |
| `Shift+Tab` | Cycle permission modes | Normal > Auto-Accept > Plan |
| `Shift+Enter` | New line | Works in iTerm2, WezTerm, Kitty |
| `Alt+P` / `Option+P` | Switch model | Cycle Sonnet/Opus/Haiku while typing |
| `Ctrl+G` | External editor | Opens prompt in $EDITOR |
| `Ctrl+R` | History search | Reverse search past prompts |
| `Ctrl+V` | Paste image | Paste from clipboard |

## Slash Commands

### Session Management
| Command | Action |
|---------|--------|
| `/clear` | Clear conversation (fresh context) |
| `/compact` | Summarize conversation to free tokens |
| `/compact focus on [topic]` | Guided summary with topic retention |
| `/resume` | Pick and resume a past session |
| `/fork` | Branch conversation into new session |
| `/init` | Scan codebase and generate CLAUDE.md |
| `/export` | Save full transcript to Markdown |

### Configuration
| Command | Action |
|---------|--------|
| `/config` | Interactive settings menu |
| `/context` | Token usage visualization |
| `/cost` | Session cost and duration |
| `/model` | Switch models interactively |
| `/permissions` | Manage tool allow/deny rules |
| `/doctor` | Check installation and connectivity |

### Advanced
| Command | Action |
|---------|--------|
| `/plan` | Enter Plan Mode explicitly |
| `/agents` | Manage custom subagents |
| `/tasks` | List background tasks |
| `/mcp` | Manage MCP servers |
| `/skills` | List discovered skills |
| `/hooks` | List active hooks |
| `/teleport` | Resume remote session from claude.ai |
| `/sandbox` | Enable sandboxed execution |
| `/help` | Show available commands |

## Special Prefixes
| Prefix | Function | Example |
|--------|----------|---------|
| `!` | Run bash, add output to context | `!npm test` |
| `#` | Add note to memory | `# Use functional components` |
| `@` | Reference file/directory/URL | `@src/utils/helpers.ts` |
| `&` | Dispatch to Claude Code Remote | `& Refactor auth module` |

## CLI Flags

### Execution
| Flag | Description |
|------|-------------|
| `-p "prompt"` / `--print` | Headless mode: execute and exit |
| `-c` / `--continue` | Resume most recent session |
| `-r "id"` / `--resume` | Resume specific session by ID |
| `--dangerously-skip-permissions` | Bypass all permission prompts |

### Output
| Flag | Description |
|------|-------------|
| `--output-format text` | Raw response (default for -p) |
| `--output-format json` | Structured JSON with metadata |
| `--output-format stream-json` | NDJSON real-time events |
| `--input-format stream-json` | Accept piped stream-json |
| `--verbose` | Include tool usage details |

### Configuration
| Flag | Description |
|------|-------------|
| `--model [name]` | Force specific model |
| `--max-turns [n]` | Limit agent loops |
| `--max-budget-usd [n]` | Cost cap for session |
| `--allowedTools "Tool1,Tool2"` | Auto-approve specific tools |
| `--add-dir [path]` | Grant access outside project root |
| `--no-session-persistence` | Clean slate (no session save) |
| `--debug` | Enable debug logging |
| `--mcp-debug` | Enable MCP-specific debug logs |

### MCP Management
| Command | Description |
|---------|-------------|
| `claude mcp add <name> -- <cmd>` | Add stdio server |
| `claude mcp add --transport http <name> <url>` | Add HTTP server |
| `claude mcp add --scope user <name> ...` | Add to user scope |
| `claude mcp add --scope local <name> ...` | Add to local scope |
| `claude mcp add --env KEY=VAL <name> ...` | Add with env vars |
| `claude mcp list` | List all configured servers |
| `claude mcp remove <name>` | Remove a server |

## Environment Variables
| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API authentication |
| `MAX_THINKING_TOKENS` | Extended thinking budget |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Response size cap |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background processes |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable telemetry/updates |
| `CLAUDE_NO_TELEMETRY` | Disable usage tracking |
| `CLAUDE_CONFIG_DIR` | Override config directory |
| `ENABLE_TOOL_SEARCH` | MCP tool lazy loading |
| `CLAUDE_CODE_TASK_LIST_ID` | Multi-instance task sharing |
