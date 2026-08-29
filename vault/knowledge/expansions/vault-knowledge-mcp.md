---
title: "How to make `vault-knowledge-mcp` better"
type: expansion
parent: "[[vault-knowledge-mcp]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-13
updated: 2026-08-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[vault-knowledge-mcp]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “find contradictions” with a truth-maintenance model

**Add:** A justification graph in which every claim records its assumptions, evidence, temporal scope, and dependent claims. Contradiction handling becomes belief revision, not semantic similarity:

`claim → supported-by → source → valid-during → interval`

When evidence changes, the system identifies which conclusions must be reconsidered rather than merely returning two opposing passages.

**Anchor:** Jon Doyle’s paper [“A Truth Maintenance System”](https://www.sciencedirect.com/science/article/abs/pii/0004370279900080) (1979), which formalizes recording reasons for beliefs, revising assumptions, and dependency-directed backtracking.

**Unlocks:** An executable demo—“change one assumption and watch the vault revise itself”—plus an agent decision record explaining why a conclusion became unsupported. The current concept can retrieve disagreement; it cannot model consequences, distinguish supersession from genuine contradiction, or explain what should change.

## 2. Add a vault-native retrieval benchmark

**Add:** A fixed evaluation corpus modeled on BEIR: 50–100 human-labeled queries spanning exact lookup, paraphrase, cross-domain synthesis, temporal questions, known contradictions, and deliberately unanswerable requests. Compare BM25, embeddings, hybrid retrieval, and reranking using `nDCG@10`, `Recall@k`, MRR, latency, and abstention accuracy.

Include adversarial pairs such as:

- “What model runs synthesis?” versus “What model used to run synthesis?”
- “Find evidence against this claim” versus “Find articles containing the same vocabulary.”
- A question whose answer exists only in the private layer and therefore must return `withheld`, not `no results`.

**Anchor:** Nandan Thakur et al., [“BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models”](https://openreview.net/pdf?id=wCu6T5xFjeJ), which showed why retrieval systems must be tested across heterogeneous tasks rather than demonstrated with favorable examples.

**Unlocks:** A publishable benchmark report and portfolio one-pager: “What retrieval architecture works on a 370-node personal knowledge graph?” It also gives the MCP server an acceptance test. The present three-tool specification proves API construction, but not that `search_concepts` retrieves anything reliably.

## 3. Treat read access as a disclosure capability, not a safety guarantee

**Add:** Query-time policy projection based on complete mediation and least privilege. Build separate public and private indexes; attach visibility labels at ingestion; re-check authorization on every returned passage; strip filesystem paths and private backlinks; audit denied queries; test inference attacks that reconstruct hidden facts through counts, snippets, contradiction edges, or timing.

The governing sentence should be: **“Read-only prevents mutation; it does not prevent exfiltration.”**

**Anchor:** Jerome Saltzer and Michael Schroeder’s [“The Protection of Information in Computer Systems”](https://www.cs.virginia.edu/~evans/cs551/saltzer/), especially fail-safe defaults, complete mediation, and least privilege.

**Unlocks:** A disclosure threat model, red-team test suite, and dual-index public demo showing identical queries producing appropriately filtered results. This would connect the project to Sean’s real public/private vault boundary and make it a credible governance artifact. The current concept’s unrestricted `get_article(slug)` is safe only in the narrowest filesystem sense; packaged publicly, it lacks an information-security model.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
