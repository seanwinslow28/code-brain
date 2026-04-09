# Vision Model Comparison for AI Image Quality Assessment (2026)
### A Production Evaluation Guide for Pixel Art Sprite QA Pipelines

***

## Executive Summary

As of April 2026, **Gemini 2.5 Flash** and **OpenAI o4-mini** represent the best balance of vision accuracy, structured-reasoning capability, low latency, and cost efficiency for a production image quality assessment pipeline. For maximum fine-grained accuracy where cost is secondary, **OpenAI o3** or **Gemini 2.5 Pro** are top choices. Among open-source models, **InternVL3-78B** and **Qwen3-VL-32B** lead the field. One critical caveat applies across all models: **pixel art at 128×128 and 256×256 is below the resolution distribution that most VLMs were trained on**, and images should be upscaled (2–4×) before submission to any vision model to maximize accuracy.

***

## Benchmark Reference

The following benchmarks are relevant to evaluating models for image quality assessment:

- **MMMU**: Massive Multi-discipline Multimodal Understanding — college-level visual reasoning across 30 image types (charts, diagrams, art, etc.)[^1]
- **MMMU-Pro**: Harder variant of MMMU with stricter visual grounding requirements[^2]
- **MathVista**: Visual mathematical reasoning using diagrams, charts, and figures[^3]
- **DocVQA**: Visual question answering over document images — tests fine-grained text and structure reading[^4]
- **ChartQA**: Visual understanding of chart and graph images[^4]
- **OCRBench**: OCR and text recognition accuracy across diverse image types[^5]
- **OmniSpatial**: Comprehensive spatial reasoning across dynamic, logical, and perspective-taking tasks[^6]
- **VQualA 2025**: ICCV 2025 visual quality comparison challenge — pairwise and multi-image quality judgment[^7]
- **VideoGameQA-Bench**: VLM evaluation on game QA including visual regression testing and glitch detection[^8][^9]
- **OmniDiff**: Fine-grained image difference captioning benchmark (ICCV 2025)[^10]

***

## Closed-Source Models

### Google Gemini 2.5 Pro

Gemini 2.5 Pro is Google's flagship multimodal model, scoring **81.7% on MMMU** — among the highest of any model. On MMMU-Pro (the harder variant), it scores **75.2%**, and achieves **85.6% on ChartQA** and **80.3% on Video-MMMU**. It features a **1-million-token context window**, enabling large batches of comparison images per call. The model was designed as multimodal from the ground up, giving it a structural advantage in integrating visual and textual information simultaneously. On OmniSpatial spatial reasoning, it ranks second among all evaluated models at **49.52%**.[^11][^12][^13][^14]

For a pixel art QA pipeline, Gemini 2.5 Pro is the most capable model for complex structured evaluation rubrics paired with visual comparison. Its weakness is cost ($1.25–$2.50/1M input, $10–$15/1M output) and latency — at 117 tokens/sec it is capable but not blazing for high-volume throughput.[^15][^16]

### Google Gemini 2.5 Flash

The Flash variant achieves strong vision benchmark scores while dramatically improving latency (TTFT **0.45 seconds**, **206 tokens/sec output**). Pricing is $0.30/1M input and $2.50/1M output — roughly 4× cheaper than Pro. For a production pipeline targeting under-10-second evaluations at scale, Gemini 2.5 Flash is the most compelling closed-source option. It supports a 1M context window, enabling multiple reference and candidate images in a single call.[^17][^18][^19]

### OpenAI o3

OpenAI's o3 is a reasoning-native model that uniquely "thinks with images" — it can include visual content in its chain-of-thought. This gives it a distinctive advantage for comparative analysis: rather than generating a single-pass assessment, it iteratively reasons about the differences between images. It achieves **82.9% on MMMU** (the highest published closed-source score after Gemini 2.5 Pro), **86.8% on MathVista**, and **78.6% on CharXiv**. On OmniSpatial, it is competitive with Gemini 2.5 Pro. The model is best for highest-accuracy evaluations where latency is flexible — it is considerably slower than Flash or 4.1 due to extended reasoning chains.[^14][^20][^21]

### OpenAI o4-mini

o4-mini scores **81.6% on MMMU**, **84.3% on MathVista**, and **72.0% on CharXiv**, performing remarkably close to o3 at a fraction of the cost. Like o3, it reasons with images in its chain of thought, enabling step-by-step visual analysis. It is specifically described as optimized for "visual tasks" while maintaining speed. For a production pipeline where cost and throughput matter, o4-mini offers the best accuracy-per-dollar ratio among OpenAI's models. Input pricing is approximately $1.10/1M tokens, output $4.40/1M.[^22][^20][^23][^24]

### OpenAI GPT-4.1

GPT-4.1 scores **74.8% on MMMU**, **72.2% on MathVista**, and **87.9% on CharXiv-D** (scientific chart descriptions). It offers a **1-million-token context window** and pricing at $2.00/1M input, $8.00/1M output. Notably, GPT-4.1 Mini matches the full model on several vision benchmarks (MathVista 73.1% vs 72.2%), making it an attractive lower-cost option. GPT-4.1 excels at following structured JSON output formats and rubric-based scoring instructions — a key property for automated QA pipelines.[^25][^26][^3]

