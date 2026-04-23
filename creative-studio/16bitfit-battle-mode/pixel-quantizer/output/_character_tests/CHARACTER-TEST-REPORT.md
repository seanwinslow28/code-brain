# Character Sprite Sheet Test Report — 2026-04-09

**Test:** Single sprite sheet per character (6 poses in 3x2 grid)
**Model:** Gemini 3.1 Flash Image Preview (Nano Banana 2)
**Result:** 12/12 PASS — all characters generated with strong identity consistency

---

## What Worked

### Anchor Image Conditioning (the breakthrough)

The single most important fix in Phase 5. Every Gemini API call now includes the character's 3 anchor reference PNGs as inline image data alongside the text prompt. This is a **multi-modal request** — Gemini sees the reference images and generates output that matches them.

**Before (text-only prompts):** Each frame produced a completely different character — different hair, skin tone, clothing, body type. Gemini interpreted "muscular build, blonde hair, white tank top" differently every time. Unusable for animation.

**After (anchor images + text):** Character identity is stable across all 6 poses in every sheet. Same hair, same clothing, same palette, same proportions. The reference images anchor Gemini's generation to a specific visual identity.

**Why it works:** Large multimodal models like Gemini are much better at "generate something that looks like THIS" (image conditioning) than "generate something matching this description" (text-only). The anchors eliminate ambiguity — there's only one way to interpret "this exact character."

**Golden Rule established:** Every Gemini generation request MUST include anchor reference images. The `GeminiAdapter` now raises a `RuntimeError` if `anchor_images` is empty. This is enforced in code, not just convention.

### Sprite Sheet Prompt Format

Requesting a 3x2 grid of poses in a single generation produced better results than generating individual frames. Gemini maintained character consistency across cells within the same sheet because it's generating one coherent image, not 6 independent ones.

The prompt structure that worked:
1. Reference to "THIS EXACT CHARACTER from the reference images"
2. Explicit pose descriptions for each cell position
3. Style tokens: "SF2 pixel art, bold #272929 dark outlines, clean pixel edges"
4. Green screen: "solid #00FF00 green for each cell"
5. Facing: "Character facing RIGHT in every pose"
6. Negatives: "No anti-aliasing, no gradients, no background scenery"

### Non-Humanoid Characters

The bosses with non-standard body types (Procrastination Phantom's spectral tail, Sloth Demon's beast form, Training Dummy's mechanical construction) all generated correctly. Gemini extracts the visual identity from the anchor images regardless of body type — it doesn't need the character to be humanoid.

### Retry Logic

Exponential backoff (5s, 15s, 30s) for Gemini 503/429 errors. During the full 12-character run, zero retries were needed — the 10-second inter-character delay was sufficient to stay under rate limits.

---

## What Didn't Work (in earlier runs)

### Text-Only Prompts (no anchor images)

The first batch run generated 60 frames for Sean with zero character consistency. Every frame was a different person. The text description "muscular build, blonde hair, white tank top, blue pants, white shoes" is too ambiguous for Gemini to produce the same character twice.

**Lesson:** Never rely on text descriptions alone for character identity. Always condition on reference images.

### Gemini `responseMimeType: "image/png"`

The initial GeminiAdapter included `responseMimeType: "image/png"` in the generation config. This is not a valid option — Gemini only accepts `text/plain`, `application/json`, etc. for `responseMimeType`. Image output is controlled by `responseModalities: ["IMAGE", "TEXT"]` instead.

**Fix:** Removed `responseMimeType` entirely. Gemini returns JPEG by default when IMAGE modality is requested.

### Gemini 503 Rate Limiting

After ~8 rapid sequential API calls, Gemini returns 503 Service Unavailable. The first batch run had no retry logic and failed immediately on 503.

**Fix:** Added 3-retry loop with 5/15/30 second backoff. The test script also adds 10 seconds between characters.

### Stale RIFE Workflow JSON (HYBRID animations)

All 5 HYBRID animations (walk_forward, walk_backward, jump, heavy_kick, special_move) failed because the RIFE VFI ComfyUI workflow was missing required inputs. The Alienware's ComfyUI node pack was updated since Phase 4, adding new required fields:
- `RIFE VFI` node: `dtype`, `scale_factor`, `torch_compile`, `batch_size`, `fast_mode`, `ensemble`
- `VHS_VideoCombine` node: `save_output`, `pingpong`, `loop_count`

**Fix:** Updated `rife_interpolation.json` with all required fields queried from the live Alienware ComfyUI at `192.168.68.201:8188/object_info/RIFE%20VFI`. Note: the VHS_VideoCombine node in the workflow was replaced with SaveImage (which doesn't need those fields), but the RIFE node fix was the critical one.

### Output Resolution

Gemini ignores pixel dimension requests in text prompts ("Generate a 128x128 sprite"). Output images are typically 512x512 or larger. This is expected — the Pixel Quantizer's first step is nearest-neighbor downscale to the target tile size.

---

## Per-Character Results

### Champions (128x128)

| Character | Poses | Consistency | Style Match | Identity | Green Screen |
|-----------|-------|-------------|-------------|----------|--------------|
| Sean | 8/8 | Strong | SF2 pixel art | Blonde hair, white tank, blue pants | Clean |
| Aria | 8/8 | Strong | SF2 pixel art | Brown ponytail, purple crop top, jeans | Clean |
| Kenji | 8/8 | Strong | SF2 pixel art | Black bun, gray gi, dark pants | Clean |
| Marcus | 8/8 | Strong | SF2 pixel art | Dark skin, yellow boxing gloves, gray tank | Clean |
| Mary | 6/6 | Strong | SF2 pixel art | Purple headband, purple sports bra/shorts | Clean |
| Zara | 6/6 | Strong | SF2 pixel art | Low bun, dark gray tank, cargo pants | Clean |

### Bosses (256x256)

| Character | Poses | Consistency | Style Match | Identity | Green Screen |
|-----------|-------|-------------|-------------|----------|--------------|
| Gym Bully | 6/6 | Strong | SF2 pixel art | Sunglasses, olive tank, red wristbands | Clean |
| Procrastination Phantom | 6/6 | Strong | Unique (ghostly) | White hoodie, spectral tail, no legs | Clean |
| Sloth Demon | 6/6 | Strong | Unique (beast) | Brown fur, gray armor, yellow eyes | Clean |
| Stress Titan | 8/8 | Strong | SF2 pixel art | Gray skin, black/orange power suit | Clean |
| Training Dummy | 6/6 | Strong | SF2 pixel art | Metal face plate, leather straps, bolts | Clean |
| Ultimate Slump | 6/6 | Strong | SF2 pixel art | Pale skin, long dark hair, hunched | Clean |

---

## Timing

| Phase | Duration |
|-------|----------|
| Full 12-character test | ~4 min (including 10s delays between characters) |
| Average per character | ~15s generation time |
| API model | gemini-3.1-flash-image-preview (NB2, Flash-tier pricing) |
| Estimated cost | ~$0.07/character x 12 = ~$0.84 total for this test run |

---

## Key Metrics

- **Character consistency:** 12/12 strong (anchor images are the solution)
- **Green screen quality:** 12/12 clean #00FF00 backgrounds
- **Style compliance:** 12/12 SF2 pixel art with dark outlines
- **Facing direction:** ~95% correct (occasional left-facing pose in multi-pose sheets)
- **Non-humanoid support:** 3/3 bosses with non-standard bodies generated correctly
- **Rate limit resilience:** 0 failures in the 12-character run with 10s delays
