from fastapi import APIRouter, Depends, Query, HTTPException

from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from .schemas import BuildingInstanceSchema, CitySchema, PlanetRegion, BuildingTypeSchema
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

@router.get("/new_building_types", response_model=List[BuildingTypeSchema])
async def get_new_building_types(
        city_id: int,
        city_rank: int,
        db = Depends(get_db)
):
    data_access = DataAccess(db)
    new_building_type_list = await data_access.BuildingAccess.getAvailableBuildingTypes(city_id,city_rank)

    building_type_schema = [new_building_type[0].to_schema() for new_building_type in new_building_type_list]

    return building_type_schema

@router.post("/create_new_building")
async def create_building(
        city_id: int,
        building_type: str,
        db = Depends(get_db)
):
    data_access = DataAccess(db)
    building_id = await data_access.BuildingAccess.createBuilding(city_id, building_type)

    print(building_id)

    if not building_id:
        raise HTTPException(status_code=400, detail="Building could not be created.")





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
