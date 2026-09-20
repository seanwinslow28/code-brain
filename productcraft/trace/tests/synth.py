#!/usr/bin/env python3
"""Build the synthetic "Callboard" engagement folder the trace kit is tested on.

Everything here is invented. pc-eng-000 "Callboard" is a fictional casting
tool for community theatre (the same invention #292's sample used); no seat
wrote any of it, no book was read for it, no ledger entry is real. The
builder *simulates* the train: it walks the passes in order, hashes each
pass's inputs from the folder as it stands at that moment, then applies the
pass's writes (a repair overwrites its artifact in place, as #274 rules), so
the hash chain in the records is real and the checker can be exercised on
superseded revisions, blind pairs and bounce loops.

Run from productcraft/trace/:  python3 tests/synth.py <out-dir>
It refuses to write anywhere under a `ledger/` path.

Used by tests (into tmp_path) and to regenerate samples/synthetic-engagement/.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ENG_ID = "pc-eng-000"
ENG_SLUG = "pc-eng-000-callboard"
OPUS, SONNET = "claude-opus-5", "claude-sonnet-5"
CODEX = "codex gpt-5.6-sol high"
AGENT = "Agent tool, fresh context"
CODEX_LAUNCH = "codex exec --model gpt-5.6-sol -c reasoning.effort=high"
WITHHELD = ["the drafting conversation", "ledger entries of other engagements"]
PROTOCOL = "templates/red-team-protocol.md"

# --------------------------------------------------------------------------- #
# invented artifact bodies — short, id-bearing, no book text
# --------------------------------------------------------------------------- #


def header(aid: str, seat: str, stage: int, grounding: str, revision: int, stale_from: str | None,
           status: str, extra: str = "") -> str:
    return (
        "---\n"
        f"id: {aid}\nengagement: {ENG_SLUG}\ndate: 2026-10-06\nseat: {seat}\nstage: {stage}\n"
        f"model: {OPUS if seat in ('product-strategist', 'discovery-lead', 'insights-analytics', 'product-leadership') else SONNET}\n"
        f"grounding: {grounding}\nthin_lane: []\nadjacent_lanes: []\nrevision: {revision}\n"
        f"stale_from: {stale_from or 'null'}\nstatus: {status}\n{extra}---\n\n"
    )


STRATEGY_R1 = header(f"{ENG_ID}.strategy", "product-strategist", 1, "full", 1, None, "draft") + """# Strategy & POV — Callboard

## Diagnosis

Community theatres lose two rehearsal weeks a season to the casting scramble: callbacks are scheduled by email threads nobody owns.

## Guiding policy

- GP-1 — the tool owns the rehearsal calendar and proposes callback slots directors accept.

## Strategic bets

- B1 — directors will accept a proposed slot over running their own thread. Dies if fewer than half accept in the pilot.
- B2 — the callback scramble is the costliest step, not auditions. Dies if interviews rank it lower.
- B3 — venues will share availability. Dies if no venue does by week four.

## Outcomes

- OC-1 — casting completes faster.
- OC-2 — directors return for a second production.
- OC-3 — the regional association recommends the tool.

## Channels considered

- C1 — direct outreach to directors
- C2 — regional theatre associations
- C3 — drama-teacher newsletters
- C4 — app stores

## Actions

- Action 1 — calendar proposal flow. Action 2 — callback notices. Action 3 — cast list export. Action 4 — venue integration.

## Evidence this rests on

- corpus/strategy/good-strategy-bad-strategy.md (shelf label read; kernel: diagnosis, guiding policy, coherent action)

## Moves

origin draft, no upstream — leaned on: Rumelt's kernel; the brief §2

meter: claude-opus-5 · 182400 in · 21300 out · 34 min
"""

STRATEGY_R2 = header(f"{ENG_ID}.strategy", "product-strategist", 1, "full", 2, "pass-02", "final") + """# Strategy & POV — Callboard

## Diagnosis

Community theatres lose two rehearsal weeks a season to the casting scramble: callbacks are scheduled by email threads nobody owns.

## Guiding policy

- GP-a — directors own the calendar; the tool proposes callback slots into it.
- GP-b — where a venue shares availability, the tool proposes and the director accepts.

## Assumption register

- A1 — directors control the rehearsal calendar (testable in the pilot).
- A2 — venues will share availability on request.

## Strategic bets

- B1 — directors will accept a proposed slot over running their own thread. Dies if fewer than half accept in the pilot.
- B2 — the callback scramble is the costliest step, not auditions. Dies if interviews rank it lower.
- B3 — venues will share availability. Dies if no venue does by week four.

## Outcomes

- OC-1 — casting completes faster.
- OC-2 — directors return for a second production.
- OC-3 — the regional association recommends the tool.

## Channels considered

- C1 — direct outreach to directors
- C2 — regional theatre associations
- C3 — drama-teacher newsletters
- C4 — app stores

## Actions

- Action 1 — calendar proposal flow. Action 2 — callback notices. Action 3 — cast list export.

## Evidence this rests on

- corpus/strategy/good-strategy-bad-strategy.md (shelf label read; kernel: diagnosis, guiding policy, coherent action)

## Moves

- kept — B1–B3 from pc-eng-000.strategy revision 1
- split — GP-1 → GP-a, GP-b from pc-eng-000.strategy revision 1
- added — A1–A2 from audits/gate-1-r1.md finding 1
- dropped — Action 4 from pc-eng-000.strategy revision 1; no source survived the split

meter: claude-opus-5 · 96700 in · 9900 out · 18 min
"""

GATE_1_R1 = """---
id: pc-eng-000.gate-1
engagement: pc-eng-000-callboard
seat: red-team-gate
gate: strategy-sign-off
anchor: pc-eng-000.strategy
anchor_revision: 1
vendor: codex gpt-5.6-sol high
verdict: STRATEGY FAIL — QUALITY VERDICT ONLY
---

## Findings

| # | Severity | Finding |
|---|---|---|
| 1 | CRITICAL | GP-1 rests on an unstated assumption that directors control the rehearsal calendar. |
| 2 | NOTE | B1–B3 hold; the register should say what each dies if. |
| 3 | NOTE | Action 4 has no source in the diagnosis. |

meter: codex gpt-5.6-sol high · 61200 in · 4800 out · 9 min
"""

GATE_1_R2 = GATE_1_R1.replace("anchor_revision: 1", "anchor_revision: 2").replace(
    "STRATEGY FAIL", "STRATEGY PASS").replace(
    "| 1 | CRITICAL | GP-1 rests on an unstated assumption that directors control the rehearsal calendar. |",
    "| 1 | NOTE | GP-a and GP-b make the calendar assumption explicit (A1). Holds. |")

EVIDENCE = """# Interviews 01–08 (synthetic)

Eight invented director interviews. No real participant exists. Transcript pointers below are fictional.

