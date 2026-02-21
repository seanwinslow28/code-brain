---
name: ai-creative-tools
description: Orchestrate advanced creative AI workflows using ComfyUI, ElevenLabs, and CLI integrations. Triggers on "generate AI art", "ComfyUI workflow", "ElevenLabs voice", "automate creative pipeline", or "generate asset queue".
---

# AI Creative Tool Orchestration

## Purpose

Automate complex creative tasks by integrating specialized AI tools (ComfyUI, ElevenLabs) directly into the Claude Code development loop. Use MCP servers or CLI wrappers to plan, execute, and post-process generated assets without leaving the terminal.

## When to Use

- Triggering local ComfyUI workflows for sprite/texture generation
- Synthesizing placeholder or final voiceovers via ElevenLabs
- Automating post-processing hooks for new AI assets
- Managing asynchronous generation queues

## Examples

**Example 1: Generating a ComfyUI Sprite**
```
User: "Generate a pixel art potion bottle using the local ComfyUI server."
Claude: [Uses ai-creative-tools]
Connecting to local ComfyUI (http://127.0.0.1:8188)...
Queueing workflow 'pixel_art_generator.json' with prompt: "Red health potion, 16x16 pixel art, isometric view"
Job ID: 412
...
Success! Image saved to: assets/generated/potion_01.png
Running post-process hook: proper-pixel-art (Cleaning palette...)
```

**Example 2: Synthesizing Dialogue**
```
User: "Create voice lines for the Merchant NPC greeting."
Claude: [Uses ai-creative-tools]
Using ElevenLabs voice 'Adam' (ID: ErX...)
Generating: "Welcome, traveler! Care to see my wares?"
Output: assets/audio/npc_merchant_greeting.mp3
Duration: 3.2s
```

## Core Workflows

### 1. ComfyUI Integration (JSON Payload)
Manage ComfyUI by injecting prompts into pre-defined workflow JSONs.

```javascript
// Function to queue a ComfyUI prompt
async function queueComfyPrompt(textPrompt, seed) {
  const workflow = require('./workflows/pixel_art.json');
  
  // Inject values into nodes (ID 6 = CLIP Text Encode, ID 3 = KSampler)
  workflow["6"].inputs.text = textPrompt;
  workflow["3"].inputs.seed = seed;

  const response = await fetch('http://127.0.0.1:8188/prompt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: workflow })
  });

  return await response.json(); // Returns { prompt_id: ... }
}
```

### 2. ElevenLabs Voice Synthesis (Python Wrapper)
Use the API directly or a CLI wrapper to generate audio assets.

```python
# scripts/generate_voice.py
import requests
import sys

VOICE_ID = "ErX..." 
API_KEY = "YOUR_XI_API_KEY"

def generate(text, output_file):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": { "stability": 0.5, "similarity_boost": 0.5 }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(output_file, 'wb') as f:
        f.write(response.content)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2])
```

### 3. Orchestration: CLAUDE.md Configuration
Define "hooks" in `CLAUDE.md` to automate the pipeline.

```markdown
# Asset Pipeline Rules

## Automation Hooks
1. **Watch:** `assets/generated/*.png`
   **Action:** Run `python3 scripts/fix_pixels.py`
   **Reason:** Enforce grid alignment on new AI sprites

2. **Watch:** `assets/dialogue/*.txt`
   **Action:** Run `python3 scripts/generate_voice.py`
   **Reason:** Auto-synthesize audio when script files change

## Directory Map
- `workflows/` -> ComfyUI JSON templates
- `assets/generated/` -> AI image outputs
- `assets/audio/` -> Voice lines
```

### 4. Custom Slash Commands
Simplify complex multi-step instructions.

```markdown
# .claude/commands/npc.md

To create a new NPC:
1. Generate sprite: Use ComfyUI 'pixel_char' workflow with prompt "{1}"
2. Generate voice: Use ElevenLabs 'Adam' for greeting "{2}"
3. Save to: `assets/npc/{name}/`
4. Update `assets.json` index
```
Usage: `/npc_create "Wizard, blue robe" "Halt! Who goes there?"`

## Success Criteria

- [ ] ComfyUI server is reachable at `127.0.0.1:8188` (or configured URL)
- [ ] JSON workflows have correct node IDs for injection
- [ ] Generated assets trigger the defined post-processing scripts
- [ ] Audio files are valid MP3/WAV and playable
- [ ] `assets.json` index is updated after generation

## Copy/Paste Ready

```
"Queue a ComfyUI job for a 16x16 pixel art chest"
"Generate audio for the opening narration using ElevenLabs"
"Set up a CLAUDE.md hook to clean new sprites automatically"
"Create a custom command for generating full NPC assets"
```
