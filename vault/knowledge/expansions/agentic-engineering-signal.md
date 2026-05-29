---
title: "How to make `Agentic Engineering Signal` better"
type: expansion
parent: "[[agentic-engineering-signal]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-29
updated: 2026-05-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agentic-engineering-signal]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Trace Semantics,” not just event analytics**

Anchor it on: **Philip Guo, “Python Tutor: Visualizing Code Execution to Support Learning Programming”** and **OpenTelemetry’s trace/span model**.

The missing facet is that `agent_run_id` is too coarse unless the run has a legible internal grammar: spans, parent/child steps, tool-call causality, retries, user corrections, and boundary hits. Add a named layer: **agent trace semantics**.

Sentence pattern to add:

> An agent run is not one event stream; it is a causal trace. Each tool call, retry, boundary refusal, human correction, and accepted artifact should be represented as a span with parentage, intent, evidence, and outcome.

This unlocks a **portfolio-grade observability spec**: `agent_run_trace.schema.json`, a Substack essay on “why agents need traces, not dashboards,” and an interview-ready decision about which failures are model failures, tool failures, policy failures, or intent failures. Right now the concept says “track steps”; trace semantics lets Sean specify *how steps become diagnosable evidence*.

2. **Add “Acceptance Is a Sociotechnical Gate,” contradicting completion metrics**

Anchor it on: **Lucy Suchman, “Plans and Situated Actions”**.

The concept says completion does not equal acceptance, but it still frames acceptance mostly as a product analytics event. Suchman gives Sean the stronger critique: plans are not execution truth; real work is situated, negotiated, repaired, and interpreted by humans in context.

Add a named mode: **situated acceptance**.

Sentence pattern to add:

> Acceptance is not the final boolean after task completion; it is the moment a human decides the agent’s work fits the local situation well enough to inherit responsibility for it.

This unlocks a **trust-runbook artifact** for agent fleets: when to auto-apply, when to stage for review, when to request clarification, when to produce evidence, when to stop. It also gives Sean a sharper AI-PM interview answer: autonomy is not earned by accuracy alone, but by reducing the human’s burden of contextual repair.

3. **Add “Control Theory for Agent Products” as the missing operating model**

Anchor it on: **Norbert Wiener, “Cybernetics: Or Control and Communication in the Animal and the Machine”**, plus the concrete modern software analog **Charity Majors, Liz Fong-Jones, and George Miranda, “Observability Engineering.”**

The concept uses “analytics is the rudder,” but it has not cashed that metaphor out into control loops: sensor, comparator, actuator, delay, instability, feedback gain. This matters because agent products fail differently when feedback arrives late or corrections overfit the next run.

Add a named framework: **agent control loop design**.

Sentence pattern to add:

> Agent analytics is not reporting; it is the sensing layer of a control system. The product decision is what gets corrected automatically, what gets exposed to a human, and what remains observational until enough evidence accumulates.

This unlocks an **agentic engineering one-pager** Sean can ship: “Run-Level Control Loops for Agent Products,” with a matrix mapping signal types to interventions: alert, block, retry, ask, rollback, fine-tune, update skill, or change autonomy boundary. Current concept reaches “measure agent runs”; this reaches “operate agent behavior.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
