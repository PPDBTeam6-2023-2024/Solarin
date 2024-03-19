import pytest
import asyncio
from tests.conftest import client


@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(client):
    data = {
        "email": "insert@example.com",
        "username": "insert",
        "password": "mypass123!"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200


async def test_logged_in(client):
    data = {
        "username": "insert",
        "password": "mypass123!"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    token = body["access_token"]

    headers = {'Authorization': f"Bearer {token}"}
    response = client.get("/auth/validate", headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["success"]

