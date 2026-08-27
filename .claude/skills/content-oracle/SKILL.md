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

| Shape | Template | What it's for |
|---|---|---|
| **Recantation** | `people switching back from {thing}` · `gave up on {thing}` | The strongest single shape. Nobody writes a recantation unless the cost was real, so the arc — adopted, hurt, left — arrives already a story. Scores high on Story and Emotion before you read a word. |
| **Friction** | `{thing} problems in production` · `what breaks with {thing}` | Sorts practitioners from vendors. "In production" and "six months in" are the phrases marketing copy cannot fake. |
| **Contested claim** | `is {claim} actually true` · `{claim} disagreement` | Finds the fault line rather than the consensus. The best of these is a claim repeated everywhere that **nobody has measured** — which is Sean's opening, because he has a running fleet with cost caps, failure manifests and six months of receipts. A claim he can settle with evidence he already owns is worth more than any trend. |
| **Silence probe** | the specific mechanism, not its category — `origin fidelity LLM drafting`, not `AI writing tools` | Deliberately aimed where results should be thin. See below. |

### Thin results are a finding, not a failed query

**Do not broaden a query that returns little.** The reflex — no hits, try a wider
term — walks straight back onto crowded ground, which is the opposite of what the
scan is for. An unoccupied space with real internal material behind it is the
strongest card the Oracle can deck: he has the story, and nobody has the coverage.

Say so on the card. "Four threads in thirty days, no write-up" is evidence, and it
belongs in *Why it's a piece*.

### Read at comment depth

The post's thesis is what everyone reacts to and therefore what everyone has already
written. The sharp dissent is three replies down. Reddit comments are live in this
setup (the ScrapeCreators key is configured), and the skill's own docs are blunt
that the top-voted replies beat the posts.

Related: **recency is not the signal — unanswered is.** A three-week-old thread with
four hundred comments and nothing written about it beats yesterday's news with forty
takes on it already.

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
