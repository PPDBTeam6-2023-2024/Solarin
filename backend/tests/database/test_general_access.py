import pytest
from sqlalchemy import update

from src.app.database.database_access.planet_access import PlanetAccess, Planet

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    for i in range(1, 6):
        await planet_access.create_planet(f"Test Planet{i}", "arctic", 1, 1)
        await planet_access.create_planet_region(i, "arctic", 0.5, 0.5)

    """
    create an army
    """

    a_id = await data_access.ArmyAccess.create_army(1, 1, 0.5, 0.5)
    await data_access.ArmyAccess.add_to_army(a_id, "soldier", 5, 5)

    await data_access.commit()


@pytest.fixture(scope="function", autouse=True)
async def general_access(data_access):
    yield data_access.GeneralAccess

async def test_general_assign(data_access, general_access):
    generals = await general_access.get_available_generals(1)

    assert len(generals) == 8

    await general_access.assign_general(1, 1, "brave")

    generals = await general_access.get_available_generals(1)

    assert len(generals) == 7

async def test_general_override_assign(data_access, general_access):
    await test_general_assign(data_access, general_access)

    await general_access.assign_general(1, 1, "angry")

    generals = await general_access.get_available_generals(1)

    assert len(generals) == 7

    for g in generals:
        assert g.name != "angry"

async def test_general_unassign(data_access, general_access):
    await test_general_assign(data_access, general_access)

    await general_access.remove_general(1, 1)

    generals = await general_access.get_available_generals(1)

    assert len(generals) == 8

async def test_get_general(data_access, general_access):
    await test_general_assign(data_access, general_access)
    general = await general_access.get_general(1)
    assert general.name == "brave"

async def test_get_modifiers(data_access, general_access):
    await test_general_assign(data_access, general_access)
    modifiers = await general_access.get_modifiers(1, "brave")
    assert len(modifiers) == 3