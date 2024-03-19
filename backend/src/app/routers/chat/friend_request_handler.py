from .request_handler import RequestHandler
from ..authentication.schemas import MessageToken


class FriendRequestHandler(RequestHandler):
    """
    This class contains methods to handle certain actions related to friend requests
    """

    def __verify_data(self):
        """
        verify the integrity of the data
        required format:
        json having the following structure:
        {
        "type": string
        if type == "add":
            "username": str
        if type == "review":
            "friend_id": int
            "accepted": bool
        }
        """

        if "type" not in self.data:
            raise Exception("Integrity Error: 'type' not defined")

        if self.data["type"] == "add":
            if "username" not in self.data:
                raise Exception("Integrity Error: 'username' not defined")

        if self.data["type"] == "review":
            if "friend_id" not in self.data:
                raise Exception("Integrity Error: 'friend_id' not defined")

            if "accepted" not in self.data:
                raise Exception("Integrity Error: 'accepted' not defined")

    async def handle(self, user_id):
        """
        do the required action
        """
        result = (False, "Nothing has been done")

        try:
            if self.data["type"] == "add":
                result = await self.__handle_add(user_id)

            if self.data["type"] == "review":
                result = await self.__handle_review(user_id)
        except Exception as e:
            result = (False, str(e))

        return result

    async def __handle_add(self, user_id):
        """
        add a friend request to the friend requests table
        the friend request will be send to the given username, coming from user_id

        :return: tuple(bool, str): -> (success, message)
        """

        to_user_id = await self.data_access.UserAccess.getUserIdUsername(self.data["username"])
        await self.data_access.UserAccess.sendFriendRequest(user_id, to_user_id)
        await self.data_access.commit()

        return True, "Friend request has been send"

    async def __handle_review(self, user_id):
        """
        this function will review an friend request and check if it is accepted or not

        :return: tuple(bool, str): -> (success, message)
        """

        if self.data["accepted"]:
            """
            in case the friend request will be accepted
            """
            await self.data_access.UserAccess.acceptFriendRequest(self.data["friend_id"], user_id)

            """
            send a default message indicating the friend request ahs been accepted
            """
            message_board = await self.data_access.MessageAccess.getPlayerMessageBoard(user_id, self.data["friend_id"])

            await self.data_access.MessageAccess.createMessage(MessageToken(sender_id=user_id, message_board=message_board,
                                                                       body="Friend request has been accepted"))
        else:
            """
            in case the friend request will not be accepted
            """
            await self.data_access.UserAccess.rejectFriendRequest(self.data["friend_id"], user_id)

        await self.data_access.commit()

        return True, f"Friend request has been {(lambda accepted: 'accepted' if accepted else 'rejected')(self.data['accepted'])}"
