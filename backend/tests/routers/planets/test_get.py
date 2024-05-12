from sqlalchemy import update
import pytest

from src.app.database.models import Planet

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    for i in range(1, 6):
        await planet_access.create_planet(f"Test Planet{i}", "arctic", 1, 1)
        await planet_access.create_planet_region(i, "arctic", 0.5, 0.5)
    await data_access.commit()

async def test_get_planets_public_1(client, auth):
    user_id, auth_header = auth
    response = client.get("/planet/planets/public", headers=auth_header)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 0


async def test_get_planets_public_2(client, auth, data_access):
    user_id, auth_header = auth
    for i in range(1, 2):
        await data_access.ArmyAccess.create_army(user_id, i, 0, 0)
    for i in range(2, 6):
        await data_access.CityAccess.create_city(i, user_id, 0, 0)

    for i in range(1, 6):
        p_id = await data_access.PlanetAccess.create_planet(f"Test Planet{i}", "arctic", 1, 1)
        await data_access.PlanetAccess.create_planet_region(p_id, "arctic", 0.5, 0.5)
        stmt = update(Planet).where(Planet.id == p_id).values(visible=True)
        await data_access.PlanetAccess.session.execute(stmt)

    await data_access.commit()

    response = client.get("/planet/planets/public", headers=auth_header)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 10
    needed = ["name", "x", "y"]
    for planet in body:
        for key in needed:
            assert key in planet

async def test_get_planets_private_1(client, auth):
    user_id, auth_header = auth
    response = client.get("/planet/planets/private", headers=auth_header)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 0

async def test_get_planets_private_2(client, auth, data_access):
    user_id, auth_header = auth
    for i in range(1, 2):
        await data_access.ArmyAccess.create_army(user_id, i, 0, 0)
    for i in range(2, 6):
        await data_access.CityAccess.create_city(i, user_id, 0, 0)

    for i in range(1, 6):
        p_id = await data_access.PlanetAccess.create_planet(f"Test Planet{i}", "arctic", 1, 1)
        await data_access.PlanetAccess.create_planet_region(p_id, "arctic", 0.5, 0.5)
        stmt = update(Planet).where(Planet.id == p_id).values(visible=True)
        await data_access.PlanetAccess.session.execute(stmt)

    await data_access.commit()

    response = client.get("/planet/planets/private", headers=auth_header)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 5
    needed = ["name", "x", "y"]
    for planet in body:
        for key in needed:
            assert key in planet