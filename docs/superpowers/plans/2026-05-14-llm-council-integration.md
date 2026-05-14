# LLM Council Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working in-session multi-vendor LLM council critique tool — Karpathy's repo cloned as reference at `tools/llm-council/upstream/`, plus a headless Python CLI (`tools/llm-council/council/`) implementing the same fan-out → cross-rank → chairman pipeline against OpenRouter, invocable from a new `.claude/skills/llm-council/` skill — with cost discipline modeled on `gemini-deep-research`. First end-to-end use case: voice-mode calibration for Substack pre-launch.

**Architecture:** Three-stage async pipeline (Stage 1 parallel fan-out → Stage 2 parallel cross-rank with anonymized model IDs → Stage 3 single chairman synthesis), driven by two configurable Profiles (premium and variance) reading API keys from the existing root `.env`. Cost tracked in `vault/health/council-spend-*.json` with per-query / daily / monthly gates. Karpathy's clone lives unmodified in a subfolder for both visible attribution and reference-implementation fallback.

**Tech Stack:** Python 3.10+, `uv` for project management, `httpx` async client, `pydantic` for typed responses, `rich` for terminal output, `python-dotenv` for env loading, `pytest` + `pytest-asyncio` for tests. OpenRouter as the model gateway.

**Spec reference:** [`docs/superpowers/specs/2026-05-14-llm-council-integration-design.md`](../specs/2026-05-14-llm-council-integration-design.md)

---

## File Structure

**Created:**
- `tools/llm-council/README.md` — wrapper README, credits Karpathy
- `tools/llm-council/.env.example` — documents `OPENROUTER_API_KEY` usage
- `tools/llm-council/.gitignore` — ignores `upstream/node_modules`, `upstream/data`, `.venv`, `__pycache__`, `data/sessions/*.json`
- `tools/llm-council/pyproject.toml` — uv project metadata + pinned deps
- `tools/llm-council/openrouter-models-snapshot-2026-05-14.json` — pricing snapshot (Task 1 output)
- `tools/llm-council/model-selection-2026-05-14.md` — decision doc for picked models + caps (Task 1 output)
- `tools/llm-council/upstream/` — Karpathy's repo cloned, unmodified (Task 2 output)
- `tools/llm-council/council/__init__.py`
- `tools/llm-council/council/profiles.py` — `Profile` dataclass + `PROFILES` dict
- `tools/llm-council/council/prompts.py` — system prompts for the 3 stages
- `tools/llm-council/council/client.py` — async OpenRouter client wrapping httpx
- `tools/llm-council/council/budget.py` — cost tracking + cap enforcement
- `tools/llm-council/council/pipeline.py` — 3-stage orchestrator
- `tools/llm-council/council/cli.py` — `python -m council` entry point
- `tools/llm-council/council/__main__.py` — enables `python -m council`
- `tools/llm-council/tests/__init__.py`
- `tools/llm-council/tests/conftest.py` — shared fixtures (mock httpx, tmp `vault/health/` dir)
- `tools/llm-council/tests/test_profiles.py`
- `tools/llm-council/tests/test_prompts.py`
- `tools/llm-council/tests/test_client.py`
- `tools/llm-council/tests/test_budget.py`
- `tools/llm-council/tests/test_pipeline.py`
- `tools/llm-council/tests/test_cli.py`
- `tools/llm-council/tests/test_e2e.py` — integration test gated by `INTEGRATION=1`
- `.claude/skills/llm-council/SKILL.md` — skill entry point with trigger phrases + workflow templates
- `.claude/skills/llm-council/decision-table.md` — council vs single-model vs gemini-deep-research routing

**Modified:**
- `.gitignore` (root) — add `vault/health/council-spend-*.json`
- `CHANGELOG.md` — new version entry
- `CLAUDE.md` — bump skill count, add llm-council to skills section, add tools/ directory to architecture comment
- `README.md` — bump skill count

---

## Task 1: Model selection + cost caps (interactive with Sean)

This task is NOT TDD-style — it's an interactive research + decision task whose output (model IDs and cost caps) is consumed by every later task. Producing a decision doc and a pricing snapshot in the repo locks the choices and gives downstream tasks concrete values to reference.

**Files:**
- Create: `tools/llm-council/openrouter-models-snapshot-2026-05-14.json`
- Create: `tools/llm-council/model-selection-2026-05-14.md`

- [ ] **Step 1: Fetch OpenRouter model catalog**

```bash
mkdir -p tools/llm-council
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $(grep ^OPENROUTER_API_KEY .env | cut -d= -f2)" \
  | jq '.' > tools/llm-council/openrouter-models-snapshot-2026-05-14.json
```

Expected: a JSON file with a `data` array of ~300+ model entries, each with `id`, `name`, `pricing.prompt`, `pricing.completion`, `context_length`, `created` timestamp.

- [ ] **Step 2: Filter to current frontier candidates**

```bash
jq '[.data[]
  | select(.context_length >= 100000)
  | select(.id | test("preview|beta") | not)
  | {id, name, prompt_price: .pricing.prompt, completion_price: .pricing.completion, context: .context_length}
  | select((.prompt_price | tonumber) <= 0.000015)
  ] | sort_by(.prompt_price | tonumber)
' tools/llm-council/openrouter-models-snapshot-2026-05-14.json | head -100
```

Read the output. Identify the May-2026-current frontier models from OpenAI, Anthropic, Google, xAI, DeepSeek, Mistral, Meta. Note their model IDs, per-1k input cost, per-1k output cost, and context windows.

- [ ] **Step 3: Present candidate panels to Sean**

Use `AskUserQuestion` to present two proposed panels:

**Premium panel (4 models, frontier-only):**
- 4 model IDs spanning OpenAI / Anthropic / Google / xAI
- One designated chairman (typically the strongest synthesizer)

**Variance panel (4 models, maximally different RLHF lineages):**
- 4 model IDs mixing premium + mid-tier from genuinely different orgs (e.g., one each from Anthropic, OpenAI, DeepSeek, Meta)
- One designated chairman (typically Claude or a strong synthesizer regardless of cost)

Show each candidate's per-1k input/output cost. Wait for Sean's approval or substitution requests. Iterate until Sean confirms both panels.

- [ ] **Step 4: Estimate per-query cost for each profile**

Assume a typical voice-mode-calibration query: 2,000 input tokens × 4 models in Stage 1, then ~2,500 input tokens × 4 models in Stage 2 (each judge sees 3 other responses), then ~8,000 input tokens × 1 chairman in Stage 3. Assume 1,500 output tokens per Stage-1 response, 500 per Stage-2 ranking, 2,000 for Stage-3 chairman.

Compute: `stage1_in_cost + stage1_out_cost + stage2_in_cost + stage2_out_cost + stage3_in_cost + stage3_out_cost` for both panels using their per-1k prices. Round up to a clean ceiling and double for safety margin.

- [ ] **Step 5: Set cost caps with Sean**

Use `AskUserQuestion` to propose:
- Per-query hard cap for premium: estimated cost × 2 (e.g., `$X.XX`)
- Per-query hard cap for variance: estimated cost × 2
- Daily circuit breaker: `5 × max(premium_cap, variance_cap)` rounded to a clean number
- Monthly governor: `30 × max(premium_cap, variance_cap)` rounded to a clean number

Wait for Sean's approval or adjustment. Capture final numbers.

- [ ] **Step 6: Write the decision doc**

Create `tools/llm-council/model-selection-2026-05-14.md`:

```markdown
# LLM Council Model Selection — 2026-05-14

**Pricing snapshot:** `openrouter-models-snapshot-2026-05-14.json` (captured 2026-05-14)

## Premium profile

| Role | Model ID | Per-1k input | Per-1k output | Context |
|---|---|---|---|---|
| Council 1 | `<id>` | $<x> | $<x> | <ctx> |
| Council 2 | `<id>` | $<x> | $<x> | <ctx> |
| Council 3 | `<id>` | $<x> | $<x> | <ctx> |
| Council 4 | `<id>` | $<x> | $<x> | <ctx> |
| **Chairman** | `<id>` | $<x> | $<x> | <ctx> |

**Estimated per-query cost:** $<estimate>
**Per-query hard cap:** $<cap>

## Variance profile

| Role | Model ID | Per-1k input | Per-1k output | Context |
|---|---|---|---|---|
| Council 1 | `<id>` | $<x> | $<x> | <ctx> |
| Council 2 | `<id>` | $<x> | $<x> | <ctx> |
| Council 3 | `<id>` | $<x> | $<x> | <ctx> |
| Council 4 | `<id>` | $<x> | $<x> | <ctx> |
| **Chairman** | `<id>` | $<x> | $<x> | <ctx> |

**Estimated per-query cost:** $<estimate>
**Per-query hard cap:** $<cap>

## Combined gates

- **Daily circuit breaker:** $<daily-cap> across both profiles
- **Monthly governor:** $<monthly-cap> across both profiles
- **Spend tracking files:** `vault/health/council-spend-{YYYY-MM-DD}.json`, `vault/health/council-spend-{YYYY-MM}.json`

## Refresh cadence

Re-run `curl https://openrouter.ai/api/v1/models` weekly. If any selected model's `pricing.prompt` or `pricing.completion` changes by >20%, alert Sean and adjust caps.
```

Fill in every `<...>` placeholder with real values from Steps 3–5.

- [ ] **Step 7: Commit**

```bash
git add tools/llm-council/openrouter-models-snapshot-2026-05-14.json \
        tools/llm-council/model-selection-2026-05-14.md
git commit -m "feat(llm-council): model selection + cost caps for premium/variance profiles"
```

---

## Task 2: Clone Karpathy's repo as `upstream/`

**Files:**
- Create: `tools/llm-council/upstream/` (entire subdirectory, unmodified)
- Modify: `tools/llm-council/.gitignore` (will be created in this task)

- [ ] **Step 1: Clone the repo**

```bash
cd tools/llm-council
git clone https://github.com/karpathy/llm-council.git upstream
cd upstream && rm -rf .git && cd ..
```

The `rm -rf .git` is intentional — we want `upstream/` to be a static reference, not a nested git repo. Karpathy's commit history is available on GitHub; we don't need it locally.

- [ ] **Step 2: Create `.gitignore` for the tools directory**

Create `tools/llm-council/.gitignore`:

```gitignore
# Karpathy's upstream — keep source, ignore build artifacts
upstream/node_modules/
upstream/data/
upstream/frontend/dist/
upstream/__pycache__/
upstream/.venv/

# Our package build artifacts
.venv/
__pycache__/
*.egg-info/
.pytest_cache/

