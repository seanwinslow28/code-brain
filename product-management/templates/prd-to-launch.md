# PRD-to-Launch Workflow Guide

Connect `prd-generator` → `jira-automation` → `sprint-roadmap` into a single end-to-end pipeline.

## Overview

This guide documents the handoff flow from PRD approval to sprint delivery. It's a workflow guide, not a skill — invoke the referenced skills at each stage.

## Stage 1: PRD Creation (`prd-generator`)

**Trigger:** "Write a PRD for [feature]" or "I need a spec for [project]"

**Output:** Approved PRD with:
- Problem statement and success metrics
- User stories with acceptance criteria
- Technical constraints and dependencies
- Scope definition (in/out)

**Approval checklist before proceeding:**
- [ ] Problem statement validated with stakeholder
- [ ] Success metrics are measurable and time-bound
- [ ] Scope is explicitly bounded (non-goals listed)
- [ ] Technical feasibility confirmed with engineering lead
- [ ] User stories have testable acceptance criteria

**Handoff to Stage 2:** "Break down this PRD into Jira tickets"

## Stage 2: Ticket Creation (`jira-automation`)

**Trigger:** "Break down this PRD into Jira tickets" or "Create tickets from this PRD"

**Input:** Approved PRD from Stage 1

**Process:**
1. Create the **Epic** (extract Problem, Solution, Scope, Metrics from PRD)
2. Create **[Design] story** covering all UI/UX deliverables
3. Create **[Implementation] stories** broken down by surface or system
4. Link all stories to the Epic
5. Assign components (Campus, theblock.co, etc.) and labels (NeedsDesign, frontend, BACKEND)

**Quality check before proceeding:**
- [ ] Epic has Problem, Solution, Scope, and Success Metrics
- [ ] Design story covers all UI deliverables with Figma handoff requirement
- [ ] Each Implementation story has user story format and acceptance criteria
- [ ] Stories are right-sized (completable in ~1 sprint)
- [ ] Components and labels match Block conventions
- [ ] All stories linked to parent Epic

**Handoff to Stage 3:** "Load these tickets into the next sprint"

## Stage 3: Sprint Planning (`sprint-roadmap`)

**Trigger:** "Plan the sprint for [Epic]" or "Prioritize these tickets for next sprint"

**Input:** Linked tickets from Stage 2

**Process:**
1. Review team capacity and current sprint commitments
2. Prioritize tickets by dependency order (Design → Implementation)
3. Assign to sprint(s) based on capacity
4. Flag any cross-team dependencies or blockers
5. Set sprint goals aligned with Epic success metrics

**Sprint loading rules:**
- Design stories go first (they unblock implementation)
- Group related Implementation stories in the same sprint when possible
- Leave 20% sprint capacity for bugs and unplanned work
- If Epic spans >2 sprints, break into milestones

## Full Pipeline Example

```
User: "Write a PRD for Campus prerequisite courses"
→ prd-generator: Generates PRD with user stories, metrics, scope

User: "Break this down into Jira tickets"
→ jira-automation: Creates Epic + Design story + 5 Implementation stories in PRO

User: "Plan the sprint"
→ sprint-roadmap: Loads Design story into Sprint 25, Implementation into Sprint 26

User: "Generate the bi-weekly update"
→ stakeholder-update: Reports progress against the Epic
```

## Trigger Patterns

Use these prompts to invoke the pipeline at any stage:

| Stage | Prompt |
|:------|:-------|
| Start from scratch | "Write a PRD for [feature], then break it into tickets" |
| PRD exists, need tickets | "Break down this PRD into Jira tickets" |
| Tickets exist, need sprint | "Plan the next sprint — include [Epic] tickets" |
| Mid-sprint check | "Sprint health check" (via `sprint-roadmap`) |
| Post-sprint report | "Generate the bi-weekly update" (via `stakeholder-update`) |
