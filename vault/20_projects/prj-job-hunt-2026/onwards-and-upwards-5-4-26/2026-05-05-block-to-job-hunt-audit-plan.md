# Onwards-and-Upwards Audit + Operating-Model Plan

## Context

Sean Winslow was laid off from The Block on 2026-05-04 (cost-cutting, not performance). The termination call was delivered by **Larry Cermak (President)** and **Vicky Lu (HR)** — NOT Alex Lebedyev (the meeting was scheduled under Alex's email but Larry ran it). Sean is repurposing this repo for an 8-week job hunt targeting AI PM > Tech PM > Creative PM (Boston metro or remote).

Two canonical strategy documents already exist and are the source of truth for the new direction:
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md) — 8-phase master plan (Track A runway, Track B pipeline, Track C MCP-server differentiator).
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md) — 5-day migration plan (Chunks 1-5).

This plan does NOT re-derive content from those documents. It produces **two read-only deliverables**:
1. **File Audit** — a priority-tiered list of stale-Block references across the repo. Confirms what's already scoped vs flags net-new findings.
2. **Job-Hunt Operating-Model Plan** — Path A vs B vs hybrid recommendation for setting up `vault/05_atlas/operating-models/job-hunt-2026/` so the daily-driver, flush, and meta-agent agents can cross-reference job-hunt rhythms the same way they cross-reference the three current domains.

No file modifications happen in this session. Sean will review and approve this plan before execution begins in a separate session.

---

## Discovery Summary

- **Files searched:** 471 total grep matches for `theblock\|the-block\|swinslow@theblock` across the repo. ~71 outside `vault/` (audit-relevant). ~400 inside `vault/` (mostly historical journal/Granola entries — out of scope per task instructions).
- **Files needing changes:** 27 files outside vault + 5 the-block operating-model artifacts inside vault = **32 files** require edits or archival across P0 + P1 + P2.
- **Operating-model recommendation:** **Hybrid (minimal fork)** — extend the existing `work-operating-model` skill in 3 places (~15 min), run the existing 5-layer interview against a new `job-hunt-2026/` domain folder (~45 min). Total: ~1 hour. **Do NOT create a sibling skill.**

---

## Deliverable 1 — File Audit

### P0 — fix this week

What breaks if we don't fix this: Block calendar/Slack/Atlassian access is being revoked. Anything that auto-queries those services will throw auth errors. The daily-driver SDK agent runs unattended via launchd at 8:45 AM — silent failures are likely.

