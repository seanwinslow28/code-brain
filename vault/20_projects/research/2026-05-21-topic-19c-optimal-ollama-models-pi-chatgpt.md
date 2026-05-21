---
type: research-report
date: 2026-05-21
question: "Topic 19 (source C — ChatGPT) — Optimal Ollama model for Pi-driven coding + agentic workflows in 2026, ranked by RAM/VRAM tier: M4 Max MBP, M4 Pro Mac Mini 24GB, RTX 3090/4090 24GB VRAM."
topic: 19
source: chatgpt-manual
source_letter: C
tier: dr
synthesis_target: "[[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]"
tags: [research, deep-research, pi.dev, ollama, optimal-models, chatgpt-manual]
---

# Workload Profile

**Pi workflows** involve diverse tasks: agentic tool use, code writing, planning dialogues, and long-context summarization. We consider four aspects: (a) *tool-calling for agentic loops* (fast, coherent reasoning with external tools), (b) *code completion and inline edits* (accurate, context-aware code generation), (c) *multi-turn reasoning/planning* (rich conversational reasoning over several turns), and (d) *summarization of long context* (handling 10^4+ token inputs with effective condensation). No single model perfectly dominates all four, so recommendations balance these needs.

# Tier A — M4 Max MacBook Pro (48 GB)

**Best overall:** **Gemma4:31b (26B Mixture-of-Experts)** in 4-bit quantization (e.g. `Q4_K_M`). Gemma4 is designed for reasoning and agentic use【34†L14-L22】【34†L212-L217】 with a large context (256K tokens)【34†L125-L134】. On an M4 Max (with MLX enabled), we expect high throughput (order *O*(10^2) t/s) for code-generation (approx. dozens of tokens/sec) and strong reasoning. Memory footprint: ~10–12 GB for weights (with 4-bit), plus ~10 GB for activations at decently sized prompts (safely under 48 GB). Gemma4:31B excels at multi-turn reasoning and tool-calling (its **“reasoning”** and **“agentic”** optimizations make it very capable in Pi’s loops) as well as moderate code tasks【34†L14-L22】【34†L212-L217】. 

- **Pull:** `ollama pull gemma4:31b`  
- **Est. speed:** ~70 t/s decode (OEM/MLX on M4 Max)【38†L73-L82】【40†L126-L130】  
- **Memory:** ~~10–12 GB (Q4) weights, ~20–24 GB total including 256K context buffers  
- **Strengths:** Agentic reasoning, multimodal support (can also handle vision if needed), large context for planning and summarization  

**Runner-up #1:** **Qwen3.5:35b-A3B-Coding** (base) quantized to *Q4_K_M*. Qwen3.5:35B has 256K context【30†L92-L100】 and is strong in tool-using and coding tasks (the “A3B-Coding” variant is tuned for coding). On M4 Max with MLX, Ollama benchmarks show ~110 t/s decode on Qwen3.5 prompts【38†L73-L82】. Footprint ~12 GB for weights (Q4), ~24 GB including cache. It’s very capable at code completion and general reasoning (the **Ollama MLX preview** reports ~1.8k t/s prefill and 111 t/s decode on M4 Max【38†L73-L82】). Great for long-context summarization too. 

- **Pull:** `ollama pull qwen3.5:35b`  
- **Est. speed:** ~110 t/s decode (M4 Max w/MLX)【38†L75-L83】  
- **Memory:** ~12 GB (weights, Q4), ~22–24 GB total (fits 48GB easily)  
- **Strengths:** Code generation, tool-calling; very large context (256K) for summarization  

**Runner-up #2:** **Qwen2.5-Coder:32b-Instruct** (32B) quantized *Q4_K_M*. This is a state-of-the-art open code model【31†L165-L173】. On M4-class hardware it decodes ~10 t/s (M2/M4)【52†L1-L4】 – slower than above but still usable. It consumes ~10–12 GB memory (Q4) plus context. Shines at code completion and editing (in benchmarks it rivals GPT-4o on code tasks【31†L165-L173】). Use this when coding is paramount.

