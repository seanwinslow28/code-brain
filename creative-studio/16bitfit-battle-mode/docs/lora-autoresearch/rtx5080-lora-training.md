---
type: reference
domain:
  - creative-studio
status: active
context: 16bitfit
ai-context: "Complete LoRA training guide for RTX 5080: kohya_ss setup, Illustrious XL, sprite pipeline, and autoresearch optimization loop."
created: 2026-03-14
source: perplexity-computer-research
---

# LoRA Training Guide — RTX 5080 Sprite & Animation Style Transfer

Complete guide to training a style LoRA on an RTX 5080 (16GB GDDR7) for 16BitFit sprite generation and 2D animation. Covers framework setup, base model selection, dataset prep, training configuration, ComfyUI integration, and an autoresearch-inspired automated optimization loop.

Synthesized from two Perplexity Computer research sessions (March 2026), reconciled against RTX 50-series community reports.

---

## Quick Reference — The Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Training framework | **kohya_ss** (dev branch, gui-uv.bat) | Best SDXL support, largest community, fits 16GB with fused backward pass |
| Base model | **Illustrious XL v0.1** | Purpose-built for 2D illustration, fewer training steps needed |
| Optimizer | **Adafactor** | Required for fused backward pass (~10GB VRAM). **NOT Prodigy** — pathologically slow on Blackwell GPUs |
| Attention | **SDPA** (PyTorch native) | xformers causes `cutlassF: no kernel found` crashes on sm_120. Disable xformers entirely |
| Mixed precision | **bf16** | Native on RTX 5080 |
| LoRA rank | **32** | Sweet spot for style LoRAs (~20-40MB file) |
| Dataset size | **30-50 PNG images** | Your art style, 1024px+, nearest-neighbor upscaling only |
| Training time | **30-90 minutes** | 10 epochs, 10-15 repeats, ~1,500-3,000 steps |

---

## Part 1: RTX 5080 Compatibility

The RTX 50-series (Blackwell) uses CUDA compute capability **sm_120**, which requires specific software versions. This is the #1 source of setup pain — get this right first.

### Version Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| PyTorch | 2.7.0 nightly cu128 | 2.7.1+ cu128 or 2.8+ | Stable releases before 2.7 do NOT support sm_120 |
| CUDA Toolkit | 12.8 | 12.8-12.9 | cu121 builds will NOT work |
| cuDNN | 9.x | 9.10.1+ | Required for Blackwell kernels |
| NVIDIA Driver | 570+ | Latest Game Ready / Studio | https://www.nvidia.com/drivers |
| xformers | **Disabled** | Do not install | Use SDPA instead — safest path |
| kohya_ss | dev branch | dev branch with gui-uv.bat | Stable branch does NOT support sm_120 |

### Path of Least Resistance: gui-uv.bat

The `gui-uv.bat` launcher in kohya_ss bundles the correct PyTorch/CUDA versions automatically. This is the recommended install path for the 5080 — it sidesteps most version-mismatch issues.

### Manual PyTorch Install (if needed)

```bash
# Install PyTorch with CUDA 12.8 support
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

# Do NOT install xformers — use SDPA instead
pip3 uninstall xformers

# Verify CUDA works
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"
```

### Setup Video Guides (RTX 5080)

- https://youtu.be/ihukS8BZVuE?si=2hK2Vm53hvIZ19Gm
- https://youtu.be/3lPc3dmxD54?si=litPINBTHNSxp3aH

### Known 50-Series Bugs

**`cutlassF: no kernel found` (xformers crash)** — Affects 5080/5090 when xformers is enabled. Fix: uninstall xformers, use SDPA.

**Prodigy optimizer is pathologically slow on Blackwell** — One user reported 4.78 s/it on a 5090 with Prodigy + gradient checkpointing. Fix: use Adafactor or AdamW. Disabling gradient checkpointing gives ~20% improvement but costs VRAM.

**GPU shows 100% utilization but low temps and slow training** — Reported on 5080/5090. GPU at 40-45°C (should be 70°C+) with very slow s/it. Likely a driver or power management issue. Update to latest drivers.

**bitsandbytes CUDA errors on Windows** — The #1 Windows-specific issue. Use latest bitsandbytes (0.44.0+). If errors persist, switch to Adafactor or standard AdamW (not 8-bit variants).

