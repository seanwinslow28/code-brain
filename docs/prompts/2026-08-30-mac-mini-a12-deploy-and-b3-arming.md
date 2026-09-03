# Mac Mini — deploy A12, arm the claim-6 drill, start B3 on Sep 1

**Hand this to Claude Code running on `seans-mac-mini.local`.** Everything below the horizontal rule is the prompt.

> **One prerequisite before you paste this:** `origin/main` must already carry the A12 build (`7aba08e0`) and the status-vocabulary fix (`3a54ed21`). If Sean has not pushed from the MacBook Pro yet, this deploy has nothing to pull.

---

You are running on Sean's **Mac Mini** — this is *production*. The fleet runs here. Read the whole brief before touching anything.

## What this deploy is for

B3 is a seven-night certification that the fleet's pager actually works. Its window is **2026-09-01 → 2026-09-07** (Sean's ruling, eng-002.d159), with a synthetic "drill" alert on **Wednesday 2026-09-02** — the window's second night. Tonight's job is to get the machinery in place before Sep 1.

Nothing here fires today. You are installing a schedule, not testing it.

## Where things stand, verified from the MacBook Pro on 2026-08-30

- The Mini is on **`main`**, clean, 0 ahead / 0 behind. B8 is closed.
- Two commits are waiting on `origin/main`: **`7aba08e0`** (the A12 drill runner, ~1,600 lines) and **`3a54ed21`** (the status-vocabulary fix).
- The drill ships **disarmed**: `schedule_enabled = false`, `day_of_month = 0`, and two empty strings. It cannot fire until you register it.
- `com.sean.agent.vault-critic` is **still loaded and firing at 03:30 daily**, even though its disable was ratified (eng-002.d15/d49) and shipped in code. The convergent removal only happens when the installer runs — which is step 3. Expect it to disappear, and treat that as the fix landing, not a fault.

## Step 1 — Pull and verify, before changing anything

```
cd ~/Code-Brain/code-brain
git status --porcelain | head           # note anything dirty BEFORE you pull
git fetch origin && git log --oneline HEAD..origin/main
git merge --ff-only origin/main
git log --oneline -3
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q
```

