# Braintrust (braintrust.dev) — Falsification Teardown vs. Golden Loop

**Date:** 2026-08-17
**Method:** Primary sources only — official docs (`braintrust.dev/docs`, via the `llms.txt` markdown index), pricing page, product changelog, homepage marketing, public GitHub org. No secondary write-ups.
**Question under test:** Does Braintrust falsify the Golden Loop hypothesis — that no incumbent gives a non-coding PM an opinionated end-to-end loop of (production failure → curated versioned golden dataset with improvement/holdout split → one-change champion/challenger round → challenger must beat champion on a never-optimized-against holdout → written promote/reject decision record)?

---

## 1. Datasets: creation from logs, versioning, non-engineer UI access

**Creation from production logs/traces — fully UI, non-engineer accessible. This part of the hypothesis is FALSIFIED for Braintrust.**

- Promote traces from logs, pure clicks: "Go to Logs. Select the traces you want to add. Click Add to > Add to dataset, then choose the dataset." A row can hold a reference to a full trace or a group of traces instead of a copied value.
  Source: https://braintrust.dev/docs/annotate/datasets/create.md
- Curate from user feedback the same way: filter logs by feedback score, "Select the traces you want to include. Select Add to dataset."
  Source: https://braintrust.dev/docs/annotate/datasets/create.md
- CSV/JSON upload with drag-to-categorize columns (Input / Expected / Metadata / Tags) and a live preview table.
  Source: https://braintrust.dev/docs/annotate/datasets/create.md
- Loop (their in-product AI agent) can "create a dataset based on your logs or specific criteria" via natural language — e.g. "Generate a dataset from the highest-scoring examples in this experiment."
  Sources: https://braintrust.dev/docs/annotate/datasets/create.md, https://braintrust.dev/docs/loop
- Bulk automation exists too, but is code: dataset pipelines (beta) "transform spans or traces from your project logs into dataset rows in bulk," defined in TypeScript/Python and run via the `bt` CLI.
  Source: https://braintrust.dev/docs/annotate/datasets/pipelines.md

**Versioning — real, but snapshot-style, and paywalled.**

- "Every change is tracked, so experiments can pin to specific versions" (datasets overview). The concrete mechanism is **snapshots**: "named checkpoints of a dataset at a specific point in time," marked by a transaction id (`xact_id`), restorable ("Roll the dataset back to the snapshot's state"), and assignable to environments for "Evaluate in experiment" / "Evaluate in playground."
  Sources: https://www.braintrust.dev/docs/guides/datasets (overview), https://braintrust.dev/docs/annotate/datasets/manage.md
- **Snapshots are Pro/Enterprise only** — the free tier gets change tracking but not named checkpoints.
  Source: https://braintrust.dev/docs/annotate/datasets/manage.md (plan gating noted); pricing page corroborates feature gating: https://www.braintrust.dev/pricing
- UI record editing exists (edit/delete records, SQL filters, tags/stars, JSON schemas with UI-only enforcement).
  Source: https://braintrust.dev/docs/annotate/datasets/manage.md
- Loop can drive versioning conversationally: "Loop can now save, list, and restore dataset snapshots and tag versions with environments" (changelog, May 2026).
  Source: https://braintrust.dev/docs/changelog.md

## 2. Holdout / split discipline

**No first-class concept. This is left entirely to user convention. Gap CONFIRMED.**

- The datasets docs (index, create, manage, pipelines, use-in-evaluations) contain **no mention of splits, train/test division, or holdout sets**. Checked explicitly across all four dataset pages.
  Sources: https://braintrust.dev/docs/annotate/datasets/create.md, https://braintrust.dev/docs/annotate/datasets/manage.md, https://braintrust.dev/docs/annotate/datasets/pipelines.md
- The closest primitives are **dataset filters** ("Scope an experiment run to a subset of a dataset instead of every record" — changelog May 2026) and **playground sampling** ("a sample rate control that evaluates a random subset of dataset rows" — changelog June 2026). Both are conveniences for running on subsets, not a guarded holdout: nothing prevents any experiment from running on, or optimizing against, any subset.
  Source: https://braintrust.dev/docs/changelog.md
- Telling detail: Braintrust's own engineering **blog** applies rigorous holdout discipline manually ("A holdout only measures something real if the eval was never tuned on it" — they hand-built a fresh split with no overlapping records). They know the concept; the product does not enforce or even represent it.
  Source: https://www.braintrust.dev/blog/rlm-harness-negative-transfer
