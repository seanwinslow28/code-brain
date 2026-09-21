"""Rung 0 of the ladder — deterministic checks, no model, no network (#272 decision 7).

Each check prints pass or fail with a count. A finding names the pass and the
thing, so the coordinator can fix the record rather than guess. What rung 0
cannot verify (an item only present in a superseded revision, which the
overwrite-in-place rule of #274 leaves unreadable) is counted and reported as
unverifiable, never quietly passed and never failed: a replay check over the
raw transcript is a later rung.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .engagement import (
    FIXED_AUDITORS, METER_SOURCES, REPO_PREFIXES as _REPO_PREFIXES, REQUIRED_COSIGNS, STAGE_SEATS,
    Engagement, Record, normalize_meter, sha256_path,
)
from .moves import extract_ids

__all__ = ["CHECK_NAMES", "Check", "run_checks", "format_report", "row_block"]

CHECK_NAMES = (
    "Records parse and carry every required field",
    "Every pass has a record",
    "Every pass has a label row",
    "Input hashes match disk or a recorded prior revision",
    "Cited corpus files appear in the transcript's file reads",
    "Every move names an existing upstream item; splits are subsets",
    "Meter present or UNMEASURED",
    "Each drafting stage has one draft, an audit, and its required co-signs",
    "Trials blind-labeled before their runtime is shown",
)

_CORPUS_PATH = re.compile(r"(?<![\w/])((?:productcraft/|systemcraft/)?corpus/[\w\-./]+?\.md)")
_STAGE_NAMES = {0: "close", 1: "Strategist", 2: "Discovery", 3: "Insights", 4: "Growth", 5: "Business", 6: "Delivery", 7: "Leadership"}


@dataclass
class Check:
    name: str
    n_ok: int = 0
    n_total: int = 0
    findings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    n_unverifiable: int = 0

    @property
    def ok(self) -> bool:
        return not self.findings

    @property
    def count(self) -> str:
        return f"{self.n_ok} of {self.n_total}"


def run_checks(eng: Engagement) -> list[Check]:
    return [
        _records_parse(eng),
        _every_pass_has_a_record(eng),
        _every_pass_has_a_label(eng),
        _hashes(eng),
        _corpus(eng),
        _moves(eng),
        _meter(eng),
        _stages(eng),
        _blind(eng),
    ]


def format_report(checks: list[Check]) -> str:
    out = []
    for c in checks:
        out.append(f"{'PASS' if c.ok else 'FAIL'}  {c.name}  {c.count}")
        for f in c.findings:
            out.append(f"  - {f}")
        for n in c.notes:
            out.append(f"  · {n}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# 0 · parse
# --------------------------------------------------------------------------- #


def _records_parse(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[0], n_total=len(eng.records) + sum(1 for e in eng.errors if e.startswith("pass-")))
    for e in eng.errors:
        if e.startswith("pass-"):
            c.findings.append(e)
    for r in eng.records:
        if r.errors:
            c.findings.extend(r.errors)
        else:
            c.n_ok += 1
    if eng.labels_error:
        c.findings.append(f"labels.md: {eng.labels_error}")
    for e in eng.errors:
        if e.startswith("brief.md"):
            c.findings.append(e)
    return c


# --------------------------------------------------------------------------- #
# 1 · every pass has a record
# --------------------------------------------------------------------------- #


def _every_pass_has_a_record(eng: Engagement) -> Check:
    ids = [r.pass_id for r in eng.records]
    have = set(ids)
    nums = sorted(int(m.group(1)) for i in ids if (m := re.match(r"^pass-(\d+)$", i)))
    expected = [f"pass-{n:02d}" for n in range(1, (nums[-1] if nums else 0) + 1)]
    referenced: dict[str, set[str]] = {}
    for r in eng.records:
        for ref in [r.triggered_by, r.shadow_of] + [ch.pass_id for ch in r.checks]:
            if ref:
                referenced.setdefault(ref, set()).add(r.pass_id)
    for pid in eng.labels:
        referenced.setdefault(pid, set()).add("labels.md")
    universe = sorted(set(expected) | have | set(referenced))
    c = Check(CHECK_NAMES[1], n_total=len(universe))
    for pid in universe:
        if pid in have:
            c.n_ok += 1
            continue
        by = ", ".join(sorted(referenced.get(pid, ()))) or "the numbering"
        c.findings.append(f"{pid} has no record (referenced by {by})")
    for r in eng.records:
        for e in r.errors:
            if "filename" in e:
                c.findings.append(e)
    return c


# --------------------------------------------------------------------------- #
# 2 · every pass has a label row
# --------------------------------------------------------------------------- #


def _every_pass_has_a_label(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[2], n_total=len(eng.records))
    have = eng.by_id
    for r in eng.records:
        if r.pass_id in eng.labels:
            c.n_ok += 1
        else:
            c.findings.append(f"{r.pass_id} has no row in labels.md")
    for pid in eng.labels:
        if pid not in have:
            c.findings.append(f"labels.md has a row for {pid}, which has no record")
    unlabeled = [r.pass_id for r in eng.records if r.pass_id in eng.labels and eng.labels[r.pass_id].verdict is None]
    if unlabeled:
        c.notes.append(f"{len(unlabeled)} row(s) still wait for a verdict: {', '.join(unlabeled)}")
    return c


# --------------------------------------------------------------------------- #
# 3 · hashes
# --------------------------------------------------------------------------- #


def _machinery_paths(eng: Engagement) -> set[str]:
    """Inputs that are shared repo machinery rather than links in this engagement's chain.

    A seat's inputs include the studio's own files — its seat contract, a lane
    manifest, an artifact template. Those live in the repo, outside the engagement,
    and they keep improving after a train closes: the ticket that fixes a template
    is doing its job, not tampering with a record. The recorded hash is provenance
    (what the seat saw), not a chain link, so a moved machinery file is *unverifiable*
    here — counted and named, never quietly passed and never failed, the same way an
    overwritten revision's Moves are. A repo path that some pass recorded as an
    output is not machinery: the engagement wrote it, so it stays in the chain.

    The limit, stated plainly: this cannot tell a template edited *between* two
    passes of a live train from one edited a month after Close. Mid-train, the
    engagement's own `## Notes` is where that belongs.
    """
    written = {o.path for r in eng.records for o in r.artifact_outputs}
    return {
        i.path for r in eng.records for i in r.inputs
        if i.path.startswith(_REPO_PREFIXES) and i.path not in written
    }


def _hashes(eng: Engagement) -> Check:
    """Inputs match disk, or match a revision an earlier pass recorded as its output — and in that
    case the disk must hold the *last* recorded revision, otherwise the file was edited outside a pass."""
    c = Check(CHECK_NAMES[3])
    history: dict[str, dict[str, str]] = {}   # path → {sha256: pass id that wrote it}
    last: dict[str, tuple[str, str]] = {}     # path → (sha256, pass id) of the latest recorded output
    for r in eng.records:                     # pass order, so history holds every recorded revision
        for o in r.artifact_outputs:
            if o.sha256:
                history.setdefault(o.path, {})[o.sha256] = r.pass_id
                last[o.path] = (o.sha256, r.pass_id)
    machinery = _machinery_paths(eng)
    moved: dict[str, set[str]] = {}
    superseded = 0
    for r in eng.records:
        for i in r.inputs:
            c.n_total += 1
            disk = eng.hash_of(i.path)
            if disk is None:
                c.findings.append(f"{r.pass_id}: input {i.path} is missing on disk")
            elif not re.fullmatch(r"[0-9a-f]{64}", i.sha256):
                c.findings.append(f"{r.pass_id}: input {i.path} has no sha256 (got {i.sha256!r})")
            elif i.sha256 == disk:
                c.n_ok += 1
            elif i.path in machinery:
                c.n_unverifiable += 1
                moved.setdefault(i.path, set()).add(r.pass_id)
            elif i.sha256 in history.get(i.path, {}):
                if i.path in last and disk == last[i.path][0]:
                    c.n_ok += 1
                    superseded += 1
                else:
                    writer = last[i.path][1] if i.path in last else history[i.path][i.sha256]
                    c.findings.append(
                        f"{r.pass_id}: input {i.path} was edited after {writer} wrote it: the disk hash matches no recorded output"
                    )
            else:
                c.findings.append(
                    f"{r.pass_id}: input {i.path} hash no longer matches disk and no earlier pass recorded it as an output"
                )
        for o in r.artifact_outputs:
            if not o.sha256:
                continue
            c.n_total += 1
            disk = eng.hash_of(o.path)
            if disk is None:
                c.findings.append(f"{r.pass_id}: output {o.path} is missing on disk")
            elif disk == o.sha256 or (o.path in last and last[o.path][1] != r.pass_id and disk == last[o.path][0]):
                c.n_ok += 1
            else:
                c.findings.append(
                    f"{r.pass_id}: output {o.path} was edited after the pass: the disk hash matches no recorded output"
                )
    if superseded:
        c.notes.append(f"{superseded} input(s) matched a superseded revision an earlier pass recorded as its output")
    if moved:
        c.notes.append(
            f"{c.n_unverifiable} input(s) are shared repo machinery that has moved since the pass "
            f"({len(moved)} file(s)): {', '.join(sorted(moved))}. The record keeps the hash the seat saw — "
            f"unverifiable at rung 0, never rewritten to match."
        )
    return c


# --------------------------------------------------------------------------- #
# 4 · corpus
# --------------------------------------------------------------------------- #


def _prior_reads(eng: Engagement) -> dict[str, dict[str, set[str]]]:
    """Per pass, the corpus reads an earlier revision of each output path can account for.

    Artifacts are redrafted in place (#274), so a repair that fixed one paragraph still
    hands back a file carrying every citation its earlier revisions made. Charging the
    repairing pass with reading all of them would be a false finding — the read happened,
    in the pass that wrote the line. So a citation is satisfied by this pass's own
    `## Corpus read` or by that of any earlier pass which recorded the same path as an
    output. Reads never travel sideways: only along one artifact's own revision chain.
    """
    seen: dict[str, set[str]] = {}                  # path → reads recorded by earlier writers of it
    out: dict[str, dict[str, set[str]]] = {}        # pass id → path → those reads
    for r in eng.records:                           # eng.records is in pass order
        paths = [o.path for o in r.artifact_outputs]
        out[r.pass_id] = {path: set(seen.get(path, ())) for path in paths}
        for path in paths:
            seen.setdefault(path, set()).update(r.corpus_read)
    return out


def _same_file(a: str, b: str) -> bool:
    """`corpus/canon/x.md` and `productcraft/corpus/canon/x.md` are the same read."""
    return a == b or a.split("corpus/", 1)[-1] == b.split("corpus/", 1)[-1]


def _corpus(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[4])
    skipped_superseded = 0
    inherited = 0
    prior = _prior_reads(eng)
    for r in eng.records:
        if not r.hands_forward:
            continue
        own = set(r.corpus_read)
        cited: dict[str, set[str]] = {}   # corpus path → the reads that may account for it
        grounding = None
        grounding_reads = set(own)
        for o in r.outputs:
            text = None
            reads = set(own)
            if o.path:
                if eng.output_state(o) == "superseded":
                    skipped_superseded += 1
                    continue  # a later revision is on disk; its citations are that pass's, not this one's
                reads |= prior.get(r.pass_id, {}).get(o.path, set())
                grounding_reads |= reads
                text = eng.read_text(o.path)
                if text is not None and grounding is None:
                    m = re.search(r"^grounding:\s*(\S+)", text, re.M)
                    grounding = m.group(1) if m else None
            elif o.id:
                p = eng.entry_path(o.id)
                text = p.read_text(encoding="utf-8") if p else None
            if text:
                for path in _CORPUS_PATH.findall(text):
                    cited.setdefault(path, set()).update(reads)
        for path in sorted(cited):
            c.n_total += 1
            accounted = [x for x in cited[path] if _same_file(x, path)]
            if accounted:
                c.n_ok += 1
                if not any(_same_file(x, path) for x in own):
                    inherited += 1
            else:
                c.findings.append(
                    f"{r.pass_id}: cites {path} but neither this pass's transcript nor any earlier "
                    f"revision of the artifact shows a read of it"
                )
        corpus_opened = [x for x in grounding_reads if "corpus/" in x]
        if grounding == "full" and not corpus_opened:
            c.findings.append(f"{r.pass_id}: artifact declares grounding: full but the transcript shows no corpus read")
        if grounding == "none" and [x for x in own if "corpus/" in x]:
            c.findings.append(f"{r.pass_id}: artifact declares grounding: none but the transcript shows corpus reads")
    if skipped_superseded:
        c.notes.append(f"{skipped_superseded} superseded artifact revision(s) not on disk: their citations are not re-checked")
    if inherited:
        c.notes.append(
            f"{inherited} citation(s) accounted for by an earlier revision's pass, not this one's — the artifact was "
            f"redrafted in place and kept the line"
        )
    return c


# --------------------------------------------------------------------------- #
# 5 · moves
# --------------------------------------------------------------------------- #


def _upstream_texts(eng: Engagement, r: Record) -> tuple[list[str], bool]:
    """Readable inputs at their recorded hash; flag whether any input is unreadable at that hash."""
    texts, any_unreadable = [], False
    for i in r.inputs:
        p = eng.resolve(i.path)
        if p is None or not p.is_file():
            any_unreadable = any_unreadable or p is None
            continue
        if eng.hash_of(i.path) != i.sha256:
            any_unreadable = True   # superseded in place, or edited: either way not what the seat saw
            continue
        text = eng.read_text(i.path)
        if text is not None:
            texts.append(text)
    return texts, any_unreadable


_ID_PARTS = re.compile(r"^([A-Z]{1,4})(-?)(\d+)([a-z]?)$")


def _text_has_id(text: str, item_id: str) -> bool:
    """`O2` is present as the token O2, or covered by a range like O1–O4 in the text."""
    if re.search(rf"(?<![\w\-]){re.escape(item_id)}(?![\w])", text):
        return True
    m = _ID_PARTS.match(item_id)
    if not m or m.group(4):
        return False
    prefix, sep, num = m.group(1), m.group(2), int(m.group(3))
    for r in re.finditer(rf"(?<![\w\-]){prefix}{sep}(\d+)\s*[–\-]\s*(?:{prefix}{sep})?(\d+)(?![\w])", text):
        if int(r.group(1)) <= num <= int(r.group(2)):
            return True
    return False


def _present(item: str, texts: list[str]) -> bool | None:
    """True if every id in the item (or its phrase) appears in some text; None if nothing to test."""
    ids = extract_ids(item)
    if ids:
        return all(any(_text_has_id(t, i) for t in texts) for i in ids)
    phrase = item.strip().strip('"“”').lower()
    if not phrase:
        return None
    return any(phrase in t.lower() for t in texts)


def _moves(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[5])
    superseded_passes: list[str] = []
    for r in eng.records:
        state = eng.moves_state(r)
        if state == "none-kind":
            continue
        if state == "superseded":
            superseded_passes.append(r.pass_id)
            continue
        out = eng.moves_artifact(r)
        rel = out.path if out else (r.artifact_outputs[0].path if r.artifact_outputs else "?")
        mv = eng.moves_for(r)
        if state == "missing" or mv is None:
            c.findings.append(f"{r.pass_id}: {rel} has no `## Moves` section on disk")
            continue
        for e in mv.errors:
            c.findings.append(f"{r.pass_id}: {rel} {e}")
        if mv.origin:
            continue
        upstream, any_unreadable = _upstream_texts(eng, r)
        own = eng.read_text(rel) or ""
        for m in mv.lines:
            c.n_total += 1
            if m.op == "added":
                c.n_ok += 1  # new by definition; the source is a claim rung 0 does not replay
                continue
            targets = m.items if m.op == "merged" else [m.item]
            verdicts = [_present(t, upstream) for t in targets]
            if all(v is True for v in verdicts):
                ok = True
                if m.op == "split":
                    for child in m.children:
                        if _present(child, upstream) is True:
                            c.findings.append(f"{r.pass_id}: split child {child} already exists upstream (line {m.lineno})")
                            ok = False
                        elif _present(child, [own]) is False:
                            c.findings.append(f"{r.pass_id}: split child {child} does not appear in {rel} (line {m.lineno})")
                            ok = False
                c.n_ok += 1 if ok else 0
            elif any_unreadable:
                c.n_unverifiable += 1   # the item may live only in a revision rung 0 cannot read
            else:
                missing = [t for t, v in zip(targets, verdicts) if v is not True]
                c.findings.append(
                    f"{r.pass_id}: {m.op} names {', '.join(missing)} but no readable upstream input contains it (line {m.lineno})"
                )
    if superseded_passes:
        c.notes.append(
            f"{len(superseded_passes)} pass(es) whose artifact was later overwritten in place, so their Moves are no "
            f"longer on disk: {', '.join(superseded_passes)}"
        )
    if c.n_unverifiable:
        c.notes.append(
            f"{c.n_unverifiable} move(s) unverifiable at rung 0: an upstream input is not readable at the hash the "
            f"seat saw (overwritten in place); a replay over the raw transcript is a later rung"
        )
    return c


# --------------------------------------------------------------------------- #
# 6 · meter
# --------------------------------------------------------------------------- #


def _meter(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[6], n_total=len(eng.records))
    totals_only: list[str] = []
    for r in eng.records:
        if r.meter_source not in METER_SOURCES:
            c.findings.append(f"{r.pass_id}: meter_source {r.meter_source!r} is not one of {' | '.join(METER_SOURCES)}")
            continue
        if r.meter_source == "UNMEASURED":
            c.n_ok += 1
            continue
        fields, bad = normalize_meter(r.meter)
        if bad:
            c.findings.append(
                f"{r.pass_id}: meter is {r.meter_source} but {', '.join(bad)} is not a whole token count"
            )
        elif "total" in fields or ("input" in fields and "output" in fields):
            c.n_ok += 1
            if "input" not in fields:
                totals_only.append(r.pass_id)
        else:
            c.findings.append(
                f"{r.pass_id}: meter is {r.meter_source} but carries neither `input` + `output` nor a `total` "
                f"(the one number the Agent tool and the Codex footer each report)"
            )
    unmeasured = [r.pass_id for r in eng.records if r.meter_source == "UNMEASURED"]
    if unmeasured:
        c.notes.append(f"{len(unmeasured)} UNMEASURED: {', '.join(unmeasured)}")
    if totals_only:
        c.notes.append(
            f"{len(totals_only)} meter(s) report a total only, as the runtime reported it, not split into "
            f"input and output: {', '.join(totals_only)}"
        )
    return c


# --------------------------------------------------------------------------- #
# 7 · stage structure
# --------------------------------------------------------------------------- #


def _stages(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[7])
    etype = str(eng.brief.get("type") or "").lower()
    if etype and etype not in ("full-train", "full train"):
        c.notes.append(f"engagement type is {etype}: not a full train, the stage structure is not asserted")
        return c
    if not etype:
        c.notes.append("brief.md names no type; asserting the full-train structure")
    stages = sorted({r.stage for r in eng.records if 1 <= r.stage <= 7})
    c.n_total = len(stages)
    for s in stages:
        ok = True
        rs = [r for r in eng.records if r.stage == s]
        drafts = [r for r in rs if r.kind == "draft"]
        if len(drafts) != 1:
            c.findings.append(f"stage {s} {_STAGE_NAMES[s]}: {len(drafts)} drafts, expected exactly one (repairs are `kind: repair`)")
            ok = False
        elif drafts[0].seat != STAGE_SEATS[s]:
            c.findings.append(f"stage {s}: draft by {drafts[0].seat}; the drafting seat is {STAGE_SEATS[s]}")
            ok = False
        audits = [r for r in rs if r.kind == "audit"]
        if not audits:
            c.findings.append(f"stage {s} {_STAGE_NAMES[s]}: no audit pass (the fixed auditor is {FIXED_AUDITORS[s]})")
            ok = False
        for a in audits:
            if a.seat != FIXED_AUDITORS[s]:
                c.findings.append(f"stage {s}: audit by {a.seat}; the fixed auditor is {FIXED_AUDITORS[s]}")
                ok = False
        if s in REQUIRED_COSIGNS:
            cosigns = [r for r in rs if r.kind == "co-sign"]
            if not cosigns:
                c.findings.append(f"stage {s}: no co-sign pass (required from {REQUIRED_COSIGNS[s]})")
                ok = False
            for cs in cosigns:
                if cs.seat != REQUIRED_COSIGNS[s]:
                    c.findings.append(f"stage {s}: co-sign by {cs.seat}; the co-signing seat is {REQUIRED_COSIGNS[s]}")
                    ok = False
        c.n_ok += 1 if ok else 0
    missing = [s for s in range(1, 8) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c


# --------------------------------------------------------------------------- #
# 8 · blind
# --------------------------------------------------------------------------- #


def row_block(html: str, pid: str) -> str | None:
    """The whole `<details id="pass-NN">…</details>`, counting nested disclosures.

    The row folds its record metadata into a `<details>` of its own, so a
    non-greedy match would stop at the first inner close and the blind check
    would read half a row.
    """
    m = re.search(rf'<details[^>]*\bid="{re.escape(pid)}"[^>]*>', html)
    if not m:
        return None
    depth = 1
    for tag in re.finditer(r"<details\b|</details\s*>", html[m.end():]):
        depth += 1 if tag.group(0).startswith("<details") else -1
        if depth == 0:
            return html[m.start(): m.end() + tag.end()]
    return html[m.start():]


_row_block = row_block


def _blind(eng: Engagement) -> Check:
    c = Check(CHECK_NAMES[8])
    html_path = eng.trace_dir / "eval.html"
    html = html_path.read_text(encoding="utf-8", errors="replace") if html_path.is_file() else None
    by = eng.by_id
    for r in eng.records:
        if r.kind != "trial" and not r.shadow_of:
            continue
        c.n_total += 1
        ok = True
        base = by.get(r.shadow_of or "")
        if base is None:
            c.findings.append(f"{r.pass_id}: shadow_of names {r.shadow_of}, which has no record")
            continue
        if sorted((i.path, i.sha256) for i in r.inputs) != sorted((i.path, i.sha256) for i in base.inputs):
            c.findings.append(f"{r.pass_id}: a trial fires on identical inputs, but its inputs differ from {base.pass_id}'s")
            ok = False
        labeled = all(eng.labels.get(p) is not None and eng.labels[p].verdict for p in (r.pass_id, base.pass_id))
        if not labeled and html is not None:
            # gates may share a runtime with the trial, so the test is scoped to the pair's own rows
            for rec in (r, base):
                block = _row_block(html, rec.pass_id)
                if block is None:
                    c.notes.append(f"{rec.pass_id}: eval.html has no row for it, so the blind cannot be verified from the render")
                    continue
                for secret in (rec.runtime, rec.launch, rec.raw_log):
                    if secret and secret not in ("—", "-") and secret in block:
                        c.findings.append(
                            f"{rec.pass_id}: eval.html shows its runtime, launch form or log path while the blind pair "
                            f"({r.pass_id} / {base.pass_id}) is not fully labeled"
                        )
                        ok = False
                        break
        c.n_ok += 1 if ok else 0
        if not labeled:
            c.notes.append(f"{r.pass_id} / {base.pass_id}: blind pair, runtime stays hidden until both carry a verdict")
    return c
