from fastapi import APIRouter, Depends
from typing import Annotated

import uuid

from ...routers.authentication.router import get_my_id
from ...database.database import get_db
from .planet_generation import generate_random_planet

router = APIRouter(prefix="/spawn", tags=["Spawn"])


@router.post("")
async def spawn_user(
        user_id: Annotated[str, Depends(get_my_id)],
        db=Depends(get_db)
) -> int:
    planet_id = await generate_random_planet(db)
    # create initial city for user

    return planet_id
