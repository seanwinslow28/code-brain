# ComfyUI LoRA Training Guide for Sprite & Animation Style Transfer

**Prepared for:** Sean Winslow — Product Manager, 16BitFit  
**Hardware:** Alienware Aurora Desktop, RTX 5080 16GB, Windows 11  
**Date:** March 2026

---

## Section 1: Training Framework Comparison

### Overview

Four major open-source frameworks support LoRA training for Stable Diffusion models. Each has different strengths for your RTX 5080 setup with 16GB VRAM.

### kohya_ss / sd-scripts (Recommended Primary)

**kohya_ss** (GUI by bmaltais, v0.9.1 sd-scripts) is the industry standard for SDXL LoRA training. CivitAI's entire training ecosystem is built around it, and it has the largest community and most extensive documentation.

- **SDXL VRAM**: Standard ~24GB, but with **fused backward pass** (bf16): **~10GB** — well within your 16GB
- **Windows**: Fully supported. RTX 5080 requires the **dev branch**, **CUDA 12.9.0**, and **cuDNN 9.10.1**. You must comment out DeepSpeed from requirements.txt. A video guide for RTX 5000-series setup is available.
- **Key features**: LoRA+, fused backward pass, block-wise training, alpha mask, optimizer groups, scheduled Huber loss, V-parameterization for SDXL
- **Known issues**: RTX 5000 series requires dev branch and manual CUDA/PyTorch version matching. bitsandbytes on Windows has historically caused CUDA errors — use the latest version (0.44.0+) or switch to AdamW/Adafactor if issues arise.

### ai-toolkit (by Ostris)

**ai-toolkit** (no versioned releases; use latest GitHub commit) is the go-to tool for **Flux.1** LoRA training, also used in HuggingFace tutorials.

- **Flux VRAM**: At least 24GB recommended, but with quantization: **NF4 ~9GB** fits your RTX 5080
- **Windows**: Supported with an easy install script by Tavris1
- **Key features**: Config-based YAML training, auto-bucketing/resizing, layer targeting, LoKr support, resumable checkpoints, sampling during training
- **Known issues**: Flux requires ~50GB system RAM for model quantization at startup. 16GB VRAM is tight for Flux and requires aggressive quantization.

### SimpleTuner

**SimpleTuner** (v3.0.1, Oct 2025) has the broadest model support across architectures, including SDXL, Flux.1, SD 3, Chroma, AuraFlow, PixArt Sigma, and many video models.

- **VRAM**: 16GB+ for medium models (2–8B LoRA), 24GB+ for large models (12B+)
- **Windows**: Not explicitly documented; primarily Linux-focused
- **Ease of setup**: Advanced — geared toward experienced users

### OneTrainer (Recommended Beginner Alternative)

**OneTrainer** (no versioned releases) is the most beginner-friendly option with a polished GUI, templates, and integrated dataset tools.

- **Windows**: Fully supported with install.bat, start-ui.bat, and update.bat
- **Key features**: GUI with templates (SDXL LoRA template), automatic backups, image augmentation, TensorBoard integration, built-in captioning (BLIP/BLIP2/WD-1.4), model format conversion UI
- **Community settings**: Prodigy optimizer, Cosine scheduler, ~100 epochs (1,500–2,600 steps), network rank 32, alpha 16

### Framework Comparison Table

| Feature | kohya_ss | ai-toolkit | SimpleTuner | OneTrainer |
|---|---|---|---|---|
| Best for | SDXL LoRA | Flux LoRA | Multi-model | Beginners |
| SDXL on 16GB | Yes (~10GB) | Less documented | Yes | Yes |
| Flux on 16GB | No | Yes (NF4 ~9GB) | Possible | Yes |
| Windows support | Full (dev branch) | Full | Unclear | Full |
| GUI | Yes | Web UI | No | Best GUI |
| Community size | Largest | Growing | Moderate | Active |

### TL;DR for Sean's Setup

Use **kohya_ss** (bmaltais GUI, dev branch) as your primary training tool for SDXL. With fused backward pass + bf16, SDXL LoRA training fits in ~10GB of your 16GB VRAM. Keep **OneTrainer** as a beginner-friendly backup. When you're ready for Flux, use **ai-toolkit** with NF4 quantization (~9GB VRAM).

