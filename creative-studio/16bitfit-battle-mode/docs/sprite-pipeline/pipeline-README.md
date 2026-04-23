# Sprite-Sheet-Automation-Project_2026
Autonomous, manifest-driven sprite animation generation + QA + atlas export for **16BitFit Battle Mode** (Phaser-ready).

This repo is the “production pipeline” for turning **gold anchor sprites** into **full animation sets** (frame-by-frame) with **hard QA gates**, **reason-code retries**, and **deterministic exports** (PNG + JSON atlases) that load cleanly in Phaser (no jitter, no drift, no halo).

---

## Why this exists (problem + approach)

### The trap
“Generate a sprite sheet” is a trap. AI output can look good but still fail in-engine:
- **Identity drift** across frames (face, outfit, silhouette changes)
- **Baseline/pivot shifts** that create visible “ice skating” jitter
- **Alpha halos** / edge bleeding after packing
- Random, manual, non-reproducible workflows

### The solution (production workflow)
We treat sprite animation like production:
1) **Manifest-driven runs** (single source of truth)
2) **Frame-by-frame generation** (not monolithic sheets)
3) **Hard gates** (kill switches) + **soft scoring**
4) **Bounded retry ladder** driven by reason codes
5) Only **approved frames** are allowed to pack/export
6) **Phaser micro-tests** validate “engine truth”

---

## What we’re building (pipeline overview)

**Stage 0 — Manifest**
- Every run is defined by a manifest: character, move, frame count, naming policy, anchor path, pose specs, generator settings, audit thresholds, retry limits, pack/export settings.

**Stage 1 — Choreographer**
- Produces a precise **pose spec per frame** for a move (e.g., “Heavy Kick frame 03”).

**Stage 2 — Generator (Nano Banana Pro)**
- Primary backend: **Gemini CLI + Nano Banana extension** using:
  - model: `gemini-3-pro-image-preview` (Nano Banana Pro)
  - mode: **edit-from-anchor** (and often edit-from-prev-frame for temporal coherence)
- Generates **one frame at a time**.

**Stage 3 — Auditor**
- **Hard Fail (reject immediately)**: format, dims, alpha, background/halo, baseline stability, naming/metadata contract, gross anatomy/identity breaks.
- **Soft scoring**: identity similarity, palette match, line weight drift, temporal coherence, halo severity.

**Stage 4 — Retry Ladder**
- Bounded retries (max attempts per frame) with reason-code routing:
  - edit-pass refinement > re-anchor identity rescue > pose rescue > fallback backend (optional future)

**Stage 5 — Approve → Pack → Export**
- Only frames in `/approved/` get packed.
- Standard output: **atlas PNG + Phaser-friendly JSON** (TexturePacker JSON Hash preferred).

**Stage 6 — Phaser Validation Micro-tests (non-negotiable)**
- Validate pivot/baseline behavior, trim behavior, frame naming keys, texture bleeding, shimmer, and in-engine animation stability.

---

## Battle Mode Constraints (non-negotiable)

- Style: **full-color arcade fighter** (SF2/Capcom-inspired), NOT DMG palette.
- Output backgrounds: **transparent** (or controlled key color + deterministic background removal if alpha is unreliable).
- Champions: typically **128×128** tiles.
- Bosses: typically **256×256** tiles.
- Generation policy: **generate frames facing RIGHT** and flip in-engine for left-facing.
- Exports must be Phaser-safe (no jitter, no halos, consistent naming contract).

---

