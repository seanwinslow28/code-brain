#!/usr/bin/env python3
"""Mock Interview Loop — record -> transcribe -> grade pipeline (Task 19 / A6).

Watches the macOS Voice Memos folder for new .m4a files (or accepts an explicit
--audio path), transcribes locally with faster-whisper ($0/run, audio never leaves
the machine — symmetric with the Kokoro-82M TTS pipeline), grades the transcript
against the 8-dimension interview rubric via the existing LLM Council
(`interview_grader` profile), and writes a transcript + grade card +
aggregated-score summary to:

    vault/20_projects/prj-job-hunt-2026/interview-prep/mock-log/

Design note (deviation from the 2026-05-20 prep-doc skeleton, documented in
INTERVIEW_GRADER.md): the Council *chairman* emits prose, not JSON, so the
canonical NUMERIC grade is computed by aggregating the four PANELIST JSON
scorecards (median per dimension, robust to a single outlier). The chairman's
prose synthesis is preserved as the qualitative read. This is more faithful to
"a 4-model calibrated panel" than trusting the chairman to re-emit JSON.

Usage:
  # One-shot — grade a specific recording against a question:
  python3 mock_interview_loop.py --audio "/path/Recording.m4a" \\
      --question "Tell me about yourself" --label tmay-attempt-1

  # Watch mode — wait for new Voice Memos, prompt for the question on each:
  python3 mock_interview_loop.py --watch

  # Grade an already-transcribed answer (skip audio + Whisper entirely):
  python3 mock_interview_loop.py --transcript-text "..." \\
      --question "Walk me through what happened with The Block" --label block-q
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import time
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
# This file lives at code-brain/agents-sdk/scripts/mock_interview_loop.py
ROOT = Path(__file__).resolve().parents[2]  # -> code-brain/
VAULT_LOG = ROOT / "vault" / "20_projects" / "prj-job-hunt-2026" / "interview-prep" / "mock-log"
RUBRIC_TEMPLATE = ROOT / "tools" / "llm-council" / "profiles" / "interview-grader-template.md"
COUNCIL_ROOT = ROOT / "tools" / "llm-council"
COUNCIL_PY = COUNCIL_ROOT / ".venv" / "bin" / "python3"
# Modern macOS Voice Memos store .m4a here (NOT ~/Voice Memos). Confirm on first run.
VOICE_MEMOS_DIR = Path.home() / "Library" / "Application Support" / "com.apple.voicememos" / "Recordings"

DIMENSIONS = (
    "timing",
    "structure",
    "impact_specificity",
    "confidence_signals",
    "filler_words",
    "weakness_flipping",
    "information_control",
    "memorability",
)


# ── Transcription ────────────────────────────────────────────────────────────
def transcribe_local_whisper(audio_path: Path) -> str:
    """Transcribe with faster-whisper. ~1-3 min for a 5-min recording on M-series.

    Install (one-time): agents-sdk/.venv/bin/pip install faster-whisper
    base.en is ~74MB and runs ~5x realtime; medium.en is cleaner but slower.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise SystemExit(
            "faster-whisper not installed. Run:\n"
            "  agents-sdk/.venv/bin/pip install faster-whisper\n"
            "(Or pass --transcript-text to skip transcription and grade text directly.)"
        ) from e

    model = WhisperModel("base.en", device="auto", compute_type="auto")
    segments, _ = model.transcribe(str(audio_path), beam_size=5)
    return " ".join(s.text.strip() for s in segments).strip()


# ── Prompt assembly ──────────────────────────────────────────────────────────
def build_grading_prompt(transcript: str, question: str) -> str:
    """Template the 8-dimension rubric with the question + transcript."""
    template = RUBRIC_TEMPLATE.read_text()
    # Only the two named tokens are replaced; the JSON example's literal braces are left intact.
    return template.replace("{question}", question.strip()).replace("{transcript}", transcript.strip())


# ── Council invocation ───────────────────────────────────────────────────────
def run_council(prompt_text: str, out_stem: Path, label: str, force: bool = False) -> Path:
    """Invoke the existing council CLI as a subprocess; return the grade-markdown path.

    Subprocess (not import) keeps the boundary clean and lets the council's own
    budget gates fire. Raises RuntimeError on non-zero exit.
    """
    prompt_file = out_stem.with_suffix(".grading-prompt.tmp.md")
    grade_md = out_stem.with_suffix(".grade.md")
    prompt_file.write_text(prompt_text)
    cmd = [
        str(COUNCIL_PY),
        "-m", "council",
        "--profile", "interview_grader",
        "--prompt-file", str(prompt_file),
        "--output", str(grade_md),
        "--tag", f"interview-grader-{label}",
    ]
    if force:
        cmd.append("--force")
    try:
        result = subprocess.run(
            cmd, cwd=str(COUNCIL_ROOT), capture_output=True, text=True, timeout=180
        )
    finally:
        prompt_file.unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(f"Council run failed (exit {result.returncode}):\n{result.stderr}")
    return grade_md


