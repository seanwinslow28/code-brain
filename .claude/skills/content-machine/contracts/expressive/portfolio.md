# Medium contract: Portfolio write-up (Expressive lane)

Wave 2 ([#171](https://github.com/seanwinslow28/code-brain/issues/171)).

**Lens: project write-up — Technical Peer → Cold Reader. About page — Stakes → Cold Reader.** The
About assignment is ruled in [#226](https://github.com/seanwinslow28/code-brain/issues/226) and is
deliberately **not** Recruiter: that lens runs the facts-only form of the law, which is
Professional-lane machinery, and importing it into an Expressive page produces the **resume bullet**
this contract lists as a negative specimen. A project write-up is the other case — its five beats
each carry a verbatim `number` and the `date` it was measured, which is the Technical Peer's
transcript. Cold Reader closes both, because every surface on the site is dense with internal nouns:
fleet, Driftgate, Groundwork, ontology.

**Status: unproven.** Neither form has run through it. The About page is the wave-1 run
([#234](https://github.com/seanwinslow28/code-brain/issues/234)), and the section of this contract
that governs it lands with that ticket.

## Governing documents, in precedence order

1. **The site's own data contract** — `seanwinslow.com/src/data/projects.ts` and the tests in
   `seanwinslow.com/tests/beats.test.ts`. These are executable and they win. A write-up that does
   not typecheck is not a write-up.
2. [`LANE.md`](LANE.md) — Expressive-lane law (the first-screen test, the outside-fact rule, the
   reply-hook memo).
3. [`../move-licensing.md`](../move-licensing.md) — the shared matrix.
4. This contract.

## What a portfolio write-up actually is

Not an essay. The site does not have a prose surface for a project. A write-up is a set of **typed
fields**, and the form is the constraint:

| Field | What it is | Bound |
|---|---|---|
| `description` | One sentence, under the title, on the work index and the project page. | One sentence. |
| Five `beats` | Fixed kicker arc: **situation → fork → catch → risk → changed**. | Each carries a verbatim `number`, the `date` it was measured, and `support`. |
| `support` | The prose. | **≤ 30 words, at most two sentences.** Machine-enforced. |
| `system` | The closing panel, "6 · The system". Same contract minus the kicker. | Same 30-word cap. |
| `visual.alt` | Alt text on every card. | Required, and it carries the figures in the art. |

**The cap wins; the essay goes in the vault.** That is Sean's 2026-08-24 call, written into the test
file, and it is the single most useful thing to know before drafting: there is no room to build to a
point. Every panel arrives already at it.

## Licensed moves: twenty, minus what the form physically defeats

Budget heat 2, room 2. Twenty of thirty-six:

**Funniest Word Last** · **Unsignposted Pivot** · **Tool-as-Character** · **Expectation / Instead** ·
**Then / Now Narrator** · **Flat Collision** · **Short Declarative Drop** · **Hard Cut / Deflation** ·
**Rule of Three + Emotional Pivot** · **Pop Culture Anchoring** · **Blunt-Literal Description** ·
**Reader-Dismissal** · **Equation / Formula Defamiliarizer** · **Borrowed Canon Line** ·
**Faux-Ignorance Aside** · **Comic Under-Reaction** · **Fumbled Idiom** · **Zeugma Paint** ·
**Rhetorical Catechism** · ~~Anaphoric Stack~~

**The beat is the panel, not the `support` string.** Ten of the twenty are room 2, and thirty words
cannot hold a two-beat move on their own. They land across the panel's parts — the number, the date,
the sentence, and the art are one unit — or across an adjacent pair in the kicker arc. Stating the
unit is a narrowing, not a widening: the medium still gets a beat and never a runway.

**Anaphoric Stack is narrowed to banned.** It needs three or more repeated openings and the form
gives it nowhere to repeat: the `support` strings are thirty words apart and the kickers are a fixed
enum it cannot borrow. Nineteen licensed here in practice.

**Equation / Formula Defamiliarizer finds its second home.** [#175](https://github.com/seanwinslow28/code-brain/issues/175)
restricted it to short-form and banned it in Substack for exactly that reason. A thirty-word panel is
short-form. After X, this is where it works.

## The two rules this medium exists under

**1. The craft is the qualification. The backstory is not.**

The write-up demonstrates creative skill by being well written. It never claims creative skill by
narrating where the skill came from. "As a former screenwriter, I…" is a credential sentence
wearing a story's clothes, and it spends the reader's attention on Sean instead of on the work.
Anything the reader would learn about him, they learn from how the thirty words are built.

**2. The copy never decodes the art.**

Panel copy adds information the image cannot carry — a number, a date, what broke, what changed.
It never narrates what is already visible. A caption that explains the picture has told the reader
their own eyes were not enough, and it wastes the only thirty words the panel gets.

The art's job is the mechanism: a project panel shows **how the thing works**. Hero scenes belong to
the index tiles. A panel that is atmosphere is a panel that is not doing the write-up's work, and the
copy cannot rescue it.

## No fluctuating counts

A portfolio page is durable copy. It is written once and read for a year, and nobody re-derives a
number in it. So a count that grows — agents, skills, tests, commits, subscribers — never appears in
`description` or in a `support` string. What is allowed is a **measured figure with its date**, which
is what the `number`/`date` pair is for: `$1.16/file · 2026-04-29` is true forever. "23 agents" is
true until Thursday.

Fixed design constants are fine. So is a count that is itself the finding, as long as it carries the
date that pins it.

## First screen

The surface the [lane's first-screen test](LANE.md#the-first-screen-test) runs against. There are
two, and the write-up clears both:

- **The index tile.** Title, the one-sentence `description`, and the scene art. This is where the
  reader decides whether the project exists for them, and it is decided almost entirely by the one
  sentence. Write that sentence last, from the five panels, never first from the idea.
- **The project page, above the fold.** Title, description, and panel 1 — the `situation` beat with
  its number and its card. If the situation panel is scene-setting rather than a stated problem with
  a figure on it, the page has opened on setup, and the fix is the lane's fix: move a beat up, never
  write one.

**Reply surface: none.** The site has no comments and no reply path. **No reply-hook memo ships with
a portfolio write-up** — the lane makes the memo conditional on a reply surface and this medium has
none. Say so in the ship packet rather than emitting an empty one.

## Format

- `description` is one sentence and it names the thing, not the category. It may carry a licensed
  move; most of the good ones close on the concrete half.
- `support` is at most two sentences and never more than thirty words. Under, not at.
- Every `number` is verbatim as measured. Never rounded to look tidy, never restated in prettier
  units.
- Every `date` is the date the figure was measured, not the date it was written up.
- `alt` describes what is in the frame including its figures, for a reader who gets the art only
  through it. It is not a second caption and it does not repeat `support`.
- `descriptionStatus` and any new panel stay at `draft-from-scope` / `placeholder`. **The machine
  never writes `approved`.** That flag is Sean's review, and the site's copy-review queue reads it.

## Negative specimens — what this must never look like

- **The caption that decodes the art.** "Here we see ten lit windows representing the ten agents."
  The reader has the picture. Spend the thirty words on what the picture cannot say.
- **The resume bullet.** "Led cross-functional design and engineering to deliver a 40% improvement
  in…" Borrowed strings, wrong lane, and it converts a built thing into a claim about a person.
- **The backstory credential.** Any sentence whose job is to establish that Sean is creative. The
  panel next to it is doing that job better.
- **The growing count.** "Now running 23 agents nightly." True for a week, wrong for a year, and
  nobody will come back and fix it.
- **The tidy number.** "Roughly $1 a file." The real figure was $1.16 and the real figure is the
  reason the beat lands.
- **The beat with no artifact.** A panel about an intention, an approach, or a plan. Every panel
  points at something that ran.
- **The five-panel essay.** Panels that only make sense in sequence, each one a paragraph of a piece
  that got chopped into fifths. Each panel stands alone with its number.

## Gates, in order

Post-draft and advisory as of 2026-08-31, in the machine's current order: **origin (claims tier) →
do-not-promote + coined-lines sweep → humanity scrub → critique / analyzer**.

**One narrowing, and it is this contract's own ruling.** The Expressive lane advises on untraced
claims. Here, **the origin gate blocks on `number` and `date`** and advises on `support` prose. A
portfolio page is a recruiter-facing claim surface; a fabricated figure on it is the resume's class
of harm, not the essay's, and the medium is built almost entirely out of figures. A contract may
narrow the lane and this is the narrowing. **Ratified by Sean 2026-09-01** ([#171](https://github.com/seanwinslow28/code-brain/issues/171)).

The coined-lines check runs `gates/coined_lines.py --lane expressive --artifact <project-slug>`.

## Delivery

A ship packet: the `projects.ts` patch as typed fields, any `alt` text, the ORIGIN LEDGER, the ASK
LIST, and a note that no reply-hook memo applies. The machine never commits to the site and never
flips a status to `approved`.

## What this contract does not own

The art (the anima/scene pipeline), the site's layout or tests, which projects ship (Sean), or the
figures (the transcript and the repos they were measured in).
