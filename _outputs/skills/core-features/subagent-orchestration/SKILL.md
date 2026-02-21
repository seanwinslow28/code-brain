---
name: subagent-orchestration
description: Claude Code subagent and multi-agent architecture assistant. Creates custom agents with YAML frontmatter, configures disallowedTools deny-lists for safe read-only agents, designs swarm/council/pipeline orchestration patterns, and manages background vs foreground execution. Use when creating an agent, running tasks in parallel, delegating to a specialized subagent, designing a multi-agent workflow, or choosing between skills vs agents vs hooks.
---

# Subagent Orchestration

## Purpose

Design and configure Claude Code subagent architectures that parallelize work, enforce security boundaries through deny-lists, and protect the context window from pollution. Use subagents for delegation and isolation; use skills for knowledge; use hooks for enforcement.

## When to Use

- Creating a custom agent (code reviewer, security auditor, documentation writer)
- Deciding whether to use a skill, agent, or hook for a given task
- Configuring tool restrictions with disallowedTools for safe agents
- Running multiple tasks in parallel using background agents
- Designing swarm, council, or pipeline multi-agent patterns
- Preventing context rot in long sessions by isolating exploration

## Examples

**Example 1: Creating a read-only auditor**
```
User: "Create an agent that reviews code for security issues but can't modify anything"
Claude: [Uses subagent-orchestration] Creates .claude/agents/security-auditor.md:

---
name: security-auditor
description: Expert security reviewer. Use proactively when touching auth, crypto, or API code.
model: sonnet
disallowedTools: [Write, Edit, MultiEdit, NotebookEdit, Bash]
color: red
---
You are a strict security auditor. Analyze code for OWASP Top 10 vulnerabilities.
Report findings with file paths and line numbers. Do NOT fix anything yourself.

The disallowedTools deny-list makes this agent physically unable to modify files.
```

**Example 2: Parallel background tasks**
```
User: "I need to refactor 10 controllers to use the new AuthService"
Claude: [Uses subagent-orchestration] Spawns 3 background agents via Task tool:
- Agent A: controllers 1-3 (run_in_background: true)
- Agent B: controllers 4-6 (run_in_background: true)
- Agent C: controllers 7-10 (run_in_background: true)
Main session stays interactive. Each agent returns results when done.
```

**Example 3: Choosing the right component**
```
User: "Should I use a skill or an agent for our code review standards?"
Claude: [Uses subagent-orchestration] Decision:
- SKILL if you want Claude to know your review standards and apply them in the main conversation
- AGENT if you want to delegate heavy review work to an isolated subprocess that returns a summary
- HOOK if you want to force a linting check every time code is edited (deterministic, not probabilistic)
Recommends: Skill for standards knowledge + Hook for automated linting.
```

## Decision Framework: Skills vs Agents vs Hooks

| Need | Component | Why |
|------|-----------|-----|
| Teach Claude a procedure or standard | **Skill** | Loads into main context, guides behavior |
| Offload heavy work (deep research, bulk analysis) | **Agent** | Isolated context, returns summary only |
| Force something to happen every time | **Hook** | Deterministic execution, not probabilistic |
| Quick user-triggered action | **Command** | Slash-command shortcut |

**Key distinction**: Skills are probabilistic (Claude tries to follow). Hooks are deterministic (always execute). Agents provide isolation (separate context window).

## Agent YAML Frontmatter

Agent definitions live in `.claude/agents/*.md` (project) or `~/.claude/agents/*.md` (global).

```yaml
---
name: agent-name              # Required. Matches subagent_type in Task tool.
description: "When to use"    # Required. Main Claude reads this for auto-delegation.
model: sonnet                 # Optional. haiku | sonnet | opus | inherit
disallowedTools:              # Optional. DENY-LIST removes these tools.
  - Write
  - Edit
  - Bash
tools:                        # Optional. ALLOW-LIST (use sparingly).
  - Read
  - Grep
  - Glob
permissionMode: default       # Optional. default | plan | acceptEdits | bypassPermissions
color: blue                   # Optional. Terminal output color.
---

# System Prompt
Your instructions go here. This becomes the agent's system prompt.
```

**Critical rule**: Use `disallowedTools` (deny-list), never allow-list alone. The deny-list is a hard boundary -- the agent cannot use those tools regardless of what the LLM attempts.

