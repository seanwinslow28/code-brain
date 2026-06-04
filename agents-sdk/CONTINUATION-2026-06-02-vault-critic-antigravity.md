# Continuation prompt — vault_critic Anti-Gravity (gemini) nightly timeout

> Paste the block below into a fresh Claude Code session in `~/Code-Brain/code-brain`.
> It is self-contained: it tells the next session what's already been proven, what's
> been ruled out, and exactly what to investigate next so no ground is re-covered.

---

## PROMPT (copy from here)

You are picking up an open investigation into the `vault_critic` nightly agent. Two prior sessions diagnosed and attempted a fix; the fix did **not** resolve it, but it produced new evidence. Your job has three parts, in order:

**Part 1 — Fleet sweep.** Give me a current health read on the whole autonomous agent fleet (the `agents-sdk/` launchd agents). Use: `launchctl list | grep com.sean`, the latest per-agent manifests in `vault/health/` (critic, synth, job-feed), the meta-agent's report at `vault/02_Areas/Agent-Fleet/daily-fleet-status-<today>.md`, the consolidated `vault/90_system/agent-logs/agent-run-history.csv`, and per-agent logs in `vault/90_system/agent-logs/`. Flag anything degraded. (Known-open secondary issues you can mention but not chase: meta-agent monitoring blind spot, job-feed ATS watchlist 404s — both ticketed.)

**Part 2 — Dig into the Anti-Gravity timeout (primary task).** Use the `systematic-debugging` skill. Do NOT propose a fix until you've found root cause. Here is the confirmed evidence so far:

CONFIRMED:
- `vault_critic` (`agents-sdk/agents/vault_critic.py`) runs nightly 03:30, shelling in parallel to Codex CLI and the "Anti-Gravity" CLI = Google `gemini` CLI on **personal OAuth** (`run_antigravity()` in `agents-sdk/lib/cli_runners.py`).
- Anti-Gravity has failed **5/5 every nightly run since 2026-05-26**. Codex succeeds every night (0 failures, ~140K tokens, same Python process, same 03:30 — so the network is up and it is gemini-specific).
- The 2026-06-02 manifest (`vault/health/critic-manifest-2026-06-02.json`), now carrying the instrumented error field, says: **`antigravity_last_error: "antigravity timeout after 120s"`**. Every AG call hangs to the full 120s per-CLI timeout. 5 × 120s = the 600s wall budget, which is why it "runs out after 5 articles."

RULED OUT (do not re-test these — they all PASS):
- The binary / OAuth / model access — the exact command works interactively, in a stripped `env -i`, under a real throwaway launchd job, and rapid-fire 5×, all in daytime.
- Prompt size (24K-token prompt returns in ~18s).
- **MCP servers** — this was the prior hypothesis and it's now disproven two ways: (a) Sean removed all `mcpServers` from `~/.gemini/settings.json` (it's now empty), and (b) the code already passes `--allowed-mcp-server-names __none__`. Yet it still times out.

NEW, MOST IMPORTANT CLUE (this is where to start):
- Before MCP removal, **zero** gemini session files existed for nightly runs (it died at startup). After MCP removal, the 2026-06-02 run **did** create a session stub: `~/.gemini/tmp/seanwinslow/chats/session-2026-06-02T07-38-8aecf757.jsonl` (07:38 UTC = 03:38 EDT). But that file is a **228-byte metadata-only stub** — `startTime == lastUpdated == 2026-06-02T07:38:06.598Z`, `kind: main`, and **zero conversation turns recorded**. So removing MCP moved the failure *later*: gemini now initializes the session, issues the model request, and then **hangs with no response (not a single token) until killed at 120s.** The hang is in the model request/stream at night, not startup. OAuth is likely fine (creds `expiry_date` ≈ 08:30 UTC was set ~1h after the 07:30 UTC run, consistent with a successful in-run refresh).

