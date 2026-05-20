# Sean Winslow

**(917) 886-1251** | [LinkedIn](https://www.linkedin.com/in/sean-winslow-204390a5) | [sean.winslow28@gmail.com](mailto:sean.winslow28@gmail.com) | [seanwinslow.com/transactions](https://seanwinslow.com/transactions) | Boston, MA

---

## Summary

Technical Product Manager who reads code, writes specs engineers respect, and builds the tools to back them up. At The Block, built an 11-Zap AdOps RevOps automation pipeline, 3 production Claude Skills, and the 10-week P&E Confluence rearchitecture — plus the Polymarket × Campus B2B integration end-to-end (PRD-to-deploy). Active builder on the Claude Agent SDK; published the `@swins/intent-engineering-mcp` MCP server to npm and the MCP registry in May 2026.

---

## Selected AI Artifacts

### intent-engineering MCP Server

- 3-tool TypeScript MCP server (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) for AI specification authoring — published to npm (`@swins/intent-engineering-mcp@0.1.0`) and the MCP registry (`com.seanwinslow/intent-engineering`, DNS-verified namespace).
- Shipped 2026-05-12, 13 days ahead of plan. Demoable in Claude Desktop with a single config change.
- Built on an evals-first methodology: the `audit_intent_spec` tool *is* the eval — it scores a spec against the framework's dimensions and tells the author what's missing before the spec ships to a coding agent. Operationalizes the "evals are the new PRDs" thesis as a portable MCP server.

### Code-Brain — Open-Source Toolkit

- Open-source agentic engineering toolkit for Claude Code: 118 skills, 13 subagents, 14 hooks, 17 autonomous Claude Agent SDK agents (8 in production on local-first launchd schedules).
- Used in production for daily PM workflows, vault automation, and content generation across crypto, creative, and personal-systems domains.
- Demonstrates Karpathy-style "agentic engineering practitioner" architecture — agents own decomposition; human owns judgment.
- Architecture writeups for two production subsystems: Phase D Typed Reasoning Edges (SQLite-backed cross-domain contradiction detection — a lightweight judge layer surfacing factual conflicts across 6 relation types) and Phase 6 Knowledge Loop (SessionEnd flush → nightly synth → weekly lint → SessionStart re-inject, with eval-gated promotion).

### Agentic Financial-Research Fleet

- Multi-agent orchestration: queue file → router → 3 retrieval agents → local-LLM synthesis → daily morning brief.
- Runs on a $0/month local-LLM stack (Ollama, SearXNG, LDR) with Gemini Deep Research as cloud fallback for compound topics.
- Design exemplar of a "sensors and actuators" architecture on a local stack — verifiable, durable, fully self-hosted.

---

## Work Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Built an end-to-end RevOps automation pipeline — 11 Zapier workflows + 10 product-specific intake forms + central Tables database — turning a Salesforce "Closed Won" trigger into auto-created parent/child Jira tickets, personalized client intake emails, and routed Slack notifications, eliminating 7 manual handoff steps per deal.
- Authored the 10-week P&E Department 2.0 execution plan consolidating 7 competing team-doc hubs, ~25 orphaned Developer Sync pages, and 5+ overlapping onboarding pages into a per-product Confluence architecture with a centralized Templates Library — framed as operational-maturity proof for the incoming CEO and direct delivery against P&E Q2 OKR Objective 5 (Operational Excellence & AI-Assisted Efficiency).
- Built the .co homepage redesign competitive visual audit — 50+ site benchmark across 8 categories (crypto-native, premium news, financial/data, modular newsletter formats, editorial design, bento layouts, crypto data, wildcards) with a structured "one to steal / one to never do" capture methodology — feeding blue-sky design exploration with the design team.
- Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — each skill scoped with a human-in-the-loop review gate before publish, send, or ticket creation — direct delivery against the P&E Q2 Objective 5 KR3 ("Ship 1–3 Claude Skills").
- Drove 0-to-1 product creation: authored the PRD (v1→v3) and shipped The Block's first sponsored-microcourse B2B revenue vertical (Polymarket × Campus) — a 5-component build (homepage module, Learn page hub, in-article recirculation, embedded course player, reporting requirements) connecting The Block's editorial audience to Campus education content, plus a sales one-pager template that productized the partnership for repeatable revenue-team sale.
- Co-authored the Block Pro 2.0 product audit + competitive analysis (9 enterprise data/research platforms benchmarked) and conducted 3 internal stakeholder interviews (sales, research, head of data) to scope the pitch deck delivered to the incoming CEO — including a structured pre-mortem (11 risks across launch-blocking, fast-follow, and track tiers) that surfaced engineering-capacity and renewal-cliff dependencies before the proposal landed.
- Automated AI-assisted image, video, and voiceover generation for the Campus 201 enterprise course launch using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs APIs, with human creative review before final asset delivery.

### New York Life Insurance — Multimedia And Design | New York, NY

**Product Operations Lead** | *March 2015 – November 2025*

- Led enterprise rollout of a SaaS DAM platform across 50+ locations, leading requirements gathering and translating business needs into actionable technical documentation within the Atlassian suite.
- Increased media asset productivity by 40% through onboarding programs and custom training for 100+ users.
- Boosted asset discoverability by 60% using prompt-engineered metadata via ChatGPT, Claude, and Gemini.

---

## Leadership Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Designed and ran an 11-risk structured pre-mortem for the Block Pro 2.0 proposal — tiering risks across launch-blocking, fast-follow, and track categories, surfacing engineering-capacity and renewal-cliff dependencies before the pitch landed with the incoming CEO. Methodology framed against Gary Klein's pre-mortem canon; reusable as a P&E governance artifact.
- Authored internal x402 / A2A / MCP strategy memo mapping 6 potential agent-economy monetization patterns — pay-per-request data access, agent-readable feeds, education micropayments, content-crawl licensing — into product questions for future Block Pro exploration.
- Created the PRD-to-Prototype Lab project — an in-product reference giving designers and engineers shared access to user flows, PRD details, and the Block design system.
- Onboarded fellow Product Managers on Claude Code and agentic-engineering workflows; built a P&E Claude Skills library covering Jira automation, ETF page creation, stakeholder updates, and design system enforcement.
- Led daily P&E standups and drove cross-functional execution across engineering, design, and revenue operations in Slack, Confluence, Jira, and Figma.

### New York Life Insurance — Multimedia And Design | New York, NY

**Team Lead, AI Workflow Integration** | *2021 – November 2025*

- Led an 8-person cross-functional team integrating prompt-engineered metadata pipelines (ChatGPT, Claude, Gemini) into enterprise DAM workflows — driving a 60% lift in asset discoverability and training 100+ users across 50+ locations. Precursor work to the agentic-engineering practice now shipping in open source.

---

## Education & Certification

**College of Staten Island** — Staten Island, NY *Bachelor of Arts in Media Studies* | 2010 – 2014

---

## Skills

**AI / Agentic Engineering:** Claude Code, Claude Agent SDK, Claude Skills authoring, MCP (Model Context Protocol), MCP namespace governance, prompt engineering, agent orchestration, RAG / local-LLM workflows (Ollama, SearXNG, Qwen3, gemma4), evals (golden-set design, LLM-as-judge rubrics, regression suites), human-in-the-loop deployment patterns, AI media generation (Nano Banana 2, Veo 3.1, Kling 3.0, ElevenLabs, Seedance 2.0)

**Tools & Platforms:** Cursor, GitHub, Python, SQLite, Jira, Confluence, Slack, Figma, Notion, Adobe Creative Suite, Zapier, Anthropic API, NotebookLM

**Product Craft:** PRD authoring, technical spec writing, user research, competitive analysis, A/B testing, GA4 analytics, roadmap planning, OKR ownership, agile / scrum, cross-functional facilitation

**Domains:** Crypto / digital assets, B2B SaaS, EdTech / online learning, AI-assisted media production, animation
