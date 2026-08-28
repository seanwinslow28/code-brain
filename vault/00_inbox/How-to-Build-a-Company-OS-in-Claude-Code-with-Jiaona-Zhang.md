---
title: How-to-Build-a-Company-OS-in-Claude-Code-with-Jiaona-Zhang
source: https://www.news.aakashg.com/p/company-os-jz
author:
  - "[[Aakash Gupta]]"
published: 2026-06-24
created: 2026-07-15
description: Jiaona Zhang, CPO at Laurel and ex-Airbnb, Dropbox, WeWork, shows exactly how  a product team of 9 can outperform 90.
tags:
  - source/web-clip
type: source
status: unprocessed
domain:
updated: 2026-07-15
---
One AI native team of 9 can now out-ship what used to take 90 people. Here is how Laurel built that team.

![](https://www.youtube.com/watch?v=qsDX0PMKcaE)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/how-to-become-a-builder-pm-with-n8n-claude-code/id1763555775?i=1000762483697), [Spotify](https://open.spotify.com/episode/5ZNRFSYL15vRo7Rt51ANXP?si=glhi9q4SS7igfxzCWWA0bw), and [YouTube](https://youtu.be/qsDX0PMKcaE).*

**Brought to you by:**

1. [Ariso](https://ariso.ai/aakash) - Ship AI agents and features faster, with fewer regressions
2. [Bolt](https://bolt.new/solutions/product-manager?utm_source=Promoted&utm_medium=email&utm_campaign=aakash-product-growth) - Ship AI-powered products 10x faster
3. [Pendo](http://www.pendo.io/aakash) - The #1 software experience management platform
4. [Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7) - Get $550 off their #1 AI PM Certification: code AAKASH550C7
5. [Customer.io](http://customer.io/productgrowth) - Send smarter messages using your product data

---

## Today’s episode

I’ve written about building a [PM OS](https://www.news.aakashg.com/p/pm-os) and [Team OS](https://www.news.aakashg.com/p/team-os-cc) in Claude Code. They are my top two most popular pieces of 2026.

Today is the upgrade: **a company OS** that enables *even CSMs at your company to [ship to production](https://www.news.aakashg.com/p/pm-guide-ship-production)*.

And this isn’t theoretical.

[Jiaona Zhang “JZ”](https://www.linkedin.com/in/jiaona/) is the CPO at Laurel - which raised a **$ [100M Series C](https://www.laurel.ai/resources-post/ai-time-platform-laurel-raises-100-million-to-transform-the-professional-services-industry)** - and her company actually runs on a Company OS. They have run into the problems and kinks. They’ve ironed them out. Now, they’re showing what works.

JZ is not some “AI purist.” She has led product at **Airbnb, Dropbox, Webflow, and WeWork**. She’s an AI realist.

And in this episode, she doesn’t hold anything back:

- **The Company OS** that enables it all
- **How PMs go from product idea to shipped feature** with agents
- **How she conducts AI PM interviews** in this era, and how to ace them

This is one of the densest episodes I’ve ever recorded.

*I hope you enjoy watching it as much as I did recording it.*

---

- ***To get access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, Relay.app, Magic Patterns, Speechify, Bolt.new and Mobbin - **[become an annual subscriber](https://www.news.aakashg.com/account) ($150), and grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*
- ***To get access to my AI PM customizations** - [PM OS](http://l.threads.com/?u=https%3A%2F%2Fwww.news.aakashg.com%2Fp%2Fpm-os&e=AT3OpE6P_HWG7KYcTl7xmfJz8h5zD8r-frJ3BkELyP3DYU58vBRyaMu95EaIbAjHMK36o_aZMzrCeGtw4SDHYwhZVyucVSaW1gqpGFsZrI6GBstPgR1InkhqtfU1niMfNeO455rFAhLe), [Job Search OS](https://www.news.aakashg.com/p/job-search-os), and [Prompt Library](https://www.news.aakashg.com/p/pm-prompt-library) - **[become a founding subscriber](https://www.news.aakashg.com/account) ($250)**.*

---

## Newsletter Deep Dive

*Welcome to the web’s first guide for how product leaders can create a Company OS to accelerate Claude Code adoption across their org:*

1. **How to build your Company OS**
	- How to spread AI adoption beyond engineering
2. **The new role of the PM in an AI-native team**
3. **How to get hired as an AI-native PM**

---

## 1\. How to build your Company OS

A company OS can unlock productivity across your organization. It takes the power of a concept like a [PM OS](https://www.news.aakashg.com/p/pm-os) beyond single PMs or [product teams](https://www.news.aakashg.com/p/team-os-cc).

At Laurel, **even CSMs are shipping to production**.

*Here’s how to build your own:*

![](https://substackcdn.com/image/fetch/$s_!PpJ9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fe0aa47-7bed-4cb3-93c5-e4f3c646bc07_2160x2700.png)

#### The architecture is simpler than you think

One GitHub repo. Every team in the company has a folder. Every folder maps to the activities that team does. Every activity has a skill file. The skill files go directly into Claude’s organization settings. Anyone who opens Claude already has the right skill loaded.

During the demo, JZ screenshared Laurel’s full GitHub structure live. Customer success, data science, design, engineering, finance, legal, marketing, all of it:

![](https://substackcdn.com/image/fetch/$s_!DuDj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f5e748b-05dd-49f9-92eb-db754b383e0e_2470x1302.png)

The original Company OS followed by JZ at Laurel

*There are three layers to build your own.*

#### Layer 1 - Start with ontology

PMs build the OS and then wonder why nobody uses it. They got the order wrong.

Start with the ontology like JZ. Map every function’s work to categories, then to tasks within each category. What should sales be doing? What should CS be doing? What should product be doing? This work map is what informs the folder structure. The OS is built from the ontology:

![](https://substackcdn.com/image/fetch/$s_!7u0N!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe2521ba-f521-436f-a550-1b52f44ce05c_2466x1234.png)

What a company ontology looks like

At Laurel, the ontology sits alongside the OS. For each function, it shows which activities should go up (more human time) and which should go down (automated away). For product, competitive analysis write-ups, stakeholder briefs, and research synthesis are in the “stop doing manually” column. Feature work, QA, and direct customer contact are in the “spend more time here” column. Color-coded. Visible to every leader.

*This is the part most companies skip. They install tools before deciding what work actually matters.*

#### Layer 2 - The skill file architecture

Once you have the ontology, build the skills.

A skill file is a Markdown document that encodes how to do a specific piece of work. Not just a generic prompt. A specific, opinionated guide that reflects how your company does that thing. How do you write a renewal email at your company? What does a good feature request look like when it comes from a CS rep? What questions do you ask before triaging a support escalation?

The skill file answers all of this. Upload it to Claude’s organization settings and it becomes available to everyone. The skill is called when needed. With this simple set up now one person’s best workflow becomes everyone’s default.

#### Layer 3 - The delivery layer

At Laurel, every customer facing team member gets a daily morning message in Slack. Calendar, meetings, check-ins, onboarding sessions, all surfaced. And embedded alongside each item, the skill to use. You have a renewal call at 10am. Here is the renewal skill. You have an onboarding session at 2pm. Here is the onboarding skill. The OS meets people where they already are.

![](https://substackcdn.com/image/fetch/$s_!dwaR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c54c706-236a-46cf-80e3-6c1c344fead3_2534x1644.png)

*The 1% will always figure it out. The Company OS is how you make their workflow everyone’s default.*

---

### How to spread AI adoption beyond engineering

When AI adoption is everyone’s responsibility, it is no one’s responsibility. The person who was going to build the CS workflow is also running renewals, handling escalations, and onboarding three new accounts. The workflow never gets built. Leads to a huge gap.

The fix ↓

#### Step 1 - Dedicate a person to it

At Laurel, this role is called AI Operations. One person, full-time mandate, whose entire job is finding efficiencies, building workflows, and spreading what works to every function.

JZ describes it as the new BizOps:

> ***AI ops** **is the new BizOps**. Before, BizOps were doing really meaningful things, but often it was very high level, all the different hats, a lot of like market level stuff. Now, if you repurpose this idea of having BizOps, which is really again a Swiss Army knife in many ways, to finding people who are insanely curious, tinkering with the latest technology, and relentless about finding efficiencies, **that’s the DNA I really look for**.*

Laurel started with one person, Sasha. Within months, every other function wanted their own Sasha. That demand is how you get budget. You demonstrate value with one person, then let the pull happen naturally.

If you are reading this as a leader who cannot yet hire for this role, the person closest to it already exists on your team. They are the one who figured out the Slack automation nobody asked them to build. Find them. Give them the mandate officially.

#### Step 2 - Run a companywide hackathon

The assumption that blocks AI adoption in non-technical functions is simple: you have to be technical to build something.

One hackathon breaks that assumption faster than any training program.

Laurel ran a companywide hackathon at their offsite roughly three months ago. Every team participated. Not just engineering. The explicit goal was to show that anyone can build. When a Customer Success manager ships something in a day, the story spreads. That story does more for adoption than any top down mandate.

If a full offsite feels out of reach, a single afternoon works too. Pick one function. Give them four hours and a clear problem to solve. Keep a low bar, make it like even a working Slack automation counts. A prompt template that saves 30 minutes a day counts. The goal is the first win over the perfect solution.

#### Step 3 - Make the culture visible

Some companies have a value on a slide that nobody reads after the presentation is done.

Laurel turned their “unreasonable hospitality” value into a workflow. When a Customer Success manager has a check-in coming up and has not had an in-person touch with that customer in a while, the OS surfaces it. Pulls from Gong transcripts what the customer loves. Suggests the gesture. Handles the logistics. If you can see, now the value is not just a slide anymore.

That is the part most leaders miss. Culture spreads through systems that make the right behavior the default behavior. You do not need everyone to be intrinsically motivated to show hospitality. You need a system that makes it easy enough that everyone does it anyway.

*The same logic applies to AI adoption. Waiting for 99% of your company to become curious about AI on their own is a losing bet. Put the right skill in front of them at the right moment and curiosity takes care of itself.*

---

## 2\. The new role of the PM in an AI-native team

There is a version of this conversation happening on Reddit right now. A PM asking if their job is going away. Getting 200 replies, half of them panicked and other dismissive. Tbh, neither group is right.

The job is not going away. The shape of it is changing faster than most people want to admit.

Here is what the new shape actually looks like.

![](https://substackcdn.com/image/fetch/$s_!7bK9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb90546b-5dd5-45e8-b288-1a029a3a1567_2160x2700.png)

#### The captain model

Forget the old handoff chain. PM writes spec, sends to designer, designer sends to engineer, engineer sends back, designer says that is not what they designed. That loop is going down in AI-native teams.

The replacement is a captain model. Every feature has one person who owns it end-to-end.

The captain is whoever has the most important skill for that feature’s hardest problem:

- **Engineering captain -** Architectural changes, system overhauls, anything where the codebase risk is the biggest variable.
- **Design captain -** Interaction heavy features where the experience is everything and the engineering is straightforward.
- **PM captain -** Features where customer understanding plus business context is the hardest thing to get right. Empty states. Onboarding flows. Anything where the content and the user insight matter more than the code.

That’s the full model.

#### Two track product reviews

Speed without alignment is just running in circles. The captain model needs guardrails.

At Laurel, there are two tracks:

**Track 1 - Fast.**

Small features, single captain, end-to-end ownership. Goes through the Ask Devin reviewers Slack channel. An engineer reviews the PR. A designer checks if needed. No formal product review meeting.

**Track 2 - Full review.**

Radical changes to core user interactions, architectural decisions, system level thinking required. This is what JZ calls a product strategy review. “Are we sure this is the right direction for the whole product?” Plus a separate architectural review - “Will the system actually support where we want to go?”

The question most teams get wrong is which track a feature belongs on.

The test is simple. If the change affects a core user interaction that touches the whole product, it is Track 2. If it is scoped to one workflow and the hardest problem is execution, it is Track 1. Temporary initiatives, despite being a frontend and backend feature, was Track 1. A redesign of how Laurel surfaces time across the entire day would be Track 2.

I covered the mechanics of PMs shipping to production in my [PM guide to shipping your first pull request](https://www.news.aakashg.com/p/pm-guide-ship-production). The captain model is what makes that shipping sustainable at scale rather than a one-off experiment.

As an ending note, I would say…

*The fundamentals of great product management never changed. What changed is that you can no longer hide behind process, meetings, and headcount.*

*The work is the work now.*

---

## 3\. How to Get Hired as an AI-Native PM

Ask someone on your team if they use AI. Everyone says yes. Ask them to show you. That is where the answer changes.

There is a framework that cuts through the noise immediately. Four levels. Every person, every team, every company sits somewhere on this scale.

![](https://substackcdn.com/image/fetch/$s_!F-Si!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62aa4187-c0a7-444b-9eb1-54e65c4343d8_2160x2700.png)

#### Level 1 - Chat mode.

You open Claude or ChatGPT. You type a question to get a specific answer.

This is AI as a slightly smarter Google. Most people are here. If you are closing the tab after every session and starting fresh next time, you are Level 1.

#### Level 2 - Workflow automation.

You stop doing a task manually and build something to do it for you.

A Slack automation that triages feature requests. A template that auto-populates from your CRM. A morning briefing that pulls your calendar and surfaces priorities. One workflow. That is the entry point. If you’re not familiar, I covered how to start building these in my [AI Agents for PMs guide](https://www.news.aakashg.com/p/ai-agents-pms).

#### Level 3 - Building apps.

You identify something tedious enough to deserve a real tool, and you build an app.

Something with a UI, logic, and state. This is where builder PMs live. Mahesh Yadav broke down exactly how to get here in [our episode on becoming a builder PM](https://www.news.aakashg.com/p/how-to-become-a-builder-pm).

#### Level 4 - Shared apps and shipping to customers.

You are building things other people use. Your Customer Success team ships a feature. Your PM submits a PR that goes to production. You are in the full product lifecycle. This is where AI-native teams operate.

In most organizations, the engineering team is split between Level 2 and Level 3. Sales and Customer Success are mostly Level 1. Finance and legal are often at Level 0, which is not even on the scale.

#### The screen-share test

Here is how JZ uses this framework in practice. In every interview, she asks the candidate to screen share.

Within 60 seconds you know exactly where someone is. A Level 1 person has a bunch of Claude chat tabs open with one-off questions. A Level 3 person has a folder structure, a set of saved workflows, maybe an app they built last week.

*The same test works for your team. Pick five people across functions. Ask them to show you how they use AI. Do not ask them to describe it. Watch it happen. You will have a clear map of where your company actually sits in under an hour.*

---

*Here’s the most important takeaways in 1 infographic:*

![](https://substackcdn.com/image/fetch/$s_!N09v!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F211898e5-a78c-45b3-a368-faab4c26ce64_2160x2700.png)

---

## Where to find Jiaona Zhang

- [LinkedIn](https://www.linkedin.com/in/jiaona/)
- [Reforge](https://www.reforge.com/profiles/jiaona-zhang)
- [Laurel](https://www.laurel.ai/)

---

POLL

### What did you think of today’s post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

## Related content

**Podcasts:**

1. [How a VP Uses Claude Without Producing Slop](https://www.news.aakashg.com/p/claude-vp) - [YouTube](https://youtu.be/yDeFGKaSoX8?si=Ys51buJ4L6LK7b4h) | [Spotify](https://open.spotify.com/episode/03YzqmgOWNSekE6ERaqy75?si=3_w5eMzrQGOlJQLeaakNYw) | [Apple](https://podcasts.apple.com/in/podcast/how-a-vp-of-product-uses-claude-without-producing/id1763555775?i=1000771935484)
2. [How to Build a Team OS in Claude Code](https://www.news.aakashg.com/p/claude-code-team-os) - [YouTube](https://youtu.be/0UArKLQ6bXA?si=qIDcoIQzw4F5SAOs) | [Spotify](https://open.spotify.com/episode/76EZMxuTLXhG8MTmVGhmi1?si=eeLVBTCWSGCfffYNEVcn6g) | [Apple](https://podcasts.apple.com/in/podcast/how-to-build-a-team-os-in-claude-code-with/id1763555775?i=1000760124968)
3. [How to Become a Builder PM](https://www.news.aakashg.com/p/how-to-become-a-builder-pm) - [YouTube](https://youtu.be/PL7908aNeSE?si=ZjqGGEfI53M2MLBt) | [Spotify](https://open.spotify.com/episode/5ZNRFSYL15vRo7Rt51ANXP?si=GAI9a0qNTu-2r5RgpmUIRQ) | [Apple](https://podcasts.apple.com/in/podcast/how-to-become-a-builder-pm-with-n8n-claude-code/id1763555775?i=1000762483697)

**Newsletters:**

1. [I spent the last week building an OS in Claude Code](https://www.news.aakashg.com/p/team-os-cc)
2. [I spent 100s of hours building a PM OS for you](https://www.news.aakashg.com/p/pm-os)
3. [How to build product strategy in the age of AI](https://www.news.aakashg.com/p/ai-product-strategy-2026)

---

*PS. Please subscribe on [YouTube](https://www.youtube.com/@growproduct?sub_confirmation=1) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/company-os-jz) on 2026-07-15T16:32:49-04:00*


**YOUTUBE TRANSCRIPT**

Aakash Gupta

Meet Jay-Z. She's the chief product officer at Loro, the $100 million AI timeline

Jiaona Zhang

You do something pretty crazy in your interviews. Can you tell me how you interview people and really find these gems?

Aakash Gupta

The fundamentals and the principles have never changed. In fact, they're even more important than ever before. But the tools and the way you operate, that's radically changed.

Jiaona Zhang

How should people be thinking about in an AI native organization, this is the role of a PM.

Aakash Gupta

And so those are the four levels. Level one is you're talking to ChatGPT, you're talking to Claude, you're really using AI kind of in chat mode. Level two is where you start to automate a workflow. Level three is when you start building, you know, apps.

And then level four, I'd say, is where you're actually building, I call shared apps.

Jiaona Zhang

How does someone start from step one? What is the process somebody needs to go through in order to build up and create their own company operating system? Before we go any further, do me a favor and check that you are subscribed on YouTube and following on Apple and Spotify podcasts.

And if you want to get access to amazing AI tools, check out my bundle, where if you become an anal subscriber to my newsletter, you get a full year free of the paid plans of Mobbin, Arise, RelayApp, Dovetail, Linear, Magic Patterns, DeepSky, Reforge Build, Descript, and Speechify. So be sure to check that out at bundle.akashg.com.

And now into today's episode. Jay Z, I've been teaching people a lot about how to use cloud code with personal operating systems with team operating systems. You guys at Laurel have taken it to a level I have not seen before. You guys have built out a company operating system.

Can you show me what this is and what it does?

Aakash Gupta

of course all right let me screen share here okay let's start here let's go to GitHub our favorite place and so you'll see here that we have in GitHub a company-wide operating system where for every single function in a company customer success data science design engineering finance imitation legal marketing we have

essentially all these folders that share how do you think about each phase of work that that function does so in customer success you do account management and within account management you're thinking about you know renewals upsells you do a customer enablement and within that we essentially work with our customers we do

office hours we help them with rollout we do training and onboarding Each of these folders have a skill and I think for those of you who are less familiar with GitHub will actually hop over here to something that is very familiar, which is essentially your file structure, your folder structure.

And so going to customer success, you can see that each of these folders have a series of folders that are the are the activities that they do and then within each of them they have skills so how do you actually think about creating the right

assets for the negotiation support or the right references I'll go back one more for renewals right what is the skill file there to really think about how do you walk through a renewal correctly with a customer and now you're like okay cool you have some folders in GitHub you have you know

some some stuff that you can download how does this all come to drive like real change and the way I'll talk about this is you know at the end of the day we all live in some form of email or slack and so what I'll do really quickly is I'll open up my slack

and again this is not real data in the sense that we do have very sensitive data that I'm not going to be sharing so this is a little bit more mock but it shows you exactly how our team operates so for example every single morning Every person on a lot of these customer facing teams, right?

They're highly repeatable motions. The more we can sing from one voice and say the same thing, the way we can create consistency and the awesomeness of the customer experience, that makes your company, you know, much more unified and it's a big part of the brand.

And so when you think about that and you think about a customer success person waking up in their day, and really seeing, let me go here. This is an example for customer success. Here's your calendar. Here are all the meetings that you have, the check-ins that you have, the onboarding sessions you have,

This is something that a lot of people are building, this example of a chief of staff light concept. But what we're now doing is we're integrating all the skills. So for example, when we do a handoff, when we do a session prep, all of these are actual skills.

And what happens is then when anyone is using Claude, for example, and I'll just go into... I'll go really quickly into the organization settings and I go into your skills you can start to see that you can upload all of these skills into your company context

and as a result when you're going through your day you can essentially say great I'm going through my day I'm doing all these things I will use these skills so that I no longer have to spend all the time creating that one deck or spend all that time creating an email.

It is actually something you know exactly what skill to use when. And I think that's the biggest thing that companies struggle with, which is you got these people who are these 1% AI users. they're tinkering with their workflows they're highly AI pilled and then you have

the you know 90 to 99 percent of the rest of the organization who isn't sure what to use when and so as a result you can actually integrate your skills again at a company level so across every single one of these functions going back to files

each one of these functions and all the activity that they do in order to be able to understand what skills should I be using when and where should I be spending my time maybe the last thing I'll just show to kind of to really bring this to life is

every single company you can map every single functions work to what I call an ontology so in sales you know all of the work in sales maps to these categories that they're supposed to be doing Within each category, there are a series of tasks that happen.

And this is actually what has informed the ontology that I just showed you. We've done the really hard work of mapping out, okay, for every single function, again, I'll scroll through this, marketing, sales, customer success, implementation, design, engineering, so on and so forth. These are the things that we believe that each function should be doing.

How do we actually create a set of skills to for you to do the things that we want you to be doing more and to also automate the things that we don't want you to be doing anymore. So I'll go to product, which is, you know, a lot of the audience here today in product.

What's really interesting is that, you know, you should be spending your time like an engineer in many ways. And we talk about this later where, you know, the ontology or the work map of a product manager is starting to look a lot more like an engineer.

but there are a lot of things that used to be in the day to day of a product manager doing competitive market analysis doing these all these like writing for stakeholder management or really mundane tedious organization getting people on a phone synthesizing feedback etc all of these things as we all know are starting to

get automated but again it's automated in a really lumpy way where one PM might be doing it really really well and another PM might not be doing it as well so what we can do here is when you onboard everyone with a company OS again going back to this GitHub and going to let's say product right

you can start to say hey these are all the playbooks all the skills that I want to give every single person on my team and then when they come in for their daily briefing what ends up happening is that they are able to see their day at a glance

and we essentially tell you where you can automate your day so you take the thing that is that is essentially designed by the one percent of any given function the person who is playing around the most and able to spread those learnings throughout the entire rest of the organization

Jiaona Zhang

Wow. I think this is so powerful because we all have been working in different teams where there's that one person who's got their skills locked, but if they're just compounding in a bucket, then nobody can really benefit. This company OS, this is bringing that power to everybody. Now, you guys are an AI native company.

You guys are an AI company yourselves. And so you guys would have certain advantages in building this. How does someone start from step one? What is the process somebody needs to go through in order to build up and create their own company operating systems?

Aakash Gupta

I like to think about it as three different steps and so let me screen share again and I will share how do I think about essentially getting your steps in going from most simple to most advanced so the first way to think about this is how do you

just start small what is one workflow that you or your team does that is incredibly tedious that you shouldn't be doing again so typically for many many functions it is you know I write this email and I want this email to have a template that is automatically

you know kicked off for me when XYZ things happen or there's a sequence of things that happen I don't want to input my data into a CRM anymore I want that to be automated so there's some degree of thinking about what is super mundane takes a

lot of time out of your day today and if that were to be automated away you'd be thrilled about and I'll give you one very product oriented example which is there are so many companies out there so many pms out there that spend a lot of their days responding

to questions escalations so the sales team comes into a channel i'm notoriously bad

Jiaona Zhang

at my inboxes i guess there's a version of that where i seem cool and unavailable but the reality is i miss sponsor emails guest pitches and stuff that my team actually needs me for so i got an ai assistant the sponsor of today's episode a reason Ariso connects to my email, calendar, and Slack.

Then I just chat with it over Slack, and it helps me with everything. It builds workflows to respond to emails, resolve customer issues, prep me for meetings. It actually comes to my meetings, updates its own knowledge, and remembers context from past conversations. So every time I talk to it, it already knows what I'm working on.

Here's the dirty secret about prototyping. You spend two weeks building a prototype. You validate your assumptions. Engineering loves the direction. Then what happens? You throw the whole thing away. Bolt changes this completely. When you prototype in Bolt, you're not building throwaway mock-up. You're building real front-end

I use Bolt every single day I host my LAN PM job cohort on it and honestly I'm up till 2am some days just vibing in the Today's podcast is brought to you by Pendo, the leading software experience management platform. McKinsey found that 78% of companies are using Gen AI,

but just as many have reported no bottom line improvements. So how do you know if your AI agents are actually working? Are they giving users the wrong answers, creating more work instead of less, improving retention, or hurting it? When your software data and AI data are disconnected, you can't answer these questions.

But when you bring all your usage data together in one place, you can see what users do before, during, and after they use AI. Showing you when agents work, how they help you grow, and when to prioritize on your roadmap. Pendo Agent Analytics is the only solution built to do this for product teams.

Start measuring your AI's performance with Agent Analytics at pendo.io slash akash. That's p-e-n-d-o dot i-o slash a-a-k-a-s-h.

Aakash Gupta

Okay, so let's move into Slack and see what this might look like. You know, a lot of companies, if you just go into any Ask product channel or any channel, you see so many success folks, support folks, sales folks, other teams hitting up that channel, asking people, hey, I have a question, I have a feature request.

And so the very small workflow that we did, and I'll go all the way down, is we created a Slack automation that essentially said, look, when a feature request comes in, we typically spend a bunch of time going back and forth asking about how many times was this asked about?

Send me the Gong recording where I can watch what the customer is actually saying. What is the impact of this for your customer which requires some degree of judgment from the person managing the account? What is actually going on here? Give me some more details. All of those things usually require back and forth.

So again, if I go back to this system of how do you think about a place to start? What is something that you do over and over again that you could really easily automate? and that automation for us was as simple as hey let's just automate what we ask someone to fill in

and then what often happens is you then have to triage it you say hey you know is it for this team or that team is it for this pm or that pm and what's the sla to getting back to the requester on what we're doing about this feature request and so

all of that you can build into something as simple as slack so again a lot of people have slack teams whatever it is you're using to chat with your teams you can do something very simple where you essentially say okay great I come in here I'm going to automatically ask for all of this

information so you know what is it who is it coming from what's going on here it automatically assigns it to the person that makes the most sense to go look at this and then it automatically creates some kind of ticket so that we can track it and

so all of that again this is 101 I would say right it's just like a very small step in and creating your operating system so I start there the next step is this idea of how do you start to really automate based on a bunch

of things that your team is doing and so the example here I have is you know again a team that usually has a lot of people a lot of humans at Laurel we have a large you know GTM team and within GTM go to market we have really awesome success folks

who are essentially you know what I call like time consultants they're getting kind of forward to into these organizations, helping them use Laurel as a product. And so what we've done is we've essentially created a playbook. And again, this is very, very long. I think anyone who's ever created a playbook before, this is 50 pages.

It covers everything from implementation to onboarding to user onboarding. And depending on who you are, is it the admin? Is it the actual timekeeper, et cetera? You know, different onboarding. These things, by the way, are very fast now with Claude. You can actually create this from a lot of sources and have it be written really quickly.

But what the struggle most companies has is now that I've created a playbook How do I actually get people to do the playbook? And how much of the playbook is actually done by the human versus actually done by, you know, agents or workflow automations, right? And so this is where, again,

going back to this concept of the playbook model, this is where you can say, okay, well, I've created a playbook. I've went through and I've audited the things that, again, it requires a human to do. It requires a human to get on the phone with someone. It requires a human to go fly on site.

um but here are the things that we think we can automate this is either um something we can productize or this is something that we can create an agent to do and so that is I would say that the next step that you graduate to where you

essentially create a playbook and then off of the playbook you decide on a set of skills and and that's by the way where we um we started to get the first version of the OS I showed you earlier when we went into customer success and we said what are all the things that someone might be

doing these large buckets it was largely off of playbooks the playbooks for implementation the playbooks for activating a customer the playbooks for really yeah talking to them the right way to make sure that they're set up for success and so that is really the second way to think about it and maybe I'll share one thing here

which is there are a lot of agent builders out there today in the world so you could use you know Claude itself they've launched obviously a lot of agents you can use a lot of things from OpenAI as well you can use a Glean you can use a Dust we at Laurel use Dust and so

Jiaona Zhang

take a moment see if this loads so if somebody hasn't heard of dust yeah this is an

Aakash Gupta

agent building tool this is an agent building tool and what we find is often a lot of the things that someone does can be turned into a series of repeatable steps that gets automatically triggered and so a great example and I'll just go scroll down here really quickly All of these are agents that we have built.

So going back to the playbook concept, if you say, hey, I have a playbook of all the things that you need to be doing here, and again, 55 pages worth. I don't think anyone's going to read anything here. What you can do is go into an agent builder and say,

I'm going to create an agent for each of these steps. If I have to draft emails a lot as a customer success manager, if I have to actually scrape LinkedIn a lot as a salesperson, if I have to look at the market as a salesperson or think about prospecting questions,

you can build an agent for each of the Parts of the workflow here and then going back to really thinking about how does everyone engage with your operating system thoughtfully? No one's going to remember that they're going to call the specific agent that's going to do the email and the specific agent that's going to do the RFP.

The big learning that we've had is how do you create a mega agent, something like a go-to-market agent that can be called by the sales team at any point by the success team at any point and then that agent is able to route the ask the the need or the help to whatever one of these sub

agents that is actually useful and then going back to like it really the delivery piece is so important even the friction of coming to something like a different interface coming to a desk and asking your questions is really low instead actually going into your um your slacks your emails and delivering people just in time playbooks and

automations is really the way to go to get to the point where you're actually getting people to use the agents and the workflows that you've built so help me

Jiaona Zhang

understand this part why use dust instead of just all clod or clod code

Aakash Gupta

Yeah, that's a great question. We started using dust back in fall of last year. And so I think there was just a maturity of the tools. Back then, it was just much easier to use something that specialized in agent building like a glean or a dust. I do think today that gap is shrinking quite rapidly.

And so as a result, I don't think you need to go out there and buy a specialized tool that does these. And in fact, you can just build them in clod. and this is actually a little bit where we're going which is if I go back to the

operating system that I was showing you earlier and all of these no longer have to go through a dust or a clod instead what we're able to do make this much larger is we can we can take all of these skill files and go into clod itself and put them in

as skill files and so as a result you could now you can literally just say hey I'm inside whatever it is I'm doing and I can just call the you know that skill slash morning briefing product and as a result it gives me my briefing right there as opposed to

Jiaona Zhang

me having to go and call an agent builder and then should people be setting up like cloud automations on top of these to be running these is your daily morning like running on a schedule or something like that yeah that's a great question it's so

Aakash Gupta

funny um I'll go I'll share a little bit my personal experience so I set up a bunch of these scheduled things and even if I just go to scheduled I'll go right here you can see that I have a lot of these scheduled tasks and you

only see a couple of these pinned and what I found was that it was almost overkill it was like I sat there I was like oh I might automate this and so I built it I was like oh I might automate that and so I built it I was like that might be

interesting information I built it and actually I think we're in a world where we are We have information overload. And so this is why we took the time as a company to be like, we can't just assume that people, first of all, that they're going to do this for themselves. And second of all,

that they're not going to be overwhelmed by the number of like automations and, you know, uh, schedule things that happen. And as a result, that's how we consolidated it all into what I was showing you earlier, which is this, this idea of actually having all in one place,

because the chances that you're going to come back and say, okay, and again this is also to make sure that the information or like the adoption of AI is actually consistent across the org and that's the main thing I think that you

see a lot of let's say PMs be super AI native a lot of engineers be super AI native you don't see the same across all the functions and potentially sometimes they go to market functions and so as a result we really think hard about how do we deliver

that to you in the form of something that you can look at on a daily basis and really be integrated with your workflow and the last thing I'll share at Laurel is we think a lot about how do we surface it even more just in time and what we're able to do in terms of our product is

we're able to detect what it is you're working on when okay so I think I get it

Jiaona Zhang

right the thing that you are encoding that's most important is not the scheduled tasks or this particular interface and dust. It is the actual skills and you are enabling the least AI proficient people at your company to operate at a similar level to those AI native people. What is the right company culture?

How do you really get people to take advantage of a company OS like this?

Aakash Gupta

Yeah, absolutely. I think it really starts with culture. I just have a few photos from our offsite. um about three months ago and um it's really important to for it to start from the top from leadership to say this is so important to us it is not just an engineering

thing it is a cross-company thing and what we did at this offsite is we did a company-wide hackathon and I do know of a lot of companies that do this on a regular basis how do we do a company-wide hackathon um every quarter every six weeks right um or how do we even get the just the

go-to-market team to do a company do a hackathon and show what it is that they're building so the expectation that you know everyone is a builder is is true everywhere in the company not just in engineering so with this um what we did is we did two things one we did um training

and so what we did is we actually did a lot of training around like how do you actually ship to production even if you're not technical so we created this enablement guide for how to ship features with Devon and so you know Devon essentially is like an agentic engineer you can give it tasks

it started off I would say a year ago two years ago when we first started using this as almost like intern level engineer and today I think it's actually you know a decent software engineer it's not a staff level software engineer but it does a

lot of things and as a result you know my team is able to ship and I'll just go through a couple examples here is a feature an end-to-end feature which includes front-end changes and back-end changes where you know we enable people to do to delete temporary initiatives so when you're keeping your time sometimes you

don't know what matter or what project you're working on yet but you know that you're doing some amount of work that should be grouped together and submitted at the end of the day and so that's where temporary initiatives is really powerful now

that again is a front end and back end feature it is not just a front end like almost like cosmetic change it's actually pretty deeply rooted in how does it interact with PMSs and other systems and when does it release versus not there's a lot of complexity in something like temporary initiatives and so this by the way

you know if you look at the person actually knocking down those tickets and committing these PRs this is actually a PM on my team and I'll just go to their LinkedIn briefly. Nick, who's awesome, has been at Laurel for some time. If I go back to his educational history, right, like we didn't grow up,

many of us didn't grow up as engineers. And yet Nick, I would say he's probably identifies, self-identifies more on the design side than on the engineering side, is able to take this feature end to end, which I think is just so cool. Similarly, within

you know many parts of our product I'll just go through another example here this is the empty state for when someone comes in so really think about new user onboarding what is it that they see how do how do we make that experience super

delightful all of this is done by by Jessica who is again a PM on my team not an engineer and also not a PM who necessarily started their career in in engineering or studied computer science. And so I think this is just such a great example of people being able to ship even when they're not technical.

And maybe the last thing I'll show you, because I think this is even cooler, is this little picture here, which is this is someone on our customer success team. Ashley is amazing. She deeply understands our customers and their needs. And by working with the PMs on the team to really create this enablement guide for Devon,

they worked on this together. so that, again, if you are even less technical than a PM, right, if you're on the success team, how might you use this guide to be able to really ship the way, you know, in a safe way, in a reliable way? And then all of these pieces we then broke down to say,

well, should we start building skill files, you know, agents to help you so that when you're trying to do this thing that typically is a playbook, and again, this is not 55 pages, but it's still eight pages. You are able to get the help and the support you need. And so that is really, again,

the crux of it all is understanding what is the work that you're doing? How do you start to document that down? And then really clearly define these are the parts that remain human centric versus these are the parts that should be automated away. I'll pause there, but I think it's also really cool to look at this ontology,

which is essentially, you know, for every single function in the company, what are all the buckets of work that they're doing? And what we do is actually we actually spend cycles saying, you know what, we believe that, like I said earlier, a product person should be operating like an engineer so all of the things that we

expect an engineer to do we expect them to be doing feature work we expect them to be testing you know we expect them to actually like crank through the backlog the exact same things show up in what we want PM to do um it is it is not a um an error

where you know here in the ontology We really have things like we want you to be, you know, doing future work with agents. We want you to be, you know, actually QA'ing your product and fixing the bugs, not just like QA'ing in the ways that people were doing before.

and what we don't want you to be doing is things that were really tedious like synthesizing competitive market you know intelligence actually writing these like detailed briefs doing research planning doing reach out for the the research synthesizing the research like all of that you know competitive analysis is a great

example it should you should be spending time building the agent to pull the competitive data and you should just be monitoring it but you shouldn't actually be doing the deep work every single day and like set up the system instead and so when we actually create this ontology we're able to say well we want these

numbers to go up We want everything in green, the time spent doing that to go up. I want to see Nick doing this. I want to see Jess, you know, shipping this feature end to end. But what I want you to stop doing is I want you to stop doing these things that are

really tedious or at the very least to be calling an agent every single time that you want to do that and then Again, going back to how do we make that true? By building the skill files, by building the agentic workflows where necessary and making sure that we're surfacing them where people work.

And that's ultimately the key pieces of the system.

Jiaona Zhang

Wow. There is so much gold buried in the various parts of your answer there. The first part I want to double click on first is PMs shipping to production. Okay. People have heard about that. but PMs not just shipping okay here's this little growth experiment where we change

the text in a button which is a front-end only change but a front-end plus back-end core feature this temporary initiatives feature for instance that we looked at that's crazy so talk to me a little bit about what is the scope of what PMs do ship

to production and how should people be thinking about in an AI native organization This is the role of a PM today.

Aakash Gupta

We talk a lot about this in terms of what is engineering anyways? What is product anyways? What is design anyways? And we've really landed on this concept of we want there always to be a captain of any given initiative. And the captain is the person where that skill set is the most important.

And so there are lots of features. Let's say we need to overhaul a system in order to make it much easier for, let's say, PMs to ship and agents to work in that code base. Usually the captain is an engineering captain because that's an architectural change. If we have a feature where the interaction is really king,

we're doing this really cool stuff on mobile to make it so easy and delightful to look at how you spend your time in a given day and get insights from that.

Jiaona Zhang

I hope you're enjoying today's episode. Are you interested in becoming an AI product manager, making hundreds of thousands of dollars more, joining OpenAI and Anthropic? Then you might want to do a course that I've taken myself, the AIPM Certificate, ran by OpenAI Product Leadership.

If you use my code and my link, you get a special discount on this course. It is a course that I highly recommend. We have done a lot of collaborations together on things like AI product strategy. So check out our newsletter articles if you want to see the quality of the type of thinking you'll get.

One of my frequent collaborators, Pavel Hearn, is the Build Labs leader. So you're going to live build an AI product with Pavel's feedback if you take this AIPM certificate. So be sure to check that out. Be sure to use my code and my link in order to get a special discount. And now back into today.

I used to think I had a retention problem. Turns out I had a messaging problem. I was sending the same onboarding emails to every new user whether they activated on day one or never logged in again. I had no idea who was slipping or why. Customer.io changed that. aakashgupta aakashgupta

You can see what's happening in your customer.io workspace. Notion used Customer.io to personalize their onboarding and hit nearly 50% open rate. Improved conversion by 6-7% That is more so than anything. It's a data problem. So we have, you know, data science really plugged in there, but really, um,

Aakash Gupta

the interaction is the most important thing to really sweat and make sure it's delightful and as a result a designer is the captain of that work stream and then something like what I just showed you something like temporary initiatives something like the empty states Really having deep customer understanding but also business context is really important.

How do I know what people want to do with temporary initiatives? How do I know what the user wants to do but also how do I know what the firm really wants to get out of it and or not? And so what we spend a lot of time now thinking about is what is the most critical

piece to nail for the outcome that we're looking for and therefore the feature that we're building? And as a result, how do we appoint a captain that is skilled in that particular area? And so that's generally how we think about the model evolving.

And so going back to a feature that might touch the front end and the back end, If we believe that the backend is in a good enough spot, and by the way, you can ask Devon or even anything that's connected to your GitHub account to look at the code and say, in what state is this?

And it actually gives you a pretty good answer. Hey, this is what I would be careful of. And then you can actually pull in engineering on the parts where you're like, this is probably the most contentious or this is where it gets the most risky.

And again, you don't do this by yourself because you happen to be the most technical person. were not. You do this through the help of asking, you know, Claude Code to look at your code base, cursor, again, whatever tool of choice you choose to use,

you can ask it to really give you answers the same way that a marketer would say, look, I'm giving you some copy, now battle test this and go back and forth. It's the same concept. And then going back to if you are clear on, again, what is the hardest thing to get right in a particular feature?

For example, empty state. The empty state that we're working on here it's the hardest part to get right is definitely not the engineering the hardest part to get right is not even the design it's the content and again the content has to do with the user and the business and the firm and

that is a very classic PM thing and so it makes sense for the PM to be the captain of that and so that's really the model we think about captains you know using um um you know LLMs essentially like ask how hard something can be

Obviously we still you know have code review and we make sure that engineers are code reviewing the things that are risky and so all of those pieces together makes it so that we can all ship including you know customer success which is again

Jiaona Zhang

really wild and like go-to-market sales I think we can all immediately see how that allows engineers to work on the highest leverage back-end tasks PMs to work on higher leverage features if CSM and go-to-market are enabled what is the Right set of checks and balances you need to put in place in your organization. You mentioned code reviews.

Where do those come in? How do CSMs or go-to-market, for instance, make sure that what they're building isn't in conflict with something the product team is building over here, in conflict with somebody else's metrics? Usually that's where the PM came in and did a lot of the glue work.

How do you handle that in this new way of working?

Aakash Gupta

Yeah, that's a great question. So we... again I believe in the power of humans so something as simple as you know creating a channel like Ask Devon Reviewers and being able to go through here and making sure that there's visibility around all of the Devon all the ways we're using Devon

to ship and then tagging in the right person tagging in you know a front-end engineer to really look at something tagging in designer to look at something else really going through and making it visible I think the first advice I give is transparency is everything

the second piece of advice is you do need to set some ground rules right so again going back to our enablement guide we've set some ground rules here As part of even the way Devon works, we actually used to do this quick check where whenever someone, let's say someone on support had an idea,

they essentially could go into this channel and post their idea and get a really quick check on, is this something that makes sense? And again, I'll just zoom in here. I'm proposing a change to this experience. Getting some feedback and being able to say, hey,

play around with the first version of it and getting people to chime in and say, hey, this makes sense. This doesn't make sense. I'm on the engineering team and let me give you some feedback. I'm the success team. Let me give you some feedback.

what you're really doing is you're taking what used to be a product review that used to take time to schedule and time to get all the stakeholders in the same room

Jiaona Zhang

and you're just compressing it double click on product reviews for me you guys have a really interesting process for when you do and don't do product reviews what is the right balance so that you enable people to move fast but you're building the right level of collaboration on bigger features

Aakash Gupta

Yeah the same way we have this captain's model I think about a framework where we call it two tracks so there's one track which is much smaller if you have something that even some of the features I just showed you like they're small enough where

again a PM somebody a product captain or a product builder right can take it end to end those don't go through the same degree of a rigorous review but they do go through things like that ask dev and channel they go through things you know like like someone looking at the PR making sure things

are good you by the way you are responsible for end-to-end testing of your features I think that's actually really positive the number of times we're in a waterfall model you would PM throws over the designer and the designer throws over to the engineer and then engineer throws back to the designer to design QA and the

designers like this is not design and that is just I think it's just such a it's like it's almost a meme because it happens so often and so I think that's actually really empowering to say I am the end to end product builder and I take something from beginning to end and

I own and I'm responsible for the quality and impact of this thing and so first of all I just think that's a much more empowered way to work um so but but then going back to the two tracks you have things that you know can really take the product life cycle and compress it down to

a day an hour you know like and that's how you get the velocity but there are some things where you're like look I think that the way that this product is going to behave what I'm suggesting is a change the feature that I want to do it requires

much more alignment so a great example is within Laurel if you're going to change the complete way that activities are displayed that's a pretty radical change and how might someone a user go zoom in and out of their day That is not a small thing. It's the whole user interaction.

And as a result, we say, look, we do want to do a product review for that. We want to make sure that we talk about, well, how do we think about the entire product as a system so that we're not adding some random thing over there and a random thing over there?

but a lot of I think the first step is to actually even say what is in what bucket so that the things that could be running really fast are but also I really don't believe in this I think a lot of quote unquote AI native companies are just like roadmaps are gone Planning is gone. Everything is gone.

And what I say is, well, if everyone's running in different directions, even if you're running incredibly fast, you're not really going to get anywhere. And I see a lot of great local maximizations, but sometimes it's really hard to get to the global max, a whole new set function change in your product, in your market,

positioning without real rigorous thought around what is our strategy, what is our plan, why are we differentiated? And those are the things that require much more of what I call a true product review process where to me it's more like product strategy review and then there's architectural review right making sure that the system actually will

support all the changes that you want and that you can get to a next level of

Jiaona Zhang

running fast so did temporary initiatives go through a product review it did not wow okay so what would be the like the right aperture what would have been some of your recent product strategy reviews yeah so um

Aakash Gupta

Today, Laurel is beloved in a lot of firms that think about billable hours. And we're starting to find that there are a lot of firms, even if they don't have billable hours, they still need to think about the concept of time. I would say it even applies to tech.

I think about the concept of time all the time. What are my PMs doing? Going back to this ontology and this work map of every single function. I mean, all of us should be thinking about the concept of time. What should salespeople be doing today versus what should not

be human anymore and this is I want to be very clear this is not a therefore we do not hire humans it is a put the humans on the most important things and I'll give you some great examples in here relationship building you just will never replace a

real check-in a real moment of you know true hospitality and delight an actual on-site taking a champion out to dinner that cannot be replaced by agents but what will make it so So much easier to operate and no one actually wants to do these things.

What if the scheduling for the onsite and making sure that all of the back and forth and logistics is taken care of? You know, again, in marketing, we do a lot of events. What if all the logistics of event planning work on? Even this idea of unreasonable hospitality. And I think this is such a great example.

It is such a core value of us, of ours here at Laurel, where we really want to delight. our customers all the time we want to delight each other we want to delight our customers and so we really have codified unreasonable hospitality as almost like a

like a cultural principle that we have a company value a lot of companies do this by the way they're like this is a cultural company value and then it's in a doc somewhere people read it and then they forget about it and what we do instead is we

say well what does that actually mean we actually want to make sure that no matter who you are even Even if you're the most thoughtful person in the world or you're not the most thoughtful person in the world, even if you're four years into your time at Laurel or you're four days into your time at Laurel,

you understand that unreasonable hospitality is a requirement of how we operate. And especially if you're on the customer success team, we expect that you do this with our customers. How do we systematize that? And that's a real question. You know, again, there are people on our team who

um just from who they are as humans they're the kind of people who's like someone told me that they're going to Mexico and so and it's the first time by the way that they're traveling outside the country and so I bought them an engraved passport

holder that is by the way a lot of people on the Laurel team but if I were to scale that to hunt like a lot a lot of people make sure that everyone's doing it every point in time, even when they're really busy with other stuff, it's pretty unlikely that that's going to happen. Instead, we say, well,

we actually want to make sure that unreasonable hospitality is a check that we put in. And so again, going back to the OS I was showing you, hey, if you have a check in with someone and You know, you haven't actually done anything like this in a while. You haven't had an in-person touchpoint.

How might you surprise and delight them? And here's some ideas that we've already pulled for you. We pulled from your Gong transcripts that these are things that they love. And we pulled from the fact that they love these things instead of making you do all the work of figuring out is it a passport holder?

How do I even get a passport holder engraved? We're going to systematize that. And so that's this real idea of like deeply understanding your company's work your team's work what are the things that makes you special where do you put the humans on the things that make you special and then where do you even in those

moments like unreasonable hospitality make it so it's easier to do that job and to

Jiaona Zhang

deliver that particular feeling so you this isn't your first rodeo you've been in product for a really long time if we rewind back to some of those experiences those formative experiences let's say like Airbnb in 20 you've been The PM traditionally never had access to GitHub,

let alone the amount we're showing here where they have a Devon agent that is shipping front-end and back-end features. And you'd be surprised, even at companies like Adobe, PMs are still living in that world that you and I were in back then. They still don't have access. They're looking at what we've just showed them and they're saying,

gosh, this is too far away from my reality. is it true that like this just won't work in certain type of companies or will they eventually get there it is just a matter of time I'll start with the end which is I

Aakash Gupta

do think it is a matter of time that every company is gonna have to get there you can't keep doing the same thing if everyone else including all your competitors are moving at 10 times the speed so I do think that there will be pressure to

ultimately get there for everyone now what you want to be for the company and for the individual is you want to be um as far uh you know as as advanced as possible right in that curve as opposed to just waiting for it to happen to you and this is where I go back to you know the

first step is just start small start with one workflow that you are doing and or I really I really push on this I think this is really a great way to get your feet wet and start to think about this go find another team

in your company somewhere and even if you're like I am not quite ready to ship to production for whatever reason and usually the reasons are not that you can't like you're not physically able to it's usually some thing about the system or the

process that it's not quite there yet but let's just say that you don't feel like you can in the next month go somewhere else where there's always somewhere in the org that is hungry for product thinking and hungry for a tool to make their life better and I would start

with let's just go build a tool for somebody in a different org to make their life better and simultaneously pick up one part of your workflow that is taking you a lot of time and there's really no reason that you should be doing that again great examples I'm getting into a customer call

I would love to be prepped for that in a way that you know an agent is serving me that information as opposed to me having to pull from multiple different sources right that's a very simple example I write the same same email over and over again

it should be auto populated again these are just small small little automations or you can call them templates whatever it is that makes sense to you start there And then I would say, if you're ready to take on something bigger, this idea of like, what does a function do?

Or what does an end to end operational journey look like? And there I would start to say, map out your ontology or take your playbook and really, you know, write that down. And again, What I find really fun is like these playbooks, I think if someone was tasked to write a playbook back in the day,

they'd be like, okay, I'll do it. It'll take me a couple of weeks. These playbooks can be written in an hour. Actually, the first draft can be written in sub a minute, but to make it actually right and, you know, really reflective of your business.

Yeah, it'll take a little bit more time, but we're talking hours here is maybe days max. We're not talking weeks. And so I think when you get a feel for how much you can enable yourself and you can enable others, you're going to create a culture.

Again, even just going back to culture change, you're going to create a culture where, um, It's celebrated and it's fun. And again, if you're leadership, what I'd really encourage you to do is make that the culture, celebrate those wins, take the people who are your 1% and take their workflows and figure out how to

scale that workflow to every single person on the team. When you create that expectation and you celebrate those wins, you'll get more and more of that behavior.

Jiaona Zhang

For you guys, did it happen as a transformation? Were you guys always this way? Did it start with the CEO and the founder? How did it come about so that now you guys do feel the confidence that you have this enablement playbook of Devon where anyone can ship to production?

Aakash Gupta

Yeah. I think there were a lot of pieces, but I'll highlight the pieces that I think are most relevant that someone listening to this could take and replicate. The first piece I've already shared which is the idea of just doing a hackathon and in the hackathon making everyone participate because it changes this idea of you

have to be technical to build something and again I think most people have done that so I would expect that you know 90% of the people listening have participated in some kind of hackathon if you have not that's the first step um the second step is to really think about all the different ways you can again

automate the workflow I think that a structural thing that I would really recommend is actually making this idea of playing with AI tooling creating workflows um automating you know large swaths of somebody's day in a way that makes them much more productive make that the actual charter and mandate of a full of a person full

time and what I really find is a lot of times when you say it's everyone's responsibility it's no one's responsibility and so what we have at Laurel is we actually have an AI operations team and to me AI ops is the new biz ops before biz

ops they were doing um really meaningful things but often it was it was very um high level all the different hats a lot of like market level stuff now if you repurpose this idea of having biz ops which is really again a Swiss Army knife in

many ways to finding people who are insanely curious tinkering with the latest technology and relentless about finding efficiencies that's the DNA I really look for and so we've actually built out an AI operations team we started with Sasha who has built out a lot of the things that I've shown today.

And what he did is basically was like, I'm going to demonstrate value in having AI operations. And very soon when you have one person who's doing an excellent job, every single other function is like, I want my Sasha. I want my own AI Sasha and that is how you then get the buy-in to say okay well

maybe we have an AI person a operations person just doing go-to-market and a separate AI operations person just doing product and a separate AI operations person just doing finance because all of these functions by the way finance rev ops product ops research ops

you name it all of them are changing so dramatically and so being able to retool your the way that your company works with someone who's really dedicated to pushing that forward really really accelerates the the journey that's really interesting

Jiaona Zhang

and you guys were founded before the ai revolution so I guess for other companies that were founded before that, I think you were 2018, who is the right driver? It feels to me like it probably has to start literally with the CEO, right?

Aakash Gupta

I want to give a ton of credit to Ryan so yes Laurel was founded actually I would say Time by Ping this is what Laurel was called previously was founded in 2018 but Ryan actually had the foresight and the courage really to say you know what when I

think about what time looks like in a world of AI and LLMs it's very different and when I think about at the time our core product timekeeping right like what is timekeeping look like in a world that where you have to kind of enter it manually or just do it through

call it what I call integrations versus a world where you can actually start to really see everything that's happening on your computer and synthesize that and run that through an LLM like he basically had the foresight and again courage to say I'm going to re-architect my entire product my entire company to be AI native

and so it's really interesting like I really believe that and I experience this day to day I would you know like I was like I want to be building at the cutting edge Laurel is AI native although it was founded like more than three years ago and so

that it does start with the CEO but even if people don't have that degree of change and conviction I think you can still do it at every single level where you know if you are not the CEO but you're an executive you can say well this is how I expect

my function to really operate here in my function I am a marketing leader I fully expect that this is what we are doing and let me go color code everything in here that should be AI enabled right like when you think about copywriting today you

should not be writing copy by hand you should be editing when you're doing videos like if you're not using a lot of the AI tooling out there you're spending a lot of money on studio on video in a way that you don't need to anymore so being able to go line by line in terms

of your again your your work map what is it that all my humans do and how do I really think about where do I need to keep that person versus where can I actually really AI charge supercharge them

Jiaona Zhang

Amazing. So I think that's the key point for a lot of people that I talk to at least is that they don't have any access to the stuff we're showing and probably it needs to start like all the way at the CEO level and then it can work its way down where

like you need really amazing CPO like yourself who is also AI pilled in order to make this happen. And that's kind of the next layer I want to talk about is As an AI Build CPO, what is your take on the types of product teams we're going to see in the future?

What types of product managers are you hiring and what is the shape of their role today?

Aakash Gupta

I think for many people, I'm sure this is dialogue that's happening everywhere, this idea of are you a product manager or are you just a product builder? And how many people are product builders? Meaning is it just the product person themselves by functional title? or is it also the designer? Is it also the engineer?

I'm a big believer of the fact that I think everyone should be a product builder. It goes back to how we operate the team today with captains and taking features end to end. What I do look for specifically in product builders who are product managers by training. I looked for a couple of things.

I found that if you're incredibly senior in the sense that you have the judgment, you've gone through the hellfire, you've shipped things that haven't worked. And I think for all of us that have shipped things, most of the time it doesn't work in the first go around. If you kind of have that battle-tested judgment,

I'm finding that the combination of that experience plus this intense curiosity, this desire to be hands-on, I think you see a little bit of a bifurcation. There are a lot of people who are very experienced and almost scared that their job is changing and...

they're feeling more fear than I would say excitement and I would say that there's another group of people who are very experienced and they have been they've never been more excited like I've never been more excited by the way to not be doing all

these things I used to do in the past that took me forever that there was no part of me that wanted to be doing that instead I love you know actually like shaping a product really getting hands on and then so being able to find those people who are excited who are curious but yet have the

the judgment and the reps is really, really important. And so again, this is not necessarily by design, but what I found really interesting was You know, there are a number of people on my team who previously were, you know, CPOs, VP of products, head of products. They've come in and they're the ones building end to end.

They're the ones shipping end to end. And again, they've never been more excited. They've never been more excited to not have a team to have to manage because they realize that a lot of that is just overhead. A lot of that's just coordination cost. They've realized that a lot of it is just coordination cost. And instead,

they can just be enabled to get right in there and drive the change that they want to see.

Jiaona Zhang

That's crazy. So you have embraced the super senior ICPM. I think you said something pretty crazy, actually, when we were talking before, which was the more senior you get, the longer you've been in product, the smaller your orgs have become. Is that the trend of the future, smaller and smaller product orgs?

Aakash Gupta

I think so yeah I mean I've had hundreds of people and today I have five PMs and four designers and there isn't a real reason to grow that because again like when you add more people you add more coordination costs you actually have a harder time

making people feel like they are absolutely responsible for taking something end to end and so I do think of that as the future. I think that the best teams are gonna be lean, but not so lean that they're starved. And so it's really important to find that line.

Jiaona Zhang

So you said you do something pretty crazy in your interviews. Can you tell me how you interview people and really find these gem AI-pilled super senior ICPMs?

Aakash Gupta

I think a lot of people are talking about, of course, you do a session where people have to build with AI. I think that's all fine. I think it makes a lot of sense to do that it takes cycles by the way to even have a standardized interview loop some companies it makes sense because they're large

enough where they're hiring you know enough PMs but again I do think many people are saying hey let's actually get a little bit more um particular about who we hire and make sure that they're really seasoned and we'd rather pay a few really seasoned people you know a lot more than having just an

army of people and so um what I've been doing and I do this by the way for every function not just product or design or so you know so and so forth um is I do ask people to screen share and what I found is it is so easy to say hey we are you know

I'm AI pilled we're AI pilled we do a bunch of stuff with AI but as soon as you get into um like if you really peek under the hoods you're like actually I think you're what I call like level one and maybe I'll just take a moment and talk about the levels for

me level one is you're talking to you know you're talking to chat GPT you're talking to Claude you're really using um AI kind of in a chat mode almost like like search mode right like I asked a question you give me an answer level two is where

you start to automate a workflow right and this is what I was showing earlier around just the first step is like start small an OS does not start necessarily as an OS but it starts with a first automation right a first little piece of workflow that

everyone's going to start doing and so that's level two level three is when you start building you know apps right you say hey you know it's really important that I I'm doing this thing it's really tedious I'm going to build an app to make it

like less tedious and then level four I'd say is where you're actually building I call shared apps and or um if you really think about the product life cycle you're you're really shipping to your customers and so those are the maybe the four levels um that you can assess

yourself on you can assess a given company on like which of those four levels is the majority of the organization um operating at and so um what i find is when you actually ask someone to screen share and show them how and show you how the ai you're very you can very quickly get a sense of

are you at level one are you basically just talking to chat GPT or have you actually created like some way to really like scale yourself some kind of workflow some kind of agent or are you starting to build like apps and or you know what are

you shipping like truly truly shipping and so really getting to see that Live on screen is really really interesting because otherwise it's really easy to just be like This is what I do and it's pulled from LinkedIn or pulled from the latest thing you saw on the internet But actually peeling it back and be like what

is on your screen is it's really fascinating Wow People don't believe me when I

Jiaona Zhang

keep saying this is the new interview. This is what I'm hearing you've heard it from a CPO herself. So a lot of people are feeling pretty bad about this whole transition like there there's a lot of fud going around in the pm field if you check out reddit or

something people are feeling a lot very nervous about this change they're saying hey we're compressing out the juniors you had a really interesting take on this which is that the best pms are actually getting more roles and the rest are feeling fear and destruction can you unpack that for us

Aakash Gupta

I think it's because 1PM can do so much more than ever before, but there aren't that many of them who are that skilled, that have that judgment, who are AI-pilled, who fearlessly are going through all of these pieces and, by the way, know that one of the most important things forever and will never change about the

PM role is that they have to stay close to their customers. The Venn diagram of all of those traits is not large in terms of the actual number of people that fall into that, and that's what every company is going to want.

And around the edges, it's like, why would I go hire someone who is not all of those things? I'm going to have to supplement them in some way. And it's going to create overhead. When in many ways I can take that piece that is not excellent and I can build a workflow and agent around that.

So I think it's really finding who I call the orchestrators, the people who are big picture in terms of their thinking but down to the detail in terms of their execution. Those are the people who are worth their weight in gold and I think that a lot of people who need to be complimented by

It's not me saying it, guys. It's her. I've been preaching this for months and months. This is the future of product management. We just gave you the entire playbook. She just screen-shared literally everything, the company OS, how they're

Jiaona Zhang

PMs are knocking down linear tickets. If you want a really amazing job, apply to Laurel. Jay-Z is not just doing this though, right? You actually have so much cool stuff going on. You teach product management at Stanford. I think you at some point have been involved with Reforge. Can you catch us up outside of Laurel?

What's the world of Jay-Z? What's going on?

Aakash Gupta

I do teach every year at Stanford. I do it for the love of... Really just getting to meet the next generation of builders. I also get the really awesome benefit of meeting people like the Sashas of the world who, you know,

once took my class then TA'd for me and now is at Laurel and you know teaching for me has been a combination of passion and honestly a pipeline so I teach at Stanford I teach at Yale and I teach at Reforge and it's just how I think that when you

teach something you have to know it like the back of your hand in order to actually share that with someone else so again I just find this really funny a lot of times I'll teach and then I'll be like ah good reminder Jay-Z like Were you doing that today in your day-to-day? Were you customer centric enough?

Were you problem space first and not solution first enough? And so I just find it both so gratifying personally, but also such a great reminder of what product really is. And I'll say one last thing, which is what's funny is that, so I teach AI leadership through Reforge and that curriculum changes literally by the month.

you know we teach every six months and the amount of change between the six months is massive but when you actually teach fundamentals when you teach what I call like PM one-on-one those core principles have not changed you should still always never jump to the solution and now that you can build faster than ever before it doesn't

mean you just build everything like what actually is important is to know why and for whom you're building for and what is it that you're trying to solve for and what success looks like and therefore you actually know you've hit your target and so what's really ironic is that

Through teaching all these different levels of product people over the years, I find that the fundamentals and the principles have never changed. In fact, they're even more important than ever before. But the tools and the way you operate and the way you can blast through the bureaucracy and feel empowered, that's radically changed.

And so as a leader, the way you empower your team is very different. Do you have the right culture do you have the right team do you have the right space for people to even build do you have the right operating system do you have the right

knowledge of what people are doing day to day do you have all of those pieces that is changing dramatically but in your actual you know one on one on one basics around what it is that a product person is supposed to be doing um the speed has

changed dramatically but what you're supposed to be doing at the heart of it that has not changed

Jiaona Zhang

What a way to end it. Alright guys, we have hit a crazy milestone. We crossed 40,000 YouTube subscribers. We have also crossed 565,000 average views per listen per episode. When I started this podcast two years ago, I wouldn't have believed it. 365,000 of you to flood Laurel's PM applications.

For my money, this is like the coolest PM job you could possibly have. And I would say if you are in a PM job where everything we were just talking about feels really foreign and like 10 steps away from what you are, find a job like this with an AI-peeled CPO like Jay-Z.

You are going to learn so much more than if you get to this four years from now and then you learn it. Thank you so much, Jay-Z. Thanks for having me. I hope you enjoyed that episode. If you could take a moment to double check that you have followed on Apple and Spotify podcasts, subscribed on YouTube,

left a rating or review on Apple or Spotify, and commented on YouTube, all these things will help the algorithm distribute the show to more and more to get access to nine and many other amazing tools that will help you as an AI product manager or builder succeed. I'll see you in the next episode.