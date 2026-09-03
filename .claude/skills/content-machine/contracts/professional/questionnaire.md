# Medium contract: Application questionnaire (Professional lane)

Wave 2 ([#171](https://github.com/seanwinslow28/code-brain/issues/171)).

## Governing documents, in precedence order

1. [`LANE.md`](LANE.md) — Professional-lane law.
2. [`../move-licensing.md`](../move-licensing.md) — the shared matrix.
3. This contract.

## What this medium is

The free-text boxes in an application: *why this company*, *tell us about a time you shipped
something that failed*, *what product do you admire and why*. Usually three to six of them, usually
with a word or character limit, usually inside an ATS.

Two properties make it a different document from the cover letter, and both of them are load-bearing:

**The question is given.** The machine does not choose the frame. Every other document in this lane
decides what it is about; this one is told.

**The set is read as one document, by one person, in one sitting.** No other Professional document
has four siblings on the same screen.

## Licensed moves: six, and the shape they make is the point

Budget heat 1, room 2. Six of thirty-six, the same six the cover letter gets:

**Expectation / Instead** · **Then / Now Narrator** · **Short Declarative Drop** ·
**Anaphoric Stack** · **Blunt-Literal Description** · **Rhetorical Catechism**

All six are structural. Not one is a joke. Everything at heat 2 or above is banned — no pop culture,
no self-deprecation as structure, no under-reaction, no canon line.

**One narrowing, from the second property above: Anaphoric Stack is rationed to one box in the set.**
The move works by repetition, and a reader meeting it in three of five answers is not meeting a
voice, they are meeting a template. This is the only medium where a licensed move can be spent by
being used correctly twice.

## Answer the question that was asked

The commonest failure here is not a voice failure. It is answering the adjacent question — the one
with better material, or the one already answered in the cover letter. A reader notices immediately,
and it reads as evasion rather than as reuse.

**The test:** read the answer without the question above it. Can you reconstruct what was asked? If
what you reconstruct is a different question, the box has been answered wrong no matter how good it
is.

## No claim, no anecdote, and no opening shape appears twice across the set

This is the rule that belongs to this medium and to no other. Five answers are graded against each
other, not one at a time.

- **A claim spent in box 2 is spent.** Restating it in box 4 does not double it; it halves both.
- **An anecdote spent in box 2 is spent.** Even a good one, even from a different angle. The reader
  concludes there is one story.
- **An opening shape spent in box 2 is spent.** Five answers that each open on a scene, or each open
  with a question, read as filled-in slots.

The ship packet carries a **cross-answer repetition report** for exactly this reason: the failure is
invisible inside any single box.

## The empty box is where invention comes from

A question handed to you, a blank field, and a word counter is the most gap-fill-inviting shape in
the whole machine. Every other document lets you write about what he actually said. This one asks
what it wants to know.

**A question with no transcript material is an ASK LIST item, not an improvisation.** Go get the
answer, or leave the box for him. The lane's rule stands and doubles here: **hedging is not
tracing** — an answer softened until it is unfalsifiable has converted a claim the gate would catch
into one it cannot, in the document most likely to be read closely.

## No ask, in any box

The cover letter has an explicit exception to `substack-value-engine`'s sideways-ask rule, because a
cover letter that never asks for the interview has failed at the genre. **That exception does not
extend here.** A questionnaire box is not the close of an application; it is a question being
answered. An answer that ends by asking for the role has changed documents mid-form.

## Format

- **Under the limit, never at it.** A 200-word box answered in 190 words reads as a person who had
  more to say and chose. Answered in 200 it reads as a person who ran out of room.
- **Write for plain text.** The ATS strips formatting. No markdown, no bold, no headers. A bulleted
  list may render as literal asterisks or as one run-on line — assume it will.
- **The reader scans the first line of every box before reading any of them.** So no box opens by
  restating the question, and no two boxes open the same way. This is a format fact about how the set
  is read, not the Expressive lane's first-screen test, which does not apply here.
- **The exact question text ships with the answer**, verbatim, so the pairing cannot drift.

## Negative specimens — what this must never look like

- **The restated question.** "I'm interested in working at Acme because Acme is doing interesting
  work in…" The first sentence has said nothing and the reader is scanning five of these.
- **The cover letter, pasted.** Same story, same claims, worse fit — and the reader has both.
- **The answer to a different question.** Especially the one with the better anecdote.
- **The same anecdote twice.** Once is a story. Twice is the only story.
- **The hedged claim.** "Helped contribute to a meaningful improvement in…" Ask or strike.
- **Borrowed enthusiasm.** "Your innovative approach to…" Template strings, banned by the lane.
- **The essay in the small box.** A 150-word answer wearing a 400-word structure, so the point lands
  after the limit and gets cut by the form.

## Gates, in order

Post-draft as of 2026-08-31, in the machine's current order: **origin (claims tier) →
do-not-promote + coined-lines sweep → humanity scrub → critique / analyzer**. Professional lane:
**origin blocks delivery** while any claim is untraced (`origin_check.py` exits 1).

`writing-humanity-pass` runs **FULL** scrub, as in the rest of this lane below LinkedIn. The six
licensed moves are structural rather than voice-bearing, so there is no signature-move layer to
protect — but a licensed move is a deliberate choice and is not a tell.

Coined lines run `gates/coined_lines.py --lane professional`, across the **whole set at once**. A
line reused between two boxes of the same application is the cheapest possible instance of the
failure the rule exists for.

## Delivery

A ship packet: each answer keyed to its verbatim question text, the ORIGIN LEDGER, the ASK LIST, and
the cross-answer repetition report. The machine never submits an application.

## What this contract does not own

Whether to apply (Sean), which role (Sean), or the claims (the transcript).
