---
name: craftwork
description: Build a new -craft team on the shared home at craftwork/. The recipe from partner session to "built" (partner session → $0 research passes → Wayfinder map → scaffold → first full-train engagement → D+14 record → self-targeted check red-teamed on Codex), what every team inherits from craftwork/ and what each team decides for itself, the three-seat floor below which a studio is not built, the voice-bearing declaration, and the naming rule. User-invoked only — run as /craftwork when Sean says "build a new craft team", "does X earn a -craft studio", or names a team to build (designcraft, devcraft, ...). It never fires on its own, and it builds nothing by itself: it hands each step to the skill that owns it.
disable-model-invocation: true
---

# craftwork — the recipe for building a -craft team

A **-craft team** is a specialist bench of at least three seats that plans, executes and audits one kind of work, explains every material choice and names what it leaned on from the canon, and keeps its machinery public and its brain private. Two exist: [Systemcraft](../../../systemcraft/README.md) (AI PM system design, five seats) and [Productcraft](../../../productcraft/README.md) (product leadership, seven seats). This skill is how the next one gets built.

**The skill knows the recipe, `craftwork/` knows the law, each team knows its craft.** The law every team inherits lives once, in [craftwork/law.md](../../../craftwork/law.md), with the shared templates, the handoff law and the trace kit beside it ([craftwork/README.md](../../../craftwork/README.md)). This file never restates it. It says what happens in what order when a team is built, which skill owns each step, and what a team is free to decide. Ruled on the Productcraft build map's [Method extraction: craftwork](https://github.com/seanwinslow28/code-brain/issues/282) ticket (2026-10-01, thirteen decisions) and written on [craftwork build 5](https://github.com/seanwinslow28/code-brain/issues/328) once the shared home had actually landed.

User-invoked only, like `/wayfinder`: it carries `disable-model-invocation`, so no agent runs it unasked. Excluded from export groups, because a team is useless without this repo's shared home, until the showcase-repo ticket in `vault/00_inbox/tickets.md` decides how a team and `craftwork/` ship together.

Sean is a PM, not a dev: plain language, one question at a time, a recommendation with every question.

## First, two questions

Ask these before anything is charted. Both are decided in the partner session, but the recipe stops here if the answers say so.

