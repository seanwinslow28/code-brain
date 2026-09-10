# Ledger entry template

One file per **material decision**, written by the deciding seat at the moment of decision (Run) or by the master skill at Close. Entries are **private** (`productcraft/ledger/`, gitignored, its own local git repo); this template is public machinery. Schema ratified 2026-09-10 on the build map's [Decision-ledger schema with the canon line](https://github.com/seanwinslow28/code-brain/issues/268) ticket; it extends [Systemcraft's entry](../../systemcraft/templates/ledger-entry.md) by one section and a handful of fields.

A decision is *material* when it survives the engagement: someone could later ask "why is it built this way?" and this entry is the answer.

**Brevity law (inherited, Systemcraft 2026-08-24):** an entry is a record, not an essay — every section reads in a breath. Depth is generated on demand from the entry, its artifact, and the corpus; never stored here.

**Canon law (L11, 2026-09-09):** every entry names what the seat leaned on from the canon — a title and the idea, in the seat's own words. Never the book's text, never a paraphrase of a source's substance. That is what keeps a `publishable: published` entry safe.

```markdown
---
id: pc-eng-001.d03                   # <engagement>.d<seq> — permanent, citable, never renamed; no letter suffixes
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-20
seat: discovery-lead                 # the owner; `coordinator` for the coordinator's own decisions
artifact: artifacts/discovery-packet.md   # the artifact this decision shaped
model: claude-opus-5                 # the runtime that actually ran, plus any deviation: "claude-opus-5 → codex gpt-5.6-sol high: gate FAIL"
grounding: full                      # full | manifest-only | none  (see the degradation ladder below)
status: decided                      # proposed | decided | superseded | reopened
ratified: null                       # date Sean signed it, else null — a field, not a state
supersedes: null                     # id this entry replaces; a redo is a new entry, never a suffix
superseded_by: null                  # id that replaced this one (may be a Systemcraft id — see cross-refs)
consulted: [insights-analytics]      # seats whose input shaped it (two-way)
informed: [delivery-execution]       # seats that received it (one-way)
hands_off_to: null                   # Systemcraft engagement id, on the entry that files a handoff brief (eng-NNN)
informed_by: []                      # Systemcraft entry ids read back after a return (eng-NNN.dNN)
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

Only ids cross; each studio writes its own side, never the other's ledger.

| Side | Field | Written by | When |
|---|---|---|---|
| Productcraft | `hands_off_to: eng-NNN` | Delivery seat, on the entry that files the handoff brief | Brief crosses |
| Productcraft | `informed_by: [eng-NNN.dNN]` | The seat that reads the return, usually at the execution breakdown's Open | Return read |
| Productcraft | `status: superseded` + `superseded_by: eng-NNN.dNN` | Same seat | A Systemcraft decision overturned a product assumption |
| Systemcraft | `originates_from: pc-eng-NNN.dNN` | Systemcraft, on its brief and entries | Engagement opened from a handoff |
| Systemcraft | `supersedes_external: pc-eng-NNN.dNN` | The Systemcraft seat that overturned it | At its decision |

Productcraft ids carry the `pc-` prefix; Systemcraft's bare `eng-NNN` ids are grandfathered and stay unique because Systemcraft is the only unprefixed studio. Every later -craft team gets its own prefix. The handoff contract ticket owns the trigger, timing, and templates on both sides; this file fixes the field names.

## Lifecycle

`proposed` — a decision memo awaiting Sean · `decided` — the seat's call, made · `superseded` — replaced, chain in `supersedes:`/`superseded_by:` · `reopened` — a Revisit-when condition fired. Sean's sign-off is the dated `ratified:` field, so the Leadership seat's memo state "ratified" reads as `decided` with `ratified:` set.

## Inherited unchanged

- **D+14 outcome rule** (Systemcraft master skill, eng-003): Close is administrative; success is judged on outside use at Close + 14 days with the P0-equivalent denominator frozen at Close. One Productcraft clarification: a handoff crossing to Systemcraft is *not* an outside-use event (it stays inside the org); the execution breakdown filing issues in the target's tracker *is* dependent work begun.
- **`publishable:`** — `no | candidate | published`, Sean's per-entry call.
