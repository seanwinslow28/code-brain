---
title: "Pencil & Prompt Revamp — Session Map"
type: plan
status: active
created: 2026-08-05
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, relaunch, session-map]
ai-context: "The working order for the full Substack revamp, produced at the close of the 2026-08-04/05 partner session (sidecar ~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md, locks L1-L7). Each session below has a paste-ready kickoff prompt. Sessions read the sidecar for decisions and this map for order. The L6/L7 territory set stays a LOOSE lock until real posts prove the value — build sessions may surface reshapes; route them back to a partner-session reconvene, never silently."
---

# Pencil & Prompt Revamp — Session Map

**The locked shape (plain terms):** Pencil & Prompt stays the name. The claim: models got good, everything they make is the same — this publication runs real experiments that push AI past the average and publishes the verdicts, including the failures. Weekly experiment series = **Building the Ladder** (numbered rungs). Funny-true-story series = **Raising Agents**. The product underneath = a public, versioned mechanism library where every entry carries a tested verdict (beat / tied / lost, public retractions). Full decisions + reasons: the sidecar (locks L1–L7).

**Standing rules for every session here:** substack-studio CLAUDE.md governs (voice chain mandatory, no em dashes, anti-hype, value gate, privacy rules). Sean hand-rewrites every chain draft. Notes practice runs continuously from today — it does not wait for any session below.

---

## S0 — Sourdough dark start (TODAY; ~1 hr; $0; private)

Starts the clock on the months-long experiment. Nothing publishes.

> **Kickoff:** Set up the Pencil & Prompt "sourdough" collaborator per lock L7 (dark start) in the sidecar at `~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md`. Design and create: (1) a private home for the aged collaborator's memory — local-only, NEVER in the public repo (candidate: a gitignored dir or under `~/.creative-harness/sourdough/`); (2) a memory file schema (what it accumulates: rejected drafts, Sean's corrections, house-style rules, its own mistakes); (3) a 15-minute weekly feeding ritual Sean can actually sustain, written as a checklist; (4) a log format that timestamps every feeding so the eventual series has receipts; (5) the blind-comparison protocol sketch (same job to aged vs fresh instance at week N, judged blind). Keep it model-agnostic in design even if v1 runs on one model. Deliverable: the running setup + first feeding done in-session.

## S1 — Doc re-anchor + hygiene (next writing-free session; ~2 hrs; $0)

Every future session reads these docs first; until they're rewritten, every session boots on the dead premise. Discharges the existing "doc re-anchor" ticket.

