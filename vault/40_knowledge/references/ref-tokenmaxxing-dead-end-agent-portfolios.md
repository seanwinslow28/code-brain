---
title: "Tokenmaxxing Is a Dead End. Learn to Manage Agent Portfolios Instead."
source: "https://substack.com/home/post/p-196783319"
author:
  - "[[Daniel Williams]]"
published: 2026-05-20
created: 2026-06-02
description: "Tokenmaxxing is the data warehouse mistake at a different layer. The fix isn’t compressing tokens. It’s deciding which agents in your portfolio earn their keep."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery, product-management]
ai-context: "Daniel Williams reframes token optimization ('tokenmaxxing') as the 1990s data-warehouse mistake repeated — the fix is agent rationalization: scoring each agent in the portfolio by revenue/cost/efficiency value, killing the bottom third, and resourcing the top, before any prompt compression is legitimate."
---
A senior engineer I know showed me his approach to prompt optimization a couple of weeks ago. Multiple columns, months of A/B tests, average tokens per call broken out by tool path. He had cut his agent’s token usage by 30+ percent. I asked him whether the work the agent produced had gotten better. He didn’t have a column for that. He didn’t have a column for whether the automation needed to exist. He had a column for tokens because tokens are denominated in dollars. The dashboard his team built had a slot for them, and this is what the executives at his company care about.

Tokenmaxxing is being sold to every CFO in the country as a discipline. It is the data warehouse mistake that we already learned, painfully, through the late 1990s and into the 2000s, that volume metrics on infrastructure whose underlying value isn’t understood produce confidently wrong decisions and a decade of compression projects on data that should have been deleted. The lesson took fifteen years and several billion dollars of write-offs to absorb then. AI tooling is reproducing it now, and the people building the dashboards have no apparent memory of how the last version of this story ended.

The discipline that worked then is the discipline that will work now: rationalization, not optimization. **Agent rationalization** means deciding, at the portfolio level, which agents are producing value and which to kill. Compressing prompts on automations that shouldn’t exist is the mistake being made now.