YOUR JOB for Part 2: find why a `gemini -p … --output-format json --approval-mode plan` request returns zero tokens and hangs to 120s at ~03:30 unattended, but completes in seconds during the day. The failure is bound to the unattended/nighttime condition and has resisted daytime reproduction, so prioritize getting evidence *from the failing condition itself* over more daytime repro. Concrete avenues:
  1. **Better instrumentation first.** `run_antigravity()` currently discards the gemini subprocess's stdout/stderr on timeout. Add a debug capture: on `asyncio.TimeoutError`, before/after `proc.kill()`, drain and write whatever partial stdout+stderr the process emitted to a timestamped file under `vault/90_system/agent-logs/` (e.g. `ag-timeout-<runid>.log`). That reveals what gemini last printed before hanging. Ship it, then trigger the real launchd job (`launchctl kickstart -k gui/$(id -u)/com.sean.agent.vault-critic`) — note this runs the full ~600s agent and overwrites today's outputs, so confirm with Sean first, or gate it behind `--max-targets 1 --per-cli-timeout-seconds 150`.
  2. **Headless/non-interactive gemini gotchas.** The `-p` help text says "Appended to input on stdin (if any)" — check whether the CLI blocks waiting on stdin under launchd (launchd gives it `/dev/null`, but verify; try invoking with stdin explicitly closed). Investigate whether gemini does an **update check**, **telemetry/usage-statistics consent**, **extension-integrity check**, or **IDE-companion handshake** at startup that can block headless. Look for env vars / flags to disable those (e.g. update-check disables, `--telemetry`/telemetry settings in `~/.gemini/settings.json`, `--yolo` vs `--approval-mode plan`).
  3. **Nighttime model/endpoint behavior.** Consider whether `gemini-3.1-pro-preview` (a *preview* model on personal OAuth) has a nighttime quota/availability window where the request stalls instead of erroring. Compare the request the CLI makes vs Codex's.
  4. **Machine state at 03:30.** This is a Mac Mini (always-on, not the Modern-Standby Alienware). Confirm it's truly awake/networked at 03:30 (codex working says yes, but verify the gemini-specific path — DNS to Google endpoints, IPv6, proxy/VPN state at night).

**Part 3 — Research (do this in parallel with Part 2, dispatch a subagent).** Research real-world `gemini` CLI (google-gemini/gemini-cli) usage and known failure modes, focused on: headless/non-interactive (`-p`) hangs and timeouts; CI/cron/launchd usage; stdin blocking; update-check / telemetry / first-run consent prompts that block non-interactively; OAuth-personal token refresh in unattended contexts; and any `--output-format json` + `--approval-mode plan` interactions. Pull from the gemini-cli GitHub issues/discussions and docs (use WebSearch/WebFetch — load via ToolSearch). Produce a short ranked list of "things known to make gemini-cli hang headless" mapped against our evidence (zero-token 120s hang, post-session-creation, nighttime-only). Recommend the single highest-probability cause and the cheapest decisive test for it.

Deliverable: a fleet status summary, a root-cause finding (or, if unconfirmed, the instrumentation shipped + the one decisive next experiment), and the research ranking. Capture any deferred follow-ups as tickets in `vault/00_inbox/tickets.md`. Don't claim the bug is fixed without evidence from a real nightly (or kickstarted) run.

Context docs: post-mortem at `agents-sdk/POSTMORTEM-2026-06-01-vault-critic-antigravity.md`; a one-time verification routine already exists (`trig_01W3WBjQ5fDe19n1RURpqvA2`). The prior fix (`--allowed-mcp-server-names __none__`) and instrumentation (`antigravity_last_error`/`codex_last_error` in the manifest) are already committed — build on them.

## (end of prompt)

---

### Quick-reference appendix (for whoever runs the next session)

**Key files**
- Invocation: [`agents-sdk/lib/cli_runners.py`](lib/cli_runners.py) → `run_antigravity()` (line ~175; timeout handler ~211 is where to add debug capture)
- Agent: [`agents-sdk/agents/vault_critic.py`](agents/vault_critic.py) (failure capture ~389; manifest payload ~125)
- Config: [`agents-sdk/config.toml`](config.toml) `[agents.vault_critic]` — `wall_budget_seconds=600`, `per_cli_timeout_seconds=120`
- gemini CLI config: `~/.gemini/settings.json` (mcpServers now empty), `~/.gemini/oauth_creds.json`, sessions in `~/.gemini/tmp/seanwinslow/chats/`
- Plist: `agents-sdk/schedules/com.sean.agent.vault-critic.plist` (logs → `vault/90_system/agent-logs/vault-critic-std{out,err}.log`)

