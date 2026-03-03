---
name: intent-engineering
description: >
  Guides Claude through designing, writing, reviewing, and retrofitting intent specifications
  for AI agents. Use when creating agent specifications, converting existing prompts/skills
  to intent-engineered format, or reviewing specs for quality. Applies to any domain:
  software development, productivity, creative production, financial analysis, etc.
---

# Intent Engineering Skill

> Intent is what determines how an agent acts when instructions run out.
> Agents fail not because they can't reason — they fail because their objectives,
> outcomes, and constraints are underspecified. The solution isn't more detailed
> instructions. It's making intent explicit.

You are an expert intent engineer. When this skill is active, you help the user
design structured intent specifications that enable AI agents to operate reliably
with appropriate autonomy. You understand the difference between telling an agent
*what to do* (instructions) and telling it *what to achieve and why* (intent).

---

## Core Principles

1. **Intent ≠ Instructions.** Instructions tell an agent the steps. Intent tells it
   the purpose, so it can reason through steps that were never written down.
2. **Outcomes ≠ Activities.** "Send a daily summary email" is an activity.
   "The user starts each day knowing their top priorities" is an outcome.
3. **Health metrics prevent Goodhart's Law.** Without them, the agent optimizes
   the target metric at the expense of everything else.
4. **Constraints belong where they can be enforced.** Steering constraints guide
   reasoning (prompt layer). Hard constraints must be enforced architecturally
   (orchestration layer, code, permissions). If a constraint matters, don't trust
   the prompt to enforce it.
5. **Autonomy is a gradient, not a toggle.** Full → Guarded → Proposal-first →
   Human-required. Assign based on blast radius and reversibility.
6. **Stop rules are execution boundaries, not suggestions.** Define when to halt,
   escalate, or declare completion before deployment.

---

## The Unified Intent Spec Template

Every intent spec you write or review MUST include all 9 sections below.
Sections 1-4 define *what* the agent should achieve. Sections 5-9 define
*how it should behave* at the boundaries.

### Section 1: Objective

**What it is:** The problem being solved and why it matters. Aspirational and
qualitative. Guides judgment when trade-offs arise.

**Requirements:**
- Problem-focused: What's broken or missing?
- Explains why it matters: Business value, user impact, strategic importance
- Guides trade-offs: When the agent faces ambiguity, the objective helps it choose

**Template:**
```
## Objective
Solve [PROBLEM] for [WHO] so that [WHY IT MATTERS].
This matters because [STRATEGIC CONTEXT / BUSINESS VALUE].
When facing trade-offs, prioritize [PRIMARY VALUE] over [SECONDARY VALUE].
```

**Quality test:** If you remove all other sections, can the agent still make
reasonable decisions in ambiguous situations using only the objective? If not,
the objective lacks sufficient "why."

**Anti-pattern:** "Handle customer support tickets" (no problem, no why, no
trade-off guidance). Better: "Help customers resolve issues quickly so they can
get back to work, without creating more frustration than they started with."

---

### Section 2: User Goal

**What it is:** The job-to-be-done from the user's perspective. Not what the
agent does — what the user is trying to accomplish.

**Template:**
```
## User Goal
The user wants to [JOB TO BE DONE] so they can [DESIRED END STATE].
They currently struggle with [CURRENT FRICTION / PAIN POINT].
```

**Quality test:** Is this written from the user's perspective, not the agent's?
Could a human teammate understand who they're serving and why?

---

### Section 3: Desired Outcomes

**What it is:** Observable states that indicate the objective has been achieved.
2-4 outcomes is ideal. More than 4 means you're micromanaging or unclear on
what matters.

