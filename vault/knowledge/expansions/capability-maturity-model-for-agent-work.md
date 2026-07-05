---
title: "How to make `Capability Maturity Model for Agent Work` better"
type: expansion
parent: "[[capability-maturity-model-for-agent-work]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-30
updated: 2026-06-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[capability-maturity-model-for-agent-work]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add a “traceability case-file” layer, anchored on Andrew Abbott’s _Time Matters: On Theory and Method_**

   The current model names maturity levels, but it does not say how Sean proves movement between levels over time. Add a case-file pattern: each level claim must cite dated traces, failed runs, revisions, and governance decisions.

   **Exemplar:** Andrew Abbott, _Time Matters: On Theory and Method_.

   **Sentence pattern:** “This system was not Level 4 because it had evals; it became Level 4 when repeated failures produced a named control loop, a changed schedule, and a durable audit artifact.”

   **Unlocks:** A portfolio one-pager or Substack essay that reads like operational history instead of self-assessment. Recruiters see judgment under temporal pressure, not a static rubric.

2. **Add a “safety case” facet, anchored on Nancy Leveson’s _Engineering a Safer World_ / STAMP**

   Your maturity ladder currently implies progress is mostly more measurement, more governance, more optimization. Leveson’s STAMP framework adds the missing contradiction: mature systems are not merely better-instrumented; they have explicit control structures, unsafe control actions, feedback paths, and responsibility boundaries.

   **Exemplar:** Nancy Leveson, _Engineering a Safer World: Systems Thinking Applied to Safety_.

   **Sentence pattern:** “Level 5 is not autonomous optimization; Level 5 is when the agent system can explain which controls prevent which unsafe actions, and where feedback would reveal control failure.”

   **Unlocks:** An agent-fleet governance runbook or “control architecture” diagram for Code-Brain. This would let Sean discuss agent safety in concrete engineering terms rather than sounding like he is just adding evals and dashboards.

3. **Add a “situated action” objection, anchored on Lucy Suchman’s _Plans and Situated Actions_**

   The concept risks over-ranking planned maturity and under-ranking adaptive work. Suchman’s argument is the useful counterweight: plans do not fully determine action; real work emerges through situated improvisation. For agent work, that means maturity cannot only mean cleaner specs, workflows, and eval loops. It must also account for how agents recover when context shifts, tools misfire, or the user’s actual intent changes midstream.

   **Exemplar:** Lucy Suchman, _Plans and Situated Actions: The Problem of Human-Machine Communication_.

   **Sentence pattern:** “A Level 4 agent is not one that follows the plan; it is one whose trace shows when the plan stopped being the right object of obedience.”

   **Unlocks:** A sharper “agentic engineering signal” essay and an executable demo: two agents receive the same intent charter, one rigidly follows the plan, the other detects changed context and escalates. That gives Sean a concrete artifact for distinguishing agentic engineering from prompt fluency.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
