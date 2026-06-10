---
description: Paste pre-AI writing; extract how you actually build a sentence, quoted back
argument-hint: (paste a chunk of your old writing, or just run it)
allowed-tools: Read, Write, Edit
---

You are running **Stage C — Mine Pre-AI Writing** of VoicePrint. Apply the
`voiceprint-interviewing` skill; read its `references/interview-playbook.md` Stage C
section first. This is the strongest signal of all: real writing the reader made
before a model could make it for them is provably their own voice.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. If it does not exist, tell the reader to
   run `/voiceprint-start` first, and stop.

## Get the sample

If the reader pasted writing with the command (`$ARGUMENTS`) or in the message, use
it. Otherwise ask:

> "Find something you wrote before you used AI to write anything — old enough that
> no model was involved. An old blog, texts to a friend, a journal, emails, a
> half-finished anything. Paste a real chunk, unguarded. Don't summarize it — paste
> it."

**Cold-start fallback** — if they say they have nothing, climb the ladder: reframe
"writing" (texts, DMs, captions, a group-chat rant, a review, a toast); point them
at a medium they already use; lower the bar (unedited is better). If genuinely
nothing exists: set `mine.cold_start: true`, lean on Stages A + B for signal, and
tell them plainly their skill will be **outline-grade** until they feed it real
samples — that's expected, the refine loop is where it gets real. Never pretend it's
fully calibrated.

## Mine it

Read the pasted writing and **quote their own lines back as evidence** for each
mechanic you find: rhythm (staccato vs. flowing, where it varies), where jokes
land, run-length before a cut, words/constructions they reach for, how they open and
close, and what they do being sincere vs. deflecting. Evidence leads; your label
annotates.

## Validate (prove you got them, not faked it)

Write **3 NEW sentences on a totally different topic** using their exact mechanics.
Ask: "Which of these land like you, and which feel faked?" Capture which landed and
why. This is the first turn of the calibration loop — a rejected sentence corrects
your extraction.

## Write the artifact

Write `voiceprint/_work/mined-samples.md`:
- The pasted writing, **verbatim** (do not clean it up).
- The extracted mechanics, each with a quoted line as evidence.
- The 3 test sentences with the reader's land/fake verdicts.
- The `cold_start` note if it applied.

## Update state

In `voiceprint/_work/pile-state.json`: set `stages.mine.status` to `complete` (or
`incomplete` for cold-start), set `artifact`, `cold_start`, and `updated`, and
recompute `next_best_action`. If interview + gauntlet + mine are all done, the next
action is `/voiceprint-synthesize`. Tell the reader what you found and point them
forward.
