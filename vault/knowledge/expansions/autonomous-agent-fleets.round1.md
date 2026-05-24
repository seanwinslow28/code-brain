---
title: "How to make `Autonomous Agent Fleets` better"
type: expansion
parent: "[[autonomous-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[autonomous-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. Add **“supervisory control plane mode”** anchored on Matei Zaharia et al., **“Databricks: Large-Scale Data Processing in the Cloud”** and the later **Apache Airflow** pattern from Maxime Beauchemin’s **“The Rise of the Data Engineer”**.

   Sentence pattern to add:  
   > An agent fleet is not only a set of workers; it needs a scheduler, lineage graph, retries, state inspection, and operator-visible failure semantics.

   The current concept treats agents as peers sharing context. What is missing is the control-plane distinction: workers do tasks; orchestrators own dependency order, observability, retries, and state transitions. This would unlock **agent-ops architecture writing**: diagrams, runbooks, and “what owns recovery?” decisions. Sean could produce a fleet topology artifact instead of another stale-context failure summary.

2. Add **“blackboard architecture”** anchored on Barbara Hayes-Roth, **“A Blackboard Architecture for Control”**.

   Sentence pattern to add:  
   > Shared context should be modeled as a blackboard with typed contributions, conflict resolution, confidence, provenance, and explicit control knowledge, not as a passive daily note.

   The article says agents read/write persistent context, but it does not distinguish “shared notes” from a formal coordination substrate. Blackboard systems give Sean a canonical frame for multiple specialist agents contributing partial hypotheses to a shared workspace. This would unlock **coordination-protocol design**: schemas for agent claims, provenance fields, confidence markers, arbitration rules, and “who may overwrite what?” policies. It moves the concept from “agents can silently fail” to “context requires governance.”

3. Add **“normal accident / tightly coupled system critique”** anchored on Charles Perrow, **“Normal Accidents: Living with High-Risk Technologies.”**

   Sentence pattern to add:  
   > Silent propagation is not an edge case; in tightly coupled agent fleets, stale state becomes a normal accident unless coupling is intentionally loosened or made observable.

   Right now the concept frames failure as an implementation weakness: one agent fails to update context, another acts on stale data. Perrow would sharpen the contradiction: autonomy plus shared mutable state creates interactive complexity and tight coupling, so failure is structurally expected. This unlocks **risk analysis and design tradeoff writing**: deciding when Sean should prefer human checkpoints, append-only logs, degraded modes, circuit breakers, or manual reconciliation over more automation. It lets him write “where not to automate” memos instead of only “how the automation broke” notes.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
