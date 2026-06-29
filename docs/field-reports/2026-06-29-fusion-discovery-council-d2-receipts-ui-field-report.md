# D2 — Per-card receipts UI (corroboration tier + freshness badge)

## What shipped

**6 commits** (spec + plan docs, 3 plan tasks, a final-review minors commit), **PR #106** into `main`.
**249 passed / 1 skipped** (was 233). New shared module `council/discovery/receipts.py`
(`receipt_line` + one-time `receipts_legend`), wired identically into `render.py` and
`render_substack.py`. Each ranked card now carries a compact `🧾` line — a two-axis
evidence-depth gradient — under its heading, with a one-time legend above the ranked list.
**$0, deterministic, render-layer only** — no model call, no gate/scoring change.

**This closes Step B** (PM4+D1 #103, D4 #104, E3 #105, D2 #106). Next arc is Step C
validation gates.

## The defining move (fourth consecutive headline): research before locking the shape

The one load-bearing unknown was the **tier vocabulary + thresholds**. A $0 deep-research
pass settled it against prior art instead of inventing from first principles:

- **Corroboration ladder = the journalism two-source rule + NATO Admiralty scale.** 1 =
  single-source (below the two-source bar), 2 = corroborated, 3+ = well-corroborated — and
  it **caps at 3+**, because arXiv 2501.01303 found *no significant trust gain from 1→5
  citations*. Without the research I'd likely have added a "very-well-corroborated" tier for
  5/8 domains, which the evidence says manufactures false precision.
- **A binary "✓ verified" stamp is meaningless** — citation-hallucination runs 11–57% even
  when links resolve. That's the whole justification for showing a *gradient in words*, not
  a checkmark, and for keeping the raw floats in the detail lines (audit trail) rather than
  in the headline receipt.
- **Freshness is a recency signal, not a truth signal** (old pain can still be real) — folded
  into the one-time legend, mirroring D4's absence-of-evidence discipline.

The research reused the existing scoring constants (`RECENCY_FLOOR`, `frame._why_now`'s 0.5
cutoff) rather than spawning parallel thresholds — the "discoverable existing threshold"
principle held.

## Process notes

- **Salvage worked again.** The deep-research harness tripped Anthropic-side rate-limiting in
  the adversarial-verify stage (the documented D4 failure mode) and skipped final synthesis.
  Per the standing lesson I did **not** re-run (~2.5M tokens avoided) — 8 claims confirmed
  cleanly pre-storm, the rest killed by *abstention* not refutation, and the threshold
  specifics were hand-vetted from the completed Search/Fetch transcripts. Note left at
  `vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md` (status: salvaged).
- **The review loop caught a real plan defect.** I wrote two buggy test assertions in the
  plan (`md.index("🧾")` as the first receipt; `"well-corroborated" not in md`) that
  collided with the legend's *own* `🧾`/tier text. The implementer contorted the
  implementation to satisfy them — legend *below* the cards, asymmetric guards between the
  two renderers — and flagged it as DONE_WITH_CONCERNS. Correct call to reject that fix: the
  defect was my tests, not the design. One fix subagent restored the clean symmetric shape
  (legend once, above the cards, identical in both ledgers) and scoped the assertions to the
  card's receipt string. The lesson: when an implementer deforms the design to pass a test,
  suspect the test.
- **Model tiering:** haiku for the pure-transcription helper (Task 1), sonnet for the
  multi-file wiring + reviews, Opus for the final whole-branch gate (**Ship, 9/10**, all six
  honesty invariants confirmed at source). Two final-review Minors folded in (an input-
  contract comment + a hoisted test helper); no behavior change.

## Vault hygiene

**Zero vault changes on the branch** — verified: the diff is code + `docs/` + SKILL.md +
CHANGELOG only. Sean's uncommitted vault WIP (`take-two-01-…`, substack-studio edits,
`tickets.md`) was never staged. The research note was written to `vault/20_projects/research/`
and **left unstaged** for Sean to commit (he owns vault commits this cycle).

## Carry-forward (Sean's court / next session)

- **Vault commits Sean owns:** the D2 research note (`2026-06-29-receipts-provenance-ui-research.md`,
  unstaged); mark **D2 ✅ DONE** + **Step B complete** in the fusion-discovery roadmap ticket
  in `tickets.md`.
- **Step B is closed.** Next is **Step C — validation gates** (both cheap, both gate the first
  *paid-per-run* builds): the **panel-vs-single-model** gate (~$1–2 OpenRouter — surface the
  estimate + check the day's discovery spend vs the $10/day cap first; gates E2) and the
  **PM3 longitudinal-signal** gate (re-run a past topic 2–4 weeks apart; gates PM3).
