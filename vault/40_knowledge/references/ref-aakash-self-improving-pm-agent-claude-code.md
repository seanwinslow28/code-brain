---
title: "How to build a self-improving PM agent in Claude Code"
source: "https://www.aakashg.com/how-to-build-a-self-improving-pm-agent-in-claude-code/"
author:
  - "[[Ashutosh Singh]]"
published: 2026-05-22
created: 2026-05-23
description: "Aparna Dhinakaran (CPO, Arize AI) shows how to build, trace, eval, and loop a PM agent in Claude Code in one live session."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery]
ai-context: "Aakash Gupta's walkthrough of a self-improving PM agent in Claude Code — feedback loop, eval-driven prompt refinement, and the architecture for an agent that gets better at PM tasks over time."
---
![](https://www.youtube.com/watch?v=DL-pUGcfrf4)

*Check out the conversation on* [*Apple*](https://podcasts.apple.com/in/podcast/how-to-become-a-builder-pm-with-n8n-claude-code/id1763555775?i=1000762483697)*,* [*Spotify*](https://open.spotify.com/episode/5ZNRFSYL15vRo7Rt51ANXP?si=glhi9q4SS7igfxzCWWA0bw)*, and* [*YouTube*](https://youtu.be/DL-pUGcfrf4)*.*

### Intro (00:00)

Aparna: Any product person that has used observability and is looking at their traces and looking at their evals, you’re probably already in the top 1% of PMs.

Aakash: What is the role then of the PM? Do PMs need to become engineers at this point?

Aparna: At the AI native teams, I am seeing that the gap between a PM and an engineer is indistinguishable.

Aakash: Aparna Dhinakaran is the CPO and co-founder of Arize AI. $131 million raised, and most of the smartest AI teams I know are building their evals on top of it. I feel like a good eval is one where you’re getting some healthy percentage right but also healthy wrong, so that you can make progress, right?

Aparna: 100%. I get excited when I see that evals are wrong, because then it gives me a chance to know that there’s improvement that could be made.

Aakash: What are the things, if somebody has just two hours this weekend, that they should concretely go do and take away besides just watching this episode, so they actually make impact in their career? If you have any two hours this weekend?

Aparna: I would say literally what we just did right now.

---

### What PMs are getting wrong with agents and evals (01:38)

Aakash: I’ve been doing a ton of episodes on Claude Code, a ton of episodes on AI agents, and separately episodes on evals. What this episode is doing today is bringing it all together for you in one iterative loop. It’s kind of like the product development cycle for AI products in a single shot. So you’re going to get to see front to back how we do it.

I think we have a tremendous opportunity to learn from Aparna. So I’m going to try to ask her the tough questions where maybe what she’s doing is skipping some steps, so you guys can see it step by step. And she’s volunteered to be our guinea pig on this. Aparna, thank you so much for showing us the ropes of how to do Claude Code evals.

Aparna: I’m super excited to be here. Thanks so much for having me, Aakash.

Aakash: So, what are people getting wrong when you look at them building agents and trying to do evals?

Aparna: I think the first question I get asked a lot is, when should I even start doing evals? Why is that important? Do I need to think about it before I even build my agent?

If I’m honest with you, most teams are starting with just building. You’ve got to start by having a real product before you run evals on it. So today, what I’m going to actually walk you through is the full end-to-end loop of getting started with building a product, and when it makes sense, because of the data that you’ve collected, to actually run evals and automate that.

Aakash: Awesome. Let’s see it in action. Where should we start?

---

### Why product taste is the alpha (04:35)

Aparna: A little bit of a vision for anyone who’s an AI PM today. Code is so cheap to go create, which means that product taste is really the alpha today.

People, especially product managers, there’s all this hype around, is it going to be the death of PMs? I’ll tell you this. We’re hiring more PMs than ever. We’re hiring more engineers than ever. The ones that stand out are those that actually have an opinion and a taste around what to go build.

So today, a little cheeky, but can we try to create taste? Can we try to have the PMs that are watching this have an upper hand to actually create that product taste?

Where does product taste actually come from? You look at some of the best products out there, and what they’re doing is taking in a ton of feedback. The best PMs do this. YC says this to every single cohort, which is talk to users and go build.

What we see is that in order to actually create taste, you need to be getting feedback from a ton of different sources. It could be everything from where your team stores those issues. It could be from GitHub discussions, or in-real-life discussions from Slack and Discord, from your actual community talking to you.

But we also see teams building out a context graph with all of this feedback. Everything from Gong transcripts every time you talk to your customers, your product analytic tools — PostHog, Amplitude, Pendo, Full Story — even down to Twitter. If you have a product that your users are tweeting about and sharing feedback on, these are all ways for you to actually create and cultivate that feedback source.

And instead of having just a human consume it, you can actually have your agent consume that feedback.

---

### What a product taste agent does (05:25)

Aparna: So what we’re going to do today is build a bit of a product taste agent.

You’re a PM. Your job is to come in and figure out what to go build. What are users asking for every day? This product taste agent’s going to tell you what your biggest pains are, what your biggest priority should be, and suggest where your product roadmap needs to go.

The product I’m going to work off of today — and you can pick your own product that makes sense for you — is actually our own open-source product, Arize Phoenix. Arize Phoenix is the leading open-source observability and eval platform. You can get started and host everything entirely open source with Phoenix.

With Phoenix, we have a ton of backlog issues. We also have really vibrant GitHub discussions. We have our own Slack community. We have feedback from people who are tweeting at us. So what I’m going to try to do is actually aggregate a lot of that and use that to surface up where we should go and where we should build next.

The steps we’re going to do here: first, create this PM agent. We’re going to do this using Claude Code. The magic behind everything that we’re going to use to improve is really tracing. We’re going to trace everything. Every step of what our agent does is going to be visible to us, and then we’re actually going to run the evals.

When people ask, “When do I do evals?” — get the data, trace everything, get the observability. The evals can then help you take your agent to the next level. So we’re going to trace it, eval, and then do this loop where we improve our agent and bring it right back.

Pick your favorite product that you want to use. Pick a product that you have all the context of. You could start super simple. What I’m going to start with today is literally just the GitHub issues, the GitHub discussions, and use that to inform what my product taste or PM agent is going to look like.

---

### Building the agent in Claude Code (07:30)

Aparna: Let’s do this. We’re going to build a PM product taste agent just using Claude Code. So go ahead, kick up Claude Code in your terminal.

For product folks, this might feel intimidating in the beginning, but I can guarantee you the level of control and iteration you’re going to get by doing this in your terminal and getting comfortable is going to be worth a little bit of that learning pain in the beginning.

Let’s do this. Go ahead and create a repo, or just a directory, and initialize Claude inside of that directory. Let’s give it a starter prompt to build this agent. I’m going to ask it to build me a PM agent for the Arize Phoenix product, and I can link the URL to that entire repo directly in here so that it has exactly the context of what I’m asking it to build.

Then I’m going to ask what context I want it to have. So: pull recent GitHub discussions, pull all the recent releases, and look at the GitHub issues.

I’m going to start piecemeal here. First, just starting with context from one location, which is GitHub. As we scale this, you can add in context from your Gong transcripts, your product analytics. You can add context from your Slack convos, your Discord channels. Anything can be brought into here.

What I first wanted to do is figure out — score the issues and the discussions based off priority. Just figure out how important is the stuff we want to actually look at and build. Things to look at: bugs versus features, reactions that people gave it, comments, recency. These are all things I’m asking this product taste agent to take a look at and consider.

Then call Claude — or I can be specific, I can say call Claude Opus, whatever model I want. I could even ask it to do some prompt caching so it doesn’t keep pulling down the issues every time I run this loop. But just to keep it simple in the beginning, I’m going to call Claude and write down a markdown PM report that has, as the output, the top pain points, feature asks, and themes. Order this by P0 to P3 priority.

This is basically the initial starter prompt to build this product taste agent. Typically what I like to do is be really thoughtful about the plan I’m giving my agent so it’s not going off of nothing. But there’s also times where you’ll just have it go off, build something, and then iteratively give it feedback. That’s totally also okay.

Then I’ll say: use my GitHub token and my Anthropic API key. Let’s see what it can come back with just with that. Super simple.

---

### Preview of a pre-built version with tracing (13:00)

Aparna: While this is going and doing its thing in the background, what I’m actually going to show you is a simple one I built right before this, and see if we can get the one we’re building right now to just match up — see how close we can get in just an hour here.

This is basically a PM agent that is already built out, and we’ve had tracing set up and is sending to Arize already. I’m going to open one of these so I can show you what it looks like. These are the traces of our actual PM agent.

For those of you who are like, what’s a trace? That’s a new concept to understand. You can think about a trace really just as the step-by-step playback of what this agent actually did. In this scenario, this agent is first going ahead and pulling back GitHub discussions. It’s pulling back the GitHub issues. It’s figuring out what are all the releases that were recently released. And then it’s going through and looking at every single issue inside of that project, and it’s consuming all of these and coming up with a score of how important each of these issues are.

As a product person, this is the first thing you need to understand: how important are all of these asks that are coming from your users? What is the pain that it’s solving? So the first thing I’m asking it to do is figure out — can you score how important each one of these asks coming back from this project is?

What I’ll actually do, as it scores, I want an eval that will evaluate how good was the score that my PM agent actually came up with. Is it accurate or inaccurate based off the context I have around how I want to prioritize bugs, how I’ve historically prioritized feature requests? So I actually want to write an eval that will help teams evaluate the quality of this initial PM agent we’ve built.

Aakash: When somebody’s setting up this repo correctly, basically you created a new GitHub repo, you gave it your Anthropic API key, and to create the repo you have to log into GitHub. Those are the main steps people have to do before this. Correct?

Aparna: Correct. And I’m happy to send you guys a sample repo if you want to get started doing this yourself, so you can follow along with a project of your choice.

In this case, you can see it’s gone ahead, it’s built this agent. It’s using my GitHub token. It’s using my Anthropic API key. Now it’s going to go ahead. It’s pulled 40 discussions, 60 issues, eight releases. It’s going to score each item, and based off the score it gives every single one of these issues, it’s going to give me a report about the most important things — top pain points, feature requests, themes, what shipped — and give me a game plan I can use as a starting point when I come in.

---

### Running the agent on a cron loop (17:00)

Aparna: A really useful feature: you’ll do this once today, but ideally you want this kind of running all the time, consistently. Every time someone adds a new bug report, adds a new issue, it’s always doing this. So what you can do is just say, “Can you run this in a loop?”

You can specifically say, using the Claude loop skill.

This is really awesome because what Claude does is spin up essentially a cron job. What’s a cron job? It’s basically you asking it to run some type of workflow that you do every day in a loop. In my case, every day, every hour — you could set this to every five minutes if you wanted to. It’ll go ahead and run this loop on whatever cadence you set, so it actually does your job every hour. Makes sure you have the latest report of what you should be prioritizing for your agent.

Looks like I need to set my GitHub token. Give me one second. Then we can run this agent and you can watch it live. This is actually going ahead and running my Phoenix PM agent.

---

### Instrumentation in one command (19:00)

Aparna: I’m going to show you guys how to do this so you can also do it, but I’ve also kind of already set up traces. What does that actually mean?

Tracing is the way for teams to get visibility into everything these agents are doing. This is a really hard thing to debug because Claude is spinning off a bunch of different things and running this in a loop, and you might not always know — if it comes back with slop or comes back with something great, how do I go and improve it? How do I figure out how it did that? Tracing is a really awesome way to understand what your agent’s doing.

Today, what I’m going to show you is — tracing used to be really hard. You had to call your engineering partner to set up tracing. I think with AI, it’s probably never gotten easier to do this.

What we have is essentially skills. We’ve released a series of skills that you can give to your coding agent. This is a set of Arize skills. You just go install, `npx skills add`. I’ll show you. Once you add this, you can just ask Claude Code to instrument the entire agent that we asked it to build.

Right now, you’re looking at a whole bunch of different skills. One of them is the Arize instrumentation skill. For those of you who are curious, it’s literally just in English, telling Claude Code what it should do to send trace data over to Arize. It makes it super easy. It’s going to feel super magical, and you’re not going to need to wait for your engineering partner to do all of this lift to get data from your agent to your observability platform.

So let’s do this. From here, I’m going to say, “Can you help me instrument this agent?” I’m going to ask it to instrument this agent.

What this is going to do is call the Arize instrumentation skill that we just talked about. So it’s going ahead, calling the skill. This instrumentation skill will first look at the codebase and understand: how is this agent built? What’s calling the LLM calls? What’s calling the tool calls? It’ll figure out, in this case the language it was written in is Python, the LLM provider was Anthropic, here’s the library to use, here’s what it’s going to do to set up the different calls.

And it says, “Cool. Everything is already wired up, sending to Arize. Is there anything else specific you’d like to change?”

---

### Traces streaming into Arize live (22:00)

Aparna: Now let’s go ahead and run my agent. See if it sends recent traces, and I should be able to pop over to the platform, my observability platform, and look at traces. We’ll see if there’s ones that show up right now from my recent run. But it should start streaming in traces from the last —

There we go. This is everything from the last 15 minutes that’s just showing up here.

You basically get a way to do all of this, and it figures out everything from the individual LLM calls, the actual tool calls that were made — it had to go and fetch stuff from GitHub. It had to score every single individual LLM call. And then it finally had to come back with that report that I asked for: what are my top pain points, what are my top feature requests, what was already shipped. So you can see it’s giving me an executive summary, my top pain points, and the things it scored really highly for me to prioritize for my product.

Literally, I didn’t open any IDE. I didn’t open anything. I just asked Claude Code to build me an agent, gave it a really good prompt, and then I asked it: go instrument my agent with Arize using the skill. Boom, now I have visibility into my agent.

Everything’s probably not going to be perfect, and I can already guarantee you that it’s not going to be perfect. But what we can do is start using this as a way to understand: how would I improve this agent?

What I’m going to show you right now is actually an in-product agent that we’ve built called Alex. Alex is an agent that sits inside of our product, and you can ask all sorts of questions like: help me figure out the common types of issues that are coming up. This will go through, look across all of the data — the inputs and the outputs — and start to surface up common types of issues that users are asking about from my traces.

I can use this to first figure out: what types of evals should I be running on top of my agent? You’re starting your evals from a place of actually looking at your traces, looking at your errors, and trying to understand: did it actually score some things correctly? Did it not score some things the way that I would have prioritized?

How many times have you had someone on your team say something was super important, super priority, but you wouldn’t have given it that high of a ranking for yourself?

---

### Asking Claude to suggest evals (28:00)

Aparna: So the next thing I want to show is, for teams: how can you use Claude Code to help you figure out a baseline eval for these agents you’re building? You can have it build a baseline eval and use that to iteratively improve, so you’re not starting from complete scratch.

You can do this in our product. You can also do this using Claude Code. In the theme of today, I’ll do this using Claude Code and show you how you can set up evals directly from your terminal.

Once I have the traces sent to Arize, I can ask: can you suggest a good eval for my agent? Let’s see what it comes back with. This will call the evaluator skill that looks across the traces and suggests —

Okay, it looks across the traces and suggests three evals you might want to do. There’s report groundedness, which checks whether the issues in the final PM report are grounded in the actual data fed in. It runs across everything. So I think about this almost like an eval on the final report that was created.

You could do an eval on priority alignment, which checks whether the P0, P1 in the report matches the top scored issues from what you’re expecting. Or something around report actionability.

Okay, I could do these, but these are all things that are looking across the end product. What I actually want, as a PM, is something different. I want to look at every single — I want to get a little bit more granular in the beginning and start to understand: for every single one of these issues, did it actually give it the right score?

In this case it said this issue had a priority of three. Let’s pick another set. In this case it gave it a zero, said this integration is not that important. It gave this privacy question a three. It’s making up these priorities, and I wanted to first evaluate: is the score that it’s attaching to determine how important these issues are — is that actually something I would have set myself?

So I wanted to run a priority eval on: is the score saying how important these GitHub issues are actually accurate based off how I want to weight them? Let me go back to Claude Code and ask it to help me come up with a way to eval this.

This is very normal, where you’re doing this back and forth with Claude and asking it to repeat yourself and get really specific about what you want. In this case I can ask: “Can you help me build an eval to evaluate if each issue’s priority is actually scored correctly?”

Aakash: I think that’s option two, right? Priority alignment.

Aparna: This is slightly more — it looks like it’s checking at the end, in the very report, if the top scored issues are what I would have picked. But what I’m looking for is something slightly more nuanced. Not just the top issues, but every single individual issue is given its appropriate weight.

So it’s giving me this priority accuracy evaluator. It’ll create a way to run this evaluator on top of the actual traces. In this case, it’s already picking one I’ve actually already created — just to show you how this works. It’ll suggest, “Hey, there’s this eval you’ve already created which does this row-level, issue-level priority.” It’s going to use this to run it on top of those traces.

In this case, it’s saying it’s running on older data. Do you want to run it from today’s issues, the new issues you just grabbed? So it’ll start running on the newer spans. Every single GitHub issue that has come in, it’s going to give it a score of how important it actually is, and then it’ll evaluate whether that score was actually appropriate or not.

---

### Vibe evals vs axial coding (33:58)

Aakash: I’m keen to see what eval it creates. I guess the traditional eval teaching literature is all about finding production traces that you feel like there was an error. So I guess that line of thinking would say: you’d go to the trace dashboard in Arize, you’d look at those priorities, you’d say, “Oh, this is a zero but this really should have been a four.” And then you’d pick up like 50 of those errors. Then you’d group them and say, “Okay, these are the 10 errors that it does.”

So are we trying to replicate that process, but have Claude Code basically do it itself? Is that what we’re doing here?

Aparna: Exactly. Basically what Claude Code is doing is — it has access to all of the traces in Arize because the skills can call an API. I can share what it’s doing under the hood, because it does feel a little bit magical when we just talk through it.

Under the hood, all of these skills are calling APIs. Specifically, what we’ve realized is that these coding agents are really good with command line, or CLI interfaces. So what it’s doing is basically fetching all of the traces. You’ve seen Hamel and Shreya tell you, “Hey, go through line by line, look at where the individual traces failed.” That is a great way to do this. You can go in, start doing annotations, write free-form text about what was good, what was wrong about this. Absolutely a great way to do that.

I’m also someone who loves to see if Claude Code can help me cut some of that time and surface up some insights. What I’m doing here is trying to understand: just with Claude Code, if I can give it access to my spans and my traces, what are some insights I should have to go and learn? Help me tell me what’s wrong with my agent.

Sometimes — just being honest — it might not come back with something amazing as your first eval. But what I typically like about it is that it gives me a place to start thinking about problems and start thinking about areas of improvement.

I’ve gone ahead and created this priority accuracy eval. It’s now running across all of my new spans. I can go in here and just say: show me everything where the label is actually inaccurate, where Claude Code thinks the priority it came up with is wrong. And why is it wrong?

This is probably something you’re going to hear all the time from folks who do evals: was my eval wrong, or was my agent wrong? You will definitely have scenarios — and there’s a whole process that Hamel and Shreya talk about — which is aligning your evals so they’re grounded in human feedback.

What I’m sharing is a way right now of: can you start with the vibe eval and then modify and improve it so it becomes something you can trust? You can do either approach. You can go through the axial coding approach, surface up all the issues, have the human in the loop, identify categories of pain. But as a product person, you might already know what types of things you definitely want to catch. For me, what I want to catch is: is every single issue this agent is prioritizing right or wrong? Is it accurate?

I can start off by saying, let me see if I can have it create an eval to suggest what that priority accuracy looks like. You can do it through a skill. If you do have human annotations built through here, the skill will look at those human annotations and use them to build you an eval as well. I didn’t have any in this scenario, but if I had, it would go through and do the whole process Hamel and Shreya walked through of aligning the evals.

So it’s run the priority accuracy eval, comparing the accuracy of the score that was assigned to each issue, and it’s surfacing up: is this an accurate score or not? Again, this is just based off a simple first pass.

I am going to refine this eval, because this eval is completely based off Claude looking at my traces and trying to identify problems. The whole point of this is: how do we get this loop kicked off? This loop is meant to give you a starting spot. It is not meant to be your end-all-be-all state for your evals or your agent. Your evals will get better, your agent will get better. That’s what we’re showing in this workflow today — how do you get started, how do you get unblocked, and then how do you do that improvement loop to make this better?

In this case I have a very simple small eval: looking at the accuracy of the score. These are ones that Claude thinks are not accurate. I can directly ask: when my priority accuracy is inaccurate, what are common issues or reasons for that?

This will kick off and look at what types of things my PM agent is not prioritizing correctly. We’re trying to go from: you built an agent, you have traces set up automatically through Claude, you have Claude suggesting what an eval could look like, and now these are already scenarios Claude thinks are not accurately scored. This is a great starting ground for me to say, okay, what can I do to understand how to improve this agent? And you barely had to write anything — you just had to ask Claude a couple things.

This is Alex giving me suggestions of what to go do here. There’s whole categories of issues. There’s feature request scoring, legacy scoring system, bugs priority scoring, low priority scoring, data fetch. There’s a lot of different categories where it’s suggesting my scoring might be off, and it’s giving me a whole bunch of spans to go look at, to debug and understand what actual problems this PM or taste agent might have in prioritizing issues coming in.

Aakash: What’s a span exactly? It’s a group of traces?

Aparna: A span is really an individual step in a trace. In this case, what you’re looking at — this entire interaction where it did this whole report — is what you’d call a trace. A span is a single individual step, or a single individual issue, that I had to go look at.

Aakash: Got it. And isn’t it a bit weird that Claude rated like everything it did inaccurate?

Aparna: Some of them are accurate and some of them are not. If everything was accurate, then that would probably be a good spot for you to understand: maybe I shouldn’t trust that eval from Claude.

Aakash: I feel like a good eval is one where you’re getting some healthy percentage right, but also healthy wrong so you can make progress, right?

Aparna: 100%. You want that feedback of — I get excited when I see that evals are wrong, because then it gives me a chance to know that there’s improvement that could be made. But when everything’s wrong, then obviously that’s a scenario where you need to look at your eval to understand what to improve.

Aakash: When can we do the vibe evals? When do we have to do the axial coding? Can you always start from vibe evals and then layer axial coding talking to the agent later?

Aparna: My take is that vibe evals are going to fall short very, very quickly. The reason is they’re not grounded on any actual human involved in curating that taste of your agent.

What you really want is something that helps you — it would be hard to say, hey, you have to immediately start by having a bunch of vibe evals and using that to evaluate your agent. The signal-to-noise ratio there is going to be really low. So having something where you have maybe a simple thing that gets kicked off, but now I’m going to go do that process where I have a simple eval and I’m now going to make sure: okay, well, is this eval I’ve created actually something I can trust?

It’s not going to be a one-shot eval out of the box. I’m going to actually go through and figure out: where do I disagree with it? Where do I not disagree with it?

You would do this process even if you did axial coding. Even if you did axial coding and individually human-annotated every single span and every single issue, and you were able to put together this amazing ground truth dataset, your eval will get misaligned over time as you see more and more data. So it is super important that you regularly align those evals to the data you’re seeing on the ground with your users.

What I’m going to do right now is walk through a process where I’ve created a very simple eval out of the box. Claude just one-shotted it for me. And now I’m going to start asking: okay, well, is this an issue with an eval? Is this an issue with my agent?

In this scenario, it looks like bugs — bug category items using the new scoring system with category four — are commonly inaccurate. So it feels like there’s scenarios where bugs maybe are not getting categorized or given the accurate score I wanted to. In my world, I want bugs to always be super high, because if it’s a bug and a customer hits a bug, that’s a really bad experience with the product. So I would prioritize bugs over even new feature work.

This gives me a way to say: let me go look at some examples of where the bugs are being prioritized really low. It gives me a category of problems to start looking at, debugging, and understanding how good this agent is.

For some teams, these evals end up — as they get really good — you can immediately ask Claude, going back to using Claude Code with evals: hey, go grab everything where this eval failed and suggest an improvement, and go improve that eval for me.

I think it’s unfair to say people aren’t using Claude to create evals. That’s maybe one of the pain points I see with always saying start with axial coding. In reality, you will always do it, but I think it’s okay to start with Claude suggesting what a good eval could be. These models have gotten so good — having it go through and look at your answers and suggest, “Hey, that probably is something you should flag and look at.” I would trust it. I would trust it as a first pass: go tell me what my evals should be.

Aakash: That’s my favorite workflow. Always start Claude generating it, but then you just give it ruthless criticism. I turn on dictation mode and I’m like, “Well, you misjudged this for this reason. You misjudged this for this reason.” And that’s where the taste alpha that you bring can actually come back in.

Aparna: Totally. For me it’s: how do I quickly get into that loop? Get data in, get an eval set up, give it criticism, and let it go run on a loop.

---

### Looping the improvement automatically (48:50)

Aparna: I showed earlier there’s the Claude loop skill. So what you can do here is — now that you have this eval, you can create a whole other skill that’s just: every day, go through, fetch everything that was inaccurately prioritized, and go fix and improve my agent. You can create a skill that will then go suggest improvements to your agent from the evals you just ran on top of this.

Aakash: So you actually loop the improvement too, not just the agent.

Aparna: Because then you get to a world of self-improvement, and that’s where, to be honest, I think we’re all headed. The data that we all collect, the evals and observability, is the foundation for self-improving agents.

So you get your observability in. You build an initial eval. It’s a first pass. You’re going to make it better. You’re going to have to give it ruthless criticism to make the agent better or make the eval better. What teams are doing right now is doing that iteratively.

You can create a loop that essentially starts to look at the evals, identify — I just asked right there, give me the common reasons why the priority accuracy is inaccurate. Oh, it’s because the way I prioritize bugs doesn’t look right. So what I can do: go back to my PM agent and just say, “Hey, go fix this issue.” And then go fix the issue, ship a new agent, now go collect traces from the next rev of that agent. That improvement loop can run inside Claude Code as a loop skill.

Aakash: So that is all fine and dandy for your internal agents that are assisting you in your work. How does this all change for the AI agents in your product? You just showed us Alex. So maybe you can go under the covers of how that worked when it’s actually a product. You’re not going to be shipping self-improvement to Alex every day, because it could just go off in some weird direction. So where do the human-in-the-review-loop parts come in there?

Aparna: There is still code review. There’s still a human that looks at every PR being put up by this self-improvement loop. But maybe what I can ask you back is: isn’t that the vision? Isn’t that the future we all want to go to?

I should be able to see someone file a bug, on Alex, gave a response that someone gave a thumbs down on. Alex is able to immediately — and this is what we’re doing internally already; you’re going to hear a lot more about us talking about it in the next couple of weeks — Alex has already taken that feedback, spun up a whole debug workflow, and used the eval, used the trace, to debug what went wrong.

In some scenarios, like we talked about, it’s the eval that’s wrong. In that case, it’s a refinement on the eval. That’s basically what you hear all about axial coding — figure out the reasons why that eval wasn’t good and use it to improve that eval.

In some cases, the eval was right and it really was the agent that needed to handle a specific scenario better. In that case, we can very simply go in and improve the agent.

Aakash: That is what we want, right? Ideally it’s happening in real time across millions of users automatically. So how do you do that safely? Code review is one step. What else do you need? Where do you need to put the human in the loop?

Aparna: There’s a couple places where that needs to happen. One is as the eval changes — that’s also a really important step to actually having the human curate that taste of what is good and what is not good. So the human is typically involved in eval changes. They’re involved in the agent changes.

There’s a lot happening right now around making sure that the skill that’s actually being used to do the improvement workflows is one that is typically designed by a human. So what does that improvement skill need to look like? What is all of the context that it needs to have access to in order to know what the improvement is?

In this scenario, it might not have all the context, because all I gave it was just GitHub issues. But if I could layer in my product analytic metrics, layer in my actual entire traces — it could end up using that information to build its own context of what went wrong, how do I need to go fix it? You leverage that information as context for the improvement loop.

Aakash: Got it. So there’s human in the loop at any agent change, any eval change. But outside of that, you can use loop commands within Claude Code, or whatever, if you’re in more production a real cron job, and every day or whatever cadence.

What is the state of the art looking like for this self-improvement? You get to work with all the best companies — Uber, DoorDash, you name it. How fast are people moving and how fast do they need to be moving to be competitive?

Aparna: I think it’s going to come very, very quickly. If I’m honest with you, I think the best teams are already doing this in a radius they’re comfortable with today, but that radius is going to get bigger and bigger.

Maybe the initial improvement is around improvements to the agent that are more simple, more around the prompts, the tools. Does that radius then become about giving entire workflows that the agent didn’t have access to do? The radius of those changes is going to become increasingly bigger, which we’re excited about. But that self-improvement loop is not going to happen without having really good data and really good evals.

If you think about — and just to maybe take an analogy for something that’s so different — but if you think about some of the best sports players, what do they do? The Nadals, the Federers if you’re a tennis fan. Novak. What they’re doing is looking at their plays. They’re looking at their previous games. They’re looking and studying their behavior, what they did, and using that as a way to understand what went well and what didn’t go well, to make improvements.

Studying your plays is what self-improving agents, or self-improving harnesses, have to do. They have to study their own plays to understand what did the human say was a good response, what did the human say was not a good response, and use that to figure out how to improve their own gameplay. That’s why the evals and the observability are the foundational layer for teams to actually build that self-improving loop.

---

### The AI native PM profile (57:00)

Aakash: I personally have encountered PMs that I feel like are in one of three buckets, and I think you have customers in all three of those buckets. There’s the AI natives — like customers you have like Handshake and the AI companies. Then there’s the digital-first companies — customers you have like Uber and Reddit and Roblox. And then there’s the normal companies who have tech arms — Pepsi, Condé, normal type of companies.

You get to work with all three of those groups. What I want to understand is: usually the AI native groups are going to be doing the “quote unquote best way” or the right way of how to do things. So what are the AI native groups doing? And specifically not just with how they’re building their evals, but the role of the PM. What is the role of a PM in an AI native company versus a company who hasn’t gotten there yet, and how does that company bring their PMs there?

Aparna: I think the role of a PM has completely changed in the last year. The role of the PM is almost like — you’re the taste maker for this product. And in order to become a really good taste maker, you really have to understand the outcomes of the agents — especially the AI PMs where the product is the agent. The product is the agent being built.

You have to spend a lot more time — the AI native PMs are almost indistinguishable from engineers in some ways, because they’re comfortable living in Claude Code. Like this entire workflow I just showed, where they’re able to build even just a simple internal agent to help them do their daily tasks.

We say this internally and I think it’s true: if you’re doing things the same way you were doing things last year, then you haven’t caught up yet.

I deeply do think that if you’re looking at your board of “here are my priorities” and you’re manually scanning them and manually understanding every single one — kind of doing what you used to do — it’s just different now. With the advent of Claude Code, I can actually have it — you’re not limited by how many individual meetings and Gong calls you can personally hear. You can have Claude Code go through; it has access to all of these customer calls that you might never have been able to consume by yourself. But can it help surface up the one or two that are super critical? You need to put your eyes on those because those are going to help you unlock your next 10, 15 customers.

In these AI native companies, what we’re seeing is that the PMs are able to leverage Claude Code to do everything from understand user data and user feedback better, surfacing that back into what a really good product experience looks like, to get really close from idea to solution. So it’s not like, “Hey, I’m handing it over to an engineer.” They’re able to effectively put together a plan for what that build needs to look like. Those are the PMs that I think are going to be 10x or whatever multiplier PMs in any team.

Aakash: So we’re talking about working with those AI native companies. You yourself are one of those AI native companies, and you referred to this — that you yourself are hiring more AI PMs than ever. So what does the new profile look like? If I want to land an AI PM role at an AI native company that has raised $131 million, what are the skills I should be developing? What is the depth of technical knowledge and topics I need to cover?

Aparna: Curiosity has always — I have always believed this is, for me, the number one most important signal. This person is trying all the new tools, exploring the boundaries of what they can and can’t do.

There’s the old way of doing things — there used to be trainings, and you’d go to these trainings, and someone would walk you through how to use a tool. What if the tool is Claude Code, and it has shipped 90 features in like 30 days? There is no old way of doing things where you can have a daily training for a product that’s moving that fast.

The onus of keeping up has become on the individual now to actually keep up with the tools, keep up with what’s changing. Not everything is going to be useful to what you do, but if something can give you the ability to say, “Hey, that used to take me an hour and now it can take me 10 minutes” — that is an advantage. Being able to identify those and use them to your advantage is built off of curiosity at this stage.

The other big one — it’s still really important to care and understand the user. Customer empathy is something that the best PMs and the best taste makers understand. You could ask them, “How is that customer using the product? What’s their biggest pain point?” They would rattle them off to you.

What’s now changed is that you can actually get even deeper. A customer asks for something — it could have taken a week to build that, two weeks to build that in the past. That could be delivered that day, if you’re able to ship at that velocity. Being able to get even closer and deliver to customers even faster is no longer just a pipe dream. It’s actually how the best products at AI natives are shipping right now.

---

### Same-day shipping is real (01:03:00)

Aakash: 99% of people aren’t in an AI native company, so they don’t believe us. I need to just confirm this is true. What you’re saying is that sometimes an issue will come in, your PMs will identify it’s important enough, either they will prototype or an engineer will prototype and make ready for production a feature, and you guys will ship it in the same day?

Aparna: Yes, that is actually what’s happening.

Aakash: So she said it herself. So what is the role then of the PM? Do PMs need to become engineers at this point?

Aparna: At the AI native teams, I am seeing that the gap between a PM and an engineer is indistinguishable. Because when code has become so much easier to actually produce, then — this goes back to where we started today’s podcast — the alpha today is product taste.

So the people that understand product taste, understand what customers want, understand how to deliver a really amazing experience are just going to have insane velocity. PMs who can go from “here’s the pain point, here’s what I think is a really amazing experience,” and they are a triple threat where they’re like, “I could probably go build that today, and figure out, talk to Claude Code, and figure out what to go build” — that is a triple threat in this environment right now.

---

### What enterprise PMs can take on now (01:04:30)

Aakash: What are you seeing at the enterprise level, because they’re not even close to there? If you’re at a big enterprise, if you’re at a Pepsi or something like that, you’re still trying to take on the best practices. Realistically, what can they take on and how do they take them on?

Aparna: What I’m seeing at enterprises — I don’t want to say there’s no innovation happening there at all. There is. All these teams are using the coding agents and feeling the unlock of those tools in their own day-to-day workflows.

What I’m seeing coming out of the teams right now, even there, is: one, amazing products that use AI to make the experience of that product useful. Two, I think there’s usually a massive — especially in larger companies — you have silos of data and people who might have access to some information other teams don’t have access to.

---

### The context graph unlock (01:06:00)

Aparna: There’s a really great piece that Jay Gupta — someone you should follow on Twitter — shared a couple weeks ago that went super viral, around context graphs. What a context graph is, essentially: can you give your agent access to —

Agents are only as good as how much context they actually have. And then of course the harness built on top of that has access to that context. Instead of all that information and data being in completely different silos — people operating in these silos — can you give one unlock for agents, which is: can you give it access to context from different environments?

What that does is it actually makes people bridge the gaps across different teams in ways that probably weren’t possible before. Figuring out how agents consume the context within an organization is going to be probably one of the biggest problems. It’s one of the biggest unlocks, biggest challenges and unlocks we’re going to see this year.

Aakash: So if you’re a product leader at one of the enterprise companies, you’re seeing what you just demoed for us. You’re saying, “Okay, how can I bring my company towards that?” What’s sort of the step-by-step roadmap I should be implementing over the next, say, 12 to 24 months?

Aparna: First, I think as an individual, building. You’ll read a lot of stuff on AI Twitter of everyone sharing every latest new model and every latest new tool out there. I would highly recommend for any AI PM: start by building. Start by building very simple, like this example that we just did today.

It doesn’t even need to be an external-facing agent that you need to publish. Can it just be an internal tool that you use to actually help you make one big unlock today? That’s huge. Because think about, if this tool that we just vibe-coded in an hour, now I’m going to go use it to figure out, okay, what are my top pains?

You can imagine the next step after that is: can I get an agent to actually go put up a draft PR for one of these? Can I get an agent to actually then review that PR and do the code review on that? The process to go from identifying a pain point to releasing it could have taken months in the past. That entire thing can be shortened to the span of a day. If that could be your day — what does everything need to look like in order to deliver on that?

I think it changes the game for individual ICs. So first I’d say, start by building. It’s the biggest unlock.

Two: as you’re building, it’s important to figure out what are the systems you need in place. It’s easy to build something and then say it doesn’t work — “I’m just going to scratch the idea and let it sit.” The most curious of the PMs — this is where having a data layer like Arize and the observability platforms are really helpful. You might not know why your agent gave you a bad response, or why the outcome wasn’t great, or what it was doing.

Getting observability — like we were talking about with the simple example of the tennis players, how do they look at their plays and figure out what went wrong, and how do they get 1% better every single day? If you could plus-one your output every single day, the story is no longer about observability and looking at your data. The story is about self-improvement — improvement of yourself as a PM, but also improvement for the products that you are building.

---

### Open source vs paid: how to choose (01:10:40)

Aakash: We used Arize’s open-source Phoenix platform and then we used Arize the paid platform to do this. Those are two options. How does somebody make a decision? What does the overall ecosystem look like and why would they choose Arize?

Aparna: Great question. Arize Phoenix — which was the open source one we pulled all the GitHub issues from today — is an amazing option if you cannot send your data to an external platform. For most enterprises, most teams building any agents that have any PII data, it’s just a reality that they want to self-host some initial observability so they can get a feel and get an unlock.

Arize Phoenix is — I think even Hamel has tweeted this before — his most favorite open-source tool for observability. It’s got a super permissive license. It’s got almost everything you just saw in the demo today out of the box. And all the skills I shared using Claude Code, all those skills exist for Phoenix too. So you can just go open up, build an agent and say, “Hey, help me instrument it. Help me figure out insights for my traces. Help me go write evals.” Phoenix will go and do all of that for you today.

Typically where teams start to feel the paid platform — the enterprise platform — makes sense is when data volume starts to scale. We have teams that send us — I think it’s a good thing that these agents are starting to find product market fit in this environment right now. The models are getting better. Products are starting to find product market fit. And so we’re starting to see almost terabytes of data. The volume and the scale is a big reason why, for teams that need that, as our agents start to get mature, it makes a ton of sense to have a more scaled-out platform observability. This is where Arize AX is uniquely fit to solve that problem. We do this really well because we’ve actually invested in our own data store that we’ve been building for a while now, ADB. It’s a data store designed for AI workloads from day one.

Aakash: So let’s say I’ve figured out I need to pay for it. I have the huge amount of data. How do I decide who to work with?

Aparna: The reason to pick Arize is really — we’re the open and independent, most independent platform out there. We are independent of framework. We don’t actually care what framework you use. We have teams using everything from LangChain, the Claude agents SDK, to teams that are building without a framework. We’re agnostic of whatever framework you use.

The second thing is, we deeply believe in the independence of your data. All of our trace data that we collect lives in open formats. Using our ADB data fabric, that data can be directly sent back to your data warehouse. The reason that’s really powerful is because you don’t want your agent trace data, which is so valuable, to be locked inside a proprietary platform. We make it accessible so you can actually use the agent trace data as part of your context graph.

We’re also independent of instrumentation. If you don’t know, we’re actually the inventors of OpenInference. Our competitors, every single one of them you mentioned — all use our instrumentation, and they’ve actually linked to it in their docs. We own — we built probably the richest telemetry — and it kind of shows in the fact that our instrumentation’s widely adopted in the ecosystem.

The last one is, I think we’ve been consistently one of the most innovative in the market. We were actually the first to shipping LLM-as-a-judge. If you go back to 2023, you’ll look at Phoenix in the repo and you’ll see LLM-as-a-judge. We were the first to release OpenInference instrumentation. Alex, that you saw in the product — we were actually the first to have an agent built into our product. The skills you’re actually looking at, that we showed how you use all of those skills — we were actually the first to have and release them. Hamel did a talk with Mikko on this about it — our open source lead. And then I was mentioning, we have the first and only way right now in market to actually take all of these agent traces and have them as standard formats as part of your context graph. It shows we’re probably the fastest innovator in the space right now.

---

### What to do this weekend (01:16:00)

Aakash: What are the things, if somebody has just two hours this weekend, that they should concretely do and take away besides just watching this episode — to actually make impact in their career?

Aparna: If you have two hours this weekend, I would say literally what we just did right now. Build an agent for yourself. Whatever would take away a couple hours of your week every week. Some repetitive thing you do every single week.

By the way, this isn’t just for PMs. If you’re someone in product marketing and you’re writing release notes every week — what is just a workflow you do every single week that takes a couple hours, try to build an agent to go do that.

What you’ll learn out of that is, one, how insanely easy it is with Claude Code. And then you’ll also realize how much work it takes to actually make it really good. To make it get better past that initial vibe code, the evals and the observability are so important.

I said this in the beginning, but any product person that has used observability and is looking at their traces and looking at your evals — you’re probably already in the top 1% of PMs in the world right now.

Aakash: What are the biggest mistakes PMs are making when they do evals?

Aparna: The biggest one is not starting with actual trace data. If you’re just starting with what you think are problems, that’s really hard.

Even the skills, for example, that we used today, that Claude was using to build the evals — what’s powerful about it is that it’s actually trying to instill best practices. It’s actually looking at all of the trace data to help and suggest what the right evals could be.

PMs need to look at — the evals don’t just come out of magic. They come out of your traces.

---

### Outro (01:18:55)

Aakash: All right, everybody. I’m going to put up Arize’s pricing page for you. This is how much Arize costs. Now here’s the cool thing. If you want to get AX Pro for 12 months free for your team because you’re convinced you want to create self-improving agents, you can do that with Aakash’s bundle. Or you can just use the free options that she’s talked about right now — Phoenix and AX free — to get started. It’s that simple. I highly recommend every AI PM master the AI eval skill. Arize is one of the easiest ways to do it.

Aparna, thank you so much for lending your expertise.

Aparna: Awesome. Thank you so much, Aakash. It was awesome to be here.

Aakash: I hope you enjoyed that episode. A couple things you can do to support the show. One, comment, review. Those ratings and reviews really help other people understand the value and the production that we are putting into this. This wasn’t an easy episode to produce. We put in a ton of pre-work. We edited it for you. We brought in the best guests. If you don’t mind sharing a rating and review, sharing the episode with others, making sure you are subscribed — that really helps the show do bigger and better productions. I’ll see you in the next episode.

---
*Clipped from [aakashg.com](https://www.aakashg.com/how-to-build-a-self-improving-pm-agent-in-claude-code/) on 2026-05-23T14:47:11-04:00*
