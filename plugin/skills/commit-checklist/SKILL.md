---
name: commit-checklist
description: Validates commits against best practices before submission
---

# Commit Checklist Skill

## When to Use

Use this skill when:
- Preparing to commit code changes
- Reviewing commit messages
- Ensuring commits follow project standards
- Before pushing to remote repositories

## Examples

**Example 1: Commit message validation**
```
User: "Help me write a commit message for these changes"
Claude: [Uses commit-checklist skill] Based on your changes, here's a commit message following conventional commits format:

feat: add user authentication middleware

- Implement JWT token validation
- Add error handling for expired tokens
- Update API routes to use new middleware

Closes #123
```

**Example 2: Pre-commit checks**
```
User: "Check if my changes are ready to commit"
Claude: [Uses commit-checklist skill] Running pre-commit checklist:
✓ All tests passing
✓ No console.log statements
✓ Commit message follows conventional format
✓ No sensitive data in changes
⚠ Consider adding unit tests for new function
```

## Checklist Items

This skill validates:
- Commit message format (conventional commits recommended)
- No debug code (console.log, print statements)
- No commented-out code
- No sensitive data (secrets, API keys)
- Tests included for new features
- Documentation updated if needed
- Code follows styleguide

## Copy/Paste Ready

To use this skill:
- "Run commit-checklist on my changes"
- "Validate this commit message"
- "Check if ready to commit"
