---
title: "The next AI platform winner won't have the best model. They'll own something most companies don't even see yet."
source: "https://natesnewsletter.substack.com/p/ai-work-primitives-access-vs-meaning?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-05-05
created: 2026-05-07
description: "Watch now | Why access without meaning is the most expensive mistake in AI right now."
tags:
  - "source/web-clip"
  - "nates-newsletter"
  - "ai-product-strategy"
  - "job-hunt-2026"
type: reference
status: processed
domain: [product-management, claude-mastery]
ai-context: "Nate's Newsletter (2026-05-05) — access vs. meaning as the next AI platform fight: why semantic control beats computer-use reach, the Stripe/Salesforce/SAP/Perplexity comparisons, and three diagnostic prompts for evaluating AI products."
---
Agents can finally use computers like humans do — open browsers, click forms, move calendar invites, run commands. The spectacle is real. It is also a distraction.

Every AI product announcement in the next year will look like progress. Most will be progress on access — the agent can now reach one more thing. A smaller share will be progress on meaning — the system actually understands what it is doing. Demos make the two look identical. Six months into a real deployment they feel completely different: access-only products are still demanding constant supervision, and meaning-rich ones are quietly compounding. If you are building, buying, or betting on AI tools right now, the difference between those two categories is the most important call you will make this year.

Computer use exists because most software was designed for human interpretation — and a person knows that moving a calendar invite is not just changing a row in a database. It may notify attendees, alter someone’s preparation, break a commitment, or reschedule a meeting that took three weeks to set. The agent can infer some of that. Inference over a human interface is not the same as software exposing the meaning of the work directly. That distinction is the next platform fight.

Computer use gives agents reach. Semantic control gives them judgment. The long-term moat is not the ability to click the button. It is ownership of the layer that tells the agent what the button means.

**Here’s what’s inside:**

- **Why coding agents arrived first.** The structural reason software development became the wedge — and what it tells you about which kinds of work agents will conquer next.
- **The Stripe move most people misread.** Why a structured payment token is strategically deeper than any agent that clicks checkout buttons.
- **The trap Perplexity is trying to escape.** Why moving from answering to operating is necessary but not sufficient.
- **The Salesforce vs. SAP wager.** Two opposite bets on agent-readability, and the buyer behavior that decides which one survives.
- **The better product test.** A single question to ask of every AI product announcement that cuts through the demo theater.
- **Three diagnostic prompts.** One to evaluate any AI product announcement against a ten-dimension semantic depth test, one to audit a tool already in your stack and decide whether to extend, wrap, replace, or wait, and one to run a structured post-mortem after an agent’s action succeeded but the outcome was wrong.

What follows is how the divergence is unfolding — and what to look for in the products you are evaluating, building, or betting on.

## LINK: Grab the prompts

Six months into a deployment is when access-only products and meaning-rich ones start to feel completely different. By then you have already paid for the difference. These three prompts exist so you can run the diagnostic earlier — before you commit, while you still own a tool, and after something has already gone wrong.

The first one runs any AI product announcement, demo, or vendor pitch through a ten-dimension test that scores it on action vocabulary, permission encoding, validation paths, and the other layers the article walks through. The second audits a tool already in your stack and tells you whether to extend, wrap, replace, or wait. The third is the one I reach for when an agent has already done something with a bad outcome — it classifies the failure into one of seven semantic gap categories and traces the root cause to a specific missing layer, not a vague “add more guardrails.”

They work in any AI assistant. They ask one question at a time. They are designed for the situation you’re actually in, not a clean hypothetical.

## How computer use gives AI agents reach

Computer use is important because the world is not going to rebuild itself around agents overnight. Enterprises are full of software that will remain human-shaped for a long time: internal dashboards, procurement systems, compliance portals, finance tools, shared drives, brittle admin panels, browser apps, desktop applications, Excel workflows, PDFs, government sites, half-documented internal tools, and strange little operational systems that only three people understand. If an agent cannot use a computer visually, it cannot reach most of this work. It would be trapped inside the handful of systems that already expose clean APIs or agent-ready connectors.

So computer use is necessary. It is a bridge technology for the messy middle period. It gives agents a universal adapter for software that has not yet become agent-native. That is why it feels magical. A user can say, “Go do this,” and the agent can attempt to move through the same interface a person would use. It can survive in the old world before the new one has been built.

But a bridge is not the destination. The broadest interface is usually the least semantically rich. A screenshot gives the agent a view of the screen, but not necessarily a structured understanding of the objects underneath it. A browser gives the agent access to nearly every web app, but not necessarily the domain meaning of the actions inside those apps. A desktop controller can click any button, but it does not automatically know whether that button is low-risk, reversible, financially material, customer-impacting, policy-sensitive, or dangerous. The agent can guess, but guessing becomes increasingly unacceptable as agents move closer to real work.

