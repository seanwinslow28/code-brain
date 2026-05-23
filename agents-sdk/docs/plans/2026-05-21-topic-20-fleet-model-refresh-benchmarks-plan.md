---
type: implementation-plan
project: agents-sdk-fleet
artifact: topic-20-fleet-model-refresh
created: 2026-05-21
status: drafted-awaiting-implementation
companion_artifacts:
  - ../../../vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md
  - ../../../vault/20_projects/research/2026-05-21-topic-16-pi-ollama-integration-chatgpt-manual.md
  - ../../config.toml
  - ../../BUGFIX-2026-04-07-launchd-path.md
  - ../../AUDIT-2026-04-28-process-inbox-reenable.md
sprint_epoch: 2026-05-04
deliverables:
  - vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md
  - agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md
  - agents-sdk/scripts/benchmark_ollama_model.py
  - agents-sdk/scripts/wake_alienware.py
  - agents-sdk/scripts/sleep_alienware.py
  - agents-sdk/lib/benchmark_scorers.py
  - agents-sdk/lib/wol.py
ai-context: "Implementation plan for Topic 20 — pulls and benchmarks 6 candidate Ollama models across Sean's 3-tier hardware fleet (M4 Max MBP / M4 Pro Mac Mini 24GB / RTX 4090 Alienware) against the Topic 19 synthesis baselines, AND stands up an on-demand wake-on-LAN architecture so the Alienware can serve as a third Ollama host without being powered on 24/7. Born 2026-05-21 from the §Correction addendum at the bottom of the Topic 19 synthesis (file linked above), which exposed a methodology bias against newer locally-runnable models. Outputs: per-tier benchmark scorecard, per-agent adoption recommendation, WoL decision record, and either a config.toml routing update or an explicit no-migrate decision with evidence. Cost ceiling: $0 incremental (everything is local inference). Soak gate to mark shipped-and-verified: 1 week of stable production load on any newly-adopted model with zero quality regressions on the agents using it."
---

# Topic 20 — Fleet Model Refresh + Alienware WoL Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Future Sean / future Claude:** check the **Status Tracker** at the bottom before starting work. The synthesis context is in [`../../../vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md`](../../../vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md) — specifically the §Correction (2026-05-21) section at the bottom. This plan is the implementation contract.

**Goal:** Land an evidence-based per-tier adoption decision for six candidate Ollama models (`qwen3.5:9b`, `qwen3.5:27b`, `qwen3.5:35b`, `qwen3.6:35b`, `nemotron3:33b`, `gemma4:26b-MoE`) benchmarked against the current production fleet models (`Qwen3-14B` on MBP, `gemma4:e4b` on Mac Mini) and the Topic 19 baselines (`qwen3-coder:30b`, `devstral:24b-small-2505`), while standing up the Alienware as the fleet's first wake-on-demand Tier C host.

**Architecture:** Pure-Python benchmark harness (no Claude Agent SDK in the benchmark loop — Ollama HTTP `/api/chat` is the system under test) that drives a fixed-prompt evaluation suite across all three hardware tiers, captures raw JSONL per model, and aggregates into a single synthesis report. WoL plumbing is on-demand magic-packet (Pattern A) sent from the always-on Mac Mini before each Alienware-bound benchmark batch, with Pattern B (scheduled wake windows) documented as the fallback if Pattern A's wake-success rate drops below 95% in soak.

**Tech Stack:** Python 3.13 (`agents-sdk/.venv`), `requests` for Ollama HTTP, `psutil` for memory sampling on macOS, `socket` for raw UDP magic packets, `subprocess` for `ollama pull`/`ollama show`/`ollama create`, `pytest` for harness tests. Ollama runtime ≥ 0.4.5 on all hosts. No new third-party Python dependencies beyond what already ships in `agents-sdk/.venv` — verify in Task 1.0.

---

## Scope guard — what this plan does NOT do

These are explicit non-goals. If a task starts drifting toward any of them, stop and either log it as deferred work in the Status Tracker or break it into a separate plan.

| Non-goal | Why deferred |
|---|---|
| Migrating any production agent's routing before the benchmark report lands | The Topic 19 §Correction explicitly says "do not migrate any production agent away from `qwen3-coder:30b` / `devstral:24b-small-2505-q4_K_M` based on this addendum alone." This plan reaffirms that — adoption only happens in Phase 6, after Phase 5 evidence is captured. |
| Cloud-model regression benchmarks (Sonnet, Opus, GPT-5.5) | Local-vs-local only. Cloud comparison is Topic 12's job. |
| Embeddings model swap (`nomic-embed-text` → alternative) | Out of scope — Topic 19 was chat-completion models only. Reuse the embeddings model. |
| Fine-tuning or custom-quantizing any candidate | Use upstream Ollama tags as published. If `nemotron3:33b` needs a smaller quant to fit in 24GB VRAM, the plan downgrades to either CPU offload (acceptable on Tier C) or rejects the model — does not produce custom quants. |
| Mid-2026 hardware refresh (M5, Blackwell) | Re-run this plan in Q3 2026 if hardware changes. |
| Reactivating `process_inbox` Path B on `gemma4:e4b` | Out of scope — that work is tracked in `AUDIT-2026-04-28-process-inbox-reenable.md`. If `gemma4:26b-MoE` wins Tier B, it MIGHT inform Path B's eventual model choice, but the Path B rewrite itself is a separate plan. |
| Replacing Obsidian-Git auto-commit with anything | Vault sync ownership stays with `.claude/hooks/session-end-auto-commit.sh` per CLAUDE.md Rule 8 / Issue #22. Benchmark result files are committed via that existing path, not a new one. |
| Wake-on-WAN (router-side WAN-wake via Deco admin UI) | Security concern flagged in Sean's intake — out of scope. LAN magic packets only. |
| Multi-region / multi-LAN benchmarking | Single LAN (TP-Link Deco BE Pro). Tailscale path is documented as a Tier-B alternative for the existing Mac Mini → MBP route but not benchmarked here. |
| Auto-routing the new Substack-Drafter agent to a new model | Substack-Drafter is `default disabled` per CLAUDE.md. If a new model wins Tier A, the Substack config note gets a comment but no enable. |

---

## Hardware budget cross-check (read before any pull)

| Tier | Hardware | Usable budget | Candidates | Fit |
|---|---|---|---|---|
| **A** | M4 Max MBP (unified memory **TBC in Task 0.2** — assume 64GB; if 36GB downgrade Tier A candidates) | ~48GB usable for LM after OS + IDE + browser | `qwen3.5:27b` (17GB) ✓ / `qwen3.5:35b` (24GB) ✓ / `qwen3.6:35b` (24GB) ✓ / `qwen3-coder:30b` (~18GB) ✓ | All fit on assumed 64GB; on 36GB the 35B candidates compete for headroom — re-evaluate in Task 0.2. |
| **B** | M4 Pro Mac Mini 24GB unified | ~17GB usable (leaves 7GB for headless OS + Ollama serve overhead + KV cache) | `qwen3.5:9b` (6.6GB) ✓ / `gemma4:26b-MoE` (18GB) — **tight** / `qwen3.5:27b` (17GB) — **tight** / `gemma4:e4b` (~4GB) ✓ baseline | `qwen3.5:9b` is the comfortable Tier-B pick; `gemma4:26b-MoE` and `qwen3.5:27b` will be benchmarked with reduced `num_ctx` to keep KV cache inside budget. |
| **C** | RTX 4090 24GB VRAM | ~22GB VRAM usable (leaves 2GB for CUDA overhead + display) | `devstral:24b-small-2505-q4_K_M` (~14GB) ✓ / `nemotron3:33b` (28GB) — **does NOT fit pure-GPU**; needs CPU offload or smaller quant | `nemotron3:33b` at advertised 28GB is too large for 24GB VRAM. Plan strategy: pull the default tag, observe Ollama's auto-CPU-offload behavior, accept slower tok/s as the price of the test. If a Q4_K_S or Q3_K_M variant ships, prefer it. |

**Disk budget per machine** (estimate ~30GB headroom needed for the pull batch):

- **MBP**: ~75GB needed (qwen3.5:27b 17GB + qwen3.5:35b 24GB + qwen3.6:35b 24GB + qwen3-coder:30b 18GB baseline). Verify in Task 0.4.
- **Mac Mini**: ~32GB (qwen3.5:9b 6.6GB + qwen3.5:27b 17GB + gemma4:26b-MoE 18GB — assume the baseline `gemma4:e4b` already present is the 4GB tag). Verify in Task 0.4.
- **Alienware**: ~45GB (nemotron3:33b 28GB + devstral 14GB). Verify in Task 0.4.

---

## File map

Each file has one clear responsibility. Files that change together live together.

**New code files:**

```
agents-sdk/lib/benchmark_scorers.py            # Pure scoring fns (JSON validity, tok/s, recall, etc.)
agents-sdk/lib/wol.py                          # Magic packet construction + readiness probe
agents-sdk/scripts/benchmark_ollama_model.py   # Main benchmark runner CLI
agents-sdk/scripts/wake_alienware.py           # Send WoL + wait until ollama is responsive
agents-sdk/scripts/sleep_alienware.py          # Trigger remote sleep gracefully
agents-sdk/tests/test_benchmark_scorers.py
agents-sdk/tests/test_wol.py
```

**New fixture / data files:**

```
agents-sdk/benchmarks/topic_20/prompts/tool_calls.jsonl       # 20 prompts × 4 tool schemas
agents-sdk/benchmarks/topic_20/prompts/agentic_loops.jsonl    # 10 multi-step Pi-style loops
agents-sdk/benchmarks/topic_20/prompts/needle_haystack.py     # 32K-token generator (writes prompts on demand)
agents-sdk/benchmarks/topic_20/results/.gitkeep               # raw JSONL drops land here
agents-sdk/benchmarks/topic_20/README.md                      # How to run + interpret
```

**New doc files:**

```
agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md   # Decision record matching local-tts-decision-record.md style
vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md   # Final synthesis report
```

**Potentially modified files (gated by Phase 6 decision):**

```
agents-sdk/config.toml                                          # Only if Phase 5 produces a winner per tier
CLAUDE.md                                                       # Agent inventory table update if routing changes
CHANGELOG.md                                                    # Entry per CLAUDE.md "When Modifying" rule
agents-sdk/schedules/com.sean.agent.<new>.plist                 # Only if a new launchd schedule is needed (e.g., Alienware wake-before-batch)
```

**Files NOT touched:**

```
.claude/hooks/session-end-auto-commit.sh    # Vault sync ownership — Issue #22 / CLAUDE.md Rule 8
.claude/settings.json                        # No permission / hook changes needed
vault/.vault-index.db                        # No schema changes
agents-sdk/agents/*.py                       # No agent-runtime changes in this plan; adoption is a config-only edit
```

---

## Phase 0 — Pre-flight clarifications and verification

### Task 0.1: Confirm Alienware OS, current Ollama state, and BIOS/UEFI WoL setting (manual, ~10 min, requires Sean)

**Why this is Task 0.1:** The Topic 20 plan has been built assuming the Alienware runs Ollama at `192.168.68.201:11434` per `[routing.machines.alienware]` in `config.toml:268-275`. The exact OS, the current sleep/idle state, and whether WoL is enabled in BIOS/UEFI are all undocumented in the repo. Until these three answers are known, the WoL phase cannot be sequenced correctly.

**Files:** None (manual investigation).

- [ ] **Step 1: Ask Sean three questions and capture answers inline in this plan's Status Tracker**

  1. What OS is currently installed on the Alienware? (Windows 11 / Linux / dual-boot / other)
  2. What's the current power state behavior — does it sleep after idle, hibernate, or stay on?
  3. Has WoL ever been enabled in BIOS/UEFI on this machine? (If yes, skip Task 2.1.1; if no/unknown, Task 2.1.1 needs to run at the machine.)

- [ ] **Step 2: Verify Ollama is installed on the Alienware**

  - If Windows: open PowerShell, run `ollama --version`. Expected: a semver ≥ 0.4.5. If "not recognized," install from `https://ollama.com/download/windows`.
  - If Linux: SSH (or local terminal) and run `ollama --version`. Install via `curl -fsSL https://ollama.com/install.sh | sh` if missing.
  - Record the version string in the Status Tracker.

- [ ] **Step 3: Capture the current Ollama model list on Alienware**

  Run: `ollama list` on the Alienware. Capture output. Expected per `config.toml:275` — `Qwen3-VL-7B` model. If absent or different, log discrepancy.

- [ ] **Step 4: Document outcomes in Status Tracker** (no commit yet — Task 0.1 is investigation only)

### Task 0.2: Confirm M4 Max MBP unified memory size

**Files:** None.

- [ ] **Step 1: On the MBP run `system_profiler SPHardwareDataType | grep "Memory"` and capture output**

  Expected something like `Memory: 64 GB` or `36 GB`. Record in Status Tracker.

- [ ] **Step 2: If memory < 48GB, mark the 35B candidates (`qwen3.5:35b`, `qwen3.6:35b`) as "skip on Tier A, retry on Tier C only"**

  Rationale: 35B FP16-rough at ~24GB plus KV cache + IDE + browser exceeds a 36GB unified-memory budget under typical interactive load. The 27B candidate stays.

### Task 0.3: Verify network topology and MAC addresses

**Files:** None.

- [ ] **Step 1: From Mac Mini, ping each host on the LAN**

  ```bash
  ping -c 3 192.168.68.50    # MBP
  ping -c 3 192.168.68.201   # Alienware (must be powered on or via WoL response)
  ```

  Record results. If Alienware is currently off, this verifies AFTER Task 2.1 — leave as gated.

- [ ] **Step 2: Confirm Alienware MAC address matches `config.toml:274` (`B4:E9:B8:F7:71:47`)**

  - On the Alienware (when powered on): Windows `getmac /v` or Linux `ip link show`.
  - Compare to the value in `config.toml:274`. If they differ, the `wol_mac` config block is stale — update it as part of Task 2.2.

- [ ] **Step 3: Verify the Deco BE Pro router does not block broadcast UDP on port 9** (default WoL port)

  - Open Deco mobile app → More → Advanced → check whether "AP Isolation" or "Client Isolation" is on. If on, magic packets won't propagate across the LAN — disable for the wired backbone segment that hosts both the Mac Mini and the Alienware.
  - Record finding in Status Tracker. (Most Deco setups have this off by default.)

### Task 0.4: Verify disk space on each host

**Files:** None.

- [ ] **Step 1: MBP — `df -h ~ | tail -1`**

  Need ≥80GB free for the candidate pulls. Record. If < 80GB, identify what to clear or downscope to fewer candidates per tier.

