from pydantic import BaseModel


class ImagePlan(BaseModel):
    model: str
    workflow: str
    positive_prompt: str
    negative_prompt: str
    style: list[str]
