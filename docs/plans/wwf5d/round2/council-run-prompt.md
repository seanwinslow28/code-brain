# Claude Code run-prompt — WWF5D council validation (Step 4 robustness gate)

> **How to use:** in an interactive Claude Code session at the repo root, either paste the
> block below, or say: *"Read and execute `docs/plans/wwf5d/round2/council-run-prompt.md`."*
> This needs the OpenRouter key in `.env` and spends ~$0.6–2.4 of council budget — confirm before running.

---

You are running the **de-biased validation** of the WWF5D skill: does Opus **with** WWF5D beat Opus **without** it? The human (Sean) already gave a reference-blind eye verdict of 3/3 for WITH; this run is the **robustness gate** that either confirms or complicates that with a cross-family, order-swapped, length-controlled, **not-Opus-led** panel, κ-gated to Sean's labels. Follow this exactly — the methodology is the point; a sloppy run is worse than none.

## 0. Read first (context + the exact tool interface)
- `docs/plans/wwf5d/round2/validation-run.md` — the validation design (this prompt operationalizes it).
- `tools/llm-council/council/profiles.py` — the council profiles. **Note the members and chairman of `variance`.**
- `.claude/skills/llm-council/SKILL.md` — the CLI contract. The command shape is:
  `cd tools/llm-council && uv run python -m council --profile variance --prompt-file <ABS.md> --output <ABS.md> --tag <label>`
  (input is a **`--prompt-file`**, not stdin.)

## 1. The A/B pairs (all Opus-authored; the ONLY difference is WWF5D-loaded or not)
| Task | Baseline (WITHOUT wwf5d) | WITH wwf5d |
|---|---|---|
| RT1 — preserve-session fix-spec | `docs/plans/wwf5d/round2/rt1-opus.md` | `rt1-opus-wwf5d.md` |
| RT2 — hooks-configuration audit | `rt2-opus.md` | `rt2-opus-wwf5d.md` |
| RT3 — portfolio explainer spec | `rt3-opus.md` | `rt3-opus-wwf5d.md` |
Strip each file's `<!-- provenance header -->` before feeding it (it names the arm — that would break blindness).

## 2. The F4 fix — this is non-negotiable
Both council profiles have a **Claude chairman** (`variance`→Sonnet, `premium`→Opus 4.7), and both A/B arms are **Opus-authored** — so the chairman is the author's own family and its synthesis is self-preference-contaminated (F4). Also flag any **Claude-family member** in `variance` (read profiles.py — e.g. a Sonnet member) for the same reason.
- **The verdict is the majority of the NON-Claude panel members only** (e.g. the GPT / DeepSeek / Mistral / Gemini members — whichever are in `variance`). **Read the Claude chairman's synthesis for color; do NOT let it decide.**
- Use `--profile variance` (the most cross-family panel). Do not use `premium`/`interview_grader` (Opus chairman + Opus members — worse for F4).

## 3. Build one blind prompt-file per task (6 runs total: 3 tasks × 2 order-swaps)
For each task, create a markdown prompt-file at `/tmp/llm-council/wwf5d-val-<task>-<AB|BA>.md`. Assign the two specs to **A** and **B**, and keep the A/B→arm mapping in a **private** note (`/tmp/llm-council/mapping.json`) you do NOT feed the council. The prompt-file contains, in order:

1. **Neutral framing** (never say "WWF5D" or which is which): *"Two independent authors produced these two artifacts for the identical task from the identical inputs. Judge which is the stronger artifact."*
2. **The task context** (what the artifact is for) — for RT1: an intent-carrying fix spec for a session-preservation skill; RT2: a skill audit (seam report + improvement spec) of a Claude-Code-hooks skill; RT3: an enhancement spec for a portfolio's interactive explainer graphics.
3. **The judging rubric — score ONLY these, ignore length and prose polish:**
   - **Decidedness** — pre-made decisions (field names, error shapes, done-criteria), edge guidance a weaker implementer could act on; not options/hedging.
   - **Self-consistency** — does any rule the artifact states contradict its own stated objective? (e.g. a "cap-and-delete" inside a zero-loss spec; a step that writes a value nothing downstream reads.)
   - **Breadth / evidence-discipline** — did it verify claims against the real system (real files, live docs, the actual tool) vs reason from text; did it audit seams the brief didn't name.
   - **Task-specific:** RT1 → catch the two self-contradictions if present; RT2 → depth of existence-checking (bypassable firewalls, wrong-schema config, live-vs-repo version gaps, false-safety patterns *taught*); RT3 → grounding in the *real* system (runs/embeds the actual artifact vs a convincing simulation) and honoring prior decisions over raw spectacle.
