# Changelog — VoicePrint

Decision log for the VoicePrint plugin. Append on every change; capture what changed and why.

## 2026-06-08 — Chunk 6: packaged + shipped

- Packaged `voiceprint.plugin` (92.5 KB, 35 files) to the outputs folder — zips the runtime content (7 commands, 6 skills, 5 scripts + generic-AI baseline, templates, README, CONNECTORS), **excludes `dogfood/` and `docs/`** (dev evidence + internal strategy that name Sean stay in the source repo, off the installable). Removed the vestigial empty `assets/` dir.
- `docs/dogfood-runbook.md` — practical guide for Sean's real-human validation (recruit 2-3 different voices, the 7-command sitting, the two gates + the cross-person leakage check).
- Repo integration: entry in root `CHANGELOG.md` (### Added), pointer in `creative-studio/CLAUDE.md` Workspace Layout, and four deferred-work tickets in `vault/00_inbox/tickets.md` (real-human dogfood, community-marketplace repo, Post 2 launch, deferred add-ons).
- Final checks green: `claude plugin validate` passed; repo `validate.py` passed with zero voiceprint warnings; runtime content + Priya's bundle Sean-free.

**Build complete.** MVP+ scope shipped: all of A/B/C/D/E + onboarding + dashboard + the proof keystone + the de-Sean'd upstream chain. Remaining work is Sean's: real-human dogfood, the marketplace repo, and the Post 2 launch (all ticketed).

## 2026-06-08 — Chunk 5: dogfood on a stranger persona (passed + caught 2 template bugs)

- Ran a deliberately un-Sean persona (**Priya**, a gentle community-garden newsletter writer) through the whole pipeline; evidence + generated bundle at `dogfood/priya/` (excluded from the shipped `.plugin`). Report: `docs/dogfood-2026-06-08.md`.
- **Hard gates passed:** Sean-leakage grep over her bundle = CLEAN (zero markers); proof pipeline = draft `closer_to: reader` (0.69 reader / 0.57 draft / 0.39 generic-AI — honest across a very different register); dashboard/state render OK.
- **Independent subagent audit (cold, no priming):** distinctness 8/10 ("could pick Priya out of a lineup"), every move quote-grounded, zero foreign content from another writer.
- **The dogfood did its job — caught two template over-reach bugs and I fixed them in the generator (helps every future reader, not just Priya):**
  1. Professional Dial invented contextual range the corpus couldn't support → now HARD-gated in `SKILL.template.md` + `voiceprint-synthesis/SKILL.md`: build a dial ONLY with 2+ register evidence, else state honestly and omit.
  2. "Do-Not-Promote" was strategist jargon foreign to a gentle voice → renamed to "Off-limits — things to keep out," to be written in the writer's own register; references updated across the bundle.
- Re-validated: `claude plugin validate` green, runtime content Sean-free, Priya's corrected bundle clean.

## 2026-06-08 — Chunk 4: bundled + de-Sean'd the chain; proof keystone built

- Bundled four generic writing skills (`storytelling-architecture`, `substack-value-engine`, `writing-critique`, `writing-humanity-pass`) — copied only SKILL.md + useful references + the analyzer; dropped Sean's baseline corpus, evals, drafts, pycache.
- **De-Sean'd all four:** chain now points at "your generated voice skill" not `writing-voice-modes`; the writing-critique baseline is per-reader (generated from the reader's voice-samples), not Sean's; humanity-pass's allowlist binds to the reader's signature moves; **the no-em-dash hard rule became a per-reader preference** (`preferences.em_dashes`, default keep) — Sean's taste is no longer imposed; the "hiring signal" dimension generalized to "credibility signal"; layoff suppression generalized to the reader's Do-Not-Promote list; all Sean-specific worked examples replaced with generic ones.
- **Verified Sean-free:** deterministic grep over `skills/` + `commands/` for Sean markers (sean / writing-voice-modes / vault paths / project names / personal-life references) returns CLEAN. (Dev docs under `docs/` legitimately name Sean as author; the runtime content a reader's bundle is built from does not.)
- **Proof keystone (task 9) built + tested:** `scripts/fingerprint.py` wraps the bundled analyzer; `scripts/generic-ai-corpus.md` → `scripts/generic-ai-baseline.json` (burstiness 0.39, the flat target). End-to-end test on a synthetic bursty reader vs a draft: reader 1.14, draft 1.06, generic-AI 0.39 → draft `closer_to: reader`. The "more you, less generic-AI" proof works locally, no API key.
- All scripts pure-stdlib; `claude plugin validate` green; repo `validate.py` passes with zero voiceprint warnings.

## 2026-06-08 — last30days social pull merged + proof/eval keystone added

- Merged Sean's three `last30days` reports into `market-read.md` §6 + new §9 "Build changes the social pull forces."
- **Decision (Sean): build the proof/eval feature as the keystone** (`/voiceprint-proof`) — reverses the plan-time deprioritization of the report card. Tracked as a task; spans Chunks 2/3/4.
- Folded research into the plan (`docs/BUILD-PLAN.md` new "Research-driven changes" section): samples-as-binding-constraint (drift defense), mining-is-a-moat, defensibility=voice+gauntlet+proof (never "interview"/"build a skill"), harden checkpoint-to-disk, disarm the fraud fear in onboarding, vocabulary (AI slop/taste/voice), community-marketplace-repo distribution (ticket).
- **Why it matters:** the social pull aimed two guns at us — the Berkeley voice-drift finding (prompt-based skills drift) and the HN eval demand ("naive testing = no confidence"). The proof feature + samples-as-constraint answer both, and they're the most defensible things we can ship.

## 2026-06-08 — Market research + positioning sharpen

- `docs/market-read.md` — web-side competitive/demand/distribution research (deep-research shape via WebSearch + fetches; Sean's last30days social runs merge into §6).
- **Key finding:** the "write like me" category is real but crowded, and EVERY competitor (ToneClone, aiblewmymind's "Voice DNA," My Writing Twin's stylometry SaaS, content-research-writer) works from what you ARE — samples → a style *description* or a measured fingerprint. None weaponize what you REJECT. So "outputs a reusable voice skill" and "kills the AI slop" are now **table stakes**, not differentiation.
- **Differentiation (grounded):** lead with (1) the Cheese Gauntlet / reactions-over-descriptions (genuinely novel), (2) works with no corpus (cold-start; competitors need 10+ samples), (3) honest "hours not one-shot" vs. everyone's "80% on the first pass," (4) local/free/no-account/no-upload/no-key (trust + privacy in a climate where users are warned to vet plugins).
- **One competitor jab to answer:** My Writing Twin's "it's qualitative all the way down — nobody measures anything." Our answer is already in the plan: the instrumented refine-diff + the bundled `writing-critique` analyzer's per-reader burstiness/MATTR baseline = local measurement without a SaaS upload. **This makes the Chunk-4 per-reader-baseline wiring competitively load-bearing, not just nice-to-have.**
- **Distribution:** ship as a GitHub marketplace repo (`.claude-plugin/marketplace.json`) in addition to the `.plugin` file — the marketplace path is how Claude Code users discover/install; the `.plugin` is for the Cowork rich-preview. (Marketplace repo deferred to a post-build ticket.)
- Folded positioning into `README.md` (new "What makes it different" section; intro now leads with the wedge) and `plugin.json` (description + keywords: write-like-me, ai-slop, local, privacy).

## 2026-06-08 — Chunk 1: interview craft + elicitation commands A/B/C

- `skills/voiceprint-interviewing/SKILL.md` — the craft that makes the interviews adaptive, not a questionnaire. Core: collect EVIDENCE not descriptions; the generic-answer detector (advance only on a named specific); the follow-up ladder; the respectability correction; verbatim capture; saturation heuristics; gauntlet reaction-speed coaching.
- `skills/voiceprint-interviewing/references/interview-playbook.md` — depth layer: per-stage question banks, worked push examples (generic answer → the follow-up that cracked it), the gauntlet register menu, the cold-start fallback ladder, the mining extraction checklist + validation test.
- `commands/voiceprint-interview.md` (A), `voiceprint-gauntlet.md` (B), `voiceprint-mine.md` (C) — thin orchestration over the skill; each reads pile-state first, runs its stage, writes its `_work/` artifact verbatim, updates state + next_best_action.

**Why a separate interviewing skill:** all three elicitation commands share the same craft, and the craft is where quality lives (spec risk #1). Extracting it into one skill keeps the commands thin and gives a single place to harden the "push past generic answers" behavior — mirroring how the canonical voice-modes skill relates to the public Cheese Gauntlet prompts.

**Anti-distillation enforced at capture time:** commands capture verbatim and quote evidence; labels annotate, evidence leads. This is the genericness-trap mitigation starting upstream of synthesis, not just in it.

## 2026-06-08 — Chunk 0: scaffold

- Created the plugin source tree at `creative-studio/voiceprint/` (chosen home: Sean's call, 2026-06-08).
- `.claude-plugin/plugin.json` — name `voiceprint`, v0.1.0, MIT.
- `README.md` — user-facing overview, the "hours not one-shot" honesty, local/private guarantee, the 6-step flow, the output bundle shape.
- `CONNECTORS.md` — VoicePrint needs no external connectors; documents that explicitly so customizers don't expect any.
- `docs/BUILD-PLAN.md` — the approved execution plan (7 chunks, checkpoints, guardrails).
- `docs/reader-workspace-conventions.md` — the on-disk contract every command reads/writes (`voiceprint/_work/` for state, `voiceprint/my-voice/` for the deliverable).

**Why this home:** VoicePrint is a standalone shippable product but lives under `creative-studio/` per Sean's decision, grouped with the writing/creative tooling it descends from. Bundled skills are plugin-internal (NOT added to the canonical `.claude/skills` store), so there is no export-group or validator skill-count change.

**Decisions locked at plan time (2026-06-08):**
- Source location: `creative-studio/voiceprint/`.
- Scope add-ons beyond A–E: onboarding `/voiceprint-start` + a generated progress dashboard. (Voice report card and `/voiceprint-status` deferred — see vault ticket.)
- Refine loop uses instrumented edit-diff metrics (stdlib, no API key).
- The no-em-dash rule does NOT ship as a default — it becomes a per-reader preference (Sean's personal taste is not universal; shipping it would be Sean-leakage).
