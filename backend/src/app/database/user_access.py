from .models import *
from .database import AsyncSession


class UserAccess:
    """
    This class will manage the sql access for data related to information of a User
    """
    def __init__(self, session: AsyncSession):
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

    async def getFriends(self, user_id: int):
        """
        returns the friends of the user_id
        This will be a symmetrical relation so if user 1 is friends with user 2,
        user 2 will also be friends with user 1
        """

        friends = self.getFriendsQuerySym(user_id)
        result = await self.__session.execute(friends)

        await self.__session.flush()
        return result.all()

    def getFriendsQuerySym(self, user_id: int):
        friends_1 = Select(FriendsOf.user1_id.label('user_id'), FriendsOf.message_board).where(user_id == FriendsOf.user2_id)
        friends_2 = Select(FriendsOf.user2_id.label('user_id'), FriendsOf.message_board).where(user_id == FriendsOf.user1_id)
        friends: CompoundSelect = friends_1.union(friends_2)

        return friends

    async def addFriendship(self, user1_id: int, user2_id: int):
        """
        Declare a friendship between 2 users
        """

        mb = MessageBoard(chat_name=f"DM {user1_id}-{user2_id}")
        self.__session.add(mb)
        await self.__session.flush()

        self.__session.add(FriendsOf(user1_id=user1_id, user2_id=user2_id, message_board=mb.bid))
