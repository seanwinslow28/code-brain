---
title: "Six agent protocols just launched. Three of them decide which products survive. Here is how to tell which three."
source: "https://natesnewsletter.substack.com/p/agent-protocol-stack-mcp-a2a"
author:
  - "[[Nate]]"
published: 2026-05-18
created: 2026-05-21
description: "Six agent protocols launched in a year. Three form the core stack: MCP for tools, A2A for delegation, AG-UI for human control. Map your product to the right layers."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management]
ai-context: "Nate Jones surveys the six newly-launched agent protocols (MCP, A2A, etc.) and identifies the three that will determine which products survive the next platform shift."
---
Google I/O opens today, and most of the coverage will be about the demos. The more interesting story is the protocol race happening underneath them. Six new agent protocols have launched in the past year, and if you are building or buying agents right now, the standards layer reads like a scrum.

The instinct is to ignore the acronyms and wait for the big platforms to absorb everything behind product surfaces. The platforms will absorb a lot of it. But the protocols are not all trying to solve the same problem, and the substrate an agent is built on shapes the customer experience more than the model choice does. Read as a pile of competing standards, the picture stays blurry. Read as layers, three of them snap into focus as the foundation most builders will actually depend on.

Three protocols are forming the core agent stack: MCP for the tools and data an agent can reach, A2A for the other agents it can delegate to, and AG-UI for the controls a human needs to stay in the loop while long-running work is happening. Those three answer the only three questions every real agent system hits within its first week of existence. What can the agent use. Who else can the agent work with. How does the human stay in control. A2UI, AP2, and x402 matter, but they sit in layers where product requirements, trust boundaries, payment rails, and platform incentives are still being negotiated. Treating those three as equal bets with the first three is the most common mistake I see in agent strategy decks right now.

Builders who try to bet on all the layers at once end up paralyzed. Builders who ignore the layer map ship agents that fail at the boundaries that actually matter, like security on tool access, approval on long-running work, and supervision when the agent crosses company lines. Buyers who cannot read the layer map cannot evaluate what they are actually purchasing when a vendor says the word “agent.” The map is the closest thing the industry has to a shared vocabulary, and the next twelve months of agent product strategy will run through it.

**Here’s what’s inside:**

- **The protocol map.** A single table that places all six protocols in the layer they actually occupy, so the acronyms stop blurring together.
- **The core stack: MCP, A2A, AG-UI.** Why these three are converging into the universal foundation, what each one is really for, and where each one fails if treated as a feature toggle instead of a boundary.
- **Why payments are not one protocol.** AP2 and x402 solve different problems, the payment space carries hidden assumptions about geography and authorization, and “agent can pay” is not a button — it is an audit problem.
- **Map, draft, audit, brief.** Map any real workflow to the layers that matter, draft the Agent Card boundary another team will integrate against, audit a workflow for the human controls it’s missing, and produce the strategy brief for the leader making the platform bet — four prompts, one per job, with renewal prep as the worked example threaded through.

The acronym pile will keep growing. The layer map will not.

## LINK: Grab the prompts

The hardest part of agent work right now is not picking the right acronym. It is staring at a real workflow — vendor intake, renewal prep, support triage, whatever yours is — and not knowing which of the six layers will actually shape whether the agent ships or stalls. These four prompts exist because that decision is where most teams freeze. The Layer Mapper takes a workflow and tells you which layers are CRITICAL, which are RELEVANT, and which you can ignore for this build, plus the sequence to ship in. The Agent Card Designer turns “what does my agent do” into the operating contract another agent or team can actually integrate against, with the boundaries and approval gates written down before they become production incidents. The Control Point Auditor walks a workflow step by step and forces a verdict on every action — Hard Gate, Soft Signal, Inspection Point, Steering Opportunity, or none — so the supervision layer is designed instead of discovered the week after launch. The Strategy Brief is for leaders deciding where to invest, where to keep an adapter, and where to defer; it produces a 30-day, 90-day, and six-month sequence with watch items that should trigger a reassessment. Start with the Layer Mapper. It tells you which of the other three you actually need.

## Software trying to become a worker

