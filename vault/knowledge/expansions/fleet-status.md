---
title: "How to make `Fleet Status` better"
type: expansion
parent: "[[fleet-status]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-17
updated: 2026-08-17
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[fleet-status]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Replace “active/disabled” with batch-agent SLOs and error budgets**

   - **What to add:** Define each agent by an observable outcome: completion, timeliness, coverage, and correctness. Example: “Daily Driver publishes a validated note by 08:40 on 29 of 30 mornings.” Attach an error-budget policy: repeated misses freeze feature work and trigger reliability work.
   - **Anchor:** Steven Thurgood and David Ferguson’s “[Implementing SLOs](https://sre.google/workbook/implementing-slos/)” in *The Site Reliability Workbook*, which explicitly defines coverage SLIs for batch pipelines and ties exhausted budgets to engineering decisions.
   - **What this unlocks:** An executable **Fleet Reliability Contract**—YAML agent SLOs, a generated scorecard, and a runbook that decides whether Sean should improve prompts, repair infrastructure, change schedules, or retire an agent. The current concept can count processes but cannot judge whether the fleet delivers value.

2. **Add “Age of Fleet Information,” not merely a `stale` label**

   - **What to add:** Every status claim should carry `observed_at`, `valid_until`, `evidence_source`, and an age-dependent confidence score. Different facts need different expiry windows: process reachability may expire in minutes; schedule configuration in days; output-quality evidence after a fixed number of runs. Sentence pattern: “Agent X was last observed producing valid artifact Y at T; this claim expires at T+n.”
   - **Anchor:** Sanjit Kaul, Roy Yates, and Marco Gruteser’s paper “[Real-Time Status: How Often Should One Update?](https://winlab.rutgers.edu/~gruteser/papers/sanjitnew.pdf),” which introduced **Age of Information** as a metric for the usefulness of status updates.
   - **What this unlocks:** A **machine-verifiable fleet-status schema** and freshness auditor that can refuse to render unsupported claims. It also gives Sean a strong Substack/demo premise: “A dashboard without epistemic expiry is a cache pretending to be truth.” The present `Status: stale` admits failure without making it actionable.

3. **Add an emergent-failure view that contradicts component health**

   - **What to add:** Treat “7 healthy agents” as insufficient evidence that the fleet is healthy. Record dependency edges, shared failure domains, compensating human actions, and near misses. Model incidents as interaction failures: indexer delay → synthesizer reads old state → critic validates obsolete output → dashboard reports green.
   - **Anchor:** Richard I. Cook’s “[How Complex Systems Fail](https://worrydream.com/refs/Cook_2000_-_How_Complex_Systems_Fail.pdf),” especially its claims that complex systems are intrinsically hazardous, catastrophe requires multiple contributing failures, and successful operation depends on continual human adaptation.
   - **What this unlocks:** A **Fleet Failure Atlas** plus an executable replay/chaos demo testing correlated failures such as an unavailable MBP, expired credentials, or poisoned shared state. That becomes unusually credible agentic-engineering portfolio evidence: not another agent dashboard, but a demonstration that local green lights can coexist with system-level failure.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
