---
title: "Exclusive: a conversation with Tibo from Codex on what your company has to become when the model can actually do the work"
source: "https://natesnewsletter.substack.com/p/codex-five-leadership-chairs-tibo-interview"
author:
  - "[[Nate]]"
published: 2026-05-15
created: 2026-05-21
description: "Watch now | Between the launch of the new Codex and GPT-5.5 and now, something happened in my own house that has stayed with me more than any benchmark."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management]
ai-context: "Tibo (Codex) interview on the five leadership chairs your company has to fill once the model can actually do the work."
---
Between the launch of the new Codex and GPT-5.5 and now, something happened in my own house that has stayed with me more than any benchmark. My wife, who is not an engineer, built and shipped a working full-stack app. She is using GitHub for the first time. That is one anecdote, not a trend, and I am wary of overreading it. But it is the cleanest signal I have for what the April release actually did. The model can now carry the work, and the surface area of who can ship working software has widened far enough that the question of where human judgment lives inside a company stops being a developer question and starts being a leadership one.

I sat down with Tibo, who leads Codex at OpenAI, to ask what changes for companies now that the model can do the work. I’ve written about this a few times since GPT-5.5 and Codex dropped in late April: the bottleneck has moved twice. The first move was from “the model can’t do the work” to “the model can’t do the work the way our team would do the work” — the workflow-packaging problem, which I covered last week. The second move does not land in a workflow file at all. It lands in five different leadership chairs across the company, and each of those chairs has to develop a new instinct that almost nobody is teaching. Our conversation kept circling back to a single organizing point: the model is good now, and the question that matters has shifted to where you put the human judgment around it. What follows is my attempt to write down the takeaways from that conversation and push the framing further than we got to in the room.

I’ve been thinking about what happens to companies that skip this layer. Some will over-restrict to the point that the agents are useless and the team works around them. A smaller number will under-restrict and end up with an incident that turns into a board-level event. The companies that do the quiet work of building the five layers will look unremarkable for two quarters and then will be impossible to catch. Watching who joins that last group is going to be one of the more interesting things to track over the next year.

I’m going to walk through a practitioner template that’s already running this way, the five chairs, and the work each one has to do this quarter. Let’s go.

Late last year — a million years ago in AI timing, fairly recent in calendar time — Addy Osmani, Director of Engineering at Google Cloud AI, published his LLM coding workflow for 2026. It is a quietly important document, because a senior engineer who could write any line of code himself describes how he has restructured his entire workflow around the model now doing the writing. His one-line summary: “Specs, skills, MCPs, small iterative chunks, and always review what the AI suggests.”

What is worth studying is the practical detail underneath that summary. Osmani spends the first part of every task on a robust spec, before any code generation begins. He breaks the work into small iterative chunks rather than asking for monolithic outputs. He keeps standing custom instructions in the repo that capture team conventions. He runs automated quality gates — tests, linters, even AI-on-AI code review — to catch what skim-reading misses. And he is unambiguous about where accountability lives: “No matter how much AI I use, I remain the accountable engineer. In practical terms, that means I only merge or ship code after I’ve understood it.”

Notice where the human judgment goes. The model produces the code, but Osmani applies his own judgment in two specific places, and neither one is runtime line-by-line review. The first placement is at design time, in the spec and the standing instructions that shape what the model writes. The second is at the gate, in the automated checks that flag the parts actually worth his attention. Everything in between, the part that used to consume his week, is handled by the agent operating under instructions that have already absorbed his taste. As he frames the underlying principle: “Treat the LLM as a powerful pair programmer that requires clear direction, context and oversight rather than autonomous judgment.” Twelve years of accumulated taste no longer live only in his head. They live in the spec, the plan, and the standing instructions the agent reads before it runs.

Plugins, skills, and MCP are how you fix the first move: they package the workflow so the agent inherits the standard, and Osmani’s piece is the most legible practitioner-grade example I’ve seen of that move done well. Packaging the workflow does not fix the second move. The workflow file knows what to do. It does not know what your company should be careful about, who decides when something is wrong, what context persists when an employee leaves, or when a human gets pulled back in. Those are leadership questions, not workflow questions, and they live in five different chairs.

## The five chairs

The second move did not land in one place. It landed in five different roles, and each role needs a different new instinct. Most companies have not built any of them. Some have started one, but I have not seen a company yet that has begun all five.

The senior practitioner used to be the human catch in review. She now has to encode the catch upfront, before the agent runs. The engineering manager and platform lead used to permission users by role. They now have to permission actions, scoped per task and audited. The engineering lead and ops leader used to be the second pair of eyes on every meaningful change. They now have to design the second pair of eyes as a system rather than personally being it. The chief of staff and people leader used to manage documentation. They now have to manage context architecture, with portability and curation as first-class concerns. The operator and owner used to run on vigilance. They now have to run on triggers.

## The senior practitioner

The senior engineer on your team has spent twelve years developing taste. She knows when a refactor is over-engineered. She knows when a test is testing the wrong thing or when an interface looks elegant but will hurt you in six months. Most of that knowledge lives in her head. Some of it surfaces in her review comments, but almost none of it lives anywhere a system can read.

That worked when her presence in the workflow was the guarantee. The team’s quality bar was, in practice, the bar she would call out in review, and that was a perfectly serviceable model when there were a handful of pull requests a week. With agents in the workflow, it stops working. The agent will produce roughly ten times the output she can review, which means her judgment shifts from being a catch to being a bottleneck — and the team’s quality bar reverts to whatever the agent does by default, which is usually plausible-looking work that misses everything she would have flagged.

The old instinct was to develop your taste and then apply it through your presence in the review queue. The new instinct is what Osmani is teaching. Your taste is a spec, not a final-line catch, and your judgment has to live in artifacts the agent can read before the agent runs.

It’s tempting to think of this as a prompt-engineering problem. In practice, it is a documentation-of-taste problem, and most senior practitioners have never been asked to do it explicitly. Their taste is a sense, and asking them to write it down feels reductive in roughly the way that asking a chef to write down what they mean by “balanced” feels reductive. It is also the work.

