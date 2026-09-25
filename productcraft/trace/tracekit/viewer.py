"""The viewer renderer — one self-contained HTML per engagement, to DESIGN.md (#292).

Reads the records, the labels file, the artifacts' Moves sections and the
notes file; runs the rung-0 checks; writes `trace/eval.html`. The page is a
view of the records, never the store: it writes nothing back. Fonts are
embedded so it opens from disk offline; every string from a record, label or
artifact is escaped; no network, no hosted surface.

The markup, styles and keyboard loop are the ones Sean ratified on the #292
sample (samples/render_sample.py), made data-driven. If this file and
DESIGN.md disagree, DESIGN.md is the intent and this file is the bug.
"""
from __future__ import annotations

import base64
import datetime as _dt
import html as _html
import json
import re
from pathlib import Path
from typing import Optional

from . import KIT_NAME, KIT_VERSION
from .cases import ASSIST_BLURB, Case, CasesDoc, Source, load_cases
from .checker import Check, run_checks
from .labels import decided
from .engagement import Engagement, Record, load_engagement, normalize_meter
from .studio import PRODUCTCRAFT, PRODUCTCRAFT_CHECK_IMPLICATIONS, Studio
from .taxonomy import Taxonomy, load_taxonomy

__all__ = ["render", "render_html", "STAGES", "SEAT_NAMES", "REVIEW_PROMPTS", "run_line", "stage_name", "stage_label", "seat_name"]

# Productcraft's names, mirrored from the default studio profile (tracekit/studio.py); the renderer
# reads `eng.studio`, so another studio's engagement renders with its own stages and seats.
STAGES = PRODUCTCRAFT.stages
SEAT_NAMES = PRODUCTCRAFT.seat_names
FONTS_DIR = Path(__file__).resolve().parents[1] / "fonts"
HIDDEN = "hidden with the runtime"

# the plan's versioned review prompts, one per kind of run (eval-learning-plan.md §2)
REVIEW_PROMPTS_VERSION = PRODUCTCRAFT.review_prompts_version
REVIEW_PROMPTS = PRODUCTCRAFT.review_prompts
# one sentence per rung-0 check, in CHECK_NAMES order: what a finding there means for the reading
CHECK_IMPLICATIONS = PRODUCTCRAFT_CHECK_IMPLICATIONS
SEVERITIES = ("MATERIAL", "NOTE", "CRITICAL", "LOOPBACK", "BLOCKER")


def esc(s: object) -> str:
    return _html.escape("" if s is None else str(s), quote=True)


def stage_name(n: int, studio: Studio = PRODUCTCRAFT) -> str:
    return studio.stage_name(n)


def stage_label(n: int, studio: Studio = PRODUCTCRAFT) -> str:
    return studio.stage_label(n)


def seat_name(slug: str, studio: Studio = PRODUCTCRAFT) -> str:
    return studio.seat_name(slug)


def fmt_tokens(n: int) -> str:
    if n <= 0:
        return "—"
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def fmt_minutes(s: Optional[int]) -> str:
    if not s:
        return "—"
    return f"{s // 60} min" if s >= 60 else f"{s} s"


def icon(name: str) -> str:
    return f'<svg class="ico" aria-hidden="true" width="14" height="14" viewBox="0 0 14 14"><use href="#i-{name}"/></svg>'


