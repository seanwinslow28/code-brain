---
title: "How to make `MCP Security Framework` better"
type: expansion
parent: "[[mcp-security-framework]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-12
updated: 2026-08-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[mcp-security-framework]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “filter hostile text” with control/data-flow separation

- **What to add:** A rule that tool output is *data*, never executable instruction. Track provenance and capabilities through every value; privileged calls must remain derivable from the authenticated user request—not retrieved content.
- **Exemplar:** Edoardo Debenedetti et al., [“Defeating Prompt Injections by Design”](https://arxiv.org/abs/2503.18813), and its [CaMeL reference implementation](https://github.com/google-research/camel-prompt-injection). CaMeL separates trusted control flow from untrusted data flow and applies capability policies at exfiltration points.
- **What this unlocks:** An executable **prompt-injection red-team demo** for `intent-engineering-mcp`: malicious issue text enters through one tool, attempts to steer another, and is blocked by provenance—not a regex. It also gives Sean a strong Substack thesis: *“Sanitization is antivirus for language; authorization belongs in the execution architecture.”*

## 2. Turn “autonomy boundaries” into object-capability grants

- **What to add:** Extend Action Schemas into explicit authority tuples: `principal × action × resource × purpose × expiry`. A tool should receive only the narrow capability required for the current action, rather than ambient credentials or a reusable bearer token.
- **Exemplar:** Norm Hardy’s [“The Confused Deputy”](https://people.eecs.berkeley.edu/~daw/teaching/cs261-f02/readings.html), applied directly by the MCP specification’s requirements for audience-bound tokens, per-client consent, and prohibition of token passthrough. The [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) explicitly identifies confused-deputy failure modes.
- **What this unlocks:** A publishable **authorization decision table and conformance suite**: “Can this client invoke this tool on this resource for this declared intent?” It upgrades Intent Engineering from prompt-layer governance into enforceable least authority—and provides a portfolio demo where identical tool calls succeed or fail based on delegated purpose and blast radius.

## 3. Add supply-chain identity and tool-definition immutability

- **What to add:** Treat the npm package, tool manifest, and runtime tool descriptions as one signed release unit. Pin the approved descriptor hash; require provenance for updates; disable newly added capabilities until separately approved. This closes the gap between “safe when reviewed” and “safe after an update.”
- **Exemplar:** Santiago Torres-Arias et al., [“in-toto: Providing Farm-to-Table Guarantees for Bits and Bytes”](https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias), plus Hao Song et al., [“Beyond the Protocol”](https://arxiv.org/abs/2506.02040), which distinguishes MCP tool poisoning, puppet attacks, rug pulls, and malicious-resource exploitation.
- **What this unlocks:** A concrete **secure npm release runbook** and CI artifact: provenance attestation, signed manifest, descriptor-diff gate, capability-escalation warning, and rollback procedure. The present concept protects request handling; this addition protects what code and tool contract users are actually running.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