| File path | Stale content (line numbers) | Recommended change | Priority | Why |
|---|---|---|---|---|
| [.claude/skills/daily-driver/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/daily-driver/SKILL.md) | L95: query BOTH calendars rule incl. `swinslow@theblock.co`. L101: `Sean's Slack user ID is U09SC58MYDN` (this is Sean's **Block** Slack ID — will fail post-revoke). L262-269: same calendar rule restated. | Remove `swinslow@theblock.co` from the parallel-query instruction. Replace L101 Slack ID line with "Slack ID will be re-set once a personal Slack workspace exists; until then the Slack overnight scan is no-op for the job-hunt domain." | P0 | Daily-driver SDK agent at 8:45 AM will fail Step 1 (Step 1: Gather Context) when calendar / Slack queries return auth errors. **Migration Chunk 2 covers calendar; Slack ID line is net-new.** |
| [.claude/skills/time-management/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/time-management/SKILL.md) | L262-269: "Always query BOTH calendars in parallel: `sean.winslow28@gmail.com`, `swinslow@theblock.co`". | Drop the `swinslow@theblock.co` bullet. Same 1-line edit. Defer rest of skill (4:45 AM, 45/35/20, day-types) per migration plan's "not rebuilding yet — give 2 weeks." | P0 | The skill is invoked by the `time-management` and `/today` workflows; calling Google Calendar with a revoked account ID surfaces a hard error. **Net-new finding — migration plan called this skill "won't break" but the calendar line itself does break.** |
| [CLAUDE.md](../../../Code-Brain/claude-code-superuser-pack/CLAUDE.md) | L59: `**Calendar rule:** Always query BOTH sean.winslow28@gmail.com AND swinslow@theblock.co in parallel.` | Replace with "Calendar rule: Single calendar — `sean.winslow28@gmail.com`. The Block work calendar archived 2026-05." | P0 | This is the load-bearing root rule that propagates into every agent's instructions. Migration Chunk 5 covers it but Chunk 5 is Day 8 — bring forward to Day 2 (Chunk 2 day) to keep ahead of access revocation. |
| [the-block/CLAUDE.md](../../../Code-Brain/claude-code-superuser-pack/the-block/CLAUDE.md) | L60: same calendar-both rule. L69: `Granola meeting transcripts at vault/30_domains/.../the-block-meetings-granola-notes/ are the source of truth — don't paraphrase from memory`. L71: `Calendar queries always hit BOTH email accounts`. | Whole file's status changes from "active day-job context" to "archived reference." Add a top-level banner: `> **ARCHIVED 2026-05.** This domain is the prior role at The Block. Templates and patterns retained for portfolio + future reference. Calendar / Atlassian / Slack rules below are no longer enforced.` | P0 | Anything that auto-loads `the-block/CLAUDE.md` via the routing table will pull in stale rules. Migration Chunk 4 mentions updating the routing table but doesn't address the file content itself. **Net-new finding.** |
| [.claude/hooks/daily-note-appender.sh](../../../Code-Brain/claude-code-superuser-pack/.claude/hooks/daily-note-appender.sh) | L46: `*the-block/product-management*) DOMAIN="the-block" ;;` L48: `*the-block*\|*theblock*) DOMAIN="the-block" ;;` L52: `*campus*\|*etf*) DOMAIN="the-block" ;;` | Once Sean's Block-specific work directories no longer exist, these patterns will continue to classify any incidental match as `the-block` and file the daily-note session entry under that domain. Keep the patterns (no harm — they only trigger when working in a `the-block*` named directory) BUT add `*job-hunt-2026*\|*job-hunt*\|*onwards-and-upwards*) DOMAIN="job-hunt" ;;` so job-hunt work gets correctly classified. | P0 | Without the new pattern, all job-hunt session work classifies as `claude-mastery` (the fallback). Sean wants the job-hunt to be a first-class domain in his daily logs. **Net-new finding.** |
| [agents-sdk/lib/artifact_loader.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/lib/artifact_loader.py) | L20: `DOMAINS: tuple[str, ...] = ("the-block", "creative-studio", "life-systems")` | After Chunk 3 archives the-block operating-model folder: replace with `("creative-studio", "life-systems", "job-hunt-2026")`. The `path.exists()` guard at L74 means dropping a domain is graceful (returns None), but the daily-driver preamble still iterates and emits "_(artifact unavailable...)_" for each missing domain. Cleaner to update the tuple. | P0 | If left unchanged after Chunk 3, every daily-driver morning brief, every flush, every knowledge_lint Tier 2 run will emit a "the-block artifact unavailable" line. Cosmetic but signals "system is broken" to anyone reading agent logs. |
| [agents-sdk/agents/daily_driver.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/agents/daily_driver.py) | L95: `for domain in ("the-block", "creative-studio", "life-systems"):` | Same change as artifact_loader. Tuple is hardcoded twice. | P0 | Same reasoning. The on-demand pointer block will emit a stale Block path on every morning brief. |
| [agents-sdk/agents/meta_agent.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/agents/meta_agent.py), [flush.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/agents/flush.py), [knowledge_lint.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/agents/knowledge_lint.py) | TBD — read in this audit was deferred. Each loads SOUL or schedule-recommendations across all 3 domains per `config.toml:[artifacts.per_agent]`. Likely contain hardcoded `("the-block", ...)` tuples too. | Audit + same tuple update post-Chunk 3. Group into the same PR. | P0 | Migration Chunk 3 says "verify the three consumers handle missing artifacts gracefully" but doesn't specify code-level cleanup. Recommend doing it in the same Chunk 3 sweep to avoid leaving "_(unavailable)_" cruft in production agent prompts. |

### P1 — fix in next 2 weeks

Misleading but won't break anything when accessed. Sweep these alongside Chunk 4 (5/8-9) so the visible context everywhere reflects the new direction.

| File path | Stale content (line numbers) | Recommended change | Priority | Why |
|---|---|---|---|---|
| [CLAUDE.md](../../../Code-Brain/claude-code-superuser-pack/CLAUDE.md) | L7: counts "117 skills, 13 subagents, 13 hooks, 14 SDK agents (7 active), 3 primary domain folders". L13-19: domain table — `the-block/` row says "Day-job PM work". L27: routing table says "PM / day-job / Block work → the-block/CLAUDE.md". | Update the domain table the-block row to "**Archived 2026-05** — reference templates from prior role at The Block." Keep the routing table row but mark it `(archived)`. Counts remain valid (no skills deleted, just sanitized in place). Add a 4th routing row for `Job-hunt work → vault/20_projects/prj-job-hunt-2026/`. | P1 | This is what gets auto-loaded into every Claude Code session. Misleading routing means Claude pulls the wrong CLAUDE.md for new tasks. **Migration Chunk 4 partially scoped (says "update routing table") but doesn't enumerate the four other CLAUDE.md changes.** |
| [README.md](../../../Code-Brain/claude-code-superuser-pack/README.md) | (deferred read, mirrors CLAUDE.md per repo convention) | Same edits as CLAUDE.md. Counts stay; domain descriptions updated; add job-hunt-2026 reference. | P1 | Same. Migration plan implies but doesn't enumerate. |
| [vault/Sean-Winslow-Full-Personal-Context-v2.0.md](../../../Code-Brain/claude-code-superuser-pack/vault/Sean-Winslow-Full-Personal-Context-v2.0.md) | L52-53 (per prior audit): "As of May 2026, the org is mid-shuffle — Matt Vitebsky left, Ed is being promoted, and a promotion path for Sean is being discussed". L106: "Ed Rupkus \| Manager at The Block + cross-domain north-star \| Sean's day-to-day reporting line AND his aspirational PM model". L182: dual-calendar rule restated. L206: "Block roadmap prep" listed as active project. | Major update. Add a new top section: `## Career Status (2026-05-04)` with: laid off 2026-05-04 (cost-cutting), running 8-week job hunt, target archetype priority AI PM > Tech PM > Creative PM, primary reference Larry Cermak, see prj-job-hunt-2026/ for live status. Move Ed-as-reporting-line content into a `### Prior Role: The Block (Nov 2025 – May 2026)` archive section. Drop the dual-calendar line. Drop "Block roadmap prep" project line. | P1 | This is the **Tier-0 identity document** that sits above all three operating-model bundles. It's loaded as preamble context by the daily-driver morning agent and other downstream agents. Stale identity = stale judgment by every agent. **Net-new finding — migration plan does not list this file.** |
| [vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md) | L27: `Recommended order: 1. the-block first`. L37-65: entire "Interview 1 — The Block" section with the prompt referencing `swinslow@theblock.co`, "sprint ceremonies, bi-weekly P&E update", `the-block-meetings-granola-notes/`. L138-156: wrap-up prompt assumes 3 interviews. | Mark "Interview 1 — The Block" with a `> **Archived 2026-05.** Interview content preserved for reference; do not re-run.` banner. Add a new "Interview 4 — Job Hunt 2026" section with start prompt, commit prompt, and cross-check prompt that mirror the existing 3 (the prompts are template-shaped already). Update L27 recommended order to: `1. job-hunt-2026 first (active during 8-week search)`. Update wrap-up prompt to reflect 3 active + 1 archived bundle. | P1 | The playbook is what Sean uses to actually run the interviews. Without an Interview 4, he has to compose the prompt from scratch — small but avoidable friction. **Net-new finding.** |
| [vault/05_atlas/operating-models/README.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/README.md) | L3: `domain: [the-block, creative-studio, life-systems]`. L11: lists `meeting-defender` (deleted per migration plan). L25: bullet `[[the-block/HEARTBEAT\|The Block — day job (PM at crypto/ETF company)]]`. L37: Tier-0 link reference. | Update frontmatter domain array: `[creative-studio, life-systems, job-hunt-2026]`. Drop `meeting-defender` from L11. Replace L25 the-block bullet with `[[the-block/HEARTBEAT\|The Block — archived 2026-05, see vault/40_archive/operating-models-the-block-2026-05/]]` and add new bullet for job-hunt-2026. | P1 | This is the index for the operating-models folder. If it lists `the-block` as active when the bundle has moved to archive, the daily-driver and meta-agent (which iterate domains from this folder) get a misleading map. **Net-new finding.** |
| [.claude/skills/work-operating-model/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/work-operating-model/SKILL.md) | L3: description lists "the-block, creative-studio, life-systems". L12: same trio. L23: same. L39: domain table the-block row "Sean as PM at The Block — crypto/ETF company, Boston, swinslow@theblock.co". L43: "If Sean says 'the Block' or 'Block' → the-block". L83-87: "Domain-Specific Tuning Notes — The Block" subsection. | Edit in place to add 4th domain. Keep the-block rows (now archived) so historical interviews can still be re-run. Add: (a) a 4th row to the domain table for `job-hunt-2026`, (b) a 4th routing rule "If 'job hunt' or 'hunt' → job-hunt-2026", (c) a new `### Job Hunt 2026` tuning subsection. See Deliverable 2 for exact wording. | P1 | This is Path C from Deliverable 2. **Net-new finding — migration plan doesn't mention this skill.** |
| [.claude/skills/work-operating-model/interview-questions.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/work-operating-model/interview-questions.md) | L16-18: "**The Block:** sprint ceremonies + bi-weekly Product & Engineering update cadence." L21: "How do you split swinslow@theblock.co time vs sean.winslow28@gmail.com time for this domain?" | Add a 4th bullet for **Job Hunt 2026** under Layer 1 Q2 (suggested: "weekly application+outreach batches, interview cycles, Friday weekly retro"). For L21 (Q5), soften: "How does this domain's work flow split across your active email accounts? Note: `swinslow@theblock.co` is being archived 2026-05; default forward to `sean.winslow28@gmail.com`." | P1 | Same reasoning as work-operating-model SKILL.md. **Net-new finding.** |
| [.claude/skills/work-operating-model/artifact-templates.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/work-operating-model/artifact-templates.md) | L52-53: HEARTBEAT.md template lists swinslow@theblock.co usage. | Add a 4th line: `- Job hunt usage: ...` or replace the Block reference with a generic placeholder `- Work email usage: ...` since the Block address is being phased out. | P1 | Template is Block-shaped. **Net-new finding.** |
| [the-block/README.md](../../../Code-Brain/claude-code-superuser-pack/the-block/README.md) | (deferred read, but flagged by grep) | Add archive banner. | P1 | Domain doc, mostly cosmetic but reflects the new reality. |
| [the-block/product-management/templates/prd-to-launch.md](../../../Code-Brain/claude-code-superuser-pack/the-block/product-management/templates/prd-to-launch.md) | (deferred read, flagged by grep) | If the only Block reference is sample text in the PRD template ("Example: The Block Data API..."), generalize to "Example: a crypto data API". If it has Block-confidential PRD content, move to `vault/40_archive/the-block-internal-2026-05/`. | P1 | Template is reusable IP per migration plan's strip-and-keep philosophy. |
| [.claude/skills/intent-engineering/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering/SKILL.md) and [references/intent-spec-template.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering/references/intent-spec-template.md) | Worked daily-driver example may reference Block calendar / Block standup. (Need to grep within the skill for exact lines.) | Generalize the worked example. **Migration plan explicitly says "intent-engineering — your IP, becoming the MCP server — leave untouched"** so the change is minimal: just replace any incidental Block sample data with generic equivalents. Don't refactor the skill structure. | P1 | This is Sean's flagship MCP-server skill per Karpathy synthesis. Block sample data weakens the portfolio piece. **Net-new finding — migration plan explicitly preserved this skill but didn't audit incidental Block refs in samples.** |
| [.claude/skills/technical-writing/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/technical-writing/SKILL.md) | L51-71: "Example 1: API Getting-Started Guide" hardcodes `# Getting Started with The Block Data API` and `https://api.theblock.co/v1/prices/BTC`. | Replace example with generic crypto data API example: `# Getting Started with the Crypto Market Data API` and `https://api.example-crypto.com/v1/prices/BTC`. | P1 | Skill is general-purpose technical-writing craft. Block branding in the example weakens reusability and looks dated. **Net-new finding — not in the migration plan's 9 skills list.** |
| [.claude/skills/zapier-chrome-automation/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/zapier-chrome-automation/SKILL.md) | (Block reference detected by grep — exact line not surfaced in the partial read; likely in the example workflow descriptions or sample prompts.) | Same as technical-writing: replace with generic. | P1 | **Net-new finding — not in migration plan's 9 skills.** |
| [.claude/skills/meeting-prep/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/meeting-prep/SKILL.md) | Whole file (321 lines) is Block-team roster, recurring meetings, JQL queries against PRO/RBS/CM, Retros.work specifics. | Per migration plan Chunk 4: strip Block specifics. Keep the **patterns** — agenda structure, 1:1 prep template, retro synthesis flow, post-meeting action items. Drop the team roster (L36-72), drop the Block-specific cadence table (L26-34), drop JQL queries (L173-180, 219-223), drop Retros.work as the named tool (replace with "your retro tool"). | P1 | **Already in migration Chunk 4 (5/8-9).** Just confirming scope — about 60% of file content is Block-specific. |
| [the 8 other Block-themed skills per migration Chunk 4] | Per Chunk 4 table | Per Chunk 4: analytics-workarounds, api-product-management, campus-education, etf-page-creator, jira-automation, revops-adops-automation, sprint-health, stakeholder-update — all sanitize-in-place. | P2 (see below) | Already scoped. |
| [agents-sdk/config.toml](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml) | L68: `project_key = "BE"` (Block Jira project key for sprint_health agent). | sprint_health agent is `enabled = false` per L64 so this is dormant. Either drop the line entirely or generalize to `project_key = "TBD"` with a comment "configure when active". | P1 | Cosmetic only — agent is disabled. **Net-new finding.** |
| [agents-sdk/tests/conftest.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/conftest.py), [test_artifact_loader.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_artifact_loader.py), [test_daily_driver_artifacts.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_daily_driver_artifacts.py), [test_flush.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_flush.py), [test_knowledge_lint.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_knowledge_lint.py), [test_meta_agent_artifacts.py](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_meta_agent_artifacts.py) | Test fixtures hardcode `the-block` as a domain string. (Specific lines not yet read.) | When updating the `DOMAINS` tuple in artifact_loader.py / daily_driver.py / meta_agent.py / flush.py / knowledge_lint.py, update the test fixtures to match. Either rename `the-block` fixtures to `job-hunt-2026` OR introduce a generic `test-domain` fixture so the test suite isn't tied to current domain reality. | P1 | Tests will fail if the production code drops `the-block` from DOMAINS but tests still expect it. Catch this on first `pytest` run. **Net-new finding.** |
| [agents-sdk/benchmarks/golden_sets/inbox_triage.json](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/benchmarks/golden_sets/inbox_triage.json) | (Block references in benchmark test cases.) | Update the benchmark to remove Block-specific examples or label them as historical. process_inbox is paused per migration so this benchmark is dormant — low urgency. | P1 | Benchmark integrity matters when process_inbox Path B rewrite ships. **Net-new finding.** |
| [creative-studio/CLAUDE.md](../../../Code-Brain/claude-code-superuser-pack/creative-studio/CLAUDE.md), [life-systems/CLAUDE.md](../../../Code-Brain/claude-code-superuser-pack/life-systems/CLAUDE.md) | (Cross-references to the-block domain or Block calendar in cross-domain context sections.) | Audit each file for incidental Block refs (e.g., "schedule around Block standup"); update to reflect post-Block schedule. | P1 | Cross-domain bleed — these files describe *other* domains but may mention Block constraints. **Net-new finding.** |
| [scripts/validate.py](../../../Code-Brain/claude-code-superuser-pack/scripts/validate.py) | (v3.15.0 hard-enforces 3 primary domain folders: the-block/, creative-studio/, life-systems/.) | If `the-block/` workspace folder is moved to archive (Chunk 4 open question), the validator hard-enforcement will fail. Either: (a) keep the-block/ in place with archive banner so validator still finds it, or (b) update the validator to drop the the-block check. Recommend (a) — minimum-change. | P1 | Hard-enforced rule per CLAUDE.md L188. Whichever path Sean picks, validator + CLAUDE.md L188 must agree. **Net-new finding — migration plan doesn't address this.** |
| [vault/05_atlas/operating-models/the-block/HEARTBEAT.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/the-block/HEARTBEAT.md), [USER.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/the-block/USER.md), [SOUL.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/the-block/SOUL.md), [operating-model.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/the-block/operating-model.md), [schedule-recommendations.md](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/the-block/schedule-recommendations.md) | Whole bundle is the prior role's operating model. | **Move (don't delete)** the entire folder to `vault/40_archive/operating-models-the-block-2026-05/` per migration Chunk 3. The archive preserves history; agents already handle the missing folder gracefully via `path.exists()` guard in artifact_loader.py. | P1 | **Already in migration Chunk 3 (5/6-7).** Just confirming scope. |
| [MEMORY.md](../../../Code-Brain/claude-code-superuser-pack/CLAUDE.md) (root memory file) and [/Users/seanwinslow/.claude/projects/.../memory/](file:///Users/seanwinslow/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/) | "Sean's Google Calendars — query BOTH" rule. "The Block Jira Config" reference block. `project_block_layoff_2026-05-04.md` already exists (good). | Per migration Chunk 5: update calendar rule to single-calendar. Move "The Block Jira Config" to a `## Archived` section. Keep the layoff project memory file as-is (correctly captures the pivot). | P1 | **Already in migration Chunk 5 (5/11).** Confirming scope. |

### P2 — sanitization sweep (already scoped in migration plan)

These are the 9 Block-themed skills already enumerated in [migration plan Chunk 4](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md). Don't re-derive — confirm scope only.

| File path | Migration plan disposition |
|---|---|
| [.claude/skills/analytics-workarounds/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/analytics-workarounds/SKILL.md) | Generalize to "PM-without-direct-analytics-tool patterns" |
| [.claude/skills/api-product-management/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/api-product-management/SKILL.md) | Replace Block Data API examples with generic data-API examples |
| [.claude/skills/campus-education/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/campus-education/SKILL.md) | Generalize to "education platform / LMS PM patterns" |
| [.claude/skills/etf-page-creator/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/etf-page-creator/SKILL.md) | Generalize to "structured-content publisher" pattern; flagged as MCP candidate |
| [.claude/skills/jira-automation/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/jira-automation/SKILL.md) | Drop Block project keys / components; keep automation patterns |
| [.claude/skills/meeting-prep/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/meeting-prep/SKILL.md) | Strip Block recurring meetings + roster; keep prep templates |
| [.claude/skills/revops-adops-automation/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/revops-adops-automation/SKILL.md) | Generalize to RevOps/AdOps PM patterns for media+data |
| [.claude/skills/sprint-health/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/sprint-health/SKILL.md) | Make project key configurable; strip Block component IDs |
| [.claude/skills/stakeholder-update/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/stakeholder-update/SKILL.md) | Generalize the bi-weekly P&E template |
| [.claude/skills/crypto-web3-context/SKILL.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/crypto-web3-context/SKILL.md) | **KEEP UNCHANGED** per migration plan |

### Verified clean

Files I read that are **not** stale-Block — already in good shape, no audit row needed:

- [vault/20_projects/prj-job-hunt-2026/README.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/README.md) — the live job-hunt tracker. Just created 2026-05-04. Up-to-date.
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md) — master plan. Authoritative.
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md) — migration plan. Authoritative; references in this audit document just confirm scope.
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow.md) — strategic anchor.
- [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/The-Block-Final-Meeting-5-4-26.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/The-Block-Final-Meeting-5-4-26.md) — historical record of termination meeting (Larry Cermak + Vicky Lu delivered the call; correctly attributed).
- [vault/20_projects/prj-job-hunt-2026/The-Block-Contacts-After-Layoff.md](../../../Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/The-Block-Contacts-After-Layoff.md) — post-layoff contact roster. Active.
- [.claude/skills/work-operating-model/artifact-templates.md](../../../Code-Brain/claude-code-superuser-pack/.claude/skills/work-operating-model/artifact-templates.md) — mostly clean; one Block-specific line (P1 above), rest is generic markdown templates.
- [agents-sdk/config.toml](../../../Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml) — clean except L68 `project_key = "BE"` (P1 above) and disabled-agent comments referencing Block context historically.
- [vault/05_atlas/operating-models/creative-studio/](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/creative-studio/) — domain bundle for creative studio. Untouched per migration plan.
- [vault/05_atlas/operating-models/life-systems/](../../../Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/life-systems/) — domain bundle for life systems. Untouched.
- All ~400 historical journal entries inside [vault/10_timeline/daily/](../../../Code-Brain/claude-code-superuser-pack/vault/10_timeline/daily/), [vault/30_domains/product-management/the-block-meetings-granola-notes/](../../../Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-meetings-granola-notes/), [vault/02_Areas/Agent-Fleet/](../../../Code-Brain/claude-code-superuser-pack/vault/02_Areas/Agent-Fleet/) — out of scope per task. These are factually-accurate-for-their-time records of past work.

