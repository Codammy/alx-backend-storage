#!/usr/bin/env python3
"""
Redis cache class in python
"""
import redis
import uuid


class Cache:
    """Redis cache memory management class"""

    def __init__(self):
        """first runner function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
        """method for retrieval and storage of data"""
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key
