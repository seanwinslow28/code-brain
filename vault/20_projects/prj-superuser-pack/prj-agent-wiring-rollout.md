---
type: plan
domain:
  - claude-mastery
  - the-block
  - creative-studio
  - life-systems
status: complete
context: superuser-pack
created: 2026-04-23
updated: 2026-05-01 (Phase 2 production soak CLOSED — PARTIAL by observation gap, no regression; rollout complete across all 3 phases)
source: claude-code-plan-mode
phase-1-status: shipped 2026-04-23 (commit a081f02, v3.16.0); soak CLOSED 2026-04-27 (4/4 gates PASS)
phase-2-status: shipped 2026-04-27 (merge `19a805e`, v3.17.0); pre-flight JSON-shape guard PASS (5/5 historical transcripts × gemma4:e4b + SOUL prepend); production soak CLOSED 2026-05-01 — 5/7 gates PASS, 2/7 PARTIAL (G4 flush + G5 lint, both unexercised by soak window conditions, no regression observed; opportunistic confirmation only)
phase-3-status: closed 2026-04-27 — meeting_defender deleted; sprint_health autonomous wiring abandoned in favor of sprint-health skill
references:
  - ~/.claude/plans/please-read-through-agent-wiring-plan-pr-rustling-wreath.md
  - agent-wiring-plan-prompt.md
  - agents-sdk/AUDIT-2026-04-09-agent-downsizing.md
  - vault/05_atlas/operating-models/
  - vault/20_projects/prj-superuser-pack/prj-knowledge-loop-consumer.md
  - https://claude.ai/code/routines/trig_01Xu9fvaxMRDfSr7rwSb5fYE
---

# Agent-Wiring Rollout — Operating-Model Artifacts → Active Agent Fleet

Approved plan canonical copy. Originating plan file: `~/.claude/plans/please-read-through-agent-wiring-plan-pr-rustling-wreath.md`. Created 2026-04-23 in Plan Mode; Phase 1 shipped same day as commit `a081f02`. This vault copy is the in-project reference; the original ~/.claude/plans file is the immutable approval record.

**Scope:** Wire the 15 `status: confirmed` operating-model artifacts (HEARTBEAT/USER/SOUL/operating-model/schedule-recommendations × 3 domains) into the 6 active SDK agents, as promised in the `v3.15.0` Known Follow-ups list.

---

## Context (why this is happening now)

- `v3.15.0` (2026-04-18) landed the 3-domain restructure and scaffolded placeholder paths.
- The 5-layer interviews closed clean — all 15 artifacts `status: confirmed` as of 2026-04-22.
- The `CHANGELOG.md v3.15.0` entry explicitly flags "Wiring… into active agents… is a future task."
- The producer side of the knowledge loop (`flush.py` → `vault_synthesizer.py` → `knowledge_lint.py`) is already live. This plan is the downstream consumer side.
- The $0.25 → $0.50 daily-driver budget bump in `v3.12.2` was an expensive lesson; any plan that meaningfully raises tokens needs an explicit cap review.

---

## Section 1 — Executive Summary

Three phases, each independently shippable, reversible, and gated. Default loading pattern is **on-demand Read** with a tiny stub in the system prompt pointing to artifact paths (Claude-Skills-style progressive disclosure). Only `HEARTBEAT.md` files are small enough to justify system-prompt injection, and only where always relevant.

- **Phase 1 (Wedge):** `daily_driver.py` morning mode loads 3 × `HEARTBEAT.md` into the preamble; exposes on-demand reads for other artifacts via a new loader. **SHIPPED 2026-04-23.**
- **Phase 2 (Fleet consumers):** `meta_agent.py` consults `schedule-recommendations.md`; `flush.py` and `knowledge_lint.py` consult `SOUL.md` — all reads go into **local-model prompts** (phi4-mini / Qwen3-14B), zero cloud egress.
- **Phase 3 (Closed 2026-04-27):** wiring spec abandoned. `meeting_defender` was deleted entirely (Daily Driver already covers the calendar surfacing; the auto-decline workflow had no demand). `sprint_health` autonomous wiring superseded by the `sprint-health` skill — same value delivered as an interactive Block Jira status check, no MCP-in-headless gymnastics needed.

