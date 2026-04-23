# Autoresearch Debugging Log: First Real Run Failures

**Date:** 2026-04-12
**Session:** Post-build debugging after first real experiment run
**Outcome:** All 5 tiers now fire correctly. Pipeline ready for 100-experiment sweep.

---

## What Happened

The autoresearch system was built and passed all dry-run tests, but when the first real run launched, **every experiment scored 0.0** and short-circuited at Tier 1 (hard gates). 12 experiments burned ~$0.84 with zero useful data before the run was stopped.

After fixing the hard gates, the VLM tier (Tier 4) connected to the Alienware but returned **empty responses** — no walk cycle scores. This required debugging Qwen3-VL's behavior to get real evaluations flowing.

---

## Root Causes and Fixes

### 1. API Key: Wrong Function Name

**Symptom:** `No Gemini API key found` on first launch attempt.

**Root cause:** `runner.py` called `get_secret("google-ai-key")` but the keychain module exports `get_credential()`. Also, the `agents-sdk/` directory (where `lib/keychain.py` lives) wasn't on the Python path.

**Fix:**
- Changed `get_secret` to `get_credential` in `runner.py:637`
- Added `sys.path.insert(0, str(SUPERUSER_ROOT / "agents-sdk"))` to `runner.py:40`

**Prevention:** Always check the actual function signatures in `agents-sdk/lib/keychain.py` before using. The canonical pattern used everywhere else in the codebase:
```python
from lib.keychain import get_credential
api_key = get_credential("google-ai-key")
```

---

### 2. Hard Gates: Dimension Check Killed Every Experiment

**Symptom:** Every experiment scored 0.0 with `Hard gate failure: ['dimensions', 'palette']`. Frames were 344x384 or 290x304, not 128x128.

**Root cause:** The scoring pipeline expected post-Pixel-Quantizer output (128x128, palette-snapped), but experiments generate **raw Gemini output** at whatever resolution the model produces. In production, the Pixel Quantizer downscales and palette-snaps as a separate step. The scoring pipeline was checking quality of an intermediate artifact that hasn't been processed yet.

**Fix:** Added a `_preprocess_frames()` step at the start of `score_sheet()` that:
- Detects frames larger than the target tile size (128x128 for champions)
- Downscales via nearest-neighbor (preserving pixel art)
- Saves processed frames alongside originals with `_processed` suffix

**Location:** `prepare.py:430-462`

**Prevention:** When building a scoring pipeline for AI-generated output, always consider what the raw model output looks like vs. what the production pipeline produces. Raw output is the input to autoresearch — production-quality checks belong after the full pipeline runs.

---

### 3. Hard Gates: Palette Check Was Impossible to Pass

**Symptom:** Every frame had 36-48% off-palette pixels, triggering the palette hard gate.

**Root cause:** Gemini generates with continuous RGB colors (millions of possible values). The palette check expected pixels to be within 30 RGB distance of a 27-color palette. Raw AI output will **never** pass this — palette quantization is a post-processing step in the Pixel Quantizer.

**Fix:**
- Removed palette compliance from Tier 1 hard gates entirely
- Added `palette_proximity` as a **soft score** in Tier 3 (deterministic checks)
- The soft score measures average distance to the nearest palette color, normalized 0-1
- This rewards generations that are naturally closer to the target palette without blocking on it

**Location:** `prepare.py:581-589` (hard gate removal), `prepare.py:780-817` (soft score addition)

**Prevention:** Hard gates should only check things that are **universally true** of valid output at the stage being evaluated. Palette compliance is only valid after quantization. Dimensions are valid after downscaling. Background color is valid at any stage.

---

### 4. VLM Model: Wrong Model Name

**Symptom:** Would have caused connection failure (caught during audit before first VLM attempt).

**Root cause:** The kickoff doc specified `qwen2.5-vl:7b` but the Alienware has `qwen3-vl:8b` installed. The CLAUDE.md for the project also specifies `qwen3-vl:8b`.

**Fix:** Changed model name in `OllamaVLMAdapter.__init__()` from `qwen2.5-vl:7b` to `qwen3-vl:8b`.

**Prevention:** Always verify installed models via `curl http://192.168.68.201:11434/api/tags` before hardcoding model names.

---

### 5. VLM: Empty Responses from Qwen3-VL 8B

This was the most complex issue, involving three interacting problems with Qwen3-VL.

#### 5a. Thinking Mode Consumes All Tokens

**Symptom:** Ollama returns HTTP 200, `eval_count=512` or `1024`, `done_reason=length`, but `content=""`.

**Root cause:** Qwen3 models have a **thinking/reasoning mode** enabled by default. When the model encounters a complex prompt (especially one asking for structured output), it generates internal reasoning in `<think>` blocks. These tokens count against `num_predict` but don't appear in the `content` field. With `num_predict: 1024`, all tokens were consumed by thinking, leaving nothing for the actual response.

**Fix:** Set `num_predict: 4096`. The model typically spends 200-400 tokens thinking, then outputs the actual scores in the remaining budget. The `/no_think` prefix is also included but doesn't fully suppress thinking for complex prompts — it reduces but doesn't eliminate it.

