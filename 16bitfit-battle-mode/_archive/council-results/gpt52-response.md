Architect for **pluralism**: build a model-agnostic “render graph” with **two generation primitives** (still + clip) and treat *image-only*, *keyframe→video*, and future “native spritesheet/video→spritesheet” models as interchangeable strategies selected per animation via policy. Then invest most of your near-term testing time in the **hybrid keyframe→video path** (because it directly targets your proven failure mode: intra-cycle pose disambiguation), while continuing to harden the audit/validation layer because it is the compounding asset.

## 1) My stance on the 3 approaches (what to bet on)

### Recommendation (Feb 2026)
**Primary bet: Hybrid keyframe→video pipeline, with image-only as a deterministic fallback, and “wait-and-adapt” only for generation R&D (not for infrastructure).**

Reasoning:
- Your bottleneck is *temporal coherence + pose ordering* (left/right leg contact, passing, recoil). Image-only prompting is fundamentally fighting the model’s weak temporal prior; audits/retries can reject bad frames but can’t *create* the missing motion continuity cheaply.
- Video models are now explicitly exposing **keyframe conditioning / first+last frame transitions** (exactly what you need for walk loops), so you can turn the problem into: “make a few *correct* key poses, then interpolate.”  
  - Veo 3.1 supports generating a transition between a **first frame and a last frame** via `last_frame` / “first and last frames” workflows. [8][9]  
  - Pika “Pikaframes 2.2” supports **multi-keyframe interpolation (up to five images)**. [12]  
  - Kling has a widely-used **Start/End frame** workflow and even “perfect loop” patterns by setting start=end (tooling varies by integration, but the control paradigm is there). [15]
- “Wait-and-adapt” is correct for *not overfitting to any single vendor API*, but waiting on generation entirely gives you no production telemetry and no regression suite. The right version is: **finish model-agnostic infra now and keep generation adapters thin**, but still implement hybrid so you’re learning with real animations.

## 2) Architecture: design the generator adapter layer for rapid model churn

### A. Treat generation as a capability-driven plugin system (not model-driven)
Create adapters that declare **capabilities** and accept a normalized request schema. Don’t hardcode “Kling vs Veo”; hardcode “clip interpolation with N keyframes,” “image edit with refs,” etc.

**Core capabilities you should model explicitly:**
1. `still.generate` (text→image)
2. `still.edit` (image+prompt→image; supports multiple refs)
3. `clip.generate` (text→video)
4. `clip.animate_image` (image→video)
5. `clip.interpolate` (first+last)  
   - Veo 3.1: first frame + `last_frame` transition generation. [9][8]
6. `clip.keyframes` (2–5 keyframes)  
   - Pიკა Pikaframes: up to five images. [12]
7. `controls.refs.max_images` (how many reference images can be supplied)
   - Veo 3.1 supports **up to 3 reference images** for guiding generation. [9]
   - Gemini 3 Pro Image Preview supports **up to 14 reference images** for image generation/editing. [22]
8. `controls.seed` / determinism (if supported)
9. `output.alpha` (true alpha support vs matte + keying required)
10. `safety.person_generation` knobs (important if you’re generating humanoids; Veo docs include person safety settings). [8]

Your adapter interface should be “tell me what you can do” + “execute one atomic op”.

### B. Use a render graph (DAG) with typed artifacts, not a linear script
You’re already manifest-driven; make the manifest describe a **graph of nodes** that produce artifacts:

**Artifact types**
- `KeyframeImage` (RGBA PNG)
- `ClipVideo` (MP4/WebM)
- `ExtractedFrames` (ordered PNG sequence)
- `PixelSpecFrames` (post-processed to palette/outlines/baseline rules)
- `Atlas` (TexturePacker output)
- `ValidationReport` (Phaser headless + your quality gates)

**Node types**
- `GenerateKeyframes` (still model)
- `InterpolateMotion` (video model)
- `ExtractFrames` (ffmpeg)
- `RestyleToPixelSpec` (image edit model + deterministic post)
- `AuditFrames` (your gates + retry ladder)
- `PackAtlas` (TexturePacker)
- `ValidateInEngine` (Phaser headless)

This makes “wait-and-adapt” a non-event: swapping in a new model is swapping the node implementation, not changing the pipeline.

### C. Separate “policy” from “mechanism”
Add a `planner` that chooses strategy per animation:
- For `idle_breathe` / `hit_sparkle`: image-only may be fine.
- For `walk`, `run`, `crouch_walk`: hybrid interpolation is default.
- For `special_move` with smear frames: hybrid or even clip-first may win.

Policy inputs:
- animation archetype (`locomotion`, `attack`, `reaction`)
- required loopability
- allowed retries / cost budget
- “strictness” profile (boss sprites might tolerate fewer retries but more manual review)

## 3) How to invest testing time (Q1–Q2 2026) across the approaches

### Allocation I’d use (pragmatic, ROI-maximizing)
1) **45% Hybrid keyframe→video**  
   Goal: make walk cycles reliably with correct contact ordering and minimal jitter.
2) **35% Audit/export/validation hardening (model-agnostic)**  
   Goal: reduce total iteration cost across *all* models and future-proof the project.
3) **20% Image-only improvements**  
   Goal: keep a reliable baseline + cover cases where video models fail style/alpha requirements.

I would *not* spend meaningful time on “wait-and-adapt” beyond ensuring your adapter layer and evaluation harness can onboard new models quickly—because you already have enough emerging capabilities (first/last, multi-keyframe) to justify shipping hybrid now. [9][8][12]

## 4) Practical strategy per approach (what “done right” looks like)

### Approach 1 — Image-only per-frame + audit/retry (keep it, but narrow its scope)
**Use it for:**
- single poses, key poses, portraits, select VFX frames
- non-locomotion where ordering ambiguity is low

