---
title: "How to make `Contextual Agent Failures Across Automation Systems` better"
type: expansion
parent: "[[contextual-agent-failures-across-automation-systems]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-13
updated: 2026-06-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[contextual-agent-failures-across-automation-systems]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Common-Knowledge Failure Mode”**

Anchor it on: **Michael Chwe, _Rational Ritual: Culture, Coordination, and Common Knowledge_**.

Current concept treats context as information retrieval: the agent “doesn’t have what it needs.” Chwe gives you the sharper missing frame: some failures happen because the system lacks **shared epistemic state**. It is not enough that the right fact exists in the vault; the agent, scheduler, critic, and daily-driver must all know which facts are live, and know that the other agents know it too.

Sentence pattern to add:

> This was not a retrieval miss; it was a common-knowledge miss. The system had the fact, but no actor could safely assume the rest of the fleet was coordinating around it.

This unlocks: an **agent coordination runbook** or **fleet-memory design note** distinguishing “private memory,” “shared memory,” and “common knowledge.” That would make the concept useful for deciding what belongs in `vault/90_system/fleet-memory/`, what gets promoted, and what needs broadcast semantics rather than passive indexing.

2. **Add “Situated Action / Plans Are Not Execution”**

Anchor it on: **Lucy Suchman, _Plans and Situated Actions: The Problem of Human-Machine Communication_**.

Your concept currently implies the fix is better pre-run context assembly. Suchman cuts against that: plans and context packets are not the work itself. Agents fail because they encounter the world as it unfolds, and brittle automation mistakes the plan for the situation.

Sentence pattern to add:

> The failure is not only that the agent starts with incomplete context; it is that the agent treats its startup context as authoritative after the situation has changed.

This unlocks: a **stop-rule and reorientation spec** for autonomous agents. Instead of “assemble more context before acting,” Sean can ship an **agent spec** with mid-run checks: when to re-query, when to invalidate assumptions, when to halt, and when to ask for human confirmation. This directly strengthens intent-engineering because it turns “what to know” into “when to distrust what you knew.”

3. **Add “Observability Is Not Logging”**

Anchor it on: **Charity Majors, Liz Fong-Jones, and George Miranda, _Observability Engineering_**.

The article gestures at “Agent Health Monitoring,” but it still sounds like summary-level reliability language. Majors/Fong-Jones/Miranda give you the missing operational distinction: logs tell you what happened; observability lets you ask novel questions about unknown failure modes. Agent fleets need high-cardinality traces of context decisions, not just pass/fail health checks.

Sentence pattern to add:

> A context failure is only diagnosable if the trace preserves the agent’s context budget, retrieval candidates, rejected sources, confidence handoff, and action boundary at the moment of commitment.

This unlocks: an **Agent Fleet Observability Dashboard spec** or **trace schema**. The current concept can say “agents rebuild context inefficiently”; this addition lets Sean define actual fields: `context_sources_considered`, `sources_rejected`, `assumption_promoted`, `staleness_seconds`, `budget_spent_before_action`, `stop_rule_triggered`. That turns the note from generic reliability critique into a portfolio-grade artifact for agentic-engineering roles.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
