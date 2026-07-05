import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_cart_apply_coupon_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/cart/apply-coupon",
        headers={"X-Restaurant-ID": "1"},
        json={"code": "SUMMER50"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_cart_update_item_unauthorized(async_client: AsyncClient):
    response = await async_client.patch(
        "/api/v1/cart/items/1",
        headers={"X-Restaurant-ID": "1"},
        json={"quantity": 2}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_cart_calculate_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/cart/calculate",
        headers={"X-Restaurant-ID": "1"}
    )
    assert response.status_code == 401