- Interview 1 — scheduled callbacks by email; lost a week.
- Interview 2 — used a shared spreadsheet; four no-shows.
- Interview 3 — "the callback scramble" is the phrase used.
- Interview 4 — venue never replied about availability.
- Interview 5 — ran auditions in one evening; callbacks took two weeks.
- Interview 6 — same phrase, unprompted.
- Interview 7 — would not pay per production.
- Interview 8 — regional association newsletter is how they hear about tools.
"""


def discovery(rev: int) -> str:
    stale = "pass-07" if rev == 2 else None
    status = "co-signed" if rev == 2 else "draft"
    e2 = "" if rev == 2 else "| E2 | directors want fewer emails | O2 | interviews (summary) | | \n"
    e4 = ("| E4 | four of eight lost a week to callbacks | O1 | evidence/interviews-01-08.md 2, 3, 5, 8 | |\n" if rev == 2
          else "| E4 | six of eight lost a week to callbacks | O1 | interviews | |\n")
    moves = (
        "- kept — O1–O4 from pc-eng-000.discovery revision 1\n"
        "- dropped — E2 from pc-eng-000.discovery revision 1; no unprompted source\n"
        "- added — E4 restated at four of eight from audits/cosign-discovery-r1.md\n"
        if rev == 2 else
        "- kept — B1 from pc-eng-000.strategy\n"
        "- kept — B3 from pc-eng-000.strategy\n"
        "- split — B2 → O2, O3 from pc-eng-000.strategy\n"
        "- added — O1, O4 from evidence/interviews-01-08.md\n"
        "- added — E1–E5 from evidence/interviews-01-08.md\n"
    )
    return header(f"{ENG_ID}.discovery", "discovery-lead", 2, "full", rev, stale, status,
                  "cosign: pending\nauditor: product-leadership\naudit: pending\n") + f"""# Discovery packet — Callboard

## Part 1 — Plan

Eight director interviews, past-behavior questions only (corpus/discovery/the-mom-test.md read).

## Part 2 — Opportunity solution tree

- O1 — casting takes two weeks (from interviews 1, 2, 5)
- O2 — the callback scramble: nobody owns the thread (from interviews 3, 6)
- O3 — auditions are not the bottleneck (from interview 5)
- O4 — venues do not answer availability requests (from interview 4)

## Part 3 — Evidence

| Claim | Statement | Under | Source | Grade (Insights) |
|---|---|---|---|---|
| E1 | callbacks are scheduled by email threads | O2 | evidence/interviews-01-08.md 1, 3, 6 | |
{e2}| E3 | the phrase "callback scramble" came up unprompted | O2 | evidence/interviews-01-08.md 3, 6 | |
{e4}| E5 | directors hear of tools via the association | — | evidence/interviews-01-08.md 8 | |

## Moves

{moves}
meter: claude-opus-5 · 240100 in · 28700 out · 41 min
"""


COSIGN_R1 = """---
id: pc-eng-000.cosign-discovery
engagement: pc-eng-000-callboard
seat: insights-analytics
kind: cosign
stage: 2
checked: pc-eng-000.discovery
checked_revision: 1
verdict: CO-SIGN BOUNCE — 2 claims
---

## Claims

Claims checked: E1–E5 under O1–O4.

| # | Claim | Grade | Verdict |
|---|---|---|---|
| E1 | email threads | reported-behavior | pass |
| E2 | fewer emails | stated-preference | bounce — no interviewee said it unprompted |
| E3 | the phrase | reported-behavior | pass |
| E4 | six of eight | inferred | bounce — transcripts show four |
| E5 | association | reported-behavior | pass |

meter: claude-opus-5 · 131400 in · 6200 out · 14 min
"""

COSIGN_R2 = COSIGN_R1.replace("checked_revision: 1", "checked_revision: 2").replace(
    "CO-SIGN BOUNCE — 2 claims", "CO-SIGN PASS").replace(
    "| E2 | fewer emails | stated-preference | bounce — no interviewee said it unprompted |\n", "").replace(
    "| E4 | six of eight | inferred | bounce — transcripts show four |", "| E4 | four of eight | reported-behavior | pass |")

INSIGHTS = header(f"{ENG_ID}.insights", "insights-analytics", 3, "full", 1, None, "final",
                  "auditor: delivery-execution\naudit: pending\n") + """# Metrics & evidence plan — Callboard

## Outcome-to-metric table

| Outcome | Metric | Instrumentation |
|---|---|---|
| OC-1a — time to cast | M1 median days audition → cast list | event: cast_list_exported |
| OC-1b — callback no-shows | M2 no-show share per callback | event: callback_attended |
| OC-2 — directors return | M3 second-production rate at 12 months | account: productions |
| OC-2 — directors return | M4 slot acceptance rate | event: slot_accepted |

OC-3 is bounced to the Strategist as unmeasurable by this plan (corpus/insights/trustworthy-online-experiments.md read: no metric without an instrument).

## Moves

- split — OC-1 → OC-1a, OC-1b from pc-eng-000.strategy
- kept — OC-2 from pc-eng-000.strategy
- added — M1–M4 from OC-1a, OC-1b, OC-2
- dropped — OC-3 from pc-eng-000.strategy; unmeasurable, bounced to the Strategist

meter: claude-opus-5 · 176500 in · 19800 out · 29 min
"""

GROWTH = header(f"{ENG_ID}.growth", "growth-distribution", 4, "manifest-only", 1, None, "final",
                "auditor: insights-analytics\naudit: pending\n") + """# Growth model & GTM — Callboard

## Loops

- L1 — director invites the cast; cast members become next season's directors. Target: 30 invites per production. price_source: hypothesis

## Channels

- C1 — direct outreach to directors (kept)
- C2 — regional theatre associations, folded together with the drama-teacher newsletters they run

## Moves

- kept — C1 from pc-eng-000.strategy
- merged — C2 + C3 → C2 from pc-eng-000.strategy
- kept — C4 from pc-eng-000.strategy
- added — L1 from OC-2

meter: claude-sonnet-5 · 151200 in · 17400 out · 22 min
"""

BUSINESS = header(f"{ENG_ID}.business", "business-economics", 5, "full", 1, None, "final",
                  "auditor: growth-distribution\naudit: pending\n") + """# Business case — Callboard

## Pricing hypotheses

- PH-1 — per production. PH-2 — per season. Interview 7 rules out per-production for the smallest theatres (corpus/business/monetizing-innovation.md read).

## Unit economics

Three scenarios; arithmetic stated so a gate can redo it. C4 dropped: app-store review and fees exceed a season's revenue for the median theatre.

## Moves

- kept — L1 from pc-eng-000.growth
- kept — C1 from pc-eng-000.growth
- kept — C2 from pc-eng-000.growth
- added — PH-1, PH-2 from E1, C2
- dropped — C4 from pc-eng-000.growth; gatekeeper cost exceeds season revenue

