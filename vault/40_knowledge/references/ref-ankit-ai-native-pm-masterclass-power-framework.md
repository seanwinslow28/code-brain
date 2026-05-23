---
title: "The Ultimate Guide to AI Native Product Management - Note & Recordings from Live Masterclass"
source: "https://thehellopm.substack.com/p/the-ultimate-guide-to-ai-native-product"
author:
  - "[[Ankit Shukla]]"
published: 2026-05-03
created: 2026-05-23
description: "Mindset, tools, concepts and real examples to help you grab this BIG career opportunity."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [product-management]
ai-context: "Ankit Shukla's two-day AI-native PM masterclass — Day 1 foundations + the POWER framework, Day 2 the technical machinery (LLMs, RAG, fine-tuning, agents, harness engineering). Long-form recap meant as a single revisitable reference doc."
---
If you have been hearing the phrase **“AI Native PM”** thrown around on LinkedIn, in job descriptions, and in YouTube thumbnails, you probably have a vague sense that it matters but no clear picture of what it actually means.

Most people assume it means knowing how to write a clever ChatGPT prompt or having Cursor installed on their laptop. That is a small piece of it, but it misses the bigger story.

Over the past two evenings, I’ve ran ran a two-day masterclass that walked through the topic from the ground up.  
Day one was a foundations session built around a whiteboard, real product workflows, and a framework called POWER.  
Day two went deeper into the technical machinery: large language models, RAG, fine-tuning, agents, and the new vocabulary of harness engineering.

**Here are videos from both days, followed by detailed notes:**

**Day 1:**

