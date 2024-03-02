from .models import *
from .database import AsyncSession


class MessageAccess:
    """
    This class will manage the sql access for data related to information of messages
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createMessage(self, message_token: MessageToken):
        """
        Create a new message in the database

        :param: message_token: a schema that contains all the needed information in regard to a message
        :return: the message id of the message that is just created
        """

        message = Message.fromMessageToken(message_token)
        self.__session.add(message)

        await self.__session.flush()
        mid = message.mid
        return mid

    async def getMessagesPlayer(self, user1_id: int, user2_id: int, offset: int, amount: int):
        """
        requests the messages exchanged between the 2 users

        :param: user1_id: id of user_1
        :param: user2_id: id of user_2
        :param: offset: the offset from where we want to start reading messages
        :param: amount: the amount of messages we want
        :return: a list of messages with a max length of 'amount'
        """
        f_sym = self.getFriendsQuerySym(user1_id)
        search_messages = Select(Message). \
            join(MessageBoard, Message.message_board == MessageBoard.bid). \
            join(f_sym, f_sym.message_board == MessageBoard.bid)\
            .where(user2_id == f_sym.user_id).offset(offset).limit(amount).order_by(desc(Message.mid))

        results = await self.__session.execute(search_messages)
        results = results.all()
        results = list(reversed(results))
        return results

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

    async def getAllianceMessageBoard(self, alliance_name: str):
        """
        Get the messageBoardId of an Alliance
        """
        search_message_board = Select(Alliance.message_board).where(Alliance.name == alliance_name)
        results = await self.__session.execute(search_message_board)

        return results.first()[0]
