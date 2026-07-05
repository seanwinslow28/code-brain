---
title: "How to make `The Illusion of Health in Autonomous Systems` better"
type: expansion
parent: "[[the-illusion-of-health-in-autonomous-systems]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-30
updated: 2026-06-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[the-illusion-of-health-in-autonomous-systems]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Drift Into Failure” as the contradiction layer.**  
   **Anchor:** Sidney Dekker, *Drift into Failure: From Hunting Broken Components to Understanding Complex Systems*.

   The missing facet is that “green dashboards” are not just bad summaries; they are part of how systems normalize deviance. Add a section arguing that autonomous systems do not usually fail because one agent suddenly breaks, but because locally rational adaptations accumulate until the control plane’s model is fiction.

   **Sentence pattern:** “The dashboard is not lying; it is faithfully reporting the system-as-imagined after the system-as-done has drifted away.”

   **Unlocks:** A stronger Substack essay or portfolio artifact: “Why My Agent Fleet Needs Incident Archeology, Not Just Health Checks.” This moves the concept from observability critique into a theory of autonomous-system degradation.

2. **Add “Error Budgets for Cognitive Handoffs.”**  
   **Anchor:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy, *Site Reliability Engineering: How Google Runs Production Systems*, especially the error-budget framing.

   Your concept says aggregate health obscures handoff failures, but it lacks an operational replacement. Add a named pattern: each agent-to-agent boundary gets a budget for stale context, missing artifacts, skipped writes, late outputs, and silent fallbacks. Health becomes “how much coordination risk remains,” not “did the script exit 0.”

   **Sentence pattern:** “The unit of reliability is not the agent; it is the handoff contract.”

   **Unlocks:** An executable runbook or agent spec for Code-Brain: `handoff-error-budget.md`, with thresholds like “daily note stale > 1 run = yellow,” “context index older than 24h = degraded,” “critic partial twice in a row = incident.” This turns the concept into an implementation standard.

3. **Add “Common Ground Breakdown” from joint activity theory.**  
   **Anchor:** Gary Klein, Paul J. Feltovich, Jeffrey M. Bradshaw, and David D. Woods, “Common Ground and Coordination in Joint Activity” in *Organizational Simulation*.

   Right now the article frames failure as observability debt. The missing human-agent facet is common ground: whether Sean and the fleet still share the same assumptions about task state, priorities, available context, and completion criteria. A green system can still be dangerous if it has lost shared context with its human operator.

   **Sentence pattern:** “Agent health is not whether the agent completed its task; it is whether Sean and the agent still agree about what just happened.”

   **Unlocks:** A product-management artifact: an “Agent Fleet Common Ground Checklist” or dashboard design spec. Instead of status pills, the UI would surface belief alignment: latest artifact seen, assumed next action, confidence, stale dependencies, and what the agent thinks Sean needs next. This would make the concept useful for AI-PM interviews because it reframes observability as human-agent coordination design.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
