# Block → Job-Hunt Migration Plan

> **Goal:** Stop every workflow that depends on Block access (calendar, Slack, Jira, Confluence, the-block heartbeat) before it starts erroring or producing stale guidance. Repurpose what's reusable. Archive (don't delete) what's Block-specific. Stand up the job-hunt rhythm in its place.
>
> **Owner:** Sean. Estimated work: ~3 hours total split across the next 5 days.
>
> **🟢 STATUS (updated 2026-05-04 evening):** Chunks 1-4 **DONE** in a single session — 13 commits on `feat/gemini-deep-research-v3.25.0`. The audit plan extended this migration with operating-model setup + DOMAINS tuple updates + active-bundle sanitization; all of that landed too. Chunk 5 (MCP cleanup) **deferred** to ~5/11 per the original calendar. See [[2026-05-04-migration-completion-handoff|2026-05-04-migration-completion-handoff.md]] for full details and the resume-here pointer.

---

## What's Block-wired in your system right now

### A. Will FAIL when Block access is revoked (urgent — fix this week)

| Surface | What breaks | Where it lives |
|---|---|---|
| `daily-driver` skill | "Query BOTH calendars" instruction → `swinslow@theblock.co` returns auth error | `.claude/skills/daily-driver/SKILL.md:95` |
| Atlassian MCP server | All Jira/Confluence calls return auth errors | MCP config (used interactively, not by SDK agents) |
| Slack MCP (when it lands) | All Block-workspace channels, DMs return auth errors | MCP config |
| Granola meetings (Block) | Future Block transcripts won't sync (you're off the calendar) | already handled — naturally ends |
| `daily-note-appender.sh` hook | Pulls calendar + Slack signals from Block sources for nightly log | `.claude/hooks/daily-note-appender.sh` |

### B. Will keep running but produce STALE/WRONG output (urgent — fix this week)

| Surface | What's stale | Where it lives |
|---|---|---|
| `daily_driver` SDK agent (8:45 AM) | Morning brief includes Block calendar pointer + the-block HEARTBEAT preamble | `agents-sdk/agents/daily_driver.py` + `vault/05_atlas/operating-models/the-block/HEARTBEAT.md` |
| `meta_agent` SDK agent (6:30 AM) | "Domain-Aware Insights" cross-references the-block schedule-recommendations | `vault/05_atlas/operating-models/the-block/schedule-recommendations.md` |
| `flush.py` (SessionEnd/PreCompact) | Prepends 3-domain SOUL including the-block | `vault/05_atlas/operating-models/the-block/SOUL.md` |
| `knowledge_lint.py` (Sun 22:00) | Tier 2 includes the-block SOUL for `soul-tier-a-conflict` issue kind | same SOUL file |
| `time-management` skill | Calibrated to Block 4:45 AM routine + 45/35/20 work split | `.claude/skills/time-management/SKILL.md` |
| `meeting-prep` skill | Hard-coded list of Sean's recurring Block meetings | `.claude/skills/meeting-prep/SKILL.md` |

### C. Block-themed skills (audit + sanitize in place — NOT archive)

> **Decision (2026-05-04):** Don't archive these. Most were written as general PM patterns with Block specifics layered in. The plan is to **strip the Block-specific lines and keep the underlying patterns** — they're useful for future roles and portfolio pieces. This audit also feeds the broader Karpathy "consolidate to 60–80 skills + identify MCP candidates" sweep.

| Skill | What's Block-specific | Sanitization approach |
|---|---|---|
| `analytics-workarounds` | GA4/Looker access patterns specific to Block | Generalize to "PM-without-direct-analytics-tool patterns"; keep the Zapier-as-bridge framing |
| `api-product-management` | Block Data API examples | Replace examples with generic data-API examples; the OpenAPI/SDK/dev-portal frameworks are universal |
| `campus-education` | Block Campus crypto curriculum | Generalize to "education platform / LMS PM patterns"; the course/quiz/cert structure is reusable |
| `etf-page-creator` | WordPress ETF pages on theblock.co | Generalize to "structured-content publisher" pattern (Karpathy synthesis flagged this as a strong MCP candidate too) |
| `jira-automation` | Block's specific Jira projects, components, labels | Generalize to "Jira automation patterns" + drop Block project keys |
| `meeting-prep` | Hardcoded list of Sean's Block standups | Strip Sean's Block recurring meetings; keep the prep-template patterns |
| `revops-adops-automation` | Block media revenue ops examples | Generalize to "RevOps/AdOps PM patterns for media+data companies" |
| `sprint-health` | Block Jira PRO/RBS/CM/GD project filter | Make project key configurable (was already configurable in agents-sdk config); strip Block-specific component IDs |
| `stakeholder-update` | Block bi-weekly P&E status template | Generalize template; the "Done / In-flight / Upcoming + risks" pattern is a universal PM communication primitive |
| `crypto-web3-context` | — | **KEEP UNCHANGED** — domain knowledge useful for AI/crypto-fintech PM roles you'll target |
| `the-block/` workspace folder | Block-specific PM templates, sprint frameworks, comms templates | Audit each file individually; keep generic templates, archive Block-confidential drafts (PRDs, internal memos) into a separate archive |

