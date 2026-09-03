# Mac Mini setup — Phase 0 verification, Pushover repair, B11 Tailscale

**Hand this to Claude Code running on `seans-mac-mini.local`.** Everything below the line is the prompt.

---

You are running on Sean's **Mac Mini** — this is *production*. The fleet runs here. Read this whole brief before you touch anything.

## Where things stand, verified from the MacBook Pro on 2026-08-28

- Repo: `~/Code-Brain/code-brain`, branch **`vault/process-inbox-2026-07-14`**, HEAD **`ad77bc5`**.
- A code-only deploy landed today (eng-002 B8 step 1). `agents-sdk/`, `.claude/` and `scripts/` are byte-identical to `origin/main` (`ce9992e`). **Vault data was deliberately not touched** and reconciles later as B8 step 2.
- Rollback points, both already in place: branch **`mini-pre-b8-archive-2026-08-28`** (`bcc9cea`) and **`~/Code-Brain/backups/job-feed-pre-b8-2026-08-28.db`** (integrity ok, 16,773 rows, deliberately outside the repo).
- The full test suite passed here after the deploy: **982 passed, 0 failed**.
- `google-genai` was synced 1.74.0 → 2.20.0.
- The Mini's HEAD is **knowingly off `main`** until B8 step 2. That is expected. Do not "fix" it.

## The defect you are here to close

The fleet's alerting has **never worked on this machine.** `vault/90_system/agent-logs/vault-synthesizer-stderr.log` carries **369** launchd-context failures reading `Missing Pushover credentials in Keychain (pushover_user_key / pushover_app_token)`, most recently **2026-08-28 03:14**, and there is **not one successful Pushover send in any log on this machine, ever**. The credentials exist on Sean's MacBook Pro and are absent here.

This matters because a reliability fix that shipped today (eng-001.d40) pages a human when the fleet is unhealthy — and its transport is dead. A seven-night certification clock (B3) is blocked until a real send is proven from this machine.

## Task 1 — Confirm the deploy, read-only

Run and report actual output; do not assert:

```
cd ~/Code-Brain/code-brain
git rev-parse --short HEAD && git rev-parse --abbrev-ref HEAD
git status --porcelain -- agents-sdk .claude scripts    # must be empty
git fetch origin && git diff --stat origin/main -- agents-sdk .claude scripts   # must be empty
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q
```

Expect: HEAD `ad77bc5`, zero dirty code paths, no diff against `origin/main` in those paths, **982 passed**. If any of that disagrees, **stop and report** — do not repair it yourself.

## Task 2 — Place the Pushover credentials (Sean does this part; you verify)

**You must not handle the secret values.** Do not read them, print them, echo them, put them in a file, or paste them into a command yourself. Your job is to prepare, verify, and prove.

Tell Sean to run these two commands **himself, in his own terminal on this Mac Mini**. The `-w` with no value makes `security` prompt for the secret without echoing it and without writing it into shell history:

```
security add-generic-password -U -s "com.sean.agents.pushover_user_key"  -a "pushover_user_key"  -w
security add-generic-password -U -s "com.sean.agents.pushover_app_token" -a "pushover_app_token" -w
```

The service prefix `com.sean.agents.` is **not optional** — `agents-sdk/lib/keychain.py` looks up `com.sean.agents.<name>` with account `<name>`, and a differently-named entry will read as absent. On the MacBook Pro the values are 30 characters each.

Then verify, **without printing the values**:

```
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
from lib.keychain import get_credential
from lib.pushover import ensure_credentials_or_raise
for k in ('pushover_user_key','pushover_app_token'):
    v = get_credential(k); print(k, '->', ('RESOLVED len='+str(len(v))) if v else 'MISSING')
ensure_credentials_or_raise(); print('credentials present; nothing sent')
"
```

## Task 3 — Prove the transport actually sends

Credentials resolving is not proof of delivery — that confusion is the whole defect. **Ask Sean's permission first** (his phone will buzz), then send exactly one test push and have him confirm he received it:

```
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
from lib.pushover import send_push
print(send_push(title='Mini pager test', message='eng-002 B3 transport check — 2026-08-28', priority=0))
"
```

**Ask him out loud whether the notification arrived on his phone.** A clean exit code is not receipt. If it did not arrive, report that — do not retry in a loop.

Then run the meta-agent for real (not `--dry-run`; it is local and $0) and confirm the delivery record now exists:

```
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/meta_agent.py
cat ~/Code-Brain/code-brain/vault/health/fleet-alert-delivery.jsonl
```

Report the JSONL rows verbatim.

**Known limitation — do not paper over it, and do not fix it here.** On a night with nothing to send, `deliver_fleet_alert()` writes `delivered: true` *without attempting a send*. So a healthy-fleet row proves the decision path ran, not that the transport works. That repair belongs on the MacBook Pro and arrives by deploy. **Say so in your report rather than editing the code.**