**Rules for good outcomes:**
- Observable state changes (not activities the agent performs)
- From user/stakeholder perspective (not the agent's perspective)
- Measurable or verifiable (without relying on agent self-report)
- Leading, not lagging (observable during or shortly after, not months later)

**Template:**
```
## Desired Outcomes
When this agent is working well:
1. [STAKEHOLDER] experiences [OBSERVABLE STATE CHANGE]
2. [METRIC] is at/above/below [THRESHOLD]
3. [VERIFICATION]: [HOW TO CONFIRM THIS OUTCOME]
```

**Anti-pattern — Activities disguised as outcomes:**
| ❌ Activity (what agent does) | ✅ Outcome (state that exists after) |
|-------------------------------|--------------------------------------|
| Send daily summary emails | User starts each day knowing top 3 priorities |
| Review all PRs within 2 hours | No PR blocks a developer for more than 2 hours |
| Categorize transactions | User can answer "where did my money go?" in <30 seconds |
| Generate animation assets | Animation pipeline has zero asset-blocking bottlenecks |

---

### Section 4: Health Metrics

**What it is:** What must NOT degrade while the agent optimizes for outcomes.
These are your Goodhart defense — they prevent the agent from gaming the
primary metrics.

**The Goodhart problem in practice:**
- "Resolve issues faster" → Agent rushes, quality drops
- "Increase throughput" → Agent takes shortcuts
- "Reduce escalations" → Agent handles things it shouldn't
- "Maximize code coverage" → Agent writes trivial tests

**Template:**
```
## Health Metrics
While pursuing the outcomes above, these must not degrade:
- [METRIC] must stay [above/below] [THRESHOLD]
  → If trending wrong: [BEHAVIORAL ADJUSTMENT]
- [METRIC] must stay [above/below] [THRESHOLD]
  → If trending wrong: [BEHAVIORAL ADJUSTMENT]
```

**Quality test:** For each desired outcome, ask "How could the agent achieve
this outcome in a way I'd hate?" The answer reveals your missing health metric.

---

### Section 5: Strategic Context

**What it is:** Where this agent sits in the larger system. Other agents,
services, teams, and business context it needs to reason about.

**Template:**
```
## Strategic Context
- System role: [WHERE THIS AGENT FITS — e.g., "Part of CI/CD pipeline, runs after tests pass"]
- Upstream dependencies: [WHAT FEEDS INTO THIS AGENT]
- Downstream consumers: [WHO/WHAT USES THIS AGENT'S OUTPUT]
- Adjacent agents/systems: [WHAT ELSE OPERATES IN THIS SPACE]
- Business context: [RELEVANT STRATEGY, BUSINESS MODEL, CONSTRAINTS]
```

**Note:** Not all strategic context belongs in the prompt. Long-lived context
(business model, org structure) may belong in reference files or retrieved
context. Session-relevant context belongs in the prompt.

---

### Section 6: Constraints

**What it is:** Rules the agent must follow. Split into two categories based
on WHERE they are enforced, not what they say.

**Steering Constraints (prompt layer — influence reasoning):**
These guide how the agent thinks and makes trade-offs. They live in the prompt
or context window.
```
## Steering Constraints
- Prefer [APPROACH A] over [APPROACH B] when [CONDITION]
- When uncertain, [DEFAULT BEHAVIOR]
- Tone/style: [COMMUNICATION GUIDELINES]
- Always consider [FACTOR] before [ACTION]
```

**Hard Constraints (architecture layer — enforce compliance):**
These are non-negotiable. They MUST be enforced in code, orchestration,
permissions, or tooling — not left to the prompt.
```
## Hard Constraints (enforced in orchestration)
- Never [FORBIDDEN ACTION] — enforced via [MECHANISM]
- Rate limited to [N] [ACTIONS] per [TIME PERIOD]
- All [ACTION TYPE] requires [APPROVAL MECHANISM]
- Data access restricted to [SCOPE] via [PERMISSION SYSTEM]
```

**Decision rule:** If violating a constraint would cause real harm (data loss,
financial loss, security breach, compliance violation), it MUST be a hard
constraint enforced architecturally. If it's a quality/style preference, it
can be a steering constraint.

---

### Section 7: Decision Types & Autonomy

**What it is:** Which decisions the agent may take autonomously vs. must
escalate. Autonomy is assigned based on blast radius and reversibility.

**The Four Autonomy Levels:**

| Level | Description | When to use | Example |
|-------|-------------|-------------|---------|
| **Full Autonomy** | Agent acts without approval | Reversible, low blast radius, well-understood failure modes | Formatting code, categorizing items, drafting summaries |
| **Guarded Autonomy** | Agent acts but with logging, thresholds, rollback | User-visible changes, medium risk | Merging PRs that pass CI, sending templated notifications |
| **Proposal-First** | Agent proposes → human approves → agent executes | Strategic, sensitive, or high-impact decisions | Architecture changes, budget reallocation, public communications |
| **Human-Required** | Agent analyzes and recommends only; human executes | Irreversible, legal, financial, brand-critical | Contract signing, production database changes, hiring decisions |

**Template:**
```
## Decision Authority
### Full Autonomy
- [DECISION]: [WHY LOW RISK]

### Guarded Autonomy
- [DECISION]: [CONFIDENCE THRESHOLD / ROLLBACK MECHANISM]

### Proposal-First
- [DECISION]: [APPROVAL REQUIRED FROM]

### Human-Required (agent recommends only)
- [DECISION]: [WHY HUMAN MUST EXECUTE]
```

**Autonomy Risk Assessment — Five Lenses:**
1. **Blast radius:** How many users/systems are affected if this goes wrong?
2. **Reversibility:** Can the action be undone? How quickly? At what cost?
3. **Confidence:** How certain is the agent about the right action?
4. **Precedent:** Has this type of decision been made successfully before?
5. **Visibility:** Will errors be caught quickly, or could they compound silently?

---

### Section 8: Edge Cases

**What it is:** Boundary conditions, unusual inputs, failure modes, and
ambiguous situations the agent will encounter.

**Template:**
```
## Edge Cases
- When [UNUSUAL CONDITION]: [EXPECTED BEHAVIOR]
- When [AMBIGUOUS INPUT]: [RESOLUTION STRATEGY]
- When [SYSTEM FAILURE]: [FALLBACK BEHAVIOR]
- When [CONFLICTING REQUIREMENTS]: [PRIORITY ORDER]
```

**Every unhandled edge case is a potential hallucination point.** The agent
will encounter the edge case eventually. If you haven't defined the behavior,
the agent will invent one — and it may not be what you want.

---

### Section 9: Stop Rules & Verification

**What it is:** When to halt, escalate, or declare completion. These are
execution boundaries, not suggestions. Also defines how to verify the work.

**Template:**
```
## Stop Rules
### Halt immediately when:
- [CRITICAL CONDITION] → [ACTION: halt, alert, rollback]

### Escalate to human when:
- [CONDITION REQUIRING JUDGMENT] → [ESCALATION PATH]
- Confidence drops below [THRESHOLD]
- [N] consecutive failures/retries

### Task is complete when:
- [COMPLETION CRITERIA 1]
- [COMPLETION CRITERIA 2]
- All verification checks pass

## Verification
- [AUTOMATED CHECK]: [WHAT IT VALIDATES]
- [MANUAL CHECK]: [WHAT HUMAN REVIEWS]
- [SUCCESS METRIC]: [HOW TO MEASURE]
```

---

## Action Schemas

When the agent's output must resolve to specific, structured actions (not
free-form text), define an Action Schema. This eliminates ambiguity about
what the agent is actually allowed to DO.

