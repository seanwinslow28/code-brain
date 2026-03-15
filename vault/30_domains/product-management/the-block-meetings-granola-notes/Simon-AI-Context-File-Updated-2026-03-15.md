# Simon AI — Updated Context File

**Last updated:** 2026-03-15
**Updated by:** Sean Winslow (with Claude analysis of meeting notes from Feb–Mar 2026)

---

## Changes from Previous Version

> **What changed and why:** This update incorporates information discovered in daily standup transcripts, 1:1 meetings, design syncs, and ticket cleanup sessions from February–March 2026. Several items from the original context file are now deprecated, and significant new developments (Simon AI API, MCP integration, standalone app) have been added.

### New additions
- Simon AI API (for internal automation workflows)
- Standalone Simon AI app concept
- Simon AI shipped to production with MCP workflow support (Mar 11, 2026)
- Open-source LLM investigation (Qwen Coder 3.5 etc.)
- iOS AI digest summaries (related AI capability)

### Deprecated / flagged
- Connect — dead on arrival, no subscriber usage (confirmed Mar 9, 2026 by Ed Rupkus)
- Zulip — backend for Connect, inactive for ~1 year
- PRO-2213 (Auto-Open Tooltip) — CLOSED WONT-FIX
- PRO-2304 (Simon AI Academy Integration) — CLOSED WONT-FIX

---

## Context Block

`<context>`

`COMPANY: The Block — a crypto media, research, and data company (https://www.theblock.co / https://www.theblock.pro).`

`PRODUCT: Simon AI — a retrieval-augmented generation (RAG) chatbot originally built for The Block Pro subscribers, now also exposed as an internal API and available for MCP-based workflows. It answers user questions by retrieving and synthesizing information from The Block's proprietary library of:`

`- News articles`

`- Research reports`

`- Learn/education content`

`- Token and index context`

`and returns precise, insight-rich responses grounded in that content.`

`CURRENT LLM: OpenAI ChatGPT API — exact deployed model version not documented ("model version unknown").`

`OPEN-SOURCE LLM INVESTIGATION: As of Feb 26, 2026, the team is actively investigating open-source models (e.g., Qwen Coder 3.5) as potential cost-saving alternatives to OpenAI. Sean Winslow raised this in standup; Mike Price is open to exploring. No decision made yet — this is an active area of research.`

`ESTIMATED MONTHLY QUERY VOLUME: Unknown — assume moderate enterprise SaaS usage with periodic spikes around major market events and product launches.`

`ESTIMATED MONTHLY API SPEND: Unknown — not documented in Confluence or Jira.`

`VECTOR DATABASE: Weaviate.`

`- Confirmed in internal documentation describing "Our Steps to Implement SimonAI," which specifies that all articles are added to a Weaviate vector database with embeddings computed via ChatGPT.`

`- See: "Prompt Engineering for AI Models Best Practices"`

`https://theblockcrypto.atlassian.net/wiki/spaces/Training/pages/729710596/Prompt+Engineering+for+AI+Models+Best+Practices`

`EMBEDDING MODEL: OpenAI embeddings via ChatGPT API — specific embedding model name/version not documented ("embedding model unknown").`

`RETRIEVAL & GENERATION PIPELINE (from internal docs):`

`1. **Data Integration**`

`- All relevant content (news, research, learn pages, token/index context) is ingested into Weaviate.`

`- Vector embeddings for each document are computed using ChatGPT / OpenAI embeddings and stored in Weaviate.`

`2. **Retrieving Relevant Documents**`

`- When a user asks a question via Simon AI, the system queries Weaviate to retrieve the most relevant documents based on vector similarity.`

`3. **Querying ChatGPT**`

`- The retrieved documents are passed as context to the ChatGPT API alongside the user's query.`

`4. **Generating the Response**`

`- ChatGPT uses the provided context to generate an answer grounded in The Block's content (e.g., for "What is Bitcoin halving?", it fetches relevant articles and synthesizes an explanation from those).`

`5. **Returning the Response**`

`- The generated answer is returned to the user via the active surface area (Pro chat, Simon AI API, or MCP workflow).`

`DATA SOURCES / SCOPE OF KNOWLEDGE:`

`- The Block's proprietary content library:`

`- News`

`- Research`

`- Learn pages`

