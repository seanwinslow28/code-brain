---
title: "How to make `System Constraints` better"
type: expansion
parent: "[[system-constraints]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-01
updated: 2026-06-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[system-constraints]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “graceful degradation budgets” anchored on Nancy Leveson’s _Engineering a Safer World_**

   Current concept treats constraints as routing boundaries: LDR cannot do compound research, so Gemini DR gets the job. Missing layer: the system-safety view that constraints should define **controlled degradation states**, not just tool selection.

   Add a facet like: “Every research route needs a degradation budget: what quality can fall, what must never fall, and what partial artifact is still safe to emit.”

   Exemplary work: Nancy Leveson, _Engineering a Safer World: Systems Thinking Applied to Safety_.

   This unlocks a **research-agent incident runbook**: `if citation grounding confidence drops below X, emit a scoped bibliography stub, not a synthesized article.` Sean could turn this concept into an agent spec for “safe partial output,” instead of only “route complex jobs to Gemini.”

2. **Add “satisficing under bounded rationality” anchored on Herbert Simon’s _Administrative Behavior_**

   The article frames system constraints as hard operational limits, but it misses the decision-theory lens: agents are not failing because they are dumb; they are operating inside bounded information, time, and search capacity.

   Add: “System constraints convert optimal-answer seeking into satisficing. The right design question is not ‘which tool is best?’ but ‘what answer quality is good enough under this time/citation/search budget?’”

   Exemplary work: Herbert A. Simon, _Administrative Behavior_.

   This unlocks a **routing policy artifact** with explicit thresholds: single-target factual lookup = local LDR; multi-target synthesis = Gemini DR; speculative map = local model allowed if labeled “hypothesis only.” Right now the concept says “compound prompts fail”; Simon gives Sean a principled way to specify when “good enough” is acceptable.

3. **Add “premortem / red-team gate” anchored on Gary Klein’s HBR essay “Performing a Project Premortem”**

   Current concept documents observed failures after the fact: timeout, citation collapse, fabricated URLs. Missing technique: force the agent to predict the likely failure mode before execution and choose a safer route up front.

   Add a “premortem gate” sentence pattern: “Before running research, the agent must answer: ‘If this output were later found unusable, what would the failure be: timeout, citation fabrication, shallow synthesis, stale source, or scope explosion?’”

   Exemplary work: Gary Klein, “Performing a Project Premortem,” _Harvard Business Review_.

   This unlocks an **executable preflight checklist** for the research queue. Instead of relying on Sean to know that “three independent investigations” should bypass LDR, the agent can classify failure risk before spending 900 seconds. This would also make a strong Substack essay: “My Research Agent Needed a Premortem, Not a Bigger Model.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
