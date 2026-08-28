Research complete. Here is the structured report.

---

# Multimodal Character-Consistency Verification — State of the Art + Competitive Movement (as of 2026-08-08)

## Part A: State of the art in automated visual character-consistency verification

**1. ViStoryBench** — https://arxiv.org/html/2505.24862 (arXiv 2505.24862v5, updated 2026-03-29; ShanghaiTech/StepFun/Westlake)
- TECHNICAL: The reference metric stack for story visualization. CIDS (Character Identification Similarity) pipeline: Grounding DINO detects/crops character regions → feature extraction (ArcFace/AdaFace/FaceNet for realistic faces; **plain CLIP encoders for stylized/anime characters**) → bipartite matching → mean cosine similarity. Reports both **cross-similarity** (vs. reference) and **self-consistency** (within generated set). Also: OCCM (onstage character-count matching, exponential-decay formula) and a copy-paste-detection metric.
- CONFIRMS-WEDGE: Acknowledged weakness — Grounding DINO "may fail entirely, returning an empty result" on generated/stylized images, and the stylized branch falls back to generic CLIP (no dedicated stylized-identity embedding). The stylized-character identity problem is explicitly unsolved at the metric level.

**2. VLM Judges Can Rank but Cannot Score** — https://arxiv.org/html/2604.25235v1 (2026-04-28)
- TECHNICAL / CONFIRMS-WEDGE: VLM judges achieve strong *ranking* correlation but unreliable *absolute* scores (32–34% exact agreement with humans on 5-point scales; 24–30% of predictions off by ≥2 points). Conformal-interval width is task-dependent (2.08 pts aesthetics vs 3.50 infographic QA) and dominated by ground-truth quality (4.5× narrower on clean multi-annotator data). Design implication for a verifier: use pairwise/relative comparison against a locked reference, not absolute 1–10 drift scores.

**3. VCMS (ACL 2026)** — https://aclanthology.org/2026.acl-long.1578/ (Jhang, Park, Koh, Jung)
- TECHNICAL: "Visual Context-Aware Metric for Story Visualization" — VLM jointly assesses caption fidelity + inter-image consistency, correlating with human judgment on two benchmarks. Academic metric, not a product; validates VLM-as-judge for *inter-image consistency* specifically.

**4. Audit & Repair** — https://arxiv.org/abs/2506.18900 (Akdemir, Kazimi, Yanardag; June 2025)
- THREATENS-WEDGE (mildly) / TECHNICAL: The closest prior art to a verification product: a multi-agent framework where a VLM audits multi-panel story visualizations, maintains a Consistency Index, produces a per-panel consistency report, then repairs via Flux-ControlNet localized edits. It is an academic pipeline bolted to generation (audit-to-repair loop), not a standalone verification tool, and reliability numbers for the audit stage aren't headline results — but it proves the audit→report→fix product shape works.

**5. Face Consistency Benchmark (FCB)** — https://arxiv.org/html/2505.11425v1
- TECHNICAL: Purpose-built framework for scoring character/face consistency in AI-generated video; face-crop DINOv2/ArcFace descriptors per frame. Photoreal-face-centric — does not solve stylized identity.

**6. VBench / video-gen leaderboards** — https://benchmarklist.com/benchmarks/vbench_video_generation/, https://arxiv.org/pdf/2605.15199 (EntityBench), https://arxiv.org/pdf/2508.00144 (World Consistency Score), https://arxiv.org/pdf/2602.23969 (MSVBench)
- TECHNICAL: "Subject consistency" is now a standard leaderboard dimension (VBench 16 dimensions; Artificial Analysis gives Seedance 2.0 a 10/10 "character consistency"). EntityBench targets entity consistency in long-range multi-shot generation; World Consistency Score proposes a unified consistency metric; MSVBench targets human-level multi-shot evaluation. All are *model-evaluation* benchmarks — none is a creator-facing tool that audits a specific creator's own image/video set.

**7. Stylized-identity embeddings** — https://arxiv.org/pdf/2604.05507 (anime character evolution tracking), Anime-2026 dataset (https://doi.org/10.1145/3805622.3810619), manga re-ID (https://arxiv.org/pdf/2204.04621)
- TECHNICAL: The emerging stylized-identity recipe is **DINOv2 (dinov2-base, 82M) features over character crops**, plus face-body joint clustering for manga re-ID. Anime-2026 is a large-scale ID-labeled anime character dataset (ICMR 2026) — exactly the training substrate for a fine-tuned stylized-identity encoder. No off-the-shelf "ArcFace for anime" checkpoint has emerged as standard yet.
- CONFIRMS-WEDGE: My search for documented "CLIP fails on anime identity" analyses came up thin — the gap between photoreal (ArcFace, mature) and stylized (generic CLIP/DINOv2, ad hoc) identity metrics is real and under-served.

