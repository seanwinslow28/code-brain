# Pose Skeleton Edits Log

## 2026-04-16: Full manual generation (not DWPose extraction)

**Problem:** DWPose and OpenPose preprocessors both failed completely on SF2 Ryu pixel
art — even after bilinear upscaling to 1024x1024, background removal (blue->white),
and Gaussian blur. Neither YOLO person detector could identify a human figure in the
upscaled pixel art. All outputs were solid black (no skeleton detected).

**Attempted fixes (all failed):**
1. Nearest-neighbor upscale to 1024x1024 -> DWPose: all black
2. Bilinear upscale + Gaussian blur (r=2) -> DWPose: all black
3. Blue background removal + bilinear upscale + blur -> DWPose: all black
4. Same as #3 -> OpenposePreprocessor: all black

**Root cause:** Person detection models (YOLO) are trained on real photographs. Even
smoothed pixel art at 1024x1024 doesn't trigger the person bounding box detector.
The original sprites are only 80x76 pixels — there's not enough detail for pose
estimation to work, regardless of upscaling method.

**Solution:** Hand-drew all 4 OpenPose skeletons programmatically using PIL, following
the standard OpenPose COCO keypoint format (18 joints, colored limbs and joints on
black background). Joint positions were set based on visual analysis of the Ryu
sprite frames. This is explicitly endorsed by the pose_skeletons README (Step 5):
"you can manually tweak the skeleton in any image editor."

**Verification:** Contact and Passing skeletons are visibly different — contact has
legs spread wide (~300px ankle separation), passing has legs nearly together (~30px
ankle separation). This is the critical distinction for the Phase 1 hypothesis.

**Source sprites used for reference:**
- Arcade CPS2 sheet from The Spriters Resource (asset 60224)
- Walk forward row: y=1296-1372, frames 1-4 (of 6), each 80x76 px
- Frame mapping: 1=contact, 2=down, 3=passing, 4=up

**Files generated:**
- `ryu_walk_contact.png` — 1024x1024, OpenPose format
- `ryu_walk_down.png` — 1024x1024, OpenPose format
- `ryu_walk_passing.png` — 1024x1024, OpenPose format
- `ryu_walk_up.png` — 1024x1024, OpenPose format
