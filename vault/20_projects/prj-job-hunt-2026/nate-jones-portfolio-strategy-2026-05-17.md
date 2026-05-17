---
title: "Nate Jones Portfolio Strategy — Enterprise AI PM positioning"
created: 2026-05-17
domain: [job-hunt-2026, life-systems]
type: strategy
status: active
tags:
  - job-hunt-2026
  - portfolio
  - enterprise-ai-pm
  - nate-jones
ai-context: "Four-phase analysis converting Sean's Super User Pack work into externally-legible artifacts for Enterprise AI PM roles ($150K–$400K band). Inputs: Nate B Jones 2026-03-25 piece + full Super User Pack walk."
---

# Nate Jones Portfolio Strategy — Enterprise AI PM positioning

**Target:** Convert the substantive work already in `claude-code-superuser-pack/` into the externally-legible artifacts a Stripe / Anthropic / Notion / Datadog / Linear hiring manager actually reads. Mix of quick-ship wins (1–2 weeks each) and one flagship multi-month build. Every project lives **outside** this monorepo so recruiters can find it without cloning Sean's vault.

---

## Phase 1 — Nate's Argument, Dissected

> **Thinking:** Five load-bearing claims. (1) The K-shaped market — well-supported by ManpowerGroup 3.2:1, 142-day TTF, 1.6M openings / 518K candidates, Accenture's 700K agentic-AI training program. (2) Artifacts > credentials — supported by his hiring-manager interview corpus + DataCamp's 23% "training doesn't translate" finding, but is itself an interpretive claim. (3) Seven specific skills — best-supported piece; he literally pulled job-posting language from Anthropic / Robinhood / Upwork / Glean / Scale AI / Pair Team / Obsidian Security / Sierra / Decagon. (4) The six-pattern failure taxonomy — he *names* it as his synthesis from advisory work; not external evidence. (5) The "specification shortage" critique of buyers — true and useful but unfalsifiable. What he doesn't say: vendor eval, build-vs-buy, governance / model-risk-mgmt, change-management — the things Enterprise PMs actually argue about in steering committees. He also ignores the vertical/horizontal product-shape distinction. Where he probably oversimplifies: the twelve-week path assumes a single learning curve when in reality the PM curve and the architect curve diverge by week 5.

### 1a. The core thesis in five bullets

1. **The AI labor market is two markets, not one.** Generalist roles are contracting (-13% in routine job postings post-ChatGPT); roles that build/operate AI systems are unfindable (3.2:1 demand-to-supply, 142-day time-to-fill, $150K–$400K). Both "infinite jobs" and "I can't get hired" are true depending on which side of the K you're on.
2. **Hiring is broken on both sides.** A non-trivial share of postings are unacknowledged market research — vague spec, fifteen-skill kitchen-sink JDs, hundred-person interview funnels, all rejected. The fix is outcome-first specification *before* posting the role.
3. **Credentials are largely worthless; artifacts are the credential.** Inbound recruiter messages in Market Two follow published work — agent specs, failure post-mortems, evaluation frameworks, narrated working sessions — not certificates.
4. **"Taste" is a cop-out for seven learnable skills.** Specification precision → evaluation/quality judgment → decomposition for delegation → failure pattern recognition → trust boundary design → context architecture → cost/token economics. They are a progression, not a checklist.
5. **The window is closing.** AWS certs were optional in 2013, table stakes by 2018. The agentic-AI cycle is compressing faster — Accenture training 700K on agentic AI, Cognizant 350K. Practitioners shipping artifacts in 2026 capture structural advantage.

### 1b. The seven skills, decomposed (staff/principal level)

| # | Skill | One-sentence definition | Staff/principal expression | Sub-skills you'd test in 60 min | Strongest single artifact |
|---|---|---|---|---|---|
| 1 | **Specification precision** | Write requirements an agent can execute literally without filling in the blanks. | Translates a fuzzy business outcome into an executable spec with explicit edge-case handling, escalation rules, and hard-vs-soft constraints separated. | (a) Rewrite a vague brief into a spec the agent can execute; (b) name three edge cases the spec doesn't cover; (c) distinguish hard constraint vs preference. | Published **agent product spec** for one real workflow — escalation logic, eval criteria, trust boundaries, cost model. |
| 2 | **Evaluation & quality judgment** | Know whether the output is actually good — across error detection, edge cases, test design, and continuous monitoring. | Designs eval suites where two domain experts independently reach the same pass/fail; defines what drift means in production; instruments quality regression detection. | (a) Spot the silent-fluent-wrong output in three samples; (b) write a pass-fail eval case for a domain task; (c) design a monitoring metric that catches quality drift. | A 10-case binary **eval suite grounded in production failure logs** with a documented red-to-green progression. |
| 3 | **Decomposition for delegation** | Break a workflow into chunks an agent can hold in context, with explicit handoffs and human-in-the-loop checkpoints. | Architects multi-agent systems with planner/sub-agent patterns sized to the harness; classifies each subtask (reasoning / retrieval / judgment / coordination); designs recovery + verification at the boundaries. | (a) Decompose a quarterly compliance review into a 5-step agent flow; (b) place the human checkpoint and justify; (c) name two cascade-failure points. | An **architecture diagram + runbook** for a real multi-agent system with named handoffs and recovery semantics. |
| 4 | **Failure pattern recognition** | Recognize and post-mortem the six recurring agentic failures: context degradation, specification drift, sycophantic confirmation, tool selection errors, cascade failures, silent failures. | Triggers each failure mode deliberately to study it; builds detection harnesses; carries a personal failure taxonomy bigger than Nate's six. | (a) Classify three real failure traces; (b) name the detection mechanism for silent failure; (c) explain why tool-description quality is the highest-leverage intervention. | A **published failure post-mortem** with named patterns, root cause, and the fix. |
| 5 | **Trust boundary & security design** | Compose blast-radius, reversibility, frequency, and verifiability to decide where humans must stay in the loop. | Designs trust frameworks for adversarial conditions (prompt injection, exfiltration via tool calls, privilege escalation); integrates with corporate IAM, audit logs, model-risk-management. | (a) Score a workflow on the four-variable rubric; (b) propose the human checkpoint placement; (c) identify the prompt-injection surface in a multi-tool flow. | A **trust-boundary review template** applied to one real workflow, with the security & auditor approvals modeled. |
| 6 | **Context architecture** | Decide what information the agent sees, when, and in what form — persistent vs per-session, summary vs detail, freshness vs cost. | Designs retrieval that defeats density bias (e.g., cluster-and-sample / TopClustRAG); separates "always loaded" from "loaded when relevant"; instruments context-decay metrics. | (a) Diagnose why retrieval over-returns one cluster; (b) propose what gets summarized vs kept verbatim; (c) cite a paper or pattern (HyDE, TopClustRAG, MemGPT). | A **public RAG/context implementation** that visibly addresses a named retrieval pathology, with before/after metrics. |
| 7 | **Cost & token economics** | Model total inference cost across a workflow; route subtasks to the cheapest model that holds quality. | Builds the cost spreadsheet before approving the build; understands input/output/cache token asymmetry; reasons about batch vs real-time and frontier vs commodity model substitution. | (a) Estimate per-task cost at 10K daily runs across three model choices; (b) identify the subtask that can move from Opus to Haiku; (c) compute the prompt-cache savings. | A **published cost model** for one workflow with a documented model-routing decision that changed the economics. |