The better interface is usually narrower and more meaningful. A connector can tell the agent that this is a calendar event, not just a rectangle on a page. A payment protocol can tell the agent that this transaction is scoped to a merchant, amount, currency, and user approval, not just a checkout form. A code repository can tell the agent that this change is a branch, this object is a pull request, this check failed, and this merge is blocked. A project-management system can tell the agent that a task is blocked, assigned, overdue, dependent on another task, or waiting for review. These narrower interfaces matter because they expose semantics. They do not merely let the agent act. They tell the agent what kind of action it is taking.

The hierarchy matters. Agents should use the richest semantic interface available. They should fall back to computer use when that richer interface does not exist. This is not only an engineering preference but the strategic structure of the market.

## Why AI tool access isn't enough for agents

Without semantic meaning, you get bad calendar invites, decks that feel wrong in tone but no one can explain why, refunds issued to customers who should not have received them, and a thousand smaller failures where the agent got the action right and the meaning wrong. The button worked. The decision did not. That is the pattern I keep watching, and more access does not fix it.

A lot of the current discourse treats access as the thing that matters. The model needs access to tools. The agent needs access to the browser. The assistant needs access to your files. The enterprise needs to connect its systems. All of that is true, but it is incomplete. Access gets the agent near the work. It does not necessarily make the work understandable.

The next layer is meaning. Consider a support agent with access to a refund tool. Access tells the system that the button can be pressed. Meaning tells the system whether this particular customer is entitled to the refund, whether the amount falls within policy, and whether the action requires a human approver. The button worked. The decision did not. That is why the questions multiply once you start looking at any real action. What is the object? What action is being proposed? Who owns the object? Who is allowed to act on it? What happens if the action succeeds? What happens if it fails? Is the action reversible? Does it create external obligations? Does it touch money? Does it touch customer data? Does it touch production infrastructure? Does it violate policy? Does it require a human to approve? Can another agent review it? Can the system validate whether the outcome is correct?

Those questions are not abstractions. They are the difference between an agent that can perform a demo and an agent that can operate inside a company. The more clearly a system can answer them, the more autonomy it can safely support. The less clearly it can answer them, the more the human has to supervise.

“Trusted write access” is too small as a thesis. Trust is not a single switch. It is an architecture of scoped authority. An agent may be trusted to read but not write, draft but not send, stage but not deploy, recommend but not approve, spend under a threshold but not above it, change a sandbox but not production, or act autonomously in one domain while requiring explicit review in another. Those distinctions depend on semantics. If the system cannot distinguish the action, it cannot scope the trust.

The real primitive is not the mouse, the browser tab, the local file, or even the API. The real primitive is the meaningful unit of work. A refund. A reschedule. A pull request. A vendor comparison. A payment authorization. A compliance exception. A support escalation. A feature rollout. A deployment. A policy interpretation. A meeting brief. A memory update. These are the things agents need to understand. The human UI hides them behind buttons and forms. Agent-native software exposes them directly.

## Why coding agents work better than other AI agents

Coding agents became the first convincing general agents because software development already contains unusually rich semantics. A codebase is not just text. It has files, modules, dependencies, build commands, tests, type systems, linters, package managers, git history, branches, pull requests, CI checks, logs, staging environments, deploy targets, ownership conventions, review norms, and rollback paths. The environment is already structured in a way that lets an agent perceive state, act on state, observe feedback, and revise its action.

This is why coding agents feel different from ordinary chatbots. They are not only answering questions about a codebase. They can inspect the repository, edit a file, run a command, see the error, change the implementation, rerun the test, produce a diff, and hand the result back for human review. The loop works because the surrounding work system makes progress legible. The agent does not have to ask a human every thirty seconds whether it is on the right track. The environment itself gives partial answers.

This is adjacent to the older “make work verifiable” idea, but it is larger than verification. Verification is one piece. The deeper point is that software development has already externalized much of its work structure. A failing test has meaning. A diff has meaning. A branch has meaning. A pull request has meaning. A CI failure has meaning. A type error has meaning. A package vulnerability has meaning. A deployment has meaning. These are not just checks. They are semantic artifacts. They tell the agent what world it is operating in.

Most knowledge work is not yet like that. A strategy document may not have tests. A calendar may contain events whose importance is hidden in politics, relationships, and priorities. A sales process may depend on unwritten account context. A procurement decision may depend on budget timing, vendor history, policy exceptions, and risk tolerance. A compliance question may depend on knowing which document is authoritative, which precedent still applies, and which jurisdiction controls. Agents can assist in these domains, but the environment does not yet give them the same density of meaning that a codebase gives them.

Coding was the wedge — not because all work will become coding or because everyone will become a programmer, but because it shows what happens when work is sufficiently agent-legible. The next phase is not to turn every worker into a developer. It is to make more kinds of work legible enough that agents can participate without turning the human into a full-time supervisor.

## Codex as a work substrate

