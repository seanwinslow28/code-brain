---
type: project
domain: [creative-studio]
status: active
context: animation-pipeline
energy-level: high
ai-context: "Active 2D animation pipeline work. Current focus: Pencil Test portfolio short (`sw-portfolio-animation-pipeline`) targeting completion before June 11. Pipeline is Nano Banana 2 keyframes + Seedance 2.0 motion + Gemini redraws. Planned: extract reusable pipeline into its own project to serve multiple 2D animations."
review-date: 2026-04-21
created: 2026-02-20
last-updated: 2026-04-21
---
# prj-animation-pipeline

## Overview
**Goal:** Build an AI-assisted 2D animation production pipeline from keyframe generation through finished shorts. Current target: Pencil Test portfolio short before June 11 travel.
**Why it matters:** The long-term north star of creative-studio — human-AI collaboration producing animated shorts, YouTube content, shows, and potentially feature films.
**Definition of Done (current project):** Pencil Test loop plays smoothly at 12fps, character is recognizably Sean on cream paper, shippable without caveats.
**Aesthetic target:** looks like a 2D animation studio made it — early Disney / 90s Nickelodeon / Cartoon Network, or modern Wacom/iPad hand-drawn.

## Canonical Sources
| Resource | Location | Role |
|---|---|---|
| Pencil Test project manual | `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/CLAUDE.md` | Project-scoped source of truth (outside this repo) |
| Changelog | `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/CHANGELOG.md` | Decision history |
| Production Checklist | `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/docs/production-checklist.md` | Check first every session |
| Manifest | `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/manifest.yaml` | Pipeline config |
| Load-bearing workflow reference | [[ref-ai-animation-nb2-seedance-workflow]] | The Nano Banana 2 + Seedance workflow note |
| Pipeline skills | `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/.claude/skills/` | `gemini-pencil-animation-image-gen`, `image-generator-prompt-science`, `2d-animation-principles`, `animation-pipeline`, `creative-director`, etc. |

## Current Status
<!-- status-update -->

## Latest Commits
<!-- git-commits -->

## Key Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-21 | Vault note repositioned as active-project pointer | Option A from operating-model interview — keep canonical files outside the vault, link from here to avoid drift |

## Blockers
- None active. Exploration phase on the post-moodboard concept step for Act 2.

## Open Questions
- When to extract the reusable pipeline out of `sw-portfolio-animation-pipeline` into its own project (so it serves multiple 2D animations, not just this style)?
- How to apply autoresearch to the pipeline beyond ComfyUI workflow optimization?

## Links
- **Repo (external to this vault's project):** `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`
- **Operating model:** [[operating-model|Creative Studio Operating Model]]
- **Related notes:** [[moc-creative-studio]], [[ref-ai-animation-nb2-seedance-workflow]]
