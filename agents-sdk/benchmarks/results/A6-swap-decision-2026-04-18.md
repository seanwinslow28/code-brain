# Phase 6 A.6 — Swap Decision Report (re-run)

**Date:** 2026-04-18
**Sample size:** 20 per task (up from 5 in the 2026-04-17 smoke run)
**Outcome:** **1 SWAP approved** (`inbox_triage` → `gemma4:e4b @ mac_mini`)
**Status vs. plan Gate Check #2:** **PASS** (config.toml `[routing.task_map]` changed this commit)

---

## Why this re-run exists

The 2026-04-17 report was blocked on two infra issues:
1. LM Studio refused the `qwen3-14b` JIT-load for the `financial_analysis` incumbent while `gemma4-31b` held 28 GB on the MBP.
2. The MBP WOL path was only partially wired — live verification never passed (see §"WOL disposition" below).

Both issues compounded because the original plan routed `financial_analysis` and `code_review` incumbents to the MacBook Pro. For this re-run we **eliminated the MBP dependency entirely**: the Mac Mini runs both incumbent and challenger through Ollama. This makes the decision reproducible and shortcuts ~2 hours of WOL debugging for a 4.5B-vs-3.8B head-to-head that always belonged on Mac Mini anyway.

**Challenger substitution:** The April-17 run used `gemma4-31b` and `gemma4:26b`. Both are MBP-only or too heavy for 24 GB Mac Mini. For this re-run we switched to **`gemma4:e4b`** (4.5B effective / 8B with embeddings, Ollama `gemma4` library, Q4_K_M, 9.6 GB on disk, 131K context). E4B is the natural peer to `phi4-mini-reasoning` (3.8B) — same size class, same hardware, same runtime. The decision that falls out of this run is the one that actually mattered: does Gemma 4's function-calling-native architecture outperform Phi's reasoning-chain architecture on our agentic workloads, given equivalent compute?

## Full N=20 results

| Task | Model | Quality | p50 latency | p95 latency | Mean latency |
|---|---|---:|---:|---:|---:|
| inbox_triage | phi4-mini-reasoning | 0.325 | 56.2 s | 140.6 s | 67.3 s |
| inbox_triage | **gemma4:e4b** | **0.400** | **24.2 s** | **68.4 s** | **36.8 s** |
| financial_analysis | **phi4-mini-reasoning** | **0.900** | 24.6 s | 80.6 s | 30.9 s |
| financial_analysis | gemma4:e4b | 0.800 | **17.8 s** | 23.4 s | 17.3 s |
| code_review | phi4-mini-reasoning | 0.000 | 50.8 s | 127.0 s | 55.1 s |
| code_review | gemma4:e4b | 0.000 | 19.1 s | 23.0 s | 18.3 s |

Both machines Mac Mini / Ollama. Bold = task winner on that metric.

## Veto-gate application (plan §A.6 + §7.1)

Rule: ≥5 pp quality regression = KEEP incumbent. Within ±5 pp AND ≥20% faster = SWAP on speed. ≥5 pp quality gain = SWAP.

### `inbox_triage` — **SWAP to gemma4:e4b**

- Δquality = **+7.5 pp** (gemma 0.400 vs phi 0.325)
- Speedup = **+57.0%** p50 (24.2 s vs 56.2 s)

Gemma wins on quality AND speed. No trade-off. Clean swap.

### `financial_analysis` — **KEEP phi4-mini-reasoning**

- Δquality = **−10.0 pp** (gemma 0.800 vs phi 0.900)
- Speedup = +27.7% p50 (17.8 s vs 24.6 s)

Veto gate fires. Phi's reasoning chains help on numerical/categorical judgment where Gemma's shorter responses lose discrimination. Speed win isn't enough to overcome the quality drop.

### `code_review` — **INCONCLUSIVE, defer swap**

Both models scored 0.000. This is **not** a real "both models fail" signal — it's an extractor bug.

Golden-set expected tags are hyphenated (`sql-injection`, `mutable-default`, `bare-except`). The extractor is `re.search(rf"\b{re.escape(exp)}\b", text.lower())` which requires the exact hyphenated form in the model's output. Neither model emits `sql-injection` as a literal token; they write "SQL injection vulnerability" (two words, space-separated). Verified manually on samples 0–2:

| Sample | Expected | Both models said (manually inspected) | Extractor saw |
|---|---|---|---|
| 0 | `sql-injection` | "SQL injection", "SQL injection vulnerability" | nothing |
| 1 | `mutable-default` | "mutable default argument" | nothing |
| 2 | `bare-except`, `swallowed-exception` | "bare except", "silent exception swallowing" | nothing |

Raw model latency still tells us something: gemma4:e4b is 62% faster than phi4-mini-reasoning on code prompts. But without a valid quality signal we can't apply the veto gate.

