---
title: "Allie K. Miller's AI workforce model — working extraction (eng-002 Step 1 input)"
date: 2026-08-24
project: agents-sdk-redesign
engagement: eng-002
status: extracted
tags: [research, agent-fleet, workforce, proactive-agents, eng-002]
source_type: video-transcript
source_url: https://www.youtube.com/watch?v=EzQAgnjTq2k
source_title: "My top secrets to running an AI Agent Workforce"
source_channel: Greg Isenberg
source_guest: Allie K. Miller
source_published: 2026-08-12
source_duration: 48m28s
fetched: 2026-08-24
fetch_method: "/watch skill — yt-dlp native English captions (video.en-orig.vtt, deduped to 1,328 lines / ~10.1k words) + 10 transcript-cue frames at 512px via ffmpeg"
cost: $0 (native captions; no Whisper API call)
---

# Allie K. Miller's AI workforce model — working extraction

**Provenance note.** This is a first-party extraction from the actual captions and on-screen frames of the source video, not a summary of a summary. Every claim below carries a `[MM:SS]` timestamp locating it in the source. Three on-screen graphics were captured as frames and are transcribed verbatim in **§8**. Quotes are Miller's words as YouTube's auto-captions rendered them (auto-caption artifacts: "Ali" for "Allie", "cloud" for "Claude", "spitting up" for "spinning up" — corrected inline where unambiguous, flagged where not).

**What this extraction is for.** eng-002 is a redesign of Sean's `agents-sdk` fleet from a self-maintaining nightly cron set into a goal-mapped, proactive workforce. This note is the outside-evidence input to that engagement. It pairs with the eng-001 ledger (the inside evidence: what Sean's current fleet actually measured).

---

## 1. The headline reframe: you are not managing agents

Miller opens by rejecting the industry's own vocabulary. **"Managing agents" is the wrong verb** [02:09].

> "Managing agents feels like I'm their direct manager and I'm like, 'Suzy, go over there and Betty, go over there and Jeremy, go over here.' And I feel like I am three rungs above at like an SVP overseeing level, where I feel like I am setting up the infrastructure and then they are figuring out the best way to execute within that." [02:37–03:02]

The role shifts along three axes, each stated explicitly:

| From | To | Source |
|---|---|---|
| Managing | **Waiting for escalations** | [03:03] |
| Delegating | **Deciding what should or shouldn't happen** | [03:09] |
| Operator | **A liability role — final say, plus "critical thinking stops"** | [03:15–03:24] |

Her verdict on the alternative: *"anyone that is still talking about 'You should manage agents' feels like early 2026 talk."* [03:35–03:40]

Greg's counter is worth keeping because it names the actual motive: **"Do we want to manage agents? Managing people is hard... a big reason a lot of people like AI to do stuff for us is so we don't have to manage things."** [03:40–03:58]

Miller's resolution — and this is the design principle, not just a nice line — is that she **split people-management into the part she loved and the part she hated, then kept only the first when designing agents**:

> "I ran an org of about 100 people at AWS. The parts of people management that I loved, it was the making them better and empowering the [hell] out of them and seeing them completely blow past their ceiling... The admin side of people management and the admin side of agent management, I want that fully gone. The things that I love about people, I'm bringing that over into agents." [04:00–04:41]

**Steal:** the design question is not "what tasks do I delegate," it's "which half of management am I automating away, and which half am I keeping as the human job." Sean's current fleet automated the *admin* half (nightly hygiene) and kept none of the ambition half. That is arguably the eng-001 finding restated from the outside.

---

## 2. The best prompt she has ever written is three words

> "One of the best prompts that I have done with my AI workforce is three words... The best prompt ever." [04:49–05:02]

The prompt is: **`do smart things`** [05:52–05:55].

The prompt only works because of what sits behind it. Her stated preconditions [05:57–06:22]:

- Access to **every context doc she has** — business, friends, family, **2026 personal goals, business goals**
- Access to **meeting transcripts, email, calendar, Notion, Stripe, Supabase, GitHub**
- Run **"several times a day"** — "look across all these things and just do smart things"

