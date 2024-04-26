from ..models import *
from ..database import AsyncSession
from ..exceptions.not_found_exception import NotFoundException
from ..exceptions.invalid_action_exception import InvalidActionException

from .database_acess import DatabaseAccess

def get_friends_query_sym(user_id: int):
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


class UserAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of a User
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_user(self, username: str, email: str, hashed_password: str):
        """
        Create a new user in the database
        :param: username: username of the new user
        :param: email: email of the new user
        :param: hashed_password: hashed password the user will use to login
        :return: user_id of the user that is just created
        """

        user = User(email=email, username=username, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        user_id = user.id

        """
        make has resource entry
        """
        await self.__set_has_resource_entries(user_id)

        """
        set the user's political stance to neutral
        """
        await self.initialize_politics(user_id)

        await self.session.commit()

        return user_id

    async def get_faction_name(self, user_id: str):
        """
        Get the faction corresponding to the given user id

        :param: user_id: id of user whose faction name we want to retrieve
        :return: faction name
        """

        find_faction_query = select(User.faction_name).where(User.id == user_id)
        results = await self.session.execute(find_faction_query)
        results = results.scalar_one_or_none()

        """
        exception in case the user_id is invalid
        """
        if results is None:
            raise NotFoundException(user_id, "User faction name")
        return results

    async def get_user_id_email(self, email: str):
        """
        Get the User id corresponding to the given email

        :param: email: the email of the user whose id we want to retrieve
        :return: user id
        """

        find_uuid = select(User.id).where(User.email == email)
        results = await self.session.execute(find_uuid)
        results = results.scalar_one_or_none()

        """
        exception in case the email has no corresponding account
        """
        if results is None:
            raise NotFoundException(email, "User")

        return results

    async def get_user_id_username(self, username: str):
        """
        Get the User id corresponding to the given username

        :param: username: the username of the user whose id we want to retrieve
        :return: user id
        """

        find_uuid = select(User.id).where(User.username == username)
        results = await self.session.execute(find_uuid)
        results = results.scalar_one_or_none()

        """
        exception in case the email has no corresponding account
        """
        if results is None:
            raise NotFoundException(username, "User")

        return results

    async def get_friends(self, user_id: int):
        """
        returns the friends of the user_id
        This will be a symmetrical relation so if user 1 is friends with user 2,
        user 2 will also be friends with user 1

        :param: user_id: user whose friends we want
        :return: all the user its friends and message board
        """

        friends = get_friends_query_sym(user_id)
        result = await self.session.execute(friends)

        await self.session.flush()
        return result.all()

    async def add_friendship(self, user1_id: int, user2_id: int):
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
        self.session.add(mb)
        await self.session.flush()
        self.session.add(FriendsOf(user1_id=user1_id, user2_id=user2_id, message_board=mb.bid))

        await self.session.flush()

    async def send_friend_request(self, from_user: int, to_user: int):
        """
        store a new friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """

        """
        check if the users are already friends
        """
        sym_friends = get_friends_query_sym(from_user)
        check_friends = sym_friends.select().where(sym_friends.c.user_id == to_user)
        results = await self.session.execute(check_friends)
        results = results.first()
        if results is not None:
            raise InvalidActionException("Users are already friends")

        if from_user == to_user:
            raise InvalidActionException("I know you are lonely, but you cannot be friends with yourself")

        """
        if friend request is already send we return that information
        """
        results = await self.session.execute(Select(FriendRequest).
                                               where((FriendRequest.from_user_id == from_user) & (FriendRequest.to_user_id == to_user)))

        results = results.first()
        if results is not None:
            raise InvalidActionException("Friend request has already been send")

        fq = FriendRequest(from_user_id= from_user, to_user_id=to_user)
        self.session.add(fq)

        await self.session.flush()

    async def accept_friend_request(self, from_user: int, to_user: int):
        """
        when a friend request is accepted, these users become friends
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """

        await self.__remove_friend_request(from_user, to_user)
        await self.add_friendship(from_user, to_user)

    async def reject_friend_request(self, from_user: int, to_user: int):
        """
        remove friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """
        await self.__remove_friend_request(from_user, to_user)

    async def __remove_friend_request(self, from_user: int, to_user: int):
        """
        remove friend request
        :param: from_user: id of the user that sends the friend request
        :param: to_user: id of the user that receives
        """
        delete_request = delete(FriendRequest).where(
            (from_user == FriendRequest.from_user_id) & (to_user == FriendRequest.to_user_id))
        await self.session.execute(delete_request)

        await self.session.flush()

    async def get_friend_requests(self, user_id: int):
        """
        We want to retrieve all the friend requests of a user
        :param: user_id: id of the user whose friend requests we want to retrieve
        :return: list of users whose sended a friend request
        """
        friend_requests = Select(User).\
            join(FriendRequest, FriendRequest.from_user_id == User.id).where(FriendRequest.to_user_id == user_id)
        results = await self.session.execute(friend_requests)
        results = results.scalars().all()
        return results

    async def __set_has_resource_entries(self, user_id: int):
        """
        make a table entry for each resource for the given user in hasResource
        """
        resources = await self.session.execute(Select(ResourceType.name))
        resources = resources.scalars().all()
        for resource in resources:
            self.session.add(HasResources(owner_id=user_id, resource_type=resource))
        await self.session.flush()

    async def get_alliance(self, user_id: int):
        """
        Get the alliance corresponding to the user
        param: user_id: id of the user whose alliance we want

        return: name of alliance (string or none in case the user is not in an alliance)
        """

        get_alliance = Select(User.alliance).where(User.id == user_id)
        result = await self.session.execute(get_alliance)
        result = result.scalar_one_or_none()
        return result

    async def initialize_politics(self, new_user_id: int):
        """
        initialize the value for each political stance to 0
        :param new_user_id: the id of the user we are creating
        """
        query = Select(PoliticalStance).where(PoliticalStance.user_id == new_user_id)
        existing_entry = await self.session.execute(query)
        if existing_entry.first() is not None:
            # there already is an entry for some reason
            update_query = update(PoliticalStance).where(PoliticalStance.user_id == new_user_id).values(anarchism=0, authoritarian=0, democratic=0, corporate_state=0, theocracy=0, technocracy=0)
            await self.session.execute(update_query)
        else:
            # create a new entry
            insert_query = insert(PoliticalStance).values(user_id=new_user_id, anarchism=0, authoritarian=0, democratic=0, corporate_state=0, theocracy=0, technocracy=0)
            await self.session.execute(insert_query)

    async def get_politics(self, user_id: int):
        """
        get the political values of a user
        :param user_id: the user in question
        :return: a values between 0 and 1 for each type of society
        """

        get_query = Select(PoliticalStance).where(PoliticalStance.user_id == user_id)
        result = await self.session.execute(get_query)
        result = result.scalars().first()
        return result

    async def update_politics(self, user_id: int, stance: dict):
        """
        Overwrite the current database values with the new values
        :param user_id: the user whose values are being changed
        :param stance: the new values
        """
        if not stance:
            raise ValueError("No stance provided for update.")

        valid_updates = {key: value for key, value in stance.items() if key in ["anarchism", "authoritarian", "democratic", "corporate_state", "theocracy", "technocracy"] and value is not None}

        if not valid_updates:
            raise ValueError("No valid fields provided for update.")

        update_query = update(PoliticalStance).where(PoliticalStance.user_id == user_id).values(**valid_updates)
        await self.session.execute(update_query)
        await self.session.commit()
