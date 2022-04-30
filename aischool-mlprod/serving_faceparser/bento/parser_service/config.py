from pathlib import Path

import torch
from pydantic import BaseSettings


class Config(BaseSettings):
    device: str = (f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu")
    half_precision: bool = True
    root_dir = Path(__file__).parent.parent
    image_size = 512
