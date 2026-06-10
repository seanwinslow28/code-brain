# VoicePrint

**A plugin that hands you your own writing voice as a reusable skill.**

Most "write like me" tools do the same thing: feed them 10 old posts, they *analyze* your writing and hand back a description, and you paste that description back into the model. It works until you hit the wall every one of them hits — *you can't write down what you don't know you're doing*, and you can't analyze a voice you haven't written down yet.

VoicePrint starts from the opposite end. Before it looks at anything you've written, it generates writing you'll **hate** — in your name, in the register that makes you cringe — and lets your gut reaction draw the outline. (You can't describe your voice, but you can spot what *isn't* it instantly.) Then it maps the references you actually quote and mines whatever real writing you do have. Three kinds of evidence — what you reject, what you love, how you actually build a sentence — quoted back to you, never paraphrased into adjectives.

It productizes the exact process behind the "Raising Claude" Cheese Gauntlet kit: three elicitation sessions, a synthesis step, and a calibration loop you re-run until the voice is yours.

## What makes it different

- **It learns you from what you reject, not just what you've written.** The Cheese Gauntlet (your disgust as signal) is the part no other voice tool does.
- **It works even if you have no corpus.** Most tools need 10+ samples to get good. VoicePrint's interview + gauntlet produce real signal from zero — and tell you honestly when the result is still outline-grade.
- **It proves it's converging instead of promising magic.** No "80% on the first pass." The refine loop measures your edit-diffs shrinking over rounds, locally.
- **Local, free, no account, no upload, no API key.** Your writing never leaves your machine. Nothing to connect, nothing to trust with your data.

## The honest expectation

This is **not** a one-shot. One session gets you a sharper outline. The tenth gets you something that sounds like you wrote it. VoicePrint builds the loop in on purpose — it's reps, not a magic prompt. Same as raising anything.

## Local and private

Everything you paste — old writing, reactions, transcripts — stays in your workspace as plain files. Nothing is uploaded anywhere by the plugin. That guarantee is the whole reason "paste me your old writing" is a safe ask.

No API key required. VoicePrint runs entirely in your Cowork session on your own subscription.

## What you do (the flow)

| Step | Command | What happens |
|---|---|---|
| Start here | `/voiceprint-start` | Sets expectations, explains the flow, sets up your workspace |
| A | `/voiceprint-interview` | Maps your real cultural taste, one question at a time, pushing past generic answers |
| B | `/voiceprint-gauntlet` | Generates 10 lines in the register you most hate, in your name; your disgust draws the outline |
| C | `/voiceprint-mine` | You paste pre-AI writing; it extracts how you actually build a sentence, quoting you back |
| D | `/voiceprint-synthesize` | Reads your three reference files and generates your personal voice skill bundle |
| E | `/voiceprint-refine` | Generates a sample in your voice, captures your edits, feeds the diff back. Re-run often. |

Do A, B, C in order before D. The gauntlet tells the model what you're *not*; the other two tell it what you *are*. You want all three.

## What you walk away with

```
voiceprint/
└── my-voice/                       # your installable voice skill
    ├── SKILL.md                    # your modes, signature moves, anti-patterns, dial
    └── references/
        ├── reference-universe.md   # your cultural library (from the interview)
        ├── cheese-bank.md          # the registers you reject (from the gauntlet)
        └── voice-samples.md        # how you build a sentence + your refine diffs
```

Drop `my-voice/` into your own Claude skills folder and write in your voice anywhere.

## Components

- **6 commands** — `voiceprint-start`, `-interview`, `-gauntlet`, `-mine`, `-synthesize`, `-refine`
- **2 core skills** — `voiceprint-interviewing` (the interview craft), `voiceprint-synthesis` (the generator)
- **4 bundled writing skills** — `storytelling-architecture`, `substack-value-engine`, `writing-critique`, `writing-humanity-pass` (generic, so you get the whole pipeline, not just voice)
- **2 scripts** — `diff_metrics.py` (refine-loop edit measurement), `pile_state.py` (workspace state)

## Setup

Install the plugin, open a folder in Cowork, and run `/voiceprint-start`. That's it.

## Credits

Built from the method in the "Raising Claude" series. The bundled `writing-critique` and `writing-humanity-pass` skills adapt, respectively, `haowjy/creative-writing-skills` (Apache 2.0) and `blader/humanizer` (MIT). Attribution retained in each skill.