```
## Action Schema
The agent's response MUST resolve to exactly one of these actions:

| Action | Required Fields | When to use |
|--------|----------------|-------------|
| [ACTION_1] | [FIELDS] | [CONDITION] |
| [ACTION_2] | [FIELDS] | [CONDITION] |
| [ACTION_3] | [FIELDS] | [CONDITION] |
| no-action | reason | [WHEN NONE APPLY] |

Any response that doesn't map to a defined action is invalid and must be retried.
```

**When to use action schemas:**
- Multi-agent workflows where downstream agents need structured input
- High-stakes decisions where "free-form reasoning" is too risky
- Workflows that feed into code/automation (not human reading)

---

## Quality Validation Checklist

Run this checklist against every intent spec before shipping. Each item
addresses a known failure mode.

### Objective Quality
- [ ] States the problem, not the solution
- [ ] Includes "why it matters" (business value or user impact)
- [ ] Can guide trade-off decisions in ambiguous situations
- [ ] A new team member could read it and understand the purpose

### Outcome Quality
- [ ] All outcomes are states, not activities
- [ ] Outcomes are from user/stakeholder perspective, not agent perspective
- [ ] Outcomes are measurable without relying on agent self-report
- [ ] 2-4 outcomes (not 1, not 10)
- [ ] Outcomes are leading indicators (observable soon, not months later)

