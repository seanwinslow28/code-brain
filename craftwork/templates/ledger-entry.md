# Ledger entry template

Every -craft team's decision-ledger entry. One file per **material decision**, written by the deciding seat at the moment of decision (Run) or by the master skill at Close. Entries are **private** (`<x>craft/ledger/`, gitignored, each team's own local git repo backed up to a private `seanwinslow28/<x>craft-ledger` remote); this template is public machinery. Schema ratified 2026-09-10 on the Productcraft build map's [Decision-ledger schema with the canon line](https://github.com/seanwinslow28/code-brain/issues/268) ticket, as an extension of Systemcraft's first entry by one section and a handful of fields. Shared law since 2026-10-01 ([craftwork build 1](https://github.com/seanwinslow28/code-brain/issues/324), moved from `productcraft/templates/`). Systemcraft adopted it on 2026-10-01 ([craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327)), retiring its own older entry; entries written before that keep the older shape and are not retrofitted.

A decision is *material* when it survives the engagement: someone could later ask "why is it built this way?" and this entry is the answer.

**Brevity law (inherited, Systemcraft 2026-08-24):** an entry is a record, not an essay — every section reads in a breath. Depth is generated on demand from the entry, its artifact, and the corpus; never stored here.

**Canon law** ([law.md § Name the canon](../law.md#name-the-canon)): every entry names what the seat leaned on from the canon — a title and the idea, in the seat's own words. Never the book's text, never a paraphrase of a source's substance. That is what keeps a `publishable: published` entry safe.

```markdown
---
id: pc-eng-001.d03                   # <engagement>.d<seq> — <two letters>-eng-NNN.dNN; permanent, citable, never renamed; no letter suffixes
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-20
seat: discovery-lead                 # the owner; `coordinator` for the coordinator's own decisions
artifact: artifacts/discovery-packet.md   # the artifact this decision shaped
model: claude-opus-5-5                 # the runtime that actually ran, plus any deviation: "claude-opus-5-5 → codex gpt-5.6-sol high: gate FAIL"
grounding: full                      # full | manifest-only | none  (see the degradation ladder below)
status: decided                      # proposed | decided | superseded | reopened
ratified: null                       # date Sean signed it, else null — a field, not a state
supersedes: null                     # id this entry replaces; a redo is a new entry, never a suffix
superseded_by: null                  # id that replaced this one (may be a Systemcraft id — see cross-refs)
consulted: [insights-analytics]      # seats whose input shaped it (two-way)
informed: [delivery-execution]       # seats that received it (one-way)
hands_off_to: null                   # sender side: the receiving studio's engagement id, on the entry that files a handoff brief
informed_by: []                      # sender side: the receiving studio's entry ids read back after a return
originates_from: null                # receiver side: the sender's brief id, on every entry of an engagement opened from a handoff
supersedes_external: null            # receiver side: the sender's entry id this decision overturns
publishable: no                      # no | candidate | published (Sean's per-entry call)
canon: [continuous-discovery-habits] # title slug(s) named in "From the canon", for index and teach-mode retrieval
tags: [discovery, evidence]
---

## Decision

One sentence, active voice: what was chosen.

## Options considered

- **The winner** — one-line tradeoff.
- **The loser(s)** — one line each. The losers are what "why" is measured against.

## Why

Why A over B, one breath, in terms a future reader can weigh.

## From the canon

*Title* (Author) — the idea, in this seat's words, and what this decision did with it.
One title normally, two at most. Never omitted: when nothing applies, say
"None — reasoning from the evidence" or "None — no lane covers this".
On `manifest-only` grounding, end the line with "(manifest only, not read this pass)".

## Evidence

Lane-manifest refs, raw-evidence pointers, live data, incident history — what grounded this.
On `manifest-only` or `none` grounding: name the sources that *would* have grounded it.

## Checks

One line per check: type (audit | co-sign | gate) · seat or vendor · verdict · material defects and how they were resolved.
"Not yet checked" is a legal state — never a silently omitted section.

## Revisit when

Named conditions that reopen this decision (a metric mark, a customer signal, a model release, a date). This is the decision memo's reversal condition.
```

## Degradation ladder

Declared in `grounding:`; the seat never fabricates a pointer into a corpus it could not open.

| Rung | When | Canon section | Evidence section |
|---|---|---|---|
| `full` | The seat read the private corpus this pass | Title and idea, in the seat's words | Lane-manifest refs and raw-evidence pointers |
| `manifest-only` | Corpus absent, tracked lane manifest present (fresh clone, employer machine) | Title and idea from the manifest's when-to-read line, marked "(manifest only, not read this pass)" | What would have grounded it, by name |
| `none` | No manifest covers the question | "None — no lane covers this" | Tracked knowledge only, said plainly |

## Cross-studio references

Only ids cross; each studio writes its own side, never the other's ledger. A field that does not apply stays `null` / `[]`.

| Side | Field | Written by | When |
|---|---|---|---|
| Sender | `hands_off_to: <receiver engagement id>` | The sending seat, on the entry that files the handoff brief | Brief crosses |
| Sender | `informed_by: [<receiver entry ids>]` | The seat that reads the return | Return read |
| Sender | `status: superseded` + `superseded_by: <receiver entry id>` | Same seat | A receiver decision overturned one of the sender's assumptions |
| Receiver | `originates_from: <sender brief id>` | The receiver, on its brief and every entry | Engagement opened from a handoff |
| Receiver | `supersedes_external: <sender entry id>` | The receiving seat that overturned it | At its decision |

**Ids.** Every team's ids carry its two-letter prefix (`pc-eng-NNN` for Productcraft). Systemcraft's bare `eng-NNN` ids are grandfathered and stay unique because Systemcraft is the only unprefixed studio. The handoff contract owns the trigger, timing, and templates on both sides; this file fixes the field names. Productcraft → Systemcraft is the first pair: Productcraft's Delivery seat writes the sender side, Systemcraft's Design Strategist the receiver side.

## Lifecycle

`proposed` — a decision memo awaiting Sean · `decided` — the seat's call, made · `superseded` — replaced, chain in `supersedes:`/`superseded_by:` · `reopened` — a Revisit-when condition fired. Sean's sign-off is the dated `ratified:` field, so the Leadership seat's memo state "ratified" reads as `decided` with `ratified:` set.

## Related law

- **D+14 outcome rule**: [law.md § Standing success measure](../law.md#standing-success-measure). Close is administrative, success is judged on outside use at Close + 14 days, and a handoff crossing is not an outside-use event for the sender.
- **`publishable:`**: `no | candidate | published`, Sean's per-entry call.