Concretely: the senior reviewer who would catch a race condition in the payment path needs to write down what triggers her suspicion. The reviewer who hates implicit type conversions needs to encode that as a non-functional eval criterion. The reviewer who pushes back on tests that mock too much surface area needs to articulate the threshold. None of this is novel logic. All of it is judgment that previously only lived in her head, and the output is a living constitutional document the agent reads. Not a style guide written for new hires, but a living set of evals, AGENTS.md-style files, and standing instructions that encode what good and what bad look like in concrete terms for this team and this codebase. Done well, the senior practitioner’s review time concentrates on the small fraction the agent flags as borderline, instead of being uniformly distributed across every PR.

If your senior people are still spending most of their week catching things in review, you have not shipped their taste yet. The goal is for their judgment to compound through the agent rather than get re-applied PR by PR.

The leading edge of this is already visible inside OpenAI itself. Jos Visser, a member of technical staff there, wrote in February: “In the year so far, I have not written five lines of code, despite committing many thousands of lines, including entire features and complete rewrites of pieces of code; all done by Codex with minimal oversight.” His role has not disappeared. It has shifted. He spends his time on design docs, plan reviews, and corrective feedback when the agent gets confused. The taste is still his, the execution is the agent’s, and the accountability is exactly where it always was. Most senior practitioners are not yet operating at Visser’s extreme, and most do not need to. The instinct is the same at every point on the spectrum: write down what used to be a feeling, because the agent will read what you wrote.

## The engineering manager and platform lead

Your platform lead spent the last three years building a careful permissioning system for humans. Production access requires a ticket and a review. Read access to customer data needs a security training course. Database write access is gated by role. Then the team starts deploying agents, and the entire permissioning model breaks in a specific way: the agent inherits the permissions of whoever invoked it, which means the agent invoked by a senior engineer can do everything the senior engineer can do. That seems like a reasonable extension of the existing model at first glance. It turns out to be the wrong model.

Human permissioning is built around identity and role, with an implicit assumption that the human will apply judgment at runtime. They will not delete the production table by accident. They will not send the customer email with the staging coupon code. They will not run the migration without checking the rollback. The permission grants the access. The human’s judgment supplies the safety. Agents do not supply that. They do exactly what they were asked to do, often well, sometimes catastrophically.

Identity is the wrong axis. Blast radius is the right one. The old groupings (trusted versus untrusted, admin versus contributor, internal versus external) lived at the identity level. The new question lives at the action level: what is the worst thing this action could do, and is it reversible? Permission gets scoped per task.

Concretely, a reasonable agent permission catalog has tiers. Read-everything access at the bottom is fine because reads are reversible. Write access to staging unlocks per-project with logging. Write access to production payments has a hard sandbox, a second-agent check, and an explicit human approval. Deletion is its own category and almost always escalates regardless of the system. External sends get their own gate, whether the action is an email, an API call to a customer, or a post to a public channel.

The platform lead’s job becomes designing this catalog, which is closer to building a permissions matrix than maintaining an access control list. The matrix has actions on one axis and risk class on the other, and the answer to “can the agent do this” depends on the cell, not on who invoked it. Both major ecosystems expose primitives for this kind of work — OpenAI through Codex’s app and plugin action controls, Anthropic through Claude Code’s permissions system and MCP servers — but the pattern matters more than the surface. The shift is from identity-based access to action-based access.

If your agent can write to anything your most senior engineer can write to, you are permissioning agents like users. The right model is closer to how you would permission a script that runs in production: narrow, specific, audited, revocable. The new instinct is graduated scope per action, not blanket scope per identity.

## The engineering lead and ops leader

Your engineering lead used to be the human in the loop. Every PR landed in his queue. Every release plan ran through his judgment. Every postmortem named him as the second pair of eyes that should have caught it. The model worked because his attention was the bottleneck and the bottleneck was tolerable when there were six PRs a week.

Now there are sixty, and most of them were written by agents. He is still trying to be the second pair of eyes, and he is failing because attention does not scale and the volume now exceeds what he can cover by an order of magnitude. He has two failure modes available. The first is to slow down to the speed at which he can actually review, which kills the throughput the agents created and frustrates the team. The second is to keep up by skimming, which is the failure mode he picks when honest about it.

Tibo named the underlying principle in our conversation more cleanly than I’ve heard it framed anywhere else: “we’re optimizing for outcome per human attention.” Human attention is now the scarce resource, and agent attention is the abundant one. The whole stack — review, permissioning, memory, escalation — is downstream of getting that ratio right. (And yes, I have a proper write-up coming on this topic.)

Maja Trębacz, on OpenAI’s alignment team, named the version of this that lives inside the verification problem in her work on scaling code verification, and the line is direct enough to quote in full: “Human verification is becoming the bottleneck. So we need to make sure that we’re also training powerful models to help humans in verification, and that our verification abilities are scaling as fast as AI capabilities.” That is a sentence with implications most companies have not yet absorbed.

The maker-checker pattern at the human level has stopped working at the volumes agents now produce. The way out is not to find a third human review pattern. It is to recognize that the structurally correct version of maker-checker now lives at the agent level. The reviewer is no longer the engineering lead. The reviewer is an agent whose objective function he wrote, monitored by the team that wrote the function. The old instinct was to be the second pair of eyes. The new instinct is to design the second pair of eyes as a system.

This is the most underdiscussed shift in the entire stack, and OpenAI has shipped the production version of it. Inside OpenAI, every PR is automatically reviewed by a Codex-based reviewer trained for high-signal review. Not just diff inspection but repo-wide reasoning, hypothesis-driven testing, and intent matching against the stated PR description. The published numbers are striking. When the reviewer leaves a comment, the author addresses it with a code change 52.7 percent of the time, which is a remarkable signal-to-noise ratio for any review tool. The reviewer has “protected high-value experiments and caught launch-blocking issues” — work that would not have been visible in the diff alone. Trębacz and her colleagues frame the result as “defense in depth,” explicitly a support tool, not a replacement for careful judgment, with the warning that “teams could start treating a clean review as a guarantee of safety rather than as one layer of defense.” That warning is the part most companies will skip, and it is exactly the part that matters.

