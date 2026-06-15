---
title: "How to make `MCP Server and Knowledge Graph Synergy` better"
type: expansion
parent: "[[mcp-server-and-knowledge-graph-synergy]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-15
updated: 2026-06-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[mcp-server-and-knowledge-graph-synergy]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “competency-question mode” before tool design.**  
   Anchor it on Michael Grüninger & Mark S. Fox, “Methodology for the Design and Evaluation of Ontologies” (1995), which treats an ontology as validated by the questions it can answer, not by the elegance of its graph. Sean’s current concept says “make the vault queryable,” but not *which decisions the graph must support*. Add a section like: “This MCP server is done only when it can answer: What concepts contradict this? What edge is stale? What missing source would change this conclusion?”  
   **Unlocks:** an executable MCP acceptance spec, not another architecture note. This becomes a portfolio artifact: “10 competency questions for an agentic personal knowledge graph.”

2. **Add “provenance-as-first-class-edge” using nanopublications / PROV-O.**  
   Anchor it on Tobias Kuhn et al., “Nanopublications: A Growing Resource of Provenance-Centric Scientific Linked Data” (2018), plus W3C PROV-O by Luc Moreau and Paul Groth. The missing facet is that `supports/contradicts/depends_on` edges are not enough unless each edge carries assertion, provenance, and publication metadata: who/what created it, from which quote or run, under which model, with what confidence, and whether it survived later critique.  
   **Unlocks:** a trustable “agent memory audit trail.” Sean could ship an agent spec or demo where Claude asks the MCP server, “Show me only contradictions supported by primary-source quotes and created by non-local models.” Current concept cannot distinguish useful graph intelligence from confident graph sediment.

3. **Add “global sensemaking vs local lookup” as a separate retrieval contract.**  
   Anchor it on Darren Edge et al., “From Local to Global: A Graph RAG Approach to Query-Focused Summarization” (Microsoft Research, 2024). The current article frames MCP as exposing live graph queries, but it misses the split between local retrieval questions and global corpus questions. “What does `concept_edges` say about X?” is local. “What is my vault systematically over-believing?” is global. Those need community summaries, cluster-level critique, and diversity scoring, not just node lookup.  
   **Unlocks:** a stronger Substack essay or portfolio one-pager: “My vault is not search; it is a nightly adversarial sensemaking system.” It also gives Sean a concrete product decision: build two MCP tool families, `lookup_*` and `synthesize_global_*`, with different evals and failure modes.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
