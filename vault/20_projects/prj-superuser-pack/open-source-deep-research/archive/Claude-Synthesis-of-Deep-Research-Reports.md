# Claude's Synthesis: Local Open-Source Deep Research Stack

**Date:** April 25, 2026
**Sources:** `Gemini-Local-Autonomous-Research-Agent-Landscape.md` + `Perplexity-Local-Open-Source-Deep-Research-Agent-Stack.md`
**Purpose:** Reconcile the two deep research reports into a single recommendation Sean can act on.

---

## Where the reports agree (high confidence)

- **Local LLMs on 16GB VRAM can do this.** A 14B-class model is the sweet spot. Don't try 32B.
- **The real cost isn't the LLM — it's the search backend.** Every framework hides this.
- **Skip UI-first tools** (Perplexica/Vane, SurfSense, Khoj) as primary picks. Headless Python is the requirement.
- **Skip STORM** for production. Stanford's project is in slow-maintenance mode; last real feature commit was mid-2025.
- **The quality ceiling is the local model, not the framework.** A 14B model running any of these frameworks will trail Perplexity DR/Gemini DR on nuance and source breadth. The win is autonomy, cost, and scheduled-unattended execution — not matching frontier quality.

---

## Where they diverge (and which to trust)

### 1. Which framework ranks #1 — important

Gemini picked `langchain-ai/local-deep-researcher`. Perplexity picked `LearningCircuit/local-deep-research`. **These are two different projects with confusingly similar names.** Perplexity correctly distinguished them; Gemini appears to have only known the LangChain one.

Trust Perplexity here. The LearningCircuit version has features the LangChain version lacks:

- Built-in **MCP server** (the existing Claude Code / Agent SDK already speaks MCP)
- **Scheduled research digests** feature (maps directly to launchd pattern)
- **PDF/Markdown export** aimed at Obsidian workflows
- Native **SearXNG** support (the LangChain version requires patching)

### 2. Which search backend

Gemini → Brave ($5/1K, claims 1,000/month free). Perplexity → SearXNG self-hosted, and explicitly states **Brave killed its real free tier in Feb 2026** (now $5/month for ~1,000 queries bundled).

Factual conflict. **Verify on Brave's pricing page before committing.** Weighting Perplexity's claim higher — more specific, more recent, aligns with the general 2025–2026 pattern of search APIs throttling free tiers. If Perplexity is right, Gemini's "125 reports/month on $20" math collapses.

### 3. Which model

Gemini → DeepSeek R1 Distill Qwen 14B. Perplexity → Qwen3 14B Q5_K_M.

Both valid:

- **DeepSeek R1 Distill** is better at **reasoning-heavy** tasks (outputs explicit chain-of-thought)
- **Qwen3 14B** is better at **instruction-following and structured output** (JSON schemas, clean citations)

Research agents need both, but they fail more often on instruction-following than reasoning. Perplexity's pick is the safer default.

### 4. Honesty about the quality gap

Perplexity's gap analysis is much more honest. Gemini mostly glossed over it. Perplexity's table showing OSS at 3-star quality vs. Perplexity DR/Gemini DR at 4-5 stars is the kind of calibration needed before replacing a paid tool.

---

## Recommended stack

Given the existing Agent SDK infrastructure, the alignment is almost too good:

| Layer | Pick | Why |
|---|---|---|
| Framework | **LearningCircuit Local Deep Research (LDR)** | MCP server plugs into the Claude Agent SDK the same way `vault_inject` does. Scheduled digests mirror the daily-driver pattern. |
| Search | **SearXNG self-hosted** (Docker) | $0/month. Both reports agree this is the only true zero-cost path. Limit to <20 concurrent queries to avoid upstream throttling. |
| Fallback search | **Tavily free tier** (1,000 credits/month) | When SearXNG gets CAPTCHA'd or quality is bad, route specific high-stakes queries to Tavily. Stays well inside $20. |
| Model (default) | **Qwen3 14B Q5_K_M** via Ollama | Best instruction-following at 16GB. ~55 tok/s. Fits with 4GB KV cache headroom. |
| Model (reasoning runs) | **DeepSeek R1 Distill Qwen 14B Q4_K_M** | Swap in when the query is analytical rather than factual. |

**Note:** Model recommendations were calibrated for the Alienware RTX 5080 (16GB CUDA VRAM). On Apple Silicon (M4 Pro, unified memory), recheck — MLX-quantized models in LM Studio may outperform GGUF, and the larger memory pool on the MacBook Pro (48GB) opens up bigger models than the reports considered.

---

## How this plugs into the existing pack

This is the cross-pollination piece worth flagging. LDR's MCP server isn't just a nice-to-have — it's what makes this compose with the existing pack:

- **Interactive mode**: Add `ldr-mcp` to the Claude Code MCP config. Any Claude Code session can call `ldr.research(...)` as a tool, alongside the existing `obsidian-vault` and `notebooklm-mcp` servers.
- **Autonomous mode**: Add a new agent at `agents-sdk/agents/deep_researcher.py` following the `daily_driver.py` pattern. It calls LDR's Python API, writes the report via the existing `vault_inject` tool at a `<!-- research-digest -->` anchor in a daily note or a dedicated project note.
- **Skill wrapper**: A new skill like `deep-research-queue` would let Sean queue research topics during interactive sessions and let the autonomous agent work through them overnight. This matches the "50 research jobs overnight" advantage both reports flagged.

LDR becomes another tool in the existing orchestration, not a parallel system.

---

## Honest risks

- **LDR requires login since v1.0.** Scheduled scripts need auth reconnect logic.
- **SearXNG upstream throttling is real.** At 20+ concurrent runs CAPTCHAs from Google/Bing kick in. Solution: rotate engines in `settings.yml`, add query delays, and keep total scheduled volume modest (5-10 runs/day).
- **14B models hallucinate citations** more than frontier models. URLs that look real but 404. Add a post-processing step that pings each cited URL — 20 lines of Python, catches most fabrications.
- **Context collapse around 16K tokens**, even though the window is 32K. Cap sources-per-iteration at 3-5, not 10+.

---

## Suggested next move

A **2-hour spike** to de-risk the biggest unknowns before full integration:

1. Verify Brave's current free tier (5 min on their pricing page). Determines if search backend decision is forced toward SearXNG.
2. `docker run` SearXNG. Confirm it returns JSON.
3. `ollama pull qwen3:14b`. Run one manual LDR query. See what the output quality actually looks like on this hardware.
4. If quality passes the sniff test, build the `deep_researcher.py` agent to slot into `agents-sdk/`.

If quality at step 3 disappoints, the fallback isn't "give up on local" — it's **hybrid**: route high-stakes queries to paid Perplexity DR via API, route bulk/scheduled background research to local. Still kills most of the current spend while keeping quality on the work that matters.
