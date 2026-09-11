#!/usr/bin/env python3
"""Prototype renderer for the eval viewer — #292 sample render.

This is NOT the trace kit's renderer (#290 builds that, to DESIGN.md). It is the
hand-built prototype that produced samples/pc-eng-000-callboard/eval.html so
Sean had a page to react to. Everything in SYNTH is invented: a fictional
engagement, fictional seats' output, fictional meters. No ledger content.

Run:  python3 samples/render_sample.py   (from productcraft/trace/)
"""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACE = HERE.parent
OUT = HERE / "pc-eng-000-callboard" / "eval.html"

STAGES = {
    1: ("Strategist", "Strategy & POV"),
    2: ("Discovery", "Discovery packet"),
    3: ("Insights", "Metrics & evidence plan"),
    4: ("Growth", "Distribution plan"),
    5: ("Business", "Economics model"),
    6: ("Delivery", "Roadmap & handoff brief"),
    7: ("Leadership", "Leadership packet"),
}

# ---------------------------------------------------------------------------
# Synthetic engagement. Callboard: a fictional casting-and-scheduling tool for
# community theatre. Invented for this sample; not a studio engagement.
# ---------------------------------------------------------------------------
P = []  # passes


def rec(pid, seat, kind, stage, runtime, launch, effort, minutes, tin, tout, tcached,
        meter_source, inputs, withheld, outputs, raw_log, checks, corpus, moves, notes,
        triggered_by=None, shadow_of=None, launched=None):
    P.append(dict(pass_id=pid, seat=seat, kind=kind, stage=stage, runtime=runtime,
                  launch=launch, effort=effort, wall_clock_s=minutes * 60, meter=dict(
                      input=tin, output=tout, cached=tcached), meter_source=meter_source,
                  inputs=inputs, withheld=withheld, outputs=outputs, raw_log=raw_log,
                  checks=checks, corpus_read=corpus, moves=moves, notes=notes,
                  triggered_by=triggered_by, shadow_of=shadow_of, launched=launched))


OPUS = "claude-opus-5"
SONNET = "claude-sonnet-5"
CODEX = "codex gpt-5.6-sol (high)"
AGENT = "Agent tool, fresh context"
CODEX_LAUNCH = "codex exec --model gpt-5.6-sol -c reasoning.effort=high"
WITHHELD = ["the drafting conversation", "ledger entries of other engagements"]
H = lambda n: f"sha256:{n:04x}…{(n * 7919) % 0xffff:04x}"  # noqa: E731 — fake hashes

rec("pass-01", "Strategist", "draft", 1, OPUS, AGENT, "high", 34, 182_400, 21_300, 96_000,
    "Agent-tool usage",
    [("engagement/brief.md", H(1)), ("corpus/strategy/shelf.md", H(2)), ("corpus/strategy/good-strategy-bad-strategy.md", H(3))],
    WITHHELD, ["artifacts/01-strategy-pov.md", "pc-eng-000.d01", "pc-eng-000.d02"],
    "logs/pass-01.jsonl",
    [("pass-02", "gate", "FAIL"), ("pass-04", "gate", "PASS"), ("pass-10", "audit", "PASS")],
    ["corpus/strategy/good-strategy-bad-strategy.md", "corpus/strategy/shelf.md", "engagement/brief.md"],
    {"origin": True, "leaned_on": ["Rumelt's kernel: diagnosis, guiding policy, coherent action"]},
    "Origin draft. Named the casting bottleneck as the diagnosis; two candidate guiding policies drafted, one chosen.",
    launched="2026-10-06T08:12")
rec("pass-02", "Red-team gate", "gate", 1, CODEX, CODEX_LAUNCH, "high", 9, 61_200, 4_800, 0,
    "codex footer",
    [("artifacts/01-strategy-pov.md", H(4)), ("templates/red-team-protocol.md", H(5))],
    WITHHELD + ["the corpus"], ["gates/g1-strategy-signoff-r1.md"], "logs/pass-02.txt",
    [], [], None,
    "Gate FAIL: guiding policy rests on an unstated assumption that directors control the rehearsal calendar.",
    launched="2026-10-06T08:51")
rec("pass-03", "Strategist", "repair", 1, OPUS, AGENT, "high", 18, 96_700, 9_900, 88_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(4)), ("gates/g1-strategy-signoff-r1.md", H(6))],
    WITHHELD, ["artifacts/01-strategy-pov.md", "pc-eng-000.d03"], "logs/pass-03.jsonl",
    [("pass-04", "gate", "PASS")], ["corpus/strategy/good-strategy-bad-strategy.md", "gates/g1-strategy-signoff-r1.md"],
    {"kept": 6, "added": 2, "split": 1, "merged": 0, "dropped": 1, "lines": [
        ("split", "Guiding policy → GP-a (directors own the calendar) and GP-b (the tool proposes, the director accepts)", "from GP-1, sources S3, S7"),
        ("added", "Assumption register A1–A2", "from gate finding 1"),
        ("dropped", "Action 4 (venue integration)", "no source survived the split")]},
    "Repair against gate r1. Calendar-ownership assumption now explicit and testable.",
    triggered_by="pass-02", launched="2026-10-06T09:05")
rec("pass-04", "Red-team gate", "gate", 1, CODEX, CODEX_LAUNCH, "high", 7, 58_900, 3_100, 0,
    "codex footer",
    [("artifacts/01-strategy-pov.md", H(7)), ("templates/red-team-protocol.md", H(5))],
    WITHHELD + ["the corpus"], ["gates/g1-strategy-signoff-r2.md"], "logs/pass-04.txt",
    [], [], None, "Gate PASS on round 2.", triggered_by="pass-03", launched="2026-10-06T09:30")
rec("pass-05", "Discovery", "draft", 2, OPUS, AGENT, "high", 41, 240_100, 28_700, 120_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("engagement/evidence/interviews-01-08.md", H(8)), ("corpus/discovery/shelf.md", H(9)), ("corpus/discovery/continuous-discovery-habits.md", H(10)), ("corpus/discovery/the-mom-test.md", H(11))],
    WITHHELD, ["artifacts/02-discovery-packet.md", "pc-eng-000.d04", "pc-eng-000.d05"], "logs/pass-05.jsonl",
    [("pass-06", "co-sign", "BOUNCED 2"), ("pass-08", "co-sign", "PASS"), ("pass-21", "audit", "—")],
    ["corpus/discovery/continuous-discovery-habits.md", "engagement/evidence/interviews-01-08.md", "artifacts/01-strategy-pov.md"],
    {"kept": 9, "added": 5, "split": 0, "merged": 2, "dropped": 0, "lines": [
        ("merged", "Opportunities O2 + O5 → O2 (\"the callback scramble\")", "from interviews 3, 4, 6"),
        ("added", "Evidence claims E1–E5", "from interviews 1–8")]},
    "Eight interviews read in full. Opportunity tree drafted with five evidence claims.",
    launched="2026-10-06T10:02")
rec("pass-06", "Insights", "co-sign", 2, OPUS, AGENT, "high", 14, 131_400, 6_200, 0,
    "Agent-tool usage",
    [("artifacts/02-discovery-packet.md", H(12)), ("artifacts/01-strategy-pov.md", H(7)), ("engagement/evidence/interviews-01-08.md", H(8))],
    WITHHELD, ["cosigns/02-evidence-r1.md"], "logs/pass-06.jsonl",
    [], ["engagement/evidence/interviews-01-08.md", "artifacts/02-discovery-packet.md"], None,
    "Bounced E2 (\"directors want fewer emails\": no interviewee said it unprompted) and E4 (count stated as six, transcripts show four).",
    launched="2026-10-06T10:48")
rec("pass-07", "Discovery", "repair", 2, OPUS, AGENT, "high", 16, 88_300, 11_000, 110_000,
    "Agent-tool usage",
    [("artifacts/02-discovery-packet.md", H(12)), ("cosigns/02-evidence-r1.md", H(13)), ("engagement/evidence/interviews-01-08.md", H(8))],
    WITHHELD, ["artifacts/02-discovery-packet.md", "pc-eng-000.d06"], "logs/pass-07.jsonl",
    [("pass-08", "co-sign", "PASS")], ["engagement/evidence/interviews-01-08.md", "cosigns/02-evidence-r1.md"],
    {"kept": 12, "added": 1, "split": 0, "merged": 0, "dropped": 1, "lines": [
        ("dropped", "E2", "no unprompted source"),
        ("added", "E4 restated at four of eight, transcripts 2, 3, 5, 8 linked", "from co-sign bounce")]},
    "Repair against co-sign r1.", triggered_by="pass-06", launched="2026-10-06T11:06")
rec("pass-08", "Insights", "co-sign", 2, OPUS, AGENT, "high", 11, 128_800, 4_900, 0,
    "Agent-tool usage",
    [("artifacts/02-discovery-packet.md", H(14)), ("engagement/evidence/interviews-01-08.md", H(8))],
    WITHHELD, ["cosigns/02-evidence-r2.md"], "logs/pass-08.jsonl",
    [], ["engagement/evidence/interviews-01-08.md", "artifacts/02-discovery-packet.md"], None,
    "All four remaining claims graded; packet done.", triggered_by="pass-07", launched="2026-10-06T11:24")
