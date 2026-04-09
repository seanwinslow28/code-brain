# Open-Source Vision Models for Local Sprite Quality Assessment

## Executive Summary

For an automated sprite quality assessment pipeline processing 128×128 and 256×256 pixel art images on an M4 Pro 48GB MacBook and RTX 5080 desktop, the **Qwen2.5-VL-7B** is the strongest all-around choice: it supports native multi-image input, structured JSON output, runs efficiently on both Apple Silicon (MLX) and NVIDIA (vLLM/GGUF), and is the most fine-tunable model in its class. For extremely high-throughput batch pipelines or memory-constrained scenarios, **SmolVLM2-2.2B** or **Moondream 2B** are strong sub-3B alternatives. The accuracy gap between a well-prompted 7B local model and a frontier API like Gemini 2.5 Pro is meaningful on zero-shot pixel art tasks, but narrows dramatically — often to near-parity — with even modest domain fine-tuning. A fine-tuned 8B model matched the accuracy of models 30× its size on a specialized visual task in documented experiments.[^1]

***

## Small/Efficient Models (Under 8B Parameters)

### Moondream 2 (2B)

Moondream is a lightweight VLM built for edge and local deployment. The April 2025 4-bit quantized release uses only **2,450 MB of VRAM** and runs at **184 tokens/second** on an RTX 3090 — the lightest footprint of any capable model. The quantization used quantization-aware training, resulting in just a **0.6% accuracy drop** compared to the full-precision model. The March 2025 release added `compile()` support that doubled inference speed from 61.4 to 123.4 tokens/second. Structured outputs in JSON, XML, and YAML are natively supported.[^2][^3][^4]

On your M4 Pro 48GB, expect ~50–70 tokens/second with 4-bit MLX (Apple Silicon support for Moondream 3.0 is forthcoming). On the RTX 5080, the model will sit entirely in VRAM with substantial headroom, making it suitable for extremely high-throughput batch processing. **Moondream 3.0** (preview) uses a MoE architecture with 9B total/2B active parameters and currently requires a 24GB NVIDIA GPU, with Apple Silicon and quantized versions announced as coming soon.[^5][^6]

**Key limitation:** Moondream is primarily trained on natural images. Pixel art is a niche domain and zero-shot quality scoring without fine-tuning will be limited. Multi-image comparison in a single call is not a core advertised feature of Moondream 2; the API is oriented toward per-image queries.

| Property | Value |
|----------|-------|
| Parameters | 2B (4-bit: ~0.9B effective) |
| VRAM (4-bit) | ~2.5 GB |
| Apple Silicon | Via Transformers/llama.cpp; MLX support in progress |
| NVIDIA | CUDA, HuggingFace Transformers, llama.cpp |
| Multi-image | Single image per call (v2); v3.0 TBD |
| Structured output | JSON, XML, YAML |
| Fine-tunable | Yes (LoRA) |
| GitHub | github.com/vikhyatk/moondream |

***

### SmolVLM2 (256M / 500M / 2.2B)

HuggingFace's SmolVLM2 family is purpose-built for resource-constrained local inference. The 2.2B variant achieves a combined benchmark score of **59.8%** across nine demanding VL benchmarks, while the 500M reaches 51% and the 256M hits 44%. SmolVLM2-2.2B delivers strong performance on OCRBench, MathVista, AI2D, and ScienceQA. Critically for a pipeline context, research validated **2.12× real-world speedup** using content-based prefix caching on Apple Silicon with MLX for repeated image queries.[^7][^8][^9]

SmolVLM2 natively handles **multi-image input**, which is essential for comparing a candidate sprite against a reference. Memory footprint is extremely low — the 2.2B model runs comfortably on hardware that would choke on larger models. It performs on par with or beats InternVL2-2B on most benchmarks despite its lower nominal parameter count.[^8][^7]

| Property | Value |
|----------|-------|
| Parameters | 256M / 500M / 2.2B |
| VRAM (2.2B, 4-bit) | ~2 GB |
| Apple Silicon | Full MLX support, tested on Apple Silicon in research paper[^9] |
| NVIDIA | HuggingFace Transformers, CUDA |
| Multi-image | Yes (natively) |
| Structured output | Via prompting |
| Fine-tunable | Yes (LoRA), well-documented examples[^2] |
| GitHub | github.com/huggingface/smollm |

***

### PaliGemma 2 (3B)

Google's PaliGemma 2 combines SigLIP-So400m vision encoder with Gemma 2 language models and is released in 3B, 10B, and 28B variants, each trained at 224px², 448px², and 896px² resolutions. The design philosophy is explicitly as a **transfer/fine-tuning model** — PaliGemma 2 is intended to be fine-tuned, not used zero-shot. For your use case this is both a strength and a caveat: it excels if you invest in fine-tuning but underperforms zero-shot compared to instruction-tuned models.[^10][^11]

The 3B model has been converted to MLX format by the community. PaliGemma 2 requires careful learning-rate tuning when fine-tuning; the 3B has a smaller optimal transfer LR than the original PaliGemma. **Critical limitation: PaliGemma 2 is a single-image model** — it does not natively support multi-image comparison in one call, which matters if your scoring prompt compares two sprites simultaneously.[^12][^11]

| Property | Value |
|----------|-------|
| Parameters | 3B (also 10B, 28B) |
| VRAM (3B, 8-bit) | ~4 GB |
| Apple Silicon | MLX community conversions available[^12] |
| NVIDIA | HuggingFace Transformers, JAX/Flax |
| Multi-image | No (single-image architecture) |
| Structured output | Via fine-tuning/prompting |
| Fine-tunable | Exceptional — designed for it[^11][^13] |
| GitHub | github.com/google-research/big_vision |

