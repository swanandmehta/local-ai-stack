from mcp.server.fastmcp import FastMCP
from comfy_client import generate_image as comfy_generate

mcp = FastMCP(
    "comfy-mcp",
    host="0.0.0.0",
    port=8000
)

@mcp.tool(
    name="generate_image",
    description="Generate an image using ComfyUI from a text prompt."
)
def generate_image(prompt: str) -> dict:
    return comfy_generate(prompt)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )