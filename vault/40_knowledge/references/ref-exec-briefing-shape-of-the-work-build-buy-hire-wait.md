---
title: "Executive Briefing: Stop asking if AI can do this. Start asking what shape the work is."
source: "https://natesnewsletter.substack.com/p/build-buy-hire-wait-ai-matrix"
author:
  - "[[Nate]]"
published: 2026-05-16
created: 2026-05-21
description: "Watch now | Every serious AI conversation eventually turns into the same practical question."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management]
ai-context: "Executive briefing on the build/buy/hire/wait AI matrix: stop asking can-AI-do-it and start classifying the shape of the work."
---
Every serious AI conversation eventually turns into the same practical question. Should we hire someone for this? Should we automate it? Should we buy a tool? Should we build the workflow ourselves? Or should we wait because the models are changing so fast that anything we build today may be obsolete in six months?

Most teams treat this as an AI question. That ends up costing time, money, and the work itself. It is a work-shape question. The right answer depends less on how impressive the model demo looked and more on the structure of the work in front of you: how often it repeats, how costly a mistake is, how much judgment it needs, and whether near-term model improvement is about to collapse what you are about to build.

Shopify gave the market one version of this question when Tobi Lütke told teams they had to show why they could not get something done with AI before asking for more headcount. It stopped hiring from being the default answer to every capacity problem. But “can AI do this?” is the wrong question to stop at.

Executives are running a capital allocation problem, not a technology question. How you allocate capital has always defined what a firm can accomplish, and the upside variance on AI investment right now is wider than most leaders have ever priced for. Pick the wrong motion for a workflow and the cost is not only the wasted spend. It is also the upside you never captured because the capital landed in the wrong place.

The wrong answer is expensive in both directions. If you hire against work that AI can already handle, you build a cost structure around disappearing scarcity. If you automate work that depends on trust and judgment, you break the business process at the point where the human mattered most. If you buy a generic tool for company-specific work, you spend months fighting the product. If you custom-build something the market has already solved, you burn scarce builders on infrastructure that should have been a line item. If you wait on a workflow that is already stable and costly, you let delay masquerade as prudence.

Gartner has put a number on it: more than 40% of agentic AI projects are forecast to be canceled by the end of 2027 because of cost, unclear business value, or inadequate risk controls. Classify the work before the spending starts.

**This briefing covers:**

- **The decision starts with the work.** A six-dimension scoring framework that routes each workflow to the right investment motion.
- **When to automate, build, buy, hire, or wait.** Real company examples (IBM, Klarna, Stripe) showing how the shape of the work determines the answer.
- **The matrix.** A two-axis visual that maps market maturity against company specificity, with named examples in every cell.
- **The executive job is changing.** Why routing logic is the new leadership skill, and what happens when executives and builders have the conversation together.
- **Four prompts that route AI investment.** A decomposer that turns a function into scoreable workflows, a scorer that writes the budget memo, a pressure test that forces three counter-arguments before capital commits, and a describability gate that holds automation projects until eight fields are filled.

Classify the work first. The investment motion follows.

## LINK: Executive Circle MCP Server

A read-only MCP server that gives your AI direct access to my entire published content library. You connect once, and then the archive just shows up inside your normal AI conversations. You ask your AI a question during your actual work, and it pulls from everything I’ve published to answer it.

Setup takes about ninety seconds.