***

### Phi-4-Multimodal (5.6B)

Microsoft's Phi-4-Multimodal uses a "mixture of LoRAs" approach — a frozen 3.8B Phi-4-Mini core with a 370M vision LoRA and 460M audio LoRA. Across 11 text-vision benchmarks it ranked 4th among 11 models, outperforming Qwen2.5-VL-3B, Claude 3.5 Sonnet, and GPT-4o-mini while trailing Qwen2.5-VL-7B. It is released under MIT license, supports multi-image inference, and delivers excellent performance per parameter for math/science visual reasoning.[^14][^15][^16]

At ~11–12 GB in BF16 or ~6 GB in 4-bit, it fits comfortably on both hardware targets. However, native MLX support is less mature than Qwen's ecosystem, and GGUF conversion is community-maintained. The model is not yet in Ollama's default library as of April 2026, though `llama.cpp`-based loading works.

| Property | Value |
|----------|-------|
| Parameters | 5.6B total (3.8B active for vision tasks) |
| VRAM (4-bit) | ~6 GB |
| Apple Silicon | llama.cpp, community MLX |
| NVIDIA | HuggingFace Transformers, CUDA |
| Multi-image | Yes |
| Structured output | Yes |
| Fine-tunable | Yes (LoRA on vision adapter) |
| GitHub | github.com/microsoft/Phi-3CookBook |

***

### Qwen2.5-VL (3B / 7B)

**Top recommendation for this use case.** Qwen2.5-VL's native dynamic resolution encodes images at their actual pixel scale without normalization, making it better suited for analyzing content with exact pixel-level detail. It natively produces **structured JSON output** including bounding box coordinates and confidence values. Multi-image comparison is a first-class feature. The model is officially on Ollama and has mature MLX-VLM support.[^17][^18][^19][^20][^21][^22]

On image classification benchmarks, Qwen2-VL-7B trailed GPT-4o by only ~1 accuracy point while consuming 29GB for BF16 batch inference. With 4-bit quantization (~8GB VRAM), the 7B model runs at ~40–55 tokens/second on M4 Pro 48GB via MLX (M4 Max 64GB benchmarks show ~67 tokens/second for Qwen2.5-7B 3-bit) and ~100–130 tokens/second on the RTX 5080 with vLLM or llama.cpp. For a 200-token structured quality evaluation response, that translates to **1.5–5 seconds per image** — well within your 10-second target.[^23][^24]

The 3B model cuts VRAM to ~4GB and runs faster (80–100+ tok/s on M4 Pro), at a moderate accuracy cost. GGUF quantization support is excellent; Q4_K_M is recommended as the sweet spot. Fine-tuning with LoRA/QLoRA is well-documented and has been validated on RTX 4070 12GB hardware.[^25][^26]

| Property | Value |
|----------|-------|
| Parameters | 3B / 7B |
| VRAM (7B, 4-bit) | ~8 GB |
| VRAM (3B, 4-bit) | ~4 GB |
| Apple Silicon (MLX) | Yes — native via MLX-VLM[^27][^28] |
| NVIDIA | vLLM, Ollama, llama.cpp GGUF, HF Transformers |
| Multi-image | Yes (native) |
| Structured output | Native JSON |
| Fine-tunable | Yes, LoRA/QLoRA extensively documented[^29][^26][^30] |
| GitHub | github.com/QwenLM/Qwen2.5-VL |

***

### InternVL3 (2B / 8B) and InternVL3.5

InternVL3's ViT-MLP-LLM architecture with Variable Visual Position Encoding (V2PE) provides strong performance across fine-grained understanding tasks. The 2B model pairs InternViT-300M with Qwen2.5-1.5B; the 8B uses InternViT-300M with Qwen2.5-7B. **InternVL3.5** (the latest release) introduces a Visual Resolution Router that dynamically adjusts resolution processing, achieving a **4.05× inference speedup** over InternVL3 with a +16% reasoning gain.[^31][^32][^33]

InternVL3-8B BF16 requires ~16–17GB VRAM — it fits on the RTX 5080 16GB at 8-bit quantization, but 4-bit is recommended for headroom. AWQ quantization is available but shows a ~73% slowdown vs BF16 on vLLM. Multi-image and video support is native. The model family has comprehensive fine-tuning documentation and strong benchmark performance approaching GPT-4V-level on document/chart understanding.[^34][^35][^36]

| Property | Value |
|----------|-------|
| Parameters | 2B / 8B (also 14B, 38B) |
| VRAM (8B, 4-bit) | ~8–9 GB |
| Apple Silicon | Community MLX conversions; less mature than Qwen |
| NVIDIA | vLLM, HF Transformers |
| Multi-image | Yes (native) |
| Structured output | Via prompting |
| Fine-tunable | Yes (LoRA) |
| GitHub | github.com/OpenGVLab/InternVL |

***

## Medium Models (8B–32B Parameters)

### LLaMA 4 Scout (109B MoE / 17B active)

LLaMA 4 Scout has 109B total parameters but only **17B active per token** due to its 16-expert MoE design. Unsloth's 1.78-bit quantization brings the model to **33.8GB** — which technically fits in 48GB unified memory. However, this is an extremely aggressive quantization, and quality at 1.78-bit will be substantially degraded compared to 4-bit. On the RTX 5080 (16GB), Scout does **not fit** even with 4-bit quantization (~55GB required).[^37][^38][^39]