After each phase: daily-driver keeps its 8:45 AM launchd slot, 30-turn max, `<!-- agent-error -->` anchor, vault-health header. Phase 6 producer loop untouched. None of the 6 disabled agents re-enabled.

---

## Section 2 — Shared Artifact Loader (`agents-sdk/lib/artifact_loader.py`)

**Status: shipped 2026-04-23 (commit a081f02).**

New module, ~150 lines, mirrors the convention in `lib/skill_loader.py`: plain module-level functions, frontmatter stripped with a regex, pathlib, explicit `FileNotFoundError` semantics.

### 2.1 Public API

```python
# Domain = "the-block" | "creative-studio" | "life-systems"
# Kind   = "HEARTBEAT" | "USER" | "SOUL" | "operating-model" | "schedule-recommendations"

def load_artifact(
    domain: str,
    kind: str,
    vault_root: Path,
    *,
    strip_frontmatter: bool = True,
    require_confirmed: bool = True,
) -> str | None: ...

def load_heartbeats(vault_root: Path) -> dict[str, str | None]:
    """Returns {"the-block": ..., "creative-studio": ..., "life-systems": ...}.
    Missing files map to None and are logged, never raised."""

def artifact_path(domain: str, kind: str, vault_root: Path) -> Path: ...

def clear_cache() -> None: ...  # for tests and long-lived processes
```

### 2.2 Caching

Module-level `dict[(domain, kind, mtime_ns), str]` keyed on `(domain, kind, file_mtime_ns)`. Reads re-hit the file only if mtime changes — safe across a single agent run, auto-invalidates if Sean edits an artifact between runs. No LRU, no TTL; the working set is 15 files.

### 2.3 Missing-file / malformed-frontmatter handling

- Missing file → return `None`, log `WARNING artifact_missing`, never raise.
- Unreadable frontmatter → log warning, return body as-is.
- `require_confirmed=True` and `status != "confirmed"` → log `INFO artifact_not_confirmed` and return `None`. Default is strict so half-populated artifacts don't leak into agent context.

### 2.4 Config additions to `agents-sdk/config.toml`

```toml
[artifacts]
enabled = true                                  # global kill-switch
vault_subpath = "05_atlas/operating-models"
cache_mtime_check = true
require_confirmed = true

[artifacts.per_agent]
daily_driver = { heartbeats = true, on_demand = ["USER", "SOUL", "operating-model", "schedule-recommendations"] }
# Phase 2 (commented placeholders):
# meta_agent = { on_demand = ["schedule-recommendations"] }
# flush = { on_demand = ["SOUL"] }
# knowledge_lint = { on_demand = ["SOUL"] }
```

Global kill-switch `[artifacts].enabled = false` is an instant rollback for all phases.

### 2.5 Tests

- `agents-sdk/tests/test_artifact_loader.py` — 15 tests (path composition, frontmatter stripping, missing-file graceful degradation, status-confirmed filtering, mtime cache invalidation, all-three-domains convenience).
- `agents-sdk/tests/conftest.py` — new `tmp_artifacts` fixture.

---

## Section 3 — Phase 1: Daily-Driver Morning Mode (the Wedge) — SHIPPED

**Shipped 2026-04-23 as commit a081f02. v3.16.0 release.**

### 3.1 Files modified (final tally)

| Path | Change | Lines |
|---|---|---|
| `agents-sdk/lib/artifact_loader.py` | New module | ~140 |
| `agents-sdk/agents/daily_driver.py` | `build_artifact_preamble()`; called from `build_preamble()` morning branch | +75 |
| `agents-sdk/lib/config.py` | `Config.artifacts` field + `artifact_config()` helper | +13 |
| `agents-sdk/config.toml` | `[artifacts]` section; morning cap 0.50 → 0.60 | +24 |
| `agents-sdk/tests/conftest.py` | `tmp_artifacts` fixture | +50 |
| `agents-sdk/tests/test_artifact_loader.py` | New | ~150 |
| `agents-sdk/tests/test_daily_driver_artifacts.py` | New | ~150 |
| `CHANGELOG.md`, `CLAUDE.md`, `README.md` | v3.16.0 doc updates | small |

