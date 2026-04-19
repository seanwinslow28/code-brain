I have all the research data. Now let me synthesize and deliver the comprehensive answer.

## RTX 5080/5090 LoRA Training Compatibility Report (as of March 2026\)

The RTX 50-series (Blackwell) uses CUDA compute capability sm\_120, which requires specific software stack versions. Here's everything confirmed working and every known issue, with sources.

---

## Confirmed Working Configurations

## kohya\_ss on RTX 5090

| Config | PyTorch | CUDA | xformers | Optimizer | Speed | Source |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Simplest fix | 2.7+ / nightly cu128 | 12.8 | Disabled (use SDPA) | Any | Varies | kohya\_ss \#3096​ |
| With xformers | Nightly cu128 | 12.8 | pip3 install \--pre \-U \--no-deps xformers \+ bitsandbytes | AdamW8bit | 2.68 s/it, 17.8GB VRAM (SDXL batch 8\) | kohya\_ss \#3096​ |
| Stable release | 2.7.1 | 12.8 | On | AdamW8bit, BF16 | 1.36 s/it (batch 2, 1024x1024) | kohya\_ss \#3096​ |
| gui-uv.bat | Bundled | 12.9 (V12.9.86), cuDNN 9.10.2 | Via gui-uv.bat | AdamW | 3.45 s/it (batch 4, grad accum 2\) | kohya\_ss \#3332​ |

## kohya\_ss on RTX 5080

