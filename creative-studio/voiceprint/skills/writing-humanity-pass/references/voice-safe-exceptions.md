# Voice-Safe Exceptions: Tell vs Signature-Move Crosswalk

In a VOICE-SAFE scrub, some `[CLASH]` tells from `ai-tells.md` collide with a
*deliberate* signature move — a move documented in the writer's own voice skill
(`my-voice/SKILL.md`, the signature-move table). When a tell collides with one of the
writer's real moves, **DEFER to the move and cite it.** In a FULL (neutral) scrub
there is no voice, so cut these normally.

## How to use this file

The writer's allowlist is **their** signature-move table, not a fixed list. Before
scrubbing voice-bearing text, read `my-voice/SKILL.md` and treat every move in its
table as protected. This file only teaches the *pattern* of collision — which generic
AI tells most often turn out to be a deliberate move in disguise:

| AI tell (ai-tells.md #) | Often collides with a move like… | Voice-safe resolution |
|---|---|---|
| #1 Significance inflation | a build-then-deflate move (epic setup landing on a mundane/absurd close) | Keep the build ONLY when it lands on a real deflation; cut it when it inflates and never pays off. |
| #10 Rule of three | a rule-of-three-with-a-pivot move (two light items, third turns real) | Keep when item 3 pivots to genuine feeling; cut decorative triples that don't pivot. |
| #12 False ranges | a metaphor-stacking move (several images for the SAME thing) | Cut literal "from X to Y" non-scales; keep escalating metaphor stacks that describe one reality. |
| #25 Generic conclusion | a callback-closer move (the close transforms the opening image) | Defer the closer slot to the writer's move; never let it collapse into "the future looks bright." |

These four are illustrations of the collision *pattern*. The actual protected moves
are whatever the writer's voice skill documents — match against THAT.

## Always-protected (when the writer's skill documents them)

Naive humanizers cut these, but they are human signals, not chatbot artifacts, when
they appear in a writer's documented voice:
- Stacked "and...and...and" (polysyndeton) used for rhythm — flag only if it runs a
  whole piece with zero variation.
- Sensory cascades, pop-culture anchoring, and hyper-specific anecdote — protected;
  the only cap is the writer's own "one strong reference earns it, three is
  self-indulgence" rule (flag a third repeat of the SAME image, not the technique).
- Parenthetical asides and self-corrections — a human signal.
- Self-deprecation as structure — protected UNLESS it slides into self-pity or names a
  direct ask; that is the "desperation posing as self-deprecation" trap, which IS a flag.

## Punctuation

Whether em dashes are a tell depends on the writer's preference (`pile-state.json` →
`preferences.em_dashes`). See SKILL.md "Punctuation preference." Do not treat the dash
as a universal cut.
