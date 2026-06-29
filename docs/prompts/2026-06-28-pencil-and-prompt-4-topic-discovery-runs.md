# Claude Code prompt — 4 Pencil & Prompt discovery runs (+ first live BACKFILL dogfood)

Paste the fenced block into a **Claude Code session opened in `code-brain`**. Everything outside the fence is context for you (Sean).

## Why this run

Two birds: (1) mine **fresh Pencil & Prompt post topics** from four *unmined journey stages* — every prior substack run sat at "generate output / keep my style"; these four hit the stages that publication's reader actually churns on; (2) **dogfood Stage-5 BACKFILL** for the first time on real topics (you built + merged it today; the tests were stubbed, so this is the first live exercise of the auto web-supplement).

The four topics (from the 2026-06-28 journey-map whitespace pass):
- **T1 — iteration tax** (the skeptic's #1 rational objection; cost/time axis)
- **T2 — accused of AI / legitimacy** (human/social axis; Fronkenschteen fuel)
- **T3 — the bounce & re-entry** (P&P's exact reader — framed on the quit/re-entry decision, not soulless-output, to avoid overlapping the 06-22 run). **Run at DEEP tier** — thinnest-evidence + highest-strategy topic, where deep's `sonar-deep-research` + 6-model panel hedge the drop-rate risk
- **T4 — the slot-machine / reproducibility** (reliability axis; your most differentiated answer)

**Cost:** three standard substack runs (~$1.10–1.65 each) + one deep T3 run (cap $4, historically ~$1–3 with variance) → ~$4–8 total, under the $10/day discovery cap. BACKFILL adds only a few tier-capped web queries (~$0.05/run). The deep run normally pauses for an interactive cost confirm — its command includes `--yes` because you've authorized it. If earlier discovery spend already landed on today's spend file, a later run may be budget-rejected — that's the guardrail working; resume tomorrow.

---

```
TASK: Run FOUR fusion-discovery-council substack-lens discovery runs to mine fresh Pencil & Prompt
post topics, AND dogfood the new Stage-5 BACKFILL (its first live use on real topics).

READ FIRST:
- .claude/skills/fusion-discovery-council/SKILL.md — the skill contract. Pay attention to §0
  (paths), §3 (flags), §4 (exact CLI invocation), §5 (cost discipline + the $10/day cap), §6 (the
  verification gate, now also governing the supplement), §7 (NEVER git add/commit the vault).

HOW TO RUN: substack lens, --supplement left DEFAULT ON (so BACKFILL fires — that is the dogfood).
Tiers: STANDARD for T1/T2/T4, DEEP for T3 (thinnest evidence + priority topic; deep's
sonar-deep-research + 6-model panel + BACKFILL-cap-6 are the hedge). The deep run normally PAUSES for
an interactive cost confirm (cap $4) — Sean pre-authorized it, so its command includes --yes. Run them
ONE AT A TIME from the CLI working dir, and do the DEEP T3 run FIRST (priority + largest single cost),
then the three standard runs. After each, capture the printed "Verified ideas: N · dropped: M · $X.XX"
line and keep a running daily total. The CLI enforces $10/day against ACTUAL spend — if any run prints
"Budget rejected", STOP, report what completed, and do NOT pass --force or raise tiers beyond those
specified. We resume the rest tomorrow.

  cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council

RUN 1 — T1 (iteration tax):
  uv run python -m council.discovery \
    "creative professionals who spend more time fixing, re-rolling, and cleaning up AI-generated output than the tools actually save them" \
    --lens substack --tier standard \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-ai-iteration-tax-substack-idea-ledger.md

RUN 2 — T2 (accused of AI / legitimacy):
  uv run python -m council.discovery \
    "artists, illustrators, and writers being falsely accused of using AI, or afraid to disclose their AI use, and the trust and legitimacy fallout they face" \
    --lens substack --tier standard \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-accused-of-ai-legitimacy-substack-idea-ledger.md

RUN 3 — T3 (the bounce & re-entry — frame on the QUIT/RE-ENTRY decision) — DEEP TIER, run this one FIRST:
  uv run python -m council.discovery \
    "skeptical creatives who tried AI tools, got generic soulless results, and quit — why they abandoned it and what would make them give it another chance" \
    --lens substack --tier deep --yes \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-skeptics-quit-ai-re-entry-substack-idea-ledger.md

RUN 4 — T4 (the slot-machine / reproducibility):
  uv run python -m council.discovery \
    "creatives who cannot get AI tools to produce the same quality result twice and struggle to build a repeatable creative process they can trust" \
    --lens substack --tier standard \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-ai-reproducibility-slot-machine-substack-idea-ledger.md

(Each run also writes a sibling ...-substack-brief.md, per SKILL.md §4.)

=== DOGFOOD CHECK (the reason this is also a test — do this per run) ===
After each run completes, open the new "## Web Supplement (gap-fill)" section in its ledger and note:
  - Did BACKFILL fire? (section present, NOT "supplement skipped: no web-search key configured")
  - Gap-fill rate: how many blind spots came back "filled" vs "still open".
  - Relevance eyeball (the one un-vetted risk): for 2-3 filled items, does the quote actually ADDRESS
    the gap, or is it on-keyword but off-topic? (This is the §9 "supplement relevance" read — the
    thing E1's entailment upgrade will later vet.)
  - Confirm supplement findings are in their OWN section and were NOT mixed into the ranked angles.

=== REPORT BACK (one compact table across the 4 runs) ===
Columns: Topic | Verified angles | Dropped | Cost | Gap-fill (filled/total) | Relevance (good/mixed/poor)
         | Highest-signal pain point (1 line) | Sharpest line from the blind-spot/whitespace map (next-topic fuel)
Then: total spend vs the $10/day cap, and a 2-3 sentence read on whether BACKFILL is pulling its weight
on real topics (worth keeping default-on, or any tuning needed).

=== DO NOT ===
- git add / git commit anything under vault/ — Obsidian-Git owns vault commits (code-brain CLAUDE.md
  rule 8). Just write the ledgers + briefs and stop.
- --force, raise tiers beyond those specified (T3 is intentionally deep), or retry a budget-rejected run. Stop and report instead.
- run image generation or any unrelated work.

=== OPTIONAL SHARPEN ===
Only if a run's evidence clearly skews to the WRONG audience (e.g. software developers' AI complaints
instead of creatives'), re-run THAT one with --segment "creative professionals" and note that you did.
```

---

## After Claude Code finishes

You'll have four new ledgers + briefs in `substack-studio/research/discovery/` and a compact comparison table. Next moves from there: fold the strongest verified pain into `SERIES-COMMAND-CENTER.md` (the Take Two / Fronkenschteen backlog + the discovery-angle map), and the BACKFILL dogfood read tells us whether E6 is production-solid on real topics. (Separately still on deck: the panel-vs-single-model test — red-team #4 — before any panel/E2 work.)
