---
title: "How PMs Ship 100K Lines of Code at OpenAI with Ryan Lopopolo, Member of Technical Staff"
source: "https://www.news.aakashg.com/p/ryan-lapopolo-podcast"
author:
  - "[[Aakash Gupta]]"
published: 2026-05-25
created: 2026-05-30
description: "Ryan Lapopolo from OpenAI’s Frontier team on why code is a liability, the three-phase harness, and how to hit a billion tokens a day."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management, claude-mastery]
ai-context: "Aakash Gupta interviews OpenAI Frontier's Ryan Lopopolo on how PMs operate inside a frontier AI lab: why code is a liability, the three-phase harness for shipping ~100K lines, and how to hit a billion tokens a day."
---
The roadmap for how PMs operate inside a frontier AI company

![](https://www.youtube.com/watch?v=8suwvrF0Lv0)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/product-growth-podcast/id1763555775), [Spotify](https://open.spotify.com/show/7vVEMqCSKb7I7xPk8xZtg5), and [YouTube](https://youtu.be/8suwvrF0Lv0).*

Brought to you by:

1. [Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7) - Get $550 off their AI PM Cerficiate with code AAKASH550C7
2. [Bolt](https://bolt.new/solutions/product-manager?utm_source=Promoted&utm_medium=email&utm_campaign=aakash-product-growth) - Ship AI-powered products 10x faster
3. [Customer.io](http://customer.io/productgrowth) - Send smarter messages using your product data
4. [Ariso](https://ariso.ai/aakash) - Ship AI agents and features faster, with fewer regressions
5. [Pendo](http://www.pendo.io/aakash) - The #1 software experience management platform

---

## Today’s episode

Most companies are still debating whether [PMs should ship code](https://www.news.aakashg.com/p/pm-guide-ship-production). OpenAI is debating the best ways for PMs to ship code. They’re living in the future.

The builder behind a lot of that harness engineering is Ryan Lopopolo. He [wrote the OpenAI post on harness engineering](https://openai.com/index/harness-engineering/) and runs a frontier team where PMs, designers, and engineers all ship using the same system.

The wild part for me? His PMs shipped around 100K lines of production code.

Did they open the IDE? Hell no! [Their coding](https://www.news.aakashg.com/p/pm-guide-ship-production) happened through [PRDs](https://www.news.aakashg.com/p/ai-prd), [tests](https://www.news.aakashg.com/p/ai-pm-observability), [docs](https://www.news.aakashg.com/p/writing-better-specs-as-a-pm), and [harness rules](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e). The model did the typing.

As someone who spent a decade in PM growth roles, I’ve seen how long it takes to move a feature from [PRD](https://www.news.aakashg.com/p/product-requirements-documents-prds) in a doc to code in prod. For most companies, that latency is weeks, months, or quarters.

In Ryan’s world, it can be days, hours, even minutes. And the PM is inside the loop - not watching from Jira. *So I had to understand how that works - and that’s today’s episode:*

---

- ***If you want access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, Relay.app, Magic Patterns, Speechify, Bolt.new and Mobbin - **[become an annual subscriber](https://www.news.aakashg.com/account) ($150), and grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*
- ***If you want access to my AI PM customizations** - [PM OS](http://l.threads.com/?u=https%3A%2F%2Fwww.news.aakashg.com%2Fp%2Fpm-os&e=AT3OpE6P_HWG7KYcTl7xmfJz8h5zD8r-frJ3BkELyP3DYU58vBRyaMu95EaIbAjHMK36o_aZMzrCeGtw4SDHYwhZVyucVSaW1gqpGFsZrI6GBstPgR1InkhqtfU1niMfNeO455rFAhLe), [Job Search OS](https://www.news.aakashg.com/p/job-search-os), and [Prompt Library](https://www.news.aakashg.com/p/pm-prompt-library) - **[become a founding subscriber](https://www.news.aakashg.com/account) ($250)**.*

---

## Today’s post

Here’s the guide to shipping code like PMs at OpenAI:

1. How the harness works
2. Ryan’s Frontier team case study
3. The new job for PMs, designers, and engineers

---

## 1\. How the harness works

You don’t need to copy every detail of OpenAI’s setup.

You do need the big pieces, because that’s the system you’ll be dropped into as an AI PM. Ryan thinks of the harness as the environment inside the repo that teaches the agent how your team builds software.

![](https://substackcdn.com/image/fetch/$s_!TYca!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15264f8b-fb8f-4260-b7da-adc519c9d4ee_2160x2700.png)

### agents.md and the docs tree

Every repo has an `agents.md` file at the root. When they run [Codex](https://www.news.aakashg.com/p/codex-pm-guide) on that repo, this file is always in the model’s [context](https://www.news.aakashg.com/p/context-engineering). `agents.md` does two things. **It explains the operating loop** like read docs, plan, implement, run tests, and ask for review. Then **it points the agent at the docs tree** like markdown files with performance patterns, networking practices, user journeys, design guidelines, and past decisions.

Each run’s execution plan gets written back as implementation history. Design docs move out of slides and Slack into the repo. And tests fail if docs fall out of sync, which forces the agent to update them while editing code. The model needs a repo that it can search to show how your team works. As a PM, that’s where your decisions belong.

### Tests and lints that enlist taste

Ryan’s team encodes taste and non‑functional requirements directly into tests and lints. No *please remember I beg of you* paragraphs. A few examples:

1. The build fails if any user‑facing markdown or HTML string uses straight quotes instead of curly quotes, because their design team is finicky about typography.
2. Business logic has to belong in the right modules. Tests enforce boundaries so a ball of mud doesn’t form.
3. When docs need to move together, tests enforce that they stay in sync.

Because the model is trained to make tests pass, each failure message is an instruction. You’re not arguing taste in Slack. The suite is the style guide. In growth roles, I learned the hard way that if something matters, you have to measure it and enforce it. Their approach is the same idea, just pointed at code and docs instead of funnels.

### Review agents as virtual staff engineers

On the review side, they run a matrixed CI job that spins up specialized review agents, each with a persona doc:

1. `frontendarchitect.md`
2. `reliabilityengineer.md`
3. `appsecengineer.md`

That feedback goes back into the loop. The implementation agent uses it to fix the current change. The team updates the docs or tests so the same class of mistake doesn’t come back.

### Observability and UI control

Finally, the harness gives the model eyes on the product. The agent can spin up a local [observability](https://www.news.aakashg.com/p/ai-pm-observability) stack (metrics, logs) and use it to debug like a human. With GPT‑5.5’s computer use, it can click through the app, inspect elements, and verify flows end‑to‑end.

The rule is simple; the agent has to prove the feature works through the same paths your users take. As a PM, that’s where your acceptance criteria also need to land.

---

## 2\. Ryan’s Frontier Team Case Study

In mid‑2025, his team ran an experiment. **Could [Codex](https://www.news.aakashg.com/p/codex-pm-guide) do the entire software engineering job for a new internal agent product?**

The constraints?

1. Start from an empty repository.
2. Build an app that supports non‑engineering knowledge work inside OpenAI.
3. Let the agent handle on‑call triage, internal tools, and text‑heavy workflows.
4. No human is allowed to type production code. Engineers can only touch the harness.

![](https://substackcdn.com/image/fetch/$s_!SUnQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58878ecc-c0ac-4d19-b966-dcb66c2f8465_2330x2700.png)

By the end, the app had around 1M lines of code. It also had roughly 250K lines of markdown prompts inside the repo. And it ran as an Electron app with multiple agents coordinating summarization, repo gardening, skills distillation, and execution.

Any time the agent failed, the team asked **what was missing in the harness that led to this failure.** The codebase improved because humans improved the environment. Nobody jumped in and rewrote everything.

---

## 3\. The new job for PMs, designers, and engineers

For most of my 10+ years in product, PMs were kept away from the repo. You were the human API between customers and engineering. You wrote PRDs, argued in sprint planning, and waited. The typing was someone else’s job.

Ryan describes a different world.

In his team, code is no longer the scarce resource. With GPT‑5, the model can generate code at scale. The difficult part is validating it, safely deploying it, and making sure it solves the right user problem. That means the harness (the environment of docs, tests, lints, review rules, and [observability](https://www.news.aakashg.com/p/ai-pm-observability)) is where work gets done.

Once the harness is strong, engineers aren’t the only ones who can write code. PMs and designers easily plug into the same system.

And literally everyone gets a new job description.

![](https://substackcdn.com/image/fetch/$s_!NTl6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07c66d73-6216-4e83-8d57-435da934725d_2160x2260.png)

### The new role for PMs

In late 2025, Ryan’s team wanted to explore a ‘ [skills system](https://www.news.aakashg.com/p/10-laws-claude-skills) ‘ so the agent could learn and reuse user preferences for data analysis. In most companies, this would kick off a chain of product reviews and engineering estimates. Here is what they did instead:

1. The PM wrote a [markdown PRD](https://www.news.aakashg.com/p/ai-prd) that defined the skills library
	- How the agent should interview users about the metrics
		- How should it store and reuse that knowledge
		- How this should appear in the product surface
2. The team reviewed the PRD once in their weekly meeting.
3. By the end of the week, the feature existed in the app. The tests the PM had *vibed* into existence were passing.

The PM and engineers did not need a week of back‑and‑forth. The harness carried the intent into code. This worked because business logic was embedded in modules with high‑fidelity fakes. Also, the tests from the product side exercised the behavior.

**The important bit: the PM’s leverage came from writing artifacts that the harness understands.** If you’re a PM reading this, imagine your next feature:

1. Could you express it as [PRD](https://www.news.aakashg.com/p/ai-prd) + [tests](https://www.news.aakashg.com/p/ai-pm-observability) + [evals](https://www.news.aakashg.com/p/ai-evals-explained-simply) the agent can run on its own?
2. If you couldn’t touch the IDE at all, what would you have to write differently?

That’s the muscle you need to build.

### Designers generate painted doors with

Early on, if a designer tried to ship a feature, they had to schedule agent runs inside their internal app. Then, to demo it quickly, they had to push a backend‑style cron system into the front of the stack. Usually, the scheduler logic ended up tangled inside frontend JavaScript.

Ryan looked at it and knew they’d regret it later. So decided to revert the change. Their team came out of that with a simple norm:

1. Designers own full painted‑door flows at the front of the app: the UI, the interaction pattern, and how scheduling is exposed.
2. Behind the door, the backend can be a no‑op plus instrumentation. They measure clicks, intent, and drop‑off before committing engineering time.

The harness then decides, based on data, which doors deserve a backend. So the JD for designers is to build high‑ [taste](https://www.news.aakashg.com/p/taste-at-speed), high‑signal surfaces that the harness sees as experiments. A designer now must give the agent and engineers the best possible signal about what’s worth building.

### Coding engineers became harness engineers

Ryan’s definition of the modern engineering job is very close to how I think about great growth engineers. **Your value is the leverage you create for everyone else.**

In his team, the primary output is leverage. Every engineer is responsible for adding tests, docs, CI rules, and observability that let many concurrent agents work. Internally, they use a simple mental model. Think of it as you just hired a cluster of interns named [Codex](https://www.news.aakashg.com/p/codex-pm-guide). Your job is to manage them.

Emotionally, that’s difficult. Many engineers (including Ryan) grew up measuring their contribution in commits and lines of code. Letting the model do the typing can feel like losing the craft. But he argues that **the craft moved. The new skill now is who can build the harness that makes GPT‑5 a strong teammate for this particular product and company?**

> *“Every engineer on the planet now has hundreds or thousands of concurrent hands on keyboards, modulo token budget.”*

That’s the world your PM career is walking into. You’ll be working with engineers who measure themselves by the systems they build.

---

## Why should YOU care? Does it matter?

Most teams use AI to speed up function‑level coding but keep the rest of their software development lifecycle unchanged. Ryan’s world is what it looks like when you redesign the system around agents that can do the full job. **The differentiator is how much of your team’s judgment is embedded in your harness.**

If you’re a founder or product leader, that’s what [AI strategy](https://www.news.aakashg.com/p/ai-product-strategy-2026) now means. It’s how you design the engineering system your PMs and designers plug into, so they can ship.

If you’re a PM, this is the [future job description](https://www.news.aakashg.com/p/how-to-become-and-succeed-as-an-ai). You’ll still need [taste](https://www.news.aakashg.com/p/taste-at-speed), [discovery skills](https://www.news.aakashg.com/p/advanced-techniques-continuous-discovery), and stakeholder management. You’ll also need to think like a harness engineer: what tests, docs, and rules would I write if the model were my team?

---

## \[Bonus\] Downloadable Takeaway

I turned Ryan’s six‑month harness plan into a one‑pager you can use as a checklist with your team.

![](https://substackcdn.com/image/fetch/$s_!Exk6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a9c4162-943b-4af0-a82a-22ce26c4d2c7_2160x2260.png)

---

## Where to find Ryan Lapopolo

- [X](https://x.com/Laoplo)
- [LinkedIn](https://www.linkedin.com/in/ryanlopopolo/)
- [OpenAI](https://openai.com/)

---

POLL

### What did you think of today’s post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

## Related content

**Podcasts:**

1. [How to Run Evals in Claude Code with Aparna Dhinakaran](https://www.youtube.com/watch?v=DL-pUGcfrf4)
2. [How to Build a Full AI Dev Team in Claude Code with Gabor Mayer](https://podcasts.apple.com/in/podcast/how-to-build-a-full-ai-dev-team-in-claude-code/id1763555775?i=1000765013076)
3. [This CPO Uses Claude Code to Run His Entire Work Life with Dave Killeen](https://open.spotify.com/episode/5jytj64qyP8EEuneAlRxnv)

**Newsletters:**

1. [PM’s Guide to Claude with Pawel Huryn](https://www.news.aakashg.com/p/ai-pms-guide-to-claude)
2. [How to Become a Builder PM with Mahesh Yadav](https://www.news.aakashg.com/p/how-to-become-a-builder-pm)
3. [How to Build a Team OS in Claude Code with Hannah Stulberg](https://www.news.aakashg.com/p/team-os-cc)

---

*PS. Please subscribe on [YouTube](https://www.youtube.com/@growproduct?sub_confirmation=1) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/ryan-lapopolo-podcast) on 2026-05-30T15:09:17-04:00*
