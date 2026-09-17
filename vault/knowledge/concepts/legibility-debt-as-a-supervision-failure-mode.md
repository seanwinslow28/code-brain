---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-09-17
updated: 2026-09-17
---

## Definition

Legibility debt is the accumulation of operational divergence between a system's actual environmental dependencies and its visible documentation, forcing supervisors to rely on tacit knowledge rather than explicit rules. This debt manifests as a supervision failure because standard observability tools cannot verify system health, requiring manual inspection of hidden state files or browser-specific quirks. The cost of this debt is that any change to the environment breaks the implicit contract between the tool and its user, necessitating deep debugging skills to resolve rather than simple configuration updates.

## Context

Sean must manually inspect hidden config directories and browser cookie formats to understand why an agent failed, preventing him from scaling his supervision. He cannot delegate fixes to other agents or junior engineers without first documenting these obscure environmental dependencies, creating a bottleneck where only he can maintain the system's operational integrity.

## Evidence

> Legibility debt accumulates when the operational requirements of a system diverge from its visible documentation or code structure, forcing supervisors to rely on tacit knowledge rather than explicit rules.

> Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp.

## Examples

- The inability of an agent to guess the correct line in a ledger without human judgment.
- Different browsers throwing distinct errors for the same underlying data format issue.

## Related Concepts

[[Tacit Knowledge Erosion vs. Automation Scale]] [[The Illusion of Competence in Automated Systems]]
