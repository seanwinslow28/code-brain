# Phase 1 Setup Notes

Session date: 2026-04-16. Setup agent: Claude Opus 4.6.

## ComfyUI Instance

| Property | Value |
|---|---|
| Version | 0.3.52 |
| Python | 3.13.12 (MSC v.1944 64-bit) |
| PyTorch | 2.11.0+cu128 |
| GPU | NVIDIA GeForce RTX 5080 (16 GB VRAM) |
| Root | `C:\Users\seanw\Documents\Code-Brain\ComfyUI\` |
| Launch command | `venv/Scripts/python.exe main.py --listen 0.0.0.0 --port 8188` |
| Health check | `GET http://127.0.0.1:8188/system_stats` |

**CRITICAL: Do NOT use `--force-fp16`.** It causes LoRA application to produce pure
noise at any strength above ~0.15. This was the root cause of hours of debugging.
The launch scripts may still have this flag — remove it before running autoresearch.

## Workflow Node IDs (for the mutator)

These are the node IDs in `phase1_sprite_gen.json` that the autoresearch mutator needs
to target. Each ID corresponds to a specific node in the workflow:

| Node ID | Class Type | Mutable Parameters |
|---|---|---|
| **1** | `CheckpointLoaderSimple` | `ckpt_name` |
| **2** | `LoraLoader` | `lora_name`, `strength_model`, `strength_clip` |
| **3** | `CLIPTextEncode` (positive) | `text` |
| **4** | `CLIPTextEncode` (negative) | `text` |
| **5** | `IPAdapterUnifiedLoaderFaceID` | `lora_strength`, `preset` |
| **7** | `IPAdapterFaceID` | `weight`, `weight_faceidv2`, `weight_type`, `embeds_scaling` |
| **9** | `LoadImage` (pose skeleton) | `image` (filename) |
| **10** | `ControlNetApplyAdvanced` | `strength`, `start_percent`, `end_percent` |
| **12** | `KSampler` | `seed`, `steps`, `cfg`, `sampler_name`, `scheduler`, `denoise` |

### Mutator quick reference

```python
# Example: mutate LoRA strength
workflow["2"]["inputs"]["strength_model"] = 0.4
workflow["2"]["inputs"]["strength_clip"] = 0.4

# Example: swap LoRA
workflow["2"]["inputs"]["lora_name"] = "FightingSprites_ILXL.safetensors"

# Example: change pose
workflow["9"]["inputs"]["image"] = "ryu_walk_passing.png"

# Example: change ControlNet strength
workflow["10"]["inputs"]["strength"] = 0.5
workflow["10"]["inputs"]["end_percent"] = 0.6

# Example: change seed
workflow["12"]["inputs"]["seed"] = 12345
```

## Model Hashes (sha256)

| Model | sha256 |
|---|---|
| thibaud_openpose_sdxl_1.0.safetensors | `5a4b928cb1e93748217900cb66d4135bf70d932d2924232f925910fad9e43a92` |
| ip-adapter-faceid-plusv2_sdxl.bin | `c6945d82b543700cc3ccbb98d363b837e9c596281607857c74b713a876daf5fb` |
| ip-adapter-faceid-plusv2_sdxl_lora.safetensors | `f24b4bb2dad6638a09c00f151cde84991baf374409385bcbab53c1871a30cb7b` |
| SF3XL.safetensors | `50b7007fc8c64bc15e213fcf383e8fe567a7ff123ac39fad624dee2512b5aa41` |
| SpaceCandy_SpriteSheet_v1_ILXL.safetensors | `9faee2cca52dd6225c3185d1a13bf7fd2b7522429d9136f8e78c810a85bca568` |
| FightingSprites_ILXL.safetensors | `cf3ab17b6fcc49b508040908072a3a4b4525b6c79c565a202fab42b686b21f3f` |

## Deviations from the Original Plan

### 1. Checkpoint: Using v2.0 instead of v3.6
The plan specified `illustriousXL_v3.6`. This model does not exist as a downloadable
checkpoint on CivitAI or HuggingFace. The official Illustrious XL CivitAI page (model
795765) only has v0.1. Versions 3.x appear to be **API-only** via the Illustrious custom
ComfyUI node (see "Illustrious API" section below). Using `Illustrious-XL-v2.0.safetensors`
which was already on disk and is compatible with all three LoRAs.

### 2. SF3XL LoRA: Incompatible with Illustrious XL v2.0
**SF3XL produces pure noise at any strength above ~0.15** on this checkpoint. Tested at
0.1 (works), 0.3 (noise), 0.5 (noise) — both with and without `--force-fp16`. The LoRA
has proper SDXL keys (2958 keys, has `te2`), so it's not a format mismatch. It may be
trained for a different Illustrious XL version or a NoobAI/NAI base.

