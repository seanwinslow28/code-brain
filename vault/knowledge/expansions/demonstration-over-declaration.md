---
title: "How to make `Demonstration Over Declaration` better"
type: expansion
parent: "[[demonstration-over-declaration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-03
updated: 2026-07-03
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[demonstration-over-declaration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “severe-test mode,” not just falsifiability.**  
   Anchor it on Deborah Mayo’s *Statistical Inference as Severe Testing* and *Error and the Growth of Experimental Knowledge* ([source](https://en.wikipedia.org/wiki/Deborah_Mayo)). The current concept says “make claims refutable,” but it does not ask whether the test was capable of catching the failure that matters.  
   Sentence pattern: “This demo only counts if it would probably fail under the exact defect I claim to prevent.”  
   Unlocks: an **agent-eval runbook** for intent specs: seeded bad specs, expected failure classes, mutation tests, false-pass budget, and a public `evals/intent-specs/` corpus. Without this, Sean risks shipping demos that are reproducible but too easy.

2. **Add “explorable explanation” as the portfolio genre.**  
   Anchor it on Bret Victor’s essay/talk lineage: *Explorable Explanations* and *Inventing on Principle* ([source](https://en.wikipedia.org/wiki/Explorable_explanation), [source](https://www.wired.com/2012/02/video-inventing-on-principle/)). The missing move is from “run my repo” to “manipulate the system and watch the concept change.”  
   Sentence pattern: “Drag the autonomy boundary from low-risk to high-risk and watch the audit obligations change.”  
   Unlocks: an **interactive portfolio one-pager** where recruiters can edit an intent spec, toggle blast radius, inject conflicting goals, and see the audit trace update live. This reaches a stronger artifact than README-demo credibility: it makes Sean’s thinking inspectable as dynamic media.

3. **Add “situated-action skepticism” as the contradiction.**  
   Anchor it on Lucy Suchman’s *Plans and Situated Actions: The Problem of Human-Machine Communication* ([source](https://en.wikipedia.org/wiki/Lucy_Suchman)). This pushes against the concept’s hidden assumption that a public reproduction proves real-world competence. Suchman’s corrective: plans and procedures do not fully determine action; use breaks in context.  
   Sentence pattern: “The demo passed in the repo; what changed when a rushed PM, a skeptical engineer, or a nontechnical recruiter tried to use it?”  
   Unlocks: a **field-test artifact**: three evaluator scripts, one for recruiter scan, one for engineering review, one for PM judgment. Each records where the proof fails socially: unclear affordance, wrong trust threshold, missing explanation, bad recovery path. This prevents “proof-by-reproduction” from becoming another polished but staged declaration.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