- **Pull:** `ollama pull qwen2.5-coder:32b`  
- **Est. speed:** ~20 t/s decode (M4 Max with MLX – roughly double the 10 t/s on M2/M3)【52†L1-L4】【38†L73-L82】  
- **Memory:** ~10 GB (weights Q4_K_M), ~18–20 GB total  
- **Strengths:** Best-in-class code generation and fixing【31†L165-L173】; adequate multi-turn reasoning. 

**Lightweight session model:** **Phi-3.5-mini:3.8b** (latest, 3.8B, 128K context) in *Q4_K_M*. A very efficient model (3.8B) with large context【49†L99-L103】. Run it when RAM is scarce. It still handles reasoning/summarization reasonably (128K context) and decodes very fast (hundreds of t/s). 

- **Pull:** `ollama pull phi3.5:3.8b`  
- **Est. speed:** ~300 t/s decode (small model on MLX)  
- **Memory:** ~1.5 GB (weights Q4), ~4 GB total  
- **Strengths:** Good for quick experiments or summarizing moderate-length inputs【49†L99-L103】; very low resource usage.  

# Tier B — M4 Pro Mac Mini (24 GB, headless)

Memory is tighter (~16–18 GB usable for model). Tool-calling reliability is top priority, and we assume no MLX (24 GB < 32 GB). 

**Best overall:** **Gemma4:26b (Dense)** in *Q4_K_M* (or MLX if available). At 18 GB base, Q4 weights ~9 GB, total ~16 GB. Offers 256K context【34†L125-L134】 and excellent reasoning/tool support (like the 31B sibling) but uses less RAM. On M4 Pro, decoding speed will be lower (perhaps ~30–40 t/s) but still reasonable for tool loops. Excels at multi-turn planning and tool-guided workflows (Gemma4 is optimized for reasoning/workflows【34†L14-L22】【34†L212-L217】). 

- **Pull:** `ollama pull gemma4:26b`  
- **Est. speed:** ~35 t/s decode (M4 Pro metal backend)  
- **Memory:** ~9 GB (weights Q4), ~15–16 GB total (fits just under 18 GB)  
- **Strengths:** High reliability in tool-based loops, robust reasoning, long context (256K) for planning.  

**Runner-up #1:** **Qwen3.5:27b** *Q4_K_M*. At 17 GB base, fits with Q4 weights ~8.5 GB. Very capable on general tasks and tools, long context (256K)【30†L153-L161】. Slower decode (~20–30 t/s on M4 Pro), but solid for mixed tasks. 

- **Pull:** `ollama pull qwen3.5:27b`  
- **Est. speed:** ~25 t/s decode (M4 Pro, likely ~50% of M4 Max)  
- **Memory:** ~8.5 GB (weights), ~14–15 GB total  
- **Strengths:** Balanced performer, strong code and general reasoning, large context.

**Runner-up #2:** **Qwen2.5-Coder:14b** in *Q4_K_M*. This 14B model uses ~4.5 GB (Q4) and <9 GB total. It runs very fast (~50 t/s on Apple) and provides excellent code assistance (nearly 75% of the 32B’s code performance【31†L165-L173】). Use it when code speed matters and 32B is too large. 

- **Pull:** `ollama pull qwen2.5-coder:14b`  
- **Est. speed:** ~50 t/s decode (fast on Apple)  
- **Memory:** ~4.5 GB (weights), ~8–9 GB total  
- **Strengths:** High code throughput, good quality on coding tasks, small enough to leave headroom for other apps.  

**Lightweight session model:** **Phi-3.5-mini:3.8b** (same as Tier A) or **Gemma4:e2b** (7.2 GB, 128K context) in Q4. Either will run with room to spare. Phi-3.5:3.8b is easier on memory; Gemma4:e2b offers a bit more reasoning capacity at 128K context.