---

## Deliverable 2 — Job-Hunt Operating Model

### Recommendation

**Use Path C (hybrid) — minimal in-place fork of the existing `work-operating-model` skill. Do NOT create a sibling skill.**

The interview-questions.md is **80% domain-agnostic by design**. Layers 1-5 ask universally-applicable questions (operating rhythms, recurring decisions, dependencies, institutional knowledge, friction). Only 4 lines need domain-specific tuning, and the SKILL.md already has a "Domain-Specific Tuning Notes" section that contains 3 subsections (one per current domain) — extending it to 4 subsections is the natural extension point. The existing skill's checkpoint behavior (summarize → confirm → write per layer) and frontmatter status lifecycle (`awaiting-interview` → `draft` → `confirmed`) work as-is. Reusing the proven architecture costs ~15 minutes of skill edits vs hours rewriting from scratch. This matches Sean's stated preference for sanitize-and-reuse over create-new (per the 9-Block-skills decision) and the Karpathy synthesis preference for consolidating skills, not adding more.

The 8-week timeline reinforces the recommendation. The operating model only needs to last through the job hunt, then either retire (job found) or evolve into a new role-specific bundle. Investing in a forked sibling skill that runs maintenance overhead for 8 weeks is over-engineering. A 15-minute edit-in-place captures 90% of the value.

