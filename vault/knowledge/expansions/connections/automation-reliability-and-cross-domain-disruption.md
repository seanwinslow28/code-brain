---
title: "How to make `Automation Reliability and Cross-Domain Disruption` better"
type: expansion
parent: "[[automation-reliability-and-cross-domain-disruption]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-24
updated: 2026-08-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-cross-domain-disruption]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “lease + fencing-token” semantics for batons**

   - **What:** Replace the binary “baton found / no baton found” model with a protocol defining ownership, generation number, expiry, renewal, replay behavior, and idempotent recovery. Sentence pattern: “Agent B may consume baton generation *n* once; generation *n–1* is permanently stale.”
   - **Anchor:** Mike Burrows, [“The Chubby Lock Service for Loosely-Coupled Distributed Systems”](https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/) (OSDI 2006). Chubby treats coordination as a distributed-systems problem involving leases, unreliable communication, and stale actors—not merely missing files.
   - **Unlock:** An executable **Baton Protocol v2 agent spec** plus a fault-injection demo covering late writers, duplicate delivery, producer crashes, expired batons, and consumer retries. The current concept can report “No baton found”; this addition lets Sean decide whether absence means *not scheduled, not yet produced, expired, consumed, or producer failure*.

2. **Add “multiple contributing conditions” mode and reject the proximate-cause story**

   - **What:** The article currently implies one baton error cascades into Calendar, Slack, Adobe, Figma, and job-hunt disruption. That causal chain is unproven—and partly category-confused: headless MCP unavailability is an architectural capability boundary, not necessarily a consequence of baton failure. Model each incident as interacting latent conditions, defenses, and failed adaptations.
   - **Anchor:** Richard I. Cook, [“How Complex Systems Fail”](https://worrydream.com/refs/Cook_2000_-_How_Complex_Systems_Fail.pdf). Cook argues that complex systems normally operate with latent defects and that accidents require combinations of conditions; attributing failure to the most visible broken component produces misleading remedies.
   - **Unlock:** A **counterfactual incident review** or Substack essay titled *Your Agent Didn’t Fail Where the Error Message Says It Failed*. Artifact structure: observed loss → contributing conditions → defenses that worked → defenses absent → counterfactual tests. This would turn generic “cross-domain disruption” prose into defensible causal analysis.

3. **Add “graceful extensibility” instead of better monitoring as the endpoint**

   - **What:** Monitoring answers “What broke?” Reliability design must answer “How does useful work continue at the boundary?” Define a capacity envelope and a degradation ladder for every dependency: live MCP data → cached snapshot → explicit stale-data mode → skeleton-only output → typed deferral. Never collapse all misses into `error`.
   - **Anchor:** David D. Woods, [“The Theory of Graceful Extensibility: Basic Rules That Govern Adaptive Systems”](https://doi.org/10.1007/s10669-018-9708-3). Woods distinguishes robustness inside a known envelope from the ability to recruit new resources and strategies when that envelope is exceeded.
   - **Unlock:** A **cross-domain continuity runbook** and reusable **Degradation Contract** for agent specs: boundary signal, preserved function, fallback resource, prohibited inference, escalation threshold, and recovery test. The current concept recommends detecting disruption earlier; this addition specifies how the fleet remains useful after detection.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
