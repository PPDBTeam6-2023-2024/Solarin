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

