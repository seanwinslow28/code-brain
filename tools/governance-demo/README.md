# governance-demo

A 60-second, runnable demonstration of the **Authority / Recovery / Audit** control
trinity described in [`agents-sdk/docs/CONTROL_ARCHITECTURE.md`](../../agents-sdk/docs/CONTROL_ARCHITECTURE.md).
It replays a synthetic spend request through the same shape of control logic the real
agent fleet enforces, and shows all three legs fire on a budget breach: the policy
blocks, the human is paged, the breach is written to a ledger, and a rollback path is
printed.

## Run it

```bash
# from this directory
python3 replay_budget_breach.py --fixture allowed        --dry-pushover
python3 replay_budget_breach.py --fixture over_budget    --dry-pushover
python3 replay_budget_breach.py --fixture missing_auth   --dry-pushover
```

Exit codes (a **demo convention** — see the stub boundary below):

| fixture        | what it shows                                            | exit |
|----------------|----------------------------------------------------------|------|
| `allowed`      | spend within the daily cap, key present → ALLOW          | `0`  |
| `missing_auth` | keychain key stripped → Authority denies at the cred gate| `3`  |
| `over_budget`  | spend breaches the cap → circuit trips, ledger + page    | `7`  |

`--dry-pushover` logs the page instead of sending it (use for rehearsal and CI). The
**live** `over_budget` run, without `--dry-pushover`, sends a real Pushover
notification when `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are set in the
environment:

```bash
PUSHOVER_USER_KEY=... PUSHOVER_API_TOKEN=... \
  python3 replay_budget_breach.py --fixture over_budget   # fires a real page; exit 7
```

## Test it

```bash
python3 -m pytest test_replay.py -v
```

Seven tests assert that the three fixtures exercise three distinct code paths (exit
`0` / `3` / `7`), that `missing_auth` denies *before* the budget is evaluated, and
that `--dry-pushover` never opens a network connection.

## The stub boundary (read this)

This harness is **stubbed and synthetic by design**. It is portfolio evidence of the
control *shape*, not a live driver of the fleet:

- **No LLM, no agent runner, no paid API is called.** Each file under `fixtures/` is a
  hand-authored, obviously-synthetic record of what an agent runner *would have*
  requested (note the `_comment` and `(synthetic)` task names). The numbers are made up.
- **The ledger is a demo file.** Runs append to `outputs/sample_ledger.jsonl` here,
  never to the real fleet ledgers under `vault/health/`. `outputs/sample_ledger.jsonl`
  is committed with one captured row per fixture so a reader can inspect the output
  shape without cloning and running.
- **Exit code `7` is a demo convention.** The production fleet enforces hook exit codes
  `0` / `1` / `2` (see [`CLAUDE.md`](../../CLAUDE.md) "Hook Exit Codes") plus typed
  exceptions (`RouteUnavailable` in [`hybrid_router.py`](../../agents-sdk/lib/hybrid_router.py),
  budget-cap aborts). This demo adopts `7` = "budget breach" and `3` = "auth denied"
  so the worked example has unambiguous, greppable outcomes. They are not claims that
  every production agent emits those codes today.
- **Credentials come from env, not the Keychain.** The real fleet sources secrets from
  the macOS Keychain via [`lib/keychain.py`](../../agents-sdk/lib/keychain.py); this demo
  reads `PUSHOVER_*` from the environment to keep its dependency surface to the stdlib.

## Files

```
governance-demo/
├── replay_budget_breach.py     # the harness (stdlib only)
├── fixtures/
│   ├── allowed.json            # within budget, key present
│   ├── over_budget.json        # breaches the daily cap
│   └── missing_auth.json       # keychain key stripped
├── outputs/
│   └── sample_ledger.jsonl     # one captured row per fixture (committed)
├── test_replay.py              # 7 tests, no network, tmp ledgers
└── README.md
```
