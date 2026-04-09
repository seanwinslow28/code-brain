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
    anchor_images: list[str] = field(default_factory=list)  # Paths to reference PNGs (MUST be provided)
    description: str = ""  # Text description fallback when anchors unavailable


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

    GOLDEN RULE: Anchor reference images MUST be provided in KeyframeConfig.
    Every generation request includes the character's anchor PNGs so Gemini
    maintains character identity across frames. Text-only prompts produce
    inconsistent characters — never skip the anchors.
    """

    MAX_RETRIES = 3
    RETRY_BACKOFF_SECS = [5, 15, 30]  # Exponential-ish backoff

    def __init__(self, model_id: str = "gemini-3-pro-image-preview"):
        self._model_id = model_id
        self._anchor_cache: dict[str, list[dict]] = {}  # char_name → loaded anchor parts

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

    def _load_anchor_parts(self, config: KeyframeConfig) -> list[dict]:
        """Load anchor images as Gemini API parts. Cached per character.

        Returns list of inlineData parts ready for the API payload.
        Raises RuntimeError if no anchors are provided or found.
        """
        import base64

        cache_key = config.character_name
        if cache_key in self._anchor_cache:
            return self._anchor_cache[cache_key]

        if not config.anchor_images:
            raise RuntimeError(
                f"GOLDEN RULE VIOLATION: No anchor_images provided for {config.character_name}. "
                f"Every Gemini generation MUST include reference images for character consistency."
            )

        parts = []
        for img_path in config.anchor_images:
            p = Path(img_path)
            # Try both absolute and relative to repo root
            if not p.exists():
                p = REPO_ROOT / img_path
            if not p.exists():
                continue

            img_b64 = base64.b64encode(p.read_bytes()).decode()
            suffix = p.suffix.lower()
            mime = "image/png" if suffix == ".png" else "image/jpeg"
            parts.append({"inlineData": {"mimeType": mime, "data": img_b64}})

        if not parts:
            raise RuntimeError(
                f"GOLDEN RULE VIOLATION: None of the anchor images found for {config.character_name}: "
                f"{config.anchor_images}"
            )

        self._anchor_cache[cache_key] = parts
        return parts

    async def _call_with_retry(self, client, url: str, params: dict, payload: dict) -> dict:
        """Call Gemini API with retry + exponential backoff for 503/429 errors."""
        import asyncio as _asyncio

        last_error = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                resp = await client.post(url, params=params, json=payload)
                if resp.status_code in (503, 429):
                    wait = self.RETRY_BACKOFF_SECS[min(attempt, len(self.RETRY_BACKOFF_SECS) - 1)]
                    print(f"    Gemini {resp.status_code}, retrying in {wait}s (attempt {attempt + 1}/{self.MAX_RETRIES + 1})")
                    await _asyncio.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES:
                    wait = self.RETRY_BACKOFF_SECS[min(attempt, len(self.RETRY_BACKOFF_SECS) - 1)]
                    print(f"    Gemini error: {e}, retrying in {wait}s")
                    await _asyncio.sleep(wait)
                    continue
        raise last_error

    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        """Generate keyframes using Gemini image generation API.

        ALWAYS sends anchor reference images alongside the text prompt.
        Uses retry with backoff for rate limiting (503/429).
        """
        import httpx

        api_key = self._get_api_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model_id}:generateContent"

        # GOLDEN RULE: Load anchor images — every request includes them
        anchor_parts = self._load_anchor_parts(config)

        char_desc = config.description or config.character_name

        frames: list[GeneratedFrame] = []
        for pose_desc in [config.start_pose, config.end_pose]:
            prompt = (
                f"Generate a pixel art sprite of THIS EXACT CHARACTER shown in the reference images. "
                f"Match the character's appearance exactly: {char_desc}. "
                f"Same hair, clothing, body type, and color palette as the reference. "
                f"Pose: {pose_desc}. "
                f"Style: {config.style}, bold #272929 dark outlines (2-3px), 3-4 tone cel shading. "
                f"Background: solid chroma key green ({config.background_color}). "
                f"Character facing RIGHT. "
                f"No anti-aliasing, no gradients, no background scenery."
            )

            # Build multi-modal payload: anchor images + text prompt
            parts = list(anchor_parts) + [{"text": prompt}]

            async with httpx.AsyncClient(timeout=90.0) as client:
                data = await self._call_with_retry(
                    client, url,
                    params={"key": api_key},
                    payload={
                        "contents": [{"parts": parts}],
                        "generationConfig": {
                            "responseModalities": ["IMAGE", "TEXT"],
                        },
                    },
                )

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
    """Adapter for Retro Diffusion rd-animation on Replicate.

    Generates pixel art animations directly from an anchor image.
    May bypass Pixel Quantizer entirely if output is already clean pixel art.
    Key from Keychain as 'replicate-key'.
    """

    # Full model version hash from Replicate
    DEFAULT_VERSION = "a9f33da7d9a985064dbc2d99621b87da5b8a22ed4d412c3a1c34ab4b807a6d8f"

    def __init__(self, model_version: str | None = None):
        self._model_version = model_version or self.DEFAULT_VERSION

    @property
    def name(self) -> str:
        return "rd-animation (Replicate)"

    @property
    def supports_keyframe_input(self) -> bool:
        return False  # rd-animation takes a single anchor image + description

    @property
    def max_keyframes(self) -> int:
        return 1  # Single anchor image

    def _get_api_key(self) -> str:
        from lib.keychain import get_credential
        key = get_credential("replicate-key")
        if not key:
            raise RuntimeError("replicate-key not found in Keychain")
        return key

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError(
            "rd-animation generates animations, not keyframes. "
            "Use generate_video() with a single anchor image instead."
        )

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        raise NotImplementedError(
            "rd-animation doesn't interpolate between keyframes. "
            "Use generate_video() with a single anchor image instead."
        )

    async def generate_video(
        self,
        reference_image: GeneratedFrame,
        motion_description: str,
        duration_secs: float = 1.0,
    ) -> GeneratedVideo:
        """Generate pixel art animation from anchor image via Replicate API.

        Args:
            reference_image: The anchor sprite (e.g., NB2-generated keyframe).
            motion_description: What animation to create (e.g., "walk cycle").
            duration_secs: Approximate duration (rd-animation outputs frames, not video).

        Returns:
            GeneratedVideo with extracted frames in metadata.
        """
        import base64
        import httpx

        api_key = self._get_api_key()

        # Encode anchor image
        b64_image = base64.b64encode(reference_image.data).decode()
        data_uri = f"data:image/png;base64,{b64_image}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Create prediction with full version hash
            resp = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Prefer": "wait",  # Wait up to 60s for sync response
                },
                json={
                    "version": self._model_version,
                    "input": {
                        "image": data_uri,
                        "prompt": motion_description,
                    },
                },
            )
            resp.raise_for_status()
            prediction = resp.json()

            # Poll for completion
            prediction_url = prediction.get("urls", {}).get("get", "")
            if not prediction_url:
                prediction_url = f"https://api.replicate.com/v1/predictions/{prediction['id']}"

            for _ in range(90):  # Max 3 min polling
                status_resp = await client.get(
                    prediction_url,
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                status_data = status_resp.json()

                if status_data["status"] == "succeeded":
                    output = status_data.get("output")
                    break
                elif status_data["status"] == "failed":
                    raise RuntimeError(
                        f"rd-animation prediction failed: {status_data.get('error', 'unknown')}"
                    )
                await __import__("asyncio").sleep(2)
            else:
                raise RuntimeError("rd-animation prediction timed out after 3 minutes")

            # Download output (could be image URL or list of URLs)
            if isinstance(output, str):
                output = [output]

            frames_data: list[bytes] = []
            for url in output:
                img_resp = await client.get(url)
                frames_data.append(img_resp.content)

        # Pack frames into a GeneratedVideo
        video_data = b"".join(frames_data)
        return GeneratedVideo(
            data=video_data,
            duration_secs=duration_secs,
            fps=12,  # rd-animation typically outputs at sprite-friendly rates
            width=reference_image.width,
            height=reference_image.height,
            format="raw_frames",
            metadata={
                "adapter": "rd-animation",
                "model": self._model_version,
                "motion": motion_description,
                "frame_count": len(frames_data),
                "frames": frames_data,
            },
        )


class Wan22Adapter(VideoModelAdapter):
    """Adapter for Wan 2.2 14B Image-to-Video via local ComfyUI on Alienware.

    Uses the ComfyUI built-in template "Wan 2.2 14B Image to Video":
    - Dual 14B models (high_noise + low_noise) in fp8
    - LightX2V 4-step LoRA for fast generation
    - Two-stage KSamplerAdvanced (high noise → low noise)
    - WanImageToVideo node (NOT Wan22ImageToVideoLatent)
    - ModelSamplingSD3 shift=5.0
    - 640×640 resolution, 81 frames, 16 FPS

    SDPA attention only (NO xformers — crashes on RTX 5080 sm_120).
    """

    DEFAULT_HOST = "192.168.68.201"
    DEFAULT_PORT = 8188
    WORKFLOW_PATH = Path(__file__).parent / "workflows" / "wan22_14b_i2v_template.json"

    # 14B fp8 models (confirmed working with ComfyUI v0.3.52 template)
    CHECKPOINT_HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
    CHECKPOINT_LOW = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
    LORA_HIGH = "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors"
    LORA_LOW = "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors"
    CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
    VAE = "wan_2.1_vae.safetensors"

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        width: int = 832,
        height: int = 480,
        num_frames: int = 81,
        fps: int = 16,
    ):
        self.COMFYUI_HOST = host or self.DEFAULT_HOST
        self.COMFYUI_PORT = port or self.DEFAULT_PORT
        self._width = width
        self._height = height
        self._num_frames = num_frames
        self._fps = fps

    @property
    def name(self) -> str:
        return "Wan 2.2 14B I2V (Local ComfyUI)"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 1

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError(
            "Wan 2.2 is a video model. Use GeminiAdapter for keyframe generation, "
            "then Wan22Adapter.interpolate_frames() to animate."
        )

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 5.0,
        fps: int = 16,
    ) -> GeneratedVideo:
        """Animate a keyframe using Wan 2.2 14B dual-model I2V pipeline.

        Uses the confirmed-working ComfyUI template architecture:
        - Dual 14B models (high_noise + low_noise) in fp8
        - LightX2V 4-step LoRA for fast generation
        - Two-stage KSamplerAdvanced
        - WanImageToVideo node with proper conditioning
        - ModelSamplingSD3 shift=5.0

        Args:
            keyframes: List with at least one keyframe (first is used).
            duration_secs: Target duration (~5s for 81 frames at 16fps).
            fps: Target FPS (16 default, matching template).

        Returns:
            GeneratedVideo with the animated output.
        """
        import httpx
        import random
        import uuid

        if not keyframes:
            raise ValueError("At least one keyframe required")

        input_frame = keyframes[0]
        base_url = f"http://{self.COMFYUI_HOST}:{self.COMFYUI_PORT}"

        async with httpx.AsyncClient(timeout=600.0) as client:
            # Step 1: Upload input image
            input_filename = f"wan22_input_{uuid.uuid4().hex[:8]}.png"
            upload_resp = await client.post(
                f"{base_url}/upload/image",
                files={"image": (input_filename, input_frame.data, "image/png")},
            )
            if upload_resp.status_code != 200:
                raise RuntimeError(
                    f"ComfyUI image upload failed: {upload_resp.status_code} {upload_resp.text}"
                )
            uploaded_name = upload_resp.json().get("name", input_filename)

            # Step 2: Build the 14B dual-model workflow
            # This matches the ComfyUI built-in "Wan 2.2 14B Image to Video" template
            seed = random.randint(1, 2**53)

            prompt_data: dict[str, Any] = {
                # CLIP text encoder
                "84": {
                    "class_type": "CLIPLoader",
                    "inputs": {
                        "clip_name": self.CLIP,
                        "type": "wan",
                        "device": "default",
                    },
                },
                # VAE (uses wan_2.1_vae, NOT wan2.2_vae)
                "90": {
                    "class_type": "VAELoader",
                    "inputs": {"vae_name": self.VAE},
                },
                # Dual UNet loaders (14B fp8)
                "95": {
                    "class_type": "UNETLoader",
                    "inputs": {
                        "unet_name": self.CHECKPOINT_HIGH,
                        "weight_dtype": "default",
                    },
                },
                "96": {
                    "class_type": "UNETLoader",
                    "inputs": {
                        "unet_name": self.CHECKPOINT_LOW,
                        "weight_dtype": "default",
                    },
                },
                # Input image
                "97": {
                    "class_type": "LoadImage",
                    "inputs": {"image": uploaded_name},
                },
                # Positive prompt (keep it simple — template style)
                "93": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "pixel art character walking forward",
                        "clip": ["84", 0],
                    },
                },
                # Negative prompt
                "89": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "morphing, anti-aliasing",
                        "clip": ["84", 0],
                    },
                },
                # WanImageToVideo — the CORRECT I2V node
                "98": {
                    "class_type": "WanImageToVideo",
                    "inputs": {
                        "width": self._width,
                        "height": self._height,
                        "length": self._num_frames,
                        "batch_size": 1,
                        "positive": ["93", 0],
                        "negative": ["89", 0],
                        "vae": ["90", 0],
                        "start_image": ["97", 0],
                    },
                },
                # LightX2V 4-step LoRAs
                "101": {
                    "class_type": "LoraLoaderModelOnly",
                    "inputs": {
                        "lora_name": self.LORA_HIGH,
                        "strength_model": 1.0,
                        "model": ["95", 0],
                    },
                },
                "102": {
                    "class_type": "LoraLoaderModelOnly",
                    "inputs": {
                        "lora_name": self.LORA_LOW,
                        "strength_model": 1.0,
                        "model": ["96", 0],
                    },
                },
                # ModelSamplingSD3 shift=5.0
                "104": {
                    "class_type": "ModelSamplingSD3",
                    "inputs": {"shift": 5.0, "model": ["101", 0]},
                },
                "103": {
                    "class_type": "ModelSamplingSD3",
                    "inputs": {"shift": 5.0, "model": ["102", 0]},
                },
                # Two-stage KSamplerAdvanced
                # Stage 1: High noise model, steps 0-2, adds noise
                "86": {
                    "class_type": "KSamplerAdvanced",
                    "inputs": {
                        "add_noise": "enable",
                        "noise_seed": seed,
                        "steps": 4,
                        "cfg": 1.0,
                        "sampler_name": "euler",
                        "scheduler": "simple",
                        "start_at_step": 0,
                        "end_at_step": 2,
                        "return_with_leftover_noise": "enable",
                        "model": ["104", 0],
                        "positive": ["98", 0],
                        "negative": ["98", 1],
                        "latent_image": ["98", 2],
                    },
                },
                # Stage 2: Low noise model, steps 2-4, refines
                "85": {
                    "class_type": "KSamplerAdvanced",
                    "inputs": {
                        "add_noise": "disable",
                        "noise_seed": 0,
                        "steps": 4,
                        "cfg": 1.0,
                        "sampler_name": "euler",
                        "scheduler": "simple",
                        "start_at_step": 2,
                        "end_at_step": 4,
                        "return_with_leftover_noise": "disable",
                        "model": ["103", 0],
                        "positive": ["98", 0],
                        "negative": ["98", 1],
                        "latent_image": ["86", 0],
                    },
                },
                # VAE Decode
                "87": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["85", 0], "vae": ["90", 0]},
                },
                # Create + Save Video
                "94": {
                    "class_type": "CreateVideo",
                    "inputs": {"fps": float(self._fps), "images": ["87", 0]},
                },
                "108": {
                    "class_type": "SaveVideo",
                    "inputs": {
                        "filename_prefix": "wan22_14b_sprite",
                        "format": "mp4",
                        "codec": "h264",
                        "video-preview": "",
                        "video": ["94", 0],
                    },
                },
            }

            # Step 3: Queue
            client_id = uuid.uuid4().hex
            queue_resp = await client.post(
                f"{base_url}/prompt",
                json={"prompt": prompt_data, "client_id": client_id},
            )
            if queue_resp.status_code != 200:
                raise RuntimeError(
                    f"ComfyUI queue failed: {queue_resp.status_code} {queue_resp.text}"
                )

            prompt_id = queue_resp.json().get("prompt_id")

            # Step 4: Poll for completion (14B takes ~60-240s)
            for _ in range(300):
                history_resp = await client.get(f"{base_url}/history/{prompt_id}")
                if history_resp.status_code == 200:
                    history = history_resp.json()
                    if prompt_id in history:
                        status = history[prompt_id].get("status", {})
                        status_str = status.get("status_str", "")
                        if status_str == "error":
                            raise RuntimeError(
                                f"ComfyUI execution error: {json.dumps(status)[:500]}"
                            )
                        outputs = history[prompt_id].get("outputs", {})
                        if outputs:
                            break
                await __import__("asyncio").sleep(2)
            else:
                raise RuntimeError(
                    f"ComfyUI Wan 2.2 14B timed out after 10 min. Prompt: {prompt_id}"
                )

            # Step 5: Download video output
            # SaveVideo node stores output under "images" key (with animated=true),
            # VHS_VideoCombine uses "gifs" or "videos" key
            video_data = b""
            for node_id, node_output in outputs.items():
                for key in ("videos", "gifs", "images"):
                    if key in node_output:
                        for item in node_output[key]:
                            fn = item.get("filename", "")
                            if fn.endswith((".mp4", ".webm", ".gif")):
                                video_resp = await client.get(
                                    f"{base_url}/view",
                                    params={
                                        "filename": fn,
                                        "subfolder": item.get("subfolder", ""),
                                        "type": item.get("type", "output"),
                                    },
                                )
                                video_data = video_resp.content
                                break
                    if video_data:
                        break
                if video_data:
                    break

            if not video_data:
                raise RuntimeError(
                    f"No video output from Wan 2.2 14B. Outputs: {json.dumps(outputs)[:300]}"
                )

        return GeneratedVideo(
            data=video_data,
            duration_secs=self._num_frames / self._fps,
            fps=self._fps,
            width=self._width,
            height=self._height,
            format="mp4",
            metadata={
                "adapter": "wan22_14b",
                "models": "dual 14B fp8 (high_noise + low_noise)",
                "lora": "LightX2V 4-step",
                "resolution": f"{self._width}x{self._height}",
                "frames": self._num_frames,
                "prompt_id": prompt_id,
                "seed": seed,
            },
        )


class RIFEAdapter(VideoModelAdapter):
    """Adapter for RIFE VFI frame interpolation via ComfyUI on Alienware.

    Uses Fannovel16/ComfyUI-Frame-Interpolation node pack with RIFE VFI.
    Pure PyTorch — no cupy dependency (unlike GMFSS Fortuna which is blocked).
    Takes 2+ keyframes and interpolates smooth frames between them.
    LOCAL + FREE — no API costs.

    Confirmed results (Phase 3):
      - Character identity: PASS
      - Pose transitions: PASS
      - Green screen: PASS
      - Color expansion: 79K-103K unique colors (Pixel Quantizer handles this)
    """

    COMFYUI_HOST = "192.168.68.201"
    COMFYUI_PORT = 8188
    WORKFLOW_PATH = Path(__file__).parent / "workflows" / "rife_interpolation.json"
    CHECKPOINT = "rife49.pth"

    def __init__(self, multiplier: int = 4, host: str | None = None, port: int | None = None):
        """Args:
            multiplier: Frames to insert between each keyframe pair.
                        4 = inserts 3 frames (4x total).
            host: ComfyUI host override.
            port: ComfyUI port override.
        """
        self._multiplier = multiplier
        if host:
            self.COMFYUI_HOST = host
        if port:
            self.COMFYUI_PORT = port

    @property
    def name(self) -> str:
        return "RIFE VFI (Local)"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 5

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError(
            "RIFE VFI interpolates between existing keyframes. "
            "Use GeminiAdapter for keyframe generation first."
        )

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 12,
    ) -> GeneratedVideo:
        """Interpolate between keyframes using RIFE VFI (rife49.pth).

        Args:
            keyframes: 2-5 keyframes to interpolate between.
            duration_secs: Target duration (informational — actual depends on
                          keyframe count * multiplier).
            fps: Output FPS (12 recommended for pixel art).

        Returns:
            GeneratedVideo with interpolated frames.
        """
        import httpx
        import uuid

        if len(keyframes) < 2:
            raise ValueError("RIFE VFI needs at least 2 keyframes")

        base_url = f"http://{self.COMFYUI_HOST}:{self.COMFYUI_PORT}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Step 1: Upload all keyframes
            uploaded_names: list[str] = []
            for i, kf in enumerate(keyframes):
                filename = f"rife_kf_{i}_{uuid.uuid4().hex[:8]}.png"
                upload_resp = await client.post(
                    f"{base_url}/upload/image",
                    files={"image": (filename, kf.data, "image/png")},
                )
                if upload_resp.status_code != 200:
                    raise RuntimeError(
                        f"ComfyUI upload failed for keyframe {i}: "
                        f"{upload_resp.status_code}"
                    )
                uploaded_names.append(upload_resp.json().get("name", filename))

            # Step 2: Build dynamic workflow
            workflow_prompt: dict[str, Any] = {}
            node_id = 1

            # Load each keyframe image
            load_ids: list[int] = []
            for name in uploaded_names:
                workflow_prompt[str(node_id)] = {
                    "class_type": "LoadImage",
                    "inputs": {"image": name},
                }
                load_ids.append(node_id)
                node_id += 1

            # Chain ImageBatch nodes to combine keyframes
            if len(load_ids) == 2:
                workflow_prompt[str(node_id)] = {
                    "class_type": "ImageBatch",
                    "inputs": {
                        "image1": [str(load_ids[0]), 0],
                        "image2": [str(load_ids[1]), 0],
                    },
                }
                batch_id = node_id
                node_id += 1
            else:
                # Chain: batch(kf0, kf1) → batch(prev, kf2) → ...
                workflow_prompt[str(node_id)] = {
                    "class_type": "ImageBatch",
                    "inputs": {
                        "image1": [str(load_ids[0]), 0],
                        "image2": [str(load_ids[1]), 0],
                    },
                }
                prev_batch = node_id
                node_id += 1

                for extra_id in load_ids[2:]:
                    workflow_prompt[str(node_id)] = {
                        "class_type": "ImageBatch",
                        "inputs": {
                            "image1": [str(prev_batch), 0],
                            "image2": [str(extra_id), 0],
                        },
                    }
                    prev_batch = node_id
                    node_id += 1

                batch_id = prev_batch

            # RIFE VFI node (pure PyTorch, no cupy needed)
            rife_id = node_id
            workflow_prompt[str(rife_id)] = {
                "class_type": "RIFE VFI",
                "inputs": {
                    "ckpt_name": self.CHECKPOINT,
                    "frames": [str(batch_id), 0],
                    "clear_cache_after_n_frames": 10,
                    "multiplier": self._multiplier,
                    "fast_mode": True,
                    "ensemble": True,
                    "scale_factor": 1.0,
                    "dtype": "float16",
                    "torch_compile": False,
                    "batch_size": 1,
                },
            }
            node_id += 1

            # Save as video
            workflow_prompt[str(node_id)] = {
                "class_type": "VHS_VideoCombine",
                "inputs": {
                    "images": [str(rife_id), 0],
                    "frame_rate": fps,
                    "format": "video/h264-mp4",
                    "filename_prefix": "rife_interpolated",
                    "loop_count": 0,
                    "pingpong": False,
                    "save_output": True,
                },
            }

            # Step 3: Queue workflow
            client_id = uuid.uuid4().hex
            queue_resp = await client.post(
                f"{base_url}/prompt",
                json={"prompt": workflow_prompt, "client_id": client_id},
            )
            if queue_resp.status_code != 200:
                raise RuntimeError(
                    f"ComfyUI RIFE queue failed: {queue_resp.status_code} "
                    f"{queue_resp.text}"
                )

            prompt_id = queue_resp.json().get("prompt_id")

            # Step 4: Poll for completion (RIFE is fast — 30s max)
            for _ in range(30):
                history_resp = await client.get(f"{base_url}/history/{prompt_id}")
                if history_resp.status_code == 200:
                    history = history_resp.json()
                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})
                        if outputs:
                            break
                await __import__("asyncio").sleep(1)
            else:
                raise RuntimeError(
                    f"ComfyUI RIFE timed out after 30s. Prompt ID: {prompt_id}"
                )

            # Step 5: Download output (VHS_VideoCombine stores under "gifs" key)
            video_data = b""
            for node_out in outputs.values():
                for key in ("gifs", "videos"):
                    if key in node_out:
                        video_info = node_out[key][0]
                        video_resp = await client.get(
                            f"{base_url}/view",
                            params={
                                "filename": video_info["filename"],
                                "subfolder": video_info.get("subfolder", ""),
                                "type": video_info.get("type", "output"),
                            },
                        )
                        video_data = video_resp.content
                        break
                if video_data:
                    break

            if not video_data:
                raise RuntimeError("No video output from RIFE VFI")

        total_frames = (len(keyframes) - 1) * self._multiplier + 1
        actual_duration = total_frames / fps if fps > 0 else duration_secs
        return GeneratedVideo(
            data=video_data,
            duration_secs=actual_duration,
            fps=fps,
            width=keyframes[0].width,
            height=keyframes[0].height,
            format="mp4",
            metadata={
                "adapter": "rife_vfi",
                "checkpoint": self.CHECKPOINT,
                "multiplier": self._multiplier,
                "keyframe_count": len(keyframes),
                "total_frames": total_frames,
                "prompt_id": prompt_id,
            },
        )


# Backward-compatible alias
GMFSSAdapter = RIFEAdapter


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


# ─── PixelLab Adapter ────────────────────────────────────────────────


class PixelLabAdapter(VideoModelAdapter):
    """Adapter for PixelLab API — native pixel art generation + animation.

    PixelLab offers:
    - "Generate Sprite": single-frame pixel art from text/image prompt
    - "Animate with Skeleton": skeleton-based animation between poses
    - "Estimate Skeleton": extract pose skeleton from an image
    - Max output: 128×128 (matches Champion tile size)
    - Pricing: $0.007-$0.016 per generation
    - Native pixel art output — may NOT need Pixel Quantizer post-processing

    API docs: https://api.pixellab.ai/v1/docs
    API key from macOS Keychain as 'pixel_lab_api_key'.
    """

    BASE_URL = "https://api.pixellab.ai/v1"

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "PixelLab"

    @property
    def supports_keyframe_input(self) -> bool:
        return True  # Supports start/end skeleton for animation

    @property
    def max_keyframes(self) -> int:
        return 2  # Animate with Skeleton: start + end pose

    def _get_api_key(self) -> str:
        if self._api_key:
            return self._api_key
        from lib.keychain import get_credential
        key = get_credential("pixel_lab_api_key")
        if not key:
            raise RuntimeError("pixel_lab_api_key not found in Keychain")
        return key

    async def generate_keyframes(
        self, config: KeyframeConfig
    ) -> list[GeneratedFrame]:
        """Generate keyframe sprites using PixelLab's 'Generate Sprite' endpoint."""
        import base64
        import httpx

        api_key = self._get_api_key()
        frames: list[GeneratedFrame] = []

        for pose_desc in [config.start_pose, config.end_pose]:
            prompt = (
                f"A {config.width}x{config.height} pixel art sprite of {config.character_name}, "
                f"{config.style} style, {pose_desc}, "
                f"solid green (#00FF00) background, facing right, "
                f"bold dark outlines"
            )

            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.BASE_URL}/generate-sprite",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "description": prompt,
                        "image_size": {"width": config.width, "height": config.height},
                        "style": "pixel_art",
                        "background_color": config.background_color,
                        # TODO: Verify exact API field names when SDK is available
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                # TODO: Adapt response parsing to actual API response format
                image_data = base64.b64decode(data.get("image", data.get("data", "")))

                frames.append(GeneratedFrame(
                    data=image_data,
                    width=config.width,
                    height=config.height,
                    metadata={"adapter": "pixellab", "pose": pose_desc},
                ))

        return frames

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 12,
    ) -> GeneratedVideo:
        """Animate between keyframes using 'Animate with Skeleton' endpoint.

        PixelLab takes start/end frame + skeleton data and generates
        in-between frames with proper pixel art interpolation.
        """
        import base64
        import httpx

        if len(keyframes) < 2:
            raise ValueError("PixelLab animation requires at least 2 keyframes")

        api_key = self._get_api_key()
        target_frames = int(duration_secs * fps)

        start_b64 = base64.b64encode(keyframes[0].data).decode()
        end_b64 = base64.b64encode(keyframes[-1].data).decode()

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{self.BASE_URL}/animate-with-skeleton",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "start_image": start_b64,
                    "end_image": end_b64,
                    "num_frames": target_frames,
                    "style": "pixel_art",
                    # TODO: Verify exact API field names — "Estimate Skeleton"
                    # may need to be called first to get skeleton data
                },
            )
            resp.raise_for_status()
            data = resp.json()

            # TODO: Adapt response parsing to actual API format
            # Expected: list of frame images in base64
            frame_images = data.get("frames", [])
            frames_data = [base64.b64decode(f) for f in frame_images]

        video_data = b"".join(frames_data)
        return GeneratedVideo(
            data=video_data,
            duration_secs=duration_secs,
            fps=fps,
            width=keyframes[0].width,
            height=keyframes[0].height,
            format="raw_frames",
            metadata={
                "adapter": "pixellab",
                "frame_count": len(frames_data),
                "frames": frames_data,
            },
        )

    async def generate_video(
        self,
        reference_image: GeneratedFrame,
        motion_description: str,
        duration_secs: float = 1.0,
    ) -> GeneratedVideo:
        """Generate animation from a single reference image + motion description.

        Uses 'Animate with Skeleton' with auto-estimated end pose.
        """
        import base64
        import httpx

        api_key = self._get_api_key()
        ref_b64 = base64.b64encode(reference_image.data).decode()
        target_frames = int(duration_secs * 12)

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Step 1: Estimate skeleton from reference
            skel_resp = await client.post(
                f"{self.BASE_URL}/estimate-skeleton",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={"image": ref_b64},
            )
            skel_resp.raise_for_status()
            skeleton = skel_resp.json()

            # Step 2: Animate with skeleton + motion description
            resp = await client.post(
                f"{self.BASE_URL}/animate-with-skeleton",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "start_image": ref_b64,
                    "skeleton": skeleton,
                    "motion_description": motion_description,
                    "num_frames": target_frames,
                    "style": "pixel_art",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            frame_images = data.get("frames", [])
            frames_data = [base64.b64decode(f) for f in frame_images]

        video_data = b"".join(frames_data)
        return GeneratedVideo(
            data=video_data,
            duration_secs=duration_secs,
            fps=12,
            width=reference_image.width,
            height=reference_image.height,
            format="raw_frames",
            metadata={
                "adapter": "pixellab",
                "motion": motion_description,
                "frame_count": len(frames_data),
                "frames": frames_data,
            },
        )


class StubPixelLabAdapter(VideoModelAdapter):
    """Stub PixelLab adapter for dry-run testing. Returns synthetic frames."""

    @property
    def name(self) -> str:
        return "PixelLab (stub)"

    @property
    def supports_keyframe_input(self) -> bool:
        return True

    @property
    def max_keyframes(self) -> int:
        return 2

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        frames = []
        for i in range(2):
            frame = _create_synthetic_frame(config.width, config.height, config.background_color, i)
            frame.metadata["adapter"] = "pixellab-stub"
            frames.append(frame)
        return frames

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 1.0,
        fps: int = 12,
    ) -> GeneratedVideo:
        total = int(duration_secs * fps)
        frames_data = []
        for i in range(total):
            f = _create_synthetic_frame(128, 128, "#00FF00", i)
            frames_data.append(f.data)

        return GeneratedVideo(
            data=b"".join(frames_data),
            duration_secs=duration_secs,
            fps=fps,
            width=128,
            height=128,
            format="raw_frames",
            metadata={"adapter": "pixellab-stub", "frame_count": total, "frames": frames_data},
        )
