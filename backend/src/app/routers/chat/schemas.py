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


class MessageOut(BaseModel):
    sender_name: str
    created_at: str # datetime is not serializable, that is why we use datatime as a string representation
    body: str

