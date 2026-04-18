# LoRA Training Runbook — 16BitFit Sprite Style

**Target machine:** Alienware RTX 5080 (192.168.68.201)
**Expected VRAM:** ~10GB with Adafactor + gradient checkpointing + fused backward pass
**Expected training time:** 30-90 minutes for 10 epochs (30-50 images, 10 repeats)

---

## Prerequisites

### 1. Download Base Model (Illustrious XL v0.1)

```powershell
# On Alienware — download once
pip install huggingface-hub
huggingface-cli download OnomaAIResearch/Illustrious-xl-early-release-v0 --local-dir C:\Users\seanw\Documents\Code-Brain\models\illustriousXL_v01
# Or download the single safetensors file:
huggingface-cli download OnomaAIResearch/Illustrious-xl-early-release-v0 illustrious-xl-v0.1.safetensors --local-dir C:\Users\seanw\Documents\Code-Brain\models
```

### 2. Install kohya_ss (Dev Branch)

```powershell
cd C:\Users\seanw\Documents\Code-Brain
git clone -b dev https://github.com/bmaltais/kohya_ss.git
cd kohya_ss

# Use gui-uv.bat — it bundles the correct PyTorch/CUDA versions automatically
gui-uv.bat
```

**CRITICAL:** Use the `dev` branch. The stable branch does NOT support RTX 5080 (sm_120).

### 3. Verify GPU and PyTorch

```powershell
cd C:\Users\seanw\Documents\Code-Brain\kohya_ss
# Activate the venv that gui-uv.bat created
.venv\Scripts\activate

python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0)}'); print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f}GB')"
```

Expected output:
```
CUDA available: True
CUDA version: 12.8+ (or 13.0)
GPU: NVIDIA GeForce RTX 5080
VRAM: 16.0GB
```

### 4. Verify SDPA (NOT xformers)

```powershell
python -c "import torch; print('xformers' in dir(torch)); print(torch.backends.cuda.flash_sdp_enabled())"
```

Expected: `False` (no xformers), `True` (SDPA enabled). If xformers is installed, uninstall it:
```powershell
pip uninstall xformers
```

---

## Prepare Dataset

### 5. Collect Source Images

Gather 30-50 PNG images of the target art style:
- SF2-style pixel art fighting game characters
- Various poses: idle, walk, attack, block, crouch, jump, hit, victory, defeat
- Clean backgrounds (transparent or solid green)
- Original resolution (typically 128×128 or 256×256)

Place them in a flat directory, e.g.:
```
C:\Users\seanw\Documents\Code-Brain\lora-training\source-sprites\
  idle_001.png
  walk_001.png
  punch_001.png
  ...
```

### 6. Run Dataset Preparation Script

From the MacBook Pro (where the dataset prep script lives):

```bash
# Copy source sprites to the dataset prep input directory first
# Then run:
cd 16bitfit-battle-mode/lora-training
python3 prepare_dataset.py \
  --input ./source-sprites \
  --output ./dataset/10_16bitfit_style \
  --target-size 1024
```

This will:
- Nearest-neighbor upscale all PNGs to 1024×1024 (sharp pixels, no blur)
- Generate matching `.txt` caption files with the `16bitfit_style` trigger word
- Validate all output images

### 7. Copy Dataset to Alienware

```bash
# From MacBook Pro
scp -r 16bitfit-battle-mode/lora-training/dataset seanw@192.168.68.201:C:/Users/seanw/Documents/Code-Brain/lora-training/
```

Or use the shared Google Drive folder if available.

---

## Train

### 8. Launch Training

```powershell
cd C:\Users\seanw\Documents\Code-Brain\kohya_ss
.venv\Scripts\activate

# Using the config TOML from this repo:
accelerate launch --num_cpu_threads_per_process 1 sdxl_train_network.py --config_file "C:\Users\seanw\Documents\Code-Brain\lora-training\sprite-style-config.toml"
```

**Alternative — using kohya_ss GUI:**
1. Run `gui-uv.bat`
2. Open browser to `localhost:7860`
3. Go to LoRA tab
4. Load the config TOML via the config file field
5. Click Start Training

### 9. Monitor Training

