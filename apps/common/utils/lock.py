# coding=utf-8
"""
    @project: qabot
    @Author：Tiger
    @file： lock.py
    @date：2023/9/11 11:45
    @desc:
"""
from functools import wraps

import uuid_utils.compat as uuid
from django.core.cache import caches
from django_redis import get_redis_connection

memory_cache = caches['default']

class RedisLock():
    def __init__(self):
        self.lock_value = None

    def try_lock(self, key: str, timeout=None):
        """
        getLock
        :param key:    getLock key
        :param timeout timeout
        :return: YesNo getarrive lock
        """
        redis_client = get_redis_connection("default")
        if timeout is None:
            timeout = 3600  # Default timeout for3600 seconds
        self.lock_value = str(uuid.uuid7())
        return redis_client.set(key, self.lock_value, nx=True, ex=timeout)


    def un_lock(self, key: str):
        """
        Unlock
        :param key: Unlock key
        :return: YesNo unlocksuccess
        """
        redis_client = get_redis_connection("default")
        unlock_script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
        redis_client.eval(unlock_script, 1, key, self.lock_value)


def lock(lock_key, timeout=None):
    """
    Lock a piece to Number
    @param lock_key: Lockkey characterstring|letterNumber  function NumberReturnvalueforcharacter string
    @param timeout:  timeout
    :return: decorator letterNumber currentThe decorator mainly limits one pieces key to only one pieces thread.Call The same key can only block etc. until the previous pieces task is completed. Different keys do not need to wait.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = lock_key(*args, **kwargs) if callable(lock_key) else lock_key
            rlock = RedisLock()
            if not rlock.try_lock(key, timeout):
                # getLock Failed, Customizedifferent normalorReturn
                return None
            try:
                return func(*args, **kwargs)
            finally:
                rlock.un_lock(key)

        return wrapper

    return decorator
