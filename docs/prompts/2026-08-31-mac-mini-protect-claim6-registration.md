# Mac Mini — keep the claim-6 registration out of git, and make its loss loud

**Hand this to Claude Code running on `seans-mac-mini.local`.** Everything below the horizontal rule is the prompt.

---

You are running on Sean's **Mac Mini** — this is *production*, and a seven-night certification (B3) starts tomorrow, 2026-09-01, with a live drill on Wed 2026-09-02 at 08:15. **Nothing you do here may disturb that.** Read the whole brief first.

## The situation

`agents-sdk/config.toml` is a **tracked file in a public repo**. On this machine it carries the claim-6 drill's production registration:

```
schedule_enabled = true
day_of_month = 2
launchd_label = "com.sean.agent.claim6-drill"
acknowledged_device = "sean-phone"
```

It is deliberately **uncommitted**, and must stay that way. Two independent reasons:

1. `acknowledged_device` is Sean's personal device name; the repo is public (CLAUDE.md rule 9).
2. `agents-sdk/tests/test_claim6_schedule.py` reads the **committed** config via `git show HEAD:agents-sdk/config.toml` and asserts the drill ships disarmed. Committing the registration turns the suite red on `main`.

Right now nothing enforces this but memory. Your job is to make it structural, without breaking anything.

**A second, larger hazard, which you will also address.** Because the file must stay dirty, a future `git merge --ff-only` whose incoming commit touches `config.toml` will refuse, and whoever resolves that conflict may drop the four values. The drill would then **silently disarm mid-window** — the plist still loaded, firing a runner that declines to send. That failure is quiet, which is the whole class of defect this engagement exists to kill.

## Task 1 — Back the registration up, outside the repo

Before touching anything else, make the values recoverable:

```
mkdir -p ~/Code-Brain/backups
cd ~/Code-Brain/code-brain
sed -n '/^\[agents\.claim6_drill\]/,/^\[/p' agents-sdk/config.toml \
  > ~/Code-Brain/backups/claim6-registration-2026-08-31.txt
cat ~/Code-Brain/backups/claim6-registration-2026-08-31.txt
```

`~/Code-Brain/backups/` is **outside the repo** — that is the point, and it is where the pre-B8 database snapshot already lives. Confirm the four values are present in the output, and paste it.

## Task 2 — Install a pre-commit guard

There are currently **no active git hooks** on this machine, `core.hooksPath` is unset, and there is no `.pre-commit-config.yaml` — verify all three before writing, and if any has changed since, **stop and report** rather than overwriting someone's hook.

Write `.git/hooks/pre-commit` (local-only, never tracked) and `chmod +x` it:

```sh
#!/bin/sh
# Local-only guard. Blocks committing an ARMED claim-6 drill registration.
# eng-002.d159/d160. Installed 2026-08-31, before B3's window.
#
# Fails OPEN on anything unexpected: during a live certification a hook that
# blocks every commit on the production machine is a worse failure than the
# leak it prevents. It objects only in the one case it understands.

CFG="agents-sdk/config.toml"

# Not staged? Nothing to say. This is the path Obsidian-Git's vault commits take.
git diff --cached --name-only 2>/dev/null | grep -qx "$CFG" || exit 0

# Judge the STAGED content — that is what would actually be committed.
staged="$(git show ":$CFG" 2>/dev/null)" || exit 0
printf '%s' "$staged" | grep -q 'schedule_enabled = true' || exit 0

cat >&2 <<'MSG'
BLOCKED — agents-sdk/config.toml is staged with the claim-6 drill ARMED.

That registration is production deploy state and must not enter this public
repo: acknowledged_device is a personal device name, and committing it turns
the suite red (tests/test_claim6_schedule.py reads the COMMITTED config and
asserts the drill ships disarmed).

  Unstage just this file:  git restore --staged agents-sdk/config.toml
  Then commit as normal.

Backup of the live values: ~/Code-Brain/backups/claim6-registration-*.txt

If you truly intend to commit a config change, disarm the drill first, or
override deliberately with:  git commit --no-verify
MSG
exit 1
```

