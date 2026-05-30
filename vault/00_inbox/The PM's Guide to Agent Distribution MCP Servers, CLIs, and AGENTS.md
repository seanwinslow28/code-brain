---
title: "The PM's Guide to Agent Distribution: MCP Servers, CLIs, and AGENTS.md"
source: "https://www.news.aakashg.com/p/master-ai-agent-distribution-channel"
author:
  - "[[Aakash Gupta]]"
published: 2026-03-06
created: 2026-05-30
description: "How to build MCP servers, CLIs, and AGENTS.md so AI agents can discover and use your product. Audit template, PRD, 10 production teardowns, Claude Code sprint."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
### Stripe, Cloudflare, Linear, and 7 others already shipped. Audit template, PRD, and Claude Code sprint included.

**Your product’s next million users won’t have eyes.**

They won’t visit your website, sit through your onboarding, or read your changelog. They’ll be AI agents, autonomous software that discovers, evaluates, and integrates tools *programmatically*.

Quote me on this:

> **If your product cannot be parsed, authenticated, and executed by an agent, you are invisible in the fastest-growing software channel.**

It sounds futuristic. It isn’t. Stripe, Cloudflare, Shopify, GitHub, Asana, Zapier, and others have already shipped agent-facing surfaces.

Andrej Karpathy put it bluntly last week: “It’s 2026. Build. For. Agents.”

