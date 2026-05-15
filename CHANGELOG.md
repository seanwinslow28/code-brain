# Changelog

All notable changes to the Claude Code Superuser Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.35.0] - 2026-05-14

### Added

- **LLM Council integration** ([Phase A + B of the 3-phase plan](docs/superpowers/specs/2026-05-14-llm-council-integration-design.md)). New `tools/llm-council/` directory with two artifacts: (a) Karpathy's [llm-council](https://github.com/karpathy/llm-council) cloned unmodified to `tools/llm-council/upstream/` as a reference implementation + visible Karpathy attribution + browser-sidecar fallback (run `cd upstream && ./start.sh`); (b) a new headless Python package `tools/llm-council/council/` implementing the same fan-out → cross-rank → chairman pipeline against OpenRouter, invocable from inside Claude Code sessions. Two configurable profiles — `premium` (Claude Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, chairman Opus 4.7, ~$0.29 typical, $1.00 per-query cap, for stakes/synthesis) and `variance` (Claude Sonnet + GPT-5.4-mini + DeepSeek v4-pro + Qwen 3.5 Plus, chairman Sonnet, ~$0.12 typical, $0.40 per-query cap, for divergence-as-signal tasks like voice-mode calibration). Model IDs and per-query / daily / monthly cost caps are pinned in [`tools/llm-council/model-selection-2026-05-14.md`](tools/llm-council/model-selection-2026-05-14.md) (sourced from a captured OpenRouter inventory at `tools/llm-council/openrouter-models-snapshot-2026-05-14.json`). Spend is tracked atomically in `vault/health/council-spend-{YYYY-MM-DD}.json` and aggregated monthly across daily files with the same three-gate pattern as `gemini-deep-research` (per-query hard cap, $7/day circuit breaker, $40/month governor). Pipeline supports degraded mode: 1 of 4 Stage-1 models can fail and the council still produces a valid N-1 output; 2+ failures abort with a clear "fall back to single-model review" message. Cross-rank ranking JSON gets one parse-retry per judge; persistent JSON failures drop that judge from the ranking set without aborting. Phase C (extracting the pipeline as a public MCP server at `seanwinslow28/llm-council-mcp`) is explicitly deferred until 5–10 real runs validate the API surface. 32 pytest tests across `profiles`, `prompts`, `client` (with `pytest-httpx` mocking + 5xx retry semantics + 4xx no-retry on content_filter), `budget` (atomic spend writes via tmp+rename, day/month roll-up via glob), `pipeline` (happy path + degraded + chairman-failure-as-RuntimeError + cross-rank JSON retry + session JSON write), and `cli` (Click + rich rendering). One additional `tests/test_e2e.py` is `INTEGRATION=1`-gated for live OpenRouter smoke validation (~$0.05/run).
- **`llm-council` skill** at `.claude/skills/llm-council/` with trigger phrases (*"convene council"*, *"council critique"*, *"variance check"*, *"calibrate voice modes"*, *"stress-test this spec"*, etc.) and four workflow templates: voice-mode calibration (Substack pre-launch blocker — diff between Sean's draft and four blind variance-profile drafts is the calibration signal), cover letter / role-fit memo critique (premium), decision pre-mortem (premium), and PRD / spec stress-test (premium). Companion `decision-table.md` documents when to convene a council vs. use single-model Claude vs. delegate to `gemini-deep-research` vs. `last30days` vs. `skill_optimizer`.
- **First end-to-end use case shipped: voice-mode calibration.** Output lands in `vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/<YYYY-MM-DD>-<topic-slug>.md`, building a measurable record of voice-spec calibration over time. Sean re-runs weekly until convergence between blind drafts and his own draft is acceptable, then ships Substack.
- **Writing-voice-modes spec sharpening** (committed before the integration). Three new craft moves added to the cross-mode table: Reader-Dismissal (3 syntactic shapes — parenthetical / coda / mid-paragraph self-correction), Equation/Formula Defamiliarizer ("PM = You and Claude = Entire P&E department"), and Inverted Refrain (flipping a canonical refrain — "And so it begins" inverts Vonnegut's "So it goes"). The Domestic Defamiliarizer entry tightened to forbid precious-euphemism softening. Bad Vonnegut anti-pattern clarified: inversion counts as invention; verbatim copying does not. New cross-mode anti-pattern: "Desperation Posing as Self-Deprecation" — self-deprecation earns the right to observe others; naming the ask directly ("I need a job") collapses the move from earned-funny to needy-transactional. References/voice-samples.md expanded by 206 lines with corpus material backing the new moves.

### Changed

- Skill count: 118 → 119
- Root `.gitignore` adds `vault/health/council-spend-*.json` (private cost data)
- `CLAUDE.md` architecture comment now lists `tools/` as a new top-level directory alongside `.claude/`, `agents-sdk/`, `vault/`, `claude-mastery/`, `the-block/`, `creative-studio/`, `life-systems/`, etc.

### Credit

Heavy creative + architectural debt to [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council). His three-stage pipeline design (fan-out → anonymized cross-rank → chairman synthesis) is the load-bearing idea; our contribution is the headless CLI + skill wrapper + cost discipline + workflow templates calibrated to Sean's daily use. The original web app remains usable unmodified at `tools/llm-council/upstream/`.

## [3.34.0] - 2026-05-13

Vault Synthesizer v2 retrofit — Tier 1 (prompt + formatter + validator). Born from a 2026-05-13 morning diagnostic session where `scripts/query.py` proved the post-v3.33.0 synthesizer was producing shallow, cluster-biased, duplicate-prone output despite the eval suite passing 7/10. Root-cause read of `vault_synthesizer.py` surfaced a structural defect: `format_connection_article` hardcoded `"Evidence pending."` in every connection thread — the LLM was never given a chance to supply evidence. Tier 1 is the prompt-and-formatter-only fix that closes that gap; Tiers 2-4 (cluster-and-sample retrieval, EDC canonicalization, three-pass agentic synthesis) are specced and gated behind the Status Tracker in the retrofit plan doc.

### Added

- **Vault Synthesizer Retrofit Tier Plan** (`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`) — 9-section intent spec built using the `intent-engineering` skill template + four-tier implementation roadmap with file:line refs, exact diff summary, research citations (TopClustRAG SIGIR 2025, Anthropic quote-first prompting, Karpathy LLM Wiki, Extract-Define-Canonicalize, MA-RAG), and an append-only verification log for future Claude sessions to track nightly-run signal across tiers.

- **`_FORBIDDEN_PLACEHOLDERS` constant** (`agents-sdk/agents/vault_synthesizer.py`) — `("Evidence pending", "(to be filled)")` — defense-in-depth so any code path that still tries to emit placeholder copy gets caught by the validator instead of writing a shallow article.

- **`_load_existing_concept_titles(knowledge_root, cap=200)` helper** (`agents-sdk/agents/vault_synthesizer.py`) — reads frontmatter titles from `vault/knowledge/concepts/*.md` once per run for injection into the prompt's canonicalization block. Caps at 200 titles to bound prompt size. Loaded inside `run_synthesis()` before the per-file loop.

- **`_CROSS_DOMAIN_FOLDERS` tuple** (`agents-sdk/agents/vault_synthesizer.py`) — the five top-level vault folders (`00_inbox`, `10_timeline`, `20_projects`, `40_knowledge`, `05_atlas`) the synthesizer treats as distinct PARA-style domains for the cross-domain preference rule.

- **`evidence` parameter on both formatters** — `format_concept_article(evidence: list[str] | None = None)` renders verbatim quotes as a new `## Evidence` blockquote section. `format_connection_article(evidence: dict[str, list[str]] | None = None)` renders per-concept verbatim quotes under each thread.

### Changed

- **`_build_synthesis_prompt` rewritten end-to-end** (`agents-sdk/agents/vault_synthesizer.py`) — old prompt was ~50 lines, new prompt is ~110 lines. Three steering rules stated up top: **evidence-first** (every claim grounded in a verbatim quote, no quote → no claim), **reuse > remint** (existing concept titles injected verbatim into the prompt; LLM told to reuse the exact slug rather than mint a near-duplicate), **cross-domain > within-domain** (connections preferring concepts from different `_CROSS_DOMAIN_FOLDERS`). Similar-file excerpts grew 200 → 800 chars so the LLM sees arguments instead of fragments. Each similar file now carries an explicit `folder:` field so the model can identify cross-domain pairs. JSON schema gained `evidence` arrays per concept and per-concept-in-connection, plus a `source_folders: [string]` field on connections. Forbidden-phrase list (`Evidence pending`, `(to be filled)`) stated inline so the model knows what gets rejected downstream.

- **`format_connection_article` no longer hardcodes `"Evidence pending."`** (`agents-sdk/agents/vault_synthesizer.py`) — the bug that caused 111 connection articles on 2026-05-13 to ship with `Evidence pending.` in every thread. Now reads the per-concept evidence dict and renders verbatim quotes as blockquotes; falls back to `"_No verbatim evidence supplied._"` when a concept's evidence is missing — honest empty-state surface that lints clean on Sunday.

- **`format_concept_article` gained an `## Evidence` section** (`agents-sdk/agents/vault_synthesizer.py`) — renders verbatim quotes from source files between the existing `## Context` and `## Examples` sections. When `evidence=None`, surfaces `"_No verbatim evidence captured this run._"`.

- **`validate_article_body` rejects placeholder strings** (`agents-sdk/agents/vault_synthesizer.py`) — was previously a one-liner counting `≥2 wikilinks`; now also rejects any body containing `Evidence pending` or `(to be filled)`. Existing wikilink test (`test_validate_article_body_requires_two_wikilinks`) still passes because its fixtures don't contain forbidden strings.

- **`run_synthesis` call sites updated** (`agents-sdk/agents/vault_synthesizer.py`) — `_build_synthesis_prompt` now receives `existing_titles`; `format_concept_article` now receives `evidence=list(c.get("evidence", []))`; `format_connection_article` now receives a defensively-cast `connection_evidence: dict[str, list[str]]` parsed from the LLM's `evidence:` payload.

### Verification

- **All 13 `tests/test_vault_synthesizer.py` unit tests pass** including the existing format/validate/regenerate-index tests that don't pass the new `evidence` param (the optional parameter preserves backward compatibility at the call-site level).
- **62 tests pass across the synthesizer's neighborhood** (`tests/test_vault_synthesizer.py` + `test_synth_manifest.py` + `test_concept_edges.py` + `test_knowledge_lint.py`).
- **Eval suite stays at 7/10 (3 skipped)** — same baseline as v3.33.0. No regression.

### Operator-action required

- **None for Tier 1 itself.** The retrofit is contained entirely within `agents-sdk/agents/vault_synthesizer.py`. No new dependencies, no schema changes, no config changes. Rollback = `git checkout agents-sdk/agents/vault_synthesizer.py`.
- **First real signal arrives 2026-05-14 02:30 AM** when launchd fires the nightly synth. Check `vault/health/synth-manifest-2026-05-14.json` (`status: ok`, `concepts_written > 0`), `grep -rn "Evidence pending" vault/knowledge/ | wc -l` should be 0 after regen, and re-run the cluster-diversity `query.py` diagnostic to see if consulted chunks now span ≥2 different top-level vault folders.

### Tiers 2-4 (pending)

- **Tier 2 — Cluster-and-sample retrieval (TopClustRAG)**: replace `retriever(primary_text[:2000], top_k=5)` with top-50 cosine → HDBSCAN clustering → 2-3 chunks per cluster. Adds `hdbscan` pip dependency. Estimated 4 hrs. Trigger: Tier 1 has 3 successful nightly runs AND `query.py` still shows densest-cluster bias.
- **Tier 3 — EDC canonicalization**: pre-write embedding cosine check against existing concepts; merge at >0.85, LLM-judge at 0.70-0.85, new file at <0.70. Adds `concept_canonicalize.py` lib + `alias_of` column on `concept_edges`. Estimated 4 hrs. Trigger: Tier 2 stable AND slug-dupe count still trending up.
- **Tier 4 — Three-pass agentic synthesis (MA-RAG / TopClustRAG full topology)**: per-cluster draft → cross-link → lint. Estimated 8 hrs. Trigger: post-employment only — do not ship under sprint pressure.

Full plan + Status Tracker at [vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md).

## [3.33.0] - 2026-05-12

Vault Synthesizer Eval Suite — Workstream B (synthesizer patches) + Workstream C (Substack-Drafter agent). Builds on v3.30.1's Workstream A eval-suite ship. The suite went from baseline 1/10 (the regression suite working as designed at A's ship) to post-fix 7/10 in one work session. The Substack-Drafter agent is a new SDK agent that closes the publishing-cadence loop for Sean's job-hunt sprint — default-disabled at three kill-switch layers so it ships ahead of the original "post-employment" schedule without risk.

### Added

- **Substack-Drafter agent** (`agents-sdk/agents/substack_drafter.py`) — Thursday-18:00 weekly agent (default-disabled, opt-in via `INSTALL_SUBSTACK_DRAFTER=1`) that reads post-fix synthesizer output, picks the densest concept cluster via wikilink density (≥3 shared wikilinks pairwise), and drafts a Substack post in a rotating 5-mode voice cycle (sean → sedaris → kerouac → thompson → vonnegut, indexed by absolute weeks since `voice_epoch = 2026-05-04`). Never publishes; drafts land in `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/` for hand review. Three kill-switch layers: (1) `enabled = false` default in `[substack_drafter]` config table; (2) opt-in launchd install via `INSTALL_SUBSTACK_DRAFTER=1` env var; (3) `--dry-run` CLI flag prints the composed prompt without calling the model. 33 TDD tests covering voice rotation, dryness gate (no-op when last N synth-manifests show `concepts_written == 0`), cluster picker (largest connected component with wikilink overlap), prompt composer (loads `writing-voice-modes/SKILL.md` verbatim, graceful degradation if missing), draft writer (frontmatter: type/voice/source_concepts/generated_at/model_used/cost_usd/status), and main() flow with all branches covered. `_route()` is wired to the real HybridRouter API: loads config, creates `HybridRouter.from_config()`, calls `asyncio.run(router.route(task))`, handles both ollama (`/api/generate`) and OpenAI-compatible (`/v1/chat/completions`) runtimes via httpx.

- **`[substack_drafter]` config table** (`agents-sdk/config.toml`) — defaults pinned for Sean's local-Qwen3-14B-first / Sonnet-fallback HybridRouter cost profile: `max_cost_usd = 0.10` hard cap, Thursday 18:00 schedule, `synthesizer_dry_threshold = 3` nights for graceful no-op, `voice_epoch = 2026-05-04`, output_dir pointing at the existing substack-drafts/ folder.

- **`agents-sdk/schedules/com.sean.agents.substack_drafter.plist`** + opt-in install path in `install_schedules.sh`. Mirrors the `INSTALL_GEMINI=1` pattern. Schedule: Thursday 18:00 weekly (`Weekday=4, Hour=18, Minute=0`). `EnvironmentVariables.PATH` preserved per CLAUDE.md non-negotiable.

- **Vault Synthesizer Eval Suite — Workstream B completion** (`evals/vault-synthesizer/`) — suite went from baseline 1/10 (10%) at Workstream A ship to **7/10 (70%) post-fix**. Three cases explicitly skipped with `skip_reason` fields naming the real blockers: vs-014 needs live-LLM infrastructure (output-completeness can't be faithfully mocked); vs-012/013 need eval-mechanics work (English-prose `pass_criteria` → Python, runner concept-body reader path, age-fixture machinery). README baseline section updated with pre-fix vs post-fix narrative. Roadmap Task 8 (build plan) marked ✅ for Steps 2+3; Step 4 rephrased with concrete 5-night gate dates. Roadmap Task 9 (Substack-Drafter) status changed from "POST-EMPLOYMENT BUILD" to "EARLY-BUILD APPROVED 2026-05-12" with rationale.

### Changed

- **Vault synthesizer status taxonomy** (`agents-sdk/agents/vault_synthesizer.py`) — added `STATUS_SUCCESS_EMPTY` and `STATUS_PARTIAL_EMPTY` to the `STATUS_VALUES` frozenset, distinguishing "healthy and quiet" (all per-file calls succeeded but no articles passed validation) from "broken and quiet" (some calls failed AND no articles produced). New per-file `files_attempted` / `files_succeeded` counters drive an end-of-loop run-level status promotion: `0 succeeded → STATUS_ERROR`, `partial + zero output → STATUS_PARTIAL_EMPTY`, `partial + some output → STATUS_PARTIAL`, `all succeeded + zero output → STATUS_SUCCESS_EMPTY`, `all succeeded + output → STATUS_OK`. Composes correctly with the existing budget-timeout path. Turns eval cases vs-015, vs-016, vs-017 green.

- **`SynthesisResult.model_used`** (`agents-sdk/agents/vault_synthesizer.py`) — defaults to `"none"` instead of empty string. Valid enum exposed as `MODEL_USED_VALUES` frozenset: `{"qwen3-14b", "claude-sonnet-4-6", "claude-haiku-4-5", "none"}`. New `_normalize_model_name()` helper maps raw model strings (with version suffixes like `claude-sonnet-4-6-20251029`) into the enum on successful calls. Turns eval case vs-018 green.

- **Pushover boot-time credential check** (`agents-sdk/lib/pushover.py`) — added `PushoverConfigurationError` class + `ensure_credentials_or_raise()` function. Called at the top of `run_synthesis()`. Honors `PUSHOVER_USER_KEY` / `PUSHOVER_API_TOKEN` env-var overrides first, then falls back to macOS keychain. Missing creds now fail loud at boot instead of producing ~40 silent-log retries per night (the original Mode 5 regression). Turns eval case vs-019 green. ⚠️ **Operator action required**: macOS keychain must contain Pushover credentials (or env vars must be set in the launchd plist) before merging — otherwise the live synthesizer will fail at boot every night. This is the correct failure mode (the whole point of the fix) but needs operator awareness.

- **Daily-driver Vault Health WARNING** (`agents-sdk/agents/daily_driver.py`) — new `render_vault_health(manifest: dict) -> str` standalone helper surfaces `success-empty` / `partial-empty` status values OR `concepts_written == 0` manifests as `⚠️ WARNING` blocks in the morning brief. Replaces the prior count-only inline rendering inside `build_preamble()`. Turns eval case vs-021 green.

- **CLAUDE.md agent count** updated from "16 autonomous SDK agents" / "8 of 16 on launchd" to "17 autonomous SDK agents" / "8 of 17 on launchd" reflecting the Substack-Drafter addition.

### Fixed

- **Eval runner conftest hooks** (`evals/vault-synthesizer/conftest.py`) — `pytest_runtest_logreport` and `pytest_sessionfinish` moved out of `runner.py` (where pytest doesn't auto-register hooks from a parametrized test module) into `conftest.py` (where it does). `last-run.md` now auto-generates on every invocation instead of requiring manual capture.

- **Existing synthesizer/pushover/daily_driver tests** — 8 tests across `test_vault_synthesizer.py` and `test_daily_driver.py` updated to assert the post-fix corrected behavior (one was asserting the old silent-empty bug; the others needed the `_stub_pushover_creds` autouse fixture so they don't trip the new boot check). Full suite: 504 passing, 3 pre-existing failures unrelated to this work (`test_job_feed_e2e`, `test_route_to_macbook` x2).

### Branch and merge state

This entry summarizes 23 commits on branch `eval-suite-2026-05-12` (Workstream B's 8 + Workstream C's 8 + 7 doc/scaffold/baseline commits). The branch is ready to merge once Sean accepts the Pushover operator-action requirement.

## [3.32.0] - 2026-05-11

SessionEnd auto-stub for new person wikilinks. Closes the regression risk Sean asked about: "if a new article lands with a new `[[Author Name]]` not in the people folder, will it show up in the broken-wikilink section every Sunday?" Answer is now no — at the end of every Claude Code session, a fire-and-forget hook scans the vault for unresolved `[[Name]]` wikilinks in `author:` YAML frontmatter fields and creates minimal stubs before the next morning's Daily Driver fire.

### Added

- `agents-sdk/scripts/auto_stub_people.py` — pure-Python utility, no Claude SDK in the loop. Two filters protect against creating garbage stubs:
  1. **Author-field signal**: the wikilink must appear inside a `author:` YAML frontmatter list (single-value inline form `author: "[[X]]"` or multi-line list form). Body-text wikilinks, `related:` fields, and any other location are ignored. This is the structured signal that the value is a person and not a typo / citation marker / folder reference.
  2. **Person-name shape**: target must match `^[A-ZÀ-Ý][A-Za-zÀ-ÿ.'\-]*( [A-ZÀ-Ý][A-Za-zÀ-ÿ.'\-]*){0,2}$` — 1-3 capitalized tokens with optional middle initials, hyphens, apostrophes, and latin diacritics. Accepts "Ali Çevik", "RT Watson", "Mary-Alice McKee", "J.J. Smith". Rejects "stage", "intent-engineering", "10", "prj-job-hunt-2026", lowercase strings, empty targets.
  Stubs land at `vault/40_knowledge/people/<slug>.md` (slug = ASCII-folded lowercase with hyphens). Existence dedup checks both filename (`<slug>.md`) and `title:` frontmatter, so the same person under a different filename slug is never duplicated. Self-recursion guard: the scan skips the `40_knowledge/people/` folder so stubs referencing other people don't generate cascading stubs. Per-run safety cap: `_MAX_STUBS_PER_RUN = 10` — if exceeded, the run logs and creates nothing (defends against bulk-import scenarios where the filters might over-fire). Stub frontmatter includes `status: unverified` and a body line prompting Sean to fill in identity when he next encounters the person.
- `.claude/hooks/session-end-auto-stub.sh` — SessionEnd hook wrapper. Fire-and-forget detached background process via `nohup ... &` + `disown`. Returns <100ms so session close isn't blocked. Recursion guard via `CLAUDE_INVOKED_BY=auto-stub` matches the existing `session-end-flush.sh` pattern. Output captured at `vault/90_system/agent-logs/session-end-auto-stub.log` (last-run stdout/stderr) plus a structured append-only log at `vault/90_system/agent-logs/auto-stub-people.log` (timestamped CREATED / WOULD CREATE / SAFETY entries).
- `.claude/settings.json` — second entry in `SessionEnd.hooks[].hooks[]` registering the new wrapper alongside the existing flush. Both fire on the same event; flush extracts knowledge from the just-ended transcript, auto-stub patches up the wikilink graph based on what's accumulated in the vault. Hook count `13 → 14`.
- `agents-sdk/tests/test_auto_stub_people.py` — 15 new test cases covering both filters (positive + negative for author-field detection and person-name shape), dedup against existing stubs (filename + title), recursion skip of `40_knowledge/people/`, `node_modules` exclusion, dry-run mode, per-run safety cap engagement, and slugification of diacritics. Full suite passes 15 / 15.

### Verified live

- Initial dry-run against the live vault surfaced one new candidate I'd missed in the v3.31.0 manual sweep: `[[Lenny Rachitsky]]`, referenced from three `vault/00_inbox/` clips (Not all AI agents are created equal, How I built LennyRPG, Your Couch-to-5K for AI). Live run created `vault/40_knowledge/people/lenny-rachitsky.md` with the unverified-stub template. `find_broken_wikilinks(vault)` still returns 0 — the new clips' wikilinks now resolve through the stub. Confirms the script does what v3.31.0 did manually, but automatically.

### Rollback

Disabling is a one-line change: remove the `session-end-auto-stub.sh` entry from `.claude/settings.json` SessionEnd block. Existing stubs stay. Re-enable with a one-line add. Or set the safety cap to 0 for a softer kill-switch.

### Note on numbering

This entry was authored on the Mac Mini as v3.28.0 in parallel with the MBP's v3.28.0 (job-feed agent). On 2026-05-11 sync, the local 3.27.0 → 3.28.0 stack was renumbered to 3.29.0 → 3.32.0 to clear the MBP's already-pushed version numbers.

## [3.31.0] - 2026-05-11

Broken-wikilink cleanup sweep. Took the lint signal from 37 (post-filter from v3.30.0) → 0 by fixing the remaining real issues and adding one more lint exclusion. Net result of v3.30.0 + v3.31.0 together: **348 → 0 broken wikilinks**, every link in the vault now resolves and every previously-orphan target is a real node the synthesizer can cluster on.

### Added

- `vault/40_knowledge/concepts/intent-engineering.md` — concept hub. Pointer to the `.claude/skills/intent-engineering/SKILL.md` source + listing of the 10+ inbound `ref-*` notes in `vault/40_knowledge/references/intent-engineering/`. Resolves all 11 stale `[[intent-engineering]]` wikilinks in one file.
- `vault/40_knowledge/concepts/writing-voice-modes.md` — concept hub. Pointer to the `.claude/skills/writing-voice-modes/SKILL.md` source. Resolves the 1 stale `[[writing-voice-modes]]` wikilink from `vault/05_atlas/operating-models/job-hunt-2026/operating-model.md`.
- `vault/40_knowledge/people/` — new folder with 10 person stubs: `nate.md` (Nate Jones / OB1 author — primary external thought-leader cited in Sean's research, 8 inbound refs), `rt-watson.md` (The Block, 2 refs), `daniel-kuhn.md` (crypto journalism, 2 refs), `yogita-khatri.md` (The Block, 1 ref), `ali-cevik.md` (Google Gemini API, 1 ref), `lukas-haas.md` (Google DR Max, 1 ref), `vivek-trivedy.md` (LangChain, 1 ref), `timmy-shen.md` (The Block, 1 ref), `callum-howe.md` (1 ref), `brian-danga.md` (Stripe, 1 ref). Each stub uses `title:` frontmatter matching the wikilink target so `[[Nate]]` / `[[RT Watson]]` etc. resolve via the existing title-fallback resolver. Resolves the 24 person-name `broken-wikilink` flags. Anyone whose identity wasn't confidently derivable from byline context is marked "Identity beyond the byline is unverified."

### Fixed

- `agents-sdk/agents/knowledge_lint.py:_vault_md_files` — added `node_modules` to the directory exclusion set alongside `.obsidian` / `.trash` / dotfiles. Kills the `[[String]]` false positive coming from a vendored npm package README inside `30_domains/product-management/the-block-resume-info/.../data-explorer-server/node_modules/optionator/`. Prevents future pollution from any vendored JS dependencies left in the archive.
- `vault/05_atlas/operating-models/life-systems/SOUL.md:139` — removed stray `\` before `|` in `[[Sean-Winslow-Full-Personal-Context-v2.0\|Full Personal Context]]`. The backslash was a Markdown escape that the lint regex captured as part of the target. Obsidian was rendering correctly; lint was wrong about brokenness, but cleaning the link is more durable than special-casing the regex.
- `vault/40_knowledge/concepts/research-hermes-agent-investigation-2026-04-26.md:10` — `[[hermes-agent-investigation-prompt]]` → `[[ref-hermes-agent-investigation-prompt]]`. Real target lives at `vault/40_knowledge/references/ref-hermes-agent-investigation-prompt.md`; the inbound link was missing the `ref-` prefix.
- `vault/20_projects/prj-job-hunt-2026/README.md` — two changes: (1) added `title: "prj-job-hunt-2026"` frontmatter so `[[prj-job-hunt-2026]]` resolves via title-fallback (the README is the project hub); (2) rewrote the broken folder-target link `[[onwards-and-upwards-5-4-26]]` on line 33 to `[[2026-05-04-onwards-and-upwards-plan]]`, pointing at the actual canonical master plan inside that folder.
- `vault/40_knowledge/references/intent-engineering/ref-personal-agentic-intent-engineering.md:19` — `[[20_projects/prj-job-hunt-2026]]` → `[[prj-job-hunt-2026]]`. The path-style target was a wrong shape for Obsidian's resolver; the basename form now resolves through the title frontmatter added to the README.
- `vault/40_knowledge/references/ref-stripe-2025-annual-letter-agentic-commerce.md:5` — replaced `author: - "[[stage]]"` with `author: - "Stripe"`. The `[[stage]]` was a web-clip artifact (the clipper grabbed "stage" from page metadata as the author), not a real wikilink.

### Verified

- `find_broken_wikilinks(vault)` on the live vault returns `0` issues. Down from 348 pre-v3.30.0.
- 25/25 knowledge_lint tests pass (no regressions to existing test cases).

## [3.30.1] - 2026-05-12

### Added
- **Vault Synthesizer Eval Suite (`evals/vault-synthesizer/`)** — 10-case binary
  pass/fail eval suite + companion synthesizer-fix workstream. Ships intentionally
  red: 6 new cases (vs-016..vs-021) grounded in 17 days of real production logs
  drive the regression-test discipline that Workstream B's patches will turn
  green. 4 retained cases (vs-012..vs-015) from pre-drafted research. 11 deferred
  cases (vs-001..vs-011) waiting on the synthesizer fix. Baseline pass rate at
  ship: 1/10 (10%) — by design. Target post-fix: 7+/10.

## [3.30.0] - 2026-05-11

Knowledge Lint broken-wikilink scan tightened — dropped 348 issues to 37 (89% reduction) by filtering out two well-understood noise sources that swamped the signal.

### Fixed

- `agents-sdk/agents/knowledge_lint.py` — `find_broken_wikilinks` now skips two categories of false-positive `[[X]]` matches before reporting:
  - **Numeric citation markers** (`[[10]]`, `[[42]]`, etc.): research notes from Gemini DR and the local LDR pipeline write footnote/bibliography references in `[[N]]` form. The regex `\[\[([^\]|#]+)...\]\]` can't tell `[[Sponsored Course Implementation Kick-off]]` from `[[10]]`. New `_CITATION_TARGET_RE = re.compile(r"^\d+$")` filters them out at scan time. This bucket was 255 of the 348 issues (73%) — almost entirely concentrated in `vault/20_projects/research/`.
  - **Granola meeting archive**: new `_BROKEN_LINK_EXCLUDE_DIRS = {"the-block-meetings-granola-notes"}` plus `_is_broken_link_excluded(rel_parts)` helper skips this folder entirely. The Granola transcripts were slug-renamed at some point (e.g. `Alex_Sean sync.md` → `mtg-2026-03-XX-alex-sean-sync.md`) but the internal cross-references inside each note still point at the pre-rename names. This archive is read-only post-2026-05-04 Block layoff — fixing the lint scope is the right call, not rewriting archived data. 57 of the 348 issues (16%).

### Added

- Two new tests in `agents-sdk/tests/test_knowledge_lint.py`: `test_find_broken_wikilinks_skips_numeric_citation_markers` and `test_find_broken_wikilinks_skips_granola_archive`. Existing test for real broken wikilinks unchanged. All 25 knowledge_lint tests pass.

### Diagnosed (no code change)

- **Missing 2026-05-03 Sunday lint run** investigated. Root cause: Mac Mini was powered off / asleep from Sunday 2026-05-03 17:09 through Monday 2026-05-04 ~08:54 — confirmed via `vault/90_system/agent-logs/agent-run-history.csv` showing zero scheduled-agent activity in that window. Five overnight jobs missed (knowledge-lint Sun 22:00; vault-indexer / synthesizer / deep-researcher Mon 02:00-02:45; daily-driver morning Mon 08:45) — the gap is bracketed by the 5/3 17:09 gemini-dr run and the first 5/4 08:54 SessionEnd flush. The launchd plist (`~/Library/LaunchAgents/com.sean.agent.knowledge-lint.plist`) and stderr log (`vault/90_system/agent-logs/knowledge-lint-stderr.log`) are both clean — only two clean runs logged (4/26 and 5/10), no crash trace for 5/3. macOS `LaunchAgents` with `StartCalendarInterval` do NOT catch up missed windows when the machine is unavailable, so the 5/3 slot is gone. Timing matches the 2026-05-04 Block layoff day disruption — this is a one-time event, not a recurring fault. All subsequent Sundays (5/10) have fired correctly.

## [3.29.0] - 2026-05-11

Fleet output consolidation — the daily note now surfaces every agent's overnight activity in one glance. Sean keeps the daily note open on his desktop all day, but until now the only fleet output visible there was the Daily Driver's own morning brief; everything else (synthesizer manifest, knowledge lint report, fleet status snapshot, new research notes, new concept/connection articles) was scattered across `vault/health/`, `vault/02_Areas/Agent-Fleet/`, `vault/knowledge/`, and `vault/20_projects/research/` with no breadcrumbs back into the daily note. This change routes everything through the daily note.

### Added

- `agents-sdk/lib/fleet_summary.py` — new helper. `build_fleet_overnight_digest(repo_root, vault_root)` reads the last 24h of `vault/90_system/agent-logs/agent-run-history.csv`, the latest `vault/health/synth-manifest-*.json`, and the latest `vault/health/*-lint-report.md` to produce a 7-line markdown digest (one line per active agent with status badge + notes snippet) plus a "Deep links" footer. Meta-agent is special-cased — it reads the CSV but doesn't write to it, so the helper uses today's `daily-fleet-status-*.md` existence as the success proxy. Empty/missing inputs degrade gracefully (no run → "no run in last 24h"; missing manifest/report → footer line omitted).
- `vault/90_system/templates/tpl-daily.md` — two new top-of-note sections. **Fleet Overnight Digest** (`<!-- fleet-overnight -->` anchor) gets filled by Daily Driver at 08:45 with the helper's output. **Fleet Activity Today** holds four Dataview blocks that auto-refresh as agents write files throughout the day: (1) today's `daily-fleet-status-*.md`, (2) new files in `knowledge/concepts/` or `knowledge/connections/` (last 24h), (3) new files in `20_projects/research/` (last 24h), (4) the latest `vault/health/*-lint-report.md`.
- `vault/10_timeline/daily/2026-05-11.md` — backfilled with the new sections so the change is visible immediately (without waiting for tomorrow's 8:45 Daily Driver fire).

### Changed

- `agents-sdk/agents/daily_driver.py` — morning mode now computes the fleet digest via `build_fleet_overnight_digest` and adds a Step 4 to the task prompt: "Locate the placeholder line under `<!-- fleet-overnight -->` and REPLACE it with this exact block, verbatim." Block is fenced by `<<<FLEET_DIGEST_BEGIN>>>` / `<<<FLEET_DIGEST_END>>>` markers so Claude has unambiguous boundaries. Existing Steps 4 → 5 renumbered (1-3-5 plan is now Step 5). Prompt cost increase: ~150 tokens — well within the $0.60 morning cap (last run was $0.5513).

### Rationale

The producer side of the fleet (the 7 active agents) is currently well-tuned and the consumer side (Sean reading their output) was the bottleneck. Putting every agent's output one scroll away on the always-open daily note closes that gap without adding any new agents, schedules, or notification channels. Dataview blocks were chosen over file-watcher / notification approaches because they're already installed in Sean's Obsidian, render live on the desktop, and require zero new moving parts.

## [3.28.0] - 2026-05-11

Job-feed agent — autonomous PM/APM role discovery wired into the morning brief.

### Added

- **Job-feed agent (autonomous SDK agent #8 on launchd)** — daily PM/APM role discovery from 4 free public feeds (RemoteOK, HN "Who's Hiring", web3.career, WeWorkRemotely) plus a ~40-company ATS watchlist (Greenhouse/Lever/Ashby auto-detect). Rules-filters with regex/YOE/geo/salary hard cuts, scores survivors with Qwen3-14B on MBP via HybridRouter (`fallback_disabled=true`; no cloud egress on MBP-asleep — postings carry over to next run), persists to standalone `vault/.job-feed.db`, renders Markdown roll-up to `vault/20_projects/prj-job-hunt-2026/job-feed/<today>.md`, and surfaces a 3-line summary block in the daily-driver morning brief. launchd schedules 7 fires from 8:00–11:00 AM ET to handle MBP-asleep catch-up via the roll-up's `complete: true` idempotency frontmatter. $0/run.
  - New SDK agent: `agents-sdk/agents/job_feed.py`
  - New lib modules: `agents-sdk/lib/job_types.py`, `job_sources.py`, `job_rules.py`, `job_db.py`, `job_scoring.py`, `job_renderer.py`
  - New CLI helper: `agents-sdk/scripts/update_status.py`
  - New launchd plist: `agents-sdk/schedules/com.sean.job-feed.plist`
  - New seed file: `vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml` (~40 companies)
  - Spec: `docs/superpowers/specs/2026-05-09-job-feed-agent-design.md`
  - Plan: `docs/superpowers/plans/2026-05-11-job-feed-agent.md`

### Changed

- `CLAUDE.md`: SDK agent count `15 → 16`; added Job Feed row to the active-agents table; "Active agents (7 of 15 on launchd; 1 manual-trigger)" → "Active agents (8 of 16 on launchd; 1 manual-trigger)".
- `README.md`: same count bump in the masthead paragraph.
- `agents-sdk/agents/daily_driver.py`: morning preamble now appends a Job Feed summary block (top-3 fits or "scoring deferred" banner) before the vault-health section when a roll-up exists for the day.

## [3.27.0] - 2026-05-10

**`skill_optimizer.py` — autoresearch optimization harness for Claude Code skills.** First one-skill prototype validated against `.claude/skills/writing-voice-modes/SKILL.md`. Adapted from Karpathy's autoresearch pattern (March 2026): mutable artifact (the body of `SKILL.md` with frontmatter + example outputs + meta-navigation sections protected by a pre-write diff guard), fixed infrastructure (orchestrator + eval YAML + judge prompt template + structural-check Python), and English-language instructions for a mutation subagent. Generation runs on Opus 4.7; LLM judging runs locally on Qwen3-14B (via Ollama on Mac Mini) with Sonnet 4.6 sample-checks every 5 iterations. Decision rule is 3-iteration moving average with bootstrap-CI keep/revert. Six anti-Goodhart trip-wires + held-out validation set + sealed surprise prompts to detect drift.

### Added

- **`agents-sdk/agents/skill_optimizer.py`** (~510 lines) — orchestrator + CLI entry. Loads `[agents.skill_optimizer]` config from `agents-sdk/config.toml`, runs the optimize→measure→keep-or-revert loop. Each kept iteration writes one row to `data/skill-optimizer/writing-voice-modes-results.tsv` and one git commit on the `autoresearch/writing-voice-modes-2026-05-09` branch. Manual-trigger (no launchd plist).
- **`agents-sdk/lib/skill_optimizer/`** — six pure-function modules:
  - `structural_checks.py` — 3 deterministic eval criteria: `substack_format_intro` (60-180 word first paragraph + ≤12 word closer), `anti_pattern_overreference` (no sensory noun >2 times), `stylometric_distance` (z-score distance from Sean's corpus + n-gram match penalty).
  - `stylometry.py` — feature extraction (sentence length, comma density, em-dash density, first-person frequency), distinctive n-gram extraction, distance computation, baseline JSON I/O.
  - `mutation_guard.py` — pre-write diff validator: rejects edits to protected line ranges (frontmatter + example outputs), protected sections (References, Related Skills, Copy/Paste Ready), whitespace-only diffs, and headings introduced that match a criterion ID verbatim (anti-gaming).
  - `decision.py` — moving average + bootstrap CI + keep/revert decision rule.
  - `tripwire.py` — 6 anti-Goodhart safety checks (train-holdout divergence, criterion uneven drift, stylometric drift, diversity collapse, judge disagreement, complexity ratchet).
  - `judge_runner.py` — `JudgeRunner` class wrapping Qwen3-14B (via Ollama HTTP, 300s timeout, 2 retries on `ReadTimeout`) and Sonnet 4.6, with `judge_single`, `judge_ensemble` (3-judge majority vote with shuffled anchor pairs + seeds), and `compute_sonnet_agreement`.
- **`.claude/skills/writing-voice-modes/evals.yaml`** — 5 training prompts + 2 holdout prompts + 3 structural criteria + 3 LLM-judge criteria + scoring config.
- **`.claude/skills/writing-voice-modes/evals.sealed.yaml`** — 3 sealed surprise prompts the optimizer never sees, scored every 5 iterations.
- **`agents-sdk/lib/skill_optimizer/program.md`** — natural-language instructions for the mutation subagent. Uses a delimited-block output format (`<<<MODIFIED_SKILL_MD>>>...<<<END_MODIFIED_SKILL_MD>>>`) so multi-line markdown bodies don't need JSON-escaping.
- **`agents-sdk/lib/skill_optimizer/judge_prompt.txt`** — judge template with output-first / anchors-after-output ordering to reduce anchor-priming bias.
- **`agents-sdk/scripts/build_stylometry_baseline.py`** + **`agents-sdk/scripts/calibrate_stylometry_threshold.py`** — pre-flight builders. Calibration uses 13 real-Sean corpus chunks + 15 generic-AI Opus generations; threshold tuned via TPR-FPR maximization to **7.57** with TPR-FPR = 0.62 (well above the 0.4 floor).
- **`agents-sdk/data/skill-optimizer/`** — `stylometry_baseline.json` (5 features + 30 distinctive n-grams + threshold), `calibration_set.jsonl` (28 labeled examples Sean reviewed and approved 2026-05-09), `writing-voice-modes-results.tsv` (one row per kept iteration).
- **`[agents.skill_optimizer]` block in `agents-sdk/config.toml`** — 26 keys covering paths, models, iteration cap, runs/prompt, cost caps.
- **89 unit tests** total across 7 module test files.
- **2 60%-professional-dial samples** appended to `.claude/skills/writing-voice-modes/references/voice-samples.md` (Slack delayed-launch + sprint-outcome stakeholder update) for cross-functional dial calibration.

### First live run results (2026-05-10, branch `autoresearch/writing-voice-modes-2026-05-09`)

- **`max_iterations=10, runs_per_prompt=15`** (option-1 budget; the plan's 25-iter / 15-runs default would have been ~25-50 hours wall-clock).
- **1 kept iteration** (commit `173e1c6`), **9 mutation-proposal failures** caught by fail-soft handling. Wall-clock 127 min.
- **Iteration 1 score**: train 0.7267 / holdout 0.7778 / decision keep. Mutation: tightening `## Sean's Signature Moves` table.
- **Per-criterion**: `substack_format_intro` 0.36 and `stylometric_distance` 0.40 below the 0.60 floor (real signal — the optimizer has work to do here); `anti_pattern_overreference` 0.79; LLM-judge criteria all 1.00 (likely Qwen3-14B leniency; Sonnet sample-check at iter 5 would have flagged this but iters 2-10 didn't reach scoring).
- **Halt reason**: iteration cap (10 reached). No tripwires fired.
- **Three real bugs surfaced + fixed during validation**:
  1. `_build_snapshot` call site was missing `holdout_history` and `diversity` args (commit `92ad279`, caught by Task 5.1 dry-run).
  2. `_OllamaClient.complete` had a hardcoded 120s timeout with no retry — caught by a 49-min `httpx.ReadTimeout` in the first live attempt; bumped to 300s + 2 retries with exponential backoff (commit `0f09e9c`). Same commit wraps the iteration body in try/except for fail-soft on transient errors.
  3. `propose_mutation` JSON parser broke on un-escaped multi-line markdown — caught by the 9-of-10 iteration failures in the second live attempt; replaced with a delimited-block format that never asks Opus to JSON-escape body content (commit `190c686`, with 5 new unit tests). Backward-compatible JSON fallback retained.

### Changed

- `CLAUDE.md`: SDK agent count `14 → 15`; added Skill Optimizer row to the active-agents table; "Active agents (7 of 14)" → "Active agents (7 of 15 on launchd; 1 manual-trigger)".
- `README.md`: same count bump in the masthead paragraph.

### Known limitations

- `cumulative_cost` field in results.tsv is hardcoded `0.0000` — the orchestrator never parses Anthropic response usage objects to compute spend. Cost caps (`cost_cap_usd_hard=200`, `cost_cap_usd_soft=50`) in config are decorative until that's wired. Mitigated for this prototype by `max_iterations` bounding the worst case (~$3.25/iter × 10 iters ≈ $32). The first live run cost ~$2-4 actual (mostly iter 1's 105 generations).
- `runs_per_prompt=15` against Mac Mini Qwen3-14B is the wall-clock bottleneck (~735 judge calls per fully-scored iteration at ~10s each ≈ 2 hours). The plan's "9-13 hour for 25 iters" estimate looks optimistic for this hardware; a 25-iter full run would more realistically take 25-50 hours.
- The Sonnet sample-check fires every 5 iterations — iter 1 of the live run didn't trigger it, so the perfect 1.000 LLM-judge scores haven't been validated against Sonnet's stricter judgment. Future runs at iter 5+ will surface this.
- `ollama_base_url` is not a field on `SkillOptimizerConfig` — the live-run wrapper sets it via monkey-patch to `http://192.168.68.200:11434` (Mac Mini direct address). The config.toml still says `localhost:5050` (a stale tunnel-mapping). Promoting `ollama_base_url` to a real field is a follow-up.

### Counts

- 117 skills (no change)
- 13 subagents (no change)
- 13 hooks (no change)
- **16 SDK agents — 8 active (launchd) + 1 manual-trigger** (job-feed added in v3.28.0; skill_optimizer added in v3.27.0).

## [3.26.4] - 2026-05-07

Meta-Agent health check rewritten to read `agent-run-history.csv` instead of looking for `.baton` files in `~/.claude/batons/`. The baton-based check was a long-standing false-negative source: only `process_inbox` ever wrote batons (per `lib/baton.py:4` — batons were designed for inter-process signaling, not health monitoring), so every other active agent fell through to the "log-only / No baton found" fallback. Today's `daily-fleet-status-2026-05-07.md` reported all 7 active agents as "log-only" even though deep-researcher had successfully completed a 640s run on Topic 3 at 02:55 and recorded `status=success` in the CSV. Discovered while Sean was checking why deep-researcher looked broken in the daily report.

### Fixed

- `agents-sdk/agents/meta_agent.py` — `check_agent_health` now reads `vault/90_system/agent-logs/agent-run-history.csv` (written by `lib.logging_setup.record_run`) as the single source of truth. Status mapping: `success` / `empty-queue` / `recursion-guard` → `healthy`; `error` → `error`; unknown values pass through. Surface details upgraded — the report now shows `mode`, age, cost (when non-zero), and a truncated `notes` snippet for each agent instead of the bare `"No baton found"` string. `meta_agent` reports itself as healthy-running-now to avoid flagging the agent that just generated the report. Alert filter in `main()` updated to drop the obsolete `"log-only"` allowlist entry.
- Per-agent stale thresholds added (`_STALE_AFTER_HOURS`) so the unified 26h window doesn't false-alarm on non-daily agents: `knowledge_lint` → 192h (Sunday 22:00 weekly + 24h buffer); `flush` → 72h (hook-triggered, absorbs quiet weekends). Other agents use the 26h default.

### Added

- `agents-sdk/tests/test_meta_agent_health.py` — 16 new test cases covering: dry-run short-circuit, meta_agent self-report, missing CSV / missing-row → no-data, recent success → healthy, hyphen↔underscore name normalization (CSV uses hyphens, ACTIVE_AGENTS uses underscores), error / empty-queue / recursion-guard status mapping, stale-flag with default and per-agent thresholds, latest-row picking, cost/duration/mode surfacing, unknown-status passthrough, and notes truncation. All 33 meta-agent tests pass; full agents-sdk suite is 303 passed / 2 unrelated WOL-routing failures (pre-existing per v3.14.3 WOL retirement).

### Verified

- Live `generate_fleet_report()` against today's CSV correctly identifies all 6 non-meta agents as `healthy` with full status detail, plus knowledge-lint as `stale` (last run 2026-04-26, 259h ago — beyond the 192h weekly threshold). Deep-researcher row now reads: `status=success · mode=queue · 14.2h ago · notes='id=092a7d0d wall=640s digest=skipped-no-note'` instead of the prior `No baton found, but log exists`.

## [3.26.3] - 2026-05-06

Meta-Agent registration fix + research routing rule. The deep-researcher agent has been running on schedule since v3.23.0, but `meta_agent.py` was never updated to monitor it — `ACTIVE_AGENTS` listed only 6 entries, so today's 08:35 fleet status report wrote "Active agents: 6 of 11" with no row for deep-researcher. Discovered while triaging today's `daily-fleet-status-2026-05-06.md` after Topic 1b's 02:45 run timed out at 900s (LDR stalled at 90 % from t=209s → t=900s on a heavy compound prompt).

### Fixed

- `agents-sdk/agents/meta_agent.py` — added `deep_researcher` to `ACTIVE_AGENTS` (now 7 entries) and to `AGENT_METADATA` (display `deep-researcher`, schedule `2:45 AM daily`, machine `Mac Mini`, cost `$0.00/run`). Header docstring updated `6 currently-active → 7 currently-active`. Tomorrow's 08:35 fleet status report will include deep-researcher's health row. Verified with `meta_agent.py --dry-run`: header line correctly prints `Active agents: 7 | Disabled: 5`.

### Added

- **Research routing rule (sharpened, two reasons not one)** — documented in `CLAUDE.md` (Deep Researcher row + standalone paragraph), `vault/00_inbox/research-queue.md` (header callout), and the auto-memory feedback file. **Heavy multi-target topics route to Gemini DR / DR Max, not the LDR queue.** The two independent reasons:
  1. **Timeout** — LDR has a 900s hard budget; compound prompts stall around 90 % and produce no output. Canonical case: Topic 1b on 2026-05-06 (3 GitHub repos × 4 axes + extension catalog + 3 pinning-pattern recipes) timed out at t=209s → t=900s; same prompt completed on Gemini DR in 406s.
  2. **Citation quality collapse** — even when LDR completes, Qwen3-14B can't ground citations across multiple targets and confidently writes fabricated entities/owners/URLs. Canonical case: Topic 1a on 2026-05-05 finished cleanly at 280s but produced a report citing `PureMCPClient`, `MCPCatalog (Central)`, `MCP ADK` (none real), `github.com/microsoft/mcp` as MCP's home (actual: `modelcontextprotocol`), and fabricated `learn.microsoft.com` docs URLs. The flawed file is retained with `status: superseded` frontmatter as the canonical bad-output specimen.

### Manual research runs (Gemini DR)

- **Topic 1b** — re-run on Gemini DR tier `dr` after the LDR timeout. 406s wall, $2.80, output at `vault/20_projects/research/2026-05-06-topic-1b-cli-driven-agentic-workflow-repo-audit-pinning-patt.md`. One small render-glitch fix applied post-DR: a `cd "$FLEET_DIR" || exit 1` line had been mangled across three lines as a `||`-vs-table-cell artifact.
- **Topic 1a** — re-run on Gemini DR tier `dr` after the LDR run was reviewed and found unciteable. The 2026-05-05 LDR-version file at `vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md` gained `status: superseded` + `superseded_by:` frontmatter and a top-of-body callout warning future agents off; original content preserved below for forensic value. New Gemini DR rerun filed alongside.

### Known caveat

- `meta_agent.py --dry-run` still writes `vault/02_Areas/Agent-Fleet/daily-fleet-status-{date}.md` (every-run side effect, predates this fix). During verification today's 08:35 report was overwritten with the dry-run "healthy (dry-run)" placeholder text and then restored from the original. Future hardening: gate the file-write on `not args.dry_run`. Out of scope for v3.26.3.

### Counts

- 117 skills (no change)
- 13 subagents (no change)
- 13 hooks (no change)
- 14 SDK agents — **7 active** (no change in count; meta-agent now correctly reports the 7th).

## [3.26.2] - 2026-05-05

`job-hunt-2026` operating-model interview completed. All five artifacts at `vault/05_atlas/operating-models/job-hunt-2026/` advanced from `status: awaiting-interview` (the v3.26.0 placeholder state) to `status: confirmed` via the `work-operating-model` skill, walking Sean through the 5 interview layers (Operating Rhythms → Recurring Decisions → Dependencies → Institutional Knowledge → Friction) with summarize → confirm → write checkpoints per layer. The bundle is now consumable by the agent fleet — daily-driver morning preamble, meta-agent Domain-Aware Insights, flush.py SOUL-prepend, and knowledge_lint Tier 2 `soul-tier-a-conflict` detection will all start picking up the populated content on their next runs.

> **Resolves the v3.26.0 "Known follow-up: Interview 4 not yet run."** That blocker is closed.

### Changed

- `vault/05_atlas/operating-models/job-hunt-2026/HEARTBEAT.md` — `awaiting-interview → confirmed`. Documents the 8:30–5:30 fluid container, sacred 8:30–9:30 AM learning hour, mandatory 1–2 PM break, Friday 4:30–5:30 PM retro, 5:30 PM hard stop on active job-hunt admin, and the 8-week phase arc.
- `vault/05_atlas/operating-models/job-hunt-2026/USER.md` — `awaiting-interview → confirmed`. Codifies prioritization stack (geo → warm intro → brand → archetype → ≥$100k → learn-and-grow → energy), auto-yes / auto-no rules, **walk-away salary $100,000/yr base**, agent-delegation boundaries (drafts only — no outbound human messages from agents), tiebreakers, and per-unit definition-of-done.
- `vault/05_atlas/operating-models/job-hunt-2026/SOUL.md` — `awaiting-interview → confirmed`. Critical-path collaborators (Mary, Matt Vitebsky, Larry Cermak); broader 9 P&E peers + warm-20 as opportunistic. Tool surface broader than the v3.26.0 seed list: adds **Pi Coding Agent** (pi.dev), **Google Anti-Gravity** (main IDE), **Figma + Claude Design**, **NotebookLM**, **Codex app**. 3-machine topology (Mac Mini primary / MBP cross-over / Alienware OSS-test). Single source of truth confirmed = `vault/20_projects/prj-job-hunt-2026/README.md`. Vocabulary, sacred cows, comms norms, Ask-X-About-Y (Larry / Matt / Mary / Jordan Leech / Nate B Jones / Matt Wolfe), past landmines, week-one tacit knowledge. **5 Tier-A truths** + **2 relocation-exception clauses** ($250k+/yr OR Anthropic specifically override remote-preferred) for `knowledge_lint` Tier 2 `soul-tier-a-conflict` checks.
- `vault/05_atlas/operating-models/job-hunt-2026/schedule-recommendations.md` — `awaiting-interview → confirmed`. 7 Protect rules ("when X, then Y"), 11 Automate targets, 6 Decline rules, 7 20-min→2-min candidates, context-switch costs, agent-fleet audit + Mac-Mini migration explicitly logged as friction. **Extra-hour north star** = (1) agentic-workflow + agent-harness fundamentals, (2) Agent Evals fluency, (3) enterprise-level building patterns. Automations that don't move toward those three are deprioritized.
- `vault/05_atlas/operating-models/job-hunt-2026/operating-model.md` — `awaiting-interview → confirmed`. Synthesized profile: TL;DR, Identity, four 1-paragraph compressions of HEARTBEAT / USER / SOUL Part A / SOUL Part B, Active Leverage Points, Known Bottlenecks, Cross-Domain Bleed (life-systems / creative-studio / claude-mastery), 7 Open Questions Sean himself flagged as "I should figure this out."
- `vault/20_projects/prj-job-hunt-2026/README.md` — Status block: "Operating-model interview" `[ ] NEXT → [x] DONE 2026-05-05`. New decision-log entry with the bundle pointer.
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-migration-completion-handoff.md` — "What to do next" Step 1 marked DONE; "What's NOT yet done" item 1 (Interview 4) removed; new "Operating-model interview completed" section pointing at the bundle.
- `MEMORY.md` (auto-memory) — appended pointer to new memory file `project_job_hunt_2026_operating_model.md` documenting the bundle's confirmed state, Tier-A truths, relocation overrides, agent-message boundary rule, and the open work items the bundle surfaced.

### Open work items surfaced by the bundle

These are explicit pile-ups the interview exposed. They're not blockers on the bundle being usable — they're the actual work the bundle now points the agent fleet toward.

1. **Track-C MCP cold-start chain** (`intent-engineering` server) — no name, no repo, no README, no plan of action yet. Required steps: name → repo → README → plan. Target ship date 2026-05-25 (per master plan Phase 4) means this kickoff happens this week. Highest-priority self-blocking decision in the bundle.
2. **Substack voice + build-in-public format decisions** — both gate the public-surface track. Substack creation is named the top-of-pile-up alongside build-in-public format / cadence.
3. **Target list of 30 companies** — gates the application volume ramp-up scheduled for weeks 3–4.
4. **Agent-fleet audit + Mac-Mini migration** — Sean explicitly flagged this as Layer-5 friction. Daily-driver + deep_researcher are the keepers; everything else needs an audit pass for relevance, reliability, and host dependency. Anything depending on MBP or Alienware being awake should move to the Mac Mini or be retired. The migration in v3.26.1 (LDR daemon + 6 stale plist deletions) is the start, not the end, of this work.
5. **Gmail labeling pipeline** — Sean wants Claude to set up labels (`recruiter`, `interview-loop`, `reference-request`, `network`) and a pipeline that pulls labeled threads → markdown in `vault/30_domains/job-hunt-2026/email/` so Claude Code has fast file-system access without needing live MCP every session.
6. **YouTube yes/no decision** — undecided whether YouTube is part of the public-surface bundle.
7. **Second portfolio artifact** — what ships after MCP v0 is unspecified.
8. **Agent Evals fluency** — Sean flagged this as one of the three extra-hour learning vectors. Needs a concrete learning loop, not just "read about it."
9. **Enterprise-level build patterns** — bridge from "local prototype" to "company would trust me to ship + manage teams against this." Pattern-level, not tool-level.

### Counts

- 117 skills (no change)
- 13 subagents (no change)
- 13 hooks (no change)
- 14 SDK agents — **7 active** (no change). Bundle is content authoring, not an agent change.
- **3 active operating-model domains, all populated** — `creative-studio`, `life-systems`, `job-hunt-2026`. (Was 3 active with `job-hunt-2026` placeholder; now 3 active with all three populated.)
- pytest suite stays green (no code changes).

### Why this is a CHANGELOG entry

The operating-model bundle is content, but agent fleet behavior changes the moment these files flip from `awaiting-interview` to `confirmed` — the artifact loader (`agents-sdk/lib/artifact_loader.py`) reads them at runtime and they shape daily-driver / meta-agent / flush / knowledge-lint output. Recording the state change in CHANGELOG keeps the audit trail intact for downstream sessions.

## [3.26.1] - 2026-05-05

Fleet reinstall on Seans-Mac-mini.local. Topic 1a missed the overnight 02:45 cron on 2026-05-04 → 2026-05-05 (and the prior night). Diagnosis: `launchctl list | grep "sean.agent"` returned empty; `~/Library/LaunchAgents/` had only one stale `meeting-defender` symlink (target deleted in v3.17.0 Phase 3); the LDR `:5050` web daemon (a hard dependency for `deep_researcher`) had been started by hand from a foreground terminal that exited, leaving no persistence story. SearXNG (`:8080`, Docker `unless-stopped`) and Ollama were already healthy.

### Removed

- 6 stale launchd plists from `agents-sdk/schedules/`: `daily-evening`, `daily-morning-baton`, `pr-digest`, `process-inbox`, `sprint-health`, `weekly-review`. Citations: `AUDIT-2026-04-09-agent-downsizing.md` (5 of 6) and `AUDIT-2026-04-28-process-inbox-reenable.md` (process-inbox paused 2026-04-29 pending Path B local-`gemma4:e4b` rewrite). Net plist count `13 → 7` (5 active SDK + 1 daily-morning + 1 gated `gemini-researcher`).
- Dangling `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` symlink (target deleted in v3.17.0 Phase 3, April 18).

### Added

- **`agents-sdk/schedules/com.sean.service.ldr-web.plist`** — first non-`agent.*` plist in the fleet. Label: `com.sean.service.ldr-web`. Persistent daemon for the Local Deep Research web server (`~/Code-Brain/local-deep-research-stack/.venv/bin/ldr-web`). `RunAtLoad=true`, `KeepAlive=true`, `ThrottleInterval=60s`. Env vars: `LDR_WEB_PORT=5050` (port 5000 collides with macOS AirPlay Receiver), `LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true`, plus the standard PATH per `BUGFIX-2026-04-07-launchd-path.md`. Establishes the `service.*` label namespace alongside `agent.*` — agents are scheduled SDK runs, services are persistent dependencies. `install_schedules.sh` already globs `*.plist` so this gets installed automatically (no script change required).

### Operational

- Reinstalled launchd schedules on Seans-Mac-mini.local. **6 active SDK agent jobs loaded** (`vault-indexer`, `vault-synthesizer`, `deep-researcher`, `meta-agent`, `knowledge-lint`, `daily-morning`) + **1 LDR service daemon** (`ldr-web`). `gemini-researcher` correctly skipped (default disabled, opt-in via `INSTALL_GEMINI=1`).
- Smoke test: `deep_researcher.py --mode queue` consumed Topic 1a from `vault/00_inbox/research-queue.md`, ran in 280s wall-clock against the now-persistent LDR + SearXNG stack, wrote `vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md` (11,284 bytes, 939 words), marked the queue item done with backlink, and recorded `success` in `agent-run-history.csv` at $0.00 cost. Daily-note digest skipped because `2026-05-05.md` doesn't exist yet (daily-driver morning hadn't run today; this is the same pattern that normal 02:45 cron runs will hit before the 08:45 daily-note creation).

### Why a service daemon, not a fix-the-script

`install_schedules.sh` was already correct in shape — it failed only because the directory contained 6 stale plists that a clean install would re-symlink. After the deletions, the script installs the right set with no behavior change. The wider gap was the LDR dependency lacking a persistence guarantee, which masquerades as a fleet-wiring bug whenever LDR happens to be down. Codifying LDR as a launchd service closes the loop.

### Files

- Plist deletions: `agents-sdk/schedules/com.sean.agent.{daily-evening,daily-morning-baton,pr-digest,process-inbox,sprint-health,weekly-review}.plist`
- Plist added: `agents-sdk/schedules/com.sean.service.ldr-web.plist`
- Plan + summary: `vault/20_projects/prj-superuser-pack/open-source-deep-research/2026-05-04-fleet-reinstall-{plan,summary}.md`
- Smoke-test artifact: `vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md`

### Active-agent count

CLAUDE.md's "**Active agents (7 of 14):**" line remains correct (5 launchd-scheduled + daily-morning + flush hook = 7). No CLAUDE.md / README.md count edits required by this release.

### Vault organization (post-execution cleanup)

Audited `vault/20_projects/prj-superuser-pack/open-source-deep-research/` after the fleet-reinstall plan landed. Folder had grown to 11 files mixing canonical specs, executed plans, and pre-migration scoping reference docs — making it non-obvious which doc was the source of truth for the 7 active research topics.

- **Active folder reduced 11 → 5 files.** Kept: `phase-4-night-1-2026-05-03.md` (canonical 7-topic spec — the source of truth for which topics exist, what they ask, and which queue/cost tier they belong to), `you-are-a-senior-modular-pelican.md` (kept as ongoing gotcha-reference for future LDR / Mac Mini work), and the 3 fleet-reinstall artifacts from this release.
- **Moved to `archive/` subfolder (6 files):** `2026-05-04-deep-researcher-fleet-reinstall-prompt.md` (the prompt that kicked off this session), `gemini-deep-research-integration-plan-2026-05-03.md` (v3.25.0 implementation plan, shipped), `macmini-migration-plan-2026-05-02.md` (Mac Mini migration plan, executed), `Claude-Synthesis-of-Deep-Research-Reports.md` + `Gemini-Local-Autonomous-Research-Agent-Landscape.md` + `Perplexity-Local-Open-Source-Deep-Research-Agent-Stack.md` (Apr 28 early scoping research, superseded by the migration + integration plans). All 6 were untracked, so no git history was lost; archive folder is the durable retention path.
- **`vault/00_inbox/gemini-research-queue.md` truthed** to match reality:
  - **Topic 2 marked `[x]`** — the manual `gemini-dr` run on 2026-05-04 17:22 ($2.80, recorded in `agent-run-history.csv`) produced the report at `vault/20_projects/research/2026-05-04-you-are-a-senior-research-analyst-specializing-in-ai-develop.md`. The agent didn't fire it (the autonomous `gemini_researcher` is `enabled = false` by intent), so the queue still showed `[ ]` despite the work being done. Now reflects ground truth.
  - **Topic 4 moved to a new `## Deferred (post-severance review)` section** with explicit rationale linking to the layoff (2026-05-04) and the portfolio-priority logic from `vault/20_projects/prj-job-hunt-2026/README.md`. The DR Max ($3–7) call is the single most expensive in the project; deferring until severance lands AND until Topic 2's findings are read is the cost-disciplined path.

### How to navigate this folder going forward

1. **Source of truth for research topics:** [`phase-4-night-1-2026-05-03.md`](vault/20_projects/prj-superuser-pack/open-source-deep-research/phase-4-night-1-2026-05-03.md). Has the 7 topics, prompts, queue assignment, expected cost.
2. **Live queues** (truthed with done-marks + backlinks):
   - LDR free tier (02:45 daily on Mac Mini): [`vault/00_inbox/research-queue.md`](vault/00_inbox/research-queue.md)
   - Gemini paid tier (manual or opt-in autonomous): [`vault/00_inbox/gemini-research-queue.md`](vault/00_inbox/gemini-research-queue.md)
3. **Topic 1a is done; Topics 1b/3/5/7 will auto-process via the 02:45 cron starting 2026-05-06.**
4. **Topic 2 is done (manual run 5/4); Topic 4 is deferred post-severance.**
5. **Any pre-migration / pre-integration scoping docs live under `archive/`** — keep but don't read first.

## [3.26.0] - 2026-05-04

Block-to-job-hunt migration — repurposes the repo from a 3-domain world (the-block / creative-studio / life-systems) to a 4-domain world (creative-studio / life-systems / job-hunt-2026 — with the-block bundle archived 2026-05). Sean was laid off from The Block on 2026-05-04 (cost-cutting layoff delivered by Larry Cermak + Vicky Lu). The migration sanitizes Block-specific instructions out of the agent fleet, repoints the daily-driver morning brief at job-hunt + deep-work signals, archives the the-block operating-model bundle without deleting it, extends the work-operating-model skill to a 4th domain (Path C — minimal in-place fork), and stands up an awaiting-interview job-hunt-2026 operating-model bundle ready for Sean to populate via the new Interview 4 prompt.

> **Migration philosophy:** Sanitize-in-place where possible (skills); archive-don't-delete where sanitization isn't appropriate (Block-confidential operating-model artifacts). No skills/agents/hooks deleted. None of the validator-protected workspace folders moved.

### Added

- `vault/05_atlas/operating-models/job-hunt-2026/` — new 4th domain bundle. 5 placeholder artifacts (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations) at `status: awaiting-interview`, ready for Sean to populate via the work-operating-model skill.
- `vault/40_archive/operating-models-the-block-2026-05/` — archived the-block bundle (`git mv` from `vault/05_atlas/operating-models/the-block/`). 5 artifacts preserved + new `README.md` documenting provenance and re-runnability.
- `.claude/skills/daily-driver/SKILL.md` — new "Step 1a: Job-Hunt + Deep-Work Morning Brief" section. The 8:45 AM SDK agent now surfaces 5 job-hunt + deep-work signals: applications submitted yesterday, today's interview events, deep-work focus (Track-C MCP server), Status checkboxes due in next 7 days, yesterday's wins.
- `.claude/skills/work-operating-model/SKILL.md` — new "Job Hunt 2026" subsection in Domain-Specific Tuning Notes. New 4th row in Domain Argument Handling table. New routing rule for "job hunt" / "hunt" / "search" / "onwards" → job-hunt-2026.
- `.claude/skills/work-operating-model/interview-questions.md` — Layer 1 Q2 sub-bullet for Job Hunt 2026 (weekly app/outreach batches, interview cycles, Friday weekly retro).
- `vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md` — new "Interview 4 — Job Hunt 2026" section with start prompt, commit prompt, and cross-check prompt mirroring Interviews 2 + 3. Interview 1 (The Block) banner-marked archived 2026-05.
- `.claude/hooks/daily-note-appender.sh` — new domain-classification pattern: `*job-hunt-2026*\|*job-hunt*\|*onwards-and-upwards*) DOMAIN="job-hunt"`. Existing patterns kept.
- `vault/Sean-Winslow-Full-Personal-Context-v2.0.md` — new top section `## Career Status (2026-05-04)` documenting layoff context, 8-week job hunt, AI/Tech/Creative PM target priority, Larry Cermak as primary reference. Ed-as-reporting-line moved to Prior Role archive subsection.

### Changed

- **DOMAINS tuple updated across 6 production files** in `agents-sdk/`: `lib/artifact_loader.py`, `agents/daily_driver.py`, `agents/meta_agent.py`, `agents/flush.py`, `agents/knowledge_lint.py`, `agents/process_inbox.py`. From `("the-block", "creative-studio", "life-systems")` to `("creative-studio", "life-systems", "job-hunt-2026")`. Test fixtures updated correspondingly.
- **9 Block-themed skills sanitized in place** (Chunk 4 of migration plan + Karpathy synthesis "consolidate" sweep): `analytics-workarounds`, `api-product-management`, `campus-education`, `etf-page-creator`, `jira-automation`, `meeting-prep`, `revops-adops-automation`, `sprint-health`, `stakeholder-update`. Strip Block specifics; keep PM patterns. None deleted.
- **`crypto-web3-context` KEPT UNCHANGED** — domain knowledge useful for AI/crypto PM target sector.
- `daily-driver` skill: dropped `swinslow@theblock.co` from calendar parallel-query. Single calendar (`sean.winslow28@gmail.com`). Slack overnight scan no-op'd until personal Slack workspace exists. Apartment-cleanup section removed (March 20 deadline already passed).
- `time-management` skill **full rewrite** for job-hunt rhythm: 5:30 AM wake (was 4:45 AM), Track A/B/C weekly structure (replaces 45/35/20 split), 8:30 AM–12:30 PM deep work, Friday 4:30–5:30 PM weekly retro, 5:30 PM hard stop (non-negotiable per master plan).
- `intent-engineering` + `technical-writing` + `zapier-chrome-automation`: incidental Block sample data → generic equivalents.
- Root `CLAUDE.md`: domain table the-block row → "Archived 2026-05"; routing table marked the-block (archived); new row "Job-hunt work → vault/20_projects/prj-job-hunt-2026/"; calendar rule replaced with single-calendar instruction.
- Root `README.md`: mirrors CLAUDE.md domain-table edits.
- `the-block/CLAUDE.md` + `the-block/README.md`: archive banner at top. Workspace folder kept in place at root per `scripts/validate.py` rule #7 (validator hard-enforces the-block/ exists).
- `creative-studio/CLAUDE.md` + `life-systems/CLAUDE.md`: incidental Block refs removed; routing reroutes to prj-job-hunt-2026/.
- `vault/05_atlas/operating-models/README.md` + `INTERVIEW-PLAYBOOK.md`: 3-active-domain framing (creative-studio, life-systems, job-hunt-2026); the-block archive note.
- `agents-sdk/config.toml`: daily-driver agent `enabled` flipped temporarily for migration; `sprint_health.project_key` generalized from `BE` to `TBD` (agent dormant; project key gets set when re-activated for new role's Jira instance).
- `agents-sdk/benchmarks/golden_sets/inbox_triage.json`: Block sample data → generic equivalents.
- `MEMORY.md` (auto-memory): single-calendar rule; new "Block-to-Job-Hunt Migration (2026-05-04)" project memory; Block Jira config moved to `## Archived` section.

### Migration plan + audit plan

Plan documents (vault, source of truth for this release):

- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` — 8-phase master plan (Track A runway / Track B pipeline / Track C MCP-server differentiator)
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md` — 5-day migration plan (Chunks 1–5)
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-audit-plan.md` — file-level audit (P0/P1/P2 tables) + operating-model recommendation (Path C) + Sean's resolutions to the 8 open questions

### Counts

- 117 skills (no change — sanitized in place, none deleted)
- 13 subagents (no change)
- 13 hooks (no change)
- 14 SDK agents (7 active — no change)
- **3 active operating-model domains** (was 3; the-block archived; job-hunt-2026 added)
- pytest suite **stays green** (modulo 2 pre-existing WOL test orphans in `tests/test_route_to_macbook.py` from the v3.14.3 WOL drop)

### Known follow-ups

- **Interview 4 not yet run** — Sean needs to run the work-operating-model skill against `domain=job-hunt-2026` interactively (~45 min) to populate the placeholder bundle. Until then, the daily-driver morning brief gets job-hunt context from `vault/20_projects/prj-job-hunt-2026/README.md` (which IS populated) instead of from the HEARTBEAT body. Cross-check prompt is in INTERVIEW-PLAYBOOK Interview 4.
- **Slack overnight scan stays no-op** until Sean has a personal Slack workspace wired in.
- **Atlassian + Block calendar MCP cleanup** (migration Chunk 5) deferred to Mon 5/11 per the migration plan calendar.

## [3.25.0] - 2026-05-03

Gemini Deep Research integration — ships a new `gemini-deep-research` skill, an autonomous SDK agent (`gemini_researcher`, **default disabled**), and a Python helper (`agents-sdk/scripts/gemini_dr.py`) with self-policing cost caps. The cap stack is: $7 per-task hard ceiling, $10 per-day circuit breaker, $20 per-month governor — meaning worst-case spend on a queue-stuffing accident is $10/day, not unbounded. The skill teaches interactive sessions when and how to delegate to Gemini DR vs. run a local LDR query. The agent is committed and plist-shipped but intentionally not loaded by `install_schedules.sh` unless the operator passes `INSTALL_GEMINI=1`. Spend is tracked in a rolling ledger at `vault/health/gemini-spend-{YYYY-MM}.json` (created on first call).

> **Version note:** The integration plan was authored as "v3.24.0" but that version slot was taken by the `gemini-image-gen` skill (commit `ded36fb`). This release is v3.25.0 with no semantic change to scope.

### Added

- `.claude/skills/gemini-deep-research/SKILL.md` — new skill teaching when to use Gemini Deep Research vs. local LDR, how to trigger it interactively, prompt-framing guidelines, and result interpretation. Skill count `116 → 117`.
- `.claude/skills/gemini-deep-research/decision-table.md` — routing decision table (task type × latency × cost × privacy) for choosing between Gemini DR, local LDR, and in-session synthesis.
- `agents-sdk/agents/gemini_researcher.py` — new autonomous SDK agent (**default disabled**). Pulls unchecked items from `vault/00_inbox/gemini-research-queue.md`, calls `gemini_dr.run()` with per-task / daily / monthly cap enforcement, and writes reports to `vault/20_projects/research/`. Not loaded by `install_schedules.sh` unless `INSTALL_GEMINI=1` env var is set.
- `agents-sdk/scripts/gemini_dr.py` — Python helper wrapping `google-genai` SDK. Enforces the three-layer cap stack ($7 task / $10 day / $20 month), reads/writes the rolling spend ledger, and returns a structured `ResearchResult` with full citation metadata.
- `vault/00_inbox/gemini-research-queue.md` — new queue file for Gemini DR tasks (same `- [ ] question` format as `research-queue.md`).
- `vault/health/gemini-spend-{YYYY-MM}.json` — rolling spend ledger (created on first call by `gemini_dr.py`; format: `{date, task_id, model, cost_usd, query_slug}[]`).
- `agents-sdk/schedules/com.sean.agent.gemini-researcher.plist` — launchd plist for nightly 03:30 execution. Committed to repo but **not loaded** by `install_schedules.sh` without `INSTALL_GEMINI=1` opt-in gate.
- Keychain entries: `com.sean.agents.gemini_api_key` (Gemini DR), `openai_api_key`, `openrouter_api_key` — stashed in macOS Keychain during Phase 0 setup.
- `[gemini]`, `[gemini.budget]`, `[agents.gemini_researcher]` config blocks in `agents-sdk/config.toml`.
- `google-genai>=1.74.0,<2.0.0` dependency added to `agents-sdk/pyproject.toml`.
- 49 new pytest tests: 32 in `tests/test_gemini_dr.py` (cap enforcement, ledger I/O, error paths), 17 in `tests/test_gemini_researcher.py` (agent lifecycle, queue parsing, result writing). Full pytest suite `239 → 288` (+49).
- `vault/90_system/agent-logs/gemini-baseline-2026-05-03.txt` — pre-integration baseline diagnostic (Keychain verification, API reachability, model listing, cap-stack smoke test).

### Changed

- `.claude/skills/last30days/SKILL.md` — appended a 1-line cross-reference to `gemini-deep-research` under a new `## Related` section.
- `.claude/skills/deep-research-queue/SKILL.md` — appended a 1-line cross-reference to `gemini-deep-research` in the existing `## Related` section.
- `agents-sdk/schedules/install_schedules.sh` — added `INSTALL_GEMINI=1` opt-in gate: the `gemini-researcher` plist is loaded only when the env var is present, keeping the agent disabled-by-default without requiring a separate file deletion.

### Notes

- **Stream A queue load + 5-night execution** (running `gemini_researcher` on a live populated queue for five consecutive nights to validate cap enforcement in production) is parked as a follow-up maintenance task. The ledger and caps mean worst-case scenario is $10/day even on queue-stuffing accidents.
- **v1 direct-SDK path is intentional.** Phase 0 inventory found no Gemini CLI extensions in the existing MCP/tool chain (per plan D9). The `google-genai` SDK is the cleanest integration point and avoids the headless-MCP limitation that affects other agents.

---

## [3.24.0] - 2026-05-03

New universal image-generation skill — `gemini-image-gen` — added to `.claude/skills/`. Catch-all generator that wraps Google Gemini's Nano Banana 2 (`gemini-3.1-flash-image-preview`) for any image type that is NOT pixel art or pencil animation (those remain on the specialized `gemini-pixel-image-gen` and `gemini-pencil-animation-image-gen` skills). Optimizes user prompts via the 7-Layer Prompt Framework before calling the API. Skill includes its own `scripts/` and `references/` (e.g., `nano-banana-2-capabilities.md`, `universal-prompt-templates.md`).

### Added

- `.claude/skills/gemini-image-gen/SKILL.md` — universal image generator. Triggers on "generate image", "create image", "make a picture", "image of", "illustration of", "photo of", "render", "visualize", "design an image", "draw", "concept art", "mockup image", "product shot", "portrait of", "landscape of". Produces photorealistic images, illustrations, concept art, UI mockups, infographics, product photos, portraits, landscapes, architectural visualizations, social media graphics, abstract art, food photography, and diagrams.
- `.claude/skills/gemini-image-gen/scripts/` and `.claude/skills/gemini-image-gen/references/` — supporting prompt templates and Nano Banana 2 capability reference.

### Changed

- `CLAUDE.md` — header skill count `115 → 116`; architecture comment `(115 skills) → (116 skills)`.
- `README.md` — header skill count `115 → 116`; "### 115 Skills Across 12 Export Groups" → "### 116 Skills Across 12 Export Groups"; `creative-projects` row in the export-groups table bumped `7 → 8` with `Gemini image gen` added to highlights.
- `export-groups/03-creative-projects/playground.json` — added `"gemini-image-gen"` to the skills list (alphabetical insertion between `creative-writing` and `phaser-game-patterns`).

---

## [3.23.0] - 2026-05-03

Mac Mini migration of the v3.21.0 deep-research stack — the autonomous `deep_researcher` agent now runs nightly at 02:45 on the always-on Mac Mini (M4 Pro, 24 GB) instead of the intermittently-available MBP. Same shipped Python agent (`agents-sdk/agents/deep_researcher.py`), same plist, same vault anchors — but the runtime layer swaps **LM Studio + MLX** for **Ollama + GGUF (Q4_K_M)** to fit the Mac Mini's 24 GB ceiling. New `deep-research-queue` skill teaches Claude how to add good queries during interactive sessions. Plan: `vault/20_projects/prj-superuser-pack/open-source-deep-research/macmini-migration-plan-2026-05-02.md`.

### Added

- `.claude/skills/deep-research-queue/SKILL.md` — interactive write-side companion to the autonomous agent. Decision tree for "queue vs answer in session", question-quality rules, anti-patterns, expected behavior post-queue. Allowed tools: `Read`, `Edit` on `vault/00_inbox/research-queue.md` only. Skill count `114 → 115`.
- Mac Mini SearXNG container — `searxng/searxng:latest` on `:8080` with `--restart unless-stopped` and `formats: [html, json]` enabled. Settings volume at `~/Code-Brain/local-deep-research-stack/searxng-settings/`.
- Mac Mini Ollama model `qwen3-14b-research:latest` — built via `ollama create -f qwen3-14b-research.Modelfile`. Custom TEMPLATE patches the stock `qwen3:14b` chat template to **unconditionally** inject `/no_think` at the end of the last user message and pre-fill an empty `<think></think>` block in the assistant prefix. This makes the model behave as non-thinking by default for ANY caller (including LDR, which doesn't pass the `think` API field). `PARAMETER think false` is not supported in Ollama 0.22.1. Modelfile + base config at `~/Code-Brain/local-deep-research-stack/qwen3-14b-research.Modelfile`.
- Mac Mini LDR v1.5.6 install at `~/Code-Brain/local-deep-research-stack/.venv/` (Python 3.11 via `uv venv`; `uv pip install "local-deep-research[mcp]"`).
- Mac Mini macOS Keychain entries: `com.sean.agents.ldr_username` (= `sean`) and `com.sean.agents.ldr_password` (40-char strong, generated at install time).
- `~/Code-Brain/local-deep-research-stack/configure_ldr.py` — one-shot Python helper that logs into LDR via REST and applies the seven required settings. Mirrors the agent's CSRF + cookie dance. Idempotent; skips already-correct values.
- `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py` — Mac Mini variant of the v3.21.0 MBP wrapper, swapping `LMSTUDIO + qwen3-14b` overrides for `OLLAMA + qwen3-14b-research:latest`. Monkey-patches `local_deep_research.api.settings_utils.create_settings_snapshot` BEFORE importing `local_deep_research.mcp.server` so the bound symbol picks up our patched version. 8 tools exposed (`quick_research`, `detailed_research`, `generate_report`, `analyze_documents`, `search`, `list_search_engines`, `list_strategies`, `get_configuration`); FastMCP 1.27.0.
- `~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist` — symlink to `agents-sdk/schedules/com.sean.agent.deep-researcher.plist`. Loaded via `launchctl load`. Sean.agent loaded count: `11 → 12`.
- `vault/90_system/agent-logs/macmini-deepresearch-baseline-2026-05-02.txt` — pre-install Mac Mini state snapshot + every execution delta hit during install (Modelfile thinking-mode patch, LDR settings-key schema shift in v1.5.6, exact-match model lookup needing `:latest` suffix, auth rate limiter, register-form `acknowledge=true` value).
- `vault/20_projects/prj-superuser-pack/open-source-deep-research/macmini-migration-plan-2026-05-02.md` — the source-of-truth migration plan (v3.23.0 §9 below appends execution deltas inline).

### Changed

- `agents-sdk/config.toml:153` — `[agents.deep_researcher].target_machine` `"macbook_pro" → "mac_mini"`. Honest reflection of where the agent now runs (the agent itself talks to `localhost:5050` regardless of host; this field is informational).
- `agents-sdk/config.toml:263` — `[routing.task_map].deep_research` model `"qwen3-14b" → "qwen3-14b-research"`, machine `"macbook_pro" → "mac_mini"`. Trail comment updated to v3.23.0.
- `agents-sdk/agents/deep_researcher.py:96` — topical-note frontmatter attribution string `"model qwen3-14b" → "model qwen3-14b-research"` so reports are honestly attributed to the patched Modelfile tag.
- `CLAUDE.md` — header skill count `114 → 115`; architecture comment `(114 skills) → (115 skills)`; `Deep Researcher` row in the active-SDK-agents table updated from `Qwen3-14B MLX on MBP` to `Qwen3-14B GGUF (Q4_K_M, qwen3-14b-research Modelfile) via Ollama on Mac Mini`, version bumped `v3.21.0 → v3.23.0`.
- `README.md` — header skill count `114 → 115`; "### 114 Skills Across 12 Export Groups" → "### 115 Skills Across 12 Export Groups".
- `export-groups/02-pm-workflows/playground.json` — added `"deep-research-queue"` to the skills list, sibling to `"research-synthesis"` (alphabetical insertion).

### Notes

- **Memory headroom budget on 24 GB:** plan §1 documents the math — peak ~22 GB during the LDR run (14B model + KV cache + Docker/SearXNG + Ollama daemon + macOS), ~1.4-1.9 GB margin. Schedule chosen for zero overlap with other Mac-Mini-resident agents (vault-indexer 02:00 finishes by 02:15; deep-researcher 02:45 caps at 15 min so frees by ~03:00; meta-agent 06:30 is 4 hr later; daily-driver morning 08:45 is 5 hr later). Future operators adding any agent in 02:00-04:00 must re-run this math.
- **Q4_K_M, not Q5_K_M:** the Ollama registry's `qwen3:14b` tag is Q4_K_M (≈9.3 GB) by default; no separate Q5_K_M tag is exposed. Q4 actually gives more headroom than the plan's Q5 estimate (~3 GB peak vs ~1.9 GB); strictly safer.
- **The MBP install is intentionally NOT decommissioned.** Per plan "Out of Scope" — MBP setup remains as ad-hoc-daytime fallback (e.g., MCP from a session opened on MBP). Re-evaluate after 30 days of clean Mac Mini schedule history.
- **MCP wrapper maintenance debt** carries over from v3.21.0 — it monkey-patches LDR's internal `settings_utils` module. After every `pip install --upgrade local-deep-research`, re-run a wrapper smoke query and confirm the model name in the response metadata still reads `qwen3-14b-research:latest`.

### Verified at install time

- Phase 4 oneshot smoke test: `Compare GGUF vs MLX inference speed on Apple M4 Pro for 14B-class language models` → 1014 words, 23 distinct citations, 8 numeric tok/s figures, 0 `<think>` tags, **wall 217s** (well under plan's 8-14 min budget — patched Modelfile suppresses thinking entirely, so no reasoning overhead).
- Phase 8 launchd manual fire on empty queue → `agent-run-history.csv` row `2026-05-03,10:16:50,deep-researcher,queue,empty-queue,0.0000,,,no unchecked items` confirms launchd → venv python3 → agent → `record_run` path is wired.
- Phase 9 stdio handshake against `ldr-mcp-wrapper.py` → MCP `initialize` returns FastMCP 1.27.0; `tools/list` returns 8 tools; default snapshot reflects all five Mac Mini overrides.

---

## [3.22.0] - 2026-05-02

Tier-0 personal-context refresh — `Sean-Winslow-Full-Personal-Context` bumped from v1.1 → v2.0 via the interview-driven workflow in [personal-context-v2-interview-prompt.md](personal-context-v2-interview-prompt.md). v2.0 lives at a single canonical path inside the vault; v1.1 archived alongside historical profiles.

### Added

- `vault/Sean-Winslow-Full-Personal-Context-v2.0.md` — new canonical Tier-0 identity file (~290 lines). 11 sections: Identity & Background, Career, Values & Motivations (centerpiece: verbatim financial-cushion north-star quote), Key Relationships (Mary Alice McKee + parents Kenneth & Valerie Winslow + Ed Rupkus + Nate B Jones, with names and birthdates), Communication Baseline (10 explicit Sean-level rules), Daily Routine & Health (post-Boston-move 5:15–5:30 wake / 7–8 gym / 21:00 bed), Tools Machines & Hard Constraints (three-machine topology + two-Google-account wall + Mac-Mini-only finance docs + hard nevers), Active Projects (Tier-0 view), Goals (30-90 / 6-12 / 2-3 yr), Cross-Domain Connections, "Success" vision. Frontmatter `status: confirmed`, `supersedes: v1.1`, `updated: 2026-05-02`.

### Changed

- `vault/05_atlas/operating-models/the-block/operating-model.md:75` — Tier-0 wikilink bumped `v1.1 → v2.0` and path simplified (basename-only).
- `vault/05_atlas/operating-models/creative-studio/operating-model.md:74` — same.
- `vault/05_atlas/operating-models/life-systems/operating-model.md:90` — converted from hardcoded `docs/` Markdown link to vault wikilink (now consistent with the other two domains).
- `vault/05_atlas/operating-models/life-systems/SOUL.md:139` — same conversion (hardcoded `docs/` → wikilink, version bumped).
- `vault/05_atlas/operating-models/README.md:37` — Tier-0 reference bumped to v2.0; archive pointer added.
- `.claude/skills/work-operating-model/artifact-templates.md:231` — template's Tier-0 wikilink bumped to v2.0 so future operating-model interviews emit v2.0-pointing artifacts.

### Removed / Archived

- `docs/Sean-Winslow-Full-Personal-Context-v1.1.md` — moved to `_archive/Sean-Winslow-Profiles-For-Context/Sean-Winslow-Full-Personal-Context-v1.1.md` (preserved for lineage).
- `vault/Sean-Winslow-Full-Personal-Context-v1.1.md` — deleted (was a duplicate of `docs/` copy per `diff`; vault tier was orphaned per Phase 6 lint reports).

### Notes

- **Single canonical location.** Per Sean's call, v2.0 lives in vault only; the prior dual-location pattern is retired.
- **Provenance-preserving diff callouts** are inline in the v2.0 body (`(was: ... )(now: ... ) — source: ...` blocks). They can be stripped on a future read-through if Sean wants a "clean" Tier-0 artifact; left in for now as PR-reviewable evidence of every material change.
- v2.0 was assembled across Steps 1–4 of the interview prompt (silent discovery → coverage map → 6-question gap interview → draft → approval → save).

---

## [3.21.0] - 2026-05-02

Local open-source deep research stack — replaces / reduces paid Perplexity DR + Gemini DR usage. New autonomous SDK agent (`deep_researcher`) drives LearningCircuit Local Deep Research (LDR) v1.5.6 against a self-hosted SearXNG container and a local Qwen3-14B MLX 4-bit model in LM Studio, writing reports into the Obsidian vault. 100% local; $0/run.

> **Merge note:** Originally developed on the MBP on 2026-04-26 as a local v3.17.0 candidate; renumbered to **v3.21.0** at merge time (2026-05-02) because v3.17.0 was used in parallel on `main` for the agent-wiring Phase 2 release. No semantic change — same code, same scope, new version label.

### Added

- `agents-sdk/agents/deep_researcher.py` — new agent (~250 lines). Pure-Python wrapper (no Claude Agent SDK in the loop) that drives LDR via httpx REST. Modes: `--mode queue` (pick first unchecked from `vault/00_inbox/research-queue.md`) and `--mode oneshot --query "..."`. Pulls credentials via `lib.keychain.get_credential("ldr_username"|"ldr_password")`. Replicates LDRClient.quick_research's REST endpoints (`/auth/login` → `/research/api/start` → `/research/api/status/<id>` → `/api/report/<id>`) using httpx (already in agents-sdk venv) instead of cross-venv-importing LDRClient (LDR runs Python 3.11; agents-sdk runs Python 3.13). Writes a topical report to `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` and injects a one-line digest under `<!-- research-digest -->` in today's daily note (with append-section fallback if the anchor is missing). Marks the queue item done with timestamp + wikilink backlink.
- `agents-sdk/schedules/com.sean.agent.deep-researcher.plist` — launchd schedule. Nightly **02:45** (after vault-indexer 02:00 and vault-synthesizer 02:30, before any morning agent). Mirrors the daily-morning plist's PATH env var requirement.
- `vault/00_inbox/research-queue.md` — new markdown queue file. Format: `- [ ] question` per line; agent rewrites to `- [x] question — done {timestamp} → [[topical-note-path]]`.
- `vault/20_projects/research/` — new directory; auto-created by the agent on first write.
- `<!-- research-digest -->` anchor block in `vault/90_system/templates/tpl-daily.md` so all future daily notes ship with the injection point.
- `~/Code-Brain/local-deep-research-stack/` (outside repo) — Python 3.11 venv with `local-deep-research[mcp]` v1.5.6, plus a SearXNG settings volume.
- SearXNG container (`searxng/searxng:latest`) running on `localhost:8080` with `json` added to `search.formats` for API access.
- macOS Keychain credentials `com.sean.agents.ldr_username` and `com.sean.agents.ldr_password` (stored via `agents-sdk/lib/keychain.py` — same pattern as Pushover, Anthropic API key, etc.).
- `~/Code-Brain/local-deep-research-stack/bin/ldr-up.sh` (outside repo, ~200 lines bash). One-command lifecycle tool for the LDR stack: launches Docker Desktop if down, starts the `searxng` container, detects LM Studio, starts `ldr-web` in the background, applies `--restart unless-stopped` to the searxng container on first run so it auto-resurrects with Docker. Symlinked at `~/.local/bin/ldr-up` for PATH convenience. Subcommands: `ldr-up` (start, idempotent), `ldr-up --status`, `ldr-up --down`, `ldr-up --help`. Validated end-to-end: cold-start → status check → idempotent re-run → teardown → status check → recovery → status check, all 8 phases green.

### Changed

- `agents-sdk/config.toml` — new `[agents.deep_researcher]` block (`enabled = true`, `max_budget_usd = 0.10` as a guard against unintended cloud fallback, `queue_path`, `output_dir`, `output_anchor = "research-digest"`, `ldr_base_url = "http://localhost:5050"`, plus LDR call shape: `ldr_search_engines = ["searxng"]`, `ldr_iterations = 2`, `ldr_questions_per_iteration = 2`, `ldr_timeout_seconds = 900`).
- `agents-sdk/config.toml` — new `[routing.task_map].deep_research = { model = "qwen3-14b", machine = "macbook_pro" }`. Routing target is informational (the agent talks to LDR over HTTP, not LM Studio directly), but documents intent for future Mac Mini migration.
- `vault/90_system/templates/tpl-daily.md` — added `## Deep Research` section with the `<!-- research-digest -->` anchor between `## Side Project Notes` and `## Evening Reflection`.

### Configuration deviations from the original plan (captured during execution)

- **LDR port: 5050, not 5000.** macOS AirPlay Receiver claims port 5000 (`Server: AirTunes/...`). Plan's `ldr-web` invocation now requires `LDR_WEB_PORT=5050 LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true`. Agent config + plist updated.
- **LDR settings live in an SQLCipher-encrypted per-user DB**, not the `~/.config/local_deep_research/settings.toml` file the plan called out (LDR v1.5.6 architecture). Settings configured via `PUT /settings/api/<key>` after first user registration. The five critical keys: `llm.provider=LMSTUDIO`, `llm.lmstudio.url=http://localhost:1234/v1` (must include `/v1`), `llm.model=qwen3-14b` (no `qwen/` HuggingFace-style prefix), `search.tool=searxng`, `search.iterations=2`.
- **Qwen3-14B "thinking mode" disabled** via `/no_think` system-prompt directive in LM Studio's Inference tab per-model preset. Without this, Qwen3 emits ~50 reasoning tokens before content; with this, generation is 1-2s for short prompts. Anticipated in plan §6 risk #2.
- **LDR rate limiter is aggressive on `/auth/login`** (5 attempts in ~5 minutes triggers 429s with sliding window). Agent caches a session per run; do not re-login per request.
- **mode=quick is a trap for headless calls.** Submitting `{query, mode: "quick"}` to `/api/start_research` returns in ~40s with **zero sources** and hallucinated prose citations. The agent uses `/research/api/start` (LDRClient's endpoint) with explicit `search_engines=["searxng"]`, `iterations`, `questions_per_iteration` instead.

### Phase 4 hard-gate evidence (smoke test)

| Plan §4 criterion | Target | Actual |
|---|---|---|
| Length | 600–1500 words | 695 |
| ≥3 distinct URL sources | yes | 9 numbered sources, 15 unique domains in body |
| Spot-check 2 URLs resolve | 200 OK both | apxml.com/... → 200, famstack.dev/... → 200 |
| ≥2 explicit tok/sec figures | yes | 5 figures captured (45–55, 35–40, 57, 3, etc.) |
| Wall time < 15 min | yes | 320s (5m20s) |

### Phase 5 verification (this release)

- Queue → live run: 561s (9m21s) wall, 2243-word topical report, daily digest injected at `<!-- research-digest -->` anchor, queue line rewritten to `[x]` with timestamp + wikilink.
- Empty-queue path: clean exit 0, recorded in `agent-run-history.csv` with status `empty-queue`.
- Both runs visible in `vault/90_system/agent-logs/agent-run-history.csv`.

### Phase 6 — MCP server hookup (shipped this release)

- **New file:** `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py` (outside repo, ~70 lines). The `ldr-mcp` binary that ships with `local-deep-research[mcp]` runs the MCP server **in-process** with default settings — it does NOT read the per-user encrypted SQLCipher DB the LDR Web UI writes to, and the MCP tool args don't expose `llm.provider` or `llm.model` overrides. The wrapper monkey-patches `local_deep_research.api.settings_utils.create_settings_snapshot` BEFORE importing `local_deep_research.mcp`, injecting `LMSTUDIO + qwen3-14b + searxng + lmstudio.url=:1234/v1 + searxng instance=:8080` overrides into every snapshot. Caller-supplied tool overrides still win because they merge after.
- **`.mcp.json`** — added `ldr` entry (stdio transport, command points at the wrapper, no env block needed since stdio MCP runs in-process and requires no LDR auth).
- **`.claude/settings.local.json`** — added `"ldr"` to `enabledMcpjsonServers` allowlist.
- **Verified:** Manual stdio handshake (`initialize` + `notifications/initialized` + `tools/list`) returns 8 tools (`quick_research`, `detailed_research`, `generate_report`, `analyze_documents`, `search`, `list_search_engines`, `list_strategies`, `get_configuration`) with proper input/output schemas. Server reports `serverInfo.name = "local-deep-research"`, version 1.27.0 (FastMCP version, distinct from LDR's 1.5.6).
- **No credentials in the repo.** Plan §3 Phase 6 anticipated `LDR_USER` / `LDR_PASS` env vars in `.claude/settings.json`; the actual MCP architecture has no auth layer (stdio = local-only by definition; security via OS user permissions per LDR's own security notice). Zero plaintext anywhere.
- **Next step requires Sean:** Restart Claude Code, then `/mcp` should list `ldr`. First tool call (e.g., asking Claude to "use the ldr tool to research X") will take 1-5 min and produce results equivalent to the deep_researcher agent.

### Maintenance debt introduced by the wrapper

- The wrapper monkey-patches LDR internals (`settings_utils.create_settings_snapshot`). If LDR refactors that module across versions, the patch will silently break (worst case: MCP falls back to `OLLAMA + gemma3:12b`, tool call fails with `connection_error` because Ollama isn't running on this MBP). When upgrading LDR (`uv pip install --upgrade local-deep-research`), re-run the wrapper smoke-test from the v3.21.0 release notes before trusting nightly runs.
- A future LDR version may expose env-var or config-file overrides for `llm.provider` / `llm.model`. When it does, retire the wrapper and configure via the documented mechanism instead.

### Out of scope (deferred)

- **Phase 7** (Qwen3.6 27B/35B-A3B A/B benchmark vs Qwen3-14B baseline) — gated on ≥1 week of real usage; do not start until Phases 0–6 are complete and trusted.
- **Mac Mini migration** of the LDR stack (plan §5) — MBP must stay plugged-in for nightly 02:45 runs until migration. Mac Mini lacks LM Studio MLX; the migration moves to Ollama Q5_K_M GGUF.
- **URL-checker post-processor** (plan §6 risk #5 mitigation) — not built. Cited URLs are not auto-validated for 404s in the topical note.
- **launchd registration** — the new plist is in place but NOT yet `launchctl load`ed. Run `./agents-sdk/schedules/install_schedules.sh` when ready to enable nightly runs.

### Known follow-ups

- Sean's LDR password was pasted into a Claude Code conversation transcript on 2026-04-26 to seed the Keychain. Consider rotating after this release if the conversation log is sensitive (the credential only protects a local-only LDR DB on this MBP).
- Plan files (`vault/20_projects/prj-superuser-pack/open-source-deep-research/you-are-a-senior-modular-pelican.md` and `~/.claude/plans/you-are-a-senior-modular-pelican.md`) still reference port 5000 + `~/.config/local_deep_research/settings.toml` in §3 Phase 3/5/6. Pending sync to both copies.

## [3.20.0] - 2026-05-01

### Added — knowledge-loop Phase D: typed reasoning edges + synthesizer manifest

- **`concept_edges` SQLite table** (NEW). Extends `vault/.vault-index.db` with a queryable typed-edge layer alongside the existing `chunks` table. Schema lives in `agents-sdk/agents/vault_indexer.py`'s `init_db()`; idempotent `CREATE TABLE IF NOT EXISTS` so a second invocation on a populated chunks table is a no-op (verified by `test_init_db_idempotent_preserves_chunks`). Six allowed relation values mirroring OB1's `thought_edges` taxonomy: `supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`. CHECK constraint rejects bad values; UNIQUE(from_slug, to_slug, relation) makes `INSERT OR IGNORE` cheap; partial index on `valid_until IS NULL` keeps the "currently-valid" reads fast.
- **`agents-sdk/lib/concept_edges.py`** (NEW). Stdlib-only helper module exposing `get_connection()`, `insert_edge()`, `find_contradictions()`, `find_superseded()`, and a stubbed `decay_pass()`. `insert_edge` raises `ValueError` (not bare `IntegrityError`) on bad input so the synthesizer can distinguish "drop this edge, log it, keep going" from "the DB is broken, abort." All functions accept an externally-managed `sqlite3.Connection` so they can be unit-tested with `:memory:`.
- **`vault/health/synth-manifest-{date}.json`** (NEW per-run record). Mirrors OB1's per-run manifest pattern. Captures `run_id`, `files_processed`, `concepts_written`, `connections_written`, `edges_written`, `edges_rejected`, `rejected_count`, `duration_seconds`, `model_used`, `wol_status`, `status`. Atomic write via tmp-then-rename so partial files never surface.
- **`write_synth_manifest()`** in `agents-sdk/agents/vault_synthesizer.py` (NEW pure helper). Pure function — no I/O state outside the named output path. Independent of `run_synthesis` so it can be tested without standing up a full synthesis run.
- **`latest_synth_manifest()` + `synth_health_summary()`** in `agents-sdk/lib/lint_report.py` (NEW siblings to the existing lint helpers). `synth_health_summary` returns `""` when no manifest exists, when JSON is malformed, or when the file is unreadable — daily-driver morning brief never crashes on a broken manifest.
- **`agents-sdk/tests/test_concept_edges.py`** (NEW, 13 tests). Schema migration, idempotency on populated chunks, indexes present, insert happy path, UNIQUE → `INSERT OR IGNORE` returns False, invalid relation → `ValueError`, self-edge rejection, confidence range guard, `find_contradictions` filters `valid_until IS NULL`, contradiction fan-out (3 contradictions from one concept), `find_superseded`, `decay_pass` no-op, `get_connection` idempotency.
- **`agents-sdk/tests/test_synth_manifest.py`** (NEW, 11 tests). `write_synth_manifest` directory creation, payload shape, JSON round-trip, atomic overwrite (no `.tmp` leftover), `latest_synth_manifest` name-sort precedence, `synth_health_summary` empty/formatted/malformed-JSON/non-dict-JSON/missing-keys variants.

### Changed

- **`agents-sdk/agents/vault_synthesizer.py`** — `SynthesisResult` gains `edges_written`, `edges_rejected`, `model_used`, `wol_status`, `run_id` fields. Synthesis prompt extended to ask for an OPTIONAL `relations` array per connection (typed edges between concept pairs); same LLM call, richer parsing only — no extra round-trip. After each connection article writes, `run_synthesis` walks `relations` and calls `concept_edges.insert_edge()` inside the existing FileLock window. Bad relations are logged at WARNING level via the synthesizer's logger and increment `result.edges_rejected`; the article still writes. New optional `db_conn`, `classifier_version`, `logger` parameters preserve the test path (`db_conn=None` skips edge writes silently). `_default_llm_caller_factory` accepts a `manifest_state` dict that captures `model_used` + `wol_status` from the first successful routing decision; `main()` writes the synth-manifest after `run_synthesis` returns and on the WOL-unavailable deferral path so the daily-driver brief sees deferrals as data.
- **`agents-sdk/agents/knowledge_lint.py`** — Tier 2 contradiction detection becomes hybrid (third touch on this file: Phase 2 added soul-tier-a-conflict, Phase C added qa/ to `_ORPHAN_EXCLUDE_DIRS`, Phase D adds the SQL fast path). New `_read_sql_contradictions()` helper queries `concept_edges` for `relation='contradicts' AND valid_until IS NULL`, emits one CRITICAL `LintIssue` per row with `(source=sql)` in the detail, and logs `Tier 2 contradiction: source=sql ...`. SQL fast path always runs when `vault/.vault-index.db` exists — gracefully no-ops on missing file or missing table (with explicit test coverage so a stale legacy DB doesn't crash the lint run; the read path also will NOT mutate the schema as a side effect). LLM slow path still runs when `llm_caller is not None`, preserving Phase 2's `soul_conflicts` discovery; LLM contradictions are deduplicated against SQL hits by normalized `frozenset({from_slug, to_slug})`. Logged with `source=llm` or `source=llm dropped (sql had it)`.
- **`agents-sdk/agents/daily_driver.py`** — Morning preamble (second touch on this file: agent-wiring Phase 1 added `build_artifact_preamble`, Phase D adds the synth line). `synth_health_summary()` is appended under the existing `vault_health_summary()` line in `morning` mode only. Empty string from `synth_health_summary` (no manifest yet) suppresses the line entirely so a fresh vault doesn't render a stub.
- **`agents-sdk/tests/test_vault_synthesizer.py`** — +4 tests. Edge-write happy path with a mocked LLM that emits `relations`, invalid-relation drop-but-don't-crash, `db_conn=None` silent skip, `run_id` ISO-shape verification.
- **`agents-sdk/tests/test_knowledge_lint.py`** — +5 tests in a new `TestSqlFastPath` class. SQL emits CRITICAL per row, no-DB path skipped silently, missing-table path no-ops without schema mutation, SQL+LLM dedupe by slug pair, soul_conflicts preserved across the dedupe boundary.
- **`agents-sdk/tests/test_daily_driver_vault_health.py`** — +4 tests. `latest_synth_manifest` name-sort, `synth_health_summary` count formatting, `build_preamble("morning")` includes the synth line when a manifest exists, `build_preamble("morning")` omits the line when no manifest exists.

### Spec interpretation note (the hybrid path)

The plan's "the existing LLM contradiction pass runs only if the fast path returns < N expected hits" was in tension with Phase 2's `soul_conflicts` capability — the Tier-2 LLM call also produces SOUL conflict findings, which have no SQL substitute. Suppressing the entire LLM call when SQL has hits would silently drop SOUL conflict detection on weeks the synthesizer flagged contradictions. **Resolution: always run the LLM call when `llm_caller is not None`, and dedupe contradictions by normalized `frozenset({from_slug, to_slug})`.** SQL hits win when both paths surface the same pair (the row carries source provenance). LLM-only contradictions still surface — the synthesizer didn't catch them. The `--full` flag has no semantic change in Phase D — both paths still run. The "zero LLM cost" axis lands when `llm_caller is None` (e.g., MBP asleep / Tier-2 staleness-only mode); contradictions still surface from the DB without any model invocation.

### Empty-vault verification path (documented, not faked)

Spec gate 5 wants ≥1 row in `concept_edges` from a real `vault_synthesizer` run, but the MBP-Qwen3-14B path is intermittent ("succeeds only when MBP awake" per CLAUDE.md). Two acceptable verification paths: (1) live synthesizer run with mocked LLM output, (2) pure unit tests with mocked LLM caller + tmp_path SQLite. **Chose path 2.** Rationale: the table semantics are identical regardless of whether the LLM is real or mocked; unit tests are hermetic and CI-friendly; live integration falls to the 1-week check-in agent firing 2026-05-08. No fake "live output" anywhere — the empty-state path (zero edges written, zero rows in the table) renders cleanly through the daily-driver brief because `synth_health_summary` returns `""` when no manifest exists.

### Verification

- `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_concept_edges.py -v` → 13/13 PASS
- `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_synth_manifest.py -v` → 11/11 PASS
- Full pytest suite: 241/241 PASS (was 204; +37 from this phase)
- `python3 scripts/validate.py` → PASSED, 58 warnings (zero new ones, exact baseline match)
- Schema migration smoke: `init_db()` called on a fresh tmp DB creates `concept_edges` + 3 indexes; called a second time on a populated chunks table preserves all chunk rows.

### Files

- NEW: `agents-sdk/lib/concept_edges.py`
- NEW: `agents-sdk/tests/test_concept_edges.py` (13 tests)
- NEW: `agents-sdk/tests/test_synth_manifest.py` (11 tests)
- MODIFY: `agents-sdk/agents/vault_indexer.py` — `concept_edges` table + 3 indexes in `init_db()`
- MODIFY: `agents-sdk/agents/vault_synthesizer.py` — `SynthesisResult` extension, prompt `relations` field, edge inserts inside FileLock window, `write_synth_manifest()`, `_default_llm_caller_factory` `manifest_state` capture, `main()` synth-manifest write
- MODIFY: `agents-sdk/lib/lint_report.py` — `latest_synth_manifest()` + `synth_health_summary()` siblings
- MODIFY: `agents-sdk/agents/knowledge_lint.py` — `_read_sql_contradictions()` helper, hybrid path with frozenset dedupe in `run_tier2`
- MODIFY: `agents-sdk/agents/daily_driver.py` — `synth_health_summary` import + 3-line morning-preamble extension
- MODIFY: `agents-sdk/tests/test_vault_synthesizer.py` — +4 Phase D tests
- MODIFY: `agents-sdk/tests/test_knowledge_lint.py` — +5 `TestSqlFastPath` tests
- MODIFY: `agents-sdk/tests/test_daily_driver_vault_health.py` — +4 synth-line tests
- MODIFY: `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `docs/agents-sdk-docs/agents-sdk.md`

### Rollback

- `sqlite3 vault/.vault-index.db "DROP TABLE concept_edges"` — drops the table; idempotent re-creation on next vault_indexer run.
- Revert `vault_synthesizer.py` edge-insert lines (LLM still writes connection articles unchanged with bare prompt — `relations` is OPTIONAL in the prompt schema).
- Revert `knowledge_lint.py` Tier 2 to LLM-only contradiction pass (preserve Phase 2 SOUL path + Phase C qa/ exclusion).
- Revert `daily_driver.py` morning-brief synth line (preserve Phase 1 artifact preamble).
- Delete `agents-sdk/lib/concept_edges.py`.
- Delete `vault/health/synth-manifest-*.json` files (or leave — inert).

## [3.19.0] - 2026-05-01

### Added — knowledge-loop Phase C: query.py + qa/ tier + OB1 provenance

- **`agents-sdk/scripts/query.py`** (NEW). Terminal Q&A against the synthesized knowledge base. Two-pass orchestration: a selection pass reads `vault/knowledge/index.md` + the question and asks the LLM for 3-N article paths with similarity scores; an answer pass reads the selected article bodies and asks for a `[[wikilink]]`-citing answer. Local-first model routing via `lib.hybrid_router.HybridRouter` (Qwen3-14B on MBP through the `vault_synthesis` task) with Anthropic Sonnet 4.6 fallback. CLI flags: `--file-back`, `--model {auto,local,api}`, `--max-articles N`. Reuses `load_config`, `setup_logger`, `record_run`, `FileLock`, `vault_io` paths.
- **`vault/knowledge/qa/`** (NEW article tier). Created on first `--file-back` run. Synthesizer `regenerate_index` now emits a `## Q&A` section listing qa/ articles alongside concepts/connections (Phase B SessionStart injection picks them up automatically).
- **`vault/knowledge/qa/.manifest.json`** (NEW, C.M2 OB1-inspired). Append-only JSONL — one record per `--file-back` run capturing `run_id`, `question`, `model`, `model_route`, `consulted` (path + chunk_id + similarity), `duration_ms`, `answer_chars`, `qa_file`. JSONL chosen over JSON for lock-friendly append semantics matching the `lib/logging_setup.py` `record_run` pattern.
- **C.M1 chunk_id + similarity in qa/ frontmatter** (OB1-inspired). Each consulted article entry in the qa/ frontmatter ships a 12-char SHA-256 prefix of `(file_path, chunk_index)` from `vault/.vault-index.db`'s `chunks` table plus the selection-pass similarity score. Origin: OB1's `derived_from` UUID provenance pattern, ported to file-path + chunk identity for Sean's vault-as-source-of-truth setup.
- **`agents-sdk/tests/test_query.py`** (NEW, 22 tests). Mocks the LLM via dependency-injected callers; covers slugify, chunk_id stability, index parsing (populated + empty stub + missing index), selection-pass filtering / similarity clamping / max-articles cap / LLM-exception-swallowing, `load_articles` chunk_id stamping (DB-backed and fallback paths), qa/ frontmatter shape, manifest append (one line per run), and end-to-end `run_query` happy path / empty-index / no-`--file-back` / two-consecutive-runs.
- **`[agents.query]` block in `agents-sdk/config.toml`.** `default_model = "auto"`, `max_articles = 10`, `task_key = "vault_synthesis"`, plus selection/answer max-tokens, qa_dir, manifest_path. CLI flags override these defaults.

### Changed

- **`agents-sdk/agents/vault_synthesizer.py`** — `QA_SUBDIR` constant added; `regenerate_index()` emits a `## Q&A` section listing `qa/*.md` articles when the directory exists. Idempotent / silent when qa/ is absent.
- **`agents-sdk/agents/knowledge_lint.py`** — `qa` added to `_ORPHAN_EXCLUDE_DIRS`. qa/ articles are intentional answer endpoints (cite outward but receive no inbound wikilinks by design); without this, every qa/ article would surface as orphan-MEDIUM noise on every Sunday lint. Existing recursive `knowledge.rglob("*.md")` checks (missing-frontmatter, camelcase-filename) and Tier 2 stale-reference scan already cover qa/, so no other lint changes were needed for the qa/ tier to stay clean.

### Spec interpretation note

The plan's "include qa/ in orphan + stale + sparse checks" is in tension with the gate "knowledge_lint Tier 1 reports zero new issues against qa/". The implementation resolves this by treating qa/ as a first-class article tier whose visibility in lint is governed by *intent*: it inherits the missing-frontmatter / camelcase-filename / stale-reference checks via existing rglob recursion and `_vault_md_files`, but is excluded from orphan detection because qa/ articles are answer endpoints by construction. No new "sparse" check kind was introduced — the term has no prior definition in `knowledge_lint.py` and the gate only requires zero new qa/ issues, which the orphan-exclusion approach delivers.

### Empty-state behavior (documented, not faked)

`vault/knowledge/index.md` is currently the empty-state stub (vault_synthesizer's Mac Mini fallback emits zero articles when the MBP-hosted Qwen3-14B is asleep — CLAUDE.md "intermittent — succeeds only when MBP awake"). Phase C handles the empty index explicitly: the selection pass returns zero candidates without invoking the LLM, the answer pass reports `"No knowledge articles match this question yet."`, and `--file-back` writes nothing (no qa/ file, no manifest line). Three unit tests lock this behavior in (`test_run_selection_pass_returns_empty_on_empty_index`, `test_run_query_empty_index_produces_clean_report_no_qa_file`, `test_run_query_missing_index_file_returns_helpful_message`). Live smoke confirmed: `query.py "..." --file-back` against the live empty index exits 0, prints the empty-state message, creates no files. Once the synthesizer produces real concept/connection articles, the same CLI works without changes.

### Gates

- `pytest agents-sdk/tests/test_query.py -v` → 22 / 22 PASS.
- `pytest agents-sdk/tests/` → 204 / 204 PASS (was 182, +22 from this phase).
- `python3 scripts/validate.py` → PASSED, 58 warnings (zero new ones — all 58 are pre-existing secret-pattern false positives carried over from v3.18.0).
- End-to-end smoke against a synthetic populated vault: `--file-back` produced a valid `vault/knowledge/qa/<slug>.md` with `chunk_id` + `similarity` per consulted article; `vault/knowledge/qa/.manifest.json` gained exactly one new line; subsequent `regenerate_index` ran without error and the new `## Q&A` section appeared in `index.md`; `knowledge_lint.run_tier1` reported zero qa/ issues.

### Rollback

- Delete `agents-sdk/scripts/query.py` (or leave it — inert without invocation).
- Delete `vault/knowledge/qa/` (or leave it — orphaned).
- Revert the qa/ inclusion in `regenerate_index()` and the qa/ entry in `_ORPHAN_EXCLUDE_DIRS` (small, surgical reverts).
- Remove the `[agents.query]` block from `agents-sdk/config.toml`.

## [3.18.0] - 2026-05-01

### Added — knowledge-loop Phase A: PreCompact safety net

- **`.claude/hooks/pre-compact-flush.sh`** (NEW). Mirror of `session-end-flush.sh`; the only diff is `--trigger pre-compact` so the daily-log session block tags are distinguishable. Hook count `12 → 13`.
- **`PreCompact` block in `.claude/settings.json`.** Fires the new hook when Claude Code auto-compacts a long session, so pre-compact knowledge isn't silently lost.
- **`--trigger {session-end,pre-compact,manual}` argparse arg in `agents-sdk/agents/flush.py`.** Default `session-end` (backwards-compatible). Threads into `session_summary["tag"]` so `vault/10_timeline/daily/*.md` session blocks now show `tag: session-end` / `tag: pre-compact` / `tag: manual` instead of the prior `tag: auto`.
- **`agents-sdk/tests/test_flush_trigger.py`** (NEW, 5 tests). Verifies the default tag, all three known triggers thread correctly into the daily-log block, argparse accepts known triggers, and rejects unknown ones with exit 2.

### Changed

- **`run_flush()` signature** gained a `trigger: str = "session-end"` keyword arg. Existing call sites in tests pass without change (default preserves prior behavior).
- **`flush.py` docstring** notes the trigger flow into the daily-log tag field.

### Re-applied fresh, not merged

The original `knowledge-loop/phase-a` branch (commit `4ca4413`, authored 2026-04-25) was too stale to rebase — it predated agent-wiring Phase 2 and would have regressed `flush.py` SOUL prepend, CLAUDE.md content, and the `flush.py` docstring. v3.18.0 ships the same intent on a fresh `knowledge-loop/phase-a-v2` branch layered on top of Phase 2 instead of regressing it. Stale branch deleted post-merge.

### Gates

- `pytest agents-sdk/tests/` 182 / 182 PASS.
- `python3 scripts/validate.py` PASSED (58 pre-existing warnings, no new ones).

### Rollback

- Remove the `PreCompact` block from `.claude/settings.json` — instant kill.
- Delete `.claude/hooks/pre-compact-flush.sh` (optional, leaves it inert).
- The `--trigger` arg is backwards-compatible — leaving it in place keeps existing daily logs valid.

## [3.17.5] - 2026-05-01

### Closed

- **Agent-wiring Phase 2 production soak — CLOSED.** 4-day window 2026-04-28 → 2026-05-01. Result: 5/7 gates PASS, 2/7 PARTIAL by observation gap, no regression observed. Rollout doc flipped `status: in-progress` → `status: complete`. Full review: `vault/20_projects/prj-superuser-pack/phase-2-soak-closeout-2026-05-01.md`.
  - **G1–G3, G6, G7 PASS:** full pytest suite green (177 passed); `python3 scripts/validate.py` passes; pre-flight JSON guard already validated 5/5 historical transcripts at ship time; producer-side loop (vault-indexer + vault-synthesizer) ran 4/4 nights with zero errors; zero new errors in `agent-run-history.csv` from any Phase 2 modified agent.
  - **G4 PARTIAL (flush SOUL prepend):** all 21 flush invocations during the window hit the recursion guard — sessions had no extractable content. Integration is structurally wired; soak window simply did not exercise the code path.
  - **G5 PARTIAL (Sunday `knowledge_lint --full`):** last run was 2026-04-26 (pre-Phase-2); next scheduled run is 2026-05-03. No `--full` run inside the window.
  - **Domain-Aware Insights signal (G4-adjacent):** 4/4 days populated, 0 fallbacks. gemma4:e4b output cross-references real Protect / Automate / Decline items by name across all three domain `schedule-recommendations.md` files. This is the strongest live evidence of Phase 2 working as intended.

### Decided

- **No more synthetic soak holds.** Operating preference, set 2026-05-01: ship validated work and observe in production. Rollback paths remain (`[artifacts].enabled = false`, hook removal, per-agent config disable). The G4 + G5 PARTIAL gates convert opportunistically — next non-trivial flush extraction confirms G4; 2026-05-03 Sunday lint confirms G5. They do not block downstream work.

## [3.17.4] - 2026-04-29

### Changed

- **`process-inbox` SDK agent disabled pending Path B rewrite.** Round 2 followup runs validated that the cloud-Sonnet path is functionally working (6 of 9 files moved across two manual runs) but cost-inefficient (~$1.16/file × 3 files/run × twice-weekly = unsustainable for the ~3-files/day steady-state arrival rate). Total cloud spend across 6 SDK invocations: ~$6.97 for 6 files moved. The audit doc's "if round 2 also trips, switch to Path B" threshold was crossed.
- **launchd job unloaded** via `launchctl bootout` — no more scheduled fires until Path B ships.
- **Active SDK agent count `7 → 6`** (back to v3.17.1 state minus `meeting_defender`/`sprint_health`).
- **Manual fallback documented:** the `process-inbox` skill in an interactive Claude Code session is the working alternative — same machinery that cleared `vault/00_inbox/` on 2026-04-25 and the final 3 files on 2026-04-29.
- Cost trajectory recorded in `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md` "Round 2 followup runs" + "Decision: Pause cloud path, switch to Path B" sections.

### Path B scope (next)

Estimated 3-4 hours of focused work:
1. Replace `claude_agent_sdk.query()` in `agents/process_inbox.py` with a `lib/hybrid_router.py` call routed via `routing.task_map.inbox_triage` (already defined at `config.toml:200`, validated `gemma4:e4b` on Mac Mini at +7.5pp quality vs `phi4-mini` in Phase 6 A.7 benchmarks).
2. Convert the multi-turn agentic loop into a deterministic Python loop: per inbox file, single local-model call with classification schema, JSON-parse response, apply move via `pathlib`. No turn caps to manage with local inference.
3. Inline the `#triage/research-candidate` flag rule into the single-turn prompt (small enough to fit).
4. Re-enable `[agents.process_inbox] enabled = true`; rerun `agents-sdk/schedules/install_schedules.sh`.
5. Test on a fresh inbox.

Cost after Path B: **$0.00/run** regardless of file count, pattern matches existing `flush.py` / `vault_synthesizer.py` / `meta_agent.py` agents.

## [3.17.3] - 2026-04-29

### Changed

- **`process-inbox` round 2 adjustments after first scheduled fire trip-cap.** First scheduled run on 2026-04-29 09:00 ET burned $1.23 / 30 turns moving zero files (the agent over-read on-demand artifact pointers before touching the inbox). Three surgical fixes applied: (a) on-demand SOUL/operating-model pointers dropped from `[artifacts.per_agent.process_inbox]` — HEARTBEATs alone preserved for routing context; (b) `max_turns` 25 → 40 and `max_budget_usd` $1.20 → $1.80 (matches Past Landmine #4 in `life-systems/SOUL.md` — "raise the cap, don't retry harder"); (c) task prompt now leads with a `BUDGET DISCIPLINE` block and `PROCESS FILES SERIALLY — one at a time` directive, capping tool calls per file at ~4 (Read → Edit → Write → optional confirm).
- `#triage/research-candidate` flag rule preserved in `build_artifact_preamble` — research-fleet tagging still works without the on-demand artifact bodies inline.
- Empty-inbox Python short-circuit unchanged ($0 cost when nothing to process).

### Cost trajectory

| Run | Inbox state | Turns | Cost | Files moved |
|---|---|---|---|---|
| 2026-04-28 dev test #1 | empty | 21 | $0.65 | 0 (cap trip) |
| 2026-04-28 dev test #2 | empty | 19 | $0.91 | 0 (cap trip) |
| 2026-04-28 dev test #3 | 9 files | 22 | $0.87 | 0 (cap trip) |
| 2026-04-29 first scheduled | 9 files | 30 | $1.23 | 0 (cap trip) |
| **Target** (round 2): | 9 files | ≤40 | ≤$1.80 | 9 |

If round 2 also trips: next move is NOT another bump — it's a Path B rewrite to local `gemma4:e4b` via `routing.task_map.inbox_triage` ($0/run, validated +7.5pp quality vs phi4-mini in Phase 6 A.7).

### Pending soak gate (revised)

- Sunday 2026-05-03 09:00 ET — first round-2 fire. Watch `vault/90_system/agent-logs/process-inbox-2026-05-03.log` for `status=success`, `cost < $1.80`, and files actually moved out of inbox.

## [3.17.2] - 2026-04-28

### Added

- **`process-inbox` SDK agent re-enabled** with operating-model artifact wiring. Disabled since 2026-04-09 due to SDK v0.1.56 transport bug; re-enabled now that v0.1.63 closes that bug. Schedule moved daily 05:30 → twice weekly Sundays + Wednesdays at 09:00 ET (`StartCalendarInterval` array of two dicts). Active SDK agent count `6 → 7`.
- **Operating-model wiring for `process_inbox`.** `[artifacts.per_agent.process_inbox] = { heartbeats = true, on_demand = ["SOUL", "operating-model"] }` — all 3 domain HEARTBEATs always-on for routing decisions; on-demand reads of `life-systems/SOUL.md` (named consumer per its frontmatter) and `life-systems/operating-model.md` (Active Leverage Points → research fleet awareness).
- **`#triage/research-candidate` tag.** When inbox items match the future-research-fleet topic register (crypto, prediction markets, x402, agentic commerce, AI tooling, autoresearch), the agent now adds this tag for downstream consumption by Sean's planned research agents (Perplexity API, Gemini Deep Research MCP, NotebookLM MCP, agentkit).
- **Python empty-inbox short-circuit.** `run()` now skips the SDK call entirely when the inbox has no non-dotfiles (apart from `.gitkeep`). Empty runs cost $0; previous tests showed an LLM-based empty check spending $0.65–$0.91 over 19–21 turns reading on-demand artifacts unnecessarily.
- **`AUDIT-2026-04-28-process-inbox-reenable.md`** — full re-enable record (test runs, cost projections, rollback ladder, soak gates).

### Changed

- `agents-sdk/agents/process_inbox.py`: bumped `MAX_TURNS` 15 → 25 and `MAX_BUDGET_USD` $0.25 → $1.20 to absorb the artifact preamble + per-file routing context. Real-load test (9 files) hit the prior 0.85 cap at turn 22 — the bump aligns with `life-systems/SOUL.md` Past Landmine #4 ("when a useful agent is bumping a cap, raise the cap"). Corrected docstring claim from "100% local via phi4-mini-reasoning" to honest "Cloud Sonnet via `claude_agent_sdk.query()`".
- `agents-sdk/schedules/com.sean.agent.process-inbox.plist`: schedule changed from single `StartCalendarInterval` dict (daily 05:30) to array of two dicts (Sun + Wed 09:00 ET). `plutil -lint` passes.
- Cost ceiling delta: pre-disable burned ~$9.30/month for 0/6 success rate. Worst-case after re-enable: $1.20 × 8 runs/month = $9.60. Realistic mix (some empty, some heavy): ~$3–5/month for actual triage output.

### Pending soak gates

- First scheduled fire: Wednesday 2026-04-29 09:00 ET. First three runs (through Sunday 2026-05-10) under cap = stable.
- launchd plist needs `launchctl bootout` + `bootstrap` to pick up the new schedule. Rerun `agents-sdk/schedules/install_schedules.sh` from a fresh shell.

## [3.17.1] - 2026-04-27

Phase 3 of the agent-wiring rollout closed. `meeting_defender` deleted; `sprint_health` autonomous wiring superseded by a new `sprint-health` skill. Skill total `113 → 114`; autonomous SDK agent total `13 → 12` (still 6 active). The 2026-04-09 audit remains the canonical record for the still-disabled fleet — no other agent re-enabled.

### Rationale

Re-evaluating Phase 3 against the post-v3.17.0 reality: Daily Driver morning already lists the day's meetings via interactive MCP and there is no Sean-side demand for an auto-decline / draft-Slack-DM workflow, so `meeting_defender` was removed completely. Sprint health's valuable shape isn't a Friday-3PM autonomous report — it's an ad-hoc "where are we on Epic X?" status check, which Sean's own `vault/05_atlas/operating-models/the-block/schedule-recommendations.md` flagged as a gap ("No `sprint-health` skill yet"). Built as a skill instead, sidestepping the browser-OAuth-MCP-in-headless constraint that originally blocked the autonomous form.

### Added

- `.claude/skills/sprint-health/SKILL.md` — Block-specific ad-hoc Jira status check. Triggers: "where are we on PRO-XXXX", "sprint health", "what's stuck", "anything stale", pre-standup / pre-1:1 / pre-bi-weekly P&E sanity checks. Reuses the Block Jira config from `jira-automation` (PRO / RBS / BE projects, Cloud ID `9660d87e-3943-45c9-82bd-ce963410b29e`). Read-only Atlassian MCP — `searchJiraIssuesUsingJql` for rollups, `getJiraIssue` for Story detail; never auto-comments / auto-transitions. Computes percent complete, stale (>3d sprint / >5d cross-project), at-risk (stale | unassigned | NeedsDesign on non-Design story), blocker / dependency-risk signals. Output format leads with the headline metric, summarizes Done lists, and only spells out items needing attention. Closes with one recommendation. Added to the `pm-workflows` export-group manifest (count `13 → 14`).

### Removed

- `agents-sdk/agents/meeting_defender.py` — autonomous Monday-7AM calendar audit / draft-Slack-DM agent. Never produced output (per the 2026-04-09 audit) and superseded by Daily Driver morning's existing calendar surfacing.
- `agents-sdk/schedules/com.sean.agent.meeting-defender.plist` — orphaned launchd schedule (was not loaded; not referenced in `install_schedules.sh`).
- `[agents.meeting_defender]` config block in `agents-sdk/config.toml`.

### Retained (dormant)

- `agents-sdk/agents/sprint_health.py` and `agents-sdk/schedules/com.sean.agent.sprint-health.plist` remain in the repo at `enabled = false`. Not loaded into launchd and never produced output even when enabled. Zero maintenance cost; future cleanup is one `git rm` away if desired. The active form of "sprint health" is now the skill above.

### Changed

- `vault/20_projects/prj-superuser-pack/prj-agent-wiring-rollout.md` — Section 5 rewritten ("Phase 3: Closed 2026-04-27"). Frontmatter `phase-3-status` updated. Section 1 executive summary, Section 6 doc-update list, Section 8 Risk #10, Section 9 Q4 decision, Section 10 effort estimate, and the live-status block all updated to reflect closure.
- `CLAUDE.md` — skill count `113 → 114`; autonomous SDK agent count `13 → 12`; the operating-model wiring paragraph's Phase 3 line now describes the closure rather than the freeze.
- `README.md` — same skill / agent count updates; `pm-workflows` row count `13 → 14` with "Jira status checks" added to the highlights.

### Doc updates verified

- [x] `CHANGELOG.md` — this entry
- [x] `CLAUDE.md` — counts + Phase 3 line in operating-model paragraph
- [x] `README.md` — counts + pm-workflows table row

### Rollback

- Restore `meeting_defender.py` + plist + config block from `git show 56decb0~1:` and run `launchctl bootstrap` if Sean ever wants the autonomous version back. (No reason to expect this.)
- The skill is additive; removal is `rm -rf .claude/skills/sprint-health` plus dropping it from `export-groups/02-pm-workflows/playground.json`.

## [3.17.0] - 2026-04-27

Two independent features landed in a single merge commit (`19a805e`): **agent-wiring Phase 2** (the headline) and **knowledge-loop Phase B** (consumer-side activation). They have zero file overlap and were sequenced this way because Phase B was held on its branch until Phase 2 cleared the Phase 1 soak. A new soak window now runs through **2026-05-01** to validate Phase 2 in production; **knowledge-loop Phase A is held until that soak closes**. See "Pending merges" below.

### Agent-Wiring Phase 2 — domain-aware local-model prompts

Phase 2 of the agent-wiring rollout. After the 4-day Phase 1 soak closed clean (all four gates PASS, mean cost $0.44 / run, zero forbidden-tone hits), three of the still-active fleet agents (`meta_agent`, `flush`, `knowledge_lint`) now consume operating-model artifacts so their local-model prompts are domain-aware. Phase 3 (`meeting_defender`, `sprint_health`) stays spec-only and frozen per the 2026-04-09 audit.

All Phase 2 work is **local-only** — the three agents call `gemma4:e4b` on Mac Mini (or Qwen3-14B on MacBook Pro for ≥100-msg flush sessions). No cloud egress of SOUL or schedule-recommendations content. Pre-flight against five historical session transcripts with the SOUL prepend produced 5 / 5 valid JSON on `gemma4:e4b` — Risk #5 from the rollout plan cleared.

### Added

- `agents-sdk/agents/meta_agent.py` — `build_schedule_recs_context(config)` loads all three domain `schedule-recommendations.md` bodies via `artifact_loader`. New gemma4:e4b summarization path on Mac Mini (`_default_summary_caller`, `_SUMMARY_PROMPT_TEMPLATE`, `_parse_summary_json`, `render_domain_aware_section`, `generate_domain_aware_summary`) produces a "Domain-Aware Insights" section that ranks fleet activity against Sean's Protect / Automate / Decline lists per domain. Section is spliced between Active Agent Health and Infrastructure; LLM failures fall back to a sentinel line so the static report still ships intact.
- `agents-sdk/agents/flush.py` — `build_soul_prepend(config)` prepends all three domain SOUL bodies to `EXTRACTION_PROMPT` when `[artifacts.per_agent.flush]` lists `SOUL` in its `on_demand` array. Locked decision per plan §9 Q3 (2026-04-23): always load all three, no domain-inference helper. Framing markers (`--- BEGIN OPERATING-MODEL SOUL CONTEXT ---` / `--- BEGIN SESSION TRANSCRIPT EXTRACTION ---`) keep the regions visually separable. JSON output schema, recursion guard, FileLock, and routing-tier logic are unchanged.
- `agents-sdk/agents/knowledge_lint.py` — `build_soul_context(config)` and `_build_tier2_prompt(soul_context)` plumb three-domain SOUL bodies into the Tier-2 LLM prompt. New `LintIssue` kind `soul-tier-a-conflict` at severity `HIGH` flags vault articles whose claims contradict any Tier-A SOUL item. `run_tier2()` parses both `contradictions` and `soul_conflicts` from the LLM response.
- `agents-sdk/tests/test_meta_agent_artifacts.py` — 17 tests covering schedule-recs context loading, JSON parsing, render fallbacks, dry-run path, and end-to-end LLM-caller integration with mock callers.
- `agents-sdk/tests/test_flush.py` — +11 tests under `TestBuildSoulPrepend` and `TestRunFlushSoulPrepend` covering toggle paths, SOUL prepend ordering, framing markers, missing per-domain artifacts, and JSON-output-shape stability.
- `agents-sdk/tests/test_knowledge_lint.py` — +12 tests under `TestBuildSoulContext`, `TestBuildTier2Prompt`, and `TestRunTier2SoulConflicts` covering toggle paths, the new `soul-tier-a-conflict` issue kind at HIGH severity, exception safety, and skip-on-empty-file handling.

### Changed

- `agents-sdk/config.toml` — `[artifacts.per_agent]` Phase 2 entries uncommented: `meta_agent = { on_demand = ["schedule-recommendations"] }`, `flush = { on_demand = ["SOUL"] }`, `knowledge_lint = { on_demand = ["SOUL"] }`. Same instant rollback as Phase 1: flip `[artifacts].enabled = false` to disable all artifact wiring fleet-wide.
- `agents-sdk/agents/flush.py` — `run_flush()` gains an optional `config: Config | None = None` parameter. When `None`, behavior matches pre-Phase-2 exactly (no SOUL prepend) so existing callers and tests are unaffected. `main()` passes `cfg` through.
- `agents-sdk/agents/meta_agent.py` — `generate_fleet_report()` gains optional `config` and `summary_caller` parameters. Health-check helper now receives an empty dict (`health_cfg`) so the legacy signature is unchanged. `main()` loads `Config` once and threads it through.
- `agents-sdk/agents/knowledge_lint.py` — `run_tier2()` gains a `soul_context: str = ""` parameter. `main()` builds the context via `build_soul_context(cfg)` and passes it through; production `llm_caller` default stays `None` (Tier-2 LLM remains opt-in via the existing injection point — wiring a default caller is downstream work).

### Stale-comment cleanup (gemma4:e4b production routing — v3.14.3 inbox_triage swap)

- `agents-sdk/agents/flush.py` — module docstring, `RoutingTier.SIMPLE` enum comment, `_concat_messages` window note, and the `router.route("inbox_triage")` inline comment now correctly say `gemma4:e4b on Mac Mini`. Prior `phi4-mini` references were stale relative to the 2026-04-18 routing swap.
- `agents-sdk/agents/meta_agent.py` — module docstring updated from `phi4-mini-reasoning for summary generation` to `gemma4:e4b for summary generation, local Ollama`.
- `agents-sdk/agents/knowledge_lint.py` — Tier 1 docstring no longer claims `phi4-mini-reasoning`; Tier 1 is and always was pure-Python structural checks.
- Live `task_map` entries for other tasks (`anki_cards = phi4-mini`, `financial_analysis = phi4-mini-reasoning`) are unchanged — the v3.14.3 swap was scoped to `inbox_triage`.

### Decisions locked 2026-04-27

- **Production model for Phase 2 = `gemma4:e4b`.** Pre-flight diagnostic against five historical transcripts produced 5 / 5 valid JSON with SOUL prepend (vs 0 / 5 against `phi4-mini-reasoning`, whose `<think>` chain-of-thought behavior fights structured-output prompts). The production routing already targets `gemma4:e4b` via `inbox_triage`, so flush carries no behavior change for the SIMPLE tier.
- **`meta_agent` newly calls `gemma4:e4b`.** Today's meta-agent has no LLM path; this release wires one for the domain-aware insights section. Local-only, no cloud egress.
- **`knowledge_lint` Tier-2 `llm_caller` stays opt-in.** Phase 2 delivers the SOUL context plumbing and new issue kind; wiring a default caller into production is intentionally out of scope.

### Gate-check status

| Gate | v3.16.0 | v3.17.0 |
|------|---------|---------|
| `python3 scripts/validate.py` | PASS | PASS (58 warnings, all pre-existing) |
| `pytest agents-sdk/tests/` | 134 passed | **177 passed** (+43 new / extended) |
| Pre-flight JSON-shape guard (5 transcripts × gemma4:e4b + SOUL) | n/a | **5 / 5 PASS** |
| Phase 6 producer-side loop (flush → synthesizer → knowledge-lint) untouched | PASS | PASS — flush JSON shape preserved; vault_synthesizer not modified |
| No regression in disabled agents | PASS | PASS — 6 disabled agents stay disabled |

### Rollback

- **Instant (config-level):** flip `[artifacts].enabled = false`. All three Phase 2 prepends + the meta_agent insights section become no-ops.
- **Per-agent:** remove the agent's entry from `[artifacts.per_agent]`.
- **Code-level:** revert this release's commits.

### Knowledge-Loop Phase B — SessionStart index injection (consumer-side activation)

Activates the consumer side of the Phase 6 knowledge loop. Every new Claude Code session in this repo now starts with `vault/knowledge/index.md` pre-loaded as `additionalContext`, so Claude opens each session knowing which concept and connection articles exist before you type anything. This pairs with the producer side (SessionEnd flush → nightly synthesizer → weekly knowledge_lint) to close the read-side loop.

Merged ahead of knowledge-loop Phase A because it has **zero file overlap** with the active Phase 2 soak — only a new hook, a new `SessionStart` block in `settings.json`, and a new `[knowledge_index]` block in `config.toml`. None of those touch the three Phase-2 agents.

#### Added (Phase B)

- `.claude/hooks/session-start-inject-index.sh` — bash hook that reads `vault/knowledge/index.md`, truncates to `KNOWLEDGE_INDEX_MAX_CHARS` (default 15,000), and emits the SessionStart `additionalContext` JSON contract on stdout. File-read-only (no LLM calls), graceful empty-state stub when the index is missing or contains only the `_(none yet)_` placeholder rows, exit-0 policy. Test override via `KNOWLEDGE_INDEX_PATH` and `KNOWLEDGE_INDEX_MAX_CHARS` env vars. The current live `vault/knowledge/index.md` only has placeholder rows, so the hook emits the empty stub today; it switches to full content automatically on the next vault_synthesizer run that produces real articles.
- `agents-sdk/tests/test_session_start_inject.py` — 5 tests covering missing-index empty stub, placeholder-only index empty stub, populated index full content, oversize truncation to exactly the configured `max_chars`, and JSON output schema validation against the `hookSpecificOutput.{hookEventName, additionalContext}` contract.

#### Changed (Phase B)

- `.claude/settings.json` — new `SessionStart` hook block with `timeout: 5000` (5 s).
- `agents-sdk/config.toml` — new `[knowledge_index]` block with `inject_on_session_start = true`, `max_chars = 15000`, `path = "vault/knowledge/index.md"`. Independent of `[artifacts]`; this hook does not touch artifact-loader state.
- Hook count `11 → 12` in `CLAUDE.md` and `README.md`. New paragraph in `CLAUDE.md` under Architecture documents the consumer-side activation alongside the existing operating-model artifact wiring note.

#### Rollback (Phase B)

- **Instant:** remove the `SessionStart` block from `.claude/settings.json` (or set `[knowledge_index].inject_on_session_start = false` for the documented kill-switch). Index injection stops on the next session start.
- **Code-level:** delete `.claude/hooks/session-start-inject-index.sh` and the `[knowledge_index]` block.

### Pending merges — Knowledge-Loop Phase A

**Held until 2026-05-01.** `knowledge-loop/phase-a` (commit `4ca4413`) carries the PreCompact safety-net flush — a new `.claude/hooks/pre-compact-flush.sh` hook plus a `--trigger {session-end,pre-compact,manual}` argparse argument on `agents-sdk/agents/flush.py` that flows into the daily-log session `tag` field.

**Why we're waiting.** Phase A modifies `flush.py`, the same file Phase 2 just modified with the SOUL prepend. Phase 2's soak observes flush.py behavior in production through 2026-05-01 (Friday). Even though Phase A's changes (argparse + tag field) and Phase 2's changes (`EXTRACTION_PROMPT` body) are in different code paths and don't conflict semantically, merging Phase A mid-soak would:
1. Shift every daily-log session entry's `tag` field from the legacy hard-coded `"auto"` to a real trigger value (`"session-end"`, `"pre-compact"`, etc.). Soak observers reading daily logs would have to mentally separate "is this difference from Phase 2 or from Phase A?"
2. Add a new event source (PreCompact-fired flushes) that the Phase 2 soak isn't designed to evaluate.

By precedent (the Phase 1 soak-safety rule that held both knowledge-loop branches off `main` until Phase 2 shipped), we hold Phase A through this second soak window. Phase A will land cleanly after the 2026-05-01 review — its `flush.py` change is additive to a different section of the file and rebases trivially onto post-Phase-2 main.

**Hook count after Phase A merges:** `12 → 13`. The Phase A merge commit will resolve that bump.

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

### Coordination — knowledge-loop consumer plan (added 2026-04-25)

A second plan, `vault/20_projects/prj-superuser-pack/prj-knowledge-loop-consumer.md`, operates on the same agentic workflow and modifies overlapping files (`flush.py`, `knowledge_lint.py`, `daily_driver.py`, `config.toml`). Both plan files now carry a "Coordination" section documenting the canonical merge order and two file-conflict watch points (`flush.py` two-section additive merge; `knowledge_lint.py` touched three times — Phase 2 → C → D, must land in that order).

Branches `knowledge-loop/phase-a` and `knowledge-loop/phase-b` were created from `main` at `f4df51f` on 2026-04-25 so the lowest-risk consumer phases (PreCompact safety net + SessionStart index injection) could be developed in parallel without touching the active Phase 1 soak. Merges held until agent-wiring Phase 2 cleared. **Phase B landed in v3.17.0 alongside Phase 2; Phase A is held until the 2026-05-01 Phase 2 soak review** — see v3.17.0 "Pending merges" for the rationale. Knowledge-loop Phase D will be gated last because it modifies `daily_driver.py` morning brief.

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