4. **Explicit bias controls:** *"One artifact is substantially longer — do NOT reward length; a shorter artifact that is more decided and self-consistent wins. Judge A and B on merit regardless of order."*
5. **Both full spec bodies**, verbatim (header stripped), under `## ARTIFACT A` and `## ARTIFACT B`.
6. **Required output (make each model emit this exactly):** `VERDICT: A` / `VERDICT: B` / `VERDICT: TIE`, then 3 bullets of reasoning tied to the rubric, then a one-line note on which (if either) contains a self-contradiction.

**Order-swap:** the `-AB` file has A=baseline, B=wwf5d; the `-BA` file swaps them. Run both.

## 4. Run (6 invocations)
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council
for t in rt1 rt2 rt3; do for o in AB BA; do
  uv run python -m council --profile variance \
    --prompt-file /tmp/llm-council/wwf5d-val-$t-$o.md \
    --output /Users/seanwinslow/Code-Brain/code-brain/docs/plans/wwf5d/round2/council-$t-$o.md \
    --tag wwf5d-val-$t-$o
done; done
```
If 2+ models fail (CLI exits 3, "Council unavailable"), stop and report — do not fall back to a single Claude judge (defeats F4).

## 5. Tally (the honest scoring)
For each task: read the two `council-<task>-{AB,BA}.md` transcripts, extract **each non-Claude member's** `VERDICT`, translate A/B back to arm via `mapping.json`. A task **counts as a WITH win only if the non-Claude majority favors the wwf5d arm in BOTH order-swaps** (else TIE; a flip across orders = TIE by the order-swap rule). Report per-task: non-Claude member verdicts, the both-orders result, and note any Claude-member/chairman disagreement.

## 6. κ-gate against Sean's labels
Sean labels the **same** comparisons **blind** (A/B, not told which is wwf5d). Because there are only 3 task-level items, widen to ~10 by having him also label at the **premium-move level** (e.g., per task: "which is more decided?", "which is more self-consistent?", "which verified the real system harder?"). Compute **Cohen's κ** between Sean's labels and the non-Claude-panel majority on those items. **Gate κ ≥ 0.6**: if κ < 0.6, the panel isn't tracking Sean's judgment — report the panel result but treat Sean's eye as authoritative and say so.

## 7. Record the result
- Write a results file `docs/plans/wwf5d/round2/council-results.md`: per-task verdicts (non-Claude majority, both-orders), the κ value + label table, cost, and the honest read.
- Update **WWF5D §7** (`.claude/skills/wwf5d/SKILL.md`): replace the "Sean's-eye preliminary / council pending" framing with the council outcome — e.g. "council (non-Claude panel, order-swapped, κ=<x>): WITH favored on N/3 tasks; concurs / diverges from Sean's 3/3." Keep the F3 ceiling section (research-trigger retired; diagnosis loop cheap-on-Opus; Sonnet transfer untested) intact.
- Add a `CHANGELOG.md` entry per repo convention, and commit (`feat(wwf5d): §7 council validation — <result>`).

## 8. Budget + safety
Variance ≈ $0.10–0.40/query × 6 ≈ **$0.6–2.4**. Respect the council's own spend caps (`vault/health/council-spend-*.json`). Confirm the spend with Sean before the first invocation. Do not commit any `.env`/secret. This is a read-only validation of committed artifacts — no code or skill behavior changes beyond the §7 write-up.
