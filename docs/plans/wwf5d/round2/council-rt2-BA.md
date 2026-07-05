# Council Session — wwf5d-val-rt2-BA

- **Session ID:** `20260705-141448-84c3a7`
- **Profile:** `variance`
- **Duration:** 82.4s
- **Tokens:** 86766 in, 5321 out
- **Cost:** $0.5136

## Original prompt

```
Two independent authors produced these two artifacts for the identical task from the identical inputs. Judge which is the stronger artifact.

## Task context

Both artifacts are a skill audit (a seam report plus an improvement spec) of a Claude-Code-hooks configuration skill, written from the same brief about the same skill and the same repository.

## Judging rubric — score ONLY these; ignore length and prose polish

1. **Decidedness** — pre-made decisions (field names, error shapes, done-criteria), edge guidance a weaker implementer could act on; not options/hedging.
2. **Self-consistency** — does any rule the artifact states contradict its own stated objective? (e.g. a "cap-and-delete" inside a zero-loss spec; a step that writes a value nothing downstream reads.)
3. **Breadth / evidence-discipline** — did it verify claims against the real system (real files, live docs, the actual tool) vs reason from text; did it audit seams the brief didn't name.
4. **Task-specific** — depth of existence-checking against the real repository: bypassable firewalls, wrong-schema configs, gaps between the live upstream docs and what the repo actually implements, and false-safety patterns the skill *teaches* (as opposed to ones it merely flags).

## Bias controls

One artifact is substantially longer than the other — do NOT reward length. A shorter artifact that is more decided and more self-consistent wins over a longer one that merely says more. Judge A and B strictly on merit regardless of which order they appear in below.

## ARTIFACT A

# Skill Audit — `hooks-configuration`

Audited the way its most demanding consumer would: a weaker model following this skill to write the fleet's real enforcement hooks (`.claude/hooks/*` + their `.claude/settings.json` registrations + the exit-code contract). Evidence base per §1.3: the 15 shipped hooks, the live `settings.json`, the skill's own `references/hook-events.md`, and the **live external contract** — the official Claude Code hooks docs at `docs.claude.com/en/docs/claude-code/hooks` — because a config skill can be a platform version behind and the repo cannot reveal that from the inside.

---

## Step 1 — Grounding (pre-pinned; restated, then consumed)

The four grounding answers were supplied. Per §1.1 I restate each in my own words, and each reappears below *doing work* in a finding — not just acknowledged.

- **(a) For** — Creating/configuring/debugging Claude Code hooks that enforce security + automate quality across the fleet's *deterministic* enforcement layer: the 15 hooks in `.claude/hooks/`, registered in `.claude/settings.json`. This is the layer CLAUDE.md calls out as "Hooks enforce; subagents judge" (Non-Negotiable Rule #3) — the binary allow/deny substrate the fleet trusts to be *always-on*, unlike model judgment.
  - *Consumed in:* SR-1 / SR-2 — the shipped enforcement hooks the skill is the guide for read a foreign schema and don't enforce; SR-6 — the fleet's own CLAUDE.md doctrine repeats the skill's incomplete exit-code model, so the error is already propagating into standing context.

- **(b) Feeds** — A *weaker model following this skill* writes real enforcement hooks the fleet depends on: actual `.claude/hooks/*` scripts, their `.claude/settings.json` registrations, and the exit-code contract that decides whether a block fires. The "downstream consumer" here is not another skill — it is Claude Code's own hook runtime, which parses stdin (`tool_name`/`tool_input`), interprets exit codes *per event*, and reads structured stdout (`hookSpecificOutput.permissionDecision`).
  - *Consumed in:* SR-1 (stdin field-name contract), SR-3 (exit-2-is-event-specific contract), SR-4 (the modern JSON-deny contract) — all three are receiving-runtime shapes the skill either gets wrong or omits.

- **(c) Disappoints** — A hook that *looks* configured but doesn't block what you think: a bypassable firewall, an unregistered hook, a hook type/matcher that doesn't fire as claimed. You trust "enforced" and it isn't. This is a false sense of safety — §2.4's exact target ("a named-but-unwired guard is worse than an admitted gap").
  - *Consumed in:* every `dangerously-wrong` finding. The signature failure the owner would hit is precisely this: `block-secrets.py` is registered, executable, exits 2 on match — and still never blocks a real `.env` write, because it tests `tool_name` against the string `"edit"` while Claude Code sends `"Edit"` in a field named `tool_name`, not `tool`.

- **(d) Wow** — Every enforcement claim is *verifiably true against this repo's real hooks + settings.json*; following the skill provably blocks; and it *flags false-sense-of-safety patterns instead of teaching them*. The bar is not "explains hooks" — it is "a hook written from this skill, dropped into this repo, actually denies the thing it names, and the skill made the author prove it before trusting it."
  - *Consumed in:* the Wow-gap scan (WG-1/WG-2) and the spec's "Verify-the-block drill" and "Fail-open audit" additions.

**Headless-case note (§1.5):** this skill has no interactive ask-step and no chain to a subagent, so no pre-answered path is needed. The consumer is a runtime, not a person — which is *why* shape-precision (§5.1) matters more here than a clarifying-question path.

**Epistemic-framing hold (§1.2):** the pinned "Disappoints" is stated as a *risk pattern* ("looks configured but doesn't block"). Where I found it *realized* in this repo (the shipped enforcement hooks), I mark it observed-and-verified against the live contract; where I only reason about runtime behavior I couldn't execute, I mark it as a test obligation, not asserted fact.

---

## Ground-truth census (§2.1/§2.2 — existence-check before believing)

Before scanning the skill's *claims*, I inventoried what the skill is actually the guide for. Two schema families coexist in `.claude/hooks/`, and that split is the whole story:

| Hook | Event (per settings.json) | Registered? | Reads stdin as… | Schema verdict |
|------|---------------------------|-------------|-----------------|----------------|
| `block-secrets.py` | PreToolUse `Write\|Edit` | **yes** | `hook_data.get('tool')`, `.get('target')`; `tool_name in ['write','edit',...]` | **WRONG** (Cursor schema) |
| `require-confirm-highrisk.sh` | PreToolUse `Bash` | **yes** | grep `"tool"`; `TOOL_NAME == "run_terminal_cmd"\|"bash"` | **WRONG** |
| `network-access-control.sh` | *(none)* | **no** | same `run_terminal_cmd`/`bash` gate | WRONG **and** unwired |
| `cost-watchdog.py` | *(none)* | **no** | `hook_data.get('tool')` (lowercased) | WRONG and unwired |
| `loop-detector.py` | *(none)* | **no** | `hook_data.get('tool')` + `tool_input` | partial (right `tool_input`, wrong `tool`) and unwired |
| `vault-integrity.py` | *(none)* | **no** | `tool` (lowercased) + `tool_input` | partial and unwired |
| `format-on-edit.sh` | PostToolUse `Write\|Edit` | yes | grep `"target"` then `"file_path"` | WRONG-ish (real key is `tool_input.file_path`, but non-blocking so harmless) |
| `log-tool-use.sh` | PostToolUse (all) | yes | grep `"tool"`/`"target"` | WRONG (logs `unknown`/`N/A`; non-blocking) |
| `run-tests-on-stop.sh` | Stop | yes | ignores stdin | fine |
| `session-start-inject-index.sh` | SessionStart | yes | emits `hookSpecificOutput.additionalContext` | **CORRECT** |
| `session-start-inject-tickets.sh` | SessionStart | yes | emits `hookSpecificOutput`/`additionalContext` | **CORRECT** |
| `session-end-flush.sh` | SessionEnd | yes | greps `transcript_path` | **CORRECT** |
| `session-end-auto-stub.sh` | SessionEnd | yes | (fleet lifecycle) | (lifecycle) |
| `pre-compact-flush.sh` | PreCompact | yes | (fleet lifecycle) | (lifecycle) |
| `daily-note-appender.sh` | *(none)* | no | (fleet lifecycle) | unwired |

**The load-bearing observation (§3.3 — record-vs-record disagreement IS the signature):** the fleet's own **lifecycle** hooks (`session-*`) use the *correct* Claude Code schema — `transcript_path`, `hookSpecificOutput`, `additionalContext` — proving the real contract is known in this repo. The **enforcement** hooks (the security firewall this skill exists to author) use a *foreign* schema — `tool`, `target`, `run_terminal_cmd` — that the live docs confirm appears **nowhere** in Claude Code (`run_terminal_cmd`: 0 occurrences, case-insensitive). And the skill's **own example code** (Example 1, and the "Complete Hook Script Patterns" block) uses the *correct* schema (`data.get('tool_input', {}).get('file_path', '')`). So: the skill documents right, the shipped enforcement hooks it guides are wrong, and **the skill never contains the one check that would catch the gap.** That is the audit's spine.

**Live-contract facts** (from the official docs — the version-gap probe, §1.3):
- Input field is **`tool_name`** (not `tool`); Write/Edit path is **`tool_input.file_path`**; Bash tool name is exactly **`Bash`**.
- Exit-code 2 semantics are **per-event**: PreToolUse exit 2 *blocks*; PostToolUse exit 2 *cannot block* ("the tool already ran"); SessionStart exit 2 *cannot block* and stderr goes *to the user, not Claude*; UserPromptSubmit exit 2 blocks *and erases the prompt*; Stop exit 2 *prevents stopping*.
- Exit code **1 fails OPEN** for a policy hook — the docs warn explicitly: *"Claude Code treats exit code 1 as a non-blocking error and proceeds with the action… If your hook is meant to enforce a policy, use `exit 2`."*
- The **modern PreToolUse deny** is `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "…"}}` on **exit 0** — *not* a top-level `decision: "block"` (which PreToolUse ignores) and not only exit 2. Precedence `deny > defer > ask > allow`.
- Matchers are **exact-string OR JS-regex depending on the characters present**; a bare `mcp__memory` (no `.*`) is treated as an *exact* string and **matches no tool**.

---

## Step 2 — Seam Scan (decided-inputs that don't survive to point-of-effect)

A "decided input" in a config skill = a contract fact the skill states early that a later section (or the reader's hook) must honor. §2.3: trace to *point-of-effect*, not point-of-arrival — the seam is where the value arrives and doesn't act.

- **SEAM-1 — The stdin field name is decided TWICE, inconsistently, and the wrong one is where the reader copies from.** The skill's `references/hook-events.md` correctly says the matcher target is `tool_name` and the payload key is `tool_name`. But the **Exit Code Protocol table**, the **Matcher Reference table**, and every prose mention treat the tool identity abstractly, and the *inline* examples in "Command Hooks" / "Matcher Reference" show `"matcher": "Bash"` without ever showing the reader that the *script* must read `tool_name`, not `tool`. Point-of-effect failure: a reader who models their script on the shipped `block-secrets.py` (or on any Cursor tutorial) reads `tool`/`target` and the block silently never fires. The skill has no step that says "your field extraction must match the payload in `references/hook-events.md` exactly, or the hook fails open." → drives SR-1.

- **SEAM-2 — "Exit code 2 = Deny" is decided once, globally, and consumed by events where it is false.** The "Exit Code Protocol" section states a single event-agnostic table (`2 = Deny — Action BLOCKED`). The Hook Event Reference table *does* carry a "Can Block?" column, but the two are never *joined*: nothing tells the reader "the exit-2 row you just read only holds for the Can-Block=Yes events." Point-of-effect failure: a reader adds a SessionStart or PostToolUse security check, returns exit 2, and it silently does not block (SessionStart stderr doesn't even reach Claude). The "Deny" semantics arrived but don't act at the event the reader chose. → drives SR-3.

- **SEAM-3 — The `matcher` is presented as a regex, but the exact-string/regex fork is dropped before the reader writes an MCP matcher.** "Matcher Reference": *"The matcher field is a regex that filters which tool calls trigger the hook."* The live contract: a matcher is an *exact string* unless it contains a regex-special character, and `mcp__memory` (no `.*`) matches **nothing**. Point-of-effect failure: a reader writes `"matcher": "mcp__github"` to guard a GitHub MCP tool, believes it's a substring/regex match, and it fires on zero tools — an unenforced guard that *looks* scoped. The skill's own table row `"mcp__.*"` happens to work, which masks the trap. → drives SR-5.

- **SEAM-4 — The security examples decide the event correctly (PreToolUse) but never state WHY that pairing is load-bearing, so the pairing doesn't survive to a reader's *new* check.** Example 1 registers `block-secrets` on `PreToolUse` — correct. But the skill never says "a *blocking* security check MUST be on a Can-Block event; the same script on PostToolUse enforces nothing." The decided input (enforcement ⇒ blocking-capable event) is present as an unexplained instance and evaporates the moment the reader writes a second, different check. This is §2.5's escalation-drop shape: the protection is there in the floor example, gone when stakes/variations rise. → folds into SR-3.

---

## Step 3 — Adapter Scan (does output land in the shape the runtime expects?)

The "downstream tool" is Claude Code's hook runtime. Its expected shapes: (a) a script that reads the *real* stdin JSON, (b) a `settings.json` block in the exact `{event: [{matcher, hooks:[{type, command}]}]}} ` shape, (c) for a modern deny, structured stdout.

- **ADAPTER-1 — No stdin adapter: the skill never converts "the payload" into the concrete field-read the runtime requires.** §5.1: a consumer named without its exact shape ships strong-content-wrong-shape. The skill hands the reader exit-code theory and script skeletons but no line that says "read `tool_name` and `tool_input.file_path` — these exact keys; anything else fails open." The proof it's missing: the shipped enforcement hooks all got this wrong, and the skill would not have caught a single one. → drives SR-1.

- **ADAPTER-2 — No JSON-output adapter for the modern deny path.** The runtime's *preferred* PreToolUse deny is `hookSpecificOutput.permissionDecision: "deny"` on exit 0. The skill's entire deny story is exit-2-to-stderr — a real but *older/coarser* channel. It never shows the JSON shape, so a reader who wants `deny`-with-reason-shown-to-Claude (or `ask`, or `updatedInput`) has no adapter and will hand-roll or omit it. The skill's own `references/hook-events.md` JSON schema block shows `type/command/prompt/model/timeout/async` but **no output-control fields at all**. → drives SR-4.

- **ADAPTER-3 — The `settings.json` registration shape is shown correctly but the "did it register?" verification is absent.** The skill shows the right JSON block, but "Disappoints" names *unregistered hook* as a top failure mode, and the census confirms 6 of 15 real hooks (incl. the WRONG-schema `network-access-control.sh` and `cost-watchdog.py`) are **written but never registered in settings.json** — they enforce nothing. The skill has no step: "confirm the hook appears under the intended event in the *active* settings.json, and confirm the matcher would select your tool." → drives SR-2 / WG-1.

---

## Step 4 — Wow-Gap Scan (gap to "every claim verifiably true; provably blocks")

- **WG-1 (highest leverage) — Missing "prove the block fires" drill.** The wow bar is "following it provably blocks." The skill stops at "exit code 2 blocks the intended action" (Success Criteria) with no procedure to *demonstrate* it against real stdin. The single highest-leverage addition is a copy-paste verification: pipe a realistic payload (`echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | .claude/hooks/block-secrets.py; echo "exit=$?"`) and assert `exit=2`. Run against the *current* `block-secrets.py` this prints `exit=0` — the drill *is* the finding. This is §5.2 (operationalize the real artifact under a check) and §5.4 (state lives on the artifact: an unverified hook is visibly un-blocked).

- **WG-2 (high leverage) — Missing "flag false-sense-of-safety patterns" section.** The pinned Wow explicitly wants the skill to *flag* bypassable patterns "instead of teaching them." The skill currently teaches at least three the fleet already shipped as live bugs: (i) reading `tool`/`target` instead of `tool_name`/`tool_input.*`; (ii) using `exit 1` for a policy hook (fails open — the docs' explicit warning); (iii) a **`CLAUDE_ALLOW_HIGHRISK` env-var opt-out** (`require-confirm-highrisk.sh`) that lets any process disable the firewall by setting one variable, and the general anti-pattern of a **`prompt`-type hook for a *security* decision** (an LLM firewall is non-deterministic — the wrong tier for hard enforcement, which is the whole "Hooks enforce; subagents judge" doctrine). A named "these look safe and aren't — reject them in review" block is the difference between a skill that *documents* hooks and one that hardens them.

- **WG-3 (lower leverage, real) — String-substring blocklists are the coarse trap the skill models.** `require-confirm-highrisk.sh` blocks `"format"` as a substring — it fires on `git format-patch`, `black --format`, `terraform fmt` is fine but `format` in any word trips; and it misses `rm    -rf` (tabs), `rm -fr`, and base64/`$IFS` obfuscation. The skill's Security Firewall pattern has the identical shape. Worth a one-line honesty note ("substring blocklists are advisory, not a security boundary; they over-block real commands and under-block obfuscated ones") — but *lower* priority than WG-1/WG-2 because it's a known limitation of the technique, not a silent-failure claim.

**Prioritization (per Step 4 requirement):** close **WG-1** (prove-the-block drill) and **WG-2** (false-safety flags) — together they convert the skill from "explains hooks" to "produces hooks that verifiably block, and refuses the patterns that only look safe." WG-3 is polish.

---

## Step 5, Artifact 1 — Seam Report

Every finding tagged exactly one severity. DW ordered first (§4).

- `dangerously-wrong` — **SR-1 · Stdin field-name contract absent (Seam Scan §Step 2 / Adapter §ADAPTER-1).** The skill never states that a hook must read `tool_name` and `tool_input.file_path` (and that the Bash tool is `Bash`, not `run_terminal_cmd`/`bash`). *What the owner observes:* a `PreToolUse` `Write|Edit` hook that greps `"tool"`/`"target"` — exactly the shipped `block-secrets.py` — exits 0 on a real `.env` write and the secret is written. The firewall is registered, executable, exits 2 on its match branch, and still never fires, because Claude Code sends `{"tool_name":"Edit","tool_input":{"file_path":".env"}}` and the script's `tool_name in write_tools` test is `False`. Silent × trusted × propagating: it fails open, in the layer the fleet trusts to be always-on, and nothing self-reports.

- `dangerously-wrong` — **SR-3 · "Exit 2 = Deny" taught as event-agnostic; it is event-specific (Seam §SEAM-2/§SEAM-4, Step: "Exit Code Protocol").** The "Exit Code Protocol" table asserts `2 = Deny — Action BLOCKED` with no event scoping, contradicting the live per-event contract. *What the owner observes:* a security check placed on `PostToolUse` or `SessionStart` (both plausible for "audit/scan on save" or "gate at session start") returns exit 2 and **does not block** — PostToolUse "already ran," SessionStart stderr never even reaches Claude. The author believes they built a gate; they built a log line. This is worse than SR-1 in one way — SR-1 is a copy-error the reader might catch; SR-3 is the *skill's own doctrine* being wrong, and it's mirrored verbatim into the fleet's CLAUDE.md (Rule #4, "Hook Exit Codes"), so the error already propagated to standing context (§3.3).

- `dangerously-wrong` — **SR-4 · The modern JSON deny path (`hookSpecificOutput.permissionDecision`) is entirely absent (Adapter §ADAPTER-2).** The skill's only deny channel is exit-2-stderr. *What the owner observes:* two failure shapes. (i) A reader who *does* try structured control copies a top-level `{"decision":"block"}` (the shape used by PostToolUse/Stop) into a PreToolUse hook — PreToolUse **ignores** top-level `decision`, so the tool proceeds; a deny that looks authored and silently no-ops. (ii) The reader cannot express `ask`, `defer`, `updatedInput`, or a deny-reason-shown-to-Claude at all, because the shape is undocumented. Tagged DW not because exit-2 is broken (it works for PreToolUse) but because the skill leaves the reader one keystroke from a silently-ignored deny with no warning.

- `structural` — **SR-2 · No "is it registered, and would the matcher select my tool?" verification step (Adapter §ADAPTER-3).** *What the owner observes:* over a third of the real hooks (`network-access-control.sh`, `cost-watchdog.py`, `loop-detector.py`, `vault-integrity.py`, `daily-note-appender.sh`) are written and never wired into settings.json — they enforce nothing, indefinitely, and look like coverage in the directory listing. Compounds silently: every new hook the skill helps author can join the unwired pile. Not DW only because it's a coverage/rot problem, not a believed-wrong output — but it is exactly the "looks configured but isn't" the owner named as a top disappointment.

- `structural` — **SR-5 · Matcher taught as "a regex"; it is exact-string-unless-special-char, and MCP prefixes without `.*` match nothing (Seam §SEAM-3).** *What the owner observes:* `"matcher": "mcp__github"` or `"matcher": "mcp__memory"` silently matches zero tools; the guard is inert. A weaker model, told "matcher is a regex," will reasonably write bare prefixes. Compounds: MCP-tool guarding is a growing need in this fleet and this trap scales with it.

- `structural` — **SR-6 · Exit-code-1 undersold as merely "logged but ignored"; for a policy hook it fails OPEN, and the docs say so explicitly.** The skill's row reads `1 = Error — Action proceeds. STDERR logged but ignored.` — technically true, but it buries the danger: a security hook that hits an internal error (bad `jq`, missing python, an unhandled path) and exits 1 **lets the action through**. *What the owner observes:* a firewall that quietly stops enforcing the first time its own script errors, with no signal. Structural because it's a latent fail-open on every hook the skill produces; not tagged DW only because it requires the hook to *also* error to bite.

- `minor` — **SR-7 · Hook-event roster is stale/incomplete vs the live contract.** The skill covers 8 events; the live docs document ~30 (adds `PermissionRequest`, `PostToolUseFailure`, `SubagentStart`, `PreCompact` trigger values, `PermissionDenied` with `{retry:true}`, etc.). Cheap to fix, loud when it bites (a reader looking for `PermissionRequest` won't find it), locally contained.

- `minor` — **SR-8 · Substring blocklist patterns over-block real commands and under-block obfuscation (Wow §WG-3).** `"format"`/`"rm -rf"` as substrings trip `git format-patch` and miss `rm  -fr`. A known limitation of the technique; worth an honesty note, not a redesign.

---

## Step 5, Artifact 2 — Intent-Carrying Improvement Spec

Structured for a *weaker implementing model* (skill-audit's stated reason to borrow intent-engineering): the *why* must survive so the model makes the same call on an edge the spec didn't enumerate. This skill *critiques and specs; it does not rewrite* — this is the spec, not the rewrite.

### Objective

This skill is the deterministic-enforcement layer's authoring guide: a weaker model uses it to write the fleet's real `.claude/hooks/*` and register them in `.claude/settings.json`, and the fleet then *trusts* those hooks to always block (CLAUDE.md: "Hooks enforce; subagents judge"). Today the skill can produce — and in this very repo *has coincided with* — hooks that look configured and enforce nothing: wrong stdin fields, wrong event for a blocking check, an exit code that fails open. A false sense of safety is worse than an admitted gap, because the owner stops looking. This fix makes every enforcement claim in the skill verifiably true against the live Claude Code contract, and makes the skill *force the author to prove the block fires* before trusting it. Trade-off priority for unspecified cases: **when a choice trades convenience against "the block provably fires," always choose provable enforcement** — this is a security layer, not a formatter.

### Desired outcome (owner's chair, answering (c) and (d))

- Before: the owner writes (or a weaker model writes) a `.env`-blocking hook, registers it, sees it in the directory, and a `.env` write goes through anyway with no signal. After: the skill's own drill makes the author pipe a real payload through the hook and see `exit=2` (or the JSON deny) *before* trusting it; the same drill run against a wrong-schema hook prints `exit=0` and the bug is caught at author time, not at breach time.
- Before: "exit 2 = deny" is believed everywhere. After: the author knows exit 2 only blocks on Can-Block events, knows the modern `permissionDecision:"deny"` path, and knows `exit 1` fails open for a policy hook.
- Before: the skill silently teaches the bypassable patterns the fleet already shipped. After: it names them in a "these look safe and aren't" block and tells the author to reject them in review.

### The change, per finding (each with reasoning-to-carry + edge guidance)

**Fix SR-1 (dangerously-wrong) — Pin the stdin contract as the first thing a command hook does, and make it copy-verifiable.**
Add, in the "Complete Hook Script Patterns" preamble, an explicit contract block, *quoted from* `references/hook-events.md` so the two can't drift: a PreToolUse/PostToolUse hook reads **`tool_name`** (the tool, e.g. `"Bash"`, `"Edit"` — capitalized, never `run_terminal_cmd`/`bash`) and **`tool_input`** (an object; file path at `tool_input.file_path`, Bash command at `tool_input.command`). State the failure mode inline: *"If you read `tool` or `target` instead of `tool_name`/`tool_input`, the hook silently fails open — it exits 0 and the action proceeds. This is the single most common bug in this repo's hooks."*
*Reasoning to carry:* the harm is silent fail-open in a trusted layer, so the fix is not "mention the field" — it's "make the wrong field a named, catchable error." *Edge guidance:* if a reader is porting a Cursor/other-IDE hook, tell them the *first* thing to change is every `tool`→`tool_name` and `target`→`tool_input.file_path`; do not assume field parity across IDEs. *§2.4:* check content, not presence — a version of this fix that just adds "reads the tool payload" without naming `tool_name` loses the load-bearing half.

**Fix SR-3 (dangerously-wrong) — Join the exit-code table to the per-event Can-Block reality; make it one table, not two.**
Replace the event-agnostic "Exit Code Protocol" with an event-scoped statement: exit 2 **blocks only on Can-Block=Yes events** — PreToolUse (blocks the tool), UserPromptSubmit (blocks + erases the prompt), Stop/SubagentStop (prevents stopping), PreCompact (blocks compaction), PermissionRequest (denies). On **PostToolUse it cannot block** ("the tool already ran"; stderr shown to Claude). On **SessionStart/SessionEnd/Notification it cannot block and stderr goes to the *user*, not Claude.** State the rule the author decides from: *"A blocking security check MUST live on a Can-Block event. The same script on PostToolUse enforces nothing — it can only observe and warn."*
*Reasoning to carry:* the whole point of a firewall is the deny; putting it on a non-blocking event produces a log that reads like a gate. *Edge guidance:* if the author needs to *react* to something that already happened (a bad file was written), that's a PostToolUse *cleanup/alert*, not a block — name the distinction so they don't reach for exit 2 expecting a rollback. *§6.9 (hold the objective):* this is a security skill; a sub-rule that lets "exit 2" read as universally-blocking betrays the Objective even though it "reads fine" — the event scoping wins. *Paired-change note:* the fleet's `CLAUDE.md` "Hook Exit Codes" section and Non-Negotiable Rule #4 mirror the old event-agnostic model; flag in the spec that fixing the skill without correcting CLAUDE.md leaves the wrong doctrine in standing context (this is a §2.7 mirrored-text situation — the *runtime doctrine* is duplicated across skill + CLAUDE.md).

**Fix SR-4 (dangerously-wrong) — Document the JSON output deny path as the modern PreToolUse enforcement channel, alongside exit 2.**
Add a "Structured deny (JSON output)" subsection: to deny a PreToolUse tool with a reason Claude sees, exit **0** and print `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"<why>"}}`. Note the four outcomes (`allow`/`deny`/`ask`/`defer`, precedence `deny > defer > ask > allow`) and `updatedInput` for input rewriting. State the trap: *"PreToolUse ignores a top-level `decision:\"block\"` — that shape is for PostToolUse/Stop. For PreToolUse, the decision lives inside `hookSpecificOutput`. And JSON is only read on exit 0; if you exit 2, any JSON you print is ignored."*
*Reasoning to carry:* exit 2 still works for a plain block, so present JSON as the *richer* channel, not a replacement — the author picks exit 2 for a hard stop, JSON when they need a reason-to-Claude, `ask`, or input rewriting. *Edge guidance:* if the author is unsure, exit 2 with a helpful stderr is the safe default and is fine; the JSON path is for when they specifically need one of the four outcomes or an `updatedInput`. *§5.1:* name the exact field vocabulary, not "return JSON to control it."

**Fix SR-2 (structural) — Add a registration + matcher-fires verification step to Success Criteria and to the security examples.**
After any "create the hook" instruction, require: (1) confirm the hook is registered under the *intended event* in the *active* `.claude/settings.json` (project vs `~/.claude` — name both scopes); (2) confirm the matcher would actually select the target tool. State why: *"An unregistered hook, or a hook whose matcher doesn't match, enforces nothing while looking present in the directory. In this repo, several written hooks are unregistered and dead."*
*Reasoning to carry:* the owner's #1 named disappointment is "looks configured but doesn't block"; registration + matcher-match are the two silent ways that happens. *Edge guidance:* if the hook is a fleet lifecycle helper the author *intends* to leave unwired for now, they must say so explicitly (a comment in the script), so "unregistered" is a marked decision, not an accident (§5.4 — an un-wired-on-purpose hook is *visibly* different from a forgotten one).

**Fix SR-5 (structural) — Correct the matcher description: exact-string unless it contains a regex-special char; MCP prefixes need `.*`.**
Replace "The matcher field is a regex" with: *"A matcher is an **exact string** (or `|`/`,`-separated list of exact strings) unless it contains a regex-special character, in which case it's an unanchored JavaScript regex. `Bash` matches only Bash; `Edit|Write` matches either. **A bare MCP prefix like `mcp__github` is an exact string and matches no tool — you must write `mcp__github.*`.** Wrap in `^…$` for whole-string matching."*
*Reasoning to carry:* the failure is a silently inert guard, and the skill's own `"mcp__.*"` example accidentally works, which hides the trap from a reader who drops the `.*`. *Edge guidance:* when guarding a whole MCP server, always append `.*`; when guarding one tool, the exact name is correct and needs no regex.

**Fix SR-6 (structural) — State plainly that exit 1 fails open for policy hooks; enforcement hooks must exit 2 (or JSON-deny), never 1, on their block path.**
Amend the exit-1 row and Configuration Best Practices: *"Exit 1 is a **non-blocking** error — the action proceeds. Claude Code says so explicitly: if your hook enforces a policy, use exit 2, not 1. Ensure your hook's error paths (bad input, missing dependency, unexpected exception) cannot exit 1 on what should be a block — a policy hook that errors to exit 1 silently stops enforcing."*
*Reasoning to carry:* a firewall that fails open on its own internal error is the quiet-failure class the owner fears. *Edge guidance:* for a *hard* security boundary, prefer failing *closed* — if the hook can't determine safety (can't parse input, tool unknown), consider exit 2 with a "could not verify — blocked" message rather than exit 0/1; call this out as the safer default for security (vs the current examples' `except: sys.exit(0)`).

**Fix WG-1 (structural, highest leverage) — Add a "Prove the block fires" drill to Success Criteria.**
Add a copy-paste verification the author runs before trusting any blocking hook:
```
echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | .claude/hooks/block-secrets.py; echo "exit=$?"
# expect: exit=2  (a wrong-schema hook prints exit=0 — that IS the bug)
```
Generalize: for any PreToolUse block, pipe a realistic payload matching the target and assert `exit=2` (or the `permissionDecision:"deny"` JSON). *Reasoning to carry:* the wow bar is "provably blocks"; a hook is not trusted until a real payload is denied, and this drill catches SR-1/SR-3/SR-6 at author time. *§5.2/§5.4:* operationalize the real artifact under a check; the artifact carries its own proof of enforcement.

**Fix WG-2 (structural, high leverage) — Add a "Patterns that look safe and aren't" section.**
List, with the reason each is a false sense of safety: (i) reading `tool`/`target` (fails open — SR-1); (ii) exit 1 on a block path (fails open — SR-6); (iii) an env-var opt-out like `CLAUDE_ALLOW_HIGHRISK=true` that lets *any* process disable the firewall by setting one variable (present in `require-confirm-highrisk.sh` — a firewall with a public off-switch is not a firewall for an autonomous fleet); (iv) a `prompt`-type (LLM) hook for a *security* decision — non-deterministic, the wrong tier per "Hooks enforce; subagents judge"; use `command` hooks for hard enforcement, reserve `prompt`/`agent` for advisory quality checks; (v) unregistered/unmatched hooks (SR-2/SR-5). *Reasoning to carry:* the pinned Wow explicitly asks the skill to *flag* these instead of teaching them; a security skill that models bypassable patterns as exemplars actively lowers safety. *Edge guidance:* an env-var *escalation* for a human at an interactive prompt may be acceptable; an env-var that a *scheduled/headless agent* can set to bypass is not — scope the allowance to interactive-only and say why.

**Minor fixes (listed, no full writeup per skill-audit):**
- SR-7: refresh the Hook Event Reference from the live docs (add `PermissionRequest`, `PostToolUseFailure`, `SubagentStart`, `PermissionDenied`/`{retry:true}`, `PreCompact` triggers) — or state the roster is a common subset and link the canonical docs.
- SR-8: add one honesty line that substring blocklists are advisory (over-block real commands like `git format-patch`; under-block obfuscated `rm  -fr`/`$IFS`), not a hard security boundary.

### What NOT to change (§3.5 — the confirmed-correct rows protect working design)

- **The skill's own example code (`data.get('tool_input', {}).get('file_path', '')` in Example 1 / "Complete Hook Script Patterns").** It is *already correct* against the live contract — it reads `tool_input.file_path`. Do not "align" it to the shipped hooks' wrong schema; the shipped hooks are the bug, the example is the reference. (This is why the fix is *pin the contract in prose*, not *change the examples*.)
- **`references/hook-events.md`'s field names.** It correctly lists `tool_name`, `tool_input`, and `PermissionRequest`. The SR-1 fix should *quote from it*, keeping it the single source — do not fork a second field list into SKILL.md.
- **The `settings.json` JSON block shape** shown in "Command Hooks" and the references schema (`{event:[{matcher,hooks:[{type,command,timeout,async}]}]}`) — correct and matches the live `.claude/settings.json`. Leave it; only *add* the output-control fields (SR-4) and the registration-check step (SR-2).
- **The Stop-hook loop-prevention pattern (`stop_hook_active` check).** Correct and load-bearing; keep it exactly.
- **The async-vs-sync table** (async can't deny; command-only) — correct against the contract; do not touch.
- **This skill's scope boundary** — "critiques and specs; does not rewrite the audited skill." Keep it. The improvement is delivered as this spec, not as an edited `hooks-configuration/SKILL.md`.

### Done looks like (executable criteria, §6.6)

- Grep of SKILL.md finds `tool_name` and `tool_input.file_path` stated as the required stdin fields, with the explicit "reading `tool`/`target` fails open" warning.
- The "Prove the block fires" drill is present verbatim; running it against the *current* `block-secrets.py` prints `exit=0` (demonstrating the bug the drill catches); running it against a contract-correct hook prints `exit=2`.
- SKILL.md states exit 2 is Can-Block-event-only and names PostToolUse/SessionStart as non-blocking; grep finds no un-scoped "exit 2 = deny / Action BLOCKED" claim.
- SKILL.md documents `hookSpecificOutput.permissionDecision:"deny"` and warns that top-level `decision:"block"` is ignored by PreToolUse.
- The matcher section states exact-string-unless-special-char and the `mcp__github` → `mcp__github.*` rule.
- A "Patterns that look safe and aren't" section names the five false-safety patterns with reasons.

### Band-aid tripwires (reject these in review, §6.5)

- Adding "make sure to read the right fields" *without naming `tool_name`/`tool_input.file_path`* — a paraphrase that loses the load-bearing half (SR-1 not fixed).
- Changing the skill's *example code* to match the shipped wrong-schema hooks "for consistency" — that propagates the bug into the reference.
- Fixing the skill but leaving CLAUDE.md's event-agnostic "Hook Exit Codes" doctrine — the wrong model still ships in standing context (SR-3 paired change unmet).
- Replacing exit-2 guidance *entirely* with JSON output — exit 2 is still valid for a hard block; the fix is to *add* the JSON channel, not swap.
- A "verification step" that only checks the file exists / is executable, not that a real payload gets `exit=2` — that re-creates the "looks configured" trap (WG-1/SR-2 not fixed).

### Deferrals (explicitly not in this build)

- Rewriting the 15 shipped hooks to the correct schema (`block-secrets.py` et al.) — that's a *code* fix, ticketed separately; this spec fixes the *skill* so the next hook is authored correctly and the existing bugs are catchable via the drill.
- Correcting CLAUDE.md's exit-code doctrine — flagged here as the paired change (§2.7); gated on a maintainer applying the skill fix and updating the mirrored doctrine in the same pass.
- A full 30-event reference — SR-7 can be a subset-plus-link; exhaustive coverage is optional polish.

---

### Self-application check (§6.7)

This spec proposes editing SKILL.md prose that is *mirrored* in the fleet's CLAUDE.md (the exit-code doctrine). Per §2.7 that makes SR-3 a paired cross-artifact change, and this spec says so explicitly in Fix SR-3 and the Deferrals — the implementer must learn the pairing from this document, not rediscover it. The spec does not exempt itself from the rule it invokes.

## ARTIFACT B

# Skill Audit — `hooks-configuration/SKILL.md`

## Grounding (Step 1 — pre-pinned, restated for confirmation)

- **(a) For** — This skill is for creating, configuring, and debugging Claude Code hooks that enforce security and automate quality across the fleet's *deterministic enforcement layer*: 15 scripts in `.claude/hooks/`, wired through `.claude/settings.json`. It's the how-to a session reaches for when standing up or fixing a hook.
- **(b) Feeds** — Its output is real enforcement infrastructure: actual `.claude/hooks/*` scripts, their `.claude/settings.json` registrations, and the exit-code contract (0=allow / 1=error / 2=deny). A weaker model follows this skill to write hooks the fleet depends on.
- **(c) Disappoints** — A hook that *looks* configured but doesn't actually block what you think: a bypassable firewall, an unregistered script, or a hook type/matcher/payload that doesn't fire as claimed. You trust "enforced" and it isn't.
- **(d) Wow** — Every enforcement claim is verifiably true against this repo's real hooks + settings.json; following the skill provably blocks; and it actively flags false-sense-of-safety patterns instead of teaching them.

**Existence-check performed.** I verified the skill's claims against the live `.claude/hooks/` scripts and `.claude/settings.json`. The finding that dominates this audit: the fleet's *own* registered enforcement hooks read a payload shape (`tool`, `target`, `run_terminal_cmd`) that Claude Code does not send (it sends `tool_name`, `tool_input.file_path`, `Bash`), so they `exit 0` on every real call — and the skill, which documents the *correct* shape in its reference, never teaches the debugger to catch this exact mismatch. That is precisely the "looks configured but doesn't block" disappointment, sitting live in the repo the skill is supposed to serve.

---

## Artifact 1 — Seam Report

- `dangerously-wrong` — **Step-5-equivalent gap / "Debugging a hook that is not firing" (When to Use) + the entire "Complete Hook Script Patterns" section.** The skill's stated debug use case is "Why isn't my PreToolUse hook firing?" yet the skill teaches no procedure for the failure mode that has actually silenced this repo's firewall: a **payload-key mismatch**. The live `block-secrets.py` and `require-confirm-highrisk.sh` (both registered as `PreToolUse` blockers in `settings.json`) read `hook_data.get('tool')` / `run_terminal_cmd` / lowercase `bash` — Cursor's schema — while Claude Code sends `tool_name` and `Bash` (as the skill's own `references/hook-events.md` correctly documents). Concrete failure the owner observes: they believe `.env` writes and `rm -rf` are blocked; in reality both hooks extract an empty tool name, skip their guard, and `exit 0`. The security firewall is a no-op and nothing in the skill would lead a debugger to discover it. This is the skill's purpose ("enforce security policies... always execute") contradicted by silent reality.

- `dangerously-wrong` — **"Configuration Best Practices" + "Success Criteria" (no registration-vs-disk reconciliation step).** The skill's success checklist ends at "Hook is registered in the correct scope," but never tells the model to reconcile scripts-on-disk against scripts-registered-in-settings.json. In this repo, 5 of 15 on-disk scripts are **unregistered** — including two that *look* like live safety controls: `network-access-control.sh` (domain whitelist firewall) and `cost-watchdog.py` (budget kill-switch). Concrete failure: an owner sees `network-access-control.sh` in `.claude/hooks/` and assumes egress is firewalled; it never runs, because nothing references it in `settings.json`. The skill offers no move that surfaces "present on disk, absent from settings = dead hook" — the canonical false-sense-of-safety pattern the grounding's "wow" bar demands be flagged.

- `structural` — **"Complete Hook Script Patterns" (Secret Blocker / Security Firewall).** The skill's own example patterns are *correct* (`data.get('tool_input', {}).get('file_path', '')`), but they are presented as write-from-scratch templates with **no instruction to validate the payload contract before trusting the script**. A weaker model following the pattern verbatim gets it right; a weaker model *debugging an existing wrong hook* has no cue to compare the script's keys against `references/hook-events.md`. The seam is between the reference (which holds the correct schema) and the patterns/debug guidance (which never sends the reader back to the reference to verify keys). Concrete failure: the model "fixes" a non-firing hook by adjusting the matcher or adding `chmod +x`, the real bug (wrong key) survives, and the hook still silently allows.

- `structural` — **"Exit Code Protocol" + Security Firewall pattern (no verify-it-actually-denies step).** The skill states exit 2 blocks and says "always print helpful stderr," but never instructs the reader to *prove* the deny fires — e.g. pipe a realistic Claude Code JSON payload into the script and assert it exits 2. Given that this repo shipped multiple hooks that exit 0 when they intend to exit 2, "it's registered and the code has `sys.exit(2)`" is demonstrably insufficient evidence of enforcement. Concrete failure: the model reports "firewall configured," the `sys.exit(2)` line is never reached at runtime, and no test in the skill's flow would have caught it.

- `structural` — **`require-confirm-highrisk.sh` env-gate bypass, not flagged by "security enforcement patterns."** The live high-risk hook honors `CLAUDE_ALLOW_HIGHRISK=true` to wave commands through — a legitimate escape hatch, but one that turns the "firewall" into an opt-out control an agent's own environment can set. The skill teaches enforcement patterns without teaching the reader to flag such env-var bypasses as trust-weakening. Concrete failure: an owner audits the hook, sees an exit-2 firewall, and misses that any process able to export one env var disables it — a false-sense-of-safety pattern the skill should name, not pass over. (Registration + payload bugs mean this hook doesn't fire *today* regardless; this is the bypass that would matter once the payload bug is fixed.)

- `structural` — **"Hook Types → Prompt Hooks / Agent Hooks" and the `model` default.** The skill presents prompt/agent hooks as first-class options and `hook-events.md` lists a `model` field defaulting to "haiku." Nothing in this repo's `settings.json` uses a prompt or agent hook — every registered hook is `type: command`. The skill never scopes *when* the deterministic command form is mandatory vs. when the model-judgment forms are acceptable, even though the fleet's whole premise (per CLAUDE.md rule 3: "Hooks enforce; subagents judge") is that **security enforcement must be deterministic**. Concrete failure: a weaker model, told prompt hooks are a valid choice, implements a security block as a Haiku `prompt` hook; it now enforces probabilistically (and can time out to allow), defeating the deterministic guarantee the enforcement layer exists to provide.

- `minor` — **Matcher Reference vs. real registration drift (`PostToolUse` with no matcher).** The skill's Matcher Reference implies matchers filter by `tool_name`; the repo's `log-tool-use.sh` is registered under `PostToolUse` with **no matcher** (fires on every tool). That's valid, but the skill never illustrates the empty-matcher "fires on everything" case in the PreToolUse/PostToolUse rows, so a reader may assume a matcher is always required. Observable impact: mild confusion, not breakage.

- `minor` — **`references/hook-events.md` lists events (`PermissionRequest`, `PostToolUseFailure`, `Notification`, `SubagentStart`) the SKILL.md body's event table omits.** The two surfaces disagree on the event roster. A reader working only from the body will believe fewer events exist than the reference claims. Low-stakes, but a maintainer extending the skill could duplicate or mis-order the list.

---

## Artifact 2 — Intent-Carrying Improvement Spec

**Objective.** This skill is the fleet's how-to for its deterministic enforcement layer (grounding a/b): a weaker model follows it to write and debug the `.claude/hooks/*` scripts and `settings.json` registrations the fleet trusts to block secrets, dangerous bash, and runaway cost. The failure the owner most fears (grounding c) is a hook that *looks* enforced and silently isn't — and that failure is **live in this very repo**: every registered `PreToolUse` blocker reads Cursor's payload schema (`tool`/`target`/`run_terminal_cmd`) instead of Claude Code's (`tool_name`/`tool_input`/`Bash`), so the firewall exits 0 on every real call, and five more scripts sit on disk unregistered. The skill currently cannot catch either condition. This matters because the skill's job is enforcement, and it is teaching enforcement while the enforcement it should describe does not fire.

**Desired outcome (grounding c → d).** After this fix, a model using the skill to build *or* debug a hook (1) verifies the script reads the real Claude Code payload keys before declaring it "configured"; (2) reconciles on-disk scripts against `settings.json` and flags any script present on disk but unregistered as a **dead hook, not a live control**; (3) proves the deny actually fires by feeding a realistic payload and asserting exit 2; and (4) names bypass/false-safety patterns (env-var opt-outs, prompt-hook enforcement of security) instead of shipping them. The observable difference: run the skill against this repo's firewall and it *finds* the mismatch and the dead hooks, rather than reporting "firewall configured." That is the screenshot-worthy result the owner described.

**The fix, per finding.**

- **Fix — `dangerously-wrong` (payload-key mismatch is the primary non-firing cause).** Add a **"Verify the payload contract" step** to the debug guidance (the "Why isn't my hook firing?" path) and to every enforcement pattern. It must instruct: before trusting any hook, confirm the script reads `tool_name` (not `tool`), `tool_input.file_path` / `tool_input.command` (not `target` / a bare `command`), and matches Claude Code's **capitalized** tool names (`Bash`, `Edit`, `Write` — not `bash`, `edit`, `run_terminal_cmd`), cross-checked against `references/hook-events.md`. Reasoning a weaker model needs on an unseen edge case: a hook that reads the wrong key does not error — it silently returns the default (empty string), skips its guard, and `exit 0`s, so it is *indistinguishable from a working hook by inspection of settings.json alone*. The tell is always at the key-read line, not the registration. Cursor and Claude Code hooks look nearly identical and are routinely copied between the two; assume a non-firing security hook is reading a foreign schema until the key-read line is proven correct.

- **Fix — `dangerously-wrong` (disk-vs-registration reconciliation).** Add a **required reconciliation step** to Configuration Best Practices and a checkbox to Success Criteria: enumerate `.claude/hooks/*`, enumerate every script path referenced in `settings.json`, and report any script on disk that is **not** referenced as an *unregistered / dead hook*. Reasoning for the weaker model: a script's mere existence in `.claude/hooks/` enforces nothing — only a `settings.json` entry makes it run. A file named like a firewall (`network-access-control.sh`, `cost-watchdog.py`) is the most dangerous case, because its name manufactures false confidence; call these out by name in the report, not just as a count. Never report "N hooks in `.claude/hooks/`" as if it equals "N hooks enforcing" — state registered vs. present separately.

- **Fix — `structural` (patterns must point back to the reference to self-verify).** In "Complete Hook Script Patterns," after each enforcement example, add one line: "Before relying on this, confirm the keys it reads match `references/hook-events.md` for your Claude Code version." Reasoning: the skill's example code is correct, but a maintainer debugging a *pre-existing* wrong hook needs an explicit pointer from the pattern back to the authoritative schema, or they will pattern-match on the matcher/permissions and miss the key-read bug.

- **Fix — `structural` (prove-the-deny loop).** Add a **verification step** to the Exit Code Protocol and Success Criteria: pipe a realistic Claude Code JSON payload (copy one from `references/hook-events.md`) into the hook script on the command line and assert it exits 2 for the case it should block and 0 for the case it should allow — before declaring the hook enforced. Reasoning the weaker model needs: "the code contains `sys.exit(2)`" is not evidence the line executes; this repo proves a hook can hold `sys.exit(2)` and still allow everything because control never reaches it. Runtime proof, not code inspection, is the enforcement bar.

- **Fix — `structural` (flag bypass / false-safety patterns).** Add a short **"Enforcement anti-patterns to flag, not ship"** subsection: (1) an env-var opt-out on a security hook (e.g. `CLAUDE_ALLOW_HIGHRISK=true`) means any process that can set that variable disables the control — allowed as a documented human escape hatch, but must be surfaced as a trust caveat, never treated as "enforced" unconditionally; (2) implementing a *security* block as a `prompt`/`agent` hook makes enforcement probabilistic and timeout-dependent — for security, `type: command` with a deterministic exit code is mandatory, per the fleet's "hooks enforce; subagents judge" rule. Reasoning: the grounding's "wow" bar is that the skill *flags* false-safety patterns instead of teaching them; a weaker model needs the explicit rule "deterministic command hook for anything security-relevant" or it will reach for the model-judgment forms the skill currently presents as equal options.

- **Minor findings (list only):** align the SKILL.md body event table with `references/hook-events.md` (add `PermissionRequest`, `PostToolUseFailure`, `Notification`, `SubagentStart`, or state the body table is a curated subset); add one empty-matcher "fires on every tool" example to the PreToolUse/PostToolUse matcher rows so the no-matcher registration (used by `log-tool-use.sh`) isn't surprising.

**What NOT to change.**

- **Do not touch the Exit Code Protocol table's semantics.** `0=allow / 1=error / 2=deny` is correct and matches the live hooks' intent and CLAUDE.md rule 4. Keep it; only add the verification step around it.
- **Do not rewrite `references/hook-events.md`'s payload schema.** It already documents the *correct* Claude Code keys (`tool_name`, `tool_input.file_path`, `stop_hook_active`) — it is the source of truth the fix routes readers toward. The bug is that the body and the live hooks diverge from it, not that the reference is wrong.
- **Do not change the SKILL.md example code** (`data.get('tool_input', {}).get('file_path', '')`, `jq -r '.tool_input.command'`, the `stop_hook_active` loop-prevention pattern). These are already the correct Claude Code shape and the correct loop guard; over-eagerly "aligning" them to the repo's broken live scripts would invert the fix.
- **Do not add rewrites of the audited hooks.** This skill critiques and specs (per its own scope); repairing `block-secrets.py` et al. is a separate task. Keep the skill teaching *how to catch and prevent* the mismatch, not carrying patched copies of specific fleet scripts.

## Required output

Emit exactly this format, in this order:

```
VERDICT: A
```
(or `VERDICT: B`, or `VERDICT: TIE`)

Then exactly 3 bullets of reasoning, each tied explicitly to one of the four rubric criteria above.

Then one final line: a note on whether ARTIFACT A, ARTIFACT B, both, or neither contains a self-contradiction (a stated rule that contradicts the artifact's own stated objective).
```

## Council responses

### ~anthropic/claude-sonnet-latest

VERDICT: A

- **Decidedness (rubric 1):** Artifact A pins exact field names, exact JSON shapes for the modern deny path (`hookSpecificOutput.permissionDecision`), exact matcher semantics (exact-string vs. regex-special-char trigger), and gives copy-paste executable done-criteria and "band-aid tripwires" that a weak implementer could mechanically apply. Artifact B's fixes are directionally right but stay more abstract (e.g., "confirm the keys match the reference" rather than stating the reference's content inline; no JSON-deny shape at all).

- **Breadth/evidence-discipline (rubric 3):** A explicitly fetches and quotes the live `docs.claude.com` contract (exit-2 is per-event, exit-1 fails open, matcher exact-string rule, `hookSpecificOutput` schema) and cross-checks all 15 hooks in a census table, catching that the fleet's own lifecycle hooks use the correct schema while enforcement hooks don't — a genuine "record vs. record" discovery. B's audit stays repo-internal, with no live-docs verification, and misses the matcher exact-string trap and the JSON-deny channel entirely.

- **Task-specific existence-checking (rubric 4):** A surfaces that "exit 2 = deny" is falsely taught as event-agnostic — a genuinely dangerous doctrine bug that has already propagated into CLAUDE.md — and flags it `dangerously-wrong`. B, by contrast, explicitly validates this same exit-code table as "correct" in its "what NOT to change" section, meaning it endorses a bug A found to be false against the live upstream contract. This is B's single biggest miss on the rubric's specific concern about "gaps between live upstream docs and what the repo actually implements."

Self-contradiction check: Neither artifact contains an internal rule that contradicts its own stated objective (both explicitly forbid removing exit-2 support while adding the JSON channel, and both stay within a "critique, don't rewrite" scope consistently). B's error is a factual/evidence-discipline failure (endorsing an unverified claim as correct), not a self-contradiction in the rubric's strict sense.

### openai/gpt-5.4-mini

VERDICT: A

- **Decidedness / self-consistency:** A is more actionable and more internally disciplined. It pins concrete field names, event-scoped exit behavior, matcher rules, and done-criteria, and it cleanly separates correct reference material from broken live hooks. B is more generic in its prescriptions and leaves more of the fix at the level of “verify the payload contract” without the same level of pre-made, implementable decisions.

- **Breadth / evidence-discipline:** A uses a broader and more specific evidence base: live docs, repo census, settings registration, and seam/adaptor scans. It audits additional seams like JSON deny output, event-scoped blocking, and exact-string-vs-regex matcher behavior. B does verify against the repo, but it stays narrower and does less cross-checking of upstream contract drift.

- **Task-specific depth:** A is stronger on the exact failure modes this skill must catch: bypassable firewalls, wrong-schema configs, mismatch between shipped hooks and live Claude Code payloads, and false-safety patterns the skill itself teaches. It also distinguishes blocking-capable from non-blocking events and adds proof-of-block criteria, which is the core task here. B identifies the major payload mismatch, but it is less complete on the upstream-vs-repo contract gaps and less forceful about the downstream false-safety teaching problem.

Note: ARTIFACT A contains a self-contradiction risk; ARTIFACT B does not clearly do so.

### deepseek/deepseek-v4-pro

VERDICT: A

- **Decidedness (Rubric 1):** Artifact A makes specific, pre-made decisions a weaker implementer can act on directly—exact field names (`tool_name`, `tool_input.file_path`), exact error shapes (the wrong-schema drill that prints `exit=0` instead of `exit=2`), concrete "reject in review" tripwires, and verbatim grep checks for done-criteria. Artifact B stays at the level of "verify the payload contract" and "reconcile disk vs. registration" without specifying *which* keys are wrong, what the reconciliation output should name, or what "prove the deny fires" looks like as a copy-paste command.

- **Self-consistency (Rubric 2):** Both artifacts correctly identify the central contradiction in the current skill—it documents the right schema while its shipped hooks and exit-code doctrine are wrong—and both protect that correct reference from being overwritten. Neither introduces a rule that contradicts its own stated objective. No self-contradiction in either artifact.

- **Breadth / evidence-discipline (Rubric 3):** Artifact A verifies claims against the live external Claude Code hooks documentation (not just the repo), audits seams the brief didn't name—the exact-string-vs-regex matcher fork, the `hookSpecificOutput.permissionDecision` JSON deny path, exit-code-2 being event-specific rather than global, and the exit-code-1 fail-open warning from upstream docs. Artifact B operates almost entirely from within the repo's own files and the skill's reference, missing the version-gap probe into the live platform contract that revealed the matcher trap, the modern JSON deny channel, and the upstream exit-code-1 warning.

- **Task-specific depth (Rubric 4):** Artifact A performs deeper existence-checking against the real repository: it catalogs every shipped hook with its schema verdict, identifies the *two* schema families (lifecycle hooks correct, enforcement hooks wrong), traces the exit-code doctrine propagation into CLAUDE.md as a paired-change obligation, and names the specific `CLAUDE_ALLOW_HIGHRISK` env-var bypass as a false-safety pattern the skill *teaches* by silence. Artifact B notes the same core payload mismatch and dead hooks but does not inventory all 15 hooks, does not distinguish the lifecycle/enforcement schema split, and does not identify the CLAUDE.md propagation.

**Self-contradiction note:** Neither Artifact A nor Artifact B contains a self-contradiction. Both correctly identify the skill's example code and reference as the source of truth to protect, and neither proposes changes that would undermine its own enforcement objective.

### mistralai/mistral-medium-3-5

VERDICT: A

- **Decidedness**: Artifact A provides explicit, actionable decisions (e.g., field names like `tool_name` and `tool_input.file_path`, exact verification drills, and named false-safety patterns) that a weaker implementer could directly apply. Artifact B's fixes are more procedural and less pre-decided (e.g., "add a verification step" without specifying the exact payload or assertions).
- **Self-consistency**: Artifact A explicitly aligns its fixes with its stated objective (e.g., "provably blocks" via the "Prove the block fires" drill) and avoids contradictions (e.g., it corrects the event-agnostic exit-2 claim while preserving valid use cases). Artifact B retains the unscoped `0=allow / 1=error / 2=deny` table, which clashes with its own finding that exit-2 is event-specific.
- **Breadth / evidence-discipline**: Artifact A cross-checks claims against live docs, real files, and the actual tool (e.g., the ground-truth census of hooks, live-contract facts from `docs.claude.com`), while Artifact B relies more on observed discrepancies in the repo without the same depth of external validation.

Neither artifact contains a self-contradiction.

## Cross-rankings

### Judge: ~anthropic/claude-sonnet-latest

- **Order:** B > C > A
- **Reasoning:** Response B gives the most substantive, specific comparison—citing concrete evidence from both artifacts (the census, the live-docs cross-check, the CLAUDE.md propagation, the specific env-var bypass) and correctly, consistently concludes neither artifact self-contradicts, with clear justification. Response C is similarly detailed and cites good specifics, but it undermines itself: the self-consistency bullet claims Artifact B's exit-code table 'clashes with its own finding' (implying a contradiction) yet the final line states neither artifact has a self-contradiction—an internal inconsistency in the response itself. Response A is the weakest: its reasoning is more generic/general (less tied to precise evidence) and it asserts an unspecified 'self-contradiction risk' in Artifact A without identifying what it is, which is an unsubstantiated claim that weakens its credibility.

### Judge: openai/gpt-5.4-mini

- **Order:** A > B
- **Reasoning:** Artifact A is stronger on decidedness and task-specific depth: it names exact field keys, exact JSON deny shapes, executable verification drills, and specific false-safety patterns, all of which a weaker implementer could act on directly. It also shows better breadth/evidence-discipline by checking live upstream Claude docs and cross-referencing the real repo’s hooks and settings, whereas B stays more internal and less specific about the platform contract. B is still solid, but it is comparatively abstract and less forceful on the exact seams that matter for bypassable enforcement hooks.

### Judge: deepseek/deepseek-v4-pro

- **Order:** A > C > B
- **Reasoning:** Response A is the most thorough, accurately tying each bullet to the rubric, providing precise examples (e.g., JSON deny shape, matcher rules), and offering a careful self-contradiction check. Response C is clear and correctly identifies self-consistency and evidence issues, but is less detailed than A. Response B's analysis is solid but its unsupported claim that ARTIFACT A contains a self-contradiction risk (while others find none) weakens its accuracy and overall insight.

### Judge: mistralai/mistral-medium-3-5

- **Order:** A > C > B
- **Reasoning:** Response A excels across all rubric criteria: it demonstrates superior decidedness (exact field names, JSON shapes, and executable criteria), self-consistency (no contradictions), breadth (live docs verification, matcher behavior, and version-gap probes), and task-specific depth (full repo census, CLAUDE.md propagation, and false-safety pattern identification). Response C mirrors A’s strength in breadth and depth but slightly softens the self-contradiction call, making it less precise. Response B, while directionally correct, is vaguer in its reasoning, mislabels a factual error as a self-contradiction, and omits critical details like the JSON deny path and matcher semantics.

## Chairman synthesis

_Chairman model: `~anthropic/claude-sonnet-latest`_

VERDICT: A

- **Decidedness (rubric 1):** All four council members converge that Artifact A pins concrete, copy-actionable decisions — exact field names (`tool_name`, `tool_input.file_path`), the exact JSON deny shape (`hookSpecificOutput.permissionDecision`), a literal verification drill with expected exit codes, and executable done-criteria/tripwires. Artifact B's fixes ("verify the payload contract," "reconcile disk vs. registration") name the right problems but stop short of the same pre-decided specificity — sonnet-latest, gpt-5.4-mini, deepseek-v4-pro, and mistral-medium-3-5 all independently flag this gap.

- **Breadth / evidence-discipline (rubric 3):** The decisive, repeatedly-cited differentiator is that Artifact A verifies against the **live external contract** (docs.claude.com), not just the repo — catching that exit-2 semantics are per-event (not global), that matchers are exact-string-unless-regex-special-char (so a bare `mcp__memory` matches nothing), and that a modern `permissionDecision:"deny"` channel exists that the skill omits entirely. Artifact B's audit, as sonnet-latest and deepseek-v4-pro both note, stays repo-internal and misses all three of these upstream-drift findings.

- **Task-specific existence-checking (rubric 4):** Artifact A goes further into the fleet's actual failure surface: a full 15-hook census distinguishing correctly-schemaed lifecycle hooks from wrongly-schemaed enforcement hooks (deepseek-v4-pro, sonnet-latest), the specific `CLAUDE_ALLOW_HIGHRISK` env-var bypass named as a false-safety pattern the skill teaches by omission, and — most consequentially — the observation that the skill's wrong exit-code doctrine is *mirrored in CLAUDE.md*, so fixing the skill alone leaves the bug propagating in standing context. Sonnet-latest sharpens this into the clearest single point of disagreement: Artifact B's "What NOT to change" section explicitly *endorses* the event-agnostic exit-code table as correct — a claim Artifact A demonstrates is false against the live docs. This is the one substantive place the two artifacts make opposite factual claims, and the live-docs check resolves it in A's favor.

**Points of convergence across the council (high confidence):** every ranking model puts A ahead of B, and every model independently reaches for the same three reasons — decidedness, live-contract verification, and depth of existence-checking against the real repo (hook census, registration reconciliation, false-safety patterns). This is not a narrow or contested win.

**Point of divergence (lower confidence):** gpt-5.4-mini raised an unspecified "self-contradiction risk" in Artifact A without identifying it, and mistral-medium-3-5 argued Artifact B (not A) self-contradicts by retaining an unscoped exit-code table alongside its own event-specific finding. Sonnet-latest and deepseek-v4-pro both explicitly checked and found *no* self-contradiction in either artifact, treating B's error as a factual/evidence-discipline miss rather than an internal contradiction — this is the more careful reading, since B never states within its own text that exit-2 is event-scoped, so there's no internal clash, only an unverified claim.

Self-contradiction note: Neither ARTIFACT A nor ARTIFACT B contains a genuine self-contradiction (a stated rule clashing with the artifact's own objective). Both explicitly protect their "correct" reference material from being overwritten and both add rather than replace the exit-2 channel when introducing the JSON-deny path. Artifact B's retention of the unscoped exit-code table is best characterized as an unverified/incorrect claim (it failed to check the live docs, per rubric 4) rather than an internal contradiction — it never asserts elsewhere in the same document that exit-2 is event-scoped, so nothing in B's own text clashes with itself.
