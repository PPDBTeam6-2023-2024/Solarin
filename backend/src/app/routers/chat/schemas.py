from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class MessageType(Enum):
    CHAT = "chat"


class Message(BaseModel):
    type: MessageType


class Chat(Message):
    body: str
    parent: Optional[int] = None


class ParentMessage(BaseModel):
    id: int
    body: str


class MessageOut(BaseModel):
    sender_name: str
    created_at: datetime
    body: str
    parent_message: Optional[ParentMessage] = None

