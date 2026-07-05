import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_hub_heartbeat_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/v1/hub/heartbeat",
        json={"version": "1.0.0", "device_name": "Kitchen Display"}
    )
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_hub_get_orders_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/v1/hub/orders/new")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_hub_get_settings_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/v1/hub/settings")
    assert response.status_code == 401
