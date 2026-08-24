# Red-team protocol

The studio's adversarial gate. A **protocol, not a person** (bench ratification 2026-08-22): no standing sixth seat — every red-team pass runs **stateless, on Codex** (GPT 5.6 Sol, High reasoning, via the codex plugin), receiving only the artifacts and this protocol, never the drafting conversation. Cross-vendor by design: a different model lineage hunts with different blind spots, at $0 Claude-usage cost.

## Posture

The red team's job is to **break the design**. It is briefed as a skeptic, not a reviewer: *"Find the strongest case that this fails. Being unable to find a material flaw is a finding — state what you attacked and why it held."* It proposes the strongest competing alternative (the steel-man), not just objections.

## When gates fire

| Engagement type | Gates |
|---|---|
| Design a new project | **Gate 1 — PRD sign-off** (after the Evals co-sign, before architecture begins) · **Gate 2 — pre-launch** (after the ops/economics model, before the design is declared done) |
| Audit an existing system | **One gate at close** — the audit's own findings are red-teamed before delivery |
| One-off question | No gate |

Any seat may additionally request an off-cycle pass on its own artifact (same protocol, same statelessness).

## Attack checklists (per artifact type)

- **PRD** — unfalsifiable success claims; hidden user/data assumptions; missing non-goals; metrics that reward hurting users (the "assumed resolution" class); scope-creep vectors.
- **ADR** — unpriced alternatives; vendor lock-in; scale cliffs; single points of failure; complexity that serves the résumé, not the product.
- **Failure-UX spec + model card** — uncovered failure modes; overtrust surfaces; missing disclosure; escalation dead-ends (no path to a human).
- **Eval plan** — judge-gameable metrics; train/test leakage; unrepresentative golden sets; the metric-vs-user gap; missing negative/abuse cases.
- **Ops model + runbook** — unit economics that only work at best case; kill-switch theater (a switch nobody can actually pull); drift blind spots; runbook steps requiring a human who won't be there at 3 AM.
- **Whole design (gate passes)** — cross-artifact contradictions; the steel-man alternative; "name the most likely way this is quietly failing six months after launch."

## Verdicts

Findings are triaged: **CRITICAL** (blocks the gate) · **MATERIAL** (fix, or Sean explicitly accepts with a recorded why) · **NOTE**. Gate outcome: **PASS** · **PASS WITH ACCEPTANCES** · **FAIL** → redraft, one model tier up (deviation trigger: redraft after material defects).

Every gate writes a ledger entry (per `ledger-entry.md`, seat: `red-team-gate`) with the verdict and acceptances; the full findings file lands in the engagement's `artifacts/`.

## Fallback — a gate never silently skips

If the Codex CLI is unavailable, the gate does **not** skip and does not wave work through: it runs as a fresh-context Claude adversarial pass, explicitly labeled `fallback: same-vendor` in the ledger entry, and a ticket is filed to re-run on Codex. (Fleet lesson: vault-critic ran 38 nights on a broken Codex symlink while reporting healthy — a gate that can fail silently is not a gate.)