### Anthropic Claude Opus 4.1

Released in August 2025, Claude Opus 4.1 achieves **77.1% on MMMU** and **80.9% on GPQA**. Anthropic's API documentation confirms support for up to **600 images per API call** (100 for models with a 200K context window), making it exceptionally powerful for multi-image comparison. The 200K context window is smaller than Gemini 2.5 Pro's 1M but still substantial. Pricing has been reduced to $5/1M input, $25/1M output as of February 2026. Claude models are known for their ability to follow precise structured output formats and adhere strictly to rubrics — a meaningful practical advantage for evaluation pipelines.[^27][^28][^29][^30]

### Anthropic Claude Sonnet 4

Sonnet 4 achieves **74.4% on MMMU** at 5× lower cost than Opus 4.1 ($3/$15 per 1M tokens). It generates at 54.84 tokens/second, considerably faster than Opus 4.1 (38.93 tokens/sec). For a balanced production deployment of visual rubric evaluation where Opus-level accuracy is not required, Sonnet 4 is the pragmatic Anthropic choice.[^31][^27]

### xAI Grok-3 / Grok-4

Grok-3 achieves **78.0% on MMMU** and **84.6% on GPQA**, while Grok-4 scores higher on GPQA (87.5%) and MMLU-Pro (87%). xAI's earlier Grok-1.5V notably **outperformed GPT-4V on RealWorldQA** (68.7% vs. 61.4%) — a benchmark designed specifically to test spatial understanding in real-world photos. However, vision-specific benchmark data for Grok-4 remains sparse in public reporting. Both models are proprietary with API access through xAI.[^32][^33][^34]

***

## Open-Source Models

### InternVL3-78B (Shanghai AI Lab)

InternVL3-78B establishes the **state-of-the-art for open-source MMMU at 72.2%**. It also achieves **79.0% on MathVista**, **95.4% on DocVQA**, and **89.7% on both AI2D and ChartQA**. The model uses InternViT-6B as its vision encoder and Qwen2.5-72B as its language backbone. On multi-image and multi-modal benchmarks (BLINK, MMIU, MuirBench, MMT), InternVL3-78B scores 68.0% overall. InternVL3.5-241B (the MoE successor released August 2025) pushes MMMU to 77.7% — competitive with Claude Opus 4.1 — with a 4× inference speedup over InternVL3 via Visual Resolution Router (ViR).[^35][^36][^37][^38]

InternVL3-78B is available via third-party providers at $0.15/$0.60 per 1M tokens, making it dramatically cheaper than closed-source flagship models.[^39]

### Qwen3-VL (Alibaba)

Qwen3-VL-235B-A22B is Alibaba's most recent VLM (released November 2025), reaching **85.8% on MathVista**, **74.6% on MathVision**, and **96.5% on DocVQA**. It supports a native **256K token context window** integrating text, images, and video. The model achieves 875 points on OCRBench with support for 39 languages. Critically for multi-image comparison, the model was used as the base engine for the **VQualA 2025 Challenge winning ensemble** (alongside Qwen2.5-VL variants), which achieved 0.757 accuracy on fine-grained visual quality comparison tasks. The model is somewhat weaker on MMMU-Pro (69.3% vs GPT-5's 78.4%), reflecting specialization in visual math and documents rather than broad general reasoning. Available under Apache 2.0 (32B dense) and permissive MoE license. The 32B dense variant outperforms the much larger Qwen2.5-VL-72B across all 15 benchmarks tested.[^40][^41][^42][^43][^5][^7]

### Qwen2.5-VL-72B (Alibaba)

Still widely deployed, Qwen2.5-VL-72B scores **~72% on MMMU** and **67% on MathVista**  with notable strength in multi-language OCR and structured document parsing. Its dynamic resolution processing handles inputs of varying sizes well. Released under a semi-commercial license (Tongyi Qianwen). The VQualA 2025 challenge ensemble combined Qwen2.5-VL-7B and 72B for robust multi-image quality assessment.[^44][^7]

### LLaMA 4 Maverick (Meta)

LLaMA 4 Maverick achieves **73.4% on MMMU**, **73.7% on MathVista**, **94.4% on DocVQA**, and **90% on ChartQA**. It is a Mixture-of-Experts model with strong multi-image reasoning capability. Meta's model is available through major inference providers (Fireworks, Together, etc.) at competitive rates. Community license applies — commercial use generally permitted with conditions.[^45]

### DeepSeek-VL2 (DeepSeek)

DeepSeek-VL2 is a MoE VLM that achieves **93.3% on DocVQA**, **86.0% on ChartQA**, **84.2% on TextVQA**, and **81.1% on OCRBench**. It scores well on structural/document tasks and uses a dynamic tiling vision encoding approach with Multi-Head Latent Attention for efficiency. The model has a 259K context window. It is strong for text-heavy visual comparison but has limited published data on spatial reasoning tasks. Its primary limitation is API pricing through third parties can be unusually high ($9.50/$4800 per 1M in/out cited through one provider) — direct self-hosted weights are available under DeepSeek's open license.[^46][^47]

### Google Gemma 3 27B

