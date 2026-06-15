---
title: "How to make `Context Assembly as a Cross-Domain Failure Point` better"
type: expansion
parent: "[[context-assembly-as-a-cross-domain-failure-point]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-12
updated: 2026-06-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[context-assembly-as-a-cross-domain-failure-point]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Data/Frame failure mode,” anchored on Gary Klein et al., [“A Data/Frame Theory of Sensemaking”](https://en.wikipedia.org/wiki/Sensemaking_%28information_science%29).**  
   Sentence pattern to add: “Context assembly fails when the agent retrieves data without carrying the frame that makes the data actionable, or when it preserves an obsolete frame after contradictory evidence arrives.”  
   This would unlock a **critic rubric / agent spec** where each context bundle must declare: current frame, evidence supporting it, evidence that would break it, and escalation rule. Right now the concept says “assemble better context”; Klein lets Sean specify **when the context should revise the agent’s interpretation**.

2. **Add “sensemaking loop instrumentation,” anchored on Peter Pirolli & Stuart Card, [“The Sensemaking Process and Leverage Points for Analyst Technology”](https://en.wikipedia.org/wiki/Peter_Pirolli).**  
   Add the Pirolli/Card stages as an operational trace: forage → evidence file → schema → hypothesis → presentation.  
   This would unlock an **executable demo or fleet observability panel** that shows where each agent run failed: bad forage, weak evidence file, wrong schema, premature synthesis, or bad presentation. The current note collapses these into one vague “context assembly” failure. Pirolli/Card gives Sean a diagnostic grammar for nightly agents: not “retrieval failed,” but “schema construction failed after adequate evidence.”

3. **Add “context rot,” anchored on Christoph Treude & Sebastian Baltes, [“Context Rot in AI-Assisted Software Development”](https://arxiv.org/abs/2606.09090).**  
   Sentence pattern to add: “Persistent context is not a durable asset; it is documentation with decay dynamics, and agents become dangerous when stale instructions remain more authoritative than current code.”  
   This would unlock a **runbook + lint artifact** Sean does not yet have: a `CLAUDE.md` / `AGENTS.md` consistency checker that tests instruction files against repo reality. For Code-Brain, this is sharper than “assemble comprehensive context”: it says the failure may be **too much trusted historical context**, not too little retrieved context. It also creates a portfolio-ready one-pager: “Context Rot Linter for Agent Fleets.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
