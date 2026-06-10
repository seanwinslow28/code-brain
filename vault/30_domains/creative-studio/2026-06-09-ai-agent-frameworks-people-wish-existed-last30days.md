---
title: "AI Agent Frameworks People Wish Existed — What's Missing (last 30 days)"
date: 2026-06-09
type: research
source: last30days
tags: [ai-agents, agent-frameworks, langchain, crewai, langgraph, agent-sdk, memory, mcp, a2a, research]
date_range: 2026-05-10 to 2026-06-09
---

# AI Agent Frameworks People Wish Existed — What's Missing

_Research run 2026-06-09 via `/last30days`. Sources: Reddit (with comments), X, YouTube (transcripts), Hacker News, web. Window: 2026-05-10 → 2026-06-09._

## TL;DR

The complaints have shifted from "the model isn't smart enough" to **"the scaffolding around the model doesn't exist yet."** Across every source, the same line recurs: _stronger models keep breaking on the exact same tasks_, because the failure is in the **harness**, not the brain. The five things people most wish existed:

1. **A real memory/state OS** — first-class, not a vector-DB bolt-on.
2. **An agent auth/identity layer** — capability-scoped permissions; "agent-ready" web.
3. **The boring production layer in a box** — observability + eval + guardrails + audit, default-on.
4. **A minimal composable harness** — own your loop without forking a monolith or rewriting from scratch.
5. **An interop + payments fabric** — agent discovery, agent-to-agent transactions, the "HTTPS moment."

Underneath all five is a disillusionment current: _"Stop building AI agents," "agents are now more expensive than developers," "everything is being called an agent now."_

---

## Gap 1 — Memory & State: the #1 unsolved primitive

This was the loudest, most cross-platform signal.

- **X — @Vegas_AI_Guy:** _"The thing nobody tells you about a long-running AI agent: it has no memory. Every session it wakes up blank. What persists isn't the model — it's the files the agent writes to itself and re-reads on boot."_
- **X — @cortexdbai:** _"The Memory Wars Are Coming."_
- **YouTube — "Why AI Agents Keep Forgetting Things" (Artificial IQ):** the sharpest technical articulation. _"These failures are often attributed to the limitations of the language model, yet stronger models continue to break on the exact same tasks. The breakdown usually stems from the infrastructure surrounding the model."_ Names the missing primitive precisely: a **four-layer architecture (brain / state / memory / external systems)**, checkpointing + rollback, and a **memory life-cycle** (create → update → summarize → delete) to prevent _"memory rot"_ — where stale preferences silently contradict new instructions. Cites Anthropic's lazy-loading of tool schemas (134K tokens of schema alone → tool-use accuracy 49% → 74%) and MemZero (91% retrieval-latency drop) as evidence the bottleneck is plumbing, not IQ.
- **Web — [mem0: State of AI Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026):** the still-open problems — **cross-session identity resolution** (the memory model assumes a stable user ID; anonymous/multi-device/mixed-auth breaks it), **memory staleness** (a highly-retrieved memory becoming confidently wrong), and **the GDPR ↔ EU AI Act tension** (right-to-be-forgotten vs. 10-year audit-trail retention for high-risk systems).