**1. Does the craft clear the floor?** The audit shape is shared law: every seat audits exactly one artifact and is audited by exactly one peer, fresh-context, in closed cycles ([§ The audit shape](../../../craftwork/law.md#the-audit-shape-and-the-three-seat-floor)). Below three seats a closed cycle cannot carry it. **Do not build a studio below three seats.** Build a skill, or a skill plus the red-team gate ([the protocol](../../../craftwork/templates/red-team-protocol.md)), and stop. A craft that wants a studio must name three seats whose lanes are distinct enough that each can audit a neighbour's work without owning it.

**2. Does its output carry Sean's voice?** A team is **voice-bearing** when the thing it ships is read as Sean (prose, scripts, jokes, posts), and **not voice-bearing** when it ships designs, plans and models that are his decisions but not his voice. Systemcraft and Productcraft declared not voice-bearing. The declaration is made at scaffold and changes what the corpus holds and how an engagement opens (below).

## The recipe

Seven steps, in order. Each is owned by a skill or a map ticket, never by this one. "Built" is defined by the last three.

**1. Partner session.** Run the `creative-partner` skill: Sean and the machine deliberate the team's shape until a set of locks is ratified — the craft, the first seats, the first engagement, the shelf, the audit layout, what the team must never do. The session sidecar is local-only and is **never quoted into a tracked file or an issue**; the locks are summarized as one inbox ticket in `vault/00_inbox/tickets.md`. Nothing after this step re-litigates a lock; new ideas may extend them.

**2. Research passes, at $0.** Run the `research` skill (local Deep Researcher, or `gemini-deep-research` for a compound question), one brief per question, each filed in `vault/20_projects/research/` and ratified by Sean before the map is charted. The three every team needs: **bench composition** (which seats, which audit cycle, what each seat's artifact is), **book-to-seat** (the tier-1 shelf, which titles are DRM-free and ingestible, which are read-only), and **plugin routing** (which installed skills and plugins each seat's toolbelt lists). Add one domain question when the craft has a method of its own (Productcraft added how evals land in discovery). Standing practice: research before any design decision that has documented prior art.

**3. Chart the map.** Sean runs `/wayfinder` himself. The destination is the studio **live plus its first engagement complete**, in the Systemcraft form: root workspace `<x>craft/` holding public machinery and a private brain, blessed by `scripts/validate.py`, with the first full train closed and its findings in the ledger. The map's Notes carry the locks as binding inputs, the research briefs, the design doctrine, the model rule and the privacy law. **The map carries execution**: its tickets are build tasks and engagements, and it closes on delivered work, not a hand-off spec.

**4. Scaffold.** One map ticket, run on `main`:

- Folder `<x>craft/` with `CLAUDE.md` (status, layout table, the team's non-negotiable rules — the inherited ones as one-line pointers into [craftwork/law.md](../../../craftwork/law.md), the team's own in full), a placeholder `README.md`, and `bench/`, `templates/`, `lanes/` holding one placeholder README each that names the map ticket that fills it.
- **The trace profile**: `<x>craft/trace/studio.py` defining `STUDIO` (the numbered stages, the record kinds, which kinds own `## Moves`, the gate seats, the repo path prefixes, the item-id shape, the brief file, where check records sit, and the team's own rung-0 line 8) plus an empty `taxonomy.md`. The kit finds the profile by walking up from the engagement folder ([craftwork/trace/README.md](../../../craftwork/trace/README.md)); Systemcraft's is the smallest example. Seat failure modes are never inherited: the file stays empty until the team's own labels earn one.
- **The private layer**: `corpus/`, `ledger/` and `books/` added to the `PRIVATE LAYER` block of the root `.gitignore` with a dated comment, each holding a local-only README. **Canary before the first commit**: drop a `.md` under each path and a stray `.epub` under `corpus/`, confirm every one with `git check-ignore`, and confirm `git ls-files <x>craft/` lists no private path after the push. `books/` is a guard only; ebooks live at `~/Books/<x>craft/`, outside the repo.
- **The ledger is its own git repo** with a private remote, `seanwinslow28/<x>craft-ledger`, created by Sean. Every session that writes to it pushes there before ending, never to this repo.
- **The blessing**: `<x>craft` added to `ADDITIONAL_WORKSPACES_TO_SCAN` in `scripts/validate.py` with a dated comment, and `python3 scripts/validate.py` passing with no new warning. Then the root README row, the root `CLAUDE.md` architecture line, and a CHANGELOG entry.
- **The master skill** at `.claude/skills/<x>craft/SKILL.md`, by the house rule, excluded from export groups. It owns only what happens when (engagement types, phases, the gate schedule, the Close checklist) and links to the law; it is designed on its own map ticket and written once the bench exists.
- **The voice-bearing declaration**, one line in the team's `CLAUDE.md`, decided in step 1.

**5. Build the machinery.** The map's tickets, in whatever order their edges allow: seat contracts and the bench, artifact templates (every one ends with `## Moves` and a `meter:` line), lane manifests that double as reading paths, the free-canon layer, book ingestion through book-to-skill (official repo only, publish step declined), and the master skill. Each team's corpus and ledger layout is its own ruling. A team that will hand work to another writes one short binding per pair in its `templates/` ([what a binding names](../../../craftwork/handoff-contract.md#9-what-a-binding-names)), and the receiving side's return template carries its own strip list.

**6. The first full-train engagement.** Opened, routed, run, gated and closed by the team's master skill under the shared law: seats pinned to registry rows, the alias probe at Route, one repair round per artifact per check, gates on the vendor that did not write the anchor, Close as `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`. **Traced from pass 1**: one record per invocation, every rung-0 line passing at Close, labels coordinator-drafted and Sean-approved and saying so. The Close's registry line reads every traced engagement of every studio (`find … -name trace` across all of them, never a one-studio glob that would overwrite the others' rows).

**7. Built.** Three things, and the recipe ends:

1. the first full-train engagement has closed;
2. its **D+14 outcome record** is written (the record is required; a PASS is not);
3. one **self-targeted check** — the studio testing its own law against that engagement's trace — has been red-teamed on Codex, under the self-targeted modifier ([§ Self-targeted modifier](../../../craftwork/law.md#self-targeted-modifier)).

Both existing studios' most valuable law changes came from that last step (Systemcraft's third engagement; Productcraft's [checks-converge ruling](https://github.com/seanwinslow28/code-brain/issues/296)). A second engagement and a first handoff are **not** part of the recipe.

## Inherit vs decide

| Every team inherits from `craftwork/` | Each team decides for itself |
|---|---|
| [law.md](../../../craftwork/law.md), all of it: name the canon · the audit shape and the three-seat floor · the standing success measure (D+14) · the availability ladder · the self-targeted modifier · model delegation · the alias probe at Route · checks converge | Seat count above three, and what each seat owns |
| The shared templates: [red-team protocol](../../../craftwork/templates/red-team-protocol.md) · [close digest](../../../craftwork/templates/close-digest.md) · [status vocabulary](../../../craftwork/templates/status-vocabulary.md) · [ledger-entry schema](../../../craftwork/templates/ledger-entry.md) · [runtime registry](../../../craftwork/templates/runtime-registry.md) | The gate schedule (which gates fire when, and their attack checklists) |
| [The handoff law](../../../craftwork/handoff-contract.md): the typed brief, copies stripped then hashed, the five crossing states, `crossing.md` on both sides, the mirror return, ids as the only thing that crosses | The bindings: which artifacts cross to which pair, the trigger, the seats, the strip list |
| [The trace kit](../../../craftwork/trace/README.md): record, labels and cases templates, the rung-0 checker, the viewer, `freeze.py`, `registry.py`, and the shared process-waste failure family | The trace profile (stages, kinds, brief file, record folders, line 8) and every seat failure mode, earned from the team's own labels |
| The two engagement modifiers: self-targeted, and handoff (sending or receiving) | Engagement types, the audit-cycle layout, lane slugs, artifact templates, corpus shape (beyond the own-work layer below) |
| The private-layer plumbing, the ledger-as-own-repo rule, the master-skill house rule, the naming rule | The team's own rules (Productcraft's "Insights measures, never decides"; Systemcraft's "summaries never outrun the record") |

A team's `CLAUDE.md` and master skill **link** to a section of the law and may add to it (a stricter rule, a studio binding). They never restate or contradict it, and they never keep a copy. Systemcraft shows what a team decides on top of a full inheritance: its own brief file, its own check-record folder, an extra `intake` kind, and a line 8 that reads a co-sign as the PRD's audit.

## The voice-bearing declaration

Decided in the partner session, written at scaffold, and deliberately not strict.

**The corpus gains an own-work layer.** The canon teaches what good craft looks like; Sean's own work teaches his voice. A suggestion that improves the craft but flattens the voice into something generic is a **failure, not a trade-off**. The team's seats are real creative partners who know what a good script or joke looks like while still knowing his voice.

**`generic-drift` is sighted, not coded.** It goes in the team's `taxonomy.md` as a sighted shape from day one and earns a code only when labels show it leading a fail, the same rule every seat failure mode follows.

**Every engagement declares its mode at Open.** Two modes:

- **Critique** — Sean brings a draft. Seats diagnose and offer labelled options beside his text; they never rewrite it in place.
- **Draft from seed** — Sean brings an idea, a premise or a beat sheet. Seats write a draft for his pass.

Either way the loop is train → Sean's pass → back to the train, and a piece is finished when Sean calls it finished. Systemcraft and Productcraft declared not voice-bearing and change nothing.

## The naming rule

Folder `<x>craft/`, master skill `<x>craft`, ledger ids `<two letters>-eng-NNN` (Productcraft's are `pc-eng-NNN`; Systemcraft's bare `eng-NNN` ids are grandfathered), private ledger remote `seanwinslow28/<x>craft-ledger`.

## What craftwork deliberately does not encode

Seat count above the floor of three; corpus shape, beyond the own-work layer for voice-bearing teams; lane slugs; artifact templates; engagement types (only the self-targeted and handoff modifiers are inherited); the gate schedule; the audit-cycle layout; each team's own rules. A rule that two teams both need, phrased the same way, is a candidate for `craftwork/law.md`, moved there on its own ticket with its origin named, never copied.

## Where the pieces are

| Piece | Path |
|---|---|
| The law | [craftwork/law.md](../../../craftwork/law.md) |
| The shared home's index and the *Moved here* table the kit reads | [craftwork/README.md](../../../craftwork/README.md) |
| The handoff law | [craftwork/handoff-contract.md](../../../craftwork/handoff-contract.md) |
| The trace kit and its Close ritual | [craftwork/trace/README.md](../../../craftwork/trace/README.md) |
| The two built teams, as worked examples | [systemcraft/](../../../systemcraft/README.md) · [productcraft/](../../../productcraft/README.md) |
| The first scaffold, step by step | Productcraft's [Workspace scaffold](https://github.com/seanwinslow28/code-brain/issues/265) ticket |
| Which crafts come next | the roster deep dive and the Designcraft and Devcraft exploration tickets in `vault/00_inbox/tickets.md` |

## Degradation

On a machine without the private layers (a fresh clone, an employer machine), the recipe still reads end to end: everything it names is tracked except the corpus and ledger a team will fill. Say so once and continue. Never fabricate a lock, a ledger precedent or a corpus citation that cannot be read, and never name a client, an employer or the startup in a tracked file.
