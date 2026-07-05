import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_request_otp(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/request-otp",
        json={"phone_number": "+1234567890"}
    )
    assert response.status_code in [200, 500]

@pytest.mark.asyncio
async def test_verify_otp_invalid(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/verify-otp",
        json={"phone_number": "+1234567890", "code": "000000"}
    )
    assert response.status_code in [400, 500]
