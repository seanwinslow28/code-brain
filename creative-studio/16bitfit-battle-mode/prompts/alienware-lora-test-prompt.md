# Alienware Claude Code Prompt — LoRA ComfyUI Testing

Paste everything below the line into Claude Code on the Alienware.

---

<role>You are helping me test a freshly trained style LoRA in ComfyUI on my Alienware RTX 5080. I'm a beginner with code — explain what you're doing and why.</role>

<context>
I just finished training a 16BitFit sprite style LoRA using kohya_ss. The training used Illustrious XL v0.1 as the base, 61 images, 10 epochs, rank 32, Adafactor optimizer. Final loss: 0.080. Two checkpoints were saved (epoch 5 and epoch 10).

Now I need to test whether this LoRA actually improves pixel art sprite quality when used for inference with a proper base model and sampler settings.
</context>

<constraints>
- RTX 5080: Use SDPA attention only. NO xformers (crashes on sm_120 architecture).
- ComfyUI must be launched with `--force-fp16` for VRAM savings.
- LoRA was TRAINED on Illustrious XL v0.1. INFERENCE must use v2.0-STABLE or v3.x (better quality, confirmed cross-compatible with v0.1 LoRAs).
- Trigger word: `16bitfit_style` — must appear in every positive prompt.
- Do NOT use Wan 2.2 or video models for this test. This is purely image generation (txt2img) to evaluate the LoRA's style transfer.
</constraints>

<file_paths>
- ComfyUI root: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\`
- LoRA (epoch 10/final): `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style.safetensors`
- LoRA (epoch 5): `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\16bitfit_sprite_style-000005.safetensors`
- Checkpoints dir: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\checkpoints\`
- Output dir: `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\comfyui-test\`
</file_paths>

<tasks>

## Task 0: Pre-flight checks

1. **Check which base models are available** in `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\checkpoints\`. List all `.safetensors` and `.ckpt` files.
2. **Check if Illustrious XL v2.0-STABLE or v3.x is present.** Look for filenames containing "illustrious", "illustriousXL", "ill-xl", or similar. If ONLY v0.1 is present, STOP and tell me — I need to download v2.0-STABLE first. DO NOT proceed with v0.1 for inference testing.
3. **Copy the epoch 5 checkpoint** to the ComfyUI loras folder if it's not already there:
   ```powershell
   if (-not (Test-Path "C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style-000005.safetensors")) {
       copy "C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\16bitfit_sprite_style-000005.safetensors" "C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\"
   }
   ```
4. **Create the output directory** if it doesn't exist:
   ```powershell
   New-Item -ItemType Directory -Force -Path "C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\comfyui-test"
   ```
5. **Check if ComfyUI is running** by testing `http://127.0.0.1:8188/`. If not running, tell me to start it with `--force-fp16`.

## Task 1: Build ComfyUI workflow JSON for LoRA testing

Create a Python script at `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\comfyui-test\run_lora_test.py` that:

1. **Uses the ComfyUI REST API** (`http://127.0.0.1:8188/`) to queue workflow prompts programmatically. This avoids us having to manually click through the ComfyUI UI — the script builds the workflow as a JSON object and sends it to ComfyUI's `/prompt` endpoint.

2. **Generates a grid of test images** covering these variables:
   - **LoRA checkpoints:** epoch 5 vs epoch 10
   - **LoRA strengths:** 0.0 (no LoRA / baseline), 0.5, 0.7, 0.8, 0.9, 1.0
   - **Test prompts** (3 prompts):
     - `"16bitfit_style, pixel art fighter, idle stance, bold outlines, green screen background, full body, facing right, 128x128 sprite"`
     - `"16bitfit_style, pixel art fighter, punch attack pose, bold outlines, green screen background, full body, facing right, dynamic action pose"`
     - `"16bitfit_style, pixel art fighter, walking frame mid-stride, bold outlines, green screen background, full body, facing right, legs apart"`

3. **Workflow structure** (this is what each JSON prompt should contain — these map to ComfyUI nodes):
   - **CheckpointLoaderSimple** — loads the Illustrious XL v2.0-STABLE (or v3.x) base model
   - **LoraLoader** — applies `16bitfit_sprite_style.safetensors` at the specified strength (for model AND clip). Skip this node entirely for strength 0.0 (baseline).
   - **CLIPTextEncode (positive)** — the test prompt
   - **CLIPTextEncode (negative)** — `"blurry, anti-aliased, gradient, low quality, 3d render, realistic, photograph, watermark, text, deformed"`
   - **EmptyLatentImage** — 1024×1024 (this is the native SDXL resolution; we downscale later)
   - **KSampler** — seed: use a FIXED seed (42) for all tests so results are directly comparable. Steps: 28, CFG: 7, sampler_name: "euler", scheduler: "normal", denoise: 1.0
   - **VAEDecode** — decode latent to image
   - **SaveImage** — save to output dir with descriptive filename: `{prompt_index}_{checkpoint}_{strength}_{seed}.png`

4. **Total images to generate:** 2 checkpoints × 6 strengths × 3 prompts = 36 images (but strength 0.0 only needs 1 run per prompt since there's no LoRA, so actually: 3 baseline + 30 with-LoRA = 33 images)

5. **After generation, create a summary** that lists all output files grouped by prompt, with the LoRA strength and checkpoint for each.

**Important implementation notes:**
- Use `requests` library to POST to ComfyUI's API
- The ComfyUI API workflow format uses numbered string keys ("1", "2", "3"...) for nodes, with `class_type` and `inputs` fields
- To get the correct node class names, you can query `http://127.0.0.1:8188/object_info` for the full node registry
- For the baseline (no LoRA) runs, connect the checkpoint loader directly to the CLIP text encoders and KSampler (skip the LoRA loader node)
- Use `websocket` to connect to `ws://127.0.0.1:8188/ws` to track when each prompt finishes before queuing the next one
- The script should be resumable — check which output files already exist and skip those

## Task 2: Run the test

Execute the script and monitor progress. Report any errors. Expected time: ~2-5 minutes per image on RTX 5080 with SDXL, so 33 images should take roughly 1-3 hours total.

## Task 3: Analyze results

After all images generate:
1. List all output files with their sizes
2. Group by prompt and summarize which strength/checkpoint combinations produced output
3. Tell me which images to compare visually — specifically:
   - For each prompt: baseline (no LoRA) vs epoch 10 at 0.8 strength (the recommended starting point)
   - Epoch 5 vs epoch 10 at 0.8 strength (to check for overfitting)
   - Strength sweep: 0.5 → 0.7 → 0.8 → 0.9 → 1.0 for epoch 10 (to find the sweet spot)

The key question we're answering: **Does the LoRA produce more consistent, recognizable 16BitFit-style pixel art sprites compared to the base model alone?** If yes, we integrate it into the production pipeline. If no, we may need to retrain with different parameters or more data.

</tasks>