---

## Section 2: Base Model Selection

### Why Base Model Choice Matters

LoRA training adapts a base model toward your target style. Starting from a base that already excels at 2D illustration means fewer training steps, better results, and less overfitting risk.

### Illustrious XL v0.1 (Recommended)

**Illustrious XL** (by OnomaAIResearch, v0.1 to v2.0) is a purpose-built SDXL finetune for anime and illustration output. It delivers cleaner line work, better color reproduction, and stronger prompt adherence than base SDXL 1.0.

- **Parameters**: 3.5 billion (SDXL architecture)
- **LoRA training**: Mature, well-documented. "Soaks concepts, art styles and characters like a sponge, usually around 500 steps gives great results"
- **Inference VRAM**: ~6–8GB
- **Cross-compatibility**: LoRAs trained on Illustrious also work on **NoobAI XL** (an Illustrious finetune)
- **v0.1** is the most commonly used version for LoRA training base (HuggingFace: OnomaAIResearch/Illustrious-xl-early-release-v0)

### Alternative SDXL Finetunes

**Pony Diffusion V6 XL**: Excellent for anime styles and character-centric work. Extensive LoRA ecosystem on CivitAI. Requires clip_skip=2 and >3,600 steps for style LoRAs. Good backup if you want broader anime community compatibility.

**NoobAI XL**: An Illustrious finetune with more stylistic range and improved composition. Cross-compatible with Illustrious LoRAs. Less popular but arguably better quality for some use cases.

**Animagine XL 3.1** (by cagliostrolab): Open-source anime model. Popular on CivitAI but less commonly used as a training base.

### Flux.1 Dev (Future Option)

**Flux.1 Dev** is a 12-billion-parameter model using flow matching architecture. It offers superior text rendering and better anatomy, but requires 24GB VRAM standard or ~9GB with NF4 quantization.

- **Licensing**: Flux.1-dev is non-commercial (requires HuggingFace token). Flux.1-schnell is Apache 2.0.
- **Flux 2 Klein 9B**: Smaller variant; community reports training on RTX 3060 (11GB) with ai-toolkit, but slow (~5 hours for 3,000 steps)
- **ComfyUI ecosystem**: Good support but ControlNet/IP-Adapter ecosystem is less mature than SDXL

### Models NOT Recommended

- **SDXL 1.0 base**: Too generic for illustration; always use a finetune
- **SD 3.5**: Limited community adoption for 2D illustration
- **SD 1.5**: Older architecture, lower resolution, smaller community going forward

### TL;DR for Sean's Setup

Start with **Illustrious XL v0.1** as your base model. Its flat illustration style aligns perfectly with 2D game art, and it requires fewer training steps than base SDXL. Download from HuggingFace (OnomaAIResearch/Illustrious-xl-early-release-v0). For Flux later, monitor **Flux 2 Klein 9B** as a 16GB-friendly alternative.

---

## Section 3: Dataset Preparation

### Image Count and Quality

- **Minimum viable**: 15–20 images
- **Recommended for style LoRAs**: 30–50 images
- **Ideal**: 50–100 images for complex styles with variation
- More important than quantity: **diversity of poses, compositions, and subjects** within a consistent style
- Avoid same subject repeatedly; avoid mixing significantly different styles

### Resolution Requirements

- **SDXL minimum**: 1024×1024, ideally up to 2048×2048
- **Native training resolution**: 1024×1024
- If images are below 1024px, upscale to at least 1024 — but see pixel art exception below
- **Aspect ratios** don't need to be 1:1; aspect ratio bucketing handles mixed ratios automatically

### Aspect Ratio Bucketing

Training frameworks (kohya_ss, OneTrainer) automatically group images into resolution "buckets" (e.g., 1024×1024, 1152×896, 768×1344) with **bucket_reso_steps=64**. No manual square cropping needed.

- **bucket_no_upscale**: Enable this to prevent upscaling smaller images; they'll be placed in smaller buckets
- **cache_latents** + **cache_latents_to_disk**: Precompute and cache latent representations for faster training and lower VRAM