![](https://substackcdn.com/image/fetch/$s_!8Oae!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f4b4a0e-a972-4f72-be9f-d352419057ed_1280x1600.png)

The post named something product teams have been slow to act on: **the distribution channel is shifting from human interfaces to agent interfaces**.

---

## Today’s Post

*This is the most practical guide I could write on how to own this shift as a PM:*

1. The 5 Distribution Channels - and Why #5 Changes Everything
2. The Agent-Accessible Product Stack
3. The PM’s Role in Agent Distribution
4. The Strategy Meeting, Pitch + PRD
5. Analyzing 10 the top MCP Servers
6. Building It - Claude Code Sprint
7. Where Teams Go Wrong

*Sections 1 and 2 are free. Sections 3-7 are for paid subscribers.*

---

## 1\. The 5 Distribution Channels - and Why #5 Changes Everything

Every generation of software has a dominant distribution channel. Every time the channel shifts, the companies that build for the new interface first win the decade.

![](https://substackcdn.com/image/fetch/$s_!rf2I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20781e53-b33c-4ac2-8ead-0112afaf2a68_1080x1080.png)

**Channel 1: Retail (1980s-90s)**

Software came in boxes. You drove to CompUSA. Distribution meant shelf space. Microsoft won by getting Windows pre-installed on PCs.

**Channel 2: Web (2000s)**

Google changed everything. Distribution shifted to search rankings, landing pages, and self-serve signups. Salesforce killed on-premise with a URL. I wrote about how this shaped [activation](https://www.news.aakashg.com/p/ultimate-guide-activation) and [onboarding](https://www.news.aakashg.com/p/the-ultimate-guide-to-onboarding) as core growth levers, and why [PLG](https://www.news.aakashg.com/p/plg-in-2026) became the dominant go-to-market.

**Channel 3: Mobile (2010s)**

The App Store created a new discovery surface. Companies that designed for small screens from day one (Instagram, Uber, WhatsApp) ate companies that tried to port desktop. I covered how [growth loops](https://www.news.aakashg.com/p/ultimate-guide-growth-loops) compound differently on mobile.

**Channel 4: AI Discovery (2020s)**

LLMs started answering questions instead of linking to websites. If ChatGPT describes your competitor instead of you, you lose the click entirely. I wrote about this shift in my [AEO/GEO guide](https://www.news.aakashg.com/p/guide-aeo-geo), the new discipline of making your product visible to AI answer engines.

**Channel 5: Agent Distribution (Now)**

This is the one Karpathy is talking about. Agents don’t discover products through search results or app stores. *They discover them through CLIs, MCP servers, and machine-readable documentation.* They don’t onboard. They don’t browse. They connect, authenticate, execute, and move on.

Each channel shift followed the same pattern: the companies that built for the new interface first captured outsized market share. The ones that tried to retrofit lost ground they never recovered.

This shift **appears to be happening faster than most interface transitions**. Major platforms, model providers, and infrastructure vendors are aligning *unusually quickly*.

#### The Numbers

MCP, the [Model Context Protocol](https://www.youtube.com/watch?v=a9wO6GSAoGk), went from zero to [97 million monthly SDK downloads](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) across Python and TypeScript in its first year.

[10,000+ active MCP servers](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation). OpenAI, Google DeepMind, Microsoft, and Cloudflare all adopted it. In December 2025, Anthropic donated MCP to the Linux Foundation’s [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) because the standard had already emerged as the early leader. OpenAI and Block joined as co-founders. Google, Microsoft, AWS, Cloudflare, and Bloomberg as supporting members.

Gartner [projects](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025) that 40% of enterprise applications will embed task-specific AI agents by end of 2026, up from less than 5% in 2025. That’s one of the steepest adoption curves in enterprise history.

**So the channel is real.** The adoption is real. The question for PMs is: *what do you actually build?*

---

## 2\. The Agent-Accessible Product Stack - What to Build First

Your API is always the foundation. MCP servers call it under the hood. CLIs call it under the hood. If your API is a mess, everything above it will be too. If your auth is broken, neither MCP nor a CLI will fix it.

On top of your API, you build three surfaces. Most companies end up with all three. They layer, they don’t replace each other, and the order you build them matters.

![](https://substackcdn.com/image/fetch/$s_!Aj7k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbff16ddc-e7f5-40dd-a79f-e55a3e929344_1080x1080.png)

#### Layer 1: Documentation

[AGENTS.md](https://agents.md/) is the emerging standard for telling agents how to work with your codebase and product. It emerged from collaborative efforts across OpenAI Codex, Google’s Jules, Cursor, GitHub Copilot, and Amp.

Think of it as a README, but written for machines instead of humans. OpenAI donated it to the [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) alongside MCP.

GitHub analyzed 2,500+ AGENTS.md files and found a clear split between ones that work and ones that don’t. The effective ones put executable commands early, show code instead of prose, set clear boundaries on what agents should never do, and specify exact framework versions. *[60,000+ projects](https://agents.md/) have already adopted the format.* OpenAI’s own repo has 88 AGENTS.md files, one per package.

The companion to AGENTS.md is an **OpenAPI spec**. If your [API docs](https://www.news.aakashg.com/p/how-to-build-ai-products) are scattered across Notion pages and README files, agents can’t parse them. An OpenAPI 3.0 spec is a machine-readable contract: every endpoint, every parameter type, every error code in one structured file. Tools like Speakeasy and Gravitee can auto-convert an OpenAPI spec into an MCP server. No spec, no conversion.

Vercel is pushing this further with **Agent Skills**: packaged instruction folders (SKILL.md files) that give agents specialized expertise. Stripe, Cloudflare, Supabase, Sentry, Expo, and Hugging Face all publish official [agent skills](https://www.news.aakashg.com/p/steal-6-of-my-claude-skills). They work across Claude Code, GitHub Copilot, Cursor, Gemini CLI, and others. It’s another documentation surface that’s quietly becoming a distribution channel.

That’s where every team should start.

#### Layer 2: CLI

Karpathy’s point about CLIs being “legacy” technology is precise. Legacy means battle-tested, standardized, universally parseable.

The entire Unix philosophy was *accidentally designed for [AI agents](https://www.news.aakashg.com/p/practical-ai-agents-pms)* decades before they existed: small composable commands, JSON output piped between tools, environment variable auth, structured exit codes.

A **quick clarification** on how CLIs relate to APIs, since this trips up a lot of PMs:

- Your API is the **engine**. It’s the raw programmatic interface.
- A CLI is a **structured wrapper** around your API that makes it composable: piping output to grep, chaining commands with jq, using environment variable auth.
- An MCP server is **another wrapper**, this one designed specifically for AI clients to discover and call tools through a standard protocol.

They’re layers, not alternatives, and each adds a new surface for different types of consumers.

Stripe’s CLI lets you pipe JSON responses to jq, chain subscription queries with customer lookups, export data in CSV. That existed years before MCP.

Now agents use it natively. Same story with AWS CLI, Terraform, Docker, GitHub’s gh, and Vercel’s CLI.

These companies built CLIs for developer productivity **and got agent-accessible infrastructure for free**.

#### Layer 3: MCP Server

This is where the biggest investment happens, but it’s also where the quality gap between companies is widest. An MCP server exposes your product’s capabilities as tools that Claude, ChatGPT, Cursor, Copilot, and thousands of other clients understand through a single [standard protocol](https://www.news.aakashg.com/p/context-engineering).

For many developer and B2B tools, an MCP server is quickly becoming *table stakes*. Having a *good* one is the **competitive advantage**.

**What Makes a Good MCP Server**

The difference between good and bad comes down to a few things most teams get wrong:

1. **Tool descriptions.** This is where most MCP servers fail. If your tool says “manages tasks,” an agent doesn’t know whether it creates, reads, updates, or deletes. Research on [MCP tool selection](https://www.speakeasy.com/mcp) shows agents start failing at 30+ tools when descriptions overlap, and virtually guarantee wrong picks at 100+. The Speakeasy team found that reducing Playwright’s MCP server from 26 tools to 8 dramatically improved agent accuracy. Design tools around outcomes, not endpoints. One `track_order(email)` that calls three APIs internally beats three separate tools the agent has to chain.
2. **Auth without a browser.** OAuth 2.0 device flows work: show a URL and code in the terminal, user approves in browser, agent gets the token. API keys for server-to-server. *No browser-dependent auth in the critical path.*
3. **Structured errors.** “API\_TOKEN is invalid, reconfigure the MCP server” is actionable. “Access denied” is not.
4. **Idempotent endpoints.** Agents retry. They will call the same endpoint multiple times on a timeout. Handle duplicates gracefully.
5. **Clear rate limits.** Return 429 status codes with Retry-After headers. Agents that hit opaque limits will either crash or hammer you exponentially.

You want to **push your team** to get to this level.

---

> ***Everything below is for paid subscribers.***
> 
> *The free section tells you **what** this channel is. The paid section gives you the part most teams will actually need help with:*
> 
> - ***The 5-question audit** to score agent readiness*
> - ***The stakeholder pitch** to win leadership buy-in*
> - ***The PRD template** for your first agent-access initiative*
> - ***The Claude Code sprint** from zero to working implementation*
> - ***10 production teardowns** to copy the right patterns*
> - ***The 7 mistakes** that make agents ignore your product*
> 
> *Most posts on this topic explain MCP. This section shows you how to actually get the initiative approved and shipped.*

![](https://substackcdn.com/image/fetch/$s_!nUdc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4e3e6d3-08e8-46a5-a06b-37320835bb86_3600x4500.png)

---

## 3\. The PM’s Role in Agent Distribution

So you’re a PM reading this. Maybe your company has a CLI. Maybe it doesn’t. Maybe you’ve heard of MCP. Maybe this is the first time.

**Here’s where you actually fit:**

- **If you’re at a** ***developer tools company*** **with an existing API and CLI…**  
	You’re closer than you think. Your CLI already outputs structured data. Your API handles authentication. The gap is probably an MCP server and better documentation. *2-4 weeks, 1-2 engineers.*
- **If you’re at a** ***B2B SaaS company*** **with an API but no CLI…**
	You have a bigger lift but a clear path. Start with AGENTS.md and an OpenAPI spec. Get your API docs in shape. Then scope a CLI or jump straight to MCP for your top 5 use cases.
- **If you’re at a company where most value is locked behind a GUI with limited API coverage…**
	You need to start earlier in the stack. The first conversation is about API coverage, not MCP. Agent access is a forcing function for building the [programmatic layer](https://www.news.aakashg.com/p/how-to-build-ai-products) you probably should have built anyway.

**The PM’s job across all three scenarios is the same:** frame the opportunity, define what to build first, write the spec, and *own the quality of the agent experience*.

That last part is where you add the most value.

Engineers will build the MCP server. They’ll expose the endpoints and handle the auth. But the quality of the [tool descriptions](https://www.news.aakashg.com/p/context-engineering)? The scoping of which features to expose first? The decision to start read-only? The choice of which use cases agents will actually care about?

*That’s [product judgment](https://www.news.aakashg.com/p/ai-product-sense).*

Look at how Stripe writes their tool descriptions. An agent reading “review payments, troubleshoot declines, process refunds” immediately knows what the tool does and when to use it. Compare that to “manages payment operations.” The first one gets picked. The second one gets skipped.

Docker’s MCP team put it directly:

> *“The agent, not the user, is the one calling your tool. Your documentation needs to support both audiences.”*

The PM is the person who understands both.

**Your role is to be the voice of the agent user.** Just like you advocate for human users, you now advocate for the agent trying to figure out your product at 3am with no [onboarding flow](https://www.news.aakashg.com/p/the-ultimate-guide-to-onboarding), no tooltips, and no customer success manager.

---

## 4\. From Strategy to Spec: The Meeting, The Pitch, The PRD

*You understand the landscape. You know the PM’s role. Now you need to actually get alignment, scope the work, and write the spec.*

This section gives you the exact playbook to go from “we should think about agent access” to “here’s the PRD, here’s the timeline, here’s who owns what.”:

### Step 1 - The Audit

Before anything else, answer five questions about your product:

1. What percentage of core value is accessible through an API?
2. Do you have a CLI? Does it output JSON?
3. Are your API docs machine-readable (OpenAPI spec)?
4. Can a developer authenticate without a browser?
5. Do you have an AGENTS.md?

Most teams score 1-2 out of 5. That’s fine. It tells you where to start.

### Step 2 - The Strategy Meeting

Your audit score is your conversation starter. You need alignment from eng leadership and probably your VP/CPO. I’d keep it to 45-60 minutes.

Start with data and a demo. Show Stripe’s MCP docs page. Show Linear’s one-command setup. If you can, open Claude Code, connect to one of their MCP servers, and show your team what it looks like when an agent uses a product. *Seeing an agent create Linear issues from conversation hits differently than reading about it.* Frame this as a distribution channel shift, not a feature request.

The next question is which features agents would actually want. Data retrieval, status checks, simple CRUD, report generation, and monitoring are the sweet spots. Cross-reference with what already has API coverage. The overlap is your starting scope.

From there, scope a concrete milestone. If you scored 0-1 on the audit: AGENTS.md plus OpenAPI spec in 2 weeks. If 2-3: CLI or MCP server on a 4-week timeline. Define it as a sentence:

> “By \[date\], an agent should be able to \[specific action\] through our \[interface\].”

**One more thing**: assign a PM as owner, not a tech lead. The PM owns the agent experience. 1-2 engineers, 2-4 weeks.

### Step 3 - The Stakeholder Pitch

If you need to sell this upward:

> *“Agent access is the next distribution channel. Stripe, Linear, Sentry, Asana, Shopify, Cloudflare, GitHub, Notion, Zapier, and Pendo all shipped production MCP servers. MCP hit 97 million monthly SDK downloads. Gartner projects 40% of enterprise apps will embed AI agents by end of 2026. The investment is 1-2 engineers for 4 weeks. The risk of not doing it is that competitors who ship agent access first become the default tool in every autonomous workflow.”*

### Step 4 - The PRD Template

I couldn’t find a good PRD template for this anywhere, so I built one. You can steal it as-is for your next strategy review, or hand it to Claude Code and have it draft your first version in minutes.

To use this: either paste it into your existing [PRD tool](https://www.news.aakashg.com/p/product-requirements-documents-prds), or feed it to Claude Code / the [PM Operating System](https://www.news.aakashg.com/p/pm-os) with context about your product and it’ll fill it out for you.

> #### AGENT ACCESS PRD
> 
> **Problem Statement**
> 
> \[X\]% of our product’s value is locked behind a GUI. As AI agents become a primary way workflows get assembled, our product is invisible to agent-based discovery. Competitors \[name them\] have shipped \[CLI/MCP/structured docs\] and are capturing agent-driven usage.
> 
> **User (Agent) Persona**
> 
> The “user” is an AI agent (Claude Code, Cursor, Codex, custom enterprise agents) acting on behalf of a human. The agent needs to: discover capabilities, authenticate programmatically, execute through structured interfaces, return parseable results. The agent’s human principal may never directly interact with our product.
> 
> Goals: complete a task in one shot. Constraints: can only see machine-readable content. Success: correct result with no confusion from vague descriptions or broken auth.
> 
> **Success Metrics**
> 
> - Agent-originated API calls as % of total (target: X% within 6 months)
> - Number of MCP client integrations (target: listed in X registries)
> - Time-to-first-action for an agent (target: under 5 minutes)
> - Error rate on agent requests (target: below X%)
> 
> **Scope: Phase 1**
> 
> - AGENTS.md file in primary repo
> - OpenAPI 3.0 spec for all public endpoints
> - CLI with JSON output for top 5 use cases: \[list them\]
> - OAuth 2.0 device flow for programmatic auth
> - MCP server exposing \[X\] read-only tools with full schema definitions
> 
> **Tool Definitions (for MCP)**
> 
> For each tool:
> 
> - Name: action-oriented, snake\_case (e.g., create\_task, get\_report)
> - Description: what it does + when to use it (1-2 sentences)
> - Input schema: JSON schema with types, required/optional, descriptions
> - Output schema: what the agent receives
> - Annotations: readOnlyHint, destructiveHint, openWorldHint
> 
> **Phase 2:** Write access with approval workflows, agent analytics dashboard
> 
> **Phase 3:** Agent-specific pricing, marketplace listings
> 
> **Non-Goals:**
> 
> - Replacing the existing GUI
> - Agent pricing in Phase 1
> - Full write access on day one

### Step 5 - Making Agent Access Part of Every PRD

The template above is for your first agent-access initiative. But every feature PRD you write from now on should include an agent access section. Not a separate doc. Part of the feature definition.

```markup
Here's my current PRD for [feature name]:
[Paste PRD]

Add an "Agent Access" section: How would an agent discover and use 
this feature? What MCP tool is needed? Input/output schema? 
Error states? Agent usage metrics?

Integrate as a subsection. Agent access is part of "done."
```

*If agent access lives in a separate PRD, it becomes someone else’s problem. If it’s a section in every feature PRD, it becomes culture.* This is the single highest-leverage change you can make.

---

## 5\. What Good Looks Like - 10 Production MCP Servers

Once you have a draft strategy and PRD, the next question is simple: **what does strong actually look like in production?**

That’s where examples help. Here’s what I learned studying 10:

![](https://substackcdn.com/image/fetch/$s_!Za7D!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F401d0ec5-2ca1-4aa9-8681-a9ded96b20d9_1080x1350.png)

1. **[Linear](https://linear.app/docs/mcp)** exposes tools for issues, projects, and comments. OAuth 2.1. Setup is one command: `claude mcp add --transport http linear-server https://mcp.linear.app/mcp`. An agent can triage bugs, plan sprints, rebalance workloads, create project structures from conversation. Their engineering team described it as “bringing Linear directly into AI tools of choice.” I wrote about [how Linear grows](https://www.news.aakashg.com/p/how-linear-grows) and agent access is now a core part of that story.
2. **[Sentry](https://docs.sentry.io/product/sentry-mcp/)** at `https://mcp.sentry.dev/mcp` lets developers query errors from their IDE or Claude. Then they played a meta-game: built MCP server *instrumentation* so you can monitor your own MCP server using Sentry. Build the MCP for your product AND the monitoring tools for everyone else’s. That’s how you become infrastructure.
3. **[Asana](https://developers.asana.com/docs/mcp-server)** connects to their Work Graph. Project updates, task search, comments, deadline management. Enterprise customers control which MCP clients are allowed. Their positioning: “Meet users where they are, enabling agent-driven interoperability.”
4. **[Shopify](https://shopify.engineering/mcp-ui-breaking-the-text-wall)** went further than anyone. They built **MCP UI**, returning *interactive UI components*, not just data. Agent searches for products, gets back embedded product cards with variant selection, image galleries, and cart flows. They open-sourced the spec. Shopify treats MCP as a first-class commerce channel alongside their storefront.
5. **[Stripe](https://docs.stripe.com/mcp)**, covered in Section 1, sets the standard for tool descriptions. An agent reads “review payments, troubleshoot declines, process refunds” and immediately knows what the tool does and when to use it. Their Order Intents API lets agents complete autonomous purchases. Visa Agent Cards add spending controls. Plus: they ship a Terraform provider so agents can manage Stripe configuration through infrastructure-as-code, not just API calls.
6. **[Cloudflare](https://developers.cloudflare.com/mcp/)** took the most radical compression approach. Over 2,500 API endpoints across DNS, Workers, R2, and Zero Trust, all routed through two tools: `search()` to find the right API call and `execute()` to run it. The agent writes JavaScript against a typed OpenAPI schema, Cloudflare runs it in a sandboxed worker. The entire interaction fits in roughly 1,000 tokens. If you have a massive API and you’re wondering how to avoid exposing hundreds of MCP tools, study Cloudflare.
7. **[GitHub](https://github.com/github/github-mcp-server)** ships one of the most full-featured MCP servers in production. Repos, issues, PRs, code review, CI/CD, Projects. What makes it worth studying: dynamic toolset discovery (agents enable tools on demand via an X-MCP-Tools header), server instructions that guide multi-step workflows through system prompts, and lockdown mode that restricts what untrusted contributor content can trigger. They consolidated related tools into fewer multi-operation tools with a `method` parameter, cutting context window usage by 50-90%. And PAT scope filtering automatically hides tools your token can’t access, so agents never see what they can’t use.
8. **[Notion](https://developers.notion.com/docs/mcp)** offers both a hosted remote MCP server (one-click OAuth) and a self-hostable open-source version. The design lesson: their v1 returned hierarchical block JSON, which ate context windows. V2 converts everything to Notion-flavored Markdown. Same information, dramatically fewer tokens. If your product stores hierarchical data (docs, wikis, knowledge bases), flatten it for agents.
9. **[Zapier](https://zapier.com/mcp)** turns 30,000 actions across 8,000 apps into MCP tools. One connection gets an agent access to Slack, Gmail, CRMs, analytics, and everything else. Their CTO [joined me on the Product Growth Podcast](https://www.youtube.com/watch?v=a9wO6GSAoGk) for a live demo. The scale is impressive but it’s also a warning: at 30K+ tools, description quality and smart routing become existential. “It’ll work one time then go off the rails” if tool descriptions overlap.
10. **Pendo** brings product analytics into agent workflows. Ask Claude to compare engagement across segments, and Pendo’s MCP server returns interactive charts you can toggle between line and bar, export the underlying data, and ask follow-up questions inline. Their CEO [joined the podcast](https://www.youtube.com/watch?v=C9hL_4Hrr8E) to talk about this approach. If you’re in analytics or reporting, Pendo shows what’s possible when you return visualizations alongside data instead of raw JSON tables.

The goal here is *not to copy any one MCP server exactly*. It’s to **study the decisions** strong teams made: what capabilities they exposed, how they described tools, how they handled auth, and where they kept the surface area narrow instead of trying to expose everything at once.

Across these ten examples, **four architecture patterns** show up again and again.

1. **Outcome-Oriented** servers map tools to workflows, not endpoints. One `track_order(email)` that calls three APIs internally beats three separate tools the agent has to chain. Stripe and Linear do this.
2. **Minimalist** servers compress massive APIs into a few meta-tools. Cloudflare routes 2,500 endpoints through two tools. The agent writes JavaScript against a typed schema, runs it in a sandboxed worker, and gets back the result. About 1,000 tokens instead of over a million if they’d mapped every endpoint.
3. **Platform Play** servers ship MCP alongside companion tools: monitoring, UI components, CLI, Terraform providers. Sentry, Shopify, and GitHub all take this approach.
4. **Knowledge Bridge** servers optimize for how agents consume information. Token-efficient formats, interactive responses, smart routing across large tool sets. Notion, Zapier, and Pendo fit here.

Most mature servers blend patterns. Stripe is outcome-oriented AND a platform play (MCP + Terraform + Visa Agent Cards). The pattern you start with depends on your API surface and customer base.

![](https://substackcdn.com/image/fetch/$s_!najw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fed59d8-e4bb-4516-be15-c306f2dfe012_3600x4500.png)

The pattern across all ten: **none of these are side projects**. They’re maintained by core teams, with OAuth or API keys, enterprise controls where needed, and listings on discovery registries. *That’s the bar*.

---

## 6\. Building It: A Claude Code Sprint

If you have [Claude Code](https://www.news.aakashg.com/p/how-to-use-claude-code-like-a-pro) access, open it in your project directory and follow along. You’re going to go from zero to a working AGENTS.md, CLI, and MCP server in a single sitting.

If you don’t have Claude Code, use this section as a spec for what to build with your engineering team. The prompts become ticket descriptions.

### Audit and Docs

Start with the audit:

```markup
> Look at our API and codebase. Audit our product for agent 
  accessibility. What's exposed? What's missing? 
  Gap analysis ranked by effort and impact.
```

Claude Code scans your codebase, finds your API routes, tells you what’s there and what isn’t. Use the output to confirm your PRD scope.

Then generate the AGENTS.md:

```markup
> Create an AGENTS.md for this project. Product capabilities in 
  plain language, auth with example commands, top 5 use cases 
  with requests and responses, rate limits, and boundaries 
  (what agents should NOT do). Keep it concise.
```

Claude Code reads your *actual code* and generates an AGENTS.md specific to your product. **Review the boundaries section carefully.** This is where you tell agents what they should never do. Commit it.

### CLI

```markup
> Build a CLI wrapping our top 5 API endpoints. Python with typer 
  and httpx. JSON output by default. Error codes in error messages. 
  Auth via PRODUCT_API_KEY env var. Thorough help text. Test locally.
```

Run a few commands. **The test: does the** `--help` **output make sense on its own?** An agent reads that to decide how to use the tool. If it confuses you, it confuses the agent.

### MCP Server

```markup
> Build an MCP server using Python and FastMCP. Read-only tools for 
  our top 5 use cases. Each tool description should explain what it 
  does and when to use it, written as if onboarding a new team member.
  Input schemas with types. Auth via env var. Read-only only.
```

Claude Code generates the server. **Now comes the part where you earn your keep as PM.**

Read every tool description. If a description says “manages tasks,” rewrite it to “Get all tasks for a project, filtered by status. Use this when checking what work is pending.” Stripe and Linear got this right. Your descriptions should be just as clear.

### Test and Ship

```markup
> Add our MCP server to your config. List all tools. Do a read 
  operation. Trigger an error. Chain two operations. Tell me 
  what felt confusing.
```

*This is where you see your product through an agent’s eyes.* If Claude Code picks the wrong tool or gets confused, every other agent will too. Fix descriptions until it’s intuitive.

Ship it:

```markup
> README with one-command setup for Claude Code, Cursor, VS Code. 
  Example prompts. Create a PR with everything.
```

Full agent access stack. Deployed from a single session.

### Already Have an MCP Server? Diagnose It.

If your team already shipped an MCP server, the question is no longer “do we have one?” It’s “is it actually good?” Most aren’t. Here’s how to find out.

**Diagnostic 1: Is your MCP server getting picked?**

If agents have access to multiple tools (yours and a competitor’s), the one with better descriptions wins. Connect Claude Code to your MCP server and a competitor’s. Ask it to complete the same task. Which tools does it reach for first? If it picks the competitor’s tool, your descriptions are too vague.

**Diagnostic 2: Description quality audit.**

```markup
> Connect to our MCP server at [URL]. List all tools. 
  For each tool, evaluate: 
  1. Is the description specific enough to pick the right tool on first try?
  2. Are input schemas complete with types and descriptions?
  3. Are readOnlyHint/destructiveHint annotations set correctly?
  4. Are error messages informative enough for an agent to self-correct?
  
  Rank issues by impact on agent usability. Suggest rewrites 
  for the worst descriptions.
```

Most MCP servers ship with vague descriptions because engineers wrote them. The PM pass is where descriptions go from “manages tasks” to “Get all tasks for a project, filtered by status. Use when checking pending work.” *That specificity gap is the difference between being picked and being skipped.*

**Diagnostic 3: Tool coverage vs. API drift.**

```markup
> Compare our MCP server's tool coverage against our API. 
  Which API endpoints don't have corresponding MCP tools? 
  Which ones should, based on frequency and agent use cases?
  Flag any tools that are out of sync with the current API.
```

MCP servers rot fast if they’re not updated alongside the product. This audit catches drift before your users do.

**Diagnostic 4: Is your MCP server driving discovery?**

Check whether your MCP server is listed on [PulseMCP](https://www.pulsemcp.com/servers), Docker’s MCP Catalog, and in the Claude integrations directory. If it’s not listed, agents can’t find it. Listing is the equivalent of submitting your app to the App Store. You also want to track: how many unique agent sessions connect per week, which tools get called most, and which tools never get called (candidates for removal or rewriting).

### Prompts for Ongoing Agent Work

These are the prompts you’ll reuse every sprint. Bookmark them.

**Competitive analysis:**

```markup
I'm a PM at [company] building [product]. Competitors:
1. [Competitor 1]
2. [Competitor 2] 
3. [Competitor 3]

Research each: CLI? MCP server? OpenAPI docs? AGENTS.md? 
Listed in MCP registries? Frame as competitive gap analysis 
for a strategy meeting.
```

If a competitor has an MCP server and you don’t, every Claude Code user, every Cursor session picks them by default. That’s the framing that gets executive attention.

**Scoping what to expose:**

```markup
Our product's core features and API coverage:
[List features with: full API, partial API, no API]

Recommend 5 features to expose to agents first. Prioritize by 
frequency, complexity (single tool call?), risk, and API readiness. 
For each, draft the MCP tool name and 2-sentence description.
```

The output becomes your PRD scope. It also surfaces API coverage gaps, which is often the real bottleneck nobody wants to talk about.

**Writing MCP tool definitions:**

These are the most important piece of copy you’ll write for the agent channel. They’re to agents what landing page copy is to humans.

```markup
Top [X] API endpoints for [product]:
[Paste API docs]

Generate MCP tool definitions: name (snake_case), description 
(what it does + when to use it), input schema, output schema, 
annotations (readOnlyHint, destructiveHint).

Write descriptions the way Stripe and Linear do: specific enough 
that an agent knows which tool to pick on first encounter.
```

**Review the output obsessively.** Vague descriptions = agents skip you for a competitor.

*(For broader PM prompts, my [PM Prompt Library](https://www.news.aakashg.com/p/pm-prompt-library) and [Context Engineering](https://www.news.aakashg.com/p/context-engineering) guide cover the full stack.)*

---

## 7\. Where Teams Go Wrong

I’ve seen enough MCP launches to spot the patterns that kill agent adoption. Here are the seven most common, ranked by how often I see them.

![](https://substackcdn.com/image/fetch/$s_!1RHH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F551989d3-2d79-4df4-9fbd-8ae965a0aacf_1080x1080.png)

#### Mistake 1: The CLI Checkbox

The team ships a CLI that wraps three endpoints, outputs human-readable tables instead of JSON, and calls it done.

This is like launching a “mobile app” that’s just your desktop site in a webview. It technically exists. Nobody uses it. Agents need structured JSON, parseable errors, environment variable auth.

A CLI is a product that needs the same care as your GUI. Every command should output JSON by default. Add `--human` or `--pretty` for readable output. *The default consumer is now a machine.*

#### Mistake 2: The Vague Description

An MCP tool that says “Manages tasks” tells an agent nothing. When to use it? What does it need? What comes back?

An agent encountering that will skip it for a competitor’s tool that says “Create a new task in a project. Use when adding a work item. Requires project\_id and title.” The specificity gap between good and bad [tool descriptions](https://www.news.aakashg.com/p/guide-aeo-geo) is the gap between getting picked and getting ignored.

Research backs this: at 30+ tools with overlapping descriptions, agents start selecting the wrong one. At 100+, failure is **nearly guaranteed**.

This is the single most common failure I see. And the fix is the simplest: write every tool description as if you’re onboarding a new team member who can’t ask follow-up questions. What does it do? When would they reach for it? What does it need from them?

Stripe writes “review payments, troubleshoot declines, process refunds.” Match that bar.

#### Mistake 3: Write Access on Day One

Full CRUD through the MCP server, no guardrails. An agent does something destructive. Everyone panics. Agent access gets rolled back *entirely*.

Linear, Stripe, Sentry all started read-only and layered in write access with approval workflows. Follow them. Phase 1 is read-only. Phase 2 adds write with `destructiveHint` annotations and confirmation flows.

That’s the right sequence. Skip it and you’ll spend a quarter rebuilding trust with your security team.

#### Mistake 4: Browser-Dependent Auth

This one kills adoption silently. Your MCP server works great in demos because someone already has a session cookie. Then an agent tries to connect at 3am and hits a login page it can’t navigate.

OAuth 2.0 device flow solves this: show a URL and code in the terminal, user approves in browser, agent gets the token. API keys for server-to-server.

The test is simple: try authenticating from a headless environment with no browser window. If it doesn’t work, **agents can’t use you**.

#### Mistake 5: Building in Isolation

Team ships an MCP server, nobody maintains it, tools drift out of sync within three months. This happens every time agent access lives in a separate repo maintained by “that one engineer who’s into AI.”

The rule: new GUI capability = new MCP tool. Same sprint. Same PR. Same CI pipeline. Same review process.

Agent access that isn’t coupled to the product codebase rots within a quarter. Make it part of the [definition of done](https://www.news.aakashg.com/p/proactive-product-quality), or don’t bother building it.

#### Mistake 6: Shipping and Not Listing

You built a great MCP server but didn’t list it anywhere.

Submit to PulseMCP, Docker’s MCP Catalog, and the Claude integrations directory the week you ship. Put the URL in your API docs, README, and developer landing page.

This is the equivalent of building an iOS app and never submitting it to the [App Store](https://www.news.aakashg.com/p/ultimate-guide-growth-loops). If agents can’t find you, *you don’t exist*.

#### Mistake 7: No Agent Metrics

You shipped the MCP server but have no idea if anyone’s using it. No tracking of agent-originated calls, no tool-level usage data, no error rate monitoring.

You wouldn’t launch a feature without [analytics](https://www.news.aakashg.com/p/success-metrics-interview). Same applies here. Segment agent-originated API calls in your existing analytics. Track calls per tool, error rates, and **which tools never get called**.

That last category matters most. Tools that never get called are either poorly described or shouldn’t exist. Both are problems a PM can fix in an afternoon.

---

## What’s Next

The teams getting this right share one thing. They treat the agent as a first-class user with a PM who owns that experience. The PM reviews tool descriptions the way they’d review [UI copy](https://www.news.aakashg.com/p/the-product-copy-playbook). Tests the MCP server the way they’d test [onboarding](https://www.news.aakashg.com/p/the-ultimate-guide-to-onboarding). Tracks agent metrics the way they’d track DAU.

That’s the job now.

**If you do nothing else after reading this, do three things this week:**

1. Run the 5-question audit
2. Pick your top 5 agent use cases
3. Ship AGENTS.md before Friday

**That alone will put you ahead of most teams still treating agent access like a 2027 problem.**

And keep this guide bookmarked. This is one of those shifts where the winners will revisit the playbook every quarter, not once.

POLL

### What did you think of today's post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

*5 resources to go deeper:*

1. *[MCP explainer and live demo with Zapier CTO](https://www.youtube.com/watch?v=a9wO6GSAoGk)*
2. *[AI PM upskilling with Pendo CEO (MCP in action)](https://www.youtube.com/watch?v=C9hL_4Hrr8E)*
3. *[Context engineering guide](https://www.news.aakashg.com/p/context-engineering)*
4. *[How to build AI products](https://www.news.aakashg.com/p/how-to-build-ai-products)*
5. *[Claude Code guide](https://www.news.aakashg.com/p/how-to-use-claude-code-like-a-pro)*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/master-ai-agent-distribution-channel) on 2026-05-30T15:16:50-04:00*
