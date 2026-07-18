# Cap-policy governance

`cap_policy.json` is the one content home for cap numbers. Editing any cap value is a cap change and requires Sean's explicit approval — the plan → approve → execute gate recorded in **the-oracle's** CLAUDE.md (rule 2 / §Spend governance) and the approved F8b plan (`the-oracle/docs/phase-plans/2026-07-18-f8b-ledger-governance.md`). Content review and activation are separate gates: reviewed content lives in git, while `python -m council.policy activate` publishes the exact validated snapshot to the shared spend root as `council-policy-active.json`. The shared activation, not any process's local checkout, is the cross-process authority.

Until the F8b migrations complete, the legacy value homes (`council/cli.py` `_DAILY_CAP_USD`/`_MONTHLY_CAP_USD`, `council/discovery/__main__.py` `DISCOVERY_*_CAP`, `experiments/panel_vs_single.py`, `the-oracle/oracle/config.py`) still exist; Tasks 3–6 wire each through the registry's enforced equality check so any drift between a code home and the activated policy fails closed instead of silently diverging. Money values are authored as JSON decimals (`7.00`, never `7`) so one semantic policy has exactly one canonical hash.

The council per-query census is `[0.40, 1.00]`: premium is $1.00 and the Sean-approved variance/interview-grader profiles in `profiles.py` are $0.40. This completes the census; it does not change a cap.

Council and discovery use `reservation_basis: "estimate"` today because their preflights reserve estimates. Tasks 3d and 4 respectively flip them to `"worst_case"` only in the same commits that make those bounds true.

`sum_exceeds_aggregate: true` asserts the decided relation: tool daily caps sum to $262 > $245 and monthly caps sum to $1,090 > $1,000. The shared aggregate can therefore bind first and starve a tool before its own cap; admission must refuse loudly and deterministically.
