# Phase 4 Completion Summary — 16BitFit Battle Mode

**Date:** 2026-04-02
**Phase:** 4 of 5 (LoRA + Memory Layer)
**Duration:** Single session build

---

## Task Results

| # | Task | Status | Details |
|---|------|--------|---------|
| 0a | RIFE adapter swap | **PASS** | `RIFEAdapter` created with rife49.pth, `GMFSSAdapter` aliased for backward compat, workflow JSON updated, strategy router supports `rife` and `gmfss` backends |
| 0b | SOURCE-OF-TRUTH update | **PASS** | Phase 3 GMFSS task marked resolved, Open Question #2 updated with RIFE VFI confirmation |
| 1 | Vault Embedding Indexer | **PASS** | Dry-run discovered 274 vault files, SQLite schema ready, incremental indexing, nomic-embed-text on Mac Mini. Launchd plist: 2:00 AM nightly |
| 2 | Preserve Session | **PASS** | Dry-run auto-detected latest session log, structured output template, on-demand trigger via `--baton-file` or auto-detect |
| 3 | PR Digest | **PASS** | Dry-run shows 3 repos configured, gh CLI integration (needs `gh auth login`). Launchd plist: 8:00 AM daily |
| 4 | RIFE → Pixel Quantizer | **PASS** | **87.6% overall, 96.4% palette, 0 off-palette pixels, 100% outline coverage.** Pixel Quantizer fully cleans RIFE color expansion. |
| 5 | Wan 2.2 + LoRA | **PASS** | Both no-LoRA and with-LoRA (pixel-000020, strength 0.85) workflows executed on Alienware. ~21-31s per generation. Visual comparison pending Sean review. |
| 6 | Stronger motion prompts | **PASS** | All 3 prompt variants (step-by-step, foot alternation, locomotion) executed on Alienware. Visual comparison pending Sean review. |
| 7 | PixelLab v3 evaluation | **PASS** | **PixelLab HAS a public API** with Python SDK. Pay-per-use ($0.007-$0.016/gen). "Animate with Skeleton" + "Estimate Skeleton" endpoints. Max 128×128. Viable for pipeline integration. |
| 8 | kohya_ss config | **PASS** | Training TOML created: Adafactor, SDPA, rank 32, Illustrious XL v0.1, fused backward pass, bf16 |
| 9 | Dataset prep script | **PASS** | Script runs, nearest-neighbor upscale confirmed sharp (verified pixel identity), auto-captioning with trigger word |
| 10 | Training runbook | **PASS** | Complete step-by-step: prerequisites, dataset prep, training launch, monitoring, ComfyUI testing, troubleshooting table |

---

## Animation Quality Comparison Table

| Source | Overall | Palette | Outline | BG Purity | Character | Gate |
|--------|---------|---------|---------|-----------|-----------|------|
| Raw NB2 Keyframes | 77.7% | 100% | — | — | — | PASS |
| Wan 2.2 5B (Phase 3) | 73.7% | 84.0% | — | — | — | PASS |
| **RIFE VFI → Quantizer** | **87.6%** | **96.4%** | **100%** | **75.0%** | **80.9%** | **PASS** |

**Key finding:** RIFE VFI through the Pixel Quantizer scores HIGHER than both raw keyframes and Wan 2.2. The quantizer perfectly handles RIFE's color expansion (79K-103K unique colors → 0 off-palette pixels).

---

## Video Model Strategy Recommendation

1. **Walk cycles (primary):** NB2 multi-keyframe → RIFE VFI 4x → Pixel Quantizer (87.6%, best quality)
2. **Idle/subtle motion:** Wan 2.2 5B ti2v from single keyframe (73.7%, adequate for pose animation)
3. **Wan 2.2 + LoRA:** Workflow confirmed working. Visual quality delta pending Sean's review of Alienware outputs.
4. **PixelLab API:** New option for programmatic animation. $0.007-$0.016/gen, supports 128×128. Build `PixelLabAdapter` behind `VideoModelAdapter` interface in Phase 5.
5. **Stronger motion prompts:** All 3 variants ran successfully. The 5B model may still produce idle bounce — visual inspection needed.

---

## Agent Fleet Status (8 agents)

| # | Agent | Machine | Model | Schedule | Status |
|---|-------|---------|-------|----------|--------|
| 1 | Daily Driver | Mac Mini | Claude Sonnet | 6:00/17:00/Fri 16:00 | Active |
| 2 | Process Inbox | Mac Mini | phi4-mini-reasoning | 5:30 AM | Active |
| 3 | Spending Analysis | MacBook Pro | Qwen3-14B | On-demand | Active |
| 4 | Sprint Health | API | Claude Sonnet | Friday 15:00 | Active |
| 5 | Meeting Defender | Mac Mini + API | phi4-mini + Haiku | Monday 07:00 | Active |
| 6 | **Vault Indexer** | Mac Mini | nomic-embed-text | **Nightly 02:00** | **NEW** |
| 7 | **Preserve Session** | MacBook Pro | Qwen3-14B | **On-demand** | **NEW** |
| 8 | **PR Digest** | MacBook Pro | Qwen2.5-Coder-32B | **Daily 08:00** | **NEW** |

---

## What You Need to Do Manually Before Phase 5

### Must-do (blocks Phase 5)

