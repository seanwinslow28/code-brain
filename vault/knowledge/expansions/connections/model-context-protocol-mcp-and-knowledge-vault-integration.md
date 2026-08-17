---
title: "How to make `Model Context Protocol (MCP) and Knowledge Vault Integration` better"
type: expansion
parent: "[[model-context-protocol-mcp-and-knowledge-vault-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-12
updated: 2026-08-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[model-context-protocol-mcp-and-knowledge-vault-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “claim packets,” not note retrieval.**

   - **What:** Make the MCP’s atomic object an assertion with three separately addressable layers: `claim`, `provenance`, and `publication metadata`. Sentence pattern: **“Claim X is supported by source Y, extracted by process Z, at confidence C, and contradicted by claim Q.”**
   - **Exemplar:** Paul Groth, Andrew Gibson, and Jan Velterop, [“The Anatomy of a Nanopublication”](https://journals.sagepub.com/doi/pdf/10.3233/ISU-2010-0613). Their nanopublication model separates a machine-readable assertion from its evidence and provenance.
   - **Unlock:** An executable **evidence-ledger demo**: MCP tools such as `get_claim_evidence`, `list_counterclaims`, and `trace_derivation`. This would also support a Substack essay—*Your Second Brain Needs Receipts, Not Better Search*—and give `intent-engineering` a concrete epistemic contract. The current concept can expose notes, but cannot tell an agent which sentences deserve belief.

2. **Add “capability-secure vault access” anchored on the confused-deputy problem.**

   - **What:** Replace “seamless integration” with **least-authority delegation**. Every request should carry an explicit capability bounded by corpus, operation, purpose, expiry, and write authority. Pattern: **“This caller may retrieve cited claims from project P for task T; it may not enumerate private notes, infer unrelated personal facts, or persist writes.”**
   - **Exemplar:** Norm Hardy, [“The Confused Deputy (or Why Capabilities Might Have Been Invented)”](https://www.scs.stanford.edu/nyu/04fa/sched/readings/confused.pdf). Hardy shows how a trusted intermediary can misuse its own ambient authority while innocently serving an untrusted caller—the exact risk created when an MCP server sits between agents and a personal vault.
   - **Unlock:** A portfolio-grade **red-team demo and authority matrix**: malicious retrieved text attempts cross-project exfiltration; scoped capabilities deny it and emit an audit record. It would turn the I-5 autonomy-boundary idea into enforceable infrastructure. The current article’s protocol-adherence framing cannot decide who may learn what, under whose authority, or for how long.

3. **Add “berrypicking sessions” instead of treating retrieval as one-shot query answering.**

   - **What:** Model knowledge work as an evolving trail: each discovered source changes the question. Add session primitives such as `start_inquiry`, `follow_citation`, `pivot_vocabulary`, `save_trail`, and `explain_query_shift`. Pattern: **“I began with Q1; evidence E changed the vocabulary to V and produced Q2.”**
   - **Exemplar:** Marcia J. Bates, [“The Design of Browsing and Berrypicking Techniques for the Online Search Interface”](https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html). Bates contradicts the conventional assumption that users formulate one stable query and merely collect matching results.
   - **Unlock:** A **stateful research-agent spec**, an inquiry-trail visualization, and an evaluation comparing one-shot RAG with evolving-query exploration on job-company diligence or concept discovery. The current concept reaches “query my vault”; this reaches “show how my understanding changed”—a much stronger agentic-engineering artifact.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
