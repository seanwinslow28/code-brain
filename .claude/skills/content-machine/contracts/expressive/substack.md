# Medium contract: Substack (Expressive lane)

**Status: thin.** Written for the walking skeleton ([#163](https://github.com/seanwinslow28/code-brain/issues/163)).
It hardens in wave 1 once real posts have run through it. Where it is silent, the publication's own
law governs — do not invent a rule here to fill a gap.

## Governing documents, in precedence order

1. The publication's `SOUL.md` — the masthead. Wins over everything.
2. The publication's `POSITIONING-AND-EDITORIAL-SPEC.md` — strategy.
3. The publication's `CLAUDE.md` — standing house law (voice chain, no em dashes, anti-hype, value
   gate, privacy).
4. This contract — what the machine does differently because the medium is Substack.

For Pencil & Prompt those live under `vault/20_projects/substack-studio/`. Read them before the
interview. A machine that reads the house rules after drafting has already wasted the interview.

## What a post has to deliver

- **A real artifact.** Something that actually happened or actually ran, captured. Never "here's how
  you could." No artifact, no post — the gate blocks and the piece waits.
- **A verdict or a lesson.** The spine series ends in a tested verdict. The story series ends in a
  navigation lesson: what the author does differently now.
- **Transfer.** The reader can do something with it that they couldn't before they read it.
- **The ask lands sideways.** Never a closing pitch, never "I need", never "you can hire me".

## Shape

Lead with the captured thing, never the abstract premise. A universal observation as an opening line
is the one shape the publication exists against.

Section last lines carry the same pressure as the closer. A deflation or an appalling pivot, never a
summary. The closer is the strongest line in the piece.

Length is bounded by padding, not word count: long enough to tell it, then stop.

## Licensed moves

The full attested roster in `writing-voice-modes` is licensed here, prose forms only — Substack is
the medium the roster was calibrated on. Two carve-outs:

- **Screenplay-only forms are not licensed.** All-caps as script format convention is not the prose
  Shout-Caps move.
- **Per-move licensing is not this contract's call.** The audit ([#162](https://github.com/seanwinslow28/code-brain/issues/162))
  will assign moves per medium properly. Until it lands, this contract licenses broadly and relies
  on the anti-pattern sweep to catch overreach.

**References are rationed: two to three woven references per piece, maximum, most paragraphs zero.**
Sourced from `reference-universe.md` or the piece's own subject. Never invented. A reference that
could be swapped for a different one and dropped anywhere is garnish — cut it.

## Hard mechanics

Inherited from `writing-voice-modes` G1–G5, restated because Substack drafts break them most:

- No em dashes. Anywhere. And no colon substituted in when one is dropped.
- Contract everything.
- Colons and semicolons rare or absent.
- No word that isn't working.
- Adjacent beats must turn. If "and then" fits better than "but" or "therefore", the beat is dead.

## Gates, in order

Value → structure → shape → critique → humanity → origin → do-not-promote.

The origin check runs `gates/origin_check.py` (mechanical layer) plus a reading pass for
recombination, which the mechanical layer is blind to. Expressive lane advises and never blocks.

## Delivery

Frontmatter follows the publication's existing convention (series, title, status, itch,
solution_artifact, transfer, hero_image, open_items). Drafts live in the publication's own folder,
one directory per piece. The machine never publishes; it hands over a ship packet.

## What this contract does not own

Story order (`storytelling-architecture`), whether the piece is worth writing
(`substack-value-engine`), sentences (`writing-voice-modes`), or the publishing decision (the
author).
