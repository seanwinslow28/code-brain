# fusion-discovery-council — Phase 1 Field Report & Phase 2 Inputs

**Date:** 2026-06-20
**Author:** Claude (subagent-driven build session, with Sean)
**Branch:** `feat/fusion-discovery-council` (not merged; no PR)
**Status:** Phase 1 complete + live-fire validated on the real OpenRouter key. This doc folds every finding from the build + two live runs into a Phase 2 backlog.

**Companion docs:**
- Spec: [`docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md`](../../../../docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md)
- Plan: [`docs/superpowers/plans/2026-06-20-fusion-discovery-council.md`](../../../../docs/superpowers/plans/2026-06-20-fusion-discovery-council.md)
- Captured API schema: [`council/discovery/FUSION_SCHEMA.md`](../discovery/FUSION_SCHEMA.md)

---

## 1. Executive summary

Phase 1 shipped the full vertical slice: GATHER → FUSE → VERIFY → FRAME → render, the `pm` lens, per-tool budget caps, the CLI, and the invocable SKILL.md. The mock test suite is **66 passed, 1 skipped** (the skip is a pre-existing `INTEG`-gated council e2e test). `scripts/validate.py` passes.

It is **proven end-to-end against the live OpenRouter API**, not just mocks. A `quick`-tier run on `"Claude Code for creatives"` produced **4 verified, evidence-linked pain points for $0.39** with **0 dropped by the fabrication gate** (the judge stayed grounded). See §3 for the worked example.

The headline Phase-2 facts:
- **Sonar is the only Stage-1 source currently feeding evidence.** It carried the whole run. The other two collectors (web, last30days) are not yet contributing — both are small, well-scoped fixes (§5), not redesigns.
- **Four bugs were found and fixed live** (§4); without the Sonar one the tool returned an empty ledger.
- **Two of the design spec's "verified" model IDs were wrong** and are now corrected (§7).
- The whole-implementation code review produced a **deferred punch list** (§6) that is the natural Phase-2 hardening backlog.

---

## 2. What Phase 1 delivered

New subpackage `tools/llm-council/council/discovery/`, co-located in the council package to reuse `client.py` + `budget.py`:

| File | Role |
|---|---|
| `evidence.py` | `EvidenceRecord` (frozen) + `EvidenceBundle` (dedup, url index) |
| `tiers.py` | `TierConfig` + `get_tier`; quick/standard/deep panels, caps, sonar model |
| `budget.py` (council, extended) | `record_spend(tool=)`, `tool_total_for_day/month`, `preflight_tool` |
| `fusion.py` | `fuse()` — one OpenRouter Fusion call (panel + judge) → `FusionResult` |
| `gather/last30.py` | last30days shell-out + compact-output parser (⚠️ not wired correctly — §5) |
| `gather/sonar.py` | Perplexity Sonar citation harvest (✅ fixed live — §4.1) |
| `gather/web.py` | Exa neural web search + complaint extraction (⚠️ Brave path missing — §5) |
| `gather/__init__.py` | `gather_evidence()` — concurrent, failure-tolerant orchestrator |
| `verify.py` | the **fabrication gate** (hardened live — §4.4) |
| `frame.py` | `frame_pm()` — verified points → ranked `IdeaCard`s + quote bank |
| `render.py` | `render_ledger()` — markdown idea ledger |
| `pipeline.py` | `run_discovery()` — 4-stage orchestrator + cost estimate + session JSON |
| `__main__.py` | CLI (`python -m council.discovery`) + budget gate + deep-confirm |

**Commit trail (chronological):** `7bb9cba` evidence · `cf04f4a` tiers · `0d19232` budget · `7f3a6d0` FUSION_SCHEMA · `c4ad4dd` fusion · `ef51546` last30 · `cab7fb9` sonar · `ae86358` web · `3b5b061` gather · `c6f9bc1` verify · `d29430e` frame · `66addbe` render · `95498ea` pipeline · `c71327f` CLI · `249f992` SKILL.md · `bf12e15` docs · **`a9c2bfa` gate-hardening · `eed7dcb` model-ID fix · `adcc3dc` CLI dotenv fix · `b47418b` Sonar annotations fix** (last four are the live-fire corrections).

---

## 3. Live-fire findings (the worked example)

