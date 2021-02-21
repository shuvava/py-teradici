# -*- coding: utf-8 -*-
from __future__ import annotations
from threading import Lock
from typing import Optional

from redis import Redis


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instance: Optional[DbEngine] = None

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def create_engine(conn_string: str) -> Redis:
    return Redis.from_url(conn_string)


class DbEngine(metaclass=SingletonMeta):

    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.db = create_engine(self.conn_string)

    def get_session(self) -> Redis:
        client = self.db.client()
        return client
