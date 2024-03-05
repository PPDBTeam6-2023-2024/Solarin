from pydantic import BaseModel
from enum import Enum
from typing import Optional


class MessageType(Enum):
    CHAT = "chat"


class Message(BaseModel):
    type: MessageType


class Chat(Message):
    body: str
    parent: Optional[int] = None
