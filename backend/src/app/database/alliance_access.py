from .models import *
from .database import db, AsyncSession


class AllianceAccess:
    """
    This class will manage the sql access for data related to information of an alliance
    """
    def __init__(self, session):
        self.__session = session

    async def createAlliance(self, clan_name: str):
        """
        Create Alliance in the database
        """

        mb = MessageBoard(chat_name=f"{clan_name} clan chat")
        self.__session.add(mb)
        await self.__session.flush()
        self.__session.add(Alliance(name=clan_name, message_board=mb.bid))

    async def getMessagesAlliance(self, alliance_name: str, offset: int, amount: int):
        """
        Ask for an amount of messages written by this clan
        """

        """
        Select all the messages that have the message board corresponding to the alliance name
        """

        search_messages = Select(Message).\
            join(MessageBoard, Message.message_board == MessageBoard.bid).\
            join(Alliance, Alliance.message_board == MessageBoard.bid).where(Alliance.name == alliance_name).offset(offset).limit(amount)
        results = await self.__session.execute(search_messages)

        return results.unique().all()

    async def setAlliance(self, user_id: int, alliance_name: str):
        add_ally = update(User)
        add_ally = add_ally.values({"alliance": alliance_name})
        add_ally = add_ally.where(User.id == user_id)

        await self.__session.execute(add_ally)

    async def getAllianceMessageBoard(self, alliance_name: str):
        search_message_board = Select(Alliance.message_board).where(Alliance.name == alliance_name)
        results = await self.__session.execute(search_message_board)

        return results.first()[0]

    async def getAllianceMembers(self, alliance_name: str):
        search_members = Select(User).where(User.alliance == alliance_name)
        results = await self.__session.execute(search_members)

        return results.all()