**Command:**
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && \
uv run python -m council.discovery "Claude Code for creatives" --lens pm --tier quick \
  --output /tmp/cc-creatives-ledger.md
```

**Run #1** (before fixes): `Verified ideas: 0 · $0.00`. Empty bundle → low-signal ledger, no Fusion call. The pipeline correctly refused to fabricate. Root cause = all three collectors silently returned `[]` (§4.1, §5).

**Run #2** (after the Sonar fix): `Verified ideas: 4 · dropped: 0 · $0.39`. **15 evidence records → 4 verified pain points.**

The 4 ranked opportunities (score = intensity × (1 + distinct-source-domains)):
1. **Context loss & aggressive auto-compaction** — score 25, 4 domains (r/ClaudeCode, Hongkiat, LinkedIn, Business Insider)
2. **Usage limits & pricing transparency** — score 20, 3 domains
3. **Long-session breakdown & workflow ergonomics** — score 20, 4 domains (incl. `github.com/anthropics/claude-code/issues/35357`)
4. **Degraded trust & over-agreeableness** — score 16, 3 domains (Fortune, Medium, Reddit)

**The single most valuable output was the blind-spot map, which audited its own topic scope:**
> *"The generic term 'creatives' is referenced, but the specific workflows of non-developer creatives (UI/UX designers, copywriters, artists) are absent — the provided complaints strictly reflect developer/coder pain points."*

**Phase-2 takeaway:** public "Claude Code + creatives" discourse is overwhelmingly *developer* pain. To get genuine creative-segment signal, the topic must be reframed toward where those users post, OR a creative-specific source set must be added. The tool surfaced this honestly rather than padding — exactly the intended behavior.

**Quote-bank artifact note:** several quote-bank lines came out fragmented (e.g. a bullet split into `"- **Usage limits feel too restrictive..."` then `"** Users say..."`). This is the Sonar sentence-splitter (`_SENT` regex) cutting on `.`/markdown bullets. Cosmetic but worth a Phase-2 cleanup (§6, sonar pairing).

---

## 4. Bugs found & fixed during the live runs

### 4.1 Sonar citations moved to `message.annotations` (THE unlock) — fixed `b47418b`
- **File:** `council/discovery/gather/sonar.py`
- **Symptom:** Sonar returned HTTP 200 with grounded results (cost ~$0.006) but the collector dropped everything → empty bundle → empty ledger.
- **Root cause:** the plan assumed a top-level `citations: [url, ...]` field. The live OpenRouter Sonar response has **no top-level `citations`**; citation URLs are in `choices[0].message.annotations`, each `{"type":"url_citation","url_citation":{"url":...,"title":...}}`. (15 such annotations on the live call.)
- **Fix:** added `_extract_citations(payload)` that reads `message.annotations` url_citations (de-duped, order-preserving) with a fallback to the legacy top-level `citations`. Regression test `test_collect_sonar_reads_message_annotations` added.
- **Phase-2 note:** the **quote↔URL pairing is still positional** (sentence *i* paired with citation *i*) — Sonar's synthesized sentence is anchored to a real citation URL but is not guaranteed to be the verbatim text at that URL. Acceptable for Phase 1 (URLs are real + fetchable; the gate keeps the judge honest), but see §6 for the hardening option (WebFetch the citation and extract a verbatim quote).

### 4.2 CLI never loaded `.env` — fixed `adcc3dc`
- **File:** `council/discovery/__main__.py`
- **Root cause:** only `council/client.py` calls `load_dotenv()`, and the discovery CLI doesn't import it, so `OPENROUTER_API_KEY` (which lives only in the repo-root `.env`, not the shell env) never resolved → a live run would 401. The SKILL.md *claimed* dotenv resolution that the code didn't do.
- **Fix:** `load_dotenv()` as the first line of `main()` (`override=False`, so test fixtures still win). `find_dotenv()` walks up from `__main__.py`'s package dir to the repo-root `.env` — verified resolving `True` from the real CLI location.

### 4.3 Two invalid model IDs in `tiers.py` — fixed `eed7dcb`
- See §7. `google/gemini-pro-latest` → `~google/gemini-pro-latest`; `mistralai/mistral-medium-3.5` → `mistralai/mistral-medium-3-5`. Task 2 assertions updated to match.

### 4.4 Fabrication gate had a reverse-containment leak — fixed `a9c2bfa`
- **File:** `council/discovery/verify.py`
- **Root cause:** the as-written match was `needle in hay or hay in needle`. The `hay in needle` direction let a model embed a real short bundle quote inside a longer **fabricated** quote, cite the real URL, and pass — publishing fabricated text to the ledger.
- **Fix:** tightened to `needle in hay` only — the cited quote must be a substring of the fetched evidence text. Regression test `test_embedding_attack_fails` added. (Caught by the whole-implementation code review, not the per-task reviews — the mock suite never exercised the embedding attack.)

---

## 5. Source integration status & exact remediation

| Source | Stage | Status | Phase-2 effort |
|---|---|---|---|
| **Perplexity Sonar** | 1b | ✅ working (carried run #2) | quote-pairing hardening only (§6) |
| **Brave web** | 1b | 🔧 key present, **code missing** | ~15 lines + test (below) |
| **Exa web** | 1b | optional (no key) | already implemented; needs `EXA_API_KEY` |
| **last30days social** | 1a | 🔧 key present, **path + flag + parser wrong** | medium (below) |

### 5.1 Brave web search — wire the missing provider
`council/discovery/gather/web.py` only implements `_default_exa_search()`; `collect_web` checks `EXA_API_KEY` only. The module docstring says "Exa/Brave" but the Brave half was never built. Sean has `BRAVE_API_KEY` in `.env`.

**Drop-in for Phase 2** (Brave Search API):
```python
def _default_brave_search(api_key: str):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
                params={"q": query, "count": 8},
            )
            r.raise_for_status()
            out = []
            for it in r.json().get("web", {}).get("results", []):
                out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                            "published": (it.get("page_age") or it.get("age") or "")[:10],
                            "_text": it.get("description", "")})  # snippet only; WebFetch for full text
            return out
    return search