**Evidence timeline**
- Last healthy nightly AG: 2026-05-23 (50K tokens). Broke 2026-05-26. 5/5 fail nightly since.
- 2026-06-01: fix #1 (disable MCP) + instrumentation shipped.
- 2026-06-02 nightly: still `timeout after 120s`, but now a session stub is created (failure moved from startup → model request).

**Decisive single test to aim for:** capture gemini's partial stdout/stderr at the moment of the 120s timeout during a real nighttime/kickstarted run. That output names the hang.

---

## Session 3 progress — 2026-06-02 midday (Claude Code)

**Shipped (committed-ready, not yet committed):**
- `lib/cli_runners.py` `run_antigravity()` rewritten: discard-on-timeout `communicate()` → **concurrent stream-pump** (`_pump_stream`) that accumulates stdout/stderr continuously, so a timeout now persists gemini's partial output to `vault/90_system/agent-logs/ag-timeout-<utc>.log` via `_write_ag_timeout_capture()`. Also: explicit `stdin=DEVNULL` (no-op on launchd, removes a daytime-repro variable) and an env-gated `VAULT_CRITIC_AG_DEBUG=1` that appends gemini's own `--debug`.
- `agents/vault_critic.py`: `critique_one_article()` passes `debug_log_dir=repo_root/vault/90_system/agent-logs`.
- `tests/test_cli_runners.py`: `_fake_proc` upgraded to the new proc interface (wait/stdout/stderr) + 2 new timeout-capture tests. 49 cli+critic tests pass; 63/64 full-suite files pass (the 1 hang is `tests/test_gemini_dr.py`, a pre-existing unmocked real-network test, unrelated).
- **Verified instrumentation end-to-end daytime:** forced timeout captured 13,703 bytes of gemini `--debug` stderr; success path still parses JSON+tokens (8.6s, 13,685 tokens).

**Root cause — high confidence, NOT yet proven from the failing condition:**
New local correlation rules out the auth-failure theories: `oauth_creds.json` `expiry_date`=08:30 UTC but the failing run's session stub started 07:38 UTC → **token was refreshed mid-run; OAuth succeeded.** `settings.json` shows `model.name=auto-gemini-3` + `previewFeatures:true` (a **preview model**, strict per-day quota). Fingerprint (auth ok → session created → request issued → zero turns → 120s hang) matches gemini-cli **issue #22648** (oauth-personal 429 RESOURCE_EXHAUSTED swallowed → silent indefinite hang). Nighttime-only is explained by **03:30 EDT = 00:30 Pacific = the daily-quota reset boundary** (#22643 quota-never-resets). Codex survives = separate quota path. Daytime reproduced as SUCCESS (8.6s), confirming the window-bound nature.

Research ranking: **#1 swallowed-429 quota hang** › #2 token-refresh-loss (RULED OUT) › #3 headless-login deadlock (RULED OUT) › #4 plan-mode approval wait › #5 first-run/DEBUG prompts.

**Decision (Sean, 2026-06-02):** capture tonight's real 03:30 run rather than a daytime kickstart (which won't reproduce). `VAULT_CRITIC_AG_DEBUG=1` added to `schedules/com.sean.agent.vault-critic.plist` EnvironmentVariables and launchd reloaded (verified in `launchctl print` env). 

**NEXT SESSION — check after 03:30 tomorrow:**
1. Read `vault/90_system/agent-logs/ag-timeout-*.log` (5 expected) + `critic-manifest-2026-06-03.json` `antigravity_last_error`. Look for `429`/`RESOURCE_EXHAUSTED`/`Quota`/`Request cancelled.` in the captured stderr → confirms #1.
2. If confirmed: migrate the nightly off oauth-personal to `GEMINI_API_KEY` (AI Studio, no daily cap) — also forced by the **oauth-personal-via-gemini-cli EOL June 18 2026**. Then **remove `VAULT_CRITIC_AG_DEBUG=1`** from the plist.
3. If the capture shows something else (startup hang, different error), re-rank.

