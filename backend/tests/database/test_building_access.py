import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import asyncio

from src.app.database.database_access.building_access import BuildingAccess
from src.app.database.database_access.data_access import DataAccess
from src.app.database.models.SettlementModels import BarracksType, BuildingInstance
from src.app.database.exceptions.not_found_exception import NotFoundException
from src.app.database.exceptions.invalid_action_exception import InvalidActionException

@pytest.fixture(scope="function")
async def building_access(data_access):
    yield data_access.BuildingAccess

@pytest.fixture(scope="function", autouse=True)
async def insert_data(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    await planet_access.create_space_region("Test Region")
    planet_id = await planet_access.create_planet("Test Planet", "arctic", 1, 1, 1)
    await planet_access.create_planet_region(planet_id, "arctic", 0.5, 0.5)
    city_access = data_access.CityAccess
    for i in range(1, 6):
        await city_access.create_city(planet_id, i, 1/i, 1/i)
    await data_access.commit()

async def test_create_building_1(building_access: BuildingAccess, session: AsyncSession):
    b_id = await building_access.create_building(1, 1, "nexus", True)
    await building_access.commit()

    stmt = (
        select(BuildingInstance)
        .where(BuildingInstance.id == b_id)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None
    assert result.building_type == "nexus"

async def test_create_building_2(building_access: BuildingAccess, data_access: DataAccess, session: AsyncSession):
    await data_access.ResourceAccess.add_resource(1, "TF", 6500)
    b_id = await building_access.create_building(1, 1, "nexus")
    await building_access.commit()

    stmt = (
        select(BuildingInstance)
        .where(BuildingInstance.id == b_id)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None
    assert result.building_type == "nexus"

async def test_create_building_3(building_access: BuildingAccess, data_access: DataAccess):
    await data_access.ResourceAccess.add_resource(1, "TF", 6499)
    with pytest.raises(InvalidActionException):
        await building_access.create_building(1, 1, "nexus")

async def test_get_city_buildings_1(building_access: BuildingAccess):
    await building_access.create_building(1, 1, "nexus", True)
    await building_access.commit()

    buildings = await building_access.get_city_buildings(1)
    assert len(buildings) == 1
    assert buildings[0].building_type == "nexus"

async def test_get_city_buildings_2(building_access: BuildingAccess):
    buildings = await building_access.get_city_buildings(1)
    assert len(buildings) == 0

async def test_get_city_buildings_3(building_access: BuildingAccess):
    await building_access.create_building(1, 1, "nexus", True)
    await building_access.create_building(1, 1, "farmpod", True)
    await building_access.commit()

    buildings = await building_access.get_city_buildings(1)
    assert len(buildings) == 2

async def test_get_building_types(building_access: BuildingAccess):
    types = await building_access.get_building_types()
    assert len(types) == 13

async def test_checked(building_access: BuildingAccess):
    b_id = await building_access.create_building(1, 1, "nexus", True)
    last_checked_b4 = await building_access.get_delta_time(b_id, True)
    await building_access.checked(b_id)
    last_checked_now = await building_access.get_delta_time(b_id, True)
    assert last_checked_now > last_checked_b4

async def test_get_available_building_types_1(building_access: BuildingAccess, data_access: DataAccess):
    await data_access.ResourceAccess.add_resource(1, "TF", 500)
    await building_access.create_building(1, 1, "Reinforced Techno-Mesh", True)
    await building_access.create_building(1, 1, "Sentry Tower", True)
    await building_access.commit()

    avail = await building_access.get_available_building_types(1, 1)
    assert len(avail) == 11
    for a in avail:
        assert not a["can_build"]

async def test_get_available_building_types_2(building_access: BuildingAccess, data_access: DataAccess):
    await data_access.ResourceAccess.add_resource(1, "TF", 500)
    await building_access.create_building(1, 1, "Reinforced Techno-Mesh", True)
    await building_access.commit()

    avail = await building_access.get_available_building_types(1, 1)
    assert len(avail) == 12
    can_build_count = 0
    for a in avail:
        if a["can_build"]:
            can_build_count += 1
    assert can_build_count == 1


