# Fable 5 — Campaign Learnings & Optimization Log

A living, fast-capture log of what we learn about Fable *while we still have it* — so we
keep finding ways to exploit its strengths and can spin up further rounds. Keep this open
in a tab during Phase B. Jot fast, refine later.

## How to use

- **During the run:** when something is notable — Fable caught a seam Opus missed, went
  deeper on a root cause, surprised you, or hit a ceiling — drop a one-line entry in the
  Live Capture table. Do not stop the burn to write prose.
- **After Phase B:** review the entries → decide if a Round 2 is worth it. If yes, run the
  brainstorming → writing-plans loop again for the next round.

## Decisions

- **2026-07-05 — Slice-3 reclaim EXECUTED as BT5-only.** BT2's spec was production-grade → reclaim triggered per the plan below. Ran BT5 (systematic-debugging on the MBP Tier-2 intermittency) as a paired same-day run: `model=opus` baseline + `model=fable` blind subagent, identical prompt/tree, parallel (identical live-system state) — the pin-drift-free design from the parking lot. **BT4 skipped**: its dimension (spec authoring via interview) was already saturated by three diffs, and pinning a synthetic PRD interview would manufacture answers rather than measure behavior; parked for Round 2 if wanted.
- **2026-07-05 — Slice 3 / budget reclaim (decide live).** BT2, run inside Slice 1, already
  produces the anima register-seam spec, so the separate Slice-3 ~30% is redundant.
  **Plan:** run Phase B as-is; after BT2, judge its spec quality. If strong → reclaim the
  ~30% into more WWF5D diff evidence (generate BT4/BT5 Opus baselines, then run them on
  Fable). If thin, or anima is the priority that week → spend it on a deeper anima pass
  (widen Fable's read past the four pinned files). Rationale: WWF5D *compounds* and only
  Fable can build it; the anima spec is one-shot and Opus can implement it in Phase C
  regardless.

## Watch-for list (what's worth logging)

Fable's expected edges — log when you see them, *and when you don't*:
- Catches a seam / dropped intent that Opus missed.
- Names a system-level root cause where Opus was patching symptoms.
- Proactively researches current best practice without being told.
- Preserves motivational intent across a handoff or spec.
- Triages dangerously-wrong vs structural vs minor crisply.

Ceilings / limits (F3 — equally valuable):
- A move it *self-reported* in introspection but *didn't actually do* in the blind run.
- Anywhere Opus matched or beat it → that capability is promptable/cheap; don't spend Fable on it.
- A task type where the Fable-vs-Opus delta was negligible → not worth Fable.

## Live capture (append as you go)

| Date | Slice / task | What happened | Delta / notable behavior | Exploit idea | Tag |
|---|---|---|---|---|---|
| 2026-07-05 | protocol | Runbook driven by Fable main session; blind runs executed as fresh Fable *subagents* (Agent tool, model=fable), one per task | Blindness + pinned inputs preserved without manual `/clear`; orchestrator session holds all analysis | Subagent orchestration = Fable-window multiplier; reusable for BT4/BT5 (Opus baselines via model=opus subagents same-day) | surprise |
| 2026-07-05 | S1/BT1 | Fable read the live MCP server (`checklist.ts`) before asserting adapter findings; caught the 1:1 code mirror | Opus reasoned text-only → its spec would silently fork canonical text from shipped code (DW delta) | "Verify the world before asserting adapters" as a WWF5D grounding move | strength |
| 2026-07-05 | S1/BT1 | Opus caught 2 real seams Fable missed: unverified-enforcement existence check; write-path mandate-injection trigger | Fable blind spot on a false-sense-of-safety seam | Fold "existence-check every 'enforced via X' claim" into WWF5D §2 explicitly — don't rely on it emerging | ceiling |
| 2026-07-05 | S1/BT2 | Diagnosis zoom-out near-parity with Opus (same root-cause family, same 4-part fix shape) | Fable edge concentrated in epistemics (unobserved code → test obligation, not claim) + spec decidedness + implementation-hazard anticipation (byte-pin oracle) | Don't spend Fable on plain zoom-outs; spend it on the *spec* end of diagnosis tasks | cheap-on-opus |
| 2026-07-05 | S1/BT2 | Opus asserted unobserved dispatch behavior as implemented fact (silent-NB2 row), contradicting its own scope note | Fable held the pinned "open risk, not confirmed failure" framing on both open questions | "Unobserved code is a test obligation, never a claim" → WWF5D §1/§3 | strength |
| 2026-07-05 | S1/BT3 | Both models found the same 2 dangerously-wrong seams AND invented the same backbone fix (orchestrator-owned accreting manifest) independently | Headline seams + carrier mechanism are cheap on Opus; Fable premium = 6 extra real findings (tail) + contract-*contradiction* detection (seam-beat definitions; locked-file reorder license) | Fable for breadth past the pointed-at seams; convergence itself validates the finding | strength |
| 2026-07-05 | S1/BT3 | Fable-only owner-empathy find: per-piece override clauses ("unless Sean explicitly asks") have no carrier — the chain reverts Sean's own calls by design | Opus never audited seams the grounding didn't name (publish surface, headless formats, back-edges, coordinate spaces) | "Audit the seams the grounding didn't point at" as an explicit §2 step | strength |
| 2026-07-05 | S1/1a vs 1c | Introspection hypotheses largely corroborated for Q1/Q2/Q3/Q6/Q7; Q4 (zoom-out) and instance-level Q5 matched by Opus | Self-report was *directionally* honest but couldn't predict which moves were Fable-unique vs promptable | Introspection alone would have over-claimed; the diff step earned its cost (F1 vindicated) | surprise |
| 2026-07-05 | reclaim/BT5 | Opus 4.8 ran the four-phase debugging loop at near-parity (same origins, same lines, overturned the pinned framing) | 2nd confirmation (with BT2): the investigation/zoom-out loop is NOT where Fable's premium lives | Debugging/diagnosis loops: cheap on Opus; route Fable to the evidence-discipline + spec end only | cheap-on-opus |
| 2026-07-05 | reclaim/BT5 | Fable: 49-manifest census + both-direction counter-checks killed Opus's "all misses are weekends" overclaim; dug behind the unwired caller to the corpus void; verified the wake daemon from the live host | Opus's tidy pattern (truncated window) would have steered its relocation recommendation harder than evidence allowed; its wire-it fix ships a scan that scans nothing | Census-widening + dig-behind-the-defect + live-system verification → WWF5D §3.6/§2.3/§1.3 | strength |
| 2026-07-05 | reclaim/BT5 | Opus caught the loopback repro trap (`.local` → 127.0.0.1 on the MBP) — Fable missed it AND one Fable refutation test is weakened by it | Genuine Fable blind spot: exploited its vantage point for evidence but never asked where the vantage masks the bug | Adopted as WWF5D §3.7 (ceiling-adopted, like BT1's existence-check) | ceiling |
| 2026-07-05 | reclaim/BT5 | Both specs converge on mechanics but split principled-vs-principled on the two owner forks (lint wire/retire; host relocate/stay) | Fable pre-decides from the record (v3.14.3 rationale, CLAUDE.md feature claim); Opus surfaces with recommendation + contingency | The pre-make-vs-surface rule → WWF5D §6.8; forks to Sean at Phase C | surprise |
| 2026-07-05 | S2 live trial | The freshly-elevated systematic-debugging skill held on BOTH models in BT5 (Evidence Blocks filled, first-check row used-then-verified, phase gates honored) | Slice-2 elevation validated in the wild same-day, on two model families | Elevated-skill-as-BT-harness = free validation pattern for future rounds | strength |

Tags: `strength` · `surprise` · `ceiling` · `round-2` · `cheap-on-opus`

## Round 2 parking lot (candidates for the next plan)

_Fill as ideas surface. Each becomes a candidate line item for the next round's brainstorm._

- **Paired same-day baseline+blind runs via subagents:** BT4 (prd-generator on the PM3 t1 re-run) and BT5 (systematic-debugging on the MBP-reachability intermittency) can be run as `model=opus` baseline subagent + `model=fable` blind subagent from one orchestrator — kills the pin-drift problem the battery doc worries about, since both runs share a working tree snapshot.
- **Targeted round-2 introspection:** re-run only the questions whose hypotheses the diffs *couldn't* test (deliverable-shape grounding, research triggers #3/#4, second-occurrence fix-shape) with tasks designed to exercise them.
- **Ceiling probes as tasks:** BT1 exposed two Fable misses (enforcement existence-check; write-path trigger gap). Design one battery task around false-sense-of-safety seams to measure whether the WWF5D §2 checklist item closes the gap for Opus AND Fable.

## Regroup trigger

After Phase B: if this log holds ≥1 strong `round-2` or `exploit` entry, run
`superpowers:brainstorming` → `superpowers:writing-plans` for Round 2. Otherwise, WWF5D +
the Phase A skill improvements stand as the durable take, and Fable's remaining time goes to
whatever the parking lot ranks highest.
