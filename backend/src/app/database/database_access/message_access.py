from ..models.models import *
from ..database import AsyncSession
from .user_access import getFriendsQuerySym
from sqlalchemy.orm import aliased


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
        We will make sure to ask the messages starting from newest till oldest with regards to which messages we take
        The list of messages will be in chronological order

        :param: user1_id: id of user_1
        :param: user2_id: id of user_2
        :param: offset: the offset from where we want to start reading messages
        :param: amount: the amount of messages we want
        :return: a list of messages with a max length of 'amount'
        """

        f_sym = getFriendsQuerySym(user1_id)

        search_messages = Select(Message).\
            where(f_sym.select().c.user_id == user2_id, f_sym.select().c.message_board == Message.message_board).\
            order_by(desc(Message.create_date_time)).offset(offset).limit(amount)

        results = await self.__session.execute(search_messages)
        results = results.all()

        """
        query is sorted from newest till oldest, so we still need to put it in chronological order
        """
        results = list(reversed(results))
        return results

    async def getMessagesAlliance(self, alliance_name: str, offset: int, amount: int):
        """
        Ask for an amount of messages written by this clan
        We will make sure to ask the messages starting from newest till oldest

        :param: alliance: the name of the alliance whose messages we want to access
        :param: offset: the offset from where we want to start reading messages
        :param: amount: the amount of messages we want
        :return: a list of messages with a max length of 'amount'
        """

        """
        Select all the messages that have the message board corresponding to the alliance name
        """

        search_messages = Select(Message).\
            join(MessageBoard, Message.message_board == MessageBoard.bid).\
            join(Alliance, Alliance.message_board == MessageBoard.bid).where(Alliance.name == alliance_name).\
            order_by(desc(Message.create_date_time)).offset(offset).limit(amount)

        results = await self.__session.execute(search_messages)

        """
        query is sorted from newest till oldest, so we still need to put it in chronological order
        """
        results = results.unique().all()
        results = list(reversed(results))
        return results

    async def getAllianceMessageBoard(self, alliance_name: str):
        """
        Get the messageBoardId of an Alliance

        :param: alliance: the name of the alliance whose messages we want to access
        :return: id of the messageboard of the alliance
        """
        search_message_board = Select(Alliance.message_board).where(Alliance.name == alliance_name)
        results = await self.__session.execute(search_message_board)

        return results.first()[0]

    async def getPlayerMessageBoard(self, user1_id: int, user2_id: int):
        """
        Get the messageBoardId of an DM between 2 friends

        :param: user1_id: id of user_1
        :param: user2_id: id of user_2
        :return: id of the messageboard of the DM between the 2 users
        """
        sym_friends = getFriendsQuerySym(user1_id)

        dm_mb = sym_friends.select().where(sym_friends.c.user_id == user2_id)
        results = await self.__session.execute(dm_mb)
        results = results.first()[1]
        return results

    async def getFriendMessageOverview(self, user1_id: int, limit: int):
        """
        Get an overview of friends with the most recently send message in the DM between the friend and the given user
        This can be used to easily display an overview of a player his DM's

        :param: user1_id: id of user_1
        :param: limit amount of friend message tuples we want
        :return: a list of tuples: (friends username, MessageBoard, Message)
        """
        sym_friends = getFriendsQuerySym(user1_id)

        sym_friends = sym_friends.select()

        """
        get most recent message create time sent by each friend
        """
        most_recent_message = (select(sym_friends.c, func.max(Message.create_date_time).label("max")).select_from(sym_friends)).join(Message, Message.message_board == sym_friends.c.message_board).group_by(sym_friends.c)

        """
        get the tuple (friend_username, Message, message_sender_username)
        """
        message_sender = aliased(User, name='message_sender')

        message_overview = (select(User.username, Message, message_sender.username).select_from(most_recent_message))\
            .join(Message, (Message.message_board == most_recent_message.c.message_board)).where(most_recent_message.c.max == Message.create_date_time)\
            .order_by(desc(Message.create_date_time)).limit(limit).join(User, User.id == most_recent_message.c.user_id)\
            .join(message_sender, message_sender.id == Message.sender_id)

        results = await self.__session.execute(message_overview)

        results = results.unique().all()
        return results

    async def getMessages(self, message_board: int, offset: int, limit: int):
        """
        get all messages from a specific message board

        :param: message_board: id of messages
        :param: offset: offset from where we want to read: offset 50 means we ignore the last 50 messages send
        :param: limit: amount of messages we want to retrieve
        :return: a list of tuples: (Message, sender username)
        """
        search_messages = Select(Message, User.username).join(User, User.id == Message.sender_id).where(Message.message_board == message_board). \
            order_by(desc(Message.create_date_time)).offset(offset).limit(limit)

        results = await self.__session.execute(search_messages)

        """
        query is sorted from newest till oldest, so we still need to put it in chronological order
        """
        results = results.unique().all()
        results = list(reversed(results))
        return results

    async def getMessage(self, mid: int):
        """
        Get a specific message based on its message mid
        :param: mid: id of the message
        :return: a list of tuples: (Message, sender username)
        """
        search_message = Select(Message, User.username).join(User, User.id == Message.sender_id).where(Message.mid == mid)

        results = await self.__session.execute(search_message)

        """
        query is sorted from newest till oldest, so we still need to put it in chronological order
        """
        result = results.first()

        if results is None:
            raise Exception("MessageAccess: GetMessage: Message does not exist")

        return result

