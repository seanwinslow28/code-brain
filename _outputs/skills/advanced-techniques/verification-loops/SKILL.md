---
name: verification-loops
description: Verification loops and quality assurance for Claude Code. Implements TDD build-test-fix cycles, PostToolUse hooks for auto-linting, Builder-Validator agent patterns, and iterate-until-pass scripting for autonomous quality gates.
---

# Verification Loops and Quality Assurance

## Purpose

Shift Claude Code from passive code generation to active, self-correcting engineering. Implement TDD cycles that prevent false-positive completions, configure PostToolUse hooks for automatic quality gates, create Builder-Validator agent architectures, and script iterate-until-pass loops for autonomous lint and test fixing.

## When to Use

- Starting any feature implementation that requires test coverage
- Setting up automatic linting/formatting after file edits
- Needing unbiased code review via a separate Validator agent
- Debugging with iterative logging when root cause is unclear
- Any time you say "verify this works", "run tests", "iterate until passing", or "quality assurance"

## Examples

**Example 1: TDD workflow**
```
User: "Add a rate limiter with tests"
Claude: [Uses verification-loops]
Writes test file first (RED). Runs tests to confirm failure. Implements
rate limiter (GREEN). Runs tests again. Iterates until all pass without
modifying the test file.
```

**Example 2: Auto-verification setup**
```
User: "Set up auto-formatting and type checking after every edit"
Claude: [Uses verification-loops]
Configures PostToolUse hooks in settings.json — Prettier runs on every
file write, TypeScript type checker runs on .ts/.tsx edits. Errors feed
back to Claude automatically.
```

## TDD Build-Test-Fix Cycle

Enforce a strict Red-Green-Refactor loop. NEVER let Claude modify tests to make them pass.

```
I want to add [Feature X].
1. Create a unit test file `tests/feature_x.test.ts` covering edge cases.
2. Run the test to confirm it fails (RED state).
3. Implement the feature in `src/feature_x.ts`.
4. Run the test again. Iterate on the implementation until the test passes (GREEN state).
5. Do NOT modify the test file during step 4.
```

The constraint "Do not modify the test" prevents the model from lowering standards to achieve a pass.

## PostToolUse Hooks for Auto-Verification

Configure automatic quality gates that run immediately after Claude edits a file. Claude receives error output and self-corrects without human intervention.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      },
      {
        "matcher": "Edit:*.ts|Edit:*.tsx",
        "hooks": [
          {
            "type": "command",
            "command": "pnpm type:check --noEmit"
          }
        ]
      }
    ]
  }
}
```

If `pnpm type:check` fails, the error output feeds back to Claude via the hook's stderr/stdout. Claude sees the type violation immediately and fixes it on the next turn.

## Builder-Validator Agent Architecture

Split responsibilities into a Builder (writes code) and a Validator (checks it). The Validator is explicitly prompted to be critical and reject incomplete work.

**Validator agent definition (`.claude/agents/validator.md`):**

```markdown
---
name: validator
description: Use this agent to verify if a task is actually complete and functional.
tools: Read, Bash, Grep
model: opus
color: red
---
You are a QA Engineer known for strict standards. Your goal is to detect false positives.
1. When asked to verify a task, DO NOT assume it works.
2. Read the implementation files.
3. Run the relevant tests or build commands.
4. If there are ANY errors, missing requirements, or "TODO" comments left in the code, reject the work.
5. Output a bulleted list of failures for the Builder agent to fix.
```

**Orchestration prompt:**
```
Use the builder agent to implement the auth module. Once the builder claims
it is done, use the validator agent to check the work. If the validator
rejects it, send it back to the builder.
```

## PreToolUse Hooks for Protected Files

Block Claude from modifying sensitive files. The hook returns exit code 2 (block) with feedback.

**Hook config (`.claude/settings.json`):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

**Script (`.claude/hooks/protect-files.sh`):**
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED_PATTERNS=(".env" "package-lock.json" "legacy_core.py")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH is protected. Suggest changes instead." >&2
        exit 2
    fi
done
exit 0
```

## The Logger Spiral Technique

When tests fail and the cause is unclear, use iterative logging instead of guessing:

1. Ask Claude to add comprehensive loggers to the code
2. Run the code and pipe output back: `npm run test 2>&1 | tee outfile | claude`
3. If root cause is not visible, add more specific loggers and repeat
4. Remove loggers only after the fix is verified

## Iterate-Until-Pass Scripting

Script Claude to loop autonomously until quality gates pass:

```bash
#!/bin/bash
MAX_RETRIES=5
COUNT=0

while ! npm run lint; do
    if [ $COUNT -eq $MAX_RETRIES ]; then
        echo "Failed to fix lint errors after $MAX_RETRIES attempts."
        break
    fi
    npm run lint 2>&1 | claude -p "Fix these lint errors. Only edit the files mentioned."
    COUNT=$((COUNT+1))
done
```

## Success Criteria

- [ ] Tests are written before implementation (TDD Red-Green-Refactor)
- [ ] PostToolUse hooks auto-run linter and type checker after every edit
- [ ] Validator agent rejects incomplete work with specific failure lists
- [ ] Protected files cannot be modified by Claude (PreToolUse guard)
- [ ] Iterate-until-pass scripts run autonomously with retry limits

## Copy/Paste Ready

```
"Set up TDD verification for this feature"
"Configure auto-formatting hooks for this project"
"Use the builder-validator pattern for this module"
"Run tests and iterate until everything passes"
"Set up file protection hooks for .env and config files"
```