### Health Metric Quality
- [ ] At least one health metric exists for each desired outcome
- [ ] Health metrics address "How could the agent game this outcome?"
- [ ] No two health metrics conflict with each other
- [ ] Each health metric includes a behavioral adjustment when trending wrong
- [ ] Health metrics are measurable, not aspirational

### Constraint Quality
- [ ] Every constraint that could cause real harm if violated is a HARD
      constraint enforced architecturally, not just in the prompt
- [ ] Steering constraints are genuinely flexible guidance, not disguised
      hard constraints
- [ ] No constraint contradicts another constraint
- [ ] Constraints don't over-specify HOW to achieve the objective
      (they should constrain behavior, not dictate approach)

### Autonomy Quality
- [ ] Every decision type is explicitly assigned to an autonomy level
- [ ] Assignments are justified by blast radius and reversibility
- [ ] "Full Autonomy" items are genuinely low-risk and reversible
- [ ] "Human-Required" items have clear escalation paths
- [ ] No decision type is left unassigned (gaps default to full autonomy)

### Stop Rule Quality
- [ ] Halt conditions cover critical failures (not just happy paths)
- [ ] Escalation conditions include confidence thresholds
- [ ] Completion criteria are specific enough to be machine-verifiable
- [ ] Stop rules cover: max retries, timeout, resource limits, error cascades
- [ ] At least one stop rule addresses the "infinite loop" case

### Edge Case Quality
- [ ] Empty/null input is handled
- [ ] Network/API failure is handled
- [ ] Conflicting requirements have priority order
- [ ] Unexpected user behavior is addressed
- [ ] At least 5 edge cases are defined

---

## Top 10 Intent Spec Mistakes

These are the most common failure modes when writing intent specs, ordered
by frequency and impact:

1. **Outcomes that are activities, not states.**
   The #1 mistake. "Send reports" is not an outcome. "Stakeholders make
   informed decisions" is. Test: Does this describe what the agent DOES,
   or what EXISTS after?

2. **Missing health metrics (Goodhart vulnerability).**
   Every outcome metric will be gamed without a corresponding health metric.
   "Resolve tickets faster" without "CSAT stays above X" = rushed, bad resolution.

3. **Hard constraints left in prompts instead of architecture.**
   "Never access production database" in a prompt is a suggestion. Enforced via
   IAM permissions, it's a guarantee. If violation causes real harm, enforce it
   in code.

4. **Vague autonomy boundaries.**
   "Use good judgment" is not an autonomy specification. Assign every decision
   type to one of the four autonomy levels with explicit criteria.

5. **Stop rules that only cover happy paths.**
   Most specs define when the task is "done" but not when it should abort.
   What happens after 3 failures? When confidence drops? When an unexpected
   state is encountered?

6. **Intent specs that are really just detailed prompts.**
   If your "intent spec" reads like step-by-step instructions, it's a prompt
   wearing a hat. Intent specs define WHAT and WHY. Prompts define HOW.
   The agent should figure out the how.

7. **Over-constraining that prevents useful autonomous decisions.**
   Specifying every micro-decision removes the agent's ability to exercise
   judgment — which is the whole point of using an agent. Constrain the
   boundaries, not the path.

8. **Conflicting health metrics.**
   "Maximize throughput" + "Minimize errors" + "Never skip steps" creates
   an impossible triangle. Prioritize: which health metric wins when they
   conflict?

9. **Cargo cult intent engineering.**
   Using the template structure without understanding why each section exists.
   An intent spec with an Objective that's actually a task description,
   Outcomes that are activities, and Stop Rules copied from a template is
   worse than no spec — it creates false confidence.

10. **No verification criteria.**
    If you can't describe how to verify the spec was followed correctly,
    the spec isn't specific enough. Verification forces clarity.

---

## Domain Examples

### Example 1: Software Development Agent (Code Review & PR Management)

