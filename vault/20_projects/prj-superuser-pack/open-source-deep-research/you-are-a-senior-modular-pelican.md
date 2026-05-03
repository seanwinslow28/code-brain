# Local Open-Source Deep Research Stack — MBP M4 Pro Deployment Plan

## Context

You want autonomous deep research running locally to (a) reduce/replace paid Perplexity DR / Gemini DR usage and (b) integrate with the existing `agents-sdk/` pattern so research can fire on a schedule and write into the Obsidian vault. The two source reports were scoped for an Alienware RTX 5080 + Mac Mini topology; this plan is rescoped to the MacBook Pro M4 Pro / 48GB / Apple Silicon as the primary target, with a follow-on migration step to the Mac Mini.

**Primary recommendation source:** `Claude-Synthesis-of-Deep-Research-Reports.md` — modified for MLX/Metal hardware and verified against current vendor pricing.

---

## 1. Pre-Flight Inventory (this machine, today)

| Check | Result | Implication |
|---|---|---|
| **Ollama installed** | ❌ Not on PATH, no `/Applications/Ollama.app`, no `~/.ollama` dir | Either install Ollama OR run everything through LM Studio (preferred — MLX). |
| **LM Studio installed** | ✅ App present at `/Applications/LM Studio.app`, models dir `~/.lmstudio/models/` | Default LLM runtime. Listens on `localhost:1234` (OpenAI-compatible). |
| **LM Studio models** | ✅ Already on disk: `mlx-community/Qwen3-14B-4bit` (plan default), `lmstudio-community/gemma-4-31B-it-MLX-4bit` (stretch tier), `mlx-community/Qwen2.5-Coder-32B-Instruct-4bit` (coder, skip for research) | **No download needed** — Phase 2 is config only. |
| **Disk free** | 154 GiB on `/System/Volumes/Data` | Plenty of headroom (model + Docker images + vault writes ≪ 50 GB). |
| **Docker** | ✅ CLI installed (`v29.3.1`) but daemon **not running** | Need to launch Docker Desktop before Phase 1. |
| **Python** | System 3.9.6 (Xcode default) | Too old for LangGraph async; use `uv venv --python 3.11`. |
| **uv** | ✅ `0.10.2` at `~/.local/bin/uv` | Use for env management. |
| **agents-sdk/** | ✅ Healthy. `daily_driver.py` is the canonical pattern. `config.toml`, `lib/vault_io.py` (`inject_at_anchor` exists), `schedules/` plists all in place. | Drop-in slot for new agent. |
| **Existing related skills** | `research-synthesis`, `vault-read-write`, `vault-architecture`, `vault-automation` | Reuse `vault-read-write` for vault ops; new skill `deep-research-queue` is additive. |
| **Other files in `open-source-deep-research/`** | Only the three source files | Greenfield — no prior implementation work to reconcile. |

**Routing config note:** `agents-sdk/config.toml` already has `[routing.machines.macbook_pro]` pointing at `192.168.68.50:1234` (LM Studio) and a `task_map` entry `vault_synthesis = { model = "qwen3-14b", machine = "macbook_pro" }`. The new research agent should add a `deep_research` task_map entry rather than hardcode endpoints.

---

## 2. Reconciled Recommendations (calibrated for M4 Pro / 48 GB unified memory / MLX)

| Layer | Pick | Why (deviation from synthesis if any) |
|---|---|---|
| **Framework** | **LearningCircuit Local Deep Research (LDR) v1.6.1** | Confirmed live on PyPI, MCP server still ships in `pip install "local-deep-research[mcp]"`. Synthesis pick stands. |
| **Search backend** | **SearXNG self-hosted** (Docker) | Brave free tier confirmed killed 2026-02-12 — Perplexity report was correct, Gemini wrong. SearXNG is the only $0 path. |
| **Search fallback** | **Tavily free tier** (1,000/mo) | Configure in LDR settings but leave inactive until SearXNG quality fails. No card-on-file required. |
| **Primary LLM runtime** | **LM Studio (MLX backend) on `localhost:1234`** | **Deviation:** Synthesis assumed Ollama/GGUF. On Apple Silicon, MLX is materially faster than GGUF for the same model — and LM Studio is already installed and wired into `agents-sdk/config.toml` routing. No reason to add Ollama. |
| **Default model** | **Qwen3-14B MLX 4-bit** (≈8 GB) — *already on disk at* `~/.lmstudio/models/mlx-community/Qwen3-14B-4bit/` | Same model class as the synthesis pick, but MLX quant. Best instruction-following at this size; safer than reasoning-distill for JSON-schema tool calls. Expect ~30–45 tok/s on M4 Pro (vs ~55 on RTX 5080 — ~70% of NVIDIA speed). |
| **Stretch model** (optional) | **Gemma-4 31B Instruct MLX 4-bit** (≈17 GB) — *already on disk at* `~/.lmstudio/models/lmstudio-community/gemma-4-31B-it-MLX-4bit/` | **Deviation:** Synthesis ruled out 32B due to 16 GB VRAM cap; you have 48 GB unified, so 31B + 32K context KV cache (~24 GB total) fits with margin. Picked over Qwen3-32B because it's already on disk, instruct-tuned (not reasoning-distill — no `<think>` tag pollution), and benchmarks comparably for synthesis. Expect ~12–18 tok/s. Use selectively for high-stakes research, not every run. |
| **Skip** | DeepSeek-R1-Distill, Qwen 3.6-35B-A3B MoE | R1 distill embeds `<think>` tags that break LDR's JSON parsers. The new Qwen 3.6-MoE is too fresh to bet on without testing — revisit after baseline works. |

**Thermal/power note:** Sustained 5–10 minute LDR runs on the 14B model will spin the fans and pull battery aggressively. For background scheduled runs, plan to keep MBP plugged in. Mac Mini (Phase 5 migration) eliminates this concern entirely.

---

## 3. Phased Execution Plan

Each phase: **Goal | Steps | Test | Time | Rollback**.

### Phase 0 — Pre-flight verification (15 min)

- **Goal:** Confirm no surprises before any installs.
- **Steps:**
  1. Launch Docker Desktop; wait for whale icon. Run `docker ps` — must succeed.
  2. Open LM Studio; confirm Local Server tab loads. Note port (default 1234).
  3. `uv --version` — confirm `0.10.x`.
  4. `git status` in this repo — confirm clean working tree before adding new files.
- **Test:** All four commands return without error.
- **Rollback:** N/A (read-only).

### Phase 1 — SearXNG via Docker (20 min)

- **Goal:** Free, JSON-capable search backend running on `localhost:8080`.
- **Steps:**
  1. Create dir `~/Code-Brain/local-deep-research-stack/searxng-settings/`.
  2. Pull and run the **official** image:
     ```
     docker run -d --name searxng -p 8080:8080 \
       -v ~/Code-Brain/local-deep-research-stack/searxng-settings:/etc/searxng \
       searxng/searxng
     ```
  3. After first start, edit `searxng-settings/settings.yml` → add `json` to `search.formats`.
  4. `docker restart searxng`.
- **Test:** `curl "http://localhost:8080/search?q=qwen3&format=json" | head` returns JSON with `results` array.
- **Time:** 20 min (first pull is slow).
- **Rollback:** `docker stop searxng && docker rm searxng` (no system mutation outside container).

### Phase 2 — LLM in LM Studio (5 min — model already on disk)

- **Goal:** `Qwen3-14B-4bit` served at `http://localhost:1234/v1` (OpenAI-compatible).
- **Steps:**
  1. Open LM Studio → My Models → confirm `mlx-community/Qwen3-14B-4bit` is listed.
  2. Load it. Set context length **32768**, KV cache type default.
  3. Local Server tab → **Start Server**. Confirm log shows `Listening on port 1234` and note the **exact model identifier** LM Studio displays (typically `mlx-community/qwen3-14b-4bit` or similar — use this verbatim in Phase 3 config).
- **Test:**
  ```
  curl http://localhost:1234/v1/models    # confirms loaded model id
  curl http://localhost:1234/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"<id from above>","messages":[{"role":"user","content":"Say hi in 5 words."}]}'
  ```
  Should return JSON completion within 2–3s.
- **Time:** 5 min.
- **Rollback:** Stop server. Model files are not deleted (they persist for other uses).

### Phase 3 — LDR install + auth (45 min)

- **Goal:** LDR running, authenticated, talking to LM Studio + SearXNG.
- **Steps:**
  1. `mkdir -p ~/Code-Brain/local-deep-research-stack && cd ~/Code-Brain/local-deep-research-stack`
  2. `uv venv --python 3.11 && source .venv/bin/activate`
  3. `uv pip install "local-deep-research[mcp]"` (mcp extra for Phase 6).
  4. `export LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true` (dev mode — keep out of production migration).
  5. Create `~/.config/local_deep_research/settings.toml`:
     ```toml
     [llm]
     provider = "openai_endpoint"
     model = "<exact id from `curl /v1/models` in Phase 2>"
     base_url = "http://localhost:1234/v1"
     api_key = "lm-studio"   # LM Studio ignores the value but field is required
     context_window = 32768

     [search]
     tool = "searxng"
     searxng_url = "http://localhost:8080"
     max_results_per_query = 5
     ```
  6. `ldr-web` — server starts on `http://localhost:5000`.
  7. Browser → `http://localhost:5000/auth/register` — create one user. Save credentials in macOS Keychain (mirror `lib/keychain.py` pattern).
- **Test:** Login at `:5000`; submit a one-line "quick research" query in the UI; confirm result returns inside 5 min with at least 3 citations.
- **Time:** 45 min.
- **Rollback:** `rm -rf ~/Code-Brain/local-deep-research-stack ~/.config/local_deep_research`. No global system changes.

### Phase 4 — First manual smoke test from Python (20 min)

- **Goal:** Prove `LDRClient` works programmatically (precondition for headless agent).
- **Steps:**
  1. In the same venv, write `~/Code-Brain/local-deep-research-stack/smoke_test.py`:
     ```python
     from local_deep_research.api import LDRClient
     c = LDRClient(base_url="http://localhost:5000")
     c.login("USERNAME", "PASSWORD")
     r = c.quick_research("Compare MLX vs GGUF inference speed on Apple M4 Pro for 14B-class models", iterations=2)
     print(r["summary"])
     ```
  2. Run it. Time it with `time python smoke_test.py`.
- **Test:** See §4 below for the full success criteria. Pass = report meets all bullets.
- **Time:** 20 min (script writing + 5–10 min generation).
- **Rollback:** Delete the script.

### Phase 5 — Integration with `agents-sdk/` (90 min)

This is the load-bearing phase. Concrete file paths and config keys:

**5a. New agent script:** `agents-sdk/agents/deep_researcher.py`
- Mirror structure of `agents/daily_driver.py`: argparse for `--mode {oneshot|queue}`, load config via `lib.config.load_config()`, build preamble, call `LDRClient`, write output via `lib.vault_io.inject_at_anchor`.
- Pull credentials via `lib.keychain.get("ldr_username")` / `ldr_password`.
- Routing: read model from `config.task_map["deep_research"]`.

**5b. Vault target & anchor:**
- Per-day digest: append to `vault/10_timeline/daily/{YYYY-MM-DD}.md` under anchor `<!-- research-digest -->` (new anchor — daily-note template will need this added).
- One-off topical reports: write a new note at `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` using the existing `vault-read-write` skill conventions.

**5c. Config additions** (`agents-sdk/config.toml`):
```toml
[agents.deep_researcher]
enabled = true
skills = ["research-synthesis", "vault-read-write"]
max_turns = 30
max_budget_usd = 0.10   # local model — cap covers any unintended cloud fallback
queue_path = "vault/00_inbox/research-queue.md"
output_anchor = "research-digest"
target_machine = "macbook_pro"
ldr_base_url = "http://localhost:5000"

[routing.task_map]
# add this line — model already loaded by LM Studio
deep_research = { model = "qwen3-14b", machine = "macbook_pro" }
```

**5d. Queue mechanism:**
- One markdown file at `vault/00_inbox/research-queue.md` with `- [ ] question` checkboxes.
- Agent reads file, picks first unchecked, runs LDR, marks done with timestamp + link to output note. This piggy-backs on the existing inbox pattern — no new infra.

**5e. launchd plist:** `agents-sdk/schedules/com.sean.agent.deep-researcher.plist`
- Mirror `com.sean.agent.daily-morning.plist` exactly (env vars, PATH including `~/.local/bin:/opt/homebrew/bin`, log paths under `vault/90_system/agent-logs/`).
- Schedule: nightly at **02:45** (after vault-indexer 02:00 / vault-synthesizer 02:30, before knowledge-lint Sunday 22:00). Plug into `install_schedules.sh`.

**5f. Doc updates** (CLAUDE.md non-negotiable rule):
- `CHANGELOG.md` — entry under next version
- `CLAUDE.md` — bump agent count "13 → 14 SDK agents (7 active)"; add row to Active agents table
- `README.md` — same agent table
- `docs/agents-sdk.md` — new section if needed

**Test (5):** Drop one question into `research-queue.md`, run `python3 agents/deep_researcher.py --mode queue --dry-run` (prints prompt + chosen question), then live run, then `cat` the daily note to confirm anchor injection.

**Time:** 90 min.
**Rollback:** Delete `agents/deep_researcher.py`, revert `config.toml`, `launchctl unload` the plist, delete it. Doc reverts via `git`.

### Phase 6 — MCP server hookup for interactive Claude Code use (20 min, optional)

- **Goal:** Call `ldr.research(...)` as a tool inside any Claude Code session.
- **Steps:**
  1. Verify `pip install "local-deep-research[mcp]"` already installed `ldr-mcp` binary.
  2. Add to `.claude/settings.json` (project-level) under `mcpServers`:
     ```json
     "ldr": {
       "command": "/Users/seanwinslow/Code-Brain/local-deep-research-stack/.venv/bin/ldr-mcp",
       "args": [],
       "env": {"LDR_BASE_URL": "http://localhost:5000", "LDR_USER": "...", "LDR_PASS": "..."}
     }
     ```
     (Move credentials to env-var lookup against Keychain — do not commit plaintext.)
  3. Restart Claude Code. Confirm `ldr` shows up in `/mcp` list.
- **Test:** In an interactive session, ask Claude to "use the ldr tool to research X"; verify a result returns and is identical (or close) to the LDR Web UI output.
- **Time:** 20 min.
- **Rollback:** Remove the `ldr` block from `mcpServers` and restart.

### Phase 7 — Model A/B benchmark (deferred — only after baseline is trusted)

- **Trigger condition:** Do not start Phase 7 until you have completed Phases 0–6 *and* run the stack against ≥5 real research questions over ≥1 week, and you are satisfied with output quality, citation accuracy, and runtime stability on Qwen3-14B. The point of this phase is *replacing a known-good default*, not "is this even working." If Phase 4 or 5 fail, debug those — do not jump to a new model hoping it fixes the issue.
- **Goal:** Decide whether to swap the default model from `Qwen3-14B-4bit` to a Qwen 3.6 variant (or keep Qwen3-14B and assign 3.6 to the stretch tier).
- **Steps:**
  1. Download both candidates in LM Studio:
     - `Qwen3.6 27B Dense` (~17.5 GB) — README leads with coding emphasis, so test prose synthesis carefully.
     - `Qwen3.6 35B A3B` (MoE, 3B active params/token, ~20 GB) — most interesting architecturally; should be faster than dense 27B despite larger total size.
  2. Pick **3 representative real queries** from the prior week's actual research-queue history (not synthetic — real questions you'd ask anyway). Mix one factual, one synthesis-heavy, one analytical.
  3. For each query, run the same LDR pipeline through all three models with identical settings (`iterations=2`, `max_results_per_query=5`, same SearXNG state). Capture per-run: wall-clock time, tok/sec, citation count, citation 404 rate, output length.
  4. Read the three reports for each query side-by-side. Score each on: factual accuracy (cross-check 2 claims), citation relevance, synthesis coherence, format compliance.
  5. Document results in `vault/20_projects/prj-superuser-pack/open-source-deep-research/model-ab-results-YYYY-MM-DD.md`.
- **Decision matrix:**
  | Outcome | Action |
  |---|---|
  | Qwen3.6 35B A3B is faster *and* materially better on ≥2/3 queries | Swap default → 35B A3B. Drop Gemma-4-31B from stretch tier; assign Qwen3.6 27B Dense as new stretch. |
  | Qwen3.6 27B Dense is materially better but slower | Keep 14B as default; promote 27B Dense to stretch tier (replacing Gemma-4-31B). |
  | Both are marginal vs. 14B (≤1/3 queries clearly better) | Keep current setup. Delete the new downloads to reclaim disk. |
  | One model breaks LDR's JSON parser or tool-call format | Permanently exclude from candidate list; document the failure mode. |
- **Test:** After swap (if any), re-run the original Phase 4 smoke test query against the new default. Must still pass all five §4 criteria.
- **Time:** ~90 min — 30 min downloads, 30 min test runs (3 queries × 3 models, mostly overlapping with reading), 30 min comparison + decision.
- **Rollback:** Revert `[routing.task_map].deep_research.model` in `config.toml` to the prior value. Models stay on disk; can re-test later.

---

## 4. Smoke Test Query (Phase 4 success criteria)

**Query:**
> "Compare MLX vs GGUF inference speed on Apple M4 Pro hardware for 14B-class language models. Cite at least three independent sources from 2025–2026 with numeric tok/sec measurements."

**Why this query:** Multi-source factual; requires recent (post-cutoff) info; numeric data forces real source consultation; subject is verifiable so hallucination is detectable.

**Expected output characteristics:**
- **Length:** 600–1,500 words.
- **Structure:** Intro / methodology mention / per-source numeric findings / synthesis / source list.
- **Citations:** ≥3 distinct sources with URLs. Spot-check 2 — both must resolve (no 404).
- **Numeric content:** At least 2 explicit tok/sec figures.
- **Generation time on M4 Pro (Qwen3-14B MLX 4-bit, 2 iterations):** ~5–9 minutes wall clock. >15 min = problem (likely SearXNG throttling or context overflow).
- **Pass = all five bullets met.** Any miss → debug before Phase 5.

---

## 5. Migration to Mac Mini (later)

> **2026-05-02:** Migration plan written and saved as a sibling doc — see [[macmini-migration-plan-2026-05-02]]. That plan supersedes this section's high-level table with a phased execution plan, a 24 GB memory headroom budget, and a re-scoped Phase 7 model A/B (Qwen3.6 27B / Gemma 4 26B / Ministral 3 14B) calibrated against the current Ollama landscape. Read it before kicking off the migration. The summary table below remains useful as a quick "what changes between machines" reference.

Mac Mini is the always-on agent driver, has 24 GB unified memory and runs Ollama (per `config.toml`). What changes:

| Concern | MBP today | Mac Mini target |
|---|---|---|
| **Model size** | 14B MLX (8 GB) default; 32B MLX (18 GB) stretch viable | **24 GB ceiling means 32B is the absolute max with thin KV-cache headroom; stay on 14B as default.** Drop the stretch tier — 18 GB model + 32K context = ~22 GB used, no thermal margin. |
| **Runtime** | LM Studio (MLX), `:1234` | Ollama (GGUF), `:11434`. Pull `qwen3:14b` Q5_K_M from Ollama registry. Update `task_map.deep_research.machine = "mac_mini"` and let routing handle the endpoint swap. |
| **Quant format** | MLX 4-bit | GGUF Q5_K_M (Ollama-friendly, slight quality bump over Q4) |
| **Schedule** | Nightly 02:45 | Same — Mac Mini is awake 24/7, MBP is not. |
| **SearXNG** | Docker on MBP `:8080` | Move container to Mac Mini. Update `searxng_url` in `~/.config/local_deep_research/settings.toml` on Mac Mini. |
| **LDR install** | `~/Code-Brain/local-deep-research-stack/.venv` on MBP | Reinstall via `uv pip install "local-deep-research[mcp]"` on Mac Mini. **Do not** symlink; treat as parallel install. |
| **Auth / credentials** | Keychain on MBP | Re-register user on Mac Mini's LDR; store new creds in Mac Mini Keychain. |
| **Speed expectation** | 14B at ~30–45 tok/s | 14B at ~25–35 tok/s (M4 base, narrower bandwidth). Add ~30% to per-run time. |
| **Path differences** | `vault_root` already absolute in `config.toml` | If Mac Mini mounts the vault at the same path, zero changes. If not, parameterize `vault_root` per-machine. |

**Won't transfer cleanly:**
- Any `localhost` URL hardcoded in the agent — must read from `config.toml` routing instead.
- `LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true` shortcut — turn this **off** on Mac Mini and use the encrypted DB path; Mac Mini is the production host.

---

## 6. Risks and Decision Points

**Risks:**
1. **SearXNG upstream throttling.** Aggressive Google/Bing CAPTCHAs after ~15–20 queries. Mitigation: cap `max_results_per_query=5` and `iterations=2–3` initially; rotate engines in `settings.yml`.
2. **JSON parser failures with reasoning models.** If you ever swap in a `<think>`-tag model (R1 distill, Qwen3 with `/think` mode), LDR's parser may break. Stick with vanilla Qwen3-14B in instruct mode.
3. **MBP thermal throttling on long runs.** Plugged-in + lid-open is required for sustained operation; expect fans. Acceptable for a smoke test, not for nightly runs — that's the migration trigger.
4. **LDR auth session expiry in scheduled scripts.** Sessions can expire; wrap `client.login()` in try/except with one retry per `daily_driver.py` patterns.
5. **Hallucinated citations from 14B model.** Add a 20-line URL-checker post-processor that pings each cited URL and tags 404s in the output note. Don't ship without it.

**Fork-in-the-road decisions for you:**

- **D1 — Cost ceiling on search:** If SearXNG quality is poor on the smoke test, do you (a) live with it for $0, (b) add Tavily free tier (still $0 up to 1K/mo), or (c) accept ~$5–10/mo on Tavily paid? Recommend default (b); revisit after 2 weeks of usage.
- **D2 — Where the 32B stretch model runs:** If Qwen3-14B disappoints on synthesis quality, do you (a) keep 14B and accept the gap, (b) run 32B on MBP only when plugged in (manual trigger), or (c) skip OSS 32B and route high-stakes queries to a paid Perplexity DR API call (~$5/mo for occasional use)? This is a quality-vs-autonomy tradeoff — your call after seeing real outputs.

---

## 7. Out of Scope (explicit)

- Fine-tuning any model.
- Custom Docker images (only official `searxng/searxng`).
- Per-skill MCP wrappers beyond the LDR one.
- Vector DB / private-document RAG (LDR supports it; not needed for v1).
- GPT Researcher or STORM as alternatives — both rejected for now (LDR wins on integration fit; revisit only if LDR fails Phase 4).
- Hybrid cloud-fallback logic to Perplexity API or Claude API for high-stakes queries (decision D2 — defer until baseline proven).
- Rewriting `daily-driver.py` to call LDR — research stays a separate agent for now; Daily Driver may *consume* the output via vault Read in a later iteration.
- Cost telemetry beyond the existing per-agent budget cap mechanism.
- Backup / DR for the LDR SQLite DB.

---

## Verification Section (end-to-end test plan)

After Phase 5 completes, run this sequence to confirm the full pipeline:

1. **Add a question:** Echo `- [ ] What are the key differences between Apple's MLX and GGUF formats for 14B LLMs in 2026?` into `vault/00_inbox/research-queue.md`.
2. **Dry run:** `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode queue --dry-run` — verify it prints the question + intended LDR call.
3. **Live run:** Same command without `--dry-run`. Watch logs at `vault/90_system/agent-logs/deep-researcher-*.log`.
4. **Inspect outputs:**
   - `vault/00_inbox/research-queue.md` — question marked `- [x]` with timestamp + output link.
   - `vault/20_projects/research/2026-04-25-mlx-vs-gguf.md` (or similar) — full report with citations.
   - Today's daily note has a 2-line digest under `<!-- research-digest -->` linking to the report.
5. **launchd test:** `launchctl load agents-sdk/schedules/com.sean.agent.deep-researcher.plist`; trigger manually with `launchctl start com.sean.agent.deep-researcher`; confirm same output.
6. **MCP test (if Phase 6 done):** Open Claude Code, run `/mcp` — confirm `ldr` listed; ask "use the ldr tool to research X" inside a session; verify equivalent output.

If all six steps pass, the stack is production-ready on the MBP and ready to migrate per §5.

---

## Critical files to be created or modified

**New files:**
- `agents-sdk/agents/deep_researcher.py`
- `agents-sdk/schedules/com.sean.agent.deep-researcher.plist`
- `vault/00_inbox/research-queue.md`
- `~/.config/local_deep_research/settings.toml` (outside repo)
- `~/Code-Brain/local-deep-research-stack/` (outside repo — venv, settings, smoke_test.py)

**Modified files:**
- `agents-sdk/config.toml` — add `[agents.deep_researcher]` + `[routing.task_map].deep_research`
- `agents-sdk/schedules/install_schedules.sh` — add new plist
- `CLAUDE.md`, `README.md`, `CHANGELOG.md` — counts + tables
- `.claude/settings.json` — only if Phase 6 proceeds (MCP server entry)
- Daily-note template (wherever in vault it lives) — add `<!-- research-digest -->` anchor

**Existing utilities to reuse (do not duplicate):**
- `agents-sdk/lib/vault_io.py:inject_at_anchor` — anchor injection
- `agents-sdk/lib/vault_io.py:daily_note_path` — daily note resolution
- `agents-sdk/lib/config.py:load_config` — config + routing
- `agents-sdk/lib/keychain.py` — credential storage
- `agents-sdk/lib/logging_setup.py:record_run` — agent run logging
- `agents-sdk/agents/daily_driver.py` — pattern to mirror (argparse, preamble builder, async query loop)
- Skills: `research-synthesis`, `vault-read-write`

---

## 8. Execution Deltas (Phases 0–5 completed 2026-04-26)

Phases 0–5 shipped in v3.17.0. Phase 6 (MCP hookup) and Phase 7 (model A/B) remain deferred. The body of this plan above is the original brief; below are the corrections discovered during execution. Both plan copies (`vault/...` and `~/.claude/plans/...`) carry this section.

### Port: 5000 → 5050
macOS AirPlay Receiver claims port 5000 (`Server: AirTunes/...`). All references to `:5000` in §3 Phases 3, 5c, 6, and §Verification Section should read **`:5050`**. The agent uses `LDR_WEB_PORT=5050 LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true ldr-web` to launch, and `agents-sdk/config.toml [agents.deep_researcher].ldr_base_url = "http://localhost:5050"`.

### LDR settings live in encrypted DB, not `settings.toml`
LDR v1.5.6 stores per-user settings in an SQLCipher database at `~/Library/Application Support/local-deep-research/encrypted_databases/`. The `~/.config/local_deep_research/settings.toml` file in §3 Phase 3 step 5 **does not exist** in v1.5.6 and is not read. Configure via the REST API after first user registration:

```python
# Five critical settings (PUT /settings/api/<key> with X-CSRFToken header):
#   llm.provider              = "LMSTUDIO"
#   llm.lmstudio.url          = "http://localhost:1234/v1"   # MUST include /v1 — without it LDR queries http://localhost:1234/models which 404s
#   llm.model                 = "qwen3-14b"                  # bare — no qwen/ HuggingFace prefix
#   search.tool               = "searxng"
#   search.iterations         = 2
```

### Qwen3-14B "thinking mode" must be disabled at the LM Studio layer
Qwen3-14B-MLX-4bit ships with thinking mode ON in LM Studio. Without disabling, every chat completion emits ~50 reasoning_tokens before content (10s for a "say hi" prompt; first run hit max_tokens cap mid-thinking and returned empty `content`).

**Fix:** In LM Studio → My Models → Qwen3-14B-4bit → gear icon → **Inference** tab → set the per-model **System Prompt** to `/no_think`. Leave **Reasoning Parsing** ON (it strips `<think>` tags into `reasoning_content` — with `/no_think` Qwen3 stops emitting tags so the parser is a no-op). Reload model with **Context Length 32768**. Verified: response went from 10s/empty-content → 1s/clean.

### Phase 5a — pure-Python wrapper, not Claude SDK orchestration
The original plan said "Mirror structure of `agents/daily_driver.py`" which implied a Claude Agent SDK loop. In practice the deep_researcher is a pure-Python wrapper because LDR + Qwen3-14B IS the synthesis engine — no Claude in the loop. The `skills` and `max_budget_usd` config fields are decorative (kept for parity with the daily-driver pattern; budget cap exists as a guard against unintended cloud fallback).

The agent talks to LDR via **httpx REST** (LDR runs Python 3.11; agents-sdk runs Python 3.13 — cross-venv import fails on bytecode). The endpoints used (replicating LDRClient.quick_research's path):
1. `GET /auth/login` → extract CSRF token from form
2. `POST /auth/login` (form-encoded) → 302 + session cookie
3. `POST /research/api/start` (JSON: `query`, `search_engines: ["searxng"]`, `iterations`, `questions_per_iteration`) → research_id
4. `GET /research/api/status/<id>` (poll every 4s until `completed`)
5. `GET /api/report/<id>` → JSON with `content` field (the markdown report)

**`mode: "quick"` on the alternate `/api/start_research` REST endpoint is a trap** — returns in ~40s with zero sources and hallucinated citations. The agent uses `/research/api/start` with explicit `search_engines` + `iterations` only.

### LDR rate limiter on `/auth/login`
Five rapid login attempts trip a sliding-window rate limit (429 responses for ~5 min). The agent caches one session per run; do not re-login per request. Restart of `ldr-web` clears the limit if you trip it during testing.

### SearXNG `:8080` settings
After first container start, edit `~/Code-Brain/local-deep-research-stack/searxng-settings/settings.yml` to add `- json` under `search.formats:` (the default is `[html]` only). `docker restart searxng` to pick up.

### Phase 5e — launchd not auto-loaded
The plist `agents-sdk/schedules/com.sean.agent.deep-researcher.plist` is committed but **NOT yet `launchctl load`ed**. Run `./agents-sdk/schedules/install_schedules.sh` when ready to enable nightly 02:45 runs.

### Phase 5 verification evidence (live)
- `vault/20_projects/research/2026-04-26-what-are-the-key-differences-between-apples-mlx-and-gguf-for.md` — 2243-word topical report, 561s wall, 100+ inline citations.
- `vault/10_timeline/daily/2026-04-26.md` — digest line landed under `<!-- research-digest -->` anchor.
- `vault/00_inbox/research-queue.md` — line rewritten from `- [ ]` to `- [x] ... — done 2026-04-26 09:56 → [[topical-note]]`.
- `vault/90_system/agent-logs/agent-run-history.csv` — both runs recorded (`success`, `empty-queue`).

### Decision points NOT triggered yet
- **D1 (Tavily fallback):** Not triggered. Phase 5 result quality is good; SearXNG-only stays for now. Revisit after 2 weeks of usage.
- **D2 (32B stretch model):** Not triggered. Qwen3-14B's Phase 4/5 output is coherent and well-cited.

### Phase 6 — MCP server hookup (shipped 2026-04-26)

The original plan §3 Phase 6 example pointed at `.claude/settings.json` `mcpServers` block + `LDR_USER`/`LDR_PASS` env vars. **Both are wrong for the modern Claude Code model and the actual `ldr-mcp` architecture.**

- Modern Claude Code stores stdio MCP servers in `.mcp.json` at project root and approves them via `enabledMcpjsonServers` in `.claude/settings.local.json` (or `.claude/settings.json`). The schema rejects `mcpServers` as a top-level key in settings.json.
- `ldr-mcp` runs the MCP server **in-process** (not as an HTTP client to ldr-web) and has NO auth layer — stdio = local-only, security via OS user perms. So no `LDR_USER` / `LDR_PASS` exist; no env vars needed.
- BUT `ldr-mcp` calls `create_settings_snapshot()` with no overrides, picking up LDR's defaults (`llm.provider = OLLAMA`, `llm.model = gemma3:12b`). It does NOT read the per-user encrypted DB. The MCP tool args only let callers override `search_engine`, `strategy`, `iterations`, `questions_per_iteration` — not `llm.provider` or `llm.model`.

**What was actually shipped:**

- `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py` — Python wrapper (~70 lines) that monkey-patches `local_deep_research.api.settings_utils.create_settings_snapshot` BEFORE importing `local_deep_research.mcp`, injecting `LMSTUDIO + qwen3-14b + searxng` overrides into every snapshot. Caller-supplied tool overrides still win.
- `.mcp.json` — `ldr` entry added (stdio, command = wrapper path, no env).
- `.claude/settings.local.json` — `"ldr"` added to `enabledMcpjsonServers`.
- Smoke test (manual stdio handshake) returns 8 tools with proper schemas; FastMCP version 1.27.0.
- **Maintenance debt:** the wrapper depends on LDR's internal module layout. If LDR refactors `settings_utils`, the patch breaks silently (falls back to defaults, tool calls fail). When upgrading LDR, re-run the wrapper smoke-test before relying on it. A future LDR version exposing env-var or config-file overrides should retire this wrapper.

**Next step (requires Sean):** Restart Claude Code → `/mcp` should list `ldr` → ask Claude inside a session to "use the ldr tool to research X" → expect 1-5 min response with citations. The wrapper requires LM Studio + SearXNG running on the MBP at the time of the call.

### Phase 7 remains deferred

Per the original plan. Qwen3.6 27B/35B-A3B benchmark is gated on ≥1 week of real usage — DO NOT start until baseline is trusted.
