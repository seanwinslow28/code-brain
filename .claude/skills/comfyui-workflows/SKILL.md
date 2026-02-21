---
name: comfyui-workflows
description: ComfyUI workflow design, debugging, and automation for image generation. Covers workflow JSON structure, node wiring (KSampler, LoRA, ControlNet, IPAdapter), API queuing and polling, custom node management, batch generation, and workflow templating. Use when asked about "ComfyUI workflow", "ComfyUI nodes", "LoRA setup", "ControlNet workflow", "image generation pipeline", "ComfyUI API", or "batch generate images".
---

# ComfyUI Workflows

## Purpose

Design, debug, and automate ComfyUI workflows for image generation. This skill covers the workflow JSON format, common node patterns, API integration for queuing/polling, LoRA and ControlNet configuration, batch generation, and workflow templating. Complements `ai-creative-tools` (which handles tool orchestration across ComfyUI, ElevenLabs, and HF) by going deep on ComfyUI specifically.

## When to Use

- Building a new ComfyUI workflow from scratch
- Debugging a workflow that produces bad results or errors
- Adding LoRA, ControlNet, or IPAdapter to an existing workflow
- Automating batch generation via the ComfyUI API
- Converting a UI-built workflow to a reusable JSON template
- Managing custom nodes and model files

## Examples

**Example 1: Build a Character Generation Workflow**
```
User: "Create a ComfyUI workflow for generating character poses with a style LoRA"
Claude: [Uses comfyui-workflows]

Workflow: character_pose_lora.json

Node graph:
  CheckpointLoader → KSampler → VAEDecode → SaveImage
       ↓                ↑
  LoraLoader ──→ CLIP ──→ CLIPTextEncode (positive)
                       ──→ CLIPTextEncode (negative)

Settings:
- Checkpoint: sd_xl_base_1.0.safetensors
- LoRA: character_style_v2.safetensors (weight: 0.8)
- Sampler: euler_ancestral, 25 steps, cfg: 7.0
- Resolution: 1024x1024

Saving workflow JSON...
```

**Example 2: Debug Poor Generation Quality**
```
User: "My ComfyUI outputs look blurry and washed out"
Claude: [Uses comfyui-workflows]

Common causes and fixes:

1. CFG too low → Increase from 4-5 to 7-8
2. Steps too few → Increase from 15 to 25-30
3. Wrong sampler → Switch from ddim to euler_ancestral for SDXL
4. VAE mismatch → Ensure SDXL uses sdxl_vae.safetensors (not SD 1.5 VAE)
5. Resolution wrong → SDXL needs 1024x1024 base (not 512x512)

Let me check your workflow JSON for these issues...
```

**Example 3: Batch Generate with API**
```
User: "Generate 20 character poses with different seeds"
Claude: [Uses comfyui-workflows]

python3 scripts/comfyui_batch.py \
  --workflow workflows/character_pose_lora.json \
  --prompt "standing hero character, front view, white background" \
  --count 20 \
  --seed-start 1000 \
  --output assets/characters/hero/

Queuing 20 jobs... [████████████████████] 20/20
All jobs complete. Output: assets/characters/hero/pose_1000-1019.png
```

## Workflow JSON Structure

ComfyUI workflows are JSON objects where each key is a node ID and each value defines the node.

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a hero character, standing pose, white background",
      "clip": ["1", 1]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "blurry, deformed, ugly, text, watermark",
      "clip": ["1", 1]
    }
  },
  "4": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 25,
      "cfg": 7.0,
      "sampler_name": "euler_ancestral",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["1", 0],
      "positive": ["2", 0],
      "negative": ["3", 0],
      "latent_image": ["5", 0]
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["4", 0],
      "vae": ["1", 2]
    }
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "character",
      "images": ["6", 0]
    }
  }
}
```

**Key concepts:**
- Node connections use `["node_id", output_index]` format
- `output_index` 0 = first output, 1 = second, etc.
- CheckpointLoaderSimple outputs: [0]=MODEL, [1]=CLIP, [2]=VAE

## Common Node Patterns

### Base Pattern: Text-to-Image

```
CheckpointLoader → CLIPTextEncode (pos) → KSampler → VAEDecode → SaveImage
                 → CLIPTextEncode (neg) ↗
                 → EmptyLatentImage    ↗
```

### LoRA Pattern

Insert between CheckpointLoader and CLIPTextEncode:

```
CheckpointLoader → LoraLoader → CLIPTextEncode → KSampler
                              ↗
```

```json
{
  "class_type": "LoraLoader",
  "inputs": {
    "lora_name": "style_v2.safetensors",
    "strength_model": 0.8,
    "strength_clip": 0.8,
    "model": ["1", 0],
    "clip": ["1", 1]
  }
}
```

**LoRA weight guidelines:**
| Weight | Effect |
|:-------|:-------|
| 0.5-0.6 | Subtle influence, maintains base model character |
| 0.7-0.85 | Strong style transfer, good balance (recommended) |
| 0.9-1.0 | Dominant, can overfit or produce artifacts |
| >1.0 | Experimental, often produces distortion |

### ControlNet Pattern

Add ControlNet conditioning to guide composition:

```
ControlNetLoader → ControlNetApply → KSampler
LoadImage (guide) ↗
```

```json
{
  "class_type": "ControlNetApplyAdvanced",
  "inputs": {
    "strength": 0.85,
    "start_percent": 0.0,
    "end_percent": 1.0,
    "positive": ["2", 0],
    "negative": ["3", 0],
    "control_net": ["cn_loader", 0],
    "image": ["guide_image", 0]
  }
}
```

**ControlNet models by use case:**
| Model | Input | Use Case |
|:------|:------|:---------|
| control_v11p_sd15_canny | Edge map | Precise outlines |
| control_v11p_sd15_lineart | Line drawing | Clean lineart guidance |
| control_v11p_sd15_openpose | Pose skeleton | Character posing |
| control_v11f1p_sd15_depth | Depth map | Composition/perspective |
| t2i-adapter_diffusers_xl_canny | Edge map (SDXL) | SDXL edge control |

### IPAdapter Pattern (Style Reference)

Use an image as a style reference (instead of text prompt):

```
IPAdapterModelLoader → IPAdapter → KSampler
CLIPVisionLoader    ↗
LoadImage (ref)     ↗
```

### Upscale Pattern (Hi-Res Fix)

Two-pass generation for higher quality:

```
KSampler (base) → LatentUpscale → KSampler (refine, denoise=0.4) → VAEDecode
```

## API Integration

### Queue a Job

```bash
curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": <workflow_json>}'

