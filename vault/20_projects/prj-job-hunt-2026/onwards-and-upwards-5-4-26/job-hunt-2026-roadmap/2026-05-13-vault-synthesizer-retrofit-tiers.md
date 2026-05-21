---
type: retrofit-plan
project: prj-job-hunt-2026
artifact: vault-synthesizer-v2
created: 2026-05-13
status: tier-1-shipped-awaiting-nightly-run
companion_artifacts:
  - 2026-05-10-eval-suite-build-plan.md   # the eval suite this retrofit moves the needle on
sprint_epoch: 2026-05-04
related_intent_skill: .claude/skills/intent-engineering/SKILL.md
ai-context: "Vault Synthesizer v2 retrofit plan. Born 2026-05-13 from a query.py diagnostic session that proved the v1 synthesizer produces shallow, cluster-biased, duplicate-prone output. Four-tier remediation grounded in 2025-2026 RAG research (TopClustRAG, EDC, Karpathy LLM Wiki, Anthropic quote-first prompting). Tier 1 ships first as a prompt + formatter fix. Future Claude sessions checking synthesizer progress should read this file's status block first. 2026-05-21 update: Tier 1.5 (depth gate) fixed the descriptive *shape* of articles, but Sean's morning review of `concepts/writing-voice-modes.md` named the next-layer gap — output is still descriptive of what exists, not generative about what's missing. The follow-on work (Pattern 1 / vault_critic agent — a new SDK agent shelling out to Codex CLI + Anti-Gravity CLI nightly at 03:30 to produce sibling `vault/knowledge/expansions/{slug}.md` files) is documented in `agents-sdk/docs/multi-cli-integration-patterns.md` and summarized at the bottom of this doc under §Follow-on layer."
---

# Vault Synthesizer v2 — Retrofit Tiers

> **Future Claude / future Sean reading this:** check the **Status Tracker** at the bottom for what's done and what's next. The intent spec is the contract; the four tiers are sequenced implementations. Tier 1 is prompt + formatter only (low risk, instant rollback). Tiers 2-4 add new dependencies and execution stages — do not skip ahead.

---

## Why this exists

On 2026-05-13 morning, after a clean nightly synth run (203 concepts, 111 connections, 186 typed edges, status=ok), Sean and Claude ran [`scripts/query.py`](../../../../../agents-sdk/scripts/query.py) with discovery questions designed to test whether the synthesizer was producing cross-domain insight or just dedup'd noise. **It was producing noise.**

Specific evidence:

1. **Cluster collapse.** Of 10 chunks retrieved per query, 6-7 always came from the agent-health/automation-reliability cluster — the densest region of the concept space. The cross-domain bridging the synthesizer is supposed to deliver (life-systems × creative-studio × job-hunt × Code-Brain) never happened.
2. **"Evidence pending" hardcoded.** Discovered while reading [`agents-sdk/agents/vault_synthesizer.py:183`](../../../../../agents-sdk/agents/vault_synthesizer.py#L183) — `format_connection_article` literally writes `"Evidence pending."` as the body of every connection thread. The LLM never gets to fill it. This is a formatter defect, not a prompt-engineering problem.
3. **Slug duplication.** Same idea emitted under multiple slugs: `daily-drive-agent` vs `daily-driver-agent`, five vibe-coding variants, `daily-note-gener` (truncated mid-word), `agent-health` vs `agent-health-monitoring`. The synthesizer has no canonicalization step.
4. **Vague output schema.** The current prompt asks for `"definition: 2-3 sentences"` and `"examples: concrete from source material"` — no verbatim-quote requirement, no source-citation anchor, no cross-domain preference. Output is generic-LLM-restating-prompt shape.
5. **Weak retrieval query.** `retriever(primary_text[:2000], top_k=5)` uses the first 2000 chars of the source file — usually frontmatter + intro — as the embedding query. Pure cosine, no MMR or diversity.

These four defects mean the synthesizer is producing the tidy-looking output Sean called "bare bones" — surface area without depth, breadth without bridges.

## Research grounding (do not skip — these patterns inform every tier)

Five named patterns from 2024-2026 production RAG / knowledge-synthesis work map onto our defects. Sources are linked so future-Claude can verify the technique rather than trusting this doc.

| Defect | Pattern | Source |
|---|---|---|
| Densest-cluster retrieval bias | **TopClustRAG** — retrieve top-50 → HDBSCAN cluster → sample 2-3 per cluster | [SIGIR 2025](https://arxiv.org/html/2506.15246v1) |
| Cluster-aware k-selection | **CAR** — dynamic k per query density | [arXiv 2511.14769](https://arxiv.org/abs/2511.14769) |
| "Evidence pending" / shallow synthesis | **Quote-first `<quotes>` XML block** before any prose | [Anthropic prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Slug duplication | **EDC — Extract, Define, Canonicalize** — cosine-merge at >0.85 before write | [arXiv 2404.03868](https://arxiv.org/abs/2404.03868) |
| No cross-domain discovery | **Karpathy LLM Wiki** — `cross_domain_connections[]` requiring different PARA folder | [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) · [LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) |
| Multi-pass synthesis topology | **MA-RAG** — Planner → Extractor → QA chain-of-thought | [arXiv 2505.20096](https://arxiv.org/abs/2505.20096) |

The full research report is preserved in the session transcript at task `a5433f9b90fe46067` (2026-05-13).

---

## Intent Spec — Vault Synthesizer v2

*Built using the [intent-engineering skill](../../../../../.claude/skills/intent-engineering/SKILL.md) 9-section template. This spec is the contract every tier implements against.*

### 1. Objective

Surface **non-obvious cross-domain patterns** across Sean's vault (life-systems × creative-studio × job-hunt × Code-Brain infra) so Sean discovers ideas, contradictions, and project leverage he wouldn't notice manually. When facing trade-offs, **prioritize cross-domain discovery and evidentiary grounding** over breadth-of-coverage or output volume.

### 2. User Goal

Sean wants the vault to function as **a thinking partner that compounds knowledge over time** — connecting webclips, research, daily notes, references, and operating-model artifacts into a graph that surfaces things he didn't realize. Currently struggles with: shallow auto-generated concepts that read like restated prompts, duplicate slugs for the same idea, and zero cross-domain bridge articles.

### 3. Desired Outcomes

1. Every concept article contains **≥2 verbatim quotes** from distinct source files (no `"Evidence pending"` strings exist anywhere in `vault/knowledge/`).
2. **≥30% of connection articles are cross-cluster** — they wikilink concepts that originate in different PARA folders (job-hunt × creative-studio, life-systems × Code-Brain, etc.).
3. **Zero near-duplicate slugs** — no two concept files have definition-embedding cosine similarity >0.85.
4. Sean can run `query.py` on a discovery question (e.g., "what cross-domain pattern haven't I named?") and get an answer that cites chunks from **≥2 different top-level vault folders**.

### 4. Health Metrics

While pursuing the outcomes above, these must NOT degrade:

- **Truth anchoring** — quotes must be byte-for-byte exact substrings of cited source files. If quote fails substring validation → article rejected, not written.
- **Run duration** — must stay under 45 min/run (current ceiling). If cluster+per-cluster passes blow the budget → fall back to single-pass with quote-first prompt.
- **Connection authenticity** — cross-cluster wikilinks must be semantically real. If a cross-link's chunk-pair cosine similarity is <0.30 → drop the connection. Catches "fake cross-domain" hallucinations.
- **Cost** — stays at $0.00/run (Qwen3-14B local). If forced to Sonnet fallback >2 runs/week → alert Sean.

### 5. Strategic Context

- **System role:** Nightly producer in the knowledge loop (SessionEnd flush → indexer → synthesizer → lint → SessionStart inject). **The only place cross-domain synthesis happens.**
- **Upstream:** `vault_indexer` (embed index over all `.md` except `daily/` + system dirs), `vault/.vault-index.db` chunks table.
- **Downstream consumers:** `scripts/query.py` (Q&A tier), `knowledge_lint.py` (Sunday quality gates), `daily_driver.py` morning brief, SessionStart injection.
- **Business context:** Vault-as-SSoT is *the* extra-hour leverage point named in both creative-studio + life-systems operating models. This agent's quality directly determines whether the vault is a thinking partner or a noisy dump.

### 6. Constraints

**Steering (prompt layer):**

- Prefer cross-cluster connections over within-cluster ones when both are available.
- When uncertain whether a concept already exists, **search first, write second**.
- When a quote can't be extracted verbatim, **drop the claim** rather than paraphrase.

**Hard (architecture layer):**

- **Never write a concept file with definition-cosine >0.85 to an existing concept** — enforced by pre-write embedding check (Tier 3).
- **Never write an article body containing the string `"Evidence pending"`** — enforced by post-LLM lint, body discarded (Tier 1).
- **Never claim a quote that fails substring match against source** — enforced by validator, article rejected + logged (Tier 1).
- Budget cap stays at 45 min wall-clock + $0.00 USD → enforced in `run_synthesis` ([line 338](../../../../../agents-sdk/agents/vault_synthesizer.py#L338)).

### 7. Decision Authority

- **Full autonomy:** writing concept/connection articles, regenerating index, inserting `concept_edges` rows, merging near-duplicate slugs at cosine >0.85.
- **Guarded autonomy:** LLM-judge call on 0.70–0.85 cosine ambiguous pairs (logged, capped at 5/run).
- **Proposal-first:** none — this agent is fully autonomous.
- **Human-required:** changing corpus scope (which folders feed input), changing the intent spec itself, changing canonicalization thresholds.

### 8. Edge Cases

- **Cluster count <3 in candidate set** → fall back to single-pass with quote-first prompt; don't force fake clusters.
- **All clusters live in one PARA folder** → write articles but skip cross-domain connection pass; log `"no cross-domain candidates this run"` to manifest.
- **Quote substring validation fails for all candidate quotes** → reject the article, increment `rejected_count`, log source file for next-run debugging.
- **Embedding similarity check fails (db missing or empty)** → fall back to slug-string-match canonicalization (Levenshtein on slug).
- **MBP asleep / Qwen3-14B unreachable** → existing `WOLUnavailable` path, fall to Sonnet 4.6 with cost-cap; if cost-cap hits, write `status: success-empty` and exit.

### 9. Stop Rules & Verification

**Halt immediately when:**

- Pushover creds missing ([line 360](../../../../../agents-sdk/agents/vault_synthesizer.py#L360)) — already enforced.
- Budget exhausted mid-pass — write `status: partial-empty`, exit cleanly.

**Verification:**

- **Eval suite gate:** vs-014 (≥2 wikilinks) + new **vs-022** (no `Evidence pending` string in any vault/knowledge/ file) + new **vs-023** (cross-cluster connection rate ≥30%) must pass before run is marked OK.
- **Per-run manifest checks:** `concepts_written > 0`, no slug-collision warnings, cross-cluster rate logged.
- **Daily smoke test:** `daily_driver` morning brief reads manifest and surfaces if any health metric trended wrong.

---

## Four-Tier Implementation Plan

### Tier 1 — Prompt + formatter retrofit (90 min, ships first)

**What it changes:** Pure text/data — no new dependencies, no new code paths, instant rollback.

**Files & line refs:**

1. **[agents-sdk/agents/vault_synthesizer.py:278-328](../../../../../agents-sdk/agents/vault_synthesizer.py#L278)** — rewrite `_build_synthesis_prompt`:
   - Add quote-first `<quotes>` block requirement (≥2 verbatim quotes per concept, ≥3 per connection)
   - Add canonicalization instruction with current `vault/knowledge/index.md` titles injected: *"If a concept matches an existing one in this index, REUSE the exact slug — do not invent a new name."*
   - Add cross-domain instruction: *"Prefer connections whose member concepts originate in different top-level vault folders (life-systems, creative-studio, job-hunt-2026, 40_knowledge, 05_atlas)."*
   - Increase chunk excerpt from 200 → 800 chars (still cheap)
   - Ban `"Evidence pending"` explicitly with a forbidden-phrase list

2. **[agents-sdk/agents/vault_synthesizer.py:174-197](../../../../../agents-sdk/agents/vault_synthesizer.py#L174)** — fix `format_connection_article`:
   - Add `evidence: dict[str, list[str]]` parameter — maps concept title → list of verbatim quotes from source files
   - Replace `f"### [[{c}]]\n\nEvidence pending."` with rendered evidence quotes per thread
   - **This is the actual structural fix** — "Evidence pending" was hardcoded, not LLM output.

3. **[agents-sdk/agents/vault_synthesizer.py:134-135](../../../../../agents-sdk/agents/vault_synthesizer.py#L134)** — extend `validate_article_body`:
   - Reject any body containing `"Evidence pending"` substring (defense in depth)
   - Reject any body containing `"(to be filled)"` placeholder

4. **Update JSON schema in prompt** to require per-concept `evidence` arrays in connection objects:
   ```json
   "connections": [{
     "title": "...",
     "synthesis": "...",
     "concepts": ["Concept A", "Concept B", "Concept C"],
     "evidence": {
       "Concept A": ["verbatim quote from source", "another verbatim quote"],
       "Concept B": ["verbatim quote", "..."]
     },
     "implications": [...]
   }]
   ```

**Verification:**
- Run existing eval suite locally: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_synthesizer.py -v` — must stay green.
- Wait for next nightly 2:30 AM synth run.
- Re-run cluster-diversity query: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/query.py "Find 3 themes from THREE DIFFERENT concept clusters..."`
- **Pass signal:** answer cites chunks from ≥2 different top-level vault folders; `grep -r "Evidence pending" vault/knowledge/` returns zero matches after the next synth run regenerates files.

**Rollback:** `git checkout agents-sdk/agents/vault_synthesizer.py` — pure text revert.

**Expected impact:** kills "Evidence pending" (structural). Kills shallow output (quote-first forcing). Kills most slug dupes (canonicalization instruction with index injection). Does NOT fix retrieval bias — that's Tier 2.

---

### Tier 2 — Cluster-and-sample retrieval (4 hrs, after Tier 1 stable)

**Trigger:** Implement after Tier 1 has run successfully for ≥3 consecutive nights AND tomorrow's query.py re-run still shows agent-health-cluster dominance in the consulted chunks.

**What it changes:** Adds `hdbscan` dependency. Modifies retrieval signature. Larger blast radius than Tier 1.

**Pattern:** TopClustRAG ([SIGIR 2025](https://arxiv.org/html/2506.15246v1))

**Files & changes:**

1. **[agents-sdk/agents/vault_synthesizer.py:405](../../../../../agents-sdk/agents/vault_synthesizer.py#L405)** — replace single retriever call:
   - Retrieve top-50 by cosine (not top-5)
   - Cluster the 50 embeddings with HDBSCAN (`min_cluster_size=3`)
   - Sample 2-3 chunks per cluster → diversified candidate set of ~10-15 chunks
   - **Better query:** instead of `primary_text[:2000]`, extract H1/H2 headings + first paragraph + frontmatter `tags`/`type` from the primary file; concatenate as the embedding query.

2. **New file: `agents-sdk/lib/retrieval_diversity.py`** — `cluster_and_sample(embeddings, k_per_cluster=2)` helper.

3. **[agents-sdk/pyproject.toml](../../../../../agents-sdk/pyproject.toml)** — add `hdbscan>=0.8.40` to dependencies.

4. **New test:** `agents-sdk/tests/test_retrieval_diversity.py` — fixture with 3 obvious clusters, assert that cluster_and_sample returns chunks from all 3.

**Verification:**
- Synth manifest gains a `clusters_sampled` field; must be ≥3.
- Cross-cluster connection rate (logged in manifest) ≥30%.
- Query.py answers cite ≥2 different vault top-level folders.

**Rollback:** Revert the retriever call; remove `hdbscan` from pyproject.

---

### Tier 3 — EDC canonicalization (4 hrs, after Tier 2 stable)

**Trigger:** Implement after Tier 2 has run for ≥3 consecutive nights AND `ls vault/knowledge/concepts/ | wc -l` shows continued slug-duplication (multiple near-synonyms surviving).

**What it changes:** Adds a pre-write check that consults the embedding index. Modifies the concept-write path.

**Pattern:** Extract-Define-Canonicalize ([arXiv 2404.03868](https://arxiv.org/abs/2404.03868))

**Files & changes:**

1. **[agents-sdk/agents/vault_synthesizer.py:427-445](../../../../../agents-sdk/agents/vault_synthesizer.py#L427)** — wrap the concept-write loop with canonicalization:
   - Before writing `concepts_dir / f"{_slugify(title)}.md"`, compute the proposed definition's embedding.
   - Cosine-match against every existing concept's definition embedding (cached in `vault/.vault-index.db` chunks table, or compute fresh).
   - **>0.85** → merge: append source to existing file's `sources:` frontmatter, increment a new `merged_concepts` counter in `SynthesisResult`. Do not write a new file.
   - **0.70-0.85** → LLM judge call (max 5/run per health metric).
   - **<0.70** → new file.

2. **New file: `agents-sdk/lib/concept_canonicalize.py`** — `find_canonical_slug(proposed_title, proposed_definition, existing_concepts_dir, db_conn) -> str | None`.

3. **Schema addition:** `concept_edges` table gains an `alias_of` nullable column so historical aliases still resolve when queries reference old slugs.

4. **New eval cases:** vs-024 (EDC cosine threshold honored), vs-025 (alias_of resolves correctly).

**Verification:**
- Manifest gains `merged_concepts` field; should be >0 after the first post-Tier-3 run if dupes existed.
- `ls vault/knowledge/concepts/ | wc -l` should *decrease* on the first run (5 vibe-coding files merge to 1, etc.) and then stabilize.

**Rollback:** Revert the wrap; `merged_concepts` field becomes inert.

---

### Tier 4 — Three-pass agentic synthesis (8 hrs, post-employment)

**Trigger:** Only after Tiers 1-3 are stable and Sean has employment-side bandwidth. This is the biggest architectural change; do not ship it under sprint pressure.

**Pattern:** MA-RAG ([arXiv 2505.20096](https://arxiv.org/abs/2505.20096)) / TopClustRAG full topology.

**What it changes:** Replaces the single LLM call with three:

1. **Per-cluster draft pass** — for each cluster from Tier 2, draft one concept article using only that cluster's chunks. Pure quote-first.
2. **Cross-link pass** — read all draft articles from this run + the index; emit typed `concept_edges` only for pairs whose source clusters differ.
3. **Lint pass** — reject any article with `Evidence pending`, <2 quotes, or zero cross-cluster wikilinks; re-queue for next run.

**Expected impact:** the synthesizer becomes a real discovery engine. Cross-cluster connection rate climbs from 30% to ~70%. Articles read like Karpathy-LLM-Wiki entries, not LLM-restating-prompt fragments.

---

## Follow-on layer — Generative-critique agent (Pattern 1 / `vault_critic`)

> **Scope note:** this is NOT a synthesizer tier. It is a separate downstream agent that critiques the synthesizer's output. It is documented here because (1) it is directly born from Sean's 2026-05-21 morning review of `concepts/writing-voice-modes.md`, the same review that triggered Tier 1.5, and (2) any future session asking "why isn't the vault a thinking partner yet?" should read this section before proposing a new synthesizer tier.

### Why this is needed (the gap Tier 1.5 cannot close)

Tier 1.5 enforces structural depth — Definition ≥3 sentences, prose evidence quotes, Synthesis naming tension + consequence, etc. The depth gate has been live since 2026-05-20 and produced its first verified output on 2026-05-21 (1 concept + 1 connection survived, 2 articles rejected with stable reason codes — see Verification Log row 2026-05-21).

But Sean's complaint on the same morning, after reading the surviving `writing-voice-modes.md`, was: *"I'm seeing an agent writing down facts about what is already in existence instead of expanding upon them. For example: I'm looking for the agent to tell me how I can make it BETTER. What am I not doing with that skill that I should be incorporating? What did I not think of?"*

The synthesizer is grounded in the vault corpus. Every quote it surfaces is a verbatim substring of an existing source file. By design, it cannot say *"here is what you're missing"* because it has no external reference frame to compare against. No amount of depth-gate tightening will fix this — it is the wrong tool for the job. The synthesizer's job is to faithfully describe the corpus; the missing piece is a *separate* agent whose job is to critique the corpus from outside.

### The minimum viable architecture

Three patterns are specced in [`agents-sdk/docs/multi-cli-integration-patterns.md`](../../../../../agents-sdk/docs/multi-cli-integration-patterns.md), built on a 2026-05-21 smoke test confirming that:

- **Codex CLI** v0.130.0 (gpt-5.5 with medium reasoning) accepts headless prompts via `codex exec --sandbox read-only --skip-git-repo-check "PROMPT"`, runs from a trusted working directory (`cwd=Path.home()`), and returns raw markdown on stdout in ~21s on the writing-voice-modes critique test. Cost: $0 incremental on ChatGPT Plus.
- **Anti-Gravity CLI** v0.42.0 (Gemini 3.1 Pro via `auto-gemini-3` router; replaced the legacy `gemini` binary on May 19, 2026) accepts headless prompts via `GEMINI_CLI_TRUST_WORKSPACE=true gemini -p "PROMPT" --output-format json --approval-mode plan` and returns clean JSON `{session_id, response, stats}` in ~43s on the same test. Cost: $0 incremental on Google personal-OAuth.
- Both CLIs independently named **Joan Didion / *The White Album*** as the #1 missing voice mode for Sean's writing-voice-modes skill — the convergence signal is itself a "you genuinely need this" indicator. Non-overlapping recommendations were complementary, not redundant (Codex: McPhee + Maggie Nelson; Anti-Gravity: Baldwin + Byung-Chul Han).
- Smoke artifacts persisted at [`agents-sdk/docs/multi-cli-smoke-2026-05-21/`](../../../../../agents-sdk/docs/multi-cli-smoke-2026-05-21/) — 5 files including critique-prompt.md (the verified prompt template), codex-out.txt / gemini-out.json (the verbatim outputs for use as test fixtures), and the two stderr captures.

**Pattern 1 (the recommended first ship)** wraps both CLIs in an SDK agent at `agents-sdk/agents/vault_critic.py` that runs on launchd at **03:30 daily** — after vault_synthesizer (02:30) and deep_researcher (02:45), before daily_driver (08:30) and meta-agent (08:45). The agent:

1. Reads the night's Mac-Mini-canonical synth manifest (`vault/health/synth-manifest-{today}.json`).
2. Filters target articles to ONLY those Mac Mini wrote — defending against PR-merge contamination of the kind that surfaced 2026-05-21 (PR #52 dropped 88 pre-Tier-2 MBP files into vault/knowledge/, polluting any naive `ls -lt` sampling). The filter cross-references the auto-commit's file list, per memory [`feedback_synth_verify_filter_to_manifest.md`](../../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_filter_to_manifest.md).
3. Selects up to **3 newly-written concept articles** per night (rate-cap-protective hard cap).
4. For each, fans out two parallel subprocess critiques (one to Codex CLI, one to Anti-Gravity CLI) using the smoke-test prompt template, with explicit trust flags + sandbox modes + per-call timeouts.
5. Writes a sibling expansion file at `vault/knowledge/expansions/{slug}.md` with frontmatter `type: expansion`, `parent: [[{original-slug}]]`, both critiques rendered side-by-side under `## From Codex (gpt-5.5)` and `## From Anti-Gravity (Gemini 3)`.
6. Writes a per-run manifest at `vault/health/critic-manifest-{date}.json` with counts, durations, token totals per CLI, and `status: ok | partial | error`.
7. Appends one row to `vault/90_system/agent-logs/agent-run-history.csv` via `record_run`.
8. Surfaces results in daily-driver's morning brief (under Vault Health) and in meta-agent's fleet-status report.

### Why Pattern 1 first, not Patterns 2 or 3

- **Pattern 2** (add Codex + Anti-Gravity adapters to the existing LLM Council at `tools/llm-council/`) is also high-value but reuses infrastructure that doesn't directly answer the "thinking partner" complaint. Plan to ship after Pattern 1 has run ≥1 week.
- **Pattern 3** (extend `agents-sdk/lib/hybrid_router.py` to route per task-class across all four backends — Claude API, Codex, Anti-Gravity, local Qwen) is the right long-term architecture but premature now. Ship only if Pattern 1 produces evidence that the single-backend routing in the current fleet has actual quality gaps worth a routing layer to solve.

### Cost + safety guards (mandatory before launch)

- **Cost cap:** $0 incremental on Sean's existing personal subscriptions. No Anthropic SDK calls in the nightly path. Sonnet fallback is **out of scope for v1** — if both CLIs rate-cap, the agent marks `status: partial` and exits cleanly. This is intentional: it isolates Pattern 1 from any cloud-API blast radius.
- **Wall-clock budget:** 600s soft cap (smoke test showed ~45s per article × 3 articles ≈ 135-180s expected — comfortable headroom).
- **Trust gates:** both CLIs refuse to run from untrusted working directories. The wrappers MUST set `--skip-git-repo-check` (Codex) and `GEMINI_CLI_TRUST_WORKSPACE=true` (Anti-Gravity) explicitly per invocation. Silent reliance on inherited env is a latent bug.
- **Sandbox modes:** Codex `--sandbox read-only`, Anti-Gravity `--approval-mode plan`. Both verified safe in the smoke test. No exceptions in the nightly path.
- **Rate-cap behavior:** if one CLI returns a rate-cap-shaped error, the OTHER CLI's response is still written; manifest captures which CLI capped; no retry within the same run.
- **Convergence detection:** when both CLIs name the same author/work (Didion appeared in both smoke runs), surface as a "🔁 Both reasoners agreed on …" callout in the expansion file. Cheap string-match; high signal for Sean.

### Implementation status (2026-05-21)

The integration patterns doc is written and the smoke tests passed. The next step is a structured implementation plan via the [`writing-plans`](../../../../../.claude/skills/superpowers/writing-plans/) skill in a fresh Claude Code session — the prompt to seed that session is captured in the 2026-05-21 working notes and lands at `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md` when produced. **Do not start implementation without that plan in hand** — vault_critic's contamination-filter is non-obvious and the manifest/launchd/daily-driver integration touches enough files that mid-flight design will produce drift.

### Verification gate for `shipped-and-verified`

Same shape Tier 1 + Tier 2 + Tier 1.5 used: **3 consecutive healthy nights** with all of:

1. `vault/health/critic-manifest-{date}.json` exists, `status: ok` or `status: partial` (not `error`), `articles_critiqued > 0`.
2. Sean reads the **median expansion file** (random sample, NOT cherry-picked — per memory [`feedback_synth_verify_against_median_not_best.md`](../../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_against_median_not_best.md)) and confirms it reads as thinking-partner work: specific named additions, specific authors, specific genre unlocks. Not "consider exploring X" — actual "add Y from Z because W."
3. Zero rate-cap-exhaustion events (`status: error` from rate-cap exhaustion on both CLIs simultaneously) across the 3 nights.

### Rollback

`./agents-sdk/schedules/install_schedules.sh --remove vault_critic` disables the launchd plist. Expansion files already written remain on disk and continue to be useful. The CLI dependencies (Codex, Anti-Gravity) require no uninstall — they're Sean's standalone tools, not pinned via `pyproject.toml`.

### Open questions deferred from the integration patterns doc

1. **Output fencing for Codex** — should the critique prompt require `<critique>…</critique>` wrapper markers to harden parsing against Codex preamble/postamble drift? Cheap to add; recommended for v1.
2. **Per-night article cap scaling** — fixed at 3 in v1. Revisit if synthesizer's nightly output starts averaging >10 articles after Tier 1.5 stabilizes.
3. **Expansion file lifecycle** — frozen snapshot vs regenerated when the parent concept is rewritten? v1 default: frozen snapshot.
4. **skill_optimizer relationship** — `vault_critic` is the cheap nightly tier; `skill_optimizer` (manual, $20-145/run, autoresearch convergence loop) is the deep tier. Footer in the expansion file recommending `skill_optimizer` for high-value critiques? Cheap to add; recommended.
5. **MBP dual-write fix** — must be resolved BEFORE marking vault_critic `shipped-and-verified`, otherwise every verification cycle has to fight PR-merge contamination. Three options enumerated in memory [`project_pr52_mbp_stale_checkout.md`](../../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/project_pr52_mbp_stale_checkout.md): disable MBP's parallel synth schedule; cron `git pull origin main` on MBP at 02:25; or accept dual-write and add manifest reconciliation in `lib/fleet_summary.py`. **Sean's call required.**

### Cross-references

- Canonical spec: [`agents-sdk/docs/multi-cli-integration-patterns.md`](../../../../../agents-sdk/docs/multi-cli-integration-patterns.md)
- Smoke-test artifacts (test fixtures): [`agents-sdk/docs/multi-cli-smoke-2026-05-21/`](../../../../../agents-sdk/docs/multi-cli-smoke-2026-05-21/)
- Pattern 1 implementation plan (to be produced): `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`
- Codex CLI config: `~/.codex/config.toml` (model: gpt-5.5, plugins: atlassian-rovo / google-calendar / gmail / figma / github / google-drive enabled)
- Anti-Gravity CLI config: `~/.gemini/settings.json` (model: auto-gemini-3, MCP servers: nanobanana / zapier / notebooklm-mcp / mcp-atlassian / chrome-devtools / pencil)
- Sean's complaint (the why): 2026-05-21 morning review of [`vault/knowledge/concepts/writing-voice-modes.md`](../../../../knowledge/concepts/writing-voice-modes.md), captured verbatim in the integration patterns doc §Why this doc exists.

---

## Status Tracker

> **Update this section after every meaningful change. Future Claude sessions: check here first.**

| Tier | Status | Started | Shipped | Notes |
|---|---|---|---|---|
| Tier 1 — Prompt + formatter retrofit | shipped-and-verified | 2026-05-13 | 2026-05-13 | Three nightly runs evaluated 2026-05-16: 1× ok (5/14, 114 concepts), 1× expected MBP-offline error (5/15, NY trip), 1× partial-with-validator-rejections (5/16, 36 concepts, 2 rejected — the new validator working). Zero "Evidence pending" strings in any file written 2026-05-14 or later. Cluster-diversity diagnostic confirmed retrieval-level bias remains (7/9 chunks from densest region) → Tier 2 trigger fired. |
| Tier 2 — Cluster-and-sample retrieval | **live-and-passing-gate (3/3 healthy nights; slug-dupes mostly FLAT, 3 new low-count pairs)** | 2026-05-16 | 2026-05-16 (initial); 2026-05-17 (routing-bug fix); **2026-05-18 / 5-19 / 5-20 = three consecutive healthy nightlies** | Tier 2 retrofit shipped 5/16 with `lib/retrieval_diversity.py` + 14 new tests + `hdbscan>=0.8.40,<0.9`. Routing bug fixed same-day 5/17 with two pinning tests. **Three consecutive healthy Tier-2 nights now logged post-fix:** 5/18 `clusters_sampled=38`, 5/19 `clusters_sampled=56`, **5/20 `clusters_sampled=37`** (all clear the ≥3 gate). 5/20 was a low-volume night (4 concepts / 1 connection / 14 files), but cluster sampling worked — quiet day on the vault input side, not a synthesizer regression. **However, real-output spot-check on 2026-05-20 (Sean's review of `automation-routines.md`, 5/19) exposed that the gate is measuring the wrong thing: median output is still shallow (CLI-snippet evidence, restatement-shape definitions, no `## Threads` substance) even when telemetry passes.** The Verification Log's prior spot-checks (5/18 `agentic-engineering-signal-in-product-development.md`, 5/19 `agentic-systems-across-personal-creative-and-professional-workflows.md`) were the *best* output of each night, not the median. Insight-depth is now the bottleneck, not retrieval diversity. Tier 3 stands down — see new Tier 1.5 row below. |
| **Tier 1.5 — Insight-depth gate + prompt v2** (NEW 2026-05-20) | **live, gate firing as designed (1/3 healthy nights — 2026-05-21 verified)** | 2026-05-20 | 2026-05-20 | **2026-05-21 first-night verdict (appended):** Mac Mini Tier-1.5 run wrote 1 concept + 1 connection and rejected 2 articles with stable reason codes (`rejected_reasons={thin-definition: 1, thin-threads: 1}`). Honest median spot-check of the 2 surviving articles (n=2, sample = corpus) confirms thinking-partner shape: `concepts/writing-voice-modes.md` and `connections/tonal-consistency-across-content-and-career-strategy.md` both meet the depth contract. One gate-undetected defect found — `tonal-consistency` has the same ~190-char quote duplicated across two threads (LLM cross-thread copy-paste), which the gate accepts because each thread independently passes the ≥60-char prose check. New reason-code candidate `duplicate-thread-quote` but n=1 is premature; watch 5/22 + 5/23. **Operational issue flagged separately in Verification Log:** PR #52 (merged 5/21 06:29) merged 88 pre-Tier-2 files from a stale-checkout MBP parallel synth into `vault/knowledge/`, polluting the corpus and producing FALSE-NEGATIVE random samples. Do NOT count PR #52 articles in Tier-1.5 verification. Re-trigger condition (branch c — STILL SHALLOW): if 5/22 + 5/23 random-samples (drawn ONLY from Mac Mini manifest output) still produce shallow shapes the gate accepted, ship the new reason code with a failing test exercising the exact shape. Verification gate to mark `shipped-and-verified`: 2 more consecutive healthy Tier-1.5 nights (5/22 + 5/23) producing non-zero `rejected_reasons` and median-quality output meeting the contract. <br><br>**Original ship notes (2026-05-20):** Born from Sean's 5/20 review surfacing the "I'm not getting a thinking partner" complaint. Tier 2 retrieval is healthy; the LLM is still producing surface output because the validator only checks wikilink count + the forbidden-placeholder string. **Three structural changes:** (1) New `evaluate_article_depth(body) -> (passed, reason)` semantic gate alongside `validate_article_body`. Concept gate: Definition ≥3 sentences AND ≥250 chars AND no restatement-tell phrases (`a collection of`, `designed to support`, `streamlines his workflow`, `ensures consistency`, etc.); Evidence ≥2 quotes each ≥60 chars; at least one non-code/CLI quote (prefix + symbol-density signals); Examples can't duplicate Evidence. Connection gate: Synthesis ≥3 sentences AND ≥200 chars naming a *tension* + *consequence*; each per-concept thread has ≥1 substantive (≥60-char) prose quote; ≥2 implications each ≥80 chars. (2) Prompt v2 — Definition demands 3-5 sentences naming the mechanism not the surface; Synthesis demands 3-5 sentences naming the cross-domain tension + consequence; explicit "REJECTED-SHAPE EXAMPLES" anti-pattern block (paraphrasing Sean's own complaint — restated-prompt definitions, CLI-quote evidence, "Three producers share an MBP dependency"-shape synthesis); explicit `OMIT the article entirely` instruction when chunks can't ground the depth. (3) Skip-thin-source path — when the diversified pool returns <2 chunks, skip the LLM call entirely; `result.skipped_thin_source` surfaces in manifest. New manifest fields: `rejected_reasons: dict[str,int]` (keyed by `thin-definition`/`restatement-definition`/`thin-evidence`/`code-only-evidence`/`duplicate-examples`/`thin-synthesis`/`thin-threads`/`thin-implications`/`wikilinks-or-placeholder`) and `skipped_thin_source: int` — operator-grade signal for *why* output volume changes night to night. **Test suite:** 12 new tests in `test_vault_synthesizer.py` (8 depth-gate cases + 1 manifest-persistence + 1 thin-source skip + 2 integration); full synthesizer suite 27 → 28 passed; synthesizer-neighborhood (synthesizer + retrieval-diversity + concept-edges + knowledge-lint + synth-manifest) **91 passed, 0 regressions**. Existing happy-path + Phase-D test fixtures updated to satisfy the new gate — the fixtures now look like the real shape we want production output to take, which doubles as documentation. **First production signal:** 2026-05-21 02:30 AM nightly synth run. Verification gate is twofold: (a) `rejected_reasons` populated with non-zero entries (validator actively gating, not silent-passing), and (b) **Sean reads at least 2 randomly sampled articles from 5/21's output and confirms they read like thinking-partner work, not "this is a research report about agentic workflows. This would benefit Sean."** Failure mode: if 5/21 produces near-zero articles because everything is rejected, the prompt is too strict — tune `_RESTATEMENT_PHRASES` / depth thresholds and re-test. If 5/21 still produces shallow articles, the gate logic missed a defect shape — add new reason code, write test, ship fix. Rollback: `git checkout agents-sdk/agents/vault_synthesizer.py agents-sdk/tests/test_vault_synthesizer.py` — pure-text + test changes, no new deps, no schema migrations. |
| Tier 3 — EDC canonicalization | **deferred — wrong defect; insight depth not slug-dedup (2026-05-20)** | — | — | Slug-duplication trend was the trigger condition (per §Tier 3 trigger above). Three consecutive Tier-2 nights produced 96 concepts (was 91 on 5/17) despite ~71 attempted writes — strong implicit reuse. Pre-existing dupe groups (`vibe-coding` 5, `daily-note` 3, etc.) are flat. Three new low-count pairs appeared (`agent-health` 2→3, `portfolio-projects` new pair, `agentic-engineering` new pair) — mild upward drift but not in the original problem clusters. The retrieval-level fix (Tier 2) is indirectly satisfying the canonicalization goal. Real defect surfaced by Sean's 5/20 review is *insight depth*, which EDC cosine-merge would not touch. Re-trigger condition: if Tier 1.5's depth gate still leaves shallow output AND slug-dedup starts trending up sharply (>3 new dupe groups in one week, or any pre-existing group growing). |
| Tier 4 — Three-pass agentic synthesis | pending (post-employment) | — | — | Do not ship under sprint pressure. Still the right architectural shape if Tier 1.5 underdelivers. |
| **Follow-on — `vault_critic` agent (Pattern 1)** (NEW 2026-05-21) | **spec written + smoke-tested; implementation plan pending via /writing-plans skill in fresh session** | 2026-05-21 | — | NOT a synthesizer tier — a separate downstream agent that critiques each newly-written concept article using Codex CLI (gpt-5.5) + Anti-Gravity CLI (Gemini 3.1 Pro) in parallel, at $0 incremental cost on Sean's existing personal subscriptions. Born from Sean's 5/21 review of `writing-voice-modes.md` ("I'm not seeing a thinking partner — I want the agent to tell me how to make this BETTER"). Smoke-tested live 2026-05-21: Codex returned in 21s with 3 named voice modes (Didion / McPhee / Maggie Nelson) with sentence patterns + genre unlocks; Anti-Gravity returned in 43s with 3 different named voice modes (Didion / Baldwin / Byung-Chul Han) — convergence on Didion is a strong "you need this mode" signal, non-overlapping recommendations were complementary. Specced in [`agents-sdk/docs/multi-cli-integration-patterns.md`](../../../../../agents-sdk/docs/multi-cli-integration-patterns.md); smoke artifacts persisted at [`agents-sdk/docs/multi-cli-smoke-2026-05-21/`](../../../../../agents-sdk/docs/multi-cli-smoke-2026-05-21/) as test fixtures. **Next step:** seed a fresh Claude Code session with the /writing-plans skill to produce `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md` (prompt template ready). **Blocker before `shipped-and-verified`:** MBP dual-write contamination (see [`project_pr52_mbp_stale_checkout.md`](../../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/project_pr52_mbp_stale_checkout.md)) must be resolved — Sean's call between three documented options (disable MBP parallel synth / cron-pull / manifest reconciliation). |

### Tier 1 shipped changes — exact diff summary

| File | Lines (post-edit) | Change |
|---|---|---|
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~127-145 | Added `_FORBIDDEN_PLACEHOLDERS = ("Evidence pending", "(to be filled)")` and extended `validate_article_body` to reject any body containing either. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~152-194 | Added optional `evidence: list[str] | None` param to `format_concept_article`; added a new `## Evidence` section that renders verbatim quotes as blockquotes. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~200-240 | Rewrote `format_connection_article` — added `evidence: dict[str, list[str]] | None` param. Per-concept threads now render verbatim quotes per linked concept. **Removed the hardcoded `"Evidence pending."` string** that caused the regression. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~315-345 | Added `_load_existing_concept_titles(knowledge_root)` helper — reads existing concept slugs from frontmatter for the canonicalization prompt block. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~347-468 | Rewrote `_build_synthesis_prompt`: quote-first JSON schema, canonicalization block with injected existing titles, cross-domain preference rule, longer chunk excerpts (200 → 800), forbidden-phrase list, per-concept `evidence` field in connection schema. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~539-543 | Added `existing_titles = _load_existing_concept_titles(knowledge_root)` one-time load at run start. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~564 | `_build_synthesis_prompt` call now passes `existing_titles`. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~590 | `format_concept_article` call now passes `evidence=list(c.get("evidence", []))`. |
| [agents-sdk/agents/vault_synthesizer.py](../../../../../agents-sdk/agents/vault_synthesizer.py) | ~616-630 | Defensive parse of LLM `evidence: dict[concept_title, quotes]` payload, then passes to `format_connection_article`. |

**Note for future sessions:** if you need to roll back Tier 1, the diff is contained entirely within `agents-sdk/agents/vault_synthesizer.py`. No new dependencies, no schema changes, no config changes. `git checkout agents-sdk/agents/vault_synthesizer.py` reverts cleanly.

### Verification log (append-only — write here after each nightly synth)

| Run date | Tier active | concepts_written | connections_written | cross-cluster rate | Evidence-pending count | Notes |
|---|---|---|---|---|---|---|
| 2026-05-13 02:30 | (baseline / pre-retrofit) | 203 | 111 | ~0% | 111 (every connection) | Baseline before Tier 1 ships. |
| 2026-05-14 02:30 | Tier 1 | 114 | 69 | TBD (qualitative ok — see notes) | 0 in 5/14-written files (75 stale pre-Tier-1 files from 5/12-5/13 still on disk; synthesizer is incremental, doesn't regen) | First post-Tier-1 night. status=ok, mbp_awake, qwen3-14b. Spot-check of `agent-health-and-knowledge-retrieval-interdependence.md` shows real per-concept verbatim quotes under `## Threads`. Tier 1 formatter fix confirmed live. |
| 2026-05-15 02:30 | Tier 1 | 0 | 0 | n/a | n/a | status=error, model=none, wol_status="". **EXPECTED** — Sean in NY 5/14-5/15, MBP off home LAN. Per memory `project_ny_trip_2026-05-14_mbp_offline.md` do NOT remediate. |
| 2026-05-16 02:30 | Tier 1 | 36 | 20 | TBD (qualitative ok — see notes) | 0 in 5/16-written files | status=partial (some files succeeded, some failed). `rejected_count=2` — most likely the new `_FORBIDDEN_PLACEHOLDERS` validator working as designed (articles missing verbatim quotes rejected before write). Sample `automation-failure-affects-daily-contextual-continuity.md` shows three concepts spanning daily-routine automation + agent-fleet + daily-note generation — actual cross-domain bridge. |
| 2026-05-17 02:30 | Tier 2 (wired but routing-bug suppressed) | 41 | 26 | n/a (Tier-2 path skipped) | 0 in 5/17-written files | status=partial, mbp_awake, qwen3-14b, duration 2715s (identical to 5/14's 2719s pre-Tier-2 — first telemetry tell that the new path wasn't being exercised). **`clusters_sampled: 0`** — Tier-2 verification gate FAILED. Root cause: `_default_retriever_factory._retrieve` shim accepted only `(query, top_k)` while `run_synthesis` calls it with `include_embeddings=True`; TypeError → silent positional retry → pool returned embedding-less → line-617 `isinstance(pool[0].get("embedding"), (list, tuple))` False → fall back to legacy `pool[:top_k]`. Underlying `vault_indexer.search(include_embeddings=True)` works correctly when called directly; HDBSCAN works correctly on synthetic 3-cluster fixture data. Bug was a single missing kwarg passthrough at the factory seam — exactly the kind of integration gap unit tests with mocked retrievers can miss. Fixed same-day (2026-05-17) with signature passthrough + two pinning tests. Real Tier-2 signal arrives 2026-05-18 02:30 AM. |
| 2026-05-18 02:30 | Tier 2 (fix live) | 32 | 11 | **PASSING** — `clusters_sampled: 38` (gate ≥ 3) | 0 in 5/18-written files | status=partial, mbp_awake, qwen3-14b, **duration 2804.9s — +85s vs 5/17's 2715s baseline, HDBSCAN overhead now visible in telemetry**. 15 files processed. `rejected_count: 9` (up from 5/16's 2 and 5/17's 3) — proportional rejection rate ~17% vs ~3-5% prior runs. Hypothesis: validator working as designed on a more diverse candidate set; LLM seeing cross-cluster chunks produces more articles it can't anchor with verbatim quotes. Worth tracking across 5/19 + 5/20 before concluding. Spot-check of `agentic-engineering-signal-in-product-development.md` (one of 5 new connection files written this run) shows real 3-cluster synthesis — `Autonomous Agent Fleets` × `Intent Engineering` × `AdOps Automation` with verbatim quotes from three distinct source files spanning Code-Brain infra × research/automation × career/Block-archive. This is the Tier-2 success shape. |
| 2026-05-19 02:30 | Tier 2 (fix live) | 35 | 16 | **PASSING** — `clusters_sampled: 56` (gate ≥ 3) | 0 in 5/19-written files | status=partial, mbp_awake, qwen3-14b, duration 3262.15s (+457s vs 5/18, +547s vs broken baseline; 23 files processed vs 5/18's 15 explains the bulk). 30 typed edges written. **Rejection-rate watchlist RESOLVED:** 2 of ~51 ≈ 4%, back to normal background variance vs 5/18's 17% spike. 5/18 was single-run noise, not a structural validator regression. Spot-check of `agentic-systems-across-personal-creative-and-professional-workflows.md` shows 3-cluster synthesis spanning `Agentic Engineering` × `Agent Health and Daily Routine Automation` × `Research Prompt: Autoresearch & Agentic Polymarket` — three distinct PARA folders with verbatim quotes per concept. Two consecutive healthy Tier-2 nights now logged. |
| **Slug-dupe trend (2026-05-19 snapshot)** | — | — | — | — | — | **Concept count: 91 → 96 (+5 over 2 days of Tier-2-live runs)** despite ~67 attempted writes (32 on 5/18 + 35 on 5/19) — strong implicit signal that Tier-1's existing-titles canonicalization block + Tier-2's diversified retrieval are together producing high reuse, not new minted slugs. **Pre-existing dupe groups are completely FLAT:** 5/17 had `vibe-coding-*` (5), `daily-note-*` (3), `track-c-*`/`crypto-pm-*`/`agent-health-*` (2 each). 5/19 has the same exact counts — zero growth in any pre-existing dupe group. **Two new dupe pairs appeared:** `vault-synthesizer-*` (2) and `vault-knowledge-*` (2), both meta-vault concepts about the synthesizer itself — these are about the work this plan describes, not redundant restatements of prior ideas. **Implication for Tier 3:** the EDC cosine-merge tier was specced to attack "continued slug-duplication trending up" (per plan §Tier 3 trigger). That trend is NOT happening. Tier 3 looks increasingly like deferred / not-needed work — the retrieval-level fix may be indirectly fixing the canonicalization problem. **Will revisit on 2026-05-21 morning with one more night of data + a full slug-dupe re-scan before committing to don't-draft.** |
| 2026-05-20 02:30 | Tier 2 (fix live) | 4 | 1 | **PASSING** — `clusters_sampled: 37` (gate ≥ 3) | 0 in 5/20-written files | status=partial, mbp_awake, qwen3-14b, duration 2816.63s. 14 files processed. Low-volume night — clustering worked but only enough cross-cluster material surfaced for a handful of articles. Third consecutive healthy Tier-2 night. **HOWEVER:** Sean's 5/20 morning review of `automation-routines.md` (written 5/19) surfaced the real defect — output is structurally shallow (CLI-snippet evidence, restatement-shape definition, no `## Threads` substance) even though telemetry is green. Prior Verification Log spot-checks (5/18, 5/19) were cherry-picks of the best output, not the median. Triggered the Tier 1.5 retrofit shipped same day. |
| **Slug-dupe re-scan (2026-05-20 snapshot)** | — | — | — | — | — | 96 concepts total. Pre-existing groups unchanged from 5/17 baseline: `vibe-coding-*` (5), `daily-note-*` (3), `track-c-*`/`crypto-pm-*`/`vault-synthesizer-*`/`vault-knowledge-*` (2 each). **Three new low-count pairs since 5/19:** `agent-health-*` 2 → 3 (+1), `portfolio-projects-*` new pair, `agentic-engineering-*` new pair. Mild upward drift but all in the densest existing region, not new clusters. Trend is *not* the slug-explosion shape Tier 3 was specced to attack. Combined with Tier 1.5's reframing of the real defect as insight-depth, Tier 3 is now formally deferred. |
| 2026-05-21 02:30 | Tier 1.5 (fix live, first night) | 1 | 1 | **PASSING** — `clusters_sampled: 36` (gate ≥ 3) | 0 in 5/21-written files | status=partial, mbp_awake, qwen3-14b, duration 2968.0s (+151s vs 5/20's 2816.6s — Tier-1.5 evaluator overhead visible in telemetry, ~5% on top of HDBSCAN baseline). 15 files processed; **102 changed files queued** per log — most produced no LLM-shaped output because the diversified pool either didn't ground a concept or the LLM declined per the new OMIT-when-thin instruction. **`rejected_reasons={thin-definition: 1, thin-threads: 1}` populated with stable reason codes** — gate is FIRING, not silent-passing. `skipped_thin_source: 0` — diversified pool always had ≥2 chunks; skip-path didn't fire this run. **Rejection rate:** 2 of 4 LLM-attempted articles (50%) — high but expected on a new strict gate; sample too small to call regression. **Surviving-article spot-check (HONEST MEDIAN, n=2):** `concepts/writing-voice-modes.md` reads as thinking-partner shape — Definition 3 sentences ~700 chars naming the mechanism (modular tonal calibration system, authorial-reference anchors, implicit constraints shaping rhythm/structure), Evidence 2 prose quotes 113+102 chars (one from the SKILL.md, one Sean-voice sample), Examples 2 prose lines distinct from Evidence. `connections/tonal-consistency-across-content-and-career-strategy.md` Synthesis solid — 3 sentences ~565 chars naming the tension ("maintaining authenticity across mediums while adapting tone to audience expectations") + consequence ("can influence perceived professionalism or personal brand"), 2 implications ≥80 chars each. **One gate-undetected defect:** `tonal-consistency`'s Substack-Drafter thread and Creative Studio Workflows thread share the IDENTICAL ~190-char quote (LLM duplicated cross-thread); gate accepts because each thread independently has a ≥60-char prose quote. New reason-code candidate `duplicate-thread-quote` but n=1 of 2 surviving articles is premature — watch 5/22 + 5/23 before shipping the fix. **Contamination event flagged:** PR #52 ("MBP overnight synth output (2026-05-21)") merged at 06:29:58 ET dropped 88 pre-Tier-2 / pre-Tier-1.5 files into `vault/knowledge/`. PR body: *"MBP's local run pre-dated the v3.37.0 retrofit code (clusters_sampled=0)"*. Mac Mini's manifest was correctly preserved via conflict resolution, but the 88 article files were merged in. **These 88 files DID NOT pass the Tier 1.5 gate.** Initial random-sample for this row picked two of them (`cost-capped-agentic-workflows-and-agent-health-monitoring.md`, `automation-routines-and-daily-workflows.md`) — both fail the contract (1-sentence Synthesis ~140-180 chars, log-fragment/heading-fragment "quotes" not prose, ≤1 implication). Diagnosed and discarded. **Operational issue surfaced:** the CLAUDE.md architecture says "MBP is inference backend only" — but PR #52 shows the MBP has its own synth schedule running stale code. Either disable MBP's local synth schedule, force `git pull` on MBP, or accept dual-write and add manifest reconciliation in `lib/fleet_summary.py`. Until resolved, do NOT count PR #52-style mass-merges in Tier-1.5 verification — only sample from Mac Mini's manifest-tracked output. |
| **Slug-dupe re-scan (2026-05-21 snapshot)** | — | — | — | — | — | 105 concepts total (96 → 105, +9 net: ~7 from PR #52's MBP pre-retrofit injection + 1 Mac Mini Tier-1.5 + 1 unexplained delta). Pre-existing dupe groups completely FLAT vs 5/20: `vibe-coding-*` 5, `daily-note-*` 3, `agent-health-*` 3, `vault-synthesizer-*` 2, `vault-knowledge-*` 2, `track-c-*` 2, `portfolio-projects-*` 2, `crypto-pm-*` 2, `agentic-engineering-*` 2 — zero growth in any pre-existing dupe group. **ONE NEW PAIR:** `infrastructure-status-*` 2 (`infrastructure-status.md` + `infrastructure-status-and-agent-failure.md`, both from PR #52's MBP pre-retrofit injection — densest cluster, meta-fleet shape). Trend remains benign and NOT the slug-explosion shape Tier 3 targets. Tier 3 status unchanged: deferred. |

**Tier 1 evaluation (2026-05-16):**

1. **Formatter fix shipped and working.** `format_connection_article` (line 195-242) no longer hardcodes "Evidence pending." — confirmed by reading source + spot-checking 5/14 and 5/16 connection files. All post-Tier-1 connection files render real per-concept verbatim quotes under `## Threads`.
2. **The literal "Evidence-pending count = 0" PASS signal was based on an incorrect assumption** that the nightly synthesizer regenerates existing concept/connection files. It doesn't — it's incremental (only writes new articles from changed files). 75 buggy connection files written 2026-05-13 13:35 (the last v1 run before Tier 1 shipped at ~13:35 commit 18457c3) remain on disk and account for all 226 "Evidence pending" matches. Zero files written 2026-05-14 onward contain the string.
3. **Validator is actively rejecting bad output.** `_FORBIDDEN_PLACEHOLDERS` check at line 145 + `rejected_count=2` on 5/14 and 5/16 indicates the defense-in-depth is doing its job — Tier 1 is preventing regression at the write boundary.
4. **Cluster-diversity diagnostic (Step 4, run 2026-05-16):** the LLM successfully *composed* a cross-cluster narrative (three named concepts from three different folders, named the hidden pattern, proposed a concrete connector slug `agent-health-automation-reliability-and-creative-workflows`). BUT the "Consulted" list shows the retrieval bias is structurally unchanged: **7 of 9 retrieved chunks are agent-health / agent-fleet / automation-reliability** (densest region of concept space). Only 1 creative chunk made it through (`creative-studio-workflows.md` sim=0.75; `ai-driven-creative-automation-for-job-hunting.md` sim=0.70). **Zero career/portfolio/interview chunks** despite the prompt explicitly asking for one. Tier 1's prompt-level cross-domain hint helps the LLM *write better synthesis prose given the candidates it's handed*, but it doesn't change *what candidates the retriever hands it*. Cluster bias is fundamentally a retrieval-level problem that **Tier 2 (TopClustRAG cluster-and-sample)** attacks structurally — exactly the trigger condition the plan specified.

**Recommended actions:**

- **Cleanup (one-time, before next verification cycle):** delete the 75 stale connection files written 2026-05-12 and 2026-05-13 so future `grep "Evidence pending"` signals are meaningful. List of affected files: `grep -rl "Evidence pending" vault/knowledge/connections/`. After deletion, the next synth run will regenerate any still-relevant connections from the embedding index (because their source `.md` files will re-cluster against fresh chunks). This is a small destructive operation, so requires Sean's explicit go-ahead.
- **Tier 2 status decision:** all three nights produced healthy Tier 1 output (1 expected MBP-offline error, 2 successful with validator-driven rejections doing their job). The stale-file false signal does not invalidate Tier 1. Sean's call on whether to ship Tier 2 next, or first run a few more nights of Tier 1 to gather cross-cluster-rate baseline data on post-Tier-1 connections only.

**2026-05-16 update — Tier 2 SHIPPED.** Sean greenlit Tier 2 in the same session. Implementation summary:

- New `agents-sdk/lib/retrieval_diversity.py` (148 lines): `cluster_and_sample(embeddings, ...) -> DiversifiedPool` (HDBSCAN min_cluster_size=3, euclidean, 2-per-cluster, ≤3 noise, max 15 total; clean fall-back for empty / degenerate / sub-min input) + `build_embedding_query(primary_text)` (frontmatter type+tags both inline and block-style, H1/H2 headings, first non-list paragraph; falls back to raw text when no structure detected).
- `vault_indexer.py::search()` gained `include_embeddings: bool = False` keyword-only param (backward compatible — extra field, not a removed one).
- `vault_synthesizer.py::run_synthesis` retrieval block replaced: `build_embedding_query` instead of `primary_text[:2000]`, retrieves POOL_SIZE=50 with `include_embeddings=True`, calls `cluster_and_sample`, accumulates `clusters_found` into new `SynthesisResult.clusters_sampled` field, strips embeddings before passing chunks to prompt (50 × 768-dim vectors would blow up context budget). `TypeError` guard for backward-compat with test-mock retrievers.
- `pyproject.toml`: `hdbscan>=0.8.40,<0.9` added (pulls scikit-learn/scipy/joblib/threadpoolctl, ~30MB on arm64).
- `agents-sdk/tests/test_retrieval_diversity.py`: 14 new tests, all pass. Synthesizer-neighborhood suite stays green at 76 passed. Full pytest suite 550 passed (3 pre-existing failures unrelated to Tier 2, confirmed via `git stash` round-trip).
- Cleanup of 75 stale files remains an open ask — Sean's "Green light" was unambiguously for Tier 2 (the immediately-preceding question), not the cleanup. Safe single command remains `grep -rl "Evidence pending" vault/knowledge/connections/ | xargs rm`; awaiting explicit go-ahead.

**2026-05-16 follow-up — stale-file cleanup EXECUTED.** Sean greenlit the cleanup in the same session. Pre-deletion verification: 75 target files, all dated 2026-05-12 (2) or 2026-05-13 (73), zero "Evidence pending" matches in `vault/knowledge/concepts/` so cleanup scope correctly limited to `vault/knowledge/connections/`. Ran `grep -rl "Evidence pending" vault/knowledge/connections/ | xargs rm` then `regenerate_index(vault/knowledge)` to refresh `index.md` and remove dead wikilinks. Post-deletion verification: `grep -r "Evidence pending" vault/knowledge/` returns **0 matches**; connection file count `163 → 88` (matches expected delta); index regenerated cleanly with 88 concepts + 88 connections. Future `grep "Evidence pending"` checks in this vault are now meaningful — any non-zero count surfaces a new Tier-1 validator regression rather than baseline noise.

**Tier 2 evaluation (2026-05-17):**

1. **First post-Tier-2 nightly run failed the verification gate.** `synth-manifest-2026-05-17.json` reports `clusters_sampled: 0` (gate is `>= 3`). Run otherwise looked healthy — `status: partial`, `wol_status: mbp_awake`, `model_used: qwen3-14b`, 41 concepts + 26 connections + 42 typed edges + 3 rejected articles (validator working). Duration **2715s, essentially identical to 5/14's pre-Tier-2 2719s** — the smoking-gun telemetry tell that the new clustering path was never exercised. If clustering were happening, wall-clock would have shifted (faster from smaller diversified pool, or slower from HDBSCAN overhead).
2. **Root cause: a factory-shim signature gap.** `_default_retriever_factory._retrieve` in `vault_synthesizer.py:841` was defined as `(query: str, top_k: int = 5)`. The Tier-2 call site at line 598-602 passes `include_embeddings=True` as a keyword arg → raises `TypeError`. The synthesizer's defensive fallback at line 603-609 catches the TypeError, silently re-invokes positional-only, and the pool returns without embeddings. The line-617 guard `isinstance(pool[0].get("embedding"), (list, tuple))` then evaluates False (because `.get("embedding")` is `None`), and the branch into legacy `similar = pool[:top_k]` fires for every file. `cluster_and_sample` is never called; `result.clusters_sampled` never increments above 0.
3. **Why unit tests didn't catch this.** The 14 Tier-2 tests in `test_retrieval_diversity.py` exercise `cluster_and_sample` directly with hand-built embedding fixtures. The synthesizer-level tests in `test_vault_synthesizer.py` pass a mocked retriever (`retriever=lambda q, top_k=5: [...]`) that happens to also accept only `(query, top_k)`. Neither test path exercises the production `_default_retriever_factory` against a real or even mocked `search()`. Pure integration-seam blind spot — both ends of the seam were tested, the seam itself wasn't.
4. **Fix shipped 2026-05-17.** One-line passthrough at the factory: `_retrieve` now accepts `*, include_embeddings: bool = False` and forwards to `search(query, db, top_k=top_k, include_embeddings=include_embeddings)`. Two regression tests added to `test_vault_synthesizer.py` — one pins the signature via `inspect`, one pins behavior via monkeypatched `search`. Synthesizer-neighborhood suite: 76 → 78 passed.
5. **What this means for Tier 2 verification.** The "Tier 2 stable for ≥3 consecutive nights" gate for Tier 3 trigger does NOT count 2026-05-17 — the new path didn't actually run. The clock starts on the 2026-05-18 02:30 AM nightly. Earliest plausible Tier-3 evaluation: morning of 2026-05-21 (three healthy post-fix nights: 5/18, 5/19, 5/20).
6. **Diagnostic query.py still works as expected.** Re-run of "Find 3 themes from THREE DIFFERENT clusters..." cited 3 concepts from 3 different folders (agent-fleet, career/portfolio, creative-studio) with similarities 0.85/0.80/0.75 — query.py uses a separate code path (LLM-driven candidate selection over `vault/knowledge/index.md`) that doesn't go through `_default_retriever_factory`, so its retrieval diversity isn't a useful Tier-2 signal either way. Use the synth-manifest `clusters_sampled` field as the verification gate, not query.py output.

**Slug-duplication snapshot (2026-05-17):** 91 concept files total. Prefix-2 dupes detected: `vibe-coding-*` (5), `daily-note-*` (3), `track-c-*` (2), `crypto-pm-*` (2), `agent-health-*` (2). Recording this here as the **pre-Tier-2-real-signal baseline** for Tier 3 trigger evaluation — if these counts hold or grow after 3 healthy Tier-2 nights, Tier 3 triggers.

---

## How to use this doc in future sessions

1. **Synthesizer healthy?** Run `cat vault/health/synth-manifest-$(date -v -1d +%Y-%m-%d).json | jq` and check `status: ok`, `concepts_written > 0`, `wol_status: mbp_awake`.
2. **Tier 1 effective?** `grep -rn "Evidence pending" vault/knowledge/ | wc -l` — should be 0 after the first post-Tier-1 nightly run.
3. **Cluster bias resolved?** Re-run the Tier-1 diagnostic: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/query.py "Find 3 themes from THREE DIFFERENT concept clusters..."` — look at the "Consulted" list. If ≥2 different vault top-level folders appear, Tier 1+2 are paying off.
4. **Tier 1.5 depth gate firing?** `cat vault/health/synth-manifest-$(date -v -1d +%Y-%m-%d).json | jq '.rejected_reasons, .skipped_thin_source'` — if `rejected_reasons` is empty AND `concepts_written > 0`, the gate may be silent-passing; investigate per Tier 1.5 row in Status Tracker.
5. **Generative-critique layer (`vault_critic`) shipped yet?** `ls vault/health/critic-manifest-$(date -v -1d +%Y-%m-%d).json 2>/dev/null && cat | jq` — if file exists, read it. If not, the agent isn't deployed yet; see §Follow-on layer for implementation status and the prompt to seed the planning session.
6. **Random-sample any output honestly.** When verifying any tier OR the vault_critic, filter the sample to Mac-Mini-manifest-tracked output only (per memory `feedback_synth_verify_filter_to_manifest.md`) and pick the median, never the cherry-picked best (per memory `feedback_synth_verify_against_median_not_best.md`).
7. **Ready for next tier?** Check the trigger condition in each tier section above. Update the Status Tracker before starting work.

## Companion docs

- [Build plan that spawned this retrofit (eval suite + Workstream B/C)](2026-05-10-eval-suite-build-plan.md)
- [Synthesizer source](../../../../../agents-sdk/agents/vault_synthesizer.py)
- [Q&A tool that surfaced the diagnosis](../../../../../agents-sdk/scripts/query.py)
- [Eval suite](../../../../../evals/vault-synthesizer/)
- [Intent engineering skill (template for this spec)](../../../../../.claude/skills/intent-engineering/SKILL.md)
- [Personal context v2.0 (the why behind cross-domain discovery)](../../../../Sean-Winslow-Full-Personal-Context-v2.0.md)
- [Life-systems operating model — Agent research fleet leverage point](../../../../05_atlas/operating-models/life-systems/operating-model.md)
- [Creative-studio operating model — Vault-as-SSoT extra-hour north star](../../../../05_atlas/operating-models/creative-studio/operating-model.md)
- **NEW 2026-05-21 — Follow-on layer (vault_critic / Pattern 1):**
  - [Multi-CLI integration patterns (canonical spec for Patterns 1-3)](../../../../../agents-sdk/docs/multi-cli-integration-patterns.md)
  - [Smoke test artifacts — verified prompt template + Codex/Anti-Gravity outputs as test fixtures](../../../../../agents-sdk/docs/multi-cli-smoke-2026-05-21/)
  - Implementation plan target (to be produced via /writing-plans): `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`