### D. Block workspace folder + operating-model artifacts (archive week 2)

| Path | Action |
|---|---|
| `the-block/` (workspace folder) | Move to `the-block-archive/` (or zip + drop in `vault/40_archive/`) |
| `vault/05_atlas/operating-models/the-block/` | Move to `vault/40_archive/operating-models-the-block-2026-05/` |
| `vault/30_domains/product-management/the-block-meetings-granola-notes/` | Stays as historical reference; no further appends |

### E. What stays untouched (DO NOT migrate)

- `crypto-web3-context` skill — useful for AI/fintech roles in your target list
- `intent-engineering` skill — your IP, becoming the MCP server
- `prd-generator`, `tech-spec`, `org-definition-of-done` — general PM craft, valuable in interviews
- `creative-studio/` workspace — your portfolio side, untouched
- `life-systems/` workspace — personal automation, untouched
- All design-team agents, animation pipeline, Remotion skills — untouched
- Vault knowledge loop (indexer, synthesizer, lint, flush) — keeps running, just won't have Block content to chew on

---

## The plan

Five chunks. Do them in order.

### Chunk 1 — Tomorrow morning (5/5), ~10 min: stop the bleed ✅ DONE 2026-05-04

> Sean already pulled the post-layoff contacts (see `vault/20_projects/prj-job-hunt-2026/The-Block-Contacts-After-Layoff.md`) and is handling reference outreach (Larry, Matt) personally — those tasks dropped from this chunk.

- [x] **Disable the daily-driver SDK morning agent** — done in commit `badd489`. Re-enabled in commit `7a78e35` after the rest of the migration landed.
- [x] **Confirm Block Slack/calendar access status** — Sean handled access/data extraction personally; not a repo-side task.

### Chunk 2 — Tomorrow afternoon (5/5), ~60 min: rewire daily-driver for job-hunt + deep-work mode ✅ DONE 2026-05-04

> **Why restructure, not turn off:** the daily-driver SDK agent is already paid-for infrastructure ($0.60/run, fires at 8:45 AM, integrated with the vault). Killing it loses a calibrated morning ritual that's been refined over months. Repointing it at the job-hunt + deep-work goals turns it into a job-hunt accelerant instead of a Block-context relic. ~10 minutes of work to repoint vs. ~hours to rebuild later.

- [x] **Update `daily-driver` skill** — done in commit `fa1415f`. Calendar rule single-source, Slack overnight scan no-op'd (per Sean's Q8 — remove the `U09SC58MYDN` Block-workspace user ID), Apartment Cleanup section removed (March 20 deadline passed).
- [x] **Add new "Step 1a — Job-Hunt + Deep-Work Morning Brief" section** — done in commit `fa1415f`. All 5 signals encoded.
- [x] **Re-enable the SDK agent** — done in commit `7a78e35` (config.toml `enabled = true`).
- [x] **Test with dry-run** — done in commit `7a78e35` close-out. Result: zero `@theblock.co`, zero `the-block` paths, 6 job-hunt + deep-work signal mentions.

### Chunk 3 — Day 2-3 (5/6-5/7), ~45 min: archive operating-model + stop SOUL crossref ✅ DONE 2026-05-04 (compressed timeline)

- [x] **Move the-block operating-model folder** — done in commit `4d862b9` (`git mv` to `vault/40_archive/operating-models-the-block-2026-05/`).
- [x] **Verify the three consumers handle missing artifacts gracefully** — done. Audit + Step 8 (commit `ac2c862`) updated DOMAINS tuple from `("the-block", ...)` to `("creative-studio", "life-systems", "job-hunt-2026")` across 6 production files (`artifact_loader.py`, `daily_driver.py`, `meta_agent.py`, `flush.py`, `knowledge_lint.py`, `process_inbox.py`) so consumers no longer iterate over a missing domain.
- [x] **`domain in ENABLED_DOMAINS` guard** — not needed. Tuple update + `path.exists()` already handle the missing-folder case cleanly.
- [x] **Stand up the new job-hunt operating-model** — done in commit `c4e44ec` (5 placeholder artifacts at `status: awaiting-interview`). **NOTE:** Interview 4 itself (~45 min interactive) is a Sean-runs-this-himself task; placeholders sit at `awaiting-interview` until then. Skill + interview prompt are wired (commits `9daec0c`, `eddb4a1`, `46e18ad`).

### Chunk 4 — Day 4-5 (5/8-5/9), ~90 min: audit + sanitize Block-themed skills (NOT archive) ✅ DONE 2026-05-04 (compressed timeline)

> Per Sean's 5/4 decision: **strip Block-specific lines, keep the underlying PM patterns.** Each skill stays at `.claude/skills/<name>/SKILL.md` — only the content changes. This also pre-stages the Karpathy "consolidate + identify MCP candidates" sweep since you're already touching every file.

