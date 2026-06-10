# VoicePrint — Build Plan (approved 2026-06-08)

The approved execution plan, living with the code. Source spec:
`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-06-07-voiceprint-plugin-build-spec.md`.

## What VoicePrint is

A Cowork plugin that interviews a reader and emits **their own** personal
writing-voice skill — a generated `SKILL.md` plus three reference files (their
reference universe, cheese bank, voice samples) — wired together and ready to
use. It productizes the Cheese Gauntlet method from the "Raising Claude" series.

## The method doctrine (design guardrails — non-negotiable)

1. **Exemplar-first, never distillation.** Collect evidence (real writing, real
   reactions), never "describe your voice." Synthesis QUOTES evidence; it never
   paraphrases voice into adjectives. This is risk #1 — the failure that produces
   one bland skill for everyone.
2. **Reactions over descriptions.** The gauntlet weaponizes disgust; the "no"
   draws the outline.
3. **Hours, not one-shot.** Set the expectation honestly; build the refine loop in.
4. **The reader's edit-diffs are the calibration data.** The refine loop captures
   the diff and feeds it back. First-class, instrumented.
5. **Each reader from scratch — zero Sean leakage.** Templates carry STRUCTURE;
   all content is elicited. The dogfood exists to catch leakage.
6. **Local + private, no API key.** Everything stays in the reader's workspace;
   everything model-facing runs in their Cowork subscription.

## Locked decisions (Sean, 2026-06-08)

- **Source location:** `creative-studio/voiceprint/` (packaged `.plugin` → outputs).
- **Add-ons beyond A–E:** onboarding `/voiceprint-start` + a generated progress
  dashboard. (Voice report card + `/voiceprint-status` deferred to a ticket.)
- **Refine loop:** instrumented edit-diff metrics (stdlib `diff_metrics.py`).
- **No-em-dash rule does NOT ship as default** — becomes a per-reader preference.

## Architecture

```
creative-studio/voiceprint/
├── .claude-plugin/plugin.json
├── commands/
│   ├── voiceprint-start.md        # onboarding (add-on)
│   ├── voiceprint-interview.md    # A — reference-universe interview
│   ├── voiceprint-gauntlet.md     # B — cheese gauntlet
│   ├── voiceprint-mine.md         # C — mine pre-AI writing (+ cold-start fallback)
│   ├── voiceprint-synthesize.md   # D — trigger the generator
│   └── voiceprint-refine.md       # E — calibration loop (instrumented)
├── skills/
│   ├── voiceprint-interviewing/   # NEW — shared interview CRAFT (the hard part)
│   ├── voiceprint-synthesis/      # NEW — generator + parameterized templates
│   ├── storytelling-architecture/ # bundled, de-Sean'd
│   ├── substack-value-engine/     # bundled, de-Sean'd
│   ├── writing-critique/          # bundled, de-Sean'd (per-reader baseline)
│   └── writing-humanity-pass/     # bundled, de-Sean'd (allowlist→reader moves)
├── scripts/
│   ├── diff_metrics.py            # refine-loop edit-distance (stdlib only)
│   └── pile_state.py              # reads workspace, reports collection state
├── assets/                        # dashboard template bits
├── docs/                          # this plan + reader-workspace conventions
├── README.md · CHANGELOG.md · CONNECTORS.md (connector-free by design)
```

Reader workspace contract: see `reader-workspace-conventions.md`. State persists in
`voiceprint/_work/`; the deliverable lands in `voiceprint/my-voice/`.

## Three engineering decisions

1. **State between turns = files.** Commands are stateless across runs;
   `pile-state.json` is the memory.
2. **The dashboard is generated static HTML, not a live `create_artifact`.** Live
   artifacts pull from connectors; VoicePrint's data is local files. So
   `start`/`refine` bake current state into `_work/dashboard.html`.
3. **No-em-dash → reader preference** (default keep). Forcing Sean's taste would be
   exactly the leakage the dogfood catches.

## The two things that carry quality

- **`voiceprint-interviewing` skill** — the generic-answer detector (advance only on
  a named specific), the deep-not-wide follow-up ladder, the "don't make yourself
  sound cool" coaching, the gauntlet reaction-speed coaching. All three elicitation
  commands load it. This is where the spec's #1 risk gets addressed.
- **`voiceprint-synthesis` skill** — quotes the reader's verbatim evidence into the
  bundle; the template spine carries only the four UNIVERSAL anti-slop rules
  (distillation trap, reference gorging, limp deflation, register-by-substitution);
  everything else is filled from the reader's pile, with citations.

