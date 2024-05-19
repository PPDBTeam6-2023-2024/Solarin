from fastapi import APIRouter, Depends
from ...database.database_access.data_access import DataAccess
from typing import Annotated, List, Tuple
from .schemas import BuildingInstanceSchema, CitySchema, BuildingTypeSchema, CostSchema, Confirmation, \
    ResourceStockSchema, StockOverViewSchema, CityInfoSchema, CityData
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession

from .city_checker import CityChecker

router = APIRouter(prefix="/cityManager", tags=["City"])


@router.get("/get_city_data/{city_id}", response_model=CityData)
async def get_city_and_building_info(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db=Depends(get_db)
) -> CityData:

    data_access = DataAccess(db)

    """
    do the city check, checking all the idle mechanics
    """
    city_checker = CityChecker(city_id, data_access)
    remaining_time_update_time_city,remaining_time_update_time_buildings = await city_checker.check_all()

    buildings = await data_access.BuildingAccess.get_city_buildings(city_id)

    """
    Initialize an empty list to store the building schemas
    """
    buildings_schemas = []

    """
    Make sure only the city owner can retrieve building information
    """
    city_owner = await data_access.CityAccess.get_city_controller(city_id) 
    if user_id != city_owner.id:
        return []

    """
    Iterate through each building, creating a BuildingInstanceSchema for each one
    """
    for building in buildings:
        remaining_update_time = 0
        if remaining_time_update_time_buildings.get(building.id) is not None:
            remaining_update_time = remaining_time_update_time_buildings[building.id]

        schema = building.to_schema(building.type.type, remaining_update_time)
        buildings_schemas.append(schema)

    maintenance_cost = await data_access.ResourceAccess.get_maintenance_city(city_id)
    maintenance_cost = [(k, v) for k, v in maintenance_cost.items()]

    """
    Get city info
    """
    city_info = await data_access.CityAccess.get_city_info(city_id)
    city_info_schema = CityInfoSchema(population=city_info[0], region_type=city_info[1],
                                      region_buffs=city_info[2], rank=city_info[3],
                                      remaining_update_time=remaining_time_update_time_city,
                                      maintenance_cost=maintenance_cost)

    """
    Return the city data, consisting of the building_schemas info and the city_info_schema
    """

    await data_access.commit()
    return CityData(city = city_info_schema, buildings = buildings_schemas)


@router.get("/cities/{planet_id}")
async def get_cities(
        planet_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    cities = await data_access.PlanetAccess.get_planet_cities(planet_id)

    """
    Iterate through each building, creating a BuildingInstanceSchema for each one
    """
    cities_schemas = []
    for city in cities:
        schema = city.to_city_schema().dict()
        schema["alliance"] = city.alliance
        cities_schemas.append(schema)
    """
    Return the list of BuildingInstanceSchema instances
    """
    return cities_schemas


@router.get("/new_building_types/{city_id}", response_model=List[BuildingTypeSchema])
async def get_new_building_types(
        city_id: int,
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    """
    dictionary with new building types, creation cost and whether the owner has sufficient funds
    """

    type_dict_list = await data_access.BuildingAccess.get_available_building_types(user_id, city_id)

    building_type_schema = []

    for row in type_dict_list:
        required_rank = row["required_rank"]
        if required_rank is None:
            required_rank = 0
        building_type_schema.append(BuildingTypeSchema(name=row['name'], type=row['type'], required_rank=required_rank,
                                                       costs=row['costs'], can_build=row['can_build']))

    return building_type_schema


@router.get("/get_upgrade_cost/{city_id}", response_model=Tuple[List[CostSchema], CostSchema])
async def get_upgrade_cost(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)
    """
    Get the city upgrade cost
    """

    city_cost_tuple = await data_access.CityAccess.get_city_upgrade_cost(city_id)
    city_upgrade_cost = CostSchema(id=city_id, costs=city_cost_tuple[0], time_cost=city_cost_tuple[1], can_upgrade=city_cost_tuple[2])

    """
    Get the upgrade costs of the buildings inside the city
    """
    buildings = await data_access.BuildingAccess.get_city_buildings(city_id)
    result = []

    for building in buildings:
        cost = await data_access.BuildingAccess.get_upgrade_cost(user_id, building.id)
        result.append(CostSchema(id=cost[0], costs=cost[1], time_cost=0, can_upgrade=cost[2]))

    return result,city_upgrade_cost

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

@router.post("/upgrade_city/{city_id}", response_model=Confirmation)
async def upgrade_city(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Upgrade the rank of city
    """
    data_access = DataAccess(db)
    data = await data_access.CityAccess.upgrade_city(user_id, city_id)

    await data_access.commit()
    return Confirmation(confirmed=data)


@router.get("/get_resource_stocks/{city_id}", response_model=StockOverViewSchema)
async def get_resource_stocks(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    returns a dictionary of all the resources stored in a given city
    key: building_id: the id of the building storing the resource
    value: a list tuples respresenting the resources stored: (resource_type, amount_in_storage, max_storage_capacity)
    """
    data_access = DataAccess(db)
    data = await data_access.BuildingAccess.get_resource_stocks(user_id,city_id)

    result_dict = dict()

    for building_id,stock_overview in data.items():
        stock_list = []
        for resource_stock in stock_overview:
            stock_list.append(ResourceStockSchema(resource_name=resource_stock[0], amount_in_stock=resource_stock[1], max_amount=resource_stock[2]))
        result_dict[building_id] = stock_list
    return StockOverViewSchema(overview=result_dict)

@router.get("/get_stats/{city_id}")
async def get_city_stats(city_id: int, db=Depends(get_db)):
    """
    get the attack and defense stat of a city + the army in it (if there is one)
    """
    data_access = DataAccess(db)
    city_stats = await data_access.CityAccess.get_cities_stats(city_id)
    c_army_id = await data_access.ArmyAccess.get_army_in_city(city_id)
    city_stats = await data_access.ArmyAccess.get_army_stats(c_army_id, city_stats)
    return city_stats
    

