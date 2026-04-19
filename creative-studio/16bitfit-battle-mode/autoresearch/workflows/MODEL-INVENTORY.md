# Phase 1 Model Inventory

Last updated: 2026-04-15 by Claude (Phase 1 setup session).

This document records every model, custom node, and Python dependency required by the
Phase 1 ComfyUI walk-cycle sprite generation pipeline. Future agents: read this before
attempting to run or modify the workflow.

## ComfyUI Instance

| Property | Value |
|---|---|
| Root path | `C:\Users\seanw\Documents\Code-Brain\ComfyUI\` |
| Version | 0.3.52 |
| Python | 3.13.12 (MSC v.1944 64-bit) |
| PyTorch | 2.11.0+cu128 |
| GPU | NVIDIA GeForce RTX 5080 (16 GB VRAM) |
| Listen address | `0.0.0.0:8188` (LAN-accessible) |
| Launch flags | `--listen 0.0.0.0 --port 8188 --force-fp16` |
| Health check | `GET http://127.0.0.1:8188/system_stats` |

## Downloaded Models (verified)

All paths relative to `ComfyUI/models/`.

### Checkpoint

| File | Path | Size | sha256 | Source | Status |
|---|---|---|---|---|---|
| Illustrious-XL-v2.0.safetensors | `checkpoints/` | ~6.5 GB | (pre-existing, not hashed this session) | CivitAI | **AVAILABLE** — was already on disk |
| illustriousXL_v3_6.safetensors | `checkpoints/` | ~7 GB (est.) | — | CivitAI (unknown model page) | **MISSING** — see note below |

**Checkpoint note:** The research plan (`program_comfyui.md`) specifies `illustriousXL_v3.6`.
We searched CivitAI model 795765 (the official Illustrious-XL page) — it only hosts v0.1.
HuggingFace mirrors (OnomaAIResearch, John6666) have v0.1 and various community merges but
no file named `illustriousXL_v3_6.safetensors`. The v2.0 checkpoint already on disk is
compatible with all three LoRAs (they target the Illustrious XL family). **Using v2.0 as
the working checkpoint until Sean locates v3.6.** If v3.6 is found later, drop it into
`checkpoints/` and update the workflow's Load Checkpoint node — no other changes needed.

### LoRAs (style)

| File | Path | Size | sha256 | Source | CivitAI model/version |
|---|---|---|---|---|---|
| SF3XL.safetensors | `loras/` | 110 MB | `50b7007fc8c64bc15e213fcf383e8fe567a7ff123ac39fad624dee2512b5aa41` | CivitAI | 1460934 / 1652109 |
| SpaceCandy_SpriteSheet_v1_ILXL.safetensors | `loras/` | 218 MB | `9faee2cca52dd6225c3185d1a13bf7fd2b7522429d9136f8e78c810a85bca568` | CivitAI | 1029493 / 1154679 |
| FightingSprites_ILXL.safetensors | `loras/` | 218 MB | `cf3ab17b6fcc49b508040908072a3a4b4525b6c79c565a202fab42b686b21f3f` | CivitAI | 2294900 / 2588501 ("Punching and Kicking" variant) |

**LoRA note:** SF3XL's actual filename on CivitAI is `ASF3_style-12.safetensors` — we
renamed it to `SF3XL.safetensors` for consistency with the research plan. SpaceCandy's
original name was `Sprite_sheet_generator_2-_Space_Candy_Media.safetensors`. FightingSprites'
original was `Fighting_Sprites.safetensors`. The FightingSprites model has three version
variants (Idle, Punching+Kicking, Kicking Only) — we downloaded "Punching and Kicking"
(version ID 2588501) as the most general fighting-pose variant.

### LoRAs (IP-Adapter FaceID)

| File | Path | Size | sha256 | Source |
|---|---|---|---|---|
| ip-adapter-faceid-plusv2_sdxl_lora.safetensors | `loras/` | 355 MB | `f24b4bb2dad6638a09c00f151cde84991baf374409385bcbab53c1871a30cb7b` | HuggingFace h94/IP-Adapter-FaceID |

