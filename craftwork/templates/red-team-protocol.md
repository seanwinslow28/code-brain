# Red-team protocol

Every -craft team's adversarial gate. A **protocol, not a person** (Systemcraft bench ratification 2026-08-22): no standing seat. Every red-team pass runs **stateless**, receiving only the artifacts and this protocol, never the drafting conversation, and on **the vendor that did not last write its anchor artifact** ([law.md § Model delegation](../law.md#model-delegation)). By default that is Codex GPT-5.6 Sol High, with the model pinned. Cross-vendor by design: a different model lineage hunts with different blind spots.

*Shared law since 2026-10-01 ([craftwork build 1](https://github.com/seanwinslow28/code-brain/issues/324)): moved from `systemcraft/templates/`. Each team keeps its own **gate schedule** and **per-artifact attack checklists**: Systemcraft in [systemcraft/templates/gate-schedule.md](../../systemcraft/templates/gate-schedule.md), Productcraft in its master skill's Gate phase and in the red-team checklist that ends each of its artifact templates.*

## Posture

The red team's job is to **break the design**. It is briefed as a skeptic, not a reviewer: *"Find the strongest case that this fails. Being unable to find a material flaw is a finding — state what you attacked and why it held."* It proposes the strongest competing alternative (the steel-man), not just objections.

## What a gate may demand

*(Systemcraft eng-003.d20, ratified 2026-08-29: a paper gate may no longer demand runtime evidence.)*

A gate attacks only what its anchor can prove at the point it fires. A gate on a design attacks cross-artifact consistency, exact rules/schemas/arithmetic, adversarial traces, design-reference proofs at their declared boundary, live-fact provenance, and the completeness of future evidence contracts. Evidence that requires built code or operation is recorded as an **IMPLEMENTATION HOLD**, with owner, trigger, required record, query/test, and fail-closed consequence. Missing implementation evidence is not a finding at a design gate. Claiming it exists, overstating a design proof, or failing to specify how it will be produced is still a finding.

A gate that waits on something that does not exist yet (an implementation candidate, a handoff brief) does not fire. Its state is **NOT FIRED — IMPLEMENTATION ABSENT** or **NOT FIRED — TRIGGER NOT MET**, never FAIL and never PASS. No document-only substitute and no acceptance can waive a hard hold.

Any seat may additionally request an off-cycle pass on its own artifact (same protocol, same statelessness).

## Verdicts

*(Systemcraft eng-003.d20/d52, ratified 2026-08-29: outcomes are typed so one gate's verdict can never be quoted as another's.)*

Findings remain **CRITICAL** (blocks the gate) · **MATERIAL** (fix, or Sean explicitly accepts with a recorded why) · **NOTE**. Outcomes are **typed by gate**, each team naming its types in its gate schedule (Systemcraft: PRD / DESIGN / LAUNCH / AUDIT; Productcraft: STRATEGY / HANDOFF / TRAIN / AUDIT). Each is **PASS · PASS WITH ACCEPTANCES · FAIL**. **IMPLEMENTATION HOLD** is an evidence obligation, not a severity and not an acceptance. A design can pass with holds, but launch cannot pass while a hard hold is open. The NOT FIRED states are states, not verdicts. Every findings file names the gate type in its title and verdict line. FAIL → the owning seat redrafts one tier up ([law.md § Model delegation](../law.md#model-delegation), trigger 1), then re-gates.

Every gate writes a ledger entry (per [ledger-entry.md](ledger-entry.md), seat: `red-team-gate`) with the typed verdict, its acceptances, and the vendor it ran on and why. The full findings file lands in the engagement's `artifacts/` or `audits/`. Reader-facing renderings of any verdict follow [status-vocabulary.md](status-vocabulary.md).

## Fallback — a gate never silently skips

If the planned vendor is unavailable, the gate does **not** skip and does not wave work through. It runs as a fresh-context adversarial pass on the other vendor, explicitly labeled `fallback: same-vendor` in the ledger entry, and a ticket is filed to re-run it on the planned vendor. (Fleet lesson: vault-critic ran 38 nights on a broken Codex symlink while reporting healthy. A gate that can fail silently is not a gate.)