### 3.2 Where the hook lands

At `daily_driver.py` `build_preamble()` morning branch:

```python
if mode == "morning":
    base += "\n" + vault_health_summary(config.vault_root) + "\n"
    artifact_block = build_artifact_preamble(config)   # NEW
    if artifact_block:
        base += "\n" + artifact_block + "\n"
```

`build_artifact_preamble(config)` returns `""` when `[artifacts].enabled = false` or no per-agent entry — silent no-op rollback.

### 3.3 System-prompt stub (rendered in dry-run)

Two blocks injected:
1. **Always-on HEARTBEATs** — bodies of all 3 domain HEARTBEATs.
2. **On-demand pointer** — Read-tool paths for the 4 other kinds × 3 domains.
3. **Tone rule** — calm/factual/zen, no scolding, no imperatives at the reader.
4. **Capture-and-defer default** — new ideas to inbox; do not promise to act on them today.

### 3.4 life-systems `USER.md` — DECISION LOCKED 2026-04-23

**Load as-is.** Daily-driver reads `vault/05_atlas/operating-models/life-systems/USER.md` on-demand from the cloud path. Non-negotiable #7 waived for this artifact × agent pair; SOUL.md (life-systems + the-block) stays local-only via Phase 2 agents. Sean accepts the cloud-egress footprint for richer morning prioritization.

### 3.5 Token budget delta (morning run, worst case)

| Source | Always-on tokens | Peak tokens |
|---|---|---|
| HEARTBEATs × 3 (loaded + framing) | +450 | +450 |
| On-demand pointer block | +150 | +150 |
| Tone/capture rule block | +80 | +80 |
| One-shot on-demand reads (USER + SOUL + schedule-recs) | 0 | +3,100 |
| **Per-turn preamble delta** | **+680** | **+680** |
| **One-shot delta (across run)** | 0 | **+3,100** |

Current morning cost: ~$0.40/run. New worst case: ~$0.44/run. **Cap bumped 0.50 → 0.60** for ~50% headroom (matching v3.12.2 pattern).

### 3.6 Gate checks

| # | Gate | Status |
|---|---|---|
| 1 | `pytest agents-sdk/tests/test_artifact_loader.py` green | PASS (15/15) |
| 2 | `pytest agents-sdk/tests/test_daily_driver_artifacts.py` green | PASS (10/10) |
| 3 | Full pytest suite stays green | PASS (134/134) |
| 4 | `python3 scripts/validate.py` passes | PASS |
| 5 | Dry-run shows new preamble block correctly | PASS |
| 6 | Three consecutive live morning runs (2026-04-24, -25, -26) clean | **In progress** — soak running |
| 7 | Sean confirms tone calm/factual/zen | Pending Monday review |

**Soak review scheduled:** Mon 2026-04-27 09:30 EDT — remote review at https://claude.ai/code/routines/trig_01Xu9fvaxMRDfSr7rwSb5fYE.

### 3.7 Rollback procedure

1. **Instant:** `[artifacts].enabled = false` in `config.toml`. Next morning matches pre-Phase-1 behavior.
2. **Config-level:** drop `daily_driver` from `[artifacts.per_agent]`. Loader stays available for Phase 2/3.
3. **Code-level:** revert commit `a081f02`.

---

## Section 4 — Phase 2: Fleet Consumers (`meta_agent`, `flush`, `knowledge_lint`) — NOT STARTED

**Critical architectural note:** none of these three agents use the Claude Agent SDK `query()` — they all call **local Ollama** via `httpx` or `lib/hybrid_router.py`. So:

- Zero cloud egress of life-systems SOUL.md content.
- No "system prompt" in the SDK sense — artifact text concatenated into the user-prompt template sent to phi4-mini / Qwen3-14B.
- Budget cap stays $0.00 (local). Only context-window pressure matters.

### 4.1 `meta_agent.py` — reads `schedule-recommendations.md` × 3 domains

**Purpose:** rank automation recommendations against Sean's Protect / Automate / Decline lists per domain. Today the meta-agent has no domain awareness.