# ── Parsing + aggregation (pure, unit-tested offline) ────────────────────────
def extract_json_objects(text: str) -> list[dict]:
    """Return every top-level balanced {...} block in `text` that parses as JSON.

    Tolerant of ```json fences and prose preamble/trailing. Scans for balanced
    braces (ignoring braces inside strings) so a scorecard wrapped in commentary
    still extracts.
    """
    objs: list[dict] = []
    depth = 0
    start = -1
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    chunk = text[start : i + 1]
                    try:
                        objs.append(json.loads(chunk))
                    except json.JSONDecodeError:
                        pass
                    start = -1
    return objs


def _section(markdown: str, header: str, next_headers: tuple[str, ...]) -> str:
    """Return the body between `header` and the next of `next_headers` (or EOF)."""
    idx = markdown.find(header)
    if idx == -1:
        return ""
    body_start = idx + len(header)
    ends = [markdown.find(h, body_start) for h in next_headers]
    ends = [e for e in ends if e != -1]
    body_end = min(ends) if ends else len(markdown)
    return markdown[body_start:body_end]


def parse_panelist_scorecards(council_markdown: str) -> list[dict]:
    """Extract each panelist's JSON scorecard from the '## Council responses' block.

    A valid scorecard is a JSON object that contains a 'scores' key. The chairman
    block is deliberately excluded — it's prose.
    """
    responses = _section(
        council_markdown, "## Council responses", ("## Cross-rankings", "## Chairman synthesis")
    )
    cards = [o for o in extract_json_objects(responses) if isinstance(o.get("scores"), dict)]
    return cards


def extract_chairman_synthesis(council_markdown: str) -> str:
    body = _section(council_markdown, "## Chairman synthesis", ())
    return body.strip()


def aggregate_scorecards(scorecards: list[dict]) -> dict:
    """Aggregate N panelist scorecards into one canonical grade.

    Per dimension: median of the available panelist scores (robust to one outlier).
    Overall: mean of the 8 dimension medians, rounded to 1 decimal.
    Revisions: merged across panelists, de-duplicated, capped at 5.
    """
    if not scorecards:
        return {
            "_error": "no parseable panelist scorecards found",
            "panelists": 0,
            "overall_score": None,
            "dimensions": {},
            "merged_revisions": [],
            "passes_gate_c": False,
        }

    per_dim: dict[str, dict] = {}
    for dim in DIMENSIONS:
        vals = []
        for card in scorecards:
            entry = card.get("scores", {}).get(dim)
            if isinstance(entry, dict) and isinstance(entry.get("score"), (int, float)):
                vals.append(float(entry["score"]))
            elif isinstance(entry, (int, float)):
                vals.append(float(entry))
        if vals:
            per_dim[dim] = {
                "median": round(statistics.median(vals), 1),
                "scores": vals,
                "spread": round(max(vals) - min(vals), 1),
            }

    medians = [d["median"] for d in per_dim.values()]
    overall = round(statistics.mean(medians), 1) if medians else None

    revisions: list[str] = []
    for card in scorecards:
        for rev in card.get("three_specific_revisions", []) or []:
            r = str(rev).strip()
            if r and r not in revisions:
                revisions.append(r)

    return {
        "panelists": len(scorecards),
        "overall_score": overall,
        "dimensions": per_dim,
        "merged_revisions": revisions[:5],
        "passes_gate_c": overall is not None and overall >= 8.0,  # operating-model Gate C bar
    }


# ── Persistence + reporting ──────────────────────────────────────────────────
def write_summary(out_stem: Path, question: str, agg: dict, chairman: str) -> Path:
    summary_md = out_stem.with_suffix(".summary.md")
    lines = [f"# Mock grade — {out_stem.name}\n", f"**Question:** {question}\n"]
    if agg.get("overall_score") is not None:
        gate = "✅ PASS (≥8.0)" if agg["passes_gate_c"] else "below the 8.0 Gate-C bar"
        lines.append(f"**Overall (median-aggregated across {agg['panelists']} panelists):** "
                     f"{agg['overall_score']}/10 — {gate}\n")
        lines.append("| Dimension | Median | Panelist scores | Spread |")
        lines.append("|---|---|---|---|")
        for dim, d in agg["dimensions"].items():
            scores = ", ".join(str(s) for s in d["scores"])
            flag = " ⚠️" if d["spread"] >= 3 else ""
            lines.append(f"| {dim.replace('_', ' ')} | **{d['median']}** | {scores} | {d['spread']}{flag} |")
        lines.append("")
        if agg["merged_revisions"]:
            lines.append("## Top revisions (merged across panel)\n")
            for r in agg["merged_revisions"]:
                lines.append(f"- {r}")
            lines.append("")
    else:
        lines.append(f"⚠️ Could not aggregate a numeric grade: {agg.get('_error', 'unknown')}. "
                     f"See the full council markdown (`.grade.md`).\n")
    if chairman:
        lines.append("## Chairman synthesis (qualitative)\n")
        lines.append(chairman)
        lines.append("")
    summary_md.write_text("\n".join(lines))
    return summary_md


