import yaml
from pathlib import Path


def load_config() -> dict:
    path = "/notebooks/ML/Flight Delay Prediction Project/ELT/config/config.yaml"
    with open(Path(path), "r") as f:
        return yaml.safe_load(f)