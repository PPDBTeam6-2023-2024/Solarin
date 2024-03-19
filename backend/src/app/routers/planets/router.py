from fastapi import APIRouter, Depends, Query
from ..authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from typing import Annotated, Tuple, List

router = APIRouter(prefix="/planet", tags=["Planet"])


@router.get("/planets")
async def get_planets(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[int, str]]:
    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.getAllPlanets()

    return planets

