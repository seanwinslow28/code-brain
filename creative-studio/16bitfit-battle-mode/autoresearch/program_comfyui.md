# Autoresearch Program — Phase 1: ComfyUI Walk Cycle Optimization

You are optimizing a ComfyUI sprite generation workflow for walk_forward animations.
The goal: beat Gemini NB2's 0.8448 best score and break the 0.80 VLM walk-score ceiling
by using **explicit pose guidance** (ControlNet OpenPose on 4 Ryu-walk-cycle skeletons)
and **identity lock** (IP-Adapter FaceID on 3 character anchors) — instead of hoping a
text prompt produces 4 distinct leg positions like in Phase 0.

All experiments run on the Alienware RTX 5080 at `http://192.168.68.201:8188`. Cost is $0.

## Rules
- NEVER modify `prepare.py` or the scoring pipeline (frozen scorer).
- ALWAYS use the same character (Sean), same 3 anchor images, same 4 Ryu pose skeletons.
- ALWAYS fix the seed per trial for direct A/B comparison.
- Each trial = one queued workflow generating all 4 walk frames → one composite sprite sheet → one score.
- Log every experiment to `results/phase1/experiment_log.jsonl` with full params + all sub-scores.
- Git-commit any trial that beats the current best score (`best_experiment.json`).
- If a trial scores worse, revert `experiment.json` to the current best and move on.
- Per-trial timeout: 120s. Kill ComfyUI job on timeout, mark trial FAIL, continue.
- Pre-flight: GET `/system_stats` before each run; bail if Alienware unreachable.
- Before any run, verify VPN (utun4) is OFF — it silently blocks LAN access to Alienware.
- No network calls leave the LAN. No Gemini API calls in Phase 1.

## Base Stack (locked unless a round says otherwise)

- **Checkpoint:** `illustriousXL_v3.6` (SDXL-scale, 6–8GB VRAM, big LoRA ecosystem).
- **LoRA pool (Round 3 rotates through these):**
  - `SF3XL` (YeiyeiArt, trained on real SF3 sprites — primary)
  - `SpaceCandy_SpriteSheet_v1_ILXL` (purpose-built for frame consistency)
  - `FightingSprites_ILXL` (Jan 2026, fighting-game action poses)
- **IP-Adapter:** FaceID Plus V2 (cubiq, 3 anchors, 224×224 square/centered).
- **ControlNet:** `thibaud/controlnet-openpose-sdxl-1.0` (the xinsir fork has known
  ComfyUI loading bugs — use thibaud).
- **Pose inputs:** `references/pose_skeletons/ryu_walk_{contact,down,passing,up}.png`
  extracted from a real SF2 Ryu walk cycle via DWPose preprocessor.

## Strategy (work through in order)

### Round 1 — LoRA Strength Sweep (trials 1–20)
Lock IP-Adapter weight 0.6, ControlNet 0.7, SF3XL LoRA, CFG 7, DPM++ 2M Karras, 25 steps.
Sweep `lora_strength` across 0.3–0.9. Find the strength ceiling before SF3 style breaks.
Hypothesis: sweet spot is 0.4–0.6 (community data says high LoRA fights ControlNet).

### Round 2 — ControlNet Strength Sweep (trials 21–40)
Lock the winning LoRA strength from Round 1. Sweep `cn_strength` 0.4–1.0.
Hypothesis: stronger CN = better leg differentiation (the core Phase 0 bottleneck) but
too strong produces stiff, uncanny poses.

### Round 3 — LoRA Comparison (trials 41–70)
Hold best strengths from R1/R2. Swap LoRAs: SF3XL → SpaceCandy → FightingSprites.
Goal: confirm SF3XL is best, or discover a surprise winner. Score each LoRA over 10 trials
with different seeds so we're not fooled by seed luck.

### Round 4 — Optuna TPE Joint Search (trials 71–110)
Warm-start Optuna with the top 5 trials from R1–R3 as prior observations. Now let TPE
explore all parameters jointly:
- `lora_strength` (0.3–0.9), `cn_strength` (0.4–1.0), `ipa_weight` (0.3–0.9)
- `cfg` (5–10), `steps` (20–35)
- `sampler` {dpmpp_2m, dpmpp_2m_sde, euler_a}, `scheduler` {karras, normal}

Log the ratio `lora_strength / cn_strength` for each trial — high-scoring trials should
cluster along a diagonal in the LoRA×CN plane.

### Round 5 — Generalization & Seed Variance (trials 111–150)
Take the top 3 configs. Run each with 10 different seeds to measure variance (Phase 0
showed baseline variance was 0.615–0.834 — seed luck matters). Then run the single best
config on:
- walk_backward (Sean) — does it generalize to the mirrored animation?
- walk_forward on a second character (Aria) with her anchors — does it generalize across identity?

## Gate Checks

- **After Round 2:** If no trial beats Phase 0's 0.8448 → pause and ask Sean before continuing.
  The hypothesis (ControlNet fixes leg differentiation) may be wrong.
- **After Round 4:** If best VLM walk-score still ≤ 0.80 → ControlNet isn't the ceiling-breaker
  we thought. Flag for a plan revision before Round 5.
- **End of run:** Write `results/phase1/summary.md` with: best config, score vs Phase 0,
  VLM rubric breakdown (especially leg_differentiation and weight_shift — the two Phase 0
  bottlenecks), and a "Phase 0 vs Phase 1 winner" recommendation.

## Safety Constraints

- Max trials: 150 (or whenever R5 completes).
- Max runtime: 8 hours wallclock.
- Per-trial timeout: 120s (kill ComfyUI job, mark FAIL).
- GPU temp guard: pause if Alienware GPU > 85°C for > 60s.
- Disk guard: stop if Alienware has < 10GB free.
- Budget: $0.00 API, $0.00 compute (local GPU only). No Gemini escalation in Phase 1 —
  the borderline VLM cases still go to Gemini 2.5 Flash per `prepare.py`, capped at $0.50.

## What to NOT do

- Do NOT re-introduce walk-cycle *reference images* as IP-Adapter input. Phase 0 proved
  they hurt scores. Only pose *skeletons* via ControlNet.
- Do NOT sweep 3+ parameters simultaneously in Rounds 1–3. Phase 0 showed multi-param
  combos collapse quality. Jointly search only in Round 4 with TPE.
- Do NOT train a new LoRA. The LoRA path was abandoned April 8. Only use the three
  community LoRAs listed above.
- Do NOT modify anchor images or pose skeletons mid-run — they are frozen inputs.
