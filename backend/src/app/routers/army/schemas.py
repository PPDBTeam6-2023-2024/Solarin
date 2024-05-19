from pydantic import BaseModel
from typing import Optional, List


class TroopTypeSchema(BaseModel):
    type: str
    training_time: int
    attack: int
    defense: int
    city_attack: int
    city_defense: int
    recovery: int
    speed: int
    required_rank: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ArmySchema(BaseModel):
    id: int
    user_id: int
    planet_id: Optional[int]
    x: float
    y: float

    class Config:
        orm_mode = True
        from_attributes = True


class ArmyUpdateSchema(BaseModel):
    x: float
    y: float


class ArmyConsistsOfSchema(BaseModel):
    army_id: int
    troop_type: str
    rank: int
    size: int

    class Config:
        orm_mode = True
        from_attributes = True


class TroopInfo(BaseModel):
    troop_type: str
    rank: int
    size: int
    army_id: int


class SplitInfo(BaseModel):
    to_split: List[TroopInfo]
