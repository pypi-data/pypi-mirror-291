# config-binder

[![downloads](https://static.pepy.tech/badge/config-binder/month)](https://pepy.tech/project/config-binder)
[![PyPI version](https://badge.fury.io/py/config-binder.svg)](https://badge.fury.io/py/config-binder)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/config-binder.svg)](https://github.com/pydantic/pydantic)

Configuration parsing with recursive class binding, environment variables resolution and type safety. 


## Installation

```bash
pip install config-binder
```

## Simple example
### input.yaml
```yaml
host: ${MYAPP_HOST:localhost}
port: 5432
username: admin
password: ${MYAPP_PASSWORD}
```
```shell
export MYAPP_PASSWORD=123
```
### With binding:
```python
class MySettings:
    host: str
    port: int
    username: str
    password: str
    source_urls: List[str]


config = ConfigBinder.load('input.yaml')
print(f"type: {type(config).__name__}, config: host:{config.host} port:{config.port} source_urls:{config.source_urls}")

# Output:
# type: MySettings, config: host:localhost port:5432 source_urls:['some-url.com', 'another-url.com']
```
### Without binding
```python
config = ConfigBinder.load('input.yaml')
print(f"type: {type(config).__name__}, config: {config}")

# Output:
# type: dict, config: {'host': 'localhost', 'port': 5432, 'username': 'admin', 'password': '123', 'source_urls': ['some-url.com', 'another-url.com']}
```