def print_report(agg: dict, summary_path: Path) -> None:
    if agg.get("overall_score") is not None:
        gate = "PASS ✅" if agg["passes_gate_c"] else "below 8.0"
        print(f"\n  Overall: {agg['overall_score']}/10  ({gate}, {agg['panelists']} panelists)")
        for dim, d in agg["dimensions"].items():
            warn = "  <-- panel disagrees" if d["spread"] >= 3 else ""
            print(f"    - {dim:20s} {d['median']:>4}{warn}")
        if agg["merged_revisions"]:
            print("  Revisions:")
            for r in agg["merged_revisions"]:
                print(f"    • {r}")
    else:
        print(f"\n  [warn] {agg.get('_error', 'no numeric grade')} — see {summary_path.with_suffix('.grade.md')}")
    print(f"\n  Wrote: {summary_path}")


# ── End-to-end ───────────────────────────────────────────────────────────────
def grade(transcript: str, question: str, label: str, audio_name: str | None, force: bool = False) -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    VAULT_LOG.mkdir(parents=True, exist_ok=True)
    out_stem = VAULT_LOG / f"{timestamp}-{label}"

    transcript_md = out_stem.with_suffix(".transcript.md")
    transcript_md.write_text(
        f"# Transcript — {timestamp}\n\n"
        f"**Question:** {question}\n\n"
        f"**Recording:** `{audio_name or '(direct text)'}`\n\n---\n\n{transcript}\n"
    )
    print(f"  → transcript: {transcript_md.name}")

    print("  → grading via Council (interview_grader, 4 panelists)…")
    grade_md = run_council(build_grading_prompt(transcript, question), out_stem, label, force=force)
    council_markdown = grade_md.read_text()

    cards = parse_panelist_scorecards(council_markdown)
    agg = aggregate_scorecards(cards)
    chairman = extract_chairman_synthesis(council_markdown)
    summary = write_summary(out_stem, question, agg, chairman)
    print_report(agg, summary)
    return agg


def grade_audio(audio_path: Path, question: str, label: str, force: bool = False) -> dict:
    print(f"  → transcribing {audio_path.name} (faster-whisper)…")
    transcript = transcribe_local_whisper(audio_path)
    return grade(transcript, question, label, audio_path.name, force=force)


def watch_loop(force: bool = False) -> None:
    if not VOICE_MEMOS_DIR.exists():
        raise SystemExit(f"Voice Memos dir not found: {VOICE_MEMOS_DIR}\n"
                         f"Confirm the path on this macOS version, or use --audio one-shot mode.")
    print(f"Watching {VOICE_MEMOS_DIR} for new .m4a. Ctrl-C to stop.")
    seen = set(VOICE_MEMOS_DIR.glob("*.m4a"))
    while True:
        time.sleep(3)
        for audio in sorted(set(VOICE_MEMOS_DIR.glob("*.m4a")) - seen):
            print(f"\n[new] {audio.name}")
            question = input("  Question this answers: ").strip()
            label = input("  Short label (e.g. tmay-attempt-1): ").strip() or "adhoc"
            try:
                grade_audio(audio, question, label, force=force)
            except Exception as e:  # keep the watcher alive
                print(f"  [error] {e}")
        seen = set(VOICE_MEMOS_DIR.glob("*.m4a"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", type=Path, help="Path to a .m4a recording (one-shot mode)")
    ap.add_argument("--transcript-text", type=str, help="Grade this text directly (skip audio + Whisper)")
    ap.add_argument("--question", type=str, help="The interview question being answered")
    ap.add_argument("--label", type=str, default="adhoc", help="Short label for the filename")
    ap.add_argument("--watch", action="store_true", help="Watch the Voice Memos folder for new recordings")
    ap.add_argument("--force", action="store_true", help="Bypass the council per-query cap (daily/monthly still enforced)")
    args = ap.parse_args()

    if args.watch:
        watch_loop(force=args.force)
    elif args.transcript_text:
        if not args.question:
            ap.error("--question is required with --transcript-text")
        grade(args.transcript_text, args.question, args.label, audio_name=None, force=args.force)
    elif args.audio:
        if not args.question:
            ap.error("--question is required in one-shot --audio mode")
        grade_audio(args.audio, args.question, args.label, force=args.force)
    else:
        ap.error("Provide --audio + --question, --transcript-text + --question, or --watch")


if __name__ == "__main__":
    main()