## Task 4 — B11, install Tailscale on the Mini

Confirmed absent here today: no `tailscale` CLI, no `/Applications/Tailscale.app`. Homebrew 6.0.17 is present; macOS 26.6.2, arm64.

Install the GUI app (not the CLI-only formula — the Mini needs to stay logged in and reachable):

```
brew install --cask tailscale-app
```

This ships a `.pkg`, so **it will ask Sean for his admin password** — that prompt is his to answer, not yours. Version at time of writing: 1.102.3.

Then have Sean open Tailscale from `/Applications`, sign in, and **use the same identity he will use on the iPhone** — the two devices must land on the same tailnet or nothing connects. Ask him which identity he picked and write it down in your report.

Afterwards, verify and report actual output:

```
/Applications/Tailscale.app/Contents/MacOS/Tailscale status
/Applications/Tailscale.app/Contents/MacOS/Tailscale ip -4
```

Record the Mini's tailnet IP (100.x.y.z) and its MagicDNS name.

**Scope B11 honestly.** Its acceptance criterion is *"Tailscale installed on the Mini and the iPhone; verified by one off-LAN packet open + answer round-trip on a test packet."* **The answer page does not exist yet** — it is ADR-02, unbuilt. So today closes only the first half: both devices installed, on one tailnet, Mini reachable from the phone off-LAN. **Report B11 as half-closed, never as done.** Also note for the record: when the answer page is built it binds to the tailnet interface only, never a public port.

## Task 5 — Prove the off-LAN path end to end (do this once, then tear it down)

"Both apps are installed" is not reachability. Prove it with a throwaway page served on the **tailnet interface only** — the same binding the real answer page will use, so this rehearses the actual topology rather than a proxy for it.

After Sean's iPhone is installed and signed in, substitute the Mini's tailnet IP for `<TAILNET_IP>` and run this in a terminal you can interrupt:

```
cd /tmp && printf 'B11 off-LAN reachability check — 2026-08-28\n' > index.html
python3 -m http.server 8899 --bind <TAILNET_IP>
```

Binding to `<TAILNET_IP>` and **not** `0.0.0.0` is the point: it is unreachable from the LAN or the internet, and reachable only over the tailnet.

Then ask Sean to, **on his iPhone with Wi-Fi turned OFF and cellular on** — that is what makes it an off-LAN test rather than a same-network test — open Safari to `http://<TAILNET_IP>:8899`.

He should see the one line of text. Have him tell you whether it loaded. Then **stop the server with Ctrl-C and delete `/tmp/index.html`** — leaving it running is an open port with no reason to exist.

Record the result plainly: off-LAN reachability **verified** or **not verified**. If it fails, the usual causes are the two devices being on different tailnets (different sign-in identity) or the iPhone's Tailscale toggle being off — check both before concluding anything about the network.

## Hard constraints — violating any of these fails the pass

- **Never hand-edit code on this host.** `agents-sdk/`, `.claude/` and `scripts/` are deploy targets; a fix here would be silently overwritten by the next deploy and is exactly the drift ADR-03's tripwire exists to catch. Code changes go to the MacBook Pro and arrive by deploy.
- **Never handle the credential values.** Sean types them; you verify by length and resolution only.
- **Do not push to `origin`, and do not merge, rebase, or reset anything.** Push is Sean's call. If a commit is genuinely needed, ask first.
- **Do not touch `vault/knowledge/`, `vault/daily/`, or anything under the PRIVATE LAYER block** in `.gitignore`.
- **Do not delete `mini-pre-b8-archive-2026-08-28` or the DB backup.**
- **Do not start B3's seven-night clock** or mark B3 satisfied. That is a separate ruling once the transport is proven and the quiet-night record is fixed.
- **Verify, do not assert.** Paste real command output for every claim.

## Report back

1. Task 1 result — did the deploy verify clean, with the actual numbers.
2. Whether the credentials now resolve, and **whether Sean confirmed the test push physically arrived on his phone**.
3. The `fleet-alert-delivery.jsonl` rows, verbatim.
4. Tailscale: installed version, the identity Sean signed in with, the Mini's tailnet IP and MagicDNS name.
5. Off-LAN reachability: verified or not verified, and that the throwaway server was torn down.
6. Anything you found and did **not** fix, named explicitly.

## Append to the ticket file when you finish

Per CLAUDE.md rule 8, append one `- ` bullet per unfinished item under `## Todo` in `vault/00_inbox/tickets.md`, and update these two existing tickets in place rather than duplicating them:

- the **"CRITICAL — the fleet's pager has never worked"** ticket — mark it closed if and only if Sean confirmed the test push physically arrived; otherwise record exactly how far it got.
- the **B11** line — record the half that closed and the half that waits on the answer page.

Do not commit `vault/` here. Sean's MacBook Pro owns vault commits; the Mini's auto-commit will sweep it.