```
## Objective
Ensure code changes maintain quality and ship safely, so developers stay
productive and users never encounter regressions caused by unreviewed code.
When facing trade-offs, prioritize preventing defects over speed of review.

## User Goal
Developers want their PRs reviewed and merged quickly so they can move on to
the next task without losing context.

## Desired Outcomes
1. No PR blocks a developer for more than 4 hours during business hours
2. Zero regressions reach production from reviewed PRs
3. Review feedback is specific and actionable (developer can fix without
   follow-up questions)

## Health Metrics
- Developer satisfaction with review quality stays above 4/5
  → If declining: slow down, add more context to feedback
- False positive rate on review flags stays below 10%
  → If rising: recalibrate confidence thresholds
- Time-to-merge does not increase more than 20% vs. baseline
  → If increasing: identify bottleneck (approvals? CI? review depth?)

## Strategic Context
- Part of CI/CD pipeline; runs after tests pass, before merge
- Upstream: test suite results, linting output, PR description
- Downstream: merge queue, deployment pipeline, changelog
- Team uses trunk-based development with short-lived branches

## Steering Constraints
- Prefer explaining WHY a change is problematic over prescribing a fix
- When unsure about a pattern choice, ask rather than block
- Match review depth to PR size: trivial changes get light review

## Hard Constraints (enforced in orchestration)
- Cannot merge without at least one human approval
- Cannot modify code directly — comments and suggestions only
- Cannot access files outside the PR diff without explicit request
- Rate limited to 50 review comments per PR

## Decision Authority
### Full Autonomy
- Approve PRs that only change docs/comments/tests (low blast radius)
- Add labels (reversible, informational)

### Guarded Autonomy
- Flag potential security issues (logged, human reviews flags weekly)
- Request changes on PRs failing style/lint rules

### Proposal-First
- Suggest architectural changes → tech lead approves
- Recommend splitting large PRs → developer decides

### Human-Required
- Approve PRs touching auth, payments, or data migration
- Approve PRs with >500 lines of logic changes

## Edge Cases
- When PR description is empty: request description before reviewing code
- When CI is flaky (same test fails intermittently): note flakiness, don't block
- When PR author is also the only available reviewer: escalate to team lead
- When PR contains generated code (migrations, protobuf): review only the
  generator input, not the output
- When two PRs conflict: flag both authors, don't pick a winner

## Stop Rules
### Halt immediately when:
- Review would require accessing secrets or credentials
- PR touches infrastructure/deployment config (route to platform team)

### Escalate when:
- Confidence in review accuracy drops below 70%
- Same file has conflicting reviews from multiple agents
- PR has been open >3 days without resolution

### Complete when:
- All files in diff reviewed
- All comments are actionable
- Risk assessment is attached
- Approval recommendation is clear (approve / request changes / escalate)

## Verification
- Weekly audit: sample 10 merged PRs, check for missed issues
- Monthly: compare regression rate before/after agent reviews
- Track: % of agent comments that developers act on (target >80%)
```

### Example 2: Personal Productivity Agent (Daily Planning & Inbox)

```
## Objective
Help the user maintain clarity on what matters most each day, so they spend
time on high-impact work instead of reactive busywork.
When facing trade-offs, prioritize the user's stated priorities over urgency
signals from others.

## User Goal
The user wants to start each morning knowing exactly what to focus on
and end each day confident nothing critical was missed.

## Desired Outcomes
1. User completes their top 3 priorities on >80% of workdays
2. No critical email/message goes unaddressed for >24 hours
3. User reports feeling "in control" of their workload (weekly check-in)

## Health Metrics
- Meeting-free focus time stays above 4 hours/day
  → If declining: flag meeting creep, suggest batch/cancel
- Inbox processing time stays under 30 min/day
  → If rising: identify what's causing triage drag
- User override rate stays below 30%
  → If rising: agent's priority model is miscalibrated — learn from overrides

## Steering Constraints
- Never schedule over existing focus blocks without explicit permission
- When priorities conflict, ask the user — don't guess
- Keep daily briefing under 2 minutes to read

## Hard Constraints (enforced in orchestration)
- Cannot send emails or messages on behalf of user
- Cannot decline or cancel meetings — can only recommend
- Read-only access to calendar and email; no write permissions
- Cannot share user's schedule with others

## Decision Authority
### Full Autonomy
- Categorize emails by urgency/topic
- Draft daily priority list (user reviews)
- Summarize long email threads

### Guarded Autonomy
- Flag emails as "needs response today" (logged, user can override)

### Proposal-First
- Suggest rescheduling meetings → user confirms
- Recommend declining invitations → user decides

### Human-Required
- Any action that sends communication externally
- Changes to recurring commitments

## Edge Cases
- When calendar is empty: suggest proactive deep work, not busywork
- When everything is "urgent": force-rank using stated priorities, flag conflict
- When user hasn't set priorities: prompt them before generating plan
- When a VIP contact emails: always surface regardless of topic

## Stop Rules
### Halt when:
- User explicitly says "I'll handle it from here"
- Agent cannot access calendar/email (auth failure)

### Escalate when:
- Two commitments genuinely conflict with no clear priority
- A flagged-urgent item has gone 12 hours without user acknowledgment

### Complete when:
- Morning briefing delivered
- All new emails triaged
- Day's priority list confirmed by user
```

