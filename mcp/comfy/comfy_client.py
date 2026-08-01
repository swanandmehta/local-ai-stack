import os
import json
import requests
import time
import uuid
import logging

from config import (
    COMFY_URL,
    WORKFLOW_DIR,
    WORKFLOW_NAME,
    POSITIVE_PROMPT_NODE,
    OUTPUT_NODE,
    OUTPUT_PREFIX,
    SAMPLER_NODES
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def check_comfy():
    logger.info("Checking ComfyUI connection")
    response = requests.get(
        f"{COMFY_URL}/system_stats"
    )
    response.raise_for_status()


def load_workflow():
    path = os.path.join(
        WORKFLOW_DIR,
        f"{WORKFLOW_NAME}.json"
    )
    logger.info(
        f"Loading workflow {path}"
    )
    with open(path, "r") as file:
        return json.load(file)


def queue_prompt(workflow):
    payload = {
        "prompt": workflow,
        "client_id": str(uuid.uuid4())
    }
    response = requests.post(
        f"{COMFY_URL}/prompt",
        json=payload
    )

    response.raise_for_status()

    return response.json()["prompt_id"]


def wait_for_completion(
    prompt_id,
    timeout=300
):

    start_time = time.time()

    while True:

        if time.time() - start_time > timeout:
            raise TimeoutError(
                "ComfyUI generation timed out"
            )

        response = requests.get(
            f"{COMFY_URL}/history/{prompt_id}"
        )

        response.raise_for_status()

        history = response.json()

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(1)


def get_output_image(history):

    try:
        images = (
            history["outputs"]
            [OUTPUT_NODE]
            ["images"]
        )
    except KeyError:
        raise Exception(
            f"No output found from node {OUTPUT_NODE}"
        )

    if not images:
        raise Exception(
            "No image generated"
        )
        
    image = images[0]
    result = {
        "filename": image["filename"],
        "subfolder": image["subfolder"],
        "type": image["type"]
    }
    logger.info(
        f"Output filename : {image['filename']}"
    )
    return result


def generate_image(prompt):

    check_comfy()

    workflow = load_workflow()
    
    # Update positive prompt
    workflow[
        POSITIVE_PROMPT_NODE
    ]["inputs"]["text"] = prompt


    # Prevent filename collisions
    workflow[
        OUTPUT_NODE
    ]["inputs"]["filename_prefix"] = (
        f"{OUTPUT_PREFIX}_{uuid.uuid4().hex[:8]}"
    )

    # Randomize sampler seeds
    for node_id in SAMPLER_NODES:

        workflow[
            node_id
        ]["inputs"]["seed"] = (
            uuid.uuid4().int % 999999999999999
        )

    prompt_id = queue_prompt(
        workflow
    )

    logger.info(
        f"Queued prompt with id: {prompt_id}"
    )

    result = wait_for_completion(
        prompt_id
    )

    logger.info(
        f"Generation complete for prompt id: {prompt_id}"
    )

    return get_output_image(
        result
    )
