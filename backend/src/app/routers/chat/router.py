from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy import UUID

from src.app.routers.authentication.router import get_my_id
from src.app.database import db
from .schemas import MessageIn, MessageOut

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/alliance")
async def get_messages(
        user_id: Annotated[UUID, Depends(get_my_id)],
        offset=Query(0),
        limit=Query(),
        db=Depends(db.get_db)
) -> list[MessageOut]:
    return


@router.post("/alliance")
async def add_message(
        user_id: Annotated[UUID, Depends(get_my_id)],
        message: MessageIn,
        db=Depends(db.get_db)
) -> MessageOut:
    return


@router.get("/{friend_id}")
async def get_messages(
        user_id: Annotated[UUID, Depends(get_my_id)],
        friend_id: int,
        offset=Query(0),
        limit=Query(),
        db=Depends(db.get_db)
) -> list[MessageOut]:
    return


@router.post("/{friend_id}")
async def add_message(
        user_id: Annotated[UUID, Depends(get_my_id)],
        friend_id: int,
        message: MessageIn,
        db=Depends(db.get_db)
) -> MessageOut:
    return

