from pydantic import BaseModel


class Region(BaseModel):
    region_type: str
    x: float
    y: float


class PlanetOut(BaseModel):
    name: str
    id: int
    planet_type: str
    regions: list[Region]
