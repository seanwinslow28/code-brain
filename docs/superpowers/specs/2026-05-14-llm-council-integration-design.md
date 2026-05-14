# LLM Council Integration — Design Spec

**Date:** 2026-05-14
**Status:** Approved (pending final user review)
**Owner:** Sean Winslow
**Inspired by:** [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council) — credit + attribution maintained throughout.

---

## 1. Goal

Bring multi-vendor, cross-ranking LLM "council" critique into Claude Code sessions for the four high-variance, high-stakes use cases where single-vendor synthesis falls short: voice-mode calibration, job-hunt artifact review, decision pre-mortems, and PRD/spec stress-testing.

Ship in three phases:
- **Phase A** — clone Karpathy's reference web app into `tools/llm-council/upstream/`. Zero modification. Reference implementation + visible Karpathy attribution + browser sidecar fallback.
- **Phase B** — write headless Python CLI (`tools/llm-council/council/`) that implements the same three-stage pipeline (fan-out → cross-rank → chairman) using OpenRouter, callable from inside Claude Code sessions via a new `llm-council` skill. **This is where daily-use value lives.**
- **Phase C** — once CLI has 5–10 real runs and API surface is stable, extract pipeline as a public MCP server in a separate repo (`seanwinslow28/llm-council-mcp`). Portfolio piece. Karpathy-credited in README.

First end-to-end use case to nail: **voice-mode calibration for Substack pre-launch.** Four models blind-draft in "Sean Mode" from the spec only → cross-rank → chairman synthesizes where the spec is load-bearing vs. ambiguous → Sean edits `writing-voice-modes` SKILL.md until convergence improves.

## 2. Non-Goals

- Replace single-model Claude review for everyday work. Council is a reserved tool, not a default.
- Replace Gemini Deep Research for web-grounded compound research. Council is peer-review, not research.
- Maintain Karpathy's web app as a product. We use it as-cloned; if upstream breaks, we fix our CLI, not the upstream clone.
- Phase C tool surface beyond three named tools (`council_consult`, `council_review`, `council_voice_calibrate`). Scope creep deferred until post-publish usage data.

## 3. Architecture

### 3.1 Repo layout

```
claude-code-superuser-pack/
├── tools/                          ← NEW directory at root
│   └── llm-council/
│       ├── README.md               ← wrapper README, credits Karpathy, points to upstream
│       ├── .env.example            ← documents OPENROUTER_API_KEY usage
│       ├── upstream/               ← Phase A — git clone of karpathy/llm-council, unmodified
│       │   └── (Karpathy's repo, gitignored: node_modules/, data/)
│       ├── council/                ← Phase B — our headless Python package
│       │   ├── __init__.py
│       │   ├── cli.py              ← `python -m council` entry point
│       │   ├── client.py           ← OpenRouter async client (httpx)
│       │   ├── pipeline.py         ← 3-stage fan-out → cross-rank → chairman
│       │   ├── profiles.py         ← premium / variance profile definitions
│       │   ├── budget.py           ← cost tracking + cap enforcement
│       │   └── prompts.py          ← system prompts (lifted from upstream w/ attribution)
│       ├── tests/                  ← pytest, mocked OpenRouter
│       └── pyproject.toml          ← uv project, pinned deps (httpx, pydantic, rich, python-dotenv)
├── .claude/skills/llm-council/     ← NEW skill
│   ├── SKILL.md
│   └── decision-table.md           ← when to use council vs single-model vs gemini-deep-research
└── .env                            ← existing — OPENROUTER_API_KEY already present
```

**Key choices and why:**
- **`upstream/` subfolder for Karpathy's clone** — keeps his code unmodified, preserves attribution via the obvious folder name, prevents our changes from leaking into a fork. `cd upstream && ./start.sh` whenever the browser app is useful. Gitignore `upstream/node_modules/` and `upstream/data/`.
- **`council/` as a Python package, not a script** — `python -m council` entry. Makes Phase C extraction clean: the MCP server just imports `council.pipeline` and exposes it.
- **Single `.env` at superuser-pack root** — CLI reads `OPENROUTER_API_KEY` via `python-dotenv` walking up from `tools/llm-council/`. No env duplication.
- **`uv` for dep management** — matches Karpathy's choice and `agents-sdk/` pyproject.toml pattern.

