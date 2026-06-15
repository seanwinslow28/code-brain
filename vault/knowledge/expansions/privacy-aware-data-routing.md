---
title: "How to make `Privacy-Aware Data Routing` better"
type: expansion
parent: "[[privacy-aware-data-routing]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-12
updated: 2026-06-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[privacy-aware-data-routing]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Information-Flow Control” as the hard technical pattern.**  
   Anchor it on Andrew C. Myers, *JFlow: Practical Mostly-Static Information Flow Control* and Dorothy Denning, “A Lattice Model of Secure Information Flow.” Right now the concept says “route private stuff elsewhere,” but it lacks the canonical security model: label data, define allowed flows, reject illegal joins.

   Sentence pattern to add: “Every synthesized artifact carries a sensitivity label; routing is permitted only when `source_label <= destination_label` under a small lattice: public < portfolio-safe < private < restricted.”

   This unlocks an **agent spec / executable policy gate**: Sean could ship `privacy_router.py` or an MCP tool that classifies source paths, propagates labels through synthesis, and blocks public writes when private provenance is present. The current note only produces a reminder; IFC turns it into enforceable architecture.

2. **Add “Provenance Tainting” from data lineage, not just path exclusion.**  
   Anchor it on Peter Buneman, Sanjeev Khanna, and Wang-Chiew Tan, “Why and Where: A Characterization of Data Provenance.” The missing facet is that privacy risk does not live only in the current file path. A public-looking concept can be derived from private job-hunt notes, calendar traces, operating-model artifacts, or ticket fragments.

   Sentence pattern to add: “Privacy follows derivation, not location: every generated concept stores `why_provenance` and `where_provenance`; if any ancestor is private, the descendant cannot be promoted without review.”

   This unlocks a **vault lineage manifest / audit runbook**: Sean could produce a `concept_provenance.jsonl` schema and a prune report that explains why each public concept is safe or unsafe. The present concept cannot answer the recruiter-risk question: “How do I know this public artifact was not derived from private career strategy?”

3. **Add “Contextual Integrity” as the contradicting privacy framework.**  
   Anchor it on Helen Nissenbaum, *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. This challenges the current framing, which treats privacy as public/private folder segregation. Nissenbaum’s sharper point is that privacy violations happen when information moves outside its expected social context, even if the data is not secret.

   Sentence pattern to add: “A datum is not classified only by sensitivity; it is classified by the context in which Sean would reasonably allow it to travel: recruiter-facing, portfolio-facing, friend-facing, agent-internal, or private self-management.”

   This unlocks a **Substack essay / portfolio governance page**: “My Agent Fleet Has Social Boundaries, Not Just Secret Folders.” That gives Sean a more mature public story than “I added exclusions.” It frames Code-Brain as agentic infrastructure with audience-aware norms, which is much closer to AI-PM / agentic-engineering signal.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
