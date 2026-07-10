# council/discovery/dashboard_render.py
"""D3 dashboard HTML: Python-built inline SVG + CSS, zero JS, one self-contained file.
Honesty rules: a global thin badge under THIN_THRESHOLD runs; missing metrics render as
explicit n/a markers (pre-E1 / pre-E4 vintage), never zeros; skipped files are listed."""

import html
from pathlib import Path

from council.discovery.__main__ import DISCOVERY_DAILY_CAP, DISCOVERY_MONTHLY_CAP
from council.discovery.dashboard import (
    SpendDay, collector_yield, discrepancies, fuse_stats, month_totals, rerun_command,
)
from council.discovery.tiers import TIERS

THIN_THRESHOLD = 10

_CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:2rem auto;
     max-width:1100px;padding:0 1rem;background:#0f1115;color:#d7dae0}
h1{font-size:1.4rem} h2{font-size:1.05rem;margin-top:2rem;border-bottom:1px solid #2a2f3a;
     padding-bottom:.3rem} table{border-collapse:collapse;width:100%;font-size:.82rem}
th,td{padding:.35rem .5rem;text-align:left;border-bottom:1px solid #232833;vertical-align:top}
th{color:#8b93a5;font-weight:600} .na{color:#6a7285;font-style:italic}
.badge{display:inline-block;background:#5c4a00;color:#ffd75e;border-radius:4px;
       padding:.1rem .45rem;font-size:.75rem;margin-left:.5rem}
.ok{color:#7bd88f} .bad{color:#ff7a7a} .dim{color:#8b93a5;font-size:.78rem}
.bar{background:#1b202b;border-radius:3px;height:10px;width:180px;display:inline-block;
     vertical-align:middle;margin-right:.5rem}
.bar>i{display:block;height:100%;border-radius:3px;background:#4c8dff}
.bar>i.over{background:#ff7a7a}
pre{background:#161a22;border:1px solid #232833;border-radius:6px;padding:.5rem .7rem;
    font-size:.78rem;overflow-x:auto;white-space:pre-wrap}
footer{margin-top:2.5rem;color:#6a7285;font-size:.75rem}
"""


def _e(text) -> str:
    return html.escape(str(text))


def _na(label: str = "") -> str:
    return f'<span class="na">n/a{f" ({label})" if label else ""}</span>'


def _metric(session: dict, key: str, vintage: str, fmt=lambda v: f"{v}") -> str:
    """Missing key = the run predates the feature (honest vintage label);
    key present but None = the run degraded (plain n/a)."""
    if key not in session:
        return _na(vintage)
    value = session[key]
    return _na() if value is None else fmt(value)


def _cap_bar(amount: float, cap: float) -> str:
    pct = min(100.0, (amount / cap) * 100.0) if cap else 0.0
    over = " over" if amount > cap else ""
    return (f'<span class="bar"><i class="{over.strip()}" style="width:{pct:.0f}%"></i></span>'
            f"${amount:.2f}")


def _mini_bars(values: list[int], color: str = "#4c8dff") -> str:
    """Inline-SVG mini bar chart (verified/dropped trend)."""
    if not values:
        return _na()
    top = max(max(values), 1)
    width, gap, h = 9, 3, 26
    bars = []
    for i, v in enumerate(values):
        bh = max(1, round((v / top) * (h - 2)))
        bars.append(f'<rect x="{i * (width + gap)}" y="{h - bh}" width="{width}" '
                    f'height="{bh}" fill="{color}" rx="1"/>')
    total_w = len(values) * (width + gap)
    return f'<svg width="{total_w}" height="{h}" role="img">{"".join(bars)}</svg>'


def _tier_cap(tier: str) -> float | None:
    cfg = TIERS.get(tier)
    return cfg.max_cost_per_run if cfg else None


def _run_rows(sessions: list[dict]) -> str:
    rows = []
    for s in sessions:
        cap = _tier_cap(s.get("tier", ""))
        cost = s.get("cost_usd")
        cost_cell = (_na() if cost is None else
                     f"${cost:.2f}" + (f' <span class="dim">/ ${cap:.2f} cap</span>' if cap else ""))
        if s["_kind"] == "failure":
            status = f'<span class="bad">failed: {_e(s.get("failed_stage", "?"))}</span>'
        elif s["_kind"] == "empty":
            status = '<span class="dim">empty gather</span>'
        else:
            status = '<span class="ok">ok</span>'
        rows.append(f"""<tr>
<td>{_e(s["_date"] or "?")}</td><td>{_e(s.get("topic", ""))}</td>
<td>{_e(s.get("lens", ""))}/{_e(s.get("tier", ""))}</td>
<td>{_metric(s, "segment", "pre-fix run", lambda v: _e(v) if v else '<span class="dim">—</span>')}</td>
<td>{status}</td>
<td>{_metric(s, "evidence_count", "")}</td>
<td>{_metric(s, "verified", "")} / {_metric(s, "dropped", "")} / {_metric(s, "merged_count", "pre-E3 run")}</td>
<td>{_metric(s, "verify_mode", "pre-E1 run", _e)}</td>
<td>{_metric(s, "citation_precision", "pre-E1 run", lambda v: f"{v:.2f}")} /
    {_metric(s, "citation_recall", "pre-E1 run", lambda v: f"{v:.2f}")}</td>
<td>{_metric(s, "velocity_mode", "pre-E4 run", _e)}</td>
<td>{_metric(s, "why_now_coverage", "pre-E4 run", lambda v: f"{v * 100:.0f}%")}</td>
<td>{cost_cell}</td></tr>""")
    return "".join(rows)


def render_dashboard(sessions: list[dict], skipped_sessions: list[tuple[str, str]],
                     spend_days: list[SpendDay], skipped_spend: list[tuple[str, str]],
                     *, generated_at: str, sessions_dir: Path) -> str:
    n = len(sessions)
    thin = f'<span class="badge">⚠ thin: {n} runs</span>' if n < THIN_THRESHOLD else ""
    parts = [f"<style>{_CSS}</style>",
             f"<h1>fusion-discovery-council — run dashboard{thin}</h1>",
             f'<p class="dim">generated {_e(generated_at)} · {n} session(s) · '
             f"source: {_e(sessions_dir)}</p>"]

    if not sessions:
        parts.append(
            f"<p><b>No session history found</b> in <code>{_e(sessions_dir)}</code>. "
            "Runs before the persist-by-default fix (D3 Slice A) were not persisted; "
            "new runs will appear here automatically.</p>")

    # Spend vs caps
    parts.append(f"<h2>Spend vs caps <span class='dim'>(${DISCOVERY_DAILY_CAP:.2f}/day · "
                 f"${DISCOVERY_MONTHLY_CAP:.2f}/mo)</span></h2>")
    if spend_days:
        day_rows = "".join(
            f"<tr><td>{_e(d.date)}</td><td>{_cap_bar(d.discovery_total, DISCOVERY_DAILY_CAP)}</td>"
            f"<td class='dim'>{len(d.runs)} run(s)</td></tr>" for d in spend_days)
        parts.append(f"<table><tr><th>day</th><th>discovery spend vs $"
                     f"{DISCOVERY_DAILY_CAP:.2f}/day</th><th></th></tr>{day_rows}</table>")
        months = "".join(
            f"<tr><td>{_e(m)}</td><td>{_cap_bar(total, DISCOVERY_MONTHLY_CAP)}</td></tr>"
            for m, total in sorted(month_totals(spend_days).items()))
        parts.append(f"<table><tr><th>month</th><th>vs ${DISCOVERY_MONTHLY_CAP:.2f}/mo</th></tr>"
                     f"{months}</table>")
    else:
        parts.append("<p class='dim'>No discovery spend recorded in the ledgers.</p>")

    # Run history
    parts.append("<h2>Run history</h2>")
    if sessions:
        ok = [s for s in sessions if s["_kind"] == "success"]
        trend = (f"<p class='dim'>verified trend {_mini_bars([s.get('verified') or 0 for s in ok])}"
                 f" · dropped trend {_mini_bars([s.get('dropped') or 0 for s in ok], '#ff7a7a')}</p>"
                 if ok else "")
        parts.append(trend)
        parts.append("<table><tr><th>date</th><th>topic</th><th>lens/tier</th><th>segment</th>"
                     "<th>status</th><th>evidence</th><th>verified/dropped/merged</th>"
                     "<th>verify</th><th>citation P/R</th><th>velocity</th>"
                     "<th>why-now coverage</th><th>cost</th></tr>"
                     f"{_run_rows(sessions)}</table>")

    # Pipeline health
    parts.append("<h2>Pipeline health</h2>")
    stats = fuse_stats(sessions)
    rate = "n/a" if stats["rate"] is None else f"{stats['rate'] * 100:.0f}%"
    parts.append(f"<p>FUSE success rate: <b>{rate}</b> "
                 f"<span class='dim'>({stats['success']} ok · {stats['failure']} failed · "
                 f"{stats['empty']} empty gathers)</span></p>")
    failures = [s for s in sessions if s["_kind"] == "failure"]
    if failures:
        parts.append("<table><tr><th>date</th><th>topic</th><th>stage</th><th>error</th></tr>" +
                     "".join(f"<tr><td>{_e(s['_date'])}</td><td>{_e(s.get('topic', ''))}</td>"
                             f"<td class='bad'>{_e(s.get('failed_stage', '?'))}</td>"
                             f"<td class='dim'>{_e(s.get('error', ''))}</td></tr>"
                             for s in failures) + "</table>")
    yields = collector_yield(sessions)
    if yields:
        parts.append("<table><tr><th>collector</th><th>records</th><th>found</th>"
                     "<th>ok runs</th><th>errors</th></tr>" +
                     "".join(f"<tr><td>{_e(c)}</td><td>{y['records']}</td><td>{y['found']}</td>"
                             f"<td>{y['ok_runs']}/{y['runs']}</td>"
                             f"<td class='bad'>{_e('; '.join(y['errors']) or '')}</td></tr>"
                             for c, y in sorted(yields.items())) + "</table>")
    for line in discrepancies(sessions, spend_days):
        parts.append(f"<p class='bad'>⚠ {_e(line)}</p>")

    # Re-run affordances
    if sessions:
        parts.append("<h2>Re-open / re-run a topic</h2>")
        for s in sessions:
            parts.append(f"<p class='dim'>{_e(s['_date'])} — {_e(s.get('topic', ''))}</p>"
                         f"<pre>{_e(rerun_command(s))}</pre>")

    # PM3 slot
    parts.append("<h2>Pain-taxonomy movement</h2>"
                 "<p class='dim'>Slot reserved: lands when PM3 persistence ships "
                 "(gated on the 7/21 t1 verdict).</p>")

    # Footer: honesty about what was skipped
    footer = [f"generated {_e(generated_at)}"]
    for name, reason in skipped_sessions:
        footer.append(f"skipped session file {_e(name)}: {_e(reason)}")
    for name, reason in skipped_spend:
        footer.append(f"skipped ledger {_e(name)}: {_e(reason)}")
    parts.append("<footer>" + "<br>".join(footer) + "</footer>")
    return "\n".join(parts)