### Captioning Strategy for Style LoRAs

**Trigger word**: Choose a unique alphanumeric token, e.g., `16bitfit_style` or `seanart_style`

**Caption formula**: `[trigger_word], [medium/style keywords], [content description]`

Example: `16bitfit_style, pixel art, retro game boy style, a warrior character standing in idle pose`

**Key principle**: Caption everything that ISN'T part of the style you want learned. Describe subjects, poses, and backgrounds — the model learns the style from what's left unspecified.

**Turn off text encoder training** for style LoRAs (set text_encoder_lr to 0). This forces the model to learn style from the UNet only.

### Auto-Captioning Tools

| Tool | Type | VRAM | Best For |
|---|---|---|---|
| **JoyCaption** | Natural language | ~17GB (4-bit quantized for smaller GPUs) | Flux models, detailed descriptions |
| **WD Tagger** (WD-1.4) | Tag-based | Low | SDXL/Illustrious, fast tagging |
| **Florence-2** | General tagging | Low | High-speed general tags |
| **BLIP/BLIP2** | Natural language | Moderate | Built into OneTrainer |

For SDXL/Illustrious training, **WD Tagger** with tag-style captions works well. For Flux training later, switch to **JoyCaption** for natural language captions.

### Regularization Images

**For style LoRAs: generally not needed.** Regularization images help prevent concept "leaking" for subject/character LoRAs, but for styles they add complexity without much benefit. Community consensus: "you can completely exclude regularization images and train almost everything just fine."

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

- **Images**: PNG format (mandatory for pixel art — JPEG compression destroys pixel clarity)
- **Captions**: .txt files with the same filename as the corresponding image
- **Repeats**: The number prefix (e.g., `10_16bitfit_style`) controls how many times each image is seen per epoch
- **Formula**: total_steps = (num_images × repeats × epochs) / batch_size

### Pixel Art & Flat 2D Illustration Tips

- **Use PNG format only** — JPEG compression artifacts destroy pixel art clarity
- **Do NOT upscale pixel art with standard upscalers** — they blur pixels. Use nearest-neighbor upscaling to maintain crisp pixels
- **Include style keywords in captions**: "pixel art", "limited color palette", "clean outlines", "flat shading", "retro game style", "game boy aesthetic"
- **Describe what makes your style unique**: color count, line thickness, shading approach
- **Do not mix pixel art with non-pixel-art images** — style consistency is critical
- **Crop characters on clean/transparent backgrounds** where possible to help the model learn character style without conflating it with backgrounds

### TL;DR for Sean's Setup

Gather 30–50 PNG images of your 16BitFit art style at 1024px+. Use nearest-neighbor upscaling only. Caption each with `16bitfit_style, pixel art, retro game boy style, [description]`. Use WD Tagger for fast auto-captioning, then prepend your trigger word. Organize as `training_data/10_16bitfit_style/` with matched .png and .txt files. Skip regularization images.

---

## Section 4: Training Configuration

### Recommended Settings for RTX 5080 (16GB) — SDXL LoRA with kohya_ss

#### Core Settings

| Parameter | Value | Why |
|---|---|---|
| **Batch size** | 1 | 16GB requires batch 1 |
| **Gradient accumulation steps** | 2 | Simulates batch size of 2 |
| **Gradient checkpointing** | Enabled | Required for 16GB |
| **Mixed precision** | bf16 | RTX 5080 supports bf16 natively |
| **Fused backward pass** | Enabled | Reduces VRAM from ~24GB to ~10GB with bf16 |
| **Cache latents to disk** | Enabled | Saves VRAM during training |

#### Network Architecture

| Parameter | Value | Notes |
|---|---|---|
| **LoRA rank (network_dim)** | 32 | Sweet spot for style LoRAs (~20–40MB file) |
| **Network alpha** | 32 | Same as rank for 1.0 scaling |
| **Network type** | networks.lora | Standard LoRA |

#### Optimizer Selection