- No "improvement vs. holdout" designation, no lockout of a split from playground/Loop optimization, no audit of which experiments touched which rows for tuning purposes anywhere in docs.

## 3. Champion/challenger and promotion workflow

**Rich comparison machinery; no promotion decision workflow. Partial overlap, gap CONFIRMED on the decision layer.**

What exists (strong):
- Baselines: designate an experiment as persistent baseline ("It will be auto-selected whenever you open that experiment... Clear baseline"); auto-fallback to "the most recent experiment on the same git branch"; project-wide default baseline.
  Source: https://braintrust.dev/docs/evaluate/compare-experiments.md
- Row-aligned deltas: "Braintrust aligns test cases across experiments and adds score deltas to every row, with improvements highlighted in green and regressions in red"; diff mode with sub-rows per experiment; sort/filter by regressions.
  Source: https://braintrust.dev/docs/evaluate/compare-experiments.md
- **Comparison grade** (changelog May 2026): "Experiment comparisons now label each experiment as improvement, regression, tradeoff, or tie relative to the base experiment." This is a machine verdict — the closest thing to champion/challenger judging.
  Sources: https://braintrust.dev/docs/evaluate/compare-experiments.md, https://braintrust.dev/docs/changelog.md
- **Pairwise scoring** (changelog July 2026): "When you compare two experiments in diff mode, you can now record which one produced the better output for each row" — human A/B preference at row level.
  Source: https://braintrust.dev/docs/changelog.md
- Experiments are "the immutable, comparable record of your eval runs"; a playground config can be promoted "to an experiment to capture an immutable snapshot."
  Sources: https://www.braintrust.dev/docs/guides/evals, https://braintrust.dev/docs/evaluate/run-in-ui.md

What does not exist:
- "The documentation does **not** describe promotion, champion-challenger selection, or approval workflows" — no promote/reject gate, no requirement that a challenger beat the champion on anything before shipping, no state machine of champion status. (Prompt *versions* can be deployed/tagged to environments, but that is deployment plumbing, not a judged promotion ritual.)
  Source: https://braintrust.dev/docs/evaluate/compare-experiments.md
- **One-change-at-a-time discipline:** "contains no explicit guidance on isolating single variables during experimental design" — nowhere in evals, compare, or run-in-UI docs.
  Sources: https://braintrust.dev/docs/evaluate/compare-experiments.md, https://www.braintrust.dev/docs/guides/evals

## 4. Decision records / audit

**Nothing produces a written record of WHY a change was promoted. Gap CONFIRMED (with one nearby feature to watch).**

- The experiment Details/summary panel shows comparisons, scorers, datasets, saved parameters, and metadata — metrics and lineage only. "No sections covering: experiment description or notes fields, written narratives explaining why results constitute improvements, decision record functionality, stakeholder-facing reporting."
  Source: https://braintrust.dev/docs/evaluate/interpret-results.md
- Permalinks exist for sharing results ("A permalink uses the experiment's object ID... stays valid permanently") — a link to metrics, not a rationale.
  Source: https://braintrust.dev/docs/evaluate/interpret-results.md
- Nearest neighbor, and the thing to watch: **Annotated version history** (changelog August 2026): "Describe what changed as you save a new version of a prompt, parameter, or scorer, and the note stays pinned to that version in its history." That is a free-text change note on an artifact version — a commit message, not a promote/reject decision record tied to a champion/challenger outcome on a holdout.
  Source: https://braintrust.dev/docs/changelog.md

## 5. Persona: quickstart walk-through and marketing

**The no-code path is real and substantial mid-loop, but the loop's entry point (tracing) is SDK-only, and marketing is engineering-led.**

- Quickstart has three paths: **Tracing** ("Integrate with AI providers and frameworks to send traces") — SDK code required; **Evaluation** via playgrounds — largely no-code; **Coding Agents** via the `bt` CLI. Workflow framing: Instrument → Observe → Annotate → Evaluate → Deploy → Admin. Step 1 (Instrument) is engineering work, always.
  Source: https://www.braintrust.dev/docs/start
- Once traces flow, a non-engineer can genuinely go end-to-end in the UI: promote traces to datasets (§1), run experiments "with no code or local setup required" — pick prompts/workflows, choose/upload a dataset, add scorers and classifiers, run on cloud.
  Source: https://braintrust.dev/docs/evaluate/run-in-ui.md
- Human review is explicitly multi-persona: "human feedback from end users, subject matter experts, and product teams in one place"; categorical/continuous/free-form scores; assignment, Slack notifications, multi-reviewer independent scoring (changelog July 2026).
  Sources: https://braintrust.dev/docs/annotate/human-review/index.md, https://braintrust.dev/docs/changelog.md