And the model-capability gate, stated plainly: *"seeing how Fable 5 and GPT 5.6 and that level model is reacting to that vague flavor of prompt — you couldn't do this a year ago. Now you absolutely can."* [06:23–06:37]

**The origin of the prompt is the most stealable part.** She noticed that *she* was the ceiling:

> "It dawned on me that I was already functioning at the limit of my own imagination in my business. And that I could be doing way more ambitious things if only someone could manage me... Why am I not leaning on the AI agents to help me with this? Like, why is everything that they're working on initially prompted by me? **Even if it's a scheduled task, I still had to come up with that task and tell it to do it.**" [05:11–05:52]

> **Golden nugget — the cron trap.** "A scheduled task is still reactive, because I invented the task" is the sharpest single line in the video for eng-002's purposes. Sean's fleet is *entirely* launchd-scheduled tasks whose content Sean specified months ago. By Miller's definition it is not a proactive fleet at all; it is a reactive fleet on a timer.

**Scope expands, risk does not.** Asked whether "do smart things" means loosening the leash, she draws a precise boundary:

> "I would say I'm giving them more breadth, more scope, more flexibility. I'm not allowing them to now send 100 emails and before I used to have to check all the emails. I still check all the emails. **So the tier of risk has stayed the same, but the width has expanded.**" [07:46–08:03]

**Steal:** widen scope and authority independently. Autonomy over *what to work on* is a different dial from autonomy over *what it may do without approval*. Turn the first one up; leave the second where it is.

---

## 3. The Pyramid of Proactivity (five levels)

Miller credits **Alex Lieberman** with the pyramid and says she turned it into her own artifact [08:12–08:28]. She **writes goals for her agents and aims them at level five** (on-screen framing).

| Level | Behaviour |
|---|---|
| **5** | *"I've already solved this thing. Here's how I'll deal with it if it goes wrong. Here are next steps."* |
| **4** | *"I've already solved this thing — here are the trade-offs."* |
| **3** | Understands the goal behind the task |
| **2** | Does what it is told, and does it well |
| **1** | Waits for the instruction |

She maps this onto Greg's three-employee taxonomy [06:38–07:25]:

1. Does not finish the task
2. Finishes it well, but invents nothing
3. Finishes, exceeds, **and invents the next task on its own**

Her read on what separates a level-2 agent from a level-3+ agent [08:47–09:04]: **someone who understands goals, and who has been given (a) the power to rethink how things get done and (b) the power to actually execute.** Both, not one.

**The goals mechanism is concrete and ritualised** [09:04–09:30]:

- Goals for the AI workforce are **written out** as documents
- Documents live on her desktop **and are duplicated to Drive** so cloud workflows can reach them
- **Every quarter she runs a goals review *with* the AI workforce**

Her closing frame on this section is a direct challenge to how most engineers scope agents:

> "It's giving it a product mindset. I think it would be extremely limiting if you only treated this thing as an engineer when **it could be the greatest product lead you've ever had**." [09:38–09:49]

> **Golden nugget.** For a PM redesigning a fleet, this is the permission slip: the fleet's job is not to execute defined work, it is to *decide what work is worth doing against written goals.* That requires the goals to exist as machine-readable artifacts, reviewed on a cadence.

---

## 4. What proactivity actually requires (the three preconditions)

Miller distinguishes two generations of proactivity [10:33–11:41]:

**Gen 1 — proactive automations that are trigger-based (defined workflows).** Her worked example: a screen recording lands in one folder → transcript auto-generated → saved to the transcript store → **nine social posts generated in her voice** for X, LinkedIn, Instagram reel scripts. She dismisses this as *"easy automation land."*

**Gen 2 — "proactive of undefined workflows"** — which she names as the interesting problem for the back half of 2026:

> "AI is probabilistic all the time and not deterministic, but I want to take that probabilistic nature of reasoning — like the step zero of reasoning — and apply that **to the actual tasks that it takes on**." [11:42–11:54]

