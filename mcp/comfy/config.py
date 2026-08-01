import os


COMFYUI_HOST = os.getenv("COMFYUI_HOST", "localhost")
COMFYUI_PORT = os.getenv("COMFYUI_PORT", "8188")

WORKFLOW_DIR = os.getenv("WORKFLOW_DIR", "/workflows")
WORKFLOW_NAME = os.getenv("WORKFLOW_NAME", "V2.0")

POSITIVE_PROMPT_NODE = os.getenv("POSITIVE_PROMPT_NODE", "2")
OUTPUT_NODE = os.getenv("OUTPUT_NODE", "7")

COMFY_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX", "mcp")

SAMPLER_NODES = os.getenv(
    "SAMPLER_NODES",
    "5,8"
).split(",")