---
name: learning-path
description: Structured progression guide for Claude Code from beginner to power user. Provides phase-by-phase milestones, practice exercises, and self-assessment checks for React/Python developers.
---

# Learning Path & Progression

## Purpose

This skill guides you through the structured mastery of Claude Code, moving from basic CLI usage to advanced agentic orchestration. It provides specific milestones, exercises, and checks to ensure you build a solid foundation before attempting complex workflows.

## When to Use

- You are new to Claude Code and don't know where to start
- You feel stuck or inefficient and want to identify knowledge gaps
- You want to advance from "Vibe Coding" to engineering-grade agentic workflows
- You need specific exercises to practice new features (MCP, Hooks, Subagents)

## Examples

**Example 1: Beginner Assessment**
```
User: "I know how to run /init, what should I learn next?"
Claude: [Uses learning-path]
### 🎓 Next Step: Phase 2 (Context Engineering)
You have mastered the basics. Your next milestone is controlling **what** I know.
**Recommended Exercise:**
- Create a `CLAUDE.md` file to enforce your coding standards.
- Use **Plan Mode** (`Shift+Tab+Tab`) for a multi-file refactor.
```

**Example 2: Power User Challenge**
```
User: "Give me an advanced exercise to test my skills."
Claude: [Uses learning-path]
### 🚀 Phase 5 Challenge: Parallel Features
**Task:** Use `git worktree` to spawn two separate agent sessions.
1. Session A: Implement a React component in `feature-frontend/`.
2. Session B: Write the Python API in `feature-backend/`.
**Goal:** Merge both without conflicts using only CLI commands.
```

## Progression Phases

### Phase 1: The Foundation (Beginner)
**Focus:** CLI fluency, Loop discipline, Cost awareness.
*   **Milestone:** Complete single-file edits without "Context Rot".
*   **Key Concepts:** `/init`, `/cost`, `/clear`, `/diff`.
*   **Exercise (React/Python):**
    1.  **The One-Shot:** Navigate to a buggy Python script. Ask: "Fix the `IndexError`." Use `/diff` to verify.
    2.  **Browser Control:** Use `/chrome` to open localhost and inspect a UI element.

### Phase 2: Context Engineering (Intermediate)
**Focus:** Prevention of hallucinations via explicit context control.
*   **Milestone:** Implement multi-file features using `CLAUDE.md` and Plan Mode.
*   **Key Concepts:** `CLAUDE.md`, Plan Mode (`Shift+Tab+Tab`), File mentions (`@utils/auth.py`).
*   **Exercise:**
    1.  **Project Memory:** Create a `CLAUDE.md` enforcing "Functional React Components" and "Pydantic v2".
    2.  **The Planning Drill:** Enter Plan Mode -> "Add dark mode to UserCard". correcting the plan *before* execution.

### Phase 3: Expanding Capabilities (Advanced)
**Focus:** Connecting to the outside world via MCP.
*   **Milestone:** Claude proactively checks databases or docs without manual pasting.
*   **Key Concepts:** MCP Servers (Postgres, GitHub, Brave), Lazy Loading.
*   **Exercise:**
    1.  **Live Docs:** Install **Context7** or a local docs server. Ask: "Check the latest Next.js docs for Server Actions."
    2.  **DB Migration:** Connect **PostgreSQL MCP**. Ask: "Analyze schema and write a migration for 'preferences' column."

### Phase 4: Orchestration (Power User)
**Focus:** Customizing the agent runtime.
*   **Milestone:** You have custom `/slash-commands` and safety hooks.
*   **Key Concepts:** Subagents, Hooks (`PreToolUse`), Custom Commands.
*   **Exercise:**
    1.  **Safety Hook:** Write a hook in `~/.claude/hooks/` blocking `rm -rf`.
    2.  **Subagent Delegation:** Create a "Code Reviewer" subagent. Task: "Critique my changes in `src/`."

### Phase 5: Parallelism (The "10x" Dev)
**Focus:** Asynchronous and headless operations.
*   **Milestone:** Managing multiple active sessions via Git Worktrees.
*   **Key Concepts:** Git Worktrees, Headless Mode (`claude -p`), Session Resume.
*   **Exercise:**
    1.  **Auto-Commit:** Pipe `git diff` into Claude headless to generate commit messages.
    2.  **Recursive Loop:** Script a loop that runs tests and fixes code until passing.

## Self-Assessment Checklist

- [ ] **Phase 1:** Do I run `/clear` every ~20 turns to prevent rot?
- [ ] **Phase 2:** Is my `CLAUDE.md` preventing repetitive mistakes?
- [ ] **Phase 2:** Do I use **Plan Mode** for EVERY multi-file task?
- [ ] **Phase 3:** Have I replaced manual web search with **Brave/Context7 MCP**?
- [ ] **Phase 4:** Do I have at least one custom `/command` to save typing?

## Copy/Paste Ready

```
"What is the next step in my learning path?"
"Give me a Phase 2 practice exercise"
"Am I ready for Phase 3?"
"How do I practice context engineering?"
"List the milestones for power users"
```