```
Then in `collect_web`'s provider-selection block, prefer Exa if `EXA_API_KEY` else Brave if `BRAVE_API_KEY` else `None`:
```python
if search is ...:
    if os.environ.get("EXA_API_KEY"):
        search = _default_exa_search(os.environ["EXA_API_KEY"])
    elif os.environ.get("BRAVE_API_KEY"):
        search = _default_brave_search(os.environ["BRAVE_API_KEY"])
    else:
        search = None
```
**Caveat:** Brave's `description` is a short snippet, not full page text, so `extract_quotes` will find fewer complaint sentences. For real quote density, add a `fetch=` implementation (WebFetch the `url` → extract). Brave free tier: 2,000 q/mo, 1 q/s. Add a mocked test mirroring `test_collect_web_builds_records`.

### 5.2 last30days social — correct path, flags, and parser
**My earlier "no headless CLI" claim was wrong.** There IS a real CLI; the collector just targets the wrong path and passes a flag that doesn't exist.

- **Real script path:** `~/.claude/plugins/marketplaces/last30days-skill/scripts/last30days.py`
  (collector currently checks `~/.claude/skills/last30days/scripts/...` and `~/.agents/skills/...` — both absent → `FileNotFoundError` → `[]`).
- **Real CLI interface** (`last30days.py --help`):
  ```
  last30days.py [--mock] [--emit {compact,json,md,context,path}]
                [--sources {auto,reddit,x,both}] [--quick] [--deep] [--debug]
                [--include-web] [--days N] [--store] [--diagnose] [--timeout SECS]
                [--x-handle HANDLE] [--search SOURCES] [--no-native-web]
                [--save-dir DIR] [topic ...]
  ```
- **The bug:** the collector passes `--agent`, which **does not exist** (argparse errors → non-zero exit → `[]`). `--emit compact` and `--no-native-web` **do** exist and are correct.
- **Required env:** `SCRAPECREATORS_API_KEY` (now in `.env`). Optional: `XAI_API_KEY`/`AUTH_TOKEN`+`CT0` (X), `BRAVE_API_KEY`/`PARALLEL_API_KEY` (web), `APIFY_API_TOKEN`, etc. Since the discovery CLI now loads dotenv into `os.environ` and `asyncio.create_subprocess_exec` inherits the parent env, the key will flow to the subprocess — **verify this** (and consider passing an explicit `env=` for hygiene).
- **Phase-2 fix list for `gather/last30.py`:**
  1. Update `_find_last30_script()` to include `~/.claude/plugins/marketplaces/last30days-skill/scripts/last30days.py` (and ideally glob the plugin cache dir for version-pinned copies).
  2. Drop `--agent`. Use e.g. `python3 last30days.py "<topic>" --emit compact --no-native-web --quick` (start with `--quick` for cost/latency; `--search reddit,hn,youtube` to scope sources).
  3. **Capture a real `--emit compact` sample and re-align `parse_last30_output`** — the current parser was written against an *assumed* emoji-section format. Run `--diagnose` first to confirm which sources are live given the keys, and `--emit json` to get a stable, parseable shape (JSON is far more robust than scraping the compact text — strongly consider switching the parser to `--emit json`).
  4. Mind interpreter/deps: `last30days.py` has its own dependencies (it emitted a urllib3/LibreSSL warning under system py3.9) and a `vendor/` dir — confirm it runs cleanly under whatever `python3` the collector invokes, or point it at the plugin's own interpreter.
  5. Respect cost/time: last30days can be slow and may call paid APIs (Scrapecreators). Keep the 300s timeout; default to `--quick`; surface its spend separately from the OpenRouter caps (it is **not** covered by the discovery budget module).

---

## 6. Code-review punch list (deferred → Phase 2 backlog)

From the whole-implementation review. None block Phase 1; all are real Phase-2 hardening.

**Important:**
1. **Budget isolation is one-directional.** `record_spend` always bumps the daily file's aggregate `total`, and council's `preflight` reads that `total` — so discovery spend reduces *council's* headroom, though the reverse is correctly prevented (discovery reads tool-scoped sums). Conservative (never overspends) but contradicts the SKILL.md "never cross-deplete" claim. **Fix:** route council's preflight through `preflight_tool(tool="council")` too, or compute `total` per-tool. Add a test asserting a large discovery spend doesn't change council headroom.
2. **Adopt the authoritative `usage.cost`.** The Fusion response returns exact `usage.cost` (e.g. the spike's $0.497; run #2 ≈ $0.39 actual vs the token-estimate recorded). `FusionResult` doesn't capture it; the pipeline records a conservative token+web-call *estimate*. **Fix:** add `cost: float = 0.0` to `FusionResult`, read `usage.get("cost")` in `_to_result`, prefer it in `_estimate_cost` (fall back to the estimate). Improves cap accuracy.
3. **Fusion HTTP errors are opaque + retry is ineffective for 4xx.** `resp.raise_for_status()` propagates to the CLI's generic `except` (exit 3, "Discovery failed: …") *after* gather already spent money. The retry loop only varies the system prompt — useless against a 400. **Fix:** catch `httpx.HTTPStatusError`, surface the OpenRouter error body, and don't retry on 4xx.
4. **Collectors swallow all exceptions silently** (`gather/__init__.py`, and each collector's `except`). This is exactly what made run #1's empty bundle undiagnosable. **Fix:** log per-collector exception type/repr (stderr; no secrets in these) and thread a per-collector status into the session JSON so "empty because quiet" vs "empty because errored" is distinguishable.

**Minor:**
5. `frame.py` quote-bank zip pairs `quotes[i]` with `supporting_urls[i]` positionally — can attribute a verified quote to an unrelated supporting URL. Emit only `(quote, url)` pairs that actually co-occur in the bundle (reuse the verify-stage match).
6. `sonar.py` positional sentence↔citation pairing (see §4.1) — same class of issue; consider WebFetch-per-citation for verbatim quotes.
7. `render.py` writes raw URLs into markdown without escaping — cosmetic, but angle-bracket-wrap to be safe.
8. `_estimate_cost` ignores `fr.web_calls` (uses the theoretical `panel × max_tool_calls` ceiling). Conservative; revisit alongside item 2.

---

## 7. Model panel reality (verified 2026-06-20, live)

Probed `GET /api/v1/models` (340 models) + minimal `max_tokens=1` completions.

| Tier | Panel | Judge |
|---|---|---|
| `quick` | `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro` | `~google/gemini-pro-latest` |
| `standard` | `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3` | `anthropic/claude-opus-4.7` |
| `deep` | standard + `deepseek/deepseek-v4-pro` + `mistralai/mistral-medium-3-5` | `anthropic/claude-opus-4.7` |

- **`~google/gemini-pro-latest`** — the leading `~` is OpenRouter's **floating "latest" alias**; it resolved to `google/gemini-3.1-pro-preview-20260219` on the probe. The bare `google/gemini-pro-latest` (no tilde) **400s**.
- **`mistralai/mistral-medium-3-5`** (hyphen) resolves to `mistralai/mistral-medium-3.5-20260430`. The dotted `mistralai/mistral-medium-3.5` **400s**. (Same hyphen ID already used by the council `variance` profile — corroborated.)
- **Valid as-is:** `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, all three Sonar variants.
- **Sonar stays `tools=False`** → Stage-1 gather only, never the Fusion panel (unchanged, correct).
- **Cost calibration:** the Task-4 spike (2-panel, `max_tool_calls=2`, Gemini judge, 4 web calls) cost **$0.497**; run #2 (`quick`, 3-panel, `max_tool_calls=3`) cost **$0.39**. Web-tool calls dominate; the per-run cap ($0.50/$1.50/$4.00) + daily/monthly ($10/$50) are the real guardrails. `usage.cost` is the authoritative figure (item 2 above).