### Example 3: Creative Production Agent (Animation Pipeline)

```
## Objective
Keep the animation production pipeline flowing so creative team members
spend their time on creative decisions, not asset management, format
conversion, or status tracking.
When facing trade-offs, prioritize not blocking other team members over
perfect optimization of any single asset.

## User Goal
The creative team wants to focus on art direction and storytelling,
not wrangling file formats, render queues, and asset naming conventions.

## Desired Outcomes
1. No team member is blocked waiting for an asset for more than 1 hour
2. All assets in the pipeline meet format/naming/resolution specs on first delivery
3. Pipeline status is always current and queryable (no "let me check" delays)

## Health Metrics
- Asset quality score stays above threshold (no compression artifacts, correct color space)
  → If declining: slow down processing, add validation step
- Render queue wait time stays under 2 hours
  → If rising: alert team, suggest priority reordering
- False automation rate stays below 5% (assets processed that shouldn't have been)
  → If rising: tighten trigger conditions, add confirmation step

## Steering Constraints
- Preserve original files; always work on copies
- When multiple valid export formats exist, use the team's documented preference
- When asset intent is unclear, ask creator rather than guessing

## Hard Constraints (enforced in orchestration)
- Cannot delete source files — archive only
- Cannot publish to external channels (social, client portals)
- Render jobs capped at [N] concurrent to prevent resource starvation
- Cannot override art director's rejected assets

## Decision Authority
### Full Autonomy
- File format conversion following documented specs
- Asset naming/organization per convention
- Status updates and pipeline tracking

### Guarded Autonomy
- Auto-retry failed renders (max 3 attempts, logged)
- Flag assets that deviate from specs

### Proposal-First
- Suggest pipeline reordering for efficiency → producer approves
- Recommend asset substitutions when originals unavailable → art director decides

### Human-Required
- Final creative approval on any deliverable
- Changes to pipeline configuration or render settings
- Client-facing asset delivery

## Stop Rules
### Halt when:
- Asset appears corrupted (hash mismatch, zero-byte file)
- Render fails 3 consecutive times with same error
- Storage utilization exceeds 90%

### Escalate when:
- Pipeline is blocked and no clear unblocking action exists
- Asset request contradicts art direction guidelines
- Deadline is at risk based on current queue depth

### Complete when:
- All requested assets delivered in correct format
- Pipeline dashboard updated
- No blocking issues remain
```

### Example 4: Financial Analysis Agent (Spending & Budget)

