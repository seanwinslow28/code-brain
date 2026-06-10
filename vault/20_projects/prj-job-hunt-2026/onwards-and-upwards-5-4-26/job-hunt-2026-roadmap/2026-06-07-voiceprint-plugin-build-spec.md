---
type: build-spec
project: prj-job-hunt-2026
series: raising-claude
artifact: reader-tool-plugin
status: spec-for-review (do not build yet)
created: 2026-06-07
working_name: VoicePrint
---

# VoicePrint — Build Spec (the post-2 flagship reader tool)

> **Status: SPEC ONLY.** This scopes the tool and estimates effort. Nothing gets built until Sean approves the shape. Working name `VoicePrint`; naming is an open decision (§9).

## 1. What it is

A Cowork plugin that interviews a reader and emits **their own** personal `writing-voice-modes` skill: a generated `SKILL.md` plus the three reference files (their reference universe, their cheese bank, their voice samples), wired together and ready to drop into Claude. It productizes the exact process Sean used to calibrate his own voice skill over this multi-session project.

The series logic: **Post 1** ("You Can't Prompt Taste Into a Machine") hands readers the Cheese Gauntlet *prompts* and says "you can too." **Post 2** says "I got tired of telling people to copy-paste three prompts, so I built the thing that runs the whole process and hands you a finished skill." The kit was the teaser; this is the product. A series becomes a destination when the reader leaves with a tool, not a pep talk.

It is also, in PM terms, the strongest possible portfolio artifact: taking a validated internal workflow and turning it into a shippable product other people can install. That signal lands on its own, no ask attached.

## 2. The core insight it productizes (the design principles ARE the lessons)

Everything this project learned becomes a product guardrail. These are non-negotiable or the tool ships the same slop the manual skill started as:

1. **Exemplar-first, never distillation.** The tool must collect EVIDENCE (real writing, real reactions), not ask "describe your voice." A description produces a paragraph of adjectives that fits half the planet; the generated skill must be built from samples and reactions.
2. **Reactions over descriptions.** The Cheese Gauntlet weaponizes disgust: the reader can't describe their voice but can spot what *isn't* it instantly. The "no" draws the outline.
3. **Hours, not one-shot.** The tool sets the expectation honestly: the first run is a sharper outline, the tenth is something that sounds like you. It builds the calibration loop in rather than promising a magic one-shot (the post-1 thesis, enforced in the product).
4. **The reader's edit-diffs are the calibration data.** The refine loop captures the diff between what the generated skill writes and what the reader changes, and feeds it back. First-class feature, not an afterthought.
5. **Each reader is from scratch.** The generated references must be the READER's (their reference universe, their cheese bank). The tool must never leak Sean's library into someone else's skill. Templates carry structure; content is 100% elicited.

## 3. Form factor + distribution

- **A Cowork plugin** (`.plugin` file), built via the standard architecture (`.claude-plugin/plugin.json` + `commands/` + `skills/`). Distributable: post 2 links to install; the reader presses "accept" on the rich preview.
- **Generic / external-ready.** Because it's for strangers, no Sean-specific content; where it must reference tooling categories, use the `~~category` placeholder pattern + a `CONNECTORS.md`. (It mostly needs none — it operates on the reader's pasted text and the workspace.)
- **Local + private.** All elicited writing, reactions, and generated files live in the reader's workspace. Nothing leaves their machine. Say so in the README; it's a trust feature for "paste me your old writing."

## 4. The pipeline (four commands + a synthesis skill)

Mirrors Sean's process and the existing Cheese Gauntlet kit, but automated, stateful, and ending in a generated artifact.

