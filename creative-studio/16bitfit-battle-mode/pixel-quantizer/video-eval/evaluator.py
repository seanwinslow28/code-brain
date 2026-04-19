"""Video Model Evaluation Framework.

Standardized evaluation harness that:
1. Takes a model adapter, keyframe config, and evaluation parameters
2. Calls the adapter to generate video
3. Extracts frames from the video output
4. Runs extracted frames through quality scoring
5. Outputs a structured evaluation report (JSON + visual grid)

The Pixel Quantizer is the gate check: if extracted frames can't be
quantized to clean pixel art, the hybrid pipeline approach is dead.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from adapters import (
    GeneratedFrame,
    GeneratedVideo,
    KeyframeConfig,
    StubAdapter,
    VideoModelAdapter,
)


@dataclass
class FrameScore:
    """Quality score for a single extracted frame."""
    frame_index: int
    palette_compliance: float  # 0-1: how many pixels match the target palette
    outline_quality: float  # 0-1: presence of bold outlines
    background_purity: float  # 0-1: how clean the background is (chroma key)
    character_presence: float  # 0-1: whether a character shape is detected
    overall: float = 0.0

    def __post_init__(self):
        self.overall = (
            self.palette_compliance * 0.3
            + self.outline_quality * 0.2
            + self.background_purity * 0.3
            + self.character_presence * 0.2
        )


@dataclass
class EvaluationReport:
    """Complete evaluation report for a model + animation test."""
    model_name: str
    animation_type: str
    character_name: str
    timestamp: str
    duration_secs: float

    # Metrics
    keyframe_count: int = 0
    extracted_frame_count: int = 0
    frame_scores: list[FrameScore] = field(default_factory=list)

    # Aggregates
    avg_palette_compliance: float = 0.0
    avg_outline_quality: float = 0.0
    avg_background_purity: float = 0.0
    avg_character_consistency: float = 0.0
    overall_score: float = 0.0

    # Timing
    keyframe_gen_ms: float = 0.0
    interpolation_ms: float = 0.0
    scoring_ms: float = 0.0
    total_ms: float = 0.0

    # Pass/Fail
    passed_gate_check: bool = False
    gate_check_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_name": self.model_name,
            "animation_type": self.animation_type,
            "character_name": self.character_name,
            "timestamp": self.timestamp,
            "metrics": {
                "keyframe_count": self.keyframe_count,
                "extracted_frame_count": self.extracted_frame_count,
                "avg_palette_compliance": round(self.avg_palette_compliance, 3),
                "avg_outline_quality": round(self.avg_outline_quality, 3),
                "avg_background_purity": round(self.avg_background_purity, 3),
                "avg_character_consistency": round(self.avg_character_consistency, 3),
                "overall_score": round(self.overall_score, 3),
            },
            "timing": {
                "keyframe_gen_ms": round(self.keyframe_gen_ms, 1),
                "interpolation_ms": round(self.interpolation_ms, 1),
                "scoring_ms": round(self.scoring_ms, 1),
                "total_ms": round(self.total_ms, 1),
            },
            "gate_check": {
                "passed": self.passed_gate_check,
                "reason": self.gate_check_reason,
            },
            "frame_scores": [
                {
                    "frame": s.frame_index,
                    "palette": round(s.palette_compliance, 3),
                    "outline": round(s.outline_quality, 3),
                    "background": round(s.background_purity, 3),
                    "character": round(s.character_presence, 3),
                    "overall": round(s.overall, 3),
                }
                for s in self.frame_scores
            ],
        }

    def to_markdown(self) -> str:
        """Generate a markdown report."""
        lines = [
            f"# Video Model Evaluation: {self.model_name}",
            f"",
            f"**Animation:** {self.animation_type} | **Character:** {self.character_name}",
            f"**Date:** {self.timestamp}",
            f"",
            f"## Gate Check: {'PASS' if self.passed_gate_check else 'FAIL'}",
            f"",
            f"**Reason:** {self.gate_check_reason}",
            f"",
            f"## Scores",
            f"",
            f"| Metric | Score |",
            f"|--------|-------|",
            f"| Palette Compliance | {self.avg_palette_compliance:.1%} |",
            f"| Outline Quality | {self.avg_outline_quality:.1%} |",
            f"| Background Purity | {self.avg_background_purity:.1%} |",
            f"| Character Consistency | {self.avg_character_consistency:.1%} |",
            f"| **Overall** | **{self.overall_score:.1%}** |",
            f"",
            f"## Timing",
            f"",
            f"| Phase | Duration |",
            f"|-------|----------|",
            f"| Keyframe Generation | {self.keyframe_gen_ms:.0f}ms |",
            f"| Video Interpolation | {self.interpolation_ms:.0f}ms |",
            f"| Frame Scoring | {self.scoring_ms:.0f}ms |",
            f"| **Total** | **{self.total_ms:.0f}ms** |",
            f"",
            f"## Frame Details",
            f"",
            f"| Frame | Palette | Outline | Background | Character | Overall |",
            f"|-------|---------|---------|------------|-----------|---------|",
        ]

        for s in self.frame_scores:
            lines.append(
                f"| {s.frame_index} | {s.palette_compliance:.1%} | "
                f"{s.outline_quality:.1%} | {s.background_purity:.1%} | "
                f"{s.character_presence:.1%} | {s.overall:.1%} |"
            )

        return "\n".join(lines)


# Sean character palette (from project spec)
SEAN_PALETTE = {
    "skin": "#F5D6C6",
    "hair": "#C2A769",
    "eyes": "#4682B4",
    "tank_top": "#F2F0EF",
    "pants": "#2323FF",
    "shoes": "#F5F5F5",
    "outline": "#272929",
    "background": "#00FF00",
}

# Convert hex to RGB tuples for scoring
PALETTE_RGB = {}
for name, hex_color in SEAN_PALETTE.items():
    h = hex_color.lstrip("#")
    PALETTE_RGB[name] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def score_frame(frame: GeneratedFrame, target_palette: dict[str, tuple[int, int, int]]) -> FrameScore:
    """Score a single frame against the target palette and quality criteria.

    Args:
        frame: The frame to score (RGBA format expected).
        target_palette: Dict of color name -> RGB tuple.

    Returns:
        FrameScore with individual metric scores.
    """
    if frame.format != "rgba" or len(frame.data) < frame.width * frame.height * 4:
        # Can't score non-RGBA frames meaningfully
        return FrameScore(
            frame_index=frame.metadata.get("frame_index", 0),
            palette_compliance=0.0,
            outline_quality=0.0,
            background_purity=0.0,
            character_presence=0.0,
        )

    palette_colors = list(target_palette.values())
    bg_rgb = target_palette.get("background", (0, 255, 0))
    outline_rgb = target_palette.get("outline", (39, 41, 41))

    total_pixels = frame.width * frame.height
    palette_matches = 0
    bg_pixels = 0
    outline_pixels = 0
    character_pixels = 0

    for i in range(0, len(frame.data), 4):
        r, g, b = frame.data[i], frame.data[i + 1], frame.data[i + 2]
        pixel = (r, g, b)

        # Check palette compliance (within 30 units of any palette color)
        min_dist = min(_color_distance(pixel, c) for c in palette_colors)
        if min_dist < 30:
            palette_matches += 1

        # Check background
        if _color_distance(pixel, bg_rgb) < 20:
            bg_pixels += 1

        # Check outline
        if _color_distance(pixel, outline_rgb) < 30:
            outline_pixels += 1

        # Check character (non-background, non-outline)
        if _color_distance(pixel, bg_rgb) > 50:
            character_pixels += 1

    non_bg_pixels = max(total_pixels - bg_pixels, 1)

    return FrameScore(
        frame_index=frame.metadata.get("frame_index", 0),
        palette_compliance=palette_matches / total_pixels,
        outline_quality=min(outline_pixels / max(non_bg_pixels * 0.1, 1), 1.0),
        background_purity=bg_pixels / total_pixels,
        character_presence=min(character_pixels / (total_pixels * 0.3), 1.0),
    )


def extract_frames_from_video(video: GeneratedVideo, target_count: int = 8) -> list[GeneratedFrame]:
    """Extract evenly-spaced frames from a video.

    For stub/raw_frames format: reads from metadata.
    For mp4: would use ffmpeg (not implemented yet — requires subprocess).
    """
    if video.format == "raw_frames" and "frames" in video.metadata:
        # Stub adapter stores frames directly
        raw_frames: list[bytes] = video.metadata["frames"]
        total = len(raw_frames)
        if total <= target_count:
            indices = range(total)
        else:
            step = total / target_count
            indices = [int(i * step) for i in range(target_count)]

        return [
            GeneratedFrame(
                data=raw_frames[i],
                width=video.width,
                height=video.height,
                format="rgba",
                metadata={"frame_index": i, "source": "extracted"},
            )
            for i in indices
        ]

    if video.format == "mp4":
        return _extract_frames_ffmpeg(video, target_count)

    raise NotImplementedError(
        f"Frame extraction for {video.format} not yet implemented."
    )


def _extract_frames_ffmpeg(video: GeneratedVideo, target_count: int) -> list[GeneratedFrame]:
    """Extract frames from an MP4 video using ffmpeg.

    Writes the video to a temp file, extracts frames as PNGs,
    reads them back as RGBA GeneratedFrame objects.
    """
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory(prefix="video_eval_") as tmpdir:
        tmp = Path(tmpdir)
        video_path = tmp / "input.mp4"
        video_path.write_bytes(video.data)

        # Extract frames as PNG
        frame_pattern = str(tmp / "frame_%04d.png")

        # Use fps filter to get evenly-spaced frames
        total_frames_est = int(video.duration_secs * video.fps)
        if total_frames_est <= 0:
            total_frames_est = target_count
        fps_filter = target_count / video.duration_secs if video.duration_secs > 0 else 8

        result = subprocess.run(
            [
                "ffmpeg", "-i", str(video_path),
                "-vf", f"fps={fps_filter:.2f}",
                "-frames:v", str(target_count),
                frame_pattern,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg frame extraction failed: {result.stderr[:300]}")

        # Read extracted frames and convert to RGBA
        frames: list[GeneratedFrame] = []
        for i in range(1, target_count + 1):
            frame_path = tmp / f"frame_{i:04d}.png"
            if not frame_path.exists():
                break

            png_data = frame_path.read_bytes()

            # Convert PNG to raw RGBA using ffmpeg
            rgba_result = subprocess.run(
                [
                    "ffmpeg", "-i", str(frame_path),
                    "-pix_fmt", "rgba",
                    "-f", "rawvideo",
                    "pipe:1",
                ],
                capture_output=True,
                timeout=10,
            )

            if rgba_result.returncode == 0 and rgba_result.stdout:
                frames.append(GeneratedFrame(
                    data=rgba_result.stdout,
                    width=video.width,
                    height=video.height,
                    format="rgba",
                    metadata={"frame_index": i - 1, "source": "ffmpeg_extracted"},
                ))
            else:
                # Fallback: store PNG data (can't score RGBA metrics but preserves frame)
                frames.append(GeneratedFrame(
                    data=png_data,
                    width=video.width,
                    height=video.height,
                    format="png",
                    metadata={"frame_index": i - 1, "source": "ffmpeg_extracted_png"},
                ))

    return frames


async def evaluate_model(
    adapter: VideoModelAdapter,
    config: KeyframeConfig,
    duration_secs: float = 1.0,
    target_frames: int = 8,
    output_dir: Path | None = None,
) -> EvaluationReport:
    """Run the full evaluation pipeline for a model.

    Pipeline:
    1. Generate keyframes (or use provided ones)
    2. Interpolate to video
    3. Extract frames
    4. Score each frame
    5. Aggregate and report
    """
    from datetime import datetime

    report = EvaluationReport(
        model_name=adapter.name,
        animation_type=config.animation_type,
        character_name=config.character_name,
        timestamp=datetime.now().isoformat(),
        duration_secs=duration_secs,
    )

    total_start = time.monotonic()

    # Step 1: Generate keyframes
    kf_start = time.monotonic()
    keyframes = await adapter.generate_keyframes(config)
    report.keyframe_gen_ms = (time.monotonic() - kf_start) * 1000
    report.keyframe_count = len(keyframes)

    # Step 2: Interpolate to video
    interp_start = time.monotonic()
    video = await adapter.interpolate_frames(keyframes, duration_secs)
    report.interpolation_ms = (time.monotonic() - interp_start) * 1000

    # Step 3: Extract frames
    extracted = extract_frames_from_video(video, target_frames)
    report.extracted_frame_count = len(extracted)

    # Step 4: Score frames
    score_start = time.monotonic()
    for frame in extracted:
        score = score_frame(frame, PALETTE_RGB)
        report.frame_scores.append(score)
    report.scoring_ms = (time.monotonic() - score_start) * 1000

    # Step 5: Aggregate
    if report.frame_scores:
        n = len(report.frame_scores)
        report.avg_palette_compliance = sum(s.palette_compliance for s in report.frame_scores) / n
        report.avg_outline_quality = sum(s.outline_quality for s in report.frame_scores) / n
        report.avg_background_purity = sum(s.background_purity for s in report.frame_scores) / n
        report.avg_character_consistency = sum(s.character_presence for s in report.frame_scores) / n
        report.overall_score = sum(s.overall for s in report.frame_scores) / n

    # Gate check: overall score must be > 0.5 and palette compliance > 0.6
    if report.overall_score >= 0.5 and report.avg_palette_compliance >= 0.6:
        report.passed_gate_check = True
        report.gate_check_reason = (
            f"Overall {report.overall_score:.1%} >= 50%, "
            f"palette {report.avg_palette_compliance:.1%} >= 60%"
        )
    else:
        report.passed_gate_check = False
        report.gate_check_reason = (
            f"Overall {report.overall_score:.1%} (need >= 50%), "
            f"palette {report.avg_palette_compliance:.1%} (need >= 60%)"
        )

    report.total_ms = (time.monotonic() - total_start) * 1000

    # Save report if output directory specified
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = adapter.name.replace(" ", "_").lower()
        json_path = output_dir / f"eval-{safe_name}-{config.animation_type}.json"
        md_path = output_dir / f"eval-{safe_name}-{config.animation_type}.md"

        with open(json_path, "w") as f:
            json.dump(report.to_dict(), f, indent=2)
        with open(md_path, "w") as f:
            f.write(report.to_markdown())

    return report


async def run_comparison(
    adapters: list[VideoModelAdapter],
    config: KeyframeConfig,
    duration_secs: float = 1.0,
    target_frames: int = 8,
    output_dir: Path | None = None,
) -> list[EvaluationReport]:
    """Run evaluation across multiple adapters and produce a comparison report."""
    reports = []
    for adapter in adapters:
        report = await evaluate_model(
            adapter, config, duration_secs, target_frames, output_dir
        )
        reports.append(report)

    if output_dir and reports:
        # Write comparison summary
        lines = [
            "# Video Model Comparison",
            "",
            f"**Animation:** {config.animation_type} | **Character:** {config.character_name}",
            "",
            "| Model | Overall | Palette | Outline | BG Purity | Character | Gate |",
            "|-------|---------|---------|---------|-----------|-----------|------|",
        ]
        for r in reports:
            gate = "PASS" if r.passed_gate_check else "FAIL"
            lines.append(
                f"| {r.model_name} | {r.overall_score:.1%} | "
                f"{r.avg_palette_compliance:.1%} | {r.avg_outline_quality:.1%} | "
                f"{r.avg_background_purity:.1%} | {r.avg_character_consistency:.1%} | "
                f"{gate} |"
            )

        comp_path = output_dir / f"comparison-{config.animation_type}.md"
        with open(comp_path, "w") as f:
            f.write("\n".join(lines))

    return reports