---

## Session 4 progress — 2026-06-03 (Claude Code) — ROOT CAUSE REVISED

**The 6/02 #1 hypothesis (swallowed-429 quota hang) is REFUTED by the failing-condition evidence.**

The 03:30 6/03 nightly fired with `VAULT_CRITIC_AG_DEBUG=1` armed and produced 5 captures
(`vault/90_system/agent-logs/ag-timeout-2026-06-03T07-{32,34,36,38,40}-*.log`). Grepping all 5 for
`429|RESOURCE_EXHAUSTED|quota|Request cancelled|cloudcode-pa` → **zero hits**. With `--debug` on,
there is **not one line about the model request** (no GenerateContent, no stream, no quota error).

What the captures DO show: gemini gets through startup (~1.9s), `Loaded cached credentials` (OAuth
fine), creates the session stub, then the **only** network activity that logs anything is the Clearcut
telemetry flush — which fails with `TypeError: fetch failed → ConnectTimeoutError (attempted address:
play.googleapis.com:443, timeout: 10000ms) UND_ERR_CONNECT_TIMEOUT` on 4/5 runs (the 5th got
`HTTP 400`). Then silence to the 120s kill.

**Decisive control:** daytime `curl` to BOTH `play.googleapis.com` and `cloudcode-pa.googleapis.com`
connects in ~30–60ms on IPv4 AND IPv6 (http=404, frontend reached). So play.googleapis.com is NOT a
permanently-blocked telemetry host — its nightly connect-timeout is a real, time-correlated signal.

**Machine-state ruled out:** pmset log shows the Mac Mini was AWAKE across 03:25–03:45 (Claude.app
NoIdleSleep assertion), no sleep/darkwake/powernap. Route to Google IPs goes via en0→gateway, not any
utun/VPN. Codex pushed 145K tokens at the same 03:30 (bulk egress works). So: machine up, network up,
non-Google egress fine — **only Google API hosts are unreachable in the ~03:30 window.**

**ROOT CAUSE (class, high confidence):** gemini's model request to `cloudcode-pa.googleapis.com` can't
establish a TCP connection to Google's API frontend at ~03:30; with no short connect timeout it hangs
to the 120s kill (zero tokens). Codex/OpenAI are on different infra and unaffected. NOT quota, NOT auth,
NOT MCP, NOT machine-asleep.

**Sub-cause NOT yet discriminated** (IPv6-to-Google nighttime breakage vs general Google-ASN
reachability vs router/ISP nightly event). One daytime hint: `curl -6` to Google connected via an
IPv4-**mapped** address (`::ffff:...`), suggesting native IPv6 to Google may already route oddly.

**Shipped (uncommitted, repo):** `lib/cli_runners.py` — added `_probe_google_reachability()` +
`_run_probe_cmd()`; on an AG timeout (gated behind `VAULT_CRITIC_AG_DEBUG=1`, run-once/process) it now
appends a `===== CONNECTIVITY PROBE (post-timeout) =====` section to the capture file: IP-family-split
`curl -4`/`curl -6` connect timing to both Google hosts + dig A/AAAA + an `api.openai.com` control.
+2 unit tests (`tests/test_cli_runners.py`, 20/20 pass). Probe smoke-tested live (daytime baseline good).
Takes effect on tonight's run automatically (launchd re-imports the module per run; no reload needed).

**NEXT SESSION — check after 03:30 2026-06-04:**
1. Read the `===== CONNECTIVITY PROBE =====` section in the new `ag-timeout-2026-06-04T07-*.log`.
   - `curl6 *.googleapis.com: PROBE-TIMEOUT` while `curl4` connects AND `api.openai.com` connects
     → **IPv6-to-Google nighttime breakage** (fix: force gemini/undici to IPv4 at night, e.g.
     `NODE_OPTIONS=--dns-result-order=ipv4first` or disable IPv6 on the egress path).
   - BOTH curl4 and curl6 to Google PROBE-TIMEOUT while OpenAI control connects → **general Google-ASN
     reachability** (ISP peering / router nightly event); fix is reschedule or provider change.
   - Google connects fine in the probe but gemini still hung → the hang is inside the CLI's request
     path, not the network; re-open the gemini-cli-internals angle.
