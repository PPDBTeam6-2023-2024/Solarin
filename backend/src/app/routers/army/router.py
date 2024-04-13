from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Annotated

from ...database.database import get_db
from ...database.database_access.army_access import *
from ..authentication.router import get_my_id
from .schemas import *
from ...database.database_access.data_access import DataAccess

router = APIRouter(prefix="/army", tags=["Army"])


@router.get("/armies", response_model=List[ArmySchema])
async def get_armies(
        planet_id: int,
        db=Depends(get_db)
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


@router.get("/troops")
async def get_troops(armyid: int, db=Depends(get_db)):
    """
    Retrieve the troops that are part of the army
    We will also retrieve the stats of the army itself, so we can display that.
    """
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.get_troops(armyid)

    troops_schema = []

    for troops in db_reply:
        temp = troops.to_armyconsistsof_schema()
        troops_schema.append(temp)

    army_stats = await data_access.ArmyAccess.get_army_stats(armyid)
    return {"troops": troops_schema, "stats": army_stats}


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


@router.post("/leave_city/{army_id}")
async def update_army_coordinates(
        userid: Annotated[int, Depends(get_my_id)],
        army_id: int,
        db=Depends(get_db)
):
    data_access = DataAccess(db)

    # Fetch current coordinates and speed of the army
    owner = await data_access.ArmyAccess.get_army_owner(army_id)
    if owner.id != userid:
        return {"success": False, "message": "user is not the owner of this army"}

    await data_access.ArmyAccess.leave_city(army_id)
    return {"success": True, "message": "User has left the city"}

@router.get("/armies_in_city/")
async def get_armies_in_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about the army in a city, including their troops.
    """
    data_access = DataAccess(db)
    army_id = await data_access.ArmyAccess.get_army_in_city(city_id)

    troops = await get_troops(army_id, db)
    troops.update({"army_id": army_id})
    return troops
