from fastapi import APIRouter, Depends
from typing import Annotated, Tuple, List, Optional

from ..authentication.router import get_my_id
from ...database.database import get_db
from ...database.database_access.data_access import DataAccess
from .schemas import PlanetOut, Region

router = APIRouter(prefix="/planet", tags=["Planet"])


@router.get("/planets")
async def get_planets(
        user_id: Annotated[int, Depends(get_my_id)],
        db=Depends(get_db)
) -> List[Tuple[int, str]]:
    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.getAllPlanets()

    return planets


@router.get("/{planet_id}")
async def get_planet(
        user_id: Annotated[int, Depends(get_my_id)],
        planet_id: int,
        db=Depends(get_db)
) -> Optional[PlanetOut]:
    data_access = DataAccess(db)
    planet = await data_access.PlanetAccess.getPlanet(planet_id)

    if not planet:
        return None

    return PlanetOut(
        id=planet.id,
        name=planet.name,
        planet_type=planet.planet_type,
        regions=[
            Region(
                region_type=region.region_type,
                x=region.x,
                y=region.y
            )
            for region in planet.regions
        ]
    )
