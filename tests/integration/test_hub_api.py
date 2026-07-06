import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_hub_heartbeat_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/hub/heartbeat",  # Fixed: added /api prefix
        json={"version": "1.0.0", "device_name": "Kitchen Display"}
    )
    assert response.status_code == 422  # 422 because X-Hub-Api-Key header is missing

@pytest.mark.asyncio
async def test_hub_get_orders_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/api/v1/hub/orders/new")  # Fixed: added /api prefix
    assert response.status_code == 422  # 422 because X-Hub-Api-Key header is missing

@pytest.mark.asyncio
async def test_hub_get_settings_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/api/v1/hub/settings")  # Fixed: added /api prefix
    assert response.status_code == 422  # 422 because X-Hub-Api-Key header is missing