This is what makes Codex strategically interesting beyond coding. The product is not merely a better developer tool. It is a proving ground for the agentic work surface. The important pieces are not only model quality, speed, or polish. The important pieces are the surrounding primitives: connectors, plugins, browser use, computer use, scheduled tasks, background execution, memory, Chronicle-style ambient context, multimodality, review agents, and the product affordances that reveal capabilities at the right moment.

Each of these gives the model a way to bind intelligence to work. Connectors let it reach systems where state lives. Plugins package repeated capabilities into forms the agent can reuse. Browser and computer use cover the long tail of software that does not expose clean interfaces. Memory carries preferences and context forward. Scheduled work lets the agent operate across time instead of only inside a single chat turn. Background execution lets the user hand off work without watching every step. Auto-review begins to separate execution from oversight. Multimodality lets the agent interpret visual, textual, and structured information together.

The model is still central, but the model alone is not the product. A model’s capability remains latent until the product gives it a usable work surface. A model that can reason but cannot access the relevant system becomes a consultant. A model that can access a system but cannot understand action semantics becomes a risky operator. A model that can act but cannot validate becomes a source of review burden. A model that can remember but cannot distinguish personal preference from company policy becomes a governance problem. The surrounding product architecture determines whether intelligence turns into work.

Product craft matters enormously in this category. When a user types “Stripe” and the product surfaces a Stripe connector, that is not just a nice UI touch. It is the product mediating between user intent and available primitives. The system is beginning to say: you are trying to do something in a domain where I have a structured capability. Would you like to use that capability instead of improvising? That is a small example of the larger shift. The agentic product should not require the user to configure fifty things before getting value. It should progressively reveal the right semantic tools as the work calls for them.

This is also why Codex becoming useful to non-coders matters. The story is not simply that a coding tool found broader adoption. The story is that the coding environment may be the first place OpenAI is learning how to assemble a more general work substrate. Engineering workflows expose the pattern first because they are already highly structured. Once the product learns how to combine state, tools, memory, background execution, review, and permissioning in that domain, the same pattern can migrate into other kinds of work.

I want to be careful not to overstate this. The story is not that everyone becomes a developer. It is closer to the opposite. The structure is what matters, not the engineering. Whether the pattern actually travels is one of the open questions of the next year, and I would not bet the company on it yet.

## How Stripe builds agentic payment primitives

Payments make the semantic problem impossible to avoid. An agent that buys something on behalf of a user cannot just be given a credit card and told to click carefully through a website. That might work once in a demo, but it is not a foundation for agentic commerce. The system needs to represent user consent, merchant identity, amount limits, credential scope, fraud risk, fulfillment, refunds, disputes, and settlement responsibility. Money requires precise semantics.

That is why Stripe’s agentic commerce work is more important than an agent operating a checkout page visually. A visual checkout flow is a human interface. A payment token scoped to a merchant, amount, and time window is an agentic primitive. The first asks the model to imitate a person. The second creates a structured transaction that a model can participate in without receiving raw credentials or improvising through a form.

Stripe’s Agentic Commerce Protocol and Link wallets for agents are examples of semantic infrastructure. They convert agentic buying from “the model clicks checkout” into “the system passes a constrained payment credential through a defined flow.” The difference is not cosmetic. It changes who owns the risk, how user approval is represented, how merchants process orders, and how payment credentials are protected. The payment layer can say that this credential is single-use, limited, scoped, and tied to a specific purchase. That is the sort of meaning an agent needs if commerce is going to move beyond demos.

This is what a real work primitive looks like. It is not the surface interaction. It is the structured operation underneath the surface. Stripe does not need to own every shopping interface if it owns a critical semantic layer of agentic transactions. That is a much stronger position than building an agent that happens to be good at clicking checkout buttons.

## Perplexity and the search trap

Perplexity’s strategic problem is easier to see through this lens. Its original strength is answering. It retrieves information, synthesizes it, cites sources, and gives users a better research experience than traditional search for many tasks. That is valuable. But research is often upstream of work. People search because they need to decide, compare, buy, write, prepare, schedule, negotiate, code, invest, or act. If the product remains at the answer layer, it can influence the work, but it does not own the work primitives where state actually changes.

This does not make search unimportant. Search is one of the most important ways agents acquire context. A search-native system can become a powerful component inside an agentic workflow. The weakness is not context. The weakness is context without semantic authority over action. A research product can tell you what to do, but the value migrates toward the system that lets you do it safely, repeatably, and with the right permissions.

That is why Perplexity has to move toward Comet, Computer, and Personal Computer. It cannot stay only in the answer layer. It needs to get closer to the browser, the desktop, the user’s files, the user’s apps, and the workflows where research becomes action. Perplexity’s own positioning reflects this shift: Computer is framed as an independent worker that takes action across web and work context, while Personal Computer gives the Mac app access to local files, native apps, voice, and an always-on desktop experience. The scope of that move is significant. It is an attempt to move from answering to operating.

