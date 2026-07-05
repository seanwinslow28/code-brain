---
title: "How to make `Provider Fallback and Automation Reliability` better"
type: expansion
parent: "[[provider-fallback-and-automation-reliability]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-29
updated: 2026-06-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[provider-fallback-and-automation-reliability]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Failure Semantics,” not just fallback**
   - **What to add:** A taxonomy of failure modes: transient outage, degraded quality, silent corruption, partial completion, budget exhaustion, stale context, and unsafe success. The current note treats fallback as uptime. It needs “what kind of failure happened, and what kind of fallback is allowed?”
   - **Anchor:** Jim Gray, **“Why Do Computers Stop and What Can Be Done About It?”**; also Michael Nygard, **_Release It!_**, especially circuit breakers, bulkheads, and timeout patterns.
   - **Unlocks for Sean:** A concrete **agent reliability runbook**: “When provider A fails in mode X, route to B only if Y quality/cost/audit condition holds.” This lets him ship something stronger than “fallback improves reliability”: a decision table for autonomous agent routing where fallback is not automatic, but semantically constrained.

2. **Add “Fallback Can Be Harmful” via SRE error-budget thinking**
   - **What to add:** A contradicting frame: fallback increases reliability only when it does not hide systemic failure, amplify cost, or degrade user trust. Sometimes the right move is to fail closed, page the human, or burn no more budget.
   - **Anchor:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, **_Site Reliability Engineering_**, especially the chapters on **error budgets** and **monitoring distributed systems**.
   - **Unlocks for Sean:** A **cost-capped agent escalation policy**: “fallback allowed until daily budget burn reaches N%, confidence drops below threshold, or trace lacks provenance.” This would sharpen Code-Brain’s agent fleet governance and make the concept useful for portfolio proof: Sean is not just wiring fallbacks, he is managing reliability as a product tradeoff.

3. **Add “Saga / Compensation Patterns” for agent workflows**
   - **What to add:** Provider fallback is too request-level. Sean’s agents perform multi-step workflows: read, transform, write, commit, notify. Reliability there requires compensation, idempotency keys, checkpoints, and resumable state, not just alternate providers.
   - **Anchor:** Hector Garcia-Molina and Kenneth Salem, **“Sagas”**; practical modern counterpart: Chris Richardson, **_Microservices Patterns_**, chapter on the Saga pattern.
   - **Unlocks for Sean:** An **agent workflow spec template** for every scheduled agent: forward action, checkpoint, retry rule, compensation action, audit artifact. This would let him produce an executable demo: “nightly vault critic survives provider failure without duplicate writes, runaway spend, or corrupted vault state.” That is materially stronger than a concept note about fallback.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