**This LoRA is required by the FaceID Plus V2 model** — it is NOT a style LoRA. It must
be loaded alongside the IP-Adapter FaceID model. cubiq's Unified Loader FaceID handles
this automatically if the file naming convention is followed (which it is).

### ControlNet

| File | Path | Size | sha256 | Source |
|---|---|---|---|---|
| thibaud_openpose_sdxl_1.0.safetensors | `controlnet/` | 4.7 GB | `5a4b928cb1e93748217900cb66d4135bf70d932d2924232f925910fad9e43a92` | HuggingFace thibaud/controlnet-openpose-sdxl-1.0 |

**ControlNet note:** The downloaded file is `OpenPoseXL2.safetensors` from thibaud's repo,
renamed to match the research plan's naming. Do NOT substitute with xinsir's fork — it has
known ComfyUI loading bugs per community reports and the research plan explicitly forbids it.

### IP-Adapter

| File | Path | Size | sha256 | Source |
|---|---|---|---|---|
| ip-adapter-faceid-plusv2_sdxl.bin | `ipadapter/` | 1.4 GB | `c6945d82b543700cc3ccbb98d363b837e9c596281607857c74b713a876daf5fb` | HuggingFace h94/IP-Adapter-FaceID |

### CLIP Vision

| File | Path | Size | sha256 | Notes |
|---|---|---|---|---|
| CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors | `clip_vision/` | 2.4 GB | (pre-existing, renamed from `model.safetensors`) | Required by cubiq's Unified Loader |

**CLIP note:** The original `model.safetensors` (2.4 GB) was copied (not moved) to the
canonical name expected by cubiq's IPAdapter Plus unified loader. The 2.4 GB size matches
CLIP-ViT-H-14 (the SD1.5 / general variant). For standard SDXL IP-Adapter models, the
bigG encoder (`CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors`, ~3.5 GB) would be needed,
but FaceID Plus V2 uses InsightFace embeddings for the face component and ViT-H for the
"plus" component, so this file should suffice. If the workflow errors on CLIP mismatch,
download bigG from `https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/image_encoder/model.safetensors`.

## Pre-existing Models (not part of Phase 1 but present on disk)

These were already in the ComfyUI models directory from prior work. Listed for completeness.

| File | Path | Notes |
|---|---|---|
| Illustrious-XL-v2.0.safetensors | `checkpoints/` | Phase 0 / LoRA training checkpoint |
| control_v11p_sd15_openpose_fp16.safetensors | `controlnet/` | SD1.5 OpenPose (not SDXL) |
| diffusers_xl_canny_full.safetensors | `controlnet/` | XL Canny ControlNet |
| ip-adapter-plus-face_sd15.safetensors | `ipadapter/` | SD1.5 face adapter |
| ip-adapter_sdxl.safetensors | `ipadapter/` | Generic SDXL adapter (not FaceID) |
| 16bitfit_sprite_style*.safetensors | `loras/` | Abandoned April 8 custom LoRA attempts |
| pixel-art-xl.safetensors | `loras/` | Generic pixel art LoRA |

## Custom Nodes Installed

| Node | Path | Purpose | Installed this session? |
|---|---|---|---|
| ComfyUI_IPAdapter_plus (cubiq) | `custom_nodes/ComfyUI_IPAdapter_plus/` | FaceID Plus V2, Unified Loader | **Yes** — cloned from GitHub |
| comfyui_controlnet_aux | `custom_nodes/comfyui_controlnet_aux/` | DWPose preprocessor (for skeleton extraction) | No — pre-existing |
| ComfyUI-Advanced-ControlNet | `custom_nodes/ComfyUI-Advanced-ControlNet/` | Advanced ControlNet application | No — pre-existing |
| ComfyUI-OpenPose-Editor | `custom_nodes/ComfyUI-OpenPose-Editor/` | Visual pose editing | No — pre-existing |
| ComfyUI-Manager | `custom_nodes/ComfyUI-Manager/` | Node manager UI | No — pre-existing |
| ComfyUI-Frame-Interpolation | `custom_nodes/ComfyUI-Frame-Interpolation/` | Frame interp (not used in Phase 1) | No — pre-existing |
| ComfyUI-Inspyrenet-Rembg | `custom_nodes/ComfyUI-Inspyrenet-Rembg/` | Background removal | No — pre-existing |
| ComfyUI-VideoHelperSuite | `custom_nodes/ComfyUI-VideoHelperSuite/` | Video utilities | No — pre-existing |

