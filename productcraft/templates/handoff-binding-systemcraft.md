# Handoff binding: Productcraft → Systemcraft

Productcraft's side of one pair under [the handoff contract](../../craftwork/handoff-contract.md), the shared law every crossing between -craft teams follows. Productcraft frames the problem and the business case; Systemcraft designs and proves the system; Productcraft reads the design back and turns it into buildable work. The contract holds the law (the brief, frozen copies, the five states, `crossing.md`, the mirror return, ids as the only thing that crosses). This file names only what is particular to the pair (contract § 9). The two packets are [handoff-brief.md](handoff-brief.md) (outbound) and Systemcraft's [handoff-return.md](../../systemcraft/templates/handoff-return.md) (the mirror, with its own strip list). Split out of the old Productcraft contract on [craftwork build 3](https://github.com/seanwinslow28/code-brain/issues/326) (2026-10-01); the pair's rulings date from [#271](https://github.com/seanwinslow28/code-brain/issues/271) (2026-09-11).

## What crosses

Frozen copies of the six design-train artifacts above Leadership, stripped of the process parts named below:

| # | Artifact | Source id | Owner |
|---|---|---|---|
| 1 | Strategy & POV doc | `pc-eng-NNN.strategy` | Product Strategist |
| 2 | Discovery packet, co-signed | `pc-eng-NNN.discovery` | Discovery Lead |
| 3 | Metrics & evidence plan | `pc-eng-NNN.insights` | Insights & Analytics |
| 4 | Growth model & GTM plan | `pc-eng-NNN.growth` | Growth & Distribution Architect |
| 5 | Business case | `pc-eng-NNN.business` | Business & Economics Modeler |
| 6 | Outcome roadmap, OKR section co-signed | `pc-eng-NNN.roadmap` | Delivery & Execution Lead |

Systemcraft's Design Strategist writes the PRD's problem, users and assumptions from the copies' graded evidence and never re-runs discovery.

**Also stays behind** (beyond the contract's list): the Leadership packet, which is written after the brief and is about the org, not the system.

## When it fires, and who sends and receives

| Engagement | Trigger | Files and drafts the brief | Systemcraft receives it as |
|---|---|---|---|
| Full train | The roadmap's first shipping slice contains a **Systemcraft-owned layer**: an AI system, a platform, a technical architecture | Delivery, right after its OKR section is co-signed at stage 6, before Leadership runs | *Design a new project* (`receive_as: design`) |
| Audit | A material finding lands in a Systemcraft-owned lane | The closing seat, at Close | *Audit / improve an existing system* (`receive_as: audit`) |
| One-off, support a role | Never. A one-off that surfaces a Systemcraft question stops and retypes | — | — |

**A layer that already has a design crosses as an audit** (ruled by Sean 2026-09-30 at the Open of Productcraft's second engagement, build map [#281](https://github.com/seanwinslow28/code-brain/issues/281)). When the first slice's Systemcraft-owned layer was already designed by a Systemcraft engagement, the full train's brief does not ask for a new design. It crosses with `receive_as: audit`, which means *reconcile the existing design*: Systemcraft's audit route on that engagement's artifacts, checked against the train's six frozen copies. The ask names the prior engagement by id, and each question says which product decision the existing design has to be checked against. Everything else stays the same: trigger, seat, gate, intake check and states.

**A no-handoff verdict** reads "no handoff: no Systemcraft-owned layer in the first slice" with `hands_off_to: none`, and the Leadership packet's stakeholder map states Systemcraft absent rather than omitting the row.

- **The outbound gate** runs on Codex: Delivery drafts on Sonnet, so the vendor rule puts the gate there with no special case.
- **The intake check on arrival** is Systemcraft's Design Strategist's, at its Open.
- **The return is read by** Productcraft's Delivery & Execution Lead, at the Open of the **execution breakdown** ([execution-breakdown.md](execution-breakdown.md)).

## The return's gate

Systemcraft's design engagement gates three times: PRD sign-off, design-complete, pre-launch. Pre-launch cannot fire until an implementation candidate exists, and Productcraft's execution breakdown is what creates one. So the return fires **after Gate 2 (design-complete)**, carrying Systemcraft's five artifacts: PRD, ADR, failure-UX spec and model card, eval plan, ops/economics model and incident runbook. **Gate 3** is recorded as `NOT FIRED — IMPLEMENTATION ABSENT` until Delivery drops `candidate-note.md` into Systemcraft's inbound folder, which it does when the breakdown files its first implementation issues. Gate 3 remains Systemcraft's.

## What counts at D+14

For Systemcraft's engagement, the execution breakdown filing issues in the target's tracker **is** dependent work begun, and counts.

## What is stripped from the copies

The process parts of Productcraft's six artifacts. Most are named by the [artifact header](artifact-header.md) or the seat templates: the `## Moves` section and its meter line, the red-team checklist, and the frontmatter's check history. The rest are the forms the first two trains wrote their repair trail in: loopback and disposition sections, repair notes at the top of a revision, the corpus-opened and what-was-on-disk lines, and the seat's own P0-equivalent check, whose nominations reach Sean as tickets, not Systemcraft. Product content stays, including inline pointers to check records by id, `## Challenges to the prior work`, and the hand-forward requirements one seat writes to the next. The list was tested against pc-eng-002's six artifacts on 2026-10-01: every named part stripped and every copy verified.

```strip
heading: ## Moves
heading: ## Red-team checklist
heading: ## Loopbacks
heading: ## Audit dispositions
heading: ## Audit NOTE dispositions
heading: ## Repair dispositions
heading: ## Repair notes
heading: ## P0-equivalent check
key: audit
key: cosign
key: gate_1
key: thin_lane
paragraph: **Repair note
paragraph: **Revision
paragraph: Corpus opened
paragraph: What was on disk
paragraph: Hands forward,
paragraph: meter:
```

A seat that writes a new kind of process note writes it under one of these headings or opens it with one of these prefixes ([artifact-header.md](artifact-header.md), Process notes). A note that leaks anyway is the gate's *reasoning that crossed* finding, and the fix is a new line here.
