---
name: content-oracle
description: Stage 0 of the content machine. Three supplies — a sweep of the author's own systems (git, dailies, closed issues, partner-session sidecars, fleet manifests), a news lane (AI news of the week, gisted), and a frame stage (four tool-denied lenses proposing experiments he could run) — plus a last30days anchor scan; one scoring pass; two decks ("worth a piece this week" on six signals, "worth posting" on five) so a writing session starts from a concrete idea instead of a blank page. Unused cards bank rather than evaporate. Use when asked "what should I write about", "find me content spikes", "what's worth writing this week", or to "run the content oracle". NOT the separate `the-oracle` capture/reminders project at ~/Code-Brain/the-oracle/ — a bare "run the oracle" is ambiguous between the two, so ask which one. On-demand only: it is on probation and has no schedule.
---

# Content Oracle

The Oracle ends "what do I write about." It does not write anything.

It reads what the author actually did in the last seven days, what happened in AI
that week, and what four different lenses say he could go find out — then scores the
lot once and hands him two short decks to pick from: **worth a piece this week** and
**worth posting**. Stage 1 of [`content-machine`](../content-machine/SKILL.md) takes
it from there.

Build tickets: [#169](https://github.com/seanwinslow28/code-brain/issues/169) (the
sweep and the six signals), [#227](https://github.com/seanwinslow28/code-brain/issues/227)
(the rulings after week 1 failed), [#238](https://github.com/seanwinslow28/code-brain/issues/238)
(frame stage, two decks), [#239](https://github.com/seanwinslow28/code-brain/issues/239)
(news lane, listening report). Pattern source: Alex Lieberman's content machine (the
five long-form signals are his, transcribed verbatim; the sixth is Sean's addition).

## The card bar: an experiment he could run

**A topic becomes a card when it names an experiment Sean could run.** Not when it
names something he did.

The experimentation thesis is *what he would go find out*, not *what he did*. Week 1
read it the other way — the sweep supplied every noun, so every card was a commit
wearing a story — and he denied all twelve, because *"me tweaking things in my
codebase isn't always going to be a story."* Commits are boring because commits are
not experiments. A card proposes a subject and an experiment; the interview happens
after he has run it.

This keeps the origin law whole. A card **never asserts he did something**. A
synthesized spike claiming he found X is still banned, and it is banned for a reason
the gates cannot fix: by interview time he really will say the words, so the origin
gate downstream passes the fake premise as his. The only thing a card may claim is
"do this, expect that," and everything on it is a hypothesis until he runs it.

Two shapes of card follow, and the deck is mostly the first:

- **Experiment cards** — an experiment he could run this week, from a frame angle, a
  news item, or a sweep item that has an open question in it.
- **Done-thing cards** — the #169 shape: a moment that already happened, with an
  artifact behind it. Still legal, still scored the same way; just no longer the only
  shape, and no longer the default.

And a bar on the first, in his words: not *"Fable 5.1 dropped, can it one-shot X."*
That is the easy content the publication exists against. *"Exploration and seeing what
it's capable of that people might not have thought about... instead of one-shot
prompting."*

## The evidence rule

**Every card carries an evidence pointer. A card with none is an invention.** The
pointer takes one of two forms, and the form says which shape of card it is:

| Card | `Evidence:` holds | Plus |
|---|---|---|
| **Done thing** | the artifact: a commit sha, a `vault/daily/<date>.md`, an issue number, a sidecar filename, a URL | — |
| **Experiment** | the **provocation**: the news URL, or the sweep item, that prompted it | `Status: unrun` |

This is the origin law (`content-machine`'s L2) applied one stage earlier. The
machine exists so drafts come from things the author said; an Oracle that
synthesized plausible-sounding spikes out of metadata would poison the well at the
source, and the origin gate downstream cannot catch it — by the time the interview
runs, the fake premise is what he is being interviewed *about*.

An experiment card cannot point at an artifact, because nothing has been done yet.
So it points at what prompted it, and says so with `Status: unrun`. A frame angle
with no provocation — nothing in the week and nothing in the news that it answers —
is still an invention, and it still banks. If neither the sweep nor the news lane
nor a frame surfaced it, it is not a card.

## Deck one — worth a piece this week (six signals)

Five are Lieberman's, from the founders transcript — the Oracle "hunts for spikes,
and spikes are basically how much point of view is there, how much story potential
is there, how much emotional intensity is there, how much lesson or framework is
there, and how much depth is there." The sixth is the L7 amendment. These were all
built for long-form, which is why they are one deck and not the only one.

| Signal | The question | 0 | 3 |
|---|---|---|---|
| **POV** | Is there a take, or only an event? | it happened | he disagrees with someone, on the record |
| **Story** | Is there a scene — a moment, a before/after, another character? | a state | a thing that happened at a time, with a turn in it |
| **Emotion** | Did it cost him something? | routine | he was wrong in public, or it broke and he had to sit with it |
| **Framework** | Is there a transferable shape? | one-off | a rule someone else could apply tomorrow |
| **Depth** | Are there specifics — numbers, names, mechanisms? | vague | measured, named, reproducible |
| **Spine** | Does it serve the Pencil & Prompt experimentation thesis? | a detour | it *is* the thesis |

Score each 0–3. Rank by the sum, out of 18.

**Spine is a veto, not an addend.** A card scoring 0 on Spine never enters the deck
no matter what the other five say — it banks. Two reasons, and the second is the
one that bites: L11 fixes the editorial law (the machine serves the existing SOUL,
it never invents unrelated stories), *and* the external scan runs on every
invocation, so without a veto the deck fills with other people's news on the weeks
his own material happens to be quiet. A high-scoring detour is the most dangerous
card in the deck, because it is the one he'll pick.

**This is not the banned scoring loop.** L8 rejects machines that score *drafts* and
revise until the number is good. Ranking *candidates* is what an Oracle is for, and
the author picks from the deck — the number orders the list, it decides nothing.

**Spine for this deck means a capture is required**: a past spike, or an experiment
he would run. *Not* "a model dropped, can it one-shot X" — that scores 0 here
however loud the release was.

## Deck two — worth posting (five signals)

An X card scores near zero on Story and Depth **by construction**: the X contract
gives the medium room 1 and no arc. In a shared ranking it sinks under every
long-form card, and the ranking is meaningless anyway — a Substack card and an X card
are not competing for one slot. So posts get their own deck, scored on what actually
makes a post land. Two definitions are reused from
[`contracts/expressive/LANE.md`](../content-machine/contracts/expressive/LANE.md)
rather than reinvented: the first screen on X is the post to the fold plus the
attached image, and the reply-hook question is "where would a reader want to argue."

| Signal | The question | 0 | 3 |
|---|---|---|---|
| **Angle** | Is there a turn? | it happened | the reader expects one thing and gets another: funny, unexpected, or teaching what's possible |
| **Clock** | Is there a reason this posts this week? | could post any week | the thing it reacts to is live now and stale by next Sunday |
| **Fit** | Does it land in one sentence? | needs a thread to make sense | one landed sentence, no setup (the contract's room 1) |
| **Image** | Does a picture carry the first screen? | nothing to show | an artifact that already exists *is* the post and the words are its caption |
| **Reply-hook** | What does a reader say back? | "nice," or nothing | they argue with it, or add their own instance |

Score each 0–3. Rank by the sum, out of 15.

**Spine-X is the veto, with its own bar: an angle exists, and the post is not an
announcement.** A pure take is legal here. *"Fable 5.1 just dropped!! It's OVER"* is
not, however many people would like it. Two guards are written into the scale:

- **An engagement question scores 0 on Reply-hook.** The lane law already says a CTA
  is the absence of a hook; scoring it 0 stops the deck drifting toward "what do you
  think?"
- **Image scores only what already exists.** "Could generate a chart" is a 1, because
  that is writing-from-nothing in picture form, and #172 already treats on-screen
  content as a claim.

Why five and not three: Fit and Image decide *which subject* becomes an X card, not
how it is formatted. A spike with a screenshot behind it is a different X candidate
from the same spike without one. That is card-time information.

## The LinkedIn credibility tag

LinkedIn is not a Spine column. L4 holds: it is a syndication target, never a
composition surface, and *"here's how I'm using it in my workflow as an AI PM"* is
native composition, which `contracts/professional/linkedin.md` bans outright.

Instead, **AI-PM credibility is a tag on the card**: `Cuts to LinkedIn: yes | no`. It
labels both decks and it **never moves a rank** — a tag, not an addend. Same lesson
as Spine-as-veto: a summed score lets the wrong cards climb on quiet weeks, and a
model release is the textbook case, maximally cuttable to LinkedIn and often a thin
story. The tag shapes *which Substack or X piece gets written*; the LinkedIn cut
follows whichever artifact ships, last, per L4.

## Interviewability

Not a signal — a gate on the card's usefulness. The machine can only write from what
he says, so a spike he cannot be interviewed about is worth nothing however it
scores. Every card therefore names its interview lens and what the interview has to
go get. If that field cannot be filled, the card is not ready and it banks.

For an experiment card the interview happens *after* he runs it. The field still has
to be fillable now: what the interview will have to go get once there is a result.
An experiment nobody could be interviewed about is a benchmark, not a piece.

## Running it

**1. Internal sweep** (stdlib, no model, $0):

```bash
python3 .claude/skills/content-oracle/sweep.py --days 7
```

Six sources: `git` (commit subjects and bodies, bookkeeping subjects dropped),
`issue` (closed GitHub issues — wayfinder resolution comments are the densest story
source in the repo, because they are where a decision's real cost is written down),
`daily`, `sidecar`, `fleet`, `tickets`. `--only <source>` narrows; `--out <path>`
writes to a file and **refuses any path git does not ignore**, because dailies and
sidecars are private material (CLAUDE.md rule 9).

**Sweeps are not retained, and there is no `sweeps/` directory on purpose.** The
default is stdout, straight into the session. Nothing downstream reads an old sweep
— the ideas bank already holds everything that mattered, as cards — so a sweep store
would be a second verbatim copy of his dailies and sidecars bought for nothing.
`--out` exists for a scratch path when a run is too large to hold in one read; put
it somewhere git-ignored and delete it after.

The sweep gathers and does not judge. Same split as the origin gate: mechanical
collection, then a reading pass. A harvester that scored would be guessing at
stories from metadata.

**2. News pull** — AI news of the week, big and small, across the five subject
branches ruled on #227: AI news, tools, agents, system design, and creativity with
AI. Built on [#239](https://github.com/seanwinslow28/code-brain/issues/239). It is
a NEWS-shaped pull on purpose (see the query table below: this is the one place
"latest on X" is allowed).

```bash
python3 .claude/skills/content-oracle/news_lane.py pull --date <sunday>   # five queries, free legs, ~3 min, $0
```

`pull` runs one fixed NEWS-shaped query per branch through `last30days` on its
**free legs only** (`hn,youtube,web`) — Reddit and X spend ScrapeCreators credits
and answer a different question, so they stay with the anchor scan — and writes two
files to the git-ignored `creative-studio/content-machine/oracle-reports/`:
`<date>-pull.md` (everything fetched, transcripts included) and
`<date>-pull-index.md` (titles and URLs only; read this one first). The script
refuses any path git does not ignore. It gathers and does not judge, same as the
sweep.

**Read the index, then write the gists.** Each item worth carrying yields a
**two-line gist** for the frame stage — what happened, and what the thing can now
do that it could not last week — in a git-ignored `<date>-gists.json`:

```json
[{"happened": "<what happened, one line>",
  "can_now": "<what it can now do that it could not last week>",
  "source": "<URL — kept for the card's Evidence field; generators never see it>"}]
```

```bash
python3 .claude/skills/content-oracle/news_lane.py gists --check <gists.json> --pull <pull.md> [--report <report.md>]
```

`gists --check` is the anti-fabrication gate one stage upstream of the frame
stage: every gist's `source` must be a URL the pull actually fetched (or one the
report's audited Sources fence carries), the two lines may carry no URL, path,
sha or address, and the frame stage's field caps apply. **A gist with no fetched
URL behind it is an invention**, and it would become a card's `Evidence:` line.

A news item is a card candidate in its own right (a **news card**: Sean consumes
the article or video, an angle forms, the interview follows) *and* a provocation
for the frame stage. The listening report that renders the week's news to local
TTS is the other half of this step — see [The listening report](#the-listening-report).

**Measured on the first pull (2026-09-03), three things about the engine:**

- **The legs are different instruments, so each gets its own phrasing.** YouTube
  and the web leg answer NEWS phrasing; the Hacker News leg is a literal keyword
  search over the window, and "this week" in the query finds nothing there. Each
  branch therefore carries two phrasings (`BRANCHES` in the script): the NEWS shape
  for YouTube and the web, bare nouns for HN.
- **HN runs through the `last30days` library, not its CLI.** With Reddit and X both
  off, the CLI takes a fallback path that never starts the HN search at all — the
  section silently does not exist. The library call works, and it hands back the
  story's own URL beside the thread URL, which is the primary source the tier audit
  wants. The web leg, by contrast, answers NEWS phrasing with aggregator trackers
  and category landing pages (tier C), so the primary usually has to be found by
  following the item.
- **YouTube ignores the window.** On NEWS phrasing it ranks by relevance and returns
  evergreen roundups from months ago whatever `--days` says. The index lists
  out-of-window items apart; they are not this week's news.

**3. Frame stage** — four fresh, tool-denied lenses on a stripped week (#227 rulings
18–19; built on #238). This is the supply the sweep cannot reach: a quiet week
produces boring nouns, and a lens applied to those nouns plus the news produces
experiments the nouns alone never would.

```bash
python3 .claude/skills/content-oracle/frame_stage.py --summary <ignored path> --gists <ignored path> [--dry-run]
```

- **The payload is stripped, and the script checks it.** The session writes a short
  summary of the week — nouns and shapes, no quotes, no paths, no identifiers — and
  the script refuses to dispatch if the summary carries a path, an email, a sha, a
  line lifted verbatim from a daily, a sidecar, the corpus or a transcript, or is
  simply too long to be a summary. `--dry-run` prints exactly what would be sent and
  sends nothing; **inspect it before the first live run of a new week.**
- **Four generators, each seeing only the summary, the gists, and its own lens
  card.** Headless `claude --print --tools ""`, the pattern validated in
  `creative-partner/references/divergence-stage.md`: fresh context and full tool
  denial enforced by the runtime, not by a prompt. Two natives + one foreign + one
  wild per run, natives from [`references/frames.md`](references/frames.md), foreign
  and wild from the creative-partner deck by reference. Rotates by week unless
  overridden. Each returns 3–5 experiment angles stamped with its lens id.
- **No critic call.** Divergence in `creative-partner` runs a fifth call to cluster
  and shortlist. Here the scoring pass (step 5) already clusters and ranks, so a
  critic would be a second judge. Four calls, roughly $0.20 on top of the $0 sweep.
- **A failed slot stays failed.** It is never re-rolled or replaced; the run header
  says how many of four returned.

**Where do fresh ideas come from if the generators have no tools, and does the
model's cutoff make them stale?** Freshness comes through the payload, not the
helper. A generator applies a forcing move — structural, cutoff-proof — to material
it is handed: this week's nouns and the news gists. The cutoff bites only if a
generator has to *know* a capability exists, which is why the news pull runs first
and each gist says what the thing can now do. Giving generators tools would make it
worse on three counts already measured in this repo: search pulls the vendor-SEO
shape (#170, and the query table below), tools are convergence pressure (the
2026-08-04 live run validated tool denial as the only pattern that kept four
generators different), and a helper with file access can read sidecars. The honest
limit, already on the record in `divergence-stage.md`: this samples the training
distribution more widely, it does not escape it. Four lenses on fresh material beats
one; it is not a web search and is not trying to be.

**4. External anchor scan** — the `last30days` skill, every run (Sean's ruling,
2026-08-26).

An anchor hit is **not a topic**. It is timeliness attached to something he
actually did, or a reaction candidate that must clear Spine on its own merits. The
question to ask of every anchor item is "which of his internal spikes does this
give a reason to publish *this week*" — not "what's trending." Subjects he has not
worked on enter through steps 2 and 3, not through this one.

### The sweep supplies the nouns — for anchor queries only

**Run the internal sweep first, then derive every *anchor* query from it.** The
usual order — scan the zeitgeist, then ask whether Sean has anything to say — is
what produces detours, and it is why Spine needed a veto. Inverting it makes the
editorial law mechanical: an anchor query built from his own week cannot return a
card about someone else's.

This rule used to govern *every* external query, and that is what made week 1 fail:
the Oracle was architecturally unable to propose a subject he had not already worked
on. It now governs anchor queries and nothing else. The news lane runs on its own
phrasing, and the frame stage phrases no search at all.

Pick the **two** internal spikes where the take already exists but the *reason to
publish now* does not — high Story and Depth, thin on nothing else. Those are the
ones an external anchor can actually improve. Two queries, not five: each
`last30days` run takes 2–8 minutes, and a deck is not worth forty.

### Query the friction, never the category

`last30days` branches on how the question is phrased, so phrasing decides the report
you get before any source is touched:

One table, two columns — the ban is scoped, not lifted (#227, ruling 18):

| Shape | Anchor queries (step 4, derived from his week) | News queries (step 2, the news lane) |
|---|---|---|
| "best X", "top X", "what X should I use" | **Banned.** Parses as RECOMMENDATIONS → a list of tools. Pulls vendor SEO and affiliate content. This is #170's documented failure reproduced on a different engine. | **Banned.** A roundup is not news. |
| "X vs Y" | **Banned.** Parses as COMPARISON → a head-to-head buyer's guide. Answers a purchasing question, not a writer's. (Fine to run deliberately outside the Oracle.) | **Banned.** Same reason. |
| "latest on X", "X news" | **Banned.** Parses as NEWS → what everyone else already read, and therefore already wrote about. An anchor wants the discussion *under* the news, not the news. | **Required.** The news lane is a NEWS-shaped pull by definition and uses this phrasing on purpose. |

Everything below parses as GENERAL, which is the mode that returns discussion rather
than a product roundup — and it governs anchor queries only.

**The phrasing rules govern the report, not the platforms — and the banned shape
re-enters through the platforms.** Measured twice, from two sources, which is the
evidence standard this machine uses (#175): run 3's GENERAL query got tool roundups
back from **YouTube** ("Best AI Tools for Writing Fiction," "The Perfect AI Writing
System"), and run 4's GENERAL query got them back from the **web leg** ("Best Open
Source LLMs 2026," "Top 5 Local LLM Tools," "Top 7 Local LLMs That Will Replace
Coding").

Roundups are what those platforms reward, so they are served whatever was asked.
Banning the phrasing stops `last30days` from *formatting* a buyer's guide; it cannot
stop a platform from *returning* one. **Nothing prevents this but reading the titles**
— which is the same instrument the thick-results diagnostic needs, and the reason it
is worth doing once, deliberately, before scoring anything.

| Shape | Template | What it's for |
|---|---|---|
| **Recantation** | `people switching back from {thing}` · `gave up on {thing}` · `{thing} removed` | The strongest single shape. It selects for **the thing stopped** — and the stop can be a choice or a removal. Either way the arc arrives already a story. |
| **Friction** | `{thing} problems in production` · `what breaks with {thing}` | Sorts practitioners from vendors. "In production" and "six months in" are the phrases marketing copy cannot fake. |
| **Contested claim** | `is {claim} actually true` · `{claim} disagreement` | Finds the fault line rather than the consensus. The best of these is a claim repeated everywhere that **nobody has measured** — which is Sean's opening, because he has a running fleet with cost caps, failure manifests and six months of receipts. A claim he can settle with evidence he already owns is worth more than any trend. |
| **Silence probe** | the specific mechanism, not its category — `origin fidelity LLM drafting`, not `AI writing tools` | Deliberately aimed where results should be thin. See below. |

**Open question — how to phrase a silence probe so it does not get rerouted.**
Unanswered, and the next silence probe's job.

Run 3 failed at exactly this. Describing the mechanism in plain practitioner English
got absorbed into the crowded neighbouring field, and the run came back full of
material about something else. Two known-bad options bracket the problem: the
author's own coined name for a mechanism (`origin fidelity`) tests whether the *word*
is private rather than whether the space is empty, and a neutral description of the
same thing collides with whatever large literature sits next door.

The untested hypothesis is to search for **the artifact the mechanism produces, or a
phrase only someone already doing it would write** — on the theory that practitioners
name their outputs before anyone names the category. One data point and no test, so
it is written here as a hypothesis and not as a rule. Try it, record which phrasing
was used in the card's `Query:` field, and let the bank settle it.

**The recantation shape catches forced removals, and they are usually the better
anchor.** Measured on the first live run (2026-08-27, the author-mode deletion): the
probe was aimed at practitioners who *chose* to abandon author-style prompting and
instead returned OpenAI removing the capability for legal reasons, plus the backlash.
Louder, better documented, and precisely dated, where a voluntary recantation is
diffuse and usually undated.

Take the removal, but do not let it become the piece. **A removal is a news event;
the piece is the difference between a capability being taken away and a capability
being tested and found wanting.** Sean's side of that comparison is what the card is
for — and it only exists because he ran the test first. Where he has no such test,
the removal is somebody else's story and Spine should say so.

### Thin results are a finding, not a failed query

**Do not broaden a query that returns little.** The reflex — no hits, try a wider
term — walks straight back onto crowded ground, which is the opposite of what the
scan is for. An unoccupied space with real internal material behind it is the
strongest card the Oracle can deck: he has the story, and nobody has the coverage.

Say so on the card. "Four threads in thirty days, no write-up" is evidence, and it
belongs in *Why it's a piece*.

**The inverse does not hold: thick results are not proof the space is occupied.**

A probe aimed at a specific mechanism can collapse into the crowded field next door
and come back full. Run 3 asked about diffing an AI draft against the human rewrite
to extract lessons, and returned 24 results across three sources — **not one of them
about that mechanism.** The query had been absorbed into AI-writing-as-culture-war:
detection, authenticity, is-it-cheating. The stats block said three sources answered.
It read like success. The probe had not run.

**Diagnostic: read the titles against the mechanism, not the counts.** If no result
names the thing you asked about, the probe did not execute, and the correct move is
to re-aim it — not to conclude the space is taken and not to score what came back as
if it answered. A false negative on silence is the expensive one, because it retires
the strongest card the Oracle can produce on evidence that was never about it.

**This is not a silence-probe problem. It is a gravity problem, and it has taken two
of the four shapes.** Run 4's contested-claim probe asked whether local open models
are good enough to replace cloud LLMs — a task-level question — and came back with a
culture-war thread about an uncensored model explaining how to make meth, top comment
*"the propaganda to stop open source models is in full force."*

**Any probe aimed at a specific question sitting next to a culturally loud one gets
dragged to the loud one.** Contested-claim is the most exposed of the four, because
`is {claim} actually true` is the exact phrasing the loud neighbour already owns.
When a probe lands in the attractor, re-aim at something the argument cannot be had
about in the abstract — a number, a mechanism, a named artifact — or drop the probe
and say so. Do not deck the culture war; Spine will not save you, because an
attractor thread genuinely is about the topic.

### What each source can and cannot carry

**Read the per-source counts before synthesizing, and record which source actually
carried the card.** A stats block listing four sources reads as four sources
agreeing, and twice now it has not been.

Two live runs, opposite profiles:

| Source | Run 1 — recantation | Run 2 — friction | Run 3 — silence | Run 4 — contested claim |
|---|---|---|---|---|
| **Reddit** | Carried it; thesis was a 123-upvote comment. | Carried it; thread *shape* was the finding. | Carried it, though the probe missed. | **Failed.** 22 threads found, **21 culled**; survivor was a viral culture-war post. |
| **X** | Nothing; all under 0.3 relevance. | Real material, buried at 1 like under promos at 35+. | Present, off-topic. | Answered a **different question** — see silent degradation below. |
| **YouTube** | Out-of-window tutorials, opposite of the query. | In window; dense transcripts; provenance hazard. | **0 of 6 in window**; category roundups. | 1 survivor, **out of window** (2026-07-24 vs a window opening 07-28). |
| **Hacker News** | Zero. | One story — a YC launch. Vendor, not practitioner. | Zero. | Zero. |

**Correction, and it retires a claim made after run 3.** After three runs the note
here read *"Reddit has carried every card in all three,"* offered as a reading order.
Run 4 falsified it. The engine discovered exactly the right subreddits — `r/LocalLLM`,
`r/LocalLLaMA`, `r/ArtificialInteligence` — searched all three, returned 22 threads,
and **discarded 21**. The practitioners were found and then thrown away by
engagement-ranked scoring, in favour of a single 1,435-point argument about an
uncensored model explaining how to make meth.

So **Reddit's three-run record was a property of those three topics, not of Reddit.**
Where a topic has a high-engagement culture-war attractor beside it, Reddit's scoring
layer selects the attractor and culls the practitioners — the same
engagement-inverse-to-specificity disease already recorded on X, operating one layer
deeper where it is harder to see, because the discarded threads never appear in the
report at all.

**The conclusion from four runs is that source yield tracks the topic, not the
shape.** Author-style mimicry lives on Reddit and nowhere else; agents-in-production
lives everywhere. So **no source is ever switched off** — the counts get read fresh
every run. The `Query:` field on every external card accumulates the rest.

**X is read against its own ranking, not skipped.** Engagement on this material runs
*inverse* to specificity: the post with a real number in it had a single like, and
the two posts framing agents as a lifestyle had seventy between them. Sort by
specificity yourself; the engine cannot.

**Hard rule: a statistic from a low-provenance source never enters a card.** Quote a
person, never a number.

Run 2's YouTube transcripts were the most quotable-looking material in the entire
scan — confident, dense, stacked with figures: *68% of deployed agents executed no
more than ten steps*, *53% of organizations saw agents exceed intended permissions*,
*59.5% are already running agents autonomously*. The videos had **6, 8, 3 and 0
views**, channel names like "Orange Banana," and read as machine-generated synthesis.
The surveys they cite may well be real; none of them was verified, and none of them
is checkable from the transcript.

This is the machine's own founding lesson pointed at its front door: **a number with
no provenance outlives a wrong sentence** (#177), because nobody re-derives it. An
Oracle card is the first thing the interview is built on, so an unsourced statistic
entering here is laundered by every honest stage downstream — and the origin gate
cannot catch it, because by then the number is something Sean said in an interview,
having been told by the card that it was true.

**The rule is not about YouTube.** Run 4's web leg returned the same hazard in a
different wrapper — *"Devstral 2 hit 72.2%," "Kimi K2.6 hit 87/100"* — from SEO
listicles. Low provenance is the property that matters, not the platform: a figure
whose source cannot be reached and checked *from the item itself*. That covers
transcripts, roundup blogs, and any post citing an unnamed survey. Statistics get
sourced independently or they do not appear.

A person's account of what happened to them is not a statistic and is not covered by
this. "We killed it after six months" is quotable; "68% of teams kill it" is not.

**Two ways the report claims coverage it did not deliver.** Both are silent, both
appear in the stats block as ordinary success, and neither is visible unless you look
for it on purpose. The stats block is a record of what the engine *did*, not of what
it *answered*.

**The YouTube date trap is query-dependent, and it bites on exactly the queries the
Oracle is built to run.** Run 2, on a well-populated topic: *"Found 4 videos within
date range"*, no override. Run 1, niche: *"19 videos (2 within date range, keeping
all)"* — and it kept all nineteen. Run 3, the most niche of the three: **zero of six
inside the window**, spanning 2025-01-27 to 2026-06-10, the top result nineteen
months outside a scan labelled "last 30 days" and ranked first because it has two
million views.

So a **niche** query starves the window and the engine widens silently, while a
crowded one does not — and the starvation is not partial, it can be total. Niche is
where the good cards are. **Check the publish date on every YouTube item before it
reaches a card**, and treat a YouTube-only finding on a niche query as unsourced
until the date is confirmed.

**The engine can silently substitute a degraded query and report the answers as if
they were yours.** Run 4's X leg hit a JSON parse error and retried on its own:

```
[Bird] Bird error: Invalid JSON response: Unterminated string ...
[Bird] 0 results for 'local open source models actually', retrying with 'local open'
```

All four X results answered **`local open`** — a two-word fragment that means almost
nothing — and the report presented them under the original question. That is why they
were generic and all dated the same day. Nothing in the stats block says so; it reads
"X: 4 posts."

**Read the engine's own stderr, not just its results.** The retry lines, the
relevance warnings (*"All results below relevance 0.3, keeping top 3"*), and the
window notes are where the engine admits what it actually ran. A source that answered
a different question is worse than a source that returned nothing, because nothing is
legible and a wrong answer is not.

**YouTube also collapses to category, which is the banned shape re-entering by a
route the phrasing rules cannot block.** Run 3's query parsed GENERAL and YouTube
answered with "Best AI Tools for Writing Fiction," "The Perfect AI Writing System,"
"Learn to Prompt Like a PRO." The RECOMMENDATIONS report was banned at the query
layer; YouTube's own SEO serves it anyway, because tool roundups are what the
platform rewards. Nothing in the phrasing table prevents this — only reading the
titles does.

### Read at comment depth

The post's thesis is what everyone reacts to and therefore what everyone has already
written. The sharp dissent is three replies down. Reddit comments are live in this
setup (the ScrapeCreators key is configured), and the skill's own docs claim
top-voted replies beat the posts.

**Measured, first run:** they do. The card that came out of it was built on a
123-upvote comment; the post it sat under was a news headline anyone could have
found. The post gave the event, the comment gave the thesis.

Related: **recency is not the signal — unanswered is.** A three-week-old thread with
four hundred comments and nothing written about it beats yesterday's news with forty
takes on it already.

**Comment-to-upvote inversion is the mechanical form of that**, and it is checkable
from the stats block without reading a word. A thread at **0–3 points with 17–29
comments** is not a thread nobody cared about; it is an argument in progress. Upvotes
mean *this is settled and I agree*. Comments mean *it isn't, and here's mine*.

Run 2 was almost entirely made of them — 1 point and 29 comments, 2 and 19, 0 and 22,
3 and 17 — and one thread carried the probe's own query as its title, drawing 19
answers and 2 upvotes. That subreddit is arguing about what breaks and nobody has
published a ledger, which is the whole card. Scan for the inversion first; it finds
unoccupied ground faster than reading does.

**5. Score and deck — one pass, two decks.** Everything from steps 1 to 4 goes into
**one pile**: sweep items, news items, anchor hits, frame angles. Score each once. A
candidate with long-form shape goes to the piece deck on the six signals; a candidate
that lands in one sentence goes to the post deck on the five; a candidate may sit in
both, scored separately, and **nothing is ranked across decks**. A card banks only if
it is dead on both bars.

Frame angles get **no lane of their own**. A merged ranking is exactly the shape the
Spine veto was built to stop, and the only way a frame angle cannot launder past
Spine is if it has nowhere else to go. It enters the pile like everything else and
faces the same veto.

Roughly ten cards across the two decks. Label each by source — `internal`,
`external`, `news`, `frame` — and say the split out loud. If news or frames are
crowding the pile, that is a fact he should see rather than a shape he has to
reverse-engineer; the majority of the deck stays experiment cards, and a deck that
is mostly news cards has drifted.

**6. He picks.** Never pick for him. A piece card and a post card may be the same
subject — one interview, then a fresh subagent per artifact, drafted in the order
the clocks close (#227, rulings 14–16). The rest bank.

## The listening report

The news lane's other half (#227 ruling 21, built on #239): a prose brief of the
week's AI news that Sean absorbs by ear. He absorbs best by listening (ruling 6),
and the brief exists so a news pick is made on the news itself rather than on a
headline in a card. It is machine-written, and that is the hazard it is built
around: a synthesis he listens to becomes his interview material, the origin gate
passes it because he really said the words, and a wrong figure ships in his voice.
**Provenance is therefore mandatory and mechanical** (ruling 8).

The shape is fixed by what `markdown_to_speech.py` actually does — headings are
spoken as section titles after a short pause, links collapse to their text, tables
are read row by row with commas, a code fence is spoken once as "Code block
omitted", bullets flatten into run-on prose:

- **1,200 to 1,500 words, hard cap 2,000; at most six items.** Kokoro reads at
  roughly 150 words a minute, so that is eight to thirteen minutes. An item that
  needs more than 250 words is a piece, not a brief: it gets a card, not more
  narration.
- **One `##` per item, then exactly three paragraphs**: what happened, with the
  source named *in the sentence*; what it can now do that it could not last week;
  the one or two experiment cards it spawned, one line each. No tables, no code in
  the body, no sub-headings, no list longer than three.
- **Spoken-safe by construction**: dates and large numbers are written as words
  ("twenty twenty-six", "sixty-two percent"); short numerals in names ("GLM 5.3")
  survive because Kokoro reads them correctly.
- **A figure is spoken only with a tier A or B source behind it. A figure from a
  tier C or D source is dropped from the narration outright** — "quote a person,
  never a number" extended to this surface. Percentages, sums of money,
  magnitudes and multipliers count as figures; a count under a hundred does not.
- **The Sources list sits at the foot inside a code fence**, one line per source,
  numbered by item (`2. title — https://…`; an item may have several). Readable
  in the markdown, spoken once as "Code block omitted" instead of six URLs read
  aloud.

Commands, in order:

```bash
NL=.claude/skills/content-oracle/news_lane.py
python3 $NL template --date <sunday> --items 6                          # skeleton → oracle-reports/<date>-oracle-report.md
# write the report from the pull index, then:
python3 $NL check   --report <report> --gists <gists> --pull <pull>    # lint + tier audit; exit 2 on any failure
python3 $NL preview --report <report>                                   # exactly what the flattener will speak
python3 $NL render  --report <report> --gists <gists> --pull <pull>    # checks again, then MP3 → vault/90_system/audio/
```

`check` is the gate: it lints the shape above, tier-audits every source in the
fence through `agents-sdk/scripts/audit_dr_citations.py` (extended on #239 to read
plain URLs, not only Gemini's redirect list), fails any item that carries a figure
with no tier A/B source, and verifies the gists. `render` refuses to run until it
is clean. The report lives at `creative-studio/content-machine/oracle-reports/`,
git-ignored with a canary test, because it names his spikes and the cards; the MP3
goes to `vault/90_system/audio/`, already ignored.

**Measured on the first render (2026-09-03, six items, first real use of the pipeline):**
1,257 words rendered to 7 minutes 59 seconds of audio, which is **158 words a minute**
at speed 1.0 — so the 2,000-word cap lands at about 12 minutes 40 seconds, inside the
13-minute ceiling. 28 segments, 61 seconds of wall clock on the MacBook Pro, $0. The
flattener did exactly what ruling 21 predicted: the H1 and each `##` were spoken as
titles after the pause, the Sources fence became one "Code block omitted", and
nothing in the body was mangled — because the shape was written for it (no tables,
no lists, no links, numbers as words). Spelled-out resolutions ("ten-eighty", "four
K") and model names with dots ("GLM 5.3") read correctly. The one thing to watch is
the template, not the flattener: an item that drifts past three paragraphs reads as
run-on, and `check` catches that before the render does.

Declined on #227: a three-minute headline brief (loses the absorb-by-listening
point) and twenty-to-thirty-minute full read-throughs (the tier audit cannot strip
figures from someone else's prose without rewriting it).

## Card format

```
SPIKE <n> — <title>
Deck: piece | post
Source: internal:<git|issue|daily|sidecar|fleet|tickets> | external:<where> | news:<where> | frame:<lens id>
Evidence: <sha | issue # | path | URL>                              ← done-thing cards
Evidence: <provocation — the news URL or the sweep item> · Status: unrun   ← experiment cards
Query: <external cards only — the shape and the exact query that surfaced it>
Signals: POV <n> · Story <n> · Emotion <n> · Framework <n> · Depth <n> · Spine <n> = <total>/18      ← piece deck
Signals: Angle <n> · Clock <n> · Fit <n> · Image <n> · Reply-hook <n> = <total>/15 · Spine-X: pass   ← post deck
Cuts to LinkedIn: yes | no
The moment | The experiment: <one or two lines — what happened, or "do this, expect that">
Why it's a piece | Why it posts: <the take or the shape it would carry>
Lane / medium: <suggested contract under contracts/>
Lens: <which interview lens — and what the interview has to go get>
```

Field rules:

- `Deck:` says which bar the `Signals:` line was scored on. A subject in both decks
  is two cards.
- `Source: frame:<lens id>` is how a frame-sourced card carries its lens — the same
  way an external card carries its query shape on `Query:`. The bank reads it (see
  Probation). `Lens:` stays the **interview** lens, because the interview engine
  requires one on every card (#231) and a field carrying two meanings would break
  both the engine and the record.
- `Status: unrun` is mandatory on every experiment card and forbidden on a
  done-thing card. It is the line that says "nothing here is a claim yet."
- `Cuts to LinkedIn:` is a tag. It never appears in a sum.

A picked card becomes the TOPIC CARD at stage 1. It is a proposal, not a brief: he
can overrule the lane, the medium, and the angle, and the interview outranks all of
it. A picked *experiment* card becomes a TOPIC CARD only after he has run the
experiment — the interview is about what happened, and until then there is nothing
to interview about.

## The ideas bank

Unused cards append to `creative-studio/content-machine/ideas-bank.md` — the private
brain, git-ignored, beside the corpus and the ledger.

Lieberman banks to a Notion database. Sean's goes to the private brain rather than a
vault note, **because the cards quote his commits, dailies and sidecars, and
`vault/20_projects/substack-studio/` is a tracked public path.** An ideas note there
would publish the sweep's private material a card at a time. `vault/daily/` was
itself pulled into the private layer on 2026-08-26; the bank follows it.

Format is the machine's one convention, so there is a single thing to remember:

```markdown
## <YYYY-MM-DD> — oracle run
<card, verbatim, exactly as decked>
```

**Banked is not dead.** Before scoring a fresh sweep, read the bank: a spike that
banked three weeks running because it was thin is a different object once this
week's work gives it an ending. Re-deck it rather than re-deriving it.

**Never delete a banked card.** Same reason the lessons ledger keeps rejections — a
deleted card gets re-proposed forever.

## Probation

**On-demand only. The Oracle has no schedule and does not get one by default (L7).**

It graduates to a scheduled agent after roughly six proven manual weeks, on the
evidence of those weeks, and not before. Test before committing.

- **Run day: Sunday. Week 1 = 2026-08-30.** Graduation reviewed after 2026-10-04.
- A **weekly email reminder** fires Sunday 08:00 so a probation week cannot quietly
  get skipped — `agents-sdk/scripts/oracle_reminder.py`, on launchd.

### Week 1 failed, and the mechanism changed mid-probation on purpose

**Sean denied every card in the first real deck** (2026-08-30). His reason: it pulled
boring topics out of the week's codebase work, and *"me tweaking things in my codebase
isn't always going to be a story."* The cause was structural rather than a scoring miss
— an external hit was defined as timeliness attached to something he had already done,
and the sweep supplied the nouns for every external query, so **the Oracle could not
propose a subject he had not already worked on.** A quiet week produced boring nouns,
boring queries, and a deck that could only anchor back to them.

**The clock does not reset. Probation still runs to 2026-10-04** (Sean's ruling,
2026-09-02). The change is not an escape from the probation record, it is the record:
*"It would have definitely failed the probation if we kept going down the path we were
on... Week 1 was a failure, so we made the change immediately to see if it can produce
better results rather than allowing it to continue producing failures."*

Read the graduation evidence accordingly. Weeks 2 onward test a **different mechanism**
than week 1 did, and the honest question at graduation is whether the changed Oracle
earns a schedule — not whether a six-week average clears a bar. Week 1 is kept in the
record as the failure that caused the change, never averaged away. Changes ruled in
that session are tracked at
[#227](https://github.com/seanwinslow28/code-brain/issues/227); the rebuild shipped
on #238 (the card bar, the frame stage, two decks) and #239 (the news lane, the
listening report). **Week 2, 2026-09-06, is the first run of the changed mechanism.**
The Oracle's reminder fires on the Mac Mini, and a ruling written here reaches that
machine only when it pulls — verify the pull before the Sunday run, never assume it.

The reminder is deliberately the dumbest thing that works: no model, no SDK, no
agent, no repo reads. It sends one fixed email. An Oracle that reached the inbox on
a schedule would have smuggled itself past its own probation, and the reminder would
have become the thing it was supposed to be testing.

Record each run in the bank (a run with zero picks still happened). The graduation
decision reads that record, and it is reading for two things:

- **Did he pick anything?** Six weeks of decks he never picked from is the answer,
  and the answer is no schedule.
- **Which query shapes produced picked cards?** Every external card carries the
  exact query that surfaced it, so the bank accumulates evidence about the shapes
  rather than opinion. If recantation probes produce every pick and silence probes
  produce none in six weeks, that is a finding worth more than the schedule
  decision itself — it is how the query table above gets corrected by use instead
  of by argument.
- **Which lenses produced picked cards?** Every frame-sourced card carries its lens
  on `Source: frame:<id>`, and every run records the four lenses it dispatched
  (the script prints a bank-record stub), so the bank accumulates the same evidence
  about lenses that it accumulates about query shapes. A lens earns or loses its
  slot on that evidence, by Sean's ruling. A run where no frame angle was picked is
  a finding about the deck, not a reason to skip the stage.
- **Did a news item become a card?** Same record, third column. A news card carries
  `Source: news:<where>` and its provocation URL on `Evidence:`, so the bank reads
  whether the lane earns picks the way it reads query shapes and lenses — and
  whether he listened to the report at all, which is the week-2 question on #239.

**Watch item: are the six signals separating?** Both pre-probation probes returned a
best card at **17 of 18**. If every card tops out, the ranking is decorative and the
scale is too generous at the top. The likely innocent explanation is that a probe
produces one best card while a real run decks ten, and ten will spread — so this is
recorded to be checked against real decks, not corrected in advance. If week 3's deck
is still nine cards clustered at 16–18, the scale is wrong, and #162's lesson applies:
the ratings are load-bearing, so the fix is a move rated one step too hot, not a new
tier.
