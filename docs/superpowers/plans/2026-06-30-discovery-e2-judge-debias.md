# E2 — Judge-Family Debias Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the FUSE panel self-preference confound by making the judge's model family disjoint from its panel in every tier.

**Architecture:** `tiers.py`-only config change enforced by one invariant — *judge family ∉ panel families*. standard/deep keep the Opus judge and drop Opus from the panel; quick keeps its 3-model panel and swaps the judge from Gemini to GPT. A private `_family()` helper defines "family," and a hermetic regression test locks the invariant. No `openrouter:fusion` change, no order-randomization, no live API calls.

**Tech Stack:** Python 3.10+, pytest, `uv`. Files under `tools/llm-council/`.

**Spec:** [`docs/superpowers/specs/2026-06-30-discovery-e2-judge-debias-design.md`](../specs/2026-06-30-discovery-e2-judge-debias-design.md)
**Research:** [`vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md`](../../../vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md)

## Global Constraints

- **Run tests with `uv`:** `cd tools/llm-council && uv run pytest tests/ -q` (baseline: 263 passed, 1 skipped). Repo-root validator: `python3 scripts/validate.py`.
- **No live API calls in tests** — assert on config only; never call `fuse()`.
- **Model IDs must stay within the FUSION_SCHEMA-validated set** exactly: `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, `mistralai/mistral-medium-3-5`. Never reintroduce the invalid `google/gemini-pro-latest` (no tilde) or dotted `mistralai/mistral-medium-3.5`.
- **family(model_id)** = strip a single leading `~`, then take the segment before the first `/`.
- **Zero vault changes on this branch.** Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

### Task 1: Debias the tier configs + lock the invariant

**Files:**
- Modify: `tools/llm-council/council/discovery/tiers.py` (add `_family()`; edit `_STANDARD_PANEL`, the `quick` judge)
- Test: `tools/llm-council/tests/discovery/test_tiers.py`

**Interfaces:**
- Produces: `_family(model_id: str) -> str` (private helper in `tiers.py`, imported by tests). `TIERS` / `get_tier()` signatures unchanged; only `.panel` and `.judge` values change.

- [ ] **Step 1: Write the failing tests**

Add to `tools/llm-council/tests/discovery/test_tiers.py` (update the import line to include `_family`):

```python
from council.discovery.tiers import get_tier, TIERS, _family

# IDs validated against the live OpenRouter API (FUSION_SCHEMA.md §2). Panel + judge
# must never drift outside this set (guards against a 400 from a typo'd/aliased id).
_VALIDATED_IDS = {
    "anthropic/claude-opus-4.7",
    "openai/gpt-5.5",
    "~google/gemini-pro-latest",
    "x-ai/grok-4.3",
    "deepseek/deepseek-v4-pro",
    "mistralai/mistral-medium-3-5",
}


def test_family_strips_tilde_and_splits_on_slash():
    assert _family("~google/gemini-pro-latest") == "google"
    assert _family("anthropic/claude-opus-4.7") == "anthropic"
    assert _family("openai/gpt-5.5") == "openai"
    assert _family("mistralai/mistral-medium-3-5") == "mistralai"


def test_judge_family_is_disjoint_from_panel_every_tier():
    # E2 invariant: the judge must not share a model family with any panelist
    # (self-preference / self-enhancement bias — see the E2 research note).
    for name in TIERS:
        t = get_tier(name)
        panel_families = {_family(m) for m in t.panel}
        assert _family(t.judge) not in panel_families, (
            f"{name}: judge {t.judge} shares family with panel {t.panel}"
        )


def test_all_panel_and_judge_ids_are_validated():
    for name in TIERS:
        t = get_tier(name)
        for m in (*t.panel, t.judge):
            assert m in _VALIDATED_IDS, f"{name}: unvalidated model id {m!r}"


def test_quick_judge_swapped_to_disjoint_family():
    t = get_tier("quick")
    assert t.judge == "openai/gpt-5.5"
    assert t.panel == (
        "~google/gemini-pro-latest",
        "x-ai/grok-4.3",
        "deepseek/deepseek-v4-pro",
    )


