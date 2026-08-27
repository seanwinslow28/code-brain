---
name: content-oracle
description: Stage 0 of the content machine. Sweeps the author's own systems (git, dailies, closed issues, partner-session sidecars, fleet manifests) plus a last30days external scan, scores candidates on six spike signals, and emits ~10 decision cards so a writing session starts from a concrete idea instead of a blank page. Unused cards bank rather than evaporate. Use when asked "what should I write about", "find me content spikes", "what's worth writing this week", or to "run the content oracle". NOT the separate `the-oracle` capture/reminders project at ~/Code-Brain/the-oracle/ — a bare "run the oracle" is ambiguous between the two, so ask which one. On-demand only: it is on probation and has no schedule.
---

# Content Oracle

The Oracle ends "what do I write about." It does not write anything.

It reads what the author actually did in the last seven days, ranks what has a
piece in it, and hands him a short deck to pick from. Stage 1 of
[`content-machine`](../content-machine/SKILL.md) takes it from there.

Build ticket: [GitHub #169](https://github.com/seanwinslow28/code-brain/issues/169).
Pattern source: Alex Lieberman's content machine (the five signals below are his,
transcribed verbatim; the sixth is Sean's addition).

## The evidence rule

**Every card points at one artifact. A card with no evidence pointer is an invention.**

This is the origin law (`content-machine`'s L2) applied one stage earlier. The
machine exists so drafts come from things the author said; an Oracle that
synthesized plausible-sounding spikes out of metadata would poison the well at the
source, and the origin gate downstream cannot catch it — by the time the interview
runs, the fake premise is what he is being interviewed *about*.

So: a commit sha, a `vault/daily/<date>.md`, an issue number, a sidecar filename, a
URL. If the sweep did not surface it, it is not a card.

## The six signals

Five are Lieberman's, from the founders transcript — the Oracle "hunts for spikes,
and spikes are basically how much point of view is there, how much story potential
is there, how much emotional intensity is there, how much lesson or framework is
there, and how much depth is there." The sixth is the L7 amendment.

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

## Interviewability

Not a signal — a gate on the card's usefulness. The machine can only write from what
he says, so a spike he cannot be interviewed about is worth nothing however it
scores. Every card therefore names its lens and what the interview has to go get. If
that field cannot be filled, the card is not ready and it banks.

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

**2. External scan** — the `last30days` skill, every run (Sean's ruling, 2026-08-26).

An external hit is **not a topic**. It is timeliness attached to something he
actually did, or a reaction candidate that must clear Spine on its own merits. The
question to ask of every external item is "which of his internal spikes does this
give a reason to publish *this week*" — not "what's trending."

### The sweep supplies the nouns

**Run the internal sweep first, then derive every external query from it.** The
usual order — scan the zeitgeist, then ask whether Sean has anything to say — is
what produces detours, and it is why Spine needed a veto. Inverting it makes the
editorial law mechanical: a query built from his own week cannot return a card about
someone else's.

Pick the **two** internal spikes where the take already exists but the *reason to
publish now* does not — high Story and Depth, thin on nothing else. Those are the
ones an external anchor can actually improve. Two queries, not five: each
`last30days` run takes 2–8 minutes, and a deck is not worth forty.

### Query the friction, never the category

`last30days` branches on how the question is phrased, so phrasing decides the report
you get before any source is touched:

| Never ask | Why |
|---|---|
| "best X", "top X", "what X should I use" | Parses as RECOMMENDATIONS → a list of tools. Pulls vendor SEO and affiliate content. This is #170's documented failure reproduced on a different engine. |
| "X vs Y" | Parses as COMPARISON → a head-to-head buyer's guide. Answers a purchasing question, not a writer's. (Fine to run deliberately outside the Oracle.) |
| "latest on X", "X news" | Parses as NEWS → what everyone else already read, and therefore already wrote about. |

Everything below parses as GENERAL, which is the mode that returns discussion rather
than a product roundup.

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

**3. Score and deck.** Read the sweep, apply the six signals, emit roughly ten cards
ranked by total. Label each internal or external, and say the split out loud —
if external is crowding the deck, that is a fact he should see rather than a shape
he has to reverse-engineer.

**4. He picks one.** Never pick for him. The rest bank.

## Card format

```
SPIKE <n> — <title>
Source: internal:<git|issue|daily|sidecar|fleet|tickets> | external:<where>
Evidence: <sha | issue # | path | URL>
Query: <external cards only — the shape and the exact query that surfaced it>
Signals: POV <n> · Story <n> · Emotion <n> · Framework <n> · Depth <n> · Spine <n> = <total>/18
The moment: <the specific thing that happened, one or two lines>
Why it's a piece: <the take or the shape it would carry>
Lane / medium: <suggested contract under contracts/>
Lens: <which interview lens — and what the interview has to go get>
```

A picked card becomes the TOPIC CARD at stage 1. It is a proposal, not a brief: he
can overrule the lane, the medium, and the angle, and the interview outranks all of
it.

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

**Watch item: are the six signals separating?** Both pre-probation probes returned a
best card at **17 of 18**. If every card tops out, the ranking is decorative and the
scale is too generous at the top. The likely innocent explanation is that a probe
produces one best card while a real run decks ten, and ten will spread — so this is
recorded to be checked against real decks, not corrected in advance. If week 3's deck
is still nine cards clustered at 16–18, the scale is wrong, and #162's lesson applies:
the ratings are load-bearing, so the fix is a move rated one step too hot, not a new
tier.
