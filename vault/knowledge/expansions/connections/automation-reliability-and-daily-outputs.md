---
title: "How to make `Automation Reliability and Daily Outputs` better"
type: expansion
parent: "[[automation-reliability-and-daily-outputs]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-25
updated: 2026-08-25
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-daily-outputs]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “agent health” with output SLOs and error budgets

**Add:** A user-journey SLO for each daily artifact. Example: “By 08:45, the daily note exists, contains a current overnight digest, and identifies every deferred agent.” Measure successful outputs—not whether processes ran.

**Anchor:** Chris Jones, John Wilkes, and Niall Murphy, [“Service Level Objectives” in *Site Reliability Engineering*](https://sre.google/sre-book/service-level-objectives/). Their key move is distinguishing indicators from objectives and explicitly budgeting acceptable failure.

**Sentence pattern:** “During any rolling 28-day window, ≥27 daily notes satisfy existence, freshness, completeness, and provenance checks; exhausting that error budget freezes fleet expansion.”

**Unlocks:** An executable `daily-output-slo.yaml`, burn-rate dashboard, and portfolio one-pager showing Sean can translate infrastructure telemetry into product-facing reliability. The current concept cannot distinguish “seven healthy agents produced stale sludge” from “Sean received a useful morning briefing.”

## 2. Add recovery-oriented computing—not just failure prevention

**Add:** Recovery as a first-class capability: recovery-time objectives, replayability, last-known-good artifacts, idempotent reruns, checkpoint boundaries, and fault-injection drills. Track “time from missing note detected to trustworthy note restored.”

**Anchor:** David Patterson et al., [“Recovery-Oriented Computing: Motivation, Definition, Techniques, and Case Studies”](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2002/5574.html). ROC argues that designing for rapid, dependable recovery can outperform attempts to prevent every failure.

**Sentence pattern:** “Every daily-output producer must support detection, bounded replay, verification, and rollback; a killed dependency at 08:29 must yield either a verified artifact or an explicit degraded-state manifest by 08:45.”

**Unlocks:** A fleet-recovery runbook plus an executable GameDay demo that kills Ollama, removes MBP availability, corrupts an intermediate artifact, and measures recovery. That is much stronger agentic-engineering evidence than another health dashboard—and the present concept has no account of repairability.

## 3. Add an “Ironies of Automation” test

**Add:** A contradicting framework: reliable automation can make the overall human system less resilient. As routine work disappears, Sean receives only rare anomalies precisely when his situational awareness and manual skill are weakest.

**Anchor:** Lisanne Bainbridge, [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468) (1983), which shows how automation can expand the operator’s problems while leaving humans responsible for abnormal conditions.

**Sentence pattern:** “For each automated output, record what Sean no longer observes, which skill decays, what anomaly returns control to him, and whether enough context survives for competent intervention.”

**Unlocks:** An automation-allocation decision record, monthly manual-recovery rehearsal, and a contrarian Substack essay: **“My Agent Fleet Worked Every Night—and Made Me Worse at Thinking.”** The current article assumes consistency is inherently beneficial; Bainbridge supplies the missing test of whether the automation preserves judgment, attention, and meaningful control.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
