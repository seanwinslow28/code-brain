---
title: "How to make `AdOps Automation` better"
type: expansion
parent: "[[adops-automation]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-20
updated: 2026-06-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[adops-automation]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “service blueprint failure modes”**
   - **What to add:** Treat AdOps Automation as a *frontstage/backstage service system*, not just an intake pipeline. Add a facet for handoffs, exception paths, support roles, and invisible labor.
   - **Anchor:** G. Lynn Shostack, “Designing Services That Deliver” (*Harvard Business Review*, 1984). Also useful: Marc Stickdorn et al., *This Is Service Design Doing*.
   - **Unlocks:** A portfolio artifact Sean currently cannot produce: a **before/after AdOps service blueprint** showing client, sales, AdOps, creative, trafficking, QA, and reporting lanes. This turns “automation reduces manual workload” into “here are the exact coordination failures the system removes or preserves.”

2. **Add “Westrum generative culture” as the contradicting frame**
   - **What to add:** Automation is not automatically good. Add the question: does this system create a *generative information culture*, or does it merely accelerate a bureaucratic one?
   - **Anchor:** Ron Westrum, “A Typology of Organisational Cultures” / the Westrum organizational culture model, later operationalized in Nicole Forsgren, Jez Humble, and Gene Kim’s *Accelerate*.
   - **Unlocks:** A sharper **AI-PM decision memo**: “Which AdOps decisions should be automated, which should be surfaced, and which should remain human-owned?” Current concept says automation improves efficiency; this frame lets Sean critique whether automation improves information flow, accountability, and recovery from campaign mistakes.

3. **Add “exception-first automation design”**
   - **What to add:** Define the system by its exception taxonomy, not its happy path: missing assets, bad specs, late creative, mismatched UTM, wrong sponsor copy, sales override, client revision, campaign underdelivery, policy/legal concern.
   - **Anchor:** Richard Cook, “How Complex Systems Fail” and Sidney Dekker, *The Field Guide to Understanding Human Error*.
   - **Unlocks:** A concrete **agent spec / runbook**: “AdOps Intake Agent: normal path, uncertainty classes, escalation triggers, audit log, recovery protocol.” This moves the concept from generic workflow automation into agentic-operations design: what the agent may decide, when it must stop, and how humans recover when the pipeline is wrong.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
