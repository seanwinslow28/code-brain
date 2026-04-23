"""
16BitFit LoRA Test Script
=========================
Sends workflow prompts to ComfyUI's REST API to generate a grid of test images
comparing LoRA checkpoints (epoch 5 vs 10), strengths (0.0-1.0), and prompts.

How it works:
- Builds a ComfyUI workflow as a JSON dict (each key is a node ID)
- POSTs it to http://127.0.0.1:8188/prompt
- Listens on a WebSocket to know when each image finishes
- Saves images to the output directory with descriptive filenames

Requirements: pip install requests websocket-client
"""

import json
import os
import struct
import sys
import time
import urllib.request
import uuid

try:
    import websocket
except ImportError:
    print("ERROR: websocket-client not installed. Run: pip install websocket-client")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
COMFYUI_URL = "http://127.0.0.1:8188"
COMFYUI_WS = "ws://127.0.0.1:8188/ws"

BASE_MODEL = "Illustrious-XL-v2.0.safetensors"

LORA_FILES = {
    "epoch05": "16bitfit_sprite_style-000005.safetensors",
    "epoch10": "16bitfit_sprite_style.safetensors",
}

STRENGTHS = [0.0, 0.5, 0.7, 0.8, 0.9, 1.0]

PROMPTS = [
    "16bitfit_style, pixel art fighter, idle stance, bold outlines, green screen background, full body, facing right, 128x128 sprite",
    "16bitfit_style, pixel art fighter, punch attack pose, bold outlines, green screen background, full body, facing right, dynamic action pose",
    "16bitfit_style, pixel art fighter, walking frame mid-stride, bold outlines, green screen background, full body, facing right, legs apart",
]

NEGATIVE_PROMPT = (
    "blurry, anti-aliased, gradient, low quality, 3d render, realistic, "
    "photograph, watermark, text, deformed"
)

SEED = 42
STEPS = 28
CFG = 7
SAMPLER = "euler"
SCHEDULER = "normal"
WIDTH = 1024
HEIGHT = 1024

OUTPUT_DIR = r"C:\Users\seanw\Documents\Code-Brain\lora-output\16bitfit-style\comfyui-test"


# ---------------------------------------------------------------------------
# Workflow builders
# ---------------------------------------------------------------------------
def build_workflow_with_lora(prompt_text, lora_file, strength):
    """
    Builds a ComfyUI API workflow with LoRA applied.

    Node graph:
      [1] CheckpointLoaderSimple -> [2] LoraLoader -> [3] CLIPTextEncode (positive)
                                                   -> [4] CLIPTextEncode (negative)
      [5] EmptyLatentImage -> [6] KSampler -> [7] VAEDecode -> [8] SaveImage

    The LoRA loader sits between the checkpoint and the text encoders,
    modifying both the model weights and the CLIP text encoder weights
    at the specified strength.
    """
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": BASE_MODEL},
        },
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": lora_file,
                "strength_model": strength,
                "strength_clip": strength,
                "model": ["1", 0],  # model output from checkpoint loader
                "clip": ["1", 1],   # clip output from checkpoint loader
            },
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["2", 1],  # clip output from LoRA loader
            },
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": NEGATIVE_PROMPT,
                "clip": ["2", 1],
            },
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1},
        },
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": SEED,
                "steps": STEPS,
                "cfg": CFG,
                "sampler_name": SAMPLER,
                "scheduler": SCHEDULER,
                "denoise": 1.0,
                "model": ["2", 0],      # model output from LoRA loader
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["5", 0],
            },
        },
        "7": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["6", 0],
                "vae": ["1", 2],  # VAE output from checkpoint loader
            },
        },
        "8": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "16bitfit_test",
                "images": ["7", 0],
            },
        },
    }


def build_workflow_baseline(prompt_text):
    """
    Builds a ComfyUI API workflow WITHOUT LoRA (baseline).

    Same as above but the checkpoint loader connects directly to
    the text encoders and KSampler — no LoRA node in between.
    This gives us the "raw" base model output for comparison.
    """
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": BASE_MODEL},
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["1", 1],  # directly from checkpoint
            },
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": NEGATIVE_PROMPT,
                "clip": ["1", 1],
            },
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1},
        },
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": SEED,
                "steps": STEPS,
                "cfg": CFG,
                "sampler_name": SAMPLER,
                "scheduler": SCHEDULER,
                "denoise": 1.0,
                "model": ["1", 0],       # directly from checkpoint
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["5", 0],
            },
        },
        "7": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["6", 0],
                "vae": ["1", 2],
            },
        },
        "8": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "16bitfit_test",
                "images": ["7", 0],
            },
        },
    }


# ---------------------------------------------------------------------------
# ComfyUI API helpers
# ---------------------------------------------------------------------------
def queue_prompt(workflow, client_id):
    """
    Sends a workflow to ComfyUI's /prompt endpoint.
    Returns the prompt_id so we can track when it finishes.
    """
    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["prompt_id"]


def wait_for_completion(ws, prompt_id):
    """
    Listens on the ComfyUI WebSocket until the given prompt_id is done.

    ComfyUI sends JSON messages with status updates. We wait for
    'execution_complete' or 'execution_error' for our prompt_id.
    The WebSocket also sends binary image preview data (first 8 bytes
    are a header) — we skip those.
    """
    while True:
        msg = ws.recv()
        # Binary messages are image previews — skip them
        if isinstance(msg, bytes):
            continue
        data = json.loads(msg)
        msg_type = data.get("type", "")
        msg_data = data.get("data", {})

        if msg_type == "executing" and msg_data.get("prompt_id") == prompt_id:
            node = msg_data.get("node")
            if node is None:
                # node=None means execution finished
                return True

        if msg_type == "execution_error" and msg_data.get("prompt_id") == prompt_id:
            print(f"  ERROR: {msg_data.get('exception_message', 'unknown error')}")
            return False


