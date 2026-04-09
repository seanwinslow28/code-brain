# Phase 5B Kickoff: Pipeline Validation & Per-Frame Consistency

Paste this entire file as your opening prompt in a new Claude Code session.

---

You are continuing the 16BitFit Battle Mode build — Phase 5B (pipeline validation). Phase 5A is complete: all infrastructure built, 12/12 character sprite sheets passed with anchor image conditioning. Now we need to validate the per-frame generation pipeline and tune for animation-quality consistency.

<role>
You are a senior graphics pipeline engineer. You write clean, tested Python and TypeScript. You verify results visually (read the output PNGs) and quantitatively (run the Pixel Quantizer scoring pipeline). You do not skip verification gates — if a task fails its gate, you diagnose and fix before proceeding.
</role>

<context>
Read these files before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/pixel-quantizer/output/_character_tests/CHARACTER-TEST-REPORT.md` — What worked and what didn't in the Phase 5A character tests
3. `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — GeminiAdapter (lines 182-340) with anchor image conditioning and retry logic
4. `16bitfit-battle-mode/pixel-quantizer/video-eval/strategy_router.py` — Strategy map and GenerationPlan
5. `16bitfit-battle-mode/pixel-quantizer/batch/batch_orchestrator.py` — Batch generation pipeline
6. `16bitfit-battle-mode/pixel-quantizer/prompts/prompt_library.py` — 15 animation prompt templates
7. `16bitfit-battle-mode/pixel-quantizer/src/cli.ts` — Pixel Quantizer CLI entry point (TypeScript/Node)
8. `16bitfit-battle-mode/pixel-quantizer/src/pipeline.ts` — Pixel Quantizer 7-step pipeline

After reading, confirm you understand:
(a) The GeminiAdapter ALWAYS sends anchor images (golden rule — raises RuntimeError if missing)
(b) The sprite sheet test (single composite image) passed 12/12, but per-frame generation (individual API calls) has NOT been validated with anchors yet
(c) The Pixel Quantizer is a TypeScript CLI: `npx tsx src/cli.ts --input <dir> --output <dir> --palette <name> --target-size 128`
(d) HYBRID animations use NB2 keyframes → RIFE VFI on Alienware (192.168.68.201:8188) → Pixel Quantizer
(e) The RIFE workflow JSON was updated with required node inputs (dtype, scale_factor, torch_compile, batch_size) on 2026-04-09
</context>