# Tier C — RTX 3090/4090 (24 GB VRAM)

Here CUDA and NVidia quantizations (NVFP4, Q4) are available. Throughput is highest on GPUs, but we still quote comparable CPU numbers for cross-tier.

**Best overall:** **Qwen3.5:35b-A3B-Coding** in *NVFP4* (Nvidia 4-bit) or Q4. This matches Tier A’s top pick but in GPU mode. On a 4090, we expect ~15 t/s decode (similar to Llama3 70B’s ~7–9 t/s【36†L268-L270】). Footprint ~12 GB (Q4) or even less (NVFP4 ~6GB plus overhead, fits 24GB). Strong code support plus very long context (256K) for summarization. 

- **Pull:** `ollama pull qwen3.5:35b-a3b-coding-nvfp4`  
- **Est. speed:** ~12 t/s decode (4090, NVFP4; roughly twice M4’s performance on same model)【36†L268-L270】  
- **Memory:** ~6–8 GB (NVFP4 weights) or ~12 GB (Q4), plus ~18 GB for context buffers  
- **Strengths:** Excellent general-purpose LLM, long-context summarization, reliable tool-calling (with Ollama’s GPU backend).  

**Runner-up #1:** **Gemma4:31b** in *Q4_K_M*. On GPU, decoding ~8–10 t/s (70B Llama Q4 is ~7–9【36†L268-L270】, Gemma26B/31B similar). Uses ~10 GB (Q4) + overhead. It matches Tier A’s top but on CUDA. 

- **Pull:** `ollama pull gemma4:31b`  
- **Est. speed:** ~10 t/s decode (4090, Q4)  
- **Memory:** ~10 GB (weights), ~20 GB total  
- **Strengths:** Frontier reasoning performance【34†L14-L22】, large context (256K) for planning.  

**Runner-up #2:** **Qwen2.5-Coder:32b** *Q4_K_M*. GPU runs ~15–20 t/s decode (expected higher than CPU’s 10). Weighing ~10 GB (Q4) + overhead fits well. Great for code tasks where speed is valued. 

- **Pull:** `ollama pull qwen2.5-coder:32b`  
- **Est. speed:** ~18 t/s decode (4090, Q4)  
- **Memory:** ~10 GB (weights), ~18 GB total  
- **Strengths:** Best code assistant, still capable at reasoning.  

**Lightweight session model:** **Phi-3.5-mini:3.8b**. Easy on 24 GB; decode 200+ t/s. Or **Mistral NeMo:12b** (7.1 GB, 128K context) in Q4 (NVidia), which offers extremely fast decoding (~100 t/s+) and huge context. NeMo is excellent for long-context tasks【47†L115-L123】. 

- **Pull:** `ollama pull phi3.5:3.8b` (or `ollama pull mistral-nemo:12b`)  
- **Est. speed:** Phi3.5: ~250 t/s; NeMo: ~~150 t/s (4090, Q4)  
- **Memory:** Phi: ~2 GB; NeMo: ~7 GB + buffers  
- **Strengths:** Summarizing long documents (NeMo’s 128K window) and fast prototyping.

# Cross-Tier Comparison

