# LLM Council

Multi-vendor LLM "council" critique for in-session use from Claude Code.

**Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council).** Karpathy's reference web app lives unmodified at [`upstream/`](upstream/) as both a working browser-based council and visible attribution. Our headless Python CLI in [`council/`](council/) implements the same three-stage pipeline (fan-out → cross-rank → chairman) for invocation from inside Claude Code sessions via the [`llm-council` skill](../../.claude/skills/llm-council/).

## Quick start

```bash
# From the superuser-pack root (where .env lives):
cd tools/llm-council
uv sync
uv run python -m council --profile variance \
    --prompt-file /tmp/your-prompt.md \
    --output /tmp/council-output.md \
    --tag your-tag
```

Output is a markdown file with: original prompt, four named responses, cross-rank table, chairman synthesis, cost summary.

## Profiles

Two profiles defined in [`council/profiles.py`](council/profiles.py):

- **premium** — four frontier models, judging flat-out. Use for high-stakes synthesis (job-hunt artifacts, decision pre-mortems).
- **variance** — four models with maximally different RLHF lineages. Use when divergence is the signal (voice-mode calibration, prompt-clarity tests).

Final model IDs and cost caps are documented in [`model-selection-2026-05-14.md`](model-selection-2026-05-14.md).

## Karpathy's browser app

Want to use the original web UI?

```bash
cd upstream
uv sync && cd frontend && npm install && cd ..
# Symlink to root .env (one-time):
ln -sf ../../.env .env
./start.sh
```

Then open http://localhost:5173.

## License + credit

Karpathy's code in `upstream/` is MIT-licensed (see `upstream/LICENSE`). Our `council/` package is also MIT, with full attribution in source and README. We do not maintain `upstream/` — if it breaks against an OpenRouter API change, we fix our CLI and treat the upstream as a frozen reference.