Anthropic exposes adjacent primitives in Claude Code through hooks, subagents, MCP, plugins, and permission controls. Hooks can block tool calls at lifecycle boundaries. Subagents can run with separate tools and context. The product surface differs from OpenAI’s, but both ecosystems expose versions of the same broad control problem: instructions, tool access, permissions, review, memory, and workflow packaging. The exact product surfaces differ, and the principle behind any of these primitives is the same: agent execution needs a control system, and the structurally correct version of that control system is another agent with different incentives.

What this looks like for the engineering lead in practice: define what the review agent should catch, then encode those as the review agent’s prompt and evals. The list usually includes drift from the original intent, scope expansion beyond what was asked, missing tests where the change touches a critical path, and irreversible operations without explicit approval. OpenAI’s customization layer for this is called AGENTS.md and lives in the repo. Claude Code uses similar mechanisms with different names. The principle is to write team-specific review standards into a file the review agent reads, rather than hold them in a senior engineer’s head.

Then spot-check the review agent itself, not the worker. Your judgment moves from runtime to design time. You build the checker once, it runs on every PR or every customer-support ticket or every research experiment depending on the workflow, and your attention concentrates on the small fraction the review agent flags. As Trębacz’s team emphasized, that residual attention is not optional. The review agent is a support tool, not a substitute for one.

A review agent adds inference cost and latency. The bet is that the added review layer is cheaper than spreading senior human attention uniformly across every generated change. OpenAI’s verification work argues that with reasonable budgets, verification can run cheaper than generation, which makes the economics favorable when you do it right.

If your “checker” is a human spot-checking on a screen, you have collapsed the maker-checker pattern. The structurally correct version is two agents, deliberately misaligned, with a human resolving the small fraction that requires real judgment. OpenAI is running this in production. Most companies have not started. The new instinct is to design the check rather than to be the check.

## The chief of staff and people leader

Your chief of staff has spent two years building an institutional memory. She knows which Slack channels matter and which are noise. She knows where the strategy decks live. She knows that the Q2 pricing deck has a data error everyone has been told about but nobody has fixed. She knows which decisions were never written down because they were made in a hallway, and she has tracked the consequences of those decisions ever since.

None of that knowledge is reaching the agents, and her knowledge is structurally invisible to the agent stack. The agent reads what it can index. It reads docs. It reads whatever’s in connected systems. It does not read her. When she leaves the company, the artifacts stay. Almost everything else goes with her.

This used to be a knowledge management problem, which is to say a documentation problem, and the accepted answer was to make the docs better, train the team to update Notion, reward the people who write things down. That answer was always partial, and now it is wrong, because the audience has changed. The audience is no longer humans browsing Notion. It is agents reading whatever you point them at, with whatever priority you assign, with whatever structure you give the corpus. The right question is no longer “are the docs current.” The right question is what context persists, who curates it, and what travels when a person leaves.

The old instinct treated knowledge management as documentation: make the artifacts better. The new instinct treats context architecture as workforce infrastructure, distinguishing three layers explicitly — personal, team, and company — and designing how each one persists, who owns it, and what happens at boundaries.

Personal memory is what an individual’s agent has learned about how that person works (preferences, patterns, taste), and it belongs to the person. When they leave, it goes with them, the way personal documents do. HR needs to draft this policy now, before the precedent gets set badly by accident. The first time an employee asks “can I take my agent memory with me when I leave,” the answer should not be improvised on a Tuesday. Tibo put it more directly than I’ve heard anyone at a platform put it: “Memories are not sensitive IP. Can I just take them with me?” When the person running Codex at OpenAI is sketching the right answer in real time, the org policy on the other side of the API call ought to keep up.

Team memory is what an agent has learned about a team’s working context. It belongs to the team as a whole, and it needs a curator, which is a role most companies have not named since the last time they had a librarian. Designate one explicitly. The curator’s job is to keep the team’s context corpus clean, current, and useful, the same way a good ops lead keeps a runbook clean. The curator role is not glamorous, and it is exactly the role that makes everything else compound.

Company memory is the deliberate corpus the agent reads from across the organization. It is the curated subset that an agent should treat as authoritative, distinct from the ambient mass of Slack and Notion and Drive content. The chief of staff’s accumulated knowledge belongs here, deliberately written into the corpus rather than left to be inferred from chat logs.

Tibo was honest about this in our conversation: the question of how personal, team, and company memory should interact is still an open research problem. He’s right at the platform level. At the org level it is also a problem that has to be solved now, not later, because the failure mode is silent. Bad team memory does not crash. It produces mediocre output across thousands of agent runs, and you don’t notice until you compare yourself to a competitor that built the layer well.

A related point Tibo made matters here too. The failure mode he sees most often inside companies deploying Codex is not under-adoption. It is “almost dogmatic, top-down” rollout, where leadership picks the approved use cases and pushes them across the org. What actually works is letting different pockets of the company discover what fits their work, then building forums where the good recipes propagate quickly. That is a curator’s job, not an executive’s. The leadership move is to designate the curator and protect the forum, not to author the recipe book.

If you can name a librarian on your team, you are ahead of most companies. If you cannot, you have a gap that will widen quietly for the next eighteen months. The new instinct is to treat context as infrastructure, not as documentation.

## The operator and owner

Your COO walked through the office last quarter and watched an agent send a customer-facing email that almost shipped without anyone reading it. She caught it because she happened to be looking. She has been looking less since then, and thinking about it less, because every time she asks “should this have a human checking it,” the honest answer is “probably, maybe, depends.” She has ambient anxiety dressed as a process, and ambient anxiety does not scale.