<constraints>
Same constraints as all previous phases:
- Gemini model: `gemini-3.1-flash-image-preview` (NB2). NOT NB Pro unless explicitly told.
- GOLDEN RULE: Every Gemini generation MUST include the character's 3 anchor reference images. No text-only prompts. Ever.
- Green screen (#00FF00) on ALL keyframes BEFORE feeding to video/interpolation models
- Sprites facing RIGHT
- Champions 128×128, Bosses 256×256
- RTX 5080 uses SDPA (NO xformers), ComfyUI with `--force-fp16`
- Wan 2.2 (NOT 2.5)
- Credentials from macOS Keychain via `lib/keychain.py`, not .env files
- Package name `claude-agent-sdk`, class `ClaudeAgentOptions`
- Anchor images path: `16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/`
</constraints>

<what_changed_since_last_session>
These fixes were applied at the end of the Phase 5A session:
1. GeminiAdapter rewritten — now loads anchor PNGs, sends as multi-modal inlineData parts, caches per character
2. Retry logic added — 3 retries with 5/15/30s backoff for Gemini 503/429
3. `responseMimeType: "image/png"` removed from Gemini payload (was causing 400 errors)
4. KeyframeConfig dataclass extended with `anchor_images: list[str]` and `description: str`
5. Batch orchestrator updated to pass `anchor_images` and `description` from manifest to KeyframeConfig
6. RIFE workflow JSON updated with all required fields for current Alienware ComfyUI node versions
7. 12/12 character sprite sheet test PASSED — character identity is strong with anchor conditioning
</what_changed_since_last_session>

<tasks>
Complete these 4 tasks IN ORDER. Each has a verification gate. Do not start the next task until the current one passes its gate.

=== TASK 1: Per-Frame Generation with Anchors (Sean, idle animation) ===

The sprite sheet test proved anchors work within a single composite image. Now test whether individual per-frame API calls maintain character consistency when each frame is a separate Gemini request.

1. Run the batch orchestrator for Sean, but ONLY the `idle` animation (4 frames):
   - `cd pixel-quantizer && python3 batch/batch_orchestrator.py manifests/champion_sean.json --resume`
   - The `--resume` flag will skip animations that already completed. You may need to clear `output/sean/idle/` first if stale frames exist from the pre-anchor run.
   - Alternatively, modify the orchestrator call or write a quick script to generate just idle.

2. After generation, visually inspect all 4 frames side by side:
   - Read each frame PNG and display it
   - Evaluate: Is Sean recognizable across all 4? Same hair, same clothes, same proportions?
   - Compare to the sprite sheet test output at `output/_character_tests/champion_sean_sheet.png`

GATE 1: Are all 4 idle frames character-consistent? (Same person across frames, matching the anchor reference)
- If YES → proceed to Task 2
- If NO → diagnose why. Possible fixes: (a) include previously generated frame as additional context in the next request, (b) generate 4 frames in a single multi-pose sheet request then split, (c) increase prompt specificity with more character detail. Try the fix, re-run, re-evaluate.

=== TASK 2: HYBRID Pipeline End-to-End (Sean, walk_forward) ===

Test the full keyframe-to-interpolation chain: NB2 generates keyframes with anchors → upload to Alienware ComfyUI → RIFE VFI interpolates → download result frames.

1. Generate 4 NB2 keyframes for Sean's walk_forward using the prompt library's keyframe prompts:
   - The strategy router routes walk_forward to HYBRID with 4 keyframes
   - Each keyframe must include anchor images (golden rule)
   - Save keyframes to `output/sean/walk_forward/keyframe_00.png` through `keyframe_03.png`

2. Upload the keyframes to Alienware and queue the RIFE workflow:
   - The RIFEAdapter in adapters.py handles this via ComfyUI REST at 192.168.68.201:8188
   - The updated workflow JSON includes all required fields (dtype, scale_factor, etc.)
   - If the Alienware is offline, use WOL (MAC: B4:E9:B8:F7:71:47) or note it as a blocker

3. Download the interpolated frames and visually inspect

GATE 2: Did RIFE produce interpolated frames? Are the interpolated frames smooth transitions between keyframes?
- If YES → proceed to Task 3
- If ALIENWARE OFFLINE → Document this as a blocker, skip to Task 3 using the IMAGE_ONLY frames from Task 1 instead
- If RIFE FAILS → Check the ComfyUI error. The workflow was updated but may still have issues. Query `192.168.68.201:8188/object_info/RIFE%20VFI` for the current node schema and fix.

=== TASK 3: Pixel Quantizer Pass ===

Run the TypeScript Pixel Quantizer pipeline on the generated frames to convert them from high-res Gemini output to game-ready 128×128 pixel art sprites.

1. First, check the Pixel Quantizer builds:
   ```bash
   cd 16bitfit-battle-mode/pixel-quantizer && npm install && npx tsx src/cli.ts --help
   ```

2. Run the quantizer on Sean's idle frames from Task 1:
   ```bash
   npx tsx src/cli.ts \
     --input output/sean/idle \
     --output output/sean/idle_quantized \
     --palette sean \
     --target-size 128 \
     --chroma-color "#00FF00" \
     --outline-weight 2 \
     --outline-color "#272929" \
     --verbose
   ```
   NOTE: The `--palette sean` may not exist yet. Check `src/palettes/index.ts` for available palettes. If Sean's palette doesn't exist, either use a generic palette or create one by extracting dominant colors from the anchor images.

3. If HYBRID frames exist from Task 2, also run the quantizer on those:
   ```bash
   npx tsx src/cli.ts \
     --input output/sean/walk_forward \
     --output output/sean/walk_forward_quantized \
     --palette sean \
     --target-size 128 \
     --verbose
   ```

4. Visually inspect the quantized output — read each output PNG
5. Report the pipeline scores (palette compliance, outline quality, BG purity, character presence)

GATE 3: Do quantized frames pass the quality gate? (Overall score > 75%, 0 off-palette pixels, clean outlines)
- If YES → proceed to Task 4
- If NO → identify which step is failing (downscale? palette? outline? alpha?) and adjust parameters. Re-run.

=== TASK 4: Prompt Tuning for Per-Frame Consistency ===

If Task 1 showed frame-to-frame inconsistency (different-looking character across individual frames), this task explores fixes. If Task 1 already showed strong consistency, this task validates it further with a combat animation (light_punch, 6 frames) and documents the approach.

Approach A — Batch sheet then split:
- Generate a 2x3 or 3x2 sprite sheet of all frames for one animation in a single Gemini call (like the character test, but with animation-specific poses instead of generic ones)
- Split the sheet into individual frames programmatically (crop each cell)
- This leverages the within-image consistency that proved strong in the sprite sheet test

Approach B — Sequential conditioning:
- Generate frame 1 with anchors only
- Generate frame 2 with anchors + frame 1 as additional reference
- Generate frame 3 with anchors + frame 2 as additional reference
- Each frame sees the previous frame, creating a consistency chain

Approach C — Prompt reinforcement:
- Add the character description TWICE in the prompt (beginning and end)
- Add "CRITICAL: This character has [specific distinguishing features]" 
- Add a negative constraint: "Do NOT change the character's appearance from the reference images"

Test at least TWO of these approaches on the same animation (light_punch, 6 frames for Sean). Compare the results visually. Report which approach produces the most consistent frames.

GATE 4: Document which approach works best. Save the winning frames. Update the prompt library or batch orchestrator if the approach requires code changes.
</tasks>

<output_format>
For each task:
1. Show the commands you ran
2. Display the output images (read the PNGs)
3. Report PASS or FAIL at the gate with specific reasons
4. If FAIL, show the fix and re-verification

After all 4 tasks, write a brief summary to `16bitfit-battle-mode/PHASE5B-VALIDATION-RESULTS.md` covering:
- Per-frame consistency: which approach won and why
- Pixel Quantizer scores for each tested animation
- HYBRID pipeline status (working / blocked on Alienware)
- Recommended approach for scaling to full roster
- Any issues that need fixing before the autoresearch run
</output_format>

<validation>
Before finishing, self-check:
1. Did every Gemini call include anchor images? (Golden rule — no exceptions)
2. Did you visually inspect output frames? (Don't just check file existence — READ the PNGs)
3. Did you run the Pixel Quantizer on at least one animation's frames?
4. Did you test at least 2 consistency approaches in Task 4?
5. Are the results documented in PHASE5B-VALIDATION-RESULTS.md?
</validation>
