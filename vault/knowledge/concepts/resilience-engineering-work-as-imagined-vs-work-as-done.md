---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/concepts/resilience-engineering-work-as-imagined-vs-work-as-done.md
tags: [auto-generated, phase-6]
created: 2026-08-18
updated: 2026-08-18
---

## Definition

This framework scores system resilience by analyzing successful adaptations under degraded conditions rather than assuming healthy components guarantee success. It measures four specific potentials—respond, monitor, learn, anticipate—and records nights when the routine succeeded despite unavailable hardware or stale inputs. This approach treats resilience as a dynamic capability of the system to preserve outcomes during failure, not a static property of its health.

## Context

Sean’s current monitoring likely focuses on whether agents are running. By adopting this lens, he can identify which adaptations preserved his daily note integrity when the MBP was unavailable or an agent delayed, providing deeper insight into his system's actual robustness than uptime metrics alone.

## Evidence

> Reject the concept’s implied equation `healthy agents → reliable routine`. Score four resilience potentials instead: respond, monitor, learn, anticipate.

> Hollnagel treats resilience as something a system does, not a health property it possesses.

## Examples

- Recording nights when the routine succeeded despite an unavailable MBP, stale input, delayed agent, or partial manifest.
- Identifying which specific adaptation preserved the outcome when standard components failed.

## Related Concepts

[[Agent Health]] [[The Illusion of Competence in Automated Systems]]
