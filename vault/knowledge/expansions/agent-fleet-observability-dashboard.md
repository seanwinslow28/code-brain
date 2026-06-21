---
title: "How to make `Agent Fleet Observability Dashboard` better"
type: expansion
parent: "[[agent-fleet-observability-dashboard]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-21
updated: 2026-06-21
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-fleet-observability-dashboard]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Wide Events, Not Dashboards” mode**

   **What to add:** A Honeycomb-style event model: every agent run emits one rich, high-cardinality event rather than many low-cardinality counters. Sentence pattern: “For every run, preserve the nouns needed to ask questions you did not know you would have.”

   **Exemplar:** Charity Majors, Liz Fong-Jones, and George Miranda, *Observability Engineering*; especially the argument that observability depends on arbitrarily explorable events, not pre-aggregated metrics.

   **What it unlocks:** A concrete **agent telemetry schema** Sean can ship: `agent_run_id`, `intent_id`, `retrieval_query`, `candidate_sources`, `discarded_sources`, `model_route`, `fallback_reason`, `artifact_written`, `critic_verdict`, `human_override`. The current concept says “record traces”; this gives him the artifact shape for a portfolio-grade “open telemetry for personal agent fleets” spec.

2. **Add “SLO/Error Budget for Epistemic Quality”**

   **What to add:** Translate agent health from uptime to reliability promises: not “did the agent run?” but “did the agent preserve epistemic quality within an acceptable failure budget?” Define service-level indicators like citation validity rate, retrieval recall against known gold notes, unsupported-claim count, stale-context rate, and actionability score.

   **Exemplar:** Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, *Site Reliability Engineering*; especially the SLO/error-budget framing from Google SRE.

   **What it unlocks:** A **decision runbook** for when to invest in agent quality. Example: “If unsupported-claim rate exceeds 3% over 7 days, pause autonomous synthesis and route to Gemini DR / council review.” This moves Sean from descriptive fleet status into governance: when to tolerate failure, when to burn budget, when to disable an agent.

3. **Add “Data Provenance / Lineage as First-Class Memory”**

   **What to add:** Treat every concept, connection, and daily-note insertion as a lineage graph: source note → retrieval chunk → model prompt → generated claim → downstream artifact. Not just “what did the agent touch,” but “what claim depends on what evidence, through what transformation.”

   **Exemplar:** Peter Buneman, Sanjeev Khanna, and Wang-Chiew Tan, “Why and Where: A Characterization of Data Provenance” (ICDT 2001).

   **What it unlocks:** A **vault audit artifact** the current concept cannot reach: “show me every claim downstream of this bad source,” or “which concepts were polluted by a fabricated Gemini citation?” This would let Sean build a visible lineage explorer for Code-Brain, turning agent observability into knowledge-system forensics rather than another health dashboard.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
