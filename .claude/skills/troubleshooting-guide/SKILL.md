---
name: troubleshooting-guide
description: Diagnoses Claude Code errors and behavioral issues. Resolves MCP connection failures, permission denials, context rot, and hallucinations using systematic decision trees.
---

# Troubleshooting & Debug Guide

## Purpose

Diagnose and fix common Claude Code runtime issues, connection failures, and behavioral degradation. This skill provides systematic decision trees to resolve "weird" behavior (hallucinations, loops) and technical errors (MCP failures, permission blocks) without needing to search external documentation.

## When to Use

- Claude starts looping, hallucinating, or forgetting instructions ("Context Rot")
- MCP tools fail to appear or return "connection refused" / "JSON-RPC error"
- You encounter "Permission denied" errors for files or commands
- Claude is being "lazy" (refusing to code) or "hyperactive" (editing without planning)
- You need to debug a silent failure in a custom tool or hook

## Examples

**Example 1: Context Rot Diagnosis**
```
User: "Claude is forgetting what I said 5 minutes ago and keeps trying to edit the wrong file."
Claude: [Uses troubleshooting-guide]
### 🛑 Context Rot Detected
The session has exceeded effective context limits.
**Action:**
1. Generate a handoff document: `claude -p "Summarize current state to HANDOFF.md"`
2. Reset session: `/clear`
3. Restore context: `cat HANDOFF.md | claude`
```

**Example 2: MCP Connection Failure**
```
User: "My new 'postgres' tool isn't showing up in the tool list."
Claude: [Uses troubleshooting-guide]
### 🔌 MCP Debugging
**Check:** Is the server logging to stdout?
**Fix:** MCP uses stdout for protocol messages. Redirect logs to stderr.
**Command:** `tail -f ~/Library/Logs/Claude/mcp.log`
```

## Troubleshooting Decisions

### 1. Behavioral Issues ("Claude is acting weird")

| Symptom | Probable Cause | Instant Fix |
| :--- | :--- | :--- |
| **Hallucinating / Looping** | Context window full (>20k tokens used) | Run `/clear` immediately. Do not argue. |
| **"Lazy" (Refusing to code)** | Vague prompting or safety guardrails | Use "Analyze -> Plan -> Execute" pattern. |
| **"Hyperactive" (Edits too fast)** | Missing "Plan Mode" | Enforce `Shift+Tab+Tab` (Plan Mode) before coding. |
| **Regressing (Undoing fixes)** | Context pollution from failed attempts | Create `HANDOFF.md` summary, then `/clear`. |

### 2. MCP Connection Failures

**Decision Tree:**
1.  **Does the server appear in `/mcp status`?**
    *   **NO:** Check `claude_desktop_config.json`.
        *   *Check:* Are you using **absolute paths**? (e.g., `/Users/sean/project/venv/bin/python`, not `python`).
        *   *Check:* Did you restart Claude after editing config?
    *   **YES, but tools are missing:**
        *   *Check:* Is `ENABLE_TOOL_SEARCH` set to `true`? Setting it to `false` forces immediate loading (good for debugging).
2.  **Is there a "JSON-RPC" error?**
    *   *Cause:* Your MCP server is printing to `stdout` (e.g., `print("Starting server...")`).
    *   *Fix:* Change all `print()` to `sys.stderr.write()` or use a logger that writes to stderr.

### 3. Permission Errors

| Error Message | Fix |
| :--- | :--- |
| **"I cannot access .env"** | **Intentional Guardrail.** Use a `PreToolUse` hook to allow specific access or use `source .env` in bash instead of reading the file directly. |
| **"Permission denied (os error 13)"** | **File Ownership.** Run `chmod +x script.sh` or check if the file is owned by root. |
| **"Tool execution rejected"** | **User Settings.** Check `~/.claude/settings.json` for `deny` patterns in the `permissions` object. |

## Technical Debugging Comands

Use these commands to diagnose silent failures:

```bash
# 1. Check MCP Logs (macOS)
tail -n 50 -f ~/Library/Logs/Claude/mcp.log

# 2. Check Claude Desktop Logs (macOS)
tail -n 50 -f ~/Library/Logs/Claude/mcp-server-local.log

# 3. Verify Python MCP Server (Standalone check)
# Run this manually to see if it crashes or prints to stdout
/path/to/venv/bin/python /path/to/server.py
```

## Success Criteria

- [ ] "Context Rot" is resolved by clearing the session (not by adding more tokens)
- [ ] MCP servers connect successfully using absolute paths
- [ ] JSON-RPC errors are eliminated by removing stdout logging
- [ ] Permission errors are identified as either "OS level" or "Claude Setting level"

## Copy/Paste Ready

```
"Why is Claude hallucinating files?"
"Debug my MCP connection error"
"Fix 'permission denied' when reading .env"
"Troubleshoot context overflow"
"Why isn't my tool showing up?"
```