**What people wish existed:** memory/state as a first-class framework primitive — durable checkpoints, deterministic rollback, retrieval you can inspect — not "wire up a vector DB yourself." See [Oracle: Agent Memory — Why Your AI Has Amnesia](https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia) and [SitePoint's 2026 memory guide](https://www.sitepoint.com/ai-agent-memory-guide/).

## Gap 2 — Auth / Identity / Permissions: agents fail at the auth step, not the reasoning step

- **Reddit — r/artificial, "AI agents fail at the auth step more than at the reasoning step. anyone else seeing this?"** (2026-06-05). The reasoning is fine; the agent dies trying to authenticate, hold a session, or get scoped access.
- **X — @ayushagarwal** (31 likes): _"Your website isn't agent-ready. We open-sourced the fix with Dualmark."_
- **Web — [Agent Protocol Stack 2026 (Turion)](https://turion.ai/blog/ai-agent-protocol-stack-2026/) + [arXiv: Permission Manifests for Web Agents](https://arxiv.org/pdf/2601.02371):** OAuth 2.1 gets you identity and coarse access, but agents need **capability-level permissions** — _"this agent can call `check_stock` but not `update_inventory`."_ Identity/trust (W3C DIDs, Agent Cards) is unsettled.

**What people wish existed:** a standard for agent identity + **capability-scoped** authorization, and an "agent-ready" web spec so sites expose safe, structured affordances instead of getting scraped/blocked.

## Gap 3 — The "boring" production layer nobody builds

A whole cluster of high-engagement posts is about everything _after_ the demo works.

- **Reddit — r/artificial, "the boring part of AI agents nobody builds and everyone needs"** (2026-06-09).
- **Reddit — r/AI_Agents, "AI Agents in Production: The Failure Modes Nobody Puts in the Demo."**
- **Reddit — r/LangChain, "For teams building AI agents: what failures are the hardest to debug?"** (2026-06-08).
- **Reddit — r/AI_Agents, "if you're building ai agents without evaluating them you're shipping blind."**
- **Reddit — r/AI_Agents, "I spent weeks building an AI agent. The real challenge came after launch."**
- **Reddit — r/artificial, "Six places our AI builds keep breaking."**
- **Web — [Towards AI: 10 frameworks I tried](https://towardsai.net/p/machine-learning/i-tried-10-ai-agent-frameworks-in-2026-heres-the-honest-guide-i-wish-i-had-earlier):** _"Production agents need observability, guardrails, evaluation harnesses, and a deployment story — underestimating these is the most common reason agent projects stall after a successful demo."_ Highest-cost mistakes happen post-launch: **runaway tool calls, skipped approvals, unclear ownership, incomplete audit timelines.**

**What people wish existed:** a default-on "boring layer" — eval harness + tracing + guardrails + audit + human-in-the-loop approval — bundled, not assembled from a dozen incompatible parts. Debugging in particular: _every agent step should log what memory was retrieved, injected, and evicted._

## Gap 4 — Frameworks are over-abstracted: the "framework tax," and the build-your-own-harness exodus

The strongest single engagement spike in the whole pull was about _leaving_ frameworks.

- **X — @mfpiccolo: "How to build your own agent harness???"** — **1,984 likes, 248 RTs.** By far the highest-engagement item.
- **Reddit — r/LangChain, "LangChain, CrewAI, AutoGen, LlamaIndex. I've used all four. Here's what you actually need to know"** (78 pts). Representative comment: _"LangGraph's 'framework tax' is front-loaded — you pay it once in graph design and then you have a real state machine"_; and on LlamaIndex, _"I disliked the APIs."_
- **X — @Avnish_gupta_45:** _"A year ago LangGraph felt like the missing piece for building reliable AI agents. But Agent SDKs are evolving fast — tool calling, memory, tracing, multi-agent workflows. So is LangGraph still worth it?"_
- **Web — [iii.dev: How to Build Your Own Agent Harness](https://iii.dev/blog/how-to-build-your-own-agent-harness/):** _"Most agent teams don't build a harness — they adopt one… If something inside it doesn't fit, you fork it, fight it, or work around it… every long-running agent team eventually ends up rewriting its harness from scratch. I think that shape is wrong."_ Martin Fowler's framing (via [LangChain](https://www.langchain.com/blog/how-to-build-a-custom-agent-harness)): **agent = model + harness; only the model reasons; the harness drives more performance than the model.**
- **Web — framework-specific gripes ([daily.dev](https://daily.dev/blog/ai-agents-guide-for-developers-langchain-crewai/), [Arsum](https://arsum.com/blog/posts/ai-agent-frameworks/)):** LangChain — _over-abstraction hurting maintainability/customization_; CrewAI — role abstraction breaks under fine-grained control needs, **~3× token footprint** of LangGraph on simple workflows, and _"action traces that don't reflect actual execution."_ Rising "I wish I'd started here" picks: **Pydantic AI** (DX 8/10 vs LangChain 5/10), **Mastra** (de facto TypeScript choice).
- **Vendors are converging on this exact wish:** [Microsoft Agent Framework at BUILD 2026](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/) now ships a first-class **"Agent Harness"** (shell/filesystem access, human-in-the-loop approval, long-session context management); LangChain's `create_agent` went **deliberately minimal** (core loop + middleware as the customization primitive).

**What people wish existed:** a **minimal, composable harness** — own the loop, swap parts, add middleware — instead of a monolith you fork or outgrow. The market is moving from "import a framework" to "compose a harness."

## Gap 5 — Interoperability & payments: agents can't find each other or transact

- **X — @CeloDevs (Frontier Pool grant focus)** — a literal "what's-missing" list: _"Agent identity & discovery / Agent-to-agent payment rails / AI-native developer tooling / Verification and trust infra / Interoperability."_
- **X — @paramiao:** framing of the moment — _"agents still need their HTTPS moment."_
- **X — @caixin:** Tencent opening WeChat's agent ecosystem to developers (book rides, order food, etc.) — platform-level agent surfaces arriving.
- **Web — [Turion](https://turion.ai/blog/ai-agent-protocol-stack-2026/) / [Zylos](https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence/) / [arXiv survey](https://arxiv.org/pdf/2505.02279):** MCP (vertical, agent→tools) + A2A (horizontal, agent→agent) are the default stack, but **an MCP server can't yet be consumed as an A2A skill** (joint spec work reportedly Q3 2026); payments are **fragmenting into bespoke rails** (Visa TAP, Mastercard Agent Pay) because A2A deliberately omits negotiation semantics — _"a pile of bespoke schemas pretending to be interoperable."_

**What people wish existed:** a unifying interop + transaction fabric — agent discovery/registry, agent-to-agent payments, cross-protocol bridging (MCP↔A2A), and trust/verification — so multi-agent systems stop being demos.

---

## The disillusionment undercurrent (context, not a gap to build)

Worth weighting because it shapes how any new framework will be received:

- **Reddit — r/GithubCopilot, "I guess AI era is over. Agents are now more expensive than developers"** (160 pts). Top comment (95 up): _"I mean this nicely but if that's more expensive than devs they are extremely underpaid."_
- **Reddit — r/artificial, "I think we're about 12 months away from the first major AI agent disaster"** (134 pts). Top comment (117 up): _"We're definitely in that weird phase where the hype is drowning out basic risk assessment."_
- **Reddit:** _"Stop building AI agents"_ (r/AIforOPS) · _"Does anyone else feel most AI tooling is becoming harder instead of easier?"_ · _"Everything is being called an AI agent now and it's getting confusing."_
- **YouTube — "Your AI Agent Isn't Wrong, You're Using It Wrong" (Celine Xu):** the maturity take — distinguish **variation** (acceptable for judgment work) from **inconsistency** (fatal for deterministic work); _"AI agents are not magic calculators."_ Recommended architecture: flexible reasoning on top, deterministic execution underneath.

---

## Why this matters for Sean (Code-Brain angle)

Sean's autonomous fleet (`agents-sdk/`) has _already_ hand-built much of the missing layer the internet is asking for — which is itself the story:

- **Gap 1 (memory/state):** the fleet-memory layer (`vault/90_system/fleet-memory/`) + the daily-note "fleet console" are exactly the durable, inspectable memory primitive people wish frameworks shipped.
- **Gap 3 (boring layer):** `agent-fleet-observability/` (kanban + manual-tickets schema), the nightly critic/lint loop, and per-run spend caps are the eval/observability/guardrail stack the Reddit threads beg for.
- **Gap 4 (compose-don't-import):** the HybridRouter + skills-as-system-prompts design is a custom harness, not an off-the-shelf framework — the precise "build your own harness" pattern @mfpiccolo's 1,984-like post is chasing.

**Substack hook (high-confidence):** _"The AI agent framework everyone wants already exists — I built it for one user."_ The five-gap structure above maps cleanly onto a "what's actually missing vs. what I wired up myself" post, and the harness-not-the-model thesis is a strong, defensible hiring-signal narrative for an AI-PM transition. Candidate for the writing chain.

---

## Stats

- **Window:** 2026-05-10 → 2026-06-09 (30 days)
- **Queries run:** 4 last30days passes + 4 web searches
- **Reddit:** ~25 unique threads (with ScrapeCreators comments) across r/AI_Agents, r/artificial, r/LangChain, r/GithubCopilot, r/AIforOPS
- **X:** ~25 posts (top engagement: @mfpiccolo "build your own agent harness" — 1,984 likes / 248 RTs)
- **YouTube:** 3 transcripted videos (memory architecture, framework selection, variance-vs-inconsistency)
- **Web:** ~30 sources — strongest: [mem0 memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026), [iii.dev harness](https://iii.dev/blog/how-to-build-your-own-agent-harness/), [Turion protocol stack](https://turion.ai/blog/ai-agent-protocol-stack-2026/), [Microsoft Agent Framework BUILD 2026](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/), [Towards AI: 10 frameworks](https://towardsai.net/p/machine-learning/i-tried-10-ai-agent-frameworks-in-2026-heres-the-honest-guide-i-wish-i-had-earlier)
- **Caveat:** social windows are noisy; the highest-signal evidence here is the convergence of Reddit complaints + the 1,984-like harness post + independent web/engineering posts all naming the **same** five gaps.
