---
title: "How to make `Coordinated Omission in Agent Observability` better"
type: expansion
parent: "[[coordinated-omission-in-agent-observability]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-18
updated: 2026-08-18
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[coordinated-omission-in-agent-observability]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “omission-corrected measurement,” and fix the concept’s reversed denominator claim.** In Gil Tene’s talk *[How NOT to Measure Latency](https://qconsf.com/sf2012/dl/qcon-san-fran-2012/slides/GilTene_HowNotToMeasureLatency.pdf)*, coordinated omission is specifically a sampling error: a blocked load generator stops issuing requests, so the missing requests never enter the latency distribution. HdrHistogram operationalizes the correction with [`recordValueWithExpectedInterval()`](https://hdrhistogram.github.io/HdrHistogram/JavaDoc/). Your article currently says the defect arises when denominators come from **expected work**; that is backwards. Expected work is the correction—the defective denominator contains only observed work. Add a concrete rule: “For every missed scheduled interval, record a deadline-relative synthetic latency or explicit omission, never zero samples.” This unlocks an executable benchmark: a fault-injection demo showing the naïve and corrected p50/p99 while an MBP sleeps or a baton stalls.

2. **Add “failure suspicion,” not just `absent` and `stale`.** Tushar Chandra and Sam Toueg’s paper *[Unreliable Failure Detectors for Reliable Distributed Systems](https://www.cs.princeton.edu/courses/archive/fall07/cos518/papers/unreliable.pdf)* separates **completeness**—eventually suspecting failed processes—from **accuracy**—not falsely suspecting healthy ones. In an asynchronous fleet, silence cannot prove whether an agent crashed, the host slept, the network partitioned, launchd never fired, or telemetry failed. An expected-run ledger that immediately converts silence into failure therefore manufactures certainty. Add a suspicion state with evidence and expiry: `expected → overdue → suspected`, followed by `confirmed_failed`, `deferred_by_policy`, or `late_completed`. This unlocks an agent-health state-machine spec and incident runbook that prescribe different recovery actions instead of collapsing every missing heartbeat into “unhealthy.”

3. **Add “deadline SLOs + multiwindow burn rates,” because counting missing runs still does not express user harm.** Steven Thurgood and collaborators’ Google SRE Workbook chapter *[Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)* recommends multiwindow, multi-burn-rate alerts and synthetic traffic for low-volume systems. Translate “request success” into “artifact delivered by deadline”: daily note ready by 08:30, index fresh before synthesis, synthesis complete before critique. A failed retry that still meets the deadline should consume no user-facing budget; one “successful” run that publishes stale output should. This unlocks a fleet SLO one-pager, Prometheus/SQLite alert rules, and a portfolio-grade dashboard that distinguishes fast budget burn requiring intervention from isolated bookkeeping anomalies.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