`- Token and index context`

`- Simon AI is **not** directly "trained on" this data; instead, it has **full access to the library at query time** as retrieval context.`

`- It is intended to have immediate access to the most recent published content so answers reflect current information in The Block's systems.`

`USER-FACING SURFACE AREAS:`

`- **The Block Pro (Active)**`

`- Simon AI is surfaced directly within Pro as an in-app chat experience.`

`- Backend uses OpenAI plus other internal systems to provide an integrated experience.`

`- **Simon AI API (Active — New as of Feb 2026)**`

`- Mike Price built and shipped a dedicated Simon AI API.`

`- Primary consumer: Jordan and his team for automation workflows.`

`- API hooks into the same Weaviate + OpenAI pipeline as the Pro chat.`

`- Source: Feb 26 standup — Mike confirmed shipping "the last bit of internals for Simon API" for Jordan's team. Mar 3 standup — Mike confirmed "shipping Simon AI API."`

`- **MCP Workflow Integration (Active — New as of Mar 11, 2026)**`

`- Simon AI shipped to production and is now available for MCP (Model Context Protocol) workflows.`

`- This represents a significant evolution — Simon AI can now be called as a tool within MCP-based agent pipelines.`

`- Source: Mar 11 standup — Mike reported "Simon AI shipped to production — now available for MCP workflows."`

`- **Standalone Simon AI App (In Development — New as of Feb 2026)**`

`- Mike Price mentioned building a "standalone Simon AI app for potential integration."`

`- Details are limited; this may be a decoupled frontend or a separate product surface.`

`- Source: Feb 10 standup.`

`- **iOS AI Digest Summaries (Active — Related Capability)**`

`- AI-powered summaries are now working in the iOS app digest (as of Feb 26, 2026).`

`- While not Simon AI directly, this uses the broader AI stack (likely same OpenAI pipeline) for content summarization in the mobile app.`

`- Source: Feb 26 standup — Mike confirmed AI summaries working in iOS digest.`

`- ~~**Connect / Zulip (DEPRECATED)**~~`

`- Connect was a Pro subscriber feature allowing clients to chat directly with The Block's research team, with Simon AI embedded in the experience.`

`- Backend was powered by Zulip (an open-source chat platform).`

`- **Status as of Mar 9, 2026:** Ed Rupkus confirmed Connect was "dead on arrival — nobody seemed to really interact with it" and "none of the subscribers use this." The last Zulip message was from nearly a year ago.`

`- Connect and Zulip should be considered inactive/deprecated for planning purposes.`

`- Historical reference: "How to use Zulip and Interact with Simon AI"`

`https://theblockcrypto.atlassian.net/wiki/spaces/PE/pages/723550235/How+to+use+Zulip+and+Interact+with+Simon+AI`

`BACKEND & INFRASTRUCTURE:`

`- **Services**`

`- simon-ai is deployed as its own service in the ECS stack alongside pro-api.`

`- ECS services created by Cesar Paz (confirmed Feb 17, 2026 standup).`

`- See: "Create services in Terraform (pro-api and simon-ai) in our ECS stack"`

`https://theblockcrypto.atlassian.net/browse/PRO-4484`

`- **Typical stack components** (based on internal infra/Jira references):`

`- Application stack: Node.js services (e.g., pro-api) with a service dedicated to Simon AI running on AWS ECS.`

`- Data warehouse: AWS Redshift (for broader data, separate from Weaviate which handles vector search).`

`- Object storage: AWS S3.`

`- Networking/edge: Cloudflare used in front of web properties.`

`PRIVACY, LICENSING & DATA HANDLING (from prompt engineering doc):`

`- **Licensing & Privacy**`

`- For licensing and privacy questions, users are directed to The Block's privacy policy.`

`- **Implementation Method**`

`- Simon AI is implemented directly in the Pro product, with OpenAI integrated on the backend.`

`- Additionally exposed via a standalone API and MCP integration (as of early 2026).`

`- **Training vs. Context**`

`- Simon AI is not trained directly on The Block's proprietary content; instead, it uses that content as retrieval context at inference time.`

`- **Real-time / Freshness**`

`- Simon AI is designed to have immediate access to newly published content so users receive up-to-date information.`

`- **Support & Feedback**`

`- Feedback option exists within the chat window.`

