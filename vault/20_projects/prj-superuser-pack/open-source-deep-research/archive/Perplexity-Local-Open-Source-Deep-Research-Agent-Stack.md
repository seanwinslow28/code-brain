# **Local Open-Source Deep Research Agent Stack — Technical Landscape Report**

*April 2026 | Compiled for a hobbyist developer targeting Ollama \+ LM Studio on 16GB VRAM \+ macOS Apple Silicon*

---

## **1\. Executive Summary**

* \#1 — Local Deep Research (LearningCircuit): The most production-ready self-hosted option. Has a clean pip install, a Python LDRClient API, an optional MCP server (works with your Claude Code setup), and native Ollama support. Commits landed *today* (April 24, 2026). Pair with SearXNG for zero-cost search.  
* \#2 — GPT Researcher (assafelovic): Highest benchmark scores — ranked \#1 on CMU's DeepResearchGym across 1,000 complex queries, beating Perplexity Sonar and OpenAI's search-preview. Best ecosystem and community. Ollama support confirmed via .env config. Tavily free tier (1,000/month) is enough for light scheduled usage.  
* \#3 — LangChain Local Deep Researcher: The lightest-weight, most hackable option. A single LangGraph workflow designed explicitly for Ollama and LM Studio. No heavy dependencies. Last committed April 21, 2026\. Ideal as a building block if you want to own the loop logic.

Key cost reality: Every framework still needs a web search backend. SearXNG self-hosted is the only genuinely $0/month option. Tavily's free tier (1,000 credits/month) covers roughly 2–5 deep research runs per day at moderate depth. Serper gives 2,500 one-time free credits. Brave killed its free tier in February 2026\.

---

## **2\. Landscape Overview**

| Framework | License | LLM Backend Support | Search Backend | Python API? | Last Commit | Stars | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Local Deep Research (LearningCircuit) | MIT | Ollama, LM Studio, OpenAI, Anthropic (configurable base URL) | SearXNG (primary), DuckDuckGo, arXiv, PubMed, Tavily, Serper | ✅ Full REST \+ Python LDRClient; MCP server available | April 24, 2026 | \~3.5K (unverified) | Only OSS tool with built-in scheduled digests, analytics dashboard, and Obsidian-friendly markdown export |
| GPT Researcher (assafelovic) | MIT | Ollama (via OPENAI\_BASE\_URL), any OpenAI-compat endpoint | Tavily, SearXNG, Serper, Bing, DuckDuckGo, Exa, and 15+ others | ✅ Full async Python library (gpt-researcher pip package) | April 16, 2026 | 24.3K+ | CMU DeepResearchGym \#1; largest community; most retriever options |
| LangChain Local Deep Researcher | MIT | Ollama and LM Studio explicitly (first-class) | Tavily, DuckDuckGo | ✅ LangGraph graph callable from Python; Docker-ready | April 21, 2026 | \~3K (unverified) | Minimal, hackable — designed as a reference implementation; easiest to embed in custom Python agent loops |
| STORM (Stanford OVAL) | MIT | Any OpenAI-compat (configurable); Ollama via custom LiteLLM/OpenAI wrapper | You (Bing/Google/etc.) | ✅ Python library (knowledge-storm pip) | September 30, 2025 | \~18K (unverified) | Produces Wikipedia-style structured articles. Last meaningful feature commit May 2025; currently in slow-maintenance mode — use with caution |
| Khoj | AGPL-3.0 | Ollama (OpenAI-compat at localhost:11434/v1), LM Studio, Anthropic | Khoj's own web search (self-hosted), pluggable | ✅ REST API; self-hosted server | April 23, 2026 | \~28K (unverified) | Personal AI second brain with deep research mode; Obsidian sync built-in. Research mode requires enabling web search in self-hosted config |
| Deep-Searcher (Zilliz) | Apache-2.0 | Ollama, any OpenAI-compat | Bing, SerpAPI, DuckDuckGo, SearXNG | ✅ Python API | November 19, 2025 | \~6K (unverified) | Last commit Nov 2025 — borderline on the 6-month rule. Heavy Milvus/Zilliz dependency. Good for document \+ web hybrid research |
| Perplexica / Vane (ItzCrazyKns) | MIT | Ollama, LM Studio (via settings) | SearXNG (bundled) | ⚠️ UI-primary; no official Python API | April 11, 2026 | \~19K (unverified) | Rebranded to "Vane" in 2026\. Primarily a web UI chat tool — not suitable as a headless agent call. Excluded from top picks |
| open-deep-research (HuggingFace/dzhng variants) | Apache-2.0 | Any (cloud-first by default) | Tavily, SerpAPI | ⚠️ Script-based only; no library | Various | Varies | HuggingFace's variant built in 24h as a proof-of-concept in Feb 2025; dzhng's is a lightweight single-file script. Neither has a maintained programmatic API. Use as inspiration, not infrastructure |

