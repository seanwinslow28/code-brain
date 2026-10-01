# The handoff contract — how one -craft team hands work to another

The law every crossing between two -craft teams shares. One team frames a question it does not own; the team that owns it does the work; the work comes back and the first team carries it on. Ratified 2026-09-11 on the Productcraft build map's [The Systemcraft handoff contract](https://github.com/seanwinslow28/code-brain/issues/271) ticket (six decisions), and split into this generic law plus one **binding** per pair on [craftwork build 3](https://github.com/seanwinslow28/code-brain/issues/326) (2026-10-01), per the [Method extraction: craftwork](https://github.com/seanwinslow28/code-brain/issues/282) ruling (decisions 5 and 6). It moved here from `productcraft/templates/handoff-contract.md`.

**One rule above the rest:** typed artifacts and references cross; reasoning never does. Neither team reads or writes inside the other's ledger. Each side writes only its own cross-reference fields ([ledger-entry.md](templates/ledger-entry.md), Cross-studio references).

**This file is the law; a binding is the pair.** Everything here holds for every crossing. What differs from pair to pair lives in the sending team's binding: which artifacts cross, which seats send and receive, what triggers it, which gate the return waits on, and which process parts are stripped from the copies (§ 9). A team that receives without a binding for the pair cannot take the crossing: it issues `rejected` and names the missing binding.

| Pair | Binding (outbound) | Mirror (return) |
|---|---|---|
| Productcraft → Systemcraft | [productcraft/templates/handoff-binding-systemcraft.md](../productcraft/templates/handoff-binding-systemcraft.md) | [systemcraft/templates/handoff-return.md](../systemcraft/templates/handoff-return.md) |

The reverse crossing, Systemcraft handing Productcraft a product-framing ask, is a second binding when an engagement first needs it, not a new contract.

## 1. What crosses: the brief plus frozen copies

The **brief** is a typed packet of references. It is never a summary, and the artifacts are never pasted into it. With it travel **frozen copies** of the artifacts the binding names, each stamped with its source id and two hashes.

**Copies cross without their process parts.** A seat's artifact holds two things: the content the receiving team works from, and the trace of how it got there (the `## Moves` section, repair notes, audit and co-sign dispositions, loopbacks, check history in the frontmatter). The trace is reasoning, so it stays home. The binding names those parts, and the kit's `freeze.py` strips exactly what the binding names and nothing else (§ 6). Anything a binding does not name crosses. A process note that leaks past the strip list is caught by the outbound gate's *reasoning that crossed* attack, and the fix is a new line in the binding, never a hand-edit of the copy.

The receiving team's seats read the copies in full and work from the sender's graded evidence. They never re-run its discovery or re-litigate its decision. The hash makes "which version did we work against" a fact: an artifact edited after the crossing does not move the target, and a material change is a new crossing.

**Stays behind, by design:** raw evidence (interview notes, transcripts, data), because the graded claims cross and the pointers stay resolvable on this disk, so no transcript is duplicated into a second private repo. Also left behind are audit and co-sign records, ledger entries (referenced by id only), the stripped process parts, and anything the binding lists as its own.

## 2. When it fires, and a verdict either way

The binding names the trigger and the seat that files it. The decision to hand off is a ledger entry with a one-line why, on that seat (`hands_off_to: <receiver-eng-id>`). **A no-handoff verdict is written too.** Where the trigger was checked and did not fire, the same entry says so with `hands_off_to: none`, so silence is never ambiguous.

## 3. Checks: the gate on the way out, the intake check on arrival

- **Outbound gate.** The red-team gate ([red-team-protocol.md](templates/red-team-protocol.md)) fires on the brief before it crosses; the brief is the anchor artifact, and the gate runs on the vendor that did not last write it ([law.md § Model delegation](law.md)). FAIL → redraft one tier up, re-gate.
- **Intake check.** The receiving seat (the binding names it, for the brief and for the return) runs one fresh-context pass at its own Open and issues the crossing's state with a one-line why. It asks exactly one thing: *can I do my job from this packet?* It never asks whether the other team's decision was right; that is the boundary. It runs on the receiving seat's baseline and is a check, not an audit: it appears under `## Checks` as `intake · <seat> · <state>`. Its first act is `freeze.py verify` on every inbound copy.
- **A repair that changes the ask re-gates; a repair that fills a named gap does not.**

## 4. The five crossing states

Typed, never prose-only. Borrowed from the protocol prior art, where "I will not do this" and "I need more from you" are first-class outcomes.

| State | Issued by | Meaning |
|---|---|---|
| `accepted` | Receiving seat at Open | An engagement is opened (or the return is taken up). `originates_from` is set on the receiver's brief record and every entry |
| `input-required` | Receiving seat at Open | Bounced to the sender with named gaps; no engagement opened. The sender repairs and re-crosses |
| `rejected` | Receiving seat at Open | Declined with the reason (the ask is not in a lane the receiver owns; the constraints contradict each other; no binding exists for the pair); no engagement opened. The sender records it and retypes or drops |
| `returned` | Receiver, at its Close | The work is complete; the return packet is in the sender's `handoff/inbound/` |
| `returned-partial` | Receiver, at its Close | A lane was deferred, named, with its rule-8 ticket; the rest is returned |

The state is a typed record, not reasoning, so the issuing seat writes it into **both** teams' `handoff/` folders (`crossing.md`, one line per state change: state · date · seat · why) and into its own Open or Close entry. A return date that cannot be met is a variance question to Sean before the date, never a silent overrun.

## 5. What comes back: the mirror

The return fires at the receiver's gate the binding names. It is the last gate that can pass before an implementation exists, so any later gate stays the receiver's to fire once the sender's follow-on work creates something to gate.

