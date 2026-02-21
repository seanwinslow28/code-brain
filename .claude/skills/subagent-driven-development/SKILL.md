---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session. Dispatches fresh subagent per task with two-stage review.
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

- Have an implementation plan with mostly independent tasks
- Want to stay in this session (vs. parallel session)
- Tasks can be executed sequentially without tight coupling

**vs. Parallel Instances (separate session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task
- Faster iteration (no human-in-loop between tasks)

## The Process

```
1. Read plan, extract all tasks with full text, create TodoWrite
2. For each task:
   a. Dispatch implementer subagent (./implementer-prompt.md)
   b. If subagent asks questions → answer, provide context
   c. Subagent implements, tests, commits, self-reviews
   d. Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)
   e. If spec issues found → implementer fixes → re-review
   f. Dispatch code quality reviewer subagent (./code-quality-reviewer-prompt.md)
   g. If quality issues found → implementer fixes → re-review
   h. Mark task complete in TodoWrite
3. After all tasks: dispatch final code reviewer for entire implementation
4. Use commit-checklist to complete the work
```

## Prompt Templates

- `./implementer-prompt.md` — Dispatch implementer subagent
- `./spec-reviewer-prompt.md` — Dispatch spec compliance reviewer subagent
- `./code-quality-reviewer-prompt.md` — Dispatch code quality reviewer subagent

## Example Workflow

```
[Read plan file once, extract all 5 tasks with full text and context]
[Create TodoWrite with all tasks]

Task 1: Hook installation script

[Dispatch implementation subagent with full task text + context]

Implementer: "Before I begin - should the hook be installed at user or system level?"
You: "User level (~/.config/hooks/)"

Implementer:
  - Implemented install-hook command
  - Added tests, 5/5 passing
  - Self-review: Found I missed --force flag, added it
  - Committed

[Dispatch spec compliance reviewer]
Spec reviewer: Spec compliant - all requirements met

[Dispatch code quality reviewer]
Code reviewer: Clean. Approved.

[Mark Task 1 complete, proceed to Task 2]
```

## Red Flags

**Never:**
- Start implementation on main/master branch without explicit user consent
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context (subagent needs to understand where task fits)
- **Start code quality review before spec compliance passes**
- Move to next task while either review has open issues

**If subagent asks questions:**
- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

**If reviewer finds issues:**
- Implementer (same subagent) fixes them
- Reviewer reviews again
- Repeat until approved

**If subagent fails task:**
- Dispatch fix subagent with specific instructions
- Don't try to fix manually (context pollution)

## Integration

**Required before starting:**
- `git-github-workflows` — Set up isolated workspace/branch before starting

**Creates the plan this skill executes:**
- `tech-spec` — Implementation plans with bite-sized tasks

**Subagents should use:**
- `verification-loops` — TDD for each task

**Alternative workflow:**
- `parallel-instances` — Use for parallel session instead of same-session execution

## Success Criteria

- Every task completed through full cycle (implement -> spec review -> quality review)
- No tasks skipped or partially completed
- All reviewer issues resolved before proceeding
- Final code review passes for entire implementation
- All tests pass
