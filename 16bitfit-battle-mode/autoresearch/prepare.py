"""Autoresearch Scoring Pipeline — FROZEN during experiments.

This file implements the 5-tier scoring pipeline for evaluating generated
sprite sheets. It is the `prepare.py` in Karpathy's three-file autoresearch
pattern. The experiment runner must NEVER modify this file.

Tiers (execute in order, short-circuit on hard failure):
  1. Hard Gates — palette, dimensions, alpha, background
  2. Identity — DINOv2 cosine similarity vs anchor embeddings
  3. Deterministic — outline weight, baseline drift, frame count
  4. VLM Walk Cycle Judge — Qwen2.5-VL-7B via Ollama on Alienware
  5. Escalation — Gemini 2.5 Flash for borderline cases (stub)

Final composite: 0.15*hard_gates + 0.20*dino + 0.10*deterministic + 0.55*vlm
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, Protocol

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# ─── Constants ───────────────────────────────────────────────────────

AUTORESEARCH_DIR = Path(__file__).parent
REFERENCES_DIR = AUTORESEARCH_DIR / "references"
RESULTS_DIR = AUTORESEARCH_DIR / "results"

# Champion tile size = 128x128, Boss tile size = 256x256
CHAMPION_TILE = 128
BOSS_TILE = 256

# Green screen background color
GREEN_SCREEN = (0, 255, 0)
GREEN_SCREEN_HEX = "#00FF00"

# Outline color
OUTLINE_COLOR = (39, 41, 41)  # #272929

# Sean's 27-color palette (RGB tuples)
PALETTE_SEAN = [
    (39, 41, 41), (0, 0, 0), (255, 255, 255), (0, 255, 0),
    # Skin tones (5)
    (255, 224, 189), (240, 200, 160), (220, 180, 140), (200, 160, 120), (180, 140, 100),
    # Hair (3)
    (255, 230, 150), (230, 200, 120), (200, 170, 90),
    # Tank top (4)
    (255, 255, 255), (230, 230, 230), (200, 200, 200), (170, 170, 170),
    # Pants (5)
    (60, 80, 160), (50, 65, 140), (40, 55, 120), (30, 45, 100), (20, 35, 80),
    # Shoes (3)
    (255, 255, 255), (220, 220, 220), (180, 180, 180),
    # Outline shades (3) - includes main outline
    (39, 41, 41), (60, 62, 62), (80, 82, 82),
    # Eyes
    (80, 120, 200),
]

# Generic SF2 palette (38 colors) — used for non-Sean characters
PALETTE_SF2 = [
    (39, 41, 41), (0, 0, 0), (255, 255, 255), (0, 255, 0),
    # Extended skin tones
    (255, 224, 189), (240, 200, 160), (220, 180, 140), (200, 160, 120),
    (180, 140, 100), (160, 120, 80),
    # Hair variants
    (255, 230, 150), (230, 200, 120), (200, 170, 90), (60, 40, 20), (120, 80, 40),
    # Clothing (warm)
    (200, 50, 50), (180, 40, 40), (160, 30, 30), (255, 200, 50), (230, 180, 40),
    # Clothing (cool)
    (60, 80, 160), (50, 65, 140), (40, 55, 120), (30, 45, 100),
    (60, 160, 80), (50, 140, 70), (40, 120, 60),
    # Neutrals
    (255, 255, 255), (230, 230, 230), (200, 200, 200), (170, 170, 170),
    (140, 140, 140), (110, 110, 110), (80, 80, 80), (50, 50, 50),
    # Outline shades
    (39, 41, 41), (60, 62, 62), (80, 82, 82),
    # Accent
    (80, 120, 200), (200, 100, 50),
]

# Palette tolerance for quantization check (Euclidean distance in RGB space)
PALETTE_TOLERANCE = 30

# DINOv2 identity threshold
DINO_IDENTITY_THRESHOLD = 0.85

# VLM walk cycle weights
WALK_WEIGHTS = {
    "leg_differentiation": 0.25,
    "pose_progression": 0.20,
    "weight_shift": 0.20,
    "character_consistency": 0.15,
    "arm_swing": 0.10,
    "height_consistency": 0.10,
}

# Final composite weights
TIER_WEIGHTS = {
    "hard_gates": 0.15,
    "dino_identity": 0.20,
    "deterministic": 0.10,
    "vlm_walk": 0.55,
}

# VLM prompt — embedded as constant, never modified
VLM_WALK_CYCLE_PROMPT = """You are a pixel art animation quality judge for a 16-bit arcade fighting game (Street Fighter II style).