**The three preconditions for an agent to act on its own** — she says this holds "whether you're talking to a human or an agent" [11:56–12:11]:

1. **The goal / the star / the vision** — what are we aiming at
2. **Access to tools *and permission to use them* in the way that actually gets work off your plate** (she separates access from permission)
3. **A sense of what would normally trigger that sort of action**

**Steal:** #3 is the one most fleets skip. Triggers usually get hard-coded as cron entries. Miller's version is that the agent holds a *model* of what circumstances warrant action, and evaluates it — which is what makes the difference between "runs at 2:30am" and "noticed something."

---

## 5. Make the whole company queryable (the diary)

> "I want my whole company to be queryable. I want AI to have context on everything that's happening." [12:27–12:33]

The gap she found: her agents had meeting transcripts, Gmail, calendar, Slack — but **"there was a lot that was not yet codified"** [12:41–12:43]. The uncodified part is judgment: what a client actually needs versus what they say they need, what she decided and why, what she now believes.

Her example of the uncodified [12:51–13:02]: *"this client, they think that what they need help with is workflows under the CMO, but actually what they have problems with is reskilling and finding new roles for this one department."*

**The mechanism** [13:03–13:51]:

- **AI prompts *her* every single day** to capture it (the agent initiates the context refresh — the human is the data source, the agent is the collector)
- Rendered **in her brand colors**, with a small prompt, because she's working *"with maybe 10% of my brain still working at the end of the day"*
- It **reminds her to dictate, "because that's four times faster than writing"**
- Sessions run **5 to 40 minutes**, end of day or throughout
- Output banks into her **personal wiki**
- On-screen counter at time of recording: **80+ entries**

Why it matters, in her words [13:56–14:16]: agents working at the flexible layer *"have to have the right context or else all their stuff is going to be wrong."*

She gives the failure mode that forced this — and it is a context-staleness bug, not a model bug [14:16–14:31]:

> "It was like, 'oh, I saw that Greg confirmed that interview.' And it's like, no, Greg confirmed it, but we're still figuring out dates and I'm doing it over text, and iMessage MCP broke so you can't see that."

Her honest timeline: **"there was a lot of stuff that we had to continually fix and it took probably months to get to where we are now."** [14:31–14:36]

---

## 6. The org structure — 34 agents, and the two roles that matter

**Shape** [14:51–15:35, confirmed on-screen at 18:20]:

- **1 AI chief of staff — Simon** — "runs this whole org"
- **6 directors**, by business function: **education, client work, operations, marketing, product, + Phoebe**
- **34 agents total** beneath them
- All named after **Friends characters**
- She views the whole thing through **"a mission control where I'm seeing how all this stuff is moving around"** [20:11–20:15]

**The anti-2015 rule.** The most counterintuitive structural claim in the video [15:40–16:39]:

> "We have all these agents that do all these tasks and we have skills... And I have to remind myself that **that is operating in 2015 world if I give all of them job titles that existed in 2015**. So if I name them CMO or chief product officer and the person underneath it is a front-end engineer and a back-end engineer, then it feels like I am operating in 2015 org structure."

The economic argument that unlocks it [16:45–16:55]:

> "All of these employees basically cost $0. And so, **at the margin, I can hire any flipping person I want to.**"

### 6a. Phoebe — the chief dreaming officer (the ambition function)

> "I just wanted this weirdo. So I hired Phoebe as like a weirdo in the corner who's just looking at all these things that we're working on, and Phoebe acts as this almost **end layer** for things that are getting generated to go: **'How do we 10x it?'**" [16:55–17:11]

Her origin story for the role is the "David" anecdote [17:14–17:50] — a colleague at Amazon so ambitious she jokes she'd pay him to interrogate her Spanish-Inquisition-style: she answers how she'd do something, and he *"slaps me across the face and says, how would you 10x that?"* Phoebe is that person, instantiated. Explicitly: **"one that I would have never hired in human world"** [17:12–17:14].

Architecturally, Phoebe is a **post-processing critic layer over the workforce's output**, not a producer.

### 6b. Toby — Simon's assistant (the self-improvement function)

