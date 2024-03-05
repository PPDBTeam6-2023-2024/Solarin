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
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["username"] == "insert"
    assert body["email"] == "insert@example.com"
    assert "id" in body


async def test_not_logged_in(client):
    data = {
        "username": "insert",
        "password": "mypass123!"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers, params={"expire": 0})
    assert response.status_code == 200
    await asyncio.sleep(1)

    body = response.json()
    token = body["access_token"]

    headers = {'Authorization': f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401

    body = response.json()
    assert body == {"detail": "Could not validate credentials"}