**SpaceCandy works well at 0.5** — produces recognizable sprite sheets. FightingSprites
partially works (scattered characters). **The default workflow uses SpaceCandy.**

### 3. ControlNet: Must use early-stop (`end_percent ≤ 0.5`)
With `end_percent=1.0` or `0.8`, the ControlNet renders the skeleton overlay literally
on top of the output image. With `end_percent=0.5`, it provides pose guidance in early
sampling steps and the later steps clean up. The default workflow uses `strength=0.4`,
`end_percent=0.5`. The autoresearch should sweep `end_percent` in range [0.3, 0.7].

### 4. Pose skeletons: Hand-drawn (not DWPose)
DWPose and OpenPose preprocessors both completely failed on pixel art sprites — even
after bilinear upscaling, background removal, and Gaussian blur. The YOLO person
detector cannot identify a human figure in upscaled pixel art. Skeletons were drawn
programmatically using PIL with standard OpenPose COCO colors. See
`references/pose_skeletons/edits.md` for full details.

### 5. Batch mode: Using Option 2 (sequential single-frame)
The current workflow processes one skeleton at a time. To generate all 4 frames, submit
the workflow 4 times with different `image` values in node 9. This is simpler for the
mutator to handle than batch mode. If batch mode is needed later, use `ImageBatch` nodes
to combine 4 skeletons and set `EmptyLatentImage` batch_size to 4.

### 6. Launch flags: No --force-fp16
ComfyUI was previously running with `--force-fp16`. This causes LoRA application to
overflow and produce noise. **Removed this flag.** Auto-precision selection works correctly.

## Illustrious API (new option from Sean)

Sean provided an Illustrious API key (`ILLUSTRIOUS_API_KEY` in `agents-sdk/.env`).
The [Illustrious custom ComfyUI node](https://www.illustrious-xl.ai/docs/comfy-custom-node)
provides API-based generation with models up to v3.5. Nodes:
- **ILXL Generator** — remote generation with resolution up to 2048x2048
- **TagBooster** — prompt expansion
- **MoodEnhancer** — atmospheric descriptions

This is an alternative path if local generation quality is insufficient. Trade-offs:
- Pro: Access to newer model versions (v3.5), no VRAM constraints
- Con: Requires internet, has API cost, adds latency, can't be used with local ControlNet/FaceID

Not integrated into the current workflow. Evaluate after Round 2 if local results are
below the 0.8448 Phase 0 benchmark.

## ERNIE-Image-Turbo (evaluated, not viable)

Sean asked about [ERNIE-Image-Turbo](https://huggingface.co/baidu/ERNIE-Image-Turbo)
from Baidu. Findings:
- **Not SDXL-based** — uses DiT (Diffusion Transformer) architecture
- **Requires 24GB VRAM** — our RTX 5080 only has 16GB
- **No ComfyUI integration** — diffusers-only
- **Our LoRAs won't work** — different architecture
- Strong at text rendering and structured layouts, but not a drop-in replacement

## Character Anchors

Path correction: Sean's anchors are at `references/anchors/champions/Sean/` (not
`references/anchors/sean/` as originally specified). The workflow loads from ComfyUI's
input directory — anchors were copied there as `sean_anchor_{1,2,3}.png`.

## Sanity Check Results

4 frames generated with defaults (SpaceCandy 0.5, CN 0.4 end 0.5, FaceID 0.6, seed 42):
- `results/phase1/sanity_check/sean_walk_{contact,down,passing,up}.png`
- Style: pixel-art sprite sheet (multiple small characters per frame)
- Quality: Baseline — the autoresearch will optimize from here
- Key issue: SpaceCandy generates sprite sheets, not single characters. The prompt or
  LoRA strength needs tuning to produce single large characters instead.

## Files Created This Session

```
autoresearch/workflows/
├── phase1_sprite_gen.json   ← API-format workflow (15 nodes)
├── SETUP-NOTES.md           ← This file
└── MODEL-INVENTORY.md       ← Full model inventory with hashes

autoresearch/references/pose_skeletons/
├── ryu_walk_contact.png     ← OpenPose skeleton (hand-drawn)
├── ryu_walk_down.png
├── ryu_walk_passing.png
├── ryu_walk_up.png
├── edits.md                 ← Documents why skeletons were hand-drawn
└── source/                  ← Ryu sprite sheet + extraction artifacts

autoresearch/results/phase1/sanity_check/
├── sean_walk_contact.png    ← Sanity check outputs
├── sean_walk_down.png
├── sean_walk_passing.png
└── sean_walk_up.png
```
