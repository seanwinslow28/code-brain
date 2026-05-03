# Local Open-Source Deep Research Stack — Mac Mini Migration & Production Plan

**Date:** 2026-05-02
**Author:** Sean (with Claude as scribe)
**Status:** Plan — not yet executed
**Sibling docs:**
- [[Claude-Synthesis-of-Deep-Research-Reports]] — primary recommendation source
- [[Gemini-Local-Autonomous-Research-Agent-Landscape]] — supporting report
- [[Perplexity-Local-Open-Source-Deep-Research-Agent-Stack]] — supporting report
- [[you-are-a-senior-modular-pelican]] — MBP deployment plan (shipped v3.21.0, 2026-04-26). Read its §8 "Execution Deltas" before Phase 3.

## Goal

Move the v3.21.0 deep-research stack from the MBP (LM Studio + MLX, intermittent availability) to the always-on Mac Mini M4 Pro (Ollama + GGUF, 24 GB) so scheduled autonomous research runs reliably nightly. Add a new `deep-research-queue` skill so Sean can queue topics during interactive sessions.

## Architecture

Migration, not greenfield. The Python agent, plist, vault template anchor, and MCP wrapper already exist from the MBP build (v3.21.0). This plan reconfigures the runtime layer (Ollama replaces LM Studio, GGUF replaces MLX), adds the missing skill, makes one config field machine-aware, and loads the existing plist into Mac Mini's launchd.

## Tech Stack

SearXNG (Docker) on `:8080` · Ollama serving Qwen3-14B Q5_K_M on `:11434` · LDR v1.5.6+ (Python 3.11 venv, `:5050`) · existing `agents-sdk/agents/deep_researcher.py` (Python 3.13 venv, httpx REST) · macOS launchd nightly 02:45.

---

## 1. Discovery Findings

### What already exists in the repo (cite-then-extend, do not duplicate)

| Artifact | Path | State |
|---|---|---|
| Autonomous agent | `agents-sdk/agents/deep_researcher.py` | **Shipped v3.21.0.** Pure-Python wrapper (no Claude SDK loop, by design — LDR + Qwen3 IS the synthesis engine). REST against `localhost:5050`. Picks question from queue, writes topical note, injects daily-note digest, marks queue done. |
| Config block | `agents-sdk/config.toml:141-159` | `[agents.deep_researcher]` enabled = true, `target_machine = "macbook_pro"`, `ldr_base_url = "http://localhost:5050"`, schedule = "02:45". |
| Routing entry | `agents-sdk/config.toml:263` | `deep_research = { model = "qwen3-14b", machine = "macbook_pro" }` (informational — agent talks to LDR HTTP, not LM Studio direct). |
| launchd plist | `agents-sdk/schedules/com.sean.agent.deep-researcher.plist` | **Committed but NOT loaded** (`launchctl list \| grep com.sean` returns 11 agents; `deep-researcher` is absent). |
| Vault template anchor | `vault/90_system/templates/tpl-daily.md:37` | `<!-- research-digest -->` already in place. No template work needed. |
| Queue file | `vault/00_inbox/research-queue.md` | Exists. |
| Output dir | `vault/20_projects/research/` | Auto-created by agent on first write. |
| MCP wrapper | `.mcp.json:16-20` → `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py` | Exists for MBP path; injects `LMSTUDIO + qwen3-14b + searxng` overrides. **Mac Mini variant required if interactive MCP wanted here.** |
| MBP plan + execution deltas | `vault/...open-source-deep-research/you-are-a-senior-modular-pelican.md:348-423` | §8 documents every gotcha hit during MBP execution — port 5000 → 5050, settings live in encrypted DB not TOML, `/no_think` requirement, rate limiter, `/api/start_research` trap. **Read in full before Phase 3.** |
| **deep-research-queue skill** | `.claude/skills/deep-research-queue/` | **DOES NOT EXIST.** Genuinely new in this plan. |

### Mac Mini inventory (2026-05-02)

| Check | Result | Implication |
|---|---|---|
| **Memory** | 24 GB unified | 14B model fits with margin if everything else is well-sized; 27B+ is *not* viable alongside daily-driver. |
| **Disk free** | 147 GiB on `/` | Plenty (Q5_K_M model + Docker images + vault writes ≪ 30 GB). |
| **Docker** | CLI v29.3.1 installed; **daemon NOT running** ("Cannot connect to docker.sock") | Phase 1 must start by launching Docker Desktop. |
| **Ollama** | Running on `:11434`. Models: `gemma4:e4b`, `gemma4:26b`, `nomic-embed-text`, `phi4-mini-reasoning` | **No `qwen3:14b`** — Phase 2 must `ollama pull`. |
| **LM Studio** | Not installed (per task brief). MLX is **not** an option here. | Hard dependency on GGUF + Ollama. |
| **Python** | System 3.9.6 only | Need `uv venv --python 3.11` for LDR (matches MBP install). |
| **uv** | 0.10.3 at `~/.local/bin/uv` | Use it. |
| **agents-sdk venv** | Existing (Python 3.13, has httpx) — same machine, ready | Agent runs as-is. |
| **claude CLI** | 2.1.126 at `~/.local/bin/claude` | OAuth available for any cloud-fallback path. |
| **launchd loaded agents** | 11 (daily-morning, daily-evening, weekly-review, vault-indexer, vault-synthesizer, knowledge-lint, meta-agent, sprint-health, daily-morning-baton, process-inbox, pr-digest) | `deep-researcher` plist present in repo but not symlinked into `~/Library/LaunchAgents/`. |
| **`~/Code-Brain/local-deep-research-stack/`** | Does NOT exist on Mac Mini | LDR install is fresh on this machine (sibling install to the MBP one — do NOT symlink). |

### Memory headroom math (24 GB)

| Resident | Steady state | Peak (during LDR run) |
|---|---|---|
| macOS + Finder + Cursor + ambient apps | ~6.0 GB | ~6.0 GB |
| Docker Desktop daemon | ~1.5 GB | ~1.5 GB |
| SearXNG container (idle) | ~0.3 GB | ~0.3 GB |
| Ollama serve (idle, no model loaded) | ~0.5 GB | ~0.5 GB |
| Qwen3-14B Q5_K_M loaded | 0 GB (unloads after `OLLAMA_KEEP_ALIVE`) | ~10.5 GB |
| KV cache (16K context, the cap LDR uses) | 0 GB | ~2.5 GB |
| LDR Python venv (`ldr-web` flask + SQLCipher) | ~0.4 GB | ~0.6 GB |
| agents-sdk Python (`deep_researcher.py` httpx loop) | 0 | ~0.2 GB |
| **Subtotal** | **~8.7 GB** | **~22.1 GB** |
| **Headroom on 24 GB** | ~15 GB | **~1.9 GB** |

**Conclusions:**
- Steady state is comfortable (15 GB free).
- Peak (during a ~10-min LDR run) leaves ~1.9 GB headroom — adequate but no concurrent daily-driver run.
- Daily-driver fires at **08:45 / 17:00 / Fri 16:00**. Deep-researcher fires at **02:45**, runs ≤15 min (`ldr_timeout_seconds = 900`). **Zero overlap window.** Safe.
- After the run completes, `OLLAMA_KEEP_ALIVE` (default 5 min) unloads the 14B model and frees ~13 GB — Mac Mini is back to 8.7 GB resident before any 06:30 (meta-agent) or 08:45 (daily-driver) wake-up.
- **If a future operator changes any agent's schedule, they must re-check this table.** Add a `## Schedule Conflict Check` line to the change checklist in Phase 10.

