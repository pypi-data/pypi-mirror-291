import json
import socket
import time
import redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError
from redis.retry import Retry


class RedisClientWrapper:

    def __init__(self, config: dict): ...

    @property
    def conn(self): ...

    def save_dict(self, key: str, dic: dict):
        """存储dict到redis
        @param key: key name
        @param dic: 数据
        @return:"""

    def __del__(self): ...