---

## 8. Phase 2 build checklist (prioritized)

**Tier A — make all Stage-1 sources real (unblocks evidence breadth):**
- [ ] Wire `_default_brave_search()` so `BRAVE_API_KEY` activates web (§5.1) + add a `fetch=` for full-page quotes.
- [ ] Fix `gather/last30.py`: path + drop `--agent` + switch parser to `--emit json` + verify `SCRAPECREATORS_API_KEY` reaches the subprocess + `--diagnose` source check (§5.2).
- [ ] Per-collector status into the session JSON + stderr logging (review item 4) — so empty runs are diagnosable.

**Tier B — budget & cost integrity:**
- [ ] Symmetric per-tool budgets (review item 1).
- [ ] Capture + prefer `usage.cost` (review item 2).
- [ ] Fusion 4xx error surfacing, no-retry-on-4xx (review item 3).

**Tier C — the deferred plan scope (Phase 2/3 from the plan's own roadmap):**
- [ ] Extended tier-gated collectors: review sites (G2/Capterra/Trustpilot/App Store) + **competitor-weakness mining** (1★/2★), GitHub Issues / Canny / roadmaps, demand/intent (PAA/autocomplete), Q&A (Stack Overflow/Quora), trend velocity. Each is a new `gather/<source>.py` slotted into `gather_evidence`.
- [ ] The `substack` lens: `frame_substack()` + a handoff brief consumable by `substack-value-engine` (+ its render variant).
- [ ] Quote-bank / Sonar verbatim-quote hardening (review items 5–6): WebFetch citations to anchor true verbatim text at each URL.

**Tier D — creative-segment signal (the run-#2 insight):**
- [ ] The blind-spot map proved generic "creatives" topics return developer pain. Add creative-native sources/topic templates (design subreddits, Behance/Dribbble discourse, writing communities, YouTube creator channels) or a `--segment` qualifier that reshapes gather queries toward non-developer creatives.

---

## 9. Appendix — operational reference

**Run (current, Sonar-only until §8 Tier A lands):**
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && \
uv run python -m council.discovery "<topic>" --lens pm --tier quick|standard|deep \
  --output <ABS PATH>
```
**Tests:** `cd tools/llm-council && uv run --extra dev python -m pytest -v` (plain `uv run pytest` does **not** work — pytest is in the `dev` extra). Current: 66 passed, 1 skipped.

**Env keys (repo-root `.env`, gitignored, loaded via dotenv):**
- `OPENROUTER_API_KEY` — required (panel + judge + Sonar).
- `SCRAPECREATORS_API_KEY` — present; needed for last30days social once §5.2 lands.
- `BRAVE_API_KEY` — present; activates web once §5.1 lands.
- `EXA_API_KEY` — optional alternative to Brave (https://dashboard.exa.ai/api-keys).

**Spend:** shared `vault/health/council-spend-{YYYY-MM-DD}.json`, discovery rows tagged `tool="discovery"`. **The skill never `git add`s the vault** (CLAUDE.md rule 8); ledger files are written and left for Obsidian-Git.

**Output convention:** `vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md` (test runs went to `/tmp` to avoid vault noise).

**Last good live run:** `Claude Code for creatives`, quick, 15 evidence → 4 verified, **$0.39**, ledger `/tmp/cc-creatives-ledger.md`, session `/tmp/.discovery-sessions/20260620-132826-2e8225.json`.
