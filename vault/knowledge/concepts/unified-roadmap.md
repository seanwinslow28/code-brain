---
title: "Unified Roadmap"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md
tags: [auto-generated, phase-6]
created: 2026-06-01
updated: 2026-06-01
---

## Definition

A bifurcated documentation architecture that separates strategic planning from operational execution by maintaining a lightweight parent file for open work and a heavy companion file for closed outcomes. This pattern prevents context window bloat during active sessions by offloading historical amendments and completed task bodies to a dedicated ship history log. The mechanism relies on a strict write discipline where new completions land in the companion file, leaving the parent focused solely on in-flight dependencies and strategic stubs.

## Context

Sean manages a complex job-hunt roadmap with numerous interdependent tasks. Without this separation, the parent file accumulates 13+ amendment entries and full task bodies, creating significant in-context bloat that degrades agent performance during active planning sessions. This structure ensures that when Sean or an agent opens the roadmap, they see only what needs to be done now, not the entire history of what was done.

## Evidence

> The parent roadmap stays focused on open + in-flight work; this file accumulates outcomes.

> Every entry below was previously inline at the top of the roadmap; cumulatively those 13 entries were the single largest in-context bloat source for sessions opening the roadmap.

> Whenever a task closes or a session-of-work ships an outcome, the writeup lands here instead of on top of the parent.

## Examples

- Moving the 2026-05-10 amendment regarding Task 8 and Task 9 from the parent's YAML frontmatter to this completion log.
- Replacing a closed task body in the parent with a 2–3 line status stub and a wikilink to this file.

## Related Concepts

[[Execution Strategy Decoupling]] [[Token Waste]]
