# Autoresearch Program — Phase 0: Gemini NB2 Walk Cycle Optimization

You are optimizing Gemini NB2 sprite sheet generation for walk_forward animations.
The goal: produce walk cycles where legs show distinctly different positions across frames,
following the Contact→Down→Passing→Up progression of real arcade fighter walk cycles.

## Rules
- NEVER modify prepare.py or the scoring pipeline
- ALWAYS use the same character (Sean) and seed for comparability
- ALWAYS include 3 anchor images (Golden Rule — enforced with RuntimeError)
- Log every experiment to results.tsv: experiment_id, params_changed, scores, generation_time, timestamp
- Commit successful improvements to git immediately
- If score decreases, revert experiment.json and try next direction
- Budget: ~$0.07 per experiment. Stop after 100 experiments or $7 total.

## Strategy (work through in order)

### Round 1: Prompt Structure (experiments 1-20)
1. Baseline: run current prompt, record score
2. Add explicit pose names per frame: "Frame 1: Contact pose — right heel strikes ground,
   left leg trails behind, arms at maximum spread"
3. Try pose-by-pose prompt (describe each frame separately) vs. sheet-level prompt
4. Add animation terminology: "walk cycle", "contact pose", "passing position",
   "weight transfer", "push-off"
5. Try adding "each frame must show a DISTINCTLY DIFFERENT leg position"

### Round 2: Reference Strategy (experiments 21-40)
6. Test with 1 anchor vs 2 vs 3 (is more always better?)
7. Add a reference walk cycle sprite sheet alongside anchors
8. Add a pose reference diagram showing contact/passing/up/down positions
9. Test anchor + style ref (full SF2 sprite sheet from another character)

### Round 3: Sheet Layout (experiments 41-60)
10. Try 2-frame pair generation (generate frames 1-2, then 3-4, etc.)
11. Try individual frame generation with heavy anchor conditioning
12. Try generating 6 keyframes instead of 4 for HYBRID walk cycles
13. Try 8 keyframes (more distinct poses for RIFE to interpolate)

### Round 4: Negative Prompts + Constraints (experiments 61-80)
14. Add "legs must be in different positions in every frame"
15. Add "no repeated poses"
16. Add 2D animation principle constraints: "body lowest at frame 2, highest at frame 4"
17. Test combination of best findings from Rounds 1-3

### Round 5: Fine-Tuning Best Configuration (experiments 81-100)
18. Take the best-scoring configuration and make small variations
19. Try the winning approach on walk_backward
20. Try on a second character (Aria) to confirm generalization
