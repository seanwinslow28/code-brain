# VoicePrint — fresh-session continuation prompt

> Paste everything below the line into a new Cowork session. It is self-contained.

---

# Project: Build VoicePrint — a Cowork plugin that gives any reader their own personal voice-mode skill

You are my thinking partner and builder on VoicePrint, the flagship reader tool for my Substack
series "Raising Claude." Be honest and challenge me; you are not an order-taker. Brief, direct, no
trailing summaries. Use AskUserQuestion before any multi-step work. Work in the code-brain repo:
/Users/seanwinslow/Code-Brain/code-brain/

## What VoicePrint is (the one-paragraph version)

A distributable Cowork plugin that interviews a reader and emits THEIR OWN personal
`writing-voice-modes` skill: a generated `SKILL.md` plus their three reference files (reference
universe, cheese bank, voice samples), wired together and ready to use. It productizes the exact
multi-session process I used to calibrate my own voice skill. Series logic: Post 1 gave readers the
three prompts and said "you can too"; VoicePrint is Post 2 — "I built the thing that runs the whole
process and hands you a finished skill." It is also my strongest PM portfolio artifact: taking a
validated internal workflow and shipping it as a product other people install.

## Read these first, in this order (do not skip — this is the whole context)

THE SPEC (your blueprint):
- vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-06-07-voiceprint-plugin-build-spec.md
  — the full build spec: pipeline (commands A–E + synthesis), components, outputs, MVP/post-MVP,
  effort, risks, success criteria. The decisions in §9 are now LOCKED (see below).

