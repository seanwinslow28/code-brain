---
name: intent-engineering
description: >
  Design, review, and retrofit intent specifications for AI agents and skills.
  Use when creating new agents, writing SKILL.md files, converting legacy prompts,
  debugging agent misalignment, or reviewing intent specs for quality. Also use
  when validating an intent spec before shipping, deciding which retrofit level
  is enough, or writing an improvement/fix spec for an existing skill.
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

That insight applies to this skill's own workflow. Every output this skill
produces opens with a declared **profile line** (see Right-Sizing Decision Rule)
and closes with a **Validation Verdict block** (see Validation Checklist). Those
two visible marks are the nearest thing a SKILL.md has to architectural
enforcement: they make a right-sized, validated spec detectably different from
an unvalidated one.

---

## Tooling & Canonical Source

Three local MCP tools automate this skill's core moves. **When they are mounted
in the session, the tool call is the default path**; the manual method in this
file is the explicit fallback when they're absent (the server is
user/plugin-scoped, not part of this repo — if a tool is missing, fall back to
the prose method, never stall).

| Tool | Call it when | Key parameters |
|------|--------------|----------------|
| `generate_intent_spec_scaffold` | Starting any new spec or retrofit conversion | `kind`: `blank` / `level-1-mvr` / `full-9-section`; optional `objective_hint`, `autonomy_level`, `agent_name` |
| `audit_intent_spec` | Every validation run — before any spec is called done | `file_path` OR `spec_text` (exactly one); paginates long input |
| `assess_retrofit_level` | Sizing a retrofit, or any right-sizing call in doubt | `file_path` OR `skill_text` (exactly one) |

`audit_intent_spec` returns a score out of 25, per-section findings, and top-3
recommendations. Hand-run reviews MUST adopt that same output shape, so any two
reviews of the same spec are comparable regardless of which path ran.

**Mirror warning (cross-repo coupling):** the 25 Validation Checklist items and
the 5 Fatal Anti-Patterns below are mirrored 1:1 as code in the shipped
`sw-mcp-intent-engineering` package (npm: `@swins/intent-engineering-mcp`) —
`src/intent/checklist.ts` carries stable item ids
(`objective.problem-not-solution` … `stop.zero-interaction-mandate` …
`edge.at-least-five`), `src/intent/anti-patterns.ts` the five anti-pattern ids,
and its scaffold templates mirror the 9 section names and order. That package's
README declares this SKILL.md the canonical source. Additive guidance *around*
the mirrored text (preambles, level tags, verdict semantics) is skill-only and
safe. **Any edit to checklist item wording, count, or meaning — or to the 9
section names/order — is a paired cross-repo change: make the matching
MCP-package edit, or file a ticket. Never fork silently.**

---

## The Unified 9-Section Intent Spec Template

A **full** intent spec includes all 9 sections. Sections 1-4 define *what* the
agent should achieve. Sections 5-9 define *how it should behave* at the
boundaries. The full form is mandatory for scheduled/autonomous agents and
high-blast-radius work; smaller jobs declare a smaller profile via the
Right-Sizing Decision Rule (MVR Guide below). Smaller profiles use a subset of
these sections — never renamed, never reordered (the names and order are
mirrored in shipped code; see Tooling & Canonical Source).

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
- Downstream consumers: [WHO USES THIS AGENT'S OUTPUT — and the exact SHAPE
  they expect: schema, format, section/tag vocabulary]
- Business context: [RELEVANT STRATEGY OR CONSTRAINTS]
```

Naming the consumer without pinning the shape is how "strong content, wrong
shape" ships and gets hand-reformatted forever. Pin the format the way Domain
Example 2 does with its Action Schema
(`{stage, status: pass|warn|block, details}`). If the shape is genuinely
unknown at spec time, write `shape: TBD — blocked on [CONSUMER]` — an explicit
unknown is a to-do; an omitted one is a seam.

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

**Preservation Constraints (What NOT to change — the third class):**
```
## Preservation Constraints (What NOT to Change)
- [WORKING THING]: protected because [WHY — e.g., mirrored in shipped code,
  consumers depend on its shape]
