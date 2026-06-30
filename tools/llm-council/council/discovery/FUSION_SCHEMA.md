# OpenRouter Fusion — captured request/response schema

**Captured:** 2026-06-20 via one live call on Sean's OpenRouter key (Task 4 spike).
**Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`
**Purpose:** ground-truth the exact JSON envelope so `fusion.py` (Task 5) parses the real shape.

This file is the source of truth for `_build_body` (request) and `_to_result` (response) in
[`fusion.py`](fusion.py). It records what *actually worked*, not what the docs imply.

---

## 1. Working request envelope (verbatim, accepted with HTTP 200)

The plan's request shape is **correct as written** — a **top-level `fusion` object**, the Fusion
**tool** entry, and `tool_choice:"required"`. No tool-embedded args were needed.

```json
{
  "model": "google/gemini-2.5-pro",
  "messages": [
    {"role": "system", "content": "<judge instruction>"},
    {"role": "user", "content": "<topic + evidence block>"}
  ],
  "tools": [{"type": "openrouter:fusion"}],
  "tool_choice": "required",
  "fusion": {
    "analysis_models": ["x-ai/grok-4.3", "deepseek/deepseek-v4-pro"],
    "max_tool_calls": 2
  }
}
```

- `model` — the **judge** / outer model (`TierConfig.judge`). Produces the final synthesized text.
- `fusion.analysis_models` — the **panel** (`TierConfig.panel`). These reason over the prompt and
  may call the Fusion web tools up to `max_tool_calls` each.
- `fusion.max_tool_calls` — per-run server-tool (web search/fetch) budget.
- Header: `Authorization: Bearer <OPENROUTER_API_KEY>`. (The council resolves the key via
  `python-dotenv`, walking up from `tools/llm-council/` to the repo-root `.env`.)

→ **Task 5 `_build_body` matches this shape verbatim. No correction needed.**

---

## 2. ⚠️ Model-ID corrections (the plan's "verified" list was partly wrong)

Validated all panel/judge IDs against the live `GET /api/v1/models` (340 models). Two of the
plan's IDs are **rejected by the live API** (`400: "<id> is not a valid model ID"`):

| Plan ID (spec §7 / `tiers.py`)   | Live status | Valid replacement(s) on OpenRouter 2026-06-20 |
|----------------------------------|-------------|-----------------------------------------------|
| `anthropic/claude-opus-4.7`      | ✅ valid    | —                                             |
| `openai/gpt-5.5`                 | ✅ valid    | —                                             |
| `x-ai/grok-4.3`                  | ✅ valid    | —                                             |
| `deepseek/deepseek-v4-pro`       | ✅ valid    | —                                             |
| `perplexity/sonar`               | ✅ valid    | —                                             |
| `perplexity/sonar-reasoning-pro` | ✅ valid    | —                                             |
| `perplexity/sonar-deep-research` | ✅ valid    | —                                             |
| `google/gemini-pro-latest`       | ❌ **400**  | **`~google/gemini-pro-latest`** ← now wired in (floating "latest" alias → resolves to `google/gemini-3.1-pro-preview`) |
| `mistralai/mistral-medium-3.5`   | ❌ **400**  | **`mistralai/mistral-medium-3-5`** ← now wired in (resolves to `mistralai/mistral-medium-3.5-20260430`) |

**RESOLVED 2026-06-20 (Sean-directed):** `tiers.py` now ships the validated IDs — `~google/gemini-pro-latest`
(the tilde is OpenRouter's floating-"latest" alias) in the `quick` judge+panel and the `standard`/`deep`
panel, and `mistralai/mistral-medium-3-5` in the `deep` panel. Both were confirmed accepted by the live
chat endpoint (HTTP 200, `max_tokens=1` probe). The Task 2 assertions were updated to match. The bare
`google/gemini-pro-latest` and dotted `mistralai/mistral-medium-3.5` from the design spec remain invalid —
do not reintroduce them.

---

## 3. Response envelope (verbatim keys, HTTP 200)

The response is a **standard chat-completions envelope**. There is **no top-level `fusion` key**
and the individual panel-model outputs are **not** separately exposed — Fusion internalizes the
panel and returns only the judge's synthesis in `message.content`.

```
top-level keys : ["id","object","created","model","provider","system_fingerprint",
                  "service_tier","choices","usage"]
choices[0]     : ["index","logprobs","finish_reason","native_finish_reason","message"]
choices[0].message : ["role","content","refusal","reasoning","reasoning_details"]
```

### Path map (what `_to_result` reads)

| Datum                         | JSON path                                              |
|-------------------------------|-------------------------------------------------------|
| Judge synthesis (the output)  | `choices[0].message.content`  (string)                |
| Finish reason                 | `choices[0].finish_reason`  (`"stop"`)                |
| Prompt tokens                 | `usage.prompt_tokens`                                 |
| Completion tokens             | `usage.completion_tokens`                             |
| **Authoritative call cost**   | `usage.cost`  (USD, float — e.g. `0.497096375`)       |
| **Web-tool calls executed**   | `usage.server_tool_use_details.tool_calls_executed`  |
| Web-tool calls requested      | `usage.server_tool_use_details.tool_calls_requested` |
| Reasoning tokens (judge)      | `usage.completion_tokens_details.reasoning_tokens`   |

> The panel clusters/contradictions/blind-spots are **not** machine-separated in the response.
> Task 5's strategy is correct: instruct the judge (via the system prompt) to emit a single JSON
> object into `message.content`, then `json.loads` it (fence-stripped). The spike confirms
> `message.content` is free text fully under our prompt's control.

### `usage` block (verbatim from the captured 200 response)

```json
{
  "prompt_tokens": 9694,
  "completion_tokens": 1293,
  "total_tokens": 10987,
  "cost": 0.497096375,
  "prompt_tokens_details": {"cached_tokens": 1341, "cache_write_tokens": 0},
  "completion_tokens_details": {"reasoning_tokens": 900},
  "server_tool_use_details": {"tool_calls_requested": 4, "tool_calls_executed": 4}
}
```

---

## 4. Notes for Task 5 (`fusion.py`) and Task 13 (`pipeline.py`)

1. **`web_calls` field path correction.** The plan's `_to_result` reads `usage.get("web_search_calls", 0)`,
   which does **not** exist in the live response. The real count is
   `usage["server_tool_use_details"]["tool_calls_executed"]`. Task 5 should read the real path with a
   safe fallback to 0. (Harmless either way for tests; the mocked `usage` lacks the key.)
2. **Authoritative cost available.** `usage.cost` is the exact USD cost OpenRouter charged. The plan
   estimates cost from token constants in `pipeline._estimate_cost`; `usage.cost` is strictly more
   accurate and is **recommended** to be captured into `FusionResult` and preferred in the pipeline
   (falling back to the token estimate when absent). Kept as-is for Phase 1 to preserve the tested
   contract; flagged to Sean.
3. **Real cost calibration.** This single 2-panel, `max_tool_calls=2` call with a Gemini 2.5 Pro judge
   cost **$0.497** (4 web tool calls executed). A `standard` tier (post-E2: 3-panel,
   `max_tool_calls=5`, with a non-panelist Opus judge) will cost meaningfully more — the per-run
   cap ($1.50) and daily/monthly caps
   ($10/$50) are the real guardrails. The web-tool count (`panel_size × max_tool_calls`) dominates.

## 5. Cost of this spike

The first attempt (with the invalid `google/gemini-pro-latest`) was rejected at 400 → **$0.00**.
The successful capture call cost **$0.497** (charged to Sean's OpenRouter key, pre-authorized for
this spike). Total Task-4 spend: **~$0.497**.
