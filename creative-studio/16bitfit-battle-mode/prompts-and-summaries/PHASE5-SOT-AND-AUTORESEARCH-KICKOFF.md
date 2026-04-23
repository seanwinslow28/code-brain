# Cowork Kickoff: SOURCE-OF-TRUTH Update + Autoresearch Plan Revision

**Date:** 2026-04-11
**Thread Purpose:** Two tasks — (1) update SOURCE-OF-TRUTH.md with Phase 5 completion data, then (2) collaboratively revise AUTORESEARCH-PLAN.md with Sean through Q&A.
**Estimated Duration:** 1 session

---

## Context

You are continuing work on **16BitFit Battle Mode** — a 2D fighting game sprite generation pipeline. This is a Cowork planning session (not Claude Code execution). Sean is a beginner coder, so explain technical choices clearly but briefly.

The project just completed **Phase 5**, which achieved a major milestone:
- 12/12 characters generated (6 Champions at 128×128, 6 Bosses at 256×256)
- 180/180 animations across 15 animation types (10 IMAGE_ONLY + 5 HYBRID)
- 1,020 IMAGE_ONLY frames + 815 RIFE-interpolated HYBRID frames
- 0 failures, ~$12.60 total Gemini API cost
- Pixel Quantizer verified on 7 characters (100% pass rate, 0 off-palette pixels)

**Key technical breakthroughs in Phase 5:**
- **Sprite sheet → split approach**: Instead of calling Gemini once per frame (which produced inconsistent characters), we generate ALL frames for an animation as a single sprite sheet in one API call, then split programmatically. This is 5x faster, 6x cheaper, and solves character consistency.
- **Anchor image conditioning (Golden Rule)**: Every Gemini NB2 call MUST include 3 character reference PNGs as inline image data. Enforced with RuntimeError — zero violations across 180 animations.
- **RIFE VFI connectivity fix**: Corporate VPN (utun4) was blocking LAN access to the Alienware (192.168.68.201). Fix: VPN disabled + httpx retries + pre-flight health check + Windows Firewall rule for port 8188.
- **Palette expansion**: Sean's palette expanded from 16 to 27 colors via k-means extraction. Generic sf2_pixel_art palette (38 colors) created from all 12 characters' anchor images.
- **Outline weight 1**: Default weight 2 was too aggressive at 128×128 (77% of pixels become outline). Weight 1 is the new standard.
- **Grid detection bug fix**: detect_grid() was preferring tiny cell subdivisions (7×4) over correct grids (4×2). Fixed with excess_penalty and size_penalty terms.

**LoRA training was ABANDONED on April 8, 2026.** Sean explicitly decided to stop all LoRA work. Multiple attempts produced anime-proportioned characters, not SF2 arcade sprites. Gemini NB2 keyframes produce the correct style natively. Do NOT propose or include LoRA training in any plans.

**Agent fleet status (from downsizing audit April 9):** Only 2 agents are active — vault-indexer (daily 2:00 AM) and daily-driver morning (8:45 AM). 6 agents were disabled due to CLIConnectionError and MCP headless limitations. Do NOT re-enable without Sean's explicit approval.

---

## Required Reading

Read these files before doing anything else:

1. **`16bitfit-battle-mode/SOURCE-OF-TRUTH.md`** — The master reference document you'll be updating. Read the ENTIRE file.
2. **`16bitfit-battle-mode/prompts-and-summaries/PHASE5C-SUMMARY.md`** — The latest phase results with all the data you need for the SOT update.
3. **`16bitfit-battle-mode/prompts-and-summaries/AUTORESEARCH-PLAN.md`** — The current draft plan that needs revision. Contains a LoRA training phase that contradicts Sean's decision.
4. **`16bitfit-battle-mode/phase-5-completion-summary.md`** — Phase 5 task completion results (9/9 PASS).
5. **`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`** — Agent fleet status. Only 2 active.

---

## Task 1: Update SOURCE-OF-TRUTH.md

<instructions>
Update the SOURCE-OF-TRUTH.md to reflect Phase 5 completion. This is a document edit task — be precise and preserve the existing structure.

### Changes required:

**1. Last-Updated header (line 4):**
Update to:
```
**Last Updated:** 2026-04-11 — Phase 5 COMPLETE. 12/12 characters, 180/180 animations, 1020 IMAGE_ONLY + 815 HYBRID frames, 0 failures, ~$12.60. Sheet→split approach LOCKED. Anchor image Golden Rule enforced. RIFE VFI connectivity fixed. Palette expanded (Sean 27, generic 38). 3 idle animations need re-gen (Marcus, Gym Bully, Procrastination Phantom). Autoresearch plan in revision.
```

