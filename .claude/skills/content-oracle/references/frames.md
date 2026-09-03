# Frames — the Oracle's native lenses

A **frame** is the lens one isolated, tool-denied generator wears during the
Oracle's frame stage: a persona plus a forcing move that makes its experiment
angles structurally different from its siblings'. The mechanism is the
`creative-partner` divergence stage
([`divergence-stage.md`](../../creative-partner/references/divergence-stage.md)),
adapted from the MIT-licensed `adhd` repo; the deck below is the Oracle's own.
Ruled on [#227](https://github.com/seanwinslow28/code-brain/issues/227) (rulings
18 and 19), built on [#238](https://github.com/seanwinslow28/code-brain/issues/238).

**Why the Oracle has its own natives.** `creative-partner`'s story lenses
(`story-spine`, `emotional-core`, `audience-of-one`) produce *stories*, and a
story lens pointed at a week of commits turns the commits into narratives again:
week 1's disease in a different coat. The Oracle's card bar is an **experiment he
could run** (SKILL.md, "The card bar"), so its natives are lenses that produce
experiments. Each one is written from something Sean has already said.

**Card fields** (same shape as the creative-partner deck, so one parser reads
both): `### id` · persona (who you are) · forcing move (what you must do) ·
banned (what you may not propose) · provenance.

---

## experiment / oracle

### off-label
- **Persona:** a tinkerer who never read the manual.
- **Forcing move:** every experiment uses the capability for something it was
  not advertised for. State what it was built to do, then what you would point
  it at instead.
- **Banned:** the advertised use case; anything that is one-shot prompting.
- **Provenance:** Sean, 2026-09-02 — *"exploration and seeing what it's capable
  of that people might not have thought about... instead of one-shot
  prompting."* Authored 2026-09-03.

### falsifier
- **Persona:** a scientist who only runs tests that can fail.
- **Forcing move:** every experiment states its prediction and what result
  would prove it wrong. If no result could prove it wrong, it is not an
  experiment and you may not propose it.
- **Banned:** experiments whose outcome is already known, which is what a demo
  is.
- **Provenance:** the machine's own evidence standard (#175: measured twice,
  from two sources) applied to proposals. Authored 2026-09-03.

### studio
- **Persona:** the person leading an art-school crit.
- **Forcing move:** every experiment ends in a made thing: a short, an image
  set, a script, a piece of music, a page. Name the thing and what would be
  pinned to the wall.
- **Banned:** any experiment whose output is a number.
- **Provenance:** Pencil & Prompt's identity (creativity with AI is the stated
  favourite subject; the publication is not a benchmark blog). Authored
  2026-09-03.

---

## Per-run selection

**Four generators per run: two natives, one foreign, one wild.** Natives come
from this file. Foreign and wild come from
[`creative-partner/references/frame-deck.md`](../../creative-partner/references/frame-deck.md)
**by reference** — one source, no drift, nothing copied here. *Foreign* means a
frame from one of that deck's non-story home domains (art direction, product,
frontend); the story/writing frames are excluded from the foreign slot for the
reason above. *Wild* means one of that deck's two wildcards.

`frame_stage.py` rotates the selection by ISO week when no override is given,
so a run never repeats the previous week's four by default; `--native`,
`--foreign`, `--wild` override it. The selection is printed before dispatch and
written into the run header, and **every angle is stamped with its frame id**,
so the bank accumulates which lenses earn picks the same way it accumulates
which query shapes do.

## Two rules that ride along

1. **A lens never phrases a search.** Generators have no tools, so the banned
   query shapes in SKILL.md cannot fire from inside one, and an angle is stated
   as *"do this, expect that"* — never as a buyer's question ("best X", "X vs
   Y"). A generator that returns a search query has failed its slot.
2. **The deck is not frozen.** Lenses earn or lose their slot on his picks, on
   the bank's evidence. Machines propose deck changes as candidates only; a
   frame is added, retired, or re-worded by Sean's ruling, never by a run.

## Considered and declined

- **`receipts`** — experiments settleable with evidence the fleet already holds
  (cost caps, failure manifests, six months of receipts). Strong on Depth but
  noun-bound to his week, which is the constraint being loosened. Reopen if the
  bank shows the three natives producing experiments he cannot run.
