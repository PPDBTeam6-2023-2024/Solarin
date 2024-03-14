from fastapi import APIRouter, WebSocket, Depends, Query
from fastapi.websockets import WebSocketDisconnect
from typing import Annotated, Tuple, List

from .connection_manager import ConnectionManager, ConnectionPool
from ..authentication.router import get_my_id
from .schemas import *
from ...database.database import get_db, AsyncSession
from ...database.database_access.data_access import DataAccess

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = ConnectionManager()


async def handle_messaging(
        user_id: int,
        board_id: int,
        connection_pool: ConnectionPool,
        websocket: WebSocket,
        db: AsyncSession
):
    # TODO: enter message
    await connection_pool.broadcast({

    })

    try:
        while True:
            data = await websocket.receive_json()
            await connection_pool.broadcast(data)  # broadcast data to everyone

            if data["type"] == MessageType.CHAT:
                chat = Chat(**data)
                # TODO: persist chat to database

    except WebSocketDisconnect:
        manager.disconnect_board(board_id=board_id, websocket=websocket)

    # TODO: exit message
    if not connection_pool.empty():
        await connection_pool.broadcast({

        })


@router.websocket("/dm/{board_id}")
async def websocket_endpoint(
        user_id: Annotated[int, Depends(get_my_id)],
        websocket: WebSocket,
        board_id: int,
        db: AsyncSession = Depends(get_db)
):
    can_access = True  # TODO: CHECK IF THIS USER CAN ACCESS THIS BOARD CHAT OF FRIEND
    if not can_access:
        await websocket.close()
        return

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
    can_access = True  # TODO: CHECK IF THIS USER CAN ACCESS THIS BOARD CHAT OF ALLIANCE
    if not can_access:
        await websocket.close()
        return

    connection_pool = await manager.connect_board(board_id=board_id, websocket=websocket)
    await handle_messaging(
        user_id=user_id,
        board_id=board_id,
        connection_pool=connection_pool,
        websocket=websocket,
        db=db
    )


@router.get("/all/{board_id}")
async def get_messages(
        user_id: Annotated[int, Depends(get_my_id)],
        board_id: int,
        offset=Query(0),
        limit=Query(),
        db=Depends(get_db)
) -> list[MessageOut]:
    # TODO: FETCH MESSAGE HISTORY
    return


@router.get("/dm_overview")
async def dm_overview(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

) -> List[Tuple[str, MessageOut]]:
    """
    Get information of the last 5 DM's between the user and other friends
    The Information we want: The user we DM with, the last message send between them
    """

    data_access = DataAccess(db)
    data = await data_access.MessageAccess.getFriendMessageOverview(user_id, 20)

    """
    transform data to web format
    """
    output_list: List[Tuple[str, MessageOut]] = []
    for d in data:
        output_list.append((d[0], d[1].toMessageOut(d[2])))

    return output_list