meter: claude-sonnet-5 · 163000 in · 18900 out · 26 min
"""

ROADMAP = header(f"{ENG_ID}.roadmap", "delivery-execution", 6, "full", 1, None, "final",
                 "cosign: pending\nauditor: business-economics\naudit: pending\nhandoff_verdict: brief\n") + """# Outcome roadmap — Callboard

## OKR translation

- KR-1 — median time-to-cast under 7 days (from OC-1a, M1)
- KR-2 — share of productions cast within a week above 60% (from OC-1a, M2)
- KR-3 — second-production rate above 40% (from OC-2)

## Bets with appetites

- B1 — six weeks, circuit breaker at week four. B2 — three weeks. B3 — two weeks.

## First shipping slice

Calendar proposal flow with a Systemcraft-owned scheduling layer: handoff brief follows (corpus/delivery/shape-up.md read).

## Moves

- split — OC-1a → KR-1, KR-2 from pc-eng-000.insights
- added — KR-3 from OC-2
- kept — B1–B3 from pc-eng-000.strategy
- added — appetites from PH-1, L1, O2

meter: claude-sonnet-5 · 198700 in · 24200 out · 31 min
"""

TRIAL = ROADMAP.replace("status: final", "status: draft").replace(
    "- split — OC-1a → KR-1, KR-2 from pc-eng-000.insights\n- added — KR-3 from OC-2\n- kept — B1–B3 from pc-eng-000.strategy\n- added — appetites from PH-1, L1, O2\n",
    "- split — OC-1a → KR-1, KR-2 from pc-eng-000.insights\n- merged — B2 + B3 → B2 from pc-eng-000.strategy\n- kept — B1 from pc-eng-000.strategy\n- added — appetites from PH-1, L1\n",
).replace("meter: claude-sonnet-5 · 198700 in · 24200 out · 31 min", "meter: codex gpt-5.6-sol high · 171900 in · 22800 out · 24 min")

HANDOFF = """---
id: pc-eng-000.handoff
engagement: pc-eng-000-callboard
seat: delivery-execution
stage: 6
return_due: 2026-10-20
---

# Handoff brief — Callboard

Ask Q1: design the scheduling layer behind the calendar proposal flow. References: pc-eng-000.strategy, .discovery, .insights, .growth, .business, .roadmap (frozen copies travel beside this brief).
"""

LEADERSHIP = header(f"{ENG_ID}.leadership", "product-leadership", 7, "manifest-only", 1, None, "final",
                    "auditor: product-strategist\naudit: pending\n") + """# Leadership packet — Callboard

## Part 1 — Stakeholder map

| Party | Hat | Can |
|---|---|---|
| Sean | decider · builder · funder | block, fund |
| venue managers | — | block (availability) |
| regional association (C2) | judge | recommend |
| app-store review (C4) | gatekeeper | block release |

## Part 3 — Operating-model doc

Team topology: two agents as their own entity type, each row pointing at its invocation record. Return date for the scheduling layer: 2026-10-20 (from the handoff brief).

## Moves

- kept — KR-1, KR-2, KR-3 from pc-eng-000.roadmap
- added — stakeholder rows from C2, C4, E5
- added — team topology from B1–B3

meter: claude-opus-5 · 205300 in · 26100 out · 33 min
"""


def audit(slug: str, seat: str, stage: int, checked: str, verdict: str, body: str) -> str:
    return f"""---
id: {ENG_ID}.audit-{slug}
engagement: {ENG_SLUG}
seat: {seat}
kind: audit
stage: {stage}
checked: {checked}
verdict: {verdict}
---

## Verdict line

{verdict}

## Findings

{body}

meter: claude-opus-5 · 120000 in · 5000 out · 12 min
"""


def entry(n: int, seat: str, artifact: str, decision: str, canon: str, corpus_path: str | None) -> str:
    canon_line = f"{canon} — the idea in the seat's words." + (f" Read at {corpus_path}." if corpus_path else "")
    return f"""---
id: {ENG_ID}.d{n:02d}
engagement: {ENG_SLUG}
date: 2026-10-06
seat: {seat}
artifact: {artifact}
grounding: full
status: decided
ratified: null
canon: [{canon.lower().replace(' ', '-')}]
---

## Decision

{decision}

## From the canon

