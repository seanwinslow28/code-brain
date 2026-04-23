# Phase 5C Completion + Autoresearch Kickoff

Paste this entire file as your opening prompt in a new Claude Code session.

---

You are continuing the 16BitFit Battle Mode build. Phase 5C generated sprites for all 12 characters (1020 frames, 180 animations, 0 failures), but the 60 HYBRID animations only have keyframes — RIFE interpolation failed because the RIFEAdapter couldn't connect to the Alienware. After fixing that and reviewing output, we move to autoresearch.

<role>
You are a senior graphics pipeline engineer and ML ops specialist. You write clean, tested Python. You verify results visually (read the output PNGs) and quantitatively (run the Pixel Quantizer scoring pipeline). You do not skip verification gates — if a task fails its gate, you diagnose and fix before proceeding.
</role>

<context>
Read these files IN ORDER before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/PHASE5C-SUMMARY.md` — **THE MOST IMPORTANT FILE.** Complete summary of what was done, what failed, and why. Read every section.
3. `16bitfit-battle-mode/PHASE5B-VALIDATION-RESULTS.md` — Includes Phase 5C results appended at the bottom
4. `16bitfit-battle-mode/pixel-quantizer/batch/batch_orchestrator.py` — Updated orchestrator with sheet→split + HYBRID extraction
5. `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — RIFEAdapter (lines 1000-1220) — THIS IS WHERE THE BUG IS
6. `16bitfit-battle-mode/pixel-quantizer/batch/generate_sheet_split.py` — Sheet→split utilities (detect_grid, split_sheet, etc.)

After reading, confirm you understand:
(a) All 120 IMAGE_ONLY animations completed successfully via sprite sheet→split approach.
(b) All 60 HYBRID animations have keyframes saved (`keyframe_00.png`, `keyframe_01.png`, etc.) but NO interpolated frames — RIFE failed with "All connection attempts failed."
(c) The Alienware WAS online the entire time with ComfyUI running at `192.168.68.201:8188` with `--listen 0.0.0.0 --port 8188 --force-fp16`.
(d) The failure is a connectivity issue in the RIFEAdapter's httpx client, NOT the Alienware being offline.
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

<critical_rule>
**ALIENWARE CONNECTIVITY: ICMP PING IS BLOCKED. HTTP WORKS FINE.**

The Alienware at 192.168.68.201 blocks ICMP ping. This has caused failures in Phase 5B and Phase 5C. Every time you interact with the Alienware:

1. NEVER use `ping` to check if it's online. It will always fail.
2. ALWAYS verify via HTTP first:
   ```bash
   curl -s --connect-timeout 5 http://192.168.68.201:8188/system_stats
   ```
3. If curl works but httpx fails, the issue is in httpx's connection handling — NOT the Alienware being down.
4. The RIFEAdapter uses `httpx.AsyncClient(timeout=120.0)` which may have DNS/resolver issues in the Claude Code sandbox. Consider adding `transport=httpx.AsyncHTTPTransport(retries=3)` or a pre-flight HTTP health check.
</critical_rule>

<tasks>
Complete these tasks IN ORDER. Each has a verification gate.

=== PART A: FIX RIFE + COMPLETE HYBRID ANIMATIONS ===

== TASK 1: Diagnose and Fix RIFEAdapter Connectivity ==

The RIFEAdapter in `video-eval/adapters.py` (line ~1062) creates an httpx client that fails to connect to `192.168.68.201:8188` despite the machine being up.

What to do:
1. First, verify Alienware is reachable via curl:
   ```bash
   curl -s --connect-timeout 5 http://192.168.68.201:8188/system_stats
   ```
2. If curl works, the issue is in httpx. Diagnose with a minimal Python test:
   ```python
   import httpx, asyncio
   async def test():
       async with httpx.AsyncClient(timeout=30.0) as c:
           r = await c.get("http://192.168.68.201:8188/system_stats")
           print(r.status_code, r.text[:200])
   asyncio.run(test())
   ```
3. If httpx fails, try these fixes in order:
   a. Add explicit `transport=httpx.AsyncHTTPTransport(retries=3)` to the client
   b. Try `httpx.AsyncClient(base_url=base_url, timeout=httpx.Timeout(30.0, connect=10.0))`
   c. If httpx is fundamentally broken in the sandbox, fall back to subprocess curl or aiohttp
4. Add a pre-flight health check at the start of `interpolate_frames()` that calls `/system_stats` before attempting the full workflow. If the health check fails, raise a clear error: "Alienware ComfyUI unreachable at {host}:{port}"

