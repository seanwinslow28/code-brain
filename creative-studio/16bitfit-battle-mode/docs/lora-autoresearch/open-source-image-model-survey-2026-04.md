# Open-Source Image Model Survey — 2026-04-18

## TL;DR

- **#1: Z-Image-Turbo (Tongyi-MAI, 6B DiT, 2025-11-27)** — fits 16 GB at BF16/FP8, native ComfyUI templates, Z-Image ControlNet Union 2.1 with pose, and a Civitai "Pixel Art Style LoRA v1.0 for Z-Image Turbo" that explicitly targets sprite work. Only candidate with a dedicated pixel-art LoRA today.
- **#2: FLUX.2-klein-4B (Black Forest Labs, Apache-2.0)** — ~13 GB footprint, Apache-2.0 commercial license, PuLID-Flux2 for face ID, mature Flux LoRA toolchain. Strong fallback if Z-Image stylization looks wrong.
- **ERNIE-Image-Turbo (GGUF)** — the SETUP-NOTES rejection is overturned on VRAM and ComfyUI integration, but there is no ControlNet and no pixel-art LoRA as of 2026-04-18. Not viable for a pose-conditioned sprite pipeline *yet*.
- Qwen-Image-Edit is the strongest reference-driven editor but is 20B, heavy at Nunchaku int4, and has no pixel-art LoRA ecosystem.
- HiDream-I1 is eliminated on VRAM (FP8 >16 GB, nf4 spikes 23 GB).

## Context

Phase 1 autoresearch (150 Optuna trials, Illustrious XL v2.0, SpaceCandy + FightingSprites + SF3XL LoRAs) peaked at composite score 0.8163 but produced output Sean judged "2019–2020-era" by eye. SDXL-family models (base, refiner, Illustrious XL, all SDXL LoRAs) are removed from the search space. See CHANGELOG [3.13.1] — 2026-04-18 for the decision log and the convergence data.

The autoresearch infrastructure is kept: the Optuna loop in [runner.py](16bitfit-battle-mode/autoresearch/runner.py), the workflow mutator in [workflow_mutator.py](16bitfit-battle-mode/autoresearch/workflow_mutator.py), the 5-tier scorer with face-grounded Qwen3-VL judge in [prepare.py](16bitfit-battle-mode/autoresearch/prepare.py), and the 150-trial benchmark artifacts at `autoresearch/results/phase1/`. What needs replacing is the model backend and a compatible ControlNet + character-reference stack. This survey is the triage before any new autoresearch run.

## Prior ERNIE Verdict — Re-Checked

SETUP-NOTES line 127–135 listed three reasons to reject ERNIE-Image-Turbo:

1. **"Requires 24GB VRAM — our RTX 5080 only has 16GB"** — **OVERTURNED.** Baidu's native BF16 run still wants ~24 GB, but `unsloth/ERNIE-Image-Turbo-GGUF` (https://huggingface.co/unsloth/ERNIE-Image-Turbo-GGUF) ships a Q2K–Q8 ladder starting at ~3.18 GB. A Q6/Q8 sits well inside 16 GB even after loading the Mistral-3B text encoder (~7.5 GB) and the VAE. The YouTube transcript demonstrates the Q2K path end-to-end in ComfyUI.
2. **"No ComfyUI integration — diffusers-only"** — **OVERTURNED.** ComfyUI ships a "Day-0" ERNIE-Image / ERNIE-Image-Turbo template in the workflow browser (https://blog.comfy.org/p/ernie-image-day-0-support, https://docs.comfy.org/tutorials/image/ernie-image/ernie-image). The GGUF path uses the existing `city96/ComfyUI-GGUF` loader (https://github.com/city96/ComfyUI-GGUF, last commit 2026-01-12) with no ERNIE-specific CUDA kernel, so sm_120 compatibility reduces to "your PyTorch build supports sm_120" — which this setup already does.
3. **"Our LoRAs won't work — different architecture"** — **STILL TRUE, BUT MOOT.** ERNIE is a DiT single-stream model; SDXL LoRAs cannot load. Per CHANGELOG 3.13.1, all SDXL-family LoRAs are being discarded anyway, so this objection no longer constrains the decision.

**What the transcript does NOT establish, and what I could not verify elsewhere as of 2026-04-18:** an ERNIE-Image ControlNet (pose/canny/depth) and any pixel-art LoRA for ERNIE. The transcript never mentions pose conditioning, ControlNet, IP-Adapter equivalents, or pixel-art output. The HuggingFace card and the DiffSynth-Studio ERNIE LoRA training script (https://github.com/modelscope/DiFfSynth-Studio) confirm LoRA training is possible but not that anyone has published a pose ControlNet. For a pose-skeleton-driven sprite pipeline this is the missing piece.

## Candidate Models

### Z-Image-Turbo (Tongyi-MAI / Alibaba)
- **Release date / current version:** 2025-11-27
- **Architecture:** Scalable Single-Stream DiT (S3-DiT)
- **Parameters / file size:** 6B; ~12 GB BF16 safetensors
- **VRAM @ quantization:**

  | Precision | VRAM | Notes |
  |---|---|---|
  | BF16 | ~12 GB | fits with workflow headroom on 16 GB |
  | FP8 | ~7 GB | comfortable |
  | SVDQ int4 | ~4–6 GB | via https://civitai.com/models/2169712 |
  | GGUF Q5/Q8 | 5–9 GB | city96 loader path |

- **ComfyUI support:** Native — official templates and a Comfy-Org HF mirror. Release coverage: https://comfyui-wiki.com/en/news/2025-11-27-alibaba-z-image-turbo-release (2025-11-27), https://blog.comfy.org/p/z-image-turbo-in-comfyui-realism (2025-11).
- **ControlNet:** **Yes** — "Z-Image ControlNet Union 2.1" (canny, depth, pose, softedge) documented in SECourses LoRA+ControlNet tutorial at https://medium.com/@furkangozukara/z-image-turbo-lora-training-with-ai-toolkit-and-z-image-controlnet-full-tutorial-for-highest-4323800177f7 (2026).
- **Character/reference conditioning:** Via ControlNet + character LoRA. No native IP-Adapter FaceID equivalent verified; PuLID-for-Z-Image **unverified**.
- **LoRA training toolchain:** Ostris AI-Toolkit is the primary trainer; `shootthesound/comfyUI-Realtime-Lora` trains inside ComfyUI. Kohya less prominent.
- **sm_120 / RTX 5080 confirmed:** Yes, via SECourses Blackwell benchmarks at CUDA 13 + Sage-Attention — https://www.patreon.com/posts/compared-quality-148472710. No Z-Image-specific sm_120 bug reports.
- **Output quality notes:** #8 overall and **#1 open-source** on Artificial Analysis T2I leaderboard. Sub-second 8-step generation reported. **Dedicated pixel-art support:** https://civitai.com/models/1770073/pixel-art-style-lora (Pixel Art Style LoRA v1.0 for Z-Image Turbo); Apatero guide claims "more consistent dithering patterns and better sprite proportions than SDXL pixel-art LoRAs" — https://apatero.com/blog/z-image-turbo-pixel-art-lora-complete-guide-2025. The ERNIE YouTube transcript also notes Z-Image handles anatomy better than ERNIE (see "Anatomy tests" section) — relevant for sprite poses.
- **Community sentiment:** Regarded as the strongest open-source release of Q4 2025. ERNIE transcript frames it as the reigning open-source leader ("current best open-source image generator, Zimage"). Bested by ERNIE on text/detail but wins on anatomy and speed.
- **Viable for Sean's pipeline?** **YES.**

### FLUX.2-klein-4B (Black Forest Labs)
- **Release date / current version:** Flux.2 family active in 2026; Klein 4B is the small variant, Apache-2.0.
- **Architecture:** MMDiT successor to Flux.1
- **Parameters / file size:** 4B; ~13 GB native
- **VRAM @ quantization:** Fits 16 GB comfortably at native precision; GGUF variants via `city96/FLUX.2-dev-gguf` (https://huggingface.co/city96/FLUX.2-dev-gguf) reduce further for Dev.
- **ComfyUI support:** Native workflows for text-to-image, editing, single-ref, multi-ref — https://blog.comfy.org/p/flux2-klein-4b-fast-local-image-editing.
- **ControlNet:** Yes (Flux.1 depth/canny transfer; Flux.2-specific in active development).
- **Character/reference conditioning:** `ComfyUI-PuLID-Flux2` — https://www.runcomfy.com/comfyui-nodes/ComfyUI-PuLID-Flux2. Multi-reference workflows confirmed.
- **LoRA training toolchain:** kohya-ss, ai-toolkit, kijai/ComfyUI-FluxTrainer, Flux-Gym. Apatero has a Q8 GGUF training guide for 16 GB cards — https://apatero.com/blog/flux-2-rtx-5070-ti-16gb-performance-guide-2025.
- **sm_120 / RTX 5080 confirmed:** Yes, via NVIDIA RTX AI Garage post — https://blogs.nvidia.com/blog/rtx-ai-garage-flux-2-comfyui/ — plus SECourses Blackwell benchmarks referenced above.
- **Output quality notes:** No dedicated Flux.2 pixel-art LoRA surfaced yet; Flux.1 pixel-art LoRAs on Civitai partially transfer (**unverified transferability**).
- **Community sentiment:** Treated in April-2026 closed-vs-open comparisons as "the only open-source self-hostable option" in the premium tier — https://blog.laozhang.ai/en/posts/nano-banana-2-vs-midjourney-vs-gpt-image-vs-flux2.
- **Viable for Sean's pipeline?** **YES** — secondary recommendation.

### ERNIE-Image-Turbo (Baidu, Unsloth GGUF)
- **Release date / current version:** 2026-04-15 — ~3 days old at this report's date.
- **Architecture:** 8B DiT single-stream with a Prompt Enhancer
- **Parameters / file size:** 8B; ~16 GB BF16
- **VRAM @ quantization:**

  | Precision | VRAM | Notes |
  |---|---|---|
  | BF16 | ~24 GB (with encoder + VAE) | does not fit 16 GB |
  | GGUF Q8 | ~9–10 GB | fits |
  | GGUF Q6 | ~7 GB | fits |
  | GGUF Q2K | ~3.2 GB | fits; transcript demonstrates |

- **ComfyUI support:** Native template ("Day-0") — https://blog.comfy.org/p/ernie-image-day-0-support, https://docs.comfy.org/tutorials/image/ernie-image/ernie-image. GGUF path via city96/ComfyUI-GGUF (last commit 2026-01-12). Requires Mistral-3B text encoder (~7.5 GB) per transcript; Flux-2 VAE reuse referenced in secondary tutorials — **unverified on official model card**.
- **ControlNet:** **Not found** as of 2026-04-18. No pose/canny/depth ControlNet for ERNIE located on HuggingFace, GitHub, or ComfyUI Registry. Mark **unverified / likely absent**.
- **Character/reference conditioning:** No native IP-Adapter / PuLID / reference-only mechanism identified. fal.ai LoRA trainer is live and DiffSynth-Studio ships `examples/ernie_image/model_training/lora/ERNIE-Image.sh`, but this is for LoRA training, not runtime reference conditioning.
- **LoRA training toolchain:** fal.ai trainer, DiffSynth-Studio (modelscope), Ostris AI-Toolkit ERNIE path — Medium 2026-03 guides.
- **sm_120 / RTX 5080 confirmed:** No ERNIE-specific report found. city96/ComfyUI-GGUF is pure-Python, so depends only on the PyTorch cu128 build already on disk. **Unverified in practice.**
- **Output quality notes:** Transcript and Baidu benchmarks show strongest-in-open-source text rendering, comics, infographics, prompt adherence. **Anatomy is a weakness** per transcript — the king-pigeon yoga test and bathtub test both fail where Z-Image succeeds. This matters for fighting-game sprites with non-trivial poses. No pixel-art LoRA exists.
- **Community sentiment:** ERNIE transcript and Baidu-published benchmarks place it ahead of Z-Image, Qwen-Image, and Flux 2 Klein on overall image-generation score, approaching Nano Banana 2. Reception in the broader community is <72 hours old at report date, so long-tail bug reports have not accumulated.
- **Viable for Sean's pipeline?** **MAYBE — not yet.** The missing ControlNet and missing character-reference mechanism are hard blockers for a pose-conditioned, identity-anchored sprite workflow. Revisit in 4–6 weeks if a pose ControlNet ships.

### Qwen-Image / Qwen-Image-Edit (Alibaba)
- **Release date / current version:** Qwen-Image 2.0 on 2026-02-10; Qwen-Image-Edit-2511 on 2025-12-23.
- **Architecture:** 20B DiT
- **VRAM @ quantization:** Native BF16 does not fit 16 GB. Nunchaku int4 and GGUF variants do fit; Qwen-Image-Lightning distillation reduces step count.
- **ComfyUI support:** Native + GGUF + Nunchaku workflows — https://blog.comfy.org/p/comfyui-now-supports-qwen-image-controlnet.
- **ControlNet:** Yes — DiffSynth ControlNets (canny, depth, inpaint) and a Union DiffSynth LoRA (lineart, softedge, normal, openpose).
- **Character/reference conditioning:** Qwen-Image-Edit dual-path (Qwen2.5-VL semantic + VAE appearance). Best-in-class among open models for reference-driven editing.
- **LoRA training toolchain:** Ostris AI-Toolkit supports Qwen-Image; `ussoewwin/ComfyUI-QwenImageLoraLoader` for Nunchaku.
- **sm_120 / RTX 5080 confirmed:** Runs via standard PyTorch cu128 path. No model-specific sm_120 issues found.
- **Output quality notes:** No dedicated pixel-art LoRA found. Heavyweight for pure sprite generation.
- **Community sentiment:** Strong for image-edit and reference-driven tasks, less so for stylized from-scratch generation.
- **Viable for Sean's pipeline?** **MAYBE — as a reference-driven editor**, not as the primary sprite generator. Reconsider if Sean needs identity-locked pose edits of existing sprites rather than first-frame generation.

### HiDream-I1
- **Release date / current version:** 2025-04-07, MIT, 17B
- **VRAM:** FP8 **>16 GB**; nf4 spikes to ~23 GB during inference. Does not fit reliably.
- **ComfyUI support:** Native + GGUF/nf4.
- **Viable for Sean's pipeline?** **NO — VRAM blocker.**

### Quick Triage (rejected on community momentum)

| Model | Status April 2026 | Verdict |
|---|---|---|
| SD3.5 | Low mindshare, supplanted by Flux.2 / Z-Image | Skip |
| Kolors | Still supported in OllamaDiffuser, minimal new LoRAs | Skip |
| Hunyuan-DiT | Overshadowed by Qwen / Flux.2 | Skip |
| PixArt-Sigma | Legacy | Skip |
| Lumina-Next / Lumina-Image 2.0 | Small community, few LoRAs | Skip |
| Seedream 4 / 4.5 (ByteDance) | API-only / closed weights | Skip (not open) |

## Community Sentiment vs Closed Models

The central closed-vs-open comparison threads located in April 2026:

- **"Z-Image vs Nano Banana Pro vs FLUX.2 Pro"** — https://medium.com/@yeekal/z-image-vs-nano-banana-pro-vs-flux-2-pro-29f71397b4a6 — concludes Z-Image matches Nano Banana Pro quality at 1/10 to 1/30 the inference cost; Nano Banana Pro retains a lead on in-image text; Flux.2 Pro wins atmospheric detail.
- **"Nano Banana 2 vs Midjourney vs GPT Image 1.5 vs FLUX.2"** — https://blog.laozhang.ai/en/posts/nano-banana-2-vs-midjourney-vs-gpt-image-vs-flux2 — frames FLUX.2 as the only self-hostable premium-tier open model.
- **"Nano Banana Pro vs FLUX.2 Max vs GPT 1.5 — Brutally Honest"** — https://medium.com/@cognidownunder/nano-banana-pro-vs-flux-2-max-vs-gpt-1-5-106c8f5de7b4 — broad parity at the top, differentiation by prompt adherence and edit fidelity.
- **Baidu's own benchmark** (via ERNIE transcript "Benchmarks" section) places ERNIE-Image ahead of Z-Image, Qwen-Image, Flux 2 Klein, and approaching Nano Banana 2 on overall image-generation score. Vendor-published; treat as directional, not independent.

**None of these threads benchmark pixel-art / sprite output quality against closed models.** That specific gap is **unverified** from the located sources.

Per the 16bitfit-battle-mode CLAUDE.md, Nano Banana Pro / Nano Banana 2 remain the production primary generators for the sprite pipeline regardless. This survey targets the local autoresearch backend only.

## Installation Steps (Top 2 Only)

> Sanity-test-only model placement. Do NOT trigger autoresearch, do NOT install custom nodes beyond what is already present. These paths assume the existing ComfyUI root at `C:\Users\seanw\Documents\Code-Brain\ComfyUI\` and existing `city96/ComfyUI-GGUF` install.

### Z-Image-Turbo

```powershell
# 1. Model download — full BF16 variant (fits 16 GB)
$Comfy = "C:\Users\seanw\Documents\Code-Brain\ComfyUI"
Invoke-WebRequest `
  "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo/resolve/main/z_image_turbo_bf16.safetensors" `
  -OutFile "$Comfy\models\diffusion_models\z_image_turbo_bf16.safetensors"

# 2. Optional: the Pixel Art Style LoRA v1.0 (Civitai manual download — requires login)
#    Place the .safetensors at:
#    $Comfy\models\loras\z_image_pixel_art_v1.safetensors
#    URL: https://civitai.com/models/1770073/pixel-art-style-lora

# 3. In ComfyUI: Templates -> search "Z-Image" -> load Z-Image-Turbo template.
#    Point the Diffusion Model node to z_image_turbo_bf16.safetensors.
#    (If Pixel Art LoRA was downloaded, drop a LoRA Loader in front of the sampler.)
```

### FLUX.2-klein-4B

```powershell
$Comfy = "C:\Users\seanw\Documents\Code-Brain\ComfyUI"

# 1. Model (Apache-2.0; HF login may be required)
Invoke-WebRequest `
  "https://huggingface.co/black-forest-labs/FLUX.2-klein-4B/resolve/main/flux2_klein_4b.safetensors" `
  -OutFile "$Comfy\models\diffusion_models\flux2_klein_4b.safetensors"

# 2. Text encoders and VAE — the Flux.2 Klein ComfyUI template will flag any missing
#    files with direct download links in the "See errors" panel. Use that button rather
#    than guessing paths; text encoders go to models\text_encoders, VAE to models\vae.

# 3. In ComfyUI: Templates -> "FLUX.2 Klein" -> load text-to-image template.
```

## Ranked Recommendation

1. **Z-Image-Turbo.** It is the only 2026-relevant open-source model that simultaneously clears every hard requirement for Sean's pipeline: (a) fits 16 GB at BF16 with workflow headroom, (b) has a mature native ComfyUI template and GGUF fallback, (c) ships a confirmed pose ControlNet (Z-Image ControlNet Union 2.1), (d) has a Civitai pixel-art LoRA built specifically for this base with documented sprite-proportion benefits over the SDXL pixel-art LoRAs Sean just discarded, and (e) holds #1 open-source position on the Artificial Analysis T2I leaderboard. Anatomy handling is noted as a strength in the ERNIE transcript's own head-to-head, which matters because the autoresearch targets pose-conditioned fighting-game frames. The main risk: PuLID/IP-Adapter-FaceID equivalent for identity locking is **unverified** — if Sean needs face-ID consistency the way Phase 1 used IPAdapterFaceID, that node may need to be retired in favor of a Sean-anchor LoRA.
2. **FLUX.2-klein-4B.** Apache-2.0 license, comfortable 16 GB fit, PuLID-Flux2 for character identity, mature LoRA training toolchain, and confirmed RTX 5080 inference per NVIDIA's own blog. The gap versus Z-Image: no dedicated pixel-art LoRA has surfaced yet, so the stylization path depends on transfer from Flux.1 LoRAs (unverified quality) or training a new Sean-specific LoRA. Run this only if Z-Image's stylization fails the eye-test on step 1.

ERNIE-Image-Turbo is not ranked because two hard requirements (pose ControlNet, character-reference conditioning) are missing at report date. Revisit when a pose ControlNet ships.

## Stock Sanity Test Protocol

- Install **Z-Image-Turbo BF16** only. Skip the pixel-art LoRA on round 1 — we want to see the base model's un-LoRA'd look, since Phase 1 proved LoRA-over-weak-base collapses quality.
- Open the ComfyUI Z-Image-Turbo template. Do not alter sampler/steps/CFG; use template defaults.
- Prompt (verbatim): `2D pixel art fighter sprite, muscular man, white tank top, blue pants, walking stance, full body, white background`. Generate **5 frames** with 5 different seeds.
- Pass criteria (eyeball): (a) recognizable single full-body character, not a sprite sheet of tiny characters; (b) pixel aesthetic or at minimum stylized / non-photoreal; (c) reasonable anatomy (arms and legs attached, facing consistent); (d) no ControlNet-style overlay artifacts (this is a no-ControlNet test).
- Fail criteria: photoreal output with no stylization, garbled anatomy in 3+ of 5 frames, or output that looks equivalent to Phase 1 (score the visual jump against the Phase 1 sanity-check frames at `autoresearch/results/phase1/sanity_check/`).
- If PASS: load the **Pixel Art Style LoRA v1.0 for Z-Image Turbo** (Civitai 1770073), rerun 5 frames, compare. If that also passes, move to a pose-conditioned test using Z-Image ControlNet Union 2.1 and one of the existing hand-drawn skeletons at `autoresearch/references/pose_skeletons/ryu_walk_passing.png`.
- If FAIL: fall back to **FLUX.2-klein-4B** before spending any time on ERNIE.
- Do **not** wire autoresearch until both the stylization sanity test and a 3-frame pose-conditioned test pass. Re-pointing `workflow_mutator.py` at a new node graph is a separate task from model selection.

## Risks and Unknowns

- No PuLID / IP-Adapter-FaceID equivalent for Z-Image-Turbo confirmed — identity anchoring mechanism needs a design decision (character LoRA vs. reference-image node). **Unverified.**
- ERNIE-Image ControlNet and reference-conditioning absence is asserted based on an exhaustive search on 2026-04-18; a node could land tomorrow. Recheck before dismissing permanently.
- Flux.2 pixel-art LoRA transferability from Flux.1 Civitai catalog is **unverified** — would need empirical test.
- city96/ComfyUI-GGUF has no commits referencing Blackwell or sm_120 specifically; kernelless Python loader path is the reason it "just works." No formal verification.
- All vendor-published benchmarks (Baidu's ERNIE scorecard) are directional only; independent pixel-art-specific benchmarks do not exist.
- SECourses Patreon benchmark of Z-Image / Flux.2 on Blackwell sits behind a paywall — confirmation is that it exists, not a first-hand read.
- The YouTube transcript has no visible publish date in the file itself; weight its claims as current-as-of-early-2026 since it discusses Unsloth ERNIE GGUFs that were published around the 2026-04-15 ERNIE release. Treat as recent but not independently dated.
- Z-Image Civitai pixel-art LoRA was found via the research agent's summary; Civitai model 1770073 should be confirmed accessible before the sanity test (login may be required).

## Sources

1. https://huggingface.co/Tongyi-MAI/Z-Image-Turbo — model card (accessed 2026-04-18)
2. https://comfyui-wiki.com/en/news/2025-11-27-alibaba-z-image-turbo-release — release coverage (2025-11-27)
3. https://blog.comfy.org/p/z-image-turbo-in-comfyui-realism — ComfyUI official (2025-11)
4. https://civitai.com/models/1770073/pixel-art-style-lora — Pixel Art LoRA for Z-Image
5. https://apatero.com/blog/z-image-turbo-pixel-art-lora-complete-guide-2025 — Apatero pixel-art guide (2025)
6. https://medium.com/@furkangozukara/z-image-turbo-lora-training-with-ai-toolkit-and-z-image-controlnet-full-tutorial-for-highest-4323800177f7 — SECourses Z-Image ControlNet + AI-Toolkit (2026)
7. https://civitai.com/models/2169712/z-image-turbo-quantized-for-low-vram — SVDQ int4 Z-Image
8. https://huggingface.co/unsloth/ERNIE-Image-Turbo-GGUF — Unsloth GGUF card
9. https://huggingface.co/baidu/ERNIE-Image-Turbo — Baidu model card
10. https://blog.comfy.org/p/ernie-image-day-0-support — ComfyUI Day-0 blog (2026-04)
11. https://docs.comfy.org/tutorials/image/ernie-image/ernie-image — ComfyUI docs tutorial
12. https://github.com/baidu/ernie-image — Baidu repo
13. https://github.com/modelscope/DiffSynth-Studio — DiffSynth ERNIE LoRA training
14. https://github.com/city96/ComfyUI-GGUF — GGUF loader (last commit 2026-01-12)
15. https://cntechpost.com/2026/04/15/baidu-open-sources-ernie-image-model-bringing-top-tier-rendering-consumer-gpus/ — ERNIE release coverage (2026-04-15)
16. https://www.stablediffusiontutorials.com/2026/04/ernie-image.html — ERNIE tutorial (2026-04)
17. https://blog.comfy.org/p/comfyui-now-supports-qwen-image-controlnet — Qwen-Image ControlNet
18. https://github.com/QwenLM/Qwen-Image — Qwen-Image repo
19. https://github.com/ussoewwin/ComfyUI-QwenImageLoraLoader — Nunchaku Qwen LoRA loader
20. https://www.kombitz.com/2025/10/03/how-to-use-controlnet-with-qwen-image-edit-2509-in-comfyui/ — Qwen-Image-Edit ControlNet (2025-10-03)
21. https://comfyui-wiki.com/en/tutorial/advanced/image/hidream/i1-t2i — HiDream-I1 wiki
22. https://bfl.ai/blog/flux-2 — Flux.2 release
23. https://blog.comfy.org/p/flux2-klein-4b-fast-local-image-editing — Flux.2 Klein (2025)
24. https://huggingface.co/black-forest-labs/FLUX.2-klein-4B — Klein 4B card
25. https://huggingface.co/city96/FLUX.2-dev-gguf — Flux.2 Dev GGUF
26. https://www.runcomfy.com/comfyui-nodes/ComfyUI-PuLID-Flux2 — PuLID-Flux2
27. https://apatero.com/blog/flux-2-rtx-5070-ti-16gb-performance-guide-2025 — Apatero Flux.2 on 16 GB (2025)
28. https://blogs.nvidia.com/blog/rtx-ai-garage-flux-2-comfyui/ — NVIDIA RTX + Flux.2
29. https://medium.com/@yeekal/z-image-vs-nano-banana-pro-vs-flux-2-pro-29f71397b4a6 — Z-Image vs Nano Banana Pro
30. https://blog.laozhang.ai/en/posts/nano-banana-2-vs-midjourney-vs-gpt-image-vs-flux2 — 2026 closed-vs-open comparison
31. https://medium.com/@cognidownunder/nano-banana-pro-vs-flux-2-max-vs-gpt-1-5-106c8f5de7b4 — Brutally Honest (2026)
32. https://www.patreon.com/posts/compared-quality-148472710 — SECourses Blackwell benchmarks
33. https://github.com/Comfy-Org/ComfyUI/discussions/6643 — ComfyUI Blackwell thread
34. https://codecalamity.com/setting-up-your-rtx-5070-5080-or-5090-for-ai-comfyui-on-windows-through-wsl/ — Blackwell ComfyUI setup
35. `16bitfit-battle-mode/docs/lora-autoresearch/Ernie-Image-Youtube-Transcript.md` — primary ERNIE transcript (local file)
36. `16bitfit-battle-mode/autoresearch/workflows/SETUP-NOTES.md` — prior ERNIE verdict (local file)
37. `CHANGELOG.md` — entry [3.13.1] 2026-04-18 (local file)