{canon_line}
"""


# --------------------------------------------------------------------------- #
# the train, in order — each pass: metadata, inputs (paths), writes (path → text)
# --------------------------------------------------------------------------- #

CORPUS = {
    "corpus/strategy/shelf.md": "strategy",
    "corpus/strategy/good-strategy-bad-strategy.md": "strategy",
    "corpus/discovery/shelf.md": "discovery",
    "corpus/discovery/continuous-discovery-habits.md": "discovery",
    "corpus/discovery/the-mom-test.md": "discovery",
    "corpus/insights/shelf.md": "insights",
    "corpus/insights/trustworthy-online-experiments.md": "insights",
    "corpus/growth/shelf.md": "growth",
    "corpus/business/shelf.md": "business",
    "corpus/business/monetizing-innovation.md": "business",
    "corpus/delivery/shelf.md": "delivery",
    "corpus/delivery/shape-up.md": "delivery",
    "corpus/leadership/shelf.md": "leadership",
}

SIX = ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md", "artifacts/metrics-evidence-plan.md",
       "artifacts/growth-gtm.md", "artifacts/business-case.md", "artifacts/outcome-roadmap.md"]


def P(seat, kind, stage, runtime, launch, minutes, meter, meter_source, inputs, outputs, writes, corpus_read,
      notes, triggered_by=None, shadow_of=None, withheld=None, same_inputs_as=None, launched="08:12"):
    return dict(seat=seat, kind=kind, stage=stage, runtime=runtime, launch=launch, minutes=minutes, meter=meter,
                meter_source=meter_source, inputs=inputs, outputs=outputs, writes=writes, corpus_read=corpus_read,
                notes=notes, triggered_by=triggered_by, shadow_of=shadow_of, withheld=withheld or WITHHELD,
                same_inputs_as=same_inputs_as, launched=launched)


def passes() -> list[dict]:
    return [
        P("product-strategist", "draft", 1, OPUS, AGENT, 34, (182400, 21300, 96000), "Agent-tool usage",
          ["brief.md", "corpus/strategy/shelf.md", "corpus/strategy/good-strategy-bad-strategy.md"],
          ["artifacts/strategy-pov.md", f"{ENG_ID}.d01", f"{ENG_ID}.d02"],
          {"artifacts/strategy-pov.md": STRATEGY_R1,
           "d01-casting-bottleneck-diagnosis.md": entry(1, "product-strategist", "artifacts/strategy-pov.md", "The diagnosis is the callback scramble, not auditions.", "Good Strategy Bad Strategy", "corpus/strategy/good-strategy-bad-strategy.md"),
           "d02-guiding-policy-choice.md": entry(2, "product-strategist", "artifacts/strategy-pov.md", "One guiding policy chosen over two candidates.", "Good Strategy Bad Strategy", None)},
          ["corpus/strategy/good-strategy-bad-strategy.md", "corpus/strategy/shelf.md", "brief.md"],
          "Origin draft. Named the casting bottleneck as the diagnosis; two candidate guiding policies drafted, one chosen.",
          launched="08:12"),
        P("red-team-gate", "gate", 1, CODEX, CODEX_LAUNCH, 9, (61200, 4800, 0), "codex footer",
          ["artifacts/strategy-pov.md", PROTOCOL], ["audits/gate-1-r1.md"], {"audits/gate-1-r1.md": GATE_1_R1}, [],
          "Gate FAIL: guiding policy rests on an unstated assumption that directors control the rehearsal calendar.",
          withheld=WITHHELD + ["the corpus"], launched="08:51"),
        P("product-strategist", "repair", 1, OPUS, AGENT, 18, (96700, 9900, 88000), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "audits/gate-1-r1.md", "corpus/strategy/good-strategy-bad-strategy.md"],
          ["artifacts/strategy-pov.md", f"{ENG_ID}.d03"],
          {"artifacts/strategy-pov.md": STRATEGY_R2,
           "d03-calendar-ownership-made-explicit.md": entry(3, "product-strategist", "artifacts/strategy-pov.md", "The calendar-ownership assumption is now explicit and testable.", "Good Strategy Bad Strategy", None)},
          ["corpus/strategy/good-strategy-bad-strategy.md", "audits/gate-1-r1.md"],
          "Repair against gate r1. Calendar-ownership assumption now explicit and testable.", triggered_by="pass-02", launched="09:05"),
        P("red-team-gate", "gate", 1, CODEX, CODEX_LAUNCH, 7, (58900, 3100, 0), "codex footer",
          ["artifacts/strategy-pov.md", PROTOCOL], ["audits/gate-1-r2.md"], {"audits/gate-1-r2.md": GATE_1_R2}, [],
          "Gate PASS on round 2.", triggered_by="pass-03", withheld=WITHHELD + ["the corpus"], launched="09:30"),
        P("discovery-lead", "draft", 2, OPUS, AGENT, 41, (240100, 28700, 120000), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "evidence/interviews-01-08.md", "corpus/discovery/shelf.md",
           "corpus/discovery/continuous-discovery-habits.md", "corpus/discovery/the-mom-test.md"],
          ["artifacts/discovery-packet.md", f"{ENG_ID}.d04"],
          {"artifacts/discovery-packet.md": discovery(1),
           "d04-opportunity-tree-shape.md": entry(4, "discovery-lead", "artifacts/discovery-packet.md", "Four opportunities under three bets; B2 split into two.", "Continuous Discovery Habits", "corpus/discovery/continuous-discovery-habits.md")},
          ["corpus/discovery/continuous-discovery-habits.md", "corpus/discovery/the-mom-test.md", "evidence/interviews-01-08.md", "artifacts/strategy-pov.md"],
          "Eight interviews read in full. Opportunity tree drafted with five evidence claims.", launched="10:02"),
        P("insights-analytics", "co-sign", 2, OPUS, AGENT, 14, (131400, 6200, 0), "Agent-tool usage",
          ["artifacts/discovery-packet.md", "artifacts/strategy-pov.md", "evidence/interviews-01-08.md"],
          ["audits/cosign-discovery-r1.md"], {"audits/cosign-discovery-r1.md": COSIGN_R1},
          ["evidence/interviews-01-08.md", "artifacts/discovery-packet.md"],
          "Bounced E2 (no interviewee said it unprompted) and E4 (count stated as six, transcripts show four).", launched="10:48"),
        P("discovery-lead", "repair", 2, OPUS, AGENT, 16, (88300, 11000, 110000), "Agent-tool usage",
          ["artifacts/discovery-packet.md", "audits/cosign-discovery-r1.md", "evidence/interviews-01-08.md"],
          ["artifacts/discovery-packet.md", f"{ENG_ID}.d05"],
          {"artifacts/discovery-packet.md": discovery(2),
           "d05-e2-dropped-e4-restated.md": entry(5, "discovery-lead", "artifacts/discovery-packet.md", "E2 dropped; E4 restated at four of eight with transcript pointers.", "The Mom Test", None)},
          ["evidence/interviews-01-08.md", "audits/cosign-discovery-r1.md", "corpus/discovery/the-mom-test.md"],
          "Repair against co-sign r1.", triggered_by="pass-06", launched="11:06"),
        P("insights-analytics", "co-sign", 2, OPUS, AGENT, 11, (128800, 4900, 0), "Agent-tool usage",
          ["artifacts/discovery-packet.md", "evidence/interviews-01-08.md"], ["audits/cosign-discovery-r2.md"],
          {"audits/cosign-discovery-r2.md": COSIGN_R2}, ["evidence/interviews-01-08.md", "artifacts/discovery-packet.md"],
          "All four remaining claims graded; packet done.", triggered_by="pass-07", launched="11:24"),
        P("insights-analytics", "draft", 3, OPUS, AGENT, 29, (176500, 19800, 130000), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md", "corpus/insights/shelf.md", "corpus/insights/trustworthy-online-experiments.md"],
          ["artifacts/metrics-evidence-plan.md", f"{ENG_ID}.d06"],
          {"artifacts/metrics-evidence-plan.md": INSIGHTS,
           "d06-oc3-bounced-unmeasurable.md": entry(6, "insights-analytics", "artifacts/metrics-evidence-plan.md", "OC-3 bounced to the Strategist rather than given an invented metric.", "Trustworthy Online Controlled Experiments", "corpus/insights/trustworthy-online-experiments.md")},
          ["corpus/insights/trustworthy-online-experiments.md", "artifacts/discovery-packet.md", "artifacts/strategy-pov.md"],
          "Metrics plan drafted. No acquisition metric: the Strategy doc names none (bounced OC-3 back to Strategist as unmeasurable).", launched="12:10"),
        P("discovery-lead", "audit", 1, OPUS, AGENT, 12, (119000, 5400, 0), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md"], ["audits/audit-strategy.md"],
          {"audits/audit-strategy.md": audit("strategy", "discovery-lead", 1, f"{ENG_ID}.strategy", "AUDIT CLEAN — stake held", "Stake: does the diagnosis survive the evidence? Yes; one wording note on OC-3.")},
          ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md"],
          "Stake: does the diagnosis survive the evidence? Yes; one wording note.", launched="12:55"),
        P("product-leadership", "audit", 2, OPUS, AGENT, 11, (117000, 4900, 0), "Agent-tool usage",
          ["artifacts/discovery-packet.md", "artifacts/strategy-pov.md"], ["audits/audit-discovery.md"],
          {"audits/audit-discovery.md": audit("discovery", "product-leadership", 2, f"{ENG_ID}.discovery", "AUDIT CLEAN — stake held", "Stake: is any opportunity a stakeholder in disguise? No; the association (E5) is a channel, not an opportunity.")},
          ["artifacts/discovery-packet.md"],
          "Stake: is any opportunity a stakeholder in disguise? No.", launched="13:05"),
        P("growth-distribution", "draft", 4, SONNET, AGENT, 22, (151200, 17400, 140000), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md", "artifacts/metrics-evidence-plan.md", "corpus/growth/shelf.md"],
          ["artifacts/growth-gtm.md", f"{ENG_ID}.d07"],
          {"artifacts/growth-gtm.md": GROWTH,
           "d07-loop-l1-over-paid-acquisition.md": entry(7, "growth-distribution", "artifacts/growth-gtm.md", "One cast-invite loop over paid acquisition.", "none", None)},
          ["corpus/growth/shelf.md", "artifacts/metrics-evidence-plan.md"],
          "Grounding manifest-only for Growth's corpus (shelf label read; book not opened).", launched="13:20"),
        P("insights-analytics", "audit", 4, OPUS, AGENT, 13, (141900, 6800, 0), "Agent-tool usage",
          ["artifacts/growth-gtm.md", "artifacts/metrics-evidence-plan.md"], ["audits/audit-growth.md"],
          {"audits/audit-growth.md": audit("growth", "insights-analytics", 4, f"{ENG_ID}.growth", "AUDIT LOOPBACK — 1 material", "Stake: can every loop target be measured by the plan? No: L1 has a target and no metric, because the plan has no acquisition metric.")},
          ["artifacts/growth-gtm.md", "artifacts/metrics-evidence-plan.md"],
          "Stake: can every loop target be measured by the plan? No: L1 has a target and no metric.", launched="13:50"),
        P("business-economics", "draft", 5, SONNET, AGENT, 26, (163000, 18900, 150000), "Agent-tool usage",
          ["artifacts/strategy-pov.md", "artifacts/discovery-packet.md", "artifacts/metrics-evidence-plan.md", "artifacts/growth-gtm.md",
           "corpus/business/shelf.md", "corpus/business/monetizing-innovation.md"],
          ["artifacts/business-case.md", f"{ENG_ID}.d08"],
          {"artifacts/business-case.md": BUSINESS,
           "d08-per-season-price-hypothesis.md": entry(8, "business-economics", "artifacts/business-case.md", "Per-season pricing carried as the primary hypothesis.", "Monetizing Innovation", "corpus/business/monetizing-innovation.md")},
          ["corpus/business/monetizing-innovation.md", "artifacts/growth-gtm.md", "artifacts/strategy-pov.md"],
          "", launched="14:10"),
        P("growth-distribution", "audit", 5, SONNET, AGENT, 9, (122400, 4100, 0), "Agent-tool usage",
          ["artifacts/business-case.md", "artifacts/growth-gtm.md"], ["audits/audit-business.md"],
          {"audits/audit-business.md": audit("business", "growth-distribution", 5, f"{ENG_ID}.business", "AUDIT CLEAN — stake held", "Stake: does the model price the loop it depends on? Yes: L1 is priced under PH-2.")},
          ["artifacts/business-case.md"], "Stake: does the model price the loop it depends on? Yes.", launched="14:48"),
        P("delivery-execution", "draft", 6, SONNET, AGENT, 31, (198700, 24200, 160000), "Agent-tool usage",
          SIX[:5] + ["corpus/delivery/shelf.md", "corpus/delivery/shape-up.md"],
          ["artifacts/outcome-roadmap.md", "artifacts/handoff-brief.md", f"{ENG_ID}.d09"],
          {"artifacts/outcome-roadmap.md": ROADMAP, "artifacts/handoff-brief.md": HANDOFF,
           "d09-first-slice-needs-a-scheduling-layer.md": entry(9, "delivery-execution", "artifacts/outcome-roadmap.md", "The first shipping slice has a Systemcraft-owned scheduling layer; a brief crosses.", "Shape Up", "corpus/delivery/shape-up.md")},
          ["corpus/delivery/shape-up.md", "artifacts/business-case.md", "artifacts/metrics-evidence-plan.md"],
          "Baseline pass of a shadow pair (the trial follows).", launched="15:05"),
        P("product-strategist", "co-sign", 6, OPUS, AGENT, 10, (117300, 4600, 0), "Agent-tool usage",
          ["artifacts/outcome-roadmap.md", "artifacts/strategy-pov.md"], ["audits/cosign-okr.md"],
          {"audits/cosign-okr.md": COSIGN_R2.replace("cosign-discovery", "cosign-okr").replace("insights-analytics", "product-strategist").replace("stage: 2", "stage: 6").replace(f"{ENG_ID}.discovery", f"{ENG_ID}.roadmap")},
          ["artifacts/outcome-roadmap.md", "artifacts/strategy-pov.md"], "Every key result passed against its outcome.", launched="15:44"),
        P("delivery-execution", "trial", 6, CODEX, CODEX_LAUNCH, 24, (171900, 22800, 0), "codex footer",
          [], ["trace/trials/outcome-roadmap-trial.md"], {"trace/trials/outcome-roadmap-trial.md": TRIAL},
          ["corpus/delivery/shape-up.md", "artifacts/business-case.md"],
          "Shadow pass on identical inputs. Label blind.", shadow_of="pass-16", same_inputs_as="pass-16", launched="15:06"),
        P("business-economics", "audit", 6, SONNET, AGENT, 11, (126800, 5000, 0), "Agent-tool usage",
          ["artifacts/outcome-roadmap.md", "artifacts/business-case.md"], ["audits/audit-roadmap.md"],
          {"audits/audit-roadmap.md": audit("roadmap", "business-economics", 6, f"{ENG_ID}.roadmap", "AUDIT CLEAN — stake held", "Stake: does the first bet pay for the second? Yes, on PH-2.")},
          ["artifacts/outcome-roadmap.md"], "Stake: does the first bet pay for the second? Yes.", launched="16:02"),
        P("red-team-gate", "gate", 6, CODEX, CODEX_LAUNCH, 8, (64100, 3900, 0), "codex footer",
          ["artifacts/handoff-brief.md", PROTOCOL], ["audits/gate-2-r1.md"],
          {"audits/gate-2-r1.md": GATE_1_R2.replace("gate-1", "gate-2").replace("strategy-sign-off", "pre-handoff").replace(f"{ENG_ID}.strategy", f"{ENG_ID}.handoff").replace("STRATEGY PASS", "HANDOFF PASS")},
          [], "Gate PASS. Brief crosses to Systemcraft with a return date.", withheld=WITHHELD + ["the corpus"], launched="16:30"),
        P("product-leadership", "draft", 7, OPUS, AGENT, 33, (205300, 26100, 170000), "Agent-tool usage",
          SIX + ["artifacts/handoff-brief.md", "corpus/leadership/shelf.md"],
          ["artifacts/leadership-packet.md", f"{ENG_ID}.d10"],
          {"artifacts/leadership-packet.md": LEADERSHIP,
           "d10-agents-as-their-own-entity-type.md": entry(10, "product-leadership", "artifacts/leadership-packet.md", "Agents appear in the topology as their own entity type, never as people.", "none", None)},
          ["corpus/leadership/shelf.md", "artifacts/handoff-brief.md", "artifacts/outcome-roadmap.md"],
          "Grounding manifest-only.", launched="16:50"),
        P("product-strategist", "audit", 7, OPUS, AGENT, 12, (139500, 5700, 0), "Agent-tool usage",
          ["artifacts/leadership-packet.md", "artifacts/strategy-pov.md"], ["audits/audit-leadership.md"],
          {"audits/audit-leadership.md": audit("leadership", "product-strategist", 7, f"{ENG_ID}.leadership", "AUDIT NOTES ONLY", "Stake: does the operating model serve the guiding policy? One note on the decision-rights table.")},
          ["artifacts/leadership-packet.md"], "Stake: does the operating model serve the guiding policy? One note on the decision-rights table.", launched="17:35"),
        P("delivery-execution", "audit", 3, SONNET, AGENT, 10, (118200, 4400, 0), "Agent-tool usage",
          ["artifacts/metrics-evidence-plan.md", "artifacts/outcome-roadmap.md"], ["audits/audit-insights.md"],
          {"audits/audit-insights.md": audit("insights", "delivery-execution", 3, f"{ENG_ID}.insights", "AUDIT NOTES ONLY", "Stake: can the roadmap's key results be read off the plan's metrics? Yes for KR-1, KR-2; KR-3 has no metric.")},
          ["artifacts/metrics-evidence-plan.md"], "Stake: can the roadmap's key results be read off the plan's metrics? Yes for KR-1, KR-2; KR-3 has no metric.", launched="17:58"),
        P("red-team-gate", "gate", 7, CODEX, CODEX_LAUNCH, 14, (92600, 6200, 0), "codex footer",
          ["artifacts/", PROTOCOL], ["audits/gate-close-r1.md"],
          {"audits/gate-close-r1.md": GATE_1_R2.replace("gate-1", "gate-close").replace("strategy-sign-off", "close").replace(f"{ENG_ID}.strategy", "the whole train").replace("STRATEGY PASS", "TRAIN PASS WITH ACCEPTANCES")},
          [], "Gate at close. Anchor: the whole train.", withheld=WITHHELD + ["the corpus"], launched="18:20"),
        P("coordinator", "close", 0, "claude-fable-5-1", "interactive session", 0, None, "UNMEASURED",
          [], ["close.md"], {"close.md": "# Close — pc-eng-000\n\nADMINISTRATIVE CLOSE — OUTCOME PENDING D+14. Deviations: Growth and Leadership ran grounding manifest-only.\n"},
          [], "Coordinator's own session. Deviations: Growth and Leadership ran grounding manifest-only (corpus not yet ingested for those seats).",
          withheld=["nothing"], launched="18:40"),
    ]


# labels by pass index (1-based): (verdict, first_failing_stage, critique)
LABELS = {
    1: ("pass", None, "Diagnosis is one sentence and names the constraint. A new hire could restate it."),
    2: ("fail", 1, "Gate was right to fail it: the calendar assumption was load-bearing and unstated. The gate's own write-up buries the finding under two notes; lead with it."),
    3: ("pass", None, "The split is honest and the register is testable. Dropping Action 4 was correct."),
    4: ("pass", None, ""),
    5: ("pass", None, "Reads the interviews rather than the brief's summary of them. Splitting B2 into O2 and O3 is defensible."),
    6: ("fail", 2, "Right to bounce E2 and E4, but E4's bounce is the packet's fault, not the co-sign's; this row fails because the co-sign let E3 through with a count nobody can find in the transcripts."),
    7: ("pass", None, ""),
    8: ("pass", None, ""),
    9: ("pass", None, "Bouncing OC-3 to the Strategist instead of inventing a metric is exactly the rule."),
    10: ("pass", None, ""),
    11: ("pass", None, ""),
    12: ("pass", None, "Manifest-only grounding declared, not hidden. Loop L1 target has no metric, which surfaces at the audit."),
    13: ("fail", 3, "The audit is correct and the failure is upstream: the metrics plan (stage 3) has no acquisition metric, so Growth could not have measured L1. Fix the plan, not the loop."),
    14: ("pass", None, ""),
    15: ("pass", None, ""),
    16: ("pass", None, "Appetites are stated in weeks with a circuit breaker each. KR-3 is unmeasured; see the Delivery audit of stage 3."),
    17: ("pass", None, ""),
    18: (None, None, ""),
    19: ("pass", None, ""),
    20: ("pass", None, ""),
    21: ("fail", 6, "The stakeholder map is fine. The topology names a return date that the handoff brief (stage 6) never set as a constraint on the team, so the packet inherited a constraint that does not exist."),
    22: (None, None, ""),
    23: (None, None, ""),
    24: ("pass", None, ""),
    25: ("pass", None, ""),
}


# --------------------------------------------------------------------------- #
# the guided-reading cases — invented teaching copy for an invented engagement
# --------------------------------------------------------------------------- #


def cases_md(out: Path) -> str:
    """Two cases over the synthetic train: one worked, one on the reader's own.

    Written last, so each source carries the sha256 of the file as the builder
    leaves it — the same contract a real writer works under.
    """
    gate = hash_path(out, "audits/gate-1-r1.md")
    strategy = hash_path(out, "artifacts/strategy-pov.md")
    growth_audit = hash_path(out, "audits/audit-growth.md")
    plan = hash_path(out, "artifacts/metrics-evidence-plan.md")
    return f"""---