Watch the terminal for:
- **Loss values:** Should decrease gradually (typical range: 0.08-0.12 for SDXL)
- **Loss plateaus early:** LR too low → increase to 0.001
- **Loss spikes:** LR too high → decrease to 0.0003
- **Sample images:** Generated every 5 epochs — check for style convergence

GPU monitoring:
```powershell
# In a separate terminal
nvidia-smi -l 2
```

Expected during training:
- GPU utilization: 80-100%
- VRAM usage: ~10GB (with fused backward pass)
- GPU temp: 65-80°C
- s/it: 0.5-1.5s per step

### 10. Expected Checkpoints

Checkpoints saved at epochs 5 and 10:
```
C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\
  16bitfit_sprite_style-000005.safetensors  (~20-40MB)
  16bitfit_sprite_style-000010.safetensors  (~20-40MB)
  sample\                                  (sample images)
  logs\                                    (tensorboard logs)
```

---

## Test in ComfyUI

### 11. Copy LoRA to ComfyUI

```powershell
copy "C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\16bitfit_sprite_style-000010.safetensors" "C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\"
```

Restart ComfyUI or refresh the model list.

### 12. Basic Test Workflow

In ComfyUI:
1. Load Checkpoint → Illustrious XL (v2.0-STABLE or v3.x for inference)
2. Load LoRA → `16bitfit_sprite_style-000010.safetensors` (strength: 0.8)
3. CLIP Text Encode → Positive: `16bitfit_style, pixel art fighter, idle stance, bold outlines`
4. CLIP Text Encode → Negative: `blurry, anti-aliased, gradient, low quality`
5. KSampler → 28 steps, CFG 7, euler sampler
6. VAE Decode → Save Image

### 13. X/Y/Z Plot for Optimal Settings

Use the `XY Plot` node to compare:
- **X axis:** Epoch checkpoints (5 vs 10)
- **Y axis:** LoRA strength (0.5, 0.7, 0.8, 0.9, 1.0)

This finds the sweet spot where style transfers cleanly without artifacts.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `cutlassF: no kernel found` | xformers installed | `pip uninstall xformers` — use SDPA |
| OOM / CUDA out of memory | VRAM exceeded | Reduce batch size to 1, ensure `fused_backward_pass = true` |
| Very slow training (>3s/step) | Wrong optimizer or driver issue | Use Adafactor, update NVIDIA drivers |
| GPU at 100% but 40°C | Power management issue | Update to latest Game Ready/Studio driver |
| `bitsandbytes` errors | Windows DLL issues | Use Adafactor instead (not 8-bit Adam) |
| Loss doesn't decrease | LR too low | Increase to 0.001. Verify dataset captions. |
| Generated images = exact training data | Overfitting | Use earlier epoch checkpoint, reduce rank to 16 |
| Style barely visible | Undertrained | Double epochs. Try LR 0.001. Increase rank to 64. |
| Path length errors | Windows 260-char limit | Keep paths short: `C:\lora-training\` |

---

## File Paths Quick Reference

| What | Path on Alienware |
|------|-------------------|
| kohya_ss | `C:\Users\seanw\Documents\Code-Brain\kohya_ss\` |
| Base model | `C:\Users\seanw\Documents\Code-Brain\models\illustriousXL_v01.safetensors` |
| Training config | `C:\Users\seanw\Documents\Code-Brain\lora-training\sprite-style-config.toml` |
| Dataset | `C:\Users\seanw\Documents\Code-Brain\lora-training\dataset\10_16bitfit_style\` |
| Output LoRA | `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\` |
| ComfyUI loras | `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\` |
| Sample prompts | `C:\Users\seanw\Documents\Code-Brain\lora-training\sample_prompts.txt` |

---

## Models to Download on Alienware

- [ ] **Illustrious XL v0.1** — `OnomaAIResearch/Illustrious-xl-early-release-v0` from HuggingFace (~6.5GB)
- [ ] **kohya_ss dev branch** — `git clone -b dev https://github.com/bmaltais/kohya_ss.git`
- [ ] For inference: **Illustrious XL v2.0-STABLE** or **v3.x** (LoRAs trained on v0.1 work across versions)
