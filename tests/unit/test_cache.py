import pytest
import asyncio
from app.core.cache import InMemoryCache

@pytest.mark.asyncio
async def test_in_memory_cache():
    cache = InMemoryCache()
    
    # Test SET and GET
    await cache.set("test_key", "test_value", ttl_seconds=1)
    val = await cache.get("test_key")
    assert val == "test_value"
    
    # Test Expiry
    await asyncio.sleep(1.1)
    val2 = await cache.get("test_key")
    assert val2 is None

@pytest.mark.asyncio
async def test_delete_pattern():
    cache = InMemoryCache()
    await cache.set("products:rest_1", "data1")
    await cache.set("products:rest_2", "data2")
    await cache.set("category:rest_1", "data3")
    
    await cache.delete_pattern("products:")
    
    assert await cache.get("products:rest_1") is None
    assert await cache.get("products:rest_2") is None
    assert await cache.get("category:rest_1") == "data3"
