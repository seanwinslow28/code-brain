In February 2026, the architectural recommendation is to **immediately pivot to the Hybrid Keyframe-to-Video Pipeline**, but with a specific architectural pattern I will call the **"Quantized Motion Bridge."**

The "Image-Only" strategy has hit a hard ceiling with temporal coherence (the "left vs. right leg" problem), and the "Wait-and-Adapt" strategy is practically obsolete because the specific capabilities you need (Start/End Frame Conditioning) are already live in the 2026 versions of Kling and Veo.

The following analysis details the recommended architecture and investment strategy.

### **Strategic Recommendation: The Hybrid "Quantized Motion Bridge"**

You should invest 70% of your testing time into the **Hybrid Pipeline**. The rapid maturation of "first-frame/last-frame conditioning" in video models (specifically **Kling 2.5/3.0** and **Google Veo 3**) has solved the gross motion hallucination problem. The new challenge—and where you must build your adapter layer—is **Sub-Pixel Drift**.

Video models operate in continuous latent space, meaning they "smear" pixels to create motion. They will turn your crisp 128px pixel art into a slightly blurred, anti-aliased MP4. Your architecture must accept this "sludge" as intermediate data and quantize it back to strict pixel specs.

#### **Recommended Pipeline Architecture**

1.  **Keyframe Generators (Gemini 2.0 / Image Model):**
    *   **Role:** Generate strictly defined "Anchor Frames" (e.g., Walk_Start, Walk_Pass, Walk_End).
    *   **Constraint:** Do not generate every frame. Generate only the *extremes* where the limb positions are unambiguous.
    *   **Input:** Dual-reference (Character LORA + Pose ControlNet).

2.  **Motion Interpolator (The New Adapter Layer):**
    *   **Tool Selection:** **Google Veo** or **Kling** (whichever offers the best API for "Keyframe Steering" in Q1 2026).
    *   **Operation:** Feed `[Frame A]` and `[Frame B]` as rigid boundary conditions. Request a short duration video (e.g., 0.5s) to bridge them.
    *   **Crucial Setting:** Low "Creativity/Motion" variance settings to prevent style drift.

3.  **The "Pixel Quantizer" (Your Custom Build):**
    *   *This is where you should spend your engineering effort.*
    *   **Downsample & Palettize:** The raw video output will be ~1080p or 720p with compression artifacts. You must:
        1.  **Nearest-Neighbor Downscale** to target resolution (128x128).
        2.  **Palette Snap:** Force every pixel to the nearest color in your specific character's palette.
        3.  **Alpha Recovery:** Use a depth map or difference matte (often available from video model metadata or separate inference) to regain clean transparency, as video models often hallucinate muddy backgrounds.

### **Detailed Comparison & Investment Guide**

| Approach | Verdict (Feb 2026) | Technical Reality |
| :--- | :--- | :--- |
| **1. Image-Only Pipeline** | **ABANDON** | **The "Temporal Wall" is real.** LLMs/Image models struggle with *implied state* (knowing which leg moved previously). Solving this requires massive ControlNet overhead (skeleton per frame) which defeats the purpose of "automation." It is slower and more brittle than video interpolation. |
| **2. Hybrid Pipeline** | **INVEST (Primary)** | **The "Sludge" is solvable.** Video models capture *momentum* and *physics* better than image models. It is easier to write a script that "cleans up" a blurry but correctly moving video frame than it is to force an image model to understand the physics of a walk cycle. |
| **3. Wait-and-Adapt** | **MINOR (Secondary)** | **Audit-Only.** Continue building your validator (Phaser 3 headless), as it is model-agnostic. However, do not wait on generation. Specialized tools like **Retro Diffusion (RD Animation)** and **PixelLab** are emerging as "black box" alternatives. Keep 10% of resources monitoring these API endpoints as a potential replacement for your custom pipeline. |

### **Immediate Action Plan (Q1 2026)**

1.  **Prototype the "Quantizer":** Before integrating Veo/Kling, write a localized script (Python/OpenCV) that takes a blurry 1080p video of a sprite, downscales it to 128x128, and snaps colors to a lookup table (LUT). If this script works, the Hybrid pipeline is viable.
2.  **Test "Loop Integrity":** Run a test with Kling using the *same image* as both the Start and End frame, with a text prompt for "idle breathing animation." If the middle frames drift in identity, your "Identity Consistency" gate needs to be tighter.
3.  **Boss Character Strategy:** For 256x256 bosses, the Hybrid pipeline is *essential*. Specialized pixel-art models (like PixelLab) often degrade at higher resolutions (training data is usually 64x64). Generic video models (Veo) excel at higher resolutions and will retain the "bold outline" style better when downscaled from 4K/1080p.

**Summary:** Stop fighting the LLM's inability to track hidden leg states. Offload *motion* to Video AI, and use your code to enforce *style* (pixel grid/palette) on the result.