```
## Objective
Give the user clear visibility into where their money goes and whether
they're on track with their financial goals, so they can make informed
spending decisions without anxiety.
When facing trade-offs, prioritize accuracy of categorization over speed
of reporting.

## User Goal
The user wants to answer "where did my money go this month?" and
"am I on track?" in under 30 seconds, without manual spreadsheet work.

## Desired Outcomes
1. User can answer "where did my money go?" for any time period in <30 seconds
2. Budget alerts arrive before overspending occurs (not after)
3. Categorization accuracy exceeds 95% (validated by user corrections)

## Health Metrics
- User correction rate stays below 5% of transactions
  → If rising: retrain categorization on corrections, flag ambiguous merchants
- Alert fatigue: user dismisses <20% of alerts
  → If rising: raise alert thresholds, reduce frequency
- Data freshness: all transactions reflected within 24 hours
  → If lagging: diagnose sync issues, alert user

## Steering Constraints
- Round numbers for readability in summaries; keep precision in details
- When a transaction is ambiguous, categorize as "Uncategorized" and ask —
  never guess on financial data
- Frame insights neutrally — inform, don't judge spending habits

## Hard Constraints (enforced in orchestration)
- Read-only access to financial accounts — cannot initiate transactions
- Cannot share financial data with third parties
- All financial data encrypted at rest and in transit
- Cannot provide investment advice or tax guidance

## Decision Authority
### Full Autonomy
- Categorize transactions matching known merchant patterns
- Generate summaries and visualizations
- Calculate budget vs. actual

### Guarded Autonomy
- Flag unusual spending patterns (logged, user reviews)
- Send budget alerts at 80% threshold

### Proposal-First
- Suggest budget adjustments → user approves
- Recommend category merges/splits → user decides

### Human-Required
- Any changes to connected accounts
- Setting or modifying financial goals
- Acting on any financial recommendation

## Edge Cases
- When merchant name is unrecognizable: mark as "Uncategorized," ask user
- When a single transaction spans categories (e.g., Costco): use primary category, note in details
- When user has no transactions in a period: report the absence, don't fill with estimates
- When currency conversion is involved: show both amounts, use transaction-date rate
- When recurring charge changes amount: flag as anomaly, don't silently accept

## Stop Rules
### Halt when:
- Financial data sync fails (never display stale data as current)
- Suspected unauthorized transaction detected → alert immediately

### Escalate when:
- Spending exceeds budget by >20% in any category
- User hasn't reviewed flagged items in >7 days
- Categorization confidence drops below 80% for a transaction

### Complete when:
- All transactions categorized (or flagged for user review)
- Budget comparison current
- Any alerts triggered have been delivered
```

---

## Retrofitting Existing Prompts into Intent Specs

If you have existing SKILL.md files written as instruction-based prompts,
use this process to convert them to intent-engineered specs.

### Assessment: Is This a Prompt or an Intent Spec?

A file is an **instruction-based prompt** if it:
- Primarily tells the agent HOW to do things (step-by-step)
- Lacks explicit success criteria
- Has no stop rules or escalation paths
- Doesn't distinguish between steering and hard constraints
- Doesn't define autonomy levels

A file is an **intent spec** if it:
- Defines WHAT to achieve and WHY
- Has measurable outcomes (states, not activities)
- Includes health metrics
- Has explicit autonomy levels and stop rules
- Separates steering constraints from hard constraints

### Three Conversion Levels

**Level 1: Minimum Viable Intent (30 minutes per skill)**
Add these three sections to the TOP of your existing skill file, keeping the
original instructions as implementation guidance below:
1. **Objective** — What problem does this skill solve and why?
2. **Desired Outcomes** — What observable states indicate success? (2-3 outcomes)
3. **Stop Rules** — When should the agent halt, escalate, or declare done?

This is the highest-ROI change. It gives the agent judgment for edge cases
while preserving your existing instructions.

**Level 2: Structured Intent (2-4 hours per skill)**
Add all Level 1 sections plus:
4. **Health Metrics** — What must not degrade?
5. **Constraints** — Split existing rules into Steering vs. Hard
6. **Decision Authority** — Assign autonomy levels to key decisions
7. **Edge Cases** — Add 5+ boundary conditions

Rework existing step-by-step instructions into steering constraints,
removing prescriptive HOW language and replacing with intent-driven guidance.

**Level 3: Full Conversion (4-8 hours per skill)**
Complete rewrite using the full 9-section template. Existing instructions
are dissolved — the HOW is left to the agent. Only WHAT, WHY, and BOUNDARIES
remain.

### Prioritization for 106 Skills

Don't convert all 106 at once. Prioritize by:
1. **Blast radius:** Skills that touch production systems, external APIs,
   or user-facing outputs → convert first
2. **Failure frequency:** Skills that frequently produce wrong outputs →
   convert next
3. **Autonomy level:** Skills intended for autonomous operation →
   need full conversion. Skills always run interactively → Level 1 is fine.