engagement: {ENG_SLUG}
written: 2026-09-20
status: proposed
---

# What happened in this review

A made-up studio planned a casting tool for community theatre, and this page is the record of that planning
being checked. Two moments are worth reading closely. Early on, a check stopped the strategy over a sentence
that was never written down. Later, a check found a real hole and pointed at the wrong document as its cause.
Everything here is invented for the kit's tests: no seat wrote it, no theatre exists, and nobody was interviewed.

## Case: A check stops the strategy over something nobody wrote down

pass: pass-02
finding: 1
assist: worked
question: What was the gate actually objecting to?
options:
  - key: a
    label: The plan picked the wrong problem to solve
  - key: b
    label: The plan leaned on a belief it never stated or tested
  - key: c
    label: The plan had too many actions for its budget
sources:
  - path: audits/gate-1-r1.md
    sha256: {gate}
    excerpt: "GP-1 rests on an unstated assumption that directors control the rehearsal calendar."
    label: Finding 1 · the gate's first round
  - path: artifacts/strategy-pov.md
    sha256: {strategy}
    excerpt: "A1 — directors control the rehearsal calendar (testable in the pilot)."
    label: What the repaired strategy says now

### Story

The studio wanted to end the scramble that eats two rehearsal weeks a season, so its first document promised
that the tool would own the rehearsal calendar and hand directors slots to accept. That promise only works if
directors are the people who decide when rehearsals happen.

