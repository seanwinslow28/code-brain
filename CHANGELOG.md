# Changelog

All notable changes to the Claude Code Superuser Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.16.0] - 2026-04-23

Phase 1 of the agent-wiring rollout — the `v3.15.0` Known Follow-up for wiring operating-model artifacts into the active agent fleet is now underway. This release wires `daily-driver` morning mode; `meta_agent` / `flush` / `knowledge_lint` arrive in Phase 2; `meeting_defender` / `sprint_health` remain frozen per the 2026-04-09 audit.

### Added

- `agents-sdk/lib/artifact_loader.py` — new module (~150 lines). `load_artifact(domain, kind, vault_root, *, strip_frontmatter, require_confirmed)` and `load_heartbeats(vault_root)` read operating-model artifacts from `vault/05_atlas/operating-models/{domain}/{kind}.md`, strip YAML frontmatter, and return `None` on missing / unconfirmed / unreadable files rather than raising. Module-level cache keyed on `(domain, kind, file_mtime_ns)` — a single agent run never re-reads the same artifact, and any edit between runs auto-invalidates. Mirrors the conventions in `lib/skill_loader.py`.
- `agents-sdk/tests/test_artifact_loader.py` — 15 tests covering happy-path reads, frontmatter stripping, missing-file graceful degradation, `status: draft` filtering, mtime-invalidated cache, and the `load_heartbeats()` convenience.
- `agents-sdk/tests/test_daily_driver_artifacts.py` — 10 tests covering `build_artifact_preamble()` content, global + per-agent toggles, morning-mode integration with `build_preamble()`, and a tone-guard that scans the preamble for forbidden scolding phrases (Risk #9 from the plan).
- `agents-sdk/tests/conftest.py` — new `tmp_artifacts` fixture. Builds a 3-domain × 5-kind temp vault with `status: confirmed` frontmatter for loader and daily-driver artifact tests.
- `agents-sdk/agents/daily_driver.py` — `build_artifact_preamble(config)` helper. Emits three sections: all-three HEARTBEATs (always-on), on-demand Read-tool pointer paths for the remaining four kinds × three domains, and the life-systems tone + capture-and-defer rules. Called from `build_preamble()` inside the existing morning-only branch — evening and weekly modes are unaffected.

### Changed

- `agents-sdk/config.toml` — new `[artifacts]` section with a global `enabled = true` kill-switch and a `[artifacts.per_agent]` block. `daily_driver` wired to load HEARTBEATs + list `USER / SOUL / operating-model / schedule-recommendations` as on-demand Read targets. Phase 2 entries for `meta_agent` / `flush` / `knowledge_lint` scaffolded as commented placeholders.
- `agents-sdk/config.toml` — `[agents.daily_driver.modes.morning].max_budget_usd` bumped from `0.50` → `0.60`. Phase 1 adds ~+680 always-on / ~+3,100 worst-case one-shot tokens per morning run; estimated new worst case is ~$0.44 / run, cap lifted for ~50% headroom matching the v3.12.2 pattern.
- `agents-sdk/lib/config.py` — `Config` gains an `artifacts: dict` field populated from `raw.get("artifacts", {})`, plus a `config.artifact_config(agent_name)` helper that returns the per-agent dict (or `{}` when artifacts are globally disabled or the agent has no entry).

### Decisions locked 2026-04-23 (from the rollout plan)

- **life-systems `USER.md` is cloud-readable by daily-driver.** Non-negotiable #7 (no cloud egress of life-systems personal data) is waived for this specific artifact × agent pair; SOUL.md stays local-only via Phase 2 agents. Trade-off accepted for richer morning prioritization.
- **Morning cap $0.50 → $0.60.** Rollback path: flip `[artifacts].enabled = false`, which makes `build_artifact_preamble()` return `""` and the run falls back under $0.50.
- **Phase 2 flush will always load all three SOULs** (no domain-inference helper). Phase 2 not shipped in this release.

### Gate-check status

| Gate | v3.15.0 | v3.16.0 |
|------|---------|---------|
| `python3 scripts/validate.py` | PASS | PASS |
| `pytest agents-sdk/tests/` | 109 passed | 134 passed (+25 new) |
| `python3 agents-sdk/agents/daily_driver.py --mode morning --dry-run` | PASS | PASS — preamble renders all 3 HEARTBEATs + on-demand pointer + tone rule; `Max budget: $0.6` |
| Three-morning live soak | n/a | Pending 2026-04-24..26 |
| Phase 6 producer loop (flush → synthesizer → lint) untouched | PASS | PASS |

### Known follow-ups

- **Three-morning live soak** (2026-04-24 through 2026-04-26). Gate-check criteria per the plan's Section 3.6: ≥1 carry-forward task reordered by sacred-block timing, zero `<!-- agent-error -->` entries, `cost_usd < 0.50` per run for the three runs (cap allows up to $0.60 but $0.50 is the healthy-soak signal), tone confirmed calm/factual/zen.
- **Phase 2** wires `meta_agent` / `flush` / `knowledge_lint` to consume `schedule-recommendations.md` and `SOUL.md` from their local-model prompt paths (zero cloud egress). Gated on Phase 1 soak being clean.
- **Phase 3** — `meeting_defender` and `sprint_health` wiring specs are written in the plan file but both agents remain `enabled = false`. Re-enablement is a separate, explicit decision per the 2026-04-09 audit.

## [3.15.0] - 2026-04-18

Internal restructure to a 3-domain folder layout and addition of the `work-operating-model` skill (Nate B. Jones's 5-layer operating-model elicitation pattern, ported as a local-markdown-only skill — no OB1/Postgres/Supabase). The aim: open one folder and find everything for that domain; downstream agents get a real per-domain context layer instead of generic defaults.

### Added

- `.claude/skills/work-operating-model/` — new skill with `SKILL.md`, `interview-questions.md`, and `artifact-templates.md`. Takes a `domain` argument (`the-block`, `creative-studio`, or `life-systems`) and runs the 5-layer interview into vault artifacts. Personal-only — intentionally NOT added to any export-group preset.
- `vault/05_atlas/operating-models/` — new folder with index `README.md` and three subfolders (`the-block/`, `creative-studio/`, `life-systems/`), each holding 5 placeholder artifacts (`HEARTBEAT.md`, `USER.md`, `SOUL.md`, `operating-model.md`, `schedule-recommendations.md`) at `status: awaiting-interview`.
- `the-block/` — new top-level domain workspace for Sean's day job at The Block. Contains `CLAUDE.md` (domain router), `README.md`, and the moved `product-management/` workspace.
- Three new domain `CLAUDE.md` routers at `the-block/CLAUDE.md`, `creative-studio/CLAUDE.md`, `life-systems/CLAUDE.md`. Each lists primary skills, primary agents, active MCPs, domain-specific non-negotiables, and links to the operating-model bundle.
- New "Domain Routing" table in root `CLAUDE.md` mapping task types to the correct domain `CLAUDE.md`.
- Non-Negotiable Rule #7 documenting the 3-domain structure and explicitly waiving the prior "product-management stays at root" rule.

### Changed

- **Folder moves (3):**
  - `16bitfit-battle-mode/` → `creative-studio/16bitfit-battle-mode/`
  - `product-management/` → `the-block/product-management/`
  - `design-team/` → `creative-studio/design-team/`
  - All three preserved as `git mv` to keep history. Untracked files inside `16bitfit-battle-mode/docs/plans/phase-6-plan-info/` (two PNGs) moved with the folder.
- **Path patches (11 files inside the moved 16bitfit folder):**
  - 8 Python files updated their `Path(__file__).parent` chains by +1 level so `REPO_ROOT` and `SUPERUSER_ROOT` still resolve to the actual `claude-code-superuser-pack/` root: `autoresearch/runner.py`, `pixel-quantizer/batch/batch_orchestrator.py`, `pixel-quantizer/batch/test_all_characters.py`, `pixel-quantizer/batch/generate_sheet_split.py`, `pixel-quantizer/video-eval/adapters.py`, `pixel-quantizer/video-eval/run_video_tests.py`, `pixel-quantizer/video-eval/run_e2e_pipeline.py`, `pixel-quantizer/video-eval/run_phase4_tests.py`.
  - 3 markdown files updated relative path references by +1 level: `creative-studio/16bitfit-battle-mode/CLAUDE.md` (`../agents-sdk/` → `../../agents-sdk/`); `creative-studio/16bitfit-battle-mode/docs/plans/phase6-SUPER-PLAN-2026-04-17.md` (~20 hits of `../../../{agents-sdk,.claude,CLAUDE.md}`); `creative-studio/16bitfit-battle-mode/docs/plans/phase-6-followup-claude-code-prompt.md` (3 hits).
- `.gitignore` — both `16bitfit-battle-mode/lora-output/` and `16bitfit-battle-mode/autoresearch/references/walk_cycle/frames_all/` rewritten to `creative-studio/16bitfit-battle-mode/...`.
- `scripts/validate.py` — `EXPECTED_DOMAINS` reduced from 5 to 3 (`the-block`, `creative-studio`, `life-systems`); missing → ERROR. Added new `ADDITIONAL_WORKSPACES_TO_SCAN = ["claude-mastery"]` so claude-mastery still gets secret-scanned without being required to exist as a primary domain. `validate_domains()` now also checks for a `CLAUDE.md` per domain (warning). `scan_secrets()` iterates `EXPECTED_DOMAINS + ADDITIONAL_WORKSPACES_TO_SCAN`.
- Root `CLAUDE.md` — refactored as a router. Preserved verbatim: Non-Negotiable Rules, Hook Exit Codes, When Modifying, Commands, Connected MCPs, Agents SDK section. Updated: skill count (111 → 113), Domain Workspaces table (3-domain layout), architecture diagram (3-domain tree), added Domain Routing section. SDK version bumped from `0.1.56` reference to `0.1.63` (now pinned).
- Root `README.md` — updated skill count (111 → 113), Domain Workspaces table rewritten to show the 3-domain layout with nested workspaces.
- `.claude/hooks/daily-note-appender.sh` — rewrote the domain-routing case statement (lines 36–58). Two bugs fixed: (1) `*block*` no longer routes to `product-management` — Block-domain paths (`the-block/`, `theblock`, plus Block products `campus`, `etf`) now route to `the-block`. (2) Pre-existing priority bug where `*superuser-pack*` was in the FIRST case caused every session in this repo to log as `claude-mastery` regardless of actual domain. Reordered to specific-first: nested project paths → domain roots → keyword fallbacks → repo-wide claude-mastery fallback last. Verified with 11-case routing test (the-block, creative-studio, life-systems, vault, claude-mastery, repo-root, campus, etf — all route correctly).
- `agents-sdk/pyproject.toml` — pinned `claude-agent-sdk` from `>=0.1.39` to `==0.1.63` for reproducibility. Matches what's now installed in the venv.
- `agents-sdk/.venv` — reinstalled missing dependencies (`claude-agent-sdk==0.1.63` + transitive `mcp`, `pydantic`, `httpx-sse`, `pandas`, `numpy`, etc.). The venv had been left in a partial state — only `wakeonlan` was present — which broke `daily_driver.py --dry-run` (and any agent that imports the SDK). `pip install -e .` failed because the project layout doesn't auto-discover packages; deps installed directly via `pip install` instead. Editable install isn't needed because agents are run via `PYTHONPATH=. .venv/bin/python3 agents/...` rather than via the `[project.scripts]` console-script entry points.

### Rationale

The root CLAUDE.md was approaching a readability ceiling and Sean's mental model (three clean domains) wasn't surfaced in the repo structure. The aggressive consolidation makes "where does this belong?" trivial for both Sean and downstream agents. The `work-operating-model` skill is the upstream prerequisite for the autonomous agent fleet to act with real context — none of the downstream agents (`meeting-defender`, `daily-driver`, `sprint-health`, etc.) can be sharply tuned without operating-model artifacts to read.

The decision to waive non-negotiable #13 (product-management stays at root) was made explicitly during planning: the only PM work Sean is doing is at The Block, so co-locating the workspace inside `the-block/` matches reality. If Sean later takes on PM work for a non-Block project, the workspace can be promoted back to root or duplicated.

OB1 (Nate B. Jones's Open Brain) was evaluated and rejected: Postgres + Supabase + MCP is architecturally incompatible with this pack's local-first, Keychain-based, three-machine substrate. The 5-layer interview pattern was ported as a single skill writing markdown to the vault. No infrastructure dependency added.

### Known follow-ups (not blocking this release)

- `vault/05_atlas/Sean-Winslow-Full-Personal-Context-v1.1.md` should bump to v2.0 once all three operating-model bundles are populated and confirmed.
- Wiring the `work-operating-model` artifacts into active agents (`daily-driver` reads `HEARTBEAT.md` for sacred-block awareness, etc.) is a future task — placeholders are scaffolded so the wiring can be added incrementally as artifacts get filled in.
- Design-team agent count was reconciled during this restructure: 5 design-team agents (`accessibility-checker`, `animation-director`, `design-system-enforcer`, `ui-reviewer`, `visual-polish-auditor`), not 4. Architecture comment in root CLAUDE.md updated accordingly.
- Add `vault/05_atlas/moc-the-block.md` — the new `the-block` domain currently has no dedicated Obsidian MOC. `moc-product-management.md` still exists and covers the generic PM tag; a new Block-specific MOC would surface the-block-tagged operating-model artifacts + Granola meeting notes + Block-specific project pages via Dataview. Low-priority — not blocking, but worth doing before populating the operating-model bundle.
- Add runtime artifact paths to `.gitignore`: `vault/90_system/agent-logs/*.csv` and `vault/90_system/agent-logs/*.log`. These files drift continuously as autonomous agents run and shouldn't show up as "modified" in every `git status`. They were intentionally left out of the v3.15.0 commit but remain tracked. A follow-up should either (a) `.gitignore` them and `git rm --cached` the tracked versions, or (b) move them under a path that's already ignored.
- ~~Three-domain interviews not yet run. The 15 operating-model placeholders are all at `status: awaiting-interview`. Run the skill three times (`Run the work-operating-model interview for the-block`, same for `creative-studio` and `life-systems`) to populate them. Interview results will be added to the `v3.15.0-restructure` branch as separate commits before merge.~~ **DONE** 2026-04-23 — all 15 artifacts at `status: confirmed` (the-block 2026-04-19 `0da643a`, creative-studio 2026-04-21 `ed3b9b5`, life-systems 2026-04-22 `7a17c0e`).

### Gate-check status

| Gate | v3.14.3 | v3.15.0 |
|------|---------|---------|
| `python3 scripts/validate.py` | PASS | PASS |
| Skill loaded by agents (work-operating-model) | n/a | PASS (registered in skill list) |
| Folder moves preserve git history | n/a | PASS (git mv used) |
| Relative paths in moved 16bitfit code | n/a | PASS (8 Python + 3 markdown patched) |
| Root CLAUDE.md preserves load-bearing sections | n/a | PASS (Non-Negotiable Rules / Hook Exit Codes / When Modifying / Commands all intact) |
| Daily Driver dry-run still works | PASS | PASS (after `claude-agent-sdk==0.1.63` reinstall in venv) |
| `daily-note-appender.sh` routes domains correctly | (latent bug — every session logged as claude-mastery) | PASS (11-case routing test) |

## [3.14.3] - 2026-04-18

Phase 6 reconciliation — commit to Mac Mini as the single always-on agent driver; retire the cross-machine WOL path that v3.14.0 added.

The parallel MBP-side A.6 run (branch `phase6-mbp-results`, closed unmerged after PR review) produced an independent N=20 benchmark that directionally agreed on `inbox_triage` (both SWAP) and `financial_analysis` (both KEEP the non-gemma4 incumbent), and disagreed on `code_review` in a way that pointed at the Jaccard extractor rather than the models. With Mac Mini chosen as the canonical driver, the MBP-sourced numbers live in git history for forensic record; the Mac Mini numbers in `A6-swap-decision-mac-mini-2026-04-18.md` are production-of-record.

### Changed

- `agents-sdk/config.toml`:
  - `[routing.machines.macbook_pro]` — `wol_mac` removed. `models` updated to `google/gemma-4-31b` (matches what LM Studio's `/v1/models` actually returns; the prior `gemma4-31b` was incorrect and silently 400'd MBP-sourced benchmark calls until the MBP-branch harness caught it). Host stays at MBP LAN IP for occasional cross-machine use.
  - `[routing.task_map]`:
    - `financial_analysis` rerouted from `qwen3-14b @ macbook_pro` to `phi4-mini-reasoning @ mac_mini`. Mac Mini is always on; MBP is not. The N=20 Mac Mini benchmark showed phi4-mini-reasoning scoring q=0.900 on this task — same quality as the prior MBP-hosted qwen3-14b incumbent — so the stack loses nothing by moving it onto the always-on host.
    - `code_review` stays on `qwen2.5-coder-32b-instruct @ macbook_pro` pending a scorer fix (both models scored below 0.2 in the MBP run / literally 0.000 in the Mac Mini run — points at the Jaccard-over-hyphenated-tags extractor, not the models).
  - `[notifications] notify_on` — `wol_failure` removed (no agent wakes the MBP anymore).
- MacBook Pro `launchctl` state — `com.sean.agent.vault-synthesizer` and `com.sean.agent.knowledge-lint` unloaded on the MBP. Mac Mini remains the sole launchd host for nightly agents.

### Rationale

v3.14.0 added a WOL-based cross-machine path so scheduled Mac Mini jobs could wake the MBP for heavy inference. Field experience showed the MBP's Private Wi-Fi Address randomizes the MAC seen by DHCP, so a fixed `wol_mac` in config wasn't reliably hitting the right interface. Rather than fight that, the stack is rescoped: agents that *need* heavy inference either run on the MBP interactively (unchanged) or fall back to Claude API on the rare paths where MBP-class capacity is required. Every scheduled agent in v3.14.3 resolves to a Mac-Mini-resident model or tolerates a missing MBP gracefully.

### Known follow-ups (not blocking this release)

- `[agents.vault_synthesizer].target_machine = "macbook_pro"` and `[routing.task_map].vault_synthesis` still point at the MBP. The nightly 02:30 run from Mac Mini will succeed only when MBP is awake, else log and exit. Future cleanup: either move synthesis to a Mac-Mini-resident model (Mac Mini can host `qwen3-14b` at 24 GB if pulled) or accept intermittent synthesis.
- `code_review` scorer rebuild — replace Jaccard-over-hyphenated-tags with either an LLM-judge rubric or a code-review-specific entity extractor. Re-run A.6 on code_review only afterward and let the veto gate decide.
- `wakeonlan>=3.1,<4` dep in `pyproject.toml` and `tests/test_route_to_macbook.py` are dead code. Leave for now; prune in a future housekeeping pass if WOL never comes back.

## [3.14.2] - 2026-04-18

Phase 6 housekeeping + scope-cut. 100% local ($0.00 API).

### Added

- `agents-sdk/scripts/phase6_gatecheck.py` Gate #7 — Meta-Agent fleet-status
  coverage check (≥5 artifacts/7d with ≥1 actionable alert) per Super Plan §E.5
- Workstream E (Meta-Agent / Fleet Self-Monitoring) adopted retroactively into
  the Phase 6 Super Plan as §E; plist invocation corrected to call
  `agents/meta_agent.py` via venv python (commit `9f7d85b`)
- `§10.1 Descope Log` in the Phase 6 Super Plan documenting D.4 removal with a
  fully-specified re-open plan, dependencies, and preserved artifacts

### Changed

- `agents-sdk/agents/knowledge_lint.py` — calibrated wikilink resolver to
  accept Obsidian path-style links `[[dir/sub/file]]`, added orphan-exclusion
  set for auto-generated directories (Granola notes, transcripts, `60_archive`,
  `00_inbox`, `90_system`, `70_apple-notes`, `daily`), strip fenced code blocks
  before scanning. **Real-vault issue count: 500 → 110** without sacrificing
  synthetic-vault recall (100% Tier 1, 0 FPs)
- `CLAUDE.md` intro line corrected to reflect actual file counts
  (13 subagents, 11 hooks, 13 SDK agents — 6 active) instead of the aspirational
  "16 agents, 8 hooks" that anticipated Phase 6 doc-update checklist counts
- Loaded meta-agent schedule (08:35 daily); unloaded the 6 audit-disabled
  launchd schedules that `install_schedules.sh` re-loaded by default
  (process-inbox, daily-evening, weekly-review, pr-digest, sprint-health,
  meeting-defender) per `AUDIT-2026-04-09-agent-downsizing.md`
- Unloaded `daily-morning-baton` plist (dead wait on disabled process-inbox
  flag); `daily-morning` continues to serve 8:45 AM daily brief

### Descoped

- **D.4 Autoresearch Feedback Loop** — the knowledge-graph consumer side of
  the Phase 6 knowledge-compounding loop (`vault/knowledge/concepts/` →
  autoresearch orchestrator read + `articles_used` logging + 7-night
  Wilcoxon A/B) is deferred. Rationale: upstream autoresearch convergence
  harness is in flight on a separate plan; integrating against a moving
  target would block Phase 6 indefinitely or generate refactor churn.
  D.1–D.3 (the producer side) remain live; the graph will accumulate data
  and sit ready when D.4 is re-opened. Gate #6 marked `DESCOPED` in
  `phase6_gatecheck.py`. Re-open spec: Super Plan §10.1.

### Gate-check status

| Gate | v3.14.0 | v3.14.2 |
|---|---|---|
| 1. Gemma 4 benchmarks on 3 tasks | PASS | PASS |
| 2. ≥1 model swap deployed | PASS | PASS |
| 3. SessionEnd ≥3 captures/week | FAIL (hook never fired) | FAIL (awaiting production runs) |
| 4. Synthesis ≥2 concepts/night | FAIL (dirs missing) | FAIL (dirs now exist, awaiting 2:30 AM MBP run) |
| 5. Lint ≥95% recall | PASS | PASS |
| 6. Autoresearch ≥10% convergence | PARTIAL | **DESCOPED** |
| 7. Meta-Agent ≥5 fleet-status/week | — (not in script) | PARTIAL (1/5, 0 alerts) |

Gates 3, 4, 7 self-resolve with accrued production data over the next 7 days.

---

## [3.14.1] - 2026-04-18

Phase 6 A.6 re-run at N=20 + WOL dependency-pin. 100% local ($0.00 API).

### Added

- `agents-sdk/benchmarks/results/A6-swap-decision-2026-04-18.md` — re-run report covering all 3 tasks × 2 models × 20 samples on Mac Mini Ollama (no MBP dependency)
- `agents-sdk/benchmarks/results/gemma4-benchmark-2026-04-18.json` — raw JSON with per-sample latency + extraction
- `wakeonlan>=3.1,<4` pinned in `agents-sdk/pyproject.toml` so `tests/test_route_to_macbook.py` can resolve `patch("wakeonlan.send_magic_packet")` (production code already had a stdlib fallback via `_send_raw_wol`)

### Changed

- `agents-sdk/config.toml` [routing.task_map]: `inbox_triage` swapped from `phi4-mini-reasoning` → **`gemma4:e4b`** on Mac Mini. N=20 head-to-head: +7.5 pp quality, +57% p50 speedup. `machines.mac_mini.models` extended to include `gemma4:e4b`.
- `agents-sdk/scripts/run_gemma4_benchmark.py`: challenger matrix re-scoped from `gemma4-31b @ macbook_pro` to `gemma4:e4b @ mac_mini` across all 3 tasks. Added `INCUMBENT_OVERRIDES` so financial_analysis + code_review test on Mac Mini regardless of config.toml's production routing. Documented WOL deferral reasoning in header.

### Deferred

- `financial_analysis` swap — gemma4:e4b regressed −10 pp on quality. Veto gate (§A.6) fires; kept phi4-mini-reasoning.
- `code_review` swap — both models scored 0.000 due to an extractor bug (hyphenated tags like `sql-injection` don't match model output text). Follow-up: fix extractor to treat `-`/` `/`_` as equivalent, then re-bench this task only.
- MBP WOL production use — live verify failed because MBP's Private Wi-Fi Address hands out the config's IP (.50) under a randomized MAC. Code (`route_to_macbook`, tests, `verify_mbp_wol.py`) stays in place; no currently-enabled agent blocks on it.

### Gate-check status

| Gate | Before | After |
|---|---|---|
| 1. Gemma 4 benchmarks on 3 tasks | PARTIAL | PASS |
| 2. ≥1 model swap deployed | PARTIAL | PASS |

## [3.14.0] - 2026-04-17

Phase 6 — Gemma 4 benchmarking + Knowledge Compounding Loop. 100% local ($0.00 API).

Renumbered from 3.13.0 → 3.14.0 during merge with main: origin/main had independently published a different 3.13.0 (Phase 1 autoresearch scoring rubric rework) and a 3.13.1 (Phase 1 results) on 2026-04-17/18. Phase 6 gets the next minor bump since it introduces new agents (flush, vault-synthesizer, knowledge-lint).

### Added

- `agents-sdk/lib/filelock.py` — fcntl-based LOCK_EX/LOCK_SH context manager with timeout (P0.1 blocker resolved)
- `agents-sdk/lib/session_transcript.py` — CC JSONL session transcript parser
- `agents-sdk/lib/pushover.py` — Pushover push-notification helper (keychain-backed, no plaintext tokens)
- `agents-sdk/lib/lint_report.py` — parses knowledge-lint reports for daily_driver surfacing
- `agents-sdk/lib/gemma4_benchmark.py` — multi-model benchmark harness (p50/p95, Jaccard, veto gate)
- `agents-sdk/agents/flush.py` — SessionEnd daily-log extractor; routes by message count (<100 → phi4-mini, ≥100 → Qwen3-14B); filelocked append to `vault/daily/YYYY-MM-DD.md`; recursion-guarded on `CLAUDE_INVOKED_BY`
- `agents-sdk/agents/vault_synthesizer.py` — nightly concept + connection article generator on MBP via `route_to_macbook`; ≥2 wikilink invariant; 45-min budget; auto-regenerates `vault/knowledge/index.md`
- `agents-sdk/agents/knowledge_lint.py` — two-tier vault health scan (Tier 1 structural on Mac Mini, Tier 2 semantic on MBP); synthetic 30-file vault with 20 planted issues for ≥95% recall gate
- `agents-sdk/scripts/run_gemma4_benchmark.py` — A.5 driver for head-to-head model runs
- `agents-sdk/scripts/phase6_gatecheck.py` — one-liner that runs all 6 gate-check criteria and emits PASS/PARTIAL/FAIL
- `agents-sdk/scripts/compare_convergence.py` — D.4 A/B harness (trials-to-best-fitness, paired Wilcoxon, ≥10% + p<0.1 gate)
- `agents-sdk/benchmarks/golden_sets/{inbox_triage,financial_analysis,code_review}.json` — 20 samples each
- `agents-sdk/schedules/com.sean.agent.vault-synthesizer.plist` — nightly 02:30
- `agents-sdk/schedules/com.sean.agent.knowledge-lint.plist` — Sunday 22:00
- `.claude/hooks/session-end-flush.sh` — SessionEnd hook, <100ms non-blocking, fire-and-forget via `nohup`, recursion-guarded
- Pushover credentials in macOS Keychain (`pushover_user_key`, `pushover_app_token`) for WOL / agent-error / gate-check-fail notifications
- `WOLUnavailable` exception + `HybridRouter.route_to_macbook()` with WOL + Pushover fallback

### Changed

- `agents-sdk/agents/vault_indexer.py` — SHA-256 hash-based state tracking in `vault/.indexer-state.json`; `detect_changed_files()` surface for synthesizer handoff; `vault/daily/` excluded from embed index (SOT D.1 line 482)
- `agents-sdk/agents/daily_driver.py` — morning mode surfaces Vault Health (CRITICAL/HIGH counts or PASS ✓)
- `agents-sdk/lib/hybrid_router.py` — recognizes `lm-studio` runtime alongside `mlx-lm`; adds `route_to_macbook()`
- `agents-sdk/config.toml`:
  - MacBook Pro port 8080 → **1234** (LM Studio default)
  - MacBook Pro models aligned to `/v1/models` IDs (`qwen3-14b`, `qwen2.5-coder-32b-instruct`, `gemma4-31b`)
  - `[routing.task_map]` `vault_synthesis` entry (Phase 6 synthesizer model resolution)
  - `[notifications]` section referencing Pushover keychain keys
  - `[agents.flush]`, `[agents.vault_synthesizer]`, `[agents.knowledge_lint]` sections added
  - `[agents.vault_indexer]` extended with synthesis + hash-state options
- `.claude/settings.json` — registers SessionEnd hook pointing at `session-end-flush.sh`
- **Agent fleet:** 2 → 5 active (vault-indexer, daily-driver morning, flush, vault-synthesizer, knowledge-lint). Hook count: 7 → 8. All new agents run 100% local; monthly cost unchanged.

### Phase 6 substitution note

Ollama's registry names Gemma 4 as `gemma4:26b` (26B MoE with 3.8B active) and `gemma4:31b` (31B dense). The super-plan used `gemma4:27b` which does not exist; the 26B MoE is the same model class and was pulled instead. LM Studio MBP path pulled `google/gemma-4-31b` as the MLX 4-bit variant (`gemma4-31b` identifier).

### A.5 / A.6 result

A.5 benchmark run: inbox_triage head-to-head completed (5 samples/model). Gemma 4 31B on MBP scored **0.567 quality / 32.3s p50** versus incumbent phi4-mini-reasoning on Mac Mini at **0.667 / 21.2s**. Gemma 4 26B on Mac Mini failed every sample (>120s) due to MoE dispatch overhead on 24 GB RAM. Veto gate (≥5% quality regression = KEEP) fires on both challengers → **NO SWAP**. financial_analysis and code_review runs were deferred after LM Studio RAM guardrail blocked JIT-load during the incumbent phase; per plan §7.1, further challenger tests are optional once inbox_triage veto fires. Full report: `agents-sdk/benchmarks/results/A6-swap-decision-2026-04-17.md`. `[routing.task_map]` unchanged.

Gate-check criteria #1 and #2 land as **PARTIAL** under plan §5's fallback path ("If Gemma 4 loses all: commit benchmark doc + mark this bullet PARTIAL"). The P6 veto gate itself is functioning correctly — that is the phase deliverable.

### Tests

- 106 pytest cases, 100% pass — new coverage: filelock (6), session_transcript (6), pushover (5), gemma4_benchmark (6), route_to_macbook (4), flush (9), vault_indexer hash-state (7), vault_synthesizer (9), knowledge_lint (7 incl. 95% recall gate against 20-issue oracle), daily_driver vault-health (4)

## [3.13.1] - 2026-04-18

### Results — Phase 1 Autoresearch (150 trials, Illustrious XL v2.0)

Full 150-trial run completed overnight on the Alienware RTX 5080. All trials succeeded (0 failures, 0 timeouts). Total runtime ~5.3 hrs.

**Best trial (#16): composite 0.8163** — SpaceCandy LoRA (str_model 0.556, str_clip 0.389), IP-Adapter FaceID weight 0.76, weight_faceidv2 1.20, weight_type `composition`, ControlNet strength 0.86 / end_percent 0.37, pose `ryu_walk_up.png`, sampler `euler`, scheduler `exponential`, CFG 6.0, steps 25, seed 2662995976.

**Score distribution:** mean 0.6357, median 0.6358, range 0.4207–0.8163.

**Convergence signals (top 20 trials):**
- `ipadapter_weight_type = composition` — 20/20 (100%, hard winner)
- `lora_name = SpaceCandy_SpriteSheet_v1_ILXL` — 18/20 (90%)
- `pose_frame = ryu_walk_up.png` — 13/20 (65%)
- `sampler_name = euler` — 11/20
- `scheduler = exponential` — 10/20

**Systemic ceiling — character consistency stuck at 1–2/5:** Every top-scoring trial earned 5/5 on silhouette, pose accuracy, pixel art discipline, proportions, and line work — but capped at 2/5 on character consistency against Sean's anchor. VLM feedback across trials: "different gender," "wrong outfit/hair," "robot vs human," "tail," etc. Root cause almost certainly the anchor itself (`champion_sean_anchor-1.png` is 2752×1536, likely a sprite sheet not a face crop) — IP-Adapter FaceID wants a clean face crop for InsightFace to extract a usable embedding. Composite ceiling is ~0.82 until character grounding is fixed. Phase 0 best was 0.8448.

### Decision — Pausing SDXL-era autoresearch

After eyeballing the top-5 sprites from this run, Sean's judgment: **output quality looks like 2019–2020-era image generation**. Not worth further investment in optimizing SDXL / Illustrious XL / SDXL-based LoRAs within this autoresearch loop. Community praise for these models doesn't outweigh the visible quality gap against modern foundation models.

**No more SDXL-era autoresearch.** The 14-parameter search space was a correct optimization target for the wrong underlying model. The autoresearch infrastructure itself (Optuna loop, workflow mutator, 5-tier scorer, VLM judge with face-grounded rubric) is sound and transferable.

### Next direction — Evaluate newer open-source image models

Candidates to investigate before restarting any autoresearch:

- **Z-Image-Turbo** (Tongyi-MAI / Alibaba) — https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
- **ERNIE-Image-Turbo (GGUF)** (Unsloth quantization of Baidu's ERNIE) — https://huggingface.co/unsloth/ERNIE-Image-Turbo-GGUF. SETUP-NOTES previously flagged ERNIE as not viable due to 24 GB VRAM requirement and no ComfyUI integration; GGUF quantization may change the VRAM calculus, and ComfyUI support may have landed since that evaluation. Worth re-checking.
- Closed-source comparison targets for quality calibration (not for pipeline use): Nano Banana 2, GPT Image 1.5.

For each candidate, before building any mutator/search space, verify:
1. RTX 5080 (16 GB VRAM, sm_120, no xformers) compatibility
2. ComfyUI node support (or alternative runtime — diffusers direct, custom API)
3. ControlNet + character-conditioning equivalents (IP-Adapter FaceID, reference image support)
4. LoRA / fine-tuning ecosystem maturity (for Sean-specific training later)

### Kept (infrastructure, not deprecated)

- `autoresearch/runner.py` Phase 1 branch, preflight, Optuna loop, CSV/DB lockstep — reusable for any new model backend.
- `autoresearch/workflow_mutator.py` mutate function — reusable pattern for any ComfyUI-based workflow.
- `autoresearch/prepare.py` 5-tier scorer with face-grounded VLM rubric — reusable regardless of which image model generates the sprite.
- 150 trial artifacts at `results/phase1/` — keep as ground truth for "SDXL/Illustrious XL ceiling on this workflow, at this hardware, judged by this rubric" benchmark. Do not delete.

## [3.13.0] - 2026-04-17

### Changed

- **Autoresearch Phase 1 scoring rubric reworked for single-pose sprites.** Phase 0 used a walk-cycle rubric in `prepare.py` (leg variety, pose flow, weight shift, arm swing, character consistency, size consistency) because its outputs were multi-frame sheets. Phase 1 generates one posed sprite per trial via ControlNet+IP-Adapter, so motion-progression axes are unscorable — the VLM was giving arbitrary low scores on arm swing / weight shift regardless of sprite quality, adding ~half-noise to the VLM signal. Rubric replaced with six Phase 1-appropriate axes: **silhouette readability, pose accuracy, pixel art discipline, character consistency, proportions, line work**. Three coordinated changes in `16bitfit-battle-mode/autoresearch/prepare.py`:
  - `WALK_WEIGHTS` dict updated with new keys and weights (silhouette 0.25, pose 0.20, pixel 0.20, character 0.15, proportions 0.10, line 0.10)
  - `OllamaVLMAdapter.score_walk_cycle` compact_prompt rewritten (kept terse to stay under the 180s Qwen3-VL:8b timeout; a verbose first draft ran past 180s)
  - `_parse_vlm_response` label_map updated so the keyword→key mapping matches new axes
- **Autoresearch Phase 1 downscale bypass.** `prepare.py::_preprocess_frames` nearest-neighbor-resizes frames to `tile_size` (128 for champions) before scoring. That masked quality differences between 1024×1024 ComfyUI outputs. Phase 1 runner now sets `scorer.tile_size` to the workflow's native latent resolution, making preprocess a no-op so the optimizer judges full-quality sprites. Downscale to production tiles is handled manually in Photoshop downstream.
- **Autoresearch Phase 1 VLM host + timeout.** `AutoresearchScorer(...)` call in `runner.run_phase1` now passes `alienware_host="127.0.0.1"` (loopback — scorer runs on the Alienware itself) and `vlm_timeout=300` (was 30, which timed out on every call; bumped from an intermediate 180 after anchor image was added, which pushed latency to ~160–210s per call).
- **VLM now receives the character anchor image.** `OllamaVLMAdapter.score_walk_cycle` was accepting an `anchor_image` bytes arg but never sending it; `_tier4_vlm_judge` was passing `b""`. Fixed both: scorer loads the first anchor from `references/anchors/champions/<Character>/`, Lanczos-downscales to ≤768px longest edge (gold-standard photo downscale — preserves edges without ringing or blur; 768 keeps Sean's face at ~200px), caches bytes on the scorer instance. Adapter sends anchor + generated sprite as two images and uses a branched prompt that labels them ("Image 1 is the character reference. Image 2 is the generated sprite.") so character_consistency is evaluated against Sean's actual reference instead of the model's imagined character from the text prompt. In a verification trial, character_consistency went from a blind 5/5 to a grounded 1/5 with specific actionable feedback ("tank top vs. shirtless, blue pants vs. tan, blonde vs. brown hair") — the exact signal the optimizer needs.

### Added

- **Autoresearch Phase 1 Optuna loop** (`autoresearch/runner.py` `run_phase1`). 14-param search space (LoRA selection + strengths, IP-Adapter weights, ControlNet strength/end_percent, sampler/scheduler/CFG/steps/seed, pose frame) defined in `autoresearch/search_space.py` (`PHASE1_PARAMS` + `suggest_phase1`). Workflow mutator in `autoresearch/workflow_mutator.py` (`mutate_phase1_sprite_gen`) targets the exact node IDs in `phase1_sprite_gen.json` per `SETUP-NOTES.md`. Hard rules enforced: SF3XL LoRA banned (broken on Illustrious XL v2.0 at strength > 0.15), `cn_end_percent` capped at 0.7 (higher renders skeleton literally into output), `lora_name="none"` bypasses LoRA by zeroing strengths.
- **Pre-flight health check** in Phase 1 runner: ComfyUI `/system_stats` reachability, VRAM free ≥10 GB warning, pose-skeleton sync into `ComfyUI/input/`, model-file presence check for LoRAs / ControlNet / IP-Adapter.
- **Resumable Optuna study** at `results/phase1/phase1.db` (study name `phase1_sprite_v1`). Supports `--resume` flag.
- **Per-trial artifacts** at `results/phase1/trials/trial_NNNN/`: `sprite.png` (1024×1024 ComfyUI output), `params.json` (sampled Optuna params), `score.json` (all 5 scoring tiers). Plus aggregate `trials.csv`.
- **CSV writes moved to Optuna post-persist callback** so `trials.csv` and `phase1.db` stay in lockstep even if the process is killed mid-trial. Previously a crash between CSV write and Optuna's DB flush could leave CSV one row ahead of DB, causing duplicate rows on `--resume`.

### Known Limitations

- Phase 0 scoring is no longer backward-compatible after the `WALK_WEIGHTS` key rename. Phase 0's best-of-N run artifacts already exist with the old rubric — re-scoring them would require reverting this commit.
- Only the first of three available Sean anchors (`champion_sean_anchor-1.png`) is sent to the VLM. Multi-anchor comparison would give the VLM more angles to judge against but would also multiply per-call latency. Deferred.

## [3.12.3] - 2026-04-09

### Changed

- **Agent fleet audit and downsizing** — Disabled 8 of 10 scheduled agents after a full audit of `agent-run-history.csv` and all agent logs from April 1–9. Only `vault-indexer` (100% success, $0 cost) and `daily-driver morning` (working since v3.12.2, ~$0.40/run) remain active. See `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md` for full reasoning.
- Unloaded 6 launchd schedules: `daily-evening`, `process-inbox`, `pr-digest`, `sprint-health`, `meeting-defender`, `weekly-review`
- Set `enabled = false` in `config.toml` for: `process-inbox`, `pr-digest`, `sprint-health`, `meeting-defender`, `preserve-session`, `spending-analysis` (daily-driver evening/weekly were already only controlled by launchd)
- Cleaned `vault/90_system/agent-logs/`: removed all logs for disabled agents, truncated stderr rolling logs, trimmed `agent-run-history.csv` to active agents only. Reduced from 44 files to 12.
- Updated Agents SDK table in `CLAUDE.md` to reflect 2-agent fleet

### Fixed

- **process-inbox burning ~$0.31/day on failures** — Agent hit `error_max_budget_usd` every run since April 1 due to `CLIConnectionError`, wasting ~$9.30/month. Disabled.

## [3.12.2] - 2026-04-08

### Fixed

- **Daily driver morning agent hitting budget cap** — The 2026-04-08 morning run connected successfully (PATH fix confirmed working) but failed with `error_max_budget_usd` after 9 turns / $0.29 spent, exceeding the $0.25 cap. Bumped morning budget from $0.25 to $0.50.

### Changed

- Daily driver morning schedule: 6:00 AM → 8:45 AM (config.toml + launchd plist)
- Daily driver morning budget: $0.25 → $0.50 (config.toml)

## [3.12.1] - 2026-04-07

### Fixed

- **launchd agents failing with `TaskGroup` / `CLIConnectionError`** — All Claude Agent SDK agents (daily-driver, process-inbox, pr-digest, etc.) had been failing since 2026-04-01. Root cause: macOS launchd runs jobs with a minimal PATH that doesn't include `~/.local/bin` where the `claude` CLI lives. The SDK spawns `claude` as a subprocess, and when launchd couldn't find the binary, the process died immediately, surfacing as `CLIConnectionError: ProcessTransport is not ready for writing` (wrapped in an unhelpful `TaskGroup` error). Added `EnvironmentVariables` with full `PATH` to all 9 launchd plists. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md` for full writeup.

### Changed

- Upgraded `claude-agent-sdk` from `0.1.39` to `0.1.56`
- All 9 launchd plists in `agents-sdk/schedules/` now include `PATH` in `EnvironmentVariables` (includes `~/.local/bin` for `claude` CLI and `/opt/homebrew/bin` for `gh` and other Homebrew tools)

## [3.12.0] - 2026-03-18

### Added

- `shadcn-ui-patterns` — shadcn/ui component library patterns for accessible React UIs. Full import from giuseppe-trisciuoglio/developer-kit community skill, adapted to pack format. Covers installation, Radix UI primitives, CSS variable theming (light/dark), React Hook Form + Zod validation, and 11 component patterns (Button, Input, Form, Card, Dialog, Select, Sheet, Menubar, Table, Toast, Charts/Recharts). Includes Next.js App Router integration, CVA variant customization, and common combinations.
- `ux-design-guidelines` — 99 priority-ranked UX design rules extracted from nextlevelbuilder/ui-ux-pro-max community skill (lightweight version, no Python/CSV dependencies). 10 categories by impact: Accessibility (CRITICAL, 14 rules), Touch & Interaction (CRITICAL, 17), Performance (HIGH, 19), Style Selection (HIGH, 13), Layout & Responsive (HIGH, 16), Typography & Color (MEDIUM, 15), Animation (MEDIUM, 25), Forms & Feedback (MEDIUM, 30), Navigation (HIGH, 27), Charts & Data (LOW, 30). Includes professional standards tables (icons, light/dark mode, layout) and pre-delivery checklist.

### Changed

- Skill count: 109 → 111
- Export group `10-master-designer` updated with both new skills
- Design-team domain: 8 → 10 skills

## [3.11.0] - 2026-03-08

### Added

- `design-arena` — Orchestrate competitive UI/UX design exploration using Claude Code Agent Teams and Pencil.dev. Multiple agents create competing layout interpretations from the same design brief, evaluate results side by side, synthesize the best elements, then build out the final design. Includes condensed design interview, constraint brief generation, creative brief library, evaluation rubric, and human-in-the-loop steering throughout.
- `writing-voice-modes` — 5 writing voice modes calibrated to Sean's personal style through interview and writing exercises. Modes: Domestic Observer (Sedaris-tuned), Gonzo Technical (Thompson-tuned), Beat Flow (Kerouac-tuned), Minimalist Absurdist (Vonnegut-tuned), and Sean Mode (calibrated hybrid default). Includes signature moves (Hard Cut/Deflation, Rule of Three with Emotional Pivot, Callback Closers, Sensory Before Numbers, Screenwriting Cut-To), professional dial (20-100% intensity by context), content type → mode mapping, complementary technique pairs, and anti-patterns. Works alongside `creative-writing` (format) and `technical-writing` (audience). References `vault/40_knowledge/references/ref-voice-mechanics-research.md` for deep author mechanics.
- `vault/90_system/scripts/process-granola-notes.py` — Granola meeting note post-processor. Auto-sorts into subfolders by title keywords, injects vault-schema YAML frontmatter (resolves Granola `type` collision), renames to `mtg-YYYY-MM-DD-title.md` convention, resolves speaker names in transcripts (You→Sean, Guest→name for 1:1s), updates cross-links. Supports `--dry-run` and `--migrate` modes. Migrated 10 embedded notes, 12 transcripts, 4 manual notes.

### Changed

- Skill count: 107 → 109
- Reconfigured `obsidian-granola-sync` plugin: `saveAsIndividualFiles: true`, `linkFromDailyNotes: true`, `transcriptHandling: "same-location"`
- Updated `tpl-daily.md` with `## Meetings` section and `<!-- meetings -->` anchor
- Updated `VAULT-GUIDE.md` Granola section with processing script docs, auto-sort rules, frontmatter schema

## [3.10.0] - 2026-02-28

### Added

- `intent-engineering` — Intent specification design, review, and retrofit skill for AI agents. 9-section unified template (Objective, User Goal, Outcomes, Health Metrics, Strategic Context, Constraints, Decision Authority, Edge Cases, Stop Rules), 4 autonomy levels mapped to architecture (full-autonomous/guarded-autonomous/proposal-first/human-required), Minimum Viable Retrofit guide (3 conversion levels for existing 107 skills), 5 fatal anti-patterns (Klarna Intent Gap, prompt-based hard constraints, activity vs outcome confusion, vibe-coded edge cases, missing stop rules), validation checklist. Includes `references/intent-spec-template.md` with blank YAML template and completed daily-driver worked example.

### Changed

- `agents-sdk/agents/daily_driver.py` — Enhanced `build_preamble()` with Zero-Interaction Mandate (formalized with schedule time from config), Safe Deferral Protocol (max 2 retries, error note at `<!-- agent-error -->` anchor), and Health Metric Awareness (data non-destruction, truth anchoring, content integrity). Added mode-aware execution limits in `build_options()` — reads per-mode overrides from `config.toml [agents.daily_driver.modes.*]`.
- `agents-sdk/config.toml` — Added per-mode execution limits for daily_driver: morning (15 turns/$0.25), evening (10 turns/$0.25), weekly (20 turns/$0.50).
- Skill count: 106 → 107

## [3.9.2] - 2026-03-04

### Changed

- **`daily-driver` Slack overnight scan** — Added Step 1b to morning planning protocol. Scans DMs, @mentions, and key channels since last EOD (~5 PM). Classifies messages as Action Required / FYI / Skip. Writes digest to new `<!-- slack-overnight -->` anchor in daily notes. Filters out Jira bot noise and already-replied messages. Uses native Slack plugin (`plugin:slack:slack`), not Zapier.
- **Daily note template** — Added `## Slack Overnight` section with `<!-- slack-overnight -->` anchor to `vault/90_system/templates/tpl-daily.md`, positioned above Morning Focus.

## [3.9.1] - 2026-03-04

### Changed

- **Native MCP preference over Zapier** — Updated 6 skills and Agent SDK docs to prefer native MCPs over Zapier equivalents where both exist. Skills updated: `daily-driver`, `time-management`, `meeting-prep`, `personal-finance`, `data-analysis`. Agent SDK docs (`docs/agents-adk-docs/agents-sdk.md`) "Tools, APIs, and MCPs" section fully rewritten with current connected MCP inventory and native-vs-Zapier preference table.
- **Slack plugin installed and authenticated** — Native Slack MCP plugin (`plugin:slack:slack`) installed and OAuth-authenticated to The Block Crypto Inc workspace. No admin approval required. Replaces Zapier Slack tools for interactive sessions.
- **Standalone Context7 MCP removed** — Redundant standalone `context7` MCP removed; `plugin:context7:context7` is the sole instance.
- **`.env` cleaned** — Removed stale command on line 43, orphaned bare key on line 61, fixed doubled Runware key, standardized variable naming (`Gemini_API` → `GEMINI_API_KEY`, consolidated ElevenLabs keys).

## [3.9.0] - 2026-02-22

### Added

- `prompt-engineering` — Prompt engineering skill applying Anthropic's official 9-technique checklist. Covers clarity, multishot examples, chain of thought, XML tags, role prompting, prefilling, chaining, long context, and validation loops. Includes detailed techniques-guide.md reference.
- **Agents SDK layer** (`agents-sdk/`) — Autonomous agents powered by the Claude Agent SDK (Python). Runs outside Claude Code sessions on macOS launchd schedules. Skills are loaded as system prompts — no content duplication.
- `agents-sdk/agents/daily_driver.py` — Daily Driver agent with three modes:
  - **Morning** (6:00 AM): Read yesterday's note, create today's from template, write 1-3-5 priority plan
  - **Evening** (5:00 PM): Summarize day's progress, write Evening Reflection (Win/Lesson/Carry Forward)
  - **Weekly** (Friday 4:00 PM): Aggregate 7 daily notes into weekly review at `vault/10_timeline/weekly/`
- `agents-sdk/lib/config.py` — Configuration loader: reads `config.toml` + `.env`, returns typed `Config` dataclass with per-agent settings and safety limits
- `agents-sdk/lib/skill_loader.py` — Skill-to-prompt bridge: reads `.claude/skills/*/SKILL.md`, strips YAML frontmatter, concatenates multiple skills with headers
- `agents-sdk/lib/vault_io.py` — Vault I/O utilities: path conventions (daily/weekly notes), anchor injection (`inject_at_anchor`), template creation, frontmatter reading
- `agents-sdk/lib/logging_setup.py` — Structured logging: per-run log files + append-only `agent-run-history.csv` with cost/duration/turns tracking
- `agents-sdk/lib/custom_tools.py` — MCP tool definitions: `vault_inject` tool for PATCH-style writes to vault anchors
- `agents-sdk/config.toml` — Central configuration: vault paths, per-agent settings (enabled, skills, max_turns, max_budget_usd), safety limits, logging config
- `agents-sdk/schedules/` — 3 launchd `.plist` files (morning, evening, weekly) + `install_schedules.sh` installer
- `agents-sdk/tests/` — 33 pytest tests covering config, skill loading, vault I/O, and logging
- `agents-sdk/pyproject.toml` — Python package with deps: `claude-agent-sdk>=0.1.39`, `python-dotenv`, `pandas`, `tomli`
- `docs/agents-sdk.md` — Comprehensive guide: architecture, usage, expansion, recommended integrations, troubleshooting

- **Granola meeting sync** — Installed `obsidian-granola-sync` community plugin for automatic meeting transcript sync from Granola into the vault. Notes land in `vault/30_domains/product-management/the-block-meetings-granola-notes/` with subfolders: `adops-revops`, `daily-standup`, `david-sean-one-on-ones`, `design-sync`, `ed-sean-one-on-ones`, `other`. Plugin syncs to a single destination folder; manual sorting into subfolders for now. **TODO**: Build auto-sort script/automation that routes Granola notes into subfolders based on meeting title keywords.

### Changed

- `CLAUDE.md` — Added Agents SDK section with commands, architecture diagram updated to include `agents-sdk/`
- `README.md` — Added Agents SDK section, updated skill count (89 → 106), added adobe-creative export group
- Skill count: 102 → 106 (+1 prompt-engineering, +3 from plugin/superpower installations)
- `CLAUDE.md` — Added mandatory doc-update rule: CHANGELOG.md, CLAUDE.md, and README.md must be updated whenever a new Skill, Agent, Sub-Agent, Hook, or Script is created
- Authentication: SDK uses Claude Code CLI's existing OAuth auth (`claude login`) — no separate API key required

## [3.8.1] - 2026-02-19

### Fixed

- `SKILLS-AUDIT-v2.md` — Fixed version drift: updated Final Skill Count table (v3.6.0 no longer marked CURRENT, v3.8.0 now CURRENT), updated all skill/agent/hook inventory sections with Phase 5-6 additions, marked all Gap Analysis items as DONE, updated section headers with correct counts, updated footer to reflect v3.8.0 state.
- `SKILLS-AUDIT-v2.md` — Updated Lessons Learned #1: background subagent limitation documented with full tool compatibility table (Read/Glob/Grep work, Write/Edit/Bash blocked with explicit error, not silent). Added workaround pattern.
- `export-groups/07-technical-stack/playground.json` — Fixed duplicate `agents` key (had both `"agents": ["code-reviewer"]` and `"agents": []`).
- Synced `docs/Superuser-Pack-Skills-Audit.md` mirror with updated audit doc.

## [3.8.0] - 2026-02-18

### Added

- `comfyui-workflows` — Dedicated ComfyUI workflow design, debugging, and automation skill. Covers workflow JSON structure, node wiring patterns (KSampler, LoRA, ControlNet, IPAdapter), API queuing/polling, batch generation, model management, and debugging common issues.
- `daily-note-appender` hook (Stop) — Appends session summary to today's Obsidian daily note when Claude Code stops.
- `network-access-control` hook (PreToolUse Bash) — Blocks curl/wget/nc to non-whitelisted domains.

### Changed

- `block-secrets.py` — Narrowed patterns to eliminate false positives. Replaced `*key*` with `*api_key*`, `*api-key*`, `*apikey*`, `*private_key*`, `*private-key*`. Replaced `*password*` with `*_password*`, `*passwd*`. Added `*secret_key*`, `*_secret*`, `*client_secret*`. No longer blocks files containing "keyboard", "keynote", "keyframe", etc.
- Skill count: 101 → 102 (+1 new)
- Hook count: 5 → 7 (+2 new)

## [3.7.0] - 2026-02-18

### Added

- `animation-pipeline` — End-to-end 2D animation production pipeline with AI-assisted generation. 12-stage pipeline (Script→Final Render) with QA gates (blocker vs warning), shot packet structure, ComfyUI integration for character/background generation, frame interpolation (RIFE/FILM), style profiles, asset naming conventions.
- `script-writing` — Screenplay writing for animated short films. Industry-standard format, beat sheet structure (6-8 beats for shorts, 10-12 for longer), dialogue craft rules, animation-specific additions (timing cues, SFX notation), production handoff with shot breakdown tables, table read protocol.
- `creative-writing` — Multi-format writing assistant for blog posts, social media (Twitter/X threads, LinkedIn, Instagram), pitch documents (festival submissions, grant applications), artist bios/statements, portfolio narratives. Cross-format adaptation guide and voice consistency profile.
- `career-transition` — PM → Animation PM/Producer transition guide. Terminology bridge (40+ term translations), role map with title-level equivalencies, festival circuit (Tier 1/2/3), production tools comparison, transition narrative template, 90-day plan.
- `personal-app-patterns` — Opinionated starter patterns for React + Vite + Tailwind + Supabase personal apps. Canonical folder structure, auth context, protected routes, common database tables, dark mode toggle, deployment checklist.
- `technical-writing` — Audience-aware document craft. Templates for API getting-started guides, system design docs, onboarding guides, runbooks, release notes, internal RFCs. Differentiated from doc-workflows (automated generation) and tech-spec (engineering blueprints).
- `rn-architecture` — React Native app architecture and project setup. Covers Expo SDK 52+, Expo Router (file-based), Zustand, TanStack Query, EAS Build profiles, feature-based folder structure. Complements rn-debug (diagnosis).
- `comfyui-workflows` — (see 3.8.0 for this entry, created alongside Phase 6)
- `animation-director` agent — Read-only reviewer for animation assets and pipeline outputs. Applies QA gates from animation-pipeline and 2d-animation-principles.
- `code-reviewer` agent — Read-only code reviewer for architecture, patterns, performance, security. Complements design-team agents (UI-focused).
- Skill count: 94 → 101 (+7 new skills)
- Agent count: 11 → 13 (+2 new agents)
- All new skills at Q:5 quality level
- Updated export-group manifests: 03-creative-projects, 02-pm-workflows, 05-life-optimization, 07-technical-stack

## [3.6.0] - 2026-02-18

### Added

- `etf-page-creator` — WordPress ETF page creation assistant for The Block. Guides data collection (Track Insight IDs, TradingView symbols, issuers, fees, categories), validates inputs, auto-generates SEO metadata using Block's standard formats, and produces copy-paste checklist matching WordPress field order.

### Changed

- `meeting-prep` — Full Block rewrite: standup format (10-10:45 AM ET, round-robin by Jira board), full team roster (17 members organized by Product/Design/Engineering/QA/DevOps), 7 recurring meetings with cadence/time/attendees, JQL queries for standup prep, 1:1 templates for Ed and David, Retros.work integration, meeting necessity check. Quality: 4→5.
- `data-analysis` — Full Block rewrite: tools access table (GA4 via Zapier MCP, Looker view-only, Jira full, Google Sheets), key metrics tracking (content, data pages, ad revenue, Campus, SEO), Ed's 6 analytics questions, Zapier MCP GA4 query patterns, pandas analysis pipeline, report templates (weekly/monthly), distribution workflow (Confluence → Slack → vault). Quality: 4→5.
- `stakeholder-update` — Merged biweekly-jira-update skill: team scope (16 members), 3 JQL queries with exact statuses, product/area prefixes (.Co, Campus, SFMC, Ad Server, Crypto IQ), status tags, output template with 3 sections, recurring patterns, quality checks. Retained general comms framework. Quality: 4→5.
- `jira-automation` — Merged the-block-jira-ticket-writer skill: Block Jira config (PRO/GD/DE/OP/BE project keys, component IDs, labels), ticket templates (Epic with Problem/Solution/Scope/Metrics, Design Story with [Design] prefix, Implementation Story with [Implementation] prefix), PRD-to-tickets workflow, real examples (PRO-4354 Sponsored Courses, PRO-3513 Job Board), quality checklist. Quality: 4→5.
- `sprint-roadmap` — Refocused as general PM sprint planning tool: capacity calculation, velocity tracking, RICE/MoSCoW/Impact-Effort prioritization with worked examples, backlog grooming workflow with JQL patterns, roadmap generation template, dependency mapping, release planning checklist. Quality: 4→5.
- `commit-checklist` — Expanded from stub to comprehensive skill: pre-commit validation checklist (security, code quality, completeness, scope), conventional commit message format with type reference table, good/bad examples, multi-commit strategy, full workflow with git commands. Quality: 3→5.
- `org-definition-of-done` — Expanded from stub to comprehensive skill: DoD templates for 4 work types (Feature, Bug Fix, Refactor, Spike), Release DoD with pre/deploy/post checklists, evidence-gathering workflow, status reporting format, customization guide for different team contexts. Quality: 3→5.
- `team-styleguide` — Expanded from stub to comprehensive skill: auto-detection from config files (ESLint, Prettier, tsconfig, .editorconfig, pyproject.toml), universal rules (naming, imports, comments, file structure), language-specific rules (TypeScript, Python, CSS/Tailwind), review workflow with pass/warn/fail output, style guide setup for new projects. Quality: 3→5.
- Skill count: 93 → 94 (+1 new etf-page-creator)
- All 94 skills now at Q:4-5 (100% quality threshold met)

## [3.5.0] - 2026-02-18

### Changed

- `health-habits` — Full rewrite with Sean's personal data: PPL split (Mon=Push, Tue=Pull/Arms, Wed=Legs/Abs, Thu=Push, Fri=Pull/Back, Sat/Sun=active recovery), 4:45 AM anchor schedule, 3-4 sets to failure training style, Apple Fitness → CSV pipeline via Shortcuts, XP/level gamification engine (10 levels from Recruit to Immortal, streak bonuses), Obsidian vault integration (daily note checkboxes, weekly summary), supplement stack tracking. Quality: 3→5.
- `personal-finance` — Full rewrite with Sean's financial data: Chase CSV parser (Transaction Date, Post Date, Description, Category, Type, Amount, Memo) + Bilt CSV parser (headerless quoted format), $5,741/mo net income baseline, 19 active subscriptions with keep/cancel status, 7 annual renewal dates, modified 50/30/20 budget framework (30% to debt+savings), debt paydown calculator with interest projection, 40+ Sean-specific regex merchant patterns, anomaly detection (Z-score). Quality: 5→5 (major content upgrade).
- `time-management` — Full rewrite with Sean's schedule: 4:45 AM→9 PM daily structure, 6-block energy map (PEAK post-workout, LOW 1-2 PM lull), 45/35/20 work split at The Block, Focus Day (Mon/Fri) vs Meeting Day (Tue-Thu), `/today` daily planning ritual, PEARL conflict resolution with personalized priority hierarchy, weekly time split review template, Google Calendar OAuth integration plan. Quality: 4→5.
- `life-admin` — Full rewrite with Sean's life context: Boston move March 21 checklist (15 tracked items), medical provider transition Medvidi→Aetna (7-step checklist with continuity of care documentation), address change tracker (financial, shopping, services, government, insurance), annual subscription renewal calendar, file organization audit workflow, Cannes France Sep 2026 trip planning. Quality: 3→5.

## [3.4.0] - 2026-02-17

### Added

- `daily-driver` — Daily personal assistant for morning planning, task prioritization, and EOD review. Integrates with Obsidian daily notes. 1-3-5 prioritization framework, carry-over tracking, weekly review.
- `subscription-audit` — Subscription and recurring expense auditor. Parses bank/credit card exports, identifies recurring charges, evaluates against free alternatives, outputs keep/replace/cancel decision matrix with savings projections.
- `analytics-workarounds` — Analytics data access workarounds for PMs without direct GA4/Looker access. Uses Zapier MCP as a data bridge to Google Sheets. Includes recurring pipeline setup patterns.
- `zapier-mcp-automation` — Master reference for ~175 Zapier MCP tools. Multi-tool workflow recipes (sprint kickoff, standup summary, weekly metrics), task budget optimization (each call = 2 tasks), cross-app automation chains.
- `vault-read-write`: added Multi-Source Synthesis Protocol (4-step framework: salient keywords, consensus, divergence, actionable takeaways; Consensus Matrix table format) and `/compress` session-end context handoff command — both merged from knowledge-management

### Changed

- `ai-creative-tools` — Full rewrite: replaced outdated "CLAUDE.md hooks" with real Claude Code PostToolUse hooks in settings.json format, removed hardcoded API keys (now env vars), added Hugging Face MCP integration (model search, Space inference, paper search), added ComfyUI queue script with polling, updated ElevenLabs to multilingual_v2 model, added asset index management and cross-references to related creative skills
- Skill count: 90 → 93 (+4 new, -1 deleted)
- Export group `02-pm-workflows`: added analytics-workarounds
- Export group `03-creative-projects`: added 2d-animation-principles (was missing from manifest)
- Export group `04-advanced-techniques`: added zapier-mcp-automation
- Export group `05-life-optimization`: added daily-driver and subscription-audit, removed knowledge-management

### Removed

- `knowledge-management` — Unique content (Synthesis Protocol, /compress) merged into vault-read-write. Remaining content (atomic notes, cross-linking, PKM organizing) fully covered by vault-architecture, knowledge-graph-nav, and vault-read-write.

## [3.3.0] - 2026-02-17

### Added

- `zapier-chrome-automation` — Zapier workflow automation combining MCP API actions with Chrome browser UI editing. Bridges the gap where MCP can query data but cannot edit Zap step configurations. Includes pre-flight account verification, editor UI patterns, and coordinated MCP+Chrome workflows.

### Fixed

- `security-reviewer` agent: replaced broken Cursor IDE tool names (`write`, `edit`, `search_replace`, `delete_file`, `run_terminal_cmd`) with correct Claude Code names (`Edit`, `Write`, `Bash`)
- `compliance-summarizer` agent: same Cursor→Claude Code tool name fix
- `data-analyst` agent: added missing `disallowedTools: [Edit, Write, Bash]` (was completely unrestricted)
- `game-design-advisor` agent: added missing `disallowedTools: [Edit, Write, Bash]` (was completely unrestricted)
- `python-automation` skill: fixed `title: string` (JS syntax) → `title: str` (Python syntax)

### Changed

- Skill count: 99 → 90 (+1 new, -10 consolidated)
- Agent security: 11/11 properly configured (was 6/11)
- `prd-generator`: added Quick Mode note (from quick-prd merge)
- `config-settings`: absorbed claude-md-optimization content (@import system, monorepo pattern, token budgets, CLAUDE.md vs Skills table, update cadence, security template)
- `stakeholder-update`: absorbed stakeholder-brief content (3 tone templates, 4 verification tests)
- `phaser-game-patterns`: absorbed phaser-pattern content (RN WebView bridge, StateMachine, LoadingScene, Common Gotchas)
- `sprite-asset-pipeline`: absorbed sprite-pipeline content (TexturePacker CLI, free-tex-packer, Aseprite CLI, pngquant/WebP, automation script, frame rates)
- `learning-accelerator`: absorbed learning-drill content (5 drill formats, 4-week progression, tracking log)
- `personal-finance`: absorbed budget-entry content (quick-entry formats, auto-categorization, integrations, monthly review)
- `supabase-backend`: absorbed supabase-python content (Python client setup, auth, queries)
- Updated 7 export-group manifests to remove references to deleted skills

### Removed

- 3 redundant skills (pure deletes): `safe-ops`, `org-security`, `quick-prd`
- 7 merged source skills (content transferred to targets): `supabase-python`, `claude-md-optimization`, `stakeholder-brief`, `phaser-pattern`, `sprite-pipeline`, `learning-drill`, `budget-entry`
- Orphan `plugin/skills/safe-ops/` directory

## [3.2.0] - 2026-02-16

### Added

- 6 new Adobe MCP skills for Creative Studio domain (Creative Studio: 15 → 21 skills):
  - `creative-director` — AI Creative Director for planning, interviewing, and critiquing visual projects. Includes critique rubrics and handoff protocol references.
  - `adobe-photoshop-mcp` — Photoshop image editing and compositing via adb-mcp UXP plugin. Includes MCP command reference.
  - `adobe-premiere-mcp` — Premiere Pro video editing and timeline automation via adb-mcp UXP plugin. Includes MCP command reference and editorial grammar (Murch's Rule of Six).
  - `adobe-aftereffects-mcp` — After Effects motion graphics and animation via adb-mcp CEP plugin (ExtendScript). Includes ExtendScript patterns reference.
  - `adobe-illustrator-mcp` — Illustrator vector graphics and SVG automation via adb-mcp CEP plugin (ExtendScript). Includes ExtendScript patterns reference.
  - `adobe-cross-app-workflows` — Cross-app pipeline orchestration, MCP architecture reference, shared guardrails, and troubleshooting.
- New export group: `12-adobe-creative` with all 6 Adobe skills

### Changed

- Skill count: 93 → 99
- Creative Studio domain: 15 → 21 skills

## [3.1.0] - 2026-02-15

### Added

- 3 new skills from Superpowers plugin deep merge:
  - `systematic-debugging` — Four-phase root cause debugging with 5 supporting reference files (root-cause-tracing, defense-in-depth, condition-based-waiting, find-polluter.sh)
  - `subagent-driven-development` — Fresh subagent per task with two-stage review (spec compliance + code quality), includes 3 prompt templates
  - `verification-before-completion` — Iron law: no completion claims without fresh verification evidence

### Enhanced

- `prd-generator` — Deep merged with Superpowers brainstorming: added HARD GATE (no code before design approval), one-question-at-a-time interview style, approach exploration (2-3 options with trade-offs), section-by-section approval for M/L scope
- `tech-spec` — Deep merged with Superpowers writing-plans: added bite-sized task structure (2-5 min RED-GREEN-REFACTOR steps), precision requirements (exact file paths, complete code, exact commands), plan header template, execution handoff (subagent-driven vs parallel session)
- `skill-system-mastery` — Deep merged with Superpowers writing-skills: added Claude Search Optimization (CSO), token efficiency targets, TDD-for-skills methodology (RED-GREEN-REFACTOR for skill creation), rationalization prevention patterns (HARD-GATE blocks, loophole closers, red flags)

### Changed

- Skill count: 89 → 93
- `export-groups/01-core-features/playground.json`: added `subagent-driven-development`
- `export-groups/04-advanced-techniques/playground.json`: added `systematic-debugging`, `verification-before-completion`

## [3.0.0] - 2026-02-08

### Architecture

- **Breaking**: Transformed from skill distribution system to personal command center / second brain
- All 89 skills now live at `.claude/skills/` (canonical, auto-loaded in this repo)
- All 11 agents live at `.claude/agents/` (7 domain + 4 new design team)
- `playgrounds/` renamed to `export-groups/` (metadata-only manifests for installer)
- `shared/agents/` removed (consolidated into `.claude/agents/`)
- Installer reads skill names from manifests, copies from `.claude/skills/`
- Stale `shared_agents`/`shared_hooks` fields removed from presets
- Preset JSON key `playgrounds` renamed to `export_groups`
- All manifest versions bumped to 3.0.0

### Added

- 6 domain workspaces with README, templates, reference materials, and scripts:
  - `claude-mastery/` — CLI, hooks, MCP, settings, tech stack (34 skills)
  - `product-management/` — PRDs, sprints, stakeholder comms (18 skills)
  - `creative-studio/` — Phaser, Remotion, sprites, pixel art (15 skills)
  - `life-systems/` — Finance, health, learning, tasks with 5 automation scripts (8 skills)
  - `design-team/` — Design system + 4 review agents (8 skills)
  - `vault/` — Obsidian vault with PARA structure (6 skills)
- 4 new design team agents (all read-only):
  - UI Reviewer — layout, spacing, color, typography, hierarchy
  - Accessibility Checker — WCAG 2.1 AA, contrast, keyboard nav, ARIA
  - Design System Enforcer — token compliance, naming, component patterns
  - Visual Polish Auditor — animations, loading/empty/error states, micro-interactions
- Obsidian vault with PARA structure, MOCs, Templates, Prompts library, RAG directory
- 5 Maps of Content (MOCs) linking to domain workspaces
- 4 Obsidian note templates (daily, project, meeting, idea)
- Life automation scripts: analyze_spending.py, health_audit.py, md_to_anki.py, organize_inbox.py, audit_calendar.py

### Changed

- `scripts/install.sh` v3.0.0: reads skill names from manifests, copies from `.claude/skills/`
- `scripts/install.ps1` v3.0.0: same changes
- `scripts/validate.py` v3.0.0: validates root .claude/, domains, vault, secret scanning across workspaces
- `CLAUDE.md`: rewritten for personal hub paradigm
- `README.md`: rewritten to reflect second brain architecture
- `.gitignore`: added vault and life-systems data patterns

### Removed

- `playgrounds/*/.claude/` subdirectories (skills moved to root .claude/)
- `playgrounds/` directory name (renamed to `export-groups/`)
- `shared/agents/` directory (agents consolidated into .claude/agents/)
- `shared_agents` and `shared_hooks` fields from presets (unused in v3 installer)

## [2.0.0] - 2025-02-06

### Architecture

- **Breaking**: Replaced tier-based packs (`packs/starter`, `packs/power`, `packs/enterprise`) with 11 domain-specific playgrounds
- New composable architecture: install individual playgrounds or use presets
- Old tier names preserved as presets (`presets/starter.json`, etc.)
- Enterprise is now a security profile applied on top of any preset, not a separate pack
- Templates folded into skill `references/` directories

### Added

- 11 domain-specific playgrounds with 89 total skills:
  - 01-core-features (12 skills): CLI, hooks, subagents, MCP, settings, skill system
  - 02-pm-workflows (13 skills): PRDs, tickets, stakeholder updates, data analysis
  - 03-creative-projects (7 skills): Phaser 3, sprites, pixel art, AI tools
  - 04-advanced-techniques (7 skills): multi-instance, context management, Plan Mode
  - 05-life-optimization (8 skills): finance, tasks, learning, health, time
  - 06-obsidian-integration (6 skills): vault architecture, MCP, semantic search
  - 07-technical-stack (9 skills): React, Python, Supabase, Git, Docker
  - 08-domain-specific (5 skills): crypto, education, API PM, RevOps, AI-native
  - 09-community-resources (6 skills): learning paths, troubleshooting, case studies
  - 10-master-designer (8 skills): animations, micro-interactions, Tailwind, Figma
  - 11-remotion-mastery (8 skills): video creation, typography, data viz, transitions
- `shared/` infrastructure: hooks, agents, and security profiles
- 4 presets: starter, power, enterprise, creative
- 2 security profiles: standard, enterprise
- `playground.json` manifest for each playground with dependencies
- `CLAUDE.section.md` composable fragments for CLAUDE.md generation
- New `scripts/install.sh` composable installer with `--preset`, `--security`, `--list` flags
- New `scripts/install.ps1` PowerShell equivalent
- New `scripts/validate.py` playground-aware validator (10 check categories)
- Creative preset for design/game-dev focused workflows
- 72 new skills generated from NotebookLM extraction pipeline

### Changed

- Install script: `install-pack.sh` replaced by `install.sh` with new CLI
- Validation script: `validate-pack.py` replaced by `validate.py` with playground checks
- Settings composition: installer builds `settings.json` from security profiles
- CLAUDE.md composition: installer concatenates playground section fragments

### Removed

- `packs/` tier-based directory structure (archived to `_archive/packs-v1/`)
- Standalone templates directory (folded into skill `references/`)
- Duplicate skills across packs (consolidated into canonical playgrounds)

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Claude Code Superuser Pack
- Three pack templates: starter, power, and enterprise
- Starter pack with 3 skills (team-styleguide, commit-checklist, safe-ops) and 2 hooks (block-secrets, log-tool-use)
- Power pack with 9 skills, 4 agents, 4 hooks, and 5 templates
- Enterprise pack with 3 skills, 2 agents, and 4 hooks (including require-confirm-highrisk)
- Installation scripts for Unix/macOS (install-pack.sh) and Windows PowerShell (install-pack.ps1)
- Validation script (validate-pack.py) to check JSON validity, required files, markdown headings, and secrets
- Plugin directory with safe, universal components
- Marketplace manifest (.claude-plugin/marketplace.json)

### Security
- block-secrets.py hook blocks edits to sensitive files (.env, **/secrets/**, etc.)
- require-confirm-highrisk.sh hook blocks risky Bash commands in enterprise pack
