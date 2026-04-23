---
type: project
domain: [creative-studio]
status: paused
context: 16bitfit
energy-level: low
ai-context: "PAUSED as of 2026-04-20. Original motivation (portfolio piece for PM roles) no longer urgent — Sean is at The Block. Will resume after the 2D animation pipeline is locked down, with a planned simplification pass (was overcomplicated). The sprite-sheet blocker is now solved in principle via the Nano Banana 2 + Seedance workflow; implementation deferred until the animation pipeline work completes."
review-date: 2026-04-21
created: 2026-02-20
last-updated: 2026-04-21
---
# prj-16bitfit

## Overview
**Goal:** A Game Boy-style fitness RPG that gamifies workout routines.
**Why it matters (originally):** Portfolio piece for PM roles + personal use. The PM-role driver is no longer active — Sean is at The Block.
**Why it still matters:** Personal interest remains; will resume with a simpler scope after the 2D animation pipeline is dialed in.
**Definition of Done:** Playable demo with 3 workout types, consistent sprite sheets, basic progression. Simplification scope TBD on resume.

## Canonical Sources
| Resource | Location | Role |
|---|---|---|
| Project source of truth | `creative-studio/16bitfit-battle-mode/SOURCE-OF-TRUTH.md` (repo root) | **Stale** — predates the pause and the simplification pivot. Review before use. |
| Battle-mode project CLAUDE.md | `creative-studio/16bitfit-battle-mode/CLAUDE.md` | Project manual |
| Mac Mini copy (via Google Drive) | `/Users/seanwinslow/Library/CloudStorage/GoogleDrive-sean.winslow28@gmail.com/Other computers/My Mac Mini/Code-Brain/16BitFit-V3/CLAUDE.md` | Drive-synced mirror |

## Current Status
<!-- status-update -->

**Paused.** Active work is on the 2D animation pipeline ([[prj-animation-pipeline]]). Resume plan: after the Pencil Test portfolio short ships (target before 2026-06-11), apply the validated Nano Banana 2 + Seedance sprite workflow and drop the old LoRA/SDXL approaches entirely. Also planning a scope simplification.

## Latest Commits
<!-- git-commits -->

## Key Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-20 | Project paused | PM-role driver no longer active; sprite blocker now solvable via new image/video gen workflows — resume after animation pipeline is locked down |
| 2026-04-21 | Vault note repositioned as project pointer | Option A from operating-model interview — keep canonical files outside the vault, link from here to avoid drift |

## Blockers
- _Historical_: sprite sheet consistency across generated assets (now solvable in principle via Nano Banana 2 + Seedance workflow).
- _Historical_: stable anchor image pipeline for character variants (same).
- _Current_: none — paused by choice.

## Open Questions
- When does resume start? Earliest candidate: after Pencil Test portfolio short ships.
- What's the simplification scope? The original battle mode was overcomplicated — trim it down to what actually ships.

## Links
- **Repo path (inside this repo):** `creative-studio/16bitfit-battle-mode/`
- **Operating model:** [[operating-model|Creative Studio Operating Model]]
- **Active sibling project:** [[prj-animation-pipeline]]
- **Related notes:** [[moc-creative-studio]]
