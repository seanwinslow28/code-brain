---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/hidden-environmental-dependencies-create-fragile-automation-anchors.md
tags: [auto-generated, phase-6]
created: 2026-09-16
updated: 2026-09-16
---

## Definition

Legibility debt accumulates when the operational requirements of a system diverge from its visible documentation or code structure, forcing supervisors to rely on tacit knowledge rather than explicit rules. This debt manifests as a supervision failure because the supervisor cannot verify the system's health through standard observability tools, only through manual inspection of hidden state files. The cost of this debt is that any change to the environment breaks the implicit contract between the tool and its user, requiring deep debugging skills to resolve.

## Context

Sean must manually inspect hidden config directories and browser cookie formats to understand why an agent failed. This prevents him from scaling his supervision because he cannot delegate fixes to other agents or junior engineers without first documenting these obscure environmental dependencies.

## Evidence

> The machine does not pick them — which sentence is the line is his judgment, and a machine guessing would fill the ledger with lines he never rat

> Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

## Examples

- The inability of an agent to guess the correct line in a ledger without human judgment.
- Different browsers throwing distinct errors for the same underlying data format issue.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Tacit Knowledge Erosion vs. Automation Scale]]
