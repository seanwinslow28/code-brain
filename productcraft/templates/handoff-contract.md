# The Systemcraft handoff contract

The one contract between Productcraft and Systemcraft. Productcraft frames the problem and the business case; Systemcraft designs and proves the system; Productcraft reads the design back and turns it into buildable work. Ratified 2026-09-11 on the build map's [The Systemcraft handoff contract](https://github.com/seanwinslow28/code-brain/issues/271) ticket (six decisions). This is the law; the two packets that cross are [handoff-brief.md](handoff-brief.md) (outbound) and Systemcraft's [handoff-return.md](../../systemcraft/templates/handoff-return.md) (inbound). Every later -craft team that hands to Systemcraft inherits this file; only the prefix and the seat names change.

**One rule above the rest:** typed artifacts and references cross; reasoning never does. Neither studio reads or writes inside the other's ledger. Each side writes only its own cross-reference fields ([ledger-entry.md](ledger-entry.md), Cross-studio references).

## 1. What crosses — the brief plus frozen copies

The brief is a typed packet of references, never a summary and never the artifacts pasted in. With it travel **frozen copies** of the six design-train artifacts above Leadership, verbatim, each stamped with its source id and a content hash:

| # | Artifact | Owner |
|---|---|---|
| 1 | Strategy & POV doc | Product Strategist |
| 2 | Discovery packet, co-signed | Discovery Lead |
| 3 | Metrics & evidence plan | Insights & Analytics |
| 4 | Growth model & GTM plan | Growth & Distribution Architect |
| 5 | Business case | Business & Economics Modeler |
| 6 | Outcome roadmap, OKR section co-signed | Delivery & Execution Lead |

Systemcraft's seats read the copies in full, so its Design Strategist writes the PRD's problem, users and assumptions from Productcraft's graded evidence and never re-runs discovery. The hash makes "which version did Systemcraft design against" a fact: a Productcraft artifact edited after the crossing does not move the target, and a material change is a new crossing.

**Stays behind, by design:** raw evidence (interview notes, transcripts, data) — the graded claims cross, the pointers stay resolvable on this disk, and no transcript is duplicated into a second private repo; audit and co-sign records; ledger entries (referenced by id only); the Leadership packet (written after the brief, about the org, not the system).

## 2. When it fires — two triggers, and a verdict either way

| Engagement | Trigger | Seat | Systemcraft receives it as |
|---|---|---|---|
| Full train | The roadmap's first shipping slice contains a **Systemcraft-owned layer** — an AI system, a platform, a technical architecture | Delivery, right after its OKR section is co-signed at stage 6, before Leadership runs | *Design a new project* |
| Audit | A material finding lands in a Systemcraft-owned lane | The closing seat, at Close | *Audit / improve an existing system* |
| One-off, support a role | Never. A one-off that surfaces a Systemcraft question stops and retypes | — | — |

The decision to hand off is a ledger entry with a one-line why, on the seat that files it (`hands_off_to: eng-NNN`). **A no-handoff verdict is written too** — the same entry reads "no handoff: no Systemcraft-owned layer in the first slice" with `hands_off_to: none` — so silence is never ambiguous, and the Leadership packet's stakeholder map states Systemcraft absent rather than omitting the row.

## 3. Checks — the gate on the way out, the intake check on arrival

- **Outbound gate.** The Codex red-team gate fires on the brief before it crosses; the brief is the anchor artifact. Delivery drafts on Sonnet, so the vendor rule puts the gate on Codex with no special case. FAIL → redraft one tier up, re-gate.
- **Intake check.** The receiving seat — Systemcraft's Design Strategist for a brief, Productcraft's Delivery seat for a return — runs one fresh-context pass at its own Open and issues the crossing's state with a one-line why. It asks exactly one thing: *can I do my job from this packet?* It never asks whether the other studio's decision was right; that is the boundary. It runs on the receiving seat's baseline and is a check, not an audit: it appears under `## Checks` as `intake · <seat> · <state>`.
- **A repair that changes the ask re-gates; a repair that fills a named gap does not.**

## 4. The five crossing states

Typed, never prose-only. Borrowed from the protocol prior art, where "I will not do this" and "I need more from you" are first-class outcomes.