| Optimizer | Learning Rate | Pros | Cons | Best For |
|---|---|---|---|---|
| **Adafactor** | 0.0005 | Required for fused backward pass; memory efficient | Slightly different convergence | 16GB VRAM (pairs with fused pass) |
| **Prodigy** | 1.0 (auto-adjusts) | Auto learning rate; hard to overfit | Slower convergence; memory overhead | Beginners (set and forget) |
| **AdamW8bit** | 0.0005 (UNet) | Reliable; well-tested | Need to tune LR manually | Experienced users |

**Recommended for your setup**: **Adafactor** with fused backward pass — this is the only way to get SDXL training into ~10GB VRAM.

#### Training Duration (for 30–50 images)

| Parameter | Value |
|---|---|
| **Repeats** | 10–15 |
| **Epochs** | 10 |
| **Total steps** | ~1,500–3,000 |
| **Expected time** | 30–90 minutes on RTX 5080 |
| **LR scheduler** | cosine or cosine_with_restarts |
| **Min SNR gamma** | 5 |
| **Noise offset** | 0.03 (start low for pixel art) |

#### Text Encoder Settings (Style LoRAs)

| Parameter | Value | Why |
|---|---|---|
| **text_encoder_lr** | 0 | Train UNet only for style |
| **network_train_unet_only** | True | Skip text encoder entirely |
| **clip_skip** | 1 (Illustrious) or 2 (Pony) | Base-model dependent |

### Network Rank Guide

| Rank | File Size | Best For | Risk |
|---|---|---|---|
| 16 | ~10–20MB | Simple flat styles | May miss nuance |
| 32 | ~20–40MB | Most style LoRAs (recommended) | Balanced |
| 64 | ~40–80MB | Complex styles with lots of variation | Overfitting with small datasets |
| 128 | ~80–150MB | Very complex adaptations | Overkill for most styles |

### VRAM Troubleshooting Ladder

If you hit VRAM errors, apply these fixes in order:

1. Enable **fused_backward_pass** + **Adafactor** (~10GB)
2. Reduce resolution to 768×768
3. Reduce network_dim from 32 to 16
4. Enable **cache_latents_to_disk**
5. Last resort: Use **optimizer_groups=8** (~14GB)

### Validation During Training

- **sample_every_n_epochs**: 5 — generates a test image every 5 epochs
- **save_every_n_epochs**: 5 — saves a checkpoint every 5 epochs for comparison
- Create a `sample_prompts.txt` with 2–3 test prompts including your trigger word
- Use **X/Y/Z plot** in ComfyUI afterward to compare epochs vs. LoRA strength
- Watch training loss: Should decrease gradually (~0.08–0.12 typical range for SDXL). Plateaus early → LR too low. Spikes → LR too high.

### What a Training Run Looks Like

1. **Loading** (5–10 min): Model loads, latents cache to disk
2. **Training**: Steps execute, loss displayed per step
3. **Sampling**: Preview images generate at intervals
4. **Completion**: Final LoRA saved as .safetensors file
5. **Total wall time**: 30–90 minutes for a typical style LoRA

### TL;DR for Sean's Setup

Use **Adafactor** optimizer with **fused backward pass** and **bf16** — this fits SDXL training in ~10GB of your 16GB. Set rank 32, alpha 32, batch 1, gradient accumulation 2, cosine scheduler, 10 epochs with 10–15 repeats. Train UNet only (text_encoder_lr=0). Save checkpoints every 5 epochs. Expected training time: 30–90 minutes.

---

## Section 5: ComfyUI Integration

### Loading Your Trained LoRA

Place your trained `.safetensors` file in:
```
ComfyUI/models/loras/
```
Restart ComfyUI or refresh the model list.

### Basic LoRA Workflow

Node chain:

1. **Load Checkpoint** → Select your base model (Illustrious XL)
2. **Load LoRA** → Connect MODEL and CLIP outputs from checkpoint
3. **CLIP Text Encode** → Positive prompt (include trigger word) and negative prompt
4. **KSampler** → Generate
5. **VAE Decode** → **Save Image**

### LoRA Weight Ranges

| Strength | Effect |
|---|---|
| 0.5–0.7 | Subtle style influence, blends with base |
| 0.7–0.9 | Recommended starting range |
| 0.9–1.0 | Strong style, may override base characteristics |
| 1.0+ | Very strong — test carefully, can cause artifacts |

