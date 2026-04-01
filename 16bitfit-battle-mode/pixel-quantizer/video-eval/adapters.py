"""Video model adapter interfaces and implementations.

Hexagonal architecture: all external video/image generation models
are accessed through typed Adapter interfaces. Core evaluation logic
never touches external APIs directly.

Four atomic operations (matching the sprite pipeline spec):
  - generate_frame: Single frame from anchor + pose ref
  - generate_keyframes: Multiple keyframes for video interpolation
  - interpolate_frames: Video model fills between keyframes
  - generate_video: Motion transfer from reference video
"""

from __future__ import annotations

import json
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add agents-sdk to path for keychain access
REPO_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))


@dataclass
class GeneratedFrame:
    """A single generated frame (image bytes + metadata)."""
    data: bytes
    width: int
    height: int
    format: str = "png"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedVideo:
    """Video output from a model (raw bytes + metadata)."""
    data: bytes
    duration_secs: float
    fps: int
    width: int
    height: int
    format: str = "mp4"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyframeConfig:
    """Configuration for keyframe generation."""
    character_name: str
    animation_type: str  # "walk", "idle", "punch", etc.
    start_pose: str  # Description of start pose
    end_pose: str  # Description of end pose
    width: int = 128
    height: int = 128
    style: str = "SF2 pixel art"
    background_color: str = "#00FF00"  # Chroma key green
    palette: dict[str, str] = field(default_factory=dict)


class VideoModelAdapter(ABC):
    """Abstract base for all video/image generation model adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable model name."""
        ...

    @property
    @abstractmethod
    def supports_keyframe_input(self) -> bool:
        """Whether this model accepts start/end frame images."""
        ...

    @property
    @abstractmethod
    def max_keyframes(self) -> int:
        """Maximum number of keyframes the model accepts."""
        ...

    @abstractmethod
    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        """Generate keyframe images for a given animation config."""
        ...

    @abstractmethod
    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        """Interpolate motion between keyframes to produce video."""
        ...

    async def generate_video(
        self,
        reference_image: GeneratedFrame,
        motion_description: str,
        duration_secs: float = 1.0,
    ) -> GeneratedVideo:
        """Generate video from a single image + motion description.

        Optional — not all models support this (motion transfer).
        """
        raise NotImplementedError(f"{self.name} does not support motion transfer")


class StubAdapter(VideoModelAdapter):
    """Stub adapter that returns synthetic frames for testing the eval pipeline."""

    def __init__(self, model_name: str = "stub"):
        self._name = model_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 5

    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        """Generate synthetic keyframes (solid color with green background)."""
        frames = []
        for i in range(3):  # 3 keyframes: start, mid, end
            # Create a minimal valid PNG-like payload for testing
            frame = _create_synthetic_frame(
                config.width, config.height, config.background_color, i
            )
            frames.append(frame)
        return frames

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        """Return a synthetic video (sequence of frames as fake mp4 bytes)."""
        total_frames = int(duration_secs * fps)

        # Create synthetic frame data for each interpolated frame
        frames_data = []
        for i in range(total_frames):
            frame = _create_synthetic_frame(128, 128, "#00FF00", i)
            frames_data.append(frame.data)

        # Pack frames as a simple binary blob (not a real video container)
        video_data = b"".join(frames_data)

        return GeneratedVideo(
            data=video_data,
            duration_secs=duration_secs,
            fps=fps,
            width=128,
            height=128,
            format="raw_frames",
            metadata={
                "adapter": self._name,
                "keyframe_count": len(keyframes),
                "total_frames": total_frames,
                "frames": frames_data,  # Store individual frame bytes
            },
        )


class GeminiAdapter(VideoModelAdapter):
    """Adapter for Google Gemini image generation (Nano Banana Pro / NB2).

    Uses Google AI API for keyframe generation.
    Key from Keychain as 'google-ai-key'.
    """

    def __init__(self, model_id: str = "gemini-3-pro-image-preview"):
        self._model_id = model_id

    @property
    def name(self) -> str:
        model_names = {
            "gemini-3-pro-image-preview": "Nano Banana Pro",
            "gemini-3.1-flash-image-preview": "Nano Banana 2",
        }
        return model_names.get(self._model_id, self._model_id)

    @property
    def supports_keyframe_input(self) -> bool:
        return False  # Gemini generates images, doesn't interpolate

    @property
    def max_keyframes(self) -> int:
        return 0

    def _get_api_key(self) -> str:
        from lib.keychain import get_credential
        key = get_credential("google-ai-key")
        if not key:
            raise RuntimeError("google-ai-key not found in Keychain")
        return key

    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        """Generate keyframes using Gemini image generation API."""
        import httpx

        api_key = self._get_api_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model_id}:generateContent"

        palette_desc = ", ".join(f"{k}: {v}" for k, v in config.palette.items())

        frames: list[GeneratedFrame] = []
        for pose_desc in [config.start_pose, config.end_pose]:
            prompt = (
                f"Generate a {config.width}x{config.height} pixel art sprite of a fighting game character "
                f"in {config.style} style. Character: {config.character_name}. "
                f"Pose: {pose_desc}. "
                f"Background: solid chroma key green ({config.background_color}). "
                f"Bold #272929 dark outlines (2-3px). 3-4 tone cel shading. "
                f"No anti-aliasing, no gradients. "
                f"Color palette: {palette_desc}. "
                f"Character facing RIGHT."
            )

            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    url,
                    params={"key": api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "responseModalities": ["IMAGE", "TEXT"],
                            "responseMimeType": "image/png",
                        },
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                # Extract image from response
                image_data = None
                for candidate in data.get("candidates", []):
                    for part in candidate.get("content", {}).get("parts", []):
                        if "inlineData" in part:
                            import base64
                            image_data = base64.b64decode(part["inlineData"]["data"])
                            break

                if image_data:
                    frames.append(GeneratedFrame(
                        data=image_data,
                        width=config.width,
                        height=config.height,
                        metadata={"model": self._model_id, "pose": pose_desc},
                    ))
                else:
                    raise RuntimeError(f"No image in Gemini response for pose: {pose_desc}")

        return frames

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        raise NotImplementedError("Gemini is an image model, not a video model")