Nothing in the document said so. The check read the promise, asked what had to be true for it to work, and
found a belief holding up the whole plan with nothing behind it — no interview, no register entry, no way to
be proved wrong. The reviewer graded that as serious enough to stop the document, and left two smaller notes
about wording alone.

The repair did not argue. It wrote the belief down as something to test in the pilot, split the promise into
the case where a venue shares its calendar and the case where it does not, and dropped an action that no
longer had a reason. The second round of the same check passed.

### Hint

Read the promise and ask what would have to be true about the people involved for it to work at all.

### Reveal

The objection was to an unstated, untested belief, not to the choice of problem. The gate's own words are in
the excerpt: the guiding policy rested on an assumption that directors control the calendar, and the document
never said it. That is why the repair is one line in an assumption register rather than a new strategy. Note
what you are judging here: the gate did a good job on a document that was not yet good. Those are two separate
verdicts, and only the first one is yours on this run.

### Your turn

In your own words: what would have made this a note rather than a stop?

### Terms

- guiding policy: the one approach a strategy commits to, out of the ones it could have chosen.
- assumption register: the list of things a plan needs to be true, written so each one can be tested.

### Diagram

- A promise in the plan
- ? Is what it depends on written down
- no: A stop, until someone writes it down and says how to test it
- yes: A note at most, and the test goes in the register

