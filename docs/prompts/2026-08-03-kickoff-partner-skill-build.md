# Continuation — build the generalized creative-partner session skill

*Kickoff prompt for a fresh Fable 5 session. Paste the body below.*

---

Build session — the creative harness's **first Phase-3 build**. Author the
generalized creative-partner session skill (T27c's Option C): the anima
front-door spine — session sidecar, one question at a time, a recommendation
with every question, a verbatim reason at every lock — generalized into a
standalone, domain-agnostic skill, with the anima emit stripped. **The sidecar
IS the deliverable.** Every design gate this build waited on is closed: T28
ratified 2026-08-02 (the f5 gate is open), and the front-door reason-capture
pattern passed its live test 2026-08-03 on a real full-length session.

## 1. Ground rules (standing, from the map — non-negotiable)

- **No web research in this session.** T27b already did the research, and the
  web lane and local lane never share a session. Everything you need is on
  disk.
- The private wayfinder lane
  (`vault/knowledge/private/creative-harness/wayfinder/`) is **gitignored and
  local-only**: never commit or push anything in it, and never copy its prose
  into tracked files. The skill you author is a **public** artifact — write it
  public-safe from the first line (generic rules public; any private samples
  go only to a gitignored `references/` dir, CLAUDE.md rule 9 pattern).
- One ticket per session. This is the partner-skill build ticket only.
- **How to grill Sean (map Notes, Sean-directed):** he's a PM, not a
  developer. Define every piece of jargon, file format, and tool name the
  first time it appears, then give the recommendation. He decides intent; you
  make the trade-off legible first.
- **Capture Sean's reasons verbatim at every decision** — he ratified this as
  standing after the live test: "It's really made me think deeper about WHY I
  want those choices… Definitely want that moving forward." If he volunteers
  the reason with the decision, record it verbatim without re-asking.

## 2. Read first, in this order

1. `vault/00_inbox/tickets.md` — the bullet **"Build the generalized
   creative-partner session skill"** (T27c provenance). Its build-spec
   requirements and the 2026-08-02 gate/scope notes are the contract.
2. Private lane, in order:
   `vault/knowledge/private/creative-harness/wayfinder/TRACKER.md` →
   `map.md` (Notes block fully — standing rules, north star, privacy gate —
   then the T27a / T27c / T28 entries under Decisions so far) →
   `tickets/T27c-skill-consolidation-and-model-routing.md` →
   `tickets/T27a-partner-evidence-unit.md` →
   `tickets/T28-partner-taxonomy-amendment.md` (schema v2; note the two items
   routed INTO this build's spec: the harvest-registry record layout and the
   block-to-move splitting procedure).
3. The spine to generalize:
   `anima/.claude/skills/brainstorm-front-door/SKILL.md` +
   `references/session-sidecar-contract.md`.
4. The live-test evidence:
   [docs/plans/2026-08-03-anima-frontdoor-reason-capture-livetest-findings.md](../plans/2026-08-03-anima-frontdoor-reason-capture-livetest-findings.md)
   + the specimen sidecar
   `anima/briefs/2026-08-02-about-me-short/frontdoor-session.md` (18 locks —
   what the pattern looks like under real load).
5. Divergence-stage sources: the adhd-repo teardown in the wayfinder
   `assets/` dir (T27b's findings doc) + the archived technique catalogs at
   `vault/60_archive/sw-creative-toolkit-bmad/` (quarry for Sean-domain
   frames — Sean: "an archive folder is perfect for them").

## 3. Already decided — do not re-litigate

- **Option C:** ONE harness-owned partner skill; front-door spine
  generalized; anima emit stripped; the sidecar is the deliverable.
  Domain-agnostic by design (Sean: "It's meant to help me think differently
  and creatively and make me better for various topics and tasks").
- **The divergence stage is the adapted adhd-style loop** (isolated parallel
  takes wearing ordinary-persona frames; mechanical generator/critic split;
  traps flagged with reasons; frame selection logged) — an explicit mode,
  **default OFF**, invoked by Sean or a stated threshold, with a call/token
  budget and a recorded mode tag.
- **Producer/consumer identity contract:** the skill and any compiled
  preference pack get distinct stable names, a defined invocation/precedence
  contract, and both artifact hashes stamped into session sidecars and
  install manifests.
- **A long-session honesty-rule reassertion mechanism** is required (in-context
  instructions drift over long sessions) — inherited from the harness or a
  bounded-session rule of the skill's own.
- **The volunteered-reason rule ships from day one** (live-test finding 1b): a
  reason volunteered with the decision satisfies the ask — record it verbatim,
  don't re-ask. (The parallel anima two-file amendment is a separate ticket
  and a separate Sean approval — do not touch anima in this session.)
- Machines write `candidate` only; no auto-memory anywhere (threat T8); the
  four standalone code-brain creative skills stay untouched.

## 4. The open choices — grill these, one at a time, recommendation first

1. **The skill's name** (and the pack's distinct name) — stable identifiers
   the identity contract hangs on.
2. **The Sean-domain frame set** for the divergence stage — authored from the
   archived catalogs, not the adhd repo's stock engineering-biased 15. How
   many, which domains (writing, anima/art direction, product/work execution,
   frontend…), and what a frame card must contain.
3. **The divergence trigger + budget** — what threshold invokes it, what the
   call/token cap is, how the mode tag is recorded.
4. **The honesty-reassertion mechanism** — which form (periodic sidecar
   re-read? lock-count checkpoint? bounded session length?), and where it
   lives.
5. **Sidecar conventions outside anima** — file name/location per session,
   and the lock/proposals shape carried over (keep the two-block discipline
   and `(verbatim)` marking).
6. **The harvest-registry record layout** (paths, defaults, cursors,
   loud-error duplicate rules) and **the block-to-move splitting procedure**
   — T28 routed both here so they can evolve with the sidecar format. Spec
   them as prose; placement respects the privacy gate (likely a private-lane
   asset, with the skill referencing the contract by name only).
7. **Where the skill's references live** — what's public SKILL.md prose vs.
   gitignored `references/` (privacy layer rule 9).

## 5. Skills to invoke

- `superpowers:writing-skills` — before authoring the SKILL.md (this is a
  skill-authoring session; use the discipline).
- `grilling` — for §4's open choices.
- `prompt-engineering` — the SKILL.md is a prompt; apply it when drafting.
- Standing memory rule: explain jargon before decisions.

## 6. Deliverables + wrap

- The skill directory under `.claude/skills/<name>/` (public-safe), honoring
  every §3 requirement.
- The registry/splitting spec (§4 item 6) written down where the privacy gate
  says it belongs.
- Per CLAUDE.md: CHANGELOG.md entry + count-table updates + `python3
  scripts/validate.py` clean.
- Update the partner-skill ticket bullet in `vault/00_inbox/tickets.md` with
  the outcome; capture any Sean call-outs as new Todo bullets (privacy gate:
  public artifacts by name, private lane as provenance only). Commit public
  files only.
- **Follow-up, not this session:** a Codex/Sol adversarial review of the
  drafted SKILL.md (same pattern as the map and T19/T22/T23 reviews) — Sean
  launches it separately.

## Context worth knowing

The live test proved the core loop on a real spark: 17/17 locks captured
verbatim with zero cadence complaints, and the why-question generated story
(the [L4] answer flipped the protagonist design). Three paths remain untested
in the wild — skip, the one-guess-on-category-answer, SUPERSEDES — so the
generalized skill inherits them as written and future sessions watch for
their first live firing.
