import asyncio
from ..src.app.database.database import db, Base
from sqlalchemy import *
from ..src.app.config import DBConfig
from ..src.app.database.data_access import *
from datetime import datetime, timedelta
from ..src.app.schemas import *
db_config = DBConfig(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        database="postgres"
    )


async def getSession():
    await db.connect(db_config)
    task = asyncio.ensure_future(db.get_db().__anext__())

    session: AsyncSession = await task

    await session.execute(text("SELECT * FROM user"))
    await session.commit()
    return session


async def clear_database(session):
    target_metadata: MetaData = Base.metadata

    for table in reversed(target_metadata.sorted_tables):
        await session.execute(table.delete())

    for sequence in reversed(target_metadata._sequences):
        await session.execute(text(f"""ALTER SEQUENCE IF EXISTS "{sequence}" RESTART WITH 1"""))

    await session.commit()


async def setup_data():
    session = await getSession()
    await clear_database(session)

    da = DataAccess(session)

    """
    Creates 50 users
    """
    for t_index in range(50):
        uuid = await da.UserAccess.createUser(f"username{t_index}", f"t{t_index}@gmail", f"hp{t_index}")
        a = await da.UserAccess.getFactionName(uuid)

        assert a == str(t_index + 1)
        assert uuid == t_index + 1

    await da.commit()

    """
    Creates friendship so that the first 20 are all friends with each other
    """
    for t_index in range(20):
        for t2_index in range(t_index, 20):
            if t_index == t2_index:
                continue

            await da.UserAccess.addFriendship(t_index + 1, t2_index + 1)

    """
    Create clan and add the ClanOwner to the clan
    """
    for t_index in range(1, 51, 2):
        await da.AllianceAccess.createAlliance(f"{t_index} his clan")
        await da.AllianceAccess.setAlliance(t_index, f"{t_index} his clan")
        await da.AllianceAccess.setAlliance(t_index + 1, f"{t_index} his clan")

    await da.commit()

    """
    Send messages inside each alliance
    """
    for times in range(21):
        for t_index in range(1, 51, 2):
            mb = await da.MessageAccess.getAllianceMessageBoard(f"{t_index} his clan")

            m_token = MessageToken(
                sender_id=t_index,
                message_board=mb,
                body="test"
            )

            mid = await da.MessageAccess.createMessage(m_token)

            m_token2 = MessageToken(
                sender_id=t_index + 1,
                message_board=mb,
                body="test reply",
                parent_message_id=mid
            )

            await da.MessageAccess.createMessage(m_token2)

    for t_index in range(1, 51, 2):
        pass

    """
    create some testing planets
    """
    sr_id = await da.PlanetAccess.createSpaceRegion("the expansion region")
    await da.DeveloperAccess.createPlanetType("Shadow planet", "planet where it is hard to see")
    p_id = await da.PlanetAccess.createPlanet("Umbara", "Shadow planet", sr_id)
    await da.DeveloperAccess.createPlanetRegionType("valley of death", "Ooh.. very scary")
    r_id = await da.PlanetAccess.createPlanetRegion(p_id, "valley of death")
    c_id = await da.CityAccess.createCity(r_id, 1)
    c_id2 = await da.CityAccess.createCity(r_id, 1)

    """
    Create some types of buildings and resources
    """
    await da.DeveloperAccess.createProductionBuildingType("The mines of moria", 100, 2000)
    await da.DeveloperAccess.createBarracksType("Kamino training complex")
    await da.DeveloperAccess.createHouseType("Solarin mansion", 50)
    await da.DeveloperAccess.createResourceType("Vibranium")
    await da.DeveloperAccess.createResourceType("Energon")
    await da.DeveloperAccess.setProducesResources("The mines of moria", "Vibranium")

    """
    Create some actual buildings inside cities
    """
    await da.BuildingAccess.createBuilding(c_id, "The mines of moria")
    b_id = await da.BuildingAccess.createBuilding(c_id, "Kamino training complex")
    await da.BuildingAccess.createBuilding(c_id, "Solarin mansion")

    await da.BuildingAccess.createBuilding(c_id2, "The mines of moria")
    b_id2 = await da.BuildingAccess.createBuilding(c_id2, "Kamino training complex")
    await da.BuildingAccess.createBuilding(c_id2, "Solarin mansion")


    """
    create an army
    """

    a_id = await da.ArmyAccess.createArmy(user_id=1)
    await da.DeveloperAccess.createToopType("tank", timedelta(hours=4),
                                            BattleStats(attack=5, defense=50, city_attack=1, city_defense=120,
                                            recovery=5, speed=0.4))

    await da.DeveloperAccess.createToopType("soldier", timedelta(hours=4, minutes=5),
                                            BattleStats(attack=30, defense=30, city_attack=30, city_defense=20,
                                                        recovery=5, speed=0.9))

    await da.DeveloperAccess.setTroopTypeCost("tank", [("Vibranium", 20), ("Energon", 2)])
    await da.DeveloperAccess.setTroopTypeCost("soldier", [("Vibranium", 5)])
    await da.ArmyAccess.addToArmy(a_id, "tank", 2, 20)
    await da.ArmyAccess.addToArmy(a_id, "tank", 2, 10)
    await da.ArmyAccess.addToArmy(a_id, "tank", 3, 10)

    """
    start training units
    """
    await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
    await da.TrainingAccess.trainType(a_id, b_id, "tank", 3, 10)
    await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)
    await da.TrainingAccess.trainType(a_id, b_id2, "tank", 3, 10)

    await da.commit()

    await db.disconnect()


