#!/usr/bin/env python3
"""
This module defines a Cache class that stores data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    A class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        Initializes a Cache object by creating a Redis client and
        flushing the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis
        using the key.
        Returns the key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
