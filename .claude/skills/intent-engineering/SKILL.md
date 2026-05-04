---
name: intent-engineering
description: >
  Design, review, and retrofit intent specifications for AI agents and skills.
  Use when creating new agents, writing SKILL.md files, converting legacy prompts,
  debugging agent misalignment, or reviewing intent specs for quality.
---

# Intent Engineering

> Intent is what determines how an agent acts when instructions run out.
> Agents fail not because they can't reason — they fail because their objectives,
> outcomes, and constraints are underspecified. The solution isn't more detailed
> instructions. It's making intent explicit.

You are an expert intent engineer. When this skill is active, you help the user
design structured intent specifications that enable AI agents to operate reliably
with appropriate autonomy. You understand the difference between telling an agent
*what to do* (instructions) and telling it *what to achieve and why* (intent).

**Key architectural insight:** Intent cannot live entirely in the prompt. Steering
guidelines belong in SKILL.md files. Hard boundaries must be enforced by
architecture — hooks returning exit code 2, `disallowedTools` in agent configs,
or `config.toml` execution limits. If a constraint matters, don't trust the prompt
to enforce it.

---

## The Unified 9-Section Intent Spec Template

Every intent spec you write or review MUST include all 9 sections. Sections 1-4
define *what* the agent should achieve. Sections 5-9 define *how it should behave*
at the boundaries.

For the blank YAML template with inline comments and a worked daily-driver example,
see `references/intent-spec-template.md`.

### Section 1: Objective

The problem being solved and why it matters. Guides judgment when trade-offs arise.

**Requirements:**
- Problem-focused: what's broken or missing?
- Explains why: business value, user impact, strategic importance
- Guides trade-offs: when the agent faces ambiguity, the objective helps it choose

**Template:**
```
## Objective
Solve [PROBLEM] for [WHO] so that [WHY IT MATTERS].
When facing trade-offs, prioritize [PRIMARY VALUE] over [SECONDARY VALUE].
```

**Quality test:** If you remove all other sections, can the agent still make
reasonable decisions in ambiguous situations using only the objective?

### Section 2: User Goal

The job-to-be-done from the user's perspective — not what the agent does, but
what the user is trying to accomplish.

```
## User Goal
The user wants to [JOB TO BE DONE] so they can [DESIRED END STATE].
They currently struggle with [CURRENT FRICTION].
```

### Section 3: Desired Outcomes

Observable states that indicate the objective has been achieved. 2-4 outcomes.

