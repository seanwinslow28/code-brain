#!/usr/bin/env python3
"""Frame stage for the Content Oracle -- four tool-denied lenses on a stripped week.

Ruled on #227 (rulings 18 and 19), built on #238. The internal sweep can only
propose subjects the author already worked on; a quiet week gives a boring deck.
This stage hands four fresh, isolated generators a *stripped* summary of the week
plus the news gists, each wearing one lens, and gets back experiment angles the
sweep cannot reach. No critic call: the in-session scoring pass is the one judge.

    python3 frame_stage.py --summary <path> [--gists <path>] [--dry-run] [--out <ignored path>]

Mechanism: headless `claude --print --tools ""` subprocesses, one per lens --
the pattern validated in creative-partner/references/divergence-stage.md. Fresh
context and full tool denial are enforced by the runtime, not by a prompt.

Payload law (the Oracle's privacy rule, one stage earlier): the generators see
only the stripped summary, the gists' two lines each, and their own lens card.
`inspect_payload` refuses to dispatch a summary that carries paths, identifiers,
or a line lifted verbatim from a private file. `--dry-run` prints exactly what
would be sent, and nothing is sent.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NATIVE_DECK = HERE / "references" / "frames.md"
FOREIGN_DECK = REPO / ".claude" / "skills" / "creative-partner" / "references" / "frame-deck.md"

# Home domains whose frames may NOT fill the foreign slot: story lenses turn a
# week of commits into narratives again (ruling 19).
STORY_DOMAINS = ("story / writing",)

SUMMARY_MAX_CHARS = 8000
GIST_MAX_ITEMS = 12
GIST_FIELD_MAX = 400
VERBATIM_MIN_CHARS = 40
CALL_TIMEOUT_S = 300

# Anything matching one of these is an identifier or a path, and has no business
# in a generator payload. Names are for the error message.
FORBIDDEN = [
    ("absolute path", re.compile(r"/Users/|/home/|C:\\\\")),
    ("home-relative path", re.compile(r"(^|\s)~/")),
    ("private vault path", re.compile(r"vault/daily|vault/10_timeline|vault/05_atlas")),
    ("sidecar path", re.compile(r"\.creative-harness|partner-sessions")),
    ("private-brain path", re.compile(r"content-machine/(corpus|transcripts|ledger|cheese-bank)")),
    ("email address", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("credential-shaped token", re.compile(r"\b(sk-ant-|sk-[A-Za-z0-9]{8}|ghp_|xox[abp]-)")),
    ("commit sha", re.compile(r"\b(?=[0-9a-f]*\d)[0-9a-f]{9,40}\b")),
]


@dataclass
class Frame:
    id: str
    domain: str
    persona: str
    forcing: str
    banned: str = ""
    wild: bool = False

    def card(self) -> str:
        lines = [f"LENS: {self.id}", f"Persona: {self.persona}", f"Forcing move: {self.forcing}"]
        if self.banned:
            lines.append(f"Banned: {self.banned}")
        return "\n".join(lines)


@dataclass
class Gist:
    happened: str
    can_now: str
    source: str = ""


@dataclass
class Selection:
    natives: list[Frame]
    foreign: Frame
    wild: Frame

    @property
    def frames(self) -> list[Frame]:
        return [*self.natives, self.foreign, self.wild]

    @property
    def ids(self) -> list[str]:
        return [f.id for f in self.frames]


@dataclass
class GeneratorResult:
    frame: Frame
    ok: bool
    text: str = ""
    error: str = ""
    cost_usd: float = 0.0
    angles: int = 0


# ── decks ────────────────────────────────────────────────────────────────────

def parse_deck(text: str) -> dict[str, Frame]:
    """Read frames from a deck file: `## domain` headings, `### id` cards, bullet fields.

    One parser reads both the Oracle's natives and the creative-partner deck,
    which is the point of keeping the card shape identical.
    """
    frames: dict[str, Frame] = {}
    domain = ""
    current: dict | None = None

    def flush() -> None:
        if current and current.get("persona") and current.get("forcing"):
            frames[current["id"]] = Frame(
                id=current["id"],
                domain=current["domain"],
                persona=current["persona"],
                forcing=current["forcing"],
                banned=current.get("banned", ""),
                wild=current["domain"] == "wildcards" or "*(wild)*" in current.get("persona", ""),
            )

    field_re = re.compile(r"^- \*\*(Persona|Forcing move|Banned|Provenance):\*\*\s*(.*)$")
    last_field: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            flush()
            current = None
            domain = line[3:].strip().lower()
            last_field = None
            continue
        if line.startswith("### "):
            flush()
            current = {"id": line[4:].strip(), "domain": domain}
            last_field = None
            continue
        if current is None:
            continue
        m = field_re.match(line)
        if m:
            key = {"Persona": "persona", "Forcing move": "forcing", "Banned": "banned",
                   "Provenance": "provenance"}[m.group(1)]
            current[key] = m.group(2).strip()
            last_field = key
            continue
        if last_field and line.startswith("  ") and line.strip():
            current[last_field] = (current[last_field] + " " + line.strip()).strip()
        elif not line.strip():
            last_field = None
    flush()
    for f in frames.values():
        f.persona = f.persona.replace("*(wild)*", "").strip()
    return frames


def load_decks(native_path: Path = NATIVE_DECK, foreign_path: Path = FOREIGN_DECK):
    natives = parse_deck(native_path.read_text(encoding="utf-8"))
    deck = parse_deck(foreign_path.read_text(encoding="utf-8"))
    return natives, deck


def select_frames(
    natives: dict[str, Frame],
    deck: dict[str, Frame],
    run_date: date,
    native_ids: list[str] | None = None,
    foreign_id: str | None = None,
    wild_id: str | None = None,
) -> Selection:
    """Two natives, one foreign, one wild. Rotates by ISO week unless overridden."""
    week = run_date.isocalendar()[1] + run_date.year * 53

    native_order = sorted(natives)
    if native_ids:
        if len(native_ids) != 2:
            raise ValueError("exactly two native frames per run")
        for nid in native_ids:
            if nid not in natives:
                raise ValueError(f"unknown native frame {nid!r}; natives are {native_order}")
        chosen = [natives[n] for n in native_ids]
    else:
        pairs = [(a, b) for i, a in enumerate(native_order) for b in native_order[i + 1:]]
        if not pairs:
            raise ValueError("the native deck needs at least two frames")
        a, b = pairs[week % len(pairs)]
        chosen = [natives[a], natives[b]]

    foreign_pool = sorted(f.id for f in deck.values() if not f.wild and f.domain not in STORY_DOMAINS)
    wild_pool = sorted(f.id for f in deck.values() if f.wild)
    if not foreign_pool or not wild_pool:
        raise ValueError("the creative-partner deck must hold at least one foreign and one wild frame")

    if foreign_id:
        if foreign_id not in foreign_pool:
            raise ValueError(f"{foreign_id!r} is not an eligible foreign frame; pool is {foreign_pool}")
        foreign = deck[foreign_id]
    else:
        foreign = deck[foreign_pool[week % len(foreign_pool)]]

    if wild_id:
        if wild_id not in wild_pool:
            raise ValueError(f"{wild_id!r} is not a wild frame; pool is {wild_pool}")
        wild = deck[wild_id]
    else:
        wild = deck[wild_pool[week % len(wild_pool)]]

    return Selection(natives=chosen, foreign=foreign, wild=wild)


# ── inputs ───────────────────────────────────────────────────────────────────

def load_gists(path: Path) -> list[Gist]:
    """Gists are a JSON list of {happened, can_now, source}. The news lane (#239) writes it."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("gists file must be a JSON list")
    gists = []
    for i, row in enumerate(data):
        if not isinstance(row, dict) or not row.get("happened") or not row.get("can_now"):
            raise ValueError(f"gist {i} needs 'happened' and 'can_now'")
        gists.append(Gist(
            happened=str(row["happened"]).strip(),
            can_now=str(row["can_now"]).strip(),
            source=str(row.get("source", "")).strip(),
        ))
    return gists


def _norm(line: str) -> str:
    """Whitespace-collapsed, lower-cased, leading list markers dropped, so a bulleted
    summary line still matches the same sentence written as prose in a daily."""
    line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", line)
    return re.sub(r"\s+", " ", line).strip().lower()


def private_files(days: int, repo: Path = REPO, sidecars: Path | None = None) -> list[Path]:
    """The private material the summary must not quote: dailies in window, sidecars, corpus, transcripts."""
    if sidecars is None:
        sidecars = Path.home() / ".creative-harness" / "partner-sessions"
    cutoff = date.today() - timedelta(days=days + 1)
    files: list[Path] = []
    daily = repo / "vault" / "daily"
    if daily.is_dir():
        for p in daily.glob("20*.md"):
            try:
                if datetime.strptime(p.stem, "%Y-%m-%d").date() >= cutoff:
                    files.append(p)
            except ValueError:
                continue
    if sidecars.is_dir():
        files += sorted(sidecars.glob("*.md"))
    brain = repo / "creative-studio" / "content-machine"
    for sub in ("corpus", "transcripts"):
        d = brain / sub
        if d.is_dir():
            files += sorted(d.rglob("*.md"))
    return files


def inspect_payload(summary: str, gists: list[Gist], private: list[Path]) -> list[str]:
    """Return every reason this payload may not be dispatched. Empty means clean."""
    problems: list[str] = []
    if len(summary) > SUMMARY_MAX_CHARS:
        problems.append(f"summary is {len(summary)} chars; cap is {SUMMARY_MAX_CHARS} -- it is not stripped")
    if not summary.strip():
        problems.append("summary is empty")
    texts = [("summary", summary)] + [
        (f"gist {i}", g.happened + "\n" + g.can_now) for i, g in enumerate(gists)
    ]
    for label, text in texts:
        for name, pattern in FORBIDDEN:
            hit = pattern.search(text)
            if hit:
                problems.append(f"{label}: {name} ({hit.group(0)[:24]!r})")
    if len(gists) > GIST_MAX_ITEMS:
        problems.append(f"{len(gists)} gists; cap is {GIST_MAX_ITEMS}")
    for i, g in enumerate(gists):
        for fname, val in (("happened", g.happened), ("can_now", g.can_now)):
            if len(val) > GIST_FIELD_MAX:
                problems.append(f"gist {i}.{fname} is {len(val)} chars; cap is {GIST_FIELD_MAX}")

    # Verbatim lift: any summary line long enough to be a sentence that appears
    # in a private file is a quote, whatever the author of the summary intended.
    candidates = [_norm(l) for l in summary.splitlines() if len(_norm(l)) >= VERBATIM_MIN_CHARS]
    if candidates:
        for path in private:
            try:
                body = _norm(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
            for line in candidates:
                if line in body:
                    problems.append(f"summary quotes a private file verbatim ({path.name}): {line[:50]!r}...")
    return sorted(set(problems))


# ── prompts ──────────────────────────────────────────────────────────────────

GENERATOR_RULES = """\
You are one of four isolated generators in a content Oracle's frame stage. You wear
exactly one lens (below). You see a stripped summary of what an author worked on this
week and a short list of AI news gists. You have no tools and no other context.

Your job: propose 3 to 5 EXPERIMENT ANGLES the author could go run and later be
interviewed about. Not stories. Not takes. Not claims about what he did.

Hard rules:
- An angle names an experiment: "do this, expect that." It never asserts the author
  did or found anything. Everything on it is a hypothesis until the experiment runs.
- Never phrase a search. No "best X", "X vs Y", "latest on X", no buyer's questions.
- No one-shot prompting ("ask model X to do Y and see"). No announcements ("X just
  dropped"). Off-label use, a falsifiable prediction, or a made thing -- those are
  angles. A demo whose outcome is already known is not.
- Ban the first three obvious ideas; assume an unimaginative competitor already
  proposed them.
- Each angle must name its PROVOCATION: which week item or which news gist prompted it,
  by its short name from the payload. An angle with no provocation is an invention.
- Generate only. Do not rank, score, evaluate, or recommend.
- Apply your lens's forcing move to every angle and respect its ban.

Output format, exactly, one block per angle, nothing before or after the blocks:

ANGLE <n> [{lens_id}]
Experiment: <do this, expect that -- one or two sentences>
Provocation: <week item or news gist, by short name>
Prediction: <what you expect, and what result would prove it wrong>
Output: <the artifact the experiment leaves behind, or "a result" if none>
Not the obvious idea because: <one line>
"""


def build_prompts(frame: Frame, summary: str, gists: list[Gist]) -> tuple[str, str]:
    """(system prompt, user payload). Sources are stripped from gists on purpose."""
    system = GENERATOR_RULES.format(lens_id=frame.id) + "\n" + frame.card() + "\n"
    parts = ["THE WEEK, STRIPPED (what the author worked on; no quotes, no identifiers):", "",
             summary.strip(), ""]
    if gists:
        parts += ["AI NEWS THIS WEEK (gist per item: what happened; what it can now do):", ""]
        for i, g in enumerate(gists, 1):
            parts.append(f"{i}. {g.happened}")
            parts.append(f"   Can now: {g.can_now}")
        parts.append("")
    else:
        parts += ["AI NEWS THIS WEEK: none supplied for this run.", ""]
    parts.append(f"Produce 3 to 5 angles through the {frame.id} lens.")
    return system, "\n".join(parts)


# ── dispatch ─────────────────────────────────────────────────────────────────

def _child_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    # A stray key must never turn a subscription call into a metered one.
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    return env


def run_generator(frame: Frame, system: str, user: str, model: str, cwd: Path) -> GeneratorResult:
    cmd = [
        "claude", "--print",
        "--model", model,
        "--output-format", "json",
        "--exclude-dynamic-system-prompt-sections",
        "--system-prompt", system,
        "--tools", "",                       # tool denial enforced by the runtime
        "--permission-mode", "bypassPermissions",
        user,
    ]
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=_child_env(), capture_output=True,
                              text=True, timeout=CALL_TIMEOUT_S)
    except (OSError, subprocess.SubprocessError) as exc:
        return GeneratorResult(frame, False, error=f"call failed: {exc}")
    if proc.returncode != 0:
        return GeneratorResult(frame, False, error=f"exit {proc.returncode}: {proc.stderr[-300:]!r}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return GeneratorResult(frame, False, error=f"non-JSON reply: {proc.stdout[:200]!r}")
    if data.get("is_error"):
        return GeneratorResult(frame, False, error=str(data.get("result", ""))[:300])
    text = str(data.get("result", "")).strip()
    cost = float(data.get("total_cost_usd") or 0.0)
    angles = count_angles(text, frame.id)
    if angles == 0:
        return GeneratorResult(frame, False, text=text, error="no ANGLE blocks stamped with the lens id",
                               cost_usd=cost)
    return GeneratorResult(frame, True, text=text, cost_usd=cost, angles=angles)


ANGLE_RE = re.compile(r"^ANGLE\s+\d+\s+\[([^\]]+)\]", re.M)


def count_angles(text: str, lens_id: str) -> int:
    """Blocks stamped with this lens. A block stamped with another lens does not count."""
    return sum(1 for m in ANGLE_RE.finditer(text) if m.group(1).strip() == lens_id)


def dispatch(selection: Selection, summary: str, gists: list[Gist], model: str) -> list[GeneratorResult]:
    """Four fresh calls in parallel. A failed slot stays a failed slot -- never replaced."""
    with tempfile.TemporaryDirectory(prefix="oracle-frames-") as neutral:
        cwd = Path(neutral)   # no project settings, hooks or MCP fire from here
        jobs = []
        with ThreadPoolExecutor(max_workers=4) as pool:
            for frame in selection.frames:
                system, user = build_prompts(frame, summary, gists)
                jobs.append(pool.submit(run_generator, frame, system, user, model, cwd))
            return [j.result() for j in jobs]


# ── rendering ────────────────────────────────────────────────────────────────

def render(selection: Selection, results: list[GeneratorResult], run_date: date,
           gists: list[Gist], model: str) -> str:
    cost = sum(r.cost_usd for r in results)
    ok = sum(1 for r in results if r.ok)
    lines = [
        f"# Oracle frame stage — {run_date.isoformat()}",
        "",
        f"frames: [{', '.join(selection.ids)}] · calls: {len(results)} attempted, {ok} returned · "
        f"model: {model} · cost: ${cost:.2f}",
        f"natives: {', '.join(f.id for f in selection.natives)} · foreign: {selection.foreign.id} · "
        f"wild: {selection.wild.id}",
        f"gists supplied: {len(gists)}",
        "",
        "Angles, unscored. Each enters the same pile as sweep items and news items and",
        "faces the same Spine veto in the one scoring pass. A picked angle becomes a card",
        "with `Source: frame:<id>`, `Evidence: <provocation>` and `Status: unrun`.",
        "",
    ]
    for r in results:
        lines.append(f"## {r.frame.id} — {'ok' if r.ok else 'FAILED'}")
        lines.append("")
        if r.ok:
            lines += [r.text, ""]
        else:
            lines += [f"FAILED SLOT: {r.error}", ""]
            if r.text:
                lines += ["Returned text, unstamped:", "", r.text, ""]
    if gists:
        lines += ["## Provocation sources (for the cards' Evidence field; generators never saw these)", ""]
        for i, g in enumerate(gists, 1):
            lines.append(f"{i}. {g.happened} — {g.source or '(no source recorded)'}")
        lines.append("")
    lines += [
        "## Bank record stub",
        "",
        f"Frames dispatched: {', '.join(selection.ids)}. Record beside the query shapes which",
        "of these produced a picked card; a run where none did is a finding about the deck.",
        "",
    ]
    return "\n".join(lines)


def render_dry_run(selection: Selection, summary: str, gists: list[Gist]) -> str:
    system, user = build_prompts(selection.frames[0], summary, gists)
    lines = [
        "DRY RUN — nothing dispatched.",
        f"frames: [{', '.join(selection.ids)}]",
        "",
        "=== SYSTEM PROMPT (first frame; the other three differ only in the lens card) ===",
        system,
        "=== USER PAYLOAD (identical for all four) ===",
        user,
        "=== END ===",
    ]
    return "\n".join(lines)


def is_ignored(path: Path, repo: Path = REPO) -> bool:
    try:
        done = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=repo,
                              capture_output=True, timeout=10)
        return done.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--summary", type=Path, required=True,
                    help="stripped week summary written by the session (nouns, no quotes, no paths)")
    ap.add_argument("--gists", type=Path, help="news gists JSON from the news lane (#239)")
    ap.add_argument("--date", type=date.fromisoformat, default=date.today(), help="run date (selection rotates by ISO week)")
    ap.add_argument("--days", type=int, default=7, help="window for the verbatim check against dailies")
    ap.add_argument("--native", help="two native frame ids, comma-separated")
    ap.add_argument("--foreign", help="foreign frame id from the creative-partner deck")
    ap.add_argument("--wild", help="wild frame id from the creative-partner deck")
    ap.add_argument("--model", default="sonnet", help="model alias for the generators (default sonnet)")
    ap.add_argument("--dry-run", action="store_true", help="print the exact payload; dispatch nothing")
    ap.add_argument("--out", type=Path, help="write the result here (must be git-ignored)")
    args = ap.parse_args(argv)

    summary = args.summary.read_text(encoding="utf-8")
    gists = load_gists(args.gists) if args.gists else []
    natives, deck = load_decks()
    try:
        selection = select_frames(
            natives, deck, args.date,
            native_ids=args.native.split(",") if args.native else None,
            foreign_id=args.foreign, wild_id=args.wild,
        )
    except ValueError as exc:
        print(f"frame selection: {exc}", file=sys.stderr)
        return 2

    problems = inspect_payload(summary, gists, private_files(args.days))
    if problems:
        print("refusing to dispatch: the payload is not clean.", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 2

    if args.out and not is_ignored(args.out):
        print(f"refusing to write {args.out}: git does not ignore it, and the angles name his week.",
              file=sys.stderr)
        return 2

    if args.dry_run:
        text = render_dry_run(selection, summary, gists)
    else:
        print(f"dispatching 4 generators: {', '.join(selection.ids)} (model {args.model})", file=sys.stderr)
        results = dispatch(selection, summary, gists, args.model)
        text = render(selection, results, args.date, gists, args.model)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"→ {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(text + ("\n" if not text.endswith("\n") else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
