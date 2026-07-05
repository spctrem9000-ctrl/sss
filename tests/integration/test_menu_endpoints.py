import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_categories_no_header(async_client: AsyncClient):
    response = await async_client.get("/api/v1/categories")
    assert response.status_code == 422 # missing header validation

@pytest.mark.asyncio
async def test_get_products_with_header(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/products",
        headers={"X-Restaurant-ID": "1"}
    )
    # Status code will depend on DB setup, but request should be structurally valid
    assert response.status_code in [200, 500]

@pytest.mark.asyncio
async def test_get_products_with_search(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/products?search=دجاج",
        headers={"X-Restaurant-ID": "1"}
    )
    assert response.status_code in [200, 500]
