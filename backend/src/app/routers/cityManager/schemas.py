from pydantic import BaseModel


class ConfigClass(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True


class BuildingInstanceSchema(ConfigClass):
    id: int
    city_id: int
    building_type: str
    rank: int
    type: str

class CitySchema(ConfigClass):
    id: int
    region_id: int
    x: float
    y: float
    controlled_by: int
    rank: int
    region_type: str
    planet_name: str
    planet_id: int

class Confirmation(BaseModel):
    confirmed: bool


class PlanetRegion(ConfigClass):
    id: int
    planet_id: int
    region_type: str
    planet: str
    cities: str

class BuildingTypeSchema(ConfigClass):
    name: str
    type: str
    required_rank: int
    cost_type: str
    cost_amount: int
    can_build: bool

class CostSchema(ConfigClass):
    id: int
    cost: int
    cost_type: str
    can_upgrade: bool

class CityLocationSchema(BaseModel):
    x: float
    y: float
