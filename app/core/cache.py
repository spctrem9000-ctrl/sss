import time
from typing import Any, Optional, Dict
from loguru import logger

class CacheEntry:
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = time.time() + ttl_seconds

class InMemoryCache:
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}

    async def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry:
            if time.time() < entry.expires_at:
                logger.info(f"Cache Hit: {key}")
                return entry.value
            else:
                # Expired
                del self._store[key]
        
        logger.info(f"Cache Miss: {key}")
        return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        self._store[key] = CacheEntry(value, ttl_seconds)

    async def delete(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    async def delete_pattern(self, pattern: str) -> None:
        keys_to_delete = [k for k in self._store.keys() if pattern in k]
        for k in keys_to_delete:
            del self._store[k]

cache = InMemoryCache()
