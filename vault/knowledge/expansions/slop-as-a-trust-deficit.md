---
title: "How to make `Slop as a Trust Deficit` better"
type: expansion
parent: "[[slop-as-a-trust-deficit]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-29
updated: 2026-06-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[slop-as-a-trust-deficit]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “appropriate reliance,” not “trust”**
   - **Anchor:** John D. Lee & Katrina A. See, [“Trust in Automation: Designing for Appropriate Reliance”](https://doi.org/10.1518/hfes.46.1.50_30392), *Human Factors*, 2004.
   - **What to add:** Reframe the concept from “users trust or distrust agents” to “users need calibrated reliance: knowing when to delegate, when to inspect, and when to ignore.”
   - **Sentence pattern:** “Slop is not low trust; it is miscalibrated reliance, where the user cannot tell whether the agent’s output deserves delegation, inspection, or rejection.”
   - **Unlocks:** A portfolio-grade **agent reliability scorecard**: per-agent reliance modes, confidence cues, inspection cost, failure classes. Current concept can complain about verification burden; this lets Sean specify measurable trust calibration.

2. **Add “automation surprises” as the mechanism**
   - **Anchor:** Nadine Sarter, David Woods & Charles Billings, “Automation Surprises,” in *Handbook of Human Factors and Ergonomics*, 2nd ed., 1997.
   - **What to add:** The missing facet is not just bad output; it is the user discovering too late that the system was in a different state, mode, or assumption set than expected.
   - **Sentence pattern:** “Slop becomes expensive when the agent’s state is hidden: the user thought it was synthesizing, but it was rate-limited, stale-indexed, context-starved, or silently degraded.”
   - **Unlocks:** An **agent observability contract**: every agent reports current mode, last successful run, skipped obligations, degraded dependencies, and required human action. This turns the concept into a runbook/spec for fleet UX, not just a diagnosis of annoyance.

3. **Add Bainbridge’s irony: automation creates harder human work**
   - **Anchor:** Lisanne Bainbridge, [“Ironies of Automation”](https://en.wikipedia.org/wiki/Ironies_of_Automation), *Automatica*, 1983.
   - **What to add:** The contradicting framework: more automation does not remove work; it often converts frequent easy work into rare, high-stakes monitoring and recovery work.
   - **Sentence pattern:** “The fleet’s failure mode is not that Sean still has work to do; it is that the remaining work becomes colder, rarer, less practiced, and more cognitively expensive.”
   - **Unlocks:** A strong **Substack essay or demo artifact**: “The Irony of Personal Agent Fleets.” It would argue that agentic systems need rehearsal loops, failure drills, and recovery affordances, not just better uptime. Current concept says slop erodes trust; Bainbridge lets Sean explain why reliability improvements alone may still leave the human operator worse off.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
