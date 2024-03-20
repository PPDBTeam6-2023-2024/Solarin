from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from ...database.database import get_db
from ...database.database_access.army_access import *
from ..authentication.router import get_my_id
from typing import List, Annotated
from .schemas import *
from ...database.database_access.data_access import DataAccess

router = APIRouter(prefix="/army", tags=["Army"])


@router.get("/armies", response_model=List[ArmySchema])
async def get_armies(
        userid: Annotated[int, Depends(get_my_id)],
        planet_id: int,
        db=Depends(get_db)
) -> List[ArmySchema]:
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.getArmies(userid, planet_id)

    armies_schema = []

    for armies in db_reply:
        for army in armies:
            temp = army.to_army_schema()
            armies_schema.append(temp)

    return armies_schema


@router.get("/troops", response_model=List[ArmyConsistsOfSchema])
async def get_troops(armyid: int, db=Depends(get_db)) -> List[ArmyConsistsOfSchema]:
    data_access = DataAccess(db)
    db_reply = await data_access.ArmyAccess.getTroops(armyid)

    troops_schema = []

    for troop_groups in db_reply:
        for troops in troop_groups:
            temp = troops.to_armyconsistsof_schema()
            troops_schema.append(temp)

    return troops_schema


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
