---
title: "Build the room before you write the memo. Grab the 4-prompt project room kit: source inventory, duplicate log, missing-context list, grounded draft."
source: "https://natesnewsletter.substack.com/p/ai-organize-files-before-writing"
author:
  - "[[Nate]]"
published: 2026-05-21
created: 2026-05-23
description: "Watch now | The first useful agent workflow is not generation. It is getting the work surface into shape."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery]
ai-context: "Nate Jones' 4-prompt 'project room' workflow — inventory sources, log duplicates, flag missing context, then write the grounded draft. Reframes prompt-engineering as preparing the work surface before generation."
---
When AI produces a mediocre draft from a messy folder, the prompt is almost never the problem. The room is.

The model has been handed a strategy doc, two slightly different versions of the operating plan, a transcript with two meetings in it, and a deck that no longer matches reality. It is asked to write a memo. To do that, it has to do two jobs at once: figure out what the project actually is, then produce the artifact. The first job is the hard one. The second job is the one that shows up in the draft.

A sharper prompt won’t fix this. You need to prepare the room first.

I recently worked on a project where the real work did not live in one place. A strategy doc, meeting transcripts, a budget spreadsheet, trip-planning notes, org-design drafts, old PDFs, follow-up emails, half-finished notes. Some clearly current. Others superseded. A few useful only because they showed how the thinking had changed.

The useful first prompt was much more boring than “write the plan.” It was something like: help me build the room. Find the relevant materials. Preserve the originals. Make an inventory. I needed to know which files were authoritative, which were duplicates, which were old, which were missing. I asked it to summarize each source before synthesizing across them, and explicitly told it not to write the final deliverable yet.

Only after that did the writing prompt become simple. Use the current operating plan for the numbers, the transcript for decision context, the older PDF only as background, and flag unsupported claims rather than smoothing them over. The room made those distinctions visible before the writing started.

This kind of workflow was not really available a year ago. Agents could draft, summarize, and answer questions, but they were uneven at walking a folder tree, opening files in sequence, comparing dates across documents, and inspecting metadata without losing the thread. In the last few months that has changed. The current generation of agents is good at the small, boring, file-level operations the work actually requires. Which means the bottleneck has moved. It is no longer “can the model produce the artifact.” It is “is the source set in shape for the model to do anything useful with it.”

**Here’s what’s inside:**

- **What is an AI project room.** What a bounded workspace looks like for one serious job, and which tools to use for which source types.
- **Why AI fails with messy source files.** Why serious work fails when you skip the preparation step and jump straight to generation.
- **How to build an AI source inventory.** How to build the artifact that makes everything downstream inspectable.
- **Summaries, duplicates, and missing context.** The three preparation layers that prevent bad synthesis before it starts.
- **The writing prompt, once the room exists.** What changes when you draft from a clean work surface instead of a raw file dump.
- **Grab the four prompts.** A room-builder for file-system tools, an inventory-and-audit for uploaded docs, a grounded-draft prompt that cites every claim back to a source, and a refresh prompt for when new files arrive.

Let’s build the room.

## LINK: Grab the Prompts

The hidden cost of skipping preparation is that you never see which source the bad claim came from. The memo reads fine. The number is wrong. Three weeks later you find out the agent pulled from a draft someone superseded in February, and now you are unwinding a decision that was already made on bad data. These four prompts exist because that failure mode is invisible until it is expensive. The room-builder and the inventory-and-audit force the agent to declare authority and surface conflicts before it drafts anything, so when something looks off you can trace it to a file instead of guessing. The grounded-draft prompt cites every claim back to a source ID and flags anything the room does not support, which means review happens against evidence rather than polish. The refresh prompt keeps the room honest when new files arrive, instead of letting an old working brief quietly outlive the project. Run them in sequence on the messiest folder you have this week. The artifact you want by the end is not a draft. It is a room you can defend.

## What is an AI project room

A project room is a bounded workspace for one serious job. It is smaller than a second brain, more specific than a knowledge management system, and not the same problem as building yourself a local AI computer. It is the workspace for one project, set up so that an agent can do useful work inside it.

