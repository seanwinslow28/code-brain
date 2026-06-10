---
description: Map the reader's real cultural taste through a deep, adaptive interview
argument-hint: (no arguments — just run it)
allowed-tools: Read, Write, Edit
---

You are running **Stage A — the Reference-Universe Interview** of VoicePrint. Apply
the `voiceprint-interviewing` skill throughout; it carries the craft (generic-answer
detector, follow-up ladder, respectability correction, verbatim capture). Read its
`references/interview-playbook.md` Stage A section before you begin.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. If it does not exist, tell the reader to
   run `/voiceprint-start` first, and stop.
2. If `stages.interview.status` is already `complete`, tell them so and ask whether
   they want to *extend* the existing interview (append new specifics) or skip. Do
   not silently overwrite.

## Run the interview

Conduct a real interview, not a questionnaire:

- **One question at a time.** Wait for each answer. React to it (push or advance)
  before asking the next. Never present a numbered list of questions.
- **Push on every generic answer.** Advance only when an answer contains a named
  specific (a title, a line, a place, a person, a substance, a moment). Use the
  follow-up ladder. Staying on one topic for several exchanges is good if it's
  producing gold.
- **Cover the domains** (checklist, not a script): the TV/movies they actually
  quote; music (what they grew up on, the embarrassing tier, the defend-to-death
  song, an origin story); where they're from (named places, slang, people, eras);
  food/games/sports/internet; and the thing they love but are a little embarrassed
  to admit.
- **Correct for respectability.** Open by telling them you want the 2 a.m. stuff,
  not the look-smart list. Reward embarrassing answers — they're the best signal.
- **Capture verbatim.** Preserve their exact words, typos and looseness included.

Stop when more questions stop producing new specifics (roughly 8–15 strong
specifics across the domains). Don't pad.

**Checkpoint as you go.** This is a long session, and a long session is exactly
where the model starts to misremember earlier answers as context fills. After each
domain is covered, append what you captured so far to
`voiceprint/_work/interview-transcript.md` — don't hold every answer in your head
until the end. If the session is interrupted, the file is the memory; re-read it and
resume from the last domain.

## Write the artifact

Write `voiceprint/_work/interview-transcript.md` with:

1. **Transcript** — the verbatim Q&A, in order.
2. **Inventory** — the named specifics grouped by domain, each with the real
   line/detail they gave.
3. **Deployment mechanics** — the patterns you actually observed in how THIS person
   uses references (quote-as-speech, embedded simile, faux-ignorance, comparison
   stacking, etc.). Only patterns you saw; import nothing.
4. **Gaps** — any domain that came back thin, flagged for the refine loop.

## Update state

In `voiceprint/_work/pile-state.json`: set `stages.interview.status` to `complete`
(or `incomplete` if it ran short), set its `artifact` and `updated`, and recompute
`next_best_action` (next is usually `/voiceprint-gauntlet`). Then tell the reader
what you captured in one or two sentences and point them to the next step.