The daily-driver restructure (migration Chunk 2, 5/5 afternoon) needs the new HEARTBEAT.md as input — the morning brief surfaces "Job-hunt status, today's interview events, deep-work focus" per Chunk 2's spec, and the HEARTBEAT.md is the source for those rhythms. Path C lets Sean run the interview Wednesday 5/6 and have the artifact live before the daily-driver re-enables. Path B would push the artifact creation to 5/8-9 — too late. Path A would produce a usable but awkward artifact (Layer 1 Q5 about Block calendar split would feel forced).

### Proposed file structure

```
vault/05_atlas/operating-models/
├── README.md                              # update: add job-hunt-2026 row, mark the-block archived
├── INTERVIEW-PLAYBOOK.md                  # update: add Interview 4, archive Interview 1
├── creative-studio/                       # unchanged (5 artifacts)
├── life-systems/                          # unchanged (5 artifacts)
└── job-hunt-2026/                         # NEW — 5 artifacts in awaiting-interview state
    ├── HEARTBEAT.md
    ├── USER.md
    ├── SOUL.md
    ├── operating-model.md
    └── schedule-recommendations.md

# After Chunk 3 archive:
vault/40_archive/operating-models-the-block-2026-05/
├── HEARTBEAT.md                           # moved from vault/05_atlas/operating-models/the-block/
├── USER.md
├── SOUL.md
├── operating-model.md
└── schedule-recommendations.md
```

