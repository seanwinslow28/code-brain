# Gate findings template — the red-team gate's artifact

The findings file a **red-team gate** writes: stateless, on the vendor that did not last write the anchor artifact (Codex GPT-5.6 Sol High by default; a fresh-context Opus 5 subagent when the anchor was last written on Codex), receiving only the artifacts and the inherited [red-team protocol](../../systemcraft/templates/red-team-protocol.md), never the drafting conversation. Productcraft's schedule: **Gate 1 — strategy sign-off** (`<eng>.gate-1`, anchor the Strategy & POV doc, after stage 3), **Gate 2 — pre-handoff** (`<eng>.gate-2`, anchor the handoff brief, only when a brief exists), the **close gate** (`<eng>.gate-close`, the whole train), and an audit engagement's single **audit-close gate**. Every gate also writes its ledger entry (`seat: red-team-gate`) naming its vendor and why; this file is the authoritative record of the verdict and the entry is derived from it.

Posture is inherited: *find the strongest case that this fails; being unable to find a material flaw is a finding — state what you attacked and why it held*; propose the steel-man alternative.

```markdown
---
id: pc-eng-001.gate-1              # gate-1 | gate-2 | gate-close | gate-audit-close
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-22
seat: red-team-gate
gate: strategy-sign-off            # strategy-sign-off | pre-handoff | close | audit-close
anchor: pc-eng-001.strategy        # the anchor artifact and revision
anchor_revision: 1
anchor_last_written_on: claude     # claude | codex — decides the vendor below
vendor: codex gpt-5.6-sol high     # the runtime that ran the gate; "fallback: same-vendor" when the other was unavailable
fallback: none                     # none | same-vendor → re-run ticket <link>
inputs: [pc-eng-001.strategy, pc-eng-001.discovery, pc-eng-001.insights, pc-eng-001.cosign-discovery, pc-eng-001.audit-strategy]
verdict: STRATEGY PASS WITH ACCEPTANCES   # see Verdict lines
ledger_entry: pc-eng-001.d22
---

## Verdict line

Typed, so a strategy verdict can never be quoted as a train verdict: `STRATEGY | HANDOFF | TRAIN | AUDIT` × `PASS | PASS WITH ACCEPTANCES | FAIL` + ` — QUALITY VERDICT ONLY`, then scope and authority, then **Means** and **Does not mean / Next**, per Systemcraft's status vocabulary. `NOT FIRED — TRIGGER NOT MET` is a state, not a verdict (a Gate 2 with no brief). FAIL → the owning seat redrafts one tier up and the gate re-runs.

## Findings

| # | Severity | Artifact and section | Finding | Attack it came from (template checklist line) | Disposition |
|---|---|---|---|---|---|
| 1 | CRITICAL \| MATERIAL \| NOTE | pc-eng-001.strategy § Strategic bets | | "A point of view that cannot be wrong" | redraft \| accepted by Sean <date>: <why> \| noted |

CRITICAL blocks the gate. MATERIAL is fixed, or Sean explicitly accepts it with a recorded why. Every finding names the checklist line it came from — an attack with no home in a template is a finding against the templates folder.

## Implementation holds

Evidence only a built thing can produce, recorded as an obligation, never a severity: owner, trigger, required record, the query or test, the fail-closed consequence. A design can pass with holds; nothing launches while a hard hold is open.

| Hold | Owner | Trigger | Required record | Query or test | If unmet |
|---|---|---|---|---|---|

## Steel-man alternative

The strongest competing design the train did not choose, in one paragraph, and why the train's choice survives it — or does not.

## What was attacked and held

Per artifact: the attacks run, and why each held. Empty is a defect.

## Six months on

"Name the most likely way this is quietly failing six months after launch." One paragraph; the metric that would show it; whether the Insights plan carries that metric.

meter: <runtime> · <tokens> · <wall-clock>
```

## Whole-train attacks (close gate; Gate 1 and Gate 2 run their anchors' template checklists plus the cross-artifact rows)

- **Cross-artifact contradictions** — positioning quoted differently downstream; a key result on a metric the Insights plan lacks; a business-case price that breaks a Growth loop; a roadmap slice with a Systemcraft layer and no brief; a cadence reading an artifact that does not exist.
- **The evidence chain** — a bet whose supporting claim was graded below `reported-behavior`, or whose claim id no longer exists after a redraft.
- **The cascade that did not fire** — an artifact below a loopback still at its old revision.
- **Checks that never ran** — a stage with no check record; a co-sign transcribed without a record; an audit at a lower tier than its auditor's baseline.
- **The steel-man** — a competing design that reaches the same outcome cheaper, and no artifact rules it out.
- **The quiet failure** — the six-months-on scenario with no metric that would reveal it.
- **Reasoning that crossed** — a brief or frozen copy carrying ledger text, transcripts, or the drafting conversation.