This is the mechanism that answers "how does the workforce self-improve," and it is a *role*, not a feature:

> "Toby is Simon's assistant whose **only job is watching the AI workforce work, take down notes, what still has friction, and who needs access to what**." [18:20–18:29]

The behaviour she describes [18:36–18:49]:

> "If we found that one agent did not have access to this, and Toby was like: **'every single time you keep correcting this one agent's output — have you thought about giving your agent access to this?'**"

**Steal — this is arguably the single most portable idea in the video for eng-002.** Toby is a meta-agent that measures the *human correction rate per agent* and converts a repeated correction into a concrete infrastructure proposal (grant this access, fix this context gap). It is self-improvement grounded in an observed signal, not in an LLM asked "how are you doing?" Contrast with the current fleet's meta-agent, which reports health rather than friction.

Her stated principle behind it [22:26–22:32]: **"stop relying on only yourself to find these blockers."**

### 6c. Model tiering

Stated in passing but concrete [20:27–20:38]: *"Now I understand that that agent can run off of a smaller model. **Not everything needs Opus. All of my sub-agents are like Haiku and Sonnet.**"*

---

## 7. How to build one — her prescribed ramp

She insists people **start with traditional job titles** and grow out of them [19:43–19:45, 20:41–20:43] — the 2015 org chart is where you begin and what you outgrow, not something to avoid at the start.

**The ramp, in her order** [19:45–20:11]:

1. What does it feel like to work with **one agent**?
2. What does it feel like to work with **one agent doing things on my behalf proactively**?
3. What does it feel like for **two agents to work together** on a task — or for one to **route to** the other?
4. What does a **workforce** look like, and how do all those things interact?

What you learn only by doing it, in her list [20:16–20:38]: how they trade notes, how context is passed, that things have to run in parallel, that an agent didn't need those tools, that an agent can run on a smaller model.

**The cold-start prompt.** She claims a workforce is one prompt away [21:19–22:03]:

> "I am a founder. I am building an AI personal shopper. My team is three humans. Here's what we do. Here's where we're based. Here's our goal... **Interview me. We're going to build out an AI workforce together.** Something that runs more efficiently and achieves my goals of saving at least 5 hours a week, capping my meetings to 15 hours per week, and make sure that I get into my capital raise by October."

Note the shape: **role + context + numeric goals + "interview me."** Goals are quantified and deadlined *in the bootstrap prompt itself*.

**Her honest split on effort** [22:03–22:26, 24:20–24:42]:

- Baseline workforce, connected to tools: **"under 3 hours"**
- Getting from "agents exist and have markdown files" to **"the 90% plus level"**: *"months"*, and *"that is all going to come through iteration cuz it's so specific to each person"*

**Steal:** the honest framing to hold onto — one prompt gets you a workforce; only iteration against your own friction gets you a *good* one. She names the common failure directly [21:03–21:11]: people *"try, they fail, and they're like 'this isn't for me' or 'the models aren't good enough yet.'"*

---

## 8. On-screen artifacts (verbatim from captured frames)

Three graphics were rendered on screen. Transcribed exactly:

**Frame t=08:32 — "THE PYRAMID OF PROACTIVITY"**
> Subtitle: *"Alex Lieberman's five levels. Allie writes goals for her agents and aims them at level five."*
> L5: "I've already solved this. Here's how I'll deal with it if it goes wrong. Here are next steps." · L4: "I've already solved this thing — here are the trade-offs." · L3: Understands the goal behind the task · L2: Does what it is told, and does it well · L1: Waits for the instruction
> Footer — GREG'S THREE EMPLOYEES: 1. Does not finish the task 2. Finishes it well, but invents nothing 3. Finishes, exceeds, and invents the next task on its own
> Pull quote: *"…it could be the greatest product lead you've ever had." — Allie K. Miller*