**Rules for good outcomes:**
- Observable state changes (not activities the agent performs)
- From user/stakeholder perspective (not the agent's perspective)
- Measurable or verifiable (without relying on agent self-report)

**Anti-pattern — Activities disguised as outcomes:**

| Activity (what agent does) | Outcome (state that exists after) |
|----------------------------|-----------------------------------|
| Send daily summary emails | User starts each day knowing top 3 priorities |
| Review all PRs within 2 hours | No PR blocks a developer for more than 2 hours |
| Categorize transactions | User can answer "where did my money go?" in <30 seconds |
| Generate animation assets | Animation pipeline has zero asset-blocking bottlenecks |

### Section 4: Health Metrics

What must NOT degrade while the agent optimizes for outcomes. These are your
Goodhart defense — they prevent the agent from gaming the primary metrics.

**The Goodhart problem in practice:**
- "Resolve issues faster" → Agent rushes, quality drops
- "Increase throughput" → Agent takes shortcuts
- "Reduce escalations" → Agent handles things it shouldn't

```
## Health Metrics
While pursuing the outcomes above, these must not degrade:
- [METRIC] must stay [above/below] [THRESHOLD]
  → If trending wrong: [BEHAVIORAL ADJUSTMENT]
```

**Quality test:** For each desired outcome, ask "How could the agent achieve
this outcome in a way I'd hate?" The answer reveals your missing health metric.

### Section 5: Strategic Context

Where this agent sits in the larger system.

```
## Strategic Context
- System role: [WHERE THIS AGENT FITS]
- Upstream dependencies: [WHAT FEEDS INTO THIS AGENT]
- Downstream consumers: [WHO USES THIS AGENT'S OUTPUT]
- Business context: [RELEVANT STRATEGY OR CONSTRAINTS]
```

### Section 6: Constraints

Rules the agent must follow. Split into two categories based on WHERE
they are enforced.

**Steering Constraints (prompt layer — influence reasoning):**
```
## Steering Constraints
- Prefer [APPROACH A] over [APPROACH B] when [CONDITION]
- When uncertain, [DEFAULT BEHAVIOR]
```

**Hard Constraints (architecture layer — enforce compliance):**
```
## Hard Constraints (enforced in orchestration)
- Never [FORBIDDEN ACTION] — enforced via [MECHANISM]
- Rate limited to [N] [ACTIONS] per [TIME PERIOD]
```

**Decision rule:** If violating a constraint would cause real harm (data loss,
financial loss, security breach), it MUST be a hard constraint enforced
architecturally — not left in the prompt.

### Section 7: Decision Types & Autonomy

Which decisions the agent may take autonomously vs. must escalate. See the
Autonomy Levels section below for definitions mapped to this architecture.

```
## Decision Authority
### Full Autonomy
- [DECISION]: [WHY LOW RISK]

### Guarded Autonomy
- [DECISION]: [ROLLBACK MECHANISM]

### Proposal-First
- [DECISION]: [APPROVAL REQUIRED FROM]

### Human-Required (agent recommends only)
- [DECISION]: [WHY HUMAN MUST EXECUTE]
```

### Section 8: Edge Cases

Boundary conditions, failure modes, and ambiguous situations.

```
## Edge Cases
- When [UNUSUAL CONDITION]: [EXPECTED BEHAVIOR]
- When [SYSTEM FAILURE]: [FALLBACK BEHAVIOR]
- When [CONFLICTING REQUIREMENTS]: [PRIORITY ORDER]
```

Every unhandled edge case is a potential hallucination point. The agent will
invent behavior if you haven't defined it.

### Section 9: Stop Rules & Verification

When to halt, escalate, or declare completion.

```
## Stop Rules
### Halt immediately when:
- [CRITICAL CONDITION] → [ACTION: halt, alert, rollback]

### Escalate to human when:
- Confidence drops below [THRESHOLD]
- [N] consecutive failures

### Task is complete when:
- [COMPLETION CRITERIA]
- All verification checks pass

## Verification
- [AUTOMATED CHECK]: [WHAT IT VALIDATES]
```

---

## Autonomy Levels

Four levels mapped to this project's architecture. Assign based on blast radius
and reversibility.

| Level | Name | Description | Architecture | Example |
|-------|------|-------------|-------------|---------|
| 1 | **Full-Autonomous** | Agent acts without human involvement. Runs on schedule via launchd. | `agents-sdk/agents/*.py` with `config.toml` limits, `allowed_tools` whitelist | Daily Driver morning/evening/weekly modes |
| 2 | **Guarded-Autonomous** | Agent acts but with logging, thresholds, and rollback capability. | `agents-sdk/agents/*.py` with stricter limits, `record_run()` CSV tracking | Spending analysis, process-inbox (when enabled) |
| 3 | **Proposal-First** | Agent proposes actions, human approves before execution. Interactive mode. | Interactive Claude Code session, standard permission mode | jira-automation (creates tickets for review), prd-generator |
| 4 | **Human-Required** | Agent analyzes and recommends only. Human must execute. | Interactive Claude Code, `disallowedTools: [Write, Edit, Bash]` on agents | Design team review agents (UI Reviewer, Accessibility Checker) |

**Autonomy Risk Assessment — Five Lenses:**
1. **Blast radius:** How many systems/files are affected if this goes wrong?
2. **Reversibility:** Can the action be undone? How quickly?
3. **Confidence:** How certain is the agent about the right action?
4. **Precedent:** Has this type of decision been made successfully before?
5. **Visibility:** Will errors be caught quickly, or could they compound silently?

**Architecture mapping:**
- Full-Autonomous agents get `permission_mode: "acceptEdits"` and explicit `allowed_tools` whitelists
- Guarded-Autonomous agents add `record_run()` logging and lower `max_budget_usd`
- Proposal-First uses Claude Code's default interactive permission flow
- Human-Required uses `disallowedTools` deny-lists to structurally prevent writes

---

## Minimum Viable Retrofit (MVR) Guide

When retrofitting existing skills (there are 107 in `.claude/skills/`), don't
rewrite from scratch. Use leveled conversion to reduce regression risk.

### Level 1: Minimum Viable Intent (30 min per skill)

Add these three sections to the TOP of the existing skill, keeping original
instructions intact below:

1. **Objective** — What problem does this skill solve and why?
2. **Desired Outcomes** — What observable states indicate success? (2-3 outcomes)
3. **Stop Rules** — When should the agent halt, escalate, or declare done?

This is the highest-ROI change. It gives the agent judgment for edge cases
while preserving existing instructions.

If the agent runs autonomously via launchd, you MUST inject the Zero-Interaction
Mandate into the Stop Rules.

### Level 2: Structured Intent (2-4 hours per skill)

Add all Level 1 sections plus:
4. **Health Metrics** — What must not degrade?
5. **Constraints** — Split existing rules into Steering vs Hard
6. **Decision Authority** — Assign autonomy levels to key decisions
7. **Edge Cases** — Add 5+ boundary conditions

### Level 3: Full Conversion (4-8 hours per skill)

Complete rewrite using the full 9-section template. Existing instructions
are dissolved — the HOW is left to the agent.

### Prioritization for 107 Skills

Don't convert all at once. Prioritize by:
1. **Blast radius:** Skills touching production systems or external APIs → convert first
2. **Failure frequency:** Skills producing wrong outputs → convert next
3. **Autonomy level:** Skills for autonomous operation need full conversion; interactive-only skills → Level 1
4. **Complexity:** Simple single-task skills → Level 1. Multi-step workflows → Level 2 or 3

---

## The 5 Fatal Anti-Patterns

Flag these immediately when reviewing any agent or skill:

### 1. The Klarna "Intent Gap" (Missing Health Metrics)
The agent has a clear goal (e.g., "resolve tickets fast") but no counter-metric
to protect quality. This is the most documented enterprise failure mode.
**Fix:** Add a health metric that constrains how the primary outcome is achieved.

### 2. Prompt-Based Hard Constraints
Telling the LLM "never delete files" in a SKILL.md is insufficient. If deletion
is catastrophic, enforce it via `disallowedTools`, PreToolUse hooks returning
exit code 2, or filesystem permissions.
**Fix:** Map every "never do X" instruction to an architectural enforcement mechanism.

### 3. Activity vs. Outcome Confusion
Defining the goal as "run a Python script" (activity) instead of "the database
contains zero duplicate rows" (outcome).
**Fix:** Rewrite every goal using the pattern: "After the agent runs, [STATE] exists."

### 4. Vibe Coding the Edge Cases
Assuming the agent will "just figure out" what to do if an API is down or a
file is missing.
**Fix:** Enumerate 5+ edge cases with explicit fallback behaviors.

### 5. Infinite Loops (Missing Stop Rules)
Failing to define when the agent should give up and defer to the human.
**Fix:** Add halt conditions, escalation thresholds, and max-retry limits.

---

## Validation Checklist

Run this against every intent spec before shipping.

### Objective Quality
- [ ] States the problem, not the solution
- [ ] Includes "why it matters"
- [ ] Can guide trade-off decisions in ambiguous situations
- [ ] A new team member could read it and understand the purpose

### Outcome Quality
- [ ] All outcomes are states, not activities
- [ ] Outcomes are from user/stakeholder perspective
- [ ] 2-4 outcomes (not 1, not 10)
- [ ] Outcomes are measurable without agent self-report

### Health Metric Quality
- [ ] At least one health metric per desired outcome
- [ ] Addresses "How could the agent game this outcome?"
- [ ] Each metric includes a behavioral adjustment when trending wrong

### Constraint Quality
- [ ] Every harm-causing constraint is enforced architecturally
- [ ] Steering constraints are genuinely flexible guidance
- [ ] No constraint contradicts another

### Autonomy Quality
- [ ] Every decision type assigned to an autonomy level
- [ ] Assignments justified by blast radius and reversibility
- [ ] "Full Autonomy" items are genuinely low-risk and reversible

### Stop Rule Quality
- [ ] Halt conditions cover critical failures
- [ ] Escalation conditions include confidence thresholds
- [ ] At least one stop rule addresses the infinite loop case
- [ ] (For scheduled agents) Zero-Interaction Mandate is present

### Edge Case Quality
- [ ] Empty/null input handled
- [ ] Network/API failure handled
- [ ] Conflicting requirements have priority order
- [ ] At least 5 edge cases defined

---

## Domain Examples

### Example 1: PM Work — Education Course Creator

*Focus: Alignment to user value and strict verification.*

- **Objective:** Create education courses for a learning platform that teach
  complex concepts accessibly. Prioritize educational accuracy over content volume.
- **Desired Outcome:** Course page published with all required fields
  populated and SEO metadata generated per the platform's standards.
- **Health Metric:** Never publish content with unverified domain data
  or claims. If uncertain, flag with `[NEEDS REVIEW]` tags.
- **Stop Rule:** Halt if the ticket-tracker API rate limit is reached. Do not
  retry more than 3 times.
- **Hard Constraint:** All content changes require PR review before merge
  (enforced via GitHub branch protection, not prompt).

### Example 2: Creative — 16BitFit Sprite Pipeline

*Focus: Asset integrity and production throughput.*

- **Objective:** Process AI-generated sprites through the Pixel Purity Pipeline,
  ensuring Game Boy aesthetic compliance. Prioritize not blocking other pipeline
  stages over pixel-perfect optimization.
- **Desired Outcome:** All sprites meet 4-color palette, 8x8 grid alignment,
  and 160x144 viewport constraints. Pipeline has zero asset-blocking bottlenecks.
- **Health Metric:** Never modify original source sprites — always work on copies.
  Compression artifacts must stay below perceptual threshold.
- **Hard Constraint:** Read-only access to `creative-studio/sprites/source/`.
  Write only to `creative-studio/sprites/processed/` (enforced via directory
  scoping in `allowed_tools`).
- **Action Schema:** Output must match the animation-pipeline 12-stage QA gate
  format: `{stage, status: pass|warn|block, details}`.

### Example 3: Personal Productivity — Daily Driver Agent

*Focus: Data preservation and autonomous scheduling.*

- **Objective:** Synthesize yesterday's open tasks and today's calendar into a
  prioritized daily plan. Prioritize accurately capturing all hard-scheduled
  meetings over creatively brainstorming new tasks.
- **Desired Outcomes:**
  - A daily note exists at `vault/10_timeline/daily/YYYY-MM-DD.md` with 1-3-5 priorities
  - The note contains a schedule block from the user's primary Google Calendar
  - Carry-forward items from yesterday are captured
- **Health Metrics:**
  - Data Non-Destruction: Never overwrite existing text. Use PATCH at
    `<!-- claude-sessions -->` and `<!-- jira-log -->` anchors only.
  - Truth Anchoring: Do not hallucinate calendar events. If Calendar MCP fails,
    note `[ERROR: CALENDAR SYNC FAILED]` and continue.
- **Stop Rule:** ZERO-INTERACTION MANDATE. Running at 6:00 AM via launchd.
  No human available. If you cannot proceed, create error note and halt.
- **Execution Limits:** `max_turns: 15`, `max_budget_usd: 0.25` (from
  `config.toml [agents.daily_driver.modes.morning]`).

### Example 4: Financial — Spending Analysis

*Focus: Truth anchoring and categorization accuracy.*

- **Objective:** Give Sean clear visibility into where his money goes. Prioritize
  accuracy of categorization over speed of reporting.
- **Desired Outcome:** User can answer "where did my money go this month?" in
  under 30 seconds using the generated report in `vault/50_sources/finance/`.
- **Health Metrics:**
  - Categorization accuracy exceeds 95% (validated by 40+ Sean-specific regex
    merchant patterns from the personal-finance skill).
  - Never guess on ambiguous transactions — mark as "Uncategorized" and flag.
- **Hard Constraint:** Read-only access to bank CSVs. Cannot initiate transactions.
  Chase CSV format: Transaction Date, Post Date, Description, Category, Type,
  Amount, Memo. $5,741/mo net income baseline for anomaly detection.
- **Stop Rule:** Halt if CSV parse fails or data freshness > 7 days.

---

## How to Use This Skill

**When asked to write an intent spec:**
1. Ask clarifying questions about the domain, users, and failure modes
2. Draft using the full 9-section template
3. Run the Validation Checklist
4. Flag sections where you lack information

**When asked to review an intent spec:**
1. Run the Validation Checklist
2. Check for all 5 Fatal Anti-Patterns
3. Provide specific, actionable feedback per section

**When asked to retrofit an existing prompt/skill:**
1. Assess current state (prompt vs. partial intent spec)
2. Recommend conversion level (1, 2, or 3) based on blast radius and complexity
3. Perform the conversion at recommended level
4. Run the Validation Checklist on the result

**When asked to compare approaches or trade-offs:**
1. Frame comparison using the Objective as decision criteria
2. Evaluate options against Desired Outcomes
3. Check against Health Metrics and Constraints
4. Recommend based on the autonomy/risk framework

---

## Reference

For the blank YAML template with inline comments and a completed daily-driver
worked example, see `references/intent-spec-template.md`.
