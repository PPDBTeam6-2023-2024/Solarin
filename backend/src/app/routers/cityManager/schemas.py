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
    remaining_update_time: int

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
    population: int

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
    costs: list[dict]
    can_build: bool

class CostSchema(ConfigClass):
    id: int
    costs: list[tuple[str, int]]
    time_cost: int
    can_upgrade: bool

class CityLocationSchema(BaseModel):
    x: float
    y: float

class CreateCitySchema(BaseModel):
    army_id: int

class ResourceStockSchema(BaseModel):
    resource_name: str
    amount_in_stock: int
    max_amount: int

class StockOverViewSchema(BaseModel):
    overview: dict[int,list[ResourceStockSchema]]

class CityInfoSchema(BaseModel):
    population: int
    rank: int
    region_type: str
    region_buffs: list[tuple[str,float]]
    remaining_update_time: int

class CityData(BaseModel):
    city: CityInfoSchema
    buildings: list[BuildingInstanceSchema]

