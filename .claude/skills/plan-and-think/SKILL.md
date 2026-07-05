---
name: plan-and-think
description: Plan Mode and Extended Thinking mastery for Claude Code. Plan Mode = double Shift+Tab or /plan — read-only exploration. Extended Thinking = single Tab — deeper reasoning. Never confuse the two. Routes task shapes to the right mode and matches thinking budget to problem depth for complex architecture decisions, stubborn bugs, and multi-file refactors. Use when you say "plan this", "think deeply", "ultrathink", "Plan Mode", "Extended Thinking", or ask which mode or shortcut a task needs.
---

# Plan Mode and Extended Thinking Mastery

## Purpose

Separate research from implementation with Plan Mode (read-only exploration) and match reasoning depth to problem depth with Extended Thinking. Pick the right mode by lookup instead of re-reasoning it each session, compose both for architecture decisions where safety and depth are both critical, and keep the two toggles impossible to confuse.

## The Two Switches (Never Confuse Them)

> **Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.**
> — CLAUDE.md, Non-Negotiable Rule #1

- **Plan Mode** is the *safety* switch. Double `Shift+Tab` from Normal (the cycle is Normal → Auto-Accept → Plan) or `/plan`. Restricts Claude to read-only tools — nothing can be edited.
- **Extended Thinking** is the *depth* switch. Single `Tab` — a sticky toggle that stays on across turns (`Option+T` / `Alt+T` is the same toggle). Gives Claude more internal reasoning before it answers.

**The trap Rule #1 guards against:** `Tab` and `Shift+Tab` are one modifier apart and do completely different things. `Tab` changes *how hard Claude thinks*; `Shift+Tab` changes *what Claude may touch*. Hold the pair as: `Tab` = think in place, `Shift+Tab` = cycle toward read-only.

What each one is NOT:

- Plan Mode does **not** deepen reasoning — it only removes write access.
- Extended Thinking does **not** add safety — Claude can still edit files while thinking deeply.
- "Both" is **not** a third mode — they are independent toggles on different keys and compose freely (see Deep Architect below).

## When to Use

- Analyzing a codebase before making changes (Plan Mode)
- Debugging a stubborn bug that resists simple fixes (Extended Thinking)
- Making architecture decisions with multiple tradeoffs (both combined)
- Creating detailed implementation plans before coding
- Deciding which switch a task needs — `Tab` vs `Shift+Tab`
- Any time you say "plan this", "think deeply", "ultrathink", "Plan Mode", "Extended Thinking", or "architecture decision"

## Task-Shape Routing

Don't re-reason the choice every session — look it up:

| Task shape | Mode(s) | Keystrokes | Why |
| :--- | :--- | :--- | :--- |
| Explore or onboard an unfamiliar codebase | Plan Mode | `Shift+Tab` ×2 | You can't break what you're still learning |
| Write a spec or architecture doc before coding | Plan Mode | `Shift+Tab` ×2 | The output is a document; write access is pure risk |
| Stubborn or regressing bug | Extended Thinking | `Tab` (add `ultrathink` to the prompt for the gnarliest) | Needs multi-path reasoning, not read-only safety |
| Multi-file or legacy refactor | Plan Mode to scope, then Extended Thinking to execute | `Shift+Tab` ×2, plan, approve; keep `Tab` on | Bound the surface first, then reason about compatibility |
| Architecture decision on a large codebase | Both together | `Shift+Tab` ×2 + `Tab` | Maximum safety and maximum depth |
| Quick, low-stakes edit or lookup | Neither | — | Overhead buys nothing; default mode is fine |

**First move when both apply:** enter Plan Mode first (bound what Claude may touch), then toggle Extended Thinking (add depth).

## Examples

