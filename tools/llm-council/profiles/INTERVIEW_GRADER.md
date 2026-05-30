# Interview Grader — mock-interview measurement rig (Task 19 / A6)

The measurement infrastructure for **Gate C** of the job-hunt operating model: *"3 consecutive 8+/10 mock interviews."* You can't improve what you don't measure — this rig converts a gut-feel goal into a binary one. Record → transcribe → grade against an 8-dimension rubric via a 4-model LLM Council.

> **The interview talking point:** *building a tool to grade your own interview answers is itself an interview-grade artifact.* It's the same epistemology as the vault eval suite (Task 8) — convert a fuzzy success criterion into a machine-readable scoreboard. Two eval rigs, one against my agents, one against my own performance.

## The pieces

| Piece | Path | Role |
|---|---|---|
| Council profile | `council/profiles.py` → `interview_grader` | 4 panelists (Opus / GPT-5.5 / Gemini Pro / Sonnet), Opus chairman, $0.40/query cap |
| Rubric template | `profiles/interview-grader-template.md` | The 8-dimension rubric; `{question}` + `{transcript}` tokens are filled at runtime |
| Orchestrator | `agents-sdk/scripts/mock_interview_loop.py` | record → transcribe (local Whisper) → council → aggregate → write |
| Output | `vault/20_projects/prj-job-hunt-2026/interview-prep/mock-log/` | per-mock `.transcript.md` + `.grade.md` + `.summary.md` |

## How a grade is computed (the one design decision to know)

The Council **chairman emits prose, not JSON** — its system prompt synthesizes a narrative read. So the canonical **numeric** grade is NOT parsed from the chairman. Instead:

1. Each of the **4 panelists** returns a JSON scorecard (the rubric instructs this).
2. The orchestrator parses all four from the `## Council responses` section.
3. Per dimension, it takes the **median** of the panelists' scores (robust to one outlier); overall = mean of the 8 medians.
4. The **chairman's prose** is preserved as the qualitative read in the `.summary.md`.

This is more faithful to "a 4-model calibrated panel" than trusting one model to re-emit JSON — and a panelist disagreement of ≥3 points on any dimension gets flagged (⚠️) so you can see where the models split. *(This is the documented deviation from the 2026-05-20 prep-doc skeleton, which assumed the chairman would emit the JSON.)*

## Setup (one-time, on the Mac)

```bash
# Local transcription — $0/run, audio never leaves the machine (symmetric with Kokoro TTS).
agents-sdk/.venv/bin/pip install faster-whisper
# OpenRouter key for the council (already configured if you've run council before):
#   tools/llm-council/.env  ->  OPENROUTER_API_KEY=...
```

## Usage

```bash
cd ~/Code-Brain/code-brain

# One-shot: grade a specific Voice Memo against a question
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py \
  --audio "$(ls -t ~/Library/Application\ Support/com.apple.voicememos/Recordings/*.m4a | head -1)" \
  --question "Tell me about yourself" \
  --label tmay-attempt-1

# Watch mode: leave it running, it prompts for the question on each new recording
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py --watch

# Text-only: grade an already-written answer (skip audio + Whisper) — handy for fast TMAY iteration
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py \
  --transcript-text "I'm a product manager who spent about ten years..." \
  --question "Tell me about yourself" --label tmay-text-1
```

Each run writes three files to `mock-log/`, prints the median scorecard + the merged top revisions, and tells you whether it cleared the 8.0 Gate-C bar.

## The 8 dimensions

timing · structure · impact specificity · confidence signals · filler words · weakness flipping · information control · memorability. Full definitions in `interview-grader-template.md`. Eight is Aakash Gupta's grading set — it lines up with what hiring managers already use in post-interview notes.

## The first test sequence (3 questions)

1. **"Tell me about yourself"** — the TMAY (`interview-prep/tmay-script.md`).
2. **"Walk me through what happened with The Block and how it reset your search."** — the contained layoff answer (`tmay-per-company-variations.md`). Exercises information-control + weakness-flipping hardest.
3. **"Walk me through a time you shipped something hard."** — the eval-suite story (Story Bank Story 1).

Drill until each clears 8+/10 three times running. Cost: ~$0.40/grade against the council's $7/day cap; transcription is free.

## Cost + privacy

- Grading: ~$0.40/mock (council `interview_grader` cap), tracked in `vault/health/council-spend-*.json`.
- Transcription: $0 (local `faster-whisper`, `base.en`).
- Privacy: recordings + transcripts stay on-machine and in the private vault `mock-log/` — never surfaced in the daily-driver brief.

## Tests

```bash
# Pure parse/aggregate logic (no network, no audio):
cd agents-sdk && python3 -m pytest tests/test_mock_interview_loop.py -q
# Profile registration:
cd tools/llm-council && python3 -m pytest tests/test_profiles.py -q
```
