from .models import *
from .database import db, AsyncSession


class MessageAccess:
    """
    This class will manage the sql access for data related to information of messages
    """
    def __init__(self, session):
        self.__session = session

    async def createMessage(self, message_token: MessageToken):
        """
        Create a new message in the database
        """

        message = Message.fromMessageToken(message_token)
        self.__session.add(message)

        await self.__session.flush()
        mid = message.mid
        return mid

    async def getMessagesPlayer(self, user1_id: int, user2_id: int, offset: int, amount: int):
        """
        requests the messages exchanged between the 2 users
        """
        f_sym = self.getFriendsQuerySym(user1_id)
        search_messages = Select(Message). \
            join(MessageBoard, Message.message_board == MessageBoard.bid). \
            join(f_sym, f_sym.message_board == MessageBoard.bid)\
            .where(user2_id == f_sym.user_id).offset(offset).limit(amount)

        results = await self.__session.execute(search_messages)

        return results.all()