**Then prove it works, and prove it is narrow** — a guard nobody tested is a guess. Run all three, leave nothing staged, and paste the real output:

1. **It blocks the bad case:** `git add agents-sdk/config.toml` then `git commit -m "test"`. Expect the BLOCKED message and a non-zero exit. Then `git restore --staged agents-sdk/config.toml`.
2. **It ignores everything else:** stage some unrelated file (a vault file already dirty is fine) and confirm a commit would proceed — use `git commit --dry-run` so **nothing is actually committed**. Then unstage it.
3. **The tree is exactly as you found it:** `git status --porcelain agents-sdk/config.toml` still shows ` M`, and `git diff --cached --name-only` is empty.

## Task 3 — Make a silent disarm loud

Write `.git/hooks/post-merge`, `chmod +x`, same fail-open discipline. This catches the larger hazard: a merge that drops the registration while the plist stays loaded.

```sh
#!/bin/sh
# Local-only. Warns when a merge has disarmed the claim-6 drill while its
# launchd plist is still loaded — the silent-disarm case (eng-002.d160).
# Advisory only: never blocks, never exits non-zero.

CFG="agents-sdk/config.toml"
grep -q 'schedule_enabled = true' "$CFG" 2>/dev/null && exit 0
launchctl list com.sean.agent.claim6-drill >/dev/null 2>&1 || exit 0

cat >&2 <<'MSG'

*** claim-6 drill DISARMED by this merge, but its plist is still loaded. ***

The scheduled runner will fire and decline to send. B3 nights will not be
green and nothing else will say so.

Restore the four values into [agents.claim6_drill] in agents-sdk/config.toml
from ~/Code-Brain/backups/claim6-registration-*.txt, then re-check with:

  cd ~/Code-Brain/code-brain/agents-sdk && PYTHONPATH=. .venv/bin/python3 \
    schedules/render_claim6_plist.py --config config.toml --check-enabled

MSG
exit 0
```

Verify it is executable and that it exits 0 in the current (armed) state — it must print nothing today.

## Hard constraints — violating any of these fails the pass

- **Do not disarm the drill, do not edit the four registered values, and do not run the installer.** B3 opens tomorrow.
- **Do not commit or push anything**, including these hooks — `.git/hooks/` is local by nature and must stay untracked. Do not add a hooks directory to the repo, and do not set `core.hooksPath`.
- **Do not use `git update-index --skip-worktree` or `--assume-unchanged`.** They look like the answer and are the wrong one: they hide the file's state, make future merges fail in confusing ways, and can lose the local value outright — the exact silent disarm Task 3 exists to catch.
- **Do not fire the drill or send any test push.** The runner has no manual send mode; do not work around it.
- **Do not edit code** under `agents-sdk/`, `.claude/` or `scripts/` — deploy targets, overwritten by the next deploy.
- **Leave the working tree exactly as you found it.** `config.toml` stays dirty; nothing staged when you finish.
- **Verify, do not assert.** Paste real output for every claim.

## Report back

1. The backup file's path and contents.
2. Confirmation that no pre-existing hook was overwritten, plus the three pre-commit test results — blocked, narrow, tree unchanged.
3. That `post-merge` is executable and silent in the armed state.
4. `git status --porcelain agents-sdk/config.toml` and `git diff --cached --name-only` at the end.
5. Anything you found and did **not** fix, named explicitly — including whether you think either hook could misfire during the Sep 1–7 window.

Then per CLAUDE.md rule 8, add a one-line `- ` bullet under `## Todo` in `vault/00_inbox/tickets.md` recording that these guards are **local to this machine only** — a fresh clone, or a `.git` rebuild, has neither, and the durable fix (a gitignored local-override file the config loader reads) remains unbuilt.
