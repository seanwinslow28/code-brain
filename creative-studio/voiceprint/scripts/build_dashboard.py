#!/usr/bin/env python3
"""
build_dashboard.py — render a self-contained progress dashboard for a reader's
VoicePrint workspace. Reads local files only, bakes the current state into a static
HTML file, and writes it to voiceprint/_work/dashboard.html. No connectors, no CDN,
no JavaScript framework — it opens by double-clicking the file, offline.

(VoicePrint's data is local files, not a connector, so this is a generated static
dashboard refreshed by /voiceprint-start and /voiceprint-refine — not a live
create_artifact, which would expect connector-backed data.)

Usage:
  python3 build_dashboard.py --root voiceprint/
"""

import argparse
import datetime
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pile_state  # noqa: E402

STAGE_ORDER = pile_state.STAGES
STAGE_LABELS = pile_state.STAGE_LABELS


def _trend_svg(trend):
    """Tiny inline SVG line of pct_changed across rounds. Lower = converging."""
    if not trend or len(trend) < 2:
        return '<p class="muted">Run a couple of refine rounds to see the convergence line.</p>'
    w, h, pad = 420, 120, 24
    mx = max(trend) or 1
    n = len(trend)
    pts = []
    for i, v in enumerate(trend):
        x = pad + (w - 2 * pad) * (i / (n - 1))
        y = pad + (h - 2 * pad) * (v / mx)  # bigger pct = lower on chart (more to fix)
        pts.append((x, y))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" class="dot"/>' for x, y in pts)
    return (
        f'<svg viewBox="0 0 {w} {h}" class="trend" role="img" '
        f'aria-label="edit-diff percent across refine rounds">'
        f'<polyline points="{poly}" class="line"/>{dots}</svg>'
        f'<p class="muted">Edit-diff % per round: {trend} — lower means your voice is converging.</p>'
    )


def render(summary, proof):
    rows = []
    for s in STAGE_ORDER:
        st = summary["stages"][s]
        cls = {"complete": "done", "incomplete": "partial", "not_started": "todo"}.get(st, "todo")
        mark = {"done": "&#10003;", "partial": "&#8226;", "todo": "&#9675;"}[cls]
        rows.append(
            f'<li class="{cls}"><span class="mark">{mark}</span>'
            f'<span class="lbl">{html.escape(STAGE_LABELS[s])}</span>'
            f'<span class="st">{html.escape(st.replace("_", " "))}</span></li>'
        )
    checklist = "\n".join(rows)

    proof_html = ""
    if proof:
        items = []
        gs = proof.get("gauntlet_self_check")
        if gs:
            items.append(f'<div class="proofrow"><b>Avoids your rejected registers</b>'
                         f'<span>{html.escape(str(gs))}</span></div>')
        fp = proof.get("fingerprint") or {}
        if fp:
            items.append(
                '<div class="proofrow"><b>Burstiness (sentence-length variety)</b>'
                f'<span>you {fp.get("reader_burstiness","?")} &nbsp;|&nbsp; '
                f'your draft {fp.get("draft_burstiness","?")} &nbsp;|&nbsp; '
                f'generic-AI {fp.get("generic_ai_burstiness","?")}</span></div>'
            )
        verdict = proof.get("verdict")
        if verdict:
            items.append(f'<div class="verdict">{html.escape(str(verdict))}</div>')
        proof_html = (
            '<section class="card"><h2>Proof — more you, less generic-AI</h2>'
            + "\n".join(items)
            + "</section>"
        )

    cold = ('<p class="warn">Cold-start: your skill is outline-grade until you add real '
            'writing samples through the refine loop. That is expected.</p>'
            if summary.get("cold_start") else "")

    nxt = summary.get("next_best_action") or "Run /voiceprint-start to begin."
    bundle = ("ready at <code>voiceprint/my-voice/</code>" if summary.get("bundle_exists")
              else "not generated yet")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VoicePrint — {html.escape(summary.get('reader_label','your'))} voice</title>
<style>
  :root {{ --ink:#1a1a1a; --muted:#6b6b6b; --paper:#fffaf2; --accent:#0a5b54; --warn:#9a5b00; --line:#e4ddcf; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:32px; background:var(--paper); color:var(--ink);
          font:16px/1.55 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif; }}
  .wrap {{ max-width:680px; margin:0 auto; }}
  h1 {{ font-size:22px; margin:0 0 2px; }}
  .sub {{ color:var(--muted); margin:0 0 24px; font-size:14px; }}
  .card {{ background:#fff; border:1px solid var(--line); border-radius:12px;
           padding:20px 22px; margin:0 0 18px; }}
  h2 {{ font-size:15px; text-transform:uppercase; letter-spacing:.04em; color:var(--accent);
        margin:0 0 14px; }}
  ul.checklist {{ list-style:none; margin:0; padding:0; }}
  ul.checklist li {{ display:flex; align-items:center; gap:10px; padding:7px 0;
                     border-bottom:1px dashed var(--line); }}
  ul.checklist li:last-child {{ border-bottom:0; }}
  .mark {{ width:20px; text-align:center; }}
  li.done .mark {{ color:var(--accent); }} li.todo .mark {{ color:#c9c1b2; }}
  li.partial .mark {{ color:var(--warn); }}
  .lbl {{ flex:1; }} .st {{ color:var(--muted); font-size:13px; }}
  .next {{ font-size:17px; }} .next b {{ color:var(--accent); }}
  .muted {{ color:var(--muted); font-size:13px; }}
  .warn {{ color:var(--warn); font-size:14px; }}
  svg.trend {{ width:100%; max-width:420px; height:auto; }}
  .trend .line {{ fill:none; stroke:var(--accent); stroke-width:2.5; }}
  .trend .dot {{ fill:var(--accent); }}
  .proofrow {{ display:flex; justify-content:space-between; gap:16px; padding:6px 0;
               border-bottom:1px dashed var(--line); font-size:14px; }}
  .verdict {{ margin-top:12px; font-weight:600; color:var(--accent); }}
  code {{ background:#f3eee3; padding:1px 5px; border-radius:4px; font-size:13px; }}
  footer {{ color:var(--muted); font-size:12px; margin-top:8px; text-align:center; }}
</style></head>
<body><div class="wrap">
  <h1>Your VoicePrint pile</h1>
  <p class="sub">Built from your evidence, on your machine. Nothing here left your computer.</p>

  <section class="card">
    <h2>The pile</h2>
    <ul class="checklist">{checklist}</ul>
    {cold}
  </section>

  <section class="card next">
    <h2>Next</h2>
    <p class="next"><b>{html.escape(nxt)}</b></p>
    <p class="muted">Your voice skill is {bundle}.</p>
  </section>

  <section class="card">
    <h2>Is it converging?</h2>
    {_trend_svg(summary.get('pct_changed_trend'))}
  </section>

  {proof_html}

  <footer>Generated {now} · refresh by re-running /voiceprint-start or /voiceprint-refine</footer>
</div></body></html>"""


def main(argv=None):
    p = argparse.ArgumentParser(description="Render the VoicePrint progress dashboard.")
    p.add_argument("--root", default="voiceprint", help="path to the voiceprint/ root")
    args = p.parse_args(argv)

    root = Path(args.root)
    work = root / "_work"
    if not work.exists():
        print(f"No workspace at {work} — run /voiceprint-start first.", file=sys.stderr)
        return 1

    summary = pile_state.summarize(root)
    proof = pile_state.load_json(work / "proof.json")
    out = work / "dashboard.html"
    out.write_text(render(summary, proof), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