**Change:** at the summary-generation step (around the phi4-mini-reasoning prompt build), add a context block from `load_artifact(domain, "schedule-recommendations", ...)` for the 3 domains. Loaded lazily.

### 4.2 `flush.py` — consults `SOUL.md` when tagging memory entries

**Purpose:** SessionEnd flush extracts decisions/lessons/actions/patterns/quotes. With SOUL context, model can map a new entry against known Tier-A items and write richer tags.

**Change:** in `EXTRACTION_PROMPT` build at `flush.py:60-79`, pre-prepend a SOUL context section that **always loads all three domain SOULs** (Q3 decision 2026-04-23). Total context addition: ~5K tokens, well within phi4-mini-reasoning (32K) and Qwen3-14B (40K+) windows. No domain-inference helper.

**Safety clause:** Tier-A contradictions get flagged as a new `patterns` entry — flush is additive-only.

### 4.3 `knowledge_lint.py` — consults `SOUL.md` to flag Tier-A conflicts

**Purpose:** when knowledge-lint proposes a new entry (Tier 2 semantic scan) flag any candidate that conflicts with a Tier-A SOUL item.

**Change:** Tier 2 prompt gains per-domain SOUL context. New `LintIssue` kind `soul-tier-a-conflict` at severity `HIGH`.

### 4.4 Files modified — Phase 2

| Path | Change |
|---|---|
| `agents-sdk/agents/meta_agent.py` | `build_schedule_recs_context()`; inject before summary-prompt build |
| `agents-sdk/agents/flush.py` | Prepend all-three-SOULs block to EXTRACTION_PROMPT |
| `agents-sdk/agents/knowledge_lint.py` | Tier-2 prompt + new issue kind `soul-tier-a-conflict` |
| `agents-sdk/config.toml` | Uncomment Phase 2 entries in `[artifacts.per_agent]` |
| `agents-sdk/tests/test_meta_agent_artifacts.py` | New, ~60 lines |
| `agents-sdk/tests/test_flush.py` | Extend, +~40 lines |
| `agents-sdk/tests/test_knowledge_lint.py` | Extend, +~50 lines |
| CHANGELOG / CLAUDE.md / README.md | Doc updates |

### 4.5 Gate checks — Phase 2

1. Phase 1 has been live ≥ 3 consecutive mornings without rollback.
2. All new/extended tests green.
3. One `flush` run on a session touching `the-block/**` emits tags referencing Ed / Matt / critical-path correctly.
4. One `knowledge_lint --full` Sunday run completes in ≤ 20 min on Mac Mini alone.
5. No regression in producer-side Phase 6 loop.

### 4.6 Rollback

Per-agent: remove the agent's entry from `[artifacts.per_agent]`. Same instant-kill via `[artifacts].enabled = false`.

---

## Section 5 — Phase 3: Closed 2026-04-27

**Phase 3 is no longer a wiring task.** After re-evaluating both agents against the post-v3.17.0 reality (Daily Driver already surfaces calendar context; operating-model artifacts now flow through the live agent fleet; browser-OAuth MCP in headless mode is still the binding constraint), the autonomous-agent shape is the wrong shape for both. Decisions locked 2026-04-27:

### 5.1 `meeting_defender` — DELETED

Removed completely from the repo. Daily Driver morning mode already lists the day's meetings via interactive MCP, and there's no Sean-side demand for an auto-decline / draft-Slack-DM workflow.

| Action | Path |
|---|---|
| Delete agent | `agents-sdk/agents/meeting_defender.py` |
| Delete schedule | `agents-sdk/schedules/com.sean.agent.meeting-defender.plist` |
| Remove config block | `[agents.meeting_defender]` in `agents-sdk/config.toml` |
| Update audit | `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md` left unchanged — historical record stands |

The autonomous SDK agent count drops from **13 → 12** (still 6 active).

### 5.2 `sprint_health` — superseded by `sprint-health` skill

The valuable shape isn't a Friday-3PM autonomous report — it's an ad-hoc "where are we on Epic X?" status check, which Sean's own `the-block/schedule-recommendations.md` flagged as a gap ("No `sprint-health` skill yet"). Built as a skill instead.