**Example 1: Architecture planning**
```
User: "Plan how to add GraphQL alongside our REST API"
Claude: [Uses plan-and-think]
Enters Plan Mode (Shift+Tab x2) for read-only exploration and Extended
Thinking (Tab) for depth. Reads the entire src/api directory without risk
of changes, evaluates three strategies with tradeoffs, and presents a
detailed migration plan for approval.
```

**Example 2: Stubborn bug**
```
User: "This auth bug keeps regressing. Think deeply about the root cause."
Claude: [Uses plan-and-think]
Extended Thinking only (Tab) — the task wants depth, not read-only safety.
Adds "ultrathink" to the prompt for maximum per-turn reasoning, then traces
the bug through multiple code paths before proposing a fix.
```

## Plan Mode vs Extended Thinking

| Feature | Plan Mode | Extended Thinking |
| :--- | :--- | :--- |
| Primary goal | Safety: read-only exploration | Depth: deep analysis and self-correction |
| What it does | Restricts Claude to read-only tools | Allocates internal reasoning budget before responding |
| Keyboard shortcut | `Shift+Tab` ×2 from Normal (cycles Normal → Auto-Accept → Plan) | `Tab` — sticky toggle (`Option+T` / `Alt+T` is the same toggle) |
| Slash command / CLI | `/plan`; `claude --permission-mode plan` | Toggle via `/config`; `MAX_THINKING_TOKENS` env var caps budget (`0` disables) |
| Default state | Off — you opt in per session or via `defaultMode` | **On** for supported models in current Claude Code — you opt *out* |
| Visual indicator | "plan mode on" above the input box | Thinking blocks stream in the transcript; `Ctrl+O` verbose shows them in full |
| Best for | Initial exploration, creating specs, onboarding | Debugging, architecture, complex refactors |

## Plan Mode Activation

**Keyboard:** Press `Shift+Tab` to cycle through modes. From Normal mode, pressing `Shift+Tab` twice reaches Plan Mode:
```
Normal -> Auto-Accept -> Plan
```

**Slash command:** `/plan` enters Plan Mode explicitly.

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

**Exiting:** When the plan is ready, Claude presents it for approval. Approving exits Plan Mode into execution (optionally with auto-accept edits); rejecting keeps you planning. `Shift+Tab` also cycles you out manually at any time.

## Extended Thinking Activation

**Keyboard:** Single `Tab` — sticky toggle, persists across turns. `Option+T` (macOS) / `Alt+T` (Windows/Linux) is an alternative binding for the same toggle. (Not `Shift+Tab` — that cycles permission modes.)

**Default state:** Current Claude Code enables thinking automatically for supported models. The toggle and settings below exist to turn it *off* or cap it, not to switch it on.

**Per-turn boost:** Include the word `ultrathink` anywhere in a prompt to request deeper reasoning for that turn only. Legacy graduated keywords ("think" < "think hard" < "megathink") no longer map to fixed budgets in current builds — `ultrathink` is the only recognized keyword; other phrasings are ordinary prompt text.

**Budget cap (env var):** Cap the token budget to control cost and latency; when set, it takes precedence over settings, and `0` disables thinking entirely:
```bash
export MAX_THINKING_TOKENS=20000
```

**Settings (`settings.json`):** `"alwaysThinkingEnabled": false` disables thinking; absent or `true` means enabled (the default). `"effortLevel"` (`"low"` | `"medium"` | `"high"` | `"xhigh"`) persists reasoning effort for supported models.

**Verbose mode:** Press `Ctrl+O` to see full thinking blocks stream in real time.

## Matching Thinking Depth to Problem Depth

Mode comes from the routing table; depth comes from here. Together they are the whole decision:

| Problem depth | Setting | Mechanism |
| :--- | :--- | :--- |
| Trivial — rename, lookup, one-liner | Off | `Tab` to toggle off, or `MAX_THINKING_TOKENS=0` for a whole shell |
| Normal feature work | Default (on) | Leave it alone — the budget adapts on supported models |
| Stubborn multi-path bug, weighty tradeoff | Per-turn boost | Add `ultrathink` anywhere in the prompt |
| Sustained deep work — architecture sprint, legacy migration | Persisted dial | `"effortLevel": "high"` (or `"xhigh"`) in `settings.json` |
| Cost-sensitive batch / headless runs | Hard cap | `export MAX_THINKING_TOKENS=<n>` — env overrides settings |

