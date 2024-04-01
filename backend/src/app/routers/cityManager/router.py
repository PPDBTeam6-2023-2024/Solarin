from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from .schemas import BuildingInstanceSchema, CitySchema, PlanetRegion, CityLocationSchema
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession

from .city_checker import CityChecker

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

    """
    do the city check, checking all the idle mechanics
    """
    city_checker = CityChecker(city_id, data_access)
    await city_checker.check_all()

    # Iterate through each building, creating a BuildingInstanceSchema for each one
    for building in buildings:
        schema = building[0].to_schema(building[1].type)
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


@router.post("/create_city")
async def create_city(
        user_id: Annotated[int, Depends(get_my_id)],
        planet_id: int,
        coordinates: CityLocationSchema,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    # TODO get the correct region id using the planet_id
    region_id = 1
    city_id = None
    city_id = await data_access.CityAccess.createCity(region_id, user_id, coordinates.x, coordinates.y)
    if city_id is not None:
        return JSONResponse(content={"message": "City was created successfully", "city_id": city_id},
                            status_code=200)

@router.get("/cities_user")
async def friend_requests(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

):
    """
    send a list of all cities controlled by a user
    """

    data_access = DataAccess(db)
    data = await data_access.CityAccess.getCitiesByController(user_id)

    cities_schemas = [city[0].to_city_schema() for city in data]

    return cities_schemas