REFERENCE IMAGE: A real arcade game walk cycle showing the gold standard for leg differentiation, weight shift, and pose progression.

GENERATED IMAGE: A sprite sheet of walk cycle frames to evaluate. Each cell is one animation frame.

ANCHOR IMAGE: The approved character design — use this to verify the generated frames show the correct character.

A correct walk cycle MUST show these 4 distinct poses across its frames:
1. CONTACT: Front heel strikes ground, rear leg trails behind. Legs at widest spread. Arms at maximum opposite swing.
2. DOWN: Body at its LOWEST point. Front leg absorbs weight, knee bends. This is the heaviest frame.
3. PASSING: Legs together, rear leg swings forward past the planted leg. Body at mid-height.
4. UP: Body at its HIGHEST point. Rear leg pushes off, front leg extends forward. This is the lightest frame.

Score each criterion from 1 (worst) to 5 (best):

1. LEG_DIFFERENTIATION: Are leg positions distinctly different across frames? (1 = all frames look the same, 5 = clear contact/passing/up/down poses visible)
2. POSE_PROGRESSION: Do poses follow a logical walking sequence? (1 = random or repeated poses, 5 = smooth contact→down→passing→up→contact cycle)
3. WEIGHT_SHIFT: Does the character's body move up and down naturally? (1 = character floats at same height, 5 = visible dip at DOWN pose and rise at UP pose)
4. ARM_SWING: Do arms swing opposite to legs? (1 = arms static or identical, 5 = natural opposite-leg arm swing with offset)
5. CHARACTER_CONSISTENCY: Is it the same character in every frame? (1 = different features between frames, 5 = identical character with only pose changes)
6. HEIGHT_CONSISTENCY: Is the character roughly the same size in all frames? (1 = character grows/shrinks noticeably, 5 = consistent size, height varies only with walk bob)

Respond in this exact JSON format:
{
  "leg_differentiation": {"score": 1-5, "reasoning": "brief explanation"},
  "pose_progression": {"score": 1-5, "reasoning": "brief explanation"},
  "weight_shift": {"score": 1-5, "reasoning": "brief explanation"},
  "arm_swing": {"score": 1-5, "reasoning": "brief explanation"},
  "character_consistency": {"score": 1-5, "reasoning": "brief explanation"},
  "height_consistency": {"score": 1-5, "reasoning": "brief explanation"},
  "composite_score": 0.0-1.0,
  "primary_issue": "one sentence describing the biggest quality problem, or 'none' if all scores >= 4",
  "suggested_fix": "one sentence describing how to improve the generation prompt, or 'none'"
}