But proximity is only the first step. If Perplexity becomes a highly capable agentic shell over other people’s tools, it gains reach but may still lack durable control. It can help users operate Google Docs, Gmail, Slack, Stripe, GitHub, Linear, Salesforce, or ServiceNow. But those systems still define the deepest semantics of their domains. They know what a document is, what a payment is, what a pull request is, what a ticket is, what a customer case is, what a permission means, and what happens after an action is taken.

Perplexity’s real challenge is therefore not whether it can build a better AI browser or a better computer-using agent. It is whether it can convert proximity into semantic authority. Can it define a durable user-level or team-level work graph above the underlying apps? Can it broker meaning across systems? Can it create persistent project memory that becomes more valuable than any single tab? Can it turn search results into structured actions with permissioning, validation, and review? Or does it remain a brilliant operator of interfaces whose meanings are owned elsewhere?

The position is precarious. Perplexity is not wrong to move toward the computer. It probably has to. But moving toward the computer is not the end of the strategy. It is the move you make when the answer layer is not enough.

## The browser is close to work, but it does not own work

The browser matters because so much modern work has collapsed into it. Research, email, documents, dashboards, SaaS apps, shopping, calendars, project trackers, analytics, internal tools, and customer systems often live inside tabs. An agent inside the browser is close to a large amount of user context. It can observe what the user is doing, move across web apps, compare pages, summarize information, and perform multi-step workflows without leaving the place where much work already happens.

That makes the browser a natural agent surface. OpenAI’s Atlas and Perplexity’s Comet both point in this direction. The browser is not just a window onto the web. It can become the place where AI sits beside the user, reads context, and takes action. That is a real platform opportunity.

But the browser’s strength is also its weakness. It is horizontal. It sits across many domains, but it does not automatically own the domain semantics inside each application. The browser can see a support dashboard, but the support platform owns the meaning of a refund, an escalation, a customer entitlement, and a policy exception. The browser can see a calendar, but the calendar system owns recurrence, availability, attendees, notifications, and meeting state. The browser can see a GitHub pull request, but GitHub owns review state, branch protection, CI checks, and merge authority.

If applications expose rich agent interfaces, the browser can become a powerful orchestrator across domains. It can route intent through structured actions. If applications do not expose those interfaces, the browser becomes a clever operator of visual flows. That is still useful, but it is less defensible and less reliable for high-consequence work.

The browser war is therefore not only about which company gets closest to the user. It is about whether the browser can assemble cross-domain meaning. If the browser only controls the screen, its advantage may be shallow. If it can build a persistent representation of the user’s work, projects, permissions, memories, and actions across applications, then it becomes much more important. The browser is a battlefield because it is close to work. But closeness only becomes a moat when it turns into meaning.

## Why AI agent safety requires semantic infrastructure

Safety in agentic systems is often framed as a constraint on capability. The more an agent can do, the more careful we have to be. That is true, but it misses the more interesting point. Safety is not only a brake. It is part of the infrastructure that allows autonomy to increase. The better a system understands the meaning of actions, the more safely it can let agents proceed without constant human supervision.

This is why review agents and auto-review patterns matter. A primary agent may be optimized to complete the task. A review layer can evaluate whether the proposed action matches the user’s intent, obeys policy, and stays within acceptable risk. If the user asked to move a calendar invite and the agent tries to delete it, the reviewer should catch the mismatch. If the user asked for a vendor comparison and the agent tries to place an order, the reviewer should stop it. If the user asked for a staging migration and the agent touches production, the reviewer should escalate. If the user asked for a draft response and the agent tries to send it to a customer, the reviewer should require approval.

But review only works well when the environment exposes enough meaning. The review system can reason much better over “delete recurring external calendar event” than over “click this button.” It can reason much better over “refund customer above threshold” than over “submit form.” It can reason much better over “run command against production database” than over “type command in terminal.” Semantic richness improves both productivity and safety because the system can distinguish harmless actions from dangerous ones.

This is where the enterprise story becomes clear. Companies do not need agents that are merely more bold. They need agents that can operate inside permission structures. They need read-only modes, draft modes, staged writes, human-approved writes, auto-reviewed writes, and fully autonomous actions only in narrow, reversible, well-instrumented workflows. That is the architecture that makes autonomy possible.

## Memory is work infrastructure

Memory looks like a personalization feature until agents begin doing serious work. Then it becomes infrastructure. A memory is not simply a remembered fact. It is a future interpretation rule. It tells the agent how to understand a user, a team, a company, a workflow, or a jurisdiction the next time it acts.

Some memories are personal. A user may prefer concise drafts, explicit assumptions, direct tone, or a certain way of framing tradeoffs. Some memories are role-based. A product manager, finance analyst, compliance officer, and plant operator may each have different definitions of a good output. Some memories are team-level. A team may have its own templates, norms, metrics, architecture boundaries, and current priorities. Some memories are company-level. A company may have brand rules, security policies, approval paths, data classifications, and customer commitments. Some memories are jurisdictional. Work in India, Europe, or the United States may require different legal constraints, language expectations, privacy rules, and data-residency assumptions.

