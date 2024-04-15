import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.app.database.database_access.army_access import ArmyAccess
from src.app.database.models.ArmyModels import Army, ArmyConsistsOf, AttackArmy
from src.app.database.exceptions.not_found_exception import NotFoundException
from src.app.database.exceptions.invalid_action_exception import InvalidActionException

@pytest.fixture(scope="function")
async def army_access(data_access):
    yield data_access.ArmyAccess

@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    for i in range(1, 6):
        await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
    planet_access = data_access.PlanetAccess
    await planet_access.create_space_region("Test Region")
    await planet_access.create_planet("Test Planet", "arctic", 1)
    await data_access.commit()

async def test_create_army(army_access: ArmyAccess, session: AsyncSession):
    await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    stmt = (
        select(Army)
        .where(Army.id == 1)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None
    assert result.x == 1
    assert result.y == 1

async def test_add_to_army_1(army_access: ArmyAccess, session: AsyncSession):
    army_id = await army_access.create_army(1, 1, 1, 1)        
    await army_access.add_to_army(army_id, "assassin", 1, 1)
    await army_access.commit()

    stmt = (
        select(Army)
        .where(Army.id == army_id)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None
    assert result.x == 1
    assert result.y == 1

    stmt = (
        select(ArmyConsistsOf)
        .where(ArmyConsistsOf.army_id == army_id)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None
    assert result.troop_type == "assassin"
    assert result.size == 1
    assert result.rank == 1

async def test_add_to_army_2(army_access: ArmyAccess):
    try:
        await army_access.add_to_army(2, "assassin", 1, 1)
        await army_access.commit()
    except IntegrityError:
        pass
    else:
        assert False

async def test_get_troops_1(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id, "assassin", 1, 1)
    await army_access.add_to_army(army_id, "assassin", 2, 1)
    await army_access.add_to_army(army_id, "soldier", 1, 10)
    await army_access.commit()

    troops = await army_access.get_troops(army_id)
    assert len(troops) == 3
    assassin_lvl1 = troops[0]
    assert assassin_lvl1.troop_type == "assassin"
    assert assassin_lvl1.size == 1
    assert assassin_lvl1.rank == 1
    assassin_lvl2 = troops[1]
    assert assassin_lvl2.troop_type == "assassin"
    assert assassin_lvl2.size == 1
    assert assassin_lvl2.rank == 2
    soldier = troops[2]
    assert soldier.troop_type == "soldier"
    assert soldier.size == 10
    assert soldier.rank == 1

async def test_get_troops_2(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)

    await army_access.commit()

    troops = await army_access.get_troops(army_id)
    assert len(troops) == 0

async def test_get_army_by_id_1(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    army = await army_access.get_army_by_id(army_id)
    assert army.x == 1
    assert army.y == 1

async def test_get_army_by_id_2(army_access: ArmyAccess):
    army = await army_access.get_army_by_id(1)
    assert army is None

async def test_get_user_armies_1(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    armies = await army_access.get_user_armies(1)
    assert len(armies) == 1
    assert armies[0].id == army_id

async def test_get_user_armies_2(army_access: ArmyAccess):
    armies = await army_access.get_user_armies(1)
    assert len(armies) == 0

async def test_get_user_armies_3(army_access: ArmyAccess):
    army_id_1 = await army_access.create_army(1, 1, 1, 1)
    army_id_2 = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    armies = await army_access.get_user_armies(1)
    assert len(armies) == 2
    assert armies[0].id == army_id_1 and armies[1].id == army_id_2 or armies[0].id == army_id_2 and armies[1].id == army_id_1

async def test_get_armies_on_planet_1(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    armies = await army_access.get_armies_on_planet(1)
    assert len(armies) == 1
    assert armies[0].id == army_id

async def test_get_armies_on_planet_2(army_access: ArmyAccess):
    armies = await army_access.get_armies_on_planet(1)
    assert len(armies) == 0

async def test_get_armies_on_planet_3(army_access: ArmyAccess):
    army_id_1 = await army_access.create_army(1, 1, 1, 1)
    army_id_2 = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    armies = await army_access.get_armies_on_planet(1)
    assert len(armies) == 2
    assert armies[0].id == army_id_1 and armies[1].id == army_id_2 or armies[0].id == army_id_2 and armies[1].id == army_id_1

async def test_get_army_time_delta_1(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.commit()

    delta = await army_access.get_army_time_delta(army_id, 0)
    assert delta.total_seconds() == 0

async def test_get_army_time_delta_2(army_access: ArmyAccess):
    delta = await army_access.get_army_time_delta(1, 0)
    assert delta.total_seconds() == 0

async def test_get_army_time_delta_3(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    # has ms of 250
    await army_access.add_to_army(army_id, "soldier", 1, 1)
    await army_access.commit()

    delta = await army_access.get_army_time_delta(army_id, 1)
    assert delta.total_seconds() == 3600 * 4

async def test_get_army_time_delta_4(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    # has ms of 350
    await army_access.add_to_army(army_id, "assassin", 1, 1)
    await army_access.commit()

    delta = await army_access.get_army_time_delta(army_id, 1)
    assert delta.total_seconds() == pytest.approx(3600 * 4 * 250/350)

async def test_change_army_direction(army_access: ArmyAccess):
    army_id = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id, "soldier", 1, 1)
    result = await army_access.get_army_by_id(army_id)
    assert result is not None
    assert result.to_x == 1
    assert result.to_y == 1
    time_b4 = result.departure_time
    await army_access.change_army_direction(1, army_id, 0, 0)
    await army_access.commit()

    result = await army_access.get_army_by_id(army_id)
    assert result is not None
    assert result.departure_time != time_b4
    assert result.to_x == 0
    assert result.to_y == 0

async def test_attack_army_1(army_access: ArmyAccess, session: AsyncSession):
    army_id_ally = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id_ally, "soldier", 1, 1)
    army_id_enemy = await army_access.create_army(2, 1, 1, 1)
    await army_access.add_to_army(army_id_enemy, "soldier", 1, 1)
    await army_access.commit()

    await army_access.attack_army(army_id_ally, army_id_enemy)
    await army_access.commit()

    stmt = (
        select(AttackArmy)
        .where(AttackArmy.army_id == army_id_ally, AttackArmy.target_id == army_id_enemy)
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    assert result is not None

async def test_attack_army_2(army_access: ArmyAccess):
    try:
        await army_access.attack_army(1, 2)
        await army_access.commit()
    except NotFoundException:
        pass
    else:
        assert False

async def test_attack_army_3(army_access: ArmyAccess):
    army_id_ally_1 = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id_ally_1, "soldier", 1, 1)
    army_id_ally_2 = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id_ally_2, "soldier", 1, 1)
    await army_access.commit()

    try:
        await army_access.attack_army(army_id_ally_1, army_id_ally_2)
    except InvalidActionException as e:
        assert "own" in str(e)
    else:
        assert False


async def test_attack_army_4(army_access: ArmyAccess, data_access):
    await data_access.AllianceAccess.create_alliance("test")
    await data_access.AllianceAccess.set_alliance(1, "test")
    await data_access.AllianceAccess.set_alliance(2, "test")

    army_id_ally = await army_access.create_army(1, 1, 1, 1)
    await army_access.add_to_army(army_id_ally, "soldier", 1, 1)
    army_id_alliance_ally = await army_access.create_army(2, 1, 1, 1)
    await army_access.add_to_army(army_id_alliance_ally, "soldier", 1, 1)

    await army_access.commit()

    try:
        await army_access.attack_army(army_id_ally, army_id_alliance_ally)
    except InvalidActionException as e:
        assert "allies" in str(e)
    else:
        assert False