A project room is the place where the agent gathers the material for one piece of work and makes it legible before anyone asks for a final answer.

For a consulting project, that might mean interview transcripts, client decks, data exports, prior proposals, and meeting notes. For a house purchase: inspection reports, disclosures, contractor estimates, mortgage documents, and email threads. A Substack piece would pull source PDFs, transcripts, draft notes, product docs, screenshots, and prior related posts. A board memo needs the financial model, operating plan, old board deck, current KPI export, and the notes from the last three review meetings.

The point is not to create a perfect archive. The point is to create a usable work surface.

A good project room separates originals from working notes and keeps file provenance intact. It creates an inventory, names the source hierarchy, identifies duplicates, and produces short summaries of each source. It flags missing context and tells you what is ready to use and what still needs human judgment.

Only after that should the agent write.

The tool choice matters. Use [Claude Projects](https://support.claude.com/en/articles/9517075-what-are-projects) when you need a bounded workspace with uploaded documents and reusable project instructions. Use [ChatGPT Projects](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt/) or ChatGPT file analysis for smaller source sets and spreadsheets. Use [Cursor](https://cursor.com/help/customization/indexing) or Claude Code when the project room includes code, technical docs, or a folder tree that needs inspection. Use [NotebookLM](https://support.google.com/notebooklm/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en) when the job is research-heavy and source-bounded, especially when you want to work against many uploaded documents rather than a live file system.

The workflow is overkill for a throwaway note. It is not overkill when the cost of being wrong exceeds the cost of preparing the room: a board memo, hiring packet, investor update, diligence brief, regulatory response, legal review, operating plan, or article that depends on source coverage. Use the room when the final artifact will travel farther than your ability to explain it.

Building an agentic back-office pipeline is a different problem entirely. If you are automating invoice processing, customer support triage, or any operational workflow that runs on a schedule, you need a data strategy that lives upstream of any one project. The room is a unit of work, not a unit of infrastructure. Use it for the deliverable you are preparing this week. Build the pipeline somewhere else.

## Why AI fails with messy source files

Most people still treat AI like a file generator.

They ask it to make a memo, build a spreadsheet, create a deck, draft a proposal, or summarize a meeting. Sometimes that works. But in serious work, the hard part is often not generating the first draft. The hard part is getting the inputs into a state where generation is worth doing.

This is especially obvious in Office work. The dream version is “AI makes the spreadsheet” or “AI makes the PowerPoint.” The real pain is different. The spreadsheet has messy exports, merged headers, hidden tabs, stale assumptions, formulas that look plausible but are wrong, and numbers that need to be tied back to a source. The deck has brand rules, executive norms, approved language, old charts, new data, and claims that need evidence. The problem is not whether AI can create a file but whether it can handle the material around the file.

That same pattern applies to almost every knowledge project.

What you actually need isn’t “write.” You need a chain of smaller operations: inspect, gather, normalize, reconcile, summarize, verify, and only then produce. When you skip those steps, the AI may still give you something fluent. It may even look useful. But you have moved the review burden downstream. Now you have to figure out whether the answer is grounded, whether the right sources were used, whether an old file contaminated the conclusion, and whether the agent missed the one document that mattered.

You can change the entire interaction by shifting when the review happens. Review the source inventory upfront, not after the memo is done. Ask for authority ranking upfront rather than discovering halfway through that the agent used an obsolete deck. Request a conflict log and a missing-context list before the synthesis, not after. These moves prevent the polished memo from hiding where it came from.

Agents shine when they’re working on structure, the context, and judgment about what’s in the room. That’s where they add real value.

## How to set up AI file organization

You saw this structure inside Prompt 1. Here’s why it’s shaped this way.

The first job is to gather without destroying.

That means the agent should not delete files, overwrite originals, or silently collapse duplicates without asking. A useful file-system agent starts conservatively. It looks, copies when appropriate, records paths, and proposes actions before taking irreversible steps.

I usually want a structure like this:

- 00\_originals — untouched source files and preserved paths.
- 01\_inbox — unsorted material that may or may not matter.
- 02\_inventory — the table of sources, authority, relevance, and notes.
- 03\_source\_summaries — one short summary per important source.
- 04\_working\_brief — the synthesis layer before drafting.
- 05\_outputs — drafts and finished artifacts.
- 99\_review — duplicate logs, proposed moves, uncertainty lists, and human approval items.

This looks basic. It should. The folder structure gives the agent a safe place to operate. It also gives you a way to supervise without reading every document first.

## How to build an AI source inventory

The most important artifact in this workflow is not the draft. It is the source inventory.

A good source inventory changes the entire interaction. It tells you what the agent thinks the project consists of. That gives you a chance to correct the working set before the final artifact inherits the mistake.

At minimum, the inventory should include file path, source type, date, owner if known, relevance, authority level, current or superseded status, supported claims, limitations, intended use in the final work, and notes for human review.

A final signed agreement outranks a negotiation draft. The current spreadsheet beats a screenshot of last month’s numbers. A transcript may be more faithful to what was said, while a cleaned meeting note may be more useful for decisions and owners. The approved deck represents the story even if the underlying data lives somewhere else, and an old PDF may be useful background but not a source for current claims.

AI can help sort this out, but it should not be allowed to hide the sorting. The inventory makes the judgment visible.

The trust habit is to review the inventory before synthesis. Spot-check the files the agent marks as authoritative. Open one source it calls current and one source it calls superseded. Check whether dates, owners, and titles match what you know. If the agent cannot explain why one file outranks another, do not let it draft from the room yet.

For a writing project, this is especially important. A model can synthesize across twenty sources in a way that feels smooth but erases the difference between confirmed facts, reported claims, working assumptions, and your own interpretation. The inventory gives you a place to say, “Use this file for the timeline, this one for the numbers, this transcript for the quote, and ignore that older draft except as background.”

Much better than trying to debug the final prose.

## Summaries before synthesis

The next step is source summaries.

This sounds like ordinary AI summarization, but the purpose is different. You are not asking for a general summary because you are too busy to read. You are asking the agent to prepare the source for later use.

A useful project-room summary should answer five questions.

What is this source?

What does it contain that matters for the project?

What claims, numbers, or decisions does it support?

What are its limitations?

How should it be used in the final work?

That last question is important. A transcript gives you tone and raw detail but not polished phrasing. A spreadsheet carries the current figures but not the strategic interpretation behind them. A slide deck represents the approved frame without the underlying evidence. A screenshot proves that something was visible at a moment in time, but not that it remains true.

The agent should also pull out uncertainty. A garbled name in a transcript should be flagged, not guessed at. A file that appears to be a draft should be labeled as one. Disagreements between documents should stay visible, not get smoothed over. Missing sources should be called out.

The discipline here is simple: do not let the agent become confident before the room is clean.

## AI duplicate file detection for projects

Most people think duplicate detection is housekeeping. In AI work, duplicates are a reasoning problem.

If the agent sees three versions of a plan and does not know which one is current, it may blend them. The same transcript exported twice with different names gets overweighted. An old deck and a new deck with similar titles become a source for wrong claims. A revised budget spreadsheet next to an earlier copy can produce averaged assumptions without any flag.

Bad synthesis starts here.

The fix is not to let the agent delete duplicates. The fix is to make it report them.

A good duplicate log should separate exact duplicates, likely duplicates, and version families. Exact duplicates appear identical. Likely duplicates share similar names, dates, or content. Version families represent the same artifact over time.

The agent should propose a current version, but it should explain why. Newer modified date is not always enough. The current version might have “final” in the title, or it might be the version attached to a later email, or the one whose contents match the latest meeting notes. Sometimes it is not possible to know without human review.

This is exactly the kind of work AI is good at. It can scan names, contents, metadata, and surrounding context quickly. But the final authority decision often belongs to the human.

That division of labor is healthy. Let the agent find the mess. Do not let it silently resolve the mess when the consequences matter.

## The missing-context list

One of the best signs that an AI agent is helping properly is that it tells you what it does not have.

A weak workflow produces an answer from whatever happens to be in front of it. A strong workflow produces a missing-context list before the answer.

For a serious project, the agent walks through the room and notices three kinds of problems. First, what is missing: the decision no one documented, the number with no source, the absent owner. Second, what is ambiguous: which version is current, which draft is outdated, where documents disagree. Third, what is dangerous: unsupported claims, private sources that should not be used, inferences presented as facts.

That matters because the missing material is often more important than the available material. Your document may say “as discussed” while the source of truth sits in the discussion itself. A transcript may say “we agreed to this,” but the actual decision may have changed later in Slack. The spreadsheet includes a number without the assumptions. The deck includes a chart without the data source.

If you ask for the final memo too early, these gaps become hallucination traps. If you ask for the missing-context list first, they become review items.

## The writing prompt, once the room exists

Once the project room exists, the writing prompt gets shorter and better.

Instead of saying:

“Write a strategy memo from these files.”

You say:

“Use the reviewed source inventory and working brief. Treat the current operating plan as authoritative for numbers, the transcript as source material for decision context, and the older deck as background only. Draft the memo, cite claims back to source IDs, and flag anything not supported by the room.”

The model is no longer guessing what the source set means. You have already reviewed the room. You have already decided which materials matter. The agent has already summarized the evidence, identified conflicts, and listed gaps. Now the writing work can be grounded.

This is also better for review. When the draft says something questionable, you can trace it back to the inventory or the source summary. Inferences should be labeled. Unsupported claims should be flagged. When the source hierarchy changes, you can update the project room and regenerate from a cleaner base.

Fast-moving projects need maintenance. If new files arrive daily, refresh the inventory before each serious drafting pass. If the source hierarchy changes, update the working brief. A project that changes purpose needs a new room rather than a contaminated old one. The goal is not a permanent archive but a clean enough work surface for the next decision.

You are not trying to make AI perfect. You are trying to make its work inspectable.

## Pick one project this week

Block 45 minutes Tuesday afternoon. Pick the project where you have the messiest folder and the most consequential deliverable. Drop the relevant materials into Claude Projects, ChatGPT Projects, Cursor, or NotebookLM depending on the source set. Use the prompts in the kit above. Do not let the agent synthesize until you have reviewed the inventory.

That single session will teach you more about how your own work is organized than another hour of prompt tweaking. The artifact you want by the end is not a draft. It is a source inventory, duplicate log, missing-context list, and working brief.

The learning ramp most people need is not “how do I make the AI sound smarter?” but “how do I make the work surface clean enough that AI can help?”

## The shift from generation to preparation

The old AI question was whether the model could produce the artifact.

Can it write the memo? Make the spreadsheet? Create the deck? Summarize the transcript?

Those questions still matter, but they are no longer the most interesting ones. The more useful question is whether the agent can help prepare the conditions under which good work happens.

Can it find the right sources, tell which ones are current, preserve originals, and identify missing context instead of inventing around it?

I think many people will first feel agents become useful right there. Not as magical writers or autonomous employees. Not as another demo where a model produces a passable first draft from a clean prompt.

As the assistant that walks into the messy room before the meeting starts, turns on the lights, labels the boxes, finds the missing folder, puts the current documents on the table, and tells you what still does not add up.

Then you can write.

Not before.

![](https://substackcdn.com/image/fetch/$s_!st7e!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F506cf1f6-7e53-49e6-b214-f724246bcd00_1254x1254.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/ai-organize-files-before-writing) on 2026-05-23T14:56:11-04:00*

YOUTUBE TRANSCRIPT
A few weeks ago, Sullivan and Cromwell, one of the most prestigious law firms on the planet, had to write an apology letter about AI to a federal bankruptcy judge. Their emergency motion in a Chapter 15 case had been filed with dozens of fabricated or misquoted citations. AI hallucinations. The other side's lawyers caught them.

Sullivan and Cromwell's own review did not. The partner who signed the apology letter is the co-head of the firm's restructuring practice. This is the failure mode I want you to think about with me for the next few minutes. I'm not talking about 2024 hallucinations where a solo practitioner uses ChatGPT and tries

and tries to tell it not to hallucinate. I'm talking about organizational and structural hallucinations at the top of agentic workflows. In this case, the motion looked legitimate, the structure of the motion was correct, the citations were professionally formatted, dozens of them were pointing at the wrong things. and nobody on the team caught it before the filing.

The model is not the problem here. The working environment around the model is the problem and it's the source for most of our 2026 hallucinations. I know what some of you are thinking. Nate, the answer is a better prompt. We talked about this. Just tell the model not to hallucinate. And by the way,

the Marc Andreessen screenshot has been all over the timeline for a few days now. It doesn't work. You cannot tell a language model not to hallucinate any more than you can tell autocomplete not to autocomplete. There is no separate truth check pass inside the model that the instruction can hook into and have some purchase and meaning.

Sullivan and Cromwell had access to the best AI tooling that money can buy. The wrong details still made it into court. The fix is not a sharper prompt. It just isn't. In the last month, with 4.7 Opus and 5.5 from OpenAI, agents have picked up a capability that changes the way we think about this,

and I don't think law firms or most other people have realized it yet. There is a fix, it is not a prompt fix, and that's what I want to talk about today. So what is it about 4.7 and 5.5 that's special?

They do long-running agentic tasks, as I've said a lot, but they do it on your file system. And that's such an unsexy thing to talk about. Oh, files. That's all the way back to 1982, right? Like, that's a long time ago we handled files. Longer ago than that. Why do we care about files now?

Why do we care that agents that are long running are now very good at taking and manipulating files, and how does all of that connect to the hallucination story? I will tell you. These new agents do not just read what you paste. They can walk a folder tree. They can open files. They can compare dates across documents.

They can inspect metadata. The workflow around hallucinations has flipped, but most people haven't caught that yet. Because the first useful prompt in a serious project is now, like, it's not write the document, right? It's much more boring than that. It is build me the folder in the file room. Build me the room to do the work in.

And I want to talk to you about three key takeaways in this video, and if you follow them, you are not going to end up in the same hallucination place because you will have set up a process that is structurally antagonistic to hallucinations.

I am saying that you are building a structure that makes them much less likely to occur at scale, and it keeps you and the work you do much more accurate and much less likely to lead to the kind of corporate liability that this prestigious law firm

generated for itself because it did not think through its agentic pipeline correctly. It all comes back to file. So here we go. Three things. One, why your first AI prompt is never do the thing. And I talked about that just above. We're going to get into why Dr. Justin Marchegiani B. Jones

The thing that sold me on this workflow was a real moment that I had, multiple real moments over the last couple of weeks with Codex. I have been in situations where the AI agent has now been able to do incredibly powerful simultaneous drafting of up to eight different documents.

I haven't gone past eight yet, I think I could. And the only way I could get eight documents drafting at once in Codex is because I prepared the data room first and I knew my outputs and I could then execute really cleanly and consistently. And it saved me so much time. It was an incredible speed up.

It felt like the hair was blowing back on my face and I was living in the future. And I think that that's one of the things that we need to pay attention to is that we get these aha moments when we think about the boring primitives, when we think about the files,

and that's why we're going to talk about them. Look, because of ChatGPT back in 2022, most people think the AI workflow starts with doing a job. Does the model write for me? Does the model code for me? Does the model make the Excel file? That's where the value is, right?

It starts when the agent walks in and does something. But I don't think that's true. I think a serious project almost never has its source material and we have had to be the human organizers for most of the prompting era in the last couple of years.

We've had to find the strategy docs and the meeting transcripts and the spreadsheets and the half-finished notes and the follow-up emails and the old deck and the PDF you forgot about and the Slack thread where the the actual decision was made. Can you tell I've actually had to do this? Some of it is current.

Some of it is stale. Some of it contradicts itself. A few files may be helpful. You're not sure which one is the source of truth. You're often wrong. When you ask an AI to write from that general mass, you're asking it to do

That is a recipe for a really mediocre result and it's one of the situations in which it's likely that you will have a hallucination problem in the way that this law firm did. The model didn't have a clean working environment so the dirt got into the dock. It didn't know which sources mattered.

It didn't know what was stale. It didn't know what was missing. It didn't know which file was authoritative. You cannot patch that with a better opening sentence and you really can't patch it by reading the doc and hand editing anymore because we're working at a different kind of scale.

You have to patch it and prevent it from the beginning by cleaning up your data room first. So your first instruction should not be do the thing, like write the memo, make the excel, etc. Instead, your first instruction needs to be find the relevant materials on the internet, on my local computer, in my files,

in the tools that I have And so the first instruction is find the relevant materials, preserve the originals, build me a data inventory, put it in a folder, tell me which files seem authoritative, which are duplicates, which are old, which are missing, summarize every source before you synthesize anything and do not write the deliverable yet.

We're just learning. That is so powerful. and it's possible because these tools can do complex long-running file manipulation tasks successfully and with very high accuracy. So let's use them to do that. Let me give the workflow a name so we can talk about it very, very clearly. I'm calling it a project room or a data room.

A project room is a bounded workspace for one serious job. It's a project, a deliverable, a source set. Now, this is much smaller than a whole second brain. It's much more specific than a knowledge management system. It is a workspace set up so an agent can do useful work inside it.

And in most cases, it is a local workspace. This is different than a lot of the published cloud solutions that Claude and ChatGPT and Codex have had where they say, here, start up a project in sort of a shared context window that people can all chat into and all work with.

I have found those have been much less useful than the flexibility of a local file system. And there is a whole 2026 conversation to be had around the idea that we are going back to files and going back to simple primitives, and those tend to work really,

really well because LLMs are being taught to use computers at their most primitive and root level in order to successfully do anything on computers, and when we go back to files, we are going back to what they know really, really well. Why not, right? Why not lean into it? So let me give you an example.

For a consulting project, this could look like client decks, interview transcripts, data exports, prior proposals, meeting notes. For a house purchase, it's inspection reports, disclosures, contractor estimates, mortgage documents, email threads. For a substack, article you're writing, it could be sources you're researching, transcripts, draft notes, screenshots, prior related posts. For a board doc, it's a financial model,

an operating plan, an old board deck, the current KPI exports, and the notes from the last three review meetings. The point here is that you don't have to build a perfect archive to gain a tremendous amount of advantage in the task you're setting the model.

The point is just to give the agent a usable work surface, just enough room for it to operate. Where you build your room, of course, will depend on your preference, on your source set. Look, you can do this in Claude projects. It's solid when you need a bounded workspace with uploaded docs.

Chet GPT projects handle smaller source sets and spreadsheets. Cursor or Claude code is the right tool when the room includes a code or folder tree. Codex works for that too. Notebook LM works when it's very sort of research heavy and source bounded. And like I said, my personal preference, just go to local files,

have it create a folder, and you can stick literally anything in there. And that's what I love about it because there's no So if you want to dive deeper on different options to organize your files from all those different tools and how you want to think about making that choice, I'd put that on Substack.

You can dig into strategies for local file organization because imagine doing 20 projects. You're going to need to have some thinking around that. You're going to want to dig into strategies if you want to use other tools too, like projects on Claude or on Notebook.lm, looking at the sort of folder structure, how you think about project breakdown.

I've got all of that in detail there. We're going to stick in this video with how we think about this as an archetype, how we think about this as a larger pattern that works across many tools. So let's keep moving. You have your folder. You have stuff in it.

The most important artifact in this whole folder I haven't talked about yet. It's a table. It's just a table. Hear me out. It's called the source inventory. And once the room exists, it's the first thing you ask the agent to present. Yeah, that does sound boring.

The Inventory tells you what the agent thinks the project consists of, which is And that gives you a chance to correct the working set of docs and current set of data before the final draft is going to inherit a bunch of mistakes and lead to hallucinations, frankly. And so yes, I do recommend checking what is

in your inventory and making sure you're aligned with it and nothing is missing. And when in doubt, just say, hey, you know, Codex, I think this transcript may not be in here. Can you check? And if need be, create a file for it. And we'll do that.

And the beautiful thing is these agents are strong enough to sort this out, right? They can tell that an approved deck represents the story, even when the underlying data lives elsewhere, that the old PDF might be useful background, but not a source for current claims.

And the agents really can sort that out at the Opus 4.7, at the ChatGPT 5.5 level. And the inventory artifact that you create, that table I'm talking about, what you're really doing is you're making the agent's judgment visible and legible so you can see it really, really clearly.

Because if you review the inventory and you can't tell why one file outranks another, you can just focus on getting the inventory right, focus on making sure all the data is there before you have to go farther. It's a really clean game. Now, I have been testing different knowledge systems for AI,

and the organization framework that I landed on for large projects is something I'm writing up in a lot of detail on Substack. So if you're serious about AI work, if you're trying to figure out how you organize these files at a 10, 20, 30 project scale so you're clean and you understand what you're working with,

that's what you want to get to. I have it all written up over there. Let's get into a couple of more artifacts to illustrate the principles, because remember, that's what we're doing. So we talked about the table. Let's talk about two more artifacts. The first is the conflict log.

When the agent reads a serious source set, it will find disagreements. The old PDF says one thing, the current plan says another. The transcript uses a different name for a person who's a key stakeholder versus a doc. The spreadsheet has a number with no visible assumptions behind it. Two documents that look adjacent are actually three months apart.

A weak workflow lets the agent synthesize and smooth those conflicts over. The output will read confidently, but you don't know what you can trust. You get into the same hallucination problem that the law firm did at the beginning of this video. This is that disagreement without necessarily resolving it,

or at least without resolving it without you being able to tell. The conflict log allows your agent to surface conflicts that I've just described and recommended responses and allows you to have opinions and edit, adjust, tell the agent it's wrong, etc., before you get into building the doc.

The second artifact I want to talk about on top of the conflict log is the missing context list. One of the best signs that an agent is helping properly is that it tells you what it doesn't have to do the job well. The missing decision, the number with no source,

the current version of a file that's nowhere to be found, the completely absent data file that is referred to in only one document. All that matters because the missing material is often more important than the material you have. Your file can say as discussed and the actual discussion can be somewhere else.

The deck can include a chart and the data source ends up being way far away and maybe not in your data room at all. Ask for the final memo or the final output or whatever you're writing too quickly and all of those gaps become effectively hallucination traps.

The model invents its way around them to get your job done and the prose looks fine and you may ship something with a very soft spot underneath and someone will find it. So ask for the missing context list first and those gaps become transparent and legible and you can review them. You can see them.

You can decide whether they matter, whether you can find the source, whether you have to phrase the claim more carefully. So the full seven-folder structure that I use inside projects, every folder name, the purposes and all of that, I link that in the Substack. It's all laid out. You can see it really cleanly there.

We're going to go on from here to talk about duplicates. And I don't want to be I'm going to be really honest about this because a lot of people miss this. People think duplicate detection in files is housekeeping, but in AI work, duplicates can be a reasoning problem.

If the agent sees three versions of a plan and doesn't know which one is current, The same transcript exported twice can get overweighted in the synthesis if you're not careful. An old deck and a new deck with similar titles can become a source for wrong claims. A revised budget sitting next to an earlier copy produces averaged assumptions.

You do not want your with your agent deleting duplicates, but you do want it to produce a duplicates report and probably a separate folder with suspected duplicates and hand that back to you. Let the agent find the mess, let the agent name the duplicates, name the likely duplicate the level of confidence, name the version families.

Do not let it silently resolve the mess, especially when you care about the work. The agent finds, you decide, that is a really healthy way to have good, clean, agentic pipeline work for very complicated, high-value, critical knowledge work. So why does all of this matter?

One more thing before I get to how we write the prompt to get actually going into stuff. There's a reason this matters now. The agents have just gotten so much better at the details of the file manipulation I'm talking about. They really do walk folder trees cleanly, they open files well, they inspect metadata,

they're good at actually doing the nitty-gritty work of file comparison at high fidelity across hundreds of documents for a long period of time. And so file organization used to be something we had to do to housekeep for ourselves. Increasingly,

I think of it as a canvas that we have to work with the agent to create so that the final work reflects the underlying data. In that sense, the data underneath is the substrate for the canvas. It's that white gesso that's on the surface of the canvas.

And then you paint across it the work you want to create with your agent. But if you don't get the canvas right, you're never going to get the final work to look right. And that's what we're doing with the data room. You're framing the work. Literally, you're framing the work. And because we are now doing harder work,

because the agents are more capable, our traditional ways of compensating don't work. You used to be able to compensate for a messy folder with a sharp prompt. It's too big now. You can't now. The mess is becoming structural and entangled, and it's becoming something that you can't clean up with a single prompt.

The mess is sitting inside the agent's context window and it's something that the agent will disentangle in the best way it knows how and the risk is actually higher because the agent will find, no matter what, come hell or high water, a way to disentangle it because that's its job and it's trained to go after that

task aggressively. You may just not have ever seen that way of disentangling it. You may not be aligned and that's exactly where you get the kinds of hallucinations that we saw in the law firm at the top of this video. That's the structural reason those sorts of things start to surface in Final Materials.

Now the good news is, we're finally at the prompt part, I know you guys are waiting for it. Once the room is in shape, once you have inventory, conflict log, missing context list, duplicate The writing prompt actually gets really short. It's not long, and the output gets much better. Before the Room, the prompt was like,

write me a strategy memo, here are a bunch of files, and then if you're doing prompt engineering, it's a very detailed, like, here's what I want you to write. After the Room, after you have your data together, the prompt is very simple. Use the reviewed source inventory in the project room in the working brief.

Treat the current operating plan as authoritative. For numbers, the transcript is source material for decision context, and the older deck is background only. Draft the memo, cite claims, flag anything not supported. The key here is that all I'm doing in that prompt is I am saying, this is what matters to me.

This is what I care about from a conflict perspective. This is what I think the authoritative true line is for this piece of work that we're working on together. And then you go do the rest. And this makes the AI's work inspectable. It's not that I'm saying if you do this, the AI's work will be perfect,

but it is the difference between using AI as a colleague and using AI as a gopher. And we are really underusing these agents if we treat We don't give them any ability to think about their structure and their context with us. They are more senior than that now.

Our AI agents deserve to be able to shape their context windows and their data rooms together with us if we want to get the most out of them. And they are capable of doing so. Now, a word on calibration before I close. I am talking specifically about agents for serious knowledge work, right?

If you are working with codecs for a 30, 40, 50 hour, two hour run, this makes sense. It makes sense for coding, it makes sense for heavy knowledge work like I've been discussing with projects and reports. Do not run this workflow on every casual interaction with AI. It's way overkill. Also, obviously,

I am not talking about using this approach to produce agentic pipelines that take care of of back-office operations. You still need a data strategy. You need to think about how you input data. That's important, and I cover it in other videos, but it's not this problem. And yes, I have more prompts on the Substack.

I know that not everyone has the exact prompt situation that I gave you. If you want more sample prompts that kind of cover a wider variety of use cases for this kind of knowledge work, it's on the Substack. You can grab them and apply it to your messiest folder this week. It'll help.

In closing, here's the mental model shift that I want you to walk away with. I'm really passionate about this. I think this is one of the most slept on implications of AI in the last 40 days, and we're not talking about it enough because it's filed and it's boring.

The old AI question was whether the model could do the thing. Nate‒sletter Can it shape the canvas? Can it find the right sources? Can it tell which ones are current? Can it identify what's missing before it vents around the missing thing? That's where agents start to feel really useful as colleagues for real work because

an agent can walk into a messy room, it can turn on the lights, it can label what's in all of the folders and it can get the entire desk area organized for serious work. That is an AI worth using. Please use your AI that way. And I'm talking specifically about ChatGPT 5.5 and Opus 4.7.

I would not do this with earlier models. I hope this has been helpful. There will be more practical tips coming on this channel shortly, so subscribe for more. Cheers.