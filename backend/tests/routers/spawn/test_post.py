import pytest
from sqlalchemy import update
from datetime import datetime, timedelta

from src.app.database.database import sessionmanager
from src.app.database.database_access.data_access import DataAccess
from src.app.database.models import Planet
from src.app.routers.spawn.planet_generation import fibonacci_spiral_point

@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(data_access: DataAccess):
    await data_access.DeveloperAccess.create_planet_type("test_planet_type")
    await data_access.DeveloperAccess.create_planet_region_type("test_planet_region")
    await data_access.DeveloperAccess.create_associated_with("test_planet_type", "test_planet_region")
    await data_access.commit()

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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body

    assert planet_id == body["planet_id"]

async def test_3(client):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)
        planet_id = await data_access.PlanetAccess.create_planet("test", "test_planet_type", 1, 1)
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    planet_id = body["planet_id"]

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    assert body["planet_id"] == planet_id

async def test_fibonacci_1(client, data_access: DataAccess):
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    planet_id = body["planet_id"]

    planet = await data_access.PlanetAccess.get_planet(planet_id)
    x, y = fibonacci_spiral_point(1)
    assert planet.x == x
    assert planet.y == y

async def test_fibonacci_2(client, data_access: DataAccess):
    await data_access.PlanetAccess.create_planet("test", "test_planet_type", 1, 1)
    await data_access.commit()

    stmt = update(Planet).where(Planet.id == 1).values(created_at=datetime.utcnow() + timedelta(hours=2))
    async with sessionmanager.session() as session:
        await session.execute(stmt)
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

    response = client.get("/spawn", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "planet_id" in body
    planet_id = body["planet_id"]

    planet = await data_access.PlanetAccess.get_planet(planet_id)
    x, y = fibonacci_spiral_point(2)
    assert planet.x == x
    assert planet.y == y