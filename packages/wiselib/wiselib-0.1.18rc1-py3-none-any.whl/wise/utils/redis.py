from unittest.mock import MagicMock
from time import perf_counter as time_now

import redis
import redis.lock
from django.conf import settings

from wise.utils.exception import NotLockedError
from wise.utils.monitoring import REDIS_COMMAND_DURATION

_redis_client = None


class RedisClientWithMonitoring(redis.Redis):
    def __init__(self, *args, **kwargs):
        self._client = redis.Redis(*args, **kwargs)

    def __getattr__(self, name):
        def method(*args, **kwargs):
            start = time_now()
            success = "false"
            try:
                ret = getattr(self._client, name)(*args, **kwargs)
                success = "true"
                return ret
            finally:
                REDIS_COMMAND_DURATION.labels(name, success).observe(time_now() - start)

        return method


def get_redis_client() -> RedisClientWithMonitoring:
    global _redis_client

    if _redis_client:
        return _redis_client

    redis_settings = settings.ENV.redis
    _redis_client = RedisClientWithMonitoring(
        host=redis_settings.host,
        port=redis_settings.port,
        db=redis_settings.db,
        username=redis_settings.user,
        password=redis_settings.password,
    )
    return _redis_client


def ensure_locked(lock: redis.lock.Lock) -> None:
    if lock.acquire(blocking=False):
        lock.release()
        raise NotLockedError()


def get_mock_redis():
    r = MagicMock()
    r.get = lambda *args, **kwargs: None
    return r
