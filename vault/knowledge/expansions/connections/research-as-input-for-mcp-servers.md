---
title: "How to make `Research as Input for MCP Servers` better"
type: expansion
parent: "[[research-as-input-for-mcp-servers]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-17
updated: 2026-06-17
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-as-input-for-mcp-servers]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Design Science Research mode”**
   - **What:** Recast research input as a `relevance -> rigor -> design/evaluate` loop, not a pre-coding checkpoint.
   - **Anchor:** Alan Hevner, Salvatore March, Jinsoo Park, Sudha Ram, “[Design Science in Information Systems Research](https://en.wikipedia.org/wiki/Design_science_%28methodology%29)” (MIS Quarterly, 2004).
   - **Unlocks:** A portfolio-grade **research-to-artifact case study**: “I built an MCP server as a design-science artifact.” Current concept only says research validates architecture; DSR lets Sean show contribution type: construct, model, method, instantiation. Artifact to ship: a one-page MCP case template with sections for problem relevance, prior knowledge, artifact, evaluation, and communication.

2. **Add “Pretotyping veto mode”**
   - **What:** Contradict the premise “no code until deep research returns.” Add a rule: for uncertain demand or interface value, run a fake-door / concierge / mechanical-Turk pretotype before deep architecture research.
   - **Anchor:** Alberto Savoia, *The Right It* / [Pretotyping.org](https://www.pretotyping.org/), especially the “Right It before building it right” frame.
   - **Unlocks:** A sharper decision rule for MCP work: **research-first when implementation risk dominates; pretotype-first when desirability risk dominates.** Current concept makes rigor sound like delay. This unlocks a Substack essay or runbook titled “When Deep Research Is Procrastination,” with examples: mock MCP tool responses, transcript-based fake server, CLI stub, or one-user concierge workflow before real protocol work.

3. **Add “Assurance case mode”**
   - **What:** Treat research citations as evidence in a structured claim tree: claim -> strategy -> subclaim -> evidence -> assumption -> defeater.
   - **Anchor:** Tim Kelly, *Arguing Safety: A Systematic Approach to Managing Safety Cases* (1998), and Goal Structuring Notation / [GSN](https://en.wikipedia.org/wiki/Goal_structuring_notation).
   - **Unlocks:** An **agent-governance artifact** the current concept cannot reach: “Why this MCP server is safe/reliable enough to expose to agents.” Instead of “research informed the design,” Sean can produce an auditable MCP assurance case: claims about permission boundaries, data provenance, failure modes, citation grounding, and stop rules. This maps directly to his intent-engineering work and gives recruiters a concrete IC artifact, not just a research habit.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
