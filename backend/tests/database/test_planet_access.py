import pytest

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    await planet_access.create_space_region("Test Region")
    for i in range(1, 6):
        await planet_access.create_planet(f"Test Planet{i}", "arctic", 1)
        await planet_access.create_planet_region(i, "arctic", 0.5, 0.5)
    await data_access.commit()

async def test_get_planets_of_user_1(data_access):
    await data_access.CityAccess.create_city(1, 1, 0, 0)
    planets = await data_access.PlanetAccess.get_planets_of_user(1)

    assert len(planets) == 1
    assert planets[0].id == 1

async def test_get_planets_of_user_2(data_access):
    for i in range(1, 6):
        await data_access.CityAccess.create_city(i, 1, 0, 0)

    planets = await data_access.PlanetAccess.get_planets_of_user(1)
    assert len(planets) == 5

