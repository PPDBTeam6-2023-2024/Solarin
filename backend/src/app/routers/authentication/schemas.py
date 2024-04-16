from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class MessageToken(BaseModel):
    sender_id: int
    message_board: int
    body: str


class BattleStats(BaseModel):
    attack: int
    defense: int
    city_attack: int
    city_defense: int
    recovery: int
    speed: float



