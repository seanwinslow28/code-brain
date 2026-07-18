# Cap-policy governance

`cap_policy.json` is the one content home for cap numbers. Editing any cap value is a cap change and requires Sean's explicit approval — the plan → approve → execute gate recorded in **the-oracle's** CLAUDE.md (rule 2 / §Spend governance) and the approved F8b plan (`the-oracle/docs/phase-plans/2026-07-18-f8b-ledger-governance.md`). Content review and activation are separate gates: reviewed content lives in git, while `python -m council.policy activate` publishes the exact validated snapshot to the shared spend root as `council-policy-active.json`. The shared activation, not any process's local checkout, is the cross-process authority.

Until the remaining F8b migrations complete, the legacy value homes (`council/discovery/__main__.py` `DISCOVERY_*_CAP`, `experiments/panel_vs_single.py`, `the-oracle/oracle/config.py`) still exist; Tasks 4–6 wire each through the registry's enforced equality check so any drift between a code home and the activated policy fails closed instead of silently diverging. The council CLI now loads its daily/monthly and aggregate caps from this registry. Money values are authored as JSON decimals (`7.00`, never `7`) so one semantic policy has exactly one canonical hash.

Policy version 2 records Sean's 2026-07-18 Task 3c approval for the council: the enumerated per-query caps are `[5.50, 11.50, 13.00]` for variance, premium, and interview-grader respectively; the tool caps are $45/day and $250/month; and admission reserves the structural worst case.

Council uses `reservation_basis: "worst_case"`. Discovery remains on `"estimate"` until its separate Task 4 migration.

`sum_exceeds_aggregate: true` asserts the decided relation: tool daily caps sum to $300 > $245 and monthly caps sum to $1,300 > $1,000. The shared aggregate can therefore bind first and starve a tool before its own cap; admission must refuse loudly and deterministically.
