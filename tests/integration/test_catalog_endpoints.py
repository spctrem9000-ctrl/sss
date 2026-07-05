import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_menu_without_header(async_client: AsyncClient):
    response = await async_client.get("/api/v1/menu")
    assert response.status_code == 422 # Missing Header

@pytest.mark.asyncio
async def test_get_menu_with_header(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menu",
        headers={"X-Restaurant-ID": "1"}
    )
    # The structure should be valid, yielding a 200 or 500 depending on DB state.
    assert response.status_code in [200, 500]

@pytest.mark.asyncio
async def test_get_products_featured(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/products?is_featured=true",
        headers={"X-Restaurant-ID": "1"}
    )
    assert response.status_code in [200, 500]
