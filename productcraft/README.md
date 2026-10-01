# Productcraft

*a product leadership studio*

A seven-seat specialist bench for product leadership work: strategy, discovery, evidence, growth, business economics, delivery, and the leadership decisions that hold them together. It plans, executes, and audits, and it explains every material choice, because the work is also the demonstration. Built by Sean Winslow (a PM, not a dev) as the second studio on the [Systemcraft](../systemcraft/README.md) method. Systemcraft designs AI systems; Productcraft decides what is worth building and hands the AI layer across.

## The bench

Seven seats, run as a sequential pipeline. Each seat receives the complete artifacts of the seats before it, never a summary, and owns one artifact contract, one template, one lane of reference reading, and one audit duty.

| # | Seat | Owns | Audits |
|---|---|---|---|
| 1 | [Product Strategist](bench/product-strategist.md) | Strategy & POV doc: diagnosis, point of view, bets, non-goals | Leadership packet |
| 2 | [Discovery Lead](bench/discovery-lead.md) | Discovery packet: plan, opportunity solution tree, evidence | Strategy & POV doc |
| 3 | [Insights & Analytics](bench/insights-analytics.md) | Metrics & evidence plan: what gets measured, and how strong each piece of evidence is | Growth model |
| 4 | [Growth & Distribution Architect](bench/growth-distribution.md) | Growth model & GTM plan, with price held as a hypothesis | Business case |
| 5 | [Business & Economics Modeler](bench/business-economics.md) | Business case: pricing, packaging, unit economics | Outcome roadmap |
| 6 | [Delivery & Execution Lead](bench/delivery-execution.md) | Outcome roadmap and the handoff verdict | Metrics & evidence plan |
| 7 | [Product Leadership & Org Designer](bench/product-leadership.md) | Stakeholder map, decision memos, operating model | Discovery packet |

The audit column forms **two closed cycles**: Strategist → Leadership → Discovery → Strategist, and Insights → Growth → Business → Delivery → Insights. Every artifact gets exactly one adversarial peer reviewer, always fresh-context: an auditor sees the artifacts, never the conversation that drafted them. One boundary rule does a lot of work: **Insights measures and never decides.** It designs the metrics and grades the evidence; the Strategist, Growth, and Business seats decide on its measurements, and the owner decides above them.

## The discipline

- **Sequential, with full artifacts forward.** Seven stages in order. Engagements are typed at Open (full train, audit, execution breakdown, one-off, support landing a role) and the type decides which seats run and which gates fire.
- **Dual-touch co-signs.** Three sections cannot be done by their author alone. Insights co-signs Discovery's evidence against pointers to the raw evidence, and grades each row on a four-rung scale from observed behavior down to inference. The Strategist co-signs Delivery's translation of the strategy into OKRs. Insights' outcome-to-metric table is the check on the Strategy doc before the first gate.
- **Every seat names the canon.** Each material choice ships with a one-breath why-A-over-B and the idea it leaned on from the reference canon: a title and the idea in the seat's own words, never the book's text. That line is the studio's teaching surface.
- **A red team that is a protocol, not a person** ([shared law](../craftwork/templates/red-team-protocol.md)). A full train gates three times: at strategy sign-off, before any handoff, and at close. Each gate runs stateless on the vendor that did not last write the work it judges. A gate that can fail silently is not a gate, so an unavailable vendor gets a labeled fallback and a re-run ticket, never a skip.
- **Checks converge, and the ladder has brakes.** One repair round per artifact per check. The second round verifies the repair and attacks only the text it changed. Escalation fires on severity, never on the number of findings. How this rule was earned is the walked-through decision below.
- **Close is never success.** A train closes administratively, and its outcome is recorded fourteen days later against a pre-registered test: did anyone use the work outside the studio, and does every must-handle finding carry a dated disposition?

## Public machinery, private brain

