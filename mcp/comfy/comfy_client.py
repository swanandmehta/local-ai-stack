import json
import os
import time
import uuid
import logging

import requests
import yaml

from model.plan import ImagePlan
from pathlib import Path

from config.config import (
    COMFY_URL,
    WORKFLOW_DIR,
    OUTPUT_PREFIX,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

CONFIG_DIR = Path(__file__).parent / "config"


def load_yaml(filename):
    path = CONFIG_DIR / filename

    with open(path, "r") as file:
        return yaml.safe_load(file)


def load_workflow(workflow_name: str):

    config = load_yaml("workflows.yaml")

    if workflow_name not in config["workflows"]:
        raise ValueError(f"Unknown workflow: {workflow_name}")

    workflow_config = config["workflows"][workflow_name]

    workflow_path = os.path.join(WORKFLOW_DIR, workflow_config["file"])

    logger.info("Loading workflow: %s", workflow_path)

    with open(workflow_path, "r") as file:
        workflow = json.load(file)

    return workflow, workflow_config


def check_comfy():

    logger.info("Checking ComfyUI connection")

    response = requests.get(f"{COMFY_URL}/system_stats")

    response.raise_for_status()


def queue_prompt(workflow):

    payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}

    response = requests.post(f"{COMFY_URL}/prompt", json=payload)

    response.raise_for_status()

    return response.json()["prompt_id"]


def wait_for_completion(prompt_id, timeout=300):

    start_time = time.time()

    while True:

        if time.time() - start_time > timeout:
            raise TimeoutError("ComfyUI generation timed out")

        response = requests.get(f"{COMFY_URL}/history/{prompt_id}")

        response.raise_for_status()

        history = response.json()

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(5)


def get_output_image(history, output_node):

    try:
        images = history["outputs"][str(output_node)]["images"]

    except KeyError:
        raise Exception(f"No output found from node {output_node}")

    if not images:
        raise Exception("No image generated")

    image = images[0]

    logger.info("Output filename: %s", image["filename"])

    return {
        "filename": image["filename"],
        "subfolder": image["subfolder"],
        "type": image["type"],
    }


def generate_image(image_plan: ImagePlan):
    logger.info(
        "Generating image using workflow=%s model=%s",
        image_plan.workflow,
        image_plan.model,
    )

    check_comfy()

    workflow, workflow_config = load_workflow(image_plan.workflow)

    workflow[str(workflow_config["positive_prompt_node"])]["inputs"][
        "text"
    ] = image_plan.positive_prompt

    workflow[str(workflow_config["negative_prompt_node"])]["inputs"][
        "text"
    ] = image_plan.negative_prompt

    output_node = workflow_config["output_node"]

    workflow[str(output_node)]["inputs"][
        "filename_prefix"
    ] = f"{OUTPUT_PREFIX}_{uuid.uuid4().hex[:8]}"

    for node_id in workflow_config["sampler_nodes"]:
        workflow[str(node_id)]["inputs"]["seed"] = uuid.uuid4().int % 999999999999999

    logger.info("Positive prompt: %s", image_plan.positive_prompt)

    logger.info("Negative prompt: %s", image_plan.negative_prompt)

    logger.info("Styles: %s", image_plan.style)

    prompt_id = queue_prompt(workflow)

    logger.info("Queued prompt: %s", prompt_id)

    history = wait_for_completion(prompt_id)

    logger.info("Generation complete: %s", prompt_id)

    return get_output_image(history, output_node)