Excluded (abandoned or incompatible): SurfSense — last checked active as of late 2025 but API-unstable; OpenManus — requires hosted LLM calls without clean local override (unverified Ollama support as of this writing).

---

## **3\. Web Search Backend Deep Dive**

This is where "free" frameworks hide their costs. Every framework above still dispatches HTTP calls to some external search index at runtime.

| Backend | Cost | Rate Limit / Free Tier | Setup Complexity | Quality Notes |
| :---- | :---- | :---- | :---- | :---- |
| SearXNG (self-hosted) | $0 (runs in Docker) | Unlimited (you own it) | Medium — Docker one-liner; requires settings.yml edit to enable JSON API | Aggregates 70+ engines (Google, Bing, DDG, etc.). Result quality matches source engines. Rate-limited by upstream engines; rotate engines in config to reduce blocks. Best choice for unattended agents |
| Tavily | 1,000 credits/month free, then $0.008/credit (\~$5/1K) | 1,000/month, no credit card required | Low — API key, one env var | Built explicitly for LLM agents; returns pre-extracted content snippets. The model=mini option costs only 4–15 credits per request. Powers GPT Researcher's \#1 benchmark result |
| Serper.dev | 2,500 one-time free credits (no recurring free tier), then $50/50K | 2,500 free (one-time, no card required) | Low — API key | Google SERP results. Excellent quality, real Google index. Credits expire in 6 months. After free credits: $1/1K \= \~$5–10/month for moderate agent use |
| Brave Search API | No free tier as of Feb 2026\. $5/month includes $5 credit (\~1,000 queries) | \~1,000 queries covered by $5/month included credit | Low — API key | Independent index (not Google/Bing-reskinned). Quality is good but shrank free allowance from 5,000 → \~1,000 in February 2026\. No longer recommended for budget builds |
| SerpAPI | Free: 250 searches/month; paid starts at $25/month (1,000/month) | 250/month free | Low | Google, Bing, Yahoo, Baidu. Expensive relative to alternatives at scale. Free tier too small for serious agent use |
| DuckDuckGo (via duckduckgo-search Python lib) | $0 — unofficial library | Unofficial; throttles/blocks heavy use | None — pip install | Non-API scraping; unreliable for unattended agents. Blocks after repeated queries. Usable for light testing only, not production scheduled scripts |
| Jina Reader / Firecrawl | Jina: free tier (rate-limited); Firecrawl: 500 credits/month free | Varies | Low | These are *content extractors*, not search engines. Use alongside a search API (give URL → get clean text). Pair with SearXNG for a fully free stack |

Bottom-line recommendation for your $0–20/month budget:

* Tier 1 (truly free): Self-hosted SearXNG \+ DuckDuckGo fallback. Works indefinitely at $0, with occasional upstream throttling.  
* Tier 2 (\< $10/month): Tavily free 1,000/month for deep research, SearXNG for general queries. Easily enough for personal scheduled agents running 1–3 research tasks per day.  
* Avoid: Brave API (no real free tier anymore), SerpAPI (expensive for volume), paid Bing/Google APIs.

---

## **4\. Local Model Recommendations for 16GB VRAM (RTX 5080\)**

Your RTX 5080 has 16GB GDDR7 — fast memory, Blackwell architecture. Models that fit entirely in VRAM are dramatically faster (benchmarks show 60–140 tokens/sec fully on-GPU vs. 13–20 tok/s with CPU offload). For long research reports, throughput matters: a 4,000-token synthesis pass at 15 tok/s takes 4+ minutes; at 60 tok/s it's under a minute.

