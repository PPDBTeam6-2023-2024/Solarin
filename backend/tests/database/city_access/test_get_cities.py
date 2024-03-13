import pytest

from src.app.database.database import sessionmanager
from src.app.database.database_access.city_access import CityAccess
from src.app.database.database_access.user_access import UserAccess
from src.app.database.database_access.planet_access import PlanetAccess
from src.app.database.database_access.developer_access import DeveloperAccess


@pytest.fixture(scope="function", autouse=True)
async def insert_test_data(connection_test):
    async with sessionmanager.session() as session:
        user_access = UserAccess(session)
        user_id = await user_access.createUser(
            username="test",
            email="test",
            hashed_password="test"
        )

        developer_access = DeveloperAccess(session)
        await developer_access.createPlanetType(
            type_name="test"
        )

        planet_region_id = await developer_access.createPlanetRegionType(
            type_name="test"
        )

        planet_access = PlanetAccess(session)
        space_region_id = await planet_access.createSpaceRegion(
            region_name="test"
        )

        await planet_access.createPlanet(
            planet_name="test",
            planet_type="test",
            space_region_id=space_region_id
        )

        city_access = CityAccess(session)
        for _ in range(10):
            await city_access.createCity(
                region_id=planet_region_id,
                founder_id=user_id
            )
        await session.commit()


async def test_get_cities():
    async with sessionmanager.session() as session:
        city_access = CityAccess(session)
        cities = await city_access.get_cities(controller=1)
        assert len(cities) == 10
