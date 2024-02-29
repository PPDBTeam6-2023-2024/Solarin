import asyncio

from ..src.app.config import DBConfig
from ..src.app.database.data_access import *


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
            mb = await da.AllianceAccess.getAllianceMessageBoard(f"{t_index} his clan")

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

    await da.commit()

    await db.disconnect()


async def checkAllianceMessages():
    session = await getSession()
    da = DataAccess(session)
    for i in range(100):
        m1 = await da.AllianceAccess.getMessagesAlliance(f"{1} his clan", 0, 20)
        assert len(m1) == 20

    for t_index in range(1, 51, 2):
        m1 = await da.AllianceAccess.getMessagesAlliance(f"{t_index} his clan", 0, 1)
        m2 = await da.AllianceAccess.getMessagesAlliance(f"{t_index} his clan", 1, 2)
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


def test_setup() -> None:
    asyncio.run(setup_data())


def test_alliance_messages():
    asyncio.run(checkAllianceMessages())


def test_friendships():
    asyncio.run(checkFriendShipRelations())


def test_alliance_members():
    asyncio.run(checkAllianceMembers())