1. **Install launchd plists** for new agents on Mac Mini:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.vault-indexer.plist ~/Library/LaunchAgents/
   cp agents-sdk/schedules/com.sean.agent.pr-digest.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.vault-indexer.plist
   launchctl load ~/Library/LaunchAgents/com.sean.agent.pr-digest.plist
   ```

2. **Install `gh` CLI and authenticate** (needed for PR Digest):
   ```bash
   brew install gh && gh auth login
   ```

3. **Review Alienware video outputs** — visually compare:
   - Test 5a (no LoRA) vs 5b (with LoRA) — does the LoRA improve pixel art quality?
   - Tests 6a/6b/6c — do any stronger prompts produce actual locomotion vs idle bounce?

4. **Collect 30-50 training images** for the custom LoRA — SF2-style sprites, various poses

5. **Download Illustrious XL v0.1 on Alienware:**
   ```powershell
   huggingface-cli download OnomaAIResearch/Illustrious-xl-early-release-v0 --local-dir C:\Users\seanw\Documents\Code-Brain\models
   ```

6. **Install kohya_ss dev branch on Alienware:**
   ```powershell
   cd C:\Users\seanw\Documents\Code-Brain
   git clone -b dev https://github.com/bmaltais/kohya_ss.git
   cd kohya_ss && gui-uv.bat
   ```

### Should-do (Phase 5 enhancements)

7. **Build `PixelLabAdapter`** behind `VideoModelAdapter` interface — PixelLab has a public API at $0.007-$0.016/gen, supports 128×128, skeleton-based animation
8. **Test FILM VFI** as RIFE backup — same node pack, slightly more ghosting
9. **Run vault indexer live** (not just dry-run) once Mac Mini Ollama has nomic-embed-text

---

## Open Questions for SOURCE-OF-TRUTH.md

1. **Wan 2.2 + LoRA quality delta** — Visual comparison pending. Does pixel-000020 LoRA improve over baseline?
2. **Stronger motion prompts vs idle bounce** — Do any of the 3 prompt variants produce real locomotion from the 5B model?
3. **PixelLab API for production** — At $0.007-$0.016/gen with 128×128 max, is it cost-effective at scale (900-1400 frames)?
4. **Custom LoRA quality** — Will the 16bitfit_style LoRA trained on Illustrious XL v0.1 improve sprite consistency enough to reduce retries?

---

## Files Created/Modified

### New Files

| File | Purpose |
|------|---------|
| `agents-sdk/agents/vault_indexer.py` | Vault Embedding Indexer (Mac Mini, nomic-embed-text, SQLite) |
| `agents-sdk/agents/preserve_session.py` | Preserve Session (MacBook Pro, Qwen3-14B, on-demand) |
| `agents-sdk/agents/pr_digest.py` | PR Digest (MacBook Pro, Qwen2.5-Coder-32B, daily 8AM) |
| `agents-sdk/schedules/com.sean.agent.vault-indexer.plist` | launchd: nightly 2:00 AM |
| `agents-sdk/schedules/com.sean.agent.pr-digest.plist` | launchd: daily 8:00 AM |
| `video-eval/workflows/rife_interpolation.json` | RIFE VFI ComfyUI workflow (replaces GMFSS) |
| `video-eval/run_phase4_tests.py` | Phase 4 video test harness (Tasks 5 & 6) |
| `video-eval/eval-results/rife-quantized/` | 5 RIFE frames through full Pixel Quantizer |
| `video-eval/eval-results/phase4-video-test-results.json` | Video test results |
| `lora-training/sprite-style-config.toml` | kohya_ss training config |
| `lora-training/sample_prompts.txt` | Training sample prompts |
| `lora-training/prepare_dataset.py` | Dataset preparation script |
| `lora-training/TRAINING-RUNBOOK.md` | Step-by-step training guide |

### Modified Files

| File | Change |
|------|--------|
| `agents-sdk/config.toml` | Added vault_indexer and pr_digest agent configs |
| `video-eval/adapters.py` | Replaced GMFSSAdapter with RIFEAdapter (+ backward-compat alias) |
| `video-eval/strategy_router.py` | Added `rife` interpolation backend, imports RIFEAdapter |
| `SOURCE-OF-TRUTH.md` | Updated Phase 3 GMFSS resolution, Open Question #2, last-updated date |

---

## Self-Check Validation

| # | Check | Result |
|---|-------|--------|
| 1 | `claude-agent-sdk` and `ClaudeAgentOptions` everywhere | YES — lazy imports in preserve_session.py |
| 2 | Credentials via keychain.py only | YES — no .env in any agent |
| 3 | Vault Embedding Indexer 100% local (Mac Mini + nomic-embed-text) | YES — $0.00 budget, routes to 192.168.68.200 |
| 4 | Preserve Session 100% local (MacBook Pro + Qwen3-14B) | YES — $0.00 budget, localhost |
| 5 | PR Digest 100% local (MacBook Pro + Qwen2.5-Coder-32B) | YES — $0.00 budget, gh CLI |
| 6 | Swapped GMFSS Fortuna → RIFE VFI | YES — RIFEAdapter with rife49.pth, GMFSSAdapter = alias |
| 7 | Used Wan 2.2 (NOT Wan 2.5) | YES — wan2.2_ti2v_5B_fp16.safetensors |
| 8 | Used SDPA (NOT xformers) in Alienware configs | YES — xformers=false, sdpa=true in training config |
| 9 | LoRA training config uses Illustrious XL v0.1 | YES — OnomaAIResearch/Illustrious-xl-early-release-v0 |
| 10 | LoRA training config uses Adafactor + rank 32 | YES — optimizer_type="Adafactor", network_dim=32 |
| 11 | Ran real RIFE output through full Pixel Quantizer | YES — 5 frames, 0 off-palette, 87.6% overall |
| 12 | All new adapters behind VideoModelAdapter interface | YES — RIFEAdapter extends VideoModelAdapter ABC |
| 13 | All new agents have config.toml entries | YES — vault_indexer and pr_digest added |
| 14 | Launchd plists for Vault Indexer + PR Digest | YES — nightly 2AM and daily 8AM |
