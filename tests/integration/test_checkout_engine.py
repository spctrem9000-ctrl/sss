import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_checkout_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/orders",
        headers={"X-Restaurant-ID": "1"},
        json={"payment_method": "cash"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_orders_unauthorized(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/orders/history",
        headers={"X-Restaurant-ID": "1"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_cancel_order_unauthorized(async_client: AsyncClient):
    response = await async_client.patch(
        "/api/v1/orders/1/cancel",
        headers={"X-Restaurant-ID": "1"}
    )
    assert response.status_code == 401
