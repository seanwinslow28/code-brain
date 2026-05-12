---
title: "prj-job-hunt-2026"
type: project
project: prj-job-hunt-2026
status: active
domain: [life-systems, career-transition]
started: 2026-05-04
target-completion: 2026-08-15
last-updated: 2026-05-12-evening
ai-context: "Active job hunt after May 4, 2026 layoff from The Block. Targeting AI PM / Technical PM / Creative PM roles, Boston metro or remote. Canonical plan: vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md."
---

# prj-job-hunt-2026 — Onwards and Upwards

The dashboard. Plan and migration docs are linked below; this file is the live tracker.

## Status

- **Day:** 1 of search (started 2026-05-04 — layoff day)
- **Phase:** Phase 0 → Phase 1 transition (logistics + positioning prep)
- **Repo migration (Block → job-hunt):** [x] **DONE 2026-05-04 evening** — 13 commits on `feat/gemini-deep-research-v3.25.0`. See [[onwards-and-upwards-5-4-26/2026-05-04-migration-completion-handoff|handoff doc]] for the resume-here pointer.
- **Operating-model interview (job-hunt-2026):** [x] **DONE 2026-05-05** — all 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/` at `status: confirmed`. Daily-driver / meta-agent / flush / knowledge-lint will start consuming on next runs. See [[../../05_atlas/operating-models/job-hunt-2026/operating-model|operating-model.md]] for the synthesis + 9 surfaced open work items.
- **Severance signed:** [ ] (deadline ~2026-05-11)
- **UI claim filed:** [ ] (target: 2026-05-05)
- **Health insurance decided:** [ ] (deadline: 2026-07-03 for SEP)
- **Resume v1 done:** [ ] (target: 2026-05-11)
- **LinkedIn refreshed:** [ ] (target: 2026-05-15)
- **First MCP server public:** [ ] (target: 2026-05-25)
- **Open to Work toggled:** [ ] (target: 2026-05-18 — after artifacts ship)
- **Migration Chunk 5 — MCP cleanup:** [ ] (target: 2026-05-11 — Atlassian + Block calendar)
- **Vault Synthesizer Eval Suite (Task 8 Step 2):** [x] **CODE COMPLETE 2026-05-12** — 14 commits on `eval-suite-2026-05-12`. 10-case binary pass/fail suite at [`evals/vault-synthesizer/`](../../../evals/vault-synthesizer/). Baseline 1/10 at ship-state. 6th flagship portfolio artifact, ahead of 2026-05-22 ship date by 10 days.
- **Synthesizer fix (Task 8 Step 3 / Workstream B):** [x] **CODE COMPLETE 2026-05-12** — 8 commits patching `agents-sdk/agents/vault_synthesizer.py` (status taxonomy + model_used enum), `agents-sdk/lib/pushover.py` (boot credential check), `agents-sdk/agents/daily_driver.py` (WARNING render). Suite jumps to 7/10 post-fix.
- **Substack-Drafter agent (Task 9 / Workstream C):** [x] **CODE COMPLETE 2026-05-12** — 10 commits. Agent at `agents-sdk/agents/substack_drafter.py` (~370 lines, 33 TDD tests), Thursday-18:00 launchd plist, opt-in via `INSTALL_SUBSTACK_DRAFTER=1`, three kill-switch layers. 7th flagship portfolio artifact. Pilot drafts (C9) gated on Workstream B's 5-night live-synth gate closing.
- **Pushover keychain creds:** [x] **DONE 2026-05-12** — `com.sean.agents.pushover_user_key` + `com.sean.agents.pushover_api_token` added via `security add-generic-password`. Satisfies vs-019 boot check requirement.
- **B7 — 5-night live-synth gate:** [ ] **calendar wait** (target window: 2026-05-17 → 2026-05-28). 5 consecutive nights of `concepts_written > 0` in `vault/health/synth-manifest-*.json`. Required precondition for C9 pilot drafts and the 2026-05-29 follow-up Substack post.
- **A14 — Substack + LinkedIn publish (eval suite):** [ ] (target: Friday 2026-05-22, primary Sedaris draft + Wednesday 2026-05-27 LinkedIn syndication)
- **A13 — Loom recording (eval suite, 5 min unedited):** [ ] (target: 2026-05-21, pre-publish)
- **C9 — 3 pilot drafts (Substack-Drafter):** [ ] (post-B7 gate; Sean reviews each cold; if all 3 publishable-with-edits → `INSTALL_SUBSTACK_DRAFTER=1` installs launchd plist)

## Plan + key docs

All launch-day artifacts live in the `onwards-and-upwards-5-4-26/` sibling folder. Master plan: [[2026-05-04-onwards-and-upwards-plan]].

- **🟢 RESUME-HERE handoff (read first in a fresh session):** [[onwards-and-upwards-5-4-26/2026-05-04-migration-completion-handoff|2026-05-04-migration-completion-handoff.md]]
- **Master plan:** [[onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan|2026-05-04-onwards-and-upwards-plan.md]]
- **Migration plan (Block → job hunt):** [[onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration|2026-05-05-block-to-job-hunt-migration.md]] — Chunks 1-4 done; Chunk 5 (MCP cleanup) deferred to ~5/11.
- **Audit + execution plan (with 8 RESOLVED resolutions):** [[onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-audit-plan|2026-05-05-block-to-job-hunt-audit-plan.md]]
- **Karpathy synthesis (strategic anchor):** [[onwards-and-upwards-5-4-26/Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow|Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow.md]]
- **Final Block meeting transcript + new CEO message:** [[onwards-and-upwards-5-4-26/The-Block-Final-Meeting-5-4-26|The-Block-Final-Meeting-5-4-26.md]]
- **Block calendar export:** `onwards-and-upwards-5-4-26/swinslow@theblock.co.ical`

## References

The 5/4 termination call was actually delivered by **Larry Cermak (President)** and **Vicky Lu (HR)**, not Alex Lebedyev (the meeting was set up under Alex's email but he didn't run the call — Larry did). Larry is the strongest professional reference.

| Name | Role | Relationship | Best contact | Status |
|---|---|---|---|---|
| Larry Cermak | President, The Block | Delivered the news, offered "anywhere" referral | Telegram `@lawmaster10` · `cermak.vavrinec@gmail.com` | Offered, not yet activated |
| Matt | Former CPO, The Block | High-school friend who hired Sean in; offered "anywhere" referral | Sean's personal contact (handled directly, not via this tracker) | Offered |
| TBD | Block peer (eng or design) | Cross-functional collaborator | See `The-Block-Contacts-After-Layoff.md` | Pending — pick from the post-layoff contact list |
| TBD | Pre-Block role | Long-arc credibility | TBD | Pending |

**Vicky Lu (HR)** — point of contact for severance / W-2 / benefits questions. Not a reference.

> Full post-layoff contacts (Larry + 9 P&E teammates who shared info in the 5/4 huddle): see [[The-Block-Contacts-After-Layoff]] in this folder.

## Pipeline

| Company | Role | Source | Applied | Status | Inside contact | Next action |
|---|---|---|---|---|---|---|
| _empty until Phase 5_ | | | | | | |

## Artifacts

| Artifact | Location | Status | Version |
|---|---|---|---|
| Master resume | `vault/20_projects/prj-job-hunt-2026/resume-master-2026-05.md` | not started | v0 |
| Resume — AI PM variant | `vault/20_projects/prj-job-hunt-2026/resume-ai-pm.md` | not started | v0 |
| Resume — Tech PM variant | `vault/20_projects/prj-job-hunt-2026/resume-tech-pm.md` | not started | v0 |
| Resume — Creative PM variant | `vault/20_projects/prj-job-hunt-2026/resume-creative-pm.md` | not started | v0 |
| LinkedIn About section | (LinkedIn) | not started | v0 |
| GitHub profile README | `github.com/<user>/<user>/README.md` | not started | v0 |
| Talk track | `vault/20_projects/prj-job-hunt-2026/talk-track.md` | not started | v0 |
| Story bank | `vault/20_projects/prj-job-hunt-2026/story-bank.md` | not started | v0 |
| MCP server #1 — `intent-engineering` | `~/Code/sw-mcp-intent-engineering/` | not started | v0 |
| **Vault Synthesizer Eval Suite (#6 flagship)** | `evals/vault-synthesizer/` | **code complete 2026-05-12; pending Loom + Substack publish 2026-05-22** | v1 (7/10 post-fix) |
| **Substack-Drafter agent (#7 flagship)** | `agents-sdk/agents/substack_drafter.py` | **code complete 2026-05-12; pending C9 pilot drafts after B7 gate** | v1 (default-disabled) |
| Public announcement post | `vault/20_projects/prj-job-hunt-2026/public-announcement.md` | drafted later | v0 |
| First essay (intent-spec or production diary) | TBD | parking lot | v0 |
| Substack post 1 — "The Night My Vault Said Nothing" (Sedaris) | `vault/20_projects/.../substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md` | drafted, ships Friday 2026-05-22 | v1 |
| Substack post 1 — Kerouac variant | `vault/20_projects/.../substack-drafts/2026-05-10-the-night-my-vault-said-nothing-kerouac-variant.md` | drafted, voice alternative | v1 |
| Substack post 2 — "Vault said something again" (follow-up) | TBD | gated on B7 5-night verification; target 2026-05-29 | v0 |

## Warm-20 outreach log

| # | Name | Tier | Sent | Replied | Call | Notes |
|---|---|---|---|---|---|---|
| 1 | Mary | — | 2026-05-04 | yes | — | personal — girlfriend, told day-of |
| 2 | Matt | — | 2026-05-04 | yes | — | personal — high-school friend who got me in at Block; not tracked further (handled directly) |
| 3 | Larry Cermak | 1 | _pending_ | — | — | reference activation — short Telegram thank-you + ask to be a reference |
| _Tier-1 candidates from the 5/4 huddle (see contacts file): Nikita Orobenko, Mike Price, Jordan Leech (media+AI), Koray Baspinar, Claudine Daumur, Bohdan Panasenko, Edvinas Rupkus, Nikita Gulis, Nikola Pivcevic, Josh Gragg_ | | | | | | |

## Weekly Retro

### Week of 2026-05-04 (Week 1)
- **Numbers:** _fill Friday_
- **What worked:** _fill Friday_
- **What didn't:** _fill Friday_
- **Non-job-hunt win:** _fill Friday_
- **Headline goal for next week:** _fill Friday_

## Decisions log

- **2026-05-04:** Got laid off. Chose target archetype priority **AI PM > Tech PM > Creative PM**. Boston metro or remote. Will sign severance unless lawyer flags material issue.
- **2026-05-04:** Will pursue Karpathy single-top-rec — first MCP server (`intent-engineering`) as portable career artifact. Starting that work in week 2 (Phase 4 in master plan).
- **2026-05-04:** Reference clarification — the 5/4 termination meeting was delivered by Larry Cermak (President) + Vicky Lu (HR), not Alex Lebedyev. Larry is the primary professional reference. Matt is a personal friend (handled directly, not in the formal tracker).
- **2026-05-04:** 11 Block-themed skills will be **audited and sanitized in place**, not archived. Most were authored as general PM patterns with Block specifics layered in — the strip-and-keep approach preserves transferable IP for portfolio + future roles.
- **2026-05-04 (evening):** **Repo migration COMPLETE** — 13 commits on `feat/gemini-deep-research-v3.25.0` executed all 11 audit-plan steps. CHANGELOG v3.26.0 added. validate.py PASSED, agents-sdk pytest 284 passed (2 pre-existing WOL orphans), daily-driver dry-run is fully Block-clean (zero `@theblock.co`, zero `the-block` paths, 6 job-hunt + deep-work signal mentions). Path C chosen for work-operating-model (extend in place, 4th domain `job-hunt-2026`). The-block operating-model bundle archived to `vault/40_archive/operating-models-the-block-2026-05/`. Sean overrode the audit on Q5 (full time-management rewrite vs defer). See [[onwards-and-upwards-5-4-26/2026-05-04-migration-completion-handoff|migration completion handoff doc]] for the resume-here pointer.
- **2026-05-05:** **Operating-model interview COMPLETE** (CHANGELOG v3.26.2). All 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/` advanced `awaiting-interview → confirmed` via the `work-operating-model` skill. Tier-A truths locked: walk-away $100k, 5-days-in-office = no, agents draft / Sean sends, Track-C protected even in offer weeks, Friday retro is the only mandatory ritual. Relocation override clauses: Anthropic specifically OR any role $250k+/yr. **Boundary rule:** every word that hits another human's inbox is Sean's. **Extra-hour north star** = agentic-workflow + Agent Evals + enterprise build patterns. 9 open work items surfaced (Track-C cold-start, Substack voice, target-30 list, agent-fleet audit, Gmail labels pipeline, YouTube y/n, second portfolio artifact, Agent Evals fluency, enterprise-build patterns). Tone baseline = story-driven Sean Mode per `.claude/skills/writing-voice-modes/SKILL.md`.
- **2026-05-06: Decision 1 — Track-C MCP server v0 scope LOCKED.** Per [unified roadmap](onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md) §"This Week's 5 Decisions". **Default adopted:** `intent-engineering` MCP server with 3 tools (`analyze_intent_spec`, `generate_template`, `audit_existing_spec`), stdio transport, Claude Desktop demo. Repo: `~/Code/sw-mcp-intent-engineering/`. Ship target: 2026-05-25. **Switch only if** a Week-2 interview loop emerges where a different MCP demo shape is more directly relevant (e.g., a recruiter explicitly asks for a vault-knowledge or eval-router demo). Locked by Wednesday-deadline so Task 3 holds 19-day margin to ship.
- **2026-05-06: Task 0 baseline grep complete (Block IP scrub).** 30 contamination hits across 7 files in `.claude/skills/` (corrected count after Sean clarified merges + path-only grep filter). Per-file: `work-operating-model/SKILL.md` (15), `etf-page-creator/SKILL.md` (5), `api-product-management/SKILL.md` (5), `jira-automation/SKILL.md` (2), `work-operating-model/interview-questions.md` (1), `work-operating-model/artifact-templates.md` (1), `daily-driver/SKILL.md` (1). **Roadmap deviation surfaced:** the 3 named skills are not all in `.claude/skills/` — `the-block-jira-ticket-writer` was merged into `jira-automation/` (2 leaks remain), `biweekly-jira-update` was merged into `stakeholder-update/` (clean — zero leaks), `etf-page-creator` is live (5 leaks). Bonus surface: `api-product-management/SKILL.md` (5 hits, `@theblock/data-sdk` SDK examples) was NOT in the roadmap's named list. Audit detail: [2026-05-08-block-skills-audit.md](onwards-and-upwards-5-4-26/2026-05-08-block-skills-audit.md).
- **2026-05-06: Task 0 Step 2 scope LOCKED — Plan A (full clean, all 30 → 0).** Sean's call: clean every `the-block` string in `.claude/skills/` to zero, not just the IP-adjacent ones. Reasoning: CIIA §2.3 only protects Block IP (so the `work-operating-model` archive references are legally fine), but the readability layer matters more — every `the-block` string in a generic-looking skill creates recruiter-friction on a public Superuser Pack push. Trade-off accepted: `work-operating-model` loses `the-block` as a literal selectable slug (replaced with `archived-employer` placeholder); historical-interview bundle stays at `vault/40_archive/operating-models-the-block-2026-05/`. Step 2 execution = ~90 min next session per the 7-step plan in the audit doc. Verification gate: corrected grep returns zero hits.
- **2026-05-06: Task 0 Step 2 EXECUTED — commit `5a84069`.** Block-string scrub landed: 30 grep hits → 5 across 7 files in `.claude/skills/`. Live-skill identifiers (slug, SDK examples, SEO templates, email refs) all sanitized; `work-operating-model` slug renamed `the-block` → `archived-employer` consistently across SKILL.md, interview-questions.md, artifact-templates.md. The 5 residual hits are all instances of the protected physical archive path `vault/40_archive/operating-models-the-block-2026-05/` referenced from `work-operating-model/SKILL.md` (lines 12, 23, 24, 39, 85) — preservation was enforced by a repo hook denial when the path was edited, matching the inviolate rule that the path-resolution logic must continue resolving to the on-disk bundle. Verification: `python3 scripts/validate.py` → 0 errors (60 pre-existing warnings unrelated to this task). **Pre-existing bug surfaced and fixed in follow-up commit `3f3fbac`:** the path string in `work-operating-model/SKILL.md` was still `vault/40_archive/...` but the actual archive bundle lives at `vault/60_archive/operating-models-the-block-2026-05/` (per commit `07da8ca` which corrected operating-model metadata but missed SKILL.md). All 6 path references in SKILL.md now resolve correctly; verified `test -d` against the on-disk bundle. **No remote push** — local commit only, awaiting Sean's review before any public visibility.
- **2026-05-12: Task 8 Workstream A + B + Task 9 Workstream C CODE COMPLETE.** Branch `eval-suite-2026-05-12`, 32 commits, executed via `subagent-driven-development` skill. **Workstream A (14 commits, ends `783bc31`):** 10-case binary eval suite at `evals/vault-synthesizer/` with 4Q EXPLANATION.md, recruiter-readable README, open-coded log-evidence traces, failure-modes taxonomy, references + interview-vocab cheat-sheet. Pre-fix baseline 1/10 (intentionally red — 6 cases grounded in 17 days of real production logs, designed to catch the 9-day silent regression). v3.30.1 CHANGELOG entry. **Workstream B (8 commits, ends `2b9f59c`):** synthesizer patches turn 6 cases green — model_used enum (`58c23ff` vs-018), status taxonomy + per-file failure promotion (`79598f8` vs-015/016/017), Pushover boot check (`b88d56f` vs-019), daily-driver WARNING render (`6dda2d9` vs-021), skip_reason refresh (`2b9f59c` vs-012/013). Post-fix baseline: 7/10. **Workstream C (10 commits, ends `37b5fde`):** Substack-Drafter agent at `agents-sdk/agents/substack_drafter.py` (~370 lines, 33 TDD tests), Thursday-18:00 launchd plist (opt-in via `INSTALL_SUBSTACK_DRAFTER=1`), three kill-switch layers, `_route()` wired to real HybridRouter via httpx. v3.33.0 CHANGELOG entry. **vs-014 explicitly skipped** with rationale (output-completeness can't be faithfully mocked offline; deferred to live-runs). **Pushover keychain credentials added** 2026-05-12 evening via `security add-generic-password` (`com.sean.agents.pushover_user_key` + `com.sean.agents.pushover_api_token`), satisfying the new boot check. **Pending Sean-owned manual tasks:** A13 Loom recording, A14 Substack/LinkedIn publish (Friday 2026-05-22), B7 5-night live-synth gate (calendar wait, window 2026-05-17 → 2026-05-28), C9 supervised pilot drafts (3 voice modes, gated on B7).
