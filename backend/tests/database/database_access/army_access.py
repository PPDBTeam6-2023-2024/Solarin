from sqlalchemy import select
import pytest

from tests.conftest import sessionmanager, connection_test

from src.app.database.database_access.army_access import ArmyAccess, Army
from src.app.database.database_access.data_access import DataAccess

@pytest.fixture(scope="function", autouse=True)
async def insert_data(connection_test):
    async with sessionmanager.session() as session:
        data_access = DataAccess(session)
        for i in range(1, 6):
            await data_access.UserAccess.create_user(f"Test{i}", f"Test{i}", f"Test{i}")
        await data_access.DeveloperAccess.create_planet_type("Test Planet Type")
        await data_access.PlanetAccess.create_space_region("Test Space Region")
        await data_access.PlanetAccess.create_planet("Test Planet", "Test Planet Type", 1)
        await data_access.DeveloperAccess.create_planet_region_type("Test Planet Region Type 1")
        await data_access.DeveloperAccess.create_planet_region_type("Test Planet Region Type 2")
        await data_access.PlanetAccess.create_planet_region(1, "Test Planet Region Type 1", 0.5, 0)
        await data_access.PlanetAccess.create_planet_region(1, "Test Planet Region Type 2", 0.5, 1)
        #await data_access.DeveloperAccess.create_troop_type
        await session.commit()


async def test_create_army_1(connection_test):
    async with sessionmanager.session() as session:
        army_access = ArmyAccess(session)
        await army_access.create_army(1, 1, 0, 0)
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(Army)
        )
        result = await session.execute(stmt)
        assert result.scalar_one_or_none() is not None


async def test_create_army_2(connection_test):
    async with sessionmanager.session() as session:
        army_access = ArmyAccess(session)

        for i in range(4):
            await army_access.create_army(1, 1, 0, 0)
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(Army)
        )
        result = await session.execute(stmt)
        assert len(result.scalars().all()) == 4

async def test_add_to_army(connection_test):
    async with sessionmanager.session() as session:
        army_access = ArmyAccess(session)
        await army_access.create_army(1, 1, 0, 0)
        await army_access.add_to_army(1, 1, 1)
        await session.commit()

    async with sessionmanager.session() as session:
        stmt = (
            select(Army)
            .where(Army.id == 1)
        )
        result = await session.execute(stmt)
        assert result.scalar_one_or_none().size == 1

