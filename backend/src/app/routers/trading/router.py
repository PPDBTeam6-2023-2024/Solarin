from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce
from typing import Union, Annotated
from fastapi.websockets import WebSocket, WebSocketDisconnect
from .connection_manager import ConnectionManager
from ....app.routers.authentication.router import get_my_id, get_db
from ....app.database.database_access.data_access import DataAccess
from fastapi.encoders import jsonable_encoder
from .schemas import *

router = APIRouter(prefix="/trading")

manager = ConnectionManager()


@router.websocket("/ws")
async def planet_socket(
        websocket: WebSocket,
        db=Depends(get_db)
):
    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")
    user_id = get_my_id(auth_token)

    data_access = DataAccess(db)
    user_alliance = await data_access.AllianceAccess.get_alliance(user_id)
    connection_pool, new_conn = await manager.connect_trade_board(alliance_name=user_alliance, websocket=websocket,
                                                                  sub_protocol=auth_token)
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "get_trades":
                trades = await data_access.TradeAccess.get_other_trade_offers(user_id)
                trades = [t.toSchema() for t in trades]

                own_offers = await data_access.TradeAccess.get_own_trade_offers(user_id)
                own_offers = [t.toSchema() for t in own_offers]

                await websocket.send_json({"trades": jsonable_encoder(trades), "action": "show_trades",
                                           "own_offers": jsonable_encoder(own_offers)})
                continue
            elif data["type"] == "accept_trade":
                await data_access.TradeAccess.accept_offer(user_id, data["offer_id"])
                await data_access.commit()

            elif data["type"] == "cancel_trade":
                await data_access.TradeAccess.cancel_offer(user_id, data["offer_id"])
                await data_access.commit()
            elif data["type"] == "create_trade":
                await data_access.TradeAccess.create_trade_offer(user_id, data["gives"], data["receives"])
                await data_access.commit()

            trades = await data_access.TradeAccess.get_other_trade_offers(user_id)
            trades = [t.toSchema() for t in trades]

            own_offers = await data_access.TradeAccess.get_own_trade_offers(user_id)
            own_offers = [t.toSchema() for t in own_offers]

            await connection_pool.broadcast({"trades": jsonable_encoder(trades), "action": "show_trades",
                                             "own_offers": jsonable_encoder(own_offers)})

    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)