`- Users can also reach out to their dedicated account manager for issues with AI responses.`

`KEY JIRA TICKETS — ACTIVE:`

`- **PRO-4484** — Create services in Terraform (pro-api and simon-ai) in our ECS stack — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-4484`

`- **PRO-2481** — Allow toggle of Connect/SimonAI at org level — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2481`

`- **PRO-2149** — Account Management / Connect design & implementation — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2149`

`- **PRO-2188** — Update Simon AI Notice (legal/consent copy) — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2188`

`- **PRO-2111** — .Pro: Simon AI chat scroll issues — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2111`

`- **PRO-2120** — .Pro: Simon AI demo issues on Marketing site — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2120`

`- **PRO-2492** — QA Connect — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2492`

`- **PRO-2537** — QA Connect - Production Environment — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2537`

`- **PRO-2560** — .Pro: Simon-AI message indicator not resetting — DONE`

`https://theblockcrypto.atlassian.net/browse/PRO-2560`

`KEY JIRA TICKETS — CLOSED / WONT-FIX (do not reference as active work):`

`- **PRO-2213** — [Implementation] Auto-Open and Tooltip for Simon AI on Pro Homepage — CLOSED WONT-FIX`

`https://theblockcrypto.atlassian.net/browse/PRO-2213`

`- **PRO-2304** — Simon AI Integration (Academy integration) — CLOSED WONT-FIX`

`https://theblockcrypto.atlassian.net/browse/PRO-2304`

`MY ROLE: Associate Product Manager. I am building this proposal to present to the engineering lead. I am not the final decision-maker — my goal is to present options with enough technical rigor and clear business rationale that engineering can evaluate feasibility and tradeoffs.`

`</context>`

---

## What's Confirmed vs. Inferred

### Grounded in internal docs (Confluence/Jira):
- **Weaviate as the vector DB** and the 5-step RAG pipeline — from Prompt Engineering for AI Models Best Practices
- Simon AI's positioning, data sources, and Pro integration — same doc
- The Zulip interface — from How to use Zulip and Interact with Simon AI
- simon-ai as its own ECS service — from PRO-4484
- Org-level toggles, notices, and UX behavior — from linked Jira tickets

### Grounded in meeting notes (Feb–Mar 2026):
- **Simon AI API** for Jordan's team automation workflows — Feb 26 & Mar 3 standups (Mike Price)
- **MCP workflow integration** shipped to production — Mar 11 standup (Mike Price)
- **Standalone Simon AI app** in development — Feb 10 standup (Mike Price)
- **iOS AI digest summaries** working — Feb 26 standup (Mike Price)
- **Connect/Zulip deprecated** — Mar 9 ticket cleanup (Ed Rupkus)
- **Open-source LLM investigation** raised — Feb 26 standup (Sean Winslow)
- **ECS service creation** by Cesar Paz — Feb 17 standup

### Best-effort / not explicitly documented:
- Exact **ChatGPT model name** (left as "model version unknown")
- Exact **embedding model** (left as "unknown")
- Exact **query volume** and **API spend** (no docs surfaced)
- Some generic stack notes (Node.js on ECS, Cloudflare, etc.) are consistent with infra Jira but not spelled out line-by-line for Simon AI specifically

---

## Meeting Notes Sources

| Date | Meeting | Key Simon AI Info |
|------|---------|-------------------|
| 2026-02-10 | Unified Daily Standup | Mike: building standalone Simon AI app |
| 2026-02-12 | Unified Daily Standup | Cesar: OKRs include AI agents via Cloud |
| 2026-02-17 | Unified Daily Standup | Cesar: created ECS services for pro-api and simon-ai |
| 2026-02-26 | Unified Daily Standup | Mike: Simon AI API for Jordan's team; Sean: open-source LLM investigation; Mike: iOS AI digest summaries working |
| 2026-03-03 | Unified Daily Standup | Mike: shipping Simon AI API |
| 2026-03-05 | Unified Daily Standup | Simon AI API progress update |
| 2026-03-09 | Ticket Cleanup (Ed + Sean) | Ed confirms Connect/Zulip is dead on arrival, no subscriber usage |
| 2026-03-11 | Unified Daily Standup | Mike: Simon AI shipped to production, available for MCP workflows |
