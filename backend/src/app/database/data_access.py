from .database import db
from .models import *


class DataAccess:
    def __init__(self, session):
        self.__session = session

    async def createUser(self, user_name: str, email: str, password: str):
        """
        Create a new user in the database

        Return: The uuid of the created User
        """
        user = User(user_name, email, password)
        self.__session.add(user)
        await self.__session.flush()
        user_id = user.id
        await self.__session.commit()
        return user_id

    async def getFactionName(self, uuid: str):
        """
        Get the faction corresponding to the given uuid
        """
        find_faction_query = select(User.faction_name).where(User.id == uuid)
        results = await self.__session.execute(find_faction_query)
        return results.first()[0]

    async def getUserIdEmail(self, email: str):
        """
        Get the User uuid corresponding to the given email
        """
        find_uuid = select(User.id).where(User.email == email)
        results = await self.__session.execute(find_uuid)
        return results.first()[0]

    async def createClan(self, clan_name: str):
        mb = MessageBoard(f"{clan_name} clan chat")
        self.__session.add(mb)
        await self.__session.flush()
        self.__session.add(Clan(clan_name, mb.bid))
        await self.__session.commit()
