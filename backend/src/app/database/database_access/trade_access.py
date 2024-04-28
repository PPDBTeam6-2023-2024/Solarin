from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from typing import List
from ..models import *
from .database_acess import DatabaseAccess
from .alliance_access import AllianceAccess
from .resource_access import ResourceAccess
from ..exceptions.invalid_action_exception import InvalidActionException
from ..exceptions.permission_exception import PermissionException


class TradeAccess(DatabaseAccess):
    """
    This class will manage the sql access for data related to information of an alliance
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_trade_offer(self, user_id: int,
                                 gives_resources: List[tuple[str, int]],
                                 receives_resources: List[tuple[str, int]]):
        """
        Make it possible for a user to place a trading offer
        :param:user_id: id of the user who makes the trade offer
        :param:gives_resources: list of tuples (resource, amount), indicating the resources the user is willing to give
        to the user who made the offer
        :param:receive_resources: list of tuples (resource, amount), indicating the resources the user is willing to
        receive from the user who made the offer

        """

        alliance_access = AllianceAccess(self.session)
        alliance_name = await alliance_access.get_alliance(user_id)
        if alliance_name is None:
            raise InvalidActionException("Trading offers can only be created when the user is part of an alliance")

        resource_access = ResourceAccess(self.session)
        """
        Check if the user ahs the resources it want to give
        """
        if not resource_access.has_resources(user_id, receives_resources):
            raise InvalidActionException("user does not have the resources it offers to give")

        """
        Remove the resources from the user account, and put it into the offer later on
        """
        for resource, amount in receives_resources:
            await resource_access.remove_resource(user_id, resource, amount)

        await self.session.flush()

        """
        Create the trading offer
        """
        trading_offer = TradeOffer(alliance_name=alliance_name, offer_owner=user_id)
        self.session.add(trading_offer)
        await self.flush()
        offer_id = trading_offer.id

        """
        Add the trading offer give field
        """
        for resource, amount in gives_resources:
            trading_give = TradeGives(offer_id=offer_id, resource_type=resource, amount=amount)
            self.session.add(trading_give)

        """
        Add the trading offer give field
        """
        for resource, amount in receives_resources:
            trading_give = TradeReceives(offer_id=offer_id, resource_type=resource, amount=amount)
            self.session.add(trading_give)

        await self.session.flush()

    async def get_own_trade_offers(self, user_id: int):
        """
        Retrieve all the trade offers made by the provided user

        :param: user_id: id of the user whose trade offers we want to retrieve
        return: list of trading offers owned by the user
        """

        get_offers = Select(TradeOffer).where(TradeOffer.offer_owner == user_id)

        offers = await self.session.execute(get_offers)
        offers = offers.scalars().unique().all()

        return offers

    async def get_other_trade_offers(self, user_id: int):
        """
        Retrieve all the trade offers not made by the provided user, but are offered to the alliance where the user is
        a part of

        :param: user_id: id of the user whose trade offers we want to retrieve
        return: list of trading offers offered within the alliance from other users
        """

        alliance_access = AllianceAccess(self.session)
        alliance_name = await alliance_access.get_alliance(user_id)
        if alliance_name is None:
            raise InvalidActionException("Trading offers can only be created when the user is part of an alliance")

        get_offers = Select(TradeOffer).\
            where((TradeOffer.alliance_name == alliance_name) & (TradeOffer.offer_owner != user_id))

        offers = await self.session.execute(get_offers)

        offers = offers.scalars().unique().all()

        return offers

    async def cancel_offer(self, user_id: int, offer_id: int):
        """
        Make it possible for users to cancel the trading offer

        :param: user_id: id of the user who wants to cancel this offer
        :param: offer_id: id of the offer we want to cancel
        """

        """
        Check if the provided user is the owner of the offer
        """
        get_offer = Select(TradeOffer).where(TradeOffer.id == offer_id)

        offer = await self.session.execute(get_offer)
        offer = offer.unique().scalar_one()

        """
        When the user is not the owner of the trading offer
        """
        if offer.offer_owner != user_id:
            raise PermissionException(user_id, "Cancel the trading offer of another user")

        """
        Refund the receive resources to the user
        """
        get_receive_resources = Select(TradeReceives).where(TradeReceives.offer_id == offer_id)
        receive_resources = await self.session.execute(get_receive_resources)
        receive_resources = receive_resources.scalars().unique().all()

        """
        Do the resource refunding
        """
        resource_access = ResourceAccess(self.session)
        for receive_resource in receive_resources:
            await resource_access.add_resource(user_id, receive_resource.resource_type, receive_resource.amount)

        """
        Remove the trade offer,
        The trade give and receive will also be removed because of cascading
        """
        delete_offer = delete(TradeOffer).where(TradeOffer.id == offer_id)
        await self.session.execute(delete_offer)

        await self.flush()

    async def accept_offer(self, user_id: int, offer_id: int):
        """
        Make it possible for users to accept a trading offer

        :param: user_id: id of the user who wants to cancel this offer
        :param: offer_id: id of the offer we want to cancel
        """

        get_offer = Select(TradeOffer).where(TradeOffer.id == offer_id)
        offer = await self.session.execute(get_offer)
        offer = offer.unique().scalar_one()
        offer_user_id = offer.offer_owner

        """
        Get the user its alliance
        """
        alliance_access = AllianceAccess(self.session)
        alliance_name = await alliance_access.get_alliance(user_id)

        if alliance_name is None or offer.alliance_name != alliance_name:
            raise InvalidActionException("Trading offers can only be accepted when the user is in the same alliance")

        """
        Check if the accepting user has the required offer resources
        """
        resource_access = ResourceAccess(self.session)

        give_resource_list = [(give_resource.resource_type, give_resource.amount)
                              for give_resource in offer.gives]

        can_give = await resource_access.has_resources(user_id, give_resource_list)
        if not can_give:
            raise InvalidActionException("user does not have the resources to accept this offer")

        """
        When the user is able to accept the offer
        """

        """
        Remove the resources from the 1 user and add it to the other 1
        """
        for give_resource in offer.gives:
            await resource_access.remove_resource(user_id, give_resource.resource_type, give_resource.amount)
            await resource_access.add_resource(offer_user_id, give_resource.resource_type, give_resource.amount)

        """
        Give the offer accept-er the 'receive resources'
        """

        for receive_resource in offer.receives:
            await resource_access.add_resource(user_id, receive_resource.resource_type, receive_resource.amount)

        delete_offer = delete(TradeOffer).where(TradeOffer.id == offer_id)
        await self.session.execute(delete_offer)

        await self.flush()
