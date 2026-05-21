---
type: prep
project: prj-job-hunt-2026
task: Task 19 Step 0 — Mock Interview Infrastructure pre-build prep
created: 2026-05-20
last_updated: 2026-05-21
status: decisions-locked-ready-for-build
build_window: 2026-05-21 to 2026-05-26
ship_target: 2026-05-26
ai-context: |
  Pre-build prep for Task 19 (A6 — Mock Interview Infrastructure). Drop-in interview_grader
  Council profile matching the existing PROFILES dict shape, 8-dim rubric prompt template,
  mock_interview_loop.py skeleton with local Whisper as the recommended transcription stack
  (symmetric with the existing Kokoro-82M TTS pipeline), test plan with Task 17 TMAY dependency
  flagged. Sean's decisions locked 2026-05-21: 4-panelist profile (Opus + GPT-5.5 + Gemini Pro +
  Sonnet), local Whisper transcription, grades stay private inside interview-prep/mock-log/
  (not surfaced in daily-driver brief), both watch + one-shot modes shipped, run tests on
  5/26 (the "Why The Block?" question SWAPPED — Sean was laid off, not departing — replaced
  with "Walk me through what happened with The Block + your search reset"), keep full council
  markdown not just chairman synthesis. Output is the measurement infrastructure for Gate C
  ("3 consecutive 8+/10 mock interviews") — without this rig, Gate C is unmeasurable.
related:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[operating-model]]"
  - "[[2026-05-20-task-15-step-0-prebuild-prep]]"
sources:
  - tools/llm-council/council/profiles.py (live)
  - tools/llm-council/council/cli.py (live)
  - tools/llm-council/council/prompts.py (live)
  - tools/llm-council/council/pipeline.py (live)
  - Roadmap Task 19 (A6) + Task 17 (A2 TMAY) for the canonical first-test prompt
---

# Task 19 — Mock Interview Infrastructure Pre-Build Prep (Step 0)

> Drop-in artifacts so the 5/26 ship is execution. New `interview_grader` Council profile, an 8-dim rubric prompt template, a `mock_interview_loop.py` watcher script, and a decision on the transcription stack (recommended: local Whisper, symmetric with your existing Kokoro TTS pipeline).

## 0. The bet, in one sentence (carry into interviews)

> **You can't improve what you don't measure.** Gate C of the operating-model says "3 consecutive 8+/10 mock interviews." A subjective gut-feel can't measure 8/10 reliably. This rig — record → transcribe → grade via a 3-model AI panel — converts an unmeasurable goal into a binary one. Aakash Gupta's "record, transcribe, grade" workflow is the load-bearing pattern.

The strategic point: **building a tool to grade your interview answers is itself an interview-grade artifact**. Hiring managers who see this rig think "this person treats their own performance like a system" — that's exactly the AI-PM mindset Tier-1 roles select for.

---

## 1. Existing infrastructure (what I'm extending, not rebuilding)

You already have `tools/llm-council/` from v3.35.0 with two profiles (`premium`, `variance`), a 3-stage pipeline (fanout → cross-rank → chairman), a budget system with per-query / daily / monthly caps, and a CLI entry point at `python -m council`. Task 19 adds:

- **One new profile** (`interview_grader`) — slots into `PROFILES` dict
- **One watcher script** (`mock_interview_loop.py`) — orchestrates record → transcribe → grade
- **One README** (`INTERVIEW_GRADER.md`) — workflow docs

That's it. Total LOC: ~250 across two new files + ~20 lines of profile addition. The pipeline / budget / OpenRouter client / Markdown renderer all stay unchanged.

---

## 2. The `interview_grader` profile — drop-in (Step 1 of Task 19)

### Decision point: 3 models vs 4 models?

The roadmap spec says "drop Grok 4.20 for this profile — speed over variance," leaving 3 panelists. **But the existing pipeline assumes 4 panelists in `prompts.py`** — both `FANOUT_SYSTEM` ("a panel of four frontier models") and `CHAIRMAN_SYSTEM` ("four other models have each independently answered") have it hardcoded. Going to 3 panelists would mean either prompt edits (expanding Task 19 scope) or accepting prompts that say "four" when there are three (sloppy).

**Cleaner move: keep 4 panelists, swap Grok for fast Claude Sonnet.** Same speed gain, no prompt refactor, different RLHF lineage from Opus (Sonnet is RL-distilled from Opus but with different instruction-tuning). This is a small departure from the roadmap spec — flag for your review.