Start at **0.8** and adjust up/down.

### Full Sprite Pipeline: LoRA + ControlNet + IP-Adapter

This workflow combines your style LoRA with pose control and character reference consistency.

**Required custom nodes:**

- **ComfyUI Manager** — Essential for installing/updating all other nodes
- **ComfyUI_IPAdapter_plus** (by cubiq) — In "maintenance only" mode since April 2025 but still functional
- **ComfyUI ControlNet Auxiliary Preprocessors** (comfyui_controlnet_aux)
- **ComfyUI_Comfyroll_CustomNodes** (by Suzie1) — LoRA stacks, multi-ControlNet

**Required models:**

- ControlNet: SDXL-compatible OpenPose or depth map model
- IP-Adapter: ip-adapter-plus_sdxl_vit-h.bin
- CLIP Vision: CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors

**Workflow:**

```
Input: Reference character image + Pose skeleton image

[Load Checkpoint] → Illustrious XL
       ↓
[Load LoRA] → Your trained style LoRA (strength 0.7–0.9)
       ↓
[IPAdapter Model Loader] + [Load CLIP Vision] + [Load Image (reference)]
       ↓
[IPAdapter Advanced] → Feeds modified model with reference style
       ↓
[ControlNet Loader] + [Load Image (pose skeleton)]
       ↓
[Apply ControlNet] → Applies pose control
       ↓
[CLIP Text Encode] → Positive (with trigger word) + Negative prompts
       ↓
[KSampler] → Generates image matching style + pose
       ↓
[VAE Decode] → [Save Image]
```

### Balancing Three Controls

| Control | Range | If too strong | If too weak |
|---|---|---|---|
| **ControlNet** | 0.5–0.8 | Output too rigid | Pose drifts |
| **IP-Adapter** | 0.5–0.8 | Over-copies reference | Character features drift |
| **LoRA** | 0.7–0.9 | Artifacts/overtrained look | Style inconsistent |

### Advanced: LoRA Masking and Scheduling

ComfyUI's December 2024 update added native LoRA scheduling:

- **Create Hook LoRA**: Apply LoRA to specific conditioning regions
- **Hook Keyframes**: Schedule LoRA strength across sampling steps — useful for varying style influence at different denoising stages

### Additional Useful Nodes

- **Efficiency Nodes**: KSampler (Efficient) for better performance
- **ComfyUI_VNCCS**: Sprite Generator node for automating sprite sheet creation

### TL;DR for Sean's Setup

Place your .safetensors in `ComfyUI/models/loras/`. Start with the basic Load Checkpoint → Load LoRA → KSampler chain at strength 0.8. For the full sprite pipeline, install **ComfyUI_IPAdapter_plus**, **ControlNet Auxiliary Preprocessors**, and **Comfyroll Custom Nodes**. Balance ControlNet (0.5–0.8), IP-Adapter (0.5–0.8), and LoRA (0.7–0.9) for consistent character sprites across poses.

---

## Section 6: Automated Sprite Optimization (Autoresearch Pattern)

### The Concept

Andrej Karpathy's **autoresearch** pattern describes an AI agent that autonomously edits parameters, runs fixed-budget experiments, evaluates against a metric, keeps improvements, and discards failures. You can adapt this to optimize your ComfyUI sprite generation pipeline.

### Core Loop

1. Define parameter search space
2. Modify ComfyUI workflow parameters programmatically
3. Run generation via ComfyUI API
4. Evaluate output against consistency metrics
5. Keep improvements, discard failures
6. Repeat autonomously (overnight on your RTX 5080)

### Parameters to Optimize

| Parameter | Search Range |
|---|---|
| ControlNet strength | 0.3–1.0 |
| IP-Adapter weight | 0.3–1.0 |
| LoRA strength | 0.5–1.2 |
| CFG scale | 3–12 |
| Sampler | euler, euler_ancestral, dpmpp_2m, dpmpp_2m_sde, dpmpp_2s_ancestral |
| Steps | 15–40 |
| Denoising strength | Variable |