## Case: A check finds a hole and names the document it is standing in

pass: pass-13
finding: none
assist: independent
question: Where does the fix for this belong?
options:
  - key: a
    label: In the growth document, which set the target
  - key: b
    label: In the metrics plan one stage earlier, which has no metric to measure it with
  - key: c
    label: Nowhere yet — there is not enough evidence to say
sources:
  - path: audits/audit-growth.md
    sha256: {growth_audit}
    excerpt: "Stake: can every loop target be measured by the plan? No: L1 has a target and no metric, because the plan has no acquisition metric."
    label: The audit of the growth document
  - path: artifacts/metrics-evidence-plan.md
    sha256: {plan}
    excerpt: "OC-3 is bounced to the Strategist as unmeasurable by this plan"
    label: The metrics plan, one stage earlier

### Story

The growth document promises a loop: a director invites the cast, and cast members become next season's
directors. It puts a number on it — thirty invites per production — which is the kind of target someone is
supposed to read off a dashboard later.

The check that follows asks one question of every loop: can the plan actually measure this? Read the two
excerpts and answer before you read on. The metrics plan written one stage earlier lists four metrics, and
none of them counts anyone arriving.

### Reveal

The auditor was right that the target cannot be read, and the reviewer of this run recorded the failure one
stage upstream: the metrics plan has no acquisition metric, so the growth seat could not have measured its
loop no matter how it wrote the target. Fixing the growth document alone would leave the hole exactly where
it is. This is the most useful line on the page when it happens — it says the work to redo is somewhere other
than the pass you are reading.

### Your turn

Write the sentence you would put in the critique, naming the evidence and the consequence.

### Terms

