# Sean Winslow

**(917) 886-1251** | [sean.winslow28@gmail.com](mailto:sean.winslow28@gmail.com) | [LinkedIn](https://www.linkedin.com/in/sean-winslow-204390a5) | [GitHub](https://github.com/seanwinslow28) | [seanwinslow.com](https://seanwinslow.com) | Boston, MA

---

## Summary

AI Product Manager and agentic-engineering practitioner who ships production Claude Skills, MCP servers, and autonomous agent fleets — every system gated by human review and eval-driven acceptance criteria. At The Block, shipped 3 production Claude Skills against P&E OKRs, co-authored the Block Pro 2.0 product audit pitched to the incoming CEO, and authored the x402 / MCP agent-economy strategy. Published `@swins/intent-engineering-mcp` to npm and the MCP registry; maintains the open-source 118-skill Code-Brain.

---

## Selected AI Artifacts

### intent-engineering MCP Server

- 3-tool TypeScript MCP server (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) for AI specification authoring — published to npm (`@swins/intent-engineering-mcp@0.1.0`) and the MCP registry (`com.seanwinslow/intent-engineering`, DNS-verified namespace).
- Shipped 2026-05-12, 13 days ahead of plan. Demoable in Claude Desktop with a single config change.
- Evals-first methodology: the `audit_intent_spec` tool *is* the eval — it scores a spec against the framework's dimensions before the spec ships to a coding agent, operationalizing the "evals are the new PRDs" thesis as a portable MCP server.

### Code-Brain — Open-Source Agentic Engineering Toolkit

- Open-source toolkit for Claude Code: 118 skills, 13 subagents, 14 hooks, 17 autonomous Claude Agent SDK agents (8 in production on local-first launchd schedules).
- Used daily in production for PM workflows, vault automation, and content generation across crypto, creative, and personal-systems domains — agents own decomposition; human owns judgment.
- Architecture writeups published for two production subsystems: typed reasoning edges (cross-domain contradiction detection) and an eval-gated knowledge loop.

### anima — Human + Agent-Fleet 2D Animation Pipeline

- 10-phase production pipeline pairing a human director with named agent personas (planner, character designer, vision critic) — agents propose, human approves; nothing burns compute until a cost-estimated plan passes a human gate.
- Three-tier critic stack: deterministic rule gates ($0, instant), vision critics that propose prompt diffs rather than pass/fail verdicts, and multi-CLI variance review at phase transitions ($0 incremental on existing subscriptions).
- Content-addressed DAG runner with draft→pro cost escalation and audited mutation contracts on locked acceptance criteria. First reference implementation (Pencil Test) shipped Act 1 to a public portfolio.

### Agentic Financial-Research Fleet

- Multi-agent orchestration (queue → router → 3 retrieval agents → local-LLM synthesis → daily morning brief) on a $0/month self-hosted stack (Ollama, SearXNG), with Gemini Deep Research as cloud fallback for compound topics.

---

## Work Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Shipped 3 production Claude Skills (ETF page creation, stakeholder updates, Jira automation), each scoped with a human-in-the-loop review gate — direct delivery of P&E Q2 OKR KR3, saving an estimated [X hrs/week] of manual work across the team.
- Built an end-to-end RevOps automation pipeline (11 Zapier workflows, 10 product-specific intake forms, central Tables database) turning a Salesforce "Closed Won" trigger into auto-created Jira tickets, personalized client intake emails, and routed Slack notifications — eliminating 7 manual handoff steps (~[X hrs] per deal).
- Co-authored the Block Pro 2.0 product audit pitched to the incoming CEO — benchmarked 9 enterprise data/research platforms, ran 3 stakeholder interviews, and led an 11-risk structured pre-mortem that surfaced engineering-capacity and renewal-cliff blockers pre-proposal.
- Drove 0-to-1 product discovery and delivery of The Block's first sponsored-microcourse B2B revenue vertical (Polymarket × Campus): authored the PRD v1→v3, shipped the 5-component build, and productized the partnership into a repeatable go-to-market motion for the revenue team [worth ~$Xk].
- Authored the internal x402 / A2A / MCP agent-economy strategy memo mapping 6 monetization patterns (pay-per-request data access, agent-readable feeds, education micropayments, content-crawl licensing) into product questions for Block Pro exploration.
- Automated AI-assisted image, video, and voiceover generation for the Campus 201 enterprise course launch (Nano Banana Pro, Veo 3.1 / Kling 3.0, ElevenLabs), with human creative review before final delivery.
- Onboarded fellow PMs on Claude Code and agentic-engineering workflows, built the P&E Claude Skills library, and led daily P&E standups driving cross-functional execution across engineering, design, and revenue operations.

### New York Life Insurance — Multimedia & Design | New York, NY

**Team Lead, AI Workflow Integration** | *2021 – November 2025*
**Product Operations Lead** | *March 2015 – November 2025*

- Led an 8-person cross-functional team integrating prompt-engineered metadata pipelines (ChatGPT, Claude, Gemini) into enterprise DAM workflows — a 60% lift in asset discoverability across 100+ users and 50+ locations. Precursor to the agentic-engineering practice now shipping in open source.
- Led enterprise rollout of a SaaS DAM platform across 50+ locations, translating stakeholder requirements into actionable technical documentation in the Atlassian suite.
- Increased media asset productivity 40% through onboarding programs and custom training for 100+ users.

---

## Education

**College of Staten Island** — Staten Island, NY *Bachelor of Arts in Media Studies* | 2010 – 2014

---

## Skills

**AI / Agentic Engineering:** Claude Code, Claude Agent SDK, Claude Skills authoring, MCP (Model Context Protocol), prompt engineering, agent orchestration, RAG / local-LLM workflows (Ollama, Qwen3), evals (golden-set design, LLM-as-judge rubrics, regression suites), human-in-the-loop deployment patterns, AI media generation (Nano Banana 2, Veo 3.1, ElevenLabs, Seedance 2.0)

**Product Craft:** product strategy, product discovery, PRD authoring, user research, competitive analysis, A/B testing & experimentation, GA4 analytics, roadmap planning, OKR ownership & north-star metrics, go-to-market (GTM), stakeholder management, agile / scrum, cross-functional facilitation, build-in-public

**Tools & Platforms:** Cursor, GitHub, Python, SQLite, Jira, Confluence, Slack, Figma, Notion, Adobe Creative Suite, Zapier, Anthropic API, NotebookLM

**Domains:** Crypto / digital assets, B2B SaaS, EdTech / online learning, AI-assisted media production, animation
