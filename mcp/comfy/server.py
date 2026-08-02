from mcp.server.fastmcp import FastMCP
from comfy_client import generate_image as comfy_generate
from model.plan import ImagePlan

mcp = FastMCP("comfy-mcp", host="0.0.0.0", port=8000)


@mcp.tool(
    name="generate_image",
    description="Generate an image using ComfyUI. Requires a completed image plan from create_image_plan. Do not call directly with raw user prompts.",
)
def generate_image(image_plan: ImagePlan) -> dict:
    return comfy_generate(image_plan)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