## De-Sean'ing the chain (the part the spec underweights)

- **storytelling-architecture** — nearly clean; strip Sean-named chain refs. Light.
- **substack-value-engine** — generalize "Hiring Signal (Sean's job-hunt)" →
  "credibility without pitching"; layoff suppression → reader's Do-Not-Promote list.
- **writing-critique** — analyzer stays (universal); `baseline.json` regenerates
  per-reader from their voice-samples, or runs baseline-free. Generalize dimension 5.
- **writing-humanity-pass** — allowlist binds to the reader's generated signature
  moves; em-dash rule → preference; layoff suppression → reader's Do-Not-Promote.

## Build sequence (checkpoint = stop and show Sean)

| # | Chunk | Deliverable | Checkpoint |
|---|---|---|---|
| 0 | Scaffold | tree, plugin.json, README/CHANGELOG, conventions, this plan, validate passes | tree + manifest |
| 1 | Interview craft + A/B/C | `voiceprint-interviewing` + 3 commands + state files + cold-start | walk one command live |
| 2 | Synthesis D | synthesis skill + 4 templates + `/voiceprint-synthesize`, anti-distillation | generate from a sample pile |
| 3 | Onboarding + refine + dashboard | `/voiceprint-start`, `/voiceprint-refine`, `diff_metrics.py`, `pile_state.py`, dashboard | run a refine round, watch the metric |
| 4 | Bundle + de-Sean chain | 4 chain skills copied + de-Sean'd | diff each vs canonical |
| 5 | Dogfood (stranger persona) | full pipeline as an un-Sean persona; leakage grep + genericness review; fix | show the stranger's bundle + audit |
| 6 | Package + ship | `claude plugin validate`, zip → `voiceprint.plugin`, dogfood runbook, CHANGELOGs, ticket | deliver `.plugin` |

## Guardrails held throughout

- Exemplar-first is the gate at every step; if a step summarizes voice into rules
  instead of capturing evidence, stop and fix.
- Zero Sean leakage, proven by a re-runnable grep scan over the stranger's bundle.
- No API key; scripts pure stdlib; model work runs in the reader's subscription.
- Repo conventions: voiceprint/CHANGELOG.md + code-brain CHANGELOG entry +
  creative-studio/CLAUDE.md pointer; deferred work → vault tickets; never
  git-commit the vault. Bundled skills are plugin-internal (no canonical-store
  or export-group churn).

## Research-driven changes (2026-06-08, after the market read)

Folded in after the competitive + `last30days` research (`docs/market-read.md`).
These change the product, not just the pitch:

1. **NEW keystone — the proof/eval feature (`/voiceprint-proof`).** Sean reversed
   the plan-time deprioritization of the report card. HN dismisses voice tools
   without a measurable before/after ("naive testing = no confidence"); the proof
   also answers the drift critique and the "all qualitative" jab. It combines the
   gauntlet self-check + the `writing-critique` analyzer (reader fingerprint vs a
   shipped generic-AI baseline AND the reader's own samples) + the refine-diff
   convergence trend. Spans Chunks 2/3/4. Tracked as its own task.
2. **Samples-as-binding-constraint (drift defense).** Synthesis makes the reader's
   verbatim samples the authority; rules annotate. The chain re-grounds each pass.
3. **Mining is a moat, not optional.** Grill Me owns Q&A interviews; nobody analyzes
   the user's actual writing. Emphasize `/voiceprint-mine`.
4. **Defensibility = voice + gauntlet + proof — never "interview" or "build a
   skill"** (Grill Me + Skill Creator own those). Never lead with them.
5. **Harden checkpoint-to-disk.** Interview writes per-domain, not only at the end
   (the known long-interview "misremembers earlier answers" failure).
6. **Disarm the fraud fear in onboarding.** Frame as your-voice-from-your-evidence +
   edit-your-own-drafts-faster, not faking being you.
7. **Vocabulary:** "AI slop," "taste," "voice," "sound like you" in descriptions +
   triggers. **Distribution (ticket):** ship as a `claude-plugins-community`
   marketplace repo; a one-screen before/after demo is the launch format.

## Validation reality

The in-session dogfood is a SIMULATED stranger — it proves zero-leakage and
distinct-voice (the real risk). Validation on real humans is Sean's post-build
step; Chunk 6 ships the runbook + scan to make that cheap.
