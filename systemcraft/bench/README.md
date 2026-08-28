# The bench

Five specialist seats, run as a **sequential pipeline with full artifact context handed forward** — never a parallel panel. Each seat owns one artifact contract, one template, one corpus lane, and one audit duty. The master skill owns the process (phases, routing, deviations); `systemcraft/CLAUDE.md` owns the law (boundaries, explain-why, fresh-context audits); these files own the craft.

| # | Seat | Produces | Baseline | Audits |
|---|---|---|---|---|
| 1 | [Design Strategist](design-strategist.md) | PRD | Opus | Failure-UX spec + model card |
| 2 | [Architecture Advisor](architecture-advisor.md) | ADR | Opus | Ops model + runbook |
| 3 | [Interaction & Trust Designer](interaction-trust-designer.md) | Failure-UX spec + model card | Sonnet | Eval plan |
| 4 | [Evals & Evidence Architect](evals-evidence-architect.md) | Eval plan | Opus | PRD (the dual-touch co-sign) |
| 5 | [Ops & Economics Modeler](ops-economics-modeler.md) | Ops/economics model + incident runbook | Sonnet | ADR |

The audit column is a closed cycle — each seat audits exactly one artifact and is audited by exactly one peer, always in fresh context. The red-team gate is not a seat: it runs stateless on Codex per [the protocol](../templates/red-team-protocol.md).
