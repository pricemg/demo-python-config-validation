from pathlib import Path
import tomllib

import yaml


def read_yaml(file: str) -> dict[str, any]:
    """Read a yaml file."""
    with open(Path(file), mode="r") as file:
        contents = yaml.safe_load(file)
    
    return contents


def read_toml(file: str) -> dict[str, any]:
    """Read a toml file."""
    with open(Path(file), mode="rb") as file:
        contents = tomllib.load(file)
    
    return contents
