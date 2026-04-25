---
type: plan
domain:
  - claude-mastery
  - the-block
  - creative-studio
  - life-systems
status: in-progress
context: superuser-pack
created: 2026-04-23
updated: 2026-04-25
source: claude-code-plan-mode
phase-1-status: shipped 2026-04-23 (commit a081f02, v3.16.0)
phase-2-status: not-started (gated on Phase 1 soak clean 2026-04-27)
phase-3-status: spec-only (frozen — re-enablement requires explicit approval)
references:
  - ~/.claude/plans/please-read-through-agent-wiring-plan-pr-rustling-wreath.md
  - agent-wiring-plan-prompt.md
  - agents-sdk/AUDIT-2026-04-09-agent-downsizing.md
  - vault/05_atlas/operating-models/
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
- **Phase 3 (Specified, frozen):** wiring spec for `meeting_defender` and `sprint_health` written but **not enabled**. Stays dormant until explicit approval.

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

## Section 5 — Phase 3: Specified, Frozen (`meeting_defender`, `sprint_health`)

**Wiring spec only. Neither agent re-enabled as part of this plan.**

### 5.1 `meeting_defender` (the-block)

- **Primary context:** `the-block/HEARTBEAT.md` + `the-block/schedule-recommendations.md`.
- **Loading:** system-prompt-loaded HEARTBEAT; on-demand schedule-recs.
- **Activation trigger when re-enabled:** `[artifacts.per_agent.meeting_defender] = { heartbeats = ["the-block"], on_demand = ["schedule-recommendations"] }`.

### 5.2 `sprint_health` (the-block)

- **Primary context:** `the-block/USER.md` + `the-block/schedule-recommendations.md`.
- **Loading:** both on-demand.

### 5.3 What stays out of Phase 3

`process_inbox`, `daily_driver evening/weekly`, `pr_digest`, `preserve_session`, `spending_analysis`, `health_audit`, `md_to_anki` — disabled for unrelated reasons.

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

### Phase 3 (only once activated — not now)

- Zero doc updates as part of this plan.

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
| 10 | Scope creep into re-enabling disabled agents | Low | Violates non-negotiable #9 | Phase 3 labeled "spec only"; audit file re-read at any activation | None — plan explicitly freezes Phase 3 |

---

## Section 9 — Decisions locked (2026-04-23)

### Q1 — life-systems `USER.md` in daily-driver

**Decision: Load as-is.** Daily-driver reads life-systems USER.md on-demand from the cloud path. Non-negotiable #7 waived for this artifact × agent pair; SOUL.md stays local-only via Phase 2 agents.

### Q2 — daily-driver `max_budget_usd` bump

**Decision: Bump 0.50 → 0.60.** Applied to morning mode only. Evening/weekly stay disabled per audit.

### Q3 — Phase 2 SOUL loading in flush

**Decision: Always load all three.** Every flush run prepends the-block + creative-studio + life-systems SOUL context. Simpler than domain inference; ~5K tokens fits both local model windows.

### Q4 — Phase 3 freeze timing

Frozen indefinitely. Sean activates `meeting_defender` or `sprint_health` in a separate session when ready.

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

### Phase 3

**0 hours.** Spec-only. Activation is a separate, explicit decision.

---

## Live status — updated 2026-04-25

- **Phase 1:** shipped 2026-04-23 as commit `a081f02` (v3.16.0). All 5 deterministic gates PASS; soak gate in progress (4 morning runs scheduled 2026-04-24 → 2026-04-27).
- **Phase 2:** held until soak review clears.
- **Phase 3:** frozen; no work scheduled.

### Soak observation log

| Date | Morning run | cost_usd | agent-error count | Tone notes |
|---|---|---|---|---|
| 2026-04-24 | TBD | TBD | TBD | TBD |
| 2026-04-25 | TBD | TBD | TBD | TBD |
| 2026-04-26 | TBD | TBD | TBD | TBD |
| 2026-04-27 | (review fires 09:30 EDT) | — | — | — |

Fill in cost / error / tone columns as each morning's daily note + agent-logs surface. Remote review automated at https://claude.ai/code/routines/trig_01Xu9fvaxMRDfSr7rwSb5fYE.

---

## No blockers remaining

All three blocking decisions resolved 2026-04-23 (Section 9). Phase 1 shipped same day. Phase 2 ready to dev whenever soak gate clears.