---

## 2. Stack Decisions for Mac Mini (deltas from synthesis)

| Layer | Mac Mini pick | MBP pick (shipped v3.21.0) | Why the delta |
|---|---|---|---|
| Framework | **LDR v1.5.6+** | LDR v1.5.6 | Same — synthesis pick stands. |
| Search | **SearXNG self-hosted** (Docker, `:8080`) | Same | Same. |
| Search fallback | Tavily free tier (configured but inactive) | Same | Same. Defer activation per D1 below. |
| LLM runtime | **Ollama** on `:11434` | LM Studio MLX on `:1234` | **Forced by hardware:** no LM Studio on Mac Mini. |
| Quant format | **GGUF Q5_K_M** | MLX 4-bit | **Forced by Ollama.** Q5_K_M ≈ 10.5 GB; slight quality bump over Q4. |
| Default model | **`qwen3:14b`** (Ollama base, default tag is Q4_K_M ≈ 9.3 GB; pull `qwen3:14b-q5_K_M` if registry exposes the explicit Q5 tag, else accept Q4) | Qwen3-14B MLX 4-bit | Same model class. |
| Model wrapper tag | **`qwen3-14b-research`** — local Ollama tag built via `ollama create -f Modelfile` from the registry base, with `/no_think` + `num_ctx 16384` + `temperature 0.3` baked in. NOT a registry model. | Per-model System Prompt in LM Studio Inference tab | Different runtime, same outcome — strip `<think>` tags so LDR's JSON parser doesn't choke. |
| Stretch model | **None** — drop the tier | Gemma-4 31B MLX 4-bit | **Forced by 24 GB ceiling:** 31B + KV cache + ambient = ~22+ GB; cannot coexist with daily-driver. |
| LDR `llm.provider` | **`OLLAMA`** | `LMSTUDIO` | **Settable only via LDR REST API** (`PUT /settings/api/llm.provider`), not `settings.toml` — that file is unread in v1.5.6. |
| LDR `llm.ollama.url` | `http://localhost:11434` | (n/a — LMSTUDIO) | New setting on Mac Mini. |

### Why Qwen3-14B over Qwen3.5/Qwen3.6/Gemma 4 (verified 2026-05-02 against ollama.com)

