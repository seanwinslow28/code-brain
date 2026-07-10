# Fable 5 — "Week 2" Campaign Kickoff (fresh Cowork session)

**How to use:** open a fresh Cowork session and paste: *"Read and execute
`docs/plans/wwf5d/2026-07-07-fable-week2-kickoff-prompt.md` in the code-brain repo."* This file is
self-contained — you need none of the prior conversation.

---

## Who you are and what this is

You are picking up the **Fable 5 campaign** for Sean, a PM deep in agentic engineering. Fable 5 is
Anthropic's scarce, expensive flagship model. Anthropic just extended Sean's Fable access by a week
(**through 2026-07-12**) on his Claude Max plan — so there is a fresh, time-boxed window to spend it
on the irreplaceable work.

**What already exists (the campaign so far):**
- **WWF5D ("What Would Fable-5 Do")** — a portable skill (`.claude/skills/wwf5d/SKILL.md`) that
  distills Fable's *observed* cognition into abstracted recipes so cheaper models (Opus/Sonnet)
  behave more Fable-like. §1–7 are filled and it is **validation-complete**: on the Round-2 battery,
  Sean's reference-blind eye judged WWF5D-loaded Opus stronger 3/3, and a cross-family, de-biased,
  order-swapped council (`variance` profile, Sonnet excluded from the vote per F4) concurred on 2/3
  and hit a position-bias TIE on the third. **WWF5D transfers — it is now a proven, reusable tool,
  not a hypothesis.** Full record: `docs/plans/wwf5d/round2/council-results.md`, `.claude/skills/wwf5d/SKILL.md §7`.
