\# Perplexity Computer: Comprehensive Product Analysis

\*\*Published:\*\* March 1, 2026 | \*\*Launch Date:\*\* February 25, 2026 | \*\*Status:\*\* Live for Max subscribers

\*\*\*

\#\# Executive Summary

Perplexity Computer is a cloud-based, multi-model AI agent platform launched on February 25, 2026, by Perplexity AI (valued at $20 billion). It orchestrates 19 different AI models simultaneously to execute complex, multi-step workflows autonomously — from research and coding to design and deployment — running in isolated cloud sandboxes for hours, days, or even months. CEO Aravind Srinivas described it as the company's "next big thing," positioning it as "a general-purpose digital worker" that "unifies every current capability of AI into a single system". Currently available exclusively to Perplexity Max subscribers at $200/month, Computer represents Perplexity's clearest articulation of its thesis that AI models are specializing — not commoditizing — and that the company best positioned to win the next era of AI is the one that orchestrates all of them together.\[1\]\[2\]\[3\]\[4\]\[5\]

\*\*\*

\#\# 1\. What Is Perplexity Computer?

Perplexity Computer is a fundamental departure from the chatbot paradigm. Rather than answering questions and handing work back to the user, Computer accepts a high-level goal and autonomously executes the entire project from start to finish. The distinction Perplexity draws is clear: "Perplexity answers your questions. Computer does your work".\[6\]\[7\]

In practical terms, Computer is a \*\*multi-model, agentic AI platform\*\* that unifies search, research, coding, automation, file management, memory, and media generation in a single environment. Users describe a desired outcome — such as "build a competitive analysis website" or "develop an Android app that assists with research" — and Computer breaks it down into subtasks, delegates those subtasks to specialized sub-agents running different AI models, and delivers the finished result.\[8\]\[4\]\[6\]

Computer solves three core problems that have plagued AI workflows:

\- \*\*Model fragmentation:\*\* Users no longer need to manually switch between Claude, Gemini, ChatGPT, and Grok for different task types.\[9\]  
\- \*\*Workflow discontinuity:\*\* Instead of chaining isolated AI outputs together manually, Computer handles end-to-end execution from idea to deployed artifact.\[7\]  
\- \*\*Statelessness:\*\* Persistent memory means Computer remembers past work, preferences, and project context across sessions.\[10\]\[6\]

\*\*\*

\#\# 2\. How It Works

\#\#\# Orchestration Architecture

At its core, Computer functions as an orchestration layer sitting above multiple foundation models. When a user submits a task, the system follows a structured five-step execution process:\[10\]

1\. \*\*Task graph construction:\*\* Claude Opus 4.6 translates the user's instruction into a structured map of sequential and parallel subtasks — not a linear list, but a project plan that begins executing immediately.\[7\]  
2\. \*\*Concurrent agent swarm:\*\* Sub-agents are spawned for each node simultaneously. One might use Gemini to query live APIs while another uses Opus to write infrastructure code and a third uses Nano Banana to generate UI graphics — all running in parallel.\[1\]\[7\]  
3\. \*\*Self-correction on obstacles:\*\* If a sub-agent hits a deprecated API, a firewall, or a missing dependency, it autonomously spawns helper agents to troubleshoot, researching alternatives and rewriting the relevant section without stopping the overall workflow.\[3\]\[7\]  
4\. \*\*Human escalation only when necessary:\*\* Users are interrupted only when the system encounters a genuine decision that only a human can make.\[7\]  
5\. \*\*Finished artifact delivery:\*\* Completed projects — code, documents, media assets, deployment files — are packaged in Computer's workspace for review, export, or iteration.\[7\]

\#\#\# The Meta-Router

A meta-router analyzes each incoming request, classifies it by type and complexity, and dispatches it to the model or combination of models most likely to produce an accurate result. The routing logic considers multiple factors beyond task type: estimated complexity, latency budget (time-sensitive queries favor faster models), and user history from persistent memory.\[10\]

\#\#\# Sandboxed Compute Environment

