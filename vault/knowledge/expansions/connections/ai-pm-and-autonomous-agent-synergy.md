---
title: "How to make `AI-PM and Autonomous Agent Synergy` better"
type: expansion
parent: "[[ai-pm-and-autonomous-agent-synergy]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-24
updated: 2026-06-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[ai-pm-and-autonomous-agent-synergy]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “control-plane PM” anchored on James C. Scott’s _Seeing Like a State_**

   The concept currently says AI-PM + agent health = “optimize and monitor agents.” That is too inside-the-system. Add the missing contradiction: every observability layer is also a simplification layer that can make local reality illegible.

   Pattern to add: **legibility debt** — the gap between what the dashboard can see and what the agent/user situation actually requires.

   Unlock: a Substack essay or portfolio one-pager called **“Agent Fleet Observability Is a Product Surface, Not a Log Viewer.”** It would let Sean argue that AI-PMs need to design for failures of measurement, not just failures of automation. Current concept only reaches “monitor agent health”; Scott lets it reach “what monitoring destroys or blinds.”

2. **Add “joint cognitive system” anchored on David D. Woods & Erik Hollnagel’s _Joint Cognitive Systems: Foundations of Cognitive Systems Engineering_**

   The article treats autonomous agents as tools PMs design and inspect. Missing facet: Sean is actually building **human-agent joint cognition**, where performance emerges from the coupling between Sean, vault, scheduled agents, hooks, runbooks, and escalation paths.

   Pattern to add: **coordination surfaces over automation surfaces** — design the handoffs, interruption points, confidence signals, and recovery paths as first-class product requirements.

   Unlock: an agent spec or runbook genre the concept cannot currently produce: **“Human-Agent Handoff Spec.”** Sections could include authority boundary, evidence shown to human, confidence/uncertainty display, recovery action, audit artifact, and post-failure learning. This upgrades Sean’s AI-PM positioning from “I manage agent workflows” to “I design resilient human-agent operating systems.”

3. **Add “promise theory” anchored on Mark Burgess’s _In Search of Certainty: The Science of Our Information Infrastructure_**

   The concept frames agents as automation routines that should be reliable. Missing framework: in distributed autonomous systems, you do not truly command components; you model what each actor promises to do, observe whether promises hold, and design around partial trust.

   Pattern to add: **agent promises, not agent tasks** — each scheduled agent should declare what it promises, what it depends on, what it refuses to promise, and what evidence proves fulfillment.

   Unlock: an executable demo or portfolio artifact: **“Agent Promise Ledger.”** For Code-Brain, each agent gets a promise contract: `promise`, `dependencies`, `health signal`, `breach condition`, `fallback`, `audit path`. This would sharpen the intent-engineering MCP work because “intent” becomes operationally checkable instead of aspirational. Current concept says “agent health monitoring”; Burgess lets Sean ship a governance primitive.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
