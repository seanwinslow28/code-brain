---
title: "Authorization Precision Reduces Slop and Restores Trust"
type: connection
connects:
  - Velocity vs. Judgment in MCP Strengthening
  - Slop as a Trust Deficit
  - Implementation Architecture
created: 2026-08-13
updated: 2026-08-13
---

## Synthesis

Sean's transition from high-rejection, low-precision runs (qwen3-14b) to lower-rejection, higher-precision runs (qwen3.6-35b) demonstrates that tightening authorization boundaries directly reduces 'slop' in the system. By treating vault operations as issued capabilities rather than ambient access, the agent fleet avoids the trust deficit caused by ambiguous authority. This shift allows Sean to scale his fleet's velocity without sacrificing the semantic value of his outputs, proving that architectural rigor is a prerequisite for reliable automation.

## Threads

### [[Velocity vs. Judgment in MCP Strengthening]]

> The present concept cannot explain where boundaries belong or what survives a storage, protocol, or retrieval change.

### [[Slop as a Trust Deficit]]

> Treat every vault operation as an issued capability, not ambient access. Model capabilities such as Read(root, glob), Search(index, scope), Append(path), and RevealPrivateMetadata, with attenuation, expiry, and audit provenance.

### [[Implementation Architecture]]

> Replace list_files_in_vault / search as the architectural center with a change-axis decomposition: MCP transport, authorization policy, vault storage, indexing/retrieval, and document projection become separate ports.

## Implications

- Sean should prioritize object-capability models in his next MCP server iteration to explicitly limit agent authority and reduce trust deficits.
- The drop in rejected_count from 78 to 11 between June and August indicates that better authorization boundaries, not just larger models, are driving efficiency.