| Model | Quant | VRAM Used | Tok/sec (RTX 4080 proxy) | Context Window | Research Suitability | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Qwen3 14B (Q4\_K\_M) | Q4\_K\_M | \~10.7 GB | \~62 tok/s | 32K (native), 128K with RoPE scaling | ⭐⭐⭐⭐⭐ Best all-rounder | Instruction-following rated best in class on 16GB; thinking mode toggleable (/think, /no\_think); pairs well with all three top frameworks |
| Qwen3 14B (Q5\_K\_M) | Q5\_K\_M | \~12 GB | \~55 tok/s est. | 32K/128K | ⭐⭐⭐⭐⭐ | Higher quality than Q4 with still \~4GB headroom for KV cache. Recommended if running 32K+ context research |
| Qwen3 32B (Q4\_K\_M) | Q4\_K\_M | \~16 GB | \~20–25 tok/s est. | 32K/128K | ⭐⭐⭐⭐ Better reasoning, slower | Tight fit — leaves little headroom for KV cache at long contexts. Risky for 64K+ context research sessions. Better on your MacBook Pro M4 Pro (48GB) |
| Phi-4 14B (Q4\_K\_M) | Q4\_K\_M | \~9 GB | \~22–35 tok/s | 16K | ⭐⭐⭐⭐ | Strong at structured reasoning and citations; shorter context hurts long synthesis. Good for sub-tasks in a multi-agent pipeline |
| DeepSeek R1 Distill Qwen 14B (Q4\_K\_M) | Q4\_K\_M | \~9–10 GB est. | \~40–55 tok/s est. | 32K | ⭐⭐⭐⭐ | Reasoning-focused distill from R1. Explicit chain-of-thought before answering; good for analytical reports. Slightly lower instruction compliance than Qwen3 14B |
| GPT-OSS 20B (Q4\_K\_M) | Q4\_K\_M | \~14 GB | \~140 tok/s | 32K | ⭐⭐⭐⭐ | Fastest fully-on-GPU option for 16GB. OpenAI's open-weight model. Blazing speed for iterative research loops; note: does not support JSON mode in Ollama — use tool-calling mode |
| Mistral Small 3.1 / Ministral 3 14B | Q4\_K\_M | \~13 GB | \~70 tok/s | 32K | ⭐⭐⭐ | Fast and solid; weaker at long-form synthesis vs. Qwen3 |

Quantization guidance:

* Q4\_K\_M is the practical default: \~75% VRAM reduction from FP16, minimal quality loss, fully supported by Ollama.  
* Q5\_K\_M is worth it for 14B models where you have headroom — meaningfully better output quality, especially for long-context synthesis.  
* GGUF is the right format for Ollama and LM Studio. EXL2 is faster on ROCm/ExllamaV2 but requires a separate runtime — unnecessary complexity given your current stack.  
* NVFP4 (Blackwell-native quantization) would be faster than GGUF Q4 on your RTX 5080, but Ollama doesn't support it yet as of April 2026; you'd need vLLM.

Recommended default for your use case: qwen3:14b at Q5\_K\_M. Pulls from Ollama in one command, fits in 12GB with 4GB for KV cache, runs at \~55 tok/s, supports long context, and has best-in-class instruction following for report writing.

---

## **5\. Quality Gap Analysis: OSS vs. Perplexity DR / Gemini DR**

## **What the benchmarks actually say**

GPT Researcher (using Tavily) ranked \#1 on Carnegie Mellon's DeepResearchGym benchmark in October 2025, evaluated on 1,000 complex queries. It beat Perplexity Sonar DeepSearch, OpenAI's gpt4-search-preview, OpenDeepSearch, and HuggingFace DeepSearch on Key Point Recall (64.67%), Citation Precision (85.36%), and Citation Recall (90.82%). This is a meaningful data point — not marketing.

However: this benchmark used GPT Researcher with Tavily (fast, LLM-optimized results) and likely GPT-4 class models. When you swap in a 14B local model via Ollama, the output degrades because the underlying LLM is smaller.

## **Where the gap actually comes from**

1\. The LLM backbone, not the framework. Perplexity Deep Research and Gemini Deep Research run on frontier models (sonnet-class, Gemini 2.5 Pro). A Qwen3 14B is genuinely worse at multi-step reasoning, synthesis, and long-context coherence. Benchmarks from early 2026 show the best open-source models (MiniMax-M2, Q61) trailing GPT-5 (Q70) by \~9 quality points — and your 14B is well below the frontier open-source ceiling.

2\. Context windows and multi-document synthesis. Perplexity Deep Research reportedly processes 135+ sources per query. At 14B on 16GB VRAM, you're realistically doing 32K context windows — enough for 10–20 pages of source material, not 135 web documents. Deep-Searcher and GPT Researcher can batch sources across multiple LLM calls to compensate, but it adds latency and potential coherence loss.