Gemma 3 uses the SigLIP vision encoder, supports 128K context, and processes up to 29 languages. It achieves 87.1% on DocVQA but MMMU scores are below the Qwen/InternVL tier. It is fully open-weight and Apache 2.0 licensed.[^48][^49]

### Microsoft Phi-4 Multimodal

Phi-4 Multimodal is optimized for on-device and low-resource environments, excelling in scenarios where GPU memory is constrained. MMMU performance is below frontier open-source models. Best suited for edge deployment.[^48]

### Moondream2

Moondream2 scores 32.4% on MMMU and 24.3% on MathVista, reflecting its extremely small parameter count (~1.9B). However, it has a specialized segmentation engine with 88.2 mIoU on RefCOCO-M (as of March 2026) — meaning it excels at **locating objects within images** with pixel-accurate masks. For a QA pipeline that needs to identify *where* a visual error occurs (not just describe it), Moondream's segmentation capability is unique among small models. Not suitable as a primary evaluation judge.[^50][^51]

### SmolVLM 2.2B (Hugging Face)

SmolVLM achieves 38.8% on MMMU and 81.6% on DocVQA. The 2.2B model runs in ~5GB VRAM and was specifically extended to handle multi-image inputs. Not competitive with larger models for quality assessment but ideal for fine-tuning on a custom pixel art QA dataset.[^52][^50]

***

## Ranked Comparison Tables

### Closed-Source Vision Models

| Rank | Model | MMMU | MathVista | DocVQA | Spatial | Context | $/1M in | TTFT | Best For |
|------|-------|------|-----------|--------|---------|---------|---------|------|----------|
| 1 | **Gemini 2.5 Pro** | 81.7%[^12] | 77.5%[^13] | — | 49.5%[^14] | 1M | $1.25[^16] | ~2–5s | Highest accuracy, rubric evals |
| 2 | **OpenAI o3** | 82.9%[^21] | 86.8%[^21] | — | 46%+[^14] | 200K | $10[^23] | 10–30s | Deep visual reasoning via CoT |
| 3 | **OpenAI o4-mini** | 81.6%[^24] | 84.3%[^24] | — | Competitive[^14] | 200K | $1.10[^23] | 3–8s | Best accuracy/cost balance |
| 4 | **Gemini 2.5 Flash** | ~76%[^45] | — | — | Good | 1M | $0.30[^19] | 0.45s[^18] | Best production throughput |
| 5 | **Claude Opus 4.1** | 77.1%[^28] | — | — | Good | 200K | $5[^27] | ~3s | Multi-image batching (600 imgs)[^30] |
| 6 | **Grok-3** | 78.0%[^32] | — | — | Spatial strength[^34] | — | N/A | — | Strong spatial reasoning |
| 7 | **GPT-4.1** | 74.8%[^3] | 72.2%[^3] | — | Moderate | 1M | $2[^26] | ~2s | Structured outputs + rubrics |
| 8 | **Claude Sonnet 4** | 74.4%[^31] | — | — | Good | 200K | $3[^27] | Fast | Cost-balanced Anthropic |
| 9 | **GPT-4.1 Mini** | 59.4%[^25] | 73.1%[^3] | — | Moderate | 1M | $0.40[^25] | Very fast | Budget visual evals |

### Open-Source Vision Models

| Rank | Model | MMMU | MathVista | DocVQA | ChartQA | Context | License | Best For |
|------|-------|------|-----------|--------|---------|---------|---------|----------|
| 1 | **InternVL3.5-241B** | 77.7%[^35] | — | — | — | — | Apache 2.0 | Top open accuracy |
| 2 | **Qwen3-VL-235B** | 69.3% Pro[^5] | 85.8%[^42] | 96.5%[^42] | — | 256K[^41] | Apache 2.0 | Visual math + documents |
| 3 | **InternVL3-78B** | 72.2%[^38] | 79.0%[^37] | 95.4%[^36] | 89.7%[^36] | ~32K[^39] | Apache 2.0 | Best open MMMU; document QA |
| 4 | **LLaMA 4 Maverick** | 73.4%[^45] | 73.7%[^45] | 94.4%[^45] | 90%[^45] | 128K | Community | Balanced open-source |
| 5 | **Qwen3-VL-32B** | Beats 2.5-VL on all 15[^40] | — | — | — | 131K[^53] | Apache 2.0 | Efficient open flagship |
| 6 | **Qwen2.5-VL-72B** | ~72%[^44] | 67%[^44] | — | — | — | Qianwen | Mature, widely deployed |
| 7 | **DeepSeek-VL2** | — | — | 93.3%[^46] | 86%[^46] | 259K[^46] | DeepSeek | OCR + document tasks |
| 8 | **Gemma 3 27B** | Moderate | — | 87.1%[^49] | — | 128K | Apache 2.0 | Multilingual, easy to run |
| 9 | **Moondream2** | 32.4%[^50] | 24.3%[^50] | 70.5%[^50] | — | Small | Apache 2.0 | Pixel segmentation only |
| 10 | **SmolVLM 2.2B** | 38.8%[^50] | 44.6%[^50] | 81.6%[^50] | — | 16K[^52] | Apache 2.0 | Fine-tunable, edge device |

