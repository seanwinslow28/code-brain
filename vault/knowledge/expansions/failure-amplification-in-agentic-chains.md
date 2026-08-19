---
title: "How to make `Failure Amplification in Agentic Chains` better"
type: expansion
parent: "[[failure-amplification-in-agentic-chains]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-19
updated: 2026-08-19
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[failure-amplification-in-agentic-chains]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add fleet-wide retry ownership, not merely bounded retries

**What to add:** “Single-layer retry ownership” plus a shared retry budget. Sentence pattern: *“A logical task receives N total attempts; only one orchestration layer may spend them.”* Backoff at every layer still multiplies load: four attempts across three layers can become 64 calls.

**Anchor:** Mike Ulrich’s Google SRE chapter, [“Addressing Cascading Failures”](https://sre.google/sre-book/addressing-cascading-failures/), specifically its server-wide retry budgets and warning against retries at multiple layers. Pair it with Marc Brooker’s [“Exponential Backoff and Jitter”](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/).

**What this unlocks:** An executable **retry-topology simulator** for Code-Brain: inject MBP unavailability, compare per-agent retries against a propagated `attempt_budget`, and graph logical tasks versus physical calls. The resulting **fleet retry-policy agent spec** would answer a question the current article cannot: *which component owns recovery?*

## 2. Add coordinated omission—and retract the unsupported diagnosis

**What to add:** “Coordinated-omission mode.” Sentence pattern: *“Measure work that should have occurred, not only attempts the system managed to start.”* A stalled scheduler, held index state, clean `wol-deferred` exit, or saturated queue may suppress observations precisely during the worst interval.

The article currently treats high synthesizer rejection counts and long durations as evidence of possible retry storms. That inference is weak: Sean’s rejection counts can arise from the T1.5 article-depth gate, while duration can reflect model throughput or host routing. Neither establishes retries without attempt-level traces.

**Anchor:** Gil Tene’s talk [“How Not to Measure Latency”](https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/GilTene_HowNotToMeasureLatency.pdf) and his [wrk2 repository](https://github.com/giltene/wrk2), built to preserve constant offered load and expose coordinated omission.

**What this unlocks:** A **fleet-observability measurement spec** separating scheduled, admitted, attempted, deferred, completed, and rejected work. Sean could ship a Substack essay—*“My Healthy Dashboard Was Coordinating With the Outage”*—plus a corrected latency/backlog panel instead of another generic resilience explainer.

## 3. Add semantic compensation: idempotency is not recovery

**What to add:** Saga-style compensating actions. Sentence pattern: *“Every side-effecting step declares `do`, `detect`, `compensate`, and `reconcile`; retry safety alone is insufficient.”* An idempotency key can prevent two identical writes, but it cannot undo a successfully written concept when the later edge update, manifest commit, or notification fails.

**Anchor:** Hector Garcia-Molina and Kenneth Salem’s canonical 1987 paper, [“Sagas”](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf), which decomposes long-lived transactions into steps with compensating transactions.

**What this unlocks:** An **agent-chain recovery contract** for intent-engineering: a durable execution ledger, explicit compensation handlers, and a reconciliation runbook. Sean could demonstrate a crash after “write concept” but before “commit manifest,” then recover deterministically—reaching partial-success semantics the current circuit-breaker vocabulary cannot express.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
