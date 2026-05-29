---
title: "Your agent dashboard is green. The run underneath it is where the work actually broke."
source: "https://natesnewsletter.substack.com/p/agent-product-analytics"
author:
  - "[[Nate]]"
published: 2026-05-27
created: 2026-05-28
description: "Watch now | The unit of product behavior is shifting from the session to delegated work."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management, claude-mastery]
ai-context: "Nate Jones argues the unit of agent product analytics is the agent run, not the session — ship agent_run_started + task_completed + user_correction_submitted joined on agent_run_id, then separate completion from acceptance to see which workflows have earned more autonomy."
---
A Cursor agent deleted a software company’s production database and its volume-level backups in nine seconds.

This was late April 2026. The founder, Jer Crane of PocketOS, watched it happen. It is the kind of story that gets passed around because it reads like a warning about how dangerous agents have become, or how badly one vendor failed. That reading misses the more interesting thing, which is that nothing on a normal product dashboard would have seen it coming. An active user, a long session, a healthy pile of chat messages, a feature getting used. All green, right up until the moment the database was gone.

Everything that actually mattered happened inside the run, and that is precisely the part most analytics cannot see. When the user is an agent, the unit of product behavior is becoming the agent run: the work a user handed over, the steps the agent took, the tools it touched, the boundaries it hit, the corrections it got back, and whether anyone accepted the result.

For the first time in the history of software, we can watch the consequences of our decisions land in real time. You used to make a call, ship it, and wait weeks to learn whether it worked. An agent collapses that loop to minutes, and if you get good signal back while it runs, you can shape and steer it mid-flight. Speed is the engine. Analytics is the rudder. A database that vanishes in nine seconds is what happens when you have a powerful engine and no way to steer.

**Here’s what’s inside:**

- **The events that are the new clicks.** What to actually count when the user is an agent and the click, the page view, and the session have stopped telling you anything useful.
- **Why your traces aren’t your answer.** Engineering already has the execution data. Why that’s necessary, not sufficient, and what product still has to build on top of it.
- **The difference between a task that finished and a task the user trusted.** Reading that one gap is how you tell which workflows have earned more autonomy.
- **The starter setup.** The three events to ship this week, the full event schema underneath them, and the prompts that turn that schema into instrumentation in your own stack, your corrections into eval cases, and your numbers into a roadmap.

Most teams have filed all of this under engineering telemetry instead of product, and that is exactly why the runs keep going fast in the wrong direction. This is how you get the rudder.

## LINK: Grab the prompts

The traces already exist, so the analytics question gets handed to engineering. What you get back is activity you can see and work you cannot judge. These three prompts exist to keep that from happening to you, and they chain on the one identifier that holds an agent run together. The first one takes your language, your framework, and your analytics sink and writes the three starter events as code you can ship this week, so the schema in this article stops being a diagram and starts emitting. The second one takes the corrections and failures those events capture and drafts the eval cases, because a denied approval or a memory miss is a label your users already wrote for you and most teams throw it away. The third one reads your completion and acceptance numbers through the four quadrants and tells you which workflows have earned more autonomy and which are finishing work nobody trusts. Instrument the runs, learn from the corrections, read the trust. That is the rudder. Without it you are just going fast.

