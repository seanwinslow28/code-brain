---
title: "How to make `Agent Health Monitoring and Cost-Capped Agentic Workflows` better"
type: expansion
parent: "[[agent-health-monitoring-and-cost-capped-agentic-workflows]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-18
updated: 2026-08-18
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-monitoring-and-cost-capped-agentic-workflows]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “agent health” with outcome SLOs and error-budget burn

- **Add:** An **Agent SLO mode**: define each scheduled run as a good event only when it finishes on time, produces a schema-valid artifact, passes semantic checks, and reaches its consumer. Track `good_runs / eligible_runs`, not process uptime or “healthy (dry-run).” Alert on **multi-window, multi-burn-rate** budget consumption.
- **Anchor:** Steven Thurgood and David Ferguson’s [“Implementing SLOs”](https://sre.google/workbook/implementing-slos/) and Google’s [“Alerting on SLOs”](https://sre.google/workbook/alerting-on-slos/). Their crucial move is from component condition to user-visible success, with explicit action when an error budget is exhausted.
- **Unlocks:** An executable **fleet reliability contract**: per-agent SLIs, 28-day objectives, burn-rate queries, and a policy specifying when to disable an agent, freeze changes, or route work elsewhere. This reaches decisions the current article cannot: whether `partial`, `wol-deferred`, stale output, or structurally valid nonsense counts as failure.

## 2. Measure cost per accepted artifact, then learn the routing policy

- **Add:** A **quality-adjusted unit-economics mode**. Replace `$15/month` with metrics such as `cost / accepted artifact`, `cost / cited claim surviving verification`, and `wasted spend from rejected or duplicate output`. Treat model selection as a constrained cascade: cheap route first, escalate only when a calibrated evaluator predicts insufficient quality.
- **Anchor:** Lingjiao Chen, Matei Zaharia, and James Zou’s [*FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance*](https://openreview.net/pdf?id=cSimKw5p6R). FrugalGPT learns cascades that optimize accuracy subject to a cost constraint; it does not confuse low spend with efficiency.
- **Unlocks:** A portfolio-grade **routing benchmark and decision record** comparing local Qwen/Gemma, subscription CLIs, and paid APIs on Sean’s actual workloads. The resulting artifact could specify: “Route vault synthesis locally until predicted acceptance falls below 0.8; escalate only within the remaining monthly quality budget.” That is stronger than a cost inventory because it proves what each dollar buys.

## 3. Contradict “healthy means reliable” with graceful extensibility

- **Add:** A **capacity-for-surprise mode**: monitor remaining maneuvering room—queue slack, alternative routes, recovery time, dependency diversity, and whether a human can still intervene before saturation. A fleet can report every agent healthy while becoming increasingly brittle.
- **Anchor:** David D. Woods’s [*Resilience as Graceful Extensibility to Overcome Brittleness*](https://irgc.org/wp-content/uploads/2018/09/Woods-Resilience-as-Graceful-Extensibility-to-Overcome-Brittleness.pdf). Woods treats resilience as the ability to extend adaptive capacity near operational boundaries, not merely to preserve nominal performance.
- **Unlocks:** A **fleet game-day runbook and executable resilience demo**: remove the MBP mid-run, expire a credential, corrupt an artifact, or exhaust a spend cap; then score detection, graceful degradation, recovery, and preserved intent. This turns “automation reliability” from a list of past root causes into evidence about how Code-Brain behaves under novel combinations of failure.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
