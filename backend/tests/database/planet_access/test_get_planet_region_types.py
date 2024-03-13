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
        await dev_access.createPlanetRegionType(
            type_name="snowy",
            description="a lot of snow"
        )
        await dev_access.createPlanetRegionType(
            type_name="icy",
            description="a lot of ice"
        )
        await dev_access.createAssociatedWith(
            planet_type="arctic",
            region_type="snowy"
        )
        await dev_access.createAssociatedWith(
            planet_type="arctic",
            region_type="icy"
        )
        await session.commit()


async def test_get_planet_region_types():
    async with sessionmanager.session() as session:
        planet_access = PlanetAccess(session)
        region_types = await planet_access.get_planet_region_types(
            planet_type="arctic"
        )

        assert len(region_types) == 2
        assert region_types[0][0].region_type == "snowy"
        assert region_types[1][0].region_type == "icy"
