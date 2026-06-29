---
title: Field report — fusion-discovery-council D4 (whitespace map as hero output)
date: 2026-06-29
branch: feat/discovery-d4-whitespace-hero
roadmap_item: D4 (Step B)
spec: docs/superpowers/specs/2026-06-29-discovery-d4-whitespace-hero-design.md
plan: docs/superpowers/plans/2026-06-29-discovery-d4-whitespace-hero.md
research: vault/20_projects/research/2026-06-29-whitespace-gap-map-presentation-research.md
---

# D4 — Whitespace Map as hero output

## What shipped

The blind-spot/whitespace map now **leads** both discovery ledgers (pm + substack) instead of
rendering last as bare `- {b}` bullets. Each gap renders as a statement + a uniform
`→ Backfill (agent WebSearch/WebFetch, solution-side)` next-action, under a deterministic
**"Sharpen the next run"** list (4 conditional rules: backfill the N gaps · add `--segment` if unset
· reframe if 0 verified · raise tier when drop-rate ≥50% and not already `deep`). New
`council/discovery/whitespace.py` holds the one shared `whitespace_hero()` helper both renderers
call (DRY); `$0`/deterministic, no model call. Honesty-preserving: gaps are framed as
absence-of-evidence, never verified claims; the action is always *investigate*, never *build*; no
fabricated score on a gap.

7 commits, **212 passed / 1 skipped** (was 195 + 17 new whitespace/pipeline tests), repo validator
passes.

## The defining move (again): research before locking the shape

Per the standing practice, I ran a **$0 deep-research pass** on gap-map presentation/actionability
*before* designing the section. It changed the design in three concrete ways:

1. **It made the central guardrail obvious.** Peer-reviewed sources on absence-of-evidence ≠
   evidence-of-absence (PMC10065758) said an unstudied gap must route to "investigate," never
   "build/discard." Our whitespace map is *by construction* absence-of-evidence (what the panel
   missed), so the per-gap action is **always backfill** — and that's honest, not a limitation. This
   is the thing I'd most likely have gotten subtly wrong from first principles (I'd have been tempted
   to frame gaps as "opportunities to build").
2. **It validated the cap + lead-with-recommendations shape** (Torres "prioritize opportunities";
   Infomineo "lead with recommendations, cap at 3–5") — so the "Sharpen the next run" list leads and
   stays short.
3. **It killed false precision** (OrgVitality) — confirming we must *not* attach a confidence number
   to a gap (it has no supporting evidence by definition). Gaps stay qualitative.

One $0 pass, three better/safer decisions. The exemplar pattern (PM4) held.

## Process notes / friction

- **The deep-research workflow failed at the Verify phase** (transient Anthropic-side rate-limiting
  during the ~44-agent adversarial-verify burst), which aborted synthesis. Rather than re-run the
  whole 2.5M-token workflow into the same rate limit, I **salvaged** the completed extractor +
  verifier transcripts (the verification had largely *succeeded* — the two highest-stakes guardrails
  carried clean 3-0 verdicts) and hand-vetted them into the research note. Lesson: the deep-research
  harness's verify fan-out can self-trip rate limits; salvage-from-transcripts is a viable $0
  recovery when the question is presentation/best-practice (lower-stakes than a load-bearing
  formula). For a higher-stakes question I'd resume the workflow instead.
- **Brainstormed the shape one question at a time** (3 AskUserQuestion rounds): actionability shape
  (per-gap action + global list, not keyword classification), supplement cohesion (link by reference
  — lowest-risk, no change to the gate-adjacent `verify_supplement.py`), and the drop-rate threshold
  (≥50%). All three locked cleanly.
- **The final adversarial review (Opus, 8/10) earned its keep:** it caught a real Important bug — the
  empty-bundle early-return in `pipeline.py` rendered the hero without `segment=`, so the
  "Add `--segment`" rule could fire even when the user *did* pass a segment that gathered nothing. A
  one-line fix + 3 guard tests. The honesty gate, scope guard, DRY, and byte-identical invariants all
  came back confirmed clean.

## A recurring small gotcha

The hero references "**Web Supplement (gap-fill)**" by name in every per-gap action, which made
several existing `assert "Web Supplement" not in md` tests false-positive. The fix was to assert on
the **section heading** (`## Web Supplement`) instead of the bare substring — the assertions' real
intent. Worth remembering: when a new section *names* another section, substring-absence tests on
that name break.

## Vault hygiene

Sean is on the MBP (no Obsidian-Git) and is mid-audit on vault files, so per his direction this branch
contains **zero vault changes** — the research note and the D4-done ticket update are left for him to
commit separately. The branch is code + `docs/` + SKILL.md + CHANGELOG only.

## Carry-forward (next PR)

- The PM4 carry-forward nits (scoring `src{i}` vs `author{i}` fixture rename + the source/domain
  asymmetry seam test) were out of D4's scope — still open for the next relevant PR.
- Remaining Step B: **E3** (MMR dedup + recency/reach decay — would let us genuinely *rank* gaps,
  removing the "panel order, no rank claim" limitation D4 ships with), then **D2** (receipts UI).