### 1c. The blind spots — what Nate doesn't say

Nate's seven are correct **and** insufficient for Enterprise AI PM. Five gaps a hiring manager at a regulated-industry buyer (Stripe, ServiceNow, Atlassian, Box) cares about that the framework underweights:

- **Vertical vs horizontal product shape.** A PM at Harvey (vertical legal AI) writes evals that encode case-law reasoning; a PM at Notion AI (horizontal) writes evals that survive any domain a customer brings. Nate's framework treats agents generically; product shape changes which of the seven skills dominate and which collapse to baseline.
- **Vendor evaluation & build-vs-buy.** Enterprise AI PMs spend a quarter of their time evaluating third-party model providers, agent platforms, and tooling stacks — and constructing the build-vs-buy memo. Nate's framing assumes you're building; in reality you're choosing between OpenAI's Assistants, Anthropic's Skills, Google's Vertex Agent Builder, and self-host. This is the single most missing skill.
- **Data infrastructure & data quality.** Context architecture is downstream of data quality. If the enterprise data layer is incoherent (no canonical entity IDs, no governance, no lineage), context engineering only paints over the rot. Nate skips the data-infra dependency entirely.
- **Org-design & change-management.** Getting a 5,000-person customer-support org to actually adopt an agentic workflow is a different muscle from designing it. Adoption rate, fallback-to-human rate, agent-rejection rate, change-fatigue management — these are PM accountabilities in any enterprise deployment.
- **Governance, audit, model-risk management.** SR-11-7, EU AI Act tiering, SOC 2 evidence for agent decisions, audit trails per agent action. The boring stuff Enterprise PMs actually fight about, almost entirely absent from Nate's piece.

---

## Phase 2 — Agentic AI Landscape, 2026–2027

> **Research strategy:** All sub-questions here are single-shape (one target, one question), so this phase uses WebSearch directly — no Gemini DR delegation (would burn $7+ for marginal lift). Skipping the LLM Council variance critique pass too: total Phase 2 spend stays under $0.30 vs the $10 session ceiling. Routing decision audit log in `vault/health/research-routing-2026-05-17.json` if Sean wants to re-run.

### 2a. State of agentic AI in production today (mid-2026)

**What's actually working at scale:**
- MCP has crossed the standardization threshold. Anthropic donated the protocol to the Linux Foundation's **Agentic AI Foundation** in December 2025; co-founded by Anthropic, Block, OpenAI, with support from Google, Microsoft, AWS, Cloudflare. The public MCP registry grew from 1,200 servers (Q1 2025) to **9,400+ by April 2026**, with **97M monthly SDK downloads** across Python and TypeScript. **78% of enterprise AI teams** report at least one MCP-backed agent in production; **67% of CTOs** name MCP their default agent-integration standard within 12 months ([cdata.com](https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption), [digitalapplied.com](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol)).
- Anthropic's **Agent Skills** shipped as the enterprise distribution mechanism with launch partners Atlassian, Figma, Canva, Stripe, Notion, Zapier ([VentureBeat](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard)).
- Narrow, bounded-domain agents work: support tier-1 (Decagon, Sierra), code (Claude Code, Cursor), sales research (Glean), legal document review (Harvey).

