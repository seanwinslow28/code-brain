---
title: "How to make `Throughput vs. Activity Illusion in Job Hunt Operations` better"
type: expansion
parent: "[[throughput-vs-activity-illusion-in-job-hunt-operations]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-19
updated: 2026-08-19
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[throughput-vs-activity-illusion-in-job-hunt-operations]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add “constraint-location mode,” not merely throughput measurement

The concept notices absent throughput but never identifies the binding constraint. Add Eliyahu Goldratt’s five focusing steps from *[The Goal](https://northriverpress.com/about/)*: identify, exploit, subordinate, elevate, repeat. Sentence pattern: **“The constraint is currently X; improving any stage except X creates inventory, not throughput.”**

For the job hunt, model `roles discovered → eligible → scored → shortlisted → contacted → replied → interviewed`. `scored=0` could mean feed scarcity, an unavailable MBP scorer, filters rejecting everything, or simply no scoring attempt. Those demand different interventions.

This unlocks an executable **constraint ledger and weekly operating runbook**: stage counts, queue depth, conversion rate, current bottleneck, one authorized intervention. It also produces a strong portfolio one-pager: “I applied Theory of Constraints to an autonomous job-search system,” rather than another observability dashboard.

### 2. Add Deming’s “tampering” as a direct contradiction

The article recommends adjusting search parameters after observing zero output. That may be precisely wrong. Add W. Edwards Deming’s *[Funnel Experiment](https://deming.org/explore/the-funnel-experiment/)* and the common-cause/special-cause distinction developed operationally in Donald J. Wheeler’s *[Understanding Statistical Process Control](https://www.spcpress.com/book_understanding_statistical_process_control.php)*. Sentence pattern: **“One zero is an observation; a run outside established process limits is a signal.”**

Job opportunities are sparse, bursty, and calendar-sensitive. Reacting to yesterday’s zero by repeatedly widening titles or rewriting filters can increase variance and destroy the ability to learn which strategy works.

This unlocks a **job-feed process-behavior chart and intervention policy**: establish a baseline by weekday/source, define minimum observation windows, and change targeting only on a special-cause signal or sustained shift. Sean could ship this as a contrarian Substack essay: **“Your Job-Hunt Dashboard Is Training You to Tamper.”**

### 3. Add “failure-demand accounting” to expose automation-created work

The concept treats debugging as wasted attention but does not classify why that work exists. Add John Seddon’s distinction between value demand and failure demand from *[Freedom from Command and Control](https://shop.vanguard-method.net/products/freedom-from-command-and-control)*. Sentence pattern: **“This operator action exists because the system failed to provide X at the moment of decision.”**

“Why did I get zero jobs?” is failure demand created by telemetry that reports execution without explaining outcome. The fix is not another uptime metric; every zero-result run should emit a typed cause such as `source_empty`, `filter_rejected_all`, `scorer_unavailable`, `route_deferred`, or `valid_market_zero`, plus the evidence supporting that classification.

This unlocks an **agent observability spec and failure-demand register** measuring minutes of human investigation caused per run. That artifact reaches beyond job hunting: it demonstrates a reusable agentic-engineering principle—optimize fleets for reduced operator demand, not successful process completion.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
