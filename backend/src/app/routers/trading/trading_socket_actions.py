import json
from ..core.connection_pool import ConnectionPool
from fastapi.websockets import WebSocket
from ...database.database_access.data_access import DataAccess
from fastapi.encoders import jsonable_encoder


class TradingSocketActions:
    """
    This class gives structure to the socket action methods
    """

    def __init__(self, user_id: int, alliance_name: str, data_access: DataAccess,
                 connection_pool: ConnectionPool, websocket: WebSocket):
        """
        The provided parameters are parameters that stay the same for the entire lifetime of this Object
        """

        self.user_id = user_id
        self.alliance_name = alliance_name
        self.data_access = data_access
        self.connection_pool = connection_pool
        self.websocket = websocket

    async def get_trades(self):
        """
        Get the currently pending trades within an alliance
        """
        trades = await self.data_access.TradeAccess.get_other_trade_offers(self.user_id)
        trades = [t.toSchema() for t in trades]

        own_offers = await self.data_access.TradeAccess.get_own_trade_offers(self.user_id)
        own_offers = [t.toSchema() for t in own_offers]

        await self.websocket.send_json({"trades": jsonable_encoder(trades), "action": "show_trades",
                                        "own_offers": jsonable_encoder(own_offers)})

    async def accept_trade(self, data: json):
        """
        accept a trade
        """
        await self.data_access.TradeAccess.accept_offer(self.user_id, data["offer_id"])
        await self.data_access.commit()

        """
        Update the trade information for everyone
        """
        await self.get_trades()

    async def cancel_trade(self, data: json):
        """
        cancel a trade offer
        """
        await self.data_access.TradeAccess.cancel_offer(self.user_id, data["offer_id"])
        await self.data_access.commit()

        """
        Update the trade information for everyone
        """
        await self.get_trades()

    async def create_trade(self, data: json):
        """
        create a trade offer
        """
        await self.data_access.TradeAccess.create_trade_offer(self.user_id, data["gives"], data["receives"])
        await self.data_access.commit()

        """
        Update the trade information for everyone
        """
        await self.get_trades()
