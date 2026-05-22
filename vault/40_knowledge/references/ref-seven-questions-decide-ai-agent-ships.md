---
title: "Seven questions decide whether your AI agent ships. Most teams can answer two."
source: "https://natesnewsletter.substack.com/p/agent-infrastructure-control-layer"
author:
  - "[[Nate]]"
published: 2026-05-19
created: 2026-05-21
description: "Watch now | The model is one piece of the agent economy. The control layer is the other, and most proposals on a CIO's desk have no answer for it."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management]
ai-context: "Nate Jones on the seven infrastructure-control-layer questions that decide whether an AI agent ever ships to production — most teams can only answer two."
---
A new class of company has taken up position around the agent economy, and they are the ones who decide whether your agent gets to ship. They do not build models. They are not on most teams’ AI stack roadmap. But every serious production agent has to pass through them, and most agent proposals on a CIO’s desk right now have no answer for what those companies are about to ask.

The model is one piece of the agent economy. The control layer is the other.

The control layer is the set of infrastructure decisions that determine whether a model’s output is allowed to act in the world. Where does the agent live. What state does it remember. Who is it acting for. When does it need approval. What can it spend. Who can stop it. None of those questions get answered by a model. They get answered by the companies sitting between the model and your production system, and the last six weeks have made it obvious who they are. Cloudflare ran Agents Week. Stripe expanded its Agentic Commerce Suite. Okta launched Okta for AI Agents and expanded it again this month. Auth0 has been publishing AI Agents docs. Datadog has been turning LLM observability into something that looks a lot more like an agent control plane than a logging product.