The return packet mirrors the outbound: a typed **return note** (the binding's mirror template) plus frozen copies of the receiver's artifacts, stripped by the mirror's own strip list and hashed the same way. The note carries one answer per ask question, by id; the gate verdict and any acceptances; every receiver decision id that overturns a sender assumption, each naming the sender entry it supersedes; the open holds the follow-on work must close; and the state.

**Reading the return.** The sender's receiving seat takes it up at the Open of its follow-on engagement. It runs the intake check, writes `informed_by: [<receiver-ids>, …]`, and flips each overturned entry of its own to `status: superseded` with `superseded_by: <receiver-id>`. That is a status change, not a new decision. If an overturn demands a new decision in the sender's own lane, that is a loopback to the owning seat as a one-off, never a rewrite in place. When the follow-on work produces the thing the receiver's later gate needs, the sender drops a one-line `candidate-note.md` into the receiver's inbound folder (tracker link, date).

## 6. Folder layout, the strip and the hash

Both ledgers keep the same shape under each engagement; each team writes its own side.

```
handoff/
├── crossing.md                 # state log: state · date · seat · why — one line per change
├── outbound/                   # what this team sent
│   ├── brief.md | return.md    # the typed packet
│   ├── manifest.md             # the table freeze.py prints: source id · copy · source sha256 · copy sha256 · stripped
│   └── artifacts/              # the frozen copies, named <source-id>--<slug>.md
└── inbound/                    # what this team received: the same three parts
```

A copy is frozen with the shared kit ([craftwork/trace/freeze.py](trace/freeze.py)), never by hand:

```
python3 craftwork/trace/freeze.py show --binding <binding.md> <artifact.md>      # what would be stripped; writes nothing
python3 craftwork/trace/freeze.py copy --binding <binding.md> --out handoff/outbound/artifacts \
    <artifact.md>=<source-id> [...]                                               # writes the copies, prints manifest.md
python3 craftwork/trace/freeze.py verify <copy.md>[=<artifact.md>] [...]          # the intake check's first act
```

It strips the parts the binding's `strip` block names, then takes `sha256` of what is left. That is the **copy hash**. It also takes `sha256` of the artifact file as it stood, the **source hash**, so the sender can show which revision crossed. Both go into the manifest and into five stamp lines at the top of the copy's frontmatter: `frozen_from`, `sha256` (the copy hash), `source_sha256`, `frozen_at`, and `stripped` (the names of what was removed: headings and directive labels, never their content). The copy hash covers the copy without those five lines, so `verify` removes them and re-hashes. Artifact ids follow each team's artifact templates (`pc-eng-NNN.<artifact-slug>` in Productcraft, `eng-NNN.<artifact-slug>` in Systemcraft).

**Copies frozen before this rule stand.** Productcraft's second engagement crossed verbatim copies to Systemcraft's eng-005 on 2026-09-30, accepted once by Sean as `pc-eng-002.d191`. They carry three stamps and no `source_sha256`, they verify unchanged, and they do not re-cross. The rule first applies to eng-005's return (due 2026-12-04).

## 7. Cross-references and the outcome rule

Field names are fixed by the ledger schema: the sender writes `hands_off_to` and `informed_by`, and flips `superseded_by` on overturned entries; the receiver writes `originates_from` on its brief record and entries, and `supersedes_external` at the overturning decision. Ids cross; nothing else does.

D+14 ([law.md § Standing success measure](law.md)): a crossing is **not** an outside-use event for the sender, because it stays inside the org. Work the return makes possible can be, and the binding names what counts.

## 8. The receiving team's side

A handoff is not a new engagement type. It is a **handoff modifier** on the receiver's existing types (the same device as the self-targeted modifier). At Open it brings the intake check and state, `originates_from` everywhere, the frozen copies as the seats' upstream artifacts, no re-run of discovery and no re-litigation of the sender's decision. At Close it brings the return note and its stripped copies packaged into the sender's inbound folder, `supersedes_external` written where a decision overturned a sender assumption, and any later gate left explicitly not fired until the candidate note arrives. The modifier's text lives in the receiver's master skill; this file is its authority.

## 9. What a binding names

A binding lives in the sending team's `templates/`, one per pair, and is short. It names:

1. **The artifacts that cross**, by id and owning seat, and anything of its own that stays behind.
2. **The trigger** (or triggers), the seat that files the handoff, and how the receiver takes it (which of its engagement types the modifier rides on).
3. **The seats**: who drafts the brief, who issues the state on arrival, who reads the return.
4. **The return's gate**: which receiver gate fires the return, and which later gate waits on the candidate note.
5. **What counts at D+14** for the receiver's engagement.
6. **The strip list**: a fenced `strip` block naming the process parts of the sending team's artifacts. Its mirror (the return template) carries the receiver's block for its own artifacts.

The `strip` block takes five directives, one per line:

| Directive | Strips |
|---|---|
| `heading: ## Moves` | the section under a heading of that level whose text is the name, or starts with it plus a space (`## Loopbacks` also takes `## Loopbacks to the Strategist`), down to the next heading of the same or a higher level |
| `heading-ending: ## dispositioned` | the section under a heading of that level whose text ends with the word |
| `heading-tag: [Δ` | a bracketed span opening with this text, removed from every kept heading line (the heading itself stays) |
| `paragraph: **Repair note` | a blank-line-delimited paragraph whose first line opens with this text |
| `key: audit` | a frontmatter key, with its continuation lines |

Headings and paragraphs inside fenced code are never matched. A binding with no `strip` block is refused: nothing is stripped by guess.