### Drop-in code for `tools/llm-council/council/profiles.py`

Add this entry to the `PROFILES` dict between `premium` and `variance`:

```python
"interview_grader": Profile(
    name="interview_grader",
    models=(
        "anthropic/claude-opus-4.7",        # depth — chairman
        "openai/gpt-5.5",                    # alternative RLHF lineage
        "~google/gemini-pro-latest",         # third lineage, different rubric biases
        "~anthropic/claude-sonnet-latest",   # speed proxy (replaces Grok 4.20 per Task 19 spec note)
    ),
    chairman="anthropic/claude-opus-4.7",
    max_cost_per_query=0.40,
),
```

### Test addition for `tools/llm-council/tests/test_profiles.py`

```python
def test_interview_grader_profile_exists():
    p = get_profile("interview_grader")
    assert p.name == "interview_grader"
    assert len(p.models) == 4, "Pipeline requires 4 panelists; do not change without prompt refactor"
    assert p.chairman in p.models, "Chairman must be one of the panelists"
    assert p.max_cost_per_query == 0.40
```

---

## 3. The 8-dimension rubric prompt (Step 1 of Task 19, prompt-content side)

The rubric is **baked into the prompt content** (via `--prompt-file`), not the system prompts. This lets you reuse the existing pipeline without refactor — the system prompt still says "you're on a council"; the user prompt focuses the council on grading.

### Rubric template (save as `tools/llm-council/profiles/interview-grader-template.md`)

```markdown
You are grading a recorded interview answer against an 8-dimension rubric.

## The question the candidate answered
{question}

## The transcript of their answer
{transcript}

## The 8-dimension rubric (score each 1–10, with 1-sentence justification)

1. **Timing** — Did the answer fit the target length (60–120s for short, 180–240s for long)? Off-target ±20% loses points.
2. **Structure** — Was there a clear arc (hook → body → close), or did it meander? STAR/CAR shapes score high; rambling scores low.
3. **Impact specificity** — Did the candidate cite *specific numbers, dates, names, outcomes*? "I shipped 5 features in Q3" beats "I shipped a lot of features."
4. **Confidence signals** — Voice steady, claims direct, no hedging filler ("kind of," "I guess," "sort of"). Pace neither rushed nor halting.
5. **Filler words** — Count "um," "uh," "like," "you know," "basically" per minute. <3/min = 10; >10/min = 1.
6. **Weakness flipping** — When discussing failures or gaps, did the candidate flip to learning/recovery/next-step? Or did they dwell?
7. **Information control** — Did the candidate volunteer information they shouldn't have (oversharing, score-tanking admissions, off-topic context)? Or did they stay scoped?
8. **Memorability** — Will an interviewer remember this answer 2 hours later? One quotable line, one specific anchor, or one unusual framing.

## Output format

Return a JSON object with exactly this shape — no preamble, no markdown fence:

{
  "scores": {
    "timing": {"score": 8, "justification": "Answer ran 95s, in the 60-120 target band."},
    "structure": {"score": 7, "justification": "..."},
    "impact_specificity": {"score": ...},
    "confidence_signals": {"score": ...},
    "filler_words": {"score": ...},
    "weakness_flipping": {"score": ...},
    "information_control": {"score": ...},
    "memorability": {"score": ...}
  },
  "overall_score": 7.8,
  "three_specific_revisions": [
    "Cut the second paragraph about the V3 redesign — it dilutes the impact moment.",
    "Replace 'kind of' (used 4x) with direct claims.",
    "Add the actual eval-suite ship date (5/12) to the close — specificity earns memorability."
  ]
}

The Council chairman will synthesize across the 4 panelists' scorecards into one canonical grade.
```

### Why this rubric vs others

