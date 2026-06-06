---
title: "How to make `Agent Health → Automation Reliability → Daily Routine` better"
type: expansion
parent: "[[agent-health-automation-reliability-daily-routine]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-06
updated: 2026-06-06
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-automation-reliability-daily-routine]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Normal Accident Mode”**
   - **WHAT to add:** Treat daily-note disruption as an expected property of tightly coupled automation, not merely a health lapse. Add a failure-mode lens: coupling, hidden dependencies, recovery paths, graceful degradation.
   - **WHO/WHAT exemplifies it:** Charles Perrow, *Normal Accidents: Living with High-Risk Technologies*.
   - **WHAT this unlocks:** A sharper **agent-fleet reliability essay or runbook**: “My daily note failed because the system was designed to fail this way.” Sean can map which routines are tightly coupled, which are loosely coupled, and where to add buffers. Current concept says “keep agents healthy”; Perrow lets him ask, “Which automations should be allowed to fail without disrupting the morning?”

2. **Add “Error Budget for Personal Automation”**
   - **WHAT to add:** Borrow SRE’s error-budget framing: define acceptable failure rates for daily-driver, vault indexer, critic, synthesizer, and meta-agent. Sentence pattern: “This agent may fail N times per month before I spend engineering time on reliability instead of feature work.”
   - **WHO/WHAT exemplifies it:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, *Site Reliability Engineering: How Google Runs Production Systems*, especially the error-budget chapters.
   - **WHAT this unlocks:** A concrete **fleet observability policy artifact**. Sean could produce a one-page “Personal Agent SLOs” spec: daily note freshness SLO, overnight digest SLO, critic expansion SLO, acceptable partial-run rate, escalation rule. The current concept cannot distinguish inconvenience from incident; SRE gives him a decision rule for when to fix, tolerate, or retire an automation.

3. **Add “Resilience Engineering / Graceful Extensibility”**
   - **WHAT to add:** Shift from “prevent failure” to “preserve adaptive capacity.” Add a mode that asks what the human-agent system does when the plan breaks: fallback routines, handoff notes, degraded-mode outputs, visible uncertainty, manual override.
   - **WHO/WHAT exemplifies it:** David D. Woods, “The Theory of Graceful Extensibility: Basic Rules That Govern Adaptive Systems.”
   - **WHAT this unlocks:** A more mature **agent spec or portfolio case study**: “Designing a daily-driver that degrades gracefully.” Instead of “agent health causes routine reliability,” Sean can show mechanisms: stale-data banners, partial manifests, fallback templates, recovery prompts, and human re-entry points. This is especially strong for AI-PM roles because it reframes his fleet as a socio-technical operating system, not a pile of scripts.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
