# Status vocabulary — reader-facing law

*Ratified 2026-08-29 (eng-003.d50–d52). The rule this file exists to enforce: **a proof that a count is right is not proof that the counted thing is right**, and a summary may never outrun the record it summarizes.*

## Authority and derived surfaces (d50)

| Claim | Authoritative record | Derived surfaces |
|---|---|---|
| Gate verdict | The named gate findings artifact's verdict line | Ledger entry, RESUME, index, digest, coordinator status |
| Sean decision | The dated Sean-ratified ledger entry or Close record | RESUME, index, digest |
| Current defect state | Latest valid owning-seat entry (supersession history preserved) | RESUME, index, digest |
| Proof result | The persisted proof output/evidence record at its capture instant | Artifact prose, entry, digest |

Every derived rendering opens with `DERIVED STATUS — <typed state>`, the authoritative record's path, and a checked instant. No gate verdict propagates while its findings artifact is absent (`GATE RUNNING — VERDICT NOT RECORDED`). If a derived value disagrees with its authority, every reader-facing surface fails closed to **`STATUS CONFLICT — DO NOT RELY`** — conflicting records named, no PASS/Close/launch/outcome claim permitted, coordinator reconciles. The wrong line is retained with a dated correction, never silently overwritten.

## Proof results (d51)

The headings **"All proofs green," "Verification passed," "Everything passed"** are banned. Every proof or bundle renders: the literal output · **Exercises** (the exact rule/fixture/path checked) · **Does not exercise** (the nearest claim a reader could wrongly infer) · evidence (command/query, path, capture instant, hash for live data) · the **permitted conclusion** (the smallest statement the result supports) · the decision effect. A bundle's header is `PROOFS EXECUTED AT THEIR STATED BOUNDARIES`; heterogeneous checks never share one color or verdict.

## Typed statuses (d52)

Never render bare `PASS`, `FAIL`, `Close`, `REVIEW`, `UNPROVEN`, `$0`, or a lone green icon. Every state carries three lines: the typed status · **Means** · **Does not mean / Next**.

| Situation | Required rendering | Prohibited shorthand |
|---|---|---|
| Design gate passed, runtime obligations open | `DESIGN PASS — IMPLEMENTATION HOLDS OPEN · NOT LAUNCH-READY` | `PASS + holds`, `ready`, green check alone |
| Administrative Close, outcome unmeasured | `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14` | `Closed successfully`, `done`, `success` |
| Required work paused by availability | `OPEN — DEFERRED · REQUIRED WORK NOT COMPLETE` | `Deferred` alone, `parked` |
| Approved allowance exhausted | `BUDGET STOP — WORK PAUSED · NO QUALITY OR OUTCOME VERDICT` | `cap met`, icon alone |
| Stopped with owed work open | `TERMINATED — INCOMPLETE / SUCCESS UNPROVEN` | `Closed`, `completed` |
| Provenance heuristic flags | `PROVENANCE REVIEW — HUMAN JUDGMENT REQUIRED` | green REVIEW count, `clean` |
| Required provenance absent/invalid | `PROVENANCE FAIL — CLAIM MUST NOT BE USED` | `warning`, waiver into PASS |
| No retained observation | `UNMEASURED — NO RETAINED OBSERVATION` | `0`, `$0`, blank, `N/A` |
| Claim lacks evidence | `UNPROVEN — <specific claim>` + the event that could prove it | `TBD`, naked `UNPROVEN` |
| Any gate verdict | `<PRD \| DESIGN \| LAUNCH \| AUDIT> <PASS \| PASS WITH ACCEPTANCES \| FAIL> — QUALITY VERDICT ONLY` + scope + authority | bare `PASS`; one gate type quoted as another |

## Cost wording (d52)

`subscription-absorbed` and `$0` never appear as totals. Every cost line carries its riders: `Sean attention: <measured | UNMEASURED>` · `Elapsed time: <measured | UNMEASURED>` · excluded costs named. Canonical form: `Claude usage: $0; Codex billing: subscription-absorbed, marginal cash UNMEASURED; Sean attention and opportunity cost: UNMEASURED.` A billing fact must survive without erasing the scarce human input.