rec("pass-09", "Insights", "draft", 3, OPUS, AGENT, "high", 29, 176_500, 19_800, 130_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("corpus/insights/shelf.md", H(15)), ("corpus/insights/trustworthy-online-experiments.md", H(16))],
    WITHHELD, ["artifacts/03-metrics-evidence-plan.md", "pc-eng-000.d07"], "logs/pass-09.jsonl",
    [("pass-12", "audit", "BOUNCED"), ("pass-22", "audit", "—")],
    ["corpus/insights/trustworthy-online-experiments.md", "artifacts/02-discovery-packet.md", "artifacts/01-strategy-pov.md"],
    {"kept": 8, "added": 4, "split": 1, "merged": 0, "dropped": 0, "lines": [
        ("split", "Outcome OC-1 → OC-1a (time-to-cast) and OC-1b (callback no-shows)", "from OC-1, sources E1, E3"),
        ("added", "Metrics M1–M4 with instrumentation notes", "from OC-1a, OC-1b, OC-2")]},
    "Metrics plan drafted. No acquisition metric: the Strategy doc names none (bounced OC-3 back to Strategist as unmeasurable).",
    launched="2026-10-06T12:10")
rec("pass-10", "Discovery", "audit", 1, OPUS, AGENT, "high", 12, 119_000, 5_400, 0,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14))],
    WITHHELD, ["audits/01-strategy-by-discovery.md"], "logs/pass-10.jsonl",
    [], ["artifacts/01-strategy-pov.md", "artifacts/02-discovery-packet.md"], None,
    "Stake: does the diagnosis survive the evidence? Yes; one wording note.", launched="2026-10-06T12:55")
rec("pass-11", "Growth", "draft", 4, SONNET, AGENT, "high", 22, 151_200, 17_400, 140_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("artifacts/03-metrics-evidence-plan.md", H(17)), ("corpus/growth/shelf.md", H(18))],
    WITHHELD, ["artifacts/04-distribution-plan.md", "pc-eng-000.d08"], "logs/pass-11.jsonl",
    [("pass-12", "audit", "BOUNCED")], ["corpus/growth/shelf.md", "artifacts/03-metrics-evidence-plan.md"],
    {"kept": 10, "added": 3, "split": 0, "merged": 1, "dropped": 0, "lines": [
        ("added", "Loop L1 (director invites cast) with a target number", "from OC-2"),
        ("merged", "Channels C2 + C3 → C2 (regional theatre associations)", "from E5")]},
    "Grounding manifest-only for Growth's corpus (shelf label read; book not opened).", launched="2026-10-06T13:20")
rec("pass-12", "Insights", "audit", 4, OPUS, AGENT, "high", 13, 141_900, 6_800, 0,
    "Agent-tool usage",
    [("artifacts/04-distribution-plan.md", H(19)), ("artifacts/03-metrics-evidence-plan.md", H(17))],
    WITHHELD, ["audits/04-growth-by-insights.md"], "logs/pass-12.jsonl",
    [], ["artifacts/04-distribution-plan.md", "artifacts/03-metrics-evidence-plan.md"], None,
    "Stake: can every loop target be measured by the plan? No: L1 has a target and no metric, because the plan has no acquisition metric.",
    launched="2026-10-06T13:50")
rec("pass-13", "Business", "draft", 5, SONNET, AGENT, "high", 26, 163_000, 18_900, 150_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("artifacts/03-metrics-evidence-plan.md", H(17)), ("artifacts/04-distribution-plan.md", H(19)), ("corpus/business/shelf.md", H(20)), ("corpus/business/monetizing-innovation.md", H(21))],
    WITHHELD, ["artifacts/05-economics-model.md", "pc-eng-000.d09"], "logs/pass-13.jsonl",
    [("pass-14", "audit", "PASS")], ["corpus/business/monetizing-innovation.md", "artifacts/04-distribution-plan.md", "artifacts/01-strategy-pov.md"],
    {"kept": 11, "added": 4, "split": 0, "merged": 0, "dropped": 2, "lines": [
        ("added", "Pricing hypotheses PH-1 (per-production) and PH-2 (per-season)", "from E1, C2"),
        ("dropped", "Channel C4 (app stores)", "gatekeeper cost exceeds season revenue")]},
    "", launched="2026-10-06T14:10")
rec("pass-14", "Growth", "audit", 5, SONNET, AGENT, "high", 9, 122_400, 4_100, 0,
    "Agent-tool usage",
    [("artifacts/05-economics-model.md", H(22)), ("artifacts/04-distribution-plan.md", H(19))],
    WITHHELD, ["audits/05-business-by-growth.md"], "logs/pass-14.jsonl",
    [], ["artifacts/05-economics-model.md"], None,
    "Stake: does the model price the loop it depends on? Yes.", launched="2026-10-06T14:48")
rec("pass-15", "Delivery", "draft", 6, SONNET, AGENT, "high", 31, 198_700, 24_200, 160_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("artifacts/03-metrics-evidence-plan.md", H(17)), ("artifacts/04-distribution-plan.md", H(19)), ("artifacts/05-economics-model.md", H(22)), ("corpus/delivery/shelf.md", H(23)), ("corpus/delivery/shape-up.md", H(24))],
    WITHHELD, ["artifacts/06-roadmap.md", "pc-eng-000.d10", "pc-eng-000.d11"], "logs/pass-15.jsonl",
    [("pass-16", "co-sign", "PASS"), ("pass-18", "audit", "PASS")],
    ["corpus/delivery/shape-up.md", "artifacts/05-economics-model.md", "artifacts/03-metrics-evidence-plan.md"],
    {"kept": 14, "added": 6, "split": 2, "merged": 0, "dropped": 1, "lines": [
        ("split", "OC-1a → KR-1 (median time-to-cast) and KR-2 (share of productions cast within a week)", "from OC-1a, M1, M2"),
        ("added", "Bets B1–B3 with appetites", "from PH-1, L1, O2")]},
    "Baseline pass of a shadow pair (pass-17 is the trial).", launched="2026-10-06T15:05")
rec("pass-16", "Strategist", "co-sign", 6, OPUS, AGENT, "high", 10, 117_300, 4_600, 0,
    "Agent-tool usage",
    [("artifacts/06-roadmap.md", H(25)), ("artifacts/01-strategy-pov.md", H(7))],
    WITHHELD, ["cosigns/06-okr-r1.md"], "logs/pass-16.jsonl",
    [], ["artifacts/06-roadmap.md", "artifacts/01-strategy-pov.md"], None,
    "Every key result passed against its outcome.", launched="2026-10-06T15:44")
rec("pass-17", "Delivery", "trial", 6, "HIDDEN", "HIDDEN", "high", 24, 171_900, 22_800, 0,
    "codex footer",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("artifacts/03-metrics-evidence-plan.md", H(17)), ("artifacts/04-distribution-plan.md", H(19)), ("artifacts/05-economics-model.md", H(22)), ("corpus/delivery/shelf.md", H(23)), ("corpus/delivery/shape-up.md", H(24))],
    WITHHELD, ["trials/06-roadmap-trial.md"], "logs/pass-17.txt",
    [], ["corpus/delivery/shape-up.md", "artifacts/05-economics-model.md"],
    {"kept": 13, "added": 5, "split": 1, "merged": 1, "dropped": 2, "lines": [
        ("split", "OC-1a → KR-1 and KR-2", "from OC-1a, M1, M2"),
        ("merged", "B2 + B3 → B2", "from PH-1, L1")]},
    "Shadow pass on identical inputs. Label blind.", shadow_of="pass-15", launched="2026-10-06T15:06")
rec("pass-18", "Business", "audit", 6, SONNET, AGENT, "high", 11, 126_800, 5_000, 0,
    "Agent-tool usage",
    [("artifacts/06-roadmap.md", H(25)), ("artifacts/05-economics-model.md", H(22))],
    WITHHELD, ["audits/06-delivery-by-business.md"], "logs/pass-18.jsonl",
    [], ["artifacts/06-roadmap.md"], None,
    "Stake: does the first bet pay for the second? Yes, on PH-1.", launched="2026-10-06T16:02")
rec("pass-19", "Red-team gate", "gate", 6, CODEX, CODEX_LAUNCH, "high", 8, 64_100, 3_900, 0,
    "codex footer",
    [("artifacts/06-handoff-brief.md", H(26)), ("templates/red-team-protocol.md", H(5))],
    WITHHELD + ["the corpus"], ["gates/g2-handoff-r1.md"], "logs/pass-19.txt",
    [], [], None, "Gate PASS. Brief crosses to Systemcraft with a return date.", launched="2026-10-06T16:30")
rec("pass-20", "Leadership", "draft", 7, OPUS, AGENT, "high", 33, 205_300, 26_100, 170_000,
    "Agent-tool usage",
    [("artifacts/01-strategy-pov.md", H(7)), ("artifacts/02-discovery-packet.md", H(14)), ("artifacts/03-metrics-evidence-plan.md", H(17)), ("artifacts/04-distribution-plan.md", H(19)), ("artifacts/05-economics-model.md", H(22)), ("artifacts/06-roadmap.md", H(25)), ("artifacts/06-handoff-brief.md", H(26)), ("corpus/leadership/shelf.md", H(27))],
    WITHHELD, ["artifacts/07-leadership-packet.md", "pc-eng-000.d12"], "logs/pass-20.jsonl",
    [("pass-21", "audit", "—")], ["corpus/leadership/shelf.md", "artifacts/06-handoff-brief.md", "artifacts/06-roadmap.md"],
    {"kept": 15, "added": 7, "split": 0, "merged": 0, "dropped": 0, "lines": [
        ("added", "Stakeholder rows: venue managers, the regional association, app-store review (gatekeeper)", "from C2, C4, E5"),
        ("added", "Team topology with two agents as their own entity type", "from B1–B3")]},
    "Grounding manifest-only.", launched="2026-10-06T16:50")
