---
title: "Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)"
source: "https://www.news.aakashg.com/p/ankur-goyal-podcast"
author:
  - "[[Aakash Gupta]]"
published: 2026-03-20
created: 2026-05-23
description: "Learn the data-task-scores eval framework from Braintrust CEO Ankur Goyal. Build evals from scratch, iterate fast, and ship better AI products."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
The Growth Podcast

Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)

The companies running 12.8 eval experiments per day are building AI products that actually work. Here is what every PM needs to steal from their process.

![](https://www.youtube.com/watch?v=71qvIkO9d_A)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/evals-are-the-new-prd-here-is-the-playbook-with-the/id1763555775?i=1000756385737), [Spotify](https://open.spotify.com/episode/6AK7zQ491XxPVL8Ku2NbF1?si=7bNdsuolThqhRLSnDxJEEw), and [YouTube](https://youtu.be/71qvIkO9d_A).*

Brought to you by:

1. **[Kameleoon](http://www.kameleoon.com/)**: Leading AI experimentation platform
2. **[Testkube](http://testkube.io/):** Leading test orchestration platform
3. **[Pendo](http://www.pendo.io/aakash)**: The #1 software experience management platform
4. **[Bolt](https://bolt.new/solutions/product-manager?utm_source=Promoted&utm_medium=email&utm_campaign=aakash-product-growth)**: Ship AI-powered products 10x faster
5. **[Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7)**: Get $550 off their #1 AI PM Certification with my link

---

## Today’s episode

I have done four eval episodes now. We covered [error analysis and LLM judges](https://www.news.aakashg.com/p/hamel-shreya-podcast) with Hamel and Shreya. [Evals from first principles](https://www.news.aakashg.com/p/hamel-shreya-podcast-2) with Ankit. [The PM’s role](https://www.news.aakashg.com/p/aman-khan-podcast) in depth.

But I kept hearing the same question: **how do I actually build one from scratch?**

That is what today’s episode delivers. We build an eval **entirely from scratch**. Live. On camera. No pre-written prompts, no pre-written data.

I sat down with Ankur Goyal, Founder and CEO of Braintrust, the eval platform behind Replit, Vercel, Airtable, Ramp, Zapier, and Notion. They just announced their **Series B at an $800 million valuation**.

Users are running **10x more evals** than this time last year. People log more data per day now than they did in the entire first year the product existed. The episode explains why, and then we build one live.

We connect to [Linear’s](https://www.news.aakashg.com/p/how-linear-grows) [MCP](https://www.youtube.com/watch?v=a9wO6GSAoGk) server, generate test data, write a scoring function, and iterate until the score goes from 0 to 0.75. And along the way, Ankur drops what might be the most important reframe of the year: **[evals](https://www.news.aakashg.com/p/ai-evals) are the [new](https://www.news.aakashg.com/p/ai-prd) [PRD](https://www.news.aakashg.com/p/product-requirements-documents-prds)**.

*Plus, we cover the **complete eval playbook for PMs**:*

---

***If you want access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, DeepSky, Relay.app, Magic Patterns, Speechify, and Mobbin - **grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*

***If you want my coaching in your job search, [apply to my cohort](https://www.landpmjob.com/).***

---

## Newsletter deep dive

*I took everything from the episode and combined it with lessons from four [eval deep dives](https://www.news.aakashg.com/p/ai-evals). Here is the complete practitioner’s playbook:*

1. Why vibe checks stop scaling
2. The data-task-scores framework
3. Evals are the new PRD
4. Offline vs online evals
5. How to maintain eval culture

---

## 1\. Why vibe checks stop scaling

![](https://substackcdn.com/image/fetch/$s_!2UL6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9517c0bf-f53d-488e-b9d5-1c7159cb6dcd_2190x2410.png)

Open your AI product right now. Try three examples. Tweak the prompt. Ship it.

Two weeks later, support tickets start coming in about edge cases you never tested.

That is the **vibe check trap**.

When you do a vibe check, you are using your brain as a scoring function. You intuit whether the result is good or bad. That is an eval. It is just the version that does not scale.

Vibe checking is **not wrong**.

It is the *earliest version of what eventually needs to become structured*. In the error analysis process I covered in an earlier episode, the first step is reviewing 100 traces and taking notes. That is a structured vibe check.

Here is what matters: the best companies treat the transition from vibe checks to structured evals as a product decision, not an engineering one.

The **wall hits** when more people start using the product, more subject matter experts start contributing to quality, and more engineers start touching the prompts.

At that point, *one person’s gut feeling cannot cover the surface area*. You need software and process to execute at scale with predictable performance.

And here is the thing about durability. Models change every few months. Agent frameworks get replaced.

The prompt you wrote today might be irrelevant by summer. But if you invest in understanding what your users actually need and encode that as data, scores, and eval flows, **that survives every model swap**.

The companies that believe their agent wiring is their moat are **highly likely to fail**. The ones building true differentiation are the ones **investing in evals**.

*The prompt is temporary. The eval is permanent. That is the whole game.*

---

## 2\. The data-task-scores framework

![](https://substackcdn.com/image/fetch/$s_!koJl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd51ada5c-dedb-4ade-96e7-cf9fbbbd5fda_2384x2408.png)

In the [evals deep dive](https://www.news.aakashg.com/p/ai-evals), we covered the full analyze-measure-improve lifecycle. That is the theory. Here is the **practitioner’s shorthand**: every eval, no matter how complex, is exactly three things.

#### Component 1 - Data

A set of inputs your AI product needs to handle.

During the episode, we generated test data for a Linear task management bot:

1. “What tasks are assigned to me?”
2. “Are there any overdue tasks?”
3. “How many tasks need to be triaged?”

You can optionally include **ground truth answers**. If you know the correct answer is 12, include it. If you do not, skip it.

> *Do not spend a month building a perfect golden data set before running your first eval. Auto-generate silly questions. Jump in. Start iterating.*

This echoes what I covered on [bootstrapping datasets with synthetic data](https://www.news.aakashg.com/p/ai-evals). But in the live demo, we took it further. We used Opus to generate the data set in seconds, edited it by hand, and ran our first eval within minutes.

#### Component 2 - Task

A task takes an input and generates an output. It could be:

1. A single LLM call to GPT 5 Nano
2. A complex agent calling MCP servers, vector databases, and multiple models
3. Anything in between

At the end of the day, it produces some kind of output. That is what you evaluate.

During the demo, the first task attempt failed badly. The model just said “Happy to help with Linear” instead of answering. That zero score was **expected and useful**.

Here is what happened next.

We connected the Linear MCP server so the model actually had access to task data. Still failed. The model said “I am ready to help with Linear tasks” but never called a single tool.

So we changed the system prompt:

```markup
Don’t ask clarifying questions, just use the tools and figure it out.
```

This matters more than you’d expect. Models are post-trained to ask clarifying questions in conversational contexts. In an eval pipeline where you send one question and expect one answer, that post-training behavior works against you. You have to explicitly override it.

Then we loosened the scoring function. It was penalizing responses that referenced Braintrust tasks as sources, even though that was valid citation behavior. The scorer was too harsh for what we actually cared about.

Then we added few-shot examples to the prompt and specified which MCP tools to use.

Score went from **0 to 0.75 across the board**. Each iteration touched a different part of the data-task-scores framework. That is the rhythm: identify which component is the bottleneck, fix it, rerun.

#### Component 3 - Scores

Scores take the input, the expected output if you have one, and the actual output. Their job: produce a number between **0 and 1**.

That normalization is critical. It forces everything to be comparable. A week from now, when you run a new eval after swapping the model, you compare directly against today.

Do not overcomplicate scores. Use **categorical options**, not freeform numbers:

1. **A** = Full answer with citations
2. **B** = Partial answer
3. **C** = No answer at all

In the [evals deep dive](https://www.news.aakashg.com/p/ai-evals), I recommended binary Pass/Fail as the default. There is a case that not every score must be binary, but **clear criteria beats freeform every time**. The key is that you are not asking the LLM to generate an arbitrary number. You are giving it defined options and asking it to classify.

> *Data in, task runs, score comes out. Everything else is iteration.*

---

## 3\. Evals are the new PRD

![](https://substackcdn.com/image/fetch/$s_!g7_v!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F056c3a8e-1c73-425a-b92f-83c54baea6f4_2412x2036.png)

This is the reframe that hit me hardest.

Think about a [PRD](https://www.news.aakashg.com/p/product-requirements-documents-prds) from 2015. Unstructured document. A spec meant to communicate how to build something. The engineering team reads it, half follows it, the final product never matches.

*The modern PRD is an eval. It is something that an engineering team who maybe does not know everything about the problem can use to quantify how well the software is solving it.*

#### Step 1 - Encode your product intuition as data

Instead of writing paragraphs describing what the product should do, create a data set of inputs that represent what users actually need.

#### Step 2 - Use scores as success criteria

Instead of prose acceptance criteria, write scoring functions that quantify whether the software works.

An engineering team that does not know the domain can look at the eval and know exactly what good looks like.

When the eval passes and the product still feels wrong, that is on you. Your scoring function does not capture what matters. And that is actually a new area of leverage that PMs did not have before. You go from providing a qualitative spec nobody follows into something quantifiable.

I have been saying PMs should own error analysis for months now. This episode pushed that further: PMs should own the eval itself. The scoring function IS the modern PRD.

#### Step 3 - Close the distance gap

The farther you are from the end user, the more critical evals become.

Ankur framed this as a **distance principle**.

At Anthropic, the people training the models, building the harness, building the product, and using the product all sit inside one set of walls. Feedback circulates with almost no friction. In healthcare, engineers are not patients or doctors.

Ankur’s parents are both doctors, and he said when he talks to them about their work, he has almost no idea what they’re talking about. The jargon is specialized, the stakes are high, and the engineering team has no intuition for what matters.

Evals become the mechanism that bridges that gap.

Finance has the same problem with different jargon. Domain experts speak a language that engineers don’t, and patients become counterparties, but the structural issue is identical. PMs own the scoring function that translates between what users need and what engineering measures.

There was a Twitter controversy about Claude Code not using evals. This blew up enough that someone pinged me about it the day it happened because their boss was questioning whether evals even mattered.

Here is the reality: Claude Code is doing evals. People at Anthropic are using the product, providing feedback, and incorporating that feedback into iterations. That is a form of eval. They just don’t need formal process because the distance between builder and user is zero. That is not the case for 99% of AI products.

One more thing Ankur pointed out: a big use case for Braintrust has been helping companies collect evals they can share with labs so the labs can better support their use case.

When you have distance, you need a ledger to capture the information. Otherwise, how do you communicate it?

*The best PRD in 2026 is not a document. It is a data set, a task function, and a scoring function the whole team can run.*

---

## 4\. Offline vs online evals

![](https://substackcdn.com/image/fetch/$s_!VX_O!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d2f36b5-9939-4871-8b84-2df7956cbfab_2408x2348.png)

You have your eval running in a playground. Scores are improving.

That is only **half the picture**.

#### Workflow 1 - Offline evals test your hypothesis

This is what we built in the demo. A data set, a task, a scoring function. You run experiments on your laptop. You iterate on the prompt. You swap models. You see the score move from 0 to 0.75.

Fast. Cheap. Repeatable.

This is the AI equivalent of what used to require an A/B test. In the old world, non-deterministic problems meant expensive production experiments. Now you can run those experiments offline. That is why Braintrust customers average **12.8 experiments per day**.

#### Workflow 2 - Online evals test reality

Take the same scoring functions and run them on **real production logs**. Every time a user asks a question, the scorer evaluates the response.

If your offline eval achieves 0.75 but your online eval consistently shows 0.3, something is not translating.

#### Workflow 3 - The flywheel

The real power is in the loop:

1. Online evals surface examples not performing well in production
2. Grab those examples, add them to your offline data set
3. Your offline evals now reflect real user behavior, not hypothetical test cases
4. Iterate until scores improve
5. Push changes, repeat

This is the same continuous improvement flywheel I covered in the [evals deep dive](https://www.news.aakashg.com/p/ai-evals). Now you can see what it looks like in practice at companies like Ramp, Notion, and Dropbox.

The best teams run this loop daily. More on the specific ritual in the eval culture section below.

*Offline evals tell you what should work. Online evals tell you what actually does. The gap between them is your roadmap.*

---

## 5\. How to maintain eval culture

![](https://substackcdn.com/image/fetch/$s_!FOGE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd652d8bd-1daa-41b8-b8e0-feffb254cafb_2408x2152.png)

The biggest risk is not that your eval system is bad. It is that your team treats evals as a **gate** instead of an **iterative loop**.

#### Mistake 1 - Running evals only at the end

If you edit your prompt, test it on three examples, then run a full eval just to see if you can ship, you are doing it backwards.

Start from the eval. The best teams Ankur works with have a morning ritual. In standup, they pull up examples from the previous day’s production logs. They reconcile what they see with what their eval scores show. They find novel patterns that have emerged, add them to the data set, and grind on those failures all day. That is the job now.

#### Mistake 2 - Only having evals that pass

If every eval succeeds, you have blind spots. Either:

1. You do not understand what your users are hitting
2. You do not understand what is impossible today

Have failing evals. When a new model drops, rerun them first. Something interesting always happens.

And interesting does not always mean better. Gemini 3 Flash was outperforming Gemini 3 Pro on coding benchmarks but hallucinating more. Those nuances only surface with a full [testing](https://www.news.aakashg.com/p/ai-testing) suite.

This is also how you plan product launches around model releases.

Braintrust shipped Loop this way. They built the eval for the feature before they shipped it. The eval failed on every model they tried. Then Claude 3.7 came out and there was a huge jump. The eval passed. They shipped.

Ankur said there was a watershed moment where 3.7 was the first model that could look at its own work and improve. Prior to that, he said models were like a dog looking at itself in the mirror. They didn’t recognize they were evaluating a virtual representation of themselves.

Create the eval for the feature you want. Watch the models. The moment a model hits the quality threshold, you ship.

#### Mistake 3 - Siloing evals to AI engineers

Evals should not be constrained to engineers. Product managers need access. Domain experts need access. The people who understand the end user should be improving the scoring functions.

Zapier was Braintrust’s first customer. Ankur told a story about their CTO [Brian](https://www.youtube.com/watch?v=a9wO6GSAoGk), who has been there for a long time and is very successful.

When Ankur met him, Brian introduced himself as a full-time AI engineer. This guy probably doesn’t have to work, but Ankur said he has never seen anyone nerd out about AI as much as Brian does. Companies like Zapier have pre-existing product-market fit.

If Ramp doesn’t work, it is very bad. They don’t have the leeway to screw things up. The quality bar is high, the scale is real, and vibe checks can’t cover the surface area. That is why these companies gravitate toward evals.

Braintrust removed user-based pricing specifically for this reason. They realized evals should not be locked behind engineering seat licenses.

Going back to the PRD analogy: if only engineers can see and edit the PRD, the product reflects what engineers think matters. Not what users need.

*The teams that win are not the ones with the most sophisticated eval setup. They are the ones where evals are the first thing the PM opens every morning.*

---

## The whole game

Treat the eval as a first-class product artifact with a PM who owns the experience. The scoring function is the new PRD. The data set is the new user research. The flywheel is the new sprint cycle.

Open your platform of choice, write your first scorer, and run it on 5 real examples today. You will learn more in that first hour than in a month of vibe checking.

*The prompt is temporary. The eval is permanent. That is the whole game.*

---

![](https://substackcdn.com/image/fetch/$s_!cqkE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36564f57-23d1-4ed8-9988-9350fdf47e1a_3600x4500.png)

---

YOUTUBE TRANSCRIPT
Evals are one of the most important skills for building effective AI products.

The failure and success of AI products is driven by how good the evals they write are, how well they use them, and of course, how much they improve them.

One of the top eval companies used by Replit, Vercel, and Airtable is BrainTrust.

I think all the top AI companies understand that building a really good feedback loop from what their users are doing in production all the way through their evals that they can run offline is really, really important. Ankur Goyal is the founder and CEO of Braintrust.

Last year, they bagged a series A valuation of $150 million. This tweet blew up. This is literally affecting people's jobs who are product managers and heads of product. How should they be dealing with this controversy?

I think vibe checks are evals. I actually think this tweet is. I think one of the most important things is to have evals that fail. If you only have evals that succeed, then you don't know what problems there are.

Yeah, my brain immediately went to, well, it's improved the system prom. So why should anyone care about evals to begin with? Before we go any further, do me a favor and check that you are subscribed on YouTube and following on Apple and Spotify podcasts. And if you want to get access to amazing AI tools,

check out my bundle, where if you become an annual subscriber to my newsletter, you get a full year free of the paid plans of Mobbin, Arise, RelayApp, Dovetail, Linear, Magic Patterns, Deep Sky, Reforge Build, Descript, and Speechify. So be sure to check that out at bundle.akashg.com. And now into today's episode. Ankur, welcome to the podcast.

Thank you so much for having me.

I'm really excited to be here.

When I think of experts in the eval space, you have to be right at the very top of the list. But some people, they just rely on vibe checks. I've had some product leaders on this podcast who have created amazing AI features that have helped their company bag the next $500, $1 billion valuation just on vibes.

So why should anyone care about evals to begin with?

You know, I actually think vibe checks are a form of eval and there's this really popular Paul Graham essay that I think is very true. It's do things that don't scale and vibe checks are like the, you know, do things that don't scale analog for evals. When you do a vibe check,

you are using your AI product and then using a scoring function, which is your brain. to try to intuit whether the result is good or bad. And if it's not very good, then you might tweak the prompt or you might try a different model or adjust how your agent is architected, whatever it may be,

and then try again. What happens is that once your product gets into production, more people start using it, you have more subject matter experts and engineers at your company that are actually contributing to its quality, then the vibe check version of an eval stops scaling.

And you need a little bit more software and process and tooling to help you execute at a higher scale and with more predictable performance. And that's where what we normally think of as evals start to come in. But I actually think it's a whole journey and vibe checking is great. It's just one type of eval. You know,

I think one of the really new things about AI development is there's this kind of magical thing, ether, that we have to deal with, which is an LLM. And an LLM, not unlike a person that you might hire or work with, is somewhat unpredictable. You don't know if your app isn't working,

whether it's because the LLM inherently doesn't understand your task or maybe you haven't prompted or built around it well. I remember... A couple of years ago, right around when BrainTrust started, a lot of my really smart friends who were LLM skeptics would say like, hey, this LLM doesn't understand C++ or it doesn't understand my specific task,

even though it works for demos. I think nowadays people have mostly moved past that, but it illustrates the idea that it's hard to know where the responsibility lies. And I actually think that What the most clever, successful AI builders have proven, you know, Manus is a really good recent example of this,

is that the alpha in building a good AI product is kind of understanding that LLMs are imperfect, yet very capable. and figuring out how to work your way around that and make the most of what LLMs are able to do today with an eye towards what they can do in the future.

And that is really where evals come into play. They are a good way for you to treat the imperfection of LLMs from being kind of a mystery or a burden into a really fun and engaging product and engineering challenge that you can actually overcome. I think a lot of people are starting to recognize this,

especially as software and models and agents are changing constantly. One of the things I come back to is that an eval is a relatively durable thing that you can invest in. So let's say that you're working on a new product area, and you use the latest agent framework and use Opus 4.5,

which is the cool model right now, all of that might change. And you know, you and I were just joking about this a few minutes ago, like all of that might change in a couple weeks or a couple months. But if you invest in evals, and by that, I mean,

you do a good job of understanding what your users are actually trying to do with the product, and then you encode that as data and scores and eval flow, then even as the models and agents and everything change, you've actually set yourself up to continue iterating and build on an investment that you make.

And so I think the companies that have started doing that effectively, they're actually building true differentiation. If you believe that the way that you've wired together your agent today is is your differentiator, you're actually highly likely to fail because that's probably going to change in a couple months. On the other hand, if you build really good evals,

then you've built something that has a little bit more durability to it.

I've been preaching this message to everybody, which is like the harness around your LLM, everything from the memory to the evals, that is actually your more durable mode because the model underneath that continues to evolve. One of the interesting things you have here on this slide is you have the quotes from Mike Krieger and Kevin Weil.

And I think it's super notable because they're the product leaders at these companies. What do you see as the role of the product manager in defining the evals? You're running one of the most used eval platforms out there. Are product managers the main user of it or how do they interact with whoever the main user actually is?

oh yeah i think this is honestly not something i anticipated when we started and just a little bit of backstory i know there's some controversy about evals and coding products and stuff and i actually think it relates to this point so i'd love

to talk about that too but what we've seen is that if you're building an ai product you are now able to solve problems that software couldn't really solve before and the people who really really drive that level of creative thinking and software application outside of the sort of four lines of what software did before are product managers.

And evals are core to product managers' ability to do that. I actually have sort of shifted my thinking. I think of evals as kind of like the natural evolution of a PRD. So if you look at a PRD in 2015, it's an unstructured document that is a spec that is meant to communicate how you

should build something and what maybe the success criteria are for the product working. Fast forward to now, I think the modern PRD is an eval. It's actually something that an engineering team who maybe doesn't know everything about the product or the problem that they're solving can use to quantify how well

the software that they're building is able to solve the problem. And I think that actually means product managers are able to be a lot more effective because they go from providing kind of a qualitative spec that no one really follows. And it's always kind of annoying to reconcile the PRD with the actual product into

something that's very quantifiable. You can look at an eval and say, does this piece of software fit the eval or not? And oftentimes it will fit the eval and the product will still suck. And that means that it's actually on the product manager to then go and improve the evals.

And I think that's an area of leverage that product managers actually didn't have before.

Yeah, I would love to talk about this coding controversy that you referred to. This tweet blew up. I actually had somebody ping me about this like the day it happened because they were like, my boss was telling me about this because I've been championing evals in my own company, but Cloud Code is not using evals.

Have we been doing it all wrong? So this is literally affecting people's jobs who are product managers and heads of product. How should they be dealing with this controversy?

Yeah, for sure. I mean, I think a lot of coding tools also don't have product managers. And the reason is that the software engineers who work on the coding tools have relatively good intuition about what other software engineers want to do. And I actually think the same principle applies here.

As I mentioned earlier, I think vibe checks are eval. So I just think this, I love Swix. He's a good friend, but I actually think this tweet is factually incorrect. Like the fact that Other people, you know, Boris and other folks at Anthropic are using cloud code and likely providing

feedback about whether the model or cloud code itself is solving their problem. That is a form of eval. Sure, they don't have it necessarily as a quantifiable process. Maybe they do by now. We don't know. Or I certainly don't know.

Or maybe they don't use a tool or whatever and follow what someone might think of as an eval. But I think they are doing evals. If someone is trying out the product and they're providing feedback and then they're incorporating that feedback into iterating on the product, which I think they are, to me, that's doing evals. Now,

why are they able to get away without a structured process that is somewhat multidisciplinary with product managers and engineers? I think it's likely because the engineers are solving problems for other engineers and they're doing it at a company that's training the models that are also able to solve that problem.

So it's totally verticalized and you don't really need any third party intuition to solve the problem. If you go into another domain, like an AI company that is applying an LLM to solve healthcare problems, I think you're in a totally different world because they're probably not making the LLM themselves.

They probably have great software engineers who are passionate about healthcare, but are not necessarily healthcare subject matter experts. And then of course, there are product managers who are able to bridge from what engineers are working on to what patients or doctors, whoever the end user is, is actually experiencing.

My parents are both doctors, so I have a little bit of a soft spot for this use case. When I hang out with them and talk to them, I have almost no idea what they're talking about, right? They're using very specific jargon. They're talking about medical issues that are obviously very important and maybe

can be assisted by software, but I just don't have the intuition for that. And so evals become a mechanism for product managers in this scenario to help glue together the unknowns of how an end user might actually interact with a piece of software into something that is tangible that an engineering and product team

can use to iterate on and improve the quality of their product.

Today's episode is brought to you by the experimentation platform Chameleon. Nine out of 10 companies that see themselves as industry leaders and expect to grow this year say experimentation is critical to their business. But most companies still fail at it. Why? Because most experiments require too much developer involvement. Chameleon handles experimentation differently.

It enables product and growth teams to create and test prototypes in minutes with prompt based experimentation. You describe what you want, Chameleon builds a variation of your webpage, lets you target a cohort of users, choose KPIs, and runs the experiment for you. Prompt-based experimentation makes what used to take days of developer time turn into minutes.

Try prompt-based experimentation on your own web apps. Visit chameleon.com slash prompt to join the waitlist. That's K-A-M-E-L-E-O-O-N dot com slash prompt. ai is writing code faster than ever but can your testing keep up testcube is the kubernetes native platform that scales testing at the pace of ai accelerated

development one dashboard all your tools full oversight run functional and load tests in minutes not hours across any framework any environment no vendor lock-in no bottlenecks just confidence that your ai driven releases are tested reliable and ready to ship testcube scale testing for the ai era See more at testcube.io slash akash. That's T-E-S-T-K-U-B-E dot I-O slash A-A-K-A-S-H.

Nailed it in my opinion, which is that if you're not the end user, it becomes more and more important. And the more distance you have from that end user, like in a healthcare setting, the more and more important it is to create the evals. I think also one thing that probably CloudCode benefits from is that Anthropic in

their post-training is using a bunch of evals around coding. So even if CloudCode doesn't have formalized evals, we know Anthropic does.

Right. I think distance is the perfect way to think about it. and the end users all inside of you know one set of four walls and so the efficiency with which they're able to circulate feedback is very high and and therefore it may not need additional process or or whatever to help facilitate uh

the feedback as any of those points of distance start to increase you actually need a little bit more structure like one of the big use cases for brain trust has actually been helping our customers collect evals that they can share with labs so that labs can do a better job of implementing support for their use case.

So they need something. They need some ledger to be able to capture that information. Otherwise, how are they going to communicate it?

Makes sense. And you mentioned brain trust. I wanted to ask you, how big is brain trust today? What can you share, whether that's users, revenue, valuation?

Yeah, BrainTrust is about 100 people. We have many hundreds of customers and many tens of thousands of organizations using the product. We actually have a pretty generous free plan, which we intend to make even more generous over time. If you're a product manager or an engineer and you're working on a hobby project.

We want you to be able to use brain trust without having to really think about it. And growth has just been absurd. Nowadays, people are running about 10 times as many evals as they were this time last year. Today, people log about twice as much data per day as they did the entire first year of

brain trust being in existence. And it's just been incredible. I think what we've seen is that everything is growing in AI. Every individual LLM call is getting bigger. People are creating larger prompts. They're putting more context into their prompts. There are more LLM calls in every request that comes through because people are

building agents and agents are doing research and interacting more frequently with users and doing much richer work. And then AI products are actually achieving real product market fit. And so the number of requests is also growing very rapidly. And if you multiply those three things together,

you get this incredible explosion of interesting data that we see flowing through Braintrust.

Wow. So as of, I believe, October 2024, so a year and change ago, it was reported that you were valued at $150 million in that fundraise. Can you give us a sense of what the scale of growth has been since then?

Yeah, I think we have been very fortunate. We were cash flow positive for a very long time. And so we've been able to utilize capital actually very, very effectively. I think I can't share the very, very specific numbers now. But if you look at our revenue metrics and growth metrics,

we are more than an order of magnitude in growth on literally every axis. And if you look at just consumption growth, it's multiple orders of magnitude of growth. So it's been a pretty wild, I don't know what it is, 15 months since then.

That's crazy. And I think it's a testament to companies that you have as customers like Vercel and Replit and Airtable being so keen on evals. Why are all the hottest companies so focused on evals?

You know, I think when we started BrainTrust, we wanted to partner with entrepreneurs and builders who had companies that had pre-existing product market fit and were earnestly investing in AI. I'll just highlight Brian from Zapier, for example. Zapier was our first customer. Brian is the CTO. He's been working on Zapier for a long time.

And when I met him, he basically introduced himself as a full-time AI engineer. Now, this guy is like super successful. He probably doesn't have to work, but I haven't seen anyone nerd out about AI as much as Brian does. And the reason that we wanted to partner with these companies is that we knew that

they would only build and ship products that met a certain level of quality and they would hold themselves to a rigorous product market fit bar. but they were very earnestly adopting AI. And that has very much turned out to be true with all of the companies on this list and most of the companies that we work with.

And I think if you consider that, like that these companies have pre-existing product market fit, so they have to do things at some level of scale, they can't simply rely on on vibe checks, although they do a lot of vibe checking as as everyone should, they can't simply rely on it,

they have enough product market fit to actually drive real scale. And then they have products like if ramp doesn't work, it's very bad, you know, they can't they don't really have the leeway to screw things up. And so the standard for the quality of the products that they're shipping is very high.

You kind of mix those ingredients together. And it's very, very obvious from first principles that you need to run evals and take observability very seriously to implement a good product. And so honestly, it's been no surprise to me. I built brain trust as an internal tool when I led the AI team at Figma. And intuitively,

I've known for a long time just how critical evals are to being able to execute product well. And we've very much seen that play out with these companies who I think are very much on the leading edge of building great AI products.

So I want to get a little bit more tactical for everybody. You have on there the stat, which I think is pretty crazy, 12.8 experiments per day. What exactly are those tangibly? Like, what are people doing that they are running this many experiments per day? I remember 10 years ago, we were talking about 2015 PRDs, for instance.

We might run 12.8 experiments total in a quarter, let alone just on our evals in a day.

of AI is that experimentation, which used to be something that you would only run in production, is now something that you can do offline as well. And that is actually one of the things that I think contributes to so much rapid evolution of AI products. You're absolutely right.

If you had this non-deterministic problem that you had to solve, then you might have to A-B test it. And doing an A-B test is a very, very high fidelity, but very expensive way to get feedback about whether a non deterministic thing works or not in AI, because you're able to do evals and actually iterate offline,

you can do those experiments just on your laptop. In fact, in a few minutes, we're going to run some experiments with a prompt and an MCP server and try and improve some stuff. And I don't know if we'll run 12.8. But we're certainly going to run more than one experiment and iterate, you know, just just live.

What are the steps that we need to go through in order to define an experiment like this?

So this is straight from our docs. An eval consists of three things. And I think this is a very helpful framework because it allows you to simplify what might otherwise be kind of an overly complex or infinitely complex experiment. But an eval is literally three things. Data, which is a set of inputs.

So we're going to play with linear's MCP in a moment. An example of a piece of data could be, how many tasks do I have assigned to me? That could be the input question. And then optionally, you might have a ground truth answer, like 12. You might not, which is totally fine.

Actually, we're not going to have ground truth in the eval that we run. But if you do, you might be able to use it. The next part is a task. A task is something that takes an input and then generates an output. And a task could be as simple as a single LLM call.

Like you could just take the question and paste it as a message into GPT-5 nano and then get a response. Or it could be as complex as an agent. It might... do some research or call an mcp server it might call other llms it might call apis

or vector databases whatever it may be at the end of the day though it's going to produce some kind of output and that's the thing that you evaluate and then the last thing is scores scores take the data so they they know about the input they

know about maybe the expected output they take the output of the task and then their job is to produce a number between zero and one I think it's actually really, really important you normalize things between a fixed range, zero and one. And the reason that's important is that it forces you to make everything comparable.

So no matter what, like a week from now or a month from now, when you run a new eval, you'll be able to produce a score that's within the same range. And when you do that, that means that you'll be able to compare how the thing that you did today performs against the thing that you do tomorrow.

So it's kind of this forcing function for you to really simplify how you want to assess whether the thing is working or not. And then once you are creative and you figure out how to do that, you have a really nice artifact that allows you to continue testing and evaluating things.

OK, so data task scores. I think I got it. Let's see it in action.

Awesome. So we are going to create an eval entirely from scratch. There's no pre-written prompts. There's no pre-written data set. There's no pre-written scoring functions. This is going to be 100% live. Expect some fun nuances along the way. And let's have some fun. And by the way, I actually haven't done this demo before.

So Akash, if you have ideas or feedback about how we can evaluate this together, I'm all ears.

All right.

For those who don't know, Linear, if you're just on a Jira ecosystem, Linear is a competitor to Jira. So it's your task management tool. It's where you're putting down, hey, these are all the things our engineers are going to build.

We use Linear. It's been a fantastic piece of software for us. And Linear also uses Braintrust. So they're a good friend of ours. And I think they have a really nice MCP server, which is super cool. And we're going to use it actually as part of this.

So let's say that we're building a tool that allows us to ask questions about our task workload and understand what work do we have to do. So let's just write a really simple system prompt. You are a helpful assistant who answers questions from linear. OK. And let's create a dataset.

And instead of creating it from scratch, let's just use Opus to help us create the dataset. So it's going to look, it's going to know that we're working on something related to linear, and it's going to generate some test data. Okay.

Okay.

And for those of you who are wondering, you just said MCP, what is that usage? So model context protocol, it's just the standard definition. Basically, it's like the API that LLMs can use. So it's allowing the tool we're looking at, Braintrust, to get access to the data inside of Linear. And Ankur mentioned Brian.

Brian is the one who did the MCP Primer podcast episode nearly a year ago on this podcast itself. So if you want more, you can check that out. But it looks like we've got the initial test data from Opus. This is not the one from the MCP yet.

There's no MCP connection yet. And actually, I don't love this data. So this is asking questions about what linear is. Let's try to improve it. So I don't really, we know what linear is. We're trying to build a bot that helps us ask questions about the workload. So let's actually tweak it.

Actually, more questions about my linear project. For example, what tasks assign to me.

So creating stronger test data, in this case, making it more about tasks and kinds of tasks instead of just the high level it was before.

Okay, great. Last but not least, remove the expected answers since we don't know them. Models still love to hallucinate. You can open this 4.5. Okay, great. So now it's going to create this data. Of course, I can always edit it. So let's see, like, we don't do sprints at Braintrust.

So let's say, like, how many tasks need to be triaged? And now what we can do is just hit run. So it's going to use GPT-5 nano, which is one of my favorite models. It's super cheap and relatively fast. And let's see what it comes up with. OK, so this doesn't seem like a great answer.

What tasks are assigned to me? Happy to help with linear. What would you like me to do? Let's see. Are there any overdue tasks? I can help with questions about linear's usage. Okay, well, what we just did is a vibe check. And that means that we looked at some of these questions. We looked at the answers.

Akash, feel free to disagree. I think these answers are pretty bad. So now, before we actually try to improve them, what I'd like to do is be able to quantify that. And that is where scoring comes in. The benefit of quantifying it is that we're, of course, going to vibe check the improved results as well.

But the artifact that we'll produce by actually running these evals is something that our team could continue to use so that as we add more data, as we evolve the prompts, we'll have a quantitative signal about whether we're improving the thing that we're trying to improve. So now let's go back to Loop. By the way,

Loop is the agent that's built into Braintrust, and it works kind of like Cloud Code or Cursor. It has tools that are plugged into all of the nooks and crannies of our product, and so it can interact with data and prompts and run evals and stuff for you.

So anyway, we have these tasks, and we know they kind of suck. Let's just see if we can write a scoring function using Loop so we don't have to create it from scratch. So these answers aren't great. They are... vague and introductory, can you create a scoring function that makes sure that the answers actually answer the question?

And B, if they cite any information or include any facts about tasks, they cite a source.

Okay. Okay. And while this is coming up here in the lore of the podcast, the prior few Inival episodes that we had from Homo Hussein, Shreyashankar, Aman Khan, they all warned against numerical scores. They said that we need to go for more of like a binary yes, no. Here we're going for a score there.

Can you talk to us about that?

Yeah, I think the simple way to think about it is that jumping into scores like 0.2 or 0.4 before you have really justified the need to do that is not a good idea. And in fact, even though we are going to create numbers here, we're actually only going to create scores that fit a specific set of values.

Let's see what the model came up with here. So it only has three options. And if we look at what the definition of B is, it's partial. So it's saying it's missing citations for tasks, but it has some sort of answer. We can change that.

We can say that, hey, actually, I don't like the fact that it's doing that. I don't want to give you any partial credit in that case. So I think it's important not to overcomplicate your scores. And I think if you're creating LLM-based scores, you shouldn't ask the LLM to generate a number because that's not very clear.

It's useful to have clear criteria. But I actually disagree that every score needs to be binary. I don't think there's any... real justification behind that. In fact, I worked with the OpenAI team about a year ago and published a research cookbook that I can send a link to you to that walks through somewhat scientifically what is

a good thing to do and what is a bad thing to do and why. And so that might be a helpful reading if anyone wants to go one level deeper.

So here we've gone with categorical, and that should be all right.

Yeah, yeah. And you can always change it. If you think it's getting too complicated, you can simplify it. If it's not complicated enough, you can make it more complicated.

Got it.

So now let's run it with the score and see how it does. We'd hope that the score is quite low. If the score is high, that means that our vibe checks are not aligned properly with the score that we created. OK, good. So it's zero everywhere. If you look at one of these, you can actually see why.

So we have the model actually tell you the rationale. And so it labeled it as option C. And it says it doesn't answer the question. It doesn't provide any claims or specific facts.

Love it. It's accurate.

So now let's have a little bit of fun and actually connect this thing to the linear MCP. It's pretty easy to do that. You just click MCP and then linear has a nice HTTP based MCP. So we can just put the URL in and it will actually authenticate to my linear

account and give me a bunch of tools. Models can get somewhat overwhelmed by having a lot of tools. So I'm going to remove some of these just to keep it simple. We can always add them back or tweak this later.

That's an interesting insight around just selecting the tools that you need so that it doesn't accidentally choose the wrong tool. Today's podcast is brought to you by Pendo, the leading software experience management platform. McKinsey found that 78% of companies are using Gen AI, but just as many have reported no bottom line improvements.

So how do you know if your AI agents are actually working? Are they giving users the wrong answers, creating more work instead of less, improving retention, or hurting it? When your software data and AI data are disconnected, you can't answer these questions.

But when you bring all your usage data together in one place, you can see what users do before. for, during, and after they use AI. Showing you when agents work, how they help you grow, and when to prioritize on your roadmap. Pendo Agent Analytics is the only solution built to do this for product teams.

Start measuring your AI's performance with Agent Analytics at pendo.io slash akash. That's p-e-n-d-o dot i-o slash a-a-k-a-s-h. Here's the dirty secret about prototyping. You spend two weeks building a prototype. You validate your assumptions. Engineering loves the direction. Then what happens? You throw the whole thing away. Bolt changes this completely.

When you prototype in Bolt, you're not building throwaway mock-up. You're building real front-end code that integrates with your existing design systems. So when you hand it to engineering, they don't throw it away. They ship on top of what you've built. I use Bolt every single day. I host my land PM job cohort on it.

And honestly, I'm up till 2 a.m. some days just vibing in the tool, having fun and building. That's when you know a product is good. When you're using it past midnight, not because you need to, but because you want to. Check out Bolt at bolt.new slash akash. That's B-O-L-T dot N-E-W slash A-A-K-A-S-H. Link in the show notes.

I hope you're enjoying today's episode. Are you interested in becoming an AI product manager, making hundreds of thousands of dollars more, joining OpenAI and Anthropic? Then you might want to do a course that I've taken myself, the AIPM certificate ran by OpenAI product leader, McDad Jaffer.

If you use my code and my link, you get a special discount on this course. It is a course that I highly recommend. We have done a lot of collaborations together on things like AI product strategy. So check out our newsletter articles if you want to see the quality of the type of thinking you'll get.

One of my frequent collaborators, Pavel Hearn, is the Build Labs leader. So you're going to live build an AI product with Pavel's feedback if you take this AIPM certificate. So be sure to check that out. Be sure to use my code and my link in order to get a special discount. And now back into today's episode.

And by the way, you can always do that later and actually evaluate that. So one of the things that you could do here is actually keep all of them enabled, run it, and then maybe you don't get great performance. You could duplicate the prompt again and then try disabling some of the tools and

see if you get better performance.

Makes sense.

Okay, great. So we'll save that and let's try running it again.

It's fun how fast you can iterate here. And so this might be an example of those 13 experiments. They're constantly improving what they're working on, and you just get the results so quickly.

Exactly. Every time I click Run, actually, it is essentially running an experiment. OK, great. So it didn't actually do that well. Welcome to AI. So let's see what happened. Here it said, are there any overdue tasks? And this model said, I'm ready to help with linear tasks, but it doesn't actually do anything.

It just says what it can do, and it doesn't really solve the problem.

Wow.

Now, there's a few things we can do. One thing we could do is we could try a different model. So we could say, maybe let's try GPT-5 or GPT-5 mini and see if we get better performance. Another thing we could do is we could try to improve the system prompt.

So we could say, don't ask clarifying questions, please. Just use the tools and figure it out. Let's try it, actually. And a third thing we could do is we could go and actually edit the questions. Maybe the questions are not great. And maybe if we made them a little bit more specific, we'd get better results.

And then, of course, the fourth thing we can do is edit the scoring function. But I agree. I think my vibe check on the score, which was zero, is consistent with what the score actually was. So I wouldn't advise that we do that.

Yeah, my brain immediately went to, well, it's improved the system prompt. Maybe let's add a few few shot examples of how to run it. Maybe let's specify the tools. But we didn't go to that level quite yet.

Exactly. And as you can see, it actually didn't solve all of the problems yet. And OpenAI returned an error for one of them. But it seems like this one is actually pretty good. So let's take a look. Here's a quick digest of the 20 issues assigned to you. So it's actually talking to linear.

And then if we go and look at the score here, it says it doesn't include a citation. So it just mentioned that it got the digest, but it did answer the question. So it gave us partial credit.

Yeah, and it did a pretty good job citing its sources. So yeah, maybe that means we should improve the scoring function. Yeah. Yeah. So it looks like we probably want to iterate both on our system prompting and our scoring function. Exactly.

And by the way, I'm hand doing this just for the purpose of showing you that. But one of the things that I really love about loop is that I can say things like, I think the scoring function is too harsh. If the response contains any references to BRA tasks, then it has cited its sources.

So this will go update the scoring function. And could we do the same for the system prompt? Could we say, right now we're still failing on four out of the five, so can we add a few few-shot examples and specify which MCP tools in linear to use?

Absolutely. So here you can see it's edited the criteria for the scorer. We can hit accept and it will update it. Here's the updated one with the new criteria. Nice. And we can also say scores still... oh yes please it's offering to actually run the task and see how it scores oh yeah

so we can do one change at a time and check it first yeah let's just have it do that yep now that i'm back to becoming a coder thanks to vibe coding tools after 16 years being away i'm like one step at a time all right hmm yes please improve yep

the prompt yeah but not just with citations right Yeah. Okay. And if you wanted, you didn't need to use AI to do this. I think like a lot of people, this might be a process also that maybe the PM isn't necessarily controlling at this point, improving the system prompt.

It might be something that an AI engineer or an engineer involved with it is. But usually the PMs are pretty involved in the scoring function, going back to your point around evals or the new PRD.

Yes. And by the way, I want to edit this slightly. We should actually get rid of this prompt so it just focuses on this one, if that's okay.

Yeah.

Okay. So I'm going to remove this one so that it just focuses on the MCP-oriented prompt.

Yeah.

And then I'm going to say, please rerun the eval and then improve the prompt.

Right.

So now we can, you know, go make a cup of coffee or relax for a little bit. It's kind of fun, like watching a movie to see it actually do its thing and try to improve the prompt. And of course, all of this is versioned in brain trust.

So if it updates the prompt or it updates the score or something in a way that doesn't make a whole lot of sense, you can always revert back.

Yes, I think the AI is right. Instead of using all the tools, a lot of times it's just listing back what's available. So now it looks like, okay, it's going to go ahead and there we go. It's creating a system prompt kind of like how we were describing.

Exactly. Yeah, you can see those examples are right here. Yeah. Let's try it. And let's just let it keep ripping away.

Yeah.

You know, there was this kind of watershed moment we saw with Claude 3-7, where it was the first time we saw that a model was able to look at its own work and improve. I think prior to that, the metaphor that I use is it was kind of like a dog looking at itself in the mirror.

It didn't really know, you know, what... Whether it was a virtual representation of itself, sometimes models would assume the identity of the model that they were or the prompt that they were working on. But when Cloud 3.7 came out, things started to change. And that's actually when we shipped loop.

We had our own eval for this problem leading up to shipping loop. And the eval performed terribly. And then finally, Cloud 3.7 came out and it was a huge jump. And we realized this product idea might actually work. And it allowed us to really be aggressive about that.

That's really, really interesting. So you should be thinking about what the future state products are going to be, create the eval, then watch the models. Once the models hit the right set of quality, you can go ahead and release it.

Absolutely. I think one of the most important things is to have evals that fail. If you only have evals that succeed, then you don't know what problems there are. And that means that you either don't have a clear understanding of what problems your users are hitting, or you don't have a clear understanding of

of what is impossible today. And I think it's very, very important to have both. If you have evals that are failing, then when a new model comes out, the first thing you should do is just rerun those evals. And you'll be surprised that every time a new model comes out, something interesting is going to happen.

I heard like some people who are running a coding tool, 3Flash was somehow performing better on like a lot of coding benchmarks than 3Pro, Gemini 3Pro, but it was hallucinating more. These are like these nuances where you need to have a full eval testing suite to really understand which metrics improving versus which it's hurting.

For sure. And I think as with any benchmark, an up does not necessarily mean good. An up just means that something interesting happened. And I think more often than not, when you see something interesting happen in a benchmark, including an improvement, it means that the benchmark itself is broken.

But you should not necessarily hypothesize whether a benchmark is broken until you're able to reproduce it with some real data. So I am a big believer in doing really dumb, seemingly obvious things like just auto-generating silly questions about linear tasks or whatever it is, and then running stuff and confronting the actual generated outputs with your

intuition and using that moment as the opportunity to improve things. As opposed to spending a month creating a perfect golden data set that you think represents the problem that you're trying to solve and doing all this other prep work. I think you should just jump in and then start iterating.

So that's a real case for don't silo your brain trust licenses and user accounts to the AI engineers. Make sure that the PMs, maybe even the right go-to-market domain experts who really understand it, have access to the tool.

Yeah, I mean, we about, I actually don't remember, maybe three or six months ago, we sort of realized that brain trust should not be constrained to the AI engineering team. And we removed user-based pricing. So there's no user-based pricing. It's just based on how many evals you run and how much data you log.

You should just not worry about that.

Mm-hmm.

Looks like this thing is cooking and it's made some serious progress. I've been watching along as we've been talking and it's solved some problems like telling the model to use the tool. It's also solved the problem of the model asking for clarification. So I think in chat-based use cases, models are post-trained to ask for clarifying questions.

In the context of this demo, we're not giving it the opportunity to do that. We're just hoping that it generates a response from one question. And so it's really important that we tell it not to do that.

Yeah, it's very cool. I think it started with a partial score, then it said, okay, let me iterate on the system prompt again to get a full score. So it's really working through the problems.

And yeah, I mean, this is evaluation. I think a few things I'd highlight are that we touched all three parts of the workflow. We worked on the data set. We iterated it a little bit. From here, you might add more examples to it. You might tweak the ones that you have.

You could use loop to help you think about more examples to add. A second thing that we did is we actually worked on the task function itself. So we wrote prompt, we picked a model, we changed the MCP tools that were available to it. We could do more work there.

Like I think maybe switching to a better model might help us consistently get a better score. Oh, wow. It looks like we're now at 0.75 across the board, which is a huge improvement from where we were before. And then the third thing that we did is we actually created and then iterated on a scoring function.

So we made an initial one. You pointed out that the scoring function was being a little bit too nitpicky. So even though the response was citing the specific issues, it wasn't really giving it credit for that because it didn't have a link or something like that so we also improved and iterated on the scoring function to

better represent what our vibe check or in this case your vibe check was indicating was a little bit off about how it was working and i think that process that we just ran is is very very representative of how people do evals

So what is the distinction between offline and online evals? And when should people be doing it?

Yeah, so one of the cool things about the work that we did is we created a scorer. And even though we're using it in this playground, this isn't the only place that you could use the scorer. So if we go into the scorer list in Braintrust, you'll see that we have the scorer right here.

And we can actually run it on real live logs and deploy it into production. So that let's say we take this app that we built and we start using it. Every time we ask a question, it will actually run the scorer online. In fact, we can do that right now.

If we go back to the playground, we can save this prompt. Oh, it's right here.

And I'm loving this prompt. Yeah, hardcore. Great.

Yeah, exactly. And again, you're a product manager. So I think you probably correct me if I'm wrong, but you see this and you get some PRD vibes, right? And that's what I mean. Like this is a much more quantifiable version of thinking about what a product should be. And it's really fun, I think,

to actually be able to take product intuition and quantify it and turn it into something really tangible. So if we go, we can actually take that score that we created and run it online. So we have linear answer quality. We can run it on every LLM span and we'll run it on 100%.

We'll give it a name.

And then it's super easy to actually test these things out in Braintrust. So we had the prompt that we created here. There's a little built-in chat interface. So I can say, like, what tasks are assigned to me? And you can see it's calling this tool, and it's going to generate an answer.

And what makes this online as it's accessing the real data? Or when people talk about that distinction, what should they understand?

Yeah, so what's happening here is we'll go to it in a minute, but every time I use a prompt in Braintrust or whatever my app is, I'm going to be generating real live logs of my production application. And online evals are taking these scorers that we build and running them on your real live user logs.

And I think that's helpful for two reasons. The first is that it gives you insight into how well the same eval functions that you're using to test things offline are actually translating into real-world performance. So let's say that offline we are able to achieve a score of 0.75, which is not bad.

and then we run the same score online and we consistently see the result is 0.3, that means that maybe it's not actually working as well in the real world as we think it's working in our little simulation environment. And then the second thing is that it becomes a really good flywheel for you to find

examples that are worth including in your offline eval. So when you see that the score is 0.3, then you can actually filter down to the examples that are not performing very well and then grab them and add them into that same data set that we were using to assess things.

Wow, I have a lot of tasks assigned to me. I'm going to have to do some coding work after this. So if we go to our logs page, you'll see that right here, This is exactly the chat thing that we had and then the eval running. And it looks like we didn't do it.

Oh, it looks like we actually in the end did a good job. So I set it up to evaluate every step. Maybe you only want to evaluate the last step, but it looks like at the end it actually scored pretty well.

Nice.

So to summarize for people, your offline eval is based on that golden data set. And you can continue to improve that golden data set when you see a discrepancy between your performance on your offline, your online evals. You say, okay, everything we failed online,

let's potentially add that back in or those are candidates to add back in to your golden data set for what's running offline. Did I get that right?

Exactly. You can actually do that directly in our UI. So you just find examples that you think are interesting and then you can add them to the data set.

Okay, very cool. So how do you maintain trust in your eval system so people don't bypass it when they're shipping new features?

Yeah, I mean, I think that the best teams don't think of evals as a gate. They think of it as a core part of their iterative loop of actually improving things. And I think that the best workflow looks like looking at real production examples. In fact,

some of our customers have kind of like a ritual where every morning in stand up, they'll look at some examples from the previous day's usage of their product. And then what they'll do is they'll reconcile what they see with those examples with what their evals have. So let's say that the scores are very low for,

let's just use this linear example, questions related to our UI. It's like, huh, maybe we don't have that many questions related to UI tasks in our eval data set. So what they'll do is find these novel patterns that have emerged from their logs and then add them to the data set.

And maybe you do that in the morning. And then what they'll do is they'll grind that day and actually try to improve the eval performance on the things that they noticed. And that becomes a really helpful way to prioritize what you should actually work on and what it means to actually succeed on a particular endeavor, like

hey, it clearly looks like we're not doing well on questions related to UIs. Let's bring in a bunch of those tasks, add them to our data sets, reproduce that problem in our evals, and then go and iterate on it until we're able to produce a better result. And I think that's the best way to think about evals.

If you think about evals as instead, which a lot of people do, and I try to discourage folks from thinking about it this way. Instead, what you might do is, I think there's a problem. Let me edit my prompt to try to fix the problem and play with it on three examples.

And then, OK, it seems like it's better. Now let me go run a full eval run and see if I can ship this thing. I think you're not going to be as efficient because you're not thinking about the broader problem, which is represented in the data set, while you're actually making those iterations in the first place.

Amazing. Couldn't agree more. This, you guys, was a less than one hour masterclass into eval. So there's much, much more out there that you can go deeper. If people want to go deeper, Encore, where should they be going?

Well, you can reach out to us. www.braintrust.dev is our website. You can email me, ankur at braintrust.dev or reach out to us on X or Discord. We also have a user conference coming up. in February called Trace. So if you go to braintrust.dev slash trace, you can see information about signing up.

It's a zero bullshit practitioner led conference. So a bunch of talks from people like companies, from companies like Dropbox, Ramp, Notion, other folks that we talked about earlier, who are just going to talk about how they're solving these problems and would love to meet you.

all right guys for my money in 2026 whether or not you're building an ai feature or not right now every pm should be learning this skill i hope we got you excited enough to go out there and try this out maybe with a free brain trust account or something else whatever platform you are using Get out there.

Start iterating. You saw how fun it was. You saw how I was jumping in on how I wanted to do more of the system prompt. I think you'll feel that same excitement once you get your hands into a tool like this. So I hope we remove that barrier to entry for you guys.

And we'll see you in the next episode. Thanks for having me. I hope you enjoyed that episode. If you could take a moment to double check that you have followed on Apple and Spotify podcasts, subscribed on YouTube, left a rating or review on Apple or Spotify and commented on YouTube,

all these things will help the algorithm distribute the show to more and more people. As we distribute the show to more people, we can grow the show, improve the quality of the content and the production to get you better insights to stay ahead in your career. Finally,

do check out my bundle at bundle.akashg.com to get access to nine AI products for an entire year for free. This includes Dovetail, Mobbin, Linear, Reforge Build, Descript, and many other amazing tools that will help you as an AI product manager or builder succeed. I'll see you in the next episode.

---

## Where to find Ankur Goyal

- [X](https://x.com/ankrgyl)
- [LinkedIn](https://www.linkedin.com/in/ankrgyl/)
- [Braintrust](https://www.braintrust.dev/)

---

## Related content

**Newsletters:**

1. [AI Evals deep dive](https://www.news.aakashg.com/p/ai-evals)
2. [AI observability for PMs](https://www.news.aakashg.com/p/ai-pm-observability)
3. [How to build AI products](https://www.news.aakashg.com/p/how-to-build-ai-products)

**Podcasts:**

1. [AI evals with Hamel Husain and Shreya Shankar](https://www.news.aakashg.com/p/hamel-shreya-podcast)
2. [AI evals part 2 with Hamel and Shreya](https://www.news.aakashg.com/p/hamel-shreya-podcast-2)
3. [AI Evals explained simply with Ankit](https://www.news.aakashg.com/p/ai-evals-explained-simply)

---

*PS. Please subscribe on [YouTube](https://youtu.be/LR_WOmcE9WI) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/ankur-goyal-podcast) on 2026-05-23T14:53:14-04:00*
