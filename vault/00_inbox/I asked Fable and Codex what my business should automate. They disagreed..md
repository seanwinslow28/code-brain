---
title: "I asked Fable and Codex what my business should automate. They disagreed."
source: "https://natesnewsletter.substack.com/p/let-ai-pick-what-to-automate?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-07-16
created: 2026-07-20
description: "Watch now | The model I liked using less found the problem that mattered more. That result changed what I ask AI to do before I give it an assignment."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
Fable won this test, and I am still divided about what that means.

Codex was a delight to work with. I gave it a sprawling assignment, turned the effort all the way up, and watched it move through my files, Slack, and content operation without making me babysit every permission request. It understood the boundary, used the tools it needed, built an automation, and finished the run. One run. No drama. This is a large part of why I spend so much of my working day in Codex now.

Fable was a hassle. I fought through permission dialogues, interruptions, and the ordinary friction of trying to keep a serious agent run moving. More than once, I wanted to call Codex the winner on the operating experience alone.

Then I looked at what each one had chosen to build.

Codex found a real problem in my content operation. Research and evidence need a cleaner handoff before I start scripting, and Codex built a tool that would make that handoff more dependable. I will probably use it. But the tool enters after I have made the decision that consumes much more of my attention: which story is worth telling at all.

Fable went there. It looked past the handoff and found the mess before the pipeline—the duplicate ideas, weak coverage, and instinctive decisions that determine whether a story ever makes it into production. Picking the right story in a world of infinite AI stories is one of the hardest jobs in my business. I know that because people ask how I do it, and my honest answer has always been some unsatisfying mixture of evidence, audience feel, sweat, and instinct.

Fable decided that was the problem worth attacking.

Codex built something useful. Fable found something I immediately felt I had to have. So the tool I enjoyed using more had completed the less consequential job, while the tool that annoyed me had seen farther into the business.

I could turn that into a simple Fable victory story. It would not match how I actually work. In practice, I still reach for Codex much more often, and on most days I would rather work inside its harness. One experiment also cannot tell me whether I am seeing a durable model difference, a harness difference, a lucky run, or some combination of all three.

I could not dismiss the result either. It kept pulling me back to a question I had not taken seriously enough. We have become much better at telling models what to do. What happens when we ask them what deserves doing?

**Here’s what’s inside:**

- **The experiment.** I gave Fable and Codex the same open brief — search my real business, find the problem worth automating, build it — and deliberately left out the one thing I normally decide myself.
- **Why they disagreed.** Codex picked the clean, finishable problem; Fable went after the messy, higher-leverage one — and the split exposes how each model handles ambiguity *before* the task is defined.
- **Routing starts earlier now.** When a model can help decide *what* to build, model choice moves upstream of the deliverable — plus when to reach for the strategic model vs. the dependable harness.
- **Why I killed the “magic button.”** The first version let the AI pick the problem *and* build it; the rebuilt skill deliberately stops short, so a bounded agent can’t make its own read feel inevitable.
- **The skill, yours to run.** A reusable automation-discovery skill that inspects your own work behind walls you set, returns up to five evidenced offers instead of one grand answer, and only builds after you choose.

I’m still divided about what it means. Here’s the full teardown — and the skill, so you can run the same experiment on your own business.

## \[LINK: Join the Slack →\]