* Requires the kohya\_ss dev branch — the stable branch does not support sm\_120.  
* CUDA 12.9, cuDNN 9.10.1 reported as working.  
* A   
* [video walkthrough exists](https://www.youtube.com/watch?v=3lPc3dmxD54)  
*  for 5080 setup.  
* Source: kohya\_ss \#3096​

## OneTrainer

* On RTX 5090: requires PyTorch 2.8+ with CUDA 12.8 to resolve sm\_120 errors. Some users report needing to change the source model to get it working.​  
* On RTX 5080: confirmed working with PyTorch nightly cu128 alongside ComfyUI.​  
* Fluxgym and OneTrainer both had initial incompatibility with 50-series; OneTrainer is further along in support.​

---

## Universal Install Commands (50-series)

The minimum viable setup for any 50-series card:

bash

*`# Install PyTorch with CUDA 12.8 support`*  
`pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128`

*`# Option A: Disable xformers entirely (safest)`*  
`pip3 uninstall xformers`

*`# Option B: Install compatible xformers (faster but riskier)`*  
`pip3 install --pre -U --no-deps xformers`  
`pip3 install -U bitsandbytes`

Source: kohya\_ss \#3096, Fooocus \#3862

---

## Known Bugs and Issues

## 1\. cutlassF: no kernel found (xformers crash)

* Affects some RTX 5090 setups when xformers is enabled.  
* Fix: Uninstall xformers and use SDPA, or use the \--pre \-U \--no-deps xformers install method.  
* Source: kohya\_ss \#3276, kohya\_ss \#3096

## 2\. Painfully slow training (4.78 s/it on a 5090\)

* Cause: Prodigy optimizer \+ gradient checkpointing is pathologically slow on Blackwell.  
* Fix: Switch to AdamW optimizer and use SDPA cross-attention. Disabling gradient checkpointing also helps (\~20% improvement).  
* After fix, one user achieved 3.45 s/it at batch 4 with gradient accumulation 2\.  
* Source: kohya\_ss \#3332​

## 3\. Same speed as RTX 4080 (no improvement)

* Some users report 1.10 s/it on 5090 at batch 2, identical to their old 4080\.  
* Likely caused by suboptimal kohya\_ss configuration or stale kohya\_ss version.  
* Suggestion from community: try AI-Toolkit or OneTrainer instead, which have better 5090 optimization.  
* Source: r/StableDiffusion​

## 4\. GPU utilization 100% but low temps and slow training

* Reported on both RTX 4070 Super and RTX 5090 — GPU shows 100% utilization in Task Manager but runs at 40-45°C (should be 70°C+), with 15.91 s/it on the 5090\.  
* Likely a driver or power management issue causing the GPU to not actually compute at full speed.  
* Source: r/StableDiffusion​

## 5\. VRAM exhaustion on RTX 5090 (32GB)

* One user ran out of VRAM training SDXL LoRA at batch 4, 1024x1024, BF16.  
* Fix: Lower batch size to 1-2, or enable gradient checkpointing (with AdamW, not Prodigy).  
* Source: kohya\_ss \#3296​

## 6\. Hard system crash (Xid 119 GSP Timeout) — Linux

* RTX 5090 FE causes instant hard power-off under sustained CUDA load (LoRA training, LLM inference).  
* Error: NVRM: Xid (PCI:0000:01:00): 119, Timeout after 6s of waiting for RPC response from GPU0 GSP  
* 100% reproducible. Persists even at 400W power limit (GPU minimum).  
* Hardware: AMD Ryzen 9 9950X3D, be quiet\! Dark Power 14 1200W PSU, driver 580.95.05, CUDA 13.0.  
* Multiple users with be quiet\! Dark Power 14 PSUs report this — possibly PSU-related.  
* No fix found. OP considers RMA.  
* Source: NVIDIA Developer Forums​

## 7\. OneTrainer sm\_120 / NoneType error on RTX 5090

* Error: NoneType object has no attribute 'to' when starting training.  
* Root cause: PyTorch version doesn't support sm\_120.  
* Fix: Install PyTorch 2.8+ with CUDA 12.8. Some users also needed to change the source model.  
* Source: r/FluxAI​

---

## Version Compatibility Matrix

| Component | Minimum for 50-series | Recommended | Notes |
| :---- | :---- | :---- | :---- |
| PyTorch | 2.7.0 nightly cu128 | 2.7.1+ cu128 or 2.8+ | Stable releases before 2.7 do NOT support sm\_120 |
| CUDA Toolkit | 12.8 | 12.8–12.9 | cu121 builds will NOT work |
| cuDNN | 9.x | 9.10.1+ | Required for Blackwell kernels |
| NVIDIA Driver | 570+ | Latest Game Ready / Studio | [NVIDIA drivers page](https://www.nvidia.com/drivers) |
| xformers | Optional | Nightly cu128 build or disable | Source of most compatibility issues |
| kohya\_ss branch | dev (for 5080\) | dev with gui-uv.bat | Stable branch may lag on 50-series support |
| OneTrainer | Latest \+ PyTorch 2.8 cu128 | Latest GitHub main | Needs manual PyTorch override |

---

## Relevance to Your RTX 5080

Your RTX 5080 (16GB GDDR7) uses the same sm\_120 compute capability as the 5090, so all of the above applies. Key differences for you:

* You will need the kohya\_ss dev branch specifically.  
* 16GB VRAM means batch size 1-2 for SDXL LoRA training at 1024x1024 with gradient checkpointing enabled.  
* The gui-uv.bat launcher in kohya\_ss bundles the correct PyTorch/CUDA versions automatically — this is the path of least resistance.  
* Disabling xformers and using SDPA is the safest starting configuration.

---

## All Sources

| Source | URL |
| :---- | :---- |

| Source | URL |
| :---- | :---- |
| kohya\_ss \#3096 (main 5090 compat thread) | github.com/bmaltais/kohya\_ss/issues/3096​ |
| kohya\_ss \#3332 (slow training) | github.com/bmaltais/kohya\_ss/issues/3332​ |
| kohya\_ss \#3276 (xformers error) | github.com/bmaltais/kohya\_ss/issues/3276​ |
| kohya\_ss \#3296 (VRAM issues) | github.com/bmaltais/kohya\_ss/issues/3296​ |
| Fooocus \#3862 (sm\_120 PyTorch fix) | github.com/lllyasviel/Fooocus/issues/3862​ |
| Fluxgym \#355 (sm\_120 on 5090\) | github.com/cocktailpeanut/fluxgym/issues/355​ |
| InvokeAI \#7683 (5090 support, OneTrainer mention) | github.com/invoke-ai/InvokeAI/issues/7683​ |
| NVIDIA Forum: Xid 119 hard crash | forums.developer.nvidia.com/.../354867​ |
| NVIDIA Forum: sm\_120 PyTorch issue | forums.developer.nvidia.com/.../338015​ |
| r/StableDiffusion: 5090 upgrade report | reddit.com/r/StableDiffusion/.../so\_i\_upgraded\_to\_a\_5090​ |
| r/StableDiffusion: 5090 same speed as 4080 | reddit.com/r/StableDiffusion/.../kohya\_ss\_with\_a\_rtx\_5090​ |
| r/StableDiffusion: GPU utilization but slow | reddit.com/r/StableDiffusion/.../kohya\_ss\_gpu\_utilization​ |
| r/StableDiffusion: 5080 vs 5090 for diffusion | reddit.com/r/StableDiffusion/.../burned\_out\_chasing\_5090​ |
| r/comfyui: LoRA training with 5090 | reddit.com/r/comfyui/.../local\_character\_lora\_training​ |
| r/comfyui: Train LoRA on 5080 | reddit.com/r/comfyui/.../train\_lora\_on\_a\_5080​ |
| r/FluxAI: OneTrainer on 5090 | reddit.com/r/FluxAI/.../issues\_with\_onetrainer​ |
| A1111 WebUI: Blackwell 50xx instructions | github.com/AUTOMATIC1111/.../16818​ |
| Stable Diffusion Art: RTX 50-series setup guide | stable-diffusion-art.com​ |

The ecosystem is stabilizing but still has rough edges. For your 5080 with kohya\_ss, the dev branch \+ gui-uv.bat \+ SDPA (no xformers) is the safest path right now.  
