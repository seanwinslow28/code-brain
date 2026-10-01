# The bench

Five specialist seats, run as a **sequential pipeline with full artifact context handed forward** — never a parallel panel. Each seat owns one artifact contract, one template, one corpus lane, and one audit duty. The master skill owns the process (phases, routing, deviations); `systemcraft/CLAUDE.md` and the shared [craftwork law](../../craftwork/law.md) own the law; these files own the craft. Each seat's `model:` line names the runtime it actually launches, a ruled row of [the runtime registry](../../craftwork/templates/runtime-registry.md) (re-ruled to the 5.5 generation on [#327](https://github.com/seanwinslow28/code-brain/issues/327), 2026-10-01).

| # | Seat | Produces | Baseline | Audits |
|---|---|---|---|---|
| 1 | [Design Strategist](design-strategist.md) | PRD | Opus 5.5 | Failure-UX spec + model card |
| 2 | [Architecture Advisor](architecture-advisor.md) | ADR | Opus 5.5 | Ops model + runbook |
| 3 | [Interaction & Trust Designer](interaction-trust-designer.md) | Failure-UX spec + model card | Sonnet 5.5 | Eval plan |
| 4 | [Evals & Evidence Architect](evals-evidence-architect.md) | Eval plan | Opus 5.5 | PRD (the dual-touch co-sign) |
| 5 | [Ops & Economics Modeler](ops-economics-modeler.md) | Ops/economics model + incident runbook | Sonnet 5.5 | ADR |

The audit column is a closed cycle — each seat audits exactly one artifact and is audited by exactly one peer, always in fresh context. The red-team gate is not a seat: it runs stateless on the vendor that did not last write its anchor artifact — Codex GPT-5.6 Sol High, pinned, while every seat drafts on Claude — per [the protocol](../../craftwork/templates/red-team-protocol.md) and [Systemcraft's gate schedule](../templates/gate-schedule.md).
