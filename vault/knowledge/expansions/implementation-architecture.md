---
title: "How to make `Implementation Architecture` better"
type: expansion
parent: "[[implementation-architecture]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-12
updated: 2026-08-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[implementation-architecture]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “information-hiding decomposition,” not a tool inventory

**WHAT to add:** Replace `list_files_in_vault` / `search` as the architectural center with a **change-axis decomposition**: MCP transport, authorization policy, vault storage, indexing/retrieval, and document projection become separate ports. Sentence pattern: “If **X changes**, only **Y boundary** should move.”

**WHO/WHAT:** David Parnas, [“On the Criteria to Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623) (1972). Parnas’s test is not whether functions look related, but whether volatile design decisions are hidden behind stable interfaces.

**WHAT this unlocks:** An architecture decision record and executable adapter-swap demo: run the same `VaultRepository` contract against Obsidian Markdown, SQLite, and an encrypted private layer without changing MCP tools. That would turn Sean’s MCP server from “another vault wrapper” into a portfolio-grade demonstration of hexagonal architecture. The present concept cannot explain where boundaries belong or what survives a storage, protocol, or retrieval change.

## 2. Add an object-capability authority model

**WHAT to add:** Treat every vault operation as an **issued capability**, not ambient access. Model capabilities such as `Read(root, glob)`, `Search(index, scope)`, `Append(path)`, and `RevealPrivateMetadata`, with attenuation, expiry, and audit provenance. The governing question becomes: “What is the smallest authority this caller must possess?”

**WHO/WHAT:** Mark S. Miller, [*Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control*](https://www.erights.org/talks/thesis/) (2006). Miller’s object-capability model addresses cooperation among components while limiting destructive interference.

**WHAT this unlocks:** A concrete agent-authority specification, threat model, and red-team demo in which a prompt-injected agent can search public concepts but cannot enumerate Sean’s private job-hunt or employer archives. It also gives the intent-engineering MCP server a serious bridge between “autonomy boundaries” and enforceable runtime authority. The current concept assumes access once connected; that is architecture’s most consequential omission.

## 3. Add a Cranfield-style retrieval test collection

**WHAT to add:** Define implementation architecture partly through **measured retrieval behavior**: a frozen set of real questions, relevance judgments, expected source notes, forbidden leakage, and metrics such as Recall@k, nDCG, citation coverage, and private-scope violations. Compare lexical, embedding, hybrid, and graph-expanded retrieval against the same collection.

**WHO/WHAT:** Ellen Voorhees, [“The Philosophy of Information Retrieval Evaluation”](https://www.nist.gov/publications/philosophy-information-retrieval-evaluation) (2002), explaining the Cranfield test-collection paradigm. Pair it with Pedro Rodriguez and Jordan Boyd-Graber’s [“Evaluation Paradigms in Question Answering”](https://aclanthology.org/2021.emnlp-main.758/) to expose the limitation of evaluating only document relevance rather than whether answers help users.

**WHAT this unlocks:** A reproducible benchmark repo, architecture trade-off memo, and portfolio one-pager showing why Sean selected a retrieval design with evidence. Right now “mcp-obsidian feels immediate” is product commentary; it cannot support an engineering decision or detect regressions in the nightly knowledge loop.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
