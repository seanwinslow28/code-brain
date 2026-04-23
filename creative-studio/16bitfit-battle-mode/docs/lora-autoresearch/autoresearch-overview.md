Okay, this is a really compelling find. Let me break this down and then connect the dots to your world.

## **What Autoresearch Actually Is**

The core idea is: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. [GitHub](https://github.com/karpathy/autoresearch) Karpathy released this in early March 2026 and it immediately went viral — 42,000+ GitHub stars [GitHub](https://github.com/karpathy/autoresearch/commits?author=karpathy).

The key insight isn't really about ML training specifically. What Karpathy identified is that the human's job is shifting from writing training code to writing research directions. In autoresearch, you don't touch the Python files at all. Instead, you write `program.md` — a plain English instruction file that tells the agent what to explore and what constraints to respect. [Substack](https://alexeyondata.substack.com/p/karpathys-autoresearch-went-viral)

### **The Three-File Architecture**

The whole system is deliberately tiny:

**`prepare.py`** — Fixed infrastructure. Data prep, tokenizer, evaluation metric. The agent **cannot** touch this. Think of it as "the rules of the game."

**`train.py`** — The single mutable file. Contains the GPT model architecture, optimizer, and training loop. The AI agent is allowed to modify anything inside this file — architectures, learning rates, batch sizes, optimizer settings. [Medium](https://medium.com/data-science-in-your-pocket/andrej-karpathys-autoresearch-bye-bye-researchers-76319a719630)

**`program.md`** — The agent's instructions, written in natural language English. Karpathy describes it as "research org code written in English." [Substack](https://alexeyondata.substack.com/p/karpathys-autoresearch-went-viral) This is the file **you** write and iterate on.

### **The Loop**

This setup transforms ML experimentation into an agentic loop, where the AI proposes code changes, runs experiments, evaluates results, and commits successful tweaks via Git. [Substack](https://kenhuangus.substack.com/p/exploring-andrej-karpathys-autoresearch)

The cycle goes: agent edits `train.py` → runs 5-minute training experiment → checks `val_bpb` (the metric) → if it improved, keep the git commit; if not, revert → repeat. The loop runs until the human interrupts, period. [GitHub](https://github.com/karpathy/autoresearch/blob/master/program.md) The agent is explicitly told never to stop and ask for permission.

### **Why the macOS Fork Matters for You**

The miolini fork officially supports macOS (Apple Silicon / MPS) and CPU environments, while preserving the original NVIDIA GPU support. It removes the hardcoded dependency on FlashAttention-3, falling back to PyTorch's native Scaled Dot Product Attention (SDPA). [GitHub](https://github.com/miolini/autoresearch-macos)

Karpathy's original required an NVIDIA GPU (CUDA). Artem Andreenko (miolini) forked it and adapted it to run on macOS using Metal. [X](https://x.com/miolini/status/2030402705374728218) Setup is straightforward — it requires Apple Silicon Mac (M1/M2/M3/M4 with Metal/MPS support), Python 3.10+, and `uv`. [GitHub](https://github.com/miolini/autoresearch-macos)

There's also an **MLX fork** (`trevin-creator/autoresearch-mlx`) that runs natively on Apple Silicon through MLX with no PyTorch dependency at all [GitHub](https://github.com/trevin-creator/autoresearch-mlx) — worth comparing.

## **Your Hardware Fit**

You actually have an interesting three-way option here:

**Mac Mini M4 Pro (24GB)** — Can run the macOS fork via MPS. Smaller memory means smaller models, but it works. Good for overnight runs since it's your always-on machine.

**MacBook Pro M4 Pro (48GB)** — Best Apple Silicon option. Double the unified memory means larger models and batch sizes. The macOS fork or MLX fork would both work here.

**Alienware RTX 5080 (16GB GDDR7, 64GB system RAM)** — This is your powerhouse. Could run Karpathy's *original* repo directly with CUDA. The RTX 5080 will dramatically outperform MPS on training throughput. You'd get more meaningful experiments per 5-minute window.

The Alienware is your best bet for serious runs. The Mac Mini is good for "set it and forget it overnight" experiments at smaller scale.

## **The Pattern That Should Excite You**

Here's where it gets interesting for your world. The patterns in AutoResearch are immediately applicable: the editable asset behaves like a controlled variable, the scalar metric functions like a fitness criterion, and the `program.md` document works like an experimental protocol. [The New Stack](https://thenewstack.io/karpathy-autonomous-experiment-loop/)

One writer already proposed the exact kind of adaptation that maps to your work: instead of refining a style guide manually, the system would treat the prompt or style guide itself as the artifact being optimized. [Substack](https://alexeyondata.substack.com/p/karpathys-autoresearch-went-viral)

This "Karpathy Loop" pattern is: **one mutable artifact \+ one measurable metric \+ one set of English-language instructions \+ autonomous agent \= overnight optimization.**

---

## **1\. ComfyUI Workflow Optimization**

This one's more technically involved but potentially higher-impact for your 16BitFit pipeline and animation work.

### **The Core Problem**

ComfyUI workflows have tons of parameters — sampler type, CFG scale, step count, denoising strength, ControlNet weights, model selection, scheduler type, and more. Right now you're tuning these by hand, running a generation, eyeballing it, adjusting. That's the exact manual loop autoresearch automates.

### **Mapping to the Three-File Architecture**

**`prepare.py` equivalent (fixed):**

* The input images (anchor sprites, reference poses)  
* The evaluation function (image scoring — more on this below)  
* The ComfyUI API client code that queues and polls workflows

**`train.py` equivalent (the mutable artifact):**

* The ComfyUI workflow JSON file — specifically the parameter values within nodes  
* The agent edits parameter values, swaps sampler nodes, adjusts weights

**`program.md` equivalent:**

* "Modify the workflow parameters. Queue the workflow via ComfyUI's API. Wait for the output image. Score it. If the score improved, keep. If not, revert."

### **The Metric Problem (Harder Here)**

Image quality is subjective, but there are computable proxies:

**For sprite consistency (your 16BitFit blocker):**

* **Structural similarity (SSIM)** between generated sprite and anchor image — measures how closely the output matches the reference  
* **CLIP similarity score** — embed both the anchor and output with CLIP, measure cosine similarity. This captures semantic/style similarity, not just pixel matching  
* **Pose accuracy** — if you're using OpenPose/ControlNet, you can run pose detection on the output and compare joint positions to the target pose

**For general image quality:**

* **Aesthetic score models** — there are open-source models (like LAION's aesthetic predictor) that output a single quality score  
* **CLIP-text alignment** — how well does the output match the text prompt?

**Composite metric:** Combine 2-3 of these into a weighted score. For example: `0.4 * CLIP_similarity + 0.3 * SSIM_to_anchor + 0.3 * aesthetic_score`. That gives you a single number the agent optimizes against.

### **What the Agent Would Mutate**

The workflow JSON has specific parameter nodes. The agent could experiment with:

* **Sampler settings:** Euler vs. DPM++ 2M Karras vs. UniPC, step counts (15 vs. 20 vs. 30 vs. 50\)  
* **CFG scale:** The guidance strength (typically 5-15 range). Huge impact on output quality  
* **Denoising strength:** How much the model departs from the input image  
* **ControlNet conditioning scale:** How tightly the pose/depth/edge map is followed  
* **Scheduler type:** Normal, Karras, exponential, SGM uniform  
* **Model checkpoint swaps:** If you have multiple fine-tuned models, the agent could test which produces better sprites  
* **LoRA weight combinations:** If you're stacking LoRAs, the agent can tune the blend weights  
* **Negative prompt engineering:** Iterating on what to exclude

Each "experiment" would be one image generation (\~30-60 seconds on your RTX 5080), scored automatically, kept or reverted. You could run 60-120 experiments per hour.

### **Implementation Sketch**

This one runs on the **Alienware** since that's where ComfyUI lives:

1. Load current workflow JSON  
2. Agent proposes parameter mutations  
3. Queue the workflow via ComfyUI's REST API (`POST /prompt`)  
4. Poll until complete (`GET /history`)  
5. Download the output image  
6. Run scoring pipeline (CLIP \+ SSIM \+ aesthetic, all local on the GPU)  
7. If score improved → save the workflow JSON, log result  
8. If not → revert to previous JSON  
9. Repeat

**Why Python directly (not Claude Code):** Same reason — you want tight, fast loops. ComfyUI has a REST API you can hit from Python. The scoring models (CLIP, SSIM) run locally on the same GPU. No need for the CLI overhead.

**Important difference from the writing use case:** This loop is heavier per iteration (30-60 seconds for image gen vs. a few seconds for text gen), so you'll get fewer experiments per hour. But the parameter space is more constrained (numeric values with known ranges), so the agent can be smarter about exploration — using something like binary search on continuous parameters rather than random mutations.

### **The Agent's `program.md` Would Include**

Constraints like: "Never set CFG below 3 or above 20\. Never set steps below 10\. Always use the same input image and seed for comparability. If a generation takes longer than 90 seconds, kill it and treat as failure. Keep a log of every parameter combination tried."

You'd also want it to be systematic: "Start by sweeping CFG scale in increments of 1\. Once you find the best CFG, sweep step count. Then sweep sampler type." This is more like a grid search guided by an intelligent agent that can also try creative combinations.

---

## **Cross-Pollination Between the Two**

Here's the connection I want to flag: both of these use cases share an identical architecture pattern. If you build the scaffolding for one, the other is mostly a matter of swapping out the mutable artifact, the evaluation function, and the mutation strategy.

You could create a generic `autoresearch-loop/` directory in your Superuser Pack with:

* A shared `loop_runner.py` that handles the keep/revert/log cycle  
* Pluggable "experiment" modules — one for prompt refinement, one for ComfyUI workflows, potentially more later  
* A shared results logging format (TSV like Karpathy, or into your vault)

This would become a reusable pattern you can point at *any* optimization problem where you have a mutable artifact and a measurable metric.

---

## **Where to Start**

I'd recommend the **writing voice mode** use case first. Here's why:

* Faster iterations (seconds vs. minutes per experiment)  
* Simpler infrastructure (just API calls, no ComfyUI setup)  
* You already have the reference corpus and rubric from the voice calibration work  
* It maps most cleanly to Karpathy's original pattern  
* The learnings transfer directly to the ComfyUI version

The biggest technical question you'll need to answer first is designing the judge prompt — that's the `prepare.py` of this whole thing. If the judge is poorly calibrated, the agent will optimize for the wrong thing. Want me to help draft the judge rubric, or would you rather dig into the ComfyUI architecture first?

