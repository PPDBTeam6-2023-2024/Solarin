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

    async def sendAllianceRequest(self, user_id: int, alliance_name: str):
        """
        add an alliance request to join an alliance
        :param: user_id: id of the user
        :param: alliance_name: name of the alliance
        """

        """
        delete old request if exists
        """
        await self.__removeAllianceRequest(user_id)

        ar = AllianceRequest(user_id=user_id, alliance_name=alliance_name)
        self.__session.add(ar)
        await self.__session.flush()

    async def acceptAllianceRequest(self, user_id: int, alliance_name: str):
        """
        accept an alliance request
        :param: user_id: id of the user
        :param: alliance_name: name of the alliance
        """

        await self.setAlliance(user_id, alliance_name)

    async def rejectAllianceRequest(self, user_id: int):
        """
        refuse alliance request
        :param: user_id: id of the user
        """
        await self.__removeAllianceRequest(user_id)

    async def __removeAllianceRequest(self, user_id: int):
        """
        remove the alliance entry of the given user
        :param: user_id: id of the user
        """
        dr = Delete(AllianceRequest).where(AllianceRequest.user_id == user_id)
        await self.__session.execute(dr)
        await self.__session.flush()