Every task runs inside an \*\*ephemeral, compartmentalized cloud sandbox\*\* on Perplexity's infrastructure. Each sandbox includes a real file system, a browser, and tool integrations. The blast radius of any failure is strictly contained — a rogue sub-agent cannot cross the sandbox boundary to touch a user's local machine, network, or corporate infrastructure. When the task finishes, the sandbox is discarded.\[8\]\[7\]

\#\#\# Persistent Memory

Computer maintains memory across sessions at three levels:\[10\]

\- \*\*Short-term memory:\*\* Context within a single conversation thread  
\- \*\*Medium-term memory:\*\* Project context that persists across conversations within a defined timeframe  
\- \*\*Long-term memory:\*\* User preferences, company information, and recurring patterns retained indefinitely until explicitly deleted

This eliminates the repetitive context-setting that consumes the first minutes of every session with stateless AI assistants.\[6\]\[10\]

\#\#\# Asynchronous and Scheduled Execution

Computer runs tasks in the background while users are away. It can monitor email, calendar, flight status, and files with condition-based triggers, and supports scheduled jobs and proactive actions like morning briefings and deadline reminders. Multiple Computer instances can run in parallel.\[3\]\[6\]

\*\*\*

\#\# 3\. The 19 AI Models

Perplexity Computer orchestrates 19 distinct AI models — the largest publicly disclosed multi-model setup in any consumer AI product at launch. The full roster is proprietary and designed to evolve as better models become available, keeping the architecture model-agnostic by design. Six models have been publicly confirmed with their assigned roles:\[7\]

| Model | Provider | Primary Role |  
|-------|----------|-------------|  
| \*\*Claude Opus 4.6\*\* | Anthropic | Core reasoning engine, orchestrator, task graph construction, coding\[1\]\[2\]\[11\] |  
| \*\*Gemini\*\* | Google | Deep research, sub-agent creation, extensive knowledge tasks\[1\]\[11\] |  
| \*\*ChatGPT 5.2\*\* | OpenAI | Long-context recall, broad web search\[1\]\[11\] |  
| \*\*Grok\*\* | xAI | Fast, lightweight task execution\[1\]\[11\] |  
| \*\*Nano Banana\*\* | (Unspecified) | Image generation\[1\]\[3\] |  
| \*\*Veo 3.1\*\* | Google | Video generation\[1\]\[3\] |

The remaining 13 models have not been publicly named. Based on one third-party analysis, the broader roster likely includes Claude Sonnet, o3 (OpenAI), Gemini 3.1 Pro, Llama 4 (Meta), Mistral Large, and several specialized models optimized for code generation, image understanding, and mathematical proof verification. Perplexity has confirmed the lineup will change as models improve, and users can override default routing to pin specific subtasks to preferred models.\[12\]\[10\]\[7\]

\#\#\# Routing Logic

The model selection process extends Perplexity's existing "Model Council" concept from Deep Research — where multiple models are queried and synthesized for accuracy — into full project workflows. Instead of synthesizing answers at the end, the orchestration layer routes different \*types of work\* to different models upfront, letting each operate in its domain of strength. Routing considers:\[7\]

\- \*\*Task type:\*\* Research, code generation, creative writing, mathematical reasoning, image analysis\[10\]  
\- \*\*Complexity:\*\* A simple factual question routes differently than a multi-step analysis\[10\]  
\- \*\*Latency requirements:\*\* Time-sensitive queries favor faster models\[10\]  
\- \*\*User context:\*\* Persistent memory pre-contextualizes queries based on user history\[10\]

Perplexity's internal data supports this approach: December 2025 queries for visual outputs were most often sent to Gemini Flash, software engineering tasks went to Claude Sonnet 4.5, and medical research queries went to GPT-5.1.\[13\]

\*\*\*

\#\# 4\. Connectors & Integrations

Perplexity claims Computer connects to "400+" external services. The platform's connector ecosystem has grown significantly from the Google Drive and Dropbox integrations available to Pro subscribers in 2024\. Below is the most comprehensive list recoverable from official documentation, help center articles, and confirmed user reports.\[14\]\[15\]\[9\]

