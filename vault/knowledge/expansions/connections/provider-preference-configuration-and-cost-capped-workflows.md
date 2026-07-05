---
title: "How to make `Provider Preference Configuration and Cost-Capped Workflows` better"
type: expansion
parent: "[[provider-preference-configuration-and-cost-capped-workflows]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-29
updated: 2026-06-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[provider-preference-configuration-and-cost-capped-workflows]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “control-plane policy” as the missing abstraction**
   - **What to add:** Treat provider preferences as a policy layer, not just routing config: explicit objectives, constraints, fallback permissions, audit logs, and escalation rules.
   - **Anchor:** Mark Burgess, *In Search of Certainty: The Science of Our Information Infrastructure*; also his Promise Theory work, especially *Thinking in Promises*.
   - **Unlocks:** A concrete **agent governance spec**: “Provider Policy Charter v1” for Code-Brain. Right now the concept says “route cheaply and reliably.” Promise Theory would let Sean specify what each provider, router, budget guard, and agent is allowed to promise, what it cannot promise, and what happens when promises fail. This turns OpenRouter config into an auditable control plane.

2. **Add “SRE error budgets for agent spend and quality”**
   - **What to add:** Cost caps should not only be hard limits. Add an error-budget model: spend budget, latency budget, hallucination/citation-failure budget, and degraded-mode budget. Define when the fleet is allowed to “burn budget” for higher-quality work.
   - **Anchor:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, *Site Reliability Engineering: How Google Runs Production Systems*, especially the chapters on service-level objectives and error budgets.
   - **Unlocks:** A **runbook and dashboard design** for agent fleet operations. Sean could produce “SLOs for Personal Agent Fleets”: examples like “Vault Critic may spend up to $0.40/night unless contradiction density exceeds threshold,” or “research agents may degrade to local-only mode after citation-quality failure.” The current concept can cap costs; SRE framing lets him decide when spending more is correct.

3. **Add “multi-armed bandit routing” as the contradicting framework**
   - **What to add:** Challenge static provider preference ordering with adaptive exploration/exploitation. Instead of fixed `sort_by=price` or fallback rules, model providers as arms with changing reward scores: cost, success rate, latency, citation quality, task fit.
   - **Anchor:** Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapter 2, “Multi-armed Bandits.” For a practical adjacent reference: John Myles White, *Bandit Algorithms for Website Optimization*.
   - **Unlocks:** An **executable demo**: `provider-bandit-router.py` replaying Sean’s agent logs and showing when static cheapest-provider routing loses to adaptive routing. This gives him a portfolio-grade artifact: “I built a learning router for cost-capped agents.” The current concept is configuration; bandits make it a self-improving decision system.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