**2. Workstream B section — add Phase 5 results:**
After the existing "NON-NEGOTIABLE" paragraph in Workstream B, add a new subsection documenting:
- The sprite sheet → split approach (replaces per-frame generation)
- Anchor image Golden Rule (3 refs per call, RuntimeError enforcement)
- 15 animation types mapped (10 IMAGE_ONLY, 5 HYBRID) with frame counts
- Full roster results table (from PHASE5C-SUMMARY.md Task 4)
- Palette details (Sean 27 colors, sf2_pixel_art 38 colors, outline weight 1)
- Cost data (~$12.60 for 180 animations)
- RIFE VFI results (60/60 HYBRID, 815 interpolated frames)
- 3 animations needing re-generation and why

**3. Phase 5 checklist (Part 4, under "Phase 5: Autoresearch + Scale"):**
Mark completed items from phase-5-completion-summary.md. Add new completed items:
- [x] Sheet→split approach for IMAGE_ONLY generation (replaces per-frame)
- [x] Full roster: 12/12 characters, 180/180 animations, 1020 frames, 0 failures
- [x] HYBRID pipeline: 60/60 animations interpolated via RIFE VFI (815 frames)
- [x] Palette expansion: Sean 16→27, generic sf2_pixel_art 38 colors
- [x] Grid detection bug fixed (excess_penalty + size_penalty)
- [x] RIFE connectivity fixed (VPN root cause, httpx retries, pre-flight health check)
- [x] Pixel Quantizer verified on 7/12 characters (100% pass, 0 off-palette)
- [x] PixelLabAdapter built behind VideoModelAdapter interface

Add remaining items:
- [ ] Re-generate 3 problematic idle animations (Marcus text overlay, Gym Bully + Procrastination Phantom multi-character)
- [ ] Run Pixel Quantizer on full roster (remaining 5 characters)
- [ ] Autoresearch plan revision (remove LoRA, focus on Gemini prompt optimization + LoRA-free ComfyUI optimization)

**4. Open Question #2 — update the resolution:**
The current text references "Wan 2.2 5B ti2v" as primary. Update to reflect that RIFE VFI is the confirmed primary interpolation engine, Wan 2.2 14B is available for single-keyframe animation, and the production pipeline is NB2 keyframes → RIFE VFI → Pixel Quantizer.

**5. Part 6: Key Numbers — update actual counts:**
- Total frames generated: 1,835 (1,020 IMAGE_ONLY + 815 HYBRID)
- Animations: 180 (15 per character × 12 characters)
- Generation cost: ~$12.60
- Agent fleet: 2 active (not 15-18 target — update note)

### Self-check after editing:
- [ ] No mention of LoRA as a future/planned activity (only in the ABANDONED historical section)
- [ ] Phase 5 marked COMPLETE with dates
- [ ] All data matches PHASE5C-SUMMARY.md numbers exactly
- [ ] Agent counts reflect the April 9 downsizing audit (2 active, not 8 or 15-18)
- [ ] Outline weight recommendation is 1 (not 2)
</instructions>

---

## Task 2: Collaboratively Revise AUTORESEARCH-PLAN.md

<instructions>
After completing the SOT update, shift to a **collaborative, conversational mode** for the autoresearch plan. Do NOT rewrite the plan unilaterally. Instead, walk Sean through the key decisions by asking questions one at a time.

### Critical issue to flag first:
The current AUTORESEARCH-PLAN.md has a **Phase 1: LoRA Training** section. Sean explicitly abandoned LoRA on April 8. Flag this contradiction clearly and confirm it should be removed before proceeding.

### Questions to work through with Sean (ask ONE at a time, wait for response):

**1. Scope question:**
"The current plan has three phases: Phase 0 (Gemini prompt optimization), Phase 1 (LoRA training — which you've abandoned), and Phase 2 (ComfyUI workflow optimization that depends on the LoRA). With LoRA removed, we have two options: (A) keep Phase 0 as a standalone experiment to optimize your Gemini prompts, or (B) redesign Phase 2 to work without LoRA — using anchor images + IP-Adapter + ControlNet instead. Which interests you more, or should we plan both?"

**2. Phase 0 value question:**
"Phase 0 optimizes the text prompts sent to Gemini. You already have 1,020 frames that work. The potential gain is marginal quality improvements and fewer re-generation needs. It costs ~$0.07 per experiment (50-100 experiments = $3.50-$7.00). Is this worth pursuing now, or would you rather focus on the ComfyUI side?"