Those layers cannot be flattened into one blob called “memory.” The agent has to know which memory applies, who owns it, whether it is portable, whether it can be shared, whether it overrides another memory, and whether it must be forgotten. A personal writing preference cannot override a company compliance rule. A team habit may apply in one business line but not another. A prior employer’s proprietary context cannot simply become part of someone’s portable AI identity. But a person’s work style, judgment preferences, and communication habits may reasonably travel with them.

“Bring your own AI” becomes a serious enterprise question for this reason. If a personal AI learns how someone works, it becomes part of that person’s productivity. The employee does not want to lose it when changing jobs. The employer may want the employee to bring it because it raises productivity. But the employer also needs to prevent leakage, enforce policy, and distinguish portable work style from company-owned knowledge. This cannot be solved by vibes. It requires memory semantics: ownership, scope, authority, portability, retention, and conflict resolution.

Memory is another version of the same moat. The question is not just who remembers the most. It is who can classify memory correctly and apply it safely to work.

## Agent-native software is not a chatbot

The weak version of the software response is to add an AI chat pane to every product. The chat pane may be useful. It may answer questions, summarize records, draft content, and help users navigate the product. But a chat pane alone does not make software agent-native. It is still a human interface with an assistant attached.

Agent-native software exposes the work model underneath the product. A project-management system should expose not only tickets, but owners, dependencies, blockers, priority, deadlines, decision history, escalation paths, and completion criteria. A procurement system should expose vendor risk, budget authority, approval thresholds, contract status, substitution options, audit history, and reversibility. A support platform should expose customer entitlement, refund authority, escalation policy, account history, regulatory sensitivity, and outcome tracking. A document system should expose authorship, provenance, permissions, comments, redlines, approval state, and retention obligations. An experimentation platform should expose rollout stage, feature flag status, metric ownership, guardrail metrics, blast radius, and rollback options.

The point is not to make the human UI more complex. The point is to create a second surface. Humans need clear interfaces. Agents need clear semantics. The best software will provide both. It will remain simple and usable for people while making its underlying objects and operations legible to agents, review systems, and governance layers.

This distinction separates software that has AI from software that is ready for AI. Software that has AI can generate text inside the product. Software that is ready for AI can participate in agentic work. It can tell the agent what exists, what can be done, what each action means, what permission is required, how the result should be checked, and what happened afterward.

## The coming platform fight

Every software company will have to decide how much semantic access to expose and to whom. Expose too little, and generic agents will operate clumsily through the UI. Users will experience the product as hard to automate, and competitors with better agent interfaces may become more attractive. Expose too much, and the product risks becoming backend infrastructure for someone else’s agentic interface. The value may migrate to the agent that owns the user relationship, while the system of record becomes a commodity service underneath it.

This is the platform tension. Model companies want broad agents that can operate across domains. Browser companies want to orchestrate work across applications. SaaS companies want to preserve authority over their domain semantics. Payment companies want to own transaction primitives. Identity providers want to govern authorization. Enterprises want interoperability without losing control. Users want convenience without supervision burden.

The clearest live example of this tension is the divergence between Salesforce and SAP. Salesforce has moved aggressively toward agent-readability, treating its data model as something agents should reach through structured interfaces and standardized protocols. The bet is that a system of record stays sticky if agents can read and act on it cleanly, even when the user-facing experience lives somewhere else. SAP has gone the other direction, restricting how agents can operate against its environments and treating that distance as a form of protection.

Both positions are defensible on paper. I think Salesforce is more right than SAP. Locking agents out feels like protection, but it reads to me like a defensive posture that protects margin in the short term and erodes relevance in the long term. The long term is closer than most enterprise software companies are pricing in. If enterprise buyers begin evaluating software partly on how well it participates in agentic workflows, and there are early signs they will, the cost of being agent-hostile rises faster than the cost of being agent-permissive.

The fight will not look like one company simply “winning AI.” It will look like boundary negotiation across the stack. Which layer owns the user’s intent? Which layer owns the object model? Which layer owns permissioning? Which layer owns memory? Which layer owns validation? Which layer owns the audit trail? Which layer owns the feedback loop that improves future automation?

The companies that win will expose enough semantics for agents to be genuinely useful, but retain enough control that they are not reduced to a database behind someone else’s assistant. That balance will be hard. It is exactly the kind of balance that creates platforms.

## How to evaluate AI agent products

This gives us a better way to judge AI product announcements. The right question is not simply whether the demo is impressive. Demos are often impressive precisely because computer use makes agency visible. The better question is: what new work primitive did this product expose?

Did it create a real action vocabulary? Did it distinguish read, draft, write, approve, publish, refund, deploy, cancel, and delete? Did it encode permissions and thresholds? Did it expose risk classes? Did it create validation paths? Did it make actions reversible where possible? Did it produce logs that a human or another agent can review? Did it know which source of truth is authoritative? Did it separate user preference from team norm and company policy? Did it reduce human supervision, or did it merely create a more spectacular thing for the human to supervise?

