import os
from config import REDIS_CONFIG
import redis.asyncio as aioredis


class RedisDriver:
    def __init__(self):
        self._redis_url = f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/{REDIS_CONFIG['db']}"
        self._redis_client = aioredis.from_url(self._redis_url, encoding="utf-8", decode_responses=True)

    async def get(self, key):
        return await self._redis_client.get(key)

    async def set(self, key, value, ttl=60*15):

        await self._redis_client.set(key, value)
        if ttl:
            await self._redis_client.expire(key, ttl)
        return True

