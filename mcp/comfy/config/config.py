import os

COMFYUI_HOST = os.getenv("COMFYUI_HOST", "localhost")
COMFYUI_PORT = os.getenv("COMFYUI_PORT", "8188")

WORKFLOW_DIR = os.getenv("WORKFLOW_DIR", "/workflows")

COMFY_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

OUTPUT_PREFIX = os.getenv("OUTPUTS_PREFIX", "mcp")
