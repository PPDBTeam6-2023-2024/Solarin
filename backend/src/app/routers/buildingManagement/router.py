from fastapi import APIRouter, Depends, Query, HTTPException
from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession
from ...database.models import *
from ..cityManager.schemas import Confirmation
router = APIRouter(prefix="/building", tags=["City"])


@router.get("/training_queue/{building_id}")
async def get_training_queue(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):

    """
    do a training progress check
    """
    da = DataAccess(db)

    """
    check if the user owns the building
    """
    is_owner = await da.BuildingAccess.is_owner(user_id, building_id)
    if not is_owner:
        return []

    """
    Check the current state of the queue, (check if troops are done training)
    """
    await da.TrainingAccess.check_queue(building_id)
    await da.BuildingAccess.checked(building_id)
    await da.commit()

    """
    retrieve training queue of a specific building
    """
    da = DataAccess(db)
    training_queue: List[TrainingQueue] = await da.TrainingAccess.get_queue(building_id)

    output = [t[0].toTrainingQueueEntry(t[1]) for t in training_queue]
    return output


@router.post("/create_new_building/{city_id}/{building_type}")
async def create_building(
        city_id: int,
        building_type: str,
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
):
    """
    this endpoint will create a new building
    """
    data_access = DataAccess(db)
    building_id = await data_access.BuildingAccess.create_building(user_id, city_id, building_type)
    await data_access.commit()

    if not building_id:
        raise HTTPException(status_code=400, detail="Building could not be created.")
    
    if building_type == "space-dock":
        planet = await data_access.PlanetAccess.get_planet_from_city_id(city_id)
        planet.visible = True
        await data_access.commit()


@router.get("/get_rates/{city_id}")
async def get_rates(user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db=Depends(get_db)):
    data_access = DataAccess(db)

    """
    Retrieve the production rates of the builings inside a city
    """

    buildings = await data_access.BuildingAccess.get_city_buildings(city_id)

    stats_dict = {}
    for b in buildings:
        stats = await data_access.BuildingAccess.get_production_building_stats(user_id, b.id)
        stats_dict[b.id] = stats

    return stats_dict


@router.post("/collect/{building_id}", response_model=Confirmation)
async def collect_resource(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):
    """
    Collect resources from specific building
    """
    data_access = DataAccess(db)
    updated_stock: list = await data_access.BuildingAccess.collect_resources(user_id, building_id, True)

    if len(updated_stock) == 0:
        raise HTTPException(status_code=400, detail="Resources could not be updated or created.")
    return Confirmation(confirmed=True)


@router.post("/upgrade_building/{building_id}", response_model=Confirmation)
async def upgrade_building(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):
    """
    Upgrade a specific building
    """
    data_access = DataAccess(db)
    confirmed = await data_access.BuildingAccess.upgrade_building(user_id, building_id)
    if not confirmed:
        raise HTTPException(status_code=400, detail="Building could not be upgraded.")
    return Confirmation(confirmed=confirmed)


@router.get("/get_stats/")
async def get_tower_wall_stats(db=Depends(get_db)):
    """
    get the base stats of all the different types of walls and towers
    """
    data_access = DataAccess(db)
    result = await data_access.BuildingAccess.get_base_stats()

    await data_access.commit()
    return result


@router.get("/get_production/")
async def get_production_stats(db=Depends(get_db)):
    """
    get the different types of production buildings and what they produce
    """
    data_access = DataAccess(db)
    result = await data_access.BuildingAccess.get_prod_stats()
    formatted_result = {}
    for item in result:
        building, resource, amount = item
        if building not in formatted_result:
            formatted_result[building] = []
        formatted_result[building].append({"resource": resource, "amount": amount})
    return formatted_result