rec("pass-21", "Strategist", "audit", 7, OPUS, AGENT, "high", 12, 139_500, 5_700, 0,
    "Agent-tool usage",
    [("artifacts/07-leadership-packet.md", H(28)), ("artifacts/01-strategy-pov.md", H(7))],
    WITHHELD, ["audits/07-leadership-by-strategist.md"], "logs/pass-21.jsonl",
    [], ["artifacts/07-leadership-packet.md"], None,
    "Stake: does the operating model serve the guiding policy? One bounce on the decision-rights table.", launched="2026-10-06T17:35")
rec("pass-22", "Delivery", "audit", 3, SONNET, AGENT, "high", 10, 118_200, 4_400, 0,
    "Agent-tool usage",
    [("artifacts/03-metrics-evidence-plan.md", H(17)), ("artifacts/06-roadmap.md", H(25))],
    WITHHELD, ["audits/03-insights-by-delivery.md"], "logs/pass-22.jsonl",
    [], ["artifacts/03-metrics-evidence-plan.md"], None,
    "Stake: can the roadmap's key results be read off the plan's metrics? Yes for KR-1, KR-2; KR-3 has no metric.", launched="2026-10-06T17:58")
rec("pass-23", "Red-team gate", "gate", 7, CODEX, CODEX_LAUNCH, "high", 14, 92_600, 6_200, 0,
    "codex footer",
    [("artifacts/", H(29)), ("templates/red-team-protocol.md", H(5))],
    WITHHELD + ["the corpus"], ["gates/g3-close-r1.md"], "logs/pass-23.txt",
    [], [], None, "Gate at close. Anchor: the whole train.", launched="2026-10-06T18:20")
rec("pass-24", "Coordinator", "close", 0, "claude-fable-5-1 (interactive)", "interactive session", "—", 0, 0, 0, 0,
    "UNMEASURED",
    [], ["nothing"], ["engagement/close.md"], "—", [], [], None,
    "Coordinator's own session. Deviations: Growth and Leadership ran grounding manifest-only (corpus not yet ingested for those seats).",
    launched="2026-10-06T18:40")

LABELS = {
    "pass-01": ("pass", None, "Diagnosis is one sentence and names the constraint. A new hire could restate it.", ""),
    "pass-02": ("fail", 1, "Gate was right to fail it: the calendar assumption was load-bearing and unstated. The gate's own write-up buries the finding under three minor ones; lead with it.", ""),
    "pass-03": ("pass", None, "The split is honest and the register is testable. Dropping action 4 was correct.", ""),
    "pass-04": ("pass", None, "", ""),
    "pass-05": ("pass", None, "Reads the interviews rather than the brief's summary of them. Merge of O2 and O5 is defensible.", ""),
    "pass-06": ("fail", 2, "Right to bounce E2 and E4, but E4's bounce is the packet's fault, not the co-sign's; this row fails because the co-sign let E3 through with a count nobody can find in the transcripts.", ""),
    "pass-07": ("pass", None, "", ""),
    "pass-08": ("pass", None, "", ""),
    "pass-09": ("pass", None, "Bouncing OC-3 to the Strategist instead of inventing a metric is exactly the rule.", ""),
    "pass-10": ("pass", None, "", ""),
    "pass-11": ("pass", None, "Manifest-only grounding declared, not hidden. Loop L1 target has no metric, which surfaces at pass-12.", ""),
    "pass-12": ("fail", 3, "The audit is correct and the failure is upstream: the metrics plan (stage 3) has no acquisition metric, so Growth could not have measured L1. Fix the plan, not the loop.", ""),
    "pass-13": ("pass", None, "", ""),
    "pass-14": ("pass", None, "", ""),
    "pass-15": ("pass", None, "Appetites are stated in weeks with a circuit breaker each. KR-3 is unmeasured; see pass-22.", ""),
    "pass-16": ("pass", None, "", ""),
    "pass-17": (None, None, "", ""),
    "pass-18": ("pass", None, "", ""),
    "pass-19": ("pass", None, "", ""),
    "pass-20": ("fail", 6, "The stakeholder map is fine. The topology names a return date that the handoff brief (stage 6) never set, so the packet inherited a constraint that does not exist.", ""),
    "pass-21": (None, None, "", ""),
    "pass-22": (None, None, "", ""),
    "pass-23": ("pass", None, "", ""),
    "pass-24": ("pass", None, "", ""),
}

RUNG0 = [
    ("Every pass has a record", "24 of 24", True),
    ("Every pass has a label row", "21 of 24", False),
    ("Input hashes match disk", "24 of 24", True),
    ("Cited corpus files appear in the transcript's file reads", "22 of 22", True),
    ("Every move names an existing upstream item; splits are subsets", "31 of 31", True),
    ("Meter present or UNMEASURED", "24 of 24", True),
    ("Each drafting stage has one draft, one audit, required co-signs", "7 of 7", True),
    ("Trials blind-labeled before their runtime is shown", "0 of 1", False),
]

ENG = dict(id="pc-eng-000", name="Callboard", kind="full train",
           opened="2026-10-06", closed="2026-10-06", pass_budget=26,
           note="Synthetic engagement, invented for the viewer design (#292). No seat wrote any of this.")

# ---------------------------------------------------------------------------


def esc(s):
    return html.escape(str(s), quote=True)


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def fmt_tokens(n):
    if n == 0:
        return "—"
    if n >= 1000:
        return f"{n / 1000:.0f}k"
    return str(n)


def fmt_minutes(s):
    if s == 0:
        return "—"
    m = s // 60
    return f"{m} min"


def stage_name(n):
    return "Close" if n == 0 else STAGES[n][0]


def icon(name, cls=""):
    return f'<svg class="ico {cls}" aria-hidden="true" width="14" height="14" viewBox="0 0 14 14"><use href="#i-{name}"/></svg>'


def label_of(pid):
    v, ffs, crit, code = LABELS.get(pid, (None, None, "", ""))
    return v, ffs, crit, code


def blind_pairs():
    pairs = {}
    for p in P:
        if p["shadow_of"]:
            pairs[p["pass_id"]] = p["shadow_of"]
            pairs[p["shadow_of"]] = p["pass_id"]
    return pairs


