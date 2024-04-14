from sqlalchemy.orm import aliased

from ..models import *
from ..database import AsyncSession


class AllianceAccess:
    """
    This class will manage the sql access for data related to information of an alliance
    """
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_alliance(self, alliance_name: str):
        """
        Create Alliance in the database

        :param: alliance_name: name of the alliance
        :return: nothing
        """

        """
        Create a message board for the alliance
        """
        mb = MessageBoard(chat_name=f"{alliance_name} clan chat")
        self.__session.add(mb)
        await self.__session.flush()

        self.__session.add(Alliance(name=alliance_name, message_board=mb.bid))

    async def set_alliance(self, user_id: int, alliance_name: str):
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

    async def get_alliance_members(self, alliance_name: str):
        """
        retrieve all the members of an alliance

        :param: alliance_name: name of the alliance
        :return: all the members of the alliance
        """
        search_members = Select(User).where(User.alliance == alliance_name)
        results = await self.__session.execute(search_members)

        return results.scalars().all()

    async def send_alliance_request(self, user_id: int, alliance_name: str):
        """
        add an alliance request to join an alliance,
        This is an alliance request from the user to join the provided alliance
        :param: user_id: id of the user
        :param: alliance_name: name of the alliance
        """

        """
        delete old request if exists
        """
        await self.__remove_alliance_request(user_id)

        ar = AllianceRequest(user_id=user_id, alliance_name=alliance_name)
        self.__session.add(ar)
        await self.__session.flush()

    async def accept_alliance_request(self, user_id: int, alliance_name: str):
        """
        Accept an alliance request
        The user who sent the request will be added to the alliance
        :param: user_id: id of the user
        :param: alliance_name: name of the alliance
        """

        await self.__remove_alliance_request(user_id)
        await self.set_alliance(user_id, alliance_name)

    async def reject_alliance_request(self, user_id: int):
        """
        refuse alliance request
        :param: user_id: id of the user
        """
        await self.__remove_alliance_request(user_id)

    async def __remove_alliance_request(self, user_id: int):
        """
        remove the alliance request entry of the given user
        :param: user_id: id of the user
        """
        dr = Delete(AllianceRequest).where(AllianceRequest.user_id == user_id)
        await self.__session.execute(dr)
        await self.__session.flush()

    async def alliance_exists(self, alliance_name: str):
        """
        check if an alliance exists
        :param: alliance_name: name of the alliance
        :return: bool, if alliance exists -> return true else -> return false
        """

        get_alliance = Select(Alliance).where(Alliance.name == alliance_name)
        results = await self.__session.execute(get_alliance)
        result = results.scalar_one_or_none()
        return result is not None

    async def get_alliance_requests(self, user_id: int):
        """
        We want to retrieve all the users requests to join the alliance

        We receive the user_id of the user who is part of the alliance, who requests the alliance requests
        to the alliance he/she is a part of.

        :param: user_id: id of the user who is a part of the alliance whose requests we want to retrieve
        :return: list of users whose sent an alliance join request
        """

        alliance_member = aliased(User, name='alliance_member')
        alliance_requests = Select(User).join(AllianceRequest, AllianceRequest.user_id == User.id).\
            join(alliance_member, alliance_member.alliance == AllianceRequest.alliance_name).\
            where(alliance_member.id == user_id)
        results = await self.__session.execute(alliance_requests)
        return results.scalars().all()

    async def get_alliance(self, user_id: int):
        """
        Get the alliance the user belongs to
        :param: user_id: id of the user whose friend requests we want to retrieve
        :return: alliance name
        """

        result = await self.__session.execute(Select(User.alliance).where(User.id == user_id))
        result = result.scalar_one_or_none()
        if result is None:
            return None

        return result
