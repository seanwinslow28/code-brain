# Mock Interview Rig — Run Cheat-Sheet

> Record → transcribe (local Whisper, $0) → grade (Council, ~$0.40) → read the scoreboard.
> Full docs: `tools/llm-council/profiles/INTERVIEW_GRADER.md`. The mic is the only input device.

All commands run from the repo root:

```bash
cd ~/Code-Brain/code-brain
```

## 1. Fastest test — no recording needed (text in, grade out)

Use this to iterate on wording or sanity-check the pipeline. ~20s, ~$0.40.

```bash
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py \
  --transcript-text "PASTE YOUR ANSWER TEXT HERE" \
  --question "Tell me about yourself" \
  --label tmay-text-1
```

## 2. Grade a recording (one-shot)

Record in QuickTime (File → New Audio Recording → save to Desktop), then:

```bash
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py \
  --audio ~/Desktop/tmay-1.m4a \
  --question "Tell me about yourself" \
  --label tmay-attempt-1
```

## 3. Hands-free watch mode

Leave it running; it grades each new Voice Memo and prompts you for the question + label.

```bash
agents-sdk/.venv/bin/python3 agents-sdk/scripts/mock_interview_loop.py --watch
```

## Find your newest recording (if using Voice Memos)

```bash
find ~/Library -name "*.m4a" -newermt "-1 hour" 2>/dev/null | head
```

## The three first-test questions (drill these to 8+/10 ×3)

1. `"Tell me about yourself"` → TMAY (`../tmay-script.md`)
2. `"Walk me through what happened with The Block and how it reset your search"` → contained layoff answer (`../tmay-per-company-variations.md`)
3. `"Walk me through a time you shipped something hard"` → eval-suite story (`../story-bank.md`, Story 1)

## What you get (here in mock-log/, timestamped)

- `*.transcript.md` — what Whisper heard (read this first — filler words you can't hear yourself say)
- `*.grade.md` — full raw Council output (4 models + chairman prose)
- `*.summary.md` — the scoreboard: median per dimension, overall, pass/fail on 8.0, top revisions

## Reminders

- Cost: ~$0.40 per grade (tracked in `vault/health/council-spend-*.json`, $7/day cap). Transcription is $0.
- A dimension flagged ⚠️ means the 4 models disagreed by 3+ points — that score is least reliable.
- First grades usually land 6–7; the usual point-losers are **filler words** and **timing**, both fixed by reading the transcript.