[The Slack community is live](https://join.slack.com/t/natescommunity/shared_invite/zt-43jji0fbo-mD~LFBAQqxCRFrxOVrPJiA)! It’s where I’ll be sharing things between articles, where you can get help on builds in real time, and where the fastest conversations in this community are already happening. I’ll see you in there!

## \[LINK: 3 Months Free to Zero to AI\]

Yesterday, [I posted a note](https://substack.com/@natesnewsletter/note/c-295971660?r=1z4sm5&utm_source=notes-share-action&utm_medium=web) about how I’ve been walking through the primitives behind [Open Brain](https://natesnewsletter.substack.com/p/every-ai-you-use-forgets-you-heres) on my other Substack, [Zero to AI](https://nateszerotoai.substack.com/). Real talk: in AI time, March was a very long time ago. If you sat that one out because it felt too big, or too scary, or you just weren’t ready, that’s fine. Now’s the time.

As a paid subscriber, you get 3 months free to Zero to AI. And if you just want to revisit the basics, Zero to AI has you covered.

Click the link. 3 months free. If it’s not for you, cancel any time.

## \[LINK: Grab the guide and try the skill\]

If you have a capable agent and keep staring at an empty prompt, this is the way out. The automation-discovery skill audits your own work behind the walls you set, hands you a short menu of evidenced automations, and builds only the one you pick. You never have to name the problem first.

Head to the guide, download `automation-discovery.zip`, unzip it into your agent’s skills folder as `automation-discovery`, then refresh the skill index and start with:

```markup
Use automation-discovery. Start with my AI session history; my write root is ~/automation-discovery-run.
```

For the first run, use one recent, representative work surface. AI session history is the easiest place to start because it catches work at the moment somebody asks for help. Later you can add approved material from Slack or Teams, Linear or Jira, documents, repositories, or whichever systems hold the work.

Approve the source plan carefully, exclude anything the agent should not inspect, and keep external writes off. When the offer sheet arrives, choose the problem whose disappearance would change the work—not merely the one with the most events. Choosing none is allowed.

## I left the most important part out of the prompt

The assignment was deliberately incomplete.

I told Fable and Codex to inspect the places where my work actually happens: local files, business Slack, the content systems, the accumulated evidence of projects moving and stalling. They could choose a recurring problem, explain why it mattered, and build an automation that addressed it. What I did not give them was the workflow.

That omission was the experiment. A normal agent brief begins after I have noticed the pain. I name the job, provide the source of truth, set the permissions, describe the output, and tell the agent what would count as done. The model may do an extraordinary amount of work, but the human still performs the first act: deciding that *this* is the thing worth doing. I wanted to know whether current models could help with that first act too.

This extends an argument I made in my piece about the [Prompt Lifecycle](https://natesnewsletter.substack.com/p/the-complete-prompt-tooling-ecosystem). My point then was that many prompts fail before anyone starts polishing the wording. The user has not formed the intent clearly enough. They ask for a presentation before deciding what decision the presentation needs to change, or request a dashboard before agreeing on the metric. Better syntax cannot rescue an unresolved purpose.

I still believe that. What changed in this experiment is where I think intent has to come from.

I had treated intent formation as a human stage. First I figure out what I mean; then I brief the model. But sometimes I do not have a clean statement of the problem because I have been living inside it for too long. I have normalized the retries, the rebuilt files, the questions that recur in Slack, and the prompts I keep writing to recover context I thought I had already supplied. If you ask me about my priorities, I can give you a perfectly respectable answer. The work itself is less polite. It shows what I keep reconstructing, chasing, and explaining.

That behavioral record gives the model something much richer than a vague request for ideas. A repeated prompt can mark a moment when I reached the edge of my own attention, and a correction can show where an earlier instruction failed to capture the work. Sometimes it reveals nothing more than a model that keeps failing in the same annoying way. The audit has to distinguish friction in the AI tool from friction in the business. But a ticket that changes owners three times, a document that is never trusted without a manual comparison, or a handoff that requires the same explanation every week is already telling a story about the process. Nobody has to remember to add it to an automation backlog. The evidence is sitting in the work.

This does not make the evidence objective. Quiet strategic work may leave almost no trace, while a cheap annoyance generates twenty prompts. A model can confuse what is legible with what is important, and one chaotic week can look like a permanent operating pattern. There is also a basic privacy question here: a fresh set of eyes is useful only if those eyes are allowed to see the material in the first place.

Still, the possibility is new enough to matter. The model is no longer waiting at the end of intent formation for a polished assignment. It can participate in the investigation that produces the assignment. The sentence I typed was an instruction, but the work I was asking for was inquiry: inspect the evidence of my behavior, form a theory about where the work is needlessly depending on me, and show me what I have stopped noticing.

## What the disagreement exposed

Codex’s handoff tool brought that home for me. Nothing was obviously wrong with it. The automation addressed a visible pain and the run had the exact quality I want from an operating agent: bounded, responsible, and finished. If I had only run Codex, I might have accepted the tool, saved some time, and concluded that the discovery exercise worked.

Fable’s answer made the omission hard to ignore. I would have automated the part after story selection while continuing to carry the story-selection problem myself.

That matters more now than it would have a year ago because I can ask Fable or Codex to take a small internal tool from problem to working artifact in one serious run. They do not always succeed, and “working” still needs to be inspected, but in this experiment the implementation was cheap enough that the choice of problem bothered me more than the build. When building was expensive, a mediocre idea often died before it could win the budget or developer time. An agent can make the same idea look finished before we have spent much time asking whether it deserved to exist.

The failure mode is strange: the model can follow the prompt beautifully, create the interface, wire the workflow, write the documentation, and hand back an impressive artifact. Then I inherit the review and maintenance burden for a problem that should never have made it past the question stage.

So I no longer think model comparison begins after the job is defined. We usually route models by deliverable: use this one for code, that one for prose, another for research. But if a model can help decide what the deliverable should be, routing starts earlier. The question becomes “Which model’s way of interpreting ambiguity is useful before I know what the thing is?” A benchmark score cannot answer that on its own.

I think Codex picked the smaller problem for the same reason I enjoy using it.

Codex made the problem finishable. It found a pain point that was voiced in the evidence, put a boundary around it, and carried the job to completion. That instinct is exactly why I trust it with so much daily work. Once I know what I need, I want the agent to stop admiring the ambiguity and finish. I want it to respect the write root, make the file, run the check, and give me something I can inspect.

In an open discovery problem, the same instinct can pull the model toward what is easiest to bound. The content handoff had identifiable inputs, an output, and an obvious place in the pipeline. Story selection was messier. The evidence was distributed across ideas, performance, audience reaction, editorial judgment, and work that never became a formal task. Solving it required the model to infer an upstream intent that I had not stated cleanly.

Fable was willing to make that inference. This is the quality I clumsily call “big model smell”: the sense that a model can read between the lines, follow a consequence upstream, and stay with a problem whose edges are not yet tidy. It saw that improving a late-stage handoff would not help if I was feeding the pipeline the wrong story.

That expansiveness has a cost. A model that ranges beyond the literal assignment can find a more consequential problem, or it can invent importance. A strategically interesting answer is not automatically a correct one. That cuts both ways. And I should separate the model from the product around it: some of my frustration came from the Claude permission experience, not from Fable’s reasoning. A wonderful model in a difficult harness and a dependable model in a delightful harness are different comparisons from “smart versus less smart.” In actual work, I experience all of it at once.

So I am not ready to turn one run into a permanent slogan that says Fable thinks and Codex does. The next model release could change the balance. A different source set could reverse the result. On a regulated, urgent, or precisely measurable job, the bounded answer may be the more valuable answer.

I do have a working hypothesis now. When the question is unstable, the way story selection was, I want a model that will range across the evidence and offer interpretations I did not arrive with. The moment the consequence is real, one reading is not enough. Once I choose the problem and can define success, I want the strongest operating harness I have to build it and return proof. In my current setup, this run makes me want to test Fable earlier and Codex later. That is an experiment I can now repeat, not a permanent routing table.

I recently wrote that [Claude and Codex are teaching two different ways to manage machine work](https://natesnewsletter.substack.com/p/claude-code-vs-codex-agents): stay close and steer, or write the assignment and dispatch. This experiment adds a stage before either of those. Sometimes I should not be steering a known task or dispatching a clean assignment yet. I should be asking a model the question Fable answered and Codex missed: am I looking at the right task?

If two capable models inspect the same business and identify different problems, it is tempting to treat that as a reliability failure. We want the answer. We paid for intelligence; surely it should converge on the single highest-value automation. But the evidence can constrain the answer without choosing the consequence we care about. Codex saw repeated friction in a handoff. Fable cared more about the decision that precedes the handoff. Both findings were real. Ranking them required a judgment about which change would alter the business more.

The model also brings its own habits into the recommendation. A system built to finish bounded work may notice bounded work first. A model that tends toward expansive interpretation may prefer a grand upstream theory. Running the second model exposed the frame inside the first answer, and it made me ask a question I will keep: did this agent find my most important problem, or the problem that looks most natural from inside its own capabilities?

I suspect we will use several models this way more often, to make their different readings visible while the problem is still cheap to change. An average would not help me. I want to see what each one noticed, what it ignored, and what I would be committing the business to if I accepted its frame.

That sounds slower than asking one model to decide. At the beginning, it is. I have to compare that cost with the time I would spend reviewing, adopting, and maintaining a finished solution to the wrong problem.

## My original “magic button” was too magical

The first version of this idea was wonderfully simple: let the AI inspect your work, pick the problem, and build the automation. I called it an automagic button for automation because that was honestly how it felt. People buy an agent, connect a few tools, and then stare at the empty prompt wondering what to give it. Here was a way out. The agent could look at their actual behavior and choose.

In the first recording, I say this with complete confidence: “You don’t have to pick. You can let the AI pick for you.” I understand why I said it. The empty prompt is real, and watching an agent notice a problem you have normalized feels like magic. But after looking at the two results side by side, I would not ship that sentence as the operating contract. The capability was real. The delegation went one step too far.

“Pick the problem” makes a judgment call disappear inside the run. A bounded agent may automate something safe and small; an expansive one may automate an attractive theory that outruns the evidence. In both cases the agent can make its own interpretation feel inevitable because the user sees only the winner.

I did not want to lose the relief of the original idea. I do not want every automation project to begin with me carrying the entire diagnostic burden, perfectly naming a problem I may be too close to see. But I also do not want one model’s reading of my business to become the future because it can build quickly.

So the rebuilt skill changes the contract.

It does not inspect the work, crown one idea, and start coding. It creates a durable, source-linked record of the recurring events it found, audits whether the claimed patterns are actually present, and returns a short set of automation offers. Each offer has to carry an evidence query, an honest account of the operating burden, and a declaration of how a finished build would prove itself. Where the evidence does not support a consequence, the skill tells the worker to say `unknown` rather than fill the gap with a persuasive story.

Then it stops.

The person running the skill can choose one, ask for a different framing, or choose none. “None” matters because a discovery system that must always recommend an automation will eventually manufacture demand. Three independent events can qualify a recurring job for consideration; they cannot establish that removing it would matter. Frequency is evidence, not value.

Only after the choice does the job change shape. The selected problem becomes a bounded build, with tighter permissions, acceptance criteria, write boundaries, and proof because the inquiry phase is over. The question opened the problem space; the build contract constrains what happens next.

Near the end of the recording, I say that 2025 was about giving AI instructions and 2026 is about asking the right questions. I believe the direction of that line, but written down it is too clean. Questions do not replace instructions; they belong at different moments.

When the problem is unknown, an over-specified prompt can trap the model inside my existing interpretation. A bounded inquiry sounds more like this: here are the sources you may inspect, here are the walls, show me the patterns, surface rival explanations, and do not act. Once the problem is chosen, vagueness becomes dangerous, and that is when I want the exact source of truth, allowed actions, expected artifact, stop conditions, and receipt. I have not abandoned specification. I just need it later.

## A skill as a reusable way of asking

A skill can preserve more than a method for producing an artifact. This one preserves how a question gets investigated.

That does not mean hiding an enormous prompt behind a short command. The question runs both directions. I ask the model what problem it sees; the system asks which part of my work matters, which evidence is legitimate, what it must not touch, whether I recognize the pattern, and what proof would make the eventual build worth trusting. It is an inquiry with rules — sources it may read, walls it may not cross, a pattern I have to confirm.

The package uses a source-linked SQLite corpus because long agent runs forget, summaries drift, and “the model remembers seeing this pattern” is not enough to justify a build. The record survives the conversation and gives an auditor source references it can sample and challenge. It still inherits the events the first workers chose and the way they normalized those events. A database reduces summary drift, but it does not remove perspective. That connects to [Open Brain](https://natesnewsletter.substack.com/p/every-ai-you-use-forgets-you-heres), but the purpose is different. Persistence here does more than help the AI remember me. It preserves the evidence and intermediate claims behind its judgment so I can inspect them later.

One grand recommendation would hide the model’s narrowing again, so the rebuilt skill returns up to five evidenced offers—with fewer or none when the evidence is thin—and lets the user choose. Before the selected build starts, it also declares what receipt would distinguish a working automation from a convincing demo. Those pieces exist because the experiment made them necessary, not because every prompt needs a database and a governance layer.

I have not yet proved the rebuilt package through a fresh, repeated real-work cycle. The scripts passed a structural smoke test, but a truly incremental and crash-safe loop still has to earn its receipt. A wall written into a prompt is also an instruction, not an access control. I excluded a personal Slack from my run; for sensitive material, I would export only the approved sources or enforce the boundary before an agent can see them.

That is much closer to the way I want to use a powerful model now. When I feel the recurring friction but cannot name the right intervention, I can give an exploratory model a bounded view of the work and ask what I am missing. If the answer would carry real consequence, I can ask for another reading, compare the evidence rather than the eloquence, and move the problem I choose into the harness most likely to finish it cleanly. For known jobs, I still want the detailed run spec, clear boundaries, and proof Codex has taught me to demand.

I am still divided. Gun to my head, Fable won this test because its strategic perspective gave me more to work with. Tomorrow I will probably burn more tokens in Codex because the harness is fast, dependable, and much easier to live in.

But the fun part is that I do not have to carry all of the noticing alone anymore. I can ask AI to look. I can disagree, agree, align, shade the perspective, choose the problem, and then build. I still decide what happens next.

## Coming up

Coming up this Sunday: an Executive Briefing on why you can rent the smartest model on the market, but the learning loop around it — the context and judgment that compound — is the part worth owning.

## Related reading

- [Grab the one-minute test that tells you if your task needs a chat, one agent, a team, or nothing at all](https://natesnewsletter.substack.com/p/agent-shaped-work)
- [How to tell what AI you actually need for a job (LOL yes there’s a prompt)](https://natesnewsletter.substack.com/p/how-to-tell-what-ai-you-need-for)
- [Claude vs Codex: inside the trillion-dollar battle for agents](https://natesnewsletter.substack.com/p/claude-vs-codex-inside-the-trillion)

![](https://substackcdn.com/image/fetch/$s_!4953!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5a26939-510d-4f45-b63a-c0b1a014c074_1390x768.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/let-ai-pick-what-to-automate?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-07-20T09:37:36-04:00*
