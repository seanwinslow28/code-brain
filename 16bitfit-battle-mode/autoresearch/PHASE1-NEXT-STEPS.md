# Phase 1 — Next Steps Checklist

Research synthesized, plan locked. What's done and what you actually need to do next.

## ✅ Done in this session
- `program_comfyui.md` — the human-written research directions (5 rounds, 150 trials)
- `references/pose_skeletons/README.md` — full extraction guide for SF2 Ryu walk cycle

## 🟡 Needs doing ON THE ALIENWARE (not in this sandbox)

These require ComfyUI + GPU, so they can't be scripted from here. Rough time estimates:

1. **Extract Ryu pose skeletons** (~30 min)
   Follow `references/pose_skeletons/README.md` steps 1–5. Outputs 4 skeleton PNGs.

2. **Download community assets** (~20 min, mostly wait time)
   - Illustrious XL v3.6 checkpoint → `ComfyUI/models/checkpoints/`
   - YeiyeiArt SF3XL LoRA → `ComfyUI/models/loras/` — https://civitai.com/models/1460934
   - Space Candy Sprite Sheet Gen v1 (ILXL) → `ComfyUI/models/loras/` — https://civitai.com/models/1029493
   - Fighting Sprites LoRA → `ComfyUI/models/loras/` — https://civitai.com/models/2294900
   - thibaud OpenPose SDXL ControlNet → `ComfyUI/models/controlnet/` — https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0
   - IP-Adapter FaceID Plus V2 (SDXL) + CLIP vision → follow cubiq's install notes — https://github.com/cubiq/ComfyUI_IPAdapter_plus

3. **Build the base workflow by hand in ComfyUI UI** (~45 min)
   Construct the node graph described in `program_comfyui.md` § "Base Stack". Queue a test
   run with all defaults to verify it outputs a clean sprite. Save as
   `autoresearch/workflows/phase1_sprite_gen.json` via "Save (API Format)" — we need the
   API JSON, not the UI JSON.

## 🔵 What I can build next in this sandbox (after assets are on Alienware)

4. **`search_space.py` extension** — add `PHASE1_PARAMS` + helper `suggest_phase1(trial)`.
5. **`workflow_mutator.py` extension** — add `mutate_phase1_sprite_gen(workflow, params)`
   that targets the actual node IDs from your exported `phase1_sprite_gen.json`.
6. **`runner.py` `--phase 1` branch** — POST to `/prompt`, poll `/history/{id}`, fetch
   output, call frozen `prepare.py` scorer. Pre-flight `/system_stats` health check + VPN
   guard.
7. **Dry-run mode** — stub ComfyUI calls, mock scores, verify mutate→queue→poll→score→
   revert/keep loop end-to-end.

The reason I need the exported `phase1_sprite_gen.json` before writing 5 and 6: the
mutator has to reference actual node IDs (e.g. `"6.inputs.strength_model": 0.5` where `6`
is whatever node number ComfyUI assigns to your Load LoRA node). We can't guess those —
they're assigned when you build the graph.

## Suggested sequence

```
Today's remaining work (on Alienware, ~2 hours):
  1. Download assets
  2. Build + test the base workflow in ComfyUI UI
  3. Export the API JSON and drop it at autoresearch/workflows/phase1_sprite_gen.json
  4. Extract Ryu pose skeletons

Next session (back here in Cowork, ~1 hour for me to write):
  5. I write search_space extension, workflow_mutator extension, runner --phase 1 branch
  6. Dry run 5 trials
  7. Kick off real 150-trial run overnight

Tomorrow morning:
  8. Review results, compare to Phase 0's 0.8448 best, decide production path
```

## If you get stuck on the Alienware step

Two likely pain points based on the research:

- **IP-Adapter install is finicky.** cubiq's repo needs the ControlNet models, CLIP vision,
  AND the IP-Adapter weights all in specific folders. If the node errors on load, check
  his README section "Installation" word-for-word.
- **SDXL OpenPose ControlNet has TWO popular variants** — use the thibaud one, not xinsir.
  The xinsir version has a known ComfyUI loading bug per community reports.

Ping me back here when the base workflow is running and I'll write the mutation code.