def _join(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def run_no(pass_id: str) -> str:
    """`pass-10` → `10`, the plain run number a reader says out loud."""
    digits = "".join(ch for ch in str(pass_id) if ch.isdigit())
    return str(int(digits)) if digits else str(pass_id)


def run_line(pass_id: str, seat: str, kind: str, studio: Studio = PRODUCTCRAFT) -> str:
    """`Run 10 · Discovery audit` — the plain-language name for a pass (plan §2)."""
    who = seat_name(seat, studio)
    what = "" if who.lower().endswith(kind.lower()) else f" {kind}"
    return f"Run {run_no(pass_id)} · {who}{what}".rstrip()


# --------------------------------------------------------------------------- #
# what the seats found, read from the check records' own tables
# --------------------------------------------------------------------------- #


def _cells(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _plain(cell: str) -> str:
    return cell.replace("**", "").replace("`", "").replace("*", "").strip()


def _tables(text: str):
    """Yield (header cells, row cells) for every markdown table in a document."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            header = [_plain(c).lower() for c in _cells(lines[i])]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append([_plain(c) for c in _cells(lines[j])])
                j += 1
            yield header, rows
            i = j
            continue
        i += 1


def _severity_of(row: list[str], index: Optional[int]) -> Optional[str]:
    cells = ([row[index]] if index is not None and index < len(row) else []) + row
    for cell in cells:
        word = cell.strip().upper()
        if word in SEVERITIES:
            return word
    return None


def check_record_findings(eng: Engagement) -> dict[str, object]:
    """Count MATERIAL / NOTE findings across the check records in `audits/`.

    A seat's assessment of an artifact, read from the seat's own findings
    table. Nothing is inferred: a table with no severity column is skipped,
    and the files counted are named so the number can be traced back.
    """
    names: list[str] = []
    out: dict[str, object] = {"material": 0, "note": 0, "other": 0, "files": 0, "names": names}
    folder = eng.root / eng.studio.checks_dir
    if not folder.is_dir():
        return out
    for f in sorted(folder.glob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        found = 0
        for header, rows in _tables(text):
            idx = next((i for i, h in enumerate(header) if "severit" in h or h == "grade"), None)
            if idx is None:
                continue
            for row in rows:
                sev = _severity_of(row, idx)
                if sev == "MATERIAL":
                    out["material"] = int(out["material"]) + 1
                elif sev == "NOTE":
                    out["note"] = int(out["note"]) + 1
                elif sev:
                    out["other"] = int(out["other"]) + 1
                if sev:
                    found += 1
        if found:
            out["files"] = int(out["files"]) + 1
            names.append(f.name)
    return out


def owner_dispositions(eng: Engagement) -> dict[str, int]:
    """Accepted / declined / noted / pending, from the gate findings' Disposition cells."""
    out = {"accepted": 0, "declined": 0, "noted": 0, "pending": 0}
    folder = eng.root / eng.studio.checks_dir
    if not folder.is_dir():
        return out
    for f in sorted(folder.glob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for header, rows in _tables(text):
            if "disposition" not in header or not any("severit" in h for h in header):
                continue  # the gate's findings table, not a residual roll-up that repeats its rows
            idx = header.index("disposition")
            for row in rows:
                if idx >= len(row):
                    continue
                cell = row[idx].strip().lower()
                if cell.startswith(("accepted", "ratified", "accept ")):
                    out["accepted"] += 1
                elif cell.startswith(("declined", "rejected")):
                    out["declined"] += 1
                elif cell.startswith("noted"):
                    out["noted"] += 1
                else:
                    out["pending"] += 1
    return out


# --------------------------------------------------------------------------- #
# public
# --------------------------------------------------------------------------- #


def render(path: Path | str, out: Optional[Path] = None, repo: Optional[Path] = None) -> Path:
    eng = load_engagement(path, repo=repo)
    target = Path(out) if out else eng.trace_dir / "eval.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_html(eng), encoding="utf-8")
    return target


def render_html(eng: Engagement, checks: Optional[list[Check]] = None, rendered_on: Optional[str] = None,
                taxonomy: Optional[Taxonomy] = None) -> str:
    S = eng.studio
    tax = taxonomy if taxonomy is not None else (load_taxonomy(S.taxonomy_path) if S.taxonomy_path is not None else load_taxonomy())
    checks = checks if checks is not None else run_checks(eng, tax)
    rendered_on = rendered_on or _dt.date.today().isoformat()
    P = eng.records
    labels = eng.labels
    total = len(P)

    def verdict(pid: str) -> Optional[str]:
        l = labels.get(pid)
        return l.verdict if l else None

    def ffs(pid: str) -> Optional[int]:
        l = labels.get(pid)
        return l.first_failing_stage if l else None

    def critique(pid: str) -> str:
        l = labels.get(pid)
        return l.critique if l else ""

    def code(pid: str) -> str:
        l = labels.get(pid)
        return (l.failure_code or "") if l else ""

    labeled = [r.pass_id for r in P if decided(verdict(r.pass_id))]   # a defer is not a label (DESIGN.md §15)
    n_pass = sum(1 for pid in labeled if verdict(pid) == "pass")
    n_fail = sum(1 for pid in labeled if verdict(pid) == "fail")
    n_defer = sum(1 for r in P if verdict(r.pass_id) == "defer")
    n_unl = total - len(labeled)
    n_checks = len(checks)
    clean = sum(1 for c in checks if c.ok)

    pairs: dict[str, str] = {}
    for r in P:
        if r.shadow_of:
            pairs[r.pass_id] = r.shadow_of
            pairs[r.shadow_of] = r.pass_id

    def blind(pid: str) -> bool:
        other = pairs.get(pid)
        return bool(other) and not (verdict(pid) and verdict(other))

    fails: list[tuple[Record, int, str]] = []
    matrix: dict[tuple[int, int], int] = {}
    for r in P:
        if verdict(r.pass_id) == "fail" and ffs(r.pass_id):
            f = ffs(r.pass_id)
            fails.append((r, f, critique(r.pass_id)))
            matrix[(f - 1, f)] = matrix.get((f - 1, f), 0) + 1
    upstream_breaks = sorted({f for r, f, _ in fails if r.stage and f < r.stage})
    break_stages = sorted({f for _, f, _ in fails})

    per_stage: dict[int, dict[str, int]] = {}
    for r in P:
        d = per_stage.setdefault(r.stage, dict(passes=0, ok=0, fail=0, unl=0))
        d["passes"] += 1
        v = verdict(r.pass_id)
        d["ok" if v == "pass" else "fail" if v == "fail" else "unl"] += 1

    loops = [(r.pass_id, r.triggered_by) for r in P if r.triggered_by]
    cases_doc = load_cases(eng)
    findings = check_record_findings(eng)
    dispositions = owner_dispositions(eng)
    next_unlabeled = next((r.pass_id for r in P if not verdict(r.pass_id)), None)
    eng_id = esc(eng.brief.get("id") or eng.root.name)
    eng_name = esc(eng.brief.get("name") or "")
    synthetic = eng.brief.get("synthetic") is True
    n_label_rows = len(labeled)

    # ---- reading line -------------------------------------------------------
    if not fails:
        break_sentence = "No break has been labeled yet."
    else:
        first, rest = break_stages[0], break_stages[1:]
        s = f"The train broke first at stage {first}"
        if rest:
            s += f", then at stage{'s' if len(rest) > 1 else ''} {_join([str(x) for x in rest])}"
        if upstream_breaks:
            s += f"; the stage-{upstream_breaks[0]} break is the one that cost downstream work."
        else:
            s += "; no break has yet cost downstream work."
        break_sentence = s
    reading = (
        f"Of <strong>{total} passes</strong>, <strong>{len(labeled)} are labeled</strong>: {n_pass} pass, {n_fail} fail. "
        f"<strong>{n_unl} wait for a verdict.</strong> "
        + (f"{n_defer} of them deferred, to come back to. " if n_defer else "")
        + f"{break_sentence} Rung 0 is clean on {clean} of {n_checks} checks."
    )

    out: list[str] = []
    out.append(f"""
<div class="page">
<header class="mast">
  <div>
    <h1>{eng_id} · {eng_name}{'<span class="synthetic">synthetic</span>' if synthetic else ''}</h1>
    <div class="meta"><span>{esc(eng.brief.get('type') or 'engagement')}</span><span>opened {esc(eng.brief.get('opened') or '—')}</span><span>closed {esc(eng.brief.get('closed') or '—')}</span><span>{total} passes{f" of a {esc(eng.brief['pass_budget'])}-pass budget" if eng.brief.get('pass_budget') else ''}</span><span>rendered from {total} records, {n_label_rows} label rows</span></div>
  </div>
  <div class="tools">
    <button class="btn" id="copy-labels" type="button" title="Copy every drafted label as rows for the labels file">Copy label rows <span id="draft-count"></span></button>
    <button class="btn" id="help" type="button" aria-haspopup="dialog">Keys <kbd>?</kbd></button>
    <button class="btn" id="mode" type="button" aria-pressed="false" aria-label="Switch to night studio">Night</button>
  </div>
</header>
{_judging_html(eng, checks, clean, n_checks, len(labeled), total, findings, dispositions)}
<h2>What happened in this review</h2>
{_intro_html(cases_doc)}
<p class="reading">{reading}</p>
<div class="counter" aria-live="polite">
  <span>Labeled <b id="labeled-n">{len(labeled)}</b> of {total}<span id="draft-note"></span></span>
  <span class="track" aria-hidden="true"><i id="track-file" style="width:{(len(labeled) / total * 100) if total else 0:.0f}%"></i></span>
  <span>Next unlabeled: {f'<a href="#{next_unlabeled}" data-jump>{next_unlabeled}</a>' if next_unlabeled else '<span>none</span>'}</span>
</div>
{_guided_html(eng, cases_doc)}
""")

    # ---- where it broke -----------------------------------------------------
    cols = S.stage_numbers                       # first failing stage
    start_row = S.first_stage - 1                # "start": nothing good yet
    rows = [start_row] + S.stage_numbers[:-1]    # last good stage
    th = "".join(f"<th scope='col'>{c}</th>" for c in cols)
    trs = []
    for r_ in rows:
        tds = []
        for c_ in cols:
            if c_ <= r_:
                tds.append("<td class='na'><span></span></td>")
                continue
            n = matrix.get((r_, c_), 0)
            cls = "z" if n == 0 else ("c3" if n >= 3 else ("c2" if n == 2 else "c1"))
            tds.append(f"<td class='{cls}'><span>{n if n else '·'}</span></td>")
        trs.append(f"<tr><th scope='row'>{'start' if r_ == start_row else S.stage_name(r_)} {'' if r_ == start_row else r_}</th>{''.join(tds)}</tr>")
    heat_note = f"{n_fail} fails so far, which is too few for a heat: read the numbers." if n_fail < 10 else f"{n_fail} labeled fails."
    matrix_html = f"""
<table class="matrix" aria-describedby="matrix-cap">
  <caption class="sr">Transition failures: rows are the last good stage, columns the first failing stage, cells are counts.</caption>
  <thead><tr><th scope="col" class="axis">last good ↓ · first failing →</th>{th}</tr></thead>
  <tbody>{''.join(trs)}</tbody>
</table>
<p class="cap" id="matrix-cap">Counts of labeled fails. {heat_note} Hatched cells cannot occur in a linear train.</p>
"""
    stage_rows = []
    for s in S.stage_numbers:
        d = per_stage.get(s, dict(passes=0, ok=0, fail=0, unl=0))
        bar = ("".join("<i class='ok' style='width:14px' title='pass'></i>" for _ in range(d["ok"]))
               + "".join("<i class='fail' style='width:14px' title='fail'></i>" for _ in range(d["fail"]))
               + "".join("<i class='unl' style='width:14px' title='unlabeled'></i>" for _ in range(d["unl"])))
        stage_rows.append(f"<li><span>{s} {S.stage_name(s)}</span><span class='bar' aria-hidden='true'>{bar}</span><span class='n'>{d['ok']} pass · {d['fail']} fail{' · ' + str(d['unl']) + ' open' if d['unl'] else ''}</span></li>")
    stages_html = f"""
<h3>Passes per stage</h3>
<ul class="stages">{''.join(stage_rows)}</ul>
<div class="legend"><span><i style="background:var(--ink-wash-3)"></i>pass</span><span><i style="background:var(--ink)"></i>fail</span><span><i style="border:1px dashed var(--ink-wash-3);box-sizing:border-box"></i>unlabeled</span></div>
"""
    if fails:
        fails_html = "".join(
            f"<li><div class='who'><b><a href='#{esc(r.pass_id)}' data-jump>{esc(r.pass_id)}</a></b>{esc(S.seat_name(r.seat))} {esc(r.kind)}<br>broke at {f} {esc(S.stage_name(f))}</div>"
            f"<div class='why'>{esc(crit) or '<span class=sub>no critique yet</span>'}<small>{'upstream of the pass read' if r.stage and f < r.stage else 'at the pass read'}</small></div></li>"
            for r, f, crit in fails)
    else:
        fails_html = "<li><div class='who sub'>—</div><div class='why sub'>No fails labeled yet.</div></li>"
    out.append(f"""
<h2>Where it broke</h2>
<div class="broke">
  <div>{matrix_html}{stages_html}</div>
  <div>
    <h3>The {n_fail} fails, first failure named</h3>
    <ul class="fails">{fails_html}</ul>
    {_rung_html(checks, S)}
  </div>
</div>
""")

    # ---- train ----------------------------------------------------------------
    colx = {s: 150 + i * 120 for i, s in enumerate(S.stage_numbers)}
    columns = list(S.stage_numbers)
    if S.coordinator_stage is not None:          # the coordinator's own passes sit in a last column
        colx[S.coordinator_stage] = 150 + len(S.stage_numbers) * 120
        columns.append(S.coordinator_stage)
    last_col = max(colx.values())
    rowh, top = 26, 40
    svg_h = top + rowh * max(total, 1) + 20
    svg_w = last_col + 90
    idx = {r.pass_id: i for i, r in enumerate(P)}
    parts = [f'<svg viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" role="img" aria-labelledby="train-title">',
             '<title id="train-title">The train: every pass in order, on its stage.</title>',
             '<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L8 4 0 8z" fill="var(--ink)"/></marker></defs>',
             '<g class="grid">']
    for s in columns:
        x = colx[s]
        parts.append(f'<line x1="{x}" y1="{top - 10}" x2="{x}" y2="{svg_h - 10}"/>')
        parts.append(f'<text x="{x}" y="{top - 18}" text-anchor="middle">{esc(S.stage_label(s))}</text>')
    parts.append('</g>')
    pts = [(colx.get(r.stage, last_col), top + i * rowh + rowh / 2) for i, r in enumerate(P)]
    if pts:
        parts.append('<polyline class="lane" fill="none" points="' + " ".join(f"{x},{y}" for x, y in pts) + '"/>')
    for i, r in enumerate(P):
        x, y = pts[i]
        v, k = verdict(r.pass_id), r.kind
        parts.append(f'<text class="pid" x="8" y="{y + 4}">{esc(r.pass_id)}</text>')
        parts.append(f'<text x="64" y="{y + 4}">{esc("gate" if r.seat in S.gate_seats else S.seat_name(r.seat))}</text>')
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
        if r.shadow_of and r.shadow_of in idx:
            off = 78 if v is None else 14
            parts.append(f'<line class="shadow" x1="{x + 8}" y1="{y}" x2="{x + off - 4}" y2="{y}"/><text x="{x + off}" y="{y + 4}">{"· " if v is None else ""}shadow of {esc(r.shadow_of)}</text>')
    for child, trig in loops:
        if child in idx and trig in idx:
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

    # ---- passes ---------------------------------------------------------------
    rows_html = [_row(eng, r, verdict(r.pass_id), ffs(r.pass_id), critique(r.pass_id), pairs.get(r.pass_id), blind(r.pass_id), code(r.pass_id), tax) for r in P]
    n_pairs = sum(1 for r in P if r.shadow_of)
    out.append(f"""
<h2>Passes</h2>
<div class="filters">
  <span>Show</span>
  <button class="btn" type="button" data-filter="all" aria-pressed="true">all {total}</button>
  <button class="btn" type="button" data-filter="fail" aria-pressed="false">fails {n_fail}</button>
  <button class="btn" type="button" data-filter="unlabeled" aria-pressed="false">unlabeled {n_unl}</button>
  <button class="btn" type="button" data-filter="deferred" aria-pressed="false">deferred {n_defer}</button>
  <button class="btn" type="button" data-filter="pairs" aria-pressed="false">shadow pairs {n_pairs}</button>
  <span style="margin-left:auto">Columns: runtime · wall-clock · tokens in+out · verdict · critique. <kbd>j</kbd>/<kbd>k</kbd> walk rows, <kbd>enter</kbd> opens.</span>
</div>
<div class="passes" id="passes">{''.join(rows_html) or '<p class="sub" style="padding:1rem 0">No pass records yet.</p>'}</div>
""")

    # ---- slots + footer ---------------------------------------------------------
    out.append(f"""
<h2>What comes later</h2>
<div class="slots">
  {_taxonomy_slot_html(tax, labels)}
  <div class="slot"><h3>Judge results</h3><p><span class="when">Arrives per failure mode</span>, only after a mode recurs across engagements with thirty to fifty labeled examples per class and a judge is validated against the labels on a held-out split. A judge's verdict will sit beside the human one in each row, never replace it.</p></div>
  {_notes_slot_html(eng)}
</div>
<footer>
  <span>Rendered {esc(rendered_on)} from {total} records and {n_label_rows} label rows. The records are the truth; this page is a view of them.</span>
  <span>{esc(S.name)} · {esc(KIT_NAME)} · kit {esc(KIT_VERSION)}</span>
</footer>
</div>
<dialog id="keys" aria-labelledby="keys-title">
  <h3 id="keys-title" style="margin-top:0">Keys</h3>
  <dl>
    <dt><kbd>j</kbd> <kbd>k</kbd></dt><dd>next / previous pass — or next / previous case while you are inside guided reading</dd>
    <dt><kbd>enter</kbd></dt><dd>open or fold the current pass</dd>
    <dt><kbd>1</kbd> <kbd>2</kbd></dt><dd>label the current pass pass / fail</dd>
    <dt><kbd>d</kbd></dt><dd>defer the current pass: come back to it (not a verdict; it still waits)</dd>
    <dt><kbd>f</kbd></dt><dd>first failing stage</dd>
    <dt><kbd>c</kbd></dt><dd>critique</dd>
    <dt><kbd>u</kbd></dt><dd>jump to the next unlabeled pass</dd>
    <dt><kbd>esc</kbd></dt><dd>leave a field</dd>
    <dt><kbd>?</kbd></dt><dd>this sheet</dd>
  </dl>
  <form method="dialog" style="margin-top:1rem"><button class="btn" type="submit">Close</button></form>
</dialog>
""")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{eng_id} · {eng_name} · eval</title>
<style>{_fonts_css()}{CSS}</style>
</head>
<body>
{SYMBOLS}
{''.join(out)}
<script>const TRACE_ENG = {json.dumps(str(eng.brief.get('id') or eng.root.name))};{JS}</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# what you are judging — four statements kept apart (plan §2)
# --------------------------------------------------------------------------- #


def _judging_html(eng: Engagement, checks: list[Check], clean: int, n_checks: int, labeled: int,
                  total: int, findings: dict[str, object], disp: dict[str, int]) -> str:
    if int(findings["files"]) == 0:
        found = "No check record has a findings table yet."
    else:
        found = f"<b>{findings['material']} material</b> · <b>{findings['note']}</b> note{'' if findings['note'] == 1 else 's'}"
        if findings["other"]:
            found += f" · {findings['other']} other"
    decided = disp["accepted"] + disp["declined"] + disp["pending"]
    if decided + disp["noted"] == 0:
        owner = "No gate has put a decision to you yet."
    else:
        owner = f"<b>{disp['pending']} pending</b> · {disp['accepted']} accepted"
        if disp["declined"]:
            owner += f" · {disp['declined']} declined"
    prompts = "".join(
        f"<tr><th scope='row'>{esc(kind)}</th><td>{esc(q)}</td></tr>" for kind, q in eng.studio.review_prompts)
    files_note = (f" Read from {findings['files']} check record{'' if findings['files'] == 1 else 's'} in <code>{esc(eng.studio.checks_dir)}/</code>."
                  if findings["files"] else "")
    noted_note = f" {disp['noted']} more are noted and ask for nothing." if disp["noted"] else ""
    return f"""
<h2>What you are judging</h2>
<div class="judging">
  <div class="stat">
    <h3>Record checks</h3>
    <p class="v"><a href="#record-checks"><b>{clean} of {n_checks}</b> pass</a></p>
    <p class="s">Automated checks of the records, not a quality score. They say the paperwork adds up, never that the thinking was good.</p>
  </div>
  <div class="stat">
    <h3>Reviewer findings</h3>
    <p class="v">{found}</p>
    <p class="s">A seat's assessment of one artifact and revision. Evidence for you to weigh, not a verdict.{files_note}</p>
  </div>
  <div class="stat">
    <h3>Your labels</h3>
    <p class="v">Labeled <b>{labeled} of {total}</b></p>
    <p class="s">Your assessment of the work of each run: pass or fail, nothing between. An empty verdict means the review is unfinished, not a pass.</p>
  </div>
  <div class="stat">
    <h3>Owner decisions</h3>
    <p class="v">{owner}</p>
    <p class="s">Yours alone; a gate's recommendation never fills one in.{noted_note}</p>
  </div>
</div>
<table class="prompts">
  <caption>What to ask of each kind of run <span class="sub">— teaching prompts to calibrate, {esc(eng.studio.review_prompts_version)}, not an automated grader</span></caption>
  <tbody>{prompts}</tbody>
</table>
"""


# --------------------------------------------------------------------------- #
# the rung-0 list: verified, failed, unverifiable — with the checker's own reasons
# --------------------------------------------------------------------------- #


def _rung_html(checks: list[Check], studio: Studio = PRODUCTCRAFT) -> str:
    items = []
    for i, c in enumerate(checks):
        state = "failed" if not c.ok else ("unverifiable in part" if c.n_unverifiable else "verified")
        glyph = icon("check") if c.ok else icon("cross")
        why = "".join(f"<li>{esc(f)}</li>" for f in c.findings)
        notes = "".join(f"<li class='sub'>{esc(n)}</li>" for n in c.notes)
        implication = studio.check_implications[i] if i < len(studio.check_implications) else ""
        body = ""
        if why:
            body += f"<ul class='why'>{why}</ul>"
        if notes:
            body += f"<ul class='why'>{notes}</ul>"
        if (why or c.n_unverifiable) and implication:
            body += f"<p class='implication'>{esc(implication)}</p>"
        items.append(
            f"<li><span class='mark'>{glyph}</span><span class='what'>{esc(c.name)}"
            f"<span class='state'>{state}</span></span><span class='n'>{esc(c.count)}</span>{body}</li>")
    return f"""
<h3 id="record-checks">Record checks</h3>
<p class="cap">Automated checks of the records and their traceability. Not a quality score, and never a verdict on a seat's thinking.</p>
<ul class="rung">{''.join(items)}</ul>
<details class="term"><summary>What the kit calls these</summary><p class="sub">Rung 0 checks are the nine deterministic checks the kit runs with no model and no network. Rung 1 is the failure taxonomy, rung 2 a judge — both listed under <em>What comes later</em>.</p></details>
"""


# --------------------------------------------------------------------------- #
# process notes: three takeaways, then the dated history
# --------------------------------------------------------------------------- #

_DATED = re.compile(r"^(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)\s+(.*)$", re.S)


def _notes_slot_html(eng: Engagement) -> str:
    head = ("<h3>Process notes</h3>"
            "<p><span class=\"when\">The coordinator's running notes for this engagement</span>, read from the "
            "engagement's notes file. What the run did, what was ruled, what to watch next time.</p>")
    text = (eng.notes or "").strip()
    if not text:
        return f'<div class="slot">{head}<div class="notes">No notes file yet.</div></div>'
    bullets = [line.strip()[2:].strip() for line in text.split("\n") if line.strip().startswith("- ")]
    if not bullets:
        return f'<div class="slot">{head}<div class="notes">{esc(text)}</div></div>'

    def item(b: str) -> str:
        m = _DATED.match(b)
        if m:
            return f"<li><b>{esc(m.group(1))}</b> {esc(m.group(2))}</li>"
        return f"<li>{esc(b)}</li>"

    takeaways = "".join(item(b) for b in bullets[:3])
    rest = "".join(item(b) for b in bullets)
    return (f'<div class="slot">{head}'
            f'<ul class="takeaways">{takeaways}</ul>'
            f'<details class="history"><summary>The full dated history, {len(bullets)} entries</summary>'
            f'<ul class="takeaways">{rest}</ul></details></div>')


# --------------------------------------------------------------------------- #
# guided reading (plan §§3, 4, 8) — the cases, with assistance by level
# --------------------------------------------------------------------------- #


def _guided_empty(reason: str) -> str:
    return f"""
<h2>Guided reading</h2>
<div class="guided empty">
  <p>{reason}</p>
  <p class="sub">Teaching content lives in <code>trace/cases.md</code> beside the records — one case per pass and finding, each quoting its source with the hash that source carried when the case was written. This page never writes a story of its own: no file, no cases. The schema is <code>productcraft/trace/cases-template.md</code>.</p>
</div>
"""


def _guided_html(eng: Engagement, doc: Optional[CasesDoc]) -> str:
    if doc is None:
        return _guided_empty("No cases have been written for this engagement yet.")
    errors = "".join(f"<li>{esc(e)}</li>" for e in doc.errors)
    errors_html = (f'<div class="case-errors"><b>{len(doc.errors)} line(s) in cases.md did not check out:</b>'
                   f'<ul>{errors}</ul></div>') if doc.errors else ""
    if not doc.cases:
        return _guided_empty("No case in <code>cases.md</code> could be read.") if not errors_html else f"""
<h2>Guided reading</h2>
<div class="guided empty"><p>No case in <code>cases.md</code> could be read.</p>{errors_html}</div>
"""
    by_id = eng.by_id
    chapters = "".join(_chapter_html(doc, c, i + 1, by_id.get(c.pass_id), eng.studio) for i, c in enumerate(doc.cases))
    links = "".join(
        f'<a href="#case-{esc(c.key)}" data-case-link>{i + 1}. {esc(c.title)}</a>' for i, c in enumerate(doc.cases))
    status = ("Every case here has been read against its sources." if doc.reviewed else
              "These explanations are proposed readings, checked against the sources but not yet read by you. "
              "They are not an answer key, and disagreeing with one on the evidence is a good outcome.")
    written = f" Written {esc(doc.written)}." if doc.written else ""
    return f"""
<h2>Guided reading</h2>
<div class="guided" id="guided">
  <p class="guided-intro">{len(doc.cases)} case{'' if len(doc.cases) == 1 else 's'} from this engagement, in the order they were written, with decreasing help. Each one names the run it comes from and quotes the record it rests on. <b>Your practice answers stay here in the browser and never touch the labels file.</b>{written}</p>
  <p class="cap">{status}</p>
  {errors_html}
  <div class="case-links">{links}</div>
  <div class="guided-tools">
    <button class="btn" type="button" id="copy-practice">Copy practice notes</button>
    <button class="btn" type="button" id="download-practice">Download backup</button>
    <label class="btn file"><input type="file" id="restore-practice" accept="application/json,.json">Restore backup</label>
    <span class="sub" id="practice-status" aria-live="polite">Nothing practised yet.</span>
  </div>
  <div class="chapters">{chapters}</div>
  <details class="practice-fallback"><summary>If copying is blocked, take the notes from here</summary><textarea id="practice-text" rows="8" readonly></textarea></details>
</div>
"""


def _source_html(s: Source) -> str:
    where = f"{esc(s.path)}{f':{s.line}' if s.line else ''}"
    label = f"<b>{esc(s.label)}</b> · " if s.label else ""
    if s.shows_excerpt:
        body = f"<blockquote>{esc(s.excerpt)}</blockquote>"
    else:
        body = f"<p class='qualified'>{esc(s.qualification)}</p>"
    fingerprint = (f"<details class='fingerprint'><summary>Fingerprint</summary><dl>"
                   f"<dt>path</dt><dd>{esc(s.path)}</dd>"
                   f"<dt>sha256 when written</dt><dd>{esc(s.sha256)}</dd>"
                   f"<dt>sha256 now</dt><dd>{esc(s.current_sha256 or 'not on disk')}</dd></dl></details>")
    return (f"<div class='source' data-src='{esc(s.label or s.path)} — {where} (sha256 {esc(s.sha256[:12])}…)'>"
            f"<p class='prov'>Source excerpt · {label}{where}</p>{body}{fingerprint}</div>")


def _wrap(label: str, width: int = 24) -> list[str]:
    lines, cur = [], ""
    for word in label.split():
        if cur and len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    lines.append(cur)
    return lines or [""]


def _diagram_svg(case: Case) -> str:
    """One optional inline SVG per case, drawn from a `### Diagram` text flow. No mermaid, no library."""
    if not case.diagram:
        return ""
    W, GAP, VGAP, LH = 160, 40, 14, 14
    columns: list[list[tuple[str, str, list[str]]]] = []
    for kind, branch, label in case.diagram:
        text = f"{branch}: {label}" if branch else label
        node = (kind, branch, _wrap(text))
        if kind == "branch" and columns and columns[-1][0][0] == "branch":
            columns[-1].append(node)
        else:
            columns.append([node])
    height_of = lambda lines: max(34, LH * len(lines) + 20)
    col_h = [sum(height_of(n[2]) for n in col) + VGAP * (len(col) - 1) for col in columns]
    svg_h = max(col_h) + 24
    mid = svg_h / 2
    parts: list[str] = []
    prev_right: Optional[tuple[float, float]] = None
    for i, col in enumerate(columns):
        x = 8 + i * (W + GAP)
        y = mid - col_h[i] / 2
        last_right = None
        for kind, _branch, lines in col:
            h = height_of(lines)
            cls = {"decision": "d-decision", "branch": "d-branch"}.get(kind, "d-step")
            tspans = "".join(
                f'<tspan x="{x + W / 2}" dy="{0 if j == 0 else LH}">{esc(l)}</tspan>' for j, l in enumerate(lines))
            parts.append(f'<rect class="{cls}" x="{x}" y="{y:.0f}" width="{W}" height="{h}" rx="3"/>'
                         f'<text x="{x + W / 2}" y="{y + h / 2 - (len(lines) - 1) * LH / 2 + 4:.0f}" text-anchor="middle">{tspans}</text>')
            if prev_right:
                parts.append(f'<path class="d-edge" d="M{prev_right[0]:.0f} {prev_right[1]:.0f} '
                             f'C {prev_right[0] + 18:.0f} {prev_right[1]:.0f}, {x - 18} {y + h / 2:.0f}, {x - 3} {y + h / 2:.0f}"/>')
            last_right = (x + W, y + h / 2)
            y += h + VGAP
        prev_right = last_right if len(col) == 1 else None
    width = 8 + len(columns) * (W + GAP)
    text_equiv = "".join(
        f"<li>{esc((branch + ': ' if branch else '') + label + ('?' if kind == 'decision' else ''))}</li>"
        for kind, branch, label in case.diagram)
    return (f'<figure class="diagram"><figcaption>One step of the decision, not the whole rule</figcaption>'
            f'<svg viewBox="0 0 {width:.0f} {svg_h:.0f}" width="{width:.0f}" role="img" aria-label="A small flow: '
            f'{esc(" then ".join(l for _, _, l in case.diagram))}">{"".join(parts)}</svg>'
            f'<ul class="diagram-text">{text_equiv}</ul></figure>')


def _practice_html(case: Case) -> str:
    opts = "".join(
        f'<label class="choice"><input type="radio" name="opt-{esc(case.key)}" value="{esc(o.key)}" '
        f'data-choice data-label="{esc(o.label)}">{esc(o.label)}</label>' for o in case.options)
    fieldset = (f'<fieldset><legend>{esc(case.question) or "What is your call?"}</legend>{opts}</fieldset>'
                if case.options else f'<p class="q">{esc(case.question)}</p>')
    prompt = case.your_turn or "Answer in your own words, and name the evidence you are using."
    return f"""
<div class="practice" data-practice="{esc(case.key)}">
  <h4>Your turn</h4>
  {fieldset}
  <label class="note-label">Your note — {esc(prompt)}
    <textarea data-practice-note rows="3" maxlength="20000"></textarea>
  </label>
  <div class="actions">
    <button class="btn" type="button" data-practice-save>Save my answer</button>
    <button class="btn" type="button" data-practice-bookmark aria-pressed="false">Come back to this</button>
    <span class="sub" data-practice-state>Nothing saved yet.</span>
  </div>
  <p class="sub">Practice notes are yours: they stay in this browser, never in the labels file, and a saved answer never fills in a verdict.</p>
</div>"""


def _chapter_html(doc: CasesDoc, case: Case, n: int, rec: Optional[Record], studio: Studio = PRODUCTCRAFT) -> str:
    run = run_line(case.pass_id, rec.seat if rec else "", rec.kind if rec else "", studio) if rec else f"Run {run_no(case.pass_id)}"
    finding = f" · finding {esc(case.finding)}" if case.finding else ""
    evidence = "".join(_source_html(s) for s in case.sources) or "<p class='sub'>No source is named for this case.</p>"
    story = "".join(f"<p>{esc(p)}</p>" for p in case.story)
    goal = f"<p>{esc(case.goal)}</p>" if case.goal else ""
    rest = "".join(f"<p>{esc(p)}</p>" for p in case.rest_of_story)
    reveal_body = "".join(f"<p>{esc(p)}</p>" for p in case.reveal) or "<p class='sub'>Not written yet.</p>"
    attribution = f"<p class='prov sub'>Explanation · {doc.attribution}.</p>"
    diagram = _diagram_svg(case)
    terms = ("".join(f"<dt>{esc(t)}</dt><dd>{esc(d)}</dd>" for t, d in case.terms))
    terms_html = f"<dl class='terms'>{terms}</dl>" if terms else ""
    qualified = ("<p class='qualified'>One source of this case has changed or gone missing since the case was "
                 "written, so read it as a qualified story.</p>" if case.qualified else "")
    notes = "".join(f"<p class='qualified'>{esc(x)}</p>" for x in case.notes)
    row_link = f'<p class="case-foot"><a href="#{esc(case.pass_id)}" data-jump>Open {esc(run_line(case.pass_id, rec.seat, rec.kind, studio)) if rec else esc(case.pass_id)}’s row below</a> to label it.</p>' if rec else ""
    hint = (f'<details class="help" data-exposure="hint"><summary>Give me one hint</summary><p>{esc(case.hint)}</p></details>' 
            if case.hint else "")

    if case.assist == "worked":
        body = f"""
<h4>Source excerpt</h4>{evidence}
<h4>Explanation</h4><div class="story">{story}</div>{attribution}
{diagram}
<div class="reveal open"><h4>The reviewer's reasoning, and what the record says happened</h4>{reveal_body}{attribution}</div>
{_practice_html(case)}"""
    elif case.assist == "hint":
        body = f"""
<h4>Source excerpt</h4>{evidence}
<h4>Explanation</h4><div class="story">{story}</div>{attribution}
{diagram}
{_practice_html(case)}
{hint}
<details class="help" data-exposure="reveal"><summary>Read what the reviewer found and what changed</summary>{reveal_body}{attribution}</details>"""
    else:
        body = f"""
<div class="story goal">{goal}</div>
<h4>Source excerpt</h4>{evidence}
{_practice_html(case)}
{hint}
<details class="help locked" data-exposure="reveal" data-locked="1"><summary>Show the diagnosis and the reviewer's reasoning</summary>
  <div class="story">{rest}</div>
  {diagram}
  {reveal_body}{attribution}</details>"""

    return f"""
<details class="chapter" id="case-{esc(case.key)}" data-case="{esc(case.key)}" data-assist="{esc(case.assist)}"
  data-title="{esc(case.title)}" data-run="{esc(run)}" data-pass="{esc(case.pass_id)}"{' open' if case.assist == 'worked' and n == 1 else ''}>
  <summary>
    <span class="number" aria-hidden="true">{n:02d}</span>
    <span class="chapter-title"><span class="ct">{esc(case.title)}</span>
      <span class="sub">{esc(run)} <span class="pid-sub">{esc(case.pass_id)}</span>{finding}</span></span>
    <span class="assist-tag">{esc(case.assist)}</span>
  </summary>
  <div class="case-body">
    <p class="focus">{esc(ASSIST_BLURB[case.assist])}</p>
    {qualified}{notes}
    {body}
    {terms_html}
    {row_link}
  </div>
</details>"""


def _intro_html(doc: Optional[CasesDoc]) -> str:
    if doc is None or not doc.intro:
        return ('<p class="intro sub">No plain-language summary has been written for this engagement yet; it lives '
                'in <code>trace/cases.md</code>. The counts below are composed from the records and the labels file.</p>')
    return f'<p class="intro">{esc(doc.intro)}</p>'


# --------------------------------------------------------------------------- #
# one pass row
# --------------------------------------------------------------------------- #



def _code_state_html(code: str, tax: Optional[Taxonomy]) -> str:
    """The row's failure_code line: a link to its mode, or an honest reason it is blank."""
    if code:
        if tax is not None and code in tax:
            return f"failure_code <a href='#mode-{esc(code)}'><code>{esc(code)}</code></a>"
        return f"failure_code <code>{esc(code)}</code> — not in the taxonomy, so free text"
    if tax is not None and tax.open:
        return "failure_code blank — codes are the taxonomy's, set in the labels file, never here."
    return "failure_code stays blank until a taxonomy exists."


def _taxonomy_slot_html(tax: Optional[Taxonomy], labels: dict) -> str:
    """DESIGN.md §10: empty state names the threshold; filled, one line per mode with its count.

    A mode is listed only when a label row carries its code — the taxonomy file
    can name a mode no row in this engagement was, and that is not this engagement's
    line. A code outside the taxonomy is listed apart as free text, as rung 0 reports it.
    """
    counts: dict[str, list[str]] = {}
    for pid in sorted(labels):
        c = (labels[pid].failure_code or "").strip()
        if c:
            counts.setdefault(c, []).append(pid)
    if not counts:
        return ('<div class="slot"><h3>Failure taxonomy</h3><p><span class="when">Arrives after about thirty labels</span>, '
                'when the critiques get grouped into named failure modes with counts. Until then this slot lists nothing '
                'and the failure_code column stays blank.</p></div>')
    known = [c for c in (tax.codes if tax is not None else {}) if c in counts]
    free = [c for c in counts if tax is None or c not in tax]
    lines = []
    for c in known:
        k = tax.codes[c]
        rows = counts[c]
        lines.append(f"<li id='mode-{esc(c)}'><b><code>{esc(c)}</code></b> <span class='sub'>({esc(k.family)})</span> "
                     f"— <b>{len(rows)}</b> row{'' if len(rows) == 1 else 's'}: {esc(', '.join(rows))}"
                     f"<br><span class='sub'>{esc(k.means)}</span></li>")
    for c in free:
        rows = counts[c]
        lines.append(f"<li><code>{esc(c)}</code> — {len(rows)} row{'' if len(rows) == 1 else 's'} "
                     f"({esc(', '.join(rows))}), <b>not in the taxonomy</b>: free text, counted toward no mode</li>")
    n_coded = sum(len(v) for v in counts.values())
    return (f'<div class="slot"><h3>Failure taxonomy</h3><p><span class="when">Open</span> — {n_coded} labeled row'
            f"{'' if n_coded == 1 else 's'} carr{'ies' if n_coded == 1 else 'y'} a code, counted here per mode from the labels file. "
            f'The modes and their provenance live in the studio\'s taxonomy file; a row\'s code links to its mode.</p>'
            f'<ul class="modes">{"".join(lines)}</ul></div>')


def _meter_counts(m: dict[str, int]) -> str:
    """The split pair when the coordinator has it, otherwise the single total the runtime reported."""
    if "input" in m and "output" in m:
        return f"{m['input']:,} in · {m['output']:,} out · {m.get('cached', 0):,} cached"
    return f"{m.get('total', 0):,} total <span class='sub'>(as the runtime reported it, not split)</span>"


def _row(eng: Engagement, p: Record, v: Optional[str], ffs: Optional[int], crit: str, pair: Optional[str], blind: bool,
         code: str = "", tax: Optional[Taxonomy] = None) -> str:
    S = eng.studio
    pid = esc(p.pass_id)
    rt_html = f"<span class='hidden-rt'>{icon('eye')} hidden</span>" if blind else esc(p.runtime or "—")
    vcls = "unl" if not v else ("def" if v == "defer" else v)
    vlabel = {"pass": "pass", "fail": "fail", "defer": "deferred"}.get(v or "", "unlabeled")
    vicon = icon("check") if v == "pass" else (icon("cross") if v == "fail" else (icon("defer") if v == "defer" else icon("open")))
    tags = ""
    if p.triggered_by:
        tags += f"<span class='tag'>{icon('loop')} {esc(p.triggered_by)}</span>"
    if p.shadow_of:
        tags += f"<span class='tag'>shadow of {esc(p.shadow_of)}</span>"
    if pair and not p.shadow_of:
        tags += f"<span class='tag'>baseline of {esc(pair)}</span>"
    m, _ = normalize_meter(p.meter)
    # a meter is the split pair or a single `total` — what the Agent tool and the Codex footer report
    unmeasured = p.meter_source == "UNMEASURED" or "total" not in m
    tok = "—" if unmeasured else fmt_tokens(m["total"])
    summary = f"""
<summary>
  <span class="run"><b>Run {run_no(p.pass_id)}</b> · <span class="seat">{esc(S.seat_name(p.seat))}</span>{'' if S.seat_name(p.seat).lower().endswith(p.kind.lower()) else f' <span class="kind">{esc(p.kind)}</span>'}{tags}<span class="pid-sub">{pid}</span></span>
  <span class="kind">{esc(S.stage_label(p.stage))}</span>
  <span class="rt">{rt_html}</span>
  <span class="wc">{fmt_minutes(p.wall_clock_s)}</span>
  <span class="tok" title="input + output tokens">{tok}</span>
  <span class="verdict {vcls}" data-verdict-cell>{vicon}<span data-verdict-word>{vlabel}</span></span>
  <span class="crit" data-crit-cell>{esc(crit) if crit else ('<span class="ffs">' + (f'broke at {ffs} {esc(S.stage_name(ffs))}' if ffs else '') + '</span>')}</span>
</summary>"""
    inputs = "".join(f"<li>{esc(i.path)}<span class='hash'>{esc(i.sha256[:12])}…</span></li>" for i in p.inputs) or "<li class='sub'>none</li>"
    withheld = "".join(f"<li>{esc(w)}</li>" for w in p.withheld) or "<li class='sub'>none listed</li>"
    outputs = "".join(f"<li>{esc(o.path or o.id)}</li>" for o in p.outputs) or "<li class='sub'>none</li>"
    checks = "".join(f"<li><span>{esc(c.pass_id)}</span><span class='sub'>{esc(c.kind)}</span><span>{esc(c.verdict)}</span></li>" for c in p.checks) or "<li class='sub' style='display:block'>none recorded</li>"
    corpus = "".join(f"<li>{esc(c)}</li>" for c in p.corpus_read) or ("<li class='sub'>none (gate: corpus withheld)</li>" if p.kind == "gate" else "<li class='sub'>none</li>")
    moves = _moves_html(eng, p)
    if blind:
        meter_html = f"{_meter_counts(m)} <span class='sub'>(source {HIDDEN})</span>" if not unmeasured else "UNMEASURED"
        launch, raw_log = esc(HIDDEN), esc(HIDDEN)
    else:
        meter_html = "UNMEASURED" if unmeasured else f"{_meter_counts(m)} <span class='sub'>({esc(p.meter_source)})</span>"
        launch, raw_log = esc(p.launch or "—"), esc(p.raw_log or "—")
    ffs_opts = "".join(f"<option value='{s}'{' selected' if ffs == s else ''}>{s} {esc(S.stage_name(s))}</option>" for s in S.stage_numbers)
    blind_note = f"<p class='blind-note'>{icon('eye')} Blind pair with {esc(pair)}: the runtime and launch form stay hidden until both passes carry a verdict.</p>" if blind else ""
    form = f"""
<div class="label-form" data-label-form data-pass="{pid}">
  <div>
    <h4>Your verdict: pass / fail</h4>
    <div class="verdicts" role="group" aria-label="Verdict for {pid}">
      <button class="btn v-pass" type="button" data-set-verdict="pass" aria-pressed="{'true' if v == 'pass' else 'false'}">{icon('check')} pass <kbd>1</kbd></button>
      <button class="btn v-fail" type="button" data-set-verdict="fail" aria-pressed="{'true' if v == 'fail' else 'false'}">{icon('cross')} fail <kbd>2</kbd></button>
      <button class="btn v-defer" type="button" data-set-verdict="defer" aria-pressed="{'true' if v == 'defer' else 'false'}" title="Not a verdict: mark it to come back to">{icon('defer')} defer <kbd>d</kbd></button>
    </div>
  </div>
  <label>Where did the problem first enter the workflow? <kbd style="font-size:0.75rem">f</kbd>
    <select data-ffs {'disabled' if v != 'fail' else ''}><option value="">—</option>{ffs_opts}</select>
  </label>
  <label>What led to your judgment? Name the evidence and the consequence. <kbd style="font-size:0.75rem">c</kbd>
    <textarea data-crit rows="2">{esc(crit)}</textarea>
  </label>
  {blind_note}
  <div class="state"><span data-state>{'Deferred in the labels file; it still waits for a verdict.' if v == 'defer' else ('In the labels file.' if v else 'No label row yet.')}</span><span class="sub">{_code_state_html(code, tax)}</span></div>
</div>"""
    detail = f"""
<div class="detail">
  <div>
    <h4>Checks on this pass</h4><ul class="checks">{checks}</ul>
    <h4 style="margin-top:1rem">Corpus read (from the transcript)</h4><ul>{corpus}</ul>
  </div>
  <div>
    <h4>Moves</h4>{moves}
    <h4 style="margin-top:1rem">Notes</h4><p style="font-size:inherit">{esc(p.notes) or '<span class="sub">none</span>'}</p>
  </div>
  <details class="record-details">
  <summary>Record details</summary>
  <div class="record-grid">
  <div>
    <h4>Record</h4>
    <dl>
      <dt>launched</dt><dd>{esc(p.launched or '—')}</dd>
      <dt>completed</dt><dd>{esc(p.completed or '—')}</dd>
      <dt>runtime</dt><dd>{rt_html}</dd>
      <dt>launch form</dt><dd>{launch}</dd>
      <dt>effort</dt><dd>{esc(p.effort or '—')}</dd>
      <dt>wall-clock</dt><dd>{fmt_minutes(p.wall_clock_s)}</dd>
      <dt>meter</dt><dd>{meter_html}</dd>
      <dt>raw log</dt><dd>{raw_log}</dd>
      <dt>record</dt><dd>{esc(p.file.name)}</dd>
    </dl>
  </div>
  <div>
    <h4>Inputs, hashed</h4><ul>{inputs}</ul>
    <h4 style="margin-top:1rem">Withheld</h4><ul>{withheld}</ul>
    <h4 style="margin-top:1rem">Outputs</h4><ul>{outputs}</ul>
  </div>
  </div>
  </details>
  {form}
</div>"""
    return (f'<details class="pass v-{vcls}" id="{pid}" data-pass="{pid}" data-kind="{esc(p.kind)}" '
            f'data-verdict="{v or "unlabeled"}" data-pair="{esc(pair or "")}">{summary}{detail}</details>')


def _moves_html(eng: Engagement, p: Record) -> str:
    state = eng.moves_state(p)
    if state == "none-kind":
        return "<p class='sub' style='font-size:inherit'>No moves: this kind hands no artifact forward.</p>"
    if state == "superseded":
        return ("<p class='sub' style='font-size:inherit'>No moves on disk: the artifact was overwritten in place by a later pass; "
                "the pass records keep the history.</p>")
    mv = eng.moves_for(p)
    if state == "missing" or mv is None:
        return "<p class='sub' style='font-size:inherit'>No moves: not recorded.</p>"
    if mv.origin:
        leaned = "; ".join(esc(x) for x in mv.leaned_on) or "nothing named"
        return f"<p class='sub' style='font-size:inherit'>Origin draft, no upstream. Leaned on: {leaned}</p>"
    counts = mv.counts()
    counts_html = " ".join(f"<span><b>{counts[k]}</b> {k}</span>" for k in ("kept", "added", "split", "merged", "dropped"))
    lines = []
    for m in mv.lines:
        if m.op == "kept":
            continue
        what = m.item
        if m.op == "split":
            what = f"{m.item} → {', '.join(m.children)}"
        elif m.op == "merged":
            what = f"{' + '.join(m.items)} → {m.result}"
        src = m.source + (f"; {m.why}" if m.why else "")
        lines.append(f"<li><b>{esc(m.op)}</b>{esc(what)} <small>· {esc(src)}</small></li>")
    errs = "".join(f"<li class='sub'>{esc(e)}</li>" for e in mv.errors)
    return (f"<div class='movecounts'>{counts_html}</div><ul class='moves'>{''.join(lines) or '<li class=sub>only kept lines</li>'}{errs}</ul>"
            f"<p class='sub' style='font-size:inherit;margin-top:0.4rem'>Kept items are listed in the artifact's Moves section, not here.</p>")


# --------------------------------------------------------------------------- #
# assets: fonts, symbols, styles, script — the ratified prototype's, verbatim where possible
# --------------------------------------------------------------------------- #


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _fonts_css() -> str:
    anybody = FONTS_DIR / "anybody-latin-wdth-normal.woff2"
    schibsted = FONTS_DIR / "schibsted-grotesk-latin-wght-normal.woff2"
    css = ""
    if anybody.is_file():
        css += ("@font-face { font-family: 'Anybody'; font-style: normal; font-weight: 100 900; font-stretch: 50% 150%; font-display: swap;\n"
                f"  src: url(data:font/woff2;base64,{_b64(anybody)}) format('woff2'); }}\n")
    if schibsted.is_file():
        css += ("@font-face { font-family: 'Schibsted Grotesk'; font-style: normal; font-weight: 400 900; font-display: swap;\n"
                f"  src: url(data:font/woff2;base64,{_b64(schibsted)}) format('woff2'); }}\n")
    return css


SYMBOLS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-check" viewBox="0 0 14 14"><path d="M2.5 7.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-cross" viewBox="0 0 14 14"><path d="M3 3l8 8M11 3l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="i-defer" viewBox="0 0 14 14"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M4.8 7h4.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></symbol>
  <symbol id="i-open" viewBox="0 0 14 14"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 2"/></symbol>
  <symbol id="i-eye" viewBox="0 0 14 14"><path d="M1.5 7c1.6-2.6 3.4-3.8 5.5-3.8S10.9 4.4 12.5 7c-1.6 2.6-3.4 3.8-5.5 3.8S3.1 9.6 1.5 7z" fill="none" stroke="currentColor" stroke-width="1.3"/><circle cx="7" cy="7" r="1.6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M2.5 11.5l9-9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></symbol>
  <symbol id="i-loop" viewBox="0 0 14 14"><path d="M11 4H5a3 3 0 0 0 0 6h3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M9 2.5L11 4 9 5.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>"""

CSS = r"""
/* ---- tokens: portfolio DESIGN.md §2 / §2.1 / §4, verbatim ---- */
:root {
  --ground: #FBF6EC; --ink: #2A2622; --sub: #6E655B; --accent: #2F5D7C;
  --ink-hairline: color-mix(in srgb, var(--ink) 14%, transparent);
  --ink-wash-1: color-mix(in srgb, var(--ink) 6%, transparent);
  --ink-wash-2: color-mix(in srgb, var(--ink) 16%, transparent);
  --ink-wash-3: color-mix(in srgb, var(--ink) 30%, transparent);
  --ink-wash-4: color-mix(in srgb, var(--ink) 48%, transparent);
  --ground-cased: color-mix(in srgb, var(--ground) 88%, transparent);
  /* verdict buttons and the row's verdict word (DESIGN.md §15, Sean 2026-09-25): pass takes the portfolio's drafting ink, fail a red pencil */
  --verdict-pass: var(--accent); --verdict-fail: #9E3B2E;
  --font-display: 'Anybody', system-ui, sans-serif;
  --font-body: 'Schibsted Grotesk', system-ui, sans-serif;
  --fs-0: 0.8125rem; --fs-1: 0.9375rem; --fs-2: 1.0625rem; --fs-3: 1.25rem; --fs-4: 1.625rem; --fs-5: 2.375rem;
  --measure: 68ch; --gutter: 1.5rem; --row-x: 0.75rem;
  color-scheme: light;
}
:root[data-mode='dark'] { --ground: #191714; --ink: #F2EBDD; --sub: #8F867A; --accent: #6BA3C9; --verdict-fail: #D9857A; color-scheme: dark; }
@media (prefers-color-scheme: dark) { :root:not([data-mode='light']) { --ground: #191714; --ink: #F2EBDD; --sub: #8F867A; --accent: #6BA3C9; --verdict-fail: #D9857A; color-scheme: dark; } }

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
.rung { list-style: none; margin: 0.5rem 0 0; padding: 0; display: grid; gap: 0.5rem; font-size: var(--fs-0); }
.rung li { display: grid; grid-template-columns: 1rem 1fr auto; gap: 0.2rem 0.5rem; align-items: baseline; padding-bottom: 0.4rem; border-bottom: 1px solid var(--ink-hairline); }
.rung li:last-child { border-bottom: 0; }
.rung .what { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: baseline; }
.rung .state { color: var(--sub); text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.75rem; }
.rung .n { color: var(--sub); }
.rung .why { grid-column: 2 / -1; margin: 0.25rem 0 0; padding-left: 1rem; }
.rung .why li { display: list-item; list-style: disc; border: 0; padding: 0; }
.rung .implication { grid-column: 2 / -1; margin: 0.3rem 0 0; color: var(--sub); max-width: 60ch; }
.term { font-size: var(--fs-0); margin-top: 0.6rem; }
.term summary { color: var(--sub); cursor: pointer; }
.term p { margin-top: 0.4rem; }

/* what you are judging */
.judging { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1.5rem 2rem; margin-bottom: 1.5rem; }
.judging .stat h3 { font-size: var(--fs-0); font-family: var(--font-body); font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--sub); margin: 0 0 0.3rem; }
.judging .v { font-size: var(--fs-2); margin: 0 0 0.35rem; font-variant-numeric: tabular-nums; }
.judging .v b { font-weight: 600; }
.judging .s { font-size: var(--fs-0); color: var(--sub); margin: 0; }
.prompts { border-collapse: collapse; font-size: var(--fs-0); max-width: var(--measure); }
.prompts caption { text-align: left; color: var(--ink); padding-bottom: 0.4rem; }
.prompts th, .prompts td { border-top: 1px solid var(--ink-hairline); padding: 0.35rem 0.75rem 0.35rem 0; text-align: left; vertical-align: top; }
.prompts th { font-weight: 600; width: 5rem; }
.intro { font-size: var(--fs-1); max-width: var(--measure); margin-top: 0.25rem; }

/* guided reading */
.guided { margin-bottom: 1rem; }
.guided.empty p { max-width: var(--measure); }
.guided-intro { max-width: var(--measure); }
.guided .cap { max-width: var(--measure); color: var(--sub); font-size: var(--fs-0); }
.case-errors { border: 1px solid var(--ink); padding: 0.6rem 0.9rem; margin: 0.75rem 0; font-size: var(--fs-0); max-width: var(--measure); }
.case-errors ul { margin: 0.35rem 0 0; padding-left: 1.1rem; }
.case-links { display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem; font-size: var(--fs-0); margin: 0.75rem 0; }
.guided-tools { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-bottom: 1rem; font-size: var(--fs-0); }
.btn.file { position: relative; overflow: hidden; display: inline-flex; align-items: center; }
.btn.file input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
.chapters { border-top: 1px solid var(--ink); }
.chapter { border-bottom: 1px solid var(--ink-hairline); }
.chapter > summary { list-style: none; display: grid; grid-template-columns: 2.5rem 1fr auto; gap: 0.75rem; align-items: baseline; padding: 0.8rem var(--row-x); cursor: pointer; }
.chapter > summary::-webkit-details-marker { display: none; }
.chapter > summary:hover { background: var(--ink-wash-1); }
.chapter[open] > summary { background: var(--ink-wash-1); }
.chapter.current > summary { box-shadow: inset 0 -2px 0 0 var(--accent); }
.chapter .number { color: var(--sub); font-variant-numeric: tabular-nums; font-size: var(--fs-0); }
.chapter .ct { display: block; font-size: var(--fs-2); }
.chapter .chapter-title .sub { font-size: var(--fs-0); }
.pid-sub { font-size: 0.75rem; color: var(--sub); margin-left: 0.35rem; font-variant-numeric: tabular-nums; }
.assist-tag { border: 1px solid var(--ink-hairline); padding: 0 0.4rem; font-size: 0.75rem; color: var(--sub); text-transform: uppercase; letter-spacing: 0.04em; white-space: nowrap; }
.case-body { padding: 0.25rem var(--row-x) 1.75rem calc(var(--row-x) + 2.5rem + 0.75rem); max-width: 68ch; }
.case-body h4 { font-family: var(--font-body); font-size: var(--fs-0); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--sub); margin: 1.25rem 0 0.4rem; }
.case-body .focus { color: var(--sub); font-size: var(--fs-0); }
.case-body .story p, .case-body .reveal p, .help p { max-width: 68ch; }
.source { border-left: 2px solid var(--ink-wash-3); padding-left: 0.9rem; margin-bottom: 0.9rem; }
.source .prov { font-size: var(--fs-0); color: var(--sub); margin-bottom: 0.3rem; overflow-wrap: anywhere; }
.source blockquote { margin: 0; font-size: var(--fs-1); }
.source blockquote::before { content: "“"; } .source blockquote::after { content: "”"; }
.qualified { border: 1px dashed var(--ink-wash-3); padding: 0.4rem 0.6rem; font-size: var(--fs-0); }
.fingerprint { font-size: 0.75rem; color: var(--sub); margin-top: 0.4rem; }
.fingerprint summary { cursor: pointer; }
.fingerprint dl { display: grid; grid-template-columns: 11rem 1fr; gap: 0.1rem 0.5rem; margin: 0.3rem 0 0; }
.fingerprint dt { color: var(--sub); } .fingerprint dd { margin: 0; overflow-wrap: anywhere; }
.prov.sub { font-size: var(--fs-0); }
.reveal.open { border-top: 1px solid var(--ink-hairline); padding-top: 0.5rem; margin-top: 1rem; }
.help { border: 1px solid var(--ink-hairline); padding: 0.55rem 0.8rem; margin: 0.9rem 0; }
.help > summary { cursor: pointer; font-weight: 600; }
.help[open] > summary { margin-bottom: 0.5rem; }
.practice { border-top: 1px solid var(--ink-hairline); margin-top: 1.25rem; padding-top: 0.75rem; }
.practice fieldset { border: 0; margin: 0; padding: 0; }
.practice legend { padding: 0; margin-bottom: 0.4rem; }
.practice .choice { display: block; margin: 0.2rem 0; }
.practice .choice input { margin-right: 0.45rem; }
.practice .note-label { display: block; color: var(--sub); font-size: var(--fs-0); margin-top: 0.75rem; }
.practice textarea { display: block; width: 100%; box-sizing: border-box; margin-top: 0.25rem; background: transparent; color: var(--ink); border: 1px solid var(--ink-hairline); border-radius: 2px; padding: 0.35rem 0.5rem; font-size: var(--fs-1); resize: vertical; }
.practice .actions { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; margin: 0.6rem 0 0.4rem; }
.practice .sub { font-size: var(--fs-0); }
.chapter .locked[data-locked='1'] > summary { font-style: italic; }
.diagram { margin: 1rem 0; }
.diagram figcaption { font-size: var(--fs-0); color: var(--sub); margin-bottom: 0.35rem; }
.diagram svg { max-width: 100%; height: auto; font-family: var(--font-body); font-size: 12px; }
.diagram text { fill: var(--ink); }
.diagram .d-step, .diagram .d-decision, .diagram .d-branch { fill: var(--ink-wash-1); stroke: var(--ink-wash-3); stroke-width: 1; }
.diagram .d-decision { fill: var(--ink-wash-2); }
.diagram .d-branch { fill: none; stroke-dasharray: 3 3; }
.diagram .d-edge { stroke: var(--ink-wash-4); fill: none; stroke-width: 1.25; }
.diagram-text { font-size: var(--fs-0); color: var(--sub); margin: 0.4rem 0 0; padding-left: 1.1rem; }
.terms { display: grid; grid-template-columns: auto 1fr; gap: 0.15rem 0.75rem; font-size: var(--fs-0); margin: 1rem 0 0; border-top: 1px solid var(--ink-hairline); padding-top: 0.6rem; }
.terms dt { font-weight: 600; } .terms dd { margin: 0; color: var(--sub); }
.case-foot { font-size: var(--fs-0); margin-top: 1rem; }
.practice-fallback { font-size: var(--fs-0); color: var(--sub); }
.practice-fallback textarea { width: 100%; box-sizing: border-box; background: transparent; color: var(--ink); border: 1px solid var(--ink-hairline); margin-top: 0.4rem; }

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
.pass summary { list-style: none; display: grid; grid-template-columns: 21rem 6rem 9rem 4rem 4rem 5.5rem 1fr; gap: 0 0.75rem; align-items: center; padding: 0.55rem var(--row-x); cursor: pointer; font-size: var(--fs-0); position: relative; }
.pass summary .run b { font-weight: 600; }
.pass summary .run .seat { color: var(--ink); }
.pass summary::-webkit-details-marker { display: none; }
.pass summary:hover { background: var(--ink-wash-1); }
.pass.current summary { box-shadow: inset 0 -2px 0 0 var(--accent); }
.pass summary .pid { font-weight: 600; color: var(--ink); }
.pass summary .kind { color: var(--sub); }
.pass summary .verdict { display: inline-flex; align-items: center; gap: 0.35rem; font-weight: 600; }
.pass summary .verdict.unl { color: var(--sub); font-weight: 400; }
.pass summary .verdict.def { color: var(--sub); font-weight: 400; font-style: italic; }
/* §15 (Sean, 2026-09-25, second ruling): the row's verdict word carries the same color as its button */
.pass summary .verdict.pass { color: var(--verdict-pass); }
.pass summary .verdict.fail { color: var(--verdict-fail); }
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
/* §15: pass and fail are the two decisions, so they are larger than every other button and carry their color; defer stays ink and ordinary size */
.verdicts .btn.v-pass, .verdicts .btn.v-fail { padding: 0.5rem 1rem; font-size: var(--fs-1); font-weight: 600; border-width: 1.5px; }
.verdicts .btn.v-pass { color: var(--verdict-pass); border-color: var(--verdict-pass); }
.verdicts .btn.v-fail { color: var(--verdict-fail); border-color: var(--verdict-fail); }
.verdicts .btn.v-pass:hover { background: color-mix(in srgb, var(--verdict-pass) 10%, transparent); }
.verdicts .btn.v-fail:hover { background: color-mix(in srgb, var(--verdict-fail) 10%, transparent); }
.verdicts .btn.v-pass[aria-pressed='true'] { background: var(--verdict-pass); border-color: var(--verdict-pass); color: var(--ground); }
.verdicts .btn.v-fail[aria-pressed='true'] { background: var(--verdict-fail); border-color: var(--verdict-fail); color: var(--ground); }
.verdicts .btn.v-pass kbd, .verdicts .btn.v-fail kbd { color: inherit; border-color: currentColor; opacity: 0.7; }
.verdicts .btn.v-defer { align-self: center; }
.label-form label { display: grid; gap: 0.25rem; color: var(--sub); }
.label-form select, .label-form textarea { background: transparent; border: 1px solid var(--ink-hairline); padding: 0.35rem 0.5rem; border-radius: 2px; color: var(--ink); }
.label-form textarea { width: 100%; min-height: 3.6rem; resize: vertical; box-sizing: border-box; }
.label-form select:focus, .label-form textarea:focus { border-color: var(--ink); box-shadow: none; }
.label-form .state { grid-column: 1 / -1; color: var(--sub); display: flex; gap: 1rem; align-items: center; }
.label-form .state .draft { color: var(--ink); }
.blind-note { grid-column: 1 / -1; color: var(--sub); }
.record-details { grid-column: 1 / -1; border-top: 1px solid var(--ink-hairline); padding-top: 0.6rem; }
.record-details > summary { cursor: pointer; color: var(--sub); text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; font-size: var(--fs-0); }
.record-details[open] > summary { margin-bottom: 0.7rem; }
.record-grid { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 1.25rem 2.5rem; }
.takeaways { list-style: none; margin: 0.5rem 0 0; padding: 0; font-size: var(--fs-0); display: grid; gap: 0.45rem; }
.takeaways li { border-left: 2px solid var(--ink-wash-2); padding-left: 0.6rem; }
.takeaways b { font-weight: 600; }
.history { font-size: var(--fs-0); margin-top: 0.7rem; }
.history summary { cursor: pointer; color: var(--sub); }
.history .takeaways { max-height: 28rem; overflow-y: auto; }

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
  .broke, .slots, .detail, .record-grid, .judging { grid-template-columns: 1fr; }
  .judging { gap: 1rem; }
  .pass summary { grid-template-columns: 1fr 5.5rem; }
  .pass summary .wc, .pass summary .tok, .pass summary .rt, .pass summary .ffs, .pass summary .crit { display: none; }
  .pass summary > .kind { display: none; }
  .case-body { padding-left: var(--row-x); }
}
@media print {
  :root { --ground: #FBF6EC; --ink: #2A2622; --sub: #6E655B; --accent: #2F5D7C; }
  html { font-size: 11px; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .tools, .filters, .label-form, .btn, dialog, .guided-tools, .practice .actions, .practice-fallback { display: none !important; }
  .pass, .fails li, .matrix, .stages, .train, .chapter, .source, .diagram { break-inside: avoid; }
  .pass summary, .chapter > summary { cursor: default; }
  .practice textarea { border: 1px solid var(--ink-hairline); min-height: 3rem; }
  h2 { break-after: avoid; }
}
"""

JS = r"""
(function () {
  const KEY = 'trace-labels:' + TRACE_ENG;
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

  // ---- drafts: browser-only, never the ledger ----
  let drafts = {}; try { drafts = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { drafts = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(drafts)); } catch (e) {} };
  const rows = $$('details.pass');
  const fileVerdict = (row) => row.dataset.verdict === 'unlabeled' ? null : row.dataset.verdict;
  const effVerdict = (row) => (drafts[row.dataset.pass] && drafts[row.dataset.pass].verdict) || fileVerdict(row);

  function paint(row) {
    const pid = row.dataset.pass, d = drafts[pid] || {};
    const v = effVerdict(row);
    const cell = $('[data-verdict-cell]', row), word = $('[data-verdict-word]', row);
    cell.className = 'verdict ' + (v === 'defer' ? 'def' : (v || 'unl'));
    word.textContent = v === 'defer' ? 'deferred' : (v || 'unlabeled');
    const ico = $('svg use', cell); ico.setAttribute('href', v === 'pass' ? '#i-check' : v === 'fail' ? '#i-cross' : v === 'defer' ? '#i-defer' : '#i-open');
    row.classList.toggle('v-fail', v === 'fail'); row.classList.toggle('v-pass', v === 'pass'); row.classList.toggle('v-def', v === 'defer'); row.classList.toggle('v-unl', !v);
    $$('[data-set-verdict]', row).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setVerdict === v)));
    const sel = $('[data-ffs]', row); sel.disabled = v !== 'fail'; if (d.ffs !== undefined) sel.value = d.ffs;
    const ta = $('[data-crit]', row); if (d.crit !== undefined && document.activeElement !== ta) ta.value = d.crit;
    const critCell = $('[data-crit-cell]', row); const crit = d.crit !== undefined ? d.crit : ta.value;
    if (crit) critCell.textContent = crit;
    const st = $('[data-state]', row);
    st.innerHTML = d.verdict || d.crit !== undefined || d.ffs !== undefined
      ? (d.verdict === 'defer' ? '<span class="draft">Deferred here, to come back to; not yet in the labels file.</span>' : '<span class="draft">Drafted here, not yet in the labels file.</span>')
      : (fileVerdict(row) === 'defer' ? 'Deferred in the labels file; it still waits for a verdict.' : (fileVerdict(row) ? 'In the labels file.' : 'No label row yet.'));
  }
  function paintBlind() {
    // The hidden runtime is not in this file (DESIGN.md §8): both verdicts drafted here only earn the note.
    rows.forEach(row => { const pair = row.dataset.pair; if (!pair) return;
      const other = document.getElementById(pair); if (!other) return;
      const decided = v => v === 'pass' || v === 'fail';   // a defer never reveals (DESIGN.md §15)
      const both = decided(effVerdict(row)) && decided(effVerdict(other));
      if (both) $$('.hidden-rt', row).forEach(el => { el.outerHTML = '<span class="sub">revealed on the next render, once both labels are in the file</span>'; });
    });
  }
  function counters() {
    const isDecided = v => v === 'pass' || v === 'fail';
    const fileN = rows.filter(r => isDecided(fileVerdict(r))).length;
    const draftN = rows.filter(r => !isDecided(fileVerdict(r)) && drafts[r.dataset.pass] && isDecided(drafts[r.dataset.pass].verdict)).length;
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

  // ---- export: rows for the labels file, in its column order ----
  $('#copy-labels').addEventListener('click', async () => {
    const lines = ['| pass | verdict | first_failing_stage | critique | failure_code |', '|---|---|---|---|---|'];
    rows.forEach(row => { const d = drafts[row.dataset.pass]; if (!d) return; const v = d.verdict || fileVerdict(row) || '';
      lines.push(`| ${row.dataset.pass} | ${v} | ${v === 'fail' ? (d.ffs || '') : ''} | ${(d.crit !== undefined ? d.crit : $('[data-crit]', row).value).replace(/\|/g, '\\|').replace(/\n/g, ' ')} |  |`); });
    const text = lines.join('\n');
    try { await navigator.clipboard.writeText(text); } catch (e) { window.prompt('Copy these rows', text); }
    const b = $('#copy-labels'); const t = b.firstChild.textContent; b.firstChild.textContent = 'Copied '; setTimeout(() => { b.firstChild.textContent = t; }, 1200);
  });

  // ---- filters: hide rows, repaint nothing ----
  $$('[data-filter]').forEach(b => b.addEventListener('click', () => {
    $$('[data-filter]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    const f = b.dataset.filter;
    let shown = 0;
    rows.forEach(r => { const v = effVerdict(r);
      r.hidden = !(f === 'all' || (f === 'fail' && v === 'fail') || (f === 'unlabeled' && !v) || (f === 'deferred' && v === 'defer') || (f === 'pairs' && r.dataset.pair)); if (!r.hidden) shown++; });
    let empty = $('#no-match'); if (!empty) { empty = document.createElement('p'); empty.id = 'no-match'; empty.className = 'sub'; empty.style.padding = '1rem 0'; empty.textContent = 'No passes match'; $('#passes').appendChild(empty); }
    empty.hidden = shown > 0;
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
    // j/k walk the guided cases while the reader is inside them, and the pass rows everywhere else
    const inGuided = document.activeElement && document.activeElement.closest && document.activeElement.closest('#guided');
    if (inGuided && (e.key === 'j' || e.key === 'k')) {
      e.preventDefault();
      const here = document.activeElement.closest('details.chapter');
      let i = chapters.indexOf(here); if (i < 0) i = e.key === 'j' ? -1 : chapters.length;
      i = Math.max(0, Math.min(chapters.length - 1, i + (e.key === 'j' ? 1 : -1)));
      const next = chapters[i]; if (!next) return;
      chapters.forEach(c => c.classList.remove('current')); next.classList.add('current');
      next.scrollIntoView({ block: 'nearest' }); $('summary', next).focus({ preventScroll: true });
      return;
    }
    const vis = visible(); const vi = vis.indexOf(curRow());
    switch (e.key) {
      case 'j': case 'ArrowDown': e.preventDefault(); setCur(vi + 1); break;
      case 'k': case 'ArrowUp': e.preventDefault(); setCur(vi - 1); break;
      case 'Enter': if (curRow() && document.activeElement === $('summary', curRow())) { e.preventDefault(); curRow().open = !curRow().open; } break;
      case '1': if (curRow()) setVerdict(curRow(), 'pass'); break;
      case '2': if (curRow()) setVerdict(curRow(), 'fail'); break;
      case 'd': if (curRow()) setVerdict(curRow(), 'defer'); break;
      case 'f': if (curRow()) { e.preventDefault(); curRow().open = true; $('[data-ffs]', curRow()).focus(); } break;
      case 'c': if (curRow()) { e.preventDefault(); curRow().open = true; $('[data-crit]', curRow()).focus(); } break;
      case 'u': { e.preventDefault(); const next = vis.find((r, i) => i > vi && !effVerdict(r)) || vis.find(r => !effVerdict(r)); if (next) setCur(vis.indexOf(next)); break; }
      case '?': e.preventDefault(); $('#keys').showModal(); break;
    }
  });
  rows.forEach((r) => $('summary', r).addEventListener('focus', () => { rows.forEach(x => x.classList.remove('current')); r.classList.add('current'); cur = rows.indexOf(r); }));
  $('#help').addEventListener('click', () => $('#keys').showModal());
  $$('[data-jump]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href').slice(1); const row = document.getElementById(id); if (!row) return; e.preventDefault(); row.open = true; setCur(rows.indexOf(row)); }));

  // ---- practice journal: the reader's own learning notes, never the labels file ----
  const PKEY = 'trace-practice:' + TRACE_ENG;
  const chapters = $$('details.chapter');
  const now = () => new Date().toISOString();
  let practice = {}; try { practice = JSON.parse(localStorage.getItem(PKEY) || '{}'); } catch (e) { practice = {}; }
  let practiceOK = true;
  const psave = () => { try { localStorage.setItem(PKEY, JSON.stringify(practice)); } catch (e) { practiceOK = false; } };
  const pentry = (k) => (practice[k] = Object.assign({ choice: '', label: '', note: '', bookmarked: false, exposures: [], first: null, latest: null }, practice[k]));
  const chKey = (ch) => ch.dataset.case;

  function unlock(ch) { $$('[data-locked]', ch).forEach(d => { d.removeAttribute('data-locked'); d.open = true; }); }
  function expose(ch, kind) { const e = pentry(chKey(ch)); if (!e.exposures.includes(kind)) { e.exposures.push(kind); psave(); paintPractice(ch); } }

  function paintPractice(ch) {
    const e = pentry(chKey(ch));
    const box = $('[data-practice]', ch); if (!box) return;
    $$('[data-choice]', box).forEach(i => { i.checked = i.value === e.choice; });
    const ta = $('[data-practice-note]', box);
    if (ta && document.activeElement !== ta) ta.value = e.note;
    const bm = $('[data-practice-bookmark]', box);
    if (bm) { bm.setAttribute('aria-pressed', String(!!e.bookmarked)); bm.textContent = e.bookmarked ? 'Marked to come back to' : 'Come back to this'; }
    const st = $('[data-practice-state]', box);
    if (st) {
      const dirty = e.latest && (e.latest.choice !== e.choice || e.latest.note !== e.note);
      let msg = e.latest ? (dirty ? 'Changed since your last saved answer.' : 'Answer saved in this browser.')
        : (e.choice || e.note ? 'Draft kept in this browser. Save it when you are ready.' : 'Nothing saved yet.');
      if (e.first && e.latest && e.first.at !== e.latest.at) msg += ' Your first answer is kept.';
      if (e.exposures.length) msg += ' Help opened: ' + e.exposures.join(', ') + '.';
      if (!practiceOK) msg += ' This browser will not keep notes between visits — download a backup.';
      st.textContent = msg;
    }
    if (e.choice || (e.latest && e.latest.choice)) unlock(ch);
  }

  chapters.forEach(ch => {
    const box = $('[data-practice]', ch);
    if (box) {
      $$('[data-choice]', box).forEach(inp => inp.addEventListener('change', () => {
        const e = pentry(chKey(ch)); e.choice = inp.value; e.label = inp.dataset.label || inp.value; psave(); unlock(ch); paintPractice(ch); practiceStatus();
      }));
      const ta = $('[data-practice-note]', box);
      if (ta) ta.addEventListener('input', () => { pentry(chKey(ch)).note = ta.value; psave(); paintPractice(ch); practiceStatus(); });
      const bm = $('[data-practice-bookmark]', box);
      if (bm) bm.addEventListener('click', () => { const e = pentry(chKey(ch)); e.bookmarked = !e.bookmarked; psave(); paintPractice(ch); practiceStatus(); });
      const sv = $('[data-practice-save]', box);
      if (sv) sv.addEventListener('click', () => {
        const e = pentry(chKey(ch));
        if (!e.choice && !e.note.trim()) { $('[data-practice-state]', box).textContent = 'Write an answer, or pick an option, before saving.'; return; }
        const snap = { choice: e.choice, label: e.label, note: e.note, at: now(), helpBefore: e.exposures.slice() };
        if (!e.first) e.first = snap; e.latest = snap; e.bookmarked = false; psave(); paintPractice(ch); practiceStatus();
      });
    }
    $$('[data-exposure]', ch).forEach(d => d.addEventListener('toggle', () => { if (d.open) expose(ch, d.dataset.exposure); }));
    if (ch.dataset.assist === 'worked') expose(ch, 'worked-example');
    paintPractice(ch);
  });

  function practiceMarkdown() {
    const out = ['# Practice notes — ' + TRACE_ENG, '', 'Written while reading the guided cases. These are learning notes, not labels: no verdict on this page was set by any of them.', ''];
    chapters.forEach(ch => {
      const e = pentry(chKey(ch));
      out.push('## ' + (ch.dataset.title || chKey(ch)), '', (ch.dataset.run || '') + ' · ' + (ch.dataset.pass || '') + ' · assistance: ' + ch.dataset.assist, '');
      if (e.latest) {
        out.push('Answer: ' + (e.latest.label || e.latest.choice || '(no option chosen)'), '', e.latest.note || '(no note)', '', 'Saved: ' + e.latest.at, 'Help opened before it: ' + (e.latest.helpBefore.join(', ') || 'none'), '');
        if (e.first && e.first.at !== e.latest.at) out.push('First answer: ' + (e.first.label || e.first.choice || '(none)') + ' — ' + (e.first.note || '(no note)') + ' (' + e.first.at + ')', '');
      } else if (e.choice || e.note) {
        out.push('Unsaved draft: ' + (e.label || e.choice || '(no option chosen)'), '', e.note || '(no note)', '');
      } else out.push('No answer yet.', '');
      if (e.bookmarked) out.push('Marked to come back to.', '');
      const srcs = $$('[data-src]', ch).map(s => '- ' + s.dataset.src);
      if (srcs.length) out.push('Sources:', ...srcs, '');
    });
    out.push('Help opened here is a record of this page only; it cannot show what was read elsewhere.', '');
    return out.join('\n');
  }
  function practiceStatus() {
    const saved = chapters.filter(ch => pentry(chKey(ch)).latest).length;
    const el = $('#practice-status'); if (!el) return;
    el.textContent = saved ? saved + ' of ' + chapters.length + ' cases answered' : 'Nothing practised yet.';
    const t = $('#practice-text'); if (t) t.value = practiceMarkdown();
  }
  function download(text, type, name) {
    const url = URL.createObjectURL(new Blob([text], { type }));
    const a = document.createElement('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  if ($('#copy-practice')) {
    $('#copy-practice').addEventListener('click', async () => {
      const text = practiceMarkdown();
      try { await navigator.clipboard.writeText(text); $('#practice-status').textContent = 'Practice notes copied.'; }
      catch (e) { const f = $('.practice-fallback'); f.open = true; $('#practice-text').value = text; $('#practice-text').select(); $('#practice-status').textContent = 'Copying is blocked here; the notes are selected below.'; }
    });
    $('#download-practice').addEventListener('click', () => download(JSON.stringify(practice, null, 2), 'application/json', TRACE_ENG + '-practice.json'));
    $('#restore-practice').addEventListener('change', async ev => {
      const f = ev.target.files && ev.target.files[0]; if (!f) return;
      try {
        if (f.size > 4000000) throw new Error('too large');
        const incoming = JSON.parse(await f.text());
        if (!incoming || typeof incoming !== 'object' || Array.isArray(incoming)) throw new Error('not a backup');
        Object.keys(incoming).forEach(k => { if (!practice[k] || (!practice[k].latest && !practice[k].note)) practice[k] = incoming[k]; });
        psave(); chapters.forEach(paintPractice); practiceStatus();
        $('#practice-status').textContent = 'Backup restored. Answers already written here were kept.';
      } catch (e) { $('#practice-status').textContent = 'That file could not be read as a practice backup. Your notes were kept.'; }
      ev.target.value = '';
    });
    practiceStatus();
  }
  $$('[data-case-link]').forEach(a => a.addEventListener('click', e => {
    const ch = document.getElementById(a.getAttribute('href').slice(1)); if (!ch) return;
    e.preventDefault(); ch.open = true; ch.scrollIntoView({ block: 'start' }); $('summary', ch).focus({ preventScroll: true });
  }));

  // ---- print: unfold everything, restore after ----
  let wasOpen = [];
  let chaptersOpen = [];
  window.addEventListener('beforeprint', () => {
    wasOpen = rows.map(r => r.open); rows.forEach(r => r.open = true);
    chaptersOpen = chapters.map(c => c.open); chapters.forEach(c => c.open = true);
  });
  window.addEventListener('afterprint', () => {
    rows.forEach((r, i) => r.open = wasOpen[i]);
    chapters.forEach((c, i) => c.open = chaptersOpen[i]);
  });
})();
"""