![](https://substackcdn.com/image/fetch/$s_!siYT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a9c8587-c728-4a3e-b649-0d8edd677b77_1920x1080.png)

## The Last Time We Did This

Through the late 1990s, large enterprises built data warehouses the way large enterprises now build agent platforms in 2025: every team got a pipeline, every system got a feed, every report became a job, and the storage line item compounded quarter over quarter. By the mid-2000s, the CFO noticed. The first response was technical. Compression ratios, columnar formats, tiered storage, partition strategies. Vendors sold optimization. Consultants sold optimization. The cost curve bent for about eighteen months and then resumed climbing, because the underlying problem wasn’t storage efficiency. The underlying problem was that nobody knew which of those pipelines was producing decisions and which was producing dust. [Forrester eventually quantified the gap](https://www.inc.com/jeff-barrett/misusing-data-could-be-costing-your-business-heres-how.html): 60 to 73 percent of enterprise data goes unused for analytics, regardless of how much storage gets optimized.

What eventually broke the cycle were master data management and data rationalization, both euphemisms for deletion. The companies that did this honestly killed 40 to 60 percent of pipelines and reports. The work that mattered ran faster and got governed better. The work that didn’t matter went away. The savings compounded because they were structural rather than technical. The companies that stayed in compression mode spent another ten years optimizing infrastructure carrying low-value freight, and the line item never came down.

Rationalization, done honestly, surfaces underinvestment as often as it surfaces waste. I ran one such engagement at a top-20 global pension fund. The work canceled hundreds of thousands of dollars a year in data licensing the fund didn’t need and identified over $10 million in new and expanded data products and services worth investing in. The client hired me to find savings. They left with something more valuable: a clear-eyed map of where they had been under-investing in assets that actually mattered.

Token spend has the same shape, on a faster clock. Any metric that captures volume of activity on infrastructure whose business value is unclear will produce optimization projects, and those projects will be confidently executed. They will not move the bottom line because the value problem has always been upstream of the volume problem. The vendor ecosystem is already lining up to sell you the optimization layer.

## “Tokenmaxxing”

Tokenmaxxing is a meme describing the cluster of practices that confuse the meter for the work. Prompt golf, where engineers spend a day shaving 800 tokens off a system prompt that runs in an automation nobody has audited for outcomes in six months. Compression schemes that pre-summarize context before it reaches the model, on the theory that if the model produces similar output for less input, the optimization is free. Agent harness comparisons that report token efficiency to 4 significant digits and output quality as a sentence. Vendor pitches denominated in dollars per million tokens, as if the unit being purchased were tokens rather than work products. The token-spend dashboard at the CFO level, which is easier to build than a value framework, is therefore the artifact that gets reviewed in the QBR.

Each of these practices shares a particular tell: teams have stopped asking what the agent is for. They have moved to asking how to do whatever it currently does for less. That move is socially comfortable. It produces a number that goes down quarter over quarter, it generates artifacts to put in the deck, and it doesn’t require any of the hard portfolio conversations about whether the automation should exist. It is also, almost without exception, in the wrong layer of the stack.

When a team tells me they cut token usage by a third, the question I ask back is which automations they killed. The answer is almost always none. They have made the existing portfolio more efficient. The portfolio still contains the same number of agents producing the same questionable work product, and the dashboard now reports the spend as down. Five quarters of that and the cost curve resumes climbing, because the underlying portfolio is still wrong.

The buying organization is not the beneficiary of any of this. Tokenmaxxing produces no shipped product, no decision improvement, and no customer value of any kind. What it produces is more token consumption, more sophisticated optimization stacks, and more reasons to keep buying inference. The parties whose interests the practice actually serves are the frontier labs billing by the token, the GPU and TPU manufacturers selling the substrate, and the data centers leasing rack space. Inside the company, paying the bills, tokenmaxxing is a discipline whose primary externality is keeping the meter running. The vendor ecosystem will tell you it’s the responsible thing to do, because for them, it is.

## What Agent Rationalization Actually Looks Like

This discipline doesn’t have a name in the current discourse. Search for AI agent governance, and you find runtime concerns: identity, kill switches, policy enforcement, and reliance drills. Search for AI portfolio rationalization, and you find vendors offering AI agents as a tool to rationalize legacy application portfolios, which is a different problem entirely. Search for agent decision frameworks, and you find guidance on selecting the right agent for a use case. The strategic question of which agents in your existing AI portfolio earn their keep, and which ones don’t, isn’t being asked. Call it **“agent rationalization.”**

The strategic move is portfolio review, not prompt engineering. The deliverable is a list of automations, agent workflows, and recurring AI-touched processes, scored by the business value they produce rather than the tokens they consume.

A professor I had in grad school taught us a framework I have used ever since. Every project a company invests in has to fit one of three buckets: **generate revenue**, **reduce costs**, or **increase efficiency**. If it does not fit cleanly into one of those three, the question is, why are we doing this? Apply it to your AI portfolio, and the answers come quickly. An agent that drafts proposals that actually win deals fits the revenue bucket. An agent that handles a class of tickets that used to require headcount fits the cost bucket. An agent that compresses a review cycle from a week to a day fits the efficiency bucket. An agent that produces an artifact nobody files, summarizes meetings nobody acts on, or runs every night because someone built it once and forgot fits none of them. That last category is where most token spending ends up when nobody is asking the question.

The bottom third of the portfolio gets retired. The middle gets re-evaluated against a sharper version of the original brief. The top gets resourced more aggressively than current spend, because the constraint on those agents is judgment and design, not token budget. Most rationalizations I have run have produced both directions of recommendation in the same deliverable: cuts to the work that wasn’t earning its keep, and increased investment in the work that was producing real value but was under-resourced. The same logic applies to agents. Useless AI initiatives don’t survive a rationalization. Value-generating ones come out the other side with more resources, not fewer. Token rationalization is a sub-discipline of agent rationalization, applied to the portfolio that survived the test. The compression and prompt optimization completed at that point are legitimate work. Done before the portfolio review, they are tokenmaxxing under a different name.

The senior person doing this work has to be willing to say which automations are not pulling their weight, which is socially harder than saying which prompts can be compressed. The shift the work asks of you is from someone who manages AI inputs to someone who governs an AI portfolio. That’s the discipline that scales with seniority, and it’s not the one a token-spend dashboard will ever measure. Most organizations will choose the easier framing because it produces clean numbers without making anyone defend their pet workflow. The companies that take the harder path will end up with smaller, sharper agent portfolios and better cost discipline three years out, the same way the companies that took the harder path on data ended up with smaller, sharper data estates.

The senior technical professionals reading this newsletter are who this work falls to, because nobody on the prompt-optimization track is going to surface it. The token-spend dashboard is being installed in your finance org right now, or it will be by the end of the year. The question to bring to the next portfolio review is not how the tokens are trending. It’s which of these agents produced work in the last quarter that someone actually used, and what would happen if you turned the others off tomorrow. That conversation is harder to have than a compression ratio, and it’s the only one that ends in a different cost curve.

If you run an AI portfolio of any size, do this one exercise this quarter: list every recurring agentic workflow your organization runs, and for each one, name the decision it informs or the artifact it produces. The ones you can’t name go on a list. The list is your starting point.

---

Daniel Williams advises clients about AI tools, strategy, and human resilience at [dewilliams.co](https://dewilliams.co/).

---

[Claude Code for Non-Coders](https://claudecodefornoncoders.substack.com/) publishes on Tuesdays and Thursdays. If you found this useful, share it with someone who’s about to install a token-spend dashboard.

---
*Clipped from [substack.com](https://substack.com/home/post/p-196783319) on 2026-06-02T11:09:24-04:00*