| Action | Path |
|---|---|
| New skill | `.claude/skills/sprint-health/SKILL.md` |
| Block-specific | Reuses `jira-automation` Block Jira config (PRO / RBS / BE / Cloud ID `9660d87e-…`) |
| Triggers | "where are we on PRO-XXXX", "sprint health", "what's stuck", "anything stale" |
| Read-only | Atlassian MCP read tools only; never auto-comments / auto-transitions |
| Cadence fit | Pre-standup, pre-1:1 with Ed, pre-bi-weekly P&E, ad-hoc Epic / Story spot-checks |

The skill picks up operating-model artifacts via the standard Read pattern when invoked interactively (the user already has the artifact-loader-injected pointers from Daily Driver morning), so no new artifact wiring is required.

The dormant `agents-sdk/agents/sprint_health.py` and `com.sean.agent.sprint-health.plist` remain in the repo as `enabled = false` artifacts. They're not loaded into launchd, never produced output even when enabled (per the 2026-04-09 audit), and add no maintenance cost. Future cleanup is one git rm away if desired.

### 5.3 What stays out of Phase 3

`process_inbox`, `daily_driver evening/weekly`, `pr_digest`, `preserve_session`, `spending_analysis`, `health_audit`, `md_to_anki` — disabled for unrelated reasons per the 2026-04-09 audit; not in scope here.

---

## Section 6 — Doc updates required per phase

### Phase 1 (DONE)

- ✅ `CHANGELOG.md` v3.16.0 entry
- ✅ `CLAUDE.md` daily-driver row + lib/ comment + operating-model paragraph
- ✅ `README.md` daily-driver row + safety line

### Phase 2

- `CHANGELOG.md`: `Added: meta-agent / flush / knowledge-lint consume operating-model artifacts for domain-aware output`.
- `CLAUDE.md`: update three affected agent rows with `+ SOUL / schedule-recs context` marker.
- `README.md`: no-op expected.

### Phase 3 (Closed 2026-04-27)

- `CHANGELOG.md`: entry under v3.17.x — meeting_defender deleted, sprint-health skill added, Phase 3 wiring closed.
- `CLAUDE.md`: skill count 113 → 114; autonomous SDK agent count 13 → 12; Phase 3 line in the operating-model wiring paragraph updated to reflect closure.
- `README.md`: same skill / agent count updates.

---

## Section 7 — Rejected alternatives

1. **Dump all 15 artifacts into every agent's system prompt.** Rejected: ~4,320 tokens × every turn × 6 agents is expensive on cloud, wasteful on local, breaks progressive-disclosure decision, kills prompt cache hit rate.
2. **Pre-derive single `context.md` per domain.** Rejected: creates a second source of truth that goes stale relative to authored artifacts.
3. **MCP-backed file serving.** Rejected: SDK agents cannot access MCP. Filesystem reads are the only viable transport.
4. **In-memory cache shared across processes (Redis / file cache).** Rejected: each agent runs as a short-lived subprocess; per-process dict cache is sufficient.
5. **Embed artifact text as an SDK "additional skill" via `skill_loader.py`.** Rejected: artifacts aren't skills; they're user-data context.

---

## Section 8 — Risks and mitigations

