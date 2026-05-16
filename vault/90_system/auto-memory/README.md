# auto-memory · cross-machine sync mirror

Snapshot mirror of Claude Code's auto-memory directory for this repo. The live, agent-readable location is per-machine and outside this repo:

```
~/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/
```

Claude Code reads memory from that path only. Files in *this* directory are a manual snapshot so the Mac Mini (and any future fresh machine) can restore memory after a `git pull` without losing context from sessions run on other machines.

## What's in here

| File | Type | Notes |
|---|---|---|
| `MEMORY.md` | index | Always loaded into Claude context — keep it under 200 lines |
| `feedback_*.md` | feedback | Behavioral guidance Sean has given |
| `project_*.md` | project | Active project state, deferrals, in-flight work |

## Restore on a fresh machine (or after a stale-memory drift)

```bash
# from repo root
TARGET="$HOME/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory"
mkdir -p "$TARGET"
cp vault/90_system/auto-memory/*.md "$TARGET/"
```

After restoring, start a new Claude Code session in this repo. The next time Claude consults memory, it'll pick these up.

## Bidirectional sync caveat

This is a **snapshot, not a live sync.** Files written here are frozen at commit time. If you write new memories on the Mac Mini after restoring, those won't appear here until you manually copy them back and commit.

A future cron / SessionEnd hook could automate the mirror in both directions. Not built yet — see `claude-mastery/` if you want to scope that.

## What's intentionally NOT mirrored

- Files older than ~30 days that have not surfaced in any recent session (stale risk outweighs sync benefit).
- Anything containing credentials, machine-specific paths only relevant to one host, or PII Sean wouldn't put in the public repo.

Last manual sync: 2026-05-16.