\#\#\# Confirmed Connectors (Official Documentation)

| Category | Connectors |  
|----------|-----------|  
| \*\*File Storage\*\* | Google Drive\[16\], Dropbox\[16\], Box\[16\], Microsoft OneDrive\[16\], Microsoft SharePoint\[16\] |  
| \*\*Email & Calendar\*\* | Gmail & Google Calendar\[16\], Outlook.com\[16\] |  
| \*\*Communication\*\* | Slack\[16\], Microsoft Teams\[17\] |  
| \*\*Project Management\*\* | Jira\[18\], Asana\[19\], Linear (Enterprise)\[20\], Notion\[16\] |  
| \*\*Knowledge Management\*\* | Confluence\[21\] |  
| \*\*Development\*\* | GitHub (Enterprise)\[16\] |  
| \*\*Data & Analytics\*\* | Snowflake\[6\], Databricks\[6\] |  
| \*\*CRM\*\* | Salesforce\[6\]\[7\] |

\#\#\# Mentioned in Reviews and User Reports

| Category | Connectors |  
|----------|-----------|  
| \*\*Messaging\*\* | Telegram\[22\] |  
| \*\*Social\*\* | Facebook\[23\] |

\#\#\# Connector Architecture

Connectors enable both read and write actions. For example, Computer can pull live data from a connected CRM, commit code to a GitHub repo, update tasks in Linear, or draft and schedule emails from a connected inbox. The integration uses the Merge platform for some connectors to handle user authentication, with data anonymized and neither stored nor logged by the intermediary.\[20\]\[6\]\[7\]

\*\*Important caveat:\*\* Despite the "400+" claim, only approximately 20 specific connectors can be confirmed by name through official documentation and credible user reports. The remainder likely includes connectors accessible through intermediary platforms or integrations that became available at or after Computer's launch. The full list is not published in any single public source.\[15\]\[9\]

\*\*\*

\#\# 5\. Full Capabilities

Computer's capabilities span a remarkably wide range, unifying functions that would previously require multiple separate tools:\[4\]\[6\]

\#\#\# Research & Intelligence  
\- Parallel web search across seven search types simultaneously: web, academic, people, image, video, shopping, social\[9\]  
\- Full source page reading (not just search snippets), including scholarly databases\[9\]  
\- Cross-referencing and source disagreement analysis\[9\]  
\- Continuous competitive intelligence monitoring on schedule\[7\]  
\- Market research agents, financial analysis agents, and news monitoring agents as domain-specific sub-agents\[6\]

\#\#\# Code & Development  
\- Multi-file code generation (React, Next.js, backend services, APIs)\[7\]  
\- Automated testing, debugging, and self-correction\[24\]\[7\]  
\- Deployment to live environments directly from the sandbox\[24\]  
\- GitHub integration for pushing code to repositories\[9\]

\#\#\# Design & Media  
\- Image generation via Nano Banana\[1\]  
\- Video generation via Veo 3.1\[1\]  
\- Logo design, website graphics, branded assets\[7\]  
\- Data visualizations, charts, and interactive dashboards\[13\]

\#\#\# Document & Content Creation  
\- Report generation with citations\[6\]  
\- Slide deck / PPTX creation\[6\]  
\- Spreadsheet generation (Perplexity cites a 4,000-row structured spreadsheet generated overnight)\[7\]  
\- Brand-consistent content using stored brand guidelines from persistent memory\[9\]

\#\#\# Communication & Workflow  
\- Email drafting and sending via connected Gmail/Outlook\[6\]  
\- Slack messaging and notifications\[15\]  
\- Task creation and management in Jira, Asana, Linear\[19\]\[18\]\[20\]  
\- Notion page creation and updates\[16\]

\#\#\# Automation & Scheduling  
\- Condition-based triggers (email arrival, calendar events, file changes)\[6\]  
\- Scheduled recurring tasks (morning briefings, weekly reports, deadline reminders)\[6\]  
\- Always-on background operation for months at a time\[3\]\[1\]

