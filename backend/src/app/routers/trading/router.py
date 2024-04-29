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
from .trading_socket_actions import TradingSocketActions
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

    trade_actions = TradingSocketActions(user_id, user_alliance, data_access, connection_pool, websocket)

    """
    Map translation function to 'function ptr' of function corresponding to the action
    """
    action_map = {"get_trades": lambda d: trade_actions.get_trades(),
                  "accept_trade": trade_actions.accept_trade,
                  "cancel_trade": trade_actions.cancel_trade,
                  "create_trade": trade_actions.create_trade
                  }

    try:
        while True:
            data = await websocket.receive_json()

            action_func = action_map[data["type"]]

            await action_func(data)

    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)


