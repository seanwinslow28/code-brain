---
title: "How to make `Control Plane / Data Plane Split for Agent Fleets` better"
type: expansion
parent: "[[control-plane-data-plane-split-for-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-01
updated: 2026-07-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[control-plane-data-plane-split-for-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “unsafe control action” mode, anchored on Nancy Leveson’s _Engineering a Safer World_ / STPA.**  
   The current concept says “split control plane from data plane,” but it does not specify how control becomes unsafe. Add a section that classifies fleet failures as unsafe control actions: control command not given, wrong command given, command given too early/late, command continued too long/stopped too soon. Leveson’s STAMP/STPA work is the missing canonical frame here: accidents are produced by inadequate control in a sociotechnical system, not just broken components. See [Nancy Leveson / STPA](https://en.wikipedia.org/wiki/Nancy_Leveson) and the STPA software-safety paper by [Abdulkhaleq, Wagner, and Leveson](https://arxiv.org/abs/1612.03109).  
   **Unlocks:** an executable **agent-fleet hazard analysis runbook**. Sean could turn “Vault Critic wrote generic slop” into a control table: controller, controlled process, process model, unsafe control action, constraint, test. That reaches audit-grade engineering; the current concept only reaches ops metaphor.

2. **Add “above-the-line / below-the-line representation” mode, anchored on Richard Cook’s “Above the Line, Below the Line” and _How Complex Systems Fail_.**  
   Sean’s concept gestures at visible workflow vs backstage agent work, but it misses the sharper point: operators never touch the real system directly; they act through representations. For an agent fleet, the daily note, manifest JSON, Obsidian graph, spend logs, and launchd status are not “observability extras.” They are the control surface. Cook’s line of representation and complex-systems-fail work is the better ancestor than generic control-plane language. See [Richard Cook’s work list](https://en.wikipedia.org/wiki/Richard_Cook_%28safety_researcher%29), especially _How Complex Systems Fail_ and “Above the Line, Below the Line.”  
   **Unlocks:** a **fleet-console critique essay / dashboard spec**: “What Sean can actually know about his agents.” It would force each widget to answer: what real process does this represent, what distortion does it introduce, what action does it enable, and what false confidence might it create?

3. **Add “distributed OODA loops, not central control” as the contradicting framework, anchored on John Boyd’s _Patterns of Conflict_ / OODA.**  
   The article assumes control-plane clarity is the main improvement. Boyd gives the contradiction: the advantage may come from faster, nested orientation loops, not cleaner top-down control. For Sean’s fleet, the question becomes: which agents need local orientation authority, and which decisions must remain centralized? Boyd’s OODA is often flattened into speed, but the important move is orientation: model-updating under uncertainty. See [John Boyd’s _Patterns of Conflict_](https://en.wikipedia.org/wiki/Patterns_of_Conflict) and [OODA loop](https://en.wikipedia.org/wiki/OODA_loop).  
   **Unlocks:** an **agent spec pattern**: `Observe -> Orient -> Decide -> Act -> Leave Trace`. This would let Sean design agents that do not merely execute scheduled jobs, but maintain explicit orientation state: what changed, what belief updated, what decision threshold moved. Current concept diagnoses bottlenecks; this would design adaptive autonomy.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