**Windows path length** — Windows has a 260-character path limit. Keep training directory paths short (e.g., `C:\lora-training\`).

**Antivirus interference** — Windows Defender slows file I/O during training. Add ComfyUI and training directories to the exclusion list.

---

## Part 2: Base Model

### Illustrious XL v0.1 (Recommended)

A purpose-built SDXL finetune for anime and illustration. Delivers cleaner line work, better color reproduction, and stronger prompt adherence than base SDXL 1.0. Its flat illustration style aligns well with 2D game art and pixel art aesthetics.

- **Parameters**: 3.5 billion (SDXL architecture)
- **Training efficiency**: ~500 steps often gives great results for style concepts
- **Inference VRAM**: ~6-8GB
- **Download**: HuggingFace — `OnomaAIResearch/Illustrious-xl-early-release-v0`
- **Cross-compatibility**: LoRAs trained on Illustrious also work on NoobAI XL (an Illustrious finetune)

### Alternatives (if Illustrious doesn't fit)

- **Pony Diffusion V6 XL** — Large LoRA ecosystem on CivitAI. Requires clip_skip=2 and >3,600 steps. Good for anime-adjacent styles
- **NoobAI XL** — Illustrious finetune with broader stylistic range. Cross-compatible with Illustrious LoRAs

### Future Option: Flux

**Flux.1 Dev** (12B params) offers superior text rendering and anatomy but needs ~9GB VRAM with NF4 quantization via ai-toolkit. ControlNet/IP-Adapter ecosystem is less mature than SDXL. Monitor **Flux 2 Klein 9B** as a 16GB-friendly option. Use ai-toolkit (by Ostris) when ready for Flux.

### Do NOT Use

- **SDXL 1.0 base** — Too generic for illustration; always use a finetune
- **SD 3.5** — Limited community adoption for 2D illustration
- **SD 1.5** — Outdated architecture

---

## Part 3: Dataset Preparation

### Image Count

- **Minimum viable**: 15-20 images
- **Recommended**: 30-50 images
- **Ideal**: 50-100 for complex styles with variation
- Quality and diversity matter more than quantity — different poses, compositions, and subjects within a consistent style

### Resolution

- **SDXL native**: 1024×1024
- Images should be at least 1024px on the shortest side
- Mixed aspect ratios are fine — aspect ratio bucketing handles this automatically with `bucket_reso_steps=64`
- Enable `bucket_no_upscale` to prevent the framework from upscaling smaller images
- Enable `cache_latents` + `cache_latents_to_disk` for faster training and lower VRAM

### Pixel Art & Flat 2D Specific Rules

- **PNG format only** — JPEG compression destroys pixel art clarity
- **Nearest-neighbor upscaling only** — Standard upscalers blur pixels
- **Crop characters on clean/transparent backgrounds** where possible
- **Do not mix pixel art with non-pixel-art images** — style consistency is critical
- Include style keywords in captions: "pixel art", "limited color palette", "clean outlines", "flat shading", "retro game style", "game boy aesthetic"

### Captioning Strategy

**Trigger word**: Choose a unique token — `16bitfit_style` or `seanart_style`

**Caption formula**: `[trigger_word], [medium/style keywords], [content description]`

**Example**: `16bitfit_style, pixel art, retro game boy style, a warrior character standing in idle pose`

**Key principle**: Caption everything that ISN'T part of the style you want learned. Describe subjects, poses, and backgrounds — the model learns the style from what remains unspecified.

**Auto-captioning tools**:
- **WD Tagger** (WD-1.4) — Best for SDXL/Illustrious, tag-based, fast, low VRAM. Use this.
- **JoyCaption** — Natural language captions, better for Flux. Save for later.
- **Florence-2** — General tagging, fast, low VRAM. Good alternative.

After auto-captioning, prepend your trigger word to every caption file.

**Text encoder**: Set `text_encoder_lr` to **0** for style LoRAs. Train UNet only — this forces the model to learn style from visual features, not text associations.

**Regularization images**: Not needed for style LoRAs. They add complexity without benefit when training style (vs. character/face).

### Folder Structure (kohya_ss)

```
training_data/
  10_16bitfit_style/
    image001.png
    image001.txt
    image002.png
    image002.txt
    ...
```

- The `10_` prefix = 10 repeats per image per epoch
- Formula: `total_steps = (num_images × repeats × epochs) / batch_size`
- For 40 images × 10 repeats × 10 epochs / 1 batch = 4,000 steps

---

## Part 4: Training Configuration

### Core Settings (RTX 5080 + Adafactor + Fused Backward Pass)

| Parameter | Value | Why |
|-----------|-------|-----|
| Batch size | **1** | 16GB requires batch 1 |
| Gradient accumulation | **2** | Simulates batch size of 2 |
| Gradient checkpointing | **Enabled** | Required for 16GB |
| Mixed precision | **bf16** | Native on RTX 5080 |
| Fused backward pass | **Enabled** | Reduces VRAM from ~24GB to ~10GB |
| Cache latents to disk | **Enabled** | Saves VRAM during training |

### Network Architecture

| Parameter | Value |
|-----------|-------|
| LoRA rank (network_dim) | **32** |
| Network alpha | **32** (same as rank for 1.0 scaling) |
| Network type | `networks.lora` |

### Optimizer

| Parameter | Value |
|-----------|-------|
| Optimizer | **Adafactor** (required for fused backward pass) |
| Learning rate | **0.0005** (UNet only) |
| text_encoder_lr | **0** |
| network_train_unet_only | **True** |
| LR scheduler | **cosine** or **cosine_with_restarts** |
| Min SNR gamma | **5** |
| Noise offset | **0.03** (start low for pixel art) |
| clip_skip | **1** (for Illustrious) |

### Training Duration

| Parameter | Value |
|-----------|-------|
| Repeats | 10-15 |
| Epochs | 10 |
| Total steps | ~1,500-3,000 |
| Expected time | **30-90 minutes** on RTX 5080 |
| sample_every_n_epochs | 5 |
| save_every_n_epochs | 5 |

### LoRA Rank Guide

| Rank | File Size | Best For | Risk |
|------|-----------|----------|------|
| 16 | ~10-20MB | Simple flat styles | May miss nuance |
| **32** | ~20-40MB | **Most style LoRAs (recommended)** | Balanced |
| 64 | ~40-80MB | Complex styles with lots of variation | Overfitting with small datasets |

### Monitoring Training

- Create a `sample_prompts.txt` with 2-3 test prompts including your trigger word
- Watch training loss: should decrease gradually (~0.08-0.12 typical for SDXL)
- Loss plateaus early → LR too low. Loss spikes → LR too high
- Use **X/Y/Z plot** in ComfyUI after training to compare epoch checkpoints vs. LoRA strength

### VRAM Troubleshooting Ladder

If you hit VRAM errors, apply in order:
1. Enable fused_backward_pass + Adafactor (~10GB)
2. Reduce resolution to 768×768
3. Reduce network_dim from 32 to 16
4. Enable cache_latents_to_disk
5. Last resort: optimizer_groups=8 (~14GB)

---

## Part 5: ComfyUI Integration

### Loading Your Trained LoRA

Place `.safetensors` file in `ComfyUI/models/loras/`. Restart ComfyUI or refresh the model list.

### Basic LoRA Workflow

```
[Load Checkpoint] → Illustrious XL
       ↓
[Load LoRA] → Your trained style LoRA (strength 0.8)
       ↓
[CLIP Text Encode] → Positive (include trigger word) + Negative
       ↓
[KSampler] → Generate
       ↓
[VAE Decode] → [Save Image]
```

### LoRA Weight Ranges

| Strength | Effect |
|----------|--------|
| 0.5-0.7 | Subtle style influence, blends with base |
| **0.7-0.9** | **Recommended starting range** |
| 0.9-1.0 | Strong style, may override base characteristics |
| 1.0+ | Very strong — test carefully, can cause artifacts |

### Full Sprite Pipeline: LoRA + ControlNet + IP-Adapter

This is the target workflow — style LoRA for consistency, ControlNet for pose control, IP-Adapter for character reference.

**Required custom nodes (install via ComfyUI Manager):**
- **ComfyUI_IPAdapter_plus** (cubiq) — Maintenance mode since April 2025 but functional
- **ComfyUI ControlNet Auxiliary Preprocessors** (comfyui_controlnet_aux)
- **ComfyUI_Comfyroll_CustomNodes** (Suzie1) — LoRA stacks, multi-ControlNet

**Required models:**
- ControlNet: SDXL-compatible OpenPose or depth map model
- IP-Adapter: `ip-adapter-plus_sdxl_vit-h.bin`
- CLIP Vision: `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`

**Full pipeline workflow:**

```
Input: Reference character image + Pose skeleton image

[Load Checkpoint] → Illustrious XL
       ↓
[Load LoRA] → Style LoRA (0.7-0.9)
       ↓
[IPAdapter Model Loader] + [Load CLIP Vision] + [Load Image (reference)]
       ↓
[IPAdapter Advanced] → Feeds modified model with reference style
       ↓
[ControlNet Loader] + [Load Image (pose skeleton)]
       ↓
[Apply ControlNet] → Applies pose control
       ↓
[CLIP Text Encode] → Positive (with trigger word) + Negative
       ↓
[KSampler] → Generates image matching style + pose
       ↓
[VAE Decode] → [Save Image]
```

### Balancing Three Controls

| Control | Range | Too strong | Too weak |
|---------|-------|------------|----------|
| ControlNet | 0.5-0.8 | Output too rigid | Pose drifts |
| IP-Adapter | 0.5-0.8 | Over-copies reference | Character features drift |
| LoRA | 0.7-0.9 | Artifacts/overtrained look | Style inconsistent |

These three weight ranges are exactly what the autoresearch loop will optimize.

### Additional Useful Nodes

- **ComfyUI_VNCCS** — Sprite Generator node for automating sprite sheet creation
- **Efficiency Nodes** — KSampler (Efficient) for better performance
- **Create Hook LoRA** — Apply LoRA to specific conditioning regions (native since Dec 2024)

---

## Part 6: Autoresearch Loop for Sprite Optimization

Inspired by Karpathy's autoresearch — an autonomous loop that iterates on parameters, scores results, keeps improvements, and discards failures. Applied to ComfyUI sprite generation.

### Architecture

```
1. Define parameter search space (ControlNet, IP-Adapter, LoRA strength, CFG, sampler, steps)
2. Modify ComfyUI workflow JSON programmatically
3. Submit to ComfyUI API
4. Wait for generation to complete
5. Score output with LPIPS + CLIP similarity
6. Bayesian optimization (optuna) selects next parameter set
7. Log results to CSV
8. Repeat overnight (~2-5 sec per image at 1024×1024 on RTX 5080)
```

### Parameter Search Space

| Parameter | Range | Type |
|-----------|-------|------|
| ControlNet strength | 0.3-1.0 | Continuous |
| IP-Adapter weight | 0.3-1.0 | Continuous |
| LoRA strength | 0.5-1.2 | Continuous |
| CFG scale | 3-12 | Continuous |
| Sampler | euler, euler_ancestral, dpmpp_2m, dpmpp_2m_sde, dpmpp_2s_ancestral | Categorical |
| Steps | 15-40 | Integer |

Keep seed fixed for direct comparison; vary for diversity testing.

### Scoring Metrics

| Metric | What It Measures | Library | Use |
|--------|------------------|---------|-----|
| **LPIPS** | Perceptual similarity (deep features) | `lpips` | Primary — style/perceptual consistency |
| **CLIP Similarity** | Semantic similarity between images | `transformers` (CLIP model) | Primary — character identity matching |
| **SSIM** | Structural similarity | `skimage.metrics` | Secondary — pixel-level consistency |
| Vision LLM | Subjective quality grading | Claude API or GPT-4V | Optional — batch grade 1-10 for "same artist/character" |

### ComfyUI API

ComfyUI exposes a REST API + WebSocket:

```python
# Queue a prompt
POST http://127.0.0.1:8188/prompt
Body: {"prompt": api_graph, "client_id": client_id}

# Get results
GET http://127.0.0.1:8188/history/{prompt_id}

# Download images
GET http://127.0.0.1:8188/view?filename=...&subfolder=...&type=...
```

**Workflow for programmatic access:**
1. Export ComfyUI workflow as API format JSON (Enable Dev Mode → Save API Format)
2. Load the JSON in Python
3. Modify parameters programmatically (node IDs → inputs)
4. Submit to ComfyUI API
5. Wait via WebSocket for completion
6. Download and evaluate results

### Python Libraries Needed

`requests` or `comfy_api_simplified`, `lpips`, `torch`, `transformers` (CLIP), `scikit-image` (SSIM), `optuna` (Bayesian optimization)

### Existing Resources

- **Sprite Sheet Diffusion** — Academic paper on sprite sheet generation using SD + ControlNet + IP-Adapter, with SSIM/PSNR/LPIPS evaluation scripts
- **ComfyUI_VNCCS** — Sprite Generator node for automating sprite sheet creation
- **2D Pixel Toolkit** and **Sprite Sheet Maker** — CivitAI LoRAs specifically for pixel art sprite generation

---

## Part 7: Troubleshooting Quick Reference

### Style LoRA Failure Modes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Style doesn't transfer | Too few steps, LR too low | Increase steps, raise LR |
| Characters look like training data | Overfitting | Reduce epochs, lower rank, increase dataset diversity |
| Colors/palettes wrong | Base model bias | Include color descriptions in captions, adjust noise_offset |
| Blurry/muddy output | Mixed quality in dataset | Ensure all images are crisp and high-res |
| LoRA only works at 1.0 | Undertrained | Increase steps or learning rate |
| LoRA breaks above 0.5 | Overtrained | Use an earlier epoch checkpoint |

### Overfitting Signs

- Generated images reproduce exact poses/compositions from training data
- Artifacts, glitches, or color banding
- LoRA only produces recognizable output at very specific strengths
- Decreasing diversity despite varied prompts

**Prevention**: Save checkpoints every 5 epochs. Compare with X/Y/Z plots. Keep network_dim at 32 or lower. Ensure dataset diversity.

### Underfitting Signs

- Output barely differs from base model
- Trigger word has minimal effect
- Style elements vague or inconsistent

**Fixes**: Double training steps. Increase LR (0.0005 → 0.001). Increase network_dim (16 → 32). Verify captions and dataset paths.

---

## Getting Started Checklist

### Phase 1: Environment Setup
- [ ] Update NVIDIA drivers to latest (570+)
- [ ] Watch RTX 5080 setup videos (links above)
- [ ] Clone kohya_ss — switch to **dev branch**
- [ ] Run `gui-uv.bat` (bundles correct PyTorch/CUDA)
- [ ] Verify: `python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"`
- [ ] Add training directories to Windows Defender exclusion list

### Phase 2: Dataset
- [ ] Gather 30-50 PNG images of your 16BitFit art style
- [ ] Upscale to 1024px+ using **nearest-neighbor only**
- [ ] Auto-caption with WD Tagger
- [ ] Prepend trigger word (`16bitfit_style`) to every caption
- [ ] Organize: `training_data/10_16bitfit_style/` with matched .png/.txt pairs

### Phase 3: Base Model
- [ ] Download Illustrious XL v0.1 from HuggingFace (`OnomaAIResearch/Illustrious-xl-early-release-v0`)

### Phase 4: Train
- [ ] Configure: Adafactor, fused backward pass, bf16, batch 1, grad accum 2, rank 32, alpha 32, LR 0.0005 (UNet only), cosine scheduler, 10 epochs, sample every 5 epochs
- [ ] Start training, monitor loss (~30-90 min)
- [ ] Review sample outputs at each checkpoint

### Phase 5: Test in ComfyUI
- [ ] Place .safetensors in `ComfyUI/models/loras/`
- [ ] Test with basic Load Checkpoint → Load LoRA → KSampler chain at 0.8 strength
- [ ] Run X/Y/Z plot: epoch checkpoints vs. LoRA strength to find sweet spot

### Phase 6: Build Sprite Pipeline
- [ ] Install ComfyUI_IPAdapter_plus, ControlNet Auxiliary Preprocessors, Comfyroll Custom Nodes
- [ ] Download ControlNet OpenPose model, IP-Adapter model, CLIP Vision model
- [ ] Build full workflow: LoRA + ControlNet + IP-Adapter
- [ ] Balance weights: ControlNet 0.5-0.8, IP-Adapter 0.5-0.8, LoRA 0.7-0.9

### Phase 7: Autoresearch Loop
- [ ] Export working ComfyUI workflow as API format JSON
- [ ] Build Python script: parameter search → ComfyUI API → LPIPS/CLIP scoring → optuna optimization
- [ ] Run overnight on Alienware
- [ ] Analyze results, lock in optimal parameters

---

## Sources

- kohya_ss GitHub issues: #3096 (main 5090 compat thread), #3332 (slow training), #3276 (xformers), #3296 (VRAM)
- Fooocus #3862 (sm_120 PyTorch fix)
- r/StableDiffusion: RTX 5090 upgrade reports, kohya_ss GPU utilization threads
- r/comfyui: LoRA training on 5080/5090 threads
- CivitAI: Illustrious XL, Pony Diffusion V6 XL model pages and training guides
- Karpathy autoresearch: github.com/karpathy/autoresearch
- Perplexity Computer research sessions (March 14, 2026)
