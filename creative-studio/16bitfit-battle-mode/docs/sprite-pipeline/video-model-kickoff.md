# Kickoff Prompt: Video Model Sprite Generation Pipeline Test

**Copy everything below this line into a new Claude conversation, along with the attached documentation file.**

---

You are an expert technical creative director and production engineer focused exclusively on AI-assisted sprite creation and sprite sheet generation for 2D games. Your job is to help me research, design, and test a new workflow for generating consistent fighting game sprite animations using video generation models.

## Project Context

I'm working on **16BitFit Battle Mode**, a 2D fighting game requiring sprite animations in Street Fighter II pixel art style. I've attached documentation from our previous testing phase that established:

1. **Successful single-frame generation** using Gemini 3 Pro Image (Nano Banana Pro)
2. **Excellent character consistency** when using multi-angle reference images
3. **A limitation**: The image model struggles with sequential animation frames, particularly walk cycles where left/right leg differentiation fails

The attached documentation contains our proven prompt structures, character specifications, and lessons learned.

## New Workflow to Test: Video Model Pipeline

I want to test a new approach that leverages video generation models to solve the animation consistency problem:

### Proposed Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: KEYFRAME GENERATION                                     │
│  Use proven single-frame prompts to generate:                    │
│  - Start pose (Frame 1 of animation)                             │
│  - End pose (Final frame of animation)                           │
│  These become anchor points for the video model                  │
├─────────────────────────────────────────────────────────────────┤
│  STEP 2: VIDEO GENERATION                                        │
│  Feed keyframes to video model with instructions to:             │
│  - Interpolate motion between start and end poses                │
│  - Maintain character identity throughout                        │
│  - Keep consistent style and background                          │
├─────────────────────────────────────────────────────────────────┤
│  STEP 3: FRAME EXTRACTION                                        │
│  Extract specific frames from generated video:                   │
│  - Select frames that match required animation timing            │
│  - Export as individual PNG images                               │
│  - Target frame counts: 4, 6, or 8 frames per animation          │
├─────────────────────────────────────────────────────────────────┤
│  STEP 4: POST-PROCESSING                                         │
│  - Remove solid green (#00FF00) chroma key background            │
│  - Normalize frame dimensions to 128×128 pixels                  │
│  - Validate character consistency across extracted frames        │
├─────────────────────────────────────────────────────────────────┤
│  STEP 5: SPRITE SHEET ASSEMBLY                                   │
│  - Arrange frames in horizontal rows                             │
│  - Export as PNG + JSON for Phaser compatibility                 │
│  - Package using TexturePacker standards                         │
└─────────────────────────────────────────────────────────────────┘
```

## What I Need From You

### Phase 1: Research & Model Selection

1. **Identify suitable video generation models** that can:
   - Accept start/end frame images as input (image-to-video with keyframes)
   - Generate short animations (1-3 seconds)
   - Maintain character consistency between keyframes
   - Handle solid color backgrounds

2. **Evaluate options** such as:
   I have access to Kling AI (https://docs.qingque.cn/d/home/eZQDvlYrDMyE9lOforCeWA4KP?identityId=1uX4dFq8Jtr#section=h.8lu2cjsljfrb), Google Veo 3.1 and Google Flow (Google AI Ultra Subscription - https://ai.google.dev/gemini-api/docs/video?example=dialogue), Fal.ai (https://fal.ai/explore), Replicate (https://replicate.com/), and Grok Imagine Video (https://grok.com/imagine). I also have access to Weavy.ai  (https://www.weavy.ai/) and I have an Alienware PC (NVIDIA(R) GeForce RTX(TM) 5080 16GB GDDR7, 64GB Dual Channel DDR5 (2x 32GB - Green) 5200 MT/s) with access to ComfyUI. Please do your research on these specific platforms and then we can focus on the next steps/Phase 2.

3. **Recommend the best model(s)** for this specific use case with rationale

### Phase 2: Workflow Design

1. **Keyframe generation strategy**: What specific poses should be the start/end frames for each animation type?
   - Walk Cycle (4 frames needed)
   - Jump (4 frames needed)
   - Idle breathing (4 frames needed)
   - Light Punch (6 frames needed)
   - Heavy Kick (8 frames needed)

2. **Video generation prompts**: How should we prompt the video model to maintain:
   - Street Fighter II pixel art aesthetic
   - Character identity
   - Solid green background
   - Appropriate motion speed/timing

3. **Frame extraction strategy**: 
   - How many total frames should the video generate?
   - Which frame numbers should we extract for each animation?
   - How do we ensure smooth looping for cyclical animations?

### Phase 3: Test Execution

Help me execute tests with:
1. One character (Sean - Champion)
2. One animation (Walk Cycle - since this is our known failure point)
3. Document results and iterate

## Technical Specifications

From the attached documentation, maintain these standards:

- **Frame Size:** 128×128 pixels
- **Style:** Street Fighter II arcade aesthetic
- **Outlines:** Bold #272929 dark outlines (2-3px)
- **Shading:** 3-4 tone cel shading
- **Background:** Solid chroma key green (#00FF00)
- **Constraints:** No anti-aliasing, no gradients

## Character Reference (Sean)

| Attribute | Value |
|-----------|-------|
| Skin | #F5D6C6 |
| Hair | #C2A769 (dirty blonde) |
| Eyes | #4682B4 (steel blue) |
| Tank Top | #F2F0EF (off-white) |
| Pants | #2323FF (neon blue) |
| Shoes | #F5F5F5 (white) |

## Success Criteria

The video model pipeline is successful if:

1. **Walk cycle leg differentiation works** - Left and right legs clearly alternate correctly
2. **Character identity maintained** - Face, hair, proportions consistent across all frames
3. **Style consistency** - Pixel art aesthetic preserved, no soft rendering or gradients
4. **Usable output** - Extracted frames can be assembled into functional sprite sheet
5. **Repeatable process** - Workflow can be applied to other animations and characters

## Starting Point

Please begin with Phase 1: Research the available video generation models and recommend which one(s) we should test for this pipeline. Consider:

- Keyframe/image-to-video capabilities
- Style consistency reputation
- Accessibility (API, web interface, pricing)
- Output quality and resolution
- Frame rate and duration options

Let me know what additional information you need from the attached documentation to proceed.

---

**ATTACHMENTS TO INCLUDE:**
1. `sprite-generation-testing-documentation.md` (the documentation file)
2. `Champion-Sean-anchor.png` (anchor image for reference)
3. `Champion-Sean-Turnaround-Sheet.png` (turnaround reference)
4. Any successful Phase 1 outputs (front, side, 3/4, back views)
5. The guard pose output (as example of successful single-frame generation)
