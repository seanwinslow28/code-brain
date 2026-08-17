---
title: "How to make `Daily-Drive Agent` better"
type: expansion
parent: "[[daily-drive-agent]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-14
updated: 2026-08-14
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[daily-drive-agent]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add an “expected value of interruption” policy

- **What to add:** Mixed-initiative mode. Every proposed intervention should compare expected benefit against interruption cost, confidence, urgency, and reversibility. Decision rule: `act when benefit × confidence > attention cost + error cost`; otherwise queue, summarize, or remain silent.
- **Anchor:** Eric Horvitz, [“Principles of Mixed-Initiative User Interfaces”](https://erichorvitz.com/chi99horvitz.pdf) (CHI 1999). Horvitz identifies poor timing, incorrect goal inference, and failure to weigh automation costs as central agent-design failures.
- **What it unlocks:** An executable **intervention-policy simulator** and portfolio one-pager showing why the agent sent a push notification, modified the daily plan, or stayed quiet. The current concept says the agent “ensures productivity” but cannot decide when its assistance becomes distraction—the defining product decision for a daily companion.

### 2. Add “plans as resources, not programs”

- **What to add:** Situated-replanning mode. Treat the morning plan as a provisional resource that must be reinterpreted when Sean’s energy, deadlines, recruiter responses, or available machines change. Sentence pattern: “Given event **E**, assumption **A** no longer holds; preserve intent **I**, discard step **S**, and offer adaptations **X/Y**.”
- **Anchor:** Lucy Suchman, [*Plans and Situated Actions: The Problem of Human-Machine Communication*](https://books.google.com/books/about/Plans_and_Situated_Actions.html?id=AJ_eBJtHxmsC). Suchman’s contradiction is direct: plans help organize situated action but do not determine its course.
- **What it unlocks:** A **daily-plan exception runbook** plus an executable demo that re-plans after a cancelled interview, failed overnight agent, low-energy day, or surprise deadline while preserving the higher-order intent. The current concept can describe routine execution; it cannot distinguish intelligent adaptation from blindly completing stale tasks.

### 3. Recast the agent as a teammate with a “Basic Compact”

- **What to add:** Joint-activity mode with four explicit properties: **basic compact**, **common ground**, **mutual predictability**, and **directability**. Specify what Sean and the agent owe each other: what state each must expose, how either party redirects work, how disagreement appears, and how the agent signals that its model of the day may be wrong.
- **Anchor:** Gary Klein, David Woods, Jeffrey Bradshaw, Robert Hoffman, and Paul Feltovich, [“Ten Challenges for Making Automation a ‘Team Player’ in Joint Human-Agent Activity”](https://www.ihmc.us/wp-content/uploads/2021/04/17.-Team-Players.pdf). Their framework rejects automation that merely performs allocated tasks without maintaining coordination and common ground.
- **What it unlocks:** A rigorous **Daily-Drive Agent charter and eval suite**: Can Sean redirect it mid-run? Can he predict what it will do? Does it announce assumption changes? Can it recover shared context after an absence? This would turn the concept into a credible agentic-engineering case study rather than another scheduler with anthropomorphic language.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