- Register once at **[promptkit.natebjones.com/executive/mcp](http://promptkit.natebjones.com/executive/mcp)**
- Enter your access code (executive\_circle) and email, and get a personal connector URL with a unique token.
	- In Claude, you go to Settings → Connectors → Add custom connector, paste the URL, and you’re done.
		- ChatGPT works the same way through Settings → Apps & Connectors.
		- If you use Claude Code, Cursor, or any other MCP-compatible client, the URL works there too.

Your subscription now works inside your AI. Have fun!

## LINK: Grab the prompts

Capital allocation mistakes in AI happen before the model ever enters the room. The team buys before they define the work, builds before they know if it’s differentiating, hires before they redesign the job, or automates a workflow they cannot describe in plain English. These four prompts close the gap between “we have an AI budget” and “we know where it should land.” The Workflow Decomposer breaks a function into scoreable units of work. The Six-Dimension Scorer produces a budget-memo paragraph an executive can paste into a planning doc. The Build-vs-Buy Pressure Test forces the three strongest objections to your team’s preferred motion before the money commits. The Describability Test refuses to let an automation project start until the workflow can survive eight specific fields. Run them in order. If a workflow cannot pass the Describability Test, the next investment is process discovery, not software.

## The decision starts with the work

Before you decide whether to hire, automate, buy, build, or wait, describe the work.

Not the department. Not the role. Not the software category. The work.

An accounts receivable team does not have one AI problem. It has collections prioritization, invoice matching, customer follow-up, exception handling, cash application, dispute resolution, reporting, and escalation. Those are different shapes of work.

A product team does not have one AI problem. It has user research synthesis, spec drafting, backlog grooming, design review, experiment analysis, roadmap judgment, launch coordination, and customer escalation. Those are different shapes of work.

A healthcare company does not have one AI problem. It has high-volume administrative transactions, clinical documentation, coding, prior authorization, audit workflows, clinician trust-building, regulatory interpretation, and evaluation design. Again, different shapes of work.

The unit of decision is not the job title. It is the workflow.

Once you get down to that level, the question becomes much easier. Every workflow can be scored across six dimensions: repetition, risk, judgment, company specificity, market maturity, and model-improvement risk.

Those six dimensions do more than help you think. They route the investment.

## When to automate work with AI

Automation is the right answer when the work repeats often, follows a clear pattern, has recognizable exceptions, and can be checked cheaply.

This is the part of AI adoption most people understand first, because the examples are obvious. [IBM’s internal AskHR system](https://www.ibm.com/case-studies/ibm-askhr) is a clean public case. IBM says AskHR handles routine HR inquiries and tasks across areas like payroll access, vacation requests, employee letters, and manager workflows, while human advisors handle more complex needs. IBM reports a 94% containment rate for common questions and a major reduction in support tickets. That is the right shape for automation: high-volume, recurring, policy-bound work where the system can answer routine cases and escalate the rest.

Klarna’s customer-service assistant is the more complicated version of the same lesson. In 2024, [Klarna said](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) its OpenAI-powered assistant handled 2.3 million conversations in its first month, about two-thirds of its customer-service chats, and did the equivalent work of 700 full-time agents. That is a real automation result. But by 2025, [Klarna’s CEO was also talking publicly](https://techcrunch.com/2025/06/04/klarna-ceo-says-company-will-use-humans-to-offer-vip-customer-service/) about bringing humans back into customer service because two things can be true at the same time: AI can reduce costs and handle routine work, while customers still need human support in higher-trust moments.

Automation works best as a routing layer, not a religion.

If a customer asks where an order is, an AI system should probably answer. If a customer is angry, confused, high-value, dealing with a complicated refund, or stuck in a situation where policy and trust collide, the goal is not to prove the AI can handle it. The goal is to get the right kind of attention to the case.

The first rule: automate when the routine cases dominate and the exceptions are visible. Do not automate when the exception is the work.

Most bad enterprise AI demos fail at exactly this line. The vendor shows the routine case in the pitch deck and the buyer signs because the routine case looks impressive. Production traffic turns out to be mostly exceptions. Six months later the executive team is staring at an accuracy number nobody can defend and asking how the demo and the deployment ended up so far apart. Nobody was lied to. The buyer bought the wrong shape of work.

## When to build AI workflows in-house

The next category is the one most executives miss.

Some work should not be bought as a generic tool, and it should not be handed to a single human forever. It should become an internal workflow.

The work repeats in this zone, but the quality depends on company-specific context. It needs your data, your standards, your approval gates, your examples, your customer language, your risk thresholds, your source hierarchy, your team’s way of doing the job. It may still need humans, but the humans should not have to reconstruct the workflow every time.

This is where skills, agents, plugins, internal copilots, workflow builders, and MCP-connected systems matter. OpenAI’s Codex uses [skills](https://openai.com/academy/codex-plugins-and-skills/) — reusable instructions that teach the system how a person, team, or company does a task. Anthropic describes [Claude plugins](https://docs.claude.com/en/docs/claude-code/plugins) as reusable packages that can bundle skills, MCP connectors, commands, and sub-agents. The technical details vary. The pattern is the same: repeated work can be packaged.

A code review workflow is not just read the diff. It is a standard for what counts as a serious bug, where to look for risk, which tests matter, what comments deserve review capital, and how the team wants findings written.

A customer research workflow goes beyond summarizing transcripts. It is a standard for source coverage, uncertainty, customer evidence, product implications, and what not to include.

A board-reporting workflow goes beyond making slides. It is a standard for which metrics matter, how assumptions are handled, what decisions need to be surfaced, what confidence level is acceptable, and which claims require backup.

You buy generic software when the market has solved the problem. You build workflows when the problem is yours in a way that matters.

If you commission a build, your team will be motivated to come back and tell you it works. That opens up the harder questions. Do you know whether it works? Can you sit as the honest third party and say this is up to the standard, or this is unacceptable and needs another pass, or this was the wrong specification and we need to redefine what we are asking for? That level of clarity around what good output looks like is missing from most build conversations. The agentic capability has improved sharply over the last several months. The executive conversation around what counts as good has not kept up, and the gap is where most build budgets go to waste.

In a recent finance-operations conversation, the orders-to-cash question had this shape. The company did not need to hire a large team or build a giant custom platform first. A large part of that workflow was high-volume, low-complexity transaction handling. It had jargon, but the underlying shape was not mysterious. The better first move was to map the process, separate routine cases from exceptions, and build or buy a workflow that routed the routine work through AI-assisted automation while preserving human review for disputes, unusual customers, and policy-sensitive cases.

In a recent healthcare AI conversation, clinical evaluation had a different shape. If the work requires sitting next to clinicians, understanding how they reason from clinical data, building trust, and translating that into ground truth and eval frameworks, you are no longer dealing with routine automation. You are dealing with a workflow that has to encode expert judgment. That may deserve tooling, but the first investment is the human system that can define what the tool should measure.

The build-or-buy line lives here. If the standard is yours, you have to package it. If it is not, do not pretend it is.

## When to buy AI tools vs building

Buying is underrated in AI because everyone wants the custom thing.

That instinct is often wrong. If the problem is common, mature, non-differentiating, and already handled well by the market, you should buy it. Your internal builders should not spend their best hours recreating solved infrastructure.

This is especially true when the vendor owns a domain primitive that would be hard or risky to recreate. Payments are the clean example. Stripe’s [agentic commerce documentation](https://docs.stripe.com/agentic-commerce) describes shared payment tokens that let AI platforms pass scoped payment credentials and risk signals to businesses without exposing the underlying credentials. That amounts to a structured transaction primitive, not a feature. If you are building an agentic commerce workflow, you should be very careful before deciding that your differentiated work is rebuilding payment semantics, credential scoping, merchant risk, and settlement logic yourself.

You probably should not build your own commodity payroll system, basic identity system, or generic helpdesk when the work is standard. You probably should not build your own scheduling infrastructure unless scheduling is core to your product, or your own security scanner when mature tools already exist.

The strategic question is whether the layer is differentiating.

If the work is common and the market has a mature solution, buy it. If the work is common but the vendor category is still thin, buy carefully and avoid long lock-ins. If the work is company-specific and central to how you operate, buying may still be useful, but only as part of a workflow you own.

## When to hire for AI vs automate

Hiring is still the right answer more often than AI maximalists want to admit.

The mistake is hiring people to do routine work that should become a system. But the opposite mistake is just as dangerous: refusing to hire the person who can define, govern, and improve the system.

A lot of companies are now trying to find a single impossible hire: domain expert, AI builder, systems architect, operator, change leader, security thinker, product person, and executive translator. Sometimes that person exists. Usually the market clears more slowly than the business wants.

The better question is what kind of human capability the workflow actually needs.

If the missing piece is domain trust, workflow engineering, evaluation design, or executive ownership — hire for that. If the missing piece is a person who can sit between clinicians, engineers, compliance, and customers and make the work legible to all four groups, do not pretend a tool will solve that.

This came up clearly in a healthcare talent conversation I had recently. Some requirements were teachable. Industry codes, payer-provider mechanics, internal jargon. A strong AI-native operator could ramp quickly on a lot of that, especially with the right support. But other requirements went deeper than knowledge. Building trust with clinicians, understanding how clinical ground truth is created, and designing evals that clinicians will actually respect required prior exposure. Not because healthcare is magic. Because trust was part of the work.

That distinction matters for every industry.

If the work requires credibility in front of customers, regulators, clinicians, enterprise buyers, auditors, or a skeptical internal team, the human is not incidental. The human is part of the production system.

Shopify’s headcount rule is useful as pressure, but it should not become a blunt instrument. Can AI do this? is not enough. The better version is: what part of this role is routine execution, what part is judgment, what part is trust, what part is workflow ownership, and what part will disappear as tools mature?

Sometimes the answer is a split. Pair a domain expert with an AI-native builder. Pair an operator who understands the process with a workflow engineer who can package it. Pair a senior judgment owner with agents that remove the coordination work around them.

In practice, build and hire often happen in sequence rather than as competing choices. Hire the operator who can define the standard, then build the workflow around that standard, then automate the repeated parts. If you automate before the standard exists, the system simply scales confusion.

## When to wait

Waiting is not the same as doing nothing.

Waiting is the right answer when the tool category is immature, the workflow is not yet stable, the risk controls are not ready, or near-term model improvement is likely to commoditize the thing you are about to build.

This is especially true in agentic AI. [Gartner has warned](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) that more than 40% of agentic AI projects may be canceled by the end of 2027 because of cost, unclear business value, or inadequate risk controls. Gartner’s [agentic AI hype cycle](https://www.gartner.com/en/articles/hype-cycle-for-agentic-ai) reinforces the maturity problem: most deployments remain narrowly scoped, and the supporting practices for governance, security, and cost management lag behind the enthusiasm.

That does not mean avoid agents. It means be precise.

If the workflow is routine, valuable, and measurable, move. If the workflow is vague, high-risk, and sold under a label that vendors themselves cannot define consistently, wait or run a narrow experiment. If the technology is changing monthly and the cost of being wrong is high, do not build a giant internal platform. Build the smallest learning loop that tells you when the category crosses your threshold.

Waiting is also right when the model is about to absorb the custom work. A year ago, a team might have built a custom summarization pipeline for internal documents. Today, much of that may be handled by stronger models with connectors, retrieval, and workspace context. A year from now, more of it will be native inside the tools people already use. If the work is generic and the models are rapidly improving into it, the right move may be to wait, prototype lightly, and avoid hardening a system whose main advantage is about to vanish.

But waiting becomes cowardice when the workflow is already stable and expensive. If a team spends five hours every week producing the same report from the same systems for the same audience, you do not need three more quarters of model progress to act. You need to describe the workflow.

The speed objection is legitimate. In a competitive market, being late can be more expensive than being wrong. But urgency is not the same as clarity. If the cost of delay exceeds the cost of a bad first version, move with a narrow learning loop. If the pressure is only that competitors are announcing things, the matrix is doing its job when it tells you to wait.

## Do not automate what you cannot describe

One line should sit above every AI investment review.

Do not automate what you cannot describe.

If you cannot describe the inputs, the output, the standard, the source of truth, the exception path, the error cost, the owner, and the review gate, then automation is premature.

Many AI projects fail at this point before the model ever enters the room. The team says it wants to automate customer onboarding, finance operations, research, compliance, sales follow-up, or reporting. But those words are too broad. They hide twenty workflows with different risk profiles.

A good automation candidate can be described in plain English.

Every Monday morning, read the last week of customer support tickets, group them by product area, deduplicate repeated issues, flag anything tied to a top account, and post a summary with links in the customer-success channel.

Describable.

For every incoming invoice from an approved vendor under a certain dollar threshold, match it against the purchase order and receipt, flag mismatches, and route clean cases for approval.

Describable.

Review all clinical notes for potential coding gaps, but only produce suggestions with evidence links and route anything uncertain to a qualified reviewer.

That is describable, though higher risk.

Make our back office AI-native is not describable. Automate finance is not describable. Replace customer support with agents is not describable.

If the workflow cannot be described, the next investment is process discovery, not automation.

Process discovery should be treated as its own investment, not as a failure to automate. Some work starts genuinely undescribed. In that case, the sequence is discover, then describe, then automate. Fund the discovery sprint, name the owner, map the exceptions, and decide what evidence would make the work describable enough for software.

The matrix is the artifact that keeps this from turning into taste or FOMO. The horizontal axis is how specific the work is to your company. The vertical axis is how mature the market solution is. The investment motion changes by cell.

## AI build vs buy decision matrix

![A two-by-three decision matrix routing AI work by market maturity and company specificity.](https://substackcdn.com/image/fetch/$s_!Xlo8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08980800-0c3f-407a-9ac9-446e12b8421a_2048x1451.png)

A two-by-three decision matrix routing AI work by market maturity and company specificity.

The visual version is the whole point. It puts six common investment motions in one place: buy mature commodity work, buy primitives while owning company-specific workflow, prototype or wait where common categories are immature, build workflow where your standards are the product, wait where generic work is likely to be absorbed by base tools, and hire first where judgment or trust has to be defined before software can help.

Read the matrix this way. If the work is common and the market is mature, buy. If the work is common and the market is immature, prototype narrowly or wait. If the work is company-specific but the market has useful primitives, buy the primitives and own the workflow. If the work is company-specific and the market is thin, build the workflow. If the bottleneck is judgment, credibility, or trust, hire the person who can define the standard before you automate around it.

Hiring cuts across the grid. If the work resists framing, requires trust, or needs someone to define the standard before software can help, the next investment may be a person. If the work is already described and repeated, the next investment is usually a workflow, a vendor, or automation.

The named examples matter because they keep the cells honest. Buy looks like IBM AskHR for routine HR service or Stripe’s payment primitive for agentic commerce. Build-workflow looks like turning code review, customer research synthesis, or board reporting into a reusable internal playbook rather than asking a human to reinvent it each time. Hire looks like the healthcare evaluation case above, where the missing capability was not another tool but a person who could earn clinician trust and define ground truth. Wait looks like broad custom RAG pipelines or generic code-review-as-a-service tools when the base workspace products are rapidly absorbing the workflow.

For finance, ask which workflows are deterministic matching, which require exception handling, which require auditability, and which require a finance leader’s judgment.

For product management, ask which parts of the job are synthesis, coordination, customer interpretation, roadmap judgment, and organizational trust.

A much more useful conversation.

## The executive job is changing

The executive job in this world is to own the routing logic — not to personally evaluate every model and tool.

This cannot be delegated to any single function. IT alone misses the business judgment. The business alone misses the implementation path. Procurement alone cannot keep pace with the category. Developers alone miss the customer trust and organizational risk.

The right conversation has both sides at the table.

Executives need to define what outcomes matter, where human judgment must remain, which risks are acceptable, and where capital should go. Builders need to say what is actually buildable, what can be bought, what should be packaged as workflow infrastructure, what is too immature, and what will be easy in six months if the company does not panic-build today.

The worst AI strategies separate those conversations. The executive team buys the vision. The builders inherit the mess. Or the builders experiment locally. The executive team never changes the operating model. Both fail in different ways.

The companies that do this well will create a new habit: before money or headcount gets committed, the team classifies the work.

What repeats? What is risky? What requires judgment? What has the market already solved?

Then they choose the investment motion.

Use it in the next budget meeting. List the top five AI investments planned for the next two quarters. For each one, write one sentence describing the actual workflow, not the department and not the tool category. Score the workflow on the two axes: how specific is this work to us, and how mature is the market solution?

Then plot each investment on the matrix. Any investment that lands in a different cell than its proposed motion gets a hard re-examination before the budget closes. A custom build proposed for a commodity-mature problem should be challenged. A generic vendor proposed for a company-specific judgment workflow should be challenged. A hire proposed for routine repeated work should be challenged unless that person is there to define the system.

## The human work does not disappear

The cheap version of this conversation turns into AI versus people.

That is not the serious version.

The serious version says that people should stop spending their time on work that no longer needs human attention, and companies should stop pretending every human task has the same shape.

Some work should become software. Some should become an internal workflow. Some should become a vendor contract. Some should remain a human responsibility. Some should wait.

The human work that remains gets more important, not less. Someone has to define the standard and know when the output is wrong. Someone has to build trust with the customer, clinician, regulator, partner, or employee. Someone has to decide which risks are worth taking, maintain the workflow as the business changes, and notice when the agent is optimizing for the wrong thing. Someone has to decide what the company is trying to become.

The firm is being forced to admit which work actually needed people in the first place.

A lot of companies will get this wrong. They will cut before they understand. They will buy before they define. They will hire before they redesign the work. They will automate what they cannot describe.

The better companies will be more specific.

They will look at the work directly and route it. They will keep humans where humans are load-bearing and use AI where repetition, scale, and consistency matter. They will buy solved primitives, build workflows around their own context, and wait where the market is still lying to itself.

That is the practical AI strategy most teams need.

Not a grand theory of the future of work. A matrix for the decision in front of them.

![](https://substackcdn.com/image/fetch/$s_!xQuX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ba3d118-fa6a-4f02-800c-7e535d181ee8_1024x1024.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/build-buy-hire-wait-ai-matrix) on 2026-05-21T15:25:28-04:00*

YOUTUBE TRANSCRIPT 
The Cretaceous extinction is coming, right? Gartner has a line that says more than 40% of agentic AI projects will get killed by the end of 2027. Why? I mean, it's pretty predictable if you're in the space, right? Cost, unclear business value, inadequate risk controls. I have seen all of these firsthand. They do happen.

So if you're reading the headline and you're thinking, well, the issue is agentic tech. No, that's not why these issues are coming up. We find over and over again success stories where we see excellent productive agentic workflows. That's why so much money is flowing into this space. This video is about how to think about your investment logic

in your AI projects so that you adequately invest in the parts of the project that truly drive value versus investing in levers that are likely to make you disappointed and you end up on that 40% Gartner list. Look, I had a finance leader tell me last month that her CFO wanted to do AI in orders to cash,

and three vendors had quoted her three different shapes of solution. None of them had described the actual work that she was doing. And I got to tell you, every conversation in this space feels like that, where like the people inside the business are saying, this is what we need.

They don't fully understand what that looks like from a workflow perspective. And there's about 10 million vendors knocking down the door saying, here, we'll sell it to you. This is what you need. I promise you, this is what you need. You don't understand AI, but this is what you need. We need to take a minute

We need to shut the proverbial door to all the vendors for just a second and have a conversation inside the house about where we invest, why we invest, and what is likely to yield success from an agentic workflows perspective. And that is what this video is about.

So here's the first thing that I see going wrong in the conversations I've had a peek in and conversations execs have shared with me privately, etc. First and foremost, AI investment is not an AI question. It is actually a question about the shape of our work. The model question is downstream of that.

The vendor question is downstream of that. The dashboard or whatever you want to build and show is downstream of that. What sits at the root of the whole conversation is how the work itself is shaped and accomplishes value. But it's really hard to talk about that. We don't have a good vocabulary for it.

And I find in practice, most teams skip that step, especially if they're vendors. encourage them to do that, which so many do. Let me give you an example here. An accounts receivable team does not have one singular AI problem in the space. They have half a dozen, maybe eight. They have to tackle collections prioritization.

They have to tackle invoice matching, customer follow-up, exception handling, cash application, dispute resolution, reporting, and escalation. Those are all very different shapes of work. They route to very different investments, like you might buy some, you might build some, etc. If you pile all of them into a single RFP, which I see happening a lot,

you're going to get a mediocre tool that does maybe one of them well and isn't adequately covering what you really need and maybe covers a bunch of other stuff in another department. It's just not going to be a great fit. What if we look at product? It's a similar situation, right?

User research synthesis is in one shape of work. Spec drafting is in another shape of work. Backlog grooming and design review and experiment analysis and roadmap judgment and launch coordination and customer escalation are all different shapes of work. Maybe some of them are builds, maybe some of them are buys.

The unit of decision for AI is not your department head. It's not a particular role. It is that work that I am naming. Now, quick definition before I go farther. When I say workflow, I don't mean a prompt. I mean the entire operating loop.

What information comes in, what the system is allowed to do, and what good output looks like. Who's checking what? What gets escalated? Who owns and is accountable for what the result is? The AI model is a tiny, tiny part of that loop. It does make the whole thing go. It's like the brains of the business.

I get it, right? It's a big deal to have an AI model in a loop. That's why we're having this conversation. But it's not the only thing, and if you want to understand how to invest correctly, you have to think less in terms of model and more in terms of the workflow because

the workflow is what you are actually investing in. That's what gives you leverage if you do it better. Once you get to that level, the question becomes much easier to follow. Every workflow can be evaluated. There are a handful of obvious inputs, how often a workflow repeats, how costly a mistake is in that workflow,

how much judgment does that workflow need, how specific to you is that workflow. Does the market have a solution here? Is the next model release gonna eat this workflow? Where does the workflow output go? So I want you to think about your workflows, think about your high priority workflows in that sort of deeply enmeshed, detailed understanding.

and I want you to then walk into your investment decision from there. Then you walk into, well, do I build? Do I buy? Do I wait? Do I kill the workflow? Do I hire for it? You really only have five options or five levers when it comes You can either automate it away.

You can also call that eating or deleting the workflow. It's similar. You can build that workflow in detail with AI and it's a complicated workflow and it's not fully automated, but there's big AI components. You can just buy a solution off the shelf and take care of it.

You can hire and those smart people are supposed to help you make the right calls. or you can just do nothing and wait. And by the way, oftentimes the solution is a mixture of those. So you have to think about moving more levers at once. Like I've seen cases where someone wants to build,

but they need to hire to build first, for example. Of those levers, the easiest call is to automate. If you're going through your workflow priorities, automation is the one that most teams understand. Automation, deleting, eating the workflow, it's the right call when the work repeats often, follows a clear pattern, has recognizable

multiple exceptions that you can define and you can check if it's good really cheaply. So IBM Ask HR is a great example there. Another one, if you're thinking, well, that's build, Nate. You're doing multiple levers. Yeah, we're doing multiple levers. Another one is a buy lever plus an automate lever, and that might be FIM.

So Fin is an agent from Intercom and is really tasked with sort of tackling repeatable customer support case volume. Now there are folks that build that, Fin is a case where you can buy that, but it's a similar idea. But whatever it is, you cannot be religious about automating.

You need to be focused on where the value is in the system and where AI can handle it versus where a human can handle it better, whether you're dealing with internal or external audiences. Regardless, automation makes sense where routine cases dominate and exceptions are easy to understand.

Don't automate when the exception is where most of the value is. And by the way, I think this is where a lot of bad enterprise AI demos start to fall down. The vendor shows you the routine case in the deck, and the buyer signs the contract because the routine case is impressive,

But the buyer never realizes that their production traffic is a lot of exceptions and the executive team is staring at an accuracy number that's very low, wondering why they were lied to. Well, nobody was lied to. The buyer just bought the wrong thing, which happens a lot right now, which is why I'm making this video.

If you want to dig into what is a full scoring template, how do you understand how to have a good conversation around whether to buy, whether to invest in building, whether to hire, how do you balance all of that for particular applications. I have a very detailed rubric that I put together on the Substack for that.

But for now, I want to focus on these big levers in this video so you understand how to start to pull them. So automation I think is the easiest one. The next category is one that a lot of executives get excited about and they don't really know how to allocate money efficiently here.

So I'm talking about building here. I'm talking about the idea that The work shape that you select is not suited to purchasing because it's unique, because it's something that has a lot of edge cases, it has a lot of exceptions. It's something where you have company-specific context that matters, your data, your standards, your approval gates, your risks.

It's your team's way of doing the job. It's the secret sauce. And obviously, you are ready at that point if you're building to invest, right? This is not a chat box solution. We're talking about having the right repeatable where you may have skills involved, you may have connectors like MCP, you may have plugins,

you may have data calls, you may have sub-agents, you may have even vendors with tools that you call inside this. Remember how I said you'd have multiple levers? Well, you might buy a lever that is a tiny part of that loop in that workflow and then you build most of it.

So the hard part here is making sure that you understand what is the data that you need to put into this workflow, what does good look like for this workflow, and how do you that the output at the end of that workflow is going to be up to snuff, going to be great,

going to be fantastic if you try to build it. Because right now, presumably if you are in business, the humans can already do it pretty good. If it was easy to automate and delete, you would have automated and deleted it. There is something complicated enough here that you need agents and data and tools

and connectors to do all of that. And I'm asking you, and this does not get asked enough, do you have bounds around that task? Do you understand the edges of that workflow? Do you understand all the bits that go into it? I named a bunch of them. And do you know what good looks like at the end?

Because your team is going to come back to you and they are going to be incentivized to tell you, yep, this is good. Yep, we built the AI thing. The AI thing the executive wanted. We did it for you. It's amazing. Okay. Do you know if it's good or not?

Can you be the honest third-party eyes that say, you know what? This actually works. Or you know what? This is terrible. It's unacceptable. Go back and build it again. Or I gave you the wrong mission and you couldn't build it. You need to have people. I'm going to hire people. Whatever it is.

That level of clarity around value is missing from most of the build conversations that I get told about, that I've sometimes been in the room for. And even though we've had this massive gain in agentic pipeline value, agentic pipeline skill, agentic pipeline impact in the last four or five months, This conversation keeps repeating.

The people in the room buying have not upleveled their conversation in response to what we can actually do, and they aren't realizing how important it is that they, the executive, understand what good looks like if they're going to be suggesting building. So often it's like, you go build it, we can't afford to buy it,

and we can't afford to hire people, so you go build it and it better be good. And they can't tell you what good looks like. That is not a solution. That is not a solution. So that's the build level. Now we come to buy, right?

It's often build versus buy, so I thought putting them next to each other made sense. Buy is really a question of whether you have the capability to take the thing you're purchasing and apply it to your workflow in a way that gives you value back right away. And that's a lot more complicated when you're talking about

You need to understand what is the underlying substrate that your purchase solution will sit on. Is it a data substrate? Where is it going to sit in your system? And then how do you know that your dev team is going to be able to to integrate it well and actually get you value.

And that's always been a very high level question in software, but because software traditionally has been so bounded, it's been a really clean box, you can at least have that conversation cleanly. With workflows, if you're buying a solution that is effectively a part of the workflow, it's And that's why when I talk about buying,

I often will separate it out and I will say you want to either be buying primitives like basic components or services that you can stack into a lot of agentic workflows that you build and those are fairly easy because then if your dev team likes them, they'll use them a lot.

I think Stripe has put a lot of agentic primitives out there right now. that are actually very easy to get started with. You're not making a big purchase decision. You're just starting to play with them and build with them and your dev team can put solutions together. And that's great.

Or you want to be in a position where the primitives are something that allow And so there's some tools out there where you're starting to have tools that help your AI that you build communicate with other AIs in your system. So that's sort of a normal way. You may buy that one piece,

it may integrate with your particular tools, and you may build around it. And then there's the folks who, kind of like Harvey, for example, for legal, they sell the whole thing. It's a whole agentic pipeline, effectively, under the surface. And you have to decide if that works with your workflow as a legal firm or a legal department.

And so when I look at all that, the hardest to most complicated one is sort of the Harvey case. How do you decide that buying Harvey makes sense? And I think the heart of that question is, if you were to look at the work that you're doing today, is it kind of Harvey-shaped or not?

Do you know their product well enough to answer that question? If they're selling you a workflow, and in this case, I don't care that it's legal. Now, hiring. I'll be honest with you, a lot of companies right now are trying to find the impossible hire, the purple unicorn, the domain expert who's an AI builder,

who's a systems architect with executive experience and a change leader. Sometimes that person exists more often than not. And if not, the market is going to clear out a lot of AI talent from under you while you figure out what you actually want.

And so I think the better question if you're looking for AI talent to hire is to ask yourself what kind of human capability that you're putting together actually need in six months or a year and then hire for that missing piece that you don't have on your existing team. Maybe it's domain trust. Maybe it's workflow engineering.

Maybe it's evaluation design. Maybe it's executive ownership. I don't know what it is, but that is a much more sustainable way to hire than to just say we need the perfect AI unicorn. And I think that this is something that's a good sort of reminder for all of us

because I get that we have talent issues with AI. People are coming to me saying, can you help me find talent? And the answer is I know lots of folks. I'm looking for lots of folks. I bring folks together where it makes sense. But ultimately,

you need to be in a place where you understand your work well enough and how you're investing in your team long term well enough and how your team's gaps align to the workflows you're building to be able to make a coherent job description. that is for a specific person, not a purple unicorn,

and who you can hire for in that market and really assess. One of the things that makes hiring really hard right now is that people are trying to sift through all the noise from the AI-generated resumes and maybe AI deepfakes on video and all of the fluff around hiring and the complexity of the market,

really a broken hiring market right now. And at the same time, they have never had And so they're trying to sort of wade through the fog of their own job description and also wade through the fog of the market and it's just a disaster. It takes months to clear roles. It's frustrating for candidates. It's frustrating for companies.

It doesn't make sense. Hire more specifically and again the workflow is a key the workflow helps you unlock that hiring definition and what what hire gaps you really have versus what your team can grow into and you really should be at a point where you can say if my

team or someone on my team can level up in six months to get to this particular talents that I need for where I want to go with my workflows Keep them inside the house. Train them up. Level them up. Do not hire for that because it's just, it's so painful to hire right now.

And I know that there will be people who are listening to this video who are like, ah, you know, it's me. I'm raising my hands. I'm here. And look, I get it. But on the hiring side of the table, it looks like 10,000 people saying, I'm here. It's me and raising their hands.

And how do you know which is which? And so we've talked about that. I've talked about Talent Board, which is a community that we're standing up along with Substack. to help folks to connect over hiring roles and over proving that they have AI talent. It's early days but I'm excited for that.

And ultimately where we want to go here is we want to be in a position where we start to clear the fog out of the market And if something like Talent Board or another tool helps you to understand who actually has AI skills versus who says they do,

and then if you take this video seriously and you start to actually define your role as a hiring manager and you start to understand how your role aligns with workflows, I think you'll be in much better shape to go wherever you go with your hiring

journey and actually get clear answers on the AI talent and actually pick up AI talent before the market clears it out from under your feet. And that's really my goal, right? If you're gonna choose to hire, hire clearly and hire quickly. And that takes a lot of work on your part up front to define against the workflow

you're looking to get to. Okay, waiting is the last motion, and it's the most counterintuitive when the world is shouting at you to do AI. I am not saying, by the way, that you should not be leaning into AI transformation. That is not what this is about.

I am saying you should be deliberate about where you apply AI for leverage in your business first. Let's say your whole business probably needs AI transformation, which is a fair basic assumption for most businesses. Think about where you get the most leverage from going first,

and when you have things that are workflow shaped that are lower on the priority list, think about waiting. Maybe it doesn't make sense to start there. You have limited resources for change management in your firm, by definition. Apply those resources where you get the most bang for the buck.

Apply them where you get the most leverage from transforming the workflow, the most leverage on your people from learning how to work in an AI-native way, and then you can spread out from there to drive the change. And so I'm not saying wait forever. I'm not even saying wait for a year.

I'm saying stack your investments and make sure that the right ones are up top and deliver disproportionate leverage. Because there's a lot of people who will tell you, well, if you're waiting, you're too late, etc. In the larger sense, if you are saying, I don't want to do AI, I would fully agree. You are too late.

It is a problem. You got to get on board with that as a company, as an individual. Fully agree. But within that, and this is true for individuals as much as firms, you have to understand where you want to prioritize that time. And there will be some things that you don't want to prioritize because it's just

too much work to change, right? Like I'll give you an example. If you're trying to rewrite your analytics system, You may not want to prioritize changing the SQL query polls too fast because SQL just works for you and you can get deterministic polls and data and it's just not

broken and so it's not the first thing you're going to fix and you're going to focus on natural language descriptions of the analytics and storytelling and things that you can only do with AI to give you a lot more upstream leverage and that's a

very small example but it illustrates what I mean when I talk about weighting and why weighting makes sense in certain cases. Now there is one principle that I have been dancing around in this whole video that I want to say very, very plainly. If you remember nothing else from this video, remember this.

Do not automate what you cannot describe. And this is a line that should sit in every single AI investment review. If you cannot describe the work you're doing in really plain English, well, what's your inputs? What's your outputs? What are the standards here? What are the exceptions? Who owns it?

It's gonna be really, really hard to make good investment decisions. And a lot of AI projects right now fail before that conversation ever comes to a conclusion because the team that wants to propose the AI thing doesn't have clean, clear words like I just described to talk about what they mean.

They're hiding 20 workflows inside the same broad-ass to the vendor. They are talking about broad outputs that could mean six different things and everyone inside the room is reading that differently. They're putting broad words in the job description that they're hiring for and everyone's talking about that differently and interviewing for it differently Be

specific so that you can get impact for your AI investment Please, please, please Now, if you want to dive into the operational layer, what actually makes agent work in practice useful and high yield for the firm, I have a whole deep dive on that in the Substack today. I think it goes with the whole conversation here.

I didn't have time for it in this video, but it's a good reminder that you need to be thinking about agent capabilities and agent workflows end to end. as a leader if you're going to make a build by higher weight decision. And so I wanted to dive deep on that.

Before we go farther, let's look very classically at an investment matrix because I love these. I've seen these in so many board decks. We're going to look at investment matrix and how you think about decisioning. So let's do that here. So what you have is two axes.

First, an axis about how specific this work is to your company. Is it super specific or is it pretty general and everyone in the space does it? An example of that would be everybody does customer service in telecom. That's not a specific thing, right? That's not special. But on the other hand, if you have very,

very specific plan switching incentives that are driven by a long term marketing motion and nobody else has those, well that might be specific. The second axis is vertical and it is how mature the market solution is So, very high level, right? These always have four boxes, and I want you to get the takeaway here.

If the work is common, general, right, and the market is mature, Now, if the work is common and the market is not mature, You want to prototype narrowly or you want to wait. The category is still defining itself. You don't want a five-year contract for a tool category that will look different in 12 months.

And if you want to invest here, you want to be prototyping and building because you have a chance to win the category. So this sort of depends on your vision for the company, where you want to go here. Now, if the work is company-specific and the market has some useful primitives, buy the primitives, buy the building blocks,

buy the tools you can call, but you own and set up the workflow that everything runs on where the value lives. This is where most ambitious teams ought to be living right now. You want to buy the connectors, you want to buy the model, you want to buy the orchestration, and you want to own the standard.

Now, some people, of course, are standing up their own open weights models. That's another way to do it. But regardless, you build it and you just bring in the building blocks as you need it. Now, there's a bit of a blurry line here, but if the work is company specific and the market is very thin or immature,

you want to definitely be building because there's value there. And you want to make sure that you're building in a way that enables you to own that category. That's a very easy call. If you're wondering, hiring cuts across this grid, you need to define your workflows to get the hiring right. And by the way, pro tip,

if the work you're trying to define is something that nobody is able to define well, if it requires trust, if you need to frame it up, if someone needs to define the standard and what goods looks like and you're like, oh gosh, Nate, I don't have that, that's a clue that you should be hiring.

Your next investment is probably a person. And you need to think about what person that is and how you can define their role in such a way that they're set up to enable that larger workflow decision to be helpful, correct, and long-term impactful for the business. And if you're wondering, does this mean the executive role is changing?

Absolutely. We're talking about a change in how we allocate capital and a need to understand agentic workflows in more detail to do that well. The job is not to become the person who personally evaluates every single tool. I'm not advocating that. The job is to understand enough about the workflow you're investing in to make

really good capital allocation decisions, which is what we're doing, right? If you're hiring, if you're building, if you're buying, if you're waiting, those are all capital allocation decisions. and you have to define what are the outcomes that matter? What are the problem frames that matter? What are the workflows that you should prioritize?

Where do you want to allocate talent in that mix? And then how do you set up your teams to be successful as you think about these larger workflows that you want to unlock for AI and you want to prioritize for AI? And so what I'm advocating is essentially,

instead of looking at AI as a sort of a singular blob that you want to have a conversation about where your CEO says, let's do an AI strategy, no. Don't do that. Instead, look at the workflows and make good investment decisions once you understand those workflows. One last thing before we close.

There is a very cheap version of this conversation I hear a lot that tends to turn the debate into AI versus people. I don't think that is a serious version. It's not a helpful version in most cases. The serious version of this conversation asks where people should be maximizing their time, where they should be up-leveling,

where there are talent gaps you can hire for, and where we have cases where people need That is a much more serious conversation. It's one that is productive. It's one that's useful. It's not one I hear nearly as much as the drama-filled version. which is AI versus humans. It's not useful. Ultimately,

the human work that remains in this version as we look at these workflows is getting more impactful and more leveraged because we are putting AI and powerful logistic systems at the heart of the business and we need to get that right. And that is a people problem. And so this is not AI replacing workers.

This is figuring out how to make investment decisions that unlock disproportionate value that get you out of that Gartner 40% figure and get you into a place where you're getting real value back on that agentic investment. And it starts and ends with the workflow. If you take nothing else away from this, understand your workflows,

be able to talk about them specifically, and have discrete investment conversations about those particular workflows that matter most to your business. And that's going to set you up for success in a way that most conversations that start with, we need an AI strategy, will not. Best of luck, and I'll see you next time.