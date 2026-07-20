---
title: "The Taste-Throughput Trade-off in Agentic Synthesis"
type: concept
sources:
  - knowledge/connections/the-taste-throughput-trade-off-in-agentic-synthesis.md
tags: [auto-generated, phase-6]
created: 2026-07-20
updated: 2026-07-20
---

## Definition

This invariant describes the inverse relationship between the volume of generated artifacts and their semantic fidelity, driven by the computational cost of high-fidelity evaluation. As Sean shifts from qwen3-14b to qwen3.6-35b-a3b-32k, the system's ability to reject low-value outputs improves, but the total number of concepts written decreases significantly. This trade-off forces a decision: prioritize the illusion of competence through high activity proof, or accept lower throughput for higher conceptual value. The mechanism relies on the fact that rigorous taste-based filtering requires more computational resources and time than simple generation, creating a bottleneck where quality scales inversely with speed.

## Context

Sean is currently optimizing his vault synthesizer runs, balancing the need for a robust knowledge base against the diminishing returns of high-volume, low-quality synthesis. Understanding this trade-off is critical for deciding when to scale up cluster sampling versus when to deepen individual concept evaluation.

## Evidence

> Sean's recent operational data reveals a critical tension between the desire for high-volume concept generation and the necessity of rigorous taste-based filtering.

> As he shifts from using qwen3-14b to qwen3.6-35b-a3b-32k, the system's ability to reject low-value outputs improves, but the total number of concepts written decreases significantly.

## Examples

- Run 2026-07-06 used qwen3.6-35b-a3b-32k and wrote 103 concepts with 47 connections.
- Run 2026-07-15 used qwen3.6-35b-a3b-32k and wrote 89 concepts with 19 connections.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Taste as Evaluation Function vs. Activity Proof]]
