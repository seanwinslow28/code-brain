---
title: fusion-discovery-council — Phase 4 (Extended Collectors + Fetch Hardening) Field Report
date: 2026-06-21
status: complete
branch: feat/fusion-discovery-council-phase4
plan: ../../../../docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase4.md
phase3_report: 2026-06-20-fusion-discovery-council-phase3-field-report.md
baseline_commit: 0d25159
head_commit: fe578ad
commits: 11
test_status: 114 passed, 1 skipped
validate: PASSED (clean on changed files)
live_e2e: standard $1.14 (<$1.50), deep $1.12 (<$4.00) — both under cap, no bump
merged: false
---

# fusion-discovery-council — Phase 4 Field Report (detailed)

**One-line:** All nine Phase-4 tasks landed green via subagent-driven TDD (implement → spec review → code-quality review per task), then a broad opus whole-branch review. Stage-1 GATHER is now widened with **three free, fabrication-gate-compatible collectors** (review sites + competitor-weakness mining, GitHub Issues, Stack Exchange Q&A), tier-gated per spec §6; the shared fetch helper is SSRF-hardened; Sonar evidence is strengthened to verbatim quotes; the two §7b code nits are folded; and a load-bearing cost-integrity regression guard is in place. Suite **114 passed, 1 skipped** (was 93+1); `scripts/validate.py` **PASSED**. The Sean-approved live cap re-check confirmed both wider tiers land well under cap (**standard $1.14, deep $1.12**) and that the new collectors fire tier-gated. §7 is the carry-forward into Phase 5.

---

## 1. Executive summary

Phase 4 was **pure additive hardening** of the existing `council/discovery/` subpackage — no new stages, no new lens, no Fusion change. It widened the evidence surface and hardened the fetch path that surface now leans on.

- **11 commits** off plan baseline `0d25159` (9 task implementations across 10 commits + 1 final-review fix). Touches `gather/web.py`, `tiers.py`, three new `gather/{reviews,github,qa}.py` collectors, `gather/sonar.py`, `gather/__init__.py`, `fusion.py`, `gather/last30.py`, `SKILL.md`, `CHANGELOG.md`, and test files. **`verify.py` (the fabrication gate) was never touched** — confirmed by an empty diff over the whole range.
- **Test suite: 93 → 114 passed, 1 skipped** (+21 net-new tests). The single skip is the pre-existing `INTEGRATION=1`-gated live test (`test_e2e.py`), unrelated to this work.
- **`scripts/validate.py`: PASSED** — clean on every changed file (the 62 pre-existing secret-pattern warnings are all in unrelated vendor/skill files).
- **Every task passed both review stages on the first implementation pass.** No implementer returned BLOCKED or NEEDS_CONTEXT; no task required a re-dispatch. The plan carried complete, current-file-grounded code, so implementers reconciled-and-verified against the live files rather than designing.
- **Live cap re-check (the only spend, ~$2.26 total):** standard **$1.14** < $1.50, deep **$1.12** < $4.00. No cap bump. Per-collector `gather_status` confirms the §6 matrix fires live.
- **Method:** `superpowers:subagent-driven-development`. Fresh implementer subagent per task; two-stage review per task (a spec-compliance reader + a code-quality reviewer), each verifying against the real diff, not the implementer's report. Tasks ran **strictly sequentially** — Task 1 (SSRF) had to precede Tasks 3/6/7 (which widen the fetch surface), and Task 2 (tier flags) had to precede Task 7 (which reads them). Closed with a broad whole-branch review on opus.

## 2. What shipped, by commit