Ollama added Scout support via its new multimodal engine with custom chunked attention. The model's early-fusion native multimodality makes it strong for vision tasks, but for a sprite QA pipeline the overhead of running a 109B-total model is hard to justify unless quality at 1.78-bit proves viable (which would require your own testing). **Not recommended as a primary pipeline model** given hardware constraints, but interesting for quality validation benchmarking.[^40]

| Property | Value |
|----------|-------|
| Parameters | 109B total / 17B active |
| VRAM for 48GB fit | Unsloth 1.78-bit (33.8GB) only[^39] |
| VRAM (4-bit) | ~55GB — does not fit on either target GPU[^37] |
| Apple Silicon | Unsloth 1.78-bit via Ollama or llama.cpp |
| NVIDIA RTX 5080 | No — VRAM insufficient |
| Multi-image | Yes (early fusion) |
| Structured output | Yes |

***

### InternVL3 14B / InternVL3.5

InternVL3-14B requires ~28GB VRAM in BF16 and ~14GB at 4-bit — it fits on the RTX 5080 at 4-bit. On the M4 Pro 48GB, 4-bit via MLX is feasible. InternVL3.5 at the 14B scale represents a meaningful quality jump over the 8B while remaining practical on your hardware. For the 8B vs 14B decision on RTX 5080: 8B at 8-bit or 14B at 4-bit both require ~8–14GB and both fit.

***

### Qwen2.5-VL-72B (Quantized)

At 4-bit, Qwen2.5-VL-72B requires ~38–40GB VRAM — exceeding the RTX 5080's 16GB but fitting within the M4 Pro's 48GB unified memory. Running via MLX-VLM with 4-bit quantization, a Mac Mini M4 Pro 64GB achieved ~5.5 tokens/second. On M4 Pro 48GB, this is borderline and may require aggressive quantization that degrades quality. The 72B model at 4-bit is recommended only if the 7B fine-tuned still misses quality targets.[^41]

***

### DeepSeek-VL2 (Tiny / Small)

DeepSeek-VL2 uses a MoE architecture: Tiny is 3.37B total / 1.0B active, Small is 16.1B total / 2.8B active. The official documentation shows Tiny requiring "<40GB" GPU memory, which appears conservative and likely refers to non-optimized inference. Community testing showed the Tiny model running on a 9GB GPU peak VRAM with quantization. **Apple Silicon support is limited** — no native MLX conversions are widely available and the custom MoE architecture requires specific PyTorch dependencies. Fine-tuning community is small compared to Qwen or InternVL.[^42][^43]

***

### Pixtral 12B (Mistral)

Pixtral 12B requires ~24GB VRAM in BF16; Q4 quantization brings it down to ~12GB, which fits the RTX 5080 with 4GB headroom. It is supported via Ollama's new multimodal engine (as Mistral Small 3.1) and works with llama.cpp GGUF. MLX-VLM has support for Mistral vision models. Multi-image support is native. At ~12B parameters, it sits between the 7B and larger tiers in quality. For the RTX 5080, Pixtral 12B at Q4 is a practical option if 7B quality is insufficient and you're NVIDIA-primary.[^27][^44][^45][^40]

***

## Hardware-Specific Deployment Summary

| Model | M4 Pro 48GB | RTX 5080 16GB | Est. Speed (M4 Pro) | Est. Speed (RTX 5080) |
|-------|------------|---------------|---------------------|----------------------|
| Moondream 2B (4-bit) | ✅ ~2.5GB | ✅ ~2.5GB | ~60–80 tok/s | ~180–200 tok/s |
| SmolVLM2-2.2B (4-bit) | ✅ ~2GB | ✅ ~2GB | ~100–130 tok/s | ~220+ tok/s |
| PaliGemma 2-3B (8-bit) | ✅ ~4GB | ✅ ~4GB | ~70–90 tok/s | ~160 tok/s |
| Phi-4-Multimodal (4-bit) | ✅ ~6GB | ✅ ~6GB | ~40–60 tok/s | ~120–140 tok/s |
| Qwen2.5-VL-3B (4-bit) | ✅ ~4GB | ✅ ~4GB | ~80–100 tok/s | ~180 tok/s |
| **Qwen2.5-VL-7B (4-bit)** | ✅ ~8GB | ✅ ~8GB | **~40–55 tok/s** | **~100–130 tok/s** |
| InternVL3-8B (4-bit) | ✅ ~9GB | ✅ ~9GB | ~35–50 tok/s | ~90–120 tok/s |
| Pixtral 12B (Q4) | ✅ ~12GB | ✅ ~12GB | ~20–30 tok/s | ~60–80 tok/s |
| InternVL3-14B (4-bit) | ✅ ~14GB | ✅ ~14GB | ~18–25 tok/s | ~55–70 tok/s |
| Qwen2.5-VL-72B (4-bit) | ✅ ~38–40GB | ❌ Too large | ~5–8 tok/s | N/A |
| LLaMA 4 Scout (4-bit) | ❌ ~55GB | ❌ Too large | N/A | N/A |
| LLaMA 4 Scout (1.78-bit) | ⚠️ ~34GB | ❌ Too large | ~10–15 tok/s | N/A |

*Speed estimates based on M4 Pro ~273 GB/s bandwidth, RTX 5080 ~132 tok/s for 8B Q4, and published community benchmarks. Multimodal models may be 30–50% slower than text-only models of same size due to vision encoding overhead.*[^46][^47]

***

## Quantization Options and Quality Tradeoffs

For GGUF/llama.cpp and Ollama (both hardware targets):

