import os
from pathlib import Path
import yaml
from pydantic import BaseModel


class Config(BaseModel):
    MODEL_NAME: str
    SQLITE_DB: str

    WEAVIATE_HOST: str
    WEAVIATE_PORT: int
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int


def load_config() -> Config:
    config_path = Path(os.path.expanduser("~/.config/utils/custom-chat-gpt/config.yml"))
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)
        config_data = {k.upper(): v for k, v in config_data.items()}
    return Config(**config_data)