I’ve covered the protocol stack already — [the six protocols that emerged and the three that decide which agents survive](https://natesnewsletter.substack.com/p/agent-protocol-stack-mcp-a2a). This piece is about the operators sitting above the protocols. The companies turning agentic behavior into controlled, permissioned, auditable infrastructure. The companies your security review is about to discover the hard way.

**Here’s what’s inside:**

- **The seven-row control map** I would put in front of any agent proposal before it touches a production system, and the one question per row that flushes out the gap.
- **Why Cloudflare, Auth0, Snowflake, Stripe, and Datadog** are becoming the operating system of the agent economy, and what each one is actually trying to own.
- **The kill switch most teams do not actually have**, even though they think they do — and the five layers it has to be implemented at to be real.
- **A real data leader’s failure mode**, live this quarter: her agents are routing around the human permission structure, and she now owns three questions she did not yet know how to answer.
- **The three prompts paid subscribers get this week.** A control-map fill-in for the agent your team is most likely to ship this quarter, a pressure-test for the next vendor pitch on your desk, and a five-layer kill-switch audit for the agent that actually scared you.

The boring layer is where the power is moving. Let me walk you through the map.

## LINK: Grab the prompts

The seven rows of the control map are not theoretical. They are the questions your security review, your CFO, your data leader, and your incident postmortem will eventually ask. These three prompts close the distance between an agent proposal that demos well and an agent that survives a real production rollout. The first walks one of your actual workflows through all seven rows and tells you which row will fail first. The second runs a vendor pitch or internal proposal through the same lens — what the pitch answers, what it dodges, and what each dodge will cost. The third is for the moment in the kill-switch section where you noticed your current stop button only works if the agent agrees to stop. None of these are generic strategy prompts. Each one ends with a filled-in artifact you can hand to a specific owner and act on this week.

## Compute is not control

Compute is necessary. It is not sufficient.

A model can generate a plan. It cannot, by itself, decide whether the plan is allowed. It can infer what a user might want. It cannot prove that the user authorized a purchase. It can ask to query a database. It cannot know which rows the user is entitled to see. It can draft an email, but whether sending that email creates a legal or customer obligation is not a question the model is positioned to answer.

The gap is between intelligence and work.

The first phase of the AI boom rewarded model access. Who had the best model? Who had the cheapest inference? Who had the context window, the multimodality, the reasoning score, the coding benchmark, the agent demo?

The next phase rewards controlled agency.

Controlled agency is the ability to let software act in the world without turning every action into a human supervision tax. It requires a runtime with state, governed data, identity and delegated authorization, commercial authority if money is involved, and observability with a real kill switch.

That is the control layer.

The infrastructure story is changing. The hyperscaler may provide the raw compute. The model lab may provide the reasoning engine. But the company that owns the control layer can decide whether the agent is usable in production.

## The runtime control point: Cloudflare

Cloudflare is interesting because it is not trying to win the model war in the obvious way. It is trying to become a place where agents can run.

Cloudflare’s [Agents SDK documentation](https://developers.cloudflare.com/agents/) is unusually revealing. It says real agents need to remember conversations, act on schedules, call tools, coordinate with other agents, and stay connected to users in real time. Each agent runs on a Durable Object: a stateful micro-server with its own SQL database, WebSocket connections, and scheduling. The agent can use tools, serve tools through MCP, schedule tasks, run workflows, coordinate with sub-agents, browse the web, talk to users, and react to events.

Hosting with memory, execution, and coordination built in. An agent runtime.

The control point is state plus execution. If agents are long-running workers rather than stateless chat completions, then the runtime matters much more than it did for ordinary web apps. An agent needs to wake up later, remember what happened, continue a stream after disconnect, accept a human approval, run a scheduled task, call a tool, retry a workflow, or stop when a policy says stop.

Cloudflare sits in a strategically useful place for that. It already lives close to traffic. It sells global infrastructure, security, workers, stateful objects, gateways, and edge execution. Agent workloads need exactly the kind of infrastructure that makes “where does this run?” less separate from “how is this controlled?”

Cloudflare is not the only company trying to occupy that runtime position. AWS has made the same control-layer claim inside its own cloud with [Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/), which packages runtime, memory, identity, gateway, browser, code interpreter, and observability services. Vercel is coming from another angle with [AI Gateway](https://vercel.com/docs/ai-gateway/), where the control point is model routing, budgets, monitoring, load balancing, and fallback across providers. Runtime control is splitting into several operator jobs: where the agent runs, how state persists, how tools are mediated, and how failures are observed.

The x402 work makes the point even clearer. Cloudflare’s [x402 docs](https://developers.cloudflare.com/agents/agentic-payments/x402/) describe a flow where a service can respond with 402 Payment Required, the client signs a payment payload, the server verifies or settles the transaction, and the resource is returned. The same docs describe charging for HTTP content and MCP tools. That is a runtime company moving into machine-native economic coordination.

Control surfaces compound. If Cloudflare runs the agent, mediates the connection, exposes or protects the tool, observes the request, and helps charge for the resource, it moves from infrastructure beneath the product into the product’s operating system.

The practical implication for builders is that agent runtime should not be an afterthought. If your agent has durable work, deadlines, callbacks, streaming UI, tools, approvals, payments, or state, the runtime is a strategic choice. A stateless API wrapper is not an agent platform. It is a demo path.

## The identity control point: Auth0 and Okta

Identity becomes much harder when software acts on behalf of people.

In the ordinary SaaS world, identity mostly meant authenticating a human user and authorizing that user against application resources. In the agent world, that is not enough. The agent may be acting for a user, for a team, for a company, or for another agent. It may need to call Google, Slack, GitHub, Salesforce, or internal APIs. It may need to request approval while the user is away. It may need to retrieve documents for a RAG pipeline but only those the user is allowed to see.

Auth0’s [AI Agents documentation](https://auth0.com/ai/docs/intro/overview) is worth reading as strategy rather than product docs alone. Auth0 is explicitly packaging user authentication, OAuth-based API access, Token Vault, asynchronous authorization, and fine-grained authorization for RAG. The key phrase is not “login for agents.” The key idea is delegated authority with constraints.

An agent should not get a broad, permanent credential because a user once signed in. It should call APIs on behalf of a user, however token storage should be opaque to the agent itself. Consent should be required for sensitive or long-running operations, and document retrieval should respect what the user is allowed to see.

That becomes a control layer because enterprises will not deploy serious agents without it.

The most dangerous agent in a company is not necessarily the most capable one. It is the one with fuzzy authority. It has access to a user’s calendar, email, files, CRM, source code, and internal documents, but nobody can clearly say whether it is acting as the user, as the company, as an application, or as itself. The persistence of that permission is unclear. So is whether the approval covers this action or a broader class of actions, and whether the agent can pass data to another agent.

That ambiguity is manageable when agents draft text. It is not manageable when agents transact, deploy, refund, schedule, provision, or make commitments.

Okta’s broader enterprise agent-security push points in the same direction. So does WorkOS, which has been explicit about giving [AI agents their own scoped credentials](https://workos.com/blog/ai-agent-credentials) and about its partnership around [Microsoft Entra Agent ID](https://workos.com/blog/workos-partners-with-entra-agent-id). AWS is making the same move inside AgentCore Identity. The identity providers understand that AI agents are becoming identity-bearing actors. The company that can register them, scope them, authorize them, revoke them, and audit them has a real control position.

The builder implication is blunt: every serious agent product needs an authority model. A login is only one piece of that model. Who is the principal, what can be delegated, what can be revoked, and what does the audit log show. If those questions are not answered, the agent will hit a ceiling in any enterprise environment that actually reviews what it deploys.

## The data control point: Snowflake

Agents are only as useful as the data they can safely interpret.

Snowflake’s agent strategy becomes more than “AI on data” at this point. Snowflake’s [Cortex Agents documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) describes agents that orchestrate across structured and unstructured data, plan tasks, use Cortex Analyst for structured data, use Cortex Search for unstructured data, and select the right tool to ensure governed access and compliance with enterprise policies.

That is a mouthful, but the strategic point is simple: the agent needs more than data access. It needs governed meaning.

Data warehouses and data clouds became important because they became places where organizations tried to create a reliable version of business truth. Revenue. Customers. Inventory. Usage. Churn. Margin. Forecast. Territory. Support volume. Claims. Risk. Supply. The numbers matter because decisions move around them.

Agents make that semantic layer more important, not less.

A generic agent can query data badly. It can join the wrong tables, trust the wrong column, misunderstand a metric, retrieve stale documents, answer confidently from ungoverned context, or present an assumption as a fact. That is not a model problem alone. It is a data control problem.

Snowflake’s position is that the agent should operate inside the governed perimeter of enterprise data — routing between structured and unstructured sources through tools that understand the environment, using semantic models, semantic views, Cortex Search, Cortex Analyst, and custom tools, and respecting the roles, policies, and existing governance the company already enforces.

That makes Snowflake a control-layer company because it can answer a question model providers cannot answer from the outside: what does this business object mean inside this company?

Databricks is making the parallel argument from the lakehouse side. Its [Mosaic AI Agent Framework](https://www.databricks.com/product/artificial-intelligence/mosaic-ai-agent-framework) is about building, deploying, evaluating, and monitoring agents inside the same governed environment where enterprise data and ML workflows already live. BigQuery and Gemini represent the hyperscaler-native version of the same move. These companies are doing more than adding chat to databases. They are trying to make the governed data platform the place where agents are allowed to reason and act.

What is ARR? Which customer hierarchy is authoritative? Which data is restricted? Which answer can be trusted?

In the agent economy, the semantic layer is not reporting infrastructure. It is action infrastructure. An agent that cannot tell current revenue from forecast revenue should not be allowed to draft the board narrative. An agent that cannot distinguish an approved supplier from a prospect should not be allowed to place an order. An agent that cannot tell public documentation from confidential customer commitments should not answer support questions directly.

The data platform that owns the governed meaning of the business owns a large part of the agent’s operating boundary.

## The payment control point: Stripe and the networks

The moment an agent touches money, the control problem becomes unavoidable.

Stripe’s agentic commerce work is strategically deeper than “agents can buy things.” Stripe’s [agentic commerce documentation](https://docs.stripe.com/agentic-commerce) separates seller flows, agent flows, product catalogs, shared payment credentials, and machine payments. It also distinguishes commerce protocols such as UCP or ACP from machine-payment protocols such as MPP or x402.

That separation matters because agent payments are not one job. A human may want an agent to buy from a merchant. A machine may want to pay for an API, data source, or tool call. A seller may need fraud protection because a bot and a legitimate buyer’s agent can look similar. A wallet may need to pass payment credentials without exposing raw credentials to the agent.

Stripe already lives at the intersection of payment credentials, merchant onboarding, fraud, billing, subscriptions, issuing, treasury, disputes, risk, and developer APIs. Agents make that intersection more valuable.

But Stripe is not alone. The card networks are moving because they understand the same control point.

Mastercard’s [Agent Pay announcement](https://www.mastercard.com/us/en/news-and-trends/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai.html) introduced Mastercard Agentic Tokens, building on tokenization systems already used in mobile contactless payments, card-on-file, Payment Passkeys, recurring expenses, and subscriptions. The strategic phrase is that agentic transactions need trust, security, and control.

Visa says its [Intelligent Commerce](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21961.html) work has already produced controlled, real-world agent-initiated transactions with partners, including consumer and B2B pilots. American Express describes its [Agentic Commerce Experiences developer kit](https://www.americanexpress.com/en-us/company/agentic-commerce/) as a suite of services for agent registration, account enablement, intent intelligence, payment credentials, and cart context.

Adyen, PayPal, Worldpay, Coinbase, and others show up in Google’s AP2 partner list for the same reason. Payment processors, wallets, risk systems, networks, and merchant infrastructure companies all see the same bottleneck: the agent can only spend at scale if the system can prove intent, preserve credentials, route payment, manage fraud, and resolve disputes.

Those are payment features, but more importantly, they are control claims.

The networks are saying: if agents are going to spend money, the payments ecosystem has to recognize legitimate agents, validate intent, protect credentials, preserve dispute rights, manage fraud, and keep issuers, merchants, and consumers inside a trusted system.

That is the right instinct. Agentic commerce will not scale because a model learns to click checkout. It will scale when the payment ecosystem can tell the difference between an authorized agent, a malicious bot, a mistaken purchase, a changed cart, a delegated budget, a merchant-specific token, and a disputed transaction.

Payment moves money, but its strategic role is institutional trust.

The company that owns that trust owns one of the most important control points in the agent economy.

## The hidden control layer is observation

Runtime, identity, data, and payment are the obvious control surfaces. The hidden one is observation.

Agents will fail differently from ordinary software. They may call the wrong tool with valid syntax, ask the right agent the wrong question, or retrieve authorized data and still draw the wrong conclusion. A run may complete the task technically while violating the user’s intent, stay inside permission boundaries while creating an expensive loop, keep retrying when it should escalate, or escalate too late when it should have stopped. Most dangerously, an agent can succeed in the tool layer and fail in the business layer — every API call green, every outcome wrong.

That means logs are not enough.

Companies need to observe agent runs as work rather than plain API traffic. What was the goal? Which tools were called? Who authorized the action? Which data sources were used? Which policy blocked the action? Which cost was incurred? Did a human accept the result?

This is where infrastructure companies can quietly gain power. Datadog’s [LLM Observability](https://www.datadoghq.com/product/ai/llm-observability/) is built around tracing prompts, responses, retrieval steps, and tool calls, then correlating that behavior with backend services, infrastructure, and user sessions. LangSmith’s [observability and evals platform](https://www.langchain.com/langsmith-platform) is closer to the developer and agent-framework layer, with traces and evaluations tied to LangChain and LangGraph workflows. [Braintrust](https://www.braintrust.dev/) and [Langfuse](https://langfuse.com/docs/) make different operator bets: evals-first quality control in one case, open-source tracing, prompt management, and evaluations in the other.

AWS is also making the integration point explicit. AgentCore Observability supports OpenTelemetry and can send agent telemetry into CloudWatch, Datadog, LangSmith, and Langfuse. That is the shape of the market: agent observability will not be one dashboard. It will be a control plane that connects traces, cost, tool calls, evals, security events, and business outcomes.

A gateway that sees model calls, routes providers, applies rate limits, caches responses, logs usage, and enforces policies becomes the place where agent behavior is made legible. Cost savings are a side effect. Control is the product. A payment processor that sees fraud and transaction patterns across merchants can distinguish good agents from bad automation. An identity provider that sees delegated authorization flows can govern who can act through whom.

The agent economy needs dashboards, but not in the shallow sense. It needs control surfaces that answer operational questions: where the agents are, what they have access to, what they cost, which actions are blocked, and which ones should be shut off.

That last question is underrated. The kill switch belongs in the product spec, not the principles deck.

It should be implemented at more than one layer. A runtime can cancel or pause the run. An identity system can revoke the credential. A gateway can block the tool call. A payment system can freeze the instrument or spending limit. A graph-based agent framework such as LangGraph can interrupt a workflow before a sensitive node. If the only kill switch is “tell the model to stop,” the kill switch is not real.

## The strongest objection

The strongest objection to this argument is that hyperscalers still own the real advantage.

They own the clouds. They own the model distribution. They own developer platforms. They own data centers. They own the enterprise contracts. They are integrating agents directly into productivity suites, cloud consoles, databases, security products, and app platforms.

That is true.

The harder version of the objection is that hyperscalers already own their own control layers. Microsoft has Entra, Azure, GitHub, Teams, Copilot, and security telemetry. AWS has IAM, Bedrock, AgentCore, CloudWatch, and the customer workloads themselves. Google has Cloud IAM, BigQuery, Gemini, Workspace, Chrome, A2A, A2UI, and AP2. If the control layer is runtime, identity, data, payment, and observability, the hyperscalers are rebuilding it inside their own clouds.

But it does not eliminate the control-layer thesis. It makes it more important.

Hyperscalers will own a lot of the agent economy because they own a lot of the existing enterprise environment. Microsoft can push agents through Office, Azure, GitHub, Teams, Copilot, and Entra. Google can push through Gemini, Workspace, Cloud, Android, Chrome, A2A, A2UI, and AP2. Amazon can push through AWS, Bedrock, marketplaces, fulfillment, and the operational backbone of the internet economy.

But agents do not live inside one vendor’s boundary forever. The more useful the agent, the more tools, clouds, apps, merchants, APIs, documents, databases, and payment systems it crosses. A company may run workloads on AWS, sell through Shopify, bill through Stripe, store customer data in Snowflake, authenticate through Okta, observe production in Datadog, and let employees use ChatGPT, Claude, Gemini, and Copilot. A control layer that only works inside one hyperscaler is powerful, but incomplete.

There is a second objection: the model labs are moving down the stack too. OpenAI’s [Responses API](https://platform.openai.com/docs/guides/responses-vs-chat-completions?api-mode=responses.html) is agentic by default, with hosted tools and remote MCP support. Anthropic has pushed Claude toward [skills, computer use, Cowork, Claude Code, and MCP support](https://support.claude.com/en/articles/12138966-release-notes). The model provider wants to become the runtime because it can make the model feel more capable when the surrounding tools, state, and workflows are native. That is the most predictable move in the market.

It still does not erase the infrastructure layer. It makes the buying question sharper. Use the model-native runtime when speed, model fit, and product simplicity matter most. Use cross-model, cross-cloud infrastructure when portability, governance, procurement, security review, or vendor risk matter more. Most serious companies will end up with both.

The last objection is lock-in. If Cloudflare runs the agent, Datadog is the only place where behavior is legible, or Stripe becomes the default commerce authority, each control layer becomes a new dependency. The mitigation is architectural: keep the runtime portable where possible, bring your own identity provider, export telemetry to a second sink, separate payment intent from payment rail, and keep audit logs in a system the business controls.

Who authenticates?

Who authorizes?

Who carries the token?

Who validates the payment?

Who observes the run?

Who can stop the agent?

Those questions create openings for infrastructure companies outside the model race. Not because they beat the hyperscalers at compute, but because they sit at unavoidable points of institutional trust.

The model produces intelligence. The control layer turns intelligence into allowed work.

Here is what that looks like in a concrete stack.

Imagine a renewal-quote agent at a regulated B2B software company. The runtime is Cloudflare Workers with Durable Objects for state, or Bedrock AgentCore if the company is standardized on AWS. Auth0, Okta, Entra, or WorkOS handles delegated identity. Snowflake or Databricks owns the governed customer-data layer. Stripe or Adyen handles quote-attached payment credentials and billing events. Datadog, LangSmith, Braintrust, or Langfuse observes the run. A production agent quickly becomes a map of control responsibilities across multiple operators.

That is why the vendor distinction matters. Cloudflare is a runtime and network-control operator. AWS is the hyperscaler-native runtime operator. Auth0, Okta, Entra, and WorkOS are authority operators. Snowflake and Databricks are governed-data operators. Stripe, Adyen, PayPal, Visa, Mastercard, and American Express are economic-trust operators. Datadog, LangSmith, Braintrust, and Langfuse are observability and evaluation operators. The model lab is one operator in that map. It is not the whole map.

## The agent control layer map

Use this table before approving an agent deployment with any AI product, vendor, or internal agent proposal.

![](https://substackcdn.com/image/fetch/$s_!-xKE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F857e97a5-660d-4b89-92a5-f62f83a35f7e_1168x732.png)

Most agent proposals are over-specified on model and under-specified on control. They will tell you which model they use, how many tools they can call, and how impressive the demo looks. They will not tell you who owns the approval path, where the agent’s authority expires, whether the payment credential is scoped, whether the data retrieval respects row-level access, whether the workflow can be paused, or who can reconstruct the run after something goes wrong.

That is backwards.

For a toy agent, model quality is the question. For a production agent, control architecture is the question.

## What to do this week

Block 60 minutes this week and pick one agent workflow your team is actually likely to ship this quarter. Not your entire AI strategy. One workflow.

For example: a sales agent preparing renewal recommendations, a finance agent analyzing monthly variance, a procurement agent comparing suppliers, a support agent drafting refunds, a coding agent provisioning infrastructure, or a marketing agent buying data and producing a brief.

Fill out the seven rows of the control map for that one workflow. Keep the exercise concrete:

- Where does the agent run?
- Which data is governed?
- Who is the principal?
- Which actions are read-only, draft-only, approval-required, or autonomous?
- What can it spend?
- Which events are logged?
- Who can shut it off?

If any row says “TBD” or “we will figure it out later,” that is the row where the agent will fail in production.

The next step is not necessarily to buy more tools. It is to assign ownership. Take the weakest row to its owner. Runtime to the platform or infrastructure leader. Identity to security. Data governance to the data leader. Payments to finance or the payments owner. Observability to engineering and operations. The question is simple: who owns this Monday morning?

Many companies will stumble here. They will treat agents as a product or productivity initiative and discover too late that agents are a cross-functional infrastructure problem. The CIO, CISO, CFO, data leader, product leader, and business owner all have part of the control surface.

Agents do not respect org charts. Your governance model has to compensate.

I was talking recently with a data leader who told me her agents had started routing around her existing permission structure, which had been designed for humans. A run would complete successfully, and she would be left with three questions she did not yet know how to answer. Was the agent allowed to work around the permission layer to get the job done? Did the human end up seeing data they should not have? Was the original permission structure simply wrong for this kind of work in the first place? There is no neutral answer to any of those. Each one is a decision someone has to own. That is the shape of the control problem when it actually shows up: not at the demo, at the post-mortem.

## Where control concentrates

Cloudflare, AWS, and Vercel are turning runtime, state, gateways, model routing, and machine payments into agent platform infrastructure. Auth0, Okta, Entra, and WorkOS are turning delegated identity and authorization into an agent safety layer. Snowflake and Databricks are turning governed enterprise data and semantic models into an agent action layer. Stripe, Adyen, PayPal, and the payment networks are turning payment credentials, fraud, mandates, tokenization, and settlement into agentic commerce infrastructure. Datadog, LangSmith, Braintrust, and Langfuse are turning traces, evals, cost, and tool behavior into the observation layer production agents require.

These companies may not all win equally. Some products will be early. Some standards will be replaced. Some protocols will fragment. Some demos will be ahead of customer readiness. That is normal.

The direction is what matters.

The model is not the whole product. The browser is not the whole product. The chatbot is not the whole product. The real product is the system that lets intelligence act inside boundaries a company can trust.

That system needs somewhere to run, something true to know, someone to act for, authority to touch the world, and a record of what happened.

That is infrastructure.

And in the agent economy, infrastructure is the control layer.

![](https://substackcdn.com/image/fetch/$s_!W9oW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8db0e815-0c67-48b0-abee-0f9811dffa6c_1254x1254.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/agent-infrastructure-control-layer) on 2026-05-21T15:22:24-04:00*

YOUTUBE TRANSCRIPT
There are companies that get to decide whether your agent actually ships or not. And they're probably not the ones you're thinking of. I bet you're thinking of OpenAI or Anthropic. No, no, no. What about Cloudflare? Cloudflare ran Agents Week last month. What about Stripe? Stripe rolled out its Agentec Commerce Suite or Okta.

Okta launched Okta for AI agents at the end of April and has continued to expand it since. Auth0 has been building out its AI agents documentation. Datadog has been quietly building out its LLM observability platform. None of these companies build models. None of these companies are on most teams' AI stack roadmaps,

but all of them are going to decide whether your AI agent gets deployed in production. So the model is one piece of the agent economy. The infrastructure companies, the ones that decide where the agent runs, who it's acting for, what it can know, what it can spend, and who can stop it,

those companies own effectively the infrastructure that controls whether an agent reaches production. And the control layer, the infrastructure layer that drives agent success, is where a lot of AI power is moving. So let's dive in. First, I want to talk about compute and how compute is not the whole story.

So the easiest AI infrastructure story is the physical one. And I've told it in other videos, so if you're interested, dive in. I've talked about GPUs and data centers and power and memory and networking and CapEx, and that story is real. But the physical infrastructure only determines whether AI can be served at scale.

If the power isn't available, the model doesn't serve, right? Once agents start doing work, the next bottleneck is whether the intelligence you can generate is governable. Where does the agent run? What does it remember? Who is it acting for? When does it need approval? What can it spend? And of course, who can stop it?

Those kinds of questions must get answered by infrastructure, not by a model. So compute is really important to scale agents as we start to talk about a full agentic economy, but it's not sufficient. Now, I've talked about protocols before. I have a whole article on Substack I've got to read

I've talked about six key protocols for the agent layer recently. This video is about the layer underneath those protocols. Who is building the infrastructure that makes those protocols come to life? And the first layer I want to talk about underneath So a model is stateless. You send a prompt, you get a response,

the conversation is over unless you send the history back next time. And that is perfectly fine for chat. But it doesn't work for an agent that has to remember what happened and wake up later and continue after a disconnect and run on a scheduled task and recover from

a tool failure or stay connected to a user in real time. Real agents need a runtime with memory and execution built out. And that's why Cloudflare is building agents SDK. Every agent runs on what Cloudflare calls a durable object, a stateful microserver with its own SQL database, its own WebSocket connections, its own scheduling.

The agent can call tools, it can serve tools through MCP, it can schedule tasks, it can coordinate with sub-agents, it can browse the web, it can react to events. And Cloudflare is not alone here, right? AWS is making the same control layer claim inside its own cloud with Amazon Bedrock Agent Core,

packaging runtime and memory and identity and gateway and browser and code interpreter and observability into a stack. Vercel is coming at a little different angle with AI Gateway where the control point is model routing and budgets and monitoring and load balancing. So there's some different bets here, but it's the same thesis.

So runtime is becoming a control surface in its own right. If your agent has durable work or or deadlines or callbacks or streaming UI or tools or approvals or payments or state, and most production agents tackle those kinds of tasks, then runtime is something that you have to decide intentionally.

It belongs at the top of your control map because it shapes the rest of the environment your agent operates in. Now we move to the next layer, the identity control point. Auth0, Okta, WorkOS, Entra. Let's sort of understand what this means. It's a huge topic. In ordinary software,

identity means authenticating a user and authorizing that user against application resources. The user logs in, the app checks the permissions, the work proceeds. That model breaks when an agent acts on behalf of a person. The agent might be acting for one user or a single team or a company or another agent.

The APIs it calls might span Google or Slack or GitHub or Salesforce. You get the idea. Approval often comes asynchronously while the user is away and when the agent retrieves documents from a RAG pipeline, only some of those documents are the ones the user is allowed to see.

Auth0 is tackling this complexity by building this layer in public. Their AI agents' docs cover user authentication, OAuth-based API access, token vault, asynchronous authorization, and fine-grained authorization for RAG. The mechanic is delegated authority with constraints. An agent does not get a broad permanent credential just because a user decided to sign in once.

Instead, it calls APIs on behalf of the user. Similarly, token storage doesn't expose secrets to the agent. The agent has to ask for consent for sensitive or long-running operations. And RAG queries only retrieve documents the user is actually authorized to see. Now Auth0 is not the only player here. Okta, WorkOS, Microsoft Entra Agent ID,

and AWS Agent Core Identity are all sort of converging in the same problem space. Because the dangerous agent in a company is not necessarily the most capable one, it's the one with very fuzzy authority. where nobody can clearly say whether it's acting as the user, as the company, as the application, or as itself.

And nobody knows whether the permissions persist across sessions or cover a class of actions beyond the original request. That's all manageable when agents draft text. It is not manageable when agents transact and deploy and refund and schedule and provision or make serious commitments on their own. A serious agent product needs a serious authority model.

Who is the principal? What can be delegated? What can be revoked? What does the audit log show? If those questions aren't answered, your agent is going to hit a ceiling in any serious company. The full operator landscape, I put that over on Substack. You can dive in

into Auth0 and Okta and WorkOS and Entra Agent ID and AWS Agent Core Identity. And you'll get the whole list on Substack of what each one is trying to control and a clear protocol for how you pick an identity provider, which is an extremely So if you want to dive in there deeper, that's where you find it.

We're going to keep moving, though, to the data control point. And that's where we talk about companies like Snowflake or Databricks. Agents are essentially only as useful as the data they can safely interpret. A generic agent fails at data in predictable ways. It joins the wrong tables, it trusts the wrong column, it misunderstands a metric,

it receives stale documents, it answers confidently from ungoverned context, it presents an assumption as a fact. One of those is a data control failure. The model is doing what it can with the data it sees, and the data it sees hasn't been governed for agent use. Snowflake's bet on the data control point is very specific.

Their Cortex Agents docs describe agents that work across both structured and unstructured data. Cortex Analyst handles structured queries, Cortex Search handles unstructured retrieval, and the agent routes between them. All of that happens inside Snowflake's governance perimeter. And so the key thing that they want you to take away is that they are governing the distribution of meaning.

Because a data warehouse is really where companies try to build a reliable meaning, right? A version of business truth, whether that's around revenue or customers or inventory or churn and agents make that semantic layer, that meaning making, more important, not less. What is ARR? Which customer hierarchy is authoritative? Which data is restricted? Which agent do I trust?

An agent that can't tell current revenue from forecasting? That's not the one that should be drafting the board narrative, right? You shouldn't have that in production. What about an agent that can't tell public docs from confidential customer commitments? They shouldn't be answering support questions directly, should they? So that's the problem space that Snowflake is going after.

Databricks is going after a similar problem and making a parallel argument with its mosaic AI agent framework. around building, deploying, evaluating, and monitoring agents inside the same governed environment where enterprise data already lives. BigQuery and Gemini are the hyperscaler native version of this same move. These companies are doing more than adding chat to databases.

They're trying to make the governed data platform the place where agents are allowed to reason and act. And if your business has a semantic layer, and almost all of them do, even if it's informal, your agent needs to be operating inside that layer's governance, not around it.

This all matters because if your business has a semantic layer, if it has a data layer that helps you make meaning of business metrics and customer relationships, and most businesses do, then your agent needs to be operating inside some kind of governed permission structure. And that's sort of what Databricks and Snowflake are going after.

Okay, let's move on to the payment control point, Stripe and the networks. The moment an agent touches money, the control problem becomes really, really critical. Now the protocols themselves, if you want to understand them, I dive deep on AP2 and X402 and others in a different video. I want to focus now a layer above the payments protocol.

I want to focus on the operator side. Stripe sits at the center of all this, not because of any single protocol. Stripe supports several of them, but because Stripe already lives in the middle of agentic commerce. Payment credentials and fraud and disputes and risk and billing and subscriptions and issuing and

and merchant onboarding and all of the developer APIs underneath all of that. Agents make every one of the intersections I just named very valuable and Stripe is the company best positioned to play across that bundle and it is moving extremely aggressively to to outline the pathways for agents to handle all of what I just described, issuing payments,

authorization, fraud mitigation. Stripe is coming for all of that with agents, and it's doing so because Stripe Nate believes that the future is a larger internet economy with a lot of agentic commerce going on. And so it makes sense for them, since they're on a mission to grow the entire internet economy,

to go after the agentic part of that economy and make sure that they enable that and set that up so it's easy to transact. That's the larger vision for Stripe and that's why you see them making these moves across all of these agentic pieces as an operator at the center of this network across multiple protocols.

The card networks are operators in the protocol space but they have a very different set of incentives than Stripe. Stripe is looking to grow the economy as a whole but the card networks need to make sure agentic payments run on their rails and that's true for MasterCard and Visa

and American Express and so they're competing on something different from a protocol perspective. They want to prove and show that an agent transaction can run on their rails and clear the same institutional trust chain a card transaction can clear. And that's how they think about fraud and dispute and merchant onboarding and everything else. That's a different bet.

So the payment ecosystem is dominated by operators who move above particular protocols and have differing motivations, but have the same And the payments ecosystem for agents is going to have to evolve quickly. That's part of why operators are moving quickly, because they know from experience with other payment products that if you don't

quickly move to enable legitimate patterns of transaction, you get fraudulent patterns of transaction, and that becomes a big issue. So the reason payments matter is that payments essentially are a form of institutional trust. And the company that is able to facilitate that institutional trust owns one of the most important control points in the Asian economy.

And if you are building in that space, if your agent is going to touch money, you have to be thinking about which of these partners you are working with in order to enable that experience. And right now, unless you are in a special jurisdiction and it's extra complicated, the default is probably strike.

In most cases, for most startups, that is the default. And if you're an enterprise, you may have your own payment stack. Amazon has its own payment stack. There are others that do as well. Regardless, you have to be thinking about whether you are investing in your own payment stack

and extending it to provide the agentic capabilities that you see from Stripe and others, or whether you're going to partner with them and build customer experiences that are that rich because these big operators are playing in the space and providing the rails on which a Gentic Congress can run. Next big theme for shipping production agents, observation.

This one's easy to underrate because it sounds like you're logging. That's not what this is. You're not just logging. Agents fail differently from ordinary software. They call the wrong tool, but they might call it with valid syntax. They ask the right agent, but they might ask it the wrong question.

They can retrieve authorized data and they still draw the wrong conclusion. They might complete a task technically while violating the user's intent. They can stay inside permission boundaries and still create a very expensive loop in terms of tokens. They keep retrying, maybe they escalate too late. Logs by themselves don't catch those sophisticated

What you need is a way to observe agent runs as work, not as API traffic. What was the goal of this work? Which tools were called for this work? Who authorized the action? Which data sources were used? Which policy blocked that action? Which cost was incurred? Did a human accept the results?

Infrastructure companies can gain real power at this layer. Datadog has been building LLM observability. It traces what the agent did end-to-end, prompts going in, responses coming back, tool calls, retrievals, and it connects all of that to the backend services and user sessions sitting around the agent. Langsmith sits closer to the developer side.

If your team is building on Langchain or Langgraph, Langsmith is where you trace the agent's workflow and run evals against it. BrainTrust and LangFuse are taking very different bets here. BrainTrust leads with evals, running quality checks against agent output. LangFuse is more of an open source tracing option. And AWS, they're just interested in wiring all this together.

Agent Core Observability supports open telemetry, which means you can send agent telemetry into CloudWatch and Datadog and LangSmith or LangFuse from one single place. So in this situation, the market is converging toward a single control plane. One more thing, the kill switch. The kill switch is absolutely a product feature and it has to be

The payment system might freeze the payment instrument or or hit a spedding limit, a framework like LandGraph can interrupt a workflow before a sensitive node is hit, right? So if the only way to tell your agent to stop is to just tell the model to stop, you don't have a kill switch.

Look at all the nuance in what I just described. So I'm going to go into kill switch architecture in the Substack piece as well, how to implement it at runtime, how to think about identity and gateway and payment and framework layers so that tell the model to stop is not your only option. You can dive into that.

But for now at this level, I want to leave you with what you can think about for this week. And I want to suggest, as I often do, that you start somewhere specific. Take a support refund agent or a customer email support agent or a claims agent or an agent that reads conversations and checks usage.

Pick a specific agent workflow. Then understand these seven things. Where does the agent run? What is the runtime layer? Is it Cloudflare? Is it Agent Core? I don't know. Who is that agent acting for? It needs an identity layer. Is it acting for the company? Does it have delegated access? That's Auth0 or Okta right there.

What can it know? Does it understand the data layer? Does it understand usage data and can it pull that in? Is that a Snowflake thing? What can it change? The tool layer. Where does it have read access? Where does it have write access? Where does it have approval? What can it spend? That's the payment layer, right?

Does it have refund limits, approval thresholds? Are you working with Stripe? What gets observed? Look at the observability layer. Did the agent issue a refund that violated policy? Did it get tricked? Now you're talking about Langsmith. Maybe you're talking about AWS or Datadog. And then who can stop it? Where's the kill switch? Can runtime cancel?

Can payment freeze? Can identity revoke? How do you do that? Fill all of that out for this one workflow. If you have a TBD on one of those rows, you need to tackle that before it gets to production. And you need to have owners for these because otherwise someone is just going to

say it's someone else's problem how to solve agent identity and then you're going to find you never solved agent identity and now you're launching and that's a problem. Agents do not respect org charts. Your governance model has to compensate for that. I was talking recently with someone who leads a data team and what she was

observing to me is that there are cases where your agents can literally hack around your existing permission structure inside your internal system because it was designed for humans and it can come back and the agent may have done a successful run and it did so outside of the permission structure and this is a problem for her

from the data perspective because she needs to figure out whether the agent executing that run was authorized to work its way around the human permission structure or whether that agent was acting inappropriately and showed data to the human that it shouldn't have and there's multiple layers to that because like one

you could say well the agent shouldn't have worked around the problem Two, you could say the human shouldn't have seen the data. Three, you could say, you know what, maybe the agent was goal-oriented in a positive way, but we need to give it better tools to solve the problem.

Four, you could say the agent was allowed to do that and we're okay with that degree of chaos. And there are a surprising number of companies that do that, but I think that that's going to become a riskier and riskier stance to take as agents get more capable. So these are real challenges.

You run into these control layer issues more as agents get more capable inside your systems, and it's often platform teams that face it first. If we step back for a minute, look, the AI economy is going to keep consuming much more compute over time. So the hyperscalers are still going to matter. NVIDIA is still going to matter.

Models, they're going to continue to get better. But none of that decides how your agent actually ships. None of the things I just named. Instead, the companies that decide whether your agent's successful are the ones that are building the layer that determines whether agents can act. And I've named a bunch of them here.

I've talked about Cloudflare and Auth0 and Snowflake and Stripe and Datadog. that this control layer helps teams figure out which control surfaces they need to enact, engage, build on in order to actually ship agents this year. Now, if you want to see an example of how you work through a workflow with all of those control points named,

all seven questions answered, I wrote that out on Substack in full. where the agent runs, who it's acting for, what it can spend, what gets observed, who can stop it. If you want to copy it for your team, you can go grab it. Otherwise, thank you for tuning in.

We are digging into agents because if we don't understand agents well, we are going to end up in a situation like my friend on the data team who's trying to figure out whether or not the agent that hacked around the authorization to get the data pull done is doing the right thing, the wrong thing,

or something in between. These are stories I'm hearing all over the industry. They matter a ton. I'll see you soon. There will be more AI News tomorrow. Cheers.