- [x] **One pass per skill** — done in commits `b0dba5e` (P1 sweep: intent-engineering, technical-writing, zapier-chrome-automation, meeting-prep) + `161adac` (P2 sweep: 8 Block-themed skills — analytics-workarounds, api-product-management, campus-education, etf-page-creator, jira-automation, revops-adops-automation, sprint-health, stakeholder-update). `crypto-web3-context` kept unchanged (target sector knowledge).
- [x] **time-management skill** — full rewrite in commit `eae934c` (Sean overrode the audit's defer-recommendation per Q5).
- [x] **Tag MCP candidates** — `etf-page-creator` flagged in its commit message as MCP candidate per Karpathy synthesis. (`mcp-candidates.md` parking-lot file not yet created — that's a Phase 4 task in the master plan.)
- [x] **`the-block/` workspace folder** — banner in place at `the-block/CLAUDE.md` and `the-block/README.md` (commit `b0dba5e`). Folder kept at root per `scripts/validate.py` rule #7. No Block-confidential PRD content found in `the-block/product-management/templates/prd-to-launch.md` (only generic sample text).
- [x] **Update root `CLAUDE.md`** — done in commit `62563c9`. Domain table the-block row → "Archived 2026-05 — reference templates from prior role"; calendar rule replaced with single-calendar instruction; routing table now includes job-hunt row.
- [x] **`python3 scripts/validate.py`** — PASSED (60 pre-existing secret-pattern warnings; 0 new errors).

### Chunk 5 — Week 2+, ~45 min: clean up the MCP layer ⏳ DEFERRED to ~5/11

- [ ] **Remove Atlassian MCP from active config** (or leave the auth errors — they're just noisy). Cleaner option: comment out the Atlassian and Slack MCP server entries in your MCP config so they don't show up as tools in Claude Code.
- [ ] **Remove Block calendar from `google-workspace` MCP** active queries — should be implicit once you stop running parallel calendar checks, but verify no hardcoded references.
- [x] **Update `MEMORY.md`** — done in the migration sweep (commit `62563c9` related work; the auto-memory file is at `~/.claude/projects/.../memory/MEMORY.md`). Single-calendar rule in place; Block Jira config moved to `## Archived` section.
- [ ] **Update CLAUDE.md Connected MCPs table** to reflect Block-revoked status. (Calendar rule already updated in commit `62563c9`; the MCPs table itself still lists Block sources — needs a sweep when actual revocation lands.)

---

## Day-by-day calendar of this migration

| Day | Date | What | Effort |
|---|---|---|---|
| 1 | 2026-05-04 (today) | Phase 0 of master plan; nothing on this list | — |
| 2 | 2026-05-05 (Tue) | Chunk 1 (morning, ~10 min) + Chunk 2 (afternoon, restructure daily-driver) | ~70 min |
| 3 | 2026-05-06 (Wed) | Chunk 3 part 1: archive operating-model + verify agents | ~30 min |
| 4 | 2026-05-07 (Thu) | Chunk 3 part 2: build job-hunt HEARTBEAT | ~15 min |
| 5-6 | 2026-05-08/9 (Fri/Sat) | Chunk 4: audit + sanitize 9 Block-themed skills (10 min each, batchable) | ~90 min |
| 7 | 2026-05-10 (Sun) | rest | — |
| 8 | 2026-05-11 (Mon) | Chunk 5: MCP cleanup | ~45 min |

---

## Things I'm explicitly NOT doing (and why)

- **Not deleting anything.** Sanitize in place where possible (skills); archive (don't delete) where sanitization isn't appropriate (Block-confidential PRDs, internal memos, the-block operating-model artifacts).
- **Not rebuilding `time-management` skill yet.** The Block 4:45 AM routine references will look weird but won't break. Rewrite when you have a stable post-Block daily rhythm — give yourself 2 weeks before locking in a new shape.
- **Not touching `creative-studio/` or `life-systems/`.** Those are unrelated to The Block and full of compounding value (animation pipeline, personal finance, health tracking). Don't pause those — they're the foundations of the next chapter.
- **Not pulling `crypto-web3-context` out.** Crypto is a target sector for AI PM roles (a16z crypto, Galaxy, Coinbase, Kraken, Chainlink, Anchorage, etc.). Keep the domain knowledge active.
- **Not drafting reference-outreach messages.** Sean handles Larry / Matt / others personally — they're his relationships.

---

## Migration checklist (mirror in `prj-job-hunt-2026/README.md`)

- [x] Chunk 1 — protect data + Telegram references (done 2026-05-04, commit `badd489`)
- [x] Chunk 2 — daily-driver job-hunt mode (done 2026-05-04, commit `fa1415f`)
- [x] Chunk 3 — archive the-block operating-model (done 2026-05-04, commits `4d862b9` + `c4e44ec` + `ac2c862`)
- [x] Chunk 4 — sanitize Block-specific skills + workspace (done 2026-05-04, commits `b0dba5e` + `161acac` + `eae934c` + `62563c9`)
- [ ] Chunk 5 — MCP cleanup (deferred to ~5/11)

**Resume-here pointer:** [[2026-05-04-migration-completion-handoff|migration completion handoff]] has the full state, validation results, and next-steps priority list.
