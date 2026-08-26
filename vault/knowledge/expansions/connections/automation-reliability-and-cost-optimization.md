---
title: "How to make `Automation Reliability and Cost Optimization` better"
type: expansion
parent: "[[automation-reliability-and-cost-optimization]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-24
updated: 2026-08-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-cost-optimization]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add **SLOs with an executable error-budget policy**

**WHAT:** Replace “critical agents run reliably” with explicit, outcome-level objectives: freshness, successful artifact delivery, acceptable degradation, and maximum recovery time. Couple each SLO to a rule such as: “Two missed synthesis windows freeze new fleet additions until reliability returns.”

**WHO/WHAT:** Steven Thurgood and David Ferguson’s *Implementing SLOs* and Thurgood’s *Example Error Budget Policy* distinguish monitoring from governance: an SLO only gains “teeth” when budget consumption changes priorities or halts releases. [Google SRE Workbook](https://sre.google/workbook/implementing-slos/), [example policy](https://sre.google/workbook/error-budget-policy/).

**UNLOCK:** A publishable **Agent Fleet Reliability Contract**: per-agent SLIs, error budgets, burn-rate alerts, degradation rules, and stop/add-capacity decisions. The present concept can report “$0 and log-only”; it cannot decide whether Sean should repair, retire, or expand an agent.

## 2. Add **coordinated-omission-safe monitoring**

**WHAT:** Monitor expected work arrivals independently of observed completions. A launchd job that never starts produces neither a success nor necessarily an informative failure; completion-derived telemetry quietly omits the worst latency. Sentence pattern: “For every scheduled execution at *t*, record a synthetic expected-run event; close it only when the promised artifact arrives.”

**WHO/WHAT:** Gil Tene’s talk *How NOT to Measure Latency* names this failure **coordinated omission**: measurements become falsely reassuring when observation waits on the delayed system itself. Tene also created [`wrk2`](https://github.com/giltene/wrk2) to measure against a constant-rate arrival schedule; his original explanation points to the relevant section of the talk. [Tene’s coordinated-omission note](https://groups.google.com/g/mechanical-sympathy/c/icNZJejUHfE/m/BfDekfBEs_sJ).

**UNLOCK:** An executable **schedule-integrity canary** and a Substack essay—“Your Agent Fleet Is Green Because It Forgot to Measure the Missing Runs.” This directly upgrades statuses like `log-only` into deadline, freshness, and silent-nonexecution detection.

## 3. Add **Bainbridge’s automation irony as a cost category**

**WHAT:** Treat operator readiness and recoverability as costs. Automation removes routine practice while leaving Sean responsible for rare, ambiguous failures; therefore $0/run can still create expensive diagnosis debt. Track “time to reconstruct state,” “manual takeover success,” and “days since recovery path was exercised.”

**WHO/WHAT:** Lisanne Bainbridge’s 1983 paper *Ironies of Automation* argues that automation can enlarge the human operator’s problems by leaving people responsible precisely for abnormal conditions they no longer routinely handle. [*Automatica*, 19(6)](https://www.sciencedirect.com/science/article/pii/0005109883900468).

**UNLOCK:** A quarterly **fleet game-day runbook** with forced host loss, stale baton, expired credential, corrupt output, and rollback drills—plus a portfolio-ready incident replay. The current concept optimizes operating expense; Bainbridge lets Sean expose and price **recovery debt**.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