\#\#\# App Building  
\- Full application generation from a single prompt\[24\]\[9\]  
\- Live previews and deployment of micro-apps\[9\]  
\- Website construction with copy, design, and code\[7\]

\*\*\*

\#\# 6\. Pricing & Access

\#\#\# Current Availability

Computer is available exclusively to \*\*Perplexity Max\*\* subscribers on the desktop web app. Rollout to Pro and Enterprise tiers is planned but has no firm timeline.\[25\]\[4\]\[13\]

\#\#\# Subscription Tiers

| Plan | Monthly Price | Annual Price | Computer Access |  
|------|-------------|-------------|-----------------|  
| \*\*Free\*\* | $0 | $0 | No |  
| \*\*Pro\*\* | $20 | $200/year | Coming soon\[26\] |  
| \*\*Max\*\* | $200 | $2,000/year | Yes — 10,000 credits/month\[4\]\[27\] |  
| \*\*Enterprise Pro\*\* | $40/seat/month | $400/seat/year | Not yet\[28\] |  
| \*\*Enterprise Max\*\* | Custom | Custom | Coming soon\[26\] |

\#\#\# Credit System

Computer operates on a usage-based credit system layered on top of the Max subscription fee:\[26\]

\- \*\*Monthly allowance:\*\* 10,000 credits per month (included with Max)\[4\]\[26\]  
\- \*\*Launch bonus:\*\* One-time 20,000 bonus credits (expires 30 days after grant)\[26\]\[4\]  
\- \*\*Standard Perplexity searches remain unlimited\*\* and do not consume credits\[26\]  
\- \*\*Credit consumption varies\*\* based on task complexity and models used — heavier models (Opus, large Gemini, Veo) cost more per task than lightweight ones (Grok)\[26\]\[7\]  
\- \*\*No per-model rate card\*\* has been published; task-level cost requires real-world testing to calibrate\[7\]

\#\#\# Spending Controls

