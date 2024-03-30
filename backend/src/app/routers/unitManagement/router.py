from fastapi import APIRouter, Depends, Query

from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List
from ..authentication.router import get_my_id
from ...database.database import get_db, AsyncSession
from ...database.models.models import *

router = APIRouter(prefix="/unit", tags=["City"])


@router.get("/train_cost/{unit_type}")
async def get_buildings(
        user_id: Annotated[int, Depends(get_my_id)],
        unit_type: int,
        db=Depends(get_db)
):
    """
    This endpoint will give back the training cost of a unit, based on the rank of the unit the user has
    """

    return ""