***

## Criteria Deep Dive

### Fine-Grained Visual Difference Detection

The **OmniDiff benchmark** (ICCV 2025) specifically evaluates the ability to describe subtle differences between image pairs across 12 distinct change types. This is closely aligned with the use case of comparing candidate sprite vs. reference sprite. The **VQualA 2025 Challenge** (also ICCV 2025) introduced the MICBench dataset with 4,000 human-annotated multi-image quality comparison questions and found that **ensemble approaches combining Qwen2.5-VL-7B, 72B, and LLaVA-OneVision performed best** — the winning team achieved 0.757 accuracy on pairwise quality comparison.[^10][^7]

Research published in mid-2025 found that VLMs "perform far worse than their encoders" on low-level visual matching tasks, with performance dropping as much as **45.5%** compared to using the vision encoder alone on precise pixel-level comparisons. This confirms that raw closed-source API calls are not perfect for sub-pixel analysis — structured prompting with specific comparison criteria significantly improves results.[^54]

For the pixel art use case, the recommended approach is:
1. **Upscale images** from 128×128 to at least 512×512 or 1024×1024 before sending to the VLM (nearest-neighbor upscaling to preserve sharp pixel art edges)
2. **Provide side-by-side images** as a single composed image rather than separate attachments, forcing explicit visual comparison
3. **Use a structured rubric prompt** that breaks evaluation into discrete criteria (outline correctness, color accuracy, proportions, symmetry, outlier pixels)

### Spatial Reasoning Accuracy

OmniSpatial (2025) benchmarks dynamic reasoning, complex spatial logic, spatial interaction, and perspective-taking across 8,400+ question-answer pairs. Results reveal that **all VLMs significantly lag humans** on comprehensive spatial cognition. The best performers are proprietary reasoning models:[^6]
- GPT-5: 56.4%[^14]
- Gemini 2.5 Pro: 49.5%[^14]
- o4-mini: 46.5%[^14]
- Open models (InternVL3-78B, Qwen2.5-VL-72B): approach GPT-4.1 mini level[^6]

For symmetry detection, proportional comparison, and positional relationship assessment in sprites, reasoning models (o3, o4-mini, Gemini 2.5 Pro) outperform standard models. The ability to reason step-by-step through spatial layout is a material advantage.

### Rubric-Based Structured Evaluation

All frontier closed-source models now support structured JSON outputs and can score images against defined criteria. GPT-4.1 is particularly well-regarded for strict instruction-following in structured output contexts. Anthropic's Claude models feature documented safety against reward-hacking, which reduces the risk of a model inflating scores to satisfy rubric patterns rather than accurately evaluating them. Gemini 2.5 Pro is the strongest on Vision2Web (43.5% per Claude Opus 4.6 on the leaderboard), reflecting its ability to translate visual reference into structured output.[^55][^56][^57]

### Latency Profile

| Model | TTFT | Tokens/sec | Typical Vision Call (est.) |
|-------|------|-----------|---------------------------|
| Gemini 2.5 Flash | 0.45s[^18] | 206[^17] | 2–4s |
| GPT-4.1 | ~0.5s | 90–120 | 3–6s |
| Gemini 2.5 Pro | ~1–2s | 117[^15] | 5–10s |
| Claude Sonnet 4 | ~0.8s | 55[^27] | 4–8s |
| o4-mini | ~2–4s (reasoning) | Variable | 5–15s |
| Claude Opus 4.1 | ~1s | 39[^27] | 8–20s |
| o3 | 5–15s (reasoning) | Variable | 15–60s |

For the <10 second per-call target, **Gemini 2.5 Flash**, **GPT-4.1**, and **Claude Sonnet 4** are the most reliable options. o4-mini typically meets the target for simple comparisons but may exceed it for complex rubrics.

### Multi-Image Context

| Model | Max Images/Call | Context Window |
|-------|-----------------|----------------|
| Claude (API) | 600 images[^30] | 200K tokens |
| Gemini 2.5 Pro | ~500+ (token-limited) | 1M tokens[^11] |
| GPT-4.1 | ~200 (token-limited) | 1M tokens[^26] |
| Qwen3-VL | Token-limited | 256K[^41] |
| InternVL3-78B | Token-limited | 32K[^39] |

For comparing a candidate vs. reference image in a single API call, **all frontier models support this natively** — this is a solved problem. The more interesting question is batch evaluation: Gemini 2.5 Pro and Claude APIs support the most images per request, enabling evaluation of full sprite sheets in one call.

***

## Known Weaknesses: Small Images and Pixel Art

This is the most critical section for the specific use case. Several documented failure modes apply:

**1. Resolution downscaling.** Claude's API documentation explicitly states that images exceeding 1,568px on the long edge are downscaled before processing. A 128×128 pixel art image is far below the threshold where downscaling applies, but it is also far below the typical resolution of training images — most VLM training data comes from web photographs and documents at 512px–2048px. **Models may have limited capacity to reason about individual pixel-level differences in a 128px canvas.**[^30]

