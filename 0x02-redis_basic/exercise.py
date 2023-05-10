#!/usr/bin/env python3
"""
This module defines a Cache class that stores data in Redis.
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable


class Cache:
    """
    A class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        Initializes a Cache object by creating a Redis client and flushing the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def _make_key(method: Callable, suffix: str) -> str:
        """
        Returns the Redis key for the given method and suffix.
        """
        return f"{method.__qualname__}:{suffix}"

    def _get_count_key(self, method: Callable) -> str:
        """
        Returns the Redis key for the call count of the given method.
        """
        return self._make_key(method, "count")

    def _increment_count(self, method: Callable) -> int:
        """
        Increments the call count for the given method and returns the new count.
        """
        count_key = self._get_count_key(method)
        return self._redis.incr(count_key)

    def _get_inputs_key(self, method: Callable) -> str:
        """
        Returns the Redis key for the input history of the given method.
        """
        return self._make_key(method, "inputs")

    def _get_outputs_key(self, method: Callable) -> str:
        """
        Returns the Redis key for the output history of the given method.
        """
        return self._make_key(method, "outputs")

    def _record_call(self, method: Callable, args: tuple, result: Union[str, bytes, int, float]) -> None:
        """
        Records the call history for the given method, arguments, and result.
        """
        inputs_key = self._get_inputs_key(method)
        outputs_key = self._get_outputs_key(method)

        input_str = str(args)
        self._redis.rpush(inputs_key, input_str)

        self._redis.rpush(outputs_key, result)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis using the key.
        Returns the key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        self._increment_count(self.store)
        self._record_call(self.store, (data,), key)

        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the data stored in Redis with the given key.
        If the key does not exist, returns None.
        If a function is provided as the 'fn' argument, applies
        it to the retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the data stored in Redis with the given key and
        returns it as a string.
        If the key does not exist, returns None.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the data stored in Redis with the given key and
        returns it as an integer.
        If the key does not exist, returns None.
        """
        return self.get(key, fn=int)
