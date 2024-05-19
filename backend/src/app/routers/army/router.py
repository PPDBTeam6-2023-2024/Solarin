from fastapi import APIRouter, Depends
from typing import Annotated

from ...database.database import get_db
from ...database.database_access.army_access import *
from ..authentication.router import get_my_id
from .schemas import *
from ...database.database_access.data_access import DataAccess

from ..cityManager.city_checker import CityChecker

router = APIRouter(prefix="/army", tags=["Army"])


@router.get("/fleets_in_space", response_model=List[ArmySchema])
async def get_fleets(db: AsyncSession = Depends(get_db)) -> List[ArmySchema]:
    """
    Endpoint to retrieve fleet information (armies in space)
    """
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.get_fleets_in_space()

    armies_schema = []

    for army in db_reply:
        temp = army.to_army_schema()
        armies_schema.append(temp)

    return armies_schema


@router.get("/fleets", response_model=List[ArmySchema])
async def get_user_fleets(user_id: int, planet_id: int, db: AsyncSession = Depends(get_db)) -> List[ArmySchema]:
    """
    Endpoint to retrieve fleet information (armies in space)
    """
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.get_user_fleets_on_planet(user_id, planet_id)

    armies_schema = []

    for army in db_reply:
        temp = army.to_army_schema()
        armies_schema.append(temp)

    return armies_schema


@router.get("/armies", response_model=List[ArmySchema])
async def get_armies(
        planet_id: int,
        db: AsyncSession = Depends(get_db)
) -> List[ArmySchema]:
    """
    Endpoint to retrieve army information
    This endpoint is used for proper testing of the backend, and can be used to retrieve the armies if needed
    """

    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.get_armies_on_planet(planet_id)

    armies_schema = []

    for army in db_reply:
        temp = army.to_army_schema()
        armies_schema.append(temp)

    return armies_schema


@router.get("/troops/{army_id}")
async def get_troops(
        user_id: Annotated[int, Depends(get_my_id)],
        army_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieve the troops that are part of the army
    We will also retrieve the stats of the army itself, so we can display that.
    """

    data_access = DataAccess(db)

    db_reply = await data_access.ArmyAccess.get_troops(army_id)

    troops_schema = []

    for troops in db_reply:
        temp = troops.to_armyconsistsof_schema()
        troops_schema.append(temp)

    army_stats = await data_access.ArmyAccess.get_army_stats(army_id)

    """
    When accessing the troops of another army, we will make sure that the stats are unknown.
    We will also make sure that the army amounts are unknown
    """
    army_owner = await data_access.ArmyAccess.get_army_owner(army_id)
    if army_owner.id != user_id:
        """
        The values we send will be -1, frontend will replace it by a question mark
        """
        for k, v in army_stats.items():
            army_stats[k] = -1

        for i, t in enumerate(troops_schema):
            t.size = -1
            troops_schema[i] = t

    general = await data_access.GeneralAccess.get_general(army_id)
    if general is not None:
        modifiers = await data_access.GeneralAccess.get_modifiers(user_id, general.name)
        modifiers = [m[0].to_scheme(m[1]) for m in modifiers]
        general = general.to_scheme().dict()
        general.update({"modifiers": modifiers})

    maintenance_cost = await data_access.ResourceAccess.get_maintenance_army(army_id)
    maintenance_cost = [(k, v) for k, v in maintenance_cost.items()]

    return {"troops": troops_schema, "stats": army_stats, "general": general, "maintenance": maintenance_cost}


@router.get("/armies_user")
async def armies_user(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

):
    """
    send a list of all armies owned by the provided user
    """

    data_access = DataAccess(db)
    armies = await data_access.ArmyAccess.get_user_armies(user_id)
    armies_schemas = [army.to_army_schema() for army in armies]
    return armies_schemas


@router.get("/army_in_city/{city_id}")
async def get_armies_in_city(
        user_id: Annotated[int, Depends(get_my_id)],
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about the army in a city, including their troops.
    """
    data_access = DataAccess(db)

    army_id = await data_access.ArmyAccess.get_army_in_city(city_id)

    """
    do the city check, checking all the idle mechanics
    """
    ch = CityChecker(city_id, data_access)
    await ch.check_all()

    troops = await get_troops(user_id, army_id, db)

    maintenance_cost = await data_access.ResourceAccess.get_maintenance_army(army_id)
    maintenance_cost = [(k, v) for k, v in maintenance_cost.items()]

    """
    Add the army_id, because this is useful information, for army actions
    """
    troops.update({"army_id": army_id, "maintenance": maintenance_cost})

    await data_access.commit()

    return troops


@router.post("/split_army/{army_id}", response_model=int)
async def split_army(
        user_id: Annotated[int, Depends(get_my_id)],
        army_id: int,
        split_data: SplitInfo,
        db: AsyncSession = Depends(get_db)
):
    """
    Split a subset of the army of and form a new army with it.
    If the main army is inside a city, have the new_army leave the city
    """
    data_access = DataAccess(db)
    troops_list = split_data.to_split
    if len(troops_list) == 0:
        return

    new_army_id = await data_access.ArmyAccess.split_army(troops_list, troops_list[0].army_id, user_id)

    return new_army_id