## Agent Patterns

### Read-Only Explorer

```yaml
---
name: safe-explorer
description: Explores codebases safely. Cannot modify any files or run commands.
model: haiku
disallowedTools: [Write, Edit, MultiEdit, Bash, NotebookEdit]
color: green
---
Explore the codebase to answer questions. Read files, search for patterns, and report findings. You cannot modify anything.
```

### Documentation Writer (No Shell)

```yaml
---
name: doc-writer
description: Updates README and documentation files. Use when documentation needs updating.
model: sonnet
disallowedTools: [Bash]
color: cyan
---
Update documentation to reflect recent code changes. Read source files to understand current behavior, then update markdown docs accordingly. Do not run commands.
```

### Code Reviewer (Report Only)

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use before committing changes.
model: sonnet
disallowedTools: [Write, Edit, MultiEdit, NotebookEdit]
color: blue
---
Review code changes for:
1. Security vulnerabilities (SQLi, XSS, auth bypass)
2. Performance issues (N+1 queries, memory leaks)
3. Type safety (any types, missing null checks)
Output a prioritized list of findings. Do NOT fix anything yourself.
```

## The Task Tool System

The Task tool spawns subagents. The main Claude calls it automatically or you can request it explicitly.

**How it maps to custom agents**: The `subagent_type` parameter matches the `name` field in the agent's YAML frontmatter exactly.

**Built-in agent types** (available without custom definitions):
- `Explore` -- read-only, fast (Haiku), for "find", "search", "locate"
- `Plan` -- read-only, reasoning-heavy, for "plan", "design"
- `general-purpose` -- full tool access, for complex execution

**Task tool parameters**:
- `subagent_type` (required): agent name or built-in type
- `prompt` (required): specific instructions for this run
- `description` (required): short summary (3-5 words)
- `run_in_background` (optional): true for async execution
- `model` (optional): override the agent's default model

## Background vs Foreground Execution

| Aspect | Foreground (default) | Background |
|--------|---------------------|------------|
| Behavior | Blocking -- main session waits | Async -- main session stays interactive |
| Trigger | Default Task call | `run_in_background: true` or `Ctrl+B` |
| Permissions | Can prompt user interactively | Must be pre-approved; fails on permission prompts |
| Use case | Sequential work needing immediate results | Long-running analysis, bulk operations |

## Multi-Agent Orchestration Patterns

### Swarm Pattern (Parallel Workers)
For embarrassingly parallel tasks like bulk refactoring.

1. Leader creates a task list (files to process)
2. Spawns N background workers via Task tool
3. Each worker claims a subset, executes, reports back
4. Leader aggregates results

### Council Pattern (Consensus)
For high-stakes architectural decisions.

1. Main agent proposes a design
2. Spawns Security-Expert, Performance-Analyst, UX-Reviewer in parallel
3. Each reviews independently and reports findings
4. Main agent synthesizes feedback into a final decision

### Pipeline Pattern (Sequential)
For structured feature implementation.

1. Planner agent (read-only) generates PLAN.md
2. Coder agent implements based on PLAN.md
3. Reviewer agent verifies code matches plan
Separating planning from execution prevents drift.

## Context Isolation Benefits

The core problem subagents solve is **context rot**: in a long session, reading 50 files to find one bug fills the window with noise.

**Solution**: A subagent starts with a clean context. It reads the 50 files, filters the noise, and returns only the relevant finding. The main agent pays the token cost for the summary, not the exploration.

**Rule of thumb**: If a task requires reading more than 5-10 files to find an answer, delegate it to a subagent.

## Success Criteria

- [ ] Agent YAML has valid name and description fields
- [ ] disallowedTools deny-list prevents unintended modifications
- [ ] Agent name matches the directory/file naming convention
- [ ] Background agents do not require interactive permission prompts
- [ ] Context isolation is used for heavy exploration tasks
- [ ] The correct component type is chosen (skill vs agent vs hook)

## Copy/Paste Ready

```
"Create an agent for code review that can't edit files"
"Run these tasks in parallel using background agents"
"Should I use a skill or an agent for this?"
"Design a multi-agent workflow for this feature"
"Create a read-only explorer agent"
```
