from fastapi import APIRouter, WebSocket, Depends, Query
from fastapi.websockets import WebSocketDisconnect
from typing import Annotated

from .connection_manager import ConnectionManager, ConnectionPool
from ..authentication.router import get_my_id
from .schemas import *
from ...database.database import get_db, AsyncSession

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = ConnectionManager()


async def handle_messaging(
        user_id: int,
        board_id: int,
        connection_pool: ConnectionPool,
        websocket: WebSocket,
        db: AsyncSession
):
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == MessageType.CHAT:
                chat = Chat(**data)
                # TODO: persist chat data
            await connection_pool.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect_board(board_id=board_id, websocket=websocket)
        if not connection_pool.empty():
            # TODO: leave message
            await connection_pool.broadcast({

            })


@router.websocket("/dm/{board_id}")
async def websocket_endpoint(
        user_id: Annotated[int, Depends(get_my_id)],
        websocket: WebSocket,
        board_id: int,
        db: AsyncSession = Depends(get_db)
):
    # TODO: CHECK IF THIS USER CAN ACCESS THIS BOARD CHAT OF FRIEND
    connection_pool = await manager.connect_board(board_id=board_id, websocket=websocket)
    await handle_messaging(
        user_id=user_id,
        board_id=board_id,
        connection_pool=connection_pool,
        websocket=websocket,
        db=db
    )


@router.websocket("/gc/{board_id}")
async def websocket_endpoint(
        user_id: Annotated[int, Depends(get_my_id)],
        websocket: WebSocket,
        board_id: int,
        db: AsyncSession = Depends(get_db)
):
    # TODO: CHECK IF THIS USER CAN ACCESS THIS BOARD CHAT OF ALLIANCE
    connection_pool = await manager.connect_board(board_id=board_id, websocket=websocket)
    await handle_messaging(
        user_id=user_id,
        board_id=board_id,
        connection_pool=connection_pool,
        websocket=websocket,
        db=db
    )


@router.get("/{board_id}")
async def get_messages(
        user_id: Annotated[int, Depends(get_my_id)],
        board_id: int,
        offset=Query(0),
        limit=Query(),
        db=Depends(get_db)
) -> list[MessageOut]:
    # TODO: FETCH MESSAGE HISTORY
    return

