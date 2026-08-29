---
title: "How to make `Cost Capping and Automation Workflows` better"
type: expansion
parent: "[[cost-capping-and-automation-workflows]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-28
updated: 2026-08-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[cost-capping-and-automation-workflows]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add a dual-budget model: money budget + error budget

**What:** Replace “cost remains capped, therefore scaling is safe” with two independent ledgers: dollars consumed and tolerated service failure. A workflow may cost $0 and still destroy trust through stale notes, silent deferrals, or missed runs.

**Anchor:** Marc Alvidrez and Mark Roth, “Embracing Risk,” in Google’s *Site Reliability Engineering*. Their error-budget pattern derives permitted failure from an SLO and slows or freezes changes when that budget is exhausted. [Google SRE: “Embracing Risk”](https://sre.google/sre-book/embracing-risk/)

**Unlock:** An **Agent Fleet Reliability Budget runbook** defining, per agent: user-visible SLI, SLO, allowable missed/partial runs, burn rate, and mandatory response when exhausted. It would turn `status: log-only` into an operational decision system: *continue experimenting, degrade gracefully, or freeze fleet expansion*. The current article can report cheapness; this addition could govern reliability.

### 2. Add constrained optimization: cost is a constraint, not the objective

**What:** Recast the fleet as maximizing useful knowledge produced subject to several constraints—not minimizing spend. Specify separate bounds for money, latency, hallucination, privacy exposure, and human-review load. This directly contradicts the article’s implication that predictable cost licenses further scaling.

**Anchor:** Joshua Achiam, David Held, Aviv Tamar, and Pieter Abbeel, “Constrained Policy Optimization.” The paper formalizes reward maximization while maintaining explicit constraints, rather than burying every concern inside one reward or score. [PMLR paper](https://proceedings.mlr.press/v70/achiam17a.html)

**Unlock:** A **portfolio-ready executable intent-governance demo**: agents bid for work against a constraint vector, and a controller rejects the cheapest route when it violates a quality or risk boundary. It also supplies the missing formal backbone for the intent-engineering MCP server: objective, constraint, measurement window, and escalation are distinct schema elements—not prose preferences.

### 3. Add retry budgets and multiplicative-work accounting

**What:** Measure *attempted work*, not merely completed-run cost. Every retry, fallback, subprocess fan-out, research branch, and model escalation consumes a shared retry budget. Use capped exponential backoff with jitter, but terminate when the workflow’s total attempt allowance is spent.

**Anchor:** Marc Brooker, “Timeouts, Retries, and Backoff with Jitter.” Brooker shows that retries can amplify overload across layered systems; backoff alone is insufficient without limiting retries at the correct layer. [Amazon Builders’ Library](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

**Unlock:** An **agent retry-storm incident replay** using an actual fleet failure: reconstruct how one unavailable host or rate-capped CLI expands into probes, retries, fallbacks, and duplicated work. Ship it as a runbook plus executable trace visualization showing `nominal cost`, `attempt-amplified cost`, and the exact circuit-breaker decision. That is stronger agentic-engineering evidence than a monthly-cost total because it demonstrates control of tail behavior, not just averages.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
