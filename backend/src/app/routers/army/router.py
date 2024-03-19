from fastapi import APIRouter, Depends, Query

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
async def get_troops(armyid: int):
    troops_db = await ArmyAccess.getTroops(armyid)

    troops = [ArmyConsistsOfSchema.from_orm(troop) for troop in troops_db]

    return troops
