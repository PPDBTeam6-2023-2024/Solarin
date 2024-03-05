import pytest
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


async def test_correct_login(client):
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
    assert body["token_type"] == "bearer"
    assert "access_token" in body


async def test_wrong_login(client):
    data = {
        "username": "insert",
        "password": "mypass123!1"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 401