| # | Risk | Likelihood | Blast radius | Mitigation | Rollback |
|---|---|---|---|---|---|
| 1 | Morning-run budget exceeds new $0.60 cap | Low | Single missed morning note | Cap alert on `cost_usd ≥ 0.55`; review after 3 runs | `[artifacts].enabled=false` |
| 2 | Cloud-egress of life-systems USER.md content | Resolved 2026-04-23 — Sean chose "Load as-is" | Personal finance patterns reach Anthropic infra | Accepted trade-off; SOUL.md stays local-only via Phase 2 | Remove `USER` from `daily_driver.on_demand` list |
| 3 | Malformed artifact frontmatter breaks preamble | Low | Morning run hard-fails before SDK call | Loader returns raw body on parse error + logs WARNING | `[artifacts].enabled=false` |
| 4 | `status: draft` artifact accidentally included | Low | Agent acts on unconfirmed data | `require_confirmed=True` default; unit test | Per-agent config entry removed |
| 5 | Phase 6 flush loop regresses (extra SOUL context destabilizes phi4-mini JSON output) | Medium | SessionEnd summaries become invalid JSON | Before-Phase-2 guard: diff flush output with/without SOUL against 5 historical transcripts | Remove `flush` from `[artifacts.per_agent]` |
| 6 | Knowledge-lint Sunday run blows past 20-min budget | Medium | Lint report delayed | Cap SOUL-context at HIGH severity checks only | Remove `knowledge_lint` from per-agent |
| 7 | Sean edits artifact mid-run; cached stale content | Very Low | One run reads stale file | mtime-keyed cache catches on next access | None needed; auto-recovers |
| 8 | `scripts/validate.py` breaks on `lib/artifact_loader.py` | Very Low | CI/local validation fail | Validate in Phase 1 gate check | Revert commit |
| 9 | Tone drift — agent output reads as scolding despite rule | Medium | Low-trust daily notes | Tone assertion in tests grep forbidden phrases | Remove tone rule; keep structural context |
| 10 | Scope creep into re-enabling disabled agents | Low | Violates non-negotiable #9 | Phase 3 closed 2026-04-27 — meeting_defender deleted, sprint_health re-shaped as skill; audit file remains the canonical "do not re-enable" record | None — re-enablement of any other disabled agent is out of scope |

---

## Section 9 — Decisions locked (2026-04-23)

### Q1 — life-systems `USER.md` in daily-driver

**Decision: Load as-is.** Daily-driver reads life-systems USER.md on-demand from the cloud path. Non-negotiable #7 waived for this artifact × agent pair; SOUL.md stays local-only via Phase 2 agents.

### Q2 — daily-driver `max_budget_usd` bump

**Decision: Bump 0.50 → 0.60.** Applied to morning mode only. Evening/weekly stay disabled per audit.

### Q3 — Phase 2 SOUL loading in flush

**Decision: Always load all three.** Every flush run prepends the-block + creative-studio + life-systems SOUL context. Simpler than domain inference; ~5K tokens fits both local model windows.

### Q4 — Phase 3 disposition (revised 2026-04-27)

**Decision: Phase 3 closed.** `meeting_defender` deleted; Daily Driver morning already covers the calendar surfacing and the auto-decline / draft-Slack-DM workflow had no demand. `sprint_health` reshaped as the `sprint-health` skill — same value as an ad-hoc "where are we on Epic X?" interactive query. No autonomous Phase 3 work pending. The original 2026-04-23 "frozen indefinitely" framing is superseded.

---

## Section 10 — Execution order + estimated effort

### Phase 1 — DONE 2026-04-23 (~4 hr)

| Step | Estimated | Actual |
|---|---|---|
| Write `artifact_loader.py` + tests | 1.5-2 hr | ~1 hr |
| Update `daily_driver.py` `build_preamble` | 30 min | ~20 min |
| Update `config.toml` | 15 min | ~10 min |
| Write `test_daily_driver_artifacts.py` | 1 hr | ~45 min |
| Pytest + validate | 5 min | 5 min |
| Dry-run | 5 min | 5 min |
| Doc updates | 30 min | ~20 min |
| Commit + push (+ rebase on b42576e) | — | ~10 min |

### Phase 2 — gated on Phase 1 soak (~4.5 hr dev + 1 week soak)

| Step | Effort |
|---|---|
| `meta_agent.py` change | 45 min |
| `flush.py` change (all-three SOULs) | 45 min |
| `knowledge_lint.py` Tier-2 + new issue kind | 1 hr |
| Extend existing tests | 1.5 hr |
| Local-model regression soak | 1 week observation, no dev time |
| Doc updates | 20 min |

### Phase 3 — Closed 2026-04-27 (~1 hr)

| Step | Effort |
|---|---|
| Delete `meeting_defender.py` + plist + config block | 5 min |
| Write `.claude/skills/sprint-health/SKILL.md` | 30 min |
| Update Section 5 + frontmatter + risk row + Q4 decision | 15 min |
| CHANGELOG / CLAUDE.md / README.md count + line updates | 10 min |
| `python3 scripts/validate.py` | 1 min |

---

## Live status — updated 2026-05-01