None of this is theoretical. Google I/O [opens today](https://io.google/2026/), and Google is very clearly trying to make the agent stack feel coherent. In March, Google published a [developer guide to AI agent protocols](https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/) that walks through MCP, A2A, AP2, A2UI, and AG-UI in a single supply-chain example. The point of the example is not subtle. A real agent checks internal data, calls remote supplier agents, authorizes payment, and renders an interactive dashboard. Software trying to become a worker, not a chatbot.

When software becomes a worker, the old integration model breaks.

The old model assumed a human was driving the software directly. A person logged in, clicked around, approved the action, reviewed the output, entered the card, downloaded the report, or sent the email. The system could rely on the human being present at the moment of action. That assumption is weakening.

An agent may read a database, ask another agent for a quote, request user approval, assemble an interface, pay for an API call, and return hours later with a result. It may do some of this while the user is away. It may cross company boundaries. It may touch systems with different owners. It may need to prove that it had permission to act.

Protocols are showing up now because of this shift. Not because developers love acronyms, though we do. Agentic software has outgrown the custom-integration era before most companies even finished understanding it.

## The protocol map

Read it by layer.

MCP is agent to tools and data. The [Model Context Protocol specification](https://modelcontextprotocol.io/specification/) defines MCP as an open protocol for connecting LLM applications to external data sources and tools. In practice, MCP lets a host discover servers that expose resources, prompts, and tools. This is why MCP became the first protocol most builders noticed. [Claude Desktop supports local MCP servers](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers), [Sourcegraph ships an MCP server](https://sourcegraph.com/docs/mcp), [Square ships an MCP server](https://developer.squareup.com/docs/mcp), and [PulseMCP lists more than 14,000 MCP servers](https://www.pulsemcp.com/servers). Agents are useless if they cannot reach the work.

A2A is agent to agent. Google describes the [Agent2Agent protocol](https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/) as the standard way for agents to discover and communicate with each other. Each A2A agent can publish an Agent Card that describes its capabilities and endpoint. Google launched A2A in April 2025 with more than 50 partners, including [Atlassian, Box, Cohere, MongoDB, PayPal, Salesforce, SAP, ServiceNow, UKG, and Workday](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/). By early 2026, more than 150 organizations had signed on, and the protocol was donated to the Linux Foundation in June 2025 for neutral governance. That list matters because A2A only matters if agents cross product and company boundaries. The important idea is not “swarms.” It is discoverable delegation.

AG-UI is agent to user. The [AG-UI docs](https://docs.ag-ui.com/introduction) describe it as an open, event-based protocol connecting agentic frontends to agentic backends. It is much younger than MCP, so it should not be treated as equal on adoption. But it is the most developed open candidate for a problem every serious agent app hits: how the frontend shares state, events, approvals, and interruptions with a long-running backend agent. CopilotKit is the home ecosystem, and the [AG-UI integrations page](https://docs.ag-ui.com/integrations) points to LangGraph, CrewAI, Amazon Bedrock AgentCore, Pydantic AI, Mastra, and others.

A2UI is agent-generated interface. Google introduced [A2UI on December 15, 2025](https://developers.googleblog.com/en/introducing-a2ui-an-open-project-for-agent-driven-interfaces/) as an open project for agent-driven interfaces. Instead of sending arbitrary HTML or JavaScript from an untrusted remote agent, A2UI sends a structured, declarative UI representation that a client can render using trusted components. This is useful, but it is narrower than the human-control problem. It is a way for an agent to describe an interface, not the whole protocol for managing the user-agent relationship.

AP2 is agent payment authority. Google announced the [Agent Payments Protocol](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol?e=48754805) in September 2025 as an open protocol for agent-led payments, with more than 60 collaborators including Adyen, American Express, Coinbase, Mastercard, PayPal, Salesforce, ServiceNow, UnionPay International, and Worldpay. The key mechanic is the mandate: a cryptographically signed proof of user instructions. AP2 is trying to answer the hardest question in agentic commerce: how does the ecosystem know the agent was authorized to buy? On April 28, 2026, Google [donated AP2 to the FIDO Alliance](https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/) for neutral governance, alongside Mastercard’s contribution of a companion standard called Verifiable Intent. Same pattern as A2A’s path to the Linux Foundation, and the same signal: this layer is settling fast enough that the founding companies are willing to hand stewardship to a standards body.

x402 is machine-native payment over HTTP. [Coinbase launched x402](https://www.coinbase.com/en-ca/developer-platform/discover/launches/x402) in May 2025 as an HTTP-native stablecoin payment protocol. [Cloudflare now documents and supports x402](https://developers.cloudflare.com/agents/agentic-payments/x402/) in its agentic payments flow. A server can return payment instructions, the client can sign a payment payload, and the server can verify or settle the transaction before returning the resource. That matters for APIs, data, content, MCP tools, and other resources where account setup and subscriptions are too heavy.

On a single map:

![](https://substackcdn.com/image/fetch/$s_!Be19!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9dd3aa3-1776-4395-8afc-12ce72a3915b_1172x710.png)

This table is the article. Most confusion comes from flattening it.

## MCP is the access layer

MCP won mindshare first because it solves the most immediate pain. An agent sitting in a chat box with no access to the user’s tools is mostly a consultant. It can advise, summarize, draft, and reason. It cannot do very much work.

The first thing every serious agent product needs is a way to connect to systems where state lives: GitHub, Slack, Google Drive, Postgres, Snowflake, Stripe, Linear, Salesforce, a file system, a browser, a calendar, an internal API, a data warehouse. Before MCP, every integration tended to become custom glue. The developer had to write tool definitions, authentication patterns, parameter schemas, error handling, and update logic for each system.

MCP tries to standardize that. A server exposes tools and resources. A host connects to it. The model receives a usable description of what can be done. The system can compose new capabilities without every agent platform rebuilding every connector from scratch.

The story usually stops there, but MCP does not make tools safe just because it standardizes them. The MCP specification itself is careful about that. It says the protocol enables powerful capabilities through arbitrary data access and code execution paths, and that implementors need consent, authorization, privacy controls, and tool safety. Security researchers are already finding why that warning matters. Invariant Labs described [MCP tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), where malicious instructions can hide in tool descriptions and influence an agent through the very metadata meant to make tools discoverable. Tool access is not a feature toggle. It is a security boundary.

The builder takeaway is simple: if your agent needs to work across tools and data, MCP is the default interface to understand. Do not build every connector from scratch unless you have a specific reason. Also do not pretend existing enterprise integrations disappear overnight. Most large companies will run custom APIs, workflow glue, and MCP side by side for years. MCP wins first at the margin: new agent-facing integrations, reusable tool surfaces, and product ecosystems where discovery matters. But do not confuse tool discovery with governance. You still need scopes, approval flows, audit trails, and a way to decide which tools the agent can see in which context. MCP gets the agent near the work, not into it.

## A2A is the delegation layer

The second problem arrives once the agent can reach tools. The agent still cannot know everything or own every capability.

A procurement agent may need a supplier agent. A travel agent may need a hotel agent. A finance agent may need a tax agent, a software agent may need a security reviewer, a customer-success agent may need billing. In a large company, no single agent will be allowed to access every system or make every decision. Work is distributed across owners, permissions, domains, and expertise.

A2A matters because it turns that distribution into something agents can reason about.

The Agent Card is the important primitive. A remote agent can describe what it is, what it does, which skills it exposes, where it can be reached, and how another agent should interact with it. It goes beyond documentation. It is a way for agentic systems to route work without hardcoding every relationship.

The standard is more serious than the swarm rhetoric around it. The world does not need ten agents role-playing as a boardroom for every task. The world does need agents that can discover the right specialist, pass the right task, preserve enough context, and return a result without forcing the user to become the integration layer.

The named operators make the distinction clearer. Box wants document agents to participate in external workflows without handing every file to another platform. Salesforce and ServiceNow want enterprise agents to cooperate outside their own product surfaces. MongoDB wants data agents to be callable by the business agents that need application state. Different motivations, same pattern: A2A is about cross-boundary work, not a cute multi-agent demo.

Coordination is not free. A2A adds another surface for latency, failure, permissions, identity, and observability. If an agent asks another agent to ask another agent to do something, the work may become more flexible, but it also becomes harder to debug.

That means A2A is not the right answer for every product. A single product with a small set of tools may not need inter-agent coordination. But any system that crosses organizational boundaries, product boundaries, or specialist domains will eventually need something like it.

The actual question is not “Should I use A2A because it is new?” It is: does this workflow require delegated expertise or authority outside the primary agent?

If yes, design the boundary now. Decide what your agent can advertise, what it can accept, what it cannot share, what requires human approval, and how a downstream result is validated. The Agent Card is the first version of an operating contract, not a marketing page.

## AG-UI is the control layer

The third protocol is easier to underestimate because it sounds like frontend infrastructure. It is not. The human interaction layer is where trust survives.

If an agent is long-running, nondeterministic, and capable of touching external systems, the user needs more than a final answer. The user needs to see what is happening, interrupt when necessary, approve sensitive steps, correct course, inspect state, and understand why the agent is waiting.

Traditional web apps were mostly built around request and response. The user clicks. The server returns. The UI updates. Agents break that pattern. They stream, pause, ask for approval, call tools, discover new information, change plans, call sub-agents, and recover after disconnects.

AG-UI exists because the chat box is not enough for that.

Its documentation lists the things agentic apps need: streaming, shared state, frontend tool calls, backend tool rendering, interrupts, sub-agent composition, steering, and custom events. This goes beyond polish. It is the difference between a magic demo and a product that can be supervised without exhausting the user.

This is the layer many teams will ignore until their agents start doing real work. They will wire a model to tools, add a pretty chat component, and discover that users have no idea what the agent is doing. Then come approval buttons, which turn out not to be enough. Then logs, which are not interaction. Then a progress spinner, which is not state.

The user does not need every token. They do need the right control points. What is the agent trying to do. What is it waiting for. What can the user approve, deny, edit, pause, or cancel. Which result is final, and which is provisional.

The AG-UI layer belongs with MCP and A2A in the core stack, even if the specific protocol is earlier in its adoption curve. MCP gives the agent tools. A2A gives it collaborators. AG-UI names the user-control layer that every production agent needs, whether the winning implementation is AG-UI itself or a close cousin.

An agent that cannot show its work becomes supervision debt.

## A2UI solves one part of the interface problem

A2UI is one of the more interesting pieces because it addresses a real product limitation: text is a bad interface for many tasks.

If an agent is booking a table, it should not ask twelve text questions. It should render a date picker, a time selector, a guest count, available tables, and a confirmation control. If an agent is comparing vendors, it may need a table. If it is analyzing sales territories, it may need a map. If it is reviewing a policy exception, it may need a form.

The danger is sending arbitrary UI code from a remote or untrusted agent. Google’s A2UI answer is to send declarative UI data that a client renders using trusted components. The client owns the styling and security boundary. The agent can ask for a component from an approved catalog. It cannot simply execute whatever interface code it wants.

That is directionally right, but it also means A2UI is probably not the same kind of universal bet as MCP or A2A. UI rendering is deeply product-specific. Consumer chat, enterprise dashboards, IDEs, mobile apps, desktop agents, and embedded copilots will not all converge cleanly on one rendering model overnight. There will be overlap among A2UI, AG-UI’s generative UI work, MCP Apps, platform-native component systems, and ordinary product engineering.

So the move is to avoid coupling your product too tightly to one generative-UI bet before the ecosystem settles.

Use the principle now: agents should produce structured interface descriptions, not arbitrary executable UI. Keep the client in control of rendering. Maintain a trusted component catalog. Make user actions explicit. Preserve state. Treat remote UI as data crossing a trust boundary.

But keep an adapter between your agent and your rendering system. The interface standards are still moving.

## Payments are not one protocol

The payment layer is where the acronym pile becomes truly political.

AP2 and x402 both matter, and they solve different problems.

AP2 is about authorization, intent, accountability, and payment method neutrality. Google describes it as a framework for users, merchants, and payment providers to transact across payment types. Its mandate model matters because agentic commerce breaks the old assumption that a human is directly clicking buy on a trusted surface. If the agent buys something while the human is absent, the system needs proof of what the user authorized.

x402 is about resource payment at the HTTP layer. It is closer to “this API, file, page, or tool costs money. Here is how the client pays and receives the resource.” Powerful for machine-to-machine activity. An agent should be able to pay a few cents for a data source, an MCP tool call, a paid API, a document, a benchmark run, or a temporary resource without opening an account and negotiating an enterprise contract.

Those are adjacent but not identical.

AP2 cares about the commercial trust chain, which means mandates and purchase authority. x402 cares about programmatic settlement, which means HTTP-native metering for resources.

The contested part is that neither lives alone. Stripe has agentic commerce, Shared Payment Tokens, UCP or ACP support for sellers, and machine-payment flows. Stripe’s surface is the one to study most carefully, because its agent-to-link authorization flow is the clearest worked example of treating agentic commerce as a human-trust problem rather than a settlement problem. Mastercard has Agentic Tokens. Visa has Intelligent Commerce. American Express has its Agentic Commerce Experiences developer kit. PayPal is supporting AP2 and building its own agentic commerce layer. Coinbase originated x402. Cloudflare is pushing it into a broader web infrastructure story.

Not a clean winner-take-all standards race. Payments never are.

Payments have issuers, networks, wallets, acquirers, merchants, fraud systems, chargebacks, identity, consumer protection, compliance, and liability. Protocol purity loses very quickly to settlement reality.

For builders, the answer is not to bet the company on one payment protocol this quarter. The answer is to separate your payment architecture into three concepts:

User intent: what did the user authorize?

Payment instrument: how is money actually moved?

Merchant or resource settlement: how does the seller or service know it has been paid?

AP2 is highly relevant to the first question. x402 is highly relevant to the third question for programmatic resources. Stripe, card networks, wallets, and payment processors sit across all three in different ways.

One layer the framework hides is geography. Payments are not uniform across markets, and most agentic payment protocols carry American assumptions about which methods customers reach for, how comfortable they are letting software transact on their behalf, and how often they expect to reauthorize. Consider a customer who has handed an agent a long-running task and does not want to be pulled back into the loop every thirty minutes to refresh an authorization token. A protocol that defaults to short-lived tokens may feel responsible to a US compliance team and intolerable to that customer, who simply wants the agent to keep working. Micropayment behavior is the other quiet default. Several of these protocols assume humans will not transact in fractions of a cent, which is fine until the agent population starts paying for resources at machine cadence. Opinionated defaults are not bad. They are inherited choices. The builder’s job is to know which ones came along for the ride.

If your agent does not touch money, do not overbuild this layer yet. If your agent does touch money, do not treat “agent can pay” as a button. Treat it as an audit problem. Who authorized the spend? Under what limits? For which merchant? With which payment credential? What if the agent retries? What if the cart changes? What if the resource is not delivered? What if the user disputes it?

The payment protocol is not where the work ends. It is where the liability begins.

## The stack that is actually forming

The working version I would use today is straightforward.

The core agent stack:

1. MCP for tools, data, and context.
2. A2A for agent discovery, delegation, and cross-agent coordination.
3. AG-UI for human interaction, supervision, state, and control.

The still-contested or domain-specific layers:

1. A2UI and related generative UI systems for safe structured rendering.
2. AP2 and similar systems for human-authorized agentic commerce, including network-specific frameworks like Mastercard Agentic Tokens and Visa Intelligent Commerce, Stripe’s Shared Payment Tokens, and OpenAI and Stripe’s Agentic Commerce Protocol.
3. x402 and similar HTTP-native systems for machine-native resource payments and API/tool metering.

This does not mean the second group is less important. In some businesses it will be more important. If you are building agentic commerce, payments are the whole story. If you are building a user-facing agent workspace, generated UI may become central. If you are selling paid data or paid APIs, x402 may be the most interesting thing in the list.

But if you are building a general agentic product, start with the first three layers. The universal shape of agent work is settling there.

The agent needs to reach systems.

The agent needs to coordinate with other agents.

The user needs a way to remain in control.

If those three are weak, everything else becomes harder. Payment cannot save an agent that cannot understand its tools. Generated UI cannot save an agent that cannot preserve state. A2A cannot save a system whose human approval flows are unusable.

## The strongest objection

The strongest objection is not that protocols may disappear into big platforms. That will happen. Most users will not know which protocol is underneath Gemini Enterprise, ChatGPT, Claude, Copilot, Salesforce, ServiceNow, Snowflake, Stripe, or Cloudflare. They will experience products. The protocol layer will disappear into the interface, the same way most people use OAuth without thinking about OAuth.

The harder objection is fragmentation.

Maybe MCP becomes the thing OpenAI and Anthropic converge around for tools, while A2A and AP2 remain more Google-shaped. Maybe OpenAI’s Apps SDK, ChatKit, and Connector Registry pull builders into an OpenAI-native surface. Maybe Anthropic’s Skills, Claude Code, and MCP connectors create a different center of gravity. Maybe enterprise platforms such as Salesforce and ServiceNow support open standards at the edge while keeping the most valuable agent behavior inside their own clouds.

That objection is real. It is also why the layer map matters more than the acronyms.

Even fragmented standards discipline the integration surface. They force builders to ask where tool semantics live, how one agent advertises capability to another, where user approval is represented, and how payment authority is proven. The protocols matter most where the work crosses a boundary that one vendor cannot fully own: a Salesforce agent calling a ServiceNow agent, a Google agent paying a merchant through a wallet or card network, a Claude or ChatGPT workflow reaching a company’s internal tools, a data agent returning governed context to a customer-facing app.

The protocol does not have to be visible to shape the market.

If MCP becomes the common way tools are exposed, then tool providers have to decide how to publish MCP servers, how to scope permissions, how to price tool calls, and how to prevent abuse. If A2A becomes a serious way agents discover each other, then companies have to decide what capabilities their agents advertise and which requests they accept. If AG-UI or something like it becomes the common way agent state flows into applications, then frontend teams have to design for long-running, interruptible, stateful work instead of ordinary chat.

Those are not implementation details. They are product strategy.

## What to do this week

The practical move is to stop asking which acronym wins and start mapping your agent to the layers.

Pick one workflow you actually want an agent to complete. Not a demo. A real workflow. Something like vendor intake, monthly close review, customer renewal prep, sales territory analysis, internal support triage, prototype deployment, product research, or procurement.

Take renewal prep for a B2B software company. The CSM wants an agent to prepare the renewal packet before a customer call. The MCP layer is Salesforce for the opportunity, Snowflake for usage and product telemetry, Google Drive or Notion for account notes, Slack for recent internal discussion, and Stripe or the billing system for invoices and payment status. MCP answers the access question: what systems can this agent actually use?

The A2A layer is narrower. The renewal agent probably should not own billing authority or legal interpretation. It may need to ask a finance-owned billing agent for unpaid invoices, a support agent for open escalations, or a legal agent for nonstandard contract language. The AG-UI layer is where the CSM sees the packet being assembled, approves whether billing context should be included, edits the risk narrative, and decides whether the draft goes to a manager. A2UI might matter if the agent renders a contract-diff card or usage chart. AP2 and x402 probably do not matter for this workflow. The framework is useful because it tells you which layers are central and which are not.

**Then answer six questions:**

1. What tools and data does the agent need? That is your MCP layer.
2. What other agents, services, or specialists does it need to call? That is your A2A layer.
3. Where does the user approve, edit, interrupt, or steer the work? That is your AG-UI layer.
4. Does the workflow need structured UI beyond text? That is your generative UI layer.
5. Does the agent need to spend money, authorize a transaction, or create a commercial obligation? That is your AP2 or agentic-commerce layer.
6. Does the agent need to pay for an API, resource, file, model call, or tool call programmatically? That is your x402 or machine-payment layer.

That exercise will tell you more than another standards-war article.

Most teams will discover that they are over-focused on model selection and under-specified on the operating surface around the model. They will know which LLM they want to use, but not which tools the agent can see. They will have a prototype that calls APIs, but no interaction model for user approval. They will imagine multiple agents coordinating, but no Agent Card, no task boundary, and no audit trail. They will talk about payments, but have not separated user intent from payment method from settlement.

The real work lives there.

## The thesis

Agents are moving from impressive demos to operating systems for work. That move requires interfaces between agents and tools, agents and other agents, agents and humans, agents and UI, and agents and money.

The first three layers are converging faster than the rest. MCP is becoming the default mental model for tool and data access. A2A is becoming the default for agent delegation across boundaries. AG-UI is the clearest open candidate for keeping long-running agents visible, steerable, and interruptible inside applications. A2UI, AP2, and x402 matter, but they sit in layers where product requirements, trust boundaries, payment rails, and platform incentives are still being negotiated.

The builder mistake is to treat all six as equal bets. The buyer mistake is to ignore all six because the acronyms are annoying. The better posture is to build against the stable shape of the stack and keep adapters around the contested layers.

Watching I/O today, I am less interested in any one new agent demo and more interested in how Google stitches these layers together. Does Gemini Enterprise become the place where A2A agents, MCP tools, A2UI interfaces, and AP2 payments feel like one operating model? Does Google make the agent stack feel less like a pile of standards and more like a product surface? Does it give developers the missing primitives for identity, permission, observability, and UI control?

That is the real question.

Not whether agents can talk.

Whether the stack around them is becoming legible enough that agents can actually work.

![](https://substackcdn.com/image/fetch/$s_!1tAn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6357221-36f1-461d-8119-f40dd2caf69d_1254x1254.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/agent-protocol-stack-mcp-a2a) on 2026-05-21T15:23:07-04:00*

YOUTUBE TRANSCRIPT
Google I.O. opens today, May 19th. There will be a ton of agent demos, I can guarantee you that. I will get into coverage for Google at another time. The more interesting story is what is happening underneath Google I.O., including in many of the protocols Google is putting out

I want to talk today about six agent protocols that have launched in the last year and how they underlie agentic systems. Why do we do that? Because it turns out the substrates for agents actually shape the customer experience. What are those six? MCP, A2A, AGUI, A2UI, AP2, and X402. It's not Star Wars robots. It's actually real protocols.

And if you're building an AI agent product right now, that list is really hard to wrestle with and understand. It feels like a standard scrum. New acronyms are popping up all the time. There's new diagrams. There's new claims that some missing piece of the agent stack has been solved with a new protocol. Here is my read.

Three of the six that I just named are becoming the actual agent stack. The other three are very much in contested layers that we need to be honest are still under debate. So we're going to talk about all six today and we're going to talk about the But before we get into which three are the standard,

I want to lay out the overall landscape for agentic protocols. What are the questions that we're trying to answer with agentic protocols? I want to suggest three for you. Keep those three in mind because they shape the customer experiences that we're trying to drive at the end of the day, whether we're building for internal or external customers,

and they also help us to understand what really matters when there's a bunch of standards out there. Now, three of those six protocols directly map onto those three questions. MCP, that's a tool and data layer. It's the protocol an agent uses to discover and invoke the systems where your work lives.

A to A, that's an agent coordination layer. It's the protocol one agent uses to discover and delegate to another agent across product or company boundaries. AGUI is a human interaction layer. It's the protocol that lets a long-running backend agent share state and events and approvals and interruptions with a user-facing app.

The other three protocols, A2UI, AP2X402, they all sit in a different spot in the stack. A2UI is about how agents render structured interfaces. AP2 is about authorizing agent-led purchases. X402 is about machine-to-machine payment at the HTTP layer on the web. All are really important and all are still contested or very domain specific.

I break down all six protocols layer by layer on the Substack with Source Links, Name Partner List. If you want the full version, you know where to get it. We're going to move on in this video to MCP, perhaps the most popular and most well-known protocol stack in AI.

MCP won Mindshare first because it solves the most immediate pain in agentic building. An agent sits in a chat box and has no access to tools and cannot do work, right? It can only advise, it can summarize, it can draft. It's a 2024 world. The work itself lives somewhere else. It lives in GitHub, it lives in Slack,

it lives in Drive and Postgres and Stripe and Linear and Salesforce, in some internal API, in a calendar. Before MCP, every integration with all of the tools I just named looked like custom glued to your chatbot, right? You had to have tool definitions and authentication patterns and parameter schemas and error handling all written from scratch every time.

The beauty and power of MCP is that it standardizes all of that. A server exposes tools The model receives a usable description of what can be done, new capabilities composed without every single agent platform rebuilding every connector. Cloud Desktop supports local MCP servers and so do most of the other agent tools out there.

There are more than 14,000 MCP servers now. And it's tempting to treat MCP as if it makes tools safe just because it's a standard across the internet. It doesn't. Tool access enables arbitrary code execution and arbitrary data access. And that's good because MCP is designed to allow agents to use tools in arbitrary ways to get tasks done.

That's the reason it was created. But that also means that MCP was created for a high trust environment and we now have to think about how we configure security and security stances around a tool using agent experience. MCP was not designed for that at root,

and so there are other challenges that we have to solve if we are trying to build secure agents. You know, Invariant Labs has already published research on what they call tool poisoning attacks, which are malicious that can hide inside tool descriptions, that can be exposed via MCP,

and those malicious instructions can influence an agent through the very metadata that's supposed to make the tool discoverable. So tool access is not a feature toggle. even though it's treated that way in a lot of user interfaces now. It is a security boundary that you're crossing. If your team is shipping MCP servers,

you still need scopes and approval flows and audit trails and a real answer to which tools the agent can see in which context. MCP does get the agent close to the work. It does not decide whether the agent should do the work. And if you're interested in digging into the security side of things,

the Substack piece goes deep on the Invariant Labs tool poisoning research, what that means for how we design our scopes, how we design our approvals. If your team's already running MCP servers, you definitely need to dig into that topic. You need to understand what you're exposing.

For now, we're going to move to A to A and the delegation layer. So MCP gets agents reach, right? The second problem arrives the moment the agent actually starts working. So the agent can't know everything. It can't own every capability. A procurement agent will need a supplier agent. A travel agent needs a hotel agent.

A finance agent may need a tax agent. A software agent may need a security reviewer. In fact, I know it does. Work is distributed across owners and permissions and domains and expertise. No one agent does it all. So A to A turns that distribution into something that agents can reason about.

And the important primitive in that stack is the agent card. A remote agent publishes a card that describes what it is, what it does, which skills it exposes, where it can be reached, and how another agent ought to interact with it. The Agent Card is the first version of an operating contract.

It has real terms and real interfaces and real responsibility. Google launched A to A with a bunch of partners, right? With Atlassian and Box and Cohere and MongoDB and PayPal and Workday, more than 50. The list matters because A to A only works if agents really can cross product and company boundaries.

So you want a world where you have discoverable delegation for agents, not just a bunch of swarms that look good on paper. But there's a cost here. Coordination isn't free. A to A adds another surface where you can have latency and failure and permissions and observability issues. If an agent asks another agent to do work,

it certainly makes the agent's workflow more flexible, but it also makes it less predictable. So A to A isn't the right answer for every product. A single product with a small set of tools may not need agent coordination at all. The right question to ask is whether this workflow requires delegated expertise or authority outside the primary agent.

If the answer is yes, you need to think about what that looks like ahead of time. Decide what your agent can say about itself. Decide what it can Decide what it can't share. Decide what requires human approval. Decide how a downstream result gets validated. The Agent Card is Google's attempt to make part of that process standard,

but it's still missing a control layer. And that's where we get to AGUI. Now, I know it's easy to underestimate AGUI because most people who hear about it think it is about driving the user interface. I don't think that's the best reading. I think a better reading is that AGUI helps us to ensure trust in agentic workflows.

An agent that's long-running, that's non-deterministic, and that's capable of touching external systems needs a lot more than a final answer for a human to see. Humans need to be able to to observe that agent as it works, approve sensitive steps, correct course, inspect state, understand why the agent is waiting.

And traditional web apps are just built for call and response. They don't really handle the streaming work that agents do. They don't handle the fact that agents may discover new information mid-task. The chatbot experience is not enough for that, and neither are most traditional apps. So AGUI is the open candidate for the human control layer.

The docs talk about what agent apps actually need, right? Streaming, shared state, front-end tool calls, So they'll wire a model to tools, they'll wire up a nice chat component, and then they'll discover what their agent is really doing. and then they'll say, oh no, we need approval buttons. Oh no, we need logs. We need a progress spinner.

None of those things by themselves are fixes for the root issue, which is about finding the right control points, understanding what the agent is trying to do, understanding what it's waiting for, and then figuring out where the user needs to approve or deny or edit or cancel. So AGUI belongs with MCP and A2A in the core stack,

even if the specific protocol is earlier in the adoption curve. AGUI itself may win that race, maybe a close cousin does, but the point is that an agent that can't show its work becomes supervision debt for humans and this is a way to address that and actually at root think about the

control problem for agents and build systems that allow humans to interact at the right moments with running agent workflows. Now if AGUI is new for you, if you want to dive deeper, the Substack piece gets into All the elements in the ecosystem, it talks about AGUI with LangGraph and CrewAI and Amazon Bedrock AgentCore and

PydanticAI and Mastra and CopilotKit. If you're picking a framework, that's where you want to dive in and look. Now, we need to get to the other three protocols, the one that I said weren't part of the core stack, because we need to understand why, because they won't tell you they're not part of the core stack.

Every protocol thinks it's a standard. Why are these not standards, and what does that tell us about the state of the agent race? So the other three are A2UI, AP2, and X402. A2UI is Google's project for agent-generated interfaces. Instead of sending arbitrary HTML or JavaScript from a remote agent, which is frankly a security disaster waiting to happen,

A2UI sends a structured declarative UI representation. The client renders using trusted components. The agent asks for components from an approved catalog. It cannot execute arbitrary interface code. And that is absolutely the right direction to be running in. But it's much narrower from a solution space than the human control problem that AGUI is solving.

A2UI is just one piece of the overall rendering question. and it doesn't try and establish a whole user control layer like AGUI. And so that's why I see A2UI as being useful and helpful for driving some kinds of generated experiences, but maybe not as focused on the substrate that many,

many agents will need to drive successful workflows in the new agentic economy. AP2, meanwhile, is Google's agentic payments protocol. Sixty-plus collaborators jumped onto this. You might think that makes it a standard, but not in payments. The collaborators include Adyen and American Express and Coinbase and MasterCard and PayPal and Salesforce and UnionPay

The key mechanic here is what's called the mandate, a cryptographically signed proof of what the user authorized. AP2 is trying to answer the most difficult question in agentic commerce. How does the ecosystem know the agent was authorized to buy? Meanwhile, X402 is Coinbase's HTTP native payment protocol. Cloudflare has adopted it.

The use case is very much agent-to-agent payment for resources. An agent buys an API call or a data source or a document or a benchmark run, and it doesn't have to set up an account. or negotiate a subscription. So AP2 and X402 are very much adjacent, but they're not the same thing.

AP2 is about commercial trust and user authorization, and X402 is about how do you settle payments for resources for agents. And this is not the end of the story. The protocol pile gets really big with payments because payments are a very valuable space to be in. If you're interested in diving deeper,

I did an entire video recently on Stripe and its role in the payment space. That is definitely a video you want to check out if you're looking at payments and agent protocols. They've done a phenomenal job understanding that you are driving human trust in agentic commerce.

And that is why their suggested experience of just sending an agent to a link to get an authorization token feels so smooth. So the protocols are going to keep piling up in the payment space, even beyond Stripe. You have MasterCard with agentic tokens, Visa with Intelligent Commerce, American Express has an agentic commerce experiences developer kit.

Paypal is supporting AP2, but is also building its own commerce layer. The payment space is so valuable, everyone wants to jump in. And if you're a builder right now, I would encourage you to think in the customer-obsessed way that you see from recent Stripe launches. Because what you want to do is think about,

for my customers who have to trust agents, how do I ensure that the payment space is something that they feel they can participate in, authorize an agent to transact in, and feel good that their wallet is secure, the payment is authorized, the payment will be completed, and their order will be done as they expected.

And so don't look at payment protocols in particular as just a technical choice. They're very much a customer experience choice. Okay. Stepping back here, how do you think about how substrates shape the customer experience and how do you think about wrestling with them and getting into that problem space if you've been

assigned to ship an AI strategy or make an AI agent or complete a workflow with AI agents? First and foremost, I've talked about this before, get into the specifics, understand what you're really doing. Are you tackling support triage or procurement or sales territory analysis? Are you doing customer renewal prep? What are you actually doing?

Understand that and then start to ask, how does the substrate we are talking about shape the agentic experience for the customer? The MCP layer is absolutely going to be part of the conversation in most cases because you're going to want to have the option to bring that agent close to the work.

The A to A layer is narrower, but can be very important if you're trying to understand how agents need to reason across other agent workflows. The AGUI layer is where you want to think about the ability to handle human approved long running agent workflows. So for example,

where the CSM might see a packet being assembled for the customer and might need to approve whether billing context should be included on the fly. Now, something like A2 UI might matter if the agent renders a particular usage chart or particular contract chart that helps someone understand what the agent is producing,

and you want some control and some guarantee that those components are real. And in this world, you need to be going through and asking yourself how your specific workflows map to the specific nuances of those protocols. And I'll give you an example from payments. So payments are complicated because payments are unique in different geographies.

And one of the things that's really interesting about the payments experience with agents is that you have to blend in multiple competing protocols with multiple competing geographies. So there's a whole gnarly customer experience. There's a bunch of competing substrates. And if you want to put together an experience that is competitive, of the United States.

It is up to you to understand that a given payments experience may be biased toward the United States, toward US payment methods. A given payments experience may be biased towards an assumption that humans will not I think that one of the things that I want to encourage you to do is to look at the

things that may seem boring about these protocols, things like how fees are handled, things like how returns are handled, things like how delivery is handled, things like how authorization is handled and how long authorization runs for. and recognize that those have real customer implications. If your customer is not comfortable reauthorizing and you have a short-term token

that you're driving for payment authorization and your customer just wants it done and doesn't want to reauthorize every 30 minutes, you're going to have a very frustrated customer on your hands. And that may be built into the protocol as a friendly default because it assumes a different customer.

So protocols can be opinionated and that's okay, but you have to think about what that means for you. And I prepared six questions to help you start to dig into that. Number one, what tools and data does the agent need? Does the agent need to get into the MCP layer? Find out, right?

Number two, what other agent surfaces or specialists does it need to call, right? That's the A to A layer. Three, where does the user need to approve or edit or interrupt or steer the work? That's the AGUI layer, the control layer. Does the workflow need structured UI beyond text? That would be number four.

A2 UI would help there. Number five, does the agent need to spend money? Does the agent need to authorize a transaction? Maybe that's an AP2 use case. Number six, does the agent need to autonomously pay for a resource programmatically? Maybe that's X402. Maybe it's something else. In general,

most teams are over-focused on model selection and they're very under-specified on the operating surface around the model. They know which LLM they want. They don't know which tools the agent can or should see. They may have a prototype that can call APIs, but they don't have an interaction model for user approval. They can imagine multiple agents coordinating,

but they don't have any way to enforce or validate that. The actual work lives in those kinds of questions. So I know we began this video talking about Google I.O. There's going to be a lot of agentic demos. I want you to watch at Google I.O. for one thing.

Does Google make the agent stack feel like a single operating model. Does Gemini Enterprise stitch A2A agents and MCP tools and A2 UI interfaces and AP2 payments into something a builder can ship against? Or does IO give us a new set of standards, another two or three standards to add to the pile?

Because this is a year where the agent stack needs to stop being a list of acronyms and needs to start being really, really buildable. and the companies that figure out how to build against the protocol stack in ways that shape customer experiences, they're gonna be the ones that win, right?

And we're gonna look back in six months and realize that because agent workflows for developers unlocked in the first half of 2026, this was a golden time for building what really mattered. Now, if you want to dive into those six questions and how you understand how to think

about agentic workflows with an eye on the customer and an eye on how these protocol substrates drive the customer experience in detail, I get into all that on the Substack, right? We'll talk about Salesforce and Snowflake and Drive and Slack all how they operate at the MCP layer.

We'll talk about billing and legal agents at the A to A layer. There's a dive on CSM facing approval surfaces at the AGUI layer and how you think about that. So if you want to get a quick start on copying some of those pieces for your team, You can grab that link. It's great.

I hope that this dive into the substrate of agents has been helpful. It may not feel sexy to talk about why agent substrates drive customer experiences, but it's profoundly impactful and it's something I don't see So I thought it was important to lay it out,

lay out the standards really clearly and help you understand how to think about these standards and of course the next one that's going to come along next week. I'll see you on the next one. Cheers.