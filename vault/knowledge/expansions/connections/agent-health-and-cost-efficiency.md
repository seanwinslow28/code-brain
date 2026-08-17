---
title: "How to make `Agent Health and Cost Efficiency` better"
type: expansion
parent: "[[agent-health-and-cost-efficiency]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-16
updated: 2026-08-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-and-cost-efficiency]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “reliability is a budget, not a maximum.”** The article assumes healthier always means cheaper. Google’s Marc Alvidrez and Mark Roth argue the opposite in [“Embracing Risk,” Chapter 3 of *Site Reliability Engineering*](https://sre.google/sre-book/embracing-risk/): excessive reliability consumes infrastructure and opportunity cost. Sentence pattern: **“For agent X, the acceptable failure budget is Y because a prevented failure costs more/less than recovery.”** This unlocks an **agent SLO and error-budget policy** specifying successful-output rate, maximum stale-output age, tolerated deferred runs, and when reliability work should displace feature work. It also gives Sean a strong portfolio decision story: why an occasionally deferred local agent can be healthier economically than a flawless cloud fallback.

2. **Add “failure amplification,” not merely “failure overhead.”** Anchor it on Marc Brooker’s [“Timeouts, Retries, and Backoff with Jitter”](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf). Brooker shows that three retries across a five-layer call chain can amplify downstream load **243×**; retries can therefore create the outage and its cost, not just respond to it. Sentence pattern: **“Every recovery edge has a retry owner, attempt ceiling, idempotency requirement, and dollar/token amplification bound.”** This unlocks a **fleet retry-topology runbook** for subprocess wrappers, routers, scheduled agents, and model fallbacks—plus an **executable failure demo** that kills a dependency and compares naive retries against single-layer retries, token buckets, capped backoff, and deterministic jitter.

3. **Add “the healthier the dashboard looks, the more it may be omitting.”** Anchor it on Gil Tene’s talk [“How NOT to Measure Latency”](https://qconlondon.com/london-2013/qconlondon.com/london-2013/presentation/How%20NOT%20to%20Measure%20Latency.html) and his [HdrHistogram repository](https://github.com/HdrHistogram/HdrHistogram). “Coordinated omission” occurs when a stalled system stops generating the very observations that would reveal the stall. Sean’s equivalent is a sleeping machine, missing baton, or never-started launchd job producing no duration/cost sample—making averages improve during failure. Sentence pattern: **“Health denominators come from expected work, not observed logs.”** This unlocks an **expected-run ledger** that records scheduled, started, completed, deferred, absent, and stale-output states; a **fault-injection benchmark** proving the dashboard detects silent non-events; and a sharp Substack essay: **“Your Agent Fleet’s Green Dashboard Is Lying.”**

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