def build():
    pairs = blind_pairs()
    total = len(P)
    labeled = [pid for pid in LABELS if LABELS[pid][0]]
    n_pass = sum(1 for pid in labeled if LABELS[pid][0] == "pass")
    n_fail = sum(1 for pid in labeled if LABELS[pid][0] == "fail")
    n_unl = total - len(labeled)
    rung0_clean = sum(1 for _, _, ok in RUNG0 if ok)

    # matrix: rows = last good stage (first_failing_stage - 1), cols = first failing stage
    matrix = {}
    fails = []
    for p in P:
        v, ffs, crit, _ = label_of(p["pass_id"])
        if v == "fail" and ffs:
            matrix[(ffs - 1, ffs)] = matrix.get((ffs - 1, ffs), 0) + 1
            fails.append((p, ffs, crit))
    # Note: last-good is derived as first_failing_stage - 1 because the studio's
    # train is linear; a non-linear pipeline would carry last_good on the label.
    maxcell = max(matrix.values()) if matrix else 1

    # per-stage counts
    per_stage = {}
    for p in P:
        s = p["stage"]
        d = per_stage.setdefault(s, dict(passes=0, ok=0, fail=0, unl=0))
        d["passes"] += 1
        v = label_of(p["pass_id"])[0]
        if v == "pass":
            d["ok"] += 1
        elif v == "fail":
            d["fail"] += 1
        else:
            d["unl"] += 1

    # bounce loops
    loops = [(p["pass_id"], p["triggered_by"]) for p in P if p["triggered_by"]]

    fonts_css = f"""
@font-face {{ font-family: 'Anybody'; font-style: normal; font-weight: 100 900; font-stretch: 50% 150%; font-display: swap;
  src: url(data:font/woff2;base64,{b64(TRACE / 'fonts' / 'anybody-latin-wdth-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: 'Schibsted Grotesk'; font-style: normal; font-weight: 400 900; font-display: swap;
  src: url(data:font/woff2;base64,{b64(TRACE / 'fonts' / 'schibsted-grotesk-latin-wght-normal.woff2')}) format('woff2'); }}
"""

    css = r"""
/* ---- tokens: portfolio DESIGN.md §2 / §2.1 / §4, verbatim ---- */
:root {
  --ground: #FBF6EC; --ink: #2A2622; --sub: #6E655B; --accent: #2F5D7C;
  --ink-hairline: color-mix(in srgb, var(--ink) 14%, transparent);
  --ink-wash-1: color-mix(in srgb, var(--ink) 6%, transparent);
  --ink-wash-2: color-mix(in srgb, var(--ink) 16%, transparent);
  --ink-wash-3: color-mix(in srgb, var(--ink) 30%, transparent);
  --ink-wash-4: color-mix(in srgb, var(--ink) 48%, transparent);
  --ground-cased: color-mix(in srgb, var(--ground) 88%, transparent);
  --font-display: 'Anybody', system-ui, sans-serif;
  --font-body: 'Schibsted Grotesk', system-ui, sans-serif;
  --fs-0: 0.8125rem; --fs-1: 0.9375rem; --fs-2: 1.0625rem; --fs-3: 1.25rem; --fs-4: 1.625rem; --fs-5: 2.375rem;
  --measure: 68ch; --gutter: 1.5rem; --row-x: 0.75rem;
  color-scheme: light;
}
:root[data-mode='dark'] { --ground: #191714; --ink: #F2EBDD; --sub: #8F867A; --accent: #6BA3C9; color-scheme: dark; }
@media (prefers-color-scheme: dark) { :root:not([data-mode='light']) { --ground: #191714; --ink: #F2EBDD; --sub: #8F867A; --accent: #6BA3C9; color-scheme: dark; } }

html { font-size: 16px; }
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--font-body); font-size: var(--fs-1); line-height: 1.5;
  -webkit-font-smoothing: antialiased; }
::selection { background: color-mix(in srgb, var(--accent) 22%, transparent); }
a { color: inherit; text-decoration: none; background-image: linear-gradient(var(--accent), var(--accent)); background-size: 0% 1px; background-repeat: no-repeat; background-position: 0 100%; }
a:hover, a:focus-visible { background-size: 100% 1px; outline: none; }
:focus-visible { outline: none; box-shadow: 0 2px 0 0 var(--accent); }
button, select, textarea, input { font: inherit; color: inherit; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 900; font-stretch: 95%; text-transform: uppercase; letter-spacing: -0.01em; line-height: 1; margin: 0; text-wrap: balance; }
h1 { font-size: var(--fs-5); }
h2 { font-size: var(--fs-4); margin-top: 3.5rem; margin-bottom: 1rem; }
h3 { font-size: var(--fs-2); letter-spacing: 0; margin-top: 1.5rem; margin-bottom: 0.5rem; }
p { margin: 0 0 0.75rem; max-width: var(--measure); }
.sub { color: var(--sub); }
.mono, .matrix, .stages .n, .counter, .mast .meta, .pass summary .wc, .pass summary .tok, .pass summary .pid, .detail dd, .rung .n, .train svg { font-variant-numeric: tabular-nums; }
.page { max-width: 1180px; margin: 0 auto; padding: 2.5rem var(--gutter) 5rem; }

/* masthead */
.mast { display: grid; grid-template-columns: 1fr auto; gap: 1rem 2rem; align-items: end; padding-bottom: 1.25rem; border-bottom: 1px solid var(--ink); }
.mast .meta { color: var(--sub); font-size: var(--fs-0); margin-top: 0.5rem; }
.mast .meta span + span::before { content: " · "; color: var(--sub); }
.tools { display: flex; gap: 0.5rem; align-items: center; }
.btn { border: 1px solid var(--ink); background: transparent; padding: 0.3rem 0.7rem; font-size: var(--fs-0); cursor: pointer; border-radius: 2px; }
.btn:hover { background: var(--ink-wash-1); }
.btn[aria-pressed='true'] { background: var(--ink); color: var(--ground); }
.btn:disabled { opacity: 0.45; cursor: default; }
.synthetic { display: inline-block; border: 1px solid var(--ink); padding: 0 0.4rem; font-size: var(--fs-0); text-transform: uppercase; letter-spacing: 0.04em; margin-left: 0.5rem; vertical-align: middle; }

/* reading line */
.reading { font-size: var(--fs-3); line-height: 1.4; max-width: 60ch; margin: 1.75rem 0 0; }
.reading strong { font-weight: 700; }
.counter { display: flex; gap: 1.25rem; align-items: baseline; margin-top: 0.75rem; color: var(--sub); font-size: var(--fs-0); flex-wrap: wrap; }
.counter b { color: var(--ink); font-weight: 600; }
.track { height: 4px; background: var(--ink-wash-1); width: 220px; position: relative; top: -2px; }
.track i { display: block; height: 100%; background: var(--ink); }
.track i.draft { background: var(--ink-wash-3); }

/* where it broke */
.broke { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: 2.5rem; align-items: start; }
.matrix { border-collapse: collapse; font-size: var(--fs-0); }
.matrix th, .matrix td { padding: 0; text-align: center; font-weight: 400; }
.matrix thead th { color: var(--sub); padding-bottom: 0.35rem; font-size: var(--fs-0); }
.matrix tbody th { text-align: right; padding-right: 0.6rem; color: var(--sub); white-space: nowrap; }
.matrix td { width: 2.6rem; height: 2.3rem; border: 1px solid var(--ground); }
.matrix td span { display: grid; place-items: center; width: 100%; height: 100%; }
.matrix td.z span { color: var(--ink-wash-3); }
.matrix td.c1 span { background: var(--ink-wash-2); }
.matrix td.c2 span { background: var(--ink-wash-3); }
.matrix td.c3 span { background: var(--ink-wash-3); font-weight: 700; box-shadow: inset 0 0 0 1px var(--ink); }
.matrix td.na span { background: repeating-linear-gradient(135deg, transparent 0 3px, var(--ink-wash-1) 3px 4px); }
.matrix .cap { text-align: left; color: var(--sub); font-size: var(--fs-0); padding-top: 0.6rem; max-width: 40ch; }
.axis { font-size: var(--fs-0); color: var(--sub); }
.stages { list-style: none; margin: 1.5rem 0 0; padding: 0; display: grid; gap: 0.4rem; }
.stages li { display: grid; grid-template-columns: 7.5rem 1fr auto; align-items: center; gap: 0.75rem; font-size: var(--fs-0); }
.stages .bar { display: flex; gap: 2px; height: 10px; }
.stages .bar i { display: block; height: 100%; }
.stages .bar .ok { background: var(--ink-wash-3); }
.stages .bar .fail { background: var(--ink); }
.stages .bar .unl { background: transparent; border: 1px dashed var(--ink-wash-3); box-sizing: border-box; }
.stages .n { color: var(--sub); white-space: nowrap; }
.legend { display: flex; gap: 1rem; color: var(--sub); font-size: var(--fs-0); margin-top: 0.5rem; }
.legend i { display: inline-block; width: 10px; height: 10px; vertical-align: -1px; margin-right: 0.3rem; }
.fails { list-style: none; margin: 0; padding: 0; }
.fails li { display: grid; grid-template-columns: 7.5rem 1fr; gap: 0.75rem; padding: 0.7rem 0; border-top: 1px solid var(--ink-hairline); }
.fails li:first-child { border-top: 0; padding-top: 0; }
.fails .who { font-size: var(--fs-0); color: var(--sub); }
.fails .who b { display: block; color: var(--ink); font-weight: 600; }
.fails .why { font-size: var(--fs-1); }
.fails .why small { display: block; color: var(--sub); font-size: var(--fs-0); margin-top: 0.15rem; }
.rung { list-style: none; margin: 0.5rem 0 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem 2rem; font-size: var(--fs-0); }
.rung li { display: grid; grid-template-columns: 1rem 1fr auto; gap: 0.5rem; align-items: baseline; }
.rung .n { color: var(--sub); }

/* train */
.train { overflow-x: auto; }
.train svg { display: block; font-family: var(--font-body); font-size: 12px; }
.train .grid line { stroke: var(--ink-hairline); }
.train .lane { stroke: var(--ink-wash-2); }
.train text { fill: var(--sub); }
.train text.pid { fill: var(--ink); }
.train .m-draft { fill: var(--ink); }
.train .m-audit { fill: none; stroke: var(--ink); stroke-width: 1.5; }
.train .m-cosign { fill: none; stroke: var(--ink); stroke-width: 1.5; }
.train .m-gate { fill: var(--ground); stroke: var(--ink); stroke-width: 1.5; }
.train .m-repair { fill: var(--ink-wash-3); stroke: var(--ink); stroke-width: 1.5; }
.train .m-trial { fill: none; stroke: var(--ink); stroke-width: 1.5; stroke-dasharray: 2 2; }
.train .m-close { fill: var(--ink); }
.train .fail-ring { fill: none; stroke: var(--ink); stroke-width: 1.5; }
.train .loop { fill: none; stroke: var(--ink); stroke-width: 1.25; marker-end: url(#arrow); }
.train .shadow { stroke: var(--ink-wash-3); stroke-dasharray: 3 3; }
.train-legend { display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; color: var(--sub); font-size: var(--fs-0); margin-top: 0.5rem; }
.train-legend svg { vertical-align: -3px; margin-right: 0.3rem; }

/* passes */
.filters { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; margin-bottom: 0.75rem; font-size: var(--fs-0); color: var(--sub); }
.filters .btn { padding: 0.2rem 0.55rem; }
.passes { border-top: 1px solid var(--ink); }
.pass { border-bottom: 1px solid var(--ink-hairline); }
.pass summary { list-style: none; display: grid; grid-template-columns: 4.5rem 11rem 4.5rem 6rem 9rem 4rem 4rem 5.5rem 1fr; gap: 0 0.75rem; align-items: center; padding: 0.55rem var(--row-x); cursor: pointer; font-size: var(--fs-0); position: relative; }
.pass summary::-webkit-details-marker { display: none; }
.pass summary:hover { background: var(--ink-wash-1); }
.pass.current summary { box-shadow: inset 0 -2px 0 0 var(--accent); }
.pass summary .pid { font-weight: 600; color: var(--ink); }
.pass summary .kind { color: var(--sub); }
.pass summary .verdict { display: inline-flex; align-items: center; gap: 0.35rem; font-weight: 600; }
.pass summary .verdict.unl { color: var(--sub); font-weight: 400; }
.pass summary .crit { color: var(--sub); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pass.v-fail summary .crit { color: var(--ink); }
.pass summary .hidden-rt { color: var(--sub); font-style: italic; display: inline-flex; gap: 0.35rem; align-items: center; }
.pass summary .tag { border: 1px solid var(--ink-hairline); padding: 0 0.3rem; margin-left: 0.3rem; font-size: 0.75rem; color: var(--sub); white-space: nowrap; display: inline-flex; gap: 0.2rem; align-items: center; }
.pass[open] summary { background: var(--ink-wash-1); }
.pass[open] summary .kind, .pass[open] summary .crit, .pass[open] summary .hidden-rt { color: var(--ink); }
.detail { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 1.25rem 2.5rem; padding: 0.75rem var(--row-x) 1.5rem calc(var(--row-x) + 4.5rem + 0.75rem); font-size: var(--fs-0); }
.detail h4 { font-family: var(--font-body); font-size: var(--fs-0); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--sub); margin: 0 0 0.35rem; }
.detail dl { margin: 0; display: grid; grid-template-columns: 8rem 1fr; gap: 0.2rem 0.75rem; }
.detail dt { color: var(--sub); }
.detail dd { margin: 0; overflow-wrap: anywhere; }
.detail ul { margin: 0; padding-left: 1rem; }
.detail li { margin: 0.1rem 0; }
.detail .hash { color: var(--sub); font-size: 0.75rem; margin-left: 0.4rem; }
.detail .moves li b { font-weight: 600; text-transform: lowercase; margin-right: 0.3rem; }
.detail .moves li small { color: var(--sub); }
.movecounts { display: flex; gap: 0.9rem; margin-bottom: 0.4rem; color: var(--sub); }
.movecounts b { color: var(--ink); font-weight: 600; }
.checks li { list-style: none; margin-left: -1rem; display: grid; grid-template-columns: 4.5rem 4.5rem 1fr; }
.label-form { grid-column: 1 / -1; border-top: 1px solid var(--ink-hairline); padding-top: 0.9rem; display: grid; grid-template-columns: auto auto 1fr; gap: 0.75rem 1.25rem; align-items: start; }
.label-form .verdicts { display: flex; gap: 0.35rem; }
.label-form .verdicts .btn { display: inline-flex; gap: 0.35rem; align-items: center; }
.label-form .verdicts .btn kbd { font-size: 0.75rem; color: var(--sub); border: 1px solid var(--ink-hairline); padding: 0 0.25rem; border-radius: 2px; }
.label-form .btn[aria-pressed='true'] kbd { color: var(--ground); border-color: var(--ground-cased); }
.label-form label { display: grid; gap: 0.25rem; color: var(--sub); }
.label-form select, .label-form textarea { background: transparent; border: 1px solid var(--ink-hairline); padding: 0.35rem 0.5rem; border-radius: 2px; color: var(--ink); }
.label-form textarea { width: 100%; min-height: 3.6rem; resize: vertical; box-sizing: border-box; }
.label-form select:focus, .label-form textarea:focus { border-color: var(--ink); box-shadow: none; }
.label-form .state { grid-column: 1 / -1; color: var(--sub); display: flex; gap: 1rem; align-items: center; }
.label-form .state .draft { color: var(--ink); }
.blind-note { grid-column: 1 / -1; color: var(--sub); }

/* slots */
.slots { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.5rem; }
.slot p { font-size: var(--fs-0); color: var(--sub); }
.slot .when { color: var(--ink); }
.notes { white-space: pre-wrap; font-size: var(--fs-1); max-width: var(--measure); }

footer { margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--ink); color: var(--sub); font-size: var(--fs-0); display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }

/* keyboard sheet */
dialog { background: var(--ground); color: var(--ink); border: 1px solid var(--ink); padding: 1.25rem 1.5rem; max-width: 26rem; font-size: var(--fs-0); }
dialog::backdrop { background: color-mix(in srgb, var(--ink) 30%, transparent); }
dialog dl { display: grid; grid-template-columns: auto 1fr; gap: 0.3rem 1rem; margin: 0.75rem 0 0; }
dialog kbd { border: 1px solid var(--ink-hairline); padding: 0 0.3rem; border-radius: 2px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }

@media (max-width: 900px) {
  .broke, .slots, .detail { grid-template-columns: 1fr; }
  .pass summary { grid-template-columns: 4.5rem 7rem 5rem 1fr; }
  .pass summary .wc, .pass summary .tok, .pass summary .rt, .pass summary .ffs, .pass summary .crit { display: none; }
}
@media print {
  :root { --ground: #FBF6EC; --ink: #2A2622; --sub: #6E655B; --accent: #2F5D7C; }
  html { font-size: 11px; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .tools, .filters, .label-form, .btn, dialog { display: none !important; }
  .pass, .fails li, .matrix, .stages, .train { break-inside: avoid; }
  .pass summary { cursor: default; }
  h2 { break-after: avoid; }
}
"""

    # -------- SVG symbols --------
    symbols = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-check" viewBox="0 0 14 14"><path d="M2.5 7.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-cross" viewBox="0 0 14 14"><path d="M3 3l8 8M11 3l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="i-open" viewBox="0 0 14 14"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 2"/></symbol>
  <symbol id="i-eye" viewBox="0 0 14 14"><path d="M1.5 7c1.6-2.6 3.4-3.8 5.5-3.8S10.9 4.4 12.5 7c-1.6 2.6-3.4 3.8-5.5 3.8S3.1 9.6 1.5 7z" fill="none" stroke="currentColor" stroke-width="1.3"/><circle cx="7" cy="7" r="1.6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M2.5 11.5l9-9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></symbol>
  <symbol id="i-loop" viewBox="0 0 14 14"><path d="M11 4H5a3 3 0 0 0 0 6h3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M9 2.5L11 4 9 5.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>"""

    # -------- masthead --------
    out = []
    out.append(f"""
<div class="page">
<!--
THESIS: one reader's desk sheet for one engagement; it refuses the span waterfall and the KPI-tile dashboard.
OWN-WORLD: the portfolio's dailies desk, verbatim tokens; ink-alpha carries magnitude, glyph and weight carry verdicts, the accent keeps its interaction-mark grammar only.
STORY: Sean reads the line, sees where the train broke, walks the rows, labels as he reads, exports rows.
FIRST VIEWPORT: masthead, the reading line, the labeling counter, then the first-failing-stage matrix beside the list of fails with their critiques.
FORM: one scrolling document with folded rows (confirmed by Sean 2026-09-11); seed n/a, prototype.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review and DESIGN.md.
-->
<header class="mast">
  <div>
    <h1>{esc(ENG['id'])} · {esc(ENG['name'])}<span class="synthetic">synthetic</span></h1>
    <div class="meta"><span>{esc(ENG['kind'])}</span><span>opened {esc(ENG['opened'])}</span><span>closed {esc(ENG['closed'])}</span><span>{total} passes of a {ENG['pass_budget']}-pass budget</span><span>rendered from 24 records, 21 label rows</span></div>
  </div>
  <div class="tools">
    <button class="btn" id="copy-labels" type="button" title="Copy every drafted label as rows for the labels file">Copy label rows <span id="draft-count"></span></button>
    <button class="btn" id="help" type="button" aria-haspopup="dialog">Keys <kbd>?</kbd></button>
    <button class="btn" id="mode" type="button" aria-pressed="false" aria-label="Switch to night studio">Night</button>
  </div>
</header>
""")

    # -------- reading line --------
    out.append(f"""
<p class="reading">Of <strong>{total} passes</strong>, <strong>{len(labeled)} are labeled</strong>: {n_pass} pass, {n_fail} fail. <strong>{n_unl} wait for a verdict.</strong> The train broke first at stage 1, then at stages 2, 3 and 6; the stage-3 break is the one that cost downstream work. Rung 0 is clean on {rung0_clean} of {len(RUNG0)} checks.</p>
<div class="counter" aria-live="polite">
  <span>Labeled <b id="labeled-n">{len(labeled)}</b> of {total}<span id="draft-note"></span></span>
  <span class="track" aria-hidden="true"><i id="track-file" style="width:{len(labeled) / total * 100:.0f}%"></i></span>
  <span>Next unlabeled: <a href="#pass-17" data-jump>pass-17</a></span>
</div>
""")

    # -------- where it broke --------
    cols = list(range(1, 8))
    rows = list(range(0, 7))
    th = "".join(f"<th scope='col'>{c}</th>" for c in cols)
    trs = []
    for r in rows:
        tds = []
        for c in cols:
            if c <= r:
                tds.append("<td class='na'><span></span></td>")
                continue
            n = matrix.get((r, c), 0)
            cls = "z" if n == 0 else ("c3" if n >= 3 else ("c2" if n == 2 else "c1"))
            tds.append(f"<td class='{cls}'><span>{n if n else '·'}</span></td>")
        trs.append(f"<tr><th scope='row'>{'start' if r == 0 else stage_name(r)} {'' if r == 0 else r}</th>{''.join(tds)}</tr>")
    matrix_html = f"""
<table class="matrix" aria-describedby="matrix-cap">
  <caption class="sr">Transition failures: rows are the last good stage, columns the first failing stage, cells are counts.</caption>
  <thead><tr><th scope="col" class="axis">last good ↓ · first failing →</th>{th}</tr></thead>
  <tbody>{''.join(trs)}</tbody>
</table>
<p class="cap" id="matrix-cap">Counts of labeled fails. {n_fail} fails so far, which is too few for a heat: read the numbers. Hatched cells cannot occur in a linear train.</p>
"""
    stage_rows = []
    for s in range(1, 8):
        d = per_stage.get(s, dict(passes=0, ok=0, fail=0, unl=0))
        w = 14
        bar = "".join(f"<i class='ok' style='width:{w}px' title='pass'></i>" for _ in range(d["ok"])) + \
              "".join(f"<i class='fail' style='width:{w}px' title='fail'></i>" for _ in range(d["fail"])) + \
              "".join(f"<i class='unl' style='width:{w}px' title='unlabeled'></i>" for _ in range(d["unl"]))
        stage_rows.append(f"<li><span>{s} {stage_name(s)}</span><span class='bar' aria-hidden='true'>{bar}</span><span class='n'>{d['ok']} pass · {d['fail']} fail{' · ' + str(d['unl']) + ' open' if d['unl'] else ''}</span></li>")
    stages_html = f"""
<h3>Passes per stage</h3>
<ul class="stages">{''.join(stage_rows)}</ul>
<div class="legend"><span><i style="background:var(--ink-wash-3)"></i>pass</span><span><i style="background:var(--ink)"></i>fail</span><span><i style="border:1px dashed var(--ink-wash-3);box-sizing:border-box"></i>unlabeled</span></div>
"""
    fails_html = "".join(
        f"<li><div class='who'><b><a href='#{p['pass_id']}' data-jump>{p['pass_id']}</a></b>{esc(p['seat'])} {esc(p['kind'])}<br>broke at {ffs} {stage_name(ffs)}</div>"
        f"<div class='why'>{esc(crit)}<small>{'upstream of the pass read' if ffs < p['stage'] else 'at the pass read'}</small></div></li>"
        for p, ffs, crit in fails)
    rung_html = "".join(
        f"<li>{icon('check') if ok else icon('cross')}<span>{esc(name)}</span><span class='n'>{esc(n)}</span></li>" for name, n, ok in RUNG0)
    out.append(f"""
<h2>Where it broke</h2>
<div class="broke">
  <div>{matrix_html}{stages_html}</div>
  <div>
    <h3>The {n_fail} fails, first failure named</h3>
    <ul class="fails">{fails_html}</ul>
    <h3>Rung 0 checks</h3>
    <ul class="rung">{rung_html}</ul>
  </div>
</div>
""")

    # -------- train --------
    colx = {s: 150 + (s - 1) * 120 for s in range(1, 8)}
    colx[0] = 150 + 7 * 120
    rowh = 26
    top = 40
    svg_h = top + rowh * total + 20
    svg_w = colx[0] + 90
    idx = {p["pass_id"]: i for i, p in enumerate(P)}
    parts = [f'<svg viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" role="img" aria-labelledby="train-title">']
    parts.append('<title id="train-title">The train: every pass in order, on its stage.</title>')
    parts.append('<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L8 4 0 8z" fill="var(--ink)"/></marker></defs>')
    parts.append('<g class="grid">')
    for s in list(range(1, 8)) + [0]:
        x = colx[s]
        parts.append(f'<line x1="{x}" y1="{top - 10}" x2="{x}" y2="{svg_h - 10}"/>')
        parts.append(f'<text x="{x}" y="{top - 18}" text-anchor="middle">{"close" if s == 0 else f"{s} {stage_name(s)}"}</text>')
    parts.append('</g>')
    # lane through passes
    pts = []
    for i, p in enumerate(P):
        pts.append((colx[p["stage"]], top + i * rowh + rowh / 2))
    parts.append('<polyline class="lane" fill="none" points="' + " ".join(f"{x},{y}" for x, y in pts) + '"/>')
    # marks
    for i, p in enumerate(P):
        x, y = pts[i]
        v = label_of(p["pass_id"])[0]
        k = p["kind"]
        parts.append(f'<text class="pid" x="8" y="{y + 4}">{p["pass_id"]}</text>')
        parts.append(f'<text x="64" y="{y + 4}">{esc(p["seat"] if p["seat"] != "Red-team gate" else "gate")}</text>')
        if k == "draft":
            parts.append(f'<rect class="m-draft" x="{x - 5}" y="{y - 5}" width="10" height="10"/>')
        elif k == "repair":
            parts.append(f'<rect class="m-repair" x="{x - 5}" y="{y - 5}" width="10" height="10"/>')
        elif k == "audit":
            parts.append(f'<circle class="m-audit" cx="{x}" cy="{y}" r="5"/>')
        elif k == "co-sign":
            parts.append(f'<path class="m-cosign" d="M{x} {y - 6}L{x + 6} {y}L{x} {y + 6}L{x - 6} {y}Z"/>')
        elif k == "gate":
            parts.append(f'<path class="m-gate" d="M{x} {y - 6}L{x + 6} {y + 5}L{x - 6} {y + 5}Z"/>')
        elif k == "trial":
            parts.append(f'<rect class="m-trial" x="{x - 5}" y="{y - 5}" width="10" height="10"/>')
        else:
            parts.append(f'<circle class="m-close" cx="{x}" cy="{y}" r="4"/>')
        if v == "fail":
            parts.append(f'<circle class="fail-ring" cx="{x}" cy="{y}" r="10"/>')
        if v is None:
            parts.append(f'<text x="{x + 14}" y="{y + 4}">unlabeled</text>')
        if p["shadow_of"]:
            j = idx[p["shadow_of"]]
            off = 78 if v is None else 14
            parts.append(f'<line class="shadow" x1="{x + 8}" y1="{y}" x2="{x + off - 4}" y2="{y}"/><text x="{x + off}" y="{y + 4}">{"· " if v is None else ""}shadow of {p["shadow_of"]}</text>')
    # bounce loops
    for child, trig in loops:
        i, j = idx[child], idx[trig]
        x = pts[i][0]
        y1, y0 = pts[i][1], pts[j][1]
        parts.append(f'<path class="loop" d="M{x + 12} {y1} C {x + 46} {y1}, {x + 46} {y0}, {x + 12} {y0}"/>')
    parts.append('</svg>')
    out.append(f"""
<h2>The train</h2>
<div class="train">{''.join(parts)}</div>
<div class="train-legend">
  <span><svg width="12" height="12"><rect x="1" y="1" width="10" height="10" fill="var(--ink)"/></svg>draft</span>
  <span><svg width="12" height="12"><rect x="1" y="1" width="10" height="10" fill="var(--ink-wash-3)" stroke="var(--ink)" stroke-width="1.5"/></svg>repair</span>
  <span><svg width="12" height="12"><circle cx="6" cy="6" r="4.5" fill="none" stroke="var(--ink)" stroke-width="1.5"/></svg>audit</span>
  <span><svg width="12" height="12"><path d="M6 0.5L11.5 6 6 11.5 0.5 6Z" fill="none" stroke="var(--ink)" stroke-width="1.5"/></svg>co-sign</span>
  <span><svg width="12" height="12"><path d="M6 1L11.5 11H0.5Z" fill="var(--ground)" stroke="var(--ink)" stroke-width="1.5"/></svg>gate</span>
  <span><svg width="12" height="12"><rect x="1" y="1" width="10" height="10" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="2 2"/></svg>trial</span>
  <span><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="none" stroke="var(--ink)" stroke-width="1.5"/></svg>labeled fail</span>
  <span><svg width="22" height="12"><path d="M2 6 C 12 6, 12 1, 20 1" fill="none" stroke="var(--ink)" stroke-width="1.25"/></svg>triggered by (a bounce loop)</span>
</div>
""")

    # -------- passes --------
    rows_html = []
    for p in P:
        pid = p["pass_id"]
        v, ffs, crit, code = label_of(pid)
        pair = pairs.get(pid)
        blind = False
        if pair:
            v2 = label_of(pair)[0]
            blind = not (v and v2)
        rt = p["runtime"]
        if blind:
            rt_html = f"<span class='hidden-rt'>{icon('eye')} hidden</span>"
        else:
            rt_html = esc(rt if rt != "HIDDEN" else "codex gpt-5.6-sol (high)")
        vcls = "unl" if not v else v
        vlabel = {"pass": "pass", "fail": "fail"}.get(v, "unlabeled")
        vicon = icon("check") if v == "pass" else (icon("cross") if v == "fail" else icon("open"))
        tags = ""
        if p["triggered_by"]:
            tags += f"<span class='tag'>{icon('loop')} {p['triggered_by']}</span>"
        if p["shadow_of"]:
            tags += f"<span class='tag'>shadow of {p['shadow_of']}</span>"
        if pair and not p["shadow_of"]:
            tags += f"<span class='tag'>baseline of {pair}</span>"
        m = p["meter"]
        tok = "—" if p["meter_source"] == "UNMEASURED" else f"{fmt_tokens(m['input'] + m['output'])}"
        summary = f"""
<summary>
  <span class="pid">{pid}</span>
  <span>{esc(p['seat'])}{tags}</span>
  <span class="kind">{esc(p['kind'])}</span>
  <span class="kind">{'close' if p['stage'] == 0 else f"{p['stage']} {stage_name(p['stage'])}"}</span>
  <span class="rt">{rt_html}</span>
  <span class="wc">{fmt_minutes(p['wall_clock_s'])}</span>
  <span class="tok" title="input + output tokens">{tok}</span>
  <span class="verdict {vcls}" data-verdict-cell>{vicon}<span data-verdict-word>{vlabel}</span></span>
  <span class="crit" data-crit-cell>{esc(crit) if crit else ('<span class="ffs">' + (f'broke at {ffs} {stage_name(ffs)}' if ffs else '') + '</span>')}</span>
</summary>"""
        inputs = "".join(f"<li>{esc(path)}<span class='hash'>{esc(h)}</span></li>" for path, h in p["inputs"]) or "<li class='sub'>none</li>"
        withheld = "".join(f"<li>{esc(w)}</li>" for w in p["withheld"])
        outputs = "".join(f"<li>{esc(o)}</li>" for o in p["outputs"])
        checks = "".join(f"<li><span>{esc(a)}</span><span class='sub'>{esc(b)}</span><span>{esc(c)}</span></li>" for a, b, c in p["checks"]) or "<li class='sub' style='display:block'>none recorded</li>"
        corpus = "".join(f"<li>{esc(c)}</li>" for c in p["corpus_read"]) or "<li class='sub'>none (gate: corpus withheld)</li>"
        mv = p["moves"]
        if mv is None:
            moves = "<p class='sub' style='font-size:inherit'>No moves: this kind does not hand an artifact forward.</p>"
        elif mv.get("origin"):
            moves = "<p class='sub' style='font-size:inherit'>Origin draft, no upstream. Leaned on: " + "; ".join(esc(x) for x in mv["leaned_on"]) + "</p>"
        else:
            counts = " ".join(f"<span><b>{mv[k]}</b> {k}</span>" for k in ("kept", "added", "split", "merged", "dropped"))
            lines = "".join(f"<li><b>{esc(op)}</b>{esc(what)} <small>· {esc(src)}</small></li>" for op, what, src in mv["lines"])
            moves = f"<div class='movecounts'>{counts}</div><ul class='moves'>{lines}</ul><p class='sub' style='font-size:inherit;margin-top:0.4rem'>Kept items are listed in the artifact's Moves section, not here.</p>"
        meter_html = ("UNMEASURED" if p["meter_source"] == "UNMEASURED" else
                      f"{m['input']:,} in · {m['output']:,} out · {m['cached']:,} cached <span class='sub'>({esc(p['meter_source'])})</span>")
        launch = esc(p["launch"] if not (blind and p["shadow_of"]) else "hidden with the runtime")
        effort = esc(p["effort"])
        ffs_opts = "".join(f"<option value='{s}'{' selected' if ffs == s else ''}>{s} {stage_name(s)}</option>" for s in range(1, 8))
        blind_note = f"<p class='blind-note'>{icon('eye')} Blind pair with {pair}: the runtime and launch form stay hidden until both passes carry a verdict.</p>" if blind else ""
        form = f"""
<div class="label-form" data-label-form data-pass="{pid}">
  <div>
    <h4>Verdict</h4>
    <div class="verdicts" role="group" aria-label="Verdict for {pid}">
      <button class="btn" type="button" data-set-verdict="pass" aria-pressed="{'true' if v == 'pass' else 'false'}">{icon('check')} pass <kbd>1</kbd></button>
      <button class="btn" type="button" data-set-verdict="fail" aria-pressed="{'true' if v == 'fail' else 'false'}">{icon('cross')} fail <kbd>2</kbd></button>
    </div>
  </div>
  <label>First failing stage <kbd style="font-size:0.75rem">f</kbd>
    <select data-ffs {'disabled' if v != 'fail' else ''}><option value="">—</option>{ffs_opts}</select>
  </label>
  <label>Critique, one to three sentences a new hire could act on <kbd style="font-size:0.75rem">c</kbd>
    <textarea data-crit rows="2">{esc(crit)}</textarea>
  </label>
  {blind_note}
  <div class="state"><span data-state>{'In the labels file.' if v else 'No label row yet.'}</span><span class="sub">failure_code stays blank until a taxonomy exists.</span></div>
</div>"""
        detail = f"""
<div class="detail">
  <div>
    <h4>Record</h4>
    <dl>
      <dt>launched</dt><dd>{esc(p['launched'] or '—')}</dd>
      <dt>runtime</dt><dd>{rt_html}</dd>
      <dt>launch form</dt><dd>{launch}</dd>
      <dt>effort</dt><dd>{effort}</dd>
      <dt>wall-clock</dt><dd>{fmt_minutes(p['wall_clock_s'])}</dd>
      <dt>meter</dt><dd>{meter_html}</dd>
      <dt>raw log</dt><dd>{esc(p['raw_log'])}</dd>
    </dl>
    <h4 style="margin-top:1rem">Inputs, hashed</h4><ul>{inputs}</ul>
    <h4 style="margin-top:1rem">Withheld</h4><ul>{withheld}</ul>
    <h4 style="margin-top:1rem">Outputs</h4><ul>{outputs}</ul>
  </div>
  <div>
    <h4>Checks on this pass</h4><ul class="checks">{checks}</ul>
    <h4 style="margin-top:1rem">Corpus read (from the transcript)</h4><ul>{corpus}</ul>
    <h4 style="margin-top:1rem">Moves</h4>{moves}
    <h4 style="margin-top:1rem">Notes</h4><p style="font-size:inherit">{esc(p['notes']) or '<span class="sub">none</span>'}</p>
  </div>
  {form}
</div>"""
        rows_html.append(f'<details class="pass v-{vcls}" id="{pid}" data-pass="{pid}" data-kind="{p["kind"]}" data-verdict="{v or "unlabeled"}" data-pair="{pair or ""}">{summary}{detail}</details>')
    out.append(f"""
<h2>Passes</h2>
<div class="filters">
  <span>Show</span>
  <button class="btn" type="button" data-filter="all" aria-pressed="true">all {total}</button>
  <button class="btn" type="button" data-filter="fail" aria-pressed="false">fails {n_fail}</button>
  <button class="btn" type="button" data-filter="unlabeled" aria-pressed="false">unlabeled {n_unl}</button>
  <button class="btn" type="button" data-filter="pairs" aria-pressed="false">shadow pairs 1</button>
  <span style="margin-left:auto">Columns: runtime · wall-clock · tokens in+out · verdict · critique. <kbd>j</kbd>/<kbd>k</kbd> walk rows, <kbd>enter</kbd> opens.</span>
</div>
<div class="passes" id="passes">{''.join(rows_html)}</div>
""")

    # -------- slots --------
    out.append("""
<h2>What comes later</h2>
<div class="slots">
  <div class="slot"><h3>Failure taxonomy</h3><p><span class="when">Arrives after about thirty labels</span>, when the critiques get grouped into named failure modes with counts. Until then this slot lists nothing and the failure_code column stays blank.</p></div>
  <div class="slot"><h3>Judge results</h3><p><span class="when">Arrives per failure mode</span>, only after a mode recurs across engagements with thirty to fifty labeled examples per class and a judge is validated against the labels on a held-out split. A judge's verdict will sit beside the human one in each row, never replace it.</p></div>
  <div class="slot"><h3>Process notes</h3><p><span class="when">Sean's notes for this engagement</span>, read from the engagement's notes file when it exists. What he noticed while reading, what he would run differently, what to watch next time.</p>
  <div class="notes">No notes file yet.</div></div>
</div>
<footer>
  <span>Rendered 2026-09-11 from 24 records and 21 label rows. The records are the truth; this page is a view of them.</span>
  <span>productcraft/trace · viewer prototype for #292</span>
</footer>
</div>
<dialog id="keys" aria-labelledby="keys-title">
  <h3 id="keys-title" style="margin-top:0">Keys</h3>
  <dl>
    <dt><kbd>j</kbd> <kbd>k</kbd></dt><dd>next / previous pass</dd>
    <dt><kbd>enter</kbd></dt><dd>open or fold the current pass</dd>
    <dt><kbd>1</kbd> <kbd>2</kbd></dt><dd>label the current pass pass / fail</dd>
    <dt><kbd>f</kbd></dt><dd>first failing stage</dd>
    <dt><kbd>c</kbd></dt><dd>critique</dd>
    <dt><kbd>u</kbd></dt><dd>jump to the next unlabeled pass</dd>
    <dt><kbd>esc</kbd></dt><dd>leave a field</dd>
    <dt><kbd>?</kbd></dt><dd>this sheet</dd>
  </dl>
  <form method="dialog" style="margin-top:1rem"><button class="btn" type="submit">Close</button></form>
</dialog>
""")

    js = r"""
(function () {
  const ENG = 'pc-eng-000';
  const KEY = 'trace-labels:' + ENG;
  const root = document.documentElement;
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));

  // ---- theme ----
  const modeBtn = $('#mode');
  const applyMode = (m) => { if (m) root.dataset.mode = m; else delete root.dataset.mode;
    const dark = m === 'dark' || (!m && matchMedia('(prefers-color-scheme: dark)').matches);
    modeBtn.setAttribute('aria-pressed', String(dark)); modeBtn.textContent = dark ? 'Day' : 'Night';
    modeBtn.setAttribute('aria-label', dark ? 'Switch to dailies desk' : 'Switch to night studio'); };
  let mode = null; try { mode = localStorage.getItem('trace-mode'); } catch (e) {}
  applyMode(mode);
  modeBtn.addEventListener('click', () => { const dark = modeBtn.getAttribute('aria-pressed') === 'true';
    mode = dark ? 'light' : 'dark'; try { localStorage.setItem('trace-mode', mode); } catch (e) {} applyMode(mode); });

  // ---- drafts ----
  let drafts = {}; try { drafts = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { drafts = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(drafts)); } catch (e) {} };
  const rows = $$('details.pass');
  const fileVerdict = (row) => row.dataset.verdict === 'unlabeled' ? null : row.dataset.verdict;
  const effVerdict = (row) => (drafts[row.dataset.pass] && drafts[row.dataset.pass].verdict) || fileVerdict(row);

  function paint(row) {
    const pid = row.dataset.pass, d = drafts[pid] || {};
    const v = effVerdict(row);
    const cell = $('[data-verdict-cell]', row), word = $('[data-verdict-word]', row);
    cell.className = 'verdict ' + (v || 'unl');
    word.textContent = v || 'unlabeled';
    const ico = $('svg use', cell); ico.setAttribute('href', v === 'pass' ? '#i-check' : v === 'fail' ? '#i-cross' : '#i-open');
    row.classList.toggle('v-fail', v === 'fail'); row.classList.toggle('v-pass', v === 'pass'); row.classList.toggle('v-unl', !v);
    $$('[data-set-verdict]', row).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setVerdict === v)));
    const sel = $('[data-ffs]', row); sel.disabled = v !== 'fail'; if (d.ffs !== undefined) sel.value = d.ffs;
    const ta = $('[data-crit]', row); if (d.crit !== undefined && document.activeElement !== ta) ta.value = d.crit;
    const critCell = $('[data-crit-cell]', row); const crit = d.crit !== undefined ? d.crit : ta.value;
    if (crit) critCell.textContent = crit;
    const st = $('[data-state]', row);
    st.innerHTML = d.verdict || d.crit !== undefined || d.ffs !== undefined ? '<span class="draft">Drafted here, not yet in the labels file.</span>' : (fileVerdict(row) ? 'In the labels file.' : 'No label row yet.');
  }
  function paintBlind() {
    rows.forEach(row => { const pair = row.dataset.pair; if (!pair) return;
      const other = document.getElementById(pair); const both = effVerdict(row) && effVerdict(other);
      $$('.rt, dd', row).forEach(() => {}); // runtime reveal needs the real value, which the prototype does not embed for the trial.
      if (both) $$('.hidden-rt', row).forEach(el => { el.outerHTML = '<span>revealed on commit (see DESIGN.md)</span>'; });
    });
  }
  function counters() {
    const fileN = rows.filter(fileVerdict).length;
    const draftN = rows.filter(r => !fileVerdict(r) && drafts[r.dataset.pass] && drafts[r.dataset.pass].verdict).length;
    $('#labeled-n').textContent = fileN;
    $('#draft-note').textContent = draftN ? ` in the file, ${draftN} drafted here` : '';
    const nDraft = Object.keys(drafts).length; $('#draft-count').textContent = nDraft ? `(${nDraft})` : '';
    $('#copy-labels').disabled = !nDraft;
  }
  rows.forEach(row => {
    paint(row);
    $$('[data-set-verdict]', row).forEach(b => b.addEventListener('click', () => setVerdict(row, b.dataset.setVerdict)));
    $('[data-ffs]', row).addEventListener('change', e => { drafts[row.dataset.pass] = Object.assign({}, drafts[row.dataset.pass], { ffs: e.target.value }); save(); paint(row); counters(); });
    $('[data-crit]', row).addEventListener('input', e => { drafts[row.dataset.pass] = Object.assign({}, drafts[row.dataset.pass], { crit: e.target.value }); save(); paint(row); counters(); });
  });
  function setVerdict(row, v) { const pid = row.dataset.pass; const cur = effVerdict(row);
    drafts[pid] = Object.assign({}, drafts[pid], { verdict: v === cur && !fileVerdict(row) ? null : v }); if (!drafts[pid].verdict) delete drafts[pid].verdict;
    if (!Object.keys(drafts[pid]).length) delete drafts[pid]; save(); paint(row); paintBlind(); counters(); }
  counters(); paintBlind();

  // ---- export ----
  $('#copy-labels').addEventListener('click', async () => {
    const lines = ['| pass | verdict | first_failing_stage | critique | failure_code |', '|---|---|---|---|---|'];
    rows.forEach(row => { const d = drafts[row.dataset.pass]; if (!d) return; const v = d.verdict || fileVerdict(row) || '';
      lines.push(`| ${row.dataset.pass} | ${v} | ${v === 'fail' ? (d.ffs || '') : ''} | ${(d.crit || $('[data-crit]', row).value).replace(/\|/g, '\\|').replace(/\n/g, ' ')} |  |`); });
    const text = lines.join('\n');
    try { await navigator.clipboard.writeText(text); } catch (e) { window.prompt('Copy these rows', text); }
    const b = $('#copy-labels'); const t = b.firstChild.textContent; b.firstChild.textContent = 'Copied '; setTimeout(() => { b.firstChild.textContent = t; }, 1200);
  });

  // ---- filters ----
  $$('[data-filter]').forEach(b => b.addEventListener('click', () => {
    $$('[data-filter]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    const f = b.dataset.filter;
    rows.forEach(r => { const v = effVerdict(r);
      r.hidden = !(f === 'all' || (f === 'fail' && v === 'fail') || (f === 'unlabeled' && !v) || (f === 'pairs' && r.dataset.pair)); });
  }));

  // ---- keyboard ----
  let cur = -1;
  const visible = () => rows.filter(r => !r.hidden);
  function setCur(i) { const vis = visible(); if (!vis.length) return; i = Math.max(0, Math.min(vis.length - 1, i));
    rows.forEach(r => r.classList.remove('current')); vis[i].classList.add('current'); cur = rows.indexOf(vis[i]);
    vis[i].scrollIntoView({ block: 'nearest' }); $('summary', vis[i]).focus({ preventScroll: true }); }
  const curRow = () => rows[cur];
  const inField = () => /^(TEXTAREA|SELECT|INPUT)$/.test(document.activeElement.tagName);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && inField()) { document.activeElement.blur(); if (curRow()) $('summary', curRow()).focus(); return; }
    if (inField() || e.metaKey || e.ctrlKey || e.altKey) return;
    const vis = visible(); const vi = vis.indexOf(curRow());
    switch (e.key) {
      case 'j': case 'ArrowDown': e.preventDefault(); setCur(vi + 1); break;
      case 'k': case 'ArrowUp': e.preventDefault(); setCur(vi - 1); break;
      case 'Enter': if (curRow() && document.activeElement === $('summary', curRow())) { e.preventDefault(); curRow().open = !curRow().open; } break;
      case '1': if (curRow()) setVerdict(curRow(), 'pass'); break;
      case '2': if (curRow()) setVerdict(curRow(), 'fail'); break;
      case 'f': if (curRow()) { e.preventDefault(); curRow().open = true; $('[data-ffs]', curRow()).focus(); } break;
      case 'c': if (curRow()) { e.preventDefault(); curRow().open = true; $('[data-crit]', curRow()).focus(); } break;
      case 'u': { e.preventDefault(); const next = vis.find((r, i) => i > vi && !effVerdict(r)) || vis.find(r => !effVerdict(r)); if (next) setCur(vis.indexOf(next)); break; }
      case '?': e.preventDefault(); $('#keys').showModal(); break;
    }
  });
  rows.forEach((r) => $('summary', r).addEventListener('focus', () => { rows.forEach(x => x.classList.remove('current')); r.classList.add('current'); cur = rows.indexOf(r); }));
  $('#help').addEventListener('click', () => $('#keys').showModal());
  $$('[data-jump]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href').slice(1); const row = document.getElementById(id); if (!row) return; e.preventDefault(); row.open = true; setCur(rows.indexOf(row)); }));

  // ---- print: unfold everything, restore after ----
  let wasOpen = [];
  window.addEventListener('beforeprint', () => { wasOpen = rows.map(r => r.open); rows.forEach(r => r.open = true); });
  window.addEventListener('afterprint', () => { rows.forEach((r, i) => r.open = wasOpen[i]); });
})();
"""

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(ENG['id'])} · {esc(ENG['name'])} · eval</title>
<style>{fonts_css}{css}</style>
</head>
<body>
{symbols}
{''.join(out)}
<script>{js}</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    (OUT.parent / "synthetic-data.json").write_text(json.dumps(dict(engagement=ENG, stages={k: v[0] for k, v in STAGES.items()}, passes=P, labels={k: dict(verdict=v[0], first_failing_stage=v[1], critique=v[2], failure_code=v[3]) for k, v in LABELS.items()}, rung0=RUNG0), indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
