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


if __name__ == '__main__':
    from pprint import pprint


    yaml_config = read_yaml('../configs/config.yaml')
    print('\nyaml config:\n')
    pprint(yaml_config)

    toml_config = read_toml('../configs/config.toml')
    print('\ntoml config:\n')
    pprint(toml_config)

    match = toml_config == yaml_config

    print(f'Does read toml file match yaml file? {match}')