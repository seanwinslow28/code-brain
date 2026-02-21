---
name: cursor-integration
description: Hybrid workflow assistant for Cursor IDE and Claude Code CLI. Optimizes context sharing, suggests tool selection (Micro vs Macro), and synchronizes configuration. Use when working with both tools, resolving conflicts, or streamlining the dev environment.
---

# Cursor IDE + Claude Code Integration

## Purpose

Maximize developer velocity by combining Cursor's low-latency editing (The Pilot) with Claude Code's autonomous agentic capabilities (The Agent). This skill defines the "Hybrid Workflow," manages context synchronization via file-based memory, and prevents conflicts between the two AI assistants.

## When to Use

- Deciding between Cursor (Composer/Inline) and Claude Code (CLI)
- Setting up project context (`CLAUDE.md` vs `.cursorrules`)
- Resolving file lock/conflict issues between tools
- Automating "background" tasks with Claude while editing in Cursor

## Examples

**Example 1: The "Plan & Execute" Loop**
```
User: "How should I build this complex feature?"
Claude: [Uses cursor-integration]
Use the Hybrid Pattern:
1. **Claude Code (CLI)**: Run `claude --permission-mode plan "Architect feature X"` to generate `implementation-plan.md`.
2. **Cursor (Composer)**: Highlight the plan in Cursor and hit Cmd+I: "Implement the database schema section."
3. **Claude Code (CLI)**: Run `claude "Verify migration"` to test.
```

**Example 2: Background Worker**
```
User: "I need tests for this component but I'm busy coding"
Claude: [Uses cursor-integration]
Offload the testing while you code:
1. Continue writing `Component.tsx` in Cursor.
2. Open terminal: `claude "Watch src/components/Component.tsx and write a full test suite in __tests__"`
```

## Domain Content

### 1. The Matrix: When to Use What

| Task | Cursor (GUI) | Claude Code (CLI) |
| :--- | :--- | :--- |
| **Surgical Edits** | ✅ Best (Cmd+K) | ❌ Slow overhead |
| **Refactoring** | ✅ Good (Composer) | ✅ Best (Multi-file) |
| **New Projects** | ❌ Manual setup | ✅ Best (Scaffolding) |
| **Debugging** | ⚠️ Limited context | ✅ Best (Log analysis) |
| **Tests** | ✅ Single file | ✅ Repo-wide |

### 2. Context Bridge Configuration

Synchronize the "brains" of both tools.

**CLAUDE.md** (Root)
For the CLI agent.
```markdown
# CLAUDE.md
- Build: `npm run build`
- Style: Strict TypeScript, no Any
```

**.cursorrules** (Root)
For Custom Instructions in Cursor.
```markdown
# .cursorrules
(See CLAUDE.md for architecture)
- Always use Composer for multi-file edits
- Prefer functional components
```

### 3. Conflict Prevention

**Parallel Worktrees**
Stop tools from fighting over the same file.

```bash
# Add to .zshrc
function w() {
  git worktree add -b "$2" "../worktrees/$1/$2" main
  code "../worktrees/$1/$2" # Open Cursor in isolated context
}
```

**Terminal Hygiene**
- Use `claude "..."` inside Cursor's integrated terminal for tighter loops.
- Run `/compact` in CLI when context usage hits 40% to keep it fast.

### 4. Shared "Memory Bank"

Create a folder readable by both tools.

```text
.cursor/memory/
├── activeContext.md   # Current focus
├── progress.md        # Todo list
└── decisions.md       # Architecture logs
```
Cursor reads this via context; Claude reads it via `ls`/`read`.

## Success Criteria

- [ ] `CLAUDE.md` and `.cursorrules` exist and are consistent
- [ ] Large refactors delegated to CLI, micro-edits to Cursor
- [ ] No file conflict errors (tools not editing same file simultaneously)
- [ ] Worktrees used for parallel branches

## Copy/Paste Ready

```
"Setup CLAUDE.md and .cursorrules"
"Plan this feature for Cursor implementation"
"Run background tests while I edit"
"Explain the hybrid workflow"
```