## Python Dependencies Installed This Session

| Package | Version | Purpose |
|---|---|---|
| insightface | 0.7.3 | Face detection/embedding for FaceID IP-Adapter |
| onnxruntime | 1.24.4 | InsightFace inference backend |

Other transitive dependencies installed: contourpy, cycler, cython, flatbuffers, fonttools,
imageio, joblib, kiwisolver, lazy-loader, matplotlib, ml_dtypes, onnx, prettytable,
protobuf, pyparsing, scikit-image, scikit-learn, threadpoolctl, tifffile, wcwidth.

## InsightFace Model

The `buffalo_l` face analysis model is required by cubiq's FaceID loader. It was NOT
pre-downloaded — InsightFace will auto-download it on first use to
`ComfyUI/models/insightface/models/buffalo_l/`. The directory structure exists but is
empty. If auto-download fails (firewall, etc.), manually download from:
https://github.com/deepinsight/insightface/releases and extract to that path.

## Character Anchors

Sean's 3 anchor images for IP-Adapter FaceID are at:
```
16bitfit-battle-mode/autoresearch/references/anchors/champions/Sean/
  champion_sean_anchor-1.png
  champion_sean_anchor-2.png
  champion_sean_anchor-3.png
```

**Path correction:** The original instructions referenced `references/anchors/sean/` but
the actual path is `references/anchors/champions/Sean/`. Workflows and scripts must use
the correct path.

## Pose Skeletons

Status: **NOT YET EXTRACTED** (Phase C work). Target location:
```
autoresearch/references/pose_skeletons/
  ryu_walk_contact.png
  ryu_walk_down.png
  ryu_walk_passing.png
  ryu_walk_up.png
```

Follow `references/pose_skeletons/README.md` for extraction steps.

## API Tokens

| Token | Location | Used for |
|---|---|---|
| HUGGINGFACE_TOKEN | `ComfyUI/.env` | HuggingFace model downloads |
| CIVIT_AI_API_KEY | `agents-sdk/.env` | CivitAI model downloads |
| GITHUB_TOKEN | `ComfyUI/.env` | GitHub API access |

**Security:** Both `.env` files are gitignored. Never commit or log token values.

## Known Issues and Deviations

1. **Checkpoint mismatch:** Plan says `illustriousXL_v3.6`, using `Illustrious-XL-v2.0`
   until v3.6 is located. Functional impact: likely minimal — both are Illustrious XL
   family, LoRAs are compatible. If v3.6 is found, swap the checkpoint file and update
   the Load Checkpoint node filename in the workflow JSON.

2. **InsightFace buffalo_l not pre-downloaded:** Will auto-download on first FaceID node
   execution. First run may take an extra 1-2 minutes. If ComfyUI has no internet access,
   this will fail silently — pre-download manually in that case.

3. **CLIP Vision model uncertainty:** The 2.4 GB file is likely ViT-H (SD1.5 scale). If
   FaceID Plus V2 on SDXL needs the bigG encoder instead, the node will error with a
   dimension mismatch. Fix: download bigG (~3.5 GB) from HuggingFace h94/IP-Adapter repo.

4. **ComfyUI restart required:** After installing ComfyUI_IPAdapter_plus and the new Python
   packages, ComfyUI must be restarted for the new nodes to appear. The server was running
   during installation — a restart is pending before Phase D.

5. **FightingSprites variant choice:** CivitAI model 2294900 has three variants. We chose
   "Punching and Kicking" (version 2588501) as the most versatile for fighting game poses.
   The "Idle" and "Kicking Only" variants are available if needed in Round 3 LoRA comparison.