\- \*\*Auto-refill:\*\* Triggers when balance drops below 500 credits ($5 worth); off by default\[26\]  
\- \*\*Default spending cap:\*\* $200/month on additional credit purchases (adjustable up to $2,000)\[26\]  
\- \*\*Pause, not cancel:\*\* If credits run out mid-task, the job pauses and preserves all progress until credits are replenished\[26\]  
\- \*\*Credit types:\*\* Monthly (reset on billing cycle, don't roll over), Purchased (expire after 1 year of inactivity), Bonus (expire on stated date)\[26\]  
\- \*\*Mobile:\*\* Credit-consuming features not yet available on mobile\[26\]

\*\*\*

\#\# 7\. Real-World Use Cases

\#\#\# Documented User Workflows

Several concrete examples have been documented since launch:

\*\*Branded micro-app development:\*\* One user gave Computer a brand guidelines file, requested a callout box generator, then a table generator in the same style — both apps with live preview and PNG export, pushed to a GitHub repo — in under 30 minutes total.\[9\]

\*\*S\&P 500 interactive bubble chart:\*\* A prompt requesting an interactive bubble chart for every S\&P 500 company (X-axis: revenue, Y-axis: net profit, bubble size: market cap, color: share price change) with 10+ annotated insights, packaged as a shareable website.\[9\]

\*\*Tesla stock price animated GIF:\*\* An animated visualization of Tesla's stock price over 10 years with annotated inflection points (Cybertruck unveil, S\&P 500 inclusion, stock splits, earnings misses) fading in and out along the timeline.\[9\]

\*\*Overnight structured data generation:\*\* Perplexity cites internal benchmarks of a 4,000-row structured spreadsheet generated overnight — a task that would normally take a skilled analyst a full week. (Note: these claims have not been independently replicated.)\[7\]

\#\#\# Example Workflow Demonstrated by Perplexity

"Research our top 5 competitors, compare their pricing, create a slide deck with the findings, and email it to the team." Computer runs parallel web searches, builds a comparison table, generates a branded PPTX, and sends it via connected Gmail — all in one session.\[6\]

\*\*\*

\#\# 8\. Competitive Landscape

\#\#\# Head-to-Head Comparison

| Dimension | Perplexity Computer | OpenClaw | Claude Cowork |  
|-----------|-------------------|----------|---------------|  
| \*\*Launch\*\* | Feb 25, 2026\[9\] | Jan 2026\[29\] | Late 2025\[23\] |  
| \*\*Approach\*\* | Multi-model cloud orchestration\[2\] | Local-first open-source agent\[29\] | Single-model desktop agent\[9\] |  
| \*\*Models\*\* | 19 models (multi-provider)\[4\] | Model-agnostic (plug in via API)\[30\] | Anthropic models only\[9\] |  
| \*\*Execution\*\* | Cloud sandbox\[7\] | Local machine (full system access)\[29\] | Desktop VM on user's machine\[31\] |  
| \*\*Price\*\* | $200/month \+ usage credits\[13\] | Free (open-source) \+ API costs\[31\] | $20-$200/month\[31\] |  
| \*\*Setup\*\* | Zero install, browser-based\[7\] | SSH, Docker, local infrastructure\[7\] | Desktop app install\[29\] |  
| \*\*Security\*\* | Isolated ephemeral sandbox\[7\] | Direct local file & shell access\[7\] | Sandboxed VM\[31\] |  
| \*\*Always-on\*\* | Yes (cloud, runs for months)\[1\] | Yes (requires computer on)\[23\] | Yes (requires computer on)\[9\] |  
| \*\*Messaging\*\* | Via connectors (Slack, Teams)\[16\] | WhatsApp, Telegram, Slack, iMessage\[29\] | No direct messaging\[23\] |

\#\#\# Where Computer Wins

\- \*\*Multi-model advantage:\*\* No other consumer product orchestrates 19 models simultaneously. Claude Cowork is limited to Anthropic models, and OpenClaw typically routes through a single model at a time.\[9\]\[7\]  
\- \*\*Zero-setup deployment:\*\* No Docker, SSH, or local infrastructure management required.\[7\]  
\- \*\*Security posture:\*\* Cloud sandbox isolation means failures cannot reach user networks or files — a direct response to OpenClaw's documented security incidents (341 malicious plugins found, 11.3% contamination rate; near-deletion of a security researcher's email archive).\[7\]  
\- \*\*Long-running background execution:\*\* Tasks can run for months without requiring a user's computer to stay on.\[1\]

\#\#\# Where Computer Falls Short

\- \*\*No local system access:\*\* Computer cannot control the user's desktop, file system, or native applications the way OpenClaw or Claude Cowork can.\[9\]\[7\]  
\- \*\*Price premium:\*\* At $200/month plus usage credits, it is significantly more expensive than the free OpenClaw or $20/month Claude Cowork.\[31\]  
\- \*\*Data governance:\*\* All execution passes through Perplexity's cloud infrastructure, which introduces data governance considerations for regulated industries that self-hosted alternatives like OpenClaw avoid.\[7\]  
\- \*\*Early maturity:\*\* The product is days old. TechCrunch reported that Perplexity cancelled a planned press demo "because of flaws found in the product hours before the event".\[13\]

\*\*\*

\#\# 9\. Limitations & Known Issues

\#\#\# Confirmed Limitations

