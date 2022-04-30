from typing import Any

from pydantic import BaseModel


class InferenceData(BaseModel):
    image: Any  # Image crops as numpy array, shape (H, W, 3), RGB