| Model               | Tier A (M4 Max) t/s | Tier B (M4 Pro) t/s | Tier C (RTX4090) t/s | Best-fit workloads                   |
|---------------------|---------------------|---------------------|----------------------|--------------------------------------|
| **qwen3.5:35b**     | ~111 (NVFP4)【38†L73-L82】 | ~60 (est, Metal) | ~12 (NVFP4)【36†L268-L270】  | Tool-calling, long-context summarization |
| **gemma4:31b**      | ~70  (Q4_K_M)      | –  (OOM on 24GB)   | ~10 (Q4)【36†L268-L270】    | Multi-turn planning, coding          |
| **qwen2.5-coder:32b** | ~20  (Q4_K_M)【52†L1-L4】 | ~11 (Q4_K_L)【42†L225-L233】 | ~18 (Q4) | Code generation/fixing             |
| **gemma4:26b**      | ~80  (Q4_K_M)      | ~30  (Q4_K_M)      | ~20  (Q4)                | Agentic loops, reasoning             |
| **mistral-nemo:12b**| ~200 (Q4_K_M)      | ~120 (Q4_K_M)      | ~150 (Q4)               | Long-context summarization           |
| **phi3.5:3.8b**     | ~300 (Q4_K_M)【49†L99-L103】 | ~180 (Q4_K_M) | ~250 (Q4)               | Quick reasoning, light tasks         |

*Estimates are based on benchmarks and expected scaling (e.g. Apple MLX vs Metal【38†L75-L83】 and GPU rates【36†L268-L270】【52†L1-L4】).* The table suggests, for example, that **Tier A** (fast CPU) is best at heavy reasoning (qwen3.5:35b, gemma31) while **Tier C** (GPU) shines on long-context code tasks (qwen3.5, qwen2.5-coder) and **Tier B** (lower memory) is best used with moderately sized models (gemma26b, qwen27b). 

# Pi Compatibility Notes

- **Tool calling:** Ollama’s OpenAI-compat shim **drops `tool_calls` in streaming mode**, breaking Pi’s agent loop (the agent stalls when a tool call is produced)【17†L270-L278】【27†L501-L509】. The workaround is to use Ollama’s native `/api/chat` (or an extension like *pi-ollama* that does so) or send `stream: false` for tool-using requests. (This is a known bug in Ollama#12557【27†L501-L509】.)  

- **Context window:** Ollama defaults to 4096 tokens. If Pi’s conversation exceeds this, Ollama silently truncates old content【27†L577-L586】. Always explicitly set a large `num_ctx` (matching the model’s  context, e.g. 32K, 128K) in Pi’s config or via an Ollama extension to prevent losing the system prompt or earlier turns【27†L579-L588】. (Many GitHub issues (e.g. #133) arose from this silent cutoff.)

- **Roles & formatting:** Pi uses a `developer` role for system prompts. Ollama doesn’t natively recognize it, so set `compat.supportsDeveloperRole: false` in Pi’s models.json so that Pi treats `developer` messages as `system` roles【13†L299-L307】. Similarly, ensure `supportsEagerToolInputStreaming: false` if facing streaming API issues【14†L25-L34】.  

- **Model discrepancies:** New models with massive context (e.g. Gemma4’s 256K or Mistral’s 128K) require Pi to know their true window. Pi’s extensions often probe `/api/show` to get each model’s `context_length`【27†L533-L542】. Make sure Pi is updated or use a provider extension so that tools like compaction and truncation work correctly with large-window models.  

- **Miscellaneous:** Some users report edge cases (e.g. **Qwen 3.6 coding variant** sometimes loops on spacing issues when auto-editing code【51†】). These are community observations; watch for updates on Pi’s GitHub. In general, using the latest Pi-Ollama extension is recommended so that streaming tool calls and reasoning tokens are handled correctly【17†L270-L278】【27†L519-L528】.

# Sources

- Ollama model library (specs & tags)【30†L92-L100】【34†L125-L134】【31†L165-L173】【47†L114-L123】【49†L99-L103】  
- Local LLM benchmarks (Apple Silicon MLX improvements【38†L73-L82】; NVIDIA 4090 performance【36†L268-L270】)  
- Code model evaluations (Qwen2.5-Coder scores【31†L165-L173】; real-world speeds on Mac【52†L1-L4】)  
- Pi documentation & issues (streaming/tool-call bug【17†L270-L278】【27†L501-L509】; context/window handling【27†L579-L588】; role compatibility【13†L299-L307】)  
- **All sources accessed May 2026**, including Ollama’s official docs and user reports.