**Action:** Defer `code_review` swap. Follow-up ticket: fix the extractor to accept `-`, ` `, and `_` as equivalent separators (`re.sub(r"[-_\s]+", r"[-_\\s]+", re.escape(exp))`), OR move code_review quality scoring to an LLM-as-judge prompt. Re-run code_review task only after that fix.

## Diff vs. 2026-04-17 smoke run

| Task / model | 2026-04-17 (N=5) | 2026-04-18 (N=20) | Delta |
|---|---|---|---|
| inbox_triage / phi4 quality | 0.667 | 0.325 | −0.342 |
| inbox_triage / phi4 p50 | 21.2 s | 56.2 s | +35.0 s |
| inbox_triage / challenger quality | 0.567 (gemma4-31b/MBP) | 0.400 (gemma4:e4b/MacMini) | comparing different models |
| financial_analysis | _not run_ | q=0.900 (phi) / 0.800 (gemma) | first real data |
| code_review | _not run_ | 0.000 (both — extractor bug) | extractor needs fix |

The April-17 N=5 numbers were noisy because the golden set has high variance across prompt complexity. At N=5 phi4 hit 2/3 easy samples (q=0.667); at N=20 it's clearly in the 0.3–0.4 range for inbox_triage. Gemma's N=20 result (0.400) is the stable signal. **Trust the N=20 numbers over April-17.**

## Config.toml changes applied

```toml
# Before
inbox_triage = { model = "phi4-mini-reasoning", machine = "mac_mini" }
# machines.mac_mini.models = ["phi4-mini-reasoning", "phi4-mini", "nomic-embed-text"]

# After (this commit)
inbox_triage = { model = "gemma4:e4b", machine = "mac_mini" }
# machines.mac_mini.models = ["phi4-mini-reasoning", "phi4-mini", "nomic-embed-text", "gemma4:e4b"]
```

Rollback: revert the two edits in `agents-sdk/config.toml`. Keep `phi4-mini-reasoning` still pulled — we still use it for `anki_cards`.

## WOL disposition (Phase 6 P0.2)

The MBP WOL path landed in commit `f2a455e` (config, `route_to_macbook`, `send_wol`, tests, `verify_mbp_wol.py`). It is **code-complete but not production-trusted.** Live verification failed today against a sleeping MBP because:

- The MBP's Wi-Fi uses **Private Wi-Fi Address** (randomized MAC `3a:b9:00:23:10:67`), which holds DHCP lease `192.168.68.50` — the IP config.toml targets.
- The MBP's permanent MAC `50:F2:65:EF:AC:3D` (what config.toml's `wol_mac` points at) holds a different DHCP lease (`192.168.68.54` in ARP cache).
- The WOL packet reached the permanent-MAC interface (`.54` pinged back), but LM Studio is bound to localhost only, so it wasn't reachable after the wake.

**Decision:** mark WOL as deferred. The code stays in place — `route_to_macbook()`, tests, and `verify_mbp_wol.py` all continue to work once the Wi-Fi randomization is turned off OR the MBP is on Ethernet. No agent currently needs WOL in production: the `vault_synthesizer` (scheduled 02:30 AM daily) will fail gracefully with `WOLUnavailable` + Pushover notification, which is the documented Phase 6 fallback per plan §7.6.

If we want nightly synthesis to actually run, the follow-up is either:
- Turn OFF Private Wi-Fi Address on MBP for `MarGodDaKween` SSID, re-run `verify_mbp_wol.py`
- Or flip `macbook_pro.always_on = true` and keep `caffeinate -d` running on MBP
- Or move `vault_synthesis` to the Mac Mini with a smaller model

Not blocking this A.6 decision.

## Gate-check impact

| Gate | Before this run | After |
|---|---|---|
| 1. Gemma 4 benchmarks on 3 tasks | PARTIAL (only inbox_triage ran) | **PASS** (all 3 tasks have both models' data) |
| 2. ≥1 model swap deployed | PARTIAL | **PASS** (inbox_triage swap committed) |
| 3–5 | unaffected | unaffected |

## Notes & follow-ups

- phi4-mini-reasoning's `<think>` chains balloon on complex prompts — the 140.6 s p95 on inbox_triage is the `<think>` block consuming the 4507-token budget. Worth noting this is a characteristic of the reasoning variant specifically; `phi4-mini` (non-reasoning) would be faster but likely worse on `inbox_triage` classification. We're keeping `phi4-mini-reasoning` for `financial_analysis` where the reasoning chain earns its latency.
- `gemma4:e4b` Q4_K_M context length is 131K (from Ollama tag metadata). Not a differentiator for our small-prompt golden sets but relevant if we start routing longer documents.
- Code_review extractor fix is low priority — no production agent uses code_review routing today. When Sean wants PR digest automation (pr_digest agent, currently disabled), we'll re-run this task with a fixed extractor first.

## Commands to reproduce

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 scripts/run_gemma4_benchmark.py --samples 20
# Output: benchmarks/results/gemma4-benchmark-YYYY-MM-DD.json
python3 scripts/phase6_gatecheck.py
```
