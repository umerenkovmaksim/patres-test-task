import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    response = await client.get("/readers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_protected_endpoint_with_token(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/readers", headers=headers)
    assert response.status_code == status.HTTP_200_OK
