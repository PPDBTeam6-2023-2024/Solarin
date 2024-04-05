import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess

from tests.conftest import client

@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)
        await data_access.DeveloperAccess.createPlanetType("test_planet_type")
        await data_access.DeveloperAccess.createPlanetRegionType("test_planet_region")
        await data_access.DeveloperAccess.createAssociatedWith("test_planet_type", "test_planet_region")
        await data_access.PlanetAccess.createSpaceRegion("test_region")
        await session.commit()

async def test_1(client):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body


async def test_2(client):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    planet_id = body["planet_id"]

    
    data = {
        "email": "user2@example.com",
        "username": "user2",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body

    assert planet_id == body["planet_id"]

async def test_3(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)
        planet_id = await data_access.PlanetAccess.createPlanet("test", "test_planet_type", 1)
        await session.commit()

    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    assert body["planet_id"] == planet_id


async def test_4(client):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    planet_id = body["planet_id"]

    response = client.post("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    assert body["planet_id"] == planet_id