class PikaAdapter(VideoModelAdapter):
    """Adapter for Pika Pikaframes 2.2 via fal.ai API.

    Supports up to 5 keyframes for video interpolation.
    Key from Keychain as 'fal-ai-key'.
    """

    def __init__(self):
        self._model_id = "fal-ai/pikaframes-2.2"

    @property
    def name(self) -> str:
        return "Pika Pikaframes 2.2"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 5

    def _get_api_key(self) -> str:
        from lib.keychain import get_credential
        key = get_credential("fal-ai-key")
        if not key:
            raise RuntimeError("fal-ai-key not found in Keychain")
        return key

    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        raise NotImplementedError("Use GeminiAdapter for keyframe generation, PikaAdapter for interpolation")

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        """Send keyframes to Pika via fal.ai for video interpolation."""
        import base64
        import httpx

        api_key = self._get_api_key()

        # Convert keyframes to base64 data URIs
        image_inputs = []
        for kf in keyframes:
            b64 = base64.b64encode(kf.data).decode()
            image_inputs.append(f"data:image/png;base64,{b64}")

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Submit job to fal.ai
            resp = await client.post(
                "https://queue.fal.run/fal-ai/pikaframes-2.2",
                headers={
                    "Authorization": f"Key {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "images": image_inputs,
                    "duration": duration_secs,
                    "fps": fps,
                    "prompt": "Smooth animation interpolation between keyframes, maintain character identity and pixel art style",
                },
            )
            resp.raise_for_status()
            result = resp.json()

            # Poll for completion if async
            if "request_id" in result:
                request_id = result["request_id"]
                for _ in range(60):  # Max 60 polls
                    status_resp = await client.get(
                        f"https://queue.fal.run/fal-ai/pikaframes-2.2/requests/{request_id}/status",
                        headers={"Authorization": f"Key {api_key}"},
                    )
                    status_data = status_resp.json()
                    if status_data.get("status") == "COMPLETED":
                        result_resp = await client.get(
                            f"https://queue.fal.run/fal-ai/pikaframes-2.2/requests/{request_id}",
                            headers={"Authorization": f"Key {api_key}"},
                        )
                        result = result_resp.json()
                        break
                    await __import__("asyncio").sleep(2)

            # Download video from result URL
            video_url = result.get("video", {}).get("url")
            if not video_url:
                raise RuntimeError(f"No video URL in Pika response: {json.dumps(result)[:200]}")

            video_resp = await client.get(video_url)
            video_data = video_resp.content

        return GeneratedVideo(
            data=video_data,
            duration_secs=duration_secs,
            fps=fps,
            width=keyframes[0].width if keyframes else 128,
            height=keyframes[0].height if keyframes else 128,
            format="mp4",
            metadata={"adapter": "pika", "keyframe_count": len(keyframes)},
        )


class KlingAdapter(VideoModelAdapter):
    """Stub adapter for Kling 3.0 — to be implemented when API access is available."""

    @property
    def name(self) -> str:
        return "Kling 3.0"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 2  # Start/end frame

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError("Kling adapter not yet implemented")

    async def interpolate_frames(self, keyframes, duration_secs=1.0, fps=24) -> GeneratedVideo:
        raise NotImplementedError("Kling adapter not yet implemented")


class ReplicateAdapter(VideoModelAdapter):
    """Stub adapter for rd-animation on Replicate."""

    @property
    def name(self) -> str:
        return "rd-animation (Replicate)"

    @property
    def supports_keyframe_input(self) -> bool:
        return False

    @property
    def max_keyframes(self) -> int:
        return 0

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError("rd-animation adapter not yet implemented")

    async def interpolate_frames(self, keyframes, duration_secs=1.0, fps=24) -> GeneratedVideo:
        raise NotImplementedError("rd-animation adapter not yet implemented")


class Wan22Adapter(VideoModelAdapter):
    """Stub adapter for Wan 2.2 + pixel animation LoRAs via local ComfyUI."""

    @property
    def name(self) -> str:
        return "Wan 2.2 (Local ComfyUI)"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 2

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError("Wan 2.2 adapter not yet implemented")

    async def interpolate_frames(self, keyframes, duration_secs=1.0, fps=24) -> GeneratedVideo:
        raise NotImplementedError("Wan 2.2 adapter not yet implemented")


def _create_synthetic_frame(
    width: int, height: int, bg_color: str, frame_index: int
) -> GeneratedFrame:
    """Create a minimal synthetic frame for testing.

    Generates a simple colored rectangle as raw RGBA bytes.
    """
    # Parse hex color
    bg = bg_color.lstrip("#")
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)

    # Create pixel data: mostly green background with a small colored region
    # that shifts position based on frame_index (simulating motion)
    pixels = bytearray()
    char_x = 32 + (frame_index * 8) % 64  # Character position shifts

    for y in range(height):
        for x in range(width):
            if char_x <= x < char_x + 32 and 32 <= y < 96:
                # Character region (skin color)
                pixels.extend([0xF5, 0xD6, 0xC6, 0xFF])
            else:
                # Background (chroma key green)
                pixels.extend([r, g, b, 0xFF])

    return GeneratedFrame(
        data=bytes(pixels),
        width=width,
        height=height,
        format="rgba",
        metadata={"synthetic": True, "frame_index": frame_index},
    )
