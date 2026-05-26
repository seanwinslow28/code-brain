---
title: "How to make `Agent Health Monitoring` better"
type: expansion
parent: "[[agent-health-monitoring]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-26
updated: 2026-05-26
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health-monitoring]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “SLO/Error-Budget Mode” for agents**
   - **What to add:** Treat each scheduled agent as a service with an explicit SLO, error budget, burn rate, and degradation policy. Not “did it run,” but “did it preserve the user-visible workflow contract?”
   - **Anchor:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, *Site Reliability Engineering: How Google Runs Production Systems*, especially the chapters on service-level objectives and error budgets.
   - **Unlocks:** A portfolio-ready **Agent Fleet SRE Runbook**: `daily-driver morning has 99% weekly note-creation SLO; vault-critic has 90% enrichment-completion SLO; if critic burns budget, reduce targets before adding retries.` This lets Sean make operational tradeoff decisions instead of writing health blurbs. The current concept only says “agent succeeded”; SLO mode says “this failure matters / does not matter because the product promise was or was not violated.”

2. **Add “Control-Plane / Data-Plane Separation”**
   - **What to add:** Split agent health into control-plane health and data-plane health. Control plane: launchd schedule, credentials, model routing, file locks, subprocess exit codes. Data plane: note quality, citation validity, concept graph changes, downstream usefulness.
   - **Anchor:** Brendan Burns, *Designing Distributed Systems*, especially the sidecar/ambassador/adapter patterns as reusable distributed-system control structures.
   - **Unlocks:** An **Agent Architecture One-Pager** for job interviews: “My vault agents are not scripts; they are a small distributed system with a control plane, artifact bus, health manifests, and downstream semantic QA.” This gives Sean language that maps his homebuilt fleet to infrastructure patterns senior engineers recognize. The current concept collapses all failures into “agent health,” which hides whether the problem is orchestration, model quality, retrieval, or user-facing value.

3. **Add “Resilience Engineering / Graceful Degradation Mode”**
   - **What to add:** Evaluate agents by their ability to fail partially, recover, and preserve human situational awareness. Add concepts like graceful degradation, fallback behavior, incident learning, and “what did the human still know in time to act?”
   - **Anchor:** Sidney Dekker, *The Field Guide to Understanding “Human Error”*; also Richard Cook, “How Complex Systems Fail.”
   - **Unlocks:** A sharper **Substack essay or incident postmortem template**: “My daily-driver failed, but the fleet degraded correctly: the meta-agent detected the missing daily note, the manifest preserved evidence, and the next interactive session knew what to backfill.” This moves Sean from uptime theater to resilience critique. The current concept treats failure as a binary defect; resilience mode asks whether the system made failure legible, bounded, and recoverable.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