This pattern shows up in every operator I talk to. The early phase of agent deployment runs on the operator’s nervous system. They feel something is off, they look, they catch the bad thing, they intervene, they relax a little, they go back to running the company. After a few months of this, two things happen. They get tired, and the catches start slipping, because the volume of agent activity has by then exceeded what nervous-system vigilance can cover.

The way out is the explicit replacement of vigilance with documented triggers that the system enforces. Triggers do the work the gut used to. Write them down, set thresholds the system enforces, audit them quarterly.

The triggers themselves are not new. A good ops team has always had escalation paths in runbooks. What is new is that most companies have not yet written them down for agents. Four categories cover most of what matters.

Cost triggers come first. Any agent action above a dollar threshold escalates, and the threshold is not the same for every workflow. A research agent burning a hundred dollars on a single deep research run is fine. A customer-support agent issuing a hundred-dollar refund without review is not.

Irreversibility is the second category, and it is the most underrated. Any deletion, any external send, any production change escalates, because reversible actions can be undone if the agent gets it wrong and irreversible actions cannot. The cost of the trigger is low. The cost of skipping it is occasionally enormous.

Confidence is the third. When the agent itself flags low confidence in its own output, escalate. Most agents have some form of self-rated confidence. Most operators ignore it, and the habit of ignoring it is a holdover from the era when models hallucinated constantly. That era is mostly over for frontier models, and when a frontier agent flags itself as uncertain, that signal carries real weight now.

The fourth is drift, which is what review-agent patterns are good at catching: the agent that was asked to refactor and decided to also rewrite the auth layer while it was in there. Drift is where reasonable-looking work shipped against a plan nobody approved. Catch it at the review-agent layer described above, not at the operator’s desk — it is the failure mode review agents are built for.

Each trigger maps to a specific risk class. The point is to write them down, give them numerical thresholds where you can, and stop relying on the operator’s nervous system to be the safety net. The other point is to audit them. Triggers set six months ago for a different model are probably wrong now, and quarterly review of the triggers themselves is part of the discipline, the same way runbook review is part of the SRE discipline.

If you cannot articulate the conditions under which a human gets pulled in, you don’t have escalation. You have ambient anxiety. Every operator I know has experienced that this year. The answer is to write the triggers down, test them against real cases, and update them when they fail. The conditions of intervention have to live somewhere outside the operator’s head.

## What happens when you build all five

Step back. The senior practitioner has shipped her taste. The platform lead has scoped permissions by action. The engineering lead has designed the review-agent pattern. The chief of staff has built context architecture with named curators. The operator runs on documented triggers, audited quarterly.

The company that has done all five looks like a company where humans concentrate on the small set of decisions that actually require human judgment, and agents execute the rest. It looks like a company that compounds. The taste shipped once gets applied a thousand times. The permission catalog gets refined as new failure modes appear. The review-agent objective function gets sharpened with every miss. The team’s context corpus gets cleaner with each curator pass. The triggers tighten or loosen based on real outcomes.

The company that has built none of these has two ways to fail, and neither one is dramatic at first. The dominant failure mode is quiet over-restriction: agents get permissioned so narrowly that the team treats them as toys, the rollout stalls, leadership concludes “agents don’t work for us,” and the company writes off the technology while a competitor compounds. The louder failure mode is the one that gets the postmortem — the under-restricted agent that deleted the production table or sent the wrong customer email at scale, and now legal is involved. Most companies will land in the quiet version. A smaller number will land in the loud one. Both versions hand the long-run advantage to the companies that built the layer.

The mistake the companion piece could leave for this one is the implicit suggestion that workflow packaging is sufficient. Workflow packaging is necessary and not sufficient. You can package the perfect plugin and ship it across your team and still hit every failure mode in this piece, because the plugin does not tell the platform lead how to permission, does not tell the chief of staff how to architect context, and does not tell the operator when to escalate. Those are five different jobs, each one needs a different instinct, and the plugin layer assumes those instincts already exist.

This is also why the question “Codex or Claude Code” is the wrong question to spend most of your strategic thinking on. Both ecosystems expose versions of the same broad control problem: instructions, tool access, permissions, review, memory, and workflow packaging. The exact product surfaces differ, and the platform you pick matters for integration, security review, and team habits. But it does not remove the need to build the five leadership instincts described here, and those instincts determine whether your company benefits from the platform at all.

## The work to do this quarter

If you are a senior practitioner, start writing down what triggers your suspicion in review. Not every rule, just the ones you know you would catch. Those become your eval seed. Osmani’s piece is the cleanest public template I know.

If you are an engineering manager or platform lead, draft the action-by-risk-class permission matrix for one workflow. Not all of them, just one. The exercise will surface the questions you have not asked yet.

If you are an engineering lead or ops leader, design the review-agent prompt for one high-stakes pipeline. Run it as a shadow check on real PRs for two weeks. See what it catches that you don’t. The OpenAI alignment post on scaling code verification is the best public worked example of this pattern in production.

If you are a chief of staff or people leader, name a librarian for one team and draft a one-page memory portability policy for HR to review. Not the final version. The draft that forces the conversation.

If you are an operator, write down four escalation triggers for one workflow — cost, irreversibility, confidence, drift — with numerical thresholds where you can and vibes-based thresholds where you must, with a note to revise.

Each of these is a week of work, not a quarter. The compounding takes longer.

Most companies will deploy agents and skip all five. They will conclude that agents don’t work for them, or they will hit an incident that gets attributed to the agent when the actual cause was the missing layer. The companies that build the layer will look unremarkable for two quarters and then will be impossible to catch.

In my own workflow, Codex now does a large share of the execution. Whether a company benefits from that kind of agentic work depends on whether the people in those five chairs have started. Most haven’t, which is the opportunity worth taking.

