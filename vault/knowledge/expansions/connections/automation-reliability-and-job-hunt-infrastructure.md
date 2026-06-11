---
title: "How to make `Automation Reliability and Job-Hunt Infrastructure` better"
type: expansion
parent: "[[automation-reliability-and-job-hunt-infrastructure]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-11
updated: 2026-06-11
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-job-hunt-infrastructure]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Job-Hunt SLOs + Error Budgets”**
   - **Anchor:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, *Site Reliability Engineering*, especially “Embracing Risk” and “Service Level Objectives.”
   - **What’s missing:** The concept says “robust fallback strategies,” but it never defines acceptable failure. Add a small SLO table: daily note created by 8:45 AM, job-feed rollup fresh by 11:00 AM, zero missed high-fit roles older than 24h, manual recovery under 15 minutes.
   - **Unlocks:** A real **agent-fleet reliability runbook** and portfolio artifact: “I operate my job hunt with SRE-style SLOs.” It turns vague reliability into decisions: when to tolerate MBP outages, when to degrade to Mac Mini-only, when to page Sean, and when to stop adding automation.

2. **Add “Graceful Extensibility,” Not Just Fallbacks**
   - **Anchor:** David D. Woods, *The Theory of Graceful Extensibility: Basic Rules that Govern Adaptive Systems*.
   - **What’s missing:** Current framing treats reliability as failover: MBP unavailable, use fallback. Woods’ sharper point is that resilient systems stretch at the boundary before they collapse. Add a “graceful extensibility mode” for the fleet: reduced ambition, preserved core promises, explicit human handoff.
   - **Unlocks:** An **agent spec** Sean cannot currently write: `degraded_job_hunt_mode.md`, where agents stop trying to synthesize deeply and instead preserve only the minimum viable loop: collect jobs, flag blockers, maintain daily note continuity, queue research for later. This also supports a strong Substack essay: “The difference between fallback automation and adaptive automation.”

3. **Add the Contradiction: “Normal Accidents” / Tight Coupling Risk**
   - **Anchor:** Charles Perrow, *Normal Accidents: Living with High-Risk Technologies*.
   - **What’s missing:** The article assumes more reliability infrastructure reduces job-hunt risk. Perrow gives the counterframe: tightly coupled, complex systems create failures that are not bugs but system properties. Sean’s fleet has launchd schedules, local models, OAuth gaps, Obsidian-Git ownership, portfolio deploys, and private-layer constraints. That is exactly where hidden coupling matters.
   - **Unlocks:** A **decision record or pre-mortem**: “Where Code-Brain should stay manual.” This would produce sharper governance than “improve automation reliability”: identify which workflows deserve automation, which need kill switches, and which should remain human-review-only because a silent failure would damage job-hunt trust.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
