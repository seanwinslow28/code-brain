---
name: commit-checklist
description: Pre-commit validation and commit message assistant. Analyzes staged changes, validates against best practices (no secrets, no debug code, tests pass, conventional commit format), and generates well-structured commit messages. Use when asked to "review my commit", "write a commit message", "check before committing", "validate changes", or "pre-commit check".
---

# Commit Checklist

## Purpose

Validate staged changes against best practices before committing. Catch common issues (secrets, debug code, missing tests), generate well-structured commit messages following conventional commit format, and enforce scope discipline. Works with any git-based project.

## When to Use

- **Pre-commit validation:** "Check if my changes are ready to commit"
- **Commit message:** "Write a commit message for these changes"
- **Review staged changes:** "Review what I'm about to commit"
- **Before pushing:** "Validate before I push"

## Pre-Commit Validation

### The Checklist

Run through these checks on staged changes (`git diff --cached`):

#### Security
- [ ] **No secrets:** No API keys, tokens, passwords, or connection strings
- [ ] **No .env files:** `.env`, `.env.local`, credentials files not staged
- [ ] **No private keys:** No `.pem`, `.key`, `.p12` files
- [ ] **No hardcoded URLs:** No internal/staging URLs that shouldn't be public

#### Code Quality
- [ ] **No debug code:** No `console.log`, `print()`, `debugger`, `binding.pry`, `TODO` left in
- [ ] **No commented-out code:** Remove dead code, don't comment it out
- [ ] **No merge conflict markers:** No `<<<<<<<`, `=======`, `>>>>>>>` markers
- [ ] **No large files:** No binaries, datasets, or files >1MB that belong in LFS or `.gitignore`

#### Completeness
- [ ] **Tests included:** New features have corresponding tests
- [ ] **Tests pass:** All existing tests still pass
- [ ] **Linter clean:** No new linter warnings or errors
- [ ] **Types correct:** TypeScript/type-checked code compiles without errors
- [ ] **Documentation updated:** README, API docs, or comments updated if public interface changed

#### Scope
- [ ] **Focused changes:** Commit addresses one logical change, not a mix
- [ ] **No unrelated changes:** Formatting-only or refactor changes in a separate commit
- [ ] **Correct files staged:** Only intended files are in the staging area

### Running the Checklist

```bash
# View what's staged
git diff --cached --stat
git diff --cached

# Check for secrets patterns
git diff --cached | grep -iE "(api_key|secret|password|token|credential)" || echo "Clean"

# Check for debug code
git diff --cached | grep -nE "(console\.log|debugger|binding\.pry|print\()" || echo "Clean"

# Check for conflict markers
git diff --cached | grep -nE "^[<>=]{7}" || echo "Clean"

# Check for large files
git diff --cached --stat | awk '{print $NF}' | while read size; do
  [[ "$size" =~ ([0-9]+) ]] && [ "${BASH_REMATCH[1]}" -gt 1000 ] && echo "Large file detected"
done
```

## Commit Message Format

### Conventional Commits

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons (no logic change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system or external dependencies |
| `ci` | CI configuration |
| `chore` | Maintenance tasks, dependency bumps |

**Subject line rules:**
- Imperative mood: "Add feature" not "Added feature" or "Adds feature"
- No period at end
- Max 72 characters
- Lowercase after type prefix

**Body rules:**
- Separated from subject by blank line
- Explain *what* and *why*, not *how*
- Wrap at 72 characters

### Good Examples

```
feat(auth): add JWT refresh token rotation

Tokens now rotate on each refresh to prevent replay attacks.
Previous tokens are invalidated after use.

Closes #234
```

```
fix(api): handle null response from payment gateway

The Stripe webhook occasionally sends null charge objects
for disputed transactions. Added null check before accessing
charge.amount to prevent 500 errors.

Fixes #456
```

```
refactor(dashboard): extract chart components into shared module

Moved bar chart, line chart, and pie chart into
src/components/charts/ for reuse across dashboard pages.
No behavior changes.
```

### Bad Examples (and why)

```
# Too vague
fix: fix bug

# Mixed concerns
feat: add login page and fix header and update deps

# Past tense
fixed: fixed the broken test

# Implementation details instead of purpose
refactor: moved function from file A to file B
```

## Workflow

### 1. Review Changes

```bash
git status           # See all modified/untracked files
git diff --cached    # See what's staged
git diff             # See what's NOT staged
```

### 2. Stage Intentionally

Stage specific files rather than `git add .`:

```bash
git add src/auth/login.ts src/auth/login.test.ts
```

### 3. Run Checklist

Go through each section: Security, Code Quality, Completeness, Scope.

### 4. Draft Message

Based on the changes:
1. Identify the type (feat, fix, refactor, etc.)
2. Identify the scope (component, module, or feature area)
3. Write a clear subject line
4. Add body if the *why* isn't obvious from the subject

### 5. Commit

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add JWT refresh token rotation

Tokens now rotate on each refresh to prevent replay attacks.

Closes #234

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## Multi-Commit Strategy

When a PR has multiple logical changes, split into focused commits:

```
1. refactor(db): extract query builder into utility module
2. feat(api): add pagination to /users endpoint
3. test(api): add pagination integration tests
4. docs(api): update API docs with pagination params
```

**Rule:** Each commit should leave the codebase in a working state. Never commit broken code as an intermediate step.

## Examples

**Example 1: Pre-commit check**
```
User: "Check if my changes are ready to commit"
Claude: [Uses commit-checklist]

Reviewing staged changes...

git diff --cached --stat:
  src/api/users.ts     | 45 +++++++++++
  src/api/users.test.ts| 32 ++++++++
  .env.local           |  3 +++

Issues found:
  [BLOCK] .env.local is staged — contains secrets. Unstage with:
    git reset HEAD .env.local

  [WARN] No debug code detected
  [PASS] Tests included for new code
  [PASS] No merge conflict markers

Action needed: Unstage .env.local before committing.
```

**Example 2: Commit message generation**
```
User: "Write a commit message for these changes"
Claude: [Uses commit-checklist]

Analyzing staged diff...

Changes: Added pagination to the users API endpoint with limit/offset
params, cursor-based navigation, and total count header.

Suggested message:

  feat(api): add pagination to users endpoint

  Support limit/offset query params with cursor-based navigation.
  Response includes X-Total-Count header for client-side pagination UI.
  Default limit: 20, max: 100.

  Closes #789
```

## Success Criteria

- [ ] All security checks pass (no secrets, no .env files)
- [ ] No debug code or commented-out code in staged changes
- [ ] Tests included for new functionality
- [ ] Commit message follows conventional commit format
- [ ] Subject line is imperative mood, under 72 characters
- [ ] Each commit is focused on one logical change
- [ ] Files staged intentionally (not blanket `git add .`)

## Copy/Paste Ready

```
"Check if my changes are ready to commit"
"Write a commit message for these changes"
"Review what I'm about to commit"
"Validate this commit message"
"Help me split these changes into multiple commits"
"Run pre-commit checks"
```