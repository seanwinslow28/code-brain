---
title: "Authorization Precision as the Lever for Semantic Integrity"
type: connection
connects:
  - Slop as a Trust Deficit
  - Velocity vs. Judgment in MCP Strengthening
  - Implementation Architecture
created: 2026-08-20
updated: 2026-08-20
---

## Synthesis

The core tension lies in the relationship between authorization precision and the semantic value of agent outputs. When agents operate with ambiguous authority, they generate 'slop' that erodes trust and increases rejection rates, effectively creating a bottleneck for velocity. By tightening authorization boundaries through object-capability models, Sean can reduce this slop, allowing his fleet to scale in speed without sacrificing the quality of his knowledge base.

## Threads

### [[Slop as a Trust Deficit]]

> When agents operate with ambiguous authority, they generate 'slop' that erodes trust and increases rejection rates, effectively creating a bottleneck for velocity.

### [[Velocity vs. Judgment in MCP Strengthening]]

> The present concept cannot explain where boundaries belong or what survives a storage, protocol, or retrieval change.

### [[Implementation Architecture]]

> Replace list_files_in_vault / search as the architectural center with a change-axis decomposition: MCP transport, authorization policy, vault storage, indexing/retrieval, and document projection become separate ports.

## Implications

- Sean should prioritize object-capability models in his next MCP server iteration to explicitly limit agent authority and reduce trust deficits.
- The drop in rejected_count from 78 to 11 between June and August indicates that better authorization boundaries, not just larger models, are driving efficiency.
