# Daily-Driver Cost Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Route the daily-driver morning run to Sonnet 4.6 and reset its budget cap to a $0.50 tripwire, ending the recurring Opus-driven cap-hits.

**Architecture:** Add a per-mode `model` override to `build_options()` that mirrors the existing per-mode `max_turns` / `max_budget_usd` resolution, then set `model = "sonnet"` and `max_budget_usd = 0.50` in `[agents.daily_driver.modes.morning]`. An absent `model` key resolves to `None` (SDK uses the OAuth default, Opus), so evening/weekly are untouched and rollback is a one-line config delete.

**Tech Stack:** Python 3.13, Claude Agent SDK 0.1.63 (`claude_agent_sdk.ClaudeAgentOptions`), pytest, TOML config.

**Design doc:** [docs/superpowers/specs/2026-06-16-daily-driver-cost-fix-design.md](../specs/2026-06-16-daily-driver-cost-fix-design.md)

---

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `agents-sdk/agents/daily_driver.py` | Resolve per-mode model; surface it in dry-run output | Modify `build_options()` (~L414-473) + dry-run print in `run()` (~L492-505) |
| `agents-sdk/config.toml` | Morning-mode model + cap | Modify `[agents.daily_driver.modes.morning]` (L22-35) |
| `agents-sdk/tests/test_daily_driver_artifacts.py` | Unit-test model resolution | Add two module-level tests |
| `CHANGELOG.md` | Record the behavior/config change | Add one bullet under the top-most version heading |

All paths are relative to repo root `/Users/seanwinslow/Code-Brain/code-brain`.

---

### Task 1: Create a working branch

**Files:** none (git only)

- [ ] **Step 1: Branch off main for the fix**

The current branch is an unrelated fleet-output chore branch. Isolate this work.

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git checkout main && git pull --ff-only
git checkout -b fix/daily-driver-sonnet-cost
```

Expected: on a clean new branch `fix/daily-driver-sonnet-cost`.

---

### Task 2: Add the per-mode model override (TDD)

**Files:**
- Modify: `agents-sdk/agents/daily_driver.py` (`build_options`, ~L414-473)
- Test: `agents-sdk/tests/test_daily_driver_artifacts.py` (append module-level tests)

- [ ] **Step 1: Write the failing test**

Append to the END of `agents-sdk/tests/test_daily_driver_artifacts.py`:

```python
def test_build_options_uses_mode_model_when_set():
    """A per-mode `model` key flows through to ClaudeAgentOptions.model."""
    from lib.config import load_config
    from agents.daily_driver import build_options

    cfg = load_config()
    # Force the value regardless of what config.toml currently holds, so this
    # test pins the resolution logic, not the shipped config.
    cfg.agents.setdefault("daily_driver", {}).setdefault("modes", {}).setdefault(
        "morning", {}
    )["model"] = "sonnet"

    opts = build_options(cfg, mode="morning")
    assert opts.model == "sonnet"


def test_build_options_model_none_when_mode_key_absent():
    """No `model` key ⇒ options.model is None ⇒ SDK keeps the OAuth default (Opus)."""
    from lib.config import load_config
    from agents.daily_driver import build_options

    cfg = load_config()
    # Evening mode carries no model override; strip one if present to be explicit.
    cfg.agents.get("daily_driver", {}).get("modes", {}).get("evening", {}).pop(
        "model", None
    )
    opts = build_options(cfg, mode="evening")
    assert opts.model is None
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py::test_build_options_uses_mode_model_when_set -v
```

Expected: FAIL — `assert None == 'sonnet'` (build_options doesn't pass `model` yet, so the SDK field defaults to `None`).

- [ ] **Step 3: Write the minimal implementation**

In `agents-sdk/agents/daily_driver.py`, inside `build_options`, immediately AFTER the `max_budget` assignment block (the one ending `or config.safety.max_budget_default` near L423), add:

```python
    # Per-mode model override (None ⇒ omit ⇒ SDK uses the OAuth default, Opus).
    # Mirrors the max_turns / max_budget resolution above. Only morning sets it
    # today (→ "sonnet") per the 2026-06-16 cost fix; absent key preserves Opus.
    model = mode_cfg.get("model")
```

Then, in the `return ClaudeAgentOptions(...)` call at the end of the function, add the `model` kwarg right after `max_budget_usd=max_budget,`:

```python
        max_budget_usd=max_budget,
        model=model,
```

- [ ] **Step 4: Run both new tests to verify they pass**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py::test_build_options_uses_mode_model_when_set tests/test_daily_driver_artifacts.py::test_build_options_model_none_when_mode_key_absent -v
```

Expected: 2 passed.

- [ ] **Step 5: Surface the model in dry-run output**

In `agents-sdk/agents/daily_driver.py`, inside `run()`, in the `if dry_run:` block, add a Model line right after `print(f"\nMode: {mode}")`:

```python
        print(f"\nMode: {mode}")
        print(f"Model: {options.model or '(SDK default — Opus)'}")
```

- [ ] **Step 6: Run the full daily-driver test module (no regressions)**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py tests/test_daily_driver_vault_health.py tests/test_daily_driver_job_feed.py -v
```

Expected: all pass (including the two fleet-memory `build_options` tests still green).

- [ ] **Step 7: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add agents-sdk/agents/daily_driver.py agents-sdk/tests/test_daily_driver_artifacts.py
git commit -m "feat(daily-driver): add per-mode model override to build_options"
```

---

### Task 3: Apply the config change (model + cap) and verify wiring

**Files:**
- Modify: `agents-sdk/config.toml` (`[agents.daily_driver.modes.morning]`, L22-35)