Expect `7aba08e0` and `3a54ed21` in the log, and **1043 passed** here (the Mini has no pre-existing failures; the MacBook's four are environmental). If the merge is not a clean fast-forward, **stop and report** — do not force it.

Then confirm the status fix is live, since it is what makes a clean seven-night streak possible:

```
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
from agents import meta_agent as m
print('deferred ->', m.STATUS_VOCABULARY['deferred'])
print('budget   ->', m.STATUS_VOCABULARY['error_max_budget_usd'])"
```

`deferred` must print `healthy`. That token is the synthesizer's *designed* off-LAN deferral; it was paging as a failure roughly one night in seven and would have reset B3's streak.

## Step 2 — Register the three values (Sean decides these; you edit and verify)

Edit `[agents.claim6_drill]` in `agents-sdk/config.toml`:

| Key | Value | Why |
|---|---|---|
| `day_of_month` | **`2`** | Puts the drill on Wed Sep 2, the window's second night — night 1 proves the quiet path, night 2 the send path, so a failure costs two nights instead of seven. Also ≤ 28, so the monthly cadence never silently skips February. |
| `launchd_label` | **`com.sean.agent.claim6-drill`** | Must match the installed plist filename minus `.plist`, or `launchctl` and the runner's own provenance guard will disagree. |
| `acknowledged_device` | **Sean's Pushover device name** | The only device whose acknowledgment can qualify the drill. |

Then set `schedule_enabled = true`. All three must be real before the installer will render anything.

**The device name needs a decision from Sean, and you should raise it rather than choose for him.** `agents-sdk/config.toml` is a **tracked file in a public repo**, and this value is read only from config — there is no env or Keychain path for it. Its own runbook says not to commit a real value.

The cheap fix: ask Sean to open Pushover and **rename the device to something non-identifying** — `fleet-pager` rather than anything naming him or his hardware. Then committing it reveals nothing and the code stays simple. He finds the current name in the Pushover app under its device settings, or at pushover.net → Your Devices. **It must match exactly**, including case.

Verify before moving on — this fails closed, which is the point:

```
cd ~/Code-Brain/code-brain/agents-sdk
grep -A 12 "\[agents.claim6_drill\]" config.toml
PYTHONPATH=. .venv/bin/python3 schedules/render_claim6_plist.py --config config.toml --check-enabled && echo "REGISTERED — installer will arm it" || echo "NOT ARMED — a value is still missing"
```

## Step 3 — Run the installer

```
cd ~/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh
```

Two things happen, and Sean has approved both:

1. The drill plist is rendered from the template and loaded — monthly, `Day=2 / Hour=8 / Minute=15`.
2. **The vault-critic schedule is removed.** ADR-04's convergent removal unloads the label and deletes the plist rather than merely skipping it. This is eng-002.d15's ratified Phase-0 disable finally being applied. **The critic's manual mode is untouched** — `--target` / `--from-list` / `--force` all still work.

Read the installer's output and report it. Then check nothing else was disturbed, because this run reloads every label:

```
launchctl list | grep -E "com.sean" | sort
```

Expect the drill label **present**, `com.sean.agent.vault-critic` **absent**, and the other eight (`vault-indexer`, `vault-synthesizer`, `deep-researcher`, `daily-morning`, `job-feed`, `knowledge-lint`, `meta-agent`, `agent-fleet-dashboard`) still loaded. **If any of those eight vanished, say so immediately** — that is a regression, not a success.

## Step 4 — Verify the schedule is real

```
plutil -p ~/Library/LaunchAgents/com.sean.agent.claim6-drill.plist
```

Confirm and report each: `Label` matches the registered `launchd_label` · `StartCalendarInterval` is `Day=2, Hour=8, Minute=15` · `EnvironmentVariables` carries the full `PATH` (`/Users/seanwinslow/.local/bin:/opt/homebrew/bin:...` — without it the agent dies with `CLIConnectionError`, per `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`) · `PYTHONPATH` is present · `CLAIM6_LAUNCHD_LABEL` matches the label.

```
launchctl list com.sean.agent.claim6-drill | head -5
```

## Hard constraints — violating any of these fails the pass

- **Do not fire the drill, and do not send any test push.** The runner has no manual send mode by design: it refuses unless its parent is launchd, the label matches, and the clock is on the exact registered minute. **Do not try to work around that.** The whole point of B3 is that the first real fire is a scheduled one — a hand-run send is precisely the evidence eng-002.d151 ruled insufficient.
- **Do not edit code on this host.** `agents-sdk/`, `.claude/` and `scripts/` are deploy targets; a hand-edit here is overwritten by the next deploy and is the drift ADR-03's tripwire exists to catch. Config registration in step 2 is the one intended exception. Anything else goes to the MacBook Pro and arrives by deploy.
- **Do not push, merge, rebase, or reset.** If step 2's config edit should be committed, ask Sean first — and note the value is going to a public repo.
- **Do not touch `vault/daily/`, `systemcraft/`, or any PRIVATE LAYER path** (CLAUDE.md rule 9).
- **Do not re-enable the critic schedule** or any of the eight agents disabled in April 2026.
- **Verify, do not assert.** Paste real command output for every claim.

## What happens next, so you can tell Sean what to expect

- **Every morning Sep 1–7**, the 08:45 meta-agent writes one row to `vault/health/fleet-alert-delivery.jsonl`. A quiet night reads `attempted: false, delivered: false, probe: "ok"`. That is a **green** night.
- **Wed Sep 2 at 08:15**, the drill fires: Sean's phone gets an **emergency-priority** alert that repeats every 5 minutes until he acknowledges it, expiring after 15 — **at most three buzzes, and it stops the moment he taps it.** He must acknowledge it on the registered device; nothing else counts.
- **At 08:45 that day**, the meta-agent reconciles the drill and writes a typed block into the fleet report *before* its own Pushover step — so a drill that never fired surfaces without using the channel being tested.
- **B3 closes Sep 7** if all seven nights are green and the drill was acknowledged.

## Report back

1. Step 1: the merge result and the test count; confirm `deferred` prints `healthy`.
2. The three registered values (say what the device name is set to, and whether Sean renamed it).
3. The installer's output, and the full `launchctl list | grep com.sean` — explicitly confirming the critic is gone and the other eight survived.
4. The rendered plist's Label, `StartCalendarInterval`, `PATH` and `CLAIM6_LAUNCHD_LABEL`.
5. Whether `config.toml` is now a dirty tracked file, and what you recommend doing about that before the Mini's auto-commit sweeps it.
6. Anything you found and did **not** fix, named explicitly.

Finally, per CLAUDE.md rule 8, append a one-line `- ` bullet under `## Todo` in `vault/00_inbox/tickets.md` for anything left open, and update the existing B3 ticket in place with the armed state rather than duplicating it.
