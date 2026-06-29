# Claude Code prompt — rescue re-runs for T1 (iteration tax) + T4 (reproducibility)

Paste the fenced block into a **Claude Code session opened in `code-brain`**. Context outside the fence is for you (Sean).

## Why these two re-runs

The 2026-06-28 sweep left two topics thin:
- **T1 — iteration tax:** strong pain ("botsitting"; the 10-hrs-gained/4-lost stat) but only **1 verified / 5 dropped**, and the blind-spot flagged that the evidence skewed to *developers*, not creatives. Fix: pin the audience with `--segment "creative professionals"`.
- **T4 — reproducibility:** the panel returned **0 angles** — the phrasing didn't land where creatives post this pain (it's mostly developer territory). BACKFILL rescued it with the real frame: *"the same prompt never works twice → stop chasing prompts, build systems"* + the "trust tax." Fix: reframe the topic toward how creatives actually say it.

**Run timing:** prefer running these on a **fresh day** — 2026-06-28 already spent ~$8 real on discovery (note: the local ledger under-counts by ~$1.9 from the crashed-run cost leak, so today's recorded total understates real spend and the $10/day cap is less protective than it looks today). A clean daily budget avoids that ambiguity. Also make sure the **BACKFILL crash-fix is committed/present** before running (it is, once you commit it).

---

```
TASK: Two RESCUE re-runs of fusion-discovery-council (substack lens) to lift the two thin 2026-06-28
topics before they get mined into the editorial backlog. New output files (do not overwrite the
originals).

READ FIRST: .claude/skills/fusion-discovery-council/SKILL.md (§3 flags incl. --segment, §4 invocation,
§5 the $10/day cap, §7 NEVER git add/commit the vault).

  cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council

RUN A — T1 iteration tax, audience-pinned (standard tier, --supplement default on):
  uv run python -m council.discovery \
    "creative professionals who spend more time fixing, re-rolling, and cleaning up AI-generated output than the tools actually save them" \
    --lens substack --tier standard --segment "creative professionals" \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-ai-iteration-tax-v2-substack-idea-ledger.md

RUN B — T4 reproducibility, reframed toward how creatives say it (standard tier, --supplement default on):
  uv run python -m council.discovery \
    "artists, writers, and designers who say AI is a slot machine — the same prompt never gives the same result twice — and who have stopped chasing prompts in favor of building a repeatable system they can trust" \
    --lens substack --tier standard --segment "creative professionals" \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/2026-06-28-ai-reproducibility-v2-substack-idea-ledger.md

(Each writes a sibling ...-substack-brief.md.)

RUN ONE AT A TIME. After each, capture "Verified ideas: N · dropped: M · $X.XX" + a running daily total.
If a run prints "Budget rejected", STOP and report (resume after the daily reset) — do NOT --force.

REPORT BACK (compact): for each run — verified angles, dropped, cost, did --segment shift the evidence
toward creatives (vs the prior dev-skew), gap-fill rate, and the single highest-signal pain point. Then
say whether each topic is now mine-able (≥3 solid creative-side verified angles) or still thin.

DO NOT: git add/commit the vault (Obsidian-Git owns it); --force; raise tiers; run image gen.
```

---

## After Claude Code finishes

If either re-run now clears ~3 solid creative-side angles, tell me and I'll fold it into `SERIES-COMMAND-CENTER` alongside the T2/T3 angles (T1 → a Tool-Drop / Take Two on cutting the correction burden; T4 → the "build systems, not prompts" angle). If a topic is still thin after the rescue, that's a real signal the creative-side pain is genuinely sparse — worth knowing before you write to it.
