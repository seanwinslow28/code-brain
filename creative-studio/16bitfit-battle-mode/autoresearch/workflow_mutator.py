"""ComfyUI Workflow Mutator — mutates workflow JSON for Optuna trials.

Takes a base ComfyUI workflow JSON and applies parameter overrides from
an Optuna trial. Queues mutated workflow to ComfyUI on Alienware via REST.

Target: Alienware RTX 5080 at 192.168.68.201:8188

Usage:
    from autoresearch.workflow_mutator import WorkflowMutator

    mutator = WorkflowMutator("pixel-quantizer/video-eval/workflows/rife_interpolation.json")
    mutated = mutator.mutate({"ksampler_steps": 30, "ksampler_cfg": 10.0, "rife_multiplier": 4})
"""

from __future__ import annotations

import copy
import json
import tempfile
import time
from pathlib import Path
from typing import Any


ALIENWARE_COMFYUI = "http://192.168.68.201:8188"


class WorkflowMutator:
    """Mutates ComfyUI workflow JSON and queues to Alienware."""

    def __init__(self, workflow_path: str | Path):
        self.workflow_path = Path(workflow_path)
        self.base_workflow = json.loads(self.workflow_path.read_text())

    def mutate(self, params: dict[str, Any]) -> dict:
        """Apply parameter overrides to a copy of the base workflow.

        Args:
            params: Dict from Optuna trial. Recognized keys:
                - ksampler_steps: KSampler steps (int)
                - ksampler_cfg: KSampler CFG scale (float)
                - ksampler_seed: Random seed (int)
                - rife_multiplier: RIFE interpolation multiplier (int)
                - rife_model: RIFE model checkpoint name (str)

        Returns:
            Mutated workflow dict ready for ComfyUI queue.
        """
        workflow = copy.deepcopy(self.base_workflow)
        prompt = workflow.get("prompt", workflow)

        for node_id, node in prompt.items():
            if isinstance(node, dict):
                class_type = node.get("class_type", "")
                inputs = node.get("inputs", {})

                # Mutate KSampler nodes
                if "KSampler" in class_type:
                    if "ksampler_steps" in params and "steps" in inputs:
                        inputs["steps"] = params["ksampler_steps"]
                    if "ksampler_cfg" in params and "cfg" in inputs:
                        inputs["cfg"] = params["ksampler_cfg"]
                    if "ksampler_seed" in params and "seed" in inputs:
                        inputs["seed"] = params["ksampler_seed"]

                # Mutate RIFE VFI nodes
                if "RIFE" in class_type:
                    if "rife_multiplier" in params and "multiplier" in inputs:
                        inputs["multiplier"] = params["rife_multiplier"]
                    if "rife_model" in params and "ckpt_name" in inputs:
                        inputs["ckpt_name"] = params["rife_model"]

        return workflow

    def save_mutated(self, workflow: dict, output_dir: Path | None = None) -> Path:
        """Save mutated workflow to a temp file.

        Returns path to the saved JSON.
        """
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            path = output_dir / f"mutated_{int(time.time())}.json"
        else:
            tmp = tempfile.NamedTemporaryFile(
                suffix=".json", prefix="comfyui_mutated_", delete=False
            )
            path = Path(tmp.name)
            tmp.close()

        path.write_text(json.dumps(workflow, indent=2))
        return path

    async def queue_to_comfyui(
        self,
        workflow: dict,
        server_url: str = ALIENWARE_COMFYUI,
        timeout_secs: float = 120.0,
    ) -> dict[str, Any]:
        """Queue a workflow to ComfyUI and wait for completion.

        Args:
            workflow: Mutated workflow dict.
            server_url: ComfyUI REST API URL.
            timeout_secs: Max wait time.

        Returns:
            ComfyUI response with output images.
        """
        import httpx

        prompt_data = workflow.get("prompt", workflow)

        async with httpx.AsyncClient(timeout=timeout_secs) as client:
            # Queue the workflow
            resp = await client.post(
                f"{server_url}/prompt",
                json={"prompt": prompt_data},
            )
            resp.raise_for_status()
            result = resp.json()
            prompt_id = result.get("prompt_id")

            if not prompt_id:
                raise RuntimeError(f"No prompt_id in ComfyUI response: {result}")

            # Poll for completion
            start = time.monotonic()
            while (time.monotonic() - start) < timeout_secs:
                history_resp = await client.get(f"{server_url}/history/{prompt_id}")
                history = history_resp.json()

                if prompt_id in history:
                    return history[prompt_id]

                await __import__("asyncio").sleep(2)

            raise TimeoutError(f"ComfyUI workflow {prompt_id} timed out after {timeout_secs}s")


# ─── Verification ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # Load RIFE workflow
    base_dir = Path(__file__).parent.parent / "pixel-quantizer" / "video-eval" / "workflows"
    rife_path = base_dir / "rife_interpolation.json"

    if not rife_path.exists():
        print(f"FAIL: RIFE workflow not found at {rife_path}")
        sys.exit(1)

    mutator = WorkflowMutator(rife_path)

    # Mutate KSampler steps and RIFE multiplier
    mutated = mutator.mutate({
        "ksampler_steps": 30,
        "ksampler_cfg": 10.0,
        "rife_multiplier": 8,
        "rife_model": "rife47.pth",
    })

    # Verify mutations applied to RIFE nodes
    prompt = mutated.get("prompt", mutated)
    rife_found = False
    for node_id, node in prompt.items():
        if isinstance(node, dict) and "RIFE" in node.get("class_type", ""):
            inputs = node["inputs"]
            assert inputs["multiplier"] == 8, f"Expected multiplier=8, got {inputs['multiplier']}"
            assert inputs["ckpt_name"] == "rife47.pth", f"Expected rife47.pth, got {inputs['ckpt_name']}"
            rife_found = True
            print(f"  RIFE node {node_id}: multiplier={inputs['multiplier']}, model={inputs['ckpt_name']}")

    assert rife_found, "No RIFE node found in workflow"

    # Save mutated workflow
    tmp_path = mutator.save_mutated(mutated)
    print(f"  Mutated workflow saved to: {tmp_path}")
    print(f"  Target: {ALIENWARE_COMFYUI}")

    print("\nALL CHECKS PASSED")
