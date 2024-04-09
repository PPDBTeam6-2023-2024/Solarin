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
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.get_armies_on_planet(planet_id)

    armies_schema = []

    for armies in db_reply:
        for army in armies:
            temp = army.to_army_schema()
            armies_schema.append(temp)
    return armies_schema


@router.get("/getarmy", response_model=ArmySchema)
async def get_army(
        army_id: int,
        db=Depends(get_db)
) -> ArmySchema:
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.getArmyById(army_id)

    army = db_reply.to_army_schema()

    return army


@router.get("/armies_outside", response_model=List[ArmySchema])
async def get_armies(
        userid: Annotated[int, Depends(get_my_id)],
        planet_id: int,
        db=Depends(get_db)
) -> List[ArmySchema]:
    """
    Tet the armies that are not inside a city

    """
    data_access = DataAccess(db)
    armies = await data_access.ArmyAccess.getArmies(userid, planet_id)

    armies_schema = []

    for army in armies:
        temp = army[0].to_army_schema()
        armies_schema.append(temp)

    return armies_schema


@router.get("/troops")
async def get_troops(armyid: int, db=Depends(get_db)):
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.getTroops(armyid)

    troops_schema = []

    for troop_groups in db_reply:
        for troops in troop_groups:
            temp = troops.to_armyconsistsof_schema()
            troops_schema.append(temp)

    army_stats = await data_access.ArmyAccess.get_army_stats(armyid)
    return {"troops": troops_schema, "stats": army_stats}


@router.post("/armies/{army_id}/update-coordinates")
async def update_army_coordinates(
        army_id: int,
        coordinates: ArmyUpdateSchema,
        db=Depends(get_db)
):
    data_access = DataAccess(db)

    # Fetch current coordinates and speed of the army
    army = await data_access.ArmyAccess.getArmyById(army_id)
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")

    # Update army coordinates
    success = await data_access.ArmyAccess.updateArmyCoordinates(army_id, coordinates.x, coordinates.y)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update army coordinates")

    # for now the traveltime is set to 1 until we implement the speed calculation and stuff
    return JSONResponse(content={"message": "Army coordinates updated successfully", "travel_time": 1}, status_code=200)


@router.get("/armies_user")
async def armies_user(
        user_id: Annotated[int, Depends(get_my_id)],
        db: AsyncSession = Depends(get_db)

):
    """
    send a list of all armies owned by a user
    """

    data_access = DataAccess(db)
    armies = await data_access.ArmyAccess.getUserArmies(user_id)
    armies_schemas = [army[0].to_army_schema() for army in armies]
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
    army_ids = await data_access.ArmyAccess.get_army_in_city(city_id)

    return await get_troops(army_ids[0], db)
