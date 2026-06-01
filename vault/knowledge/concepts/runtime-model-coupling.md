---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-31-task-12-day-6-handoff.md
tags: [auto-generated, phase-6]
created: 2026-06-01
updated: 2026-06-01
---

## Definition

Runtime-Model Coupling occurs when the structural schema of a data object must be expanded to expose internal state that was previously hidden from downstream consumers. In this case, the `ActionProposal` schema required a new `content_preview` field because the policy rules needed to inspect the actual draft text, not just metadata. Without this coupling, the judge layer operates on incomplete information, causing it to default to permissive outcomes like `ALLOW` because it cannot verify the content against the rules. This creates a dependency where the agent's output format must evolve in lockstep with the policy engine's inspection requirements.

## Context

This matters to Sean because his job-hunt automation relies on a judge layer to ensure quality and compliance. If the judge cannot see the draft content, the entire safety mechanism is bypassed, leading to unvetted Substack posts. The fix required modifying the data contract between the drafter and the judge, highlighting how tightly coupled the agent's output structure is to the validation logic.

## Evidence

> the eight original fields are all metadata, none carried the draft text the policy rules actually read

> Without it the judge sees only metadata and always falls through to ALLOW

> The Day-3 unit tests hid this by mocking the model response

## Examples

- Added `content_preview: Optional[str] = None` to `ActionProposal` in `lib/judge/schema.py`
- Renders `content_preview` in a fenced block in `_build_user_prompt` so the local model knows which text to review

## Related Concepts

[[Substack-Drafter agent]] [[Agent Health Monitoring]]
