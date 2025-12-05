import redis.asyncio as redis
from typing import Optional, Any
import json
from app.config import settings


class RedisCache:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        self.redis = await redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            decode_responses=True
        )
    
    async def disconnect(self):
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
        
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        if not self.redis:
            return
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await self.redis.setex(key, ttl, value)
    
    async def delete(self, key: str):
        if not self.redis:
            return
        
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        if not self.redis:
            return False
        
        return await self.redis.exists(key) > 0


cache = RedisCache()