async def checkMessages():
    session = await getSession()
    da = DataAccess(session)
    for i in range(100):
        m1 = await da.MessageAccess.getMessagesAlliance(f"{1} his clan", 0, 20)
        assert len(m1) == 20

    for t_index in range(1, 51, 2):
        m1 = await da.MessageAccess.getMessagesAlliance(f"{t_index} his clan", 0, 1)
        m2 = await da.MessageAccess.getMessagesAlliance(f"{t_index} his clan", 1, 2)
        assert len(m1) == 1
        assert len(m2) == 2
        assert m1[0][0].body == "test"
        assert m2[0][0].body == "test reply"

    await da.commit()
    await db.disconnect()


async def checkFriendShipRelations():
    session = await getSession()
    da = DataAccess(session)

    for t_index in range(20):
        friends = await da.UserAccess.getFriends(t_index+1)
        assert len(friends) == 19
        for f in friends:
            assert 0 < f[0] <= 20
            assert f[0] != t_index+1

    await da.commit()
    await db.disconnect()


async def checkAllianceMembers():
    session = await getSession()
    da = DataAccess(session)
    for t_index in range(1, 51, 2):
        members = await da.AllianceAccess.getAllianceMembers(f"{t_index} his clan")
        assert len(members) == 2
        for m in members:
            assert m[0].email in (f"t{t_index-1}@gmail", f"t{t_index}@gmail")

    await da.commit()
    await db.disconnect()


async def checkPlanet():
    session = await getSession()

    da = DataAccess(session)

    regions = await da.PlanetAccess.getRegions(1)
    assert len(regions) == 1
    assert regions[0][0].id == 1

    cities = await da.PlanetAccess.getPlanetCities(1)
    assert len(cities) == 2
    assert cities[0][0].id == 1
    assert cities[0][0].controlled_by == 1

    await da.commit()
    await db.disconnect()




def test_setup() -> None:
    asyncio.run(setup_data())


def test_alliance_messages():
    asyncio.run(checkMessages())


def test_friendships():
    asyncio.run(checkFriendShipRelations())


def test_alliance_members():
    asyncio.run(checkAllianceMembers())


def test_planets() -> None:
    asyncio.run(checkPlanet())