def test_deep_panel_excludes_anthropic_keeps_two_extra_lineages():
    t = get_tier("deep")
    assert "anthropic/claude-opus-4.7" not in t.panel
    assert "deepseek/deepseek-v4-pro" in t.panel
    assert "mistralai/mistral-medium-3-5" in t.panel
    assert t.judge == "anthropic/claude-opus-4.7"
```

Then REPLACE the existing `test_standard_panel_is_four_frontier_vendors` (it encodes the
pre-E2 confounded panel) with the post-E2 version:

```python
def test_standard_panel_is_anthropic_free_with_opus_judge():
    t = get_tier("standard")
    assert t.panel == (
        "openai/gpt-5.5",
        "~google/gemini-pro-latest",
        "x-ai/grok-4.3",
    )
    assert t.judge == "anthropic/claude-opus-4.7"
    assert "anthropic/claude-opus-4.7" not in t.panel
    assert t.max_cost_per_run == 1.50
```

Leave `test_deep_adds_two_more_lineages_and_confirms_cost`, `test_sonar_never_in_panel`,
`test_three_tiers_exist`, `test_unknown_tier_raises`, `test_collector_tier_gating_matches_matrix`,
and `test_supplement_blind_spot_caps_scale_by_tier` unchanged.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_tiers.py -q`
Expected: FAIL — `ImportError`/`cannot import name '_family'` (helper not defined yet), and the new
membership/invariant tests fail because the judge is still a panelist in all three tiers.

- [ ] **Step 3: Add the `_family()` helper to `tiers.py`**

Insert above the `@dataclass` (after the imports):

```python
def _family(model_id: str) -> str:
    """OpenRouter model family: the segment before the first '/', minus a leading '~'
    floating-alias marker. E2 keeps each tier's judge family disjoint from its panel
    (self-preference debias — see the E2 research note)."""
    return model_id.removeprefix("~").split("/", 1)[0]
```

- [ ] **Step 4: Edit `_STANDARD_PANEL` — drop the Opus panelist**

Change:

```python
_STANDARD_PANEL = (
    "anthropic/claude-opus-4.7",
    "openai/gpt-5.5",
    "~google/gemini-pro-latest",
    "x-ai/grok-4.3",
)
```

to:

```python
# E2: Opus is the standard/deep JUDGE, so it is intentionally NOT a panelist
# (judge family must be disjoint from the panel — self-preference debias).
_STANDARD_PANEL = (
    "openai/gpt-5.5",
    "~google/gemini-pro-latest",
    "x-ai/grok-4.3",
)
```

(`deep` builds on `_STANDARD_PANEL + ("deepseek/deepseek-v4-pro", "mistralai/mistral-medium-3-5")`,
so it automatically becomes a 5-vendor anthropic-free panel. `standard.judge` and `deep.judge` stay
`"anthropic/claude-opus-4.7"` — no change there.)

- [ ] **Step 5: Swap the `quick` judge to a disjoint family**

In the `"quick"` `TierConfig`, change `judge="~google/gemini-pro-latest"` to:

```python
        judge="openai/gpt-5.5",   # E2: disjoint from quick panel {google, x-ai, deepseek}
```

Leave the quick `panel=("~google/gemini-pro-latest", "x-ai/grok-4.3", "deepseek/deepseek-v4-pro")` unchanged.

- [ ] **Step 6: Run the tier tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_tiers.py -q`
Expected: PASS (all tier tests green).

- [ ] **Step 7: Run the full discovery + fusion suite to catch any hardcoded-panel assumptions**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_fusion.py tests/discovery/test_panel_vs_single_core.py tests/discovery/test_panel_vs_single_cli.py -q`
Expected: PASS. If any test hardcoded the 4-model standard panel or the gemini quick judge, fix that
test to the new config (it was encoding the old design) — do NOT change `tiers.py` back.

- [ ] **Step 8: Run the entire suite + validator**