THE ENGINE you are productizing (read fully — the generated skill is a per-reader version of this):
- .claude/skills/writing-voice-modes/SKILL.md
- .claude/skills/writing-voice-modes/references/voice-samples.md  ← the most important reference;
  note Rounds 6 + 7 (Sean's edit-diffs) and the Raw Stories grit anchor. Exemplars beat rules.
- .claude/skills/writing-voice-modes/references/reference-universe.md
- .claude/skills/writing-voice-modes/references/cheese-bank.md
- .claude/skills/writing-voice-modes/references/calibration-notes.md
- .claude/skills/writing-voice-modes/drafts/2026-06-04-script-mining-report.md

THE CHAIN to bundle (decision 3 = bundle these, generic, alongside the voice skill):
- .claude/skills/storytelling-architecture/SKILL.md
- .claude/skills/substack-value-engine/SKILL.md
- .claude/skills/writing-critique/SKILL.md
- .claude/skills/writing-humanity-pass/SKILL.md
  (Note: writing-humanity-pass has Sean-specific allowlist content; the bundled version must be
  de-Sean'd / parameterized to the reader's signature moves.)

THE MANUAL VERSION OF THE TOOL (what VoicePrint automates):
- vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/raising-claude-cheese-gauntlet-kit-PUBLIC.md
  — the 3 copy-paste prompts (reference-universe interview, Cheese Gauntlet, mine-your-pre-AI-writing).
  VoicePrint turns these into adaptive, stateful commands that end in a generated skill bundle.
- vault/.../substack-drafts/2026-06-05-raising-claude-post1.md  — Post 1, the thesis.

PROOF THE METHOD WORKS (the validation A/B):
- docs/MEANING_OVER_ACCESS.md  — labeled cheese specimen ("try-hard Hunter Thompson").
- voice-samples.md Round 7  — the upgraded skill rewrote it clean; Sean's edits graduated the skill.

HOW TO BUILD A COWORK PLUGIN:
- Invoke/read the `create-cowork-plugin` skill (cowork-plugin-management plugin) for the plugin
  architecture (.claude-plugin/plugin.json, commands/, skills/), the five-phase workflow, the
  component schemas, and the .plugin packaging step. Also `skill-system-mastery` for SKILL.md craft.

## The method doctrine (these lessons ARE the product's design guardrails — hold to them)

1. EXEMPLAR-FIRST, NEVER DISTILLATION. The tool collects EVIDENCE (real writing, real reactions),
   never "describe your voice." A description = adjectives that fit half the planet. This is the
   single failure that killed v1 of my own skill; if VoicePrint's synthesis paraphrases instead of
   quoting the reader's verbatim samples/reactions, every reader gets the same bland skill. This is
   risk #1.
2. REACTIONS OVER DESCRIPTIONS. The Cheese Gauntlet weaponizes disgust — readers can't describe
   their voice but spot what ISN'T it instantly. The "no" draws the outline.
3. HOURS, NOT ONE-SHOT. Build the honest expectation in: session one is a sharper outline, the tenth
   sounds like them. The refine loop (E) is how the skill gets good; don't promise magic.
4. THE READER'S EDIT-DIFFS ARE THE CALIBRATION DATA. The refine loop must capture the diff between
   what the generated skill writes and what the reader changes, and feed it back. First-class feature.
5. EACH READER FROM SCRATCH — ZERO SEAN LEAKAGE. The generated bundle must contain none of my
   content (my reference universe, my cheese bank, my stories). Templates carry STRUCTURE; all
   content is elicited from the reader. The dogfood step exists to catch leakage.
6. LOCAL + PRIVATE. All elicited writing/reactions/outputs stay in the reader's workspace. Say so;
   it's a trust feature for "paste me your old writing." The plugin must NOT require the reader to
   have an Anthropic API key — it runs in their Cowork session on their subscription.

## Decisions LOCKED (Sean, 2026-06-07)

1. NAME: **VoicePrint**.
2. SCOPE: build the BEST plugin possible — ship A/B/C/D/E (all five: interview, gauntlet, mine,
   synthesis, refine loop) AND propose+add anything else you think makes it better during planning.
   Max ambition, not MVP-minimal.
3. BUNDLE THE UPSTREAM CHAIN: include generic storytelling-architecture + substack-value-engine +
   writing-critique + writing-humanity-pass so the reader gets the whole pipeline, not just voice.
4. HARDEN FIRST: build it generic/external-ready, but the rollout plan is dogfood on a few real
   humans (non-Sean) before opening it publicly. Bake a validation/dogfood phase into the plan.

## Your task

1. FIRST, produce a detailed EXECUTION PLAN (use plan mode). The plan should cover: the full plugin
   component breakdown (plugin.json, the five commands, the synthesis skill, the bundled chain skills,
   the parameterized SKILL.md template + the three reference-file templates); the design of each
   adaptive interview (the hard part — pushing on generic answers like a real interviewer, not a
   static questionnaire); how interview state/transcripts are stored between turns; the
   reaction-capture UX for the gauntlet; the refine-loop diff capture; the de-Sean'ing of the bundled
   humanity-pass; the dogfood-on-non-Sean validation phase; and packaging to a .plugin. Sequence it
   into buildable chunks with checkpoints. Surface any additions you recommend (decision 2 invites them).
2. Get my approval on the plan (ExitPlanMode / AskUserQuestion at decision points). Do not build the
   whole thing before I see the plan.
3. THEN build incrementally, checking in between chunks. Run `claude plugin validate` and dogfood as
   you go. Deliver the installable `.plugin` file at the end.

## Success criteria (from spec §10)

- A stranger runs the interviews and gets a SKILL.md that sounds like THEM, not a template, on the
  first pass.
- The generated bundle contains zero Sean-specific content.
- It sets the "hours, not one-shot" expectation honestly.
- Re-running the refine loop measurably sharpens the voice (the reader's edit-diffs shrink).
- Post 2 can credibly say "install this and start your own pile this weekend."

## Repo conventions

- Append to CHANGELOG.md on every change. Capture deferred work as one-line bullets under `## Todo`
  in vault/00_inbox/tickets.md. NEVER git-commit the vault (Obsidian-Git owns it).
- Decide with me where the plugin SOURCE lives (likely a new dir under code-brain, e.g.
  `creative-studio/` or a dedicated `voiceprint/` project dir) vs the packaged `.plugin` (outputs).
- Cost-safety: if any tooling you build calls models directly, route through the Claude subscription
  (Agent SDK / OAuth), never an Anthropic API key. I keep no API key on this machine.

## How to behave

Thinking partner, not executor. Honest pushback expected. Plan before building. Exemplar-first is
the whole game — if a design step starts summarizing voice into rules instead of capturing evidence,
stop and fix it. The genericness trap is the enemy; the dogfood-on-a-real-human test is how you know
you beat it. Start by reading the files above (spec first), then propose the execution plan.
