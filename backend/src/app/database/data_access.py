from .database import db
from .models import *
from ..schemas import MessageToken


class DataAccess:
    def __init__(self, session):
        self.__session = session

    async def createUser(self, user_name: str, email: str, password: str):
        """
        Create a new user in the database
        Return: The uuid of the created User
        """

        user = User(email=email, username=user_name, hashed_password=password)
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

    async def createAlliance(self, clan_name: str):
        """
        Create Alliance in the database
        """

        mb = MessageBoard(f"{clan_name} clan chat")
        self.__session.add(mb)
        await self.__session.flush()
        self.__session.add(Alliance(clan_name, mb.bid))
        await self.__session.commit()

    async def createMessage(self, message_token: MessageToken):
        """
        Create a new message in the database
        """

        message = Message(message_token)
        self.__session.add(message)
        await self.__session.commit()

    async def getMessagesAlliance(self, alliance_name: str, offset: int, amount: int):
        """
        Ask for an amount of messages written by this clan
        """

        search_messages = Select(Message).\
            join(MessageBoard, Message.message_board == MessageBoard.bid).\
            join(Alliance, Alliance.name == alliance_name).offset(offset).limit(amount)

        results = await self.__session.execute(search_messages)

        return results.all()

    async def getFriends(self, user_id: int):
        """
        returns the friends of the user_id
        This will be a symmetrical relation so if user 1 is friends with user 2,
        user 2 will also be friends with user 1
        """

        friends_1 = Select(FriendsOf.user1_id.label('user_id')).where(user_id == FriendsOf.user2_id)
        friends_2 = Select(FriendsOf.user2_id.label('user_id')).where(user_id == FriendsOf.user1_id)
        friends: CompoundSelect = friends_1.union(friends_2)
        result = await self.__session.execute(friends)

        await self.__session.commit()
        return result.all()

    async def addFriendship(self, user1_id: int, user2_id: int):
        """
        Declare a friendship between 2 users
        """

        mb = MessageBoard(chat_name=f"DM {user1_id}-{user2_id}")
        self.__session.add(mb)
        await self.__session.flush()

        self.__session.add(FriendsOf(user1_id=user1_id, user2_id=user2_id, message_board=mb.bid))

        await self.__session.commit()
