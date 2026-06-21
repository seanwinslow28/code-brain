---
title: "Context Compounding"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-and-knowledge-retrieval-interdependence.md
tags: [auto-generated, phase-6]
created: 2026-06-21
updated: 2026-06-21
---

## Definition

A behavioral pattern where agents function as information foragers rather than simple index queryers, following scent to decide whether to exploit a patch, abandon it, or widen their search. This mechanism requires tracking the decision trace over search patches, specifically noting why a source was initially promising and what signals caused the scent to weaken. It shifts the focus from top-k chunk retrieval efficiency to the agent's ability to navigate the information landscape effectively.

## Context

Sean's agents often retrieve knowledge but fail to synthesize it because they lack the behavioral frame for when to stop searching. By treating retrieval as foraging, Sean can optimize his agents to recognize when they have exhausted a 'patch' of useful information and need to pivot, preventing token waste on diminishing returns.

## Evidence

> Agents are not merely querying an index; they are following scent, deciding whether to exploit a patch, abandon it, or widen search.

> Retrieval is no longer “top-k chunks went in”; it becomes a decision trace over search patches.

## Examples

- An agent abandoning a source because the 'scent' of relevance weakened after reading three paragraphs.
- An agent widening its search when the initial patch failed to provide sufficient evidence for a claim.

## Related Concepts

[[Token Waste]] [[Indexing and Synthesis]]
