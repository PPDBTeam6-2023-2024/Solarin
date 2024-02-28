from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class MessageToken(BaseModel):
    sender_id: str
    message_board: int
    body: str
    parent_message_id: int = None