| Candidate | Size on disk | Peak RAM (model + KV + Docker + ambient) | 24 GB headroom | Daily-driver coexistence? | Validated on this code path? |
|---|---|---|---|---|---|
| **`qwen3:14b`** (chosen) | 9.3 GB | ~22 GB | ~2 GB | Yes (zero overlap window anyway) | **Yes** — MBP shipped v3.21.0 |
| `qwen3.6:27b` (1 week old, "agentic coding" marketing) | 17 GB | ~29 GB | **negative** | No — would need KV cache cut to 8K | No |
| `qwen3.6:35b` (Ollama's `:latest`) | 24 GB | won't fit alongside anything | — | No | No |
| `gemma4:26b` (already on disk, "frontier-level... agentic workflows") | 17 GB | ~29 GB | **negative** | No | No |
| `qwen3.5:27b` | ~17 GB | ~29 GB | **negative** | No | No |

**The headroom math kills the bigger options:**
- A 27B model at Q4_K_M ≈ 17 GB + 16K-context KV cache (~4 GB) + Docker/SearXNG (~1.5 GB) + Ollama daemon (~0.5 GB) + macOS+apps (~6 GB) = **~29 GB peak.** Does not fit on 24 GB.
- Workaround = drop context to 8K — but the synthesis explicitly flagged "context collapse around 16K, even though the window is 32K." Cutting to 8K hurts research quality more than the model upgrade gains.
- Inference speed: 14B at Q4 ≈ 25-35 tok/s on M4 Pro; 27B should be roughly half (12-18 tok/s). That nearly doubles wall-clock per run, pushing past `ldr_timeout_seconds = 900` (15 min) for multi-iteration syntheses.
- Validation surface: changing both runtime (LM Studio → Ollama) AND model (Qwen3-14B → Qwen3.6-27B) at the same time is bad debugging hygiene if the smoke test fails.

Ollama confirms `qwen3:14b` is current — listed, not deprecated, no "superseded by" notice. "11 months old" by Ollama's display but actively supported. The deferred Phase 7 below re-scopes the model A/B around the new Qwen3.6/Gemma-4 candidates once a baseline week of Mac Mini history exists.

---

## 3. Phased Execution Plan

### Phase 0 — Discovery + memory headroom verification (15 min)

- **Goal:** Confirm the table in §1 is still accurate the day deployment starts.
- **Steps:**
  1. `git status` — confirm clean tree before mutations.
  2. `ollama list` — confirm `qwen3:14b` is still absent (Phase 2 will pull).
  3. `docker info --format '{{.ServerVersion}}'` — must succeed. If not, launch Docker Desktop and re-check.
  4. `vm_stat | head -10` — record baseline free pages × 4 KB; calculate baseline RSS. Record in `vault/90_system/agent-logs/macmini-deepresearch-baseline-{date}.txt`.
  5. Confirm Mac Mini's IP (`192.168.68.200`) matches `[routing.machines.mac_mini].host` in `config.toml` line 212. If LAN reassigned, update line 212 in a one-line edit (out of scope of this phase, document only).
- **Test:** All checks return without error; baseline file created.
- **Time:** 15 min.
- **Rollback:** None (read-only).

### Phase 1 — SearXNG via Docker (20 min)

- **Goal:** SearXNG returning JSON on `localhost:8080`.
- **Steps:**
  1. Launch Docker Desktop; wait for whale icon in menu bar.
  2. `mkdir -p ~/Code-Brain/local-deep-research-stack/searxng-settings`
  3. ```
     docker run -d --name searxng -p 8080:8080 \
       --restart unless-stopped \
       -v ~/Code-Brain/local-deep-research-stack/searxng-settings:/etc/searxng \
       searxng/searxng:latest
     ```
     (`--restart unless-stopped` matters on Mac Mini — survives reboots without manual `docker start`.)
  4. After first start populates the volume, edit `searxng-settings/settings.yml`:
     - In `search.formats:` add `- json` (default is `[html]` only).
     - Optional: in `engines:` raise the per-engine `disabled` toggle off for at least Bing, DuckDuckGo, and Brave — the default ships with several disabled.
  5. `docker restart searxng`.
- **Test:** `curl -s "http://localhost:8080/search?q=qwen3&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('results') else 'EMPTY')"` → prints `OK`.
- **Time:** 20 min (image pull dominates).
- **Rollback:** `docker stop searxng && docker rm searxng && rm -rf ~/Code-Brain/local-deep-research-stack/searxng-settings`. No system mutation outside container.

### Phase 2 — Ollama model pull + endpoint smoke test (30 min)

- **Goal:** Qwen3-14B Q5_K_M served from `localhost:11434` with `/no_think` baked in via custom Modelfile.
- **Steps:**
  1. `ollama pull qwen3:14b` (or `qwen3:14b-q5_K_M` if the registry exposes the explicit Q5 tag — check with `ollama show qwen3:14b --modelfile` after pull).
  2. Create `~/Code-Brain/local-deep-research-stack/qwen3-14b-research.Modelfile`:
     ```
     FROM qwen3:14b
     SYSTEM """/no_think"""
     PARAMETER num_ctx 16384
     PARAMETER temperature 0.3
     ```
     (`num_ctx 16384` matches the synthesis "cap context near 16K to avoid context collapse" recommendation; `0.3` for synthesis vs default 0.8 reduces hallucination.)
  3. `ollama create qwen3-14b-research -f ~/Code-Brain/local-deep-research-stack/qwen3-14b-research.Modelfile`.
  4. Smoke test:
     ```
     curl -s http://localhost:11434/api/chat -d '{
       "model":"qwen3-14b-research",
       "messages":[{"role":"user","content":"Say hi in 5 words."}],
       "stream":false
     }' | python3 -c "import sys,json; d=json.load(sys.stdin); print('content:', d['message']['content'][:200]); print('eval_count:', d.get('eval_count')); print('eval_duration_ms:', d.get('eval_duration',0)//1_000_000)"
     ```
- **Test:** Response returns within 3 s, `content` is a 5-word greeting, no `<think>` tag in the output. tokens/s = `eval_count / (eval_duration_ms/1000)` should be ≥ 20 on M4 Pro 24 GB (synthesis budget said 25-35 on M4 base; M4 Pro is faster).
- **Time:** 30 min (10 GB pull dominates).
- **Rollback:** `ollama rm qwen3-14b-research && ollama rm qwen3:14b`. Keeps the registry tidy.

### Phase 3 — LDR install + auth + Ollama config (50 min)

- **Goal:** LDR v1.5.6+ running at `http://localhost:5050`, authenticated, configured to call Ollama + SearXNG.
- **Steps:**
  1. `cd ~/Code-Brain/local-deep-research-stack && uv venv --python 3.11`
  2. `source .venv/bin/activate`
  3. `uv pip install "local-deep-research[mcp]"` (mcp extra installs `ldr-mcp` for Phase 9).
  4. `pip show local-deep-research | grep Version` — record version.
  5. Launch the web server on port 5050 (port 5000 is claimed by macOS AirPlay):
     ```
     LDR_WEB_PORT=5050 LDR_BOOTSTRAP_ALLOW_UNENCRYPTED=true ldr-web
     ```
     Run in a separate terminal or tmux pane; leave running for the rest of the install.
  6. Browser → `http://localhost:5050/auth/register` — create one user `sean`, generate a strong password. **Do not reuse the MBP credential** — Mac Mini gets its own.
  7. Stash credentials in macOS Keychain via the existing helper:
     ```
     python3 agents-sdk/lib/keychain.py set ldr_username sean
     python3 agents-sdk/lib/keychain.py set ldr_password '<generated>'
     ```
     (These overwrite any MBP-era entries — the agent on Mac Mini will read the Keychain on Mac Mini, so this is correct.)
  8. Configure LDR via REST (settings live in encrypted SQLite, not `settings.toml`). Write a one-shot Python helper at `~/Code-Brain/local-deep-research-stack/configure_ldr.py` that logs in (CSRF + cookie), then PUTs each setting to `/settings/api/<key>`:
     ```
     llm.provider              = "OLLAMA"
     llm.ollama.url            = "http://localhost:11434"
     llm.model                 = "qwen3-14b-research"   # the Modelfile-built tag, /no_think baked in
     search.tool               = "searxng"
     search.searxng_url        = "http://localhost:8080"
     search.iterations         = 2
     search.max_results_per_query = 5
     ```
     (This script's structure should mirror the agent's REST flow at `agents-sdk/agents/deep_researcher.py:154-188` — same login dance, same `X-CSRFToken` header on PUTs.)
  9. From the LDR Web UI (`localhost:5050`), submit a one-line "quick research" query like *"What is SearXNG"* — confirm it returns inside 5 min with at least 3 citations and no `<think>` artifacts.
- **Test:** UI query passes; topical report renders inline; no error toast.
- **Time:** 50 min.
- **Rollback:** `rm -rf ~/Code-Brain/local-deep-research-stack/.venv ~/Library/Application\ Support/local-deep-research/`. No global system changes.

### Phase 4 — Manual research run from agent path on Mac Mini hardware (25 min)

- **Goal:** Validate the *exact* code path that launchd will run — `deep_researcher.py --mode oneshot --query "..."` against the Mac Mini's Ollama/SearXNG stack, with M4 Pro 24 GB performance characterized.
- **Steps:**
  1. Ensure `[agents.deep_researcher].enabled = true` in `agents-sdk/config.toml` (already is — confirm).
  2. The agent reads `ldr_base_url = "http://localhost:5050"` (already correct — same on both machines).
  3. Run dry-run first:
     ```
     cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk
     PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode oneshot \
       --query "Compare GGUF vs MLX inference speed on Apple M4 Pro for 14B-class language models" \
       --dry-run
     ```
     Expected: prints config, base_url, anchor, no LDR call.
  4. Live run:
     ```
     time PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode oneshot \
       --query "Compare GGUF vs MLX inference speed on Apple M4 Pro for 14B-class language models"
     ```
     Watch `vault/90_system/agent-logs/deep-researcher-*.log`.
  5. While running, in a separate terminal: `top -o MEM -n 5 -l 10` — capture peak RSS for `ollama`, `Docker`, `python3`. Record in `vault/90_system/agent-logs/macmini-deepresearch-baseline-{date}.txt` from Phase 0.
- **Test:** All five §5 smoke-test pass criteria met. Wall time: **6-12 min** acceptable; **>15 min** = problem (likely SearXNG throttling, context overflow, or Ollama swap thrash).
- **Time:** 25 min (script + 8-12 min generation + observation).
- **Rollback:** Delete the topical note + queue mutation; agent's writes are scoped and reversible via `git checkout`.

### Phase 5 — New skill: `deep-research-queue` (45 min)

- **Goal:** Skill that teaches Claude in interactive sessions how to add good queries to `vault/00_inbox/research-queue.md` and what makes a research-worthy question.
- **Files:**
  - Create: `.claude/skills/deep-research-queue/SKILL.md`
  - Create: `.claude/skills/deep-research-queue/examples.md` (optional reference)
- **SKILL.md frontmatter (concrete):**
  ```yaml
  ---
  name: deep-research-queue
  description: Queue research topics into vault/00_inbox/research-queue.md for the
    autonomous deep_researcher agent to process overnight. Use when Sean asks to
    "queue research", "add to research queue", "research this later", or surfaces
    a question during work that needs ≥5 min of multi-source synthesis. Triggers
    when the question is not answerable in-session OR would consume too many
    tokens vs deferring to local LDR + Qwen3-14B at $0/run. Skip for: simple
    factual lookups, code questions, or anything Sean wants answered now.
  ---
  ```
- **Body (sections, with concrete content):**
  1. **When to queue vs answer in-session** — decision tree: (a) factual one-look-up → answer; (b) multi-source synthesis with ≥3 citations needed → queue; (c) question with a deadline within an hour → answer in-session even if expensive; (d) Sean explicitly says "queue" → always queue.
  2. **Question quality rules** — what makes a good research-queue question (specific, falsifiable, time-scoped, citation-friendly). Anti-patterns: vague ("tell me about AI"), unanswerable ("predict the market"), too-narrow (single-fact lookups).
  3. **How to queue** — open `vault/00_inbox/research-queue.md`, append `- [ ] {refined question}` on a new line. Show before/after diff. Note: do NOT add timestamps or metadata — the agent rewrites the line on completion with its own timestamp + wikilink.
  4. **What happens after queueing** — `deep_researcher` fires nightly at 02:45 on Mac Mini, picks the first `- [ ]`, runs LDR, writes a topical report at `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md`, injects a digest line under `<!-- research-digest -->` in today's daily note, and rewrites the queue line to `- [x] {question} — done {ts} → [[link]]`.
  5. **Cost / latency expectation** — $0/run, 5-12 min of Mac Mini compute at 02:45. Quality is "trustworthy first draft" not "Perplexity DR replacement"; treat outputs as starting points.
  6. **Allowed tools** — `Read`, `Edit` on `vault/00_inbox/research-queue.md` only. No vault_inject, no agent-side launching.
- **Test:** In a fresh interactive Claude Code session, ask *"queue research on whether SearXNG can survive 50 concurrent queries"* — Claude reads the skill, edits the queue file, confirms back. Then `cat vault/00_inbox/research-queue.md` — last line is `- [ ] {refined version of the question}`.
- **Time:** 45 min (writing + a verification round in a fresh session).
- **Rollback:** `rm -rf .claude/skills/deep-research-queue/`. No other touchpoints.

### Phase 6 — Extend the existing agent (no rewrite) (20 min)

- **Goal:** Make the agent machine-aware so the config block honestly reflects where it now runs, without changing the runtime path (still `localhost:5050`).
- **Files:**
  - Modify: `agents-sdk/config.toml:153` — change `target_machine = "macbook_pro"` → `target_machine = "mac_mini"`.
  - Modify: `agents-sdk/config.toml:263` — change `deep_research = { model = "qwen3-14b", machine = "macbook_pro" }` → `deep_research = { model = "qwen3-14b-research", machine = "mac_mini" }`. (Reflects the Modelfile tag *and* the new host. Still informational — agent doesn't read it; runtime machine is wherever launchd fires.)
  - Modify: `agents-sdk/agents/deep_researcher.py:96` — change the topical-note frontmatter line `model qwen3-14b` → `model qwen3-14b-research` so reports are honestly attributed.
- **Do NOT change:**
  - `ldr_base_url = "http://localhost:5050"` — stays. The agent runs on whichever machine launchd fires it from; the localhost convention IS the machine-awareness.
  - REST endpoint logic (login, start, status, report fetch) — proven on MBP; no reason to touch.
  - `_run_ldr` signature — keep stable since the dry-run path and any future Phase 9 wrapper depend on it.
- **Test:** `PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode queue --dry-run` prints the new model name and `mac_mini` is consistent across logs.
- **Time:** 20 min (3 small edits + dry-run).
- **Rollback:** `git restore agents-sdk/config.toml agents-sdk/agents/deep_researcher.py`.

### Phase 7 — Vault template (already shipped; one-line check) (5 min)

- **Goal:** Confirm the digest landing zone exists and works end-to-end.
- **Steps:**
  1. `grep -n "research-digest" vault/90_system/templates/tpl-daily.md` → expect line 37 (already present per discovery).
  2. Open today's daily note (`vault/10_timeline/daily/{today}.md`). If `<!-- research-digest -->` is absent, the template was applied before the v3.21.0 anchor add — manually paste the same `## Deep Research\n<!-- research-digest -->` block once for today; future days inherit it from the template.
- **Test:** `inject_at_anchor` (used by the agent at line 120) succeeds against today's daily note.
- **Time:** 5 min.
- **Rollback:** N/A (no mutation unless backfilling today's note).

### Phase 8 — launchd schedule on Mac Mini + non-overlap verification (15 min)

- **Goal:** Plist symlinked into `~/Library/LaunchAgents/`, loaded, fires at 02:45 on Mac Mini.
- **Steps:**
  1. Confirm plist `WorkingDirectory` and `ProgramArguments` paths are correct on Mac Mini (they are — repo path is identical; `agents-sdk/.venv/bin/python3` exists per the `claude` CLI being on PATH).
  2. Run `./agents-sdk/schedules/install_schedules.sh` — symlinks every `.plist` in the schedules dir into `~/Library/LaunchAgents/` and `launchctl load`s them. **Side-effect to know:** this re-loads ALL schedules, not just the new one. The script is idempotent (unloads first if already loaded), so existing 11 agents are unaffected. If you want to load only `deep-researcher`:
     ```
     ln -sf "$PWD/agents-sdk/schedules/com.sean.agent.deep-researcher.plist" ~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist
     launchctl load ~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist
     ```
  3. Verify: `launchctl list | grep deep-researcher` → returns one line.
  4. Confirm schedule choice doesn't collide with anything Mac-Mini-resident:
     - `02:00` vault-indexer (Mac Mini, ~10-15 min, frees 02:15) ✓
     - `02:30` vault-synthesizer (MBP — *different machine*, irrelevant for Mac Mini memory) ✓
     - `06:30` meta-agent (Mac Mini, but ≤5 min and 4 hr later) ✓
     - `08:45` daily-driver morning (Mac Mini, but ≥5 hr after deep-researcher's 15-min cap) ✓
     - **Verdict: 02:45 stays.** Mac-Mini-resident agents do not overlap.
  5. Trigger a manual fire to confirm launchd config is syntactically correct (do this at a time when SearXNG + LDR + Ollama are all up):
     ```
     launchctl start com.sean.agent.deep-researcher
     ```
     Then `tail -f vault/90_system/agent-logs/deep-researcher-stdout.log`.
- **Test:** Manual `launchctl start` fires the agent end-to-end. Tomorrow morning: `cat vault/90_system/agent-logs/agent-run-history.csv | grep deep-researcher` shows a 02:45 entry.
- **Time:** 15 min (5 min install, 10 min manual fire observation).
- **Rollback:** `launchctl unload ~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist && rm ~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist`. The repo plist is untouched.

### Phase 9 — MCP server hookup on Mac Mini (optional, 30 min)

- **Goal:** Interactive Claude Code sessions on the Mac Mini can call `ldr.research(...)` as a tool, just like the MBP path.
- **Steps:**
  1. The `.mcp.json:16-20` `ldr` entry points at `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py`. That path didn't exist on Mac Mini before this plan; Phase 3 created the venv. Copy or recreate `bin/ldr-mcp-wrapper.py` on Mac Mini, but with the **OLLAMA overrides instead of LMSTUDIO**:
     - Change the monkey-patched `create_settings_snapshot` to inject `llm.provider = OLLAMA`, `llm.ollama.url = "http://localhost:11434"`, `llm.model = "qwen3-14b-research"`, `search.tool = "searxng"`, `search.searxng_url = "http://localhost:8080"`.
     - The wrapper is ~70 lines per the v3.21.0 deltas; adapt the existing MBP version field-by-field.
  2. The shipped `.mcp.json` already has `"ldr"` in `mcpServers` and `.claude/settings.local.json` already has `"ldr"` in `enabledMcpjsonServers` — **no settings file edits required** if Mac Mini reuses the same checkout. Confirm with `grep -n ldr .mcp.json .claude/settings.local.json`.
  3. Restart Claude Code → run `/mcp` → `ldr` should appear with 8 tools (FastMCP 1.27.0 baseline).
  4. Smoke test: in a fresh session, *"use the ldr tool to research what is SearXNG"* — expect 1-5 min response with citations.
- **Test:** Tool appears in `/mcp` list; one synthetic query returns coherent output with citations resolving (no 404).
- **Time:** 30 min (wrapper port + smoke test).
- **Rollback:** Remove the wrapper file or remove `"ldr"` from `enabledMcpjsonServers` in `.claude/settings.local.json`.
- **Maintenance debt to inherit:** Per the v3.21.0 Phase 6 delta, the wrapper monkey-patches LDR's `settings_utils.create_settings_snapshot`. If LDR refactors that module, the patch breaks silently → tool calls fall back to LDR defaults (`OLLAMA + gemma3:12b`) and may fail or hallucinate. Re-test after every `pip install --upgrade local-deep-research`.

### Phase 10 — Mandatory doc updates (25 min)

Per the CLAUDE.md non-negotiable: any new Skill, Agent, Hook, or Script must update CHANGELOG.md, CLAUDE.md, README.md. This phase ships the **`deep-research-queue` skill** (new) plus a **migration entry** for the agent (existing).

- **CHANGELOG.md** — new `## [3.23.0] - YYYY-MM-DD` section:
  - **Added:** `deep-research-queue` skill at `.claude/skills/deep-research-queue/SKILL.md`. Mac Mini SearXNG container, Ollama `qwen3-14b-research` Modelfile, Mac Mini LDR install at `~/Code-Brain/local-deep-research-stack/`, Mac Mini Keychain entries `ldr_username` / `ldr_password`, Mac Mini `ldr-mcp-wrapper.py` variant if Phase 9 done.
  - **Changed:** `agents-sdk/config.toml` `[agents.deep_researcher].target_machine` `"macbook_pro"` → `"mac_mini"`. `[routing.task_map].deep_research` `qwen3-14b` → `qwen3-14b-research` and machine to `mac_mini`. `agents-sdk/agents/deep_researcher.py:96` model attribution string.
  - **Notes:** Mac Mini production migration — frees the deep-research stack from MBP availability. Memory budget table documented for future schedule additions.

- **CLAUDE.md updates:**
  - Skills count: **114 → 115** (add `deep-research-queue`). Update header line and the domain table row that owns deep research (likely `creative-studio/` or `claude-mastery/` — currently the existing `research-synthesis` skill lives in `creative-studio/`; place the new skill there too OR in `life-systems/` if framed as a personal-knowledge tool — recommend **`creative-studio/`** since LDR's outputs feed downstream creative work and `research-synthesis` is already a sibling).
  - Active SDK agents table: bump deep_researcher row's machine from MBP → **Mac Mini** in both the description and the cost note (it remains $0.00). Bump v3.21.0 reference to v3.23.0 if the row cites version.
  - Architecture diagram comment block: skill count `(114)` → `(115)` in the `.claude/skills/` line.

- **README.md updates:**
  - Header line: "114 skills, 13 Claude Code subagents, 13 hooks, 13 autonomous SDK agents (7 active)" → "**115** skills, ...".
  - Any agents-table row for deep_researcher: machine column → Mac Mini.

- **Test:** `python3 scripts/validate.py` exits 0. Counts match across the three files (run `grep -c '^- ' .claude/skills/*/SKILL.md | wc -l` to ground-truth the skill count if uncertain).

- **Time:** 25 min.

---

## 4. Concrete Integration Specs (the new agent + the new skill)

### Agent

- **File:** `agents-sdk/agents/deep_researcher.py` — **already exists; do NOT rewrite.** This plan only edits the model attribution string (Phase 6).
- **Pattern note (correction to the original task brief):** The agent does NOT use the daily_driver Claude SDK loop pattern, by deliberate v3.21.0 design (v3.21.0 §8 delta: *"the deep_researcher is a pure-Python wrapper because LDR + Qwen3-14B IS the synthesis engine — no Claude in the loop"*). It does mirror daily_driver's *structural* conventions: argparse, `lib/config.py:load_config`, `lib/keychain.py:get_credential`, `lib/vault_io.py:inject_at_anchor`, `lib/logging_setup.py:record_run`. That structural mirroring is correct and stays.
- **Skills loaded** (decorative, since no SDK loop reads them): `["research-synthesis", "vault-read-write"]` — kept for parity with the daily-driver pattern; the `agents-sdk/lib/skill_loader.py:load_skills(...)` call is not invoked.
- **Anchor:** `<!-- research-digest -->` (already in `vault/90_system/templates/tpl-daily.md:37`).
- **Anchor location:** today's daily note at `vault/10_timeline/daily/{YYYY-MM-DD}.md`. If anchor missing, agent appends a `## Deep Research` section with the anchor as a fallback (`deep_researcher.py:111-125`).
- **Topical reports:** `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` (auto-created).
- **Schedule:** **02:45 daily** on Mac Mini. Non-overlap verified §1.
- **`max_turns`:** 30 (decorative — pure Python loop, no agent turns).
- **`max_budget_usd`:** 0.10 — keep as guard against unintended cloud fallback. **Argument for keeping:** the agent doesn't make Anthropic API calls, but `lib/config.py` may eventually be reused by a future hybrid path; the cap costs nothing and is one fewer surprise in the audit log. **Argument for zeroing:** could mislead readers into thinking there's a cloud path. **Recommendation: keep at 0.10** — trivial guard, matches the precedent set by other "all-local" agents (`vault_indexer = 0.00`, but `meta_agent = 0.10` for the same defensive reason).
- **Allowed tools:** N/A — the agent uses Python `httpx` + filesystem; no Claude tool whitelist applies. **Inheritance check:** the agent runs *outside* Claude Code, so the `block-secrets` PreToolUse hook does not fire on it. `setting_sources=["project"]` does not apply (no SDK options object). The `block-secrets` guarantee in CLAUDE.md applies to interactive sessions and SDK-loop agents — this agent is neither. **This is a real gap to acknowledge in §6.**
- **Failure modes (autonomous handling, no human present):**
  1. **Empty queue** → log `empty-queue` to history.csv, exit 0 (`deep_researcher.py:259-265`). Already implemented.
  2. **LDR not running (port 5050 closed)** → httpx `ConnectError`, agent logs `LDR call failed` and exits 3. Already implemented at line 299-308. Pushover does not fire — `notify_on = ["agent_error", ...]` requires a Python-side hook the wrapper doesn't currently install. **Gap to flag in §6.**
  3. **LDR auth rate limiter (429)** → agent has `try/except` but no retry; logs error and exits. Per v3.21.0 §8 delta, login session is cached per run, so rate-limit is unlikely on a single 02:45 fire.
  4. **LDR research timeout (>900s)** → agent raises and exits cleanly with `error` status logged to history.csv. Already implemented at line 213-214.
  5. **SearXNG empty results** → LDR returns a low-citation report; agent still writes it. The 14B + thin-source combo is the most common cause of fabricated citations; mitigated by a future URL-checker (out of scope this round, see §6 risk 4).

### Skill (`deep-research-queue`)

- **File:** `.claude/skills/deep-research-queue/SKILL.md` (new — full body in Phase 5).
- **Domain:** `creative-studio/` (sibling to `research-synthesis`).
- **Trigger description (excerpt):** *"Use when Sean asks to 'queue research', 'add to research queue', 'research this later', or surfaces a question during work that needs ≥5 min of multi-source synthesis."*
- **Allowed tools (skill-level — these are recommendations to the LLM, not enforcement):** `Read`, `Edit` on `vault/00_inbox/research-queue.md`. No vault_inject. No subprocess.

---

## 5. Smoke Test Query (validates the full chain end-to-end on Mac Mini)

**Query:**
> *"Compare GGUF vs MLX inference speed on Apple M4 Pro hardware for 14B-class language models. Cite at least three independent sources from 2025-2026 with numeric tok/sec measurements."*

**Why this query:**
- Multi-source factual; forces SearXNG to find real benchmarks.
- Numeric content makes hallucination immediately falsifiable.
- Topic is exactly the runtime-tradeoff question the synthesis flagged for the Mac Mini path → the *agent itself* will produce the canonical answer to the question its existence depends on.

**Expected output characteristics on Mac Mini M4 Pro 24 GB (Qwen3-14B Q5_K_M, 2 iterations, `num_ctx 16384`):**
- **Length:** 600-1,500 words.
- **Structure:** intro / per-source numeric findings / synthesis / source list.
- **Citations:** ≥3 distinct URLs; ≥2 of 2 spot-checked must resolve (no 404).
- **Numeric content:** ≥2 explicit tok/s figures.
- **No `<think>` tags anywhere** — confirms `qwen3-14b-research` Modelfile worked.
- **Wall time:** **8-14 minutes.** MBP M4 Pro 48 GB ran ~9 min; Mac Mini M4 Pro 24 GB has same chip class, narrower memory bandwidth → expect ~10-30% slower. >15 min = something is wrong (SearXNG throttled, Ollama swapping, KV-cache pressure).
- **Pass criteria:** all five bullets met. Any miss → debug before Phase 5.

---

## 6. Risks and Decision Points

### Risks specific to running this stack alongside daily-driver on 24 GB

1. **Memory pressure if a future operator adds an agent at 02:45-03:00.** Current schedule has the LDR run alone in that window; adding any concurrent Mac-Mini-resident agent that loads its own model breaks the headroom math (§1). **Mitigation:** add the schedule-conflict check from Phase 0 to the CLAUDE.md "When Modifying" checklist alongside the existing skill-count rule.
2. **Ollama keep-alive interaction with vault-indexer.** `OLLAMA_KEEP_ALIVE` defaults to 5 min; vault-indexer at 02:00 uses `nomic-embed-text` (~300 MB) and finishes by 02:15. By 02:45, embed model is unloaded. But if vault-indexer ever switches to a larger embedder, both could be resident. **Mitigation:** none required today; flag in CLAUDE.md if/when vault-indexer's model changes.
3. **SearXNG upstream throttling at the small daily volume planned (1-3 questions/night) is unlikely** — but a queue burst (Sean queues 20 questions in one day) would hit it, since the agent processes *one* per night and the queue compounds. **Mitigation:** the agent picks one per night, so backlog grows but throttle pressure stays constant. No change needed; document in the skill (Phase 5).
4. **Hallucinated citations from Qwen3-14B** — same issue as MBP path. The 20-line URL-checker post-processor recommended in the synthesis was **not implemented** in v3.21.0 and is **out of scope here**. Risk profile is unchanged. **Mitigation:** flag in Phase 5 skill body so Sean treats outputs as drafts with citation-checking expected.
5. **MCP wrapper monkey-patch fragility** — if Phase 9 ships, the wrapper depends on LDR's internal `settings_utils.create_settings_snapshot`. LDR refactor → silent fallback to `OLLAMA + gemma3:12b` defaults → wrong-model research that *still returns plausible-looking output*. **Mitigation:** add a wrapper-side smoke test that asserts `llm.model == "qwen3-14b-research"` after the patch and logs to stderr if not. Existing v3.21.0 risk; carries over.
6. **Agent does NOT inherit the `block-secrets` PreToolUse hook.** Hooks fire on Claude Code tool invocations; this agent doesn't use Claude Code tools — it's pure Python. The CLAUDE.md autonomous-agent rules around `setting_sources=["project"]` don't bind here. **Practical impact:** the queue file and topical reports are local-only and Sean-authored, so secret-leak risk is low — but the rule's spirit (defense in depth) is bypassed. **Mitigation:** add a one-line regex check at the top of `_build_topical_note` that strips obvious patterns (AWS keys, API tokens) from `summary` before write. Out of scope this round; flag for follow-on.

### Genuine forks for you to decide

- **D1 — Should the agent run on a fixed schedule, only on-demand via Phase 9 MCP, or both?**
  Current shipped: scheduled (02:45) + interactive MCP both available (Phase 9 was completed on MBP).
  Default recommendation: **keep both.** Schedule processes the queue overnight; MCP handles "I want this answered now" inside a session. They write to separate paths (scheduled = daily-note digest; MCP = inline tool result returned to Claude), so no collision. The cost (~30 min Phase 9 work + maintenance debt on the wrapper) is small.
  Alternate: **scheduled only.** Skip Phase 9, document MCP availability as MBP-only. Saves the wrapper-port maintenance burden but loses interactive parity.
  Pick: **both** — the MCP cost is small, the optionality is real.

- **D2 — Q5_K_M vs Q4_K_M as the Mac Mini default model quant.**
  Q5_K_M (~10.5 GB): synthesis-recommended, slight quality bump, ~1.9 GB peak headroom.
  Q4_K_M (~9.0 GB): more headroom (~3 GB peak), measurable but minor quality dip on instruction-following.
  Pick: **Q5_K_M default; document the Q4 escape hatch.** If a future memory-pressure incident occurs (third agent added to the 02:45 window, OS bloat, etc.), swap Modelfile `FROM qwen3:14b` → `FROM qwen3:14b-q4_K_M` and rebuild — single-line change.

### Deferred Phase 7 — Model A/B (re-scoped 2026-05-02 against current Ollama landscape)

Original MBP plan §3 Phase 7 candidates were Qwen3.6 27B Dense and Qwen3.6 35B-A3B MoE, gated on ≥1 week of clean baseline runs.

**Re-scoped Mac Mini candidate set** (because the 24 GB ceiling and the 1-week-old Qwen3.6 release reshape the field):

1. **Qwen3-14B (current default — control)** — production baseline.
2. **Qwen3.6 27B at Q4_K_M with `num_ctx` cut to 12K** — closes the 24 GB gap but only barely. Test for whether the quality bump is worth the memory squeeze and ~2× wall-clock time.
3. **Gemma 4 26B (already on disk at `gemma4:26b`)** — free to test, marketed as "frontier-level... agentic workflows," same size class as Qwen3.6 27B. Different family = different failure modes.
4. **Ministral 3 14B** — recent (4 months old) direct-replacement at the same size class. Lowest-risk upgrade path if Qwen3-14B underwhelms but the 27B options are too memory-tight.

Drop from candidates: Qwen3.6 35B-A3B (24 GB on disk = won't fit alongside anything), Qwen2.5-Coder-32B (coder family — wrong tool for synthesis).

**Trigger:** ≥1 week of clean Mac Mini run history on the 14B baseline AND a corpus of ≥5 real research-queue questions to score against. Re-use the original MBP Phase 7 scoring matrix.

---

## 7. Mandatory Doc Updates (per CLAUDE.md non-negotiable)

| File | Specific change | Counts before → after |
|---|---|---|
| `CHANGELOG.md` | New `## [3.23.0]` section with Added / Changed / Notes per Phase 10. | n/a |
| `CLAUDE.md` | Header skill count `114 → 115`; architecture comment skill count `(114) → (115)`; Active agents table — `deep_researcher` machine column `MBP → Mac Mini`. The "13 autonomous SDK agents (7 active)" tally is unchanged (deep_researcher was already in the active 7). | 114 skills → 115; agents 13 (7 active) unchanged |
| `README.md` | Header line `114 skills` → `115 skills`. Any agent table row that names deep_researcher's host. | Same as CLAUDE.md |
| `scripts/validate.py` | Run after edits; expect 0 errors. The validator hard-enforces the 3 primary domain folders and skill counts in playground manifests. | n/a |
| `export-groups/*/playground.json` | If `deep-research-queue` is added to the `creative-studio` export group, append it to the relevant `playground.json` skills list. | One manifest gets one new entry |

**Total artifacts touched in Phase 10:** 4 files in repo + 1 export-group manifest.

---

## 8. Out of Scope

- Fine-tuning any model.
- Custom Docker images (only `searxng/searxng:latest`).
- Vector DB / private-document RAG (LDR supports it; not needed for v1).
- A URL-checker post-processor for citation validation (deferred — see risk #4; estimate 30 min of Python when prioritized).
- A secrets-strip pre-write filter for topical notes (deferred — see risk #6).
- Hybrid cloud-fallback to paid Perplexity DR or Claude Code for "high-stakes" queries (was D2 in the MBP plan; remains deferred until ≥2 weeks of Mac Mini run history exists).
- Removing the MBP install. The MBP setup remains as a fallback for ad-hoc daytime runs (e.g., MCP from a session opened on the MBP). Do NOT decommission until Mac Mini has 30 days of clean schedule history.
- Decommissioning the existing `target_machine = "macbook_pro"` route in `[routing.task_map].deep_research` — Phase 6 changes this in place; if the MBP is ever needed as a fallback host, reverting is a one-line edit.
- Phase 7 of the prior MBP plan (Qwen 3.6 27B / 35B-A3B model A/B) — **DO NOT START** until ≥1 week of clean Mac Mini run history exists, per the original gating rule. Use the re-scoped candidate set in §6 above.
- Any change to `daily_driver.py` to consume research outputs — research stays a separate agent; daily-driver may *read* outputs in a future iteration via vault Read in its morning prompt.

---

## Verification Section (end-to-end test plan, post-Phase 8)

After Phase 8 completes, run this sequence to confirm the full pipeline on Mac Mini:

1. **Add a question:** Append `- [ ] What are the practical differences between Ollama Modelfile SYSTEM prompts and runtime system messages for Qwen3?` into `vault/00_inbox/research-queue.md`.
2. **Dry run:** `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode queue --dry-run` — verify it prints the question + intended LDR call.
3. **Live run:** Same command without `--dry-run`. Watch logs at `vault/90_system/agent-logs/deep-researcher-*.log`.
4. **Inspect outputs:**
   - `vault/00_inbox/research-queue.md` — question marked `- [x]` with timestamp + output link.
   - `vault/20_projects/research/{date}-{slug}.md` — full report with citations, no `<think>` tags.
   - Today's daily note has a one-line digest under `<!-- research-digest -->` linking to the report.
5. **launchd test:** Manually trigger via `launchctl start com.sean.agent.deep-researcher`; confirm same output and the next-day 02:45 fire produces an entry in `agent-run-history.csv`.
6. **MCP test (if Phase 9 done):** Open a fresh Claude Code session on Mac Mini, run `/mcp` — confirm `ldr` listed; ask "use the ldr tool to research X"; verify equivalent output.

If all six steps pass, the stack is production-ready on Mac Mini.

---

## Critical files to be created or modified

**New files (in repo):**
- `.claude/skills/deep-research-queue/SKILL.md` (Phase 5)
- `.claude/skills/deep-research-queue/examples.md` (Phase 5, optional)

**Modified files (in repo):**
- `agents-sdk/config.toml` — `target_machine` and `deep_research` task_map entries (Phase 6)
- `agents-sdk/agents/deep_researcher.py:96` — model attribution string (Phase 6)
- `CLAUDE.md`, `README.md`, `CHANGELOG.md` — counts + tables (Phase 10)
- `export-groups/*/playground.json` — new skill manifest entry (Phase 10)

**New files (outside repo):**
- `~/Code-Brain/local-deep-research-stack/` — Python 3.11 venv, settings volume, Modelfile, configure_ldr.py
- `~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py` — Mac Mini variant with OLLAMA overrides (Phase 9, optional)
- `~/Library/LaunchAgents/com.sean.agent.deep-researcher.plist` — symlink to repo plist (Phase 8)
- macOS Keychain entries: `com.sean.agents.ldr_username`, `com.sean.agents.ldr_password`

**Existing utilities to reuse (do not duplicate):**
- `agents-sdk/lib/vault_io.py:inject_at_anchor` — anchor injection
- `agents-sdk/lib/vault_io.py:daily_note_path` — daily note resolution
- `agents-sdk/lib/config.py:load_config` — config + routing
- `agents-sdk/lib/keychain.py` — credential storage
- `agents-sdk/lib/logging_setup.py:record_run` — agent run logging
- `agents-sdk/agents/deep_researcher.py` — already shipped; structural pattern to preserve
- Skills: `research-synthesis`, `vault-read-write`

---

## Self-Check (per writing-plans skill)

1. ✅ Read all three source files + the prior MBP plan (full body + execution deltas §8).
2. ✅ Inventoried Mac Mini: ollama models present, Docker daemon down, no LDR install, no `qwen3:14b`, 24 GB RAM, 147 GB disk, Python 3.9.6 + uv 0.10.3.
3. ✅ Model + search backend calibrated for 24 GB + Ollama-only: Qwen3-14B Q5_K_M default, no stretch tier, GGUF (no MLX), Q4 fallback documented. Larger candidates (Qwen3.6 27B, Gemma 4 26B) verified against ollama.com on 2026-05-02 and rejected for v1 on memory grounds; deferred to a re-scoped Phase 7.
4. ✅ Agent integration follows existing structural pattern (argparse, lib/* imports). Plan correctly identifies that the daily_driver SDK-loop pattern is *not* used here by deliberate v3.21.0 design and explains why.
5. ✅ Anchor name `<!-- research-digest -->` and template location `vault/90_system/templates/tpl-daily.md:37` are concrete; verified present today.
6. ✅ CHANGELOG/CLAUDE.md/README.md updates listed with explicit count deltas (114 → 115 skills).
7. ✅ Memory pressure with concurrent daily-driver + LDR + Ollama + SearXNG quantified (§1 table, ~22.1 GB peak, ~1.9 GB headroom). Schedule chosen for zero overlap.
8. ✅ 02:45 schedule does not overlap with daily-driver (08:45 / 17:00 / Fri 16:00) — verified by hour math, ≥5 hour gap.

---

End of plan. Ready to execute on user approval.

---

## 9. Execution Deltas (Phases 0–10 completed 2026-05-02 → 2026-05-03, shipped v3.23.0)

This mirrors the v3.21.0 §8 "Execution Deltas" section in `you-are-a-senior-modular-pelican.md`. Below are the corrections discovered during execution; the body of the plan above is the original brief.

### Phase 0 — vm_stat page-size correction
The plan §1 baseline math used `pages × 4 KB`. Apple Silicon uses **16 KB pages**, not 4 KB. Conclusion (~8.7 GB resident baseline / ~22 GB peak / ~1.4-1.9 GB headroom) holds; only the math needs the page-size fix. Recorded in `vault/90_system/agent-logs/macmini-deepresearch-baseline-2026-05-02.txt`.

A separate cosmetic finding: 12 `com.sean.agent.*.plist` files in `~/Library/LaunchAgents/`, only 11 loaded — `meeting-defender.plist` is a stale symlink left from before its 2026-04-27 retirement. Not a blocker for this migration; flag for cleanup in a future sweep.

### Phase 2 — Ollama Q5_K_M tag absent; Qwen3 thinking mode bypasses SYSTEM `/no_think`

Two interlocking issues:

1. **Q4_K_M only.** `ollama pull qwen3:14b` returns the registry default Q4_K_M (≈9.3 GB). No separate `qwen3:14b-q5_K_M` tag is exposed by the registry. Plan §2 documented this branch ("else accept Q4"). Q4 actually gives more headroom (~3 GB peak) than the plan's Q5 estimate (~1.9 GB peak); strictly safer.

2. **`SYSTEM """/no_think"""` does NOT disable Qwen3's thinking mode under Ollama 0.22.1.** Ollama models thinking as a separate top-level `thinking` field on the chat response, not as inline `<think>` tags. The stock `qwen3:14b` template injects `/no_think` into the user message tail ONLY when the API request includes `"think": false`. Generic Ollama clients (LDR included) don't pass that field, so the model defaults to thinking ON, burning 300-500 tokens per call on internal reasoning routed to the hidden `thinking` field.

   `PARAMETER think false` is rejected in Ollama 0.22.1 ("unknown parameter 'think'"). Fix: patch the TEMPLATE itself to (a) **unconditionally** append `/no_think` at the end of the last user message, and (b) pre-fill an empty `<think></think>` block in the assistant prefix. This makes the model behave as non-thinking by default for ANY caller, regardless of whether they pass the `think` API field.

   The patched Modelfile lives at `~/Code-Brain/local-deep-research-stack/qwen3-14b-research.Modelfile`. Verification: 8-token greeting in 282 ms (28.4 tok/s), no `thinking` field returned. **This made Phase 4 finish in 217s instead of the plan's 8-14 min budget** — no thinking overhead means generation is direct.

### Phase 3 — LDR v1.5.6 settings key schema shift + exact-match Ollama lookup + register-form checkbox value

Four interlocking findings, applied in `~/Code-Brain/local-deep-research-stack/configure_ldr.py`:

1. **`search.searxng_url` and `search.max_results_per_query` do not exist in v1.5.6.** Both return HTTP 404 from `/settings/api/<key>`. The per-engine schema moved them under `search.engine.web.searxng.default_params.{instance_url, max_results}`. Remaining keys (`llm.provider`, `llm.ollama.url`, `llm.model`, `search.tool`, `search.iterations`) keep the plan's names.

2. **Provider value case.** The `/settings/api/llm.provider` options list uses lowercase `"ollama"`; LDR ships defaulting to uppercase `"OLLAMA"`. Setting to `"ollama"` is accepted (HTTP 200) and matches the canonical options list value.

3. **Exact-match model lookup.** Setting `llm.model = "qwen3-14b-research"` produces a research-start failure at t≈4s with `metadata.error = "Model 'qwen3-14b-research' not found in Ollama"`. Ollama's `/api/tags` reports models built via `ollama create` with an explicit `:latest` suffix; LDR does an exact-string lookup. **Setting must be `qwen3-14b-research:latest`.** This delta carries through to the MCP wrapper (Phase 9) — same `:latest` requirement.

4. **Register form `acknowledge=true`.** The form uses `<input type="checkbox" name="acknowledge" value="true">`. WTForms accepts only the literal string from the input's `value` attribute — `acknowledge=on` and `acknowledge=y` both yield HTTP 400 with "You must acknowledge that password recovery is not possible". Use `acknowledge=true`.

The auth rate limiter on `/auth/login` (already documented in v3.21.0 §8) was reconfirmed — `pkill -f ldr-web` + restart clears the sliding window. The agent's pattern of "login once per run + reuse cookie" was inherited unchanged.

### Phase 4 — wall time vs plan estimate
Plan §5 expected **8-14 min** wall on M4 Pro 24 GB; actual was **217s (3.6 min)**. Root cause: the patched Modelfile (Phase 2 delta #2) eliminates Qwen3's thinking-token overhead entirely. For a 2-iteration synthesis with 4 LLM calls + final report, the saved overhead is ~80-100s per iteration. This is a quality-positive finding — keep Phase 7 model A/B's wall-clock budget calibration around the new baseline.

Side effect to note: the digest landing path used the `appended-section` fallback (not `injected`) because today's daily note lacked the `<!-- research-digest -->` anchor pre-run. The agent added a fresh `## Deep Research` section + anchor + line. Future daily notes that inherit the v3.21.0 template anchor will get the `injected` path. Not a regression.

### Phase 8 — single-load vs bulk install_schedules.sh
Used the plan's documented "load only deep-researcher" path (single `ln -sf` + `launchctl load`) instead of the bulk `install_schedules.sh`. Reason: `install_schedules.sh` symlinks every `.plist` in the schedules dir, which would also re-symlink the stale `meeting-defender.plist` (Phase 0 finding) into `~/Library/LaunchAgents/`. Single-load minimized blast radius without changing semantics.

### Phase 9 — `.claude/settings.local.json` is per-machine, not inherited
Plan §3 Phase 9 step 2 said the shipped `.mcp.json` and `.claude/settings.local.json` already have `"ldr"` so "no settings file edits required if Mac Mini reuses the same checkout." This is true for `.mcp.json` (committed) but **NOT** for `.claude/settings.local.json` — the `.local.json` suffix is gitignored (`.gitignore:2: **/.claude/settings.local.json`), so each machine has its own copy. The Mac Mini's pre-migration `enabledMcpjsonServers` was `["obsidian-vault", "zapier"]`; added `"ldr"` to make it `["obsidian-vault", "zapier", "ldr"]`. Per-machine, gitignored — does NOT appear in the v3.23.0 commit.

The wrapper itself was recreated from §8's architectural description (`~/Code-Brain/local-deep-research-stack/bin/ldr-mcp-wrapper.py`, ~80 lines incl. comments). Stdio handshake confirmed: FastMCP 1.27.0, 8 tools (`quick_research`, `detailed_research`, `generate_report`, `analyze_documents`, `search`, `list_search_engines`, `list_strategies`, `get_configuration`), and the in-process patch verification confirmed `mcp.server.create_settings_snapshot is _patched` plus all five Mac Mini overrides applied to default snapshots.

### Phase 10 — export-group placement
Plan recommended placing the new `deep-research-queue` skill in "creative-studio (sibling to research-synthesis)". Confirmed: skills physically live in `.claude/skills/<name>/` (flat layout), not in domain folders. The `research-synthesis` skill's export-group manifest is **`02-pm-workflows`**, not `03-creative-projects`. Added `deep-research-queue` to `02-pm-workflows/playground.json` (alphabetic insertion, sibling to `research-synthesis`). Domain-affinity-wise this is consistent with research-synthesis's PM framing.

### Decision points NOT triggered
- **D1 (interactive MCP via wrapper):** Triggered — Phase 9 shipped per plan recommendation.
- **D2 (Q5_K_M vs Q4_K_M):** Resolved at registry layer — no Q5_K_M tag exposed; Q4_K_M is the default and gives more headroom than plan's Q5 estimate. The escape hatch in plan §6 D2 is unchanged.

### Verified at install time

- Phase 4 oneshot: 1014 words, 23 distinct citations, 8 numeric tok/s figures, 0 `<think>` tags, wall 217s.
- Phase 8 launchd manual fire: `agent-run-history.csv` gained `2026-05-03,10:16:50,deep-researcher,queue,empty-queue,0.0000,,,no unchecked items` — confirms launchd → venv python → agent → `record_run` path is wired.
- Phase 9 stdio handshake: MCP `initialize` returns `{name: "local-deep-research", version: "1.27.0"}`, `tools/list` returns 8 tools.

The full pre-install state baseline + every delta hit during install lives at `vault/90_system/agent-logs/macmini-deepresearch-baseline-2026-05-02.txt`.
