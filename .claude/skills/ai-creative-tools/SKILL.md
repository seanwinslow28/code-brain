---
name: ai-creative-tools
description: Orchestrate advanced creative AI workflows using ComfyUI, ElevenLabs, and Hugging Face integrations. Triggers on "generate AI art", "ComfyUI workflow", "ElevenLabs voice", "automate creative pipeline", "generate asset queue", or "AI image generation".
---

# AI Creative Tool Orchestration

## Purpose

Automate complex creative tasks by integrating specialized AI tools (ComfyUI, ElevenLabs, Hugging Face) into the Claude Code development loop. Queue image generation jobs, synthesize voice audio, and post-process generated assets using hooks and CLI scripts.

## When to Use

- Triggering local ComfyUI workflows for sprite/texture generation
- Synthesizing voiceovers via ElevenLabs API
- Searching and using Hugging Face models/spaces for generation tasks
- Automating post-processing of AI-generated assets
- Managing asynchronous generation queues

## Examples

**Example 1: ComfyUI Sprite Generation**
```
User: "Generate a pixel art potion bottle using the local ComfyUI server."
Claude: [Uses ai-creative-tools]
Queueing workflow 'pixel_art_generator.json' with prompt:
  "Red health potion, 16x16 pixel art, isometric view"

curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": <workflow_json>}'

Job queued (prompt_id: abc123). Polling for completion...
Image saved to: assets/generated/potion_01.png
Running post-process: pngquant for palette reduction.
```

**Example 2: ElevenLabs Voice Synthesis**
```
User: "Create voice lines for the Merchant NPC greeting."
Claude: [Uses ai-creative-tools]
Using ElevenLabs voice 'Adam' via API...

python3 scripts/generate_voice.py \
  --text "Welcome, traveler! Care to see my wares?" \
  --voice adam \
  --output assets/audio/npc_merchant_greeting.mp3

Output: assets/audio/npc_merchant_greeting.mp3 (3.2s)
```

**Example 3: Hugging Face Model Search**
```
User: "Find a good model for pixel art generation"
Claude: [Uses ai-creative-tools + Hugging Face MCP]
Searching Hugging Face Hub for pixel art models...

Top results:
1. nerijs/pixel-art-xl (SDXL LoRA, 2.4k downloads)
2. PublicPrompts/All-In-One-Pixel-Model (SD 1.5, fine-tuned)

Recommendation: pixel-art-xl works with your SDXL ComfyUI setup.
Download: huggingface-cli download nerijs/pixel-art-xl
```

## Core Workflows

### 1. ComfyUI Integration

ComfyUI exposes a REST API at `http://127.0.0.1:8188`. Interact via Bash tool.

**Queue a workflow:**
```bash
# Load a pre-defined workflow JSON and inject the prompt
python3 scripts/comfyui_queue.py \
  --workflow workflows/pixel_art.json \
  --prompt "Red health potion, 16x16 pixel art" \
  --seed 42
```

**The queue script pattern:**
```python
#!/usr/bin/env python3
"""Queue a ComfyUI workflow with injected prompt and seed."""
import argparse
import json
import os
import requests
import time

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")

def queue_prompt(workflow_path: str, text_prompt: str, seed: int = -1):
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Find CLIP Text Encode and KSampler nodes by class_type
    for node_id, node in workflow.items():
        if node.get("class_type") == "CLIPTextEncode" and "positive" in str(node):
            node["inputs"]["text"] = text_prompt
        if node.get("class_type") == "KSampler" and seed >= 0:
            node["inputs"]["seed"] = seed

    resp = requests.post(f"{COMFYUI_URL}/prompt",
                         json={"prompt": workflow})
    resp.raise_for_status()
    return resp.json()["prompt_id"]

def poll_completion(prompt_id: str, timeout: int = 120):
    """Poll until the job completes or times out."""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        if resp.ok and prompt_id in resp.json():
            return resp.json()[prompt_id]
        time.sleep(2)
    raise TimeoutError(f"Job {prompt_id} did not complete in {timeout}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--seed", type=int, default=-1)
    args = parser.parse_args()

    pid = queue_prompt(args.workflow, args.prompt, args.seed)
    print(f"Queued: {pid}")
    result = poll_completion(pid)
    print(f"Done: {result}")
```

**Environment setup:**
```bash
export COMFYUI_URL="http://127.0.0.1:8188"
```

### 2. ElevenLabs Voice Synthesis

Use the ElevenLabs API for voice generation. Store the API key in environment variables — never hardcode it.

