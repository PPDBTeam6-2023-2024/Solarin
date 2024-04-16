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
    confirmed = await data_access.BuildingAccess.collect_resources(user_id, building_id)
    if not confirmed:
        raise HTTPException(status_code=400, detail="Resources could not be updated or created.")
    return Confirmation(confirmed=confirmed)


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
