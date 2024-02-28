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

async def setup_data():
    await db.connect(db_config)
    task = asyncio.ensure_future(db.get_db().__anext__())

    session = await task
    da = DataAccess(session)

    #t_index = 1
    #uuid = await da.createUser(f"t{t_index}@gmail", f"usernamet{t_index}", f"hp{t_index}")
    #a = await da.getFactionName(uuid)
    """
    session.add(User("t1@gmail", "username", "hp"))
    session.add(User("t2@gmail", "username2", "hp2"))
    mb = MessageBoard("super cool chat")
    session.add(mb)
    await session.flush()
    session.add(Clan("epic clan", mb.bid))
    await session.commit()
    """
    m_token = MessageToken(
        sender_id="d0dd0cb0-c8ac-42b7-9902-f8e3171838e1",
        message_board=1,
        body="test"
    )

    #await da.createMessage(m_token)

    a = await da.getMessagesAlliance("epic clan", 0, 1)
    b = await da.getMessagesAlliance("epic clan", 1, 2)
    #await da.addFriendship(1, 3)
    f = await da.getFriends(1)
    f2 = await da.getFriends(3)
    print(f)
    print(f2)

    await db.disconnect()

def test_messageboard() -> None:
    asyncio.run(setup_data())
    assert True

