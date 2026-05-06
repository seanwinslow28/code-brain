---
title: "Intent Engineering SKILL.md — Design Guide & Research Summary"
type: reference
status: processed
domain: claude-mastery
created: 2026-02-28
ai-context: "Design rationale for the intent-engineering Claude Code skill — synthesizes Huryn's 7-part, Pathmode's IntentSpec, I-5, and Action Schemas into a unified 9-section template; documents Top 10 mistakes, 5 anti-patterns, 3-level retrofit framework, and 4 usage modes (Write/Review/Retrofit/Compare)."
tags:
  - reference
  - intent-engineering
  - source/pdf
  - skill-design
related:
  - "[[intent-engineering]]"
source-pdf: "Intent-Engineering-Skill.pdf"
---

# Intent Engineering SKILL.md — Design Guide & Research Summary

The companion design memo for the production-ready `intent-engineering` Claude Code skill (917-line SKILL.md + blank template). Synthesizes four leading frameworks into one coherent 9-section template with validation checklists, domain examples, retrofitting guidance, and anti-pattern detection.

## Source Framework Synthesis

The skill merges four approaches:

- **Huryn's 7-part structure** — Objective, Desired Outcomes, Health Metrics, Strategic Context, Constraints (steering vs. hard), Decision Types & Autonomy (4-level gradient), Stop Rules.
- **Pathmode's IntentSpec** — Adds User Goal (job-to-be-done), Edge Cases as boundary conditions, and Verification criteria.
- **I-5 Framework** — Top-down flow Intent → Interpretation → Information → Instruction → Implementation.
- **Action Schemas** (GitHub multi-agent guide) — Typed, constrained output formats that eliminate ambiguous agent actions.

## The Unified 9-Section Template

Objective · User Goal · Desired Outcomes · Health Metrics · Strategic Context · Constraints (Steering + Hard) · Decision Authority · Edge Cases · Stop Rules & Verification.

### Why 9 Sections Instead of 7

Huryn's 7-part structure omits two failure-mode catchers:

- **User Goal** (from Pathmode) forces the spec writer to articulate the job-to-be-done from the user's perspective — the difference between "categorize transactions" and "user can answer 'where did my money go?' in 30 seconds."
- **Edge Cases** as a dedicated section ensures boundary conditions get explicit treatment instead of being scattered. Every unhandled edge case is a potential hallucination point.

### Constraint Split: Steering vs. Hard

The most impactful principle. Steering constraints (prompt layer, influence reasoning) vs. hard constraints (architecture layer, enforce compliance). Decision rule: if violating the constraint causes real harm (data loss, financial exposure, security breach), it MUST be enforced architecturally. Production agent failures consistently trace back to constraints that were stated but not mechanically enforced.

### Autonomy as a Gradient

Four-level model — Full → Guarded → Proposal-first → Human-required — assigned using five risk lenses: blast radius, reversibility, confidence, precedent, visibility. Replaces the binary "autonomous or not" approach. As capability increases, autonomy should *decrease* proportionally to maintain safety.

## Quality Validation: 30-Item Checklist

Organized across 7 dimensions: Objective, Outcome, Health Metric, Constraint, Autonomy, Stop Rule, Edge Case quality. Each item maps directly to a known production failure mode.

## Top 10 Intent Spec Mistakes

| Rank | Mistake | Root Cause |
|------|---------|------------|
| 1 | Outcomes are activities, not states | Confusing what the agent does with what exists after |
| 2 | Missing health metrics | Goodhart vulnerability — agent games the primary metric |
| 3 | Hard constraints left in prompts | Critical rules enforced by "suggestion" not code |
| 4 | Vague autonomy boundaries | "Use good judgment" is not a specification |
| 5 | Stop rules only cover happy paths | No abort conditions for failures or edge cases |
| 6 | Intent spec is really a detailed prompt | Steps masquerading as intent — no judgment framework |
| 7 | Over-constraining | So many rules the agent can't exercise useful judgment |
| 8 | Conflicting health metrics | Impossible optimization triangle |
| 9 | Cargo cult intent engineering | Template structure without understanding why |
| 10 | No verification criteria | Spec not specific enough to validate |

## Five Named Anti-Patterns

- **"Prompt in a Hat"** — Step-by-step instructions with intent section headers. Fix: delete the steps, write the why, let the agent figure out the how.
- **"Over-Constrained Straitjacket"** — So many constraints the agent can't make useful decisions. Fix: for each constraint, ask "if the agent did something different, would that be bad?"
- **"Conflicting Health Metrics"** — Metrics that can't all be satisfied simultaneously. Fix: explicit priority ordering.
- **"Cargo Cult"** — Template structure filled with content that doesn't encode intent. Fix: verify each section passes its quality test.
- **"Missing the Architecture Layer"** — All constraints in the prompt, including ones that need code enforcement. Fix: every constraint answers "what enforces this?"

## Domain Examples (Worked)

1. **Software Development Agent** (code review, PR management) — Autonomy graduation from auto-approving doc-only PRs to requiring human approval for auth/payments code; health metrics prevent false-positive review fatigue.
2. **Personal Productivity Agent** (daily planning, inbox processing) — Read-only hard constraints prevent the agent from sending communications; user override rate as a calibration health metric.
3. **Creative Production Agent** (animation pipeline, asset management) — "Never delete source files" as architectural constraint; asset quality scores as health metrics against compression artifacts.
4. **Financial Analysis Agent** (spending tracking, budget optimization) — "Never guess on financial data" steering constraint; categorizing (full autonomy) vs. providing investment advice (forbidden).

## Retrofitting Process for Existing Skills

Three-level conversion framework:

| Level | Effort | What to Add | Best For |
|-------|--------|-------------|----------|
| **L1: Minimum Viable** | 30 min/skill | Objective + Outcomes + Stop Rules (keep existing instructions) | Simple, interactive skills |
| **L2: Structured** | 2–4 hrs/skill | + Health Metrics, Constraint split, Decision Authority, Edge Cases | Multi-step workflows |
| **L3: Full Conversion** | 4–8 hrs/skill | Complete rewrite using 9-section template; original instructions dissolved | Autonomous, high-blast-radius skills |

**Prioritization:** (1) skills touching production/external APIs, (2) skills with frequent wrong outputs, (3) skills intended for autonomous operation, (4) complex multi-step workflows. Simple single-task interactive skills only need L1.

**Conversion test:** Remove the original step-by-step instructions and see if the agent can still succeed using only the intent spec. If yes, conversion is complete.

## SKILL.md Format Compliance

Follows Claude Code's official format: YAML frontmatter (`name`, `description`) + markdown body. Description triggers on relevant queries (creating agent specs, converting prompts, reviewing specs). References a `template.md` companion and an `examples/` directory.

```
~/.claude/skills/intent-engineering/
├── SKILL.md (main skill — 917 lines)
├── template.md (blank intent spec form)
└── examples/
    └── (domain-specific examples)
```

## Four Usage Modes

- **Write** — Drafts a new intent spec using the 9-section template, asks clarifying questions about domain/users/failure modes, runs the validation checklist.
- **Review** — Audits an existing spec against the 30-item checklist, checks all 10 common mistakes and 5 anti-patterns, provides section-by-section feedback.
- **Retrofit** — Assesses an existing prompt-based skill, recommends a conversion level, performs the conversion, validates the result.
- **Compare** — Frames trade-offs using the Objective as decision criteria, evaluates options against Outcomes and Health Metrics, recommends based on the autonomy/risk framework.