**Frame t=12:45 / 14:52 — "MAKE THE WHOLE COMPANY QUERYABLE"**
> Subtitle: *"Meetings, email and Slack miss the context that decides the answer."*
> **80+** diary entries banked, in a personal wiki her agents read
> HOW — *dictated, not typed*: 4x faster than writing · 5 to 40 minutes, end of day · AI prompts her for it daily
> WHAT GOES IN — *the uncodified part*: what a client actually needs · what you decided and why · what you now believe and why
> **WHAT ANY AGENT NEEDS BEFORE IT CAN ACT ON ITS OWN**: 1. The goal and the North Star 2. Tools, plus permission to use them 3. A sense of what would normally trigger the work
> **TRIGGERS ARE THE EASY HALF — ALREADY RUNNING**: A screen recording lands in the folder → transcript, then nine social posts in her voice (X, LinkedIn, Instagram reel scripts). *"The hard half is proactive work with no defined workflow."*
> Pull quote: *"I want my whole company to be queryable." — Allie K. Miller*

**Frame t=18:20 — "A 2026+ ORG CHART"**
> Subtitle: *"2015 job titles give you a 2015 org. At the margin, these hires cost nothing."*
> **SIMON** — AI chief of staff — runs the whole workforce · **TOBY** — Simon's assistant — *watches the workforce work, logs friction and missing access*
> Directors: EDUCATION · CLIENT WORK · OPERATIONS · MARKETING · PRODUCT · **PHOEBE — chief dreaming officer**
> *SIX DIRECTORS · 34 AGENTS UNDER THEM · ALL NAMED AFTER FRIENDS CHARACTERS*
> **WHY PHOEBE EXISTS**: *"The weirdo in the corner. She reads what the workforce produces and asks one question: how do we 10x it? A human budget would never carry this role. An AI workforce carries it for nothing."*
> Pull quote: *"All of these employees basically cost zero dollars." — Allie K. Miller*

**Frame t=45:28 — Slack screenshot**: a message with the reaction *"**Claude** reacted with :saluting_face:"*. The anecdote it illustrates is in §10.

---

## 9. AI as watchdog — and "dashboards are dumb"

Miller calls this *"one of the best use cases that exists right now, and almost no one is doing this"* [22:29–22:37]. Her three named watchdogs [22:37–22:50]:

- An AI watchdog **in Slack** — to catch **duplicative work**
- An AI watchdog **on the calendar** — to catch **conflicts**
- An AI watchdog **over meetings** — to see **where disagreement is happening**

She frames the whole category as an unworked seam: ten years ago "compare and contrast with AI" on contract redlines was the greatest use case ever, *"and yet no one today is using AI for this weird **cross-functional gap analysis** at a more advanced level than we would have done 10 years ago."* [22:51–23:22]

**The delivery standard.** When Greg asks about opportunities, watchdog-with-insight is her #2 — and she states the bar sharply [25:57–26:29]:

> "AI as a watchdog over any single thing that I am normally tracking. And I don't just mean visibility. **I think dashboards are dumb**, but I want visibility **with anomaly detection or insights** or something. So don't just tell me what my social media following is or views or whatever. Tell me **what are people talking about? What are people best reacting to? What is not performing well? What should I do tomorrow? Write me a script that helps me for that.** So: AI as a watchdog, but with **insights into action**."

> **Golden nugget — the eng-001 rhyme.** "Detection without delivery" (eng-001 d40) and "dashboards are dumb, I want insight-to-action" are the same finding reached from two directions. Miller's version supplies the missing half of the standard: the output of a watchdog is not a state report, it is *the next action, pre-drafted.* "Write me a script that helps me for that" is the delivery bar.

---

## 10. Multiplayer — the workforce is not single-player

Miller's #1 "one thing I want people to think about" at the close [45:50–46:14] is that the workforce should be **multiplayer**: not just an AI workforce, but *"a multiplayer AI workforce that other humans can chime in on — and have it be proactive."*

The concrete implementation [23:22–24:20]:

- **Claude is in every one of her chat channels**
- A dedicated Slack channel called **`Loop Allie`** *(captioned "Loop Alley")* where **"my human team can talk to my AI workforce"**
- Worked example: a teammate asks in Slack *"did that large financial services client respond to Allie's email?"* — **the workforce answers the teammate directly**, and *"that person will not have to wait for me for 5 hours to get back to them"*

