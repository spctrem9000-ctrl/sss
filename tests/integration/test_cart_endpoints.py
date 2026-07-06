import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_cart_unauthorized(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/cart",
        headers={"X-Restaurant-ID": "1"}
    )
    # 401 Unauthorized expected because no JWT is provided
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_add_item_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/cart/items",  # Fixed: was /add-item, correct path is /items
        headers={"X-Restaurant-ID": "1", "X-Branch-ID": "1"},
        json={"product_id": 1, "quantity": 1}
    )
    assert response.status_code == 401
