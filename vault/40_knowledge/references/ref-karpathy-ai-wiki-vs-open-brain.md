---
title: "Karpathy's viral AI wiki has a flaw most of the 100K people who bookmarked it haven't noticed yet"
source: "https://natesnewsletter.substack.com/p/your-ai-re-derives-everything-it?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-04-21
created: 2026-04-24
description: "Watch now | A few weeks ago, Andrej Karpathy posted an idea that more than a hundred thousand people bookmarked."
tags:
  - "source/web-clip"
type: "source"
status: draft
domain: [claude-mastery]
ai-context: "Nate's comparison of Karpathy's AI-compiled-wiki approach vs Open Brain's structured-database approach — when synthesis happens at write time vs query time."
---
A few weeks ago, Andrej Karpathy posted an idea that more than a hundred thousand people bookmarked. On the surface it sounded almost too simple: use your AI to build and maintain a personal wiki. You throw raw material into a folder, articles, research, meeting notes, whatever you’ve got. The AI reads all of it, pulls out what matters, connects ideas across sources, flags where things contradict, and keeps a running set of organized notes that gets smarter every time you feed it something new. No database, no special tools. Just folders, text files, and an AI doing the work of a full-time research librarian.

Since Karpathy’s post went up, I’ve gotten hundreds of messages asking some version of the same question: “Nate, is this the same thing as Open Brain?” “Does this make Open Brain obsolete?” “Is the wiki better?” The honest answer is more interesting than any of those questions assume. These two systems solve the same problem from opposite directions, and the difference between them is one of the most consequential design decisions you can make right now if you’re building anything serious with AI.

**Here’s what’s inside:**

