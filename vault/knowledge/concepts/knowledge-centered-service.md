---
title: "Knowledge-Centered Service"
type: concept
sources:
  - knowledge/expansions/confluence-overhaul-plan.md
tags: [auto-generated, phase-6]
created: 2026-06-03
updated: 2026-06-03
---

## Definition

Knowledge-Centered Service (KCS) inverts the traditional documentation lifecycle by treating knowledge creation as a byproduct of operational work rather than a separate maintenance task. This mechanism requires that documentation artifacts be generated, updated, and validated within the flow of support, engineering, or incident workflows. The system relies on demand loops where repeated questions or unresolved tickets trigger immediate doc updates, ensuring that the knowledge base reflects current reality rather than historical intent. This approach eliminates the gap between documented procedure and actual practice by tying content quality directly to operational efficiency.

## Context

Sean is positioning himself as an AI Product Manager who understands that documentation quality is an operational metric, not a virtue. By adopting KCS, he can argue that AI knowledge systems fail when they summarize documents without modeling who needs the document to mean what, shifting his narrative from 'PM improves Confluence' to 'AI knowledge systems require operational grounding.' This allows him to propose concrete agent specs that watch for stale links and unresolved tickets, demonstrating a sophisticated understanding of knowledge rot.

## Evidence

> Docs are created and improved in the flow of work, especially support, PM, engineering, and incident workflows.

> Documentation quality is an operational byproduct, not a documentation-team virtue.

> Don’t assign documentation as a cleanup project; wire it into demand loops.

## Examples

- An agent spec for a Confluence-maintenance agent that watches repeated questions, stale links, unresolved tickets, Slack/meeting residue, and support escalations, then proposes doc updates with provenance.
- A portfolio one-pager where Sean shows how he diagnoses knowledge rot by artifact class, including orphaned docs, duplicate truth, ambiguous ownership, stale onboarding, and decision amnesia.

## Related Concepts

[[Confluence Overhaul Plan]] [[Knowledge-Lint]] [[Agent Ops / FDP Backup Track]]
