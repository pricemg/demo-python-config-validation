# demo-python-config-validation
Demo of loading and validating a config file in python.

Loading either toml or yaml files will yield the same result:
```python
 >>> python3.11 io.py

yaml config:

{'clients': {'data': [['gamma', 'delta'], [1, 2]], 'hosts': ['alpha', 'omega']},
 'database': {'connection_max': 5000,
              'enabled': True,
              'ports': [8001, 8001, 8002],
              'server': '192.168.1.1'},
 'logs': {'path': './my/logs.json', 'save': True},
 'owner': {'dob': datetime.datetime(1979, 5, 27, 7, 32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600))),
           'name': 'Tom Preston-Werner'},
 'servers': {'alpha': {'dc': 'eqdc10', 'ip': '10.0.0.1'},
             'beta': {'dc': 'eqdc10', 'ip': '10.0.0.2'}},
 'title': 'Config Example'}

toml config:

{'clients': {'data': [['gamma', 'delta'], [1, 2]], 'hosts': ['alpha', 'omega']},
 'database': {'connection_max': 5000,
              'enabled': True,
              'ports': [8001, 8001, 8002],
              'server': '192.168.1.1'},
 'logs': {'path': './my/logs.json', 'save': True},
 'owner': {'dob': datetime.datetime(1979, 5, 27, 7, 32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600))),
           'name': 'Tom Preston-Werner'},
 'servers': {'alpha': {'dc': 'eqdc10', 'ip': '10.0.0.1'},
             'beta': {'dc': 'eqdc10', 'ip': '10.0.0.2'}},
 'title': 'Config Example'}

Does read toml file match yaml file? True
```

Validation of dictionaries (i.e. loaded config files) can be achieved through
the use of `pydantic` models.

```python
>>> python3.11 validators.py  

=====================
Validating config:
{'name': 'Matt Price', 'dob': datetime.datetime(1901, 1, 1, 0, 0)}

This will be a:
Valid configuration.


Validation successful

Validated config:
{'name': 'Matt Price', 'dob': datetime.datetime(1901, 1, 1, 0, 0)}


=====================
Validating config:
{'name': 'Matt Price', 'dob': datetime.datetime(1901, 1, 1, 0, 0), 'location': 'Home'}

This will be a:
Valid configuration: location field not in model so not present after
validation.


Validation successful

Validated config:
{'name': 'Matt Price', 'dob': datetime.datetime(1901, 1, 1, 0, 0)}


=====================
Validating config:
{'name': 'Matt', 'dob': '1901-01-01'}

This will be a:
Invalid configuration: both fields fail checks.


Validation failed

Error:

2 validation errors for ValidateOwner
name
  must contain a space (type=value_error)
dob
  invalid datetime format (type=value_error.datetime)

=====================
Validating config:
{'server': '192.168.1.1', 'ports': 8080, 'connection_max': 5000.1, 'enabled': True}

This will be a:
Valid configuration: server field converted to IPv4 address object, ports
field converted to a list.


Validation successful

Validated config:
{'server': IPv4Address('192.168.1.1'), 'ports': [8080], 'connection_max': 5000.1, 'enabled': True}


=====================
Validating config:
{'server': '192.168.1.1', 'ports': [8001, 8001, 8002], 'connection_max': 5000}

This will be a:
Valid configuration: server field converted to IPv4 address object
enabled field not specified so set to default, connection_max converted
to a float.


Validation successful

Validated config:
{'server': IPv4Address('192.168.1.1'), 'ports': [8001, 8001, 8002], 'connection_max': 5000.0, 'enabled': False}


=====================
Validating config:
{'server': '192.168.1.1', 'ports': [8001, 8001, 8002, 8081], 'connection_max': 5000, 'enabled': True}

This will be a:
Invalid configuration: one entry in ports is not in range.


Validation failed

Error:

1 validation error for ValidateDatabase
ports -> 3
  8081 not a valid port number. (type=assertion_error)

=====================
Validating config:
{'save': True, 'path': './my/logs.json'}

This will be a:
Valid configuration: path field converted to Path object


Validation successful

Validated config:
{'save': True, 'path': PosixPath('my/logs.json')}


=====================
Validating config:
{'save': True, 'path': './validators.py'}

This will be a:
Invalid configuration: path field converted to Path object, file at path
already exists.


Validation failed

Error:

1 validation error for ValidateLogs
path
  validators.py already exists (type=assertion_error)
```