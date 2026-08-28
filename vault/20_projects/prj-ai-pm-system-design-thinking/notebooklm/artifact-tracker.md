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

| 2026-08-17 | M2 | Audio — pre-brief (brief/short) | `b7b84c07` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-17 | M2 | Audio — deep-dive (long) | `afd5322f` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-17 | M2 | Audio — debate | `d1583ba7` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-22 | M3 | Audio — pre-brief (brief/short) | `63351ebb` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-22 | M3 | Audio — deep-dive (long) | `5671f806` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-22 | M3 | Audio — debate | `5d9b1bef` | completed (in notebook) | not downloaded — listen in the notebook |
| 2026-08-22 | M4 | Audio — pre-brief (brief/short) | `02650839` | completed (in notebook) — *Why Maximizing AI Trust Is a Trap* | not downloaded — listen in the notebook |
| 2026-08-22 | M4 | Audio — deep-dive (long) | `1bd75057` | completed (in notebook) — *Calibrating User Trust in AI Systems* | not downloaded — listen in the notebook |
| 2026-08-22 | M4 | Audio — debate | `a92ed175` | completed (in notebook) — *Should users see AI confidence scores* | not downloaded — listen in the notebook |
| 2026-08-24 | M5 | Audio — pre-brief (brief/short) | `3de16887` | completed (in notebook) — *Manual trace reviews and AI unit economics* | not downloaded — listen in the notebook |
| 2026-08-24 | M5 | Audio — deep-dive (long) | `251be81c` | completed (in notebook) — *AI Unit Economics and Production Evaluation* | not downloaded — listen in the notebook |
| 2026-08-24 | M5 | Audio — debate | `48c5e959` | completed (in notebook) — *Should AI agents judge their own work* | not downloaded — listen in the notebook |

M1 source selection: `2251b249` (lesson) · `bb367054` (PAIR guidebook) · `f0988a1f` (ML thresholds) · `66c038cd` (Amazon case).
M2 source selection: `5b756d4b` (lesson) · `1ab0974b` (PAIR data chapter) · `9ac74ee9` (Datasheets) · `dbb721bc` (RAG taxonomy) · `d269db15` (Zillow).
M3 source selection: `37b21bfc` (lesson) · `8641160f` (Anthropic agents) · `ce870d74` (Sculley) · `a06dd429` (MS agentic taxonomy) · `9d283700` (Harrison Chase harness).
M5 source selection: `f7b99e57` (lesson) · `bc1cf6c0` (Hamel evals) · `4301f4c3` (Hamel LLM-judge) · `af5b612b` (ML Test Score) · `1dfcc9f0` (LLM-as-judge survey) · `0d1f0ebd` (ICONIQ 2026) · `ce870d74` (Sculley, carried from M3 — the debate omits it and ICONIQ stays in).
M4 source selection: `7a8e6894` (lesson) · `a7548548` (Amershi CHI 2019) · `d98b596c` (PAIR Errors) · `ff6fd6a9` (PAIR Explainability + Trust) · `230a9929` (Intercom Fin outcomes) · `8fa09511` (Zhang/Liao/Bellamy FAT* 2020).

**M4 prompt note:** the three M4 prompts share a common preamble kept in `audio-instructions/_m4-calibration-block.txt` and concatenated into each prompt file. M4's calibration block is the inverse of M3's — it instructs the hosts NOT to tell Sean he already knows this material, names the three narrow transfers that do exist, and lists what must be taught from zero. Prompts are passed with `--prompt-file`, which handles multi-thousand-character instructions the positional argument would mangle.

## Prompt length — an open question with one datapoint each way

Prompt files are passed with `--prompt-file`; the positional argument mangles anything multi-thousand-character. Sizes so far: M3 deep-dive 7,559 chars, M4 11,767, M5 15,099. **No cap has ever been hit**, and M5 is the evidence that the long end still works — its deep-dive prompt has eleven numbered items and the generated title, *"AI Unit Economics and Production Evaluation,"* reflects item **10 of 11**, so the tail of the prompt was read rather than truncated. Treat ~15K as demonstrated-safe and anything beyond it as untested.

## Verify the queue, don't trust the exit code

**`generate audio` can fail and still exit 0.** On 2026-08-17 a loop queued three M2 episodes and reported all three "queued"; `artifact list` showed only one had been created. The other two produced an error payload that a lazy JSON parse read as success.

**Always confirm against `artifact list` after generating**, and count. Expect `modules × 3`. A generate command that printed something is not a generate command that did something — same lesson as the source-fetch rule in `source-manifest.md`.

## Known flakes

- Audio, video, quiz, flashcard and infographic generation rate-limit. Wait 5–10 min and retry; `--retry N` handles it inline.
- `.mp3` and `.mp4` files are local-only and gitignored — they also live in the notebook.

## Deliberately NOT generated

- **Quizzes and flashcards.** The retired program produced 7 of each and Sean consumed none. Recall drills are not the bottleneck; forward design, written artifacts and spoken articulation are. Revisit only if a spaced re-listen proves insufficient for retention.
- **Explainer videos.** Same reasoning, and they cost the most wall-clock of any artifact type.
