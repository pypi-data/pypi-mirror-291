import os
from typing import Literal, List, Dict

from config_binder import ConfigBinder, ConfigType

input_yaml = """
name: MyApplication
logging_level: INFO
redis_config:
  host: ${MYAPP_REDIS_HOST:127.0.0.1}
  post: ${MYAPP_REDIS_PORT:6379}
  password: ${MYAPP_REDIS_PASS}
  encryption_Key: ${MYAPP_REDIS_ENCRYPTION_KEY}
sources_configs:
  orders:
    url: some-url.com/orders
    token: ${MYAPP_ORDERS_SOURCE_TOKEN}
    retry_policy:
      max_attempts: 5
      backoff_seconds: 10
  products:
    url: another-url.com/products
    token: ${MYAPP_ORDERS_PRODUCTS_TOKEN}
    retry_policy:
      max_attempts: 3
      backoff_seconds: 5
"""


class RedisConfig:
    host: str
    port: int
    password: str
    encryption_key: str


class RetryPolicy:
    max_attempts: int
    backoff_seconds: int


class SourceConfig:
    url: str
    token: str
    retry_policy: RetryPolicy


class AppConfig:
    name: str
    logging_level: Literal['DEBUG', 'INFO', 'ERROR']
    redis_config: RedisConfig
    sources_configs: Dict[str, SourceConfig]


os.environ['MYAPP_REDIS_PASS'] = 'redis_pass'
os.environ['MYAPP_REDIS_ENCRYPTION_KEY'] = 'very_strong_key'
os.environ['MYAPP_ORDERS_SOURCE_TOKEN'] = 'orders_token'
os.environ['MYAPP_ORDERS_PRODUCTS_TOKEN'] = 'products_token'

config = ConfigBinder.read(ConfigType.yaml, input_yaml, AppConfig)
print(config)
