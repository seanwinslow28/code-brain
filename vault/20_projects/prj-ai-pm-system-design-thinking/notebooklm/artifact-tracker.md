# NotebookLM Artifact Tracker

Notebook: `bcb4e6aa-9da7-49fe-8c65-46d27110313e` — "System Design Thinking for AI PM"

One row per generated artifact. Update on every generate and every download.

**The audio arc, per module** (from curriculum-map.md):
1. **Pre-brief** — `--format brief --length short`, ~5 min. Vocabulary laid down *before* the deep dive, so nothing in it is unfamiliar.
2. **Deep-dive** — `--format deep-dive --length long`. The module, anchored to one real product throughout.
3. **Debate** — `--format debate`. The module's core trade-off argued honestly both ways.
4. **Spaced re-listen** of the pre-brief roughly a week later. (No new artifact — a calendar item.)

**Every generation carries the calibration instructions verbatim.** Prompt files live in `notebooklm/audio-instructions/`. The three non-negotiables:
- Never explain what an agent, harness, model or API is.
- Define every statistical term in plain language on first use.
- **Never mention a company, incident, paper or researcher without a one-sentence setup.** This is the specific defect that killed the retired curriculum's M1 audio.

**Source selection is mandatory** (`-s`), never whole-notebook. Pass each `-s` as an explicit flag — a shell variable holding several `-s` pairs does not word-split correctly through this CLI and fails with `VALIDATION_ERROR` naming the whole string as one ID.

| Date | Module | Type | Artifact ID | Status | Downloaded to |
|------|--------|------|-------------|--------|---------------|
| 2026-08-17 | M1 | Audio — pre-brief (brief/short) | `747416f7` | completed (in notebook) | not downloaded — Sean listens in the notebook |
| 2026-08-17 | M1 | Audio — deep-dive (long) | `5f88a198` | completed (in notebook) | not downloaded — Sean listens in the notebook |
| 2026-08-17 | M1 | Audio — debate | `164db4c4` | completed (in notebook) | not downloaded — Sean listens in the notebook |

M1 source selection: `2251b249` (lesson) · `bb367054` (PAIR guidebook) · `f0988a1f` (ML thresholds) · `66c038cd` (Amazon case).

## Known flakes

- Audio, video, quiz, flashcard and infographic generation rate-limit. Wait 5–10 min and retry; `--retry N` handles it inline.
- `.mp3` and `.mp4` files are local-only and gitignored — they also live in the notebook.

## Deliberately NOT generated

- **Quizzes and flashcards.** The retired program produced 7 of each and Sean consumed none. Recall drills are not the bottleneck; forward design, written artifacts and spoken articulation are. Revisit only if a spaced re-listen proves insufficient for retention.
- **Explainer videos.** Same reasoning, and they cost the most wall-clock of any artifact type.
