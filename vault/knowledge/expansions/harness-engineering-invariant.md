---
title: "How to make `Harness Engineering Invariant` better"
type: expansion
parent: "[[harness-engineering-invariant]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-19
updated: 2026-06-19
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[harness-engineering-invariant]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Gall’s Law as a deletion test,” anchored on John Gall’s *The Systems Bible*.**  
   Pattern to add: “A harness feature is only allowed if it evolved from a smaller working harness, not because the imagined future agent might need it.” Gall’s useful provocation is that complex systems that work usually evolve from simple systems that worked first, while complex systems designed from scratch fail. See [*Systemantics / The Systems Bible*](https://en.wikipedia.org/wiki/Systemantics).  
   This unlocks a **Harness Deletion Runbook** for Code-Brain: every tool, hook, agent, and scheduled job gets classified as `working-simple-origin`, `speculative-capability`, or `maintenance-debt`. That is sharper than the current concept’s “resist feature creep” framing because it gives Sean a deletion criterion.

2. **Add “STAMP control structure mode,” anchored on Nancy Leveson’s *Engineering a Safer World*.**  
   The missing facet is that harness reliability is not just tool count; it is control-loop quality: controller, controlled process, feedback, unsafe control actions, and delayed/missing feedback. Leveson’s STAMP/STPA work reframes accidents as control failures, not component failures. See [Nancy Leveson, *Engineering a Safer World*](https://en.wikipedia.org/wiki/Nancy_Leveson).  
   This unlocks an **Agent Fleet Control Diagram** or **STPA-lite audit**: Daily Driver, Vault Critic, Obsidian-Git, SessionStart hooks, launchd, and manual Sean decisions mapped as feedback loops. The current concept can say “more harness means more care”; STAMP lets Sean identify exactly where care is blind: stale manifests, missing negative feedback, blocked OAuth-only MCPs, or launchd jobs acting on incomplete state.

3. **Add “graceful extensibility vs tool austerity,” anchored on David Woods’s paper “The theory of graceful extensibility: basic rules that govern adaptive systems.”**  
   The contradiction: deleting tools can improve reliability, but over-pruning can make the fleet brittle when the environment changes. Woods’s frame distinguishes robustness against known stress from extensibility under surprise. See [David D. Woods, “The theory of graceful extensibility”](https://en.wikipedia.org/wiki/David_Woods_%28safety_researcher%29).  
   This unlocks a stronger **Substack essay / portfolio one-pager**: “I deleted tools until the agent improved, then stopped before I deleted adaptability.” It would let Sean sound less like a generic simplification advocate and more like someone who knows the real trade: remove unused capability, preserve expansion joints, and name the boundary where a lean harness becomes an overfit harness.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