| Commit | Task | What | Tests after |
|---|---|---|---|
| `9cbdaa7` | 1 | **SSRF/redirect allow-list in `_simple_fetch`.** New `_is_safe_fetch_url` + `_resolve_ips`; manual per-hop redirect following (`follow_redirects=False`, `_FETCH_MAX_REDIRECTS=3`) validating scheme + resolved public-IP of the initial URL **and every hop** before connecting. Blocks `file://`/`gopher://`/`ftp://`, loopback/private/link-local incl. `169.254.169.254` cloud-metadata, and redirects into them. | 97 |
| `e2b7e73` | 2 | **TierConfig flags** `reviews`/`github`/`qa` (appended with defaults; frozen-dataclass-safe). Matrix: quick none / standard reviews+github / deep +qa. | 98 |
| `1e7da4c` | 3 | **Review-sites collector** (`gather/reviews.py`) — Brave site-targeted query biased to low-star/negative language across G2/Capterra/Trustpilot/ProductHunt/App Store/Play; complaint-sentence extraction. Reuses `_default_brave_search`/`_simple_fetch`/`extract_quotes` (no second Brave client). | 102 |
| `4fbcf39` | 4 | **GitHub Issues collector** (`gather/github.py`) — free Search API (`/search/issues`), optional `GITHUB_TOKEN` for rate limit, issue title as verbatim quote, `reactions.total_count` as engagement. | 105 |
| `e8863e8` | 5 | **Stack Exchange Q&A collector** (`gather/qa.py`) — free `/2.3/search/advanced` (no key), question title `html.unescape`'d to a clean verbatim quote, `score` as engagement. | 108 |
| `c4919ba` | 6 | **Sonar verbatim-quote hardening** — `collect_sonar` gains `fetch=None`; when wired, the top `_VERBATIM_FETCH_LIMIT=6` citations are fetched and a true page substring replaces the synthesized sentence (falls back when the fetch yields nothing). Default `None` keeps existing behavior byte-for-byte. | 110 |
| `be11792` | 7 | **Orchestrator wiring** (`gather/__init__.py`) — the three collectors slot into the default `collectors` dict gated by `tier.reviews/github/qa`; the `sonar` entry opts into `fetch=_simple_fetch`. Dedup/status/concurrency machinery preserved; cost-integrity invariant docstring added. | 111 |
| `b1a7d11` | 8 | **§7b nits** — `_first_json_object` scans forward past a malformed leading object (string-aware); last30 `300` timeout hoisted to `_LAST30_TIMEOUT_S`. | 113 |
| `9713e6a` | 9 | **Cost-integrity guard + docs** — new `test_gather_cost_integrity.py` (a full free-collector gather records $0 discovery spend), SKILL.md §2 "extended collectors are LIVE" reconciliation, CHANGELOG Phase-4 entry. | 114 |
| `a68c4f9` | 9 | **Live cap re-check reconciliation** — CHANGELOG updated with the real figures (replacing the forward-reference "validated live (Step 6)" the per-task review flagged). | 114 |
| `fe578ad` | — | **Final-review M1** — drop the unused `_simple_fetch` import in `sonar.py`. | 114 |

**Backlog coverage from the Phase-3 field-report §7c (the Phase-4 scope):** review-sites + competitor-weakness ✅ (Task 3) · GitHub Issues ✅ (Task 4) · Stack Exchange Q&A ✅ (Task 5) · `_simple_fetch` SSRF/redirect allow-list ✅ (Task 1, landed first) · Sonar verbatim-quote hardening ✅ (Task 6) · §7b nits ✅ (Task 8) · cost-integrity guard + documented threading recipe ✅ (Tasks 7+9) · tier gating per §6 matrix ✅ (Task 2) · mandatory live standard+deep cap re-check ✅ (Task 9 Step 6).

## 3. How the execution went

Exceptionally clean. The plan was unusually complete — every task carried verbatim, current-file-grounded code and tests — so the implementer role was transcription-plus-TDD, not design. Model selection reflected that: haiku for the genuinely mechanical tasks (Task 2 dataclass fields), sonnet for the collectors and integration, opus for the final whole-branch review.

- **No execution failures.** All nine implementers returned DONE on the first pass; none went BLOCKED or NEEDS_CONTEXT; none needed a re-dispatch. Every task confirmed RED before GREEN (the cost-integrity guard, which locks already-true behavior, was mutation-verified non-vacuous: injecting a `record_spend` made it fail `0.03 ≠ 0.0`, then removal restored green).
- **The two-stage per-task review found no Critical/Important issues on any task.** All findings were Minor (polish, coverage nits, runtime-yield observations) — recorded in the progress ledger and triaged at the final review rather than churning per-task.
- **One pre-flight finding** was surfaced before Task 1: the plan's Task 6 mandates importing `_simple_fetch` into `sonar.py` "for symmetry," but it's never referenced there. Decision at the time: implement as written, let the review loop adjudicate. The final review confirmed it as a plan defect (see §3.1 / M1).
- **No scope drift.** The fabrication gate was never touched; no paid scraper was introduced; caps were not weakened; only the planned files changed.

### 3.1 The one deviation (M1 — a plan defect, not an implementation failure)

