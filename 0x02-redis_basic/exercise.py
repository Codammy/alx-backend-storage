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
        self = args[0]
        self._redis.incr(method.__qualname__)
        return method(*args, **kwargs)
    return wrapper


def call_history(method: typing.Callable) -> typing.Callable:
    """stores function input and output history"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """`method wrapper`"""
        self = args[0]
        self._redis.rpush(method.__qualname__ + ":inputs", str(args[1:]))
        output = method(*args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output
    return wrapper


def replay(func: typing.Callable):
    """displays the history of calls of a particular function"""
    r = redis.Redis()
    no_called = int(r.get(func.__qualname__))
    print(f"{func.__qualname__} was called {no_called} times:")
    inputs = r.lrange(f"{func.__qualname__}:inputs", 0, -1)
    outputs = r.lrange(f"{func.__qualname__}:outputs", 0, -1)
    history = zip(inputs, outputs)
    for h in history:
        print(f"Cache.store(*{h[0].decode('utf-8')}) -> {h[1]}")


class Cache:
    """Redis cache memory management class"""

    def __init__(self):
        """first runner function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