- [ ] **Step 1: Replace the morning-mode block**

In `agents-sdk/config.toml`, replace the entire current `[agents.daily_driver.modes.morning]` block (L22-35, the `max_turns = 15` block with the 5/22 + 6/15 comment history and `max_budget_usd = 1.25`) with:

```toml
[agents.daily_driver.modes.morning]
max_turns = 15
# 2026-06-16: routed morning to Sonnet 4.6 (model="sonnet") and reset the budget
# cap 1.25 → 0.50. Root cause of the recurring cap-hits (5/29 $0.97, 6/12 $0.91,
# 6/15 $0.91) was running a TEMPLATED note task on Opus — NOT MCPs or pulled-
# content size (the injected fleet digest is ~200 tokens). The earlier cap bumps
# (0.60→0.90→1.25) chased the creep instead of removing the cause. Sonnet does
# this task for ~$0.15-0.20/run (~5x cheaper), so the cap now sits as a TRIPWIRE:
# ~2.7x over expected Sonnet cost, still below the ~$0.88 Opus floor — an
# accidental revert to Opus trips the cap loudly instead of billing silently.
# Worst-case month: ~$15 (was ~$37.50 on Opus). Rollback: delete the model line
# (→ Opus default) and/or restore 1.25. Design:
# docs/superpowers/specs/2026-06-16-daily-driver-cost-fix-design.md
model = "sonnet"
max_budget_usd = 0.50
```

Leave the `[agents.daily_driver.modes.evening]` and `[...weekly]` blocks unchanged.

- [ ] **Step 2: Verify the wiring via dry-run (free, zero side-effects)**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run | head -8
```

Expected output includes:
```
Mode: morning
Model: sonnet
Max turns: 15
Max budget: $0.5
```

- [ ] **Step 3: Confirm the shipped config resolves Sonnet through build_options**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
from lib.config import load_config
from agents.daily_driver import build_options
o = build_options(load_config(), mode='morning')
print('model=', o.model, 'budget=', o.max_budget_usd)
assert o.model == 'sonnet' and o.max_budget_usd == 0.5
print('OK')
"
```

Expected: `model= sonnet budget= 0.5` then `OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add agents-sdk/config.toml
git commit -m "fix(daily-driver): route morning to Sonnet, reset cap to \$0.50 tripwire"
```

---

### Task 4: CHANGELOG entry

**Files:**
- Modify: `CHANGELOG.md` (top-most version/Unreleased heading)

- [ ] **Step 1: Add the changelog bullet**

Open `CHANGELOG.md`, find the top-most version or `## [Unreleased]` heading, and add this bullet under it (match the surrounding bullet style):

```markdown
- **fix(daily-driver):** Morning run routed to Sonnet 4.6 via a new per-mode `model`
  override in `build_options`; budget cap reset $1.25 → $0.50 as a regression
  tripwire. Root cause of the 5/29–6/15 cap-hits was a templated note task running
  on Opus (~$0.88/run), not MCPs. Expected ~$0.15–0.20/run. Rollback is config-only.
  Spec: `docs/superpowers/specs/2026-06-16-daily-driver-cost-fix-design.md`.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add CHANGELOG.md
git commit -m "docs(changelog): daily-driver Sonnet swap + cap tripwire"
```

---

### Task 5: Post-deploy verification (next scheduled run)

**Files:** none (observation only — no manual live run today, to avoid a second idempotent portfolio commit)

- [ ] **Step 1: After tomorrow's 08:45 run, check the recorded cost + status**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
grep "$(date -v+1d +%F),0" vault/90_system/agent-logs/agent-run-history.csv | grep daily-driver | grep morning
```

(Or simply `grep daily-driver vault/90_system/agent-logs/agent-run-history.csv | grep morning | tail -1` the next day.)

Expected: status `success`, `cost_usd` ~$0.15–0.20 (vs the 6/16 Opus row at $0.8847), no `error_max_budget_usd`.

- [ ] **Step 2: Eyeball tomorrow's daily note for output quality**

Open `vault/10_timeline/daily/<tomorrow>.md` and confirm:
- a valid 1-3-5 plan is present in the Morning Focus section, and
- the fleet digest is injected verbatim at the `<!-- fleet-overnight -->` anchor.

If cost is good and quality holds, the fix is verified. If quality regresses, roll back per the design doc (delete the `model` line → Opus) and reopen the trim discussion.

---

## Self-Review

**Spec coverage:**
- Change 1 (per-mode model override) → Task 2 ✓
- Change 2 (config: model=sonnet, cap=0.50, comment) → Task 3 ✓
- Verification (dry-run + tomorrow's scheduled run) → Task 3 Step 2-3 + Task 5 ✓
- Rollback (config-only) → documented in config comment (Task 3 Step 1) + Task 5 Step 2 ✓
- Doc updates (CHANGELOG) → Task 4 ✓
- Out-of-scope items (preamble trim, etc.) → not implemented, correctly absent ✓

**Placeholder scan:** No TBD/TODO/"handle edge cases"; every code step shows exact code. ✓

**Type/name consistency:** `model` variable in `build_options` matches the `model=` kwarg and `options.model` assertions; `mode_cfg.get("model")` matches the config key `model = "sonnet"`. The dry-run prints `options.model`. All consistent. ✓

**One implementation guardrail (from the spec):** `ClaudeAgentOptions` exposes a `model` field (verified in SDK 0.1.63) and passing `None` is its default — so the absent-key path is inert. If a future SDK bump rejects `model=None`, guard with a conditional kwarg dict, but that is not needed today.
