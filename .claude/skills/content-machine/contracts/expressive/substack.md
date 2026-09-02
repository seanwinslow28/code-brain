# Medium contract: Substack (Expressive lane)

**Status: thin.** Written for the walking skeleton ([#163](https://github.com/seanwinslow28/code-brain/issues/163)).
It hardens in wave 1 once real posts have run through it. Where it is silent, the publication's own
law governs — do not invent a rule here to fill a gap.

## Governing documents, in precedence order

1. The publication's `SOUL.md` — the masthead. Wins over everything.
2. The publication's `POSITIONING-AND-EDITORIAL-SPEC.md` — strategy.
3. The publication's `CLAUDE.md` — standing house law (voice chain, no em dashes, anti-hype, value
   gate, privacy).
4. [`LANE.md`](LANE.md) — Expressive-lane law, inherited by every contract in this lane (the
   first-screen test, the reply-hook memo).
5. This contract — what the machine does differently because the medium is Substack. It may narrow
   anything in `LANE.md`; it may not delete it.

For Pencil & Prompt those live under `vault/20_projects/substack-studio/`. Read them before the
interview. A machine that reads the house rules after drafting has already wasted the interview.

## What a post has to deliver

- **A real artifact.** Something that actually happened or actually ran, captured. Never "here's how
  you could." No artifact, no post — the gate blocks and the piece waits.
- **A verdict or a lesson.** The spine series ends in a tested verdict. The story series ends in a
  navigation lesson: what the author does differently now.
- **Transfer.** The reader can do something with it that they couldn't before they read it.
- **The ask lands sideways.** Never a closing pitch, never "I need", never "you can hire me".

## First screen

The surface the [lane's first-screen test](LANE.md#the-first-screen-test) runs against. Substack has
two and the piece has to clear both, because most readers meet it in the first one:

- **In the inbox.** The title as subject line, the subtitle as preview text, and roughly the first
  two or three lines of body before the reader decides to read or archive. No image has loaded yet
  in most clients. This is the harder screen and it is the one to write for.
- **On the web and in the app.** Title, subtitle, hero image, and the first paragraph above the
  fold.

**Reply surface: yes.** Post comments, plus replies to the email, which arrive in Sean's inbox as
mail. The [reply-hook memo](LANE.md#the-reply-hook-memo-advisory-never-a-gate) ships with every
piece.

## Shape

Lead with the captured thing, never the abstract premise. A universal observation as an opening line
is the one shape the publication exists against.

Section last lines carry the same pressure as the closer. A deflation or an appalling pivot, never a
summary. The closer is the strongest line in the piece.

Length is bounded by padding, not word count: long enough to tell it, then stop.

## Licensed moves

**Licensing is not this contract's call.** [`move-licensing.md`](../move-licensing.md) is the shared
matrix ([#162](https://github.com/seanwinslow28/code-brain/issues/162)); this contract inherits it and
may narrow it, never widen it. Substack's budget is **heat 3, room 4** — the widest in the set, which
is right: it is the medium the roster was calibrated on. **34 of 36 moves licensed.**

The two it does not get:

- **Equation / Formula Defamiliarizer** — banned, short-form only.
- **Screenwriting Cut-To** — **conditional**. The juxtaposition is licensed; the literal screenplay
  notation is not. Write the hard turn in prose, never with `HARD CUT TO:` or a bare italic *cut to*.

**References are rationed: two to three woven references per piece, maximum, most paragraphs zero.**
Sourced from `reference-universe.md` or the piece's own subject. Never invented. A reference that
could be swapped for a different one and dropped anywhere is garnish — cut it.

## Ratified lessons from shipped pieces

Routed here by the lessons loop. Reasons live in the gitignored ledger.

- **The navigation lesson has to show real capability, not a routine.** "I check it and I ask Claude
  to check it too" is a boring cap on a Raising Agents episode. Name the actual practice: what gets
  evaluated, what gets traced, what watches what. The lesson is where the reader decides whether the
  author knows what he is doing.
- **Introduce an unfamiliar tool the first time it appears.** Naming one of Sean's own skills bare
  ("the creative-partner skill") assumes a reader who already knows it. A possessive does the
  introduction at zero cost: *"my /creative-partner skill"*. The bar is recognition, not obscurity:
  *"It's not like the viral /last30days skill that a lot of people in this space would immediately
  recognize."* (Run #2, 2026-08-28.)
- **Closer register for this series: honest realist, wit, a dash of professionalism.** The ending
  admits the breakage is inevitable and shows the thing that keeps it survivable. It never resolves
  into a tidy win.

## Hard mechanics

Inherited from `writing-voice-modes` G1–G5, restated because Substack drafts break them most:

- No em dashes. Anywhere. And no colon substituted in when one is dropped.
- Contract everything.
- Colons and semicolons rare or absent.
- No word that isn't working.
- Adjacent beats must turn. If "and then" fits better than "but" or "therefore", the beat is dead.

## Gates, in order

**Post-draft and advisory as of 2026-08-31** (the rules-off re-scope: nothing below is a drafting-time constraint any more). Order: **origin (claims tier) → do-not-promote + coined-lines sweep → humanity scrub → critique / analyzer**.
The **structure read** also runs here, post-draft and advisory, rather than as a stage the draft must pass through first.

**The value gate is the exception, and it runs BEFORE the interview** (corrected 2026-09-02, [#224](https://github.com/seanwinslow28/code-brain/issues/224)). This line previously swept it in with the rest. The 2026-08-31 re-scope retired the *drafting* chain to post-draft advisory; `substack-value-engine` was never a drafting stage, it is the publication's pre-writing hard block (substack-studio CLAUDE.md §3: *"Before a post is worth writing... If there is no real artifact, the gate blocks and the angle waits until Sean has done the work."*). A value gate run post-draft is not a gate — the interview and the draft have already been paid for by the time it answers. It clears at stage 1, and the Oracle's card bar is the same test one stage earlier still ([#227](https://github.com/seanwinslow28/code-brain/issues/227)).

The **first-screen test** runs post-draft on the assembled draft (see LANE.md; the shape gate that used to host it is retired). A failure returns as a
reorder, never as new material (see `LANE.md`). The **reply-hook memo** is not a gate at all; it is
written after do-not-promote and travels with the ship packet.

The origin check runs `gates/origin_check.py` (mechanical layer) plus a reading pass for
recombination, which the mechanical layer is blind to. Expressive lane advises and never blocks.

The do-not-promote sweep runs `gates/coined_lines.py` alongside the suppressed-topic check: a coined
line lives in exactly one artifact and is never recycled here.

## Delivery

Frontmatter follows the publication's existing convention (series, title, status, itch,
solution_artifact, transfer, hero_image, open_items). Drafts live in the publication's own folder,
one directory per piece. The machine never publishes; it hands over a ship packet.

## What this contract does not own

Story order (`storytelling-architecture`), whether the piece is worth writing
(`substack-value-engine`), sentences (`writing-voice-modes`), or the publishing decision (the
author).
