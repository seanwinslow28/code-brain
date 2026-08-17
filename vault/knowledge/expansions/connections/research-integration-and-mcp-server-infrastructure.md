---
title: "How to make `Research Integration and MCP Server Infrastructure` better"
type: expansion
parent: "[[research-integration-and-mcp-server-infrastructure]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-13
updated: 2026-08-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-integration-and-mcp-server-infrastructure]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “belief revision,” not merely contradiction retrieval

**What to add:** Model every claim as a belief with explicit justifications, assumptions, and dependency edges. A contradiction should trigger one of four outcomes: retract, supersede, scope, or preserve as an unresolved alternative.

**Anchor:** Jon Doyle’s 1979 paper [“A Truth Maintenance System”](https://www.sciencedirect.com/science/article/abs/pii/0004370279900080). Doyle’s key move is recording *why* a belief exists so the system can revise beliefs through dependency-directed backtracking.

**Sentence pattern:** “`find_contradictions` should return not two conflicting passages, but the assumptions supporting each passage and the smallest belief set that must change to restore consistency.”

**What this unlocks:** An executable **decision-revision demo**: change an architectural assumption—such as “the MBP is available overnight”—and show the MCP server identifying every decision invalidated downstream. That is a much stronger agentic-engineering artifact than semantic search branded as contradiction detection. It could become both an agent spec and a Substack essay: **“Your Second Brain Needs Retractions, Not More Connections.”**

## 2. Add provenance as a first-class schema

**What to add:** Represent each research-derived claim using `Entity → Activity → Agent` lineage, including source URL, retrieval timestamp, producing model, transformation step, confidence, and the human or agent that accepted it.

**Anchor:** The W3C’s [PROV-O recommendation](https://www.w3.org/TR/prov-o/), edited by Timothy Lebo, Satya Sahoo, and Deborah McGuinness. It supplies interoperable vocabulary such as `wasGeneratedBy`, `wasDerivedFrom`, and `wasAttributedTo`.

**Sentence pattern:** “A research finding is not integrated until its derivation path survives the transformation from source document to extracted claim to recommendation to implemented decision.”

**What this unlocks:** A **research-chain audit view** and portable MCP response contract. Sean could ship a one-page architecture diagram plus a live demo answering: “Which portfolio claim depends on this superseded research?” It also turns the existing anti-fabrication gate into a legible portfolio capability rather than hidden implementation hygiene.

## 3. Add an end-to-end argument against the article’s own infrastructure claim

**What to add:** Explicitly contradict the implication that reusing publication infrastructure constitutes research integration. MCP transport can expose a claim, but only the consuming workflow can verify that the claim changed a decision or artifact.

**Anchor:** Jerome Saltzer, David Reed, and David Clark’s [“End-to-End Arguments in System Design”](https://www.cs.cmu.edu/~15712/papers/saltzer84.pdf). Their principle says lower-layer mechanisms cannot fully guarantee properties that only the application endpoint can evaluate.

**Sentence pattern:** “DNS verification, signing, and registry publication prove delivery and identity; they cannot prove that research altered a decision, survived verification, or produced value.”

**What this unlocks:** An **integration acceptance-test runbook** with three endpoint assertions: provenance preserved, decision changed, downstream artifact regenerated. It also gives Sean a sharper portfolio narrative: **“MCP is the pipe, not the product”**—a useful counter-position to infrastructure-first agent demos.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