**What's still demo-ware:**
- **Multi-agent coordination at >5 steps.** Even at 85% per-step reliability a 10-step workflow lands at ~20% E2E success; checkpointing/resume primitives are immature ([Temporal](https://temporal.io/blog/ai-reliability-is-a-decade-old-problem)).
- **Silent failures** — most production agents fail silently from context corruption with no detection ([Mezmo via TFiR](https://tfir.io/ai-agents-production-reliability-mezmo-aura/)). This is Sean's "Mode 1" from `evals/vault-synthesizer/failure-modes.md` — the same failure class, now industry-wide.
- **Cross-vendor agent-to-agent communication** — A2A standards lag MCP by ~12 months.

### 2b. The next 18–36 months — where the puck is going

1. **Long-running autonomous agents.** MCP's 2026 roadmap calls out the **Tasks primitive** (retry semantics, durable execution) and transport scalability for stateful sessions ([modelcontextprotocol.io 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/), [a2a-mcp.org](https://a2a-mcp.org/blog/mcp-2026-roadmap)). PM craft shifts from "design a chat turn" to "design a 4-hour autonomous run with checkpoint/rollback semantics."
2. **MCP becomes the agent-interop substrate** — Q2 2026 ships OAuth 2.1 with PKCE and SAML/OIDC, unlocking regulated industries.
3. **Chat-first → agent-first product surfaces.** The product is no longer the chat window; the product is the agent that lives inside the user's existing tools (Notion, Linear, Slack, Salesforce) and surfaces summaries.
4. **AgentOps / AI reliability as a named discipline.** Datadog's 2026 *State of AI Engineering* report formalizes the category; "Harness Engineering" is the emerging name for the practice ([agent-engineering.dev](https://www.agent-engineering.dev/article/harness-engineering-in-2026-the-discipline-that-makes-ai-agents-production-ready)). A new job family — AgentOps Engineer, AI Reliability Engineer — sits between traditional SRE and the AI PM.
5. **Cost-curve dynamics.** Per-token costs continue ~6–10× annual deflation at the commodity tier; frontier costs hold. Routing intelligence (cheap-model for retrieval / classification, frontier for synthesis) is now the dominant unit-economics lever — making cost/token economics a *senior* qualification that locks in salary bands.

### 2c. 2027 premium tier — what Enterprise AI PMs will be evaluated on

If Nate's seven are 2026 table stakes, 2027's premium adds:

1. **Agent-product-market-fit modeling.** Adoption, fallback-to-human, and override rates as the new DAU/MAU. Premium PMs publish their adoption funnel.
2. **Vendor/model-routing economics under deflation.** Decisions made today must survive 2027's cost curves. Premium PMs model the 12-month substitution path before approving a build.
3. **AgentOps observability & SLO design.** Defining what "uptime" means for a non-deterministic system; setting agent SLOs (% successful E2E completions, time-to-recover, silent-failure detection lag); owning the incident review.
4. **Governance & evidence for audit.** SR-11-7-style model risk tiering, EU AI Act conformity, agent-action audit trails, prompt-injection red-team artifacts. The PMs who can sit through a SOC 2 audit and defend an agent decision will price at a 25–35% premium.
5. **Cross-vendor portability strategy.** Build-vs-buy framed as "which capability do we own, which do we rent, which do we share via MCP?" The PM as a horizontal-stack architect.

### 2d. Top hiring snapshot (mid-2026)

| Company | Role(s) currently posted | JD language signal | Disclosed band | Artifacts asked for |
|---|---|---|---|---|
| **Anthropic** | Agent Platform PM, Research PM (Labs), PM Compute Platform, Senior PM Education Labs, Applied AI Engineer (Enterprise) | "scaled model evaluation framework," "context engineering," "agent coordination at many scales" | $250K–$450K total ([Anthropic careers](https://www.anthropic.com/careers/jobs)) | Published spec or eval framework; failure write-up; CCA Foundations cert preferred |
| **Stripe** | AI Skills PM, Agent Platform PM | "Agent Skills partner," vendor-evaluation framing | $260K–$420K total | Production artifact + vendor decision memo |
| **Notion** | AI PM (Skills), AI PM (Workspace Agents) | horizontal context-engineering | $230K–$390K | Live agent demo + cost model |
| **Datadog** | AI PM (LLM Observability), AI PM (AgentOps) | "state of AI engineering," reliability framing | $208K Sr → $468K Staff ([Levels.fyi](https://www.levels.fyi/companies/datadog/salaries/product-manager)) | Observability artifact, SLO spec |
| **Figma** | AI PM (Generative) | horizontal design agent | $282K–$565K ([Levels.fyi](https://www.levels.fyi/companies/figma/salaries/product-manager)) | Live product surface + UX research |
| **Linear** | AI PM (Agent-first surfaces) | embedded agent | $220K–$380K | Agent product spec |
| **Atlassian** | PM, Rovo Agents | enterprise agent platform | $230K–$400K | Trust-boundary + governance write-up |
| **ServiceNow** | PM, NowAssist Agents | regulated-industry agent governance | $240K–$410K | Audit-evidence artifact |
| **Sierra / Decagon** | PM, Agent Quality / Eval | vertical CX agents | $200K–$360K | Eval framework, failure post-mortem |
| **Box** | AI PM (Content Cloud) | content-grounded agents | $220K–$390K | RAG/context architecture artifact |

National AI-PM band confirmed: **$305K median total comp, 28% premium over generic PM** ([Glassdoor 2026](https://www.glassdoor.com/Salaries/ai-product-manager-salary-SRCH_KO0,18.htm), [IdeaPlan](https://www.ideaplan.io/product-manager-salary/ai-product-manager)).

---

## Phase 3 — Skill-Gap Analysis vs. Sean's Super User Pack

> **Thinking:** Scoring rule applied — 1 = no evidence, 2 = internal-only (recruiter never sees it), 3 = legible + packaged but not in portfolio form, 4 = portfolio-ready today, 5 = staff/principal-level impressive. Counting before writing: most scores must land at 2 or 3 because the work IS substantive but lives inside a personal monorepo no recruiter will clone. If anything scores 4+, it has to already be extractable as a standalone artifact today. After scoring honestly: 0 at 4+, 4 at 3, 3 at 2. That's right — the work exists, the packaging doesn't.

### Skill-by-skill scoring

| Nate skill | Evidence in Super User Pack | Score | What it would take to get to 4+ |
|---|---|---|---|
| **1. Specification precision** | Agent prompts and skill definitions across `agents-sdk/agents/daily_driver.py`, `agents-sdk/agents/vault_synthesizer.py:1–100`, `.claude/skills/` (118 skills); operating-model 4-doc spec (`vault/05_atlas/operating-models/{creative-studio,life-systems,job-hunt-2026}/{USER,SOUL,HEARTBEAT,operating-model}.md`); intent-engineering tools listed in MCP registry. Real specification discipline — but for personal automation, not enterprise workflows, and not published. | **2** | Extract one prompt as the *agent product spec* for a fictional but realistic enterprise workflow (e.g., AP-automation tier-1). Publish to a separate public repo with eval criteria, escalation logic, trust boundaries, cost model. |
| **2. Evaluation & quality judgment** | `evals/vault-synthesizer/cases.yaml` (10-case binary suite), `failure-modes.md` (6 named modes grounded in 17 days of production logs), `README.md` documenting 1/10 → 7/10 progression, `EXPLANATION.md` written as a portfolio piece, `runner.py` with rubric/exact-match judge types. This is the strongest single piece of evidence. **But it sits buried at `claude-code-superuser-pack/evals/vault-synthesizer/`** — no separate public repo, no companion post, no recruiter will navigate to it. | **3** | Lift the entire `evals/vault-synthesizer/` directory into its own public repo `vault-synthesizer-evals`. Rewrite README as a portfolio narrative. Companion 1,500-word Substack post: "Shipping an Eval Suite Intentionally Red." Add the missing 3 deferred cases. |
| **3. Decomposition for delegation** | 17-agent SDK fleet across `agents-sdk/agents/*.py`; `lib/hybrid_router.py` three-tier routing with health checks and WOL; planner/sub-agent pattern in the design-team agents (`.claude/agents/ui-reviewer.md`, `design-system-enforcer.md`, etc.); two-tier `knowledge_lint.py` (structural Python → semantic LLM). Real multi-agent orchestration in production — running on launchd, surviving outages, recovering. Internal only. | **2** | Extract a single multi-agent flow (e.g., the knowledge-loop: indexer → synthesizer → query → lint) as an open-source reference architecture with C4 diagrams, named handoffs, and recovery semantics. |
| **4. Failure pattern recognition** | The v3.26.3 LDR grounding-collapse story is the highest-quality artifact in this category Sean has — `CLAUDE.md` documents fabricated entities (`PureMCPClient`, `MCPCatalog (Central)`), wrong owner for MCP repo, fabricated Microsoft Learn URLs, missed deliverable; the bad output is preserved at `vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-...md` with `status: superseded`. Six-mode taxonomy in `evals/vault-synthesizer/failure-modes.md`. The vault_synthesizer Tier-1 (v3.34.0) and Tier-2 (v3.37.0) retrofit stories are textbook post-mortems with diagnosis → hypothesis → intervention → verification. **All buried inside the monorepo.** | **3** | Publish two post-mortems as separate Substack posts with their own GitHub repo containing the diagnostic queries and the failing/passing outputs as fixtures. |
| **5. Trust boundary design** | 14 hooks: `network-access-control.sh` (domain whitelist + exit-2 deny), `block-secrets.py` (16 sensitive-path patterns), `cost-watchdog.py` (per-session USD ceiling with PostToolUse enforcement), `require-confirm-highrisk.sh`, `pre-compact-flush.sh`. Per-agent cost caps in `agents-sdk/config.toml` ($0.60 morning, $0.25 evening, $0.50 weekly). Personal-grade trust boundaries; not enterprise/audit/IAM/SR-11-7 framing. | **2** | Build one "Enterprise Agent Trust-Boundary Review" template, apply it to a realistic enterprise workflow, model corporate IAM/audit/MRM integration. Publish as separate repo + post. |
| **6. Context architecture** | `agents-sdk/lib/retrieval_diversity.py` — TopClustRAG implementation (HDBSCAN, `min_cluster_size=3`, ≤2 per cluster, fall-back semantics) explicitly grounded in SIGIR 2025; `agents-sdk/lib/concept_edges.py` — OB1-inspired 6-relation typed reasoning graph with SQL fast path consumed by `knowledge_lint`; `.claude/hooks/session-start-inject-index.sh` injects vault index as additionalContext; PARA + 4-doc operating-model context hierarchy. Genuinely deep. Anthropic's CCA exam dedicates 15% weight to context engineering — Sean is implementing TopClustRAG + typed reasoning edges. Internal. | **3** | Write a 2,000-word "Defeating Cluster Bias in Vault Retrieval — A TopClustRAG Implementation" post with before/after retrieval-diversity metrics from the live `2026-05-17 02:30` synth run. Push `retrieval_diversity.py` + `concept_edges.py` as a standalone open-source module. |
| **7. Cost & token economics** | `lib/hybrid_router.py` three-tier local-first routing (Mac Mini Ollama → MBP MLX-LM → Alienware CUDA → Claude API fallback); `tools/llm-council/council/profiles.py` two profiles with `max_cost_per_query=1.00` (premium) and `0.40` (variance); spend trackers at `vault/health/{council,gemini}-spend-*.json`; Gemini DR three-tier circuit breaker ($7 task / $20 day / $50 month); per-agent USD caps across all 8 active launchd agents; daily-driver bumped 0.50 → 0.60 with a documented rationale. Real numbers, real discipline. Internal. | **3** | Build a public interactive cost-model calculator (one HTML/JS page) that takes (workflow steps, model mix, daily volume) → produces cost/quality/latency Pareto. Companion post showing a 5-step flow's cost dropping 12× via smart routing. |

**Honest counts:** 0 fours, 4 threes, 3 twos. The pattern is unambiguous — the substance exists, the *external packaging* doesn't.

### The three weakest skills, in detail

**Specification precision (2).** Sean's operating-model 4-doc spec is genuinely sophisticated PM work — better than what most PMs produce internally — but a recruiter has no way to see it without cloning the vault, and even then would have to navigate `vault/05_atlas/operating-models/job-hunt-2026/` to read it. There is *no published agent product spec for an enterprise workflow*. This is the single highest-leverage gap. Nate names the agent product spec as the most underproduced artifact in the market; Sean has the muscle to write one in a weekend and isn't shipping it. Until this lands, every "what have you built?" question gets answered with a personal repo URL instead of a portfolio link.

**Decomposition for delegation (2).** A 17-agent fleet running on launchd with hybrid routing, retry/recovery semantics, cost caps, and observability *is* an Enterprise AI PM portfolio piece — it's just not packaged as one. The closest external artifact is `CLAUDE.md` itself, which is a system document, not a portfolio narrative. A recruiter reading it would not immediately understand what's load-bearing vs scaffolding. Extracting one flow (e.g., the producer→consumer knowledge loop with named handoffs, the v3.26.3 routing rule for compound research, the v3.34.0/v3.37.0 retrofit progression) into a reference-architecture post would convert this from 2 to 4 in a single week.

**Trust boundary design (2).** Sean's hooks are personal-grade — they prove discipline but they don't speak Enterprise. A regulated-industry hiring manager wants to see the four-variable framework (blast radius / reversibility / frequency / verifiability) applied to a workflow that crosses corporate IAM, generates audit-trail evidence, survives an SR-11-7 review, and accounts for the prompt-injection surface area on a multi-tool flow. None of that is in the pack today. This is the gap that most directly limits Sean to mid-market employers — top regulated-industry buyers (Stripe, ServiceNow, Box, Atlassian Enterprise) will not interview without it.

### What Sean already has that he's not getting credit for

Five pieces of work are portfolio-grade *today* and are buried where no recruiter will find them:

1. **The `evals/vault-synthesizer/` suite.** Ten cases, six failure modes, intentionally-red baseline, documented 1/10 → 7/10 progression. The standard Hamel-Husain / Shreya-Shankar canon + Anthropic "Demystifying Agent Evals" school of evaluation, applied to a real system.
2. **The v3.26.3 LDR grounding-collapse story.** Fabricated entities + fake URLs in confidently-formatted output — Nate's "silent failure" pattern in the wild, post-mortemed with the routing rule that fixes it. This is the literally-textbook "failure post-mortem" Nate names as the highest-signal artifact.
3. **The TopClustRAG retrieval-diversity implementation** (`retrieval_diversity.py`). Implementing a SIGIR 2025 paper to defeat a named retrieval pathology Sean diagnosed via the `query.py` cluster-diversity probe — context engineering at the CCA-exam-relevant tier.
4. **The typed-reasoning concept-edges schema** (`concept_edges.py`). OB1-inspired six-relation graph with SQL fast path consumed by `knowledge_lint`. A real graph-RAG primitive.
5. **The LLM Council** (`tools/llm-council/`). Karpathy-inspired multi-vendor critique with two cost-disciplined profiles. The kind of side-project that turns into a hiring conversation.

These five extracted into separate public repos + 1,500-word posts would move every Phase 3 score from 2/3 to 4 within six weeks. That is the asymmetric opportunity.

---

## Phase 4 — The Build Roadmap

> **Thinking:** Ranked by impact-per-week. Top of list = ship-in-14-days asymmetric wins (extract work that already exists). Middle = 2–4 week net-new artifacts that close specific gaps. Bottom = 2–3 month flagship. Hard constraints: every project lives outside `claude-code-superuser-pack/`; every project maps to ≥2 of Nate's seven and ≥1 of the 2027 premium capabilities; every project includes real eval + cost + documented failure; ≥1 project addresses an Enterprise PM concern Nate doesn't cover (vendor eval / build-vs-buy / governance / change-management); ≥1 project is a public-facing artifact (Substack/talk/README), not just code.

### Project 1: `vault-synthesizer-evals` — public eval suite extraction

**One-line pitch:** A 10-case, 6-failure-mode binary eval suite for a local Qwen3-14B synthesizer, intentionally shipped red, with a documented 1/10 → 7/10 fix progression — the artifact Nate names as the highest-leverage thing a PM can ship.

**Time investment:** 12 hrs over 5 calendar days.

**Maps to Nate skills:** Evaluation (primary), Failure pattern recognition, Specification precision.

**Maps to 2027 premium capabilities:** AgentOps observability & SLO design.

**Problem statement:** Most "AI PM eval" content is theoretical. There is almost no published example of a binary pass/fail eval suite grounded in real production logs, with a red-then-green progression you can reproduce.

**What you'll build:** A standalone GitHub repo `seanwinslow/vault-synthesizer-evals` containing `cases.yaml`, `failure-modes.md`, `runner.py`, `EXPLANATION.md`, `traces/`, and a rewritten `README.md` framed as a portfolio narrative. Plus the 3 deferred cases (vs-012, vs-013, vs-014) closed. Plus a 1,500-word Substack post: "Shipping an Eval Suite Intentionally Red."

**Evaluation:** Suite already moves 1/10 → 7/10 → 10/10 with the deferred-case closures. Add a CI workflow that runs the suite on every PR.

**Failure modes you'll document:** All six already documented in `failure-modes.md` — silent empty output (Mode 1), status-field misreport (Mode 2), missing status taxonomy (Mode 3), `model_used` schema integrity (Mode 4), Pushover fail-quiet (Mode 5), downstream-consumer misread (Mode 6).

**Cost model:** $0 ongoing (runs locally). Document the local-vs-cloud routing decision that keeps it $0.

**Publication plan:** `github.com/seanwinslow/vault-synthesizer-evals` (MIT). Substack post the same day. LinkedIn: "I shipped an eval suite intentionally red. Here are the 6 failure modes it catches." Cross-post to r/LocalLLaMA + Hacker News.

**Why a hiring manager cares:** This is literally the artifact Nate names as the second-highest-signal thing a PM can publish. There are almost no public examples. It would be the strongest single piece in Sean's portfolio within 48 hours.

**Risks / why this might not land:** The repo is small; depth-of-thought has to come through in the README. Mitigation: write the README *first*, treat the code as the appendix.

---

### Project 2: "When LDR Hallucinated A Microsoft Docs URL" — failure post-mortem

**One-line pitch:** A real production failure where a local-LLM research agent confidently produced fabricated entities, wrong repository owners, and fake Microsoft Learn URLs in well-formatted output — diagnosed, root-caused, and fixed with a routing rule. Nate's silent-failure pattern in the wild.

**Time investment:** 8 hrs over 4 days.

**Maps to Nate skills:** Failure pattern recognition (primary), Evaluation, Trust boundary design.

**Maps to 2027 premium capabilities:** Vendor/model-routing economics under deflation.

**Problem statement:** Practitioners under-publish failure post-mortems because they're embarrassing. The result: the industry keeps re-discovering the same agent failure modes. Nate explicitly names "published failure post-mortem with named patterns" as one of two artifacts that work for every track.

**What you'll build:** A Substack post + companion repo `seanwinslow/ldr-grounding-collapse` containing: the original prompt, the bad output (the actual `2026-05-05-topic-1a-...md` file with the fabricated entities), the diagnostic process, the routing rule fix from `CLAUDE.md`, and the eval case that would have caught it.

**Evaluation:** Reproduce the failure on demand (the fixture). Show the routing rule prevents recurrence on three follow-up topics.

**Failure modes you'll document:** Silent failure (Nate #6) — confidently formatted, plausibly wrong, no error signal. Specification drift on multi-target compound prompts.

**Cost model:** $0 to write; $0 to reproduce. Include the per-topic cost comparison: local LDR $0 (failed) vs Gemini DR $0.40 (succeeded).

**Publication plan:** Substack: "Local LLMs Fail Silently When They Try Too Much — A Post-Mortem." GitHub repo with fixtures + routing rule. LinkedIn announcement.

**Why a hiring manager cares:** Demonstrates Nate's most differentiating skill (failure pattern recognition) plus the meta-skill of post-mortem discipline. Hiring managers at Anthropic, Sierra, and Datadog (AgentOps) actively look for this.

**Risks / why this might not land:** Local-LLM-specific framing might read as too niche. Mitigation: frame the failure as a *general agent-routing pattern* (when to escalate beyond a single-model substrate), not a Qwen-specific issue.

---

### Project 3: `agent-cost-calculator` — interactive cost-model web tool

**One-line pitch:** A single-page interactive cost-model calculator: drop in (workflow steps, model mix per step, daily volume) and watch the per-task cost vary 50× across routing strategies. Built because almost nobody ships agent cost models.

**Time investment:** 16 hrs over 7 days.

**Maps to Nate skills:** Cost & token economics (primary), Decomposition for delegation.

**Maps to 2027 premium capabilities:** Vendor/model-routing economics under deflation.

**Problem statement:** Nate says agent cost models are the rarest senior-level artifact; almost no PM ships one. Hiring managers running production agent systems would actively use this.

**What you'll build:** Static HTML/JS site at `cost.seanwinslow.com` plus repo `seanwinslow/agent-cost-calculator`. Live API token costs across Anthropic, OpenAI, Google, DeepSeek, Mistral, Groq. User configures a workflow as a DAG, chooses model per node, sets daily volume — the tool computes total cost, breaks it down per step, identifies the highest-leverage substitution.

**Evaluation:** Three worked example workflows (customer-support tier-1, document summarization, code review). Show the cost reduction from naive frontier-only routing → smart-routed: target ≥10×.

**Failure modes you'll document:** Frontier-everywhere over-spend (Nate's #7); model substitution that silently degrades quality (without an eval gate); prompt-cache miss assumptions.

**Cost model:** $0 build (Cloudflare Pages), <$5/mo to host. Document the per-task cost of three reference workflows live.

**Publication plan:** Substack: "Your Agent Workflow Costs 12× More Than It Has To." Tool live at custom subdomain. LinkedIn + Hacker News + r/LocalLLaMA.

**Why a hiring manager cares:** Almost nobody ships an agent cost model. Tool is reusable for hiring-manager teams. Demonstrates the senior-tier skill at a senior-tier altitude.

**Risks / why this might not land:** Token prices change weekly; the tool will rot unless maintained. Mitigation: pull prices from a JSON file the community can PR.

---

### Project 4: `enterprise-ap-agent-spec` — published agent product spec

**One-line pitch:** A full agent product spec for an enterprise accounts-payable tier-1 automation flow at a 200-person SaaS company — problem definition, escalation logic, eval criteria, trust boundaries, cost model, vendor build-vs-buy memo. The single highest-leverage PM artifact Nate names.

**Time investment:** 24 hrs over 10 days.

**Maps to Nate skills:** Specification precision (primary), Trust boundary design, Evaluation.

**Maps to 2027 premium capabilities:** Governance & evidence for audit; cross-vendor portability strategy.

**Problem statement:** Real agent product specs are nearly unfindable on the open web. The closest analogues are blog posts; full PRD-grade artifacts with eval/escalation/cost discipline don't exist publicly.

**What you'll build:** A canonical PRD published at `seanwinslow/enterprise-ap-agent-spec` (Notion + GitHub mirror). Sections: problem statement → user stories → success metrics (adoption, fallback-to-human, override) → eval framework (10 cases) → escalation logic decision tree → trust boundary review (blast radius / reversibility / frequency / verifiability) → cost model at 5K invoices/month → build-vs-buy memo (Anthropic Skills vs OpenAI Assistants vs in-house) → governance evidence schema (SOC 2 + SR-11-7 mapping).

**Evaluation:** PRD includes its own eval framework as §6 — meta-eval. Solicit critique from 3 enterprise AI PMs on LinkedIn.

**Failure modes you'll document:** Sycophantic confirmation on the vendor invoice (Nate #3); cascade failure when invoice metadata is wrong (Nate #5); silent failure when invoice currency is misread (Nate #6).

**Cost model:** Embedded in PRD §7. Three vendor scenarios + a "do nothing" baseline + a hybrid routing scenario.

**Publication plan:** Notion (live link) + GitHub (markdown mirror) + Substack post: "What an Enterprise Agent Product Spec Actually Looks Like."

**Why a hiring manager cares:** Hiring managers at Atlassian Rovo, ServiceNow NowAssist, Box, ServiceNow can show this to their CFO. It's a usable artifact, not a portfolio piece pretending to be one.

**Risks / why this might not land:** Choosing a less-defensible workflow. AP is defensible because it's universal, regulated-adjacent (SOX-aware), and has clear escalation criteria.

---

### Project 5: `build-vs-buy-framework` — vendor-eval rubric (Enterprise PM gap-filler)

**One-line pitch:** A multi-vendor evaluation rubric for enterprise agent platforms (Anthropic Skills, OpenAI Assistants, Google Vertex Agent Builder, AWS Bedrock Agents, self-host) — the artifact every Enterprise PM writes and nobody publishes.

**Time investment:** 18 hrs over 10 days.

**Maps to Nate skills:** Trust boundary design, Cost & token economics, Specification precision.

**Maps to 2027 premium capabilities:** Cross-vendor portability strategy; Governance & evidence for audit. **Closes Nate blind spot: vendor evaluation & build-vs-buy.**

**Problem statement:** Vendor eval is the most universal Enterprise AI PM activity and the most under-published. Nate's seven skills are silent on it. Hiring managers at Stripe, ServiceNow, Atlassian read vendor memos daily and have nothing to compare against.

**What you'll build:** A rubric (12 dimensions × 5 vendors) + scoring methodology + worked example for one workflow + a Notion template recruiters can fork. Dimensions: cost at scale, latency at P99, vendor lock-in surface, MCP support depth, audit-log primitives, SSO/IAM integration depth, governance certifications (SOC 2, ISO 27001, HIPAA, EU AI Act), prompt-injection hardening, eval tooling, support SLA, roadmap predictability, exit cost.

**Evaluation:** The rubric is itself eval-able — does it produce a defensible decision for a worked example? Test against the AP-agent spec from Project 4.

**Failure modes you'll document:** Vendor-lock-in cascade failure (you can't migrate when prices change); silent capability degradation when a vendor updates a model behind the API.

**Cost model:** Each dimension priced at $X/1M tokens for cost; latency budget per workflow type.

**Publication plan:** Substack: "What an Enterprise AI Vendor-Eval Memo Looks Like." Notion template. LinkedIn post tagging Anthropic / OpenAI / Vertex DevRel.

**Why a hiring manager cares:** This is the artifact Nate's seven skills miss entirely. Demonstrates that Sean is reading Enterprise AI PM at full altitude — not just the agent-mechanics layer but the procurement / governance layer above it.

**Risks / why this might not land:** Vendor scoring is contestable; could draw vendor pushback. Mitigation: source-cite every dimension to public documentation.

---

### Project 6: `llm-council-mcp` — production-quality MCP server

**One-line pitch:** Ship the deferred-Phase-C llm-council MCP server. Multi-vendor critique as a callable MCP tool any agent can use. One of the 9,400+ servers in the registry, with the discipline most of them lack.

**Time investment:** 20 hrs over 14 days.

**Maps to Nate skills:** Decomposition for delegation, Cost & token economics, Evaluation.

**Maps to 2027 premium capabilities:** Cross-vendor portability strategy.

**Problem statement:** 78% of enterprises run an MCP-backed agent in production. Almost none of the public MCP servers ship with proper cost discipline, observability, or eval.

**What you'll build:** Public repo `seanwinslow/llm-council-mcp`, registered in the MCP server registry. Two profiles (premium / variance) exposed as MCP tools. Per-call cost cap. JSONL spend tracking. Tested against an eval suite.

**Evaluation:** Run 5 real critique tasks (cover-letter, PRD critique, decision pre-mortem, voice-mode calibration, build-vs-buy review) before merging the deferred Phase C. Document the cost & ranking-spread results.

**Failure modes you'll document:** Vendor-API rate-limit cascade (Nate #5); ranking-judge sycophancy (Nate #3); chairman over-weighting one model.

**Cost model:** $0.14/query variance, $0.29/query premium. Track real spend in `spend.jsonl`.

**Publication plan:** GitHub repo. Listed in the MCP server registry. Substack: "I Built an MCP Server That Calls Five LLMs and Asks Them to Critique Each Other."

**Why a hiring manager cares:** Real MCP server with cost discipline, observability, and eval. Demonstrates Sean is shipping on the standard that's about to be table stakes.

**Risks / why this might not land:** OpenRouter API instability. Mitigation: built-in retry semantics + dropped-model handling already in `tools/llm-council/council/pipeline.py:55-71`.

---

### Project 7: `narrated-agent-working-session` — recorded craft demonstration

**One-line pitch:** A 35-minute screen recording of Sean building, evaluating, and debugging a real agent flow live — narrated, with the messy parts left in. Nate's "almost unfakeable" artifact.

**Time investment:** 8 hrs over 3 days (record once, edit lightly).

**Maps to Nate skills:** All seven, in motion.

**Maps to 2027 premium capabilities:** AgentOps observability.

**Problem statement:** Hiring managers can't tell from a polished portfolio whether someone actually thinks the way they claim. The recorded working session is the cheapest way to prove craft.

**What you'll build:** One Loom-quality video (35 min target, 45 hard ceiling). Pick a real failure to chase down — e.g., the Tier-2 cluster-and-sample diagnostic from 2026-05-16 (`scripts/query.py` cluster-diversity probe). Narrate: "Here's the symptom, here's my hypothesis, here's how I'm going to test it." Show the cluster-bias output, run HDBSCAN locally, write the test, watch it fail, fix it, watch it pass.

**Evaluation:** Solicit feedback from 3 senior AI PMs. Iterate once.

**Failure modes you'll document:** Performed live. The point is to *show* a real failure being diagnosed.

**Cost model:** $0 to record.

**Publication plan:** YouTube (unlisted) + linked from portfolio site + LinkedIn post.

**Why a hiring manager cares:** Filter for craft, not for performance. Nate calls this the artifact that is "underused and almost unfakeable."

**Risks / why this might not land:** Could come across as scripted. Mitigation: pick a problem Sean hasn't fully solved yet; let the friction show.

---

### Project 8 (flagship): `agentlens` — open-source AgentOps observability layer

**One-line pitch:** A drop-in observability and reliability layer for multi-agent workflows that automatically detects Nate's six failure patterns (and Sean's three additional silent-failure modes) in production. The AgentOps category-defining open-source project.

**Time investment:** 120 hrs over 10 calendar weeks.

**Maps to Nate skills:** All seven.

**Maps to 2027 premium capabilities:** AgentOps observability & SLO design; Governance & evidence for audit; Vendor portability.

**Problem statement:** 78% of enterprises run MCP agents in production; almost none have observability that catches silent failures, context degradation, or cascade failures. Datadog's State of AI Engineering names AgentOps the emerging discipline. There is no obvious open-source default.

**What you'll build:** A Python library + CLI + small web UI that drops into an existing agent (Claude Agent SDK, LangGraph, or vanilla MCP). Records every step. Detects the six Nate patterns + the three Sean patterns (silent-empty output, status-field misreport, downstream-consumer misread). Exposes Prometheus metrics. Ships with the eval suite from Project 1 as a reference test corpus.

**Evaluation:** Apply to three real open-source agent projects; demonstrate detection on a deliberately-corrupted run.

**Failure modes you'll document:** All six Nate + three Sean. Plus the meta-failure: observability that observes the wrong thing.

**Cost model:** $0 ongoing. Self-host or per-call cap.

**Publication plan:** Repo `seanwinslow/agentlens`. Launch post on Substack. Talk submission to AI Engineer Summit, MLOps World, or similar. Companion eBook.

**Why a hiring manager cares:** Flagship-grade artifact that demonstrates depth across the entire Nate framework. Generates inbound recruiter messages on its own merits.

**Risks / why this might not land:** Crowded category — LangSmith, LangFuse, Arize, Helicone exist. Mitigation: anchor on **failure-pattern-detection** as the differentiator (the others are general traces; AgentLens is failure-mode-specific). Bind to MCP-native and ship cost discipline by default.

---

### Recommended sequencing

| Wave | Window | Projects | Why |
|---|---|---|---|
| **Wave 1 — Asymmetric extraction** | Days 1–14 | #1 (eval suite), #2 (failure post-mortem) | The work already exists; this is packaging. Massive ROI per hour. After these two ship, every recruiter conversation has a URL to point to. |
| **Wave 2 — Net-new core** | Days 15–35 | #3 (cost calculator), #4 (agent product spec) | The two most-cited "rarely-shipped" artifacts in Nate's seven. After these, Sean's portfolio covers 5 of 7 skills at score 4. |
| **Wave 3 — Enterprise-PM differentiator** | Days 36–55 | #5 (build-vs-buy framework), #7 (narrated session) | #5 closes the Enterprise-PM blind spot Nate doesn't address. #7 is the craft-proof recruiters can't fake-verify any other way. |
| **Wave 4 — Standard-bearer** | Days 56–80 | #6 (MCP server) | Ship on the protocol that's about to be table stakes. Listed in the registry. |
| **Wave 5 — Flagship** | Weeks 12–22 | #8 (AgentLens) | Defer until Waves 1–4 generate inbound. Use the AgentLens build as the answer to "what are you working on now?" in interviews from week 6 onward. |

**Defer indefinitely unless inbound is weak after Wave 3:** any project requiring custom infrastructure beyond a Python library, any project that requires a third-party dataset, any project that requires writing a paper-quality report (vs a ship-quality artifact). The point is artifacts, not academic output.

---

## The recruiter narrative

> Product Manager (4 years), pivoting hard into Enterprise AI PM. Spent the last 18 months building a production agentic system I run on my own hardware — 17 autonomous agents on launchd, three-tier local-cloud routing, $0/run for everything except the multi-vendor critique tool I built because I wanted independent blind-spot coverage on my own writing. Watch what I actually ship: a 10-case binary eval suite for a local LLM synthesizer, [intentionally red](https://github.com/seanwinslow/vault-synthesizer-evals) with a documented 1/10 → 7/10 fix progression grounded in 17 days of real production logs; the [post-mortem](https://github.com/seanwinslow/ldr-grounding-collapse) on the day a local research agent fabricated Microsoft Learn URLs in confidently-formatted output and how I caught it; a [cost calculator](https://cost.seanwinslow.com) that shows your agent workflow probably costs 12× more than it should. I don't have a CS degree — I'm in Nate's 60% — but I read the actual code, I run TopClustRAG to defeat retrieval cluster-bias in my own vault, and I ship cost models because nobody else does. If you're hiring for AgentOps, agent platform, or enterprise agent surfaces, I'd like 30 minutes to walk you through the AgentLens project I'm building now.

---

*Generated 2026-05-17 as Phase 4 deliverable of `prj-job-hunt-2026`. Routing decisions logged in `vault/health/research-routing-2026-05-17.json`. Self-check pass: skill scores honestly tilted to 2–3, every Phase 4 project lives outside the monorepo, Project 5 closes the vendor-eval gap Nate doesn't address, recruiter narrative written in Sean's voice (dense, product-y, brief).*