She flags the tooling honestly [23:22–23:35]: **Claude Tag** helps here but *"it's a mess right now in this exact moment that we're recording this... to set up"*; she also wired her own Claude Code into Slack.

**The weirdness anecdote** [45:01–46:42]: she wrote something unkind about Claude in a Slack channel late at night; a 🫡 emoji reaction appeared; she hovered — it was Claude. She asked *"is that you?"* and got back **"Yep. That was me. I'm here."** Her framing: lean into the weirdness, keep 10% of the fear next to you.

Her three closing asks of the audience [45:50–46:33]:
1. A **multiplayer** AI workforce other humans can chime in on, that is **proactive**
2. Give it **flexibility to roam free**
3. Work out what it looks like for **a teammate or a system to up-level** — "dark factory" space or just answering better questions in Slack

---

## 11. Build the factory, not the thing

Her #3 arbitrage opportunity, and the one she says almost nobody is talking about [26:29–30:10].

The choice, in her framing: you want to ship a product (her AI-First Index benchmark). **Option one** is to point Claude Code / Codex / Anti-Gravity at it, iterate for hours or days, ship. **Option two** is to recognise that *"that's probably not going to be the only product you build, or the only iteration of that product you build"* — and instead build **"a mini and very beginner software factory."**

> "It's going one level up in abstraction. It's like what dev tool companies did for engineering, but **you're creating dev tools at that level for yourself.** You're going to the kernel level for yourself." [27:54–28:06]

You build the **primitives** everything will need — login, payments, social sharing, newsletters to promote the thing [28:18–28:31]. She calls it *"measure twice, cut once, but the measurement is building out that foundational layer"* [28:43–28:48], and describes the result as **"optimizing loops... that aren't super autonomous and are very heavy-handed with humans"** [28:59–29:06].

The learning rule inside the factory [29:35–29:47]: **"I want to learn through the mess. Like we had a webhook issue, whatever. I want to learn through that mess and then I want to never make that mistake again."**

Generalised [29:47–30:09]: *"Think of the factory behind the one singular task instead of the one singular task itself. That is one of the biggest ways to rethink work in the AI age."* — applicable, she says, to a content engine or net-new lead handling, not just product building.

---

## 12. The bottleneck rule (how she picks what to fix)

A precise correction to standard advice [37:10–37:29]:

> "A lot of people will say the phrase 'look for the bottlenecks and solve the bottlenecks,' and I always kind of disagreed with it — or I don't think it's fully complete. The phrase that I say is: **look for the bottlenecks, then evaluate the value of fixing those bottlenecks, and then pick the bottleneck that is high value to fix.**"

Her example of correctly-identified bottlenecks: not writing code, not design — but *getting a local HTML file into an actual iOS app*, or word-of-mouth/referral mechanics [37:30–38:14]. And: *"video creation, no matter how much AI is helping me edit — it is still a slog. So that is still a bottleneck and it's very high value."* [38:23–38:37]

**Steal:** this is a prioritisation rule the redesign can adopt directly — an agent that is unreliable but low-value is not the one to fix first.

---

## 13. Adjacent claims worth noting (context, lower priority for eng-002)

