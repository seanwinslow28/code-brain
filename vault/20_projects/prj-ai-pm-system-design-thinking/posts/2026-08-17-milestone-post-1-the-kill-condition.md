---
title: "The Kill Condition"
type: substack-post-draft
status: draft for Sean's review (milestone post #1 per decision-log D5)
created: 2026-08-17
chain: storytelling-architecture → substack-value-engine → writing-voice-modes (Sean Mode, 70%) → writing-critique (revise, 3 majors fixed) → writing-humanity-pass (voice-safe)
subtitle: "I spent a day trying to kill my next product. Here's the five-rule check you can run on yours before it eats five weeks of your life."
---

# The Kill Condition

The first thing I wrote for my new product wasn't code. It was the sentence designed to kill it. Straight into the public decision log, dated, before I'd read a single competitor's docs. If the research finds this gap already closed, the whole thing reopens. I don't get to pivot, and I don't get to squint at the evidence until it looks friendly. Dead is dead.

Then I pointed five research agents at the five tools most likely to pull the trigger, and I gave the scariest one the meanest brief. Freeplay markets itself straight at product managers, my target user, so its instructions read like a hit job on my own idea. Be extra adversarial. Try hard to prove there is no gap.

Here's what was on the table. Golden Loop is my next build, a tool that turns an AI feature's production failures into a versioned test set and forces honest improvement rounds against a sealed holdout. Five weeks of nights and weekends. And the research that birthed the idea came with its own warning label. The cheapest test of any "missing capability" bet is a teardown proving the capability is actually missing. Building into a solved market is how you donate a month of your life to the graveyard, and I'd caught myself falling in love with the pitch.

The pitch died before lunch.

I'd been telling anyone within earshot that PMs can't run eval labs without engineers. That's false. Braintrust ships a no-code path from production traces to test datasets. Langfuse built most of the same machinery in the last nine months. And Freeplay's docs name product managers as their audience, in writing, using the words "golden set." The lab I was going to build exists, and one company is selling it to my exact user with my exact vocabulary. I sat there watching my differentiation section turn into a brochure for other people's products.

That's the moment you either close the laptop or keep reading. I kept reading, mostly out of spite.

Then the evidence got strange on me. Every tool had the lab. None of them had the rules.

I found the same three absences everywhere. A sealed holdout, the slice of your test set the tuning loop never gets to see, so you can't grade your own homework. One-change-at-a-time rounds, so when the score moves you know what moved it. And a written record of why anything shipped. Not a metrics dump. A reason, attached to a decision, signed by a human.

The strange part is the incumbents know. They testify against themselves in their own material. promptfoo's docs warn that skipping its optional validation split "may overfit," a safety feature that ships turned off, with a note explaining why you'll be sorry. Braintrust's engineering blog hand-builds holdouts because the product can't express one. Statsig ships genuine decision records, wired only to online experiments, a seatbelt installed in the trunk. Every one of them says the discipline matters. Not one of them will make you keep it.

But five tools proving a gap is a hunch wearing a lab coat. "Nobody does this" is the easiest claim in this job because nobody checks it, including the person making it. So I sent another agent through ten more tools by name. LangSmith, Arize, Weights and Biases, Comet, Vellum, the whole second shelf. Three came close enough to earn honorable mention. Arize ships train-test split labels with nothing sealed. Confident AI's docs literally recommend changing one variable at a time, then enforce nothing. Vellum requires approvals for deployments, rationale optional. Fifteen tools. Zero ship the discipline.

Somewhere in the middle of that second sweep it clicked that the verdict was never the prize. The method was. I'd spent the whole day trying to lose, and the trying is the only reason the idea that survived is worth building.

One finding I never went looking for. In the past twelve months, OpenAI acquired two of the five tools I tore down, and Anthropic acqui-hired a third big name, which shut its doors. The labs are eating the eval vendors and pointing them at their own roadmaps. While everybody built labs, the referee's chair got emptier.

So the verdict went in the log. Build. Not the pitch I started with. The one that survived is smaller and sharper. Not another eval lab. The thing that makes the lab honest.

Two honest footnotes, and I need them more than you do. First, this moat is an opinion, not a technology. Langfuse built most of its machinery in nine months, and any of these teams could ship holdout flags and decision logs in a quarter or two. I'm betting on speed and stubbornness. Second, a missing feature isn't a wanted feature. The next test is showing a one-pager to the people who'd actually buy this and watching whether they forward it to a peer or say "neat" and change the subject.

Here's the procedure, because it's the part you can steal today. One day of work. The out-of-pocket cost was $2.80.

1. **Write the kill condition first.** Dated, in writing, before you touch any evidence. Write it after and you'll write one your idea can survive.
2. **Attack a named list.** "I googled around" is not a teardown. Name your five scariest competitors and read their docs, their changelogs, and their pricing pages. Not their landing pages.
3. **Give the scariest one the meanest brief.** If your idea survives a hostile read of its closest competitor, it earned something real.
4. **Sweep a second ring before claiming any negative.** "Nobody does X" is exactly as strong as the list you tried to break it against.
5. **Publish the near-misses.** The three tools that almost close your gap make the most credible sentence in your positioning. Hide them and you're betting nobody checks. They check.

The [full verdict is public](https://github.com/seanwinslow28/code-brain/blob/main/vault/20_projects/prj-ai-pm-system-design-thinking/research/2026-08-17-phase-b-falsification-verdict.md), scoreboard and citations and near-misses and all. Steal the format.

Golden Loop has a decision log now. The first entry is still the sentence that was built to kill it. That's the entry I trust most.

<!-- writing-humanity-pass: voice-safe scrub complete. Protected critique fixes preserved: "research agents" wording, verdict-doc link, de-duplicated spans (product/exact/already/before thinned per analyzer). Additional scrub: clipped no-tail rewritten first person ("I don't get to pivot..."), one colon removed (G1), zero em dashes. Deliberate keeps: "my exact user with my exact vocabulary" (ironic double), bold recipe lead-ins (the Transfer artifact's checklist form). -->
