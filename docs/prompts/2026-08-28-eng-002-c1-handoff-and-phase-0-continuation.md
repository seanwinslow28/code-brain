# eng-002 continuation — hand C1 to Codex, resume Phase 0

*Written 2026-08-28 for a fresh session. Paste the whole thing.*

---

Invoke `/systemcraft`. This continues **eng-002-fleet-to-workforce-redesign**.

Read `systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/RESUME.md` first — it was reconciled on 2026-08-28 and its top carries a correction note. Then `systemcraft/ledger/index.md` and the entries you need. **d144, d145, d146 are the newest and describe exactly where the last session stopped.**

## Where it stands

**Gate 2 (pre-launch) round 6 = FAIL — 1 CRITICAL (RT-G2R6-C1) / 0 MATERIAL / 1 NOTE.** RESUME.md previously said PASS; that was written at 18:50 while the findings landed at 19:48. Corrected in place. **146 ledger entries, 25 artifact files (6 design artifacts + 11 red-team findings + the proofs and fixtures), 6 runnable proofs, nothing committed, private layer intact.**

**My posture, still binding:** the gate blocks the 1A launch, not the build. Phase 0 and the C1 repair run **in parallel**, never in sequence. No further gate rounds until both are done; the re-gate comes after and is scoped to what changed.

## 1 — Launch the C1 repair on Codex. This is the first thing you do.

The brief is written and waiting at:

```
systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/briefs/c1-repair-brief.md
```

Read it, then launch it. **This exact invocation is verified working as of 2026-08-28** — a `Bash(codex exec:*)` rule was added to `~/.claude/settings.json` and a `CODEX_OK` smoke test passed:

```
codex exec --model gpt-5.6-sol -c model_reasoning_effort=high --full-auto "$(cat systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/briefs/c1-repair-brief.md)" < /dev/null
```

Run it with the Bash tool's `run_in_background: true`. Four things that will cost you an hour if you get them wrong:

- **`< /dev/null` is mandatory.** Without it Codex blocks on stdin and hangs silently while looking busy. This has already cost ~50 minutes once.
- **Do not use `nohup … &`.** A `Bash(codex exec:*)` allow rule is a *prefix* match, so `nohup codex exec` does not match it and gets refused. Use the tool's background flag instead.
- **Do not use `--dangerously-bypass-approvals-and-sandbox`.** It is what tripped the auto-mode classifier in the first place, and the seat writes only inside this repo, so `--full-auto` is sufficient. If it genuinely cannot write something, tell me — do not reach for the bypass flag.
- **Never run two instances of one seat concurrently.** They share the ledger index.

While it runs, work Phase 0 below. Do not idle waiting on it.

### What the C1 defect is, in one breath

The manual 1A bridge has no single lawful population. My producer content-scores eight rows; Claude then verifies locations and six pass. Three current artifacts support three values of `n` — 6 (PASS), 8 (DELIVERY-FAIL), 0 (INCONCLUSIVE) — from the same event history. `v5-projection-replay.py` cannot decide it because `project()` receives `n_items` from its caller.

**On the record: I caused this.** My d131 ratification removed ADR-11 from 1A, so the frozen rule's "qualifying" lost its referent in the phase that runs first. It is not a seat's error and the brief says so. The brief also names the two options, requires one to be picked and the loser recorded, and requires the eight-row trace replayed green.

## 2 — Phase 0. Already started. Keep going.

**Written, tested, and UNCOMMITTED in the working tree.** Do not commit them without draft-then-ratify, and do not lose them:

```
 M agents-sdk/agents/daily_driver.py        # assert_daily_note + wired into run()
 M agents-sdk/agents/meta_agent.py          # d21 "ok" token; d40 collect_fleet_alerts/deliver_fleet_alert
 M agents-sdk/config.toml                   # [agents.vault_critic] schedule_enabled = false
 M agents-sdk/schedules/install_schedules.sh # INSTALL_VAULT_CRITIC + skip_disabled() convergent removal
?? agents-sdk/tests/test_phase0_p0_fixes.py # 17 tests
```

Verify with `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q`. Expect **978 passed, 4 failed**. The four (`test_doc_to_audio_cli::test_main_json_mode_emits_parseable_json`, three `test_job_db` CLI cases) **pre-date this work** — confirmed by stashing and re-running. Do not "fix" them as part of Phase 0; if they bother you, raise them as a separate ticket.

**The critical path is B8 → deploy → B3's seven-night clock.** B8 is the long pole; B3 is a seven-day tail that cannot start before the fixes land on the Mini. Everything else runs alongside.

**d05 index truncation stays deferred.** Its reasoning is unchanged. Do not re-open it.

## 3 — Three rulings I owe you. Ask for them at the right moment, one at a time, with a recommendation.

