Option 1 \- Claude Desktop Prompt Response  
This is your complete, production-ready architectural specification. It synthesizes your NotebookLM context, Anthropic’s official agent-building best practices, the current state of the MCP ecosystem, and the latest releases as of **February 2026** (specifically Claude Sonnet 4.6, Claude Code Agent Teams, and the official Microsoft/AWS MCP catalogs).  
Given your financial context—credit card debt from the PM switch, saving for a ring/house, and the impending March 21 Boston move—**cost containment and measurable ROI are the primary architectural constraints.** Every decision below optimizes for minimizing Anthropic API spend by leveraging Prompt Caching, strict tool whitelisting, and aggressively routing repetitive token burn to your local Alienware RTX 5080\.  
**SECTION 1: Complete Agent Fleet Specification**

*Note: Cost estimates assume Claude Sonnet 4.6 ($3/MTok In, $15/MTok Out) with **Prompt Caching** aggressively enabled for your 106 loaded skills, dropping effective input costs by 90% to $0.30/MTok.*  
**1\. PM Work & Creative Pipeline**

| Agent Name | Domain | One-Line Purpose | Trigger Type | Schedule | Skills Loaded | MCP Tools Required | Vault Notes Read (Input) | Vault Notes Written (Output) | Allowed Tools Whitelist | Max Turns | Max Budget | Dependencies | Est. Cost/Run | Priority Tier | Goal Served |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Standup Prep** | PM Work | Pulls Jira/GitHub data to draft daily standup updates. | Schedule (launchd) | M-F 8:30 AM | jira-automation, meeting-prep, daily-driver | mcp-atlassian, GitHub CLI | 01\_Daily/YYYY-MM-DD.md, 04\_Projects/TheBlock.md | 01\_Daily/YYYY-MM-DD.md (\`\`) | Read, mcp\_\_atlassian\_\_search, mcp\_\_vault\_inject, Bash (gh restricted) | 10 | $0.15 | Daily Driver | $0.04 | Build Now | PM Career |
| **Meeting Brief Gen** | PM Work | Contextualizes upcoming meetings via Cal \+ Jira. | Event (Hook) | 15m pre-meeting | meeting-prep, daily-driver | Zapier (GCal), mcp-atlassian | 01\_Daily/YYYY-MM-DD.md | 01\_Daily/YYYY-MM-DD.md (\`\`) | Read, mcp\_\_zapier\_find\_event, vault\_inject | 8 | $0.10 | None | $0.03 | Build Now | PM Career |
| **Metrics Monitor** | PM Work | GA4 trend summaries and anomaly detection. | Schedule (launchd) | Mon 7:00 AM | data-analysis, analytics-workarounds | Zapier (GA4, Sheets) | 04\_Projects/Metrics\_Config.md | 04\_Projects/Metrics\_Log.md | Read, mcp\_\_zapier\*, vault\_inject | 15 | $0.20 | None | $0.06 | Build Later | PM Career |
| **Comfy Batch Mgr** | Creative | Queues sprite generation and polls local completion. | Manual | N/A | comfyui-workflows, sprite-asset-pipeline | ComfyUI API | 04\_Projects/16BitFit/Queue.md | 04\_Projects/16BitFit/QA\_Log.md | Bash (curl), Read, vault\_inject | 25 | $0.30 | None | $0.08 | Build Now | Creative R\&D |
| **Style Enforcer** | Creative | Vision QA on output frames vs. reference style. | Event (Watcher) | Post-render | animation-pipeline | Local Vision (Ollama) | 04\_Projects/Shorts/Style.md | 00\_Inbox/QA\_Reports/ | Read, Bash, vault\_inject | 10 | $0.05 | Comfy Batch | $0.00 (Local) | Build Next | Creative R\&D |
| **Festival Tracker** | Creative | Monitors Filmfreeway deadlines and preps packages. | Schedule (launchd) | Sun 8:00 AM | career-transition | Web Search (Built-in) | 05\_Life/Festivals.md | 01\_Daily/YYYY-MM-DD.md (\`\`) | WebSearch, \`Read\`, \`vault\_inject\` | 12 | $0.15 | None | $0.04 | Build Later | Creative Transition |
| **Asset Organizer** | Creative | Renames files, TexturePacker prep, asset index. | Event (Watcher) | Folder output | \`sprite-asset-pipeline\` | None | \`04\_Projects/16BitFit/Naming.md\` | \`04\_Projects/16BitFit/Index.md\` | \`Read\`, \`Bash\` (\`mv\`), \`vault\_inject\` | 10 | $0.10 | None | $0.02 | Build Next | Creative R\&D |
| **Portfolio Gen** | Creative | Auto-generates case studies from completed projects. | Manual | End of project | \`career-transition\` | None | \`04\_Projects/\*\` | \`02\_Areas/Portfolio/\*.md\` | \`Read\`, \`Glob\`, \`vault\_inject\` | 20 | $0.50 | None | $0.15 | Experim. | Creative Transition |

**2\. Life Systems, Vault Management & Meta**

| Agent Name | Domain | One-Line Purpose | Trigger Type | Schedule | Skills Loaded | MCP Tools Required | Vault Notes Read (Input) | Vault Notes Written (Output) | Allowed Tools Whitelist | Max Turns | Max Budget | Dependencies | Est. Cost/Run | Priority Tier | Goal Served |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Spend Analysis** | Life | Parses pre-processed bank JSONs to detect trends. | Schedule (launchd) | 1st & 15th | personal-finance, subscription-audit | Zapier (Sheets) | 50\_Sources/finance/clean.json | 05\_Life/Finance.md (\`\`) | Read, mcp\_\_zapier\*, vault\_inject | 15 | $0.25 | Pre-processor Hook | $0.06 | Build Now | Debt Paydown |
| **Health Audit** | Life | Tracks PPL progression, calculates XP, finds plateaus. | Schedule (launchd) | Sun 6:00 AM | health-habits | None | 01\_Daily/\*.md (workouts) | 05\_Life/Fitness.md | Read, Glob, vault\_inject | 12 | $0.15 | None | $0.05 | Build Later | Routine |
| **Learning Tracker** | Life | Cross-domain skill development, Anki card generation. | Schedule (launchd) | Sat 8:00 AM | career-transition | None | 03\_Resources/\*.md | 05\_Life/Anki\_Imports.csv | Read, Glob, Write | 20 | $0.20 | None | $0.00 (Local) | Build Later | Creative Transition |
| **Meal Planner** | Life | Meal prep suggestions based on goals and budget. | Schedule (launchd) | Sat 9:00 AM | health-habits | None | 05\_Life/Diet\_Macros.md | 01\_Daily/YYYY-MM-DD.md (\`\`) | Read, \`vault\_inject\` | 10 | $0.10 | None | $0.03 | Experim. | Routine |
| **Process Inbox** | Vault | Triages \`00\_inbox/\`, classifies, routes, adds frontmatter. | Schedule (\`launchd\`) | Daily 4:50 AM | \`process-inbox\`, \`vault-read-write\` | Obsidian Local REST | \`00\_inbox/\*.md\` | \`02\_Areas/\`, \`03\_Resources/\` | \`Read\`, \`Bash\` (\`mv\`), \`vault\_inject\` | 20 | $0.20 | None | $0.00 (Local) | Build Now | Vault Health |
| **Stale Note Det.** | Vault | Finds \`status: active\` notes untouched for 30+ days. | Schedule (\`launchd\`) | 1st of month | \`vault-read-write\` | None | Vault-wide | \`00\_Inbox/Stale\_Review.md\` | \`Bash\` (\`find\`), \`Read\`, \`vault\_inject\` | 10 | $0.10 | None | $0.03 | Build Next | Vault Health |
| **Knowledge Synth** | Vault | Read related notes, generate connection insights. | Schedule (\`launchd\`) | Sun 2:00 AM | \`prompt-engineering\` | Obsidian Local REST | \`03\_Resources/\*\` | \`03\_Resources/MOCs/\*\` | \`Read\`, \`Glob\`, \`vault\_inject\` | 30 | $0.50 | None | $0.25 | Experim. | Vault Health |
| **MD to Anki** | Vault | Generates spaced-repetition cards from reference notes. | Event (Watcher) | Note tagged \`\#anki\` | \`vault-read-write\` | None | \`03\_Resources/\*.md\` | \`05\_Life/Anki\_Deck.csv\` | \`Read\`, \`vault\_inject\`, \`Write\` | 15 | $0.15 | None | $0.00 (Local) | Build Next | Career Transition |
| **Vault Health Rep.** | Vault | Weekly stats—notes created, domains growing, gaps. | Schedule (\`launchd\`) | Sun 11:30 PM | \`analytics-workarounds\` | None | Vault-wide | \`99\_Meta/Vault\_Health.md\` | \`Bash\`, \`Read\`, \`vault\_inject\` | 15 | $0.20 | None | $0.06 | Build Later | Meta |
| **Preserve Session** | Meta | Claude Code stop hook → capture decisions to vault. | Event (Hook) | \`Stop\` hook | \`vault-read-write\` | None | \`.claude/history\` | \`99\_Meta/Decisions.md\` | \`Read\`, \`vault\_inject\` | 5 | $0.05 | None | $0.01 | Build Now | Meta |
| **Weekly Pattern** | Meta | Meta-review of all agent outputs → surface insights. | Schedule (\`launchd\`) | Sun 10:00 PM | \`data-analysis\` | None | \`01\_Daily/\*.md\` | \`99\_Meta/Weekly\_Review.md\` | \`Glob\`, \`Read\`, \`vault\_inject\` | 20 | $0.30 | Fleet Monitor | $0.10 | Build Next | Meta |
| **State of Sean** | Meta | Longitudinal analysis across all domains. | Schedule (\`launchd\`) | 1st of month | \`data-analysis\`, \`career-transition\` | None | \`02\_Areas/*\`, \`05\_Life/*\` | \`99\_Meta/Monthly\_Review.md\` | \`Glob\`, \`Read\`, \`vault\_inject\` | 25 | $0.50 | Fleet Monitor | $0.20 | Experim. | Life Architecture |
| **Fleet Monitor** | Meta | Reviews all agent run logs for cost/errors. | Schedule (\`launchd\`) | Sun 11:00 PM | \`analytics-workarounds\` | None | \`.claude/logs/\*\` | \`99\_Meta/Agent\_Health.md\` | \`Read\`, \`Glob\`, \`vault\_inject\` | 15 | $0.20 | All scheduled | $0.05 | Build Next | System Health |

**SECTION 2: External Tools, APIs & MCP Integration Roadmap**

Your reliance on 175 Zapier MCP tools is a latency and token-cost risk. In 2026, the official MCP ecosystem is robust enough to use direct, dedicated servers for heavy tasks (e.g., Atlassian, GitHub).  
**OAuth Flow Explanation (Beginner Level):**  
Think of OAuth like giving a valet key to a parking attendant. Instead of giving Claude your master Google password (which would let it delete your account or change your password), you log into Google yourself, and Google hands Zapier a temporary "valet key" (a token). This key is programmed to *only* open the Google Calendar or Sheets doors, and *only* for a set time. If the agent goes rogue, you just revoke the valet key from Google's security dashboard; your main password remains perfectly safe.

| Service Name | MCP Server / Connection Method | Auth Type | How to Store Credentials Safely (bypassing .env) | Which Agents Use It | Setup Complexity | Security Considerations | Current Status |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Zapier MCP** | npx @zapier/hq-mcp | OAuth | Handled by Zapier; API key in \~/.claude\_mcp (outside vault). | Spending Analysis, Metrics, Calendar | Low | Do not let Claude "Glob" your Zapier config directory. | Connected |
| **Custom vault\_inject** | Local Python script | Local | None | All Vault Writers | Low | Hardcode the allowed base directory (\~/Obsidian) to prevent escapes. | Built |
| **Jira/Confluence** | @modelcontextprotocol/server-atlassian | API Token | Store in macOS Keychain. SDK dynamically pulls into memory. | Standup Prep, Sprint Health | Medium | Generate a Jira API token restricted *only* to the projects you need, not global admin. | Planned |
| **Slack** | Zapier MCP (or official Slack MCP) | OAuth | Same as Zapier | Stakeholder Report, Agent error alerts | Low | Prefer Zapier for simple webhooks; Slack MCP requires admin workspace approval. | Connected (via Zapier) |
| **Google Cal/Sheets/GA4** | Zapier MCP | OAuth | Same as Zapier | Meeting Brief, Spend Analysis, Metrics | Low | Monitor Zapier task usage; GA4 reports can consume massive token context if not paginated. | Connected (via Zapier) |
| **GitHub CLI** | gh (direct bash execution) | OAuth/PAT | Natively managed by gh auth login in macOS Keychain. | PR Digest, Sprint Health | Low | Agent uses Bash tool to run gh pr list. Exclude gh repo delete via hooks. | Planned |
| **Obsidian REST** | mcp-obsidian (Community) | Local Token | Plaintext in config.py (Safe, as it only accepts 127.0.0.1 traffic). | Process Inbox, Synth | Low | Allows direct reading of your entire 1,431 note vault; keep it local. | Planned |
| **NotebookLM MCP** | Unofficial Python wrapper MCP | Cookies | Save session cookie locally via a script. | Knowledge Synth (Audio) | High | Fragile; breaks when Google updates NotebookLM UI. | Planned |
| **Hugging Face** | @huggingface/mcp | API Token | macOS Keychain | Occasional inferences | Low | Ensure HF Token has correct inference permissions; monitor free tier limits. | Connected |
| **Figma** | @modelcontextprotocol/server-figma | PAT | macOS Keychain | Design review automation | Medium | Read-only by default, but Figma canvases are massive in tokens. | Planned |
| **ComfyUI API** | Custom Python MCP / REST | Local | None (Local network only) | Comfy Batch Mgr | Medium | Ensure Windows firewall allows your Mac IP on port 8188; block public internet access. | Planned |
| **ElevenLabs API** | Direct API (via SDK custom tool) | API Key | macOS Keychain | Animation Pipeline | Low | ElevenLabs is expensive. Consider Kokoro TTS (local) instead to save money. | Planned |
| **Filmfreeway** | Puppeteer MCP (@modelcontextprotocol/server-puppeteer) | Session | Login manually, save session cookies to a local .json for Puppeteer. | Fest Tracker | High | Web scraping is notoriously brittle to UI updates. | Planned |

**Configuration Snippet (agents-sdk/config.py):**  
To inject credentials safely without .env files (respecting your block-secrets.py hook), pull from the macOS Keychain at runtime:  
Python  
import subprocess  
from claude\_agent\_sdk import ClaudeAgentOptions  
def get\_keychain\_secret(service):  
    return subprocess.check\_output(\["security", "find-generic-password", "-w", "-s", service\]).decode("utf-8").strip()  
def get\_agent\_options(agent\_name: str) \-\> ClaudeAgentOptions:  
    return ClaudeAgentOptions(  
        mcp\_servers={  
            "atlassian": {  
                "command": "npx",  
                "args": \["-y", "@modelcontextprotocol/server-atlassian"\],  
                "env": {"JIRA\_API\_TOKEN": get\_keychain\_secret("jira\_token"), "JIRA\_EMAIL": "sean@theblock.co"}  
            }  
        },  
        \# STRICT WHITELIST: Only allow exact tools needed for this agent  
        allowed\_tools=\["Read", "Bash", "mcp\_\_atlassian\_\_search\_issues", "mcp\_\_vault\_tools\_\_vault\_inject"\],  
        permission\_mode="acceptEdits", \# Auto-accepts file edits for scheduled headless runs  
        cwd="/Users/sean/ObsidianVault",  
        max\_turns=15,  
        max\_budget\_usd=0.50,  
        additional\_flags=\["-p"\] \# Run headlessly  
    )  
**SECTION 3: Skills Audit for Autonomous Operation**

Autonomous agents **cannot pause to ask you a question**. Many of your interactive skills will hang the SDK if they hit an edge case, draining your budget until the timeout.  
**1\. Ready for Autonomous Use (No Changes Needed)**

* vault-read-write, jira-automation, animation-pipeline, sprite-asset-pipeline, comfyui-workflows, zapier-mcp-automation. (These expect rigid, structured inputs/outputs and use strict formatting).

**2\. Needs Adaptation (Specific Changes Required)**

* daily-driver:  
  * **Modify:** Remove *"Ask the user what they want to focus on."*  
  * **Replace with:** *"Read 02\_Areas/Focus.md. If empty, default to 'Jira Standup Prep' and 'Boston Move tasks'. Execute vault\_inject to write the plan to today's note. Do not ask for confirmation. Terminate run after injection."*  
* process-inbox:  
  * **Modify:** Remove *"Confirm the tags with me before moving the file."*  
  * **Replace with:** *"Apply tags autonomously based on the \[Allowed\_Tags\] list. If confidence is \<80%, apply \#triage/human and move to 00\_Inbox/Review/. Do not halt execution."*  
* personal-finance / subscription-audit:  
  * **Modify:** Remove *"Review these anomalies with the user."*  
  * **Replace with:** *"Do not search the web for merchant names. If a transaction category is unknown, classify it strictly as 'UNKNOWN' in the JSON output. Format anomalies into a markdown table and append to 05\_Life/Financial\_Alerts.md."*  
* stakeholder-update:  
  * **Modify:** Remove *"Ask me for a summary tone"* and *"Are there specific blockers?"*  
  * **Replace with:** *"Use a strictly objective, professional tone. Auto-emphasize any ticket tagged 'High Priority' that has been in 'In Progress' for \>3 days. Do not ask for my review prior to generating the report."*  
* health-habits / time-management / life-admin / data-analysis / analytics-workarounds:  
  * **Modify:** Ensure all of these explicitly state: *"Output final analysis to \[Target File\] using vault\_inject. Conclude your turn without asking follow-up questions."*

**3\. Interactive Only (Remove from Autonomous Pools)**

* prompt-engineering, career-transition, design-team-reviewers. (These inherently require your human aesthetic judgment, nuance, and life decisions. Keep them in interactive Claude CLI sessions only).

**SECTION 4: Safety & Guardrails Architecture**

**1\. Permission Modes**

* **acceptEdits**: Use this for **all scheduled PM and Vault agents**. It allows Claude to use standard MCP file writers autonomously without hanging the terminal waiting for a y/n prompt, but still blocks raw dangerous bash commands.  
* **dangerouslySkipPermissions**: Use *only* for the Creative Pipeline agents (e.g., Comfy Batch Mgr) that require compiling code or running heavy Bash scripts natively on your Alienware hardware. Never use this globally.

**2\. Tool Whitelisting Strategy**  
In your ClaudeAgentOptions, explicitly define allowed\_tools per agent tier.

* *Read-Only Analysis (Health Audit, Metrics):* \["Read", "Glob", "mcp\_\_zapier\_\_ga4"\]  
* *Vault Writers (Inbox, Daily Driver):* \["Read", "Glob", "mcp\_\_vault-tools\_\_vault\_inject"\] (Strictly NO Edit or Write tool to prevent whole-file formatting destruction).  
* *External API Callers (Standup):* \["Read", "mcp\_\_atlassian\_\_search"\]. (Explicitly excluding Jira creation tools).

**3\. Financial Data Safety (The Pre-Processing Airgap Pattern)**

* **Vulnerability:** Giving Claude raw Chase/Bilt bank CSVs risks API leaks or logs capturing your account numbers.  
* **Solution:** Write a dumb, local, non-AI Python script (sanitize\_finance.py). launchd runs this script *first*. It uses pandas to drop Account Numbers, real names, and hashes exact transaction IDs, leaving only Amount, Category, Date. It outputs a sanitized.json. The *Spend Analysis* agent is ONLY allowed to read the JSON. Raw CSVs stay gitignored in 50\_sources/finance/ and are blocked via your network-access-control hook.

**4\. Agent Error Recovery & Cost Circuit Breakers**

* When an agent fails mid-run (e.g., Jira API is down), do not let it loop.  
* Implement a **token velocity check** in your Python orchestrator. If turn\_count \> 5 but no vault file has been modified or meaningful new context gathered, the agent is confused. sys.exit(1) to kill the agent.  
* Wrap the query() execution in a try/except block. On failure, append the error to 99\_Meta/Agent\_Logs.csv and trigger a silent Slack notification to yourself via Zapier webhook. Do **not** auto-retry.

**5\. Dry-Run Protocol & Deployment Checklist (safety-checklist.md)**  
Add this to your vault and check before scheduling any new agent:

1. \[ \] Skill prompts updated to remove human-in-the-loop requests.  
2. \[ \] allowed\_tools restricted to the absolute minimum required.  
3. \[ \] Run with \--dry-run flag to verify vault path targeting.  
4. \[ \] Run interactively with \--max-budget 0.10 to observe token caching hits.  
5. \[ \] Verify credentials are loaded via Keychain, not .env.  
6. \[ \] Add to launchd plist.

**SECTION 5: Hooks to Build**

Place these in your SDK's .claude/hooks/ directory to intercept actions natively.

| Hook Name | Hook Type | Trigger Condition | What it Does | Exit Code Behavior | Applies To |
| :---- | :---- | :---- | :---- | :---- | :---- |
| vault-verifier.py | PreToolUse | vault\_inject or Write called | Regex checks if target path is within allowed directories (01\_Daily/, etc.). Blocks overwrites of core MOCs or outside \~/ObsidianVault/. | 0 (allow) or 2 (deny) | Vault Writers |
| cost-circuit-breaker.sh | PostToolUse | Every tool execution | Reads current session token usage. If session\_cost \> agent\_budget, forces agent to wrap up thoughts. | 1 (Error/Allow: "Budget exceeded. Stop.") | All Autonomous |
| pii-filter.py | PreToolUse | Any Write, vault\_inject, or Bash | Regex scans tool payload for SSNs, 16-digit card numbers, or API keys. Redacts them. | 0 (Modify payload) or 2 (Deny) | Spend Analysis, Meta |
| finance-sanitizer.sh | PreLaunch (Custom) | Agent \== Spend Analysis | Runs the pandas Python script to sanitize raw CSVs *before* Claude initializes. | 0 (Launch) or 1 (Abort launch) | Spend Analysis |
| health-ping.py | Stop | Session ends naturally | Appends \[Timestamp, AgentName, ExitCode, TotalCost, Turns\] to 99\_Meta/Agent\_Logs.csv. | 0 (Allow) | All Agents |

**SECTION 6: Multi-Agent Coordination Architecture**

**1\. Write Conflict Prevention (Lock Files)**  
Rely exclusively on your custom vault\_inject MCP tool using HTML anchors (\`\`). Because it acts as an atomic PATCH request rather than a full-file rewrite, two agents won't overwrite each other's work easily. However, you must add a basic file.lock pattern in \`vault\_io.py\`. Before injecting, it creates \`today.md.lock\`. If another agent hits it, it sleeps for 5 seconds and retries.  
**2\. Agent Dependency Chains via launchd**  
launchd cannot natively chain scripts based on success. Use a **"Baton File" (Semaphore)** pattern.

1. Process Inbox runs at 4:50 AM. Upon successful completion, its Stop hook touches a hidden file: \~/.claude/batons/inbox\_done.flag.  
2. The Daily Driver launchd plist is configured with WatchPaths targeting that flag file. It triggers instantly when the flag appears, rather than guessing a time.

**3\. Shared State via Vault**  
Agents communicate asynchronously through a shared state note: 99\_Meta/Fleet\_State.md.  
Markdown  
| Agent | Status | Last Run | Output Link | Notes |  
|-------|--------|----------|-------------|-------|  
| ProcessInbox | SUCCESS| 04:50 AM | \[\[Triage\_Log\]\] | Moved 4 files |  
| StandupPrep | BLOCKED| 08:35 AM | N/A | Jira API Timeout |  
**4\. Inter-Agent Awareness & Fleet Monitoring**  
The **Fleet Monitor** meta-agent runs weekly. It reads Fleet\_State.md and your Agent\_Logs.csv, using standard data-analysis skills to identify looping agents, consistent failures, or agents that are costing more than their allocated budget, outputting a summary to Vault\_Health.md.  
**SECTION 7: Cost Projection Model**

*Assumptions: Claude Sonnet 4.6 pricing ($3 In / $15 Out). We must account for Anthropic's Prompt Caching rates: Cache Writes cost a premium ($3.75/MTok) while Cache Reads are heavily discounted ($0.30/MTok). The average cached run costs $0.02 \- $0.08.*  
\+1

| Phase | Active Agents | Runs/Month | Est. Cost/Run | Monthly Cost | Financial Viability |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Phase 1 (Wk 1-4)** | 4 (Daily, Inbox, Move, Standup) | \~150 | $0.05 | \*\*\~$7.50\*\* | Very High (Protects move sanity; saves 5 hrs/mo). |
| **Phase 2 (Wk 5-8)** | 8 (+ Comfy, Finance, Sprint, Style) | \~280 | $0.06 | \*\*\~$16.80\*\* | High (Debt analysis catches sub fees). |
| **Phase 3 (Wk 9-12)** | 12 (+ Meta Synth, Audits, Fest Tracker) | \~400 | $0.05 | \*\*\~$20.00\*\* | Excellent (Under $25 budget ceiling). |
| **Steady State** | 15+ (Full Fleet) | \~500 | $0.02\* | \*\*\~$10.00\*\*\* | *Costs drop heavily by offloading to RTX 5080\.* |

**Crucial Note for Debt Paydown:** $20/month is incredibly lean and aligns perfectly with your goals. However, to achieve the $10 steady state, you **must route simple tasks to your local hardware**.  
**SECTION 8: Open-Source Models & Local Inference Strategy**

Your Windows 11 Alienware RTX 5080 (16GB GDDR7 VRAM) is a massive, untapped asset. In 2026, 16GB VRAM is the exact "sweet spot" for highly optimized 7B–14B parameter models running at 40+ tokens per second.  
**1\. Model Recommendations by Task (16GB VRAM fit):**

* **Text Classification & Triage (Process Inbox):** Qwen2.5-14B-Instruct or Llama-3.1-8B-Instruct. Fast, highly capable of JSON formatting and strict PARA sorting.  
* **Vision & Sprite QA (Style Enforcer):** Qwen2.5-VL-7B-Instruct. Unmatched for native OCR and analyzing sprite sheets/animation alignments without paying Anthropic's vision pricing.  
* **Semantic Vault Search:** nomic-embed-text. Tiny, instant. Embed your 1,431 notes locally instead of paying API context costs.  
* **Code/JSON Parsing (CSV sanitization):** DeepSeek-Coder-V2-Lite or Qwen2.5-Coder-14B.

**2\. Deployment Methods Compared:**

* **Ollama (Recommended):** Install natively on Windows. It is robust, lightweight, and exposes an OpenAI-compatible REST API automatically. Use this.  
* **Docker/OrbStack:** Too much overhead for just hosting models on Windows; stick to native Ollama.  
* **Hugging Face MCP:** Good for cloud inference, but you have a 5080\. Run local.

**3\. Hybrid Routing Architecture:**  
Implement a router in your SDK (agents-sdk/skill\_loader.py):  
Python  
def route\_task(task\_domain: str, payload: str):  
    \# Route simple classification and vision tasks to the RTX 5080 (Cost: $0.00)  
    if task\_domain in \["inbox\_triage", "vision\_qa", "expense\_categorization", "anki\_gen"\]:  
        return call\_local\_ollama(model="qwen2.5-14b", prompt=payload) \# Points to Alienware IP  
    \# Route complex reasoning and PM strategy to Claude (Cost: $0.05)  
    else:  
        return call\_claude\_api(model="claude-3-5-sonnet", prompt=payload)  
**4\. Specific Workflow Integrations:**

* **Process Inbox:** Local classifier. (Saves \~$3/mo).  
* **Sprite QA Vision Checks:** Local Vision model. *Never* pay Anthropic to check thousands of animation frames. (Saves \~$10/mo).  
* **Financial CSV Parsing:** Local model. Zero risk of bank data leaking to the cloud. (Priceless security).

**SECTION 9: 90-Day Phased Buildout Timeline**

**Phase 1 — Foundation (Weeks 1-4, Feb 23 – Mar 21, Pre-Move)**

* *Focus:* Automate stress, prepare for disruption.  
* **Week 1:** Harden SDK layer. Refactor SKILL prompts for autonomous use. Build Boston Move Mgr.  
* **Week 2:** Finalize Daily Driver and Process Inbox on launchd. Establish the .lock file system.  
* **Week 3:** Build Standup Prep. Implement cost-circuit-breaker and vault-verifier hooks.  
* **Week 4:** Build Spend Analysis agent (with Python sanitization script) to track moving expenses. *System freeze during March 21 move.*

**Phase 2 — Expansion (Weeks 5-8, Late Mar – April, Post-Move Settling)**

* *Focus:* Hardware utilization and restarting the creative pipeline.  
* **Week 5:** Unpack Alienware. Set up Ollama network bridge to Mac. Route Process Inbox to local API.  
* **Week 6:** Migrate high-use Zapier tools to direct Atlassian/GitHub MCPs to reduce latency. Build Sprint Health Monitor.  
* **Week 7:** Build ComfyUI Batch Manager. Connect Comfy API.  
* **Week 8:** Deploy local vision model (Qwen2.5-VL) and build Style Enforcer.

**Phase 3 — Advanced (Weeks 9-12, May)**

* *Focus:* Automation loops and Meta-analysis.  
* **Week 9:** Transition time-based launchd scripts to event-driven triggers (WatchPaths) using Baton Files.  
* **Week 10:** Build Health Audit (PPL tracker) and Festival Tracker.  
* **Week 11:** Implement Knowledge Synthesizer and Fleet Monitor.  
* **Week 12:** Full fleet token audit. Aggressively optimize Prompt Caching breakpoints. Deploy an Agent Team for 16BitFit.

**SECTION 10: Agent SDK vs Agent Teams Decision Framework**

Anthropic's early 2026 release of **Agent Teams** allows 3-5 sub-agents to spawn, share a task list, debate in parallel, and message each other via terminal panes (claude \--teammate-mode tmux).  
**The Decision Framework:**

* **Agent SDK (Python/launchd):** Best for solitary, predictable, scheduled background jobs (Inbox triage, Standup prep, Batch renders). *Low cost, highly reliable.* Use this 90% of the time.  
* **Agent Teams:** Best for exploratory, ambiguous coding or debugging tasks where you need frontend, backend, and QA perspectives simultaneously. *High speed, high token cost.*

**Mapping Your Projects:**

* *Daily standup prep* $\\rightarrow$ **SDK Agent** (Simple data extraction).  
* *Financial analysis of CSVs* $\\rightarrow$ **SDK Agent** (Structured parsing).  
* *Vault-wide knowledge synthesis* $\\rightarrow$ **SDK Agent** (Batch processing).  
* *Animation pipeline multi-stage render* $\\rightarrow$ **SDK Agent** (Pipeline orchestration).  
* *16BitFit full sprint rebuild* $\\rightarrow$ **Agent Teams**. Spawn a team: one on game logic, one on sprite integration, one QA reviewer. *Note: Use Claude Code's new isolation: "worktree" feature so the team builds in a Git sandbox and doesn't break your main branch.*

*Cost Warning:* Agent Teams burn tokens rapidly because 3-5 instances maintain independent context windows. Only use Teams for career R\&D when the parallel speedup justifies a $2.00-$5.00 burst spend.  
**SECTION 11: Things I Haven't Thought Of (Senior Architect Insights)**

1. **The Context Poisoning Loop:** Agents reading 01\_Daily notes will eventually read their *own* previous outputs and hallucinate loops. Ensure vault\_inject writes agent outputs into specific blockquotes (e.g., \> \[\!bot\] Agent Output), and ensure your Read tools are instructed to ignore lines starting with \> \[\!bot\].  
2. **Prompt Caching Cost Trap:** Anthropic charges a premium ($3.75/MTok) to *write* to the 5-minute cache, but reads are cheap ($0.30/MTok). Because your 106 skills are loaded as system prompts, if you space your agent runs 2 hours apart, you will pay the expensive *write* fee every single time. **Architecture fix:** Schedule your morning agents (Standup, Inbox, Move Mgr) to run back-to-back within the same 5-minute window so Agents 2 and 3 get the 90% cache read discount.  
3. **Local TTS for Animation (Cost Optimization):** You use ElevenLabs for voice generation. ElevenLabs is expensive. Since you have an RTX 5080, run **Kokoro TTS** or **Parler TTS** locally. They easily fit in 16GB VRAM, are completely free, and are nearly indistinguishable from ElevenLabs for animatics, directly supporting your debt paydown goal.  
4. **Cursor IDE Workspace Prep:** Since you do creative tech R\&D in the early mornings, have an SDK agent generate a .cursorrules file overnight based on the current active sprint in Jira. When you sit down at 5:00 AM, your Cursor IDE is already primed with the exact context of the bugs you need to fix.  
5. **Memory Leaks in Daemons:** Claude Code CLI patched several memory leaks recently, but long-running daemon agents will still bloat your Mac's RAM over time. Ensure your launchd scripts completely terminate the Python process after completion (ExitTimeOut), rather than keeping a single process alive indefinitely.

