---
title: "How to Run Evals in Claude Code with Aparna Dhinakaran, Founder and CPO of Arize"
source: "https://www.news.aakashg.com/p/aparna-dhinakaran-podcast"
author:
  - "[[Aakash Gupta]]"
published: 2026-05-22
created: 2026-05-23
description: "Install Arize skills, ask Claude to suggest evals, and build a self-improving loop. Exact commands and steps with Aparna Dhinakaran, CPO of Arize AI."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
Here's the exact prompts and steps to build evals in minutes

![](https://www.youtube.com/watch?v=DL-pUGcfrf4)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/how-to-become-a-builder-pm-with-n8n-claude-code/id1763555775?i=1000762483697), [Spotify](https://open.spotify.com/episode/5ZNRFSYL15vRo7Rt51ANXP?si=glhi9q4SS7igfxzCWWA0bw), and [YouTube](https://youtu.be/DL-pUGcfrf4).*

**Brought to you by:**

1. [Superhuman](http://superhuman.com/akash) - The fastest email experience ever. Get 1-month free with my link
2. [Land PM Job](https://www.landpmjob.com/) - My 12-week AI PM + Job Search Course
3. [Vanta](http://vanta.com/aakash) - Automate your compliance. Close deals faster
4. [Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7) - Get $550 off their AI PM Certification, code AAKASH550C7
5. [Bolt.new](https://bolt.new/solutions/product-manager?utm_source=Promoted&utm_medium=email&utm_campaign=aakash-product-growth) - Ship AI-powered products 10x faster

---

## Today’s episode

If you’re building in Claude Code, you should learn how to build evals in… Claude Code.

There are two major evals platforms in the market today. We’ve already had the CEO and founder of one on, [Ankur Goyal of Braintrust](https://www.news.aakashg.com/p/ankur-goyal-podcast).

Today we return with the other major platform, Arize. And we have on the CPO and founder, [Aparna Dhinakaran](https://www.linkedin.com/in/aparnadhinakaran).

Many of the smartest AI teams are running their evals on Arize - Uber, Booking.com, Pepsi... I even offer Arize in my [bundle](https://www.news.aakashg.com/p/aakashs-bundle). So now we bring you the guide to using it.

This episode builds upon the basics I taught with [Hamel Husain](https://www.news.aakashg.com/p/hamel-shreya-podcast-2), [Shreya Shankar](https://www.youtube.com/watch?v=J7N9FMouSKg), and [Ankit Shukla](https://www.news.aakashg.com/p/ai-evals-explained-simply). It even includes a segment that, if a candidate did it in an interview, Aparna said **she would hire them on the spot**:

---

- ***If you want access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, Relay.app, Magic Patterns, Speechify, Bolt.new and Mobbin - **[become an annual subscriber](https://www.news.aakashg.com/account) ($150), and grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*
- ***If you want access to my AI PM customizations** - [PM OS](http://l.threads.com/?u=https%3A%2F%2Fwww.news.aakashg.com%2Fp%2Fpm-os&e=AT3OpE6P_HWG7KYcTl7xmfJz8h5zD8r-frJ3BkELyP3DYU58vBRyaMu95EaIbAjHMK36o_aZMzrCeGtw4SDHYwhZVyucVSaW1gqpGFsZrI6GBstPgR1InkhqtfU1niMfNeO455rFAhLe), [Job Search OS](https://www.news.aakashg.com/p/job-search-os), and [Prompt Library](https://www.news.aakashg.com/p/pm-prompt-library) - **[become a founding subscriber](https://www.news.aakashg.com/account) ($250)**.*

---

## Newsletter Deep Dive

*I’ve put together the complete guide for running evals in Claude Code.*

1. Evals don’t have to take forever and be hard
2. Step-by-step, how to run Claude Code evals
3. How to build a self improving loop
4. The new PM operating system

---

*Save this. A 3-step playbook on how to run [Claude Code](https://www.youtube.com/watch?v=4nthc76rSl8) [evals](https://www.news.aakashg.com/p/ai-evals) with exact commands.*

![](https://substackcdn.com/image/fetch/$s_!XRQd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6121e5fa-7e7a-4074-a23d-ef3dc88c3a05_2160x2260.png)

---

## 1\. Evals don’t have to take forever and be hard

In the past, I’ve [taught you the ways of Hamel Husain and Shreya Shankar](https://www.news.aakashg.com/p/ai-evals) who said that you need to look at the traces yourself, categorize them yourself.

In practice, what this means is **a lot of PMs skip evals** because it takes too long.

That’s a mistake. You can actually use Claude Code to do all those steps.

Here is what changed.

![](https://substackcdn.com/image/fetch/$s_!FlKK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef953f25-a771-4b43-9c06-e6f707d77e1d_2160x2260.png)

#### The old assumption - Evals need human-led error analysis

The old model assumed you had to be the one reading every trace. You needed to understand what went wrong before you could write an eval that tests for it. That meant the eval quality was capped by how much time you had.

That assumption made sense when models were weaker. It does not hold the same way anymore.

#### The new reality - Claude can suggest your first eval

When I asked Aparna, she said:

> *“I think it’s okay to start with Claude suggesting what a good suggestion of an eval could be. These models have gotten so good. Having it go through and look at your answers and suggest, that probably is something you should flag and look at. I would trust it. I would trust it as a first pass.”*

This is not about replacing rigorous eval work. Hamel and Shreya’s methods still produce the most calibrated evals over time. But you do not need to start there. Claude gives you a working v0 in minutes. That v0 gets you data. That data gets you something to actually improve.

Aparna demoed “vibe based evals” using Claude Code. Here’s how it works.

---

## 2\. Step-by-step, how to run Claude Code evals

You have an agent running. It is producing output. You have no idea if that output is accurate or just confident looking.

Here is exactly how to change that in one session.

#### Step 1 - Install the Arize skills into Claude Code

Open Claude Code. Run one command:

npx skills add Arize-ai/arize-skills

![](https://substackcdn.com/image/fetch/$s_!A2-I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2772d81e-bd83-4b1c-9d50-8bc4cd46b741_1142x740.png)

You can see all the skills added to Claude Code.

Claude Code now has access to instrumentation, eval suggestion, and improvement skills, you do not need to write any eval code yourself. You just ask Claude Code in plain English what you want. It calls the right skill for the job automatically.

The instrumentation skill is the first one you need. It looks at your codebase, identifies every LLM call and tool call, and wires them to Arize for tracing.

#### Step 2 - Ask Claude to suggest an eval

Once you have traces, ask:

Can you suggest a good eval for my agent?

![](https://substackcdn.com/image/fetch/$s_!IbLs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa926d3cd-3fe6-40eb-b5b6-1e98440c7ecc_2076x576.png)

Claude looks across your traces and returns candidates. In Aparna’s live demo it surfaced three:

- **Report groundedness.** Do the issues cited in the final PM report actually exist in the source data?
- **Priority alignment.** Does the P0/P1 ranking in the report match the highest-scored issues?
- **Report actionability.** Is the output something a PM can act on the same day?

Good starting point. But these are output level evals. You want to go one layer deeper.

#### Step 3 - Get specific about what you actually care about

Ask something more targeted:

Can you help me build an eval to evaluate if each issue’s priority is actually scored correctly?

Claude runs this across your spans. In the demo it flagged four failure categories: bug priority scoring, feature request scoring, legacy scoring system conflicts, and low priority edge cases.

Now you have something real. Specific categories of failure, with specific spans attached. That is what you need to improve the agent systematically.

*You cannot fix what you cannot name. The eval names it for you.*

---

## 3\. How to build a self improvement loop

Your eval is running. It is flagging failures. The natural next question is: now what?

Most PMs stop at the eval. They have the signal. They do not build the system that acts on it. That is the difference between a PM who runs evals and a PM who has a self-improving agent.

#### The loop - three moves, on a schedule

The loop is not complicated. It is three moves that run automatically on a cadence you set.

**Move 1 - Fetch everything the eval flagged as wrong.** Claude pulls every span from the last cycle where the priority accuracy eval fired.

**Move 2 - Find the pattern.** Claude groups those failures by category. Bugs being underweighted. Long feature requests getting inflated scores. Edge cases involving third party integrations always landing wrong. The categories tell you where the agent’s logic is broken.

**Move 3 - Propose a fix.** Claude suggests a specific prompt change or scoring adjustment that would address the most common failure category. A concrete edit you can review and approve.

![](https://substackcdn.com/image/fetch/$s_!i4Iv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d26f2f2-9c91-47f2-afeb-8562cc7b8463_2160x2260.png)

To set this on a schedule, ask Claude:

Can you run this in a loop using the Claude loop skill?

Claude spins up the equivalent of a cron job. Every day, or every week, your choice, the loop runs. It fetches failures, groups them, proposes a fix, and waits for you.

#### The human stays in the middle, always

This is the part that gets skipped in the excitement of automation. The loop is an accelerator. It is not a replacement for your judgment.

Eval changes need your sign-off before they run. Agent changes need your sign-off before they ship. The loop proposes. You approve. That is the design.

Aparna put it cleanly:

> “Get data in, get an eval set up, give it criticism and let it go run on a loop.”

The criticism is still yours. The speed is Claude’s.

#### What compounds and what does not

The teams that build this loop are getting smarter with every cycle. Each round of failures produces better calibrated evals. Better evals produce more accurate agents. More accurate agents produce fewer failures. The signal to noise ratio improves over time.

*The teams that skip the loop keep starting from the same baseline every sprint.*

---

## 4\. The new PM operating system

Step back from the mechanics for a second.

What you just learned is not a new feature to add to your existing workflow. It is a different operating system for how you do the job.

#### What the old operating system looked like

Monday morning. Open [Linear](https://www.news.aakashg.com/p/how-linear-grows). Read 40 new issues. Mentally rank them. Write a summary for standup. Two hours gone before you have typed a single Slack message.

Thursday. Pull up Gong. Watch three customer calls. Try to find the pattern. Write a themes doc that gets skimmed in a meeting and never opened again.

That cycle has a ceiling. There are only so many issues you can read. Only so many calls you can watch. Only so many sprints in a quarter.

#### What the new operating system looks like

The new operating system runs differently. Your agent already ran overnight. It pulled the latest issues, scored them by severity, recency, and reaction count, and wrote the PM report. It is sitting in your repo when you open your laptop.

Your job is a five-minute scan. Do you agree with the priorities? When you disagree, that disagreement is your next eval.

![](https://substackcdn.com/image/fetch/$s_!msb5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d6c3a60-7e75-4517-82ea-884f1a7fce0e_2160x2260.png)

As Aparna said:

> *“If you are doing things the same way you were doing them last year, you have not caught up yet.”*

That’s it for today. If you have any doubts, Aparna demoed the full process in the episode. Run the simple commands shared above. Watch Claude Code vibe it.

*See you in the next episode.*

---

## Where to find Aparna Dhinakaran

- [LinkedIn](https://www.linkedin.com/in/aparnadhinakaran/)
- [Arize](https://arize.com/?utm_source=aakashgupta&utm_medium=newsletter&utm_campaign=arize_sponsor_ai)
- [X](https://x.com/aparnadhinak)

---

POLL

### What did you think of today’s post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

## Related content

**Podcasts:**

1. [AI Evals with Hamel Husain and Shreya Shankar](https://open.spotify.com/episode/08RmC7UfmbJuGCJmoGmNSH)
2. [Evals are the new PRD with Ankur Goyal](https://podcasts.apple.com/us/podcast/evals-are-the-new-prd-here-is-the-playbook-with-the/id1763555775?i=1000756385737)
3. [AI PM Crash Course with Aman Khan](https://youtu.be/Ej4pBDaHspk?si=mVs_Ru3I-pKNnmnT)

**Newsletters:**

1. [AI Evals for PMs: Everything You Need to Know to Get Started in 2026](https://www.news.aakashg.com/p/ai-evals)
2. [Your Complete AI PM Course & Career Roadmaps](https://www.news.aakashg.com/p/ai-pm-learning-roadmap)
3. [AI PM’s Guide to LLM Judges](https://www.news.aakashg.com/p/ai-pm-llm-judge)

---

*PS. Please subscribe on [YouTube](https://www.youtube.com/@growproduct?sub_confirmation=1) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/aparna-dhinakaran-podcast) on 2026-05-23T14:45:07-04:00*
