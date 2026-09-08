---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/fragile-anchors-and-the-cost-of-hidden-dependencies.md
tags: [auto-generated, phase-6]
created: 2026-09-08
updated: 2026-09-08
---

## Definition

Legibility debt emerges when system reliability depends on opaque, environment-specific workarounds that are invisible to standard monitoring. This debt accumulates because the failure modes are tied to external state rotations or permission boundaries rather than internal logic errors. Consequently, supervision fails not because the agent is incompetent, but because the necessary context for its operation is hidden behind fragile manual anchors. The system appears functional until a boundary condition changes, at which point the lack of explicit dependency management causes immediate and unexplained failure.

## Context

Sean's fleet relies on browser-specific quirks and local file states to maintain authentication and session continuity. When these anchors break, the cost is not just downtime but the loss of trust in the automated system's ability to handle complex, stateful interactions without human intervention.

## Evidence

> When that session rotates there is no fallback: Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

> x/stimulus.py sweep works live today only because ~/.config/last30days/.env holds AUTH_TOKEN/CT0 written by the last30days setup wizard on 2026-06-08

## Examples

- Safari's EPERM error due to missing Full Disk Access permissions
- Chrome's JavaScript number overflow on WebKit cookie timestamps
- Firefox lacking a defined profile directory for session storage

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Operational Uptime vs. Semantic Value in Agent Fleets]]
