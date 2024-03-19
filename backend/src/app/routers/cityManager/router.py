from fastapi import APIRouter, Depends, Query

from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from .schemas import BuildingInstanceSchema, CitySchema, PlanetRegion

router = APIRouter(prefix="/cityManager", tags=["City"])


@router.get("/buildings", response_model=List[BuildingInstanceSchema])
async def get_buildings(
        city_id: int,
        db=Depends(get_db)
) -> List[BuildingInstanceSchema]:
    data_access = DataAccess(db)
    buildings = await data_access.BuildingAccess.getCityBuildings(city_id)

    # Initialize an empty list to store the building schemas
    buildings_schemas = []

    # Iterate through each building, creating a BuildingInstanceSchema for each one
    for building in buildings:
        schema = BuildingInstanceSchema.from_orm(building[0])
        buildings_schemas.append(schema)

    # Return the list of BuildingInstanceSchema instances

    return buildings_schemas


@router.get("/cities", response_model=List[CitySchema])
async def get_cities(
        planet_id: int,
        db=Depends(get_db)
) -> List[CitySchema]:
    data_access = DataAccess(db)
    cities = await data_access.PlanetAccess.getPlanetCities(planet_id)

    # Initialize an empty list to store the building schemas
    cities_schemas = []

    # Iterate through each building, creating a BuildingInstanceSchema for each one
    cities_schemas = [city[0].to_city_schema() for city in cities]

    # Return the list of BuildingInstanceSchema instances
    return cities_schemas
