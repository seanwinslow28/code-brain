---
name: parallel-instances
description: Multi-instance parallel Claude Code development. Orchestrates git worktrees, shared task lists, and fan-out patterns for running multiple Claude sessions simultaneously without file conflicts.
---

# Multi-Instance Parallel Development

## Purpose

Orchestrate multiple simultaneous Claude Code sessions to parallelize development work. Use git worktrees for file isolation, shared task lists for coordination, and fan-out scripts for batch processing. Prevent merge conflicts, manage rate limits, and decide when parallel beats sequential.

## When to Use

- Splitting a large feature into independent frontend/backend/docs tracks
- Running a Writer/Reviewer pattern for unbiased code review
- Batch processing many files (migrations, refactors, test generation)
- Multitasking across unrelated tasks in the same repo
- Any time you say "run in parallel", "multiple instances", or "split this work"

## Examples

**Example 1: Feature split**
```
User: "I need to build auth and dashboard simultaneously"
Claude: [Uses parallel-instances]
Sets up two git worktrees — one for feature/auth, one for feature/dashboard.
Opens separate Claude sessions in each worktree. Links them via
CLAUDE_CODE_TASK_LIST_ID for shared progress tracking.
```

**Example 2: Batch migration**
```
User: "Migrate all 200 JS files to TypeScript"
Claude: [Uses parallel-instances]
Uses the fan-out pattern to spawn headless Claude instances, each converting
a subset of files. Monitors progress and collects results.
```

## Git Worktree Setup

Git worktrees check out multiple branches into separate directories, giving each Claude instance its own isolated filesystem while sharing git history.

```bash
# Create a worktree for a feature branch
git worktree add ../feature-auth feature/auth-refactor

# Navigate and start Claude in isolation
cd ../feature-auth
claude

# Create another worktree for parallel work
git worktree add ../feature-ui feature/dashboard-ui
cd ../feature-ui && claude

# Clean up when done (after merge)
git worktree remove ../feature-auth
git worktree remove ../feature-ui
```

**Why worktrees over separate clones:** Worktrees share the `.git` directory, so they are lightweight and keep git history in sync. Two Claude sessions editing the same file in the same directory will conflict; worktrees eliminate this entirely.

## Shared Task Coordination

Link multiple Claude sessions to a shared task list using the `CLAUDE_CODE_TASK_LIST_ID` environment variable. Agents can mark tasks done and check each other's progress.

```bash
# Terminal 1 (Frontend Agent)
export CLAUDE_CODE_TASK_LIST_ID="project-alpha-migration"
claude -p "Mark the backend tasks as pending and start the frontend migration"

# Terminal 2 (Backend Agent)
export CLAUDE_CODE_TASK_LIST_ID="project-alpha-migration"
claude -p "Check the task list. If frontend has started, begin database schema updates."
```

Use this when agents need to signal completion to each other (e.g., "API updated" by Agent A signals Agent B to update the client).

## Fan-Out Pattern (Headless Batch Processing)

For large-scale repetitive tasks, spawn multiple headless instances:

```bash
# Generate file list
find src -name "*.js" > files_to_migrate.txt

# Process files in parallel (backgrounded)
for file in $(cat files_to_migrate.txt); do
  claude -p "Migrate $file to TypeScript. Return ONLY the code." \
         --allowedTools "Read,Write" \
         --output-format text > "${file%.js}.ts" &
done
wait
```

The `--allowedTools` flag prevents the script from hanging on permission prompts. Monitor rate limits carefully when running many instances.

## Writer/Reviewer Pattern

Run two sessions to improve quality without context pollution:

1. **Session A (Writer):** "Implement the RateLimiter class in `src/utils/`."
2. **Session B (Reviewer):** "Review `src/utils/RateLimiter.ts`. Look for race conditions and edge cases. Output a list of issues."
3. **Session A:** "Here is feedback from the reviewer: [paste]. Fix these issues."

The reviewer starts with fresh context and no implementation bias.

## When to Parallelize vs Stay Sequential

| Factor | Parallel | Sequential |
| :--- | :--- | :--- |
| Task independence | High (frontend vs backend) | Low (B depends on A's exact output) |
| Context load | Heavy (splitting prevents overflow) | Light (fits in 200k tokens) |
| Verification | Writer/Reviewer (unbiased review) | Self-correction (agent checks own work) |
| Speed | Fast (latency bound) | Slow (throughput bound) |

**Key heuristic:** If Task B requires deep knowledge of exactly HOW Task A was implemented, keep it sequential. If Task B only cares that Task A is DONE (interface contract), parallelize.

## Instance Limits and Rate Management

- **Interactive sessions:** Practical limit of 3-4 simultaneous sessions (human context-switching cost)
- **Pro Plan:** 3-5 parallel agents will likely hit rate limits quickly
- **Max Plan:** Necessary for sustained parallel workflows (5x+ limits)
- **Subagents vs OS instances:** Built-in subagents (via `/agents`) are more token-efficient because they share the project-level context cache while maintaining isolated conversation windows

## Success Criteria

- [ ] Each parallel session operates in an isolated filesystem (worktree or separate directory)
- [ ] No file conflicts between concurrent sessions
- [ ] Shared task list enables cross-session coordination when needed
- [ ] Rate limits are respected (Pro: 3 max, Max: 5+)
- [ ] Merge conflicts are deferred to git merge, not real-time filesystem collisions

## Copy/Paste Ready

```
"Set up parallel development for auth and dashboard features"
"Run multiple Claude instances on this migration"
"Split this work across worktrees"
"Use the writer/reviewer pattern for this component"
"Fan out this batch job across headless instances"
```
