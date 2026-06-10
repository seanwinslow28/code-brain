---
description: Generate 10 lines in the register you most hate; your disgust draws the outline
argument-hint: (optional) a topic you'd actually write about
allowed-tools: Read, Write, Edit
---

You are running **Stage B — the Cheese Gauntlet** of VoicePrint. Apply the
`voiceprint-interviewing` skill; read its `references/interview-playbook.md` Stage B
section first. The whole trick: people can't describe their voice but can spot what
*isn't* it instantly. Their "no" draws the outline.

## Before you start

1. Read `voiceprint/_work/pile-state.json`. If it does not exist, tell the reader to
   run `/voiceprint-start` first, and stop.
2. The gauntlet works best after the interview, but does not require it. If
   `stages.interview.status` is not `complete`, note that running the interview
   first sharpens the lines, and let them proceed if they want.

## Run the gauntlet

1. **Get a real topic.** Use `$ARGUMENTS` if provided; otherwise ask: "Pick a topic
   you'd actually write about — your work, a life update, a thing you learned."
2. **Confirm the register to parody.** Default to the universal cringe registers
   (LinkedIn-inspirational, motivational-poster, fake-profound, hustle-culture,
   epiphany cliché, hype-closer). Let them name a more specific register they hate.
3. **Generate 10 short lines "in their voice"** on that topic, but written in the
   hated register: fluent, confident, grammatically perfect. Number them 1–10.
   **Do not explain them. Present the ten lines and wait.**
4. **Coach the reaction** before they respond: "React to each fast — one or two
   words. 'No.' 'Gross.' 'Never.' Don't explain yet; the gut reaction is the
   signal. If one's almost right but still off, tell me why in five words."
5. **Collect all ten reactions**, verbatim.

## Turn disgust into the bank

Synthesize what the reactions reveal:
- The **registers they reject** (name each cringe family they hit).
- The **moves they won't make** (parallel-structure inspiration, naming the lesson
  out loud, abstract profundity, etc.).
- The **instant-tell words** that made them recoil.
- Any **fix they offered** — if they rewrote a bad line into a true one, capture
  that inversion verbatim; it's the highest-value thing in the stage.

## Write the artifact

Write `voiceprint/_work/gauntlet-reactions.md`:
- A table: line # | the line | their verbatim reaction | cheese type.
- Then the synthesized sections: registers I reject / moves I won't make /
  instant-tell words / my fixes.

## Update state

In `voiceprint/_work/pile-state.json`: set `stages.gauntlet.status` to `complete`,
set `artifact` and `updated`, recompute `next_best_action` (next is usually
`/voiceprint-mine`). Tell the reader, in one or two sentences, what their disgust
revealed, and point to the next step.