#### 5b. JSON Output Format Triggers Extended Thinking

**Symptom:** Any prompt asking for JSON response (`"Respond as JSON"`, providing a JSON template) produced empty content even with high `num_predict` and `/no_think`.

**Root cause:** The JSON format instruction appears to trigger particularly aggressive thinking in Qwen3-VL. The model spends excessive tokens planning JSON structure rather than producing output. This was confirmed by testing: descriptive prompts worked; JSON prompts didn't.

**Fix:** Switched from JSON output format to plain text with `N/5` scoring:
```
Score leg variety 1-5, pose flow 1-5, weight shift 1-5, arm swing 1-5, 
character consistency 1-5, size consistency 1-5. Give scores and one 
biggest issue. Be brief.
```

Updated `_parse_vlm_response()` to parse `N/5` and bare `N` formats instead of JSON, using regex to map text labels to criterion keys.

#### 5c. Large Images Fill Context Window

**Symptom:** 2x upscaled images (2752x1536) produced empty responses. Original resolution (1376x768) worked.

**Root cause:** VLMs tokenize images into patches. A 2752x1536 image produces thousands of image tokens that consume most of the model's context window, leaving insufficient room for reasoning + output. The 8B model has a smaller effective context than larger models.

**Fix:** Send images at original Gemini output resolution (no upscale). The original ~1376x768 sprite sheets are already large enough for the VLM to evaluate walk cycle quality. The 4x upscale in the original design was intended for `qwen2.5-vl:7b` which may handle it differently — `qwen3-vl:8b` cannot.

Also removed the side-by-side composition (reference + generated) since that doubled the image width. The VLM evaluates the generated sheet alone.

**Prevention:** When using local VLMs (especially <=8B), always test with the actual image sizes you'll send in production. Image token counts scale with resolution and can silently consume the entire context window.

---

### 6. VLM Parser: Inconsistent Score Formats

**Symptom:** Some VLM responses parsed correctly (`Leg variety: 2/5`), others didn't (`Leg variety: 3,`).

**Root cause:** Qwen3-VL doesn't always format scores identically. Sometimes it uses `N/5`, sometimes bare `N` followed by a comma or period.

**Fix:** Updated the regex parser to handle both patterns:
```python
# Primary: "N/5" format
score_match = re.search(r"(\d)/5", line)
# Fallback: bare number after colon
if not score_match:
    score_match = re.search(r":\s*(\d)\b", line)
```

---

## Final Working Configuration

| Component | Setting | Why |
|-----------|---------|-----|
| Frame preprocessing | Nearest-neighbor downscale to 128x128 | Raw Gemini output varies (290x304, 344x384, etc.) |
| Hard gates | Dimensions + background + non-empty (NO palette) | Palette is post-quantization only |
| Palette scoring | Tier 3 soft score, 0-1, average distance to nearest palette color | Rewards closer colors without blocking |
| DINOv2 | Local CPU, facebook/dinov2-base, ~14s load + 0.1s/frame | Too small to justify remote setup |
| VLM model | `qwen3-vl:8b` on Alienware via Ollama | Only VL model installed |
| VLM prompt | Plain text, one-line, `/no_think` prefix | JSON and structured formats trigger thinking mode |
| VLM num_predict | 4096 | Must exhaust ~300 thinking tokens before output |
| VLM image size | Original resolution (no upscale) | 2x+ fills context window, causes empty output |
| VLM parser | Regex for `N/5` and bare `N` formats | Qwen3-VL output format varies |
| API key | `get_credential("google-ai-key")` from `lib.keychain` | Matches rest of codebase |

## Qwen3-VL 8B Behavior Reference

For any future VLM work with this model:

| Behavior | Detail |
|----------|--------|
| `/no_think` | Reduces but does NOT eliminate thinking mode |
| JSON output requests | Trigger extended thinking — avoid entirely |
| `num_predict` | Must be 4096+ to get output after thinking |
| Image resolution | Keep under ~1400px on longest side for reliable output |
| Multiple images | Avoid — each image consumes significant context |
| Simple prompts | Work reliably (single sentence, descriptive answers) |
| Complex prompts | Risk empty output — keep scoring criteria on one line |
| `eval_count` without content | Model is thinking, not producing output |
| `done_reason: length` with empty content | All tokens consumed by thinking |

---

## Lessons for Future Phases

1. **Phase 1 (ComfyUI):** The same scoring pipeline will work since ComfyUI output can be configured to exact dimensions. Hard gates should pass more consistently.

2. **Model upgrades:** If a larger VLM is installed (e.g., `qwen3-vl:32b`), the JSON output format and 4x upscaling could be re-enabled. The 8B model's limitations are context-window and thinking-mode specific.

3. **Palette scoring:** As the autoresearch finds better prompts, palette proximity scores should naturally improve (Gemini generates closer-to-palette colors when given better style direction). This is a useful signal even though it can't be a hard gate.