GATE 1: The httpx client can successfully call `http://192.168.68.201:8188/system_stats` from within the RIFEAdapter. Show the response.

== TASK 2: Run HYBRID Animations via --resume ==

Once the RIFEAdapter connectivity is fixed, re-run the batch orchestrator for all 12 characters with `--resume`. This should:
- Skip all IMAGE_ONLY animations (already COMPLETE)
- Re-attempt HYBRID animations that have keyframes but no interpolated frames
- Upload keyframes to ComfyUI, run RIFE VFI, download interpolated video, extract frames via ffmpeg

What to do:
1. Run for Sean first as a test:
   ```bash
   cd pixel-quantizer && python3 batch/batch_orchestrator.py manifests/champion_sean.json --resume
   ```
2. Verify Sean's walk_forward produces interpolated frames (should go from 4 keyframes → 8+ smooth frames)
3. If Sean passes, run all remaining characters:
   ```bash
   for manifest in manifests/champion_*.json manifests/boss_*.json; do
     python3 batch/batch_orchestrator.py "$manifest" --resume
     sleep 15
   done
   ```

GATE 2: At least Sean's walk_forward should have interpolated frames (more than the 4 keyframes). Visually inspect 2-3 interpolated frames — character identity should be preserved, green screen maintained.

=== PART B: REVIEW ALL OUTPUT ===

== TASK 3: Visual Quality Audit ==

Spot-check the full roster for quality issues.

What to do:
1. For each of the 12 characters, read their `idle` sprite sheet and at least 1 attack animation sheet. Report any issues:
   - Character not matching anchor reference (wrong hair, outfit, etc.)
   - Multiple characters in a single grid cell
   - Green screen bleeding into character
   - Poses too similar across frames (no animation readability)
2. Run the Pixel Quantizer on 3 different characters' light_punch animations with `--outline-weight 1`:
   ```bash
   for char in marcus procrastination_phantom sloth_demon; do
     npx tsx src/cli.ts --input output/$char/light_punch --output output/$char/light_punch_quantized --palette sf2_pixel_art --target-size 128 --outline-weight 1 --verbose
   done
   ```
   (Use `--target-size 256` for bosses)
3. Report a quality summary: characters that look great vs. characters that need re-generation

GATE 3: Provide a visual quality report with at least 6 sprite sheets shown (mix of champions and bosses, mix of idle/attack/movement).

=== PART C: AUTORESEARCH SETUP ===

== TASK 4: Read and Synthesize Autoresearch Docs ==

Read these files to understand the autoresearch pattern:
1. `16bitfit-battle-mode/docs/lora-autoresearch/autoresearch-overview.md`
2. `16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-lora-training.md`
3. `16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-compatibility.md`

Then propose a concrete plan for the first autoresearch experiment:
- What is the mutable artifact? (e.g., ComfyUI workflow JSON, LoRA training config, prompt template)
- What is the metric? (e.g., Pixel Quantizer score, CLIP similarity to anchor, human-eval proxy)
- What is the `program.md` equivalent? (Natural language instructions for the agent)
- Which machine runs it? (Alienware for GPU, Mac Mini for orchestration)
- What are the safety constraints? (Cost cap, time limit, revert-on-failure)

Do NOT start building the autoresearch loop yet. Present the plan for review first.

GATE 4: A written plan (saved to `16bitfit-battle-mode/AUTORESEARCH-PLAN.md`) that maps the Karpathy three-file pattern to the 16BitFit sprite pipeline. The plan must be specific enough to execute in the next session.
</tasks>

<output_format>
For each task:
1. Show the code changes you made (file + what changed)
2. Show the commands you ran
3. Display output images (read the PNGs) for verification
4. Report PASS or FAIL at the gate with specific reasons
5. If FAIL, show the fix and re-verification

After all tasks, update `16bitfit-battle-mode/PHASE5C-SUMMARY.md` (append a "Phase 5C Completion" section) covering:
- RIFE connectivity fix (what was wrong, what fixed it)
- HYBRID animation results (how many completed, any failures)
- Visual quality audit results
- Autoresearch plan summary
</output_format>

<validation>
Before finishing, self-check:
1. Did you verify Alienware via HTTP (not ping) before attempting RIFE?
2. Did the RIFEAdapter successfully connect and produce interpolated frames?
3. Did you visually inspect sprite sheets from at least 6 different characters?
4. Did you run the Pixel Quantizer on at least 3 characters and report scores?
5. Did you write the autoresearch plan to a file?
6. Are all results documented?
</validation>
