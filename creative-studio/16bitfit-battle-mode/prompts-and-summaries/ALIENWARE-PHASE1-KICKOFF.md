# Alienware Phase 1 Kickoff Prompt — Copy/Paste into Claude Code

This prompt is designed for a Claude Code session running ON the Alienware (192.168.68.201),
where ComfyUI is installed and the RTX 5080 lives. It walks Claude Code through the manual
asset setup, the workflow build, and the autoresearch kickoff. Sean has already written the
frozen scorer, `program_comfyui.md`, and the pose-skeleton extraction guide on the Mac Mini
side — this session's job is the Alienware-local work and the final hand-off back to the
orchestrator.

---

## The Prompt

Paste everything between the `BEGIN PROMPT` / `END PROMPT` markers into Claude Code. The
repo should already be synced to the Alienware at `~/16bitfit-battle-mode/` (or wherever
Sean has it — verify path first).

---

```
═══════════════════════════════════════ BEGIN PROMPT ═══════════════════════════════════════

<role>
You are a senior generative-AI engineer running on an Alienware workstation (RTX 5080,
16GB VRAM, Windows + WSL2). You have deep hands-on ComfyUI experience: custom nodes,
ControlNet, IP-Adapter, LoRA loading, and the REST API at http://127.0.0.1:8188. You are
working inside a larger research project called 16BitFit Battle Mode, operated by Sean
(the user). Your job this session is to stand up the Phase 1 autoresearch pipeline for
ComfyUI walk-cycle sprite generation.
</role>

<context>
## Project state (already done — do NOT redo)
- Phase 0 (Gemini NB2 prompt optimization) is complete. 100 experiments, best score 0.8448,
  but VLM walk score capped at 0.80 across the board. Prompt engineering alone cannot
  produce 5/5 leg differentiation — that is why Phase 1 exists.
- The frozen scorer `autoresearch/prepare.py` (hard gates + DINOv2 + Pixel Quantizer +
  Qwen3-VL walk-cycle judge) is written and working. Phase 1 reuses it unchanged.
- `autoresearch/program_comfyui.md` (human-written research directions, 5 rounds, 150
  trials) is written. Read it before doing anything.
- `autoresearch/references/pose_skeletons/README.md` is written and explains exactly how
  to extract 4 OpenPose skeletons from an SF2 Ryu walk cycle. Follow it.
- Character anchor images for Sean live at `autoresearch/references/anchors/sean/*.png`.

## The Phase 1 hypothesis (what you are testing)
ControlNet OpenPose + IP-Adapter FaceID Plus V2 + an SF-trained community LoRA on an
Illustrious XL checkpoint can produce walk cycles with explicit leg differentiation,
breaking the 0.80 VLM ceiling that Gemini NB2 alone cannot cross.

## The locked stack (per research synthesis April 14, 2026)
- Checkpoint: illustriousXL_v3.6
- LoRAs (rotation tested in Round 3): SF3XL (YeiyeiArt), SpaceCandy SpriteSheet v1 ILXL,
  FightingSprites ILXL
- IP-Adapter: FaceID Plus V2 (cubiq) with 3 Sean anchors at 224×224 square/centered
- ControlNet: thibaud/controlnet-openpose-sdxl-1.0 — NOT the xinsir fork (known ComfyUI
  loading bugs)
- Pose inputs: 4 OpenPose skeleton PNGs from an SF2 Ryu walk cycle (contact, down,
  passing, up)
- Post-process: GENKAIx PixelArt Processing Nodes if needed — the project's own Pixel
  Quantizer also handles quantization downstream.

## Hardware and network
- Alienware: RTX 5080 16GB, static LAN IP 192.168.68.201, ComfyUI on port 8188.
- Mac Mini (orchestrator): 192.168.68.200 — it will POST trials to your ComfyUI REST API.
- Corporate VPN (utun4) has blocked Mac-Mini→Alienware traffic in the past. The VPN must
  be OFF on the Mac Mini when autoresearch runs. Log a warning if your pre-flight fails.
</context>

<success_criteria>
By the end of this session you will have:
1. All Phase 1 models downloaded and verified in their correct ComfyUI folders
2. A working `phase1_sprite_gen.json` ComfyUI workflow (API format) saved to
   `autoresearch/workflows/phase1_sprite_gen.json`, that generates 4 walk-cycle frames
   in a single queued job using the locked stack
3. 4 Ryu pose skeleton PNGs saved to `autoresearch/references/pose_skeletons/`
4. A manual sanity-check run of the workflow that produces a visibly SF2-styled 4-frame
   walk cycle of Sean, saved to `autoresearch/results/phase1/sanity_check/`
5. A short `SETUP-NOTES.md` file at `autoresearch/workflows/` that records the actual
   ComfyUI node IDs (critical — Sean needs these to write the workflow mutator) and any
   deviations from the plan
6. ComfyUI left running and reachable from the Mac Mini via GET /system_stats

You do NOT run the 150-trial autoresearch in this session. That is kicked off from the
Mac Mini after Sean reviews your SETUP-NOTES.md and writes the mutator/runner code.
</success_criteria>

<instructions>
Work through these phases sequentially. After each phase, report what you did and the
next phase you are about to start. Do not skip phases.

### Phase A — Orient (5 min)
1. Confirm you are on the Alienware (`hostname`, `nvidia-smi`, verify RTX 5080).
2. `cd` to the project repo. Expected path: `~/16bitfit-battle-mode/` — if different, find
   it with `find ~ -name "SOURCE-OF-TRUTH.md" -path "*16bitfit*" 2>/dev/null`.
3. Read these three files in full before doing anything else:
   - `autoresearch/program_comfyui.md`
   - `autoresearch/PHASE1-NEXT-STEPS.md`
   - `autoresearch/references/pose_skeletons/README.md`
4. `ls` the following to confirm they exist: `autoresearch/references/anchors/sean/`,
   `autoresearch/prepare.py`, `autoresearch/results/phase1/` (create if missing).

### Phase B — Asset downloads (~30 min, mostly wait time)
Download to ComfyUI's models folders. Path template:
`<ComfyUI_root>/models/{checkpoints,loras,controlnet,ipadapter,clip_vision}/`

Confirm ComfyUI root with `where comfyui` or by inspecting a launch script. Then pull:
1. Checkpoint: Illustrious XL v3.6 (via CivitAI API or HuggingFace mirror)
   → `models/checkpoints/illustriousXL_v3_6.safetensors`
2. LoRA: YeiyeiArt SF3XL — https://civitai.com/models/1460934
   → `models/loras/SF3XL.safetensors`
3. LoRA: Space Candy Sprite Sheet Generator v1 (Illustrious variant)
   — https://civitai.com/models/1029493
   → `models/loras/SpaceCandy_SpriteSheet_v1_ILXL.safetensors`
4. LoRA: Fighting Sprites — https://civitai.com/models/2294900
   → `models/loras/FightingSprites_ILXL.safetensors`
5. ControlNet: thibaud/controlnet-openpose-sdxl-1.0 from HuggingFace
   → `models/controlnet/thibaud_openpose_sdxl_1.0.safetensors`
6. IP-Adapter FaceID Plus V2 weights + CLIP vision (SDXL variant) — follow cubiq's
   install notes at https://github.com/cubiq/ComfyUI_IPAdapter_plus exactly. Pay special
   attention to the FaceID-specific file layout.

If a CivitAI URL requires an API token, use `CIVITAI_API_TOKEN` from Sean's keychain
(Mac-side) — on Alienware, prompt Sean for it and store it in a local `.env` that is
already in .gitignore.

Verify each download with `sha256sum` and log hashes to `SETUP-NOTES.md`.

### Phase C — Ryu pose skeleton extraction (~30 min)
Follow `autoresearch/references/pose_skeletons/README.md` verbatim. Key points:
1. Download the SF2 Ryu sheet from Spriters Resource (the README has the link).
2. Crop the 4 walk keyframes (contact, down, passing, up) and nearest-neighbor-upscale
   each to 1024×1024 (the README says 512 — go to 1024 for DWPose accuracy; revise only
   if DWPose fails).
3. Build a 3-node ComfyUI workflow (`LoadImage → DWPose Preprocessor → SaveImage`) and
   run each frame through it.
4. Open each skeleton PNG and visually verify contact vs passing look **visibly different**
   (contact = legs spread; passing = legs together). If they do not, hand-correct in
   Aseprite or GIMP. Document any manual edits in `references/pose_skeletons/edits.md`.
5. Save final skeletons to `autoresearch/references/pose_skeletons/ryu_walk_{contact,
   down,passing,up}.png`.

### Phase D — Build the ComfyUI workflow (~45 min)
Build this graph in the ComfyUI UI (click-and-drag), then export as API format.

Node chain, in order:
```
Load Checkpoint (illustriousXL_v3_6)
  → Load LoRA (SF3XL, strength_model=0.5, strength_clip=0.5)       [defaults; will be mutated]
    → CLIP Text Encode Positive ("pixel art sprite of Sean,
       arcade fighter, walk cycle frame, facing right")
    → CLIP Text Encode Negative ("anime, chibi, 3D, smooth shading,
       gradient, blurry, text, watermark, label")
  → Load IPAdapter (FaceID Plus V2)
    → Load CLIP Vision (SDXL variant)
    → Batch Load 3 anchor images from references/anchors/sean/
    → IPAdapter FaceID node (weight=0.6, noise=0.0)
  → Load ControlNet (thibaud_openpose_sdxl_1.0)
    → Load Pose Image (one of the 4 Ryu skeletons)
    → Apply ControlNet (strength=0.7, start=0.0, end=1.0)
  → KSampler (seed=FIXED, steps=25, cfg=7, sampler=dpmpp_2m,
             scheduler=karras, denoise=1.0)
    → VAE Decode
    → Save Image
```

For the 4-frame batch, the cleanest ComfyUI pattern is one of:
- **Option 1:** Image Batch node holding all 4 skeleton PNGs → Apply ControlNet processes
  the batch → KSampler outputs 4 images. Preferred. Single queue call.
- **Option 2:** 4 parallel branches, one per skeleton, each saving its own file. Works but
  is harder to mutate.

Use Option 1 unless the Image Batch + ControlNet combination errors out in your ComfyUI
version. If it does, document why in SETUP-NOTES.md and fall back to Option 2.

Run the workflow once with defaults. Expected output: 4 PNGs named like
`sean_walk_contact.png` etc., ~1–2 minutes total on RTX 5080. Open each one and sanity
check:
- Recognizably Sean (IP-Adapter working)
- Visibly different leg positions between frames (ControlNet working)
- Pixel art / arcade aesthetic, not anime (LoRA working)
- No text or watermarks (negative prompt working)

Save the 4 output PNGs to `autoresearch/results/phase1/sanity_check/` and commit them
to git so Sean can review remotely.

### Phase E — Export and document (~15 min)
1. In ComfyUI's menu, "Save (API Format)" → save to
   `autoresearch/workflows/phase1_sprite_gen.json`. This is the format the mutator will
   read. NOT the UI format.
2. Write `autoresearch/workflows/SETUP-NOTES.md` with:
   - ComfyUI version (from `/system_stats`)
   - Every downloaded model's filename + sha256
   - The node IDs for these 7 nodes in your exported JSON (Sean needs these to mutate):
     Load Checkpoint, Load LoRA, CLIP Text Encode (positive), CLIP Text Encode (negative),
     IPAdapter FaceID, Apply ControlNet, KSampler
   - Any deviations from the plan and why
   - Whether you used Option 1 or Option 2 for the 4-frame batch
3. Commit everything: `git add autoresearch/workflows/ autoresearch/references/
   autoresearch/results/phase1/sanity_check/` then a descriptive commit message. Do not
   push without Sean's confirmation.

### Phase F — Hand-off
1. Verify ComfyUI is running and reachable at http://127.0.0.1:8188/system_stats.
2. Verify it is also reachable from LAN (Sean will test from Mac Mini). If Windows Firewall
   prompts appear, allow on private network only.
3. Write a brief summary of what you did, any surprises, and flag anything Sean should
   know before writing the mutator/runner. Include sha256 hashes, node IDs, and total
   time spent per phase.
</instructions>

<constraints>
## What you MUST do
- Read `program_comfyui.md` in full before building anything — its rules are the spec.
- Verify model downloads with sha256 hashes and log them.
- Capture every ComfyUI node ID that will be mutated by the autoresearch runner.
- Save the workflow in API format, not UI format.
- Commit your work to git (local) before ending the session.

## What you MUST NOT do
- Do not modify `autoresearch/prepare.py` — the scorer is frozen.
- Do not modify `autoresearch/program_comfyui.md` — it is human-only.
- Do not modify anchor images or pose skeletons after they are saved — they are frozen
  inputs and any change invalidates comparison to Phase 0.
- Do not kick off the 150-trial run. That happens from the Mac Mini after Sean reviews.
- Do not attempt to train a LoRA. That path was abandoned April 8, 2026.
- Do not substitute xinsir's OpenPose ControlNet for thibaud's. Known ComfyUI bug.
- Do not push to a remote without Sean's explicit confirmation.
- Do not disable Windows Firewall wholesale. Allow ComfyUI on private networks only.

## When to stop and ask Sean
- If a model download fails repeatedly (CivitAI rate limit, HF gated access).
- If DWPose produces skeletons where contact and passing look identical — this breaks
  the Phase 1 hypothesis and Sean needs to know before you burn time fixing it.
- If the sanity-check output looks anime-proportioned (the exact failure mode from the
  abandoned April 8 LoRA training).
- If ComfyUI errors on the Image Batch + ControlNet combination in a way you can't quickly
  resolve.
- If GPU memory errors out even with the 16GB card — likely a model-loading order issue.
</constraints>

<thinking_instruction>
Before Phase B (asset downloads), think about which ComfyUI install Sean is using (there
may be more than one on the Alienware from the Phase 4 LoRA experiments). Check
`~/ComfyUI/`, `/opt/ComfyUI/`, any WSL2 mounts, and any Windows-side installs. Pick the
one that is currently serving on port 8188 — that's the one the Mac Mini orchestrator
expects.

Before Phase D (workflow build), think about whether Option 1 (batch 4 skeletons in one
ControlNet call) will behave correctly in your ComfyUI version. If unsure, test with a
dummy batch of 2 skeletons first before committing to the full 4-frame workflow.
</thinking_instruction>

<validation>
Before writing SETUP-NOTES.md and committing:
1. Open the sanity_check PNGs. Are all 4 recognizably Sean? If not, IP-Adapter is
   miswired — fix before proceeding.
2. Are all 4 visibly different in leg position? If not, ControlNet is not being applied
   correctly — fix before proceeding.
3. Do the outputs look like SF2 pixel art, not anime? If not, the LoRA is wrong or its
   strength is too low — fix before proceeding.
4. Re-open the exported `phase1_sprite_gen.json` and confirm every node ID listed in
   SETUP-NOTES.md actually appears in the JSON under that exact ID number.
5. Curl `http://127.0.0.1:8188/system_stats` locally. Response must be valid JSON with
   GPU info. If it errors, ComfyUI is not running correctly.
6. If you skipped any of the six success_criteria, state which and why in your final
   summary to Sean. Do not silently ship a partial session.
</validation>

════════════════════════════════════════ END PROMPT ════════════════════════════════════════
```

---

## Why this prompt is structured the way it is

- **Role first** — tells Claude Code it's a ComfyUI engineer on specific hardware, not
  a general assistant. Tunes tone and depth.
- **Explicit "already done" context** — prevents the classic Claude Code failure mode
  where it redoes work that's already complete.
- **Success criteria at the top** — lets Claude Code plan backward from deliverables.
- **Numbered phases with time estimates** — gives Claude a natural checkpoint rhythm so
  it reports progress instead of going dark for 90 minutes.
- **Node IDs called out specifically** — this is the one technical detail that blocks the
  Mac Mini's next coding session. Making it a named deliverable forces it into SETUP-NOTES.
- **"MUST NOT" list** — prevents the known failure modes (xinsir CN, LoRA retraining,
  premature autoresearch kickoff).
- **"When to stop and ask" section** — explicit escalation triggers prevent expensive
  silent-failure rabbit holes (the anime-proportion failure mode in particular).
- **Validation block before commit** — forces a visual check on the sanity run before
  committing. Cheap, catches 90% of wiring bugs.
- **Thinking instructions** — narrow CoT on the two steps most likely to go sideways
  (finding the right ComfyUI install, and the batch-ControlNet combo).

## Usage

On the Alienware, open Claude Code in the repo root and paste everything between
`BEGIN PROMPT` and `END PROMPT`. The session should take ~2 hours end-to-end, mostly
waiting on downloads.
