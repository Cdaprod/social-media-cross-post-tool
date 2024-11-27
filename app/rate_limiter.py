# app/rate_limiter.py

import redis
from redis.exceptions import RedisError
from .config import Config
import logging

logger = logging.getLogger(__name__)

class RedisRateLimiter:
    def __init__(self, redis_url, requests, window):
        self.redis = redis.StrictRedis.from_url(redis_url)
        self.requests = requests
        self.window = window

    def is_allowed(self, client_id: str) -> bool:
        try:
            key = f"rate_limit:{client_id}"
            current = self.redis.get(key)
            if current and int(current) >= self.requests:
                return False
            else:
                pipe = self.redis.pipeline()
                pipe.incr(key, 1)
                pipe.expire(key, self.window)
                pipe.execute()
                return True
        except RedisError as e:
            logger.error(f"Redis error in rate limiter: {str(e)}")
            return False