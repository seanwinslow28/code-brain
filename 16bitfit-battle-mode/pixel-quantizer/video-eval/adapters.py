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
    """Adapter for Wan 2.2 + pixel animation LoRA via local ComfyUI on Alienware.

    Connects to ComfyUI REST API at 192.168.68.201:8188.
    Uses Wan 2.2 I2V checkpoint with styly-agents/Wan2-2-pixel-animate LoRA.
    SDPA attention only (NO xformers — crashes on RTX 5080 sm_120).
    """

    DEFAULT_HOST = "192.168.68.201"
    DEFAULT_PORT = 8188
    WORKFLOW_PATH = Path(__file__).parent / "workflows" / "wan22_i2v_pixel_animate.json"

    # Model filenames confirmed on Alienware (April 2026)
    # 5B ti2v model works with Wan22ImageToVideoLatent node
    # 14B i2v models have channel mismatches with current ComfyUI node implementations
    CHECKPOINT = "wan2.2_ti2v_5B_fp16.safetensors"
    CHECKPOINT_14B_HIGH = "wan2.2_i2v_high_noise_14B_fp16.safetensors"
    CHECKPOINT_14B_LOW = "wan2.2_i2v_low_noise_14B_fp16.safetensors"
    VAE = "wan2.2_vae.safetensors"

    def __init__(
        self,
        lora_strength: float = 0.85,
        host: str | None = None,
        port: int | None = None,
        use_lora: bool = True,
    ):
        self._lora_strength = lora_strength
        self.COMFYUI_HOST = host or self.DEFAULT_HOST
        self.COMFYUI_PORT = port or self.DEFAULT_PORT
        self._use_lora = use_lora

    @property
    def name(self) -> str:
        return "Wan 2.2 (Local ComfyUI)"

    @property
    def supports_keyframe_input(self) -> bool:
        return True  # Takes a static image and animates it

    @property
    def max_keyframes(self) -> int:
        return 1  # Wan 2.2 I2V takes a single input image

    async def generate_keyframes(self, config: KeyframeConfig) -> list[GeneratedFrame]:
        raise NotImplementedError(
            "Wan 2.2 is a video model. Use GeminiAdapter for keyframe generation, "
            "then Wan22Adapter.interpolate_frames() to animate."
        )

    async def interpolate_frames(
        self,
        keyframes: list[GeneratedFrame],
        duration_secs: float = 2.0,
        fps: int = 24,
    ) -> GeneratedVideo:
        """Send a keyframe to ComfyUI for Wan 2.2 I2V animation.

        Builds the workflow programmatically using ComfyUI's built-in
        Wan nodes (confirmed installed: comfy_extras/nodes_wan.py).

        Args:
            keyframes: List with at least one keyframe (first is used).
            duration_secs: Target duration (maps to frame count: 2s = 49 frames).
            fps: Target FPS (24 default).

        Returns:
            GeneratedVideo with the animated output.
        """
        import httpx
        import uuid

        if not keyframes:
            raise ValueError("At least one keyframe required")

        input_frame = keyframes[0]
        base_url = f"http://{self.COMFYUI_HOST}:{self.COMFYUI_PORT}"

        # Calculate frame count from duration (Wan 2.2 uses 49 frames for ~2s)
        frame_count = max(25, int(duration_secs * fps) + 1)

        async with httpx.AsyncClient(timeout=300.0) as client:
            # Step 1: Upload input image to ComfyUI
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

            # Step 2: Build workflow using confirmed Alienware nodes
            # UNETLoader + CLIPLoader + VAELoader → WanImageToVideo → KSampler → VAEDecode → VHS_VideoCombine
            positive_prompt = (
                "pixel art sprite animation, smooth walk cycle motion, "
                "chroma key green background preserved, bold dark outlines, "
                "SF2 fighting game style, no anti-aliasing"
            )
            negative_prompt = (
                "blurry, low quality, distorted, deformed, anti-aliased, "
                "gradient background, watermark, text"
            )

            prompt_data: dict[str, Any] = {
                # Load UNet (diffusion model)
                "1": {
                    "class_type": "UNETLoader",
                    "inputs": {
                        "unet_name": self.CHECKPOINT,
                        "weight_dtype": "default",
                    },
                },
                # Load CLIP text encoder
                "2": {
                    "class_type": "CLIPLoader",
                    "inputs": {
                        "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
                        "type": "wan",
                    },
                },
                # Load VAE
                "3": {
                    "class_type": "VAELoader",
                    "inputs": {
                        "vae_name": self.VAE,
                    },
                },
                # Load input image
                "4": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": uploaded_name,
                    },
                },
                # Positive prompt
                "5": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": positive_prompt,
                        "clip": ["2", 0],
                    },
                },
                # Negative prompt
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": negative_prompt,
                        "clip": ["2", 0],
                    },
                },
                # Wan 2.2 Image-to-Video latent (NOT WanImageToVideo — that's 2.1)
                "7": {
                    "class_type": "Wan22ImageToVideoLatent",
                    "inputs": {
                        "vae": ["3", 0],
                        "width": 480,
                        "height": 480,
                        "length": frame_count,
                        "batch_size": 1,
                        "start_image": ["4", 0],
                    },
                },
                # KSampler — SDPA attention only (NO xformers on RTX 5080 sm_120)
                # Wan22ImageToVideoLatent outputs [0]=LATENT only
                # Conditioning comes from CLIPTextEncode nodes 5 (positive) and 6 (negative)
                "8": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": 42,
                        "steps": 20,
                        "cfg": 5.0,
                        "sampler_name": "euler",
                        "scheduler": "normal",
                        "denoise": 1.0,
                        "model": ["1", 0],
                        "positive": ["5", 0],
                        "negative": ["6", 0],
                        "latent_image": ["7", 0],
                    },
                },
                # VAE Decode
                "9": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["8", 0],
                        "vae": ["3", 0],
                    },
                },
                # Save as video via VHS (confirmed installed)
                "10": {
                    "class_type": "VHS_VideoCombine",
                    "inputs": {
                        "images": ["9", 0],
                        "frame_rate": fps,
                        "loop_count": 0,
                        "filename_prefix": "wan22_sprite",
                        "format": "video/h264-mp4",
                        "pingpong": False,
                        "save_output": True,
                    },
                },
            }

            # Optionally add LoRA if enabled and available
            if self._use_lora:
                prompt_data["20"] = {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": "pixel-000020.safetensors",
                        "strength_model": self._lora_strength,
                        "strength_clip": self._lora_strength,
                        "model": ["1", 0],
                        "clip": ["2", 0],
                    },
                }
                # Rewire: prompts and sampler use LoRA-modified model/clip
                prompt_data["5"]["inputs"]["clip"] = ["20", 1]
                prompt_data["6"]["inputs"]["clip"] = ["20", 1]
                prompt_data["8"]["inputs"]["model"] = ["20", 0]

            # Step 3: Queue the workflow
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

            # Step 4: Poll for completion
            for _ in range(300):  # Max 10 min for video gen on RTX 5080 (14B model is large)
                history_resp = await client.get(f"{base_url}/history/{prompt_id}")
                if history_resp.status_code == 200:
                    history = history_resp.json()
                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})
                        if outputs:
                            break
                await __import__("asyncio").sleep(2)
            else:
                raise RuntimeError(
                    f"ComfyUI Wan 2.2 generation timed out after 6 minutes. "
                    f"Prompt ID: {prompt_id}"
                )

            # Step 5: Download output — handle both images and video
            frames_data: list[bytes] = []
            video_data = b""
            output_format = "raw_frames"

            for node_id, node_output in outputs.items():
                # Try video output first (VHS_VideoCombine uses "gifs" key, not "videos")
                video_key = "videos" if "videos" in node_output else "gifs" if "gifs" in node_output else None
                if video_key:
                    video_info = node_output[video_key][0]
                    video_resp = await client.get(
                        f"{base_url}/view",
                        params={
                            "filename": video_info["filename"],
                            "subfolder": video_info.get("subfolder", ""),
                            "type": video_info.get("type", "output"),
                        },
                    )
                    video_data = video_resp.content
                    output_format = "mp4"
                    break

                # Fallback: image output (SaveImage — individual frames)
                if "images" in node_output:
                    for img_info in node_output["images"]:
                        img_resp = await client.get(
                            f"{base_url}/view",
                            params={
                                "filename": img_info["filename"],
                                "subfolder": img_info.get("subfolder", ""),
                                "type": img_info.get("type", "output"),
                            },
                        )
                        if img_resp.status_code == 200:
                            frames_data.append(img_resp.content)

            if not video_data and not frames_data:
                raise RuntimeError(
                    f"No output from ComfyUI. Outputs: {json.dumps(outputs)[:300]}"
                )

        if output_format == "mp4":
            return GeneratedVideo(
                data=video_data,
                duration_secs=duration_secs,
                fps=fps,
                width=480,
                height=480,
                format="mp4",
                metadata={
                    "adapter": "wan22",
                    "lora": "Wan2-2-pixel-animate" if self._use_lora else "none",
                    "lora_strength": self._lora_strength if self._use_lora else 0,
                    "frame_count": frame_count,
                    "prompt_id": prompt_id,
                },
            )
        else:
            # Individual frames from SaveImage
            combined = b"".join(frames_data)
            return GeneratedVideo(
                data=combined,
                duration_secs=duration_secs,
                fps=fps,
                width=480,
                height=480,
                format="raw_frames",
                metadata={
                    "adapter": "wan22",
                    "lora": "Wan2-2-pixel-animate" if self._use_lora else "none",
                    "lora_strength": self._lora_strength if self._use_lora else 0,
                    "frame_count": len(frames_data),
                    "prompt_id": prompt_id,
                    "frames": frames_data,
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
                    "optional_interpolation_states": None,
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
                    "quality": 90,
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

            # Step 5: Download output
            video_data = b""
            for node_out in outputs.values():
                if "videos" in node_out:
                    video_info = node_out["videos"][0]
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
