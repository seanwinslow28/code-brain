---
title: "You're Loading 66,000 Tokens of Plugins Before You Even Type. That's Why Your Limit Disappears."
source: "https://natesnewsletter.substack.com/p/your-claude-sessions-cost-10x-what?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-04-01
created: 2026-05-17
description: "Watch now | Token management is a indicator of AI fluency. Here's how to get better at it."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
I recently saw a production AI pipeline that ingests multiple long-form conversations per user, runs analysis across dozens of dimensions, and generates fully personalized output. All on the most expensive models money can buy. The cost per user? Less than a quarter. Most of you are spending more than that asking Claude what to have for dinner.

That number should bother you — not because frontier AI is expensive, but because it isn’t. Frontier AI running on the most expensive models available costs pennies when you know what you’re doing. The problem is that most people don’t know what they’re doing. They’re burning 5x, 10x, sometimes 20x what they should on the exact same work, and they think that’s just what AI costs.

The models aren’t expensive. Your habits are expensive.

And with Claude usage limits dominating every AI community on the internet, those habits are finally catching up with people. So I want to be direct about what I’m actually seeing.

**Here’s what’s inside:**

- **The ChatGPT migration problem.** Why habits from ChatGPT are catastrophically expensive on Claude, and the single fix that changes everything.
- **What I’m actually seeing.** The four levels of token waste, from rookie to “advanced,” with real numbers.
- **The math that should scare you.** Clean vs. sloppy sessions, Mythos pricing implications, and why the gap keeps widening.
- **A diagnostic.** Six questions to find out if you’re the problem.
- **What we’re building.** The Stupid Button, KISS Commandments, and the Heavy File Ingestion skill already in the OB1 repo.

The usage limit crisis started getting loud about a week ago. Some of it is real infrastructure strain — but some of it is fixable.

## LINK: Grab the Prompts

Token waste shows up in patterns, not one-off mistakes, which means you can’t fix it with a pep talk. You fix it with executable diagnostics that look at your actual habits and tell you what’s wrong.

The prompt kit below contains the **Stupid Button** — the blunt diagnostic from the article built as a copy-paste prompt — plus four supporting tools for the specific fixes it surfaces: rescuing bloated conversations without losing your work, routing tasks to the right model tier, auditing agent architectures against the KISS commandments, and translating your typical session into actual token economics so you can see where your budget went. These aren’t generic “be mindful about tokens” prompts. They’re built around the failure modes in this article, the ones I see dozens of times a week when people ask me why they’re hitting their limits.