- [ ] **Step 2: Mac Mini — same command**

  Need ≥40GB free. Record.

- [ ] **Step 3: Alienware — Windows: `Get-PSDrive C` (PowerShell); Linux: `df -h /`**

  Need ≥50GB free. Record.

### Task 0.5: Verify `agents-sdk/.venv` has the dependencies the harness needs

**Files:** None (read-only check).

- [ ] **Step 1: Run from `agents-sdk/`**

  ```bash
  .venv/bin/python3 -c "import requests, psutil, pytest; print('ok')"
  ```

  Expected: `ok` printed. If any import fails, install with `.venv/bin/pip install requests psutil pytest` (these should already be present from prior agent work — confirm in `pyproject.toml`).

### Task 0.6: Confirm Ollama is reachable on the Mac Mini and MBP

**Files:** None.

- [ ] **Step 1: From any machine on the LAN, hit the Mac Mini's Ollama tags endpoint**

  ```bash
  curl -s http://192.168.68.200:11434/api/tags | head -c 200
  ```

  Expected: JSON response listing existing models including `gemma4:e4b`, `nomic-embed-text`, and `qwen3-14b-research`. If timeout, the Mac Mini's Ollama isn't bound to 0.0.0.0 — `launchctl setenv OLLAMA_HOST 0.0.0.0` plus a restart fixes per Topic 16 §2.

- [ ] **Step 2: From the Mac Mini, hit the MBP's LM Studio endpoint (verifies MBP-currently-awake state)**

  ```bash
  curl -s --max-time 3 http://192.168.68.50:1234/v1/models | head -c 200
  ```

  Expected: JSON listing `qwen3-14b` (or 500 / timeout if MBP is asleep). Either is fine — just record the state so Phase 4 knows when MBP is reachable.

---

## Phase 1 — Benchmark harness construction (TDD)

This phase builds the reusable benchmark CLI before any model is pulled. The harness is the system the rest of the plan depends on. Build it with tests first.

### Task 1.1: Create the topic_20 benchmark scaffold

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/README.md`
- Create: `agents-sdk/benchmarks/topic_20/prompts/` (directory)
- Create: `agents-sdk/benchmarks/topic_20/results/.gitkeep`

- [ ] **Step 1: Create the directory structure**

  ```bash
  mkdir -p agents-sdk/benchmarks/topic_20/prompts
  mkdir -p agents-sdk/benchmarks/topic_20/results
  touch agents-sdk/benchmarks/topic_20/results/.gitkeep
  ```

- [ ] **Step 2: Write the README**

  Content of `agents-sdk/benchmarks/topic_20/README.md`:

  ```markdown
  # Topic 20 — Fleet Model Refresh Benchmarks

  Reusable benchmark harness for evaluating candidate Ollama models against
  the current production fleet. Driven by `agents-sdk/scripts/benchmark_ollama_model.py`.

  ## Run a single model

      cd agents-sdk
      PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
          --model qwen3.5:27b \
          --host http://192.168.68.200:11434 \
          --tier B \
          --out benchmarks/topic_20/results/

  ## Prompts

  - `prompts/tool_calls.jsonl` — 20 single-turn tool-call prompts, 4 schemas.
  - `prompts/agentic_loops.jsonl` — 10 multi-step "Pi-style" sessions.
  - `prompts/needle_haystack.py` — generates a 32K-token prompt with a needle
    at the 28K mark; produces a new haystack each call so models can't memorize.

  ## Dimensions captured per (model, tier) pair

  1. Tool-call JSON validity (% pass)
  2. Decode tok/s on a fixed 1024-token output (mean ± stddev, 3 runs)
  3. Peak memory footprint during a 5-iter Pi-style session
  4. Agentic-loop reliability (successful completions / 10)
  5. Long-context recall at 28K (5 runs)
  6. Pi-specific gotcha checks (5 binary tests)

  ## Output

  Raw results land at `results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl`.
  Each line is one prompt's full record. Aggregation lives in the synthesis
  report at `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`.
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/benchmarks/topic_20/
  git commit -m "feat(benchmarks): scaffold topic_20 fleet refresh harness"
  ```

### Task 1.2: Write failing tests for `benchmark_scorers.py`

**Files:**
- Create: `agents-sdk/tests/test_benchmark_scorers.py`

- [ ] **Step 1: Write the failing test file**

  ```python
  # agents-sdk/tests/test_benchmark_scorers.py
  """Tests for lib/benchmark_scorers.py."""
  import pytest
  from lib.benchmark_scorers import (
      score_tool_call_json,
      compute_tokens_per_second,
      score_needle_recall,
      score_pi_gotcha_compat,
  )


  def test_valid_tool_call_passes():
      output = '{"name": "read_file", "arguments": {"path": "/etc/hosts"}}'
      schema = {"name": "read_file", "required": ["path"]}
      result = score_tool_call_json(output, schema)
      assert result["valid"] is True
      assert result["schema_match"] is True


  def test_malformed_json_fails():
      output = '{"name": "read_file", "arguments": {path: "/x"'
      schema = {"name": "read_file", "required": ["path"]}
      result = score_tool_call_json(output, schema)
      assert result["valid"] is False


  def test_wrong_tool_name_flagged():
      output = '{"name": "write_file", "arguments": {"path": "/x"}}'
      schema = {"name": "read_file", "required": ["path"]}
      result = score_tool_call_json(output, schema)
      assert result["valid"] is True
      assert result["schema_match"] is False


  def test_missing_required_arg_flagged():
      output = '{"name": "read_file", "arguments": {}}'
      schema = {"name": "read_file", "required": ["path"]}
      result = score_tool_call_json(output, schema)
      assert result["valid"] is True
      assert result["schema_match"] is False


  def test_tokens_per_second_basic():
      tps = compute_tokens_per_second(token_count=1024, elapsed_seconds=20.48)
      assert tps == pytest.approx(50.0, rel=1e-3)


  def test_tokens_per_second_zero_elapsed_returns_zero():
      assert compute_tokens_per_second(token_count=100, elapsed_seconds=0) == 0.0


  def test_needle_recall_finds_exact_string():
      response = "...the needle is BLUEFOX-9417 hidden at position 28000..."
      needle = "BLUEFOX-9417"
      result = score_needle_recall(response, needle)
      assert result["recalled"] is True


  def test_needle_recall_misses_when_absent():
      response = "I cannot find the needle in this haystack."
      needle = "BLUEFOX-9417"
      result = score_needle_recall(response, needle)
      assert result["recalled"] is False


  def test_pi_gotcha_compat_flags_developer_role_unsupported():
      sample_response_text = '{"error": "unknown role: developer"}'
      result = score_pi_gotcha_compat(sample_response_text, gotcha="developer_role")
      assert result["affected"] is True


  def test_pi_gotcha_compat_passes_when_dev_role_handled():
      sample_response_text = '{"role": "assistant", "content": "Hello."}'
      result = score_pi_gotcha_compat(sample_response_text, gotcha="developer_role")
      assert result["affected"] is False
  ```

- [ ] **Step 2: Run tests to verify they fail**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_benchmark_scorers.py -v
  ```

  Expected: All tests fail with `ImportError: No module named 'lib.benchmark_scorers'`.

- [ ] **Step 3: Commit failing tests**

  ```bash
  git add agents-sdk/tests/test_benchmark_scorers.py
  git commit -m "test(benchmarks): add failing scorer tests for topic_20"
  ```

### Task 1.3: Implement `lib/benchmark_scorers.py` until tests pass

**Files:**
- Create: `agents-sdk/lib/benchmark_scorers.py`

- [ ] **Step 1: Write minimal implementation**

  ```python
  # agents-sdk/lib/benchmark_scorers.py
  """Pure scoring functions for the topic_20 benchmark harness.

  Each scorer takes raw model output (or a derived measurement) and returns
  a dict with at minimum a binary pass/fail field. No I/O. No state.
  """
  from __future__ import annotations

  import json
  from typing import Any


  def score_tool_call_json(output: str, schema: dict[str, Any]) -> dict[str, Any]:
      """Score a single tool-call output against an expected schema.

      Returns:
          {"valid": bool, "schema_match": bool, "parsed": dict | None, "error": str | None}
      """
      try:
          parsed = json.loads(output)
      except json.JSONDecodeError as e:
          return {"valid": False, "schema_match": False, "parsed": None, "error": str(e)}

      if not isinstance(parsed, dict):
          return {"valid": False, "schema_match": False, "parsed": parsed, "error": "not a JSON object"}

      name_match = parsed.get("name") == schema.get("name")
      args = parsed.get("arguments") or {}
      required = schema.get("required") or []
      args_present = all(key in args for key in required)

      return {
          "valid": True,
          "schema_match": bool(name_match and args_present),
          "parsed": parsed,
          "error": None,
      }


  def compute_tokens_per_second(token_count: int, elapsed_seconds: float) -> float:
      """Return decode tok/s. Returns 0.0 if elapsed_seconds is 0 (no division by zero)."""
      if elapsed_seconds <= 0:
          return 0.0
      return float(token_count) / float(elapsed_seconds)


  def score_needle_recall(response: str, needle: str) -> dict[str, Any]:
      """Binary recall check — is the needle string present in the response?"""
      return {"recalled": needle in response, "needle": needle}


  # Map of Pi-gotcha probes to recognizable failure signatures in raw model output.
  # Sourced from Topic 19 §"Critical Pi Gotchas" + Topic 16 §"Gotchas".
  _PI_GOTCHA_SIGNATURES: dict[str, list[str]] = {
      # Ollama doesn't recognize `developer` role -> crashes or echoes the input
      "developer_role": ["unknown role: developer", "role.*developer"],
      # Default num_ctx 2048 -> truncation behaviors visible in output tail
      "ctx_2048_truncation": ["context length exceeded", "truncated", "max tokens"],
      # Tool-call streaming bug -> empty content with finish_reason: stop
      "streaming_tool_calls": ['"finish_reason":"stop"', '"content":""'],
      # Gemma4 vision-on-text bug -> fails when read tool emits binary
      "gemma4_vision_read": ["image_url required", "binary data not accepted"],
      # Auto-compaction overflow -> output mentions truncated work
      "auto_compaction": ["session truncated", "compaction overflow"],
  }


  def score_pi_gotcha_compat(response_text: str, gotcha: str) -> dict[str, Any]:
      """Binary affected-by-gotcha check.

      Returns {"affected": True} if the response text contains any failure
      signature for the named gotcha, False otherwise.
      """
      import re
      sigs = _PI_GOTCHA_SIGNATURES.get(gotcha, [])
      for sig in sigs:
          if re.search(sig, response_text, re.IGNORECASE):
              return {"affected": True, "matched_signature": sig}
      return {"affected": False, "matched_signature": None}
  ```

- [ ] **Step 2: Run tests to verify they pass**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_benchmark_scorers.py -v
  ```

  Expected: 10 tests pass.

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/lib/benchmark_scorers.py
  git commit -m "feat(benchmarks): implement benchmark_scorers for topic_20"
  ```

### Task 1.4: Write failing tests for `lib/wol.py`

**Files:**
- Create: `agents-sdk/tests/test_wol.py`

- [ ] **Step 1: Write the failing test file**

  ```python
  # agents-sdk/tests/test_wol.py
  """Tests for lib/wol.py — magic packet construction."""
  import pytest
  from lib.wol import build_magic_packet, parse_mac


  def test_parse_mac_colon_separated():
      assert parse_mac("B4:E9:B8:F7:71:47") == b"\xb4\xe9\xb8\xf7\x71\x47"


  def test_parse_mac_dash_separated():
      assert parse_mac("B4-E9-B8-F7-71-47") == b"\xb4\xe9\xb8\xf7\x71\x47"


  def test_parse_mac_lowercase():
      assert parse_mac("b4:e9:b8:f7:71:47") == b"\xb4\xe9\xb8\xf7\x71\x47"


  def test_parse_mac_invalid_format_raises():
      with pytest.raises(ValueError):
          parse_mac("not-a-mac")


  def test_magic_packet_structure():
      mac = "B4:E9:B8:F7:71:47"
      packet = build_magic_packet(mac)
      # Magic packet: 6 bytes 0xFF + 16 repetitions of the 6-byte MAC = 102 bytes
      assert len(packet) == 102
      assert packet[:6] == b"\xff" * 6
      # Verify the MAC repeats 16 times after the sync stream
      mac_bytes = b"\xb4\xe9\xb8\xf7\x71\x47"
      for i in range(16):
          offset = 6 + i * 6
          assert packet[offset:offset + 6] == mac_bytes
  ```

- [ ] **Step 2: Run tests to verify they fail**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_wol.py -v
  ```

  Expected: All fail with `ImportError`.

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/tests/test_wol.py
  git commit -m "test(wol): add failing magic packet tests"
  ```

### Task 1.5: Implement `lib/wol.py`

**Files:**
- Create: `agents-sdk/lib/wol.py`

- [ ] **Step 1: Write the implementation**

  ```python
  # agents-sdk/lib/wol.py
  """Wake-on-LAN magic packet construction + send.

  Pattern A — sender is the always-on Mac Mini; target is the Alienware on the
  same wired LAN. Magic packet is broadcast UDP on port 9 (RFC convention).
  """
  from __future__ import annotations

  import re
  import socket
  from typing import Optional


  _MAC_RE = re.compile(r"^([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})$")


  def parse_mac(mac: str) -> bytes:
      """Parse a MAC address in colon or dash format into 6 raw bytes."""
      m = _MAC_RE.match(mac.strip())
      if not m:
          raise ValueError(f"invalid MAC address: {mac!r}")
      return bytes(int(group, 16) for group in m.groups())


  def build_magic_packet(mac: str) -> bytes:
      """Build a standard WoL magic packet for the given MAC address.

      Format: 6 bytes of 0xFF + 16 repetitions of the target MAC = 102 bytes.
      """
      mac_bytes = parse_mac(mac)
      return b"\xff" * 6 + mac_bytes * 16


  def send_magic_packet(
      mac: str,
      broadcast_addr: str = "255.255.255.255",
      port: int = 9,
      repeats: int = 3,
  ) -> None:
      """Send a WoL magic packet via UDP broadcast.

      Sends `repeats` times back-to-back (some NICs miss the first one).
      """
      packet = build_magic_packet(mac)
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      try:
          for _ in range(repeats):
              sock.sendto(packet, (broadcast_addr, port))
      finally:
          sock.close()


  def probe_until_ready(
      host: str,
      port: int,
      timeout_total_secs: int = 120,
      interval_secs: int = 3,
  ) -> Optional[float]:
      """Open a TCP connect to (host, port) every interval_secs until it succeeds.

      Returns elapsed seconds on success, None on total-timeout.
      """
      import time
      start = time.monotonic()
      deadline = start + timeout_total_secs
      while time.monotonic() < deadline:
          try:
              with socket.create_connection((host, port), timeout=interval_secs):
                  return time.monotonic() - start
          except (OSError, socket.timeout):
              time.sleep(interval_secs)
      return None
  ```

