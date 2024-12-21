#!/usr/bin/env python3
""" In this tasks, i will implement a
get_page function (prototype: def get_page(url: str) -> str:).
The core of the function is very simple.
It uses the requests module to obtain the HTML content of a
particular URL and returns it.
"""
import requests
import redis
import typing
from functools import wraps


def cache_count(func: typing.Callable) -> typing.Callable:
    """decorator function for caching url counts"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function"""
        r = redis.Redis()
        url = args[0]
        r.incr(f"count:{{url}}")
        r.expire(url, 10)
        return func(url)
    return wrapper


@cache_count
def get_page(url: str) -> str:
    """ It uses the requests module to obtain
    the HTML content of a particular URL and returns it.
    """
    resp = requests.get(url)
    return resp.text