Under this test, many flashy products look thinner. A model clicking through a website is useful, but it may not be defensible. A structured payment token is less cinematic, but strategically deeper. A browser agent is powerful, but a workflow system that exposes typed, permissioned, reviewable operations may own more durable value. A general computer-use agent can reach many tasks, but the product that defines the semantics of a high-value task may become the platform those agents depend on.

I love raw computer access. I love that agents are getting closer to file primitives and closer to actual work. I love MCP servers and the rest of the connector layer. Access is good. But access was the conversation in 2025. The conversation in 2026 is what the agent understands once it gets there. Those are different fights, and the second one decides who builds platforms and who becomes a feature.

The question to ask of every AI product is: does this merely give the model access, or does it give the model meaning?

## The thesis

The original thesis was that leverage in AI is a function of proximity to computing primitives. That is close, but it needs to be sharpened. Leverage is a function of proximity to meaningful work primitives. Raw computer access gets the agent near the work. Semantic control lets the agent do the work reliably.

Computer use is how agents survive in the old software world. It lets them operate human interfaces while the rest of the software industry catches up. It matters because the installed base is messy, and the long tail of work will not become agent-native quickly. But the durable moat is the semantic layer that makes work legible: the objects, actions, permissions, risks, validations, memories, and review paths that allow agents to act with less supervision and more reliability.

Codex matters because it is not only a coding product. It is a laboratory for the work substrate around models. Stripe’s agentic commerce work matters because it turns a checkout click into a structured transaction primitive. MCP matters as one early attempt to standardize how tools and context become accessible to agents. Browser agents matter but are not enough — they are close to the user, but closeness is not the same as semantic authority. And Perplexity’s move toward the computer is strategically necessary but incomplete. It must move beyond answers, but it also has to avoid becoming only a brilliant operator of other people’s interfaces.

The future is not an AI that clicks every button for you. That is the bridge. The future is software where the button is no longer the primitive. The primitive is the action behind it, fully described, permissioned, reviewable, reversible where possible, and composable across workflows.

Computer use gives agents hands. Semantic control gives the system a way to know what those hands are touching.

That is the moat.