**2. Performance degradation on low-quality/low-resolution images.** A 2025 study found that all tested VLMs (including GPT-4o and Gemini) dropped from 95%+ accuracy on high-quality product images to approximately 75% on degraded/low-resolution versions. Pixel art is a distinct domain (not simply degraded photography), but the small-canvas challenge is real.[^58]

**3. Fine-grained visual matching drops significantly.** Research found a 45.5% performance drop between encoder-level visual similarity and VLM-level reasoning on low-level matching tasks. The implication: VLMs may "understand" a pixel art image conceptually while missing specific pixel-level errors in color, outline precision, or symmetry.[^54]

**4. VLMs are not yet ready for game QA.** The VideoGameQA-Bench (NeurIPS 2025) concluded that "while VLMs generally perform well on other multimodal benchmarks, they are still not ready to be deployed for many video game QA tasks". This does not mean they cannot contribute — it means they should be used with guardrails, structured prompts, and validation against ground truth.[^9]

**Mitigation strategies:**
- Pre-process images: nearest-neighbor upscale to 512×512 or 1024×1024
- Compose a side-by-side or diff-annotated image rather than sending raw sprites
- Use region-annotated images (draw bounding boxes around areas of concern) to focus model attention
- Apply structured rubrics with binary criteria (pass/fail per sub-criterion) rather than holistic scoring
- Fine-tune a smaller open-source model (SmolVLM, Qwen3-VL-8B) on your specific pixel art evaluation criteria — the FG-BMK study showed contrastive training substantially improves fine-grained distinction[^59]

***

## Recommendations for the Pixel Art QA Pipeline

### Recommended Stack

**Primary Judge (Cloud, Production):**
**Gemini 2.5 Flash** for throughput-sensitive pipelines. It offers ~0.45s TTFT, 206 tokens/sec, 1M context, and competitive MMMU scores at $0.30/1M input. For the highest accuracy on ambiguous cases, **escalate to o4-mini** (thinking with images, 84.3% MathVista, strong spatial reasoning).[^18][^19][^17]

**Open-Source Alternative:**
**Qwen3-VL-32B** (Apache 2.0, 131K context, outperforms Qwen2.5-VL-72B on all visual benchmarks) or **InternVL3-78B** (72.2% MMMU, 95.4% DocVQA, $0.15/1M via API) — both are cost-efficient for high-volume QA at the cost of some proprietary model accuracy.

**Fine-Tuning Candidate:**
For the best long-term results, fine-tune **Qwen3-VL-8B** or **SmolVLM-2.2B** on a labeled dataset of sprite comparisons. The Qwen3-VL architecture was specifically noted as effective for grounded visual reasoning tasks when fine-tuned.[^41][^60]

### Workflow Architecture

1. **Preprocessing**: Upscale 128×128 and 256×256 sprites to 512×512 using nearest-neighbor interpolation
2. **Composition**: Compose a single image with reference (left) and candidate (right) side-by-side, with a 4px separator — this forces explicit visual comparison in a single visual context
3. **Rubric prompt**: Provide a JSON schema for output with discrete binary/scale sub-criteria: outline accuracy, color palette match, proportions, symmetry, artifact pixels
4. **Model call**: Send to Gemini 2.5 Flash (primary) or o4-mini (escalation for complex cases)
5. **Validation**: For automated pipelines, cross-validate with a second model or human review on flagged edge cases
6. **Feedback loop**: Log failures and use them to build a fine-tuning dataset for a specialized small model

### Cost Estimate

At Gemini 2.5 Flash pricing, a typical sprite comparison prompt (2 composed images + ~500 tokens prompt + ~300 tokens output) costs approximately **$0.0003–$0.001 per evaluation call**, making large-scale automated QA feasible at scale.[^19][^17]

***

## Research Gaps and Emerging Work

The **VQualA 2025 challenge** (ICCV 2025) specifically advanced the state of the art for **pairwise and multi-image visual quality comparison** using LMMs. The MICBench dataset it introduced is the most directly relevant benchmark to the described use case. The winning ensemble at 75.7% accuracy used Qwen2.5-VL variants — suggesting that the current ceiling on VLM-based visual quality judgment is in the 75–80% range without task-specific fine-tuning.[^7]

The **OmniDiff** benchmark (ICCV 2025) advances image difference captioning across 12 change types and 324 diverse scenarios. Models fine-tuned on OmniDiff training data (M3Diff) show significant improvements over base VLMs for describing specific inter-image differences — this training data could be a valuable starting point for fine-tuning a sprite comparison model.[^10]

The **FG-BMK** benchmark (April 2025) evaluated 12 VLMs on fine-grained image tasks across semantic recognition and feature representation. Its key finding: **contrastive training significantly improves fine-grained distinction**, but aligning vision and text too closely can hurt detail perception — relevant guidance for any fine-tuning effort on pixel art evaluation.[^59]

---

## References

