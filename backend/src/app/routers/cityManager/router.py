from fastapi import APIRouter, Depends, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from .schemas import BuildingInstanceSchema, CitySchema, PlanetRegion, CityLocationSchema, BuildingTypeSchema, Confirmation, CostSchema, CreateCitySchema
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
    buildings = await data_access.BuildingAccess.get_city_buildings(city_id)

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
    cities = await data_access.PlanetAccess.get_planet_cities(planet_id)

    # Initialize an empty list to store the building schemas
    cities_schemas = []

    # Iterate through each building, creating a BuildingInstanceSchema for each one
    cities_schemas = [city.to_city_schema() for city in cities]
    # Return the list of BuildingInstanceSchema instances
    return cities_schemas

@router.get("/new_building_types", response_model=List[BuildingTypeSchema])
async def get_new_building_types(
        city_id: int,
        city_rank: int,
        user_id: Annotated[int, Depends(get_my_id)],
        db = Depends(get_db)
):
    data_access = DataAccess(db)
    # dictionary with new building types, creation cost and whether the owner has sufficient funds
    type_dict_list = await data_access.BuildingAccess.get_available_building_types( user_id, city_id, city_rank)

    building_type_schema = []

    for row in type_dict_list:
        required_rank = row["required_rank"]
        if required_rank is None:
            required_rank = 0
        building_type_schema.append(BuildingTypeSchema(name = row['name'], type = row['type'], required_rank = required_rank,
                           costs = row['costs'], can_build = row['can_build']))



    return building_type_schema

@router.post("/create_new_building")
async def create_building(
        city_id: int,
        building_type: str,
        user_id: Annotated[int, Depends(get_my_id)],
        db = Depends(get_db)
):
    data_access = DataAccess(db)
    building_id = await data_access.BuildingAccess.create_building(user_id, city_id, building_type)
    await data_access.commit()

    if not building_id:
        raise HTTPException(status_code=400, detail="Building could not be created.")


@router.get("/collect", response_model=Confirmation)
async def collect_resource(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    confirmed = await data_access.BuildingAccess.collect_resources(user_id, building_id)
    if not confirmed:
        raise HTTPException(status_code=400, detail="Resources could not be updated or created.")
    return Confirmation(confirmed=confirmed)

@router.get("/upgrade_building", response_model=Confirmation)
async def upgrade_building(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    confirmed = await data_access.BuildingAccess.upgrade_building(user_id, building_id)
    if not confirmed:
        raise HTTPException(status_code=400, detail="Building could not be upgraded.")
    return Confirmation(confirmed=confirmed)


@router.get("/get_upgrade_cost", response_model=List[CostSchema])
async def get_upgrade_cost(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    buildings = await get_buildings(city_id, db=db)
    result = []

    for building in buildings:
        cost = await data_access.BuildingAccess.get_upgrade_cost(user_id, building.id)
        result.append(CostSchema(id=cost[0], costs=cost[1], can_upgrade=cost[2]))
    if not cost:
        raise HTTPException(status_code=400, detail="Upgrade cost could not be retrieved.")

    return result


@router.post("/create_city")
async def create_city(
        user_id: Annotated[int, Depends(get_my_id)],
        create_city_scheme: CreateCitySchema,
        db=Depends(get_db)
):
    data_access = DataAccess(db)

    """
    Create the new city
    """

    planet_id, x, y = await data_access.ArmyAccess.get_current_position(create_city_scheme.army_id)

    city_id = await data_access.CityAccess.create_city(planet_id, user_id, x, y)

    await data_access.commit()
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
    data = await data_access.CityAccess.get_cities_by_controller(user_id)

    cities_schemas = [city.to_city_schema() for city in data]

    return cities_schemas
