---
title: "How to make `Provider Fallback Mechanism` better"
type: expansion
parent: "[[provider-fallback-mechanism]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-23
updated: 2026-06-23
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[provider-fallback-mechanism]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “circuit breaker semantics,” not just fallback parsing.**  
   Anchor it on Michael Nygard’s *Release It!* pattern “Circuit Breaker.” Your current concept treats provider weirdness as a parsing defect: strip SSE comments, recover balanced JSON, record failure cost. What’s missing is the operational state machine: `closed → open → half-open`, with failure thresholds, cool-down windows, probe requests, and explicit degraded behavior.

   **Sentence pattern to add:** “A provider fallback is not a retry policy; it is a runtime state machine that decides when a dependency is no longer trustworthy enough to call.”

   **Unlocks:** an **agent-fleet runbook**: “When OpenRouter bills failed calls, when do we stop calling it?” This gives Sean a decision artifact the current concept cannot reach: thresholds for disabling Fusion/DR/provider routes before cost leakage becomes invisible drift.

2. **Add “bulkheads + graceful degradation” as the architectural sibling.**  
   Anchor it on Sam Newman’s *Building Microservices*, specifically the resilience patterns around bulkheads, timeouts, and degraded functionality. The concept currently says “handle provider quirks precisely.” That is useful but too local. It does not ask whether one flaky provider should be allowed to contaminate the whole workflow.

   **Sentence pattern to add:** “Provider fallback should preserve the mission of the workflow, not the illusion that every step completed.”

   **Unlocks:** an **agent spec / routing policy** for Sean’s fleet: if Fusion fails, still emit an evidence ledger; if cost accounting fails, mark the run `financially_untrusted`; if citation verification fails, suppress FRAME output. This turns “fallback” from parser hardening into workflow design: partial outputs with named confidence states.

3. **Add “compensating transactions / saga thinking” for failures after money or state changes.**  
   Anchor it on Hector Garcia-Molina and Kenneth Salem’s paper “Sagas” and, for modern distributed systems framing, Chris Richardson’s *Microservices Patterns*. Sean’s example says failed Fusion calls bill OpenRouter but record `$0` locally. That is not merely a provider failure; it is a split-brain accounting event. The external side effect happened, but the local ledger missed it.

   **Sentence pattern to add:** “Fallback is insufficient once a side effect has crossed the boundary; the system now needs compensation, reconciliation, or quarantine.”

   **Unlocks:** a **cost-integrity audit artifact**: a daily reconciliation job that compares provider-side spend, local manifests, and failed-run envelopes. This would let Sean produce a portfolio-grade one-pager on “financially accountable agent infrastructure,” which is much stronger than “I hardened JSON parsing.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
