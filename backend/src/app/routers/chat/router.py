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
from .friend_request_handler import FriendRequestHandler
from ..authentication.schemas import MessageToken

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = ConnectionManager()

security = HTTPBearer()


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
    messages = await data_access.MessageAccess.getMessages(board_id, 0, 10)
    output_list: List[MessageOut] = []
    for d in messages:
        output_list.append(d[0].toMessageOut(d[1]).model_dump())

    await websocket.send_json({"type": "paging", "message": output_list})

    connection_pool = await manager.connect_board(board_id=board_id, websocket=websocket)

    """
    start receiving new requests
    """
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

            if data["type"] == "paging":
                limit = data["limit"]
                offset = data["offset"]

                messages = await data_access.MessageAccess.getMessages(board_id, offset, limit)

                """
                don't send empty paging answers
                """
                if len(messages) == 0:
                    continue

                output_list: List[MessageOut] = []
                for d in messages:
                    output_list.append(d[0].toMessageOut(d[1]).model_dump())

                await websocket.send_json({"type": "paging", "message": output_list})

    except WebSocketDisconnect:
        connection_pool.disconnect(websocket)


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
    data = await data_access.MessageAccess.getFriendMessageOverview(user_id)

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

):
    """
    obtain all the friend requests of the user or add new friend requests
    """
    data = await request.json()

    """
    use FriendRequestHandler to handle the data
    """

    try:
        fh = FriendRequestHandler(data, db)
        success, message = await fh.handle(user_id)

    except Exception as e:
        success = False
        message = e

    return {"success": success, "message": message}


@router.post("/create_alliance")
async def create_alliance(
        request: Request,
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db),

) -> dict:
    """
    obtain all the friend requests of the user
    """
    data = await request.json()

    data_access = DataAccess(db)

    alliance_name = data["alliance_name"]

    alliance_exists = await data_access.AllianceAccess.allianceExists(alliance_name)
    if alliance_exists:
        return {"success": False, "message": "Alliance name already in use"}

    await data_access.AllianceAccess.createAlliance(alliance_name)
    await data_access.AllianceAccess.setAlliance(user_id, alliance_name)
    await data_access.commit()
    return {"success": True, "message": "Alliance is created"}

@router.post("/join_alliance")
async def join_alliance(
        request: Request,
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db),

) -> dict:
    """
    obtain all the friend requests of the user
    """
    data = await request.json()
    data_access = DataAccess(db)
    alliance_name = data["alliance_name"]

    alliance_exists = await data_access.AllianceAccess.allianceExists(alliance_name)
    if not alliance_exists:
        return {"success": False, "message": "Alliance name already in use"}

    await data_access.AllianceAccess.sendAllianceRequest(user_id, alliance_name)
    await data_access.commit()
    return {"success": False, "message": "Alliance join request has been send"}


@router.get("/alliance_requests")
async def alliance_requests(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

) -> List[Tuple[str, int]]:
    """
    obtain all the friend requests of the user
    """

    data_access = DataAccess(db)
    data = await data_access.AllianceAccess.getAllianceRequests(user_id)

    """
    transform data to web format
    format: User -> (username, id)
    """
    output_list: List[Tuple[str, int]] = []
    for d in data:
        output_list.append((d[0].username, d[0].id))
    return output_list

@router.post("/alliance_requests")
async def alliance_requests(
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
        alliance = await data_access.AllianceAccess.getAlliance(user_id)
        await data_access.AllianceAccess.acceptAllianceRequest(data["user_id"], alliance)
    else:
        await data_access.AllianceAccess.rejectAllianceRequest(data["user_id"])
    await data_access.commit()

    return ""

@router.get("/alliance_messageboard")
async def alliance_messageboard(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

) -> int:
    data_access = DataAccess(db)

    alliance = await data_access.AllianceAccess.getAlliance(user_id)
    message_board = await data_access.MessageAccess.getAllianceMessageBoard(alliance)
    return message_board

@router.get("/ranking")
async def get_ranking(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

) -> List[Tuple[str, int]]:
    """
    get the ranking of users, based on the amount of Solarium they have
    """

    data_access = DataAccess(db)
    ranking = await data_access.RankingAccess.getTopRanking(30)
    return ranking

@router.websocket("/wss")
async def websocket_test(
        websocket: WebSocket
):

    await websocket.accept()
