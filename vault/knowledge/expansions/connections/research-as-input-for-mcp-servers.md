---
title: "How to make `Research as Input for MCP Servers` better"
type: expansion
parent: "[[research-as-input-for-mcp-servers]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-16
updated: 2026-06-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-as-input-for-mcp-servers]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “decision-rationale mode,” not just research-input mode.**  
   Anchor it on Horst Rittel & Werner Kunz, *Issues as Elements of Information Systems* (1970), the IBIS origin paper. The missing move is: research should not merely precede MCP implementation; it should produce an argument graph of **issue → positions → arguments → chosen constraint**. Sentence pattern: “Because SOURCE shows RISK, this MCP server chooses POSITION over ALTERNATIVE, and records REJECTED OPTION because FAILURE MODE.”  
   **Unlocks:** a publishable agent spec / ADR format for `intent-engineering MCP`: “research-backed MCP design rationale.” Right now the concept proves discipline; IBIS would let Sean ship decision artifacts that show judgment under ambiguity.

2. **Add “situated-use evidence mode.”**  
   Anchor it on Lucy Suchman, *Plans and Situated Actions: The Problem of Human-Machine Communication* (1987), later expanded as *Human-Machine Reconfigurations* (2007). Suchman is the contradiction to the article’s current assumption: plans and research do not determine competent action; real work is improvised inside messy material situations. Sentence pattern: “This MCP server is justified not by abstract architecture research alone, but by EPISODE: user tried to do TASK, context broke at POINT, server affordance repairs BREAKDOWN.”  
   **Unlocks:** a Substack essay or portfolio one-pager where Sean moves from “I research before building” to “I derive MCP tools from observed workflow breakdowns.” That is a stronger AI-PM signal because it connects research to lived task evidence, not just citation hygiene.

3. **Add “assurance-case mode” for MCP servers.**  
   Anchor it on Tim Kelly, *Arguing Safety: A Systematic Approach to Managing Safety Cases* (1998), and the Goal Structuring Notation lineage. The missing facet is proof burden. If MCP servers expose tools to agents, “deep research returned architecture validation” is insufficient; the server needs an explicit claim-evidence-risk structure. Sentence pattern: “Claim: this MCP server may safely expose ACTION under CONDITIONS. Evidence: TEST / TRACE / CONSTRAINT. Rebuttal: known failure case. Mitigation: STOP RULE / PERMISSION BOUNDARY.”  
   **Unlocks:** an executable demo or runbook: “MCP Assurance Case Template.” This would connect Sean’s intent-engineering work to governance, auditability, and agent safety in a way the current concept cannot reach.

Sources: [Alexander context](https://en.wikipedia.org/wiki/Notes_on_the_Synthesis_of_Form), [Suchman overview](https://en.wikipedia.org/wiki/Lucy_Suchman), [situated action summary](https://en.wikipedia.org/wiki/Situated_cognition), [second-order cybernetics context](https://en.wikipedia.org/wiki/Second-order_cybernetics).

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
