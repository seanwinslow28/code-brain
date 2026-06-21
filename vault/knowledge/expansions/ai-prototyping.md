---
title: "How to make `AI Prototyping` better"
type: expansion
parent: "[[ai-prototyping]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-20
updated: 2026-06-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[ai-prototyping]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “prototype-as-argument,” anchored on Michael Schrage’s _Serious Play_**

   Current concept treats AI prototyping as interview execution: build something fast to prove fluency. Missing facet: prototypes are not just demos; they are arguments that force a decision.

   Add a section: **Prototype-as-argument mode**. Sentence pattern: “This prototype is not the product; it is a disposable artifact designed to make one disputed assumption visible.”

   Exemplar: Michael Schrage, _Serious Play: How the World’s Best Companies Simulate to Innovate_.

   Unlocks: Sean can produce an **interview prototype memo** or **portfolio case artifact** where the deliverable is not “look, I made a Cursor app,” but “here is the decision this prototype de-risks.” That maps better to senior PM and AI-PM interviews, where the evaluator cares less about code volume and more about judgment under ambiguity.

2. **Add “Wizard-of-Oz AI prototype,” anchored on Bill Buxton’s _Sketching User Experiences_**

   Current concept over-indexes on working AI tools. Missing contradiction: the best AI prototype may fake the AI entirely, especially when testing whether users understand, trust, or want the behavior.

   Add: **Wizard-of-Oz mode for agentic UX**. Sentence pattern: “Before building the model/tool/agent, simulate the intelligence with a human, script, or fixture and test the interaction contract.”

   Exemplar: Bill Buxton, _Sketching User Experiences_, especially his distinction between sketches, prototypes, and design exploration.

   Unlocks: Sean can produce a **runbook for interview take-homes**: when to build real automation vs when to fake the agent and test the workflow. This is directly useful for AI-PM roles because it shows he understands product risk, not just implementation speed. It also gives him a sharper critique of “vibe-coded demo theater”: many demos answer “can I build this?” before answering “is this the right interaction?”

3. **Add “concierge MVP / manual-first automation,” anchored on Eric Ries’s _The Lean Startup_**

   Current concept frames AI prototyping as rapid technical proof. Missing facet: sometimes the correct prototype is deliberately non-scalable, because the learning target is demand, behavior, or willingness-to-change, not feasibility.

   Add: **Concierge-agent prototype**. Sentence pattern: “Run the agent’s intended service manually once, write the transcript, then automate only the repeated judgment/action loop.”

   Exemplar: Eric Ries, _The Lean Startup_, specifically the concierge MVP pattern.

   Unlocks: Sean can produce an **agent spec** that starts from observed manual service traces instead of imagined agent capabilities. For Code-Brain, this would let him turn “my fleet summarizes my vault” into “what judgment did I manually wish the agent had made?” For job-hunt artifacts, it becomes a strong **AI-PM one-pager**: problem, manual concierge trial, repeated decision pattern, automation boundary, eval criteria.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