\- \*\*Desktop web only at launch:\*\* No mobile credit support yet; Computer is only accessible on web desktop.\[26\]\[6\]  
\- \*\*Credit visibility gaps:\*\* Without a published per-model rate card, users cannot precisely predict task costs in advance. Multi-agent workflows can burn credits quickly.\[7\]  
\- \*\*Cancelled demo:\*\* Perplexity cancelled a planned press demonstration hours before a media event due to product flaws discovered at the last moment. This signals early-stage instability.\[13\]  
\- \*\*Unverified benchmarks:\*\* The 4,000-row overnight spreadsheet and other internal performance claims have not been independently replicated.\[7\]  
\- \*\*Data governance concerns:\*\* All execution runs on Perplexity's cloud infrastructure. Organizations in regulated industries (healthcare, finance, legal) should carefully evaluate what data is appropriate to route through a third-party cloud platform.\[7\]  
\- \*\*Connector list opacity:\*\* Despite claiming "400+" connectors, only \~20 can be confirmed by name through official documentation.\[15\]\[9\]  
\- \*\*Watermarking:\*\* Computer adds "Generated with Perplexity Computer" watermarks to generated applications.\[9\]  
\- \*\*Agent governance risks:\*\* Autonomous agents acting across real tools require internal approval workflows, audit trails, and human-in-the-loop checkpoints — especially for financial data or external system actions.\[7\]

\#\#\# Broader Platform Concerns

\- Some users have reported quality degradation when Perplexity wraps models versus using native APIs — personality nuance and creative range can be diminished by the aggregation layer's system prompts and routing filters.\[32\]  
\- An MIT study flagged that Perplexity's Comet browser (a related product) had no specific safety testing or benchmark performance disclosures documented.\[33\]

\*\*\*

\#\# 10\. Strategic Context

\#\#\# The "Multi-Model Is the Future" Thesis

Perplexity Computer is the product expression of a thesis the company has been refining for over a year: that AI models are not converging into general-purpose commodities but are instead specializing, and the company best positioned to win is the one that orchestrates them all. CEO Aravind Srinivas wrote on the day of launch: "When models specialize, they just become tools similar to the file system, CLI tools, connectors, browser, search".\[2\]\[5\]

One Perplexity executive put it bluntly: "Multi-model is the future." Models, in their view, are specializing, not commoditizing. The company has found that users frequently switch between models to obtain the results they are looking for — evidence they cite as proof that no single model dominates across all task types.\[13\]

\#\#\# The Advertising Pivot

Computer's launch comes weeks after Perplexity made another major strategic decision: fully abandoning advertising. The company had generated only approximately $20,000 in ad revenue in 2024 (out of $34 million total), and executives concluded that ads undermined users' trust in answer accuracy. By late 2025, Perplexity reportedly reached $200 million in annual recurring revenue from subscriptions alone. The subscription-only model, anchored by the $200/month Max tier, is now the company's sole monetization strategy for consumers.\[34\]\[35\]\[36\]\[37\]\[13\]

\#\#\# The Samsung Distribution Play

Simultaneously with Computer's launch, Perplexity announced a multi-year partnership with Samsung for native OS-level integration on the Galaxy S26 series. The Perplexity app comes preloaded on every Galaxy S26 — making Perplexity the first non-Google company to receive OS-level access on a Samsung device. Users can activate it via "Hey Plex" or the side button, with deep integration across Samsung's Calendar, Notes, Gallery, Clock, and Reminders apps. Samsung's revamped Bixby now also uses Perplexity's APIs for web search and reasoning.\[38\]\[39\]\[4\]

\#\#\# Existential Threat to "AI Wrapper" Startups

Computer natively unifies frontier models from multiple providers and autonomously handles routing logic between them. The fundamental value proposition of single-purpose AI wrapper tools — "we connect model X to workflow Y" — is substantially diminished when an orchestration platform does that routing dynamically across 19 models as a baseline feature. What survives this shift: highly proprietary datasets, deeply specialized hardware integrations, and genuinely vertical-specific workflows with unique compliance requirements.\[7\]

\*\*\*

\#\# 11\. Surprising Facts & Non-Obvious Insights

\#\#\# For Product Managers

