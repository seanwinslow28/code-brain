---
description: Generate your personal voice skill from the evidence you've collected
argument-hint: (no arguments — run it after the interview, gauntlet, and mine)
allowed-tools: Read, Write, Edit
---

You are running **Stage D — Synthesis** of VoicePrint. Apply the
`voiceprint-synthesis` skill; read its `references/synthesis-method.md` and the four
files in its `templates/` directory before you generate anything.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. If it does not exist, tell the reader to
   run `/voiceprint-start` first, and stop.
2. Check the stages. Ideally `interview`, `gauntlet`, and `mine` are all `complete`.
   If some are missing, tell the reader what's thin, and ask whether to proceed with
   a partial (honestly flagged) bundle or collect more first.

## Generate the bundle

Read the reader's evidence — `_work/interview-transcript.md`,
`_work/gauntlet-reactions.md`, `_work/mined-samples.md` — and generate their voice
skill into `voiceprint/my-voice/`, filling the four templates:

- `my-voice/SKILL.md` ← `SKILL.template.md`
- `my-voice/references/reference-universe.md` ← `reference-universe.template.md`
- `my-voice/references/cheese-bank.md` ← `cheese-bank.template.md`
- `my-voice/references/voice-samples.md` ← `voice-samples.template.md`

Hold to the two governing rules:
- **Quote evidence, never distill it.** Every voice claim is backed by a verbatim
  quote from the reader's `_work/` files. No quote → no claim. Strip the template's
  `<!-- guidance -->` comments from the generated output.
- **Samples are the binding constraint.** The generated SKILL.md carries the
  authority statement verbatim; the move table cites real sample lines; the
  anti-patterns cite real gauntlet reactions; `voice-samples.md` holds real passages,
  one per `##` heading (so `/voiceprint-proof` can fingerprint them).

If `mine.cold_start` is true, include the outline-grade banner and bias toward the
interview + gauntlet evidence; say plainly that the sample-backed parts are thin.

**Zero-leakage check:** before finishing, scan the bundle for anything that did not
come from this reader's `_work/` files and cut it.

## Update state and hand off

In `voiceprint/_work/pile-state.json`: set `stages.synthesize.status` to `complete`,
record `generated_from` (the artifact paths you read) and `updated`, and recompute
`next_best_action` to point at `/voiceprint-refine` (and `/voiceprint-proof` once
refine has run at least once).

Then tell the reader, in a couple of sentences: where their skill lives
(`voiceprint/my-voice/`), how to use it (drop it in their Claude skills folder, or
just point Claude at it), and that it sharpens through `/voiceprint-refine`. Do not
oversell it as finished — name one thing that's still thin and will improve with reps.