- [ ] **Step 2: Run tests to verify they pass**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_wol.py -v
  ```

  Expected: 5 tests pass.

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/lib/wol.py
  git commit -m "feat(wol): implement magic packet construction + TCP probe"
  ```

### Task 1.6: Write `scripts/wake_alienware.py`

**Files:**
- Create: `agents-sdk/scripts/wake_alienware.py`

- [ ] **Step 1: Write the script**

  ```python
  # agents-sdk/scripts/wake_alienware.py
  """Wake the Alienware via WoL and block until Ollama is responsive.

  Defaults pulled from config.toml [routing.machines.alienware]. The script
  exits 0 once Ollama at /api/tags responds with 200, exits 1 on total timeout.
  """
  from __future__ import annotations

  import argparse
  import sys
  import time
  from pathlib import Path

  # Add agents-sdk to PYTHONPATH so `from lib.wol import …` works regardless of cwd.
  HERE = Path(__file__).resolve().parent.parent
  sys.path.insert(0, str(HERE))

  from lib.config import load_config  # type: ignore[import-not-found]
  from lib.wol import send_magic_packet, probe_until_ready  # type: ignore[import-not-found]


  def main() -> int:
      p = argparse.ArgumentParser(description="WoL + readiness probe for the Alienware (Tier C).")
      p.add_argument("--mac", help="Override MAC (defaults to config.toml routing.machines.alienware.wol_mac)")
      p.add_argument("--host", help="Override host:port for the readiness probe")
      p.add_argument("--timeout", type=int, default=180, help="Total wait budget in seconds (default 180)")
      p.add_argument("--quiet", action="store_true")
      args = p.parse_args()

      cfg = load_config()
      machine = cfg.get("routing", {}).get("machines", {}).get("alienware", {})
      mac = args.mac or machine.get("wol_mac")
      host = args.host or machine.get("host", "192.168.68.201")
      port = int(machine.get("port", 11434))

      if not mac:
          print("ERROR: no MAC address resolved (set --mac or config.toml routing.machines.alienware.wol_mac)", file=sys.stderr)
          return 1

      if not args.quiet:
          print(f"[wake_alienware] sending magic packet to {mac} via UDP broadcast :9 (x3)")

      send_magic_packet(mac)

      if not args.quiet:
          print(f"[wake_alienware] probing tcp://{host}:{port} every 3s for up to {args.timeout}s")

      start = time.monotonic()
      elapsed = probe_until_ready(host, port, timeout_total_secs=args.timeout, interval_secs=3)
      if elapsed is None:
          print(f"[wake_alienware] TIMEOUT after {args.timeout}s", file=sys.stderr)
          return 1

      if not args.quiet:
          print(f"[wake_alienware] ready in {elapsed:.1f}s")
      return 0


  if __name__ == "__main__":
      sys.exit(main())
  ```

- [ ] **Step 2: Verify import-only run (does NOT actually send a packet — needs `--help`)**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/wake_alienware.py --help
  ```

  Expected: argparse help printed; no errors.

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/scripts/wake_alienware.py
  git commit -m "feat(wol): wake_alienware CLI with config-driven defaults"
  ```

### Task 1.7: Write `scripts/sleep_alienware.py`

**Files:**
- Create: `agents-sdk/scripts/sleep_alienware.py`

- [ ] **Step 1: Write the script**

  Strategy: SSH-based for both Windows-OpenSSH and Linux. Sean confirms in Task 0.1 whether OpenSSH is enabled on the Alienware. If Windows-OpenSSH is not enabled, the plan documents enabling it as an Alienware-side action in Task 2.1.

  ```python
  # agents-sdk/scripts/sleep_alienware.py
  """Trigger a graceful sleep on the Alienware via SSH.

  Windows: invokes `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` (modern sleep).
  Linux: invokes `systemctl suspend`.

  The OS is inferred from a small probe — if the SSH banner contains "Windows"
  the Windows command is used; otherwise Linux is assumed. Override with --os.
  """
  from __future__ import annotations

  import argparse
  import shlex
  import subprocess
  import sys


  def detect_os(host: str, user: str) -> str:
      """Return 'windows' or 'linux' based on the remote SSH banner."""
      result = subprocess.run(
          ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=5",
           f"{user}@{host}", "ver"],
          capture_output=True, text=True, timeout=10,
      )
      out = (result.stdout + result.stderr).lower()
      if "windows" in out or "microsoft" in out:
          return "windows"
      return "linux"


  def sleep_remote(host: str, user: str, os_override: str | None = None) -> int:
      os_kind = os_override or detect_os(host, user)
      if os_kind == "windows":
          cmd = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
      else:
          cmd = "sudo systemctl suspend"

      result = subprocess.run(
          ["ssh", "-o", "StrictHostKeyChecking=accept-new", f"{user}@{host}", cmd],
          timeout=30,
      )
      return result.returncode


  def main() -> int:
      p = argparse.ArgumentParser(description="Gracefully sleep the Alienware (Tier C) via SSH.")
      p.add_argument("--host", default="192.168.68.201")
      p.add_argument("--user", required=True, help="SSH username on the Alienware")
      p.add_argument("--os", choices=["windows", "linux"], help="Skip OS auto-detect")
      args = p.parse_args()
      return sleep_remote(args.host, args.user, args.os)


  if __name__ == "__main__":
      sys.exit(main())
  ```

- [ ] **Step 2: Verify `--help`**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/sleep_alienware.py --help
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/scripts/sleep_alienware.py
  git commit -m "feat(wol): sleep_alienware CLI for graceful remote sleep"
  ```

### Task 1.8: Write prompt fixtures — `tool_calls.jsonl`

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/prompts/tool_calls.jsonl`

The format is one JSON object per line. Each line is `{"id": str, "prompt": str, "schema": {"name": str, "required": [str]}}`. Twenty prompts spread across four tool schemas (read_file, write_file, edit_file, run_bash) — the Pi-canonical tool set per Topic 16 §5 and Topic 19 §1.

- [ ] **Step 1: Write the file**

  ```jsonl
  {"id": "tc-01", "prompt": "Call the read_file tool to load /etc/hosts and show me the first 5 lines.", "schema": {"name": "read_file", "required": ["path"]}}
  {"id": "tc-02", "prompt": "Read the file at ~/.zshrc using the read_file tool.", "schema": {"name": "read_file", "required": ["path"]}}
  {"id": "tc-03", "prompt": "Use read_file to open /tmp/foo.txt and return its contents.", "schema": {"name": "read_file", "required": ["path"]}}
  {"id": "tc-04", "prompt": "I need you to read the file located at /var/log/system.log.", "schema": {"name": "read_file", "required": ["path"]}}
  {"id": "tc-05", "prompt": "Please read /home/user/notes.md via the read_file tool.", "schema": {"name": "read_file", "required": ["path"]}}
  {"id": "tc-06", "prompt": "Write the string 'hello world' to /tmp/greeting.txt via write_file.", "schema": {"name": "write_file", "required": ["path", "content"]}}
  {"id": "tc-07", "prompt": "Create a new file at /tmp/config.yaml with the content 'enabled: true'.", "schema": {"name": "write_file", "required": ["path", "content"]}}
  {"id": "tc-08", "prompt": "Use write_file to save 'first line\\nsecond line' to /tmp/multi.txt.", "schema": {"name": "write_file", "required": ["path", "content"]}}
  {"id": "tc-09", "prompt": "Save the JSON object {\"x\": 1} to /tmp/data.json with the write_file tool.", "schema": {"name": "write_file", "required": ["path", "content"]}}
  {"id": "tc-10", "prompt": "Write a 3-line bash shebang script (echo hello, exit 0) to /tmp/run.sh.", "schema": {"name": "write_file", "required": ["path", "content"]}}
  {"id": "tc-11", "prompt": "In /tmp/foo.py replace the string 'old' with 'new' using the edit_file tool.", "schema": {"name": "edit_file", "required": ["path", "old_string", "new_string"]}}
  {"id": "tc-12", "prompt": "Edit /etc/hosts to change 'localhost' to 'localhost.local' via edit_file.", "schema": {"name": "edit_file", "required": ["path", "old_string", "new_string"]}}
  {"id": "tc-13", "prompt": "Use edit_file to swap 'TODO' for 'DONE' inside /tmp/list.txt.", "schema": {"name": "edit_file", "required": ["path", "old_string", "new_string"]}}
  {"id": "tc-14", "prompt": "Rename the variable 'foo' to 'bar' in /tmp/code.py using edit_file.", "schema": {"name": "edit_file", "required": ["path", "old_string", "new_string"]}}
  {"id": "tc-15", "prompt": "Replace 'enabled: false' with 'enabled: true' in /tmp/config.yaml.", "schema": {"name": "edit_file", "required": ["path", "old_string", "new_string"]}}
  {"id": "tc-16", "prompt": "Run 'ls -la /tmp' and show me the output. Use the run_bash tool.", "schema": {"name": "run_bash", "required": ["command"]}}
  {"id": "tc-17", "prompt": "Execute 'df -h' via run_bash and report.", "schema": {"name": "run_bash", "required": ["command"]}}
  {"id": "tc-18", "prompt": "Use run_bash to run 'uname -a'.", "schema": {"name": "run_bash", "required": ["command"]}}
  {"id": "tc-19", "prompt": "Run 'echo $HOME' via run_bash.", "schema": {"name": "run_bash", "required": ["command"]}}
  {"id": "tc-20", "prompt": "Execute 'cat /etc/os-release' using run_bash.", "schema": {"name": "run_bash", "required": ["command"]}}
  ```

- [ ] **Step 2: Verify file parses as valid JSONL**

  ```bash
  cd agents-sdk && .venv/bin/python3 -c "import json; [json.loads(l) for l in open('benchmarks/topic_20/prompts/tool_calls.jsonl')]; print('ok')"
  ```

  Expected: `ok`.

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/benchmarks/topic_20/prompts/tool_calls.jsonl
  git commit -m "feat(benchmarks): add 20 tool-call prompts for topic_20"
  ```

### Task 1.9: Write prompt fixtures — `agentic_loops.jsonl`

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/prompts/agentic_loops.jsonl`

Ten multi-step prompts representing the Pi agentic-loop pattern (read → edit → bash → verify, repeated). Each loop has 5-10 expected tool calls. The harness counts whether the loop completes the full sequence.

- [ ] **Step 1: Write the file**

  ```jsonl
  {"id": "al-01", "prompt": "Open /tmp/loop_test_01.txt, read its contents, then append the string 'visited' on a new line, and run 'cat /tmp/loop_test_01.txt' to verify.", "min_tool_calls": 3, "expected_tools": ["read_file", "edit_file", "run_bash"]}
  {"id": "al-02", "prompt": "Read /tmp/loop_test_02.py, find the function named 'process', rename it to 'process_data', and run 'python3 -c \"import ast; ast.parse(open(\\\"/tmp/loop_test_02.py\\\").read())\"' to confirm valid Python.", "min_tool_calls": 3, "expected_tools": ["read_file", "edit_file", "run_bash"]}
  {"id": "al-03", "prompt": "Create /tmp/loop_test_03.json containing {\"counter\": 0}. Then read it, increment counter to 1, write it back, and cat the file.", "min_tool_calls": 4, "expected_tools": ["write_file", "read_file", "edit_file", "run_bash"]}
  {"id": "al-04", "prompt": "List files in /tmp matching loop_test_*. For each file found, print its first line. Use run_bash twice — once for the listing, once for the print loop.", "min_tool_calls": 2, "expected_tools": ["run_bash"]}
  {"id": "al-05", "prompt": "Read /tmp/loop_test_05.yaml. If it contains 'enabled: false', flip it to 'true' and save. Verify by re-reading.", "min_tool_calls": 3, "expected_tools": ["read_file", "edit_file"]}
  {"id": "al-06", "prompt": "Create three files in /tmp: alpha.txt, beta.txt, gamma.txt — each containing its own name. Then run 'ls /tmp/{alpha,beta,gamma}.txt' to confirm.", "min_tool_calls": 4, "expected_tools": ["write_file", "run_bash"]}
  {"id": "al-07", "prompt": "Read /tmp/loop_test_07.log. Count how many lines contain the word 'ERROR'. Append that count to /tmp/error_count.txt.", "min_tool_calls": 3, "expected_tools": ["read_file", "run_bash", "write_file"]}
  {"id": "al-08", "prompt": "Edit /tmp/loop_test_08.sh to add a 'set -euo pipefail' line right after the shebang. Then run 'bash -n /tmp/loop_test_08.sh' to syntax-check.", "min_tool_calls": 2, "expected_tools": ["edit_file", "run_bash"]}
  {"id": "al-09", "prompt": "Read /tmp/loop_test_09.csv. Convert it to JSON (one object per row) and save to /tmp/loop_test_09.json. Verify by counting lines in both files.", "min_tool_calls": 4, "expected_tools": ["read_file", "write_file", "run_bash"]}
  {"id": "al-10", "prompt": "Find every .py file in /tmp/loop_test_10/, read it, and report which ones import 'os'. Use a single run_bash with grep.", "min_tool_calls": 1, "expected_tools": ["run_bash"]}
  ```

- [ ] **Step 2: Validate JSONL**

  ```bash
  cd agents-sdk && .venv/bin/python3 -c "import json; [json.loads(l) for l in open('benchmarks/topic_20/prompts/agentic_loops.jsonl')]; print('ok')"
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/benchmarks/topic_20/prompts/agentic_loops.jsonl
  git commit -m "feat(benchmarks): add 10 agentic-loop prompts for topic_20"
  ```