The scale is the part that makes it urgent. [Over the last year I have shipped something close to 55,000 developer-years of equivalent code, which works out to roughly 10 billion tokens of output](https://dashboard-sepia-beta-83.vercel.app/). At that speed the thing that determines whether you are building something good is not how fast the work moves. It is whether you can see where it is going and correct it before it arrives.

## The product event moved

Most product dashboards were built for human navigation.

Did the user show up, and if so, did they click? Did they come back? Did they move through the funnel and convert?

Those questions still matter. They are just no longer enough.

In an agent product, the action that matters is an instruction, not a click. The event worth counting is a tool call, not a page view. And the failure that hurts is rarely a user dropping out of onboarding. It is the agent retrying the same action, hitting a permission boundary, asking for approval, losing context, or finishing work the user then has to rewrite.

A team can ship an AI feature, watch usage climb, read long chat logs, and still have almost no idea whether the product is doing useful work.

The old funnel ran on human navigation. Page viewed, button clicked, form submitted, signup completed, user retained. The agent funnel runs on delegated work. Intent received, plan made, tools chosen, actions attempted, approvals requested, permissions checked, work completed, output accepted or sent back to be redone.

That second funnel is the one that matters when the product is doing the work for you.

## Chat logs are not product analytics

The first mistake is treating the chat transcript as the analytics system.

Chat logs are useful. They tell you what the user said and what the agent replied. They help with qualitative review. They can reveal weak prompts, missing context, bad tone, obvious hallucinations, and places where the product is confusing.

But a chat log does not tell you enough about the work.

It usually does not tell you which tools were available, which tools the agent called, which calls failed, where it retried, where permissions blocked the work, or whether the user accepted, corrected, interrupted, or finished the task manually.

Even when some of that signal appears in the transcript, it is trapped in prose. One person can read one transcript and learn something. A dashboard cannot pull that apart and aggregate it the way you need when you have hundreds or thousands of agents running in production.

This matters because chat activity can look healthy while the work underneath it is failing. If you live in a chatbot mental model, that activity is exactly what you think you should be watching.

A long chat may mean the user is exploring a complex task. It may also mean the agent is forcing the user to restate context, fix errors, approve obvious steps, and route around missing product structure. In most dashboards, both collapse into the same metric. Active session.

That is not enough for an agent product. The question is no longer what the user typed. It is what the agent tried to do once the user handed over the work.

## Observability is not enough either

Developer observability already points in the right direction. Tracing tools can capture model calls, tool calls, handoffs, guardrails, latency, cost, and errors during execution.

That data matters. Engineering teams need it.

But trace data is not automatically product analytics.

A trace is good at the mechanics. It will tell you that a tool call failed, that the agent asked for approval, that a run cost thirty cents. What it will not tell you is whether any of that mattered. Did the failed call cost the user anything, or did the workflow finish anyway? Did the approval buy real safety, or just slow everyone down? Did the thirty cents move a task the customer actually cares about? The trace records the event. Whether the event was good or bad for the product is a separate question, and it is the one product analytics has to answer.

The trace layer is also where you choose tooling, and the choice should follow the use case rather than fashion. Use [OpenAI traces](https://openai.github.io/openai-agents-python/tracing/) if the product is built on the OpenAI Agents stack. Use [LangSmith](https://docs.langchain.com/oss/javascript/langgraph/observability) when the product is built around LangChain or LangGraph. Use [Helicone](https://docs.helicone.ai/guides/cookbooks/cost-tracking) when vendor-neutral observability and cost attribution are the immediate pain. Use [Braintrust](https://www.braintrust.dev/articles/llm-observability-guide) when traces need to become eval cases. Use [Langfuse](https://langfuse.com/docs/observability/overview) or [Phoenix](https://arize.com/docs/phoenix) when open-source or self-hosted tracing matters.

And keep that instrumentation off the critical path when it does not have to be there. Write traces asynchronously, sample the heaviest payloads, keep hot product metrics separate from cold debugging records, and make cost per completed task a first-class metric. Observability that makes the product slower will eventually get turned off.

This is the layer most teams still have to build.

The product team needs to translate agent execution into product questions. It needs to know which workflows fail most often and which tools are unreliable, which approvals actually change outcomes and which are just friction. It needs to tell the permission blocks that protect the business from the ones breaking the product without anyone noticing, spot the tasks that look complete but keep getting reopened, and see which outputs users accept without edits. Underneath all of it sits the question the roadmap turns on: which workflows have earned more autonomy, and which still need a human steering.

## The agent run is the work unit

A session tells you that a user showed up. An agent run tells you what work was attempted.

A run might begin when a user asks for customer support, invoice reconciliation, meeting preparation, contract review, code repair, candidate movement, or account research. The workflow changes by product. The analytic problem does not.

Once the user delegates work, a different set of questions takes over. What was the user trying to accomplish, and did the agent understand the intent? From there it is a chain: which tools did it use, which calls failed, did it ask for approval, did a permission policy stop the action? Did the task complete, partially complete, fail, or get abandoned, and did the user accept the output or redo the work themselves?

They tell the team whether the product is easy for an agent to operate inside. They reveal where the agent has enough context and where it is guessing. They expose whether the permission model is too loose, too strict, or just confusing. They show where users trust the agent and where they take control back.

Salesforce is a useful market signal here.

In its fiscal Q4 earnings release in February 2026, Salesforce introduced Agentic Work Units, or AWUs, to measure tasks accomplished by an AI agent. The company said 2.4 billion AWUs had been delivered to date across Agentforce and Slack, growing 57 percent quarter over quarter. Benioff described an AWU as one unit of agentic work, and admitted on the same call that the company is still figuring out exactly what the number means. His CMO, Patrick Stokes, was more concrete: an AWU is a record updated, a workflow triggered, a decision made, an MCP call. The work coming out of the system, not the tokens going into it.

That is a real shift. The largest enterprise software company on earth is now trying to name the work unit instead of counting seats, sessions, or tokens.

The company is running 2.4 billion of these and still cannot say precisely what one of them means. That is honest, and it is the whole problem. A work unit only helps if the team knows what kind of work happened, what workflow it belonged to, whether the tool calls succeeded, whether the user trusted the output, and whether the business outcome moved.

Without that, the new metric becomes the old problem with a better name. Instead of staring at chat volume, teams stare at work-unit volume.

The product team still needs the run-level view.

## What to actually watch

A serious agent product tracks the behavior that explains whether delegated work is succeeding, not just whether it is happening. A few of those signals carry more weight than the rest.

Approval is one of the strongest trust signals in the whole system. Track how often approvals get requested, granted, denied, modified, ignored, or expired, and break that down by action type and risk tier. The pattern tells you something the completion rate never will. If a high-value action always gets an approval dialog the user always accepts, the approval is friction with no safety. If a high-risk action gets approved in half a second every time, the approval is theater. If users keep denying the same class of action, the agent is proposing the wrong work.

Memory misses are the quiet one. A memory miss is when the agent should know something and does not. It asks for a preference the user already gave, forgets a team standard, applies stale context, or fails to retrieve a decision that was made last week. Users read every one of those as the product being careless, even when the model did nothing wrong.

These are the events that turn a flat completion number into a story about where the work breaks.

## Corrections are the label set

One of the most valuable signals in an agent product is the correction.

When a user interrupts an agent, edits its output, denies an approval, gives a clarification, or reopens a completed task, they are doing more than using the product. They are labeling it.

They are telling the product team what the agent misunderstood, what context was missing, which action felt unsafe, and which output did not meet the standard.

That is why agent analytics and evals belong close together.

A denied approval can become a test: should the agent have proposed that action? A memory miss can become a retrieval test: should the agent have found the relevant preference or policy? A failed tool call can become a schema test. A user correction can become a quality benchmark. An abandoned workflow can become a research queue.

This does not mean every prompt, customer record, and model output should be thrown into a training system. The privacy treatment has to be explicit.

Capture typed metadata by default: workflow type, tool name, status, risk tier, latency, cost, and outcome. Be careful with raw prompts, account data, customer records, internal documents, and full model outputs. For sensitive workflows, store redacted summaries or references and keep the source payload behind the customer’s existing data boundary.

Product analytics should help the team see the work without turning every trace into a compliance problem.

The reason corrections matter is that they are high-intent. The user is not browsing. They are trying to get something done. When they correct the agent, they are showing you exactly where the product’s understanding of the work falls short of their real standard.

## Completion and acceptance are different

Most product teams will track task completion and call it done. Completion matters. It just is not the finish line.

Completion means the task reached a finished state. Acceptance means the user trusted the result and used it. Two different outcomes, and the space between them is where the product really lives.

If completion is high and acceptance is low, the agent is finishing work users do not trust. If completion is low and acceptance is low, users are bailing before the product reaches a reviewable state. If completion is low and acceptance is high, the product is too cautious but valuable when it does fire. If both are high, the workflow may be ready for more autonomy.

Completion without acceptance is the blind spot. It is the one thing most dashboards cannot show you today.

That is where the product conversation gets better. Not “engagement is up.” Instead: which delegated workflows are trusted enough to get more autonomy, which ones need better product structure, and which ones should stay supervised.

## Ship three events first

A team building an agent product does not need a giant event catalog on day one. It needs enough structure to join the human session, the agent run, the tool trace, and the business outcome.

Start with three events: agent\_run\_started, task\_completed, and user\_correction\_submitted.

Tie all three to the same agent\_run\_id, and carry the basics on every event: user\_id, account\_id, workflow\_type, status, timestamp, and trace\_id where a trace exists.

That small set is enough to see completion rate and correction rate by workflow. Everything else earns its place as the product gets real usage.

When you do expand, here is the set worth instrumenting and what each one means:

- `agent_run_started` — the user has delegated a task to an agent.
- `tool_call_failed` — the agent tried to use a tool and the call failed, with a typed failure reason.
- `approval_denied` — the human rejected a proposed action.
- `permission_blocked` — the system stopped the run because the user or agent lacked the needed scope, role, credential, or policy clearance.
- `user_correction_submitted` — the user corrected the output, plan, tool choice, or assumption.
- `memory_miss` — expected memory or prior context was unavailable, stale, or wrong.
- `escalation_triggered` — the agent handed work to a human, admin, reviewer, support queue, manager, or another system.
- `task_completed` — the run reached a completed state the user could actually use.
- `task_abandoned` — the user or system gave up on the run before completion.
- `business_outcome_recorded` — the run connected to a real outcome, like an email sent, a ticket resolved, an invoice reconciled, a meeting scheduled, a pull request merged, a customer retained, or a report delivered.

Salesforce’s AWU framing points to the right business question: what work did the agent accomplish? The product team’s version has to go one layer deeper. What workflow was the unit part of, what happened inside the run, and did the user or the business accept the result?

Start measuring the work instead of only measuring the surface.

## The product question changes

For most of product analytics history, the question was simple. Where can I see user behavior?

The question now is harder and more interesting. What work did the agent try to do, and where did it break?

That moves your attention off the visible surface and into the system underneath. Interruptions, retries, handoffs, approvals, memory, permissions, corrections, outcomes. Those are the new clicks of the agent era. They are the events worth counting, because they are the ones that tell you whether the work is going anywhere good.

A good agent product does much more than produce a fluent answer. It moves through work with the right amount of autonomy, asks for help at the right moments, recovers from failure, respects permissions, uses memory correctly, and produces outcomes people trust. You cannot see any of that in a chat-volume chart.

So this week, ship the three events. Compare completion and correction rates across your top three workflows, then add acceptance. High completion paired with high correction means the agent is finishing work nobody trusts. When permission blocks pile up on a single workflow, that workflow needs a different surface, and when corrections concentrate on one tool, the tool contract is the thing that is wrong.

This is the part I keep pushing on. Too many teams hand the whole question to engineering and decide the traces are enough. Traces are necessary. You build product analytics on top of them. But if you want a real opinion about whether the agent runs are worth anything, you need the run-level view and a schema built for it. Without that, all you are seeing is activity, and then a result like the database that vanished in nine seconds, and you are standing there asking why.

Flip it around. With the run-level view, the better question is the one you can actually answer. What was the history of agent behavior on this workflow that we could have seen, understood, and predicted off of? The nine-second deletion was an autonomy and permissions failure, not an analytics failure, and no dashboard stops a destructive call in the moment. What the run-level view buys you is earlier. You should be able to spot a workflow producing defective runs long before any agent gets near a delete command. That is what the rudder is for.

Everyone else will be staring at chat volume. And chat volume is activity. It was never evidence that the work succeeded.

The teams that instrument agent behavior now are the ones who get to steer. The rest are just going fast.

![](https://substackcdn.com/image/fetch/$s_!e9Ah!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4bef4c4-69f2-4940-983f-037f1bf34efc_1254x1254.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/agent-product-analytics) on 2026-05-28T17:17:24-04:00*

YOUTUBE TRANSCRIPT

We have never had a chance to look at the impact of our decisions in real time. And now we do with agents. And we think of this as a problem. We think of this as, oh, there's more evals to do. Nate’s Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter To have agents that we can guide.

To have agents that have good boundaries. Because effectively we have 10X or 100X or 1000X our ability to get stuff done. We gotta shape this speedboat that we built. It's really important. A cursor agent reportedly erased Pocket OS's production database and backups in nine seconds.

That is the kind of sentence that gets passed around by CTOs because it sounds like a horror story. It's a small software company, it's a production database, The obvious story here is that an AI coding agent went rogue, right? I don't think that's the most useful story here.

I think the more useful story is that most product analytics would have missed the actual product failure. A normal dashboard might show an active user, it might show a long session, it might show that the AI feature was used, it might even show a lot of messages in chat.

But none of that tells you what happened inside the agent run. What instruction was the agent given? What environment did it think it was in? What credential did it find? What tool call did it make? What permission boundary failed? What did it report afterward? Where did the human trust loop break? This, this is the new analytics problem.

When the user is an agent, product analytics no longer stops at clicks and sessions and messages and funnels. The unit of product behavior is becoming delegated work. And that's the mental model I want to keep in mind for this video. Agent analytics is not a debugging sidebar. It is the way we shape our work.

It is the future of product. For most of product analytics history, the question was very simple. Did the user show up? Did they click? Nate’s Agent failure might not be a user dropping out of onboarding, it might be the agent retrying the same action, hitting a permission boundary, asking for approval, losing context,

or finishing work the user quietly rewrites. Chat logs are useful. They tell you what the user said and what the agent replied. They help with qualitative review. They can reveal weak prompts and missing context and bad tone and obvious hallucinations and places where the product is confusing.

But a chat log does not tell you enough about the work. It usually doesn't tell you which tools were available, which tools the agent called, which calls failed, where it retried, where permissions blocked the work, or whether the user accepted or corrected or interrupted or finished the task by themselves.

Even when some of that signal appears in a chat transcript, it's trapped in text. So a person might be able to read that chat transcript and get some insights, but a dashboard can't pull that up and aggregate it in a way that we can scale when we have hundreds or thousands of agents in production.

All of this matters because chat activity can look healthy, and if you live in a chatbot mental model, you think that's what you need. And yet the work can still be failing when agents aren't monitored appropriately. Let me give you an example. A long chat might mean the user is exploring a complicated task,

but it might also mean the agent is forcing the user to restate context and correct errors and approve obvious steps and work around missing product structure. And in most monitoring, both of those cases collapse into the same metric, the active session. This is just not enough for Nogentic product.

Developer observability is closer here, but it's still not the whole answer. And I think most people think it is, right? So tracing tools can capture model calls and tool calls and handoffs and guardrails and latency and cost and errors during execution. And that data really matters and engineering teams definitely need it.

But trace data is not automatically product analytics. Product Analytics has to tell you whether that failure mattered to the user, whether the workflow still completed, and whether the user accepted the result, and whether the product ought to change. So a trace can tell you that the agent asked for approval,

and Product Analytics has to tell you whether that approval created real safety or just added friction. A trace can tell you that a run costs $0.30. Product Analytics has to tell you whether that was worth it. So this is the layer most teams are missing right now. They still have to build.

And the right unit to think about is the agent run. A session tells you that a user showed up. An agent run tells you what work was attempted. A run might begin when a user asks for customer support or invoice reconciliation or meeting preparation or candidate movement in the pipeline or account research.

The workflow can totally change by product. The analytical problem is very similar. Because you ask the same questions. What was the user trying to accomplish? Did the agent understand the intent? What tools did it use? Which calls failed? Did it ask for approval? Did a permission policy stop the action? Did the task complete? Did it partially complete?

Did it fail? Did it get abandoned? Did the user accept the output or redo the work? Those are now product questions that we have to care about. Now, Salesforce is kind of pointing in this direction already. In its February 2026 fiscal Q4 earnings release, Salesforce introduced Agent Work Units, or AWUs, say that five times fast,

to measure tasks accomplished by AI agents. The company said 2.4 billion AWUs had been delivered to date across Agent Force and Slack, growing 57% quarter over quarter. And that's a significant shift because that means Salesforce, the biggest SaaS company on the planet, is not talking about seats. It's not talking about sessions. It's not even talking about tokens.

It's trying to name the work unit. But a work unit is only useful if the team knows what kind of work happened, what workflow it belonged to, whether the tool calls succeeded, whether the user trusted the output, and whether the business outcome improved. Otherwise, the new metric becomes the old problem with a nice name.

Instead of staring at chat volume, teams will then stare at work unit volume. The product team still needs a run level view per agent. One of the most valuable signals in that view is the correction. When does a user interrupt an agent, edit an output, deny an approval, give a clarification,

or reopen a task in the middle of a run? They are labeling that run. They are telling the product team what the agent misunderstood, what context was missing, which action felt unsafe, and which output didn't meet the standard. That's why agent analytics and evals belong so close together. Nate’s Substack

and customer record and model output should be thrown into a training system. The privacy treatment has to be explicit. You can't just do it by volume anyway. But it does mean that the product team should shape product analytics that help us understand how people are actually getting work done with agents.

And the product team's ability to understand mid-agent run corrections is key. Let me give a few examples here. Completion means the task reached a finish date, right? Acceptance means the user trusted the result. Those are very different things. If in a product analytics system, the completion rate is high and the acceptance rate is low, the agent is

Not raising trust, right? It's finishing work users don't trust. If completion is low and acceptance is low, users may be abandoning before the product reaches a reviewable state. If completion is low and acceptance is high, the product may be too conservative but very valuable when it works. And if completion and acceptance are both high,

that's a signal that your workflow may be ready for more autonomy. The gap between completion and acceptance is the part most dashboards have difficulty with today. So if you're trying to get started, where should you ship first? I would say you want to ship three events. You want to understand when your agent runs start,

when your tasks are completed, and when users shape your agent runs in the middle. And you want to tie all to the same agent run ID. That's really critical because it helps you then to get to completion rate and correction rate by workflow.

We really have to step back and think about a different set of questions when we're shaping agent work that works this fast. And that's why I emphasize interruptions and retries and handoffs so much because those are the new clicks of the agent era. A good agent product does much more than just produce an answer, right?

It moves through work with the right amount of autonomy. It asks for help at the right moments. It recovers from failure. It respects permissions. It uses memory correctly. It produces outcomes that users trust. This is the task you are trying to solve with product analytics. You're trying to understand to what extent, as you build an agent product,

is the usage you're getting useful? To what extent is the agent that you are working on able to get this work done in a way that's meaningful? You should be asking yourself really regularly whether you have the product analytics views you need to shape agents at the speed at which they run.

And that question has never been more high leverage. Agents are capable of accelerating work 1000x. But the extent to which we're going in the right direction with them is really a function of the rudder on those agents. And that rudder is product analytics. And I see too many people who are delegating that to engineering,

who are saying the engineering traces are enough. We see the engineering traces and we can shape it and move it. Those are necessary. You have to have engineering traces to build the product analytics on the top. But you really, really need a good data schema and good product analytics if you're going to have

an opinion about the product value of the agent runs. And that's what you need to get useful work done. Otherwise, all you're seeing is activity and then terrible results Nate‒sletter Nate‒ Nate’sletter Nate’sletter Nate’sletter Nate’sletter So if that's you, I've got the start guide over on Substack and I will see you next time.

We've got lots more fun stuff coming. Hey, I never really stop. So subscribe and you won't get lost and you won't get left behind. Cheers.