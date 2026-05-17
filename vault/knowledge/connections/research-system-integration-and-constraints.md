---
title: "Research System Integration and Constraints"
type: connection
connects:
  - Deep Research Queue
  - Local Deep Research (LDR)
  - System Constraints
created: 2026-05-16
updated: 2026-05-16
---

## Synthesis

The Deep Research Queue, LDR, and Gemini DR are interdependent systems that rely on routing rules to manage research workloads effectively.

## Threads

### [[Deep Research Queue]]

> Routing rule (v3.26.3, 2026-05-06): This queue is for **single-shape topics only** — one target, one question, one pattern.

### [[Local Deep Research (LDR)]]

> LDR is pinned to v1.5.6 awaiting upstream PR #4000.

### [[System Constraints]]

> Both topics were re-run on Gemini DR successfully.

## Implications

- Future work should explore ways to streamline the integration between LDR and Gemini DR while maintaining strict constraints.