- **Phase 1:** shipped 2026-04-23 as commit `a081f02` (v3.16.0). Soak CLOSED 2026-04-27 — all 4 gates PASS.
- **Phase 2:** shipped 2026-04-27 as merge `19a805e` (v3.17.0). **Production soak CLOSED 2026-05-01 — 5/7 gates PASS, 2/7 PARTIAL by observation gap (no regression observed).** Soak conclusion: do not block. The two PARTIAL gates (G4 flush SOUL prepend, G5 Sunday knowledge_lint) failed only because production conditions during the 4-day window did not exercise those code paths — flush hit the recursion guard on all 21 invocations (sessions had no extractable content), and the next scheduled `knowledge_lint --full` run fell outside the window. Pre-flight JSON guard already validated the SOUL prepend against 5 historical transcripts at ship time. Domain-Aware Insights output: 4/4 days populated, 0 fallbacks, output cross-references real Protect/Automate/Decline items by name. Full review: [phase-2-soak-closeout-2026-05-01.md](phase-2-soak-closeout-2026-05-01.md). Rollout complete.
- **Phase 3:** closed 2026-04-27. `meeting_defender` deleted; `sprint_health` re-shaped as the `sprint-health` skill. See Section 5.

### Soak observation log

| Date | Morning run | cost_usd | turns | agent-error count | Tone hits | Notes |
|---|---|---|---|---|---|---|
| 2026-04-24 (Fri) | success | **$0.4502** | 10 | 0 | 0 | Big Thing = weekly sweep (matches the-block HEARTBEAT "Fri lighter day"); creative deep work deferred to weekend |
| 2026-04-25 (Sat) | success | **$0.4681** | 9 | 0 | 0 | Big Thing = Pencil Test pipeline (matches creative-studio HEARTBEAT "Weekends = implementation mode") |
| 2026-04-26 (Sun) | success | **$0.4248** | 8 | 0 | 0 | Big Thing = Pencil Test continues |
| 2026-04-27 (Mon) | success | **$0.4169** | 9 | 0 | 0 | Block deep work in 10:30–14:00 (HEARTBEAT deep-work block); Pencil Test parked in "weekday = research only" lot — direct lift of creative-studio HEARTBEAT weekday rule. References CEO transition (5/1) from the-block HEARTBEAT Monthly/Quarterly section |

### Phase 1 closeout — gate check (2026-04-27)

| Gate | Status | Evidence |
|---|---|---|
| G1. cost_usd < $0.50/run | **PASS (4/4)** | $0.4502 / $0.4681 / $0.4248 / $0.4169. Mean $0.4400, max $0.4681. None approached the $0.60 cap. Delta vs. baseline ~$0.40 = +~10% per run, matching the Section 3.5 estimate of +$0.02–$0.06. |
| G2. zero agent-error entries | **PASS** | Zero `<!-- agent-error -->` anchors across all 4 daily notes. All 4 morning runs `success` in `agent-run-history.csv`. Zero error/exception/traceback hits in the four `daily-driver-2026-04-2{4,5,6,7}-morning.log` files. |
| G3. sacred-block awareness | **PASS — strong** | Friday weekly-sweep, weekend Pencil Test, weekday Block-deep-work, no 21:00+ commitments, nothing in 14:00–15:00 decompress. Monday note cites HEARTBEAT verbatim ("weekday = research mode only, not implementation") and surfaces the CEO transition from the Monthly/Quarterly section. Small-things list explicitly references "Monday ritual per HEARTBEAT". |
| G4. tone calm/factual/zen | **PASS** | Zero hits for "you should" / "you need to" / "make sure to" / "don't forget" / "you missed" / "you haven't" across all 4 notes. Carry-over discipline (12 → 13 → 14 → 15 iterations of the same descope task) is framed as factual auto-descope threshold logic, never scolding. |

**Recommendation:** All four gates PASS. Phase 1 soak clean. Operating-model context is doing real work in morning runs — agent reaches into HEARTBEATs, schedule rules, and Monthly/Quarterly facts to rank priorities. Safe to proceed to Phase 2.

Remote-review trigger fired 2026-04-27 13:30 UTC and auto-disabled (`run_once_fired`). Routine: https://claude.ai/code/routines/trig_01Xu9fvaxMRDfSr7rwSb5fYE.

