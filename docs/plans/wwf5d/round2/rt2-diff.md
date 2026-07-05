# RT2 diff — Fable vs Opus on skill-audit(hooks-configuration) (axis: existence-check / false-sense-of-safety, §2.4)

**Compared:** `rt2-fable.md` (12 findings: 4 DW / 5 S / 3 m) vs `rt2-opus.md` (8 findings: 2 DW / 5 S / 2 m). Identical harness (`skill-audit`), target, pinned grounding. Tags `dangerously-wrong`/`structural`/`minor`, direction **FABLE+** / **OPUS+**.

**Headline + the ceiling result.** This was the ceiling probe: **does Fable's BT1 existence-check blind spot recur?** It did **not** — Fable existence-checked *harder* than Opus here, catching three inert protection layers to Opus's one and reading the live upstream docs. Both arms verified the world (both caught the dead-payload-key firewalls + the 5 unregistered scripts — the shared headline). The split: Fable found the skill **teaches** false-safety patterns (a bypassable substring firewall, a matcher that can't be a file boundary) and is a platform version behind (checked live docs); Opus uniquely caught two bypass patterns Fable didn't (env-var opt-out; prompt-hook-for-security). A genuinely balanced diff — the sharpest of the three — with Fable's premium in breadth + proactive research and a real OPUS+ tail.

---

## FABLE+ deltas (admissible WWF5D evidence)

- `dangerously-wrong` — **FABLE+ — the skill TEACHES a bypassable substring blocklist as a security boundary.** Fable: the "Security Firewall (Bash)" pattern (`[[ "$CMD" == *"rm -rf"* ]]`) is defeated by `rm -fr`, `rm -r -f`, `$IFS`, quoting, base64-pipe — and upstream says the *permission system*, not a hook, must enforce a hard deny. The skill presents it as the reference firewall and moves on. **Opus never flagged the blocklist's bypassability at all** (Opus's DW findings are the payload-key mismatch + disk-vs-registration). This is the exact "flag false-safety patterns instead of teaching them" the (d) wow-bar demands — Fable's catch, Opus's miss.

- `dangerously-wrong` — **FABLE+ — Example 1's `.env` block is bypassable by design (a matcher is not a file-access boundary).** Fable: `Read|Edit|Write` doesn't stop `Bash cat .env`, `Grep`, or an MCP file tool; hard file-access denial belongs in `permissions.deny` (`Read(./.env)`). Opus caught the *implementation* bug (the live hook reads dead keys) but not the *design* bug (a matcher can never be a complete file boundary regardless of keys). Breadth past the named seam — Fable audited the design, Opus audited the code.

- `dangerously-wrong` — **FABLE+ — the third inert layer: the `permissions` block uses an invented schema.** Fable existence-checked settings.json's `permissions` (`default`/`rules`/`pattern`) against the real Claude Code shape (`allow`/`deny`/`ask` arrays with `Read(./.env)` entries) → the `.env` deny is *also* inert. "Three layers of '.env is protected,' zero of them real." Opus checked the hooks + registrations but not the permissions-block schema. Verify-the-world went one layer further.

- `dangerously-wrong` — **FABLE+ — exit-1-fails-open is a security trap the skill doesn't flag.** Fable: a weaker model will `sys.exit(1)` on an internal error (jq missing, malformed JSON) → Claude reads 1 as non-blocking → the guarded action **proceeds** (fails open); upstream has a standing warning. Opus didn't surface exit-1-fail-open. A real fail-open security hazard.

- `structural` — **FABLE+ — the `timeout: 5000` = 83-minutes unit bug, caught live.** Fable read the actual registration and knew the unit (`timeout` is seconds), flagging the SessionStart hooks' 5000 = 83 min. Opus didn't. Verify-the-world at the config level.

- `structural` — **FABLE+ — proactive current-best-practice research: the skill is a platform version behind.** Fable **fetched the live upstream hooks docs** (code.claude.com/docs) and found missing hook types (`http`, `mcp_tool`), the modern **`permissionDecision` structured-deny output** (the clean deny-with-reason path the skill never teaches), and a ~20+ event set vs the skill's 8. Opus flagged the internal body-vs-reference event drift (minor) but **did not check upstream** — it reasoned from the repo. This is the research-trigger hypothesis firing: Fable researched the current state of the world unprompted; Opus didn't. (Cross-corroborates RT3.)

## OPUS+ deltas (ceiling evidence — F3)

- `structural` — **OPUS+ — the env-var opt-out bypass. Fable didn't name it.** Opus: `require-confirm-highrisk.sh` honors `CLAUDE_ALLOW_HIGHRISK=true` — any process that can set one env var disables the "firewall"; the skill should flag env-var opt-outs as trust-weakening, not treat the hook as unconditionally enforced. Fable noted the hook is dead anyway but didn't surface the bypass-once-fixed. A specific false-safety pattern Opus caught and Fable missed.

- `structural` — **OPUS+ — don't use prompt/agent hooks for *security* (probabilistic enforcement).** Opus tied it to CLAUDE.md rule 3 ("hooks enforce; subagents judge"): a security block implemented as a Haiku `prompt` hook enforces probabilistically and can time out to allow — for security, deterministic `type: command` is mandatory. Fable *added* http/mcp_tool types but didn't flag the security-must-be-deterministic rule. Another false-safety pattern in the OPUS+ column.

## Matched (no meaningful delta — cheap on Opus)

- The dead-firewall headline: both independently caught that `block-secrets.py` + `require-confirm-highrisk.sh` read Cursor-schema keys (`tool`/`target`/`run_terminal_cmd`) Claude Code never sends → `exit 0` on every call → registered no-op security layer. Both caught the 5 unregistered/orphaned scripts. Both prescribed the same three missing moves (verify-the-payload-contract; disk-vs-registration reconciliation; prove-the-deny-by-piping-a-payload). This convergence *is* the existence-check premium landing on both — and it validates the substrate.

## ⚖ Ceiling watch-for result (the reason RT2 exists)

**Fable's BT1 existence-check blind spot did NOT recur.** In BT1 Fable missed the unverified-enforcement seam entirely (Opus's best find); here, un-WWF5D'd, Fable caught the existence-check class *thoroughly* — arguably more than Opus (three inert layers vs one; the taught-bypassable firewall; the live-docs version gap). Caveats: (1) different substrate than BT1 — a hooks skill makes "enforced via X" claims maximally salient, so this doesn't prove the blind spot is gone in general; (2) it's a paired premium-harvest, not a with/without-WWF5D arm — whether §2.4 *closes* the gap for the deployment models (Opus/Sonnet) routes to **Step 4** (RT2's prompt is a held-out validation task there). What RT2 *does* show: on an enforcement-claim-dense substrate, existence-checking emerges for Fable without the recipe — encouraging for the premise, and a reason to keep §2.4 as an explicit Opus/Sonnet aid (they need it more than Fable did here — note Opus's DW set was narrower on the *design*-level bypasses).

## Bottom line

Balanced and rich. **FABLE+** in breadth (three inert protection layers; design-level `.env` bypass; the taught bypassable firewall; exit-1-fail-open; the timeout unit) and **proactive research** (live upstream docs → missing types + `permissionDecision`). **OPUS+** in two specific false-safety patterns (env-var opt-out; prompt-hook-for-security). Corroborates §2.4 (existence-check — now on both models), §1.3 (verify-the-world, incl. live docs), §2.1 (breadth past the named seam). New candidate: **"read the current upstream contract, not just the local one — a config skill can be a platform version behind, and the repo's own artifacts can't tell you that"** (§1.3 extension: first-degree references include the *live external spec*, corroborated on RT3 too).
