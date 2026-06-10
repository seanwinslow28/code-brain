# Synthesis Method

Depth layer for `voiceprint-synthesis`. How to fill the templates from the reader's
evidence without distilling, inventing, or leaking.

## The fill loop

For each template, go placeholder by placeholder:

1. **Find the evidence.** Locate the specific quote(s) in `_work/` that support this
   slot — a sample line, an interview specific, a gauntlet reaction.
2. **Quote it.** Drop the verbatim line in. The reader's words fill the slot; your
   words are only the label around it.
3. **If there's no evidence, don't fill it.** Cut the row/section, or write one
   honest line that the evidence is thin here and the refine loop will fill it. Never
   invent a move, a reference, or a reaction to complete the shape.

A filled template should read, when you scan it, as *mostly the reader's words* with
your light scaffolding between. If it reads as mostly your prose with a few quotes
sprinkled in, you distilled — go back and let the evidence lead.

## Worked micro-example (generic — shows the shape, not a person to copy)

Suppose `_work/mined-samples.md` contains this reader passage:

> "i didn't plan the talk. i just walked up there with three index cards and a coffee
> i'd already spilled on, and started telling them about the time the printer caught
> fire. people laughed. i forgot card two entirely."

**Distillation (WRONG):**
> Signature move: Self-deprecating, anecdotal, casual delivery with vivid detail.

**Evidence-first (RIGHT) — a signature-move row:**
| Move | What it does | Quoted proof |
|---|---|---|
| Prop-anchored open | Opens on a concrete object mid-scene, not a thesis | "three index cards and a coffee i'd already spilled on" |

The second one teaches the model something specific and checkable. The first is an
adjective cloud. Always produce the second.

## Wiring the samples-win statement

The generated `SKILL.md` must carry the authority rule verbatim (it's in the
template). Make it real, not decorative:
- The signature-move table's "proof" column must hold actual sample lines.
- The anti-patterns' "their reaction" column must hold actual gauntlet reactions.
- `voice-samples.md` must hold the real passages, one per heading.
If those three are genuinely the reader's evidence, the "samples win" rule has teeth.
If they're your paraphrases, the rule is a lie and the skill will drift.

## Analyzer-shape rules (so the proof step works)

`voice-samples.md` is read by `/voiceprint-proof` and the `writing-critique` analyzer
to compute the reader's fingerprint. Honor the shape:
- **One self-contained passage per `##` heading.** The analyzer splits on headings.
- **Use long, real passages.** Burstiness and lexical-diversity signals are
  meaningless on one-liners. Prefer the reader's longest most-them samples.
- **Verbatim only.** A fingerprint computed on your cleaned-up version of their prose
  measures *you*, not them, and the proof becomes a lie.

## Cold-start

If `pile-state.json` has `mine.cold_start: true`, include the outline-grade banner
(in the template) at the top of the generated SKILL.md, and bias the bundle toward
the interview + gauntlet evidence. Be honest in the prose that the sample-backed
parts are thin and will fill in through refine rounds.

## Zero-leakage check (run before finishing)

Before you call synthesis done, scan the generated bundle for any content that did
NOT come from this reader's `_work/` files — a reference, a move, a turn of phrase, a
register rule that you carried in from anywhere else (including other voice skills you
may have seen). If you find one, cut it. The bundle is built from this reader's
evidence and nothing else.
