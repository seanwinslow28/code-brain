---
title: "How to make `Coupling Fragility vs Adaptive Capacity in Agent Fleets` better"
type: expansion
parent: "[[coupling-fragility-vs-adaptive-capacity-in-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-01
updated: 2026-07-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[coupling-fragility-vs-adaptive-capacity-in-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “control-structure critique” via STPA, not just coupling language.**  
   Anchor it on Nancy Leveson’s *Engineering a Safer World* and STPA/STAMP. The missing move is: “For each agent, name the controller, controlled process, feedback channel, unsafe control action, and missing constraint.” This turns “A creates B’s unsafe context” into an analyzable control loop. It unlocks a portfolio-grade **agent fleet safety case** or **STPA worksheet for personal automation**, where Sean can show specific constraints like “daily-driver must not consume stale synth output without freshness metadata.”

2. **Add “graceful extensibility budget” as the operational form of adaptive capacity.**  
   Anchor it on David Woods’s “The Theory of Graceful Extensibility,” especially the idea that units hit saturation and need mechanisms to expand capacity. Sentence pattern: “This fleet is healthy only if it can detect saturation, recruit alternate capacity, and preserve coordination before brittle collapse.” This unlocks a **dashboard spec** the current concept cannot reach: not green/red agent status, but remaining slack, fallback depth, degraded-mode quality, and manual-recovery cost.

3. **Add “promise contracts” for autonomous agents instead of orchestration assumptions.**  
   Anchor it on Jan Bergstra and Mark Burgess’s *Promise Theory: Principles and Applications* / Burgess’s *Thinking in Promises*. The missing frame is that autonomous agents do not truly “obey” each other; they make, keep, break, and observe promises. Sentence pattern: “Agent X promises output shape Y under conditions Z; Agent B trusts that promise only if freshness, provenance, and confidence promises are also present.” This unlocks an **agent contract spec** or **intent-engineering MCP artifact**: machine-readable promises between fleet members, stronger than descriptive dependency maps and more aligned with Sean’s “intent, not imperative prompt” thesis.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
