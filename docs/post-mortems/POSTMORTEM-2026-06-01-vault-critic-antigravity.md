# Post-Mortem — vault_critic Anti-Gravity CLI silent 100% nightly failure

| | |
|---|---|
| **Date authored** | 2026-06-01 |
| **Author** | Sean (with Claude Code) |
| **Component** | `vault_critic` nightly agent → Anti-Gravity (gemini) CLI path |
| **Severity** | Medium — one of two critique engines fully dark for ~6 nights; no data loss, degraded knowledge-loop quality |
| **Detection** | Manual (Sean noticed `ag_fail` in the daily digest); **not** caught by the meta-agent |
| **Status** | Fixed 2026-06-01; nightly verification scheduled for 2026-06-02 09:00 ET (routine `trig_01W3WBjQ5fDe19n1RURpqvA2`) |
| **Reproduced in lab?** | **No** — failure is bound to the unattended ~03:30 condition; every daytime reproduction attempt succeeded. See [Honest caveats](#honest-caveats). |

---

## 1. Summary (TL;DR)

The `vault_critic` agent runs nightly at 03:30 and critiques synthesizer concept articles by shelling out to **two CLIs in parallel** — Codex CLI (gpt-5.5) and the "Anti-Gravity" CLI (the Google `gemini` CLI on personal OAuth, routing to Gemini 3.1 Pro). From **2026-05-26 through 2026-06-01**, the Anti-Gravity half failed on **100% of nightly calls** (`antigravity_calls: 5, antigravity_failures: 5, antigravity_tokens_total: 0`) while Codex succeeded every night. Half of every nightly critique was silently missing the Gemini perspective.

Root cause: the `gemini` CLI loads **6 MCP servers on every invocation** (per `~/.gemini/settings.json`). That startup is fine interactively (~12–18s) but hangs past the agent's **120s per-CLI timeout** on the unattended 3:30am run — the CLI was killed during *startup*, before it ever reached the model (zero gemini session files were created on any nightly run). Codex, with a lightweight single-process startup, was unaffected.

Fixed by telling the critic's gemini call to load **zero** MCP servers (`--allowed-mcp-server-names __none__`) — it only needs a text critique, never a tool — and by closing the diagnostic gap that hid the failure for a week (the manifest now persists the actual per-CLI error text, not just a failure count).

---

## 2. Impact

- **Knowledge-loop degradation:** Every nightly critic expansion written between 5/26 and 6/1 contains only the Codex perspective; the Anti-Gravity ("From Anti-Gravity (Gemini 3)") section fell back to the placeholder `_Anti-Gravity rate-capped or failed; no critique this run._`. The dual-vendor cross-critique design — the whole reason for running two CLIs — was operating at 50%.
- **No data loss, no cost:** Both CLIs are subscription-absorbed ($0 incremental). The run exited cleanly as `status: partial` every night and wrote its expansions. Nothing crashed.
- **Wasted wall-clock:** Each failing AG call still consumed time before timing out, contributing to the 600s wall budget exhausting "after 5 articles" every night.
- **Silent:** The meta-agent reported "all active agents healthy" throughout, because `partial` is a tolerated status (it's the normal both-CLIs-rate-capped exit). A 100%-dead sub-CLI never tripped an alert.

---

## 3. Timeline (UTC dates; runs are ~03:30 America/New_York)

| Date | Event |
|---|---|
| 2026-05-23 | Last healthy nightly AG run — 3 calls, 0 failures, 50,454 tokens. |
| 2026-05-24 | Daytime manual runs healthy (up to 109K tokens). |
| 2026-05-26 | **First full nightly AG failure** — 2/2 calls fail, 0 tokens. |
| 2026-05-27 | Daytime manual run *partially* works — 9 calls, 4 failures, 167K tokens (5 succeeded). First sign the failure is conditional, not absolute. |
| 2026-05-28 → 06-01 | Every nightly run: **AG 5/5 fail, 0 tokens.** Codex clean (0 fail, ~120–160K tokens) each night. |
| 2026-05-31 | Failure pattern flagged in the daily digest (`ag_fail=5`); noted for follow-up. |
| 2026-06-01 ~10:30 | Investigation + fix (this document). |
| 2026-06-02 09:00 ET | Scheduled remote verification of the first post-fix nightly run. |

---

## 4. Investigation — how we got to root cause

The discipline that mattered here: **do not fix before the root cause is found**, and **gather evidence at each component boundary** rather than guessing. The failure looked like it could be a dozen things (auth, network, quota, the binary, the prompt). We eliminated them one boundary at a time.

### 4.1 Read the symptom precisely
The nightly manifests showed a clean, repeating signature: `antigravity_calls: 5, antigravity_failures: 5, antigravity_tokens_total: 0`, `status: partial`, `duration_seconds: ~600`. Codex in the **same manifest** showed `codex_failures: 0` and ~140K tokens. So whatever broke was specific to the gemini path, not the agent, the machine, or the network as a whole.

### 4.2 Establish the CLI is not broken
Running the *exact* command the agent runs (`gemini -p … --output-format json --approval-mode plan`) from an interactive shell **succeeded** — exit 0, valid JSON, 13.8K tokens. The binary, OAuth credentials, and model access were all healthy.

### 4.3 Eliminate candidate causes one at a time
Every reproducible condition we could think of **passed**, ruling it out:

| Hypothesis | Test | Result |
|---|---|---|
| Prompt too large | 24,924-token prompt | ✅ 18s, succeeded |
| Minimal/stripped environment | `env -i` with only the plist's PATH + HOME | ✅ 14s, succeeded |
| The launchd execution context itself | Threw away a real launchd job (`launchctl bootstrap`/`kickstart`) running the exact command, daytime | ✅ exit 0, 12.6K tokens |
| Rapid-fire rate limiting | 5 back-to-back calls | ✅ 5/5 succeeded |
| Auth/OAuth expiry | Inspected `oauth_creds.json` (refresh token present, auto-refresh) | Not a hard blocker |

### 4.4 The smoking gun — failure is in *startup*, before the model
The gemini CLI writes a session file per invocation under `~/.gemini/tmp/<project>/chats/`. We listed every session file: **all of them are daytime; there are zero session files for any nightly run.** That is the decisive evidence — at 03:30 the CLI dies during startup, before it ever creates a session or contacts the model. And since Codex (same Python process, same 03:30, same network) succeeds, it is **not** a network outage — it is gemini-CLI-specific startup.

### 4.5 Identify the heavy, fragile part of startup
`~/.gemini/settings.json` registers **6 MCP servers** that the CLI spins up on every invocation: `nanobanana` (node), `zapier` (remote HTTP via `mcp-remote`), `notebooklm-mcp`, `mcp-atlassian` (`uvx`), `chrome-devtools` (`npx chrome-devtools-mcp@latest --browser-url=http://127.0.0.1:9222`), and `pencil`. Several need things that don't exist at 3:30am — most notably `chrome-devtools` connecting to a Chrome instance on `:9222` that is only running during Sean's interactive daytime sessions, plus `npx`/`uvx`/remote subprocesses. This heavy startup is what hangs past the 120s timeout unattended, while it resolves in ~12–18s interactively (warm caches, Chrome up).

### 4.6 Confirm the fix path is real
We verified that `--allowed-mcp-server-names __none__` makes the CLI load **zero** MCP servers (0 "already registered" lines in stderr), still returns a valid critique, and runs in ~12s — and then verified it end-to-end through the agent's own `run_antigravity()` function: `ok=True, 12,096 tokens, 6.4s, error=None`.

---

## 5. Root cause

> The `vault_critic` Anti-Gravity path invokes the `gemini` CLI with its full user MCP configuration. The CLI eagerly initializes all 6 configured MCP servers at startup. Under the unattended 03:30 condition (Chrome closed, post-wake / resource-contended window, cold caches), that initialization blocks past the agent's 120s per-CLI timeout, so the CLI is killed before reaching the model — yielding 0 tokens and a counted failure on 100% of nightly calls. The lightweight Codex CLI shares none of that startup surface and is unaffected.

A **contributing cause** made this expensive to diagnose: the manifest recorded only failure *counts*, never the per-call error text — even though `CLIResponse.error` was being captured and then discarded. With no error surfaced, a 100%-failing CLI looked identical to the benign "rate-capped" case for six days.

---

## 6. Resolution

Two changes, both shipped 2026-06-01 (see `CHANGELOG.md` → Unreleased → Fixed):

1. **Fix — strip MCP startup from the critic's gemini call.**
   [`agents-sdk/lib/cli_runners.py`](lib/cli_runners.py), `run_antigravity()`: appended `--allowed-mcp-server-names __none__` to the command. The critic only ever needs the model to emit a text critique; it never calls a tool. Loading zero MCP servers makes gemini's startup as lightweight as Codex's.

2. **Instrumentation — make the next failure self-reporting.**
   [`agents-sdk/agents/vault_critic.py`](agents/vault_critic.py): added `codex_last_error` and `antigravity_last_error` to the `CritiqueResult` dataclass, captured them from `CLIResponse.error` in the failure path, and wrote them into the nightly manifest. If the fix ever regresses, the manifest will now name the reason instead of just counting.

**Verification status:** 47 critic/cli unit tests pass; `scripts/validate.py` passes; the fix is verified live through the real `run_antigravity()` code path in daytime. The *nightly* condition cannot be reproduced on demand, so the true confirmation is the first post-fix 03:30 run, checked by remote routine `trig_01W3WBjQ5fDe19n1RURpqvA2` at 2026-06-02 09:00 ET.

---

## 7. Honest caveats

- **We never reproduced the actual 3:30am failure.** Every daytime reproduction — including under a genuine launchd job — succeeded. The MCP-startup-hang explanation is the best-supported hypothesis given all evidence (zero nightly sessions = startup death; gemini-only; heavy MCP startup is the obvious fragile surface), but it is an inference, not a captured stack trace. The instrumentation exists precisely so that if the fix doesn't hold, tomorrow's manifest hands us the real error verbatim.
- **The fix is also robust even if the precise mechanism differs.** Whatever the exact startup hang was, removing 6 unnecessary MCP subprocess spin-ups can only make startup faster and more reliable, and it removes the single most plausible failure surface. It has no downside for this agent (no tool calls are ever made).

---

## 8. What we learned

1. **A "tolerated" status can hide a total failure.** `partial` was designed for the benign both-CLIs-rate-capped case, so the monitor treated a 100%-dead sub-CLI as healthy. Tolerated/degraded states need a floor: *some* degradation is normal, *complete* loss of a sub-component is not.
2. **Capture the error, not just the count.** The most expensive part of this incident was the six days of opacity, caused entirely by discarding `CLIResponse.error`. Counters tell you *that* something failed; they never tell you *why*. Persist the why.
3. **Reproduce at the boundary that actually differs.** The bug lived in the gap between "works interactively" and "fails unattended at 3:30am." Testing prompt size, env, and even the launchd context all passed because none of them was the real differentiator (time-of-day machine/Chrome state). Knowing *which* boundary you haven't crossed is as important as the tests that pass.
4. **Heterogeneous redundancy has heterogeneous failure modes.** Running Codex + Gemini for independent perspectives is good design — but the two CLIs fail for completely different reasons. The lightweight one survived a condition that killed the heavy one. Redundancy across vendors does not imply redundancy across *startup fragility*.
5. **A subprocess inherits the full user config.** Shelling to `gemini` pulled in Sean's entire interactive MCP loadout (Zapier, Atlassian, Chrome DevTools, …) — none of which a headless text-critique needs. Headless invocations should run with the *minimum* config, not the developer's interactive one.

---

## 9. How we should proceed

### Immediate (done / scheduled)
- [x] Apply the MCP-disable fix and error-persistence instrumentation (2026-06-01).
- [x] Schedule remote verification of the first post-fix nightly run (routine `trig_01W3WBjQ5fDe19n1RURpqvA2`, 2026-06-02 09:00 ET).
- [ ] **Read tomorrow's report.** If FIX CONFIRMED, close this out. If STILL FAILING, the manifest's `antigravity_last_error` is now the next clue — follow it.

### Short-term (tickets filed in `vault/00_inbox/tickets.md`)
- [ ] **Close the meta-agent monitoring blind spot.** Alert when any sub-CLI's `failures == calls` (100% failure) or `tokens_total == 0 with calls > 0`, *even when overall status is `partial`*, and surface the new `*_last_error` text in the alert. This is the highest-leverage follow-up — it would have caught this on night one.
- [ ] **Fix the job-feed ATS watchlist decay** (separate issue surfaced during the fleet sweep): 14 company pollers 404 every run + `web3career_token` missing from Keychain. Refresh/prune the endpoint list.

### Longer-term / principles to apply elsewhere
- **Audit other headless CLI shell-outs for inherited config bloat.** Any agent that shells to a tool with a rich user config (`gemini`, `codex`, future CLIs) should pass the minimal config explicitly. Prefer a dedicated, lean profile for headless invocations over the interactive default.
- **Make "error text in the manifest" the standard, not the exception.** The counters-only pattern likely exists in other agents' manifests. Where a manifest records `*_failures`, it should also record `*_last_error`. Cheap to add, decisive when something breaks.
- **Consider a per-CLI startup budget separate from the call budget.** A startup that consistently consumes the full 120s call timeout is a smell; a shorter, explicit startup deadline would fail fast and free wall-clock for the articles that can be critiqued.

---

## Appendix — key evidence

- Manifest signature (every night 5/28–6/1): `antigravity_calls: 5, antigravity_failures: 5, antigravity_tokens_total: 0`, `codex_failures: 0`, `status: partial`, `duration_seconds: ~600`.
- Last healthy nightly: `critic-manifest-2026-05-23.json` (AG tokens 50,454).
- Zero nightly gemini session files in `~/.gemini/tmp/<project>/chats/` (all existing sessions are 14:xx–21:xx UTC = daytime ET).
- MCP servers configured in `~/.gemini/settings.json`: nanobanana, zapier, notebooklm-mcp, mcp-atlassian, chrome-devtools, pencil.
- Live post-fix call through `run_antigravity()`: `ok=True exit=0 tokens=12096 rate_capped=False dur=6.4s error=None`.
- Code: [`lib/cli_runners.py`](lib/cli_runners.py) (`run_antigravity`), [`agents/vault_critic.py`](agents/vault_critic.py) (manifest fields + capture).