![](https://www.youtube.com/watch?v=et2esTkHFgU)

**Day 2:**

![](https://www.youtube.com/watch?v=CvLLYBWAXjY)

This post is a long-form recap of both days. If you missed the live sessions, or if you attended and want a single document you can revisit later, this is meant to be that reference. I have kept the order roughly the same as the sessions, but I have tightened the explanations so each idea stands on its own.

## Table of Contents

1. [What an AI Native PM Actually Is](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#what-an-ai-native-pm-actually-is)
2. [Before You Can Be an AI PM, You Have to Be a PM](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#before-you-can-be-an-ai-pm)
	- [The Three Phases: Discovery, Delivery, Distribution](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#discovery-delivery-distribution)
3. [The Three Types of People in the AI Era](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#three-types-of-people)
4. [The POWER Framework for AI Native Work](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#power-framework)
	- [P is for Possibilities](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#possibilities)
		- [O is for Opportunities](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#opportunities)
		- [W is for Workflow](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#workflow)
		- [E is for Engineering](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#engineering)
		- [R is for Reflection](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#reflection)
5. [The Mindset Shift: AI Is Like Fire](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#mindset-shift)
6. [Day Two: Building With AI Instead of Just Using It](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#day-two)
7. [What Large Language Models Actually Do](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#what-llms-do)
8. [The Six Limitations of LLMs](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#six-limitations)
9. [Working Around Hallucination and Indeterminism](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#hallucination-fix)
10. [How a Real Product Like Chat PRD Works](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#chat-prd)
11. [Solving the Context Problem with RAG](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#rag)
12. [Solving the Cost Problem with Fine-Tuning](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#fine-tuning)
13. [Solving Reactivity with Agents](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#agents)
14. [Putting It All Together](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_editor#putting-it-together)

---

## What an AI Native PM Actually Is

The session opened with a simple question to a room of nearly five hundred people: *“What is your definition of an AI Native PM?”* The answers ranged across the predictable spectrum. Someone who uses AI as a thinking partner. Someone who builds with AI rather than just using AI features. Someone who makes AI-informed decisions based on customer needs.

All of those are partially right. But Ankit’s working definition is sharper, and it is worth pinning down before going any further.

> An AI Native PM is a product manager who can identify the roadblocks in their own product management cycle and then choose the right kind of AI tool to remove those roadblocks, with the goal of **better outcomes** rather than **faster outputs**.

Read that twice. The two ideas inside it carry the whole point of the masterclass.

First, an AI Native PM starts from their own workflow. They are not chasing tools, prompts, or templates from someone else’s playbook. They look at their own job, find where they are stuck, and then go fishing for the AI capability that helps.

Second, an AI Native PM is not optimizing for time saved. They are optimizing for impact. If you build a product in one month instead of six, but the product earns the company nothing, you have not won. You have just generated a faster failure. The job of a PM is to ship things that move the business, and AI is a way to make those things bigger and better, not just quicker.

## Before You Can Be an AI PM, You Have to Be a PM

This was repeated several times across both days, so it is worth slowing down here.

The biggest mistake people make right now is trying to skip the basics. They jump straight to Cursor, Claude Code, NotebookLM, and Lovable without ever sitting down to understand what a product manager actually does. The result is someone who knows the names of fifteen tools but cannot tell you what discovery, delivery, and distribution mean.

So the session started with a whiteboard breakdown of the universal PM workflow. The job has not changed because of AI. The shape of it is the same as it was a decade ago. AI changes how you do the work, not what the work is.

### The Three Phases: Discovery, Delivery, Distribution

Every product manager, in every company, in every industry, operates inside the same loop.

**Discovery** is everything that happens before code gets written. The company hands you a business goal, or you create one yourself if you are senior enough. You research the market. You talk to stakeholders in sales and marketing because they sit closer to the customer. You look at competitors and trends. You collect data. You brainstorm. You generate a long list of opportunities, and because you always have more ideas than capacity (the classic PM problem of plenty), you validate which ones are worth pursuing. You prioritize them based on impact and cost. The output of discovery is a product roadmap, which is just a sequenced list of bets the product is going to make.

**Delivery** is the build phase. You translate the roadmap into product requirement documents (PRDs), then into user stories and tasks, then hand all of it over to engineers and designers who execute. Testing happens here too. The output is a shippable product.

**Distribution** is what happens after the build. You partner with marketing and sales to actually get the product into the hands of users. You define the ideal customer profile, design landing pages, write release notes, set up analytics, and run a go-to-market plan. Then users give you data and feedback, the loop closes, and you head back into discovery.

When Ankit asked the room where they thought a PM should ideally spend most of their time, the answers all pointed to discovery. When he asked where they actually spend most of their time, the picture flipped immediately. Most PMs are buried in delivery: standups, status meetings, alignment conversations with engineers, knowledge transfer sessions, expectation management, follow-ups, and yet another round of documentation.

The result is mediocre products. Because PMs cannot afford to spend time on real discovery, they take the safest possible bets. They copy competitors. They optimize for shipping rather than for impact. They never get the time to ask the harder strategic questions.

This is the gap AI is supposed to close. By absorbing the heavy lifting of delivery and distribution, AI gives the PM their time back so they can spend it where it actually creates leverage.

## The Three Types of People in the AI Era

Before getting into the framework, the session laid out a useful sorting tool. There are roughly three groups of people right now when it comes to AI.

**Group one: AI is just hype.** These are the skeptics. They believe AI is a passing trend, that it cannot be trusted, that it hallucinates too much to be useful. They are sitting it out. The polite way to put it is that they are paying an opportunity cost. The honest way is that they are quietly falling behind.

**Group two: the followers.** This is most people. They want to use AI but they need someone else to tell them how. They watch tutorials, search for prompts on YouTube, save templates, and copy workflows. They are at least moving, which puts them in the top ten percent compared to group one. But because they are always borrowing other people’s solutions, their advantage is shallow. The moment a workflow is publicly shared, it stops being a competitive edge.

**Group three: the inventors.** These are the top one percent. They look at their own situation and figure out how to apply AI to it. Nobody told them what to do. They saw a problem in their own day, asked whether AI could touch it, and built something. The example Ankit gave from his own work was using Claude Code to read three onboarding call transcripts from his cohorts and generate seven detailed user personas, which he then uses to vet every product decision he makes for HelloPM. Nobody had documented that use case anywhere. He built it because he had the problem.

The whole point of day one was teaching people how to move from group two to group three. And that is where the framework comes in.

## The POWER Framework for AI Native Work

Ankit is not generally a fan of frameworks, but this one is worth keeping. The five letters in **POWER** stand for **Possibilities, Opportunities, Workflow, Engineering, and Reflection**. Each one is a step. You are supposed to walk through them in order, every time you want to apply AI to something.

### P is for Possibilities

Before you can use AI, you have to know what AI can actually do. This is harder than it sounds because the surface area of these models keeps expanding.

At its core, AI right now does three things well:

- **Understand data**, whether that data is text, code, images, audio, or video.
- **Transform data**, taking a long document and summarizing it, or converting a meeting recording into action items.
- **Generate data**, producing essays, code, slide content, or emails from a short prompt.

Beyond those three capabilities, what AI can do is limited only by your imagination. Some people use it just to summarize meetings. Others extract insights. Others go further and have AI automatically create to-do items from the meeting and place them in the right person’s calendar with the right deadline.

A small example that captures this perfectly: AI image generation often introduces spelling mistakes and looks visibly machine-made. Most people stop there and either wait for the models to improve or skip image generation entirely. Ankit went a different direction. AI is excellent at writing HTML. So instead of asking AI to make an infographic image, he asks AI to design the infographic as a styled HTML page, then takes a screenshot. No spelling errors. Easy to edit. Fully under his control. That is what understanding possibilities looks like in practice.

### O is for Opportunities

Once you understand what AI can do, you have to look at your own work and find the right places to apply it. An opportunity is somewhere you spend a lot of time, or somewhere you would do better work if you had more time.

Two questions help you spot opportunities. *How much time does this task take?* And *how much accuracy does it require?*

If a task takes a lot of time and does not need high accuracy, hand it to AI without much fuss. If it takes a lot of time and does need high accuracy, use AI but keep a human in the loop. If it takes very little time, leave it alone. The point is to be deliberate. Time saved is one parameter, but it is not the only one.

Different companies have different opportunities. The discovery, delivery, and distribution map gives you a starting point. Are you spending all your time in alignment meetings during delivery? That is an opportunity. Are you only able to do competitor research on one rival because of bandwidth? That is an opportunity to scale to ten or twenty.

### W is for Workflow

This is where most people skip ahead and lose the plot. A workflow is the actual step-by-step way you do a task, broken down to the level where you can see the seams.

User research is a good example. The high-level workflow looks like this: identify users, reach out to them, conduct interviews, analyze the responses, build personas, then use those personas to make decisions. But each of those steps has its own substructure. When you conduct interviews, you need a set of questions. When you write those questions, you need to follow good interview principles, like the ones in *The Mom’s Test*, so that people cannot lie or flatter you out of useful information.

Once you write down your workflow at this level, the AI opportunities become obvious. You can ask AI to generate Mom’s Test compliant interview questions for a given product idea. You can take your interview transcripts and have AI cluster patterns into personas. You can simulate how those personas would answer follow-up questions before you go back into the field.

The discipline here is the same as classical product management. You start with the problem space (possibilities, opportunities, workflow) before you go anywhere near the solution space (tools, prompts, templates). Most people invert that order and end up with a hammer looking for a nail.

### E is for Engineering

Now and only now do you talk about tools. Engineering is the part where you pick the right kind of AI surface for the job. There are roughly four levels.

**Level zero is straight chat.** Open ChatGPT, Claude, or Gemini. Type your question. Get an answer. Refine with follow-up prompts. Around eighty percent of personal AI use cases live here. If you are writing an email, drafting a press release, or thinking through an idea, level zero is enough. Do not over-engineer.

**Level one is repeatable instructions.** When you find yourself doing the same kind of prompt over and over again, package it. Claude has Projects. ChatGPT has Custom GPTs. Google has Gemini Gems. They all do roughly the same thing: you give them a system prompt and reference materials once, and then anyone can use that mini-app to solve a recurring problem.

The session included a live demo of a Gemini Gem called *“Roast Your Resume”* that took a sample resume and returned a brutal but useful critique. The point of the demo was not the joke. It was that almost any recurring task you do as a PM can be wrapped in a Gem in five minutes.

This level also includes **Claude Skills**, which are sets of instructions Claude follows during a task. There is a public registry at *skills.sh* where you can browse community-built skills, including a Humanizer skill that strips AI tells from generated text, a front-end design skill, an AI image generation skill, and many more. You can install them or write your own.

**Level two is custom apps and prototypes.** When you need a real interface with multiple inputs, outputs, and user flows, you graduate to tools like Lovable, Google AI Studio, and Bolt. PMs traditionally needed engineers for this kind of thing. Now you can build a working prototype, a landing page, or a small experimental product in an afternoon. There are also automation tools like n8n, Make, and Zapier that sit between level one and level two for process automation.

**Level three is agents.** This is where you build something that can act on its own, on a schedule, without waiting for you to type a prompt. The session included a live demo of building a competitor tracker in Claude Code: identify the list of competitors, crawl their websites daily at 8am, write up changes in pricing, offerings, hiring, and marketing, and email a report. Claude asked clarifying questions about the business and the deliverables, then went off and built it. With Claude’s recently launched cloud agents, the agent can run even when your laptop is shut off.

The order matters. Most people jump straight to level three because it sounds impressive, then realize they have built a complicated thing that solves a problem nobody actually has. Start at level zero and only climb when the previous level cannot do the job.

### R is for Reflection

This is the step almost everyone skips. After the AI does its work, you have to look at what came back, find the gaps, and improve your approach for next time. Reflection is what turns a one-off prompt into a compound capability over weeks and months. It is also where evaluations come in, which day two covered in detail.

## The Mindset Shift: AI Is Like Fire

Before moving into the technical content of day two, the masterclass spent serious time on mindset. The most common reason people stay in group one is the hallucination objection. *AI makes things up. Therefore AI cannot be trusted. Therefore I should not use it.*

The technical answers to this are real. Evaluations let you measure how often a model is wrong. Better prompts reduce hallucination. Newer models hallucinate less than older ones, and the rate has dropped to roughly ten percent of what it was a couple of years ago. Retrieval augmented generation gives the model fresh, grounded data to work from. Post-training techniques have taught models that it is okay to say *“I do not know.”*

But the deeper answer is a mindset shift. Every powerful technology comes with risk. Alternating current still kills people every year, but humanity did not abandon electricity. We learned to insulate wires, ground sockets, and wear rubber soles. AI is the same. It is fire. Used carelessly it burns down the forest. Used well it cooks your food and powers your civilization.

If you spend your energy looking for AI’s mistakes instead of learning to control it, you pay an opportunity cost. The businesses around you have already taken the call. Either you learn the tool or you fall behind quietly while pretending you are taking a principled stand.

## Day Two: Building With AI Instead of Just Using It

Day one was about using AI to be a better PM. Day two flipped the angle: how do you build AI products? Because while there is real money in being a PM who uses AI well, there is significantly more money in being a PM who builds AI products that millions of other people use.

That means understanding what is actually happening inside the box, what the limits are, and what techniques exist to work around those limits.

## What Large Language Models Actually Do

A large language model is a neural network trained to predict and generate data. The companies behind them, OpenAI, Anthropic, Google, Meta, and others, took massive amounts of text from the internet, broke it into pieces, and used it to train a model that can take an input and continue it in a sensible way.

The technical depth of how this happens, what transformers are, how attention works, why these models are so good at completing patterns, is its own multi-hour topic. The masterclass pointed to a free 3.5 hour deep dive on YouTube for anyone who wants to go further. For the purposes of building products, what matters most is knowing what these models cannot do.

## The Six Limitations of LLMs

Every LLM has the same set of structural problems. If you want to build with them, you need to know these cold.

1. **Hallucination.** Models will confidently make up facts when they do not know the answer. This is a smaller problem than it used to be, partly because labs like Meta have explicitly trained models to say *“I do not know”* instead of fabricating, and partly because newer models are better at grounding themselves. But it has not gone to zero, and it never will. It is the nature of a pattern completion machine.
2. **Indeterministic output.** Ask the same model the same question twice and you will get two different answers. This is not a bug. It is what makes the models creative. But it means the same prompt cannot be relied on to produce the same output, which is a problem when you are building software that depends on consistency.
3. **Expensive.** Token pricing adds up fast at scale. Anthropic’s best model costs roughly five dollars per million input tokens and twenty-five dollars per million output tokens, while their smaller model is around twenty times cheaper. For a personal use case the cost barely matters. For a product serving millions of users, the gap between picking Opus and picking Haiku is the difference between a profitable product and a money pit.
4. **Reactive.** LLMs do nothing until you prompt them. They cannot kick off work on their own.
5. **Context limitation.** Every model has a maximum amount of input it can process at once. Even when the limit is huge (Claude’s million-token context window can hold several books), pushing too much into context degrades performance, increases hallucination, and costs more money. Bigger context is not always better.
6. **Locked memory.** A model only knows what it was trained on, up to the date of its training cutoff. Anything that happened after that is invisible to it.

The right way to think about an LLM is as a lion in a circus. The beast is powerful and capable of incredible things. It is also dangerous and unpredictable. The job of the ringmaster, which in this case means the AI product builder, is to design the leashes, the cage, and the performance space so the lion’s power can be used safely. That is what the rest of the day was about.

## Working Around Hallucination and Indeterminism

For hallucination, the tactical fix is good prompts and explicit grounding in real-time data, which is what RAG handles. The deeper fix is acknowledging that you can only reduce, not eliminate, and building guardrails around the parts of your product where wrong answers would hurt.

For indeterminism, the answer is **evaluations**. The same way a high-end restaurant runs a tasting check on every dish before it leaves the kitchen, your AI product needs an automated way to check whether each output meets a quality bar. Evaluations are detailed enough to deserve their own walkthrough, and the masterclass included a separate video resource on the topic.

## How a Real Product Like Chat PRD Works

The first concrete product example was **Chat PRD**. You give it a product idea. It returns a complete, well-structured PRD. Behind the scenes, the magic is unspectacular but instructive.

When you submit your idea, Chat PRD wraps it in a prepared system prompt that says something like: *“For the given user input, create a PRD with the following sections (objective, user persona, business goals, user flows, metrics, important questions). Make sure you draw inspiration from these examples.”* The system prompt also attaches two or three exemplar PRDs as references. The combined package is sent to an underlying LLM, which generates the document and returns it to the user.

That is the entire architecture. Your input plus a system prompt plus reference examples, sent to an LLM. The clever part is the prompt and the curated examples, not the model. Which is why you can replicate Chat PRD with a Gemini Gem or a Claude Project in a few minutes. Many tools you see being sold as standalone products are this same pattern with a UI on top.

## Solving the Context Problem with RAG

The next problem to tackle is context. What if you want a chatbot that can answer questions based on your entire company’s knowledge base, or a research assistant that can pull from your full Google Drive? You cannot dump all of that into a prompt. You will burn through context windows, spend a fortune on tokens, and degrade the model’s ability to focus.

The answer is **Retrieval Augmented Generation**, or RAG.

The analogy that makes this stick: imagine your nagging neighbor knocks on your door asking for sugar. You do not search every room of your house. You do not check the bedroom, the bathroom, the utility closet, or the dining hall. You walk straight to the kitchen, find the right shelf, scoop out some sugar, and hand it over. You retrieved the relevant thing from the relevant place.

RAG does the same thing for an LLM. You take all your documents and break them into small *chunks* (a paragraph, a page, a section). When the user asks a question, you search the chunks for the most relevant ones, usually five to ten. Then you build a new prompt that says *“Answer the following user query, based on these retrieved chunks,”* and send only that to the LLM.

The three parts of the name spell out the steps:

- **Retrieval:** pull the relevant chunks from your knowledge base.
- **Augmentation:** build a new prompt that combines the user’s question with those chunks.
- **Generation:** hand it to the LLM to produce the answer.

In real systems, the retrieval step uses vector search rather than keyword matching, which lets the system find chunks that mean the same thing as the query even when they do not share words. But the principle is the same.

**NotebookLM** is a polished consumer example of RAG in action. You upload sources (YouTube videos, PDFs, websites), it chunks them into a knowledge base, and then it lets you ask questions, generate FAQs, build mind maps, create study guides, and even produce podcast-style audio overviews from the same material. Every user gets their own private RAG system.

RAG also solves the locked memory problem. Whatever knowledge the model lacks, you can add to your retrieval database, and the model will be able to answer questions about it.

## Solving the Cost Problem with Fine-Tuning

The third problem, cost, requires a different technique. The case study used here was **Cursor**, the AI coding tool that became a billion-dollar company.

Cursor’s original problem was that they were just a UI. Every coding request a user made got forwarded to Anthropic’s Claude or OpenAI’s GPT. Users paid Cursor, and Cursor paid those LLM providers. As Cursor scaled, those API bills became enormous.

Their solution was to build their own model, called **Composer**. There was some controversy because they initially claimed it was fully their own, and the internet later figured out they had taken Moonshot AI’s *Kimi K2* model as a base and fine-tuned it on top. Cursor’s CEO eventually acknowledged this. But the technique itself is exactly right, and it is the third major lever for working around LLM limitations.

Fine-tuning means taking a base model and changing its parameters by training it further on a specific dataset. Unlike RAG, which adds knowledge at query time, fine-tuning bakes new behavior into the model itself.

To fine-tune, you need two ingredients: **a base model** and **training data**. Cursor used Kimi K2 as the base. For training data, they generated examples by running coding tasks through Anthropic’s Claude and OpenAI’s GPT, and they pulled from open codebases. After spending a few million dollars on the fine-tune, their model performed close to Opus on their internal coding benchmarks while being dramatically cheaper to run.

This is the same technique **DeepSeek** became famous for. When they claimed they had trained a frontier-level model for around ten million dollars, the internet eventually figured out they had used outputs from existing top-tier models to train theirs. Which is a strategy called **transfer learning**, sometimes described as *“standing on the shoulders of giants.”*

The mental model that ties RAG and fine-tuning together: **Opus is Superman.** He can do everything. But if you need cataract surgery, you do not call Superman. You call an ophthalmologist. Fine-tuning is the way to create a small, cheap, specialized doctor for the one thing your product does, instead of paying Superman rates every time.

The decision rule between the two:

- If your data changes constantly and varies by user, use **RAG**. NotebookLM uses RAG because every user uploads different sources.
- If your behavior pattern is fixed and you are going to use the model again and again at scale, **fine-tune** once and pay less forever. Cursor fine-tuned because every user is doing roughly the same kind of task (writing code).

## Solving Reactivity with Agents

The final problem is that LLMs are pure thinkers. They cannot do anything until you prompt them, and even then they can only return text. They cannot run code, browse the web, write to a database, or send an email on their own.

Stephen Hawking was a brilliant mind who needed a computer interface to interact with the world. An LLM has the same constraint. To make it useful in the real world, you have to wire it up to a body.

That body is called an **agent**. An agent is an LLM plus four supporting pieces:

- **Tools.** Functions the LLM can call. Web search, file creation, API requests, sending emails, executing code. The model decides which tool to use based on the task.
- **Memory.** Persistent storage so the agent remembers information across steps and across conversations. Without memory, every interaction starts fresh and the agent loses context as soon as the LLM’s context window fills up.
- **Environment.** The runtime where the agent actually operates. A Node environment for a JavaScript agent, your computer for a desktop agent, a cloud sandbox for a hosted agent.
- **Guardrails.** Rules about what the agent must and must not do. Do not delete files without asking. Do not execute commands without permission. Do not send emails without confirmation.

Stack one agent with another and you get **multi-agent systems**. One agent acts as the architect, another lays the bricks, another handles the cement, another finishes the marble. They pass tasks and information between each other, working in parallel like a human team.

The new vocabulary that has emerged for designing all this is **harness engineering**. We started with prompt engineering, which was about writing better instructions. Then RAG made context engineering important, which was about feeding the right information at the right time. Now harness engineering is the umbrella term that covers all of it: the LLM, the tools, the memory, the environment, the guardrails, all assembled into a working system. Claude Code and OpenCode are both examples of well-designed harnesses.

You cannot control how the underlying models evolve. But you can build excellent harnesses on top of them, and that is where most of the product value is going to be created over the next few years.

## Putting It All Together

Looking back across both days, the through line is consistent. AI is not a magic shortcut. It is a powerful set of capabilities that rewards people who think carefully about their own work, understand the limits of the technology, and build deliberately on top of those limits.

If you are a PM today, the practical sequence looks something like this:

1. Get your product management fundamentals solid first, because no AI tool will compensate for not understanding discovery, delivery, and distribution.
2. Walk through the POWER framework when you want to apply AI to anything.
3. Start at level zero of the engineering stack and only climb when you need to.
4. Build your own muscle by inventing use cases for your own situation rather than borrowing other people’s playbooks.

If you want to **build AI products**, learn the six limitations of LLMs and the three primary techniques for working around them:

- **Prompt engineering** for simple cases.
- **RAG** when you need fresh or grounded knowledge.
- **Fine-tuning** when you need cheap repeatable behavior.

Then learn to design good harnesses around these models so they can act in the real world without breaking things.

The people who do this well over the next few years are going to compound. The people who keep waiting for AI to *“settle down”* or who keep cursing it for hallucinating are going to fall further behind without noticing.

If you found this useful, the live recordings of both sessions are on the HelloPM YouTube channel, and the program runs cohorts roughly every couple of months for anyone who wants the full fifteen-week version.

Now go figure out one workflow in your week that you can rebuild with AI. That is the real homework.

**Here are resources as discussed in the session:**

1. Masterclass on AI Product Management:
![](https://www.youtube.com/watch?v=KjYCEiBTHFo)
2. Fundamentals of Product Management: [https://hellopm.co/hellopm-masterclass-resources-m31/](https://hellopm.co/hellopm-masterclass-resources-m31/)
3. Learn Vibe Coding: [https://hellopm.co/vibe-coding/](https://hellopm.co/vibe-coding/)
4. Learn Prompt Engineering: [https://hellopm.co/prompt-engineering](https://hellopm.co/prompt-engineering)
5. AI Evaluations with [Aakash Gupta](https://open.substack.com/users/4429439-aakash-gupta?utm_source=mentions)
![](https://www.youtube.com/watch?v=Raa3qjEBvKE)

**Important papers and articles:**

1. Attention is all you need: [https://proceedings.neurips.cc/paper\_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
2. Composer 2 - Technical Report: [https://arxiv.org/abs/2603.24477](https://arxiv.org/abs/2603.24477)
3. NotebookLM & RAG for Lung Cancer Staging: [https://arxiv.org/abs/2410.10869](https://arxiv.org/abs/2410.10869)
4. Prompt Engineering in LLMs - Technique and Applications: [https://arxiv.org/abs/2402.07927](https://arxiv.org/abs/2402.07927)
5. Harness Engineering by Anthropic: [https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
6. Harness Design by Meta: [https://arxiv.org/abs/2603.28052](https://arxiv.org/abs/2603.28052)

If you are serious about making a career in AI Product Management, do check out our detailed bootcamp here: https://hellopm.co

Thanks & Never Stop Learning!

---
*Clipped from [substack.com](https://thehellopm.substack.com/p/the-ultimate-guide-to-ai-native-product) on 2026-05-23T15:23:01-04:00*