Run: `cd tools/llm-council && uv run pytest tests/ -q` (expect 263+ passed, 1 skipped — count rises by the new tests) and `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py` (expect PASS).

- [ ] **Step 9: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add tools/llm-council/council/discovery/tiers.py tools/llm-council/tests/discovery/test_tiers.py
git commit -m "feat(discovery): E2 judge-family debias — judge disjoint from panel every tier

quick judge gemini->gpt-5.5 (panel unchanged); standard/deep drop the Opus
panelist (Opus stays the judge). New _family() helper + an invariant test that
permanently blocks reintroducing the self-preference confound.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Update SKILL.md + CHANGELOG

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§2 FUSE description, line ~58)
- Modify: `CHANGELOG.md` (top of `[Unreleased]`)

- [ ] **Step 1: Update the FUSE stage description in SKILL.md**

In `.claude/skills/fusion-discovery-council/SKILL.md`, the §2 FUSE bullet currently reads
"Run the gathered evidence through an OpenRouter **Fusion panel** (Opus / GPT / Gemini / Grok at
standard tier) plus an outer **judge** model." Replace the parenthetical + add the invariant so it
reflects E2 (Opus is now the judge, not a panelist):

Old:
```
2. **FUSE** — Run the gathered evidence through an OpenRouter **Fusion panel** (Opus / GPT / Gemini / Grok at standard tier) plus an outer **judge** model. The panel reads the evidence and proposes candidate pain points; the judge consolidates and de-duplicates them.
```
New:
```
2. **FUSE** — Run the gathered evidence through an OpenRouter **Fusion panel** (GPT / Gemini / Grok at standard tier) plus an outer **judge** model (Opus at standard/deep, GPT at quick). The panel reads the evidence and proposes candidate pain points; the judge consolidates and de-duplicates them. **E2 invariant:** the judge's model family is deliberately disjoint from every panelist's, so no model grades its own family's output (self-preference debias — see [the E2 research note](../../../vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md)).
```

- [ ] **Step 2: Add a CHANGELOG entry**

In `CHANGELOG.md`, immediately under `## [Unreleased]` (above the D2 entry), add:

```markdown
### fusion-discovery-council E2 — judge-family debias (2026-06-30)
- **fusion-discovery-council E2 — panel self-preference fix.** The FUSE judge was a literal
  member of its own panel in every tier (the confound the Step-C gate flagged). E2 enforces one
  invariant — *judge model family ∉ panel families* — in `tiers.py`: `quick` judge swaps
  Gemini→GPT (panel unchanged); `standard`/`deep` drop the Opus panelist (Opus stays the judge,
  panels become anthropic-free 3-/5-vendor sets). A `_family()` helper + a regression test lock
  the invariant. `tiers.py`-only, $0, no live calls; the `openrouter:fusion` path is untouched.
  Research ($0 deep-research): family separation is the highest-leverage debias lever and the
  only one robust to both mechanism accounts; the full order-randomized pipeline was rejected
  (wrong task shape for a synthesis judge; order-swap can backfire). Decision record:
  `vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md`.
```

- [ ] **Step 3: Verify validator still passes**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md
git commit -m "docs(discovery): E2 judge-family debias — SKILL.md FUSE invariant + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:** invariant (Task 1 Step 1 `test_judge_family_is_disjoint...`); per-tier config (Steps 4–5 + membership tests); `_family()` helper (Step 3 + unit test); validated-ID guard (`test_all_panel_and_judge_ids_are_validated`); updated old test (Step 1 replacement); SKILL.md + CHANGELOG (Task 2); non-goals are no-ops (nothing touches `fusion.py`/order/blinding) — covered. quick judge = `gpt-5.5` locked per spec.

**Placeholder scan:** none — every step has exact code/commands.

**Type consistency:** `_family(model_id: str) -> str` defined once (Task 1 Step 3), imported in tests and referenced consistently; `.panel`/`.judge` are existing `TierConfig` fields, unchanged in type.

**Final whole-branch adversarial review** (Code Reviewer agent, most-capable model) against the branch diff before opening the PR, per conventions.