**To reduce left/right leg ambiguity without video:**
- Generate each frame from an explicit **pose reference image** you control (you’re already doing dual-reference). The trick is to stop relying on text (“left leg forward”) and instead rely on *visual pose refs that are unambiguous* (even if they’re crude stick-figures or 3D mannequins). Then audits enforce identity/palette/baseline.

**Why it stays as fallback:** it’s the most debuggable: one request → one frame → pass/fail.

### Approach 2 — Hybrid keyframe→video interpolation (make this your locomotion workhorse)
This is where current APIs are finally aligning with your needs:

**Two viable conditioning patterns you can support in your adapter layer:**
- **(A) First+Last interpolation** (cheap + stable for short loops)
  - Veo 3.1 supports first frame + `last_frame` transition generation. [9]
  - Vertex AI docs show “generate from first and last frames” as a first-class workflow. [8]
  - Kling Start/End frame workflows are widely used for controlled transitions; also supports “perfect loops” by setting start=end in some tooling contexts. [15]
- **(B) Multi-keyframe interpolation (2–5 keyframes)** (best for walk cycles)
  - Pika Pikaframes 2.2: upload **up to five images** and interpolate across them. [12]

**For a SF2-style walk (6–8 frames), do this:**
- Author/generate 3–5 keyframes in pixel style:
  - contact (L forward), passing, contact (R forward), (optional: recoil, anticipation)
- Interpolate to a clip that spans exactly one loop.
- Extract frames at the exact count you need (e.g., 8).
- Post-process frames back to pixel spec.

**Critical: plan for style drift**
Even if the video model keeps identity, it will often introduce:
- subpixel wobble
- anti-aliased edges inconsistent with your pixel outline rules
- palette creep
- inconsistent alpha edges

So treat video output as a *motion field provider*, not final art. Your pipeline should assume a restyle step.

### The “restyle back to pixel art spec” step (make it a first-class node)
You’re already auditing palette fidelity, outlines, baseline, alpha. For hybrid, add a dedicated node:

`RestyleToPixelSpec(frames, anchor_refs, palette_spec) -> pixel_frames`

Implementation options:
- **Image editing model pass** using strong references:
  - Gemini image generation/editing supports multiple reference images and is designed for “professional asset production” in the Pro tier; the docs explicitly note up to **14 reference images** for Gemini 3 Pro Image Preview. [22]
- Deterministic transforms:
  - palette quantization (fixed palette)
  - outline enforcement
  - baseline lock / registration
  - alpha matte cleanup

Then run your audit gates and retry ladder.

### Approach 3 — Wait-and-adapt (do it only as “adapter + eval readiness”)
The part you *should* “wait” on is committing to any single vendor’s proprietary feature set. But you should **not wait** on:
- manifest schema stabilization
- artifact lineage (hashing, caching, provenance)
- audit gates + headless validation
- benchmark harness

Because those are the multipliers that make future models immediately valuable.

## 5) The adapter layer: concrete shape (what I would implement)

### A. Normalized request objects
- `StillRequest`
  - prompt, negative_prompt
  - refs: `{type: anchor|pose|style, image_uri, weight}`
  - output: `{w,h,format:'png',alpha:true}`
  - seed, guidance, steps (optional)
- `ClipRequest`
  - prompt, negative_prompt
  - keyframes: `[ {t, image_uri} ... ]` (support 1, 2, or 2–5)
  - refs: style/character refs (if the model supports it; Veo supports up to 3 reference images). [9]
  - duration, fps, aspect_ratio
  - seed (optional)

### B. Capability discovery
Each adapter returns something like:
```json
{
  "name": "veo31",
  "caps": {
    "clip.interpolate": true,
    "clip.keyframes.max": 2,
    "clip.reference_images.max": 3
  }
}
```
Back it with what the platform states:
- Veo 3.1: transitions between first+last frame, plus reference images. [9]
- Pika Pikaframes: up to five keyframes. [12]

### C. A strategy planner that chooses:
- `image_only`
- `keyframes_to_video`
- `video_first` (future)
based on caps + animation type + cost budget.

## 6) What your next 4–8 weeks should look like (most leverage)

1. **Ship a minimal hybrid path end-to-end for one locomotion animation**
   - 3 keyframes → interpolate → extract 8 frames → restyle → audit → pack → Phaser validation.
2. **Create a regression suite**
   - fixed prompts + fixed refs
   - scorecards for identity consistency, palette delta, baseline drift, alpha artifacts, plus a “temporal jitter” metric (optical-flow smoothness or keypoint stability).
3. **Run an adapter bake-off weekly**
   - Veo (first+last) [8]
   - Pika Pikaframes (multi-keyframe) [12]
   - Kling start/end (where accessible) [15]
   Log cost, success rate, and how often restyle/audit salvage works.

## Bottom line
- **Don’t choose one approach.** Architect so all three are “strategies” over the same manifest DAG.
- **Invest most testing in hybrid now** because the ecosystem has converged on keyframe conditioning primitives (first+last; 2–5 keyframes) that directly solve your walk-cycle ambiguity. [8][9][12]
- **Keep image-only as the reliable fallback** and as the keyframe generator.
- **Treat video output as motion scaffolding** and make “restyle to pixel spec” an explicit stage, then let your audit/retry enforce the Street Fighter II constraints.

Sources: Veo 3.1 capabilities and reference images + first/last transitions [9]; Vertex AI “generate from first and last frames” Veo docs [8]; fal.ai blog describing Pika Model 2.2 / Pikaframes with up to five images [12]; Kling start/end frame workflow and looping pattern via start=end (integration guidance) [15]; Gemini image generation docs noting Gemini 3 Pro Image Preview and up to 14 reference images (useful for restyling/consistency) [22].