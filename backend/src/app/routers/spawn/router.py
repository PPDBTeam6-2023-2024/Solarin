from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy import UUID

from ...routers.authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.planet_access import PlanetAccess
from ...logic.planet_generation.planet_generation import generate_planet_random

router = APIRouter(prefix="/spawn", tags=["Spawn"])


@router.post("")
async def spawn_user(
        user_id: Annotated[UUID, Depends(get_my_id)],
        db=Depends(get_db)
) -> int:
    planet_access = PlanetAccess(db)

    generated_planet = generate_planet_random()


    generated_planet

    return