**a. The Mini `.gitignore` fix — ask first, it has a live residual.** On 2026-08-28 six of my personal daily notes were found publicly readable on `origin/vault/process-inbox-2026-07-14`; I ruled delete and the branch is gone (`origin/main` and the research branch verified clean). But the Mini's `.gitignore` still lacks the `vault/daily/` rule and Obsidian-Git has `disablePush: false`. It will **not** re-push on a timer (`autoSaveInterval` and `autoPushInterval` are both 0), but **the next manual sync on the Mini recreates the branch with the same six notes.** The fix is one `.gitignore` line plus `git rm --cached vault/daily/`. Full record: eng-002.d146.

**b. Push local `main` to `origin` — 204 commits.** B8's ADR-03 aims its reconciliation at `origin/main`, which is 204 commits behind local `main` (`3343c05` vs `ff2df36`). Reconciling the Mini onto it would move production backwards onto a stale trunk. Good news that shrinks B8: of the 11 apparently divergent code files, **nine are byte-identical** to local main; only `.gitignore` and a *comment-only* difference in `vault_indexer.py` actually differ. Full record: eng-002.d145.

**c. B11 Tailscale.** My install, Mini + iPhone, ~10–20 min, confirmed absent. Off the critical path. Nudge me.

**Nothing touches the Mac Mini without my explicit approval, per change.** Read-only `ssh -o BatchMode=yes` probing is fine and is how the above was established.

## 4 — One question already on the table, unanswered

Last session recommended **keeping the 1A verdict rule rather than running 1A observationally**, with the loser on record. The argument: four of the five population forks were the rule hardening against real attacks and converging; the fifth (C1) has a single nameable exogenous cause in my own d131. And decisively — 1A already retains every event, so the observational reading is available after the fact anyway; going observational would subtract the pre-commitment and add nothing. Named trigger to revisit: **if the C1 repair itself forks, bring it back unprompted.**

I have not ruled. Do not re-litigate it unprompted, but if the Codex pass comes back with a seventh definitional problem, raise it immediately.

## Binding constraints

- **Model routing:** heavy delegated work goes to **Codex `gpt-5.6-sol` at High**. **Do not escalate a seat to Fable without naming the trigger and asking me first** — the ladder's per-invocation rule has no aggregate budget and it exhausted my quota mid-engagement.
- **Verify, don't assert.** Run all six proofs and report actual output. Last verified green 2026-08-28: `v3-enumeration.py` (5,400 cells / 0 ambiguous / 399 / 236) · `v5-projection-replay.py` (**22**) · `g2c1-gate-replay.py` (24) · `tco-line-sum.py` (8) · `check-version-drift.py` (**exit 0**, 0 FAIL / 135 REVIEW, `--selftest` **23**) · `geo-label-replay.py` (35). Leave no `__pycache__`.
- **Nothing committed** without draft-then-ratify; push is my call. `git status --porcelain systemcraft/` must be empty at every stop. Private layer never reaches git.
- **Every live count carries its exact SQL, database path and capture instant** — that standard exists because the coordinator broke it twice, both times a loose query reported as a precise one. Corrected forms only: **105** roll-ups (not 107) · **54** strong fits / 16 at score 5 / 503 scored / 16,460 total (53 = the dated 2026-08-24 baseline) · exact `Remote, US` = **60** · exact `100% Remote (US)` = **2** · the 443 "US-remote-pattern" figure is **withdrawn** · the notification era = **31 role IDs in ~20 API-accepted batched messages, receipt and attention unmeasured**.
- **Ratified, do not reopen:** the disposed-decision unit of value · the job-hunt beachhead · two-week clean-room 1A · the frozen risk dial (never apply, email or contact anyone) · rule v5 · the nine claims · the sourcing sentinel · the no-quota principle · the eight April-2026-disabled agents · d02 · **d131** · my four Gate-1 acceptances · Tailscale/B11 · escalation one push that week and none during 1A · **3 interrupts/day** · **2 applications/week, calibration only, never a target** · geo **remote (preferred) or Boston, MA**.
- I'm a PM, not a dev — plain language, one question at a time, a recommendation with every question.

## What done looks like

C1 closed by one bounded Codex pass with the eight-row replay green, and the result explained to me in plain language. Phase 0 advanced as far as my rulings allow. Ledger accreting; RESUME.md reconciled again at the stop. Then, and only then, scope the re-gate to what changed.

## One live thing, unrelated to the design

Two genuinely eligible score-5 roles are sitting untriaged and neither is one I flagged: **id 4445 Liberate — AI Product Manager — Boston, MA** and **id 4441 Liberate — Agent Product Manager — Boston, MA**, both `status = new` since 2026-05-16. Probably closed by now, which is the point. Six eligible score-4s too (Sourcegraph IC4 Remote; three Klaviyo Boston; Webflow U.S. Remote; Mercury Remote US). Caveat: 46 of the 55 untriaged strong fits have blank location — that is CF-01, not a geo failure, and "eligible" here means eligible *on the stored string*, the field B16 exists because we cannot trust. Don't act on these; just don't let them rot silently.
