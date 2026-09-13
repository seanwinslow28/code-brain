# The bench

Seven specialist seats, run as a **sequential pipeline with full artifact context handed forward** — never a parallel panel, never a summary. Each seat owns one artifact contract, one template, one lane manifest, one audit duty, and a baseline model. The master skill owns the process (phases, routing, gates, deviations); [`productcraft/CLAUDE.md`](../CLAUDE.md) owns the law (public/private split, explain-why and the canon line, Insights never decides, full artifacts forward, the two audit cycles, one invocation one seat); these files own the craft. Authored on the build map's [Author the seven-seat bench](https://github.com/seanwinslow28/code-brain/issues/275) ticket (2026-09-13) from the contracts of [#266](https://github.com/seanwinslow28/code-brain/issues/266), the baselines of [#267](https://github.com/seanwinslow28/code-brain/issues/267) and the lane slugs of [#270](https://github.com/seanwinslow28/code-brain/issues/270).

| # | Seat | Produces | Baseline | Audits | Co-sign touches |
|---|---|---|---|---|---|
| 1 | [Product Strategist](product-strategist.md) | Strategy & POV doc | Opus 5 | Leadership packet (anchor: the decision memos) | Co-signs Delivery's OKR translation at stage 6 |
| 2 | [Discovery Lead](discovery-lead.md) | Discovery packet — plan + opportunity solution tree + evidence | Opus 5 | Strategy & POV doc | Its evidence is co-signed by Insights |
| 3 | [Insights & Analytics](insights-analytics.md) | Metrics & evidence plan | Opus 5 | Growth model & GTM plan (anchor: the experiments) | Co-signs Discovery's evidence; its outcome-to-metric table is the stage-3 check on the Strategy doc |
| 4 | [Growth & Distribution Architect](growth-distribution.md) | Growth model & GTM plan | Sonnet 5 | Business case | — |
| 5 | [Business & Economics Modeler](business-economics.md) | Business case — pricing & packaging + unit-economics model | Sonnet 5 | Outcome roadmap | — |
| 6 | [Delivery & Execution Lead](delivery-execution.md) | Outcome roadmap, then the handoff verdict; the execution breakdown after Systemcraft's return | Sonnet 5 | Metrics & evidence plan | Its OKR translation is co-signed by the Strategist |
| 7 | [Product Leadership & Org Designer](product-leadership.md) | Leadership packet — stakeholder map + decision memos + operating-model doc | Opus 5 | Discovery packet (anchor: the discovery plan) | — |

**Two closed audit cycles**, every audit a fresh-context invocation over artifacts only, on the auditor's own baseline, firing the moment its artifact is final (trailing) — Discovery's audit of the Strategy doc is the one that waits, for stage 2's evidence:

- **Cycle A:** Strategist → Leadership → Discovery → Strategist
- **Cycle B:** Insights → Growth → Business → Delivery → Insights

Every seat audits exactly one artifact and is audited by exactly one peer. The three co-sign touches are not audits: a co-sign is a second pair of eyes on one named section before the artifact is done. **The red-team gate is not a seat** — it runs stateless on the vendor that did not last write its anchor artifact, per the inherited [protocol](../../systemcraft/templates/red-team-protocol.md) and the master skill's schedule.

**What an invocation carries** (rule 7): the seat file below, the [seat preamble](../templates/seat-preamble.md) verbatim (explain why, name the canon, declare grounding, loop back never rewrite, close with `## Moves`, meter yourself — standing behavior lives there and is restated nowhere), the lane manifest, the declared target, and the upstream artifacts. Never the drafting conversation. The `model:` line in each file names the runtime that actually runs; a deviation is a per-pass change against one of the four named triggers, never silent.

**Baselines, in one line** (#267): 4 Opus / 3 Sonnet — judgment-heavy seats on Opus 5 (framing, open-ended synthesis, evidence grading, stance prediction), corpus-carried and structured seats on Sonnet 5. Escalation goes one tier — Sonnet 5 → Opus 5 → Codex GPT-5.6 Sol High → Codex Sol xhigh → ask Sean — only on a gate FAIL, an audit that bounced substance, a thin lane decided at Route, or Sean's word. Haiku 4.5 is the downshift floor, never a baseline.
