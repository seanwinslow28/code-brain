---
title: "How to make `Automation Reliability and Agent Fleet Health` better"
type: expansion
parent: "[[automation-reliability-and-agent-fleet-health]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-23
updated: 2026-08-23
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-agent-fleet-health]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “healthy/stale” with service-level objectives and error budgets

**Add:** A reliability-contract mode: define each automation by an observable outcome, acceptable failure budget, and multi-window burn rate—not whether its process merely ran.

**Anchor:** Steven Thurgood et al., [“Alerting on SLOs,” *The Site Reliability Workbook*](https://sre.google/workbook/alerting-on-slos/). Their method distinguishes fast catastrophic failures from slow cumulative degradation and routes them differently.

**Sentence pattern:** “The Daily Driver’s objective is not ‘runs at 08:30’; it is ‘a usable daily-note skeleton exists by 08:40 on 29 of 30 mornings.’ Page on rapid budget burn; create a ticket for slow burn.”

**Unlocks:** A publishable **Agent Fleet Reliability Contract** plus machine-readable SLO registry: success event, evaluation window, dependency exclusions, error budget, page threshold, and ticket threshold per agent. This would turn the current article’s vague “ensure reliability” implication into defensible decisions about when to repair, tolerate, disable, or redesign an automation.

## 2. Treat fleet health as uncertain knowledge, not ground truth

**Add:** An unreliable-failure-detector model separating **observation** from **inference**. A missed heartbeat cannot prove an agent failed; the machine may be asleep, unreachable, intentionally disabled, deferred, or partially complete.

**Anchor:** Tushar Deepak Chandra and Sam Toueg, [“Unreliable Failure Detectors for Reliable Distributed Systems”](https://research.google/pubs/unreliable-failure-detectors-for-reliable-distributed-systems/) (1996). Their foundational move is to model failure detection through completeness and accuracy rather than pretending suspicions are facts.

**Sentence pattern:** “`last_seen=02:30` is evidence; `suspected_unavailable` is an inference; `failed` requires a terminal manifest or violated deadline.”

**Unlocks:** A concrete **Fleet State Semantics agent spec** and dashboard-schema migration from `healthy/stale` to states such as `scheduled`, `running`, `succeeded`, `partial`, `deferred`, `suspected`, and `confirmed_failed`, each carrying evidence, confidence, and expiry. This directly prevents false incidents around sleeping machines and expected off-LAN deferrals.

## 3. Contradict “reliability means seamless operation” with graceful extensibility

**Add:** A resilience mode that evaluates what happens when the fleet exceeds its designed envelope. Reliability preserves expected performance; resilience preserves useful control under surprise.

**Anchor:** David D. Woods, [“Four Concepts for Resilience and the Implications for the Future of Resilience Engineering”](https://doi.org/10.1016/J.RESS.2015.03.018). Woods distinguishes rebound, robustness, **graceful extensibility**, and sustained adaptability.

**Sentence pattern:** “When the MBP disappears mid-synthesis, does the fleet merely avoid crashing, or does it preserve provenance, bound damage, expose reduced capability, and create a recoverable next action?”

**Unlocks:** An executable **agent-fleet game-day runbook** and portfolio demo that injects host loss, stale credentials, malformed manifests, concurrent writes, and dependency latency—then scores degradation quality, recoverability, and operator burden. The present concept can report normal-state status; this lens can demonstrate engineering judgment under surprise.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
