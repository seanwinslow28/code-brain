# Alienware ComfyUI Setup for Video Model Testing

## Launch ComfyUI (RTX 5080 safe)

```bash
# SDPA only — NO xformers (crashes on sm_120)
cd /path/to/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 --force-fp16 --fp16-intermediates
```

## Install Required Custom Nodes

```bash
cd /path/to/ComfyUI/custom_nodes

# Frame Interpolation (GMFSS Fortuna)
git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
cd ComfyUI-Frame-Interpolation && pip install -r requirements.txt && cd ..

# Video Helper Suite (for VHS_VideoCombine node)
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
```

## Download Wan 2.2 Model + LoRA

```bash
cd /path/to/ComfyUI/models

# Wan 2.2 I2V checkpoint (bf16)
huggingface-cli download Wan-AI/Wan2.2-I2V-14B-480P --local-dir checkpoints/wan22_i2v/

# Pixel Animation LoRA (styly-agents)
huggingface-cli download styly-agents/Wan2-2-pixel-animate --local-dir loras/
# Rename to match workflow: wan22_pixel_animate.safetensors

# Optional: CivitAI attack animation LoRA
# https://civitai.com/models/2085866
# Download manually and place in loras/
```

## Verify

```bash
# From MacBook Pro:
curl http://192.168.68.201:8188/system_stats
# Should return JSON with VRAM info
```

## Wan 2.2 Workflow

Workflow JSON: `workflows/wan22_i2v_pixel_animate.json`
- Input: Static sprite PNG with #00FF00 green background
- Output: 2-second MP4 at 24fps
- LoRA strength: 0.85 (adjustable)

## GMFSS Fortuna Workflow

Workflow JSON: `workflows/gmfss_fortuna_interpolation.json`
- Input: 2-5 keyframe PNGs
- Output: Interpolated MP4 at 12fps
- Multiplier: 4x (inserts 3 frames between each pair)
