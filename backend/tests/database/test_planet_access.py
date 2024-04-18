import pytest
from sqlalchemy import update

from src.app.database.database_access.planet_access import PlanetAccess, Planet

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    await planet_access.create_space_region("Test Region")
    for i in range(1, 6):
        await planet_access.create_planet(f"Test Planet{i}", "arctic", 1, 1, 1)
        await planet_access.create_planet_region(i, "arctic", 0.5, 0.5)
    await data_access.commit()


@pytest.fixture(scope="function", autouse=True)
async def planet_access(data_access):
    yield data_access.PlanetAccess

async def test_get_planets_of_user_1(data_access, planet_access):
    await data_access.CityAccess.create_city(1, 1, 0, 0)
    planets = await planet_access.get_planets_of_user(1)

    assert len(planets) == 1
    assert planets[0].id == 1

async def test_get_planets_of_user_2(data_access, planet_access):
    for i in range(1, 6):
        await data_access.CityAccess.create_city(i, 1, 0, 0)

    planets = await planet_access.get_planets_of_user(1)
    assert len(planets) == 5


async def test_get_planets_of_user_3(data_access, planet_access):
    for i in range(1, 6):
        await data_access.ArmyAccess.create_army(1, i, 0, 0)

    planets = await planet_access.get_planets_of_user(1)
    assert len(planets) == 5

async def test_get_planets_of_user_4(data_access, planet_access):
    for i in range(1, 2):
        await data_access.ArmyAccess.create_army(1, i, 0, 0)
    for i in range(2, 6):
        await data_access.CityAccess.create_city(i, 1, 0, 0)

    planets = await planet_access.get_planets_of_user(1)
    assert len(planets) == 5

async def test_get_panet_count_1(planet_access):
    region_id = await planet_access.create_space_region("Test Region 2")

    count = await planet_access.get_planets_amount(region_id)
    assert count == 0

async def test_get_panet_count_2(planet_access):
    region_id = await planet_access.create_space_region("Test Region 2")
    for i in range(1, 6):
        await planet_access.create_planet(f"Test Planet{i}", "arctic", region_id, 1, 1)

    count = await planet_access.get_planets_amount(region_id)
    assert count == 5

async def test_get_planets_global_1(planet_access: PlanetAccess):
    planets = await planet_access.get_planets_global(1)
    assert len(planets) == 0

async def test_get_planets_global_2(planet_access, data_access):
    for i in range(1, 6):
        await data_access.ArmyAccess.create_army(1, i, 0, 0)
    planets = await planet_access.get_planets_global(1)
    assert len(planets) == 5

async def test_get_planets_global_3(planet_access, data_access, session):
    for i in range(1, 2):
        await data_access.ArmyAccess.create_army(1, i, 0, 0)
    for i in range(2, 6):
        await data_access.CityAccess.create_city(i, 1, 0, 0)


    for i in range(1, 6):
        p_id = await planet_access.create_planet(f"Test Planet{i}", "arctic", 1, 1, 1)
        await planet_access.create_planet_region(p_id, "arctic", 0.5, 0.5)
        stmt = update(Planet).where(Planet.id == p_id).values(visible=True)
        await planet_access.session.execute(stmt)

    planets = await planet_access.get_planets_global(1)
    assert len(planets) == 10