# Session output (real council runs)
data/sessions/*.json

# Local env override
.env
.env.local
```

- [ ] **Step 3: Verify upstream files present**

```bash
ls tools/llm-council/upstream/
```

Expected: `README.md`, `backend/`, `frontend/`, `pyproject.toml`, `start.sh`, `header.jpg`, and others.

- [ ] **Step 4: Commit**

```bash
git add tools/llm-council/upstream tools/llm-council/.gitignore
git commit -m "feat(llm-council): clone karpathy/llm-council as upstream/ reference"
```

---

## Task 3: Python project scaffolding

**Files:**
- Create: `tools/llm-council/pyproject.toml`
- Create: `tools/llm-council/council/__init__.py`
- Create: `tools/llm-council/council/__main__.py`
- Create: `tools/llm-council/tests/__init__.py`
- Create: `tools/llm-council/.env.example`
- Create: `tools/llm-council/README.md`

- [ ] **Step 1: Write `pyproject.toml`**

Create `tools/llm-council/pyproject.toml`:

```toml
[project]
name = "council"
version = "0.1.0"
description = "Multi-vendor LLM council for in-session critique. Inspired by Andrej Karpathy's llm-council."
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.6",
    "rich>=13.7",
    "python-dotenv>=1.0",
    "click>=8.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-httpx>=0.30",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["council"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 2: Create package init files**

Create `tools/llm-council/council/__init__.py`:

```python
"""LLM Council — multi-vendor critique pipeline.

Inspired by Andrej Karpathy's llm-council (https://github.com/karpathy/llm-council).
"""

__version__ = "0.1.0"
```

Create `tools/llm-council/council/__main__.py`:

```python
"""Allow `python -m council` to invoke the CLI."""

from council.cli import main

if __name__ == "__main__":
    main()
```

Create `tools/llm-council/tests/__init__.py`:

```python
```

(Empty file — just marks tests/ as a package.)

- [ ] **Step 3: Write `.env.example`**

Create `tools/llm-council/.env.example`:

```bash
# LLM Council reads OPENROUTER_API_KEY from the superuser-pack root .env.
# This file documents the expected variable for anyone setting up a fresh checkout.
#
# Get a key at https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-...

# Optional: override the spend tracking directory (default: vault/health/)
# COUNCIL_SPEND_DIR=/path/to/spend-tracking
```

- [ ] **Step 4: Write the wrapper README**

Create `tools/llm-council/README.md`:

```markdown
# LLM Council

Multi-vendor LLM "council" critique for in-session use from Claude Code.

**Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council).** Karpathy's reference web app lives unmodified at [`upstream/`](upstream/) as both a working browser-based council and visible attribution. Our headless Python CLI in [`council/`](council/) implements the same three-stage pipeline (fan-out → cross-rank → chairman) for invocation from inside Claude Code sessions via the [`llm-council` skill](../../.claude/skills/llm-council/).

## Quick start

```bash
# From the superuser-pack root (where .env lives):
cd tools/llm-council
uv sync
uv run python -m council --profile variance \
    --prompt-file /tmp/your-prompt.md \
    --output /tmp/council-output.md \
    --tag your-tag
```

Output is a markdown file with: original prompt, four named responses, cross-rank table, chairman synthesis, cost summary.

## Profiles

Two profiles defined in [`council/profiles.py`](council/profiles.py):

- **premium** — four frontier models, judging flat-out. Use for high-stakes synthesis (job-hunt artifacts, decision pre-mortems).
- **variance** — four models with maximally different RLHF lineages. Use when divergence is the signal (voice-mode calibration, prompt-clarity tests).

Final model IDs and cost caps are documented in [`model-selection-2026-05-14.md`](model-selection-2026-05-14.md).

## Karpathy's browser app

Want to use the original web UI?

```bash
cd upstream
uv sync && cd frontend && npm install && cd ..
# Symlink to root .env (one-time):
ln -sf ../../.env .env
./start.sh
```

Then open http://localhost:5173.

## License + credit

Karpathy's code in `upstream/` is MIT-licensed (see `upstream/LICENSE`). Our `council/` package is also MIT, with full attribution in source and README. We do not maintain `upstream/` — if it breaks against an OpenRouter API change, we fix our CLI and treat the upstream as a frozen reference.
```

- [ ] **Step 5: Set up uv environment**

```bash
cd tools/llm-council
uv sync --extra dev
```

Expected: `uv` resolves and installs dependencies into `.venv/`, no errors.

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/pyproject.toml \
        tools/llm-council/council/__init__.py \
        tools/llm-council/council/__main__.py \
        tools/llm-council/tests/__init__.py \
        tools/llm-council/.env.example \
        tools/llm-council/README.md
git commit -m "feat(llm-council): scaffold council Python package with uv"
```

---

## Task 4: `profiles.py` — Profile dataclass + PROFILES dict

**Files:**
- Create: `tools/llm-council/council/profiles.py`
- Test: `tools/llm-council/tests/test_profiles.py`

- [ ] **Step 1: Write failing tests**

Create `tools/llm-council/tests/test_profiles.py`:

```python
import pytest
from council.profiles import Profile, PROFILES, get_profile


def test_premium_profile_exists():
    p = get_profile("premium")
    assert p.name == "premium"
    assert len(p.models) == 4
    assert p.chairman  # non-empty
    assert p.max_cost_per_query > 0


def test_variance_profile_exists():
    p = get_profile("variance")
    assert p.name == "variance"
    assert len(p.models) == 4
    assert p.chairman
    assert p.max_cost_per_query > 0


def test_unknown_profile_raises():
    with pytest.raises(KeyError):
        get_profile("nonexistent")


def test_chairman_must_be_listed_in_models_or_distinct():
    for name in ("premium", "variance"):
        p = get_profile(name)
        # Chairman is either one of the four council models, OR a distinct fifth model.
        # Either is allowed; what's NOT allowed is an empty chairman.
        assert p.chairman != ""


def test_profile_max_cost_is_positive_float():
    for name in ("premium", "variance"):
        p = get_profile(name)
        assert isinstance(p.max_cost_per_query, float)
        assert p.max_cost_per_query > 0


def test_premium_more_expensive_than_variance():
    # Premium uses frontier models; variance mixes mid-tier. Caps should reflect this.
    assert get_profile("premium").max_cost_per_query >= get_profile("variance").max_cost_per_query
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
cd tools/llm-council
uv run pytest tests/test_profiles.py -v
```

Expected: ImportError — `council.profiles` doesn't exist yet.

- [ ] **Step 3: Write `profiles.py`**

Create `tools/llm-council/council/profiles.py`:

```python
"""Council profiles — two named configurations (premium, variance)."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Profile:
    name: str
    models: tuple[str, ...]  # 4 OpenRouter model IDs
    chairman: str            # one of `models`, or a fifth distinct model
    max_cost_per_query: float


# Model IDs and caps are sourced from model-selection-2026-05-14.md.
# Update both files together; this is the single source of truth at runtime.
PROFILES: dict[str, Profile] = {
    "premium": Profile(
        name="premium",
        models=(
            # FILLED IN FROM Task 1 OUTPUT:
            # e.g. "openai/gpt-X.Y", "anthropic/claude-X.Y", "google/gemini-X.Y", "x-ai/grok-Y"
        ),
        chairman="",  # FILLED IN FROM Task 1 OUTPUT
        max_cost_per_query=0.0,  # FILLED IN FROM Task 1 OUTPUT
    ),
    "variance": Profile(
        name="variance",
        models=(
            # FILLED IN FROM Task 1 OUTPUT:
            # mix of premium + mid-tier, maximally different RLHF lineages
        ),
        chairman="",  # FILLED IN FROM Task 1 OUTPUT
        max_cost_per_query=0.0,  # FILLED IN FROM Task 1 OUTPUT
    ),
}


def get_profile(name: str) -> Profile:
    """Return the named profile or raise KeyError with available names."""
    if name not in PROFILES:
        available = ", ".join(sorted(PROFILES))
        raise KeyError(f"Unknown profile {name!r}. Available: {available}")
    return PROFILES[name]
```

**IMPORTANT:** Replace every `# FILLED IN FROM Task 1 OUTPUT` block with the actual model IDs and cap values from `tools/llm-council/model-selection-2026-05-14.md`. The tests will fail until real values are in place — that's intentional, it forces consumption of Task 1's output.

- [ ] **Step 4: Fill in the actual Task 1 values**

Open `tools/llm-council/model-selection-2026-05-14.md` and copy the model IDs into the two `models=(...)` tuples and the `chairman=` strings, and the per-query caps into `max_cost_per_query=` for both profiles.

- [ ] **Step 5: Run tests, verify they pass**

```bash
uv run pytest tests/test_profiles.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/profiles.py tools/llm-council/tests/test_profiles.py
git commit -m "feat(llm-council): premium and variance profiles with caps from model selection"
```

---

## Task 5: `prompts.py` — three-stage prompt templates

**Files:**
- Create: `tools/llm-council/council/prompts.py`
- Test: `tools/llm-council/tests/test_prompts.py`

- [ ] **Step 1: Write failing tests**

Create `tools/llm-council/tests/test_prompts.py`:

```python
from council.prompts import (
    fanout_prompt,
    crossrank_prompt,
    chairman_prompt,
)


def test_fanout_prompt_includes_user_query():
    p = fanout_prompt(user_query="Write a haiku about pythons.")
    assert "Write a haiku about pythons." in p


def test_crossrank_prompt_anonymizes_with_letters():
    others = [
        {"model_id": "openai/gpt-X", "content": "Response one body."},
        {"model_id": "anthropic/claude-X", "content": "Response two body."},
        {"model_id": "google/gemini-X", "content": "Response three body."},
    ]
    p = crossrank_prompt(user_query="Q", others=others)
    # Anonymized labels A, B, C appear; real model IDs do NOT
    assert "Response A" in p
    assert "Response B" in p
    assert "Response C" in p
    assert "openai/gpt-X" not in p
    assert "anthropic/claude-X" not in p
    assert "google/gemini-X" not in p
    # All response bodies are present
    assert "Response one body." in p
    assert "Response two body." in p
    assert "Response three body." in p


def test_crossrank_prompt_requests_json_ranking():
    p = crossrank_prompt(user_query="Q", others=[
        {"model_id": "m1", "content": "c1"},
        {"model_id": "m2", "content": "c2"},
    ])
    # The prompt instructs the model to return a JSON object with `ranking` and `reasoning`
    assert "JSON" in p or "json" in p
    assert "ranking" in p
    assert "reasoning" in p


def test_chairman_prompt_includes_named_responses_and_rankings():
    responses = [
        {"model_id": "openai/gpt-X", "content": "Resp A"},
        {"model_id": "anthropic/claude-X", "content": "Resp B"},
    ]
    rankings = [
        {"judge_model": "openai/gpt-X", "ranking": ["B", "A"], "reasoning": "B was more concise."},
        {"judge_model": "anthropic/claude-X", "ranking": ["A", "B"], "reasoning": "A had better insight."},
    ]
    p = chairman_prompt(user_query="Q", responses=responses, rankings=rankings)
    # Chairman sees real model IDs (NOT anonymized — synthesis benefits from naming)
    assert "openai/gpt-X" in p
    assert "anthropic/claude-X" in p
    # Both response bodies and reasoning are present
    assert "Resp A" in p
    assert "Resp B" in p
    assert "B was more concise." in p
    assert "A had better insight." in p
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
uv run pytest tests/test_prompts.py -v
```

Expected: ImportError — `council.prompts` doesn't exist.

- [ ] **Step 3: Write `prompts.py`**

Create `tools/llm-council/council/prompts.py`:

```python
"""System prompts for the three council stages.

Stage 1 (fan-out): each model receives the raw user query, no context about other models.
Stage 2 (cross-rank): each model receives the other N-1 responses with anonymized labels.
Stage 3 (chairman): one model receives the original query, all named responses, all rankings.

Lifted with attribution from karpathy/llm-council's prompts and adapted for our use cases.
"""

from typing import Iterable
import json


FANOUT_SYSTEM = """You are a member of an LLM Council. The user has posed a question to a panel \
of four frontier models, and you are one of them. Answer the user's question to the best of your \
ability. Be substantive, specific, and direct. Do not hedge unnecessarily. Your response will \
later be cross-ranked by the other council members and synthesized by a chairman."""


CROSSRANK_SYSTEM = """You are a member of an LLM Council reviewing the responses of the other \
council members to a user's question. You see anonymized responses labeled "Response A", \
"Response B", etc. — you do NOT know which model wrote which.

Rank the responses by overall quality (accuracy + insight + clarity), best first. Then briefly \
explain your ranking in 2-4 sentences.

You MUST return a single JSON object with exactly these keys:
{
  "ranking": ["A", "B", "C"],   // letters in descending quality order
  "reasoning": "string explaining the ranking"
}

Return ONLY the JSON object — no preamble, no markdown fence."""


CHAIRMAN_SYSTEM = """You are the Chairman of an LLM Council. Four other models have each \
independently answered a user's question, then cross-ranked each other's responses anonymously. \
You now see the original question, all four named responses, and all four rankings with reasoning.

Synthesize a single final response that:
1. Resolves disagreements between models (cite which model claimed what where useful)
2. Identifies points of convergence (high confidence) and divergence (low confidence)
3. Produces a direct, substantive answer to the user's original question

Be specific about which model contributed which insight. The user values seeing the lineage."""


def fanout_prompt(*, user_query: str) -> str:
    """Build the user-facing prompt for Stage 1. System prompt is FANOUT_SYSTEM."""
    return user_query


def crossrank_prompt(*, user_query: str, others: list[dict]) -> str:
    """Build the user-facing prompt for Stage 2. `others` is a list of {model_id, content} dicts
    for the OTHER N-1 council members (the judge's own response is excluded by the caller).

    Anonymizes model IDs with letters A, B, C, ... (per call — fresh mapping every cross-rank).
    """
    if not others:
        raise ValueError("crossrank_prompt requires at least one other response")
    labels = [chr(ord("A") + i) for i in range(len(others))]
    sections = "\n\n".join(
        f"=== Response {label} ===\n{o['content']}" for label, o in zip(labels, others)
    )
    return f"""The original user question:

{user_query}

You see {len(others)} other council members' responses below, anonymized:

{sections}

Return your ranking and reasoning as a JSON object per the system instructions."""


def chairman_prompt(*, user_query: str, responses: list[dict], rankings: list[dict]) -> str:
    """Build the user-facing prompt for Stage 3.

    `responses` is a list of {model_id, content}; `rankings` is a list of
    {judge_model, ranking, reasoning}.

    Unlike Stage 2, models are NAMED here — the chairman benefits from knowing lineage.
    """
    response_block = "\n\n".join(
        f"=== {r['model_id']} ===\n{r['content']}" for r in responses
    )
    ranking_block = "\n\n".join(
        f"=== {rk['judge_model']} ranked ===\n"
        f"Order (best first): {' > '.join(rk['ranking'])}\n"
        f"Reasoning: {rk['reasoning']}"
        for rk in rankings
    )
    return f"""Original user question:

{user_query}

=== Council responses (named) ===

{response_block}

=== Cross-rankings ===

{ranking_block}

Synthesize the final response per the system instructions."""
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
uv run pytest tests/test_prompts.py -v
```

Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/prompts.py tools/llm-council/tests/test_prompts.py
git commit -m "feat(llm-council): three-stage prompt templates with model anonymization in cross-rank"
```

---

## Task 6: `client.py` — async OpenRouter client

**Files:**
- Create: `tools/llm-council/council/client.py`
- Create: `tools/llm-council/tests/conftest.py`
- Test: `tools/llm-council/tests/test_client.py`

- [ ] **Step 1: Write conftest fixtures**

Create `tools/llm-council/tests/conftest.py`:

```python
"""Shared pytest fixtures."""

import os
import json
from pathlib import Path

import pytest


@pytest.fixture
def fake_api_key(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-fake-for-tests")
    yield "sk-or-v1-fake-for-tests"


@pytest.fixture
def tmp_spend_dir(tmp_path, monkeypatch):
    spend_dir = tmp_path / "vault" / "health"
    spend_dir.mkdir(parents=True)
    monkeypatch.setenv("COUNCIL_SPEND_DIR", str(spend_dir))
    yield spend_dir
```

- [ ] **Step 2: Write failing tests**

Create `tools/llm-council/tests/test_client.py`:

```python
import pytest
from httpx import Response

from council.client import OpenRouterClient, ModelResponse, ClientError


@pytest.mark.asyncio
async def test_complete_returns_typed_response(fake_api_key, httpx_mock):
    httpx_mock.add_response(
        url="https://openrouter.ai/api/v1/chat/completions",
        method="POST",
        json={
            "choices": [{"message": {"content": "hello world"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        },
    )
    client = OpenRouterClient()
    resp = await client.complete(
        model="openai/gpt-X",
        system="You are helpful.",
        user="hi",
    )
    assert isinstance(resp, ModelResponse)
    assert resp.model_id == "openai/gpt-X"
    assert resp.content == "hello world"
    assert resp.tokens_in == 10
    assert resp.tokens_out == 5
    assert resp.latency_ms > 0
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_sends_correct_payload(fake_api_key, httpx_mock):
    httpx_mock.add_response(
        url="https://openrouter.ai/api/v1/chat/completions",
        method="POST",
        json={
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
        },
    )
    client = OpenRouterClient()
    await client.complete(model="m", system="sys", user="usr")
    sent = httpx_mock.get_request()
    assert sent.headers["authorization"] == "Bearer sk-or-v1-fake-for-tests"
    import json
    body = json.loads(sent.content)
    assert body["model"] == "m"
    assert body["messages"] == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ]
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_retries_on_5xx_then_succeeds(fake_api_key, httpx_mock):
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(
        json={
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
        }
    )
    client = OpenRouterClient(max_retries=1)
    resp = await client.complete(model="m", system="s", user="u")
    assert resp.content == "ok"
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_raises_on_persistent_5xx(fake_api_key, httpx_mock):
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(status_code=503)
    client = OpenRouterClient(max_retries=1)
    with pytest.raises(ClientError) as exc:
        await client.complete(model="m", system="s", user="u")
    assert "503" in str(exc.value)
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_raises_on_content_filter_no_retry(fake_api_key, httpx_mock):
    # Content-policy refusals are non-retryable
    httpx_mock.add_response(
        status_code=400,
        json={"error": {"code": "content_filter", "message": "refused"}},
    )
    client = OpenRouterClient(max_retries=3)
    with pytest.raises(ClientError) as exc:
        await client.complete(model="m", system="s", user="u")
    assert "content_filter" in str(exc.value) or "refused" in str(exc.value)
    # Should have made exactly 1 request, not retried
    assert len(httpx_mock.get_requests()) == 1
    await client.aclose()


@pytest.mark.asyncio
async def test_missing_api_key_raises_at_init(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ClientError) as exc:
        OpenRouterClient()
    assert "OPENROUTER_API_KEY" in str(exc.value)
```

- [ ] **Step 3: Run tests, verify they fail**

```bash
uv run pytest tests/test_client.py -v
```

Expected: ImportError — `council.client` doesn't exist.

- [ ] **Step 4: Write `client.py`**

Create `tools/llm-council/council/client.py`:

```python
"""Async OpenRouter client wrapping httpx with retry + typed responses."""

import asyncio
import os
import time
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

# Load .env walking up from CWD; superuser-pack root is expected to hold OPENROUTER_API_KEY.
load_dotenv()

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


@dataclass
class ModelResponse:
    model_id: str
    content: str
    tokens_in: int
    tokens_out: int
    latency_ms: int


class ClientError(Exception):
    """Raised on any non-recoverable client failure."""


class OpenRouterClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = OPENROUTER_BASE,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
    ) -> None:
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise ClientError(
                "OPENROUTER_API_KEY not found in environment. "
                "Set it in the superuser-pack root .env file."
            )
        self._api_key = key
        self._base_url = base_url
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def complete(self, *, model: str, system: str, user: str) -> ModelResponse:
        """Single non-streaming completion call. Retries 5xx; does not retry 4xx."""
        url = f"{self._base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }

        attempt = 0
        start = time.perf_counter()
        while True:
            try:
                resp = await self._client.post(url, headers=headers, json=payload)
            except httpx.TimeoutException as e:
                if attempt >= self._max_retries:
                    raise ClientError(f"timeout after {self._timeout}s on model {model}") from e
                attempt += 1
                await asyncio.sleep(0.5 * (2 ** attempt))
                continue

            if 200 <= resp.status_code < 300:
                body = resp.json()
                content = body["choices"][0]["message"]["content"]
                usage = body.get("usage", {})
                latency_ms = int((time.perf_counter() - start) * 1000)
                return ModelResponse(
                    model_id=model,
                    content=content,
                    tokens_in=usage.get("prompt_tokens", 0),
                    tokens_out=usage.get("completion_tokens", 0),
                    latency_ms=latency_ms,
                )

            # 4xx — do not retry. Surface the error.
            if 400 <= resp.status_code < 500:
                try:
                    msg = resp.json().get("error", {}).get("message", resp.text)
                    code = resp.json().get("error", {}).get("code", "")
                except Exception:
                    msg = resp.text
                    code = ""
                raise ClientError(
                    f"4xx from OpenRouter on model {model}: {resp.status_code} {code} {msg}"
                )

            # 5xx — retry if budget remains.
            if attempt >= self._max_retries:
                raise ClientError(
                    f"persistent 5xx from OpenRouter on model {model}: {resp.status_code}"
                )
            attempt += 1
            await asyncio.sleep(0.5 * (2 ** attempt))
```

- [ ] **Step 5: Run tests, verify they pass**

```bash
uv run pytest tests/test_client.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/client.py \
        tools/llm-council/tests/conftest.py \
        tools/llm-council/tests/test_client.py
git commit -m "feat(llm-council): async OpenRouter client with 5xx retry and typed responses"
```

---

## Task 7: `budget.py` — cost estimation + cap enforcement

**Files:**
- Create: `tools/llm-council/council/budget.py`
- Test: `tools/llm-council/tests/test_budget.py`

- [ ] **Step 1: Write failing tests**

Create `tools/llm-council/tests/test_budget.py`:

```python
import json
from datetime import date
from pathlib import Path

import pytest

from council.budget import (
    estimate_cost,
    record_spend,
    preflight,
    BudgetExceeded,
    Pricing,
)


SAMPLE_PRICING = {
    "openai/gpt-X": Pricing(prompt_per_1k=0.0050, completion_per_1k=0.0150),
    "anthropic/claude-X": Pricing(prompt_per_1k=0.0030, completion_per_1k=0.0150),
    "google/gemini-X": Pricing(prompt_per_1k=0.0025, completion_per_1k=0.0100),
    "x-ai/grok-X": Pricing(prompt_per_1k=0.0050, completion_per_1k=0.0150),
}


def test_estimate_cost_sums_per_model():
    cost = estimate_cost(
        pricing=SAMPLE_PRICING,
        per_model_tokens=[
            ("openai/gpt-X", 1000, 500),       # in_tokens, out_tokens
            ("anthropic/claude-X", 1000, 500),
        ],
    )
    # GPT-X: 1k * 0.005 + 0.5k * 0.015 = 0.005 + 0.0075 = 0.0125
    # Claude-X: 1k * 0.003 + 0.5k * 0.015 = 0.003 + 0.0075 = 0.0105
    # Total: 0.023
    assert cost == pytest.approx(0.023, abs=1e-6)


def test_estimate_cost_raises_on_unknown_model():
    with pytest.raises(KeyError):
        estimate_cost(
            pricing=SAMPLE_PRICING,
            per_model_tokens=[("unknown/model", 100, 100)],
        )


def test_record_spend_appends_atomically(tmp_spend_dir):
    today = date(2026, 5, 14)
    record_spend(amount=0.50, profile="variance", tag="test-1", on_date=today)
    record_spend(amount=0.30, profile="premium", tag="test-2", on_date=today)
    daily_file = tmp_spend_dir / "council-spend-2026-05-14.json"
    assert daily_file.exists()
    data = json.loads(daily_file.read_text())
    assert data["total"] == pytest.approx(0.80, abs=1e-6)
    assert len(data["runs"]) == 2
    assert data["runs"][0]["amount"] == 0.50
    assert data["runs"][0]["tag"] == "test-1"


def test_preflight_passes_when_under_caps(tmp_spend_dir):
    preflight(
        estimated=0.40,
        per_query_cap=0.80,
        daily_cap=5.00,
        monthly_cap=30.00,
        on_date=date(2026, 5, 14),
    )  # no exception


def test_preflight_rejects_when_over_per_query_cap(tmp_spend_dir):
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=0.90,
            per_query_cap=0.80,
            daily_cap=5.00,
            monthly_cap=30.00,
            on_date=date(2026, 5, 14),
        )
    assert "per-query" in str(exc.value).lower()


def test_preflight_rejects_when_estimated_plus_today_over_daily(tmp_spend_dir):
    today = date(2026, 5, 14)
    record_spend(amount=4.70, profile="premium", tag="prior", on_date=today)
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=0.50,  # 4.70 + 0.50 = 5.20 > 5.00 daily cap
            per_query_cap=0.80,
            daily_cap=5.00,
            monthly_cap=30.00,
            on_date=today,
        )
    assert "daily" in str(exc.value).lower()


def test_preflight_rejects_when_month_to_date_plus_estimated_over_monthly(tmp_spend_dir):
    # Spread spend across days in the same month
    from datetime import date as date_cls
    for day in (1, 2, 3, 4, 5):
        record_spend(amount=5.00, profile="premium", tag=f"day-{day}", on_date=date_cls(2026, 5, day))
    # Month-to-date = 25.00; add 6.00 → 31.00 > 30.00 monthly cap
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=6.00,
            per_query_cap=10.00,
            daily_cap=100.00,  # high so daily doesn't fire
            monthly_cap=30.00,
            on_date=date_cls(2026, 5, 6),
        )
    assert "monthly" in str(exc.value).lower()
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
uv run pytest tests/test_budget.py -v
```

Expected: ImportError — `council.budget` doesn't exist.

- [ ] **Step 3: Write `budget.py`**

Create `tools/llm-council/council/budget.py`:

```python
"""Cost estimation, spend recording, and pre-flight cap enforcement.

Spend files live at $COUNCIL_SPEND_DIR (default: vault/health/) and are append-only
JSON written atomically via tmp + rename.
"""

import json
import os
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Pricing:
    """Per-1k-token prices in USD."""
    prompt_per_1k: float
    completion_per_1k: float


class BudgetExceeded(Exception):
    """Raised when a pre-flight check rejects a query."""


def _spend_dir() -> Path:
    raw = os.environ.get("COUNCIL_SPEND_DIR")
    if raw:
        d = Path(raw)
    else:
        # Walk up to find vault/health/ relative to this file.
        here = Path(__file__).resolve()
        d = here.parents[3] / "vault" / "health"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _daily_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.isoformat()}.json"


def _monthly_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.strftime('%Y-%m')}.json"


def estimate_cost(*, pricing: dict[str, Pricing], per_model_tokens: list[tuple[str, int, int]]) -> float:
    """Sum per-model (in_tokens × prompt_per_1k + out_tokens × completion_per_1k) over /1000.

    `per_model_tokens` is a list of (model_id, in_tokens, out_tokens) tuples.
    Raises KeyError if any model_id is missing from pricing.
    """
    total = 0.0
    for model_id, in_tokens, out_tokens in per_model_tokens:
        if model_id not in pricing:
            raise KeyError(f"pricing missing for model {model_id!r}")
        p = pricing[model_id]
        total += (in_tokens / 1000.0) * p.prompt_per_1k
        total += (out_tokens / 1000.0) * p.completion_per_1k
    return total


def _atomic_write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def _read_total_for_day(on_date: date) -> float:
    f = _daily_file(on_date)
    if not f.exists():
        return 0.0
    return float(json.loads(f.read_text()).get("total", 0.0))


def _read_total_for_month(on_date: date) -> float:
    # Sum every council-spend-YYYY-MM-DD.json in the same YYYY-MM
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    total = 0.0
    for f in _spend_dir().glob(f"{prefix}*.json"):
        try:
            total += float(json.loads(f.read_text()).get("total", 0.0))
        except (json.JSONDecodeError, ValueError):
            continue
    return total


def record_spend(*, amount: float, profile: str, tag: str, on_date: date) -> None:
    """Append a run to today's daily spend file. Atomic write."""
    f = _daily_file(on_date)
    if f.exists():
        data = json.loads(f.read_text())
    else:
        data = {"date": on_date.isoformat(), "total": 0.0, "runs": []}
    data["runs"].append({"amount": amount, "profile": profile, "tag": tag})
    data["total"] = round(data["total"] + amount, 6)
    _atomic_write_json(f, data)


def preflight(
    *,
    estimated: float,
    per_query_cap: float,
    daily_cap: float,
    monthly_cap: float,
    on_date: date,
    force: bool = False,
) -> None:
    """Reject the query if any cap would be breached.

    `force=True` bypasses per-query cap (but still respects daily/monthly).
    Daily and monthly caps are NEVER bypassed.
    """
    if not force and estimated > per_query_cap:
        raise BudgetExceeded(
            f"per-query cap exceeded: estimated ${estimated:.4f} > cap ${per_query_cap:.4f}. "
            f"Use --force to override (still subject to daily/monthly caps)."
        )
    today_total = _read_total_for_day(on_date)
    if today_total + estimated > daily_cap:
        raise BudgetExceeded(
            f"daily cap would be exceeded: today=${today_total:.4f} + "
            f"estimated=${estimated:.4f} > daily_cap=${daily_cap:.4f}"
        )
    month_total = _read_total_for_month(on_date)
    if month_total + estimated > monthly_cap:
        raise BudgetExceeded(
            f"monthly cap would be exceeded: month-to-date=${month_total:.4f} + "
            f"estimated=${estimated:.4f} > monthly_cap=${monthly_cap:.4f}"
        )
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
uv run pytest tests/test_budget.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/budget.py tools/llm-council/tests/test_budget.py
git commit -m "feat(llm-council): per-query / daily / monthly cost gates with atomic spend tracking"
```

---

## Task 8: `pipeline.py` — three-stage orchestrator

**Files:**
- Create: `tools/llm-council/council/pipeline.py`
- Test: `tools/llm-council/tests/test_pipeline.py`

- [ ] **Step 1: Write failing tests**

Create `tools/llm-council/tests/test_pipeline.py`:

```python
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from council.client import ModelResponse, ClientError
from council.pipeline import run_council, CouncilSession
from council.profiles import Profile


@pytest.fixture
def fake_profile():
    return Profile(
        name="test",
        models=("m1", "m2", "m3", "m4"),
        chairman="m1",
        max_cost_per_query=10.0,
    )


def _resp(model: str, text: str, tin: int = 10, tout: int = 10) -> ModelResponse:
    return ModelResponse(model_id=model, content=text, tokens_in=tin, tokens_out=tout, latency_ms=10)


@pytest.mark.asyncio
async def test_run_council_happy_path_calls_all_three_stages(fake_profile):
    client = MagicMock()
    # Stage 1: 4 fan-out calls
    # Stage 2: 4 cross-rank calls
    # Stage 3: 1 chairman call
    valid_ranking = '{"ranking": ["A", "B", "C"], "reasoning": "fine."}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "answer 1"),
        _resp("m2", "answer 2"),
        _resp("m3", "answer 3"),
        _resp("m4", "answer 4"),
        _resp("m1", valid_ranking),
        _resp("m2", valid_ranking),
        _resp("m3", valid_ranking),
        _resp("m4", valid_ranking),
        _resp("m1", "synthesized."),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert isinstance(session, CouncilSession)
    assert len(session.responses) == 4
    assert len(session.rankings) == 4
    assert session.chairman_response.content == "synthesized."
    assert client.complete.call_count == 9


@pytest.mark.asyncio
async def test_run_council_degraded_with_one_stage1_failure(fake_profile):
    client = MagicMock()
    valid_ranking = '{"ranking": ["A", "B"], "reasoning": "fine."}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        ClientError("m2 timed out"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        # Cross-rank: now only 3 judges (m1, m3, m4)
        _resp("m1", valid_ranking),
        _resp("m3", valid_ranking),
        _resp("m4", valid_ranking),
        # Chairman
        _resp("m1", "synth"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert len(session.responses) == 3  # N-1 survivors
    assert len(session.rankings) == 3
    assert "m2" in session.dropped_models
    assert session.chairman_response.content == "synth"


@pytest.mark.asyncio
async def test_run_council_wraps_chairman_failure_as_runtime_error(fake_profile):
    """Spec §5: chairman failure must surface as a RuntimeError the CLI can catch."""
    client = MagicMock()
    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", valid),
        _resp("m2", valid),
        _resp("m3", valid),
        _resp("m4", valid),
        ClientError("chairman timeout"),  # Stage 3 fails
    ])

    with pytest.raises(RuntimeError) as exc:
        await run_council(
            client=client,
            profile=fake_profile,
            user_query="Q",
            tag="t",
        )
    assert "chairman synthesis failed" in str(exc.value).lower()
    assert "m1" in str(exc.value)  # the chairman model name appears


@pytest.mark.asyncio
async def test_run_council_aborts_on_two_stage1_failures(fake_profile):
    client = MagicMock()
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        ClientError("m2 timed out"),
        ClientError("m3 timed out"),
        _resp("m4", "a4"),
    ])

    with pytest.raises(RuntimeError) as exc:
        await run_council(
            client=client,
            profile=fake_profile,
            user_query="Q",
            tag="t",
        )
    assert "two or more" in str(exc.value).lower() or "council unavailable" in str(exc.value).lower()


@pytest.mark.asyncio
async def test_cross_rank_retries_non_json_then_skips(fake_profile):
    client = MagicMock()
    # m2 returns garbage twice → its ranking is skipped; chairman still gets 3 rankings.
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m2", "not json"),         # first attempt fails to parse
        _resp("m2", "still not json"),   # retry also fails
        _resp("m3", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m4", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m1", "synthesized"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert len(session.rankings) == 3  # m2's ranking skipped
    assert all(r["judge_model"] != "m2" for r in session.rankings)


@pytest.mark.asyncio
async def test_session_writes_json_to_data_sessions_dir(fake_profile, tmp_path):
    client = MagicMock()
    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", valid),
        _resp("m2", valid),
        _resp("m3", valid),
        _resp("m4", valid),
        _resp("m1", "synth"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="voice-mode",
        sessions_dir=tmp_path,
    )

    # A JSON file should have been written at tmp_path/<session.id>.json
    session_files = list(tmp_path.glob("*.json"))
    assert len(session_files) == 1
    data = json.loads(session_files[0].read_text())
    assert data["tag"] == "voice-mode"
    assert data["profile"] == "test"
    assert len(data["responses"]) == 4
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
uv run pytest tests/test_pipeline.py -v
```

Expected: ImportError — `council.pipeline` doesn't exist.

- [ ] **Step 3: Write `pipeline.py`**

Create `tools/llm-council/council/pipeline.py`:

```python
"""Three-stage council orchestrator: fan-out → cross-rank → chairman."""

import asyncio
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from council.client import ClientError, ModelResponse, OpenRouterClient
from council.profiles import Profile
from council.prompts import (
    CHAIRMAN_SYSTEM,
    CROSSRANK_SYSTEM,
    FANOUT_SYSTEM,
    chairman_prompt,
    crossrank_prompt,
    fanout_prompt,
)


@dataclass
class CouncilSession:
    id: str
    profile: str
    tag: str
    user_query: str
    responses: list[dict]                  # [{model_id, content, tokens_in, tokens_out, latency_ms}]
    rankings: list[dict]                   # [{judge_model, ranking, reasoning}]
    chairman_response: ModelResponse
    dropped_models: list[str] = field(default_factory=list)
    ranking_failed_models: list[str] = field(default_factory=list)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    duration_ms: int = 0


def _parse_ranking(content: str) -> dict | None:
    """Try to parse the cross-rank JSON. Returns the dict or None on failure."""
    try:
        # Strip optional markdown fence if present
        text = content.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)
        if "ranking" in data and "reasoning" in data:
            return data
    except (json.JSONDecodeError, IndexError, KeyError):
        return None
    return None


async def _fanout(client: OpenRouterClient, models: tuple[str, ...], user_query: str) -> tuple[list[ModelResponse], list[str]]:
    """Stage 1: parallel fan-out. Returns (surviving_responses, dropped_model_ids)."""
    user_msg = fanout_prompt(user_query=user_query)
    coros = [
        client.complete(model=m, system=FANOUT_SYSTEM, user=user_msg)
        for m in models
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    survivors: list[ModelResponse] = []
    dropped: list[str] = []
    for model, r in zip(models, results):
        if isinstance(r, Exception):
            dropped.append(model)
        else:
            survivors.append(r)
    return survivors, dropped


async def _crossrank_one(
    client: OpenRouterClient,
    judge_model: str,
    user_query: str,
    others: list[dict],
) -> dict | None:
    """Run one judge's cross-rank. Returns parsed dict or None after retry failure."""
    user_msg = crossrank_prompt(user_query=user_query, others=others)
    try:
        first = await client.complete(model=judge_model, system=CROSSRANK_SYSTEM, user=user_msg)
        parsed = _parse_ranking(first.content)
        if parsed is not None:
            return {"judge_model": judge_model, **parsed}
        retry = await client.complete(
            model=judge_model,
            system=CROSSRANK_SYSTEM + "\n\nReturn ONLY a JSON object. No prose, no markdown fence.",
            user=user_msg,
        )
        parsed = _parse_ranking(retry.content)
        if parsed is not None:
            return {"judge_model": judge_model, **parsed}
    except ClientError:
        return None
    return None


async def _crossrank(
    client: OpenRouterClient,
    responses: list[ModelResponse],
    user_query: str,
) -> tuple[list[dict], list[str]]:
    """Stage 2: each surviving model judges the OTHER N-1 responses.

    Returns (parsed_rankings, ranking_failed_model_ids).
    """
    coros = []
    judge_models = []
    for judge in responses:
        others = [
            {"model_id": r.model_id, "content": r.content}
            for r in responses
            if r.model_id != judge.model_id
        ]
        coros.append(_crossrank_one(client, judge.model_id, user_query, others))
        judge_models.append(judge.model_id)
    results = await asyncio.gather(*coros)
    rankings: list[dict] = []
    failed: list[str] = []
    for model, r in zip(judge_models, results):
        if r is None:
            failed.append(model)
        else:
            rankings.append(r)
    return rankings, failed


async def _chairman(
    client: OpenRouterClient,
    chairman_model: str,
    user_query: str,
    responses: list[ModelResponse],
    rankings: list[dict],
) -> ModelResponse:
    """Stage 3: synthesis."""
    user_msg = chairman_prompt(
        user_query=user_query,
        responses=[{"model_id": r.model_id, "content": r.content} for r in responses],
        rankings=rankings,
    )
    return await client.complete(
        model=chairman_model,
        system=CHAIRMAN_SYSTEM,
        user=user_msg,
    )


async def run_council(
    *,
    client: OpenRouterClient,
    profile: Profile,
    user_query: str,
    tag: str,
    sessions_dir: Path | None = None,
) -> CouncilSession:
    """End-to-end council run. Aborts on 2+ Stage-1 failures; degrades on 1."""
    started = time.perf_counter()
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    responses, dropped = await _fanout(client, profile.models, user_query)
    if len(dropped) >= 2:
        raise RuntimeError(
            f"Council unavailable: two or more models failed in Stage 1 ({dropped}). "
            "Fall back to single-model review."
        )

    rankings, ranking_failed = await _crossrank(client, responses, user_query)

    try:
        chairman_resp = await _chairman(
            client,
            profile.chairman,
            user_query,
            responses,
            rankings,
        )
    except ClientError as e:
        # Spec §5: chairman failure aborts with a clear message. The CLI catches
        # RuntimeError and produces a graceful exit; we wrap ClientError here
        # to centralize error normalization at the pipeline boundary.
        raise RuntimeError(
            f"Chairman synthesis failed ({profile.chairman}): {e}. "
            f"Stage-1 produced {len(responses)} responses; Stage-2 produced "
            f"{len(rankings)} rankings. Council session JSON was not written. "
            f"Fall back to single-model review or retry."
        ) from e

    total_in = sum(r.tokens_in for r in responses) + chairman_resp.tokens_in
    total_out = sum(r.tokens_out for r in responses) + chairman_resp.tokens_out

    session = CouncilSession(
        id=session_id,
        profile=profile.name,
        tag=tag,
        user_query=user_query,
        responses=[
            {
                "model_id": r.model_id,
                "content": r.content,
                "tokens_in": r.tokens_in,
                "tokens_out": r.tokens_out,
                "latency_ms": r.latency_ms,
            }
            for r in responses
        ],
        rankings=rankings,
        chairman_response=chairman_resp,
        dropped_models=dropped,
        ranking_failed_models=ranking_failed,
        total_tokens_in=total_in,
        total_tokens_out=total_out,
        duration_ms=int((time.perf_counter() - started) * 1000),
    )

    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        out = sessions_dir / f"{session_id}.json"
        out.write_text(json.dumps({
            "id": session.id,
            "profile": session.profile,
            "tag": session.tag,
            "user_query": session.user_query,
            "responses": session.responses,
            "rankings": session.rankings,
            "chairman": asdict(chairman_resp),
            "dropped_models": session.dropped_models,
            "ranking_failed_models": session.ranking_failed_models,
            "total_tokens_in": session.total_tokens_in,
            "total_tokens_out": session.total_tokens_out,
            "duration_ms": session.duration_ms,
        }, indent=2))

    return session
```

- [ ] **Step 4: Run tests, verify they pass**

```bash
uv run pytest tests/test_pipeline.py -v
```

Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/pipeline.py tools/llm-council/tests/test_pipeline.py
git commit -m "feat(llm-council): three-stage pipeline with degraded-mode + ranking retry"
```

---

## Task 9: `cli.py` — `python -m council` entry point

**Files:**
- Create: `tools/llm-council/council/cli.py`
- Test: `tools/llm-council/tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

Create `tools/llm-council/tests/test_cli.py`:

```python
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from council.cli import main
from council.client import ModelResponse


def _r(model: str, content: str) -> ModelResponse:
    return ModelResponse(model_id=model, content=content, tokens_in=10, tokens_out=10, latency_ms=10)


def test_cli_help_shows_profiles(fake_api_key):
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "premium" in result.output or "profile" in result.output.lower()


def test_cli_writes_markdown_output(fake_api_key, tmp_path, tmp_spend_dir, monkeypatch):
    prompt_file = tmp_path / "in.md"
    prompt_file.write_text("What's the best way to test async code?")
    out_file = tmp_path / "out.md"

    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    fake_responses = [
        _r("m1", "Use pytest-asyncio."),
        _r("m2", "Use anyio."),
        _r("m3", "Use trio test."),
        _r("m4", "Use unittest IsolatedAsyncioTestCase."),
        _r("m1", valid), _r("m2", valid), _r("m3", valid), _r("m4", valid),
        _r("m1", "Synthesis: pytest-asyncio is most idiomatic..."),
    ]

    with patch("council.cli.OpenRouterClient") as mock_client_cls, \
         patch("council.cli.get_profile") as mock_get_profile:
        from council.profiles import Profile
        mock_get_profile.return_value = Profile(
            name="variance", models=("m1","m2","m3","m4"), chairman="m1", max_cost_per_query=10.0,
        )
        mock_inst = MagicMock()
        mock_inst.complete = AsyncMock(side_effect=fake_responses)
        mock_inst.aclose = AsyncMock()
        mock_client_cls.return_value = mock_inst

        runner = CliRunner()
        result = runner.invoke(main, [
            "--profile", "variance",
            "--prompt-file", str(prompt_file),
            "--output", str(out_file),
            "--tag", "test-tag",
            "--skip-budget-check",
        ])

    assert result.exit_code == 0, result.output
    assert out_file.exists()
    text = out_file.read_text()
    assert "What's the best way to test async code?" in text  # original prompt
    assert "Use pytest-asyncio." in text                       # m1 response
    assert "Synthesis: pytest-asyncio is most idiomatic..." in text  # chairman
    assert "test-tag" in text                                  # tag echoed


def test_cli_exits_nonzero_on_missing_prompt_file(fake_api_key, tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "--profile", "variance",
        "--prompt-file", str(tmp_path / "missing.md"),
        "--output", str(tmp_path / "out.md"),
        "--tag", "x",
    ])
    assert result.exit_code != 0
```

- [ ] **Step 2: Run tests, verify they fail**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: ImportError — `council.cli` doesn't exist.

- [ ] **Step 3: Write `cli.py`**

Create `tools/llm-council/council/cli.py`:

```python
"""`python -m council` entry point."""

import asyncio
import sys
from datetime import date
from pathlib import Path

import click
from rich.console import Console

from council.budget import BudgetExceeded, preflight, record_spend
from council.client import OpenRouterClient
from council.pipeline import run_council
from council.profiles import PROFILES, get_profile

console = Console()


def _render_markdown(session, profile, user_query: str, cost_usd: float) -> str:
    lines = []
    lines.append(f"# Council Session — {session.tag}\n")
    lines.append(f"- **Session ID:** `{session.id}`")
    lines.append(f"- **Profile:** `{profile.name}`")
    lines.append(f"- **Duration:** {session.duration_ms / 1000:.1f}s")
    lines.append(f"- **Tokens:** {session.total_tokens_in} in, {session.total_tokens_out} out")
    lines.append(f"- **Cost:** ${cost_usd:.4f}")
    if session.dropped_models:
        lines.append(f"- **Dropped models (Stage 1 failures):** {', '.join(session.dropped_models)}")
    if session.ranking_failed_models:
        lines.append(f"- **Ranking-failed judges (Stage 2):** {', '.join(session.ranking_failed_models)}")
    lines.append("")
    lines.append("## Original prompt\n")
    lines.append("```")
    lines.append(user_query)
    lines.append("```\n")

    lines.append("## Council responses\n")
    for r in session.responses:
        lines.append(f"### {r['model_id']}\n")
        lines.append(r["content"])
        lines.append("")

    lines.append("## Cross-rankings\n")
    for rk in session.rankings:
        lines.append(f"### Judge: {rk['judge_model']}\n")
        lines.append(f"- **Order:** {' > '.join(rk['ranking'])}")
        lines.append(f"- **Reasoning:** {rk['reasoning']}")
        lines.append("")

    lines.append("## Chairman synthesis\n")
    lines.append(f"_Chairman model: `{session.chairman_response.model_id}`_\n")
    lines.append(session.chairman_response.content)
    lines.append("")
    return "\n".join(lines)


@click.command()
@click.option("--profile", type=click.Choice(list(PROFILES.keys())), required=True)
@click.option("--prompt-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--tag", type=str, default="adhoc", help="Free-form label for spend tracking + filename.")
@click.option("--force", is_flag=True, help="Bypass per-query cap (daily/monthly still enforced).")
@click.option("--skip-budget-check", is_flag=True, hidden=True, help="Test-only: skip all budget gates.")
def main(profile: str, prompt_file: Path, output: Path, tag: str, force: bool, skip_budget_check: bool) -> None:
    """Run an LLM council session against the given prompt file."""
    user_query = prompt_file.read_text().strip()
    if not user_query:
        console.print("[red]Prompt file is empty.[/red]")
        sys.exit(1)

    p = get_profile(profile)

    if not skip_budget_check:
        # Pre-flight uses a coarse estimate. Real cost is computed post-run.
        # Conservative estimate: 4 models × (2k in + 2k out) + 1 chairman × (8k in + 2k out)
        # This is a rough enough estimate that we lean on per-query cap as the real gate.
        rough = p.max_cost_per_query * 0.5  # half the cap, before actual call
        try:
            preflight(
                estimated=rough,
                per_query_cap=p.max_cost_per_query,
                daily_cap=_load_daily_cap(),
                monthly_cap=_load_monthly_cap(),
                on_date=date.today(),
                force=force,
            )
        except BudgetExceeded as e:
            console.print(f"[red]Budget rejected: {e}[/red]")
            sys.exit(2)

    async def _go():
        client = OpenRouterClient()
        try:
            sessions_dir = output.parent / ".sessions"
            session = await run_council(
                client=client,
                profile=p,
                user_query=user_query,
                tag=tag,
                sessions_dir=sessions_dir,
            )
            return session
        finally:
            await client.aclose()

    try:
        session = asyncio.run(_go())
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(3)

    # Post-run actual cost (uses recorded usage; pricing snapshot loaded lazily).
    # For v0.1 we estimate from token counts × profile's avg price; refine in a future task.
    estimated_cost = (session.total_tokens_in / 1000.0) * 0.005 + (session.total_tokens_out / 1000.0) * 0.015

    if not skip_budget_check:
        record_spend(amount=estimated_cost, profile=p.name, tag=tag, on_date=date.today())

    output.write_text(_render_markdown(session, p, user_query, estimated_cost))
    console.print(f"[green]Council session written:[/green] {output}")
    console.print(f"[dim]Approximate cost: ${estimated_cost:.4f}[/dim]")


def _load_daily_cap() -> float:
    """Read daily cap from model-selection doc. v0.1 uses a hardcoded value; refine later."""
    # Replace with the value from tools/llm-council/model-selection-2026-05-14.md
    return float(_DAILY_CAP_USD)


def _load_monthly_cap() -> float:
    return float(_MONTHLY_CAP_USD)


# Hardcoded from model-selection-2026-05-14.md output of Task 1.
# Update both files together when refreshing caps.
_DAILY_CAP_USD = 5.00      # REPLACE WITH TASK 1 OUTPUT
_MONTHLY_CAP_USD = 30.00   # REPLACE WITH TASK 1 OUTPUT
```

- [ ] **Step 4: Replace cap placeholders with Task 1 values**

Open `tools/llm-council/model-selection-2026-05-14.md`. Find the daily and monthly cap values from §"Combined gates". Replace `_DAILY_CAP_USD = 5.00` and `_MONTHLY_CAP_USD = 30.00` in `cli.py` with those exact numbers.

- [ ] **Step 5: Run tests, verify they pass**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 6: Run the full test suite**

```bash
uv run pytest -v
```

Expected: every test in every test_*.py file PASSES. No skipped tests (except the e2e file, which isn't created yet).

- [ ] **Step 7: Commit**

```bash
git add tools/llm-council/council/cli.py tools/llm-council/tests/test_cli.py
git commit -m "feat(llm-council): CLI entry point with budget gates and markdown rendering"
```

---

## Task 10: Gated integration test

**Files:**
- Create: `tools/llm-council/tests/test_e2e.py`

- [ ] **Step 1: Write the gated integration test**

Create `tools/llm-council/tests/test_e2e.py`:

```python
"""End-to-end integration test that hits the real OpenRouter API.

Skipped unless INTEGRATION=1 is set. Uses the cheapest variance-profile models
to keep cost under ~$0.05 per run. Run manually with:

    INTEGRATION=1 uv run pytest tests/test_e2e.py -v -s
"""

import os
from pathlib import Path

import pytest

from council.client import OpenRouterClient
from council.pipeline import run_council
from council.profiles import get_profile

pytestmark = pytest.mark.skipif(
    os.environ.get("INTEGRATION") != "1",
    reason="set INTEGRATION=1 to run live API integration test",
)


@pytest.mark.asyncio
async def test_full_variance_council_run(tmp_path):
    """Cheap, real, end-to-end. Validates wire compatibility with OpenRouter."""
    client = OpenRouterClient(timeout_seconds=180.0)
    try:
        profile = get_profile("variance")
        session = await run_council(
            client=client,
            profile=profile,
            user_query=(
                "In one sentence, what is the most underrated principle of writing "
                "good unit tests?"
            ),
            tag="e2e-smoke",
            sessions_dir=tmp_path,
        )
    finally:
        await client.aclose()

    assert len(session.responses) >= 3            # allow N-1 degraded
    assert len(session.rankings) >= 2             # allow some ranking failures
    assert session.chairman_response.content      # non-empty
    assert session.total_tokens_in > 0
    assert session.total_tokens_out > 0
```

- [ ] **Step 2: Verify the test is skipped without the env flag**

```bash
uv run pytest tests/test_e2e.py -v
```

Expected: 1 test SKIPPED with reason "set INTEGRATION=1 to run live API integration test".

- [ ] **Step 3: (Optional) Run the live integration test**

```bash
INTEGRATION=1 uv run pytest tests/test_e2e.py -v -s
```

Expected: test PASSES. Will charge ~$0.05 to your OpenRouter account. If it fails, the error message tells you whether it's an auth issue, a model availability issue, or a wire-format mismatch.

- [ ] **Step 4: Commit**

```bash
git add tools/llm-council/tests/test_e2e.py
git commit -m "test(llm-council): gated INTEGRATION=1 e2e test against live OpenRouter"
```

---

## Task 11: Skill decision table

**Files:**
- Create: `.claude/skills/llm-council/decision-table.md`

- [ ] **Step 1: Write the decision table**

Create `.claude/skills/llm-council/decision-table.md`:

```markdown
# LLM Council — Decision Table

When to convene a council vs. use a single model vs. use Gemini Deep Research.

## Quick routing

| Question shape | Tool | Cost | Why |
|---|---|---|---|
| "Help me think through this code change" | Single-model Claude (in-session) | $0 | Code work; council adds noise |
| "Is this PRD missing anything?" | **`llm-council` premium** | $0.30–2 | Four-vendor stress-test surfaces holes one model misses |
| "Draft this cover letter and critique" | **`llm-council` premium** | $0.30–2 | Different RLHF biases → diverse tone critique |
| "Which interpretation of this voice spec is correct?" | **`llm-council` variance** | $0.10–0.80 | Divergence itself is the signal — mid-tier models add variance |
| "What could go wrong with this decision?" | **`llm-council` premium** | $0.30–2 | Each model's blind spot is different; pre-mortem benefits from diversity |
| "Research the landscape for X" | `gemini-deep-research` | $1–7 | Council = peer-review, not research with citations |
| "What's hot on Reddit this week" | `last30days` | $0 | Social conversation, not synthesis |
| "Synthesize 8 papers I've already read" | Single-model Claude | $0 | One model can hold all 8; council adds latency without insight |

## Profile selection

- **premium** — four frontier models, judging flat-out.
  - High-stakes synthesis: job-hunt artifacts, decision pre-mortems, PRD reviews.
  - When you'd rather pay $1 than have the answer be subtly wrong.

- **variance** — four models with maximally different RLHF lineages (premium + mid-tier mix).
  - Stylistic/divergence questions: voice modes, prompt-clarity tests.
  - When the *spread* between models is the signal, not their consensus.
  - Cheaper, so usable more frequently.

## When NOT to use council

- **Coding tasks.** Claude Code is the venue; council multiplies noise.
- **Anything `skill_optimizer` handles.** That's already a council (Opus generator + Qwen judge + Sonnet sample-check) tuned for SKILL.md.
- **Anything Qwen-local can answer at $0.** Cost discipline matters — don't burn OpenRouter credits on questions a local 14B can field.
- **Daily ops.** Single Claude is fine.

## Cost gates

- Per-query hard caps live in `tools/llm-council/council/profiles.py:PROFILES[<name>].max_cost_per_query`
- Daily / monthly governors live in `tools/llm-council/council/cli.py:_DAILY_CAP_USD` and `_MONTHLY_CAP_USD`
- Spend tracked in `vault/health/council-spend-{YYYY-MM-DD}.json`
- Use `--force` ONLY when Sean explicitly asks (bypasses per-query cap, not daily/monthly)
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/llm-council/decision-table.md
git commit -m "docs(llm-council): decision table for council vs single-model vs gemini-deep-research"
```

---

## Task 12: `SKILL.md` for the new skill

**Files:**
- Create: `.claude/skills/llm-council/SKILL.md`

- [ ] **Step 1: Write the SKILL.md**

Create `.claude/skills/llm-council/SKILL.md`:

```markdown
---
name: llm-council
description: Convene a multi-vendor LLM council (4 models cross-ranking + chairman synthesis) for high-variance, high-stakes critique tasks via OpenRouter. Use when Sean says "convene council", "council critique", "variance check", "premium council", "four-model review", "calibrate voice modes", "stress-test this spec", "council pre-mortem", or surfaces a question where (a) different RLHF biases would produce useful spread, OR (b) different frontier-model blind spots would catch what one model misses. Two profiles available — premium (4 frontier models, ~$0.30–2/query, for stakes/synthesis) and variance (4 mixed-lineage models, ~$0.10–0.80/query, for stylistic/divergence questions). Skip for coding tasks (use Claude Code directly), for research with citations (use gemini-deep-research), for anything skill-optimizer already handles, or for daily ops where single-model Claude is fine. Inspired by Andrej Karpathy's llm-council.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# LLM Council

Multi-vendor LLM critique via OpenRouter, invocable from inside Claude Code sessions. Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council).

See [`decision-table.md`](decision-table.md) for the full routing reference.

---

## 1. When to convene a council

| Question shape | Profile | Why |
|---|---|---|
| Voice spec calibration ("how differently do models read this?") | **variance** | Divergence = signal |
| Cover letter / role-fit memo critique | **premium** | Different vendors, different tone biases |
| Decision pre-mortem ("strongest objection?") | **premium** | Each model has different blind spots |
| PRD / tech-spec stress test | **premium** | Multi-vendor catches holes single-vendor misses |
| Prompt clarity test ("is my SKILL.md unambiguous?") | **variance** | Spread reveals ambiguous instructions |

**Skip council when:**
- Writing or refactoring code (single-model Claude is faster)
- Researching the landscape for X (use `gemini-deep-research`)
- Anything `skill_optimizer` already does (it's structurally a council)
- Daily ops (overkill)

---

## 2. Workflow templates

### 2.1 Voice-mode calibration (variance profile)

Use when Sean wants to check whether the `writing-voice-modes` SKILL.md spec is unambiguous enough that four different frontier models would read it the same way.

**Steps:**

1. Ask Sean for (a) the topic (one sentence) and (b) optionally his own draft (to compare against, not to share with the council).

2. Read the relevant voice-mode spec section from `.claude/skills/writing-voice-modes/SKILL.md` (typically "Sean Mode" unless Sean specifies a different mode).

3. Build the prompt file at `/tmp/llm-council/voice-mode-calibration-<timestamp>.md`:

   ```
   You are critiquing a writing sample written in "<mode name>" — a calibrated voice
   defined in writing-voice-modes SKILL.md.

   [paste the relevant voice-mode spec section verbatim]

   The author wants to know whether the spec is unambiguous enough that four different
   frontier models would read it the same way.

   YOUR TASK: Write a 150-word paragraph on [TOPIC] in <mode name>, following the spec
   exactly. Do not reference any existing sample — write blind from the spec only.
   ```

4. Invoke the CLI:

   ```bash
   cd tools/llm-council && uv run python -m council \
       --profile variance \
       --prompt-file /tmp/llm-council/voice-mode-calibration-<ts>.md \
       --output vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/<YYYY-MM-DD>-<topic-slug>.md \
       --tag voice-mode-calibration
   ```

   Create parent directories first if they don't exist (`mkdir -p ...`).

5. Read the chairman synthesis from the output file. Report back to Sean: where did the four interpretations converge, where did they diverge, what does the chairman think the spec is missing.

6. (Optional, on Sean's request) Draft a diff to `.claude/skills/writing-voice-modes/SKILL.md` based on the divergence findings.

### 2.2 Cover letter / role-fit memo critique (premium profile)

1. Ask Sean for the role context (company, role title, what he's submitting).

2. Write the prompt file:

   ```
   The author is applying for [ROLE TITLE] at [COMPANY], coming from [BACKGROUND].

   Below is their draft. Critique it on:
   1. Specificity (claims that are too generic / could apply to any candidate)
   2. Differentiators that are buried or missing
   3. Tone (confident vs. arrogant vs. hedging)
   4. Concrete edits that would improve it

   Be direct. The author wants the strongest critique, not flattery.

   === DRAFT ===

   [paste full draft]
   ```

3. Invoke the CLI with `--profile premium --tag cover-letter-<company-slug>`.

4. Output to `vault/20_projects/prj-job-hunt-2026/applications/<company>/<YYYY-MM-DD>-council-critique.md`.

### 2.3 Decision pre-mortem (premium profile)

1. Ask Sean to share the decision doc or spec (read it via `Read`).

2. Write the prompt file:

   ```
   The author is about to commit to the following decision/design. Before they pull
   the trigger, surface the strongest objections.

   Each model should independently surface:
   1. The single strongest reason this could fail in production
   2. The most likely "this is fine for v0.1 but will hurt at v1.0" debt
   3. The assumption the author is making that they shouldn't be

   Be ruthless. The author wants pre-mortem, not validation.

   === DECISION/DESIGN ===

   [paste full doc]
   ```

3. Invoke the CLI with `--profile premium --tag premortem-<topic-slug>`.

4. Output to the same directory as the decision doc with `-council-premortem.md` suffix.

### 2.4 PRD / spec stress-test (premium profile)

1. Read the PRD or spec via `Read`.

2. Write the prompt file:

   ```
   Stress-test the following PRD/spec. Each council member should independently surface:
   1. Acceptance criteria that are ambiguous or unmeasurable
   2. Missing edge cases (what happens when X is empty / large / concurrent)
   3. Hidden dependencies (this requires Y to exist first; Y isn't mentioned)
   4. Vocabulary mismatches (the term "user" is used 3 different ways)

   Quote specific lines/sections when possible.

   === PRD/SPEC ===

   [paste full doc]
   ```

3. Invoke the CLI with `--profile premium --tag spec-stress-<topic-slug>`.

4. Output next to the source doc.

---

## 3. Cost discipline

- Every CLI invocation does a pre-flight cap check. If estimated cost > per-query cap, the CLI refuses with a clear error.
- Daily and monthly caps are enforced across BOTH profiles combined.
- The CLI never uses `--force` unless Sean has explicitly authorized it for this query.
- After a successful run, the CLI records actual spend to `vault/health/council-spend-{YYYY-MM-DD}.json`.

If the CLI rejects a query on budget, surface the error verbatim and ask Sean whether to:
1. Wait until tomorrow (daily reset)
2. Use `--force` (per-query bypass, daily/monthly still enforced)
3. Switch to single-model Claude review

---

## 4. Failure modes

- **One model fails in Stage 1** — CLI continues with N-1 survivors; output names the missing model in the cost summary. Surface the partial output to Sean.
- **Two+ models fail in Stage 1** — CLI exits with code 3 and "Council unavailable" message. Recommend falling back to single-model Claude review.
- **Chairman synthesis fails** — CLI exits with partial transcript; Sean still has the four raw drafts + cross-rankings.

---

## 5. Output handling

Council output files are full markdown transcripts: original prompt, four named responses, cross-rank table with reasoning, chairman synthesis, cost summary. They live in the vault sub-project relevant to the task (see workflow templates) for permanent record. Session JSON also written to `tools/llm-council/data/sessions/<session-id>.json` for machine-readable replay.

For voice-mode-calibration specifically, the run-trail is portfolio-worthy: the diff between Sean's draft and the four blind drafts is the calibration signal, accumulating over time.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/llm-council/SKILL.md
git commit -m "feat(skill): llm-council skill with 4 workflow templates + decision table"
```

---

## Task 13: Update `.gitignore` for spend files

**Files:**
- Modify: `.gitignore` (root)

- [ ] **Step 1: Read the current root .gitignore**

```bash
grep -n council /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.gitignore || echo "no council entries yet"
```

- [ ] **Step 2: Append council spend pattern**

Add to the end of `.gitignore`:

```gitignore

# LLM Council spend tracking — private cost data
vault/health/council-spend-*.json
```

- [ ] **Step 3: Verify**

```bash
tail -5 .gitignore
```

Expected: shows the new pattern.

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore llm-council spend tracking files"
```

---

## Task 14: Update CHANGELOG.md

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Determine the next version number**

```bash
grep -E "^## \[" CHANGELOG.md | head -3
```

Read the topmost version; the next one bumps the minor or patch per existing convention. The llm-council integration is a new feature (skill + tool), so use a MINOR version bump from the latest. If CLAUDE.md is at v3.34.0, the next is v3.35.0.

- [ ] **Step 2: Write the new CHANGELOG entry**

Insert AT THE TOP of CHANGELOG.md, BEFORE the existing topmost version:

```markdown
## [3.35.0] - 2026-05-14

### Added

- **LLM Council integration** ([Phase A + B of the 3-phase plan](docs/superpowers/specs/2026-05-14-llm-council-integration-design.md)). New `tools/llm-council/` directory with two artifacts: (a) Karpathy's [llm-council](https://github.com/karpathy/llm-council) cloned unmodified to `tools/llm-council/upstream/` as a reference implementation + visible Karpathy attribution + browser-sidecar fallback (run `cd upstream && ./start.sh`); (b) a new headless Python package `tools/llm-council/council/` implementing the same fan-out → cross-rank → chairman pipeline against OpenRouter, invocable from inside Claude Code sessions. Two configurable profiles — `premium` (four frontier models, judging flat-out, ~$0.30–2/query) and `variance` (four mixed-lineage models, ~$0.10–0.80/query, for divergence-as-signal tasks like voice-mode calibration). Model IDs and per-query / daily / monthly cost caps are pinned in [`tools/llm-council/model-selection-2026-05-14.md`](tools/llm-council/model-selection-2026-05-14.md) (sourced from an OpenRouter inventory at install time). Spend is tracked atomically in `vault/health/council-spend-{YYYY-MM-DD}.json` and `vault/health/council-spend-{YYYY-MM}.json` with the same three-gate pattern as `gemini-deep-research` (per-query hard cap, daily circuit breaker, monthly governor). Pipeline supports degraded mode: 1 of 4 Stage-1 models can fail and the council still produces a valid N-1 output; 2+ failures abort with a clear "fall back to single-model review" message. Cross-rank ranking JSON gets one parse-retry per judge; persistent JSON failures drop that judge from the ranking set without aborting. Phase C (extracting the pipeline as a public MCP server at `seanwinslow28/llm-council-mcp`) is explicitly deferred until 5–10 real runs validate the API surface.
- **`llm-council` skill** at `.claude/skills/llm-council/` with trigger phrases (*"convene council"*, *"council critique"*, *"variance check"*, *"calibrate voice modes"*, *"stress-test this spec"*, etc.) and four workflow templates: voice-mode calibration (Substack pre-launch blocker — diff between Sean's draft and four blind variance-profile drafts is the calibration signal), cover letter / role-fit memo critique (premium), decision pre-mortem (premium), and PRD / spec stress-test (premium). Companion `decision-table.md` documents when to convene a council vs. use single-model Claude vs. delegate to `gemini-deep-research` vs. `last30days` vs. `skill_optimizer`.
- **First end-to-end use case shipped: voice-mode calibration.** Output lands in `vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/<YYYY-MM-DD>-<topic-slug>.md`, building a measurable record of voice-spec calibration over time. Sean re-runs weekly until convergence between blind drafts and his own draft is acceptable, then ships Substack.

### Changed

- Skill count: 118 → 119
- Root `.gitignore` adds `vault/health/council-spend-*.json` (private cost data)
- `CLAUDE.md` architecture comment now lists `tools/` as a new top-level directory alongside `.claude/`, `agents-sdk/`, `vault/`, `claude-mastery/`, `the-block/`, `creative-studio/`, `life-systems/`, etc.

### Credit

Heavy creative + architectural debt to [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council). His three-stage pipeline design (fan-out → anonymized cross-rank → chairman synthesis) is the load-bearing idea; our contribution is the headless CLI + skill wrapper + cost discipline + workflow templates calibrated to Sean's daily use. The original web app remains usable unmodified at `tools/llm-council/upstream/`.
```

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): v3.35.0 — llm-council integration phases A+B"
```

---

## Task 15: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update the skill / architecture counts in the top description**

In `CLAUDE.md`, the line near the top reads:

```
118 skills, 13 Claude Code subagents, 14 hooks, 16 autonomous SDK agents...
```

Update to:

```
119 skills, 13 Claude Code subagents, 14 hooks, 16 autonomous SDK agents...
```

- [ ] **Step 2: Add `tools/` to the Architecture section**

Find the Architecture code block. Locate the section showing `agents-sdk/`, `creative-studio/`, etc. Add a new entry:

```
tools/                                # NEW v3.35.0 — sidecar tools (non-skill, non-agent)
└── llm-council/                      # Multi-vendor LLM council (inspired by karpathy/llm-council)
    ├── upstream/                     # Karpathy's reference web app, unmodified
    └── council/                      # Headless CLI used by .claude/skills/llm-council/
```

- [ ] **Step 3: Add llm-council to the Connected External Research APIs section**

Find the section titled "Connected External Research APIs" (it mentions Gemini Deep Research). Append a new paragraph after the Gemini DR block:

```
**LLM Council** is available via `tools/llm-council/council/` (a headless Python CLI wrapping OpenRouter) and the `.claude/skills/llm-council/` skill. Two profiles — `premium` (4 frontier models) and `variance` (4 mixed-lineage). Cost-disciplined: per-query / daily / monthly gates, spend tracked in `vault/health/council-spend-*.json`. Use for high-variance critique (voice-mode calibration, cover-letter critique, decision pre-mortem, PRD stress-test) where different vendor RLHF biases produce useful spread or independent blind-spot coverage. The original Karpathy web app remains usable at `tools/llm-council/upstream/`. Phase C (separate public MCP server at `seanwinslow28/llm-council-mcp`) is deferred until 5–10 real runs validate the API surface.
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): llm-council skill + tools/ directory + skill count bump"
```

---

## Task 16: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Find the skill count in README**

```bash
grep -n "118 skills" README.md
```

- [ ] **Step 2: Update the count(s)**

Replace every `118 skills` with `119 skills`. If there's a skill table, add a row for `llm-council` with a brief description; check existing skill rows for the format pattern (use the same wording style).

- [ ] **Step 3: (If a skill table exists) Insert row for `llm-council`**

```markdown
| `llm-council` | Multi-vendor LLM council (4 models cross-ranking + chairman synthesis) via OpenRouter. Inspired by [Karpathy](https://github.com/karpathy/llm-council). Premium (frontier-only) and variance (mixed-lineage) profiles. Use for voice-mode calibration, cover-letter critique, decision pre-mortem, PRD stress-test. |
```

Insert in alphabetical order with the other skills.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(readme): llm-council skill + skill count 118 → 119"
```

---

## Task 17: First real voice-mode calibration smoke run

This task validates the whole stack against a real OpenRouter call and produces the first artifact in the voice-mode-calibration run-trail.

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/2026-05-14-<topic-slug>.md`

- [ ] **Step 1: Verify the target directory exists**

```bash
mkdir -p vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs
```

- [ ] **Step 2: Ask Sean for a topic and (optionally) his own draft**

Use `AskUserQuestion` to ask:

> "For the first voice-mode-calibration run, pick a topic for the four models to write a 150-word paragraph on, in Sean Mode (blind from the spec). Optionally share your own draft for comparison after."

Capture Sean's topic. Slugify it for the filename (e.g. "How AI changed my morning routine" → `how-ai-changed-my-morning-routine`).

- [ ] **Step 3: Read the Sean Mode spec**

```bash
grep -A 200 "Sean Mode" .claude/skills/writing-voice-modes/SKILL.md | head -250
```

Capture the Sean Mode definition section verbatim.

- [ ] **Step 4: Build the prompt file**

```bash
mkdir -p /tmp/llm-council
```

Write `/tmp/llm-council/voice-mode-calibration-2026-05-14.md`:

```
You are critiquing a writing sample written in "Sean Mode" — a calibrated voice
defined in writing-voice-modes SKILL.md.

[PASTE Sean Mode spec section verbatim from Step 3]

The author wants to know whether the spec is unambiguous enough that four different
frontier models would read it the same way.

YOUR TASK: Write a 150-word paragraph on [SEAN'S TOPIC from Step 2] in Sean Mode,
following the spec exactly. Do not reference any existing sample — write blind from
the spec only.
```

- [ ] **Step 5: Invoke the CLI**

```bash
cd tools/llm-council
uv run python -m council \
    --profile variance \
    --prompt-file /tmp/llm-council/voice-mode-calibration-2026-05-14.md \
    --output ../../vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/2026-05-14-<topic-slug>.md \
    --tag voice-mode-calibration
```

Expected: CLI runs to completion in <120s. Console shows "Council session written: ..." and approximate cost. The output file exists and contains: original prompt, four named blind drafts, cross-rank table, chairman synthesis.

- [ ] **Step 6: Read the output and report to Sean**

```bash
cat vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/2026-05-14-<topic-slug>.md
```

Surface to Sean:
1. The chairman synthesis verbatim (where models converged, where they diverged, what the spec is missing).
2. The four blind drafts side-by-side (a one-paragraph summary of each is fine; full text is in the file).
3. Recommendation: which sections of `writing-voice-modes/SKILL.md` look load-bearing vs ambiguous based on this run.

- [ ] **Step 7: Verify spend was recorded**

```bash
ls vault/health/council-spend-2026-05-14.json && cat vault/health/council-spend-2026-05-14.json
```

Expected: file exists, `total` reflects the run cost, `runs` array contains one entry tagged `voice-mode-calibration`.

- [ ] **Step 8: Commit the artifact**

```bash
git add vault/20_projects/prj-job-hunt-2026/substack-pre-launch/voice-mode-calibration-runs/2026-05-14-<topic-slug>.md
git commit -m "vault: first voice-mode-calibration run — 2026-05-14"
```

Do NOT commit the spend file — it's gitignored per Task 13.

- [ ] **Step 9: Final verification — full test suite + skill loaded**

```bash
cd tools/llm-council && uv run pytest -v && cd ../..
python3 scripts/validate.py
```

Expected:
- All pytest tests PASS (excluding the e2e test which is INTEGRATION-gated)
- `scripts/validate.py` reports no errors and recognizes the new `llm-council` skill in the skill count

---

## Done

After Task 17, the integration is shipped:
- Phase A: Karpathy's repo cloned at `tools/llm-council/upstream/`, browser app usable via `./start.sh`
- Phase B: Headless CLI + skill working end-to-end against real OpenRouter, with cost discipline, on a real Substack-pre-launch use case
- Phase C: Deferred per spec §8 — re-open after 5–10 real runs

Re-run voice-mode-calibration weekly. After 3 runs land in the run-trail directory, write the small eval script (spec §7) that checks output schema. After 5–10 runs, consider extracting Phase C to a public repo.
