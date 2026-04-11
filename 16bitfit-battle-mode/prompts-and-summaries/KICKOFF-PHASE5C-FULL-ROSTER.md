# Phase 5C Kickoff: Fix Pipeline + Scale to Full Roster

Paste this entire file as your opening prompt in a new Claude Code session.

---

You are continuing the 16BitFit Battle Mode build — Phase 5C (pipeline fixes + full roster generation). Phase 5B is complete: per-frame generation validated, RIFE interpolation working, Pixel Quantizer passing all gates. Now we need to integrate the validated approaches into the batch orchestrator and generate sprites for all 12 characters.

<role>
You are a senior graphics pipeline engineer. You write clean, tested Python and TypeScript. You verify results visually (read the output PNGs) and quantitatively (run the Pixel Quantizer scoring pipeline). You do not skip verification gates — if a task fails its gate, you diagnose and fix before proceeding.
</role>

<context>
Read these files before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/PHASE5B-VALIDATION-RESULTS.md` — What was validated and what still needs fixing
3. `16bitfit-battle-mode/pixel-quantizer/batch/batch_orchestrator.py` — Current batch pipeline (NEEDS UPDATES)
4. `16bitfit-battle-mode/pixel-quantizer/batch/generate_sheet_split.py` — Validated sheet→split approach (reference implementation)
5. `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — GeminiAdapter + RIFEAdapter (RIFE already fixed in 5B)
6. `16bitfit-battle-mode/pixel-quantizer/video-eval/strategy_router.py` — Strategy map (IMAGE_ONLY vs HYBRID routing)
7. `16bitfit-battle-mode/pixel-quantizer/prompts/prompt_library.py` — Animation templates with per-frame pose descriptions
8. `16bitfit-battle-mode/pixel-quantizer/src/palettes/sean.json` — Current 16-color palette (NEEDS EXPANSION)
9. `16bitfit-battle-mode/pixel-quantizer/src/cli.ts` — Pixel Quantizer CLI entry point

After reading, confirm you understand:
(a) Phase 5B proved that individual per-frame Gemini API calls produce INCONSISTENT characters (different hair, outfit, skin each frame). The fix is generating all frames as a single sprite sheet, then splitting programmatically.
(b) The batch orchestrator's IMAGE_ONLY path (lines 195-226) still uses the broken per-frame approach. It must be rewritten to use the sheet→split approach from `generate_sheet_split.py`.
(c) The batch orchestrator's HYBRID path (lines 227-256) has a TODO at line 255: "Extract frames from video, run Pixel Quantizer, score." The RIFEAdapter returns a `GeneratedVideo` with raw MP4 bytes in `.data` — you must extract frames from this (ffmpeg or PyAV).
(d) The RIFEAdapter was already fixed in Phase 5B (added `scale_factor`, `dtype`, `torch_compile`, `batch_size` to RIFE VFI node; added `loop_count`, `pingpong`, `save_output` to VHS_VideoCombine; fixed `gifs` output key). Do NOT re-fix these.
(e) Alienware ComfyUI is accessible at 192.168.68.201:8188 (HTTP works, ICMP ping is blocked). Running `--listen 0.0.0.0 --port 8188 --force-fp16`.
</context>