2. Regardless: oauth-personal EOL June 18 — migrate/replace the AG path (tickets logged).
3. Then remove `VAULT_CRITIC_AG_DEBUG=1` from the plist.

**Also shipped Session 4 — AG circuit breaker (budget protection, independent of root cause):**
Codex+AG run in parallel per article, so a hung AG charges the full 120s to every article even after
Codex finishes → 5×120s ate the whole 600s budget (only ~3 articles/night). Added a circuit breaker in
`vault_critic.py run()`: after N consecutive AG failures, stop spawning AG (`antigravity_enabled=False`)
and go Codex-only. Config `[agents.vault_critic].antigravity_circuit_threshold` = **1** (aggressive,
while AG is dead); `--ag-circuit-threshold` overrides; 0 disables. Manifest gains `antigravity_skipped`.
A successful AG resets the counter (transient failure won't trip it). 5 new tests; full suite 829 pass.
VERIFY on the next nightly: manifest `antigravity_calls`≈1, `antigravity_skipped`≈N-1, more
`articles_critiqued`, `duration_seconds` well under 600. Raise threshold to 2 once AG is healthy.

---

## Session 5 — 2026-06-04 results (both fixes verified)

**Circuit breaker: WORKS.** `critic-manifest-2026-06-04.json`: antigravity_calls=1, antigravity_skipped=7,
codex_calls=8, articles_critiqued=3 + backfill 5 = **8 total** (was 5 on 6/03), codex_tokens=260K
(was 145K), duration=**323s** (was 610s). Warning: "antigravity circuit-breaker tripped after 1
consecutive failures". Throughput up ~60%, wall budget no longer starved.

**Network-reachability root cause: REFUTED by the 6/04 probe.** Only one ag-timeout capture (breaker
trips after the first failure → run-once probe fired on it). The `CONNECTIVITY PROBE` section, captured
AT the 120s-timeout moment, shows the network was FULLY UP during the hang:
  curl4 cloudcode-pa.googleapis.com: http=404 connect=0.023s
  curl6 cloudcode-pa.googleapis.com: http=404 connect=0.026s
  curl4 play.googleapis.com:         http=404 connect=0.016s
  curl6 play.googleapis.com:         http=404 connect=0.014s
  curl4 api.openai.com (control):    http=421 connect=0.066s
Both Google hosts reachable on BOTH families in ~15-26ms while gemini's model request hung to 120s / 0
tokens. This run's Clearcut flush even got an HTTP 400 (connected) rather than a connect-timeout. So the
6/03 play.googleapis.com `UND_ERR_CONNECT_TIMEOUT` was an intermittent telemetry-endpoint red herring,
NOT a signal about the model host.

**Where that leaves it:** eliminated = MCP, OAuth-refresh, machine-asleep, raw network reachability,
and swallowed-429 (no quota strings). What remains is the authenticated Code Assist *streaming* call
silently hanging (server-side throttle-as-hang on the preview model, or a gemini-cli stream bug) —
caveat: curl-reachable ≠ authed-call-works, and the CLI swallows the real error, so more --debug
captures won't reveal more. **Decision: stop chasing the gemini hang.** The breaker contains it at $0
cost and the **June-18 oauth-personal EOL** obsoletes the entire path. Next action is the migration
decision (drop AG / GEMINI_API_KEY / Antigravity CLI), not more debugging.

**Cleanup pending:** `VAULT_CRITIC_AG_DEBUG=1` can now be removed from the plist (the probe has given
its verdict) — but it's harmless (1 capture + ~10s probe per night) and confirms the breaker each
night, so leaving it until the migration is also fine. The run-once probe is gated behind it.