SCORING RULE: composite_score = (sum of all scores) / 30.0
If ANY score is 1, the walk cycle fundamentally fails — composite_score should not exceed 0.3."""


# ─── Data Classes ────────────────────────────────────────────────────

@dataclass
class ScoreResult:
    """Complete scoring result for one sprite sheet evaluation."""
    composite: float  # 0.0-1.0 final score
    hard_gates: dict[str, Any]  # Per-gate pass/fail
    dino_identity: float  # 0.0-1.0
    deterministic: dict[str, Any]  # Per-check scores
    vlm_scores: dict[str, Any]  # Per-criterion scores from VLM
    vlm_raw_response: str  # Full VLM JSON response
    primary_issue: str  # From VLM
    suggested_fix: str  # From VLM
    tier_reached: int  # 1-5, how far scoring got
    timestamp: float = field(default_factory=time.time)


# ─── VLM Adapter Protocol (Hexagonal Architecture) ──────────────────

class VLMAdapter(Protocol):
    """Port for VLM scoring — allows swapping Qwen for Gemini or others."""

    def score_walk_cycle(
        self,
        comparison_image: bytes,
        anchor_image: bytes,
    ) -> dict[str, Any]:
        """Score a walk cycle using the VLM rubric.

        Args:
            comparison_image: Side-by-side reference + generated (PNG bytes).
            anchor_image: Character anchor upscaled (PNG bytes).

        Returns:
            Dict with scores per criterion, composite_score, primary_issue, suggested_fix.
        """
        ...


class OllamaVLMAdapter:
    """Qwen2.5-VL-7B via Ollama REST API on Alienware."""

    def __init__(self, host: str = "192.168.68.201", port: int = 11434, timeout: int = 30):
        self.base_url = f"http://{host}:{port}"
        self.model = "qwen3-vl:8b"
        self.timeout = timeout

    def score_walk_cycle(
        self,
        comparison_image: bytes,
        anchor_image: bytes,
    ) -> dict[str, Any]:
        import base64
        import httpx

        comparison_b64 = base64.b64encode(comparison_image).decode()
        anchor_b64 = base64.b64encode(anchor_image).decode()

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": VLM_WALK_CYCLE_PROMPT,
                    "images": [comparison_b64, anchor_b64],
                }
            ],
            "stream": False,
            "options": {"temperature": 0.1},
        }

        try:
            resp = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data.get("message", {}).get("content", "")
            return self._parse_vlm_response(content)
        except httpx.ConnectError:
            logger.warning("Alienware/Ollama unreachable at %s — skipping VLM tier", self.base_url)
            return {}
        except httpx.TimeoutException:
            logger.warning("VLM request timed out after %ds — skipping VLM tier", self.timeout)
            return {}
        except Exception as e:
            logger.warning("VLM scoring failed: %s — skipping VLM tier", e)
            return {}

    def _parse_vlm_response(self, content: str) -> dict[str, Any]:
        """Parse JSON from VLM response, handling markdown code blocks."""
        # Strip markdown code blocks if present
        text = content.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json) and last line (```)
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            logger.warning("Could not parse VLM response as JSON")
            return {}


class GeminiEscalationAdapter:
    """Gemini 2.5 Flash escalation — stub for Phase 0."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.enabled = False  # Disabled for Phase 0

    def score_walk_cycle(
        self,
        comparison_image: bytes,
        anchor_image: bytes,
    ) -> dict[str, Any]:
        logger.info("Escalation would have fired (disabled for Phase 0)")
        return {}


# ─── Image Utilities ─────────────────────────────────────────────────

def upscale_nearest(image: Image.Image, scale: int = 4) -> Image.Image:
    """Upscale via nearest-neighbor to preserve pixel art."""
    return image.resize(
        (image.width * scale, image.height * scale),
        Image.Resampling.NEAREST,
    )


