---
title: "How to make `Infrastructure Monitoring and Daily Routines` better"
type: expansion
parent: "[[infrastructure-monitoring-and-daily-routines]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-30
updated: 2026-08-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[infrastructure-monitoring-and-daily-routines]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add “output-contract mode,” anchored on Spotify/Google’s pipeline SLOs

The concept monitors whether agents ran; it never defines whether Sean received a usable product. Add the framework from Rita Sodt, Igor Maravić et al., [“Data Processing Pipelines,” *The Site Reliability Workbook*](https://sre.google/workbook/data-processing/): measure **freshness, completeness, and correctness** independently.

For the daily note:

- Freshness: rendered by 08:35.
- Completeness: all required fleet sections populated.
- Correctness: dates, links, and run statuses pass synthetic probes.
- Degraded success: evergreen skeleton delivered, explicitly marked stale.

Because this is a low-frequency batch service—roughly 30 executions monthly—generic availability percentages and conventional burn-rate alerts will be noisy. This unlocks an **executable reliability contract**, portfolio-ready SLO one-pager, and acceptance-test suite. The current concept can say “the agent succeeded”; this addition can prove “the morning artifact was fit for use.”

### 2. Add “defenses-in-depth failure mode,” anchored on Richard Cook’s *How Complex Systems Fail*

Replace the article’s linear claim—unhealthy agent → disrupted routine—with Cook’s argument that failures emerge from interacting latent conditions and that successful systems are already operating with many hidden defects. See Richard I. Cook, [*How Complex Systems Fail*](https://worrydream.com/refs/Cook_2000_-_How_Complex_Systems_Fail.pdf).

Sentence pattern:

> “The missing daily note was not caused by component X; it became possible when defenses A, B, and C were simultaneously absent, stale, or bypassed.”

Apply that to the 401 incident: expiring interactive authentication, unattended launchd execution, missing durable-token validation, and no degraded note path formed the accident—not merely “daily-driver failed.”

This unlocks a **Cook-style incident review template** with contributing conditions, failed defenses, near misses, and recovery capacity. It also supports a sharp Substack essay—“Your Agent Didn’t Cause the Incident”—and gives Sean a systems-safety portfolio artifact stronger than a dashboard screenshot.

### 3. Add “operator-readiness mode,” anchored on Lisanne Bainbridge’s *Ironies of Automation*

The concept assumes more monitoring automatically improves Sean’s routine. Bainbridge’s contradiction is that automation can make the remaining human work rarer, harder, and more cognitively demanding: the operator is left to intervene precisely when context is worst. See Lisanne Bainbridge, [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468).

Add three measures alongside agent health:

- time for Sean to understand an alert;
- ability to reconstruct the last known-good state;
- ability to perform the routine manually after weeks of automation.

Then specify **handoff quality**, not merely alert delivery: “what failed, user impact, safe next action, rollback point, and what must not be retried.”

This unlocks a **human-takeover drill**, alert-writing standard, and recovery runbook. It also creates the contrarian essay “The Healthier My Agent Fleet Became, the Less Ready I Was to Operate It”—a claim the current infrastructure-centric concept cannot reach.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
