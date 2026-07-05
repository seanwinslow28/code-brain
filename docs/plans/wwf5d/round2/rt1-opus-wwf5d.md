RT1 preserve-session fix-spec · OPUS + WWF5D · 2026-07-05

# Fix Spec — `preserve-session` skill

**Profile: 4-element floor (fix spec)** — Objective, Desired Outcome, The change per finding (with reasoning-to-carry), What NOT to Change. Sized per the intent-engineering Right-Sizing Decision Rule Row 0. The skill is **interactive-only** (`[agents.preserve_session] enabled = false` in `config.toml`, no launchd schedule), so this is not a scheduled/autonomous change and the full 9-section template is not warranted. Two findings (#6 daily-note format contract, #8 Open-Questions routing) reach into a *downstream contract* — resume-session's read shape and the fleet console's Dataview parse — so those two carry the paired-change protocol and edge up to per-fix reasoning, but the spec as a whole stays at the floor. No autonomy level, hard constraint, or execution limit changes.

---

## Grounding — restated, then used

The task pre-supplies four grounding facts. Restated in my own words, each then does work below (WWF5D §1.1 — consume, don't just restate):

- **(a) For.** Sean runs preserve-session at session end to hand off state with **zero loss** to a future session. It is the **WRITE** half; resume-session is the **READ** half. → This makes *zero-loss* the spec's Objective invariant (WWF5D §6.9): every fix is re-checked against it, and any rule that drops a gathered item (a cap that deletes, a fail-open skip) is a self-contradiction the objective overrides. It also means the reader's *shape* is the target the writer must hit — findings #5, #6, #8 are all "wrote it, but not where/how the reader can use it."
- **(b) Feeds.** Consumers: resume-session + a human reading CLAUDE.md. Three destinations: (1) project CLAUDE.md `## Session Log`; (2) the vault project note's `ai-context` / `<!-- status-update -->` / decisions table / blockers; (3) today's daily note `<!-- claude-sessions -->`. SessionStart inject hooks + a SessionEnd flush hook operate nearby. → This is the seam inventory. I traced each destination to its *point of effect* (WWF5D §2.3): resume-session's exact extract list (its lines 26/30/33), the daily anchor's Dataview parser, and the flush hook's *actual* write target. Two of those traces broke the skill's stated assumptions (see #6 and #8).
- **(c) Disappoints.** Resume misses captured items; you can't tell if vault/daily writes landed; the skill **always reports "saved"** though the hand-off is lossy. → This is the `dangerously-wrong` core: silent × trusted × propagating (WWF5D §4). The confirmation is believed, and it's wrong on the failure path — which is *most* paths, since `## Session Log` has landed in **zero** CLAUDE.md files across the tree (verified).
- **(d) Wow.** Zero-loss reconstruction **in the reader's shape**, with **per-destination confirmation** that each write landed or was **skipped-with-a-reason**. → This is the Desired Outcome, verbatim in intent. "Skipped-with-a-reason" (never a silent skip, never a false "saved") is the load-bearing phrase every fix serves.

**Live-system checks I ran before writing** (WWF5D §1.3 — expand to first-degree references, inspect measured state):
- `grep -rl "## Session Log" --include=CLAUDE.md` → **0 files**. The skill's primary artifact has never landed. (Confirms #2.)
- CLAUDE.md files (root, anima, creative-studio, life-systems) carry **no YAML frontmatter**; `context:` lives on the vault note (`context: 16bitfit`, line 5 of `prj-16bitfit.md`). (Confirms #3.)
- `vault/20_projects/prj-code-brain/` is a **folder of sub-notes** (`prj-automode.md`, `prj-knowledge-loop-consumer.md`, `prj-agent-wiring-rollout.md`, …) with **no `prj-code-brain.md`**. (Confirms #4.)
- Real daily notes live at **`vault/10_timeline/daily/`** (e.g. `2026-06-10.md`), anchor `<!-- claude-sessions -->` present at line 161. **`vault/daily/` does not exist.**
- **flush.py resolves `vault_daily_dir = cfg.vault_root / "daily"` → `vault/daily/`** (config.toml `vault_root` line 3). It **appends a raw `## Sessions` block** via `format_daily_log_body` (line 172), **creates the file if missing** (lines 210–212), and **never touches `<!-- claude-sessions -->`**. So preserve-session and flush.py target **different directories** and **different sections** — a sharper form of #6/#7 than the finding states. (See #6 change note.)
- SessionEnd hook chain (`.claude/settings.json`): `session-end-flush.sh` then `session-end-auto-stub.sh`. Obsidian-Git is the **sole vault auto-commit owner** (root CLAUDE.md Rule #8).
- `mcp-obsidian` (with `patch_content`/`append_content`) is documented only as an **optional Claude-Desktop** setup (`obsidian-mcp-setup` skill); it is **not guaranteed mounted** in a Claude Code CLI session. → the write transport must floor on always-available built-ins.

---

## 1. Objective

**The problem.** `preserve-session` promises three structured writes but has no verified mechanism for any of them, aims two of them at targets that do not reliably resolve, and then reports success from the fact that its *steps ran* rather than from a re-read confirming bytes landed. The observable result: a session-end hand-off that says "saved" while losing state — proven by `## Session Log` existing in **zero** CLAUDE.md files. This matters because preserve-session is the WRITE half of the only zero-loss continuity path Sean has; when it lies about landing, resume-session silently reconstructs from missing or stale data, and the loss is invisible until a future session is already working from a wrong premise.

**Trade-off priority for unspecified cases.** Prefer a **visibly incomplete, honestly-reported** hand-off over a **silently lossy, confidently-"saved"** one. When any fix decision is ambiguous, choose the branch that (a) preserves the gathered item somewhere durable and (b) tells the truth about where it landed or why it didn't. Zero loss beats vault-tidiness; an honest SKIP beats a fabricated success. This line is the designed fallback when the spec doesn't enumerate a case (WWF5D §6.2).

---

## 2. Desired Outcome (owner-observable, before → after)

| | Before (today) | After (this fix) |
|---|---|---|
| **Confirmation** | Step 5 prints "CLAUDE.md updated / Vault note updated / Daily note appended" because the steps executed. A silent no-op and a real write print **identically**. | Every destination line reports one of exactly three states, each derived from a **read-back**: `WRITTEN & VERIFIED — <what, where>`, or `SKIPPED — <reason>`, or `FAILED — <reason + the exact payload, so nothing is lost>`. No fourth state; no unqualified "saved". |
| **CLAUDE.md** | `## Session Log` claimed, never lands (0 files). | The `## Session Log` entry is present in the file after the run, confirmed by re-reading the file and finding the new timestamped block. |
| **Vault note match** | Falls back to a `context:`-in-CLAUDE.md key that never exists; directory-name match has no target for `prj-code-brain`. | Match resolves against fields that actually exist; the code-brain "folder-not-note" case is handled explicitly; an unresolved match is a reported SKIP, never a guessed wrong sub-note. |
| **Two vault anchors** | One blanket "PATCH not PUT" rule stacks stale status under `<!-- status-update -->`. | `<!-- status-update -->` is **replaced**; `<!-- claude-sessions -->` is **appended**. resume-session surfaces *current* status, not last week's. |
| **Daily note** | Silent no-op on any day the Daily Driver hasn't created the note. | The note is located or created at the correct path; the session line lands in the anchor in the exact format the fleet console parses. |
| **Open Questions** | Gathered, shown as work-done, written nowhere; resume-session can't resurface it. | Written to a durable destination **and** resume-session is taught to read it back — the one class Sean flags for his own next decision survives the hand-off. |

---

## 3. The change, per finding

Notation: **DW** = dangerously-wrong, **S** = structural, **m** = minor (from the findings file). Each DW/S fix carries the reasoning a weaker implementing model needs to make the same call on an edge the spec didn't enumerate (WWF5D §6.2).

### 3.1 [DW] #1 — Confirm from a verified read-back, not from "the step ran"

**Change.** Replace Step 5 "Confirm" with a **read-back verification** per destination. After each write, **re-read the target region** and assert the just-written content is present; the Step-5 report line is *emitted from that assertion*, not from the fact that a write was attempted. Report vocabulary is fixed to three states only:

- `WRITTEN & VERIFIED — <destination>: <one-line what landed>` — the re-read found the new content.
- `SKIPPED — <destination>: <reason>` — the write was deliberately not performed (e.g. no vault note found; daily anchor absent and create declined). A skip is a *decision with a reason*, never silence.
- `FAILED — <destination>: <reason>. Unsaved payload: <the exact text that did not land>` — a write was attempted and the re-read did **not** confirm it. Dumping the payload is mandatory so the item is recoverable by hand.

**Reasoning to carry.** The root cause of the whole skill is *reporting from intent instead of from state* (WWF5D §5.4 — state lives on the artifact, not in promised behavior). The fix is not "add a retry loop" (an interactive human is present and can act on a FAILED line; a retry masks the signal). The fix is **make the report a function of a fresh read**. Edge rule the spec can't enumerate exhaustively: if you ever cannot re-read a destination to verify (permission, transport error), that destination is `FAILED` with its payload dumped — **never** `WRITTEN & VERIFIED`, and **never** silently downgraded to a bare `SKIPPED`. Verified means *you looked and saw it*; anything short of that is Failed-or-Skipped, and the difference is whether you *tried*.

### 3.2 [DW] #2 — Name the write transport, with a fallback ladder and an anti-skip rule

**Change.** Add a **Write Mechanism** subsection consumed by Steps 2–4. The transport is a fixed ladder, floored on always-available built-ins:

1. **`Edit`** (built-in) for modifying an existing file/region — anchor replacement, appending a Session Log entry to an existing CLAUDE.md, replacing `<!-- status-update -->` content, inserting into `<!-- claude-sessions -->`. **`Write`** (built-in) only when creating a file that does not yet exist (a missing daily note; a scaffolded vault note if that fork is taken — see §6).
2. **Optional upgrade:** if the `mcp-obsidian` MCP is **mounted in this session** and exposes `patch_content` / `append_content`, its anchor-aware write MAY substitute for the vault-note writes — but the §3.1 read-back still runs afterward regardless of which transport wrote. mcp-obsidian is **not** assumed present (it is an optional Claude-Desktop setup, not part of this repo); when absent, the built-in `Edit`/`Write` path is the mechanism, not a stall.

**Anti-skip rule (the load-bearing half).** The common improvisation — *"the anchor already looks current, so I'll skip the write"* — is **forbidden**. preserve-session's whole job is to capture *this* session; "looks current" is never grounds to skip, because the current-looking content is from a *prior* session. Perform the write, then verify. The only legitimate non-write is a `SKIPPED — <reason>` where the reason is a real blocker (no target resolves), not "it looked done."

**Reasoning to carry.** WWF5D §2.4 / §5.4: an unnamed mechanism is a false sense of safety worse than an admitted gap — the executor improvises, and the cheapest improvisation is the silent no-op that produced the zero-landed-files evidence. Naming `Edit`/`Write` as the floor guarantees the mechanism exists in every Claude Code session. Edge rule: if a write genuinely cannot be performed by any available transport, that is `FAILED` with payload dump (§3.1), not an invented success. Never retry a transport in a loop — one attempt, then verify, then report.

### 3.3 [DW] #3 — Fix the vault-note match keys to fields that exist

**Change.** Rewrite Step 3's match logic. The current match key #2 — "the `context` field in CLAUDE.md frontmatter" — is **deleted**: verified, CLAUDE.md files carry no frontmatter, so this key can never fire. Replace the match procedure with, in order:

1. **Directory-name → note-name convention**, but handled per §3.4 (the folder-vs-note case is real).
2. **`context:` field on the *vault note*** (not CLAUDE.md): scan `vault/20_projects/**/*.md` frontmatter for a `context:` value matching the working directory's basename (e.g. working in `16bitfit/` → note with `context: 16bitfit`). This is where `context:` actually lives.
3. If neither resolves to a single note → **SKIP with reason** (§3.5), never a guess.

**Reasoning to carry.** WWF5D §2.4 (existence-check every claim about the world): the skill asserted a field location without checking it. The correcting principle is *match on fields that are observed to exist in the store you're reading*. Edge rule: if step 1 and step 2 resolve to **different** notes, prefer the explicit `context:` match (step 2) — a frontmatter field authored by a human is a stronger signal of intent than a directory-name coincidence.

### 3.4 [DW] #4 — Define the target for the folder-that-is-not-a-note case (the code-brain common case)

**Change.** Add explicit handling for the case where the directory-name match points at a **folder of sub-notes with no single top-level note** — verified true for `vault/20_projects/prj-code-brain/`, which is the most common session-end repo. When the derived note path (`vault/20_projects/prj-<name>/prj-<name>.md`) **does not exist as a file**:

1. Try the `context:`-on-vault-note match (§3.3 step 2) first — it may resolve to a real sub-note the human tagged.
2. If that also fails to resolve to a single note → **do not** write the structured block into an arbitrary sub-note. Instead, **redirect the vault block into the project CLAUDE.md** as a fallback destination (append it under the `## Session Log` entry as a `**Vault note:** not resolved — captured here instead` sub-block), and report `SKIPPED — vault note: no single note for <dir>; block preserved in CLAUDE.md`.

**Reasoning to carry.** WWF5D §2.3 (trace to point-of-effect) + the Objective's zero-loss priority: the failure here is *silent loss or wrong-destination write*. Guessing a sub-note pollutes an unrelated note and is unrecoverable; the CLAUDE.md redirect preserves the content in a destination that *definitely* exists and that resume-session *definitely* reads, at the cost of it not being in the vault. Zero-loss beats vault-placement (Objective trade-off line). Edge rule: never invent a `prj-code-brain.md` — creating the canonical note for a multi-note folder is a vault-structure decision that is not preserve-session's to make.

### 3.5 [S] #5 — Split the two vault anchors' write disciplines, with a distinguishing test

**Change.** Replace the single "PATCH not PUT" instruction with **two rules keyed to the anchor's semantics**:

- `<!-- status-update -->` holds **current state** → **REPLACE** the anchor's body each session. (resume-session reads it for "where you left off"; appending stacks stale status and resume surfaces last week as current.)
- `<!-- claude-sessions -->` (and the CLAUDE.md `## Session Log`) is a **log** → **APPEND** a new timestamped entry, never replace. (Replacing wipes the day's earlier lines = data loss.)

Add a one-line **discipline test** the implementer can run: *does resume-session read this region as "the current state" or as "a history"? Current-state → replace; history → append.*

**Reasoning to carry.** WWF5D §2.5 (degraded/asymmetric paths) + §6.9 (hold the objective): one blanket rule is *half-wrong by construction* — correct for the append region, data-losing for the replace region, and the reverse mislabeling (append-to-status) is the subtler bug because it doesn't lose data, it *poisons freshness*. The generalizable rule is **write-discipline follows read-semantics**: match the reader's expectation of the region, not a global preference. This is the discriminating rule for any *future* anchor the skill learns to write.

### 3.6 [S] #6 — Mark `<!-- claude-sessions -->` a shared, format-load-bearing surface; pin the line shape; state the flush relationship; fix the path

**Change (three coupled parts):**

**(a) Pin the exact line format** the fleet console parses. The daily session line MUST be emitted as the inline-field Dataview shape:
```
- [time:: HH:MM] | [domain:: <domain>] | [context:: <project>] | **Outcomes:** <1-sentence summary>. Link: [[prj-<project>]]
```
Every field is required. If a field's value is unknown at write time, emit a **placeholder, never omit the field** — `[domain:: unknown]`, `[context:: unknown]`, `Link: [[prj-unknown]]`. A dropped field (not just a wrong value) makes the whole session **invisible** to the Dataview roll-up on the daily-note fleet console.

**(b) Fix the path.** The correct daily-note directory is **`vault/10_timeline/daily/YYYY-MM-DD.md`** (verified; this is also what resume-session Step 1 reads). The skill's current text is already correct on this; the fix is to keep it pinned and add the note below.

**(c) State the flush relationship explicitly** (this also resolves finding #10 and Fork 2). Add a note: *"`session-end-flush.sh` → `flush.py` is a separate SessionEnd hook that mines the transcript into `vault/knowledge/` and appends a raw `## Sessions` block to `vault/daily/YYYY-MM-DD.md` (a different directory and a different section from this skill's `<!-- claude-sessions -->` anchor in `vault/10_timeline/daily/`). The two do not collide and must not be merged: flush is unattended knowledge-extraction; preserve-session is the interactive, structured, human-triggered hand-off for resume-session. preserve-session does not write to `vault/knowledge/` and does not touch the `## Sessions` block. Do not add a second vault auto-commit step — Obsidian-Git is the sole auto-commit owner (root CLAUDE.md Rule #8)."*

**Reasoning to carry.** WWF5D §2.3 (arrives-but-unreadable) + §5.1 (name WHO and the exact SHAPE): the anchor is a **cross-owner contract**, not private free-text. `daily_driver.py` parses this exact line for a Dataview roll-up; drift makes a session vanish from the console silently. **This is a paired-change awareness:** the line shape is *consumed by* the fleet console — if a future edit changes the fields, it must change the console's parser too, or file a ticket (WWF5D §2.7). Edge rule: when in doubt about a field value, a visible `unknown` placeholder is always safe; an omitted field is never safe.

### 3.7 [S] #8 — Route "Open Questions" to a durable home AND teach resume-session to read it (paired change)

**Change (two files — this is the point-of-effect pairing).**

**In preserve-session:** add an **Open Questions** field to the `## Session Log` template (Step 2), so all five gathered categories (Step 1) have a destination:
```
**Open Questions (for next session's decision):**
- <question 1>
- <question 2>
```
Also insert the same list into the vault note under `<!-- status-update -->` if a note resolved (it is current-state: these are open *now*).

**In resume-session (`.claude/skills/resume-session/SKILL.md`) — the paired change:** add `Open Questions` to the Step-1 extract list (currently line 26 extracts "decisions, blockers, next steps, files modified" with **no line for open questions**) and add a **`### Open Questions`** section to the Step-2 briefing template, so the reader surfaces them.

**Reasoning to carry.** WWF5D §2.3 corollary (the RT1 lesson, verbatim): *a value written to a surface its consumer doesn't read is inert; if surfacing it requires editing the reader too, that is a paired change — make it, never protect the reader into inertness.* Writing Open Questions to CLAUDE.md while resume-session's extract list ignores them would *look* fixed and change nothing. The Objective (zero loss) is only satisfied when the item is written **and** read. Edge rule: Open Questions are the one class the grounding says Sean flags for *his own next-session decision* — if forced to pick a single durable home, CLAUDE.md `## Session Log` wins (it always exists and resume-session always reads it), with the vault-note copy as a bonus when a note resolves.

> **Self-application note (WWF5D §6.7 / intent-engineering §6.5):** resume-session is named in "What NOT to Change" as *read-only* (§5). This fix edits it — the edit is **additive read behavior only** (a new extract line + a new briefing section), which does not violate read-only-ness (it reads *more*, writes nothing). The pairing is called out here so the implementer makes both edits in one change and does not treat the resume-session edit as scope creep.

### 3.8 [S] #7 — Locate-or-create the daily note (no silent no-op)

**Change.** Replace Step 4's guard "if today's daily note exists" with **locate-or-create**:
1. Look for `vault/10_timeline/daily/YYYY-MM-DD.md`.
2. If absent, **create it from the template** at `vault/90_system/templates/tpl-daily.md` (which carries the `<!-- claude-sessions -->` anchor), then write the session line into the anchor.
3. Only if creation itself fails → `SKIPPED — daily note: could not locate or create; session line preserved in CLAUDE.md Session Log`.

**Reasoning to carry.** WWF5D §2.5 (fail-open intake): "if X exists, write X" silently drops every evening/weekend/out-of-band session — precisely the sessions a hand-off matters most for, because no morning Daily Driver ran to create the note. The distinguishing question — *legitimately-absent vs not-yet-created* — resolves to "always create," because the anchor's absence here is never intentional. Edge rule: create from the template (so the anchor and the Dataview blocks exist for the fleet console), not as a bare file — a bare file with no anchor re-creates finding #9 one level down. Do **not** add a git commit after creating (Rule #8 — Obsidian-Git owns that).

### 3.9 [S] #9 — Define the missing/renamed-anchor adapter

**Change.** Add a rule for every anchor write (`<!-- status-update -->`, `<!-- claude-sessions -->`): **if the anchor is absent** from the target file (a hand-edited note, a note predating the template):
1. **Append** a new section with the anchor and the content, at the end of the file (e.g. `\n## Current Status\n<!-- status-update -->\n<content>` or `\n## Claude Code Sessions\n<!-- claude-sessions -->\n<content>`). Appending a missing anchor is safe; guessing an insertion point in unfamiliar structure is not.
2. Report `WRITTEN & VERIFIED — <dest>: anchor was absent, appended new section` (verified by re-read per §3.1) — the "anchor absent" fact is surfaced, not hidden.

**Reasoning to carry.** WWF5D §2.5 + §3.1: the current skill writes "nowhere or in the wrong place" and still reports success. The fix makes anchor-absence a **visible, self-healing** event (append + note it), never a silent land-nowhere. Edge rule: for a `status-update` (replace-discipline) anchor that is absent, appending a fresh section is correct — there is no prior state to replace. Never fabricate the whole template structure around a missing anchor; append the one section you need.

### 3.10 [m] #11 — Timestamp gets a timezone/source

**Change.** Step 2's timestamp is emitted as **local time with an explicit offset or tz abbreviation** (e.g. `2026-07-05 14:30 ET`). Source is the machine clock. Brief: resume-session mis-orders across a tz boundary without it.

### 3.11 [m] #12 — `ai-context` is summarized, not truncated

**Change.** The "keep ai-context under 200 characters" rule gains: **summarize to fit, never hard-cut.** If the natural summary exceeds 200 chars, compress the *meaning* to fit; do not slice mid-sentence. Brief: real values run ~380 chars; a mid-sentence cut is worse than a shorter true summary.

### 3.12 [m] #13 — `## Session Log` gets a cap that ARCHIVES, never deletes

**Change.** Add a rotation rule: when `## Session Log` exceeds **N = 10** entries, move the **oldest** entries to a `## Session Log (archive)` section at the bottom of the same file (or a sibling `CLAUDE-session-log-archive.md`), keeping the 10 most recent under `## Session Log`. **Archive, never delete.**

**Reasoning to carry (WWF5D §6.9 — hold the objective as an invariant).** A cap that *drops* the oldest entry is **data loss inside a zero-loss spec** — locally reasonable (keep the file small), globally a betrayal of the Objective. The objective wins: rotation must relocate, never delete. This is the one minor finding that carries reasoning, because the obvious implementation (drop oldest) directly contradicts the spec's purpose.

---

## 4. Owner-forks — surfaced with a recommendation + contingency (not silently decided)

Per WWF5D §6.8 / intent-engineering: pre-make what the record decides; **surface** genuine owner-taste calls with a recommendation and its contingency — never a bare menu, never a silent pick. Both named forks are genuine taste calls (the record does not decide them), so both are surfaced.

### Fork A — Missing vault note: report-and-skip vs auto-scaffold vs CLAUDE.md-redirect

**What the record says.** Current skill (line 88): *"report it but don't create one automatically."* That is the standing decision, but it predates the zero-loss framing and the code-brain folder-not-note evidence.

**New tradeoff info the diagnosis surfaced.** Option (iii) — **redirect the structured block into CLAUDE.md** — was not in the original skill. It preserves **zero loss** (the item lands in a destination that always exists and that resume-session always reads) **without** touching the vault at all, so it sidesteps the vault-cleanliness objection to option (ii). Note on Rule #8: auto-scaffolding a note (option ii) would *not itself* violate the "no second auto-commit" rule — Obsidian-Git still does the commit — but it does add un-asked-for files to the vault, which is the cleanliness cost.

**Recommendation:** **(iii) CLAUDE.md-redirect** as the default when no vault note resolves, combined with **(i) report** — i.e. `SKIPPED — vault note: none resolved for <dir>; block preserved in CLAUDE.md Session Log`. This is what §3.4 and §3.8 already implement, because it is the only option that satisfies the Objective's zero-loss priority for the *most common* case (code-brain) without a vault-structure guess.

**Contingency (if Sean prefers vault-cleanliness over CLAUDE.md redirect):** fall back to **(i) pure report-and-skip** — emit `SKIPPED — vault note: none resolved; not captured to vault (Open Questions/next-steps still in CLAUDE.md)`. Do **not** adopt (ii) auto-scaffold unless Sean explicitly asks, because a scaffolded stub for every unmatched directory clutters `vault/20_projects/` and creates notes no human authored. The recommendation is a decision Sean can flip in one line; it is surfaced, not buried.

### Fork B — Flush-hook coexistence: stay two structures vs reconcile into one

**What the record says.** flush is a SessionEnd hook (knowledge-loop producer; root CLAUDE.md line 160) that mines the transcript into `vault/knowledge/` and appends a raw `## Sessions` block to `vault/daily/`. The record does **not** decide "reconcile"; Rule #8 forbids a second auto-commit mechanism.

**Recommendation:** **stay two separate structures.** They serve different purposes on different surfaces: flush = unattended, transcript-mined, knowledge/narrative, targeting `vault/knowledge/` + `vault/daily/## Sessions`; preserve-session = interactive, human-curated, structured hand-off, targeting `<!-- claude-sessions -->` in `vault/10_timeline/daily/` + CLAUDE.md + the vault note. §3.6(c) writes this coexistence into the skill. Reconciling into one writer would either make preserve-session unattended (it is not — `enabled = false`) or make flush structured (it can't curate decisions/blockers from a transcript as well as the interactive session can). Keeping them separate is the lower-risk, record-consistent choice.

**Contingency (if Sean later wants one console line per session, not two records):** the reconciliation is a *separate* piece of work — it must (a) pick one writer as the owner of the `<!-- claude-sessions -->` line, (b) route the other's output through it, and (c) **not** introduce a second auto-commit step (Rule #8). That is out of scope for this fix and would be its own spec; flag it as a deferral, do not attempt it here.

---

## 5. What NOT to change (Preservation Constraints — the thing + WHY)

Per intent-engineering Section 6 (mandatory on a fix spec) and WWF5D §3.5 (confirmed-correct rows protect working design from the fix):

- **resume-session stays read-only** — *why:* it is the READ half; it must never write to the sources it reads or it corrupts the state it reports. The §3.7 edit is **additive read behavior only** (new extract line + new briefing section); it reads more, writes nothing. Do not add any write to resume-session.
- **"Report it but don't create one automatically" is the *default* for a missing vault note** (Fork A) — *why:* auto-creating vault notes is a vault-structure decision that belongs to Sean, not the skill. The recommended CLAUDE.md-redirect preserves zero loss *without* auto-creating a note, so the "don't auto-create" instinct is honored, not overridden.
- **`## Session Log` and `<!-- claude-sessions -->` stay APPEND-discipline** — *why:* they are logs; replacing them is data loss (#5). This is the half of "PATCH not PUT" that was **right** — preserve it. Do **not** over-generalize the append rule to `<!-- status-update -->`, which is *supposed* to be replaced (that over-generalization is finding #5 itself).
- **The `<!-- anchor -->` PATCH pattern itself** — *why:* anchored, region-scoped writes (vs whole-file PUT) are correct and are what let multiple writers share a file. The fix refines *which discipline per anchor*, not the anchor mechanism.
- **The 200-char `ai-context` cap and the one-line daily Outcome** — *why:* these are consumer-shape contracts (resume-session reads `ai-context`; the Dataview roll-up expects a one-line Outcome). The fix changes truncate→summarize (#12) but keeps the length targets — do not lengthen them.
- **The five-item Step-1 gather list** (decisions, blockers, files modified, next steps, open questions) — *why:* it is the correct capture set; the bug was that Open Questions had no *destination* (#8), not that it was gathered. Keep all five; the fix adds the missing destination + reader.
- **No Zero-Interaction Mandate** — *why:* preserve-session is interactive (`[agents.preserve_session] enabled = false`, no schedule). The mandate's trigger is "runs unattended," not "is a skill." Injecting it here would be wrong — it would tell an interactive skill that has a human present to never ask, which is the opposite of correct.
- **flush.py, `session-end-flush.sh`, and the `## Sessions` block are not touched** — *why:* they are a separate, working, unattended knowledge-extraction path (Fork B). preserve-session states the relationship (§3.6c) but writes none of flush's surfaces. Reconciliation is a deferral, not this fix.

---

## 6. Done looks like (checkable statements)

Each is a grep, a test, or an exact behavior an implementer can run (WWF5D §6.6):

1. **Transport named:** `grep -n "Edit\|Write" .claude/skills/preserve-session/SKILL.md` shows the built-in write mechanism named in a Write Mechanism subsection; `grep -n "already.*current\|looks current" SKILL.md` shows the **anti-skip rule** forbidding "skip because it looks current."
2. **Confirmation is read-back-gated:** the skill's Step 5 text emits only `WRITTEN & VERIFIED` / `SKIPPED — <reason>` / `FAILED — <reason> + payload`; `grep -n "updated\b" SKILL.md` finds no unqualified "updated/saved" success line that isn't downstream of a re-read.
3. **Dead match key gone:** `grep -n "context.*field in CLAUDE.md\|CLAUDE.md frontmatter" SKILL.md` returns **nothing** (the never-firing key #2 is deleted); the `context:`-on-vault-note match is present instead.
4. **Folder-not-note handled:** the skill names the `prj-code-brain`-style "folder of sub-notes, no single note" case and its CLAUDE.md-redirect fallback; it never instructs creating `prj-<name>.md` for such a folder.
5. **Two anchor disciplines split:** the skill states `<!-- status-update -->` = REPLACE and `<!-- claude-sessions -->` = APPEND, with the current-state-vs-history test. A reviewer can confirm the two anchors carry *different* verbs.
6. **Daily line shape pinned:** the exact `- [time:: …] | [domain:: …] | [context:: …] | **Outcomes:** … Link: [[prj-…]]` format is in the skill, with the "placeholder-not-omit" rule for unknown fields; the daily path reads `vault/10_timeline/daily/`.
7. **Flush relationship stated:** `grep -n "flush\|## Sessions\|Obsidian-Git\|Rule #8\|sole" SKILL.md` shows the coexistence note (different dir, different section, do-not-merge, no second auto-commit).
8. **Open Questions has a destination AND a reader:** `grep -n "Open Questions" .claude/skills/preserve-session/SKILL.md` shows it in the Session Log template; `grep -n "Open Questions" .claude/skills/resume-session/SKILL.md` shows it in **both** resume-session's Step-1 extract list and Step-2 briefing template. (Both greps non-empty = the paired change landed; either empty = inert.)
9. **Locate-or-create daily:** the skill creates the daily note from `tpl-daily.md` when absent, and only SKIPs if creation fails; `grep -n "if today's daily note exists" SKILL.md` returns nothing (the fail-open guard is gone).
10. **Missing-anchor adapter defined:** the skill states the append-new-section behavior for an absent anchor and reports it, rather than landing nowhere.
11. **Cap archives, never deletes:** `grep -n "Session Log" SKILL.md` shows a rotation rule that **relocates** entries beyond N=10 to an archive section; `grep -n "delete\|drop.*oldest\|remove.*oldest" SKILL.md` shows no delete-oldest rule.
12. **Timestamp carries tz; ai-context summarizes:** the skill's timestamp format includes an offset/tz; the ai-context rule says summarize-to-fit not hard-cut.
13. **Live acceptance test (the outcome that matters):** run preserve-session at the end of a real code-brain session; then `grep -c "^### " <that CLAUDE.md's ## Session Log>` shows the new entry present (the zero-landed-files symptom is gone), and Step 5's report shows a `SKIPPED — vault note` line naming the folder-not-note reason (not a false "Vault note updated").

---

## 7. Band-aid tripwires (reject these in review)

- **"Report from a flag we set after writing"** instead of a fresh read-back — this is the original bug reworded. The report MUST derive from re-reading the destination, not from an in-memory "did_write=true".
- **A retry loop** on a failed write — an interactive human is present; a `FAILED — <payload>` line they can act on beats a silent retry that masks the failure. Reject added retry logic.
- **"Skip the write if the anchor looks current"** in any form — the anti-skip rule (§3.2) is explicit; a reviewer should reject any hedge that lets current-looking prior-session content justify not writing.
- **Writing Open Questions to CLAUDE.md but not editing resume-session** — inert by construction (§3.7). Both files change or neither claim is fixed.
- **A `## Session Log` cap that deletes** the oldest entry — data loss in a zero-loss spec (§3.12). Must archive.
- **Auto-scaffolding a vault note by default** for every unmatched directory (§Fork A) — clutters the vault with un-authored stubs; only on Sean's explicit ask.
- **Adding any git commit / auto-commit step** anywhere in the skill — Rule #8: Obsidian-Git is the sole vault auto-commit owner.

---

## 8. Deferrals (explicitly NOT in this fix; what gates them)

- **Reconciling preserve-session and flush into one `<!-- claude-sessions -->` writer** (Fork B) — gated on Sean choosing "one record per session, not two." It is its own spec: pick the line-owner, route the other through it, keep Rule #8. Not attempted here.
- **Fixing flush.py's `vault/daily/` vs `vault/10_timeline/daily/` path discrepancy** — surfaced during grounding (flush writes to a directory that doesn't exist), but flush.py is out of this skill's scope. Flagged for a follow-up ticket; not fixed in this SKILL.md.
- **Auto-creating a canonical `prj-code-brain.md`** for the code-brain multi-note folder — a vault-structure decision for Sean, not a skill behavior. The fix redirects to CLAUDE.md instead; a real canonical note is Sean's call.

---

## VALIDATION VERDICT — Profile: 4-element floor (Objective + Outcome in scope) — hand-run (intent-engineering MCP tools not confirmed mounted this session)

- **Objective Quality:** pass — states the problem (writes with no verified mechanism to targets that don't resolve, reported from intent), why it matters (zero-loss continuity path lies about landing → resume rebuilds from missing/stale data), and a trade-off line that guides unspecified cases (visibly-incomplete-honest > silently-lossy-confident).
- **Outcome Quality:** pass — outcomes are observable states from the owner's chair (per-destination WRITTEN/SKIPPED/FAILED report derived from read-back; `## Session Log` present after run; current-not-stale status; Open Questions survive), measurable without agent self-report (greps + a live acceptance test), and there are 3–6 of them, not 1, not 10.
- **Out of scope (floor):** Health Metric, Constraint (beyond Preservation), Autonomy, Edge-Case group as a standalone section — governed here by the consumer's contract (resume-session's read shape, the Dataview parser) rather than this checklist; recorded as out of scope, not as failures.
- **Preservation Constraints:** present and reasoned (§5) — mandatory on a fix spec, satisfied.
- **Paired-change protocol:** applied — §3.6 (daily line ↔ fleet-console parser) and §3.7 (Open Questions ↔ resume-session reader) both carry the "edit both or file a ticket" rule; the self-application note flags the resume-session edit as additive-read, in-scope.
- **Owner-forks:** both surfaced with recommendation + contingency (§4), neither silently decided nor left a bare menu.
- **Handoff rehearsal (WWF5D §1.5 / intent-engineering pre-emit):** fresh un-enumerated case — *"preserve-session runs in a brand-new project directory with no CLAUDE.md and no vault note at all."* Would the Objective + trade-off line force the right call for a weaker model? **Yes:** zero-loss-over-tidiness → create the CLAUDE.md `## Session Log` (the always-available destination) via `Write`, capture everything including Open Questions there, report `SKIPPED — vault note: none for a new project` and `WRITTEN & VERIFIED — CLAUDE.md: created Session Log`. No silent loss, no fabricated success, no vault-structure guess. The Objective carried the case the spec didn't enumerate — no edge-case-list patch needed.
