---
name: hooks-configuration
description: Claude Code hooks creation and debugging assistant. Configures PreToolUse, PostToolUse, Stop, SessionStart, UserPromptSubmit, and other lifecycle hooks in settings.json. Creates command hooks (Bash/Python scripts), prompt-based hooks (LLM evaluation), and agent hooks. Handles exit codes (0=allow, 1=error, 2=deny), matchers, async execution, and security enforcement patterns. Use when creating a hook, debugging a hook, blocking dangerous commands, auto-formatting on save, running tests on stop, or adding session logging.
---

# Hooks Configuration

## Purpose

Create, configure, and debug Claude Code hooks that enforce security policies, automate quality checks, and inject context at precise points in the agentic loop. Hooks are deterministic -- they always execute, unlike skills which rely on model judgment.

## When to Use

- Creating a PreToolUse hook to block dangerous commands or sensitive file access
- Setting up PostToolUse hooks for auto-formatting or logging
- Adding a Stop hook to run tests before Claude yields control
- Configuring SessionStart hooks to inject project context
- Debugging a hook that is not firing or is causing errors
- Choosing between command hooks, prompt hooks, and agent hooks

## Examples

**Example 1: Block secrets access**
```
User: "Create a hook that prevents Claude from reading .env files"
Claude: [Uses hooks-configuration] Creates .claude/hooks/block-secrets.py:

import sys, json
data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')
if '.env' in path or 'secrets' in path:
    print(f"ACCESS DENIED: '{path}' contains secrets.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)

Adds to .claude/settings.json:
"PreToolUse": [{"matcher": "Read|Edit|Write", "hooks": [{"type": "command", "command": "python3 .claude/hooks/block-secrets.py"}]}]
```

**Example 2: Auto-format Python files**
```
User: "Run ruff format every time Claude edits a Python file"
Claude: [Uses hooks-configuration] Configures a PostToolUse hook with matcher "Edit|Write" that checks if the file ends in .py, then runs ruff format on it. Uses exit code 0 for success, exit code 1 for format failure (non-blocking).
```

**Example 3: Test gate before stopping**
```
User: "Don't let Claude stop until tests pass"
Claude: [Uses hooks-configuration] Creates a Stop hook that runs npm test. If tests fail, exits with code 2 and prints failures to stderr. Claude reads the stderr and continues fixing. Includes stop_hook_active check to prevent infinite loops.
```

## Hook Event Reference

For the complete event reference with matchers and JSON payloads, see `references/hook-events.md`.

| Event | Can Block? | Common Use |
|-------|-----------|------------|
| SessionStart | No | Inject git status, project context |
| UserPromptSubmit | Yes | Validate prompts, inject dynamic context |
| PreToolUse | Yes | Security firewall, block destructive commands |
| PostToolUse | No | Auto-format, logging, notifications |
| Stop | Yes | Run tests, verify completion criteria |
| SubagentStop | Yes | Verify subagent work quality |
| PreCompact | No | Archive transcripts, inject summary hints |
| SessionEnd | No | Cleanup temp files, audit logging |

## Exit Code Protocol

| Code | Name | Behavior |
|------|------|----------|
| **0** | Allow | Action proceeds. STDOUT injected into context for SessionStart/UserPromptSubmit. |
| **1** | Error | Action proceeds. STDERR logged but ignored. Script failed internally. |
| **2** | Deny | Action BLOCKED. STDERR fed back to Claude as rejection reason. |

Exit code 2 is the enforcement mechanism. Always print a helpful message to stderr so Claude can self-correct.

## Hook Types

### Command Hooks (type: "command")
Shell scripts that receive JSON on stdin and communicate via exit codes.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/firewall.sh",
        "timeout": 30
      }]
    }]
  }
}
```

### Prompt Hooks (type: "prompt")
Send a query to a fast LLM (defaults to Haiku) for evaluation. Must return JSON.

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Evaluate if the task is complete. Check: 1. All acceptance criteria met. 2. Tests passed. 3. No TODO placeholders left. Respond with JSON: {\"ok\": true} or {\"ok\": false, \"reason\": \"what is missing\"}.",
        "timeout": 30
      }]
    }]
  }
}
```

