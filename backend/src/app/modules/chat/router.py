from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy import UUID

from src.app.modules.authentication.router import get_my_id
from src.app.database import db

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/alliance")
async def get_messages(user_id: Annotated[UUID, Depends(get_my_id)], db=Depends(db.get_db)):
    return


@router.post("/alliance")
async def add_message(user_id: Annotated[UUID, Depends(get_my_id)], db=Depends(db.get_db)):
    return


@router.get("/{friend_id}")
async def get_messages(user_id: Annotated[UUID, Depends(get_my_id)], friend_id, db=Depends(db.get_db)):
    return


@router.post("/{friend_id}")
async def add_message(user_id: Annotated[UUID, Depends(get_my_id)], friend_id,  db=Depends(db.get_db)):
    return