![](https://substackcdn.com/image/fetch/$s_!6t_T!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b9d57a2-dc48-4532-90e0-385284a0b901_1024x1024.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/codex-five-leadership-chairs-tibo-interview) on 2026-05-21T15:26:17-04:00*

YOUTUBE TRANSCRIPT
Hello!

What you're about to watch is an exclusive interview I did with Tebow, who runs Codex at OpenAI. This conversation is what sparked the entire idea for the article below. I had so much fun. He sat down with me to talk through something I've been kind of wrestling with for months. What changes when the

I feel like that happened with Codex and Chat GPT 5.5 and I'm so appreciative that I got a chance to sit down and talk with Tebow and Conversation is like the agents have to grow up and we have to grow up in how we

use them and just saying you use agents is not really going to get you anywhere.

Use agents responsibly.

Use agents responsibly. Use them for what they're good for. Do you have a pet definition of agent that you give to people who are non-technical that helps them understand the difference? Because I know a lot of people who are like, I am using ChatGPT on my phone level. Yes. And that's where they're at.

And those people hear the word agent and they're like, like my mom, what's an agent?

Yeah, my simple definition is, you know, it can answer questions, an agent can do things for you. It has hands and legs, right? It can do things. Yes, it can act, it can do things when you're behind. And so, you know, it is much closer to a human in that regard, where, you know,

I could ask you to send an email on my behalf that, like, an agent, a powerful agent should be able to do that.

And by that definition, Codex meets that bar.

Oh, Codex is definitely an agent. It is on all our evaluations and personal usage and what we're seeing from people, it is the strongest generally available agent out there. Yeah, yeah.

And actually, that reminds me, to what extent are you seeing in usage patterns that users are starting to move away from just using codecs for coding? And all of this knowledge work you're seeing inside the company, you're seeing it show up in general user patterns as more and more codecs features start to shift.

Yeah, so we tried growth. Growth has been phenomenal recently. We hit 4 million users recently. Right, I saw that. Well, you know, the growth has been accelerating since then. So, like, you know, we're on top to hit 5 million soon. But one of the things that's been remarkable there as well is the fraction of users

who is doing, you know, general purpose work and not coding is growing faster.

Faster than the overall growth curve.

Yes, faster than coders are adopting products.

Interesting. And so,

for example, last week compared to this week, we saw for non-coding 40% week over week growth. Wow. This is going to take over Codex. Yeah, at that pace it will.

So I think maybe the first thing I want to do is just... Nate’s

We've always had conviction, but the thing that I like here is, the first one is, it's good to see you again. And it's great to see you.

The shift from last time, where it was like some curiosity, right?

Engaging into what felt like my job. Nate’s Nate’s the vibe shift externally with people, you know, coming out and speaking about Codex is like something that they truly, you know, love and feel that, you know, it is doing things in a way where, you know, they've not seen it done like, you know, like this before or,

you know, they just sort of like really love it just for the product itself. That's been so validating, right? That's just been like, okay, this is like what we've been trying to build all this time. Like, you know, maybe we're a little bit slower at it. You know, we were taking our time with the engineering.

We're taking our time at the craft. Yeah. But then seeing that come through is, you know, it just makes me smile. Of course. One of the things that we're really trying to instill and belief is that it should just work. It should just work. You should open it. It should present itself in a calm way.

You're holding into your hands a very deeply Nate’s Instantly capable new powerful technology but it should present itself in a simple way and grow with you along the way. As you learn different ways to engage with the GPT models you get a little bit more out of it every day.

You share maybe some tips and tricks with friends or you learn about them on the internet. But it shouldn't be overwhelming. You shouldn't have to configure 50 different things in order to just get to use it initially. And then it's all about progressively showing you, hey, maybe you can connect Stripe.

Hey, maybe you can connect your Google events. Maybe if you use Slack, you should do that. And internally, we use Slack for everything at OpenAI. And the number of use cases that we've been able to get from connecting Notion, Slack, the whole Google Suite, it just unlocks a whole different set of productivity things, way beyond coding.

Tell me a little bit about, you mentioned at the top, sort of this idea that everyone uses Codex, not just the technical team. And I know I've seen that in other places, sort of in the news on Axe, people talking about it. What does it look like internally when you hit that tipping point and like the

non-coders start to use Codex?

Initially, it was a gradual thing. It was definitely very engineering-driven, and then it was engineering-adjacent. Product managers, designers, or technical product managers, helping with standards. Nate’s the computer, for example, suddenly you're like, hey, I'm actually faster with managing the entire GPU fleet if Codex is there helping me out. And then it sort of inspires people.

One of the initial really inspiring examples was when we were working with folks on the comms team and we were showing them and initially it was like, oh, Codex is for programmers. It's like, no, since we have the app and now with Nate’s It's like having this little assistant on your computer. And so these started to propagate.

And then, you know, certainly it seemed like, you know, sort of overnight, you know, I was like, suddenly we wake up and, you know, everyone's just using Codex at the company, including in the latest, Sarah Friars talks about this quite often, how it was tremendously helpful, you know, in the latest fundraise, you know,

in keeping track of everything.

Yeah, I did see that. I did see that, which is obviously a very non-technical use for Codex.

It's like a largest five-inch fundraiser in the history. Codex is instrumental in that. The amount of use cases, now it's a question of how creative are you? Because it's not capable of everything, but almost everything.

Yeah, it has a very wide general purpose surface area. How do you think about, like, one of the things I've noticed is that, like, when I open ChadGPT on the Mac now, it feels dusty compared to Codex. Like, Codex feels like you can get, like, the Chrome is on that app, right? It's, like, polished up and, like,

are you guys thinking that you see two separate visions for that long term or just, I don't know, talk to me.

We're currently pouring a ton of innovation into FedEx. There's a lot of good energy there. ChadGBT is the world's most successful wide application of AI. It's giving access to Nate’s a lot of what gives Codex that feel like, hey, I can do new things. It feels quite polished.

It's a new way to engage and not use your computer. We're going to bring that to Chad.

That would have been my guess. But I love that Codex gets it first. It feels like the power tool, right? At least right now it does.

Yes, and for everyone who discovers it, there's something there. Now we're making explicit as well. You don't have to be a programmer to use Codex. You're going to feel like you have something very powerful in your hands. That was originally meant for engineers, but now it's for you too.

And if you feel like it's a little bit too daunting, worry not. It's going to come to China.

Yeah, that makes sense. And I guess that brings up an interesting piece that I've seen from folks I talk with where they're starting to see bottlenecks emerge at team productivity level versus individual. Like I have like a CTO that wrote to me Nate’s And it felt like part of the answer was connectors and integrations because I think

his context layer, I think it might have been Notion. But do you see that more broadly as like a connectors integrations shaped problem or is it something where you're thinking about team productivity for codecs itself in a certain way? I'd be curious.

There is sort of like an evolution there where initially coding agents had access to nothing but the file system.

Yes.

And then gradually we're bringing more and more of the tools that have been built for humans, making them accessible to the same agent.

Yeah.

And, you know, connecting them through what we refer to as plugins, but like under the hood, there is a connector. you know which is like responsible for you know basically the API between that system and the agent and also like the authentication piece you can wrap that in a

plugin and you know make it a little bit more user friendly and also plugins are able to have skills and so you tie it all together into a concept that the agent can leverage And I wouldn't be surprised there if we see innovation when it comes to project management and Nate’sletter Nate’sletter Nate’s

That's such a big shift too. And it's funny, like I talk with companies that are shifting how they work. And when you peel the onion back, it's like 10% getting the tool. And it's like 90% the soft skills needed to recognize that you have to reorient your entire building workflow and skillset to facilitate an agentic development pipeline.

And that just seems to be a massive shift that people are still sort of working through what that means.

Yeah, the more you can get and make things accessible to the agent, you're going to have a better time if you do that. And then the more you can have guardrails and mechanisms to help you assess whether an outcome is correct or not.

Quickly.

Quickly. And then give the same access to the agent too so that the agent can validate itself. That's right. But its work is good. Then that reduces the amount of attention that you need So one of the things that we're really, it's like a deep belief that we have is like we're optimizing for, you know,

outcome per human attention Yes,

and human attention will be scarce relative to agent attention Agents will continue

to improve in their capabilities quite exponentially So therefore, you know, we have to invent a system such that, you know, it requires like very little human attention for everything

Tell me about the computers, because I know we wanted to get into that, and I just, it's so elegant. It's so far from where we were a year ago when it was so janky, and I remember computers, we were staring at this, and I knew it would get better,

but I was staring at this little mouse moving around, and I was like, God, this feels so slow. I know it's going to get better. I believe in the scaling law, but boy, is it not there now. and here it is like here we are in 2026 it's so much smoother it's a combination of

three things your great craft yeah you know the models being better and then you know it's like deep deep understanding of like macOS and Apple system the way it works under the hood it's highly non-trivial it required you know very deep technical work a lot of the work is done by

You know, the amazing team that joined us. From Sky?

From Sky, yes. They've poured so much effort and craft into this. And then the models were finally right for these kinds of use cases. And so that's why we decided to put it out there. It is so loved inside of the company and it's been one of the most successful features that we released.

It's been amazing. It felt like magic opened up for me. I was like, I knew this could happen. I knew it was coming somewhere. Finally, it's here. So the fact that you were in the background, it's been such an unlock. And it unlocks new primitives. So one of the things, I don't know if you paid attention, but...

Clicky came out like this week or last week out of whatever it was, Alpha. And it's basically a very consumer-friendly agent experience where you can just instantiate with your voice. It's a little blue cursor that follows you around. But under the hood, they're spinning up Codex child agents and computer use to do it.

And so you're essentially sort of building a primitive that other companies are starting to build on.

Yes, and a lot of the early days still for events and we're going to see many, many more such innovations and so inspiring other approaches out there is a big part of why I love my job as well and a big part of why we're also open source. Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s

Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor

Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s

Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate’s Instructor Nate�

Nate’ Like one of the things I've been curious about like I know that you guys are like we talked about that as a primitive and sort of putting that out how intentional are you guys being and when you like start to put something together

and it's working inside the company you put it out there do you think of it sort of as this is a new kind of Lego block and I'm putting this out it's a new primitive I think people will do cool stuff with it and it complements the other bricks we have

in the stack what's that conversation like for you are you very intentional sort of adding adding in as you go

We have a few very fundamental pieces that we know Yeah. They really stem from wanting to build, you know, the world's, like, most capable agent. So, you know, you need to give it access to a lot of, you know, different primitives. You know, maybe, you know, you can, you know, just have, like, even if you have, like,

you know, the best MCP implementation in the world, you're not going to have an MCP, you know, server or implementation for everything. No. And so, you know, it's very clear that, you know, you need good computer use. It's clear as well that a lot of your life is done in the browser.

You're logged in, you have access to everything. Your agent should be able to use the browser in a way that's delightful and that's secure. Browser use, pushing that capability to the max is very important to us right now. Going from there, it's using the strengths of OpenAI when it comes to multimodality and enabling to

communicate and exchange information with your agent in non-textual ways. That feels like the future, very important to us too. And in a way, this year is just really where I think a lot of the bets that OpenAI had been making, which felt maybe at times a little bit unfocused,

just really come together where you realize actually we are assembling Nate’s an extremely capable entity and allowing you to interact with it in ways that will surprise you in how delightful they are compared to just you having to prompt it.

Okay, this is going to flip into sort of team level stuff. Do you have any tips or tricks that you would want to give folks who are looking at building agentic build pipelines? And the top, I'll give you the top objections and questions I get, like real honestly off the top from people who talk to me.

One is, it's really hard to do this with brownfield applications and brownfield code bases. Two, it's really painful to do this with persistent memory and handling the memory and context layers really hard. And then three, And you touched on this earlier. I'm sure you can touch on it again. But basically,

once you get people through the soft skill of I now have to write clear intent and clear evals, well, now you have to get people to actually figure out what good looks like at the end and judge good quickly and appropriately.

And so if you have any tips or tricks for folks, like I think I would be remiss if I just ask.

No, these are three excellent points. So, like, brownfield code bases are more challenging. Yeah. But with the current level of GPT-55, it's like, you can do refactors fairly quickly as well. And so, it's never too late to start, you know, and introduce this technology.

Like, I would be lying if I were to say that, you know, OpenAI's code base is pristine. You know, like, in a way, it's like, what? Like, it's not pristine.

We existed for a decade. You know, we're also reinventing things. Yeah.

We're seeing this with the customers that we work with directly. We've been rolling out codecs within NVIDIA and NVIDIA has sprawling immense complexity. And so you're being thoughtful there, but it is not the case that you don't get Nate’s Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter

Yes, it will be.

And you kind of want to allow people to discover what works for your company in different pockets of the company. And then what you want to do is you want to create the right forum so that the right recipes expand very quickly and get exchanged very quickly.

I love that recipes image. It's like a cook-off and you're like, this recipe works really well.

Yeah, and it's going to be a little bit different for every company. So you want to create that forum. Context management, the current approach that we're still taking is you want to Yeah, we do a ton of that Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter

Nate’s a thoughtful integration with StatStick and so we're able to do feature robots fully autonomously.

Oh, you do like Canary in the coal mine and then you tune the dial and all of that.

Yeah, and we have specific guardrails to prevent mistakes from happening.

I actually knew the StatStick guys before you guys grabbed them and I was like, oh, this is wonderful.

It's a good combination for everybody. You'll all be very happy together. Yeah, and so then we're able to ask questions such as like, hey, what is the current rollout of this feature? And then correlate that to data catalogs, for example. And we have canonical plugins for that inside the company. So I recommend investing time in standardizing.

There are a ton of plugins out there as well that people are creating. But context management will continue to, I think, evolve over the coming months. Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter That's right. And so we're doing three things there. We're increasing the context length and we're being more efficient with the context as well.

And the compression and the way you handle it.

Yeah. And compressing the representations. And so that's a benefit to your time. It's a benefit to, like, we're using less tokens and so it's costing less. It's good efficiencies. And this is how we've been doing a lot of you know improving on like the speed as well like you know i remember like last

time we talked you know codex was like you know synonymous with like you know being

slow well and i turned on whatever you call it super fast lightning mode like i feel like the wind is pushing back my hair when i get it's just like this is a slow

this is the slowest it will ever be you know we have breakthroughs coming up uh which will make it significant faster so amazing very excited for that Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’s You know, why this is the ownership of this particular, this is the responsibility and ownership of this particular piece and that you understand it,

you know, as a human, you know, what should and shouldn't be changed in this particular area of the code so that, you know, you can pattern out very quickly. You know, if your agent comes back with a change in the signal, suddenly it's like you're doing rate limiting somewhere in your odd stat.

That's obviously not going to be correct. And then having good tests, end-to-end tests help, giving very clear instructions for what good looks like to the agent itself, like an LA55. It can mostly figure it out for itself if it has the information like what you're actually trying to do.

That's oftentimes seeing failures where people are not prescriptive enough on what a good outcome looks like.

Yes, I think that's true. And one of the things that I noticed when I see people writing evals for eval-driven development, the first blush people take, like 80-90% That's right. That's right. And don't do it.

That's right. And now if you do that, models are like extremely good at just making sure that, you know, they actually do fruitfully adhere to your description of what good looks like. And then also recommend like just enabling memory because your preferences are remembered over time. And, you know, you're just going to have a better,

the model is going to be like a 5.5 is going to have a better feel. for what your personal preferences are so that you don't just have to keep repeating them on your phone.

Is there a thought around how personal memory and team-level memory interact long-term?

Still very much an open research question.

Okay.

This is something that we want to solve for. Right now it's personal memory. Right. It is obvious that certain things are not personal preferences, but like team preferences or preferences, company preferences, you know, like country preferences. And so there should be like some sort of like hierarchy tool of it. Yeah. Still unsold.

Yeah, and this also gets at one of the things that I'm hearing from folks who are switching jobs right now is that they feel it's like missing limb syndrome. They're like, I was used to working with this AI instance, with this memory enabled, and I was this productive with it, and now I switch.

It may even be the same AI tool, but it doesn't have my memory. Nate’s

Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Yeah, and so in a sense, you know, the reverse might be true as well, where, you know,

you have your own personal AI, which has learned,

you know, a lot about your preferences and how you work, and you kind of want to bring that, you know, during your day-to-day work.

B-Y-A-I, right?

It's like, why would an employer, like, you know, refuse? So if you're actually more productive... They have every incentive. ...incentive thing to do. Yeah.

No, and I think that we don't have, like, we don't have, speaking of primitives, we have no primitives for that in the ecosystem right now. It's a really interesting question.

Yeah, I expect a lot of developments there quite soon. We're investing a lot in these kinds of primitives. This is where our memory implementation comes from. This is where Chronicle comes from. And it does feel like there is an element there of you should be able to have more control. You should be able to share it.

You should be able to shape it.

Yeah, that makes a ton of sense. Nate’s Nate’s

That's right. We're investing in Windows. You know, we were the first to, like, the sandbox item with us. We take, like, a thoughtful, you know, measure the approach to things. So computer use will arrive on Windows at some point. To when it's ready. Yeah.

It will hopefully be as delightful and surprising to people as it was on Mac. Mm-hmm. That's the bar that we're aiming for. In terms of how we view things, there is a spectrum of efficiency and safety, where if you have tight interfaces and very bespoke implementation,

You know you're able to probably be more efficient and also you're able to understand exactly what the semantics of the operations are such that you know like this is a read operation this is a write operation you know read operations are fine write operations are not and you can disable that and so you can give like

read only access to your agent With browser use or computer use, this gets more tricky because it's so powerful. And so it is also possible then that your agent might make some mistakes. If you ask it to move a calendar invite, it might accidentally delete it.

I've literally had that happen, but not with you guys. It's been a different agent that I had that happen with, and it was not fun.

And so we invest a lot in the precision, the alignment and the safety components of the agent itself. FireFive is tremendously good at that. The second thing that we have released as well is AutoReview, which we will write a lot more about, but it's a pretty sophisticated system, which

It allows us to run a second agent which reviews the actions of the project.

I thought it came out, but it didn't get talked about a lot.

This is our answer to running things outside of the sandbox. So we're going to start recommending people to just really... Every time I've talked about running outside of the sandbox, I've always told people, like, be very careful. You're running without any guardrails. It is very powerful. Nate’s

to what is safe, what is secure, and what was your initial intent as a user. So if your intent is like, hey, move my calendar invite, and suddenly your primary agent is, Codex is trying to take an action where it's deleting an invite on your calendar.

That's not aligned to the original.

All of you will catch that. This is not aligned with the intent and will stop the action from happening before it happens.

And so from an incentive's perspective, essentially review agent's incentive is correctness and adherence to security protocols.

Minimizing the risk. And minimizing risk. Yeah. And so it's going to sometimes catch things that are like could get the job done and is going to recommend to the main agent to take a different approach that is

less risky. Essentially it minimizes reward hacking.

It is true that the first agent is optimized to get the job done as efficient as possible, which you want with almost any means at times. And then the second one is there to protect you and your interests.

Yeah, yeah.

It is an approach where you do, you know, defense and debts, right? And this is like, you know, safety and debts. Like we train our, you know, 5.5 is like remarkable, you know, unlike all benchmarks when it comes to, you know, safety and alignment. But it is not foolproof. And therefore, you know, you want additional safety. Yes.

And this is always going to be a thing. You know, you might have the safest card in the world. We're still going to want to wear a seatbelt. You want to invest in the airbag.

Yeah. That's right. Yeah.

Exactly. And so, you know, if you combine all these things, suddenly you find yourself, you know, benefiting from a very powerful agent that, you know, also, you know, feels very robust, is secure, you know, is safe. And that is what we want. Like as we are increasing the capabilities, you know,

we want to invest in all of these other things that, you know, are going to ensure that this is like actually a robust tool for humans.

Yeah, like net-net, it sounds like the vision is like we want to raise the ceiling on like what you can build with these primitives, but we want to make sure the floor is secure and you're not going to get sinkholes and like other disasters on the downside as you get these capabilities.

Yes, that makes a lot of sense. Because I will tell you, like I see across my feed every day, I'm sure you see it too, the stories of people who have their agents set up poorly and then get these like my database was deleted moments and

I look at it as an invitation to basically do some production architecture analysis and say well how did we get to this point in the first place and how do we set this up incorrectly and what can we learn

Yes, and I think it's important to, you know, get excited about new technology. Yes. So what I would love to see more of is, you know, just open public discourse on, like, you know, some of the risks as well and, like, you know, how to mitigate that. And, you know, this is why, again, you know,

I've been always, like, warning people, like, do not just run outside of the sandbox unless you know what you're doing. Yeah. Spend time thinking about the tools, thinking about the permissions, and You should be supervising your agent. If you're giving it a risky task, such as messing around with your production database, do not leave it unattended.

Yeah. It's like I don't leave my eight-year-old to cook unattended.

But now with systems like auto-review, maybe you could. And it's actually going to catch a majority of issues.

Yeah. No, that makes a lot of sense. And I think that one of the big themes that I've seen in 2026 is this idea that, you know, we started the year and it was like, it was the year of agents and this and that, right?

And then it's like, it feels like we're getting toward the halfway point of the year. And the conversation is like, the agents have to grow up and we have to grow up in how we use them.

And just saying you use agents is not really going to get you anywhere.

I'm curious, you talked about being proud of the craft that's come through in this conversation. If you look ahead to December, end of year, is there something where you would say, this is the world I want to create with this tool by the end of the year that would make me personally really proud?

A lot of what we're trying to do with Credex is create new opportunities to solve problems that have never been solved before. And this is also true across science, for example, mathematics. Mathematics, Physics, and just really hard science. Internally, we're using codecs to help solve tough problems on the inference nod and just making it more reliable and

Nate’sletter Nate’sletter unambiguously valuable things for humanity and seeing codecs used for that. And two, keeping broad access to the technology and not making this something that only

small elites can use. Yeah. And that's something that I've seen you guys emphasize in the last week or two. And it's, I think it's been somewhat encouraging because there's a lot of fear going around and sort of folks I talked to that like the, that floor that we talked about is rising. And like,

if you're not going to be willing to spend tens of thousands of dollars a month, you're never going to get the best models. And it sounds like you guys are trying to push that floor back down and say, no, no, no, no. This is something that everybody should be able to get ahold of.

Broad access to just acknowledge it is like one of the primary reasons I joined opening. Yeah. Yeah.

Yeah, that makes sense.

And what's interesting about your answer is, and I love this as a product person, your answer is not, this is what I built. Your answer is, this is the outcome that I want to see unlocked in the market because the product is there.

That's the whole purpose of this technology.

And then sort of on the other side of the interview, I think the thing I would say is basically, do you have... Like, I have... Builders in my audience, I have folks who are, I guess, prosumers, passionate generalists about AI, and I have folks who are leaders. It's a broad audience,

but they come from across that whole spectrum and they're united by their passion for AI. If you're speaking to them, and this is our second conversation now, what is a last words where you're like, guys, this is what I would love you to take away and think about and chew on for the next month or two?

What I would like people to take away is that this isn't just about making yourself a little bit more productive. What you have to consider is that this technology will profoundly affect and transform your day-to-day in a way where you will be able to do things that you thought were never possible before.

And that is the way that you should engage and try to engage with this technology. Just really think deeply and creatively and question your own understanding of what is possible.

And I would add, do it without fear, because I hear a lot of fear from people around that change.

Yes, do it without fear. It's remarkably empowering. If you haven't done it already, just install the Codex app and try and use it. Point it at your desktop to organize your life's files, for example. I did that, actually. It works for you. You just do it. Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter Nate’sletter I love it.

[![Nate’s Substack](https://substackcdn.com/image/fetch/$s_!TAjW!,w_96,h_96,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8b4663-3eb8-42e2-a41a-1efd45e5ab98_1400x1400.png)](https://natesnewsletter.substack.com/)