Keep seed fixed for direct comparison; vary for diversity testing.

### Sprite Consistency Metrics

| Metric | What It Measures | Library | Best For |
|---|---|---|---|
| **LPIPS** | Perceptual similarity (deep features) | lpips (pip install) | Style/perceptual consistency |
| **CLIP Similarity** | Semantic similarity between images | transformers (CLIP model) | Character identity matching |
| **SSIM** | Structural similarity | skimage.metrics | Pixel-level consistency |
| **Subject Consistency** | Cross-frame identity | vbench library | Character across poses |
| **PSNR** | Pixel-wise difference | skimage.metrics | Raw pixel accuracy |

**Recommended approach**: Primary: **LPIPS** + **CLIP Similarity**. Secondary: **SSIM** for structural checks. Optional: Use a vision LLM (e.g., Claude or GPT-4V) to grade batches 1–10 for "looks like same artist/character."

### ComfyUI API for Batch Generation

ComfyUI exposes a REST API + WebSocket interface:

```python
# Queue a prompt
POST http://127.0.0.1:8188/prompt
Body: {"prompt": api_graph, "client_id": client_id}

# Get results
GET http://127.0.0.1:8188/history/{prompt_id}

# Download images
GET http://127.0.0.1:8188/view?filename=...&subfolder=...&type=...
```

**Python workflow:**
1. Export your ComfyUI workflow as API format JSON (Enable Dev Mode → Save API Format)
2. Load the JSON in Python
3. Modify parameters programmatically (node IDs → inputs)
4. Submit to ComfyUI API
5. Wait via WebSocket for completion
6. Download and evaluate results

The Cohorte production playbook provides production-grade Python code for this pattern.

### Building the Optimization Loop

```
1. Define search space (parameter ranges)
2. Write evaluation function (LPIPS + CLIP similarity)
3. Use ComfyUI API to generate batches
4. Score each batch
5. Bayesian optimization (optuna) or grid search
6. Log results to CSV/JSON
7. Run overnight (~2–5 sec per image at 1024×1024 on RTX 5080)
```

**Python libraries needed**: requests or comfy_api_simplified, lpips, torch, transformers (CLIP), scikit-image (SSIM), optuna (Bayesian optimization)

### Existing Resources

- **Sprite Sheet Diffusion** — Academic paper on sprite sheet generation using SD + ControlNet + IP-Adapter, with SSIM/PSNR/LPIPS evaluation scripts
- **ComfyUI_VNCCS** — Sprite Generator node for automating sprite sheet creation
- **2D Pixel Toolkit** and **Sprite Sheet Maker** — CivitAI LoRAs specifically for pixel art sprite generation

### TL;DR for Sean's Setup

Use ComfyUI's API to batch-generate sprites with different parameter combinations. Score them with **LPIPS** + **CLIP Similarity** for perceptual and semantic consistency. Use **optuna** for Bayesian optimization. Your RTX 5080 generates ~2–5 sec per image at 1024×1024, so an overnight run can test hundreds of combinations. Start with the Cohorte production playbook for production-grade API code.

---

## Section 7: Common Pitfalls & Troubleshooting

### Style LoRA Failure Modes

| Problem | Likely Cause | Fix |
|---|---|---|
| Style doesn't transfer | Too few steps, LR too low, or text encoder stealing UNet capacity | Increase steps, raise LR, set text_encoder_lr=0 |
| Characters look like training data | Overfitting | Reduce epochs, lower rank, increase dataset diversity |
| Colors/palettes wrong | Base model bias | Include color descriptions in captions, adjust noise_offset |
| Blurry/muddy output | Mixed quality in dataset | Ensure all images are crisp and high-res |
| LoRA only works at 1.0 | Undertrained | Increase steps or learning rate |
| LoRA breaks above 0.5 | Overtrained | Use an earlier epoch checkpoint |

### Overfitting Signs and Prevention

**Signs:**
- Generated images reproduce exact poses/compositions from training data
- Artifacts, glitches, or color banding appear
- LoRA only produces recognizable output at very specific strengths
- Decreasing diversity despite varied prompts