\- \*\*Computer uses Parallel-Agent Reinforcement Learning (PARL):\*\* This training paradigm teaches the orchestrator to keep the full agent swarm running concurrently, preventing the "serial collapse" problem where multi-agent systems default to sequential execution despite having parallel capacity. Understanding PARL is valuable for any PM thinking about multi-agent product architectures.\[40\]\[7\]  
\- \*\*The Model Council architecture predates Computer:\*\* Computer extends Perplexity's existing "Model Council" concept from Deep Research — where multiple models are queried and synthesized for accuracy — into full project workflows. This pattern (query multiple models → synthesize) is a design pattern worth studying for any product that aggregates AI outputs.\[7\]  
\- \*\*Users can override routing and pin models to subtasks:\*\* This gives power users granular control over cost and quality tradeoffs per sub-agent. It's a clever hybrid of automatic and manual model selection that balances simplicity with control.\[41\]\[7\]  
\- \*\*Perplexity was using Computer internally since January 2026\*\* for real workflows — content publishing, app development, spreadsheet creation, documentation deployment — before the public launch. This is not a beta.\[42\]\[7\]

\#\#\# For Technical Creatives

\- \*\*Seven parallel search types simultaneously:\*\* Computer doesn't search sequentially — it runs web, academic, people, image, video, shopping, and social searches concurrently and cross-references results. This is a fundamentally different research architecture than any single-model tool offers.\[9\]  
\- \*\*Brand memory for design consistency:\*\* Uploading a brand guidelines file lets Computer generate consistently branded assets — apps, callout boxes, tables, social graphics — without re-explaining brand specs each time.\[9\]  
\- \*\*Search-to-deploy pipeline:\*\* Computer can go from a natural language prompt to a deployed, live website or application without the user touching an IDE, terminal, or hosting provider. The implications for rapid prototyping and MVPs are significant.\[24\]

\#\#\# For AI Fluency

\- \*\*The connector architecture is the moat, not the models:\*\* As one LinkedIn commenter noted, "orchestration alone won't be the moat. The real differentiation will come from who owns persistent memory and state, domain-specific data and workflows, and developer ecosystems". Computer's 400+ connectors and persistent memory may matter more than which 19 models are in the roster.\[5\]  
\- \*\*Claude Opus 4.6 as the reasoning backbone validates Anthropic's position:\*\* Despite competing with Claude Cowork, Perplexity chose Opus as the core orchestrator — meaning Anthropic profits from Computer's success regardless. This "frenemy" dynamic is a pattern worth tracking across the AI industry.\[9\]  
\- \*\*Perplexity's own search API now powers the index:\*\* The company is no longer reliant on other companies' APIs for its web index and now has its own AI-optimized search API. This is an underappreciated infrastructure development.\[13\]  
\- \*\*The $200/month price point is an industry convergence:\*\* Perplexity Max, OpenAI's ChatGPT Pro, and Anthropic's Claude Max all landed at $200/month. Google's Gemini AI Ultra is $249.99. This isn't a coincidence — it reflects the actual compute economics of running heavy agentic workloads, and suggests this price tier is where serious AI productivity tools will live for the near future.\[43\]\[7\]  
\- \*\*Credit-based pricing may become the standard for agentic AI:\*\* Flat-rate subscriptions proved economically unsustainable for AI providers handling heavy agent workloads (Anthropic was forced to clamp down on developers abusing flat-rate subscriptions for massive agent tasks). Perplexity's credit model — designed from the start to keep economics sustainable — may preview how all agentic AI products are priced going forward.\[7\]

---

Here's the comprehensive report on Perplexity Computer. It covers all 11 requested sections drawing from 30+ sources including Perplexity's official help center and changelog, VentureBeat, TechCrunch, Ars Technica, Forbes, hands-on user reviews, and CEO Aravind Srinivas's own launch announcement.

A few things worth flagging for you specifically, Sean:

The connector list gap is real. Despite the "400+" claim, only \~20 connectors can be confirmed by name through official docs. This is a transparency issue worth watching — especially given your role at The Block, where you'd want to verify integration claims before writing about them or recommending them internally.

The cancelled demo is a yellow flag. TechCrunch confirmed Perplexity pulled a press demo hours before a media event due to product flaws. Days-old software at this ambition level will have rough edges.

The PARL architecture and Model Council pattern are worth studying for your PM portfolio — they represent genuinely novel approaches to multi-agent coordination that you could reference in product case studies about agentic AI design patterns.  
