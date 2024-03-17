from fastapi import APIRouter, WebSocket, Depends, Query, Request
from fastapi.websockets import WebSocketDisconnect
from typing import Annotated, Tuple, List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .connection_manager import ConnectionManager, ConnectionPool
from ..authentication.router import get_my_id
from .schemas import *
from ...database.database import get_db, AsyncSession
from ...database.database_access.data_access import DataAccess
import json

from ..authentication.schemas import MessageToken

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = ConnectionManager()

security = HTTPBearer()

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
        websocket: WebSocket, board_id: int, db: AsyncSession = Depends(get_db)
):

    auth_token = websocket.headers.get("Sec-WebSocket-Protocol")
    user_id = get_my_id(auth_token)
    await websocket.accept(subprotocol=auth_token)

    can_access = True  # TODO: CHECK IF THIS USER CAN ACCESS THIS BOARD CHAT OF FRIEND
    if not can_access:
        await websocket.close()
        return

    """send the first 30 messages to the user"""
    data_access = DataAccess(db)
    messages = await data_access.MessageAccess.getMessages(board_id, 0, 30)
    output_list: List[MessageOut] = []
    for d in messages:
        output_list.append(d[0].toMessageOut(d[1]).model_dump())

    await websocket.send_json({"type": "paging", "message": output_list})

    connection_pool = await manager.connect_board(board_id=board_id, websocket=websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "new message":
                """
                store message in database
                """
                mid = await data_access.MessageAccess.createMessage(MessageToken(sender_id=user_id,
                                                                     message_board=board_id,
                                                                     body=data["body"]))

                """
                obtain information about the just created message
                """
                message = await data_access.MessageAccess.getMessage(mid)
                message = message[0].toMessageOut(message[1])
                await data_access.commit()
                await connection_pool.broadcast({"type": "new message", "message": [message.model_dump()]})



    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)


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

) -> List[Tuple[str, MessageOut, int]]:
    """
    Get information of the last 5 DM's between the user and other friends
    The Information we want: The user we DM with, the last message send between them
    """

    data_access = DataAccess(db)
    data = await data_access.MessageAccess.getFriendMessageOverview(user_id, 20)

    """
    transform data to web format
    """
    output_list: List[Tuple[str, MessageOut, int]] = []
    for d in data:
        if d[1] is None:
            continue
        output_list.append((d[0], d[1].toMessageOut(d[2]), d[1].message_board))

    return output_list


@router.get("/friend_requests")
async def friend_requests(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

) -> List[Tuple[str, int]]:
    """
    obtain all the friend requests of the user
    """

    data_access = DataAccess(db)
    data = await data_access.UserAccess.getFriendRequests(user_id)

    """
    transform data to web format
    format: User -> (username, id)
    """
    output_list: List[Tuple[str, int]] = []
    for d in data:
        output_list.append((d[0].username, d[0].id))
    return output_list


@router.post("/friend_requests")
async def friend_requests(
        request: Request,
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db),



) -> str:
    """
    obtain all the friend requests of the user
    """
    data = await request.json()

    data_access = DataAccess(db)

    if data["accepted"]:
        await data_access.UserAccess.acceptFriendRequest(data["friend_id"], user_id)
    else:
        await data_access.UserAccess.rejectFriendRequest(data["friend_id"], user_id)
    await data_access.commit()
    return ""