**Prevention:**
- Use **Prodigy** optimizer (auto-adjusts LR)
- Save checkpoints every 5–10 epochs and compare
- Use X/Y/Z plotting to find the sweet spot
- Keep **network_dim at 32 or lower** for style LoRAs
- Ensure dataset diversity (different subjects in your art style)

### Underfitting Signs and Fixes

**Signs:**
- Output barely differs from base model
- Trigger word has minimal effect
- Style elements are vague or inconsistent

**Fixes:**
- Double your training steps/epochs
- Increase learning rate (e.g., 5e-4 → 1e-3; for Prodigy try 1.5)
- Increase network_dim (16 → 32)
- Verify captions are correct and trigger word is consistently placed
- Check that image files are actually loading (verify dataset paths)

### VRAM Optimization Checklist for RTX 5080

1. **Fused backward pass** (Adafactor only): ~10GB for SDXL
2. **cache_latents_to_disk**: Offloads latent cache to SSD
3. **Gradient checkpointing**: Trades compute for memory
4. **bf16 mixed precision**: Native on RTX 5080
5. **batch_size=1** with gradient_accumulation_steps=2
6. **xformers or torch SDPA**: Memory-efficient attention
7. **Close other GPU applications** during training (ComfyUI, browsers, etc.)

### Windows-Specific Issues

1. **bitsandbytes CUDA errors**: The #1 Windows issue historically. Use latest bitsandbytes (0.44.0+). If errors persist, switch to Adafactor or standard AdamW (not 8-bit variants).

2. **RTX 5000 series compatibility**: Requires **CUDA 12.9+**, **cuDNN 9.10.1+**, **PyTorch 2.5+**. Use kohya_ss **dev branch**. Comment out DeepSpeed from requirements.txt.

3. **Path length issues**: Windows has a 260-character path limit. Keep training directory paths short.

4. **CUDA/PyTorch version mismatch**: Verify with:
   ```
   python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"
   ```

5. **Memory leaks**: Some training runs accumulate memory. Monitor with `nvidia-smi`. Restart if VRAM usage climbs unexpectedly.

6. **Antivirus interference**: Windows Defender can slow file I/O during training. Add ComfyUI and training directories to the exclusion list.

### TL;DR for Sean's Setup

The most common issues you'll face: bitsandbytes CUDA errors (fix: use Adafactor instead), RTX 5080 requiring dev branch + CUDA 12.9 (fix: follow the video guide), and overfitting (fix: save checkpoints every 5 epochs, use X/Y/Z plots). Always verify your CUDA setup first with the torch.cuda.is_available() check. Add your training folders to Windows Defender exclusions.

---

## Getting Started Checklist

1. **Install prerequisites**: CUDA 12.9.0, cuDNN 9.10.1, Python 3.10–3.12, Git, Visual Studio C++ Redistributable
2. **Clone kohya_ss** (bmaltais GUI) — switch to dev branch
3. **Set up environment**: Comment out DeepSpeed from requirements.txt, run setup.bat, configure Accelerate for bf16
4. **Download base model**: Illustrious XL v0.1 from HuggingFace (OnomaAIResearch/Illustrious-xl-early-release-v0)
5. **Prepare dataset**: 30–50 PNG images of your art style, 1024px+ resolution
6. **Caption images**: Use WD Tagger or JoyCaption, prepend trigger word (`16bitfit_style`)
7. **Organize folder**: `training_data/10_16bitfit_style/` with matched image + caption pairs
8. **Configure training**: Adafactor, fused backward pass, bf16, batch 1, grad accum 2, rank 32, alpha 32, LR 0.0005 (UNet only), cosine scheduler, 10 epochs, sample every 5 epochs
9. **Start training**: Monitor loss, check sample previews (~30–90 min)
10. **Test in ComfyUI**: Load Checkpoint → Load LoRA (strength 0.8) → generate test images
11. **Find optimal settings**: X/Y/Z plot varying epoch checkpoints vs. LoRA strength
12. **Build sprite pipeline**: Add ControlNet (OpenPose) + IP-Adapter to workflow
13. **Iterate and automate**: Build autoresearch loop for parameter optimization