1. [MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning
  Benchmark for Expert AGI](http://arxiv.org/pdf/2311.16502.pdf) - We introduce MMMU: a new benchmark designed to evaluate multimodal models on
massive multi-disciplin...

2. [MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding
  Benchmark](https://arxiv.org/html/2409.02813) - ...Pro, a robust version of the Massive
Multi-discipline Multimodal Understanding and Reasoning (MMM...

3. [GPT-4.1: Features, Access, GPT-4o Comparison, and More](https://www.datacamp.com/blog/gpt-4-1) - On image-heavy benchmarks like MMMU, it reached 74.8% vs. 68.7% for GPT-4o. On MathVista, which incl...

4. [GPT-4o vs Gemini 2.5 Pro Comparison - LLM Stats](https://llm-stats.com/models/compare/gpt-4o-2024-08-06-vs-gemini-2.5-pro) - Compare GPT-4o and Gemini 2.5 Pro side-by-side. Detailed analysis of benchmark scores, API pricing, ...

5. [Qwen3-VL can scan two-hour videos and pinpoint nearly every detail](https://the-decoder.com/qwen3-vl-can-scan-two-hour-videos-and-pinpoint-nearly-every-detail/) - In the complex MMMU-Pro test, Qwen3-VL scored 69.3 percent, trailing GPT-5's 78.4 percent. Commercia...

6. [OmniSpatial: Towards Comprehensive Spatial Reasoning ... - arXiv](https://arxiv.org/html/2506.03135v3) - In this work, we introduce OmniSpatial, a comprehensive and challenging benchmark for spatial reason...

7. [VQualA 2025 Challenge on Visual Quality Comparison for ... - arXiv](https://arxiv.org/html/2509.09190v1) - This paper presents a summary of the VQualA 2025 Challenge on Visual Quality Comparison for Large Mu...

8. [VideoGameQA-Bench: Evaluating Vision-Language Models for ...](https://neurips.cc/virtual/2025/poster/121740) - Recent advances in vision-language models (VLMs) hold significant potential to automate and enhance ...

9. [VideoGameQA-Bench: Evaluating Vision-Language Models ... - arXiv](https://arxiv.org/html/2505.15952v1) - Our results show that while VLMs generally perform well on other multimodal benchmarks, they are sti...

10. [OmniDiff - ICCV 2025 Open Access Repository](https://openaccess.thecvf.com/content/ICCV2025/html/Liu_OmniDiff_A_Comprehensive_Benchmark_for_Fine-grained_Image_Difference_Captioning_ICCV_2025_paper.html)

11. [Gemini 2.5 Pro vs GPT-4o Comparison: Benchmarks, Pricing ...](https://llm-stats.com/models/compare/gemini-2.5-pro-vs-gpt-4o-2024-05-13) - Compare Gemini 2.5 Pro and GPT-4o side-by-side. Detailed analysis of benchmark scores, API pricing, ...

12. [Gemini 2.5 Pro: Features, Tests, Access, Benchmarks & More](https://www.datacamp.com/blog/gemini-2-5-pro) - MMMU (multimodal understanding): Gemini 2.5 Pro leads the benchmark with a score of 81.7%. How to Ac...

13. [Multimodal AI Leaderboard: Vision, Video, and Beyond](https://awesomeagents.ai/leaderboards/multimodal-benchmarks-leaderboard/) - Video-MMMU scores reveal an interesting stratification. The top three models (Gemini 3 Pro, GPT-5.2 ...

14. [Benchmarking Spatial Reasoning of Vision-Language Models in ...](https://arxiv.org/html/2510.19400v2) - Abstract. Vision-language models (VLMs) are essential to Embodied AI, enabling robots to perceive, r...

15. [Gemini 2.5 Pro Benchmarks 2026: Scores, Rankings & Performance](https://benchlm.ai/models/gemini-2-5-pro) - Gemini 2.5 Pro ranks #40 out of 123 models in mathematics benchmarks with an average score of 83.5. ...

16. [Gemini API Pricing (Updated March 2026) — 2.5 Pro ... - TLDL](https://www.tldl.io/resources/google-gemini-api-pricing) - Gemini API pricing 2026: 2.5 Pro $1.25/$10, Flash $0.30/$2.50 per 1M tokens. FREE tier available. Se...

17. [Gemini 2.5 Flash API Pricing 2026 - Costs, Performance & Providers](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-flash) - Gemini 2.5 Flash was released on June 17, 2025. Pricing starts at $0.300 per million input tokens an...

18. [Gemini 2.5 Flash: API Provider Performance Benchmarking & Price ...](https://artificialanalysis.ai/models/gemini-2-5-flash/providers) - The providers with the lowest input token pricing for Gemini 2.5 Flash (Non-reasoning) are Google (V...

19. [Gemini Pricing in 2026 for Individuals, Orgs & Developers - Finout](https://www.finout.io/blog/gemini-pricing-in-2026) - Gemini 2.5 Model Pricing (Per 1M Tokens, USD) ; 2.5 Flash. $0.30 (text/image/video), $1.00 (audio). ...

20. [Thinking with images | OpenAI](https://openai.com/index/thinking-with-images/) - OpenAI o3 and o4-mini represent a significant breakthrough in visual perception by reasoning with im...

21. [o3 vs o4-mini Comparison - LLM Stats](https://llm-stats.com/models/compare/o3-2025-04-16-vs-o4-mini) - o3 scores COLLIE: 98.4%, AIME 2024: 91.6%, ARC-AGI: 88.0%, MathVista: 86.8%, AIME 2025: 86.4%. o4-mi...

22. [Introducing OpenAI o3 and o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/) - Our smartest and most capable models to date with full tool access

23. [API Pricing](https://openai.com/api/pricing/) - Explore OpenAI API pricing for GPT-5.4, multimodal models, and tools. Compare token costs, realtime,...

24. [O4-Mini: Tests, Features, O3 Comparison, Benchmarks & More](https://www.datacamp.com/blog/o4-mini) - AIME 2024: o4-mini (no tools) scores 93.4%, outperforming o3 (91.6%), o3-mini (87.3%), and o1 (74.3%...

25. [GPT-4.1 vs GPT-4o mini Comparison - LLM Stats](https://llm-stats.com/models/compare/gpt-4.1-2025-04-14-vs-gpt-4o-mini-2024-07-18) - Compare GPT-4.1 and GPT-4o mini side-by-side. Detailed analysis of benchmark scores, API pricing, co...

26. [OpenAI gpt-4-vision-preview Pricing Calculator | API Cost Estimation](https://www.helicone.ai/llm-cost/provider/openai/model/gpt-4-vision-preview) - Explore AI costs with our comprehensive OpenAI gpt-4-vision-preview Pricing Calculator. Compare pric...

27. [Api Integration Guide](https://blog.laozhang.ai/en/posts/claude-opus-4-vs-sonnet-4-complete-comparison-guide) - Comprehensive comparison of Claude Opus 4.5 and Sonnet 4.5 with the latest February 2026 pricing upd...

28. [Claude Opus 4.1 - Simon Willison's Weblog](https://simonwillison.net/2025/Aug/5/claude-opus-41/) - Surprise new model from Anthropic today - Claude Opus 4.1, which they describe as "a drop-in replace...

29. [Anthropic Claude Opus 4.1 출시 | 벤치마크 성능·구독별 접근 권한 ...](https://marcus-story.tistory.com/245) - 안녕하세요,코딩 성능이 우수한 AI 모델로 잘 알려진 Anthropic이 최신 버전인 Claude Opus 4.1을 새롭게 공개했습니다. 이번 업데이트는 단순한 성능 향상을 넘어,...

30. [Vision - Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/vision) - You can include multiple images in a single request: up to 20 for claude.ai, and up to 600 for API r...

31. [Claude Opus 4 vs Claude Sonnet 4 Comparison - LLM Stats](https://llm-stats.com/models/compare/claude-opus-4-20250514-vs-claude-sonnet-4-20250514) - Compare Claude Opus 4 and Claude Sonnet 4 side-by-side. Detailed analysis of benchmark scores, API p...

32. [Grok-3 vs Grok-4 Comparison - LLM Stats](https://llm-stats.com/models/compare/grok-3-vs-grok-4) - Grok-3 scores AIME 2024: 93.3%, AIME 2025: 93.3%, GPQA: 84.6%, LiveCodeBench: 79.4%, MMMU: 78.0%. Gr...

33. [Grok 3 vs Grok 4: practical differences, performance, and what ...](https://www.datastudios.org/post/grok-3-vs-grok-4-practical-differences-performance-and-what-changes-for-users-in-2025) - Grok 3 vs Grok 4: practical differences, performance, and what changes for users in 2025 · The leap ...

34. [DeepSeek vs. Grok-4: Full Report and Comparison (August 2025 ...](https://www.datastudios.org/post/deepseek-vs-grok-4-full-report-and-comparison-august-2025-updated) - Overview and Model LineupDeepSeek is an open-source AI model suite from a Chinese AI firm (DeepSeek-...

35. [InternVL3.5: Advancing Open-Source Multimodal Models in ... - arXiv](https://arxiv.org/html/2508.18265v2) - ... benchmarks, surpassing InternVL3-2B of similar size, which scores 74.7. ... Llama-4-Maverick met...

36. [InternVL3: Exploring Advanced Training and Test-Time Recipes for ...](https://substack.com/home/post/p-161407317) - The flagship InternVL3-78B model achieves a score of 72.2 on the MMMU benchmark, setting a new state...

37. [InternVL3](https://internvl.github.io/blog/2025-04-11-InternVL-3.0/) - We introduce InternVL3, an advanced multimodal large language model (MLLM) series that demonstrates ...

38. [InternVL3: Exploring Advanced Training and Test-Time Recipes for ...](https://arxiv.org/abs/2504.10479) - In particular, InternVL3-78B achieves a score of 72.2 on the MMMU benchmark, setting a new state-of-...

39. [OpenGVLab: InternVL3 78B Review](https://designforonline.com/ai-models/opengvlab-internvl3-78b/) - OpenGVLab's InternVL3 78B supports vision and multimodal input but has no benchmark data available, ...

40. [Qwen2.5 VL 72B Instruct vs Qwen3 VL 32B Instruct - LLM Stats](https://llm-stats.com/models/compare/qwen2.5-vl-72b-vs-qwen3-vl-32b-instruct) - Qwen2.5 VL 72B Instruct outperforms in 0 benchmarks, while Qwen3 VL 32B Instruct is better at 15 ben...

41. [[2511.21631] Qwen3-VL Technical Report - arXiv](https://arxiv.org/abs/2511.21631) - We introduce Qwen3-VL, the most capable vision-language model in the Qwen series to date, achieving ...

42. [Alibaba Releases Qwen3-VL Technical Report Detailing Two-Hour ...](https://www.unite.ai/alibaba-releases-qwen3-vl-technical-report-detailing-two-hour-video-analysis/) - The model achieved 96.5% on DocVQA for document comprehension and 875 points on OCRBench, supporting...

43. [Alibaba's visual language AI model 'Qwen3-VL' can identify inserted ...](https://gigazine.net/gsc_news/en/20251201-qwen3-vl-technical-report/) - Its document processing capabilities are also high, with high scores of 96.5% in DocVQA, which measu...

44. [Top Vision LLMs Compared: Qwen 2.5-VL vs LLaMA 3.2 - Labellerr](https://www.labellerr.com/blog/qwen-2-5-vl-vs-llama-3-2/) - Compare Qwen 2.5‑VL and Llama 3.2 Vision in 2025: see which model dominates in vision understanding,...

45. [Gemini 2.5 Flash vs Llama 4 Maverick - DocsBot AI](https://docsbot.ai/models/compare/gemini-2-5-flash/llama-4-maverick) - Model Performance ; MMMU. Massive Multitask Multimodal Understanding - Tests understanding across te...

46. [DeepSeek VL2](https://airank.dev/models/deepseek-vl2) - Comprehensive DeepSeek VL2 analysis by DeepSeek. Top benchmarks: DocVQA: 93.3%, ChartQA: 86.0%, Text...

47. [DeepSeek-VL2: Mixture-of-Experts Vision-Language ...](https://arxiv.org/html/2412.10302v1)

48. [Best Open-Source Vision Language Models of 2026 - Labellerr](https://www.labellerr.com/blog/top-open-source-vision-language-models/) - Discover the leading open-source vision-language models (VLMs) of 2025 including Qwen 2.5 VL, LLaMA ...

49. [Gemini 2.5 Pro vs Gemma 3 12B Comparison - LLM Stats](https://llm-stats.com/models/compare/gemini-2.5-pro-vs-gemma-3-12b-it) - Gemini 2.5 Pro outperforms in 3 benchmarks (Global-MMLU-Lite, GPQA, SimpleQA), while Gemma 3 12B is ...

50. [SmolVLM - small yet mighty Vision Language Model - Hugging Face](https://huggingface.co/blog/smolvlm) - This simple approach yielded surprisingly competitive results on the CinePile benchmark, with a scor...

51. [Moondream Segmenting Update: Better Masks, Better Benchmarks ...](https://moondream.ai/blog/segmenting-update-2026-03-10) - Moondream Cloud segmenting now delivers stronger benchmark scores, improved mask quality, and 40% fa...

52. [SmolVLM to SmolVLM2: Compact Models for Multi-Image VQA](https://pyimagesearch.com/2025/06/23/smolvlm-to-smolvlm2-compact-models-for-multi-image-vqa/) - Importantly, the original SmolLM2 was limited to 2k tokens of context. However, even a single 512×51...

53. [Qwen2.5 VL 7B Instruct vs Qwen3 VL 30B A3B Thinking - LLM Stats](https://llm-stats.com/models/compare/qwen2.5-vl-7b-vs-qwen3-vl-30b-a3b-thinking) - Qwen2.5 VL 7B Instruct outperforms in 1 benchmarks (OCRBench), while Qwen3 VL 30B A3B Thinking is be...

54. [Hidden in plain sight: VLMs overlook their visual representations](https://arxiv.org/html/2506.08008v1) - Previous works have 1) attributed VLM limitations to vision encoder weakness and proposed ensembling...

55. [Vision2Web Benchmark 2026: 3 model averages - BenchLM.ai](https://benchlm.ai/benchmarks/vision2Web) - A benchmark for converting visual references into functional web implementations. Which model scores...

56. [GPT 4.1: Better and Cheaper Than GPT-4o? - Labellerr](https://www.labellerr.com/blog/gpt-4-1-better-and-cheaper-than-gpt-4o/) - It achieved 52.9% accuracy, more than double GPT-4o's score. It also made very few unnecessary chang...

57. [Claude 4 in 2025: Performance, Safety, Benchmarks, Ecosystem ...](https://www.datastudios.org/post/claude-4-in-2025-performance-safety-benchmarks-ecosystem-news-and-real-world-impact-for-enterpr) - Anthropic’s launch of Claude 4 in May 2025 brought a major leap for business-ready generative AI. Th...

58. [Evaluating How Image Quality Affects Product Captioning with VLMs](https://arxiv.org/html/2511.08917v1) - We discuss the need for model evaluations that center on disabled people's experiences throughout th...

59. [Benchmarking Large Vision-Language Models on Fine-Grained ...](https://www.youtube.com/watch?v=0Oyt5HW-z6Y) - Title: Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: A Comprehensive Evalua...

60. [Multimodal AI: The Best Open-Source Vision Language Models in ...](https://www.bentoml.com/blog/multimodal-ai-a-guide-to-open-source-vision-language-models) - The latest wave, from Qwen3-VL to GLM-4.6V, pushes open-source multimodality into new territory once...

