---
name: context-management
description: Context window management for Claude Code. Prevents context overflow, implements the Sawtooth compression pattern, manages handoff files, and recovers from context rot symptoms like hallucination and instruction drift.
---

# Context Window Management

## Purpose

Manage Claude Code's context window to maintain high-quality output throughout long sessions. Implement the Sawtooth pattern (explore, consolidate, clear, repeat), use handoff files for session continuity, recognize context overflow symptoms, and apply recovery techniques before quality degrades.

## When to Use

- Starting a long development session that may exceed context limits
- Noticing Claude hallucinating file names, forgetting instructions, or producing lazy code
- Needing to pass work between sessions without losing progress
- Deciding whether to use /compact, /clear, or subagent delegation
- Any time you mention "context window", "running out of context", "Claude forgot", or "long session"

## Examples

**Example 1: Session handoff**
```
User: "I'm about to hit context limits, help me hand off"
Claude: [Uses context-management]
Writes a HANDOFF.md summarizing accomplishments, current state, known issues,
and next steps. Instructs user to /clear and reload from HANDOFF.md.
```

**Example 2: Quality degradation**
```
User: "Claude keeps referencing files that don't exist"
Claude: [Uses context-management]
Recognizes hallucination as a context rot symptom. Recommends immediate /clear
or /rewind. Generates handoff file before clearing.
```

## The Sawtooth Pattern

Instead of letting context grow monotonically until it overflows, use an explore-consolidate-clear cycle:

1. **Explore:** Work on the current task, reading files and writing code
2. **Consolidate:** Before hitting limits, write findings to a handoff file
3. **Clear:** Run `/clear` to wipe the context window
4. **Resume:** Load the handoff file and continue

This keeps the context window fresh and reasoning quality high.

## Handoff File Strategy

Before clearing, generate a persistent summary file:

```markdown
Write a HANDOFF.md file in the .claude/context/ directory.
Include:
1. What we accomplished in this session.
2. The current state of [Feature X].
3. Known issues or bugs discovered.
4. Exact next steps for the next session.
5. Key architectural decisions made.

Ensure this file is concise enough to load into a fresh session.
```

Resume in a new session:

```bash
claude "Read @.claude/context/HANDOFF.md and continue working on the next steps."
```

## Manual /compact vs Auto-Compact

| Feature | Manual /compact | Auto-compact |
| :--- | :--- | :--- |
| Trigger | You type `/compact [instructions]` | Automatic at ~95% capacity |
| Control | You specify what to preserve | Algorithm decides |
| Risk | Low (you guide the summary) | High (may discard nuanced instructions) |
| When to use | Between distinct sub-tasks | Last resort (let it run if you forgot) |

**Best practice:** Proactively compact or clear BEFORE hitting the limit. Specify what to keep:

```
/compact Keep the auth refactor decisions and the API contract. Drop the debugging logs.
```

Adjust the compaction threshold to trigger earlier (e.g., at 50% capacity) for sharper performance throughout.

## Context Tiering: What Goes Where

| Tier | Location | Content | Persistence |
| :--- | :--- | :--- | :--- |
| Tier 1 (Always on) | CLAUDE.md | Build commands, style rules, "never" rules | Permanent |
| Tier 2 (Session) | Handoff files | Session state, decisions, next steps | Between sessions |
| Tier 3 (Ephemeral) | Conversation | Debug logs, iteration cycles, temp reasoning | Current session only |

**Rule:** If you correct Claude more than once on the same thing, promote it from Tier 3 to Tier 1.

## Subagent Delegation for Context Protection

Delegate heavy read operations to subagents. Subagents run in isolated context windows, so reading 50 files to find a bug does not pollute your main session.

```
Use a subagent to investigate the auth module and report back the root cause of the login bug.
```

The subagent returns only its findings to your main context, keeping it clean and focused.

## Signs of Context Overflow

Recognize these symptoms and act immediately:

- **Hallucinations:** Claude references files that do not exist or uses deprecated APIs
- **Lazy coding:** Claude starts leaving `// ... rest of code` placeholders instead of full implementations
- **Instruction drift:** Claude ignores "never" rules established at the start of the session
- **Repetition:** Claude re-explains things it already covered, or asks questions already answered

## Recovery Techniques

1. **`/clear`**: Most effective. Wipe the session and provide a handoff summary
2. **`/rewind`**: Double-tap `Esc` or type `/rewind` to undo recent steps (e.g., after cat-ing a massive log file)
3. **Clone/Half-Clone**: Duplicate the conversation, keeping only the relevant half
4. **Do NOT argue**: Never try to correct a confused context window with more conversation. Clear it.

## Re-injecting Context via Hooks

When auto-compaction drops critical context, re-inject it automatically:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'REMINDER: Use Bun, not npm. Current sprint: Auth Refactor.'"
          }
        ]
      }
    ]
  }
}
```

## V4 Optimization: Lazy Loading

Claude Code V4 (Jan 2026) reduces initial context usage by ~85% (from ~77k to ~8.7k tokens) via MCP Tool Search. Tool definitions are lazy-loaded only when needed rather than loaded at startup.

## Success Criteria

- [ ] Session handoffs preserve all critical state in a loadable file
- [ ] Context rot symptoms are caught before quality drops significantly
- [ ] Subagents are used for heavy read operations to protect main context
- [ ] /compact is used proactively with explicit preservation instructions
- [ ] Recovery (/clear, /rewind) is applied immediately when symptoms appear

## Copy/Paste Ready

```
"Write a handoff file before I clear this session"
"My context is getting long, help me compact"
"Claude keeps forgetting my instructions"
"Set up context management for this long refactoring session"
"Use a subagent to investigate this so we don't pollute context"
```
