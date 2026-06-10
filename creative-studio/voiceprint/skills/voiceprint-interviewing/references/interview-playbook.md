# Interview Playbook

Depth layer for `voiceprint-interviewing`. Per-stage question banks, worked push
examples, the gauntlet register menu, the cold-start fallback ladder, and the
mining extraction checklist. Load when running an elicitation command.

---

## Stage A — Reference-Universe Interview

Goal: a map of the reader's *actual* cultural taste, so their generated skill never
invents a generic reference. References are roughly half of voice; a model will
fabricate plausible-but-wrong ones unless handed the real library.

### Domains to cover (not a script — a checklist of pressures)

- **TV & movies they actually quote** — not the prestige list; the lines that come
  out of their mouth in real life.
- **Music** — what they grew up on, the embarrassing tier, the one song they'd
  defend to the death, the origin story of getting into a band.
- **Where they're from** — the specific places, slang, people, eras. Neighborhood
  details, the bar, the school, the job.
- **Food / games / sports / internet** — whatever they actually spend time on.
  Food TV, a lifelong game, the one team with feelings attached, the corner of the
  internet they live in.
- **The thing they love but are a little embarrassed to admit** — almost always
  the highest-signal answer in the whole interview.

### Opening line (set the frame)

> "I'm going to map your actual taste so your voice skill never invents a generic
> reference. I'll ask one thing at a time and I'll push when an answer's too clean.
> Give me the stuff you actually quote at 2 a.m., not the stuff you'd list to look
> smart. Wrong-but-true beats impressive. Ready? First one:"

### Worked push examples (generic → the follow-up that cracked it)

| They said | Don't accept | The push that worked |
|---|---|---|
| "I like comedies." | category | "Name the exact bit you quote most." |
| "Good classic rock." | category | "Which song, and where were you the first time it hit you?" |
| "I'm from the city." | vague place | "Which block? What was on the corner?" |
| "I love Kurosawa." | respectability bias | "Sure. Now the dumb one — what do you put on when you're hungover?" |
| "I'm pretty sarcastic." | self-description | "Don't tell me — quote me the last sarcastic thing you actually said." |
| "It was a rough year." | feeling, no scene | "Walk me to one specific day. Where were you, what happened?" |

### The deployment-mechanics note (part of the artifact)

After the inventory, capture HOW they deploy references, because the same reference
used wrong reads as fake. Watch for and note patterns like:
- Quote-as-speech (canon lines dropped in unattributed as their own words).
- Embedded-quote-as-simile (a line woven into a sentence, source unflagged).
- Faux-ignorance (deadpan pretending not to know a famous thing).
- Underdog/comparison stacking, self-incriminating third item.
Record the patterns you actually observe in THIS person — don't import a list.

### Artifact → `_work/interview-transcript.md`

Verbatim Q&A, then a tight inventory section: the named specifics grouped by
domain, each with the real line/detail they gave, plus the deployment-mechanics
note. Mark any domain that came back thin.

---

## Stage B — The Cheese Gauntlet

Goal: weaponize disgust. People can't describe their voice but spot what *isn't* it
instantly. The "no" draws the outline the adjectives couldn't.

### Setup

1. Ask: "Pick a topic you'd actually write about — your work, a life update, a
   thing you learned." Get a real one.
2. Confirm the register to parody. Default to the universal cringe registers; let
   them name a more specific one they hate.
3. Generate **10 short lines "in their voice"** on that topic, but in the hated
   register: fluent, confident, grammatically perfect. Number them 1–10. **Do not
   explain them. Present the ten and wait.**

### The register menu (what to write the bad lines in)

The universal cringe registers (use unless they name their own):
- **LinkedIn-inspirational** — "X wasn't an ending. It was an invitation to begin."
- **Motivational poster** — "Every rep is a vote for the person you're becoming."
- **Fake-profound** — "There's something magical about ___."
- **Hustle-culture** — "5 AM. Coffee. Grind. This is where it happens."
- **Epiphany cliché** — "In that moment, I realized the future was already here."
- **Hype-closer** — "Buckle up, because the next decade is going to be wild."

### Reaction coaching (say this before they react)

> "React to each fast. One or two words — 'No.' 'Gross.' 'Never.' Don't explain
> yet; the gut reaction is the signal. If one's almost right but still off, tell me
> why in five words."

### Turning disgust into the bank

After the ten reactions, synthesize what they reveal:
- The **registers they reject** (name each cringe family they hit).
- The **moves they won't make** (parallel-structure inspiration, abstract
  profundity, naming the lesson out loud, etc.).
- The **instant-tell words** — specific words that made them recoil ("magical,"
  "journey," "unlock").
- Any **fix they offered** — when someone rewrites a bad line into a true one
  ("New chapter, same dream" → "Different city, different chapter, same shit"),
  that inversion is pure gold; capture it verbatim.

### Artifact → `_work/gauntlet-reactions.md`

A table of the 10 lines + verbatim reaction + cheese type, then the synthesized
"registers I reject / moves I won't make / instant-tell words / my fixes" sections.

---

## Stage C — Mine Pre-AI Writing

Goal: the strongest signal of all. Real writing the reader made before a model
could make it for them is evidence of a voice that's provably theirs.

### The ask

> "Find something you wrote before you used AI to write anything — old enough that
> no model was involved. An old blog, texts you sent friends, a journal, emails, a
> zine, a half-finished anything. Paste a real chunk, the more unguarded the
> better. Don't summarize it — paste it. I learn more from one rambling real
> paragraph than from any description."

### Cold-start fallback ladder (for "I don't have anything")

Most people think they have nothing. They do. Climb until something surfaces:
1. **Reframe "writing."** "Not just essays — texts, DMs, captions, a long rant in
   a group chat, a review you left, a Reddit comment, a toast you wrote."
2. **Point at a medium they use.** "Open your texts to your closest friend and
   scroll up a year. Paste a real exchange."
3. **Lower the bar.** "It doesn't have to be good. Unedited is better."
4. **If genuinely nothing exists:** record `mine.cold_start: true`, lean harder on
   Stages A + B for voice signal, and tell them plainly: their skill will be
   **outline-grade** until they feed it real samples — and that's expected, the
   refine loop is where it gets real. Do not pretend the skill is fully calibrated.

### The mining extraction checklist

Read the pasted writing and quote their own lines back as evidence for each:
- **Rhythm** — short staccato vs. long flowing; where they vary it.
- **Where jokes land** — sentence-end punchline? buried mid-list? deadpan?
- **Run-length before a cut** — how long they build before deflating.
- **Words & constructions they reach for** — recurring diction, sentence shapes,
  punctuation habits.
- **How they open / how they close** — their instinctive first and last moves.
- **Sincerity vs. deflection** — what they do when being real vs. when dodging.

### The validation test (proves you got them, not faked it)

After extracting, write **3 NEW sentences on a totally different topic** using their
exact mechanics. Ask: "Which of these land like you, and which feel faked?" Capture
which landed and why. A landed test sentence confirms a real mechanic; a rejected
one corrects your extraction. This is the first turn of the calibration loop.

### Artifact → `_work/mined-samples.md`

The pasted writing (verbatim), the extracted mechanics each with a quoted line as
evidence, the 3 test sentences with the reader's land/fake verdicts, and the
`cold_start` flag if it applied.
