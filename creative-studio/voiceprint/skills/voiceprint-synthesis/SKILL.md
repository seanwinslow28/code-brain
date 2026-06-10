---
name: voiceprint-synthesis
description: >
  Generate a reader's personal writing-voice skill from their collected evidence.
  Use when running /voiceprint-synthesize, or when asked to "build my voice skill",
  "generate my voiceprint", "turn my interview and gauntlet into a skill", or
  "synthesize my voice bundle". Reads the three reference files (reference universe,
  cheese bank, voice samples) and emits a complete, reusable voice-skill bundle —
  quoting the reader's verbatim evidence, never paraphrasing it into adjectives.
version: 0.1.0
---

# VoicePrint Synthesis

Turn a pile of evidence into a working voice skill. This is the step that decides
whether the reader gets *their* skill or a template with their name on it. The whole
job is governed by one rule, and a second rule that keeps the result from drifting.

## Rule 1 — Quote evidence, never distill it (the anti-genericness gate)

The failure that produces one bland skill for everyone: summarizing a voice into
adjectives. "Witty, conversational, a little dark" fits half the planet and teaches
the model nothing.

**Every claim in the generated bundle must be backed by a verbatim quote from the
reader's evidence.** If you write "she opens cold, mid-scene," the next line must be
her actual opener, quoted. If you can't quote it, you can't claim it — cut the claim.

- Pull the reader's real lines, references, and reactions into the bundle **word for
  word**, typos and looseness intact. Looseness is voice data.
- Your prose is the *connective tissue and the labels*. The evidence leads; your
  annotation rides behind it. Never the reverse.
- A generated reference file should read mostly as the reader's own words, lightly
  organized — not as your description of them.

Test before writing any line of the generated SKILL.md: *is there a specific quote
under this, or is it an adjective?* Adjectives without evidence are the tell that
distillation crept in. Delete them.

## Rule 2 — Samples are the binding constraint, rules only annotate (the drift defense)

A skill made of *rules* drifts: the model's training overrides a "write like this"
instruction within a paragraph or two. A skill anchored to *verbatim samples* holds,
because the samples are concrete evidence the model matches against, not an
abstraction it averages away.

So the generated SKILL.md must say, explicitly, in its own body:

> **When these rules and the voice samples conflict, the samples win.** The samples
> are the authority; the rules below are notes that point at what the samples
> already prove.

Build the bundle so the samples carry the weight: the signature-move table cites
sample lines; the anti-patterns cite gauntlet reactions; the reference list is the
reader's real library. The downstream chain (`writing-critique`,
`writing-humanity-pass`, and the refine loop) re-grounds every draft against these
samples, which is how the voice survives length instead of drifting.

## Inputs

Read from the reader's workspace (paths relative to their `voiceprint/` root):
- `_work/interview-transcript.md` — reference universe (Stage A)
- `_work/gauntlet-reactions.md` — what they reject (Stage B)
- `_work/mined-samples.md` — how they build a sentence (Stage C)
- `_work/pile-state.json` — stage status, preferences, `mine.cold_start`

If a stage is missing or incomplete, say so and proceed with what exists, flagging
the result as partial (see Cold-start).

## Outputs — the reader's bundle

Generate into `my-voice/` (next to `_work/`), from the templates in
`templates/`. Fill every `{{PLACEHOLDER}}` from the reader's evidence; never leave a
placeholder, and never invent content to fill one — if the evidence is thin, say so.

```
my-voice/
├── SKILL.md                      # from SKILL.template.md
└── references/
    ├── reference-universe.md     # from reference-universe.template.md
    ├── cheese-bank.md            # from cheese-bank.template.md
    └── voice-samples.md          # from voice-samples.template.md
```

### The generated SKILL.md must contain

- **The samples-win statement** (Rule 2), verbatim.
- **The reader's signature moves** — a table, each row a move named from THEIR
  evidence with a quoted line as proof. Mined from the samples + interview. Do not
  import moves from any other person's skill.
- **Their register / house style** — the texture, built from the interview + the
  gauntlet (what they reject defines the edges). Quoted anchors.
- **A professional dial** — ONLY if the evidence shows the writer in two or more
  registers. Do not invent contextual range: with a single-register corpus you cannot
  claim how the voice flexes, so say that honestly in one line and omit the table.
  Asserting "their voice barely changes" or "they dial down by substitution" without a
  sample that proves it is the distillation trap wearing a confident face.
- **Anti-patterns** — the four universal anti-slop rules (below) as the spine, PLUS
  the reader's specific rejected registers, each citing a gauntlet reaction.
- **An Off-limits section** the reader fills in, in their own words (topics true but
  not for showing) — never framed as marketing/"promotion" jargon.
- **References pointer** to the three generated reference files.

### The universal anti-slop spine (ships in every reader's SKILL.md)

These four are not specific to any one writer — they are how voice survives
generation for anyone. Include them, framed generically:

1. **The distillation trap** — write from quoted exemplars, not adjective summaries.
2. **Reference gorging** — references are a pantry, not a menu; ration them; most
   sentences should run on the writer's own specifics, not borrowed ones.
3. **Limp deflation** — self-deprecation must be a specific incriminating story
   (named place/person/cost), never an abstract "I'm bad at X."
4. **Register-by-substitution** — to dial intensity down, swap each strong word for
   its tamer equivalent and keep the bite; never sterilize to neutral.

## Make the bundle analyzer-ready (feeds the proof step)

`/voiceprint-proof` and the bundled `writing-critique` analyzer read
`voice-samples.md` to compute the reader's quantitative fingerprint (sentence-length
burstiness, lexical diversity) for the "more you, less generic-AI" proof. So:
- In `voice-samples.md`, put **one self-contained sample passage per `##` heading**
  (the analyzer reads passages by heading). Use the reader's longest, most-them real
  passages — not one-liners.
- Keep the samples verbatim and uncut; the fingerprint is only honest if the prose
  is really theirs.

## Cold-start handling

If `mine.cold_start` is true (the reader had little/no pre-AI writing): build the
bundle from the interview + gauntlet, and **mark the generated SKILL.md
outline-grade** at the top — state plainly that it will sharpen as they add real
samples through `/voiceprint-refine`. Do not present an outline as a finished voice.

## References

- `references/synthesis-method.md`: the placeholder-fill playbook, worked
  evidence→bundle examples, the samples-win wiring, and the analyzer-shape rules.
- `templates/`: the four parameterized templates.

## Success Criteria

- [ ] Every voice claim in the bundle is backed by a verbatim quote.
- [ ] The generated SKILL.md carries the samples-win statement.
- [ ] Signature moves and anti-patterns cite the reader's own evidence.
- [ ] The universal anti-slop spine is present, framed generically.
- [ ] `voice-samples.md` is analyzer-ready (one passage per heading, verbatim).
- [ ] No placeholders left; no invented content; thin evidence flagged honestly.
- [ ] Zero content from any other person's voice skill.