### 3.2 CLI pipeline

```
Input: prompt (str), profile (premium|variance), [optional: chairman_override]
  ↓
Stage 1 — FAN-OUT (parallel, asyncio.gather)
  Each model in profile.models receives the raw prompt independently.
  Output: List[ModelResponse(model_id, content, tokens_in, tokens_out, latency_ms)]
  ↓
Stage 2 — CROSS-RANK (parallel, asyncio.gather)
  Each model receives the OTHER N-1 responses with anonymized IDs ("Response A/B/C/D").
  Asked to rank by accuracy + insight, return JSON {ranking: [...], reasoning: "..."}.
  Identity-anonymization mapping is fresh per cross-rank call (no self-favoring).
  Output: List[CrossRank(judge_model, ranking, reasoning)]
  ↓
Stage 3 — CHAIRMAN (single call, profile.chairman or override)
  Receives: original prompt + all 4 responses (named) + all 4 cross-rankings.
  Asked to synthesize the final answer, citing which model said what where useful.
  Output: ChairmanResponse(content, model_id, tokens, latency_ms)
  ↓
Returns: CouncilSession (full transcript, JSON-serializable, written to data/sessions/<id>.json)
```

### 3.3 Profiles

```python
@dataclass
class Profile:
    name: str                  # "premium" | "variance"
    models: list[str]          # 4 OpenRouter model IDs
    chairman: str              # one of the models, or distinct
    max_cost_per_query: float  # USD, hard cap before call

PROFILES: dict[str, Profile] = {
    "premium": Profile(name="premium", models=[...TBD...], chairman="...", max_cost_per_query=...),
    "variance": Profile(name="variance", models=[...TBD...], chairman="...", max_cost_per_query=...),
}
```

**Actual model IDs and cost caps are deferred to an OpenRouter inventory pass at implementation time.** Karpathy's Nov 2025 lineup (GPT-5.1, Gemini 3 Pro, Claude Sonnet 4.5, Grok 4) is six months stale as of 2026-05-14. The implementation plan's first task: query OpenRouter for May 2026 frontier models, select premium 4 and variance 4 jointly with Sean, then set cost caps based on per-model pricing.

**Profile-routing intent:**
- **premium** — stakes/synthesis questions (job-hunt artifacts, decision pre-mortems, PRD reviews). Four best frontier models, judging flat-out.
- **variance** — divergence/calibration questions (voice modes, prompt-clarity tests). Four models with maximally different RLHF lineages (mix of premium + mid-tier) so divergence is the signal.

### 3.4 Skill wrapper

`.claude/skills/llm-council/SKILL.md` — trigger phrases: *"convene council"*, *"council critique"*, *"variance check"*, *"premium council"*, *"four-model review"*, *"calibrate voice modes"*, *"stress-test this spec"*.

Body covers:
1. **Decision table** (separate file: `decision-table.md`) — when council is the right tool vs `gemini-deep-research` vs single-model Claude. Mirrors `gemini-deep-research/decision-table.md` shape.
2. **Profile-routing rule** — variance for stylistic/divergence questions; premium for stakes/synthesis questions.
3. **Workflow templates** — one per primary use case, starting with voice-mode-calibration.
4. **Allowed-tools list** — `Bash` (to call CLI), `Read`, `Write`, `AskUserQuestion`. Omits `Edit` because the skill writes new output files rather than modifying existing ones.

## 4. Cost discipline

Modeled on the proven `gemini-deep-research` pattern.