def compose_side_by_side(left: Image.Image, right: Image.Image, gap: int = 4) -> Image.Image:
    """Compose two images side-by-side with a gray gap."""
    max_h = max(left.height, right.height)
    combined = Image.new("RGB", (left.width + gap + right.width, max_h), (128, 128, 128))
    combined.paste(left, (0, 0))
    combined.paste(right, (left.width + gap, 0))
    return combined


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert PIL Image to bytes."""
    buf = BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def load_image(path_or_bytes: Path | bytes) -> Image.Image:
    """Load a PIL Image from path or bytes."""
    if isinstance(path_or_bytes, bytes):
        return Image.open(BytesIO(path_or_bytes))
    return Image.open(path_or_bytes)


# ─── Scorer ──────────────────────────────────────────────────────────

class AutoresearchScorer:
    """5-tier scoring pipeline for sprite sheet evaluation."""

    def __init__(
        self,
        character: str,
        animation_type: str,
        alienware_host: str = "192.168.68.201",
        skip_dino: bool = False,
        skip_vlm: bool = False,
        vlm_timeout: int = 30,
    ):
        self.character = character
        self.animation_type = animation_type
        self.skip_dino = skip_dino
        self.skip_vlm = skip_vlm

        # Determine tile size based on character type
        self.tile_size = self._get_tile_size(character)

        # Select palette
        self.palette = PALETTE_SEAN if character.lower() == "sean" else PALETTE_SF2

        # Load anchor images
        self.anchor_paths = self._find_anchors(character)

        # Load walk cycle references
        self.walk_ref_paths = self._find_walk_references()

        # VLM adapter (hexagonal — swappable)
        self.vlm_adapter: VLMAdapter = OllamaVLMAdapter(
            host=alienware_host,
            timeout=vlm_timeout,
        )
        self.escalation_adapter = GeminiEscalationAdapter()

        # DINOv2 model (lazy-loaded)
        self._dino_model = None
        self._dino_processor = None

    def _get_tile_size(self, character: str) -> int:
        """Determine tile size: 128 for champions, 256 for bosses."""
        bosses = {
            "gym bully", "procrastination phantom", "sloth demon",
            "stress titan", "training dummy", "ultimate slump",
        }
        return BOSS_TILE if character.lower() in bosses else CHAMPION_TILE

    def _find_anchors(self, character: str) -> list[Path]:
        """Find 3 anchor images for the character."""
        anchors_dir = REFERENCES_DIR / "anchors"
        # Search in champions and bosses
        for category in ["champions", "bosses"]:
            char_dir = anchors_dir / category / character
            if char_dir.exists():
                paths = sorted(char_dir.glob("*.png"))
                # Filter out .DS_Store and other non-anchor files
                paths = [p for p in paths if "anchor" in p.name.lower()]
                if paths:
                    return paths[:3]
        logger.warning("No anchors found for character: %s", character)
        return []

    def _find_walk_references(self) -> list[Path]:
        """Find walk cycle reference images."""
        walk_dir = REFERENCES_DIR / "walk_cycle"
        if walk_dir.exists():
            return sorted(walk_dir.glob("*.png"))
        return []

    def _load_dino(self):
        """Lazy-load DINOv2 model."""
        if self._dino_model is not None:
            return

        try:
            import torch
            from transformers import AutoImageProcessor, AutoModel

            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info("Loading DINOv2 on %s", device)

            self._dino_processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
            self._dino_model = AutoModel.from_pretrained("facebook/dinov2-base").to(device)
            self._dino_model.eval()
            self._dino_device = device
        except Exception as e:
            logger.warning("Could not load DINOv2: %s — skipping identity tier", e)
            self._dino_model = None

    def _get_dino_embedding(self, image: Image.Image) -> np.ndarray | None:
        """Extract CLS token embedding from DINOv2."""
        if self._dino_model is None:
            return None

        import torch

        inputs = self._dino_processor(images=image.convert("RGB"), return_tensors="pt")
        inputs = {k: v.to(self._dino_device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self._dino_model(**inputs)

        # CLS token is first token of last_hidden_state
        cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()
        return cls_embedding

    def score_sheet(self, sheet_path: Path, frames: list[Path]) -> ScoreResult:
        """Score a generated sprite sheet through all 5 tiers.

        Args:
            sheet_path: Path to the full sprite sheet image.
            frames: List of paths to individual frame images.

        Returns:
            ScoreResult with composite score and per-tier details.
        """
        timestamp = time.time()

        # ── Tier 1: Hard Gates ──
        hard_gates = self._tier1_hard_gates(frames)
        if not all(hard_gates.values()):
            return ScoreResult(
                composite=0.0,
                hard_gates=hard_gates,
                dino_identity=0.0,
                deterministic={},
                vlm_scores={},
                vlm_raw_response="",
                primary_issue=f"Hard gate failure: {[k for k, v in hard_gates.items() if not v]}",
                suggested_fix="Fix hard gate failures before evaluating quality",
                tier_reached=1,
                timestamp=timestamp,
            )

        hard_gate_score = 1.0  # Binary — all passed

        # ── Tier 2: DINOv2 Identity ──
        dino_score = self._tier2_dino_identity(frames)

        # ── Tier 3: Deterministic Checks ──
        deterministic = self._tier3_deterministic(frames)
        det_score = np.mean(list(deterministic.values())) if deterministic else 1.0

        # ── Tier 4: VLM Walk Cycle Judge ──
        vlm_scores = {}
        vlm_raw = ""
        vlm_walk_score = 0.5  # Default if VLM skipped
        primary_issue = "VLM scoring skipped"
        suggested_fix = "none"

        if not self.skip_vlm and self.animation_type in ("walk_forward", "walk_backward"):
            vlm_result = self._tier4_vlm_judge(sheet_path, frames)
            if vlm_result:
                vlm_scores = vlm_result
                vlm_raw = json.dumps(vlm_result, indent=2)
                vlm_walk_score = self._compute_vlm_composite(vlm_result)
                primary_issue = vlm_result.get("primary_issue", "unknown")
                suggested_fix = vlm_result.get("suggested_fix", "none")

                # ── Tier 5: Escalation check ──
                self._tier5_escalation_check(vlm_result)
        elif not self.skip_vlm:
            # Non-walk animations: VLM not applicable, use deterministic only
            vlm_walk_score = det_score  # Fall back to deterministic for non-walk
            primary_issue = f"VLM not applicable for {self.animation_type}"

        # ── Composite Score ──
        composite = (
            TIER_WEIGHTS["hard_gates"] * hard_gate_score
            + TIER_WEIGHTS["dino_identity"] * dino_score
            + TIER_WEIGHTS["deterministic"] * det_score
            + TIER_WEIGHTS["vlm_walk"] * vlm_walk_score
        )

        tier_reached = 5 if vlm_scores else (3 if not self.skip_vlm else 2)

        return ScoreResult(
            composite=round(composite, 4),
            hard_gates=hard_gates,
            dino_identity=round(dino_score, 4),
            deterministic=deterministic,
            vlm_scores=vlm_scores,
            vlm_raw_response=vlm_raw,
            primary_issue=primary_issue,
            suggested_fix=suggested_fix,
            tier_reached=tier_reached,
            timestamp=timestamp,
        )

    def score_dry_run(self) -> ScoreResult:
        """Generate a synthetic score for testing without generation."""
        import random

        return ScoreResult(
            composite=round(random.uniform(0.3, 0.8), 4),
            hard_gates={"dimensions": True, "palette": True, "background": True, "non_empty": True},
            dino_identity=round(random.uniform(0.7, 0.95), 4),
            deterministic={
                "frame_count": 1.0,
                "outline_present": round(random.uniform(0.6, 1.0), 2),
                "character_present": 1.0,
                "size_consistency": round(random.uniform(0.7, 1.0), 2),
            },
            vlm_scores={
                "leg_differentiation": {"score": random.randint(2, 4), "reasoning": "dry run"},
                "pose_progression": {"score": random.randint(2, 4), "reasoning": "dry run"},
                "weight_shift": {"score": random.randint(2, 4), "reasoning": "dry run"},
                "arm_swing": {"score": random.randint(2, 4), "reasoning": "dry run"},
                "character_consistency": {"score": random.randint(3, 5), "reasoning": "dry run"},
                "height_consistency": {"score": random.randint(3, 5), "reasoning": "dry run"},
                "composite_score": round(random.uniform(0.4, 0.8), 2),
                "primary_issue": "dry run — no real evaluation",
                "suggested_fix": "none",
            },
            vlm_raw_response='{"dry_run": true}',
            primary_issue="dry run — no real evaluation",
            suggested_fix="none",
            tier_reached=4,
        )

    # ── Tier 1: Hard Gates ───────────────────────────────────────────

    def _tier1_hard_gates(self, frames: list[Path]) -> dict[str, bool]:
        """Check each frame: dimensions, palette, background, non-empty."""
        results = {
            "dimensions": True,
            "palette": True,
            "background": True,
            "non_empty": True,
        }

        for frame_path in frames:
            try:
                img = Image.open(frame_path).convert("RGBA")
            except Exception as e:
                logger.warning("Cannot open frame %s: %s", frame_path, e)
                results["non_empty"] = False
                continue

            # Dimensions check
            if img.width != self.tile_size or img.height != self.tile_size:
                logger.info(
                    "Frame %s: expected %dx%d, got %dx%d",
                    frame_path.name, self.tile_size, self.tile_size, img.width, img.height,
                )
                results["dimensions"] = False

            # Non-empty check (has some opaque, non-green content)
            pixels = np.array(img)
            alpha = pixels[:, :, 3]
            rgb = pixels[:, :, :3]

            # Count opaque, non-green pixels
            opaque_mask = alpha > 128
            green_mask = (
                (np.abs(rgb[:, :, 0].astype(int) - GREEN_SCREEN[0]) < 20)
                & (np.abs(rgb[:, :, 1].astype(int) - GREEN_SCREEN[1]) < 20)
                & (np.abs(rgb[:, :, 2].astype(int) - GREEN_SCREEN[2]) < 20)
            )
            content_pixels = opaque_mask & ~green_mask
            content_ratio = content_pixels.sum() / max(opaque_mask.sum(), 1)

            if content_ratio < 0.01:
                logger.info("Frame %s: appears empty (content ratio: %.3f)", frame_path.name, content_ratio)
                results["non_empty"] = False

            # Background check: non-character area should be green or transparent
            transparent_mask = alpha < 128
            non_char_opaque = opaque_mask & ~content_pixels
            if non_char_opaque.sum() > 0:
                bg_colors = rgb[non_char_opaque]
                # Check if non-character opaque pixels are green
                bg_green = (
                    (np.abs(bg_colors[:, 0].astype(int) - GREEN_SCREEN[0]) < 30)
                    & (np.abs(bg_colors[:, 1].astype(int) - GREEN_SCREEN[1]) < 30)
                    & (np.abs(bg_colors[:, 2].astype(int) - GREEN_SCREEN[2]) < 30)
                )
                if bg_green.sum() / max(len(bg_green), 1) < 0.8:
                    # Allow if mostly transparent background instead
                    if transparent_mask.sum() / (img.width * img.height) < 0.2:
                        results["background"] = False

            # Palette compliance (soft check — within tolerance)
            if content_pixels.sum() > 0:
                char_colors = rgb[content_pixels]
                # Sample up to 1000 pixels for speed
                if len(char_colors) > 1000:
                    indices = np.random.choice(len(char_colors), 1000, replace=False)
                    char_colors = char_colors[indices]

                palette_arr = np.array(self.palette)
                off_palette = 0
                for color in char_colors:
                    distances = np.sqrt(np.sum((palette_arr - color.astype(float)) ** 2, axis=1))
                    if distances.min() > PALETTE_TOLERANCE:
                        off_palette += 1

                off_ratio = off_palette / len(char_colors)
                if off_ratio > 0.15:  # More than 15% off-palette
                    logger.info(
                        "Frame %s: %.1f%% off-palette pixels",
                        frame_path.name, off_ratio * 100,
                    )
                    results["palette"] = False

        return results

    # ── Tier 2: DINOv2 Identity ──────────────────────────────────────

    def _tier2_dino_identity(self, frames: list[Path]) -> float:
        """Cosine similarity between frame embeddings and anchor embeddings."""
        if self.skip_dino or not self.anchor_paths:
            return 1.0  # Default to pass if skipped

        self._load_dino()
        if self._dino_model is None:
            return 1.0  # Graceful skip

        # Get anchor embedding (average of available anchors)
        anchor_embeddings = []
        for anchor_path in self.anchor_paths:
            try:
                anchor_img = Image.open(anchor_path).convert("RGB")
                emb = self._get_dino_embedding(anchor_img)
                if emb is not None:
                    anchor_embeddings.append(emb)
            except Exception as e:
                logger.warning("Could not process anchor %s: %s", anchor_path.name, e)

        if not anchor_embeddings:
            return 1.0

        anchor_mean = np.mean(anchor_embeddings, axis=0)

        # Get frame embeddings and compute similarity
        similarities = []
        for frame_path in frames:
            try:
                frame_img = Image.open(frame_path).convert("RGB")
                emb = self._get_dino_embedding(frame_img)
                if emb is not None:
                    cos_sim = np.dot(anchor_mean, emb) / (
                        np.linalg.norm(anchor_mean) * np.linalg.norm(emb) + 1e-8
                    )
                    similarities.append(float(cos_sim))
            except Exception as e:
                logger.warning("Could not process frame %s: %s", frame_path.name, e)

        if not similarities:
            return 1.0

        return float(np.mean(similarities))

    # ── Tier 3: Deterministic Checks ─────────────────────────────────

    def _tier3_deterministic(self, frames: list[Path]) -> dict[str, float]:
        """Frame count, outline weight, character presence, size consistency."""
        results = {}

        # Frame count check
        expected = 4  # Walk cycles use 4 keyframes for IMAGE_ONLY/HYBRID
        results["frame_count"] = 1.0 if len(frames) == expected else max(0.0, 1.0 - abs(len(frames) - expected) * 0.25)

        # Per-frame checks
        outline_scores = []
        presence_scores = []
        bboxes = []

        for frame_path in frames:
            try:
                img = Image.open(frame_path).convert("RGBA")
                pixels = np.array(img)
                rgb = pixels[:, :, :3]
                alpha = pixels[:, :, 3]

                # Character presence: opaque non-green pixels should be 5-80% of frame
                opaque = alpha > 128
                green = (
                    (np.abs(rgb[:, :, 0].astype(int) - GREEN_SCREEN[0]) < 20)
                    & (np.abs(rgb[:, :, 1].astype(int) - GREEN_SCREEN[1]) < 20)
                    & (np.abs(rgb[:, :, 2].astype(int) - GREEN_SCREEN[2]) < 20)
                )
                content = opaque & ~green
                content_ratio = content.sum() / (img.width * img.height)

                if 0.05 <= content_ratio <= 0.80:
                    presence_scores.append(1.0)
                else:
                    presence_scores.append(0.5)

                # Outline check: dark outline pixels present but not dominant
                outline_near = (
                    (np.abs(rgb[:, :, 0].astype(int) - OUTLINE_COLOR[0]) < 15)
                    & (np.abs(rgb[:, :, 1].astype(int) - OUTLINE_COLOR[1]) < 15)
                    & (np.abs(rgb[:, :, 2].astype(int) - OUTLINE_COLOR[2]) < 15)
                    & opaque
                )
                outline_ratio = outline_near.sum() / max(content.sum(), 1)

                if 0.01 < outline_ratio < 0.50:
                    outline_scores.append(1.0)
                elif outline_ratio >= 0.50:
                    outline_scores.append(0.5)  # Too many outline pixels
                else:
                    outline_scores.append(0.7)  # No outlines detected (not necessarily bad)

                # Bounding box of character content
                if content.any():
                    rows = np.any(content, axis=1)
                    cols = np.any(content, axis=0)
                    rmin, rmax = np.where(rows)[0][[0, -1]]
                    cmin, cmax = np.where(cols)[0][[0, -1]]
                    bboxes.append((rmax - rmin, cmax - cmin))

            except Exception as e:
                logger.warning("Deterministic check failed for %s: %s", frame_path.name, e)
                presence_scores.append(0.0)
                outline_scores.append(0.0)

        results["outline_present"] = float(np.mean(outline_scores)) if outline_scores else 0.0
        results["character_present"] = float(np.mean(presence_scores)) if presence_scores else 0.0

        # Size consistency: bounding boxes should be within 20% of each other
        if len(bboxes) >= 2:
            heights = [b[0] for b in bboxes]
            widths = [b[1] for b in bboxes]
            h_var = (max(heights) - min(heights)) / max(max(heights), 1)
            w_var = (max(widths) - min(widths)) / max(max(widths), 1)
            if h_var < 0.20 and w_var < 0.20:
                results["size_consistency"] = 1.0
            elif h_var < 0.30 and w_var < 0.30:
                results["size_consistency"] = 0.7
            else:
                results["size_consistency"] = 0.4
        else:
            results["size_consistency"] = 1.0

        return results

    # ── Tier 4: VLM Walk Cycle Judge ─────────────────────────────────

    def _tier4_vlm_judge(self, sheet_path: Path, frames: list[Path]) -> dict[str, Any]:
        """VLM evaluation of walk cycle quality."""
        # 1. Upscale each frame 4x via nearest-neighbor
        # 2. Compose comparison image: walk ref (left) | gap | generated sheet (right)
        # 3. Upscale anchor-1 for identity context
        # 4. Send to VLM

        # Load and upscale the generated sheet
        try:
            sheet_img = Image.open(sheet_path).convert("RGB")
            sheet_upscaled = upscale_nearest(sheet_img)
        except Exception as e:
            logger.warning("Could not load sheet for VLM: %s", e)
            return {}

        # Load best walk cycle reference
        if not self.walk_ref_paths:
            logger.warning("No walk cycle references found — skipping VLM")
            return {}

        try:
            ref_img = Image.open(self.walk_ref_paths[0]).convert("RGB")
            # Scale reference to match generated sheet height
            scale = sheet_upscaled.height / max(ref_img.height, 1)
            ref_resized = ref_img.resize(
                (int(ref_img.width * scale), sheet_upscaled.height),
                Image.Resampling.NEAREST,
            )
        except Exception as e:
            logger.warning("Could not load walk reference: %s", e)
            return {}

        # Compose side-by-side: reference (left) | gap | generated (right)
        comparison = compose_side_by_side(ref_resized, sheet_upscaled)
        comparison_bytes = image_to_bytes(comparison)

        # Load anchor-1 upscaled
        anchor_bytes = b""
        if self.anchor_paths:
            try:
                anchor_img = Image.open(self.anchor_paths[0]).convert("RGB")
                anchor_upscaled = upscale_nearest(anchor_img)
                anchor_bytes = image_to_bytes(anchor_upscaled)
            except Exception as e:
                logger.warning("Could not load anchor for VLM: %s", e)

        if not anchor_bytes:
            anchor_bytes = comparison_bytes  # Fallback

        return self.vlm_adapter.score_walk_cycle(comparison_bytes, anchor_bytes)

    def _compute_vlm_composite(self, vlm_result: dict[str, Any]) -> float:
        """Compute weighted VLM score from individual criteria."""
        total = 0.0
        weight_sum = 0.0

        for criterion, weight in WALK_WEIGHTS.items():
            entry = vlm_result.get(criterion)
            if isinstance(entry, dict) and "score" in entry:
                score = entry["score"]
                total += weight * (score / 5.0)
                weight_sum += weight
            elif isinstance(entry, (int, float)):
                total += weight * (entry / 5.0)
                weight_sum += weight

        if weight_sum > 0:
            return total / weight_sum
        return vlm_result.get("composite_score", 0.5)

    # ── Tier 5: Escalation ───────────────────────────────────────────

    def _tier5_escalation_check(self, vlm_result: dict[str, Any]) -> None:
        """Check if escalation should fire (stub for Phase 0)."""
        # Escalation fires when any VLM score = 3 (borderline)
        borderline = False
        for criterion in WALK_WEIGHTS:
            entry = vlm_result.get(criterion)
            if isinstance(entry, dict) and entry.get("score") == 3:
                borderline = True
                break

        if borderline:
            logger.info(
                "Escalation would fire (borderline VLM scores) — disabled for Phase 0"
            )