### Proposed sequence of changes

Order matters — this sequence threads through migration Chunks 2-3 so the operating-model artifacts are ready when the daily-driver re-enables.

1. **(Migration Chunk 1, Tue 5/5 AM, ~10 min)** Disable daily-driver SDK agent (`agents-sdk/config.toml:8` flip `enabled = true → false`). Confirms migration plan; not new work.

2. **(Migration Chunk 2, Tue 5/5 PM, ~60 min)** Rewire daily-driver skill per migration plan; remove Block calendar pulls. Re-enable agent.

3. **(NEW — recommend Wed 5/6 AM, ~15 min)** Edit `.claude/skills/work-operating-model/SKILL.md` in 4 places:
   - **L3 (description):** Add `job-hunt-2026` to the domain enumeration: `Takes a required domain argument: one of "the-block" (archived), "creative-studio", "life-systems", "job-hunt-2026".`
   - **L39 (Domain Argument Handling table):** Add a 4th row:
     ```
     | `job-hunt-2026` | `vault/05_atlas/operating-models/job-hunt-2026/` | Sean executing 8-week job hunt — AI/Tech/Creative PM, Boston metro or remote |
     ```
   - **L43 (routing rules):** Add: `If "job hunt", "hunt", "search", or "onwards" → job-hunt-2026.`
   - **After L97 (Domain-Specific Tuning Notes):** Add a new subsection:
     ```markdown
     ### Job Hunt 2026
     - Layer 1, Q2: Weekly application + outreach batch rhythm; interview cycle scheduling. Friday weekly retro per prj-job-hunt-2026/README.md.
     - Layer 1, Q5: Most flow through `sean.winslow28@gmail.com` (the-block address being archived 2026-05). Track recruiter/interview emails separately or via Gmail labels.
     - Layer 2: Auto-yes for warm-intro outreach; auto-no for cold-recruiter spam. Target archetype priority: AI PM > Tech PM > Creative PM. Boston metro or remote.
     - Layer 3, Q1: Larry Cermak (primary reference), Matt (personal — handled directly), 9 P&E peers per The-Block-Contacts-After-Layoff.md.
     - Layer 5: Application fatigue, interview prep collisions, offer-decision paralysis are the prime friction points. Look for automation candidates that move 20+ min tasks to 2.
     ```

