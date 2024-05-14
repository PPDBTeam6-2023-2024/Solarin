import pytest
from sqlalchemy import update

from src.app.database.database_access.planet_access import PlanetAccess, Planet

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    await user_access.create_user(f"Test1", f"test1@test.test", f"test1")

    planet_access = data_access.PlanetAccess
    await planet_access.create_planet(f"Test Planet1", "arctic", 1, 1)
    await planet_access.create_planet_region(1, "arctic", 0.5, 0.5)

    await data_access.CityAccess.create_city(1, 1, 0.5, 0.5)
    await data_access.BuildingAccess.create_building(1, 1, "barracks", True)
    await data_access.BuildingAccess.create_building(1, 1, "farmpod", True)

    await data_access.ArmyAccess.create_army(1, 1, 0.5, 0.5)

    await data_access.ArmyAccess.add_to_army(1, "soldier", 1, 1000)
    await data_access.ArmyAccess.add_to_army(1, "fighter", 1, 1000)

    await data_access.commit()


@pytest.fixture(scope="function", autouse=True)
async def resource_access(data_access):
    yield data_access.ResourceAccess

@pytest.fixture(scope="function", autouse=True)
async def building_access(data_access):
    yield data_access.BuildingAccess

@pytest.fixture(scope="function", autouse=True)
async def city_access(data_access):
    yield data_access.CityAccess

@pytest.fixture(scope="function", autouse=True)
async def army_access(data_access):
    yield data_access.ArmyAccess


async def test_city_modifiers_1(data_access, resource_access, building_access):
    modifiers = await resource_access.get_maintenance_city(1)
    assert len(modifiers.values()) == 2


async def test_city_modifiers_2(data_access, resource_access, building_access):
    await building_access.create_building(1, 1, "space-dock", True)

    modifiers = await resource_access.get_maintenance_city(1)

    assert len(modifiers.values()) == 4
    assert modifiers["RA"] == 132


async def test_lose_city(data_access, resource_access, building_access, city_access):
    """
    Test that the user loses its city, because a lack of resources
    """
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    await resource_access.check_maintenance_city(1, 1, 3600)
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1
    b = await building_access.get_city_buildings(1)
    assert len(b) == 1


async def test_lose_city_2(data_access, resource_access, building_access, city_access):
    """
    Test that the user loses its city, because a lack of resources
    """
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 2

    await resource_access.add_resource(1, "RA", 102)

    await resource_access.check_maintenance_city(1, 1, 3600)
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 1


async def test_keep_city(data_access, resource_access, building_access, city_access):
    """
    Test that the user keeps the city, because he/she has enough resources
    """
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 2

    await resource_access.add_resource(1, "RA", 132)
    await resource_access.add_resource(1, "OI", 25)
    await resource_access.add_resource(1, "UR", 25)
    await resource_access.add_resource(1, "SOL", 25)

    await resource_access.check_maintenance_city(1, 1, 3600)
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 2


async def test_keep_city_2(data_access, resource_access, building_access, city_access):
    """
    Test that the user keeps the city, because he/she has enough resources
    """
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 2

    await resource_access.add_resource(1, "RA", 132)
    await resource_access.add_resource(1, "OI", 25)
    await resource_access.add_resource(1, "UR", 25)
    await resource_access.add_resource(1, "SOL", 25)

    await resource_access.check_maintenance_city(1, 1, 3600)
    cities = await city_access.get_cities_by_controller(1)
    assert len(cities) == 1

    b = await building_access.get_city_buildings(1)
    assert len(b) == 2


async def test_keep_army(data_access, resource_access, building_access, army_access):
    """
    Test that the user keeps the army, because he/she has enough resources
    """
    troops = await army_access.get_troops(1)

    assert troops[0].size == 1000

    m_cost = await resource_access.get_maintenance_army(1)
    assert m_cost["RA"] == 28*1000

    await resource_access.add_resource(1, "RA", 29*1000)
    await resource_access.add_resource(1, "OI", 29*1000)

    await resource_access.check_maintenance_army(1, 1, 3600)

    troops = await army_access.get_troops(1)

    assert troops[0].size == 1000


async def test_lose_troops(data_access, resource_access, building_access, army_access):
    """
    Test that the user loses troops, because he/she has not enough resources
    """
    troops = await army_access.get_troops(1)

    assert troops[0].size == 1000

    m_cost = await resource_access.get_maintenance_army(1)
    assert m_cost["RA"] == 28*1000

    await resource_access.check_maintenance_army(1, 1, 3600)

    troops = await army_access.get_troops(1)

    """
    Loses 20% of its army
    """
    assert troops[0].size == 900


async def test_lose_troops_2(data_access, resource_access, building_access, army_access):
    """
    Test that the user loses troops, because he/she has not enough resources
    """
    troops = await army_access.get_troops(1)

    assert troops[0].size == 1000

    m_cost = await resource_access.get_maintenance_army(1)
    assert m_cost["RA"] == 28*1000

    await resource_access.check_maintenance_army(1, 1, 3600*3)

    troops = await army_access.get_troops(1)

    assert troops[0].size == 730


async def test_lose_troops_3(data_access, resource_access, building_access, army_access):
    """
    Test that the user loses troops, because he/she has not enough resources
    """
    troops = await army_access.get_troops(1)

    assert troops[1].size == 1000

    m_cost = await resource_access.get_maintenance_army(1)

    assert m_cost["RA"] == 28*1000

    await resource_access.add_resource(1, "RA", 29 * 1000)
    await resource_access.check_maintenance_army(1, 1, 3600)

    troops = await army_access.get_troops(1)

    """
    The fighters lose troops, because not enough oil, while the troops remain
    """
    assert troops[0].size == 1000
    assert troops[1].size == 900