### Carry-over signals worth flagging (not gating)

- The animated-short descope task hit its 15th carry-over on 2026-04-27. The agent's framing is correct (factual + auto-descope threshold language), but the underlying item really should be closed manually or excluded from the carry-over scan. This is **task-list hygiene**, not a Phase 1 defect.
- Daily notes show consistent `[DEFERRED] MCP unavailable in headless mode` messaging — matches the documented headless limitation. No regression.

---

## Rollout complete — 2026-05-01

All three phases shipped or closed. Phase 1 soak closed 2026-04-27 (4/4 PASS). Phase 2 soak closed 2026-05-01 (5/7 PASS, 2/7 PARTIAL by observation gap, no regression). Phase 3 closed 2026-04-27 — `meeting_defender` deleted, `sprint-health` skill replaces the autonomous wiring. Plan status flipped `in-progress` → `complete` 2026-05-01.

Opportunistic post-close confirmation (not gating, do not block on these):
- **G4** (flush SOUL prepend in production): the next non-trivial Claude Code session that produces a real flush extraction will exercise the SOUL prepend on a fresh transcript. Rollback path stays `[artifacts.per_agent.flush] = {}` if anything looks off.
- **G5** (Sunday `knowledge_lint --full` run): 2026-05-03 22:00 ET fires the first post-soak Sunday lint pass with the `soul-tier-a-conflict` issue kind active.

---

## Coordination with `prj-knowledge-loop-consumer.md` (added 2026-04-25)

This plan and `prj-knowledge-loop-consumer.md` operate on the **same agentic workflow** and modify overlapping files (`flush.py`, `knowledge_lint.py`, `daily_driver.py`, `config.toml`). Future agents must respect the merge order below — running these plans out of sequence will produce avoidable rebase conflicts and may invalidate the Phase 1 soak signal.

### Merge order (canonical)

1. **Agent-wiring Phase 1** — SHIPPED 2026-04-23 (commit `a081f02`). Currently in soak through 2026-04-27 09:30 EDT.
2. **Knowledge-loop Phase A + Phase B** — develop now in parallel branches `knowledge-loop/phase-a` and `knowledge-loop/phase-b` (created 2026-04-25). Zero conflict with the soak — neither phase touches `daily_driver.py` morning path or `artifact_loader.py`. Hold merges until Phase 2 ships.
3. **Agent-wiring Phase 2** — ships after soak clears. Modifies `flush.py` (EXTRACTION_PROMPT prepend) + `knowledge_lint.py` (Tier 2 SOUL context + new `soul-tier-a-conflict` issue kind) + `meta_agent.py` (schedule-recs).
4. **Knowledge-loop Phase C** — after Phase 2 lands. Adds `query.py` + qa/ tier; light extensions to `vault_synthesizer.py` and `knowledge_lint.py`.
5. **Knowledge-loop Phase D** — after Phase C lands. Highest-conflict phase: it modifies `daily_driver.py` morning brief Vault Health section AND is the third change to `knowledge_lint.py`. Single-session feasible but rebase deliberately.

### Two file-conflict watch points

- **`flush.py`** — agent-wiring Phase 2 prepends a SOUL block to `EXTRACTION_PROMPT` (around `flush.py:60-79`). Knowledge-loop Phase A adds a `--trigger {session-end,pre-compact,manual}` argparse arg and threads it into the daily-log tag field. Both are additive to different sections of the file; whichever ships second rebases cleanly.
- **`knowledge_lint.py`** — touched **three times** across the two plans (Phase 2 → C → D). Land in that exact order. Each adds a distinct concern (Phase 2: SOUL Tier-A conflict kind. C: qa/ in orphan/stale/sparse checks. D: SQL fast-path against `concept_edges`). No pair overlaps semantically, but order matters because each rebases onto the prior.

### Soak-safety rule

Anything that modifies `agents-sdk/agents/daily_driver.py` morning path or `agents-sdk/lib/artifact_loader.py` invalidates the active Phase 1 soak. **Do not merge knowledge-loop Phase D until Phase 2 has shipped and Phase 1 soak is closed.**