<constraints>
Same constraints as all previous phases:
- Gemini model: `gemini-3.1-flash-image-preview` (NB2). NOT NB Pro unless explicitly told.
- GOLDEN RULE: Every Gemini generation MUST include the character's 3 anchor reference images. No text-only prompts. Ever.
- Green screen (#00FF00) on ALL keyframes BEFORE feeding to video/interpolation models
- Sprites facing RIGHT
- Champions 128x128, Bosses 256x256
- RTX 5080 uses SDPA (NO xformers), ComfyUI with `--force-fp16`
- Wan 2.2 (NOT 2.5)
- Credentials from macOS Keychain via `lib/keychain.py`, not .env files
- Package name `claude-agent-sdk`, class `ClaudeAgentOptions`
- Anchor images path: `16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/`
</constraints>

<what_changed_in_phase_5b>
These are the validated findings from Phase 5B. Do not re-validate — treat as proven:

1. **Per-frame API calls are broken** — Each independent Gemini call produces a completely different character (different hair, outfit, skin tone) despite sending 3 anchor images. This is a fundamental limitation of text+image conditioning across separate API calls.

2. **Sprite sheet approach works** — Generating all frames as a single composite sprite sheet in one Gemini call, then splitting programmatically, produces excellent character consistency. Tested on idle (4 frames), walk_forward (8 frames), light_punch (6 frames) for Sean.

3. **Gemini generates more grid cells than requested** — When asked for a 2x2 grid, Gemini often produces 4x2 (8 cells). The `detect_grid()` function in `generate_sheet_split.py` auto-detects the actual grid layout based on image dimensions and cell aspect ratio.

4. **RIFE VFI is working** — 3 keyframes → 9 interpolated frames in <1s on RTX 5080. Character identity preserved. Green screen maintained. Output is under the `gifs` key in ComfyUI history (not `videos`).

5. **Pixel Quantizer passes** — 14/14 frames passed (0 off-palette pixels, outline coverage 0.776-0.858, clean backgrounds). BUT quantized sprites are very dark because Sean's 16-color palette lacks mid-tones.

6. **Sequential conditioning also works** — Sending the previous frame as additional context to each Gemini call maintains consistency, but costs 6x more and takes 5x longer. Use as fallback only.

7. **New script exists**: `batch/generate_sheet_split.py` — standalone reference implementation with `approach_sheet()`, `approach_sequential()`, `detect_grid()`, `split_sheet()`, `call_gemini()`, `load_anchors()`.
</what_changed_in_phase_5b>

<tasks>
Complete these 4 tasks IN ORDER. Each has a verification gate.

=== TASK 1: Update Batch Orchestrator — IMAGE_ONLY Sheet Approach ===

Rewrite the IMAGE_ONLY branch of `batch_orchestrator.py` (lines 195-226) to use the sprite sheet → split approach instead of per-frame generation.

What to do:
1. Extract the reusable functions from `generate_sheet_split.py` — specifically `build_sheet_prompt()`, `detect_grid()`, `split_sheet()`, `call_gemini()`, `load_anchors()`, and `get_grid_layout()`. Either import them or integrate into the orchestrator.
2. Replace the per-frame loop (lines 197-224) with:
   a. Build a sprite sheet prompt using all frame poses for the animation
   b. Call Gemini ONCE with anchor images + sheet prompt
   c. Auto-detect the grid layout from the returned image
   d. Split into individual frame PNGs
   e. Save each frame to `output/{character}/{animation}/frame_{idx:02d}.png`
   f. Also save the full sheet as `output/{character}/{animation}/{animation}_sheet.png` for debugging
3. Keep the dry-run path working (print what would happen without calling APIs)
4. Keep the resume path working (skip COMPLETE animations)

GATE 1: Run the orchestrator on Sean's `idle` animation (clear the output first) and visually verify 4 consistent frames. Then run on `light_punch` (6 frames). Both must show the same character (blonde hair, white tank top, blue pants).
- Command: `cd pixel-quantizer && python3 batch/batch_orchestrator.py manifests/champion_sean.json --resume`
- If `--resume` skips idle because it's marked COMPLETE in batch_status.json, either delete the status file or add a `--force` flag.

=== TASK 2: Update Batch Orchestrator — HYBRID Frame Extraction ===

Complete the TODO at line 255 of `batch_orchestrator.py` for the HYBRID path. After RIFE interpolation returns a `GeneratedVideo`, extract individual frames and save them.

What to do:
1. `GeneratedVideo.data` contains raw MP4 bytes. Write them to a temp file.
2. Use ffmpeg (subprocess) or PyAV to extract all frames as PNGs:
   ```
   ffmpeg -i temp.mp4 -vsync 0 output/{char}/{anim}/frame_%02d.png
   ```
3. Count the extracted frames and update `result.frames_generated`.
4. Clean up the temp file.
5. The HYBRID path currently only generates keyframes from `start_pose` and `end_pose` (2 frames). It should generate ALL keyframes defined in `kf_prompts` (typically 3). Fix the KeyframeConfig creation to handle multiple keyframes — either:
   a. Generate keyframes as a sprite sheet (same sheet→split approach), then pass to RIFE, OR
   b. Generate each keyframe individually (only 3 calls, acceptable cost) with anchor images

GATE 2: Run the orchestrator on Sean's `walk_forward` animation (HYBRID strategy, 3 keyframes → RIFE → frames). Verify:
- Keyframes were generated with anchor images (golden rule)
- RIFE interpolation produced smooth frames
- Extracted frames are saved as individual PNGs
- Frame count matches expectation

=== TASK 3: Expand Sean's Palette ===

The current 16-color palette produces very dark quantized output because:
- There are only 2 skin tones (skin #F5D6C6, skin_shadow #D4B5A5) — needs a mid-tone and a highlight
- There are only 2 clothing tones per item (base + shadow) — needs mid-tones
- The outline color (#272929) is too close to black, so the palette quantizer over-maps to it

What to do:
1. Read the anchor images for Sean: `16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/champions/Sean/champion_sean_anchor-1.png`
2. Extract the dominant colors from the anchor image using k-means clustering or color histogram analysis (Python with PIL/sklearn)
3. Create an expanded palette (24-32 colors) that adds:
   - Skin: highlight, mid-tone, base, shadow (4 tones)
   - Hair: highlight, base, shadow (3 tones)
   - Tank top: highlight, base, shadow (3 tones)
   - Pants: highlight, base, shadow (3 tones)
   - Shoes: highlight, base, shadow (3 tones)
   - Outline: keep #272929 for silhouette, add a lighter dark (#3A3C3C or similar) for internal detail lines
   - Keep chroma key #00FF00, black #000000, white #FFFFFF
4. Save to `src/palettes/sean.json` (overwrite the existing file)
5. Format: `[{ "hex": "#F5D6C6", "r": 245, "g": 214, "b": 198, "name": "skin_base" }, ...]`

GATE 3: Re-run the Pixel Quantizer on Sean's idle frames with the new palette:
```bash
npx tsx src/cli.ts --input output/sean/idle --output output/sean/idle_quantized --palette sean --target-size 128 --verbose
```
Visually inspect the quantized output. The sprites should look brighter and more detailed than Phase 5B's dark output. Still must pass: 0 off-palette pixels, clean outlines, clean background.

=== TASK 4: Scale to Full Roster ===

Generate sprites for all 12 characters using the updated batch orchestrator.

Character manifests (all in `pixel-quantizer/manifests/`):
- Champions (128x128): champion_sean.json, champion_aria.json, champion_kenji.json, champion_marcus.json, champion_mary.json, champion_zara.json
- Bosses (256x256): boss_gym_bully.json, boss_procrastination_phantom.json, boss_sloth_demon.json, boss_stress_titan.json, boss_training_dummy.json, boss_ultimate_slump.json

What to do:
1. First, create palettes for each character (or use a generic "sf2_pixel_art" palette extracted from the anchor images). At minimum, register each in `src/palettes/index.ts`.
2. Run the batch orchestrator for each character:
   ```bash
   for manifest in manifests/champion_*.json manifests/boss_*.json; do
     python3 batch/batch_orchestrator.py "$manifest"
   done
   ```
3. Add a 10-second delay between characters to avoid Gemini rate limiting.
4. IMAGE_ONLY animations should use the sheet→split approach (Task 1 fix).
5. HYBRID animations should generate keyframes → RIFE → extract frames (Task 2 fix).
6. If Alienware goes offline mid-run, HYBRID animations should be skipped (not crash the whole run). The `--resume` flag should let you pick them up later.

GATE 4: At least 10/12 characters should complete with all IMAGE_ONLY animations passing. HYBRID may have partial failures depending on Alienware stability. Report:
- Characters completed vs failed
- Total animations completed vs failed
- Any patterns in failures (rate limiting? specific animation types?)

After generation, run the Pixel Quantizer on at least 3 different characters' idle animations and report scores.
</tasks>

<rate_limiting_strategy>
Gemini rate limits are real. Use this strategy:
- 10-second delay between animation sheet generations within a character
- 15-second delay between characters
- If you get a 429 or 503, the retry logic in the adapter handles it (3 retries with 5/15/30s backoff)
- If a character fails entirely, log the error and continue to the next character
- The `--resume` flag lets you re-run to pick up failures later
</rate_limiting_strategy>

<output_format>
For each task:
1. Show the code changes you made (file + what changed)
2. Show the commands you ran
3. Display output images (read the PNGs) for at least 2 frames per tested animation
4. Report PASS or FAIL at the gate with specific reasons
5. If FAIL, show the fix and re-verification

After all 4 tasks, update `16bitfit-battle-mode/PHASE5B-VALIDATION-RESULTS.md` (append a "Phase 5C Results" section) covering:
- Batch orchestrator changes (sheet approach + RIFE extraction)
- Palette expansion results
- Full roster generation summary (pass/fail per character)
- Total cost estimate (number of Gemini API calls made)
- Any issues for the next phase
</output_format>

<validation>
Before finishing, self-check:
1. Did the batch orchestrator's IMAGE_ONLY path use the sheet→split approach (NOT per-frame calls)?
2. Did every Gemini call include anchor images? (Golden rule — no exceptions)
3. Did the HYBRID path extract frames from RIFE's MP4 output?
4. Did you visually inspect quantized output with the expanded palette?
5. Did you run the full roster (or at least attempt all 12 characters)?
6. Are all results documented?
</validation>
