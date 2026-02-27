This is the complete, implementation-ready architectural blueprint for expanding your Claude Agent SDK infrastructure into a hybrid-cloud autonomous fleet. It rigorously adheres to your existing agents-sdk/ patterns, local hardware constraints (RTX 5080 / 24GB VRAM), and strict financial goals.  
By implementing **Hybrid Inference Routing**, we strictly reserve the Claude API (Sonnet 4.5 / Haiku 4.5) for complex tool orchestration and high-level reasoning, while aggressively offloading data-heavy processing (CSVs, Vault search, embeddings, summarization) to open-source models running on your Alienware. This asymmetric capability design ensures your monthly operating costs stay well beneath the $12 Rocket Money threshold.  
**1\. Agent Fleet Master Specification**

Below is the exhaustive specification for your expanded fleet. Pass these parameters into your config.toml and agent Python runners. All agents run strictly under the acceptEdits permission mode.  
**Phase 1: Core Systems & Finance (Pre-Move)**

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Process Inbox** |
| Domain | Vault Management |
| Python File | agents/process\_inbox.py |
| Trigger | Schedule (launchd: Daily 5:30 AM) |
| Skills Loaded | process-inbox, para-routing |
| MCP Tools Required | vault-tools, ollama-mcp |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject", "vault\_move\_file", "ollama\_generate"\] |
| Vault Notes Read | 1\_Inbox/\*.md |
| Vault Notes Written | 2\_Areas/\*, 3\_Projects/\* (Anchors: \`\`) |
| Max Turns | 20 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: DeepSeek-R1-Distill-Qwen-14B** |
| Local Model Offload | 100%. Fast triage and semantic tagging is perfect for local CoT models. |
| Dependencies | None |
| Priority Tier | Phase 1 (Now) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | 1\_Inbox/ is empty at 6:00 AM wake up; notes correctly PARA tagged. |
| Failure Modes | Local model hallucinates path. *Recovery*: Strict Python regex validation hook before \`vault\_move\_file\` executes. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Daily Driver (Morning, Evening, Friday)** |
| Domain | Life Systems |
| Python File | agents/daily\_driver.py |
| Trigger | Schedule (launchd: 6:00 AM, 5:00 PM, Fri 4:00 PM) |
| Skills Loaded | daily-planner, weekly-review, vault-read-write |
| MCP Tools Required | vault-tools, zapier-mcp (GCal) |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject", "zapier\_gcal\_read"\] |
| Vault Notes Read | 0\_Daily/{{today}}.md, Work/Priorities.md |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchors: , ) |
| Max Turns | 15 |
| Max Budget USD | $0.15 |
| Model Routing | **Claude 4.5 Haiku** |
| Local Model Offload | None. Requires fast, reliable cross-tool context mapping. |
| Dependencies | Process Inbox |
| Priority Tier | Phase 1 (Existing, requires updates) |
| Estimated Cost/Run | $0.03 API |
| Success Criteria | Actionable daily brief ready when you sit down. |
| Failure Modes | Zapier API timeout. *Recovery*: Graceful fallback to vault-only context. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Spending Analysis ("Rocket Money Killer")** |
| Domain | Life Systems / Financial |
| Python File | agents/spending\_analysis.py |
| Trigger | Event (launchd WatchPaths: \~/Downloads/BankCSVs/) |
| Skills Loaded | subscription-audit, financial-categorization |
| MCP Tools Required | vault-tools, ollama-mcp |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject", "ollama\_generate"\] |
| Vault Notes Read | Pre-processed CSV, Finance/Budget\_2026.md |
| Vault Notes Written | Finance/Monthly\_{{YYYY\_MM}}.md (Anchor: \`\`) |
| Max Turns | 10 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: Qwen 2.5 32B** (Heavy reasoning) |
| Local Model Offload | **CRITICAL:** CSV parsing and categorization NEVER touches the Claude API. |
| Dependencies | Deterministic Python pre-processor (lib/csv\_anonymizer.py) |
| Priority Tier | Phase 1 (Now) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Safely replaces $12/mo Rocket Money. Flags new subscriptions accurately. |
| Failure Modes | CSV header changes. *Recovery*: Python pre-processor throws exit code 1\. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Boston Move Coordinator** |
| Domain | Life Systems |
| Python File | agents/boston\_move.py |
| Trigger | Schedule (Mon/Wed/Fri 6:30 AM) — **EXPIRES MAR 21, 2026** |
| Skills Loaded | move-logistics, timeline-enforcer |
| MCP Tools Required | vault-tools, zapier-mcp (Gmail/GCal) |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject", "zapier\_gmail\_search"\] |
| Vault Notes Read | Projects/Boston\_Move.md |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchor: \`\`) |
| Max Turns | 10 |
| Max Budget USD | $0.15 |
| Model Routing | **Claude 4.5 Sonnet** |
| Local Model Offload | None. High penalty for hallucination on leases/utilities. |
| Dependencies | Daily Driver (Morning) |
| Priority Tier | Phase 1 (Urgent) |
| Estimated Cost/Run | $0.08 API |
| Success Criteria | Zero dropped balls on U-Haul, landlord comms, and utility transfers. |
| Failure Modes | Agent runs post-move. *Prevention*: Hardcoded expires\_on logic in \`config.toml\` terminates the agent. |

**Phase 2: PM Integrations & Retrieval**

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Sprint Health Monitor & Standup Prep** |
| Domain | PM Work |
| Python File | agents/sprint\_health.py |
| Trigger | Schedule (Mon-Fri 8:30 AM) |
| Skills Loaded | jira-sprint-analysis, standup-prep |
| MCP Tools Required | mcp-atlassian, vault-tools |
| Allowed Tools Whitelist | \["jira\_search", "jira\_get\_issue", "vault\_inject"\] |
| Vault Notes Read | Work/Campus\_Platform.md |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchor: \`\`) |
| Max Turns | 15 |
| Max Budget USD | $0.20 |
| Model Routing | **Claude 4.5 Sonnet** (Pristine JQL orchestration) |
| Local Model Offload | Local model pre-summarizes massive ticket descriptions before Sonnet synthesizes the standup brief. |
| Dependencies | Daily Driver (Morning) |
| Priority Tier | Phase 2 (30 days) |
| Estimated Cost/Run | $0.08 API |
| Success Criteria | Identifies agile blockers automatically before 9:30 AM standup. |
| Failure Modes | Jira API timeout. *Recovery*: Graceful exit 0, leaves anchor empty. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Meeting Defender** |
| Domain | PM Work |
| Python File | agents/meeting\_defender.py |
| Trigger | Schedule (Sunday 7:00 PM) |
| Skills Loaded | calendar-audit, maker-schedule-protector |
| MCP Tools Required | zapier-mcp (GCal, Slack), vault-tools |
| Allowed Tools Whitelist | \["zapier\_gcal\_find", "zapier\_slack\_draft\_dm", "vault\_inject"\] |
| Vault Notes Read | Work/Priorities.md |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchor: \`\`) |
| Max Turns | 10 |
| Max Budget USD | $0.10 |
| Model Routing | **Claude 4.5 Haiku** |
| Local Model Offload | Pre-classifies meetings as "declinable" locally via Phi-4. |
| Dependencies | None |
| Priority Tier | Phase 2 (30 days) |
| Estimated Cost/Run | $0.02 API |
| Success Criteria | Reclaims \>3 hours/week of maker time. |
| Failure Modes | False positive declines. *Prevention*: Only drafts Slack suggestions for you to review; never auto-declines via API. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Stakeholder Report Generator** |
| Domain | PM Work |
| Python File | agents/stakeholder\_report.py |
| Trigger | Schedule (Friday 2:00 PM) |
| Skills Loaded | vp-product-formatting, exec-summary |
| MCP Tools Required | mcp-atlassian, zapier-mcp (Confluence), vault-tools |
| Allowed Tools Whitelist | \["jira\_search", "zapier\_confluence\_create", "vault\_read"\] |
| Vault Notes Read | 0\_Daily/\*.md (Mon-Fri) |
| Vault Notes Written | Confluence Page (via MCP) |
| Max Turns | 20 |
| Max Budget USD | $0.40 |
| Model Routing | **Map-Reduce Hybrid**: Local Phi-4 summarizes the 5 daily notes. Claude Sonnet synthesizes Jira data and summaries into the final report. |
| Local Model Offload | Initial reduction of the week's daily notes. |
| Dependencies | Daily Driver (Friday) |
| Priority Tier | Phase 2 (30 days) |
| Estimated Cost/Run | $0.15 API |
| Success Criteria | Draft requires \<5 mins of editing before sending to VP. |
| Failure Modes | Context overflow. *Prevention*: Map-reduce strictly limits context sent to Sonnet. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Vault Embedding Indexer** |
| Domain | Meta-System |
| Python File | agents/vault\_indexer.py |
| Trigger | Schedule (Daily 2:00 AM) |
| Skills Loaded | None (Python-native logic wrapped in SDK) |
| MCP Tools Required | ollama-mcp |
| Allowed Tools Whitelist | \["ollama\_embed"\] |
| Vault Notes Read | \*\*/\*.md (Files modified in last 24h) |
| Vault Notes Written | Local vector SQLite DB (.claude/vector.db) |
| Max Turns | 1 (Batch) |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: nomic-embed-text** |
| Local Model Offload | 100%. Generates embeddings for semantic search. |
| Dependencies | None |
| Priority Tier | Phase 2 (30 days) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Semantic search over 1,431 notes runs in \< 200ms without Anthropic API. |
| Failure Modes | Alienware asleep. *Recovery*: Script executes Wake-on-LAN magic packet. |

**Phase 3: Developer & Memory**

| Field | Value |
| :---- | :---- |
| **Agent Name** | **PR Digest & Code Review Summarizer** |
| Domain | Tech / PM Work |
| Python File | agents/pr\_digest.py |
| Trigger | Schedule (Weekdays 7:30 AM) |
| Skills Loaded | code-review-pm, github-triage |
| MCP Tools Required | github-mcp (or Zapier), vault-tools |
| Allowed Tools Whitelist | \["github\_read\_pr", "vault\_inject"\] |
| Vault Notes Read | None |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchor: \`\`) |
| Max Turns | 10 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: Qwen2.5-Coder-14B** |
| Local Model Offload | 100%. Massive token savings by keeping code diffs local. |
| Dependencies | None |
| Priority Tier | Phase 3 (60 days) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Translates complex crypto backend PRs into business impact for PMs. |
| Failure Modes | Massive diff blows context. *Recovery*: Truncate diffs to 8000 tokens locally before inference. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Preserve Session** |
| Domain | Meta-System |
| Python File | agents/preserve\_session.py |
| Trigger | Event (Claude Code CLI post-stop hook) |
| Skills Loaded | preserve-session |
| MCP Tools Required | vault-tools, ollama-mcp |
| Allowed Tools Whitelist | \["vault\_inject", "ollama\_generate"\] |
| Vault Notes Read | Piped STDIN from .claude/history.json |
| Vault Notes Written | System/Sessions/{{date}}.md (Anchor: \`\`) |
| Max Turns | 5 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: DeepSeek-R1-Distill-Qwen-14B** |
| Local Model Offload | 100%. Perfect for local text extraction. |
| Dependencies | CLI exit |
| Priority Tier | Phase 3 (60 days) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Transcribes valuable terminal learnings into Obsidian automatically. |
| Failure Modes | Concurrent terminal closures. *Recovery*: filelock advisory locking. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Health Audit** |
| Domain | Life Systems |
| Python File | agents/health\_audit.py |
| Trigger | Schedule (Daily 7:00 PM) |
| Skills Loaded | health-habits, ppl-split-tracker |
| MCP Tools Required | vault-tools, ollama-mcp |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject", "ollama\_generate"\] |
| Vault Notes Read | 0\_Daily/{{today}}.md |
| Vault Notes Written | Personal/Health/PPL\_Tracker.md (Anchor: \`\`) |
| Max Turns | 5 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: Phi-4** |
| Local Model Offload | Extracting informal PPL workout text into Dataview YAML. |
| Dependencies | Daily Driver (Evening) |
| Priority Tier | Phase 3 (60 days) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Automatically gamifies gym consistency. |
| Failure Modes | Misinterprets text. *Recovery*: Appends \[?\] tag for Sean to review. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **MD to Anki** |
| Domain | Vault Management |
| Python File | agents/md\_to\_anki.py |
| Trigger | Schedule (Daily 10:00 PM) |
| Skills Loaded | spaced-repetition, flashcard-extraction |
| MCP Tools Required | vault-tools, AnkiConnect MCP (Local REST) |
| Allowed Tools Whitelist | \["vault\_read", "anki\_add\_note"\] |
| Vault Notes Read | Notes tagged \#anki-source |
| Vault Notes Written | Removes \#anki-source tag |
| Max Turns | 15 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: DeepSeek-R1-Distill-Qwen-14B** |
| Local Model Offload | 100%. Q\&A pair generation is highly suited for local CoT logic. |
| Dependencies | Vault Indexer |
| Priority Tier | Phase 3 (60 days) |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Generates high-quality Cloze and Basic cards injected directly to Anki. |
| Failure Modes | Anki desktop closed. *Recovery*: Fails gracefully, leaves tag for next day. |

**Phase 4 & 5: Creative Pipeline & Meta-Intelligence**

| Field | Value |
| :---- | :---- |
| **Agent Name** | **ComfyUI Sprite Orchestrator** |
| Domain | Creative Pipeline |
| Python File | agents/sprite\_orchestrator.py |
| Trigger | Queue (launchd WatchPaths on Sprites/Inbox/) |
| Skills Loaded | 16bitfit-style, comfyui-prompting |
| MCP Tools Required | Custom ComfyUI MCP, Local Vision MCP |
| Allowed Tools Whitelist | \["comfy\_queue\_prompt", "comfy\_check\_status", "local\_vision\_qa", "vault\_inject"\] |
| Vault Notes Read | Projects/16BitFit/Specs.md |
| Vault Notes Written | Projects/16BitFit/Render\_Log.md (Anchor: \`\`) |
| Max Turns | 30 |
| Max Budget USD | $0.50 |
| Model Routing | **Claude 4.5 Sonnet** (Orchestration) \+ **Local Qwen2.5-VL-7B** (Vision QA) |
| Local Model Offload | **CRITICAL:** Visual consistency QA runs locally on the Alienware to evaluate output frames before Claude accepts them. |
| Dependencies | Alienware ON, ComfyUI running |
| Priority Tier | Phase 4 (90 days) |
| Estimated Cost/Run | $0.10 API |
| Success Criteria | Automates overnight batch generation of Phaser 3 sprite sheets. |
| Failure Modes | Alienware VRAM OOM. *Recovery*: Agent checks /api/tags to verify Ollama memory availability before vision inference. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Festival Submission Tracker** |
| Domain | Creative Pipeline |
| Python File | agents/festival\_tracker.py |
| Trigger | Schedule (Weekly Monday 12:00 PM) |
| Skills Loaded | festival-strategy |
| MCP Tools Required | zapier-mcp (Sheets), vault-tools |
| Allowed Tools Whitelist | \["zapier\_read\_sheet", "vault\_inject"\] |
| Vault Notes Read | /Creative/Festivals/\*.md |
| Vault Notes Written | 0\_Daily/{{today}}.md (Anchor: \`\`) |
| Max Turns | 5 |
| Max Budget USD | $0.05 |
| Model Routing | **Claude 4.5 Haiku** |
| Local Model Offload | None. |
| Dependencies | None |
| Priority Tier | Phase 4 |
| Estimated Cost/Run | $0.01 API |
| Success Criteria | Zero missed FilmFreeway deadlines for animated shorts. |
| Failure Modes | Zapier sheet schema mismatch. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Portfolio Case Study Generator** |
| Domain | Career Pipeline |
| Python File | agents/portfolio\_gen.py |
| Trigger | Manual (CLI) |
| Skills Loaded | case-study-storytelling, pm-to-creative-translation |
| MCP Tools Required | vault-tools |
| Allowed Tools Whitelist | \["vault\_read", "vault\_inject"\] |
| Vault Notes Read | Projects/\*\*/\*.md, Creative/\*.md |
| Vault Notes Written | Portfolio/Drafts/\*.md |
| Max Turns | 20 |
| Max Budget USD | $0.00 |
| Model Routing | **100% Local: Phi-4 14B** |
| Local Model Offload | 100%. Iterative creative writing is free locally. |
| Dependencies | None |
| Priority Tier | Phase 5 |
| Estimated Cost/Run | $0.00 |
| Success Criteria | Translates crypto PM mechanics into animation industry terminology. |
| Failure Modes | Output reads generic. *Recovery*: Refine skill prompt with explicit portfolio examples. |

| Field | Value |
| :---- | :---- |
| **Agent Name** | **Meta-Agent / Chief of Staff** |
| Domain | Meta-System |
| Python File | agents/chief\_of\_staff.py |
| Trigger | Schedule (Sunday 11:00 PM) |
| Skills Loaded | fleet-health-monitor, cross-domain-synthesis |
| MCP Tools Required | vault-tools, obsidian-mcp |
| Allowed Tools Whitelist | \["vault\_read", "obsidian\_global\_search", "vault\_inject"\] |
| Vault Notes Read | /Meta/Agent-Logs/\*.csv, 7x Daily Notes |
| Vault Notes Written | /Meta/Fleet-Health.md (Anchor: \`\`) |
| Max Turns | 20 |
| Max Budget USD | $0.50 |
| Model Routing | **Map-Reduce Hybrid**: Local model maps daily logs; **Claude Opus 4.6** synthesizes the final strategic review. |
| Local Model Offload | Pre-summarization of massive log CSVs to compress Opus token context. |
| Dependencies | All weekly agents must complete first. |
| Priority Tier | Phase 5 |
| Estimated Cost/Run | $0.20 API \+ Local Compute |
| Success Criteria | Accurate detection of looping agents and friction points in your routine. |
| Failure Modes | Context window bloat. *Prevention*: Strictly enforce local map-reduce summarization step. |

**2\. MCP Integration Architecture**

Define your servers in ClaudeAgentOptions(mcp\_servers=...) or .claude/settings.json.

| Service | MCP Server / Method | Auth Type | Auth Setup Steps | Config Snippet (mcp\_servers) | Which Agents Use It | Setup Complexity | Security Considerations |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Vault Tools** | Custom Python (lib/custom\_tools.py) | Local FS | Native to SDK | {"vault-tools": {"command": "python", "args": \["lib/custom\_tools.py"\]}} | All Agents | Low | Enforce anchor-based PATCH via python. Require filelock. |
| **Atlassian (Jira)** | @modelcontextprotocol/server-atlassian | API Token | 1\. Generate token at id.atlassian.com. 2\. Set JIRA\_API\_TOKEN & JIRA\_EMAIL in .env. | {"atlassian": {"command": "npx", "args": \["-y", "@modelcontextprotocol/server-atlassian", "https://sean-theblock.atlassian.net"\]}} | Sprint Health, Report Gen | Med | Protect .env with block-secrets.py hook. Restrict state changes. |
| **Zapier (Slack/GCal/Gmail)** | @zapier/mcp-server | OAuth | Run npx @zapier/mcp-server login. Authenticate via browser. | {"zapier": {"command": "npx", "args": \["-y", "@zapier/mcp-server"\], "env": {"ENABLE\_TOOL\_SEARCH": "true"}}} | Meeting Defender, Boston Move, Festivals | Med | **CRITICAL:** ENABLE\_TOOL\_SEARCH=true prevents injecting 175 tool schemas into prompts, saving massive token costs. |
| **GitHub CLI** | @modelcontextprotocol/server-github | PAT | Create Fine-grained PAT. Export GITHUB\_PERSONAL\_ACCESS\_TOKEN. | {"github": {"command": "npx", "args": \["-y", "@modelcontextprotocol/server-github"\]}} | PR Digest | Low | Restrict token read-only to specific work repos. |
| **Obsidian** | @cyanheads/obsidian-mcp-server | Local API | 1\. Install Obsidian Local REST API plugin. 2\. Copy bearer token to .env. | {"obsidian": {"command": "npx", "args": \["-y", "@cyanheads/obsidian-mcp-server"\]}} | Inbox Triage, Meta-Agent | Med | Sandboxed to local network. Restrict allowed paths. |
| **Ollama (Local Models)** | @rawveg/ollama-mcp | None (LAN) | Install Ollama on Windows. Set OLLAMA\_HOST=0.0.0.0:11434. | {"ollama": {"command": "npx", "args": \["-y", "@rawveg/ollama-mcp"\], "env": {"OLLAMA\_HOST": "http://\<ALIENWARE\_IP\>:11434"}}} | All local-offload agents | Low | Windows firewall MUST block 11434 from WAN, allowing only Mac IP. |
| **ComfyUI API** | Custom Python Wrapper | None (LAN) | Bind ComfyUI to 0.0.0.0 with \--listen. | {"comfyui": {"command": "python", "args": \["lib/mcp/comfy\_mcp.py", "--host", "\<ALIENWARE\_IP\>"\]}} | Sprite Orchestrator | High | Generates high GPU load. Must verify VRAM availability first. |
| **Hugging Face** | @huggingface/mcp-server | HF Token | Generate fine-grained read token. | {"huggingface": {"command": "npx", "args": \["-y", "@huggingface/mcp-server"\]}} | Discovery/Fallback | Low | Free tier limits apply. Use for niche HF Spaces (e.g., Audio/BG removal). |
| **NotebookLM** | N/A | N/A | NotebookLM currently lacks API/MCP. | N/A | N/A | N/A | Cannot integrate directly yet. Continue using manually. |

**3\. Open-Source Model Architecture (Windows 11 / RTX 5080\)**

Your RTX 5080 is an absolute powerhouse, but 24GB VRAM requires strategic quantization to run an LLM *alongside* ComfyUI (which takes \~8-12GB depending on workflow). You have \~12-16GB available for LLMs while ComfyUI is active.  
**3a. Model Selection Matrix**

| Use Case | Recommended Model (Early 2026\) | Params | Quantization | VRAM Req. | Why This Model | HF / Ollama Tag |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Fast Triage / Logic** | **Phi-4** | 14B | 4-bit (Q4\_K\_M) | \~9.5 GB | Unbelievable reasoning for its size. **Fits perfectly alongside ComfyUI**. Competes with Haiku. | phi4 |
| **Heavy Reasoning / Finance** | **DeepSeek-R1-Distill-Qwen-14B** | 14B | 4-bit (Q4\_K\_M) | \~9.5 GB | SOTA chain-of-thought in a small footprint. Perfect for analyzing spending locally. | deepseek-r1:14b |
| **Code Review / PRs** | **Qwen2.5-Coder-14B** | 14B | 4-bit (Q4\_K\_M) | \~9.5 GB | Beats most 70B models in coding benchmarks. Translates diffs locally. | qwen2.5-coder:14b |
| **Vision (Sprite QA)** | **Qwen2.5-VL-7B-Instruct** | 7B | 5-bit (Q5\_K\_M) | \~6.5 GB | Best open multimodal model for image QA and pixel consistency checking. | qwen2.5-vl-7b |
| **Heavy Synthesis (Offline)** | **Qwen2.5-32B-Instruct** | 32B | 4-bit (Q4\_K\_M) | \~20.0 GB | Rivals Sonnet. **Cannot run concurrently with ComfyUI**. Use for nighttime heavy tasks. | qwen2.5:32b |
| **Embeddings (Vault)** | **nomic-embed-text** | 137M | FP16 | \< 1.0 GB | Massive 8k context window, specifically designed for document retrieval. | nomic-embed-text |

**3b. Serving Infrastructure: Native Ollama**  
**Recommendation: Ollama (Native Windows)**  
Do not overcomplicate with Docker/vLLM on Windows unless you need batched production throughput. Pinokio is great for ComfyUI GUIs but opaque for API servers.

* **Why?** Ollama dynamically unloads models via the OLLAMA\_KEEP\_ALIVE=2m variable. If an agent calls Phi-4, Ollama loads it, serves the text, and 2 minutes later drops it from VRAM—instantly returning 100% of the RTX 5080 to your ComfyUI workflow. It natively supports the Anthropic Messages API (/v1/messages), meaning the Claude Agent SDK can target it directly.  
* **Setup:** Install Ollama for Windows. Set Windows Environment Variable OLLAMA\_HOST=0.0.0.0:11434. Allow Port 11434 in Windows Defender Firewall.

**3c. Hybrid Routing Architecture**

Create lib/hybrid\_router.py. This utility enables seamless offloading and graceful degradation.  
Python  
import httpx  
from claude\_agent\_sdk import ClaudeAgentOptions  
from config import get\_config  
def get\_routing\_options(task\_type: str) \-\> ClaudeAgentOptions:  
    config \= get\_config()  
    alienware\_url \= config.local\_models.endpoint \# http://\<ALIENWARE\_IP\>:11434  
      
    \# 1\. Ping Alienware (Health Check)  
    try:  
        r \= httpx.get(f"{alienware\_url}/api/tags", timeout=1.0)  
        alienware\_alive \= r.status\_code \== 200  
    except httpx.RequestError:  
        alienware\_alive \= False  
    \# 2\. Route Task  
    if task\_type in \["finance", "triage", "code\_review"\] and alienware\_alive:  
        model\_name \= "deepseek-r1:14b" if task\_type \== "finance" else "phi4"  
        return ClaudeAgentOptions(  
            model=model\_name,  
            base\_url=f"{alienware\_url}/v1", \# Exploits Ollama Anthropic compatibility  
            api\_key="ollama"   
        )  
    elif task\_type \== "finance" and not alienware\_alive:  
        raise Exception("Alienware offline. Cannot process financial PII safely.")  
    else:  
        print("Falling back to Claude API...")  
        return ClaudeAgentOptions(model="claude-3-5-haiku-latest")  
**3d. Hugging Face Integration Strategy**

* **HF Inference API (Free):** Use as a *tertiary fallback* in hybrid\_router.py for embedding generation if the Alienware is asleep. It supports Llama-3.3-70B-Instruct for free (with strict rate limits).  
* **HF Spaces:** Useful for finding specific niche tools (like background removal) via the HF MCP server, but too slow for core agent logic due to cold boots.  
* **HF Pro ($9/mo):** **Do not purchase.** The RTX 5080 offers lower latency, zero queue times, and total privacy. Use the $9 for Claude API orchestration tokens instead.

**3e. Pinokio & One-Click Deployment**

Use Pinokio **only** for creative apps (ComfyUI, Audio generation tools). Pinokio's containerization abstracts ports and environment variables, making it brittle to run a background 24/7 Ollama API server. Keep your LLM server bare-metal via native Ollama.  
**3f. Cost Savings Projection (The "Rocket Money Math")**

*Rocket Money Budget Constraint:* $12.00 / month.

| Agent Task | Pure API Cost/Mo | Hybrid Cost/Mo | Notes |
| :---- | :---- | :---- | :---- |
| Spending Analysis (CSVs) | \~$2.00 (Sonnet) | \*\*$0.00\*\* (Local R1) | Avoids sending PII to Anthropic. |
| Process Inbox | \~$1.50 (Haiku) | \*\*$0.00\*\* (Local Phi-4) | Runs 30x/month. |
| PR Summarization (Diffs) | \~$6.00 (Sonnet) | \*\*$0.00\*\* (Local Coder) | Diffs consume massive context. |
| MD to Anki / Session Logs | \~$3.00 (Haiku) | \*\*$0.00\*\* (Local R1) | High token output tasks. |
| Embeddings (1400 notes) | \~$1.50 (Anthropic) | \*\*$0.00\*\* (Local Nomic) | Re-indexed freely upon changes. |
| **Total Monthly Savings** | **\~$14.00/mo** |  |  |

*Electricity estimate:* Alienware uses \~300W under load. 1 hour/day \= \~9 kWh/month ≈ $2.50/month.  
**Result:** Hybrid routing successfully brings the fleet cost well below the $12/mo threshold, justifying the cancellation of Rocket Money.  
**4\. Safety & Guardrails Architecture**

**a) Permission Mode Matrix:** All autonomous agents MUST run in permission\_mode="acceptEdits". The allow\_dangerously\_skip\_permissions flag must remain False. **No agent ever receives bash or run\_command access.**  
**b) Tool Whitelisting Strategy:** Precisely define allowed\_tools per agent in config.toml. The Spending Analysis agent receives \["vault\_inject"\]; it does NOT receive \["zapier\_slack\_dm"\].  
**c) Hook Architecture (.claude/hooks/):**  
Hooks execute based on exit codes (0=allow, 1=error, 2=deny).

1. **loop-detector.py**: Intercepts PostToolUse MCP calls. Maintains a sliding window hash of the last 3 tool calls. If hash(call\[n\]) \== hash(call\[n-2\]), exit 1\.  
2. **cost-watchdog.py**: Parses agent-run-history.csv on PreRun. If sum(costs\_today) \> 2.00, exit 2 (Denies API access, preventing bill shock).  
3. **vault-integrity.py**: Intercepts vault\_inject. If the string to replace is "" (meaning overwrite whole file) instead of a valid \`\`, exit 2\.

**d) File Locking (filelock):**  
Because launchd triggers multiple agents, concurrent writes will corrupt Obsidian files.  
Python  
from filelock import FileLock, Timeout  
def vault\_inject(path, anchor, content):  
    lock \= FileLock(f"{path}.lock", timeout=10)  
    with lock:  
        \# Safe read/modify/write  
**e) Financial Data Privacy Pipeline:**  
Raw Chase/Bilt CSVs *never* go to Claude API.

1. lib/strip\_pii.py reads CSV via pandas. Drops Account \#s, maps names to generics.  
2. Sends the anonymized CSV rows to the **Local Qwen 14B model** on the Alienware. Data never leaves your LAN.

**f) Dry-Run Protocol:**  
Implement if args.dry\_run: inside vault\_inject. It prints the diff to the console instead of writing to disk. Enforce mandatory dry-runs before enabling any new agent in config.toml. Set enable\_file\_checkpointing \= True in ClaudeAgentOptions for vault rollback on agent failure.  
**g) Sensitive Data Handling:**  
All OAuth tokens (Claude, Zapier) rely on the CLI's native secure keystore. Jira tokens go in .env, protected by the existing block-secrets.py hook. DO NOT commit .env.  
**5\. Cost Optimization Strategy**

**a) Model Routing Logic:**

* **Claude Sonnet 4.5**: ONLY used when complex multi-tool orchestration is needed (Sprint Health, Boston Move, Meta-Agent synthesis).  
* **Claude Haiku 4.5**: Used for fast JSON parsing and API data routing (Daily Driver, Meeting Defender).  
* **Local Open-Source**: Used for all raw text processing (CSVs, transcripts, PR diffs, CLI histories, Inbox routing).

**b) Token Reduction Techniques:**

* **Map-Reduce Meta-Analysis**: Do not feed 30 daily notes (30k+ tokens) to Opus 4.6. Run a script where local Phi-4 summarizes the daily note locally into a dense 150-word JSON for $0.00. Feed the 30 short JSON summaries to Opus on Sunday.  
* **Skill Pruning**: skill\_loader.py must only inject the skills explicitly listed in config.toml. Injecting all 106 skills burns context.  
* **Prompt Caching**: Put dynamic daily data at the *end* of the prompt so Claude 4.5 can cache the static skills/instructions at the beginning.

**6\. Scheduling & Orchestration**

**a) launchd Schedule Architecture (\~/Library/LaunchAgents/)**

* 02:00: Vault Indexer (Local DB update)  
* 05:30: Process Inbox (Local Triage)  
* 06:00: Daily Driver Morning (Haiku)  
* 06:30: Boston Move Coordinator (Sonnet)  
* 07:30: PR Digest (Local Coder)  
* 08:30: Sprint Health (Sonnet)  
* 17:00: Daily Driver Evening (Haiku)  
* 19:00: Health Audit (Local)  
* 22:00: MD to Anki (Local)

**b) Dependency Chain (DAG):**  
Process Inbox → Boston Move → Sprint Health → **Daily Driver** *(compiles output from the prior three into one brief).*  
**c) Event-Driven Triggers:**

* **Stop Hook**: .claude/hooks/post-stop.sh executes preserve\_session.py when CLI exits.  
* **WatchPaths**: spending\_analysis.py is triggered by launchd WatchPaths on \~/Downloads/BankCSVs/.

**d) Boston Move Adjustments:**  
Add expires\_on \= "2026-03-22" to config.toml for the Boston Move agent. The Python wrapper checks this date and cleanly executes sys.exit(0) if passed, subsequently unloading its own plist.  
*During the move (Days 24-28)*: The Alienware will be boxed up. Ensure fallback\_to\_api \= True is configured so the Mac seamlessly shifts to 100% Cloud API. Spending Analysis will safely queue CSVs until the PC is reconnected.  
**e) Cross-Machine Orchestration & Network Resilience:**  
If the Alienware is asleep when a morning agent runs:

1. lib/local\_router.py times out on health check.  
2. Executes a Wake-On-LAN (WOL) magic packet to the Alienware MAC address (wakeonlan \<MAC\>).  
3. Waits 45 seconds for Windows/Ollama to boot.  
4. If still down, gracefully degrades to Claude Haiku 4.5.

**7\. Vault Integration Architecture**

**a) Anchor Registry (\`\`)**  
Every agent writes strictly to HTML comments to prevent destroying your vault.

* \`\` (Process Inbox)  
* \`\` (Sprint Monitor)  
* \`\` (Meeting Defender)  
* \`\` (Spending Analysis)  
* \`\` (Boston Move)  
* \`\` (ComfyUI Orchestrator)  
* \`\` (Preserve Session)  
* \`\` (Meta-Agent)

**b) Semantic Search via Local Embeddings:**

1. Phase 2: vault\_indexer.py runs nightly, scanning modified files.  
2. It sends text to nomic-embed-text running in Ollama on the Alienware.  
3. Vectors are stored locally on the Mac in a SQLite DB (sqlite-vec).  
4. Agents call {"tool": "obsidian\_search", "query": "..."} which hits the SQLite DB, instantly returning the top 5 relevant notes without calling the internet. Zero API cost.

**8\. Complete config.toml Expansion**

Ini, TOML  
\[fleet\]  
owner \= "Sean Winslow"  
vault\_path \= "/Users/sean/Documents/Obsidian\_Vault"  
\[cost\_control\]  
max\_fleet\_daily\_budget \= 2.00  
alert\_webhook \= "zapier\_slack\_msg"  
\[local\_models\]  
enabled \= true  
endpoint\_url \= "http://192.168.1.100:11434" \# Alienware LAN IP  
wol\_mac\_address \= "00:1A:2B:3C:4D:5E"  
primary\_triage \= "phi4"  
primary\_reasoning \= "deepseek-r1:14b"  
primary\_vision \= "qwen2.5-vl-7b"  
primary\_coder \= "qwen2.5-coder:14b"  
fallback\_to\_api \= true  
\[hybrid\_routing\]  
fallback\_model \= "claude-3-5-haiku-20241022"  
\[mcp\_servers.vault-tools\]  
command \= "python"  
args \= \["lib/mcp/vault\_mcp.py"\]  
\[mcp\_servers.zapier\]  
command \= "npx"  
args \= \["-y", "@zapier/mcp-server"\]  
env \= { ENABLE\_TOOL\_SEARCH \= "true" }  
\[mcp\_servers.ollama-mcp\]  
command \= "npx"  
args \= \["-y", "@rawveg/ollama-mcp"\]  
env \= { OLLAMA\_HOST \= "http://192.168.1.100:11434" }  
\[agents.sprint\_health\]  
enabled \= true  
model \= "claude-3-5-sonnet-20241022"  
skills \= \["jira-sprint-analysis", "standup-prep"\]  
max\_turns \= 15  
max\_budget\_usd \= 0.20  
allowed\_tools \= \["jira\_search", "jira\_get\_issue", "vault\_inject"\]  
depends\_on \= \["daily\_driver\_am"\]  
\[agents.spending\_analysis\]  
enabled \= true  
model \= "local:finance" \# Handled by hybrid router  
skills \= \["subscription-audit", "financial-categorization"\]  
max\_turns \= 10  
max\_budget\_usd \= 0.00  
allowed\_tools \= \["vault\_inject", "ollama\_generate"\]  
\[agents.boston\_move\]  
enabled \= true  
model \= "claude-3-5-sonnet-20241022"  
skills \= \["move-logistics"\]  
max\_turns \= 10  
max\_budget\_usd \= 0.15  
expires\_on \= "2026-03-22"  
allowed\_tools \= \["vault\_inject", "zapier\_gmail\_search"\]  
**9\. Testing Strategy**

**a) Unit & Integration Testing:** Extend the 33 Pytest tests. Use pytest-httpx to mock responses from Ollama and the Claude API to test the hybrid router logic without spending API credits.  
**b) Automated Agent Evals (Zero Cost):** Do not pay Anthropic to evaluate Anthropic. Write an eval script that passes the Daily Driver's markdown output to your local Alienware (Phi-4). Ask Phi-4 to score the output 1-10 based on criteria in SKILL.md.  
**c) Dry-Run Validation:** Implement \--dry-run flag in the agent runner. Overrides max\_turns=2, limits allowed\_tools, and mocks vault\_inject to output diffs to stdout.  
**d) Red Team Scenarios:**

* *Conflict*: Start a massive ComfyUI render, then trigger the PR Digest agent. Verify the Python script catches the 503/timeout from Ollama and correctly falls back to Claude Haiku.  
* *File Lock*: Open a Daily Note and type while Daily Driver is running. Verify filelock prevents file corruption.

**10\. Implementation Roadmap (90 Days)**

**Phase 1 (Days 1-14): Infrastructure & Rocket Money Replacement**

* **Hardware**: Install Ollama natively on Windows 11; configure OLLAMA\_HOST and Windows Firewall. Pull phi4 and deepseek-r1:14b.  
* **Software**: Implement lib/hybrid\_router.py and filelock. Build Python PII stripper.  
* **Agents**: Build Process Inbox, Spending Analysis, and Boston Move Coordinator (Urgent).  
* *Milestone*: Local models accessible; Rocket Money canceled.

**Phase 2 (Days 15-30): PM Layer & The Move**

* *Boston Move Date (March 21, roughly Day 26\)*: Pause new deployments. Let boston\_move.py expire naturally. Alienware offline; agents fallback to Haiku via API.  
* **Integrations**: Setup mcp-atlassian with block-secrets.py hook.  
* **Agents**: Build Sprint Health Monitor, Meeting Defender, & PR Digest (with local Qwen-Coder). Deploy local Vault Indexer.

**Phase 3 (Days 30-45): Meta-System & Memory**

* **Integrations**: Configure CLI Stop Hooks (stop-hook.sh).  
* **Agents**: Build Preserve Session agent, Health Audit, and MD to Anki.  
* *Milestone*: Zero-friction CLI capture and workout logging.

**Phase 4 (Days 45-60): Creative Pipeline Activation**

* **Integrations**: Build ComfyUI Python MCP wrapper. Pull Qwen2.5-VL-7B to Ollama.  
* **Agents**: Build ComfyUI Sprite Orchestrator and Festival Tracker.  
* *Milestone*: Agent batches prompts to Windows, evaluates output with local vision model.

**Phase 5 (Days 60-90): Advanced Synthesis**

* **Agents**: Build Meta-Agent (Chief of Staff) and Portfolio Case Study Generator.  
* *Milestone*: Weekly synthesis is fully autonomous utilizing local map-reduce summaries and Opus synthesis.

**11\. Open Questions & Risks**

1. **VRAM Contention (ComfyUI vs Ollama)**  
   *Risk*: The RTX 5080 has 24GB. ComfyUI takes \~10-12GB. A 14B model takes \~9.5GB. They *can* run simultaneously, but it leaves little headroom. A 32B model (20GB) will immediately crash ComfyUI.  
   *Decision*: Standardize on 14B models for concurrent automated background tasks. Reserve 32B models strictly for sequential tasks. Utilize Ollama's OLLAMA\_KEEP\_ALIVE=2m to instantly free VRAM when LLMs finish.  
2. **Zapier MCP Token Bloat**  
   *Risk*: Zapier MCP exposes 175 tools. Passing the schema for all 175 to Claude on every turn consumes thousands of tokens, destroying your budget.  
   *Decision*: You MUST set ENABLE\_TOOL\_SEARCH="true" in the Zapier MCP config env, or write a wrapper that only exposes strictly necessary tools (e.g., GCal, Slack) to specific agents.  
3. **Machine Sleep States & Power Cost**  
   *Risk*: Leaving the Alienware idling 24/7 draws power (\~$3-5/mo).  
   *Decision*: Utilize Wake-on-LAN via the Mac to wake the Alienware 5 minutes before morning agents run, keeping power costs negligible while maintaining zero-queue inference.  
4. **Hugging Face Pro vs Local**  
   *Risk*: If VRAM juggling is annoying, HF Pro ($9/mo) exists.  
   *Decision*: Build the hybrid routing first. The RTX 5080 is an incredible asset offering absolute privacy for your bank data and Obsidian notes. Use HF Free Inference API only as an emergency fallback.