- **Q8_0**: Near-lossless, ~1.1× model size reduction. Best for models where quality is paramount and VRAM allows.
- **Q4_K_M**: The recommended sweet spot — 4× size reduction with acceptable quality loss. The gap between Q4_K_M and FP16 is difficult to perceive in most tasks. **Start here.**[^25]
- **Q3**: Quality noticeably drops; only use if VRAM is severely constrained.[^25]
- **AWQ**: Available for Qwen2.5-VL and InternVL models. CUDA-optimized, but ~40–70% slower than BF16 on vLLM due to immature kernel support. Avoid for latency-critical pipelines.[^36]
- **GPTQ-Int4/Int8**: Good for NVIDIA deployments via vLLM; generally faster than AWQ for throughput.

For Apple Silicon (MLX):
- MLX 4-bit is 56% faster than Ollama GGUF for the same model. Use MLX-VLM, not GGUF, as your primary Mac backend.[^48]
- The vllm-mlx framework achieves 21–87% higher throughput than llama.cpp and provides a **28× speedup for repeated image queries** via content-based prefix caching — critical for batch pipelines where the same reference sprite appears repeatedly.[^49][^50]

***

## The Critical Question: Local VLM vs. Frontier API Accuracy Gap

For **fine-grained visual comparison of two similar small images** — specifically pixel art sprites — the accuracy picture is nuanced and important to understand clearly.

### The Zero-Shot Gap Is Real

In zero-shot, domain-agnostic tasks, GPT-4o and Gemini 2.5 Pro hold a meaningful lead over open-source models, particularly for fine-grained discrimination. A study on image quality assessment found that "only the closed-source GPT-4V provides a reasonable account for human perception of image quality, but is weak at discriminating fine-grained quality variations... and at comparing visual quality of multiple images". Multi-image comparison benchmarks show a significant performance gap between open-source and API models. One benchmark showed a 13–14% gap between open and API models on fine-grained tasks.[^51][^52][^53]

For **pixel art specifically**, all models — frontier and local alike — are working outside their training distribution. Standard VLMs are trained on natural photographs, web images, and document scans. Pixel art with deliberate 8×8 to 32×32 sprite work, color palette constraints, and sub-pixel animation is not represented in any published training set. This means the zero-shot baseline for even GPT-4o on pixel art quality rubrics will be weaker than on natural image tasks, partially narrowing the practical gap.

### Fine-Tuning Closes the Gap Dramatically

This is the most important finding: **a fine-tuned 8B model matched the accuracy of models 30× its size** on a specialized visual task (OCR/structured extraction) with domain-specific fine-tuning. After fine-tuning, the error rate dropped by half compared to the base model, and the error rate for a specific sub-task dropped from 4.6% to 0.0%. The fine-tuning took approximately one day and cost ~$100 on cloud hardware.[^1]

For your sprite QA pipeline, this suggests the following strategy:
1. Collect 200–500 labeled examples of "good" vs. "bad" sprites across your quality criteria.
2. Fine-tune Qwen2.5-VL-7B (or InternVL3-8B) with LoRA/QLoRA on your RTX 5080 (12GB VRAM is sufficient for QLoRA).[^26]
3. The fine-tuned local model will likely match or closely approach frontier API quality for your specific rubric, while eliminating API costs and latency.

