from pydantic import BaseModel
from enum import Enum


class RegionType(Enum):
    SNOWY="snowy"


class Region(BaseModel):
    type: RegionType
    x: int
    y: int


class Planet(BaseModel):
    width: int
    height: int
    regions: list[Region]

