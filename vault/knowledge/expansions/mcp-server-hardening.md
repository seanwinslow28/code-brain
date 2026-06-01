---
title: "How to make `MCP Server Hardening` better"
type: expansion
parent: "[[mcp-server-hardening]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-01
updated: 2026-06-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[mcp-server-hardening]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “lethal-trifecta threat modeling,” not just path hardening.**  
   Anchor it on Simon Willison’s essay, [“The lethal trifecta for AI agents: private data, untrusted content, and external communication”](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).  
   Pattern to add: “This server is dangerous only when three capabilities co-reside: it can read private files, ingest attacker-controlled content, and transmit results outward.”  
   This unlocks a **portfolio-grade MCP security one-pager**: a matrix of each tool by `private data`, `untrusted input`, `egress`, and the specific mitigation. Current concept only says “path guard”; this gives Sean a crisp outside-view risk frame.

2. **Add “confused deputy” as the older canonical model underneath prompt injection.**  
   Anchor it on Norm Hardy’s [“The Confused Deputy”](https://dl.acm.org/doi/10.1145/54289.871709).  
   Pattern to add: “The model is not ‘breaking out’; it is being tricked into spending the server’s authority on the attacker’s behalf.”  
   This unlocks a **Substack essay / interview answer** where Sean stops sounding like he is chasing the latest MCP checklist and instead frames agent security as a classic authority-design problem. It also sharpens his intent-engineering thesis: agents need delegated capabilities, not ambient permissions.

3. **Add “protocol-level MCP threat model” to contradict the server-only scope.**  
   Anchor it on the paper [“Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents”](https://arxiv.org/abs/2601.17549), especially its claims around capability attestation, origin authentication, and trust propagation. Pair it with the [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/).  
   Pattern to add: “Path confinement fixes one server-local exfiltration path; it does not prove the MCP deployment is secure unless host, client, server, tool metadata, and downstream transports have separate trust boundaries.”  
   This unlocks an **agent spec or hardening runbook** with sections for tool-description poisoning, sampling/origin boundaries, OAuth/session handling, and multi-server trust. The current concept can produce a patch; this produces a defensible security architecture artifact.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
