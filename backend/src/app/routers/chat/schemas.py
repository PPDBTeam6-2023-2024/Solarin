from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageIn(BaseModel):
    body: str
    parent: Optional[int]


class ParentMessage(BaseModel):
    id: int
    body: str


class MessageOut(BaseModel):
    sender_name: str
    created_at: datetime
    body: str
    parent_message: Optional[ParentMessage]