### Agent Hooks (type: "agent")
For complex verification requiring tool use (e.g., actually running a command to check).

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Run npm test and verify all tests pass. If any fail, block the stop action.",
        "timeout": 120
      }]
    }]
  }
}
```

## Complete Hook Script Patterns

### Security Firewall (Bash)

```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command')

BLOCKED_PATTERNS=("rm -rf" "curl" "wget" "chmod 777" "dd if=" "> /dev/sd")
for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$CMD" == *"$pattern"* ]]; then
    echo "BLOCKED: Command contains '$pattern'. Use safer alternatives." >&2
    exit 2
  fi
done

exit 0
```

### Secret Blocker (Python)

```python
#!/usr/bin/env python3
import sys, json

data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')

SENSITIVE = ['.env', 'secrets/', 'credentials', '.pem', '.key']
for pattern in SENSITIVE:
    if pattern in path:
        print(f"ACCESS DENIED: '{path}' matches sensitive pattern '{pattern}'.", file=sys.stderr)
        print("Use environment variables from README instead.", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

### Auto-Format on Edit (Python)

```python
#!/usr/bin/env python3
import sys, json, subprocess

data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')

FORMATTERS = {
    '.py': ['ruff', 'format'],
    '.ts': ['npx', 'prettier', '--write'],
    '.tsx': ['npx', 'prettier', '--write'],
    '.js': ['npx', 'prettier', '--write'],
}

ext = '.' + path.rsplit('.', 1)[-1] if '.' in path else ''
if ext in FORMATTERS:
    try:
        subprocess.run([*FORMATTERS[ext], path], capture_output=True, check=True)
        print(f"Formatted {path}")
    except subprocess.CalledProcessError as e:
        print(f"Format failed: {e.stderr}", file=sys.stderr)
        sys.exit(1)

sys.exit(0)
```

### Stop Gate with Loop Prevention

```bash
#!/bin/bash
INPUT=$(cat)
LOOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# Prevent infinite loops: if stop hook already fired, let Claude stop
if [ "$LOOP_ACTIVE" = "true" ]; then
  exit 0
fi

# Run tests
npm test 2>&1
if [ $? -ne 0 ]; then
  echo "Tests failed. Fix them before stopping." >&2
  exit 2
fi

exit 0
```

## Matcher Reference

The matcher field is a regex that filters which tool calls trigger the hook.

| Event | Matches Against | Example Matchers |
|-------|----------------|-----------------|
| PreToolUse / PostToolUse | tool_name | `"Bash"`, `"Edit\|Write"`, `"mcp__.*"` |
| SessionStart | source | `"startup"`, `"resume"`, `"clear"` |
| SessionEnd | reason | `"clear"`, `"logout"` |
| SubagentStart / Stop | agent_type | `"Explore"`, `"Plan"`, custom names |
| Stop / UserPromptSubmit | N/A | No matcher support; always fires |

## Async vs Sync Hooks

| Aspect | Sync (default) | Async (`"async": true`) |
|--------|---------------|------------------------|
| Blocking | Yes -- Claude waits | No -- Claude continues immediately |
| Can deny (exit 2) | Yes | No (action already proceeded) |
| Use case | Security checks, pre-validation | Logging, notifications, slow tests |
| Available for | command, prompt, agent | command only |

## Configuration Best Practices

1. **Use jq for JSON parsing** in Bash hooks -- never grep raw JSON input
2. **Print helpful stderr on exit 2** -- Claude reads it and self-corrects
3. **Check stop_hook_active** in Stop hooks to prevent infinite loops
4. **Use absolute paths** or `$CLAUDE_PROJECT_DIR` for script references
5. **Scope appropriately**: global hooks in `~/.claude/settings.json`, project hooks in `.claude/settings.json`
6. **Quiet STDOUT** for PreToolUse hooks unless returning structured JSON

## Success Criteria

- [ ] Hook fires on the correct event and matcher
- [ ] Exit code 2 blocks the intended action with a helpful stderr message
- [ ] No infinite loops in Stop hooks (stop_hook_active check present)
- [ ] Scripts are executable (chmod +x) and handle JSON input via stdin
- [ ] Hook is registered in the correct scope (global vs project)

## Copy/Paste Ready

```
"Create a hook that blocks dangerous bash commands"
"Add auto-formatting when Claude edits files"
"Set up a test gate so Claude can't stop until tests pass"
"Why isn't my PreToolUse hook firing?"
"Add session logging for all tool usage"
```