Everything that shows *how the studio works* is tracked here: [bench/](bench/), [templates/](templates/) (the seven seat artifacts, the leadership seat's hard contracts, check records, gate findings, and the handoff contract), [lanes/](lanes/) (topic-organized shelf labels that double as a reading path), the shared law every -craft team inherits in [craftwork/](../craftwork/README.md) (including the [runtime registry](../craftwork/templates/runtime-registry.md)), and the shared local evals kit in [craftwork/trace/](../craftwork/trace/README.md): one record per invocation, a labels file, deterministic checks, and an offline HTML viewer for reading a whole train. This studio's side of it sits in [trace/](trace/README.md): its profile (the train's shape the kit checks against) and the failure modes its own labels named. The reference corpus (distilled practitioner canon plus ingested books) and the decision ledger stay on local disk. The manifests are shelf labels, never the books. On a machine without the private layers, seats say so plainly and never fabricate a citation.

## The handoff to Systemcraft

Productcraft owns the product decision; [Systemcraft](../systemcraft/README.md) owns the AI system. When the first shipping slice holds a layer Systemcraft owns, the Delivery seat crosses a typed brief plus frozen, hashed copies of the six design artifacts above Leadership. The raw evidence, the audits, and the reasoning stay behind, and so do each artifact's own process notes, stripped from the copies by a shared script before they are hashed. The receiving seat checks the brief fresh and answers with one of five typed states (accepted, input required, rejected, returned, or returned partial), recorded on both sides. When Systemcraft's design is done, the return lands on Delivery, which breaks it into epics, stories, and a first sprint. When no such layer exists, Delivery writes a no-handoff verdict instead ([the contract](../craftwork/handoff-contract.md)).

## Proof: the first engagement

The shakedown was a full-train revisit of 16BitFit, Sean's retro fitness game, run as input to that project's own open decisions ([engagement record](https://github.com/seanwinslow28/code-brain/issues/278)). What the machinery did on contact:

- All seven seats ran in order, both audit cycles closed, and two cross-vendor gates passed the work with acceptances the owner ruled on one by one, each dated.
- Delivery returned a **no-handoff verdict**: the first shipping slice held no AI system, so nothing crossed to Systemcraft.
- The fourteen-day record **passed on time**: the work was used outside the studio, and all five must-handle findings carry dated dispositions. It also says what it does not mean: nothing is built yet and no tester has been contacted.
- Reading the whole train back produced the studio's first two named failure modes. The most common, a measure defined on an event the product's own rules can never produce, led three of five failing passes.

## One decision, walked through

Judgment doesn't travel unless the reasoning is visible, so here is one engagement decision in the four-question form the studio uses: situation, decision, risk, change.

**Situation.** Ten invocations into a budget of twenty-six, the train was still at stage two. Every audit had found something material, every repair drew another audit, and the escalation ladder climbed a model tier on every material one. The Strategy doc was on its third revision with one defect still open: a success measure defined around an app event that the pilot's own no-contact rule never guarantees. Repairing by the book would have spent the budget before stage seven. Sean put the real question plainly: tell a red team it must find flaws, and it will find them, even if it has to make them up.

**Decision.** Stop the loop now and test the suspicion later, on evidence. Take a minimal repair at baseline, cap every check at one repair round for the rest of the train, and carry whatever the cap leaves to the next gate as a visible acceptance. Then read the finished train back before the second engagement and answer whether the checks converge or manufacture. Rejected: repairing by the ladder (it had no stopping rule, so it would breach the budget), and softening the auditors' mandate on a hunch.

**Risk.** A cap can ship real defects, and a suspicion tested after the fact can come back confirmed. Accepted, because capped findings were never dropped. They travelled to the gates as acceptances the owner had to rule on by name. And an adversarial posture that is quietly weakened is worse than one that is measured.

**Change.** The train finished within a budget Sean raised once, on the record. The read-back cleared the auditors: every material finding from the seat audits was a real defect, repaired and verified or accepted with a dated reason, and none was manufactured. One first-sight audit came back with no material findings at all. What had no brakes was the ladder, and what kept feeding it was **repair-induced surface**: every new finding on the re-audit sat in text the previous repair had touched, none in text it had left alone. So the studio's law changed, not its posture. One repair round per check, a verification pass in place of a fresh audit, escalation on severity, and the checker changes vendor rather than the repairer climbing a tier ([the ruling](https://github.com/seanwinslow28/code-brain/issues/296)).

---

Built along the [Productcraft build map](https://github.com/seanwinslow28/code-brain/issues/264). Every design decision on this studio is itself recorded as a closed, ratified ticket.
