from redis.asyncio import Redis
from fastapi.encoders import jsonable_encoder
import json
from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel
import redis

T = TypeVar('T', bound=BaseModel)

class CacheService(Generic[T]):
    def __init__(self, redis: Redis, prefix: str = ""):
        self.redis = redis
        self.prefix = prefix
        self.default_expiration = 3600

    def _get_key(self, key: str) -> str:
        return f"{self.prefix}:{key}" if self.prefix else key

    async def get(self, key: str) -> Optional[dict]:
        try:
            data = await self.redis.get(self._get_key(key))
            return json.loads(data) if data else None
        except (redis.RedisError, json.JSONDecodeError) as e:
            return None

    async def set(
        self, 
        key: str, 
        value: Any, 
        expiration: Optional[int] = None
    ) -> bool:
        try:
            data = jsonable_encoder(value)
            await self.redis.set(
                self._get_key(key),
                json.dumps(data),
                ex=expiration or self.default_expiration
            )
            return True
        except redis.RedisError as e:
            print(f"Cache set error: {str(e)}") 
            return False

    async def delete(self, key: str) -> bool:
        try:
            await self.redis.delete(self._get_key(key))
            return True
        except redis.RedisError as e:
            return False

    async def clear_prefix(self, prefix: str) -> bool:
        try:
            keys = await self.redis.keys(f"{prefix}:*")
            if keys:
                await self.redis.delete(*keys)
            return True
        except redis.RedisError as e:
            return False