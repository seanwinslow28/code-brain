# Continuation prompt — Content Oracle, probation week 2 (2026-09-06)

Paste the block below into a fresh session on the **MacBook Pro**. Written 2026-09-06 at the close
of the [#246](https://github.com/seanwinslow28/code-brain/issues/246) session.

---

Run the Content Oracle's **week-2 probation run**. Today is Sunday 2026-09-06.

Load the `content-oracle` skill and follow it. This prompt is orientation, not a substitute for the
skill — where the two differ, the skill wins.

## Why this run matters more than a normal one

Week 1 (2026-08-30) produced a deck Sean **denied in full**. The cause was structural, not taste: the
internal sweep supplied every noun, so the Oracle could only ever propose subjects he had already
worked on. [#227](https://github.com/seanwinslow28/code-brain/issues/227) ruled the fix and it shipped
as two builds — [#238](https://github.com/seanwinslow28/code-brain/issues/238) (the frame stage, the
card bar flipped from *what did I do that's a story* to *what should I go find out*, two decks) and
[#239](https://github.com/seanwinslow28/code-brain/issues/239) (the news lane, the listening report).

**This is the first run of the changed mechanism.** Graduation on 2026-10-04 judges the changed
Oracle, not a six-week average — week 1 stays in the record as the failure that caused the change and
is never averaged away. **#238 and #239 both stay open until this run's record lands**, so posting
that record is part of the job, not a nicety.

## Run it on this machine, and know why

Three of the Oracle's inputs live **outside the repo** and git cannot carry them, so a Mac Mini run
would report a clean sweep over sources it never saw:

- partner-session sidecars at `~/.creative-harness/partner-sessions/` (one of the sweep's six sources)
- `last30days` credentials at `~/.config/last30days/.env`
- the private brain (`ideas-bank.md`, corpus, watchlist) — ruled canonical on the MacBook Pro 2026-09-03

The vault side is fine: the Mini's scheduled agents push `vault/health/`, so pull before starting and
the fleet leg sees its overnight work. The dependency runs Mini → MBP through git, never the reverse.

**The Oracle has no launchd stanza on either machine and must not get one.** L7 probation is
on-demand only. `com.sean.oracle-reminder` is a fixed email with no repo reads — deliberately the
dumbest thing that works, so an Oracle arriving on a schedule could not smuggle itself past its own
probation. Separately, `com.sean.the-oracle.*` belongs to Sean's **other** `the-oracle` project; it is
not this.

## The stages

```bash
python3 .claude/skills/content-oracle/sweep.py --days 7
python3 .claude/skills/content-oracle/news_lane.py pull --date 2026-09-06
python3 .claude/skills/content-oracle/news_lane.py gists --check <gists.json> --pull <pull.md>
python3 .claude/skills/content-oracle/frame_stage.py --summary <path> --gists <path> [--dry-run]
```

Order: internal sweep → news pull → read the index and write two-line gists → `gists --check` →
frame stage → score once → two decks. Read `ideas-bank.md` **before** scoring: a thin spike from three
weeks ago may have an ending now.

## Standing rules a fresh session gets wrong

- **Spine is a veto, not an addend.** With a summed score, external items fill the deck on quiet weeks,
  and a high-scoring detour is the most dangerous card in the deck because it is the one he will pick.
- **Every card points at one artifact.** This is the origin law one stage upstream of where the origin
  gate can see, because a synthesized spike becomes the thing he is later interviewed about. An
  experiment card proposes a subject and an experiment, never a claim about what he did; its evidence
  is its provocation plus `Status: unrun`.
- **Interviewability is a usability gate, not a signal.** A card that cannot name what the interview
  must go get **banks** instead of decking.
- **Banned query shapes:** "best X" (vendor SEO), "X vs Y" (a buyer's guide), "latest on X" (what
  everyone already wrote) — except inside `news_lane.py pull`, which is NEWS-shaped on purpose and is
  the one allowed place. Use the four GENERAL-parsing shapes; the strongest is the **recantation
  probe**, because nobody writes a recantation unless the cost was real. **Two queries per run**,
  drawn from spikes where the take exists but the reason to publish now does not.
- **Thin results are a finding, not a failed query.** Broadening walks back onto crowded ground. An
  unoccupied space with real internal material is the strongest card the Oracle can deck.
- **External cards carry the query that surfaced them**, so probation measures which shapes earn picks.
- **L4:** LinkedIn is a card-time credibility tag, never a rank input.
- **L8:** ranking *candidates* is legal at any count; producing a *score* on drafts is banned at any
  count. The two decks are "worth a piece" (five long-form signals) and "worth posting" (angle / clock
  / fit / image / reply-hook, with engagement questions scoring 0 and image scoring only artifacts
  that already exist).
- A card's **lens** field copies the medium contract; it does not choose
  ([#231](https://github.com/seanwinslow28/code-brain/issues/231)).

## Do not

- **Do not wire the news lane's X leg.** It is [#252](https://github.com/seanwinslow28/code-brain/issues/252),
  deliberately deferred until after graduation so week 2 measures **one** changed mechanism rather than
  two. (Its stated cost premise is wrong — the X leg resolves to Bird first, free — and it is still
  deferred, on measurement grounds rather than cost.)
- **Do not give the generators tools.** Freshness arrives through the payload: the news pull runs first
  and hands each generator *what happened + what it can now do*. Tools would reintroduce vendor SEO,
  convergence, and sidecar exposure.
- **Do not paste anything from the private brain** — sidecars, corpus, dailies, transcripts,
  `ideas-bank.md` — into a tracked file, an issue, or a commit message. The repo is public. The frame
  stage's payload is stripped and the script refuses to dispatch if it carries a path, an email, a sha,
  or a line lifted verbatim.

## An open question this run can help answer

The map carries fog on **whether experiment cards need an "unrun" reading of Story and Emotion**. The
#238 dry run seated six frame-sourced experiment cards at 16 / 15 / 14 / 13 / 12 / 12 — they score low
on Story and Emotion by construction, because nothing has happened yet. A mixed deck may therefore
always prefer done things, which would quietly undo #227's ruling 4. Whether that is a scale fix (a
card rated one step too low, the #162 lesson) or just a supply fact needs **real** week-2 and week-3
decks with both card shapes in the pile. Note what you see; do not fix it on one run.

## Record it

Record the run in the ideas bank **even with zero picks** — a run with no picks still happened, and
graduation reads that record for two things: did he pick anything, and which query shapes produced
picked cards. The bank now also records **which lenses** earned picks. Then post the run's record to
**#238 and #239**, which is what closes them.

## Context from the session that wrote this

[#246](https://github.com/seanwinslow28/code-brain/issues/246) closed last night: X's standalone route
ran end to end under the Observer lens and produced a hand-rewritten final, not yet posted — Sean's
call is to start posting once there is a body of them. Two things from it that touch Oracle output:
a live hypothesis that **the comic register may belong to X's reactive route rather than the standalone
one** (settled by [#255](https://github.com/seanwinslow28/code-brain/issues/255), not by this run), and
[#257](https://github.com/seanwinslow28/code-brain/issues/257), which now blocks #233.
