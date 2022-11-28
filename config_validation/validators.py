from datetime import datetime
from ipaddress import IPv4Address
from pathlib import Path
from textwrap import dedent
from typing import Any, List, Mapping, Union

from more_itertools import always_iterable
from pydantic import BaseModel, validator, ValidationError


def set_to_list(value) -> List:
    """Ensure value is a list."""
    return list(always_iterable(value))


class ValidateOwner(BaseModel):
    name: str
    dob: datetime

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()


class ValidateDatabase(BaseModel):
    server: IPv4Address
    ports: List[int]
    connection_max: float
    enabled: bool = False

    # Define validators to apply to values.
    _set_to_list = (
        validator(
            'ports',
            pre=True,
            always=True,
            allow_reuse=True
        )
        (set_to_list)
    )

    @validator('ports', each_item=True)
    def check_ports(cls, v):
        assert 8001 <= v <= 8080, f'{v} not a valid port number.'
        return v


class ValidateServerType(BaseModel):
    ip: IPv4Address
    dc: str


class ValidateServers(BaseModel):
    alpha: ValidateServerType
    beta: ValidateServerType


class ValidateClients(BaseModel):
    data: List[List[Union[str, int]]]
    hosts: List[str]

    # Define validators to apply to values.
    _set_to_list = (
        validator(
            'hosts',
            pre=True,
            always=True,
            allow_reuse=True
        )
        (set_to_list)
    )

    @validator('hosts', each_item=True)
    def check_valid_host(cls, v):
        valid_hosts = [
            'alpha',
            'omega',
        ]

        assert v in valid_hosts, f'{v} not one of valid host: {valid_hosts}'
        return v


class ValidateLogs(BaseModel):
    save: bool = False
    path: Path

    @validator('path')
    def check_file_does_not_exist(cls, v: Path) -> Path:
        assert not v.is_file(), f'{v} already exists'
        return v


class ValidateConfig(BaseModel):
    title: str
    owner: ValidateOwner
    database: ValidateDatabase
    servers: ValidateServers
    clients: ValidateClients
    logs: ValidateLogs


def try_validation(
    config: Mapping[str, Any],
    Validator: BaseModel,
    outcome: str = None,
) -> None:
    """Run config through validator, catching any validation error.

    This function serves only to demo validation and the errors that would
    stop execution in normal circumstances.

    Parameters
    ----------
    config
        Configuration mapping to pass through the validator
    Validator
        Validation model to run config through.
    outcome
        Description of what the passed config should do.
    
    Returns
    -------
    None

    """
    print(dedent(f"""
        =====================
        Validating config:
        {config}
    """))

    if outcome:
        print(f'This will be a:{outcome}')

    try:
        validated_config =  Validator(**config).dict()
        print(dedent(f"""
        Validation successful
        
        Validated config:
        {validated_config}
        """))

    except ValidationError as e:
        print(dedent("""
        Validation failed
        
        Error:
        """))
        # Print error seperately only for nice formating of prints (dedent not
        # behaving as expected when error in above statement).
        print(e)


if __name__ == '__main__':
    # from config_validation.io import read_yaml

    # config = read_yaml('configs/config.yaml')
    # try_validation(config, ValidateConfig)

    outcome = dedent("""
    Valid configuration.
    """)
    owner = {
        'name': 'Matt Price',
        'dob': datetime(1901, 1, 1),
    }
    try_validation(owner, ValidateOwner, outcome)

    outcome = dedent("""
    Valid configuration: location field not in model so not present after
    validation.
    """)
    owner = {
        'name': 'Matt Price',
        'dob': datetime(1901, 1, 1),
        'location': 'Home',
    }
    try_validation(owner, ValidateOwner, outcome)

    outcome = dedent("""
    Invalid configuration: both fields fail checks.
    """)
    owner = {
        'name': 'Matt',
        'dob': '1901-01-01',
    }
    try_validation(owner, ValidateOwner, outcome)

    outcome = dedent("""
    Valid configuration: server field converted to IPv4 address object, ports
    field converted to a list.
    """)
    database = {
        'server': '192.168.1.1',
        'ports': 8080,
        'connection_max': 5000.1,
        'enabled': True,
    }
    try_validation(database, ValidateDatabase, outcome)

    outcome = dedent("""
    Valid configuration: server field converted to IPv4 address object
    enabled field not specified so set to default, connection_max converted
    to a float.
    """)
    database = {
        'server': '192.168.1.1',
        'ports': [ 8001, 8001, 8002],
        'connection_max': 5000,
    }
    try_validation(database, ValidateDatabase, outcome)

    outcome = dedent("""
    Invalid configuration: one entry in ports is not in range.
    """)
    database = {
        'server': '192.168.1.1',
        'ports': [ 8001, 8001, 8002, 8081],
        'connection_max': 5000,
        'enabled': True,
    }
    try_validation(database, ValidateDatabase, outcome)

    outcome = dedent("""
    Valid configuration: path field converted to Path object
    """)
    logs = {
        'save': True,
        'path': './my/logs.json'
    }
    try_validation(logs, ValidateLogs, outcome)

    outcome = dedent("""
    Invalid configuration: path field converted to Path object, file at path
    already exists.
    """)
    logs = {
        'save': True,
        'path': './validators.py'
    }
    try_validation(logs, ValidateLogs, outcome)