**Recommendation:** Use Gemini 2.5 Pro or GPT-4o to label your training dataset (it's cost-effective to label 500 images via API), then fine-tune a local 7B model. This hybrid approach gets you frontier-quality annotations for training, then full local inference permanently.

***

## Apple Silicon Serving Frameworks

### MLX-VLM (Primary Recommendation for Mac)

MLX-VLM by Prince Canuma is the most mature Apple Silicon VLM framework. It supports inference and fine-tuning of vision-language and omni models via MLX. Features include CLI, Python API, Gradio demo, FastAPI server, LoRA/QLoRA fine-tuning, and multimodal support (images, audio, video). Supported models include Qwen2.5-VL, Mistral/Pixtral, PaliGemma, InternVL, and many others.[^54][^55][^19][^27]

```bash
pip install mlx-vlm
python -m mlx_vlm.generate --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit \
  --image sprite1.png --image sprite2.png \
  --prompt "Compare these two sprites and score: [clarity, color accuracy, animation frame consistency] 0-10"
```

### vllm-mlx (High-Throughput Batch Processing)

For batch pipeline workloads, vllm-mlx adds **continuous batching** and **prefix caching** on top of MLX. The prefix caching is especially relevant: if your pipeline sends the same reference sprite repeatedly for comparison, the vision encoding is computed once and cached, reducing latency from 21.7 seconds to under 1 second on cached queries. Published at EuroMLSys '26, it achieves 21–87% higher throughput than llama.cpp across tested models.[^50][^49]

### Ollama (Ease of Use)

Ollama's May 2025 multimodal engine update added proper support for Qwen2.5-VL, Llama 4, Gemma 3, and Mistral Small 3.1. The new engine separates vision and text decoding into distinct modules for better reliability. For a pipeline requiring OpenAI-compatible API, Ollama is the fastest way to get running. Use GGUF Q4_K_M for Qwen2.5-VL-7B via Ollama, but note it will be ~56% slower than the MLX path.[^56][^48][^40]

***

## Fine-Tuning for Sprite-Specific Quality Assessment

All top-tier models support LoRA fine-tuning, but the practical experience varies significantly:

### Qwen2.5-VL-7B (Best Fine-Tuning Choice)

LoRA fine-tuning with 4-bit quantization (QLoRA) is well-documented and validated on consumer hardware as low as an RTX 4070 12GB. Your RTX 5080 with 16GB VRAM can fine-tune the full 7B model with QLoRA comfortably. Key notes from practice:[^26]
- **Sensitive to grayscale images** — normalize pixel values consistently before training.[^57]
- Pixel art sprites are effectively high-contrast, low-palette images that may behave similarly to grayscale; consistent normalization matters.
- Use LoRA rank 4, alpha 16 as a starting point.[^26]
- Unsloth integration reduces memory overhead significantly.[^57]

### PaliGemma 2-3B (Best Fine-Tuning Architecture)

Designed explicitly as a transfer model, PaliGemma 2 often achieves better transfer efficiency than instruction-tuned models when fine-tuned on a small dataset. Fine-tuning for 8 epochs with LR 5e-6 is a validated starting point. The tradeoff is lack of multi-image support and less mature MLX/GGUF ecosystem.[^11]

### SmolVLM2 (Fastest Fine-Tuning Iteration)

SmolVLM2's tiny size makes fine-tuning iteration extremely fast — full fine-tune in minutes on a single GPU rather than hours. For rapid experimentation on your quality rubric, this is the best model for "fail fast / iterate fast" prototyping.[^2]

### Dataset Size Requirements

LoRA fine-tuning produces meaningful results with "a few hundred high-quality examples". For a binary "good vs. bad" sprite quality classifier with 4–5 quality dimensions, 200–400 labeled examples should be sufficient for initial fine-tuning. Quality matters more than volume for LoRA adaptation.[^58]

***

## Issues with Small Images and Pixel Art

Several potential issues to test before committing to a model:

1. **Upsampling behavior**: Most VLMs resize images to a minimum token dimension. A 128×128 sprite may be upsampled to 224×224 or 448×448. This is actually beneficial for pixel art — upscaling provides more tokens representing each pixel, improving the model's ability to reason about individual pixels. Qwen2.5-VL's native dynamic resolution handles this transparently.[^20]

2. **Pixel repetition artifacts**: When a VLM upsamples a pixel art image, sharp edges may be preserved or blurred depending on the interpolation method. In testing, Qwen2.5-VL's vision encoder is reported to handle low-resolution inputs reasonably well due to its variable resolution training.

3. **Domain mismatch**: Pixel art uses intentional dithering, limited palettes, and sub-pixel animation conventions that no model has seen in training. Zero-shot models will attempt to evaluate pixel art against natural image quality criteria (photo realism, smooth gradients) — producing nonsensical scores without careful prompting or fine-tuning.

4. **Pixel value normalization**: Qwen2.5-VL can be sensitive to inconsistent grayscale normalization. For color sprites, this is less concerning, but ensure preprocessing is consistent across your pipeline.[^57]

5. **Compressed image robustness**: VLMs struggle significantly with heavily compressed images; below 0.1 bpp, semantic understanding degrades. PNG (lossless) format is strongly recommended for your pipeline over JPEG.[^59]

***

## Framework Comparison: Ollama vs. LM Studio vs. MLX-VLM

| Feature | Ollama | LM Studio | MLX-VLM |
|---------|--------|-----------|---------|
| Apple Silicon optimization | GGUF (llama.cpp) | GGUF (llama.cpp) | Native MLX (fastest)[^48] |
| Vision model support | Yes (new engine)[^40] | Yes (GGUF) | Yes (primary purpose)[^19] |
| API interface | OpenAI-compatible REST | OpenAI-compatible REST | Python + FastAPI |
| Batch processing | Limited | Limited | Prefix caching, batching[^50] |
| Ease of setup | Easiest | Easy | Moderate |
| Fine-tuning | No | No | Yes (LoRA/QLoRA)[^54] |
| Speed vs. GGUF | Baseline | Baseline | +56% on 7B models[^48] |
| Multi-image | Via new engine | Via GGUF models | Yes |
| Recommended use | Quick prototyping | GUI-based testing | Production pipeline |

***

## Recommended Pipeline Architecture

Given your specific constraints — automated pipeline, 8–120 images/batch, <10s latency, fully offline, M4 Pro 48GB primary — the following architecture is recommended:

**Primary (Mac, daily use):**
- Model: Qwen2.5-VL-7B-Instruct, 4-bit MLX quantization
- Framework: MLX-VLM with vllm-mlx prefix caching for batch efficiency
- Expected throughput: ~40–55 tokens/second; a 200-token evaluation response ~4–5 seconds per image
- Multi-image mode: Pass reference sprite + candidate in single call for pairwise scoring

**Secondary (NVIDIA, high-throughput batch runs):**
- Model: Qwen2.5-VL-7B-Instruct, Q4_K_M GGUF or FP8 via vLLM
- Framework: vLLM with CUDA
- Expected throughput: ~100–130 tokens/second; ~1.5–2 seconds per image
- Well within 10s/image at batch sizes up to 120

**Quality Ceiling (when accuracy is paramount):**
- Model: Qwen2.5-VL-72B, 4-bit MLX on M4 Pro 48GB
- Expected: ~5–8 tokens/second; ~25–40 seconds per image — outside your 10s target
- Alternative: LLaMA 4 Scout at 1.78-bit Unsloth quantization via Ollama (~10–15 tok/s, ~13–20s) — borderline on latency

**Recommended fine-tuning workflow:**
1. Use Gemini 2.5 Pro API to generate quality labels for 300–500 diverse sprite examples
2. Fine-tune Qwen2.5-VL-7B with QLoRA via Unsloth on the RTX 5080 (16GB sufficient)
3. Re-evaluate vs. frontier API to measure domain-specific accuracy gap
4. Ship fine-tuned local model for all production inference

***

## Notable 2025–2026 Papers

- **Phi-4-Mini & Phi-4-Multimodal** (arXiv 2503.01743, March 2025): Microsoft's mixture-of-LoRAs multimodal architecture enabling multi-modal inference without interference[^60]
- **SmolVLM** (arXiv 2504.05299, April 2025): HuggingFace's systematic design of efficient VLMs at 256M–2.2B scale with strong multi-image capabilities[^8]
- **InternVL3** (arXiv 2504.10479, April 2025): Variable Visual Position Encoding and InternEVO training achieving 50–200% training speedup[^32]
- **vllm-mlx** (arXiv 2601.19139, January 2026, EuroMLSys '26): Native MLX inference framework with 28× multimodal speedup via content-based prefix caching[^50]
- **Benchmarking VLMs for Compressed Images** (arXiv 2512.20901, December 2025): Key finding that scaling model size does not consistently improve compression artifact robustness — breaking expected scaling laws[^59]
- **Qwen2.5-VL Technical Report** (arXiv 2502.13923, February 2025): Full architecture and benchmark details for the Qwen2.5-VL series[^61]
- **Attention-Aware Multi-Level Caching for VLM Inference** (IEEE 2026): Apple Silicon MLX validation showing 2.12× speedup with L2 caching on SmolVLM2[^9]

---

## References

1. [End-to-End OCR with Vision Language Models - Ubicloud](https://www.ubicloud.com/blog/end-to-end-ocr-with-vision-language-models) - Even better, by fine-tuning for a specific use-case, smaller models can perform as well as frontier-...

2. [Top Vision Models 2025 - Trelis Research](https://trelis.substack.com/p/top-vision-models-2025) - - SmolVLM by HuggingFace: 250M/500M param variants using pixel mixing for efficiency. - Qwen 2.5-VL:...

3. [moondream/moondream-2b-2025-04-14-4bit - Hugging Face](https://huggingface.co/moondream/moondream-2b-2025-04-14-4bit) - On an Nvidia RTX 3090, it uses 2,450 MB of VRAM and runs at a speed of 184 tokens/second. We used qu...

4. [Moondream 2025-03-27 Release](https://moondream.ai/blog/moondream-2025-03-27-release) - While we don't have a public benchmark available to highlight, our internal benchmark and vibe check...

5. [Underdog VLM: Moondream 3.0 with Only 2B Activated Parameters ...](https://www.aibase.com/news/www.aibase.com/news/21621) - Moondream 3.0 adopts an innovative MoE architecture, with a total of 9B parameters but only 2B activ...

6. [Moondream Docs: Overview](https://docs.moondream.ai) - Here are some early benchmark results. We show it alongside some top frontier models for comparison....

7. [SmolVLM to SmolVLM2: Compact Models for Multi-Image VQA](https://pyimagesearch.com/2025/06/23/smolvlm-to-smolvlm2-compact-models-for-multi-image-vqa/) - In this blog post, we explore the design and capabilities of SmolVLM and its successor, SmolVLM2, tw...

8. [SmolVLM: Redefining small and efficient multimodal models - arXiv](https://arxiv.org/html/2504.05299v1)

9. [Attention-Aware Multi-Level Caching for Efficient Multimodal Vision-Language Inference](https://ieeexplore.ieee.org/document/11393741/) - Multimodal vision-language models (VLMs) have achieved remarkable capabilities but suffer from high ...

10. [PaliGemma 2: A Family of Versatile VLMs for Transfer](https://arxiv.org/abs/2412.03555) - PaliGemma 2 is an upgrade of the PaliGemma open Vision-Language Model (VLM)
based on the Gemma 2 fam...

11. [PaliGemma 2: A Family of Versatile VLMs for Transfer - arXiv](https://arxiv.org/html/2412.03555v1) - PaliGemma 2 is an upgrade of the PaliGemma open Vision-Language Model (VLM) based on the Gemma 2 fam...

12. [mlx-community/paligemma-3b-mix-224-8bit - Hugging Face](https://huggingface.co/mlx-community/paligemma-3b-mix-224-8bit) - This model was converted to MLX format from google/paligemma-3b-mix-224 using mlx-vlm version 0.1.0....

13. [How to Fine-tune PaliGemma 2 - Roboflow Blog](https://blog.roboflow.com/fine-tune-paligemma-2/) - This tutorial will demonstrate how to fine-tune PaliGemma 2 using Google Colab to extract data from ...

14. [Phi-4 Multimodal (Text+Image+Audio) - Best Multimodal SLM Out There?](https://newsletter.victordibia.com/p/phi-4-multimodal-textimageaudio-best) - #31 | I tested the recently released Phi-4 multimodal model - it's impressive!

15. [Microsoft's Phi-4 Multimodal Model Can Process Text, Images, and ...](https://www.deeplearning.ai/the-batch/microsofts-phi-4-multimodal-model-can-process-text-images-and-speech-simultaneously/) - Microsoft debuted its first official large language model that responds to spoken input.

16. [Empowering innovation: The next generation of the Phi family](https://azure.microsoft.com/en-us/blog/empowering-innovation-the-next-generation-of-the-phi-family/) - We are excited to announce Phi-4-multimodal and Phi-4-mini, the newest models in Microsoft’s Phi fam...

17. [qwen2.5vl - Ollama](https://ollama.com/library/qwen2.5vl) - Flagship vision-language model of Qwen and also a significant leap from the previous Qwen2-VL.

18. [Ollama¶](https://qwen.readthedocs.io/en/latest/run_locally/ollama.html)

19. [MLX-VLM is a package for inference and fine-tuning of ... - GitHub](https://github.com/Blaizzy/mlx-vlm) - MLX-VLM is a package for inference and fine-tuning of Vision Language Models (VLMs) and Omni Models ...

20. [Qwen2-VL: Enhancing Vision-Language Model's Perception ... - arXiv](https://arxiv.org/html/2409.12191v1) - Qwen2-VL introduces the Naive Dynamic Resolution mechanism, which enables the model to dynamically p...

21. [Qwen2.5 VL! Qwen2.5 VL! Qwen2.5 VL! | Qwen](https://qwenlm.github.io/blog/qwen2.5-vl/) - 5-VL supports structured outputs of their contents, benefiting usages in finance, commerce, etc. ......

22. [Qwen/Qwen2.5-VL-3B/7B/72B-Instruct are out!! : r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1itq30t/qwenqwen25vl3b7b72binstruct_are_out/) - The key enhancements of Qwen2.5-VL are: Visual Understanding: Improved ability to recognize and anal...

23. [Geekerwan benchmarked Qwen2.5 7B to 72B on new M4 Pro and ...](https://www.reddit.com/r/LocalLLaMA/comments/1gmi2em/geekerwan_benchmarked_qwen25_7b_to_72b_on_new_m4/) - Only the Max models can run the 72B model at reasonable speed, around 9 tokens per second for M4 Max...

24. [Benchmarking Top Vision Language Models (VLMs) for Image ...](https://www.clarifai.com/blog/best-vision-language-models-vlms-for-image-classification-performance-benchmarks) - The primary goal of this blog is to benchmark Top Vision Language Models on an image classification ...

25. [Qwen2.5-VL-7B-Instruct-GGUF : Which Q is sufficient for OCR text?](https://www.reddit.com/r/LocalLLaMA/comments/1ntbzqw/qwen25vl7binstructgguf_which_q_is_sufficient_for/) - Qwen2.5-VL-7B-Instruct-GGUF : Which Q is sufficient for OCR text?

26. [How to Fine-Tune Qwen2.5-VL | Datature Blog](https://datature.com/blog/how-to-fine-tune-qwen2-5-vl) - Learn how to train Qwen2.5-VL to automatically detect and describe objects in images. This guide cov...

27. [Running Vision Models on Apple Silicon with MLX-VLM - YouTube](https://www.youtube.com/watch?v=DUwo11iOnCk) - I show and explain how to run Qwen and Mistral vision models on Apple Silicon with MLX-VLM. I share ...

28. [Structured Data Annotation with Qwen2.5 VL and MLX-VLM](https://www.youtube.com/watch?v=2Ojtc9mdEes) - Qwen2.5 VL can provide bounding box coordinates and confidence values for extracted structured data....

29. [How to Fine-Tune Qwen2.5-VL with a Custom Dataset - Roboflow Blog](https://blog.roboflow.com/fine-tune-qwen-2-5/) - Learn how to fine-tune Qwen2.5-VL for document processing using a custom dataset.

30. [Fine-Tuning the Qwen2.5-7B-VL-Instruct Model - Aman Blog](https://connectaman.hashnode.dev/fine-tuning-the-qwen25-7b-vl-instruct-model-a-comprehensive-guide) - In this blog post, we explore the intricacies of fine-tuning the Qwen2.5-7B-VL-Instruct model—a stat...

31. [OpenGVLab/InternVL3-2B - Hugging Face](https://huggingface.co/OpenGVLab/InternVL3-2B) - We introduce InternVL3, an advanced multimodal large language model (MLLM) series that demonstrates ...

32. [InternVL3: Exploring Advanced Training and Test-Time Recipes for ...](https://arxiv.org/html/2504.10479v1) - As shown in Table 4, even the smallest variant in the InternVL3 family (InternVL3-1B) demonstrates p...

33. [cyankiwi/InternVL3_5-8B-AWQ-8bit - Hugging Face](https://huggingface.co/cyankiwi/InternVL3_5-8B-AWQ-8bit) - 5 to achieve up to a +16.0% gain in overall reasoning performance and a 4.05 × \times × inference sp...

34. [Introduction of InternVL2 Series - InternVL's tutorials! - Read the Docs](https://internvl.readthedocs.io/en/latest/internvl2.0/introduction.html) - InternVL 2.0 features a variety of instruction-tuned models, ranging from 1 billion to 108 billion p...

35. [Mini-InternVL 2.0: A Flexible-Transfer Pocket Multimodal ...](https://internvl.github.io/blog/2024-10-21-Mini-InternVL-2.0/)

36. [[Bug] InternVL3-8B-AWQ is much slower than InternVL3-8B - GitHub](https://github.com/OpenGVLab/InternVL/issues/1057) - I'm using InternVL3-8B-AWQ to inference on vLLM, which is much slower than InternVL3-8B. The decive ...

37. [Llama 4 Scout and Maverick Are Here—How Do They Shape Up?](https://www.runpod.io/blog/llama4-scout-maverick) - Note, however, that these are MoE models unlike previous Llama models which were dense models—›so th...

38. [Llama 4 Scout: Specifications and GPU VRAM Requirements](https://apxml.com/models/llama-4-scout) - Hardware requirements are well-documented for various configurations. Meta and partners (NVIDIA, Uns...

39. [Llama 4: How to Run & Fine-tune | Unsloth Documentation](https://unsloth.ai/docs/models/tutorials/llama-4-how-to-run-and-fine-tune) - The Llama-4-Scout model has 109B parameters, while Maverick has 402B parameters. The full unquantize...

40. [Ollama's new engine for multimodal models](https://ollama.com/blog/multimodal-models) - Ollama now supports multimodal models via Ollama's new engine, starting with new vision multimodal m...

41. [Running Qwen2.5 72B 4bit VL on my Mac Mini M4 Pro 64GB with ...](https://www.linkedin.com/posts/andrej-baranovskij_running-qwen25-72b-4bit-vl-on-my-mac-activity-7290813395493163009-9WBI) - Running Qwen2.5 72B 4bit VL on my Mac Mini M4 Pro 64GB with MLX and MLX-VLM. Approx 5.5 tokens per s...

42. [DeepSeek VL2 Local Test and Install (A VERY Good Tiny VLM!)](https://www.youtube.com/watch?v=B3gJUKzPFU4) - Timestamps: 00:00 - Intro 02:55 - Technical Report 07:10 - Installation Tutorial 12:10 - Testing 16:...

43. [Quick Start | deepseek-ai/DeepSeek-VL2 | DeepWiki](https://deepwiki.com/deepseek-ai/DeepSeek-VL2/1.2-quick-start) - This guide provides practical examples to help you start using DeepSeek-VL2 quickly. It covers insta...

44. [Run Pixtral-12B-2409 locally - Beginners - Hugging Face Forums](https://discuss.huggingface.co/t/run-pixtral-12b-2409-locally/147785) - Ideally, you would need at least 25GB for Pixtral 12B. In addition to model loading, VRAM and RAM ar...

45. [Pixtral 12b GPU requirements : r/MistralAI - Reddit](https://www.reddit.com/r/MistralAI/comments/1l4xn6a/pixtral_12b_gpu_requirements/) - Professional-grade local AI on consumer hardware — 80B stable on 44GB mixed VRAM (RTX 5060 Ti ×2 + R...

46. [The Best GPUs for Local LLM Inference in 2025](https://localllm.in/blog/best-gpus-llm-inference-2025) - Comprehensive analysis of the best GPUs for local LLM inference in 2025, featuring RTX 5090 performa...

47. [A Deep Dive into MLX Performance on the M4 Max - LinkedIn](https://www.linkedin.com/pulse/running-llms-locally-your-mac-deep-dive-mlx-m4-max-travis-lelle-gp6ce) - On Apple Silicon, llama.cpp delivers solid performance - community benchmarks show around 150 tok/s ...

48. [Local LLM Speed: Qwen2 & Llama 3.1 Real Benchmark Results](https://singhajit.com/llm-inference-speed-comparison/) - What tokens per second can you expect running Qwen2 1.5B on M1 Mac or Llama 3.1 8B on RTX 4070? Real...

49. [Native LLM and MLLM Inference at Scale on Apple Silicon - arXiv](https://arxiv.org/html/2601.19139v1)

50. [Native LLM and MLLM Inference at Scale on Apple Silicon - arXiv](https://arxiv.org/abs/2601.19139) - The growing adoption of Apple Silicon for machine learning development has created demand for effici...

51. [GuessBench: Sensemaking Multimodal Creativity in the Wild](https://arxiv.org/abs/2506.00814) - We propose GuessBench, a novel benchmark that evaluates Vision Language Models (VLMs) on modeling th...

52. [Benchmarking Multi-Image Understanding in Vision and Language Models:
  Perception, Knowledge, Reasoning, and Multi-Hop Reasoning](https://arxiv.org/html/2406.12742) - ...to compare, analyze, and reason across
multiple images. Our benchmark encompasses four categories...

53. [A Comprehensive Study of Multimodal Large Language Models for Image
  Quality Assessment](https://arxiv.org/html/2403.10854v1) - ...transformations, and color differences) in both full-reference and
no-reference scenarios. Experi...

54. [MLX-VLM: Local-first toolkit for inference and fine-tuning of …jimmysong.io › mlx-vlm](https://jimmysong.io/ai/mlx-vlm/) - A local-first toolkit for inference and fine-tuning of vision-language and omni models using MLX, op...

55. [Multimodal AI Models on Apple Silicon with MLX with Prince Canuma](https://twimlai.com/podcast/twimlai/multimodal-ai-models-on-apple-silicon-with-mlx) - Today, we're joined by Prince Canuma, an ML engineer and open-source developer focused on optimizing...

56. [Ollama's new engine for multimodal models · Ollama Blog](https://ollama.com/blog/multimodal-models?trk=article-ssr-frontend-pulse_little-text-block) - Ollama now supports new multimodal models with its new engine.

57. [Fine-tuning Qwen 2.5-VL for a classification task using multiple images](https://www.reddit.com/r/MLQuestions/comments/1obk7hx/finetuning_qwen_25vl_for_a_classification_task/) - Hi, I don't know if that's the right place to ask, but I am using unsloth to do LoRA fine-tuning of ...

58. [Parameter-Efficient Fine-Tuning with LoRA Using Custom Data](https://www.digitalocean.com/community/tutorials/fine-tune-llms-with-lora-for-custom-domains) - LoRA can produce meaningful results with a relatively small dataset, often a few hundred high-qualit...

59. [Benchmarking and Enhancing VLM for Compressed Image ... - arXiv](https://arxiv.org/html/2512.20901v1) - To investigate the relationship between human vision and machine perception, we conducted a comparat...

60. [Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs](https://arxiv.org/abs/2503.01743) - We introduce Phi-4-Mini and Phi-4-Multimodal, compact yet highly capable language and multimodal mod...

61. [Qwen2.5-VL Technical Report](https://arxiv.org/pdf/2502.13923.pdf) - We introduce Qwen2.5-VL, the latest flagship model of Qwen vision-language
series, which demonstrate...