4. **(Same session, 5/6 AM, ~5 min)** Edit `.claude/skills/work-operating-model/interview-questions.md`:
   - **L16-18 (Layer 1 Q2):** Add a 4th sub-bullet:
     ```
     - **Job Hunt 2026:** weekly application/outreach batches, interview cycles, Friday weekly retro per prj-job-hunt-2026/README.md.
     ```
   - **L21 (Layer 1 Q5):** Soften: `How does this domain's work flow split across your active email accounts? (Note: swinslow@theblock.co is being archived 2026-05; default forward to sean.winslow28@gmail.com.)`

5. **(Same session, 5/6 AM, ~2 min)** Create the 5 placeholder artifact files at `vault/05_atlas/operating-models/job-hunt-2026/{HEARTBEAT,USER,SOUL,operating-model,schedule-recommendations}.md` with minimal frontmatter (`status: awaiting-interview`, `domain: [job-hunt-2026]`, etc.) — this is what the work-operating-model skill expects to find at the start of an interview.

6. **(Same session, 5/6 AM, ~5 min)** Edit `vault/05_atlas/operating-models/README.md` — add job-hunt-2026 bullet, mark the-block archived. Edit `vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md` — add Interview 4 prompts (start, commit, cross-check), banner Interview 1 as archived.

