import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.developer_access import DeveloperAccess
from src.app.database.database_access.planet_access import PlanetAccess


@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(connection_test):
    async with sessionmanager.session() as session:
        dev_access = DeveloperAccess(session)

        await dev_access.createPlanetType(
            type_name="arctic",
            description="Arctic planet with snow and ice"
        )
        await session.commit()


async def test_one_type():
    async with sessionmanager.session() as session:
        planet_access = PlanetAccess(session)
        planet_type = await planet_access.get_random_planet_type()

        assert planet_type[0].type == "arctic"


async def test_multiple_types():
    # sketchy test with randomness, im too lazy to mock random
    async with sessionmanager.session() as session:
        dev_access = DeveloperAccess(session)
        for i in range(500):
            await dev_access.createPlanetType(
                type_name=f"arctic{i}",
                description="Arctic planet with snow and ice"
            )
        await session.commit()

        planet_access = PlanetAccess(session)

        fail_count = 0
        for i in range(100):
            failed = False
            prev_type = None
            for _ in range(2):
                planet_type = await planet_access.get_random_planet_type()
                failed = failed or prev_type == planet_type[0]
                prev_type = planet_type[0]
            if failed:
                fail_count += 1
        assert fail_count < 50