The plan's Task 6 step 3 instructed importing `_simple_fetch, extract_quotes` into `sonar.py` "for symmetry/availability." But `collect_sonar` uses the **injected** `fetch` callable, not the import, and the orchestrator (`gather/__init__.py`) imports `_simple_fetch` from `web.py` directly. So the `sonar.py` import was dead code. The opus whole-branch reviewer flagged the "for symmetry" rationale as self-undermining — *no other collector imports a helper it doesn't call, so keeping it is inconsistent, not symmetric.* Because it is an incidental implementation detail (**not** one of Sean's locked design decisions), has zero behavioral effect, and is reversible, the controller applied the fix (`fe578ad`): `from council.discovery.gather.web import extract_quotes`. Full suite stayed 114/1. This is the only place the implementation departs from the plan's literal text; revert that one line to restore the plan-as-written if desired.

## 4. Live e2e — the cap re-check (2026-06-21, Sean-approved spend)

The new collectors widen the evidence bundle → a larger Fusion prompt → potentially higher per-run cost. The Phase-3 live `quick` run was $0.36; standard/deep had never been live-tested with the wider bundle. Two runs on `"obsidian plugins" --lens pm`:

| Tier | Cost | Cap | Under? | Verified ideas | Dropped |
|---|---|---|---|---|---|
| standard | **$1.14** | $1.50 | ✅ | 5 | 1 |
| deep | **$1.12** | $4.00 | ✅ | 7 | 0 |

**Per-collector `gather_status` (from the session JSONs in `<output>/.discovery-sessions/`):**

| Collector | standard | deep |
|---|---|---|
| last30 | ok: 0 (degraded — see §5) | ok: 0 |
| sonar | ok: 15 | ok: 20 |
| web | ok: 6 | ok: 6 |
| **reviews** | **ok: 3** | **ok: 3** |
| **github** | **ok: 8** | **ok: 8** |
| **qa** | *absent — correctly not run on standard* | **ok: 8** |

This is the spec §6 matrix, confirmed live: standard adds reviews+github; deep adds reviews+github+qa; quick stays lean. All three new collectors fire, each emitting real URLs + verbatim quotes that the Stage-3 gate governs. **No cap bump needed** — caps stay $0.50 / $1.50 / $4.00.

## 5. What we learned

1. **Widening the evidence bundle barely moved cost.** Deep ($1.12) came in *essentially equal to* standard ($1.14) despite adding the `qa` collector, two extra Fusion panel models (`deepseek-v4-pro`, `mistral-medium-3-5`), a higher tool-call budget (8 vs 5), and the heavier `sonar-deep-research` harvester. Takeaway: per-run Fusion cost on this topic is **not** dominated by panel breadth or evidence-bundle size — it's dominated by the judge + the panel's own web tool-call behavior, which was modest here. The headroom under the deep cap ($1.12 vs $4.00) is large; future collector additions have plenty of budget room before a cap re-think is warranted.
2. **The fabrication-gate-compatible collector design held end-to-end.** Because every collector emits a record whose `quote` is a true substring of real fetched/returned content (review complaint sentence, GitHub issue title, HTML-unescaped SO title, Sonar verbatim-or-synthesized), the gate stayed the sole arbiter with zero special-casing. The opus reviewer traced the full path (collector `quote` → `fusion._evidence_block` → panel "copy verbatim" instruction → `verify.py` `needle in hay`) and confirmed there is no path where a collector can synthesize a quote the panel couldn't ground.
3. **Sequencing the SSRF hardening first was the right call.** Task 1 landed before any collector widened the fetch surface, so review-sites fan-out and the Sonar verbatim fetch both route through a single hardened `_simple_fetch`. github/qa hit fixed JSON API hosts (not attacker-influenced URLs), so they correctly don't need the page-fetch guard.
4. **A "complete-code" plan makes subagent-driven execution nearly frictionless** — zero re-dispatches across nine tasks — but it does **not** eliminate plan defects (M1). The value of the final whole-branch review is exactly catching the cross-cutting / plan-level issue a per-task spec review can't see.
5. **`last30` remains a zero-yield live source** (see §6). GATHER is effectively Sonar + web + the three new collectors live; the social backbone is still dark.

## 6. Failures & known-degraded paths

- **No execution failures** — all nine tasks succeeded first-pass; the final review found no Critical/Important issues.
- **`last30` contributes 0 records live** — the upstream `last30days` plugin crashes before emitting JSON (`config.get('INCLUDE_SOURCES', '').split(',')` → `AttributeError` because `INCLUDE_SOURCES` is set to an explicit null). Our collector degrades safely to `[]`, so the pipeline never crashes, but the social backbone yields nothing. This is an **external config bug**, unchanged by Phase 4 — tracked in `vault/00_inbox/tickets.md`. The 30-second unblock (set `INCLUDE_SOURCES=reddit,hackernews` in `~/.config/last30days/.env`) was **not** done this session.
- **Review collector under-yields (3 records)** — Brave collapses the OR'd multi-`site:` query in `_review_query` (Brave treats `site:` as a single filter hint, not a Boolean). Records that *do* return are real + gate-valid (correctness fine); this is yield tuning only. **Ticketed** (see §7, M2).
- **Accepted security risk (documented):** the SSRF guard has a residual TOCTOU/DNS-rebinding gap between `getaddrinfo` and the actual httpx connect — the connection isn't pinned to the validated IP. The `_resolve_ips` docstring explicitly accepts this for a personal tool whose fetch targets come from Brave, not an attacker. **If this tool ever fetches user-supplied URLs, pin the connection IP.**

## 7. Carry-forward into Phase 5 (the actionable backlog)

### 7a. Open tickets (in `vault/00_inbox/tickets.md`)
- **M2 (LOW, NEW this phase):** discovery review-sites collector under-yields — fan out to N single-`site:` queries (one per `REVIEW_DOMAIN`) instead of one OR'd query, or feed query-expansion. Correctness fine; yield tuning only.
- **(carried) discovery last30 live-blocked** by the upstream `INCLUDE_SOURCES=null` crash — config/upstream fix. Resolving it before Phase 5 turns GATHER from 2 live backbone sources into 3 before the substack lens draws on the bundle.
- **(carried) Fusion response robustness / null-content render** — pre-existing tickets, not Phase-4 scope.

### 7b. Phase 5 scope (per the plan's phasing reminder + the Phase-5 plan)
- **`substack` lens** — `frame_substack` + a handoff brief into the `substack-value-engine` skill.
- **`--segment` qualifier** — audience/segment narrowing of the discovery query.
- Phase 5 can ship independently (its plan grounds against today's collectors), **but** it now benefits from the Phase-4 widening: the substack lens draws on review/GitHub/Q&A evidence, not just Sonar + web. The Phase-5 plan flags the "Phase-4-landed-first" deltas inline — re-read those now that reviews/github/qa are live.
- Plan: `docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md`. Run it in a **fresh session** with a sibling kickoff in the shape of `docs/prompts/2026-06-20-fusion-discovery-council-phase4-execution.md`.

### 7c. Cheap follow-ons if Phase 5 touches these files (non-blocking, within-spec today)
- `gather/qa.py` / `gather/github.py`: slice-before-skip can yield `< max_results` (spec says "up to" — conformant). A one-line test for the github `reactions`-missing defensive path is cheap insurance if the file is touched.
- Consider a `# noqa`-free convention check if a strict linter is ever added to `validate.py` (the M1 dead import is now gone, so the tree is clean today).

### 7d. Deferred further (documented, not lost)
- demand-intent (autocomplete/PAA → produces queries, not URL-anchored quotes → dropped by VERIFY; better modeled later as query-expansion feeding web/reviews)
- trend-velocity feeds (no clean free API)
- Quora (anti-scraping), Canny / public roadmaps (no free API, overlaps the review-style path)
- App-Store/Play RSS, multi-site Stack Exchange (beyond `stackoverflow`)

## 8. State of the branch

- **Branch:** `feat/fusion-discovery-council-phase4` — **not merged, no PR** (per the kickoff: stay on the feature branch unless asked).
- **Range:** `0d25159..fe578ad`, 11 commits. Suite **114 passed, 1 skipped**; `validate.py` **PASSED** clean on changed files.
- **Git hygiene:** nothing of this work is left staged; the only modified working-tree files are under `vault/` (incl. the new M2 ticket), which **Obsidian-Git owns** per CLAUDE.md rule 8 — never `git add`'d by this session. The live-run ledgers went to `/tmp`; no `vault/health/` spend row was staged here.
- **Final whole-branch review (opus): Ready to merge — with the M1 fix applied (done).** No Critical, no Important.