7. **(Migration Chunk 3, Wed 5/6 PM, ~30 min)** Per migration plan: archive `vault/05_atlas/operating-models/the-block/` to `vault/40_archive/operating-models-the-block-2026-05/`. Verify agents handle missing artifacts gracefully (artifact_loader.py L74 `path.exists()` already guards this).

8. **(NEW — Wed 5/6 PM, ~5 min, after step 7)** Update domain tuples in agents-sdk:
   - `agents-sdk/lib/artifact_loader.py:20`: `DOMAINS = ("creative-studio", "life-systems", "job-hunt-2026")`
   - `agents-sdk/agents/daily_driver.py:95`: same tuple
   - `agents-sdk/agents/meta_agent.py`, `flush.py`, `knowledge_lint.py`: audit for hardcoded `the-block` and update to match
   - `agents-sdk/tests/*.py`: update fixtures (rename `the-block` to `job-hunt-2026` OR introduce a generic `test-domain` fixture)
   - Run `cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/ -q` — must stay green.

9. **(Wed 5/6 PM or Thu 5/7 AM, ~45 min interactive)** Run the interview: in an interactive Claude Code session, paste the new Interview 4 prompt from INTERVIEW-PLAYBOOK.md. Walk through all 5 layers with checkpoints. Skill writes 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/`, status moves `awaiting-interview` → `draft` → `confirmed`.

10. **(Thu 5/7 PM, ~5 min)** Verify the daily-driver morning agent picks up the new HEARTBEAT.md the next day (8:45 AM Friday 5/8). Dry-run check:
    ```
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run | grep -A 3 "job-hunt-2026"
    ```
    Expected: HEARTBEAT body for job-hunt-2026 surfaces in the preamble; no the-block references; no "_(artifact unavailable...)_" lines.

11. **(Migration Chunks 4-5, 5/8-11)** Per migration plan as written. Add the P1 "net-new" findings from this audit (Sean-Winslow-Full-Personal-Context-v2.0.md, INTERVIEW-PLAYBOOK.md, work-operating-model SKILL.md, intent-engineering, technical-writing, zapier-chrome-automation skills) to the Chunk 4 batch since the Block sanitization pass already touches `.claude/skills/*`.

**Total net-new work beyond migration plan: ~30 minutes of edits + ~45 min interactive interview = ~1.25 hours.** Plus the audit-induced additions to Chunks 4-5 (sanitizing the 6 net-new files) — ~30 minutes more.

---

## Open Questions for Sean — RESOLVED 2026-05-04

> Resolutions captured in this section after Sean's two-round AskUserQuestion gate at the start of the migration execution session. All 8 resolved before Step 1 began.

1. **the-block/ workspace folder disposition.** **RESOLVED:** Banner in place. Workspace folder stays at repo root; archive banner added at top of `the-block/CLAUDE.md` and `the-block/README.md`. Validator stays happy. Block-confidential drafts NOT moved to `vault/40_archive/the-block-internal-2026-05/` in this pass — the audit found no Block-confidential PRD content in `the-block/product-management/templates/prd-to-launch.md` (only generic sample text).

2. **the-block/CLAUDE.md fate.** **RESOLVED:** Banner in place (consistent with #1).

3. **work-operating-model approach.** **RESOLVED:** Path C (extend in place). 4th domain added; the-block kept as a (now-archived) selectable domain so historical interviews can still be re-run. ~15 minutes of skill edits as the audit projected.

4. **agents-sdk tests/ fixture strategy.** **RESOLVED:** Option B (generic test-domain fixture) — adapted at execution time. The `tmp_artifacts` fixture in `agents-sdk/tests/conftest.py` uses production domain literals (`creative-studio` / `life-systems` / `job-hunt-2026`) for integration tests so they assert real-system behavior, while `test_artifact_loader.py`'s lower-level unit tests use generic `test-domain-{a,b,c}` names locally inside their assertions. Documented in the conftest.py docstring.

5. **time-management skill rewrite scope.** **RESOLVED — Sean OVERRODE the audit's defer-recommendation in favor of full rewrite now.** Sean provided 4 rhythm inputs at execution time (5:30 AM wake, Track A/B/C structure, Friday 4:30–5:30 PM weekly retro, 5:30 PM hard stop). Skill rewritten end-to-end. Note in commit: when an offer signs and a new role brings new rhythms, this skill should be re-rewritten then.

6. **CHANGELOG.md handling.** **RESOLVED:** Add v3.26.0 entry "Block-to-job-hunt migration" linking to both this audit plan and the migration plan. Done.

7. **Daily-driver morning agent timing.** **RESOLVED:** Re-enable Tue PM (after Chunk 2 lands). Wed AM brief won't yet have the populated job-hunt-2026 HEARTBEAT body (interview is recommended Wed 5/6) but will be fully Block-clean — no `swinslow@theblock.co` calendar query, no the-block iteration in DOMAINS, no `_(artifact unavailable...)_` lines. Job-hunt context surfaces from `vault/20_projects/prj-job-hunt-2026/README.md` until the interview populates the HEARTBEAT.

8. **Slack user ID line in daily-driver SKILL.md.** **RESOLVED:** Remove entirely. Slack overnight scan no-op'd until a personal Slack workspace is wired in. Historical pattern preserved as reference in the SKILL.md for re-enable.

---

## Validation Checklist

- [x] Read every file in the "must audit at minimum" list (or explained deferrals — meta_agent.py, flush.py, knowledge_lint.py, the-block operating-model artifact bodies, and a few skill files were partially read; full audit deferred to execution session).
- [x] Larry Cermak and Vicky Lu (NOT Alex Lebedyev) referenced correctly in Context section.
- [x] Operating-model recommendation accounts for the 8-week timeline (Path B rejected as over-engineering; Path C chosen for minimum maintenance).
- [x] Every P0 item has a clear "what breaks" rationale.
- [x] grep discovery sweep ran (471 total matches; 71 outside vault).
- [x] No file modifications made during this session — Plan Mode preserved; only the plan file at `/Users/seanwinslow/.claude/plans/distributed-sprouting-frog.md` was written.