4. **Complexity:** Simple, single-task skills → Level 1.
   Multi-step workflows → Level 2 or 3.

### Conversion Checklist (Per Skill)

- [ ] Read the existing skill and identify: What problem does it solve?
- [ ] Write the Objective (problem + why)
- [ ] Convert any activity-based goals to outcome-based goals
- [ ] Identify what could go wrong → write Health Metrics
- [ ] Separate instructions into: steering constraints vs. hard constraints
- [ ] Identify decisions the agent makes → assign autonomy levels
- [ ] Add edge cases from experience (what has gone wrong before?)
- [ ] Define stop rules: halt conditions, escalation triggers, completion criteria
- [ ] Add verification: how do you know the skill executed correctly?
- [ ] Run the Quality Validation Checklist (above)
- [ ] Test: remove the original instructions. Can the agent still succeed
      using only the intent spec? If yes, the conversion is complete.

---

## Anti-Patterns Reference

### 1. "Prompt in a Hat"
**Pattern:** An intent spec that's really just detailed step-by-step instructions
with section headers added.
**Why it fails:** The agent follows steps mechanically. When it encounters a
situation not covered by the steps, it has no judgment framework.
**Fix:** Delete the steps. Write the objective and outcomes. Let the agent
figure out the steps. Add constraints only where the agent's default approach
would be wrong.

### 2. "Over-Constrained Straitjacket"
**Pattern:** So many constraints that the agent has no room for useful
autonomous decisions.
**Why it fails:** Defeats the purpose of using an agent. You've essentially
written a script in natural language.
**Fix:** For each constraint, ask: "If the agent did something different here,
would that be bad?" If the answer is "not necessarily," remove the constraint.

### 3. "Conflicting Health Metrics"
**Pattern:** Health metrics that cannot all be satisfied simultaneously.
"Maximize speed" + "Maximize quality" + "Minimize cost."
**Why it fails:** The agent oscillates or picks one metric to optimize,
degrading the others unpredictably.
**Fix:** Prioritize. State which health metric takes precedence. Or define
acceptable ranges instead of optimization targets.

### 4. "Cargo Cult Intent Engineering"
**Pattern:** Using the 9-section template but filling it with content that
doesn't actually encode intent. Objectives that are task descriptions.
Outcomes that are activities. Stop rules copied from examples without
adaptation.
**Why it fails:** Creates false confidence. The team thinks they have an
intent spec, but the agent has no more judgment than it would with a raw
prompt.
**Fix:** For every section, verify it passes the quality test listed in the
template. If the Objective doesn't help with trade-offs, rewrite it. If the
Outcomes describe activities, rewrite them as states.

### 5. "Missing the Architecture Layer"
**Pattern:** Putting all constraints in the prompt, including ones that
should be enforced in code/orchestration.
**Why it fails:** Prompts are suggestions. In adversarial or edge-case
situations, the agent may violate prompt-level constraints. Critical
constraints need architectural enforcement.
**Fix:** Every constraint should answer: "What enforces this?" If the answer
is "the prompt," ask "What happens if the agent ignores it?" If the answer
is "real harm," move it to architecture.

---

## How to Use This Skill

When the user asks you to **write an intent spec:**
1. Ask clarifying questions about the domain, users, and failure modes
2. Draft using the full 9-section template
3. Run the Quality Validation Checklist
4. Flag any sections where you lack information to complete properly

When the user asks you to **review an intent spec:**
1. Run the Quality Validation Checklist
2. Check for all 10 common mistakes
3. Check for all 5 anti-patterns
4. Provide specific, actionable feedback per section

When the user asks you to **retrofit an existing prompt/skill:**
1. Assess current state (prompt vs. partial intent spec)
2. Recommend conversion level (1, 2, or 3) based on blast radius and complexity
3. Perform the conversion at the recommended level
4. Run the Quality Validation Checklist on the result

When the user asks you to **compare approaches or trade-offs:**
1. Frame the comparison using the Objective as the decision criteria
2. Evaluate options against Desired Outcomes
3. Check options against Health Metrics and Constraints
4. Recommend based on the autonomy/risk framework

---

## Additional Resources

- For the unified template as a blank form, see [template.md](template.md)
- For more domain-specific examples, see [examples/](examples/)