> **Kickoff:** Run the "substack-studio doc re-anchor" ticket in `vault/00_inbox/tickets.md`. Rewrite `vault/20_projects/substack-studio/` SOUL.md (masthead: divergence thesis replaces taste-transfer; keep the honest-arc DNA), POSITIONING-AND-EDITORIAL-SPEC.md, SERIES-COMMAND-CENTER.md (formats: Building the Ladder rungs + Raising Agents episodes; Graveyard verdict policy; retire Take Two/Back to Basics as structures, note what each fed into), SKILL-PACKAGING-PLAN.md (catalog swaps from taste-transfer skills to divergence mechanisms; library-as-product answers its §6.1), and CLAUDE.md §0/§2 guardrails. Source of truth: the sidecar locks L1–L7 + the three research syntheses (`research/2026-08-05-prior-art-synthesis.md`, `research/2026-08-05-competitive-check-six-territories.md`, `research/discovery/2026-08-05-territory-pain-validation.md`). Carry the research caveats INTO the docs: the masthead claim must not lean on the weak "stickiness" number (2 studies — state it as an open question or a future rung); the precise library claim is "no prompt or technique library publishes per-entry tested verdicts against a published protocol" (broad versions are falsifiable); never use the $2.51B or 10–30x figures. Hygiene in the same pass: fix the stale discovery-cap figures ($10/day/$50/month → policy v3's $30/day/$100/month) in code-brain CLAUDE.md + the fusion-discovery-council skill doc. Subtitle wording: run the naming pass here (subtitle = plain value prop, thesis-facing).

## S2 — Theme & image pass (after S1; Mac session — image APIs; ~$2-5)

The sidecar flagged all images for review against the new theme.

> **Kickoff:** Review the Pencil & Prompt image house style (`vault/20_projects/substack-studio/playbook/image-house-style.md`, style anchors in `_assets/style-anchors/`) against the relaunched identity (sidecar locks L4/L5: keep the name; Building the Ladder + Raising Agents series; divergence thesis). Decide with Sean: does the pencil-test look survive (it fits the name and the mascot lineage — the mascots are now the Raising Agents cast), and what visual language marks the two series apart (rung numbering treatment; the ladder motif; the existing amber/teal accent split)? Then generate: masthead/banner candidates, a Building the Ladder series card, a Raising Agents series card, and hero images for the launch bundle (About, Start Here, origin-confession post). `openai-image-gen` primary. New assets to `_assets/` + per-post `images/`; superseded versions to `images/_superseded/`, never deleted.

## S3 — Pages + profile cleanup (after S1, can parallel S2; ~2-3 hrs)

The old relaunch checklist, updated — this is where the previous sessions' work gets carried, not lost.

> **Kickoff:** Execute the Pencil & Prompt relaunch surface prep. (A) PAGES: rewrite Start Here and About from the re-anchored SOUL.md (S1 must be done) — existing drafts at `pages/` are the raw material but predate the refocus AND the writing-voice-modes G1-G5 update, so treat as quarry, not base. Full writing workflow: brainstorm the shape first, then the voice chain, then Sean hand-rewrites, then fold his rewrite into voice-samples. (B) PROFILE (browser, `@seanpwins`, same account — never a new one): set the new subtitle from S1's naming pass; rewrite the bio (kill any remaining PM-recruiter voice; the new positioning is the experimenter who publishes verdicts, funny first, anti-hype); curate restacks (keep the creative-AI/animation ones, drop the PM-job-interview outlier, re-restack the best with a one-line take); unpublish (revert to draft, never delete) the 3 old live posts; build the custom homepage + launch-lean nav: Home · Start Here · Building the Ladder · About · GitHub · Portfolio — sections only get added when content exists. Sean confirms each irreversible-looking profile action before it happens.

## S4 — The origin confession (Rung 0 / launch flagship; after S1+S3 shape work)

The launch bundle = S3's pages + this post, live together.

> **Kickoff:** Write the Pencil & Prompt relaunch flagship: the origin confession. The true story, funny first: Sean preached taste-transfer, ran one GPT Image 2 test with a simple prompt + reference, and disproved his own newsletter — then found the real problem (everything the models make converges on the same average) and the real job (run the experiments, publish the verdicts, build the ladder in public). Beats end on the promise + what ships every week (rungs, episodes, the library with verdicts). Full workflow per substack-studio CLAUDE.md §8: Stage-0 preflight is substantially pre-paid by the 2026-08-05 research round (cite from the syntheses, tier-audited sources only); brainstorm the shape with Sean before drafting; full voice chain; Sean hand-rewrites. Value gate: the Itch is Sean's own dead premise (documented), the Solution artifact is the captured GPT Image 2 test itself, the Transfer is the reader's permission to distrust technique-sellers + the promise of tested verdicts. Frontmatter per SERIES-COMMAND-CENTER conventions.

## S5 — The scoreboard (protocol post + artifact; before Rung 1 — hard order, three research passes converged on this)

> **Kickoff:** Build and write the Pencil & Prompt measurement protocol — the thing the entire research round says is the actual product ("the mechanism is the commodity, the verdict is the product"; a verdict is only as credible as its published metric). (A) THE ARTIFACT: a short, versioned protocol doc — what a mechanism entry is, what beat/tied/lost mean, the baseline (the default/median run, shown), the metric (semantic diversity with the known traps from Finding 8 of `research/2026-08-05-prior-art-synthesis.md`: lexical metrics insufficient; naive embedding-cosine conflates novelty with incoherence; quality-restriction flips findings — pick something honest and defensible at solo scale, state its limits), blind judging where feasible, and the retraction rule (d10 Graveyard: losers get public retractions). Decide with Sean where the library lives (open question from the sidecar: public repo vs claude.ai skills vs plugin — the Pocock-style public repo is the research-favored lead-magnet shape). (B) THE POST: the funny-first story of why a newsletter needs a lab notebook ("everyone ships the prompt; nobody reports back" — Sean's own L7 reason is the seed), ending with the protocol as the takeaway. Full voice chain + Sean rewrite.

## S6 — Rung 1: does arguing help? (after S5)

> **Kickoff:** Run and write Building the Ladder, Rung 1: Manufactured Opposition. The experiment: does making AI argue with you actually improve the work? Baseline = the agreeable default on one real creative job (d1 instrument: run it ~20x, show the sameness grid). Contenders: the free public "disagree with me" persona prompts (the commodity), and the stakes version (an opponent with something to lose) run heterogeneously via Sean's llm-council/fusion-discovery-council infrastructure (the evidence-favored variant — homogeneous panels hit consensus collapse; cite Hegazy 2024 WITH its 2024-era-models vintage). Score against the S5 protocol; theater-detection is a named check (did the disagreement CHANGE the output, or just perform?). Publish the verdict whatever it is; failures per the Graveyard policy. Ship the mechanism both tiers (copy-paste + installable skill) into the library with its verdict attached. Full voice chain + Sean rewrite. NOTE: if any claim needs the contaminated T3 pain evidence, run the reframed ~$1.50 discovery re-run first (sidecar L7 gate) — otherwise it is not needed for this rung.

## Ongoing / parallel

- **Notes, starting today.** No session needed. First candidates: the two-isolated-AIs-wrote-the-same-three-examples anecdote (the thesis in one story); the em-dash-as-tell irony; "the models got good and that's the problem."
- **"The Night My Vault Said Nothing" rewrite** (existing ticket) — first Raising Agents episode; needs current voice modes; publishes after the launch bundle. Any-time session after S1.
- **d4 data-hole re-run** (~$1.50) — only when a data-hole draft actually starts (L7 gate).
- **Sourdough feeding** — weekly ritual from S0; the series announces itself when the first blind comparison exists.

## Carried forward from the pre-refocus sessions (verified against the old docs)

| Old item | Status in this map |
|---|---|
| Profile cleanup checklist (subtitle, bio, restacks, unpublish 3 posts, homepage/nav) | S3, updated to new positioning |
| Start Here + About drafts (2026-06-27, proven workflow) | S3 quarry — workflow survives; copy predates refocus + voice-modes update |
| Image house style (pencil-test, amber/teal) + mascot lineage | S2 review — mascots recast as the Raising Agents cast |
| Voice chain + Sean-hand-rewrite + fold-back-to-voice-samples loop | Unchanged, every writing session |
| Value gate (Itch/Solution/Transfer) | Unchanged; sharpened by "verdict is the product" |
| Old back catalog (01–07, bonus, Take Two backlog) | Quarry per sidecar: incidents → Raising Agents; jobs → rung subjects; all rewrites go through current voice modes |
| Notes from day zero | Ongoing, starts now |
| Naming (Pencil & Prompt locked 2026-06-22) | Kept (L4); subtitle re-cut in S1 |
