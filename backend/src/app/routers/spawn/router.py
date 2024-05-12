from fastapi import APIRouter, Depends
from typing import Annotated
import random

from ...routers.authentication.router import get_my_id
from ...database.database import get_db
from .planet_generation import generate_random_planet
from datetime import datetime, timedelta

from ...database.database_access.data_access import DataAccess

router = APIRouter(prefix="/spawn", tags=["Spawn"])


@router.post("")
async def spawn_user(
        user_id: Annotated[str, Depends(get_my_id)],
        db=Depends(get_db)
) -> dict[str, int]:
    """
    Spawns a user on a planet.
    If the user already has a planet, the most recent planet is returned.
    If the user does not have a planet, a planet which was created within the last hour is returned.
    """

    data_access = DataAccess(db)
    planets = await data_access.PlanetAccess.get_planets_of_user(user_id)

    if planets:
        planet_id = max(planets, key=lambda planet: planet.created_at).id
        return {
            "planet_id": planet_id
        }

    delta = timedelta(hours=1)
    curr_time = datetime.utcnow()
    recent_planets = await data_access.PlanetAccess.get_planets_between_times(curr_time - delta, curr_time)

    if recent_planets:
        planet_id = recent_planets[0].id
    else:
        planet_id = await generate_random_planet(db)

    await data_access.ArmyAccess.create_army(user_id, planet_id, random.uniform(0, 1), random.uniform(0, 1))
    await db.commit()
    return {
        "planet_id": planet_id
    }