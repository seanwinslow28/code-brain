---
name: plan-and-think
description: Plan Mode and Extended Thinking mastery for Claude Code. Activates read-only exploration via Plan Mode (Shift+Tab or /plan) and deep reasoning via Extended Thinking for complex architecture decisions, stubborn bugs, and multi-file refactors.
---

# Plan Mode and Extended Thinking Mastery

## Purpose

Separate research from implementation using Plan Mode (read-only exploration) and activate deep reasoning with Extended Thinking for complex problems. Combine both for architecture decisions where safety and depth are critical. Correctly use the keyboard shortcuts and understand when each mode provides the most value.

## When to Use

- Analyzing a codebase before making changes (Plan Mode)
- Debugging a stubborn bug that resists simple fixes (Extended Thinking)
- Making architecture decisions with multiple tradeoffs (both combined)
- Creating detailed implementation plans before coding
- Any time you say "plan this", "think deeply", "Plan Mode", "Extended Thinking", or "architecture decision"

## Examples

**Example 1: Architecture planning**
```
User: "Plan how to add GraphQL alongside our REST API"
Claude: [Uses plan-and-think]
Enters Plan Mode for safe exploration. Enables Extended Thinking for deep
analysis. Reads the entire src/api directory without risk of changes.
Evaluates three strategies with tradeoffs. Outputs detailed migration plan.
```

**Example 2: Stubborn bug**
```
User: "This auth bug keeps regressing. Think deeply about the root cause."
Claude: [Uses plan-and-think]
Activates Extended Thinking for deeper reasoning. Allocates extra tokens to
internal Chain of Thought analysis. Traces the bug through multiple code paths
before proposing a fix.
```

## Plan Mode vs Extended Thinking

| Feature | Plan Mode | Extended Thinking |
| :--- | :--- | :--- |
| Primary goal | Safety: read-only exploration | Depth: deep analysis and self-correction |
| What it does | Restricts Claude to read-only tools | Allocates hidden token budget for internal reasoning |
| Keyboard shortcut | Shift+Tab (cycles: Normal, Auto-Accept, Plan) | Option+T (macOS) / Alt+T (Windows/Linux) |
| CLI activation | `claude --permission-mode plan` | `MAX_THINKING_TOKENS=20000` env var |
| Slash command | `/plan` | Toggle via `/config` |
| Visual indicator | Plan mode status in prompt | "thinking..." spinner |
| Best for | Initial exploration, creating specs, onboarding | Debugging, architecture, complex refactors |

## Plan Mode Activation

**Keyboard:** Press Shift+Tab to cycle through modes. From Normal mode, pressing Shift+Tab twice reaches Plan Mode:
```
Normal -> Auto-Accept -> Plan
```

**CLI flag:** Start directly in Plan Mode:
```bash
claude --permission-mode plan
```

**Headless planning query:**
```bash
claude --permission-mode plan -p "Analyze @src and draft a refactor plan"
```

**Project default (`.claude/settings.json`):**
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## Extended Thinking Activation

**Keyboard:** Press Option+T (macOS) or Alt+T (Windows/Linux) to toggle thinking for the current session.

**Verbose mode:** Press Ctrl+O to see raw thinking tokens stream in real-time.

**Environment variable:** Cap the token budget to control costs and latency:
```bash
export MAX_THINKING_TOKENS=20000
```

**Global config:** Enable via `/config` to turn on "Extended thinking" globally.

## The Explore-Plan-Code Workflow

The structured workflow that separates research from implementation:

1. **Enter Plan Mode** (Shift+Tab x2): Ensure no code changes are possible
2. **Explore:** Ask Claude to analyze files or architecture. It uses read-only tools.
   - Prompt: "Read /src/auth and understand our session flow."
3. **Generate plan:** Ask for a detailed implementation plan.
   - Prompt: "Create a step-by-step plan to migrate to OAuth2."
4. **Refine (Ctrl+G):** Open the generated plan in your text editor. Edit manually.
5. **Switch to Normal Mode** (Shift+Tab) and execute.
   - Prompt: "Implement the plan from the previous step."

## The Deep Architect Workflow (Combined)

For maximum depth and safety, combine both modes:

1. **Activate Plan Mode** (Shift+Tab x2) for read-only safety
2. **Activate Extended Thinking** (Option+T) for deeper reasoning
3. **Prompt:**
   > "Analyze the entire `@src/api` directory. Think deeply about how to introduce
   > GraphQL alongside our REST endpoints. Evaluate three strategies, considering
   > performance and developer experience. Propose a detailed migration plan."
4. Claude uses read-only tools to scan code, spends significant tokens reasoning (visible via Ctrl+O), and outputs a high-quality plan
5. **Switch to Normal Mode** and implement

## When to Use Each

**Use Plan Mode when:**
- You want to explore a new codebase without risk
- Creating specs or architecture docs before coding
- Onboarding to an unfamiliar project
- You want Claude to analyze without accidentally changing anything

**Use Extended Thinking when:**
- A bug has resisted multiple fix attempts
- Making a decision with complex tradeoffs
- Refactoring legacy code where backward compatibility matters
- You need Claude to reason through edge cases before acting

**Use both together when:**
- Architecture decisions on large codebases
- Evaluating multiple implementation strategies
- Any "think before you act" scenario on critical systems

## Configuration Example

Force Plan Mode by default and enable thinking for sensitive repos:

```json
{
  "permissions": {
    "defaultMode": "plan"
  },
  "alwaysThinkingEnabled": true,
  "maxThinkingTokens": 16000
}
```

## Headless Planning Script

Run a planning session from the CLI without user interaction:

```bash
claude \
  --permission-mode plan \
  --print "Read @README.md and @src/main.py. Create a plan to add logging." \
  > implementation_plan.md
```

## Success Criteria

- [ ] Plan Mode is used for exploration before any major code changes
- [ ] Extended Thinking is activated for complex reasoning tasks
- [ ] Keyboard shortcuts are used correctly (Shift+Tab for Plan, Option+T for Thinking)
- [ ] The Explore-Plan-Code workflow separates research from implementation
- [ ] Configuration is set appropriately for the project's risk level

## Copy/Paste Ready

```
"Enter Plan Mode and analyze this codebase"
"Think deeply about the root cause of this bug"
"Plan the migration before we start coding"
"Use Extended Thinking to evaluate these architecture options"
"Switch to Plan Mode and explore the auth module"
```
