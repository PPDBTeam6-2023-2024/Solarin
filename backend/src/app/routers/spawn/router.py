from fastapi import APIRouter, Depends
from typing import Annotated

import uuid

from ...routers.authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.planet_access import PlanetAccess
from .region_generation import generate_regions

router = APIRouter(prefix="/spawn", tags=["Spawn"])


@router.post("")
async def spawn_user(
        user_id: Annotated[str, Depends(get_my_id)],
        db=Depends(get_db)
) -> int:
    planet_access = PlanetAccess(db)

    region_id = await planet_access.createSpaceRegion(
        region_name="region1"
    )

    planet_id = await planet_access.createPlanet(
        planet_name=str(uuid.uuid4()),
        planet_type=generated_planet.type.value,
        space_region_id=region_id
    )



    return