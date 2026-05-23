---
title: "How to Build a Full AI Dev Team in Claude Code | Guide from Google PM Gabor Meyer"
source: "https://www.news.aakashg.com/p/claude-code-dev-team"
author:
  - "[[Aakash Gupta]]"
published: 2026-04-30
created: 2026-05-23
description: "How a Google PM runs 21 specialized Claude Code agents to go from idea to App Store in 72 minutes. The complete workflow with Confluence, JIRA, and Figma."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery]
ai-context: "Aakash Gupta podcast with Google PM Gabor Meyer on assembling a full AI dev team inside Claude Code — agent roles, n8n orchestration, and the builder-PM workflow."
---
What a Google PM’s 21-agent workflow actually looks like - from Confluence spec to App Store in 135 mins

![](https://www.youtube.com/watch?v=kQelqKkI-EQ)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/how-to-become-a-builder-pm-with-n8n-claude-code/id1763555775?i=1000762483697), [Spotify](https://open.spotify.com/episode/5ZNRFSYL15vRo7Rt51ANXP?si=glhi9q4SS7igfxzCWWA0bw), and [YouTube](https://youtu.be/kQelqKkI-EQ).*

**Brought to you by:**

1. [Maven](https://bit.ly/4bPulv7) - Get a $675 discount off Gabor’s course with my code
2. [Amplitude](https://amplitude.com/session-replay?utm_campaign=session-replay-launch-2025&utm_source=linkedin&utm_medium=organic-social&utm_content=productgrowthpodcast) - The market-leader in product analytics
3. [Testkube](http://testkube.io/) - The leading test orchestration platform
4. [Land PM Job](https://www.landpmjob.com/) - My 12-week AI PM + Job Search Course starts Monday!
5. [Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7) - Get $550 off their #1 AI PM Certification with code AAKASH550C7

---

## Today’s episode

Here’s the problem with most Claude Cost demos: they stop at the prototype.

Nobody shows what happens next. You try to add a second feature. The first one breaks. The styling reverts to default. The code is so tangled that you spend more time debugging than you saved by generating.

[Gabor Mayer](https://linktr.ee/gabor.productmanager) showed me what happens when you stop treating Claude Code like a magic prompt box and start treating it like a team.

He is a PM at Google. He has not written production code in 15 years. But over the past several months, he has been building real mobile apps using 21 specialized Claude Code agents. Not prototypes that live in a demo. Apps that are on the App Store.

*In today’s episode, he walked through the entire workflow live and share [all the resources](https://github.com/gabormayer/pm) free.*

---

***If you want access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, DeepSky, Relay.app, Magic Patterns, Speechify, and Mobbin - **grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*

***Do you want to become an AI PM? I’ve created a course for you. [Starts next week](https://www.landpmjob.com/).***

---

## Newsletter deep dive

*Thank you for having me in your inbox. Here is the complete guide to building a full AI development team in Claude Code:*

1. Why one-prompt vibe coding fails
2. The 21-agent team architecture
3. The spec-first workflow
4. From design to code without touching either
5. What changes when PMs actually build

---

*Save this. The full 10-step playbook on one page. Everything below is the why and how behind each step.*

![](https://substackcdn.com/image/fetch/$s_!ZvbK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F899be65a-c976-4ff6-ac59-75f257fe73da_2400x3027.png)

---

## 1\. Why one-prompt vibe coding fails

Every PM I know has built something with [Bolt](https://www.news.aakashg.com/p/pm-guide-bolt), Lovable, or [Replit](https://www.news.aakashg.com/p/guide-replit). The prototype looks great. It runs. It impresses people in a Slack message.

Then you try to ship it to real users. And you hit a wall.

#### Blocker 1 - Context compression silently destroys your spec

This is the failure mode that nobody talks about in tutorials. When you give one agent one massive prompt, the model compresses context. Details get dropped. Not randomly. Strategically. The model decides what is “important” and what is not.

In the episode, Gabor defined a complete color palette. Oranges, neutrals, specific accent tones. The agent received everything. The output used none of it. The layout was there. The structure was solid. But every color was a default.

The reason is straightforward. When the context window is full, visual styling details are lower priority than functional logic. So the model drops them. Silently. Without warning. Without an error message. You just get generic output and wonder what went wrong.

The fix is not better prompts. It is [context engineering](https://www.news.aakashg.com/p/context-engineering). Smaller, scoped tasks. Each agent gets only the context it needs for its specific job. The designer agent gets the brand guideline. The CTO agent gets the architecture spec. Neither gets the full 50-page document.

#### Blocker 2 - AI-generated code compiles but is not maintainable

A Reddit comment that hit home for Gabor -

> *“Vibe coding is just the rebranding of unmaintainable, low-quality source code.”*

This is the real prototype-to-production gap. The code works today. You can demo it. You can push it to TestFlight. But the moment you touch it to add a feature, three other features break. No naming conventions. Circular references between modules. Zero comments explaining why anything was built the way it was.

The fix is a dedicated code quality agent. Gabor calls his the Spaghetti Agent. It runs after every sprint and checks naming conventions, circular references, comment coverage, and structural debt. When he ran it on his codebase for the first time, it caught issues he never would have found manually.

If you are building anything beyond a one-off demo, this agent is not optional. I covered similar quality patterns in my [AI testing](https://www.news.aakashg.com/p/ai-testing) guide and my [AI evals](https://www.news.aakashg.com/p/ai-evals-explained-simply) deep dive.

#### Blocker 3 - No dependency mapping means cascading failures

When you build without organizing work into sprints, agents try to build features that depend on code that does not exist yet. Front-end components reference API endpoints that have not been created. Database queries call tables that have not been defined.

The Atlassian MCP currently cannot create sprints directly in JIRA. That is a real limitation. Gabor uses tags as a workaround. He tags tickets as Sprint 1, Sprint 2, Sprint 3 and maps dependencies between them manually before starting the build. Without this step, the entire multi-agent workflow falls apart.

Every PM who has gone from prototype to production with AI agents has hit at least one of these blockers. The ones who shipped figured out the workarounds. The ones who quit assumed the tools were the problem.

Here is what the three blockers look like side by side, and what flips the moment you stop one-prompting and start running a team.

![](https://substackcdn.com/image/fetch/$s_!3lp7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51c7c9a3-b766-416f-b6e9-365680dff5b5_2160x2767.png)

---

## 2\. The 21-agent team architecture

You do not need 21 agents to start. Three will get you surprisingly far. But understanding the full architecture shows you where the complexity lives and which roles to add as your projects grow.

Here is the full roster: four clusters, 21 roles, and the markdown file pattern that makes them portable across every project you build next.

![](https://substackcdn.com/image/fetch/$s_!iTZB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d2e0254-5f68-4756-8ab7-45d0510873bf_2160x2754.png)

#### 2a. The core agents every PM needs

**The System Analyst** is the linchpin. It breaks down product requirements into technical specifications. It asks clarifying questions one at a time. It documents decisions in [Confluence](https://www.news.aakashg.com/p/ai-draft-email-mcp). It creates tickets in JIRA. Without this agent, every other agent operates on incomplete context.

In the episode, the system analyst asked 14 clarifying questions before a single line of documentation was written. Vector DB choice. Usage limit mechanics. Conversation history handling. Search fallback strategy. API provider. Minimum iOS version. Screen count. Naming conventions. Each question one at a time so the answers stay deep.

The prompt pattern that makes this work -

> “Please act like a good system analyst. Ask clarifying questions until you have a complete and comprehensive understanding. Ask questions one at a time. Do not start writing documentation until all questions are answered.”

Two critical instructions. “One at a time” prevents the agent from dumping 25 questions at once. “Do not start writing” stops it from jumping ahead before the spec is complete. Different LLMs have different tendencies. Some love to start coding instantly. You need to explicitly constrain them. This is the same principle behind the [prompt engineering](https://www.news.aakashg.com/p/prompt-engineering) techniques that work across any AI tool.

**The Spaghetti Agent** handles code maintainability. Naming conventions. Circular references. Comment quality. Structural debt. Born from that Reddit comment. When Gabor ran it on his codebase for the first time, it caught problems he never knew existed.

**The UX Flow Architect** creates clickable prototypes using Figma’s built-in prototyping arrows. This is a small but important detail. The early versions of this agent placed visual drawn arrows between screens instead of using Figma’s actual prototyping connections. The prototype looked like it had navigation. But when you clicked play, nothing happened. It took months of iteration to fix.

Each agent has a specific [Claude Code agent markdown file](https://www.news.aakashg.com/p/how-to-use-claude-code-like-a-pro) that defines its role, its constraints, and its interaction patterns. The setup mirrors how you would build a [Claude Code Team OS](https://www.news.aakashg.com/p/claude-code-team-os) for a human team.

#### 2b. The real blockers nobody warns you about

**The Figma MCP color problem.** When you connect Claude Code to Figma through the MCP and pass it your full specification, the screens look structurally correct but the colors are wrong. Not slightly wrong. Completely wrong. The model compressed the context and dropped your entire visual identity. The fix is to pass the brand guideline as a separate, focused input to the Designer Agent. Never bundle it with the functional spec.

**The Atlassian MCP sprint limitation.** The MCP currently cannot create sprints directly in JIRA. Gabor uses tags as a workaround. Sprint 1, Sprint 2, Sprint 3. It works. But it means dependency mapping is a manual step in the system analyst prompt, not an automated feature.

**The consumer app vs Claude Code gap.** An agent role you set up in the Claude consumer app does not automatically transfer to Claude Code. You need to define agents separately in both environments. The system analyst in your consumer app conversation is a different instance from the system analyst in your Claude Code agent folder. Your [AI PM stack](https://www.news.aakashg.com/p/ai-stack-pm) needs to account for this separation.

**The $200 Max plan economics.** On the Max plan, a major build session uses roughly 10% of your monthly allocation. That means you get about 10 full build sessions per month. For a side project, that is plenty. For a production workflow with daily iterations, you need to be deliberate about when you run multi-agent sprints.

#### 2c. Why reusable agents beat fresh setups

Every painful lesson, every edge case fix, every API workaround gets encoded into the agent markdown file. The next project starts from a position of strength. The Spaghetti Agent that took weeks to calibrate on project one is immediately useful on project two. The UX Flow Architect that took months to stop drawing fake arrows works correctly from day one on every subsequent project.

This is the compound interest of building with agents. The first project is slow. The second is faster. By the fifth, your agent team is genuinely effective. Gabor’s Maven course walks through the full setup at [maven.com/gabor/productbuilder](https://bit.ly/4bPulv7).

*The 21 agents are not the point. The point is that every role on a software team can be replicated by a scoped, reusable AI agent. Start with three. Add roles when you hit friction.*

---

## 3\. The spec-first workflow

Most tutorials start with the terminal. Open Claude Code. Start prompting. Start coding.

That is backwards. The workflow that actually ships production apps starts in the consumer app. On your phone. Possibly while walking your dog. The process maps cleanly to the [PM OS](https://www.news.aakashg.com/p/pm-os) framework that works for any complex project.

#### 3a. Define the system analyst role first

Before you describe your app, you ask the LLM to define what a good system analyst does. This creates a behavioral framework that the agent will follow for the rest of the conversation.

The prompt -

> “What is the difference between a good system analyst and a bad system analyst in a software development team? Be as detailed as possible.”

The response gives you a blueprint. Requirement elicitation. Stakeholder management. Process modeling. Dependency documentation. You then instruct the agent to act like a good system analyst.

This is the same principle behind [AI agents for PMs](https://www.news.aakashg.com/p/ai-agents-pms). Define the role explicitly before assigning the task. It works in [Claude Cowork](https://www.news.aakashg.com/p/you-should-be-using-claude-cowork) the same way it works in Claude Code.

#### 3b. Dictate, do not type

This is where [superwhisper](https://superwhisper.com/) changes the game. In the episode, the app specification was dictated in a single long monologue. Technology stack (Flutter + Firebase). Data storage rules (device-only, no server-side user data). API key security (Firebase Secret Manager, never exposed to front-end). Usage limits (20,000 word cumulative cap with escalating cooldowns). Tone of voice (friendly but firm, like a 20-year referee friend). Vector database configuration (Vertex AI embeddings for IIHF rulebook and Situation Book).

Typing that specification would have taken 30 minutes and produced half the detail. Dictating it took five minutes and captured every nuance. The longest dictation prompt in the history of this podcast.

Here is the actual prompt, the five-step workflow it kicks off, and the two-word constraint - “one at a time” - that stops the agent from face-planting.

![](https://substackcdn.com/image/fetch/$s_!duT9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8a3d123-3586-48ca-aad5-dda3d97921bd_2160x2724.png)

The key rule - even if you ramble, even if you are not perfectly concise, the LLM will understand. You lose nothing by over-specifying. You lose everything by under-specifying. This applies whether you are building a [prototype](https://www.news.aakashg.com/p/ai-prototyping-for-pms) or shipping to production.

#### 3c. Documentation before design

The system analyst creates the full Confluence documentation before any design or code begins. Product overview. Technical architecture. AI agent specification. Data flow diagrams. API endpoint mapping.

Without documentation, every agent operates on partial context. With documentation, every agent operates on the same source of truth. I covered this exact approach in my [PRDs guide](https://www.news.aakashg.com/p/product-requirements-documents-prds). The principle is identical whether your team is human or AI.

*The boring part of building is the specification. The exciting part is watching agents create screens and write code. But if you skip the boring part, the exciting part produces garbage. The PMs who understand [product strategy](https://www.news.aakashg.com/p/ai-product-strategy-2026) already know this.*

---

## 4\. From design to code without touching either

Once the specification is locked, the workflow shifts from the consumer app to three parallel tracks. This is where the 21-agent architecture pays off and where most of the real-world friction surfaces.

Three tracks - design, tickets, build - running in parallel into four sprints. 72 minutes from idea to App Store submission. Here is the map.

![](https://substackcdn.com/image/fetch/$s_!ZKON!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff336dcd0-beae-4179-8cbd-583d8a83c463_2160x2700.png)

#### 4a. Design through Figma Make and Claude Code

Start in Figma Make. Go to Spotted in Prod. Take screenshots of apps you admire. Feed those into Figma Make to create a brand guideline. Typography. Color palettes. CTA buttons. Error states. Transitions.

In the episode, two inspiration images produced a full brand guideline. One of them was a photo of a laptop cover. Figma Make derived custom colors from the image without manual hex entry.

Claude Code then used the [Figma MCP](https://www.news.aakashg.com/p/ed-bayes-gui-seiz-podcast) to build actual screens in Figma based on that style guide. Five screens appeared in real time. Each one matching the brand guideline. The Chrome DevTool MCP lets Claude Code visually verify designs in a browser, catching visual bugs the Figma MCP alone cannot detect.

#### 4b. Tickets with the full team review

The system analyst creates JIRA tickets. The entire agent team reviews every ticket before development starts. This is the step that separates production builds from demo builds. Same [product launch](https://www.news.aakashg.com/p/product-launch-playbook) discipline, different toolchain.

Designer agent verifies screenshots are attached. Test Architect ensures test coverage. Spaghetti Agent sets naming expectations. Product Council confirms data storage policies. CTO Agent validates architecture. This maps to the [AI observability](https://www.news.aakashg.com/p/ai-pm-observability) principles I wrote about previously.

#### 4c. Sprint execution with the dependency mapping workaround

Tickets organized into sprints using tags (Atlassian MCP workaround). Dependencies mapped. Database setup in Sprint 1. API in Sprint 2. Front-end in Sprint 3. Integration in Sprint 4.

> “Claude, start building. Go for Sprint 1. Once done, Sprint 2, then Sprint 3, and so on. If you have any questions, ask.”

Multiple agents work in parallel. The coding phase is the fastest part. On the $200 Max plan, roughly 10% per session.

*Everything before the code is the hard part. Once those are right, the code practically writes itself. This is true whether you are [shipping to production](https://www.news.aakashg.com/p/pm-guide-ship-production) as a PM or managing an engineering team.*

---

## 5\. What PMs gain by building with agents

*If agents can spec, design, code, and test, what is the PM actually doing?*

**Making product decisions. The tools just got absurdly faster.**

#### Gain 1 - Firsthand understanding of agent behavior

When you interact with agents daily, you develop intuition for context window limits, hallucination patterns, and compression behaviors. That intuition directly improves your roadmap decisions. You stop over-scoping agent features because you know where agents break down. You stop under-investing in [evals](https://www.news.aakashg.com/p/ai-evals) because you have seen what happens without them.

Gabor has not written production code in 15 years. But he now understands agent behavior better than most PMs who have only read about it. That understanding compounds across every product decision.

#### Gain 2 - A portfolio that proves competence

A working app on the App Store is undeniable proof. Password-protect a section showing the build process. Confluence docs. JIRA tickets. Agent architecture. That [portfolio item](https://www.news.aakashg.com/p/vibe-code-pm-portfolio) says more than any certificate. It says you shipped.

#### Gain 3 - Iteration speed that compounds

The first build is the hard part. The UX Flow Architect alone took months. The Spaghetti Agent needed weeks of tuning.

But once v1 ships, everything accelerates. New features take a morning. The reusable agent files carry forward every lesson. The PM who has shipped one app can ship the next in a fraction of the time. Not because the tools are better. Because their agents are better.

Stack those three gains over a year and the gap between PMs who build and PMs who watch stops being a gap. It becomes a moat.

![](https://substackcdn.com/image/fetch/$s_!K1qy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc057e217-24f5-414f-85ff-ae52ed3bcda0_2160x2767.png)

*You do not need to know how to code. You need a willingness to understand how software works and the patience to specify before you build. If you want to get started, [my Claude Code guide](https://www.news.aakashg.com/p/how-to-use-claude-code-like-a-pro) walks through the full setup.*

---

## Where to find Gabor Mayer

- [Maven course - Go from PM to AI Builder](https://bit.ly/4bPulv7)
- [LinkedIn](https://www.linkedin.com/in/mayergabor/)
- [X](https://x.com/gabor_pm)

---

POLL

### What did you think of today’s post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

YOUTUBE TRANSCRIPT
AI agents are writing PRDs, designing in Figma, writing JIRA tickets and even shipping code all from 1pm at 4am.

Gabor Meyer

I set up these agents on a way how I would imagine in a real world I would work with a group of software engineering team members. If you build a good specification and you break it down appropriately then you will have a much better quality end product.

Aakash Gupta

What breaks when you give AI agents too much context? And what's your honest take on co-work and dispatch?

Gabor Meyer

White Pudding is just the rebranding of unmaintainable, low-quality source code.

Aakash Gupta

Gabor Meyer is a product manager at Google who has spent the last five months building AI-powered apps using a team of specialized agents. And in today's episode, he's going to walk you through his agent setup, and he's going to show you how you can go from zero actual app in the App Store in

just a couple of hours. The gap between you and the other PM, in two years it's going to be huge. If people want to get started, where should they go?

Gabor Meyer

The best place to start, if you just want to do it for yourself, pull up your favorite AI, ChatGPT Gemini Crowdcode, and start asking questions on how to do things.

Aakash Gupta

If you stay to the end, you'll see a live demo of Gabor's agent workflow and see how to set up your own agent team. Before we go any further, do me a favor and check that you are subscribed on YouTube and following on Apple and Spotify podcasts. And if you want to get access to amazing AI tools,

check out my bundle, where if you become an annual subscriber to my newsletter, you get a full year free of the paid plans of Mobbin, Arise, RelayApp, Dovetail, Linear, Magic Patterns, Deep Sky, Reforge Build, Descript, and Speechify. So be sure to check that out at bundle.akashg.com. And now into today's episode.

As PMs, we've been working in this model where we work with human developers, human designers. But what if Cloud Code was your designer, your developer, your systems analyst? I've had plenty of episodes on Cloud Code, but today's episode is different. It's not a PM operating system. It's a startup operating system.

Gabor Meyer is a PM at Google who has been staying up till 4 or 5 a.m. every day playing in Cloud Code, and he has figured out how to create an entire startup inside Cloud Code. front-end engineers, back-end engineers, legal counsel. And in today's episode,

he's going to walk you through his agent setup and he's going to show you how you can go from zero to an actual app in the app store in just a couple of hours. Gabor, welcome to the podcast.

Gabor Meyer

Thank you so much. I'm glad to be here.

Aakash Gupta

Gabor, you told me something pretty crazy, which is that you're not just using CloudCode for PM tasks. You're using it to replicate a company. You have a 15 agent team, CTO agent, design agent, coding agent. Can you walk us through your agent setup in CloudCode?

Gabor Meyer

yes absolutely so I have actually now I just realized that it's 21 agents apparently according to what I can see on the screen so the probably the most important agent that I use is the system analyst agent I set up these agents on a way

How I would imagine in a real world I would work with a group of software engineering team members. So I have someone who looks after the brand, I have someone who looks into whether our code is maintainable. I have a CTO who looks after the more strategic technical decisions, I have designer agents,

I have agents that implement the actual software, the code I have an agent which takes care of the performance of the application. I have another designer agent. I have a product council which looks into how do we handle data, how do we

We store data just to make sure that we are not leaving anything available for bad actors. We also have a product spec architect which usually checks for me whether our specification is well structured and easy to understand. This will be important later. I will walk you through that. We have a test architect which designs how we

guarantee the quality of the whole application. And then I have a UX flow architect. This will be very interesting when we are designing the clickable prototype, which is the basis of the app. We will come back to the UX flow architect as well.

Aakash Gupta

Amazing. Can you show us inside one of these agent markdown files? Since you mentioned system analyst, I'd love to see under the covers what that definition looks like.

Gabor Meyer

Yes, of course I can show you. This is my system analyst agent. So this basically breaks down product requirements and technical specifications and it pretty much operates as you would expect from a system system analyst so if there's anything ambiguous it asks you questions it also takes

care of dependencies so that they are properly documented and I find that the system analyst agent is really a key player in my setup because the system analyst agent is the one that I use to create both my documentation as well as my tickets for the

Aakash Gupta

development amazing so that's the high-level view of the system guys now we're going to show you through a live demo zero to test flight where should we get started

Gabor Meyer

yeah let me walk you through how I build and to make it more accessible for product managers who might not be fully comfortable using cloud code just yet let me start this whole process from the cloud app the desktop app or This is basically the consumer app that you can run on your mobile device as well

So the way how I usually start building anything is that I start creating a description of what I want to build And the reason why I love to use the consumer app for this is because it allows me to use it even let's say while I'm walking my dog

I can put cloud into voice mode and I can talk to cloud and I can define new features I can ideate what I want to build so let me show you how I get started At first I will tell Claude to act like it is a system analyst and then I will ask

Claude to listen and create the idea with me of a new application that we will build today. The application that we will build today is an AI chat application that helps ice hockey fans understand the rules of ice hockey better. Why exactly that? Because I was an ice hockey referee for 20 years

And I would have always loved if the fans and the players or even ourselves, the referees, would have a better understanding of the rules and an easier way to find the applicable rules for some niche situations. So that's what we will build today. How does that sound?

Aakash Gupta

Sounds useful.

Gabor Meyer

All right, cool. So the very first thing that I do, and again, you can do this on your mobile phone, open your cloud app or your favorite AI app, whatever it is, ChatGPT, Gemini, you name it. And start by, and by the way, I will use dictation here.

So sometimes I will talk to the camera, but sometimes I will talk to cloud. Now I will talk to cloud. and I will set up a system analyst and this is how I do it so you don't necessarily have to define everything by yourself you can use the LLMs and the Gen AI to help

you craft stuff so look at this Can you tell me what is the difference between a good system analyst and a bad system analyst in a software development team? And in general, can you define me the role of a system analyst in a software development environment?

Please be as detailed as possible about everything that the system analyst does and always point out what is the difference between a good and a not so good system analyst. So as the first step I basically just ask for a definition of what a system analyst

does When I send in this prompt it will now tell me what a system analyst does and it will point out what's the difference between a good system analyst and a bad system analyst Requirement Documentation Requirement Elicitation Stakeholder Management Process and System Modeling So it describes you pretty well what are the things that a system analyst does

Aakash Gupta

Gabor has a course on Maven called Go from PM to AI Builder with Cloud Code. It's a four-week program. The pitch is simple. You ship a real app, not a prototype, not a certificate. An actual app on the App Store or Google Play with an AI feature built in.

He walks you through the full stack you've seen today, plus more. Cloud Code, Flutter, Firebase You get live workshops every Thursday, a build companion app with milestone checklists, and Gabor in the trenches with you until your app ships. It's $2,995 but you get a discount with my link in the description. Full workflow, lifetime access to recordings,

and a community of other PMs building alongside you. This is for mid to senior PMs who want to become AI PMs but don't get to build AI products in their current roles. Technical ICs with a product idea, PMs in career transition who know a certificate won't differentiate them. You don't need to know how to code,

you just need a willingness to understand how software works.

Gabor Meyer

The link is in the description. If you've enjoyed today's episode and thought, I want to build that, check out his course.

Aakash Gupta

Today's episode is brought to you by Amplitude. Replays of mobile user engagement are critical to building better products and experiences, but many session Replay tools don't capture the full picture. Some tools take screenshots every second, leading to choppy replays and high storage costs from enormous capture sizes.

Others use wireframes, but key moments go missing, creating gaps in your understanding. Neither approach gives you a truly mobile experience. Amplitude does things differently. Their mobile replays capture the full experience. Every tap, As the next step, I will tell the app to act like a good system analyst and help me define a product that we will build.

For full context, I will provide the system analyst agent

Gabor Meyer

links to our documentation. So actually, let me explain how I store my documentation. So for documentation and why is it needed? I use the Atlassian Jira and Confluence for documentation let's focus at first on Confluence I use Confluence just because it's pretty much an industry standard in

many companies so I thought it's a basic choice but you can use whatever software documentation tool that you want, there are a bunch out there. I picked this one because it also integrates through an MCP to Cloud. So I went into Cloud, I connected through the settings and connectors the Atlassian MCP and I hooked up

my Atlassian account and now I have a completely empty Confluence space and this is where our documentation will live and I have a completely empty Kanban board where our software development tickets will live. Why do we need this development? The reason why we need this development documentation is because if we document our decisions,

our specification and our software development steps really well, they will be replicatable and your app will be maintainable. a very typical mistake that many product managers or in general people who vibe code do that they go into a vibe coding app or setup and they start by giving one

prompt and then they expect that at the end of that one prompt there will be a completely beautifully done software on the other side but this is the equivalent of you wanting to build a new house you go to one guy you speak to that one guy and tell the one guy build me a three

bedroom house with two bedrooms and then half a year later you come back and surprise the house might not be just how you like it but instead if you would have spoken to a team leader of a team let's say an architect who has a a complete team that builds the house

and specified what you need you probably would have had a much better outcome in the final house building instead of the mess that you got when you just spoke to one guy one time right and this is the same here If you build a good specification and you break it down appropriately,

then you will have a much better quality end product. So let me give the two links, the Confluence and the Jira link to my system analyst agent and start talking to it as we are brainstorming around the app.

Aakash Gupta

So what I'm hearing is that the classic product management skill makes you a better vibe coder. Where do we go from here?

Gabor Meyer

So from here I asked the cloud app to tell me what a good system analyst and a bad system analyst does and now I will ask the system analyst or cloud to act like a good system analyst and I will provide the system analyst the idea or the description of what I want to

build and I will also give the system analyst my Confluence page and Jira just as a context that this is where we will save everything that we discussed. So this is how I do it. Okay, please act like you are a good system analyst. and your goal will be to help me create a comprehensive documentation for an

application that we will build. It's important that at first I don't want you to start writing any documentation. I want you to ask clarifying questions until you have a complete, comprehensive and full understanding of what we are building. Please ask as many clarifying questions as you need to but ask questions one at a

time because I might get overwhelmed if you ask too many questions at once. Also I provide you a Confluence and a Jira link that you can reach through the Atlassian MCP These are the only Confluence, Space and Jira boards that you can use. Please do not touch any other board or space or project through the Atlassian MCP,

only these two. this is there were a couple of important things in this prompt firstly it's important that you ask the agent to ask you questions before moving forward different agents have different tendencies some agents or some LLMs love to start coding instantly some agents love to start writing instantly so that's why I was

telling Claude do not start writing but ask questions so that's first important point the second important point is that you want to tell to ask you questions one at the time because sometimes it comes back with like 25 questions in which case you easily get overwhelmed and it's very hard to answer all

of the questions so if it asks one at the time then it's It's a much more linear conversation. And yeah, obviously, giving the Jira and the Atlassian link makes sure that you have all your project-related stuff at one place. So let me just add those links. Oops, I forgot that this also puts it on my clipboard.

So here are the links. yeah so now it will set up and the next step i will define what we want to build it's confirming that it will just ask me questions now it's checking the space asks my permission to access those spaces one thing i'm noticing is that

Aakash Gupta

The average person, they would just want to jump in. They wouldn't want to define the role of a system analyst, create the connection to Atlassian. What you're doing is you're putting effort in the scaffolding up front so that as you go along building, you don't run into kind of spaghetti code,

undocumented code that you can't build on top of. Is that right?

Gabor Meyer

That is absolutely right. The spaghetti code has a slightly different angle to it as well because oftentimes when people who don't understand code and yeah I have an engineering background but I haven't done industrial level coding for like 15 years we wouldn't be able to recognize when there are major issues in how the software is

structured and I read or read it a comment about vibe coding which was saying something like vibe coding is just the rebranding of unmaintainable low quality source code and it definitely hit home with me so what I did I created a spaghetti agent which I think my setup code

like code maintainability agent or something like that but what I thought that the spaghetti agent should do is that it should make sure that there are no circular references that are commenting in in the code is high quality, that naming conventions are followed. These are things that as a product manager,

I remember that we were always very mindful of when doing software development. So I just told the agent to watch out for these. And when I ran it for the first time on my code base, it did catch some of those issues.

nice cool all right so as the next step we need to define what do we want to build but before we do so i want to make one differentiation an agent or a role that i set up here in this discussion in this chat in the cloud app is not available in

cloud code so in cloud code we actually need to set up our agents separately and we will have a system analyst there and we have a system analyst here but they are not exactly the same so my system analyst agent setup will be separate there and it will act on its own behalf whereas here it is just

acting like a system analyst does it make sense yep cool and just to accelerate things let me actually kick off the creation of those agents on the cloud code side because it will take a couple of minutes so it can run in the background it will be very useful for us

First we will want to set up the agent so let me tell Claude that we will do this and right now If I check what agents I have, I literally have no agents. Sorry, actually I was not in Claude yet. So let me start Claude. This is the first time we are starting Claude in this space,

so I expect that I will have no agents. oh interesting I have interesting okay I have one system analyst agent which probably comes from a global agent setup that I might have set up previously which is all over user specific instead of just being project specific yeah it's a user

agent but I don't have any of the other agents but now we will set them up so the way I usually set them up is this I will give you two files now. One will be an agent setup with several agents that I want to use in this project and I will also give you a

Different file which has a couple of processes that I use in development such as few steps defined how to handle bugs or few steps defined how to create new features. Please add this to the project memory. By the way, do you also say please when you talk to AI?

I don't know why I do it, but I always say please.

Aakash Gupta

No. But I do give it encouragement. I will be like, okay, you've given me a 7.5 out of 10 draft. Now we need to get it to 8.5. Here's what we can do.

Gabor Meyer

All right so these are the agents and the workflows so now if I hit enter oh I need to authenticate okay this part we will definitely ah we don't need to cut okay because it went to another screen just one sec okay looking successful good let's try again and just for context quickly check

where we stand with the usage of cloud that's my cloud API here so right now we are standing on yeah two percent of the usage quota so we will see by the end of the building where do we stand on the usage quota oh this will be

Aakash Gupta

fun to see

Gabor Meyer

yeah all right cool so our cloud cloud code should be yeah building the agent and we can go back to cloud and start discussing what the application is supposed to do okay this will be a longer dictation so bear with me I want to create a mobile app which will have a Flutter frontend and a Firebase backend.

The mobile app will be a simple chat screen and in this chat interface the user will be able to have a discussion with an AI agent about rules of ice hockey, specifically the International Ice Hockey Federation rules, IIHF rules, and I want the user to be able to ask questions and get answers about the rules for

this application. I will provide two sources for the AI agent in the background. One will be the official IIHF rule book and the other one will be the IIHF situation book. These both will have have to be converted into a vector embedding, put into a vector database and converted into embeddings because I want to optimize

my but firm. I want the agent to act like a good friend of the user who has been a referee for 20 years. no coincidence I was a referee for 20 years in ice hockey and I often when I was watching games fans approached me and asked questions so I imagined that I would be

inside of that AI answering questions based on the latest rules there is Another aspect that the AIH is for the 2025-2026 ice hockey season and something that you find online about an earlier situation, let's say if you find a Reddit discussion about a specific and relevant situation from 2022 or 2024,

They might be outdated or based on an outdated rule which might have changed ever since. Whenever you refer to such a discussion always flag this for the user that the discussion or the source that you found online was from an older time which might mean that the rules have changed ever since.

If you can also double check the latest rules and the conclusions that you found in online sources. The primary lookup should always happen in the rulebook the secondary lookup should always happen in the situation book and then the fallback should be the online search through the search API when the user

asks you something our goal should be to find an accurate answer but we also want to be mindful of how much So we want to be balanced between the amount of context that we send to LLMs and the accurate of the answer that we are bringing in.

There will be some usage limitations because I don't want an infinite amount of cost on the API. for this reason if any user would have spent more than 20,000 words in either direction of the conversation combined so this includes what the user said this includes what the AI agent responded so anything that goes beyond 20,000 words

should be stopped and the user's allowance should be suspended for 24 hours and the user should get a warning that for 24 hours you cannot ask more questions because you reached a limit. After the 24 hours expired the user can again ask questions. The technical stack we clarified also I want to make sure and this is exceptionally

important that API keys should be stored in the Firebase Secret Store and never exposed to the frontend or to the source code because I don't want additional cost incurred by existing I am accidentally exposing my API keys. So please make sure that API keys are never exposed to the code, especially not to the frontend,

and they are only stored inside of the Firebase Secret Manager. The app will be launching on iOS only for now and the minimum version I'm preparing for is iOS 16 or later. Feel free to ask any clarifying questions that you may have.

Aakash Gupta

AI is writing code faster than ever, but can your testing keep up? Testkube is the Kubernetes native platform that scales testing at the pace of AI accelerated development. One dashboard, all your tools, full oversight. Run functional and load tests in minutes, not hours, across any framework, any environment no vendor lock-in no bottlenecks just confidence that your AI

driven releases are tested reliable and ready to ship testcube skill testing for the AI era see more at testcube.io slash akash that's t-e-s-t-k-u-b-e dot i-o slash a-a-k-a-s-h Are you looking to land your next product management job? I am accepting a group of just 30 product managers into a 12-week cohort led by me

where every Monday for 90 minutes I help you through your job search, creating your candidate market fit, updating your LinkedIn, You're going to get personalized feedback and one-on-one mentorship sessions with my co-teachers Ankit Farmani who is an AIPM at Atlassian and was a Group Product

Manager at Meta Prasad Reddy who is a CPO and has been in product for over 26 years as well as my other live instructor Bart Jaworski who's going to run another 90-minute session per week where we really help you deliver on all of the deliverables in an actionable way and get you custom resume feedback custom

LinkedIn feedback this program worked If you want to get a higher paying PM job, be sure to check out my LandPMJob.com cohort. The next cohort starts in February, runs through the end of April. The next time I'm opening up a cohort is in May.

So if you want coaching from me to land a PMJob, this cohort is a no-brainer. It is a premium priced product. It is more expensive than the average product out there, but the return is huge. Most people who join the cohort see a salary raise anywhere from I hope you're enjoying today's episode.

Are you interested in becoming an AI product manager?

Gabor Meyer

Making hundreds of thousands of dollars more,

Aakash Gupta

joining OpenAI and Anthropic, then you might want to do a course that I've taken myself, the AIPM Certificate, ran by OpenAI product leader, McDad Jaffer. If you use my code and my link, you get a special discount on this course. It is a course that I highly recommend.

We have done a lot of collaborations together on things like AI product strategy. So check out our newsletter articles if you want to see the quality of the type of thinking you'll get. One of my frequent collaborators, Pavel Hearn, is the Build Labs leader.

So you're going to live build an AI product with Pavel's feedback if you take this AIPM certificate. So be sure to check that out. Be sure to use my code and my link in order to get a special discount. And now back into today's episode.

Gabor Meyer

Now I stop the dictation. The brilliant thing about dictation is that just imagine how long it would have taken me to type all of this up. I could have provided way deeper context to Claude that compared to what I would have been able to provide while typing.

And even when I was not super concise all along the way, it will figure it out and it will be a good outcome.

Aakash Gupta

Any observations you might have? That was the longest dictation prompt we have seen yet on this podcast. Impressive.

Gabor Meyer

yeah we might want to 2x the speed but yeah I like to define very well in the beginning because if you have a good specification then you will have a good product if you have a sheet specification then you will have a subpar product and you can see that Super Whisper is still doing the

transcribing but I like that even if I speak kind of this long it always transcribes quite well the only thing is that I can't really click away from it ah there we go pasted yeah it wasn't that long for the transcription okay let's see in the meantime okay so our agent setup seems

to be done let me see what agents do we have now somehow it did not set up our agents in the project so I will try it again now okay let's see if it does it now I think the confusion was that I placed these MD files into the project and it assumed that it will just

use that project file all the time but now I try to prompt it to more explicitly to set it up so we will see if it sets up the actual agents and in the meantime let's go back to our system analyst here question two 20,000 were usage limit needs to be tracked per user

it will be just stored on the device so it will be a per device tracking we also don't want any user input to be stored on the server side we only want to store information that came from the user on the mobile device of the user this means that the user would not need to create a login

or an account they would be just using the app without authentication and we would be just processing information on the server side but we never store anything on the server side This simplifies the mobile app launch as well, especially when you are creating your very first launch because if you don't store

user information that is just easier for the first launch process. Okay, so let's see if now we have agents. and we don't. Interesting. The weird thing is that it tells me that it did set up the... Actually let me then just create a...

new directory and do it from there because this is literally the first step and for some reason it does not like my agent setup so I will now create a separate folder and we will develop in that folder it's a new folder okay this one

Aakash Gupta

Always, when you do the live demo, it's like now.

Gabor Meyer

Never happened to me. This literally never happened to me. This setup, I did it and I helped many people do the same. And this setup never failed. Well, it's okay. Sometimes it happens. So now we change over. Cloud. Here is our cloud. And now...

I will just reuse this prompt And hopefully now it will ask me for permissions to read Yes, this is good Because it should read yes it can read from that file yes this is looking already much better one thing that i would highly recommend everyone who is building especially for the first

time when you are doing vibe coding always read always read what it what cloud code asks because it happened to me once that it asked me to provide to give an agreement for it to read the secret storage of my Chrome passwords. Obviously, I did not provide that agreement. I didn't quite feel comfortable with that.

I even have a screenshot of that. You have to be always mindful what you allow cloud code to do and what you don't allow it to do. Generally, as a rule of thumb, as long as it operates inside of the development folder, you are good.

But as soon as it would operate outside, then it would be something to watch more closely.

Aakash Gupta

and as you speak of it, it's actually trying to make some directories.

Gabor Meyer

Yeah which is fine because this is basically now setting up the infrastructure that it needs but it is setting up inside of the right directory so I can see that it is setting it up inside of the rule ask directory and that is the new directory that I

created and now it is creating all of those agents that we try to create in the ruleask.com directory which for some reason didn't happen on the first attempt but now it is happening so it's all good so let's go back to our questions about the system so

since the conversation history lives on the device I need to understand how the chat experience works when the user closes the app it reopens yeah okay this is a good question When the user reopens the app, they should be shown a list of previous conversations that they had and they would

be allowed to start a new conversation or look up or even continue a previous conversation. When a conversation appears in the list. Oh, okay. This is a good question. Each conversation should have a short summary, like a couple of words summary. what the conversation was about and when the user continues the conversation and it

evolves this short summary might change over time. This can be auto-generated by the LLM. Do you have many more questions left? Now I'm getting a bit impatient and eager to build. oh my gosh it has more yeah they can review the previous conversations but we don't

want them to be able to continue those conversations but they can review it yes that's the name of the app and the last question yes it can show the link and in that case i don't really want an in-app browser so it should just open

the system default browser okay and this concludes our questions so now the magic will happen because now that all the questions are done now I will tell Claude to create the documentation and it will be fascinating to see how it creates all the

Aakash Gupta

documentation okay so what epics what tasks what the Jira setup looks like the confluence setup I want to see how detailed it gets it does it really simulate a

Gabor Meyer

human team Yeah, I'm a bit concerned because I told it not to use Jira just yet, so I might stop this. Please do not create any Jira tickets yet, only create the comfort influence documentation for now this is important because first we want to create

the design as the next step and once the design is done that's when we want to start creating the development tickets because the Jira tickets will be for development so now I just want the documentation to be created okay so let's see

our pages and by the way a quick look at our usage yeah not much five percent we will go much further up right so let's see the documentation it was empty and now we actually have pages so let's go one by one product overview problem statement target audience Okay, very basic. Good, always allow.

Now it will create more. Technical Architecture, this will be interesting to see. While this is happening, let me move on to the next step and we will come back to it because this will craft for a few minutes. Is that okay?

Aakash Gupta

Yeah. Okay. Good.

Gabor Meyer

And our cloud is in the meantime doing its settings, creating all the agents that we need. which is good alright so the next step what I usually do is that I need to create a design for an application and I do this usually in two steps so one step is that I

go into Figma Make in Figma Make I create a app guideline, design guideline or design brief with typology and color definitions and all the different buttons and color transitions so that I can use that design specification as a basis of my actual design. So step one is that I need to create this.

For that, I usually like to do some kind of inspiration. The way how I get inspired is I just go to Spotted in Prod and I look through applications here you can see a bunch of applications and whichever catches your eye and feel that yeah okay this looks like a good design

you can just click on it take a screenshot and reuse it for your own app I literally don't really overthink it I just I just take a screenshot on whichever item I feel that it looks appealing to my eye and that's about it. Yeah, this looks like a decent Okay, this is the cloud app.

No surprise that I'm intrigued to take it, but this looks interesting, but I don't like the color pattern. Okay, I like these logos. okay this looks interesting so I take a screenshot of this and this website spottedinprod.com it's free yes I think it has some content which is free and then

it has some content which is paid but there is a bunch of content that is free and also you can actually use much simpler things let me show you what I sometimes use but let me first put the prompt so now we are in Figma Make and I will tell

Figma Make what I want to do we will create a brand guideline for a mobile application. I want you to create the whole typography definition, colors, CTA buttons, color transitions, error stages and so on and so on. So I need a full package that can provide an input for a mobile app designer

with a comprehensive set of assets for a mobile application. The mobile application has the name of Rule Ask and the goal of the mobile application is to have a chat interface through which the user can ask AI about the rules of ice hockey. Please don't start designing anything just yet because I will provide you with a

couple of images that you can use as an inspiration for this design. Please do not copy anything just use it as an inspiration. this last part of the prompt to use it as an inspiration do not copy this is very important because if I wouldn't say that Figma would actually say sorry I cannot

create a copy for you because I think Figma figured out that people would just take a screenshot of an app that they like and then they would try to copy it which obviously wouldn't be great Super Whisper is slow but accurate okay so here and now let me put the images so here is one and then

the other one is this one I love this image so this one I took a screenshot sorry

Aakash Gupta

not a screenshot a photo of a

Gabor Meyer

laptop thing cover. So I took a photo of my laptop cover and remove the Apple logo and I will use this as an inspiration and we will see if the color palette will anyhow give us some remembrance of these colors. You can design now. All right. So we will now have the typography and everything.

So now Figma Make is designing.

Aakash Gupta

What do you think about Figma Make versus the other tools out there? Bolt, Replit, Lovable, Base44?

Gabor Meyer

So I have a very specific use case what I use Figma Make for and I only use it for creating designs such as this one I don't use it to create actual prototype with Figma Make at least I haven't utilized it because I feel that I can create a higher

quality prototype if I pair it up with Cloud Code previously I used Lovable but this was probably more than a year ago at that time I got quite frustrated with the issue that the AI was lying I found an issue I tell

the AI to fix it it said it fixed it and it didn't fix it and we were just going rounds and rounds and issues were still present and it was unable to fix it so I'm sure that Lovable and other tools got much better in the meantime

and these vicious cycles of errors don't happen all that often anymore but sort of that was a turn-off moment for me I tried I think I tried both once but I found that It was around the same time when I tried Lovable and I felt that Lovable was more convenient to use at that time.

So I went with Lovable and then I ran into this issue with Lovable and then Couple of months later like late last year I had this idea that you know what now that there are MCPs and stuff let's see if I could actually build a mobile app like

I wanted to challenge myself after seeing a podcast episode on Lenny's podcast with Zevi from Meta who also sort of built a lot of agents and prototypes for himself. He inspired me to get into the deeper side of VibeCoding because with Lovable for example or Bolt or with FigmaMake you go from prompt to prototype in one step.

But what we do today in this podcast episode is that we go from idea to prompt, prompt to code code to product so idea to prompt prompt to code code to product and I just like that more and look at that look at the colors look at the colors like this is this

is the crazy part this is the crazy part and also typography like man this is the exciting part I can't tell you how much I love this stuff like look at these Seriously, even like last year or before, creating this sort of quality input, how long would it have taken to get this output?

You would have hired an agency to create this for you. Isn't this absolutely incredible?

Aakash Gupta

Now it's pretty much the free version of Figma Mate.

Gabor Meyer

Yeah, I'm on a paid version, but yeah, I don't know how capable the free version is, but it is just mind-blowing Anyways, let's check back with our agents Okay, so in theory we have all the documentation done Let's see if our agents are properly set up it's still working but let's check our documentation so now refreshing confluence

oh yeah okay technical architecture let's see oh look at that it's pretty fancy yeah this is decent This is a decent technology stack, front-end, back-end, vertex AI, vector database, the two resources, embedding strategy, fallback Yeah, appropriate. Yeah, looks all right. Then, oops, sorry. Then, AI agent specification.

Aakash Gupta

When you're looking at this, what are you reading it for?

Gabor Meyer

I primarily read it whether it reflects accurately what I said so for example here receive the user query embed it search it against the similar things in the vector database evaluate confidence just that it goes through the steps and you can see like this is a beneficial part for a product manager if you build an application like

this like obviously I don't have a need to create a ice hockey rules app even though I will send this to a couple of friends and I think they will appreciate it but there is no need for me to create an ice hockey rules app but the benefit that if I can

Launch this app, put it into the App Store. I can literally put it on my resume as a portfolio item and I can show anybody that, hey, look, I built this and I can create a subsection of that app which I can let's say password protect where I would

provide all this information of how I built this application. So this provides an inevitable or undoubtable proof that I as a product manager I know what I'm doing around these systems and I can build. Okay, so let's see if our agents are now set up. Let's hope that at this time the system did not fail us.

There we go. Okay, so now we have the agents and we can use all of these agents. So now what we want to do is I want to give my style guide to the agent. So I have created a mobile app design guideline for the team to use. Here is the link for it.

Please save it to the project memory so that we will always refer to this style guide whenever we need to make a design decision about the application. and now we need to save this one and we save it to... here it is, good Saving into memory.

I already created an empty Figma file where I will ask the agents to save the design. As the next step I want SystemAnalyst agent to work with the designer agent and the brand agent to create the actual design and the screens in Figma through the Figma MCP for the application.

I want to create the smallest number of screens that can serve all the use cases. The goal is to have exceptionally high quality screens but rather small number of them. And when this will be building it, it will be also a quite mind-blowing experience to see.

And one more thing I would need to check, actually let me put this on the clipboard for now, is whether we have the Figma MCP connected just to be sure that it has access to both Figma Make and Figma because if we don't then it will start failing so that's an important part to do

this is the annoying part of using a CLI that you cannot just highlight everything and then with one tap delete the whole thing but you need to actually wait to delete or maybe I'm using it wrongly but yeah let's check our MCPs okay we are all connected

Figma is the most important and we have the Figma friend as well Good Xpector One MCP that I'm missing Can you also install the Chrome DevTool MCP? The Chrome DevTool MCP is useful because it can operate the browser and it can have a better comparison or visual to verify your design.

So yeah, we are allowing it to put it into this project. OK, Chrome DevTools has been installed. Whenever you install a new MCP, you actually need to restart Cloud Code. And now we should see. Yeah, Chrome DevTools connected. OK, perfect. All right, so now we can start our design.

Aakash Gupta

So now what I expect.

Gabor Meyer

is that it will start creating the design based on the specification and based on the figma make link and I think I didn't call out specifically the figma make so I can inject an additional instruction use the figma make style guide as a basis.

Aakash Gupta

Yeah, I love slash btw.

Gabor Meyer

Yeah, I love the by the way thing because it just injects it and it evaluates in parallel. See, it already accepted it.

Aakash Gupta

This is one of the things that you're going to get in Cloud Code that you're not going to get in Cloud. So besides the agents, you get a lot of different functionality. If you've been scared about using Cloud Code, open up that terminal.

Gabor Meyer

Yeah, exactly. It's very convenient, honestly. So you can see that now it runs multiple agents. So if I come to the Figma page, this is where I expect that the Figma designs will start showing up very soon. So as soon as the screens are done it will be much quicker. It's also fascinating to read these,

what are the things that are happening in the mind of the agents that are working on your behalf. The reason why I say that product managers should build is because if they understand how today agents work how they behave what are their limitations what are their ups and downs while using

them then it's much easier for any product manager to understand how their own product that they are working on should be serving users but if you don't interact with agents then you will not have a sense of what does it mean to work with an AI agent that's why it's super beneficial to build using AI agents

Aakash Gupta

100% the future of products mostly is going to be agentic you actually think about how Gabor described that he wanted to use Atlassian he said oh well they have an MCP server where I can easily connect to that's going to be the type of decision

someone is going to make and you're going to simulate making a lot of those decisions so that you can prioritize your roadmap correctly

Gabor Meyer

oh finally ok set up Figma file structure that's good and then build screen good now we will start seeing yes ok now let's see the magic happen we've got the Figma file structure and now it's starting to build the onboarding screen so this will be

very interesting to see how the cloud code is operating Figma I can also ask to give me the Figma links for the screens wow now this is cool we just needed to

Aakash Gupta

refresh and you can see that it is still working here

Gabor Meyer

the fifth screen has just appeared right so it like literally while we are talking it just added the fifth screen here it was telling that it is building and now the

Aakash Gupta

settings screen is done done yeah so this is a very powerful workflow that we've done up and until this point We specified exactly what we want in depth with Claude. Then we created a prototype in Figma Make. Then we used Claude code to build that in Figma. So that's where we are currently.

Gabor Meyer

Exactly. And if you look at these, just look at the level of detail, the precision You don't need to actually fix a lot of things. Maybe, for my taste, I would change a little bit this icon or this button to be the same size as the input box.

But even if you leave it like this, it is a completely appropriate looking design. And this is how your app will look. So the next step is that we will start turning this into a prototype. The way how you would put together a prototype is that you would manually select an item and then you would connect

with this prototyping button or prototyping arrow to the next screen where it needs to go and I automated this one as well so I can actually create this without doing anything just simply telling cloud cloud code to perform this step for me awesome

so the next step that we want to do is that we need to make this to be a clickable prototype so normally what you would do in Figma you would manually come and start connecting screens just like this but one of the agents

will do this for us so I will now ask the agent so these are our agents and the user UXflow architect will do this for us so here we go system analyst and UXflow agent please go through the documentation and the Figma and create the prototype arrows in Figma.

Please use the Chrome Dev Tool MCP where you need as well as the Figma MCP and the Confluence MCP. So now you will see that it will most likely open another browser window that it will take control of and then we will see how it is creating all the arrows and

while it will be creating the arrows because it will take some time we will start initiating the backend of the application. Okay, full Figma structure is there.

Aakash Gupta

All right, so we're getting those infamous parallel agent workflows started again.

Gabor Meyer

Yeah, we need to speed up a bit. Actually, I can dictate this one. So now I would like system analyst agent to create the first Jira tickets that would help initiate the backend of the application we don't want anything else right now just a couple of

tickets that would initiate the database and all the firebase basic setup that we need so that we can start connecting the domain and setting up the firebase secret store and so on so only do the very basics just yet create the Jira tickets so that we can go step by step and what it will do now is

that it will create these tickets for us so now we kind of have our front-end inner back-end processes starting to parallelize yeah so that we can speed up the process

Aakash Gupta

a bit how many agents are you typically running at once

Gabor Meyer

so it depends on what task do I do you will see when we will start creating the actual development sprints I will pretty much use the whole team seven or eight agents running at once it will happen in a second and you know I think I have like

15-16 agents total so yeah it will it will be interesting to see when all of them work and all of them contribute And that's when your cloud usage really starts running quickly. Yeah, it will. Okay, so, ooh, look at this. Remember, I just added that one single arrow here,

and all of these have been added by the agent. And what this did is that now if I start a prototype view, now we actually have a clickable prototype in Figma this is going to save a ton of

Aakash Gupta

time yes how amazing this is wow look at that and so I think the unlock here is a lot of people and they might say hey it's bad at doing x step but what you've done is you've actually connected into Figma and Figma regular

You've used that connection to have Cloud Code drive it like a user would and that I think is the unlock here.

Gabor Meyer

Yes. And now if we go into our Jira, we will see that it will start creating our Jira tickets. for the initiation of the backend. It will start adding the backend tickets here. And once we have the backend tickets, I can start creating the rest of the tickets.

Aakash Gupta

Cool. And that's our system analyst agent at work, right?

Gabor Meyer

Yes. But when we are creating all of the tickets, we will actually use the whole team.

Aakash Gupta

Okay.

Gabor Meyer

because I want usually I want the whole team to chime in and the reason is because all of the or each agent have a different role you know one is for the code maintainability the other one is making sure that our privacy is set up etc etc so

those will be important that all of them have their own perspective in the development tickets before we actually start implementing the code itself got it okay so it is now creating the epic and this is the freelance look so now this ticket is created and this is not me creating anything it is the app actually

right and now it will start just creating more and more tickets See, so when this is done, okay, all tickets are created. Okay, so let's start the development of these. Mark all of these tickets as sprint1. Use the tag because you don't have access to creation of actual sprints so use the

tags to mark all of these as sprint1 and after that you can start executing sprint1 There is a weird limitation right now for this Atlassian MCP that somehow it doesn't have the permission to create a sprint so we need a workaround. You could manually start organizing tickets into a sprint but I usually just use

tags which it has access to. Why is it important that you use sprints? Just like in any other software development project There are dependencies when you create software. and you want to make sure that some stuff gets done before you start building some

other right that's why you need springs and this is what we what we did here so now we are just initializing basically the the Firebase we will add stuff to our Firebase secret store like the cloud API and stuff so yeah that's happening right there and now

Let me start the whole team to start creating the rest of the sprints and the rest of the tickets. So now things will get a little bit faster. Now I would like the whole team to work with System Analyst Agent to start creating the tickets for the actual software development. At first only

create the frontend tickets and make sure that every frontend ticket has a screenshot attached or has an explicit Figma file linked so that our development agents will have a clear view of what needs to be developed. I particularly want that tester agent and system analyst agent would verify that

each ticket that is a frontend ticket would have a screenshot attached. I really need to be particular about the screenshots because if you don't add the screenshot the cloud code agents will just create the typical AI looking app instead instead of creating the design that you made in Figma.

So it will be the typical black and purple AI looking app instead of what you designed. And that's what we'll also evaluate so now we will have a bunch of tickets and we will just check that every one of them would have either a Figma link or a

screenshot Got it So now we will see a lot of movement in here so now you can see it says now let me launch the system analyst and the test architect agents in parallel to plan the epics and stories breakdown see and now system analyst and test architect are working together but then later the other

agents will also chime in and in the meantime on the parallel thread, the other agents like Flutter Mobile Architect, they are working on the implementation of the backend. And sometimes if you are waiting too much, you can actually create yet another terminal window, yet another terminal window, and just as much capacity you have,

you can just parallelize stuff when it's possible. But right now I don't think I can give them anything that I could do in parallel After the frontend tickets are done we will create the backend tickets then organize them into sprints do a quick review by the whole team to see that all

aspects are considered and then we will hit the big green button and start developing the sprints. Have you ever used dangerously skipped permissions? my policy is that as long as the agent is doing something within my project folder I'm chill like the worst it can do it damages my project and since I created the

project like in an hour or two worst case I can recreate when it asks me something for outside of the project folder, that's when I'm more careful what do I answer whether I allow it or not. Because once it happened that for some reason, I think we spoke about this an hour ago or so,

but it was literally asking to access my Chrome password storage. which is yeah not not necessarily delighting and for the coding agents i've seen

Aakash Gupta

you using opus i think for some of the other prompt for instance you're okay using sonnet is that kind of the split you want to use opus for coding but you're okay with sonnet for the prompt

Gabor Meyer

That was not necessarily an intentional choice. I haven't been able to observe a significant enough difference with my level of coding understanding whether one One would do a better job than the other. I'm sure that some of the developers, experienced developers and architects can see a difference.

But for me, for my purposes, I didn't really have this differentiation. So it was just more like what the app recommended and what some of my friends recommended along the way. So now we are creating the epics so now you can see that this is the first frontend

ticket being created and here you can see that here is the actual Figma link see so if I open this it opens a specific screen you can see now that when I opened, it has this specific area selected. So yeah, it's quite particular about which ticket is about what.

Aakash Gupta

I remember when you had to write all the tickets, you would tell your tech lead, okay, please file the tickets. Now all that automated.

Gabor Meyer

And there was always sort of a disagreement. Okay, who should do this step? Who should do that step? Who should define the if this, then that? Who should think about the edge cases? No, that's a system manager job. No, that's a product manager job. No, that's a developer job.

That's what I like about is that actually these help a lot.

Aakash Gupta

And one thing people who maybe tried this out in November or a little while ago, look how long running these tasks are that it's giving itself both six minute plus. It's able to work a lot longer autonomously than before. And I think that's been a huge unlock that's actually allowed things like your

seven agent dev team to be possible.

Gabor Meyer

yeah definitely and it works longer and it works quite reliable in these cases unlike for example a couple of other things in the ecosystem such as a newly launched feature newly like a couple of weeks ago I think it was launched dispatch dispatch for example I don't see it to be that reliable it

very often breaks and has hiccups and it does not provide always the exact same quality output that it provided at a previous run which I'm sure it will have a better quality in a few weeks or few months because these are all always quite rapidly evolving so you don't have a hot

Aakash Gupta

take on this batch in there do you?

Gabor Meyer

I like the idea of dispatch I think we all think where dispatch came from or the idea of dispatch came from with OpenClaw but right now I use it mindfully so I know that it is good but I also I'm very aware that I need to supervise it in order to make sure that it runs properly and

I'm aware that oftentimes I will need to tell it to hey you missed this bit you missed that bit which is a bit annoying because it would be lovely if it would be just reliable and it will in my judgment it will have a chance to replace some of

the software needs of people because you can just tell in regular human language what you want and it will do it

Aakash Gupta

For somebody who's trying to run their own dev team, what is the role of ClaudeCode, OpenClaw, Cowork, Dispatch? How would you put it all together?

Gabor Meyer

So OpenClaw, I did not experiment much with. The reason is quite profound. I was not brave enough to put it on my main computer, and I decided to order a separate computer. And when I placed the order, I knew that I needed one with a larger RAM. It was on a backorder, so I needed to wait,

and by the time it arrived, Cloud launched dispatch. So I didn't get into the craziness of OpenClo yet. For the other pieces I think so far really the biggest unlock is the MCPs so as you could see in this setup I'm essentially replicating the whole flow of how a regular

software development team would work I just apply the principles and the steps to the agents and I try to do as many things with the agents as possible

Aakash Gupta

So what I'm hearing is Claude code is your tool of choice. You wouldn't say co-worker dispatch is really replacing much. Yeah.

Gabor Meyer

From the cloud ecosystem, cloud code is the most powerful. I would not necessarily go as far as, yeah, cloud is my ultimate tool of choice for everything. But in this particular use case, as you can see, it is one very viable possibility that I think people should be

aware of because it's it's a lot of fun what do you think about cloud code versus codex so codex I did not experiment as deeply with as with cloud code so I only like tried a very minimal amount and Somehow the convenience of using cloud code was just better for me and Codex I

didn't go further into it. It's the same feeling when I tried Bolt once and then I tried Lovable once and the first few steps felt easier on Lovable so I defaulted to Lovable after all and this was pretty much the same here that

on cloud, it just felt more capable and easier to work with in the first place. So I don't have a particularly strong opinion on the capabilities of codecs. I'm sure that there are a lot of fans of codecs and also other tools that people use very successfully.

Okay, so it seems like both of these are done, so let me start the back-end tickets as well. Okay, now please get the whole team to look into the back-end tickets. Again, get System Analyst Agent to lead the discussion, but heavily involve now all the rest of the

CTO agent specifically for the architecture but also we want to make sure that our code quality and maintainability is high so the spaghetti agent I also want to pay special attention when creating the back-end tickets So now backend tickets will be created and then when the backend tickets are also

created I will just ask the whole team to do a quick review of all the tickets and organize it into sprints and then we will start developing the sprints It will be fairly quick because we only have a couple of screens so it's not an awfully huge app and

At the end of the sprints hopefully we will be able to see a working application first in the simulator and then we will send it to TestFlight and if we have time at the end I might even add you to TestFlight as a user and you can download the

app on your phone and try it for yourself Sweet I didn't even ask are you an iPhone user or are you an Android iPhone yes since

Aakash Gupta

iPhone 1 that hurts my heart for obvious reasons but I understand I also have an

Gabor Meyer

iPhone alright so now we are creating all the backend tickets as well while our setup on firebase is finishing now the sixth out I think it was six or seven tickets maybe six the last ones are in flight by this group of agents and

these ones are creating the tickets so we are almost done now it will soon ask me to put the API keys in that is a very important part that we will need to put those into the firebase secret store because you don't want your secret keys for your API to be

exposed but you will see when I add them how does it look when you are adding it to the secret store

Aakash Gupta

And basically you don't want that because if somebody gets your key, they can charge API usage to you and you'll pay for it.

Gabor Meyer

Oh, so you can always put a backstop on the spending. So there needs to be like a multi-layer protection. But, you know, if you were stupid enough not to put a limit to how much charge you can entail and you exposed accidentally your key, then yeah, there can be trouble. Okay,

so it seems that we are done with this one It says that we need authentication providers which we will not need because we will not use them Okay, we don't need that Okay, so I need to tell it that we will not use any login for the app so we don't need to enable Google and Apple

single sign-ons how is it called yeah single sign-on SSO yeah I'm blanking yeah how are we doing on our cloud usage I don't think it's too bad yet but let me quickly check okay it moved 10%

Aakash Gupta

okay not bad so you can have two full agents writing all your back-end front-end tickets without worrying too much and what plane are you on?

Gabor Meyer

I'm on the $200 plan okay so if we go to Jira we should be able to see all these tickets yeah let's check them oh and you can see that some of our tickets moved to done nice yeah So they got 29 tickets in their backlog I think more because under each we even

Aakash Gupta

have sub tickets in some cases and dependencies yeah right now I think we are on 35

Gabor Meyer

tickets but there will be I think a lot more because these are just the epics and now it will create the actual tickets

Aakash Gupta

Have you tried this workflow without creating tickets? What happened?

Gabor Meyer

Yeah so actually we could see earlier today I could have done ticket based design creation so when we were creating the design we could have started with asking system analysts to create the tickets for the designer and then asking the designer to create the Figma design we didn't do that or I didn't do that and

actually this way I think the Design turned out a little bit less high quality and less like I wanted it to be based on Figma Make and the Figma Make definition of the brand so for example these parts of the color palette and these parts of the color palette were not necessarily used

and it is primarily because I did not break it down into tickets but rather I just told the agent to take this as an input, take the whole specification as an input and create the design. This resulted in the context being so large that I assume that some compression happened and some details were lost.

I can't prove it or I can't necessarily say that this is 100% the truth but this is what I suspect that happened I'm not seeing that the app looks bad but for example I don't see not even a single orange item on there yeah it didn't use the whole

Aakash Gupta

palette yeah so that's what happens So basically you get more AI slop if you're not gonna have these agents replicate real roles. Because one might ask like, well, for AI, should we not be replicating the way we did things in the past?

Gabor Meyer

No, AI should not necessarily be fully replicating it. But at least for now, it gives a good framing of how to do things. Think about it this way. You are trusting AI to do a multi-step process. You don't necessarily watch every step of the AI, but you sort of check in at places.

So even this type of work is a very new type of interacting because i haven't created a single ticket i haven't written anything of the of the actual specification on confluence so we are using it on a on a drastically new way but it

it somewhat resonates with how we used to do stuff but it's very far from very far from it okay so let me Quickly do a review. It doesn't seem to be too large number of tickets, which is good. So let's just organize them.

Okay, now I want the whole team, every single agent to do a review of every ticket. to make sure that the ticket makes sense from their perspective. I especially want Designer Agent to check all the front-end development tickets, that there is enough information there and that they screenshot is attached to each. I want tester agent,

test architect agent to make sure that we have a decent test coverage for every ticket and we know what is is our overall test plan and regression test plan to ensure quality. And I want the code maintainability agents to watch out when we are creating the code

that we have a clear expectation on naming conventions and approach to create a maintainable, well-documented and well-commented code. And I also want Product Council to check that we are storing data appropriately. We don't send any user data to the server side storage. On the server side we are just processing information but all the storage should

always be on the device side because we are not expecting the user to create an account, we are not expecting the user to log in Therefore we only want to store user data locally and process the data on the server side when needed. Also I want to make sure that the

Database setup for the AI functionality is Firebase and Vertex database. That's where we will store the rulebook and the situation book so that we will be using our tokens wisely in the API queries. Okay, this will take a minute to transcribe. But yeah,

I wanted to make sure that I specifically call out which agent should watch out for what and also give a little bit more context. And I can't emphasize enough how important or how yeah how important I find that when I use voice to text I can give way more context

and depth to the requirements compared to if I would want to type all of this up and even if I make a mistake by describing it doesn't matter because AI will understand okay let's see what our other agents are saying Yeah, remove the Google sign-in and Apple sign-in. Simplify the authorized repo. That's good.

Now the agents are reviewing. Now get SystemAnalystAgent to create sprints using the tag functionality with an appropriate dependency mapping between the tickets in the backlog. okay so as we can see now all the tickets are created and all the dependencies are mapped so let me just very quickly prompt the whole set of sprints to be started

and developed Alright Claude let's start building go for sprint 1 once you are done with it sprint 2 then sprint 3 and so on and so on so let's start building and if you have any question in the meantime about any step

please make sure you ask and hopefully by the end of all the sprints are done we will have a build that will run in a local simulator and from there we just need to export and upload to the app store wow all right so how are agents doing Okay,

so the build has gone through and I found a small inaccuracy or a couple of small inaccuracies mainly around how our AI is identifying the actual topics that are being asked so I had to prompt them to improve the quality of how the AI identifies the right content from the knowledge base but now

I think it should be decent the good news is that we've got our build so let me just restart the build and we will see it right here what happens but

Aakash Gupta

this is already a working build wow that's exciting yeah so the coding was the short part if I reflect on this like once you had it create the tickets just a couple prompts front and back end now we got a working out

Gabor Meyer

yeah it is actually because the definition is really the investment into creating the good backbone of the whole project and the whole application and once that's done then the coding goes quite fast And that's what holds back most product managers. It is just simply, oh, I don't know where to start, how to set up my system.

But at the end, once you set it up, it gets actually quite quick and interesting. So let's restart the app. This window restarted a new build, but we actually just need to restart the app. Restart the app in the simulator with the existing build so now it will restart the

app and then we will need to push it to test right awesome that's really exciting I

Aakash Gupta

like how we did all this work and now we're really seeing the fruits of our labor and somebody who who previously was scared of coding, all of a sudden they're literally building an app on the phone.

Gabor Meyer

Yeah, exactly. And now you just have almost no limit on what you are able to do.

Aakash Gupta

And for you personally, what's like the, when do you squeeze this in? Are you staying up late? Because being a Google PM isn't known to be an easy job.

Gabor Meyer

Yeah, so in general it is something that I can easily do until like 4 a.m. in the morning on the weekends and I need to actively force myself to go sleep during the weekdays because otherwise I would just not wake up but also it helps when I know that you know next morning

let's say I'm usually a morning person and I usually go to the gym session in the weekdays in the morning and I know that if I don't go to sleep I won't be able to wake up for the gym so yeah that's a good motivator as well because we sit enough

all day alright unlike our agents who are not sitting around at all

Aakash Gupta

Is there a way you're keeping them working like 24-7 like overnight or something?

Gabor Meyer

I haven't been able to keep them running that long but I have been able to keep them running for kind of decently long enough over let's say half an hour, one hour that can easily happen So that's not a problem.

Aakash Gupta

So for people who don't know what's going on, basically Claude has used Apple's SDK in order to pull up this app called Simulator. And so Simulator pulls an iPhone up on your computer and you can touch and click it like an iPhone. So that's what we're doing now.

Gabor Meyer

Yes. I don't know if you realized the splash screen. That was a small Easter egg there. I'm blind. I'm deaf. I want to be a ref. This is one of the fun things that I've heard from the spectators on the from the audience when I was a referee. So yeah, here is our app.

So welcome to our AI consultant for ice hockey rules. So let's start with a simple one. Here are a few chips which the app provided. So what's a tripping? This is sent to the AI and the AI at this time is using all the knowledge bases in the background to understand our requests.

I actually added an observer mode so so if you turn that on you can see in a little bit more detail what is happening so it searched the rulebook it found four hits it searched the secondary resource the situation book which is the other official IIHF documentation for referees and then

it didn't even go forward to the web because these five hits were enough to find out And we can see how many tokens we used and what was the output and what was the latency. But we don't need the observer mode. but we just need the actual explanation so this is what tripping is in ice hockey

and if you want to know the details here is the actual wording from the book from the rulebook and if you don't believe then you can even look up the PDF and it brings up exactly there here is tripping rule number 57

Aakash Gupta

I think that's actually the killer feature right there being able to go through a

Gabor Meyer

book for you exactly and not just the rulebook but actually it goes through the situation book as well which usually is the extended version of the rulebook with examples so let's see another one what's hooking so now it will do the same it explains

Aakash Gupta

So you created an AI-powered app, not just any app, guys.

Gabor Meyer

Yes. So I created an AI-powered app which has two knowledge bases in the background.

Aakash Gupta

And we didn't even go into all the details of, hey, is this a graph rag? Is this a vector rag? Cloud Code took all of that for you.

Gabor Meyer

I was actually I did define because I said that it should be a vector and or maybe I didn't say that it should be a vector but when I defined that it should be a vertex database that implies that vertex is a vector database so it did imply that

Aakash Gupta

it it would be embeddings oh there we go so there is some level of specification

Gabor Meyer

yes Alright, anyways, let's push it to test flight because that was our promise at the beginning of the session that in one session we get to the test flight so push the build to test

Aakash Gupta

flight

Gabor Meyer

What happens at this time is I had to set up test flight before but if you look at my test flight which should be somewhere here yeah so I set it up but currently I have no builds so I will just get the very first build now uploaded

into Testrite so what I had to do is just fill in the basic details If I want to go further from TestFlight and I want to actually launch the app, then I would need to add screenshots as well as I would need to create To create the support URL, I would need to create the privacy URL.

Fun fact, these privacy and other URLs are easily created also by Cloud Code and you can host it on Firebase as well. Therefore, you just give the prompt, create my privacy page, you redirect the URL and it's done. But for now what matters for us is uploading the build Okay so the production build

is still running which is good Yeah so now it is just a little bit of a waiting game while it gets to test flight and then we can see it being deployed on the phone So that concludes basically the whole project project let me quickly just go through what exactly we did so we started basically

from cloud where we defined specified our application then it created the specification in confluence After having the specification in Confluence we went into FigmaMake where we prompted FigmaMake to create our design package like design briefing for the app After that we went into the actual Figma to create the screens

Once we had the screens we went back to cloud code and asked the agents to create our development tickets probably if I refresh this page now I will have a lot more yeah 51 tickets are now in in done stage and a couple of them couple of bugs are open in the backlog for

tickets all the rest basically are done from the backlog element and then we pushed the code to a simulator and from the simulator when we saw that okay it is doing what it needs to do then we are now uploading it to TestFlight and from TestFlight is just one step

uploading some screenshots and descriptions and submitting it for Apple's review

Aakash Gupta

pretty cool I had Gemini try to create a little summary of what we did here so it got one thing wrong but it got the rest of it right we had the system analyst we actually he Gabor used Claude to create that prompt not Confluence and then the

design pipeline to Figma make and Figma the development ticketing the Flutter front-end development the QA and review and now we're in deployment yeah that sounds good yeah notebook LM is pretty awesome

Gabor Meyer

yeah i love i love notebook elem it's one of my favorite harnesses i think cloud code is like my favorite but notebook elem is like second yeah it really helps when you want to understand complex complex problems or complex ecosystems or complex topics you just throw in everything that you know about it and then it will um

makes sense of it for you.

Aakash Gupta

So let's talk about that COVID unemployment. You actually in a LinkedIn post said you were delivering food on Deliveroo. So you went from delivering food on Deliveroo to product manager at Google. You have to tell us the inside story of how you cracked Google.

Gabor Meyer

Right so there was one step in between but let me give you the full story so late 2019 I changed job and I started with a new company just at the beginning of 2020 and Covid hit around April 2020 and the company where I worked was hit by COVID and I found myself being relatively new

living in London but coming from Hungary where I lived for 30 years in my life so my savings were decent on a Hungarian level but when you move to London that's another step change and the biggest problem was that during those days UK being an island and you not

being allowed to fly out on a commercial flight because it's a lockdown and France saying that nope we are not allowing anybody to cross the British Channel there were no routes out of the UK this means that I had to stay in London and yeah my other unfortunate situation was that given that I changed job and I

worked for a small startup the startup asked me to be a self-employed instead of a proper employee so when COVID hit everybody who got laid off who used to be an employee got government help but I since I was a self-employed and I only had like two months three months under my belt as a self-employed they

required a full year in order to get some money from the government I got nothing so my Hungarian savings were flying out of the window with the London rent prices and back then I didn't really have any fancy fang company on my resume and there

were literally almost no jobs to interview for and I found myself that okay So now is the time when you need to do what you need to do. You need to put some, you know, food on the table. So I took the one job that at that time was available for me.

We were only allowed to work as new riders at the peakest peak times, like Friday afternoon and Saturday afternoon. It is not an easy job. It is not an easy job. I have to tell you that it was a humbling experience. So yeah, it wasn't easy.

it was it was a humbling time but now it's a good memory and it's a good story so

Aakash Gupta

how did you crack google what was the process for you like how did i crack google

Gabor Meyer

um so after after the unemployment i got a job in between um which was kind of a fixed term contract uh backstop job i was really fortunate to to land that with which allowed me to kind of get back on my feet and I managed to find someone

online who was offering some help for candidates who were preparing for FAANG interviews and I didn't have the money to pay them but I knew that I had to get some help because previously I went into feng interviews but I

always failed at the last step I went into the loop but I didn't get the job so I knew that something was broken and I knew that I needed help therefore I put down the deposit from almost my last money and I said I will collect the rest of the money

and I will come back in a few months and then we will work together and that's what I did I saved up some money and I actually made a deal I said you are too expensive for me I pay you half the money if I don't get in but I pay twice the money if I

get in and the coach said game on and guess what he got twice the money nice

Aakash Gupta

so you actually invested in cracking it you worked really hard obviously if you're investing money you probably put in tens hundreds of hours practicing on top of that so you didn't treat these interviews lightly

Gabor Meyer

No, I absolutely didn't. So I think I prepared overall for the interviews about 200 hours. My pace for those weeks were that I typically had four mock interviews per week. and I had one coaching session per week. That's how I operated.

And the best part was when you do so many mock interviews, you start to find other people who are also similarly good because you just go through so many people in the practice that you will find okay this this person was really good in the practice

so i found three other people it was a group of four of us and out of the four of us three of us made it into google one in the united states one in um one actually two in the US and I myself in Switzerland but we didn't know each

other before like we had zero connection to each other we just found each other online and we started to practice together do you remember where was it exponent Louis Lin how'd you find them I think it was at that time they had on I got an offer.com a special group

where you could only get to practice if you had an active FANG interview process on so you had to send to Exponent your recruiter email in order to be allowed into that practice community that was their quality bar very cool yeah

Aakash Gupta

Everybody wants to become an AIPM that I talk to. They're all saying, hey, it gets 30% pay bomb, but there's more AIPM jobs. It's 30% of open PM jobs as well. Should people be getting AIPM certificates to get an AIPM job?

Gabor Meyer

That's an interesting one and I actually have a similar answer to it what I always had about the Scrum Certificate or Agile Certificate The certificate itself is not the thing that you need the knowledge is what you need I don't think anybody should pay for a certificate for the certificate's sake

pay for a course for the knowledge not for the certificate and that's where people go wrong because oftentimes these courses are fully automated you pay the money you get in there there are those sessions whether or not you attended the sessions whether or not you learned anything at the end it automatically generates you a pdf

But the PDF will worth very little when you actually need to do something about AI. So the best courses are the ones where you need to have hands-on building The absolute best places to do some learning is where you not just build something but you build something that you can later on share.

and there is actually a contradiction that couple of years ago I had a very strong opinion that product managers would not need a portfolio and I'm actually lately refining this opinion and I believe that if you can demonstrate that you build something now it is valuable because the product management practice and the

product management profession is quite split right now Every company wants to do AI, but the reality of product managers within companies is that if you are one of the few lucky ones within a company that works in an area where building AI makes sense and your leadership wants to invest into AI, you will gain AI experience.

But the majority of the PMs in their everyday job may not touch any AI product for the next year or two just because it doesn't trickle down that fast to every place in every company. And for those PMs who don't have the chance to work on AI initiatives within their job,

All they are left with is trying to make themselves more productive with ChatGPT Which is not going to cut it In two years the gap will be so big between those who build and those who are just productivity AI users That it will be very hard to catch up That's why I recommend everybody to start building,

if not within your work than outside of your work. Not because you want to build a business out of it, just because you want to experience it and you want to demonstrate that you are able to build.

Aakash Gupta

And what are the tools that PM should be investing their time in? Today we obviously really triple clicked on Cloud Code. What is your take on Cloud Cowork and Cloud Dispatch?

Gabor Meyer

Cowork and Dispatch are still I feel that they are a little bit premature and somewhat moderately reliable. They are interesting because you can achieve more with them and you can let the AI do more without you and they can handle through a browser extension they can operate your browser they can do much

more than just the chat itself but right now I find that they are quite fragile and not necessarily reliable but they are getting better by the day

Aakash Gupta

Man, two weeks ago you thought they were shit, but it sounds like you've changed your tune on that.

Gabor Meyer

Don't tell anyone. Yeah, two weeks ago we had a conversation. oh so how do you find this batch oh it's absolutely shit it was it was but now it's now it's just fragile so I think another couple of weeks go by and by the time this

video is published it will be probably reasonable and then another few weeks and it will be oh my god this is the best thing ever so you mentioned a PM portfolio and I

Aakash Gupta

actually want to triple click on that How do you create a PM portfolio that really helps you crack into the top tier of jobs and fame companies?

Gabor Meyer

I'm not sure if I have the right answer for it, but I do have an approach for it. So as you could see in the app that we built today, I added an observation mode. And the reason why I added that because if I would ever want to show this app to anyone

I would turn on that observation mode and I could walk through the listener what I built in the background how those things are working what are the knowledge bases I can tell an interesting story about the calibration of the scoring. When I was putting together,

when I found actually a bug in the app where it didn't identify the correct section of the rulebook, I started to troubleshoot why and I found a fascinating story about it and I actually documented it here. so there was a problem in there where the scoring which is a multi-component

scoring that identifies whether the rulebook part is relevant for the query or not did not understand the difference between panel t's and panel t or Boarding and Board. So I had to add this and also some of the thresholds were just too strict.

So when I would say this story and I would explain how did this impact the actual user experience, this would be a really good not portfolio, but like a demonstration story. So while I cannot necessarily advise you on how a really good portfolio look like,

I would say that if you have a couple of stories like this about how you built and fine tuned AI, that is definitely a useful story to tell.

Aakash Gupta

Awesome.

Gabor Meyer

All right this is what we've been waiting for so let's now distribute the app and we can put it into test flight so now it's gonna prepare the upload it's gonna do the signing and then uploading so in probably like three to five minutes we will have our first test flight build in the

App Store Connect Test Flight section. Alright so it seems that we finally managed to upload our app to the test flight.

Aakash Gupta

Let's refresh.

Gabor Meyer

Yes there is the build. So now we just need to wait while Apple processes it. This usually takes a couple of minutes and once the processing is done we can invite our internal testers to start testing the application on their devices and they will be able to download it anywhere in

the world as long as they are invited as testers and after that you can just launch

Aakash Gupta

the product wow so now we actually have the app in TestFlight

Gabor Meyer

yeah it took us a while but it is there and again from here it's only the question of uploading all those screenshots and filling in the different distribution details and phone numbers and descriptions and keywords and in a couple of days you will be in the actual App Store the one thing I would warn everybody that given

that the barrier to entry for building apps is now lower than ever, suddenly the App Store reviews, especially for the very first submission, they are just stretching over many days. Like I expected, based on Apple's documentation, that it would take one or maximum two days, but it took more than a week to get the first review done.

So just brace yourself for that.

Aakash Gupta

That sounds exactly like how it was when I was building apps back in 2012. So good luck, guys. God, today's class has been just that a masterclass, I think, in how the PM can potentially put on that founder hat, start to make themselves become a product builder, start to embrace the new way of product management.

And like you said, the gap between you and the other PM in two years, it's going to be huge. So make sure to use the time to do a similar activity to what we've shown in today's episode. If people want to get started, where should they go?

Gabor Meyer

If people want to get started, the best place to start, if you just want to do it for yourself, pull up your favorite AI, ChatGPT Gemini Cloud Code, and start asking questions how to do things. If you have time, this is the cheapest way to get started.

If you want to accelerate your journey and you want some structured information to start building and kind of If you shortcut your way from idea to build to actually doing it, then you should ask for some help. I, amongst many others, can help you. If you want to check out how I help folks building their own apps,

just go on Maven and you can find my AI Builder course there.

Aakash Gupta

So check out his Maven course and I think he's a great follow on LinkedIn as well. Gabor, thanks for being so generous with your time. I know preparing this episode itself probably took 10 plus hours. Then doing it, really appreciate you.

Gabor Meyer

Thank you so much. Bye everyone.

Aakash Gupta

I hope you enjoyed that episode. If you could take a moment to double check that you have followed on Apple and Spotify podcasts, subscribed on YouTube, left a rating or review on Apple or Spotify and commented on YouTube, all these things will help the algorithm distribute the show to more and more

Finally, do check out my bundle at bundle.akashg.com to get access to nine I'll see you in the next episode.
## Related content

**Podcasts:**

1. [My Claude Code PM OS with Dave Killeen](https://www.news.aakashg.com/p/dave-killeen-podcast)
2. [Claude Code OS Layer with Carl Vellotti](https://www.news.aakashg.com/p/carl-vellotti-3)
3. [How to Design like OpenAI and Figma with Ed Bayes and Gui Seiz](https://www.news.aakashg.com/p/ed-bayes-gui-seiz-podcast)

**Newsletters:**

1. [The complete guide to Claude Code](https://www.news.aakashg.com/p/how-to-use-claude-code-like-a-pro)
2. [AI agents for PMs](https://www.news.aakashg.com/p/ai-agents-pms)
3. [How to build AI products](https://www.news.aakashg.com/p/how-to-build-ai-products)

---

*PS. Please subscribe on [YouTube](https://youtu.be/LR_WOmcE9WI) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/claude-code-dev-team) on 2026-05-23T14:47:58-04:00*
