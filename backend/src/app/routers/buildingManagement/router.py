from fastapi import APIRouter, Depends, Query

from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession
from ...database.models.models import *

router = APIRouter(prefix="/building", tags=["City"])


@router.get("/training_queue/{building_id}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        building_id: int,
        db=Depends(get_db)
):
    """
    retrieve training queue of a specific building
    """
    da = DataAccess(db)
    training_queue: List[TrainingQueue] = await da.TrainingAccess.get_queue(building_id)
    output = [t[0].toTrainingQueueEntry(t[1]) for t in training_queue]

    return output