**8. StoryBlender / CANVAS / Story2Board** — https://arxiv.org/html/2604.03315v1, https://arxiv.org/html/2604.13452, https://daviddinkevich.github.io/Story2Board/ (all April 2026)
- TECHNICAL: CIDS is being adopted as the standard eval (StoryBlender uses CIDS + CSD style-coherence metric; CANVAS names "character appearance drift" as the core failure mode). Drift is now a *named, measured* problem in the literature — but always in service of better generation, never as a shipped verification product.

## Part B: Competitive movement since early August 2026

**9. Novarrium** — https://novarrium.com/ (fetched live today)
- CONFIRMS-WEDGE: **Zero visual/image/multimodal features.** All 9 verification checks are text-only (character traits, dead-stay-dead, POV, plot points, world rules, voice, author rules, quality score, bible update). No changelog entries suggesting visual work. 729+ series imported — traction is in text canon enforcement.

**10. Novelium** — https://novelium.com/ (search + site content)
- CONFIRMS-WEDGE: Text-only. Its "visual timeline" is a text-derived visualization of timeline conflicts, not image analysis. No multimodal announcements found.

**11. Bunsho** — https://www.bunsho.io/ (fetched live today)
- CONFIRMS-WEDGE: Still **pre-launch ("private beta soon," waitlist)**. Features (continuity checker, plot-hole checker, Director Mode, ripple detection) are all text-graph based. No visual features mentioned.

**12. New entrants (Product Hunt / X / launch searches)** — EMPTY RESULT
- CONFIRMS-WEDGE: Searches for Product Hunt launches, "character drift detection tool," and "multimodal continuity checker" for visual serials returned **no product** doing visual/multimodal series-consistency *verification*. The entire commercial field (LlamaGen, Ideogram Character, Dzine, ConsistentCharacterAI, Anifusion, ComicPad, Leonardo LoRA workflows) is consistency-conditioned *generation*. One trade source (OutlierKit teardown, https://outlierkit.com/resources/ai-tools-vertical-micro-drama-2026/) states holding identity across a 2–3-minute multi-generation sequence "still requires manual reference locking, and no tool currently ships this end-to-end at production quality."

**13. Generation vendors** — Midjourney (https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/), Higgsfield Soul ID (https://higgsfield.ai/blog/tools-for-consistent-ai-characters), Kling 3.0 (https://www.glbgpt.com/hub/kling-ai-character-consistency-explained/), Veo 3.1/Sora 2 (https://www.digitalapplied.com/blog/ai-video-generation-omni-vs-sora-vs-veo-3)
- CONFIRMS-WEDGE: All ship consistency-*conditioned generation* (--oref/--ow, Soul ID trained identities, reference-image locking) — **none ships a post-hoc verification score/report on a generated set.** Veo 3.1's "92% identity preservation across five shots" is a marketing/benchmark claim, not a user-facing audit feature. Provenance features (SynthID, C2PA) verify *authenticity*, not *identity consistency*. Documented open failure: multi-character close-up interaction blurs identity on every platform; Runway Gen-4.5 has no dedicated character-training tool and drifts over long sequences.

## Empty/negative searches (findings in themselves)
- No Product Hunt or X launch of a visual consistency *checker* (searched Aug 2026 window).
- No vendor announcement of built-in drift scoring/reporting.
- No standard "ArcFace-for-stylized" embedding checkpoint exists yet.
- No Novarrium/Novelium/Bunsho multimodal announcement of any kind.

## Verdict

**The multimodal verification wedge is still open as of 2026-08-08.** The three text-serial checkers remain strictly text-only (one still pre-beta); every commercial player in visual character consistency sits on the generation side; and generation vendors expose consistency as an *input* (reference locking) never as an *output* (audit report) — while trade press explicitly says nobody ships end-to-end identity QA at production quality. The threat surface is academic, not commercial: Audit & Repair proves the audit→report→repair loop, and CIDS/VCMS give any fast follower a public metric recipe — so the moat is execution speed and stylized-domain calibration, not secret technique. Strongest technical approach for stylized-character identity checking: a **hybrid pipeline — Grounding DINO character detection → DINOv2 features on character crops (fine-tuned or k-NN-calibrated against the Anime-2026-style ID-labeled data, with per-series reference anchoring), reporting both cross-similarity to the locked reference and self-consistency across the set — with a VLM judge layered on top strictly in pairwise/ranking mode** (never absolute scores, per the VLM-judge reliability findings) to explain *what* drifted (hair, outfit, proportions) in language a creator can act on. Handle the known detector failure mode (Grounding DINO returning empty on heavily stylized panels) as a first-class "unverifiable panel" state rather than a silent skip.