| Gate | Premium profile | Variance profile | Source |
|---|---|---|---|
| Per-query hard cap | TBD (set at model-selection time) | TBD | `Profile.max_cost_per_query` |
| Daily circuit breaker | TBD combined across both profiles | — | `vault/health/council-spend-{YYYY-MM-DD}.json` |
| Monthly governor | TBD combined across both profiles | — | `vault/health/council-spend-{YYYY-MM}.json` |

Flow:
1. **Pre-flight estimate** — input tokens × N models × per-model price-per-1k (cached from `openrouter list-models`, refreshed weekly). If estimate > per-query cap, abort with reason. If estimate + day-to-date > daily cap, abort. Same for monthly.
2. **In-flight tracking** — actual per-model token usage logged; cumulative spend appended to today's JSON after stage completes (atomic write via tmp + rename).
3. **Sean override** — `--force` flag bypasses per-query cap (still records spend, still respects daily/monthly). Skill never uses `--force` without explicit user request.

**Cost cap numbers are placeholders in this spec.** Finalized during model selection in the implementation plan's first task. The mechanism is fixed; the numbers are TBD.

## 5. Error handling

- **Single model fails in Stage 1** (timeout, 5xx, content filter) → log the failure, continue with N-1 responses. Cross-rank uses surviving N-1. Chairman is told which model dropped. **Degraded run is a valid output** — Sean sees what he got and the missing piece is named.
- **Two+ models fail in Stage 1** → abort, write partial transcript with error summary, skill surfaces "council unavailable, fallback to single-model Claude review."
- **Cross-rank parse failure** (model returns non-JSON ranking) → one retry with `response_format=json_object` hint, then skip that judge's ranking; chairman still gets the other rankings.
- **Chairman fails** → abort, write partial transcript with stage-1 + stage-2 contents; skill returns "council ran but chairman synthesis failed; here are the raw stages."
- **OpenRouter API key missing** → fail-fast at CLI startup with clear instruction pointing to `.env`.

## 6. First use case — voice-mode calibration

```
1. Sean: "calibrate voice modes against this paragraph"
   (pastes a Sean Mode draft, ~150-300 words)

2. Skill writes input file: /tmp/llm-council/voice-mode-input-<ts>.md
   Content:
   ---
   You are critiquing a writing sample written in "Sean Mode" — a calibrated hybrid
   voice defined in writing-voice-modes SKILL.md.
   [paste relevant excerpt from SKILL.md defining Sean Mode]

   The author wants to know whether the spec is unambiguous enough that four different
   frontier models would read it the same way.

   YOUR TASK: Write a 150-word paragraph on [TOPIC: the same topic Sean wrote about]
   in Sean Mode, following the spec exactly. Do not reference Sean's draft — write
   blind from the spec only.
   ---

3. Skill invokes:
   cd tools/llm-council && uv run python -m council \
     --profile variance --prompt-file ... --tag voice-mode-calibration

4. Council runs. Stage 1 = 4 models each draft 150 words in Sean Mode (blind).
   Stage 2 = 4 models cross-rank "which draft best embodies Sean Mode per the spec."
   Stage 3 = chairman synthesizes: "where did the four interpretations converge,
   where did they diverge, what does that tell us about which parts of the spec
   are load-bearing vs ambiguous."

5. Output written to: vault/20_projects/prj-job-hunt-2026/substack-pre-launch/
     voice-mode-calibration-runs/<YYYY-MM-DD>-<topic-slug>.md
   (with full transcript + chairman synthesis + cost summary)

6. Sean reads the chairman synthesis + the four blind drafts side-by-side with his
   own draft. Diff = signal on where writing-voice-modes spec needs sharpening.
   Apply edits to writing-voice-modes SKILL.md. Re-run calibration weekly until
   convergence is acceptable.
```

The output location is intentional: lives inside the Substack pre-launch sub-project, becomes a measurable record of voice spec calibration over time, and the diff trail is portfolio-worthy if Sean writes about the methodology.

## 7. Testing

