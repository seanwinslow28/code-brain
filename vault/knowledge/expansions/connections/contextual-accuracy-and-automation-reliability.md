---
title: "How to make `Contextual Accuracy and Automation Reliability` better"
type: expansion
parent: "[[contextual-accuracy-and-automation-reliability]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-13
updated: 2026-06-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[contextual-accuracy-and-automation-reliability]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “Common Ground Breakdown” as the missing failure mode

**What to add:**  
Add a contextual-accuracy facet based on **common ground**: agents fail when they act as if shared assumptions already exist between user, vault, task, and tool state. Sentence pattern: “This is not a retrieval miss; it is a common-ground hallucination, where the agent assumes the missing premise has already been mutually established.”

**Who/what exemplifies it:**  
Herbert H. Clark, **_Using Language_**. Especially Clark’s theory of common ground and joint action.

**What this unlocks:**  
This turns the concept from “better context assembly” into an **agent conversation protocol**. Sean could ship a runbook or agent spec called `common-ground-check.md`: before acting, the agent must identify which premises are grounded, inferred, stale, or absent. This would help the daily-driver and critic stop sounding like generic summarizers and start exposing “you think I know X, but X was never established.”

## 2. Add “Blackboard Architecture” as the coordination pattern

**What to add:**  
Add blackboard architecture as a concrete alternative to each agent rebuilding context from scratch. The missing idea is not just retrieval quality; it is **shared intermediate state**. Sentence pattern: “Reliable automation needs a blackboard, not just a memory: a shared workspace where specialists post partial interpretations, constraints, hypotheses, and conflicts before any one agent acts.”

**Who/what exemplifies it:**  
H. Penny Nii, **“Blackboard Systems: The Blackboard Model of Problem Solving and the Evolution of Blackboard Architectures”**.

**What this unlocks:**  
This gives Sean a stronger architecture for `fleet-memory` and the daily note as fleet console. He could ship an executable demo: `blackboard_context_assembler.py`, where indexer, synthesizer, critic, and daily-driver write typed claims into a shared board before downstream agents consume them. The artifact is stronger than “context index” because it supports contradiction, provenance, and partial work products.

## 3. Add “Normal Accident” critique against reliability optimism

**What to add:**  
Add a contradicting framework: some automation failures are not caused by insufficient context; they are caused by **tight coupling and interactive complexity**. Sentence pattern: “The reliability target is not perfect context; it is graceful degradation when tightly coupled agent chains produce surprising interactions.”

**Who/what exemplifies it:**  
Charles Perrow, **_Normal Accidents: Living with High-Risk Technologies_**.

**What this unlocks:**  
This lets Sean write a sharper Substack essay or portfolio one-pager: “Why Agent Fleets Need Incident Design, Not Just Better RAG.” It also unlocks concrete reliability artifacts: incident taxonomies, blast-radius budgets, stop rules, replay logs, and degraded-mode runbooks. The current concept says “assemble better context”; Perrow lets Sean say “some failures are structurally inevitable, so design containment.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