| Step | Component | What it does | Emits |
|---|---|---|---|
| A | `/voiceprint-interview` (command) | The reference-universe interview: one question at a time, deep-not-wide, pushes on generic answers. Adaptive, not a static list. | `references/reference-universe.md` (the reader's) |
| B | `/voiceprint-gauntlet` (command) | Generates 10 deliberately-bad lines in the reader's most-hated register on a topic they'd actually write about; captures fast, blunt reactions; turns disgust into a labeled cheese bank. | `references/cheese-bank.md` |
| C | `/voiceprint-mine` (command) | Reader pastes pre-AI writing; the tool extracts signature moves, sentence mechanics, opener/closer habits, sincerity-vs-deflection patterns, quoting them back as evidence. | `references/voice-samples.md` + a signature-move list |
| D | `voiceprint-synthesis` (skill) | Reads the three reference files and generates the reader's personalized `writing-voice-modes` `SKILL.md` from a parameterized template, wired to their references. | the reader's complete voice-skill bundle |
| E | `/voiceprint-refine` (command) | The calibration loop: generate a sample in the reader's voice, capture their reaction/edit, append the diff to their voice-samples, regenerate. Run repeatedly. | updated `voice-samples.md` (the diffs) |

**Cold-start handling (Step C):** readers who think they have no pre-AI writing get a fallback — old texts, emails, a journal, social posts, anything provably theirs from before LLMs. If genuinely nothing exists, the tool leans harder on A + B and flags the skill as "outline-grade until you feed it real samples."

## 5. What it outputs (the reader's bundle)

A self-contained skill directory the reader can use immediately:

```
my-voice/
├── SKILL.md                      # generated from template: their modes, dial, signature moves, anti-patterns
└── references/
    ├── reference-universe.md      # from /voiceprint-interview
    ├── cheese-bank.md             # from /voiceprint-gauntlet
    └── voice-samples.md           # from /voiceprint-mine + /voiceprint-refine diffs
```

The generated `SKILL.md` inherits the *structure* validated here (House Style/grit register elicited per-reader, Professional Dial, signature-move table, anti-patterns including the lexical-repetition and reference-governor rules, a Do-Not-Promote section the reader fills in) but every value is theirs. The four anti-slop rules this project discovered (distillation trap, reference gorging, limp deflation, grit-by-substitution) ship as the template's spine because they're not Sean-specific — they're how voice survives generation for anyone.

## 6. MVP vs post-MVP

- **MVP:** the plugin scaffold + commands A, B, C + the synthesis skill D. A reader can run three sessions and walk away with a generated voice skill. (E documented as a manual loop.)
- **Post-MVP:** `/voiceprint-refine` (E) as a polished recurring command; a "voice report card" that scores the generated skill against the reader's own gauntlet reactions; optional bundling of the generic upstream chain (storytelling-architecture / value-engine / humanity-pass) so the reader gets the whole pipeline, not just voice.
- **Explicitly OUT (for now):** the autoresearch eval harness / `skill_optimizer`. That's Sean's power-user apparatus; a reader tool does not need a 25-iteration Opus optimization loop. Mention it in post 2 as "how I tune mine," not as part of the product.

## 7. Rough effort estimate

Ranges, assuming focused build sessions; the prompt-engineering of the interviews is the real work, not the plumbing.

| Chunk | Effort |
|---|---|
| Plugin scaffold + `plugin.json` + README + packaging | ~0.5 session |
| Commands A/B/C (adaptive interview + gauntlet + mining flows) | ~2–3 sessions (prompt design + state/file capture is the hard part) |
| Synthesis skill D + the parameterized `SKILL.md` template | ~1–2 sessions |
| Dogfood on a NON-Sean person (validates it builds a real voice, not a generic one) | ~1 session |
| **MVP total** | **~4–6 sessions (~2–4 focused days)** |
| Post-MVP (refine loop, report card, chain bundling, marketplace polish) | **+~1–2 weeks** |

The single biggest effort risk is making the interviews *adaptive* (pushing on generic answers the way a good interviewer does) rather than a static questionnaire. That's where the quality lives and where the time goes.

## 8. Risks & guardrails

- **The genericness trap (the one that killed v1 of Sean's skill).** If the synthesis step summarizes instead of quoting, every reader gets the same bland skill. Mitigation: the template must carry the reader's verbatim samples and reactions, and the synthesis must quote evidence, never paraphrase it into rules.
- **Quality variance / expectation-setting.** A one-session output is an outline. The tool must say so up front (the post-1 thesis is the honesty feature), or readers feel cheated when session one isn't magic.
- **Privacy.** "Paste me your old writing" only works if readers trust it stays local. Make the local-only guarantee explicit.
- **Reader ≠ Sean.** Zero Sean content in any generated bundle. The dogfood-on-someone-else step exists to catch leakage.
- **Reaction capture UX.** The gauntlet only works if reactions are fast and blunt; the command must coach "one or two words, before the polite part of your brain shows up."

## 9. Decisions — LOCKED (Sean, 2026-06-07)

1. **Name: VoicePrint.**
2. **Scope: best-possible, not MVP-minimal.** Ship all five (A/B/C/D/E) + anything the build session deems worth adding. (Supersedes §6's MVP/post-MVP split — treat post-MVP items as in-scope; the eval/autoresearch harness stays out.)
3. **Bundle the upstream chain** (generic storytelling-architecture / value-engine / writing-critique / humanity-pass) so readers get the whole pipeline. The bundled humanity-pass must be de-Sean'd / parameterized to the reader's signature moves.
4. **Harden first.** Build it generic/external-ready, but dogfood on a few real (non-Sean) humans before opening it publicly. A validation/dogfood phase is part of the build plan.

Execution continuation prompt for a fresh build session: [`2026-06-07-voiceprint-continuation-prompt.md`](2026-06-07-voiceprint-continuation-prompt.md).

## 10. Success criteria

- [ ] A stranger runs A/B/C and gets a `SKILL.md` that sounds like *them*, not a template, on the first pass.
- [ ] The generated bundle contains zero Sean-specific content.
- [ ] The output sets the "hours, not one-shot" expectation honestly.
- [ ] Re-running the refine loop measurably sharpens the voice (the reader's edit-diffs shrink over sessions).
- [ ] Post 2 can credibly say "install this and start your own pile this weekend."