- **Scale of the opportunity** [25:15–25:53]: of all AI users, the share who are paid users *and* using Codex/Claude Code is *"minuscule."* Building even a basic workforce puts you *"top 1%, probably top 0.5%."* Getting to the advanced level *"feels like I'm operating a company of a thousand people and not my small scrappy Gremlin group."*
- **`/last30days` endorsement** [42:13–43:47]: she names Matt Van Horn's `/last30days` skill as *"amazing"* and says she has **integrated it with her Claude wiki**. Her uses: spin up on an unfamiliar industry or company before a workshop; and idea-generation — *"startup ideas that could be built by someone with the following background or the following skills."* **(Sean already has this skill installed and it ran 76 days ago.)**
- **SaaS-pocalypse** [32:33–34:52]: mediocre software dies, but slower than predicted — because enterprises are bandwidth-constrained, and because *"you want someone to call... you also want someone to blame."* Liability is her first question about any AI replacement. Plus a lag argument: incumbents get day-one access to new models; you get day-30.
- **Where value shifts** [36:25–36:56]: on the consumer side, from science to art — creative/video-first people win; code matters less.
- **Research avenues for opportunity-spotting** [41:35–44:56]: watch what YC publicly asks for (assume they're 18 months out); use `/last30days`; and listen for the **fear questions** executives are asking now that they weren't three years ago.

---

## 14. What this video does *not* give you

Recorded honestly, because eng-002's PRD needs evaluable criteria and this source does not supply them:

1. **No usefulness metric.** Miller never states how she measures whether an agent earns its keep. Toby measures *friction* (corrections, missing access) — a maintenance signal, not a value signal. There is no "consumption is the gate" equivalent, no cost-per-useful-output, no kill criterion for an agent that produces nothing anyone reads.
2. **No eval or regression discipline.** No mention of evals, test cases, or how she'd know a workforce change made things worse.
3. **No failure/incident handling.** Nothing on what happens when an agent acts wrongly at level 4/5, beyond "I still check all the emails."
4. **No cost accounting.** *"These employees basically cost $0"* is stated as an axiom [16:48], never reconciled against token spend. Model tiering (Haiku/Sonnet for sub-agents) is the only cost mechanism mentioned.
5. **N=1, and hers is a client-facing consulting business** with a human team, a content engine and paying Fortune 500 clients. The goal structure transfers; the business shape does not.
6. **Attention cost unaddressed.** Everything is *more* output aimed at her — daily diary prompts, watchdog alerts, Slack answers, Phoebe's 10x notes. She never discusses the ceiling on how much a single human can absorb. eng-001 d42 ("attention is the real cost") is the counterweight this model lacks.

---

## 15. The extraction, compressed to what eng-002 should carry forward

1. **The cron trap** — a scheduled task you invented is still reactive. [05:46]
2. **Proactivity has three preconditions** — written goal, tools *plus permission*, and a model of what should trigger action. Triggers are the easy half. [11:56, on-screen]
3. **Scope and risk are separate dials.** Widen what it may work on; keep what it may do without approval. [07:46]
4. **Goals must be machine-readable artifacts, reviewed quarterly *with* the fleet.** [09:04]
5. **A Toby role** — one agent whose only job is watching the others, logging friction and missing access, and converting repeated human corrections into concrete infrastructure asks. This is the self-improvement engine. [18:20]
6. **A Phoebe role** — a critic layer over output asking "how do we 10x this," justified purely because marginal cost is ~zero. [16:55]
7. **Don't inherit 2015 job titles.** Structure by what the work actually is. [15:40]
8. **Watchdogs, not dashboards** — output is anomaly + insight + the drafted next action, never a state report. [25:57]
9. **Multiplayer** — the fleet should be addressable by, and answer to, people other than its owner. [23:22, 45:50]
10. **Capture the uncodified** — a daily agent-initiated, dictated capture of judgment that never reaches transcripts or email. [12:27]
11. **Build the factory, not the thing** — invest in the primitives, learn through the mess once, never repeat it. [26:29]
12. **Bottleneck rule** — find them, *value* them, fix the high-value ones. [37:10]
13. **Ramp deliberately** — one agent → one proactive agent → two coordinating → workforce with mission control. [19:45]
14. **Honest timeline** — 3 hours to a workforce, months to a good one, and it is person-specific iteration. [22:03, 14:31]

---

## Reproduction

```
yt-dlp 2026.08.19 · native en captions (auto-generated), no Whisper call
/watch --detail transcript  → transcript
/watch --detail transcript --timestamps 8:32,9:02,12:45,13:12,14:52,15:22,18:20,20:14,45:28,45:44  → 10 cue frames @512px
```
Working directory (ephemeral, scratchpad): `watch-akm/` (captions) and `watch-akm2/` (frames). Deduped transcript: 1,328 lines / ~10,127 words.