def get_history(prompt_id):
    """Fetches the output history for a completed prompt."""
    resp = urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}")
    return json.loads(resp.read())


def download_image(filename, subfolder, output_path):
    """Downloads a generated image from ComfyUI's /view endpoint."""
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
    resp = urllib.request.urlopen(f"{COMFYUI_URL}/view?{params}")
    with open(output_path, "wb") as f:
        f.write(resp.read())


# ---------------------------------------------------------------------------
# Build test matrix
# ---------------------------------------------------------------------------
def build_test_jobs():
    """
    Creates the list of all test jobs to run.

    Returns a list of dicts with:
      - prompt_idx: which test prompt (0, 1, 2)
      - checkpoint: "baseline", "epoch05", or "epoch10"
      - strength: float
      - output_file: where to save the result
      - workflow: the ComfyUI workflow JSON
    """
    jobs = []
    prompt_labels = ["idle", "punch", "walk"]

    for p_idx, prompt_text in enumerate(PROMPTS):
        # Baseline: no LoRA, strength 0.0 — only need one per prompt
        out_name = f"p{p_idx}_{prompt_labels[p_idx]}_baseline_s0.0_seed{SEED}.png"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        jobs.append({
            "prompt_idx": p_idx,
            "checkpoint": "baseline",
            "strength": 0.0,
            "output_file": out_path,
            "output_name": out_name,
            "workflow": build_workflow_baseline(prompt_text),
        })

        # LoRA runs: each checkpoint at each non-zero strength
        for ckpt_name, lora_file in LORA_FILES.items():
            for strength in STRENGTHS:
                if strength == 0.0:
                    continue  # already covered by baseline
                out_name = f"p{p_idx}_{prompt_labels[p_idx]}_{ckpt_name}_s{strength}_seed{SEED}.png"
                out_path = os.path.join(OUTPUT_DIR, out_name)
                jobs.append({
                    "prompt_idx": p_idx,
                    "checkpoint": ckpt_name,
                    "strength": strength,
                    "output_file": out_path,
                    "output_name": out_name,
                    "workflow": build_workflow_with_lora(prompt_text, lora_file, strength),
                })

    return jobs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jobs = build_test_jobs()
    total = len(jobs)

    # Check which jobs already have output (makes the script resumable)
    remaining = [j for j in jobs if not os.path.exists(j["output_file"])]
    skipped = total - len(remaining)

    print(f"16BitFit LoRA Test")
    print(f"==================")
    print(f"Base model:  {BASE_MODEL}")
    print(f"Total jobs:  {total}")
    print(f"Already done: {skipped}")
    print(f"To generate: {len(remaining)}")
    print()

    if not remaining:
        print("All images already generated! Delete output files to re-run.")
        print_summary(jobs)
        return

    # Connect WebSocket for tracking progress
    client_id = str(uuid.uuid4())
    print(f"Connecting to ComfyUI at {COMFYUI_URL}...")
    ws = websocket.WebSocket()
    ws.connect(f"{COMFYUI_WS}?clientId={client_id}")
    print("Connected!\n")

    completed = 0
    failed = 0
    start_time = time.time()

    for job in remaining:
        label = f"[{skipped + completed + failed + 1}/{total}]"
        print(f"{label} {job['output_name']}  (ckpt={job['checkpoint']}, strength={job['strength']})")

        try:
            prompt_id = queue_prompt(job["workflow"], client_id)
            success = wait_for_completion(ws, prompt_id)

            if success:
                # Retrieve the saved image from ComfyUI's output
                history = get_history(prompt_id)
                outputs = history[prompt_id]["outputs"]
                # SaveImage is node "8"
                images = outputs["8"]["images"]
                if images:
                    img = images[0]
                    download_image(img["filename"], img["subfolder"], job["output_file"])
                    size_mb = os.path.getsize(job["output_file"]) / (1024 * 1024)
                    print(f"  -> Saved ({size_mb:.1f} MB)")
                    completed += 1
                else:
                    print("  -> WARNING: No images in output")
                    failed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  -> ERROR: {e}")
            failed += 1

    ws.close()
    elapsed = time.time() - start_time

    print(f"\n{'='*50}")
    print(f"Done in {elapsed/60:.1f} minutes")
    print(f"  Completed: {completed}")
    print(f"  Failed:    {failed}")
    print(f"  Skipped:   {skipped}")
    print()

    print_summary(jobs)


def print_summary(jobs):
    """Prints a grouped summary of all output files."""
    prompt_labels = ["Idle Stance", "Punch Attack", "Walking Frame"]

    print("\n" + "=" * 60)
    print("OUTPUT SUMMARY")
    print("=" * 60)

    for p_idx, label in enumerate(prompt_labels):
        print(f"\n--- Prompt {p_idx}: {label} ---")
        p_jobs = [j for j in jobs if j["prompt_idx"] == p_idx]
        for j in p_jobs:
            exists = os.path.exists(j["output_file"])
            status = "OK" if exists else "MISSING"
            size = ""
            if exists:
                size_mb = os.path.getsize(j["output_file"]) / (1024 * 1024)
                size = f" ({size_mb:.1f} MB)"
            print(f"  [{status}] {j['output_name']}{size}")

    print(f"\n--- Key Comparisons ---")
    print("For each prompt, compare these images:")
    print("  1. Baseline vs Epoch10 @ 0.8  (does LoRA help?)")
    print("  2. Epoch05 vs Epoch10 @ 0.8   (overfitting check)")
    print("  3. Epoch10: 0.5 -> 0.7 -> 0.8 -> 0.9 -> 1.0  (strength sweep)")
    print()


if __name__ == "__main__":
    main()
