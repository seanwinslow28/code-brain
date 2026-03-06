---
name: git-github-workflows
description: Git and GitHub workflow automation. Handles commit messages, branch management (worktrees), PR creations, conflict resolution, and CI/CD pipelines. Use when interacting with version control, setting up Actions, or resolving merge conflicts.
---

# Git & GitHub Workflows

## Purpose

Standardize version control practices and automate repetitive tasks. This skill manages the full lifecycle of a code change: from feature branching (using Worktrees for context isolation) to CI/CD verification (GitHub Actions) to PR submission and clean history management.

## When to Use

- Writing Conventional Commit messages
- Managing branches and Git Worktrees
- Creating and reviewing Pull Requests
- Resolving complex merge conflicts
- Configuring GitHub Actions for React/Python CI/CD

## Examples

**Example 1: Conventional Commit**
```
User: "Generate a commit message for these changes"
Claude: [Uses git-github-workflows]
Based on the staged changes to the auth system, here is a compliant message:

feat(auth): implement JWT-based session handling

- Add session middleware in `src/middleware/auth.ts`
- Update login endpoint to return secure tokens
- Fix type definitions for UserSession

Ref: #123
```

**Example 2: Automated CI/CD Setup**
```
User: "Add a CI pipeline for my React app"
Claude: [Uses git-github-workflows]
I'll add a GitHub Action to build and test on every push:

name: React CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## Domain Content

### 1. Smart Branch Management (Worktrees)

Use **Git Worktrees** for parallel development without context switching overhead.

**Bash Function (`w`)**
Add this to `.zshrc` to manage worktrees.

```bash
function w() {
  local repo=$1
  local branch=$2
  local target="$HOME/projects/worktrees/$repo/$branch"
  
  git worktree add -b "$branch" "$target" main
  cd "$target"
}
```

### 2. PR Automation Patterns

**Automated Review Action**
Use `anthropics/claude-code-action` to review PRs against standards.

```yaml
name: AI Code Review
on: [pull_request]
permissions:
  contents: read
  pull-requests: write
steps:
  - uses: actions/checkout@v4
  - uses: anthropics/claude-code-action@v1
    with:
      anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
      prompt: "Review for security flaws and style violations."
```

### 3. Conflict Resolution

**Strategy**: Context-aware 3-way merge.
1. Identify conflicting files (`git status`).
2. Analyze `HEAD` (current) vs `MERGE_HEAD` (incoming).
3. Synthesize a functional hybrid, don't just pick one.

**Rebase vs Squash**
- **Squash**: Use when merging Feature -> Main (Clean history).
- **Rebase**: Use when updating Feature < - Main (Linear history).

### 4. Ignore Patterns (.gitignore)

Standard robust exclusion list for the stack.

```text
# Dependencies
node_modules/
.venv/
__pycache__/

# Build
dist/
build/
.next/

# Environment - CRITICAL
.env*
!.env.example

# IDE
.vscode/
.idea/
```

### 5. CI/CD Templates

**Python Automation Pipeline**
```yaml
name: Python Script
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

## Success Criteria

- [ ] Commits follow Conventional Commits format (feat, fix, chore)
- [ ] Secrets never committed (.gitignore includes .env)
- [ ] CI/CD pipelines use specific action versions (@v4)
- [ ] Worktrees used for parallel features instead of multiple clones

## Copy/Paste Ready

```
"Generate a commit message"
"Create a GitHub Action for React"
"Resolve merge conflicts in [file]"
"Setup a generic .gitignore"
```