Start with the Stupid Button, let it identify your waste patterns, then use whichever follow-up prompts match what it finds. And if you’re in the “rookies bleeding out on document ingestion” category: the **[Heavy File Ingestion](https://github.com/NateBJones-Projects/OB1/tree/main/skills/heavy-file-ingestion)** (link) skill in the continuously growing **[OB1 repo](https://github.com/NateBJones-Projects/OB1)** (link) stops that leak at the infrastructure layer — converts files to markdown on ingest and creates lightweight indexes so you never pay the raw-PDF penalty again.

## The usage limit crisis

If you’ve been anywhere near the Claude ecosystem in the last seven days, you’ve seen the meltdown. Anthropic confirmed that peak-hour session limits are now tighter, and your five-hour session window burns faster between 5am and 11am Pacific on weekdays. Pro subscribers are getting hit hardest. Even some Max users paying $100 to $200/month are reporting their meters jumping from 50% to 100% on a single prompt, and one Max 20x subscriber watched their allotment evaporate in 90 minutes doing the same work that used to last all day.

Reddit is furious. PCWorld, TechRadar, The Register, PYMNTS, MacRumors — all running stories about users hitting walls. Anthropic says about 7% of users are newly affected. The vibes are bad.

Some of this is real infrastructure constraint. Millions of new users showed up after Anthropic’s Pentagon standoff, the 1M token context window just went generally available at standard pricing with no more long-context surcharge, and agentic workflows through Claude Code and Cowork are burning compute at rates that flat-rate subscriptions were never designed to absorb. Anthropic is capacity-constrained. That part is real.

But nobody in the outrage cycle is asking the harder question, which is whether most of the people hitting their limits are doing it to themselves.

## The ChatGPT migration problem

I need to single this out because it’s the biggest driver of the complaints I’m seeing.

A massive wave of users just migrated from ChatGPT to Claude. Some came because of the Pentagon thing, some came because Claude is better at the work they do, and it doesn’t really matter why. What matters is they brought their ChatGPT habits with them, and those habits are catastrophically expensive on Claude.

ChatGPT and Claude handle conversation context in fundamentally different ways. ChatGPT manages long conversations by progressively compressing or dropping older messages to stay within limits. You lose history, but you never pay an escalating cost per message. You can let a thread run for 100 turns and your 100th message costs roughly the same as your 10th, because ChatGPT has already shed the first 80.

Claude doesn’t do this. Claude tries to keep your *entire* conversation in its context window. That enormous 1M token window Anthropic just made free at standard pricing? It means Claude *can* hold a massive conversation, and it will try. Every new message you send resubmits everything before it — every document you loaded, every response Claude generated, every tangent you explored.

This means the cost per turn in a Claude conversation escalates as the conversation grows, and not linearly. A message at turn 5 might cost around 2,000 tokens. By turn 30, the accumulated context could push that to 40,000 or more. At turn 50, you could be looking at 80,000 tokens per exchange. That’s the math of maintaining full conversational context, and I want to be careful not to overstate the precision of those numbers — they’re illustrative, not measured — but the direction is unambiguous. Every turn costs more than the last.

If you’re coming from ChatGPT and you’re used to letting threads run to 50, 60, 80 turns without thinking about it, you just discovered why you’re hitting your Claude limit in an hour. You’re paying the accumulated weight of every previous exchange on every new message, and Claude’s generous context window is letting you dig yourself deeper into that hole without any resistance.

The fix is simple but requires a habit change: **start new conversations constantly.** When you shift topics, open a fresh chat. When a conversation gets past 15 to 20 turns, copy the relevant context into a new chat and continue there. Think of Claude conversations as disposable work sessions, not persistent threads. This single habit change will do more for your usage limits than anything else in this article.

## What I’m actually seeing

I review AI workflows constantly — dozens a week. Architectures, agent harnesses, Claude Desktop setups, Cowork environments. And the token waste I see is so consistent, so patterned, and so fixable that I’ve started to think of token burn rate as the single most revealing metric of someone’s actual AI fluency. Not how many tools they use, not how many agents they’ve deployed. How many tokens they burn relative to what they accomplish.

Here’s what the spectrum looks like.

**The rookies are bleeding out on document ingestion.** This one drives me insane because it’s so easy to fix. A brand-new Claude Desktop user drags three PDFs into a conversation, maybe 1,500 words each. Just 4,500 words of text. They say “summarize these” and Claude processes the raw PDFs with all the formatting overhead: headers, footers, embedded fonts, layout metadata, the entire binary structure decoded into tokens.

Those 4,500 words of content could cost tens of thousands of tokens to ingest as PDFs. If they’d asked Claude to convert them to markdown first — which takes ten seconds with code execution — the same content would cost 5,000 to 6,000 tokens. That’s potentially a 10x penalty or worse for not knowing a single trick. And these users do it every session, multiple times a day, and then wonder why they hit their limit before lunch.

The waste compounds, too, because once those tokens are in your conversation history, they’re being resubmitted on every subsequent turn. By turn 10, you’ve effectively paid for those PDFs ten times. By turn 20, twenty times. The rookie who converted to markdown first is paying for 5K tokens per turn instead of tens of thousands. The gap widens with every message.

**The intermediate users are killing themselves with conversation sprawl.** I covered the mechanics above, but a specific case illustrates how invisible this problem is.

Someone showed me a conversation last week. 62 turns about a product launch. They’d loaded some reference docs early on, asked a bunch of planning questions, iterated on copy, went back and forth on positioning — normal knowledge work. By the end, each exchange was consuming roughly 85,000 tokens. They hit their limit in what felt like five minutes of actual work, and their reaction was “Claude is broken.”

Claude wasn’t broken. Claude was faithfully carrying 62 turns of accumulated context because they never started a fresh conversation. If they’d broken that into four 15-turn conversations, copying forward only the relevant decisions and outputs each time, the same work would have consumed roughly one-quarter of the tokens. Same output, same quality, 75% less burn.

**The plugin hoarders are paying a boot tax they don’t know exists.** One of our community members ran `/context` in Claude Code last week and discovered he was loading **66,000 tokens in every single session before doing anything.** Before a single prompt, before a single line of code — just the overhead of skills, plugins, and custom frontmatter he’d accumulated was eating over half his context window on boot.

He halved it by removing 36 plugins and cleaning up skill frontmatter. He’d been driving with the parking brake on. And he’s a technical user who builds things. Imagine what the average Claude Desktop user’s overhead looks like if they’ve been installing every shiny plugin they see recommended on Twitter.

**The advanced users are the most expensive disaster,** and it’s worth pausing on why because it’s counterintuitive. The self-described “context engineers” building agentic systems — you’d think they’d be the most disciplined. They’re often the worst, because the waste is hidden behind infrastructure.

The pattern looks like this: an agent harness that passes 200K tokens of unindexed context on every call. A system prompt that’s 15K tokens long because nobody pruned it after the fifth iteration. Reference documents dumped raw into every agent’s context window instead of indexed and retrieved on demand. No prompt caching, so the same stable context — system prompt, tool definitions, reference material — gets billed at full price on every single API call.

These people are spending $50 to $100/day on workflows that should cost $10 to $15. And they think that’s what AI costs.

---

## The math that should scare you

I want to make this concrete, because I think the abstract version of “you’re wasting tokens” doesn’t land until you see the actual numbers side by side.

**Sloppy session on Opus 4.6:** You feed raw PDFs into context (tens of thousands of tokens vs 5K), let a conversation sprawl to 30+ turns (escalating cost per turn), use Opus for everything including reformatting and proofreading. Over a five-hour session: roughly 800K to 1M input tokens, 150K to 200K output tokens including thinking. At $5/$25 per million, that’s $8 to $10 worth of compute.

**Clean session, same work:** Convert documents to markdown first, start fresh conversations every 10 to 15 turns, use Opus for reasoning and Sonnet for execution and Haiku for polish, scope context to what’s needed. Over the same five hours: 100K to 150K input tokens, 50K to 80K output. Blended rates across models. **About a dollar.**

Same output. Same quality of work. An 8 to 10x difference in cost. Scale it across a week and the sloppy user burns $40 to $50 in compute while the clean user burns $5 to $7. Across a 10-person team on API, that’s $2,000/month vs $250/month. For subscription users, it’s the difference between hitting your limit daily and forgetting limits exist.

Now here’s where it gets serious.

Anthropic’s Mythos model leaked on March 26, accidentally left in a publicly searchable data store along with close to 3,000 unpublished assets, because apparently the company building the world’s most advanced AI models configured their CMS with the security posture of a shared Google Doc. Mythos sits in a new tier called “Capybara,” above Opus. Anthropic calls it “a step change” in capabilities, dramatically better on coding, reasoning, and cybersecurity benchmarks. It’s the most capable thing they’ve ever built.

It’s also expensive enough that they’ve described it as not ready for general availability partly due to cost. A new pricing tier *above* Opus almost certainly means we’re looking at something north of $5/$25 per million tokens. Potentially well north. The leaked draft describes Capybara as “larger and more intelligent than our Opus models,” and “more expensive” — a new ceiling on the pricing structure, not a replacement.

The problem with token waste is that **it scales with the price of intelligence.** If you’re currently wasting 10x on Opus at $5/M input, that’s $45/M in unnecessary burn. When the next frontier model costs $15/M input, the same habits waste $135/M. Your sloppiness gets more expensive every time the models get better.

And the models will keep getting better. Every quarter, every release. The trajectory is unambiguous. The people who learn token discipline now will be the ones running Mythos-class models next quarter. Everyone else will be priced out of the frontier by their own habits.

---

## The part where you find out it’s you

I’ve been saying for weeks that what the industry actually needs is a stupid button. Not a gentle guide — a blunt diagnostic that looks at your actual behavior and tells you where you’re being dumb. We’re building one. But until it ships, here’s the manual version, and I’d encourage you to be honest with yourself, because the most expensive habit is the one you’ve convinced yourself isn’t a problem.

The first thing to check is whether you’re feeding Claude raw PDFs and images when all you actually need is the text. If you are, you’re paying a 10 to 20x markup on every document interaction and you probably don’t even realize it. Converting to markdown first takes Claude ten seconds with code execution. And when it writes that conversion code, save it — don’t let it regenerate a fresh script every time, because that regeneration itself costs tokens you didn’t need to spend.

The second thing — and this is the one that catches most people — is conversation length. When was the last time you started a fresh conversation? If you can’t remember, you’re carrying the context debt of potentially dozens of turns on every new message. Your most recent messages are the most expensive ones you’ve sent all day. Start new conversations aggressively. Copy over only what matters.

Then there’s model routing, and I want to be careful here because the advice isn’t “never use Opus.” Opus is your architect. It plans, reasons, makes judgment calls on hard problems. But it should not be reformatting your tables, proofreading your emails, or doing any task that doesn’t require real reasoning. Sonnet handles execution. Haiku handles cleanup. Switching models within a workflow isn’t a compromise — it’s the tell of someone who actually understands what they’re paying for.

There’s also the question of what’s loading in your context before you even type. Run `/context` in Claude Code and look at the number. If you’ve been accumulating skills and plugins without auditing them, you could be loading tens of thousands of tokens before your first prompt. Trim ruthlessly. Every token of system prompt overhead compounds across every turn of every conversation.

For API builders specifically: are you caching your stable context? Prompt caching gives you a 90% discount on repeated content. Cache hits on Opus cost $0.50/M vs $5/M standard. If your system prompt, tool definitions, and reference documents aren’t cached, you’re paying ten dollars for every dollar of stable context, and this should be the first thing you set up.

And finally — this one sounds strange until you see the numbers — are you letting Claude do web research the expensive way? A builder I know personally built a Claude Code plugin that routes all web searches through Perplexity instead of Claude’s native search. In our testing: 5x faster (6.8 seconds vs 36.2 seconds average), structured citations, and the number that matters: **10,000 to 50,000 tokens saved per search** because Claude doesn’t have to ingest and process raw web results in its context window. Over a research-heavy session, this single plugin saves more tokens than most people spend on their actual work. It’s **[open-source](https://github.com/justfinethanku/LEJ-Perplexity-Powered-Search-for-Claude)**.

If three or more of those hit home, you’re probably burning 5 to 10x what you need to. Which means your usage limit complaints aren’t really about Anthropic’s capacity. They’re about your workflow.

## What we’re building to fix this

Writing about token discipline helps, but tools help more, and I’ve learned enough by now to know that any habit you have to consciously maintain is a habit that eventually breaks.

**The stupid button (token burn tester)** exists at three levels, because the problem exists at three levels of sophistication. Level 1 is a prompt — something you run against your recent conversations that identifies the specific wasteful patterns: feeding raw documents, conversation sprawl, model misuse, redundant context loading. It looks at your actual habits and tells you what to fix first. Anyone can use it, any plan, no setup required. We’re targeting the Claude Desktop user who just wants to know “why do I keep hitting my limit?” and needs a concrete answer.

Level 2 is a skill — an invokable tool that audits your Claude Code or Desktop environment in real time. It measures your per-session token overhead, flags system prompt bloat, checks your plugin and skill loading, and gives you a before-and-after when you make changes. Think of it as a linter for your AI workflow. You wouldn’t ship code without running a linter. Why would you run an AI workflow without checking your token overhead?

Level 3 is the infrastructure layer — guardrails that sit directly on your knowledge store (your OpenBrain, your MCP servers, your reference context) so you stop burning tokens on *input.* Automatic markdown conversion before documents enter context, index-first retrieval instead of dump-and-search, context scoping that enforces minimum-viable-context per query. This is where token management stops being a discipline you have to maintain and becomes infrastructure that maintains itself. You shouldn’t have to remember to do the right thing every time. The system should make the wrong thing hard.

**The KISS commandments for agents** came from a pattern I kept noticing — people asking me “is my agent architecture stupid?” dozens of times a week, and the answer being yes for the same five reasons almost every time. We’re codifying it into something people can use as a pre-deploy checklist.

First, index your references. If an agent is getting raw documents instead of relevant chunks, you’ve already failed. The entire point of retrieval is to scope what the model sees to what it actually needs. Dumping a full document set into every agent call isn’t “giving the agent context” — it’s making the agent do retrieval work you should have done at the infrastructure layer.

Second, prepare context for consumption. Pre-process, pre-summarize, pre-chunk. A reference document should arrive in an agent’s context window ready to be *used*, not ready to be *read*. If the model’s first 5,000 tokens of reasoning are spent understanding the format of your input, you’ve wasted those tokens.

Third, cache your stable context. System prompts, tool definitions, persona instructions, reference material that doesn’t change between calls — all of it should be cached. At a 90% discount on cache hits, this is the lowest-effort, highest-impact cost reduction available. If you’re making thousands of agent calls a day and not caching, do the math on what you’re throwing away.

Fourth, scope each agent’s context to the minimum it needs. A planning agent doesn’t need your full codebase. An editing agent doesn’t need your project roadmap. Passing everything to every agent is architectural laziness, and it has a direct cost — both in tokens burned and in degraded agent performance. Models perform worse when they’re drowning in irrelevant context. Scoping isn’t just about cost. It’s about quality.

Fifth, measure what you burn. If you don’t know your per-call token cost, you’re flying blind. Instrument your agent calls. Track input tokens, output tokens, thinking tokens, cache hit rates. You can’t improve what you don’t measure, and most teams building agentic systems have literally no visibility into their per-call economics.

Five rules. Most agentic architectures I review violate at least three of them. Following all five typically cuts costs by 5 to 10x and — this is the part people don’t expect — makes the agents *perform better* because they’re not drowning in irrelevant context.

## The real point

There’s a cultural problem underneath all of this, and I’ve been thinking about why it’s so persistent.

Somewhere along the way, people started treating high token consumption as a badge. Burning through your rate limit fast means you’re doing important work. Running up a big API bill means you’re building something serious. Token count became a vanity metric — the AI equivalent of “I’m so busy.”

It’s the opposite. High token burn is almost always evidence that you’re making the model *process* when you should be making it *think.* You’re paying Claude to ingest, parse, and reorganize information that should have been prepared before the prompt was sent. Processing is expensive and adds no intelligence. Thinking — when the context is clean, scoped, and pre-digested — is cheap and is where all the value lives.

Pennies per user. That’s what a complex, multi-step AI pipeline costs on the most expensive models available when the token management is tight. Your mileage may vary depending on your use case and scale, but the order of magnitude is real. That number should radicalize you.

Token discipline is going to be one of those skills that separates people who use AI from people who are fluent in it. Not because it’s hard — it’s actually one of the easier things to fix once you see it. But because most people never look. They pay the bill, or they hit the limit, and they assume that’s just what AI costs. It isn’t. And the longer you wait to figure that out, the more expensive the lesson gets.

![](https://substackcdn.com/image/fetch/$s_!DbuK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef8a9bf5-708f-4894-bafa-42571151461f_1024x1024.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/your-claude-sessions-cost-10x-what?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-05-17T15:34:01-04:00*

YOUTUBE TRANSCRIPT

The next generation of models is likely to drop in the next one to two months. I'm talking about Claude Mythos. I'm talking about whatever Chad GPT drops next. I'm talking about the next Gemini model. They will be more expensive, a lot more expensive, because they're all trained on much more expensive chips, the GB300 series from NVIDIA,

and it's just going to get more expensive from there. The intelligence we're going to get, the ambient compute all around us that is essentially free intelligence, is going to be the dumber models. That's just how it is. If you want to use cutting-edge models, you have got to stop burning tokens and blaming the model.

And that is the theme for this video. If you're in a position where you're wondering how much token usage you have or how expensive your AI is or whether you're using too many tokens for your AI or how you can even measure that, how you can get better at it, that is what this is.

And that is going to be one of the most valuable skills on the planet. by the way, because you do not want to be in a position where you are putting $250,000 a year, a real number that Jensen Huang gave in a real interview for what he expects an

actual individual engineer to spend in a year on tokens. You don't want to be the person spending 250 grand on tokens you don't have to be spending on. You want to be smart. And I'm going to give you a specific example. This is a real-life example. A real person I know gave me permission to use this.

I recently saw a production AI pipeline that ingests multiple long-form conversations per user, runs an analysis across dozens of dimensions, and generates a fully personalized output, all on the most expensive models that money can buy. Not because the person wants to use expensive models, but because he tested it.

And what he found was that the better models produce the results he needs for this business. The cost per user, less than a quarter. Less than 25 cents per user for that. Most of us are spending more than we need to on AI. And this is a video about that.

You can be really smart, use really good cutting edge AI, And you can be intelligent with your token usage and not spend a ton of money. If you want to know what that's like, keep on watching because we're going to get into specific strategies.

And I'm going to show you what I built so that we can actually make this easier for everybody. So it's not just a guessing game anymore. The takeaway is that Frontier AI can be absurdly cheap when you know what you're doing. Essentially, the models are not expensive. It's your habits that cost a lot.

And with Claude usage limits dominating everything in the last week, I think it's worth having that conversation again. So let's get to it. I've made the case we can use our models better. What are the specific habits we can change? I want to name specific habits that I have seen in conversations with others, looking over shoulders,

reading GitHub repos, listening to conversations online. These are specific examples that are patterns I see over and over again. And the first one is the rookies, the folks who are new to cutting edge AI. You know what you bleed out on in tokens? you bleed out on document ingestion.

This one drives me crazy because it's so, so easy to fix. A brand new Claude desktop user might drag in three PDFs into a conversation that might be 1500 words each, which is just 4,500 words of text. It's not that long. And they say, summarize these and Claude processes the raw PDFs with all the formatting overhead

that goes with that. The headers, the footers, the embedded fonts, the layout metadata, and the entire binary structure gets encoded as tokens. And so the 4,500 words of content can become a hundred plus thousand tokens if you're not careful. All you have to do to avoid that is just think in terms of markdown.

If you just asked Claude, or frankly, go to any of a number of services on the internet that are free and say, please convert to Markdown, it will just do it, right? It will just take 10 seconds and convert to Markdown. And then you have a very clean set of content that's between four and 6,000 tokens.

And that's like saving you 20X on the memory. And this waste just compounds, right? Because once those 100,000 tokens are in your conversation history, they bounce back and forth and bounce back and forth and this is how you fill up your token window and you wonder how other people get so much done. Please, please, please,

if you're new to AI or if you've never thought about it, think about the file formats you're throwing because so many of these file formats are designed to be human readable. They're not designed to be AI readable. Think about the token efficiency of these file formats. And if you're wondering, well, how do I convert to Markdown?

I built something for you. Because all you have to do is just ingest a file. You hit transform and it just converts it back into Markdown. That's it. And we have a number of file types. We're adding more from the community all the time as part of the OpenBrain ecosystem.

It's just a plugin you can put in and it'll just convert it to Markdown. But That's not the only way. You can tell Claude to do it directly. You can also just directly do it on the internet with any of a number of free web services. Markdown conversion should not be gated.

It just, it's super easy to do. Tokens are designed to preserve everything in an original text. If you wanted to reason about the style of the PDF, fine, keep it. But 99% of the time, all you care about is the text. You just want it in Markdown. Please, please, please think about your file formats.

Next big mistake that people make, and this one comes a little bit after people tend to convert to Markdown and start to understand how some of these initial documents work. Please do not sprawl your conversations. If you were doing 20, 30,

40 turns on a conversation,

no AI was reinforcement learned, trained, or designed to handle that kind of sprawl. All you're doing is compressing the ratio of the conversation where the original instructions happened. And yes, the models are getting better and better and better at anchoring on and remembering those original instructions, even when they go through compression. But why make them suffer?

Why make yourself suffer by filling up the context window with cruft? Why waste tokens? Why not just ask for what you want upfront? And if you're gonna have an evolving exchange or evolving conversation, clearly mark it at the top as our goal here is to evolve and reach a conclusion together.

And then you have a light conversation that goes 20 or 30 turns and say, thank you, I've got a conclusion, please summarize this. And then you go and do real work. I see so many people trying to mix together modes, but AI is really designed for single turn, do a lot of heavy work more and more,

And in that context, you need to do the thinking in advance and bring that to the table. And if you need to think with AI, that should be in a separate chat, separate conversation. It might even be a separate model. It might be three separate models, and you're bringing all of that in.

I do that all the time. I'm like, okay, I want to look through what communities are thinking about AI on X. I'm going to go to Grok for that. Or I'm gonna go through and look at what earnings reports are saying about the state of AI and capital investment.

I'm gonna go and pipe that through chat GPT thinking mode and get a bunch of reports out on that. Or I'm gonna go through perplexity research and get a bunch of reports out on that. Now I'm gonna go and have a look at what some major blog posts have to say about a particular AI topic.

I'll just go to Claude Opus 4.6. We'll do a targeted web search. We'll go back through. We'll make sure we understand what we're looking at. None of that is intended to be a single answer, right? These are all evolving conversations. Once I get what I want out of each of these individual threads,

I can pull them together and say, okay, now I have a piece of work to do. Now I have something I actually need done and I have all the context needed. So you should have two modes here. You should have a mode where you are trying to gather information and a mode where

you are trying to focus and get work done. Do not mix the two together. That is how you burn tokens. That is how you confuse the AI. Your objective when you want the AI to do real work should be to be so clear that the AI needs to do nothing else.

And it just goes and gets the work done and comes back. It should be that clear. If you are an intermediate user and you are like, I know this stuff, Nate. Well, let me give you another tip you may not know. The people who are adding lots of plugins to their chat GPT or their cloud instances,

you are paying a tax every time you start a conversation because in the background, those are going to be loaded in and they're going to start to fill the context window. I know someone who shared with me that they are over 50,000 tokens in on a context

window before they type the first word because they actually load that many plugins and connectors. You don't need that much. You know what that's like? That is like walking in to a fully functional tool work. And the first thing you do instead of leaving the tools on the walls is you go and

get all the tools off and you lay them out on the workbench and you say, okay, now we're going to do, I don't know, we're going to do something. We're going to make a bench. Do you need all 200 tools in the workshop to make the bench? No, you probably need the right five. Think about that.

the next time you have an approach to tooling. Because so many people, we hear about this new plugin, we hear about this new connector, someone hypes it up, we say we need to add it, and we don't realize it's a silent tax for the rest of time, every time we have a conversation,

and it just adds that little bit. It adds 1,000 tokens, it adds 2,000 tokens, whatever it does, and it just adds it always. Do you want to pay that for the model? Maybe you should think more strategically about which plugins and connectors are really adding value for you, because they can.

tremendously valuable, but make sure you know which ones you really want. Because if you don't, then you're going to be looking at dozens of plugins that you don't really need that are supposed to add value, but just add a bunch of cruft, a bunch of junk into your context window and confuse the model and keep it from

doing good work and maybe confuse it as to which tools it's supposed to use. Now, I'm saving the most expensive and the most advanced users for last because this is where the leverage lies. If you are an advanced user, if you are someone who's like, send me to the GitHub repo. I can just do this myself.

Let me install OpenClaw on my Mac mini. I'm OK managing the gateway. I can be secure. This is for you. you have the most leverage of anybody out there in terms of how many tokens you use. And typically speaking, your mistakes are the most expensive ones, because if you screw up,

you're screwing up at a level of hundreds of thousands or millions of tokens, maybe more. And the reason why is simple. you are doing bigger projects with AI. And when you do big projects with AI, your ability to leverage AI effectively becomes one of the most critical things you

can do to manage ROI and cost on a particular project. It is a job skill at that level. If you're technical enough to go to a GitHub, you have a job skill to manage tokens efficiently, and you cannot pass that off to somebody else. That is not going to be somebody else's full-time job at an org.

All of us are going to have to learn to manage our tokens well. If you are sitting there and you are the person who is responsible for the system prompt on an agent and you haven't pruned it in the last couple of weeks, what are you doing?

If you haven't sat there and gone long by line and said, you know what? A hundred of these lines, I don't need anymore because they've been here since 3.5 and like, I don't need them now. If you're sitting there and you're like, I don't know why we're loading this entire repo into the context window.

We just do it all the time. And it seemed to work two generations ago, but we never tested it. That's just irresponsible. you need to be in a position where you are actually allowing the gains in model intelligence to lean out your context window.

If you want to look at the larger trend that we see in AI today, it is that we needed to front load and be really specific about a lot of context for dumber models in 2025. And now that it's 2026, as the models get more intelligent,

we can lean out the context window initially because we can trust the model to retrieve better so take that seriously that is something you can do that is practical to get ready for cloud mythos don't sleep on it this is again if you're technical these are million token decisions we're talking about especially if you're running this

agent over and over again it adds up let me give you a specific example that is based on the original beginner example with pdfs to show you the tangible difference in cost right and this is something that should cascade all the way across if you don't believe me this is real

Let's say you feed raw PDFs into context. Let's say it's 100,000 tokens versus 5K like we talked about. Let's say it's a conversation sprawl that takes 30 turns. I've seen these, like this is very realistic. And let's say you use Opus 4.6 for everything, including formatting, including proofreading, and you're making something.

Over a five-hour session where you're talking back and forth, you might be spending roughly 800,000 to a million input tokens with maybe 150,000 to 200,000 of output tokens, including thinking. $5 in and $25 out per million, you're spending $8 to $10 worth of compute, which you might say, you know what,

I can tolerate that or I got the unlimited plan or I don't care, whatever. But I want you to look at the difference because anytime you start to get serious with AI, you need to see the difference. We talk about not being wasteful with artificial intelligence. This is being wasteful.

You wanna save water, you wanna save energy, don't waste your tokens. Clean session, same work. Convert documents to markdown first, start fresh conversations every 10 to 15 turns, use opus for reasoning and sonnet for execution and haiku for polish, and scope the context to what's needed. And over the same period of time,

you get the same result for 100 to 150,000 input tokens, a lot less, and maybe 50 to 80,000 output tokens. You blend that across both models. And instead of costing eight to $10 in compute, you spent a buck and you got the same amount. In other words, you got an eight to 10 X reduction in costs.

Now scale it, right? That sloppy user is burning 40 to 50 bucks in compute a week. And the clean user is burning five to seven bucks a week across a 10 person team on an API. That's 2000 bucks a month versus 250 bucks a month for the exact same results for subscription users.

It's the difference between hitting your limit daily and then forgetting that limits exist because you just are so productive. Now, if you think this isn't serious, I want you to think about the cost structure for Mythos for a minute. Mythos is rumored to be by far Anthropics' most expensive model. I think very strongly by April or May,

we are going to have a new class of pricing well above $5, $25 range for tokens into maybe 10x that, right? Imagine a world where you are 10x what Opus costs now. $5 in, $25 out for Opus. What if it's $50 in, $250 out for Opus? Well, now things start to get serious.

Now that 8 or 10x reduction on individual work for a day becomes something that you can actually measure and think about as a business. And you imagine how big that gets when you start to work across a dev team. The mistakes you're making today were tolerable because models were priced cheaply

When cutting edge intelligence that you want comes out more expensive, and I don't know the exact price, right? I'm not saying it's 50 and 250. I'm giving you a thought exercise. It might be 10 and 50 instead. It's still the same point. The point is the model that you want is going to cost more.

And as models cost more, your mistakes scale. Your mistakes scale with the price of intelligence. And make no mistake, the models will keep getting better. Every quarter, every release, the trajectory is unambiguous. People who tell you the models are plateauing are lying. They are lying to you. The models are getting much faster.

And I do see that occasionally, that people are insisting that the models aren't getting better. It's not true by any measure out there. And the people that I see insisting on it, I think they're insisting on it partly because they don't want to face the world as it will exist when AI is this good and

continuing to accelerate this fast. It's scary, right? But we should face it and we can all work through it together. All right, I have built a stupid button. That is my contribution to this discourse. I am building a stupid button so you can check and see if you are using your context incorrectly.

I want to save you money. I want to save you hundreds of dollars. Please do not be stupid with your tokens. If you care about it, don't waste the water, don't waste the electricity. If you just care about the bottom line, also don't waste your bucks. We should probably care about all of those things.

If you want to know what's in Nate's stupid button, it's really simple. There's six questions that I'm helping you answer. Number one, do you feed Claude raw PDFs and images when all you need is text? Is there something you are doing that is grossly inefficient as far as token go. By the way, screenshots, terribly inefficient.

It would be much, much better just to copy and paste text. Convert to markdown always. Claude can do it really, really fast for you. Why not? Question two, when was the last time you started a fresh conversation? Are you one of those people that keeps a conversation going forever?

I swear the number of people who keep their conversations going forever is highly correlated to the number of people who start experiencing symptoms of LLM psychosis. Why? Because models drift over time. They were never intended for that long a conversation. If you're having a long running conversation, you're just in strange territory.

When was the last time you started a fresh conversation? And why is that? Again, every time you take a turn in a conversation, you read it as sending one line back, but Claude or ChatGPT or Gemini reads it as sending the entire conversation back. And if you're wondering, is this something that's just for Claude?

Nate's talking about Claude a lot. No, it's for Chad GPT. It's for Gemini. It's for Llama. It's for any LLM you're using. It's for Quen. This is how LLMs work. Don't waste it. Question three, are you using the most expensive model for everything? Are you using Opus? Are you using 5.4 on pro mode? Whatever your choice is,

are you picking the most expensive model and just blindly using it regardless when the cheaper model may work better? This is a especially important if you have production workloads, but it's also true for all of us. Like if you're doing something that's a simple formatting task, don't depend on Opus for it. Don't depend on 5.4 for it.

Use the models for what they're designed for. Don't bring a Ferrari to the grocery store. Question four, do you know what's loading in context before you even type? You can actually find this out. You can run slash context in cloud code, by the way.

You could look at the number of things that are loading if you're in cloud code. If you don't know what that means, you can go to your chat GPT or your cloud. You can see how many connectors you have available. You can see how many you've loaded up.

You could be loading tens of thousands of tokens that you're not really aware of and not really using. If you enable Google Drive, months ago and you never, never, ever use Google Drive. You just thought it was cool on the day it launched. Why? Just drop it.

There are so many examples like that where we see something cool, we add it and we forget it's there and it's like a barnacle on a ship. It's gonna slow you down. It's gonna burn tokens. You don't need to have it. Audit. Audit your plugins. It matters. Next question.

API builders, are you caching stable context so you don't reuse it? Prompt caching can give you a 90% discount on repeated content, right? Cache hits on Opus cost 50 cents per million versus $5 per million standard. It makes a difference. Do not sit there and ignore prompt caching. Take it seriously. If your system prompt, your tool definitions,

your reference documents aren't cached, what are you doing? This is not advanced stuff in 2026. You should just be doing it. And the last question, the stupid button test for it. This is a real button, by the way. I really built a stupid button. How are you handling web search?

Are you letting Claude do web research the expensive way? People don't realize this, but if you call perplexity for a search, it tends to be much more token cheap than using Cloud natively. Now, Cloud is addressing this. There are lots of ways to do Cloud search. You can actually use Cloud to navigate through a browser.

You can also directly search in the terminal, and it will spin up something in the background that's a service, and you can call something in like an MCP connector for perplexity. All different options you can use. This is broadly true. It's not just true for Cloud. It's true for ChatGPT. It's true for Gemini, et cetera.

because MCP is magic. But if you are trying to do search, the larger point is that you should be doing search as cheaply as possible. If you just want quick results that are token efficient, it may be worth it to take the time to spin up an MCP and just have a dedicated

service that just returns the search results. That's what I have found experimentally with perplexity and Claude, is that perplexity tends to burn something like 10 to 50,000 less tokens per search, which is not a small number if you're doing complex search. And it tends to be five times faster and it has structured citations.

So this is not meant to be a perplexity plug. It's just a token management plug. Try it for yourself. But I got to say, I like faster. I like citations. I like less tokens. over a research heavy session, like a plugin like that can save you a lot on the token side. And that's a larger call out.

Like if you have ways to look at your token usage and to diagnose it, you're going to be smarter about it. And that's the whole point of the stupid button is like, let's not fly blind here. Let's look at our actual token usage and let's actually make some good choices and let's optimize it. Now,

What's in this stupid button? Number one, there is a prompt. If you've never done this, if you're like, what is an MCP server? We got a prompt for you, right? A prompt you can run against your recent conversations that actually identifies the specific dumb things you specifically are doing. Like it will see which documents you're feeding raw.

It It will see your conversation swirl. It will look at model misuse. It will look at redundant context loading. It looks at your actual patterns and it will tell you what to fix first. So that's the easy version, right? Anyone can use it, any plan, no setup required. Number two, a skill.

This is an invocable skill that audits your cloud code or your desktop environment or any other environment. It could be chat, GPT, et cetera. Skills are also translatable and it measures your per session token overhead. It will flag system prompt load. It will check your plugin and your skill loading.

It will give you a before and after before you make changes. Think of it as like you kind of need a gas tank for your tokens and gee, wouldn't it be nice to have one, right? So it's like the gas tank skill. Number three, we built some guardrails. So guardrails will sit directly on your knowledge store.

So if you're an open brain person, which is something we've been doing as a community, it will sit right on your open brain and you will stop burning tokens on input, which is a nice touch, right? Automatic markdown conversion for documents that are hitting the store, index first retrieval instead of just dump and search,

context scoping that enables a sort of minimum viable context for the query. This is where token management stops just being a personal discipline And it becomes infrastructure that starts to maintain itself. And I think I'm really excited to see how the community continues to build on this

because OpenBrain is open source and we'll keep evolving it and improving it. But I wanted to make sure that we had Rails that ensured we have responsible token usage for the OpenBrain community. Look, I'm going to close by talking briefly about agents and context because agents burn hundreds of millions of tokens in some cases.

We don't want to leave them out. How do we think about context management for agents? I'm going to give you five commandments. I call it the keep it simple, stupid commandments for agents. Number one, index your references, right? If an agent is getting raw documents instead of relevant trunks, you've already failed.

The entire point of retrieval is to scope what the model sees to what it needs. Dumping a full document set into the window on every agent call is wildly irresponsible. You can't do that just to give the agent context. Don't make the agent do work it doesn't need to do. Number two, please prepare your context for consumption.

Pre-process, pre-summarize, pre-chunk it. A reference document should arrive in an agent's context, ready to be used, not ready to be read or processed. If the model's first several thousand tokens of reasoning are just spent dealing with the crappy pre-processing you did, you're not being a responsible agent builder. Number three, this is something we've mentioned before.

I'm calling it out in the context of agents because it's so important for agent workflows. Please, please, please cache your stable context. System prompts, tool definitions, persona instructions, reference material, anything that is stable all should be cached. At a 90% discount on cash hits, this is the lowest effort, highest impact optimization that you have on the table.

If you're making thousands of agent calls a day and you're not cashing, it's just pouring money down the drain. Number four, scope every agent's context to the minimum it needs, right? A planning agent does not need your full code base. Don't give it the full code base. An editing agent doesn't need your project roadmap.

Don't give it the project roadmap. You get the idea, right? Passing everything to every agent is architectural laziness and it has real costs, both in tokens burn and frankly, in degraded agent performance. Models perform worse when they're drowning in a relevant context. And by the way, if you're like, I'm not sure what the agent will need,

aren't the smarter agents supposed to find it? The answer is yes, but you will only do that efficiently if you give them a searchable repo that is pre-processed so they can go and get only the relevant slice of context. So take the time to do it right. Number five, measure what you burn.

If you don't know your per call token cost, you're just optimizing without any information, right? Please instrument your agent calls. Track your input tokens, track your output tokens, track your overall model mix and your cost ratio. You cannot improve what you do not measure. And most teams building agentic systems are thinking a lot about whether they are

semantically correct, not whether they're functionally correct. There's a big difference. And they're thinking a lot about optimizing their system prompt. They're not thinking a ton about their model cost. Because most of the time, the model cost is not what makes the project live or die. And I get that. In this age, in 2025, early 2026,

with the costs we have today and the urgency from executives to build, the $12 per run cost or whatever it's going to be is not going to make or break the ship. Plan for a world where the models are more expensive. Plan for a world where you have to scale up.

Plan for a world where you have to be responsible and instrument now. Stepping back, there's a cultural problem we need to acknowledge behind all of this. At some point in the last few months, burning tokens has become a badge of honor. And I get it.

There is a degree to which you need to be burning tokens in order to do meaningful work in the age of AI. None of this is to say that I expect token consumption to go down. It won't. You need to be ready to burn those tokens. This is not an ask that you not do that.

This is an ask that you do it efficiently. And so when Jensen sits there on stage and says $250,000 in token costs per developer and everyone is shocked or rolls their eyes or whatever the reaction is, my reaction is, I hope it's $250,000 in smart token costs.

It's not the individual dollar amount for Jensen because he's got cash in the bank. It's whether the tokens were used well. It's whether it's smart tokens. So begin to think to yourself, yes, I need to be maxing out my cloud. There are people who like go into withdrawal when they don't get to use their cloud.

I know people like that who are like, I went to a movie and I couldn't use my cloud for a few hours. I feel like I missed out on my token limit. Touch some grass. It's going to be okay. But use your tokens well. Be efficient with your token usage. Know what you're spending it on.

Don't spend it on silly stuff. Don't spend it on the PDFs that you have to convert. Actually spend it on meaningful work. And that is something that is a human problem. We need to be bold and audacious. These models are really good at stuff.

So let's get more bold, more audacious, and think bigger about what we can aim them at. Because if we can be more efficient, we can do a whole lot more cool and creative stuff with those tokens. That's why I built the internet a stupid button. Cheers.