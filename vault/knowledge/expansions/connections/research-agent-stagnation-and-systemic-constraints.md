---
title: "How to make `Research Agent Stagnation and Systemic Constraints` better"
type: expansion
parent: "[[research-agent-stagnation-and-systemic-constraints]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-30
updated: 2026-08-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-agent-stagnation-and-systemic-constraints]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “query-by-committee” as an autonomous research-replenishment policy

**What to add:** Replace “Sean must actively manage the queue” with: *the fleet should propose questions where its models, vault concepts, or evidence sources disagree most*. Rank candidates by disagreement × decision relevance × evidence scarcity.

**Anchor:** Burr Settles, *Active Learning Literature Survey*, especially uncertainty sampling and **query-by-committee**, where disagreement identifies the next most informative query. [University of Wisconsin–Madison](https://minds.wisconsin.edu/handle/1793/60660)

**Sentence pattern:** “An empty queue is not missing clerical input; it is evidence that the system lacks an epistemic query policy.”

**Unlocks:** A `research-replenisher` agent spec and executable demo that converts council disagreement, unresolved concept edges, and low-confidence claims into scored research briefs. The current concept can detect starvation but cannot generate worthwhile demand.

## 2. Add Theory of Constraints’ Five Focusing Steps—and stop calling the symptom the constraint

**What to add:** Distinguish:

- **Observed state:** queue depth = 0.
- **Candidate constraints:** no question-generation mechanism, weak acceptance criteria, inaccessible evidence, insufficient research demand, or downstream synthesis capacity.
- **Test:** measure arrival rate, completion rate, acceptance rate, blocked time, and downstream concept reuse before intervening.

**Anchor:** Eliyahu M. Goldratt, *The Goal*, and its **Five Focusing Steps**: identify, exploit, subordinate, elevate, then reassess. TOC explicitly warns against optimizing a non-constraint. [Goldratt Research Labs](https://www.goldrattresearchlabs.com/introduction-to-toc)

**Sentence pattern:** “Queue starvation is telemetry, not diagnosis; the constraint is whichever factor currently limits valuable knowledge throughput.”

**Unlocks:** A fleet constraint-diagnosis runbook or fault-tree document that tells Sean whether to generate questions, restore access, change routing, or leave the agent idle. The present article jumps from observation directly to remedy without falsifying alternatives.

## 3. Add an economic pull model that contradicts “empty queue = stagnation”

**What to add:** Treat research as product-development inventory. A full queue can represent speculative overproduction; an empty queue can be healthy when no question has sufficient expected value. Introduce replenishment thresholds, WIP limits, aging rules, discard criteria, and a lightweight **cost-of-delay divided by job size** priority.

**Anchor:** Donald G. Reinertsen, *The Principles of Product Development Flow*. Reinertsen connects economic decisions, queue management, WIP constraints, batch size, and feedback speed rather than treating utilization as the goal. [Reinertsen & Associates](https://reinertsenassociates.com/books/)

**Sentence pattern:** “The objective is not to keep the researcher busy; it is to minimize the delay between a consequential uncertainty appearing and decision-grade evidence resolving it.”

**Unlocks:** A research-portfolio operating policy, kanban schema, and observability dashboard showing demand age, expected decision impact, evidence cost, and downstream reuse. This gives Sean a principled way to decide **what not to research**—a decision the current utilization-centered concept cannot make.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
