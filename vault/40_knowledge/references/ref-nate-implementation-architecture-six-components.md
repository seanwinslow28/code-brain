---
title: "Six things have to be true before AI changes a workflow. Most companies have built two."
source: "https://substack.com/@natesnewsletter/p-197618334"
author:
  - "[[Nate]]"
published: 2026-05-13
created: 2026-05-16
description: "Watch now | The interesting thing about Anthropic’s new enterprise AI services company isn’t the services part."
tags:
  - "source/web-clip"
  - "ai-pm"
  - "enterprise-ai"
type: "source"
status: draft
domain: [product-management]
ai-context: "Nate's six-component framework for productizing AI in enterprise workflows (workflow design, data access, authority, evaluation, audit trails, recovery & ownership) — context for the Anthropic enterprise-services and OpenAI Deployment Company launches on 2026-05-04."
---
The interesting thing about Anthropic’s new enterprise AI services company isn’t the services part. Enterprise software has always needed implementation help: cloud migrations, ERP projects, Salesforce rollouts, the forward-deployed engineering Palantir made famous. What’s new is the target. Anthropic is aiming this venture at mid-sized businesses: the segment with enough operating complexity to benefit from frontier AI, but rarely with enough internal engineering to turn it into working systems.

That target tells you something. The hard part of enterprise AI is no longer buying access to a powerful model. Any company can approve ChatGPT Enterprise, Claude, or Gemini, buy seats, call an API, and produce impressive internal demos. None of that proves the company has actually changed how support tickets move, how invoices close, how compliance reviews happen, or how customers get served. Value shows up when the model has a specific role in a specific workflow, with the right data, permissions, review process, and success metric. That work is what most companies haven’t built. In the last few months, agents have gotten reliable enough at running entire workflows that the distance between companies that have built it and companies that haven’t is starting to compound.

That’s why Anthropic, OpenAI, Blackstone, Hellman & Friedman, and Goldman Sachs are all making moves right now. The implementation layer has become the strategic layer in enterprise AI. There are trillions of dollars in workflow value waiting on whoever figures this out first, and the companies that already understand this are about to pull further ahead.

**Here’s what’s inside:**

- **What’s actually new about the Anthropic deployment company.** Why the mid-market target and PE backing signal a shift from model sales to deployment capacity — and what private equity sees that the market doesn’t.
- **What “implementation architecture” actually means.** The technical and operational work that separates AI experiments from production workflows.
- **The risk: services that don’t turn into product.** When field work compounds into reusable assets versus when it stays bespoke.
- **What this means for startups, buyers, and builders.** Where narrow, deep ownership beats generic AI productivity plays — and the specific move each one should make next.
- **The implementation architecture audit.** A prompt that scores your AI product against the six components, tells you whether you own a workflow or decorate a model, and surfaces the two questions that will end your next enterprise deal.

Let me show you how the pieces connect, and what the next phase of enterprise AI actually requires.

## LINK: Grab the prompts

I keep thinking about how the builders I talk to describe their products. The pitch is usually fluent. The answers under pressure usually need some work. A buyer’s engineer asks about evals or audit trails or recovery paths and the conversation thins out fast. That gap between the pitch and the answer is what this prompt forces. It runs you through the six implementation components: workflow design, data access, authority, evaluation, audit trails, recovery and ownership. Then it scores what you actually own versus what you’re hand-waving. The output is a tier verdict and the two questions your next buyer is going to ask that you can’t yet answer. I’d rather you find that out reading this than in the second meeting with their consultants. \[LINK: Grab the prompt →\]

## What’s actually new about the Anthropic deployment company

