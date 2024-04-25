from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce
from typing import Union, Annotated
from fastapi.websockets import WebSocket, WebSocketDisconnect
from .connection_manager import ConnectionManager
from ....app.routers.authentication.router import get_my_id, get_db
from ....app.database.database_access.data_access import DataAccess
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

            pass

    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)


