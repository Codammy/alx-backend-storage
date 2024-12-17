#!/usr/bin/env python3
"""
Redis cache class in python
"""
import redis
import uuid
import typing
from functools import wraps


def count_calls(method: typing.Callable) -> typing.Callable:
    """decorator function"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """wrapper function"""
        args[0]._redis.incr(method.__qualname__)
        return method(*args, *kwargs)
    return wrapper


class Cache:
    """Redis cache memory management class"""

    def __init__(self):
        """first runner function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """method for retrieval and storage of data"""
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(self, key: str, fn: typing.Callable = None):
        """returns data corresponding to `key` in redis hashmap"""
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val

    def get_int(self, key: str) -> int:
        """returns converted byte value to int from redis"""
        return int(self.get(key))

    def get_str(self, key: str) -> str:
        """returns converted byte value to str from redis"""
        return str(self.get(key))
