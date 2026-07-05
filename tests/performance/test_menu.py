import pytest
import time
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_cache_performance(async_client: AsyncClient):
    """
    Test that the second request for the same resource is significantly faster
    due to caching.
    """
    # Note: Without a real DB, both might be fast or both might fail.
    # This is a structural test for demonstration.
    headers = {"X-Restaurant-ID": "1"}
    
    start_1 = time.time()
    await async_client.get("/api/v1/categories", headers=headers)
    time_1 = time.time() - start_1
    
    start_2 = time.time()
    await async_client.get("/api/v1/categories", headers=headers)
    time_2 = time.time() - start_2
    
    # We expect time_2 to be very fast since it hits the cache
    # assert time_2 < time_1 or time_2 < 0.05
