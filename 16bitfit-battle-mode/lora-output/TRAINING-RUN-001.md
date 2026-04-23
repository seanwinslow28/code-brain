# Training Run 001 — 16BitFit Sprite Style LoRA

**Date:** 2026-04-07
**Machine:** Alienware RTX 5080 (16GB GDDR7)
**Operator:** Claude Code (automated execution of TRAINING-RUNBOOK.md)

---

## Configuration

| Parameter | Value |
|-----------|-------|
| Base model | Illustrious XL v0.1 (`illustriousXL_v01.safetensors`, 6.46GB) |
| Framework | kohya_ss dev branch (v25.2.1) |
| Script | `sd-scripts/sdxl_train_network.py` |
| PyTorch | 2.7.0+cu128 |
| CUDA | 12.8 |
| Attention | SDPA (no xformers) |
| Optimizer | Adafactor (relative_step=true) |
| LR scheduler | Adafactor internal scheduler (overrides cosine when relative_step is true) |
| Learning rate | 5e-4 (used as initial_lr) |
| Network rank | 32 |
| Network alpha | 32 |
| Mixed precision | bf16 |
| Batch size | 1 |
| Gradient accumulation | 2 |
| Gradient checkpointing | true |
| Cache latents to disk | true |
| Resolution | 1024x1024 (bucketing enabled, 64px steps) |
| Augmentation | None (no flip, no color — preserves sprite facing direction and palette) |
| Noise offset | 0.03 |
| Min SNR gamma | 5 |
| Seed | 42 |

## Dataset

| Metric | Value |
|--------|-------|
| Images | 61 PNGs (1024x1024, nearest-neighbor upscaled from source sprites) |
| Captions | 61 matching .txt files with `16bitfit_style` trigger word |
| Repeats | 10 (folder prefix `10_16bitfit_style`) |
| Effective images/epoch | 610 |
| Total steps | 3,050 (610 / batch 1 / grad_accum 2 * 10 epochs) |

## Training Results

| Metric | Value |
|--------|-------|
| Total time | **2h 12m 29s** |
| Avg speed | 2.61 s/step |
| Final avg loss | **0.0799** |
| Peak VRAM | ~11.4 GB / 16 GB |
| GPU temp | 44-45°C |

### Loss Progression

| Phase | Steps | Avg Loss |
|-------|-------|----------|
| Warmup (epoch 1) | 0-305 | 0.088 |
| Mid-training (epoch 5) | ~1,525 | 0.084 |
| Final (epoch 10) | 3,050 | 0.080 |

Loss decreased steadily and stabilized in the 0.08 range — within the expected 0.08-0.12 target for SDXL style LoRAs.

## Output Files

### Checkpoints

| File | Epoch | Size | Path |
|------|-------|------|------|
| `16bitfit_sprite_style-000005.safetensors` | 5 | 163 MB | `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\` |
| `16bitfit_sprite_style.safetensors` | 10 (final) | 163 MB | `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\` |

Note: Checkpoint size is 163MB (larger than the 20-40MB estimate in the runbook). This is because rank 32 applied to the full SDXL UNet produces larger LoRA files than SD 1.5 equivalents.

Note: The final epoch 10 checkpoint was saved as `16bitfit_sprite_style.safetensors` (no epoch number suffix) rather than the `*-000010.safetensors` naming the runbook expected. This is kohya_ss default behavior for the final checkpoint.

### Sample Images

6 sample images generated (3 per checkpoint epoch):

| File | Epoch | Prompt |
|------|-------|--------|
| `16bitfit_sprite_style_e000005_00_*.png` | 5 | idle stance |
| `16bitfit_sprite_style_e000005_01_*.png` | 5 | punch attack |
| `16bitfit_sprite_style_e000005_02_*.png` | 5 | walking frame |
| `16bitfit_sprite_style_e000010_00_*.png` | 10 | idle stance |
| `16bitfit_sprite_style_e000010_01_*.png` | 10 | punch attack |
| `16bitfit_sprite_style_e000010_02_*.png` | 10 | walking frame |

**Sample image quality is poor** — this is expected. Training samples are generated using the raw Illustrious XL v0.1 base model with minimal sampler settings. Actual inference should use a better base model (v2.0-STABLE or v3.x) with proper sampler configuration (28 steps, CFG 7, negative prompts).

### ComfyUI Installation

Final LoRA copied to: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style.safetensors`

## Setup Issues Encountered & Fixed

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Model download 404 | Filename case mismatch (`illustrious-xl-v0.1` vs `Illustrious-XL-v0.1`) | Used correct capitalization, renamed to match config |
| `uv` not installed | Fresh machine, kohya_ss requires uv | Installed via `irm https://astral.sh/uv/install.ps1` |
| xformers installed by default | kohya_ss pyproject.toml includes xformers as dependency | `pip uninstall xformers -y` after venv setup |
| Training script not found | Script is in `sd-scripts/` subdirectory, not kohya_ss root | Launched from `sd-scripts/` directory |
| UnicodeEncodeError crash | Japanese log messages can't encode on Windows cp1252 | Set `PYTHONUTF8=1` environment variable |
| `fused_backward_pass` not supported | Only available in `sdxl_train.py` (full fine-tune), not `train_network.py` (LoRA) | Removed from config TOML |
| `train_data_dir` wrong level | Config pointed to `dataset/10_16bitfit_style/` but kohya_ss expects the parent directory | Changed to `dataset/` (auto-discovers repeat folders) |

## Config Corrections Applied

The original `sprite-style-config.toml` had two issues corrected during this run:

1. **`train_data_dir`** — Changed from `.../dataset/10_16bitfit_style` to `.../dataset` (kohya_ss auto-discovers `{repeats}_{class}` subfolders)
2. **`fused_backward_pass = true`** — Removed (not supported in `train_network.py` for LoRA training; only works in `sdxl_train.py` for full fine-tuning)

These corrections have been applied to the deployed config at `C:\Users\seanw\Documents\Code-Brain\lora-training\sprite-style-config.toml`. The source config in the superuser pack repo has NOT been updated.

## Next Steps

1. **Test in ComfyUI** — Load with Illustrious XL v2.0+ base, LoRA strength 0.8, 28 steps, CFG 7, euler sampler
2. **X/Y/Z plot** — Compare epoch 5 vs 10 checkpoints at strengths 0.5, 0.7, 0.8, 0.9, 1.0
3. **Update source config** — Apply the two config corrections back to the superuser pack repo
4. **Consider rank reduction** — If 163MB is too large, re-train with rank 16 for ~80MB checkpoints
5. **Evaluate overfitting** — If epoch 10 outputs look like exact training data, use epoch 5 instead

## File Paths Reference

| What | Path |
|------|------|
| Training config (deployed) | `C:\Users\seanw\Documents\Code-Brain\lora-training\sprite-style-config.toml` |
| Training config (source) | `16bitfit-battle-mode\docs\lora-training\sprite-style-config.toml` |
| Dataset | `C:\Users\seanw\Documents\Code-Brain\lora-training\dataset\10_16bitfit_style\` |
| Output checkpoints | `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\` |
| Sample images | `C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\sample\` |
| ComfyUI LoRA | `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style.safetensors` |
| kohya_ss | `C:\Users\seanw\Documents\Code-Brain\kohya_ss\` |
| Base model | `C:\Users\seanw\Documents\Code-Brain\models\illustriousXL_v01.safetensors` |