- The campaign spine + budget logic: `docs/plans/2026-07-04-fable5-audit-campaign.md`.
- The method constraints **F1–F4**: `docs/plans/2026-07-04-wwf5d-research-findings.md`.
- The learnings log (Fable's premium / ceilings / cheap-on-Opus findings): `docs/plans/wwf5d/fable-learnings-log.md`.

**Your job this session:** help Sean **brainstorm and plan how to spend the extra Fable week** —
auditing, hardening, and improving his current projects and workflows — then produce a runnable plan.
This is a brainstorm-and-plan session first; execution (driving Fable) follows once the plan is set.

## The single most important lesson — and it scopes everything

The campaign's central finding: **Fable's premium is real and portable on the *spec / audit* end** —
spec-decidedness (pre-make every decision), **contract-contradiction detection** (a rule that fights
the artifact's own objective; a value written that nothing reads), **breadth past the seams the brief
named**, and **evidence-discipline** (verify claims against the *live system* — existence-check every
"enforced via X" before believing it). This literally found that code-brain's own security firewall
was a dead no-op. **The plain diagnosis / zoom-out loop is cheap-on-Opus** (Opus matched Fable at
near-parity twice) — do NOT spend Fable there. And **taste/voice is Sean's**, never a model's.

So every candidate target sorts into one of two lanes:

- **Lane A — Fable-only (the crown jewel):** the hardest audits + intent-carrying specs where the
  premium above is irreplaceable. Few targets, high leverage. This is what the window is *for*.
- **Lane B — WWF5D-Opus (the multiplier, now unlocked):** load `wwf5d` as Opus/Sonnet standing
  context and sweep the long tail cheaply. Validated to transfer → this is the compounding payoff,
  runs in parallel, and costs **zero Fable**. (This is the campaign's original "Phase C," now enabled.)

**The triage rule:** a target earns Lane A only if it exercises the premium (spec end, breadth,
contract-contradiction, evidence-discipline against a live system). If Opus-with-WWF5D could do it
about as well, it belongs in Lane B. Do not spend the scarce week on Lane-B work.

## The proven mechanism (reuse it exactly)

- **Paired same-day subagents from one orchestrator.** The `Agent` tool accepts `model: "fable"` and
  `model: "opus"`. Run each blind task as a fresh `model="fable"` subagent given the pinned prompt
  verbatim (it sees neither baselines nor siblings); generate the matched Opus baseline as a
  `model="opus"` subagent on the **same working-tree snapshot** (kills pin-drift). The orchestrator
  (you, Opus) holds the diff.
- **Capture-first → disk, then commit-handoff.** Save every raw Fable output to a file **before**
  distilling. Note: the **Cowork sandbox mount denies `git commit`** (no unlink/rename) — so "capture"
  = write durable files (they persist to Sean's disk) and hand Sean ready-to-paste commit commands.
- **F1** self-report is a hypothesis; only a behavioral delta earns a WWF5D entry. **F2** WWF5D holds
  abstracted recipes, never transcripts. **F3** partial transfer is the honest outcome — log ceilings.
  **F4** any validation judge is cross-family, order-swapped, length-controlled, NOT Claude-led,
  κ-gated to Sean's labels; Sean's eye is the Engine-Truth final call.
- Fold any new corroborated Fable deltas into WWF5D §1–6 + the evidence index as you go (the skill
  keeps compounding).

## Your mission: brainstorm → triage → plan the Fable Week

Sean's projects, by priority:
- **Primary:** `anima` (`/Users/seanwinslow/Code-Brain/anima`) and `code-brain`
  (`/Users/seanwinslow/Code-Brain/code-brain`, this repo — the fleet).
- **Secondary but active:** `sw-ai-pm-portfolio` (`/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio`)
  and the **Substack project** (`vault/20_projects/substack-studio/POSITIONING-AND-EDITORIAL-SPEC.md`).

Below is a **seed menu** of candidate targets to accelerate the brainstorm — not a decision. Rank
them by *leverage × only-Fable-can-do-it*, sort into Lane A / Lane B, and let the genuine
Sean-decisions surface. Add and reframe freely.

**code-brain (primary):**
- **The enforcement / hook / agent-security layer — a demonstrated hardening target.** Round 2's RT2
  audit already found code-brain's *own* security hooks are largely inert (dead-payload-key firewalls,
  5–6 unregistered scripts, a wrong-schema `permissions` block, an 83-minute timeout). A full Fable
  **evidence-discipline audit** of `.claude/hooks/` + `settings.json` + the agents-sdk security surface
  → an intent-carrying **hardening spec**. Squarely Lane A (existence-check + false-safety), high
  leverage (this is the fleet's trust layer, and it's broken).
- **The autonomous SDK agent fleet** (`agents-sdk/`) — audit the scheduled agents for seams,
  contract-contradictions, and silent-skip patterns (the vault-synthesizer / knowledge-lint
  intermittency was one; there are likely more). Lane A where it's contract-contradiction/breadth.
- **The privacy layer** (public repo + a gitignored private layer) — an evidence-discipline audit:
  does the ignore actually hold, is any real personal/employer data in tracked files, does history
  leak? (Recruiter-readiness.) Lane A — Fable existence-checks the privacy claims against the tree.
- **The 128-skill library long tail** — **Lane B**: WWF5D-Opus sweep; reserve Fable only for the
  top few most-load-bearing skills not yet elevated.

**anima (primary):**
- **An end-to-end `intended-vs-implemented` / ship-check of the 10-phase pipeline** — it's a large
  AI-built system never audited whole for contract-contradictions (the critic stack T1/T2/T3, the
  museum layer, the run orchestrator). Lane A where the premium (breadth, contract-contradiction).
- **An intent-carrying spec for the next hard seam** — e.g. the Outward Turn (multi-character /
  multi-style routing beyond the register-seam), or the museum publish gate. Lane A (spec-decidedness).
- Note: the register-seam Phase-C *implementation* is Opus work, not Fable.

**sw-ai-pm-portfolio (secondary):**
- **A ship-check / static security + performance audit of the live recruiter-facing site** (AI-built;
  hardening matters before more recruiters see it). The `pm-ai-shipping` skills fit exactly.
- **The daily-dated "honesty layer"** (Daily Driver → portfolio-refresh) — an evidence-discipline
  audit: the "real and dated / unfakeable" claim is load-bearing; can it fabricate or silently stale?
  Lane A.
- The explainer-graphics enhancement spec (Round 2 RT3) → Opus implementation (Lane B).

**Substack project (secondary):**
- **Audit `POSITIONING-AND-EDITORIAL-SPEC.md` for internal contract-contradictions + intent-preservation
  across the idea→published workflow** — the creative-*chain* seam audit shape (like Round-1 BT3), on
  the positioning/editorial *system* and its pipeline seams. Lane A — Fable audits the spec's
  self-consistency and the handoffs. **NOT** a Fable target: writing the actual posts (voice/taste is
  Sean's — that's the whole point of the voiceprint chain).

## Context files — read these first, in this order

1. `CLAUDE.md` (code-brain root) — repo rules (privacy layer, hooks, domains). Also skim
   `anima/CLAUDE.md` and `sw-ai-pm-portfolio/CLAUDE.md` for those projects' shapes.
2. `docs/plans/wwf5d/fable-learnings-log.md` — the premium / ceiling / cheap-on-Opus findings.
3. `docs/plans/2026-07-04-fable5-audit-campaign.md` — the campaign spine + budget logic + the
   funnel/triage doctrine.
4. `.claude/skills/wwf5d/SKILL.md` — the validated skill; **§7** = the transfer map (what ported,
   what's cheap-on-Opus, what's Sean's) — this *is* the scoping instrument.
5. `docs/plans/2026-07-04-wwf5d-research-findings.md` — F1–F4.
6. `docs/plans/wwf5d/round2/` — the Round-2 exemplars to mirror: `round2-task-battery.md` +
   `round2-session-driver.md` (the runnable format), the `rt{1,2,3}-diff.md` (what a good diff looks
   like), `council-results.md` (how validation is judged + reported).
7. `docs/architecture/fleet-ops-protocol.md` (in the **anima** repo) — the standing discipline for any
   costed/multi-step run.

## Skills to use (Cowork)

- **`superpowers:brainstorming`** — scope + triage the week (the regroup trigger mandates it). Use it
  to sort the seed menu into Lane A / Lane B and rank.
- **`superpowers:writing-plans`** — turn the scope into a **Fable-Week task battery + session driver**
  (mirror `docs/plans/wwf5d/round2/round2-task-battery.md` + `round2-session-driver.md`: pinned inputs,
  self-contained per-arm run-prompts, blind-run discipline, capture-first).
- **`wwf5d`** — **load it.** It is both the map of where Fable's premium lives (so you triage right)
  and the standing context that makes all the Lane-B Opus work Fable-like.
- **`honest-thinking-partner`** and/or **`grilling`** — pressure-test the triage *before* committing
  Fable to it (is each Lane-A target really only-Fable, or is it cheap-on-Opus in disguise?).
- The audit/spec **harnesses**: `skill-audit`, `zoom-out-and-think`, `intent-engineering`,
  `systematic-debugging`, and the **`pm-ai-shipping`** suite (`ship-check`, `security-audit-static`,
  `performance-audit-static`, `document-app`, `intended-vs-implemented`, `derive-tests`) — the last is
  a strong fit for auditing/hardening the AI-built apps (anima, portfolio, the fleet).
- Cowork manages the task list and uses `AskUserQuestion` for the genuinely-Sean decisions (which
  projects/targets to prioritize, the week's Lane-A budget, risk appetite, go/no-go before each Fable
  spend).

## Guardrails (carry all of these)

- **F1–F4** as above (the method's spine).
- **Triage discipline:** every Fable (Lane-A) target must exercise the premium; route everything else
  to Lane B (WWF5D-Opus). Do not spend the week on cheap-on-Opus or taste work.
- **Fleet-ops (for any costed/multi-step run):** bill the **subscription/OAuth, never
  `ANTHROPIC_API_KEY`**; one isolated worktree per plan; single owner; clean teardown. (anima's
  `docs/architecture/fleet-ops-protocol.md`.)
- **Privacy layer (code-brain):** never `git add` the private-layer paths; never write real
  income/medical/contact/employer data into tracked files; `writing-voice-modes` / `personal-finance`
  / `life-admin` edit the **public `SKILL.md` only**. Verify before any commit touching those.
- **Capture-first, commit-handoff:** write raw Fable output to durable files before distilling; hand
  Sean ready-to-paste commit commands (the Cowork sandbox can't `git commit`, and a failed attempt can
  leave a stale `.git/index.lock` — tell Sean to `rm -f .git/index.lock` first).
- **Ground-first:** no cold Fable kickoffs — pin inputs + grounding before any Fable subagent runs.
- **Window awareness:** Fable is gone after ~2026-07-12. This is a **triage funnel, not a sweep** —
  a few high-leverage Lane-A burns + a broad Lane-B WWF5D-Opus sweep.

## First actions for the fresh session

1. Read the context files (order above); set up a task list for the session.
2. Invoke **`superpowers:brainstorming`**: sort the seed menu (+ your own additions) into Lane A /
   Lane B, ranked by leverage × only-Fable. Keep it tight — the inputs are rich.
3. Surface the genuine Sean-decisions with `AskUserQuestion`: which projects/targets make the Lane-A
   cut, how to split the week, risk appetite. (Optionally `grill` the Lane-A shortlist first — is each
   really irreplaceable-by-Opus?)
4. On his picks, move to **`superpowers:writing-plans`** → the Fable-Week task battery + driver under
   `docs/plans/wwf5d/week2/` (or similar). Then, on his go, drive Lane A on Fable (paired subagents,
   capture-first) and kick off the Lane-B WWF5D-Opus sweep in parallel.

## Deliverable of this session

A prioritized **Fable-Week plan**: the **Lane-A Fable battery** (targets, order, pinned inputs +
self-contained paired-run prompts, durable outputs — hardening specs, root-cause decision-docs,
intent-carrying specs, and more WWF5D corroboration) **plus** the **Lane-B WWF5D-Opus sweep** (the
long tail to run in parallel at zero Fable cost) — saved as a task battery + session driver mirroring
the Round-2 artifacts, ready to execute.

## Out of scope this session

- Writing the plan is the goal — don't burn Fable on execution until the plan is set and Sean approves.
- Taste/voice work (Substack post-writing, portfolio copy) is not a Fable target — that's Sean's, via
  the voiceprint/writing chain.
- The Round-2 implementation specs (preserve-session fix, explainer-graphics enhancement) are Opus
  implementation work, not Fable — schedule them as Lane-B/Phase-C, not Lane-A.