### Task 1.10: Write `needle_haystack.py` — 32K-token needle generator

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/prompts/needle_haystack.py`

- [ ] **Step 1: Write the generator**

  ```python
  # agents-sdk/benchmarks/topic_20/prompts/needle_haystack.py
  """Generate a 32K-token prompt with a needle at the 28K-token mark.

  Uses lorem-ipsum-style filler (no external deps; deterministic given a seed)
  so each model sees the same haystack distribution. The needle is a randomly
  generated 12-character uppercase token; the model is asked to recall it.

  Token counting is approximate (chars/4 heuristic). Targeted budget: 32K tokens
  ≈ 128K characters of filler.
  """
  from __future__ import annotations

  import random
  import string
  from dataclasses import dataclass

  CHAR_PER_TOKEN = 4  # Conservative estimate; matches OpenAI's old rule of thumb.

  _FILLER_PARA = (
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
      "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
      "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
      "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
      "cillum dolore eu fugiat nulla pariatur. "
  )


  @dataclass
  class HaystackPrompt:
      prompt: str
      needle: str
      needle_position_chars: int


  def make_needle(rng: random.Random) -> str:
      """Generate a 12-char uppercase needle (alphanumeric, no ambiguous chars)."""
      alphabet = "".join(c for c in string.ascii_uppercase + string.digits if c not in "OIL01")
      return "".join(rng.choices(alphabet, k=12))


  def generate(
      seed: int = 42,
      target_tokens: int = 32000,
      needle_position_tokens: int = 28000,
  ) -> HaystackPrompt:
      rng = random.Random(seed)
      needle = make_needle(rng)
      target_chars = target_tokens * CHAR_PER_TOKEN
      needle_char_position = needle_position_tokens * CHAR_PER_TOKEN

      filler = (_FILLER_PARA * ((target_chars // len(_FILLER_PARA)) + 1))[:target_chars]
      sentence = f" The secret code is {needle}. Remember it. "
      injected = filler[:needle_char_position] + sentence + filler[needle_char_position:target_chars]

      prompt = (
          "Read the following long document carefully. At the end, I will ask you "
          "to recall a specific 12-character code that appears somewhere inside. "
          "Do not summarize the document — only output the code when asked.\n\n"
          "DOCUMENT:\n"
          f"{injected}\n\n"
          "QUESTION: What was the 12-character secret code? Output ONLY the code, "
          "nothing else."
      )
      return HaystackPrompt(prompt=prompt, needle=needle, needle_position_chars=needle_char_position)


  if __name__ == "__main__":
      import json
      import sys
      seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
      result = generate(seed=seed)
      print(json.dumps({"seed": seed, "needle": result.needle, "prompt_chars": len(result.prompt)}))
  ```

- [ ] **Step 2: Smoke test the generator**

  ```bash
  cd agents-sdk && .venv/bin/python3 benchmarks/topic_20/prompts/needle_haystack.py 1
  ```

  Expected: a JSON line with `seed`, `needle` (12 chars), and `prompt_chars` (≥125,000).

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/benchmarks/topic_20/prompts/needle_haystack.py
  git commit -m "feat(benchmarks): add 32K needle-in-haystack generator"
  ```

### Task 1.11: Write the main benchmark runner — `benchmark_ollama_model.py`

**Files:**
- Create: `agents-sdk/scripts/benchmark_ollama_model.py`

- [ ] **Step 1: Write the runner**

  ```python
  # agents-sdk/scripts/benchmark_ollama_model.py
  """Run the topic_20 benchmark suite against a single Ollama model.

  Captures all 6 dimensions defined in benchmarks/topic_20/README.md.
  Writes one JSONL per run at:
      benchmarks/topic_20/results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl

  Each line is a complete record for ONE measurement (one tool-call probe,
  one tok/s sample, one needle run, etc.) with a `kind` field disambiguating.

  Idempotency: re-running with the same (model, tier, date) APPENDS — caller
  should manage that or pass --out-file with a unique name.

  All inference is over Ollama's native /api/chat endpoint (NOT /v1 OpenAI-
  compat) to bypass the streaming tool_calls bug per Topic 19 §"Critical Pi
  Gotchas — 1. Tool-call streaming bug (Ollama issue #12557)".
  """
  from __future__ import annotations

  import argparse
  import json
  import sys
  import time
  from datetime import date
  from pathlib import Path

  import requests

  HERE = Path(__file__).resolve().parent.parent
  sys.path.insert(0, str(HERE))

  from lib.benchmark_scorers import (
      score_tool_call_json,
      compute_tokens_per_second,
      score_needle_recall,
      score_pi_gotcha_compat,
  )
  from benchmarks.topic_20.prompts import needle_haystack  # type: ignore[import-not-found]


  DEFAULT_HOST = "http://localhost:11434"
  TIMEOUT_PER_REQUEST = 600  # seconds; long for needle-haystack at 32K
  TOOL_CALL_PROMPTS = HERE / "benchmarks/topic_20/prompts/tool_calls.jsonl"
  AGENTIC_LOOP_PROMPTS = HERE / "benchmarks/topic_20/prompts/agentic_loops.jsonl"


  # ─── Ollama HTTP wrappers ─────────────────────────────────────────────────

  def _ollama_chat(host: str, model: str, messages: list[dict], options: dict | None = None,
                   stream: bool = False, format_json: bool = False) -> dict:
      body: dict = {"model": model, "messages": messages, "stream": stream}
      if options:
          body["options"] = options
      if format_json:
          body["format"] = "json"
      resp = requests.post(f"{host}/api/chat", json=body, timeout=TIMEOUT_PER_REQUEST)
      resp.raise_for_status()
      return resp.json()


  # ─── Dimension runners ────────────────────────────────────────────────────

  def run_tool_call_suite(host: str, model: str) -> list[dict]:
      """Dimension 1: tool-call JSON validity.

      Each prompt is forwarded with `format=json` so Ollama constrains output to
      valid JSON. The schema-match check still verifies the model picked the
      right tool name + required args.
      """
      results = []
      with open(TOOL_CALL_PROMPTS) as f:
          for line in f:
              probe = json.loads(line)
              system_msg = (
                  "You are a tool-calling assistant. Output ONLY a single JSON "
                  "object of the form {\"name\": <tool>, \"arguments\": {...}}. "
                  "No prose, no markdown fences."
              )
              try:
                  resp = _ollama_chat(
                      host, model,
                      messages=[
                          {"role": "system", "content": system_msg},
                          {"role": "user", "content": probe["prompt"]},
                      ],
                      options={"num_ctx": 4096, "temperature": 0.0},
                      format_json=True,
                  )
                  content = resp["message"]["content"]
                  scored = score_tool_call_json(content, probe["schema"])
              except Exception as e:
                  scored = {"valid": False, "schema_match": False, "error": str(e)}
                  content = None

              results.append({
                  "kind": "tool_call",
                  "probe_id": probe["id"],
                  "model": model,
                  "raw_response": content,
                  **scored,
              })
      return results


  def run_throughput_suite(host: str, model: str, runs: int = 3) -> list[dict]:
      """Dimension 2: decode tok/s on a fixed ~1024-token output.

      Asks the model to emit ~1024 tokens of generated text. Uses Ollama's
      eval_count / eval_duration metrics from the response for accurate tok/s.
      """
      prompt = (
          "Write a 1000-word fictional vignette about a programmer debugging "
          "a network issue at 3 AM. Include dialogue, technical detail, and a "
          "twist ending. Aim for exactly 1000 words."
      )
      results = []
      for i in range(runs):
          start = time.monotonic()
          resp = _ollama_chat(
              host, model,
              messages=[{"role": "user", "content": prompt}],
              options={"num_ctx": 4096, "num_predict": 1024, "temperature": 0.7, "seed": i},
          )
          wall = time.monotonic() - start
          eval_count = resp.get("eval_count", 0)
          eval_duration_ns = resp.get("eval_duration", 0)
          ollama_tps = compute_tokens_per_second(eval_count, eval_duration_ns / 1e9)
          wall_tps = compute_tokens_per_second(eval_count, wall)
          results.append({
              "kind": "throughput",
              "model": model,
              "run": i,
              "eval_count": eval_count,
              "eval_duration_secs": eval_duration_ns / 1e9,
              "wall_secs": wall,
              "ollama_tps": ollama_tps,
              "wall_tps": wall_tps,
          })
      return results


  def run_needle_suite(host: str, model: str, num_ctx: int, runs: int = 5) -> list[dict]:
      """Dimension 5: long-context needle recall at 28K position inside 32K window.

      If num_ctx < 32768, this dimension is reported as 'skipped' for the model.
      """
      if num_ctx < 32768:
          return [{
              "kind": "needle",
              "model": model,
              "skipped_reason": f"num_ctx={num_ctx} < 32768",
          }]

      results = []
      for seed in range(runs):
          hs = needle_haystack.generate(seed=seed)
          try:
              resp = _ollama_chat(
                  host, model,
                  messages=[{"role": "user", "content": hs.prompt}],
                  options={"num_ctx": 32768, "temperature": 0.0, "num_predict": 32},
              )
              content = resp["message"]["content"].strip()
              scored = score_needle_recall(content, hs.needle)
          except Exception as e:
              scored = {"recalled": False, "error": str(e)}
              content = None
          results.append({
              "kind": "needle",
              "model": model,
              "seed": seed,
              "needle": hs.needle,
              "response": content,
              **scored,
          })
      return results


  def run_pi_gotcha_suite(host: str, model: str) -> list[dict]:
      """Dimension 6: probe each of the 5 Pi gotchas as binary pass/fail.

      Probes are constructed to surface each gotcha:
      - developer_role: send a 'developer'-role message and see if model crashes
      - ctx_2048_truncation: send a 3K-token prompt with num_ctx unset (default 2048) and check for truncation
      - streaming_tool_calls: ask for a tool call with stream=True and check for empty content + finish_reason
      - gemma4_vision_read: skipped here (text-only fleet; not Sean's blocker)
      - auto_compaction: tested implicitly during agentic_loop runs; flagged here only if model is gemma4 family
      """
      results = []

      # 1. developer_role
      try:
          resp = _ollama_chat(
              host, model,
              messages=[{"role": "developer", "content": "Say hello."}],
              options={"num_ctx": 4096, "temperature": 0.0},
          )
          text = json.dumps(resp)
          results.append({
              "kind": "pi_gotcha",
              "gotcha": "developer_role",
              "model": model,
              **score_pi_gotcha_compat(text, "developer_role"),
          })
      except requests.HTTPError as e:
          results.append({
              "kind": "pi_gotcha", "gotcha": "developer_role", "model": model,
              "affected": True, "matched_signature": f"HTTP {e.response.status_code}",
          })

      # 2. ctx_2048_truncation — feed ~3K-token prompt with default ctx
      big_input = ("the quick brown fox jumps over the lazy dog. " * 600)  # ~3000 tokens
      try:
          resp = _ollama_chat(
              host, model,
              messages=[{"role": "user", "content": big_input + "\n\nSummarize in 5 words."}],
              # NOTE: deliberately omitting num_ctx to trigger the default 2048
          )
          content = resp["message"]["content"]
          # If the model summarized, it either truncated or extended ctx natively
          affected = len(content) < 5 or "[..." in content or "..." in content[-30:]
          results.append({
              "kind": "pi_gotcha", "gotcha": "ctx_2048_truncation", "model": model,
              "affected": affected, "matched_signature": "truncation heuristic",
          })
      except Exception as e:
          results.append({
              "kind": "pi_gotcha", "gotcha": "ctx_2048_truncation", "model": model,
              "affected": True, "matched_signature": str(e),
          })

      # 3. streaming_tool_calls — stream=True, ask for a tool call
      try:
          body = {
              "model": model,
              "stream": True,
              "messages": [
                  {"role": "system", "content": "Output a JSON tool call only."},
                  {"role": "user", "content": "Call read_file with path /etc/hosts."},
              ],
              "options": {"num_ctx": 4096, "temperature": 0.0},
              "format": "json",
          }
          last_chunk = None
          got_content = False
          with requests.post(f"{host}/api/chat", json=body, stream=True, timeout=TIMEOUT_PER_REQUEST) as r:
              for line in r.iter_lines():
                  if not line:
                      continue
                  chunk = json.loads(line)
                  last_chunk = chunk
                  if chunk.get("message", {}).get("content"):
                      got_content = True
          # Bug signature: stream ends with finish-reason but no content was ever emitted
          done_no_content = (last_chunk and last_chunk.get("done") and not got_content)
          results.append({
              "kind": "pi_gotcha", "gotcha": "streaming_tool_calls", "model": model,
              "affected": bool(done_no_content),
              "matched_signature": "done=true with no content emitted" if done_no_content else None,
          })
      except Exception as e:
          results.append({
              "kind": "pi_gotcha", "gotcha": "streaming_tool_calls", "model": model,
              "affected": True, "matched_signature": str(e),
          })

      # 4 + 5. gemma4_vision_read + auto_compaction — flag-by-family, not measured
      results.append({
          "kind": "pi_gotcha", "gotcha": "gemma4_vision_read", "model": model,
          "affected": model.lower().startswith("gemma4"),
          "matched_signature": "model is gemma4 family" if model.lower().startswith("gemma4") else None,
          "note": "Vision-on-read bug is irrelevant for text-only fleet — flagged for awareness only.",
      })
      results.append({
          "kind": "pi_gotcha", "gotcha": "auto_compaction", "model": model,
          "affected": False,
          "matched_signature": None,
          "note": "Tested implicitly via agentic loops; flagged separately only if a loop times out >120s.",
      })

      return results


  # ─── Main ─────────────────────────────────────────────────────────────────

  def main() -> int:
      p = argparse.ArgumentParser(description="Topic 20 benchmark runner for a single Ollama model.")
      p.add_argument("--model", required=True, help="Ollama model tag, e.g., qwen3.5:27b")
      p.add_argument("--host", default=DEFAULT_HOST, help="Ollama base URL")
      p.add_argument("--tier", required=True, choices=["A", "B", "C"], help="Hardware tier (A=MBP, B=Mac Mini, C=Alienware)")
      p.add_argument("--num-ctx", type=int, default=16384, help="Native context window of the model variant under test")
      p.add_argument("--out", default=str(HERE / "benchmarks/topic_20/results"))
      p.add_argument("--skip", nargs="*", default=[], choices=["tool_calls", "throughput", "needle", "pi_gotchas"],
                     help="Dimensions to skip (useful for debugging or rerunning a single dimension)")
      args = p.parse_args()

      out_dir = Path(args.out)
      out_dir.mkdir(parents=True, exist_ok=True)
      slug = args.model.replace(":", "_").replace("/", "_")
      out_file = out_dir / f"{slug}-tier{args.tier}-{date.today().isoformat()}.jsonl"

      all_results: list[dict] = []
      if "tool_calls" not in args.skip:
          print(f"[bench] tool_calls suite on {args.model}@tier{args.tier}…", flush=True)
          all_results.extend(run_tool_call_suite(args.host, args.model))
      if "throughput" not in args.skip:
          print(f"[bench] throughput suite…", flush=True)
          all_results.extend(run_throughput_suite(args.host, args.model))
      if "needle" not in args.skip:
          print(f"[bench] needle suite (num_ctx={args.num_ctx})…", flush=True)
          all_results.extend(run_needle_suite(args.host, args.model, num_ctx=args.num_ctx))
      if "pi_gotchas" not in args.skip:
          print(f"[bench] pi_gotchas suite…", flush=True)
          all_results.extend(run_pi_gotcha_suite(args.host, args.model))

      with out_file.open("a") as f:
          for record in all_results:
              f.write(json.dumps(record) + "\n")

      tc_pass = sum(1 for r in all_results if r.get("kind") == "tool_call" and r.get("schema_match"))
      tc_total = sum(1 for r in all_results if r.get("kind") == "tool_call")
      print(f"[bench] DONE — wrote {len(all_results)} records to {out_file}")
      print(f"[bench] tool-call pass rate: {tc_pass}/{tc_total}")
      return 0


  if __name__ == "__main__":
      sys.exit(main())
  ```

- [ ] **Step 2: Verify `--help`**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py --help
  ```

  Expected: argparse help. No traceback.

- [ ] **Step 3: Smoke-test against the existing `gemma4:e4b` on Mac Mini, with the tool-call dimension only**

  ```bash
  cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
      --model gemma4:e4b \
      --host http://192.168.68.200:11434 \
      --tier B \
      --num-ctx 16384 \
      --skip throughput needle pi_gotchas
  ```

  Expected: runs to completion in <2 min; emits 20 records; prints non-zero tool-call pass rate.

- [ ] **Step 4: Inspect smoke output**

  ```bash
  cd agents-sdk && head -2 benchmarks/topic_20/results/gemma4_e4b-tierB-$(date +%Y-%m-%d).jsonl
  ```

  Each line is a valid JSON record with `kind: tool_call` and `valid`, `schema_match` fields. If the pass rate is 0, the harness has a bug — debug before continuing.

- [ ] **Step 5: Commit**

  ```bash
  git add agents-sdk/scripts/benchmark_ollama_model.py
  git commit -m "feat(benchmarks): main topic_20 benchmark runner"
  ```

### Task 1.12: Add a memory-snapshot side script

**Files:**
- Modify: `agents-sdk/scripts/benchmark_ollama_model.py` (already created in Task 1.11)

Dimension 3 (peak memory footprint) is OS-dependent and can't be measured from inside the benchmark process — it requires sampling the Ollama server's RSS during inference. The cleanest approach: a separate shell script the operator runs in another terminal during a long benchmark.

- [ ] **Step 1: Create `agents-sdk/scripts/sample_ollama_rss.sh`**

  ```bash
  #!/usr/bin/env bash
  # Sample ollama-server RSS every 2 seconds for the duration of a benchmark.
  # Writes timestamped samples to benchmarks/topic_20/results/<host>-rss-<date>.csv
  # Usage: ./sample_ollama_rss.sh <hostname-tag> [duration-seconds]
  set -euo pipefail

  HOST_TAG="${1:?host tag required, e.g., macmini / mbp / alienware}"
  DURATION="${2:-600}"
  REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
  OUT="$REPO_ROOT/benchmarks/topic_20/results/${HOST_TAG}-rss-$(date +%Y-%m-%d).csv"

  echo "ts,rss_kb,vsz_kb" > "$OUT"
  END=$(( $(date +%s) + DURATION ))
  while [ "$(date +%s)" -lt "$END" ]; do
    LINE=$(ps -o rss=,vsz= -p "$(pgrep -x ollama | head -1)" 2>/dev/null || echo "0 0")
    RSS=$(echo "$LINE" | awk '{print $1}')
    VSZ=$(echo "$LINE" | awk '{print $2}')
    echo "$(date +%s),$RSS,$VSZ" >> "$OUT"
    sleep 2
  done
  echo "[sample_ollama_rss] wrote $OUT"
  ```

- [ ] **Step 2: Make executable + verify**

  ```bash
  chmod +x agents-sdk/scripts/sample_ollama_rss.sh
  agents-sdk/scripts/sample_ollama_rss.sh test 6
  cat agents-sdk/benchmarks/topic_20/results/test-rss-$(date +%Y-%m-%d).csv
  ```

  Expected: 3-4 rows of (ts, rss_kb, vsz_kb). Delete the test file before committing.

  ```bash
  rm agents-sdk/benchmarks/topic_20/results/test-rss-$(date +%Y-%m-%d).csv
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/scripts/sample_ollama_rss.sh
  git commit -m "feat(benchmarks): RSS sampler for ollama-server during benchmarks"
  ```

---

## Phase 2 — Alienware Tier C standup + WoL

The Alienware joins the agent fleet for the first time in this phase. Sequence: enable WoL at the hardware level → confirm magic packets work → install Ollama as a service → soak-test the wake cycle → write the decision record.

**WoL Pattern selection (primary vs fallback):**

- **Primary: Pattern A — on-demand magic packets from Mac Mini.** Reasons:
  1. Sean's hard constraint ("must not be powered on overnight") favors on-demand wakes.
  2. The Alienware is stationary + wired Ethernet — the prior WoL retirement (v3.14.3) was for a closed-lid laptop scenario that doesn't generalize here.
  3. Magic packet → ready-to-serve latency on a desktop is typically 30-60s from S5; acceptable for batch benchmark runs.
  4. Power cost: <5W in S5 vs ~80-150W idle.
- **Fallback: Pattern B — scheduled wake windows.** Documented in the decision record; flip to Pattern B only if Pattern A's wake-success rate drops below 95% during the Phase 2 soak (10 attempts, ≤9 successes triggers the flip). Pattern B wakes the Alienware at fixed times via Windows Task Scheduler / `rtcwake` and Mac Mini hits the LAN endpoint without sending a packet.

### Task 2.1: Enable WoL at the hardware level (Alienware-side, manual)

**Files:** None (BIOS/UEFI + OS settings).

- [ ] **Step 1: Enter BIOS/UEFI**

  Boot the Alienware → tap F2 (Alienware default) repeatedly during POST. Navigate to: Power Management → Wake on LAN. Set to `Enabled` (or `Enabled on LAN + WLAN` if both NICs are wanted; LAN is sufficient here).

- [ ] **Step 2: Save BIOS settings and let machine boot**

- [ ] **Step 3 (Windows-specific, run from elevated PowerShell on Alienware)**

  ```powershell
  # List adapters
  Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Format-List Name, MacAddress
  # Enable WoL on the Ethernet adapter (substitute "Ethernet" for the actual name)
  Set-NetAdapterPowerManagement -Name "Ethernet" -WakeOnMagicPacket Enabled
  Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Wake on Magic Packet" -DisplayValue "Enabled"
  # Verify
  Get-NetAdapterPowerManagement -Name "Ethernet" | Select-Object Name, WakeOnMagicPacket
  ```

  Expected: `WakeOnMagicPacket : Enabled`. Disable Windows "Fast Startup" — it blocks WoL from full shutdown:

  ```powershell
  powercfg /h off
  ```

- [ ] **Step 3-Linux (only if Alienware is Linux)**

  ```bash
  # Identify the interface
  ip link show
  # Enable WoL on the wired interface (replace eno1 with actual name)
  sudo ethtool -s eno1 wol g
  # Persist across reboots — distro-specific. systemd-networkd or NetworkManager:
  # NetworkManager:
  sudo nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan magic
  # Verify
  sudo ethtool eno1 | grep -i "wake-on"
  ```

  Expected: `Wake-on: g`.

- [ ] **Step 4: Power off the Alienware (full shutdown, not sleep)**

  Used to validate WoL from cold S5 in the next task.

### Task 2.2: Send a magic packet from Mac Mini and verify wake

**Files:** None — uses scripts from Task 1.6.

- [ ] **Step 1: From the Mac Mini, send a magic packet**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk \
    && PYTHONPATH=. .venv/bin/python3 scripts/wake_alienware.py --timeout 180
  ```

  Expected: prints `sending magic packet` and `probing tcp://…`; within 60-120s prints `ready in XX.Xs`. If timeout, troubleshoot in order:
  1. Verify Alienware MAC matches `config.toml:274` (Task 0.3 Step 2).
  2. Verify Deco router doesn't block UDP broadcast on port 9 (Task 0.3 Step 3).
  3. Verify Ollama is installed and configured to auto-start on Alienware boot (Task 2.3).
  4. Re-check BIOS WoL setting (Task 2.1 Step 1).

- [ ] **Step 2: If MAC was wrong, update `config.toml`**

  ```toml
  [routing.machines.alienware]
  ...
  wol_mac = "<actual-mac-from-step-0.3>"
  ```

  Commit:

  ```bash
  git add agents-sdk/config.toml
  git commit -m "fix(routing): correct alienware wol_mac after BIOS verification"
  ```

### Task 2.3: Install Ollama on Alienware as an auto-start service

**Files:** None (system-level).

- [ ] **Step 1 (Windows): Verify Ollama installed as a service**

  Ollama on Windows installs as a user-mode service auto-starting on login. Verify:

  ```powershell
  Get-Process ollama -ErrorAction SilentlyContinue
  ```

  If absent: install from `https://ollama.com/download/windows`, log out and log back in. Note: Windows Ollama serves on `127.0.0.1` by default — bind to all interfaces:

  ```powershell
  # Set system env var so Ollama listens on the LAN
  [System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "User")
  # Restart Ollama by signing out + signing back in (or restart the Ollama tray app)
  ```

- [ ] **Step 1-Linux: Install Ollama with systemd auto-start**

  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  # Edit the unit to listen on LAN
  sudo systemctl edit ollama
  # Add:
  # [Service]
  # Environment="OLLAMA_HOST=0.0.0.0:11434"
  sudo systemctl daemon-reload
  sudo systemctl enable --now ollama
  ```

- [ ] **Step 2: Verify from Mac Mini that Ollama on Alienware responds**

  ```bash
  curl -s --max-time 5 http://192.168.68.201:11434/api/tags
  ```

  Expected: JSON listing existing models (likely just `Qwen3-VL-7B` per config.toml or empty).

### Task 2.4: Set Alienware idle-sleep policy

**Files:** None.

- [ ] **Step 1 (Windows): Set sleep-on-idle to 30 minutes**

  ```powershell
  # Allow this device to wake the computer (NIC) — verify
  powercfg -devicequery wake_armed
  # Set both AC and battery sleep-after to 30 min
  powercfg /change standby-timeout-ac 30
  powercfg /change standby-timeout-dc 30
  # Modern Standby (S0) vs S3: prefer S3 for true low-power WoL responsiveness
  # If Modern Standby is the default, S3 may be enforceable via:
  powercfg /a   # diagnoses available sleep states
  ```

  Expected: `powercfg /a` shows Standby (S3) as supported. If Modern Standby (S0) is the only option, document that the wake latency may be slower (the system stays in low-power S0 with network connectivity, so WoL is effectively instant — but power draw is higher than S3).

- [ ] **Step 1-Linux: Set 30-minute idle suspend**

  ```bash
  # systemd-logind handles idle suspend
  sudo systemctl edit systemd-logind
  # Add:
  # [Login]
  # IdleAction=suspend
  # IdleActionSec=30min
  sudo systemctl restart systemd-logind
  ```

### Task 2.5: 24-hour soak — 10 wake/sleep cycles

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/wol_soak_log.md` (provisional — moved into decision record by Task 2.7)

- [ ] **Step 1: Run 10 wake-sleep cycles spaced across 24 hours**

  Each cycle is: send WoL packet → measure wake latency → run a no-op Ollama call → trigger remote sleep → wait for confirmation.

  Helper script (one-shot inline, not committed):

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
  for i in $(seq 1 10); do
    echo "=== CYCLE $i @ $(date) ==="
    PYTHONPATH=. .venv/bin/python3 scripts/wake_alienware.py --timeout 180
    sleep 2
    curl -s -X POST http://192.168.68.201:11434/api/chat \
        -H 'Content-Type: application/json' \
        -d '{"model": "Qwen3-VL-7B", "messages":[{"role":"user","content":"say hi"}], "stream": false}' \
        | jq -r '.message.content' | head -c 80
    echo
    PYTHONPATH=. .venv/bin/python3 scripts/sleep_alienware.py --user <USER>  # substitute SSH user
    sleep $((60 * 90))  # 90 min between cycles
  done | tee benchmarks/topic_20/wol_soak_log.md
  ```

  **Soak gate:** ≥9 of 10 cycles must succeed end-to-end. If <9 succeed:
  - Investigate which step failed most often (wake latency timeout? sleep didn't take?)
  - Flip to Pattern B (scheduled wake windows) — document the reason in the decision record (Task 2.7).
  - Pattern B specifics: Windows Task Scheduler entry for "Wake the computer to run this task" at 09:00, 13:00, 17:00 daily; OR Linux `rtcwake -m mem -t $(date -d 'tomorrow 09:00' +%s)`.

- [ ] **Step 2: Append cycle results to `wol_soak_log.md`** (no commit yet — content moves to decision record in Task 2.7)

### Task 2.6: Verify SSH-based sleep works under different power states

**Files:** None.

- [ ] **Step 1: From the Mac Mini, after the Alienware is awake and idle**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
  PYTHONPATH=. .venv/bin/python3 scripts/sleep_alienware.py --user <USER>
  echo $?  # Expect 0
  ```

  Then verify the Alienware is unreachable on TCP/11434 within 15s:

  ```bash
  for i in 1 2 3 4 5; do
    nc -z -w 3 192.168.68.201 11434 && echo "still up" || echo "down"
    sleep 3
  done
  ```

  Expected: 1-2 "still up" lines, then "down".

### Task 2.7: Write the Alienware Wake Architecture Decision Record

**Files:**
- Create: `agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md`

- [ ] **Step 1: Write the decision record matching the `local-tts-decision-record.md` style**

  ```markdown
  ---
  type: decision-record
  created: 2026-05-21
  status: accepted
  ---

  # Alienware Tier C — On-Demand Wake-on-LAN Architecture

  ## Decision

  Adopt **Pattern A — on-demand magic packets from the Mac Mini** as the
  wake mechanism for the Alienware Tier C host. Pattern B (scheduled wake
  windows) is documented as the fallback and gated to <95% Pattern A
  success in the 10-cycle soak.

  ## Context

  Sean is unemployed (post-Block, 2026-05) and minimizing electricity cost
  matters. The Alienware (RTX 4090, ~150W idle, ~5W in S3) sits unused
  most of the day; leaving it on overnight to serve a few hours of agent
  workload is a poor power tradeoff. The Mac Mini is the always-on agent
  driver per v3.14.3; the Alienware joins the fleet for Tier C workloads
  (batch codegen, long-context summarization, nemotron3-class agentic
  tasks).

  | Dimension | Pattern A (on-demand WoL) | Pattern B (scheduled windows) |
  |---|---|---|
  | Power cost | <5W in S3, ~150W during workload | ~150W for full window (hours/day) |
  | Wake latency | 30-90s magic packet → ready | 0s within window; cold start at window boundary |
  | Sean-effort to maintain | Low — config-driven, no schedule changes | Low — but adds another schedule to reason about |
  | Failure mode | First packet missed → second/third attempt | Window misalignment → request fails or stalls |
  | Composability | Trivially composable with any caller | Caller must check window membership |
  | Recovery | Re-send packet, max ~3 min | Wait for next window or trigger manual wake |

  ## Rationale

  - **Sean's constraint is binding.** The hard rule "must not be powered on
    overnight" makes Pattern B's all-day-window approach lose on idle power.
  - **Stationary + Ethernet eliminates the v3.14.3 risk.** That retirement
    was for a closed-lid laptop. Desktop + wired NIC is the WoL happy path.
  - **Pattern A latency is acceptable for batch use.** Tier C workloads
    (benchmark sweeps, batch codegen) tolerate a 60s wake; no real-time
    request needs sub-second wake.
  - **Caller integration is one line.** Any agent or script that needs
    Tier C invokes `wake_alienware.py` before its call. No window math.
  - **Power math.** Conservative: 22 hours/day asleep × 4W + 2 hours
    workload × 150W = ~388 Wh/day ≈ 12 kWh/month ≈ $1.50/month (at $0.13/
    kWh ET). Pattern B at 8 hours/day window × 150W = 36 kWh/month ≈
    $4.70/month. Pattern A is a 3x power reduction without sacrificing
    capability.

  ## Implementation summary

  - `agents-sdk/lib/wol.py` — magic packet construction + TCP readiness probe.
  - `agents-sdk/scripts/wake_alienware.py` — CLI wrapper, config-driven defaults.
  - `agents-sdk/scripts/sleep_alienware.py` — SSH-based graceful sleep trigger.
  - `agents-sdk/config.toml [routing.machines.alienware]` — `wol_mac`,
    `host`, `port` already wired (lines 268-275).
  - BIOS/UEFI WoL enabled; Windows Fast Startup disabled; idle-sleep set
    to 30 minutes.

  ## Soak evidence

  10-cycle / 24-hour test on 2026-05-XX (fill date when soak runs in Task 2.5):

  | Cycle | Wake latency (s) | Sleep success | Notes |
  |---|---|---|---|
  | 1 | ... | ... | ... |
  | ... | ... | ... | ... |
  | 10 | ... | ... | ... |
  | **Median** | ... | — | — |
  | **Success rate** | — | ... / 10 | — |

  **Decision held / flipped:** [held — Pattern A adopted | flipped — Pattern B
  adopted because <fill reason>]

  ## Rollback

  To disable Tier C entirely:
  1. Set `[routing.machines.alienware].always_on = false` (already the value).
  2. Remove any task-map entries that route to `alienware` from
     `config.toml [routing.task_map]`.
  3. Power the Alienware off and leave it off; no other change needed.

  To revert Pattern A → Pattern B:
  1. Add a Windows Task Scheduler entry (or Linux `rtcwake`) for the wake
     windows.
  2. Remove `scripts/wake_alienware.py` invocations from any caller (none
     exist as of the v1 ship; Phase 6 may add them — those callers can be
     updated trivially since the script is invoked only inside the batch
     entry point).

  ## Open questions

  - Whether Pattern A's per-call latency starts to dominate end-to-end
    benchmark wall time on rapid-fire test batches. If so, the wake should
    be hoisted out of the per-call path into a per-batch wrapper (already
    the design; this is just a perf note).
  - Whether Tailscale-based wake is worth standing up for off-LAN access
    (Sean travels). Deferred — no off-LAN Tier C call path exists yet.

  ## References

  - Plan: `agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md`
  - Synthesis context: `vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md`
  - Prior WoL retirement (different scenario): `CHANGELOG.md` v3.14.3 (2026-04-18)
  ```

- [ ] **Step 2: Fill in the soak evidence table with the actual data from Task 2.5**

- [ ] **Step 3: Commit**

  ```bash
  git add agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md
  git rm agents-sdk/benchmarks/topic_20/wol_soak_log.md  # absorbed into decision record
  git commit -m "docs: Alienware Tier C wake architecture decision record"
  ```

---

## Phase 3 — Pull candidate models per tier

Each pull is reversible via `ollama rm <tag>`. The Modelfile overlays set the `num_ctx` and disable Qwen `thinking` mode where applicable.

### Task 3.1: Pull Tier A candidates on the MBP

**Files:** None (Ollama state).

**Pre-req:** Ollama must be running on the MBP. Sean's MBP currently runs LM Studio (not Ollama) per config.toml — verify:

```bash
ollama --version  # If missing: brew install ollama && ollama serve &
```

If Ollama is not installed on MBP, install it now. Note: LM Studio's port 1234 is separate; both can run. Ollama defaults to 11434.

- [ ] **Step 1: Pull `qwen3.5:27b` (17GB)**

  ```bash
  ollama pull qwen3.5:27b
  ```

- [ ] **Step 2: Pull `qwen3.5:35b` (24GB) IF MBP has ≥48GB unified memory (Task 0.2)**

  ```bash
  ollama pull qwen3.5:35b
  ```

  If MBP is 36GB, skip — log "skipped: insufficient unified memory" in Status Tracker.

- [ ] **Step 3: Pull `qwen3.6:35b` (24GB) IF MBP has ≥48GB unified memory**

  ```bash
  ollama pull qwen3.6:35b
  ```

- [ ] **Step 4: Pull `qwen3-coder:30b` (baseline from Topic 19 synthesis)**

  ```bash
  ollama pull qwen3-coder:30b
  ```

- [ ] **Step 5: Build 32K-context Modelfile variants for each, with `thinking` disabled where applicable**

  ```bash
  for tag in qwen3.5:27b qwen3.5:35b qwen3.6:35b qwen3-coder:30b; do
    [ -n "$(ollama list | grep -F "$tag")" ] || continue
    slug=$(echo "$tag" | tr ':/' '__')
    ollama show "$tag" --modelfile > "/tmp/${slug}-32k.modelfile"
    echo "PARAMETER num_ctx 32768" >> "/tmp/${slug}-32k.modelfile"
    # Disable thinking mode on Qwen 3.5/3.6 — verify support per-model via
    # `ollama show <tag> | grep -i think` after Task 3.1 Step 1. If supported:
    echo "PARAMETER think false" >> "/tmp/${slug}-32k.modelfile" || true
    ollama create "${tag%:*}-32k" -f "/tmp/${slug}-32k.modelfile"
  done
  ```

  **Note on `think false`:** verify per-model that this parameter is honored. Qwen3-style models accept `/no_think` in the TEMPLATE or `think: false` as an options field on `/api/chat`. If `PARAMETER think false` errors in `ollama create`, drop that line and instead pass `"think": false` per-call from the benchmark runner.

- [ ] **Step 6: Verify each variant exists**

  ```bash
  ollama list | grep -E "(qwen3\.5|qwen3\.6|qwen3-coder)-32k"
  ```

- [ ] **Step 7: Commit no code — pull state is host-local and reversible via `ollama rm`**

### Task 3.2: Pull Tier B candidates on the Mac Mini

**Files:** None.

- [ ] **Step 1: SSH to Mac Mini and pull `qwen3.5:9b`**

  ```bash
  ssh sean@192.168.68.200 'ollama pull qwen3.5:9b'
  ```

  (Or run locally on the Mac Mini if Sean is already there.)

- [ ] **Step 2: Pull `qwen3.5:27b` on Mac Mini**

  ```bash
  ssh sean@192.168.68.200 'ollama pull qwen3.5:27b'
  ```

  This is the same model as Tier A — pulling on both hosts is intentional (different num_ctx tunings tested per tier).

- [ ] **Step 3: Pull `gemma4:26b` MoE on Mac Mini**

  ```bash
  ssh sean@192.168.68.200 'ollama pull gemma4:26b'
  ```

  Disambiguate: the user prompt cites `gemma4:26b` as the MoE 3.8B-active variant. Confirm via `ollama show gemma4:26b | head -20` that the parameters reflect MoE (look for "experts" or "active parameters" in the show output). If the tag is the dense 26B variant, look for `gemma4:26b-moe` or substitute the correct tag from `https://ollama.com/library/gemma4`.

- [ ] **Step 4: Build 16K-context Modelfile variants (Tier B is memory-bound, smaller ctx than Tier A)**

  ```bash
  ssh sean@192.168.68.200 'bash -s' <<'REMOTE'
    for tag in qwen3.5:9b qwen3.5:27b gemma4:26b; do
      slug=$(echo "$tag" | tr ':/' '__')
      ollama show "$tag" --modelfile > "/tmp/${slug}-16k.modelfile"
      echo "PARAMETER num_ctx 16384" >> "/tmp/${slug}-16k.modelfile"
      ollama create "${tag%:*}-16k" -f "/tmp/${slug}-16k.modelfile"
    done
  REMOTE
  ```

- [ ] **Step 5: Verify**

  ```bash
  ssh sean@192.168.68.200 'ollama list | grep -E "(qwen3\.5|gemma4).*16k"'
  ```

### Task 3.3: Pull Tier C candidates on the Alienware

**Files:** None.

**Pre-req:** Alienware must be awake (run `wake_alienware.py` from Mac Mini first).

- [ ] **Step 1: Wake Alienware**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk \
    && PYTHONPATH=. .venv/bin/python3 scripts/wake_alienware.py --timeout 180
  ```

- [ ] **Step 2: Pull `devstral:24b-small-2505-q4_K_M` (baseline from Topic 19)**

  Windows:
  ```powershell
  ollama pull devstral:24b-small-2505-q4_K_M
  ```

  Linux:
  ```bash
  ssh sean@192.168.68.201 'ollama pull devstral:24b-small-2505-q4_K_M'
  ```

- [ ] **Step 3: Pull `nemotron3:33b` — expect partial GPU fit on 24GB VRAM**

  ```bash
  ssh sean@192.168.68.201 'ollama pull nemotron3:33b'
  ```

  After pull, run a smoke inference to observe whether Ollama auto-offloads to CPU:

  ```bash
  ssh sean@192.168.68.201 'ollama run nemotron3:33b "Say hello." --verbose 2>&1 | head -40'
  ```

  Look for log lines like `offloaded XX of YY layers to GPU`. If layer count is significantly < total layers, the model runs with CPU/GPU split — expect 5-15 tok/s (vs 40-55 tok/s pure-GPU). Document the layer split in the benchmark report.

  If Ollama refuses to load the model entirely (OOM), fall back to whatever next-smaller quant is in the Ollama library — search `ollama show nemotron3 --help` or check `https://ollama.com/library/nemotron3` for available size tags. If no smaller variant exists, mark `nemotron3:33b` as "rejected — does not fit Tier C hardware" and proceed without it.

- [ ] **Step 4: Build the 32K-context Modelfile variants on Alienware**

  Windows:
  ```powershell
  $tags = @("devstral:24b-small-2505-q4_K_M", "nemotron3:33b")
  foreach ($tag in $tags) {
    $slug = $tag -replace "[:/]", "_"
    ollama show $tag --modelfile | Out-File "$env:TEMP\$slug-32k.modelfile"
    Add-Content "$env:TEMP\$slug-32k.modelfile" "`nPARAMETER num_ctx 32768"
    $base = $tag.Split(":")[0]
    ollama create "$base-32k" -f "$env:TEMP\$slug-32k.modelfile"
  }
  ```

  Linux:
  ```bash
  ssh sean@192.168.68.201 'bash -s' <<'REMOTE'
    for tag in devstral:24b-small-2505-q4_K_M nemotron3:33b; do
      slug=$(echo "$tag" | tr ':/' '__')
      ollama show "$tag" --modelfile > "/tmp/${slug}-32k.modelfile"
      echo "PARAMETER num_ctx 32768" >> "/tmp/${slug}-32k.modelfile"
      base="${tag%%:*}"
      ollama create "${base}-32k" -f "/tmp/${slug}-32k.modelfile"
    done
  REMOTE
  ```

- [ ] **Step 5: Verify**

  ```bash
  ssh sean@192.168.68.201 'ollama list | grep -- -32k'
  ```

### Task 3.4: Rollback inventory — record what was pulled where

**Files:**
- Modify: `agents-sdk/benchmarks/topic_20/README.md` (append a section)

- [ ] **Step 1: Append a "Pulled models" table to the README**

  ```markdown
  ## Pulled models (state as of $(date +%Y-%m-%d))

  | Tier | Host | Base tag | Custom variant | Modelfile num_ctx | Disk |
  |---|---|---|---|---|---|
  | A | MBP | qwen3.5:27b | qwen3.5-32k | 32768 | 17GB |
  | A | MBP | qwen3.5:35b | qwen3.5-32k | 32768 | 24GB |
  | A | MBP | qwen3.6:35b | qwen3.6-32k | 32768 | 24GB |
  | A | MBP | qwen3-coder:30b | qwen3-coder-32k | 32768 | 18GB |
  | B | Mac Mini | qwen3.5:9b | qwen3.5-16k | 16384 | 6.6GB |
  | B | Mac Mini | qwen3.5:27b | qwen3.5-16k | 16384 | 17GB |
  | B | Mac Mini | gemma4:26b | gemma4-16k | 16384 | 18GB |
  | C | Alienware | devstral:24b-small-2505-q4_K_M | devstral-32k | 32768 | 14GB |
  | C | Alienware | nemotron3:33b | nemotron3-32k | 32768 | 28GB |

  ## Rollback (per-host)

  Remove all pulled candidates in one go:

      # MBP
      for tag in qwen3.5:27b qwen3.5:35b qwen3.6:35b qwen3-coder:30b \
                 qwen3.5-32k qwen3.6-32k qwen3-coder-32k; do
        ollama rm "$tag" || true
      done

      # Mac Mini
      ssh sean@192.168.68.200 'for tag in qwen3.5:9b qwen3.5:27b gemma4:26b \
                 qwen3.5-16k gemma4-16k; do ollama rm "$tag" || true; done'

      # Alienware (after wake)
      ssh sean@192.168.68.201 'for tag in devstral:24b-small-2505-q4_K_M nemotron3:33b \
                 devstral-32k nemotron3-32k; do ollama rm "$tag" || true; done'
  ```

- [ ] **Step 2: Commit**

  ```bash
  git add agents-sdk/benchmarks/topic_20/README.md
  git commit -m "docs(benchmarks): topic_20 pulled-models inventory + rollback"
  ```

---

## Phase 4 — Run the benchmark sweep

Each tier's sweep is one task. Total wall time per sweep: ~30-60 min per model.

### Task 4.1: Tier A sweep on MBP

**Files:**
- Modifies (appends to): `agents-sdk/benchmarks/topic_20/results/*.jsonl`

- [ ] **Step 1: In one terminal on MBP, start the RSS sampler**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain
  ./agents-sdk/scripts/sample_ollama_rss.sh mbp 7200  # 2-hour budget
  ```

- [ ] **Step 2: In a second terminal, run the benchmark for each Tier A candidate sequentially**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
  for variant in qwen3.5-32k qwen3.6-32k qwen3-coder-32k; do
    [ -n "$(ollama list | grep -F "$variant")" ] || { echo "skip $variant — not pulled"; continue; }
    PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
      --model "$variant" \
      --host http://localhost:11434 \
      --tier A \
      --num-ctx 32768
  done
  ```

  **Also benchmark the current production model** (Qwen3-14B running on LM Studio at port 1234) — separate harness invocation because LM Studio's OpenAI-compat endpoint differs from Ollama's `/api/chat`. **Decision: skip LM Studio baseline here.** Rationale: LM Studio is a different runtime; comparing across runtimes confounds the benchmark. Instead, also pull `qwen3:14b` (the Ollama variant — verify tag exists at `https://ollama.com/library/qwen3`) onto the MBP via `ollama pull qwen3:14b`, create a `qwen3-14b-32k` variant, and benchmark THAT as the apples-to-apples baseline. Add this pull to Task 3.1 retroactively (or here):

  ```bash
  ollama pull qwen3:14b
  ollama show qwen3:14b --modelfile > /tmp/q3-14b.modelfile
  echo "PARAMETER num_ctx 32768" >> /tmp/q3-14b.modelfile
  ollama create qwen3-14b-32k -f /tmp/q3-14b.modelfile
  PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
    --model qwen3-14b-32k --host http://localhost:11434 --tier A --num-ctx 32768
  ```

- [ ] **Step 3: Stop the RSS sampler** (Ctrl-C in the first terminal).

- [ ] **Step 4: Verify results landed**

  ```bash
  ls -la agents-sdk/benchmarks/topic_20/results/*tierA*$(date +%Y-%m-%d)*
  ```

  Expected: 4 JSONL files (one per variant) plus 1 RSS CSV.

- [ ] **Step 5: Commit results**

  ```bash
  git add agents-sdk/benchmarks/topic_20/results/*.jsonl agents-sdk/benchmarks/topic_20/results/*.csv
  git commit -m "data(benchmarks): topic_20 Tier A sweep results"
  ```

### Task 4.2: Tier B sweep on Mac Mini

**Files:** Same pattern as Task 4.1.

- [ ] **Step 1: Start RSS sampler on Mac Mini**

  ```bash
  ssh sean@192.168.68.200 'bash -lc "cd /path/to/code-brain && ./agents-sdk/scripts/sample_ollama_rss.sh macmini 7200"' &
  ```

- [ ] **Step 2: From Mac Mini directly (avoids LAN serialization noise), run the sweep**

  ```bash
  ssh sean@192.168.68.200
  cd /path/to/code-brain/agents-sdk
  for variant in qwen3.5-16k gemma4-16k; do  # qwen3.5-16k covers both 9b and 27b — adjust per actual variant names
    PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
      --model "$variant" \
      --host http://localhost:11434 \
      --tier B \
      --num-ctx 16384
  done
  # Also benchmark the current production gemma4:e4b as the baseline
  PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
    --model gemma4:e4b --host http://localhost:11434 --tier B --num-ctx 16384
  ```

  **Note on variant naming:** Task 3.2 Step 4 created variants `qwen3.5-16k` and `gemma4-16k` per the `${tag%:*}-16k` template — but pulling BOTH `qwen3.5:9b` and `qwen3.5:27b` writes to the SAME variant name (`qwen3.5-16k`). Fix the Task 3.2 loop to disambiguate:

  ```bash
  # On Mac Mini, post-fix the variant names:
  ollama rm qwen3.5-16k 2>/dev/null || true
  for tag in qwen3.5:9b qwen3.5:27b; do
    slug=$(echo "$tag" | tr ':/' '__')
    ollama show "$tag" --modelfile > "/tmp/${slug}-16k.modelfile"
    echo "PARAMETER num_ctx 16384" >> "/tmp/${slug}-16k.modelfile"
    # Distinct name per size
    ollama create "${slug}-16k" -f "/tmp/${slug}-16k.modelfile"
  done
  # Then benchmark each independently:
  for variant in qwen3.5__9b-16k qwen3.5__27b-16k gemma4__26b-16k; do
    PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
      --model "$variant" --host http://localhost:11434 --tier B --num-ctx 16384
  done
  ```

- [ ] **Step 3: Commit results** (Mac Mini repo, then sync via existing vault sync owner — i.e., normal `git push` from Mac Mini side after benchmark)

### Task 4.3: Tier C sweep on Alienware

**Files:** Same pattern.

- [ ] **Step 1: From Mac Mini, wake the Alienware**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk \
    && PYTHONPATH=. .venv/bin/python3 scripts/wake_alienware.py --timeout 180
  ```

- [ ] **Step 2: From Mac Mini, drive the benchmark against the Alienware's Ollama**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
  for variant in devstral-32k nemotron3-32k; do
    PYTHONPATH=. .venv/bin/python3 scripts/benchmark_ollama_model.py \
      --model "$variant" \
      --host http://192.168.68.201:11434 \
      --tier C \
      --num-ctx 32768
  done
  ```

- [ ] **Step 3: Sleep the Alienware once the sweep completes**

  ```bash
  PYTHONPATH=. .venv/bin/python3 scripts/sleep_alienware.py --user <USER>
  ```

- [ ] **Step 4: Commit results from Mac Mini side**

### Task 4.4: Sanity-check raw results before synthesis

**Files:** None.

- [ ] **Step 1: Inspect each result file for completeness**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk/benchmarks/topic_20/results
  for f in *.jsonl; do
    echo "=== $f ==="
    .venv/bin/python3 -c "
  import json, sys
  by_kind = {}
  for line in open('$f'):
      rec = json.loads(line)
      by_kind[rec['kind']] = by_kind.get(rec['kind'], 0) + 1
  print(by_kind)
  "
  done
  ```

  Expected per file (for each model):
  - `tool_call`: 20
  - `throughput`: 3
  - `needle`: 5 (or 1 `skipped_reason` if num_ctx < 32768)
  - `pi_gotcha`: 5

  Total records per file: ~33. If any file has zero of any kind, the benchmark for that model needs to be re-run.

- [ ] **Step 2: If any model has missing dimensions, re-run with `--skip` flags excluding only the missing kinds**

---

## Phase 5 — Synthesize results into the Topic 20 report

### Task 5.1: Aggregate raw JSONL into per-tier scorecards (one-off Python in the report writeup)

**Files:**
- Create: `agents-sdk/benchmarks/topic_20/aggregate.py`

- [ ] **Step 1: Write the aggregator**

  ```python
  # agents-sdk/benchmarks/topic_20/aggregate.py
  """Aggregate raw JSONL benchmark results into per-(model, tier) scorecards.

  Reads every *.jsonl in benchmarks/topic_20/results/, groups by (model, tier),
  and writes a single markdown table per tier to stdout. Designed to be
  imported into the synthesis report.
  """
  from __future__ import annotations

  import json
  from collections import defaultdict
  from pathlib import Path
  from statistics import mean, stdev


  RESULTS_DIR = Path(__file__).parent / "results"


  def load_records() -> list[dict]:
      records = []
      for jl in RESULTS_DIR.glob("*.jsonl"):
          for line in jl.open():
              line = line.strip()
              if not line:
                  continue
              try:
                  records.append(json.loads(line))
              except json.JSONDecodeError:
                  continue
      return records


  def aggregate(records: list[dict]) -> dict:
      """Group by (model, tier) → dimension summaries."""
      grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
      for r in records:
          key = (r.get("model", "?"), r.get("tier", "?") if r.get("tier") else _infer_tier(r))
          grouped[key].append(r)

      summary = {}
      for (model, tier), recs in grouped.items():
          tcs = [r for r in recs if r.get("kind") == "tool_call"]
          tps = [r for r in recs if r.get("kind") == "throughput"]
          nls = [r for r in recs if r.get("kind") == "needle" and not r.get("skipped_reason")]
          pis = [r for r in recs if r.get("kind") == "pi_gotcha"]

          tool_pass = sum(1 for r in tcs if r.get("schema_match"))
          ollama_tps_vals = [r["ollama_tps"] for r in tps if r.get("ollama_tps")]
          needle_pass = sum(1 for r in nls if r.get("recalled"))
          pi_affected = sum(1 for r in pis if r.get("affected"))

          summary[(model, tier)] = {
              "tool_call_pass_rate": (tool_pass / len(tcs)) if tcs else None,
              "tool_call_n": len(tcs),
              "ollama_tps_mean": mean(ollama_tps_vals) if ollama_tps_vals else None,
              "ollama_tps_stdev": stdev(ollama_tps_vals) if len(ollama_tps_vals) > 1 else 0.0,
              "needle_recall": (needle_pass, len(nls)) if nls else (None, 0),
              "pi_gotchas_affected": pi_affected,
              "pi_gotchas_total": len(pis),
          }
      return summary


  def _infer_tier(record: dict) -> str:
      """Some records may lack a tier field — infer from model name conventions."""
      model = (record.get("model") or "").lower()
      if any(s in model for s in ["e4b", "9b", "gemma4__26b", "gemma4-26b"]):
          return "B"
      if any(s in model for s in ["nemotron", "devstral"]):
          return "C"
      return "A"


  def print_markdown(summary: dict) -> None:
      for tier in ("A", "B", "C"):
          print(f"\n## Tier {tier} scorecard\n")
          print("| Model | Tool-call pass | Tok/s mean ± stdev | Needle recall (28K/32K) | Pi gotchas affected |")
          print("|---|---|---|---|---|")
          for (model, t), s in sorted(summary.items()):
              if t != tier:
                  continue
              tc = f"{s['tool_call_pass_rate']:.0%} ({s['tool_call_n']})" if s['tool_call_pass_rate'] is not None else "—"
              tps = f"{s['ollama_tps_mean']:.1f} ± {s['ollama_tps_stdev']:.1f}" if s['ollama_tps_mean'] else "—"
              nr = f"{s['needle_recall'][0]}/{s['needle_recall'][1]}" if s['needle_recall'][1] else "—"
              pi = f"{s['pi_gotchas_affected']}/{s['pi_gotchas_total']}"
              print(f"| `{model}` | {tc} | {tps} | {nr} | {pi} |")


  if __name__ == "__main__":
      records = load_records()
      summary = aggregate(records)
      print_markdown(summary)
  ```

- [ ] **Step 2: Run it and capture the output**

  ```bash
  cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
  .venv/bin/python3 benchmarks/topic_20/aggregate.py
  ```

  Expected: three markdown tables (Tier A, B, C). Save the output verbatim — it will paste into the Topic 20 report in Task 5.2.

- [ ] **Step 3: Commit the aggregator**

  ```bash
  git add agents-sdk/benchmarks/topic_20/aggregate.py
  git commit -m "feat(benchmarks): topic_20 result aggregator"
  ```

### Task 5.2: Write the Topic 20 synthesis report

**Files:**
- Create: `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`

- [ ] **Step 1: Write the report with frontmatter matching the existing research-report style**

  ```markdown
  ---
  type: research-report
  date: 2026-05-21
  status: complete
  question: "Topic 20 — Benchmark 6 candidate Ollama models against current production fleet and Topic 19 baselines on Sean's 3-tier hardware (MBP / Mac Mini / Alienware), and stand up Alienware Tier C wake-on-LAN."
  topic: 20
  supersedes:
    - "[[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]"
  sources:
    - "agents-sdk/benchmarks/topic_20/results/*.jsonl"
    - "agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md"
  tags: [research, synthesis, ollama, fleet, hardware-tier, benchmark, alienware-tier-c]
  ---

  # Topic 20 — Fleet Model Refresh Benchmarks (2026-05-21)

  ## TL;DR — adoption decisions per tier

  | Tier | Hardware | Current production | Recommended | Action |
  |---|---|---|---|---|
  | A | MBP M4 Max | Qwen3-14B (LM Studio) | <fill from data> | <migrate / hold / reject> |
  | B | Mac Mini 24GB | gemma4:e4b | <fill from data> | <migrate / hold / reject> |
  | C | Alienware 4090 | — (unused) | <fill from data> | <newly adopted as Tier C> |

  ## Benchmark dimensions

  Each model was scored on 6 dimensions (full schema in
  `agents-sdk/benchmarks/topic_20/README.md`):

  1. **Tool-call JSON validity** (% of 20 prompts producing correct schema)
  2. **Decode tokens/sec** (mean of 3 runs at fixed 1024-token output)
  3. **Peak Ollama-server RSS** (from `scripts/sample_ollama_rss.sh`)
  4. **Agentic-loop reliability** (10 multi-step Pi-style sessions — manual scoring)
  5. **32K needle recall** (5 runs at 28K position)
  6. **Pi gotcha exposure** (5 binary probes)

  ## Decision thresholds (set 2026-05-21 before benchmark execution)

  | Dimension | Adoption-viable | Reject-outright |
  |---|---|---|
  | Tool-call pass rate | ≥90% | <80% |
  | Tok/s on tier | Within 20% of baseline on that tier | <50% of baseline |
  | Agentic-loop reliability | ≥8/10 | <6/10 |
  | Needle recall | ≥4/5 | ≤2/5 |
  | Pi gotchas affected | ≤1 of 3 measured | ≥3 of 3 measured |

  A model must clear every "adoption-viable" gate to be recommended.

  <PASTE AGGREGATOR OUTPUT HERE>

  ## Per-tier adoption analysis

  ### Tier A (M4 Max MBP)

  <fill — which candidate wins and by how much; what does it replace; what's
  the migration cost; what's the rollback>

  ### Tier B (Mac Mini 24GB)

  <fill>

  ### Tier C (Alienware 4090)

  <fill — first time this tier joins the fleet; reference the WoL decision record>

  ## Per-agent adoption recommendation

  | Agent | Current model | Recommended | Notes |
  |---|---|---|---|
  | `vault_synthesizer` | Qwen3-14B @ MBP | <fill> | <fill> |
  | `knowledge_lint` Tier 2 | Qwen3-14B @ MBP | <fill> | <fill> |
  | `deep_researcher` LDR loop | qwen3-14b-research @ Mac Mini | <fill> | <fill> |
  | `meta_agent` | gemma4:e4b @ Mac Mini | <fill> | <fill> |
  | `flush.py` | gemma4:e4b @ Mac Mini | <fill> | <fill> |
  | `inbox_triage` task | gemma4:e4b @ Mac Mini | <fill> | <fill> |
  | `job_feed` scoring | Qwen3-14B @ MBP | <fill> | <fill> |
  | (new) Tier C batch agent | — | <fill or "no Tier C adoption yet"> | <fill> |

  ## What changed from the Topic 19 synthesis

  - Topic 19 §Correction (2026-05-21) flagged that the prior synthesis
    method had a bias against newer locally-runnable models. This
    benchmark addresses that bias directly with hardware-grounded data.
  - <Add 2-4 specific findings: e.g., "qwen3.5:27b was X% faster than
    qwen3-coder:30b on Tier A with identical tool-call accuracy" or
    "nemotron3:33b's CPU offload penalty made it non-competitive on Tier
    C — devstral baseline holds.">

  ## Open questions deferred to Topic 21+ or skipped

  - <Any candidate that needs more soak time before adoption — e.g.,
    qwen3.6:35b's 3-week age + limited published benchmarks may warrant
    a 4-week soak before adoption.>
  - <Anything that surfaced during benchmarks but doesn't block this
    decision — e.g., thinking-mode disable on Qwen 3.5 wasn't testable
    via PARAMETER think false; needs option-pass.>

  ## Rollback

  Any adoption-driven config change is reversible by reverting the commit
  that landed it. The Modelfile variants on each host can be removed with
  `ollama rm <variant>`. The Alienware Tier C standup is reversible per
  the decision record's Rollback section.

  ## Sources

  - Topic 19 synthesis (superseded): [[2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]
  - Topic 16 Pi+Ollama integration: [[2026-05-21-topic-16-pi-ollama-integration-chatgpt-manual]]
  - Alienware wake architecture: [`agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md`](../../../agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md)
  - Raw benchmark JSONL: `agents-sdk/benchmarks/topic_20/results/*.jsonl`
  - Benchmark harness: `agents-sdk/scripts/benchmark_ollama_model.py`
  ```

- [ ] **Step 2: Fill in every `<fill>` placeholder with data from the aggregator output and the raw JSONL — no `<fill>` may remain in the committed file**

- [ ] **Step 3: Commit the report**

  ```bash
  git add vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md
  git commit -m "data(research): topic_20 fleet model refresh benchmarks report"
  ```

  (The shell-level auto-commit hook will re-commit any vault changes per Issue #22 ownership — that's expected and fine.)

### Task 5.3: Mark the Topic 19 synthesis frontmatter as `superseded`

**Files:**
- Modify: `vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md` (line 4)

- [ ] **Step 1: Edit the frontmatter**

  Change line 4 from `status: superseded-pending-benchmarks` to `status: superseded` and add `superseded_by: "[[2026-05-21-topic-20-fleet-model-refresh-benchmarks]]"`.

- [ ] **Step 2: Commit**

  ```bash
  git add vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md
  git commit -m "docs(research): mark topic 19 superseded by topic 20 benchmarks"
  ```

---

## Phase 6 — Adoption (gated by Phase 5 findings)

This phase only executes if Phase 5 identified at least one model as adoption-viable per its tier. If no winner emerges (e.g., all candidates fall below decision thresholds), skip Phase 6 entirely and log "no adoption" in the Status Tracker.

### Task 6.1: Per-tier soak pilot (1 week)

For each tier with a winner, migrate ONE low-stakes agent's routing to the new model and soak for 7 days before broader rollout.

**Recommended pilot agents per tier (lowest blast radius first):**

| Tier | Pilot agent | Why this one |
|---|---|---|
| A | `knowledge_lint` Tier 2 | Sunday-only, advisory output, easy to compare against prior weeks |
| B | `meta_agent` (08:45 daily) | Read-only fleet summary; low downstream coupling |
| C | (new) a manually-triggered batch codegen scratchpad — NOT a launchd agent | Tier C is brand new; don't bind a critical agent to it on day one |

- [ ] **Step 1: Update `agents-sdk/config.toml` for the pilot agent**

  For Tier B `meta_agent` (example):
  ```toml
  [routing.task_map]
  # 2026-05-XX: meta_agent piloting <new-tier-B-winner> per Topic 20 benchmark.
  # Rollback: revert this line. Pilot soak ends 2026-06-XX.
  meta_agent_task = { model = "<new-tier-B-winner>", machine = "mac_mini" }
  ```

  Update `agents-sdk/agents/meta_agent.py` (or wherever it resolves its model) to read from this key. If `meta_agent.py` currently hardcodes `gemma4:e4b`, change to reading `routing.task_map.meta_agent_task` via `lib/config.py`.

- [ ] **Step 2: Commit with rollback breadcrumb**

  ```bash
  git add agents-sdk/config.toml
  git commit -m "feat(routing): pilot Tier B <winner> on meta_agent (topic_20 soak)"
  ```

- [ ] **Step 3: Soak 7 days. Monitor:**
  - `vault/90_system/agent-logs/agent-run-history.csv` — no new error states
  - `vault/health/<agent>-manifest-*.json` — output quality matches prior week
  - Per CLAUDE.md auto-memory feedback `feedback_synth_verify_against_median_not_best.md` — sample the MEDIAN output, not the best one

- [ ] **Step 4: After 7 days, log soak outcome in the Topic 20 report**

  Add a "Soak outcome" section at the bottom of the report. Either: (a) confirmed-stable → broader rollout in Task 6.2, or (b) regression detected → rollback in Task 7.x.

### Task 6.2: Broader rollout (only if Task 6.1 passes)

**Files:** `agents-sdk/config.toml` (additional task_map entries), possibly `CLAUDE.md` (agent inventory table).

- [ ] **Step 1: Migrate remaining agents on that tier one at a time, with a 24h wait between each migration**

  Example sequence for Tier B with `gemma4:26b` winning:
  1. Day 1: `flush.py` → new model
  2. Day 2: `inbox_triage` (if Path B has shipped — otherwise skip)
  3. Day 3: any remaining Tier B caller

  Each migration is a config-only edit. Commit per-step with the rollback breadcrumb pattern from Task 6.1 Step 2.

- [ ] **Step 2: Update `CLAUDE.md` agent inventory table**

  In the "Agent inventory" table (CLAUDE.md ~line 107-120), update the "Skills/Model" column for each migrated agent. Bump the version section if appropriate per CHANGELOG conventions.

- [ ] **Step 3: Add a CHANGELOG.md entry**

  Per CLAUDE.md "When Modifying" rule:
  ```markdown
  ## vX.Y.Z (2026-XX-XX) — Topic 20 fleet refresh

  - Migrated Tier B agents (`meta_agent`, `flush.py`, `inbox_triage`) from
    `gemma4:e4b` to `<winner>` per Topic 20 benchmarks. Quality delta:
    +X.Xpp. Soak: 7 days, zero regressions. Rollback: revert <commit-sha>.
  - Adopted Alienware as Tier C agent host via on-demand WoL (decision
    record: agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md).
  - Topic 19 synthesis superseded.
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add CLAUDE.md CHANGELOG.md
  git commit -m "docs: topic 20 fleet refresh — CLAUDE.md + CHANGELOG"
  ```

---

## Phase 7 — Rollback procedures (per-step)

If any Phase 6 migration causes a regression, rollback is one of:

| Symptom | Rollback step |
|---|---|
| Tool-call quality drops on a migrated agent | `git revert <migration commit>` — restores prior `[routing.task_map]` entry |
| Wake-on-LAN flakiness — Alienware doesn't wake reliably | Flip to Pattern B per decision record §Rollback (Task 2.7) |
| New model OOMs the Mac Mini under real load | `ollama rm <variant>`; `git revert` the migration commit |
| nemotron3 CPU-offload too slow for Tier C tasks | Drop nemotron3 from `routing.task_map`; devstral stays |
| Alienware power cost higher than projected | Increase idle-sleep aggressiveness (Task 2.4); or fully deprovision Tier C via decision record §Rollback |
| Topic 20 report shows no winner on any tier | No-op; commit the report with "no adoption" outcome; Topic 19 baselines remain in production |

**Total Topic 20 rollback** (remove all artifacts of this plan):

1. `git revert` all commits made under this plan in reverse chronological order. Vault sync hook absorbs the vault-side reverts.
2. On each host, run the per-host `ollama rm` block from Task 3.4's rollback section.
3. Power the Alienware off and disable the BIOS WoL setting (Task 2.1 Step 1).
4. Remove `agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md` (or keep as historical context — preferred).

---

## Phase 8 — Done-when checklist

The plan is "done" when:

- [ ] Phase 0 verification all green (or any red item is documented as "intentional deviation" in Status Tracker)
- [ ] All scorer + WoL tests pass: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_benchmark_scorers.py tests/test_wol.py -v`
- [ ] All 9 model variants pulled (or explicitly skipped with documented reason)
- [ ] All 9 benchmark JSONL files present in `agents-sdk/benchmarks/topic_20/results/` for the date this plan executes
- [ ] Alienware WoL soak: ≥9/10 cycles successful within 24 hours
- [ ] `agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md` committed with all `<fill>` placeholders resolved
- [ ] `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md` committed with all `<fill>` placeholders resolved
- [ ] Topic 19 synthesis frontmatter updated to `status: superseded`
- [ ] If any adoption happened: 7-day pilot soak logged in the report + CLAUDE.md/CHANGELOG updated
- [ ] If no adoption: report explicitly logs "no adoption" with reasoning
- [ ] `python3 scripts/validate.py` passes (CLAUDE.md "When Modifying" rule)

---

## Self-review notes (writing-plans skill checklist, run 2026-05-21)

**1. Spec coverage:**
- ✅ Pull 4 candidate models on correct tiers — Phase 3 covers all 6 plus baselines plus the user-requested 4
- ✅ Run fixed benchmark suite vs current production — Phase 4 against Qwen3-14B (via qwen3:14b Ollama variant per Task 4.1 Step 2), gemma4:e4b, qwen3-coder:30b, devstral baselines
- ✅ Wake-on-LAN architecture — Phase 2 + decision record
- ✅ Capture results in `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md` — Task 5.2
- ✅ Decision recommendations per tier — Task 5.2 report sections
- ✅ Wake architecture decision record at `agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md` — Task 2.7
- ✅ `agents-sdk/scripts/benchmark_ollama_model.py` — Task 1.11
- ✅ Config changes documented — Phase 6 + scope guard
- ✅ Rollback procedure — Phase 7

**2. Placeholder scan:** all `<fill>` markers in the Topic 20 report are intentional (must be replaced with actual data when the plan executes); all `<USER>` placeholders are SSH-username fills that depend on Sean's confirmation in Task 0.1. The decision record's soak table has empty cells deliberately (filled by Task 2.5 evidence). No "TBD" / "implement later" / "TODO" in actionable code.

**3. Type consistency:**
- `score_tool_call_json(output, schema)` — used identically in `tests/test_benchmark_scorers.py` and `scripts/benchmark_ollama_model.py`. ✓
- `compute_tokens_per_second(token_count, elapsed_seconds)` — same arg names in both files. ✓
- `score_needle_recall(response, needle)` — same. ✓
- `score_pi_gotcha_compat(response_text, gotcha)` — same. ✓
- `parse_mac(mac)` / `build_magic_packet(mac)` / `send_magic_packet(mac, ...)` — consistent. ✓
- `probe_until_ready(host, port, timeout_total_secs, interval_secs)` — used in `wake_alienware.py` with positional + kw forms matching the def. ✓

---

## Status Tracker

(Fill during execution. Don't commit empty rows; commit once Phase 0 is complete and again after each major phase.)

### Phase 0 answers

- **Alienware OS:** Windows 11
- **Alienware power state behavior:** (sleeps after X min / hibernates / stays on)
- **BIOS WoL previously enabled?:** (yes / no / unknown)
- **Alienware Ollama version:** (semver)
- **Alienware current models:** (output of `ollama list`)
- **MBP unified memory:** (X GB)
- **Decision on 35B Tier A candidates given memory:** (proceed / skip)
- **Disk free MBP / Mac Mini / Alienware:** (X / Y / Z GB)
- **Deco AP isolation:** (on / off)
- **MBP currently reachable?:** (yes / no / asleep)

### Phase 1 progress

- [ ] Harness scaffold (Task 1.1)
- [ ] Scorer tests + impl (1.2, 1.3)
- [ ] WoL tests + impl (1.4, 1.5)
- [ ] wake/sleep scripts (1.6, 1.7)
- [ ] Tool-call prompts (1.8)
- [ ] Agentic-loop prompts (1.9)
- [ ] Needle haystack generator (1.10)
- [ ] Main runner (1.11)
- [ ] RSS sampler (1.12)

### Phase 2 progress

- [ ] BIOS + OS WoL enabled (2.1)
- [ ] Magic packet wake verified (2.2)
- [ ] Ollama auto-start configured on Alienware (2.3)
- [ ] Idle-sleep policy set (2.4)
- [ ] 10-cycle soak (2.5) — record X/10 successes here:
- [ ] SSH sleep verified (2.6)
- [ ] Decision record written (2.7)

### Phase 3 progress

- [ ] MBP pulls (3.1)
- [ ] Mac Mini pulls (3.2)
- [ ] Alienware pulls (3.3)
- [ ] Inventory + rollback documented (3.4)

### Phase 4 progress

- [ ] Tier A sweep (4.1)
- [ ] Tier B sweep (4.2)
- [ ] Tier C sweep (4.3)
- [ ] Sanity-checked (4.4)

### Phase 5 progress

- [ ] Aggregator (5.1)
- [ ] Topic 20 report written (5.2)
- [ ] Topic 19 marked superseded (5.3)

### Phase 6 progress (only if winners exist)

- [ ] Pilot soak started — agent: ____, model: ____, start date: ____
- [ ] Pilot soak passed
- [ ] Broader rollout
- [ ] CLAUDE.md + CHANGELOG updated

### Final done-when

- [ ] All Phase 8 checklist items green
- [ ] `python3 scripts/validate.py` passes