On May 4, [Anthropic announced](https://www.anthropic.com/news/enterprise-ai-services-company) a partnership with Blackstone, Hellman & Friedman, Goldman Sachs, and other investors to launch a new enterprise AI services company. The announcement says the company will help mid-sized companies bring Claude into their core business operations, with the consortium’s PE portfolios — spanning healthcare, manufacturing, financial services, retail, and real estate — serving as an initial customer base. Anthropic engineering and partnership resources are embedded directly within the new firm’s team.

Anthropic did not disclose a dollar amount. Press reports put the venture at roughly $1.5 billion, but that figure should be treated as reported rather than confirmed.

The same day, OpenAI closed [its own private-equity-backed enterprise venture](https://www.bloomberg.com/news/articles/2026-05-04/openai-finalizes-10-billion-joint-venture-with-pe-firms-to-deploy-ai): The Deployment Company, a $10 billion vehicle anchored by TPG with backing from Brookfield, Bain Capital, Advent, Dragoneer, SoftBank, and roughly fifteen other investors. The PE consortium is putting in about $4 billion. OpenAI is contributing up to $1.5 billion of its own capital and retains majority control through super-voting shares. The structural detail worth noticing: OpenAI is guaranteeing the PE backers a 17.5 percent annual return over five years. That’s an unusual instrument. It converts equity-style upside into a fixed-yield product for the financial sponsors, which both compresses OpenAI’s risk profile in a way the labs don’t normally accept and tells you how badly the labs want this distribution channel. A week later, on May 11, OpenAI agreed to [acquire consulting firm Tomoro](https://www.bloomberg.com/news/articles/2026-05-11/openai-to-buy-consulting-firm-for-private-equity-joint-venture), bringing about 150 engineers into The Deployment Company to handle implementation work directly. That acquisition is the clearest signal yet that the labs see the forward-deployed engineering work as something they need to own rather than route through partners. OpenAI’s existing enterprise effort — its [Frontier Alliances](https://openai.com/index/frontier-alliance-partners/) with McKinsey, BCG, Accenture, and Capgemini, plus internal forward-deployed engineering — sits alongside this new vehicle, not underneath it.

The two ventures landed on the same day. They are not the same shape. Anthropic’s is smaller, more concentrated among prestige financial sponsors, and structured as a partnership with the PE firms as both investors and customers. OpenAI’s is bigger in capital, broader across investors, more aggressively financialized, and explicitly designed to make PE portfolios into a captive distribution channel. The direction is identical in both cases: the labs are organizing around the practical work of enterprise deployment, not just the sale of model access.

OpenAI’s own framing makes the point. The Frontier Alliances post argues that the bottleneck for enterprise AI isn’t model intelligence — it’s how agents get built and operated inside companies. That sentence is worth taking seriously coming from a company whose public identity has been defined by the model race. OpenAI is still competing on models, but it’s also acknowledging that enterprise value depends on the work system around the model.

## What “implementation architecture” actually means

A model can produce a useful response inside a chat window. A business process needs much more: knowing which data is authoritative, what the user is allowed to do, when a human approval is required, what to log, how to evaluate output, and what happens when the model is wrong. The system has to fit into the tools employees already use, respect company policy, and survive ongoing changes to models, workflows, and rules.

By “implementation architecture,” I mean the specific decisions that let a model perform a real role inside a business process. There are roughly six of them, and most enterprise AI conversations only address one or two:

- **Workflow design.** Which decisions the model gets to make, which steps stay human, where the handoffs happen, what counts as done.
- **Data access.** Which sources of truth the model reads, which permissions apply at the row and field level, which records are authoritative versus stale.
- **Authority.** What the model is allowed to do, against which systems, with what spending or commitment limits. Reading is one risk profile, writing is a different one, and spending is harder to undo than either.
- **Evaluation.** How output gets scored against the business rules that actually matter — not benchmarks, but adherence to the company’s own policy and outcome standards.
- **Audit trails.** What gets logged, what has to get logged, and what an auditor or risk team can reconstruct after a failure.
- **Recovery and ownership.** What happens when the model does something wrong, how an action gets reversed, and who keeps the system tuned as models, processes, and policies change.

A company can buy model access without doing any of this work. It cannot get process-level value without doing all of it.

Customer support is the simplest example. An AI assistant that drafts replies can save individual agents some time, but the agent still has to check the facts, compare against policy, update the customer record, decide on escalation, and copy information between systems. The human is still holding the operation together. Some writing time gets saved. The workflow doesn’t really change.

A serious support deployment starts from the workflow, not the chat window. The company decides which tickets can be classified automatically, which customer records the system can read, which policy rules matter, when a refund can be prepared, when a manager has to approve, and what metrics will prove the project worked. Only then does the model get a role: classifying tickets, drafting replies, recommending escalations, preparing refunds for approval, summarizing account history, or updating records after a human confirms. Value comes from reducing coordination across the business, not from generating a slightly better paragraph in isolation.

Finance follows the same pattern. Anthropic recently released [finance agent templates](https://www.anthropic.com/news/finance-agents) covering KYC screening, pitchbooks, month-end close, valuation review, market research, model building, and general ledger reconciliation. These templates are useful evidence because of what surrounds the model in each one. A finance agent needs access to the right documents and systems, has to follow the firm’s conventions, has to know which outputs are drafts versus reviewed versus untouchable, and has to leave a record that finance, risk, or audit can inspect later.

Not every finance team needs Anthropic’s exact templates. The point is that the template format reflects the actual deployment problem: the model is one component, and the value depends on the instructions, connectors, permissions, review paths, and workflow design built around it.

This is where most enterprise AI pilots break. The pilot gets built around what the model can do in a controlled setting. The business process is built around what the company has to do repeatedly, safely, and measurably. Those are different standards. A pilot can produce an impressive output and still have no clear path into production. It can summarize, answer, draft, or analyze, but if nobody has connected it to the system of record, defined a review process, assigned an owner, or tied it to a business outcome, it stays an experiment.

Something else changed in the last few months that makes this conversation feel different than it did a year ago. Agents can now run an entire workflow end to end with enough reliability that companies are willing to bet operating processes on them, not just side experiments. That’s a 2026 capability shift, not a marginal one, and it’s the reason the conversation about implementation has moved from interesting to urgent.

## Why private equity is here

The new Anthropic company isn’t only selling Claude. It’s selling the deployment capacity around Claude: operations review, use-case identification, custom system builds, ongoing support. These are the steps companies skip when they treat AI adoption as a procurement decision.

Private equity has a direct operating reason to care. PE firms own or influence large numbers of companies where margin, revenue, and back-office efficiency matter immediately, and they have board access and operating partners who can push management teams to act. A deployment company that improves finance ops, support, engineering throughput, procurement, claims processing, compliance, or sales operations across a portfolio shows up in company performance and exit value.

That’s a different distribution model than normal software sales. A vendor usually has to convince each company on its own. A PE firm can introduce a deployment partner across a portfolio at once, compare results across similar companies, and standardize playbooks where the same patterns repeat. The PE firm becomes capital, distribution, governance, and pressure in one channel.

## Why the mid-market

Large enterprises already have access to help, even if they don’t always use it well. They can hire major consulting firms, build internal AI teams, partner with cloud providers, and fund multi-year overhaul programs. Mid-sized companies usually have enough process complexity for AI to matter without the internal AI engineering to build a deployment layer.

A regional bank might have KYC, fraud review, lending, support, and compliance workflows that could benefit from AI but no team that can safely build agents into them. A manufacturer has maintenance logs, supplier communications, quality reports, procurement approvals, and field documentation, but no internal group that can turn those into governed AI systems. A health system has scheduling, billing, claims, documentation, coding, and compliance needs that can’t simply be handed to a generic model without careful controls.

These companies don’t need broad statements about what AI will change. They need someone to map a process, connect systems, define permissions, build a working deployment, train users, measure outcomes, and keep improving the system after launch.

## Forward-deployed engineering, with caveats

Forward-deployed engineering exists because that work can’t be done entirely from a product roadmap. The role sits close to both the customer’s operations and the product. It’s technical, but it also requires understanding how the business actually functions: where work starts, where it ends, who owns each step, which systems matter, which exceptions show up often, which risks are unacceptable, and which outputs users will trust.

This isn’t strategy work, and it isn’t standard software installation. The engineer translates the customer’s operating reality into a system the model can use, which can mean building connectors, designing retrieval flows, defining action permissions, building review screens, writing evals, setting up logs, testing with real users, and feeding what’s learned back into the product.

Palantir is the obvious historical reference because it made forward-deployed engineering central to its enterprise model. The lesson worth taking isn’t that every AI company should imitate Palantir’s culture or sales motion. It’s that some enterprise software categories get discovered in the field. The product team can’t fully understand the customer’s workflow from outside. It has to see how the work actually happens, then turn repeated patterns into product.

## The risk: services that don’t turn into product

The risk for these new ventures is getting pulled into bespoke services work that doesn’t scale. If every deployment requires a large custom team forever, the economics start to look more like consulting than software: variable delivery quality, compressed margins, customers dependent on external teams, product roadmaps deformed by one-off demands.

The opportunity is that early deployment work can teach the labs and their partners what should become repeatable. If ten banks need similar KYC flows, parts of that work can become a template. If many finance teams need similar month-end close support, instructions, connectors, review patterns, and evals can become product. If manufacturers share common procurement, maintenance, or quality workflows, deployment teams will learn which parts are industry-standard and which are company-specific.

That’s how services become product instead of staying services. Field work has to produce reusable assets: templates, connectors, permission models, evaluation methods, implementation playbooks, and vertical workflows. Without that, the deployment company is a body shop with a model partnership. With it, the company can build a defensible implementation layer around the model.

That implementation layer is likely to become one of the most important parts of the enterprise AI stack. Customers need both the model and the surrounding system that makes the model usable in a business: data access, work mapping, business rules, controls, evals, monitoring, change management. Whoever owns those pieces will have influence over how AI is adopted, which models get used, and which workflows become automated.

## What this means for startups

A generic “AI for enterprise productivity” company is walking into a much harder environment than it was a year ago. Four sources of pressure are converging on the same ground at the same time. Frontier labs are moving down the stack toward deployment, releasing vertical templates and forward-deployed teams instead of just APIs. Major consultancies, including McKinsey, BCG, Accenture, and Capgemini, are moving up the stack into agentic build practices and showing up with engineers, not just slide decks. Systems of record like Salesforce, ServiceNow, Workday, and SAP are exposing structured interfaces that let agents act directly inside their platforms with their permissions and their audit trails. And private equity is becoming a distribution channel of its own, capable of pushing one deployment partner across an entire mid-market portfolio. A startup that doesn’t own a specific workflow, vertical, or control layer can find itself squeezed by all four at once.

The better startup opportunity is narrower and deeper. Own a painful workflow that the labs don’t understand well enough. Build the infrastructure that lets companies evaluate agent output against business outcomes. Solve permissioning for AI actions. Build memory, audit, or monitoring for agents working across enterprise tools. Create vertical deployment packages for industries where generic agents won’t be trusted. Become the system of action for a job that matters.

Founders should also expect to do more customer work than a pure software story would suggest. That doesn’t mean building an unlimited services org. It means learning from customers closely enough to find the repeatable product. Early deployments should answer practical questions: which data sources matter every time, which permissions are always required, which steps need human approval, which outputs must be auditable, which exceptions break the workflow, which UI actually fits the daily job.

Those answers don’t come from a pitch deck. They come from watching the work.

The founder mistake is to avoid this work because it feels unscalable. The product stays shallow if the company never does it. The goal isn’t to customize forever — it’s to use early deployments to learn what should become standard. Every customer should make the next implementation faster, clearer, and more productized. Without that learning loop, the company is doing services without building software leverage.

## What this means for enterprise buyers

Buyers should stop treating AI budgets as if the main cost were the model subscription. Seats and API access are only part of the spend. A serious AI program also has to fund integration, workflow design, data cleanup, security review, evaluation, training, monitoring, and internal ownership. Without those line items, the company is budgeting for experimentation rather than operational change.

A useful question to ask before approving a project: after this is done, which business process will run differently, and who will be accountable for proving it improved? “Employees will save time” doesn’t qualify. The answer needs a process, a group of users, a baseline, a new operating method, and a metric. For example: reduce manual variance analysis during month-end close while keeping controller review in place; cut support escalation time for a defined ticket category; reduce time spent on first-pass KYC review while preserving compliance oversight; or shorten procurement cycle time for low-risk vendors under a defined spend threshold.

This level of specificity is uncomfortable because it forces the business to name the work. It also protects the company from buying AI activity that never converts into value.

Buyers should also be careful about outsourcing too much of the learning. Deployment partners can be valuable, especially when internal capacity is limited. But the customer still needs to understand the workflow, the controls, the failure modes, and the maintenance plan. If the partner owns all of that knowledge, the customer ends up with a system it can’t govern or improve.

The better posture is to use outside help to build internal capability faster. A deployment partner should leave behind more than a working agent: documentation, trained owners, evaluation methods, system knowledge, and a clearer playbook for the next workflow. The customer should know which parts of the deployment are portable, which are vendor-specific, and which should become part of its own operating model.

This matters because AI deployments aren’t static. The model underneath will change. The company’s processes will change. Policies will change. Users will find new failure modes. A workflow that’s safe when the model only drafts may need new controls if the model later starts taking actions. That evolution has to be managed. Implementation isn’t a one-time project.

## How to judge the next phase

I’ve been thinking about why the historical analogs for this feel insufficient, and I think it’s because each one only covers part of the challenge. Cloud professional services helped companies migrate infrastructure into a new environment. Systems integrators helped install and configure large enterprise software. Palantir’s forward-deployed engineers translated customer problems into software. Enterprise AI borrows from all three, but its operating challenge is different. It doesn’t only move software from one environment to another. It changes who does parts of the work, how decisions get prepared, when humans review, and how actions move across systems.

Implementation matters so much because of that. A model running inside a company isn’t just another application. It can draft, classify, recommend, summarize, search, call tools, and in some cases take action. The more authority it gets, the more the company needs clear rules around data, permissions, review, and accountability. Better model capability doesn’t reduce the need for those rules. It raises the stakes of getting them right.

The independent adoption data points the same direction. MIT’s [GenAI Divide](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/) report argued that many organizations have struggled to convert generative AI investment into measurable return, with failures tied to brittle workflows, poor integration, and weak fit with day-to-day operations. Any broad study deserves careful reading, but the pattern matches what enterprise teams are seeing on the ground: individual use is widespread; production workflows are still hard.

The reason isn’t mysterious. Individual AI use happens at the edge of a job — a person asks a model for help, checks the answer, decides what to do. Enterprise value requires the model to participate in the flow of work across people and systems, and that second problem is harder because it touches process design, ownership, incentives, governance, and technical integration all at once.

The companies that figure this out look different from the inside. They’ll have a small number of clear use cases instead of a sprawl of disconnected experiments. They’ll know how to choose workflows, assign owners, connect systems, define permissions, test outputs, monitor results, and train users. They’ll develop internal standards for when an AI system can read, draft, recommend, update, approve, or act. Some workflows shouldn’t be automated at all.

Everyone else will have a lot of AI usage and very little AI leverage. Employees will keep using tools, pilots will keep appearing, vendors will keep presenting demos, and leadership will keep asking where the savings are. The missing piece will be the same in each case: nobody rebuilt the workflow around a clear role for the model.

The Anthropic and OpenAI moves matter for that reason. The frontier labs aren’t abandoning the model layer. They’re protecting its value by moving toward the work required to make models useful inside companies. A model that stays outside the business process is easy to swap, underuse, or ignore. A model built into the process with the right controls and integrations becomes part of how the company operates — value for the customer, stickiness for the lab.

That also changes how the next phase should be judged. The product announcement that matters isn’t the one saying a company has added an AI assistant. It’s the one that explains which workflow the system can run, which systems it connects to, which permissions it respects, how its outputs are evaluated, and which business outcome changed. The market has had enough assistant launches; it needs proof that AI systems can handle real operating work.

For builders, this means the product has to sit closer to the business object. A support product needs to understand cases, policies, customers, entitlements, escalations, and outcomes. A finance product needs to understand close tasks, reconciliations, controls, approvals, audit trails, and reporting deadlines. A procurement product needs to understand vendors, contracts, thresholds, budgets, risk, and approvals. A coding product needs to understand repositories, issues, branches, tests, reviews, deployments, and incidents. Generic intelligence becomes valuable when it gets attached to the objects and actions that define the work.

The plain version of the enterprise AI shift: companies don’t need more abstract excitement about AI. They need the engineering and operating work that makes AI useful where money, risk, customers, and employees actually live. The labs have started organizing around that fact.

The best reading of the Anthropic announcement isn’t that services have returned — services never left. It’s that implementation has become a strategic layer in enterprise AI. Private equity is in this because PE has portfolio companies where operating improvements matter. Mid-market companies are in this because they have real complexity and limited AI capacity. Forward-deployed engineering is in this because the work can’t be fully understood from outside the customer. Finance agents and enterprise alliances are in this because the repeated parts of deployment are starting to become product.

The practical question for every company is now: which workflow are we changing, what role will the model play, and what has to be built around it for the change to actually work? A company that can answer those questions has a path to value. A company that can’t won’t solve the problem by buying access to a better model.

![](https://substackcdn.com/image/fetch/$s_!nj_1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fc92b99-fbfe-47cd-8bf6-243a8fdd8794_1024x1024.png)

---
*Clipped from [substack.com](https://substack.com/@natesnewsletter/p-197618334) on 2026-05-16T12:00:11-04:00*

YOUTUBE TRANSCRIPT

Let me tell you why I'm excited about this whole implementation challenge for agents. People think it's an agent story. It's actually the story of finance changing what it believes is the model of software in the future. And at the same time, the story of hyperscalers finding out what doesn't work. And at the same time,

the story of companies figuring out where the disproportionate value in AI is. All of these forces are converging on this private equity-driven services deployment model that we're gonna talk about today. It's so cool. So private equities for a long time had this saying, it's a real saying, you can ask a financier that you know,

that SaaS companies all taste like chicken. In other words, all SaaS companies are the same from a balance sheet perspective. They all have the same growth characteristics, the same numbers. They're very easy to analyze. That makes them ideal as an investment vehicle until recently, when of course,

SaaS company growth metrics and profitability all went to hell in a handbasket because they could not This puts competitive pressure on the PE investment firms because I cannot tell you the number of PEs who have funds that are dated 26, 27, 28.  Hyperscalers are realizing they cannot just sit in fancy brick-walled Silicon

Valley conference rooms and talk cleverly about how AI is helpful and easy to implement and not be out in the trenches. They are realizing that Palantir is right. You have to have forward deployed engineers who have to sit in the weeds with customers and figure out how this works. OpenAI figured it out, Anthropic figured it out,

and they realize they have a new business model for this, they're not equipped for this, and so they're starting to do joint ventures, and they're starting to look for capital to do that, because of course, what's the thing with hyperscalers? They are capital constrained. Anthropic is, OpenAI is,

I do not care that they have raised more capital than just about any company in history. They are still capital constrained because of the tremendous costs of reaching AGI, of getting GPUs, of model training, etc., of serving models increasingly. So, They have to partner up, they have to find finance. Private equity is there with the finance.

That's sort of how the incentives align for those two. And they're all aimed at the third player in this market, the company. The company is realizing, and I'm talking about the company as in Fortune 500, I am talking about people who did not understand the difference between a chat and an agent just a few months ago.

Something happened in December and it's been accelerating since and people who I have talked to who have been in co-pilot chat mode for years are now understanding what agents can do because agents got that much more valuable. and they're desperate to put them to work in real use cases. And they know they don't have the expertise.

They know they don't understand how agents work well, but they know they can get it done because they've seen enough examples in their own work. And I want to be very clear here. The value we're talking about is trillions of dollars. It's because agents can do an entire workflow.

And there's disproportionate value in getting to 100% on that. And getting to 100% on an entire workflow is a new phenomenon. It is a 2026 spring phenomenon that you can do that reliably, clearly, at scale, and repeatably. That didn't used to be the case. It's brand new. Super cool.

And it means that these companies see enough of agents to know they can do this, know they have a lot of places to apply it, and know they need help. And so they are turning to these new companies saying, OpenAI, Anthropics, somebody, please help us. Sit someone down. Please, consulting company, help us.

Maybe you sell snake oil, maybe you don't. I don't know. Please help us. And that is the dynamic that we're wrestling with when we talk about the implementation problem. Anthropic just announced a deployment company with Blackstone, Hellman & Friedman, and Goldman Sachs. It's reported to have $1.5 billion in capital behind it.

OpenAI is going after the same thing with a venture value near $10 billion. Now, I want you to look at that in the context of all of the AI products on the market. Because the AI products on the market right now are by and large not being taken as

seriously as the OpenAI and Claude implementations that I just described as having billions of dollars of capital on the line. that they cannot just implement enterprise AI agent solutions without forward deployed engineers and very serious investment. And the labs aren't the only ones moving here. There are consultancies that have concluded that their best value is actually product.

It's shipping agents into the same accounts that Anthropic and Google and OpenAI are all involved in. And what they're recognizing is that the value in the market right now is in the completed workflow. And that, by the way, if you're wondering where the dollars went, that is where the capital is coming from,

from these private equity firms for these open AI and anthropic joint ventures. But these private equity firms are seeing trillions of dollars on the line in these workflows, and they are not going to miss their chance because they're already squeezed on their previous business model, which in many cases was SaaS predominated and SaaS is in danger.

And so I want to give you a strategic reframe for how you think about the battle to implement full delegated work agentic workflows. We're not talking about pricing here, we're talking about how you actually get these services up and running. Now a lot of the conversation is about the idea that services are where we're going after software.

I think that the larger conversation beyond sort of whether services can be a replacement for SaaS, that's a finance conversation. I think the larger conversation is where the value of the model shows up in the workflow versus where the the harness value shows up. Is the value in the data? Is it in the permissions?

Is it in the evals? Is it in the audits? Is it in the ownership after the launch? This is the wrestling match that we're all having. Companies are having this with vendors. Companies are having this with OpenAI and Anthropic around pricing. Private equity firms are trying to get their piece.

And for years, we have been thinking that the moat is in the data. But that advice is not complete, and I want to differentiate data and model and workflow from the implementation layer, what you might call the harness around the model. And by the way, if you're wondering if I'm just making that up,

the labs are starting to talk this way too. AI's own Frontier Alliances post argues that the bottleneck for enterprise AI is how agents are built and operated inside companies. When the company shipping the model tells you the bottleneck isn't their model, it's the whole implementation layer, we gotta be taking notes.

So I'm gonna dig into more of the lab strategy and I'm gonna dig in way, way deeper on the implementation side in the Substack post, but right now I wanna show you the squeeze that is making this whole shift unlock. There is a specific squeeze of pressure on generic AI for enterprise setups right now.

And I'm going to name that squeeze across four different axes of pressure that are pressuring agentic workflows and how agentic workflows work and how companies selling agents work. Because if you are in the business of the AI economy, you are inevitably now in the business of agents, and these pressures affect you.

And these pressures are exactly what this large hyperscaler forward implementation is about. It's what companies are wrestling with when they put agent workflows into place. It's what the private equity financiers want their piece of. How can they negotiate these pressures and get to value? So, first axis. Frontier Labs are moving down stack.

This has been widely reported and observed. Anthropic and OpenAI used to ship the model and let everyone else build around that. But now they're standing up deployment companies. As I've said, they're hiring these engineers that are going to be inside embedded in companies. They're also going directly at product pieces, right?

Like Claude releasing Claude Design or Claude releasing Finance Agent Templates or even going after traditional coding agent patterns, which of course we've kind of forgotten, but going after Cursor, for example, with Codex, with Claude Code, that was the first example of this. You want to pay attention when they do that to

where the labs are saying the value lives more than what they're claiming they own on the surface. I'll give you an example. I do not think, as amazing as Claude is at finance, that Claude is going to replace the Bloomberg terminal. It's not. I do not believe that these dedicated,

deeply embedded solutions are going to be easily displaced. I do think this is a signal, very publicly, of where AI labs are willing to allocate capital to go after particular pieces of value in enterprise workflows that they have high confidence AI can solve. And that is a very, very valuable signal. So I read their hiring lists.

I read their launch notes as essentially a cheat sheet from the hyperscalers on where they think AI agents are good, which is really helpful for the rest of us. But it is also a source of pressure, right? It's a pressure on everyone around them. When, like, Cloud Design releases, everyone begins to ask questions of Figma.

And we should, right? And it becomes a source of pressure. So second piece, second axis of pressure. Consultancies are moving up the stack. I'm talking big ones. McKinsey, BCG, Accenture, Capgemini, all are inside the OpenAI Frontier Alliance program. PricewaterhouseCoopers is collaborating with OpenAI on the office of the CFO. These firms are not just doing change management,

They are now starting to build deliberate agentic practices. They're training delivery teams on production deployment patterns and they're showing up with engineers who can wire AI into operating systems. They have decades of relationships and they are coming for agentic workflows that they think are held by the decision makers whom they have existing relationships with.

This obviously puts them at a massive advantage versus the average startup. who may also be selling AI agents because that's all anyone with AI is selling right now. Third axis of pressure. Systems of record are exposing structured interfaces that make it easier and easier to stay with them. If you are trying to disrupt

These vendors don't need a startup sitting between their data and a customer's agent. They want the agent to call their platform directly with their permission and their audit trail. I've talked about that. That is an axis of pressure on anyone trying to play the game for agent workflows today. Fourth axis of pressure.

Private equity has become a distribution channel. So the Anthropic Deployment Company that I talked about P.E. effectively owns and influences thousands of mid-market companies, especially SaaS companies around finance, ops, support, procurement, compliance, and they are desperate to get more efficiency out of those investments, as I discussed earlier. in this video. A PE firm, therefore,

can be an axis of deployment that gives someone who has a partnership with them an incredible advantage because they can introduce one deployment partner across the entire portfolio, compare results across companies, and standardize the playbooks where the same patterns repeat very quickly and they are incentivized to do so.

That is a very different distribution shape than vendor-by-vendor sales, which most startups go for, and you're just not going to win that battle. So there are four pressures that are all aligning on a particular AI deployment pattern at the enterprise level. And we're going to get into that next.

So what does this mean for you if you're a builder? If you're shipping a generic AI for Enterprise wrapper Without owning a workflow, without owning an action layer, a governance structure, if you're just depending on the model and maybe saying we can access your data for the special sauce,

you are going to get squeezed by the four pressures I just talked about. I'll go farther and say I want you to understand that if you're sitting there trying to figure out which with each agent to ladder across multiple workflows. You need to be thinking more about how your implementation layer shapes the value

and less about whatever a particular vendor is claiming. All the vendors will tell you their data is key, accessing their data is key, that their agent is going to be the one that delivers for you. I get that. You need to decide in terms of the value that you are putting into place as a buyer now,

are you getting value for money? Are you getting an agent that is extraordinarily capable within the implementation environment you actually have? Bring your developers to the table. And in keeping with the SaaS platforms, the data platforms you're actually integrating with. And that is where the pressures that we feel from everyone converging around this

agentic workflow stack really start to bite. We're basically in a position where we're paralyzed for choice. And that choice paralysis analysis is a function of the exact trillion dollar market I talked about at the top of this video. The pot of gold here is so valuable that everyone is converging on it and it makes

choosing and building on it difficult and it makes discerning value difficult. Look, plenty of wrapper companies are going to keep shipping in this market. The defensibility window may be closing, but most people who are building right now are still building and pricing in last year's market and they don't have good answers for someone who asks hard questions

about the value of what they're selling versus the value of what you bring to bear as the installer of the system, as your devs implement and build the system. Now if you want to dig in deeper on what specific moves you should take under this pressure, whether you are competing with a lab, whether you're a consultancy,

whether you're a buyer, I have a much deeper dive on each of those personas on the Substack. But I want you to take away the idea that the squeeze matters regardless because Everyone is going to continue to apply pressure on agentic workflows until someone is able to clearly claim ownership in the space.

And we are very much years away from having clarity there. It is not a foregone conclusion, for example, that Claude will own all those workflows. It's not a foregone conclusion OpenAI will own all those workflows. It's not a foregone conclusion that anyone will own them.

that's why everyone's taking a claim and that's why you need real clarity on where value lies. Now let's dig into this implementation layer just a little bit. Implementation layer is a phrase that gets thrown around and it's thrown around so often it can be difficult to define it. I'm going to be very specific here.

There are specific implementation layer components that tie to the value I'm talking about. If you've Built them, you understand. And if you haven't, I'll explain them so you get it. Workflow design comes first. You must decide which decisions the model gets to make, what steps stay human, where the handoffs are, and what counts as done.

That's not a problem. Data access is another piece here. What sources of truth does the agent read? Which permissions apply at the row and field level? Which records are authoritative and which are stale? The model can produce a very confident answer from a six-month-old PDF or from a live record, but you probably care which,

and the implementation layer decides which. What is the agent allowed to do? Against which systems? With what spending or commitment limits? Reading is one risk profile. Writing is a whole separate risk profile. And spending is something you can't undo, typically. Evals are another one. How do you measure whether the agent's output is correct,

complete and safe before it goes anywhere? Evals are not a benchmark, right? Evals are actually the way you score the model's adherence to specific business rules. If you can't tell me what's in your eval, You're not going to be in a position to tell me whether your agent works. Audit trails? What gets logged?

What has to get logged? What can an auditor reconstruct after a failure? What about recovery and ongoing ownership? What happens when the agent does something wrong? How does an action get reversed? Who at the customer keeps the system tuned and up to date?

These are all components that are not model work that are typically put on the enterprise to do that have an extraordinary impact on the total package of value that the agent does. But everyone's gonna tell you, if they're a vendor, that they're selling you that value. And unless they're coming in to actually build that for you,

they're not reasonably going to be selling you that value. The value lies with the builders. The value lies with people who can build an implementation layer that surrounds these agents and allows them to do work that is truly enterprise grade. Now I have a deeper teardown of all of the components I just named over on the

Substack and if you're building on any of those components, that is where you can get a full readout on regulated, unregulated workflows, how you think about them together. If we zoom out for a minute and we ask why this is happening right now,

I think we have to come back to that finance part of the story I called about earlier. Because the reason why PE is going after this space is twofold sass and growing it. I referenced that earlier. P.E. firms are incentivized to put together AI stories for the companies they are selling.

And they need to do that to turn their SaaS players into sellable companies. And that is part of why OpenAI and Anthropic can find the capital to do this right now. And so the question you should ask if you are not at OpenAI or Anthropic is,

is your product something a PE firm could plausibly buy on behalf of 50 portfolio companies? Are you stuck in one-to-one enterprise sales? If you are getting sold a product, is it a product that has that kind of scale and track record to it where you can validate it? Or is it something that is one-to-one?

You need to get into understanding how a particular move that the PE companies are making right now shapes your competitive set and build options. Because if you're not ready to explore PE as either a distribution channel or as a signal of real enterprise value, then you're probably not really talking about agentic workflows that scale.

Because the ones that scale, PE is already going after them. and you should be seeing that when you have these conversations with people who are building them. Now all of this can seem very difficult to follow and I want to simplify it down for you.

If I were building in the next 12 months and I were thinking in terms of product strategy, the key thing I would think about And this is true whether you are in the enterprise, or whether you are building product for the enterprise, or even whether you are in PE.

The key principle is to sit closer to the business object. Generic intelligence becomes valuable when it gets attached to the specific objects and actions that define real work. Not abstract reasoning, not better summarization, but the actual objects that drive business workflows. So let's walk through what that might look like.

Let's say you have a support product that has to understand cases and policies and customers and entitlements and escalation paths. You want a implementation layer where the object model for customer support ties into a clear bundle the agent can act against to actually close on customer support tickets, etc.

to actually deliver value for customers in a finished, fully formed way. Another example, let's say that you are working on sales. You are going outbound on sales, you're going inbound on sales, you're closing sales motions. You want a sales object oriented model where you can actually have the model

understand the different objects in the business workflows and work against them all the way across the entire sales funnel in a reliable, consistent manner. And that requires thinking about your data layer and thinking about your implementation layer as one clearly integrated substrate that allows an agent to operate across the top. Now,

specific agents are going to stand out in any conversation we have as buyers, as sellers, even in PE in the next 6 to 12 months. And the reason why they will stand out is because when you ask questions that dig for those specifics, ...vendors that haven't thought through or software builders that haven't thought

through how their value proposition works at a discrete level, they're going to show their cards. They're not going to be what they say they are. They're going to be saying, oh, the model's great. We're betting on the model getting better and better. We trust your data. Your data is going to help us.

They're going to give these generic answers. Builders who do well, whether they sit in the enterprise or outside it, are builders who understand that the implementation layer is not something that is just up for grabs that Anthropic can take tomorrow The implementation layer is the detail that allows you to actually get value out of your agents. Now,

if you want the complete breakdown component by component on the implementation layer with specific guidance on what to keep inside the house versus what to bring to a partner with a buyer side audit framework. I have all of that on the Substack. Link is in the description.

If you're building with this, you do need to be clear on your implementation detail. I'm not just kidding around. I don't have to understand when I say you have to And if you're in PE, you have to understand enough of the detail of the people who are selling you

software or offering you companies with software that you know that there's actual value there. And by the way, I do know for a fact there are PE firms out there who are currently testing SaaS company build by saying, can my crack team in-house build this in cloud code over the weekend?

The things I am talking about with the implementation layer are too complicated, too nuanced, and too far into the weeds on specific enterprises to be built in a weekend by cloud code. It just does not work that way. And that is part of the challenge is that the business models have to change.

The business model of SaaS tastes like chicken was predicated on the idea that software could be generic and could be essentially the same format. in every single place where it was put in every single company in the world. We don't live in that world anymore. The disproportionate value in agentic workflows is in customization.

And so the reason why I'm emphasizing that we are living through an implementation layer war is because people have figured out that there are trillions of dollars in getting this right. And people are trying to figure out where is the leverage point to get to that value? Is the leverage point in the data?

Salesforce would probably argue that. There are others. SAP would argue that. Is the leverage point in the model? I'm sure Anthropic and OpenAI will tell you the leverage point is in the model, maybe in the harness. Is the leverage point in the memory? We didn't even get a chance to talk about that,

but there's a whole set of companies that will tell you the leverage point is in the memory. What I am here to tell you is that the actual leverage in this system is the way an implementation layer assembles a model, assembles a harness, assembles data into an actionable workflow.

And that is going to be custom and that is not going to be something anybody else can easily do. It is biased toward building internally And you need to think about, if you are bringing someone in, whether they can build and bring in components that align to where your implementation detail lives.

And that's sort of how you start to assess, is you're going to have a You have to ask yourself, does this vendor that comes in, does what they sell play nicely with my implementation fabric? Do they understand the data objects I work with? Do they understand my workflows at a very detailed level?

If you want to keep learning and you want to keep digging into this, hit subscribe. I've got more videos coming on this shortly. For a deeper read on this one, check out the Substack and happy building. The implementation layer is so encouraging to entrepreneurs. If you want to build in this space, it's wide open.

If you want to build internally in this space as an entrepreneur, it's really wide open. And if you want to be part of figuring out how we unlock trillions of dollars of value, there's going to be so many roles around this space to go after. I'm so excited about this one. Have fun.

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

![](https://substackcdn.com/image/fetch/$s_!6t_T!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b9d57a2-dc48-4532-90e0-385284a0b901_1024x1024.png)

[Exclusive: a conversation with Tibo from Codex on what your company has to become when the model can actually do the work](https://natesnewsletter.substack.com/p/codex-five-leadership-chairs-tibo-interview)

2 hrs ago • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!Wycm!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff495bcae-894d-4d1c-a65d-70166b77333e_1024x1024.png)

[The 2 prompts I'd run before any 2026 SaaS renewal (especially if you're deploying agents)](https://natesnewsletter.substack.com/p/saas-agent-license-renewal)

May 15 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!ha-w!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F222fe587-cc73-46c0-a86c-2ee94bd7f9e2_1024x1024.png)

[Your AI agent is rediscovering 85% of its context every run. Here's the architecture fix (+ Contract Spec, Failure Triage, and Stack ADR)](https://natesnewsletter.substack.com/p/rag-agents-knowledge-layer-architecture)

May 13 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!HTab!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8be3b75d-6a62-4aa6-9358-df28cc3660af_1024x1024.png)

[Six layers your agent has to handle. Most products have only thought about two. + a responsibility-layer audit.](https://natesnewsletter.substack.com/p/agentic-commerce-protocol-war)

May 12 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!Dxc2!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95ff4114-970a-4da1-919d-deefb9bc0a07_1024x1024.png)

[You gave your AI agent real tools. Here's the 4-part control layer it's missing + the Judge Layer implementation guide](https://natesnewsletter.substack.com/p/agent-judge-layer-production-control)

May 11 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!ZqA3!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb922b2e-7db7-4dde-a8d6-29b7f8efcf6f_1024x1024.png)

[Executive Briefing: Six announcements in 48 hours just changed how enterprise AI gets bought (+ 2 prompts for the new process)](https://natesnewsletter.substack.com/p/enterprise-ai-buying-build-room)

May 10 • [Nate](https://substack.com/@natesnewsletter)

![](https://substackcdn.com/image/fetch/$s_!rgE9!,w_150,h_150,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F025c0d0c-0cf1-4edd-b203-550b02126b43_1024x1024.png)

[OpenAI made Codex smart enough that the bottleneck moved. Most people haven't noticed where it went.](https://natesnewsletter.substack.com/p/codex-plugins-bottleneck-moved)

May 9 • [Nate](https://substack.com/@natesnewsletter)