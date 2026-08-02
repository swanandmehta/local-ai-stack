import os
import json
import yaml
import logging
import requests
import time
from model.request import ImageRequest
from model.plan import ImagePlan

from fastapi import FastAPI

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

PLANNER_MODEL = os.getenv("PLANNER_MODEL", "qwen2.5:7b")

CONFIG_DIR = os.getenv("CONFIG_DIR", "/app/config")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger("image-planner")


def load_yaml(filename):
    path = os.path.join(CONFIG_DIR, filename)

    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_prompt():
    path = os.path.join(CONFIG_DIR, "system_prompt.txt")

    with open(path, "r") as f:
        return f.read()


def create_system_prompt(user_prompt):
    return SYSTEM_TEMPLATE.format(
        MODELS=yaml.dump(MODELS), STYLES=yaml.dump(STYLES), USER_PROMPT=user_prompt
    )


def ask_ollama(user_prompt: str):
    payload = {
        "model": PLANNER_MODEL,
        "prompt": create_system_prompt(user_prompt),
        "stream": False,
        "format": "json",
    }

    logger.info("Calling Ollama model=%s", PLANNER_MODEL)

    start = time.time()

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        logger.exception("Ollama request failed")
        raise e

    data = response.json()

    logger.info("Ollama completed in %.2fs", time.time() - start)

    return json.loads(data["response"])


@app.post("/plan-image")
def plan_image(request: ImageRequest):
    logger.info("Image request: %s", request.prompt)

    result = ask_ollama(request.prompt)

    plan = ImagePlan(**result)

    logger.info("Selected model=%s workflow=%s", plan.model, plan.workflow)

    return plan


@app.on_event("startup")
def startup_event():
    logger.info("Planner model: %s", PLANNER_MODEL)


MODELS = load_yaml("models.yaml")
STYLES = load_yaml("styles.yaml")
SYSTEM_TEMPLATE = load_prompt()
