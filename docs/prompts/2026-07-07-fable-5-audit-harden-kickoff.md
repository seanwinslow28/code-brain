# Kickoff — Fable 5 Audit / Harden / Improve Week (through July 12)

**How to use:** Start a fresh Cowork session, **switch the model to Fable 5**, then paste everything below the line. It's self-contained — it assumes no prior conversation.

---

I have Fable 5 access through **July 12** (a bonus week Anthropic added to Claude Max). I want to spend it on the work Fable 5 is uniquely good at. I already distilled *what* that is into a skill called **`wwf5d`** ("What Would Fable-5 Do") — grounding, seam-catching, root-cause, dangerously-wrong/structural/minor triage, and intent-preserving specs. Read it first: it's both your operating manual for this session AND the map of where to point Fable 5 this week.

`wwf5d` skill: `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/wwf5d/SKILL.md`

**Your job this session:** brainstorm the highest-leverage ways to use Fable 5 to **audit, harden, and improve** my projects and workflows, then converge to a **prioritized, ranked plan**. **Stop at the plan — do not start executing audits.** I'll review and greenlight the top items into their own sessions afterward.

## The projects (in priority order)

1. **anima** — `/Users/seanwinslow/Code-Brain/anima` — a 10-phase 2D-animation pipeline with a named agent fleet (Maya/Cy/Sam/Bea/Flo/Em/Mo/T3) and a T1/T2/T3 critic stack. *Primary target.* Grounding: `CLAUDE.md`, `PHILOSOPHY.md`, `ROADMAP.md`, `docs/architecture/pipeline-architecture-v1.md`.
2. **code-brain** — `/Users/seanwinslow/Code-Brain/code-brain` — my personal command center: skills, hooks, and an autonomous Agent-SDK fleet on launchd schedules. *Primary target.* Grounding: `CLAUDE.md`, `CHANGELOG.md`, `vault/00_inbox/tickets.md`.
3. **sw-ai-pm-portfolio** — `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio` — the live Astro portfolio. *Secondary.* Grounding: `CLAUDE.md`, `docs/specs/PORTFOLIO-MASTER-PLAN.md`.
4. **Substack (Pencil & Prompt)** — `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/POSITIONING-AND-EDITORIAL-SPEC.md` (+ `SOUL.md`). *Secondary.*

Weight anima and code-brain heavily. Portfolio and Substack still matter — surface their best Fable-5 uses, but don't let them crowd the mains.

## Skills to use, and when

**Thinking spine (run these to structure the reasoning):**
- **`superpowers:brainstorming`** — the process spine. Generate breadth before converging; pressure-test intent. Invoke this before proposing anything.
- **`honest-thinking-partner`** — run the brainstorm through this so it surfaces blind spots and forces concrete action. This is an audit/harden session, not a validation session. Push back on me.
- **`wwf5d`** — standing context throughout. Use its section map as the menu of Fable's edge: §2 seam/handoff audits, §3 root-cause, §4 triage, §6 intent-preserving specs. When you propose a use case, name which wwf5d move it exploits.

**Audit instruments (name them in the plan; don't run them yet):**
- **`pm-ai-shipping:intended-vs-implemented`** — the gap between documented intent and actual code. The formal version of wwf5d seam-catching; tailor-made for anima and code-brain.
- **`pm-ai-shipping:ship-check`** — reviewer-ready hardening pass (docs → security → performance → test-map).
- **`grilling`** — stress-test the *plan itself* before I commit Fable-week to it.
- **`superpowers:writing-plans`** — turn the converged picks into executable specs (pair with wwf5d §6).

**For the Substack thread only, if it earns a slot:** `voiceprint:writing-critique` + `substack-value-engine`.

## The flow (interactive — check in with me at the gates)

1. **Ground first (wwf5d §1).** Read `wwf5d`, then the grounding docs for the two primary projects. Don't characterize a system from its docs alone where you can inspect its live/measured state (schedules, logs, tests, the actual pipeline/critic wiring). Report what you grounded in before proposing.
2. **Diverge.** With `superpowers:brainstorming` + `honest-thinking-partner`, generate candidate Fable-5 use cases across **audit / harden / improve**, project by project. For each: the target seam or failure class, which wwf5d move it uses, and why Fable specifically (vs. Opus/Sonnet — be honest where Opus is at parity; wwf5d §7 says the diagnosis loop is cheap-on-Opus, so favor the seam/contract-contradiction/evidence-discipline/spec moves where Fable's edge is real).
3. **Converge + triage.** Rank the candidates. Use wwf5d §4 (dangerously-wrong first) **and** value × effort × "is this genuinely a Fable job." Pause here and show me the ranked menu before going further.
4. **Stress-test.** Run the top picks through `grilling`. Kill the ones that don't survive.
5. **Plan.** With `superpowers:writing-plans` + wwf5d §6, write executable specs for the **top 1–3** so each is ready to hand to its own session. Then **stop.**

## Guardrails

- **Honesty over completeness.** Mark every claim observed / documented / assumed (wwf5d §1.4). No fabricated findings, no asserting an unverified failure as fact. If Fable's edge doesn't apply to something, say so.
- **Capture deferred work as tickets.** Any follow-up that won't finish this session → a one-line bullet under `## Todo` in `/Users/seanwinslow/Code-Brain/code-brain/vault/00_inbox/tickets.md` before wrapping (per code-brain's CLAUDE.md rule 8).
- **Deliverables:** (a) the ranked use-case menu, and (b) plan/spec docs for the top 1–3. Save cross-cutting plans under `code-brain/docs/plans/` (`YYYY-MM-DD-slug.md`); project-specific plans co-located in that project.
- Start by asking me any scoping question that would change the ranking — otherwise ground and go.