```

Mandatory on any fix/improvement/change spec for an existing system; greenfield
specs may write "N/A — greenfield," but the heading must be present. This is
what stops a weaker implementing model from "fixing" working parts out of
over-eagerness — and because it lives *inside* Section 6, it survives escalation
from the 4-element floor (see Right-Sizing Decision Rule) to the full template
without renumbering the sections that shipped code mirrors. Name the thing
*and* the reason it's protected; a bare list invites the next editor to treat
it as stale.

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

When retrofitting existing skills (the live inventory in `.claude/skills/` —
count it with `ls .claude/skills/ | wc -l`, never trust a hardcoded number),
don't rewrite from scratch. Use leveled conversion to reduce regression risk.

### Level 1: Minimum Viable Intent (30 min per skill)

Add these three sections to the TOP of the existing skill, keeping original
instructions intact below:

1. **Objective** — What problem does this skill solve and why?
2. **Desired Outcomes** — What observable states indicate success? (2-3 outcomes)
3. **Stop Rules** — When should the agent halt, escalate, or declare done?

This is the highest-ROI change. It gives the agent judgment for edge cases
while preserving existing instructions.

If the agent runs autonomously via launchd, you MUST inject the Zero-Interaction
Mandate into the Stop Rules — copy the canonical text below, never paraphrase it.

### The Zero-Interaction Mandate (canonical text)

Any spec for an agent that runs unattended (launchd, cron, headless SDK) carries
this block in its Stop Rules. Copy it verbatim and adapt only the bracketed
schedule/anchor specifics — never re-derive it from memory or a worked example.
A paraphrase that keeps "never ask" but drops the halt-and-error-note fallback
leaves the agent with no defined behavior at the exact moment it's stuck with
nobody watching.

```
ZERO-INTERACTION MANDATE: Never ask clarifying questions or prompt for input.
This agent runs unattended via [SCHEDULER — e.g., launchd at 6:00 AM]; no human
is available, and any prompt for input causes a silent timeout hang, not a
visible error. If you cannot proceed, write an error note at [ERROR ANCHOR —
e.g., <!-- agent-error -->] and halt.
```

The trigger is "runs unattended," not "is an agent" — interactive-only skills
do not inject it.

### Level 2: Structured Intent (2-4 hours per skill)

Add all Level 1 sections plus:
4. **Health Metrics** — What must not degrade?
5. **Constraints** — Split existing rules into Steering vs Hard
6. **Decision Authority** — Assign autonomy levels to key decisions
7. **Edge Cases** — Add 5+ boundary conditions

### Level 3: Full Conversion (4-8 hours per skill)

Complete rewrite using the full 9-section template. Existing instructions
are dissolved — the HOW is left to the agent.

### Right-Sizing Decision Rule (which level is enough?)

First match wins, top to bottom. This rule mirrors the decision logic shipped
in `assess_retrofit_level`, so the written rule and the tool cannot disagree —
when the tool is mounted, call it and paste its reasoning as your
justification; hand-apply this rule only when it isn't.

0. **Fix/improvement spec for an existing skill** (the skill-audit /
   zoom-out-and-think handoff) → the **4-element floor**: Objective, Desired
   Outcome, the fix per finding with reasoning, and What NOT to Change
   (Section 6 Preservation Constraints). Escalate to the full template only
   when the change alters autonomy, constraints, or a downstream contract.
   Rows 1-3 size new specs and retrofit conversions.
1. **Level 3 (full 9-section)** — high blast radius (irreversible-harm
   surfaces, usually compounding: destructive ops, money, production, secrets,
   outbound comms); OR scheduled/autonomous AND blast radius above low; OR the
   target already has 5+ of the 9 sections (finish the conversion — don't
   leave it hybrid).
2. **Level 2** — scheduled/autonomous with low blast radius; OR multi-step AND
   blast radius above low; OR medium blast radius; OR 3-4 sections already
   present.
3. **Level 1** — single-task, interactive, low blast radius.

Tie-breaks and overrides:
- When two rows both plausibly apply, take the heavier level — blast radius
  dominates convenience.
- A known history of wrong outputs escalates one level (failure history means
  you need the Health Metrics and Edge Cases that live at L2+; it's also an
  input the text-only tool can't see, so apply it yourself).
- Unattended at ANY level injects the canonical Zero-Interaction Mandate — the
  mandate is not what Level 3 is for.

**Declare it.** Every output opens with a profile line —
`Profile: Level 1 (MVR) — single-task interactive skill, low blast radius` —
chosen by this rule or pasted from `assess_retrofit_level`. The declared
profile is what the Validation Checklist scopes against; an undeclared profile
means all 25 items apply.

### Prioritization Across the Skill Inventory

Don't convert all at once. Prioritize by:
1. **Blast radius:** Skills touching production systems or external APIs → convert first
2. **Failure frequency:** Skills producing wrong outputs → convert next
3. **Autonomy level:** Skills for autonomous operation convert before interactive-only ones — size each with the Right-Sizing Decision Rule above
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

Run this against every intent spec before shipping — and running it has **gate
semantics**: it produces a Validation Verdict block appended to the emitted
spec, and a spec without a verdict block is not done. That visible mark is what
makes "nothing forced it to run" impossible to miss. The 25 items below are the
canonical standard and the hand-run fallback; they are mirrored as code (see
Tooling & Canonical Source), and when `audit_intent_spec` is mounted, the tool
run IS the checklist run.

**How to run it:**

1. **Route:** if the intent-engineering MCP tools are available, call
   `audit_intent_spec` on the draft and paste its score, per-section findings,
   and top-3 recommendations as the verdict block. Hand-walk the items only
   when the tool is absent.
2. **Scope by declared profile:** Level 1 runs the groups tagged *(all
   levels)* — Objective + Outcome + Stop Rule, 12 items. Level 2+ and full
   specs run all 25. The 4-element floor runs Objective + Outcome (its other
   two elements are governed by the consumer's contract, not this checklist).
   Scope by content present, floor by declared level: if a Level-1 spec
   voluntarily includes an Edge Cases section, validate that group too — but
   never validate below the declared level. This scoping is what lets an
   honest Level-1 retrofit PASS: out-of-scope groups are recorded as out of
   scope, not as 13 guaranteed failures that train you to ignore the gate.
3. **Failure semantics:** every failing in-scope item is either fixed before
   the spec is emitted or listed as `WAIVED: <one-line reason>`. Silence is
   the only forbidden state. If the user explicitly declines validation, emit
   `VALIDATION: SKIPPED (user request)` — the visible mark is the
   non-negotiable part, not the ceremony.
4. **No theater:** a verdict block generated without actually evaluating the
   items recreates the original unvalidated-spec failure one level down.
5. **Fragments:** when only one section is under discussion, the verdict block
   may cover just the touched groups — but must say so.

**Verdict block form:**

```
VALIDATION VERDICT — Profile: Level 1 (12/25 items in scope) — via audit_intent_spec [or: hand-run]
- Objective Quality: pass
- Outcome Quality: fail → "2-4 outcomes": had 6, trimmed to 4 — fixed
- Stop Rule Quality: pass (Zero-Interaction Mandate: canonical text copied)
- Out of scope (Level 1): Health Metric, Constraint, Autonomy, Edge Case
- Handoff rehearsal: "calendar API returns duplicate events" → Objective forced the right call: yes
```

### Objective Quality *(all levels)*
- [ ] States the problem, not the solution
- [ ] Includes "why it matters"
- [ ] Can guide trade-off decisions in ambiguous situations
- [ ] A new team member could read it and understand the purpose

### Outcome Quality *(all levels)*
- [ ] All outcomes are states, not activities
- [ ] Outcomes are from user/stakeholder perspective
- [ ] 2-4 outcomes (not 1, not 10)
- [ ] Outcomes are measurable without agent self-report

### Health Metric Quality *(Level 2+)*
- [ ] At least one health metric per desired outcome
- [ ] Addresses "How could the agent game this outcome?"
- [ ] Each metric includes a behavioral adjustment when trending wrong

### Constraint Quality *(Level 2+)*
- [ ] Every harm-causing constraint is enforced architecturally
- [ ] Steering constraints are genuinely flexible guidance
- [ ] No constraint contradicts another

### Autonomy Quality *(Level 2+)*
- [ ] Every decision type assigned to an autonomy level
- [ ] Assignments justified by blast radius and reversibility
- [ ] "Full Autonomy" items are genuinely low-risk and reversible

### Stop Rule Quality *(all levels)*
- [ ] Halt conditions cover critical failures
- [ ] Escalation conditions include confidence thresholds
- [ ] At least one stop rule addresses the infinite loop case
- [ ] (For scheduled agents) Zero-Interaction Mandate is present with the
      halt-and-error-note fallback
<!-- PAIRED-MCP-CHANGE: the mirrored item `stop.zero-interaction-mandate` in
     sw-mcp-intent-engineering src/intent/checklist.ts still reads
     "…Mandate is present"; its description must gain "with the
     halt-and-error-note fallback" in the next MCP release. -->

### Edge Case Quality *(Level 2+)*
- [ ] Empty/null input handled
- [ ] Network/API failure handled
- [ ] Conflicting requirements have priority order
- [ ] At least 5 edge cases defined

### The Handoff Rehearsal (pre-emit)

Per-section checks can all pass while the spec still fails the first situation
nobody enumerated — and the bar is a spec that survives planner → implementer →
subagent handoffs with zero intent drift. So before emitting:

1. Invent one plausible edge case the spec does NOT enumerate.
2. Ask: would the Objective and Constraints alone force a weaker model to the
   right call?
3. If not, strengthen the Objective's trade-off line — not the edge-case list.
   The list can never be complete; the Objective is the designed fallback when
   instructions run out. Re-test once.
4. Record the rehearsal case and result in the verdict block.

One rehearsal case, one strengthening pass. If the spec fails a second fresh
case, the Objective is wrong, not under-written — go back to grounding instead
of iterating wordsmithing.

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
  Amount, Memo. Net-income baseline for anomaly detection comes from the local profile.
- **Stop Rule:** Halt if CSV parse fails or data freshness > 7 days.

### Example 5: Fix Spec for an Existing Skill (4-element floor)

*Focus: right-sized ceremony — the shape skill-audit and zoom-out-and-think
hand off. Most incoming jobs look like this, not like Examples 1-4.
(Hypothetical fix, real shape.)*

- **Profile:** 4-element floor — fix spec; the change alters no autonomy,
  constraint, or downstream contract.
- **Objective:** meeting-prep builds agendas from calendar data fetched once,
  so a meeting moved after the fetch shows a confidently wrong time. Fix the
  staleness seam. Trade-off: prefer a visibly incomplete agenda over a
  silently stale one.
- **Desired Outcome:** Every agenda states its fetch timestamp; a post-fetch
  reschedule surfaces as `[STALE — refetch]`, never as a wrong time stated
  with confidence.
- **The fix, per finding:** Add a fetch-timestamp line to the agenda header
  and a staleness check before emit. Reasoning a weaker model needs: the
  failure mode is silent confidence, so the fix is *visibility* — not retry
  logic, which an unattended run can't supervise.
- **What NOT to change (preservation):** the agenda section order — the
  daily-note injection anchors on those headings.
- **Verdict block:** `Profile: floor (Objective + Outcome in scope) — hand-run
  — Objective: pass; Outcome: pass; rehearsal: "meeting deleted after fetch"
  → Objective forces the [STALE] marker: yes.`

---

## How to Use This Skill

Every mode opens its output with the declared profile line and closes with the
Validation Verdict block — the two marks that make a right-sized, validated
spec distinguishable from an unvalidated one.

**When asked to write an intent spec:**
1. Gather grounding: ask clarifying questions about the domain, users, and
   failure modes. If the answers are already supplied (pre-pinned context, a
   headless or subagent invocation with no reachable user), restate them and
   proceed without asking — an unconditional "ask first" in a zero-interaction
   context either hangs the run or gets silently skipped.
2. Restate the answers and confirm your understanding before drafting.
3. Right-size: declare the profile (Right-Sizing Decision Rule, or
   `assess_retrofit_level` when in doubt), then scaffold with
   `generate_intent_spec_scaffold` using the matching `kind` — or copy the
   template manually when the tools are absent.
4. Draft. The Objective's trade-off line and every Health Metric must be
   traceable to the step-1 answers — pulled from them, never invented.
5. Flag what you don't know as `[GAP: <what's unknown> — <which section it
   blocks>]` instead of inventing an answer to fill space. If no user is
   reachable, emit with the GAP flags in place.
6. Run the Handoff Rehearsal.
7. Validate — `audit_intent_spec`, or hand-run scoped to the declared
   profile — and append the verdict block. Do not emit a spec without it.

**When asked to review an intent spec:**
1. Run `audit_intent_spec` when mounted; otherwise hand-run the checklist in
   the tool's output shape (score /25, per-section findings, top-3
   recommendations) so any two reviews of the same spec are comparable.
2. Check for all 5 Fatal Anti-Patterns.
3. Provide specific, actionable feedback per section and append the verdict
   block — a review without a verdict is an opinion, not a review.

**When asked to retrofit an existing prompt/skill:**
1. Assess current state: call `assess_retrofit_level` and paste its reasoning
   as your justification, or hand-apply the Right-Sizing Decision Rule.
2. Declare the profile line.
3. Perform the conversion at that level. If the target runs unattended, copy
   the canonical Zero-Interaction Mandate into its Stop Rules — verbatim,
   adapting only the bracketed specifics.
4. Run the Validation Checklist scoped to the declared level and append the
   verdict block.
5. Run the Handoff Rehearsal on the result and record it in the verdict block.

**When asked to compare approaches or trade-offs:**
1. Frame comparison using the Objective as decision criteria
2. Evaluate options against Desired Outcomes
3. Check against Health Metrics and Constraints
4. Recommend based on the autonomy/risk framework

---

## Reference

For the blank YAML template with inline comments and a completed daily-driver
worked example, see `references/intent-spec-template.md`. When the MCP tools
are mounted, `generate_intent_spec_scaffold` returns the same templates
programmatically — same content, zero hand-copying.