![](https://substackcdn.com/image/fetch/$s_!YQcw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2e724b4-062c-4757-9a54-760d86cc315b_1024x1024.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/ai-work-primitives-access-vs-meaning?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-05-07T12:11:07-04:00*


YOUTUBE TRANSCRIPT

This is a piece about the strategy that we have to build as product leaders when we think about where agents play best. And what I'm asserting is that the work primitive is what really matters. And a lot of us are assuming that the agents

Nate’s ability to use the computer sort of levels the playing field because we can all sort of put our programs out there and the agent can use it or we can build an MCP server and it's just going to work. I want to suggest that there's a deeper strategy in play that some of the

hyperscalers understand and that need Needs to be more widely shared and understood Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’s The future is not an AI that gets really good at clicking buttons for you. That's the bridge. The real fight is over who defines what the button means.

Because once agents start acting inside companies, the question is not just can it click, Nate’s Nate’sletter Nate’sletter Nate’sletter Nate’sletter There are three layers to keep in your head. Access, meaning and authority. Those are all layers that agents can touch. Computer use lets agents access parts of the computer. Semantic work primitives gives agents meaning.

So there are three layers to keep in Nate’sletter So there's three levels, right? And that sounds abstract, so we're going to start with something really simple. Imagine an AI agent moving a calendar invite. I've had Codex do that. On the screen, that looks like changing a time and clicking save. But the action is not really click save.

It may notify five people. It may move prep time. It may break a commitment someone made to a customer. It may turn a private conversation into a meeting that now conflicts with something more important. The human sees a calendar event and brings all of that context with them. The software sees fields in a database, right?

The agent sees that it needs to fill out the calendar and just do the job. It doesn't necessarily understand the human intent behind the meeting. And the human intent behind the meeting making the And that's a big difference The same thing happens with checkout. A button that says buy is not just a button. It represents money,

user consent, tax, merchant identity, fraud risk, fulfillment, returns, card security, and maybe a dispute a few weeks from now. Or take deleting a file. Natesnewsletter Nate’ And right now we're kind of we're kind of getting hints of that. So the auto review feature in Codex basically is there to guard human intent and

ensure that the agent using the computer is actually using it to do the right task. I love it. It works pretty well, but it feels like an initial draft in that direction. Nate’s Instruction because it's very much a guardrail tool. It's there to guardrail the agent and keep it from doing something it shouldn't. That's good.

I want it to do its job. But that's different from positively ensuring that agents have the semantic meaning they need to really deeply understand my calendar. Calendars are complex things. Deeply understand the email context for a relationship I've had for three and a half years with someone when they write one message. That's a larger piece of context.

And look, I get it. Most of the world is not agent-native, and the fact that we have computer use is hugely helpful. The fact that we have jumped in just a few months to the point where it's useful is a godsend. Companies are full of software that assumes a human is sitting there interpreting everything, right? Boards,

Procurement Tools, Shared Drives, Government Websites, Excel Workflows, the whole thing, right? All of computing assumes a human will use it. If an agent cannot use a computer visually in that world, it cannot reach so much of our work. It is stuck inside the clean But, a universal adapter is typically a shallow interface.

A screenshot can show the agent what is on the screen, but it does not automatically reveal the structure underneath. A browser can reach almost every web app, but it does not automatically know the domain meaning of each workflow. A desktop controller can click a button, but it does not automatically know whether that button is reversible.

Whether that button is financially material or dangerous, If an agent is helping you summarize an article, then guessing is probably something you can fix. If it is deciding whether to issue a contract, that's a different thing. If it's deciding whether to email a customer, that's a different thing entirely. Or spend money, you have to be sure.

And this is where the hierarchy of meaning becomes clear. Agents should use the richest semantic interface available. If there's a connector, use the connector. If there's a proper protocol, use the protocol. If the system exposes a typed object and a permissioned action, use that.

Only fall back to a browser or desktop control when the richer interface doesn't exist. This is not just engineering preference here. This is how things should be architected. Nate’sletter Nate’sletter So we're not likely to have as many issues as long as we have as many connectors as possible plugged into our preferred AI systems,

which by the way is, pun intended, a plug for you adding plugins to your ChatGP. Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’s Nate’s Nate‐describing the agent having the power to write as just, oh, you trusted to write. Trusted write access is the engineering term. That's too small a way of picturing what we're doing here.

Trust is not a switch. An agent might be trusted to read but not write, draft but not Send Stage but not deploy Recommend but not approve Change a sandbox but not production Write in one space but not another All of those distinctions depend on semantics If it cannot tell the difference between issuing a refund from your

chosen Shopify Natesnewsletter Nate’s The real primitive here is not the ability of the agent to use the computer. It's not even the browser tab for web browsing. The real primitive, the foundation on which we're building, is a semantically meaningful unit of work. A refund, a reschedule, a payment. Natesnewsletter

This, by the way, is also why coding agents arrived first. It is very tempting to say that coding agents worked first because code is text and language models are good at text. That's part of it, but it's not the whole story. Coding agents worked first because software development already has unusually rich work semantics.

A codebase is not just a pile of text files. It has modules and dependencies and tests and type systems and linters and package managers and git history, etc. It has all of these things. That means the agent can perceive state and act on state and observe feedback and revise its actions. It can inspect the repo.

It can edit a file. It can run a test. It can see the error. It can change the implementation and hand the result back. The loop is powerful because the work environment itself gives the agent semantic feedback. The human doesn't have to answer every 30 seconds, is this right?

If the test is failing, the agent can just tell it's wrong. We are talking about coding tests. We are not just talking about verification artifacts. We're talking about semantic meaning artifacts. They tell the agent what world it's operating in. Most knowledge and work is not like that yet, right? A strategy doc doesn't have tests.

A calendar has events, but the importance of those events is hidden behind politics and priorities and relationships. A sales process might depend on unwritten account history. Often it does. A procurement decision may depend on budget timing and risk tolerance, which isn't written down. Agents can help in those domains. They already do.

But the environment doesn't give them the same density of meaning that a code base would give them. This is why coding is a wedge. Not because all work Nate‒sletter Nate‒sletter Nate‒sletter Nate‒sletter Nate’s Because to do work, a model needs to be in a harness that can enable it to access and operate against a

system that has semantically meaningful units of work. And if you want it to be non-coding work, then the non- Coding work has to be semantically meaningful. So harnesses really matter. Harnesses help the agent access the work. But you also have to make sure that the work that's being accessed is actually done in a way that makes sense.

Nate’ And I want to be blunt here. I know that this is a hard problem, but it is exactly the hard problems that are valuable to solve. This is basically a free roadmap if you are a startup. Because as a startup, Nate’s McP Interface, try and break it, understand where it's not working,

understand where it connects to levers, but the agent doesn't know how to reliably drive the levers from a prompt because there's something else about understanding the task that isn't there. I get super passionate about this because if we don't have agents that Nate’s Now, in the article that I'm writing for this on Substack,

I spend more time on getting into the commerce stack, understanding the difference between discovery and checkout and infrastructure, and how our agentic commerce strategies are shaped by this approach, by how we understand semantic meanings of work. Because there's a critical semantic layer to agentic transactions that's super important. But for our purposes today,

we're gonna assume that you realize we have to have a semantic meaning to transactions Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’s Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’s that is really undecided in 2026 is who is going to have the AI browser. If perplexity becomes an AI browser for someone else's tools and other tools plug into it,

it gets durable control here because it manages the browser that can see your Nate’s Nate’s Nate’sletter Nate’sletter It still has kind of a shaky hold on the semantic meaning of work. Nate’s Nate’s Nate’s Nate’s Nate’s has some holes in it. If you're just coming from the computer side, as I've been sharing many specific examples of,

your computer may not fully understand the purpose of the work it's doing. Your agent may not fully understand the purpose of the work it's doing. The calendar example is a good one. If it moves the calendar invite, does it really realize it's inconveniencing two or three other people you don't want to mess with? Probably not.

On the other hand, if you're coming from the semantic meaning of work, if you're coming from making sure that you understand how to bundle that together and make it useful, sort of like perplexity is doing, Nate’s Nate’s Substack Hiper Scaler, the lane's been picked for you because you don't have a gigantic model that you can

use to do code with that doesn't belong to someone else that you're renting. And so when you think about it that way, the world becomes simpler. Humans need clear interfaces. Agents need clear The best software will provide both. Nate’s Nate’s Sass companies want to preserve authority over domain semantics. Identity providers want to govern authorization.

They all have their interests, right? The question is going to be, Which layer owns the meaning of work? Which layer owns the meaning of work that the agent can read? And every software company is gonna have to decide how much semantic access to expose and to whom. If you expose too little, generic agents will operate Nate’s

Nate’sletter Nate’sletter Nate’sletter Nate’s Natesnewsletter Nate’s Nate’s Nate’s Nate’s Nate’s Nate’s That's the bridge we have today. The future is software where the button is no longer the primitive. The primitive is the action behind it. It's described. It's permissioned. It's reviewable. It's reversible where possible. It's composable. So computer use and tools like that give agents hands.

MCP gives agents hands. Semantic controls tell the agent what it's touching. And that is the deeper moat. Now, if you want to dive deeper on this, I'm going to go into memory ownership, enterprise permissions, browser strategy, and agentic commerce on the Substack.

But the core lens here is the same one I would use for every AI product over the next year. Do not ask only whether the agent can act. Ask whether the product knows what that action means. That is your key takeaway. All right. I'll see you next time. Cheers.

[![Nate’s Substack](https://substackcdn.com/image/fetch/$s_!TAjW!,w_96,h_96,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8b4663-3eb8-42e2-a41a-1efd45e5ab98_1400x1400.png)](https://natesnewsletter.substack.com/)

Nate's Notebook

Welcome to my podcast! In these audio reviews of my newsletters, I am to break down complex AI topics in a way that's approachable and relatable. I want you to walk away with the confidence to leverage AI more effectively at home and at work!

Listen on

Substack App

Apple Podcasts

RSS Feed

Email mobile setup link

Appears in episode

[](https://substack.com/@natesnewsletter?utm_source=author-byline-face-podcast)

[Nate](https://substack.com/@natesnewsletter)

Recent Episodes

![](https://substackcdn.com/image/fetch/$s_!bA1X!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e7e3a64-a148-4136-a24b-ef05614768fa_1024x1024.jpeg)

[OpenClaw, Anthropic, and Gemma 4 just redefined what "agent framework" means. You need to pick a side.](https://natesnewsletter.substack.com/p/openclaw-agent-runtime-model-swapping)

3 hrs ago • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!s0Ub!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd53a2b07-f442-496c-a709-b90644ca6c3f_1024x1024.png)

[The Anticipation Gap: Why 4 Problems Have to Be Solved Together for Consumer AI to Work](https://natesnewsletter.substack.com/p/consumer-ai-anticipation-gap)

May 5 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!rgB4!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a07438a-e158-48e3-83a0-f605356dbb85_1024x1024.png)

[55-75% of your week is on thin ice. Here is the audit that shows you which part.](https://natesnewsletter.substack.com/p/job-at-risk-ai-audit)

May 4 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!91hT!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F178d1f1a-a21b-4729-8d13-a9edb4b419ab_1024x1024.png)

[Executive Briefing: What Stripe Sessions 2026 actually means for how you sell](https://natesnewsletter.substack.com/p/agentic-commerce-buyers-power)

May 3 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!Q7An!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83c8e450-fc5c-40c1-b21d-5c11d0d2f34d_2048x2048.png)

[AI agents are about to route around every tool that can't pass 5 structural tests. Here's the diagnostic.](https://natesnewsletter.substack.com/p/issue-trackers-agent-infrastructure)

May 2 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!Dlrn!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bf78199-7530-432a-bb6e-c91a48900d2b_1024x1024.jpeg)

[The buying rule for your personal AI computer (and how to skip the $5,000 mistake)](https://natesnewsletter.substack.com/p/personal-ai-computer-stack)

May 1 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!5_iP!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F888dbbd4-4d44-4912-8929-f43225df8c2a_1024x1024.jpeg)

[The four-hour-a-week tax you are paying because IT picked the wrong AI default](https://natesnewsletter.substack.com/p/wrong-ai-default)

Apr 30 • [Nate](https://substack.com/@natesnewsletter)