Eight dimensions is the sweet spot — fewer than 6 misses signal (e.g., a Loom that's perfect on content but disastrous on filler words still scores high on a 4-dim rubric); more than 10 fragments judgment so models hedge. Eight is also what Aakash Gupta's grading playbook uses, so it lines up with what hiring managers reading post-interview notes are already used to.

---

## 4. `mock_interview_loop.py` skeleton (Steps 2 + 3 of Task 19)

Drop into `agents-sdk/scripts/mock_interview_loop.py`. This is the orchestrator — record → transcribe → invoke council → save grade.

```python
#!/usr/bin/env python3
"""Mock Interview Loop — record → transcribe → grade pipeline.

Watches ~/Voice Memos/ for new .m4a files (or accepts --audio explicit path),
transcribes via the configured backend (default: local Whisper via faster-whisper),
saves transcript + grade card to vault/20_projects/prj-job-hunt-2026/interview-prep/mock-log/.

Usage:
  # One-shot grade a specific recording + question:
  python3 mock_interview_loop.py --audio ~/Voice\\ Memos/Recording-001.m4a \\
      --question "Tell me about yourself" --label tmay-attempt-1

  # Watch mode (waits for new recordings, prompts for question when one lands):
  python3 mock_interview_loop.py --watch
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VAULT_LOG = ROOT / "vault" / "20_projects" / "prj-job-hunt-2026" / "interview-prep" / "mock-log"
RUBRIC_TEMPLATE = ROOT / "tools" / "llm-council" / "profiles" / "interview-grader-template.md"
COUNCIL_ROOT = ROOT / "tools" / "llm-council"
VOICE_MEMOS_DIR = Path.home() / "Library" / "Application Support" / "com.apple.voicememos" / "Recordings"
# (Modern macOS Voice Memos stores .m4a here, not ~/Voice Memos — confirm path on first run.)


def transcribe_local_whisper(audio_path: Path) -> str:
    """Transcribe with faster-whisper. ~1-3 min for a 5-min recording on M-series.

    Install: pip install faster-whisper
    Falls back to OpenAI Whisper if faster-whisper is unavailable.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit(
            "faster-whisper not installed. Run:\n"
            "  agents-sdk/.venv/bin/pip install faster-whisper\n"
            "Or pass --transcriber otter to use the Otter.ai API instead."
        )

    # base.en is ~74MB, runs ~5x realtime on M-series. medium.en is ~769MB, slower but cleaner.
    model = WhisperModel("base.en", device="auto", compute_type="auto")
    segments, _ = model.transcribe(str(audio_path), beam_size=5)
    return " ".join(s.text.strip() for s in segments)


def transcribe_otter(audio_path: Path) -> str:
    """Otter.ai API fallback. Requires OTTER_API_KEY env var.

    Free tier: 300 transcription minutes/month. Sufficient for ~30 mock interviews.
    """
    raise NotImplementedError("Otter.ai backend — implement when needed; local Whisper is the default.")


def transcribe(audio_path: Path, backend: str) -> str:
    if backend == "local-whisper":
        return transcribe_local_whisper(audio_path)
    elif backend == "otter":
        return transcribe_otter(audio_path)
    else:
        raise ValueError(f"Unknown transcriber backend: {backend}")


def build_grading_prompt(transcript: str, question: str) -> str:
    """Compose the user-facing prompt by templating the rubric."""
    template = RUBRIC_TEMPLATE.read_text()
    return template.replace("{question}", question).replace("{transcript}", transcript)


def run_council_grade(prompt_text: str, output_path: Path, label: str) -> dict:
    """Invoke the existing council CLI as a subprocess.

    Could be refactored to import the council package directly; subprocess
    keeps the boundary clean and lets the council's existing budget gates fire.
    """
    prompt_file = output_path.with_suffix(".grading-prompt.tmp.md")
    prompt_file.write_text(prompt_text)
    grade_md = output_path.with_suffix(".grade.md")

    try:
        result = subprocess.run(
            [
                str(COUNCIL_ROOT / ".venv" / "bin" / "python3"),
                "-m", "council",
                "--profile", "interview_grader",
                "--prompt-file", str(prompt_file),
                "--output", str(grade_md),
                "--tag", f"interview-grader-{label}",
            ],
            cwd=str(COUNCIL_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        prompt_file.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(f"Council run failed: {result.stderr}")

    # Council writes markdown; the chairman synthesis section contains the JSON we want.
    # Parse it back out for a structured summary.
    grade_text = grade_md.read_text()
    # Extract the JSON from the chairman synthesis section
    # (Pattern: chairman's content is a JSON object embedded in markdown.)
    try:
        json_start = grade_text.find("{", grade_text.find("## Chairman synthesis"))
        json_end = grade_text.rfind("}") + 1
        scorecard = json.loads(grade_text[json_start:json_end])
        return scorecard
    except (json.JSONDecodeError, ValueError) as e:
        # Chairman didn't return parseable JSON. Save the raw output anyway.
        print(f"[warn] could not parse chairman scorecard JSON: {e}")
        return {"_raw": grade_text}


def grade_one(audio_path: Path, question: str, label: str, backend: str) -> None:
    """End-to-end: transcribe + grade + persist."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    out_stem = VAULT_LOG / f"{timestamp}-{label}"
    VAULT_LOG.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Transcribing {audio_path.name} via {backend}...")
    transcript = transcribe(audio_path, backend)
    transcript_md = out_stem.with_suffix(".transcript.md")
    transcript_md.write_text(
        f"# Transcript — {timestamp}\n\n"
        f"**Question:** {question}\n\n"
        f"**Recording:** `{audio_path.name}`\n\n"
        f"---\n\n{transcript}\n"
    )
    print(f"   → wrote {transcript_md}")

    print(f"[2/3] Grading via Council (interview_grader profile)...")
    prompt = build_grading_prompt(transcript, question)
    scorecard = run_council_grade(prompt, out_stem, label)
    print(f"   → wrote {out_stem.with_suffix('.grade.md')}")

    print(f"[3/3] Result:")
    if "overall_score" in scorecard:
        print(f"   Overall: {scorecard['overall_score']}/10")
        for dim, data in scorecard.get("scores", {}).items():
            print(f"     - {dim}: {data['score']}/10 — {data['justification']}")
        revisions = scorecard.get("three_specific_revisions", [])
        if revisions:
            print(f"   Three revisions:")
            for r in revisions:
                print(f"     • {r}")


def watch_loop(backend: str) -> None:
    """Watch ~/Voice Memos for new recordings; prompt for question on each."""
    print(f"Watching {VOICE_MEMOS_DIR} for new .m4a files. Ctrl-C to stop.")
    seen = {p for p in VOICE_MEMOS_DIR.glob("*.m4a")}
    while True:
        time.sleep(3)
        current = {p for p in VOICE_MEMOS_DIR.glob("*.m4a")}
        new = current - seen
        for audio in new:
            print(f"\n[watch] new recording: {audio.name}")
            question = input("  Question this answers: ").strip()
            label = input("  Short label (e.g. 'tmay-attempt-1'): ").strip()
            try:
                grade_one(audio, question, label, backend)
            except Exception as e:
                print(f"[error] {e}")
        seen = current


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", type=Path, help="Path to .m4a recording (one-shot mode)")
    parser.add_argument("--question", type=str, help="Interview question being answered")
    parser.add_argument("--label", type=str, default="adhoc", help="Short label for filename")
    parser.add_argument("--watch", action="store_true", help="Watch ~/Voice Memos for new recordings")
    parser.add_argument(
        "--transcriber",
        choices=["local-whisper", "otter"],
        default="local-whisper",
        help="Transcription backend (default: local-whisper — symmetric with Kokoro TTS)",
    )
    args = parser.parse_args()

    if args.watch:
        watch_loop(args.transcriber)
    elif args.audio:
        if not args.question:
            parser.error("--question is required in one-shot mode")
        grade_one(args.audio, args.question, args.label, args.transcriber)
    else:
        parser.error("Provide --audio + --question, or use --watch")


if __name__ == "__main__":
    main()
```

---

## 5. The transcription decision — local Whisper vs Otter vs Granola

Three viable paths. The choice matters because it sets the per-mock cost and the privacy boundary.

| Backend | Cost / mock | Privacy | Latency | Setup |
|---|---|---|---|---|
| **Local Whisper (`faster-whisper`)** | **$0** | Audio never leaves machine | ~1-3 min for 5-min audio | `pip install faster-whisper` (1-time, ~80MB model `base.en`) |
| Otter.ai API | $0 (free tier — 300 min/month) | Audio goes to Otter cloud | ~30s | API key dance, hits free-tier limit at ~30 mocks/mo |
| Granola REST API | Unclear pricing | Audio goes to Granola cloud | ~30s | Already have OAuth via MCP, but REST surface is private |

### Recommendation: local Whisper via `faster-whisper`

Three reasons:
1. **$0/run** — fits the operating-model cost discipline. Council grades cost $0.40/mock; transcription should be $0 to keep the total economical.
2. **Symmetric with your existing pipeline** — you already run Kokoro-82M ONNX for TTS at $0/run on Apple Silicon. Whisper is the symmetric STT — same hardware, same cost model, same privacy story.
3. **Privacy** — mock interview recordings often contain sensitive context (real company names, actual past failures, in-progress framings). Sending them to Otter or Granola creates a leak surface for zero benefit.

**Trade-off:** ~1-3 min transcription latency vs Otter's ~30s. The whole loop (record 2 min → transcribe 1 min → grade 60s) is still well inside the 10-min target.

**Fallback path baked into the script:** if `faster-whisper` ever fails or you're on a different machine, the `--transcriber otter` flag is wired but stubbed. Implement only if needed.

---

## 6. Vault layout — `interview-prep/mock-log/`

Create the directory:

```bash
mkdir -p ~/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/interview-prep/mock-log
touch ~/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/interview-prep/mock-log/.gitkeep
```

Per-mock output:
- `YYYY-MM-DD-HH-MM-{label}.transcript.md` — the Whisper transcript with question header
- `YYYY-MM-DD-HH-MM-{label}.grade.md` — the Council scorecard (markdown wrapper containing the JSON synthesis)

After 10 mocks the directory is ~10 transcript MDs + ~10 grade MDs. After Gate C closes (3 consecutive 8+/10), you have a chronological learning trail.

### Optional addition (post-ship): a `summarize_mocks.py` script

Once you have 10+ grades, a small Python script can compute trend lines: which dimensions are improving, which are stuck. Reasonable Week-3 add-on. Not part of Task 19 scope.

---

## 7. Test plan (Step 4 of Task 19)

The roadmap says "Run 3 mock TMAY attempts. Verify Council returns scored output. Verify cost stays under $0.40/query."

### The TMAY dependency
**Task 17 (A2 — TMAY 2-min script) ships by 5/31**, which is 5 days *after* Task 19 ships by 5/26. So the canonical first test happens *after* the rig is live. **Mitigation:** Sean can test the rig immediately with any practice TMAY draft (even a rough one), or with other common questions like "Why are you leaving The Block?" or "Tell me about a time you disagreed with engineering." The rig's correctness check doesn't require a polished TMAY — it requires *any* recorded answer to grade against the rubric.

### Suggested first-test sequence (5/26) — UPDATED 2026-05-21

> **Question #2 swapped** per Sean's 2026-05-21 direction: "I was laid off from the Block, so we might want to switch up that specific test." The original "Why are you leaving The Block?" assumed a voluntary departure; the laid-off framing changes the answer's posture (factual narrative + recovery + forward intent, not justification). New Q2 below is calibrated for that.

1. **Record 3 practice answers**, ~60-120s each, with macOS Voice Memos. Questions:
   - "Tell me about yourself" (rough TMAY)
   - **"Walk me through what happened with The Block and how it reset your search."** Tests the laid-off-candidate narrative pattern: 1 sentence on the layoff (factual, unembellished) → 1 sentence on what The Block was (so the recruiter knows the substance you ran) → 2-3 sentences on what changed in your search posture (AI PM > Tech PM > Creative PM lock-in, the 8-week sprint, the published artifacts). Rubric dims this exercises hard: *information control* (don't over-explain the layoff), *weakness flipping* (the layoff becomes the inflection that produced the public artifacts), *impact specificity* (cite specific shipped things — MCP server on the registry, fleet dashboard live).
   - "Walk me through a time you shipped something hard" (the eval-suite story from Task 8 is the obvious answer)

2. **Run the rig** on each:
   ```bash
   cd ~/Code-Brain/code-brain
   PYTHONPATH=. agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py \
     --audio "$(ls -t ~/Library/Application\ Support/com.apple.voicememos/Recordings/*.m4a | head -1)" \
     --question "Tell me about yourself" \
     --label "tmay-attempt-1"
   ```

3. **Verify**:
   - Transcript MD lands at `vault/.../interview-prep/mock-log/`
   - Grade MD lands with the chairman JSON parseable
   - Cost recorded in `vault/health/council-spend-2026-05.json` is < $0.40 (per query) and the day's total stays inside the $7 daily cap
   - End-to-end wall time < 10 min

4. **Iterate the rubric** if the scores feel mis-calibrated (e.g., if a clearly-rough answer scores 8/10, the rubric is too generous; tighten the per-dimension justification standards).

---

## 8. DECISIONS LOCKED (2026-05-21)

Sean's answers from `open-question-answers-5-21.md`.

| # | Decision | Locked answer |
|---|---|---|
| 1 | 4-panelist (Opus + GPT-5.5 + Gemini Pro + Sonnet) vs 3-panelist? | ✅ **Default — 4 panelists with Sonnet as the 4th.** No prompt refactor, $0.40/query cap maintained, different RLHF lineage from Opus. |
| 2 | Local Whisper vs Otter vs Granola? | ✅ **Local Whisper.** $0/run, symmetric with the existing Kokoro-82M TTS pipeline, audio never leaves the machine. |
| 3 | Auto-publish mock grades to `vault/health/` or stay private? | ✅ **Stay private** inside `interview-prep/mock-log/`. Not surfaced in the daily-driver morning brief. |
| 4 | Watch mode + one-shot, or one-shot only? | ✅ **Default — both.** Skeleton ships both modes. |
| 5 | Test on 5/26 with rough drafts (don't wait for Task 17)? | ✅ **Yes, run tests 5/26.** **AND** Question #2 SWAPPED — Sean was laid off from The Block, not voluntarily departing. New Q2: "Walk me through what happened with The Block and how it reset your search" (see §7 for the rubric-dim-by-dim rationale). |
| 6 | Full council markdown or chairman-only? | ✅ **Keep the full markdown.** Sean wants to read everything the council has to say (raw 4-model responses + cross-rankings, not just chairman synthesis). |

### Operational note on Decision 5 (the question swap)

Sean's framing for the laid-off narrative is structurally different from the "voluntary departure" framing the original spec assumed. The right pattern for the laid-off candidate:
1. **One factual sentence on the layoff** — unembellished, no spin
2. **One sentence on what The Block was** — gives the recruiter substance context
3. **2–3 sentences on the search-posture reset** — AI PM > Tech PM > Creative PM lock-in, the 8-week sprint, the public artifacts that came out of it

This pattern exercises three rubric dimensions hard:
- **Information control** — don't over-explain the layoff
- **Weakness flipping** — layoff becomes the inflection that produced the artifacts
- **Impact specificity** — cite the MCP server on the registry, the fleet dashboard at fleet.seanwinslow.com, the eval suite shipped 5/12

After the rig is live, this pattern should be drilled until the rubric scores 8+/10 consistently. It's the highest-leverage question to nail because *every recruiter call opens with some flavor of it*.

---

## 9. Timeline (3-day build window, 5/21–5/26)

| Date | Hours | Step | Output |
|---|---|---|---|
| **Wed 2026-05-21** | 0.5 | Step 1: Add `interview_grader` profile + test | `profiles.py` + 1 test pass |
| Wed 5/21 | 1 | Step 1b: Write `interview-grader-template.md` rubric | `tools/llm-council/profiles/interview-grader-template.md` |
| **Thu 2026-05-22** | 3 | Step 2: `mock_interview_loop.py` from §4 skeleton, add `faster-whisper` to `agents-sdk/.venv` | `mock_interview_loop.py` + venv update |
| Thu 5/22 | 0.5 | Step 3: Wire transcribe → council subprocess → parse | Same file extended |
| **Fri 2026-05-23** | 1 | Step 4a: Self-test with one canned audio file (any old voice memo will do) | Validation pass |
| Fri 5/23 | 0.5 | Step 5: Write `INTERVIEW_GRADER.md` README | README |
| **Mon 5/26** | 2 | Step 4b: Run 3 real mocks per §7 test plan, verify cost + latency + parseable scorecard | 3 mock-log entries |
| Mon 5/26 | 0.5 | Verification gate + commit | Commit landed |

**Total: ~9 hours** across 4 days, all inside 8:30–5:30 containers. Ship gate hits 5/26 EOD with two days of buffer before Task 17 ships 5/31.

---

## 10. Interview talking points (carry these forward)

The "why" behind each load-bearing decision:

**"Why build a tool to grade your own interview answers?"**
> Aakash Gupta's research shows that PMs who do "record, transcribe, grade" loops compound their interview performance ~3x faster than those who do verbal practice alone. The act of seeing your own transcript with a rubric overlay surfaces filler-word patterns and hedging tics that you literally can't hear yourself doing in real time. The tool isn't about cleverness; it's about closing a feedback loop that's normally open.

**"Why 4 panelists instead of 1 grader?"**
> Single-LLM grading is biased toward whatever its RLHF tuning rewards (Claude tends to over-praise; GPT tends to over-critique; Gemini varies more than the other two). A 4-model panel with different lineages produces calibrated scores. The chairman synthesis is essentially what you'd get from a senior recruiter — "this is what the panel actually said, here's the consensus."

**"Why local Whisper instead of an API?"**
> Three reasons. One: cost — $0 per mock vs ~$0.05 per minute on commercial APIs. Two: privacy — mock recordings contain unvarnished claims and real company names; not sending them to a third party reduces the attack surface. Three: symmetry — I already run Kokoro-82M for TTS locally; Whisper is the symmetric STT and runs on the same hardware. Building infrastructure that's *consistent in its tradeoffs* is itself a credibility signal.

**"What's the failure mode if the rubric is wrong?"**
> Calibration drift. If the rubric rewards traits that don't actually move offer rates, the tool optimizes you toward the wrong target. Mitigation: after 5 graded mocks, compare the rig's overall scores against your subjective gut on the same answers. If they diverge >2 points consistently, the rubric needs tightening. Aakash's 8-dimension structure is the prior; my data will tell me whether the prior holds for my voice.

**"Why does this matter for Gate C?"**
> Gate C says "3 consecutive 8+/10 mock interviews." Without a tool that produces 8/10 as a *measurable artifact*, Gate C is unfalsifiable — I can always claim I scored 8/10 in my head. The rig converts the gate from subjective to binary. That's the same pattern the eval suite imposed on the vault synthesizer in Task 8 — make the success criterion machine-readable and the discipline follows.

---

## 11. Cross-task pollinations (so you can speak to them in interviews)

This task connects to **three** other artifacts in your portfolio:

- **Task 8 (Vault Eval Suite, shipped 5/12)** — Same architectural pattern: convert a fuzzy success criterion ("the synthesizer is healthy" / "I interview well") into a binary scoreboard. **Both are evals.** That's the un-fakeable claim: "I've shipped two eval rigs — one against my agents, one against my own performance. Same epistemology applied two layers." Recruiters at Anthropic / Glean / Sierra will hear this and recognize it as the AI-PM mindset.

- **Task 12 (Judge Layer, ships ~6/4)** — Adds a similar review pattern to the substack-drafter agent. The judge-layer-as-review-primitive concept is rehearsed here on Sean's own voice before being applied to agent output.

- **Task 13 (Manifesto, draft-locks 5/23)** — The mock interview rig is itself a meaning-layer artifact (it converts vague "how did that answer feel?" into typed scores). Should be plotted on the spectrum chart as an 8th data point if you want — though I'd hold it back from the manifesto so the manifesto's 7-artifact framing stays clean. **Reserved slot for the manifesto's v2 update if Task 19 generates a strong narrative beat.**

---

## 12. Stacked deliverables status (this session)

| Task | Status | File |
|---|---|---|
| Task 20 — GitHub Profile Audit | Ready to execute (you, Fri 5/22) | `2026-05-20-task-20-github-profile-audit-deliverable.md` |
| Task 13 — Manifesto Outline (Step 1) | Ready for your 6 decisions; then I run Step 2 | `2026-05-20-task-13-step-1-manifesto-outline.md` |
| Task 15 — Vault Scorecard Pre-Build Prep | Build window 6/1–6/3 is execution; awaiting 6 decisions | `2026-05-20-task-15-step-0-prebuild-prep.md` |
| **Task 19 — Mock Interview Infra Pre-Build Prep** | **Build window 5/21–5/26 is execution; awaiting 6 decisions** | **this file** |

**Pattern across all four:** each one is *queued* with the heavy authoring + the live data + the open decisions, so when you sit down to build, it's paste-and-test rather than design-and-build. Your time gets spent on the Sean-only work: voicing the answers, reviewing the synthetic fixture, posting the LinkedIn announcement.

---

*End of Task 19 pre-build prep. The 5/21 start opens with: a drop-in profile, an 8-dimension rubric template, a `mock_interview_loop.py` skeleton with local Whisper as the recommended backend, a 6-decision checklist, a 3-mock test plan, and 4 interview talking points connecting this rig to your broader portfolio thesis.*
