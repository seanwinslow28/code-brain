---
title: "How to make `Research System Integration and Constraints` better"
type: expansion
parent: "[[research-system-integration-and-constraints]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-29
updated: 2026-06-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-system-integration-and-constraints]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “queue economics mode” anchored on John D. C. Little’s 1961 paper, [“A Proof for the Queuing Formula: L = λW”](https://en.wikipedia.org/wiki/Little%27s_law).**

   Current concept says “routing rules manage workloads,” but it has no throughput math. Add a section that treats research topics as queue arrivals, researcher/model runs as service capacity, and stale unanswered questions as WIP.

   Sentence pattern: “A research route is healthy only if arrival rate, service time, and WIP are all visible; otherwise ‘use Gemini for compound topics’ is policy theater.”

   This unlocks a **research operations runbook**: backlog limits, SLA by research class, routing thresholds, and a dashboard metric like `open_topics * mean_age / completed_topics_7d`. Right now Sean can describe constraints; this would let him decide when to delete, defer, batch, or escalate research.

2. **Add “sensemaking-loop mode” anchored on Pirolli & Card’s [“The Sensemaking Process and Leverage Points for Analyst Technology”](https://en.wikipedia.org/wiki/Peter_Pirolli).**

   The article treats research as a queue-routing problem, but not as an analyst cognition problem. Pirolli/Card’s frame separates foraging, evidence marshaling, schema building, and presentation. That gives Sean a missing distinction: LDR/Gemini are not just interchangeable engines; they occupy different points in the sensemaking loop.

   Sentence pattern: “Do not route by model first; route by cognitive operation: forage, triage, cluster, contradict, synthesize, package.”

   This unlocks an **agent spec** for the Deep Research Queue where each task declares its intended cognitive operation before choosing tooling. It also gives the Vault Critic sharper failure labels: “weak foraging,” “premature synthesis,” “missing contradiction,” “no presentation product.” Current concept cannot tell whether a bad output failed because of model capacity, bad topic shape, or wrong sensemaking stage.

3. **Add “complexity-domain override” anchored on Snowden & Boone’s [“A Leader’s Framework for Decision Making”](https://hbr.org/2007/11/a-leaders-framework-for-decision-making).**

   The “single-shape topics only” rule is useful, but too tidy. Cynefin contradicts it: some research questions are not complicated-but-decomposable; they are complex, meaning the right move is probing multiple small experiments before synthesis.

   Sentence pattern: “Single-shape is valid for complicated questions; complex questions require probe portfolios, not cleaner prompts.”

   This unlocks a **triage decision tree**: clear questions go to local lookup, complicated questions go to Gemini DR, complex questions spawn 3–5 probes with explicit uncertainty, chaotic incidents go to immediate containment notes. It would help Sean write a Substack essay or portfolio one-pager showing he understands when agentic systems need governance, not just better routing.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
