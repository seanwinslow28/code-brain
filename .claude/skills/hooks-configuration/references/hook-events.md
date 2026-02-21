# Hook Events Reference

## Complete Event Lifecycle

| Event | Trigger Point | Can Block? | Matcher Target | JSON Input Key Fields |
|-------|--------------|-----------|----------------|----------------------|
| SessionStart | Session init or resume | No | `source` (startup, resume, clear, compact) | `session_id`, `cwd` |
| UserPromptSubmit | User presses Enter | Yes | N/A (always fires) | `prompt`, `session_id` |
| PreToolUse | Before tool executes | Yes | `tool_name` (Bash, Edit, Write, Read, etc.) | `tool_name`, `tool_input`, `session_id`, `cwd` |
| PermissionRequest | Permission dialog appears | Yes | tool_name | `tool_name`, `tool_input` |
| PostToolUse | After tool succeeds | No | `tool_name` | `tool_name`, `tool_input`, `tool_output`, `file_path` |
| PostToolUseFailure | After tool fails | No | `tool_name` | `tool_name`, `tool_input`, `error` |
| Notification | System alerts | No | `notification_type` | `notification_type`, `message` |
| SubagentStart | Subagent spawns | No | `agent_type` | `agent_type`, `prompt` |
| SubagentStop | Subagent finishes | Yes | `agent_type` | `agent_type`, `result` |
| Stop | Claude finishes responding | Yes | N/A (always fires) | `stop_hook_active`, `session_id` |
| PreCompact | Before context summarization | No | `trigger` (manual, auto) | `trigger`, `token_count` |
| SessionEnd | Session terminates | No | `reason` (clear, logout, prompt_input_exit) | `reason`, `session_id` |

## JSON Input Payload Examples

### PreToolUse (Bash)
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /var/www"
  },
  "session_id": "sess_abc123",
  "cwd": "/Users/dev/project"
}
```

### PreToolUse (Read)
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/Users/dev/project/.env"
  },
  "session_id": "sess_abc123",
  "cwd": "/Users/dev/project"
}
```

### PostToolUse (Edit)
```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/Users/dev/project/src/app.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_output": "File edited successfully",
  "session_id": "sess_abc123"
}
```

### Stop
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": false,
  "session_id": "sess_abc123"
}
```

### UserPromptSubmit
```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Delete all test files",
  "session_id": "sess_abc123"
}
```

## Hook Configuration JSON Schema

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<RegexPattern>",
        "hooks": [
          {
            "type": "command" | "prompt" | "agent",
            "command": "/path/to/script.sh",
            "prompt": "LLM evaluation instructions...",
            "model": "claude-3-haiku-20240307",
            "timeout": 600,
            "async": false
          }
        ]
      }
    ]
  }
}
```

### Field Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| type | string | required | "command", "prompt", or "agent" |
| command | string | - | Script path or inline command (command type only) |
| prompt | string | - | LLM evaluation query (prompt/agent types only) |
| model | string | haiku | Model override for prompt/agent types |
| timeout | number | 600 (cmd), 30 (prompt) | Seconds before timeout |
| async | boolean | false | Run in background (command type only) |
| matcher | string | "" (match all) | Regex to filter events |

## Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Only Bash tool calls |
| `"Edit\|Write"` | Edit or Write tool calls |
| `"mcp__.*"` | Any MCP server tool |
| `"mcp__github__.*"` | Only GitHub MCP tools |
| `""` or omitted | All tool calls for that event |