**3. ComfyUI scope question (if Phase 2 is desired):**
"Without LoRA, the ComfyUI autoresearch would optimize: IP-Adapter weight (how much the anchor images influence generation), ControlNet strength (pose guidance), CFG scale (prompt adherence), sampler choice, and step count. This runs entirely on the Alienware for free. The question is: what's the GOAL? Are you trying to (A) replace Gemini with a local ComfyUI pipeline, or (B) use ComfyUI as a post-processing/refinement step on Gemini output?"

**4. Scoring pipeline question:**
"The plan proposes a composite score: 35% CLIP similarity + 30% LPIPS + 20% Pixel Quantizer pass + 15% SSIM. There's also a more advanced option from the SOURCE-OF-TRUTH: DISTS + DINOv2 + EDOKS + Qwen3-VL as an LLM judge. The simpler scoring is faster to build. The advanced version catches more subtle quality issues but requires installing more dependencies on the Alienware. Which would you prefer to start with?"

**5. Orchestration question:**
"The plan has the Mac Mini orchestrating the Alienware via SSH/REST, with a Claude Agent SDK agent running the loop. But only 2 agents are active right now, and the headless SDK can't access MCP servers. Should the autoresearch agent run as: (A) a new Agent SDK agent on the Mac Mini (adds complexity, needs approval), (B) a standalone Python script on the Mac Mini that just calls the Alienware's ComfyUI API (simpler, no SDK needed), or (C) a Claude Code prompt you paste into a terminal on the Alienware (simplest, but not autonomous)?"

**6. Timeline/priority question:**
"Before running autoresearch, you mentioned wanting to review the sprites that were already generated. After that review, what's your priority order: (A) fix the 3 broken idle animations → review all sprites → then autoresearch, or (B) go straight into autoresearch to improve quality BEFORE reviewing everything?"

### After all questions are answered:
Rewrite AUTORESEARCH-PLAN.md incorporating Sean's decisions. Remove the LoRA Phase 1 entirely. Update the composite score, machine assignments, and implementation order based on his answers. Keep the Karpathy three-file pattern structure — it's elegant and Sean likes it.

### Self-check after rewriting:
- [ ] Zero references to LoRA training as a planned or future activity
- [ ] Implementation order matches Sean's stated priorities
- [ ] Machine assignments are accurate (Mac Mini orchestrator, Alienware GPU)
- [ ] Safety constraints are preserved ($2 agent cap, 8hr limit, 120s kill timeout)
- [ ] Open questions from the original plan are resolved or explicitly deferred
</instructions>

---

## Deferred Tasks (DO NOT work on these — just track them)

<deferred_tasks>
These tasks are parked for a future session. Note them so nothing is forgotten, but do NOT start them.

1. **Re-generate 3 idle animations:**
   - Marcus: "Idle Neutral" text burned into frame_00. Fix: add "no text, no labels, no captions" to negative prompt.
   - Gym Bully: Multiple characters per cell in idle. Fix: add "exactly ONE character per cell" constraint.
   - Procrastination Phantom: Same multi-character issue as Gym Bully.
   - All other animations for these characters are clean — only idle needs re-gen.

2. **Run Pixel Quantizer on full roster:**
   - 7/12 characters verified (Sean, Aria, Kenji, Marcus, Gym Bully, Procrastination Phantom, Sloth Demon).
   - Remaining 5: Mary, Zara, Stress Titan, Training Dummy, Ultimate Slump.
   - Use `--outline-weight 1` and appropriate palette (sean for Sean, sf2_pixel_art for all others).

3. **Visual sprite review:**
   - Sean wants to personally review all generated sprites before making further pipeline decisions.
   - This review may change priorities for autoresearch and re-generation.
</deferred_tasks>

---

## Rules for This Session

- You are in a **Cowork planning session**, not Claude Code. No code execution.
- Sean is a beginner coder. Explain technical choices clearly but don't over-explain.
- For Task 1 (SOT update): just do it. Don't ask questions — the data is in the files.
- For Task 2 (autoresearch): be conversational. Ask ONE question at a time. Wait for Sean's answer before moving to the next question.
- **Never propose LoRA training.** It's abandoned. Period.
- **Never propose re-enabling disabled agents** without Sean's explicit approval.
- When referencing costs, use actual numbers from PHASE5C-SUMMARY.md (~$0.07/Gemini call).
</instructions>
