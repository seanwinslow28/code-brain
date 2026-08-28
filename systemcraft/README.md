# Systemcraft

*an AI PM system design studio*

A five-seat specialist bench that plans, executes, and audits AI product system design — and explains every material choice, because the work is also the demonstration. Built by Sean Winslow (a PM, not a dev) as working machinery, not a portfolio prop: its first engagement audited a live production system, survived its own red team, and fixed the outage it found the same day.

## The bench

Five seats, run as a sequential pipeline — full artifacts handed forward, never summaries. Each seat owns one artifact contract, one template, one corpus lane, and one audit duty.

| # | Seat | Owns | Audits |
|---|---|---|---|
| 1 | [Design Strategist](bench/design-strategist.md) | PRD — framing, users, evaluable success criteria | Failure-UX spec + model card |
| 2 | [Architecture Advisor](bench/architecture-advisor.md) | ADR — options, each priced | Ops model + runbook |
| 3 | [Interaction & Trust Designer](bench/interaction-trust-designer.md) | Failure-UX spec + model card | Eval plan |
| 4 | [Evals & Evidence Architect](bench/evals-evidence-architect.md) | Eval plan — measurements, no thresholds | PRD (the dual-touch co-sign) |
| 5 | [Ops & Economics Modeler](bench/ops-economics-modeler.md) | Ops/economics model + incident runbook | ADR |

The audit column is a closed cycle: every artifact gets exactly one adversarial peer reviewer, always **fresh-context** — an auditor never sees the drafting conversation, only the artifacts. Two boundary rules do a lot of work: the seat that designs a test never sets its passing grade (measurements are Evals', thresholds are Ops'), and a PRD isn't done until Evals co-signs that every success claim can become a runnable test.

## The discipline

- **Engagements run a five-phase lifecycle** — Open → Route → Run → Gate → Close — with routing by engagement type: a new design takes the full train, an audit fields every seat whose lane the target has, a one-off takes one seat that must name what it didn't cover.
- **Every seat states why-A-over-B** on every material choice, in one breath. Depth is generated on demand, never stored — the brevity law.
- **Models are assigned per seat and deviations are never silent**: each seat file carries its baseline; the orchestrator may escalate or downshift per task against named triggers, always with a stated why.
- **Decisions land in a ledger** — one file per material decision, seven short sections, accreting per engagement ([entry template](templates/ledger-entry.md)). The ledger is the studio's memory and message bus.
- **A red team that is a protocol, not a person** ([the protocol](templates/red-team-protocol.md)): milestone gates run stateless on a different vendor's model, briefed to break the work, with FAIL → redraft one model tier up. A gate that can fail silently is not a gate, so an unavailable red team triggers a labeled fallback and a re-run ticket — never a skip.

## Public machinery, private brain

Everything that shows *how the studio works* is tracked here: [bench/](bench/), [templates/](templates/) (PRD, ADR, failure-UX + model card, eval plan, ops model + runbook), and [lanes/](lanes/) — five topic-organized manifests pointing into the reference corpus. The corpus itself (distilled practitioner canon + five purchased books) and the decision ledger are local-only: the manifests are shelf labels, never the books. On a machine without the private layers, seats say so plainly and flag what would normally be corpus-grounded — they never fabricate a citation.

## Proof: the first engagement

The studio's shakedown was a five-seat audit of this repo's own autonomous agent fleet — a real production system with real incidents ([engagement record](https://github.com/seanwinslow28/code-brain/issues/157)). What the machinery did on contact:

- Seats audited from **live production evidence** over read-only SSH, not documentation — and found the documentation wrong.
- The cross-vendor gate **failed the audit twice**: it falsified two headline numbers, forced a root cause to move, and surfaced the one question all five seats missed. The redrafts re-measured instead of arguing, at a higher model tier, per protocol.
- The audit **root-caused a live outage** (a network renumbering had orphaned hardcoded addresses; the pipeline reported success while producing nothing) — and the fix shipped the same day, verified end-to-end.
- Eighteen ledger entries now anchor the studio's memory, each one a breath long.

The engagement's working thesis, earned the hard way: *a system that reports green while delivering nothing is the default failure mode of autonomous fleets — and the fix is measured evidence with a delivery path to a human, not more dashboards.*

## One decision, walked through

Judgment doesn't travel unless the reasoning is visible, so here is one engagement decision in the four-question form the studio uses — situation, decision, risk, change.

**Situation.** Five seats had finished the audit: real findings, a live outage root-caused, ledger entries drafted. The cross-vendor red-team gate then **failed the whole thing** — two headline numbers didn't survive attack (the availability figure, the accretion math), and the gate named a question all five seats had missed. The findings *felt* done. The evidence said otherwise.

**Decision.** Redraft under escalation and re-measure everything the gate touched, then submit to the gate again — twice more, as it turned out. Rejected: shipping round one with caveats (the falsified numbers were headline claims, not footnotes), and defending the original figures (the protocol treats "defend" as legal only when re-measurement backs it).

**Risk.** Three adversarial rounds cost real time and tokens, and re-measurement could have weakened the audit's verdicts. Accepted, because an audit that can't survive its own skeptic isn't deliverable — it's a liability with confident formatting.

**Change.** The availability figure moved from 33% to a persisted, per-night-sourced 49.6%; the root cause moved to where the evidence actually pointed; the gate's miss-list produced the engagement's most consequential finding; and every surviving claim became auditable rather than merely plausible. The redrafts made the audit *stronger* under attack — which is the property that makes it worth reading.

---

Built along the [Systemcraft build map](https://github.com/seanwinslow28/code-brain/issues/142) — every design decision on this studio is itself recorded as a closed, ratified ticket. Charting the route is the same craft the studio sells.