# Response: {"prompt_id": "abc-123-def"}
```

### Poll for Completion

```bash
curl -s http://127.0.0.1:8188/history/abc-123-def

# Returns job details when complete, empty when still processing
```

### Get Generated Images

```bash
# After job completes, images are in the output directory
# Default: ComfyUI/output/
# Filename: {prefix}_{counter}.png
```

### Batch Generation Script

```python
#!/usr/bin/env python3
"""Batch queue ComfyUI workflows with varying seeds."""
import json
import requests
import time
import sys

COMFYUI_URL = "http://127.0.0.1:8188"

def queue_batch(workflow_path, prompt_text, count, seed_start, output_prefix):
    with open(workflow_path) as f:
        workflow = json.load(f)

    jobs = []
    for i in range(count):
        seed = seed_start + i
        # Inject prompt and seed
        for node_id, node in workflow.items():
            if node.get("class_type") == "CLIPTextEncode" and "positive" in str(node):
                node["inputs"]["text"] = prompt_text
            if node.get("class_type") == "KSampler":
                node["inputs"]["seed"] = seed
            if node.get("class_type") == "SaveImage":
                node["inputs"]["filename_prefix"] = f"{output_prefix}_{seed}"

        resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow})
        resp.raise_for_status()
        jobs.append(resp.json()["prompt_id"])
        print(f"Queued {i+1}/{count} (seed={seed})")

    # Poll all jobs
    for job_id in jobs:
        while True:
            resp = requests.get(f"{COMFYUI_URL}/history/{job_id}")
            if resp.ok and job_id in resp.json():
                break
            time.sleep(2)

    print(f"All {count} jobs complete.")
```

## Model Management

### Directory Structure

```
ComfyUI/
├── models/
│   ├── checkpoints/    # Base models (.safetensors)
│   ├── loras/          # LoRA weights
│   ├── controlnet/     # ControlNet models
│   ├── vae/            # VAE models
│   ├── clip_vision/    # CLIP vision models (for IPAdapter)
│   └── ipadapter/      # IPAdapter models
├── custom_nodes/       # Custom node packages
├── input/              # Input images (for ControlNet, IPAdapter)
└── output/             # Generated images
```

### Recommended Base Models

| Model | Size | Best For |
|:------|:-----|:---------|
| sd_xl_base_1.0 | 6.9 GB | General SDXL generation |
| sdxl_turbo | 6.9 GB | Fast SDXL (4 steps) |
| sd_v1-5 | 4.3 GB | SD 1.5 workflows, more LoRA support |
| animagine-xl-3.1 | 6.9 GB | Anime/illustration style |

## Debugging Workflows

| Symptom | Likely Cause | Fix |
|:--------|:------------|:----|
| Black image | VAE mismatch or missing connection | Check VAE is connected to VAEDecode |
| Blurry/washed out | CFG too low or steps too few | Increase cfg to 7-8, steps to 25+ |
| Wrong resolution | SDXL at 512x512 | SDXL needs 1024x1024 base |
| Style not applied | LoRA weight too low or wrong model | Increase weight, verify model compatibility |
| Artifacts/distortion | LoRA weight too high | Reduce to 0.7-0.8 |
| ControlNet ignored | Strength too low or wrong model | Increase strength, verify CN model matches base |
| "Node not found" error | Missing custom node | Install via ComfyUI Manager |
| OOM (out of memory) | Resolution too high or batch too large | Reduce resolution or batch_size to 1 |

## Success Criteria

- [ ] Workflow JSON is valid and all node connections resolve
- [ ] Generated images match the intended style and composition
- [ ] LoRA weights are in the 0.7-0.85 range for style consistency
- [ ] API queuing and polling work reliably
- [ ] Batch generation completes with proper seed variation
- [ ] Output filenames are descriptive and organized

## Related Skills

- `ai-creative-tools` — Tool orchestration across ComfyUI, ElevenLabs, and HF (the higher-level skill)
- `animation-pipeline` — Uses ComfyUI for character/background generation in production
- `sprite-asset-pipeline` — Post-processes ComfyUI output for game assets
- `pixel-art-retro-style` — Aesthetic rules when generating pixel art via ComfyUI

## Copy/Paste Ready

```
"Build a ComfyUI workflow for [description]"
"Add a LoRA to this workflow"
"Add ControlNet to guide composition"
"Debug this ComfyUI workflow — output is [problem]"
"Batch generate 20 variations of [prompt]"
"Set up IPAdapter for style reference"
"What nodes do I need for [task]?"
```