- Marketing persona: headline "Ship quality agents at scale"; positions for engineering-to-product teams (Cloudflare, Coursera, Notion, Box, Replit, Vercel logos); featured quote is an **Engineering Manager**. Claims "Surface patterns in production, turn them into evals, and improve quality." No PM-first framing; no documented PM end-to-end journey in the docs.
  Source: https://www.braintrust.dev/
- **But there is no opinionated methodology anywhere**: the docs hand you primitives (datasets, baselines, diffs, review queues) and never prescribe a loop, a split discipline, or a decision ritual. The PM must invent the process.

## 6. Pricing, source model, 2026 momentum

**Pricing** (https://www.braintrust.dev/pricing):
- Free "Starter": $0, "1 GB processed data," "10k scores," "14-day retention," "$10 credits," "Unlimited users, projects, datasets, playgrounds, and experiments." Gated: human review scores (1 per project), **Loop agent**, playground annotations.
- Pro: "$249 / month," 5 GB, 50k scores, 30-day retention, unlimited human review, basic RBAC, custom charts. Overages: +$3–4/GB, +$1.50–2.50/1k scores.
- Enterprise: custom; full RBAC, on-prem/hybrid deployment.
- Note for Golden Loop: **dataset snapshots (the versioning backbone) and Loop are both paid-tier features** — the free tier cannot run a versioned-golden-dataset discipline properly.

**Source model** (https://github.com/braintrustdata):
- Platform is **closed source**. Open source: SDKs (Apache-2.0/MIT; JS 28★, Python 17★), braintrust-proxy (MIT, 408★), autoevals (1k★), agentbehavior (275★), `bt` CLI (Apache-2.0), Terraform data-plane module (self-host infra).

**2026 momentum toward PM-grade workflow** (https://braintrust.dev/docs/changelog.md):
- The 2026 changelog is dense with UI/non-engineer moves: comparison grades (May), classifiers + conditional/visibility-scoped review scores (June), pairwise scoring + multi-reviewer + Slack review assignments (July), trace groups in datasets + annotated version history + experiment Summary table (August). Loop gained dataset-snapshot management (May).
- Direction of travel is unmistakable: more review-team ergonomics, more verdict-like labels, more change annotation. They are building the *ingredients* of a decision layer bottom-up, without (yet) the opinionated loop, holdout guard, or decision record.

---

## 7. VERDICT

**Braintrust does NOT falsify the core hypothesis, but it kills the weak version of it.**

- **DEAD parts of the differentiation claim:** "Incumbents are engineer-first / SDK-required for curation" is false for Braintrust's mid-loop. A non-coding PM can promote production traces into a dataset by clicking (create.md), edit and tag rows in the UI (manage.md), run a no-code experiment with scorers (run-in-ui.md), and read an automatic improvement/regression/tradeoff/tie verdict against a pinned baseline (compare-experiments.md). Dataset versioning exists (snapshots, Pro+). Do not pitch Golden Loop as "the first UI for turning traces into eval datasets" or "the first versioned golden dataset" — Braintrust ships both today.
- **ALIVE, with primary-source evidence:** (a) **Holdout discipline** — zero product concept of a held-out split that experiments/Loop cannot optimize against; their own blog does holdouts by hand, proving the product doesn't (blog/rlm-harness-negative-transfer). (b) **Promotion workflow** — comparison grades and pairwise scores render verdicts, but there is no champion state, no promote/reject gate, no beat-the-champion-on-holdout requirement (compare-experiments.md explicitly lacks it). (c) **Decision records** — nothing captures WHY a change shipped; annotated version history (Aug 2026) is a commit message on an artifact, not a decision artifact (interpret-results.md, changelog.md). (d) **One-change-at-a-time** — never mentioned as method anywhere. (e) **Opinionated end-to-end loop for a PM** — marketing and quickstart are engineering-led; the six-stage workflow starts at SDK instrumentation and the docs prescribe no methodology.
- **Risk assessment:** The remaining gap is methodology + governance, not features — and Braintrust's 2026 cadence (verdict labels, pairwise judging, version annotations, review assignment) shows them assembling adjacent pieces roughly monthly. Golden Loop's defensible core is the *enforced discipline* (locked holdout, one-change rounds, mandatory decision record), which incumbents structurally avoid because opinionation narrows their market. Positioning must be "the decision layer on top of your trace tool," never "a better eval tool" — on primitives, Braintrust wins.