- **The insight most of those hundred thousand bookmarkers missed.** The wiki isn’t the breakthrough. What matters is a deeper shift in how the AI relates to your knowledge over time, and almost nobody is talking about it clearly.
- **The fork that determines everything.** Every AI knowledge system has to decide when the hard thinking happens: at write time or at query time. That single choice shapes what the system costs, where it breaks, and what kind of trust you’re placing in the AI.
- **Where each approach cracks under load.** Specific failure modes for both the wiki and the database, including why a neglected wiki is more dangerous than a neglected database, and why most teams are choosing their architecture by accident.
- **The hybrid that gives you both.** A concrete architecture that combines [Open Brain’s](https://natesnewsletter.substack.com/p/every-ai-you-use-forgets-you-heres) structured storage with Karpathy-style compiled synthesis — and the wiki compiler recipe to build it.
- **How to decide what to build this week.** Clear criteria based on your actual situation: solo vs. team, research vs. operations, one project vs. long-term infrastructure.

This piece is the full comparison I wish someone had written before I started building.

## LINKS: Grab the prompts + Wiki Compiler (OB1)

Choosing between these architectures is one thing. Actually building one without stalling at the first design decision is another. The [prompt kit for this article](https://promptkit.natebjones.com/20260405_2ro_promptkit_1) walks you through that part: a diagnostic that tells you which architecture fits your actual situation, a schema designer that produces the editorial policy your wiki lives or dies by, a synthesis agent you can run every time you ingest a new source, an auditor that catches wiki drift and hidden contradictions before they compound, and a hybrid blueprint if you want both layers working together. Five prompts, each one built around a specific failure mode from the article.

If you already have [Open Brain](https://natesnewsletter.substack.com/p/every-ai-you-use-forgets-you-heres) running, the hybrid I describe below isn’t hypothetical anymore. The [Wiki Compiler recipe](https://github.com/NateBJones-Projects/OB1/tree/main/recipes/wiki-compiler) is live in the OB1 repo. It extracts entities and relationships from your stored thoughts, builds typed reasoning edges (supports, contradicts, supersedes), and generates per-entity wiki pages and topic-level synthesis pages from your database. You can run it on demand or schedule it as a recurring compilation pass. Your SQL stays the source of truth. The wiki is the compiled, regenerable view on top. If a page is wrong, you fix the underlying data and regenerate. That’s the whole point.

## Karpathy’s big insight (it’s not the wiki)

Before I get into the comparison, I need to explain why Karpathy’s post matters. Because on the surface it looks simple, maybe too simple. Folders and text files? That’s the big idea?

Yes. But the wiki isn’t the insight. The insight is about what the AI is doing.

Here’s how almost everyone uses AI with their documents today. You upload files to ChatGPT, or you use NotebookLM, or you set up some kind of retrieval system. Then you ask a question. The AI goes and finds the relevant chunks of your documents, reads them, and gives you an answer. This works. But what’s actually happening under the hood: the AI is rediscovering your knowledge from scratch every single time you ask.

Ask a question that requires connecting five documents? The AI has to find all five, read them, figure out how they relate, and produce a synthesis. Ask a similar question tomorrow? It does the whole thing again. Nothing was saved. No connections were preserved, no synthesis retained. The AI did real cognitive work and then threw it all away.

This is how ChatGPT file uploads work. This is how NotebookLM works. This is how most retrieval-augmented generation works. The AI is smart in the moment and amnesiac afterward.

Karpathy’s insight is: **what if the AI didn’t throw away the work?**

What if, instead of just finding relevant chunks and answering questions, the AI actually wrote down what it learned? What if every time you added a new source, the AI read it, figured out what mattered, and updated a set of organized notes, notes that already contained everything it had learned from every previous source? What if those notes included cross-references, flagged contradictions, tracked how your understanding evolved?

That’s the wiki. It’s not a clever file organization system. It’s a persistent artifact where the AI’s understanding lives. The AI reads a paper on Monday, writes up what it learned, and links it to what it learned last week. On Friday, when you ask a question, the AI doesn’t have to re-read everything from scratch. The synthesis is already sitting there, the cross-references already built, the contradictions already flagged.

Karpathy’s own words: “The knowledge is compiled once and then kept current, not re-derived on every query.”

That’s the sentence that matters. Most AI knowledge tools re-derive. His wiki compiles. That’s a fundamentally different relationship between AI and your information.

He described his working setup as having the AI agent on one side and Obsidian (a note-viewing app) on the other. The AI makes edits based on their conversation, and he browses the results in real time, following links, checking the graph view, reading updated pages. His metaphor: “Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.” In plain English: the note app is where he reads; the AI is who writes; the wiki is what gets built.

Think of it like this. Most AI tools are like having a brilliant research assistant who reads your entire filing cabinet every time you ask a question, gives you a great answer, and then immediately forgets everything they figured out. Karpathy’s wiki is like that same assistant keeping a running set of notes, organized, cross-referenced, updated, so that each question builds on the last one instead of starting over.

That’s why more than a hundred thousand people bookmarked the post. Not because folders and text files are exciting. Because “an AI that builds up understanding over time instead of starting from zero every session” is the thing everyone’s been waiting for.

But there’s a catch that almost nobody in those bookmarks is thinking about yet. Every time the AI turns a raw source into a wiki page, it’s making editorial choices. What to include, what to leave out, how to frame the connections between ideas. Those are the AI’s choices, not yours. Important nuance that got dropped might matter six months from now, and you won’t know it’s missing because the wiki reads so cleanly. This is the same trap as dashboards in analytics: a dashboard is easier to read than a spreadsheet, but it can hide exactly the thing you need to see.

Karpathy is honest about this. His architecture keeps all the raw sources untouched in their own folder, so you can always go back to the originals. But most people building on his pattern won’t maintain that discipline. In practice, the wiki will become the thing they trust. The source of truth will quietly shift from the raw material to the AI’s summary of it. And if the AI’s summary missed something, or framed something slightly wrong, that error is now baked into your understanding. You won’t question it, because it reads like something you already know.

## The fork in every knowledge system

Now here’s where Open Brain enters the picture and things get interesting.

Every knowledge system with an AI at its core has to answer one question: **when does the AI do the hard thinking — when information comes in, or when you ask about it?**

This is the fork. Everything else follows from it.

Karpathy’s wiki is a **write-time** system. When a new source arrives (an article, a paper, a set of notes) the AI doesn’t just store it. It reads the source, extracts what matters, and writes that understanding into the wiki. It updates topic pages. It revises summaries. It adds links between related ideas. It notes where new data contradicts something filed last week. The hard work happens once, at the moment information comes in. After that, you can browse the wiki and get pre-built understanding without the AI doing any work at all.

Open Brain is a **query-time** system. When new information arrives, it gets stored faithfully — tagged, categorized, made searchable. But nobody synthesizes anything yet. The data sits in structured tables, waiting. When you or your AI agent asks a question, the AI reads the relevant entries, does the thinking fresh, and produces an answer on the fly. The hard work happens at the moment you need it, not before.

Think of it this way. Karpathy’s wiki is like a study guide that a really good tutor writes for you as you learn a subject. Every time you cover new material, the tutor updates the guide, adding new sections, revising old ones, connecting ideas across chapters. When exam day comes, you just read the guide. The thinking has been done.

Open Brain is like a perfectly organized filing cabinet with a brilliant librarian standing next to it. Every document is filed, indexed, and searchable. When you need an answer, the librarian pulls the relevant files, reads through them, and tells you what they mean. The filing is pristine. But the librarian has to do the thinking fresh every time you ask.

Study guides and filing cabinets are both useful. They’re good at very different things.

## Why this matters for you

Now for the version that isn’t about architecture.

If you only store stuff, your AI has to figure out what it all means every single time you ask. You’ve been feeding it articles, meeting notes, and research for six months. You ask a question that requires connecting five different sources. The AI has to find those sources, read them, figure out how they relate, and produce a synthesis, from scratch. Every time. Nothing was pre-built. Nothing compounds. You’re paying full cost on every question, and the hundredth question isn’t any cheaper than the first.

If you only build a wiki, your AI can read the summary but can’t do anything precise with the raw data underneath. You want to pull every deal over $50K from the last quarter? Filter all meetings by client name? Have three different AI tools query your knowledge base at the same time? A folder of text files can’t answer those questions. The understanding is there, but the structured data to act on it isn’t.

You’ve probably noticed that your hundredth conversation with an AI doesn’t feel meaningfully different from your tenth. You’re more skilled at prompting, sure. But the AI itself hasn’t gotten any smarter about you, your domain, your accumulated context. No model upgrade will fix it. It’s a storage architecture problem, specifically the question of whether anyone is doing the work of turning raw information into compiled understanding, and whether that compiled understanding is available the next time an agent acts on your behalf.

For a team, the stakes are sharper. Most organizations are generating enormous volumes of AI-touched knowledge right now (meeting summaries, strategy docs, research outputs, Slack threads) and almost all of it is write-once-read-never. Nobody maintains it. Nobody synthesizes across documents. Nobody flags that the Q2 strategy deck contradicts what the CEO said in last week’s all-hands. Your company’s AI-generated knowledge is either a compounding asset or a growing pile of noise. The choice between these two outcomes is a design decision, and most teams are making it by accident.

And here’s a subtlety that matters more for teams than individuals: sometimes contradictions are the most valuable thing in your knowledge base. Engineering thinks the timeline is twelve weeks. Sales promised the client eight. A wiki that resolves that contradiction into one coherent narrative, picking a side or splitting the difference, actually hides the most important strategic signal in the system. The gap between what engineering knows and what sales promised *is* the problem your leadership needs to see. A database that stores both views without resolving them preserves that tension. A well-meaning wiki can smooth it away. For teams, the right system might need to *surface* contradictions side by side rather than resolve them into tidy prose.

## The AI’s job description changes

One of the sharpest practical differences between these approaches is what the AI actually spends its time doing.

In Karpathy’s system, the AI is primarily a **writer**. Its job is to maintain a document. When you add a new source, the AI reads the raw material, then writes or updates wiki pages: summaries, concept explanations, cross-references, an index. It’s doing editorial work. It’s making judgment calls about what’s important, what connects to what, and where the contradictions are.

In Open Brain, the AI is primarily a **reader**. Its job is to answer questions by pulling from structured data. When you or an agent asks something, the AI searches the database, reads the relevant entries, and produces a fresh synthesis. It’s doing analytical work on the fly.

Same AI. Completely different job description. And this has real consequences.

When the AI is a writer, you interact with it intensively when new information comes in. Adding a single research paper might trigger updates across a dozen wiki pages. That’s the heavy operation. But afterward, getting answers is cheap, because the thinking has been done.

When the AI is a reader, adding new information is cheap. Write a row, tag it, done. The heavy operation is every question, because the AI has to reconstruct understanding from data every time. Simple lookups are fast. Deep synthesis questions are expensive. And that cost recurs every time you ask something similar, because nothing was pre-built.

This difference raises a question most people aren’t asking yet: **whose understanding is it?**

When your AI maintains a wiki, and a colleague asks you about a topic, and you check the wiki before answering, are you sharing your understanding, or the AI’s interpretation of your sources? You’re trusting that the AI’s capture of your thinking is good enough to share with your colleagues as yours. With a database, provenance is different. These are facts, from identified sources, with timestamps. You can trace any claim back to where it came from. You know what you know, and you know why you know it. With a compiled wiki, you’re trusting not just the AI’s ability to retrieve information, but its editorial judgment about what matters and how things connect. That’s a deeper and more consequential kind of trust.

It also means the instructions you give the AI, the schema file that tells it how to organize your wiki, quietly becomes the highest-leverage document in the whole system. It’s not a configuration file. It’s an editorial policy for your personal knowledge base. The quality of that schema determines the quality of every synthesis the AI produces. Most people will underinvest in it, and the wiki will be worse than it should be as a result.

## What each approach is good at

Let me be specific.

**Karpathy’s wiki wins when:**

You’re deep in research. When you’re reading ten papers on a topic over two weeks, each one building on or contradicting the last, the wiki approach is dramatically better. By paper five, the wiki already contains a synthesis of the first four. Paper five gets integrated against that existing picture. Contradictions are flagged at the moment of ingest. Cross-references are built automatically. By paper ten, you have a rich, navigable artifact that represents the current state of your understanding, not just the current state of your files.

This also wins for personal knowledge that evolves over months (health tracking, self-improvement, competitive analysis), and for any domain where the value is in the connections between sources rather than in any single source alone.

The other place it wins: the wiki still works even without an AI in the loop. It’s human-readable text files. You can open them in any note app, browse the links, follow the connections. If every AI API went down tomorrow, you’d still have organized, useful notes. That’s a real form of durability that a database can’t match.

**Open Brain wins when:**

You need precise, structured operations across your knowledge. “Show me every meeting note from Q1 where pricing was discussed.” “Pull the three most recent competitor updates and compare them.” “Find all action items assigned to me in the last two weeks.” These are database queries. They return exact, filterable results. A folder of text files can approximate this with keyword search, but it breaks fast, especially when you need to combine filters, sort by date, or work across hundreds of entries.

Open Brain also wins for multi-agent access. When you have Claude Code, ChatGPT, Cursor, and a scheduled automation all needing to read from and write to the same knowledge store in the same hour, you need a database that handles simultaneous access, not a directory of files where two agents editing the same page creates a mess.

And it wins at volume. Open Brain handles thousands of entries across dozens of categories with search, metadata, and relational queries. Karpathy’s own research wiki runs to about a hundred articles. The pattern works well at that scale, maybe into the low thousands with extra search tooling, but it was never designed for the volume an organization generates. When you’re dealing with thousands of contacts, transactions, events, or tasks, structured storage is the only sane option.

## Where each one cracks

Every system has a load where it starts to break. Here’s where.

**Karpathy’s wiki cracks at:**

**Team use.** The moment two people (or two agents) try to update the same wiki page, you have a conflict. Not just a technical conflict — a semantic one. Two agents reaching different conclusions about the same concept from different sources. For a solo practitioner this is invisible. For a team, it’s a serious problem.

**Fast-moving domains.** If your knowledge changes daily (project status, competitive positioning, live deal flow) the cost of re-synthesizing the wiki on every update becomes punishing. Every change potentially ripples across multiple pages. Karpathy’s system is optimized for knowledge that moves at “papers and articles” speed, not “Slack messages and ticket updates” speed. If you don’t think about the speed of business your knowledge system was designed for, you’re going to implement the wrong one.

**Dangerous when neglected.** This is the one that worries me most. A neglected database just has gaps: the old facts are still true, there’s just missing recent stuff. A neglected wiki *drifts*. Old syntheses become increasingly wrong as new information doesn’t get integrated, but they still read with confidence because they’re well-written prose. Database staleness looks like ignorance, and you know you’re missing something. Wiki staleness looks like misinformation, and you don’t know you’re wrong, because the page reads like it knows what it’s talking about. Confident prose you don’t question is more dangerous than a gap you can see.

**Precise queries.** “How many sources mention transformer attention?” You’d have to read every file. “What percentage of articles were updated in the last 30 days?” There’s no structured metadata to query. “Give me all companies sorted by number of mentions.” You need a database for that, not prose.

**Open Brain cracks at:**

**Deep synthesis quality.** When a question requires understanding the relationships between fifteen different stored entries, the AI has to discover and reconstruct those relationships on the fly. It has no pre-built map. It’s searching shelves every time. For complex multi-source questions, the answer is usually good but rarely as good as a pre-built synthesis that had time to integrate everything deliberately.

**Browsability.** Open Brain is headless. There’s no artifact you open and wander through. You can build dashboards and briefings on top of it (and the Life Engine extension does exactly that), but the default experience is: ask a question, get an answer. For people who think by reading and exploring, following links, stumbling on unexpected connections, this is a real gap.

**Catching contradictions.** In the wiki, contradictions surface when new information comes in, because the AI is actively integrating against existing pages. In a database, contradictions sit silently in adjacent rows until someone asks exactly the right question to expose them. You can build periodic audits (and Open Brain supports this), but it’s a bolt-on, not a default behavior.

**Telling a story.** Databases store facts. They don’t tell stories. If you need “give me the overall arc of how my understanding of this topic evolved over six months,” a database hands you timestamped entries. A wiki hands you a narrative with cross-references. The difference matters for reflection, learning, and explaining your thinking to other people.

## The principles both systems share

What struck me most about these two approaches: they disagree on almost every implementation detail and agree on almost every underlying belief.

**You own the artifact, not the tool.** Karpathy’s files are text in a folder you control. Open Brain’s data is in a database you own. Neither system hands your knowledge to a platform that can reprice, deprecate, or lock you in. Karpathy calls this “file over app.” I’ve called it building with “no SaaS middlemen.” Same conviction, different file formats.

**The AI does the grunt work. You do the judgment work.** In both systems, the human’s job is curation and questioning. What sources go in. What questions to ask. What the priorities are. The AI’s job is the tedious, high-volume work nobody wants to do by hand: summarizing, cross-referencing, maintaining, updating, filing. Same division of labor. Only the specific tasks differ.

**Memory compounds through structure, not accumulation.** Dumping everything into a pile doesn’t make you smarter. Karpathy’s wiki compounds because each new source gets integrated into an existing web of interlinked pages. Open Brain compounds because each new entry is categorized, embedded, and relationally connected to everything else. Both systems reject the “just throw it in and search later” model that makes most AI knowledge tools feel like slightly better Google Drives.

**The knowledge base should be AI-native.** Karpathy designed his wiki to be worked on by Claude Code, Codex, or any AI that can read and write files. Open Brain was designed from day one for MCP — the open protocol that lets any AI tool connect. Both systems assume that the primary user of the knowledge base isn’t you reading in a browser. It’s an AI agent working on your behalf. Human readability is a bonus. Agent accessibility is the requirement.

## The hybrid I’d actually build next

If I’m being honest about what the mature system looks like, it’s neither of these alone. It’s both.

I’ll lay out the specific architecture I’d propose, and what I think should become the next major Open Brain extension.

**Keep Open Brain as your permanent store.** Everything goes in. Every meeting note, article clip, research finding, task, contact. Tagged, searchable, queryable. This is your durable memory layer. It handles high volumes, precise queries, multi-agent access, and recall across every domain of your life. It’s the source of truth.

**Add a wiki layer as the compiled view.** A new process where a compilation agent runs on a schedule (daily, weekly, or on-demand after major ingest). The agent reads from Open Brain’s structured data, synthesizes across entries, and produces wiki pages: topic summaries, entity profiles, trend analyses, contradiction reports, an index. These pages are generated artifacts. Think of them like a daily briefing that a really good chief of staff writes by reading everything in your files and distilling it into something you can actually browse.

**The compilation agent follows Karpathy’s patterns** — cross-referencing, linking related topics, flagging contradictions, maintaining an evolving synthesis. But it works from structured data, not raw files. That means it can do things Karpathy’s ingest can’t: filter entries by date or category before synthesizing, weight by confidence, exclude outdated items. The synthesis is richer because the underlying data is richer.

**The wiki pages are the easy-to-read layer.** Browse them in Obsidian or any note app. Your AI reads them for pre-built context before doing deep work. They’re your “hot” reference, and when you’re actively working on a topic, the wiki gives you instant access to the current state of your understanding without the AI having to reconstruct it from database rows every time.

**The database stays the single source of truth.** New information always goes into Open Brain first. The wiki is never edited directly. This prevents the error-compounding problem that several commenters on Karpathy’s post flagged: if the AI writes something slightly wrong into the wiki and it stays there, the next answer builds on that wrong thing, and errors accumulate. In the hybrid model, the database is always authoritative. The wiki is generated from it. If the wiki has an error, you fix the source data and regenerate. The wiki never drifts from reality because it’s always rebuilt from reality.

In Open Brain terms, this is a recipe, a composable workflow that reads from the database and produces output. A “wiki compiler” recipe would query relevant tables, synthesize pages through the AI, write the output to a wiki directory, and log the compilation. It could run on an automated schedule, getting better every cycle because the underlying data grew since last time. That’s the compounding loop.

What you end up with: Open Brain for structured storage and agent access. Karpathy-style wiki for compiled understanding and human browsability. The database feeds the wiki. The wiki never contradicts the database. You query either one depending on what you need — a precise fact or a synthesized narrative.

## How to decide what to build right now

**Build a Karpathy-style wiki if:** You’re going deep on one research topic. You’re a solo user. You don’t need precise queries or multi-agent access. You think by reading and browsing. You want something running in thirty minutes with zero infrastructure. Karpathy’s gist is designed to be pasted into Claude Code or Codex, and the AI builds the whole system for you.

**Build Open Brain if:** You need multiple AI tools accessing the same memory. You’re capturing high-volume information across many categories. You need structured queries. You’re building automated agent workflows. You’re thinking about this as infrastructure for years, not a single project.

**Build both if:** You have Open Brain running and you want a browsable, pre-synthesized understanding layer on top of it. Filing system plus briefing book. You need both, and neither replaces the other.

## What Karpathy got right that everyone should steal

Regardless of which system you build, two ideas from Karpathy’s post are worth adopting immediately.

**The idea file as a publishing format.** Karpathy didn’t write a tutorial. He didn’t ship a tool. He published a high-level description of an idea, designed to be pasted into an AI agent that would then build the specifics with you. This is a new way to share technical knowledge, a blueprint for an AI to execute, not a step-by-step for a human to follow. It respects the reader’s agency (you and your agent decide the details together) while giving them a proven pattern to start from. I think we’re going to see a lot more of this.

**The AI as maintainer, not oracle.** The deepest insight isn’t the wiki structure. It’s the role the AI plays. Most people treat AI as something you ask questions to. Karpathy treats it as something that has an ongoing job — maintaining a knowledge artifact that gets better over time. The AI isn’t here for one-off answers. It’s here for sustained work that compounds. The question is just the interface.

Open Brain embeds the same principle through extensions, recipes, and the Life Engine’s autonomous loop. But Karpathy stated it more cleanly than anyone: you never write the wiki yourself. The AI writes and maintains all of it. You curate, you explore, you ask the right questions. The AI does the grunt work.

That division of labor — human judgment, AI maintenance — is the real pattern underneath both of these systems. And it’s the pattern that makes AI knowledge actually compound instead of just accumulate.

## Where this is going

Karpathy noted there’s room for “an incredible new product” in this space. He’s right. But I think the product that wins isn’t a better wiki tool or a better database. It’s the hybrid — structured storage, compiled synthesis, multi-agent access, and human browsability in one stack.

There’s a deeper question hiding underneath all of this, though, and it’s the one that will determine whether Karpathy’s approach gets more important or less important over the next two years. His entire system is implicitly a bet that context windows (the amount of text an AI can process at once) will stay small relative to the amount of knowledge you accumulate. If you could dump everything into one enormous prompt, you wouldn’t need to pre-compile anything. You’d just let the AI re-derive every time.

Context windows are getting bigger. Gemini can already handle over a million tokens. So is pre-compilation dying?

No. And this is the part that’s easy to get wrong. There’s a real difference between “the AI can see all your documents” and “the AI has already thought carefully about how they relate.” Seeing isn’t understanding. A massive context window full of raw sources still requires the AI to do the synthesis work live, during your query, under time pressure. Pre-compilation means that work was done deliberately, with your guidance, not rushed. That distinction will matter even when context windows are ten times bigger than today. More input doesn’t eliminate the need for thought. It actually increases it.

So I built Open Brain to handle this too. The wiki compiler recipe is live in the OB1 repo. It reads your database, synthesizes across entries, and produces Karpathy-style wiki pages you can browse in Obsidian or any note app. Your database stays the source of truth. The wiki is the readable layer on top.

The tools are different. The principle is the same. And the people who get this right first will have an advantage that widens every single week.

---

*The Open Brain repo is at [github.com/NateBJones-Projects/OB1](http://github.com/NateBJones-Projects/OB1).*

*[Karpathy’s LLM Wiki gist can be found here.](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)*

*Both are free, open, and designed to be built with an AI agent at your side.*

![](https://substackcdn.com/image/fetch/$s_!T_vq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23abd7af-2f1f-48c5-9759-3d1c18cc87b0_1448x1086.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/your-ai-re-derives-everything-it?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-04-24T09:35:32-04:00*


TRANSCRIPT FROM YOUTUBE

## 41,000 bookmarks and hundreds of DMs

Everybody is going nuts about the wiki idea that Andre Carpathy posted a couple of days ago. 41,000 people have

bookmarked it. And on the surface, it sounds ridiculously simple. You use your AI to build and maintain a personal

wiki. As someone who launched something somewhat similar with OpenBrain, I have gotten hundreds of DMs and emails

saying, "Nate, is this the same thing? Nate, is this different? Nate, does this make OpenBrain obsolete? Nate, is the

wiki better?" I want to actually step back and give you a different answer

than you expected. We are going to go through, we are going to talk about what

the wiki approach gets right, why Andre put it together, the principles

underlying this wiki approach versus the open brain approach. And I want to be honest about why we're doing that. We're

not doing that just for giggles. We're doing that because deciding how you organize your context layer is one of

the single most important things you can do in 2026. It is a really big deal. And Karpathy's approach is really different

from OpenBrain. It's not the same thing at all. And there are specific reasons why he went with his decision and why I

went with the decisions that I made to construct open brand. And I'm going to be really open about both. I'm not going

to give you a steelman. I'm not going to say one is better than the other. So just get that out of your head. We're going to talk about where each one

breaks, the scale issues that each have, and where each one is strong. And then I

promise you, I am going to help you solve the problem because I know that what most of you are going to say is, "I want the best of both worlds." We are

going to get there. I put a plugin into OpenBrain that will help you have the

best of both worlds. So you can have the wiki approach Carpathy takes with the structured data that OpenBrain brings.

And by the end of this video, you'll understand why it matters to be able to do both and you'll feel equipped to make

that decision. So let me explain a little bit about what's under the surface that is a little bit more

complex than it might appear at first glance. Because on the surface, Carpathy's implementation is very simple. It's just folders and it's text

files. That is the big idea for him. And you might wonder why did he go so simple? Well, his insight is the idea

that everybody uses AI with their documents today all day, right? You upload files to chat GPT, you use

notebook LM, you use cloud, and you always end up in a place where you have bunches of documents everywhere and then

you ask a question and the AI has to go and find relevant chunks of documents, previous chats, reads them, gives you an

answer. It's all hyper fragmented all over. This works okay, but it's actually

not ideal because what's happening under the hood is that AI is effectively rediscovering your knowledge from

## The insight underneath the simplicity

scratch every single time you ask a question. So, if you ask a question that requires connecting five different

documents across six different chats, the AI has to find all five, read the six chats, figure out how they relate,

and produce some kind of a synthesis. If you ask a similar question tomorrow, it does the whole thing over again. Nothing

was saved about that synthesis. It doesn't inherently preserve connections between documents, even if you're in the

same chat application, let alone if you're in two or three different AIs like so many of us are. In other words,

the AI did real cognitive work and then threw it all away. And that is what

bothered Carpathy enough to put together a different solution. What he asked is, what if instead of just finding relevant

chunks and answering questions, the AI actually wrote down what it learned? What if every time you added a new

source, the AI read that source, figured out what mattered and updated a set of organized notes that already contained

everything it learned from the previous source? In other words, what if it started to auto update based on its own

synthesis? What if those notes already included cross references, flagged contradictions, tracked how your

understanding evolved? If you're trying to learn how you think and evolve over time, that's what this wiki idea is for.

It essentially becomes not just a clever file organization system, but actually a

persistent artifact as a whole where you're capturing the AI's evolving

understanding of your thinking over time. So the AI might read a paper you

give it on Monday, write up what it learned, and link back to it what it learned the previous week from some

other thread that you were working on. The next Friday when you ask a question, the AI doesn't have to reread everything

from scratch. Instead, it looks at the synthesis that is already sitting there, the cross references that are already built, the contradictions that have been

flagged. And in Carpathy's own words, the knowledge is compiled once and then kept current. It's not rederived on

every query. And that is really the key here. Most AI knowledge tools spend compute and tokens to rederive. whereas

his wiki compiles. That's a fundamentally different relationship between AI and your information and it

has different strengths and weaknesses than a lot of other predominant memory paradigms including OpenBrain. He

described his working setup as having the AI agent on one side and Obsidian which is just a note viewing app on the

other side. And so that allows the AI to make edits based on their conversation and he can browse the results in real

## Why AI throws away its cognitive work every time

time and follow links and check the graph view and read the updated pages and kind of have an evolving conversation with the agent. And of

course being a programmer the way he talks about it is the LLM is sort of the programmer for the codebase of the wiki

which means in plain English the note app is where he actually reads and the AI is the one writing in the notes app

based on a collected series of built documents. Some of them are raw sourced

that he inputs from previous chats. Some of them are docs. Some of them are synthesis the AI puts together. Think of it like most AI tools are like having a

brilliant research assistant who reads your entire filing cabinet every time you ask a question and then it gives you

a really great answer and then immediately forgets everything that it figured out. Andre Carpathy's wiki is

like that same assistant keeping a running set of notes that are organized and cross-referenced and updated so that

each question builds on the last one instead of starting over. I think that idea of being able to build on your

learnings is why 41,000 people jumped on it and bookmarked the post. Right? It's not because the folders and the text

files themselves are exciting. It's because an AI that builds understanding over time instead of starting from zero

is something we're all hungry for right now. It's the thing everyone's been waiting for. It's what made people really excited about OpenBrain. But

there's a catch that almost nobody in these 41,000 bookmarks is thinking about yet. Every time the AI turns a raw

source into a wiki page, it is making editorial decisions. It's making decisions about how to frame the

connections between ideas that may be right or wrong, but those are the AI's choices, right? They're not the human's choices. It's making synthesis choices

somewhat independently of what you may or may not think. And so important nuance could get dropped that m might

matter a few months from now and you would literally never know. You wouldn't know what's missing because the wiki

reads so cleanly. This is sort of the same trap as dashboards and analytics. A

dashboard is so much easier to read than a spreadsheet, but it is a condensation of data, right? It can hide exactly the

thing you need to see because it just shows only the thing that it thinks you

want to see in the moment. And to his credit, Andre Carpath has been very honest about this, right? His architecture keeps all the raw sources

untouched in their own folders. So he can always go back to the originals, which is a really smart design. But to

be honest, most people building on his pattern are not going to maintain the discipline to go back to raw sources. In

practice, I think the wiki will become the thing that is trusted as this open source project rolls out. And the source

## Knowledge compiled once vs re-derived on every query

of truth is quietly going to shift from raw material to an AI summary of that

material, which may be correct 80% of the time. maybe 90% of the time, but where it misses something or where it

frames something slightly wrong, there are going to be issues that arise and that errors will now be baked into our

understanding if that is the only way we're approaching memory. And you won't get in the habit of questioning it

because the whole premise of this when I started this video is that we are lazy people. It's really nice to have a wiki

where you can just chuck stuff in and it sort of automatically organizes, learns, and comes back with written artifacts.

And so this is where open brain enters the picture and things get really really interesting. Every knowledge system with

an AI at its core has to answer one question. When does the AI do the hard

thinking? Is it when information comes in or is it when you ask about that

information you got to pick that's the fork everything else follows from that. Carpathy's wiki is a right time system.

So when a new source arrives like an article, a paper, a set of notes, the AI does not just store it. The AI actually

actively works against it. It reads the source. It extracts what matters and it writes that understanding into the wiki.

It will update topic pages for you. It will write relevant summaries for you.

You get the idea, right? It's going to actively work to add links between

related ideas, develop concepts, note where new data contradicts something that was filed last week. It will do a

lot of that thinking at input, right? The hard work then happens one time at

the beginning, the moment the information comes in the door. After that, you can browse the wiki and get

pre-built understanding without the AI doing virtually any work at all. It's just retrieving. Open brain is

different. It is a query time system. When new information arrives, OpenBrain is designed to store it faithfully. It

tags it. It categorizes it. It makes it searchable. But we're not assuming that

you need to synthesize that information yet. Nobody's synthesizing. Nobody's doing work. The data is sitting in

structured tables waiting. When you or your AI agent asks a question, that's

when the AI goes to work. It reads the relevant entries. at that point at query time. It does the thinking fresh and it

produces an answer on the fly. So the hard work happens at the moment you need it, not before you need it. So think of

it this way. Carpathy's wiki is like a study guide that a really good tutor writes for you as you learn the subject.

## Write time vs query time: the fundamental fork

Every time you cover new material, the tutor will update the guide for you so

you don't get lost along the way. The tutor will add new sections, revise old sections, connect ideas across chapters,

and really help you dig in so that when exam day comes, you just read the guide, and you're good to go. Which is exactly

kind of how that wiki is supposed to work. Ideally, the thinking has been done for you. The tutor has prepared everything so perfectly, you can't fail.

Open brain is like a perfectly organized filing cabinet with a brilliant librarian standing next to that filing

cabinet for you. Every document is filed. It's indexed. It's searchable. So that when you need an answer, the

librarian can very quickly pull the relevant file, read through that relevant file for you, and then pinpoint

exactly what you need to find in that file. It will tell you what you're looking for. The filing is really clean

and pristine, and that enables the metaphorical librarian to do the thinking fresh in a very efficient way

every time you ask, so you get exactly the synthesis you're looking for. To be honest with you, I'm not here to compare

and contrast and give you an easy winner. Study guides and filing cabinets can both be useful, but they're good at different things, and I don't want them

compared inaccurately. And that's really important. So, why does this matter for you? This is the way to think about it

that's not about architecture. If you only store stuff, your AI has to figure out what it all means every time you

ask. You've been feeding it articles, meeting notes, and research for months and months and months and months. You

ask a question that requires connecting a bunch of different sources together. And the AI has to go and burn tokens. It

has to find those sources. It has to make sense of them. It has to read them. It has to think through them. It has to

understand what's going on, figure out how they relate together. And ultimately, it has to produce a

synthesis that actually works from scratch. And it has to do that every

single time. Nothing has been pre-built. Now, here's the other side. If you only build a wiki, your AI can read the

summary, but it cannot do anything precise with the raw data underneath. You want to pull every deal over $50,000

from the last quarter. You want to filter all your meetings by client name. You want to have three different AI

tools that query your knowledge base at the same time. A folder of text files cannot answer complex questions like

that. The understanding is there in synthesized form, but the detailed

structured data to make meaningful decisions just isn't there. And it isn't there by design. It's just not going to

be there. In addition, if you have three or more agents, that's just going to break when they're all trying to write

Markdown files at once. The wiki structure presupposes a single agent

working for you that just writes in one place. Whereas the open brain structure

assumes you may want to hook in multiple agents at multiple points to contribute to or pull from a structured database.

## Study guide vs filing cabinet with librarian

Let's move on from structured data to talk about a different kind of challenge with AI. It is difficult right now to

actually trace how an AI learns or improves over time when there is no

memory architecture under the system. And I want to talk about a distinction

between remembering detailed facts which open brain is designed to do and remembering narrative or synthesis which

the wiki is designed to do. And I want to help you understand how that plays out for a team because it's really

important to understand that our storage architectures shape the futures that we are unlocking for teams because that

we're effectively choosing a context layer that you need to make sense of,

use, input information into, believe, trust, and depend on for decisions. The stakes could not be higher. Most

organizations are generating enormous volumes of AI touched knowledge right now. We're generating meeting summaries.

We're generating strategy documents touched by AI. We're generating research outputs. We're generating Slack threads.

And almost all of it is write once, read never because nobody is maintaining any

of it. Nobody is synthesizing across any of those documents. Nobody is flagging

that the Q2 strategy deck contradicts what the CEO said in last week's all

hands. Your company's AI generated knowledge right now is either a compounding asset or it's just a growing

pile of noise. And so the choice between the two memory structures here is a lot

more than a design decision. It's actually the thing that most teams are making by accident that determines how

reliable their northstar compass in product decisioning is. And the subtlety that matters here is that sometimes

contradictions are the most valuable thing in your knowledge base. And one of the things that you worry about is that

you're going to lose the distinctions that you need to make good decisions in a wiki format. So engineering might

think the timeline for the build is 12 weeks and sales promise the client 8. And something like a smart wiki might

resolve that contradiction into one coherent narrative rather than flagging that you have a fundamental misalignment. And that is a strategic

signal in the system that you would not want to synthesize across with an estimate of 10 weeks. The gap between

what engineering knows and what sales promised is exactly the problem your leadership would need to see in that

situation. A database that stores both views without resolving them preserves that tension and a well-meaning wiki

might smooth those all away. So those are some of the structural differences. But if we go past the structural

differences in these two memory systems, the open brain system and the wiki system, I want to talk a little bit

about the job that the AI does in each system and why it's important to name

the AI job description really clearly. One of the sharpest practical differences between these approaches is

what the AI will spend its time doing. And you need to decide like where do you want to invest in your AI. In Karpathy's

system, the AI is primarily a writer. The job is to maintain a document. And when you add a new source, you have to

## The editorial trap in wiki synthesis

write to that, right? You have to read the raw material, synthesize it, write what you think about it. Update wiki

pages, connect new links, make sense of it, add concept explanations, cross

reference it, create an index. There's a ton to do. It's effectively doing editorial work. It's making judgment

calls about what's important, about what connects to what, and where those contradictions might lie. Whereas in

open brain, we think of the AI as primarily a reader. Its job is to answer questions by pulling from the structured

data and when you or an agent will ask something, the AI will just search the database that has been carefully read

and carefully organized, read the relevant entries and come back with a

precise, fresh synthesis based on all of the available data. So effectively, it

is doing the analytical work on the fly, but it's able to produce more detailed results because all of the detail is

immediately available in the database. And so those different job descriptions have real consequences. When the AI is a

writer, you interact with it intensively when new information comes in. Is that a job that you want to do? Do you want to

interact with it a lot when the new information comes in? it does adding a single research paper trigger updates

across a dozen wiki pages and is that something you're comfortable doing as you think through and and figure out the connections? It's a somewhat heavy

operation on the front end, but afterward you end up getting answers that are very cheap because all of your

thinking is captured in that wiki. The thinking has been done. When the AI is

more of a reader, as in open brain, what you get is adding new information is lazy and cheap. That's sort of why I did

it because I'm a lazy person and I want my stuff autocatategorized as cheaply

and easily as possible. We just write a row, we tag it and we're done. The heavy operation is when you ask a question

because the AI has to reconstruct understanding from the data each time. So simple lookups can be fast and

complex lookups will take time as the AI does deep synthesis because it's

actually interrogating the raw data. That cost is going to recur every time if you ask something similar. But on the

other hand, you are not going to lose detail if you need to get into the grounds and really understand what is

going on. The difference between these approaches raises a question that that I think most of us aren't asking yet.

Whose understanding matters here? When your AI maintains a wiki, what you are

effectively saying is that when a colleague asks you about a topic, you are willing to check the wiki and trust

what the AI says before answering. And you are trusting that the AI's capture

of your understanding or your thinking or the article you gave it is good enough to share with your colleagues as

yours. Whereas if you have an open brain style database, the providence is very clear. These are facts from identified

sources with timestamps. You can trace any claim back to where it came from. What you know, you know, and you know

why you know it. And you can come back with a fair bit of authority and say, "I'm not just trusting the AI's ability

## Dashboards hide exactly the thing you need to see

to synthesize information. I'm actually saying this is the raw material I got. This is the facts that I'm basing this

on, and this is a considered opinion based on a query across all of the data that I've collected over the last few

months or the last few weeks or whatever it is for you." That is a deeper and more consequential kind of trust. It

also means the instructions you give the AI that tells it how to organize your

wiki becomes the highest leverage document in the whole system. Because if you're building a wiki, I want you to

think about this for a second. If you're building a wiki, you basically are telling in one markdown file the AI to

organize and synthesize in a way that's profoundly useful to you and profoundly

accurate. and you're betting your career that it will get it right or you're going to invest time on every single

ingest to make sure it's correct and to doublech checkck it. Most people will underinvest in that and the wiki will be

worse than it should be as a result. Not because it can't be good, but because we're lazy. If we were to talk about

what each approach is good at and where the advantages are, I would say that Carpathy's wiki wins when you're deep in

research mode, when you're reading 10 papers on a topic over a couple of weeks, which sounds a lot like what

Andre does, right? like it's written for him. You could tell, right? And each one might build on. It might contradict the

last. It's a thinking person's tool. The wiki approach is going to be dramatically better in that situation

because by paper five, you're continuing to wrestle with it. You're continuing to read. You're giving input. The wiki

contains a synthesis of the first four. You've read all of the primary sources. You have them in your head as well. And

paper 5 can get integrated into that existing picture and help you evolve your thinking. contradictions get

flagged at the moment of ingest and you can see them really quickly. Cross references get built automatically. It's

basically an academic researcher's dream. And so by paper 10, you have a really rich navigable artifact that

represents the current state of your understanding of a very difficult subject. It's sort of like notebook LM

on steroid. It's not just the current state of your files. It also wins

because your personal knowledge evolves over months and you can actually see it grow. Right? So if you're thinking about

your health over months about self-improvement about competitive analysis for any domain where the value

is in the connections between the sources rather than in any single source

alone then that's where Carpathy's approach is going to win right because you're really looking at how it can help

you understand a complex synthesis problem but open brain wins when you

need precise structured operations across your knowledge base. If you want to ask, "Show me every meeting note from

Q1 where pricing was discussed," that's an open-brain type question. If you want to pull the three most recent competitor

updates and compare them, that's an open-brain question. Or find all actionable items assigned to me in the

last two weeks, open brain. Again, these are database queries, right? You are digging in for specific facts. They

return exact filterable results. A folder of text files can approximate this with some keyword search, but it's

## Where Karpathy's wiki wins: deep research mode

not going to be perfect, right? It's going to miss stuff. it's going to break fast and it's not really what that whole

wiki system was designed for, especially when you need to combine filters, sort

by date, or work across hundreds of entries. OpenBrain also wins for multi- aent access when you have clouded code

and chat GPT and cursor and a scheduled automation all working against the same data source at once, all needing to read

from and write to the same knowledge store at the same time. Well, you need a database that handles simultaneous access in that situation, not a

directory of files where two agents editing the same page creates a complete mess. And OpenBrain wins on volume, too,

right? OpenBrain can handle thousands of entries across dozens of categories with search, with metadata, with relational

queries. And and Carpathy absolutely acknowledges this. It works best at roughly 100 to 10,000 high signal

documents. It is not corporate level memory. And I hear corporations saying we should just use this for for our

company level context layer. And that will not work. And at the upper end, 10,000 documents, you already need extra

search tooling just to stay manageable. And so when you're dealing with thousands of contacts and transactions and events and tasks and documents on

top of all of that, structured storage is the only sane option that scales. But

to be fair, we should look at where both systems break, right? Every system has a load where it starts to break. They just

tend to break in different ways. So as I've called out, the wiki approach tends to break at scale. So, if you have a

team that's using it where you are starting to hit that wiki structure from multiple directions, well, now the wiki

doesn't know how to autooptimize, right? If person A has an understanding that's evolving differently than person B or or

agent A and agent B all have different approaches and they're trying to update the same wiki page. One, you have a

conflict and that's going to be a problem. But two, the wiki is going to look like a weird merge of these

different approaches that doesn't reflect deep personal understanding. Fundamentally, the semantic understanding that you're evolving with

the wiki is designed for a world that's kind of like Andre's world where he's a researcher and he's thinking deeply

about a problem and it's for him and it's his evolving understanding with the agent. So for a solo practitioner, you

don't get issues here. But for a team, this becomes a really serious problem. If your knowledge changes daily, if you

are an operation where you have project status, you have competitive positioning, you have live deal flow, the cost of reynthesizing the wiki every

time something comes in becomes really punishing because every change potentially ripples across multiple

pages in ways that you can't control. And it should not, right? It should just be another data point in the row. And

so, think of the wiki system as being optimized for like papers and articles speed, not Slack message and ticket

update speed. And that's the thing that worries me the most is that people don't recognize that a particular knowledge

system is designed to work at a particular speed of business. And if you don't think about it that way, you might

implement the wrong one. A neglected database has gaps, but the old facts are still true. as opposed to a wiki. A

neglected wiki tends to drift because old syntheses become increasingly wrong

## Where OpenBrain wins: precise structured operations

as new information is not integrated, but they still read with the confidence that comes from well-written pros. And

so database staleness can look like ignorance. It can look like you're missing something. I forgot to put stuff

into my open brain. But wiki staleness looks differently. It actually looks like active misinformation because you

don't know that you're wrong because the page reads like it knows what it's talking about because that is the entire purpose. It's supposed to synthesize

stuff and write confident pros that helps you understand a situation and you might not question the gap that you do

not see. Now, let's get at some of the scale breakpoints for OpenBrain. And by the way, yes, I am launching fixes for

these because that's what we're all about with AI. We make things better over time. In the past, Open Brain has

really cracked around deep synthesis quality. If you try to synthesize 15 different facts at once, the AI can do

it, but it tends to do it in slightly unpredictable ways because it has no previous map of how that worked in the

past to do it well. It's essentially searching the shelves of the database every single time from scratch. Now, the

answer is usually good because the AI is good, but it's rarely as good as a

pre-built synthesis that had the time to integrate everything deliberately from the beginning. And that is something

that we're addressing. Browsability is another area that we can think about here. Open brain is deliberately

headless. There's no artifact you open and wander through. And I built it that way because it gives you the flexibility

to decide how you want to access it. Now, the nice thing is it's very very easy to build the right head over the

top. There are people who have added Obsidian to OpenBrain. There's a plugin for that already. So, if that's something where you're like, I just I

just can't browse the database, you're absolutely right. Just pick the plugin of your choice and you can browse it.

whether that's Obsidian or something else. Here's another one we're building to improve in the wiki. Contradictions

surface when new information comes in as long as your initial markdown file deliberately says look for contradiction

because the AI is actively integrating against existing pages following your prompt. But in a database environment,

the contradiction might just sit silently in adjacent rows unless you

specifically ask the right question to expose that contradiction. I'm building a plugin that helps with that. If you

are interested in essentially running audits that check for contradictions in your data set, we're launching a plug-in

that helps you use OpenBrain as a contradiction surfacing tool. You can

actually build out and understand a map of the contradictions in your team or your org data sets really, really easily

because you can look through the raw material and see it right away. Yes, databases store facts. they're not

contradiction aware by default, but it's relatively easy in the age of AI to extend something like open brain and

make it aware of those contradictions. That's what I did. And I know I've spent a lot of time talking about differences, but one of the things I want to call out

is that there are a lot of common principles that these systems share. They might disagree on implementation

details, but a lot of the underlying thesis or principles about AI and about data they agree on. They agree that you

## Multi-agent access and volume scaling

own the artifact, not the tool. So, Carpathy's files are text in a folder you control. Open brains data is in a

database you own. It's the same principle. Neither system hands your knowledge to a platform that can repric

or lock you in. Carpathy calls this file over app. I've called it building with no SAS middlemen. It's a very similar

mindset. It's the same conviction at root. In the age of AI, we should own our own context layer. Right? There

should not be someone who is out there whom we are paying just to own our context layer. Also, in both systems,

the human's job is curation and questioning. We have to ask what sources go in. We have to figure out what

questions to ask. We humans retain a big job in both cases. There's no substitute

for thinking carefully about how to organize your personal context layer.

And yes, the AI has lots of work to do. It has to understand the facts that you

put in an open brain. It has to be able to effectively synthesize on the wiki side. It's effectively a similar

division of labor. It's just timing that work differently because on the carpathy wiki approach, it's doing all of that up

front and on the open brain approach, it's doing all of that at query time when you ask. In both cases, memory

compounds through intentional structure, not just through random accumulation. The only difference is how that

structure is positioned and where that structure lives. So it might live in a wiki in Karpathy's case and it lives in

a SQL database in OpenBrain's case. But in both cases, the structure is intentionally framed to enable a certain

kind of connection to occur. And so for wiki work where you might want the

connections to be between documents, that makes a ton of sense, right? You want all of the documents there. You

want the AI thinking it through. And that's an intentional structure. Whereas for OpenBrain, the intentional structure

is a SQL database that you know can scale and it is designed to hold operational facts and make sure that

they are in a neat place where you can reason against them and get audit ready results from day one. Both systems

assume that the primary user of the knowledge base isn't you reading in a browser. It's an AI agent working on

your behalf. And I think increasingly that's going to be the assumption of all of these memory systems. Human

readability is a bonus. Asian accessibility is actually the requirement. So now we come to what I've

built because let's be honest, we want a mature system that gives us the strength of both approaches. It's not either of

those alone. And so the specific architecture that I'm putting together and proposing is the next major open

brain extension. You want to keep openrain as your permanent store. Don't change that. It's

a great spot for fax. Everything goes in there. That's fantastic. Every meeting note, every article clip, every research

finding, every task, every contact, it's all tagged. It's all searchable. It's all queryable. That makes sense. That is

your durable memory layer right there. And it can handle high volumes. It can handle precise query. It can recall

## Where each system breaks at scale

across multiple domains in your life. It can be the source of truth. And a wiki layer can act as a compiled view on

demand. And and so I'm launching a new process, a new plug-in where a compilation agent can run on a schedule

daily, weekly, on demand. And the agent can read from open brain structured

data. Effectively, it becomes an open brain graph. It can synthesize across

entries. It can produce wiki pages on demand. It can produce topic summaries. All driven by the idea that if you form

a graph of your knowledge base, you can get the advantages of the wiki approach

with the solidity and the factuality that comes from an open-brain SQL database. And so these pages can be

generated artifacts for you. Think of them like a daily briefing that a really good chief of staff writes by reading

everything in your files and distilling it into something you can browse. The graph approach allows you to follow

Karpathy's patterns for synthesis to cross reference to link related topics to flag contradictions to maintain an

evolving synthesis but it works from structured data not raw files and that

means it can do things Carpathy's ingest can't like filter entries by date or category before synthesizing. It can

wait by confidence. It can exclude outdated items. In other words, the synthesis is richer because the

underlying data is more detailed. The wiki pages are an easy to read layer and

you can browse them in Obsidian. You can browse them in a note app, but they're all powered by a pre-built context graph

that lives on your structured data that would not exist without your structured data. They end up being your hot

reference for when you're actively working on a topic. And the structured data ends up being like the raw files

that Carpathy uses when he wants to look at the raw material in his wiki. But unlike the raw files, these are easily

queryable and organized in a SQL database. So you can scale them in a way that you can't with raw files. You do

not have a 10,000 file limit with OpenBrain in the same way. So the database stays the single source of

truth. New information always goes into the core SQL open brain first. The wiki

is never edited directly and this prevents the error compounding problem that several commenters on Carpathy's

post flagged. If the AI writes something slightly wrong into the wiki and it stays there, the next answer will build

on that wrong thing and you start to get drift and errors start to accumulate. Whereas in the hybrid model that I'm

proposing with OpenBrain, the database is always authoritative. The wiki is generated from a graph built off of that

database. So if the wiki has an error, well, you fix the source data and you

regenerate. You're not dependent on the wiki as a source of truth. The wiki never drifts from reality because it's

always rebuilt from ground reality in the SQL database. In open brain terms, this is like a recipe. It's a composable

workflow that reads from the database and produces an output based on a graph. A wiki compiler recipe can query

## Wiki stillness vs database stillness

relevant tables, synthesize pages through AI, and effectively develop a network of relationships and write that

output to a wiki directory. And if you're wondering, yes, it can run on an automated schedule. It can get better

every cycle because the underlying data hopefully, if you're committing to it, grew since last time. It becomes a

compounding loop as long as you are good at putting data in. And so what you end up with is OpenBrain for structured

storage and Asian access and a Carpathy style wiki over the top for compiled understanding and human browsability.

The database ends up feeding the wiki and the wiki never contradicts the

database. You can query either one depending on what you need, whether it's a precise fact or a synthesized

narrative, and you can decide which you want to go for depending on the kind of problem that you're solving. And so just

to be really really blunt about which of these because I know I'm going to get asked which do I build? If you are going

deep on a single research topic, if you're a solo user, if you don't need precise queries, if you don't need

multi- aent access, if you want to think by reading and by browsing, you want

something running in 30 minutes with zero infrastructure. In those situations, then it absolutely makes

sense to use straight up Carpathy's wiki that he posted on the GitHub because the AI will build the whole system for you

and it's designed for exactly that kind of solo use case. But you should build with open brain if you need multiple AI

tools accessing the same memory. If you are assuming that you have a team working with this information, if you're

capturing high volume information across many categories, if that information is not necessarily narrative based, if it's

numbersbased, if you need structured queries, if you're building automated agent

workflows off of this, if you're thinking about this as infrastructure that lasts for a long time and needs to

scale and not just for a single project. In a sense, a lot of what the wiki feels

like is a better, cooler version of Notebook LM, which is an amazing tool,

but not a tool that you can use for an entire team. And so, right now, I tend to say have it both ways. Have your open

brain running, and if you want a browsable presynthesized understanding layer, just grab the graph plugin and

add that over the top. And then neither replaces the other, and you get the benefits of both. None of this is to say

that Andre Carpathy isn't right about what he built. He built a phenomenal tool for himself and for other researchers in a similar position. And

regardless of which system you end up going with, there are two ideas from Karpathy's post that are worth adopting

## The hybrid: OpenBrain graph database plugin

right away. The idea file as a publishing format is one of those. And

one of those is really simple. It's the way he shared it. The idea file is his publishing format. Carpathy didn't ship

a tool. He published a high-level description of an idea that was designed to be pasted into an AI agent that would

build the specifics with you. This is what I have been saying when I tell you to take my YouTube transcript and feed

it to an AI. It is a genuinely new way to share technical knowledge. It is a great blueprint for an AI to execute.

And I think we're going to see more of it because it's much simpler than just having to give an exhaustive step by

step that a human has to follow. It ends up respecting the reader's agency because they can give their own

commentary on the idea and then them and the agent can decide the details together while giving them a proven

pattern to start from. And yes, if you're wondering, you can absolutely take the transcript from this YouTube

video and get started on your own memory project as we've been going through this video together. Just plug it into your

agent and go. But the deepest insight here is that Carpathy is moving the AI from Oracle to maintainer. The role AI

plays is starting to change. Most of us have treated AI as something you ask questions to. Whereas Karpathy correctly

treats it as something that has an ongoing job, maintaining a knowledge artifact that gets better over time. The

AI isn't here for magical pie in the sky one-off answers from the clouds. It's

here for building sustained work that compounds. And the question that we're all facing is just is this the right

interface for that maintenance role. Right? I don't want to lose the fact that underneath that there is a profound

insight here about moving from an answer engine mindset to moving to a mindset

where AI is a maintainer of thinking systems that allow you to think deliberately and do your work better. I

think that's a profound insight because it allows us to be the ones who curate, who think, who select, who explore, and

it allows the AI to support us, right? As we ask the right questions, the AI

can help us by doing so much of the grunt work. And isn't that what we wanted in the first place? Didn't we

want that division of labor in the AI dream world to be the AI doing more of the grunt work and human judgment being

relevant? That's the dream. What Andre Karpathy is describing is one way to get

there, especially if you are in a deep solo research project. And OpenBrain describes another way to do the same

## AI as maintainer, not oracle

thing. It's just focused on more scalable structured data. And yes, you can have the best of both worlds because

we can build a graph over the top of OpenBrain. This is exactly why I built it Extensible because I knew that we

would have more stuff coming out around memory in 2026 and I wanted to build a foundation we could build on. So here we

are. It's our first major test and we can build something over the top that allows us to have the best of this wiki

approach as well as the best of the structure data that open brain gives us. Ultimately, I think the lesson that we

get from Karpathy's wiki is that we need to become thinkers about how we want our

memory and our context layers to work in order to be effective builders of agents

and effective partners with AI over the second half of 2026 and into 2027. None

of what I am describing excuses us from doing that thinking. In fact, it's the opposite. What I've been spending time

telling you in this video is that there is no substitute for making really clear

distinctions and really clear decisions about the way you want your knowledge

structured. Whether that's just you in your room with a laptop and it's your personal knowledge base or whether it's

for your team or whether it's for your org. It is up to you to say I want structured data because I know that I

need to query against structured data and get reliable results above 10,000 artifacts. Or it's up to you to say you

know what I want the best of both world. There's going to be some stuff where I'm going to actually want to query with multiple agents and get structured

results for three different reports at the same time. But over the top of that, I want a graph database that allows me

to think in connections between materials. That would be a little bit more difficult to do if I was just

querying structured data by itself. It's up to you. It is not up to me. We all have to wrestle with this. And if you

are an engineer thinking about this or a product manager thinking about this in an org, you cannot substitute for that

## Making the decision for your context layer

level of thoughtfulness. I'm sorry. You got to do the thinking. And so I hope this video has helped give you the tools

to make that decision clearly.