| State | Issued by | Meaning |
|---|---|---|
| `accepted` | Receiving seat at Open | An engagement is opened (or the return is taken up). `originates_from` is set on Systemcraft's brief and every entry |
| `input-required` | Receiving seat at Open | Bounced to the sender with named gaps; no engagement opened. The sender repairs and re-crosses |
| `rejected` | Receiving seat at Open | Declined with the reason (the ask is not in a Systemcraft-owned lane; constraints contradict each other); no engagement opened. The sender records it and retypes or drops |
| `returned` | Systemcraft, at its Close after Gate 2 | Design complete; the return packet is in the sender's `handoff/inbound/` |
| `returned-partial` | Systemcraft, at its Close | A lane was deferred, named, with its rule-8 ticket; the rest is returned |

The state is a typed record, not reasoning, so the issuing seat writes it into **both** studios' `handoff/` folders (`crossing.md`, one line per state change: state · date · seat · why) and into its own Open or Close entry. A return date that cannot be met is a variance question to Sean before the date, never a silent overrun.

## 5. What comes back — the mirror, after Gate 2

Systemcraft's design engagement gates three times: PRD sign-off, design-complete, pre-launch. Pre-launch cannot fire until an implementation candidate exists, and Productcraft's execution breakdown is what creates one. So the return happens **after Gate 2**, and Gate 3 stays Systemcraft's to fire during the build.

The return packet mirrors the outbound: a typed **return note** ([handoff-return.md](../../systemcraft/templates/handoff-return.md)) plus frozen, hashed copies of Systemcraft's five artifacts — PRD, ADR, failure-UX spec and model card, eval plan, ops/economics model and incident runbook. The note carries: one answer per ask question, by id; the Gate 2 verdict and any acceptances; every Systemcraft decision id that overturns a Productcraft assumption, each naming the Productcraft entry it supersedes; the open implementation holds the build must close; and the state.

**Reading the return.** Delivery takes it up at the execution breakdown's Open: runs the intake check, writes `informed_by: [eng-NNN.dNN, …]`, and flips each overturned Productcraft entry to `status: superseded` with `superseded_by: eng-NNN.dNN` — a status change, not a new decision. If an overturn demands a new *product* decision, that is a loopback to the owning seat as a one-off, never a rewrite in place. When the breakdown files its first implementation issues, Delivery drops a one-line `candidate-note.md` into Systemcraft's inbound folder (tracker link, date) so Gate 3 can be scheduled; Gate 3 remains Systemcraft's.

## 6. Folder layout and the hash

Both ledgers keep the same shape under each engagement; each studio writes its own side.

```
handoff/
├── crossing.md                 # state log: state · date · seat · why — one line per change
├── outbound/                   # what this studio sent
│   ├── brief.md | return.md    # the typed packet
│   ├── manifest.md             # one line per frozen copy: source id · path · sha256 · frozen-at
│   └── artifacts/              # the frozen copies, verbatim, named <source-id>--<slug>.md
└── inbound/                    # what this studio received — same three parts
```

A frozen copy is the file's bytes at crossing time; the hash is `sha256` of those bytes, written in the manifest and in the copy's frontmatter (`frozen_from: pc-eng-001.strategy`, `sha256:`, `frozen_at:`). Artifact ids follow each studio's artifact templates (`pc-eng-NNN.<artifact-slug>` here, `eng-NNN.<artifact-slug>` there).

## 7. Cross-references and the outcome rule

Field names are fixed by the ledger schema: Productcraft writes `hands_off_to` and `informed_by`, and flips `superseded_by` on overturned entries; Systemcraft writes `originates_from` on its brief and entries and `supersedes_external` at the overturning decision. Ids cross; nothing else does.

D+14 (inherited): a crossing is **not** an outside-use event for the sender — it stays inside the org. For Systemcraft's engagement, the execution breakdown filing issues in the target's tracker **is** dependent work begun, and counts.

## 8. Systemcraft's side, in one paragraph

A handoff is not a sixth engagement type. It is a **handoff modifier** on Systemcraft's existing types (the same device as its self-targeted modifier): at Open, the Design Strategist's intake check and state, `originates_from` everywhere, the frozen copies as the seats' upstream artifacts, no re-run of discovery and no re-litigation of the product decision; at Close, the return note and copies packaged into the sender's inbound folder, `supersedes_external` written where a decision overturned a product assumption, Gate 3 left explicitly `NOT FIRED — IMPLEMENTATION ABSENT` until the candidate note arrives. The modifier's text lives in the Systemcraft master skill; this file is its authority.
