---
title: "How to make `Vault Knowledge - MCP Research` better"
type: expansion
parent: "[[vault-knowledge-mcp-research]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-12
updated: 2026-08-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[vault-knowledge-mcp-research]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “toxic-flow threat modeling,” not a vulnerability scrapbook

- **What:** Model attacks as paths connecting an **untrusted source**, a **sensitive capability**, and an **exfiltration sink**. This exposes dangerous *compositions* of individually legitimate MCP servers.
- **Anchor:** Giulio Beurer-Kellner and Invariant Labs, [“Toxic Flow Analysis”](https://invariantlabs.ai/blog/toxic-flow-analysis1). Their framework generalizes the GitHub exploit into analyzable source-to-sink flows rather than treating it as an isolated incident.
- **Unlock:** Ship an **MCP attack-path runbook and executable scanner demo** for Code-Brain: enumerate tool/resource trust labels, generate cross-server attack graphs, and fail CI when a new server completes a toxic path. The current concept can document attacks; this would predict previously unseen combinations.

## 2. Add “control/data separation” anchored on CaMeL

- **What:** Treat prompt injection as an architectural information-flow problem—not something better prompting or instruction precedence can solve. A trusted planner determines control flow; untrusted tool output remains typed data and receives only explicitly delegated capabilities.
- **Anchor:** Edoardo Debenedetti et al., [“Defeating Prompt Injections by Design”](https://arxiv.org/abs/2503.18813). CaMeL combines explicit control/data-flow extraction with capability-based enforcement and reports provable security on a substantial portion of AgentDojo tasks.
- **Unlock:** Ship an **executable intent-engineering MCP demo** where the seven-part intent specification compiles into capabilities and flow constraints: “GitHub issue text may influence classification but may never select a credential-reading or outbound-network action.” This gives Sean a concrete answer to the hard question his current I-5 framing cannot reach: *how does declared intent remain authoritative after hostile context enters the agent?*

## 3. Add “resource-bound delegation” as a separate threat class

- **What:** Separate prompt injection from OAuth delegation failures: confused deputies, token passthrough, audience confusion, and consent laundering. Required pattern: one audience-bound token per resource; never relay an inbound bearer token downstream; record consent per client.
- **Anchor:** Dick Hardt, [RFC 8707: “Resource Indicators for OAuth 2.0”](https://www.rfc-editor.org/rfc/rfc8707), applied concretely by the MCP specification’s [Authorization requirements](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization). The specification requires the `resource` parameter, audience validation, separate downstream tokens, and prohibits token passthrough.
- **Unlock:** Ship an **MCP authorization decision record plus conformance harness** containing adversarial tests for wrong-audience tokens, reused consent cookies, passthrough, and proxy-client confusion. That artifact would demonstrate security engineering judgment to AI-PM and agentic-IC employers; the current concept collapses authentication roadmap items into “security” without specifying the authority boundaries that actually prevent delegation attacks.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
