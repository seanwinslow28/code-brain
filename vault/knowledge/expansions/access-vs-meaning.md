---
title: "How to make `Access vs Meaning` better"
type: expansion
parent: "[[access-vs-meaning]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-08
updated: 2026-06-08
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[access-vs-meaning]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “relevance as situated action,” anchored on Lucy Suchman’s _Plans and Situated Actions_**

   The missing distinction is not just access vs meaning; it is **plan-following vs situated interpretation**. Your agent had a plan: scan files, retrieve notes, produce concepts. What it lacked was the ability to treat each file as part of an unfolding situation where relevance changes based on context.

   Add a mode like:

   > Access answers “can I touch it?” Meaning answers “what situation am I in, and what would count as a useful next move?”

   **Exemplar:** Lucy Suchman, _Plans and Situated Actions: The Problem of Human-Machine Communication_.

   **Unlocks:** A stronger agent spec/runbook genre: “situated retrieval protocols.” Instead of telling the synthesizer to process 30 files, you can specify situational tests: “What kind of note is this? What job is it doing? What downstream action could it change?” This turns the article from a failure memoir into an evaluable design pattern for agent reading.

2. **Add “information scent,” anchored on Peter Pirolli and Stuart Card’s paper “Information Foraging in Information Access Environments”**

   The concept currently treats meaning as judgment, but it does not yet name the intermediate layer: **cues that help an agent decide whether something is worth pursuing before fully reading it**. Humans do this constantly. Agents need explicit scent markers.

   Add a sentence pattern like:

   > Meaning does not begin at the answer. It begins at the trailhead: titles, backlinks, timestamps, verbs, unresolved questions, repeated phrases, and friction points that tell the agent whether a note is food or sawdust.

   **Exemplar:** Peter Pirolli and Stuart Card, “Information Foraging in Information Access Environments.”

   **Unlocks:** A concrete artifact: a **vault scent schema** or **retrieval triage rubric**. Example fields: `decision_pressure`, `reuse_signal`, `contradiction_signal`, `artifact_potential`, `staleness_risk`. This would let the nightly fleet rank notes before synthesis instead of treating all reachable markdown as equal input.

3. **Add “felicity conditions,” anchored on J. L. Austin’s _How to Do Things with Words_**

   Your current failure mode is “green checkmarks hid useless output.” Austin gives you a sharper weapon: an action can be syntactically complete and still **misfire** because the conditions for a meaningful act were not present. The agent did not merely fail to understand; it performed an invalid speech act and the system counted it as valid.

   Add a frame like:

   > A successful agent run is not one that completes. It is one whose act is felicitous: the right action, by the right agent, under the right conditions, producing the intended change in the world.

   **Exemplar:** J. L. Austin, _How to Do Things with Words_, especially the theory of performative utterances and misfires.

   **Unlocks:** A portfolio-grade essay and an eval artifact: **“felicity tests for agents.”** Instead of metrics like files read, tokens spent, or concepts written, define conditions under which “synthesis” actually counts as synthesis. This gives you a named critique of fake productivity that is more durable than “agents need judgment.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
