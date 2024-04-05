from ..models.models import *
from ..database import AsyncSession


def getFriendsQuerySym(user_id: int):
    """
    Function to get the SQL expression that access all retrieves all friends of the given user_id
    :param: user_id: user whose friends we want
    :return: (friend_id, message_board_id): message_board_id of the message DM message board
    """
    friends_1 = Select(FriendsOf.user1_id.label('user_id'), FriendsOf.message_board).where(
        user_id == FriendsOf.user2_id)
    friends_2 = Select(FriendsOf.user2_id.label('user_id'), FriendsOf.message_board).where(
        user_id == FriendsOf.user1_id)
    friends: CompoundSelect = friends_1.union(friends_2)

    return friends


class UserAccess:
    """
    This class will manage the sql access for data related to information of a User
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def createUser(self, username: str, email: str, hashed_password: str):
        """
        Create a new user in the database
        :param: username: username of the new user
        :param: email: email of the new user
        :param: hashed_password: hashed password the user will use to login
        :return: user_id of the user that is just created
        """

        user = User(email=email, username=username, hashed_password=hashed_password)
        self.__session.add(user)
        await self.__session.flush()
        user_id = user.id

        """
        make has resource entry
        """
        await self.__setHasResourceEntries(user_id)

        return user_id

    async def getFactionName(self, user_id: str):
        """
        Get the faction corresponding to the given user id

        :param: user_id: id of user whose faction name we want to retrieve
        :return: faction name
        """

        find_faction_query = select(User.faction_name).where(User.id == user_id)
        results = await self.__session.execute(find_faction_query)
        results = results.first()

        """
        exception in case the user_id is invalid
        """
        if results is None:
            raise Exception("SQL UserAccess --> getFactionName: user_id is invalid")
        return results[0]
    async def getUsernameUserId(self, user_id: str):
        """
        Get the username corresponding to given user id

        :param: user_id: the user id
        :return: the username
        """
        find_username = select(User.username).where(User.id == user_id)
        results = await self.__session.execute(find_username)
        results = results.first()
        if results is None:
            raise Exception("SQL UserAccess --> getUsernameUserId: no id corresponds to username")


    async def getUserIdEmail(self, email: str):
        """
        Get the User id corresponding to the given email

        :param: email: the email of the user whose id we want to retrieve
        :return: user id
        """

        find_uuid = select(User.id).where(User.email == email)
        results = await self.__session.execute(find_uuid)
        results = results.first()

        """
        exception in case the email has no corresponding account
        """
        if results is None:
            raise Exception("SQL UserAccess --> getUserIdEmail: no id corresponds to the email")

        return results[0]

    async def getUserIdUsername(self, username: str):
        """
        Get the User id corresponding to the given username

        :param: username: the username of the user whose id we want to retrieve
        :return: user id
        """

        find_uuid = select(User.id).where(User.username == username)
        results = await self.__session.execute(find_uuid)
        results = results.first()

        """
        exception in case the email has no corresponding account
        """
        if results is None:
            raise Exception("SQL UserAccess --> getUserIdUsername: no id corresponds to the username")

        return results[0]

    async def getFriends(self, user_id: int):
        """
        returns the friends of the user_id
        This will be a symmetrical relation so if user 1 is friends with user 2,
        user 2 will also be friends with user 1

        :param: user_id: user whose friends we want
        :return: all the user its friends and message board
        """

        friends = getFriendsQuerySym(user_id)
        result = await self.__session.execute(friends)

        await self.__session.flush()
        return result.all()

    async def addFriendship(self, user1_id: int, user2_id: int):
        """
        Declare a friendship between 2 users

        :param: user1_id: user id of the user who want to become a friend with the other one
        :param: user2_id: user id of the user who want to become a friend with the other one
        :return: nothing
        """

        """
        first create a messageboard that will be used for DM messages between the users
        """
        mb = MessageBoard(chat_name=f"DM {user1_id}-{user2_id}")
        self.__session.add(mb)
        await self.__session.flush()
        self.__session.add(FriendsOf(user1_id=user1_id, user2_id=user2_id, message_board=mb.bid))

        await self.__session.flush()

    async def sendFriendRequest(self, from_user: int, to_user: int):
        """
        store a new friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """

        """
        check if the users are already friends
        """
        sym_friends = getFriendsQuerySym(from_user)
        check_friends = sym_friends.select().where(sym_friends.c.user_id == to_user)
        results = await self.__session.execute(check_friends)
        results = results.first()
        if results is not None:
            raise Exception("Users are already friends")

        if from_user == to_user:
            raise Exception("I know you are lonely, but you cannot be friends with yourself")

        """
        if friend request is already send we return that information
        """
        results = await self.__session.execute(Select(FriendRequest).
                                               where((FriendRequest.from_user_id == from_user) & (FriendRequest.to_user_id == to_user)))

        results = results.first()
        if results is not None:
            raise Exception("Friend request has already been send")

        fq = FriendRequest(from_user_id= from_user, to_user_id=to_user)
        self.__session.add(fq)

        await self.__session.flush()

    async def acceptFriendRequest(self, from_user: int, to_user: int):
        """
        when a friend request is accepted, these users become friends
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """

        await self.__removeFriendRequest(from_user, to_user)
        await self.addFriendship(from_user, to_user)

    async def rejectFriendRequest(self, from_user: int, to_user: int):
        """
        remove friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """
        await self.__removeFriendRequest(from_user, to_user)

    async def __removeFriendRequest(self, from_user: int, to_user: int):
        """
        remove friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """
        delete_request = delete(FriendRequest).where(
            (from_user == FriendRequest.from_user_id) & (to_user == FriendRequest.to_user_id))
        await self.__session.execute(delete_request)

        await self.__session.flush()

    async def getFriendRequests(self, user_id: int):
        """
        We want to retrieve all the friend requests of a user
        :param: user_id: id of the user whose friend requests we want to retrieve
        :return: list of users whose sended a friend request
        """
        friend_requests = Select(User).join(FriendRequest, FriendRequest.from_user_id == User.id).where(FriendRequest.to_user_id == user_id)
        results = await self.__session.execute(friend_requests)
        results = results.all()
        return results

    async def __setHasResourceEntries(self, user_id: int):
        """
        make a table entry for each resource for the given user in hasResource
        """
        resources = await self.__session.execute(Select(ResourceType.name))
        resources = resources.all()
        for resource in resources:
            self.__session.add(HasResources(owner_id=user_id, resource_type=resource[0]))
        await self.__session.flush()