- loop: a way the product brings the next user in through the last one.
- first failing stage: the point in the train where the problem entered, which can be earlier than the run you are reading.
"""


# --------------------------------------------------------------------------- #
# the builder
# --------------------------------------------------------------------------- #


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def hash_path(root: Path, rel: str) -> str:
    p = root / rel
    if p.is_dir():
        h = hashlib.sha256()
        for f in sorted(x for x in p.rglob("*") if x.is_file()):
            h.update(f"{f.relative_to(p).as_posix()}\0{sha256_bytes(f.read_bytes())}\n".encode())
        return h.hexdigest()
    return sha256_bytes(p.read_bytes())


def record_text(pid: str, spec: dict, inputs: list[tuple[str, str]], outputs: list[dict]) -> str:
    seat, kind = spec["seat"], spec["kind"]
    launched = f"2026-10-06T{spec['launched']}:00-04:00"
    hh, mm = map(int, spec["launched"].split(":"))
    total = hh * 60 + mm + spec["minutes"]
    completed = f"2026-10-06T{total // 60:02d}:{total % 60:02d}:00-04:00"
    lines = [
        "---",
        f"pass: {pid}", f"seat: {seat}", f"kind: {kind}", f"stage: {spec['stage']}",
        f"runtime: {spec['runtime']}", f'launch: "{spec["launch"]}"',
        f"effort: {'—' if kind == 'close' else 'high'}",
        f"launched: {launched}", f"completed: {completed}", f"wall_clock_s: {spec['minutes'] * 60}",
    ]
    if spec["meter"] is None:
        lines.append("meter: null")
    else:
        i, o, c = spec["meter"]
        lines += ["meter:", f"  input: {i}", f"  output: {o}", f"  cached: {c}"]
    lines.append(f"meter_source: {spec['meter_source']}")
    if inputs:
        lines.append("inputs:")
        for path, h in inputs:
            lines += [f"  - path: {path}", f"    sha256: {h}"]
    else:
        lines.append("inputs: []")
    lines.append("withheld:")
    lines += [f"  - {w}" for w in spec["withheld"]]
    lines.append("outputs:")
    for o in outputs:
        if "id" in o:
            lines.append(f"  - id: {o['id']}")
        else:
            lines += [f"  - path: {o['path']}", f"    sha256: {o['sha256']}"]
    ext = "txt" if spec["runtime"].startswith("codex") else "jsonl"
    lines.append(f"raw_log: {'—' if kind == 'close' else f'trace/logs/{pid}.{ext}'}")
    lines.append("checks: []")
    lines.append(f"triggered_by: {spec['triggered_by'] or 'null'}")
    lines.append(f"shadow_of: {spec['shadow_of'] or 'null'}")
    lines.append("---")
    lines.append("")
    lines.append("## Corpus read")
    lines.append("")
    if spec["corpus_read"]:
        lines += [f"- {c}" for c in spec["corpus_read"]]
    else:
        lines.append("none" + (" (gate: corpus withheld)" if kind == "gate" else ""))
    lines += ["", "## Moves", ""]
    art = next((o["path"] for o in outputs if "path" in o and (o["path"].startswith("artifacts/") or "/trials/" in o["path"])), None)
    lines.append(f"{art} § Moves" if art and kind in ("draft", "repair", "trial") else "none — this kind hands no artifact forward")
    lines += ["", "## Notes", "", spec["notes"] or "none", ""]
    return "\n".join(lines)


def fill_checks(records: dict[str, str], specs: list[dict], outputs_by_pid: dict[str, list[dict]]) -> None:
    """Transcribe each check pass's verdict onto the pass it checked (the coordinator's after-step)."""
    # map artifact path → list of pass ids that produced it (latest wins per stage)
    producers: dict[str, list[str]] = {}
    for i, spec in enumerate(specs, start=1):
        pid = f"pass-{i:02d}"
        for o in outputs_by_pid[pid]:
            if "path" in o:
                producers.setdefault(o["path"], []).append(pid)
    for i, spec in enumerate(specs, start=1):
        pid = f"pass-{i:02d}"
        if spec["kind"] not in ("audit", "co-sign", "gate"):
            continue
        verdict = ""
        for path, text in spec["writes"].items():
            for line in text.split("\n"):
                if line.startswith("verdict:"):
                    verdict = line.split(":", 1)[1].strip()
        # the checked artifact is the pass's first artifacts/ input
        checked = next((p for p in spec["inputs"] if p.startswith("artifacts/") and p != "artifacts/"), None)
        if not checked or checked not in producers:
            continue
        # the producer whose output hash equals this pass's recorded input hash
        target = producers[checked][-1]
        for prod in producers[checked]:
            rec = records[prod]
            for o in outputs_by_pid[prod]:
                if o.get("path") == checked and f"sha256: {o['sha256']}" in records[pid]:
                    target = prod
        records[target] = records[target].replace(
            "checks: []", f"checks:\n  - pass: {pid}\n    kind: {spec['kind']}\n    verdict: {verdict}", 1
        ) if "checks: []" in records[target] else records[target].replace(
            "triggered_by:", f"  - pass: {pid}\n    kind: {spec['kind']}\n    verdict: {verdict}\ntriggered_by:", 1)


def build(out: Path) -> Path:
    if "ledger" in {p.lower() for p in out.resolve().parts}:
        raise SystemExit("refusing to build a synthetic engagement inside a ledger/ path")
    out.mkdir(parents=True, exist_ok=True)
    (out / "brief.md").write_text(
        "---\n"
        f"id: {ENG_ID}\nname: Callboard\ntype: full-train\nopened: 2026-10-06\nclosed: 2026-10-06\n"
        "pass_budget: 26\nsynthetic: true\n---\n\n"
        "# Brief — Callboard (synthetic)\n\nA casting-and-callback scheduling tool for community theatre. Invented for the trace kit's tests (#290); no seat wrote any of this and no book was read for it.\n",
        encoding="utf-8",
    )
    for rel, lane in CORPUS.items():
        p = out / rel
        p.mkdir(parents=True, exist_ok=True) if False else p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# {rel}\n\nSynthetic {lane} shelf label — invented for the trace kit's tests; not a distillate, no book text.\n", encoding="utf-8")
    (out / "evidence").mkdir(exist_ok=True)
    (out / "evidence" / "interviews-01-08.md").write_text(EVIDENCE, encoding="utf-8")
    (out / "templates").mkdir(exist_ok=True)
    (out / "templates" / "red-team-protocol.md").write_text("# Red-team protocol (stub)\n\nSynthetic stand-in for the inherited protocol.\n", encoding="utf-8")
    for d in ("artifacts", "audits", "trace/logs", "trace/trials"):
        (out / d).mkdir(parents=True, exist_ok=True)

    specs = passes()
    records: dict[str, str] = {}
    inputs_by_pid: dict[str, list[tuple[str, str]]] = {}
    outputs_by_pid: dict[str, list[dict]] = {}
    for i, spec in enumerate(specs, start=1):
        pid = f"pass-{i:02d}"
        if spec["same_inputs_as"]:
            inputs = list(inputs_by_pid[spec["same_inputs_as"]])
        else:
            inputs = [(rel, hash_path(out, rel)) for rel in spec["inputs"]]
        inputs_by_pid[pid] = inputs
        for rel, text in spec["writes"].items():
            p = out / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        outputs = []
        for o in spec["outputs"]:
            if "/" in o or o.endswith(".md"):
                outputs.append({"path": o, "sha256": hash_path(out, o)})
            else:
                outputs.append({"id": o})
        outputs_by_pid[pid] = outputs
        if spec["kind"] != "close":
            ext = "txt" if spec["runtime"].startswith("codex") else "jsonl"
            (out / "trace" / "logs" / f"{pid}.{ext}").write_text(
                '{"synthetic": true, "note": "stub transcript; the kit never parses raw logs at rung 0"}\n', encoding="utf-8")
        records[pid] = record_text(pid, spec, inputs, outputs)
    fill_checks(records, specs, outputs_by_pid)
    for i, spec in enumerate(specs, start=1):
        pid = f"pass-{i:02d}"
        (out / "trace" / f"{pid}-{spec['seat']}-{spec['kind']}.md").write_text(records[pid], encoding="utf-8")

    rows = []
    for i in range(1, len(specs) + 1):
        v, ffs, crit = LABELS.get(i, (None, None, ""))
        rows.append(f"| pass-{i:02d} | {v or ''} | {ffs or ''} | {crit.replace('|', chr(92) + '|')} |  |")
    (out / "trace" / "labels.md").write_text(
        "---\n"
        f"engagement: {ENG_SLUG}\nlabeler: Sean\n---\n\n"
        "# Labels — pc-eng-000 Callboard (synthetic)\n\n"
        "One row per pass. `verdict` is pass or fail, nothing between. `first_failing_stage` is set on a fail and may be upstream of the pass read. `critique`: one to three sentences a new hire could act on. `failure_code` stays blank until the taxonomy exists.\n\n"
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    (out / "trace" / "cases.md").write_text(cases_md(out), encoding="utf-8")
    (out / "trace" / "notes.md").write_text(
        "# Process notes — pc-eng-000 (synthetic)\n\n"
        "- 2026-10-06 Synthetic process notes. The stage-3 break is the one to watch: an audit at stage 4 found a hole "
        "in the metrics plan, which is exactly the upstream-of-the-pass-read line the viewer is built to show.\n"
        "- 2026-10-06 The strategy was redrafted in place after the gate, so its first revision is no longer on disk; "
        "the pass records keep the history and the checker says so rather than passing it quietly.\n"
        "- 2026-10-06 The roadmap ran as a shadow pair (pass-16 baseline, pass-18 trial) and both stay blind until "
        "each carries a verdict in the labels file.\n"
        "- 2026-10-06 Growth and Leadership ran grounding manifest-only: the shelf labels were read, the books were not.\n",
        encoding="utf-8",
    )
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 tests/synth.py <out-dir>")
    target = build(Path(sys.argv[1]))
    n = len(list((target / "trace").glob("pass-*.md")))
    print(f"built synthetic engagement at {target} ({n} pass records)")
