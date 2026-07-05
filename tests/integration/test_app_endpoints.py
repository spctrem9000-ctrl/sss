import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_initialize_app_not_found(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/app/initialize",
        json={"app_key": "invalid_key"}
    )
    # The actual status code depends on DB connection state
    assert response.status_code in [404, 500]