**Unit tests (`tools/llm-council/tests/`):**
- `test_budget.py` — cost estimator math, daily/monthly file I/O (atomic writes), pre-flight cap rejection, force-flag bypass
- `test_profiles.py` — profile loading, chairman validation, model-ID existence (mock OpenRouter list-models)
- `test_pipeline.py` — fan-out fan-in correctness with mocked httpx; identity-anonymization mapping is fresh per cross-rank; degraded-mode (N-1 surviving responses); chairman receives correct named transcript
- `test_prompts.py` — system prompt templates render correctly for all three stages

**Integration test (one cheap model only, gated by env flag):**
- `INTEGRATION=1 pytest tests/test_e2e.py` — tiny end-to-end against cheapest variance-profile model 4-way (estimated <$0.05/run) to catch live API contract drift. Skipped in CI; manual run when changing OpenRouter client.

**Eval pattern (deferred until 3+ real runs):**
- After three voice-mode-calibration runs land in `vault/.../voice-mode-calibration-runs/`, write a small eval script that checks output schema (4 drafts present, cross-ranks present, chairman synthesis present, cost summary present, no hallucinated cost). No quality-of-output eval — that's Sean reading the markdown.

## 8. Phase C boundary (deferred)

When CLI has 5–10 real runs and the API surface is stable, extract Phase C to a **separate public GitHub repo**: `seanwinslow28/llm-council-mcp`.

Boundary rules:
- The MCP server **imports** `council.pipeline`, `council.profiles`, `council.client` — does not duplicate them
- Initially achieved via `pip install -e .` from the in-tree path; once the repo is public, `pip install llm-council-mcp` from a published package
- The new repo's README leads with "Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council)" and links to his project
- Tools exposed: `council_consult(prompt, profile)`, `council_review(content, profile)`, `council_voice_calibrate(spec, sample, topic)` — three named tools (indexes better for portfolio + Claude's tool-selection)
- Public repo also ships an example workflow doc and screenshots — portfolio value lives in the README, not the code

**What does NOT move in Phase C:**
- Skill stays in superuser-pack (personal use)
- Karpathy's `upstream/` clone stays in `tools/llm-council/` (personal reference)
- Cost tracking files (`vault/health/`) stay personal

Phase C is "publish the engine, keep your personal config private." Standard portfolio-piece shape.

## 9. Open items deferred to implementation plan

These are deliberately deferred from the design spec because they need fresh data at implementation time, not speculation now:

1. **Model selection** — query OpenRouter for May 2026 frontier models. Pick 4 for premium, 4 for variance, 1 chairman per profile. Sean approves selection.
2. **Cost cap numbers** — derived from selected models' per-token pricing. Per-query, daily, monthly numbers set jointly.
3. **OpenRouter pricing snapshot mechanism** — manual (run `openrouter list-models` weekly, commit to repo) or automated (script polls + alerts on price change). Decide during implementation.
4. **Skill registration in CHANGELOG/CLAUDE.md/README.md** — required per CLAUDE.md non-negotiable rule #8 "Mandatory doc updates."

## 10. Decisions log (during brainstorming)

| # | Decision | Rationale |
|---|---|---|
| 1 | A + B + C in that order | Phase A free (clone). Phase B = daily-use value. Phase C = portfolio piece. |
| 2 | Two profiles (premium, variance), toggleable | Different jobs need different panels; variance is the actual point of a council. |
| 3 | Models TBD pending OpenRouter inventory at impl time | Karpathy's lineup 6 months stale as of 2026-05-14. |
| 4 | Voice-mode calibration as first use case | Active blocker (Substack pre-launch), variance-profile job, output is directly auditable. |
| 5 | Approach 2 (compressed: A clone + B CLI parallel, C deferred) | Fastest to daily use. Karpathy repo still present as reference + credit anchor. |
| 6 | Cost cap numbers deferred to model-selection time | Caps depend on per-model pricing. Mechanism is fixed; numbers are TBD. |
| 7 | Phase C lives in separate public repo, not in-tree | Portfolio narrative + clean Karpathy credit + reusable by others. |
