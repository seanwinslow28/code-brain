# Claude Code prompt — add an automatic web-supplement (BACKFILL) stage to fusion-discovery-council

Paste the fenced block below into a **Claude Code session opened in `code-brain`**. It implements the feature, tests it, and updates the skill doc. Everything outside the fence is context for you (Sean).

## Why this change (the intent)

Today the council ends at FRAME: it produces ranked pain points plus a **blind-spot / whitespace map** that honestly lists what the evidence and panel *missed*. On the 2026-06-27 substack runs, every run's blind-spot map flagged the same holes (no proof that references/LoRA/calibration actually fix the problem; no tool head-to-head; no success cases; no quantitative data) and a human had to run a manual web-search pass afterward to fill them. This change folds that manual pass into the pipeline so **every future run leaves no blind spot un-chased**, automatically, with the same anti-fabrication discipline as the rest of the tool.

## How, in one line

Add a new **Stage 5 — BACKFILL** that runs after FRAME, turns each blind-spot bullet into a targeted web search (solution/evidence-side, not complaint-side), URL-anchors every finding, and appends a clearly-labeled **Web Supplement** section to the ledger, marking any gap it could not fill as "still open."

---

```
TASK: Add an automatic web-supplement stage ("BACKFILL", Stage 5) to the fusion-discovery-council
pipeline so every run web-searches its own blind-spot map and appends a verified gap-fill section
to the ledger. This is a real feature with tests, not a doc edit.

FIRST, read so you have the full picture:
- .claude/skills/fusion-discovery-council/SKILL.md   (the skill contract; you will update it)
- tools/llm-council/council/discovery/pipeline.py     (run_discovery orchestrator: gather→fuse→verify→frame→render)
- tools/llm-council/council/discovery/fusion.py        (FusionResult.blind_spots is the input you act on)
- tools/llm-council/council/discovery/verify.py         (the verbatim-quote-at-a-real-URL gate; mirror its philosophy)
- tools/llm-council/council/discovery/evidence.py       (EvidenceBundle / EvidenceRecord; has_url + dedup)
- tools/llm-council/council/discovery/gather/web.py      (collect_web + _simple_fetch + extract_quotes; SSRF-hardened)
- tools/llm-council/council/discovery/gather/__init__.py (READ THE COST-INTEGRITY INVARIANT docstring)
- tools/llm-council/council/discovery/render_substack.py + render.py (where ledger sections are emitted)
- tools/llm-council/council/discovery/tiers.py           (TierConfig; you add a per-tier budget field)
- tools/llm-council/council/discovery/__main__.py         (CLI flags, budget preflight, spend recording)
- tools/llm-council/tests/discovery/                       (test conventions; collectors are injectable for credential-free tests)

WORK ON A BRANCH. Use TDD: write the failing backfill test first, then implement to green.

=== WHAT TO BUILD ===

Stage 5 — BACKFILL, inserted in run_discovery() AFTER the ledger angles are framed and BEFORE render.
Input: fr.blind_spots (list[str]) + the existing EvidenceBundle (to dedup URLs) + topic + segment + tier.
Output: a structured supplement result the renderer appends as a new ledger section.

For each blind-spot bullet (up to a tier-scaled cap):
  1. Derive a SOLUTION/EVIDENCE-side search query, NOT a complaint query. The blind spots are gaps like
     "no evidence whether references/fine-tuning solve it" or "no tool head-to-head" — the fill lives in
     how-to / comparison / study content, not in more complaints. So the query targets the gap directly,
     e.g. f"{topic} {segment} {gap_phrase} 2026", after stripping leading meta-words
     ("No evidence on", "Little", "No", "Sparse", etc.) from the bullet.
  2. Run the search via the EXISTING web collector path (Exa if EXA_API_KEY, else Brave) + _simple_fetch.
     Reuse collect_web — do not write a second HTTP/SSRF path. To do this cleanly, PARAMETERIZE collect_web
     with optional `query` and `extract` overrides that default to the current behavior (so all existing
     web tests stay green). The backfill stage passes its gap-fill query and a PERMISSIVE extractor.
  3. Use a PERMISSIVE quote extractor (new helper, e.g. extract_relevant_quotes) that pulls verbatim
     sentences overlapping the query keywords — do NOT reuse the complaint-only regex (we want solutions,
     comparisons, and data, not complaints). Still verbatim, still from fetched text at a real URL.
  4. Emit EvidenceRecords tagged source_type="web-supplement", deduped against the existing bundle's URLs
     and within the supplement (reuse EvidenceBundle/_dedup_key semantics).

THE GATE (non-negotiable, mirror verify.py): a supplement item ships ONLY if its quote appears verbatim at
a real fetched URL. Never synthesize a claim that isn't a quote at a URL. A blind spot with no usable
finding is rendered as "still open — not filled," never papered over. This is the same anti-fabrication
contract as SKILL.md §6; extend §6 to say it now also governs the supplement.

FORWARD-COMPAT (roadmap item E1 — shared verification gate): do NOT inline a private copy of the
verbatim-quote-at-URL check inside the backfill stage. Call a SINGLE shared verification helper (factor one
out of verify.py if needed, e.g. `quote_supported_at_url(...)`) that BOTH verify.py and BACKFILL use — a
roadmap item (E1) will upgrade that helper from substring containment to atomic-claim + NLI entailment, and
the supplement must inherit that upgrade for free. Add a code comment noting the supplement is SAFE BY
CONSTRUCTION (deterministic extraction can't fabricate a quote that isn't on the page) but its real failure
mode is RELEVANCE — keyword-overlap can surface an on-keyword / off-topic sentence — which the E1 entailment
upgrade will later vet ("does this quote actually address the gap?"). Until E1 lands, label the Web Supplement
section as gap-fill LEADS, not consensus-verified claims. (Full rationale: the 2026-06-27 improvement idea
ledger §10 red-team + §4 item E6.)

RENDER: add a "## Web Supplement (gap-fill)" section to BOTH ledgers (render_substack.py and render.py).
Per blind spot, show: the gap, the query run, and either the found quote(s) + URL(s) or "still open."
Keep it clearly SEPARATE from the panel's ranked angles — do NOT inject web-sourced findings into the
ranked list (that would bypass FUSE consensus and destabilize scoring). Honest empty state when the whole
stage is skipped (see degradation).

CLI: add `--supplement/--no-supplement` (default ON) in __main__.py. Default-on satisfies "every run."

TIERS: add a field to TierConfig, e.g. `supplement_max_blind_spots` (quick 2, standard 4, deep 6),
1 query each, so cost stays bounded.

=== INVARIANTS YOU MUST RESPECT ===

- COST-INTEGRITY: the gather collectors are the documented $0-billing tier (Exa/Brave use their own keys,
  not OpenRouter). Keep the supplement on that rail: reuse collect_web ONLY, and do NOT add any OpenRouter/
  model call in v1 (no model query-gen, no model synthesis). Deterministic query templating keeps the stage
  $0-on-the-OpenRouter-ledger and fully testable. If you ever add a billable call later, it must thread its
  cost into a typed failure + record_spend exactly like FusionError.cost → DiscoveryFailed.cost_usd
  (see the gather/__init__.py invariant + test_gather_cost_integrity.py). State this in a code comment.
- BUDGET: fold the supplement's estimated web-query cost into _estimate_cost (reuse WEB_QUERY_PRICE ×
  supplement queries) so the preflight and recorded spend stay honest. The $10/day cap still governs.
- GRACEFUL DEGRADATION: if neither EXA_API_KEY nor BRAVE_API_KEY is set, the stage SKIPS and the ledger
  says "supplement skipped: no web-search key configured" — it must never crash the run.
- BACKWARD COMPAT: collect_web's default behavior is byte-unchanged (defaults preserve the complaint query
  + complaint extractor). A run with --no-supplement produces the exact pre-change ledger. Empty blind_spots
  → no supplement section (or an explicit "no blind spots surfaced" line).
- Works for BOTH lenses (pm + substack), since both carry blind_spots.

=== TESTS (add tests/discovery/test_backfill.py; update affected tests) ===
Collectors are injectable (search=/fetch= params) — keep it credential-free:
  - blind-spot bullets → solution-side queries (meta-prefix stripped).
  - only URL-anchored verbatim findings are emitted; a fabricated/uncited candidate is dropped.
  - an unfillable blind spot renders as "still open" (honest empty state).
  - --no-supplement skips the stage and the ledger is byte-identical to pre-change.
  - no web key → "supplement skipped" note, no crash.
  - supplement query cost is folded into result.cost_usd.
  - tier scaling: deep covers more blind spots than quick.
Update test_pipeline.py, test_render_substack.py, test_render.py, test_cli.py, test_tiers.py as needed.
Run: cd tools/llm-council && uv run pytest tests/discovery/ -q   (full suite must be green; then uv run pytest tests/ -q)

=== DOCS ===
- Update .claude/skills/fusion-discovery-council/SKILL.md: the "four stages" become FIVE (add Stage 5 —
  BACKFILL after FRAME); document --supplement/--no-supplement in §3 Flags; extend §6 (the gate now covers
  supplement findings); add the cost note (small, tier-scaled, free collector) to §5; add a §8 failure mode
  (no web key → skipped honestly). Keep the skill's voice and the path-resolution rules intact.
- Add a code-brain CHANGELOG.md entry (code-brain CLAUDE.md doc-update rule). Do NOT touch the vault.
- llm-council has no CHANGELOG; a short note in its README is optional, not required.

=== DELIVERABLE / REPORT BACK ===
Show the diff summary (files added/changed), the passing test output, and a 5-line before/after of a sample
ledger's new "Web Supplement" section (you can use stubbed search/fetch to render an example). Do not merge;
leave it on the branch for Sean to review.
```

---

## After Claude Code finishes

Quick review checklist for you, Sean: confirm the full discovery suite is green, eyeball the new `## Web Supplement (gap-fill)` section on a stubbed sample, confirm `--no-supplement` reproduces the old ledger, and confirm a no-key run degrades to the "skipped" note instead of crashing. Then merge. Every future `--lens substack` (or pm) run will self-fill its blind spots from then on.
