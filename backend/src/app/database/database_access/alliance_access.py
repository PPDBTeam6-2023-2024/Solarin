from ..models.models import *
from ..database import AsyncSession


class AllianceAccess:
    """
    This class will manage the sql access for data related to information of an alliance
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createAlliance(self, alliance_name: str):
        """
        Create Alliance in the database

        :param: alliance_name: name of the alliance
        :return: nothing
        """

        mb = MessageBoard(chat_name=f"{alliance_name} clan chat")
        self.__session.add(mb)
        await self.__session.flush()
        self.__session.add(Alliance(name=alliance_name, message_board=mb.bid))

    async def setAlliance(self, user_id: int, alliance_name: str):
        """
        Add a user to an alliance

        :param: alliance_name: name of the alliance
        :param: user_id: id of the user we want to add to the alliance
        :return: nothing
        """
        add_ally = update(User)
        add_ally = add_ally.values({"alliance": alliance_name})
        add_ally = add_ally.where(User.id == user_id)

        await self.__session.execute(add_ally)

    async def getAllianceMembers(self, alliance_name: str):
        """
        retrieve all the members of an alliance

        :param: alliance_name: name of the alliance
        :return: all the members of the alliance
        """
        search_members = Select(User).where(User.alliance == alliance_name)
        results = await self.__session.execute(search_members)

        return results.all()
