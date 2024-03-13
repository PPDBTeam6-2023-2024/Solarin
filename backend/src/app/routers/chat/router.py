from fastapi import APIRouter, Depends, Query
from typing import Annotated, Tuple, List
from sqlalchemy import UUID

from ...routers.authentication.router import get_my_id
from ...database.database import get_db
from .schemas import MessageIn, MessageOut
from ...database.database_access.data_access import DataAccess
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/alliance")
async def get_messages(
        user_id: Annotated[UUID, Depends(get_my_id)],
        offset=Query(0),
        limit=Query(),
        db=Depends(get_db)
) -> list[MessageOut]:
    return


@router.post("/alliance")
async def add_message(
        user_id: Annotated[UUID, Depends(get_my_id)],
        message: MessageIn,
        db=Depends(get_db)
) -> MessageOut:
    return


@router.get("/friend/{friend_id}")
async def get_messages(
        user_id: Annotated[UUID, Depends(get_my_id)],
        friend_id: int,
        offset=Query(0),
        limit=Query(),
        db=Depends(get_db)
) -> list[MessageOut]:
    return


@router.post("/friend/{friend_id}")
async def add_message(
        user_id: Annotated[UUID, Depends(get_my_id)],
        friend_id: int,
        message: MessageIn,
        db=Depends(get_db)
) -> MessageOut:
    return


@router.get("/dm_overview")
async def dm_overview(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[str, MessageOut]]:
    """
    Get information of the last 5 DM's between the user and other friends
    The Information we want: The user we DM with, the last message send between them
    """

    data_access = DataAccess(db)
    data = await data_access.MessageAccess.getFriendMessageOverview(user_id, 5)

    """
    transform data to web format
    """
    output_list: List[Tuple[str, MessageOut]] = []
    for d in data:
        output_list.append((d[0], d[1].toMessageOut(d[2])))

    return output_list
