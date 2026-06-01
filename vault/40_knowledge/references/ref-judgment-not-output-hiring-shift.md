---
title: "You’re Not Being Hired Strictly for Output Anymore. Your Judgment Is What Is in Demand Now."
source: "https://claudecodefornoncoders.substack.com/p/youre-not-being-hired-strictly-for"
author:
  - "[[Daniel Williams]]"
published: 2026-05-13
created: 2026-06-01
description: "Companies are running Agile retrospectives while the production function underneath them has changed. The work that built your career was output. The work that holds it now is judgment."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [life-systems]
ai-context: "Daniel Williams argues AI collapsed the cost of output, so the scarce resource (and the new hiring axis) is judgment about which work is worth doing — interviews shift from 'walk me through a hard implementation' to 'walk me through a hard call'; proposes the one-page 'feature contract' as the judgment-up-front artifact replacing velocity targets."
---
On May 6, [Alfred Lin posted a question on X](https://x.com/Alfred_Lin/status/2052023929993298060): “Every era of computing invented its own way of building software. Waterfall optimized for reliability and control. Agile optimized for velocity and modularity. The AI era will optimize for direction and leverage, but we don’t yet know what to call it. Who’s going to define how we build in the age of agents?” [Garry Tan quote-tweeted](https://x.com/garrytan/status/2052024023861899655) the answer: “Just in time software is here.”

Tan’s framing is half right. “Just in time software” captures the speed shift: agents produce the artifact when it’s needed, on demand, at near-zero marginal cost. But that framing keeps the bottleneck on execution. The bottleneck has moved off execution entirely. Direction and leverage are judgment problems, not execution problems. When AI made the act of writing code cheap, the constraint moved up the stack: from how fast can we ship to which thing is worth shipping, from how do we coordinate the work to who decides which work counts. Waterfall was a methodology over reliability. Agile was a methodology over velocity. The AI era’s methodology has to be over judgment, because that’s the new scarce resource.

That has consequences for what gets people hired. The Agile-era career was built on output: story points delivered, sprints closed, features shipped, throughput measured against capacity. AI just collapsed the cost of every variable in that equation. Output is now cheap, fast, and abundant. Judgment about which output is worth producing, which output got shipped to the wrong target, and which output is creating a future liability is none of those things. You’re not being hired strictly for output anymore. Your judgment is what’s in demand now.

![](https://substackcdn.com/image/fetch/$s_!iAjd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3e5ed20-ae1c-4ab2-9dea-8e18727cb4a4_1920x1080.png)

## The Assumption Built on a Dying Model of Work

Agile and Jira were built on the premise that work is the bottleneck. Story points exist because human execution effort had to be allocated and tracked. Velocity exists because the rate of execution mattered to delivery dates. Sprints exist because work had to be packaged into committable units. The whole apparatus is a machine for managing scarce execution capacity, and it served its era well: fragile systems and long release cycles in the Waterfall era gave way to microservices, decoupled teams, and continuous deployment in the cloud era. The methodology shift was a response to a shift in constraints.

Now, the constraint is shifting again. AI made the act of writing code, drafting a spec, generating a test, or producing a report a near-zero-marginal-cost activity. The bottleneck moved off execution. Most companies haven’t acknowledged this yet. They are still running velocity reviews, capacity planning sessions, and roadmap commit ceremonies as if the work itself were scarce. The framework keeps running. The scarcity it was built to manage no longer exists. Velocity tracking isn’t useless at the team-operations layer. It still measures coordination overhead, dependency latency, and cycle time, all of which matter. It just stopped being the primary signal of value, which is the role it played for two decades.

You see the symptom in retrospectives that go sideways. The team shipped everything they committed to. The metric is green. The customer outcome was unclear, the validation was weak, the product hypothesis was never tested honestly, and nobody is sure whether the right work got done. The retrospective treats this as a discipline problem (“we need better acceptance criteria”) rather than a methodology problem (“the framework we are using doesn’t measure what matters now”).

## What Agents Help With and What They Don’t

Agents help with a remarkable amount of the upstream work. They help with ideation: surfacing patterns, generating options, and stress-testing hypotheses against prior work. They help with research: pulling sources, synthesizing context, and summarizing positions. They help with first drafts: code, specs, plans, decks, communications. They help with exploration: prototyping multiple directions in the time it used to take to commit to one. The pace of input generation has changed dramatically, and any senior person who isn’t using agents for this work is leaving real productivity on the table.

What agents don’t do is make a final judgment about which of those inputs to act on. Take three calls that a senior person routinely makes. Deciding whether a feature is worth building mixes customer reality, business strategy, opportunity cost, and risk. Shipping a draft means weighing audience, stakes, and consequences. Adding someone to the team means dealing with people and politics. These calls get cheaper or faster when an agent can produce the underlying artifact. But they are still constrained by domain knowledge, organizational context, and risk appetite that the agent doesn’t and can’t have.

The result is a productivity profile most organizations are not designed for. The inputs to a decision arrive faster, in greater volume, with more variety. The decision itself takes the same time it always did, and is more important than ever because the cost of acting on a wrong decision compounds at the speed of agent execution. Agents made the inputs cheap. They made the judgment more valuable, not less.

## The Feature Contract as Artifact

If the methodology Alfred Lin is asking about exists, the “feature contract” is a piece of it. The feature contract is an artifact I have been building for months as part of every project I work on now. It forces the judgment up front: what are we building, why are we building it now, who is the user, what is the success criterion, and what does the validation look like before we declare the work done. It is a one-page document that bridges strategic intent and execution. The execution then runs against the contract rather than a velocity target.

User stories capture execution intent: as a user, I want X, so that Y. Feature contracts capture judgment intent: this is the bet we are making about a customer reality, this is the cost of being wrong, this is what success looks like, and this is how we will know we are done. The execution that follows is downstream of the bet. If the bet is wrong, no amount of velocity saves the work. If the bet is right and the contract is honest, the execution becomes a question of taste and time, both of which agents have made cheap.

I run automationresilience.com on this pattern. I run my agent ops business on this model. Every meaningful feature has a contract. The execution moves quickly because the judgment work was done up front, and the agents are fast at the execution. The judgment work, the part that decides whether the feature is worth building at all, takes longer than the build itself does in many cases. That ratio is the new normal. The methodology that follows from accepting it is not a refinement of Agile. It is a different machine running on a different scarcity.

## What This Asks of You

The companies that figure this out first will hire differently and measure differently. The job description that used to read “5+ years shipping production code” is starting to read “5+ years of judgment in domain X.” The interview question that used to be “walk me through a hard implementation” is starting to be “walk me through a hard call you made and why.” The performance review that used to weigh velocity is now weighing decision quality. None of these shifts is universal yet, and most senior professionals are still being measured on the old axis. The transition creates the asymmetry: while the metrics catch up, the people whose judgment is sharpest are pulling away from those whose output was their differentiator.

You used to be hired for the work itself. You’re hired now for the judgment about which work is worth doing. That isn’t a software problem. That’s a belief-system problem, and the belief most organizations still operate under is that more output is the answer.

The exercise to run this quarter: pick one decision you made in the last month that turned out to matter more than the work that followed it. Write down what you actually weighed, who you talked to, what you considered and rejected, and what you would do differently. That is the artifact of your judgment. It is also increasingly the thing you will be paid for.

---

Daniel Williams advises clients about AI tools, strategy, and human resilience at [dewilliams.co](https://dewilliams.co/).

---

[Claude Code for Non-Coders](https://claudecodefornoncoders.substack.com/) publishes on Tuesdays and Thursdays. If you found this useful, share it with someone who’s still measuring output.

---
*Clipped from [substack.com](https://claudecodefornoncoders.substack.com/p/youre-not-being-hired-strictly-for) on 2026-06-01T17:28:09-04:00*
