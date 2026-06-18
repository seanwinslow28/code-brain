---
title: "How to make `Research Methodology Integration` better"
type: expansion
parent: "[[research-methodology-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-17
updated: 2026-06-17
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-methodology-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Protocol Before Retrieval” mode**
   - **Anchor:** Barbara Kitchenham & Stuart Charters, *Guidelines for Performing Systematic Literature Reviews in Software Engineering*; PRISMA 2020 Statement by Page et al.
   - **Pattern to add:** every research item gets a tiny protocol before execution: `question`, `inclusion criteria`, `exclusion criteria`, `source classes`, `extraction fields`, `stop rule`, `confidence grade`.
   - **Unlocks:** a research runbook and agent spec where Gemini DR / LDR are not just tiered by cost and depth, but governed by evidence discipline. Current concept says “which tool runs the question”; this would let Sean ship “how the answer earns trust.”

2. **Add “Analysis of Competing Hypotheses” as the critic layer**
   - **Anchor:** Richards J. Heuer Jr., *Psychology of Intelligence Analysis*, especially the ACH method.
   - **Pattern to add:** each research output must name 2-4 rival hypotheses, then score evidence by whether it confirms, contradicts, or is diagnostic against each one. Sentence pattern: “The strongest evidence against my preferred answer is…”
   - **Unlocks:** a vault-critic upgrade, decision pre-mortem template, or Substack essay about “agentic research that tries to disprove itself.” Current concept integrates research machinery; ACH would integrate adversarial judgment.

3. **Add “Wicked Problem / IBIS Mapping” for questions that should not become reports**
   - **Anchor:** Horst Rittel & Melvin Webber, “Dilemmas in a General Theory of Planning”; Werner Kunz & Horst Rittel, *Issues as Elements of Information Systems*; Jeff Conklin, *Dialogue Mapping*.
   - **Pattern to add:** distinguish `answerable research questions` from `wicked coordination questions`. Represent the latter as `Issue -> Positions -> Arguments`, not as a synthesized memo.
   - **Unlocks:** an executable “research-to-decision map” artifact for product strategy, job-hunt positioning, and agent architecture tradeoffs. The current concept treats research as knowledge acquisition; IBIS would let Sean model unresolved tension without prematurely flattening it into summary prose.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
