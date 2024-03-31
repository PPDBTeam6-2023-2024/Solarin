from fastapi import APIRouter, Depends, Query, Request

from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession
from ...database.models.models import *

router = APIRouter(prefix="/unit", tags=["City"])


@router.get("/train_cost/{unit_type}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        unit_type: str,
        db=Depends(get_db)
):
    """
    This endpoint will give back the training cost of a unit, based on the rank of the unit the user has
    """

    da = DataAccess(db)

    cost_list = await da.TrainingAccess.get_troop_cost(user_id, unit_type)
    return cost_list


@router.post("/train/{building_id}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        request: Request,
        building_id: int,
        db=Depends(get_db)
):
    """
    This endpoint will give back the training cost of a unit, based on the rank of the unit the user has
    """

    data = await request.json()
    da = DataAccess(db)
    troop_type = data["type"]
    amount = int(data["amount"])

    """
    re-check current training progress
    """
    await da.TrainingAccess.check_queue(building_id)
    await da.BuildingAccess.checked(building_id)
    await da.commit()

    rank = await da.TrainingAccess.get_troop_rank(user_id, troop_type)
    await da.TrainingAccess.trainType(1, building_id, troop_type, rank, amount)
    await da.commit()

    """
    return all the training queue entries, combined with a status and message indicating if the training was successfully
    """
    da = DataAccess(db)
    training_queue: List[TrainingQueue] = await da.TrainingAccess.get_queue(building_id)

    output = [t[0].toTrainingQueueEntry(t[1]) for t in training_queue]
    return {"queue": output, "success": True, "message": ""}