## The Explore-Plan-Code Workflow

The structured workflow that separates research from implementation:

1. **Enter Plan Mode** (`Shift+Tab` ×2): Ensure no code changes are possible
2. **Explore:** Ask Claude to analyze files or architecture. It uses read-only tools.
   - Prompt: "Read /src/auth and understand our session flow."
3. **Generate plan:** Ask for a detailed implementation plan.
   - Prompt: "Create a step-by-step plan to migrate to OAuth2."
4. **Refine:** Give feedback in chat until the plan is right. For long refinement notes, `Ctrl+G` opens your *current prompt* in `$EDITOR` — it edits your next message, not the generated plan.
5. **Execute:** Approve the plan when Claude presents it (this exits Plan Mode), or `Shift+Tab` back to Normal and say "Implement the plan."

## The Deep Architect Workflow (Combined)

Plan Mode and Extended Thinking are orthogonal switches — "use both" just means flipping both, in this order:

1. **Activate Plan Mode first** (`Shift+Tab` ×2) — bound the read-only surface
2. **Toggle Extended Thinking** (`Tab`) — add reasoning depth
3. **Prompt:**
   > "Analyze the entire `@src/api` directory. Think deeply about how to introduce
   > GraphQL alongside our REST endpoints. Evaluate three strategies, considering
   > performance and developer experience. Propose a detailed migration plan."
4. Claude uses read-only tools to scan code, spends significant tokens reasoning (visible via `Ctrl+O`), and outputs a high-quality plan
5. **Approve the plan** (exits Plan Mode) and implement

## Configuration Examples

**Sensitive repo — always start read-only** (thinking is already on by default):
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

**Cheap, fast-turnaround repo — turn thinking off:**
```json
{
  "alwaysThinkingEnabled": false
}
```

**Budget control is environment-level, not settings-level:** use the `MAX_THINKING_TOKENS` env var. `maxThinkingTokens` is a deprecated Agent-SDK option, not a supported `settings.json` key in current builds — don't put it in settings.

## Headless Planning Script

Run a planning session from the CLI without user interaction:

```bash
claude \
  --permission-mode plan \
  --print "Read @README.md and @src/main.py. Create a plan to add logging." \
  > implementation_plan.md
```

## Success Criteria

- [ ] Plan Mode entered via double `Shift+Tab` or `/plan`; Extended Thinking toggled via single `Tab` — the two never confused (Non-Negotiable Rule #1)
- [ ] Mode chosen by lookup from the task-shape routing table, not re-reasoned each session
- [ ] Thinking depth matched to problem depth: off / default / `ultrathink` / `effortLevel` / env cap
- [ ] Research separated from implementation via Explore-Plan-Code, with the plan approved before execution
- [ ] Configuration matches the repo's risk level (`defaultMode: plan` for sensitive repos)

## Copy/Paste Ready

```
"Enter Plan Mode and analyze this codebase"
"Think deeply about the root cause of this bug"
"ultrathink — trace why this auth bug regresses across all three code paths"
"Plan the migration before we start coding"
"Use Extended Thinking to evaluate these architecture options"
"Switch to Plan Mode and explore the auth module"
```

## Provenance

Shortcut canon: `claude-mastery/reference/shortcuts.md` and CLAUDE.md Non-Negotiable Rule #1. Behavior claims (default-on thinking, `ultrathink` as the only surviving keyword, `alwaysThinkingEnabled`, `effortLevel`, deprecated `maxThinkingTokens`) verified against the installed Claude Code v2.1.199 binary, 2026-07.