3\. Factual accuracy on obscure queries. A community benchmark thread in June 2025 reported \~95% SimpleQA accuracy on Local Deep Research with GPT-4.1-mini (cloud). Local model accuracy was not yet benchmarked by the community at time of writing. The Local Deep Research team explicitly stated they need community help to benchmark local models.

4\. User experience in practice. Multiple Reddit users (r/perplexity\_ai, r/LocalLLaMA) in 2025–2026 consistently report:

* Perplexity DR is faster (1–4 minutes per run) with inline citations that are easy to click-verify.  
* Gemini DR produces deeper, more "report-like" structure (depth score 4.6/5 vs. Perplexity's 4.1/5 in one comparison) but takes 22–90 seconds.  
* OSS tools with 14B local models produce adequate-to-good reports for technical and factual topics, but users report inconsistency on nuanced synthesis, weaker citation discipline, and occasional format failures (hallucinated JSON, incomplete sections).

## **Honest summary**

| Dimension | Perplexity DR | Gemini DR | Local OSS (14B) |
| :---- | :---- | :---- | :---- |
| Raw report quality | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (varies heavily) |
| Citation accuracy | ⭐⭐⭐⭐ (inline, clickable, occasional errors) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (framework-dependent) |
| Source breadth | ⭐⭐⭐⭐⭐ (135+ sources) | ⭐⭐⭐⭐⭐ (140+ sources) | ⭐⭐⭐ (10–30 sources typically) |
| Speed | ⭐⭐⭐⭐⭐ (1–4 min) | ⭐⭐⭐ (22–90 sec per deep run) | ⭐⭐ (5–20 min on 14B) |
| Privacy / local | ❌ cloud | ❌ cloud | ✅ fully local |
| Cost at scale | $20/month (20 DR runs) | Included in Google One AI | $0/month |
| Scheduled/unattended | ❌ | ❌ | ✅ |

The real advantage of OSS is not quality — it's autonomy. You can run 50 research jobs overnight. You can customize the search-decompose-synthesize loop. You can pipe output directly into your Obsidian vault. None of that is possible with Perplexity or Gemini.

---

## **6\. Top 3 Ranked Recommendations**

## **\#1 — Local Deep Research (LearningCircuit)**

Why it ranks here: Only framework that checks every box — active daily commits, clean pip install, documented Python API callable from a scheduled script, MCP server for Claude Code integration, native Ollama support, SearXNG integration, and built-in scheduled digest subscriptions that align exactly with your launchd-scheduled agent pattern.

Pros:

* pip install local-deep-research \+ ldr-web \= running in under 10 minutes  
* LDRClient Python API handles auth, CSRF, and sessions internally  
* Supports SearXNG (free), Tavily, DuckDuckGo, arXiv, PubMed out of the box  
* PDF and Markdown export — direct to Obsidian vault  
* Optional MCP server: Claude Code can call it as a tool  
* "Automated Research Digests" feature maps exactly to your scheduled Python scripts  
* \~95% SimpleQA accuracy on cloud models; community benchmarking for local models in progress

Cons:

* Web interface is the primary UX; headless Python API requires running the server process first (not a pure library call)  
* Auth layer (required since v1.0) adds setup friction for headless use  
* Smaller community than GPT Researcher; fewer third-party integrations

Who it's for: You. Specifically: someone who wants a local research assistant with scheduled digests, Obsidian export, Python API, and full Ollama compatibility — and is already using Claude Code MCP workflows.

---

## **\#2 — GPT Researcher (assafelovic)**

Why it ranks here: Best benchmark performance, largest community, cleanest async Python API, and the most extensive retriever ecosystem. If you want the highest-quality reports that OSS can produce, this is it — especially when search quality matters.

Pros:

* \#1 on CMU DeepResearchGym  
* pip install gpt-researcher with full async Python API (await researcher.conduct\_research())  
* 15+ search retrievers (Tavily, SearXNG, Serper, Bing, etc.)  
* Active maintainer (Assaf Elovic), frequent releases  
* Multi-agent orchestration via GPTResearcher \+ Orchestrator classes  
* Reports exceed 2,000 words with proper section structure

Cons:

* Ollama setup requires manual .env configuration (OPENAI\_BASE\_URL, LLM\_PROVIDER=ollama); not zero-friction  
* Some GitHub issues report inconsistencies when running with smaller local models  
* No built-in scheduling; you build the cron wrapper yourself  
* Default config assumes Tavily; SearXNG requires additional config

Who it's for: Developers who want maximum output quality and don't mind spending time on configuration; those who want to build custom multi-agent research pipelines.

---

## **\#3 — LangChain Local Deep Researcher**

Why it ranks here: The most hackable, lowest-footprint option. It's a pure LangGraph state machine — you import it, configure it, and own the loop. Built explicitly for Ollama and LM Studio as first-class citizens.

Pros:

* Designed specifically for Ollama and LM Studio (not retrofitted)  
* Minimal dependencies; easy to embed in existing Python code  
* Docker-deployable with a single command including Ollama base URL  
* LangGraph state machine is auditable and forkable  
* Active maintenance by LangChain team (last commit April 21, 2026\)

Cons:

* Only 3 search options: Tavily, DuckDuckGo, Perplexity (no SearXNG built-in; must patch)  
* No web UI, no scheduled digests, no Obsidian export — purely a building block  
* Fewer research iterations and less context management than LDR or GPT Researcher  
* Produces shorter, less structured reports by default

Who it's for: Python developers who want to embed research capability into a larger agentic workflow they control end-to-end; those who find LDR too heavyweight.

---

## **7\. Setup Path for \#1 Pick: Local Deep Research**

Repo: https://github.com/LearningCircuit/local-deep-research

## **Prerequisites**

bash

*`# On your Alienware Windows 11 machine (or Mac via Homebrew):`*  
*`# - Ollama already installed and running ✓`*  
*`# - Docker Desktop installed (for SearXNG)`*  
`ollama pull qwen3:14b   # ~9GB download, 14B Q4_K_M`

## **Step 1: Stand up SearXNG (free search backend)**

bash

`docker run -d \`  
  `--name searxng \`  
  `-p 8080:8080 \`  
  `-v $(pwd)/searxng-settings:/etc/searxng \`  
  `searxng/searxng`

Then edit searxng-settings/settings.yml to enable JSON output:

text

`search:`  
  `formats:`  
    `- html`  
    `- json   # Add this line — required for API access`

Restart: docker restart searxng. Verify: curl "http://localhost:8080/search?q=test\&format=json".

## **Step 2: Install Local Deep Research**

bash

`pip install local-deep-research`  
*`# Allow unencrypted DB for headless/dev use`*  
`export LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true`

## **Step 3: Configure Ollama endpoint**

LDR detects Ollama automatically at http://localhost:11434. To set explicitly, create or edit \~/.config/local\_deep\_research/settings.toml:

text

`[llm]`  
`provider = "ollama"`  
`model = "qwen3:14b"`  
`base_url = "http://localhost:11434"`  
`context_window = 32768`

`[search]`  
`tool = "searxng"`  
`searxng_url = "http://localhost:8080"`

## **Step 4: Start the server**

bash

`ldr-web`  
*`# Server starts at http://localhost:5000`*

Register a user account at http://localhost:5000/auth/register (one-time setup; required since v1.0).

## **Step 5: Call from a scheduled Python script**

python

*`# research_agent.py — called by launchd/cron`*  
`from local_deep_research.api import LDRClient`  
`from pathlib import Path`  
`from datetime import datetime`

`client = LDRClient(base_url="http://localhost:5000")`  
`client.login("your_username", "your_password")`

`result = client.quick_research(`  
    `"Latest developments in open-source AI inference frameworks Q2 2026"`  
`)`

*`# Write to Obsidian vault`*  
`vault_path = Path("~/Documents/Obsidian/Research").expanduser()`  
`timestamp = datetime.now().strftime("%Y-%m-%d")`  
`output_file = vault_path / f"{timestamp}-research-digest.md"`  
`output_file.write_text(result["summary"])`  
`print(f"Research saved to {output_file}")`

Reference: docs/api-quickstart.md and docs/features.md in the repo.

## **Step 6: First test query**

python

`summary = client.quick_research("What is Qwen3?", iterations=2)`  
`print(summary["summary"][:500])`

Expected output: A 500–1,500 word markdown summary with inline citations, section headers, and a source list. Generation time: 3–8 minutes with qwen3:14b depending on iteration depth.

## **Optional: MCP server (for Claude Code integration)**

bash

`pip install "local-deep-research[mcp]"`  
*`# Add to your Claude Code MCP config:`*  
*`# {"mcpServers": {"ldr": {"command": "ldr-mcp"}}}`*

This lets Claude Code call ldr.research("query") as a tool action.

---

## **8\. Risks and Gotchas**

Context window limits are the silent killer. A deep research run can accumulate 20,000–60,000 tokens of source material before synthesis. At Q5\_K\_M on qwen3:14b with a 32K context window, you can fit \~24,000 words. GPT Researcher handles this by chunking and iterating; LDR uses progressive summarization. Watch for context length exceeded errors in Ollama logs — if they appear, lower questions\_per\_iteration or switch to a model with larger context headroom (Qwen3 14B supports 128K with rope scaling, but KV cache at 128K on 16GB VRAM is impractical).

SearXNG upstream throttling. SearXNG is a metasearch aggregator — it still calls Google, Bing, DDG, etc. Aggressive agents (10+ concurrent queries) will trigger CAPTCHA responses from upstream engines. Use searxng-settings.yml to rotate engines, add delays between searches, and enable the cache plugin. A batch of 5 research runs/day should be safe indefinitely; 20+ concurrent runs will get blocked.

Small model hallucination in citation synthesis. 14B models are more likely than frontier models to confabulate citations — inventing URLs that sound real. Always configure your framework to include full URLs in citations and run a post-processing step that checks for 404s if citation accuracy is critical for your use case.

GPT-OSS 20B JSON mode issue. If you use gpt-oss:20b (fastest on 16GB), note it does not support JSON mode in Ollama as of August 2025\. Switch LDR/GPT Researcher to tool-calling mode in config.

LDR auth overhead in scheduled scripts. Since Local Deep Research v1.0 requires login, your scheduled Python script must handle session management. The LDRClient class handles this internally, but if the server restarts between runs, the script must re-authenticate. Add try/except and reconnect logic around client.login().

Deep-Searcher's Milvus dependency. Deep-Searcher bundles a vector store dependency (Milvus/Zilliz) that adds significant setup overhead and occasional startup failures. Fine for the use case it was designed for (document \+ web hybrid RAG), but overkill and fragile for pure web research.

LM Studio vs. Ollama endpoint differences. Both expose OpenAI-compatible APIs, but LM Studio defaults to port 1234 and Ollama to 11434\. LM Studio also requires the model to be loaded manually before the API accepts calls. For unattended scheduled scripts, Ollama is more reliable because it handles model loading/unloading automatically on demand.

STORM's slow-maintenance status. STORM (Stanford OVAL) has not had a substantive feature commit since May 2025; the last commit (September 2025\) was a minor dependency pin. Its Ollama support requires wrapping via LiteLLM — an extra layer that adds latency and potential breakage. Given the maintenance trajectory, avoid for production agent pipelines.

---

## **9\. Sources**

All citations are inline throughout this report. Primary sources consulted include:

* GitHub repositories (live commit data): LearningCircuit/local-deep-research, assafelovic/gpt-researcher, langchain-ai/local-deep-researcher, stanford-oval/storm, ItzCrazyKns/Vane (formerly Perplexica), zilliztech/deep-searcher, khoj-ai/khoj  
* Official documentation: GPT Researcher Ollama guide, LDR API quickstart, LDR pip install guide, Khoj Ollama docs, Tavily pricing, SearXNG LangChain integration  
* Benchmark data: CMU DeepResearchGym via Tavily and LinkedIn posts; SimpleQA community benchmark thread  
* Pricing sources: Tavily pricing page; Brave API discontinuation; Serper pricing; SerpAPI pricing  
* VRAM/performance benchmarks: RTX 4080 16GB Ollama benchmark (proxy for RTX 5080); VRAM requirements guide; RTX 5080 VRAM fit checker; GPU cheat sheet for Qwen3 32B  
* Quality gap analysis: CMU benchmark; open-source vs. proprietary LLM comparison; Gemini vs. Perplexity user test; Reddit r/perplexity\_ai; aiixx.ai deep research comparison  
* HuggingFace open-deep-research announcement; LangChain Local Deep Researcher source

---

Self-check confirmation:

1. ✅ All top-3 frameworks verified to work with Ollama (LDR: langchain-ollama in pip deps; GPT Researcher: official Ollama doc; LangChain LDR: built for Ollama)  
2. ✅ \#1 pick repo URL: https://github.com/LearningCircuit/local-deep-research  
3. ✅ Web search cost addressed for every framework in Section 3  
4. ✅ All three top picks committed within the last 2 weeks (LDR: Apr 24, GPT Researcher: Apr 16, LangChain LDR: Apr 21\)  
5. ✅ Quality gap grounded in CMU benchmark, user reports from Reddit, and structured testing — not speculation

Prepared by Deep Research  
