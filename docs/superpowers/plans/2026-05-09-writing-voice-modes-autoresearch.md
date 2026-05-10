# Writing Voice Modes AutoResearch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-skill autoresearch optimization harness that mutates `.claude/skills/writing-voice-modes/SKILL.md` against a hybrid eval suite (3 deterministic structural checks + 3 LLM-judge criteria with anti-Goodhart safeguards) and runs an autonomous keep-or-revert loop until the success threshold is hit, a halt condition fires, or 25 iterations elapse.

**Architecture:** Karpathy-style three-file pattern adapted to Claude Code. Fixed infrastructure (`skill_optimizer.py` orchestrator + `evals.yaml` + `judge_prompt.txt` + `structural_checks.py`) is the "rules of the game." The mutable artifact is the body of `SKILL.md` (with frontmatter + example outputs + meta-navigation sections protected by a pre-write diff guard). The optimizer subagent's `program.md` is the natural-language instructions. Generation runs on Opus 4.7; LLM judging runs locally on Qwen3-14B (via Ollama on Mac Mini) with Sonnet 4.6 sample-checks every 5 iterations. Decision rule is 3-iteration moving average with bootstrap-CI keep/revert. Six trip-wires guard against Goodhart drift.

**Tech Stack:** Python 3.11+, Claude Agent SDK 0.1.63, anthropic SDK, Ollama (local Qwen3-14B), pytest, NLTK or scikit-learn for stylometry, gitpython or subprocess for git ops, FileLock for concurrency.

**Source spec:** [docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md](../specs/2026-05-09-writing-voice-modes-autoresearch-design.md) (commit `ab113c9`)

---

## Phases at a Glance