**Script pattern:**
```python
#!/usr/bin/env python3
"""Generate voice audio via ElevenLabs API."""
import argparse
import os
import requests

API_KEY = os.environ["ELEVENLABS_API_KEY"]

VOICES = {
    "adam": "pNInz6obpgDQGcFmaJgB",
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "domi": "AZnzlk1XvdvUeBnXmlld",
}

def generate(text: str, voice: str, output_file: str,
             model: str = "eleven_multilingual_v2"):
    voice_id = VOICES.get(voice, voice)  # Accept name or raw ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    resp = requests.post(url, json=data, headers=headers)
    resp.raise_for_status()
    with open(output_file, "wb") as f:
        f.write(resp.content)
    print(f"Saved: {output_file} ({len(resp.content)} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="adam")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    generate(args.text, args.voice, args.output)
```

**Environment setup:**
```bash
export ELEVENLABS_API_KEY="your-key-here"
```

### 3. Hugging Face Integration (MCP)

Use the Hugging Face MCP tools available in Claude Code for model discovery and Spaces.

**Search for models:**
- `hub_repo_search` — Find models by task, keyword, or tag
- `hub_repo_details` — Get model card, download count, license
- `space_search` — Find interactive demo Spaces
- `paper_search` — Find related research papers

**Use a Hugging Face Space for generation:**
- `dynamic_space` — Run inference on a Hugging Face Space directly
- Works for image generation, text-to-speech, style transfer, etc.

**Workflow: Find and use a model**
1. Search: `hub_repo_search("pixel art SDXL LoRA", type="model")`
2. Evaluate: `hub_repo_details("nerijs/pixel-art-xl")` — check downloads, license, last updated
3. Download: `huggingface-cli download nerijs/pixel-art-xl --local-dir models/`
4. Integrate: Place in ComfyUI `models/loras/` directory

### 4. Post-Processing Hooks

Use Claude Code hooks to automatically process generated assets.

**PostToolUse hook for asset cleanup** (in `.claude/settings.json`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "bash -c 'FILE=\"$TOOL_INPUT_FILE_PATH\"; if [[ \"$FILE\" == assets/generated/*.png ]]; then pngquant --force --quality=65-80 --output \"$FILE\" \"$FILE\" 2>/dev/null; fi'"
      }
    ]
  }
}
```

**PostToolUse hook for sprite grid alignment:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "command": "bash -c 'if echo \"$TOOL_INPUT_COMMAND\" | grep -q \"comfyui_queue\"; then python3 scripts/fix_pixels.py assets/generated/; fi'"
      }
    ]
  }
}
```

### 5. Asset Index Management

Keep an `assets.json` index updated when new assets are generated:

```json
{
  "sprites": [
    {
      "id": "potion_01",
      "path": "assets/generated/potion_01.png",
      "prompt": "Red health potion, 16x16 pixel art, isometric view",
      "seed": 42,
      "date": "2026-02-17",
      "postprocess": ["pngquant", "grid-align"]
    }
  ],
  "audio": [
    {
      "id": "npc_merchant_greeting",
      "path": "assets/audio/npc_merchant_greeting.mp3",
      "text": "Welcome, traveler! Care to see my wares?",
      "voice": "adam",
      "date": "2026-02-17"
    }
  ]
}
```

After any generation, update this index so assets are discoverable.

## Directory Structure

```
project/
├── workflows/          # ComfyUI JSON workflow templates
├── scripts/
│   ├── comfyui_queue.py
│   ├── generate_voice.py
│   └── fix_pixels.py
├── assets/
│   ├── generated/      # AI image outputs
│   ├── audio/          # Voice lines
│   └── processed/      # Post-processed finals
├── models/             # Downloaded model weights (gitignored)
└── assets.json         # Asset index
```

## Cross-References

- **sprite-asset-pipeline** — Post-processing, sprite sheet packing, palette enforcement
- **pixel-art-retro-style** — Game Boy aesthetic rules for generated pixel art
- **adobe-cross-app-workflows** — Adobe MCP tools for further asset refinement
- **video-animation-production** — FFmpeg/ImageMagick for generated asset conversion

## Success Criteria

- [ ] ComfyUI server reachable and workflows queue successfully
- [ ] API keys stored in environment variables (never hardcoded)
- [ ] Generated assets trigger post-processing hooks
- [ ] Audio files are valid MP3/WAV
- [ ] `assets.json` index is updated after each generation
- [ ] Hugging Face MCP tools used for model discovery

## Copy/Paste Ready

```
"Queue a ComfyUI job for a 16x16 pixel art chest"
"Generate audio for the opening narration using ElevenLabs"
"Find a Hugging Face model for pixel art generation"
"Set up a post-processing hook for new AI sprites"
"Search Hugging Face for text-to-speech models"
```