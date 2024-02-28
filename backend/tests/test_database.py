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

    t_index = 12
    uuid = await da.createUser(f"t{t_index}@gmail", f"usernamet{t_index}", f"hpt{t_index}")
    a = await da.getFactionName(uuid)
    print(uuid, "a", a)

    """
    session.add(User("t1@gmail", "username", "hp"))
    session.add(User("t2@gmail", "username2", "hp2"))
    mb = MessageBoard("super cool chat")
    session.add(mb)
    await session.flush()
    session.add(Clan("epic clan", mb.bid))
    await session.commit()
    """

    await db.disconnect()

def test_messageboard() -> None:
    asyncio.run(setup_data())
    assert True