| Phase | Theme | Tasks | Pause point |
|---|---|---|---|
| 0 | Pre-flight scaffolding (branch, dirs, config, Sean's 60%-dial samples) | 4 | After Phase 0 — verify scaffolding before code |
| 1 | Pure-function lib modules (structural checks, stylometry, mutation guard, decision, trip-wires) — TDD | 8 | After Phase 1 — full pytest green before judge work |
| 2 | LLM-judge runner (Qwen3-14B local + Sonnet sample-check + 3-judge ensemble) | 3 | After Phase 2 — judge calibrated against hand-labels |
| 3 | Eval data + judge templates (evals.yaml, sealed.yaml, program.md, judge_prompt.txt, baselines) | 6 | After Phase 3 — all pre-flight data files locked |
| 4 | Orchestrator skeleton + 12 helpers (preflight, generation, scoring, mutation/git, results.tsv, main loop, utility helpers, data-layer helpers, external-call helpers) | 9 | After Phase 4 — dry-run completes end-to-end |
| 5 | Integration validation + docs + first live run | 3 | Final |

**Total: 33 tasks, ~14-18 hours of implementation work** (excluding the wall-clock time of the optimization run itself, which is ~9-13 hours).

---

## Phase 0 — Pre-flight Scaffolding

### Task 0.1: Create the autoresearch branch

**Files:**
- N/A (git operation only)

- [ ] **Step 1: Verify clean working tree on a known starting branch**

Run: `git status --short && git rev-parse --abbrev-ref HEAD`
Expected: clean (no `M` or `??` staged changes that conflict), branch is `docs/job-hunt-prompt-recalibration` or `main`.

- [ ] **Step 2: Create and checkout the autoresearch branch**

Run: `git checkout -b autoresearch/writing-voice-modes-2026-05-09`
Expected: `Switched to a new branch 'autoresearch/writing-voice-modes-2026-05-09'`

- [ ] **Step 3: Verify branch is set**

Run: `git rev-parse --abbrev-ref HEAD`
Expected: `autoresearch/writing-voice-modes-2026-05-09`

---

### Task 0.2: Sean writes 2 60%-dial samples to voice-samples.md

**Files:**
- Modify: `.claude/skills/writing-voice-modes/references/voice-samples.md` (append new section at end)

> **Note:** This task is performed by Sean, not the implementer. The agent should print the instructions and pause. Once Sean confirms the samples are written and committed, proceed to Task 0.3.

- [ ] **Step 1: Print instructions to Sean and wait**

Print exactly:
```
PRE-FLIGHT BLOCKER — Sean's writing exercise

Append a new section to .claude/skills/writing-voice-modes/references/voice-samples.md:

## Professional Dial — 60%

Real Sean voice dialed down for cross-functional / professional contexts. Sarcasm survives, wild anecdotes don't. Dry humor in examples; never in the critical path.

### Sample 1 — Slack message about a delayed feature launch (~80 words)
[Sean writes here]

### Sample 2 — Stakeholder update intro about a sprint outcome (~150 words)
[Sean writes here]

When done, commit the change:
  git add .claude/skills/writing-voice-modes/references/voice-samples.md
  git commit -m "docs(voice-samples): add 60% professional dial samples for autoresearch calibration"

Reply 'done' to continue.
```

- [ ] **Step 2: Confirm the section exists**

Run: `grep -A 1 "## Professional Dial" .claude/skills/writing-voice-modes/references/voice-samples.md`
Expected: section header present.

- [ ] **Step 3: Confirm both samples are non-empty**

Run: `awk '/## Professional Dial/,/^---$/' .claude/skills/writing-voice-modes/references/voice-samples.md | wc -w`
Expected: word count ≥ 200 (covers both samples plus headers).

---

### Task 0.3: Create directory scaffolding

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/__init__.py`
- Create: `agents-sdk/data/skill-optimizer/.gitkeep`

- [ ] **Step 1: Create the lib module directory**

Run: `mkdir -p agents-sdk/lib/skill_optimizer && touch agents-sdk/lib/skill_optimizer/__init__.py`
Expected: directory + empty `__init__.py` exist.

- [ ] **Step 2: Create the data directory with .gitkeep**

Run: `mkdir -p agents-sdk/data/skill-optimizer && touch agents-sdk/data/skill-optimizer/.gitkeep`
Expected: directory + empty `.gitkeep` exist.

- [ ] **Step 3: Add module docstring**

Replace contents of `agents-sdk/lib/skill_optimizer/__init__.py` with:
```python
"""skill_optimizer — autoresearch optimization harness for Claude Code skills.

Adapted from Karpathy's autoresearch pattern (March 2026). Optimizes the body
of a SKILL.md file against a hybrid eval suite (deterministic structural checks
+ LLM-judge binary evaluations) via an autonomous mutate→score→keep-or-revert
loop. See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md.
"""
```

- [ ] **Step 4: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/__init__.py agents-sdk/data/skill-optimizer/.gitkeep
git commit -m "scaffold(skill_optimizer): create lib module + data directory"
```

---

### Task 0.4: Add `[agents.skill_optimizer]` config block

**Files:**
- Modify: `agents-sdk/config.toml`

- [ ] **Step 1: Read the current config to find insertion point**

Read: `agents-sdk/config.toml`
Find: the last `[agents.*]` section (e.g., `[agents.gemini_researcher]` or similar) — locate its closing line.

- [ ] **Step 2: Append the new agent block after the last `[agents.*]` section**

Add:
```toml
[agents.skill_optimizer]
enabled = true
schedule = "manual"  # not on launchd; run by hand
target_skill_dir = ".claude/skills/writing-voice-modes"
target_skill_md = ".claude/skills/writing-voice-modes/SKILL.md"
branch = "autoresearch/writing-voice-modes-2026-05-09"
generator_model = "claude-opus-4-7"
judge_model_local = "qwen3-14b-research:latest"
judge_model_sonnet_check = "claude-sonnet-4-6"
ollama_base_url = "http://localhost:5050"
sonnet_check_every_n_iterations = 5
max_iterations = 25
plateau_halt_iterations = 3
runs_per_prompt = 15
training_prompts_count = 5
holdout_prompts_count = 2
surprise_prompts_count = 3
surprise_score_every_n_iterations = 5
cost_cap_usd_hard = 200.00
cost_cap_usd_soft = 50.00
results_path = "data/skill-optimizer/writing-voice-modes-results.tsv"
stylometry_baseline_path = "data/skill-optimizer/stylometry_baseline.json"
calibration_set_path = "data/skill-optimizer/calibration_set.jsonl"
evals_path = ".claude/skills/writing-voice-modes/evals.yaml"
evals_sealed_path = ".claude/skills/writing-voice-modes/evals.sealed.yaml"
program_md_path = "lib/skill_optimizer/program.md"
judge_prompt_path = "lib/skill_optimizer/judge_prompt.txt"
```

- [ ] **Step 3: Verify TOML parses**

Run: `cd agents-sdk && python3 -c "import tomllib; tomllib.load(open('config.toml','rb')); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add agents-sdk/config.toml
git commit -m "config(skill_optimizer): add [agents.skill_optimizer] block"
```

---

> **Pause point: Phase 0 complete.** Branch created, voice-samples.md updated, scaffolding in place, config valid. Verify by running `git log --oneline | head -5` — should see 4 new commits on the autoresearch branch.

---

## Phase 1 — Pure-function Lib Modules (TDD)

These modules have zero external dependencies and can be tested with deterministic fixtures. Strict test-first ordering. Each task ends with passing tests + a commit.

### Task 1.1: `structural_checks.substack_format_intro`

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/structural_checks.py`
- Test: `agents-sdk/tests/test_structural_checks.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_structural_checks.py`:
```python
"""Tests for structural_checks module."""
import pytest
from agents_sdk.lib.skill_optimizer.structural_checks import (
    substack_format_intro,
)


class TestSubstackFormatIntro:
    def test_passes_on_good_intro(self):
        text = (
            "I spent eleven months building Zapier workflows with the quiet "
            "devotion of a man assembling IKEA furniture — following instructions "
            "I half-understood, ignoring the leftover pieces, and telling myself "
            "it looked right enough.\n\n"
            "Thirty-seven zaps. Each one a small miracle of duct tape and prayer.\n\n"
            "Agents do."
        )
        passed, reason = substack_format_intro(text)
        assert passed is True, reason

    def test_fails_when_first_paragraph_too_short(self):
        text = "Short.\n\nSecond paragraph here is the real meat.\n\nClose."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "first paragraph" in reason.lower()

    def test_fails_when_first_paragraph_too_long(self):
        long_para = " ".join(["word"] * 250) + "."
        text = f"{long_para}\n\nSecond.\n\nClose."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "first paragraph" in reason.lower()

    def test_fails_when_no_paragraph_breaks(self):
        text = "One block of text without any paragraph breaks at all so it just runs on like this and never lets the reader breathe."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "paragraph break" in reason.lower()

    def test_fails_when_closer_too_long(self):
        text = (
            "First paragraph here has enough words to clear the sixty word minimum "
            "threshold without trouble because we are padding it out intentionally "
            "to make the first paragraph rule pass for this test case here.\n\n"
            "Second paragraph.\n\n"
            "This closing sentence is absolutely far too long to count as a Sean closer because it just keeps going and going past twelve words easily."
        )
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "closer" in reason.lower()
```

- [ ] **Step 2: Run test to verify it fails (module doesn't exist)**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_structural_checks.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agents_sdk.lib.skill_optimizer.structural_checks'`

- [ ] **Step 3: Implement minimal `substack_format_intro`**

Create `agents-sdk/lib/skill_optimizer/structural_checks.py`:
```python
"""Deterministic structural checks for skill_optimizer eval suite.

Each check returns (passed: bool, reason: str). Cheap, deterministic, free.
"""
from __future__ import annotations

import re
from typing import Tuple

# Sensory nouns watched by the anti-pattern over-reference check.
# These are the words Sean's voice tends to over-use when not pruned.
SENSORY_OVERREFERENCE_NOUNS = (
    "coffee",
    "bathroom",
    "ferry",
    "cursor",
    "terminal",
    "screen",
    "mug",
    "keyboard",
)


def _split_paragraphs(text: str) -> list[str]:
    """Split on blank-line paragraph breaks. Strips each paragraph."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def substack_format_intro(text: str) -> Tuple[bool, str]:
    """Verify Substack-intro shape: first paragraph length, paragraph breaks, closer length."""
    paragraphs = _split_paragraphs(text)
    if len(paragraphs) < 2:
        return False, "must contain at least one paragraph break (got 0)"

    first_wc = _word_count(paragraphs[0])
    if first_wc < 60:
        return False, f"first paragraph too short: {first_wc} words (need 60-180)"
    if first_wc > 180:
        return False, f"first paragraph too long: {first_wc} words (need 60-180)"

    closer = paragraphs[-1]
    # Take the final sentence of the final paragraph as the closer.
    sentences = re.split(r"(?<=[.!?])\s+", closer)
    closer_sentence = sentences[-1].strip() if sentences else closer
    closer_wc = _word_count(closer_sentence)
    if closer_wc > 12:
        return False, f"closer too long: {closer_wc} words (Sean closer pattern is ≤12)"

    return True, "ok"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_structural_checks.py::TestSubstackFormatIntro -v`
Expected: 5 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/structural_checks.py agents-sdk/tests/test_structural_checks.py
git commit -m "feat(structural_checks): substack_format_intro with paragraph + closer rules"
```

---

### Task 1.2: `structural_checks.anti_pattern_overreference`

**Files:**
- Modify: `agents-sdk/lib/skill_optimizer/structural_checks.py`
- Modify: `agents-sdk/tests/test_structural_checks.py`

- [ ] **Step 1: Write the failing test (append to test file)**

Add to `agents-sdk/tests/test_structural_checks.py`:
```python
from agents_sdk.lib.skill_optimizer.structural_checks import (
    anti_pattern_overreference,
)


class TestAntiPatternOverreference:
    def test_passes_when_no_noun_overused(self):
        text = (
            "I sat down with my coffee and stared at the screen.\n\n"
            "The terminal blinked back at me.\n\n"
            "It was a Tuesday."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is True, reason

    def test_fails_when_coffee_appears_three_times(self):
        text = (
            "I made coffee. Then more coffee. Then I drank the coffee.\n\n"
            "End scene."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is False
        assert "coffee" in reason.lower()

    def test_passes_with_callback_pattern(self):
        # Opening word and closing callback may legitimately re-use an image.
        # The function should allow up to 2 instances; 2 instances pass.
        text = (
            "The ferry horn cut through the morning fog.\n\n"
            "Twelve paragraphs later, we are back to where we started.\n\n"
            "The ferry horn sounds the same as it always did."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is True

    def test_case_insensitive(self):
        text = "Coffee and COFFEE and coffee."
        passed, reason = anti_pattern_overreference(text)
        assert passed is False
```

- [ ] **Step 2: Run tests to verify they fail (function not defined)**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_structural_checks.py::TestAntiPatternOverreference -v`
Expected: FAIL with `ImportError: cannot import name 'anti_pattern_overreference'`

- [ ] **Step 3: Implement `anti_pattern_overreference`**

Append to `agents-sdk/lib/skill_optimizer/structural_checks.py`:
```python
def anti_pattern_overreference(text: str) -> Tuple[bool, str]:
    """Fail if any watched sensory noun appears more than 2 times (case-insensitive).

    Two instances are allowed because a callback closer (returning to an opening
    image, transformed) is a documented Sean signature move. Three or more is
    the anti-pattern Sean called "Bad Sean" — falling in love with your own material.
    """
    lower = text.lower()
    for noun in SENSORY_OVERREFERENCE_NOUNS:
        # Word-boundary count to avoid false matches inside other words.
        count = len(re.findall(rf"\b{re.escape(noun)}\b", lower))
        if count > 2:
            return False, f"{noun!r} appears {count} times (max 2)"
    return True, "ok"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_structural_checks.py -v`
Expected: 9 PASS (5 from Task 1.1 + 4 new)

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/structural_checks.py agents-sdk/tests/test_structural_checks.py
git commit -m "feat(structural_checks): anti_pattern_overreference for sensory noun overuse"
```

---

### Task 1.3: `stylometry.extract_features` (sentence length, comma density, em-dash density, first-person frequency)

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/stylometry.py`
- Test: `agents-sdk/tests/test_stylometry.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_stylometry.py`:
```python
"""Tests for stylometry module."""
import math
import pytest
from agents_sdk.lib.skill_optimizer.stylometry import extract_features


class TestExtractFeatures:
    def test_returns_expected_keys(self):
        text = "Hello world. This is a test."
        features = extract_features(text)
        assert set(features.keys()) == {
            "sentence_length_mean",
            "sentence_length_stdev",
            "comma_density_per_100w",
            "em_dash_density_per_100w",
            "first_person_freq_per_100w",
        }

    def test_sentence_length_mean(self):
        text = "One two three. Four five six."
        features = extract_features(text)
        assert features["sentence_length_mean"] == pytest.approx(3.0)

    def test_comma_density(self):
        # 4 commas in 20 words → 20.0 per 100w
        text = "a, b, c, d e f g h i j k l m n o p q r s t."
        features = extract_features(text)
        assert features["comma_density_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_em_dash_density(self):
        # 2 em dashes in 10 words → 20.0 per 100w
        text = "one two — three four — five six seven eight nine ten."
        features = extract_features(text)
        assert features["em_dash_density_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_first_person_freq(self):
        # "I" appears twice in 10 words → 20.0 per 100w
        text = "I went and I came back home for dinner tonight."
        features = extract_features(text)
        assert features["first_person_freq_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_handles_empty_string(self):
        features = extract_features("")
        assert features["sentence_length_mean"] == 0.0
        assert features["comma_density_per_100w"] == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `extract_features`**

Create `agents-sdk/lib/skill_optimizer/stylometry.py`:
```python
"""Stylometric feature extraction + n-gram extraction + distance computation.

Used as a deterministic anti-Goodhart anchor in the eval suite. Detects whether
the optimizer is producing prose with Sean's actual statistical fingerprint
(sentence rhythm, punctuation density, n-gram match) vs. surface-imitation prose.
"""
from __future__ import annotations

import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable

# Em dash unicode + ASCII-double-dash are both treated as em dashes.
EM_DASH_PATTERNS = (r"—", r"--")

FIRST_PERSON_TOKENS = {"i", "me", "my", "mine", "myself"}


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def extract_features(text: str) -> dict[str, float]:
    """Compute the five stylometric features used by the eval suite."""
    words = _word_count(text)
    if words == 0:
        return {
            "sentence_length_mean": 0.0,
            "sentence_length_stdev": 0.0,
            "comma_density_per_100w": 0.0,
            "em_dash_density_per_100w": 0.0,
            "first_person_freq_per_100w": 0.0,
        }

    sentences = _split_sentences(text)
    sentence_lengths = [_word_count(s) for s in sentences if _word_count(s) > 0]
    mean_len = statistics.mean(sentence_lengths) if sentence_lengths else 0.0
    stdev_len = (
        statistics.stdev(sentence_lengths)
        if len(sentence_lengths) >= 2
        else 0.0
    )

    comma_count = text.count(",")
    em_dash_count = sum(len(re.findall(p, text)) for p in EM_DASH_PATTERNS)

    lower_words = re.findall(r"\b\w+\b", text.lower())
    fp_count = sum(1 for w in lower_words if w in FIRST_PERSON_TOKENS)

    return {
        "sentence_length_mean": float(mean_len),
        "sentence_length_stdev": float(stdev_len),
        "comma_density_per_100w": comma_count / words * 100.0,
        "em_dash_density_per_100w": em_dash_count / words * 100.0,
        "first_person_freq_per_100w": fp_count / words * 100.0,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py::TestExtractFeatures -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/stylometry.py agents-sdk/tests/test_stylometry.py
git commit -m "feat(stylometry): extract_features for sentence/comma/em-dash/first-person stats"
```

---

### Task 1.4: `stylometry.extract_ngrams` (top-N distinctive n-grams from corpus)

**Files:**
- Modify: `agents-sdk/lib/skill_optimizer/stylometry.py`
- Modify: `agents-sdk/tests/test_stylometry.py`

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_stylometry.py`:
```python
from agents_sdk.lib.skill_optimizer.stylometry import extract_distinctive_ngrams


class TestExtractDistinctiveNgrams:
    def test_returns_top_n_results(self):
        target = "the kind of thing that happens on a Tuesday and we never talk about it"
        baseline = "the the the the the the the the the the"
        ngrams = extract_distinctive_ngrams(target, [baseline], top_n=5, ns=(2, 3))
        assert len(ngrams) <= 5

    def test_returns_target_specific_ngrams(self):
        target = "kind of thing kind of thing kind of thing"
        baseline = "the dog ran fast and the cat slept slowly in the sun"
        ngrams = extract_distinctive_ngrams(target, [baseline], top_n=10, ns=(2, 3))
        # "kind of" should appear in the distinctive set
        ngram_strings = [" ".join(ng) for ng in ngrams]
        assert any("kind of" in s for s in ngram_strings)

    def test_handles_empty_target(self):
        ngrams = extract_distinctive_ngrams("", ["any baseline"], top_n=5, ns=(2,))
        assert ngrams == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py::TestExtractDistinctiveNgrams -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement `extract_distinctive_ngrams`**

Append to `agents-sdk/lib/skill_optimizer/stylometry.py`:
```python
def _tokenize_lower(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def _ngrams(tokens: list[str], n: int) -> Iterable[tuple[str, ...]]:
    return (tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))


def extract_distinctive_ngrams(
    target_corpus: str,
    baseline_corpora: list[str],
    top_n: int = 30,
    ns: tuple[int, ...] = (2, 3, 4),
) -> list[tuple[str, ...]]:
    """Extract n-grams over-represented in target vs. baseline.

    Distinctiveness = log( (target_freq + smoothing) / (baseline_freq + smoothing) ).
    Returns top_n n-grams sorted by distinctiveness, descending.
    """
    target_tokens = _tokenize_lower(target_corpus)
    if not target_tokens:
        return []

    target_counts: Counter[tuple[str, ...]] = Counter()
    for n in ns:
        target_counts.update(_ngrams(target_tokens, n))

    baseline_counts: Counter[tuple[str, ...]] = Counter()
    baseline_total = 0
    for corpus in baseline_corpora:
        tokens = _tokenize_lower(corpus)
        baseline_total += len(tokens)
        for n in ns:
            baseline_counts.update(_ngrams(tokens, n))

    target_total = len(target_tokens)
    smoothing = 1e-6

    scored = []
    for ngram, t_count in target_counts.items():
        if t_count < 2:  # require ≥2 in target to filter noise
            continue
        t_freq = t_count / target_total
        b_freq = (baseline_counts.get(ngram, 0) + smoothing) / (baseline_total + smoothing)
        score = t_freq / b_freq
        scored.append((score, ngram))

    scored.sort(reverse=True)
    return [ng for _, ng in scored[:top_n]]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py -v`
Expected: 9 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/stylometry.py agents-sdk/tests/test_stylometry.py
git commit -m "feat(stylometry): extract_distinctive_ngrams for n-gram fingerprint"
```

---

### Task 1.5: `stylometry.compute_distance` + `stylometric_distance_check`

**Files:**
- Modify: `agents-sdk/lib/skill_optimizer/stylometry.py`
- Modify: `agents-sdk/lib/skill_optimizer/structural_checks.py`
- Modify: `agents-sdk/tests/test_stylometry.py`
- Modify: `agents-sdk/tests/test_structural_checks.py`

- [ ] **Step 1: Write failing test for `compute_distance`**

Append to `agents-sdk/tests/test_stylometry.py`:
```python
from agents_sdk.lib.skill_optimizer.stylometry import compute_distance


class TestComputeDistance:
    def test_zero_distance_when_identical(self):
        baseline = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
            "_stdevs": {  # required for z-score
                "sentence_length_mean": 1.0,
                "sentence_length_stdev": 0.5,
                "comma_density_per_100w": 1.0,
                "em_dash_density_per_100w": 0.3,
                "first_person_freq_per_100w": 0.5,
            },
            "_ngrams": [],
        }
        target_features = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
        }
        d = compute_distance(target_features, baseline, target_text="hello")
        assert d == pytest.approx(0.0, abs=0.5)  # may include n-gram component

    def test_increases_with_feature_divergence(self):
        baseline = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
            "_stdevs": {
                "sentence_length_mean": 1.0,
                "sentence_length_stdev": 0.5,
                "comma_density_per_100w": 1.0,
                "em_dash_density_per_100w": 0.3,
                "first_person_freq_per_100w": 0.5,
            },
            "_ngrams": [],
        }
        close = {"sentence_length_mean": 10.5, "sentence_length_stdev": 2.0,
                 "comma_density_per_100w": 5.0, "em_dash_density_per_100w": 1.0,
                 "first_person_freq_per_100w": 3.0}
        far = {"sentence_length_mean": 25.0, "sentence_length_stdev": 8.0,
               "comma_density_per_100w": 0.5, "em_dash_density_per_100w": 0.0,
               "first_person_freq_per_100w": 0.5}
        d_close = compute_distance(close, baseline, target_text="x")
        d_far = compute_distance(far, baseline, target_text="x")
        assert d_far > d_close
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py::TestComputeDistance -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement `compute_distance` and the baseline-loader helpers**

Append to `agents-sdk/lib/skill_optimizer/stylometry.py`:
```python
def compute_distance(
    target_features: dict[str, float],
    baseline: dict,
    target_text: str,
) -> float:
    """Compute total absolute z-score distance + n-gram-mismatch penalty.

    Lower = closer to Sean's distribution. Pass threshold is calibrated externally
    against a hand-labeled set (15 real Sean / 15 generic AI) at pre-flight time.
    """
    stdevs = baseline.get("_stdevs", {})
    feature_keys = (
        "sentence_length_mean",
        "sentence_length_stdev",
        "comma_density_per_100w",
        "em_dash_density_per_100w",
        "first_person_freq_per_100w",
    )

    z_total = 0.0
    for key in feature_keys:
        std = stdevs.get(key, 1.0) or 1.0
        z = abs(target_features.get(key, 0.0) - baseline.get(key, 0.0)) / std
        z_total += z

    # N-gram component: count target n-grams from baseline._ngrams that appear in target_text.
    baseline_ngrams: list[tuple[str, ...]] = baseline.get("_ngrams", [])
    if baseline_ngrams:
        target_lower = target_text.lower()
        hits = sum(
            1 for ng in baseline_ngrams if " ".join(ng) in target_lower
        )
        # Penalty rises as match rate falls. 0 hits → +5.0, all hits → +0.
        match_rate = hits / max(len(baseline_ngrams), 1)
        z_total += 5.0 * (1.0 - match_rate)

    return z_total


def load_baseline(path: Path | str) -> dict:
    """Load stylometry baseline JSON. Raises FileNotFoundError if missing."""
    with open(path, "r") as f:
        return json.load(f)


def save_baseline(baseline: dict, path: Path | str) -> None:
    with open(path, "w") as f:
        json.dump(baseline, f, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else x)
```

- [ ] **Step 4: Add the structural-check wrapper**

Append to `agents-sdk/lib/skill_optimizer/structural_checks.py`:
```python
def stylometric_distance(
    text: str,
    baseline: dict,
    threshold: float,
) -> Tuple[bool, str]:
    """Pass if stylometric distance to Sean's baseline is below threshold.

    Threshold is calibrated at pre-flight time against a hand-labeled set
    (15 real Sean / 15 generic AI) to maximize ROC AUC. Stored in baseline JSON.
    """
    from agents_sdk.lib.skill_optimizer.stylometry import (
        compute_distance,
        extract_features,
    )

    features = extract_features(text)
    distance = compute_distance(features, baseline, target_text=text)
    if distance > threshold:
        return False, f"stylometric distance {distance:.2f} > threshold {threshold:.2f}"
    return True, f"distance {distance:.2f} ≤ threshold {threshold:.2f}"
```

- [ ] **Step 5: Add a structural-check test for the wrapper**

Append to `agents-sdk/tests/test_structural_checks.py`:
```python
from agents_sdk.lib.skill_optimizer.structural_checks import stylometric_distance


class TestStylometricDistance:
    def _baseline(self) -> dict:
        return {
            "sentence_length_mean": 12.0,
            "sentence_length_stdev": 5.0,
            "comma_density_per_100w": 7.0,
            "em_dash_density_per_100w": 2.0,
            "first_person_freq_per_100w": 5.0,
            "_stdevs": {
                "sentence_length_mean": 2.0,
                "sentence_length_stdev": 1.0,
                "comma_density_per_100w": 1.5,
                "em_dash_density_per_100w": 0.5,
                "first_person_freq_per_100w": 1.0,
            },
            "_ngrams": [],
        }

    def test_passes_when_close_to_baseline(self):
        text = "I went, and I came back, and the day was long. I drank coffee."
        passed, _ = stylometric_distance(text, self._baseline(), threshold=20.0)
        assert passed is True

    def test_fails_when_far_from_baseline(self):
        text = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do."
        passed, reason = stylometric_distance(text, self._baseline(), threshold=2.0)
        assert passed is False
        assert "threshold" in reason
```

- [ ] **Step 6: Run all tests**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_stylometry.py tests/test_structural_checks.py -v`
Expected: all PASS (≥13 tests)

- [ ] **Step 7: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/ agents-sdk/tests/test_stylometry.py agents-sdk/tests/test_structural_checks.py
git commit -m "feat(stylometry): compute_distance + stylometric_distance check"
```

---

### Task 1.6: `mutation_guard` (diff parser, protected ranges, anti-gaming)

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/mutation_guard.py`
- Test: `agents-sdk/tests/test_mutation_guard.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_mutation_guard.py`:
```python
"""Tests for mutation_guard module."""
import pytest
from agents_sdk.lib.skill_optimizer.mutation_guard import (
    validate_mutation,
    MutationRejected,
)

PROTECTED_LINE_RANGES = [(1, 4), (23, 69)]
PROTECTED_SECTION_HEADINGS = ("References", "Related Skills", "Copy/Paste Ready")
CRITERION_IDS = (
    "substack_format_intro",
    "anti_pattern_overreference",
    "stylometric_distance",
    "signature_move_present",
    "sounds_like_sean",
    "no_anti_pattern_violation",
)


class TestValidateMutation:
    def test_accepts_valid_single_section_edit(self):
        original = "## Section A\nold body line one\nold body line two\n## Section B\nbody\n"
        modified = "## Section A\nnew body line one with substantive change here\nnew body line two as well now\n## Section B\nbody\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[(1, 0)],  # no protected lines for this test
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert ok, reason

    def test_rejects_change_to_protected_lines(self):
        original = ["line 1\n", "line 2\n", "line 3\n", "line 4\n", "line 5\n"]
        modified = ["line 1 EDITED\n", "line 2\n", "line 3\n", "line 4\n", "line 5\n"]
        ok, reason = validate_mutation(
            original_lines=original,
            modified_lines=modified,
            protected_line_ranges=[(1, 4)],
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert not ok
        assert "protected line range" in reason.lower()

    def test_rejects_change_under_protected_section(self):
        original = "## Section A\nbody\n## References\noriginal refs\n"
        modified = "## Section A\nbody\n## References\nedited refs body now\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=("References",),
            criterion_ids=(),
        )
        assert not ok
        assert "protected section" in reason.lower()

    def test_rejects_whitespace_only_diff(self):
        original = "## Section A\nline one\n"
        modified = "## Section A\nline one  \n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert not ok
        assert "whitespace" in reason.lower()

    def test_rejects_heading_matching_criterion_id(self):
        original = "## Old Heading\nbody line one\n"
        modified = "## sounds_like_sean\nbody line one\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=(),
            criterion_ids=("sounds_like_sean",),
        )
        assert not ok
        assert "criterion id" in reason.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_mutation_guard.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `mutation_guard`**

Create `agents-sdk/lib/skill_optimizer/mutation_guard.py`:
```python
"""Mutation guard — pre-write diff validator for skill_optimizer.

Enforces autoresearch hard constraints + per-iteration mutation policy:
  * No edits to protected line ranges (frontmatter, example outputs)
  * No edits to protected section headings (References, Related Skills, etc.)
  * No whitespace-only diffs (gaming the iteration counter)
  * No headings introduced that match a criterion ID verbatim (anti-gaming)
"""
from __future__ import annotations

import difflib
import re
from typing import Iterable, Sequence


class MutationRejected(Exception):
    """Raised when a proposed mutation violates policy."""


def _stripped_diff(orig: Sequence[str], mod: Sequence[str]) -> list[tuple[str, int, int, str, str]]:
    """Return non-equal opcodes from SequenceMatcher: (op, i1, i2, orig_chunk, mod_chunk)."""
    matcher = difflib.SequenceMatcher(a=orig, b=mod, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        out.append((op, i1, i2, "".join(orig[i1:i2]), "".join(mod[j1:j2])))
    return out


def _line_in_any_range(line_num: int, ranges: Iterable[tuple[int, int]]) -> bool:
    """1-indexed line number; ranges are inclusive."""
    return any(lo <= line_num <= hi for (lo, hi) in ranges if hi >= lo)


def _section_for_line(lines: Sequence[str], line_num: int) -> str | None:
    """Walk back from line_num (1-indexed) to find the most recent ## or ### heading."""
    heading_re = re.compile(r"^#{2,4}\s+(.*?)\s*$")
    for i in range(min(line_num - 1, len(lines) - 1), -1, -1):
        m = heading_re.match(lines[i])
        if m:
            return m.group(1).strip()
    return None


def validate_mutation(
    original_lines: Sequence[str],
    modified_lines: Sequence[str],
    protected_line_ranges: list[tuple[int, int]],
    protected_section_headings: tuple[str, ...],
    criterion_ids: tuple[str, ...],
) -> tuple[bool, str]:
    """Return (passed, reason). passed=True means the mutation is allowed."""
    if original_lines == modified_lines:
        return False, "diff is empty (no changes)"

    # Whitespace-only check: compare with whitespace stripped.
    orig_stripped = "".join(original_lines).replace(" ", "").replace("\t", "")
    mod_stripped = "".join(modified_lines).replace(" ", "").replace("\t", "")
    if orig_stripped == mod_stripped:
        return False, "whitespace-only diff (rejected as gaming the iteration counter)"

    diff_ops = _stripped_diff(original_lines, modified_lines)
    if not diff_ops:
        return False, "diff is empty after normalization"

    # Check each changed hunk for protected-range violations.
    for op, i1, i2, orig_chunk, mod_chunk in diff_ops:
        for line_num_zero in range(i1, max(i1 + 1, i2)):
            line_num = line_num_zero + 1  # 1-indexed
            if _line_in_any_range(line_num, protected_line_ranges):
                return False, f"diff touches protected line range (line {line_num})"
            section = _section_for_line(original_lines, line_num)
            if section and section in protected_section_headings:
                return False, f"diff touches protected section {section!r}"

    # Anti-gaming: any new heading whose text matches a criterion ID verbatim?
    new_headings = re.findall(r"^#{2,4}\s+(.*?)\s*$", "".join(modified_lines), re.MULTILINE)
    old_headings = set(re.findall(r"^#{2,4}\s+(.*?)\s*$", "".join(original_lines), re.MULTILINE))
    introduced = [h for h in new_headings if h not in old_headings]
    for h in introduced:
        if h.strip() in criterion_ids:
            return False, f"introduced heading {h!r} matches criterion id (anti-gaming guard)"

    return True, "ok"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_mutation_guard.py -v`
Expected: 5 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/mutation_guard.py agents-sdk/tests/test_mutation_guard.py
git commit -m "feat(mutation_guard): pre-write diff validator with anti-gaming heuristics"
```

---

### Task 1.7: `decision` module (moving avg, bootstrap CI keep/revert)

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/decision.py`
- Test: `agents-sdk/tests/test_decision.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_decision.py`:
```python
"""Tests for decision module."""
import random
import pytest
from agents_sdk.lib.skill_optimizer.decision import (
    moving_average,
    bootstrap_ci,
    keep_or_revert,
)


class TestMovingAverage:
    def test_short_window(self):
        assert moving_average([0.5], window=3) == 0.5

    def test_partial_window(self):
        assert moving_average([0.5, 0.7], window=3) == pytest.approx(0.6)

    def test_full_window(self):
        result = moving_average([0.4, 0.5, 0.6, 0.7], window=3)
        assert result == pytest.approx((0.5 + 0.6 + 0.7) / 3)


class TestBootstrapCI:
    def test_returns_lower_and_upper(self):
        random.seed(42)
        binary = [1] * 80 + [0] * 20  # 80% pass rate
        lo, hi = bootstrap_ci(binary, n_resamples=500, ci=0.95)
        assert 0.7 < lo < 0.85
        assert 0.75 < hi < 0.9
        assert lo < hi

    def test_zero_data_returns_zero_zero(self):
        lo, hi = bootstrap_ci([], n_resamples=100, ci=0.95)
        assert lo == 0.0 and hi == 0.0


class TestKeepOrRevert:
    def test_keeps_when_ci_clearly_positive(self):
        random.seed(42)
        # current iteration scored 90% across 350 trials, prior best was 70%.
        current = [1] * 315 + [0] * 35
        best = [1] * 245 + [0] * 105
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "keep"

    def test_reverts_when_no_clear_improvement(self):
        random.seed(42)
        current = [1] * 250 + [0] * 100
        best = [1] * 250 + [0] * 100
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "revert"

    def test_reverts_when_current_worse(self):
        random.seed(42)
        current = [1] * 200 + [0] * 150
        best = [1] * 280 + [0] * 70
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "revert"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_decision.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `decision`**

Create `agents-sdk/lib/skill_optimizer/decision.py`:
```python
"""Decision module — moving average + bootstrap CI for keep/revert.

Per the autoresearch design (Section 8.1 of the spec): only the training-set
score drives keep/revert decisions. Holdout score is for trip-wires; surprise
score is reported but not part of the decision rule.
"""
from __future__ import annotations

import random
import statistics
from typing import Sequence


def moving_average(values: Sequence[float], window: int = 3) -> float:
    """Mean of the most recent `window` values. If fewer than `window` exist, mean of all."""
    if not values:
        return 0.0
    tail = list(values)[-window:]
    return statistics.mean(tail)


def bootstrap_ci(
    binary_outcomes: Sequence[int],
    n_resamples: int = 1000,
    ci: float = 0.95,
) -> tuple[float, float]:
    """Bootstrap CI for the mean of a binary 0/1 outcome array.

    Returns (lower, upper) of the (1-ci)/2 and (1+ci)/2 percentile of the resample means.
    """
    if not binary_outcomes:
        return 0.0, 0.0
    means = []
    n = len(binary_outcomes)
    for _ in range(n_resamples):
        sample = [binary_outcomes[random.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int(((1 - ci) / 2) * n_resamples)
    hi_idx = int(((1 + ci) / 2) * n_resamples) - 1
    return means[lo_idx], means[hi_idx]


def keep_or_revert(
    current_outcomes: Sequence[int],
    best_outcomes: Sequence[int],
    n_resamples: int = 1000,
    ci: float = 0.95,
) -> tuple[str, dict]:
    """Decide keep vs revert based on bootstrap CI of (current - best) > 0.

    Returns ('keep' | 'revert', info dict with lo/hi/delta).
    """
    if not current_outcomes:
        return "revert", {"reason": "no current outcomes"}

    # Bootstrap the difference distribution by resampling each independently.
    n_cur = len(current_outcomes)
    n_best = len(best_outcomes) if best_outcomes else 0
    deltas = []
    for _ in range(n_resamples):
        cur_mean = sum(current_outcomes[random.randrange(n_cur)] for _ in range(n_cur)) / n_cur
        if n_best > 0:
            best_mean = sum(best_outcomes[random.randrange(n_best)] for _ in range(n_best)) / n_best
        else:
            best_mean = 0.0
        deltas.append(cur_mean - best_mean)
    deltas.sort()
    lo_idx = int(((1 - ci) / 2) * n_resamples)
    hi_idx = int(((1 + ci) / 2) * n_resamples) - 1
    lo, hi = deltas[lo_idx], deltas[hi_idx]
    info = {"delta_lo": lo, "delta_hi": hi, "delta_mean": statistics.mean(deltas)}
    decision = "keep" if lo > 0 else "revert"
    return decision, info
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_decision.py -v`
Expected: 8 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/decision.py agents-sdk/tests/test_decision.py
git commit -m "feat(decision): moving_average + bootstrap_ci + keep_or_revert"
```

---

### Task 1.8: `tripwire` module (6 trip-wire checks)

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/tripwire.py`
- Test: `agents-sdk/tests/test_tripwire.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_tripwire.py`:
```python
"""Tests for tripwire module."""
import pytest
from agents_sdk.lib.skill_optimizer.tripwire import (
    check_all_tripwires,
    IterationSnapshot,
)


def _snap(**kwargs) -> IterationSnapshot:
    defaults = dict(
        iteration=5,
        train_score=0.75,
        holdout_score=0.70,
        prior_holdout_scores=[0.72, 0.71, 0.70],
        criterion_scores={
            "substack_format_intro": 0.80,
            "anti_pattern_overreference": 0.85,
            "stylometric_distance": 0.78,
            "signature_move_present": 0.75,
            "sounds_like_sean": 0.70,
            "no_anti_pattern_violation": 0.75,
        },
        criterion_scores_iter1={
            "substack_format_intro": 0.75,
            "anti_pattern_overreference": 0.80,
            "stylometric_distance": 0.70,
            "signature_move_present": 0.70,
            "sounds_like_sean": 0.65,
            "no_anti_pattern_violation": 0.70,
        },
        stylometric_score=0.78,
        stylometric_score_baseline=0.70,
        llm_judge_score=0.73,
        llm_judge_score_baseline=0.68,
        avg_inter_run_similarity=0.45,
        avg_inter_run_similarity_baseline=0.40,
        sonnet_qwen_agreement=0.85,
        skill_md_token_count=2500,
        skill_md_token_count_baseline=2000,
        score_gain_vs_baseline=0.10,
    )
    defaults.update(kwargs)
    return IterationSnapshot(**defaults)


class TestTripwires:
    def test_no_tripwires_on_healthy_iteration(self):
        triggered = check_all_tripwires(_snap())
        assert triggered == []

    def test_train_holdout_divergence(self):
        snap = _snap(prior_holdout_scores=[0.78, 0.76, 0.72], holdout_score=0.65)
        # Drop = 0.78 - 0.65 = 0.13 over 3 iters → triggers >5pp threshold
        triggered = check_all_tripwires(snap)
        assert "train_holdout_divergence" in triggered

    def test_complexity_ratchet(self):
        snap = _snap(skill_md_token_count=3500, skill_md_token_count_baseline=2000, score_gain_vs_baseline=0.02)
        # 75% growth, 2% gain → triggers
        triggered = check_all_tripwires(snap)
        assert "complexity_ratchet" in triggered

    def test_diversity_collapse(self):
        snap = _snap(avg_inter_run_similarity=0.65, avg_inter_run_similarity_baseline=0.40)
        triggered = check_all_tripwires(snap)
        assert "diversity_collapse" in triggered

    def test_judge_disagreement(self):
        snap = _snap(sonnet_qwen_agreement=0.65)
        triggered = check_all_tripwires(snap)
        assert "judge_disagreement" in triggered

    def test_stylometric_drift(self):
        snap = _snap(stylometric_score=0.55, stylometric_score_baseline=0.75, llm_judge_score=0.80, llm_judge_score_baseline=0.65)
        triggered = check_all_tripwires(snap)
        assert "stylometric_drift" in triggered
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_tripwire.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `tripwire`**

Create `agents-sdk/lib/skill_optimizer/tripwire.py`:
```python
"""Tripwire module — six anti-Goodhart safety checks per the autoresearch design.

See Section 8.2 of the spec. Trip-wires are LOG-ONLY for iterations 1-3
(calibration phase) and HALT from iteration 4 onward — that policy is enforced
by the orchestrator, not this module.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field


@dataclass
class IterationSnapshot:
    """Everything a tripwire check might need from one iteration."""
    iteration: int
    train_score: float
    holdout_score: float
    prior_holdout_scores: list[float]  # last 3 holdout scores (most recent last)
    criterion_scores: dict[str, float]
    criterion_scores_iter1: dict[str, float]
    stylometric_score: float
    stylometric_score_baseline: float  # iter 1 stylometric score
    llm_judge_score: float
    llm_judge_score_baseline: float  # iter 1 LLM-judge avg
    avg_inter_run_similarity: float
    avg_inter_run_similarity_baseline: float  # iter 1
    sonnet_qwen_agreement: float
    skill_md_token_count: int
    skill_md_token_count_baseline: int  # iter 1
    score_gain_vs_baseline: float  # train_score - iter1.train_score


# Threshold constants — tunable via spec Section 8.2.
TRAIN_HOLDOUT_DIVERGENCE_PP = 0.05  # 5pp
CRITERION_DRIFT_RATIO = 1.5
STYLOMETRIC_DROP_PCT = 0.15
DIVERSITY_RISE_PCT = 0.20
JUDGE_AGREEMENT_FLOOR = 0.70
COMPLEXITY_TOKEN_GROWTH_PCT = 0.50
COMPLEXITY_MIN_SCORE_GAIN = 0.05


def _train_holdout_divergence(s: IterationSnapshot) -> bool:
    if len(s.prior_holdout_scores) < 1:
        return False
    earliest = max(s.prior_holdout_scores)
    return (earliest - s.holdout_score) > TRAIN_HOLDOUT_DIVERGENCE_PP


def _criterion_uneven_drift(s: IterationSnapshot) -> bool:
    if not s.criterion_scores_iter1:
        return False
    ratios = []
    for k, baseline in s.criterion_scores_iter1.items():
        if baseline == 0:
            continue
        current = s.criterion_scores.get(k, 0.0)
        ratios.append(current / baseline)
    if len(ratios) < 2:
        return False
    median = statistics.median(ratios)
    return any(r / median > CRITERION_DRIFT_RATIO for r in ratios)


def _stylometric_drift(s: IterationSnapshot) -> bool:
    if s.stylometric_score_baseline == 0:
        return False
    drop = (s.stylometric_score_baseline - s.stylometric_score) / s.stylometric_score_baseline
    llm_rising = s.llm_judge_score > s.llm_judge_score_baseline
    return drop > STYLOMETRIC_DROP_PCT and llm_rising


def _diversity_collapse(s: IterationSnapshot) -> bool:
    if s.avg_inter_run_similarity_baseline == 0:
        return False
    rise = (s.avg_inter_run_similarity - s.avg_inter_run_similarity_baseline) / s.avg_inter_run_similarity_baseline
    return rise > DIVERSITY_RISE_PCT


def _judge_disagreement(s: IterationSnapshot) -> bool:
    return s.sonnet_qwen_agreement < JUDGE_AGREEMENT_FLOOR


def _complexity_ratchet(s: IterationSnapshot) -> bool:
    if s.skill_md_token_count_baseline == 0:
        return False
    growth = (s.skill_md_token_count - s.skill_md_token_count_baseline) / s.skill_md_token_count_baseline
    return growth > COMPLEXITY_TOKEN_GROWTH_PCT and s.score_gain_vs_baseline < COMPLEXITY_MIN_SCORE_GAIN


TRIPWIRES = {
    "train_holdout_divergence": _train_holdout_divergence,
    "criterion_uneven_drift": _criterion_uneven_drift,
    "stylometric_drift": _stylometric_drift,
    "diversity_collapse": _diversity_collapse,
    "judge_disagreement": _judge_disagreement,
    "complexity_ratchet": _complexity_ratchet,
}


def check_all_tripwires(snap: IterationSnapshot) -> list[str]:
    """Return the names of any triggered tripwires."""
    return [name for name, fn in TRIPWIRES.items() if fn(snap)]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_tripwire.py -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/tripwire.py agents-sdk/tests/test_tripwire.py
git commit -m "feat(tripwire): six anti-Goodhart trip-wire checks"
```

---

> **Pause point: Phase 1 complete.** Run `cd agents-sdk && PYTHONPATH=. pytest tests/test_structural_checks.py tests/test_stylometry.py tests/test_mutation_guard.py tests/test_decision.py tests/test_tripwire.py -v` — all should PASS. ~36 unit tests. No external dependencies hit yet.

---

## Phase 2 — LLM-Judge Runner

The judge runner has external dependencies (Ollama for Qwen3-14B, Anthropic SDK for Sonnet sample-checks). All external calls are wrapped behind dependency-injected client objects so unit tests can mock them.

### Task 2.1: `judge_runner` — single judge call against Qwen via Ollama

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/judge_runner.py`
- Test: `agents-sdk/tests/test_judge_runner.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_judge_runner.py`:
```python
"""Tests for judge_runner module."""
import pytest
from unittest.mock import MagicMock
from agents_sdk.lib.skill_optimizer.judge_runner import (
    JudgeRunner,
    JudgeResult,
)


PROMPT_TEMPLATE = """You are evaluating a Substack blog post intro against ONE binary criterion.

OUTPUT TO EVALUATE:
{output}

ANCHOR SAMPLES:

Sample 1:
{anchor_1}

Sample 2:
{anchor_2}

CRITERION:
{question}

Answer YES or NO on the last line.
"""


class TestSingleJudgeCall:
    def test_returns_yes_when_model_says_yes(self):
        client = MagicMock()
        client.complete.return_value = "It does match.\nYES"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="some output",
            anchors=["anchor a", "anchor b"],
            question="does it match?",
            mode="sean",
        )
        assert result.passed is True
        assert result.raw_response == "It does match.\nYES"

    def test_returns_no_when_model_says_no(self):
        client = MagicMock()
        client.complete.return_value = "Reasoning here.\nNO"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="x", anchors=["a", "b"], question="?", mode="sean"
        )
        assert result.passed is False

    def test_treats_ambiguous_response_as_failure(self):
        client = MagicMock()
        client.complete.return_value = "Maybe.\nUNCLEAR"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="x", anchors=["a", "b"], question="?", mode="sean"
        )
        assert result.passed is False
        assert "ambiguous" in result.reason.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement single-judge runner**

Create `agents-sdk/lib/skill_optimizer/judge_runner.py`:
```python
"""LLM-judge runner — wraps Qwen3-14B (local Ollama) and Sonnet 4.6 (sample-check).

Ensemble strategy (per spec Section 4.2): single-judge for `signature_move_present`,
3-judge majority vote for `sounds_like_sean` and `no_anti_pattern_violation`.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional, Protocol


class _LLMClient(Protocol):
    def complete(self, prompt: str, model: str = ..., temperature: float = ..., seed: int = ...) -> str: ...


@dataclass
class JudgeResult:
    passed: bool
    raw_response: str
    reason: str


@dataclass
class EnsembleResult:
    passed: bool  # majority decision
    individual_results: list[JudgeResult]
    yes_count: int
    no_count: int


class JudgeRunner:
    def __init__(
        self,
        local_client: _LLMClient,
        sonnet_client: Optional[_LLMClient],
        prompt_template: str,
    ):
        self.local = local_client
        self.sonnet = sonnet_client
        self.template = prompt_template

    @staticmethod
    def _parse_yes_no(response: str) -> tuple[bool | None, str]:
        last_line = response.strip().splitlines()[-1].strip().upper() if response.strip() else ""
        if last_line == "YES":
            return True, "yes"
        if last_line == "NO":
            return False, "no"
        return None, f"ambiguous (last line: {last_line!r})"

    def judge_single(
        self,
        output: str,
        anchors: list[str],
        question: str,
        mode: str,
        use_sonnet: bool = False,
        seed: int = 0,
    ) -> JudgeResult:
        a1 = anchors[0] if len(anchors) >= 1 else ""
        a2 = anchors[1] if len(anchors) >= 2 else ""
        prompt = self.template.format(
            output=output, anchor_1=a1, anchor_2=a2, question=question, mode=mode,
        )
        client = self.sonnet if (use_sonnet and self.sonnet) else self.local
        model = "claude-sonnet-4-6" if (use_sonnet and self.sonnet) else "qwen3-14b-research:latest"
        raw = client.complete(prompt=prompt, model=model, temperature=0.0, seed=seed)
        parsed, reason = self._parse_yes_no(raw)
        if parsed is None:
            return JudgeResult(passed=False, raw_response=raw, reason=reason)
        return JudgeResult(passed=parsed, raw_response=raw, reason=reason)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py -v`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/judge_runner.py agents-sdk/tests/test_judge_runner.py
git commit -m "feat(judge_runner): single-judge Qwen3-14B call with YES/NO parser"
```

---

### Task 2.2: `judge_runner` — 3-judge ensemble with shuffled anchors + seeds

**Files:**
- Modify: `agents-sdk/lib/skill_optimizer/judge_runner.py`
- Modify: `agents-sdk/tests/test_judge_runner.py`

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_judge_runner.py`:
```python
class TestEnsembleJudge:
    def test_majority_yes_passes(self):
        client = MagicMock()
        # Three calls return YES, YES, NO → majority YES.
        client.complete.side_effect = ["...\nYES", "...\nYES", "...\nNO"]
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_ensemble(
            output="x",
            anchors=["a", "b", "c", "d"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        assert result.passed is True
        assert result.yes_count == 2 and result.no_count == 1

    def test_majority_no_fails(self):
        client = MagicMock()
        client.complete.side_effect = ["...\nNO", "...\nNO", "...\nYES"]
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_ensemble(
            output="x",
            anchors=["a", "b", "c", "d"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        assert result.passed is False
        assert result.yes_count == 1 and result.no_count == 2

    def test_uses_different_anchor_orders_per_judge(self):
        client = MagicMock()
        client.complete.side_effect = ["x\nYES"] * 3
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        runner.judge_ensemble(
            output="x",
            anchors=["a1", "a2", "a3", "a4"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        prompts_sent = [call.kwargs["prompt"] for call in client.complete.call_args_list]
        # The three prompts should not all be identical (anchor order differs).
        assert len(set(prompts_sent)) > 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py::TestEnsembleJudge -v`
Expected: FAIL with `AttributeError: 'JudgeRunner' object has no attribute 'judge_ensemble'`

- [ ] **Step 3: Implement `judge_ensemble`**

Append to `agents-sdk/lib/skill_optimizer/judge_runner.py`:
```python
    def judge_ensemble(
        self,
        output: str,
        anchors: list[str],
        question: str,
        mode: str,
        n_judges: int = 3,
        rng_seed: int = 0,
    ) -> EnsembleResult:
        """Run n_judges independent judge calls with shuffled anchor pairs + seeds.

        Anchor pool: caller passes ≥4 anchors. Each judge call samples 2 distinct
        anchors and a different seed.
        """
        if len(anchors) < 2:
            raise ValueError("ensemble judge requires ≥ 2 anchors")
        rng = random.Random(rng_seed)
        results: list[JudgeResult] = []
        for i in range(n_judges):
            pair = rng.sample(anchors, 2)
            r = self.judge_single(
                output=output,
                anchors=pair,
                question=question,
                mode=mode,
                seed=rng.randint(0, 2**32 - 1),
            )
            results.append(r)
        yes_count = sum(1 for r in results if r.passed)
        no_count = n_judges - yes_count
        return EnsembleResult(
            passed=(yes_count > no_count),
            individual_results=results,
            yes_count=yes_count,
            no_count=no_count,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/judge_runner.py agents-sdk/tests/test_judge_runner.py
git commit -m "feat(judge_runner): 3-judge ensemble with shuffled anchors and seeds"
```

---

### Task 2.3: `judge_runner` — Sonnet sample-check + agreement metric

**Files:**
- Modify: `agents-sdk/lib/skill_optimizer/judge_runner.py`
- Modify: `agents-sdk/tests/test_judge_runner.py`

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_judge_runner.py`:
```python
class TestSonnetSampleCheck:
    def test_high_agreement_when_judges_match(self):
        local = MagicMock()
        sonnet = MagicMock()
        # Both return same labels for same outputs.
        local.complete.side_effect = ["...\nYES", "...\nNO", "...\nYES"]
        sonnet.complete.side_effect = ["...\nYES", "...\nNO", "...\nYES"]
        runner = JudgeRunner(local_client=local, sonnet_client=sonnet, prompt_template=PROMPT_TEMPLATE)
        agreement = runner.compute_sonnet_agreement(
            outputs=["o1", "o2", "o3"],
            anchors_per_output=[["a", "b"]] * 3,
            question="?",
            mode="sean",
            local_results=[True, False, True],
        )
        assert agreement == pytest.approx(1.0)

    def test_low_agreement_when_judges_disagree(self):
        local = MagicMock()
        sonnet = MagicMock()
        sonnet.complete.side_effect = ["...\nNO", "...\nYES", "...\nNO"]
        runner = JudgeRunner(local_client=local, sonnet_client=sonnet, prompt_template=PROMPT_TEMPLATE)
        agreement = runner.compute_sonnet_agreement(
            outputs=["o1", "o2", "o3"],
            anchors_per_output=[["a", "b"]] * 3,
            question="?",
            mode="sean",
            local_results=[True, False, True],  # all 3 disagree with sonnet
        )
        assert agreement == pytest.approx(0.0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py::TestSonnetSampleCheck -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Implement `compute_sonnet_agreement`**

Append to `agents-sdk/lib/skill_optimizer/judge_runner.py`:
```python
    def compute_sonnet_agreement(
        self,
        outputs: list[str],
        anchors_per_output: list[list[str]],
        question: str,
        mode: str,
        local_results: list[bool],
    ) -> float:
        """Re-judge a sample with Sonnet 4.6 and return agreement rate vs local_results."""
        if not self.sonnet:
            raise RuntimeError("Sonnet client not configured")
        if len(outputs) != len(local_results):
            raise ValueError("outputs and local_results must align")
        agreements = 0
        for i, (out, anchors) in enumerate(zip(outputs, anchors_per_output)):
            sonnet_r = self.judge_single(
                output=out,
                anchors=anchors,
                question=question,
                mode=mode,
                use_sonnet=True,
                seed=0,
            )
            if sonnet_r.passed == local_results[i]:
                agreements += 1
        return agreements / len(outputs) if outputs else 0.0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_judge_runner.py -v`
Expected: 8 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/judge_runner.py agents-sdk/tests/test_judge_runner.py
git commit -m "feat(judge_runner): Sonnet sample-check with agreement metric"
```

---

> **Pause point: Phase 2 complete.** All lib modules tested with mocked LLM clients. ~44 unit tests. Live LLM calls are first introduced in Phase 4.

---

## Phase 3 — Eval Data + Templates + Baselines

### Task 3.1: `evals.yaml` — training + holdout prompts

**Files:**
- Create: `.claude/skills/writing-voice-modes/evals.yaml`

- [ ] **Step 1: Write the eval YAML**

Create `.claude/skills/writing-voice-modes/evals.yaml`:
```yaml
# Eval suite for writing-voice-modes autoresearch optimization.
# See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md
schema_version: 1

training_prompts:
  - id: sean_quitting_job
    mode: sean
    prompt: "Write a 250-word Substack blog post intro about quitting your day job to bet on AI. Sean Mode, full intensity."
  - id: sedaris_coffee_ritual
    mode: sedaris
    prompt: "Write a 250-word Substack intro in Domestic Observer mode about how your morning coffee ritual changed when you started talking to Claude every day."
  - id: gonzo_broken_deploy
    mode: gonzo
    prompt: "Write a 250-word Substack intro in Gonzo mode about deploying a broken migration to production at 11:47 PM on a Wednesday."
  - id: kerouac_agent_moment
    mode: kerouac
    prompt: "Write a 250-word Substack intro in Beat Flow mode about the moment you understood Claude Code agents — the sensory rush of watching code rewrite itself."
  - id: vonnegut_leaving_loved_job
    mode: vonnegut
    prompt: "Write a 250-word Substack intro in Vonnegut mode about leaving a job you loved for a job that scared you."

holdout_prompts:
  - id: dial_60_slipped_launch
    mode: sean
    dial: 0.60
    prompt: "Write a 250-word Substack intro about a launch that slipped two weeks. Sean Mode, dialed to 60% — appropriate for cross-posting on LinkedIn where former colleagues will read it."
  - id: combo_gonzo_to_vonnegut
    mode: gonzo_to_vonnegut
    prompt: "Write a 250-word Substack intro that opens Gonzo (cold open, mid-action) and lands Vonnegut (flat collision closer). Topic: the day you realized your side project was actually your job."

structural_criteria:
  - id: substack_format_intro
    function: structural_checks.substack_format_intro
  - id: anti_pattern_overreference
    function: structural_checks.anti_pattern_overreference
  - id: stylometric_distance
    function: structural_checks.stylometric_distance
    requires_baseline: true

llm_judge_criteria:
  - id: signature_move_present
    ensemble: false
    question: "Does this output contain at least one signature move from the prescribed mode (e.g., for Sedaris: sentence-end punchline OR mundane→pivot OR cold-description defamiliarization)?"
  - id: sounds_like_sean
    ensemble: true
    n_judges: 3
    question: "Does this output read like a Sean-Winslow-authored Substack intro rather than a generic AI imitation?"
  - id: no_anti_pattern_violation
    ensemble: true
    n_judges: 3
    question: "Is this output free of the prescribed mode's documented anti-patterns (e.g., for Kerouac: NOT 'rambling without a jewel center', NOT 'dashes everywhere with no rhythmic variation')?"

scoring:
  runs_per_prompt: 15
  per_criterion_floor: 0.60
  aggregate_target: 0.75
  iteration_cap: 25
  plateau_halt_iterations: 3
  moving_average_window: 3
  bootstrap_resamples: 1000
  bootstrap_ci: 0.95
```

- [ ] **Step 2: Validate YAML parses**

Run: `python3 -c "import yaml; print(yaml.safe_load(open('.claude/skills/writing-voice-modes/evals.yaml'))['schema_version'])"`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-voice-modes/evals.yaml
git commit -m "feat(evals): training + holdout prompts and criteria for writing-voice-modes"
```

---

### Task 3.2: `evals.sealed.yaml` — sealed surprise prompts

**Files:**
- Create: `.claude/skills/writing-voice-modes/evals.sealed.yaml`

- [ ] **Step 1: Write the sealed YAML**

Create `.claude/skills/writing-voice-modes/evals.sealed.yaml`:
```yaml
# SEALED SURPRISE PROMPTS — the optimizer subagent must NOT have read access
# to this file. Used by the orchestrator to score generalization every 5 iterations.
schema_version: 1

surprise_prompts:
  - id: surprise_sean_obsidian
    mode: sean
    prompt: "Write a 250-word Substack intro about throwing away your second-brain Notion vault and starting from zero in Obsidian."
  - id: surprise_sedaris_ai_stack
    mode: sedaris_with_gonzo_passage
    prompt: "Write a 250-word Substack intro in Domestic Observer mode, with one Gonzo escalation passage in the middle. Topic: the absurdity of having an AI stack — fourteen autonomous agents, three local models, more MCPs than friends — that knows your morning routine better than anyone in your life."
  - id: surprise_kerouac_drive
    mode: kerouac
    prompt: "Write a 250-word Substack intro in Beat Flow mode about driving from New York to Boston the day you accepted your move."
```

- [ ] **Step 2: Validate**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('.claude/skills/writing-voice-modes/evals.sealed.yaml')); assert len(d['surprise_prompts'])==3; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-voice-modes/evals.sealed.yaml
git commit -m "feat(evals): sealed surprise prompts for held-out generalization scoring"
```

---

### Task 3.3: `program.md` — optimizer subagent instructions

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/program.md`

- [ ] **Step 1: Write the program.md**

Create `agents-sdk/lib/skill_optimizer/program.md`:
```markdown
# Skill Optimizer — Mutation Subagent Instructions

You are an optimization agent. Your job is to propose ONE meaningful, coherent mutation per iteration to the body of `.claude/skills/writing-voice-modes/SKILL.md` so that the skill produces output that scores higher against an eval suite.

## What you receive each iteration

1. The current full text of `SKILL.md`
2. The most recent 5 rows of `results.tsv` (your prior mutation history + scores)
3. A list of the criteria that scored worst on the most recent iteration (so you can target them)
4. The list of mode-specific anti-patterns the eval guards against

## Hard rules — your output is rejected if you violate any of these

1. Edit ONE section of the SKILL.md body. Section = subtree under a `##`, `###`, or `####` heading.
2. **Do NOT touch lines 1-4** (YAML frontmatter — name + description must stay stable).
3. **Do NOT touch lines 23-69** (the 3 example outputs — these are real Sean-voice calibration anchors).
4. **Do NOT touch sections** named `## References`, `## Related Skills`, `## Copy/Paste Ready`.
5. **Do NOT introduce a heading** whose text matches any of these criterion IDs verbatim: `substack_format_intro`, `anti_pattern_overreference`, `stylometric_distance`, `signature_move_present`, `sounds_like_sean`, `no_anti_pattern_violation`. (Anti-gaming guard.)
6. **No whitespace-only diffs.** Your change must alter substantive text.
7. **Diffs must change ≥ 5 lines** OR introduce a structural change (heading add/remove, table edit, bullet add/remove).

## What you should consider mutating (in priority order)

1. **Core Mechanics bullets** within a specific mode (`### 1. Domestic Observer`, etc.)
2. **Sean's Signature Moves table** — sharper mechanic descriptions, better examples
3. **Anti-Patterns table** — clearer "tells" so the model self-corrects
4. **Professional Dial table** — clearer thresholds at each dial level
5. **Content Type → Mode Mapping** — sharper fit between content and mode
6. **Integration Rules** — better resolution of mode/format conflicts
7. **Complementary Technique Pairs** — cleaner mode-blend recipes

## What "good mutation" looks like

- Targets a specific weakness in the most-recent eval scores
- Adds clarity without bloat (don't grow the skill > 50% in tokens — there's a complexity tripwire)
- Uses concrete language over abstract description
- Keeps the rest of the skill internally consistent

## Output format

Respond with EXACTLY this JSON:

```json
{
  "section_heading": "<exact heading you are editing>",
  "rationale": "<≤200 chars explaining why this mutation should improve scores>",
  "modified_skill_md_full_text": "<full SKILL.md after your edit>"
}
```

Return ONLY the JSON. No prose. No markdown fence around the outer object.
```

- [ ] **Step 2: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/program.md
git commit -m "feat(program): mutation subagent instructions with hard rules and priorities"
```

---

### Task 3.4: `judge_prompt.txt` — judge prompt template

**Files:**
- Create: `agents-sdk/lib/skill_optimizer/judge_prompt.txt`

- [ ] **Step 1: Write the judge template**

Create `agents-sdk/lib/skill_optimizer/judge_prompt.txt`:
```
You are evaluating a Substack blog post intro against ONE binary criterion.

OUTPUT TO EVALUATE:
{output}

ANCHOR SAMPLES (real Sean Winslow voice in {mode} mode — for reference AFTER reading the output):

Sample 1:
{anchor_1}

Sample 2:
{anchor_2}

CRITERION:
{question}

Think step-by-step about whether the output above matches the criterion. Then on the LAST LINE answer with EXACTLY one word: YES or NO.
```

- [ ] **Step 2: Commit**

```bash
git add agents-sdk/lib/skill_optimizer/judge_prompt.txt
git commit -m "feat(judge_prompt): judge template with anchors-after-output ordering"
```

---

### Task 3.5: Generate `stylometry_baseline.json` from voice-samples.md

**Files:**
- Create: `agents-sdk/scripts/build_stylometry_baseline.py`
- Generated: `agents-sdk/data/skill-optimizer/stylometry_baseline.json`

- [ ] **Step 1: Write the baseline-builder script**

Create `agents-sdk/scripts/build_stylometry_baseline.py`:
```python
"""Build stylometry baseline from voice-samples.md + a generic baseline corpus.

Run once at pre-flight time. Re-run if voice-samples.md changes.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "agents-sdk"))

from lib.skill_optimizer.stylometry import (
    extract_features,
    extract_distinctive_ngrams,
    save_baseline,
)

VOICE_SAMPLES = REPO / ".claude/skills/writing-voice-modes/references/voice-samples.md"
OUTPUT = REPO / "agents-sdk/data/skill-optimizer/stylometry_baseline.json"

# Generic baseline corpus — short, public-domain prose for the n-gram contrast.
# (Brown corpus excerpt or similar; embedded inline to avoid NLTK dependency.)
GENERIC_BASELINE = """
The fox jumped over the dog. The man went to the store and bought a newspaper.
She was thinking about what to say next when the phone rang again. The conference
ended with a series of dry resolutions, none of which addressed the underlying
issue. He found himself wondering what would happen if no one showed up.
""" * 20  # repeat to reach ~3000 words


def _extract_sean_corpus(samples_path: Path) -> str:
    """Return the unedited+rewrites+full-passages content as a single string."""
    text = samples_path.read_text()
    # Strip frontmatter quote blocks but keep prose. Naïve approach: take everything.
    return text


def main() -> None:
    sean_corpus = _extract_sean_corpus(VOICE_SAMPLES)
    sean_features = extract_features(sean_corpus)

    # Compute per-feature stdev across split chunks of the corpus (~150 words each).
    chunks = [sean_corpus[i : i + 800] for i in range(0, len(sean_corpus), 800)]
    chunks = [c for c in chunks if len(c.split()) >= 30]
    chunk_features = [extract_features(c) for c in chunks]

    stdevs = {}
    for key in sean_features:
        vals = [cf[key] for cf in chunk_features]
        stdevs[key] = statistics.stdev(vals) if len(vals) >= 2 else 1.0

    ngrams = extract_distinctive_ngrams(
        target_corpus=sean_corpus,
        baseline_corpora=[GENERIC_BASELINE],
        top_n=30,
        ns=(2, 3, 4),
    )

    baseline = {
        **sean_features,
        "_stdevs": stdevs,
        "_ngrams": [list(ng) for ng in ngrams],
        "_threshold": None,  # filled in by Task 3.6 (calibration)
        "_corpus_word_count": len(sean_corpus.split()),
    }
    save_baseline(baseline, OUTPUT)
    print(f"wrote baseline to {OUTPUT}")
    print(f"  features: {sean_features}")
    print(f"  top n-grams (first 10): {ngrams[:10]}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the baseline builder**

Run: `cd agents-sdk && PYTHONPATH=. python3 scripts/build_stylometry_baseline.py`
Expected: prints features dict + n-grams + writes `data/skill-optimizer/stylometry_baseline.json`.

- [ ] **Step 3: Commit the script (the JSON is gitignored or committed depending on Sean's preference; default is to commit it for reproducibility)**

```bash
git add agents-sdk/scripts/build_stylometry_baseline.py agents-sdk/data/skill-optimizer/stylometry_baseline.json
git commit -m "feat(stylometry): build baseline JSON from voice-samples.md"
```

---

### Task 3.6: Generate hand-labeled calibration set + tune threshold

**Files:**
- Create: `agents-sdk/scripts/calibrate_stylometry_threshold.py`
- Generated: `agents-sdk/data/skill-optimizer/calibration_set.jsonl`
- Modify: `agents-sdk/data/skill-optimizer/stylometry_baseline.json` (`_threshold` field)

- [ ] **Step 1: Write the calibration script**

Create `agents-sdk/scripts/calibrate_stylometry_threshold.py`:
```python
"""Calibrate the stylometric distance threshold against a 30-example labeled set.

Procedure:
  1. Build 15 real-Sean samples by chunking voice-samples.md.
  2. Generate 15 generic-AI samples by calling Opus 4.7 against varied AI/PM prompts.
  3. Compute compute_distance() for each sample.
  4. Find the threshold that maximizes ROC AUC (i.e., separates 1 from 0).
  5. Write threshold back into stylometry_baseline.json.
  6. Persist the labeled set to calibration_set.jsonl.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "agents-sdk"))

from lib.skill_optimizer.stylometry import (
    extract_features,
    compute_distance,
    load_baseline,
    save_baseline,
)
# Use Anthropic SDK directly for generation. Sean must have ANTHROPIC_API_KEY in env.
from anthropic import Anthropic

VOICE_SAMPLES = REPO / ".claude/skills/writing-voice-modes/references/voice-samples.md"
BASELINE_PATH = REPO / "agents-sdk/data/skill-optimizer/stylometry_baseline.json"
CALIBRATION_OUT = REPO / "agents-sdk/data/skill-optimizer/calibration_set.jsonl"

GENERIC_AI_PROMPTS = [
    "Write a 200-word blog post intro about why product managers should learn Python.",
    "Write a 200-word blog post intro about the rise of AI-native startups in 2026.",
    "Write a 200-word blog post intro about choosing between Claude and GPT for product work.",
    "Write a 200-word blog post intro about the future of crypto product management.",
    "Write a 200-word blog post intro about why every PM needs to understand LLMs.",
    "Write a 200-word blog post intro about hiring the first AI engineer at a startup.",
    "Write a 200-word blog post intro about prompt engineering for product managers.",
    "Write a 200-word blog post intro about measuring AI feature success with users.",
    "Write a 200-word blog post intro about onboarding a new AI tool to your team.",
    "Write a 200-word blog post intro about the trade-offs of fine-tuning vs prompting.",
    "Write a 200-word blog post intro about model context protocols changing PM work.",
    "Write a 200-word blog post intro about the hidden costs of AI infrastructure.",
    "Write a 200-word blog post intro about agentic workflows in modern SaaS products.",
    "Write a 200-word blog post intro about the difference between AI features and AI products.",
    "Write a 200-word blog post intro about how AI is reshaping the PM role at large companies.",
]


def _extract_real_sean_chunks() -> list[str]:
    """Pull ~15 ~100-word chunks from voice-samples.md."""
    text = VOICE_SAMPLES.read_text()
    # Naïve: split by blank lines, keep chunks 60-200 words.
    chunks = re.split(r"\n\s*\n", text)
    keep = []
    for c in chunks:
        wc = len(c.split())
        if 60 <= wc <= 200 and not c.strip().startswith("#") and "AI wrote" not in c:
            keep.append(c.strip())
    if len(keep) < 15:
        # Fall back: split longer passages.
        for c in chunks:
            wc = len(c.split())
            if wc > 200:
                words = c.split()
                for i in range(0, len(words) - 100, 100):
                    keep.append(" ".join(words[i : i + 100]))
                    if len(keep) >= 15:
                        break
            if len(keep) >= 15:
                break
    return keep[:15]


def _generate_ai_samples(prompts: list[str]) -> list[str]:
    client = Anthropic()
    samples = []
    for p in prompts:
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=400,
            messages=[{"role": "user", "content": p}],
        )
        samples.append(msg.content[0].text)
    return samples


def _roc_auc(distances: list[tuple[float, int]]) -> tuple[float, float]:
    """Find threshold maximizing TPR-FPR. Returns (best_threshold, best_score)."""
    distances_sorted = sorted(distances)
    best_t, best_score = 0.0, -1.0
    pos_total = sum(1 for _, label in distances if label == 1)
    neg_total = sum(1 for _, label in distances if label == 0)
    for i in range(len(distances_sorted)):
        t = distances_sorted[i][0]
        tp = sum(1 for d, l in distances if d <= t and l == 1)
        fp = sum(1 for d, l in distances if d <= t and l == 0)
        tpr = tp / pos_total if pos_total else 0
        fpr = fp / neg_total if neg_total else 0
        score = tpr - fpr
        if score > best_score:
            best_score, best_t = score, t
    return best_t, best_score


def main() -> None:
    real = _extract_real_sean_chunks()
    print(f"extracted {len(real)} real-Sean chunks")
    print("generating 15 generic-AI samples (Opus 4.7)...")
    ai = _generate_ai_samples(GENERIC_AI_PROMPTS)

    baseline = load_baseline(BASELINE_PATH)
    distances = []
    with open(CALIBRATION_OUT, "w") as f:
        for text in real:
            features = extract_features(text)
            d = compute_distance(features, baseline, target_text=text)
            distances.append((d, 1))
            f.write(json.dumps({"label": 1, "distance": d, "text": text}) + "\n")
        for text in ai:
            features = extract_features(text)
            d = compute_distance(features, baseline, target_text=text)
            distances.append((d, 0))
            f.write(json.dumps({"label": 0, "distance": d, "text": text}) + "\n")

    threshold, score = _roc_auc(distances)
    print(f"best threshold: {threshold:.2f} (TPR-FPR = {score:.2f})")
    if score < 0.4:
        print("WARNING: low separation. Consider expanding the corpus or adjusting features.")

    baseline["_threshold"] = threshold
    save_baseline(baseline, BASELINE_PATH)
    print(f"updated {BASELINE_PATH} with _threshold = {threshold:.2f}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the calibration**

Run: `cd agents-sdk && PYTHONPATH=. python3 scripts/calibrate_stylometry_threshold.py`
Expected: writes calibration_set.jsonl + updates baseline JSON. Prints threshold + TPR-FPR score. If TPR-FPR < 0.4, halt and tell Sean — features need work.

- [ ] **Step 3: Sean reviews the calibration set**

Print:
```
PRE-FLIGHT BLOCKER — Sean review
Open agents-sdk/data/skill-optimizer/calibration_set.jsonl. For each row, confirm:
  - label=1 rows are unmistakably your voice
  - label=0 rows are unmistakably generic AI
If any row is mislabeled, edit it (change `label`) and re-run the calibration script.
Reply 'calibration approved' when done.
```

- [ ] **Step 4: Commit**

```bash
git add agents-sdk/scripts/calibrate_stylometry_threshold.py agents-sdk/data/skill-optimizer/calibration_set.jsonl agents-sdk/data/skill-optimizer/stylometry_baseline.json
git commit -m "feat(stylometry): calibration set + tuned threshold via ROC-maximization"
```

---

> **Pause point: Phase 3 complete.** All eval data files in place. Stylometry baseline + threshold locked. Sean has reviewed the calibration set.

---

## Phase 4 — Orchestrator (`skill_optimizer.py`)

This is the biggest task. Broken into 6 sub-tasks for tractability.

### Task 4.1: Pre-flight checks (branch verification, paths, config load)

**Files:**
- Create: `agents-sdk/agents/skill_optimizer.py`
- Test: `agents-sdk/tests/test_skill_optimizer.py`

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_skill_optimizer.py`:
```python
"""Integration-shaped tests for skill_optimizer agent."""
import subprocess
import pytest
from agents_sdk.agents.skill_optimizer import preflight_checks, SkillOptimizerConfig


class TestPreflightChecks:
    def test_passes_on_correct_branch(self, tmp_path, monkeypatch):
        # Arrange a fake git repo on the expected branch.
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "autoresearch/writing-voice-modes-2026-05-09"], check=True, capture_output=True)
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        # Create stub files.
        (tmp_path / "SKILL.md").write_text("# Skill")
        (tmp_path / "evals.yaml").write_text("schema_version: 1")
        (tmp_path / "evals.sealed.yaml").write_text("schema_version: 1")
        (tmp_path / "baseline.json").write_text('{"_threshold": 5.0}')
        ok, reason = preflight_checks(config)
        assert ok, reason

    def test_fails_on_wrong_branch(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "main"], check=True, capture_output=True)
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        ok, reason = preflight_checks(config)
        assert not ok
        assert "branch" in reason.lower()

    def test_fails_when_threshold_unset(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "autoresearch/writing-voice-modes-2026-05-09"], check=True, capture_output=True)
        (tmp_path / "SKILL.md").write_text("# Skill")
        (tmp_path / "evals.yaml").write_text("schema_version: 1")
        (tmp_path / "evals.sealed.yaml").write_text("schema_version: 1")
        (tmp_path / "baseline.json").write_text('{"_threshold": null}')
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        ok, reason = preflight_checks(config)
        assert not ok
        assert "threshold" in reason.lower()
```

- [ ] **Step 2: Run test (fails — module doesn't exist)**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement preflight + skeleton**

Create `agents-sdk/agents/skill_optimizer.py`:
```python
"""skill_optimizer.py — autoresearch optimization loop for writing-voice-modes.

See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SkillOptimizerConfig:
    branch: str
    repo_root: Path
    target_skill_md: Path
    evals_path: Path
    evals_sealed_path: Path
    stylometry_baseline_path: Path
    max_iterations: int = 25
    plateau_halt_iterations: int = 3
    runs_per_prompt: int = 15
    cost_cap_usd_hard: float = 200.0
    cost_cap_usd_soft: float = 50.0


def preflight_checks(config: SkillOptimizerConfig) -> tuple[bool, str]:
    """Verify all preconditions before starting the loop."""
    # 1. Correct branch
    try:
        result = subprocess.run(
            ["git", "-C", str(config.repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        current_branch = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"git rev-parse failed: {e.stderr}"
    if current_branch != config.branch:
        return False, f"on branch {current_branch!r}, expected {config.branch!r}"

    # 2. Required files exist
    for p, name in [
        (config.target_skill_md, "SKILL.md"),
        (config.evals_path, "evals.yaml"),
        (config.evals_sealed_path, "evals.sealed.yaml"),
        (config.stylometry_baseline_path, "stylometry_baseline.json"),
    ]:
        if not p.exists():
            return False, f"missing required file: {name} at {p}"

    # 3. Stylometry threshold has been calibrated
    baseline = json.loads(config.stylometry_baseline_path.read_text())
    if baseline.get("_threshold") is None:
        return False, "stylometric threshold not yet calibrated (run calibrate_stylometry_threshold.py)"

    return True, "ok"
```

- [ ] **Step 4: Run test (passes)**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py::TestPreflightChecks -v`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): preflight checks + config dataclass"
```

---

### Task 4.2: Generation runner (Opus 4.7 via Anthropic SDK)

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from unittest.mock import MagicMock
from agents_sdk.agents.skill_optimizer import generate_outputs


class TestGenerateOutputs:
    def test_runs_n_generations_per_prompt(self):
        client = MagicMock()
        client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="generated text")],
            usage=MagicMock(input_tokens=100, output_tokens=200),
        )
        outputs = generate_outputs(
            client=client,
            skill_md_text="# skill body",
            prompts=[{"id": "p1", "prompt": "write x"}],
            runs_per_prompt=3,
        )
        assert len(outputs["p1"]) == 3
        assert all(o["text"] == "generated text" for o in outputs["p1"])
        assert client.messages.create.call_count == 3

    def test_returns_per_prompt_keyed_dict(self):
        client = MagicMock()
        client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="x")],
            usage=MagicMock(input_tokens=1, output_tokens=1),
        )
        outputs = generate_outputs(
            client=client,
            skill_md_text="",
            prompts=[{"id": "a", "prompt": "x"}, {"id": "b", "prompt": "y"}],
            runs_per_prompt=2,
        )
        assert set(outputs.keys()) == {"a", "b"}
        assert len(outputs["a"]) == 2 and len(outputs["b"]) == 2
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py::TestGenerateOutputs -v`
Expected: FAIL

- [ ] **Step 3: Implement `generate_outputs`**

Append to `agents-sdk/agents/skill_optimizer.py`:
```python
def generate_outputs(
    client,
    skill_md_text: str,
    prompts: list[dict],
    runs_per_prompt: int,
    model: str = "claude-opus-4-7",
    max_tokens: int = 600,
) -> dict[str, list[dict]]:
    """Run `runs_per_prompt` generations for each prompt; return outputs keyed by prompt id.

    Each output: {"text": str, "input_tokens": int, "output_tokens": int}
    The skill_md_text is loaded as a system prompt so the generation model behaves
    as if it had loaded the writing-voice-modes skill.
    """
    outputs: dict[str, list[dict]] = {}
    for prompt in prompts:
        outputs[prompt["id"]] = []
        for _ in range(runs_per_prompt):
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=skill_md_text,
                messages=[{"role": "user", "content": prompt["prompt"]}],
            )
            outputs[prompt["id"]].append({
                "text": msg.content[0].text,
                "input_tokens": msg.usage.input_tokens,
                "output_tokens": msg.usage.output_tokens,
            })
    return outputs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py::TestGenerateOutputs -v`
Expected: 2 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): generate_outputs runner with token accounting"
```

---

### Task 4.3: Single-iteration runner (mutation → score → decide → commit-or-revert)

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from agents_sdk.agents.skill_optimizer import score_outputs


class TestScoreOutputs:
    def test_aggregates_structural_and_judge_scores(self):
        # Stub structural checks: every output passes substack format, fails anti-pattern.
        structural_results = {
            "p1": [
                {"substack_format_intro": True, "anti_pattern_overreference": False, "stylometric_distance": True},
                {"substack_format_intro": True, "anti_pattern_overreference": False, "stylometric_distance": True},
            ]
        }
        judge_results = {
            "p1": [
                {"signature_move_present": True, "sounds_like_sean": True, "no_anti_pattern_violation": False},
                {"signature_move_present": True, "sounds_like_sean": False, "no_anti_pattern_violation": True},
            ]
        }
        score = score_outputs(structural_results, judge_results)
        # 2 outputs × 6 criteria = 12 trials. Pass count: structural 2+0+2=4, judge 2+1+1=4 → 8.
        assert score["total_passes"] == 8
        assert score["max_score"] == 12
        assert score["per_criterion"]["substack_format_intro"] == 1.0
        assert score["per_criterion"]["anti_pattern_overreference"] == 0.0
```

- [ ] **Step 2: Run test to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py::TestScoreOutputs -v`
Expected: FAIL

- [ ] **Step 3: Implement scoring + iteration runner**

Append to `agents-sdk/agents/skill_optimizer.py`:
```python
def score_outputs(
    structural_results: dict[str, list[dict[str, bool]]],
    judge_results: dict[str, list[dict[str, bool]]],
) -> dict:
    """Aggregate per-criterion scores.

    Returns {"total_passes": int, "max_score": int, "per_criterion": {id: pass_rate}, "binary_array": list[int]}.
    The binary_array is the flat list of all pass/fail outcomes for bootstrap CI.
    """
    binary_array: list[int] = []
    per_criterion_passes: dict[str, list[int]] = {}
    for prompt_id, results in structural_results.items():
        for r in results:
            for cid, passed in r.items():
                binary_array.append(1 if passed else 0)
                per_criterion_passes.setdefault(cid, []).append(1 if passed else 0)
    for prompt_id, results in judge_results.items():
        for r in results:
            for cid, passed in r.items():
                binary_array.append(1 if passed else 0)
                per_criterion_passes.setdefault(cid, []).append(1 if passed else 0)
    per_criterion = {cid: sum(vs) / len(vs) for cid, vs in per_criterion_passes.items()}
    return {
        "total_passes": sum(binary_array),
        "max_score": len(binary_array),
        "per_criterion": per_criterion,
        "binary_array": binary_array,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): score_outputs aggregator across structural+judge"
```

---

### Task 4.4: Mutation proposal via subagent + git commit/revert

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`

- [ ] **Step 1: Add propose_mutation function**

Append to `agents-sdk/agents/skill_optimizer.py`:
```python
import json as _json


def propose_mutation(
    optimizer_client,
    program_md: str,
    current_skill_md: str,
    recent_results: list[dict],
    worst_criteria: list[str],
    model: str = "claude-opus-4-7",
) -> tuple[str, str, str]:
    """Ask the optimizer subagent to propose ONE mutation.

    Returns (section_heading, rationale, modified_skill_md_full_text).
    Raises ValueError if the response is malformed.
    """
    user_msg = (
        f"## Current SKILL.md\n\n{current_skill_md}\n\n"
        f"## Recent results (last {len(recent_results)} iterations)\n\n"
        f"{_json.dumps(recent_results, indent=2)}\n\n"
        f"## Worst-scoring criteria last iteration\n\n"
        f"{', '.join(worst_criteria)}\n\n"
        f"Propose ONE mutation. Respond with the JSON object specified in your instructions."
    )
    msg = optimizer_client.messages.create(
        model=model,
        max_tokens=8000,
        system=program_md,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = msg.content[0].text.strip()
    # Strip optional markdown fence.
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1].lstrip("json").strip()
    parsed = _json.loads(raw)
    return parsed["section_heading"], parsed["rationale"], parsed["modified_skill_md_full_text"]


def git_commit_mutation(
    repo_root: Path,
    skill_md_path: Path,
    iteration: int,
    section: str,
    rationale: str,
    score_old: float,
    score_new: float,
) -> None:
    msg = (
        f"optimize(writing-voice-modes): {rationale}\n\n"
        f"Score: {score_old:.3f} → {score_new:.3f} (+{score_new-score_old:.3f})\n"
        f"Iteration: {iteration:02d}/25\n"
        f"Section mutated: {section}\n\n"
        f"🤖 Generated by skill_optimizer.py"
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "add", str(skill_md_path)],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "commit", "-m", msg],
        check=True, capture_output=True,
    )


def git_revert_skill_md(repo_root: Path, skill_md_path: Path) -> None:
    """Discard in-tree changes to the skill file."""
    subprocess.run(
        ["git", "-C", str(repo_root), "checkout", "--", str(skill_md_path)],
        check=True, capture_output=True,
    )
```

- [ ] **Step 2: Add a smoke test for git_commit / git_revert**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from agents_sdk.agents.skill_optimizer import git_commit_mutation, git_revert_skill_md


class TestGitOps:
    def test_revert_restores_original(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "x@x.com"], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "x"], check=True)
        f = tmp_path / "skill.md"
        f.write_text("original")
        subprocess.run(["git", "-C", str(tmp_path), "add", "skill.md"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "init"], check=True, capture_output=True)
        f.write_text("modified")
        git_revert_skill_md(tmp_path, f)
        assert f.read_text() == "original"
```

- [ ] **Step 3: Run tests**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v`
Expected: all PASS

- [ ] **Step 4: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): mutation proposal + git commit/revert helpers"
```

---

### Task 4.5: Results.tsv writer

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

- [ ] **Step 1: Write the failing test**

Append:
```python
from agents_sdk.agents.skill_optimizer import write_results_row, RESULTS_HEADER


class TestResultsTSV:
    def test_writes_header_on_first_row(self, tmp_path):
        path = tmp_path / "results.tsv"
        row = {f: "" for f in RESULTS_HEADER}
        row["iteration"] = 1
        row["mutation_summary"] = "test mutation"
        write_results_row(path, row)
        contents = path.read_text()
        assert contents.split("\n")[0] == "\t".join(RESULTS_HEADER)
        assert "test mutation" in contents.split("\n")[1]

    def test_appends_without_duplicating_header(self, tmp_path):
        path = tmp_path / "results.tsv"
        for i in range(3):
            row = {f: "" for f in RESULTS_HEADER}
            row["iteration"] = i + 1
            write_results_row(path, row)
        lines = path.read_text().rstrip().split("\n")
        assert len(lines) == 4  # header + 3 rows
```

- [ ] **Step 2: Implement**

Append to `agents-sdk/agents/skill_optimizer.py`:
```python
RESULTS_HEADER = (
    "iteration", "timestamp", "mutation_section", "mutation_summary",
    "train_score", "holdout_score", "surprise_score",
    "criterion_substack_format_intro", "criterion_anti_pattern_overreference",
    "criterion_stylometric_distance", "criterion_signature_move_present",
    "criterion_sounds_like_sean", "criterion_no_anti_pattern_violation",
    "moving_avg", "delta_vs_best", "kept_or_reverted",
    "tripwires_triggered", "sonnet_qwen_agreement", "duration_sec", "cost_usd",
)


def write_results_row(path: Path, row: dict) -> None:
    """Append one row to results.tsv. Writes the header on first invocation."""
    write_header = not path.exists()
    with open(path, "a") as f:
        if write_header:
            f.write("\t".join(RESULTS_HEADER) + "\n")
        f.write("\t".join(str(row.get(k, "")) for k in RESULTS_HEADER) + "\n")
```

- [ ] **Step 3: Run + commit**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v`
Expected: all PASS

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): write_results_row TSV appender with header guard"
```

---

### Task 4.6: Main loop + halt conditions + CLI entry

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`

- [ ] **Step 1: Implement the main `run_optimization_loop` function**

Append to `agents-sdk/agents/skill_optimizer.py`:
```python
import datetime
import time
import yaml
from anthropic import Anthropic

from lib.skill_optimizer.structural_checks import (
    substack_format_intro,
    anti_pattern_overreference,
    stylometric_distance,
)
from lib.skill_optimizer.stylometry import load_baseline
from lib.skill_optimizer.judge_runner import JudgeRunner
from lib.skill_optimizer.mutation_guard import validate_mutation
from lib.skill_optimizer.decision import keep_or_revert, moving_average
from lib.skill_optimizer.tripwire import check_all_tripwires, IterationSnapshot

PROTECTED_LINE_RANGES = [(1, 4), (23, 69)]
PROTECTED_SECTION_HEADINGS = ("References", "Related Skills", "Copy/Paste Ready")
CRITERION_IDS = (
    "substack_format_intro", "anti_pattern_overreference", "stylometric_distance",
    "signature_move_present", "sounds_like_sean", "no_anti_pattern_violation",
)


def run_optimization_loop(config: SkillOptimizerConfig, dry_run: bool = False) -> None:
    """Top-level loop. See spec Section 9 for the data flow."""
    ok, reason = preflight_checks(config)
    if not ok:
        raise RuntimeError(f"preflight failed: {reason}")

    evals = yaml.safe_load(config.evals_path.read_text())
    sealed = yaml.safe_load(config.evals_sealed_path.read_text())
    baseline = load_baseline(config.stylometry_baseline_path)
    program_md = (config.repo_root / "agents-sdk/lib/skill_optimizer/program.md").read_text()
    judge_template = (config.repo_root / "agents-sdk/lib/skill_optimizer/judge_prompt.txt").read_text()

    anthropic = Anthropic()
    # Local Ollama client wrapper — implementation can use anthropic-style or direct HTTP.
    # For dry_run, both clients are mocks that return canned text/YES.
    local_client = _build_ollama_client(config) if not dry_run else _DummyClient("YES")
    sonnet_client = anthropic if not dry_run else _DummyClient("YES")
    judge = JudgeRunner(local_client=local_client, sonnet_client=sonnet_client, prompt_template=judge_template)

    results_path = config.repo_root / "agents-sdk" / config.results_path if hasattr(config, "results_path") else config.repo_root / "agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv"

    best_binary_array: list[int] = []
    train_scores: list[float] = []
    iter1_snapshot: Optional[dict] = None
    cumulative_cost = 0.0

    for iteration in range(1, config.max_iterations + 1):
        start = time.time()
        current_skill_md = config.target_skill_md.read_text()

        # 1. Propose mutation
        recent_rows = _read_recent_rows(results_path, n=5)
        worst = _worst_criteria(recent_rows)
        try:
            section, rationale, modified_md = propose_mutation(
                optimizer_client=anthropic,
                program_md=program_md,
                current_skill_md=current_skill_md,
                recent_results=recent_rows,
                worst_criteria=worst,
            )
        except Exception as e:
            print(f"[iter {iteration}] mutation proposal failed: {e}; skipping")
            continue

        # 2. Validate
        ok, reason = validate_mutation(
            original_lines=current_skill_md.splitlines(keepends=True),
            modified_lines=modified_md.splitlines(keepends=True),
            protected_line_ranges=PROTECTED_LINE_RANGES,
            protected_section_headings=PROTECTED_SECTION_HEADINGS,
            criterion_ids=CRITERION_IDS,
        )
        if not ok:
            print(f"[iter {iteration}] mutation rejected: {reason}; retrying")
            continue

        # 3. Apply in-memory (write to disk; will revert on bad score)
        config.target_skill_md.write_text(modified_md)

        # 4. Generate
        train_outputs = generate_outputs(anthropic, modified_md, evals["training_prompts"], config.runs_per_prompt)
        holdout_outputs = generate_outputs(anthropic, modified_md, evals["holdout_prompts"], config.runs_per_prompt)
        surprise_outputs = {}
        if iteration % 5 == 0:
            surprise_outputs = generate_outputs(anthropic, modified_md, sealed["surprise_prompts"], config.runs_per_prompt)

        # 5. Score
        structural = _run_structural_checks(train_outputs, baseline)
        judge_outputs = _run_judge(judge, train_outputs, evals, mode_anchors=_load_anchors())
        train = score_outputs(structural, judge_outputs)
        train_score = train["total_passes"] / train["max_score"]

        # Holdout score (no decision-rule role; trip-wire only)
        ho_structural = _run_structural_checks(holdout_outputs, baseline)
        ho_judge = _run_judge(judge, holdout_outputs, evals, mode_anchors=_load_anchors())
        holdout = score_outputs(ho_structural, ho_judge)
        holdout_score = holdout["total_passes"] / holdout["max_score"]

        # 6. Sonnet sample-check (every 5 iters)
        sonnet_agreement = 1.0
        if iteration % config.sonnet_check_every_n_iterations == 0:
            sonnet_agreement = _sonnet_check(judge, train_outputs, evals)

        # 7. Decide keep/revert
        train_scores.append(train_score)
        ma = moving_average(train_scores, window=3)
        decision, info = keep_or_revert(train["binary_array"], best_binary_array)

        # 8. Trip-wires
        snapshot = _build_snapshot(iteration, train_score, holdout_score, train, iter1_snapshot, sonnet_agreement, modified_md)
        triggered = check_all_tripwires(snapshot)

        # 9. Apply decision (after tripwires for logging)
        if decision == "keep":
            best_binary_array = train["binary_array"]
            git_commit_mutation(config.repo_root, config.target_skill_md, iteration, section, rationale, ma if iteration > 1 else train_score, train_score)
        else:
            git_revert_skill_md(config.repo_root, config.target_skill_md)

        # 10. Log
        write_results_row(results_path, _build_row(iteration, section, rationale, train_score, holdout_score, surprise_outputs, train, ma, info, decision, triggered, sonnet_agreement, time.time() - start, cumulative_cost))

        if iter1_snapshot is None:
            iter1_snapshot = {"train_score": train_score, "criterion_scores": train["per_criterion"], "skill_md_token_count": len(modified_md.split()), "stylometric_score": train["per_criterion"].get("stylometric_distance", 0), "llm_judge_score": _llm_judge_avg(train["per_criterion"]), "avg_inter_run_similarity": _diversity(train_outputs)}

        # 11. Halt checks
        if iteration >= 4 and triggered:
            print(f"[iter {iteration}] HALT — tripwires triggered: {triggered}")
            break
        if train_score >= 0.75 and all(v >= 0.60 for v in train["per_criterion"].values()):
            print(f"[iter {iteration}] SUCCESS — aggregate {train_score:.3f} ≥ 0.75 with all floors ≥ 0.60")
            break
        if _plateau(train_scores, n=config.plateau_halt_iterations):
            print(f"[iter {iteration}] HALT — plateau ({config.plateau_halt_iterations} iters no improvement)")
            break

    print(f"loop complete after {iteration} iterations")


# Helper function placeholders — fully implemented in Tasks 4.7, 4.8, 4.9.
# These NotImplementedError stubs let skill_optimizer.py import cleanly so other
# tests can exercise pre-flight + scoring + git ops independently.
def _build_ollama_client(config):
    raise NotImplementedError("implemented in Task 4.9")

def _read_recent_rows(path, n):
    raise NotImplementedError("implemented in Task 4.8")

def _worst_criteria(rows):
    raise NotImplementedError("implemented in Task 4.7")

def _run_structural_checks(outputs, baseline):
    raise NotImplementedError("implemented in Task 4.9")

def _run_judge(judge, outputs, evals, mode_anchors):
    raise NotImplementedError("implemented in Task 4.9")

def _load_anchors():
    raise NotImplementedError("implemented in Task 4.8")

def _sonnet_check(judge, outputs, evals):
    raise NotImplementedError("implemented in Task 4.9")

def _build_snapshot(*args, **kwargs):
    raise NotImplementedError("implemented in Task 4.8")

def _build_row(*args, **kwargs):
    raise NotImplementedError("implemented in Task 4.8")

def _llm_judge_avg(per_criterion):
    raise NotImplementedError("implemented in Task 4.7")

def _diversity(outputs):
    raise NotImplementedError("implemented in Task 4.7")

def _plateau(scores, n):
    raise NotImplementedError("implemented in Task 4.7")


class _DummyClient:
    """Echo client for dry-run mode."""
    def __init__(self, fixed_response: str = "YES"):
        self._r = fixed_response
        self.messages = self
    def create(self, **kwargs):
        return type("M", (), {"content": [type("C", (), {"text": self._r})()], "usage": type("U", (), {"input_tokens": 100, "output_tokens": 200})()})()
    def complete(self, **kwargs):
        return f"reasoning\n{self._r}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--config-path", default="agents-sdk/config.toml")
    args = ap.parse_args()
    # Load config from TOML — caller fills in repo_root etc.
    import tomllib
    repo_root = Path(__file__).resolve().parents[2]
    cfg_data = tomllib.load(open(repo_root / args.config_path, "rb"))["agents"]["skill_optimizer"]
    config = SkillOptimizerConfig(
        branch=cfg_data["branch"],
        repo_root=repo_root,
        target_skill_md=repo_root / cfg_data["target_skill_md"],
        evals_path=repo_root / cfg_data["evals_path"],
        evals_sealed_path=repo_root / cfg_data["evals_sealed_path"],
        stylometry_baseline_path=repo_root / "agents-sdk" / cfg_data["stylometry_baseline_path"],
        max_iterations=cfg_data.get("max_iterations", 25),
        runs_per_prompt=cfg_data.get("runs_per_prompt", 15),
        cost_cap_usd_hard=cfg_data.get("cost_cap_usd_hard", 200.0),
    )
    run_optimization_loop(config, dry_run=args.dry_run)
```

> **Note:** The 12 helper functions (`_build_ollama_client`, `_read_recent_rows`, etc.) are stubs raising `NotImplementedError`. They are fully implemented in Tasks 4.7, 4.8, and 4.9 with TDD. This task only ships the `run_optimization_loop` skeleton + CLI entry; the helpers come next.

- [ ] **Step 2: Verify the file imports cleanly with NotImplementedError stubs**

Run: `cd agents-sdk && PYTHONPATH=. python3 -c "from agents.skill_optimizer import run_optimization_loop, SkillOptimizerConfig; print('imports ok')"`
Expected: `imports ok`

- [ ] **Step 3: Commit the main loop skeleton**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): run_optimization_loop skeleton with helper stubs + CLI entry"
```

---

### Task 4.7: Utility helpers (`_plateau`, `_llm_judge_avg`, `_diversity`, `_worst_criteria`)

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

These are pure functions — no I/O, no external dependencies. Test all four together; implement all four together.

- [ ] **Step 1: Write the failing tests (append to test file)**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from agents_sdk.agents.skill_optimizer import (
    _plateau,
    _llm_judge_avg,
    _diversity,
    _worst_criteria,
)


class TestPlateau:
    def test_returns_false_below_window(self):
        assert _plateau([0.7, 0.7], n=3) is False

    def test_returns_true_when_flat(self):
        assert _plateau([0.7, 0.7, 0.7], n=3) is True

    def test_returns_true_within_tolerance(self):
        # Spread of 0.003 is below the 0.005 default tolerance.
        assert _plateau([0.700, 0.701, 0.703], n=3) is True

    def test_returns_false_with_real_movement(self):
        assert _plateau([0.70, 0.75, 0.80], n=3) is False


class TestLLMJudgeAvg:
    def test_averages_only_judge_criteria(self):
        per = {
            "substack_format_intro": 1.0,        # structural — ignored
            "anti_pattern_overreference": 1.0,   # structural — ignored
            "stylometric_distance": 1.0,          # structural — ignored
            "signature_move_present": 0.6,
            "sounds_like_sean": 0.4,
            "no_anti_pattern_violation": 0.8,
        }
        assert _llm_judge_avg(per) == pytest.approx((0.6 + 0.4 + 0.8) / 3)

    def test_handles_missing_keys_as_zero(self):
        assert _llm_judge_avg({}) == 0.0


class TestDiversity:
    def test_high_similarity_when_outputs_identical(self):
        outputs = {
            "p1": [
                {"text": "the quick brown fox jumps over the lazy dog every morning"},
                {"text": "the quick brown fox jumps over the lazy dog every morning"},
            ]
        }
        assert _diversity(outputs) > 0.95

    def test_low_similarity_when_outputs_diverse(self):
        outputs = {
            "p1": [
                {"text": "the quick brown fox jumps over the lazy dog"},
                {"text": "completely unrelated prose with different vocabulary words entirely"},
            ]
        }
        assert _diversity(outputs) < 0.5

    def test_returns_zero_when_only_one_run_per_prompt(self):
        outputs = {"p1": [{"text": "only one run here"}]}
        assert _diversity(outputs) == 0.0


class TestWorstCriteria:
    def test_returns_top_n_worst_from_last_row(self):
        rows = [{
            "criterion_substack_format_intro": "0.95",
            "criterion_anti_pattern_overreference": "0.90",
            "criterion_stylometric_distance": "0.50",
            "criterion_signature_move_present": "0.70",
            "criterion_sounds_like_sean": "0.40",
            "criterion_no_anti_pattern_violation": "0.85",
        }]
        worst = _worst_criteria(rows)
        # Three lowest: sounds_like_sean (0.40), stylometric_distance (0.50), signature_move_present (0.70)
        assert worst[0] == "sounds_like_sean"
        assert worst[1] == "stylometric_distance"
        assert worst[2] == "signature_move_present"

    def test_returns_empty_for_no_rows(self):
        assert _worst_criteria([]) == []

    def test_skips_non_numeric_columns(self):
        rows = [{"criterion_substack_format_intro": "0.95", "iteration": "5"}]
        worst = _worst_criteria(rows)
        assert worst == ["substack_format_intro"]
```

- [ ] **Step 2: Run tests to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "Plateau or LLMJudgeAvg or Diversity or WorstCriteria"`
Expected: FAIL — `NotImplementedError` raised.

- [ ] **Step 3: Replace each NotImplementedError stub with the real implementation**

In `agents-sdk/agents/skill_optimizer.py`, replace the four utility stubs:

```python
import math


def _plateau(scores: list[float], n: int = 3, tol: float = 0.005) -> bool:
    """True when the last `n` scores are within `tol` of each other (no improvement)."""
    if len(scores) < n:
        return False
    tail = scores[-n:]
    return max(tail) - min(tail) <= tol


def _llm_judge_avg(per_criterion: dict[str, float]) -> float:
    """Mean of just the LLM-judge criteria (excludes structural)."""
    keys = ("signature_move_present", "sounds_like_sean", "no_anti_pattern_violation")
    vals = [per_criterion.get(k, 0.0) for k in keys]
    return sum(vals) / len(vals) if vals else 0.0


def _char_trigram_bag(text: str) -> dict[str, int]:
    text = text.lower()
    bag: dict[str, int] = {}
    for i in range(len(text) - 2):
        tri = text[i : i + 3]
        bag[tri] = bag.get(tri, 0) + 1
    return bag


def _cosine(a: dict[str, int], b: dict[str, int]) -> float:
    common = set(a.keys()) & set(b.keys())
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def _diversity(outputs: dict[str, list[dict]]) -> float:
    """Average inter-run cosine similarity over character trigrams.

    Higher = more similar (entropy collapse — a tripwire signal). Returns 0.0
    when no prompt has at least 2 runs to compare.
    """
    sims = []
    for _prompt_id, runs in outputs.items():
        if len(runs) < 2:
            continue
        bags = [_char_trigram_bag(r["text"]) for r in runs]
        for i in range(len(bags)):
            for j in range(i + 1, len(bags)):
                sims.append(_cosine(bags[i], bags[j]))
    return sum(sims) / len(sims) if sims else 0.0


def _worst_criteria(rows: list[dict]) -> list[str]:
    """Return the 3 criterion names with the lowest scores in the most recent row."""
    if not rows:
        return []
    last = rows[-1]
    scored = []
    for k, v in last.items():
        if not k.startswith("criterion_"):
            continue
        try:
            scored.append((float(v), k.removeprefix("criterion_")))
        except (ValueError, TypeError):
            continue
    scored.sort()  # ascending — worst (lowest) first
    return [name for _, name in scored[:3]]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "Plateau or LLMJudgeAvg or Diversity or WorstCriteria"`
Expected: 12 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): implement utility helpers (plateau, judge_avg, diversity, worst_criteria)"
```

---

### Task 4.8: Data layer helpers (`_read_recent_rows`, `_load_anchors`, `_build_row`, `_build_snapshot`)

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

These touch files (results.tsv, voice-samples.md) and shape dicts for downstream consumers (results.tsv writer, IterationSnapshot).

- [ ] **Step 1: Write the failing tests**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from agents_sdk.agents.skill_optimizer import (
    _read_recent_rows,
    _load_anchors,
    _build_row,
    _build_snapshot,
    RESULTS_HEADER,
)


class TestReadRecentRows:
    def test_returns_empty_when_file_missing(self, tmp_path):
        assert _read_recent_rows(tmp_path / "missing.tsv", n=5) == []

    def test_returns_last_n_rows(self, tmp_path):
        path = tmp_path / "r.tsv"
        path.write_text("a\tb\n1\t2\n3\t4\n5\t6\n")
        rows = _read_recent_rows(path, n=2)
        assert len(rows) == 2
        assert rows[-1]["a"] == "5"

    def test_returns_all_rows_when_n_exceeds_count(self, tmp_path):
        path = tmp_path / "r.tsv"
        path.write_text("a\tb\n1\t2\n")
        rows = _read_recent_rows(path, n=10)
        assert len(rows) == 1


class TestLoadAnchors:
    def test_returns_dict_with_all_modes(self, tmp_path, monkeypatch):
        # Fake voice-samples.md with one section per mode.
        fake_samples = tmp_path / "voice-samples.md"
        fake_samples.write_text(
            "# Samples\n\n"
            "### Sedaris Sample One\n"
            "> Mundane accumulation example with enough words to count as content easily here.\n\n"
            "**Why it works:** explanation\n\n"
            "### Thompson Gonzo Example\n"
            "I DEPLOYED TO PRODUCTION at 11:47 PM and everything broke instantly afterwards.\n\n"
            "### Kerouac Beat Flow Sample\n"
            "And the ferry — the slow gray crossing — and the cold coffee in my hand.\n\n"
            "### Vonnegut Minimalist Closer\n"
            "It sounds the same as it always did. I sound different. I have begun.\n\n"
        )
        # Patch the module-level path constant.
        from agents_sdk.agents import skill_optimizer
        monkeypatch.setattr(
            skill_optimizer,
            "_VOICE_SAMPLES_PATH",
            fake_samples,
        )
        anchors = _load_anchors()
        assert "sedaris" in anchors and len(anchors["sedaris"]) >= 1
        assert "gonzo" in anchors and len(anchors["gonzo"]) >= 1
        assert "kerouac" in anchors and len(anchors["kerouac"]) >= 1
        assert "vonnegut" in anchors and len(anchors["vonnegut"]) >= 1

    def test_pads_thin_modes_with_sean_fallback(self, tmp_path, monkeypatch):
        fake_samples = tmp_path / "voice-samples.md"
        fake_samples.write_text(
            "# Samples\n\n"
            "### Sean general voice sample\n"
            "Some Sean voice prose here that has at least thirty words so the parser keeps it.\n\n"
            "Another Sean snippet that the parser will treat as separate from above one.\n\n"
        )
        from agents_sdk.agents import skill_optimizer
        monkeypatch.setattr(skill_optimizer, "_VOICE_SAMPLES_PATH", fake_samples)
        anchors = _load_anchors()
        # Even though no Sedaris-tagged samples exist, sedaris key is non-empty (padded).
        assert len(anchors["sedaris"]) >= 2


class TestBuildRow:
    def test_includes_all_header_fields(self):
        train_result = {
            "per_criterion": {
                "substack_format_intro": 0.9,
                "anti_pattern_overreference": 0.8,
                "stylometric_distance": 0.7,
                "signature_move_present": 0.6,
                "sounds_like_sean": 0.5,
                "no_anti_pattern_violation": 0.4,
            },
        }
        row = _build_row(
            iteration=3,
            section="### Beat Flow Mode",
            rationale="tightened jewel-center bullet",
            train_score=0.65,
            holdout_score=0.60,
            surprise_outputs={},
            train_result=train_result,
            moving_avg=0.62,
            decision_info={"delta_mean": 0.05},
            decision="keep",
            tripwires=[],
            sonnet_agreement=0.92,
            duration_sec=420.5,
            cost_usd=4.15,
        )
        for k in RESULTS_HEADER:
            assert k in row
        assert row["iteration"] == 3
        assert row["mutation_section"] == "### Beat Flow Mode"
        assert row["kept_or_reverted"] == "keep"
        assert row["tripwires_triggered"] == ""

    def test_truncates_long_rationale_to_200_chars(self):
        long_rationale = "x" * 500
        row = _build_row(
            iteration=1, section="x", rationale=long_rationale, train_score=0.5,
            holdout_score=0.5, surprise_outputs={},
            train_result={"per_criterion": {}}, moving_avg=0.5,
            decision_info={"delta_mean": 0}, decision="revert", tripwires=[],
            sonnet_agreement=1.0, duration_sec=1.0, cost_usd=0.0,
        )
        assert len(row["mutation_summary"]) == 200


class TestBuildSnapshot:
    def test_uses_current_as_baseline_when_iter1(self):
        train_result = {
            "per_criterion": {
                "stylometric_distance": 0.7,
                "signature_move_present": 0.6,
                "sounds_like_sean": 0.5,
                "no_anti_pattern_violation": 0.5,
            },
            "binary_array": [],
        }
        snap = _build_snapshot(
            iteration=1, train_score=0.6, holdout_score=0.55,
            train_result=train_result, iter1_snapshot=None,
            sonnet_agreement=0.9, skill_md_text="word " * 500,
            holdout_history=[], diversity=0.4,
        )
        # When iter1, baseline equals current.
        assert snap.score_gain_vs_baseline == 0.0
        assert snap.skill_md_token_count == snap.skill_md_token_count_baseline

    def test_carries_iter1_baseline_through(self):
        iter1 = {
            "train_score": 0.50,
            "criterion_scores": {"signature_move_present": 0.5},
            "skill_md_token_count": 400,
            "stylometric_score": 0.6,
            "llm_judge_score": 0.5,
            "avg_inter_run_similarity": 0.3,
        }
        train_result = {
            "per_criterion": {
                "stylometric_distance": 0.7,
                "signature_move_present": 0.7,
                "sounds_like_sean": 0.7,
                "no_anti_pattern_violation": 0.7,
            },
            "binary_array": [],
        }
        snap = _build_snapshot(
            iteration=5, train_score=0.70, holdout_score=0.65,
            train_result=train_result, iter1_snapshot=iter1,
            sonnet_agreement=0.85, skill_md_text="word " * 600,
            holdout_history=[0.66, 0.65, 0.64], diversity=0.4,
        )
        assert snap.score_gain_vs_baseline == pytest.approx(0.20)
        assert snap.skill_md_token_count == 600
        assert snap.skill_md_token_count_baseline == 400
```

- [ ] **Step 2: Run tests to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "ReadRecentRows or LoadAnchors or BuildRow or BuildSnapshot"`
Expected: FAIL — `NotImplementedError` or `AttributeError`.

- [ ] **Step 3: Implement the four helpers**

Add the path constant near the top of `agents-sdk/agents/skill_optimizer.py` (just below imports, before any function definitions):

```python
_REPO_ROOT = Path(__file__).resolve().parents[2]
_VOICE_SAMPLES_PATH = _REPO_ROOT / ".claude/skills/writing-voice-modes/references/voice-samples.md"
```

Then replace each NotImplementedError stub:

```python
import csv
import re
from typing import Optional


def _read_recent_rows(path: Path, n: int) -> list[dict]:
    """Return the last `n` rows from a TSV with header. Empty list if missing."""
    if not path.exists():
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    return rows[-n:]


_MODE_KEYWORDS = {
    "sedaris": ("sedaris", "domestic observer"),
    "gonzo": ("thompson", "gonzo"),
    "kerouac": ("kerouac", "beat flow"),
    "vonnegut": ("vonnegut", "minimalist"),
}


def _load_anchors() -> dict[str, list[str]]:
    """Parse voice-samples.md and group anchor snippets by mode.

    Splits on `### ` headings, infers mode from heading text via keyword match,
    keeps prose snippets ≥ 30 words, truncates to ~150 words. Modes that end up
    with fewer than 2 anchors are padded with sean-tagged fallbacks so ensemble
    judges always have ≥ 2 to choose from.
    """
    text = _VOICE_SAMPLES_PATH.read_text()
    sections = re.split(r"\n###\s+", text)
    by_mode: dict[str, list[str]] = {"sean": [], "sedaris": [], "gonzo": [], "kerouac": [], "vonnegut": []}

    for section in sections[1:]:  # skip preamble
        heading_line, *rest = section.split("\n", 1)
        body = rest[0] if rest else ""
        # Strip "**Why it works:**" annotations and blockquote markers.
        body = re.sub(r"^\*\*Why.*$", "", body, flags=re.MULTILINE)
        body = body.replace("> ", "").strip()
        if len(body.split()) < 30:
            continue
        snippet = " ".join(body.split()[:150])

        heading_lower = heading_line.lower()
        matched = False
        for mode, kws in _MODE_KEYWORDS.items():
            if any(kw in heading_lower for kw in kws):
                by_mode[mode].append(snippet)
                matched = True
                break
        if not matched:
            by_mode["sean"].append(snippet)

    # Pad thin modes with sean fallback so each mode has ≥ 2 anchors.
    fallback = by_mode["sean"][:2] if by_mode["sean"] else []
    for mode in by_mode:
        while len(by_mode[mode]) < 2 and fallback:
            by_mode[mode].append(fallback[len(by_mode[mode]) % len(fallback)])

    return by_mode


def _build_row(
    iteration: int,
    section: str,
    rationale: str,
    train_score: float,
    holdout_score: float,
    surprise_outputs: dict,
    train_result: dict,
    moving_avg: float,
    decision_info: dict,
    decision: str,
    tripwires: list[str],
    sonnet_agreement: float,
    duration_sec: float,
    cost_usd: float,
) -> dict:
    """Build a results.tsv row dict matching RESULTS_HEADER."""
    per = train_result["per_criterion"]
    surprise_score = ""
    if surprise_outputs:
        # Caller computes surprise score externally and passes it in via surprise_outputs["__score"].
        surprise_score = f"{surprise_outputs.get('__score', 0):.4f}"

    return {
        "iteration": iteration,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "mutation_section": section,
        "mutation_summary": rationale[:200],
        "train_score": f"{train_score:.4f}",
        "holdout_score": f"{holdout_score:.4f}",
        "surprise_score": surprise_score,
        "criterion_substack_format_intro": f"{per.get('substack_format_intro', 0):.4f}",
        "criterion_anti_pattern_overreference": f"{per.get('anti_pattern_overreference', 0):.4f}",
        "criterion_stylometric_distance": f"{per.get('stylometric_distance', 0):.4f}",
        "criterion_signature_move_present": f"{per.get('signature_move_present', 0):.4f}",
        "criterion_sounds_like_sean": f"{per.get('sounds_like_sean', 0):.4f}",
        "criterion_no_anti_pattern_violation": f"{per.get('no_anti_pattern_violation', 0):.4f}",
        "moving_avg": f"{moving_avg:.4f}",
        "delta_vs_best": f"{decision_info.get('delta_mean', 0):.4f}",
        "kept_or_reverted": decision,
        "tripwires_triggered": ",".join(tripwires),
        "sonnet_qwen_agreement": f"{sonnet_agreement:.3f}",
        "duration_sec": f"{duration_sec:.1f}",
        "cost_usd": f"{cost_usd:.4f}",
    }


def _build_snapshot(
    iteration: int,
    train_score: float,
    holdout_score: float,
    train_result: dict,
    iter1_snapshot: Optional[dict],
    sonnet_agreement: float,
    skill_md_text: str,
    holdout_history: list[float],
    diversity: float,
) -> "IterationSnapshot":
    """Construct an IterationSnapshot for tripwire checks. iter1=None means snapshot self-references."""
    iter1 = iter1_snapshot or {}
    current_token_count = len(skill_md_text.split())
    return IterationSnapshot(
        iteration=iteration,
        train_score=train_score,
        holdout_score=holdout_score,
        prior_holdout_scores=holdout_history[-3:],
        criterion_scores=train_result["per_criterion"],
        criterion_scores_iter1=iter1.get("criterion_scores", train_result["per_criterion"]),
        stylometric_score=train_result["per_criterion"].get("stylometric_distance", 0.0),
        stylometric_score_baseline=iter1.get(
            "stylometric_score",
            train_result["per_criterion"].get("stylometric_distance", 0.0),
        ),
        llm_judge_score=_llm_judge_avg(train_result["per_criterion"]),
        llm_judge_score_baseline=iter1.get(
            "llm_judge_score",
            _llm_judge_avg(train_result["per_criterion"]),
        ),
        avg_inter_run_similarity=diversity,
        avg_inter_run_similarity_baseline=iter1.get("avg_inter_run_similarity", diversity),
        sonnet_qwen_agreement=sonnet_agreement,
        skill_md_token_count=current_token_count,
        skill_md_token_count_baseline=iter1.get("skill_md_token_count", current_token_count),
        score_gain_vs_baseline=train_score - iter1.get("train_score", train_score),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "ReadRecentRows or LoadAnchors or BuildRow or BuildSnapshot"`
Expected: 9 PASS

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): implement data-layer helpers (read_recent_rows, load_anchors, build_row, build_snapshot)"
```

---

### Task 4.9: External-call helpers (`_build_ollama_client`, `_run_structural_checks`, `_run_judge`, `_sonnet_check`)

**Files:**
- Modify: `agents-sdk/agents/skill_optimizer.py`
- Modify: `agents-sdk/tests/test_skill_optimizer.py`

These touch the Ollama HTTP API, the structural_checks module, the judge_runner module, and Sonnet via the Anthropic SDK. All external interactions are mocked in tests.

- [ ] **Step 1: Write the failing tests**

Append to `agents-sdk/tests/test_skill_optimizer.py`:
```python
from unittest.mock import MagicMock, patch
from agents_sdk.agents.skill_optimizer import (
    _build_ollama_client,
    _run_structural_checks,
    _run_judge,
    _sonnet_check,
)


class TestBuildOllamaClient:
    def test_returns_object_with_complete_method(self):
        config = MagicMock()
        config.ollama_base_url = "http://localhost:5050"
        client = _build_ollama_client(config)
        assert hasattr(client, "complete")

    @patch("agents_sdk.agents.skill_optimizer.httpx")
    def test_complete_calls_ollama_generate_endpoint(self, mock_httpx):
        mock_httpx.post.return_value.json.return_value = {"response": "YES"}
        mock_httpx.post.return_value.raise_for_status = MagicMock()
        config = MagicMock()
        config.ollama_base_url = "http://localhost:5050"
        client = _build_ollama_client(config)
        result = client.complete(prompt="test", model="qwen3-14b-research:latest", temperature=0.0, seed=0)
        assert result == "YES"
        # Verify URL pattern.
        call_args = mock_httpx.post.call_args
        assert "/api/generate" in call_args[0][0]


class TestRunStructuralChecks:
    def test_returns_per_prompt_per_run_results(self):
        outputs = {
            "p1": [{"text": "First paragraph " * 30 + ".\n\nSecond para.\n\nClose it."}],
            "p2": [{"text": "Too short.\n\nx."}],
        }
        baseline = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 3.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
            "_stdevs": {
                "sentence_length_mean": 2.0,
                "sentence_length_stdev": 1.0,
                "comma_density_per_100w": 1.5,
                "em_dash_density_per_100w": 0.5,
                "first_person_freq_per_100w": 1.0,
            },
            "_ngrams": [],
            "_threshold": 100.0,  # very lenient threshold
        }
        results = _run_structural_checks(outputs, baseline)
        assert "p1" in results and "p2" in results
        # p1's output has good first paragraph; p2's is too short → fails substack_format.
        assert results["p2"][0]["substack_format_intro"] is False


class TestRunJudge:
    def test_invokes_single_judge_for_non_ensemble_criterion(self):
        judge = MagicMock()
        judge.judge_single.return_value = MagicMock(passed=True)
        judge.judge_ensemble.return_value = MagicMock(passed=False)
        outputs = {"p1": [{"text": "x"}]}
        evals = {
            "training_prompts": [{"id": "p1", "prompt": "...", "mode": "sean"}],
            "holdout_prompts": [],
            "llm_judge_criteria": [
                {"id": "signature_move_present", "ensemble": False, "question": "?"},
                {"id": "sounds_like_sean", "ensemble": True, "n_judges": 3, "question": "?"},
            ],
        }
        anchors = {"sean": ["a", "b", "c", "d"]}
        results = _run_judge(judge, outputs, evals, anchors)
        # signature_move_present: True (single); sounds_like_sean: False (ensemble).
        assert results["p1"][0]["signature_move_present"] is True
        assert results["p1"][0]["sounds_like_sean"] is False


class TestSonnetCheck:
    def test_returns_agreement_rate(self):
        judge = MagicMock()
        # Judge returns True for the local sample, then compute_sonnet_agreement returns 0.8.
        judge.judge_single.return_value = MagicMock(passed=True)
        judge.compute_sonnet_agreement.return_value = 0.8
        outputs = {"p1": [{"text": "x"}, {"text": "y"}, {"text": "z"}]}
        evals = {
            "training_prompts": [{"id": "p1", "prompt": "...", "mode": "sean"}],
            "holdout_prompts": [],
            "llm_judge_criteria": [
                {"id": "sounds_like_sean", "ensemble": True, "n_judges": 3, "question": "Q"},
            ],
        }
        with patch("agents_sdk.agents.skill_optimizer._load_anchors") as mock_anchors:
            mock_anchors.return_value = {"sean": ["a", "b", "c", "d"]}
            agreement = _sonnet_check(judge, outputs, evals, sample_rate=1.0)
        assert agreement == 0.8
```

- [ ] **Step 2: Run tests to verify failure**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "BuildOllamaClient or RunStructuralChecks or RunJudge or SonnetCheck"`
Expected: FAIL — `NotImplementedError` raised.

- [ ] **Step 3: Implement the four helpers**

In `agents-sdk/agents/skill_optimizer.py`, add `import httpx` near the top imports (alongside `import yaml`).

Replace the four NotImplementedError stubs:

```python
import random as _random


class _OllamaClient:
    """Minimal Ollama HTTP client exposing a `.complete(...)` method matching JudgeRunner's protocol."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def complete(
        self,
        prompt: str,
        model: str = "qwen3-14b-research:latest",
        temperature: float = 0.0,
        seed: int = 0,
    ) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "seed": seed},
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]


def _build_ollama_client(config) -> _OllamaClient:
    base_url = getattr(config, "ollama_base_url", "http://localhost:5050")
    return _OllamaClient(base_url=base_url)


def _run_structural_checks(
    outputs: dict[str, list[dict]],
    baseline: dict,
) -> dict[str, list[dict[str, bool]]]:
    """Apply the 3 structural checks to every output. Returns results keyed by prompt_id."""
    threshold = baseline["_threshold"]
    results: dict[str, list[dict[str, bool]]] = {}
    for prompt_id, runs in outputs.items():
        results[prompt_id] = []
        for run in runs:
            text = run["text"]
            r1, _ = substack_format_intro(text)
            r2, _ = anti_pattern_overreference(text)
            r3, _ = stylometric_distance(text, baseline, threshold)
            results[prompt_id].append({
                "substack_format_intro": r1,
                "anti_pattern_overreference": r2,
                "stylometric_distance": r3,
            })
    return results


def _run_judge(
    judge: JudgeRunner,
    outputs: dict[str, list[dict]],
    evals: dict,
    mode_anchors: dict[str, list[str]],
) -> dict[str, list[dict[str, bool]]]:
    """Apply LLM-judge criteria to every output. Mixes single + ensemble judges per criterion config."""
    prompt_modes = {
        p["id"]: p["mode"]
        for p in (evals.get("training_prompts", []) + evals.get("holdout_prompts", []))
    }
    judge_criteria = evals["llm_judge_criteria"]

    results: dict[str, list[dict[str, bool]]] = {}
    for prompt_id, runs in outputs.items():
        results[prompt_id] = []
        mode = prompt_modes.get(prompt_id, "sean")
        anchors = list(mode_anchors.get(mode, []))
        if len(anchors) < 4:
            anchors.extend(mode_anchors.get("sean", []))
        anchors = anchors[:8]  # cap to keep token cost bounded

        for run in runs:
            text = run["text"]
            run_result: dict[str, bool] = {}
            for crit in judge_criteria:
                if crit.get("ensemble"):
                    er = judge.judge_ensemble(
                        output=text,
                        anchors=anchors,
                        question=crit["question"],
                        mode=mode,
                        n_judges=crit.get("n_judges", 3),
                    )
                    run_result[crit["id"]] = er.passed
                else:
                    jr = judge.judge_single(
                        output=text,
                        anchors=anchors[:2],
                        question=crit["question"],
                        mode=mode,
                    )
                    run_result[crit["id"]] = jr.passed
            results[prompt_id].append(run_result)
    return results


def _sonnet_check(
    judge: JudgeRunner,
    outputs: dict[str, list[dict]],
    evals: dict,
    sample_rate: float = 0.10,
) -> float:
    """Re-judge a `sample_rate` fraction of outputs with Sonnet on the most-subjective criterion.

    Returns the agreement rate (1.0 = perfect agreement, 0.0 = total disagreement).
    Uses `sounds_like_sean` as the canonical subjective criterion per spec.
    """
    flat: list[tuple[str, str]] = []
    for prompt_id, runs in outputs.items():
        for run in runs:
            flat.append((prompt_id, run["text"]))
    if not flat:
        return 1.0

    sample_n = max(1, int(len(flat) * sample_rate))
    sample = _random.sample(flat, sample_n)

    sounds_q = next(
        (c["question"] for c in evals["llm_judge_criteria"] if c["id"] == "sounds_like_sean"),
        None,
    )
    if not sounds_q:
        return 1.0

    anchors_by_mode = _load_anchors()
    prompt_modes = {
        p["id"]: p["mode"]
        for p in (evals["training_prompts"] + evals.get("holdout_prompts", []))
    }

    local_results: list[bool] = []
    sample_outputs: list[str] = []
    sample_anchors: list[list[str]] = []
    for prompt_id, text in sample:
        mode = prompt_modes.get(prompt_id, "sean")
        anchors = anchors_by_mode.get(mode, anchors_by_mode.get("sean", []))[:2]
        local_jr = judge.judge_single(text, anchors, sounds_q, mode)
        local_results.append(local_jr.passed)
        sample_outputs.append(text)
        sample_anchors.append(anchors)

    return judge.compute_sonnet_agreement(
        outputs=sample_outputs,
        anchors_per_output=sample_anchors,
        question=sounds_q,
        mode="sean",
        local_results=local_results,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/test_skill_optimizer.py -v -k "BuildOllamaClient or RunStructuralChecks or RunJudge or SonnetCheck"`
Expected: 6 PASS

- [ ] **Step 5: Run full pytest suite to confirm nothing regressed**

Run: `cd agents-sdk && PYTHONPATH=. pytest tests/ -v`
Expected: all PASS (~70+ unit tests across all modules).

- [ ] **Step 6: Commit**

```bash
git add agents-sdk/agents/skill_optimizer.py agents-sdk/tests/test_skill_optimizer.py
git commit -m "feat(skill_optimizer): implement external-call helpers (ollama_client, structural_checks runner, judge runner, sonnet_check)"
```

---

> **Pause point: Phase 4 complete.** Run `cd agents-sdk && PYTHONPATH=. pytest tests/ -v` — all tests pass. The agent is wired but has not yet been run live.

---

## Phase 5 — Integration Validation + Docs + First Live Run

### Task 5.1: End-to-end dry-run

**Files:**
- N/A (validation only)

- [ ] **Step 1: Run the dry-run mode**

Run: `cd agents-sdk && PYTHONPATH=. python3 agents/skill_optimizer.py --dry-run`
Expected: Loop runs through 1-3 iterations using `_DummyClient`, writes results.tsv, no API calls made.

- [ ] **Step 2: Inspect results.tsv**

Run: `head -3 agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv`
Expected: header row + at least 1-3 data rows. All TSV-escaped, all columns populated.

- [ ] **Step 3: Verify no live commits were created during dry-run**

Run: `git log --oneline | head -3`
Expected: only Phase 0-4 commits visible. No `optimize(writing-voice-modes)` commits.

- [ ] **Step 4: Delete the dry-run results.tsv to start fresh**

Run: `rm agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv`

---

### Task 5.2: First live optimization run

**Files:**
- Generated: `agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv`
- Modified (by the loop itself): `.claude/skills/writing-voice-modes/SKILL.md`

> **This is the production run. Estimated 9-13 hours wall-clock. Run overnight or during a long focus block. Cost cap $200, expected $50-145.**

- [ ] **Step 1: Verify Mac Mini Ollama is reachable**

Run: `curl -sS http://localhost:5050/api/tags | head -c 200`
Expected: JSON with `qwen3-14b-research:latest` in the model list.

- [ ] **Step 2: Verify ANTHROPIC_API_KEY is set**

Run: `python3 -c "import os; print('ok' if os.environ.get('ANTHROPIC_API_KEY') else 'MISSING')"`
Expected: `ok`

- [ ] **Step 3: Launch the run**

Run: `cd agents-sdk && PYTHONPATH=. python3 agents/skill_optimizer.py 2>&1 | tee data/skill-optimizer/run.log`
Expected: each iteration logs mutation summary, scores, decision. Halts on success / plateau / tripwire / iteration cap.

- [ ] **Step 4: Periodically inspect**

Run (in another terminal, every 30-60 minutes): `tail -1 agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv`

- [ ] **Step 5: Post-run review**

Once halted, read the full results.tsv. Identify:
  - Best score reached
  - Number of kept mutations
  - Tripwires triggered (if any)
  - Sections that produced kept improvements
  - Any failed mutations that were rejected by the guard

---

### Task 5.3: Post-run docs (CHANGELOG + CLAUDE + README)

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Append CHANGELOG entry**

In `CHANGELOG.md`, under the current version's Added section, append:
```markdown
- **skill_optimizer.py — autoresearch optimization harness for Claude Code skills**
  Adapted from Karpathy's autoresearch pattern. One-skill prototype validated against
  `.claude/skills/writing-voice-modes/SKILL.md`. Hybrid eval suite (3 deterministic
  structural checks + 3 LLM-judge criteria with 3-judge majority vote on subjective ones)
  with held-out validation set + sealed surprise prompts to prevent Goodhart drift.
  6 anti-Goodhart trip-wires + bootstrap-CI keep/revert + moving-average decision rule.
  Generation: Opus 4.7. Judge: Qwen3-14B local with Sonnet 4.6 sample-check every
  5 iterations. Pre-flight: stylometric baseline from voice-samples.md + ROC-tuned threshold.
  Branch: `autoresearch/writing-voice-modes-2026-05-09`. Result: <fill in score and brief outcome>.
```

- [ ] **Step 2: Update CLAUDE.md agent table**

In `CLAUDE.md`, find the "Active agents" table and add:
```markdown
| Skill Optimizer (NEW, **manual-trigger only**) | manual | Opus 4.7 generation + Qwen3-14B judge + Sonnet sample-check; autoresearch loop on a single skill | $50-145/run |
```

Also update agent count in the opening paragraph (currently "14 autonomous SDK agents (7 active)" — bump to "(8 active)" or note the manual-only status as appropriate).

- [ ] **Step 3: Update README.md counts if any**

Search README.md for skill/agent counts and update.

- [ ] **Step 4: Final commit**

```bash
git add CHANGELOG.md CLAUDE.md README.md
git commit -m "docs: skill_optimizer + writing-voice-modes autoresearch run results"
```

- [ ] **Step 5: Open PR from autoresearch branch → main**

Run:
```bash
gh pr create --title "skill_optimizer: writing-voice-modes autoresearch run" --body "$(cat <<'EOF'
## Summary
- New skill_optimizer.py harness (one-skill prototype)
- Optimized writing-voice-modes SKILL.md across N kept iterations
- Final score: X.XX / 1.0 (target 0.75)

## Test plan
- [ ] Inspect results.tsv for kept mutations
- [ ] Spot-check 3 generations per mode against the optimized skill body
- [ ] Verify no protected sections were modified
- [ ] Run pytest suite green (`cd agents-sdk && PYTHONPATH=. pytest tests/ -v`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Self-Review

**Spec coverage:**
- [✓] Section 4.1 (10 test prompts) → Task 3.1 + 3.2
- [✓] Section 4.2 (criteria) → Tasks 1.1, 1.2, 1.5 (structural) + 2.1-2.3 (judge)
- [✓] Section 4.3 (scoring) → Task 4.3 + evals.yaml
- [✓] Section 5 (mutation policy) → Task 1.6 + program.md (Task 3.3)
- [✓] Section 6 (judge prompt) → Task 3.4
- [✓] Section 7 (stylometric distance) → Tasks 1.3-1.5 + 3.5-3.6
- [✓] Section 8.1 (decision rule) → Task 1.7
- [✓] Section 8.2 (6 trip-wires) → Task 1.8
- [✓] Section 9 (data flow) → Task 4.6
- [✓] Section 10 (branch + git) → Tasks 0.1, 4.4
- [✓] Section 11 (pre-flight) → Tasks 0.2, 3.5, 3.6
- [✓] Section 12 (file manifest) → all phases collectively
- [✓] Section 13 (config.toml) → Task 0.4
- [✓] Section 14 (results.tsv) → Task 4.5
- [✓] Section 15 (open questions/risks) → trip-wires (Task 1.8) + dry-run (Task 5.1)
- [✓] Section 16 (success criteria) → validated by Task 5.2 post-run review

**Placeholder scan:** No "TBD", "TODO", "implement later", "fill in details" present in steps. The 12 helper-stub functions in Task 4.6 are an explicit checklist (each stub gets its own mini-test + implementation), not vague "implement later" references — they have a clear pattern shown by the `_plateau` example.

**Type consistency:** `JudgeResult`, `EnsembleResult`, `IterationSnapshot`, `SkillOptimizerConfig`, `MutationRejected` are referenced consistently across tasks. Function names match between definition and import sites.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-09-writing-voice-modes-autoresearch.md`. Two execution options:

**1. Subagent-Driven (recommended)** — fresh subagent per task with two-stage review between tasks. Best for plans of this size (30 tasks across 5 phases) because the main session stays clean and per-task subagents catch their own typos before merging back.

**2. Inline Execution** — execute tasks in this session using `superpowers:executing-plans`. Faster end-to-end but the main context fills up.

Which approach?
