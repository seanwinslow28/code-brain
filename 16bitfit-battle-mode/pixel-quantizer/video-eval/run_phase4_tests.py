#!/usr/bin/env python3
"""Phase 4 video model tests — Wan 2.2 LoRA + stronger motion prompts.

Task 5: Test Wan 2.2 with the pixel-000020 LoRA vs without LoRA.
Task 6: Test stronger motion prompts to push for actual locomotion.

Requires: Alienware online at 192.168.68.201:8188 with ComfyUI running.
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
import uuid
from pathlib import Path

# Add agents-sdk to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "agents-sdk"))

COMFYUI_HOST = "192.168.68.201"
COMFYUI_PORT = 8188
BASE_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

EVAL_RESULTS = Path(__file__).parent / "eval-results"
KEYFRAME = EVAL_RESULTS / "keyframe-nano_banana_2-start.png"


def build_wan22_workflow(
    uploaded_image: str,
    positive_prompt: str,
    use_lora: bool = True,
    lora_name: str = "pixel-000020.safetensors",
    lora_strength: float = 0.85,
    frame_count: int = 49,
    seed: int = 42,
) -> dict:
    """Build a Wan 2.2 5B I2V workflow."""

    prompt_data = {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "wan2.2_ti2v_5B_fp16.safetensors",
                "weight_dtype": "default",
            },
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
                "type": "wan",
            },
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "wan2.2_vae.safetensors",
            },
        },
        "4": {
            "class_type": "LoadImage",
            "inputs": {
                "image": uploaded_image,
            },
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": positive_prompt,
                "clip": ["2", 0],
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "blurry, low quality, distorted, deformed, anti-aliased, gradient background, watermark, text",
                "clip": ["2", 0],
            },
        },
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
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
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
        "9": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["8", 0],
                "vae": ["3", 0],
            },
        },
        "10": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["9", 0],
                "frame_rate": 24,
                "loop_count": 0,
                "filename_prefix": "wan22_phase4_test",
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True,
            },
        },
    }

    if use_lora:
        prompt_data["20"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": lora_name,
                "strength_model": lora_strength,
                "strength_clip": lora_strength,
                "model": ["1", 0],
                "clip": ["2", 0],
            },
        }
        prompt_data["5"]["inputs"]["clip"] = ["20", 1]
        prompt_data["6"]["inputs"]["clip"] = ["20", 1]
        prompt_data["8"]["inputs"]["model"] = ["20", 0]

    return prompt_data


async def upload_image(client, image_path: Path) -> str:
    """Upload an image to ComfyUI."""
    filename = f"phase4_input_{uuid.uuid4().hex[:8]}.png"
    image_data = image_path.read_bytes()
    resp = await client.post(
        f"{BASE_URL}/upload/image",
        files={"image": (filename, image_data, "image/png")},
    )
    resp.raise_for_status()
    return resp.json().get("name", filename)


async def submit_and_wait(client, workflow: dict, test_name: str, timeout: int = 600) -> dict | None:
    """Submit a workflow and wait for completion."""
    client_id = uuid.uuid4().hex
    print(f"  [{test_name}] Queuing workflow...")

    queue_resp = await client.post(
        f"{BASE_URL}/prompt",
        json={"prompt": workflow, "client_id": client_id},
    )
    if queue_resp.status_code != 200:
        print(f"  [{test_name}] FAILED to queue: {queue_resp.status_code} {queue_resp.text[:200]}")
        return None

    prompt_id = queue_resp.json().get("prompt_id")
    print(f"  [{test_name}] Queued: {prompt_id}. Waiting for completion...")

    start = time.monotonic()
    for i in range(timeout // 2):
        history_resp = await client.get(f"{BASE_URL}/history/{prompt_id}")
        if history_resp.status_code == 200:
            history = history_resp.json()
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                if outputs:
                    elapsed = time.monotonic() - start
                    print(f"  [{test_name}] Completed in {elapsed:.0f}s")
                    return outputs
        await asyncio.sleep(2)
        if i % 15 == 14:
            elapsed = time.monotonic() - start
            print(f"  [{test_name}] Still running ({elapsed:.0f}s)...")

    print(f"  [{test_name}] TIMED OUT after {timeout}s")
    return None


async def run_tests():
    """Run all Phase 4 video model tests."""
    import httpx

    print("=" * 60)
    print("Phase 4 Video Model Tests")
    print(f"Alienware: {COMFYUI_HOST}:{COMFYUI_PORT}")
    print("=" * 60)

    if not KEYFRAME.exists():
        print(f"ERROR: Keyframe not found: {KEYFRAME}")
        return

    async with httpx.AsyncClient(timeout=600.0) as client:
        # Upload the keyframe once
        print(f"\nUploading keyframe: {KEYFRAME.name}")
        uploaded_name = await upload_image(client, KEYFRAME)
        print(f"  Uploaded as: {uploaded_name}")

        results = {}

        # ═══ TASK 5: Wan 2.2 with LoRA vs without ═══
        print("\n" + "=" * 60)
        print("TASK 5: Wan 2.2 with Pixel Animate LoRA")
        print("=" * 60)

        base_prompt = (
            "pixel art sprite animation, smooth walk cycle motion, "
            "chroma key green background preserved, bold dark outlines, "
            "SF2 fighting game style, no anti-aliasing"
        )

        # Test 5a: WITHOUT LoRA (baseline)
        print("\n[5a] Wan 2.2 5B — NO LoRA (baseline)")
        workflow_no_lora = build_wan22_workflow(
            uploaded_name, base_prompt, use_lora=False, seed=42
        )
        results["5a_no_lora"] = await submit_and_wait(client, workflow_no_lora, "5a-no-lora")

        # Test 5b: WITH LoRA at 0.85
        print("\n[5b] Wan 2.2 5B — WITH pixel-000020 LoRA (strength=0.85)")
        workflow_lora = build_wan22_workflow(
            uploaded_name, base_prompt, use_lora=True,
            lora_name="pixel-000020.safetensors", lora_strength=0.85, seed=42
        )
        results["5b_with_lora"] = await submit_and_wait(client, workflow_lora, "5b-lora-0.85")

        # ═══ TASK 6: Stronger Motion Prompts ═══
        print("\n" + "=" * 60)
        print("TASK 6: Stronger Motion Prompts")
        print("=" * 60)

        motion_prompts = {
            "6a": (
                "pixel art character walking forward step by step, legs moving in walk cycle, "
                "side view scrolling, green screen, 2D arcade fighter"
            ),
            "6b": (
                "walking animation cycle, left foot forward then right foot forward, "
                "repeating stride, pixel art sprite, green background"
            ),
            "6c": (
                "character locomotion from left to right, full body walk cycle animation, "
                "pixel art style, chroma key green"
            ),
        }

        for test_id, prompt in motion_prompts.items():
            print(f"\n[{test_id}] Prompt: {prompt[:60]}...")
            workflow = build_wan22_workflow(
                uploaded_name, prompt, use_lora=False, seed=42
            )
            results[test_id] = await submit_and_wait(client, workflow, test_id)

        # ═══ Summary ═══
        print("\n" + "=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)

        for test_id, output in results.items():
            status = "PASS (output received)" if output else "FAIL (no output)"
            print(f"  {test_id}: {status}")

        # Save results
        summary_path = EVAL_RESULTS / "phase4-video-test-results.json"
        summary = {
            "date": "2026-04-02",
            "tests": {
                k: {"status": "completed" if v else "failed", "has_output": v is not None}
                for k, v in results.items()
            },
        }
        summary_path.write_text(json.dumps(summary, indent=2))
        print(f"\nResults saved to: {summary_path}")


if __name__ == "__main__":
    asyncio.run(run_tests())
